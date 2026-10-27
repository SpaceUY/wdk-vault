---
type: system
status: shipped
package: '@candidelabs/wdk-protocol-sda-candide'
source:
  - wdk-docs/content/docs/sdk/sda-modules/sda-candide/index.mdx
  - wdk-docs/content/docs/sdk/sda-modules/index.mdx
---
# sda-candide

Módulo comunitario (`@candidelabs/wdk-protocol-sda-candide`) que implementa `ISdaProtocol` con las Forwarding Addresses de Candide: una dirección EVM determinística recibe depósitos y los reenvía al destinatario. Derivar una dirección no activa su monitoreo; `createDepositAddress()` lo activa con un `expiry` que hay que renovar. Las direcciones delegan en un beacon actualizable que administra Candide, así que el uso implica confiar en el proveedor.

## Structural
- depends on → [[wdk-wallet]] because la doc declara como peer el paquete base de wallets de WDK

## Associative
- contrasts with → [[sda-rhinofi]] because Candide usa un contrato determinístico con retiro del destinatario, mientras Rhino.fi opera de confianza las direcciones y barre los fondos
