"""Biblioteca de motivos.

Cada motivo se dibuja dentro de una caja local de 100x100 con el centro en
(50, 50), para poder escalarlo y rotarlo con `svg.colocar`.

La regla de diseño es siempre la misma: el símbolo de Naruto se somete a la
gramática del bordado istmeño (simetría, repetición en banda, contorno de
cadenilla, relleno plano de seda floja) y nunca al revés.
"""

from __future__ import annotations

import math
from typing import Sequence

from .paleta import C
from .svg import (
    circulo,
    colocar,
    grupo,
    linea,
    n,
    polar,
    polilinea,
    rectangulo,
    ruta,
)

# --------------------------------------------------------------------------
# Espirales: el puente formal entre el remolino Uzumaki y el xicalcoliuhqui
# --------------------------------------------------------------------------


def _espiral_cinta(
    cx: float,
    cy: float,
    r_inicio: float,
    r_fin: float,
    vueltas: float,
    grosor_inicio: float,
    grosor_fin: float,
    fase: float = -90.0,
    sentido: int = 1,
    pasos: int = 150,
) -> str:
    """Devuelve el contorno cerrado de una cinta en espiral de grosor variable."""
    t_max = math.radians(360.0 * vueltas)
    externo: list[tuple[float, float]] = []
    interno: list[tuple[float, float]] = []
    for i in range(pasos + 1):
        u = i / pasos
        ang = math.radians(fase) + sentido * u * t_max
        r = r_inicio + (r_fin - r_inicio) * u
        w = grosor_inicio + (grosor_fin - grosor_inicio) * (u ** 0.85)
        externo.append((cx + (r + w / 2) * math.cos(ang), cy + (r + w / 2) * math.sin(ang)))
        r_in = max(r - w / 2, 0.0)
        interno.append((cx + r_in * math.cos(ang), cy + r_in * math.sin(ang)))
    return polilinea(externo + interno[::-1], cerrada=True)


def espiral_uzumaki(color: str = None, contorno: str = None, vueltas: float = 2.45,
                    grosor: float = 10.5, pasos: int = 150) -> str:
    """Remolino Uzumaki: espiral de cinta que remata en punta, como la del chaleco."""
    color = color or C["rojo"]
    contorno = contorno or C["oro"]
    d = _espiral_cinta(50, 50, 4.5, 43.0, vueltas, grosor, grosor * 0.12, pasos=pasos)
    return grupo([
        ruta(d, fill=color, stroke=contorno, stroke_width=1.1, stroke_linejoin="round"),
        circulo(50, 50, grosor * 0.52, fill=color, stroke=contorno, stroke_width=1.1),
    ])


def hoja_konoha(hoja: str = None, espiral: str = None, contorno: str = None) -> str:
    """Hoja de Konoha: la hoja aloja una espiral, igual que la greca de Mitla."""
    hoja = hoja or C["verde"]
    espiral = espiral or C["naranja"]
    contorno = contorno or C["oro"]
    # Hoja lanceolada: punta aguda arriba, panza abajo. Si se ensancha de más
    # deja de leerse como hoja y pasa a parecer una gota de agua.
    perfil = (
        "M 50,2 "
        "C 57,22 79,44 81,63 "
        "C 83,83 69,97 50,97 "
        "C 31,97 17,83 19,63 "
        "C 21,44 43,22 50,2 Z"
    )
    nervio = "M 50,8 C 52,38 52,66 50,92"
    remolino = _espiral_cinta(50, 59, 3.2, 28.0, 1.8, 13.0, 1.8)
    return grupo([
        ruta(perfil, fill=hoja, stroke=contorno, stroke_width=1.6, stroke_linejoin="round"),
        ruta(nervio, fill="none", stroke=contorno, stroke_width=1.0, opacity=0.55),
        ruta(remolino, fill=espiral, stroke=contorno, stroke_width=1.0),
        circulo(50, 59, 6.4, fill=espiral, stroke=contorno, stroke_width=1.0),
    ])


# --------------------------------------------------------------------------
# Ojos del clan convertidos en rosas istmeñas
# --------------------------------------------------------------------------


