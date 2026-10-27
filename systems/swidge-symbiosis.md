---
type: system
status: shipped
package: '@symbiosis-finance/wdk-protocol-swidge-symbiosis'
source:
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-symbiosis/index.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-symbiosis/configuration.mdx
---
# swidge-symbiosis

Módulo comunitario (`@symbiosis-finance/wdk-protocol-swidge-symbiosis`) que sirve rutas dentro de una cadena, entre cadenas y combinadas por la API REST pública de Symbiosis, con ejecución desde cuentas EVM, Bitcoin, TON, Tron o Solana según lo que la cuenta soporte. Solo admite entrada exacta, y `swidge()` vuelve a pedir la ruta, de modo que montos y calldata pueden diferir de la cotización previa. Las rutas TON, Tron y Solana quedan solo para cotizar cuando la cuenta no tiene la capacidad que exigen.

## Structural
- depends on → [[wdk-wallet]] because la ejecución depende de las capacidades de la cuenta de WDK ligada, que el módulo comprueba al ejecutar
- can replace → [[Agregadores de swap y bridge directos]] because puede asumir el rol de una integración directa con la API de Symbiosis, que la doc describe como pública, pero queda limitado a entrada exacta y a los límites de tasa de la API
