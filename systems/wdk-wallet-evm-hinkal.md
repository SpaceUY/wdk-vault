---
type: system
status: shipped
package: '@hinkal/wdk-wallet-evm-hinkal'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-hinkal/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-hinkal/api-reference.mdx
---
# wdk-wallet-evm-hinkal

Módulo comunitario, mantenido por Hinkal y no por Tether, que agrega envíos privados a cuentas EVM: deposita fondos y programa un retiro posterior al destinatario. Solo admite cuentas derivadas de una seed, no signers por clave privada, de hardware ni nombrados, y requiere configurar el bundling para Node.

## Structural
- depends on → [[wdk-wallet-evm]] because su manager extiende `WalletManagerEvm`
- requires → [[Seed derivada en el dispositivo]] because la creación de cuentas solo acepta seed y no signers externos
