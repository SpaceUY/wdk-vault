"""Genera _meta/versions.md, _meta/versions.json y (con --checkpoint) _meta/last-sync.md y _meta/indexado.json.

Con --cambios compara el estado actual contra la foto _meta/indexado.json y escribe _meta/cambios.md.

Solo lectura sobre los repos del workspace: nunca hace fetch ni escribe en ellos. Analiza
`origin/<rama>` (o la rama local si no hay origin) con `git show`/`git ls-tree`/`git archive`:
nunca lee el arbol de trabajo. Los repos salen de `_meta/repos.txt`.
Red solo detras de --npm (npm view), --org (API de GitHub) y --checkpoint (GET del changelog del sitio).
"""
import argparse
import http.client
import io
import itertools
import json
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SITE_CHANGELOG_URL = "https://docs.wdk.tether.io/overview/changelog.md"
ORG_REPOS_URL = "https://api.github.com/orgs/tetherto/repos?per_page=100&page={page}"
ORG_REPO_RE = re.compile(r"wdk|pear-wrk|tether-wrk", re.IGNORECASE)
USER_AGENT = "wdk-vault-versions/1.0"
SNAPSHOT = "indexado.json"
SNAPSHOT_MISSING = "no hay foto indexada; correr primero --checkpoint"
NO_CHANGES = "sin cambios"
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
PAGE_STATUS = {"A": "agregada", "M": "modificada", "D": "borrada", "R": "renombrada", "T": "modificada"}
CHANGELOG_REL = "content/docs/overview/changelog.mdx"
RELEASE_RE = re.compile(r"^(?![Rr]evert\b)(?:[Rr]elease:\s+v?|.*?release/v)(\d+\.\d+\.\d+)")
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
UNSCOPED_NAME_RE = re.compile(r"wdk-(?:protocol|wallet)-[\w.-]+")
MENTION_RE = re.compile(
    r"`(@[A-Za-z0-9][\w.-]*/[\w.-]+|[\w.-]+)@(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)`")
CALLOUT_BLOCK_RE = re.compile(r"<Callout\b[^>]*>(.*?)</Callout>", re.DOTALL)
BETA_VERSION_RE = re.compile(r"`(v\d+\.\d+\.\d+[^`\s]*)`")
PLACEHOLDER_SCOPES = ("@your-org", "@example", "@myorg", "@my-org", "@acme")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)\s*(\w*)")
DEP_SECTIONS = ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies")
FOLDER_PACKAGES = {"core-module": "@tetherto/wdk", "cli": "@tetherto/wdk-cli"}
MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}
SUMMARY_LEN = 160
UNKNOWN = "unknown"
NPM_404 = "no publicado (404)"
NPM_ERROR = "error"
NPM_VERSION_RE = re.compile(r"^v?\d+\.\d+\.\d+")
DOCS_ONLY = "docs-only"


@dataclass(frozen=True)
class RepoState:
    name: str
    branch: str
    analyzed_ref: str
    head: str
    head_date: str
    local_head: str
    local_head_date: str
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


def _commit_date(repo: Path, rev: str) -> str:
    return _git(repo, "log", "-1", "--format=%cd", "--date=short", rev)


def repo_state(repo: Path, branch: str = "main") -> RepoState:
    """Todo sale de `origin/<branch>` (o de la rama local si no hay origin); HEAD local solo para la brecha."""
    origin = f"origin/{branch}"
    origin_head = _git_optional(repo, "rev-parse", "--verify", "-q", origin)
    head = _git(repo, "rev-parse", origin if origin_head else branch)
    local_head = _git(repo, "rev-parse", "HEAD")
    behind = _count(repo, f"HEAD..{origin}") if origin_head else None
    ahead = _count(repo, f"{origin}..HEAD") if origin_head else None
    release = _find_release(repo, head)
    return RepoState(
        name=repo.name,
        branch=branch,
        analyzed_ref=origin if origin_head else f"{branch} (sin origin)",
        head=head,
        head_date=_commit_date(repo, head),
        local_head=local_head,
        local_head_date=_commit_date(repo, local_head),
        origin_head=origin_head,
        behind_origin=behind,
        ahead_origin=ahead,
        release=release[0] if release else None,
        release_commit=release[1] if release else None,
        release_date=release[2] if release else None,
        ahead_of_release=_count(repo, f"{release[1]}..{head}") if release else None,
        package_version=_package_version(repo, head),
        dirty=bool(_git(repo, "--no-optional-locks", "status", "--porcelain")),
    )


# --------------------------------------------------------------- lockfiles

LockProblem = tuple[str, str]
READ_ERRORS = (json.JSONDecodeError, subprocess.CalledProcessError, UnicodeDecodeError)


def _show(repo: Path, ref: str, path: str) -> str:
    """Contenido de `path` en `ref`; nunca el del arbol de trabajo."""
    result = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=repo, capture_output=True, check=True)
    return result.stdout.decode("utf-8")


def _tree_files(repo: Path, ref: str) -> set[str]:
    return set(filter(None, _git(repo, "ls-tree", "-r", "-z", "--name-only", ref).split("\0")))


