---
type: system
status: shipped
source:
  - wdk-indexer-wrk-ton/README.md
  - wdk-indexer-wrk-ton/package.json
  - wdk-indexer-wrk-ton/workers/lib/chain.ton.client.js
  - wdk-indexer-wrk-ton/config/ton.json.example
---
# wdk-indexer-wrk-ton

Indexer de TON con workers `wrk-ton-indexer-*` para la moneda nativa y `wrk-jet-indexer-*` para Jettons. Hace failover desde el RPC principal hacia RPC secundarios (con proveedores `toncenter`, `ankr` y `quicknode` en sus configs de ejemplo) y usa la cuenta de solo lectura de `@tetherto/wdk-wallet-ton-gasless` para los recibos gasless. Su release desplegada está en `_meta/versions.md`.

## Structural
- depends on → [[wdk-indexer-wrk-base]] because extiende sus workers `proc` y `api` con clientes TON y Jetton
- depends on → [[wdk-wallet-ton-gasless]] because `getGasLessTransactionReceipt` instancia su cuenta de solo lectura; en el lockfile arrastra también a `wdk-wallet-ton`
