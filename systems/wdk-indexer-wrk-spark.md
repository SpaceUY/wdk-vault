---
type: system
status: shipped
source:
  - wdk-indexer-wrk-spark/README.md
  - wdk-indexer-wrk-spark/package.json
  - wdk-indexer-wrk-spark/workers/lib/chain.spark.client.js
  - wdk-indexer-wrk-spark/workers/lib/providers/spark.js
  - wdk-indexer-wrk-spark/config/spark.json.example
---
# wdk-indexer-wrk-spark

Indexer de Spark, la capa 2 de Bitcoin: un `proc` sincroniza transferencias desde la API de Sparkscan, con un `apiKey` en su configuración, y un `api` las sirve por RPC. Carga `@tetherto/wdk-wallet-spark` de forma diferida para armar una cuenta de solo lectura. Su release desplegada está en `_meta/versions.md`.

## Structural
- depends on → [[wdk-indexer-wrk-base]] because extiende sus workers `proc` y `api` con un cliente Spark
- depends on → [[wdk-wallet-spark]] because usa su cuenta de solo lectura en el cliente de la cadena
