---
type: decision
status: shipped
source:
  - wdk-vault/_meta/versions.py
  - wdk-vault/_meta/last-sync.md
---
# Usar la release integrada en SpaceUY como versión desplegada

Decisión del 2026-10-26: la «versión desplegada» de un repo es la última release de Tether integrada en `origin/main` de SpaceUY, detectada por el asunto del commit (`Release: vX.Y.Z` o merge de `release/vX.Y.Z`). Los upstream de Tether son privados, así que el vault no puede saber si existe una release más nueva y lo declara. Un repo adelantado se informa como «release + N commits» (por ejemplo `wdk-indexer-wrk-base` en v0.3.1 + 49 commits), y sin releases la referencia es `origin/main`.

## Structural
- establishes → [[Verificar la versión antes de afirmar una capacidad]]
