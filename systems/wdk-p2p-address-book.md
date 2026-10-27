---
type: system
status: shipped
package: '@tetherto/wdk-p2p-address-book'
source:
  - wdk-docs/content/docs/tools/p2p-address-book/index.mdx
---
# wdk-p2p-address-book

Libreta de contactos cifrada y replicada entre los dispositivos de un mismo usuario por redes peer-to-peer de Holepunch (`@tetherto/wdk-p2p-address-book`), con `AddressBook.fromSeed()` como flujo recomendado. Es sincronización entre dispositivos del mismo usuario, no un directorio público ni un modo de compartir contactos. Guarda destinos pero no valida sintaxis ni prueba propiedad de la dirección.

## Structural
- requires → [[Seed derivada en el dispositivo]] because `fromSeed()` toma los bytes de la seed de la wallet y un namespace para que cada dispositivo derive el mismo libro

## Associative
- contrasts with → [[wdk-utils]] because la libreta guarda destinos sin validarlos, y la doc remite a `wdk-utils` para los validadores y parsers
