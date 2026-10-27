---
type: system
status: shipped
source:
  - wdk-app-node/CLAUDE.md
  - wdk-app-node/README.md
  - wdk-app-node/workers/base.http.server.wdk.js
  - wdk-app-node/workers/lib/services/ork.js
  - wdk-app-node/workers/lib/server.js
---
# wdk-app-node

Gateway HTTP (Fastify) del backend de billeteras del WDK: autentica con JWT, valida la entrada y reenvía cada operación a un ork por hRPC; no guarda estado de billeteras. Para balances usa Redis como dependencia obligatoria. El paquete `@tetherto/wdk-app-node` no figura en la documentación pública; su release desplegada está en `_meta/versions.md`.

## Structural
- depends on → [[wdk-ork-wrk]] because todas las rutas con datos de billetera terminan en una llamada hRPC al ork
- depends on → [[Descubrimiento de orks por hyperswarm]] because no tiene los orks en su configuración: los busca por topic
