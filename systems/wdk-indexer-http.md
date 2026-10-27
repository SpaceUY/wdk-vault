---
type: system
status: shipped
package: '@tetherto/wdk-indexer-http'
source:
  - wdk-docs/content/docs/tools/indexer-api/sdk.mdx
  - wdk-docs/content/docs/tools/indexer-api/sdk-api-reference.mdx
---
# wdk-indexer-http

Cliente JavaScript para Node.js y Bare que llama a la Indexer API: consulta saldos y transferencias, procesa resultados por lote y registra billeteras para que el servidor sincronice sus transferencias. No genera claves ni firma transacciones. Acepta un `baseUrl` para apuntar a otro despliegue del Indexer, pero la doc no dice qué despliegue distinto del hospedado sería válido.

## Structural
- depends on → [[Indexer API]] because cada método es una llamada HTTP a sus endpoints bajo `/api/v1`

## Associative
- opens a question about → [[wdk-data-shard-wrk]] because `registerWallets` y `getWalletTransfers` se parecen a las billeteras y la sincronización de transferencias de un shard, pero la doc no relaciona ambos
