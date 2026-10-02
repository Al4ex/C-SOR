"""Utilidades mínimas para escribir SVG a mano, sin dependencias externas."""

from __future__ import annotations

import math
from typing import Iterable, Sequence

TIPO = "DejaVu Sans, Verdana, Geneva, sans-serif"
TIPO_TITULO = "DejaVu Serif, Georgia, 'Times New Roman', serif"
TIPO_MONO = "DejaVu Sans Mono, Menlo, Consolas, monospace"


def n(v: float) -> str:
    """Formatea un número para SVG sin ceros sobrantes."""
    s = f"{float(v):.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def attrs(**kw) -> str:
    partes = []
    for clave, valor in kw.items():
        if valor is None:
            continue
        nombre = clave.rstrip("_").replace("__", ":").replace("_", "-")
        if isinstance(valor, float):
            valor = n(valor)
        partes.append(f'{nombre}="{valor}"')
    return " ".join(partes)


def el(tag: str, cuerpo: str | None = None, **kw) -> str:
    a = attrs(**kw)
    sep = " " if a else ""
    if cuerpo is None:
        return f"<{tag}{sep}{a}/>"
    return f"<{tag}{sep}{a}>{cuerpo}</{tag}>"


def grupo(cuerpo: str | Iterable[str], **kw) -> str:
    if not isinstance(cuerpo, str):
        cuerpo = "".join(cuerpo)
    return el("g", cuerpo, **kw)


def ruta(d: str, **kw) -> str:
    return el("path", d=d, **kw)


def rectangulo(x: float, y: float, w: float, h: float, **kw) -> str:
    return el("rect", x=n(x), y=n(y), width=n(w), height=n(h), **kw)


def circulo(cx: float, cy: float, r: float, **kw) -> str:
    return el("circle", cx=n(cx), cy=n(cy), r=n(r), **kw)


def elipse(cx: float, cy: float, rx: float, ry: float, **kw) -> str:
    return el("ellipse", cx=n(cx), cy=n(cy), rx=n(rx), ry=n(ry), **kw)


def linea(x1: float, y1: float, x2: float, y2: float, **kw) -> str:
    return el("line", x1=n(x1), y1=n(y1), x2=n(x2), y2=n(y2), **kw)


def texto(x: float, y: float, contenido: str, tam: float = 14, color: str = "#F6F0E3",
          familia: str = TIPO, anclaje: str = "start", peso: str = "normal",
          espaciado: float | None = None, opacidad: float | None = None,
          italica: bool = False) -> str:
    return el(
        "text",
        escapar(contenido),
        x=n(x),
        y=n(y),
        fill=color,
        font_family=familia,
        font_size=n(tam),
        font_weight=peso,
        font_style="italic" if italica else None,
        text_anchor=anclaje,
        letter_spacing=None if espaciado is None else n(espaciado),
        opacity=None if opacidad is None else n(opacidad),
    )


def escapar(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def polilinea(puntos: Sequence[tuple[float, float]], cerrada: bool = False) -> str:
    if not puntos:
        return ""
    d = "M " + " L ".join(f"{n(x)},{n(y)}" for x, y in puntos)
    return d + " Z" if cerrada else d


def colocar(cuerpo: str, cx: float, cy: float, lado: float, rot: float = 0.0,
            base: float = 100.0, **kw) -> str:
    """Coloca un motivo dibujado en una caja local `base`x`base` centrado en (cx, cy)."""
    s = lado / base
    t = (
        f"translate({n(cx)},{n(cy)}) "
        f"rotate({n(rot)}) "
        f"scale({n(s)}) "
        f"translate({n(-base / 2)},{n(-base / 2)})"
    )
    return grupo(cuerpo, transform=t, **kw)


def documento(ancho: float, alto: float, cuerpo: str, defs: str = "") -> str:
    bloque_defs = el("defs", defs) if defs else ""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{n(ancho)}" height="{n(alto)}" '
        f'viewBox="0 0 {n(ancho)} {n(alto)}">\n'
        f"{bloque_defs}\n{cuerpo}\n</svg>\n"
    )


def polar(cx: float, cy: float, r: float, grados: float) -> tuple[float, float]:
    a = math.radians(grados)
    return cx + r * math.cos(a), cy + r * math.sin(a)
