---
type: system
status: shipped
source:
  - wdk-docs/content/docs/examples-and-starters/react-native-starter.mdx
  - wdk-docs/content/docs/start-building/react-native-quickstart.mdx
  - https://github.com/tetherto/wdk-starter-react-native
---
# wdk-starter-react-native

Wallet de referencia autocustodial con Expo y React Native (el paquete de la app se llama `wdk-starter-wallet`) que muestra cómo integrar el WDK mediante worklets de BareKit. La documentación y el README la marcan como alfa y advierten no usarla con fondos reales hasta que haya un release estable. Su repo incluye guías de arquitectura, seguridad y respaldo en la nube.

## Structural
- depends on → [[wdk-react-native-core]] because su `package.json` lo declara como dependencia
