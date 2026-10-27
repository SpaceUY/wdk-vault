---
type: service
status: shipped
detect:
  - alchemy-sdk
  - moralis
  - '@covalenthq/client-sdk'
  - '@quicknode/sdk'
  - api.etherscan.io
  - tronscan
source:
  - wdk-docs/content/docs/tools/indexer-api/index.mdx
  - wdk-indexer-wrk-evm/config/eth.json.example
  - wdk-indexer-wrk-btc/config/bitcoin.json.example
  - wdk-indexer-wrk-solana/config/solana.json.example
  - wdk-docs/content/docs/ai/mcp-toolkit/configuration.mdx
---
# Indexadores y nodos de terceros

Categoría de mercado que agrupa las APIs hospedadas que devuelven saldos, transferencias e historial por dirección, y los proveedores de nodos RPC que las alimentan. Moralis, Covalent, Etherscan y Tronscan son ejemplos de la categoría y señales de `detect:`: ni la documentación del WDK ni los repos los nombran. Alchemy y QuickNode sí aparecen, pero solo como proveedores RPC en URLs y configs de ejemplo, y los indexers del WDK siguen necesitando al menos uno por cadena.
