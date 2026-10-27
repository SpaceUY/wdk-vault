---
type: system
status: shipped
package: '@tetherto/wdk-backup-cloud'
source:
  - wdk-docs/content/docs/tools/backup-cloud/index.mdx
  - wdk-docs/content/docs/tools/backup-cloud/usage.mdx
  - wdk-docs/content/docs/tools/backup-cloud/configuration.mdx
  - wdk-docs/content/docs/tools/backup-cloud/guides/migrate-from-react-native.mdx
---
# wdk-backup-cloud

Fachada con dos proveedores (Google Drive `appDataFolder` y CloudKit) para guardar una clave maestra de wallet que la app ya cifró. Mantiene un único respaldo por proveedor, no guarda versiones y verifica solo que el ítem exista, no que descifre a la wallet esperada.

## Structural
- requires → [[backup-cloud no cifra, la app cifra antes]] because sube el string tal cual, sin cifrar ni validar nada
- mitigates → [[Pérdida de fondos por seed sin backup]] because permite recuperar la wallet entre dispositivos a partir de un respaldo cifrado
- supersedes → [[wdk-backup-cloud-react-native]] because la guía de migración lo presenta como reemplazo del paquete legado, con CloudKit en lugar de iCloud Drive y migración por usuario en el cliente
