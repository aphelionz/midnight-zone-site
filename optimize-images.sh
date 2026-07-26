#!/usr/bin/env bash
# Convert the raw Shopify PNGs in raw/ into web-sized WebP in images/.
# Run locally, commit the output. CI never builds anything.
#
#   ./optimize-images.sh
#
# Naming: images/<shopify-handle>-day.webp  (daylight photograph)
#         images/<shopify-handle>-uv.webp   (under blacklight)
# Both are stacked in the page and crossfaded by the light/dark toggle.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p images
shopt -s nullglob
for src in raw/*.png raw/*.jpg raw/*.jpeg; do
  base="$(basename "${src%.*}")"
  out="images/${base}.webp"
  [ -e "$out" ] && [ "$out" -nt "$src" ] && continue
  cwebp -quiet -q 80 -resize 1200 0 -metadata none "$src" -o "$out"
  printf '%-34s %6s -> %6s\n' "$base" \
    "$(du -h "$src"  | cut -f1)" "$(du -h "$out" | cut -f1)"
done
echo "total: $(du -sh images | cut -f1)"
