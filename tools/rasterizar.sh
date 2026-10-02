#!/usr/bin/env bash
# Convierte las láminas SVG a PNG con Chrome headless (para previsualización
# en el README; las láminas SVG siguen siendo la fuente de verdad).
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ORIGEN="${1:-$RAIZ/laminas}"
DESTINO="${2:-$RAIZ/previews}"
CHROME="${CHROME:-google-chrome}"

mkdir -p "$DESTINO"
RAIZ_PERFILES="$(mktemp -d)"
trap 'rm -rf "$RAIZ_PERFILES"' EXIT

# Chrome headless deja el proceso vivo después de escribir la captura, así que
# cada invocación va envuelta en `timeout` y todas corren en paralelo.
captura() {
  local svg="$1" base w h
  base="$(basename "$svg" .svg)"
  read -r w h < <(sed -n 's/.*width="\([0-9.]*\)" height="\([0-9.]*\)".*/\1 \2/p' "$svg" | head -1)
  timeout 90 "$CHROME" --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
    --user-data-dir="$RAIZ_PERFILES/$base" \
    --force-device-scale-factor=1 \
    --window-size="${w%.*},${h%.*}" \
    --screenshot="$DESTINO/$base.png" "file://$svg" >/dev/null 2>&1 || true
  if [[ -f "$DESTINO/$base.png" ]]; then
    echo "  $DESTINO/$base.png  (${w%.*}x${h%.*})"
  else
    echo "  FALLÓ: $base" >&2
  fi
}

for svg in "$ORIGEN"/*.svg; do
  captura "$svg" &
done
wait
