#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Measure the owner's original Soaring Bird drawing — groundwork for the mark rebuild.

The rebuild reconstructs the bird on a stated construction grid, with the owner's own
drawing as the REFERENCE it must match, not the file that ships. Before any grid can be
drawn, the reference itself has to be measured: where its ink actually sits, how much of
the artboard it fills, where its interior counters (the enclosed gaps a small mark's
first casualty) are, and how far its ink centre sits from the artboard's own centre.

Nothing here judges the mark or proposes a rebuild. It measures the drawing exactly as
Aninda drew it, at brand-kit/03_logo/original/GRU953-logo-master.svg, and writes what it
finds to original-measurements.json — a fact sheet the actual rebuild reads later, and a
human can check by eye against the numbers.

METHOD
------
Rasterised through Chromium (Playwright), the same renderer the mark will actually be
seen through everywhere else in this kit — never a second, unrelated SVG engine, so a
rendering quirk cannot make the measurement disagree with what the mark will really look
like. Ink coverage, bounding box and centroid are read off the rendered pixels, not
computed from the path data, because path data can self-intersect and overlap in ways
that make an analytic area calculation lie.

Run:
    PLAYWRIGHT_BROWSERS_PATH=$(pwd)/00_sandbox/browsers ../../.venv/bin/python \
        brand-kit/03_logo/measure_original.py
"""
import collections
import json
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
MASTER_SVG = HERE / "original" / "GRU953-logo-master.svg"
OUT_PATH = HERE / "original-measurements.json"

# The artboard the master is drawn on. Read from the SVG's own viewBox, not assumed —
# asserted below, so a future re-drawing at a different canvas size fails loudly rather
# than silently measuring against the wrong scale.
EXPECTED_VIEWBOX = (0, 0, 1024, 1024)

# Rendered at 4x the artboard's own units, so a 1-unit feature is a 4px feature — enough
# for the ink-coverage and centroid measurements below to not be dominated by anti-aliasing
# at the shape's edges. Native 1x and 4x are both captured; see RENDER_SCALES.
RENDER_SCALES = [1, 4]

# A pixel this dark or darker counts as ink. The master's fill is solid black
# (fill="currentColor", resolved to black with no CSS override) on a white page
# background, so the midpoint of 0 (black) and 255 (white) is the natural threshold.
INK_THRESHOLD = 128


def render_png(scale: int) -> Image.Image:
    size = 1024 * scale
    html = f"""<!doctype html><html><head><style>
      html, body {{ margin: 0; padding: 0; background: #fff; }}
      svg {{ display: block; width: {size}px; height: {size}px; }}
    </style></head><body>{MASTER_SVG.read_text(encoding='utf-8')}</body></html>"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": size, "height": size})
        page.set_content(html)
        page.wait_for_timeout(50)
        png_bytes = page.screenshot()
        browser.close()
    img = Image.open(__import__("io").BytesIO(png_bytes)).convert("L")
    assert img.size == (size, size), f"expected {size}x{size}, got {img.size}"
    return img


# ---------------------------------------------------------------- interior counters
#
# An interior counter (the enclosed gap inside a wing facet, the hole in an "o") is the
# first thing to close as a drawing shrinks, and it is the whole reason the mark ships as
# a tile below the owner's stated 16px floor rather than a shrunken line drawing. Found
# the same way brand-kit/03_logo/marks.py already proves its own survival check: flood
# white in from the artboard border; whatever white is left, unreachable from outside,
# is enclosed by ink. Rendered through Chromium here, not rsvg-convert (marks.py's own
# choice, unavailable on this machine) -- the substitution this whole sandbox is built on.
COUNTER_RENDER_PX = 512   # large enough that every counter is certainly still open


