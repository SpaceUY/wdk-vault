---
type: system
status: shipped
source:
  - wdk-indexer-wrk-btc/README.md
  - wdk-indexer-wrk-btc/package.json
  - wdk-indexer-wrk-btc/workers/lib/chain.btc.client.js
  - wdk-indexer-wrk-btc/config/bitcoin.json.example
---
# wdk-indexer-wrk-btc

Indexer de Bitcoin: un worker `proc` escanea la cadena y un worker `api` responde saldos e historial por dirección, convirtiendo el modelo UTXO al formato `from`/`to` común de los indexers. Lee de un nodo Bitcoin Core por RPC o de proveedores externos de tipo `quicknode` y `blockbook`, con uno principal y varios secundarios. A diferencia de los demás, no declara ningún módulo `wdk-wallet-*` en su `package.json` ni en su lockfile. Su release desplegada está en `_meta/versions.md`.

## Structural
- depends on → [[wdk-indexer-wrk-base]] because extiende sus workers `proc` y `api` con un `ChainBaseClient` de Bitcoin
