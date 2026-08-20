#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Emit the GRU953 Soaring Bird — ONE drawing, plus the tile.

There is exactly one bird. Earlier there were three builds (Detail, Core, Glyph) meant to
serve different sizes; they were separate constructions and they drifted, and the smallest one
ended up with its wing severed from the body. One drawing cannot drift from itself.

The bird is the union of Aninda's own master drawing: sub-path 0 is the outer contour, and
every other sub-path is an interior counter cut out of it. Nothing is redrawn, thickened,
simplified or re-traced — the file that ships is his line art, exactly.

Below 24px the bare mark's strokes thin out, so the TILE is used instead: the same bird in
Daybreak on a Meridian square. The tile's block of colour carries recognition at sizes where
a line drawing cannot.

THIS IS THE PRE-REBUILD MARK, NOT THE FINAL ONE. The confirmed rebuild plan (kept outside
this repo, in the owner's own planning notes -- not referenced by path here, since a path
useful on one machine is meaningless on a clone) keeps the Soaring Bird concept but rebuilds
its geometry on a stated construction grid so it works natively at a 16px floor, with the
owner's own drawing as the reference rather than the shipped file (see
check_rebuild_fidelity.py, the fidelity harness that rebuild will be measured against). Until
that rebuild replaces it, this file keeps the current 24px-floor, ship-the-original-verbatim
approach working and honest.

Run:
    PLAYWRIGHT_BROWSERS_PATH="$(pwd)/00_sandbox/browsers" ./.venv/bin/python \
        brand-kit/03_logo/marks.py
"""
import io
import json
import pathlib
import re
import subprocess
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
# Resolved from THIS FILE, not typed. An absolute path baked in here worked on exactly
# one machine — the one the kit was built on — and made every clone of this
# repository fail at the first svgo call.
SANDBOX = str(pathlib.Path(__file__).resolve().parent.parent / "00_sandbox")
TILE_INSET = 0.19          # the bird's ink occupies the middle 62% of the tile
# A GRU953 house choice, NOT a platform requirement. Verified 20 August 2026 against
# Apple's own current app-icon guidance: it states no corner radius, no percentage, no
# squircle value anywhere -- the mask is designed to "precisely match... the bezel of
# the physical device itself", so no fixed percentage can be right for Apple's own
# masked platforms. This file's own earlier version claimed the opposite ("the squircle
# corner radius iOS and Android both expect") in both a code comment and this SVG's own
# screen-reader-audible <desc> -- a false claim a screen reader was, until this fix,
# announcing as fact. Android's adaptive-icon system masks every launcher icon itself
# regardless of this value, so in practice this radius only ever matters on platforms
# that do not mask the icon at all (the bare web/README/social use of this same file).
TILE_RADIUS = 0.2246


def preflight_chromium():
    """See measure_original.py's own preflight_chromium for the reasoning -- a
    missing browser install must exit 2 (not equipped), never crash into exit 1
    (a real failure) or silently pass."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
    except Exception as e:
        print(f"NOT EQUIPPED: Chromium did not launch ({e}). Run: "
              f"sh 00_sandbox/setup.sh (with PLAYWRIGHT_BROWSERS_PATH set to "
              f"$(pwd)/00_sandbox/browsers) and re-run this script.")
        sys.exit(2)


def optimise(p):
    """Shrink the file without breaking its accessible name.

    The settings live in 00_sandbox/svgo.config.mjs, and the important one is cleanupIds
    being off: svgo renames <title id="t"> but does not rewrite the root's
    aria-labelledby="t d", so the accessible name would resolve to nothing.

    This used to pass `--disable=...`, which this version of svgo does not accept. It
    rejected the whole run, the error went into a swallowed capture_output, and the file was
    never optimised at all. Failures are now reported and the good file is kept.
    """
    before = p.read_bytes()
    r = subprocess.run(["npx", "--no-install", "svgo", "--config", "svgo.config.mjs",
                        str(p), "-o", str(p)], cwd=SANDBOX, capture_output=True, text=True)
    out = p.read_bytes()
    if r.returncode != 0 or len(out) < 200 or b"<svg" not in out:
        p.write_bytes(before)
        print(f"  ! svgo did not optimise {p.name}: "
              f"{(r.stderr or r.stdout).strip().splitlines()[:1]} — kept the original")


def bird_path():
    """Aninda's master path, verbatim.

    Earlier this flattened the curves to polygons and re-computed the counters with polygon
    arithmetic. That produced a 60 kB file of straight-line chords — six times the size, and
    an approximation of a drawing that was already exact. The master path's counters are
    already wound opposite to its outer contour, which is precisely what fill-rule="nonzero"
    needs, so no computation is required at all. The mark IS the drawing.
    """
    src = (HERE / "original/GRU953-logo-master.svg").read_text()
    d = re.search(r'\sd="([^"]+)"', src).group(1)
    return re.sub(r"\s+", " ", d.replace("&#xA;", " ").replace("&#x9;", " ")).strip()


