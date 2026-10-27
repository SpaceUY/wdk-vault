---
type: system
status: shipped
package: '@tetherto/wdk'
source:
  - wdk-docs/content/docs/sdk/core-module/index.mdx
  - wdk-docs/content/docs/sdk/core-module/api-reference.mdx
  - wdk-docs/content/docs/sdk/core-module/guides/error-handling.mdx
  - wdk-docs/content/docs/start-building/nodejs-bare-quickstart.mdx
  - wdk-docs/content/docs/ai/agent-skills.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk

`@tetherto/wdk` es el orquestador del SDK: recibe una seed de la app, registra los módulos de wallet y de protocolo y expone una interfaz única para operar cuentas en varias cadenas. No guarda ni gestiona la seed por su cuenta. Ese modelo le permite ocupar el lugar de proveedores hospedados de custodia o de wallets embebidas.

## Structural
- depends on → [[wdk-wallet]] because los managers que registra extienden `WalletManager` del paquete base
- requires → [[Seed derivada en el dispositivo]] because el constructor recibe la seed que la app genera o descifra
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` cambios de contrato de las políticas entre betas
- can replace → [[Custodia tercerizada (MPC)]] because solo si la app asume la custodia, la recuperación y el respaldo de la seed, que dejan de estar en manos de un proveedor
- can replace → [[Wallets embebidas WaaS]] because reemplaza las cuentas y claves por cadena si la app asume custodia, recuperación y respaldo; la autenticación, el login y la biometría no se reemplazan y siguen a cargo de la app
