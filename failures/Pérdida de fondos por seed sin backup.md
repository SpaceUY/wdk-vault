---
type: failure
status: shipped
source:
  - wdk-docs/content/docs/resources/concepts.mdx
  - wdk-docs/content/docs/tools/backup-cloud/index.mdx
  - wdk-docs/content/docs/tools/wdk-utils/guides/shamir-secret-sharing.mdx
---
# Pérdida de fondos por seed sin backup

Como la seed es la única forma de recuperar las cuentas y el WDK no guarda copias, perder el dispositivo sin un respaldo verificado deja los fondos inaccesibles. Un respaldo subido sin comprobar que descifra a la wallet esperada tampoco garantiza la recuperación. Cubrirlo es responsabilidad de la app: respaldo cifrado en la nube o reparto de la seed en partes.
