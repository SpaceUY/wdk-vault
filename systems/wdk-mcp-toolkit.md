---
type: system
status: shipped
package: '@tetherto/wdk-mcp-toolkit'
source:
  - wdk-docs/content/docs/ai/mcp-toolkit/index.mdx
  - wdk-docs/content/docs/ai/mcp-toolkit/configuration.mdx
---
# wdk-mcp-toolkit

Biblioteca para construir servidores MCP que dan a agentes de IA acceso a wallets autocustodiales del WDK (`@tetherto/wdk-mcp-toolkit`): extiende `McpServer` del SDK oficial y trae herramientas de wallets, precios, indexer, swaps, bridges, lending y fiat. Las operaciones de escritura piden confirmación al usuario por elicitations, y la seed queda local. La doc advierte no registrar ciertos adaptadores de swap, bridge y lending con ciertas versiones del wallet EVM; las versiones están en `_meta/versions.md`.

## Structural
- depends on → [[wdk-wallet]] because cada cadena se habilita registrando con `registerWallet()` un módulo de wallet de WDK

## Associative
- contrasts with → [[wdk-cli]] because la doc ofrece el CLI como alternativa lista para usar cuando no hace falta construir un servidor MCP propio
