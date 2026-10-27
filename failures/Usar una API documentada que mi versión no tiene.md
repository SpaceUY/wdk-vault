---
type: failure
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm/index.mdx
  - wdk-vault/_meta/versions.py
---
# Usar una API documentada que mi versión no tiene

Se escribe código o se promete una capacidad a partir de la doc actual, pero el repo instala una versión anterior que no la incluye. Caso concreto: la doc de `@tetherto/wdk-wallet-evm` describe overrides de gas en transferencias ERC-20 desde `1.0.0-beta.20`, mientras `wdk-indexer-wrk-evm` instala `1.0.0-beta.11`. El resultado es una llamada que falla en tiempo de ejecución o una respuesta falsa al cliente.
