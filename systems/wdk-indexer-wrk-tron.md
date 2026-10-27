---
type: system
status: shipped
source:
  - wdk-indexer-wrk-tron/README.md
  - wdk-indexer-wrk-tron/package.json
  - wdk-indexer-wrk-tron/workers/lib/chain.tron.client.js
  - wdk-indexer-wrk-tron/config/tron.json.example
---
# wdk-indexer-wrk-tron

Indexer de TRON con workers `wrk-tron-indexer-*` para la moneda nativa y `wrk-trc20-indexer-*` para tokens TRC-20. Su cliente importa `@tetherto/wdk-wallet-tron-gasfree` al construirse y arma una cuenta de solo lectura con el bloque `gasFreeConfig`, que rechaza si está presente pero incompleto. Su release desplegada está en `_meta/versions.md`.

## Structural
- depends on → [[wdk-indexer-wrk-base]] because extiende sus workers `proc` y `api` con clientes TRON y TRC-20
- depends on → [[wdk-wallet-tron-gasfree]] because el constructor del cliente lo importa y lo instancia con `gasFreeConfig`; en el lockfile arrastra también a `wdk-wallet-tron`
- can replace → [[Indexadores y nodos de terceros]] because puede asumir las consultas de saldo y transferencias TRC-20 por dirección, a condición de que el proyecto opere los workers `proc` y `api`, un motor de base de datos, los peers hyperswarm y un proveedor RPC de TRON (los ejemplos de config usan TronGrid), más el servicio GasFree si necesita recibos
