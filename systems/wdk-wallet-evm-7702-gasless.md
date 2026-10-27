---
type: system
status: shipped
package: '@tetherto/wdk-wallet-evm-7702-gasless'
source:
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-7702-gasless/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-7702-gasless/configuration.mdx
  - wdk-docs/content/docs/overview/changelog.mdx
---
# wdk-wallet-evm-7702-gasless

Módulo EVM que combina delegación EIP-7702 con `UserOperation` ERC-4337: el usuario conserva su dirección EOA y las transacciones pasan por un bundler y un paymaster. Admite el modo patrocinado o el pago del fee en un token. Exige verificar el `delegationAddress`, porque la EOA delega su ejecución en ese contrato.

## Structural
- depends on → [[wdk-wallet-evm]] because la doc declara su dependencia del paquete EVM, cuya instancia exacta hay que usar para envolver una cuenta existente
- depends on → [[Delegación EIP-7702]] because la cuenta delega su ejecución en el `delegationAddress` configurado
- requires → [[Bundler ERC-4337]] because necesita la URL de un bundler ERC-4337
- requires → [[Gasless requiere paymaster configurado]] because necesita un endpoint de paymaster, y una política de patrocinio o un token de pago
- mitigates → [[Usuario con USD₮ y sin token nativo no puede transferir]] because con patrocinio o con `paymasterToken` el usuario no paga con token nativo, siempre que el paymaster esté configurado
- causes → [[Breaking change entre betas]] because el changelog marca como `[Breaking]` la beta.7, que acepta providers ethers y comparte el cliente RPC del manager
- can replace → [[Infraestructura AA de terceros]] because puede asumir el rol del SDK de smart accounts del lado cliente, pero la app debe seguir aportando un bundler, un paymaster y un `delegationAddress` verificado

## Associative
- contrasts with → [[wdk-wallet-evm-erc-4337]] because mantiene la dirección EOA del usuario, mientras que el módulo ERC-4337 opera desde una smart account Safe
