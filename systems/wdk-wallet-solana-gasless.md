---
type: system
status: shipped
package: '@tetherto/wdk-wallet-solana-gasless'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-solana-gasless/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-solana-gasless/configuration.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-wallet-solana-gasless

Módulo de Solana que envuelve al módulo estándar y manda las transacciones por un paymaster compatible con Kora, que pasa a ser el fee payer. El fee se cotiza y se cobra en el token configurado como `paymasterToken`. Los tokens del paymaster tienen que estar financiados para las cuentas que necesiten transacciones patrocinadas.

## Structural
- depends on → [[wdk-wallet-solana]] because la doc lo presenta como un envoltorio del módulo estándar de Solana
- requires → [[Gasless requiere paymaster configurado]] because `paymasterUrl`, `paymasterAddress` y `paymasterToken` son obligatorios
- mitigates → [[Usuario con USD₮ y sin token nativo no puede transferir]] because el paymaster actúa como fee payer y el fee se cobra en un token SPL, no en SOL
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` la beta.5, que reemplaza `ConfigurationError` por `ValueError`