def _magatama(r: float) -> str:
    """Coma del sharingan, dibujada apuntando hacia la derecha."""
    return (
        f"M 0,{n(-r)} "
        f"A {n(r)},{n(r)} 0 1 1 0,{n(r)} "
        f"C {n(1.7 * r)},{n(1.05 * r)} {n(3.1 * r)},{n(0.5 * r)} {n(3.6 * r)},{n(-0.7 * r)} "
        f"C {n(2.4 * r)},{n(0.15 * r)} {n(1.1 * r)},{n(0.25 * r)} 0,{n(-r)} Z"
    )


def _petalos(cantidad: int, r_interno: float, r_externo: float, ancho: float,
             color: str, contorno: str, giro: float = 0.0, opacidad: float = 1.0) -> str:
    piezas = []
    for i in range(cantidad):
        ang = giro + i * 360.0 / cantidad
        piezas.append(
            grupo(
                ruta(
                    f"M 0,{n(-ancho / 2)} "
                    f"C {n(r_externo * 0.45)},{n(-ancho * 0.62)} {n(r_externo * 0.8)},{n(-ancho * 0.34)} {n(r_externo)},0 "
                    f"C {n(r_externo * 0.8)},{n(ancho * 0.34)} {n(r_externo * 0.45)},{n(ancho * 0.62)} 0,{n(ancho / 2)} Z",
                    fill=color,
                    stroke=contorno,
                    stroke_width=1.1,
                    stroke_linejoin="round",
                    opacity=opacidad,
                ),
                transform=f"translate(50,50) rotate({n(ang)}) translate({n(r_interno)},0)",
            )
        )
    return grupo(piezas)


def rosa_sharingan(fondo_ojo: str = None, comas: str = None) -> str:
    """Rosa de cadenilla cuyo corazón es un sharingan de tres comas."""
    fondo_ojo = fondo_ojo or C["rojo"]
    comas = comas or C["fondo"]
    oro = C["oro"]
    piezas = [
        _petalos(8, 14, 34, 19, C["cochinilla"], oro, giro=22.5, opacidad=0.95),
        _petalos(8, 10, 27, 17, C["naranja"], oro, giro=0.0),
        circulo(50, 50, 16.5, fill=fondo_ojo, stroke=oro, stroke_width=1.6),
        circulo(50, 50, 16.5, fill="none", stroke=C["cochinilla"], stroke_width=3.2, opacity=0.5),
    ]
    for i in range(3):
        ang = -90 + i * 120
        x, y = polar(50, 50, 9.6, ang)
        piezas.append(
            grupo(
                ruta(_magatama(3.5), fill=comas, stroke=oro, stroke_width=0.6),
                transform=f"translate({n(x)},{n(y)}) rotate({n(ang + 105)})",
            )
        )
    piezas.append(circulo(50, 50, 4.1, fill=comas, stroke=oro, stroke_width=0.8))
    return grupo(piezas)


def rosa_rinnegan(anillo_a: str = None, anillo_b: str = None) -> str:
    """Rinnegan leído como «ojo de dios»: anillos concéntricos en marco de rombo."""
    anillo_a = anillo_a or C["morado"]
    anillo_b = anillo_b or C["plata"]
    oro = C["oro"]
    piezas = [
        ruta(polilinea([(50, 6), (94, 50), (50, 94), (6, 50)], cerrada=True),
             fill=anillo_a, stroke=oro, stroke_width=1.6, opacity=0.95),
        ruta(polilinea([(50, 15), (85, 50), (50, 85), (15, 50)], cerrada=True),
             fill="none", stroke=oro, stroke_width=1.2, opacity=0.7),
    ]
    radios = [31, 26, 21, 16, 11, 6]
    for i, r in enumerate(radios):
        piezas.append(circulo(50, 50, r, fill="none",
                              stroke=anillo_b if i % 2 == 0 else oro,
                              stroke_width=2.4 if i % 2 == 0 else 1.2))
    piezas.append(circulo(50, 50, 3.0, fill=C["fondo"], stroke=anillo_b, stroke_width=1.0))
    for i in range(6):
        x, y = polar(50, 50, 34.5, i * 60 - 90)
        piezas.append(circulo(x, y, 2.4, fill=C["amarillo"], stroke=oro, stroke_width=0.6))
    return grupo(piezas)


