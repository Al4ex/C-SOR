#!/usr/bin/env python3
"""Genera las láminas SVG del cuaderno de diseño.

    python3 tools/generar_laminas.py [destino]

Sin argumentos escribe en `laminas/`. Solo usa la biblioteca estándar.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from huipil.laminas import LAMINAS  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    destino = Path(argv[1]) if len(argv) > 1 else RAIZ / "laminas"
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, constructor in LAMINAS.items():
        ruta = destino / f"{nombre}.svg"
        ruta.write_text(constructor(), encoding="utf-8")
        print(f"  {ruta.relative_to(RAIZ) if RAIZ in ruta.parents else ruta}"
              f"  ({ruta.stat().st_size // 1024} kB)")
    print(f"\n{len(LAMINAS)} láminas escritas en {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
