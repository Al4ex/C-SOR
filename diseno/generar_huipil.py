#!/usr/bin/env python3
"""Genera el plano vectorial (SVG) del huipil para hombre del Istmo de Oaxaca
con iconografía de Naruto.

Uso:
    python3 generar_huipil.py            # escribe huipil-istmo-naruto.svg
"""
from __future__ import annotations

import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Escala y paleta
# ---------------------------------------------------------------------------
PX_POR_CM = 8                      # 1 cm = 8 px
ANCHO_CM, LARGO_CM = 66, 78        # lienzo (delantero / trasero)
W, H = ANCHO_CM * PX_POR_CM, LARGO_CM * PX_POR_CM   # 528 x 624

NEGRO = "#0b0b0d"        # terciopelo negro
NARANJA = "#F7931E"      # naranja Naruto
ROJO = "#C8102E"         # rojo Uzumaki / Akatsuki
ORO = "#E8B923"          # hilo dorado (cadenilla)
AZUL = "#2E86DE"         # azul Rasengan
BLANCO = "#F5F0E6"       # hilo crudo
MORADO = "#7B5EA7"       # Rinnegan
MORADO_CLARO = "#C9B8E8"
VERDE = "#3E9B4F"        # hojas (verde istmeño)
ROSA = "#E8449A"         # rosa mexicano
TURQUESA = "#1ABC9C"
PLATA = "#C9CDD3"
CARBON = "#1f1f22"

KANJI_FONT = "'Noto Sans CJK JP','Noto Sans JP','WenQuanYi Micro Hei','Droid Sans Fallback',sans-serif"
UI_FONT = "'Inter','DejaVu Sans','Liberation Sans',sans-serif"


def fmt(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def pt(x: float, y: float) -> str:
    return f"{fmt(x)},{fmt(y)}"


# ---------------------------------------------------------------------------
# Primitivas geométricas
# ---------------------------------------------------------------------------
def spiral_points(cx, cy, r0, r1, turns, ccw=False, steps_per_turn=48):
    pts = []
    n = int(turns * steps_per_turn)
    theta_max = turns * 2 * math.pi
    for i in range(n + 1):
        th = theta_max * i / n
        r = r0 + (r1 - r0) * i / n
        a = -th if ccw else th
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def polyline_d(pts, close=False):
    d = "M" + " L".join(pt(x, y) for x, y in pts)
    return d + (" Z" if close else "")


def tapered_arc(cx, cy, d, width, phi0, sweep, steps=24):
    """Polígono tipo 'tomoe': banda sobre el círculo de radio d que se afina."""
    outer, inner = [], []
    for i in range(steps + 1):
        t = i / steps
        a = math.radians(phi0 + sweep * t)
        w = width * (1 - t)
        outer.append((cx + (d + w) * math.cos(a), cy + (d + w) * math.sin(a)))
        inner.append((cx + (d - w) * math.cos(a), cy + (d - w) * math.sin(a)))
    return polyline_d(outer + inner[::-1], close=True)


def tapered_curve(p0, p1, p2, w0, w1=0.0, steps=20):
    """Polígono que sigue una Bézier cuadrática con grosor que se afina."""
    left, right = [], []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
        dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        w = w0 + (w1 - w0) * t
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return polyline_d(left + right[::-1], close=True)


# ---------------------------------------------------------------------------
# Motivos Naruto
# ---------------------------------------------------------------------------
def konoha(cx, cy, s, color=ORO, sw=None):
    """Símbolo de la Aldea Oculta de la Hoja."""
    sw = sw or s * 0.13
    r1 = s * 0.42
    pts = spiral_points(cx, cy, s * 0.04, r1, 1.75, ccw=True)
    d = polyline_d(pts) + f" L{pt(cx + s * 0.95, cy + r1)}"
    # triángulo (punta de la hoja) en la parte superior izquierda
    a = math.radians(225)
    bx, by = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
    tx, ty = math.cos(a + math.pi / 2), math.sin(a + math.pi / 2)
    ax, ay = cx + (r1 + s * 0.34) * math.cos(a), cy + (r1 + s * 0.34) * math.sin(a)
    tri = f"M{pt(bx + tx * s * 0.17, by + ty * s * 0.17)} L{pt(bx - tx * s * 0.17, by - ty * s * 0.17)} L{pt(ax, ay)} Z"
    return (f'<g class="konoha"><path d="{d}" fill="none" stroke="{color}" stroke-width="{fmt(sw)}" '
            f'stroke-linecap="round" stroke-linejoin="round"/><path d="{tri}" fill="{color}"/></g>')


def uzumaki(cx, cy, diam, color=ROJO, turns=2.6, sw=None, outline=None):
    """Espiral del clan Uzumaki (espalda de la chamarra de Naruto)."""
    sw = sw or diam * 0.09
    pts = spiral_points(cx, cy, 0, diam / 2 - sw / 2, turns, steps_per_turn=64)
    d = polyline_d(pts)
    out = ""
    if outline:
        out = (f'<path d="{d}" fill="none" stroke="{outline}" stroke-width="{fmt(sw * 1.6)}" '
               f'stroke-linecap="round"/>')
    return (f'<g class="uzumaki">{out}<path d="{d}" fill="none" stroke="{color}" '
            f'stroke-width="{fmt(sw)}" stroke-linecap="round"/></g>')


def tomoe(cx, cy, d, r, phi0, color=CARBON):
    a = math.radians(phi0)
    hx, hy = cx + d * math.cos(a), cy + d * math.sin(a)
    return (f'<circle cx="{fmt(hx)}" cy="{fmt(hy)}" r="{fmt(r)}" fill="{color}"/>'
            f'<path d="{tapered_arc(cx, cy, d, r, phi0, 95)}" fill="{color}"/>')


def petalos(cx, cy, R, n, color, color2=None, rot=0):
    """Corona de pétalos (flor istmeña) detrás de un medallón."""
    out = []
    for i in range(n):
        a = rot + 360 * i / n
        c = color if (color2 is None or i % 2 == 0) else color2
        out.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy - R * 0.72)}" rx="{fmt(R * 0.30)}" ry="{fmt(R * 0.55)}" '
                   f'fill="{c}" stroke="{NEGRO}" stroke-width="1.5" transform="rotate({fmt(a)} {fmt(cx)} {fmt(cy)})"/>')
    return "".join(out)


