---
type: failure
status: shipped
source:
  - wdk-app-node/CLAUDE.md
  - wdk-app-node/workers/base.http.server.wdk.js
  - wdk-app-node/workers/lib/services/ork.js
  - wdk-app-node/workers/lib/server.js
  - wdk-app-node/workers/lib/utils/errorsCodes.js
---
# Sin orks disponibles (503)

Cuando `app-node` no tiene ningún ork en su lista, las rutas que consultan datos de billetera responden 503 con `ERR_NO_ORKS_AVAILABLE`, y `/ready` devuelve `not_ready` mientras `/health` informa `degraded`. El worker no se cae: arranca igual y sigue sirviendo lo que no depende de un ork. Se recupera solo cuando un refresco de la lista (cada 120 s) encuentra al menos un ork anunciado.
