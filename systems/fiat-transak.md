---
type: system
status: shipped
package: '@transak/wdk-protocol-fiat-transak'
source:
  - wdk-docs/content/docs/sdk/fiat-modules/fiat-transak/index.mdx
  - wdk-docs/content/docs/sdk/fiat-modules/fiat-transak/configuration.mdx
  - wdk-docs/content/docs/sdk/fiat-modules/index.mdx
---
# fiat-transak

Módulo comunitario (`@transak/wdk-protocol-fiat-transak`), en beta según la doc, que arma URLs de widget y cotizaciones de Transak para comprar y vender cripto con fiat. Debe correr en el backend, junto con los callbacks `widgetUrl` y `getOrder`, porque envía la API key de partner y los secretos no pueden salir del servidor. Conviene usar una cuenta de solo lectura o ninguna en ese entorno.

## Structural
- can replace → [[On-ramp integrado a mano]] because puede asumir el rol de la integración del widget de Transak, y los flujos de KYC los resuelve el proveedor, pero requiere una cuenta de partner de Transak y un backend con IP de salida estática autorizada por Transak
