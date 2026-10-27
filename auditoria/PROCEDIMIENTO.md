# Procedimiento de auditoría: ¿puede un servicio actual reemplazarse con WDK?

Objetivo: dado el proyecto de un cliente, decidir qué servicios de mercado que ya usa pueden reemplazarse con módulos del WDK, bajo qué condiciones y en qué orden migrar. El resultado es un informe a partir de `plantilla-informe.md`. Contexto del dominio: [[architecture-overview]]; mapa de todo el vault: [[MOC WDK]].

Reglas que valen en todos los pasos:

- El vault es de solo lectura sobre el proyecto auditado: no instalar dependencias, no ejecutar su código, no modificar nada. Todos los comandos son de lectura.
- Los upstream de Tether son privados: el vault no sabe si existe una release más nueva que la integrada en `origin/main` de SpaceUY (ver `_meta/last-sync.md`). Cualquier afirmación sobre versiones vale hasta esa fecha.
- Las columnas «mi versión» de `_meta/versions.md` describen los repos de SpaceUY, no el proyecto del cliente. La versión instalada del cliente sale de su propio lockfile (paso 1).
- Antes de empezar, mirar `analyzed_on` en `_meta/last-sync.md`. Si el vault está viejo, actualizarlo antes de auditar (skill `updating-typed-knowledge-vaults`).

Los comandos usan sintaxis POSIX (`detect_pattern() {…}`, `$(…)`, bucles `for … do`): correr en bash o zsh (no en fish).

Variables usadas abajo (ajustar la ruta):

```sh
VAULT=/ruta/al/wdk-vault      # raíz de este vault
# todos los comandos del paso 1 se corren desde la raíz del proyecto auditado
```

## Paso 1. Detectar qué servicios usa el proyecto

Desde la raíz del proyecto auditado.

**1a. Dependencias declaradas y resueltas.** Lista las dependencias de cada `package.json` (incluye monorepos) y los lockfiles presentes:

```sh
find . -name package.json -not -path '*/node_modules/*' -exec sh -c 'echo "== $1"; jq -r "((.dependencies // null) + (.devDependencies // null)) | select(. != null) | to_entries[] | \"\(.key)@\(.value)\"" "$1"' _ {} \;
ls pnpm-lock.yaml package-lock.json yarn.lock bun.lockb 2>/dev/null
```

Versiones resueltas de los paquetes WDK, si ya usa alguno (sirven en el paso 3):

```sh
grep -n '@tetherto/' pnpm-lock.yaml package-lock.json yarn.lock 2>/dev/null | head -50
```

Nota: el filtro de `jq` evita `{}` a propósito, porque `find` lo sustituye por la ruta del archivo dentro del filtro y `jq` falla.

**1b. Construir el patrón de cada servicio a partir de su `detect:`.** Cada nota de `$VAULT/services/` tiene un bloque `detect:` con paquetes npm o dominios. Este one-liner lo lee, quita las comillas YAML, escapa los puntos y une las entradas con `|`:

```sh
detect_pattern() { awk '/^detect:/{f=1;next} /^[A-Za-z_]+:/{f=0} f&&/^  - /{sub(/^  - /,""); gsub(/^'\''|'\''$/,""); gsub(/\./,"\\."); print}' "$1" | paste -sd'|' -; }
detect_pattern "$VAULT/services/Wallets embebidas WaaS.md"
# @privy-io/react-auth|@privy-io/expo|magic-sdk|@web3auth/modal|@dynamic-labs/sdk-react-core|@privy-io/|@magic-ext/|@web3auth/|@dynamic-labs/
```

Si el patrón se arma a mano, cada entrada de `detect:` va tal cual, con `.` escapado (`api\.0x\.org`) y separadas por `|`. Una entrada que termina en `/` (`@privy-io/`) es un prefijo: coincide con cualquier paquete de ese scope. Los servicios actuales son siete: `Custodia tercerizada (MPC)`, `Wallets embebidas WaaS`, `Infraestructura AA de terceros`, `Indexadores y nodos de terceros`, `Agregadores de swap y bridge directos`, `On-ramp integrado a mano` y `Feeds de precio de terceros`; el listado real es el contenido de `$VAULT/services/`.

**1c. Buscar en el código.** Primero qué archivos coinciden, por servicio:

```sh
for s in "$VAULT"/services/*.md; do
  p=$(detect_pattern "$s"); echo "### $(basename "$s" .md)"
  grep -rIl --exclude-dir=node_modules --exclude-dir=.git -E "$p" .
done
```

Y para anotar la evidencia como `archivo:línea` en el informe:

```sh
grep -rIn --exclude-dir=node_modules --exclude-dir=.git -E "$(detect_pattern "$VAULT/services/Indexadores y nodos de terceros.md")" .
```

