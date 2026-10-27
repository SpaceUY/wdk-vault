---
type: system
status: draft
source:
  - wdk-docs/content/docs/sdk/community-modules/wdk-wallet-rgb/index.mdx
---
# wdk-wallet-rgb

Módulo comunitario (`@utexo/wdk-wallet-rgb`) para activos RGB on-chain sobre Bitcoin, que envuelve `@utexo/rgb-sdk` detrás de las clases de manager y cuenta de WDK. Guarda estado local de RGB en un `dataDir` persistente, y la seed recrea las claves pero no ese estado.

## Structural
- depends on → [[wdk-wallet]] because envuelve el SDK de RGB detrás de las clases de manager y cuenta de WDK

## Associative
- opens a question about → [[Pérdida de fondos por seed sin backup]] because la doc aclara que la seed no reemplaza el respaldo del estado RGB local, algo que este modelo de pérdida no cubre
