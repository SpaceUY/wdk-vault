---
type: failure
status: shipped
source:
  - wdk-app-node/CLAUDE.md
  - wdk-app-node/workers/lib/utils/cached.route.js
  - wdk-app-node/workers/lib/server.js
---
# Balance desactualizado por caché

Un cliente que consulta un balance justo después de una transferencia puede recibir el valor anterior, porque `app-node` lo sirve desde Redis hasta 30 s sin ir al ork. Pasar `cache=false` en la consulta fuerza la lectura fresca y evita además escribir esa respuesta en la caché.