Agregar `--exclude-dir=dist --exclude-dir=build --exclude-dir=.next` si el proyecto genera artefactos que ensucian el resultado.

**Advertencia: una coincidencia de `detect:` es evidencia a inspeccionar, no prueba de uso.** Abrir cada hit y confirmar que el código realmente llama al servicio. Casos que producen falsos positivos:

- Enlaces de explorador: `tronscan` o `etherscan` que solo arman una URL para que el usuario vea una transacción no son una dependencia de indexado.
- Palabras comunes: `permissionless` o `moralis` aparecen en prosa, comentarios y READMEs.
- Lockfiles y dependencias transitivas: figurar en un lockfile no significa que el código lo use directamente.
- Documentación, tests y mocks.

Lo contrario también vale: **no encontrar nada no prueba que el servicio no se use** (clientes HTTP con otro dominio, URLs en variables de entorno o en infra, un backend en otro repositorio). Revisar también `.env.example`, la configuración de despliegue y preguntar al cliente por los servicios que contrata.

**1d. Qué usa el proyecto del servicio.** Por cada servicio confirmado, listar qué APIs o funciones usa realmente (por ejemplo, de Alchemy: solo saldos e historial, o también NFT, webhooks o APIs enriquecidas). Cada función sin equivalente en los módulos del paso 2 se registra como fila aparte con veredicto `Sin equivalente WDK`; no se descarta.

Salida del paso: lista de servicios confirmados, cada uno con su evidencia `archivo:línea` y las funciones que usa.

## Paso 2. Candidatos WDK por servicio

Para cada servicio confirmado, leer qué módulos pueden asumir su rol. Las entradas `can replace` están en el índice inverso, con la condición después de `because`:

```sh
grep -F 'can replace → Wallets embebidas WaaS' "$VAULT/_meta/edges.md"
```

(Reemplazar por el título exacto de la nota de servicio.) Cada línea es `<módulo> — can replace → <servicio> because <condiciones>`: ese módulo es un candidato y las condiciones son el primer borrador de «Condiciones» del informe. Abrir la nota `systems/<módulo>.md` del candidato y la del servicio, que dice qué sigue necesitando la app aunque migre (por ejemplo, la clave o el proveedor externo).

Si un servicio confirmado no tiene ninguna entrada `can replace`, o el proyecto usa una capacidad que ningún candidato cubre (autenticación y login, por ejemplo, que las notas indican que WDK no reemplaza), esa fila termina en el paso 4 como `Sin equivalente WDK`.

## Paso 3. Recorrer las aristas hasta los failures y leer la madurez

Por cada candidato:

1. **Aristas estructurales.** Leer su sección `## Structural` y seguir las relaciones `requires`, `depends on` y `constrains` hacia cada destino, y de ahí en adelante, hasta llegar a los `failures` (son sumideros: ahí termina el recorrido). Cada nota alcanzada es un requisito o riesgo del reemplazo.

   ```sh
   sed -n '/^## Structural/,/^## Associative/p' "$VAULT/systems/wdk-wallet-evm-erc-4337.md"
   ```

   Los `failures` que apuntan al candidato (`causes`) o que el candidato mitiga se leen en `$VAULT/_meta/edges.md`, bajo el título de la falla.

2. **Versión y madurez.** Buscar el paquete en la sección «Catálogo: todos los paquetes documentados» de `$VAULT/_meta/versions.md`, que da la versión documentada y la `latest` de npm:

   ```sh
   grep -F '| @tetherto/wdk-wallet-evm-erc-4337 |' "$VAULT/_meta/versions.md"
   ```

   Ese comando devuelve también filas de las tablas por repo, que describen solo los repos de SpaceUY: ignorarlas. Para el proyecto auditado, «mi versión» es la del lockfile del cliente (paso 1a), y se compara con la fila del catálogo (sección «Catálogo: todos los paquetes documentados»): la de 5 columnas, sin repo, con paquete, versión documentada, `latest` de npm, estado y quién lo usa. Si el estado dice «documentada no publicada en npm», la versión documentada no se puede instalar desde npm; `no publicado (404)` en la columna de npm significa que el paquete no existe en npm.

   Madurez: una versión con `-beta.N` es beta, con `-rc.N` es release candidate, sin sufijo es estable. Una nota con `status: draft` (no se instala desde npm o su madurez no está clara) tiene madurez no verificada. Comparar la versión del lockfile del cliente con la documentada y la `latest` de la fila del catálogo.

