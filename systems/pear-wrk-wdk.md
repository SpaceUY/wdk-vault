---
type: system
status: shipped
package: '@tetherto/pear-wrk-wdk'
source:
  - wdk-docs/content/docs/tools/pear-wrk-wdk/index.mdx
  - wdk-docs/content/docs/tools/pear-wrk-wdk/configuration.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# pear-wrk-wdk

Capa de transporte y handlers para correr el WDK dentro de un worklet Bare, con un cliente y servidor HRPC y un servidor JSON-RPC para hosts nativos. Mantiene el estado y la firma fuera del hilo principal y transporta las claves y la seed cifrada como `Buffer`.

## Structural
- depends on → [[wdk]] because inicializa el WDK dentro del worklet con la seed cifrada que recibe
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` el paso de los campos secretos de base64 a `Buffer`
