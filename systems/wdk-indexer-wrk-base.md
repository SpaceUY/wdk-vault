---
type: system
status: shipped
source:
  - wdk-indexer-wrk-base/CLAUDE.md
  - wdk-indexer-wrk-base/README.md
  - wdk-indexer-wrk-base/workers/proc.indexer.wrk.js
  - wdk-indexer-wrk-base/workers/api.indexer.wrk.js
  - wdk-indexer-wrk-base/workers/lib/chain.base.client.js
---
# wdk-indexer-wrk-base

Biblioteca base de los indexers por cadena, no un servicio autónomo: define el worker `proc` (sincroniza bloques y publica en Redis), el worker `api` (réplica de solo lectura que responde consultas por RPC) y el contrato `ChainBaseClient` que cada cadena implementa. Los repos de cada cadena la declaran como dependencia git y le agregan su cliente. El paquete `@tetherto/wdk-indexer-wrk-base` no figura en la documentación pública; su release desplegada está en `_meta/versions.md`.
