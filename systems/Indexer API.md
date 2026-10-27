---
type: system
status: shipped
source:
  - wdk-docs/content/docs/tools/indexer-api/index.mdx
  - wdk-docs/content/docs/tools/indexer-api/get-started.mdx
  - wdk-docs/content/docs/tools/indexer-api/api-reference.mdx
  - wdk-qualification-exercise/README.md
---
# Indexer API

API REST hospedada por Tether que devuelve saldos, transferencias e historial por dirección para varias cadenas, con una API key en el header `x-api-key`. La documentación no dice cómo está construida ni si corre los workers de estos repos. El único vínculo que aparece está en el README del caso de SpaceUY, que presenta su stack autoalojado como reemplazo opcional de esta API hospedada.

## Structural
- can replace → [[Indexadores y nodos de terceros]] because cubre saldos y transferencias por dirección, a condición de que el proyecto dependa de un servicio de Tether con API key, de los límites de tasa documentados y de las cadenas y tokens que publica `GET /api/v1/chains`

## Associative
- opens a question about → [[wdk-app-node]] because ambos exponen `/api/v1/health` y `/api/v1/chains`, pero `app-node` usa JWT y rutas propias de billetera, y la doc no aclara si el servicio hospedado es una instancia de ese gateway
- opens a question about → [[wdk-indexer-wrk-base]] because sus indexers responden `getBalance` y `queryTransfersByAddress` por RPC, y la doc no dice si esta API los consulta
