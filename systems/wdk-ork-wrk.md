---
type: system
status: shipped
source:
  - wdk-ork-wrk/CLAUDE.md
  - wdk-ork-wrk/README.md
  - wdk-ork-wrk/workers/api.ork.wrk.js
  - wdk-ork-wrk/workers/lib/data.shard.util.js
---
# wdk-ork-wrk

Worker orquestador (`WrkOrkApi`): es el directorio que sabe en qué shard vive cada usuario, billetera y canal, y reenvía las llamadas al data shard correspondiente sin guardar datos de billetera. El directorio se guarda en `autobase` o `mongodb`, según `lookupEngine`, y corre como un maestro más nodos secundarios. El paquete `@tetherto/wdk-ork-wrk` no figura en la documentación pública; su release desplegada está en `_meta/versions.md`.

## Structural
- depends on → [[wdk-data-shard-wrk]] because proxea las acciones de billetera al shard que resuelve desde su directorio
