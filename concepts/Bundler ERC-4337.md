---
type: concept
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/configuration.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-7702-gasless/index.mdx
---
# Bundler ERC-4337

El bundler es el servicio que recibe las `UserOperation` firmadas por la cuenta, las empaqueta y las envía a la cadena. Los módulos EVM con abstracción de cuentas del WDK lo exigen como `bundlerUrl`, y es una pieza separada del RPC de la cadena y del paymaster, aunque un mismo endpoint puede servir como bundler y como paymaster. Sin un bundler accesible la cuenta no puede construir, estimar ni enviar operaciones, porque el módulo lo usa en esas tres etapas.
