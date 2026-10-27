---
type: concept
status: shipped
source:
  - wdk-app-node/CLAUDE.md
  - wdk-app-node/workers/lib/services/ork.js
  - wdk-qualification-exercise/infra/wdk-stack/README.md
---
# Afinidad usuario-ork por CRC32

Para un usuario autenticado, `app-node` elige siempre el mismo ork aplicando `CRC32(userId) % cantidad de orks` sobre la lista descubierta; las solicitudes sin usuario rotan por round-robin. El índice depende del tamaño actual de esa lista. Si el canal del ork elegido se cierra, las lecturas idempotentes se reintentan en el siguiente ork y las escrituras tienen un solo intento.

## Structural
- is part of → [[wdk-app-node]] because el cálculo vive en `resolveOrkRpcKey` de su servicio `ork.js`
- depends on → [[Descubrimiento de orks por hyperswarm]] because el módulo se calcula sobre los orks que el lookup devolvió
