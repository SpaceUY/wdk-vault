---
type: moc
status: shipped
source:
  - wdk-app-node/CLAUDE.md
  - wdk-ork-wrk/CLAUDE.md
  - wdk-data-shard-wrk/CLAUDE.md
  - wdk-indexer-wrk-base/CLAUDE.md
  - wdk-docs/content/docs/tools/indexer-api/index.mdx
  - wdk-qualification-exercise/README.md
---
# MOC Backend e indexado

Mapa del backend de billeteras del WDK y de su indexado. El camino de una solicitud va de [[wdk-app-node]] a [[wdk-ork-wrk]] y de ahí a [[wdk-data-shard-wrk]], que consulta a los indexers; la falla [[Sin orks disponibles (503)]] se recorre hacia atrás hasta [[Descubrimiento de orks por hyperswarm]], y [[Balance desactualizado por caché]] hasta [[Caché de lecturas de 30 s en app-node]]. Las releases desplegadas de cada repo están en [[MOC Versiones]].

## Camino de una solicitud
- [[wdk-app-node]]
- [[Afinidad usuario-ork por CRC32]]
- [[Descubrimiento de orks por hyperswarm]]
- [[Capability del handshake ork debe coincidir]]
- [[wdk-ork-wrk]]
- [[Data shard por usuario]]
- [[wdk-data-shard-wrk]]

## Indexado
- [[wdk-indexer-wrk-base]]
- [[wdk-indexer-processor-wrk]]
- [[Stream de transferencias agrupadas en Redis]]
- [[wdk-indexer-wrk-btc]]
- [[wdk-indexer-wrk-evm]]
- [[wdk-indexer-wrk-solana]]
- [[wdk-indexer-wrk-spark]]
- [[wdk-indexer-wrk-ton]]
- [[wdk-indexer-wrk-tron]]

## Fallas
- [[Sin orks disponibles (503)]]
- [[Balance desactualizado por caché]]
- [[Caché de lecturas de 30 s en app-node]]

## Indexer API hospedada y el caso SpaceUY
- [[Indexer API]]
- [[wdk-indexer-http]]
- [[wdk-qualification-exercise]]

## Servicios de mercado que estos módulos pueden reemplazar
- [[Indexadores y nodos de terceros]]

## No modelado
Quedaron afuera los motores de base de datos (`hyperdb`, `mongodb`) y de lookup (`autobase`, `mongodb`), las migraciones, las métricas Prometheus, el circuito de `RpcBaseManager` entre proveedores, el rate limiting, el modo de sync por rango de los indexers, los trabajos programados de cada worker y el uso del trace id. Tampoco se modela la relación entre la Indexer API hospedada y estos workers, porque la documentación no la declara.