def inked_bbox():
    """The bird's own inked bounding box, in artboard units.

    Read from original-measurements.json (measure_original.py) rather than computed here
    a second way: that figure comes from real rendered pixels, cross-checked at 1x and 4x
    render scale, which is a MORE faithful answer to "where is the ink" than an analytic
    bounding box over Bezier control points -- a control-point box can be looser than the
    curve's own true extent. Requires measure_original.py to have been run first; fails
    loudly rather than silently computing a second, less-verified number if it hasn't.
    """
    path = HERE / "original-measurements.json"
    if not path.exists():
        print(f"FAIL: {path.name} does not exist. Run measure_original.py first -- "
              f"this file reads the inked bounding box from its output rather than "
              f"recomputing a second, less-verified version of the same figure.")
        sys.exit(1)
    data = json.loads(path.read_text(encoding="utf-8"))
    b = data["measurements_by_render_scale"][0]["inked_bbox_artboard_units"]
    return b["x"], b["y"], b["x"] + b["width"], b["y"] + b["height"]


D = bird_path()

MARK = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" '
    'role="img" aria-labelledby="t d">'
    '<title id="t">GRU953 Soaring Bird</title>'
    '<desc id="d">The GRU953 Soaring Bird: a climbing bird drawn in fine lines, its wing '
    'fanned into four facets. Used at 24px and above; below that the tile is used instead.'
    '</desc>'
    f'<path fill="currentColor" fill-rule="nonzero" d="{D}"/></svg>')
mp = HERE / "GRU953-bird.svg"
mp.write_text(MARK)
optimise(mp)

S = 1024.0
# Fit and centre the bird's INKED bounding box, not its viewBox. The master drawing carries
# its own padding and is wider than it is tall, so scaling the viewBox left the bird small
# and sitting off-centre inside the tile. Measure the ink, fit that.
_x0, _y0, _x1, _y1 = inked_bbox()
_bw, _bh = _x1 - _x0, _y1 - _y0
_box = S * (1 - 2 * TILE_INSET)
_sc = _box / max(_bw, _bh)
_tx, _ty = (S - _bw * _sc) / 2 - _x0 * _sc, (S - _bh * _sc) / 2 - _y0 * _sc
TILE = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" '
    'height="1024" role="img" aria-labelledby="at ad">'
    '<title id="at">GRU953 app icon</title>'
    '<desc id="ad">The GRU953 Soaring Bird in Daybreak on a Meridian tile, on a rounded '
    'square (a GRU953 house choice, not a platform requirement -- neither Apple nor '
    'Android publishes a fixed app-icon corner radius). Used wherever the bare mark '
    'would be smaller than 24px.</desc>'
    f'<rect width="1024" height="1024" rx="{S * TILE_RADIUS:.1f}" fill="#1A1753"/>'
    f'<g transform="translate({_tx:.2f} {_ty:.2f}) scale({_sc:.6f})" '
    f'color="#FFAB8E"><path fill="currentColor" fill-rule="nonzero" d="{D}"/></g></svg>')
tp = HERE / "GRU953-appicon.svg"
tp.write_text(TILE)
optimise(tp)

print(f"GRU953-bird.svg      {mp.stat().st_size:7,} bytes   "
      f"(the master path, verbatim — {D.count('M')} sub-paths, curves intact)")
print(f"GRU953-appicon.svg   {tp.stat().st_size:7,} bytes")

