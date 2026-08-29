# Guía de compra e instalación (México)

## 1. Qué comprar (caso recomendado)

**Sonoff NSPanel, formato US / 120, 2 botones.**

Lista de pedido:

1. NSPanel US (blanco o negro).
2. App **eWeLink** (gratis, Play Store / App Store).
3. Electricista si no te sientes seguro con 127 V.

Opcional: sensor de humedad extra; el NSPanel ya mide temperatura.

## 2. Dónde comprarlo

Envío a San Juan y al resto del país:

| Tienda | Notas |
|--------|--------|
| [Abasteo.mx](https://www.abasteo.mx/Electrodomesticos/Smart-Home/Iluminacion-Inteligente/Interruptores-y-Atenuadores-Inteligentes/Sonoff-Interruptor-de-Luz-Inteligente-NSPANEL-2-Botones-Wi-Fi-Negro.html) | ~$879 MXN + envío, stock de empresa |
| [Mercado Libre](https://articulo.mercadolibre.com.mx/MLM-1442668955-apagador-inteligente-2-salidas-pantalla-tactil-wifi-nspanel-_JM) | Útil para envío a domicilio y meses |
| Amazon México | Buscar `Sonoff NSPanel US` (no el Pro) |

Al pedir, confirma:

- Texto **US**, **120** o medidas ~120 × 74 mm.
- **2 gang / 2 botones / 2 salidas** si tu apagador actual tiene dos teclas.
- Que **no** diga Pro, a menos que sepas que no va a sustituir el apagador.

## 3. Revisar la caja antes de instalar

1. Baja la **pastilla** del circuito (tablero).
2. Quita la tapa y el apagador viejo.
3. Cuenta cables:

| Qué ves | Qué significa |
|---------|----------------|
| Fase + retorno (2 cables) | **No hay neutro.** NSPanel no se alimenta bien. Baja neutro o compra modelo sin neutro. |
| Fase + retorno + neutro (blanco/azul) | Listo para NSPanel. |
| 3 o 4 cables de colores raros | Puede ser **escalera** (3 vías). Dilo al electricista; no todos los smart switch sirven en escalera. |

En México el neutro a veces no es blanco. Si hay un cable que va al puente del resto de apagadores y no corta la luz, puede ser neutro; si hay duda, electricista con detector.

## 4. WiFi

- Red **2.4 GHz**. En módems Infinitum/Totalplay/Izzi suele llamarse el SSID sin “_5G”.
- Contraseña a la mano.
- El celular en 2.4 GHz mientras emparejas (desactiva 5G temporalmente si no parea).

## 5. Instalación eléctrica (resumen)

**Cortar energía. Si no tienes oficio de electricista, contrata uno.**

Conexión típica NSPanel (con neutro):

- **L** — fase (la que trae corriente, la que “prende” el tester).
- **N** — neutro.
- **L1** — retorno de la lámpara 1.
- **L2** — retorno de la lámpara 2 (si solo hay una luz, se deja sin usar o se tapa según el manual).

El aparato queda empotrado en la chalupa; la pantalla queda al ras de la pared.

Carga máxima aproximada: **600 W** en total. Focos LED de casa caben de sobra. No conectes boiler, horno ni motor.

## 6. App

1. Instala **eWeLink**.
2. Crea cuenta.
3. Enciende el NSPanel; entra en modo emparejamiento (manual: suele ser mantener un botón o desde el menú de la pantalla).
4. Agrégalo a la misma red 2.4 GHz.
5. Prueba: toque en pared, toque en app, y que la temperatura del cuarto aparezca en la pantalla.

Compartir con familia: en eWeLink, “Share device”.

Alexa / Google: vincular la skill eWeLink en la app del asistente.

## 7. Si no hay neutro

Opciones reales:

1. Electricista baja el neutro desde la caja de registro (la solución más limpia para poder poner NSPanel).
2. Compras [Tecnolite Creator sin neutro](https://tecnolite.mx/tienda/p/apagador-inteligente-tactil-wifi-1-circuito-sin-cable-neutro-compatible-con-app-movil-y-asistentes-de-voz/TSWIM1MVBTCWSN) e instalas el **capacitor** en paralelo con el foco (va en el plafón, no en la chalupa). Temperatura: sensor aparte en la app.
3. Módulo “sin neutro” detrás del apagador actual (Zigbee tipo Sonoff ZBMINI-L2): conservas el look del apagador viejo, pero necesitas hub Zigbee y **no** ves temperatura en la pared.

## 8. Problemas frecuentes

| Síntoma | Qué revisar |
|---------|-------------|
| No aparece en la app | WiFi 5 GHz, 2.4 GHz lejos, o no está en modo pairing |
| Foco LED parpadea (modelo sin neutro) | Falta el capacitor junto al foco, o el LED es de muy pocos watts |
| La pantalla no enciende | No hay neutro, o L/N invertidos |
| Temperatura “rara” | El sensor está dentro de la caja y se calienta un poco; es normal ±1–2 °C |
| Se desconecta | WiFi saturado; acerca un repetidor 2.4 GHz |

## 9. Seguridad

- Nunca trabajes con la pastilla arriba.
- Si al quitar el apagador viejo ves cables quemados o cajas de metal sin tierra, para y llama electricista.
- El NSPanel no sustituye un interruptor termomagnético ni un GFCI.
