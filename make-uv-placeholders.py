#!/usr/bin/env python3
"""TEMPORARY. Fabricate stand-in "UV" frames so the crossfade can be reviewed
before the real blacklight shoot happens.

These are NOT photographs of the work under UV. Nobody has shot that yet.
They are the daylight frames darkened and pushed cool, purely so the toggle
mechanism is visible during review. Every pair rendered from these carries
data-uv="placeholder" in index.html, which paints a badge over the image and
turns on a site-wide notice in dark mode.

When the real shoot lands: drop <handle>-uv.png into raw/, run
./optimize-images.sh, delete the data-uv attributes, delete this script.
"""
from PIL import Image, ImageEnhance
import glob, os, colorsys

for src in sorted(glob.glob("images/*-day.webp")):
    out = src.replace("-day.webp", "-uv.webp")
    im = Image.open(src).convert("RGB")
    im = ImageEnhance.Color(im).enhance(2.4)     # push chroma
    im = ImageEnhance.Brightness(im).enhance(0.42)  # kill the room lights
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            hh, ss, vv = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            # saturated areas "fluoresce": lift value, drag hue toward cyan/violet
            if ss > 0.30:
                vv = min(1.0, vv * (1.0 + ss * 1.5))
                hh = (hh + 0.42) % 1.0
                ss = min(1.0, ss * 1.15)
            else:
                vv *= 0.35   # unpigmented ground goes to near-black
            r, g, b = colorsys.hsv_to_rgb(hh, ss, vv)
            px[x, y] = (int(r*255), int(g*255), int(b*255))
    im.save(out, "WEBP", quality=80, method=4)
    print(f"  {os.path.basename(out)}")
print(f"\n{len(glob.glob('images/*-uv.webp'))} placeholder frames. NOT real UV photography.")
