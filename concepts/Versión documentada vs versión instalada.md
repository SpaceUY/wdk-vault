---
type: concept
status: shipped
source:
  - wdk-docs/content/docs/overview/changelog.mdx
  - wdk-vault/_meta/versions.py
---
# Versión documentada vs versión instalada

La documentación de cada módulo describe una versión concreta del paquete, y esa versión puede ser distinta de la que un repo tiene instalada y de la `latest` de npm. Por ejemplo, al 2026-10-26 la doc de `@tetherto/wdk-wallet-evm` refleja `1.0.0-beta.20`, `wdk-indexer-wrk-evm` instala `1.0.0-beta.11` y npm publica `1.0.0-beta.24`. Leer una página sin ubicar estas tres versiones lleva a dar por disponible lo que el repo no tiene.

## Structural
- causes → [[Usar una API documentada que mi versión no tiene]]