# --------------------------------------------------------------------------
# Armas y emblemas de clan
# --------------------------------------------------------------------------


def shuriken(color: str = None, contorno: str = None, hojas: int = 4) -> str:
    color = color or C["plata"]
    contorno = contorno or C["fondo"]
    piezas = []
    for i in range(hojas):
        piezas.append(
            grupo(
                ruta("M 0,0 L 0,-44 Q 13,-27 14,-6 Z", fill=color, stroke=contorno,
                     stroke_width=1.4, stroke_linejoin="round"),
                transform=f"translate(50,50) rotate({n(i * 360 / hojas)})",
            )
        )
    piezas.append(circulo(50, 50, 9.5, fill=color, stroke=contorno, stroke_width=1.4))
    piezas.append(circulo(50, 50, 4.2, fill=C["fondo"], stroke=contorno, stroke_width=1.0))
    return grupo(piezas)


def kunai(color: str = None, mango: str = None) -> str:
    color = color or C["plata"]
    mango = mango or C["fondo"]
    oro = C["oro"]
    return grupo([
        ruta("M 50,6 L 62,34 L 58,52 L 42,52 L 38,34 Z", fill=color, stroke=oro,
             stroke_width=1.2, stroke_linejoin="round"),
        ruta("M 50,10 L 50,50", fill="none", stroke=C["humo"], stroke_width=1.0, opacity=0.8),
        rectangulo(44, 52, 12, 30, fill=mango, stroke=oro, stroke_width=1.2, rx=2),
        circulo(50, 88, 7.5, fill="none", stroke=color, stroke_width=3.4),
    ])


def uchiwa(superior: str = None, inferior: str = None) -> str:
    """Abanico Uchiha, resuelto como abanico de palma tejida del Istmo.

    Se dibuja como abanico de verdad —varillas y cabo— y no como disco
    bicolor, para que no se confunda con cualquier emblema circular.
    """
    superior = superior or C["rojo"]
    inferior = inferior or C["manta"]
    oro = C["oro"]
    piezas = [
        ruta("M 46,70 L 38,96 L 52,98 L 58,70 Z", fill=C["humo"], stroke=oro,
             stroke_width=1.1, stroke_linejoin="round"),
        ruta("M 14,46 A 36,36 0 0 1 86,46 L 86,52 L 14,52 Z", fill=superior,
             stroke=oro, stroke_width=1.3, stroke_linejoin="round"),
        ruta("M 14,52 A 36,36 0 0 0 52,87 A 36,36 0 0 0 86,52 Z", fill=inferior,
             stroke=oro, stroke_width=1.3, stroke_linejoin="round"),
    ]
    for ang in (-62, -31, 0, 31, 62):
        x1, y1 = polar(50, 52, 9.0, ang + 90)
        x2, y2 = polar(50, 52, 33.0, ang + 90)
        piezas.append(linea(x1, y1, x2, y2, stroke=oro, stroke_width=0.9, opacity=0.75))
    piezas.append(ruta("M 14,52 H 86", fill="none", stroke=oro, stroke_width=1.2))
    return grupo(piezas)


def nube_akatsuki(color: str = None, contorno: str = None) -> str:
    color = color or C["rojo"]
    contorno = contorno or C["manta"]
    # Tres lóbulos arriba, tres ondas cortas abajo: la nube roja de los mantos.
    perfil = (
        "M 10,62 "
        "C 0,52 8,36 22,38 "
        "C 22,18 46,10 56,26 "
        "C 70,14 94,24 88,44 "
        "C 100,50 98,68 86,70 "
        "C 80,78 70,76 66,70 "
        "C 60,78 48,78 42,70 "
        "C 36,77 24,76 20,69 "
        "C 14,70 10,67 10,62 Z"
    )
    return grupo([
        ruta(perfil, fill=color, stroke=contorno, stroke_width=1.5, stroke_linejoin="round"),
        ruta("M 22,52 C 34,44 48,44 56,50 C 64,44 76,45 82,52", fill="none",
             stroke=contorno, stroke_width=1.1, opacity=0.5),
    ])


