"""Genera _meta/versions.md, _meta/versions.json y (con --checkpoint) _meta/last-sync.md.

Solo lectura sobre los repos del workspace: nunca hace fetch ni escribe en ellos.
Red solo detras de --npm (npm view) y --checkpoint (GET del changelog del sitio).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SITE_CHANGELOG_URL = "https://docs.wdk.tether.io/overview/changelog.md"
CHANGELOG_REL = "content/docs/overview/changelog.mdx"
RELEASE_RE = re.compile(r"(?:^[Rr]elease:\s+v?|release/v)(\d+\.\d+\.\d+)")
CALLOUT_RE = re.compile(r"These pages reflect `([^`]+)`")
HEADING_RE = re.compile(r"^###\s+([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})")
GITHUB_LINK_RE = re.compile(r"github\.com/tetherto/([^/\s)]+)/(?:releases/tag|tree)/v?(\d[^)\s]*)")
SCOPED_TAG_RE = re.compile(r"github\.com/[^/\s)]+/[^/\s)]+/releases/tag/(?:%40|@)([^/\s)]+)/([^/\s)]+?)-v(\d[^)\s]*)")
OTHER_GITHUB_RE = re.compile(r"github\.com/(?!tetherto/)([^/\s)]+)/([^/\s)]+)/(?:releases/tag|tree)/v?(\d[^)\s]*)")
VERSION_LINK_RE = re.compile(r"\*\*(.+?)\*\*\s*\(\[v?\d[^\]]*\]\((https?://[^)\s]+)\)\)")
NPM_LINK_RE = re.compile(r"npmjs\.com/package/((?:@[^/]+/)?[^/\s]+)/v/([^)\s]+)")
ENTRY_RE = re.compile(r"^\s*-\s+\*\*.+?\*\*\s*\(\[[^\]]*\]\([^)]*\)\):?\s*(.*)$")
LOCK_NAME_RE = re.compile(r"(?:^|/)node_modules/(@tetherto/[^/]+)$")
PNPM_VERSION_RE = re.compile(r"^lockfileVersion:\s*'?(\d+)")
PNPM_KEY_RE = re.compile(r"^  '?(@tetherto/[^@'\s]+)@(\d[^'(\s:]*)")
INSTALL_RE = re.compile(r"\b(?:npm\s+(?:install|i)|pnpm\s+(?:add|install)|yarn\s+add|bun\s+add)\b([^\n`]*)")
IMPORT_RE = re.compile(r"""(?:\bfrom\s+|\brequire\(\s*|\bimport\s+)['"](@[^'"]+)['"]""")
SCOPED_NAME_RE = re.compile(r"@[A-Za-z0-9][\w.-]*/[\w.-]+")
PLACEHOLDER_SCOPES = ("@your-org", "@example", "@myorg", "@my-org", "@acme")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)\s*(\w*)")
DEP_SECTIONS = ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies")
FOLDER_PACKAGES = {"core-module": "@tetherto/wdk", "cli": "@tetherto/wdk-cli"}
MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}
SUMMARY_LEN = 160
UNKNOWN = "unknown"


@dataclass(frozen=True)
class RepoState:
    name: str
    branch: str
    head: str
    head_date: str
    origin_head: str | None
    behind_origin: int | None
    ahead_origin: int | None
    release: str | None
    release_commit: str | None
    release_date: str | None
    ahead_of_release: int | None
    package_version: str | None
    dirty: bool


@dataclass(frozen=True)
class DocVersion:
    package: str
    version: str
    source: str


@dataclass(frozen=True)
class ChangelogEntry:
    date: str
    package: str
    version: str
    breaking: bool
    summary: str


# ---------------------------------------------------------------- versions

def version_key(v: str) -> tuple:
    """Orden semver: las prereleases van antes que la version final."""
    core, _, _build = v.strip().lstrip("v").partition("+")
    main, _, pre = core.partition("-")
    nums = tuple(int(n) for n in re.findall(r"\d+", main))
    if not pre:
        return (nums, 1, ())
    parts = tuple((0, int(p), "") if p.isdigit() else (1, 0, p) for p in pre.split("."))
    return (nums, 0, parts)


def compare(mine: str, documented: str) -> str:
    if mine.startswith("git:"):
        return "git"
    a, b = version_key(mine), version_key(documented)
    if a == b:
        return "al día"
    return "atrás" if a < b else "adelante"


def changes_between(entries: list[ChangelogEntry], package: str, mine: str, documented: str) -> list[ChangelogEntry]:
    low, high = version_key(mine), version_key(documented)
    return [e for e in entries if e.package == package and low < version_key(e.version) <= high]


# --------------------------------------------------------------------- git

def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _git_optional(repo: Path, *args: str) -> str | None:
    try:
        return _git(repo, *args) or None
    except subprocess.CalledProcessError:
        return None


def _count(repo: Path, rev_range: str) -> int:
    return int(_git(repo, "rev-list", "--count", rev_range))


def _find_release(repo: Path, branch: str) -> tuple[str, str, str] | None:
    log = _git(repo, "log", "--format=%H%x09%ad%x09%s", "--date=short", branch)
    for line in log.splitlines():
        sha, commit_date, subject = line.split("\t", 2)
        match = RELEASE_RE.search(subject)
        if match:
            return f"v{match.group(1)}", sha, commit_date
    return None


def _package_version(repo: Path, branch: str) -> str | None:
    raw = _git_optional(repo, "show", f"{branch}:package.json")
    if raw is None:
        return None
    try:
        version = json.loads(raw).get("version")
    except (json.JSONDecodeError, AttributeError):
        return None
    return version if isinstance(version, str) else None


def repo_state(repo: Path, branch: str = "main") -> RepoState:
    head = _git(repo, "rev-parse", branch)
    head_date = _git(repo, "log", "-1", "--format=%cd", "--date=short", branch)
    origin = f"origin/{branch}"
    origin_head = _git_optional(repo, "rev-parse", "--verify", "-q", origin)
    behind = _count(repo, f"{branch}..{origin}") if origin_head else None
    ahead = _count(repo, f"{origin}..{branch}") if origin_head else None
    release = _find_release(repo, branch)
    return RepoState(
        name=repo.name,
        branch=branch,
        head=head,
        head_date=head_date,
        origin_head=origin_head,
        behind_origin=behind,
        ahead_origin=ahead,
        release=release[0] if release else None,
        release_commit=release[1] if release else None,
        release_date=release[2] if release else None,
        ahead_of_release=_count(repo, f"{release[1]}..{branch}") if release else None,
        package_version=_package_version(repo, branch),
        dirty=bool(_git(repo, "--no-optional-locks", "status", "--porcelain")),
    )


# --------------------------------------------------------------- lockfiles

LockProblem = tuple[str, str]


def _npm_lock_versions(repo: Path) -> tuple[dict[str, list[str]], list[LockProblem]]:
    name = "package-lock.json"
    path = repo / name
    if not path.is_file():
        return {}, []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as error:
        return {}, [(name, f"no se pudo leer: {type(error).__name__}")]
    packages = data.get("packages") if isinstance(data, dict) else None
    if not isinstance(packages, dict):
        version = data.get("lockfileVersion") if isinstance(data, dict) else None
        return {}, [(name, f"formato no soportado: sin clave packages, lockfileVersion {version}")]
    top: dict[str, str] = {}
    nested: dict[str, list[str]] = {}
    for key, info in packages.items():
        match = LOCK_NAME_RE.search(key)
        version = info.get("version") if isinstance(info, dict) else None
        if not match or not isinstance(version, str):
            continue
        name = match.group(1)
        if key == f"node_modules/{name}":
            top[name] = version
        else:
            nested.setdefault(name, []).append(version)
    found: dict[str, list[str]] = {}
    for name in sorted(set(top) | set(nested)):
        ordered = ([top[name]] if name in top else []) + nested.get(name, [])
        found[name] = list(dict.fromkeys(ordered))
    return found, []


def _pnpm_lock_versions(repo: Path) -> tuple[dict[str, list[str]], list[LockProblem]]:
    name = "pnpm-lock.yaml"
    path = repo / name
    if not path.is_file():
        return {}, []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        return {}, [(name, f"no se pudo leer: {type(error).__name__}")]
    header = next((m for m in map(PNPM_VERSION_RE.match, lines) if m), None)
    if header is None or int(header.group(1)) < 9:
        found = header.group(1) if header else "ausente"
        return {}, [(name, f"formato no soportado: lockfileVersion {found}")]
    collected: dict[str, set[str]] = {}
    section = ""
    for line in lines:
        if line and not line[0].isspace() and line.endswith(":"):
            section = line[:-1]
            continue
        if section not in ("packages", "snapshots"):
            continue
        match = PNPM_KEY_RE.match(line)
        if match:
            collected.setdefault(match.group(1), set()).add(match.group(2))
    return {n: sorted(v, key=version_key, reverse=True) for n, v in sorted(collected.items())}, []


def _git_pins(repo: Path) -> dict[str, list[str]]:
    pins: dict[str, list[str]] = {}
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git")]
        if "package.json" not in files:
            continue
        try:
            data = json.loads((Path(root) / "package.json").read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        for section in DEP_SECTIONS:
            deps = data.get(section)
            for name, spec in (deps.items() if isinstance(deps, dict) else []):
                if not (name.startswith("@tetherto/") and isinstance(spec, str)):
                    continue
                if spec.startswith(("github:", "git+")):
                    ref = spec.partition("#")[2] or "HEAD"
                    pins.setdefault(name, [])
                    if f"git:{ref}" not in pins[name]:
                        pins[name].append(f"git:{ref}")
    return pins


def scan_lockfiles(repo: Path) -> tuple[dict[str, list[str]], list[LockProblem]]:
    """Paquetes `@tetherto/*` fijados y los lockfiles que no se pudieron leer: (archivo, motivo)."""
    found, problems = _npm_lock_versions(repo)
    pnpm, pnpm_problems = _pnpm_lock_versions(repo)
    for name, vers in pnpm.items():
        found[name] = list(dict.fromkeys(found.get(name, []) + vers))
    found.update(_git_pins(repo))
    return dict(sorted(found.items())), problems + pnpm_problems


def locked_packages(repo: Path) -> dict[str, list[str]]:
    return scan_lockfiles(repo)[0]


# -------------------------------------------------------------------- docs

def _callout_package(value: str, mdx: Path) -> tuple[str, str]:
    if value.startswith("@"):
        package, _, version = value.rpartition("@")
        return package, version.lstrip("v")
    folder = mdx.parent.name
    return FOLDER_PACKAGES.get(folder, f"@tetherto/wdk-{folder}"), value.lstrip("v")


def docs_callouts(docs: Path) -> dict[str, DocVersion]:
    found: dict[str, DocVersion] = {}
    for mdx in sorted((docs / "content" / "docs").rglob("*.mdx")):
        match = CALLOUT_RE.search(mdx.read_text(encoding="utf-8", errors="replace"))
        if not match:
            continue
        package, version = _callout_package(match.group(1), mdx)
        current = found.get(package)
        if current is None or version_key(version) > version_key(current.version):
            found[package] = DocVersion(package, version, f"callout:{mdx.relative_to(docs).as_posix()}")
    return found


def _wdk_name(spec: str) -> str | None:
    """Nombre `@scope/name` de un especificador (sin version ni subruta) si contiene `wdk`."""
    match = SCOPED_NAME_RE.match(spec.strip("'\""))
    if not match:
        return None
    scope, _, name = match.group(0).partition("/")
    return match.group(0) if "wdk" in name.lower() and scope not in PLACEHOLDER_SCOPES else None


def _without_removed_diff_lines(text: str) -> str:
    """Quita las lineas `-` de los bloques ```diff y une las continuaciones con `\\`."""
    kept: list[str] = []
    lang: str | None = None
    for line in text.splitlines():
        fence = FENCE_RE.match(line)
        if fence:
            lang = None if lang is not None else fence.group(1).lower()
        elif lang == "diff" and line.lstrip().startswith("-"):
            continue
        kept.append(line)
    return re.sub(r"\\\n\s*", " ", "\n".join(kept))


def docs_install_packages(docs: Path) -> dict[str, str]:
    """Paquetes `@scope/*wdk*` nombrados en comandos de instalacion o imports: paquete -> primera pagina."""
    root = docs / "content" / "docs"
    pages = sorted(p for pattern in ("*.mdx", "*.md") for p in root.rglob(pattern))
    found: dict[str, str] = {}
    for page in pages:
        text = _without_removed_diff_lines(page.read_text(encoding="utf-8", errors="replace"))
        specs = [t for m in INSTALL_RE.finditer(text) for t in m.group(1).split()]
        specs += [m.group(1) for m in IMPORT_RE.finditer(text)]
        for name in filter(None, map(_wdk_name, specs)):
            found.setdefault(name, page.relative_to(docs).as_posix())
    return found


def _plain_text(text: str) -> str:
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return text.replace("`", "").replace("**", "").strip()


def _entry_package(line: str) -> tuple[str, str] | None:
    """Paquete y version del link de version de la linea (o de la linea entera si no hay)."""
    link = VERSION_LINK_RE.search(line)
    target = link.group(2) if link else line
    candidates = []
    for regex, build in (
        (GITHUB_LINK_RE, lambda m: (f"@tetherto/{m.group(1)}", m.group(2))),
        (NPM_LINK_RE, lambda m: (m.group(1), m.group(2))),
        (SCOPED_TAG_RE, lambda m: (f"@{m.group(1)}/{m.group(2)}", m.group(3))),
        (OTHER_GITHUB_RE, lambda m: (f"github:{m.group(1)}/{m.group(2)}", m.group(3))),
    ):
        match = regex.search(target)
        if match:
            candidates.append((match.start(), build(match)))
    return min(candidates, key=lambda c: c[0])[1] if candidates else None


def _heading_date(line: str) -> str | None:
    match = HEADING_RE.match(line)
    if not match or match.group(1) not in MONTHS:
        return None
    return f"{match.group(3)}-{MONTHS[match.group(1)]:02d}-{int(match.group(2)):02d}"


def changelog_entries(text: str) -> list[ChangelogEntry]:
    entries: list[ChangelogEntry] = []
    current = ""
    for line in text.splitlines():
        heading = _heading_date(line)
        if heading:
            current = heading
            continue
        found = _entry_package(line) if current and line.lstrip().startswith("- ") else None
        if not found:
            continue
        body = ENTRY_RE.match(line)
        summary = _plain_text(body.group(1) if body else line)[:SUMMARY_LEN]
        entries.append(ChangelogEntry(current, found[0], found[1], "[Breaking]" in line, summary))
    return entries


def changelog_unmapped(text: str) -> list[str]:
    """Lineas del changelog con link de version pero sin paquete reconocido."""
    unmapped: list[str] = []
    current = ""
    for line in text.splitlines():
        current = _heading_date(line) or current
        link = VERSION_LINK_RE.search(line) if line.lstrip().startswith("- ") else None
        if link and not _entry_package(line):
            unmapped.append(f"{current or 'sin fecha'} · {_plain_text(link.group(1))}: {link.group(2)}")
    return unmapped


def changelog_top_date(text: str) -> str:
    for line in text.splitlines():
        heading = _heading_date(line)
        if heading:
            return heading
    return ""


def _read_changelog(docs: Path) -> str:
    path = docs / CHANGELOG_REL
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def _newest_per_package(entries: list[ChangelogEntry]) -> dict[str, DocVersion]:
    newest: dict[str, ChangelogEntry] = {}
    for entry in entries:
        current = newest.get(entry.package)
        if current is None or version_key(entry.version) > version_key(current.version):
            newest[entry.package] = entry
    return {p: DocVersion(p, e.version, f"changelog:{e.date}") for p, e in newest.items()}


def documented_versions(docs: Path) -> dict[str, DocVersion]:
    found = _newest_per_package(changelog_entries(_read_changelog(docs)))
    found.update(docs_callouts(docs))
    return dict(sorted(found.items()))


def documented_with_installs(documented: dict[str, DocVersion], installs: dict[str, str]) -> dict[str, DocVersion]:
    """Suma los paquetes que solo aparecen en comandos de instalacion, con version vacia."""
    extra = {p: DocVersion(p, "", f"install:{path}") for p, path in installs.items() if p not in documented}
    return dict(sorted({**documented, **extra}.items()))


def _merge_github_ids(catalog: dict[str, DocVersion]) -> dict[str, DocVersion]:
    """Un paquete solo de instalacion toma la version del id `github:<org>/<repo>` del mismo modulo."""
    by_repo = {p.rpartition("/")[2]: p for p in catalog if p.startswith("github:")}
    for package, doc in list(catalog.items()):
        github = by_repo.get(package.rpartition("/")[2])
        if doc.version or not github or package.startswith("github:"):
            continue
        found = catalog.pop(github)
        catalog[package] = DocVersion(package, found.version, f"{found.source} via {github}")
    return catalog


def _catalog(documented: dict[str, DocVersion], entries: list[ChangelogEntry]) -> dict[str, DocVersion]:
    catalog = _newest_per_package(entries)
    catalog.update(documented)
    return dict(sorted(_merge_github_ids(catalog).items()))


# ----------------------------------------------------------------- render

def _doc_cell(doc: DocVersion | None) -> str:
    if not doc:
        return "—"
    return f"{doc.version or '—'} ({doc.source})"


def _repos_table(states: list[RepoState]) -> list[str]:
    lines = [
        "## Repos: mi versión vs desplegada",
        "",
        "| repo | HEAD local | release desplegada (+N commits) | origin/main (atrás/adelante) | sucio |",
        "|---|---|---|---|---|",
    ]
    for s in states:
        if s.release:
            released = f"{s.release} + {s.ahead_of_release} commits ({s.release_date})"
        else:
            released = f"sin release (referencia: origin/{s.branch})"
        if s.origin_head is None:
            origin = f"sin origin/{s.branch}"
        else:
            origin = f"{s.origin_head[:7]}: atrás {s.behind_origin} / adelante {s.ahead_origin}"
        lines.append(f"| {s.name} | {s.head[:7]} ({s.head_date}) | {released} | {origin} | {'sí' if s.dirty else 'no'} |")
    return lines


def _range_cell(changes: list[ChangelogEntry]) -> str:
    breaking = [e for e in changes if e.breaking]
    if not breaking:
        return str(len(changes))
    return f"{len(changes)}, {len(breaking)} breaking: {', '.join(e.date for e in breaking)}"


def _package_row(package: str, mine: list[str], documented: dict[str, DocVersion],
                 entries: list[ChangelogEntry], npm_latest: dict[str, str]) -> tuple[str, list[ChangelogEntry]]:
    doc = documented.get(package)
    latest = npm_latest.get(package) or "—"
    if doc is None:
        status, changes_cell, changes = "sin documentar", "—", []
    elif mine[0].startswith("git:"):
        status, changes_cell, changes = "git", "—", []
    elif not doc.version:
        status, changes_cell, changes = "sin versión documentada", "—", []
    else:
        status = compare(mine[0], doc.version)
        changes = changes_between(entries, package, mine[0], doc.version) if status == "atrás" else []
        changes_cell = _range_cell(changes)
    row = f"| {package} | {', '.join(mine)} | {_doc_cell(doc)} | {latest} | {status} | {changes_cell} |"
    return row, changes


def _repo_sections(states: list[RepoState], locked_by_repo: dict[str, dict[str, list[str]]],
                   documented: dict[str, DocVersion], entries: list[ChangelogEntry],
                   npm_latest: dict[str, str],
                   lock_problems: dict[str, list[LockProblem]]) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    breaking_lines: list[str] = []
    for s in states:
        lines += [f"## {s.name}", ""]
        locked = locked_by_repo.get(s.name, {})
        problems = lock_problems.get(s.name, [])
        lines += [f"lockfile ilegible: {file} ({reason})" for file, reason in problems]
        if problems:
            lines.append("")
        if not locked:
            lines += [] if problems else ["Sin paquetes `@tetherto/*` fijados.", ""]
            continue
        lines += ["| paquete | mi versión | documentada (fuente) | npm latest | estado | cambios en el rango |",
                  "|---|---|---|---|---|---|"]
        for package, mine in locked.items():
            row, changes = _package_row(package, mine, documented, entries, npm_latest)
            lines.append(row)
            breaking_lines += [f"- {s.name} · {package} {e.version} ({e.date}): {e.summary}"
                               for e in changes if e.breaking]
        lines.append("")
    return lines, breaking_lines


def _catalog_table(catalog: dict[str, DocVersion], locked_by_repo: dict[str, dict[str, list[str]]],
                   npm_latest: dict[str, str]) -> list[str]:
    lines = [
        "## Catálogo: todos los paquetes documentados",
        "",
        "| paquete | documentada (fuente) | npm latest | lo uso en |",
        "|---|---|---|---|",
    ]
    for package, doc in catalog.items():
        used = [f"{repo} {', '.join(locked[package])}" for repo, locked in locked_by_repo.items() if package in locked]
        lines.append(f"| {package} | {_doc_cell(doc)} | {npm_latest.get(package) or '—'} | {'; '.join(used) or 'no instalado'} |")
    return lines


def render_versions_md(states: list[RepoState], locked_by_repo: dict[str, dict[str, list[str]]],
                       documented: dict[str, DocVersion], entries: list[ChangelogEntry],
                       npm_latest: dict[str, str], unmapped: list[str] | None = None,
                       lock_problems: dict[str, list[LockProblem]] | None = None) -> str:
    lines = [
        "# Versiones: mi versión vs desplegada vs documentada",
        "",
        "Archivo generado por `_meta/versions.py`; no se edita a mano. Los upstream de Tether son privados:",
        "no se puede ver una release posterior a la integrada en `origin/main` de cada repo.",
        "",
    ]
    lines += _repos_table(states) + [""]
    sections, breaking_lines = _repo_sections(
        states, locked_by_repo, documented, entries, npm_latest, lock_problems or {})
    lines += sections
    lines += ["## Cambios breaking entre mi versión y la documentada", ""]
    lines += (breaking_lines or ["Ninguno."]) + [""]
    lines += _catalog_table(_catalog(documented, entries), locked_by_repo, npm_latest) + [""]
    lines += ["## Entradas del changelog sin paquete reconocido", ""]
    lines += [f"- {item}" for item in unmapped or []] or ["Ninguna."]
    return "\n".join(lines) + "\n"


def render_last_sync(states: list[RepoState], docs_site: dict, analyzed_on: str) -> str:
    lines = [
        "# last-sync",
        "",
        "Punto de sincronización de cada fuente. Los upstream de Tether son privados: no se puede ver una",
        "release posterior a la integrada en `origin/main` de cada repo (`deployed_release`).",
    ]
    for s in states:
        lines += ["", f"## {s.name}", f"branch: {s.branch}", f"commit: {s.head}", f"date: {s.head_date}"]
        if s.release:
            lines += [f"deployed_release: {s.release}", f"release_commit: {s.release_commit}",
                      f"release_date: {s.release_date}", f"ahead_of_release: {s.ahead_of_release}"]
        else:
            lines.append(f"deployed_release: none (origin/{s.branch})")
        lines += [f"origin_main: {s.origin_head or 'none'}", f"behind_origin: {s.behind_origin if s.behind_origin is not None else 'none'}"]
        if s.name == "wdk-docs":
            lines += [f"{k}: {docs_site[k]}" for k in ("site_changelog_top", "repo_changelog_top", "site_matches_repo") if k in docs_site]
        lines.append(f"analyzed_on: {analyzed_on}")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------- IO

def _discover_repos(workspace: Path, vault: Path) -> list[Path]:
    return [d for d in sorted(workspace.iterdir()) if d.is_dir() and d.name != vault.name and (d / ".git").exists()]


def _analysis_branch(repo: Path) -> str:
    if _git_optional(repo, "rev-parse", "--verify", "-q", "main"):
        return "main"
    return _git_optional(repo, "symbolic-ref", "--short", "HEAD") or "main"


def _npm_latest_one(package: str) -> tuple[str, str]:
    try:
        result = subprocess.run(["npm", "view", package, "dist-tags.latest"],
                                capture_output=True, text=True, check=True, timeout=60)
        return package, result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return package, ""


def _fetch_npm_latest(packages: list[str]) -> dict[str, str]:
    with ThreadPoolExecutor(max_workers=8) as pool:
        return dict(pool.map(_npm_latest_one, packages))


def _site_changelog_top() -> str:
    try:
        request = urllib.request.Request(SITE_CHANGELOG_URL, headers={"User-Agent": "wdk-vault-versions/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            return changelog_top_date(response.read().decode("utf-8", errors="replace")) or UNKNOWN
    except (OSError, ValueError):
        return UNKNOWN


def _docs_site(repo_top: str) -> dict:
    site_top = _site_changelog_top()
    if UNKNOWN in (site_top, repo_top or UNKNOWN):
        matches = UNKNOWN
    else:
        matches = "yes" if site_top == repo_top else "no"
    return {"site_changelog_top": site_top, "repo_changelog_top": repo_top or UNKNOWN, "site_matches_repo": matches}


def main(argv: list[str], vault: Path = VAULT) -> int:
    parser = argparse.ArgumentParser(description="Genera _meta/versions.md y versions.json")
    parser.add_argument("--npm", action="store_true", help="consulta dist-tags.latest en npm")
    parser.add_argument("--checkpoint", action="store_true", help="escribe _meta/last-sync.md")
    args = parser.parse_args(argv)

    workspace = vault.parent
    docs = workspace / "wdk-docs"
    if not docs.is_dir():
        print(f"error: falta {docs}; clona https://github.com/tetherto/wdk-docs.git en el workspace", file=sys.stderr)
        return 2

    repos = _discover_repos(workspace, vault)
    states = [repo_state(r, _analysis_branch(r)) for r in repos]
    scans = {r.name: scan_lockfiles(r) for r in repos}
    locked_by_repo = {name: scan[0] for name, scan in scans.items()}
    lock_problems = {name: scan[1] for name, scan in scans.items() if scan[1]}
    changelog = _read_changelog(docs)
    entries = changelog_entries(changelog)
    unmapped = changelog_unmapped(changelog)
    for name, problems in lock_problems.items():
        for file, reason in problems:
            print(f"warning: {name}: lockfile ilegible {file} ({reason})", file=sys.stderr)
    for item in unmapped:
        print(f"warning: changelog sin paquete reconocido: {item}", file=sys.stderr)
    documented = documented_with_installs(documented_versions(docs), docs_install_packages(docs))
    catalog = _catalog(documented, entries)
    npm_latest = _fetch_npm_latest([p for p in catalog if not p.startswith("github:")]) if args.npm else {}

    packages = set(catalog) | set(documented) | {e.package for e in entries}
    for locked in locked_by_repo.values():
        packages.update(locked)
    today = date.today().isoformat()
    meta = vault / "_meta"
    (meta / "versions.md").write_text(
        render_versions_md(states, locked_by_repo, documented, entries, npm_latest, unmapped, lock_problems),
        encoding="utf-8")
    payload = {
        "generated": today,
        "repos": {s.name: {**asdict(s), "locked": locked_by_repo[s.name],
                         "lockfile_problems": [f"{f} ({r})" for f, r in lock_problems.get(s.name, [])]}
                  for s in states},
        "packages": sorted(packages),
    }
    (meta / "versions.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.checkpoint:
        site = _docs_site(changelog_top_date(changelog))
        (meta / "last-sync.md").write_text(render_last_sync(states, site, today), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
