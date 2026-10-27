# Empezar aquí

Este vault reúne el conocimiento transversal del WDK de Tether como un **grafo tipado y dirigido**. Es una capa de razonamiento, no una segunda copia de la documentación: `wdk-docs` y los repos del workspace siguen siendo la fuente de verdad, y cada nota apunta al archivo del que salió.

Empezar por el MOC raíz (TODO: se enlaza cuando exista, en una tarea posterior).

## Cómo leer una nota

Cada nota expone una afirmación en pocas oraciones y luego lista sus aristas bajo `## Structural` (la capa que se recorre para diagnosticar) y `## Associative` (la capa que se recorre para explicar o explorar).

Tres convenciones que conviene conocer antes de agregar nada:

1. **Las relaciones salen de `_meta/relations.md` y de ningún otro lugar.**
2. **Cada arista se escribe una sola vez, en la nota de la que parte.** Aristas entrantes: panel de backlinks, o `_meta/edges.md` si se leen los archivos planos.
3. **El `status` del frontmatter es determinante.** `proposed` significa que la mitigación todavía no existe.

Correr `python3 _meta/check.py` después de editar.

## Probar

Hacer estas preguntas con el vault como único contexto: cada una debe volver como una cadena causal que termina en un conjunto ordenado de acciones, no como una lista de temas relacionados.

1. TODO: pregunta sobre la espina causal más importante (se define en la Task 8).
2. TODO: pregunta que parte de una falla con nombre y camina hacia atrás (se define en la Task 8).
3. TODO: pregunta sobre una restricción y lo que obliga a hacer (se define en la Task 8).

Una respuesta vaga es una señal sobre el grafo, no sobre el modelo: la espina está poco tipada y la solución son mejores aristas, no más notas.

## Qué hay aquí

TODO: se completa al cerrar el vault. Gran parte del dominio queda deliberadamente sin modelar; el alcance se declara al final del MOC raíz.
