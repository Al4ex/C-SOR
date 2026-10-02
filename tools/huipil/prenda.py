"""Geometría y composición de la prenda.

Todo se dibuja en centímetros; quien llame envuelve el resultado en un
`translate(x0,y0) scale(esc)` para pasar a píxeles.

La prenda es un huipil de hombre: tres lienzos de telar de cintura unidos por
randas, doblados por el hombro (sin costura de hombro), con cuello cuadrado y
costados abiertos para la sisa. Es la construcción del huipil istmeño llevada
a un cuerpo masculino: más largo de tiro, más ancho de pecho y sin vuelo.
"""

from __future__ import annotations

from typing import NamedTuple

from . import motivos as M
from .paleta import C, reves
from .svg import circulo, colocar, grupo, linea, polar, rectangulo, ruta


class Medidas(NamedTuple):
    talla: str
    ancho: float          # ancho plano de la prenda
    largo: float          # del doblez de hombro al ruedo
    cuello_ancho: float
    cuello_frente: float
    cuello_espalda: float
    vista: float          # ancho de la vista/banda del cuello
    lienzo_lateral: float
    randa: float
    sisa: float           # profundidad de la abertura de manga
    abertura: float       # abertura lateral del ruedo
    ruedo: float          # alto total de las bandas del ruedo


TALLAS = {
    "M": Medidas("M", 62.0, 78.0, 22.0, 9.0, 3.0, 3.0, 18.2, 1.7, 28.0, 14.0, 19.0),
    "L": Medidas("L", 66.0, 82.0, 24.0, 10.0, 3.5, 3.2, 19.5, 1.8, 30.0, 16.0, 20.0),
    "XL": Medidas("XL", 70.0, 86.0, 25.0, 10.5, 3.5, 3.4, 20.6, 1.9, 32.0, 18.0, 21.0),
}

P = TALLAS["L"]


def lienzo_central(m: Medidas = P) -> float:
    return m.ancho - 2 * m.lienzo_lateral - 2 * m.randa


def randas_x(m: Medidas = P) -> tuple[float, float]:
    return m.lienzo_lateral, m.ancho - m.lienzo_lateral - m.randa


# --------------------------------------------------------------------------
# Piezas de construcción
# --------------------------------------------------------------------------


def tela(m: Medidas = P, fondo: str | None = None) -> str:
    fondo = fondo or C["fondo"]
    return grupo([
        rectangulo(0, 0, m.ancho, m.largo, fill=fondo),
        rectangulo(0, 0, m.ancho, m.largo, fill="url(#trama)"),
        rectangulo(0, 0, m.ancho, m.largo, fill="url(#luzTerciopelo)"),
    ])


def contorno(m: Medidas = P) -> str:
    return rectangulo(0, 0, m.ancho, m.largo, fill="none", stroke=C["oro"],
                      stroke_width=0.16, opacity=0.85)


def randas(m: Medidas = P) -> str:
    a, b = randas_x(m)
    opciones = dict(vertical=True, paso_rel=2.2, escala=0.80)
    return grupo([
        M.banda_sellos(a, 0, m.randa, m.largo, **opciones),
        M.banda_sellos(b, 0, m.randa, m.largo, **opciones),
    ])


def cuello(m: Medidas = P, espalda: bool = False) -> str:
    """Cuello cuadrado con vista bordada: la vista hace de banda ninja."""
    hondo = m.cuello_espalda if espalda else m.cuello_frente
    x1 = (m.ancho - m.cuello_ancho) / 2
    x2 = x1 + m.cuello_ancho
    ox1, ox2 = x1 - m.vista, x2 + m.vista
    oy = hondo + m.vista
    marco = (
        f"M {ox1},0 H {ox2} V {oy} H {ox1} Z "
        f"M {x1},0 H {x2} V {hondo} H {x1} Z"
    )
    piezas = [
        # El hueco deja ver el revés del lienzo, no el papel de la lámina.
        rectangulo(x1, 0, m.cuello_ancho, hondo, fill=reves()),
        rectangulo(x1, 0, m.cuello_ancho, hondo, fill="url(#trama)", opacity=0.7),
        ruta(marco, fill=C["anil"], fill_rule="evenodd", stroke=C["oro"], stroke_width=0.1),
        ruta(marco, fill="url(#trama)", fill_rule="evenodd", opacity=0.45),
    ]
    # Pespunte doble de oro en los dos cantos de la vista, como la correa de la banda.
    for dx in (0.4, 0.72):
        piezas.append(ruta(f"M {ox1 + dx},0 V {oy - dx} H {ox2 - dx} V 0",
                           fill="none", stroke=C["oro"], stroke_width=0.08, opacity=0.85))
    for dx in (0.3, 0.6):
        piezas.append(ruta(f"M {x1 - dx},0 V {hondo + dx} H {x2 + dx} V 0",
                           fill="none", stroke=C["oro"], stroke_width=0.08, opacity=0.85))
    # Remaches de plata en las esquinas, igual que los de la placa metálica.
    for px in (ox1 + m.vista / 2, ox2 - m.vista / 2):
        piezas.append(circulo(px, hondo + m.vista / 2, m.vista * 0.17, fill=C["plata"],
                              stroke=C["fondo"], stroke_width=0.06))
    return grupo(piezas)


