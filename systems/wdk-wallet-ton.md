---
type: system
status: shipped
package: '@tetherto/wdk-wallet-ton'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-ton/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-ton/api-reference.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-wallet-ton

Módulo estándar de TON: cuentas con contratos V5R1, saldos de TON y Jettons, y firmas Ed25519. Cambió el path de derivación por defecto y, más tarde, el esquema de firma de mensajes, que ya no es compatible con el anterior.

## Structural
- depends on → [[wdk-wallet]] because su manager extiende `WalletManager` del paquete base
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` el nuevo esquema de firma de mensajes
