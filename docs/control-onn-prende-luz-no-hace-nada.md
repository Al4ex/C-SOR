# Control Onn: prende luz pero no hace nada

Guía para cuando aprietas un botón, **el LED del control se enciende**, y el televisor / la cajita Onn **no responde**.

---

## 1. Antes de nada: qué significa esa luz

La lucecita del control **no es la señal**. Solo confirma que el botón cerró el circuito y que las pilas tienen *algo* de carga.

El aparato responde a otra cosa:

| Tipo de control | Cómo habla con el aparato | Qué necesita |
|-----------------|---------------------------|--------------|
| Caja Onn Google TV / Android TV | **Bluetooth** (menús) + **IR** (a veces volumen/power) | Emparejado. No hace falta apuntar si ya está pareado. |
| TV Onn Roku (voz) | **RF / pairing** | Emparejado. Botón Pair bajo la tapa o atrás. |
| Control de TV Onn “tonto” | Solo **infrarrojo (IR)** | Apuntar al sensor del TV. Sin pairing. |
| Universal Onn (TV / SAT / AUDIO) | Solo **IR** + un **código** de marca | Modo correcto (TV, SAT…) y código programado. |

Por eso es el síntoma más común: **el LED prende y el aparato se hace wey**. El control “vive”, pero o no emite IR/Bluetooth, o emite y el aparato ya no lo reconoce.

**Regla de oro:** cambia las pilas **antes** de cualquier otra cosa. El LED gasta poquito; el IR y el Bluetooth gastan más. Pilas flojas = luz sí, mando no.

---

## 2. Identifica tu control (30 segundos)

Míralo y elige **una** ruta. El resto de la guía depende de esto.

| Lo que ves en el control | Es este |
|--------------------------|---------|
| Botón de micrófono / Google Assistant, Home con casita, Netflix / YouTube / Disney | **Caja Onn Google TV** → sección 5 |
| Logo Roku o asterisco/voz, Home con casa Roku | **TV o player Onn Roku** → sección 6 |
| Solo power, vol, ch, menú. Sin micrófono. Hay que apuntar o no prende nada si tapas la punta | **TV Onn por IR** → sección 7 |
| Botones extra **TV / SAT/CBL / AUDIO / STREAM** (a veces DVD) | **Universal Onn** → sección 8 |

El modelo exacto suele estar **impreso dentro del compartimento de las pilas**. Anótalo si vas a comprar repuesto.

---

## 3. Arreglo rápido (5 minutos)

Hazlo en este orden. Casi siempre se resuelve aquí.

1. **Saca las dos pilas.** Con el control vacío, aprieta **cualquier botón 10 segundos** (descarga residual).
2. Limpia los contactos de metal con un trapo seco o un cotonete. Si hay verdín, un poco de alcohol isopropílico y deja secar.
3. Pon **2 pilas AAA alcalinas nuevas** (Duracell, Energizer, Kirkland). Mismo par, mismas marca y fecha. **No mezcles** nueva + vieja, ni alcalina + recargable.
   - El lado plano (−) va contra el resorte.
4. Prueba a 50 cm del aparato, **sin nada en medio** (barra de sonido, marco, vidrio del mueble).
5. Según el tipo:
   - **Caja Google TV:** mantén **Atrás + Inicio (Home)** hasta que el LED **parpadee**. En la cajita, mantén el botón **Reset** 5 segundos. Espera el mensaje de emparejado.
   - **Roku:** destapa las pilas, mantén el botón **Pairing** (o Atrás + Home) 5 segundos hasta que parpadee. Acércalo al TV.
   - **IR / universal:** apunta a la **franja inferior o el logo** del TV (ahí está el sensor), no a la pantalla.
6. Confirma que el TV está en la **entrada correcta** (HDMI 1, HDMI 2…). El control de la cajita no cambia de HDMI si el TV está en otra entrada y el CEC está apagado.

Si después de esto sigue igual, ve al diagnóstico.

---

## 4. Diagnóstico por síntoma

