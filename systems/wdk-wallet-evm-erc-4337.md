---
type: system
status: shipped
package: '@tetherto/wdk-wallet-evm-erc-4337'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/configuration.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-wallet-evm-erc-4337

Módulo de smart accounts ERC-4337 (Safe) para EVM: envía `UserOperation` a un bundler y puede pagar el fee en un token vía paymaster, con patrocinio o con el token nativo. Es la variante gasless EVM que mueve la cuenta a una dirección de smart account distinta de la EOA. Requiere configurar `bundlerUrl` y, según el modo, los datos del paymaster.

## Structural
- depends on → [[wdk-wallet-evm]] because la doc declara que el módulo depende del paquete EVM, del que reutiliza derivación y firma
- requires → [[Bundler ERC-4337]] because `bundlerUrl` es un parámetro obligatorio para procesar transacciones
- requires → [[Gasless requiere paymaster configurado]] because los modos Paymaster Token y Sponsorship Policy exigen `paymasterUrl`
- mitigates → [[Usuario con USD₮ y sin token nativo no puede transferir]] because en los modos Paymaster Token y Sponsorship Policy la cuenta no necesita token nativo, pero el modo Native Coins no lo evita
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` la aceptación de providers ethers y el traslado de los overrides de gas a las opciones, en la beta.21
- can replace → [[Infraestructura AA de terceros]] because puede asumir el rol del SDK de smart accounts del lado cliente, pero la app debe seguir aportando un `bundlerUrl` y, según el modo, un `paymasterUrl` de un proveedor externo

## Associative
- opens a question about → [[Modos de pago de gas en ERC-4337]] because la doc describe tres modos pero indica que solo debe estar activo uno, sin explicar qué ocurre con una combinación
