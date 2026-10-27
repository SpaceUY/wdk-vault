---
type: system
status: shipped
source:
  - wdk-indexer-processor-wrk/README.md
  - wdk-indexer-processor-wrk/workers/indexer.processor.wrk.js
  - wdk-indexer-processor-wrk/config/common.json.example
---
# wdk-indexer-processor-wrk

Enrutador de transacciones: lee el stream de Redis que publica el indexer de una cadena y token, resuelve a qué shard pertenece cada dirección y reenvía la transferencia al stream de ese shard. Se arranca con `--chain` y `--token`, y necesita el directorio de lookups (`autobase` con la clave de bootstrap, o `mongodb`). El paquete `@tetherto/wdk-indexer-processor-wrk` no figura en la documentación pública; su release desplegada está en `_meta/versions.md`.

## Structural
- depends on → [[wdk-ork-wrk]] because solo lee el directorio que el ork escribe (dirección → billetera y billetera → shard, vía `getWalletIdByAddress` y `getLookup`)
