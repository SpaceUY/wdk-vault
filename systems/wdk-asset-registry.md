---
type: system
status: shipped
package: '@tetherto/wdk-asset-registry'
source:
  - wdk-docs/content/docs/tools/asset-registry/index.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-asset-registry

Registro en memoria de metadatos estandarizados de activos (id, símbolo, decimales, chain id y dirección del contrato) con listas incluidas de tokens comunes. No lee balances, precios ni estado de cadena: sirve para que wallets, protocolos y UI compartan una misma identidad de activo.

## Structural
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` que `getTokenByAddress()` pase a distinguir mayúsculas