def _npm_lock_versions(repo: Path, ref: str, files: set[str]) -> tuple[dict[str, list[str]], list[LockProblem]]:
    name = "package-lock.json"
    if name not in files:
        return {}, []
    try:
        data = json.loads(_show(repo, ref, name))
    except READ_ERRORS as error:
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


def _pnpm_lock_versions(repo: Path, ref: str, files: set[str]) -> tuple[dict[str, list[str]], list[LockProblem]]:
    name = "pnpm-lock.yaml"
    if name not in files:
        return {}, []
    try:
        lines = _show(repo, ref, name).splitlines()
    except (subprocess.CalledProcessError, UnicodeDecodeError) as error:
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


def _git_pins(repo: Path, ref: str, files: set[str]) -> dict[str, list[str]]:
    pins: dict[str, list[str]] = {}
    for path in sorted(files):
        parts = path.split("/")
        if parts[-1] != "package.json" or "node_modules" in parts:
            continue
        try:
            data = json.loads(_show(repo, ref, path))
        except READ_ERRORS:
            continue
        if not isinstance(data, dict):
            continue
        for section in DEP_SECTIONS:
            deps = data.get(section)
            for name, spec in (deps.items() if isinstance(deps, dict) else []):
                if not (name.startswith("@tetherto/") and isinstance(spec, str)):
                    continue
                if spec.startswith(("github:", "git+")):
                    pin = spec.partition("#")[2] or "HEAD"
                    pins.setdefault(name, [])
                    if f"git:{pin}" not in pins[name]:
                        pins[name].append(f"git:{pin}")
    return pins


def scan_lockfiles(repo: Path, ref: str = "HEAD") -> tuple[dict[str, list[str]], list[LockProblem]]:
    """Paquetes `@tetherto/*` fijados en `ref` y los lockfiles que no se pudieron leer: (archivo, motivo)."""
    files = _tree_files(repo, ref)
    found, problems = _npm_lock_versions(repo, ref, files)
    pnpm, pnpm_problems = _pnpm_lock_versions(repo, ref, files)
    for name, vers in pnpm.items():
        found[name] = list(dict.fromkeys(found.get(name, []) + vers))
    found.update(_git_pins(repo, ref, files))
    return dict(sorted(found.items())), problems + pnpm_problems


def locked_packages(repo: Path, ref: str = "HEAD") -> dict[str, list[str]]:
    return scan_lockfiles(repo, ref)[0]


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
    """Nombre de un especificador (sin version ni subruta): `@scope/*wdk*` o `wdk-protocol-*`/`wdk-wallet-*` sin scope."""
    spec = spec.strip("'\"")
    unscoped = UNSCOPED_NAME_RE.match(spec)
    if unscoped:
        return unscoped.group(0)
    match = SCOPED_NAME_RE.match(spec)
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
    """Paquetes WDK nombrados en comandos de instalacion o imports: paquete -> primera pagina."""
    found: dict[str, str] = {}
    for page in _pages(docs):
        text = _without_removed_diff_lines(page.read_text(encoding="utf-8", errors="replace"))
        specs = [t for m in INSTALL_RE.finditer(text) for t in m.group(1).split()]
        specs += [m.group(1) for m in IMPORT_RE.finditer(text)]
        for name in filter(None, map(_wdk_name, specs)):
            found.setdefault(name, page.relative_to(docs).as_posix())
    return found


def _pages(docs: Path) -> list[Path]:
    root = docs / "content" / "docs"
    return sorted(p for pattern in ("*.mdx", "*.md") for p in root.rglob(pattern))


def docs_version_mentions(docs: Path) -> dict[str, DocVersion]:
    """Paquetes WDK nombrados con version entre backticks (`pkg@x.y.z`): la version mas alta de cada uno."""
    found: dict[str, DocVersion] = {}
    for page in _pages(docs):
        text = _without_removed_diff_lines(page.read_text(encoding="utf-8", errors="replace"))
        for match in MENTION_RE.finditer(text):
            package, version = _wdk_name(match.group(1)), match.group(2)
            current = found.get(package) if package else None
            if package and (current is None or version_key(version) > version_key(current.version)):
                found[package] = DocVersion(package, version, f"mention:{page.relative_to(docs).as_posix()}")
    return found


def docs_beta_callouts(docs: Path, known: set[str]) -> dict[str, DocVersion]:
    """Version `v<semver>` de un Callout de un index.mdx, para el paquete que infiere la carpeta si ya se conoce."""
    found: dict[str, DocVersion] = {}
    for mdx in sorted((docs / "content" / "docs").rglob("index.mdx")):
        text = mdx.read_text(encoding="utf-8", errors="replace")
        for block in CALLOUT_BLOCK_RE.finditer(text):
            match = BETA_VERSION_RE.search(block.group(1))
            if not match:
                continue
            package, version = _callout_package(match.group(1), mdx)
            current = found.get(package)
            if package in known and (current is None or version_key(version) > version_key(current.version)):
                found[package] = DocVersion(package, version, f"callout-beta:{mdx.relative_to(docs).as_posix()}")
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


