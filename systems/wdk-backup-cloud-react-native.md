---
type: system
status: superseded
package: '@tetherto/wdk-backup-cloud-react-native'
source:
  - wdk-docs/content/docs/tools/backup-cloud/guides/migrate-from-react-native.mdx
  - wdk-qualification-exercise/apps/rn-wdk-exercise/package.json
---
# wdk-backup-cloud-react-native

Paquete anterior de respaldo en la nube para React Native, con `GoogleDriveProvider` y un `ICloudProvider` que usa un archivo de iCloud Drive. La guía de migración de la documentación lo reemplaza por `@tetherto/wdk-backup-cloud`, que usa CloudKit en lugar de iCloud Drive: el SDK nuevo no puede leer ese archivo y la migración se corre en el cliente, por usuario. `wdk-qualification-exercise` todavía lo declara; las versiones están en `_meta/versions.md`.