def llama_kurama(color: str = None, interior: str = None) -> str:
    """Una de las nueve colas de Kurama, resuelta como voluta de fuego."""
    color = color or C["naranja"]
    interior = interior or C["amarillo"]
    return grupo([
        ruta("M 50,96 C 16,82 14,48 36,20 C 34,44 46,52 54,40 "
             "C 58,60 78,56 74,34 C 94,58 86,86 50,96 Z",
             fill=color, stroke=C["oro"], stroke_width=1.4, stroke_linejoin="round"),
        ruta("M 50,90 C 32,80 30,58 44,40 C 44,58 54,64 60,54 C 64,72 72,72 68,56 "
             "C 78,70 70,84 50,90 Z",
             fill=interior, stroke="none", opacity=0.85),
    ])


def kanji_fuego(color: str = None) -> str:
    """Kanji 火 (hi, fuego) del Hokage, en cuatro trazos de cadenilla.

    Cuatro trazos y no cinco: los dos puntos altos y las dos piernas del 人.
    Si se añade un vertical central el carácter deja de ser 火.
    """
    color = color or C["manta"]
    trazo = dict(fill="none", stroke=color, stroke_linecap="round", stroke_linejoin="round")
    return grupo([
        ruta("M 32,22 C 27,33 23,41 17,48", stroke_width=6.0, **trazo),
        ruta("M 70,22 C 75,33 79,41 85,48", stroke_width=6.0, **trazo),
        ruta("M 54,14 C 50,38 40,64 15,88", stroke_width=7.0, **trazo),
        ruta("M 48,46 C 56,62 68,76 86,88", stroke_width=6.5, **trazo),
    ])


def hitai_ate(placa: str = None, banda: str = None) -> str:
    """Placa de la banda ninja, bordada en hilo metálico."""
    placa = placa or C["plata"]
    banda = banda or C["anil"]
    return grupo([
        rectangulo(0, 38, 100, 24, fill=banda, stroke=C["fondo"], stroke_width=1.0),
        rectangulo(10, 26, 80, 48, fill=placa, stroke=C["humo"], stroke_width=1.4, rx=5),
        rectangulo(14, 30, 72, 40, fill="none", stroke=C["fondo"], stroke_width=1.0,
                   opacity=0.3, rx=3),
        circulo(19, 50, 2.6, fill=C["humo"], stroke=C["fondo"], stroke_width=0.6),
        circulo(81, 50, 2.6, fill=C["humo"], stroke=C["fondo"], stroke_width=0.6),
        colocar(hoja_konoha(hoja=C["anil"], espiral=C["plata"], contorno=C["oro"]),
                50, 50, 38),
    ])


# --------------------------------------------------------------------------
# Rombos, flores y sellos: el vocabulario zapoteco de soporte
# --------------------------------------------------------------------------


def rombo_zapoteco(colores: Sequence[str] | None = None) -> str:
    colores = list(colores or [C["anil"], C["naranja"], C["amarillo"], C["rojo"]])
    piezas = []
    for i, color in enumerate(colores):
        r = 46 - i * 10
        piezas.append(
            ruta(polilinea([(50, 50 - r), (50 + r, 50), (50, 50 + r), (50 - r, 50)], cerrada=True),
                 fill=color, stroke=C["oro"], stroke_width=1.1)
        )
    piezas.append(circulo(50, 50, 4.0, fill=C["manta"], stroke=C["oro"], stroke_width=0.8))
    return grupo(piezas)


def flor_istmena(petalo: str = None, corazon: str = None) -> str:
    petalo = petalo or C["naranja"]
    corazon = corazon or C["amarillo"]
    oro = C["oro"]
    piezas = [
        _petalos(6, 12, 32, 22, C["cochinilla"], oro, giro=30, opacidad=0.9),
        _petalos(6, 9, 26, 20, petalo, oro),
        circulo(50, 50, 10, fill=corazon, stroke=oro, stroke_width=1.2),
    ]
    for i in range(6):
        x, y = polar(50, 50, 5.2, i * 60)
        piezas.append(circulo(x, y, 1.7, fill=C["cochinilla"]))
    return grupo(piezas)


