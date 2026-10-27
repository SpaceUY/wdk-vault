---
type: failure
status: shipped
source:
  - wdk-docs/content/docs/overview/changelog.mdx
  - wdk-docs/content/docs/sdk/wallet-modules/wallet-evm/index.mdx
---
# Breaking change entre betas

Los módulos del WDK están en prerelease y marcan `[Breaking]` cambios de contrato entre betas consecutivas, de modo que subir o comparar versiones no es neutro. En `@tetherto/wdk-wallet-evm`, el rango entre `1.0.0-beta.11` y `1.0.0-beta.20` incluye un cambio rompiente fechado 2026-09-30. Un código que funcionaba en una beta puede dejar de hacerlo en la siguiente sin que cambie el número mayor.
