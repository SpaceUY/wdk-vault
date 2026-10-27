---
type: system
status: shipped
package: '@lifi/wdk-protocol-swidge-lifi'
source:
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-lifi/index.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-lifi/configuration.mdx
---
# swidge-lifi

Módulo comunitario (`@lifi/wdk-protocol-swidge-lifi`) que cotiza y ejecuta rutas de swap, bridge y combinadas por LI.FI desde cuentas EVM estándar y ERC-4337, con límites de fee en bps y una lista opcional de contratos confiables. LI.FI define el conjunto vivo de rutas, así que conviene consultar `getSupportedChains()` y `getSupportedTokens()` en runtime. Puede descubrir cadenas no EVM, pero solo ejecuta desde cuentas EVM.

## Structural
- depends on → [[wdk-wallet-evm]] because la doc declara soporte para cuentas `WalletAccountEvm` y de smart account ERC-4337, y exige direcciones EVM
- can replace → [[Agregadores de swap y bridge directos]] because puede asumir el rol del SDK de LI.FI, y la API key es opcional y se usa para límites de tasa mayores, pero las rutas son las que LI.FI sirve y solo se ejecutan desde cuentas EVM
