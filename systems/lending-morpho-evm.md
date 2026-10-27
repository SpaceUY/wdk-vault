---
type: system
status: shipped
package: '@morpho-org/wdk-protocol-lending-morpho-evm'
source:
  - wdk-docs/content/docs/sdk/lending-modules/lending-morpho-evm/index.mdx
  - wdk-docs/content/docs/sdk/lending-modules/index.mdx
---
# lending-morpho-evm

Módulo comunitario (`@morpho-org/wdk-protocol-lending-morpho-evm`) para depositar y retirar de vaults Morpho V2 y operar mercados Morpho Blue (colateral, préstamo, repago) desde cuentas EVM, apoyado en `@morpho-org/morpho-sdk`. Trae presets para Ethereum mainnet, pero los vaults fuera de ellos se configuran de forma explícita tras verificar su activo subyacente y su exposición. Expone helpers de requirements para las aprobaciones y firmas que pide el SDK de Morpho.

## Structural
- depends on → [[wdk-wallet-evm]] because la doc lista las cuentas de ese módulo y las ERC-4337 como compatibles
