---
type: concept
status: shipped
source:
  - wdk-docs/content/docs/resources/concepts.mdx
  - wdk-docs/content/docs/sdk/core-module/guides/error-handling.mdx
  - wdk-docs/content/docs/sdk/get-started.mdx
---
# Seed derivada en el dispositivo

En el WDK la app aporta una seed BIP-39 y cada módulo deriva de ella, en el propio dispositivo, las claves de su cadena con un path de derivación específico. Mientras la seed esté disponible se pueden volver a derivar todas las cuentas, y sin ella no hay forma de reconstruirlas. Esto vuelve a la seed el único activo que hay que proteger y respaldar.

## Structural
- requires → [[La seed nunca sale del dispositivo]] because la derivación solo es autocustodial si la seed no sale del entorno de la app
- requires → [[backup-cloud no cifra: la app cifra antes]] because la única recuperación posible pasa por un respaldo que la propia app cifró