| Síntoma | Causa más probable | Qué hacer |
|---------|--------------------|-----------|
| LED prende **fijo** al apretar, el aparato no se mueve | Perdió el pairing, o es IR y no apunta al sensor | Sección 5, 6 o 7 |
| LED **parpadea 3 veces** y se apaga | Pilas agotadas (lo dice el manual Onn) | Cambiar las dos AAA |
| LED prende, **volumen/power sí**, menús **no** | Está en modo IR; falta Bluetooth | Sección 5 (re-parear) |
| LED prende, **nada** responde, ni de muy cerca | IR muerto, o TV/caja congelada | Sección 9 y 10 |
| Funciona a ratos, hay que apretar recio | Contactos sucios o membrana gastada | Sección 10 |
| Apuntas y no, de lado tampoco | Sensor del TV tapado (barra, adorno) | Sección 7 |
| El TV enciende con el botón de atrás, el control no | El TV está bien; el control no emite o no está pareado | Sección 9, luego 5–8 |
| Después de un apagón o update dejó de servir | Se le olvidó el pairing | Sección 5 o 6 |
| Universal: LED prende, TV no hace caso | Código perdido o modo SAT en vez de TV | Sección 8 |

---

## 5. Caja Onn Google TV / Android TV (Bluetooth)

Es el caso más frecuente de “prende luz y no hace nada”. El LED enciende aunque **ya no esté emparejado**. Sin pairing, los menús no se mueven. A veces el volumen del TV sí responde por IR: eso confirma que el control vive y que el problema es Bluetooth.

### 5.1 Re-parear (oficial)

1. TV encendido, **entrada HDMI** de la cajita Onn.
2. Cajita con luz **blanca** (encendida). Roja = reposo: despiértala con el botón de power del TV o desenchufa y vuelve a conectar.
3. En el control, mantén **Atrás (←) + Inicio (casita)** hasta que el LED **parpadee**.
4. En la **cajita**, mantén el botón **Reset** (hoyito o botón chico, atrás o abajo) **5 segundos**. Eso solo resetea el pairing, no borra tus apps.
5. Acerca el control a la cajita. En pantalla debe salir “Pairing successful” / “Control emparejado”.
6. Suelta los botones y prueba Inicio, OK y las flechas.

Si no hay pantalla de pairing: desenchufa la cajita **5–7 segundos**, conéctala, espera el inicio y repite 3–5.

### 5.2 Olvidar el control viejo (si puedes entrar al menú)

Con otro control, el app del teléfono (sección 11) o un mouse USB en el puerto de la cajita:

**Ajustes → Mandos y accesorios / Remotes & accessories → tu control → Olvidar / Forget.**

Luego otra vez Atrás + Home.

### 5.3 Si solo fallan volumen y power del TV

Eso lo manda por **IR** o por **CEC (HDMI)**. El Bluetooth de la cajita puede estar bien.

- Apunta al sensor del **televisor**, no a la cajita.
- En el TV: activa HDMI-CEC (en Samsung se llama Anynet+, en LG SimpLink, en Hisense CEC, en Sony Bravia Sync).
- En la cajita: **Ajustes → Mandos → Configurar control para el televisor** (o IR programming) y vuelve a enseñarle marca y códigos.

---

## 6. TV Onn Roku

1. Quita las pilas del control.
2. **Desenchufa el TV 5 segundos** y vuélvelo a conectar. Espera a que cargue el inicio Roku.
3. Reescribe las pilas.
4. Abre la tapa. Busca el botón **Pairing** (a veces atrás del control).
   - **Con botón Pair:** mantén 5 segundos hasta que el LED parpadee.
   - **Sin botón Pair:** mantén **Atrás + Home** 5 segundos hasta que parpadee.
5. Acerca el control al TV y espera hasta **30 segundos**. Debe salir el aviso de emparejado.

Si el LED de pairing **nunca** parpadea: pilas nuevas otra vez y limpia contactos. Sin parpadeo no entra en modo pairing.

