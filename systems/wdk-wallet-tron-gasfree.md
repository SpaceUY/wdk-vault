---
type: system
status: shipped
package: '@tetherto/wdk-wallet-tron-gasfree'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron-gasfree/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron-gasfree/configuration.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron-gasfree/guides/handle-errors.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron-gasfree/api-reference.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron-gasfree/guides/send-transactions.mdx
---
# wdk-wallet-tron-gasfree

Módulo de TRON que hace transferencias TRC20 sin que el usuario gestione gas o recursos de TRON, a través de un servicio GasFree. Los envíos nativos de TRX no están soportados: para eso se usa el módulo base de TRON. El fee se paga en unidades del token, y puede incluir un cargo de activación si la cuenta GasFree todavía no está activa.

## Structural
- depends on → [[wdk-wallet-tron]] because su manager extiende `WalletManagerTron`
- requires → [[Gasless requiere paymaster configurado]] because `gasFreeProvider`, la URL del servicio GasFree que cubre el fee, es un parámetro obligatorio
- causes → [[Cargo de activación de la cuenta GasFree]] because cuando la cuenta GasFree está inactiva, la cotización y la transferencia suman el cargo de activación, que se cobra en el token
- mitigates → [[Usuario con USD₮ y sin token nativo no puede transferir]] because las transferencias TRC20 pasan por el servicio GasFree y no exigen TRX al usuario, siempre que el proveedor esté configurado