def sharingan(cx, cy, R):
    g = [f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R)}" fill="{CARBON}"/>',
         f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R * 0.86)}" fill="{ROJO}"/>',
         f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R * 0.5)}" fill="none" stroke="{CARBON}" stroke-width="{fmt(R * 0.06)}"/>']
    for k in range(3):
        g.append(tomoe(cx, cy, R * 0.5, R * 0.14, -90 + 120 * k))
    g.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R * 0.17)}" fill="{CARBON}"/>')
    return f'<g class="sharingan">{"".join(g)}</g>'


def rinnegan(cx, cy, R):
    g = [f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R)}" fill="{MORADO_CLARO}" stroke="{MORADO}" stroke-width="{fmt(R * 0.08)}"/>']
    for k in range(1, 5):
        g.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R * k / 5)}" fill="none" stroke="{MORADO}" stroke-width="{fmt(R * 0.05)}"/>')
    g.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R * 0.1)}" fill="{CARBON}"/>')
    return f'<g class="rinnegan">{"".join(g)}</g>'


def nube_akatsuki(cx, cy, w, color=ROJO, borde=BLANCO):
    circ = [(-0.30, 0.06, 0.20), (-0.09, -0.09, 0.26), (0.17, -0.02, 0.22), (0.35, 0.10, 0.15), (0.04, 0.16, 0.18)]
    outline = "".join(f'<circle cx="{fmt(cx + x * w)}" cy="{fmt(cy + y * w)}" r="{fmt(r * w + w * 0.045)}" fill="{borde}"/>' for x, y, r in circ)
    fill = "".join(f'<circle cx="{fmt(cx + x * w)}" cy="{fmt(cy + y * w)}" r="{fmt(r * w)}" fill="{color}"/>' for x, y, r in circ)
    return f'<g class="akatsuki">{outline}{fill}</g>'


def shuriken(cx, cy, R, color=PLATA, fondo=NEGRO):
    pts = []
    for k in range(8):
        a = math.radians(k * 45 + (12 if k % 2 else 0))
        r = R if k % 2 == 0 else R * 0.3
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return (f'<g class="shuriken"><path d="{polyline_d(pts, True)}" fill="{color}" stroke="{CARBON}" stroke-width="1.2"/>'
            f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R * 0.11)}" fill="{fondo}"/></g>')


def kunai(cx, cy, L, rot=0, color=PLATA):
    blade = polyline_d([(0, -0.5 * L), (0.14 * L, -0.06 * L), (0, 0.06 * L), (-0.14 * L, -0.06 * L)], True)
    handle = f'<rect x="{fmt(-0.035 * L)}" y="{fmt(0.05 * L)}" width="{fmt(0.07 * L)}" height="{fmt(0.3 * L)}" fill="{CARBON}" stroke="{color}" stroke-width="1"/>'
    wrap = "".join(f'<line x1="{fmt(-0.035 * L)}" y1="{fmt(y)}" x2="{fmt(0.035 * L)}" y2="{fmt(y + 0.03 * L)}" stroke="{BLANCO}" stroke-width="1"/>'
                   for y in [0.08 * L, 0.15 * L, 0.22 * L, 0.29 * L])
    ring = f'<circle cx="0" cy="{fmt(0.42 * L)}" r="{fmt(0.065 * L)}" fill="none" stroke="{color}" stroke-width="{fmt(0.03 * L)}"/>'
    return (f'<g class="kunai" transform="translate({fmt(cx)} {fmt(cy)}) rotate({fmt(rot)})">'
            f'<path d="{blade}" fill="{color}" stroke="{CARBON}" stroke-width="1"/>{handle}{wrap}{ring}</g>')