def documented_versions(docs: Path, installs: dict[str, str] | None = None) -> dict[str, DocVersion]:
    """Precedencia: aviso `These pages reflect`, changelog, aviso beta, mencion `pkg@ver`."""
    changelog = _newest_per_package(changelog_entries(_read_changelog(docs)))
    beta = docs_beta_callouts(docs, set(changelog) | set(installs or {}))
    found = {**docs_version_mentions(docs), **beta, **changelog, **docs_callouts(docs)}
    return dict(sorted(found.items()))


def documented_with_installs(documented: dict[str, DocVersion], installs: dict[str, str]) -> dict[str, DocVersion]:
    """Suma los paquetes que solo aparecen en comandos de instalacion, con version vacia."""
    extra = {p: DocVersion(p, "", f"install:{path}") for p, path in installs.items() if p not in documented}
    return dict(sorted({**documented, **extra}.items()))


def _merge_github_ids(catalog: dict[str, DocVersion]) -> dict[str, DocVersion]:
    """Un paquete sin version, o solo con una mencion o aviso beta, toma la version del changelog del id `github:<org>/<repo>`."""
    by_repo = {p.rpartition("/")[2]: p for p in catalog if p.startswith("github:")}
    for package, doc in list(catalog.items()):
        github = by_repo.get(package.rpartition("/")[2])
        weak = not doc.version or doc.source.startswith(("mention:", "callout-beta:"))
        if not weak or not github or package.startswith("github:"):
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


def _repos_table(states: list[RepoState], unanalyzable: dict[str, str]) -> list[str]:
    lines = [
        "## Repos: mi versión vs desplegada",
        "",
        "| repo | ref analizada (commit, fecha) | release desplegada (+N commits) | HEAD local (atrás/adelante de origin) | sucio |",
        "|---|---|---|---|---|",
    ]
    for s in states:
        if s.release:
            released = f"{s.release} + {s.ahead_of_release} commits ({s.release_date})"
        else:
            released = f"sin release (referencia: {s.analyzed_ref})"
        local = f"{s.local_head[:7]} ({s.local_head_date})"
        if s.origin_head is None:
            local += f": sin origin/{s.branch}"
        else:
            local += f": atrás {s.behind_origin} / adelante {s.ahead_origin}"
        lines.append(f"| {s.name} | {s.analyzed_ref}: {s.head[:7]} ({s.head_date}) | {released} | {local} "
                     f"| {'sí' if s.dirty else 'no'} |")
    if unanalyzable:
        lines += [""] + [f"- {name}: no analizable: {reason}" for name, reason in sorted(unanalyzable.items())]
    return lines


def _local_gap(s: RepoState) -> list[str]:
    """Aviso cuando el checkout local no coincide con la ref analizada."""
    parts = [f"{n} commits {word}" for n, word in ((s.behind_origin, "detrás"), (s.ahead_origin, "adelante")) if n]
    if not parts:
        return []
    return [f"tu checkout local está {' y '.join(parts)} de {s.analyzed_ref}; "
            f"las versiones de esta tabla son las de {s.analyzed_ref}", ""]


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
                   lock_problems: dict[str, list[LockProblem]],
                   skipped: set[str]) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    breaking_lines: list[str] = []
    for s in states:
        lines += [f"## {s.name}", ""] + _local_gap(s)
        if s.name in skipped:
            lines += [f"Lockfiles no escaneados (`{DOCS_ONLY}` en `_meta/repos.txt`).", ""]
            continue
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
        "| paquete | documentada (fuente) | npm latest | estado | lo uso en |",
        "|---|---|---|---|---|",
    ]
    for package, doc in catalog.items():
        used = [f"{repo} {', '.join(locked[package])}" for repo, locked in locked_by_repo.items() if package in locked]
        latest = npm_latest.get(package) or "—"
        lines.append(f"| {package} | {_doc_cell(doc)} | {latest} | {_npm_state(doc, latest)} "
                     f"| {'; '.join(used) or 'no instalado'} |")
    return lines


def _npm_state(doc: DocVersion, latest: str) -> str:
    """Marca la version documentada que es mas nueva que todo lo publicado en npm."""
    if doc.version and NPM_VERSION_RE.match(latest) and version_key(latest) < version_key(doc.version):
        return "documentada no publicada en npm"
    return "—"


def render_versions_md(states: list[RepoState], locked_by_repo: dict[str, dict[str, list[str]]],
                       documented: dict[str, DocVersion], entries: list[ChangelogEntry],
                       npm_latest: dict[str, str], unmapped: list[str] | None = None,
                       lock_problems: dict[str, list[LockProblem]] | None = None,
                       npm_line: str = "npm consultado: no", skipped: set[str] | None = None,
                       unanalyzable: dict[str, str] | None = None) -> str:
    lines = [
        "# Versiones: mi versión vs desplegada vs documentada",
        "",
        "Archivo generado por `_meta/versions.py`; no se edita a mano. Los upstream de Tether son privados:",
        "no se puede ver una release posterior a la integrada en `origin/main` de cada repo.",
        "Las versiones salen de la ref analizada (`origin/main`), no del checkout local.",
        "",
        f"{npm_line}.",
        "",
    ]
    lines += _repos_table(states, unanalyzable or {}) + [""]
    sections, breaking_lines = _repo_sections(
        states, locked_by_repo, documented, entries, npm_latest, lock_problems or {}, skipped or set())
    lines += sections
    lines += ["## Cambios breaking entre mi versión y la documentada", ""]
    lines += (breaking_lines or ["Ninguno."]) + [""]
    lines += _catalog_table(_catalog(documented, entries), locked_by_repo, npm_latest) + [""]
    lines += ["## Entradas del changelog sin paquete reconocido", ""]
    lines += [f"- {item}" for item in unmapped or []] or ["Ninguna."]
    return "\n".join(lines) + "\n"


