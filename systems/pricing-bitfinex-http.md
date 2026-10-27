---
type: system
status: shipped
package: '@tetherto/wdk-pricing-bitfinex-http'
source:
  - wdk-docs/content/docs/tools/price-rates/index.mdx
  - wdk-docs/content/docs/sdk/pricing-modules/index.mdx
---
# pricing-bitfinex-http

Cliente `PricingClient` respaldado por Bitfinex (`@tetherto/wdk-pricing-bitfinex-http`) para precios actuales, por lote e históricos, que la doc de Price Rates presenta como su base. Traduce símbolos comunes a códigos de Bitfinex (`USDT` pasa a `UST`) y devuelve `null` para los pares que Bitfinex no cotiza directamente. Es compatible con `PricingProvider`.

## Structural
- can replace → [[Feeds de precio de terceros]] because puede asumir el rol de un feed de precios de terceros, pero cubre solo los pares que Bitfinex cotiza directamente y devuelve `null` para el resto

## Associative
- contrasts with → [[pricing-coingecko-http]] because ambos son fuentes `PricingClient`: Bitfinex cotiza solo pares directos y CoinGecko mapea tickers a ids y admite una API key
