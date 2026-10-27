---
type: system
status: shipped
package: '@tetherto/wdk-react-native-secure-storage'
source:
  - wdk-docs/content/docs/tools/react-native-secure-storage/index.mdx
  - wdk-docs/content/docs/tools/react-native-secure-storage/configuration.mdx
---
# wdk-react-native-secure-storage

Wrapper tipado sobre `react-native-keychain` que guarda la seed y la entropía cifradas junto con la clave de cifrado, con acceso biométrico opcional por wallet. No genera seeds ni cifra texto plano ni hace respaldo en la nube: eso queda en la app.

## Structural
- mitigates → [[Fuga de seed por almacenamiento inseguro]] because mantiene el material de la wallet cifrado en el keychain del dispositivo