def parse_last_sync(text: str) -> dict[str, list[str]]:
    """Lineas no vacias de cada seccion `## <repo>` de un last-sync.md."""
    sections: dict[str, list[str]] = {}
    current: list[str] | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = sections.setdefault(line[3:].strip(), [])
        elif current is not None and line.strip():
            current.append(line)
    return sections


SYNC_KEYS = ("commit:", "date:", "analyzed_on:")


def _kept_sync_lines(previous: list[str]) -> dict[str, str] | None:
    """`commit`/`date`/`analyzed_on` de la seccion anterior, tal cual; None si falta alguna."""
    kept = {key: next((line for line in previous if line.startswith(key)), None) for key in SYNC_KEYS}
    return None if None in kept.values() else kept


def render_last_sync(states: list[RepoState], docs_site: dict, analyzed_on: str,
                     previous: dict[str, list[str]] | None = None, advance: set[str] | None = None,
                     keep: tuple[str, ...] = ()) -> str:
    """`advance` None avanza todas las secciones; si no, las demas conservan commit/date/analyzed_on.

    Una seccion no avanzada sin punto anterior se omite (no se inventa un punto de sincronizacion).
    `keep` son repos no analizables cuya seccion anterior se copia tal cual.
    """
    previous = previous or {}
    lines = [
        "# last-sync",
        "",
        "Punto de sincronización de cada fuente. Los upstream de Tether son privados: no se puede ver una",
        "release posterior a la integrada en `origin/main` de cada repo (`deployed_release`).",
    ]
    sections: dict[str, list[str]] = {}
    for s in states:
        fresh = {"commit:": f"commit: {s.head}", "date:": f"date: {s.head_date}",
                 "analyzed_on:": f"analyzed_on: {analyzed_on}"}
        sync = fresh if advance is None or s.name in advance else _kept_sync_lines(previous.get(s.name, []))
        if sync is None:
            continue
        sections[s.name] = _sync_section(s, docs_site, sync)
    sections.update({name: previous[name] for name in keep if name in previous})
    for name in sections:
        lines += ["", f"## {name}", *sections[name]]
    return "\n".join(lines) + "\n"


def _sync_section(s: RepoState, docs_site: dict, sync: dict[str, str]) -> list[str]:
    lines = [f"branch: {s.branch}", sync["commit:"], sync["date:"], f"analyzed_ref: {s.analyzed_ref}"]
    if s.release:
        lines += [f"deployed_release: {s.release}", f"release_commit: {s.release_commit}",
                  f"release_date: {s.release_date}", f"ahead_of_release: {s.ahead_of_release}"]
    else:
        lines.append(f"deployed_release: none (origin/{s.branch})")
    lines += [f"origin_main: {s.origin_head or 'none'}", f"behind_origin: {s.behind_origin if s.behind_origin is not None else 'none'}"]
    if s.name == "wdk-docs":
        lines += [f"{k}: {docs_site[k]}" for k in ("site_changelog_top", "repo_changelog_top", "site_matches_repo") if k in docs_site]
    lines.append(sync["analyzed_on:"])
    return lines


# ---------------------------------------------------------------- cambios

PageChange = tuple[str, str, str | None]


def _range_changes(entries: list[ChangelogEntry], package: str, source: str, low: str, high: str) -> list[ChangelogEntry]:
    """Entradas `low < version <= high`, tambien bajo el id `github:` del que salio la version (`... via github:x/y`)."""
    ids = [package] + ([source.rpartition(" via ")[2]] if " via " in source else [])
    return [e for pid in ids for e in changes_between(entries, pid, low, high)]


def _entry_line(e: ChangelogEntry) -> str:
    breaking = " [Breaking]" if e.breaking else ""
    return f"- {e.date} · {e.version}{breaking}: {e.summary.removeprefix('[Breaking]').strip()}"


def _cambios_header(previous: dict, current: dict) -> list[str]:
    before, now = previous.get("wdk_docs") or {}, current["wdk_docs"]
    old = before.get("commit", "")
    lines = [f"- Foto indexada: {previous.get('indexed_on', '—')}, wdk-docs `{old[:7]}` ({before.get('date', '—')})",
             f"- Actual: wdk-docs {now['ref']} `{now['commit'][:7]}` ({now['date']})"]
    same = old == now["commit"]
    return lines + [f"- Commit de la doc: {NO_CHANGES}" if same else f"- La doc avanzó: `{old[:7]}..{now['commit'][:7]}`"]


