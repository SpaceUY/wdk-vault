---
type: moc
status: shipped
source:
  - wdk-docs/content/docs/sdk/swap-modules/index.mdx
  - wdk-docs/content/docs/sdk/bridge-modules/index.mdx
  - wdk-docs/content/docs/sdk/swidge-modules/index.mdx
  - wdk-docs/content/docs/sdk/fiat-modules/index.mdx
  - wdk-docs/content/docs/sdk/lending-modules/index.mdx
  - wdk-docs/content/docs/sdk/sda-modules/index.mdx
  - wdk-docs/content/docs/sdk/pricing-modules/index.mdx
---
# MOC Protocolos

Mapa de los módulos de protocolo del WDK, los que operan sobre una cuenta de wallet para mover o valorar activos: swaps, bridges, rutas swidge, fiat, lending, depósitos y precios. Cada módulo indica de qué wallet depende y, cuando corresponde, qué servicio de mercado puede reemplazar y con qué condiciones. Los paquetes y versiones de todo el catálogo están en `_meta/versions.md`, y la vista por área en [[MOC Catálogo WDK]].

## Swap y bridge standalone
- [[swap-velora-evm]]
- [[bridge-usdt0-evm]]

## Swidge (swap, bridge o ambos, por proveedor)
- [[swidge-0x]]
- [[swidge-butter]]
- [[swidge-lifi]]
- [[swidge-moonpay-trade]]
- [[swidge-orchestra]]
- [[swidge-rhinofi]]
- [[swidge-symbiosis]]

## Fiat
- [[fiat-moonpay]]
- [[fiat-transak]]

## Lending
- [[lending-aave-evm]]
- [[lending-morpho-evm]]

## Smart Deposit Address
- [[sda-candide]]
- [[sda-rhinofi]]

## Precios
- [[wdk-pricing-provider]]
- [[pricing-coingecko-http]]
- [[pricing-bitfinex-http]]

## Servicios de mercado que estos módulos pueden reemplazar
- [[Agregadores de swap y bridge directos]]
- [[On-ramp integrado a mano]]
- [[Feeds de precio de terceros]]

## Falla relacionada
- [[Breaking change entre betas]]

## No modelado
Quedaron afuera las guías, la configuración y la referencia de API de cada módulo, las tablas de cadenas y tokens soportados, los límites de fee y de slippage, y la comparación entre proveedores de una misma categoría. Tampoco se modelan los proveedores como servicios individuales (LI.FI, 0x, MoonPay, Transak, Rhino.fi, Candide, Symbiosis, Butter, Flashnet, Morpho, Aave, Velora, LayerZero), la seguridad de los módulos comunitarios, ni las incompatibilidades puntuales de provider entre ciertas versiones de las wallets EVM y los adaptadores de swap, bridge y lending, que se verifican contra `_meta/versions.md`.
