# themidnightzone.art

Single-page site for **The Midnight Zone**, the UV-reactive paintings of Amy Chace, shown at Jon Sarkin's Fish City Studios in Gloucester, Massachusetts.

Single static `index.html`, no build step. Served via GitHub Pages at the custom domain `themidnightzone.art` (see `CNAME`). Same setup as [intelligence-community-site](https://github.com/aphelionz/intelligence-community-site) and [astra-perdita-site](https://github.com/aphelionz/astra-perdita-site).

## The idea

The light/dark switch is not chrome, it is the product. Light mode shows each painting photographed in daylight; dark mode shows the same painting under blacklight. Flipping the switch does to the page what flipping the switch does to the booth wall.

Two consequences for anyone editing this:

- **Every visitor lands in light mode**, on purpose. The pre-paint script in `<head>` deliberately ignores `prefers-color-scheme`, because here the mode is content rather than a preference. A visitor who never presses the switch never learns what the work does, so the control is header-level, sticky, and labelled in words (Daylight / Blacklight) rather than sun and moon icons alone.
- **Each card holds both photographs stacked**, crossfading on `opacity`. Never swap `src`: the transformation has to be watchable, and a swap that blinks kills the whole effect.

## Edit

Edit `index.html` and push to `main`. GitHub Pages redeploys automatically.

Local preview:

```bash
python3 -m http.server 8092
```

## Images

Originals from the Shopify CDN are multi-megabyte 16-bit PNGs (182 MB for 18 files), so they never go in the repo. Drop them in `raw/` (gitignored) named `<shopify-handle>-day.png` or `<shopify-handle>-uv.png`, then:

```bash
./optimize-images.sh
```

That writes ~1200px WebP at quality 80 into `images/`, which is what gets committed. CI never builds anything.

## Before launch

> [!IMPORTANT]
> The blacklight photographs **do not exist yet.** Nobody has shot this work under UV. The `-uv.webp` files currently in `images/` were fabricated by `make-uv-placeholders.py` from the daylight frames, purely so the switch could be reviewed.

They are marked in three places so they cannot ship by accident: a `simulated` badge on each image in dark mode, a dashed notice above the grid in dark mode, and a `data-uv="placeholder"` attribute on every `.pair`.

When the real shoot lands:

1. Put the UV frames in `raw/` as `<handle>-uv.png` and run `./optimize-images.sh`
2. Delete every `data-uv="placeholder"` attribute in `index.html`
3. Delete the `.notice` paragraph and its CSS block
4. Delete `make-uv-placeholders.py`
5. Regenerate `og.jpg` from a real blacklight frame

Also outstanding: the booth's UV wavelength (365nm vs 395nm) is still unmeasured, and the bundled lamp has not been specced.

## DNS

> [!NOTE]
> The domain file is currently parked as **`CNAME.pending`**, not `CNAME`.
>
> With a live `CNAME` file, Pages sets the custom domain immediately and the
> `github.io` URL redirects to it. Until DNS actually points at GitHub that
> redirect goes nowhere, which would break the review URL. So while this is in
> review the site lives at **https://aphelionz.github.io/midnight-zone-site/**.
>
> When DNS is in place: `git mv CNAME.pending CNAME`, push, then set the custom
> domain under Settings > Pages and tick Enforce HTTPS once the cert provisions.

Not documented in any of the sibling repos, so it is written down here. `themidnightzone.art` is an apex domain, so it needs A records rather than a CNAME record at the registrar:

```
A     185.199.108.153
A     185.199.109.153
A     185.199.110.153
A     185.199.111.153
AAAA  2606:50c0:8000::153
AAAA  2606:50c0:8001::153
AAAA  2606:50c0:8002::153
AAAA  2606:50c0:8003::153
```

Then in the repo: **Settings > Pages > Source = "GitHub Actions"**, and once the certificate provisions, tick **Enforce HTTPS** by hand. It is not automatic (it is on for theintelligencecommunity.art and off for astraperdita.com).

## Fonts

Self-hosted in `fonts/`, both OFL with licences alongside. **Deliberate deviation from the sibling sites, which use no webfonts at all** — but the zero-third-party-request rule still holds, because these are served same-origin. Never swap them for a Google Fonts `<link>`.

- **Fraunces** (display: h1, lede, h2, piece titles). Variable, four axes. `SOFT` bends the curves; `WONK` swaps in flowing alternates for `g h m n s`, which is most of what "The Midnight Zone" and "bathypelagic submersion" are made of.
- **Manrope** (body and UI). Quiet humanist sans, open apertures.

> [!WARNING]
> **Do not run `fraunces.woff2` through `pyftsubset` to save weight.**
>
> `WONK` works by GSUB `FeatureVariations`, and the subsetter does not close over those. It keeps the feature records but prunes the `.alt` glyphs they point at, so the axis silently goes inert and the headline quietly loses its character while everything still *looks* fine in code review. This was tried twice (Google's own served slice has the same problem) and caught by measuring the string `ghmns` at `WONK` 0 versus 1: if the two widths are identical, the axis is dead.
>
> The full face is 190KB, which is noise beside 4.3MB of artwork.

## Colours

Generated by Palette Forge, seed `ocean`, scheme `analogous`, mode `both`. Two locks, both measured rather than chosen:

**`accent` #8f00ff, the hue of 365nm.** Computed from the tabulated CIE 1931 2-degree standard observer: at 365nm the observer gives X=0.0002321, Y=0.000006965, Z=0.001086, a chromaticity of x=0.1752, y=0.0053, which is the violet corner of the spectral locus. That corner sits well outside sRGB, so it is desaturated 12.6% toward white to bring it into gamut, then normalised for lightness.

> [!NOTE]
> **365nm is invisible.** Human vision runs out around 380nm and the eye's response at 365nm is about 0.0065% of its peak at 555nm, which is exactly why a 365nm lamp looks nearly dark while everything else fluoresces. There is no honest sRGB value for 365nm at its true luminance; it is essentially black. `#8f00ff` is the chromaticity a 365nm stimulus would carry *if it were bright enough to see*.
>
> Useful consequence: the hue is flat across the whole near-UV band. 395nm computes to `#8e00ff`, one unit of red away. **The booth's unmeasured wavelength does not affect the palette**, so that open question can be closed for theming purposes.

Do not "fix" this by hand with a fitted approximation. The Wyman/Sloan/Shirley multi-lobe Gaussian fit to the CIE observer is only valid from roughly 380nm up, and below that it extrapolates non-physically (it returns cyan for 365nm). Use the tabulated data.

**`accent-2` #c15428**, the measured centroid of 38,917 saturated warm pixels across all eighteen paintings. Amy's work is roughly 62% reds through yellows with the blue band nearly empty, so the two locks land near-complementary and the violet room throws the work forward instead of competing with it.

Both modes pass WCAG AA with no adjustments and no outstanding contrast suggestions. If the UV photographs come back a dominant green, this palette is the first thing to revisit.

## Files

- `index.html` : the site
- `images/` : `<handle>-day.webp` and `<handle>-uv.webp` pairs, committed
- `raw/` : source PNGs, gitignored
- `optimize-images.sh` : raw PNG to web WebP
- `make-uv-placeholders.py` : temporary, delete after the real shoot
- `og.jpg` : social card
- `CNAME.pending` : custom domain, parked until DNS is live (see DNS above)
