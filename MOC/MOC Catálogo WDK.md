---
type: moc
status: shipped
source:
  - wdk-docs/content/docs/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/index.mdx
  - wdk-docs/content/docs/ai/mcp-toolkit/index.mdx
  - wdk-docs/content/docs/ai/agent-skills.mdx
  - wdk-docs/content/docs/cli/index.mdx
  - wdk-docs/content/docs/ui-kits/react-native-ui-kit/index.mdx
---
# MOC Catálogo WDK

Catálogo de todo módulo del WDK que la documentación describe, agrupado por área. Cada entrada enlaza a su nota `system` con una frase. Para saber el paquete exacto y su versión documentada, la `latest` de npm y si un repo local lo usa, ver `_meta/versions.md` (sección «Catálogo: todos los paquetes documentados»): incluye también los módulos que ningún repo del workspace instala. Las diferencias entre betas están en [[MOC Versiones]].

## Núcleo y wallets por cadena
- [[wdk]]: orquestador que registra módulos de wallet y de protocolo
- [[wdk-wallet]]: interfaces base que implementan todos los módulos de wallet
- [[wdk-wallet-evm]]: cuentas EVM estándar, con gas en el token nativo
- [[wdk-wallet-btc]]: Bitcoin en capa base
- [[wdk-wallet-solana]]: Solana, SOL y tokens SPL
- [[wdk-wallet-ton]]: TON, Jettons y firmas Ed25519
- [[wdk-wallet-tron]]: TRON, TRX y TRC20
- [[wdk-wallet-spark]]: Spark, capa 2 de Bitcoin con Lightning
- [[wdk-wallet-aptos]]: Aptos, APT y fungible assets

## Wallets gasless
- [[wdk-wallet-evm-erc-4337]]: smart accounts con bundler y paymaster
- [[wdk-wallet-evm-7702-gasless]]: EOA con delegación EIP-7702 y UserOperation
- [[wdk-wallet-ton-gasless]]: Jettons con fee en un Jetton de paymaster
- [[wdk-wallet-tron-gasfree]]: TRC20 vía servicio GasFree
- [[wdk-wallet-solana-gasless]]: Solana con paymaster compatible con Kora

## Multisig, privacidad y módulos comunitarios de wallet
- [[wdk-wallet-multisig-safe]]: cuentas Safe con umbral de owners
- [[wdk-wallet-multisig-squads]]: bóvedas Squads en Solana
- [[wdk-wallet-evm-hinkal]]: envíos privados en EVM
- [[wdk-wallet-evm-bermuda]]: cuentas blindadas de Bermuda en EVM
- [[wdk-wallet-cosmos]]: cadenas Cosmos, comunitario
- [[wdk-wallet-rgb]]: activos RGB sobre Bitcoin, comunitario
- [[wdk-rgb-lightning]]: nodo Lightning con RGB, comunitario

## Protocolos de swap y bridge
- [[swap-velora-evm]]: swaps EVM por Velora
- [[bridge-usdt0-evm]]: bridge de USD₮0 y XAU₮0 por LayerZero
- [[swidge-0x]]: swaps en una cadena por 0x
- [[swidge-butter]]: rutas por Butter Network
- [[swidge-lifi]]: swap, bridge y rutas combinadas por LI.FI
- [[swidge-moonpay-trade]]: swaps y transferencias por MoonPay Trade
- [[swidge-orchestra]]: rutas de BTC y stablecoins por Flashnet Orchestra
- [[swidge-rhinofi]]: swaps y bridges por Rhino.fi
- [[swidge-symbiosis]]: rutas por Symbiosis

## Protocolos de fiat, lending y depósitos
- [[fiat-moonpay]]: on-ramp y off-ramp con widget de MoonPay
- [[fiat-transak]]: on-ramp y off-ramp con widget de Transak, comunitario
- [[lending-aave-evm]]: Aave V3 desde cuentas EVM
- [[lending-morpho-evm]]: vaults y mercados de Morpho, comunitario
- [[sda-candide]]: direcciones de depósito determinísticas de Candide
- [[sda-rhinofi]]: direcciones de depósito emitidas por Rhino.fi