Plan B: app **Roku** en el celular, misma Wi‑Fi que el TV. Desde ahí: **Settings → Remotes & devices → Add device / Pair remote**.

---

## 7. TV Onn solo IR (hay que apuntar)

No se empareja. O el sensor ve la luz invisible, o no.

1. Apunta a la **barrita o ventanita** del TV (abajo al centro o junto al logo), no al centro de la pantalla.
2. Acércate a **30–50 cm**, a oscuras si puedes, y prueba power y volumen.
3. Quita lo que tape el sensor: barra de sonido pegada al marco, marco de fotos, vidrio del mueble, sticker, polvo grueso.
4. Prueba el **botón físico del TV** (atrás o abajo, a veces es un joystick). Si el TV responde al botón y no al control, el TV está bien.
5. Haz la **prueba de cámara** (sección 9).

Algunos Onn “Android TV” de pantalla (no cajita) también usan Bluetooth. Si trae micrófono, trátalo como sección 5.

---

## 8. Control universal Onn

Si el LED prende y el TV no hace caso, casi siempre **perdió el código** o está en **otro modo** (SAT/CBL en vez de TV).

### 8.1 Primero: modo correcto

Aprieta **TV** (el botón debe quedar o encenderse). Luego power. Si programaste el cable, SAT no va a apagar el televisor.

### 8.2 Código directo

