---
type: system
status: shipped
package: '@tetherto/wdk-pricing-coingecko-http'
source:
  - wdk-docs/content/docs/sdk/pricing-modules/pricing-coingecko-http/index.mdx
  - wdk-docs/content/docs/sdk/pricing-modules/pricing-coingecko-http/configuration.mdx
---
# pricing-coingecko-http

Cliente `PricingClient` respaldado por CoinGecko (`@tetherto/wdk-pricing-coingecko-http`) para precios actuales, por lote, con variación de 24 horas y series históricas. Trae un mapa de tickers a ids de CoinGecko para cinco activos y se amplía con la opción `coinIds`. Acepta una API key demo o pro, y queda sujeto a los límites de tasa de CoinGecko.

## Structural
- depends on → [[wdk-pricing-provider]] because su clase extiende el `PricingClient` base que ese paquete define
- can replace → [[Feeds de precio de terceros]] because puede asumir el rol de llamar a la API de CoinGecko a mano, pero sigue consumiendo CoinGecko, con sus límites de tasa, la disponibilidad de datos y el nivel de la API key, y solo mapea de fábrica cinco activos