def _cambios_versions(previous: dict, current: dict, entries: list[ChangelogEntry]) -> list[str]:
    before, now = previous.get("packages") or {}, current["packages"]
    changed = [p for p in sorted(set(before) & set(now)) if before[p].get("documented", "") != now[p]["documented"]]
    if not changed:
        return []
    lines = ["| paquete | indexada | actual | npm indexado → npm actual | cambios del changelog en el rango |",
             "|---|---|---|---|---|"]
    details: list[str] = []
    for package in changed:
        old, new = before[package].get("documented", ""), now[package]["documented"]
        changes = _range_changes(entries, package, now[package]["source"], old, new)
        npm = f"{before[package].get('npm') or '—'} → {now[package]['npm'] or '—'}"
        lines.append(f"| {package} | {old or '—'} | {new or '—'} | {npm} | {_range_cell(changes)} |")
        if changes:
            details += ["", f"`{package}`:"] + [_entry_line(e) for e in changes]
    return lines + details


def _links(notes: list[str]) -> str:
    return ", ".join(f"[[{n}]]" for n in notes)


def _cambios_pages(pages: list[PageChange] | None, cited: dict[str, list[str]], docs_name: str,
                   old: str, new: str) -> list[str]:
    if pages is None:
        return [f"no se pudo comparar: el commit indexado `{old[:7]}` no está en {docs_name} (¿falta un fetch?)"]
    if not pages:
        return []
    reviewed: list[str] = []
    uncited: list[str] = []
    for status, path, new_path in pages:
        word = PAGE_STATUS.get(status, status)
        old_notes = cited.get(f"{docs_name}/{path}", [])
        if new_path is None:
            label, notes, stale = f"`{path}` ({word})", old_notes, []
        else:
            label, notes, stale = f"`{path}` → `{new_path}` ({word})", cited.get(f"{docs_name}/{new_path}", []), old_notes
        parts = [_links(notes)] if notes else []
        if stale:
            parts.append(f"citan la ruta vieja, corregir su `source:`: {_links(stale)}")
        if parts:
            reviewed.append(f"- {label}: {'; '.join(parts)}")
        else:
            uncited.append(f"- {label}")
    return [f"`git diff --name-status {old[:7]}..{new[:7]} -- content/docs`: {len(pages)} páginas.", "",
            "Notas a revisar:", *(reviewed or ["- ninguna"]), "",
            "Páginas sin nota que las cite:", *(uncited or ["- ninguna"])]


def _cambios_catalog(previous: dict, current: dict) -> list[str]:
    before, now = previous.get("packages") or {}, current["packages"]
    new, gone = sorted(set(now) - set(before)), sorted(set(before) - set(now))
    if not new and not gone:
        return []
    added = [f"- `{p}`: {now[p]['documented'] or '—'} ({now[p]['source']})" for p in new]
    removed = [f"- `{p}`: {before[p].get('documented') or '—'} ({before[p].get('source', '—')})" for p in gone]
    return ["Nuevos:", *(added or ["- ninguno"]), "", "Desaparecidos:", *(removed or ["- ninguno"])]


def _cambios_npm(previous: dict, current: dict) -> list[str]:
    before, now = previous.get("packages") or {}, current["packages"]
    lines = []
    for package in sorted(set(before) & set(now)):
        old, new = before[package].get("npm", ""), now[package]["npm"]
        known = old and new and NPM_ERROR not in (old, new)
        if known and old != new and before[package].get("documented", "") == now[package]["documented"]:
            lines.append(f"- `{package}`: npm {old} → {new}; documentada sigue en {now[package]['documented'] or '—'}")
    return ["npm cambió y la versión documentada no: la doc va atrás de npm.", "", *lines] if lines else []


def _cambios_org(before: dict, now: dict) -> list[str]:
    if not before:
        return ["la foto no tiene repos de tetherto: correr `--checkpoint` con `--org` para guardarlos"] if now else []
    both = sorted(set(now) & set(before))
    groups = {
        "Nuevos": [f"- `{r}`" for r in sorted(set(now) - set(before))],
        "Con push más reciente": [f"- `{r}`: {before[r].get('pushed_at', '')} → {now[r]['pushed_at']}"
                                  for r in both if now[r]["pushed_at"] > before[r].get("pushed_at", "")],
        "Archivados": [f"- `{r}`" for r in both if now[r]["archived"] and not before[r].get("archived")],
        "Desaparecidos": [f"- `{r}`" for r in sorted(set(before) - set(now))],
    }
    if not any(groups.values()):
        return []
    lines: list[str] = []
    for title, items in groups.items():
        lines += [f"{title}:", *(items or ["- ninguno"]), ""]
    return lines[:-1]


CHECKLIST = [
    "1. Revisar las notas de la sección 2 contra las páginas que cambiaron.",
    "2. Actualizar `package:` o las notas que tocan las secciones 1, 3 y 5.",
    "3. Correr `python3 _meta/versions.py --npm --org --checkpoint <repos sincronizados>`; con `wdk-docs` "
    "entre ellos se guarda la foto nueva.",
    "4. Correr `python3 _meta/check.py`, que tiene que terminar limpio.",
]


