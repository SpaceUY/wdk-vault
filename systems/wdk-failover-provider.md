---
type: system
status: shipped
package: '@tetherto/wdk-failover-provider'
source:
  - wdk-docs/content/docs/tools/failover-provider/index.mdx
---
# wdk-failover-provider

Wrapper genérico que agrupa varios providers detrás de un proxy y reintenta contra el siguiente candidato cuando una llamada falla, de forma síncrona o asíncrona. Un predicado `shouldRetryOn` limita el failover a errores transitorios y no reenvía escrituras ni enumeración de propiedades.
