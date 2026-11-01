# Linux para juegos: ¿la gráfica puede funcionar como en Windows?

Investigación al **1 de noviembre de 2026**. No tenemos el modelo exacto de la gráfica en este chat, así que la respuesta va por marca. El modelo (RTX 3060, RX 6700 XT, GTX 1660, Arc A770…) cambia la recomendación.

## Respuesta corta

Sí se puede instalar una distro de juegos y usar la gráfica de verdad: Steam, Proton, Vulkan, DLSS o FSR, HDR y frecuencia variable. En un solo jugador de Steam, y en muchos multijugador con anti-cheat compatible, la experiencia ya es de PC gamer, no de “Linux sin drivers”.

Igualar Windows en **todos** los juegos y en **todas** las funciones del panel de NVIDIA o AMD no está resuelto. Hay dos huecos distintos:

1. **Rendimiento.** En AMD RDNA 2 y RDNA 3 suele quedar a pocos puntos de Windows, y a veces los 1% lows salen mejor en Linux. En NVIDIA el resultado es irregular: juegos Vulkan nativos se acercan, y el ray tracing o el path tracing suelen ir detrás. En RDNA 4 (RX 9070 / 9070 XT) el soporte ya existe y mejoró durante 2026, y aun así hay reportes serios de un hueco de alrededor del 20–35% frente a Windows en los mismos títulos.
2. **Juegos que ni arrancan.** Valorant, League of Legends, Fortnite, Apex, Call of Duty con Ricochet, Battlefield, EA Sports FC, Rainbow Six Siege, Destiny 2, PUBG y Roblox siguen bloqueados por anti-cheat de kernel. Ninguna distro lo arregla. Ahí Windows se queda.

Si esos juegos son el uso diario, el camino práctico es **dos discos**: Linux para la biblioteca de Steam y Windows para lo que el anti-cheat rechaza. Borrar Windows el primer día es la forma de arrepentirse.

## Qué distro, según la gráfica

| Gráfica | Distro que yo instalaría | Por qué |
|---------|--------------------------|---------|
| **AMD Radeon**, PC de sala, un solo disco para juegos | **SteamOS 3.8** | Desde junio de 2026 Valve deja instalar la imagen en un PC de escritorio con **GPU AMD discreta**. Pierre-Loup Griffais (Valve), 24 jun 2026: con una AMD ya puedes armar tu propia Steam Machine. NVIDIA sigue en trabajo; en The Verge dijo que el equipo existe y que no contaría con ello dentro de 2026. |
| **AMD**, PC que también es escritorio (navegador, archivos, trabajo) | **Bazzite** (imagen AMD/Intel) o **CachyOS** | Misma pila Mesa/RADV. Bazzite se actualiza por imagen completa y puedes volver al arranque anterior si un update sale mal. CachyOS (Arch) suele ir un poco adelante en kernel y frametimes, y pide más mano. |
| **NVIDIA RTX 20 o más nueva** (Turing, Ampere, Ada, Blackwell) | **Bazzite, imagen NVIDIA** | El estable `44.20261026` (26 oct 2026) trae el módulo abierto **615.78.08**, kernel 7.2.11 y Mesa 26.2.4. No se baja el `.run` de NVIDIA. El modo consola (Steam Gaming Mode) y el uso HTPC con NVIDIA siguen marcados como **beta** en bazzite.gg. |
| **GTX 900, GTX 1000 o Volta** | **Bazzite, imagen legacy / LTS** | El driver abierto 615 ya no cubre Maxwell, Pascal ni Volta. Esa imagen lleva el branch **580.178.04**, el último que NVIDIA mantiene para esas generaciones, sobre un kernel LTS. |
| **Intel Arc** | **Bazzite** o **Nobara** | Mesa (ANV) las mueve. Sirven para jugar. Quedan más lejos de “como en Windows” que una Radeon RDNA 2/3 en los juegos DirectX 12 pesados. |

Nobara (Fedora, mantenida por GloriousEggroll, el autor de Proton-GE) es la alternativa si quieres un sistema normal, con `dnf`, y el driver NVIDIA ya integrado. En FPS, Bazzite y Nobara quedan dentro del ruido de medición: el techo lo pone Proton y el driver, no el logo de la distro.

