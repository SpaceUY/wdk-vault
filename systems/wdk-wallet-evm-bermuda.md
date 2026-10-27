---
type: system
status: draft
package: '@bermuda/wdk-wallet-evm-bermuda'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-bermuda/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/index.mdx
---
# wdk-wallet-evm-bermuda

Módulo comunitario en beta (paquete `@bermuda/wdk-wallet-evm-bermuda`) que deriva cuentas blindadas de Bermuda desde un wallet EVM y las expone con `getBermudaAccount()`. Se instala desde GitHub y no desde npm, y la doc lo limita a Plasma testnet; tener cuentas blindadas no establece anonimato ni disponibilidad productiva.

## Structural
- depends on → [[wdk-wallet-evm]] because su manager extiende el manager EVM y suma `getBermudaAccount()`

## Associative
- contrasts with → [[wdk-wallet-evm-hinkal]] because ambos dan privacidad en EVM: cuentas blindadas con pool propio frente a envíos privados con retiro programado
