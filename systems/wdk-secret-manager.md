---
type: system
status: shipped
package: '@tetherto/wdk-secret-manager'
source:
  - wdk-docs/content/docs/tools/secret-manager/index.mdx
  - wdk-docs/content/docs/tools/secret-manager/configuration.mdx
---
# wdk-secret-manager

Herramienta en memoria que genera la seed y la entropía BIP-39, las cifra con una passkey (PBKDF2 y libsodium secretbox) y las borra con `dispose()`. Existe para que la seed nunca se persista en claro. Funciona en Node y en Bare (paquete `@tetherto/wdk-secret-manager`).

## Structural
- mitigates → [[Fuga de seed por almacenamiento inseguro]] because cifra la seed con una passkey y la limpia de memoria
