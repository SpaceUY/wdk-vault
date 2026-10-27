---
type: system
status: shipped
package: '@tetherto/wdk-protocol-swap-velora-evm'
source:
  - wdk-docs/content/docs/sdk/swap-modules/swap-velora-evm/index.mdx
  - wdk-docs/content/docs/sdk/swap-modules/swap-velora-evm/configuration.mdx
---
# swap-velora-evm

Módulo de Tether (`@tetherto/wdk-protocol-swap-velora-evm`) que cotiza con `quoteSwap` y ejecuta swaps de tokens en redes EVM a través del agregador Velora. Funciona con cuentas EVM estándar y smart accounts ERC-4337, y con cuentas de solo lectura para cotizar. La doc advierte que ciertas versiones no inicializan con cuentas derivadas de managers cuyo provider ethers compartido no ofrece `request()` de EIP-1193; las versiones están en `_meta/versions.md`.

## Structural
- depends on → [[wdk-wallet-evm]] because la doc lista las cuentas de ese módulo como compatibles y exige un provider EVM en `account._config.provider`
- can replace → [[Agregadores de swap y bridge directos]] because puede asumir el rol del SDK de un agregador, y la configuración documentada no pide clave de API, pero queda limitado a las redes que soporta Velora y exige un provider RPC en la cuenta
