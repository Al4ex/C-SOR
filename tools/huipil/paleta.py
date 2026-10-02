"""Paleta cromática del huipil istmeño shinobi.

Cada color cruza un tinte histórico del Istmo de Tehuantepec con un color
de la iconografía de Naruto, para que la prenda siga leyéndose como un
huipil y no como una camiseta impresa.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, NamedTuple


class Tinte(NamedTuple):
    clave: str
    nombre: str
    hex: str
    hilo: str
    lectura: str


PALETA: list[Tinte] = [
    Tinte("fondo", "Negro terciopelo", "#15111B", "Terciopelo de algodón",
          "Fondo clásico del huipil de Tehuantepec; noche del Istmo"),
    Tinte("naranja", "Naranja nindō", "#F0801E", "Seda floja n.º 208",
          "Naranja del traje de Naruto, usado como el amarillo de los pétalos"),
    Tinte("rojo", "Rojo Uzumaki", "#C32730", "Seda floja n.º 112",
          "Remolino del clan y grana de las rosas istmeñas"),
    Tinte("cochinilla", "Grana cochinilla", "#8E1B33", "Lana teñida en grana",
          "Sombra de los pétalos; tinte oaxaqueño de nopal"),
    Tinte("verde", "Verde hoja", "#2F7D53", "Seda floja n.º 316",
          "Hoja de Konoha y follaje de los huipiles de cadenilla"),
    Tinte("anil", "Azul añil", "#1E4C96", "Algodón teñido en añil",
          "Chaleco chūnin y añil de los telares del Istmo"),
    Tinte("amarillo", "Amarillo sannin", "#F2C230", "Seda floja n.º 044",
          "Corazón de las flores y cabello del Cuarto Hokage"),
    Tinte("morado", "Morado istmeño", "#5B2A86", "Terciopelo alterno",
          "Variante de fondo para huipil de fiesta"),
    Tinte("plata", "Plata hitai-ate", "#BFC4CB", "Hilo metálico laminado",
          "Placa metálica de la banda ninja, bordada en cadenilla"),
    Tinte("oro", "Oro cadenilla", "#D9A334", "Hilo de oro entorchado",
          "Contornos y randas, como en el huipil de cadenilla"),
    Tinte("manta", "Blanco manta", "#F6F0E3", "Algodón crudo",
          "Base del telar de cintura y de la camisa de manta del hombre"),
    Tinte("humo", "Gris humo", "#6E6A78", "Algodón mercerizado",
          "Trazos auxiliares y sombras de la placa metálica"),
]

C: dict[str, str] = {t.clave: t.hex for t in PALETA}

PAPEL = "#0C0A10"
PAPEL_CLARO = "#17141E"
TINTA = "#EDE7DA"
TINTA_SUAVE = "#9A94A6"
GUIA = "#4A4456"


def _canales(hexa: str) -> tuple[int, int, int]:
    h = hexa.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def reves(fondo: str | None = None) -> str:
    """Color del revés de la tela, visto por el hueco del cuello.

    Un fondo oscuro se aclara y uno claro se oscurece: así el hueco siempre
    se lee como tela vuelta y no como un agujero en el papel del dibujo.
    """
    r, g, b = _canales(fondo or C["fondo"])
    claro = (0.299 * r + 0.587 * g + 0.114 * b) > 110
    mezcla, peso = ((0, 0, 0), 0.46) if claro else ((255, 255, 255), 0.13)
    return "#%02X%02X%02X" % tuple(
        round(c + (m - c) * peso) for c, m in zip((r, g, b), mezcla)
    )


@contextmanager
def variante(cambios: dict[str, str]) -> Iterator[None]:
    """Sustituye tintes de la paleta mientras se dibuja una variante de color."""
    previos = {clave: C[clave] for clave in cambios}
    C.update(cambios)
    try:
        yield
    finally:
        C.update(previos)


VARIANTES = [
    ("Gala — terciopelo negro", "Vela, bodas y mayordomías", {}),
    ("Diario — manta cruda", "Camisa de trabajo y fiesta chica",
     {"fondo": "#EFE6D2", "plata": "#7D8795", "oro": "#A8761B", "manta": "#2A2430"}),
    ("Vela nocturna — morado", "Baile de la Vela, hombres del son",
     {"fondo": "#30124A", "anil": "#102E6E", "cochinilla": "#6E1230"}),
]
