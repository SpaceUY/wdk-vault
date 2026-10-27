---
type: system
status: draft
source:
  - https://github.com/tetherto/wdk-starter-kotlin
---
# wdk-starter-kotlin

App Android de ejemplo en Jetpack Compose que integra `wdk-core-kotlin`: crea o importa una wallet, muestra saldos de Ethereum (Sepolia) y Bitcoin (testnet), envía transacciones y firma mensajes. Su propio README advierte que no es una wallet endurecida: guarda juntas la clave de cifrado y la seed cifrada en `SharedPreferences`, y recomienda `EncryptedSharedPreferences` con Android Keystore para producción. La documentación del WDK todavía no la cubre.

## Structural
- depends on → [[wdk-core-kotlin]] because la referencia como módulo Gradle local, según su README
- evidences → [[Fuga de seed por almacenamiento inseguro]] because su README admite que guarda la clave de cifrado junto a la seed cifrada, sin respaldo por hardware, y que el backup de Android podría incluir ambas
