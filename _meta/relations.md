# Vocabulario de relaciones

Esta lista es cerrada. Es la barrera que mantiene el grafo tipado: un vocabulario
abierto es la forma en que un grafo dirigido degenera otra vez en «related to».

Agregar una relación es una edición deliberada de este archivo, no algo que se hace
de paso mientras se escribe una nota. Si una arista no puede nombrarse con esta lista,
probablemente sea débil, y eso es motivo para eliminarla, no para inventar un nombre.

`_meta/check.py` lee las tablas de abajo. Una relación que no figure aquí hace fallar
el chequeo. Los nombres de las relaciones se mantienen en inglés.

## Formato de línea

    - <relation> → [[Target]]
    - <relation> → [[Target]] because <reason>

El sujeto es la propia nota y nunca se repite como wikilink. Cada arista se escribe una
sola vez, en la nota de la que parte. Las aristas entrantes se leen en el panel de
backlinks, o en `_meta/edges.md` cuando se lee el vault como archivos planos.

## Structural

Dirigida y acíclica. Es la capa que Claude recorre cuando tiene que explicar,
diagnosticar o defender algo.

| Relation | Cuándo usarla |
| --- | --- |
| `requires` | El destino tiene que cumplirse para que el sujeto sea seguro o posible. |
| `depends on` | El sujeto no puede funcionar sin el destino. |
| `causes` | El sujeto produce el destino. Del mecanismo al resultado. |
| `enables` | El sujeto hace posible el destino sin forzarlo. |
| `forbids` | El sujeto descarta el destino. Restricción frente a antipatrón. |
| `mitigates` | El sujeto reduce la probabilidad o el alcance del daño del destino. |
| `prevents` | El sujeto elimina el destino por completo. Más fuerte que `mitigates`. |
| `evidences` | El sujeto es un dato observado que respalda la afirmación del destino. |
| `constrains` | El sujeto delimita cómo puede diseñarse u operarse el destino. |
| `establishes` | Una decisión crea la restricción destino. Solo en notas de decisión. |
| `supersedes` | El sujeto reemplaza al destino. Típico entre ADRs. |
| `is part of` | Composición. |
| `is a case of` | Instancia específica del patrón general del destino. |
| `can replace` | El módulo WDK sujeto puede asumir el rol del servicio de mercado destino en un proyecto. |

## Associative

Puede formar ciclos. Sirve para descubrir y explicar por analogía, nunca para
diagnosticar. Debe mantenerse escasa: una arista asociativa igual tiene que responder
«¿por qué estas dos ideas deberían dialogar?».

| Relation | Cuándo usarla |
| --- | --- |
| `resembles` | Misma forma en un dominio distinto. |
| `contrasts with` | Diferencia instructiva, incluida una alternativa descartada. |
| `is a metaphor for` | Útil para explicarle el destino a alguien que recién llega. |
| `opens a question about` | El sujeto plantea una pregunta sin resolver sobre el destino. |
