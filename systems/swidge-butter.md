---
type: system
status: shipped
package: '@butternetwork/wdk-protocol-swidge-butter'
source:
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-butter/index.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/swidge-butter/configuration.mdx
---
# swidge-butter

Módulo comunitario (`@butternetwork/wdk-protocol-swidge-butter`) que descubre rutas, cotiza entrada exacta y ejecuta swaps en una cadena y operaciones entre cadenas por el servicio de ruteo de Butter. Descubrir y cotizar no requiere cuenta; ejecutar sí, y la ruta EVM incorporada valida el destino mínimo solo en el caso de una misma cadena. Una cotización fijada vive en una sola instancia y no se restaura tras un reinicio.

## Structural
- depends on → [[wdk-wallet]] because la ejecución exige una cuenta de WDK que pueda enviar las transacciones de la cadena de origen
- can replace → [[Agregadores de swap y bridge directos]] because puede asumir el rol de una integración directa con Butter, pero requiere un `entrance` emitido por Butter, credenciales de API según `authMode` y solo admite operaciones de entrada exacta
