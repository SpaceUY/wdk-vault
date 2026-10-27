---
type: system
status: shipped
source:
  - wdk-indexer-wrk-solana/README.md
  - wdk-indexer-wrk-solana/package.json
  - wdk-indexer-wrk-solana/workers/lib/chain.solana.client.js
  - wdk-indexer-wrk-solana/config/solana.json.example
---
# wdk-indexer-wrk-solana

Indexer de Solana con workers `wrk-solana-indexer-*` para la moneda nativa y `wrk-spl-indexer-*` para tokens SPL. Obtiene los bloques de Bitquery; los RPC secundarios se usan solo para consultar saldos, y para eso instancia la cuenta de solo lectura de `@tetherto/wdk-wallet-solana`. Su release desplegada está en `_meta/versions.md`.

## Structural
- depends on → [[wdk-indexer-wrk-base]] because extiende sus workers `proc` y `api` con clientes Solana y SPL
- depends on → [[wdk-wallet-solana]] because su cuenta de solo lectura resuelve los saldos contra el RPC configurado
