---
type: system
status: shipped
source:
  - wdk-qualification-exercise/README.md
  - wdk-qualification-exercise/package.json
  - wdk-qualification-exercise/infra/wdk-stack/README.md
  - wdk-qualification-exercise/infra/wdk-stack/docker-compose.yml
  - wdk-qualification-exercise/apps/backend/README.md
  - wdk-qualification-exercise/apps/backend/package.json
  - wdk-qualification-exercise/apps/rn-wdk-exercise/package.json
  - wdk-docs/content/docs/tools/backup-cloud/guides/migrate-from-react-native.mdx
---
# wdk-qualification-exercise

Caso de SpaceUY que consume el stack: una app React Native (Expo) con billetera autocustodiada y un backend NestJS que detecta pagos en USDT, emite cupones de cashback y los paga en tokens ERC-20. Su carpeta `infra/wdk-stack` levanta en Docker una versión autoalojada del backend WDK (indexers de Ethereum, Bitcoin, Spark y Tron, processors, data shard, dos orks y `app-node`), que el README define como reemplazo opcional de la Indexer API hospedada. El backend elige su fuente de transferencias con `INDEXER_TRANSPORT`, y por defecto lee el stream de Redis de ese stack.

## Structural
- depends on → [[wdk-app-node]] because la app móvil registra billeteras y consulta historial contra su REST, y el backend le emite los JWT
- depends on → [[Stream de transferencias agrupadas en Redis]] because con el transporte `redis-stream`, que es el predeterminado, el backend abre su propio consumer group sobre él
- depends on → [[wdk-react-native-core]] because la app lo declara en su `package.json`
- depends on → [[wdk-wallet-evm]] because el backend firma con él el pago del cashback y la app lo declara
- depends on → [[wdk-wallet-evm-erc-4337]] because la app lo declara en su `package.json`
- depends on → [[wdk-wallet-btc]] because la app lo declara en su `package.json`
- depends on → [[wdk-wallet-spark]] because la app lo declara en su `package.json`
- depends on → [[wdk-wallet-tron]] because la app lo declara en su `package.json`
- depends on → [[wdk-backup-cloud-react-native]] because la app declara el paquete legado `@tetherto/wdk-backup-cloud-react-native`, que la guía de migración de la documentación reemplaza por `@tetherto/wdk-backup-cloud`

## Associative
- contrasts with → [[Indexer API]] because el backend conserva `INDEXER_TRANSPORT=hosted-api`, marcado como deprecado, para volver a ella en lugar de usar el stack autoalojado