## Precios
- [[wdk-pricing-provider]]: caché y failover sobre clientes de precio
- [[pricing-coingecko-http]]: cliente de precios de CoinGecko
- [[pricing-bitfinex-http]]: cliente de precios de Bitfinex

## Herramientas
- [[wdk-secret-manager]]: seed cifrada en memoria con passkey
- [[wdk-utils]]: validadores, parsers y Shamir
- [[wdk-failover-provider]]: reintento contra el siguiente provider
- [[wdk-asset-registry]]: metadatos estandarizados de activos
- [[wdk-p2p-address-book]]: contactos cifrados entre dispositivos
- [[wdk-backup-cloud]]: respaldo de la clave maestra en la nube
- [[wdk-react-native-core]]: hooks de wallet para React Native
- [[wdk-react-native-secure-storage]]: keychain para seed cifrada
- [[wdk-worklet-bundler]]: bundles Bare para workers
- [[pear-wrk-wdk]]: transporte HRPC y JSON-RPC para worklets
- [[create-wdk-module]]: scaffolding de módulos nuevos

## IA, pagos y CLI
- [[wdk-mcp-toolkit]]: servidores MCP con wallets del WDK
- [[Agent Skills WDK]]: instrucciones `SKILL.md` para agentes
- [[x402]]: pagos HTTP con USD₮0
- [[wdk-wallet-evm-x402-facilitator]]: facilitator x402 autoalojado, comunitario
- [[wdk-cli]]: CLI local, daemon y servidor MCP

## UI
- [[wdk-uikit-react-native]]: componentes React Native para wallets

## Backend e indexado
- [[Indexer API]]: API REST hospedada de saldos y transferencias
- [[wdk-indexer-http]]: cliente de la Indexer API
- [[wdk-app-node]]: gateway HTTP del backend de billeteras
- [[wdk-ork-wrk]]: directorio de shards y orquestación
- [[wdk-data-shard-wrk]]: persistencia y lectura por shard
- [[wdk-indexer-processor-wrk]]: enrutador de transferencias a shards
- [[wdk-indexer-wrk-base]]: base de los indexers por cadena
- [[wdk-indexer-wrk-btc]]: indexer de Bitcoin
- [[wdk-indexer-wrk-evm]]: indexer de EVM
- [[wdk-indexer-wrk-solana]]: indexer de Solana
- [[wdk-indexer-wrk-spark]]: indexer de Spark
- [[wdk-indexer-wrk-ton]]: indexer de TON
- [[wdk-indexer-wrk-tron]]: indexer de TRON

## Casos
- [[wdk-qualification-exercise]]: caso de SpaceUY que consume el stack

## Mapas por tema
- [[MOC Billetera self-custodial]]
- [[MOC Gasless]]
- [[MOC Protocolos]]
- [[MOC Backend e indexado]]
- [[MOC Versiones]]

## No modelado
Los paquetes `@tetherto/wdk-core` y `@tetherto/wdk-core-react-native` solo aparecen en entradas históricas del changelog y no tienen nota. Tampoco `@tetherto/wdk-backup-cloud-react-native` (se cita solo en una guía de migración), los kits `@tetherto/wdk-safe-protocol-kit` y `@tetherto/wdk-safe-relay-kit`, los paquetes `@tetherto/docs-seo-*` ni las dependencias internas del backend (`hp-svc-facs-*`, `svc-facs-*`, `tether-wrk-base`), que figuran en `_meta/versions.md` pero no son módulos documentados del SDK. La página de OpenClaw se cubre dentro de [[Agent Skills WDK]]. No se modelan las guías por módulo ni la referencia de API, y el contenido del CLI más allá de su página de entrada (comandos, seguridad y formato de almacenamiento) queda sin detalle.
