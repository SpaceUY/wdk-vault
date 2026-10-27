---
type: constraint
status: shipped
source:
  - wdk-docs/content/docs/overview/about.mdx
  - wdk-docs/content/docs/sdk/core-module/guides/error-handling.mdx
  - wdk-docs/content/docs/resources/concepts.mdx
---
# La seed nunca sale del dispositivo

El WDK no es dueño de la seed: la recibe de la app, que decide dónde se guarda, cuándo se descifra y cuándo se limpia con `dispose()`. Ninguna pieza del WDK guarda una copia del lado servidor ni envía la seed a un tercero, y por eso las claves no salen del control del usuario. El costo es que nadie más puede restaurarla.

## Structural
- forbids → [[Fuga de seed por almacenamiento inseguro]] because guardar la seed en claro en un lugar que no controla el dispositivo rompe la garantía
- causes → [[Pérdida de fondos por seed sin backup]] because al no existir otra copia, perder el dispositivo sin respaldo propio pierde el acceso
