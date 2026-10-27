---
type: system
status: shipped
package: wdk-protocol-swidge-orchestra
source:
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-orchestra/index.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-orchestra/configuration.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/index.mdx
---
# swidge-orchestra

Módulo comunitario mantenido por Flashnet (paquete `wdk-protocol-swidge-orchestra`, sin scope) que implementa `SwidgeProtocol` para rutas de BTC y stablecoins que sirve Flashnet Orchestra. `quoteSwidge()` no tiene efectos; `swidge()` y `executeSwapIntent()` pueden mover fondos de la cuenta de origen, por lo que la app debe persistir el intent y el estado antes y después del pago. Lightning no debe exponerse como origen.

## Structural
- depends on → [[wdk-wallet]] because envía los pagos de origen desde cuentas de WDK y registra las cuentas fuente
- can replace → [[Agregadores de swap y bridge directos]] because puede asumir el rol de una integración directa con Orchestra, pero requiere una API key de Flashnet y solo cubre las rutas de BTC y stablecoins que Orchestra devuelve
