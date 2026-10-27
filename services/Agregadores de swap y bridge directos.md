---
type: service
status: shipped
detect:
  - '@lifi/sdk'
  - '@0x/swap-ts-sdk'
  - api.0x.org
  - '@uniswap/sdk-core'
  - '@across-protocol/app-sdk'
source:
  - wdk-docs/content/docs/sdk/swidge-modules/index.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-0x/configuration.mdx
  - wdk-docs/content/docs/sdk/swap-modules/swap-velora-evm/index.mdx
  - wdk-docs/content/docs/tools/asset-registry/index.mdx
---
# Agregadores de swap y bridge directos

Categoría de mercado que agrupa los SDKs y APIs de agregadores de swap, puentes y servicios de ruteo que una app integra de forma directa para cotizar y ejecutar rutas. LI.FI, 0x, Uniswap y Across son ejemplos de la categoría y señales de `detect:`. La doc del WDK nombra a 0x y a LI.FI como proveedores detrás de módulos swidge y a Uniswap solo en un helper de listas de tokens de `wdk-asset-registry` y en un ejemplo de protocolo no registrado; Across no aparece en la doc ni en los repos. Reemplazar la integración directa por un módulo WDK no elimina al proveedor: la app sigue necesitando su API o su clave.