# -- Sellos de mano en rejilla, pensados para el punto de cruz ---------------


def _rejilla_caracol(lado: int = 11) -> list[str]:
    """Caracol cuadrado: el remolino Uzumaki contado punto por punto.

    Es exactamente la greca escalonada de Mitla cuando se la obliga a girar;
    de ahí que sirva igual como sello de mano y como motivo zapoteco.
    """
    rej = [["." for _ in range(lado)] for _ in range(lado)]
    x = y = 0
    dx, dy = 1, 0
    rej[0][0] = "X"
    tramo = lado - 1
    while tramo > 0:
        for _ in range(2):
            for _ in range(tramo):
                x += dx
                y += dy
                rej[y][x] = "X"
            dx, dy = -dy, dx
        tramo -= 2
    return ["".join(f) for f in rej]


SELLOS: dict[str, list[str]] = {
    "tora": [
        ".....X.....",
        "....X.X....",
        "...X...X...",
        "..X.....X..",
        ".X...X...X.",
        "X...XXX...X",
        ".X...X...X.",
        "..X.....X..",
        "...X...X...",
        "....X.X....",
        ".....X.....",
    ],
    "mi": [
        "XXX.....XXX",
        "X.X.....X.X",
        "X.XXX.XXX.X",
        "....X.X....",
        "..XXX.XXX..",
        "..X.....X..",
        "..XXX.XXX..",
        "....X.X....",
        "X.XXX.XXX.X",
        "X.X.....X.X",
        "XXX.....XXX",
    ],
    "hitsuji": [
        "XXXXX.XXXXX",
        "X...X.X...X",
        "X.X.X.X.X.X",
        "X.X.X.X.X.X",
        "X.X.XXX.X.X",
        "X.X.....X.X",
        "X.XXXXXXX.X",
        "X.........X",
        "XXXXX.XXXXX",
        "....X.X....",
        "....XXX....",
    ],
    "inu": [
        "....XXX....",
        "...X...X...",
        "..X.XXX.X..",
        ".X.X...X.X.",
        "X.X.XXX.X.X",
        "X.X.X.X.X.X",
        "X.X.XXX.X.X",
        ".X.X...X.X.",
        "..X.XXX.X..",
        "...X...X...",
        "....XXX....",
    ],
    "uma": [
        "X.........X",
        "XX.......XX",
        "X.X.....X.X",
        "X..X...X..X",
        "X...X.X...X",
        "X....X....X",
        "X...X.X...X",
        "X..X...X..X",
        "X.X.....X.X",
        "XX.......XX",
        "X.........X",
    ],
    "caracol": _rejilla_caracol(11),
}


def rejilla_a_ruta(rej: Sequence[str], x0: float, y0: float, celda: float,
                   marca: str = "X") -> str:
    """Convierte una rejilla de caracteres en un único `d` de path.

    Agrupar las celdas en un solo elemento, en vez de un `<rect>` por punto,
    baja el conteo de nodos del SVG en dos órdenes de magnitud; con las randas
    sembradas de sellos la diferencia es la que hace que el archivo se pueda
    abrir.
    """
    trozos = []
    for j, fila in enumerate(rej):
        i = 0
        while i < len(fila):
            if fila[i] == marca:
                k = i
                while k < len(fila) and fila[k] == marca:
                    k += 1
                ancho = (k - i) * celda
                trozos.append(
                    f"M{n(x0 + i * celda)},{n(y0 + j * celda)}"
                    f"h{n(ancho)}v{n(celda)}h{n(-ancho)}z"
                )
                i = k
            else:
                i += 1
    return "".join(trozos)


def sello_mano(nombre: str, color: str = None, fondo: str | None = None,
               celda: float = 100 / 11) -> str:
    color = color or C["amarillo"]
    rej = SELLOS[nombre]
    alto = len(rej)
    ancho = max(len(f) for f in rej)
    cx0 = (100 - ancho * celda) / 2
    cy0 = (100 - alto * celda) / 2
    piezas = []
    if fondo:
        piezas.append(rectangulo(0, 0, 100, 100, fill=fondo))
    piezas.append(ruta(rejilla_a_ruta(rej, cx0, cy0, celda), fill=color))
    return grupo(piezas)


