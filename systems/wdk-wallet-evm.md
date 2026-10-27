---
type: system
status: shipped
package: '@tetherto/wdk-wallet-evm'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm/api-reference.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-wallet-evm

Módulo estándar para cuentas compatibles con EVM, donde el usuario paga el gas con el token nativo. Deriva varias cuentas desde una sola seed con BIP-44 y cubre firma de mensajes, transferencias ERC-20 y estimación de fees. Sirve de base a los módulos privados de Hinkal y Bermuda.

## Structural
- depends on → [[wdk-wallet]] because su manager extiende `WalletManager` del paquete base
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` el cambio de overrides de gas en transferencias ERC-20

## Associative
- opens a question about → [[wdk-failover-provider]] because acepta una lista ordenada de providers como failover, pero la doc no dice si lo implementa con ese paquete
