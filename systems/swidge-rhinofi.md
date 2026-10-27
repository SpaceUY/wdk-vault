---
type: system
status: shipped
package: '@rhino.fi/wdk-protocol-swidge-rhinofi'
source:
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-rhinofi/index.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-rhinofi/configuration.mdx
---
# swidge-rhinofi

Módulo comunitario (`@rhino.fi/wdk-protocol-swidge-rhinofi`) que cotiza y ejecuta swaps y bridges entre cadenas por Rhino.fi con cuentas EVM de WDK, incluidas las ERC-4337. Resuelve cuando el depósito de origen se difunde, y la liquidación entre cadenas sigue de forma asíncrona, por lo que se consulta con `getSwidgeStatus()`. Cada llamada, incluso el descubrimiento, está autenticada con una API key.

## Structural
- depends on → [[wdk-wallet-evm]] because firma los depósitos de origen con cuentas de ese módulo
- can replace → [[Agregadores de swap y bridge directos]] because puede asumir el rol de una integración directa con Rhino.fi, pero exige una API key para cada llamada y hoy solo ejecuta desde origen EVM, con Solana, TON y Tron marcados como planeados
