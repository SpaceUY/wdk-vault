---
type: system
status: shipped
package: '@tetherto/wdk-worklet-bundler'
source:
  - wdk-docs/content/docs/tools/worklet-bundler/index.mdx
  - wdk-docs/content/docs/tools/worklet-bundler/configuration.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-worklet-bundler

CLI que empaqueta los módulos de wallet y de protocolo elegidos en un bundle Bare que corre fuera del hilo de la UI, con transporte HRPC o JSON-RPC. Genera los puntos de entrada, los tipos y el import estable `./.wdk` que consume el host.

## Structural
- depends on → [[pear-wrk-wdk]] because los puntos de entrada que genera importan esa capa
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` volver opcional la conversión ESM a CJS
