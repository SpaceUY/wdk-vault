---
type: concept
status: shipped
source:
  - wdk-ork-wrk/CLAUDE.md
  - wdk-ork-wrk/workers/lib/data.shard.util.js
  - wdk-data-shard-wrk/CLAUDE.md
---
# Data shard por usuario

El ork mantiene un mapa de usuario a shard, además de mapas aparte para billeteras y canales, y reenvía las llamadas de un usuario al shard que ese mapa le asignó. La primera vez que resuelve a un usuario le asigna el siguiente shard por round-robin y recién persiste la asignación después de resolver la clave RPC de ese shard, para no apuntar a uno inalcanzable. Desde entonces el ork devuelve siempre el shard guardado.

## Structural
- requires → [[wdk-ork-wrk]] because el mapa usuario → shard vive en su directorio de lookups
- depends on → [[wdk-data-shard-wrk]] because es el código que cada shard ejecuta para guardar y servir esos datos
