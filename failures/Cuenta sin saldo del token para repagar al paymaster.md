---
type: failure
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/guides/handle-errors.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/configuration.mdx
---
# Cuenta sin saldo del token para repagar al paymaster

En `wdk-wallet-evm-erc-4337`, un envío o una transferencia en modo Paymaster Token puede fallar porque la Safe no tiene saldo del token con el que repagarle al paymaster. El módulo lo reporta como `TransactionError` con `INSUFFICIENT_BALANCE`, también cuando el error AA50 aparece al estimar el fee o al construir la operación. Tener el paymaster bien configurado no alcanza si la cuenta no conserva ese saldo.
