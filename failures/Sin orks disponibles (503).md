---
type: failure
status: shipped
source:
  - wdk-app-node/CLAUDE.md
  - wdk-app-node/workers/base.http.server.wdk.js
  - wdk-app-node/workers/lib/services/ork.js
  - wdk-app-node/workers/lib/server.js
  - wdk-app-node/workers/lib/utils/errorsCodes.js
  - wdk-app-node/workers/lib/utils/round.robin.js
  - wdk-qualification-exercise/infra/wdk-stack/README.md
---
# Sin orks disponibles (503)

Cuando `app-node` no tiene ningún ork en su lista, las rutas que consultan datos de billetera responden 503 con `ERR_NO_ORKS_AVAILABLE`, y `/ready` devuelve `not_ready` mientras `/health` informa `degraded`. El worker no se cae: arranca igual y sigue sirviendo lo que no depende de un ork. Las rutas sin usuario autenticado pueden fallar con `ERR_EMPTY` (`round.robin.js:11`), que `errorsCodes.js:42` también mapea a 503. Se recupera solo cuando un refresco de la lista (cada 120 s) encuentra al menos un ork anunciado. Para diagnosticar, en orden: verificar que un ork está corriendo y anunciándose en el topic, esperar un refresco (120 s; el primer descubrimiento sobre la DHT puede tardar entre 10 y 60 s), consultar `/ready` y revisar que la capability coincida.
