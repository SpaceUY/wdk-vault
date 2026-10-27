# Empezar aquí

Este vault reúne el conocimiento transversal del WDK de Tether como un **grafo tipado y dirigido**. Es una capa de razonamiento, no una segunda copia de la documentación: `wdk-docs` y los repos del workspace siguen siendo la fuente de verdad, y cada nota apunta al archivo del que salió.

Empezar por el MOC raíz, [[MOC WDK]], y seguir con [[architecture-overview]] para la orientación del dominio.

Para qué sirve: (1) auditar el proyecto de un cliente y decidir qué servicios actuales puede reemplazar un módulo WDK, con el procedimiento de `auditoria/PROCEDIMIENTO.md`; (2) responder «¿puedo hacer X con mi versión?» con el procedimiento de `CLAUDE.md`, que manda sobre cualquier lectura de la doc: nunca afirmar que algo funciona en una versión solo porque la documentación lo describe.

## Cómo leer una nota

Cada nota expone una afirmación en pocas oraciones y luego lista sus aristas bajo `## Structural` (la capa que se recorre para diagnosticar) y `## Associative` (la capa que se recorre para explicar o explorar).

Tres convenciones que conviene conocer antes de agregar nada:

1. **Las relaciones salen de `_meta/relations.md` y de ningún otro lugar.**
2. **Cada arista se escribe una sola vez, en la nota de la que parte.** Aristas entrantes: panel de backlinks, o `_meta/edges.md` si se leen los archivos planos.
3. **El `status` del frontmatter es determinante.** `proposed` significa que la mitigación todavía no existe.

Correr `python3 _meta/check.py` después de editar.

## Probar

Hacer estas preguntas con el vault como único contexto: cada una debe volver como una cadena causal que cita notas y termina en un conjunto ordenado de acciones, no como una lista de temas relacionados.

1. «¿Puedo pasar un `Provider` de ethers ya existente a `WalletManagerEvm` en `wdk-indexer-wrk-evm` con la versión que tengo?»
2. «Un usuario tiene USD₮ en Tron y no puede transferir: ¿qué falta y en qué orden se arregla?»
3. «Un proyecto usa Privy y Alchemy: ¿qué parte reemplaza WDK y bajo qué condiciones?»

Una respuesta vaga es una señal sobre el grafo, no sobre el modelo: la espina está poco tipada y la solución son mejores aristas, no más notas.

## Qué hay aquí

Cuatro espinas modeladas en profundidad: [[MOC Billetera self-custodial]], [[MOC Gasless]], [[MOC Backend e indexado]] y [[MOC Protocolos]], más el catálogo de todos los módulos ([[MOC Catálogo WDK]]) y el control de versiones ([[MOC Versiones]]). Los siete servicios de mercado en `services/` y el procedimiento en `auditoria/` sirven para auditar proyectos. Gran parte del dominio queda deliberadamente sin modelar; el alcance se declara al final de [[MOC WDK]].
