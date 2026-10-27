---
type: moc
status: shipped
source:
  - wdk-docs/content/docs/index.mdx
  - wdk-vault/_meta/versions.py
---
# MOC WDK

Mapa raíz del vault sobre el WDK de Tether. Para la orientación del dominio, empezar por [[architecture-overview]]; para la mecánica del vault y las preguntas de prueba, por [[00-START-HERE]]. Desde acá se llega a cada espina y a las herramientas para auditar un proyecto y responder «¿puedo hacer X con mi versión?».

## Mapas por tema
- [[MOC Billetera self-custodial]]
- [[MOC Gasless]]
- [[MOC Backend e indexado]]
- [[MOC Protocolos]]
- [[MOC Catálogo WDK]]
- [[MOC Versiones]]

## Versiones y sincronización
- [[_meta/versions]]
- [[_meta/last-sync]]

## Auditoría
- [[auditoria/PROCEDIMIENTO]]
- [[auditoria/plantilla-informe]]

## Servicios de mercado que el WDK puede reemplazar
- [[Custodia tercerizada (MPC)]]
- [[Wallets embebidas WaaS]]
- [[Infraestructura AA de terceros]]
- [[Indexadores y nodos de terceros]]
- [[Agregadores de swap y bridge directos]]
- [[On-ramp integrado a mano]]
- [[Feeds de precio de terceros]]

## Convenciones del vault
- [[CLAUDE]]

## No modelado
Este mapa no audita ningún proyecto concreto: el procedimiento y la plantilla son el método, y cada informe se guarda aparte en `auditoria/`. Quedan fuera los servicios de mercado que no figuran en `services/`, los upstream privados de Tether (no se puede saber qué publicó después de la release integrada en SpaceUY) y todo lo que cada MOC temático declara como no modelado en su propia sección.
