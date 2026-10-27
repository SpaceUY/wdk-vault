---
type: constraint
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/configuration.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-7702-gasless/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-ton-gasless/configuration.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-solana-gasless/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron-gasfree/configuration.mdx
---
# Gasless requiere paymaster configurado

Ninguna variante gasless del WDK paga el fee por sí sola: en los modos gasless todas exigen que la app configure un tercero que lo cubra. En EVM y TON es un paymaster (`paymasterUrl` o `paymasterToken`), en Solana un paymaster compatible con Kora, y en TRON el servicio GasFree (`gasFreeProvider`), que cumple ese mismo rol aunque la doc no lo llame paymaster. Sin ese componente configurado no existe el camino gasless.

## Structural
- requires → [[Paymaster]] because sin un paymaster o relay configurado el fee no tiene quién lo cubra
