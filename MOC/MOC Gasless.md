---
type: moc
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/which-wallet-module.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm-erc-4337/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-ton-gasless/index.mdx
---
# MOC Gasless

Mapa de las transacciones sin token nativo con el WDK. Parte de la falla [[Usuario con USD₮ y sin token nativo no puede transferir]], sigue por las variantes de cada cadena que la mitigan y llega a [[Paymaster]] a través de [[Gasless requiere paymaster configurado]]. Las diferencias entre betas de cada módulo están en [[MOC Versiones]], y la base de wallets en [[MOC Billetera self-custodial]].

## Variantes gasless por cadena
- [[wdk-wallet-evm-erc-4337]]
- [[wdk-wallet-evm-7702-gasless]]
- [[wdk-wallet-ton-gasless]]
- [[wdk-wallet-tron-gasfree]]
- [[wdk-wallet-solana-gasless]]

## Conceptos
- [[Paymaster]]
- [[Bundler ERC-4337]]
- [[Modos de pago de gas en ERC-4337]]
- [[Delegación EIP-7702]]

## Restricción y fallas
- [[Gasless requiere paymaster configurado]]
- [[Usuario con USD₮ y sin token nativo no puede transferir]]
- [[Cuenta sin saldo del token para repagar al paymaster]]
- [[Breaking change entre betas]]

## Servicios de mercado que estos módulos pueden reemplazar
- [[Infraestructura AA de terceros]]

## No modelado
Quedaron afuera las guías de cada módulo, las opciones de configuración (reintentos, failover de providers, headers, `onChainIdentifier`), los carriles de nonce paralelos, la firma de `UserOperation` sin envío y la selección de EntryPoint v0.8 o v0.9. Tampoco se modelan los proveedores concretos que la doc usa como ejemplo (Candide, Pimlico, Openfort, Kora, GasFree.io), el uso de estos módulos desde los módulos de protocolo (swap, bridge, lending) ni la compatibilidad de providers ethers con esos protocolos.
