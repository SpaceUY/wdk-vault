---
type: service
status: shipped
detect:
  - api.coingecko.com
  - coinmarketcap
  - '@chainlink/contracts'
source:
  - wdk-docs/content/docs/sdk/pricing-modules/index.mdx
  - wdk-docs/content/docs/sdk/pricing-modules/pricing-coingecko-http/configuration.mdx
  - wdk-docs/content/docs/tools/price-rates/index.mdx
  - wdk-qualification-exercise/apps/backend/src/config/prices.config.ts
  - wdk-qualification-exercise/apps/backend/src/prices/prices.service.ts
---
# Feeds de precio de terceros

Categoría de mercado que agrupa las fuentes externas de precios actuales e históricos de activos, ya sean APIs HTTP o oráculos on-chain. CoinGecko, CoinMarketCap y Chainlink son ejemplos de la categoría y señales de `detect:`. La doc del WDK nombra a CoinGecko y a Bitfinex como fuentes de sus módulos de precios, y el backend del caso SpaceUY llama a `api.coingecko.com` por su cuenta, con un proxy y una caché propios. CoinMarketCap y Chainlink no aparecen en la doc ni en los repos, y un oráculo on-chain como Chainlink no es un feed HTTP que un cliente de precios del WDK pueda reemplazar.
