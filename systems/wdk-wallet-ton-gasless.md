---
type: system
status: shipped
package: '@tetherto/wdk-wallet-ton-gasless'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-ton-gasless/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-ton-gasless/configuration.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-wallet-ton-gasless

Módulo de TON que transfiere Jettons sin que el usuario tenga TON: el fee se paga en un Jetton de paymaster, validado contra la configuración del servicio TON API. Solo cubre transferencias de Jettons; el envío nativo, la cotización nativa y la firma de transacciones no están soportados.

## Structural
- depends on → [[wdk-wallet-ton]] because hereda de ese módulo la derivación por defecto y las firmas de mensajes con separación de dominio
- requires → [[Gasless requiere paymaster configurado]] because `paymasterToken` es obligatorio y `tonApiClient` se usa para construir y retransmitir las transferencias gasless
- mitigates → [[Usuario con USD₮ y sin token nativo no puede transferir]] because las transferencias de Jettons no requieren que el usuario tenga TON, pero el Jetton de fee debe figurar en la configuración del servicio gasless
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` la beta.13, con firmas de mensajes con separación de dominio incompatibles con las anteriores
