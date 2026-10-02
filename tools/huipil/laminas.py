"""Armado de las láminas del cuaderno de diseño."""

from __future__ import annotations

import math
from typing import Callable, Sequence

from . import motivos as M
from . import prenda as PR
from .paleta import C, GUIA, PALETA, PAPEL, PAPEL_CLARO, TINTA, TINTA_SUAVE, VARIANTES, variante
from .svg import (
    TIPO,
    TIPO_MONO,
    TIPO_TITULO,
    circulo,
    colocar,
    documento,
    grupo,
    linea,
    n,
    polilinea,
    rectangulo,
    ruta,
    texto,
)

PROYECTO = "HUIPIL ISTMEÑO SHINOBI"
AUTORIA = "Cuaderno de diseño textil · Istmo de Tehuantepec × Konohagakure"

DEFS = f"""
  <pattern id="trama" width="0.42" height="0.42" patternUnits="userSpaceOnUse">
    <path d="M0 0.105 H0.42" stroke="#FFFFFF" stroke-opacity="0.06" stroke-width="0.21"/>
    <path d="M0.105 0 V0.42" stroke="#000000" stroke-opacity="0.18" stroke-width="0.21"/>
  </pattern>
  <linearGradient id="luzTerciopelo" x1="0" y1="0" x2="0.65" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.10"/>
    <stop offset="0.38" stop-color="#FFFFFF" stop-opacity="0.015"/>
    <stop offset="1" stop-color="#000000" stop-opacity="0.30"/>
  </linearGradient>
  <radialGradient id="vineta" cx="0.5" cy="0.42" r="0.78">
    <stop offset="0" stop-color="{PAPEL_CLARO}"/>
    <stop offset="1" stop-color="{PAPEL}"/>
  </radialGradient>
"""


# --------------------------------------------------------------------------
# Elementos comunes de lámina
# --------------------------------------------------------------------------


def envolver(cadena: str, ancho: int) -> list[str]:
    lineas: list[str] = []
    actual = ""
    for palabra in cadena.split():
        if not actual or len(actual) + len(palabra) + 1 <= ancho:
            actual = f"{actual} {palabra}".strip()
        else:
            lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


def parrafo(x: float, y: float, cadena: str, ancho: int = 58, tam: float = 15,
            interlinea: float = 1.45, color: str = TINTA_SUAVE, familia: str = TIPO,
            anclaje: str = "start") -> str:
    piezas = []
    for i, linea_txt in enumerate(envolver(cadena, ancho)):
        piezas.append(texto(x, y + i * tam * interlinea, linea_txt, tam=tam,
                            color=color, familia=familia, anclaje=anclaje))
    return grupo(piezas)


def marco(ancho: float, alto: float, codigo: str, titulo: str, subtitulo: str,
          cuerpo: str, pie: str = "") -> str:
    piezas = [
        rectangulo(0, 0, ancho, alto, fill="url(#vineta)"),
        rectangulo(22, 22, ancho - 44, alto - 44, fill="none", stroke=GUIA, stroke_width=1.4),
        rectangulo(28, 28, ancho - 56, alto - 56, fill="none", stroke=C["oro"],
                   stroke_width=0.8, opacity=0.4),
        texto(60, 86, PROYECTO, tam=20, color=C["oro"], espaciado=5.5, peso="bold"),
        texto(60, 134, titulo, tam=42, color=TINTA, familia=TIPO_TITULO),
        texto(60, 164, subtitulo, tam=16, color=TINTA_SUAVE, italica=True),
        linea(60, 186, ancho - 60, 186, stroke=C["oro"], stroke_width=1.2, opacity=0.55),
        texto(ancho - 60, 86, codigo, tam=20, color=TINTA_SUAVE, anclaje="end",
              familia=TIPO_MONO, espaciado=2.0),
        linea(60, alto - 72, ancho - 60, alto - 72, stroke=GUIA, stroke_width=1.0),
        texto(60, alto - 46, AUTORIA, tam=13, color=TINTA_SUAVE),
        texto(ancho - 60, alto - 46, pie or "Dibujo vectorial generado con Python",
              tam=13, color=TINTA_SUAVE, anclaje="end"),
        cuerpo,
    ]
    return documento(ancho, alto, grupo(piezas), defs=DEFS)


def llamada(numero: int, x: float, y: float, hacia: tuple[float, float] | None = None,
            r: float = 14) -> str:
    piezas = []
    if hacia:
        piezas.append(linea(x, y, hacia[0], hacia[1], stroke=C["oro"], stroke_width=1.0,
                            opacity=0.55, stroke_dasharray="4 3"))
        piezas.append(circulo(hacia[0], hacia[1], 3.0, fill=C["oro"], opacity=0.8))
    piezas += [
        circulo(x, y, r, fill=PAPEL, stroke=C["oro"], stroke_width=1.3, opacity=0.95),
        texto(x, y + 5, str(numero), tam=14, color=C["oro"], anclaje="middle", peso="bold"),
    ]
    return grupo(piezas)


