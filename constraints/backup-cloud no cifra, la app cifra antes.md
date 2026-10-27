---
type: constraint
status: shipped
source:
  - wdk-docs/content/docs/tools/backup-cloud/index.mdx
  - wdk-docs/content/docs/tools/backup-cloud/usage.mdx
---
# backup-cloud no cifra, la app cifra antes

`@tetherto/wdk-backup-cloud` sube a Google Drive o CloudKit exactamente el string que recibe y no cifra, descifra ni valida nada. La app tiene que entregarle solo texto cifrado autenticado, nunca una seed, una clave privada ni una contraseña. Un respaldo que sube la seed en claro deja de ser un respaldo y se convierte en una fuga.

## Structural
- mitigates → [[Fuga de seed por almacenamiento inseguro]] because al exigir texto cifrado de origen, el proveedor de nube no recibe la seed en claro, aunque el respaldo sigue exponiendo identificadores, tiempos y accesos
