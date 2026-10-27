---
type: concept
status: draft
source:
  - repo-name/path/to/file.md
---
# Título de la nota

Entre dos y cuatro oraciones que enuncian la afirmación: qué es y por qué importa para la cadena en la que está. No se copia ningún párrafo de la fuente: el puntero `source:` de arriba es la forma en que el lector llega al detalle.

## Structural
- causes → [[Otra nota]]
- requires → [[Una nota más]] because el motivo cabe en una línea

## Associative
- resembles → [[Una nota de otro dominio]]

<!--
type:    concept | constraint | failure | decision | system | service   (debe coincidir con la carpeta)
status:  shipped | built-off-by-default | proposed | draft | todo | superseded
source:  una o más rutas relativas al workspace, con el nombre del repo como prefijo
         (p. ej. wdk-docs/content/docs/...). El primer segmento debe ser un directorio
         del workspace o la entrada debe empezar con https://; la ruta tiene que existir.
package: opcional, solo en systems/. Nombre del paquete npm, por ejemplo '@tetherto/wdk'.
         Debe figurar en _meta/versions.json (campo "packages"); si no figura, se omite
         y el paquete se nombra en la prosa. Se aceptan comillas simples o dobles.
detect:  obligatorio en services/. Lista no vacía de paquetes npm o dominios con los que
         se reconoce ese servicio en un proyecto:
           detect:
             - '@moonpay/moonpay-js'
             - moonpay.com

Las dos secciones de relaciones son opcionales. Una nota sin sección Structural es un
sumidero: el final de una cadena. Es lo esperado en failures/ y merece una segunda
mirada en cualquier otro lado.

Las relaciones salen de _meta/relations.md y de ningún otro lugar.
El sujeto es implícito: nunca escribir [[Esta nota]] en sus propias líneas de relación.
`can replace` es estructural: va bajo ## Structural, de un módulo WDK (systems/) hacia un
servicio de mercado (services/).
-->
