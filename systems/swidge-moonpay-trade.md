---
type: system
status: shipped
package: '@moonpay/wdk-protocol-swidge-moonpay-trade'
source:
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-moonpay-trade/index.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-moonpay-trade/configuration.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# swidge-moonpay-trade

Módulo comunitario (`@moonpay/wdk-protocol-swidge-moonpay-trade`) que conecta cuentas de WDK con la API SwapsXYZ de MoonPay para swaps y transferencias entre cadenas. `swidge()` pide una cotización nueva, crea el swap y envía el depósito a la dirección del proveedor, sin esperar la liquidación en destino. Hay que fijar `minAmountOut` y los límites de fee antes de ejecutar, porque la cotización indicativa no es la que se ejecuta.

## Structural
- depends on → [[wdk-wallet]] because la doc exige una cuenta escribible concreta (EVM, Bitcoin, TON, Tron, Solana o variantes de abstracción de cuentas) para enviar el depósito
- can replace → [[Agregadores de swap y bridge directos]] because puede asumir el rol de una integración directa con SwapsXYZ, pero exige una API key, `fetch` global y un provider RPC de la red de origen
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` la ejecución de depósitos mediante cuentas escribibles concretas, con verificación de mínimo de salida
