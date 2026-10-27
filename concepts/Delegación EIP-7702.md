---
type: concept
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-7702-gasless/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-7702-gasless/configuration.mdx
---
# Delegación EIP-7702

Con EIP-7702 una dirección EOA delega su ejecución en un contrato de smart account, de modo que conserva su dirección y aun así puede operar mediante `UserOperation`. En `wdk-wallet-evm-7702-gasless` ese contrato es el `delegationAddress` de la configuración, y la doc lo trata como dato sensible a verificar antes de usar fondos reales. La delegación y el EntryPoint tienen que corresponder a la misma versión.
