# Informe de auditoría WDK: <proyecto>

- **Proyecto:** <nombre del proyecto y repositorio>
- **Commit auditado:** <sha del proyecto, de `git rev-parse HEAD`>
- **Fecha:** <YYYY-MM-DD>
- **Versión del vault:** <commit de `wdk-docs` en `_meta/last-sync.md`>, analizado el <YYYY-MM-DD de `analyzed_on`>
- **Auditor:** <nombre>

Procedimiento seguido: `auditoria/PROCEDIMIENTO.md`. Los upstream de Tether son privados: el vault no puede saber si existe una release más nueva que la integrada en `origin/main` de SpaceUY.

## Resumen

<Una a tres oraciones: cuántos servicios se encontraron, cuántos son reemplazables y cuál es el mayor bloqueo.>

## Servicios encontrados

| Servicio actual | Evidencia (archivo:línea) | Módulo WDK | Versión doc / npm | Veredicto | Esfuerzo | Riesgos |
| --- | --- | --- | --- | --- | --- | --- |
| <servicio> | <ruta:línea> | <módulo candidato, o —> | <documentada> / <npm latest>; instalada en el cliente: <versión o —> | Reemplazable / Reemplazable con condiciones / No reemplazable hoy / Sin equivalente WDK | S / M / L | <riesgos y supuestos del esfuerzo> |

Veredictos permitidos, sin variantes: `Reemplazable`, `Reemplazable con condiciones`, `No reemplazable hoy`, `Sin equivalente WDK`.

## Condiciones

Una entrada por cada fila `Reemplazable con condiciones`:

- **<servicio> → <módulo>:** <condición concreta (tercero que sigue haciendo falta, infraestructura a operar, custodia a asumir, subida de versión, madurez)>. Evidencia: <nota del vault o `_meta/versions.md`>. Capacidades verificadas con el procedimiento «¿Puedo hacer X con mi versión?» de `CLAUDE.md`: <capacidad, resultado «sí / no / sí con cambios»>.

## No reemplazable

Una entrada por cada fila `No reemplazable hoy` o `Sin equivalente WDK`:

- **<servicio o capacidad>:** <veredicto>. Motivo: <por qué>. Qué tendría que cambiar: <versión, módulo o decisión del cliente; o «nada: queda fuera del WDK»>.

## Orden de migración

1. <Paso: qué se migra, de qué depende, esfuerzo>. Condición de salida: <qué se verifica antes de seguir>.
2. <Paso>. Condición de salida: <...>.
