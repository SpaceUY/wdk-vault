---
type: moc
status: shipped
source:
  - wdk-vault/_meta/versions.py
  - wdk-docs/content/docs/overview/changelog.mdx
---
# MOC Versiones

Mapa de lo que hay que saber para responder «¿puedo hacer X con mi versión?». Empezar por [[Versión documentada vs versión instalada]], que explica por qué las tres versiones difieren, y seguir por la regla [[Verificar la versión antes de afirmar una capacidad]], que se fundamenta en la decisión [[Usar la release integrada en SpaceUY como versión desplegada]].

Fallas que la regla evita:
- [[Usar una API documentada que mi versión no tiene]]
- [[Breaking change entre betas]]

Los números concretos viven en `_meta/versions.md` (versión instalada, documentada y `latest` de npm por paquete y repo) y el commit analizado de cada fuente, en `_meta/last-sync.md`. Ambos se regeneran con `python3 _meta/versions.py --npm --checkpoint`.

## No modelado
Las notas de este MOC no registran el historial completo del changelog ni las versiones de dependencias transitivas. Tampoco se sabe qué publicó Tether después de la última release integrada en SpaceUY, porque sus repos son privados.