def lista_llamadas(x: float, y: float, entradas: Sequence[tuple[int, str, str]],
                   ancho_txt: int = 46, paso: float = 0) -> str:
    piezas = []
    cursor = y
    for numero, titulo, detalle in entradas:
        piezas.append(circulo(x + 13, cursor - 5, 13, fill="none", stroke=C["oro"],
                              stroke_width=1.2))
        piezas.append(texto(x + 13, cursor, str(numero), tam=13, color=C["oro"],
                            anclaje="middle", peso="bold"))
        piezas.append(texto(x + 38, cursor, titulo, tam=16, color=TINTA, peso="bold"))
        lineas = envolver(detalle, ancho_txt)
        for i, ln in enumerate(lineas):
            piezas.append(texto(x + 38, cursor + 21 + i * 19, ln, tam=14, color=TINTA_SUAVE))
        cursor += 30 + len(lineas) * 19 + (paso or 14)
    return grupo(piezas)


def cota_h(x1: float, x2: float, y: float, etiqueta: str, color: str = TINTA_SUAVE,
           arriba: bool = True) -> str:
    f = 7
    return grupo([
        linea(x1, y, x2, y, stroke=color, stroke_width=1.0),
        ruta(polilinea([(x1 + f, y - 4), (x1, y), (x1 + f, y + 4)]), fill="none",
             stroke=color, stroke_width=1.0),
        ruta(polilinea([(x2 - f, y - 4), (x2, y), (x2 - f, y + 4)]), fill="none",
             stroke=color, stroke_width=1.0),
        texto((x1 + x2) / 2, y - 8 if arriba else y + 18, etiqueta, tam=14, color=color,
              anclaje="middle", familia=TIPO_MONO),
    ])


def cota_v(y1: float, y2: float, x: float, etiqueta: str, color: str = TINTA_SUAVE,
           derecha: bool = True) -> str:
    f = 7
    return grupo([
        linea(x, y1, x, y2, stroke=color, stroke_width=1.0),
        ruta(polilinea([(x - 4, y1 + f), (x, y1), (x + 4, y1 + f)]), fill="none",
             stroke=color, stroke_width=1.0),
        ruta(polilinea([(x - 4, y2 - f), (x, y2), (x + 4, y2 - f)]), fill="none",
             stroke=color, stroke_width=1.0),
        texto(x + 10 if derecha else x - 10, (y1 + y2) / 2 + 5, etiqueta, tam=14,
              color=color, anclaje="start" if derecha else "end", familia=TIPO_MONO),
    ])


def tabla(x: float, y: float, encabezados: Sequence[str], filas: Sequence[Sequence[str]],
          anchos: Sequence[float], alto_fila: float = 30, tam: float = 14) -> str:
    piezas = []
    total = sum(anchos)
    piezas.append(rectangulo(x, y - alto_fila + 8, total, alto_fila, fill=C["oro"],
                             opacity=0.14))
    cx = x
    for h, w in zip(encabezados, anchos):
        piezas.append(texto(cx + 10, y, h, tam=tam, color=C["oro"], peso="bold"))
        cx += w
    for j, fila in enumerate(filas):
        yy = y + (j + 1) * alto_fila
        if j % 2 == 0:
            piezas.append(rectangulo(x, yy - alto_fila + 8, total, alto_fila,
                                     fill=TINTA, opacity=0.035))
        cx = x
        for celda, w in zip(fila, anchos):
            piezas.append(texto(cx + 10, yy, celda, tam=tam, color=TINTA_SUAVE,
                                familia=TIPO_MONO))
            cx += w
    piezas.append(rectangulo(x, y - alto_fila + 8, total, alto_fila * (len(filas) + 1),
                             fill="none", stroke=GUIA, stroke_width=1.0))
    return grupo(piezas)


def lienzo_prenda(contenido: str, x0: float, y0: float, esc: float) -> str:
    return grupo(contenido, transform=f"translate({n(x0)},{n(y0)}) scale({n(esc)})")


def a_px(x0: float, y0: float, esc: float) -> Callable[[float, float], tuple[float, float]]:
    return lambda X, Y: (x0 + X * esc, y0 + Y * esc)


# --------------------------------------------------------------------------
# L00 · Paleta y simbología
# --------------------------------------------------------------------------


