---
type: moc
status: shipped
source:
  - wdk-docs/content/docs/sdk/wallet-modules/index.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/which-wallet-module.mdx
  - wdk-docs/content/docs/overview/vision.mdx
---
# MOC Billetera self-custodial

Mapa de la espina de la billetera autocustodial construida con el SDK del WDK. Empezar por [[Seed derivada en el dispositivo]], que explica de dónde salen las claves, seguir por la restricción [[La seed nunca sale del dispositivo]] (establecida por [[Diseñar el WDK como autocustodial sin custodio intermediario]]) y por sus consecuencias: las fallas [[Pérdida de fondos por seed sin backup]] y [[Fuga de seed por almacenamiento inseguro]] y la regla [[backup-cloud no cifra, la app cifra antes]]. Las versiones de cada paquete están en `_meta/versions.md`, y las diferencias entre betas en [[MOC Versiones]].

## Núcleo del SDK
- [[wdk]]
- [[wdk-wallet]]

## Wallets por cadena
- [[wdk-wallet-evm]]
- [[wdk-wallet-btc]]
- [[wdk-wallet-solana]]
- [[wdk-wallet-ton]]
- [[wdk-wallet-tron]]
- [[wdk-wallet-spark]]
- [[wdk-wallet-aptos]]

## Multisig y privacidad
- [[wdk-wallet-multisig-safe]]
- [[wdk-wallet-multisig-squads]]
- [[wdk-wallet-evm-hinkal]]
- [[wdk-wallet-evm-bermuda]]

## Módulos comunitarios
- [[wdk-wallet-cosmos]]
- [[wdk-wallet-rgb]]
- [[wdk-rgb-lightning]]

## Herramientas
- [[wdk-secret-manager]]
- [[wdk-react-native-core]]
- [[wdk-react-native-secure-storage]]
- [[wdk-backup-cloud]]
- [[wdk-worklet-bundler]]
- [[pear-wrk-wdk]]
- [[wdk-utils]]
- [[wdk-failover-provider]]
- [[wdk-asset-registry]]
- [[wdk-uikit-react-native]]

## Restricciones, fallas y decisión
- [[La seed nunca sale del dispositivo]]
- [[backup-cloud no cifra, la app cifra antes]]
- [[Pérdida de fondos por seed sin backup]]
- [[Fuga de seed por almacenamiento inseguro]]
- [[Diseñar el WDK como autocustodial sin custodio intermediario]]

## Servicios de mercado que estos módulos pueden reemplazar
- [[Custodia tercerizada (MPC)]]
- [[Wallets embebidas WaaS]]

## No modelado
Las wallets con abstracción de cuentas y gasless están en [[MOC Gasless]], el indexer y el backend de billeteras en [[MOC Backend e indexado]], y los módulos de protocolo (swap, bridge, lending, fiat, swidge, SDA), los precios, el CLI y el MCP toolkit en [[MOC Protocolos]] y [[MOC Catálogo WDK]]. Quedaron afuera las guías por módulo y los starters. Tampoco se modelan las opciones de configuración de cada wallet, las firmas externas (`ISigner`) en detalle ni las políticas y middleware del núcleo, y no se evalúa la seguridad de los módulos comunitarios.