**SteamOS y el disco único.** La instalación actual regraba el disco. Griffais explicó a The Verge que todavía no hay un asistente que aparte Windows y partizione. Secure Boot hay que apagarlo para instalar. Si el plan es conservar Windows, SteamOS va en **otro disco**, o se prueba antes Bazzite / Nobara / CachyOS, que sí saben convivir con otra partición.

## Cómo se ve el rendimiento, sin números inventados

No hay una cifra única de “Linux corre al X% de Windows”. Depende del juego, de la API y de la generación.

- **Juegos nativos en Vulkan** (Counter-Strike 2, y varios títulos nuevos con backend Vulkan): es donde las dos plataformas más se parecen.
- **DirectX 11 y 12 vía Proton** (DXVK y VKD3D-Proton): es la vía normal de la biblioteca de Steam. En Radeon RDNA 2/3 las comparativas de 2026 de Nobara, CachyOS y Bazzite contra Windows 11 suelen salir empatadas o con Linux adelante en estabilidad de frametime. En NVIDIA, el mismo juego puede ir casi igual o claramente más lento; el ray tracing agranda el hueco.
- **RDNA 4.** Un reporte detallado en los foros de Phoronix (RX 9070 XT, pruebas de enero a abril de 2026, repetidas con kernel 7, Mesa 26 y Proton 11, en Ubuntu, Fedora, Nobara, CachyOS y Bazzite) midió Crysis 3 Remastered a 117 FPS en Linux contra 167 en Windows, y el mismo orden de diferencia en cómputo. Es un usuario, no un laboratorio, y documentó el método. No hay que vender la RX 9070 como “idéntica a Windows”.
- **DLSS en NVIDIA.** La guía de NVIDIA actualizada el 23 sep 2026 documenta Super Resolution, Frame Generation, Ray Reconstruction y DLAA tanto en juegos nativos de Linux como en Proton, mediante DXVK-NVAPI. Frame Generation se ha caído del menú al cambiar de versión de Proton (issue abierto de Valve, discutido todavía en mayo de 2026). Si un juego pierde el toggle, se prueba otra versión de Proton antes de culpar a la distro.
- **FSR** en AMD funciona dentro del juego, igual que en Windows. El panel Adrenalin no existe; el equivalente de uso diario es CoreCtrl o LACT.
- **Grabar y streamear.** NVENC funciona. El overlay de GeForce Experience / NVIDIA App no. En Linux se usa MangoHud, Gamescope y OBS.

HDR y VRR están en la propuesta de Bazzite y de Gamescope. En NVIDIA, el modo consola donde eso más importa sigue en beta. En un monitor VRR de escritorio con KDE Wayland, AMD es el camino con menos sorpresas.

## Juegos: lo que la gráfica no puede arreglar

