---
type: system
status: draft
source:
  - https://github.com/tetherto/wdk-signer-local
---
# wdk-signer-local

Addon nativo de Bare que guarda mnemonics y claves privadas bajo nombre en el keychain de iOS y macOS o en el Android KeyStore con protección biométrica, y firma con derivación HD (BIP-32/BIP-39, SLIP-10 y TON). Su README indica instalarlo desde GitHub Packages y compilar el addon antes de usarlo; en npm solo existe un placeholder, y la documentación del WDK todavía no lo cubre.

## Structural
- mitigates → [[Fuga de seed por almacenamiento inseguro]] because su README describe el guardado de los secretos en el keychain o el KeyStore de la plataforma en lugar de en claro

## Associative
- resembles → [[wdk-react-native-secure-storage]] because también deja el material de la wallet en el keychain del dispositivo, aunque este addon además deriva claves y firma