def render_cambios(previous: dict, current: dict, entries: list[ChangelogEntry], pages: list[PageChange] | None,
                   cited: dict[str, list[str]], docs_name: str = "wdk-docs",
                   org_missing: str = "no consultado (correr con --org)") -> str:
    """Informe de lo que cambio desde la foto `previous`. `current["org_repos"]` None: la org no se consulto."""
    old, new = (previous.get("wdk_docs") or {}).get("commit", ""), current["wdk_docs"]["commit"]
    bodies = {
        "1. Paquetes con versión documentada distinta": _cambios_versions(previous, current, entries),
        "2. Páginas de la doc que cambiaron": _cambios_pages(pages, cited, docs_name, old, new),
        "3. Paquetes nuevos / desaparecidos del catálogo": _cambios_catalog(previous, current),
        "4. npm": _cambios_npm(previous, current),
    }
    org = current["org_repos"]
    bodies["5. Repos de tetherto"] = _cambios_org(previous.get("org_repos") or {}, org) if org is not None else []
    changed = old != new or any(bodies.values())
    lines = [
        "# Cambios desde la última foto indexada",
        "",
        "Archivo generado por `_meta/versions.py --cambios`; no se edita a mano. Compara el estado actual",
        "contra la foto `_meta/indexado.json`, que guarda `--checkpoint` cuando incluye `wdk-docs`.",
        "",
        "## 0. Encabezado",
        "",
        *_cambios_header(previous, current),
    ]
    for title, body in bodies.items():
        if title.startswith("5.") and org is None:
            body = [org_missing]
        lines += ["", f"## {title}", "", *(body or [NO_CHANGES])]
    lines += ["", "## 6. Qué hacer", "", *(CHECKLIST if changed else [NO_CHANGES])]
    return "\n".join(lines) + "\n"


