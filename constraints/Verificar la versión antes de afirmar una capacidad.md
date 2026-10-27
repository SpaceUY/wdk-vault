---
type: constraint
status: shipped
source:
  - wdk-vault/_meta/versions.py
  - wdk-vault/CLAUDE.md
---
# Verificar la versión antes de afirmar una capacidad

Antes de decir que un módulo puede hacer algo, hay que comparar la versión instalada en el repo con la documentada y revisar los cambios del rango en `_meta/versions.md`. Si el rango toca la capacidad, o hay duda, se confirma la API clonando el tag de la versión instalada en el scratchpad. Que la documentación describa algo nunca alcanza como evidencia de que funciona en la versión de SpaceUY.

## Structural
- prevents → [[Usar una API documentada que mi versión no tiene]]
- mitigates → [[Breaking change entre betas]]
