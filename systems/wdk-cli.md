---
type: system
status: shipped
package: '@tetherto/wdk-cli'
source:
  - wdk-docs/content/docs/cli/index.mdx
---
# wdk-cli

CLI local (`@tetherto/wdk-cli`) que instala los binarios `wdk`, `wdk-daemon` y `wdk-mcp` para gestionar wallets con nombre, derivar direcciones, leer saldos, firmar mensajes, enviar activos y buscar rutas de swap y bridge. El CLI y su servidor MCP integrado comparten el mismo almacén local de wallets y el mismo daemon. Hay que instalar el paquete con scope: el `wdk-cli` sin scope no es este CLI.

## Structural
- depends on → [[wdk-wallet]] because la doc declara sus módulos de wallet integrados como dependencias normales del paquete
