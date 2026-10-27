---
type: concept
status: shipped
source:
  - wdk-indexer-wrk-base/CLAUDE.md
  - wdk-indexer-wrk-base/workers/proc.indexer.wrk.js
  - wdk-indexer-processor-wrk/workers/indexer.processor.wrk.js
  - wdk-data-shard-wrk/CLAUDE.md
  - wdk-qualification-exercise/infra/wdk-stack/README.md
---
# Stream de transferencias agrupadas en Redis

Cuando el motor de eventos es Redis, el `proc` de cada indexer publica las transferencias de una transacción en el stream `@wdk/grouped-transactions:{chain}:{token}`; el processor las lee con un consumer group, resuelve el shard de cada dirección y las reenvía al stream `shard-{shardGroup}`, que consume el `proc` del data shard. Tras procesar cada mensaje el processor hace `XDEL`, así que un tercer consumidor del mismo stream, como el backend del caso SpaceUY, tiene que bloquear en `XREADGROUP` de forma continua para no perder eventos.

## Structural
- requires → [[wdk-indexer-wrk-base]] because su `proc` es quien escribe el stream de entrada
- requires → [[wdk-indexer-processor-wrk]] because es el enrutador que lo lleva al stream de cada shard
