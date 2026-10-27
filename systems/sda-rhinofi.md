---
type: system
status: shipped
package: '@rhino.fi/wdk-protocol-sda-rhinofi'
source:
  - wdk-docs/content/docs/sdk/sda-modules/sda-rhinofi/index.mdx
  - wdk-docs/content/docs/sdk/sda-modules/index.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# sda-rhinofi

Módulo comunitario (`@rhino.fi/wdk-protocol-sda-rhinofi`) que descubre rutas, emite Smart Deposit Addresses y estima y rastrea depósitos por Rhino.fi, sin firmar ni difundir la transacción del usuario. Rhino.fi opera las direcciones y controla el barrido y la liquidación, un modelo de operador de confianza, y las direcciones no se derivan localmente. Los métodos heredados `deriveDepositAddress()` y `renewDepositAddress()` no están soportados.

## Structural
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` cambios del manejo de errores y de la dirección de destino de las direcciones emitidas

## Associative
- opens a question about → [[Diseñar el WDK como autocustodial sin custodio intermediario]] because los depósitos pasan por direcciones que el proveedor emite y barre, un modelo de custodia que esa decisión no contempla
