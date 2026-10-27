---
type: constraint
status: shipped
source:
  - wdk-docs/content/docs/overview/about.mdx
  - wdk-docs/content/docs/sdk/core-module/guides/error-handling.mdx
  - wdk-docs/content/docs/resources/concepts.mdx
---
# La seed nunca sale del dispositivo

El WDK no es dueño de la seed: la recibe de la app, que decide dónde se guarda, cuándo se descifra y cuándo se limpia con `dispose()`. La documentación lo describe como una arquitectura autocustodial y sin estado, en la que las claves no salen del control del usuario. Eso no impide los respaldos que la propia app cifra antes de subirlos: lo que la restricción excluye es que la seed salga sin cifrar.

## Structural
- forbids → [[Fuga de seed por almacenamiento inseguro]] because guardar o enviar la seed sin cifrar fuera del control de la app rompe la garantía
