---
type: system
status: shipped
package: '@tetherto/wdk-wallet-multisig-safe'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-multisig-safe/index.mdx
  - wdk-docs/content/docs/sdk/core-module/api-reference.mdx
---
# wdk-wallet-multisig-safe

Módulo para cuentas Safe en EVM donde el gasto requiere las firmas de un umbral de owners. En lugar de `sendTransaction()` expone propuestas que se aprueban y se ejecutan como UserOperations de ERC-4337, y la firma de un solo owner no alcanza si el umbral exige más.

## Structural
- depends on → [[wdk-wallet]] because implementa los contratos multisig que exporta el paquete base
