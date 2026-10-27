---
type: system
status: shipped
package: '@tetherto/wdk-protocol-fiat-moonpay'
source:
  - wdk-docs/content/docs/sdk/fiat-modules/fiat-moonpay/index.mdx
  - wdk-docs/content/docs/sdk/fiat-modules/fiat-moonpay/configuration.mdx
  - wdk-docs/content/docs/sdk/fiat-modules/index.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# fiat-moonpay

Módulo de Tether (`@tetherto/wdk-protocol-fiat-moonpay`) que genera URLs de widget de MoonPay, firmadas o sin firmar, para comprar y vender cripto con fiat dentro de la app, además de cotizaciones y estado de transacciones. La firma se delega en un callback `signUrl` que debe correr en un backend de confianza. Los activos, redes y países disponibles los define MoonPay y se consultan en runtime.

## Structural
- can replace → [[On-ramp integrado a mano]] because puede asumir el rol de la integración del widget de MoonPay, y los flujos de KYC los resuelve el proveedor, pero requiere una cuenta de desarrollador de MoonPay, su `apiKey` y, para URLs firmadas, un backend que firme
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` el reemplazo de la firma con `secretKey` por el callback `signUrl` opcional