FICHAS = [
    ("Hoja de Konoha", "xicalcoliuhqui", lambda: M.hoja_konoha(),
     "La espiral de la hoja es la misma espiral escalonada de Mitla: el emblema entra al huipil sin disfraz."),
    ("Remolino Uzumaki", "caracol de mar", lambda: M.espiral_uzumaki(),
     "Va al centro de la espalda, donde el chaleco chūnin lo lleva y donde el huipil lleva su medallón."),
    ("Sharingan", "rosa de cadenilla", lambda: M.rosa_sharingan(),
     "Las tres comas ocupan el corazón amarillo de la rosa istmeña; los pétalos son de seda floja."),
    ("Rinnegan", "ojo de dios", lambda: M.rosa_rinnegan(),
     "Anillos concéntricos dentro del rombo: el ojo del clan y el ojo tejido comparten estructura."),
    ("Uchiwa", "abanico de palma", lambda: M.uchiwa(),
     "El abanico Uchiha y el abanico de palma del Istmo tienen la misma silueta de medio círculo."),
    ("Shuriken", "estrella de rombos", lambda: M.shuriken(),
     "Relleno menudo entre flores, y banda de sisa y puños. Cuatro hojas, nunca más."),
    ("Kunai", "punta de lanza", lambda: M.kunai(),
     "Un solo kunai, vertical, bajo la placa: marca el eje del lienzo central."),
    ("Nube Akatsuki", "nube de lluvia", lambda: M.nube_akatsuki(),
     "La nube roja se vuelve el motivo de lluvia que cruza la línea del hombro en la espalda."),
    ("Cola de Kurama", "voluta de fuego", lambda: M.llama_kurama(),
     "Nueve llamas en el ruedo, una por cola. Es la banda que se lee al caminar."),
    ("Kanji 火 (hi)", "fuego del Hokage", lambda: M.kanji_fuego(),
     "Cuatro trazos de cadenilla de oro en la nuca, justo debajo de la vista del cuello."),
    ("Hitai-ate", "vista del cuello", lambda: M.hitai_ate(),
     "La banda ninja no se cuelga: se convierte en la vista del cuello cuadrado."),
    ("Sello de mano", "greca de caracol", lambda: M.sello_mano("caracol", color=C["amarillo"]),
     "Los sellos se cuentan en rejilla, como el punto de cruz; van en la randa."),
    ("Rombo zapoteco", "rombo del Istmo", lambda: M.rombo_zapoteco(),
     "Motivo local sin cita externa: sostiene y separa a los demás."),
    ("Rosa istmeña", "flor de cadenilla", lambda: M.flor_istmena(),
     "La flor de siempre. Sin ella la prenda dejaría de ser un huipil."),
    ("Greca de la hoja", "banda B1", lambda: None,
     "Síntesis del proyecto: dos escaleras de Mitla y una hoja, de tres en tres."),
]