def sello_ocho_trigramas(cx, cy, R):
    """Hakke no Fūin Shiki: espiral central + ocho trazos radiales."""
    g = [f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R * 0.56)}" fill="none" stroke="{ORO}" stroke-width="{fmt(R * 0.035)}" stroke-dasharray="4 3"/>']
    for base in (-90, 90):
        for off in (-33, -11, 11, 33):
            a = math.radians(base + off)
            p0 = (cx + R * 0.62 * math.cos(a), cy + R * 0.62 * math.sin(a))
            p2 = (cx + R * 1.0 * math.cos(a), cy + R * 1.0 * math.sin(a))
            bend = math.radians(base + off * 1.6)
            p1 = (cx + R * 0.82 * math.cos(bend), cy + R * 0.82 * math.sin(bend))
            g.append(f'<path d="{tapered_curve(p0, p1, p2, R * 0.055, 0)}" fill="{NARANJA}"/>')
    g.append(uzumaki(cx, cy, R * 0.95, color=ROJO, turns=2.4, sw=R * 0.075, outline=NARANJA))
    return f'<g class="hakke">{"".join(g)}</g>'


def colas_kurama(cx, cy, Wd):
    """Abanico de nueve colas de Kurama (llamas de chakra)."""
    g = []
    base = (cx, cy + Wd * 0.28)
    for i in range(9):
        a = math.radians(-170 + 160 * i / 8)
        L = Wd * (0.42 if i in (0, 8) else 0.5 if i in (1, 7) else 0.56 if i in (2, 6) else 0.6)
        p2 = (cx + L * math.cos(a), base[1] + L * math.sin(a) - Wd * 0.02)
        side = -1 if i < 4 else (1 if i > 4 else 0)
        p1 = (cx + L * 0.5 * math.cos(a) - side * Wd * 0.12, base[1] + L * 0.55 * math.sin(a))
        g.append(f'<path d="{tapered_curve(base, p1, p2, Wd * 0.045, 0)}" fill="{NARANJA}"/>')
        g.append(f'<path d="{tapered_curve(base, p1, p2, Wd * 0.02, 0, steps=20)}" fill="{ORO}" opacity="0.9"/>')
    # cabeza de zorro estilizada (cara + orejas)
    hx, hy = cx, base[1] + Wd * 0.02
    g.append(f'<path d="M{pt(hx - Wd * 0.11, hy - Wd * 0.05)} L{pt(hx - Wd * 0.13, hy - Wd * 0.17)} L{pt(hx - Wd * 0.03, hy - Wd * 0.09)} '
             f'L{pt(hx + Wd * 0.03, hy - Wd * 0.09)} L{pt(hx + Wd * 0.13, hy - Wd * 0.17)} L{pt(hx + Wd * 0.11, hy - Wd * 0.05)} '
             f'Q{pt(hx + Wd * 0.13, hy + Wd * 0.06)} {pt(hx, hy + Wd * 0.12)} Q{pt(hx - Wd * 0.13, hy + Wd * 0.06)} {pt(hx - Wd * 0.11, hy - Wd * 0.05)} Z" '
             f'fill="{NARANJA}" stroke="{ROJO}" stroke-width="1.5"/>')
    for sx in (-1, 1):
        g.append(f'<path d="M{pt(hx + sx * Wd * 0.02, hy - Wd * 0.03)} L{pt(hx + sx * Wd * 0.085, hy - Wd * 0.045)} L{pt(hx + sx * Wd * 0.055, hy + Wd * 0.005)} Z" fill="{ROJO}"/>')
    g.append(f'<circle cx="{fmt(hx)}" cy="{fmt(hy + Wd * 0.06)}" r="{fmt(Wd * 0.014)}" fill="{CARBON}"/>')
    return f'<g class="kurama">{"".join(g)}</g>'


