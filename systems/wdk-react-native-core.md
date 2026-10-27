---
type: system
status: shipped
package: '@tetherto/wdk-react-native-core'
source:
  - wdk-docs/content/docs/tools/react-native-core/index.mdx
  - wdk-docs/content/docs/start-building/react-native-quickstart.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-react-native-core

Librería de hooks para apps React Native que gestiona creación, restauración, bloqueo y cambio de wallets, y corre el WDK en un worklet Bare aislado. Incluye su propio almacenamiento en keychain y deja la política de autenticación y biometría a cargo de la app.

## Structural
- depends on → [[pear-wrk-wdk]] because el worklet Bare que aloja al WDK usa esa capa de transporte
- requires → [[wdk-worklet-bundler]] because necesita el bundle del worklet que genera el bundler
- mitigates → [[Fuga de seed por almacenamiento inseguro]] because guarda las credenciales cifradas en el keychain del dispositivo
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` el paso a identidad de wallet a cargo de la app
- can replace → [[Wallets embebidas WaaS]] because cubre creación, bloqueo y desbloqueo de wallets si la app asume custodia, recuperación y respaldo; no impone autenticación ni biometría, que la app aplica antes de `unlock()`

## Associative
- contrasts with → [[wdk-react-native-secure-storage]] because incluye su propio storage con identificadores explícitos y autenticación a cargo de la app, a diferencia del paquete standalone
