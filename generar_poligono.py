#!/usr/bin/env python3
"""Genera una imagen satelital con el polígono del predio a partir de sus vértices.

Uso:
    python3 generar_poligono.py

Los datos del predio se editan en la sección PREDIO de este archivo.
La imagen de fondo son mosaicos de Esri World Imagery.
"""

import io
import math
import urllib.request

from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------- #
# PREDIO
# --------------------------------------------------------------------------- #
PROGRAMA = "PRODUCCION PARA EL BIENESTAR 2026"
PRODUCTOR = "RAÚL CRUZ JOAQUÍN"
PREDIO = "ARROYO MAMEY"
ESTADO = "OAXACA"
LOCALIDAD = "THE REAL"

# (vértice, latitud, longitud) en el orden en que se recorre el perímetro
VERTICES = [
    ("1", 17.094392, -95.121977),
    ("2", 17.094149, -95.120135),
    ("3", 17.092351, -95.120284),
    ("4", 17.092622, -95.122197),
]

COLINDANCIAS = {
    "NORTE": "ARMANDO GUZMÁN MÉNDEZ",
    "SUR": "EJIDO DE BUENA VISTA",
    "ESTE": "EJIDO DE BUENA VISTA",
    "OESTE": "NICASIO LUIS ARAGÓN",
}

SALIDA = "imagen_satelital_poligono.png"

# --------------------------------------------------------------------------- #
# Mosaicos / proyección Web Mercator
# --------------------------------------------------------------------------- #
TILE_URL = (
    "https://services.arcgisonline.com/ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"
)
TILE = 256
ANCHO, ALTO = 1600, 1150  # tamaño del mapa
BANDA = 215  # franja de datos debajo del mapa
MARGEN = 0.13  # fracción del encuadre que queda libre alrededor del polígono
# El encuadre se corre unos píxeles para que el polígono no choque con el
# cuadro del encabezado; mapa y polígono se desplazan juntos.
DESPLAZAMIENTO = (26, 46)


