---
type: system
status: shipped
package: '@tetherto/wdk-wallet-spark'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-spark/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-spark/api-reference.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/which-wallet-module.mdx
---
# wdk-wallet-spark

Módulo para la red Spark, una capa 2 de Bitcoin, con pagos Lightning, facturas Spark y depósitos y retiros hacia la capa base. Es la opción cuando se necesitan pagos Lightning y no operaciones directas sobre la cadena de Bitcoin.

## Structural
- depends on → [[wdk-wallet]] because su manager extiende `WalletManager` del paquete base

## Associative
- contrasts with → [[wdk-wallet-btc]] because el selector de módulos los separa: Lightning sobre Spark frente a Bitcoin en capa base
