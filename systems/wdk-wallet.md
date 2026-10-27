---
type: system
status: shipped
package: '@tetherto/wdk-wallet'
source:
  - wdk-docs/content/docs/sdk/core-module/index.mdx
  - wdk-docs/content/docs/sdk/core-module/api-reference.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/index.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-wallet

`@tetherto/wdk-wallet` es el paquete base de wallets: define las interfaces compartidas (`WalletManager`, `IWalletAccount`, `ISigner`, disposal y contratos multisig) que implementan los módulos por cadena. Es un paquete distinto del orquestador `wdk` y se versiona por separado. Cada módulo por cadena concreta sus métodos, unidades de fee y flujo de transacción.

## Structural
- causes → [[Breaking change entre betas]] because el changelog marca varios cambios `[Breaking]` de contratos base entre betas consecutivas