def lonlat_a_pixel(lon, lat, z):
    n = TILE * 2**z
    x = (lon + 180.0) / 360.0 * n
    s = math.sin(math.radians(lat))
    y = (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n
    return x, y


def descargar_tile(z, x, y):
    url = TILE_URL.format(z=z, x=x, y=y)
    req = urllib.request.Request(url, headers={"User-Agent": "poligono-predio/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGB")


def elegir_zoom(lats, lons):
    """Zoom más detallado con el que el polígono (más margen) cabe en el lienzo."""
    for z in range(19, 13, -1):
        xs, ys = zip(*(lonlat_a_pixel(lo, la, z) for la, lo in zip(lats, lons)))
        ancho_util = ANCHO * (1 - 2 * MARGEN)
        alto_util = ALTO * (1 - 2 * MARGEN)
        if max(xs) - min(xs) <= ancho_util and max(ys) - min(ys) <= alto_util:
            return z
    return 14


def mosaico(centro_px, z, escala):
    """Fondo satelital del encuadre, tomando los mosaicos del zoom z.

    Con escala > 1 se piden menos mosaicos y se amplía la imagen, que es la
    única salida cuando el zoom necesario no tiene imagen publicada.
    """
    w, h = ANCHO / escala, ALTO / escala
    x0, y0 = centro_px[0] - w / 2, centro_px[1] - h / 2
    t_x0, t_y0 = math.floor(x0 / TILE), math.floor(y0 / TILE)
    t_x1, t_y1 = math.floor((x0 + w) / TILE), math.floor((y0 + h) / TILE)

    fondo = Image.new("RGB", (math.ceil(w), math.ceil(h)), (40, 40, 40))
    for tx in range(t_x0, t_x1 + 1):
        for ty in range(t_y0, t_y1 + 1):
            try:
                t = descargar_tile(z, tx, ty)
            except Exception:
                continue
            fondo.paste(t, (int(tx * TILE - x0), int(ty * TILE - y0)))
    return fondo, (x0, y0)


def sin_imagen(fondo):
    """Proporción de píxeles del gris plano que Esri usa donde no hay imagen."""
    m = fondo.resize((80, 60))
    grises = sum(
        1 for r, g, b in m.getdata()
        if abs(r - g) < 6 and abs(g - b) < 6 and 170 < r < 225
    )
    return grises / (80 * 60)


def fondo_disponible(centro_lonlat, lats, lons):
    """Baja de zoom hasta encontrar imagen satelital real y la amplía al lienzo."""
    z_ideal = elegir_zoom(lats, lons)
    for z in range(z_ideal, 14, -1):
        escala = min(2 ** (z_ideal - z), 2)
        cx, cy = lonlat_a_pixel(*centro_lonlat, z)
        centro = (cx - DESPLAZAMIENTO[0] / escala,
                  cy - DESPLAZAMIENTO[1] / escala)
        fondo, origen = mosaico(centro, z, escala)
        if sin_imagen(fondo) < 0.25 or z == 15:
            if escala != 1:
                fondo = fondo.resize((ANCHO, ALTO), Image.LANCZOS)
            return fondo, origen, z, escala
    raise RuntimeError("sin imagen satelital disponible para estas coordenadas")


# --------------------------------------------------------------------------- #
# Geometría
# --------------------------------------------------------------------------- #
def area_y_perimetro(vertices):
    """Área (ha) y perímetro (m) por proyección plana local equirrectangular."""
    lat0 = sum(v[1] for v in vertices) / len(vertices)
    m_lat = 111132.92 - 559.82 * math.cos(2 * math.radians(lat0))
    m_lon = 111412.84 * math.cos(math.radians(lat0))
    pts = [((lo - vertices[0][2]) * m_lon, (la - vertices[0][1]) * m_lat)
           for _, la, lo in vertices]

    s = 0.0
    per = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
        per += math.hypot(x2 - x1, y2 - y1)
    return abs(s) / 2 / 10000, per


def fuente(tam, negrita=False):
    nombres = (
        ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"] if negrita
        else ["DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
    )
    for n in nombres:
        try:
            return ImageFont.truetype(n, tam)
        except OSError:
            continue
    return ImageFont.load_default(tam)


def caja_texto(draw, xy, lineas, f, pad=10, fondo=(255, 255, 255, 225),
               borde=(0, 0, 0, 255), color=(0, 0, 0, 255), ancho_min=0):
    alto_l = f.size + 6
    ancho = max(ancho_min, max(draw.textlength(t, font=f) for t in lineas) + 2 * pad)
    alto = alto_l * len(lineas) + 2 * pad - 6
    x, y = xy
    draw.rectangle([x, y, x + ancho, y + alto], fill=fondo, outline=borde, width=2)
    for i, t in enumerate(lineas):
        draw.text((x + pad, y + pad + i * alto_l), t, font=f, fill=color)
    return ancho, alto


def main():
    lats = [v[1] for v in VERTICES]
    lons = [v[2] for v in VERTICES]
    centro_lonlat = ((min(lons) + max(lons)) / 2, (min(lats) + max(lats)) / 2)

    img, (ox, oy), z, escala = fondo_disponible(centro_lonlat, lats, lons)
    img = img.convert("RGBA")
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)

    pts = []
    for _, la, lo in VERTICES:
        px, py = lonlat_a_pixel(lo, la, z)
        pts.append(((px - ox) * escala, (py - oy) * escala))

    # Polígono: relleno translúcido + contorno amarillo
    d.polygon(pts, fill=(255, 235, 0, 45))
    d.line(pts + [pts[0]], fill=(255, 235, 0, 255), width=5, joint="curve")

    f_vert = fuente(26, negrita=True)
    f_txt = fuente(22)
    f_tit = fuente(30, negrita=True)
    f_chico = fuente(19)

    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)

    # Vértices numerados, con la etiqueta hacia afuera del polígono
    for (etq, _, _), (px, py) in zip(VERTICES, pts):
        r = 9
        d.ellipse([px - r, py - r, px + r, py + r],
                  fill=(255, 0, 0, 255), outline=(255, 255, 255, 255), width=3)
        tw = d.textlength(etq, font=f_vert) + 14
        th = f_vert.size + 10
        dx, dy = px - cx, py - cy
        norma = math.hypot(dx, dy) or 1
        bx = px + dx / norma * 26 - tw / 2
        by = py + dy / norma * 26 - th / 2
        d.rectangle([bx, by, bx + tw, by + th], fill=(0, 0, 0, 180))
        d.text((bx + 7, by + 5), etq, font=f_vert, fill=(255, 235, 0, 255))

    # Colindancias sobre cada lado del encuadre
    posiciones = {
        "NORTE": (cx, min(p[1] for p in pts) - 78),
        "SUR": (cx, max(p[1] for p in pts) + 50),
        "ESTE": (max(p[0] for p in pts) + 56, cy),
        "OESTE": (min(p[0] for p in pts) - 56, cy),
    }
    for rumbo, (tx, ty) in posiciones.items():
        texto = f"{rumbo}: {COLINDANCIAS[rumbo]}"
        tw = d.textlength(texto, font=f_chico)
        if rumbo == "ESTE":
            x = tx
        elif rumbo == "OESTE":
            x = tx - tw - 16
        else:
            x = tx - tw / 2 - 8
        y = ty if rumbo in ("NORTE", "SUR") else ty - f_chico.size / 2 - 5
        d.rectangle([x, y, x + tw + 16, y + f_chico.size + 10],
                    fill=(0, 0, 0, 165))
        d.text((x + 8, y + 5), texto, font=f_chico, fill=(255, 255, 255, 255))

    # Encabezado
    caja_texto(
        d, (24, 24),
        [f"PREDIO: {PREDIO}", f"PRODUCTOR: {PRODUCTOR}",
         f"{LOCALIDAD}, {ESTADO}", PROGRAMA],
        f_txt, pad=14,
    )

    # Escala gráfica
    res = (156543.03392 * math.cos(math.radians(sum(lats) / len(lats)))
           / (2**z) / escala)
    for metros in (300, 200, 150, 100, 50, 25):
        largo = metros / res
        if largo <= 300:
            break
    ex, ey = ANCHO - largo - 60, ALTO - 70
    d.rectangle([ex - 14, ey - 34, ex + largo + 14, ey + 22],
                fill=(255, 255, 255, 215), outline=(0, 0, 0, 255), width=2)
    mitad = largo / 2
    d.rectangle([ex, ey, ex + mitad, ey + 12], fill=(0, 0, 0, 255))
    d.rectangle([ex + mitad, ey, ex + largo, ey + 12],
                fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
    d.text((ex, ey - 30), "0", font=f_chico, fill=(0, 0, 0, 255))
    d.text((ex + largo - d.textlength(f"{metros} m", font=f_chico), ey - 30),
           f"{metros} m", font=f_chico, fill=(0, 0, 0, 255))

    # Norte
    nx, ny = ANCHO - 80, 60
    d.ellipse([nx - 42, ny - 32, nx + 42, ny + 86], fill=(255, 255, 255, 200),
              outline=(0, 0, 0, 255), width=2)
    d.polygon([(nx, ny - 22), (nx - 16, ny + 34), (nx, ny + 22), (nx + 16, ny + 34)],
              fill=(0, 0, 0, 255))
    d.text((nx - d.textlength("N", font=f_tit) / 2, ny + 38), "N",
           font=f_tit, fill=(0, 0, 0, 255))

    # Crédito del fondo
    credito = "Imagen: Esri World Imagery / Maxar"
    d.text((ANCHO - d.textlength(credito, font=f_chico) - 16, ALTO - 26),
           credito, font=f_chico, fill=(255, 255, 255, 230))

    mapa = Image.alpha_composite(img, capa).convert("RGB")

    # Banda de datos debajo del mapa
    area, per = area_y_perimetro(VERTICES)
    final = Image.new("RGB", (ANCHO, ALTO + BANDA), (255, 255, 255))
    final.paste(mapa, (0, 0))
    b = ImageDraw.Draw(final)
    b.rectangle([0, 0, ANCHO - 1, ALTO + BANDA - 1], outline=(0, 0, 0), width=3)
    b.line([0, ALTO, ANCHO, ALTO], fill=(0, 0, 0), width=3)

    f_enc = fuente(23, negrita=True)
    y0 = ALTO + 18
    paso = 28
    negro = (0, 0, 0)

    b.text((30, y0), "COORDENADAS (WGS84)", font=f_enc, fill=negro)
    cols = (30, 190, 360)
    for col, enc in zip(cols, ("VÉRTICE", "LATITUD", "LONGITUD")):
        b.text((col, y0 + paso), enc, font=f_enc, fill=negro)
    for i, (etq, la, lo) in enumerate(VERTICES):
        y = y0 + paso * (2 + i)
        for col, val in zip(cols, (etq, f"{la:.6f}", f"{lo:.6f}")):
            b.text((col, y), val, font=f_txt, fill=negro)
    b.line([cols[0], y0 + paso * 2 - 5, 560, y0 + paso * 2 - 5],
           fill=negro, width=1)

    b.text((660, y0), "COLINDANCIAS", font=f_enc, fill=negro)
    for i, (rumbo, nombre) in enumerate(COLINDANCIAS.items()):
        y = y0 + paso * (1 + i)
        b.text((660, y), f"{rumbo}:", font=f_enc, fill=negro)
        b.text((780, y), nombre, font=f_txt, fill=negro)

    b.text((1230, y0), "SUPERFICIE Y PERÍMETRO", font=f_enc, fill=negro)
    b.text((1230, y0 + paso), f"SUPERFICIE APROX.: {area:.2f} ha",
           font=f_txt, fill=negro)
    b.text((1230, y0 + paso * 2), f"PERÍMETRO APROX.: {per:.0f} m",
           font=f_txt, fill=negro)
    b.text((1230, y0 + paso * 4),
           "Cálculo a partir de los vértices;", font=f_chico, fill=(90, 90, 90))
    b.text((1230, y0 + paso * 5),
           "verificar con levantamiento en campo.", font=f_chico,
           fill=(90, 90, 90))

    final.save(SALIDA)
    final.save(SALIDA.rsplit(".", 1)[0] + ".jpg", quality=92)
    print(f"{SALIDA}  zoom={z}  escala={escala}  "
          f"{area:.2f} ha  perímetro {per:.0f} m")


if __name__ == "__main__":
    main()
