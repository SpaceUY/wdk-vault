---
type: service
status: shipped
detect:
  - '@privy-io/react-auth'
  - '@privy-io/expo'
  - magic-sdk
  - '@web3auth/modal'
  - '@dynamic-labs/sdk-react-core'
source:
  - wdk-docs/content/docs/overview/about.mdx
  - wdk-docs/content/docs/ai/agent-skills.mdx
---
# Wallets embebidas WaaS

Servicios que ofrecen wallets embebidas en una app como producto alojado, donde el proveedor gestiona la autenticación y la infraestructura de claves (Privy, Magic, Web3Auth, Dynamic). Se los reconoce por sus SDKs de frontend. La documentación del WDK contrasta ese modelo, que cita con Privy y con la infraestructura de wallets como servicio, frente a sus claves locales y autogestionadas.

## Associative
- contrasts with → [[Seed derivada en el dispositivo]] because el proveedor hospedado gestiona las claves, mientras la seed derivada las mantiene en el dispositivo