# --------------------------------------------------------------------------
# Bandas (grecas) — el corazón del diseño: motivos sometidos a repetición
# --------------------------------------------------------------------------


def _modulo_exacto(ancho: float, deseado: float) -> tuple[float, int]:
    reps = max(1, round(ancho / deseado))
    return ancho / reps, reps


def _banda_rejilla(x: float, y: float, ancho: float, alto: float, modulo_deseado: float,
                   rejilla: tuple[int, int], puntos: Sequence[tuple[float, float]],
                   color: str, grosor_rel: float, espejo: bool = False) -> str:
    gw, gh = rejilla
    modulo, reps = _modulo_exacto(ancho, modulo_deseado)
    sx, sy = modulo / gw, alto / gh
    grosor = grosor_rel * alto
    piezas = []
    for k in range(reps):
        pts = puntos if not (espejo and k % 2) else [(gw - px, py) for px, py in puntos]
        abs_pts = [(x + k * modulo + px * sx, y + py * sy) for px, py in pts]
        piezas.append(ruta(polilinea(abs_pts), fill="none", stroke=color,
                           stroke_width=grosor, stroke_linecap="square",
                           stroke_linejoin="miter"))
    return grupo(piezas)


# Xicalcoliuhqui: escalera que sube de tres en tres y cierra en gancho.
# Es el motivo de Mitla, no un rectángulo con esquinas: los escalones son el motivo.
GRECA_HOJA = [(0, 12), (2, 12), (2, 9), (5, 9), (5, 6), (8, 6), (8, 3), (14, 3),
              (14, 9), (10, 9), (10, 6), (12, 6)]
REJILLA_GRECA = (16, 14)
GRECA_ESCALERA = [(0, 11), (3, 11), (3, 8), (6, 8), (6, 5), (9, 5), (9, 2), (12, 2)]


def banda_greca_hoja(x: float, y: float, ancho: float, alto: float,
                     color: str = None, modulo: float | None = None) -> str:
    """Greca de la hoja: dos xicalcoliuhqui enfrentados y una hoja de Konoha.

    El ciclo de tres módulos (greca, greca en espejo, hoja) es lo que permite
    que el emblema entre en la banda sin romper la cuenta del telar.
    """
    color = color or C["naranja"]
    modulo = modulo or alto * 1.15
    reps = max(3, 3 * round(ancho / (3 * modulo)))
    m = ancho / reps
    gw, gh = REJILLA_GRECA
    sx, sy = m / gw, alto / gh
    grosor = alto * 0.085
    piezas = [linea(x, y + alto - sy * 0.9, x + ancho, y + alto - sy * 0.9,
                    stroke=C["oro"], stroke_width=grosor * 0.5, opacity=0.5)]
    for k in range(reps):
        x0 = x + k * m
        if k % 3 == 2:
            piezas.append(colocar(hoja_konoha(hoja=C["verde"], espiral=C["naranja"],
                                              contorno=C["oro"]),
                                  x0 + m / 2, y + alto * 0.46, alto * 0.80))
            continue
        pts = GRECA_HOJA if k % 3 == 0 else [(gw - px, py) for px, py in GRECA_HOJA]
        piezas.append(ruta(polilinea([(x0 + px * sx, y + py * sy) for px, py in pts]),
                           fill="none", stroke=color, stroke_width=grosor,
                           stroke_linecap="square", stroke_linejoin="miter"))
    return grupo(piezas)


def banda_escalera(x: float, y: float, ancho: float, alto: float,
                   color: str = None, modulo: float | None = None) -> str:
    color = color or C["plata"]
    modulo = modulo or alto * 1.1
    return _banda_rejilla(x, y, ancho, alto, modulo, (12, 13), GRECA_ESCALERA, color, 0.13)


