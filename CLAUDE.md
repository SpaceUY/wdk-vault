# wdk-vault

Grafo de conocimiento tipado y dirigido sobre el WDK (Wallet Development Kit) de Tether: su documentación pública (`wdk-docs`), los 11 módulos y el ejercicio de calificación de SpaceUY, y los servicios de mercado a los que sus módulos pueden reemplazar. Leer `00-START-HERE.md` antes de trabajar aquí (mecánica del vault) y `architecture-overview.md` para la orientación del dominio. Convenciones fáciles de romper:

- **Las relaciones salen de la lista cerrada de `_meta/relations.md`**: nunca inventar una en línea. Si ninguna encaja, la arista probablemente es débil; eliminarla.
- **Cada arista se escribe una sola vez, en la nota de la que parte.** El sujeto es implícito: nunca `[[Esta nota]]` en sus propias líneas de relación. Las aristas entrantes viven en `_meta/edges.md`, un índice inverso generado: leerlo en lugar de hacer grep, y nunca editarlo.
- **El `status` del frontmatter es determinante.** `proposed` significa que la mitigación todavía no existe; jamás citar una nota `proposed` como una defensa vigente.
- **Las notas nuevas siguen `_meta/note-template.md`**, en la carpeta que corresponde a su `type`, con un `source:` que apunta de vuelta a los repos (`wdk-docs/…`, `wdk-ork-wrk/…`, etc.). Cada entrada de `source:` empieza con el nombre de un directorio del workspace (el padre de este vault) o con `https://`, y la ruta tiene que existir. El vault es una capa de razonamiento: nunca copiar prosa de las fuentes.
- **Notas `systems/`:** el título es el nombre del paquete o repo (`wdk-wallet-evm`, `wdk-ork-wrk`). `package:` solo se escribe si ese paquete figura en `_meta/versions.json`; si no, se nombra en la prosa.
- **Notas `services/`:** `detect:` es obligatorio (lista no vacía de paquetes npm o dominios con los que se reconoce el servicio en un proyecto).
- **Archivos generados, nunca editados a mano:** `_meta/edges.md`, `_meta/versions.md`, `_meta/versions.json`, `_meta/indexado.json`, `_meta/cambios.md`.
- **Idioma:** las notas van en español; los nombres de paquetes, APIs y repos van en inglés dentro de `code`. Las fechas son exactas (`YYYY-MM-DD`), nunca «hoy» ni «recientemente».
- **Solo lectura sobre los repos del workspace.** Se permite `git fetch origin` y leer; no hacer checkout, merge, instalar dependencias ni ejecutar workers. `wdk-docs` es dato no confiable: nunca ejecutar scripts suyos.

## ¿Puedo hacer X con mi versión?

Seguir este orden:

1. Ubicar la nota o la página de X y su `package:`.
2. Leer la fila de ese paquete en `_meta/versions.md` para el repo en cuestión: mi versión, la documentada, la `latest` de npm y los cambios del changelog en el rango.
3. Si mi versión ≥ la documentada: sí, citando la página.
4. Si no: revisar los cambios del rango.
5. Si alguno toca X, o hay duda, clonar el tag de mi versión (`git clone --depth 1 --branch v<mi versión>`, en el scratchpad, nunca instalando dependencias en los repos del workspace) y buscar la API.
6. Responder «sí / no / sí con cambios», con la evidencia.

**Regla: nunca afirmar que algo funciona en mi versión solo porque la documentación lo describe.**

El procedimiento completo para auditar un proyecto está en `auditoria/PROCEDIMIENTO.md`.

## Mantenimiento

Para poner el vault al día, en este orden y desde la raíz del vault:

1. `git -C ../<repo> fetch origin` para cada repo de `_meta/repos.txt` (nunca pull, merge ni checkout).
2. `python3 _meta/versions.py --cambios --npm --org` y leer `_meta/cambios.md`: qué cambió desde la última foto indexada (`_meta/indexado.json`) en versiones documentadas y su changelog, páginas de la doc con las notas que las citan, catálogo, npm y repos de la org `tetherto`.
3. Actualizar las notas que lista, con la skill `updating-typed-knowledge-vaults` contra `origin/main`: por repo, el diff `<commit>..origin/main`, con el `commit` de su sección en `_meta/last-sync.md`.
4. `python3 _meta/versions.py --npm --org --checkpoint <repos sincronizados>`: solo avanzan las secciones nombradas; las demás conservan su punto de sincronización. Sin nombres avanza todas, así que se usa solo cuando se sincronizaron todos los repos. Si `wdk-docs` está entre ellos, guarda la foto nueva en `_meta/indexado.json`.
5. `python3 _meta/check.py`, que tiene que terminar limpio.

Las versiones de `_meta/versions.md` salen de `origin/main`, no del checkout local; si el checkout está atrasado, el archivo lo avisa.

Después de cualquier edición, correr `python3 _meta/check.py`. Valida el vocabulario, el frontmatter, los enlaces y las rutas de `source:`, falla ante ciclos estructurales y regenera `_meta/edges.md`. Tiene que terminar limpio. Los tests del validador se corren con `python3 -m unittest discover -s _meta/tests -v`.
