---
type: system
status: shipped
package: '@tetherto/wdk-pricing-provider'
source:
  - wdk-docs/content/docs/tools/price-rates/index.mdx
  - wdk-docs/content/docs/tools/price-rates/api-reference.mdx
  - wdk-docs/content/docs/sdk/pricing-modules/index.mdx
---
# wdk-pricing-provider

Clase `PricingProvider` que envuelve uno o varios `PricingClient` para sumar caché en memoria del último precio y failover ordenado entre fuentes. Define también la interfaz abstracta `PricingClient` que implementan los módulos de precios, con precio actual, precios por lote, datos con variación y serie histórica.

## Associative
- resembles → [[wdk-failover-provider]] because ambos reintentan contra el siguiente candidato cuando uno falla, aquí con fuentes de precio y allá con providers genéricos
