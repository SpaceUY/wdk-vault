---
type: constraint
status: shipped
source:
  - wdk-app-node/CLAUDE.md
  - wdk-app-node/workers/lib/services/ork.js
  - wdk-ork-wrk/CLAUDE.md
  - wdk-ork-wrk/workers/api.ork.wrk.js
  - wdk-data-shard-wrk/CLAUDE.md
  - wdk-indexer-processor-wrk/README.md
  - wdk-indexer-processor-wrk/workers/indexer.processor.wrk.js
  - wdk-qualification-exercise/infra/wdk-stack/docker-compose.yml
---
# Capability del handshake ork debe coincidir

`app-node`, el ork y el data shard arrancan su servidor RPC con `topicConf.capability` y la incluyen en cada llamada saliente; un par con otro valor no completa el handshake. La guía del ork recomienda revisar primero que el valor sea idéntico cuando un worker no responde. El stack del caso SpaceUY lo resuelve generando un único secreto que comparten todos los servicios.

## Structural
- constrains → [[wdk-app-node]] because su `rpcCall` envía la capability configurada en cada solicitud al ork
- constrains → [[wdk-ork-wrk]] because levanta su servidor RPC y sus llamadas a shards con la misma capability
- constrains → [[wdk-data-shard-wrk]] because exige el mismo valor para aceptar llamadas del ork y para hablar con su `proc`
- constrains → [[wdk-indexer-processor-wrk]] because arranca su servidor RPC con `topicConf.capability`, que su README incluye en la configuración común

## Associative
- opens a question about → [[Sin orks disponibles (503)]] because los repos dicen que una capability distinta impide la conexión, pero no aclaran si `app-node` lo vería como lista de orks vacía o como un error de canal
