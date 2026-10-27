---
type: system
status: draft
package: '@semanticio/wdk-wallet-evm-x402-facilitator'
source:
  - wdk-docs/content/docs/ai/x402.mdx
  - wdk-docs/content/docs/ai/agent-skills.mdx
---
# wdk-wallet-evm-x402-facilitator

Módulo comunitario en beta, mantenido por Semantic Pay (paquete `@semanticio/wdk-wallet-evm-x402-facilitator`), pensado para adaptar una cuenta EVM de WDK al signer de facilitator de x402 y verificar y liquidar pagos dentro del propio proceso. Su versión publicada depende de una versión anterior del módulo EVM y de x402, y la doc no recomienda combinarla con las versiones de sus ejemplos sin confirmación del mantenedor. Tether no lo audita ni lo respalda.

## Structural
- depends on → [[wdk-wallet-evm]] because la doc declara que el paquete publicado depende del módulo EVM de WDK
