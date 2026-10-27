---
type: failure
status: shipped
source:
  - wdk-docs/content/docs/tools/backup-cloud/index.mdx
  - wdk-docs/content/docs/tools/react-native-secure-storage/index.mdx
  - wdk-docs/content/docs/sdk/core-module/guides/error-handling.mdx
---
# Fuga de seed por almacenamiento inseguro

Guardar la seed o la clave de cifrado sin protección (en claro, en logs, en un respaldo en la nube sin cifrar o en un string que no se puede borrar de memoria) la expone a cualquiera que acceda a ese almacenamiento. Quien obtiene la seed controla todos los fondos de todas las cadenas derivadas de ella. Las herramientas del WDK separan el cifrado, el almacenamiento local y el respaldo para que ninguna pieza reciba la seed en claro.