def placa_ninja(m: Medidas = P) -> str:
    """Placa hitai-ate al frente, como la lleva puesta un shinobi."""
    hondo = m.cuello_frente + m.vista
    lado = m.cuello_ancho * 0.66
    return colocar(M.hitai_ate(), m.ancho / 2, hondo + lado * 0.33, lado)


def kanji_nuca(m: Medidas = P) -> str:
    hondo = m.cuello_espalda + m.vista
    return colocar(M.kanji_fuego(color=C["oro"]), m.ancho / 2, hondo + 5.4, 9.0)


def ruedo(m: Medidas = P) -> str:
    """Cinco bandas apiladas; de arriba a abajo, de lo abstracto a lo narrativo."""
    y = m.largo - m.ruedo
    alturas = [
        (1.1, M.banda_filete),
        (7.0, M.banda_greca_hoja),
        (1.1, lambda x, yy, w, h: M.banda_filete(x, yy, w, h, color=C["plata"],
                                                 color_punto=C["oro"])),
        (8.4, M.banda_nueve_colas),
        (3.4, M.banda_rombos_shuriken),
    ]
    total = sum(a for a, _ in alturas)
    escala = m.ruedo / total
    piezas = [linea(0, y, m.ancho, y, stroke=C["oro"], stroke_width=0.14, opacity=0.8)]
    for alto, fn in alturas:
        h = alto * escala
        piezas.append(fn(0, y, m.ancho, h))
        y += h
    return grupo(piezas)


def orillas(m: Medidas = P) -> str:
    """Dobladillos de sisa y aberturas laterales del ruedo."""
    guia = dict(fill="none", stroke=C["plata"], stroke_width=0.1, opacity=0.65)
    piezas = []
    for x in (0.9, m.ancho - 0.9):
        piezas.append(ruta(f"M {x},0 V {m.sisa}", **guia))
        piezas.append(ruta(f"M {x},{m.largo - m.abertura} V {m.largo}",
                           stroke_dasharray="1.2 0.8", **guia))
    piezas.append(ruta(f"M 0,{m.largo - 0.9} H {m.ancho}", **guia))
    return grupo(piezas)


# --------------------------------------------------------------------------
# Vistas
# --------------------------------------------------------------------------


def registros_frente(m: Medidas = P) -> dict[str, float]:
    """Alturas de los cuatro registros del frente, medidas desde el doblez."""
    libre_desde = m.cuello_frente + m.vista
    libre_hasta = m.largo - m.ruedo
    return {
        "placa": libre_desde + m.cuello_ancho * 0.66 * 0.33,
        "flores": libre_desde + 18.8,
        "abanicos": libre_hasta - 13.0,
        "sembrado": libre_hasta - 4.2,
        "ruedo": libre_hasta,
    }


def frente(m: Medidas = P) -> str:
    cx = m.ancho / 2
    izq = m.lienzo_lateral / 2
    der = m.ancho - m.lienzo_lateral / 2
    r = registros_frente(m)
    piezas = [tela(m)]

    # Registro de flores grandes: dos sharingan flanqueando un rinnegan.
    piezas.append(colocar(M.rosa_sharingan(), izq, r["flores"], m.lienzo_lateral * 0.92))
    piezas.append(colocar(M.rosa_sharingan(), der, r["flores"], m.lienzo_lateral * 0.92))
    piezas.append(colocar(M.rosa_rinnegan(), cx, r["flores"], lienzo_central(m) * 0.78))

    # Registro de abanicos: dos uchiwa y un kunai que marca el eje del lienzo.
    y2 = r["abanicos"]
    piezas.append(colocar(M.flor_istmena(), izq, y2, m.lienzo_lateral * 0.60))
    piezas.append(colocar(M.flor_istmena(), der, y2, m.lienzo_lateral * 0.60))
    piezas.append(colocar(M.uchiwa(), cx - 5.6, y2 - 0.6, 9.6, rot=-14))
    piezas.append(colocar(M.uchiwa(), cx + 5.6, y2 - 0.6, 9.6, rot=14))
    piezas.append(colocar(M.kunai(), cx, y2 + 4.4, 7.6))

    # Sembrado menudo: lo que en el huipil rellena el fondo entre flores.
    for mx, rot in ((izq - 7.0, 0), (izq + 7.0, 45), (der - 7.0, 45), (der + 7.0, 0)):
        piezas.append(colocar(M.shuriken(), mx, r["flores"] + 9.6, 4.4, rot=rot))
    for mx, rot in ((cx - 8.4, 18), (cx + 8.4, -18)):
        piezas.append(colocar(M.shuriken(), mx, r["flores"] - 10.4, 3.8, rot=rot))
    for mx in (izq, der, cx):
        piezas.append(colocar(M.nube_akatsuki(), mx, r["sembrado"], 7.4))

    piezas += [ruedo(m), randas(m), cuello(m), placa_ninja(m), orillas(m), contorno(m)]
    return grupo(piezas)