def rasengan(cx, cy, R):
    g = [f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(R)}" fill="url(#gradRasengan)" stroke="{BLANCO}" stroke-width="1.2"/>']
    for k in range(3):
        pts = spiral_points(cx, cy, R * 0.1, R * 0.85, 0.9, steps_per_turn=40)
        g.append(f'<path d="{polyline_d(pts)}" fill="none" stroke="{BLANCO}" stroke-width="{fmt(R * 0.09)}" '
                 f'stroke-linecap="round" opacity="0.85" transform="rotate({120 * k} {fmt(cx)} {fmt(cy)})"/>')
    return f'<g class="rasengan">{"".join(g)}</g>'


# Símbolos de las Cinco Grandes Aldeas (trazo cadenilla)
def suna(cx, cy, s, color=ORO):
    sw = s * 0.12
    return (f'<g class="suna" fill="none" stroke="{color}" stroke-width="{fmt(sw)}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M{pt(cx - s * 0.3, cy - s * 0.45)} L{pt(cx + s * 0.3, cy - s * 0.45)} L{pt(cx - s * 0.3, cy + s * 0.45)} L{pt(cx + s * 0.3, cy + s * 0.45)} Z"/>'
            f'<line x1="{fmt(cx - s * 0.45)}" y1="{fmt(cy)}" x2="{fmt(cx + s * 0.45)}" y2="{fmt(cy)}"/></g>')


def kiri(cx, cy, s, color=ORO):
    sw = s * 0.12
    g = []
    for i, (ly, half) in enumerate([(-0.36, 0.42), (-0.12, 0.46), (0.12, 0.46), (0.36, 0.42)]):
        y = cy + ly * s
        x0, x1 = cx - half * s, cx + half * s
        q = (x1 - x0) / 4
        g.append(f'<path d="M{pt(x0, y)} q{pt(q / 2, -s * 0.12)} {pt(q, 0)} t{pt(q, 0)} t{pt(q, 0)} t{pt(q, 0)}"/>')
    return f'<g class="kiri" fill="none" stroke="{color}" stroke-width="{fmt(sw)}" stroke-linecap="round">{"".join(g)}</g>'


def kumo(cx, cy, s, color=ORO):
    sw = s * 0.12
    d = (f"M{pt(cx - s * 0.45, cy + s * 0.25)} a{fmt(s * 0.2)},{fmt(s * 0.2)} 0 0 1 {pt(s * 0.2, -s * 0.33)} "
         f"a{fmt(s * 0.22)},{fmt(s * 0.22)} 0 0 1 {pt(s * 0.42, -s * 0.08)} a{fmt(s * 0.2)},{fmt(s * 0.2)} 0 0 1 {pt(s * 0.3, s * 0.41)} Z")
    return f'<path class="kumo" d="{d}" fill="none" stroke="{color}" stroke-width="{fmt(sw)}" stroke-linejoin="round"/>'


def iwa(cx, cy, s, color=ORO):
    sw = s * 0.12
    return (f'<g class="iwa" fill="none" stroke="{color}" stroke-width="{fmt(sw)}" stroke-linejoin="round">'
            f'<path d="M{pt(cx - s * 0.45, cy + s * 0.45)} L{pt(cx - s * 0.3, cy + s * 0.05)} L{pt(cx + s * 0.3, cy + s * 0.05)} L{pt(cx + s * 0.45, cy + s * 0.45)} Z"/>'
            f'<path d="M{pt(cx - s * 0.25, cy + s * 0.05)} L{pt(cx - s * 0.12, cy - s * 0.4)} L{pt(cx + s * 0.12, cy - s * 0.4)} L{pt(cx + s * 0.25, cy + s * 0.05)}"/></g>')


# ---------------------------------------------------------------------------
# Elementos de cadenilla (greca istmeña)
# ---------------------------------------------------------------------------
def linea_cadenilla(x0, y0, x1, y1, color=ORO, sw=2.2):
    return (f'<line x1="{fmt(x0)}" y1="{fmt(y0)}" x2="{fmt(x1)}" y2="{fmt(y1)}" stroke="{color}" '
            f'stroke-width="{fmt(sw)}" stroke-dasharray="3.5 2" stroke-linecap="round"/>')


def zigzag(x0, x1, y, amp, paso, color=ORO, sw=2.2):
    pts = []
    x = x0
    i = 0
    while x <= x1 + 0.1:
        pts.append((x, y - amp if i % 2 == 0 else y + amp))
        x += paso
        i += 1
    return f'<path d="{polyline_d(pts)}" fill="none" stroke="{color}" stroke-width="{fmt(sw)}" stroke-dasharray="3.5 2" stroke-linejoin="round" stroke-linecap="round"/>'


def gradita(x0, x1, y, h, paso, color=ORO, sw=2.2):
    """Greca escalonada ('la gradita', pirámide zapoteca)."""
    pts = []
    x = x0
    up = True
    pts.append((x, y + h))
    while x < x1:
        if up:
            pts += [(x, y - h), (x + paso, y - h)]
        else:
            pts += [(x, y + h), (x + paso, y + h)]
        x += paso
        up = not up
    return f'<path d="{polyline_d(pts)}" fill="none" stroke="{color}" stroke-width="{fmt(sw)}" stroke-dasharray="3.5 2" stroke-linejoin="round"/>'


def rombos(x0, x1, y, h, paso, color=ORO, sw=2.2):
    g = []
    x = x0
    while x + paso <= x1 + 0.1:
        d = f"M{pt(x, y)} L{pt(x + paso / 2, y - h)} L{pt(x + paso, y)} L{pt(x + paso / 2, y + h)} Z"
        g.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{fmt(sw)}" stroke-dasharray="3.5 2" stroke-linejoin="round"/>')
        x += paso
    return "".join(g)


# ---------------------------------------------------------------------------
# Composición de un lienzo (delantero / trasero)
# ---------------------------------------------------------------------------
ESCOTE_W, ESCOTE_H_DEL, ESCOTE_H_TRAS = 160, 140, 64   # 20 x 17.5 cm  /  20 x 8 cm
BANDA_ESCOTE = 22
SISA = 26 * PX_POR_CM        # abertura de brazo 26 cm
ABERTURA_LATERAL = 12 * PX_POR_CM


def lienzo(ox, oy, trasero=False):
    g = [f'<g class="lienzo {"trasero" if trasero else "delantero"}" transform="translate({ox} {oy})">']
    esc_h = ESCOTE_H_TRAS if trasero else ESCOTE_H_DEL
    ex0, ex1 = (W - ESCOTE_W) / 2, (W + ESCOTE_W) / 2

    # tela (terciopelo negro) con escote cuadrado recortado
    cuerpo = (f"M0,0 H{fmt(ex0)} V{fmt(esc_h)} H{fmt(ex1)} V0 H{W} V{H} H0 Z")
    g.append(f'<path d="{cuerpo}" fill="url(#terciopelo)" stroke="{ORO}" stroke-width="1.5"/>')
    g.append(f'<path d="{cuerpo}" fill="url(#textura)" opacity="0.35"/>')
    g.append(f'<clipPath id="clip{"T" if trasero else "D"}"><path d="{cuerpo}"/></clipPath>')
    g.append(f'<g clip-path="url(#clip{"T" if trasero else "D"})">')

    # --- Banda A: hombros (y 0-60): zigzag 'cerrito' + cinco aldeas ----------
    yA = 32
    g.append(zigzag(6, W - 6, yA, 9, 16, NARANJA))
    g.append(linea_cadenilla(6, yA - 22, W - 6, yA - 22, ORO))
    g.append(linea_cadenilla(6, yA + 22, W - 6, yA + 22, ORO))
    aldeas = [konoha, suna, kiri, kumo, iwa]
    for i, x in enumerate([40, 100, W - 100, W - 40]):
        f = aldeas[[0, 1, 2, 3][i]] if not trasero else aldeas[[4, 0, 0, 4][i]]
        g.append(f'<rect x="{fmt(x - 16)}" y="{fmt(yA - 16)}" width="32" height="32" fill="{NEGRO}"/>')
        g.append(f(x, yA, 26, ORO))

    # --- Banda B: pecho (y 60-170) ------------------------------------------
    if not trasero:
        for cx, ojo, c1, c2 in ((92, sharingan, ROSA, ROJO), (W - 92, rinnegan, TURQUESA, MORADO)):
            cy = 118
            g.append(petalos(cx, cy, 52, 10, c1, c2, rot=18))
            # hojas istmeñas (verdes) a los lados
            for sx in (-1, 1):
                g.append(f'<ellipse cx="{fmt(cx + sx * 62)}" cy="{fmt(cy + 22)}" rx="7" ry="18" fill="{VERDE}" '
                         f'transform="rotate({fmt(sx * 40)} {fmt(cx + sx * 62)} {fmt(cy + 22)})"/>')
            g.append(ojo(cx, cy, 34))
        # tomoe sueltos junto al escote
        for cx in (ex0 - 24, ex1 + 24):
            g.append(tomoe(cx, 118, 0.1, 9, -90, NARANJA))
    else:
        for cx in (92, W - 92):
            g.append(konoha(cx, 118, 70, NARANJA, sw=9))
            g.append(f'<circle cx="{fmt(cx)}" cy="118" r="50" fill="none" stroke="{ORO}" stroke-width="2" stroke-dasharray="3.5 2"/>')

    # --- Banda escote ---------------------------------------------------------
    bx0, bx1, by1 = ex0 - BANDA_ESCOTE, ex1 + BANDA_ESCOTE, esc_h + BANDA_ESCOTE
    g.append(f'<path d="M{pt(bx0, 0)} V{fmt(by1)} H{fmt(bx1)} V0 H{fmt(ex1)} V{fmt(esc_h)} H{fmt(ex0)} V0 Z" fill="{ROJO}"/>')
    g.append(f'<path d="M{pt(bx0 + 3, 0)} V{fmt(by1 - 3)} H{fmt(bx1 - 3)} V0" fill="none" stroke="{ORO}" stroke-width="2" stroke-dasharray="3.5 2"/>')
    g.append(f'<path d="M{pt(ex0 - 3, 0)} V{fmt(esc_h + 3)} H{fmt(ex1 + 3)} V0" fill="none" stroke="{ORO}" stroke-width="2" stroke-dasharray="3.5 2"/>')
    # konoha pequeñitos sobre la banda del escote
    n = 5 if not trasero else 2
    for i in range(n):
        yk = 14 + (esc_h - 28) * i / max(n - 1, 1)
        for xk in (bx0 + BANDA_ESCOTE / 2, bx1 - BANDA_ESCOTE / 2):
            g.append(konoha(xk, yk, 16, ORO, sw=2.4))
    for i in range(6):
        xk = ex0 + 10 + (ESCOTE_W - 20) * i / 5
        g.append(konoha(xk, esc_h + BANDA_ESCOTE / 2, 16, ORO, sw=2.4))

    if not trasero:
        # --- Banda C (y 176-220): rombos con shuriken ----------------------
        yC = 198
        g.append(linea_cadenilla(0, yC - 22, W, yC - 22, ORO))
        g.append(linea_cadenilla(0, yC + 22, W, yC + 22, ORO))
        g.append(rombos(0, W, yC, 18, 48, NARANJA))
        for i in range(11):
            g.append(shuriken(24 + 48 * i, yC, 11))

        # --- Banda D (y 228-372): medallón Hakke Fūin + kunai ----------------
        yD = 300
        g.append(petalos(W / 2, yD, 74, 12, NARANJA, ROJO, rot=15))
        g.append(f'<circle cx="{fmt(W / 2)}" cy="{fmt(yD)}" r="54" fill="{NEGRO}"/>')
        g.append(sello_ocho_trigramas(W / 2, yD, 52))
        for sx in (-1, 1):
            cx = W / 2 + sx * 170
            g.append(kunai(cx - 14, yD, 92, rot=-28))
            g.append(kunai(cx + 14, yD, 92, rot=28))
            for k in range(3):
                g.append(tomoe(cx, yD - 2, 36, 7, -90 + 120 * k, ORO))
            g.append(f'<circle cx="{fmt(cx)}" cy="{fmt(yD - 2)}" r="48" fill="none" stroke="{ORO}" stroke-width="2" stroke-dasharray="3.5 2"/>')
        # tomoe de relleno entre medallón y kunai
        for sx in (-1, 1):
            for yy in (yD - 48, yD + 48):
                g.append(tomoe(W / 2 + sx * 100, yy, 0.1, 6, -90, ROSA))

        # --- Banda E (y 380-430): nubes Akatsuki -----------------------------
        yE = 405
        g.append(linea_cadenilla(0, yE - 24, W, yE - 24, BLANCO, 1.6))
        g.append(linea_cadenilla(0, yE + 24, W, yE + 24, BLANCO, 1.6))
        for i in range(5):
            g.append(nube_akatsuki(52 + i * 106, yE + 2, 64))
    else:
        # --- Espalda: gran espiral Uzumaki (y 176-430) -------------------------
        yS = 303
        g.append(linea_cadenilla(0, 180, W, 180, ORO))
        g.append(linea_cadenilla(0, 429, W, 429, ORO))
        g.append(petalos(W / 2, yS, 128, 14, ROJO, NARANJA, rot=12))
        g.append(f'<circle cx="{fmt(W / 2)}" cy="{fmt(yS)}" r="100" fill="{NEGRO}"/>')
        g.append(f'<circle cx="{fmt(W / 2)}" cy="{fmt(yS)}" r="100" fill="none" stroke="{ORO}" stroke-width="2.5" stroke-dasharray="3.5 2"/>')
        g.append(uzumaki(W / 2, yS, 176, ROJO, turns=3.0, sw=15, outline=BLANCO))
        # shuriken y tomoe a los costados
        for sx in (-1, 1):
            cx = W / 2 + sx * 196
            g.append(shuriken(cx, yS - 70, 22))
            g.append(shuriken(cx, yS + 70, 22))
            for k in range(3):
                g.append(tomoe(cx, yS, 24, 6, -90 + 120 * k, NARANJA))
            g.append(f'<circle cx="{fmt(cx)}" cy="{fmt(yS)}" r="34" fill="none" stroke="{ORO}" stroke-width="2" stroke-dasharray="3.5 2"/>')

    # --- Banda F (y 440-545): colas de Kurama + Rasengan + gradita ------------
    yF = 494
    g.append(gradita(0, W, yF - 44, 5, 12, ORO, 1.8))
    g.append(gradita(0, W, yF + 46, 5, 12, ORO, 1.8))
    for i in range(3):
        cx = 92 + i * 172
        g.append(colas_kurama(cx, yF, 150))
    for cx in (178, 350):
        g.append(rasengan(cx, yF + 26, 15))

    # --- Banda G (y 556-600): guarda roja con kanji 忍 y Konoha ---------------
    yG = 578
    g.append(f'<rect x="0" y="{fmt(yG - 22)}" width="{W}" height="44" fill="{ROJO}"/>')
    g.append(linea_cadenilla(0, yG - 19, W, yG - 19, ORO))
    g.append(linea_cadenilla(0, yG + 19, W, yG + 19, ORO))
    for i in range(12):
        cx = 22 + i * 44
        if i % 2 == 0:
            g.append(f'<text x="{fmt(cx)}" y="{fmt(yG + 11)}" font-family="{KANJI_FONT}" font-size="30" font-weight="700" '
                     f'fill="{ORO}" text-anchor="middle">忍</text>')
        else:
            g.append(konoha(cx, yG, 24, BLANCO, sw=3.4))
    g.append(linea_cadenilla(0, H - 6, W, H - 6, ORO, 2.5))
    g.append("</g>")  # fin clip

    # --- Indicaciones de confección (líneas técnicas) --------------------------
    g.append(f'<line x1="0" y1="{fmt(H - ABERTURA_LATERAL)}" x2="0" y2="{H}" stroke="{TURQUESA}" stroke-width="5"/>')
    g.append(f'<line x1="{W}" y1="{fmt(H - ABERTURA_LATERAL)}" x2="{W}" y2="{H}" stroke="{TURQUESA}" stroke-width="5"/>')
    g.append(f'<line x1="0" y1="6" x2="0" y2="{fmt(SISA)}" stroke="{AZUL}" stroke-width="5" stroke-dasharray="8 5"/>')
    g.append(f'<line x1="{W}" y1="6" x2="{W}" y2="{fmt(SISA)}" stroke="{AZUL}" stroke-width="5" stroke-dasharray="8 5"/>')
    g.append("</g>")
    return "\n".join(g)


# ---------------------------------------------------------------------------
# Hoja completa
# ---------------------------------------------------------------------------
def cota(x0, y0, x1, y1, texto, color="#555"):
    vertical = abs(x1 - x0) < 1
    tx, ty = ((x0 + x1) / 2, y0 - 6) if not vertical else (x0 - 8, (y0 + y1) / 2)
    rot = f' transform="rotate(-90 {fmt(tx)} {fmt(ty)})"' if vertical else ""
    return (f'<g class="cota" stroke="{color}" stroke-width="1"><line x1="{fmt(x0)}" y1="{fmt(y0)}" x2="{fmt(x1)}" y2="{fmt(y1)}"/>'
            f'<line x1="{fmt(x0)}" y1="{fmt(y0 - 5 if not vertical else y0)}" x2="{fmt(x0 if not vertical else x0 - 5)}" y2="{fmt(y0 + 5 if not vertical else y0)}"/>'
            f'<line x1="{fmt(x1)}" y1="{fmt(y1 - 5 if not vertical else y1)}" x2="{fmt(x1 if not vertical else x1 + 5)}" y2="{fmt(y1 + 5 if not vertical else y1)}"/>'
            f'<text x="{fmt(tx)}" y="{fmt(ty)}" font-family="{UI_FONT}" font-size="12" fill="{color}" text-anchor="middle" stroke="none"{rot}>{texto}</text></g>')


def leyenda(x, y):
    items = [
        (lambda cx, cy: konoha(cx, cy, 30, ORO, sw=4), "Konoha (Aldea de la Hoja)", "escote, hombros, bajo"),
        (lambda cx, cy: uzumaki(cx, cy, 30, ROJO, sw=4, outline=BLANCO), "Espiral Uzumaki", "medallón de espalda"),
        (lambda cx, cy: sharingan(cx, cy, 15), "Sharingan", "flor izquierda del pecho"),
        (lambda cx, cy: rinnegan(cx, cy, 15), "Rinnegan", "flor derecha del pecho"),
        (lambda cx, cy: sello_ocho_trigramas(cx, cy, 17), "Hakke Fūin (sello de 8 trigramas)", "medallón central"),
        (lambda cx, cy: shuriken(cx, cy, 15, fondo="#ffffff"), "Shuriken", "greca de rombos"),
        (lambda cx, cy: kunai(cx, cy, 34, rot=30), "Kunai", "flancos del medallón"),
        (lambda cx, cy: nube_akatsuki(cx, cy, 36, ROJO, "#222"), "Nube Akatsuki", "franja media"),
        (lambda cx, cy: colas_kurama(cx, cy, 46), "Nueve colas de Kurama", "franja inferior"),
        (lambda cx, cy: rasengan(cx, cy, 13), "Rasengan", "entre las colas"),
        (lambda cx, cy: f'<g>{suna(cx - 22, cy, 16, "#444")}{kiri(cx - 7, cy, 16, "#444")}{kumo(cx + 8, cy, 16, "#444")}{iwa(cx + 23, cy, 16, "#444")}</g>',
         "Suna · Kiri · Kumo · Iwa", "hombros (5 grandes aldeas)"),
        (lambda cx, cy: f'<text x="{fmt(cx)}" y="{fmt(cy + 9)}" font-family="{KANJI_FONT}" font-size="26" font-weight="700" fill="{ROJO}" text-anchor="middle">忍</text>',
         "忍 (shinobi)", "guarda roja del bajo"),
    ]
    g = [f'<text x="{x}" y="{y}" font-family="{UI_FONT}" font-size="17" font-weight="700" fill="#222">Motivos y ubicación</text>']
    yy = y + 30
    for draw, nombre, lugar in items:
        g.append(f'<rect x="{x}" y="{fmt(yy - 20)}" width="46" height="40" rx="5" fill="#f3efe6" stroke="#ddd"/>')
        g.append(draw(x + 23, yy))
        g.append(f'<text x="{x + 56}" y="{fmt(yy - 2)}" font-family="{UI_FONT}" font-size="13" font-weight="600" fill="#222">{nombre}</text>')
        g.append(f'<text x="{x + 56}" y="{fmt(yy + 14)}" font-family="{UI_FONT}" font-size="11.5" fill="#666">{lugar}</text>')
        yy += 50
    # paleta
    yy += 6
    g.append(f'<text x="{x}" y="{yy}" font-family="{UI_FONT}" font-size="17" font-weight="700" fill="#222">Paleta de hilos</text>')
    yy += 14
    paleta = [(NEGRO, "terciopelo negro"), (NARANJA, "naranja"), (ROJO, "rojo"), (ORO, "oro"), (BLANCO, "crudo"),
              (AZUL, "azul"), (MORADO, "morado"), (VERDE, "verde"), (ROSA, "rosa mexicano"), (TURQUESA, "turquesa")]
    for i, (c, n) in enumerate(paleta):
        px = x + (i % 2) * 168
        py = yy + (i // 2) * 24
        g.append(f'<rect x="{px}" y="{py}" width="22" height="16" rx="3" fill="{c}" stroke="#999"/>')
        g.append(f'<text x="{px + 28}" y="{py + 12}" font-family="{UI_FONT}" font-size="11.5" fill="#333">{n} {c}</text>')
    return "\n".join(g)


def hoja():
    CW, CH = 1690, 1020
    fx, fy = 70, 168
    bx, by = fx + W + 110, fy
    lx = bx + W + 90
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">']
    s.append(f"""<defs>
  <linearGradient id="terciopelo" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#1a1a1f"/><stop offset="0.45" stop-color="{NEGRO}"/><stop offset="1" stop-color="#141418"/>
  </linearGradient>
  <radialGradient id="gradRasengan" cx="0.4" cy="0.4" r="0.7">
    <stop offset="0" stop-color="#dff3ff"/><stop offset="0.5" stop-color="{AZUL}"/><stop offset="1" stop-color="#143d75"/>
  </radialGradient>
  <filter id="ruido" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  <pattern id="textura" width="120" height="120" patternUnits="userSpaceOnUse">
    <rect width="120" height="120" filter="url(#ruido)"/>
  </pattern>
</defs>""")
    s.append(f'<rect width="{CW}" height="{CH}" fill="#faf7f0"/>')
    # título
    s.append(f'<text x="{fx}" y="54" font-family="{UI_FONT}" font-size="30" font-weight="800" fill="#1b1b1b">Huipil de hombre · Istmo de Oaxaca × Naruto</text>')
    s.append(f'<text x="{fx}" y="82" font-family="{UI_FONT}" font-size="15" fill="#555">'
             f'«Bidaani\' Shinobi» · terciopelo negro, bordado de cadenilla y puntada de relleno · talla M (holgado) · escala 1 cm = {PX_POR_CM} px</text>')
    s.append(f'<text x="{fx}" y="104" font-family="{UI_FONT}" font-size="13" fill="#777">'
             f'Línea azul punteada = sisa abierta (26 cm) · línea turquesa = abertura lateral (12 cm) · banda roja del escote = guarda de terciopelo rojo con cadenilla dorada</text>')
    # etiquetas y lienzos
    s.append(f'<text x="{fx + W / 2}" y="{fy - 34}" font-family="{UI_FONT}" font-size="16" font-weight="700" fill="#333" text-anchor="middle">DELANTERO</text>')
    s.append(f'<text x="{bx + W / 2}" y="{by - 34}" font-family="{UI_FONT}" font-size="16" font-weight="700" fill="#333" text-anchor="middle">ESPALDA</text>')
    s.append(lienzo(fx, fy, trasero=False))
    s.append(lienzo(bx, by, trasero=True))
    # cotas
    s.append(cota(fx, fy + H + 28, fx + W, fy + H + 28, f"{ANCHO_CM} cm"))
    s.append(cota(fx - 26, fy, fx - 26, fy + H, f"{LARGO_CM} cm"))
    s.append(cota(fx + (W - ESCOTE_W) / 2, fy - 8, fx + (W + ESCOTE_W) / 2, fy - 8, "escote 20 cm", "#a33"))
    s.append(cota(bx + (W - ESCOTE_W) / 2, by - 8, bx + (W + ESCOTE_W) / 2, by - 8, "escote 20 cm", "#a33"))
    s.append(cota(bx + W + 26, by, bx + W + 26, by + SISA, "sisa 26 cm", AZUL))
    s.append(cota(bx + W + 26, by + H - ABERTURA_LATERAL, bx + W + 26, by + H, "12 cm", TURQUESA))
    # leyenda
    s.append(leyenda(lx, fy - 6))
    # pie
    s.append(f'<text x="{fx}" y="{CH - 40}" font-family="{UI_FONT}" font-size="12" fill="#888">'
             f'Confección: dos lienzos rectangulares unidos en hombros y costados; escote cuadrado con guarda; bandas horizontales de cadenilla a máquina '
             f'(hilo de seda/rayón) y medallones en puntada de relleno.</text>')
    s.append(f'<text x="{fx}" y="{CH - 22}" font-family="{UI_FONT}" font-size="12" fill="#888">'
             f'Los motivos de Naruto son © Masashi Kishimoto / Shueisha; diseño de inspiración, no para uso comercial.</text>')
    s.append("</svg>")
    return "\n".join(s)


if __name__ == "__main__":
    out = Path(__file__).with_name("huipil-istmo-naruto.svg")
    out.write_text(hoja(), encoding="utf-8")
    print(f"escrito {out}")
