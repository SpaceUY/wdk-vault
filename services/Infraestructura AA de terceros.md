---
type: service
status: shipped
detect:
  - '@biconomy/account'
  - '@alchemy/aa-core'
  - '@account-kit/smart-contracts'
  - '@gelatonetwork/relay-sdk'
  - permissionless
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/configuration.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-7702-gasless/guides/get-started.mdx
---
# Infraestructura AA de terceros

Categoría de mercado que agrupa los SDKs de smart accounts del lado cliente y los bundlers y paymasters hospedados por terceros, que las apps usan para enviar `UserOperation`. Biconomy, Alchemy AA, Gelato y `permissionless` son ejemplos de esta categoría y las señales de `detect:`: la documentación del WDK no los nombra. La doc del WDK sí cita a Candide, Pimlico y Openfort como proveedores de bundler y paymaster, y la app sigue necesitando uno de ellos.
