---
type: system
status: shipped
package: '@tetherto/wdk-wallet-aptos'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-aptos/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/index.mdx
---
# wdk-wallet-aptos

Módulo de Aptos con derivación SLIP-0010 Ed25519, saldos de APT y de fungible assets, transferencias y cotización de fees por simulación. Opera sobre la API REST del nodo vía `fetch`, sin el SDK de Aptos en runtime, lo que lo hace compatible con Bare.

## Structural
- depends on → [[wdk-wallet]] because se integra mediante las interfaces de wallet compartidas
