---
type: system
status: draft
source:
  - https://github.com/tetherto/wdk-core-kotlin
---
# wdk-core-kotlin

Biblioteca Android (`WdkCore`) con una API de corrutinas Kotlin que corre el WDK de JavaScript en un worklet Bare sobre BareKit y le habla por JSON-RPC. Su build de Gradle genera el bundle del worklet a partir de `js/wdk.config.js` y descarga el runtime de BareKit. Su README presenta la publicación en Maven Central como plan; por ahora se incluye como módulo Gradle local. La documentación del WDK todavía no la cubre, y el README no describe dónde se guardan la entropía cifrada ni su clave en el dispositivo.

## Structural
- depends on → [[wdk]] because el `package.json` de su carpeta `js/` declara `@tetherto/wdk` como dependencia del worklet
- depends on → [[pear-wrk-wdk]] because esa capa es el runtime del worklet y atiende los mensajes JSON-RPC de `WdkCore`
- requires → [[wdk-worklet-bundler]] because el build de Gradle lo invoca para producir el bundle y enlazar los addons nativos

## Associative
- contrasts with → [[wdk-react-native-core]] because es el camino de integración móvil sin React Native, con la misma arquitectura de worklet Bare