# ---------------------------------------------------------------- the size gate
#
# THE CLAIM BEING TESTED: at 24px this is still recognisably THIS bird, because the holes
# inside the wing are still holes.
#
# An earlier version of this gate measured the fraction of near-white pixels across the
# WHOLE canvas and called that "the counters are open". That is not the same test at all —
# a blank canvas passes it, and so would a solid rectangle with a wide white margin. It
# could not tell "the wing's holes filled in" from "there is a lot of empty space around
# the drawing".
#
# What is measured now: the enclosed white regions INSIDE the drawing's own bounding box.
# The mark is rasterised, the white area connected to the outside border is flooded away,
# and what survives is exactly the set of interior counters. Their COUNT is compared with
# the count at a large size, where they are certainly all open. If any counter has silted
# up, the count drops, and the file is not written.
#
# Rendered through Chromium (Playwright), the same renderer every other measurement in this
# kit uses -- not rsvg-convert, which this file called until this fix and which is not
# installed anywhere in this project's own sandbox (Phase 1 of the rebuild replaced it with
# Chromium everywhere else; this was the one place that substitution had not yet reached).
# Pure Python throughout, no numpy: the same flood-fill and connected-component technique
# already proven in measure_original.py's enclosed_mask()/find_counters(), applied here to
# the SHIPPED bird at several small sizes instead of the ORIGINAL drawing at one large size.
def render_ink_mask(svg_text: str, px: int) -> list:
    html = f"""<!doctype html><html><head><style>
      html, body {{ margin: 0; padding: 0; background: #fff; }}
      svg {{ display: block; width: {px}px; height: {px}px; }}
    </style></head><body>{svg_text}</body></html>"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": px, "height": px})
        page.set_content(html)
        page.wait_for_timeout(50)
        png_bytes = page.screenshot()
        browser.close()
    img = Image.open(io.BytesIO(png_bytes)).convert("L")
    assert img.size == (px, px), f"expected {px}x{px}, got {img.size}"
    data = img.load()
    # ink is black; anything light (>170) is background -- same threshold this file's
    # numpy version used, kept identical so the size-gate's own pass/fail is unaffected.
    return [[data[x, y] <= 170 for x in range(px)] for y in range(px)]


def enclosed_mask(px: int) -> list:
    """Rasterise the mark at `px` and return the mask of white pixels ENCLOSED by ink.

    White that can be reached from the border is outside the drawing; what cannot be
    reached is a counter. This is the only way to ask the question that matters — "are the
    holes in the wing still holes?" — rather than the question a whole-canvas pixel count
    actually answers, which is "is there a lot of empty space around the drawing?"
    """
    is_ink = render_ink_mask(mp.read_text().replace("currentColor", "#000"), px)
    is_white = [[not v for v in row] for row in is_ink]
    h, w = len(is_white), len(is_white[0])
    outside = [[False] * w for _ in range(h)]
    stack = ([(0, x) for x in range(w) if is_white[0][x]]
             + [(h - 1, x) for x in range(w) if is_white[h - 1][x]]
             + [(y, 0) for y in range(h) if is_white[y][0]]
             + [(y, w - 1) for y in range(h) if is_white[y][w - 1]])
    while stack:
        y, x = stack.pop()
        if outside[y][x] or not is_white[y][x]:
            continue
        outside[y][x] = True
        if y: stack.append((y - 1, x))
        if x: stack.append((y, x - 1))
        if y < h - 1: stack.append((y + 1, x))
        if x < w - 1: stack.append((y, x + 1))
    return [[is_white[y][x] and not outside[y][x] for x in range(w)] for y in range(h)]


def reference_counters(px=512, min_area=40):
    """The mark's real counters, measured where they are certainly all open.

    Returns one normalised centroid per counter, so each can be looked for again at a
    smaller size. Counting regions at a small size instead would be meaningless:
    antialiasing splits a single counter into several specks and the count goes UP as the
    mark degrades.
    """
    m = enclosed_mask(px)
    h, w = len(m), len(m[0])
    seen = [[False] * w for _ in range(h)]
    out = []
    for y in range(h):
        for x in range(w):
            if m[y][x] and not seen[y][x]:
                pts, st = [], [(y, x)]
                while st:
                    cy, cx = st.pop()
                    if seen[cy][cx] or not m[cy][cx]:
                        continue
                    seen[cy][cx] = True
                    pts.append((cy, cx))
                    for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                        if 0 <= ny < h and 0 <= nx < w:
                            st.append((ny, nx))
                if len(pts) >= min_area:
                    out.append((sum(q[0] for q in pts) / len(pts) / h,
                                sum(q[1] for q in pts) / len(pts) / w))
    return out


def counters_surviving(px, refs):
    """How many of the reference counters are still open at `px`.

    A counter counts as open if the pixel at its centroid, or any of its eight neighbours,
    is still enclosed white. The neighbourhood allows for rounding when a 512px centroid is
    mapped onto a 24px grid; it does not let a closed counter pass, because a closed counter
    has no enclosed white anywhere near its centre.
    """
    m = enclosed_mask(px)
    h, w = len(m), len(m[0])
    alive = 0
    for fy, fx in refs:
        y, x = min(h - 1, int(round(fy * h))), min(w - 1, int(round(fx * w)))
        if any(m[min(h - 1, max(0, y + dy))][min(w - 1, max(0, x + dx))]
               for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
            alive += 1
    return alive


def main():
    preflight_chromium()

    refs = reference_counters()
    print(f"  the mark has {len(refs)} interior counters, measured at 512px")
    survive = {}
    for px in (32, 24, 20, 16):
        survive[px] = counters_surviving(px, refs)
        print(f"  at {px}px: {survive[px]} of {len(refs)} still open"
              + ("   <- the documented floor" if px == 24 else ""))

    floor = 24
    if survive[floor] < len(refs):
        print(f"FAIL — only {survive[floor]} of the mark's {len(refs)} interior "
              f"counters survive at {floor}px, the documented floor. The wing has "
              f"silted up. Do not ship.")
        return 1
    print(f"PASS — all {len(refs)} interior counters are still open at the "
          f"documented {floor}px floor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
