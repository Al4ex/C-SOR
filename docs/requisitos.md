# Requisitos — apagador inteligente

Capturados a partir de la solicitud original:

> “Oye, soy de México, san juan, ocupo un apagador inteligente que se pueda usar desde el celular, también que se toque obviamente y pues si se puede que muestre la temperatura.”

## 1. Usuario y contexto

| Campo | Valor |
|-------|--------|
| País | México |
| Localidad | San Juan (envío nacional; instalación residencial típica) |
| Red eléctrica | 127 V, 60 Hz |
| Caja de pared | Chalupa estándar 2x4 (formato US / 120 mm) |
| Uso | Sustituir un apagador de luz de casa |

## 2. Requisitos funcionales

### Obligatorios

- **RF-01 Control desde el celular.** Encender y apagar la luz desde Android o iPhone, en casa o fuera (con internet).
- **RF-02 Control táctil en la pared.** Seguir usándolo como apagador: tocar la placa o un botón, sin teléfono.
- **RF-03 Sustituir el apagador actual.** Encaja en chalupa 2x4 y controla al menos 1 circuito de iluminación.
- **RF-04 Voltaje México.** Aceptar 100–240 V AC 50/60 Hz.

### Deseables

- **RD-01 Temperatura en el propio aparato.** Pantalla o indicador que muestre la temperatura del cuarto, no solo en el celular.
- **RD-02 Dos circuitos.** Útil si el apagador actual tiene 2 botones (dos lámparas).
- **RD-03 Voz.** Alexa o Google Assistant.
- **RD-04 Horarios.** Encender/apagar a cierta hora o al atardecer.
- **RD-05 Compartir con familia.** Varias personas con la misma app.

### Fuera de alcance (por ahora)

- Control de boiler o minisplit como función principal.
- Sistema KNX / instalación profesional de edificio.
- App propia: se usa la del fabricante (eWeLink, Smart Life, Tecnolite Connect).

## 3. Requisitos de instalación

- **RI-01 Neutro.** Confirmar si la chalupa tiene neutro. Muchas casas en México no lo tienen.
  - Con neutro: NSPanel y la mayoría de modelos con pantalla.
  - Sin neutro: modelos Tuya/Tecnolite “sin neutro” (no suelen traer pantalla de temperatura).
- **RI-02 WiFi 2.4 GHz.** Obligatorio. Si el módem es “banda única 5 GHz”, hay que activar 2.4 GHz o un SSID mixto.
- **RI-03 Carga.** Respetar watts máximos del aparato (NSPanel: 600 W total / ~2 A por canal; no es para boiler ni plancha).
- **RI-04 Seguridad.** Cortar energía en la pastilla. Instalación por electricista recomendada.

## 4. Criterios de aceptación

El producto se considera correcto si:

1. Desde el celular se enciende y se apaga la luz, y el estado coincide con lo que se ve en la pared.
2. Tocando el aparato (pantalla o botón) la luz cambia, aunque el celular esté apagado o fuera de casa.
3. Si se eligió la opción con temperatura: en la pantalla del apagador se ve un valor de ambiente razonable (±2 °C respecto a un termómetro de cuarto).
4. Sigue funcionando el toque local si se cae internet (el WiFi del aparato puede perderse; el relé local debe seguir respondiendo al botón).

## 5. Restricciones

- No usar el **NSPanel Pro** como reemplazo de apagador: no tiene relés de luz.
- No comprar formato europeo 86×86 mm si la caja es chalupa mexicana 2x4; pedir **US / 120**.
- No conectar cargas de calefacción de agua ni motores en un apagador de 2 A / 600 W.
