---
type: system
status: shipped
package: '@tetherto/wdk-wallet-tron'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-tron/api-reference.mdx
---
# wdk-wallet-tron

Módulo estándar de TRON para cuentas donde el usuario cubre los fees y recursos de la red con TRX. Soporta saldos TRX y TRC20, transacciones arbitrarias (llamadas a contratos o TronWeb prearmadas) y listas ordenadas de providers con failover.

## Structural
- depends on → [[wdk-wallet]] because su manager extiende `WalletManager` del paquete base
