---
type: concept
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/configuration.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/guides/handle-errors.mdx
---
# Modos de pago de gas en ERC-4337

`wdk-wallet-evm-erc-4337` ofrece tres modos de pago, de los que se activa uno solo: Paymaster Token (el fee se cobra en un ERC-20), Sponsorship Policy (un patrocinador cubre el fee, con `isSponsored`) y Native Coins (el usuario paga con el token nativo, con `useNativeCoins`). Solo los dos primeros evitan que la cuenta necesite saldo nativo, y el modo Paymaster Token exige además que la Safe conserve saldo del token para repagar al paymaster.

## Structural
- causes → [[Cuenta sin saldo del token para repagar al paymaster]] because en modo Paymaster Token el fee se descuenta del saldo de la Safe, y si ese saldo no alcanza el envío falla con un error de saldo insuficiente
