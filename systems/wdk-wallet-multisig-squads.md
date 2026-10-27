---
type: system
status: shipped
package: '@tetherto/wdk-wallet-multisig-squads'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-multisig-squads/index.mdx
  - wdk-docs/content/docs/sdk/core-module/api-reference.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-wallet-multisig-squads

Módulo para bóvedas Squads en Solana, con permisos por miembro, votos on-chain y timelock opcional. Distingue tres direcciones (la cuenta de configuración, la bóveda que guarda los fondos y la cuenta de cada miembro), y un `transaction.hash` no implica que el pago de la bóveda se haya ejecutado.

## Structural
- depends on → [[wdk-wallet]] because implementa los contratos multisig que exporta el paquete base
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` el resultado de aprobaciones off-chain