def banda_filete(x: float, y: float, ancho: float, alto: float, color: str = None,
                 color_punto: str = None) -> str:
    """Filete delgado: dos reglas y una hilera de puntos. Sirve para respirar."""
    color = color or C["oro"]
    color_punto = color_punto or C["plata"]
    paso = alto * 1.9
    _, reps = _modulo_exacto(ancho, paso)
    paso = ancho / reps
    piezas = [
        linea(x, y + alto * 0.14, x + ancho, y + alto * 0.14, stroke=color,
              stroke_width=alto * 0.1, opacity=0.9),
        linea(x, y + alto * 0.86, x + ancho, y + alto * 0.86, stroke=color,
              stroke_width=alto * 0.1, opacity=0.9),
    ]
    r = alto * 0.19
    for k in range(reps):
        cx = x + (k + 0.5) * paso
        cy = y + alto / 2
        piezas.append(ruta(polilinea([(cx, cy - r), (cx + r, cy), (cx, cy + r),
                                      (cx - r, cy)], cerrada=True), fill=color_punto))
    return grupo(piezas)


def banda_motivos(x: float, y: float, ancho: float, alto: float, motivo: str,
                  cantidad: int | None = None, escala: float = 0.86,
                  alternar: str | None = None) -> str:
    """Repite un motivo a lo largo de la banda, con separadores de rombo."""
    cantidad = cantidad or max(1, round(ancho / (alto * 1.35)))
    paso = ancho / cantidad
    piezas = []
    for k in range(cantidad):
        cx = x + (k + 0.5) * paso
        cuerpo = alternar if (alternar and k % 2) else motivo
        piezas.append(colocar(cuerpo, cx, y + alto / 2, alto * escala))
    for k in range(1, cantidad):
        cx = x + k * paso
        r = alto * 0.12
        piezas.append(ruta(polilinea([(cx, y + alto / 2 - r), (cx + r, y + alto / 2),
                                      (cx, y + alto / 2 + r), (cx - r, y + alto / 2)],
                                     cerrada=True), fill=C["oro"], opacity=0.75))
    return grupo(piezas)


def banda_remolinos(x: float, y: float, ancho: float, alto: float,
                    cantidad: int | None = None) -> str:
    cantidad = cantidad or max(2, round(ancho / (alto * 1.15)))
    paso = ancho / cantidad
    piezas = []
    for k in range(cantidad):
        cx = x + (k + 0.5) * paso
        piezas.append(colocar(
            espiral_uzumaki(color=C["rojo"] if k % 2 == 0 else C["naranja"],
                            vueltas=1.9, grosor=13),
            cx, y + alto / 2, alto * 0.9, rot=0 if k % 2 == 0 else 180))
    return grupo(piezas)


def banda_rombos_shuriken(x: float, y: float, ancho: float, alto: float,
                          cantidad: int | None = None) -> str:
    cantidad = cantidad or max(2, round(ancho / alto))
    paso = ancho / cantidad
    piezas = [
        linea(x, y + alto * 0.06, x + ancho, y + alto * 0.06, stroke=C["oro"], stroke_width=alto * 0.05),
        linea(x, y + alto * 0.94, x + ancho, y + alto * 0.94, stroke=C["oro"], stroke_width=alto * 0.05),
    ]
    for k in range(cantidad):
        cx = x + (k + 0.5) * paso
        piezas.append(colocar(rombo_zapoteco([C["anil"], C["manta"], C["rojo"]]),
                              cx, y + alto / 2, alto * 0.82))
        piezas.append(colocar(shuriken(color=C["plata"], contorno=C["fondo"]),
                              cx, y + alto / 2, alto * 0.52, rot=k * 15))
    return grupo(piezas)


def banda_nueve_colas(x: float, y: float, ancho: float, alto: float) -> str:
    """Nueve llamas: una por cada cola de Kurama. Remate del ruedo."""
    paso = ancho / 9
    piezas = []
    for k in range(9):
        cx = x + (k + 0.5) * paso
        piezas.append(colocar(llama_kurama(), cx, y + alto * 0.52, alto * 0.95,
                              rot=-6 if k % 2 else 6))
    for k in range(10):
        cx = x + k * paso
        piezas.append(colocar(rombo_zapoteco([C["cochinilla"], C["amarillo"]]),
                              cx, y + alto * 0.86, alto * 0.22))
    return grupo(piezas)


