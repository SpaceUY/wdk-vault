---
type: system
status: shipped
source:
  - wdk-indexer-wrk-evm/README.md
  - wdk-indexer-wrk-evm/package.json
  - wdk-indexer-wrk-evm/workers/lib/chain.evm.client.js
  - wdk-indexer-wrk-evm/config/eth.json.example
---
# wdk-indexer-wrk-evm

Indexer de cadenas EVM con dos familias de workers: `wrk-evm-indexer-*` para la moneda nativa y `wrk-erc20-indexer-*` para cada token ERC-20, cada una con su `proc` y sus `api`. El cliente carga `@tetherto/wdk-wallet-evm-erc-4337` solo para consultar el recibo de una transacción gasless, por eso su configuración incluye datos de bundler y paymaster. Su release desplegada está en `_meta/versions.md`.

## Structural
- depends on → [[wdk-indexer-wrk-base]] because extiende sus workers `proc` y `api` con clientes EVM y ERC-20
- depends on → [[wdk-wallet-evm-erc-4337]] because `getGasLessTransactionReceipt` usa su cuenta de solo lectura; en el lockfile arrastra también a `wdk-wallet-evm`
- can replace → [[Indexadores y nodos de terceros]] because puede asumir las consultas de saldo y transferencias ERC-20 por dirección, a condición de que el proyecto opere los workers `proc` y `api`, un motor de base de datos (hyperdb o MongoDB), los peers hyperswarm y al menos un proveedor RPC por cadena, más Redis si publica el stream de transferencias
