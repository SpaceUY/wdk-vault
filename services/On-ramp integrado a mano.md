---
type: service
status: shipped
detect:
  - '@moonpay/moonpay-react'
  - '@transak/transak-sdk'
  - '@ramp-network/ramp-instant-sdk'
source:
  - wdk-docs/content/docs/sdk/fiat-modules/index.mdx
  - wdk-docs/content/docs/sdk/fiat-modules/fiat-moonpay/index.mdx
  - wdk-docs/content/docs/sdk/fiat-modules/fiat-transak/index.mdx
---
# On-ramp integrado a mano

Categoría de mercado que agrupa los widgets y SDKs de proveedores de compra y venta de cripto con fiat que una app embebe por su cuenta. MoonPay, Transak y Ramp son ejemplos de la categoría y señales de `detect:`. La doc del WDK nombra a MoonPay y a Transak como proveedores de sus módulos fiat, pero no los paquetes `@moonpay/moonpay-react` ni `@transak/transak-sdk`, y Ramp no aparece en la doc ni en los repos. Cambiar a un módulo fiat de WDK no quita al proveedor: la app sigue necesitando su cuenta, su clave y, para URLs firmadas, un backend.
