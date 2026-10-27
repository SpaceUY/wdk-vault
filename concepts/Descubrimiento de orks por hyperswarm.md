---
type: concept
status: shipped
source:
  - wdk-app-node/CLAUDE.md
  - wdk-app-node/workers/base.http.server.wdk.js
  - wdk-ork-wrk/workers/api.ork.wrk.js
  - wdk-qualification-exercise/infra/wdk-stack/README.md
---
# Descubrimiento de orks por hyperswarm

Cada ork se anuncia en el topic `@wdk/ork` y `app-node` lo consulta al arrancar y cada 120 s, de modo que `app-node` no necesita la dirección de ningún ork en su configuración. Si el primer lookup vuelve vacío, `app-node` reintenta tres veces, arranca igual y queda sin orks hasta el siguiente refresco. Un lookup vacío posterior conserva la lista anterior. Los shards (`@wdk/data-shard`) y los indexers (`{chain}:{token}`) se resuelven con el mismo mecanismo, y el README del stack de SpaceUY avisa que el primer descubrimiento sobre la DHT pública puede tardar entre 10 y 60 segundos.

## Structural
- requires → [[wdk-ork-wrk]] because al menos un ork tiene que anunciarse en el topic para que haya algo que descubrir
- causes → [[Sin orks disponibles (503)]] because mientras la lista de orks esté vacía, las rutas que dependen de un ork responden 503
