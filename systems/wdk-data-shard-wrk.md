---
type: system
status: shipped
source:
  - wdk-data-shard-wrk/CLAUDE.md
  - wdk-data-shard-wrk/README.md
  - wdk-data-shard-wrk/workers/api.shard.data.wrk.js
  - wdk-data-shard-wrk/workers/proc.shard.data.wrk.js
  - wdk-data-shard-wrk/workers/lib/blockchain.svc.js
---
# wdk-data-shard-wrk

Capa de persistencia y lectura de un shard: un worker `proc` escribe billeteras, balances, transferencias y secretos de usuario, y varios workers `api` sirven lecturas desde réplicas y reenvían las escrituras al `proc`. Para saldos y transferencias consulta a los indexers por el topic `{chain}:{ccy}` mediante `BlockchainService`. El paquete `@tetherto/wdk-data-shard-wrk` no figura en la documentación pública; su release desplegada está en `_meta/versions.md`.

## Structural
- depends on → [[wdk-indexer-wrk-base]] because consume el contrato RPC de los indexers (`getBalance`, `queryTransactions`, `getBalanceMulti`) que ese repo base define y anuncia