def render_counter_mask(px: int) -> list:
    """Render the mark at `px` and return a 2D list of bool: True = ink (dark).

    Same polarity as measure_at_scale()'s ink test (`< INK_THRESHOLD` = ink, a low
    grayscale value). Getting this backwards here once meant "is ink" and "is white"
    silently swapped through two inversions downstream and produced a single wrong
    77-artboard-unit "counter" instead of the several genuine ones — caught only by
    it being a suspiciously round, suspiciously singular result, not by the code
    raising anything.
    """
    html = f"""<!doctype html><html><head><style>
      html, body {{ margin: 0; padding: 0; background: #fff; }}
      svg {{ display: block; width: {px}px; height: {px}px; }}
    </style></head><body>{MASTER_SVG.read_text(encoding='utf-8')}</body></html>"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": px, "height": px})
        page.set_content(html)
        page.wait_for_timeout(50)
        png_bytes = page.screenshot()
        browser.close()
    img = Image.open(__import__("io").BytesIO(png_bytes)).convert("L")
    assert img.size == (px, px), f"expected {px}x{px}, got {img.size}"
    data = img.load()
    return [[data[x, y] < INK_THRESHOLD for x in range(px)] for y in range(px)]


def enclosed_mask(is_white: list) -> list:
    """White reachable from the artboard border is background; anything left is a
    counter, enclosed by ink on every side. BFS flood from the four edges."""
    h = len(is_white)
    w = len(is_white[0])
    outside = [[False] * w for _ in range(h)]
    q = collections.deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_white[y][x] and not outside[y][x]:
                outside[y][x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if is_white[y][x] and not outside[y][x]:
                outside[y][x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and is_white[ny][nx] and not outside[ny][nx]:
                outside[ny][nx] = True
                q.append((ny, nx))
    return [[is_white[y][x] and not outside[y][x] for x in range(w)] for y in range(h)]


def find_counters(enclosed: list, min_area_px: int = 20) -> list:
    """Connected-component label the enclosed mask. For each region: pixel count,
    centroid (fraction of canvas), and an INSCRIBED-CIRCLE RADIUS ESTIMATE.

    The radius estimate is a multi-source BFS distance-to-boundary within the region
    (4-connected), maximised over every pixel in the region -- the region's own "widest
    point". This is an approximation under Manhattan/Chebyshev-adjacent distance, not a
    true Euclidean distance transform; stated as such in the output, not silently
    presented as exact.
    """
    h = len(enclosed)
    w = len(enclosed[0])
    seen = [[False] * w for _ in range(h)]
    regions = []
    for y0 in range(h):
        for x0 in range(w):
            if enclosed[y0][x0] and not seen[y0][x0]:
                pts = []
                st = [(y0, x0)]
                seen[y0][x0] = True
                while st:
                    y, x = st.pop()
                    pts.append((y, x))
                    for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                        if (0 <= ny < h and 0 <= nx < w and enclosed[ny][nx]
                                and not seen[ny][nx]):
                            seen[ny][nx] = True
                            st.append((ny, nx))
                if len(pts) >= min_area_px:
                    regions.append(pts)

    out = []
    pt_set_template = None
    for pts in regions:
        pt_set = set(pts)
        # Boundary of this region = pixels with a 4-neighbour outside the region
        # (either not enclosed at all, or a different region -- either way, an edge).
        boundary = [(y, x) for (y, x) in pts
                    if any((ny, nx) not in pt_set
                           for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)))]
        dist = {p: 0 for p in boundary}
        q = collections.deque(boundary)
        while q:
            y, x = q.popleft()
            d = dist[(y, x)]
            for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if (ny, nx) in pt_set and (ny, nx) not in dist:
                    dist[(ny, nx)] = d + 1
                    q.append((ny, nx))
        max_dist = max(dist.values()) if dist else 0
        cy = sum(p[0] for p in pts) / len(pts)
        cx = sum(p[1] for p in pts) / len(pts)
        out.append({
            "pixel_count": len(pts),
            "centroid_fraction": {"x": round(cx / w, 4), "y": round(cy / h, 4)},
            "inscribed_radius_px_estimate": max_dist,
            "inscribed_diameter_px_estimate": max_dist * 2,
        })
    out.sort(key=lambda r: -r["pixel_count"])
    return out


def measure_counters() -> dict:
    is_ink_dark = render_counter_mask(COUNTER_RENDER_PX)
    # render_counter_mask returns True where the pixel counts as INK (dark). The
    # enclosed-white analysis wants True where a pixel is WHITE (background-coloured);
    # invert.
    is_white = [[not v for v in row] for row in is_ink_dark]
    enclosed = enclosed_mask(is_white)
    counters = find_counters(enclosed)
    px_to_artboard = 1024 / COUNTER_RENDER_PX
    for c in counters:
        c["inscribed_diameter_artboard_units_estimate"] = round(
            c["inscribed_diameter_px_estimate"] * px_to_artboard, 2)
    return {
        "render_px": COUNTER_RENDER_PX,
        "method": "flood-fill from the artboard border finds white reachable from "
                  "outside; what remains, enclosed on every side by ink, is a counter. "
                  "Radius is a 4-connected BFS distance-to-boundary within each region, "
                  "maximised -- an approximation, not a true Euclidean distance "
                  "transform, and stated as such.",
        "counter_count": len(counters),
        "counters": counters,
    }


def assert_viewbox():
    svg_text = MASTER_SVG.read_text(encoding="utf-8")
    import re
    m = re.search(r'viewBox="([\d.\s]+)"', svg_text)
    if not m:
        print("FAIL: master SVG has no viewBox attribute.")
        sys.exit(1)
    values = tuple(float(x) for x in m.group(1).split())
    if values != EXPECTED_VIEWBOX:
        print(f"FAIL: viewBox is {values}, expected {EXPECTED_VIEWBOX}. "
              f"The measurements below assume a 1024x1024 artboard; if the artboard has "
              f"genuinely changed, update EXPECTED_VIEWBOX and re-run.")
        sys.exit(1)


def measure_at_scale(scale: int) -> dict:
    img = render_png(scale)
    w, h = img.size
    px = img.load()

    # Ink mask: True where a pixel is dark enough to count as drawn.
    ink_pixels = []
    min_x, min_y, max_x, max_y = w, h, -1, -1
    sum_x = sum_y = count = 0
    for y in range(h):
        row_has_ink = False
        for x in range(w):
            if px[x, y] < INK_THRESHOLD:
                row_has_ink = True
                count += 1
                sum_x += x
                sum_y += y
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
        if row_has_ink:
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

    if count == 0:
        print(f"FAIL at scale {scale}x: no ink pixels found — the render produced a "
              f"blank page. Nothing was measured.")
        sys.exit(1)

    bbox_w = max_x - min_x + 1
    bbox_h = max_y - min_y + 1
    ink_centroid_x = sum_x / count
    ink_centroid_y = sum_y / count
    bbox_centre_x = min_x + bbox_w / 2
    bbox_centre_y = min_y + bbox_h / 2
    artboard_centre = w / 2

    # Normalise everything back to the 1024x1024 artboard's own units, regardless of
    # what scale it was rendered at, so the JSON reads the same story at every scale —
    # and so scale is itself a cross-check: two independent renders should agree.
    def norm(v):
        return v / scale

    return {
        "render_scale": scale,
        "render_px": w,
        "ink_pixel_count": count,
        "ink_coverage_pct_of_artboard": round(100 * count / (w * h), 3),
        "inked_bbox_artboard_units": {
            "x": round(norm(min_x), 2), "y": round(norm(min_y), 2),
            "width": round(norm(bbox_w), 2), "height": round(norm(bbox_h), 2),
        },
        "inked_bbox_aspect_ratio_w_over_h": round(bbox_w / bbox_h, 4),
        "ink_centroid_artboard_units": {
            "x": round(norm(ink_centroid_x), 2), "y": round(norm(ink_centroid_y), 2),
        },
        "bbox_centre_artboard_units": {
            "x": round(norm(bbox_centre_x), 2), "y": round(norm(bbox_centre_y), 2),
        },
        # How far the ink's own centre of mass sits from the geometric centre of its
        # bounding box, as a fraction of the box's own diagonal -- a construction that
        # is optically balanced should have a small figure here, not necessarily zero.
        "centroid_offset_from_bbox_centre_artboard_units": {
            "x": round(norm(ink_centroid_x) - norm(bbox_centre_x), 2),
            "y": round(norm(ink_centroid_y) - norm(bbox_centre_y), 2),
        },
        "artboard_centre_artboard_units": round(norm(artboard_centre), 2),
    }


def main():
    assert_viewbox()
    results = [measure_at_scale(s) for s in RENDER_SCALES]

    # Cross-check: two independent render scales measuring the same artboard-unit
    # figures should agree closely. A real disagreement means anti-aliasing or
    # rounding is distorting one of the scales enough to matter, and that is a finding,
    # not something to average away silently.
    bbox_1x = results[0]["inked_bbox_artboard_units"]
    bbox_4x = results[-1]["inked_bbox_artboard_units"]
    disagreement_px = max(
        abs(bbox_1x["width"] - bbox_4x["width"]),
        abs(bbox_1x["height"] - bbox_4x["height"]),
    )
    agrees = disagreement_px <= 2.0  # 2 artboard units tolerance, i.e. <=2px at 1x

    counters = measure_counters()

    out = {
        "$note": "Measured, not asserted. Every figure here was read off rendered "
                 "pixels of brand-kit/03_logo/original/GRU953-logo-master.svg through "
                 "Chromium (Playwright) -- the same renderer the mark is seen through "
                 "everywhere else in this kit. Regenerate: "
                 "python3 brand-kit/03_logo/measure_original.py",
        "source_file": "brand-kit/03_logo/original/GRU953-logo-master.svg",
        "artboard": {"viewbox": list(EXPECTED_VIEWBOX), "units": "SVG user units"},
        "ink_threshold": INK_THRESHOLD,
        "measurements_by_render_scale": results,
        "cross_check": {
            "method": "bounding-box width/height measured at 1x and 4x render scale, "
                      "compared in artboard units",
            "max_disagreement_artboard_units": round(disagreement_px, 3),
            "agrees_within_2_units": agrees,
        },
        "interior_counters": counters,
        "not_yet_measured": [
            "Per-facet wing angles (needs manual identification of the four facet "
            "edges from the path data, then a least-squares line fit to each).",
            "Stroke width sampled along the drawing's own centreline (needs a "
            "centreline extraction this script does not attempt).",
            "A true Euclidean distance transform for the inscribed-circle radii "
            "above -- the current estimate is a 4-connected BFS approximation, "
            "which is somewhat smaller than a true Euclidean radius for a "
            "non-axis-aligned counter shape.",
        ],
    }

    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")

    print(f"wrote {OUT_PATH.name}")
    for r in results:
        b = r["inked_bbox_artboard_units"]
        print(f"  {r['render_scale']}x: ink {r['ink_coverage_pct_of_artboard']}% of "
              f"artboard, bbox {b['width']}x{b['height']} at ({b['x']},{b['y']}), "
              f"aspect {r['inked_bbox_aspect_ratio_w_over_h']}")
    print(f"  cross-check (1x vs {RENDER_SCALES[-1]}x): "
          f"{'agrees' if agrees else 'DISAGREES'} "
          f"(max diff {disagreement_px:.3f} artboard units)")
    print(f"  {counters['counter_count']} interior counters found at "
          f"{counters['render_px']}px")
    for i, c in enumerate(counters["counters"], 1):
        print(f"    #{i}: {c['pixel_count']}px, inscribed diameter "
              f"~{c['inscribed_diameter_artboard_units_estimate']} artboard units")
    if not agrees:
        print("  FAIL: the two render scales disagree by more than 2 artboard units.")
        sys.exit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
