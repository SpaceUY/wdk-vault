---
type: system
status: shipped
package: '@tetherto/wdk-wallet-solana'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-solana/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-solana/api-reference.mdx
---
# wdk-wallet-solana

Módulo de Solana con derivación SLIP-0010 y firma Ed25519, que maneja SOL, tokens SPL y mensajes de transacción prearmados. Cambió su path de derivación por defecto entre betas, por lo que las wallets creadas antes se importan indicando el path explícito, con todos los segmentos hardened.

## Structural
- depends on → [[wdk-wallet]] because su manager extiende `WalletManager` del paquete base
- causes → [[Breaking change entre betas]] because el cambio del path por defecto produjo direcciones distintas para una misma seed