def banda_sellos(x: float, y: float, ancho: float, alto: float, vertical: bool = False,
                 color: str = None, fondo: str = None, paso_rel: float = 1.18,
                 escala: float = 0.84) -> str:
    """Randa: la tira que une dos lienzos, aquí sembrada de sellos de mano.

    En la prenda va con `paso_rel` alto, para que los sellos se lean como
    cuentas separadas y la randa no se convierta en una franja de color que
    parta el huipil en tres.
    """
    color = color or C["oro"]
    fondo = fondo or "#1B1526"
    orden = ["tora", "mi", "hitsuji", "caracol", "inu", "uma"]
    largo = alto if vertical else ancho
    grueso = ancho if vertical else alto
    cantidad = max(1, round(largo / (grueso * paso_rel)))
    paso = largo / cantidad
    piezas = [rectangulo(x, y, ancho, alto, fill=fondo)]
    for k in range(cantidad):
        nombre = orden[k % len(orden)]
        if vertical:
            cx, cy = x + ancho / 2, y + (k + 0.5) * paso
        else:
            cx, cy = x + (k + 0.5) * paso, y + alto / 2
        piezas.append(colocar(sello_mano(nombre, color=color), cx, cy, grueso * escala))
    # El grosor del canto es relativo al de la randa: la banda se dibuja tanto en
    # centímetros (sobre la prenda) como en píxeles (en la lámina de bandas).
    borde = dict(stroke=C["oro"], stroke_width=grueso * 0.055, opacity=0.9)
    if vertical:
        piezas += [linea(x, y, x, y + alto, **borde), linea(x + ancho, y, x + ancho, y + alto, **borde)]
    else:
        piezas += [linea(x, y, x + ancho, y, **borde), linea(x, y + alto, x + ancho, y + alto, **borde)]
    return grupo(piezas)


def banda_nubes(x: float, y: float, ancho: float, alto: float) -> str:
    cantidad = max(2, round(ancho / (alto * 1.08)))
    paso = ancho / cantidad
    piezas = []
    for k in range(cantidad):
        cx = x + (k + 0.5) * paso
        piezas.append(colocar(nube_akatsuki(), cx, y + alto / 2, alto * 0.98))
    return grupo(piezas)


def banda_uchiwa(x: float, y: float, ancho: float, alto: float) -> str:
    cantidad = max(2, round(ancho / (alto * 1.1)))
    paso = ancho / cantidad
    piezas = []
    for k in range(cantidad):
        cx = x + (k + 0.5) * paso
        piezas.append(colocar(uchiwa(), cx, y + alto / 2, alto * 0.88, rot=180 if k % 2 else 0))
    return grupo(piezas)


BANDAS = {
    "greca-hoja": ("B1", "Greca de la hoja", banda_greca_hoja,
                   "Escalera de Mitla y hoja de Konoha alternando en ciclos de tres módulos"),
    "remolinos": ("B2", "Cadena de remolinos", banda_remolinos,
                  "Remolino Uzumaki en alternancia invertida, como el caracol istmeño"),
    "rombos-shuriken": ("B3", "Rombos con shuriken", banda_rombos_shuriken,
                        "Rombo zapoteco con shuriken inscrito; va en sisa y puños"),
    "nueve-colas": ("B4", "Nueve colas", banda_nueve_colas,
                    "Nueve llamas de Kurama: una por cola, para el ruedo"),
    "nubes": ("B5", "Nubes Akatsuki", banda_nubes,
              "Nube roja tratada como el motivo de nube de los lienzos de fiesta"),
    "sellos": ("B6", "Sellos de mano", banda_sellos,
               "Randa de unión entre lienzos, con los sellos tora, mi, hitsuji…"),
    "uchiwa": ("B7", "Abanicos uchiwa", banda_uchiwa,
               "Abanico Uchiha y abanico de palma del Istmo en la misma silueta"),
    "escalera": ("B8", "Escalera de Mitla", banda_escalera,
                 "Escalonado puro, sin cita: respiración entre bandas cargadas"),
    "filete": ("B9", "Filete de puntos", banda_filete,
               "Separador de 1 cm; sin él las bandas cargadas se vuelven ruido"),
}
