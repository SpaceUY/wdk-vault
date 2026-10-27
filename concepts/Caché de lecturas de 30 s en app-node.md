---
type: concept
status: shipped
source:
  - wdk-app-node/CLAUDE.md
  - wdk-app-node/README.md
  - wdk-app-node/workers/lib/utils/cached.route.js
  - wdk-app-node/workers/lib/server.js
---
# Caché de lecturas de 30 s en app-node

Las rutas de balance de `app-node` leen primero de Redis con una clave `cache:<ruta>:<id>` y un TTL de 30 s; solo si no hay entrada consultan al ork y guardan el resultado. El parámetro `cache=false` fuerza una lectura fresca y además omite la escritura. Todas las instancias deben compartir el mismo Redis, que es una dependencia obligatoria.

## Structural
- is part of → [[wdk-app-node]] because lo implementa `cachedRoute` sobre el Redis de ese worker
- causes → [[Balance desactualizado por caché]] because mientras la entrada no venza, la respuesta repite el saldo anterior sin consultar al ork
