---
type: system
status: shipped
package: '@tetherto/wdk-wallet-btc'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-btc/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-btc/api-reference.mdx
---
# wdk-wallet-btc

Módulo de Bitcoin en capa base: cuentas SegWit nativas por defecto (BIP-84), soporte del path legacy BIP-44, manejo de UTXOs y envío de transacciones. El path por defecto cambió entre betas, así que la misma seed produce direcciones distintas según la versión y las wallets antiguas se recuperan con `getAccountByPath`.

## Structural
- depends on → [[wdk-wallet]] because su manager extiende `WalletManager` del paquete base
- causes → [[Breaking change entre betas]] because el cambio del path de derivación por defecto alteró las direcciones de una misma seed