def docs_page_changes(repo: Path, old: str, new: str) -> list[PageChange] | None:
    """(estado, ruta, ruta nueva si es un renombre) de `content/docs` entre dos commits; None si git no puede comparar."""
    if not SHA_RE.match(old):
        return None
    try:
        raw = subprocess.run(["git", "diff", "--name-status", "-z", "-M", f"{old}..{new}", "--", "content/docs"],
                             cwd=repo, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None
    fields = iter(raw.split("\0"))
    changes: list[PageChange] = []
    for code in fields:
        if not code:
            break
        path = next(fields)
        changes.append((code[0], path, next(fields) if code[0] in "RC" else None))
    return changes


def _frontmatter_sources(text: str) -> list[str]:
    end = text.find("\n---", 4) if text.startswith("---\n") else -1
    sources: list[str] = []
    inside = False
    for line in text[4:end].splitlines() if end != -1 else []:
        if line.startswith("  - ") and inside:
            sources.append(line[4:].strip().strip("'\""))
        elif line.strip():
            inside = line.startswith("source:")
    return sources


def note_sources(vault: Path) -> dict[str, list[str]]:
    """Ruta de `source:` -> notas que la citan (fuera de `_meta` y de las carpetas ocultas)."""
    cited: dict[str, list[str]] = {}
    for path in sorted(vault.rglob("*.md")):
        parts = path.relative_to(vault).parts
        if "_meta" in parts or any(part.startswith(".") for part in parts):
            continue
        for source in _frontmatter_sources(path.read_text(encoding="utf-8", errors="replace")):
            cited.setdefault(source, []).append(path.stem)
    return cited


# --------------------------------------------------------------------- IO

def _repo_list(vault: Path) -> list[tuple[str, set[str]]] | None:
    """Entradas de `_meta/repos.txt`: (directorio, marcas). None si el archivo no existe."""
    path = vault / "_meta" / "repos.txt"
    if not path.is_file():
        return None
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        words = line.partition("#")[0].split()
        if words:
            entries.append((words[0], set(words[1:])))
    return entries


def _discover_repos(workspace: Path, vault: Path) -> tuple[list[Path], set[str]]:
    """Repos a analizar y los marcados `docs-only`; sin `repos.txt`, todos los repos git del workspace."""
    listed = _repo_list(vault)
    if listed is not None:
        return [workspace / name for name, _ in listed], {name for name, flags in listed if DOCS_ONLY in flags}
    print("warning: falta _meta/repos.txt; se analizan todos los repos git del workspace", file=sys.stderr)
    found = [d for d in sorted(workspace.iterdir()) if d.is_dir() and d.name != vault.name and (d / ".git").exists()]
    return found, set()


def _analysis_branch(repo: Path) -> str:
    if _git_optional(repo, "rev-parse", "--verify", "-q", "origin/main") or \
            _git_optional(repo, "rev-parse", "--verify", "-q", "main"):
        return "main"
    return _git_optional(repo, "symbolic-ref", "--short", "HEAD") or "main"


def _analyze(repos: list[Path]) -> tuple[list[RepoState], dict[str, str]]:
    """Estado de cada repo; los que git no puede analizar quedan en el segundo dict con su motivo."""
    states: list[RepoState] = []
    failed: dict[str, str] = {}
    for repo in repos:
        if not (repo / ".git").exists():
            failed[repo.name] = "no es un repo git del workspace"
            continue
        try:
            states.append(repo_state(repo, _analysis_branch(repo)))
        except subprocess.CalledProcessError as error:
            detail = (error.stderr or "").strip().splitlines()
            failed[repo.name] = detail[0] if detail else f"git terminó con código {error.returncode}"
    return states, failed


def _export_docs(docs: Path, ref: str, dest: Path) -> Path:
    """`content/docs` tal como esta en `ref` (git archive), sin leer el arbol de trabajo."""
    raw = subprocess.run(["git", "archive", "--format=tar", ref, "content/docs"],
                         cwd=docs, capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        archive.extractall(dest, filter="data")
    return dest


def _npm_latest_one(package: str) -> tuple[str, str]:
    """`latest` de npm, o `no publicado (404)` / `error` para no confundirlos con una version."""
    try:
        result = subprocess.run(["npm", "view", package, "dist-tags.latest"],
                                capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return package, NPM_ERROR
    if result.returncode != 0:
        return package, NPM_404 if "E404" in (result.stderr or "") else NPM_ERROR
    return package, result.stdout.strip()


def _fetch_npm_latest(packages: list[str]) -> dict[str, str]:
    with ThreadPoolExecutor(max_workers=8) as pool:
        return dict(pool.map(_npm_latest_one, packages))


def _site_changelog_top() -> str:
    try:
        request = urllib.request.Request(SITE_CHANGELOG_URL, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=20) as response:
            return changelog_top_date(response.read().decode("utf-8", errors="replace")) or UNKNOWN
    except (OSError, ValueError, http.client.HTTPException):
        return UNKNOWN


def _fetch_org_repos() -> dict[str, dict] | None:
    """Repos publicos de tetherto cuyo nombre es del WDK: nombre -> pushed_at y archived. None ante un error de red."""
    found: dict[str, dict] = {}
    try:
        for page in itertools.count(1):
            request = urllib.request.Request(ORG_REPOS_URL.format(page=page), headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=20) as response:
                items = json.loads(response.read().decode("utf-8"))
            if not isinstance(items, list):
                raise ValueError("la respuesta no es una lista")
            if not items:
                break
            for item in items:
                name = item.get("name") if isinstance(item, dict) else None
                if isinstance(name, str) and ORG_REPO_RE.search(name):
                    found[name] = {"pushed_at": (item.get("pushed_at") or "")[:10], "archived": bool(item.get("archived"))}
    except (OSError, ValueError, http.client.HTTPException) as error:
        print(f"warning: no se pudo consultar la org tetherto en GitHub: {error}", file=sys.stderr)
        return None
    return dict(sorted(found.items()))


def _docs_site(repo_top: str) -> dict:
    site_top = _site_changelog_top()
    if UNKNOWN in (site_top, repo_top or UNKNOWN):
        matches = UNKNOWN
    else:
        matches = "yes" if site_top == repo_top else "no"
    return {"site_changelog_top": site_top, "repo_changelog_top": repo_top or UNKNOWN, "site_matches_repo": matches}


def _previous_npm(meta: Path) -> dict | None:
    """Bloque `npm` del versions.json actual, si tiene valores."""
    try:
        npm = json.loads((meta / "versions.json").read_text(encoding="utf-8")).get("npm")
    except (OSError, json.JSONDecodeError, AttributeError):
        return None
    ok = isinstance(npm, dict) and isinstance(npm.get("latest"), dict) and isinstance(npm.get("queried_on"), str)
    return npm if ok else None


def _npm_values(query: bool, packages: list[str], meta: Path, today: str) -> tuple[dict, str]:
    """Valores npm y la linea de encabezado: consultados hoy, los de la ultima consulta, o ninguno."""
    if query:
        return {"queried_on": today, "latest": _fetch_npm_latest(packages)}, f"npm consultado: sí ({today})"
    previous = _previous_npm(meta)
    if previous:
        return previous, f"npm consultado: no; valores npm del {previous['queried_on']} (última consulta)"
    return {"queried_on": None, "latest": {}}, "npm consultado: no"


def _write_checkpoint(meta: Path, states: list[RepoState], failed: dict[str, str], changelog: str,
                      names: list[str], today: str) -> None:
    path = meta / "last-sync.md"
    previous = parse_last_sync(path.read_text(encoding="utf-8")) if path.is_file() else {}
    advance = set(names) if names else None
    for s in states:
        if advance is not None and s.name not in advance and s.name not in previous:
            print(f"warning: {s.name} no tiene sección en last-sync.md y no se nombró en --checkpoint: "
                  "queda sin punto de sincronización", file=sys.stderr)
    site = _docs_site(changelog_top_date(changelog))
    text = render_last_sync(states, site, today, previous, advance, tuple(failed))
    path.write_text(text, encoding="utf-8")


def snapshot_payload(today: str, docs_state: RepoState, catalog: dict[str, DocVersion], npm_latest: dict[str, str],
                     org_repos: dict) -> dict:
    """Foto de lo indexado: commit de la doc, cada fila del catalogo con su npm, y los repos de tetherto."""
    return {
        "indexed_on": today,
        "wdk_docs": {"ref": docs_state.analyzed_ref, "commit": docs_state.head, "date": docs_state.head_date},
        "packages": {p: {"documented": d.version, "source": d.source, "npm": npm_latest.get(p, "")}
                     for p, d in catalog.items()},
        "org_repos": org_repos,
    }


def _load_snapshot(meta: Path) -> dict | None:
    try:
        data = json.loads((meta / SNAPSHOT).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str], vault: Path = VAULT) -> int:
    parser = argparse.ArgumentParser(description="Genera _meta/versions.md y versions.json")
    parser.add_argument("--npm", action="store_true", help="consulta dist-tags.latest en npm")
    parser.add_argument("--checkpoint", nargs="*", metavar="REPO",
                        help="escribe _meta/last-sync.md; sin nombres avanza todos los repos, con nombres solo esos; "
                             "si incluye wdk-docs, guarda la foto _meta/indexado.json")
    parser.add_argument("--org", action="store_true", help="consulta los repos de la org tetherto en GitHub")
    parser.add_argument("--cambios", action="store_true",
                        help="compara contra _meta/indexado.json y escribe _meta/cambios.md")
    args = parser.parse_args(argv)
    if args.cambios and _load_snapshot(vault / "_meta") is None:
        print(f"error: {SNAPSHOT_MISSING}", file=sys.stderr)
        return 2

    workspace = vault.parent
    docs = workspace / "wdk-docs"
    if not docs.is_dir():
        print(f"error: falta {docs}; clona https://github.com/tetherto/wdk-docs.git en el workspace", file=sys.stderr)
        return 2

    repos, docs_only = _discover_repos(workspace, vault)
    unknown = sorted(set(args.checkpoint or []) - {r.name for r in repos})
    if unknown:
        print(f"error: --checkpoint con repos desconocidos: {', '.join(unknown)}", file=sys.stderr)
        return 2
    states, failed = _analyze(repos)
    for name, reason in failed.items():
        print(f"warning: {name}: no analizable: {reason}", file=sys.stderr)
    docs_state = next((s for s in states if s.name == docs.name), None)
    try:
        docs_state = docs_state or repo_state(docs, _analysis_branch(docs))
    except subprocess.CalledProcessError:
        print(f"error: {docs} no es analizable con git", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory() as tmp:
        return _generate(args, vault, _export_docs(docs, docs_state.head, Path(tmp)), states, failed, docs_only,
                         docs_state)


def _generate(args: argparse.Namespace, vault: Path, docs: Path, states: list[RepoState],
              failed: dict[str, str], docs_only: set[str], docs_state: RepoState) -> int:
    workspace = vault.parent
    scans = {s.name: scan_lockfiles(workspace / s.name, s.head) for s in states if s.name not in docs_only}
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
    installs = docs_install_packages(docs)
    documented = documented_with_installs(documented_versions(docs, installs), installs)
    catalog = _catalog(documented, entries)
    today = date.today().isoformat()
    meta = vault / "_meta"
    npm, npm_line = _npm_values(args.npm, [p for p in catalog if not p.startswith("github:")], meta, today)

    packages = set(catalog) | set(documented) | {e.package for e in entries}
    for locked in locked_by_repo.values():
        packages.update(locked)
    (meta / "versions.md").write_text(
        render_versions_md(states, locked_by_repo, documented, entries, npm["latest"], unmapped, lock_problems,
                           npm_line, docs_only, failed),
        encoding="utf-8")
    payload = {
        "generated": today,
        "npm": npm,
        "repos": {s.name: {**asdict(s), "locked": locked_by_repo.get(s.name, {}),
                         "lockfile_problems": [f"{f} ({r})" for f, r in lock_problems.get(s.name, [])]}
                  for s in states},
        "packages": sorted(packages),
    }
    _write_json(meta / "versions.json", payload)
    saves_snapshot = args.checkpoint is not None and (not args.checkpoint or docs_state.name in args.checkpoint)
    org = _fetch_org_repos() if args.org and (args.cambios or saves_snapshot) else None
    previous = _load_snapshot(meta) or {}
    snapshot = snapshot_payload(today, docs_state, catalog, npm["latest"],
                                previous.get("org_repos", {}) if org is None else org)
    if args.cambios:
        old = (previous.get("wdk_docs") or {}).get("commit", "")
        pages = docs_page_changes(workspace / docs_state.name, old, docs_state.head)
        missing = "no se pudo consultar (error de red; ver stderr)" if args.org else "no consultado (correr con --org)"
        report = render_cambios(previous, {**snapshot, "org_repos": org}, entries, pages, note_sources(vault),
                                docs_state.name, missing)
        (meta / "cambios.md").write_text(report, encoding="utf-8")
    if args.checkpoint is not None:
        _write_checkpoint(meta, states, failed, changelog, args.checkpoint, today)
    if saves_snapshot:
        if org is None and args.org:
            print("warning: org_repos: se conservan los de la foto anterior", file=sys.stderr)
        _write_json(meta / SNAPSHOT, snapshot)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
