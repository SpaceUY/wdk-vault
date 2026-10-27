---
type: system
status: draft
package: 'github:UTEXO-Protocol/wdk-rgb-lightning'
source:
  - wdk-docs/content/docs/sdk/community-modules/wdk-rgb-lightning/index.mdx
---
# wdk-rgb-lightning

Módulo comunitario (`@utexo/wdk-rgb-lightning`) que corre un nodo LDK con `rgb-lib` detrás de la interfaz de manager y cuenta de WDK, para canales, pagos BOLT11 y transferencias RGB. Deriva una identidad distinta a la de la wallet RGB on-chain y exige un `dataDir` propio.

## Structural
- depends on → [[wdk-wallet]] because se expone mediante la interfaz de manager y cuenta de WDK

## Associative
- contrasts with → [[wdk-wallet-rgb]] because ambos manejan RGB pero son wallets separadas, con identidades y bases de datos distintas
