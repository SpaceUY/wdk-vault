---
type: system
status: shipped
package: '@0x/wdk-protocol-swidge-0x'
source:
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-0x/index.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-0x/configuration.mdx
---
# swidge-0x

Módulo comunitario (`@0x/wdk-protocol-swidge-0x`) que conecta una cuenta EVM de WDK con la API Swap v2 de 0x para swaps dentro de una misma cadena, con aprobación ERC-20 automática y estado derivado del receipt. No sirve para rutas entre cadenas: un `toChain` distinto del `chainId` configurado se rechaza. La cotización de `quoteSwidge()` es indicativa y distinta de la cotización firme que obtiene `swidge()`.

## Structural
- depends on → [[wdk-wallet-evm]] because la doc lo presenta como conexión entre una cuenta EVM de WDK y la API de 0x
- can replace → [[Agregadores de swap y bridge directos]] because puede asumir el rol del SDK o la API de 0x que la app llamaría a mano, pero sigue necesitando una API key de 0x y queda limitado a swaps en una sola cadena
