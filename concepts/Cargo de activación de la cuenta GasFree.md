---
type: concept
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron-gasfree/guides/send-transactions.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron-gasfree/api-reference.mdx
---
# Cargo de activación de la cuenta GasFree

En `wdk-wallet-tron-gasfree`, si la cuenta GasFree del usuario todavía no está activa, el fee de la transferencia incluye un cargo de activación que informa el proveedor y se paga en el token, no en TRX. `quoteTransfer()` y `transfer()` lo devuelven aparte como `activationFee`, que vale `0n` cuando no corresponde. Conviene cotizar antes de la primera transferencia para que el usuario sepa que el token tiene que cubrir ese cargo.
