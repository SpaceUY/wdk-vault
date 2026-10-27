---
type: system
status: shipped
package: '@tetherto/wdk-utils'
source:
  - wdk-docs/content/docs/tools/wdk-utils/index.mdx
  - wdk-docs/content/docs/tools/wdk-utils/guides/shamir-secret-sharing.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-utils

Funciones sueltas para validar direcciones por cadena, parsear pagos y facturas, cifrar seeds con una passphrase y repartir un mnemónico en partes con Shamir. Las partes son material de recuperación sin cifrar y deben guardarse en lugares separados.

## Structural
- mitigates → [[Pérdida de fondos por seed sin backup]] because permite repartir el mnemónico en partes y recuperarlo con un umbral
- mitigates → [[Fuga de seed por almacenamiento inseguro]] because cifra la seed con una passphrase antes de persistirla
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` cambios en los resultados de validación de direcciones

## Associative
- contrasts with → [[wdk-secret-manager]] because ambos cifran seeds con una passphrase, con esquemas distintos (AES-GCM con scrypt frente a secretbox con PBKDF2)
