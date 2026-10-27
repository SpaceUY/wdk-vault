---
type: failure
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-ton-gasless/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron-gasfree/index.mdx
---
# Usuario con USD₮ y sin token nativo no puede transferir

Con un módulo estándar, como `wdk-wallet-evm`, el usuario paga el gas con el token nativo de la cadena. Si solo tiene USD₮ y ninguna cantidad de ETH, TON o TRX, no puede enviar ni siquiera la transferencia que quería hacer. Los módulos gasless existen para ese caso, pero ninguno lo elimina por completo: dependen de un paymaster o relay configurado y de que el token de pago esté soportado.
