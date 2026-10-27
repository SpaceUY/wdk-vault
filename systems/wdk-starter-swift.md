---
type: system
status: draft
source:
  - https://github.com/tetherto/wdk-starter-swift
---
# wdk-starter-swift

App iOS de ejemplo que integra `WdkSwiftCore` de punta a punta: crea o importa una wallet, deriva direcciones, consulta saldos y libera los recursos. Usa XcodeGen y el bundler del WDK para generar el worklet y los addons, de modo que no depende del IDE de Xcode. La documentación del WDK todavía no la cubre.

## Structural
- depends on → [[wdk-core-swift]] because es el paquete Swift que integra, según su README