def registros_espalda(m: Medidas = P) -> dict[str, float]:
    libre_hasta = m.largo - m.ruedo
    y_nubes = m.cuello_espalda + m.vista + 10.0
    diam = m.ancho * 0.41
    return {
        "kanji": m.cuello_espalda + m.vista + 5.4,
        "nubes": y_nubes,
        "alto_nubes": 6.4,
        "medallon": libre_hasta - diam / 2 - 3.4,
        "diametro": diam,
        "satelites": diam / 2 + 4.4,
        "ruedo": libre_hasta,
    }


def espalda(m: Medidas = P) -> str:
    cx = m.ancho / 2
    izq = m.lienzo_lateral / 2
    der = m.ancho - m.lienzo_lateral / 2
    r = registros_espalda(m)
    piezas = [tela(m)]

    piezas.append(M.banda_nubes(0, r["nubes"], m.ancho, r["alto_nubes"]))

    # Medallón del remolino sobre el omóplato, como el del chaleco chūnin.
    y_med, diam = r["medallon"], r["diametro"]
    piezas.append(circulo(cx, y_med, diam * 0.45 + 1.0, fill="none", stroke=C["oro"],
                          stroke_width=0.18, opacity=0.8))
    # Los satélites nunca se rotan: un rombo girado 45° deja de ser rombo.
    for k in range(8):
        px, py = polar(cx, y_med, r["satelites"], k * 45 - 90)
        if 1.0 < px < m.ancho - 1.0:
            piezas.append(colocar(M.uchiwa() if k % 2 == 0 else M.rombo_zapoteco(),
                                  px, py, 6.0))
    piezas.append(colocar(M.espiral_uzumaki(pasos=260), cx, y_med, diam))

    y_lados = r["nubes"] + r["alto_nubes"] + 7.4
    for mx in (izq, der):
        piezas.append(colocar(M.flor_istmena(), mx, y_lados, m.lienzo_lateral * 0.50))
        piezas.append(colocar(M.rombo_zapoteco([C["cochinilla"], C["amarillo"]]),
                              mx, y_lados + 11.0, 4.8))
        piezas.append(colocar(M.shuriken(), mx, y_med + diam / 2 - 1.0, 4.6, rot=22))

    piezas += [ruedo(m), randas(m), cuello(m, espalda=True), kanji_nuca(m),
               orillas(m), contorno(m)]
    return grupo(piezas)


def tira_de_telar(m: Medidas = P) -> str:
    """Despiece: la tira continua del telar, doblada por el hombro."""
    largo = m.largo * 2
    x1 = (m.ancho - m.cuello_ancho) / 2
    piezas = [
        rectangulo(0, 0, m.ancho, largo, fill=C["fondo"]),
        rectangulo(0, 0, m.ancho, largo, fill="url(#trama)"),
    ]
    a, b = randas_x(m)
    for x in (a, b):
        piezas.append(rectangulo(x, 0, m.randa, largo, fill=C["anil"], opacity=0.9))
        piezas.append(linea(x, 0, x, largo, stroke=C["oro"], stroke_width=0.12))
        piezas.append(linea(x + m.randa, 0, x + m.randa, largo, stroke=C["oro"],
                            stroke_width=0.12))
    piezas.append(rectangulo(x1, m.largo - m.cuello_espalda, m.cuello_ancho,
                             m.cuello_espalda + m.cuello_frente, fill="#07060A",
                             stroke=C["plata"], stroke_width=0.16))
    piezas.append(linea(0, m.largo, m.ancho, m.largo, stroke=C["plata"],
                        stroke_width=0.2, stroke_dasharray="2 1.4"))
    piezas.append(rectangulo(0, 0, m.ancho, largo, fill="none", stroke=C["oro"],
                             stroke_width=0.2))
    return grupo(piezas)
