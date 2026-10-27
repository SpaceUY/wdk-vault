---
type: decision
status: shipped
source:
  - wdk-docs/content/docs/overview/vision.mdx
  - wdk-docs/content/docs/overview/about.mdx
---
# Diseñar el WDK como autocustodial sin custodio intermediario

Tether presenta el WDK como un toolkit open source y autocustodial, sin lock-in y sin gatekeepers, a diferencia de los proveedores cerrados de infraestructura de wallets como servicio. Esa postura implica que las claves nunca salen del control del usuario y que la seed la gestiona la app, no el SDK. Es el origen de la restricción que ordena toda esta espina.

## Structural
- establishes → [[La seed nunca sale del dispositivo]] because la visión de control total del usuario sobre sus activos exige que el SDK no retenga la seed
