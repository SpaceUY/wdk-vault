---
type: system
status: shipped
package: '@tetherto/wdk-protocol-lending-aave-evm'
source:
  - wdk-docs/content/docs/sdk/lending-modules/lending-aave-evm/index.mdx
  - wdk-docs/content/docs/sdk/lending-modules/lending-aave-evm/configuration.mdx
---
# lending-aave-evm

Módulo de Tether (`@tetherto/wdk-protocol-lending-aave-evm`) para suministrar, retirar, pedir prestado y repagar en Aave V3 desde cuentas EVM, con cotizadores (`quoteSupply`, `quoteBorrow`) y lectura de colateral, deuda y health factor. Supply y repay exigen una aprobación de token aparte hacia el Pool de Aave, y la app aporta el provider RPC y las direcciones correctas del Pool y de los tokens. Como Velora y el bridge USD₮0, ciertas versiones no inicializan con cuentas derivadas de managers con provider ethers compartido.

## Structural
- depends on → [[wdk-wallet-evm]] because la doc lista las cuentas de ese módulo como compatibles y exige que la cuenta exponga el provider EVM
