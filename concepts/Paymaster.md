---
type: concept
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/configuration.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-7702-gasless/index.mdx
---
# Paymaster

En ERC-4337 el paymaster es el servicio, con su contrato asociado, que se hace cargo del costo de una `UserOperation`: o la patrocina según una política, o se la cobra al usuario en un token ERC-20 en lugar del token nativo. Los módulos EVM del WDK lo reciben como `paymasterUrl`, `paymasterAddress` y `paymasterToken`, y lo proveen terceros: la app no lo trae incluido en el paquete. Es la pieza que permite que una cuenta con USD₮ y sin token nativo pague su fee.

## Structural
- mitigates → [[Usuario con USD₮ y sin token nativo no puede transferir]] because al cobrar el fee en el token del paymaster o patrocinarlo, la cuenta no necesita saldo nativo, siempre que el paymaster esté configurado y soporte el token
