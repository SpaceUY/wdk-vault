---
type: system
status: draft
source:
  - wdk-docs/content/docs/sdk/community-modules/wdk-wallet-cosmos/index.mdx
---
# wdk-wallet-cosmos

Módulo comunitario (`@base58-io/wdk-wallet-cosmos`) que deriva cuentas Bech32 y opera en cadenas Cosmos mediante las interfaces de wallet de WDK, con envíos bank e IBC. Su manager acepta solo mnemónico o bytes de seed, y la doc advierte límites de la beta, como que `transferMaxFee` se verifica recién después del broadcast.

## Structural
- depends on → [[wdk-wallet]] because se expone mediante las interfaces de wallet de WDK
- requires → [[Seed derivada en el dispositivo]] because el manager no admite signers nombrados ni externos