3. **Capacidades de las que depende la migración.** Para cada capacidad concreta que el cliente necesita (por ejemplo, «pasar un `Provider` de ethers existente a `WalletManagerEvm`»), correr el procedimiento «¿Puedo hacer X con mi versión?» de `CLAUDE.md`, con la versión del cliente. La regla es la de ese procedimiento: nunca afirmar que algo funciona en una versión solo porque la doc lo describe. Si el rango entre la versión instalada y la documentada tiene cambios (`[Breaking]` incluidos, listados en `_meta/versions.md`), se verifica la API clonando el tag de esa versión en un directorio temporal, sin instalar dependencias en el proyecto. Ese procedimiento también cubre los cambios entre la versión documentada y la `latest` de npm: `_meta/versions.md` lista entradas del changelog solo hasta la documentada, así que para lo posterior hay que leer las releases de GitHub del paquete.

4. **Chequeos específicos del tipo de servicio.**
   - Custodia de claves ([[Custodia tercerizada (MPC)]], [[Wallets embebidas WaaS]]): cómo migran las claves de los usuarios existentes (exportar e importar) es una pregunta abierta que se resuelve con el proveedor. Sin esa respuesta el veredicto no puede ser mejor que `Reemplazable con condiciones`. Ver también [[Seed derivada en el dispositivo]].
   - Indexado ([[Indexadores y nodos de terceros]]): confirmar cadenas y tokens contra `GET /api/v1/chains` de la [[Indexer API]], o contra los indexers autoalojados (`wdk-indexer-wrk-*`), antes de dar el veredicto.
   - Toda función detectada en 1d sin equivalente: `Sin equivalente WDK`.

Salida del paso: por candidato, la lista de condiciones, riesgos, versión del cliente frente a la documentada y a npm, y madurez.

## Paso 4. Veredicto y esfuerzo

Asignar a cada fila uno de estos veredictos (escala fija, sin variantes):

| Veredicto | Cuándo |
| --- | --- |
| `Reemplazable` | Un módulo cubre el rol, las condiciones del paso 3 ya se cumplen o no existen, y la capacidad está verificada en la versión que se usaría. |
| `Reemplazable con condiciones` | Un módulo cubre el rol, pero el reemplazo exige algo que hoy no está: un tercero que siga contratándose (bundler, paymaster, API key, proveedor RPC), operar infraestructura propia, asumir custodia y respaldo, subir de versión o aceptar madurez beta. Cada condición se lista. |
| `No reemplazable hoy` | Existe módulo, pero algo lo bloquea: la capacidad falta o no se pudo verificar en una versión usable, la cadena o el token no están soportados, o el módulo es `draft` y el caso exige producción. Se indica qué tendría que cambiar. |
| `Sin equivalente WDK` | Ningún módulo del vault asume ese rol (no hay `can replace`, o la capacidad queda fuera, como la autenticación). |

Una capacidad «no verificada» no es un veredicto: queda como condición abierta y, si bloquea el reemplazo, la fila es `No reemplazable hoy`.

Esfuerzo, con este criterio:

- **S**: cambio acotado de dependencia y configuración, sin infraestructura ni datos nuevos.
- **M**: reescritura de la integración o subida de versión con cambios `[Breaking]`, o un tercero nuevo por configurar.
- **L**: operar infraestructura propia (por ejemplo, el stack de backend e indexado), o trasladar custodia, respaldo y recuperación a la app, o migrar usuarios existentes.

El esfuerzo es una estimación gruesa de este procedimiento, no un dato del vault; anotar el supuesto en «Riesgos».

## Paso 5. Orden de migración

Ordenar solo las filas `Reemplazable` y `Reemplazable con condiciones`. Criterios, en este orden de prioridad:

1. Primero lo que no toca claves ni fondos y se puede revertir con un flag (precios, lectura de saldos e historial).
2. Antes de un módulo, sus dependencias: la wallet base antes de su variante gasless, el proveedor de terceros que seguirá haciendo falta antes del módulo que lo usa.
3. Las condiciones que son subir de versión van antes del reemplazo que las necesita.
4. Último, lo que traslada custodia a la app (custodia tercerizada, wallets embebidas), porque exige plan de migración de seeds y de respaldo.

Cada paso lleva una condición de salida verificable (qué se prueba antes de seguir).

## Paso 6. Guardar el informe

Copiar la plantilla y completarla. El informe es confidencial del cliente: va en `auditoria/informes/`, que `.gitignore` excluye, y nunca se commitea en el vault compartido.

```sh
mkdir -p "$VAULT/auditoria/informes"
cp "$VAULT/auditoria/plantilla-informe.md" "$VAULT/auditoria/informes/<proyecto>-<YYYY-MM-DD>.md"
```

Datos de cabecera: el commit auditado sale de `git rev-parse HEAD` en el proyecto; la versión del vault es el commit de `wdk-docs` en `last-sync.md`:

```sh
awk '/^## wdk-docs/{f=1} f&&/^commit:/{print $2; exit}' "$VAULT/_meta/last-sync.md"
```

El informe cita solo lo que el vault respalda, con evidencia `archivo:línea` del proyecto en cada fila, y repite la limitación de los upstream privados en «Riesgos» cuando una conclusión dependa de versiones.
