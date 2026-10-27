---
type: system
status: draft
source:
  - https://github.com/tetherto/wdk-core-swift
---
# wdk-core-swift

Paquete Swift (`WdkSwiftCore`) con una API `async/await` para iOS y macOS que corre el WDK de JavaScript en un worklet Bare sobre BareKit y le habla por JSON-RPC. El worklet y los xcframeworks de los addons nativos no vienen incluidos: hay que generarlos con `wdk-worklet-bundler`, porque su README declara que ya no hay artefactos precompilados vigentes. Se agrega por SPM y no se instala desde npm, y la documentación del WDK todavía no lo cubre. Entrega a la app la entropía cifrada y su clave de cifrado; su README no describe dónde se guardan en el dispositivo.

## Structural
- depends on → [[wdk]] because su README la presenta como paquete Swift del WDK y su API ejecuta cualquier método del WDK (`callMethod`)
- requires → [[wdk-worklet-bundler]] because el worklet y los addons nativos se generan con ese CLI y el README no ofrece otra vía soportada

## Associative
- contrasts with → [[wdk-react-native-core]] because es el camino de integración móvil sin React Native, con la misma arquitectura de worklet Bare