def lamina_00() -> str:
    ancho, alto = 1700, 1250
    piezas = []

    # Columna de paleta.
    x = 60
    y = 248
    piezas.append(texto(x, y - 36, "PALETA Y CORRESPONDENCIA DE HILOS", tam=16,
                        color=C["oro"], espaciado=2.4, peso="bold"))
    for tinte in PALETA:
        piezas.append(rectangulo(x, y - 22, 56, 40, fill=tinte.hex, stroke=GUIA,
                                 stroke_width=1.0, rx=3))
        piezas.append(texto(x + 70, y - 3, tinte.nombre, tam=15.5, color=TINTA, peso="bold"))
        piezas.append(texto(x + 70, y + 15, f"{tinte.hex} · {tinte.hilo}", tam=11.5,
                            color=TINTA_SUAVE, familia=TIPO_MONO))
        piezas.append(parrafo(x + 352, y - 2, tinte.lectura, ancho=33, tam=12,
                              interlinea=1.4))
        y += 56

    piezas.append(parrafo(
        60, y + 34,
        "Regla de color: el fondo manda. El naranja de Naruto entra en el lugar que el "
        "huipil istmeño reserva al amarillo de los pétalos, y el rojo Uzumaki en el de la "
        "grana. Ningún tinte se añade por ser «de Naruto»: cada uno sustituye a uno que "
        "ya estaba en el huipil.",
        ancho=62, tam=14))

    # Rejilla de fichas de motivos.
    x0, y0 = 700, 222
    cols, paso_x, paso_y = 5, 196, 306
    for i, (nombre, lectura, dibujo, nota) in enumerate(FICHAS):
        cx = x0 + (i % cols) * paso_x
        cy = y0 + (i // cols) * paso_y
        piezas.append(rectangulo(cx, cy, 176, 282, fill=C["fondo"], stroke=GUIA,
                                 stroke_width=1.0, rx=5))
        piezas.append(rectangulo(cx, cy, 176, 282, fill="none", stroke=C["oro"],
                                 stroke_width=0.8, opacity=0.3, rx=5))
        arte = dibujo()
        if arte is None:
            piezas.append(M.banda_greca_hoja(cx + 12, cy + 38, 152, 68, modulo=76))
        else:
            piezas.append(colocar(arte, cx + 88, cy + 72, 124))
        piezas.append(texto(cx + 88, cy + 164, nombre, tam=15, color=TINTA,
                            anclaje="middle", peso="bold"))
        piezas.append(texto(cx + 88, cy + 184, f"→ {lectura}", tam=13, color=C["oro"],
                            anclaje="middle", italica=True))
        piezas.append(parrafo(cx + 88, cy + 210, nota, ancho=27, tam=11.5,
                              interlinea=1.42, anclaje="middle"))

    return marco(ancho, alto, "L-00", "Paleta y simbología",
                 "Qué símbolo de Naruto ocupa el lugar de qué motivo istmeño, y por qué",
                 grupo(piezas))


# --------------------------------------------------------------------------
# L01 / L02 · Vistas de frente y espalda
# --------------------------------------------------------------------------


LLAMADAS_FRENTE = [
    (1, "Vista de cuello cuadrado", "Añil con pespunte de oro y remaches de plata: la banda ninja se vuelve el acabado del cuello."),
    (2, "Placa hitai-ate", "Hilo metálico laminado con la hoja de Konoha grabada. Única pieza que imita metal."),
    (3, "Rosa con corazón de sharingan", "Ø 18 cm. Ocho pétalos de seda floja y el ojo donde iría el corazón amarillo."),
    (4, "Rinnegan en marco de rombo", "Ø 18 cm en el lienzo central. Seis anillos concéntricos leídos como ojo de dios."),
    (5, "Randa de sellos de mano", "Las dos tiras que unen los lienzos, sembradas de sellos: tora, mi, hitsuji, caracol, inu, uma."),
    (6, "Abanicos uchiwa y kunai", "Dos abanicos del clan Uchiha y un kunai que marca el eje del lienzo central."),
    (7, "Greca de la hoja (B1)", "Banda de 7 cm: dos escaleras de Mitla y una hoja de Konoha, de tres en tres."),
    (8, "Nueve colas de Kurama", "Banda de 8.4 cm con nueve volutas de fuego, una por cola. Es lo que se ve al caminar."),
    (9, "Sisa abierta de 30 cm", "Sin manga montada: el costado simplemente no se cose, como en el huipil de lienzos."),
    (10, "Abertura lateral de 16 cm", "Da paso a la zancada y deja caer el ruedo recto, sin arrugar el bordado."),
]

LLAMADAS_ESPALDA = [
    (1, "Doblez de telar", "No hay costura de hombro: la tira tejida se dobla a la mitad, como en el huipil."),
    (2, "Kanji 火 (hi, fuego)", "En la nuca, en cadenilla de oro. La marca del Hokage remata el cuello por detrás."),
    (3, "Banda de nubes Akatsuki", "Cruza la línea del hombro. La nube roja entra como motivo de lluvia de fiesta."),
    (4, "Medallón del remolino", "Ø 27 cm de espiral Uzumaki. Se borda al final, y por eso cruza las randas sin cortarse."),
    (5, "Corona de satélites", "Ocho piezas alternas, abanico y rombo, como los rayos de una flor grande."),
    (6, "Lienzos laterales ligeros", "Flor istmeña y shuriken nada más: no deben competir con el medallón."),
    (7, "Secuencia del ruedo", "Filete · greca de la hoja · filete · nueve colas · rombos con shuriken."),
    (8, "Cuello cuadrado de 3.5 cm", "Caída trasera corta: el peso del bordado queda al frente, donde se ve."),
]


def _lamina_vista(codigo: str, titulo: str, subtitulo: str, contenido: str,
                  entradas, puntos, pie: str) -> str:
    ancho, alto = 1320, 1120
    esc = 9.1
    x0, y0 = 72, 212
    p = a_px(x0, y0, esc)
    piezas = [lienzo_prenda(contenido, x0, y0, esc)]
    for numero, (cmx, cmy, dx, dy) in puntos.items():
        tx, ty = p(cmx, cmy)
        piezas.append(llamada(numero, tx + dx, ty + dy, hacia=(tx, ty)))
    piezas.append(lista_llamadas(742, 252, list(entradas), ancho_txt=58, paso=12))
    piezas.append(linea(716, 212, 716, alto - 100, stroke=GUIA, stroke_width=1.0))
    return marco(ancho, alto, codigo, titulo, subtitulo, grupo(piezas), pie=pie)


def lamina_01() -> str:
    m = PR.P
    cx = m.ancho / 2
    r = PR.registros_frente(m)
    puntos = {
        1: (cx - m.cuello_ancho / 2 - m.vista / 2, 3.2, -46, -14),
        2: (cx + 5.0, r["placa"], 54, -40),
        3: (m.lienzo_lateral / 2, r["flores"], -44, 0),
        4: (cx, r["flores"] + 6.4, 56, 14),
        5: (m.lienzo_lateral + m.randa / 2, 41.0, -58, 8),
        6: (cx + 5.6, r["abanicos"], 54, 10),
        7: (m.ancho * 0.74, r["ruedo"] + 4.6, 50, -16),
        8: (cx, r["ruedo"] + 13.4, 62, 18),
        9: (0.9, 16.0, -44, -10),
        10: (m.ancho - 0.9, m.largo - 6.0, 46, 16),
    }
    return _lamina_vista(
        "L-01", "Frente", "Huipil de hombre, talla L · tres lienzos de telar de cintura",
        PR.frente(m), LLAMADAS_FRENTE, puntos,
        "Proporciones a escala · medidas en cm")


def lamina_02() -> str:
    m = PR.P
    cx = m.ancho / 2
    r = PR.registros_espalda(m)
    sat = r["satelites"] * math.cos(math.radians(45))
    puntos = {
        1: (m.ancho * 0.2, 0.8, -46, -20),
        2: (cx, r["kanji"], 46, -34),
        3: (m.ancho * 0.8, r["nubes"] + r["alto_nubes"] / 2, 52, -14),
        4: (cx, r["medallon"], 60, -4),
        5: (cx + sat, r["medallon"] - sat, 48, 18),
        6: (m.lienzo_lateral / 2, r["nubes"] + r["alto_nubes"] + 7.2, -44, 2),
        7: (m.ancho * 0.3, r["ruedo"] + 10.0, -48, 22),
        8: (cx - m.cuello_ancho / 2, 2.4, -34, -26),
    }
    return _lamina_vista(
        "L-02", "Espalda", "Medallón del remolino sobre el omóplato · randas continuas",
        PR.espalda(m), LLAMADAS_ESPALDA, puntos,
        "Proporciones a escala · medidas en cm")


# --------------------------------------------------------------------------
# L03 · Patrón, medidas y secuencia de confección
# --------------------------------------------------------------------------


def lamina_03() -> str:
    ancho, alto = 1740, 1260
    m = PR.P
    piezas = []
    a, b = PR.randas_x(m)

    # A · Despiece: la tira continua del telar.
    esc_t = 4.05
    xt, yt = 92, 304
    pt = a_px(xt, yt, esc_t)
    piezas.append(texto(xt, yt - 46, "A · TIRA DE TELAR, VISTA PLANA", tam=16,
                        color=C["oro"], espaciado=2.0, peso="bold"))
    piezas.append(lienzo_prenda(PR.tira_de_telar(m), xt, yt, esc_t))
    piezas += [
        cota_h(pt(0, 0)[0], pt(m.ancho, 0)[0], yt - 20, f"{m.ancho:.0f} cm"),
        cota_v(yt, pt(0, m.largo * 2)[1], pt(m.ancho, 0)[0] + 46, f"{m.largo * 2:.0f} cm"),
        cota_v(yt, pt(0, m.largo)[1], pt(0, 0)[0] - 36, f"{m.largo:.0f}", derecha=False),
        texto(pt(m.ancho / 2, 0)[0], pt(0, m.largo)[1] - 10, "doblez de hombro", tam=13,
              color=C["plata"], anclaje="middle", italica=True),
        texto(pt(m.ancho / 2, 0)[0], pt(0, m.largo * 2)[1] + 30,
              f"lienzos {m.lienzo_lateral:.1f} + {PR.lienzo_central(m):.1f} + "
              f"{m.lienzo_lateral:.1f} cm", tam=13, color=TINTA_SUAVE, anclaje="middle"),
        texto(pt(m.ancho / 2, 0)[0], pt(0, m.largo * 2)[1] + 50,
              f"más dos randas de {m.randa:.1f} cm", tam=13, color=C["oro"],
              anclaje="middle", italica=True),
    ]
    for x in (a + m.randa / 2, b + m.randa / 2):
        piezas.append(texto(pt(x, 0)[0], yt + 24, "randa", tam=11, color=C["oro"],
                            anclaje="middle"))

    # B · Plano acotado, sin bordado figurativo.
    esc_f = 5.2
    xf, yf = 520, 304
    pf = a_px(xf, yf, esc_f)
    x1 = (m.ancho - m.cuello_ancho) / 2
    piezas.append(texto(xf, yf - 46, "B · PLANO ACOTADO (TALLA L)", tam=16,
                        color=C["oro"], espaciado=2.0, peso="bold"))
    piezas.append(lienzo_prenda(grupo([
        PR.tela(m), PR.ruedo(m), PR.randas(m), PR.cuello(m), PR.placa_ninja(m),
        PR.orillas(m), PR.contorno(m),
    ]), xf, yf, esc_f))
    piezas += [
        cota_h(pf(0, 0)[0], pf(m.ancho, 0)[0], yf - 20, f"{m.ancho:.0f}"),
        cota_h(pf(x1, 0)[0], pf(x1 + m.cuello_ancho, 0)[0], pf(0, 30.0)[1],
               f"cuello {m.cuello_ancho:.0f}", arriba=False),
        cota_v(pf(0, 0)[1], pf(0, m.largo)[1], pf(m.ancho, 0)[0] + 112, f"{m.largo:.0f}"),
        cota_v(pf(0, 0)[1], pf(0, m.sisa)[1], pf(0, 0)[0] - 36, f"sisa {m.sisa:.0f}",
               derecha=False),
        cota_v(pf(0, m.largo - m.abertura)[1], pf(0, m.largo)[1], pf(0, 0)[0] - 36,
               f"ab. {m.abertura:.0f}", derecha=False),
        cota_v(pf(0, m.largo - m.ruedo)[1], pf(0, m.largo)[1], pf(m.ancho, 0)[0] + 42,
               f"ruedo {m.ruedo:.0f}"),
        cota_v(pf(0, 0)[1], pf(0, m.cuello_frente)[1], pf(x1, 0)[0] + 14,
               f"{m.cuello_frente:.0f}"),
    ]

    # E · Consumos, debajo del plano acotado.
    ye = yf + m.largo * esc_f + 92
    piezas.append(texto(xf, ye, "E · CONSUMOS ESTIMADOS", tam=16, color=C["oro"],
                        espaciado=2.0, peso="bold"))
    piezas.append(tabla(xf, ye + 48, ["Material", "Cantidad"],
                        [["Algodón de telar, trama fina", "3 lienzos · 1.64 m c/u"],
                         ["Terciopelo de forro (vista)", "0.25 m"],
                         ["Seda floja, 7 colores", "ovillo de 20 g c/u"],
                         ["Hilo metálico laminado", "2 ovillos"],
                         ["Hilo de oro entorchado", "3 ovillos"]],
                        [300, 232]))

    # C · Tallas.
    xtab = 1024
    piezas.append(texto(xtab, 258, "C · CUADRO DE TALLAS (cm)", tam=16, color=C["oro"],
                        espaciado=2.0, peso="bold"))
    filas = []
    for clave in ("M", "L", "XL"):
        t = PR.TALLAS[clave]
        filas.append([t.talla, f"{t.ancho:.0f}", f"{t.largo:.0f}", f"{t.cuello_ancho:.0f}",
                      f"{t.sisa:.0f}", f"{t.abertura:.0f}", f"{t.ruedo:.0f}"])
    piezas.append(tabla(xtab, 306,
                        ["Talla", "Ancho", "Largo", "Cuello", "Sisa", "Abert.", "Ruedo"],
                        filas, [80, 80, 80, 84, 72, 78, 72]))

    # D · Secuencia de confección.
    piezas.append(texto(xtab, 488, "D · SECUENCIA DE CONFECCIÓN", tam=16, color=C["oro"],
                        espaciado=2.0, peso="bold"))
    pasos = [
        "Tejer en telar de cintura tres lienzos de 164 cm de largo: dos de 19.5 cm y uno de 23.4 cm.",
        "Bordar cada lienzo suelto en bastidor: rosas, abanicos y las cinco bandas del ruedo. El lienzo plano se borda mejor que la prenda armada.",
        "Unir los lienzos con randa de 1.8 cm a punto de ojal, sembrando los sellos de mano sobre la propia randa.",
        "Doblar la tira a la mitad y cerrar los costados desde 30 cm bajo el doblez hasta 16 cm antes del ruedo.",
        "Cortar el cuello cuadrado, aplicar la vista de añil, pespuntear el oro y remachar la plata.",
        "Bordar la placa hitai-ate al frente y el kanji 火 en la nuca, ya con la vista puesta.",
        "Dejar para el final el medallón del remolino: cruza las dos randas y sólo queda continuo si se borda sobre la prenda armada.",
        "Lavar a mano en frío, planchar del revés sobre paño y guardar en doblez, nunca en gancho.",
    ]
    cursor = 530
    for i, paso in enumerate(pasos, start=1):
        piezas.append(texto(xtab, cursor, f"{i:02d}", tam=14, color=C["oro"],
                            familia=TIPO_MONO, peso="bold"))
        lineas = envolver(paso, 62)
        for j, ln in enumerate(lineas):
            piezas.append(texto(xtab + 36, cursor + j * 20, ln, tam=14, color=TINTA_SUAVE))
        cursor += len(lineas) * 20 + 16

    piezas.append(parrafo(
        xtab, cursor + 24,
        "El orden importa: todo lo que se puede bordar en plano se borda en plano. "
        "Sólo lo que debe cruzar una randa —el medallón de la espalda— se deja para "
        "cuando la prenda ya está armada.",
        ancho=62, tam=14, color=TINTA))

    return marco(ancho, alto, "L-03", "Patrón y confección",
                 "Despiece del telar, plano acotado, tallas y orden de bordado",
                 grupo(piezas), pie="Medidas en cm · sin margen de costura")


# --------------------------------------------------------------------------
# L04 · Biblioteca de bandas
# --------------------------------------------------------------------------


def lamina_04() -> str:
    ancho, alto = 1460, 1800
    piezas = []
    x, y = 100, 248
    w = ancho - 2 * x
    for clave in ("greca-hoja", "remolinos", "rombos-shuriken", "nueve-colas",
                  "nubes", "sellos", "uchiwa", "escalera", "filete"):
        codigo, nombre, fn, nota = M.BANDAS[clave]
        alto_banda = 48 if clave == "filete" else 92
        piezas.append(texto(x, y - 14, f"{codigo} · {nombre}", tam=18, color=TINTA,
                            peso="bold"))
        piezas.append(texto(x + w, y - 14, nota, tam=13.5, color=TINTA_SUAVE,
                            anclaje="end", italica=True))
        piezas.append(rectangulo(x, y, w, alto_banda, fill=C["fondo"]))
        piezas.append(fn(x, y, w, alto_banda))
        piezas.append(rectangulo(x, y, w, alto_banda, fill="none", stroke=C["oro"],
                                 stroke_width=1.0, opacity=0.45))
        y += alto_banda + 62

    piezas.append(parrafo(
        x, y + 12,
        "Las nueve bandas comparten módulo: cualquiera se puede sustituir por otra sin "
        "rehacer la prenda, porque todas repiten en función de su propio alto. La B8 y la "
        "B9 existen para dejar respirar a las demás; sin bandas vacías el huipil se vuelve "
        "ruido. El orden del ruedo va de lo abstracto arriba a lo narrativo abajo, que es "
        "como se lee una prenda en movimiento: primero el filete, al final las nueve colas.",
        ancho=108, tam=15))

    return marco(ancho, alto, "L-04", "Biblioteca de bandas",
                 "Nueve grecas intercambiables, todas con el mismo módulo de repetición",
                 grupo(piezas), pie="Bandas a tamaño de dibujo, no a escala de prenda")


# --------------------------------------------------------------------------
# L05 · Gráficos de rejilla (punto de cruz y cadenilla contada)
# --------------------------------------------------------------------------


def _rasterizar_polilinea(puntos, gw: int, gh: int) -> list[str]:
    rej = [["." for _ in range(gw + 1)] for _ in range(gh + 1)]
    for (x1, y1), (x2, y2) in zip(puntos, puntos[1:]):
        pasos = max(abs(x2 - x1), abs(y2 - y1))
        for k in range(pasos + 1):
            x = round(x1 + (x2 - x1) * k / pasos)
            y = round(y1 + (y2 - y1) * k / pasos)
            if 0 <= y <= gh and 0 <= x <= gw:
                rej[y][x] = "N"
    return ["".join(f) for f in rej]


def _rejilla_rombo_shuriken(lado: int = 15) -> list[str]:
    c = lado // 2
    rej = [["." for _ in range(lado)] for _ in range(lado)]
    for y in range(lado):
        for x in range(lado):
            dx, dy = x - c, y - c
            d = abs(dx) + abs(dy)
            if d == c:
                rej[y][x] = "A"
            elif d == c - 2:
                rej[y][x] = "O"
            elif (dx == 0 and abs(dy) <= 4) or (dy == 0 and abs(dx) <= 4):
                rej[y][x] = "P"
            elif abs(dx) == abs(dy) and abs(dx) == 2:
                rej[y][x] = "P"
    rej[c][c] = "R"
    return ["".join(f) for f in rej]


PERFIL_HOJA = [
    ".........V.........",
    "........VVV........",
    ".......VVVVV.......",
    "......VVVVVVV......",
    ".....VVVVVVVVV.....",
    "....VVVVVVVVVVV....",
    "...VVVVVVVVVVVVV...",
    "..VVVVVVVVVVVVVVV..",
    "..VVVVVVVVVVVVVVV..",
    ".VVVVVVVVVVVVVVVVV.",
    ".VVVVVVVVVVVVVVVVV.",
    ".VVVVVVVVVVVVVVVVV.",
    ".VVVVVVVVVVVVVVVVV.",
    "..VVVVVVVVVVVVVVV..",
    "..VVVVVVVVVVVVVVV..",
    "...VVVVVVVVVVVVV...",
    "....VVVVVVVVVVV....",
    ".....VVVVVVVVV.....",
    "......VVVVVVV......",
    ".......VVVVV.......",
    "........VVV........",
]


def _rejilla_hoja() -> list[str]:
    """Hoja contada, con el caracol del remolino encima en otro hilo."""
    rej = [list(fila) for fila in PERFIL_HOJA]
    for j, fila in enumerate(M._rejilla_caracol(9)):
        for i, ch in enumerate(fila):
            if ch == "X" and rej[j + 6][i + 5] == "V":
                rej[j + 6][i + 5] = "N"
    return ["".join(f) for f in rej]


def _rejilla_remolino(lado: int = 21) -> list[str]:
    return [fila.replace("X", "N") for fila in M._rejilla_caracol(lado)]


COLORES_REJILLA = {
    "N": ("naranja", "Naranja nindō"),
    "V": ("verde", "Verde hoja"),
    "A": ("anil", "Azul añil"),
    "O": ("oro", "Oro cadenilla"),
    "P": ("plata", "Plata hitai-ate"),
    "R": ("rojo", "Rojo Uzumaki"),
    "M": ("amarillo", "Amarillo sannin"),
}


def grafico_rejilla(x: float, y: float, rej: Sequence[str], celda: float,
                    titulo: str, nota: str) -> str:
    gw = max(len(f) for f in rej)
    gh = len(rej)
    piezas = [
        texto(x, y - 36, titulo, tam=17, color=TINTA, peso="bold"),
        texto(x, y - 16, nota, tam=13, color=TINTA_SUAVE, italica=True),
        rectangulo(x, y, gw * celda, gh * celda, fill="#0A0810"),
    ]
    for marca in sorted({ch for fila in rej for ch in fila} & set(COLORES_REJILLA)):
        piezas.append(ruta(M.rejilla_a_ruta(rej, x, y, celda, marca=marca),
                           fill=C[COLORES_REJILLA[marca][0]]))
    for fuerte in (False, True):
        trazos = []
        for i in range(gw + 1):
            if (i % 5 == 0) == fuerte:
                trazos.append(f"M{n(x + i * celda)},{n(y)}V{n(y + gh * celda)}")
        for j in range(gh + 1):
            if (j % 5 == 0) == fuerte:
                trazos.append(f"M{n(x)},{n(y + j * celda)}H{n(x + gw * celda)}")
        piezas.append(ruta("".join(trazos), fill="none", stroke=TINTA_SUAVE,
                           stroke_width=1.4 if fuerte else 0.5,
                           opacity=0.55 if fuerte else 0.3))
    piezas.append(texto(x, y + gh * celda + 24, f"{gw} × {gh} puntos", tam=13,
                        color=C["oro"], familia=TIPO_MONO))
    return grupo(piezas)


def lamina_05() -> str:
    ancho, alto = 1700, 1340
    piezas = []

    piezas.append(grafico_rejilla(
        92, 312, _rasterizar_polilinea(M.GRECA_HOJA, *M.REJILLA_GRECA), 22,
        "G1 · Greca de la hoja, un módulo",
        "Escalera de tres en tres que cierra en gancho; se repite en espejo"))

    piezas.append(grafico_rejilla(
        572, 312, _rejilla_remolino(21), 18,
        "G2 · Remolino en rejilla",
        "Caracol cuadrado: el remolino Uzumaki, contado"))

    piezas.append(grafico_rejilla(
        1000, 312, _rejilla_hoja(), 18,
        "G3 · Hoja con espiral",
        "Hoja en verde hoja y remolino en naranja nindō encima"))

    piezas.append(grafico_rejilla(
        1380, 312, _rejilla_rombo_shuriken(15), 18,
        "G4 · Rombo con shuriken",
        "Banda B3, para sisa y remate"))

    # G5 · Los seis sellos de mano, en fila.
    x, y = 92, 840
    piezas.append(texto(x, y - 36, "G5 · Los seis sellos de mano", tam=17, color=TINTA,
                        peso="bold"))
    piezas.append(texto(x, y - 16,
                        "Cada sello ocupa 11 × 11 puntos y se siembra en la randa en este orden",
                        tam=13, color=TINTA_SUAVE, italica=True))
    for k, nombre in enumerate(["tora", "mi", "hitsuji", "caracol", "inu", "uma"]):
        cx = x + k * 256
        rej = [fila.replace("X", "O") for fila in M.SELLOS[nombre]]
        piezas.append(grupo([
            ruta(M.rejilla_a_ruta(rej, cx, y, 16, marca="O"), fill=C["oro"]),
            rectangulo(cx, y, 11 * 16, 11 * 16, fill="none", stroke=TINTA_SUAVE,
                       stroke_width=0.8, opacity=0.4),
            texto(cx + 88, y + 11 * 16 + 28, nombre, tam=15, color=C["oro"],
                  anclaje="middle", familia=TIPO_MONO),
        ]))

    # Clave de hilos.
    piezas.append(texto(92, 1150, "CLAVE DE HILOS", tam=15, color=C["oro"],
                        espaciado=2.0, peso="bold"))
    cx = 92
    for marca, (clave, nombre) in COLORES_REJILLA.items():
        piezas.append(rectangulo(cx, 1168, 22, 22, fill=C[clave], stroke=GUIA,
                                 stroke_width=0.8))
        piezas.append(texto(cx + 30, 1185, nombre, tam=13, color=TINTA_SUAVE))
        cx += 222

    piezas.append(parrafo(
        92, 1232,
        "Estos gráficos son el puente real entre las dos tradiciones: el bordado contado "
        "del Istmo y la retícula en la que están dibujados los emblemas de Naruto "
        "funcionan igual. Nada se calca; todo se cuenta.",
        ancho=120, tam=15))

    return marco(ancho, alto, "L-05", "Gráficos de rejilla",
                 "Los mismos motivos contados punto por punto, para bordar sin calcar",
                 grupo(piezas), pie="1 cuadro = 1 punto de cruz o 1 lazada de cadenilla")


# --------------------------------------------------------------------------
# L06 · Variantes de color
# --------------------------------------------------------------------------


def lamina_06() -> str:
    ancho, alto = 1680, 900
    m = PR.P
    esc = 4.9
    piezas = []
    for k, (nombre, uso, cambios) in enumerate(VARIANTES):
        x0 = 120 + k * 520
        y0 = 290
        with variante(cambios):
            piezas.append(lienzo_prenda(PR.frente(m), x0, y0, esc))
        piezas.append(texto(x0, y0 - 46, nombre, tam=19, color=TINTA, peso="bold"))
        piezas.append(texto(x0, y0 - 24, uso, tam=14, color=C["oro"], italica=True))
        piezas.append(texto(x0, y0 + m.largo * esc + 34,
                            f"fondo {cambios.get('fondo', C['fondo'])}", tam=13,
                            color=TINTA_SUAVE, familia=TIPO_MONO))
    piezas.append(parrafo(
        120, y0 + m.largo * esc + 76,
        "La estructura no cambia nunca: sólo el fondo y dos o tres tintes. Es la misma "
        "lógica del guardarropa istmeño, donde una prenda de gala y una de diario "
        "comparten patrón y se distinguen por la tela y la densidad del bordado.",
        ancho=112, tam=15))
    return marco(ancho, alto, "L-06", "Variantes de color",
                 "Gala, diario y Vela nocturna sobre el mismo patrón",
                 grupo(piezas), pie="Mismo patrón, reducido · medidas en cm")


LAMINAS: dict[str, Callable[[], str]] = {
    "L-00-paleta-y-simbologia": lamina_00,
    "L-01-frente": lamina_01,
    "L-02-espalda": lamina_02,
    "L-03-patron-y-confeccion": lamina_03,
    "L-04-biblioteca-de-bandas": lamina_04,
    "L-05-graficos-de-rejilla": lamina_05,
    "L-06-variantes-de-color": lamina_06,
}