1. Enciende el aparato que quieres controlar.
2. Mantén el botón de categoría (**TV**, **SAT/CBL**, etc.) hasta que el LED se quede **rojo fijo**.
3. Teclea el **código de 4 dígitos** de la marca (viene en el instructivo o en [onnremotes.com](https://www.onnremotes.com/troubleshooting/)).
4. Si el código es válido, el LED **se apaga**. Si parpadea y se queda encendido, el código no sirvió: prueba el siguiente de la lista.
5. Prueba power, vol, input. Si “medio sirve”, **cambia al siguiente código** de esa marca. El primero que apaga no siempre mueve todas las teclas.

### 8.3 Búsqueda automática

1. Aparato encendido. Mantén el botón de categoría hasta LED fijo.
2. Elige de nuevo la categoría. El LED pestañea y se queda.
3. Apunta al aparato y **mantén OK** hasta que **se apague**. Suelta al instante para fijar el código.
4. Prueba todas las teclas. Si faltan funciones, repite: a veces agarra un código a medias.

La búsqueda puede tardar **varios minutos**. Si sueltas OK sin querer, al repetir suele seguir donde se quedó.

**Luz que parpadea 3 veces** en un universal Onn = cambia pilas. No es un código malo.

---

## 9. Prueba de cámara: ¿el IR está vivo?

Sirve para IR y universales, y para saber si la cajita Google al menos emite IR.

1. Abre la **cámara del celular** (en muchos Android se ve; en iPhone reciente a veces solo la frontal, o no se ve por el filtro).
2. Apunta la puntita del control a la cámara, a 5–10 cm.
3. Aprieta un botón y mira la **pantalla del teléfono**, no el LED del control.

| Qué ves en el teléfono | Significado |
|------------------------|-------------|
| Destello morado / blanco en la puntita | El IR **sí sale**. El problema es pairing, código, sensor o entrada HDMI. |
| El LED del control prende y **en la cámara no hay destello** | El emisor IR está **muerto** o las pilas no dan para emitirlo. Cambia pilas y repite. Si sigue así: control nuevo. |
| No se ve destello y tu iPhone es reciente | No concluyas: prueba con otro Android. |

Bluetooth **no se ve** en la cámara. Si es caja Google y el IR destella pero los menús no, re-parea (sección 5).

---

## 10. Pilas, contactos y control “ahogado”

Aunque el LED prenda:

- Dos AAA **alcalinas nuevas del mismo paquete**. Las “que le quedan a la linterna” ya no sirven.
- Recargables NiMH andan en ~1.2 V: algunos Onn fallan con ellas aunque el LED prenda. Prueba alcalinas de 1.5 V antes de declarar el control muerto.
- Resortes oxidados o chuecos: estíralos un milímetro para que aprieten. Verdín verde = limpia con alcohol y deja secar.
- Control que se mojó o se le cayó el refresco: ábrelo (a veces solo ganchitos), lava la placa con alcohol isopropílico, seca 24 h. Si la membrana de hule se pegó, ya no recupera el tacto.
- Si hay que **aplastar** para que el LED prenda: la goma del botón está lisa. Se puede cambiar la membrana (repuesto genérico) o conviene un control nuevo.

---

## 11. Mientras tanto: usa el teléfono

No te quedes sin mando.

| Aparato | App | Nota |
|---------|-----|------|
| Caja Onn Google TV | [Google TV](https://play.google.com/store/apps/details?id=com.google.android.videos) / [Google Home](https://play.google.com/store/apps/details?id=com.google.android.apps.chromecast.app) o **Android TV** | Misma red Wi‑Fi. En Home: el dispositivo → control remoto. |
| TV / player Roku | [Roku](https://www.roku.com/mobile-app) | Misma Wi‑Fi. Desde ahí también se re-parea. |
| TV con HDMI-CEC | El control **original del televisor** | Power, vol y a veces las flechas llegan a la cajita. |

Muchas cajitas Onn aceptan un **mouse USB** en el puerto de atrás para moverse por Ajustes si no hay ningún control.

También está el **botón/joystick del TV** (atrás o abajo): sirve para cambiar HDMI y no quedarte en negro.

---

## 12. El aparato, no el control

Si el IR destella en la cámara y el pairing no pega, prueba el receptor:

1. **Desenchufa** TV y cajita. Espera 10 segundos. Enchufa primero el TV, luego la cajita.
2. Prueba **otro control** (el del TV, un universal, el del vecino del mismo modelo). Si ninguno sirve, el sensor del TV o el Bluetooth de la cajita están mal.
3. En cajas Google: **Ajustes → Sistema → Acerca de → Actualización del sistema**. Un update a medias deja el Bluetooth sordo; al terminar, re-parea.
4. Cajita metida **detrás de un metal** o dentro de un mueble cerrado: el Bluetooth se corta. Sácala a un costado, con el HDMI bien puesto.
5. Muchos Bluetooth juntos (bocinas, smartwatch, teclado) no suelen matarlo, pero un **USB 3** o un hub pegado a la cajita sí mete ruido. Prueba sin extras.

Reset de fábrica de la cajita (último recurso): Reset **+ energía** 5 segundos, o Ajustes → Fábrica. **Se borran cuentas y apps.** No lo hagas si solo falló el control.

---

## 13. Cuándo ya no vale la pena

Cambia el control si:

- Con pilas nuevas, la cámara **no ve destello IR** y es un control IR/universal.
- Es Google TV o Roku y **nunca** entra a modo pairing (LED no parpadea) con pilas nuevas y contactos limpios.
- Se mojó, se partió o los botones ya no regresan.
- Costó menos de lo que te va a tardar desarmarlo.

Repuestos en México (Walmart, Mercado Libre): busca **el modelo de adentro de la tapa** (ej. `100021244`, `100026240`, `100003397`, o “onn Google TV remote”). Los genéricos “para Onn 4K” suelen servir si dicen **Bluetooth + IR**. Un universal barato **no reemplaza** el control de la cajita para menús y voz.

Mientras llega el nuevo, usa la app del teléfono (sección 11).

---

## 14. Checklist para no dar vueltas

- [ ] Dos AAA alcalinas nuevas, bien puestas, contactos limpios
- [ ] TV en el HDMI de la cajita (si aplica)
- [ ] Nada tapando el sensor del TV
- [ ] Identificaste el tipo (sección 2)
- [ ] Re-pareaste (Google: Atrás + Home + Reset 5 s; Roku: Pair 5 s)
- [ ] Prueba de cámara: ¿hay destello IR?
- [ ] App del teléfono como control de respaldo
- [ ] Si IR muerto o pairing imposible: control nuevo del mismo modelo