Lista tomada de [GamingOnLinux Anti-Cheat](https://www.gamingonlinux.com/anticheat/), consultada para esta nota. El estado lo decide el publisher, y cambia sin avisar.

| Juego | En Linux | Anti-cheat |
|-------|----------|------------|
| Counter-Strike 2, Dota 2 | Funciona | VAC |
| Overwatch | Funciona | Defense Matrix |
| Marvel Rivals | Funciona en escritorio con el argumento de lanzamiento `SteamDeck=1 %command%` | NEAC |
| Fall Guys, Lost Ark, New World, Insurgency: Sandstorm | Funciona | Easy Anti-Cheat, con soporte Linux activado por el estudio |
| Genshin Impact | Funciona, sin declaración oficial de soporte | miHoYo Protect |
| GTA V | Solo un jugador | BattlEye en el online |
| Valorant, League of Legends, Teamfight Tactics, 2XKO | No arranca | Vanguard |
| Fortnite | No arranca | Easy Anti-Cheat, Epic no lo habilita en Proton |
| Apex Legends | No arranca | Easy Anti-Cheat |
| Call of Duty moderno, Warzone, Black Ops 6 y 7 | No arranca | Ricochet |
| Battlefield (incluye Battlefield 6), EA Sports FC 24 a FC 27 | No arranca | EA Javelin |
| Rainbow Six Siege X, Destiny 2, PUBG | No arranca | BattlEye, sin soporte Linux en esos títulos |
| Roblox | No arranca | Hyperion |

Easy Anti-Cheat y BattlEye **sí** tienen modo Linux. El estudio tiene que encenderlo. Por eso Sea of Thieves o Fall Guys entran, y Fortnite o Destiny 2 no. Cambiar de Bazzite a Nobara no mueve esa lista.

Game Pass de PC (la app de Microsoft Store) no es una biblioteca instalable fiable en Linux. Lo que sí corre es el juego en la nube, en el navegador. Epic, GOG, Ubisoft, EA App y Battle.net se lanzan con Lutris o Heroic; el anti-cheat de cada juego sigue aplicando.

Antes de formatear, los cinco juegos que más se usan se buscan en [ProtonDB](https://www.protondb.com/).

## Cómo probarlo sin quedarse sin Windows

1. Anota el modelo exacto. En Windows: Administrador de dispositivos → Adaptadores de pantalla, o `dxdiag` → pestaña Pantalla. También sirve la caja o la factura.
2. Respalda lo que no esté en la nube. La imagen de SteamOS **borra el disco destino**.
3. Si hay un segundo SSD, instala ahí. El disco de Windows no se toca. En la BIOS se elige el disco de arranque.
4. ISO según la tabla de arriba. En Bazzite el selector de la página de descarga pregunta la GPU y, si es NVIDIA vieja, manda a la imagen legacy. Hay que leer el aviso de beta si se quiere el modo consola con NVIDIA.
5. Secure Boot: SteamOS pide apagarlo. Bazzite firma sus imágenes y enrolla una llave en el primer arranque; se puede dejar encendido si se sigue su guía.
6. En Steam, Proton Experimental por juego. Si un título con DLSS Frame Generation pierde la opción, se prueba Proton 9 o la hotfix antes de cambiar de distro.
7. Una semana de uso real. Si los juegos que importan están en la tabla de “no arranca”, Windows se queda en el otro disco.

## Fuentes

- Bazzite, página oficial (aviso de NVIDIA en Gaming Mode / HTPC como beta) y release estable `44.20261026` del 26 oct 2026: kernel 7.2.11, Mesa 26.2.4, Nvidia Open 615.78.08, Nvidia LTS 580.178.04. https://bazzite.gg/ y https://github.com/ublue-os/bazzite/releases
- Universal Blue, nota de las imágenes legacy: el branch 580 es el último con Maxwell, Pascal y Volta, y esas imágenes pasan a kernel LTS. https://universal-blue.discourse.group/t/bazzites-biggest-update-deck-44-has-launched-happy-birthday-to-universal-blue/12373
- Phoronix, SteamOS 3.8.10 estable, 18 jun 2026. https://www.phoronix.com/news/SteamOS-3.8.10-Stable
- Pierre-Loup Griffais, 24 jun 2026, imagen de instalación 3.8 con GPU AMD discreta; más GPUs en camino. Recogido por VideoCardz y GamingOnLinux.
- The Verge, entrevista con Griffais: SteamOS en hardware de escritorio, NVIDIA en desarrollo y sin fecha dentro de 2026, instalador sin asistente de dual boot. https://www.theverge.com/games/953411/valve-steamos-desktop-nvidia
- NVIDIA, “DLSS / Smooth Motion / Reflex”, guía de driver, actualizada el 23 sep 2026. https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/gaming.html
- Phoronix, driver Linux 615.78.08 y `VK_NV_low_latency2` r3 para VKD3D-Proton, 7 oct 2026. https://www.phoronix.com/news/NVIDIA-615.78.08-Linux
- Valve Proton issue 8692, regresión de DLSS Frame Generation entre versiones de Proton, seguimiento hasta mayo 2026. https://github.com/ValveSoftware/Proton/issues/8692
- Foro Phoronix, reporte de RX 9070 XT un 20–35% por debajo de Windows, mayo 2026 con addendum de abril. https://www.phoronix.com/forums/forum/linux-graphics-x-org-drivers/open-source-amd-linux/1633449-rdna4-gpus-consistently-performing-20-35-worse-on-linux-than-on-windows
- GamingOnLinux, lista de anti-cheat. https://www.gamingonlinux.com/anticheat/
