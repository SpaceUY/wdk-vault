---
type: system
status: draft
source:
  - https://github.com/tetherto/wdk-examples
  - wdk-docs/content/docs/ai/mcp-toolkit/langchain.mdx
---
# wdk-examples

Repo de ejemplos ejecutables, con una carpeta por paquete o integración (`wdk`, wallets EVM, ERC-4337, Solana, TON y TRON, `mcp-toolkit` y `walletconnect-walletkit`) y un `package.json` propio en cada una. La documentación solo lo cita desde la página de LangChain del MCP toolkit, para los ejemplos de agentes. En npm el paquete `@tetherto/wdk-examples` es un placeholder, así que se usa clonando el repo; la mayoría de los ejemplos con transacciones solo cotizan salvo que se active `ACTUALLY_SEND=true`.
