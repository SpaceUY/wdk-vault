---
type: service
status: shipped
detect:
  - '@fireblocks/fireblocks-web3-provider'
  - fireblocks-sdk
  - '@bitgo/sdk-api'
source:
  - wdk-docs/content/docs/overview/about.mdx
  - wdk-docs/content/docs/ai/agent-skills.mdx
---
# Custodia tercerizada (MPC)

Servicio en el que un proveedor tercero custodia las claves o co-firma con ellas, típicamente mediante computación multipartita (MPC), y la app opera a través de su API. Los SDKs de Fireblocks y BitGo son la señal con la que se lo reconoce en un proyecto. El WDK ofrece el camino inverso: claves locales y sin dependencia de un custodio externo. Fireblocks y BitGo son ejemplos de esta categoría de mercado y de las señales de `detect:`; la documentación del WDK no los nombra.

## Associative
- contrasts with → [[Seed derivada en el dispositivo]] because la custodia tercerizada delega las claves, la seed derivada las deja en el dispositivo
