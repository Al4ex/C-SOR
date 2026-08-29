# C-SOR — Apagador inteligente

Requisitos y recomendación de compra para un apagador de pared que se controle **desde el celular**, **al tocarlo** y, si se puede, **muestre la temperatura**. Pensado para instalación residencial en México (127 V, chalupa 2x4).

## Lo que pediste

| Requisito | Prioridad | Cómo se cubre |
|-----------|-----------|----------------|
| Encender y apagar desde el celular | Obligatorio | App (eWeLink, Smart Life o Tecnolite Connect) |
| Encender y apagar tocándolo en la pared | Obligatorio | Panel táctil y/o botones físicos |
| Mostrar temperatura | Deseable | Pantalla + sensor de ambiente |
| México / San Juan | Contexto | 127 V, envío nacional, caja tipo chalupa |

Detalle completo: [docs/requisitos.md](docs/requisitos.md).  
Cómo comprarlo e instalarlo: [docs/guia-compra-instalacion.md](docs/guia-compra-instalacion.md).

## Recomendación

**Sonoff NSPanel (formato US / 120 mm)** es el que cubre las tres cosas en un solo aparato.

- App **eWeLink** (Android e iPhone): enciendes, apagas y programas desde donde estés.
- En la pared: **pantalla táctil de 3.5"** más **2 botones físicos**.
- **Sensor de temperatura** integrado: la muestra en pantalla (también clima/hora si hay WiFi).
- Controla **hasta 2 luces** (2 circuitos).
- Voltaje 100–240 V: sirve en México.
- Precio de referencia en México: **alrededor de $880–$1,500 MXN**.

Dónde buscarlo:

- [Abasteo.mx — NSPanel negro](https://www.abasteo.mx/Electrodomesticos/Smart-Home/Iluminacion-Inteligente/Interruptores-y-Atenuadores-Inteligentes/Sonoff-Interruptor-de-Luz-Inteligente-NSPANEL-2-Botones-Wi-Fi-Negro.html) (~$879 MXN + envío)
- [Mercado Libre — NSPanel 2 salidas](https://articulo.mercadolibre.com.mx/MLM-1442668955-apagador-inteligente-2-salidas-pantalla-tactil-wifi-nspanel-_JM) (envío a San Juan y resto del país)

**No confundir** con el **NSPanel Pro**: ese es un panel de control y **no sustituye** el apagador de la luz (no trae relés).

## Si no hay presupuesto para pantalla

Un apagador táctil WiFi barato (~$160–$575 MXN) + un sensor de temperatura Tuya (~$150–$300 MXN) cubre celular y toque. La temperatura se ve en el celular, no en la placa.

Marca mexicana lista para chalupa 2x4, incluso **sin cable neutro**:

- [Tecnolite Connect Creator MSN I](https://tecnolite.mx/tienda/p/apagador-inteligente-tactil-wifi-1-circuito-sin-cable-neutro-compatible-con-app-movil-y-asistentes-de-voz/TSWIM1MVBTCWSN) (~$574 MXN)

## Antes de comprar

1. Baja la pastilla y mira la caja del apagador: si hay **cable neutro** (suele ser blanco o azul), el NSPanel entra directo. Si solo hay dos cables, compra modelo **sin neutro** o pide que un electricista baje el neutro.
2. El WiFi de la casa debe tener banda **2.4 GHz** (la de 5 GHz sola no sirve).
3. Instalación eléctrica: mejor con electricista. No es un cambio de foco.

## Documentos

- [Requisitos](docs/requisitos.md)
- [Guía de compra e instalación](docs/guia-compra-instalacion.md)
- [Comparativa de productos](docs/comparativa.md)
