---
type: service
status: shipped
detect:
  - '@privy-io/react-auth'
  - '@privy-io/expo'
  - magic-sdk
  - '@web3auth/modal'
  - '@dynamic-labs/sdk-react-core'
  - '@privy-io/'
  - '@magic-ext/'
  - '@web3auth/'
  - '@dynamic-labs/'
source:
  - wdk-docs/content/docs/overview/about.mdx
  - wdk-docs/content/docs/ai/agent-skills.mdx
---
# Wallets embebidas WaaS

Servicios que ofrecen wallets embebidas en una app como producto alojado, donde el proveedor gestiona la autenticación y la infraestructura de claves. Privy, Magic, Web3Auth y Dynamic son ejemplos de esta categoría de mercado y de las señales de `detect:`; la documentación del WDK solo menciona a Privy, en su comparación de wallets hospedadas frente a autocustodiales. Reemplazarlos con el WDK traslada a la app la custodia, el respaldo y la recuperación, pero no resuelve la autenticación ni el login.

## Associative
- contrasts with → [[Seed derivada en el dispositivo]] because el proveedor hospedado gestiona las claves, mientras la seed derivada las mantiene en el dispositivo
