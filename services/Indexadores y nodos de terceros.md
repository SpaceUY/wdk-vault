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
  - wdk-qualification-exercise/apps/rn-wdk-exercise/utils/explorer.ts
---
# Indexadores y nodos de terceros

Categoría de mercado que agrupa las APIs hospedadas que devuelven saldos, transferencias e historial por dirección, y los proveedores de nodos RPC que las alimentan. Moralis, Covalent, Etherscan y Tronscan son ejemplos de la categoría y señales de `detect:`. Moralis y Covalent no aparecen en la documentación ni en los repos; Etherscan y Tronscan aparecen solo como enlaces de explorador en la app del caso SpaceUY, que no es una dependencia de indexado, así que una coincidencia de `detect:` con esos enlaces no cuenta como uso del servicio. Alchemy y QuickNode aparecen solo como proveedores RPC en URLs y configs de ejemplo, y los indexers del WDK siguen necesitando al menos uno por cadena.
