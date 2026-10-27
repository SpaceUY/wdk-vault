---
type: system
status: shipped
package: '@tetherto/wdk-protocol-bridge-usdt0-evm'
source:
  - wdk-docs/content/docs/sdk/bridge-modules/bridge-usdt0-evm/index.mdx
  - wdk-docs/content/docs/sdk/bridge-modules/bridge-usdt0-evm/configuration.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/index.mdx
---
# bridge-usdt0-evm

Módulo de Tether (`@tetherto/wdk-protocol-bridge-usdt0-evm`) que mueve USD₮0 y XAU₮0 entre redes EVM y hacia Solana, TON y TRON mediante LayerZero, desde cuentas EVM de WDK. `getSupportedChains()` y `getSupportedTokens()` leen configuración estática y no prueban una ruta concreta: esa se confirma con `quoteBridge()`. Al igual que Velora, ciertas versiones no inicializan con cuentas derivadas de managers con provider ethers compartido.

## Structural
- depends on → [[wdk-wallet-evm]] because la doc declara que mueve los tokens desde cuentas EVM de WDK y exige soporte de transacciones EVM
- can replace → [[Agregadores de swap y bridge directos]] because puede asumir el rol de un SDK de bridge, pero solo cubre USD₮0 y XAU₮0 sobre LayerZero y no rutas arbitrarias de otros tokens

## Associative
- contrasts with → [[swidge-lifi]] because la doc separa el bridge standalone de USD₮0 de los proveedores swidge, que sirven rutas de un servicio externo de ruteo
