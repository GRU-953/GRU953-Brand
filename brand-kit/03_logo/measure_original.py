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

The two exceptions: the four wing-facet angles are measured directly from the path's own
Bezier control points (see analyse_wing_facets), because there the control points ARE the
design decision, with no rendering step between this script and what Aninda drew; and
stroke width along the centreline (see measure_stroke_width_at_scale) is still rasterised,
but through a chamfer distance transform rather than the counters' own 4-connected BFS,
because a diagonal edge (this mark's own wing ribs sit at ~27 degrees) makes that
distinction a real, measured difference, not a stylistic one.

Run, from the repo root (PLAYWRIGHT_BROWSERS_PATH must point at the sandbox's own
Chromium, never a system one):
    PLAYWRIGHT_BROWSERS_PATH="$(pwd)/00_sandbox/browsers" ./.venv/bin/python \
        brand-kit/03_logo/measure_original.py
"""
import collections
import io
import json
import math
import pathlib
import re
import sys

from PIL import Image, ImageDraw
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


def preflight_chromium():
    """Every measurement below depends on Chromium actually launching. Without
    this check, a missing browser install crashes deep inside the first render
    with a stack trace that reads as a real failure (exit 1) -- this project's
    own three-way convention (0 pass / 1 real failure / 2 NOT EQUIPPED) says a
    tool that could not run must never read as either a pass OR a fail. Fail
    this loudly and distinctly, first, before any measurement work starts."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
    except Exception as e:
        print(f"NOT EQUIPPED: Chromium did not launch ({e}). Run: "
              f"sh 00_sandbox/setup.sh (with PLAYWRIGHT_BROWSERS_PATH set to "
              f"$(pwd)/00_sandbox/browsers) and re-run this script.")
        sys.exit(2)


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
    img = Image.open(io.BytesIO(png_bytes)).convert("L")
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
    img = Image.open(io.BytesIO(png_bytes)).convert("L")
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
    centroid (fraction of canvas), an INSCRIBED-CIRCLE RADIUS ESTIMATE, and an
    ELONGATION ESTIMATE (see below).

    The radius estimate is a multi-source BFS distance-to-boundary within the region
    (4-connected), maximised over every pixel in the region -- the region's own "widest
    point". This is an approximation under Manhattan/Chebyshev-adjacent distance, not a
    true Euclidean distance transform; stated as such in the output, not silently
    presented as exact.

    The elongation estimate is used by analyse_wing_facets() below to pick out the
    thin, nested facet-gap counters from the more compact head/throat/tail ones.
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
        # Elongation via 2nd-order image moments, not an axis-aligned bounding box.
        # A bbox over-reports elongation for a shape that is compact but sits at an
        # angle -- its axis-aligned box then spans extra width AND height, since
        # neither axis lines up with the shape's own long dimension. Several of
        # this mark's own counters sit at roughly a 27-degree tilt (see
        # analyse_wing_facets below), where this distinction is not academic: an
        # axis-aligned bbox on the first pass here ranked the central, roughly
        # triangular counter as MORE elongated than the genuinely thin wing-facet
        # slits, which is visibly wrong on the rendered mark. The moment ratio is
        # rotation-invariant and does not make that mistake.
        ixx = sum((x - cx) ** 2 for (y, x) in pts)
        iyy = sum((y - cy) ** 2 for (y, x) in pts)
        ixy = sum((x - cx) * (y - cy) for (y, x) in pts)
        trace = ixx + iyy
        det = ixx * iyy - ixy * ixy
        disc = max(0.0, trace ** 2 - 4 * det) ** 0.5
        lam_major = (trace + disc) / 2
        lam_minor = max(1e-9, (trace - disc) / 2)
        elongation = (lam_major / lam_minor) ** 0.5
        out.append({
            "pixel_count": len(pts),
            "centroid_fraction": {"x": round(cx / w, 4), "y": round(cy / h, 4)},
            "inscribed_radius_px_estimate": max_dist,
            "inscribed_diameter_px_estimate": max_dist * 2,
            "elongation_estimate": round(elongation, 4),
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


# ---------------------------------------------------------------- wing facet angles
#
# Closes the first of the two gaps this file's own output used to name under
# "not_yet_measured". The four wing facet angles are the mark's signature -- the
# plan this rebuild follows says so explicitly, and says everything else about the
# mark may move before those four angles do. Measured directly from the master
# SVG's own path data (the exact vector geometry, not a rasterisation of it), because
# the control points ARE the design decision here, with no anti-aliasing or
# discretisation between this script and what Aninda actually drew.
#
# The path is a single <path d="..."> built entirely from cubic Bezier "C" commands
# across 9 subpaths: one 44-segment outer silhouette, plus the same 8 subpaths that
# render_counter_mask()/find_counters() above already find as interior counters (in
# the identical path order). Nothing here is a general-purpose vector-facet-finder --
# it is a computed rule against this one mark's own geometry, and every step below
# fails loudly (an assertion, not a silent guess) if that geometry's assumed
# structure -- 9 subpaths, 44 silhouette segments, a clearly-separated wing-angle
# family spanning multiple subpaths -- no longer holds on a future re-drawing.

# The raw file stores literal XML character-reference escapes (&#x9; = tab,
# &#xA; = newline) INSIDE the quoted d="..." string, rather than real whitespace
# bytes. &#x9; contains a bare digit 9; a tokenizer that does not strip these first
# reads that digit as a stray coordinate and desyncs every M/C argument count after
# it -- caught by asserting the subpath and segment counts below, not silently.
PATH_ENTITY_RE = re.compile(r'&#x[0-9A-Fa-f]+;')
PATH_TOKEN_RE = re.compile(r'([MCz])|(-?\d+(?:\.\d+)?)')

# A cubic segment whose two control points sit within this fraction of the chord's
# own length counts as "near-straight" -- this is not an arbitrary round number: a
# scan of every segment in this file's own silhouette shows a real gap in the data
# between the straightest ~45 segments (all under 0.015) and every genuinely curving
# one (jumping to 0.023+); 0.02 sits in that gap.
STRAIGHT_RATIO_THRESHOLD = 0.02
# Consecutive near-straight segments chain into one candidate edge when their chord
# angles agree within this many degrees -- again not arbitrary: this file's own
# inter-segment angle jumps show a real gap between 2.9 deg (the largest genuine
# same-edge continuation) and 6.5 deg (the smallest real corner); 4 deg sits in it.
CHAIN_ANGLE_TOL_DEG = 4.0
# A chain is only accepted if EVERY accumulated sample point's perpendicular
# residual from the whole chain's own least-squares fit stays under this many
# artboard units. Local chord-to-chord angle agreement alone is not sufficient: two
# segments can each be individually near-straight and share a similar LOCAL chord
# angle while sitting on two different, merely near-parallel sides of one of the
# wing's narrow nested facet-gap slits. A first version of this chaining, gated
# only on local angle agreement, merged exactly that case in one of the facet-gap
# counters -- rms residual 21.9 units against every other chain's under 1 unit, a
# "suspiciously singular result" caught only by printing every chain's own residual
# as a routine diagnostic, the same discipline render_counter_mask()'s own
# docstring above describes for its polarity bug.
MAX_POINT_RESIDUAL = 3.0
# Below this end-to-end chord length, a near-straight run is noise (an incidental
# few-unit segment sharing a family's angle by coincidence), not a real edge.
MIN_CHAIN_CHORD_UNITS = 30.0
# Two candidate edges (from anywhere in the whole path, any subpath) belong to the
# same angle family -- the same design decision, restated by another edge -- if
# their fitted angles agree within this many degrees.
FACET_CLUSTER_TOL_DEG = 5.0


def parse_path_d(d: str) -> list:
    """Return the 9 subpaths of the master SVG's single path, each a list of
    (p0, c1, c2, p3) cubic-Bezier segments in path order."""
    d = PATH_ENTITY_RE.sub(' ', d)
    cmds = []
    for letter, num in PATH_TOKEN_RE.findall(d):
        cmds.append(letter if letter else float(num))
    subpaths, cur, segs = [], None, None
    i, n = 0, len(cmds)
    while i < n:
        tok = cmds[i]
        if tok == 'M':
            if segs is not None:
                subpaths.append(segs)
            cur = (cmds[i + 1], cmds[i + 2])
            segs = []
            i += 3
        elif tok == 'C':
            c1 = (cmds[i + 1], cmds[i + 2])
            c2 = (cmds[i + 3], cmds[i + 4])
            p3 = (cmds[i + 5], cmds[i + 6])
            segs.append((cur, c1, c2, p3))
            cur = p3
            i += 7
        elif tok == 'z':
            i += 1
        else:
            raise ValueError(f"unexpected path token {tok!r} at index {i}")
    if segs is not None:
        subpaths.append(segs)
    return subpaths


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _point_line_perp_dist(q, p0, p3):
    chord_len = _dist(p0, p3)
    if chord_len < 1e-9:
        return _dist(q, p0)
    cross = (p3[0] - p0[0]) * (q[1] - p0[1]) - (p3[1] - p0[1]) * (q[0] - p0[0])
    return abs(cross) / chord_len


def _bezier_point(p0, c1, c2, p3, t):
    mt = 1 - t
    x = mt**3*p0[0] + 3*mt**2*t*c1[0] + 3*mt*t**2*c2[0] + t**3*p3[0]
    y = mt**3*p0[1] + 3*mt**2*t*c1[1] + 3*mt*t**2*c2[1] + t**3*p3[1]
    return (x, y)


def _chord_angle_deg(p0, p3):
    """Undirected line angle in [0, 180) -- a line and its reverse are the same line."""
    return math.degrees(math.atan2(p3[1] - p0[1], p3[0] - p0[0])) % 180.0


def _angle_diff_mod180(a, b):
    d = abs(a - b) % 180.0
    return min(d, 180.0 - d)


def _total_least_squares_angle(points):
    """Orthogonal-regression line angle through `points`, via the 2x2 covariance
    matrix's principal eigenvector -- closed form, no numpy needed. Returns
    (angle_deg_in_[0,180), (centroid_x, centroid_y), max_perp_residual)."""
    n = len(points)
    mx = sum(p[0] for p in points) / n
    my = sum(p[1] for p in points) / n
    sxx = sum((p[0] - mx) ** 2 for p in points) / n
    syy = sum((p[1] - my) ** 2 for p in points) / n
    sxy = sum((p[0] - mx) * (p[1] - my) for p in points) / n
    theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
    angle = math.degrees(theta) % 180.0
    dx, dy = math.cos(theta), math.sin(theta)
    max_resid = max(abs(-(x - mx) * dy + (y - my) * dx) for (x, y) in points)
    return angle, (mx, my), max_resid


def _segment_straightness(seg):
    p0, c1, c2, p3 = seg
    chord_len = _dist(p0, p3)
    max_dev = max(_point_line_perp_dist(c1, p0, p3), _point_line_perp_dist(c2, p0, p3))
    return (max_dev / chord_len) if chord_len > 1e-9 else float('inf')


def chains_for_subpath(subpath: list) -> list:
    """Residual-gated chaining of consecutive near-straight Bezier segments within
    one subpath into candidate long straight edges. Starts at a non-straight
    segment (or index 0 if the whole subpath is straight) so a closed loop never
    needs a separate wraparound merge step."""
    n = len(subpath)
    seg_info = []
    for idx, seg in enumerate(subpath):
        p0, _, _, p3 = seg
        seg_info.append({
            "idx": idx, "angle": _chord_angle_deg(p0, p3),
            "is_straight": _segment_straightness(seg) <= STRAIGHT_RATIO_THRESHOLD,
        })
    start = 0
    for i, info in enumerate(seg_info):
        if not info["is_straight"]:
            start = (i + 1) % n
            break
    ordered = seg_info[start:] + seg_info[:start]

    chains, cur_pts, cur_idxs, last_angle = [], [], [], None

    def flush():
        nonlocal cur_pts, cur_idxs
        if cur_idxs:
            chains.append((cur_idxs[:], cur_pts[:]))
        cur_pts, cur_idxs = [], []

    for info in ordered:
        if not info["is_straight"]:
            flush()
            last_angle = None
            continue
        seg = subpath[info["idx"]]
        new_pts = [_bezier_point(*seg, t) for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
        if not cur_idxs:
            cur_idxs, cur_pts, last_angle = [info["idx"]], new_pts, info["angle"]
            continue
        if _angle_diff_mod180(last_angle, info["angle"]) > CHAIN_ANGLE_TOL_DEG:
            flush()
            cur_idxs, cur_pts, last_angle = [info["idx"]], new_pts, info["angle"]
            continue
        # Provisional merge -- refit over the WHOLE accumulated set, not just the
        # new segment against its immediate neighbour. See MAX_POINT_RESIDUAL above.
        trial_pts = cur_pts + new_pts
        _, _, max_resid = _total_least_squares_angle(trial_pts)
        if max_resid > MAX_POINT_RESIDUAL:
            flush()
            cur_idxs, cur_pts, last_angle = [info["idx"]], new_pts, info["angle"]
        else:
            cur_idxs.append(info["idx"])
            cur_pts = trial_pts
            last_angle = info["angle"]
    flush()

    out = []
    for idxs, pts in chains:
        p_start, p_end = subpath[idxs[0]][0], subpath[idxs[-1]][3]
        e2e = _dist(p_start, p_end)
        if e2e < MIN_CHAIN_CHORD_UNITS:
            continue
        angle, centroid, _ = _total_least_squares_angle(pts)
        out.append({"seg_indices": idxs, "p_start": p_start, "p_end": p_end,
                     "e2e": e2e, "angle": angle, "centroid": centroid})
    out.sort(key=lambda r: -r["e2e"])
    return out


def _subpath_centroid_fraction(subpath, viewbox=1024.0):
    """Approximate centroid of a closed subpath, sampled along each Bezier --
    used only to match this path-order subpath to the raster counter
    find_counters() already detected for it, never as a measurement of its own."""
    xs, ys = [], []
    for seg in subpath:
        for t in (0.0, 0.5):
            x, y = _bezier_point(*seg, t)
            xs.append(x); ys.append(y)
    return (sum(xs) / len(xs) / viewbox, sum(ys) / len(ys) / viewbox)


def analyse_wing_facets(raster_counters: list) -> dict:
    """The four wing-facet rib angles, by a data-driven rule -- not four
    hand-picked indices:

    1. Chain every one of the 9 subpaths (the outer silhouette AND all 8
       counters) independently into candidate straight edges.
    2. Cluster every candidate edge, from any subpath, by angle.
    3. The wing-facet family is the cluster spanning the MOST DISTINCT
       subpaths -- a design element repeated across several separate parts
       of the path is far stronger evidence of a deliberate angle than one
       long, merely lucky edge. (On this mark: 7 of the 9 subpaths.)
    4. Within that family, rank the counter-subpaths involved by elongation
       (find_counters()'s own moment-based estimate) -- the wing's nested
       facet-gap slits are thin, unlike the more compact head/throat/tail
       counters that can still share the same coincidental angle range.
       Take the 3 most elongated.
    5. Pair the silhouette's own 2 longest matching edges with those 3
       slits' 6 edges into 4 ribs, ordered along the axis perpendicular to
       the family's own mean angle (a fan of parallel ribs is naturally
       ordered by how far each sits across the fan, not along it).

    Any OTHER counter-subpath that also falls in the wing-facet angle family
    but was not among the 3 selected as slits is reported separately, as a
    disputed alternate reading, never silently included or excluded --
    exactly this ambiguity was independently flagged by three separate
    analyses of this same geometry, and is a real, unresolved judgement call
    this file does not make on a human's behalf.
    """
    d_attr = re.search(r'\sd="([^"]+)"', MASTER_SVG.read_text(encoding='utf-8')).group(1)
    subpaths = parse_path_d(d_attr)
    assert len(subpaths) == 9, (
        f"expected 9 subpaths (1 outer silhouette + 8 counters), got "
        f"{len(subpaths)} -- the master SVG's own structure has changed; this "
        f"whole method needs re-deriving, not just re-running.")
    assert len(subpaths[0]) == 44, (
        f"expected 44 segments in the outer silhouette, got {len(subpaths[0])}.")

    all_chains = []
    for sp_idx, subpath in enumerate(subpaths):
        for ch in chains_for_subpath(subpath):
            ch["subpath"] = sp_idx
            all_chains.append(ch)

    ordered = sorted(all_chains, key=lambda c: c["angle"])
    clusters, cur = [], []
    for c in ordered:
        if cur and _angle_diff_mod180(cur[-1]["angle"], c["angle"]) > FACET_CLUSTER_TOL_DEG:
            clusters.append(cur)
            cur = [c]
        else:
            cur.append(c)
    if cur:
        clusters.append(cur)
    if len(clusters) >= 2 and _angle_diff_mod180(
            clusters[-1][-1]["angle"], clusters[0][0]["angle"]) <= FACET_CLUSTER_TOL_DEG:
        clusters = [clusters[-1] + clusters[0]] + clusters[1:-1]

    def n_distinct_subpaths(cluster):
        return len({c["subpath"] for c in cluster})

    clusters.sort(key=n_distinct_subpaths, reverse=True)
    wing_cluster = clusters[0]
    n_sub = n_distinct_subpaths(wing_cluster)
    assert n_sub >= 4, (
        f"expected the wing-facet angle family to span at least 4 distinct "
        f"subpaths (the silhouette plus at least 3 counters); the largest "
        f"cluster found spans only {n_sub}. The structural assumption this "
        f"rule depends on may no longer hold on this geometry -- do not trust "
        f"a rib-angle result built on it without checking by eye first.")

    counter_subpaths = sorted({c["subpath"] for c in wing_cluster if c["subpath"] != 0})

    def match_raster_counter(sp_idx):
        cx, cy = _subpath_centroid_fraction(subpaths[sp_idx])
        best, best_d = None, float("inf")
        for rc in raster_counters:
            fx, fy = rc["centroid_fraction"]["x"], rc["centroid_fraction"]["y"]
            d = math.hypot(cx - fx, cy - fy)
            if d < best_d:
                best, best_d = rc, d
        return best, best_d

    elong_by_subpath = {}
    for sp_idx in counter_subpaths:
        rc, d = match_raster_counter(sp_idx)
        assert d < 0.05, (
            f"subpath {sp_idx} did not match any raster counter closely "
            f"(nearest at fractional centroid distance {d:.4f}) -- path-order "
            f"and raster-order counters may have desynced.")
        elong_by_subpath[sp_idx] = rc["elongation_estimate"]

    ranked = sorted(counter_subpaths, key=lambda s: -elong_by_subpath[s])
    assert len(ranked) >= 3, (
        f"need at least 3 elongated counter-subpaths in the wing-facet family "
        f"to form the 3 nested slits; found {len(ranked)}.")
    top3 = ranked[:3]
    excluded = ranked[3:]

    sil_edges = sorted([c for c in wing_cluster if c["subpath"] == 0],
                        key=lambda c: -c["e2e"])
    assert len(sil_edges) >= 2, (
        f"expected at least 2 silhouette edges (leading + wing-root) in the "
        f"wing-facet family, found {len(sil_edges)}.")
    sil_edges = sil_edges[:2]

    slit_edges = [c for c in wing_cluster if c["subpath"] in top3]
    assert len(slit_edges) == 6, (
        f"expected exactly 2 wing-facet-family edges from each of the 3 "
        f"selected slit counters (6 total); got {len(slit_edges)} from "
        f"subpaths {top3} -- one of them contributed an unexpected number of "
        f"straight sides.")

    rib_source_edges = sil_edges + slit_edges
    mean_angle, _, _ = _total_least_squares_angle(
        [pt for c in rib_source_edges for pt in (c["p_start"], c["p_end"])])
    theta = math.radians(mean_angle)
    dx, dy = math.cos(theta), math.sin(theta)
    rib_source_edges.sort(key=lambda c: -c["centroid"][0] * dy + c["centroid"][1] * dx)

    ribs = []
    for i in range(0, 8, 2):
        a, b = rib_source_edges[i], rib_source_edges[i + 1]
        w = a["e2e"] + b["e2e"]
        ribs.append({
            "angle_deg": round((a["e2e"] * a["angle"] + b["e2e"] * b["angle"]) / w, 2),
            "edges": [
                {"subpath": a["subpath"], "length_units": round(a["e2e"], 1),
                 "angle_deg": round(a["angle"], 2)},
                {"subpath": b["subpath"], "length_units": round(b["e2e"], 1),
                 "angle_deg": round(b["angle"], 2)},
            ],
        })
    angles = [r["angle_deg"] for r in ribs]

    result = {
        "method": "Computed rule, not hand-picked indices: chain near-straight "
                  "Bezier runs in every one of the 9 subpaths (residual-gated "
                  "total-least-squares fit), cluster all chains across all "
                  "subpaths by angle, take the cluster spanning the most "
                  "distinct subpaths as the wing-facet family, select the 3 "
                  "most elongated counter-subpaths in that family as the "
                  "nested facet-gap slits, pair the silhouette's own 2 "
                  "longest matching edges with the 3 slits' 6 edges into 4 "
                  "ribs, ordered across the fan by perpendicular offset from "
                  "the family's own mean angle.",
        "ribs": ribs,
        "spread_deg": round(max(angles) - min(angles), 2),
        "wing_cluster_subpath_count": n_sub,
        "selected_slit_subpaths": top3,
    }
    if excluded:
        alt_edges = [c for c in wing_cluster if c["subpath"] in excluded]
        result["alternate_disputed_facet"] = {
            "note": f"Counter-subpath(s) {excluded} sit in the same angle "
                    "family as the four ribs above but were excluded from "
                    "them because they are not among the 3 most-elongated "
                    "slits (they read as more compact or triangular, not a "
                    "thin nested slit). A different, equally defensible "
                    "reading could include one of these as a genuine 4th "
                    "wing facet instead of one of the silhouette-boundary "
                    "ribs above. This file does not resolve that choice -- "
                    "it needs a human eye-check against the rendered mark "
                    "before either reading is treated as final.",
            "candidate_edges": [
                {"subpath": c["subpath"], "length_units": round(c["e2e"], 1),
                 "angle_deg": round(c["angle"], 2)} for c in alt_edges
            ],
        }
    return result


# ---------------------------------------------------------------- stroke width
#
# Closes the second of the two gaps this file's own output used to name under
# "not_yet_measured". Method: rasterise the full mark (fill-rule already cuts the
# 8 counter holes out of the ink, same as everywhere else in this file), build a
# distance-to-boundary field for every ink pixel, thin the ink to a 1-pixel
# centreline, and read the distance field back at each centreline pixel (doubled)
# as the local stroke width there.
#
# The distance transform is a two-pass CHAMFER approximation (edge weight 1.0
# orthogonal, sqrt(2) diagonal -- the classic Borgefors algorithm), not the
# 4-connected BFS find_counters() above uses for the counters' inscribed radius.
# The two are deliberately different: a 4-connected (Manhattan) distance-to-
# boundary provably OVER-estimates true Euclidean distance for a diagonal edge --
# up to a factor of sqrt(2) at 45 degrees, since Manhattan distance is always >=
# Euclidean distance -- and this mark's own wing ribs sit at a real diagonal,
# ~27 degrees. The calibration self-test below (calibrate_stroke_width_method)
# measures the chamfer transform's own residual bias directly, rather than
# asserting it is exact.


def _crop_to_ink(mask, margin):
    h, w = len(mask), len(mask[0])
    min_x, min_y, max_x, max_y = w, h, -1, -1
    for y in range(h):
        row = mask[y]
        for x in range(w):
            if row[x]:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
    min_x, min_y = max(0, min_x - margin), max(0, min_y - margin)
    max_x, max_y = min(w - 1, max_x + margin), min(h - 1, max_y + margin)
    cropped = [row[min_x:max_x + 1] for row in mask[min_y:max_y + 1]]
    return cropped, (min_x, min_y)


def chamfer_distance_transform(ink: list) -> list:
    """Two-pass chamfer (1, sqrt(2)) distance-to-nearest-non-ink-pixel, in
    pixels, for every ink pixel. Pure Python, O(pixels), no numpy needed."""
    h, w = len(ink), len(ink[0])
    INF = float("inf")
    D2 = 2 ** 0.5
    dt = [[0.0 if not ink[y][x] else INF for x in range(w)] for y in range(h)]
    for y in range(h):
        row = dt[y]
        prev = dt[y - 1] if y > 0 else None
        for x in range(w):
            v = row[x]
            if v == 0.0:
                continue
            if x > 0 and row[x - 1] + 1.0 < v: v = row[x - 1] + 1.0
            if prev is not None:
                if prev[x] + 1.0 < v: v = prev[x] + 1.0
                if x > 0 and prev[x - 1] + D2 < v: v = prev[x - 1] + D2
                if x < w - 1 and prev[x + 1] + D2 < v: v = prev[x + 1] + D2
            row[x] = v
    for y in range(h - 1, -1, -1):
        row = dt[y]
        nxt = dt[y + 1] if y < h - 1 else None
        for x in range(w - 1, -1, -1):
            v = row[x]
            if v == 0.0:
                continue
            if x < w - 1 and row[x + 1] + 1.0 < v: v = row[x + 1] + 1.0
            if nxt is not None:
                if nxt[x] + 1.0 < v: v = nxt[x] + 1.0
                if x < w - 1 and nxt[x + 1] + D2 < v: v = nxt[x + 1] + D2
                if x > 0 and nxt[x - 1] + D2 < v: v = nxt[x - 1] + D2
            row[x] = v
    return dt


def zhang_suen_thin(ink: list) -> list:
    """Standard two-subiteration Zhang-Suen thinning. Returns a new mask: the
    1-pixel-wide skeleton (medial axis) of `ink`."""
    h, w = len(ink), len(ink[0])
    img = [[1 if v else 0 for v in row] for row in ink]

    def get(y, x):
        return img[y][x] if 0 <= y < h and 0 <= x < w else 0

    changed = True
    while changed:
        changed = False
        for step in (1, 2):
            to_delete = []
            for y in range(h):
                row = img[y]
                for x in range(w):
                    if row[x] != 1:
                        continue
                    p2, p3, p4 = get(y-1, x), get(y-1, x+1), get(y, x+1)
                    p5, p6, p7 = get(y+1, x+1), get(y+1, x), get(y+1, x-1)
                    p8, p9 = get(y, x-1), get(y-1, x-1)
                    neigh = (p2, p3, p4, p5, p6, p7, p8, p9)
                    b = sum(neigh)
                    if b < 2 or b > 6:
                        continue
                    seq = neigh + (p2,)
                    a = sum(1 for i in range(8) if seq[i] == 0 and seq[i + 1] == 1)
                    if a != 1:
                        continue
                    if step == 1:
                        if p2 * p4 * p6 != 0 or p4 * p6 * p8 != 0:
                            continue
                    else:
                        if p2 * p4 * p8 != 0 or p2 * p6 * p8 != 0:
                            continue
                    to_delete.append((y, x))
            if to_delete:
                changed = True
                for (y, x) in to_delete:
                    img[y][x] = 0
    return [[bool(v) for v in row] for row in img]


STROKE_WIDTH_MARGIN_PX = 6


def measure_stroke_width_at_scale(scale: int) -> dict:
    resolution = 1024 * scale
    mask = render_counter_mask(resolution)
    cropped, _ = _crop_to_ink(mask, margin=STROKE_WIDTH_MARGIN_PX * scale)
    h, w = len(cropped), len(cropped[0])
    dt = chamfer_distance_transform(cropped)
    skeleton = zhang_suen_thin(cropped)
    px_to_artboard = 1024 / resolution
    widths = sorted(2 * dt[y][x] * px_to_artboard
                     for y in range(h) for x in range(w) if skeleton[y][x])
    n = len(widths)
    return {
        "render_scale": scale, "render_px": resolution, "n_skeleton_samples": n,
        "width_stats_artboard_units": {
            "min": round(widths[0], 2), "max": round(widths[-1], 2),
            "mean": round(sum(widths) / n, 2),
            "median": round(widths[n // 2] if n % 2 else
                             (widths[n // 2 - 1] + widths[n // 2]) / 2, 2),
            "p10": round(widths[int(n * 0.10)], 2),
            "p90": round(widths[int(n * 0.90)], 2),
        },
    }


def calibrate_stroke_width_method(test_angles_deg: list) -> dict:
    """Permanent regression check, not a one-off finding: draw a synthetic
    strip of EXACTLY known width via PIL (no SVG, no Chromium -- pure
    ground-truth geometry) at each of `test_angles_deg`, run the identical
    chamfer + Zhang-Suen pipeline used on the real mark above, and report how
    far the recovered width lands from the true one. Every run re-measures
    this rather than assuming the method is unbiased -- the project's own
    standing rule against trusting a generator's first output, applied here
    to the measurement METHOD, not just its output."""
    canvas, true_width, strip_length = 300, 32, 220

    def make_strip_mask(angle_deg):
        img = Image.new("L", (canvas, canvas), 255)
        draw = ImageDraw.Draw(img)
        cx, cy = canvas / 2, canvas / 2
        theta = math.radians(angle_deg)
        ux, uy = math.cos(theta), math.sin(theta)
        vx, vy = -uy, ux
        hl, hw = strip_length / 2, true_width / 2
        corners = [(cx + s * ux + t * vx, cy + s * uy + t * vy)
                   for s, t in ((-hl, -hw), (-hl, hw), (hl, hw), (hl, -hw))]
        draw.polygon(corners, fill=0)
        data = img.load()
        return [[data[x, y] < INK_THRESHOLD for x in range(canvas)] for y in range(canvas)]

    results = []
    for angle in test_angles_deg:
        ink = make_strip_mask(angle)
        dt = chamfer_distance_transform(ink)
        skeleton = zhang_suen_thin(ink)
        cx, cy = canvas / 2, canvas / 2
        # Keep only skeleton points away from the strip's own end-caps, where the
        # medial axis is contaminated by the cap geometry, not the strip's width.
        central = [2 * dt[y][x] for y in range(canvas) for x in range(canvas)
                   if skeleton[y][x] and abs(x - cx) < 60 and abs(y - cy) < 60]
        est = sum(central) / len(central) if central else None
        results.append({
            "angle_deg": round(angle, 2), "true_width_px": true_width,
            "recovered_width_px": round(est, 3) if est is not None else None,
            "ratio": round(est / true_width, 4) if est is not None else None,
        })
    ratios = [r["ratio"] for r in results if r["ratio"] is not None]
    return {
        "method": "synthetic strip of known width, drawn with PIL (no SVG "
                  "involved -- pure ground-truth geometry), run through the "
                  "identical chamfer distance transform + Zhang-Suen "
                  "thinning pipeline used on the real mark above.",
        "tests": results,
        "mean_overestimate_ratio": round(sum(ratios) / len(ratios), 4) if ratios else None,
    }


def assert_viewbox():
    svg_text = MASTER_SVG.read_text(encoding="utf-8")
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
    preflight_chromium()
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
    wing_facets = analyse_wing_facets(counters["counters"])

    stroke_width_results = [measure_stroke_width_at_scale(s) for s in (1, 2)]
    sw_1x = stroke_width_results[0]["width_stats_artboard_units"]
    sw_2x = stroke_width_results[1]["width_stats_artboard_units"]
    sw_median_disagreement = round(abs(sw_1x["median"] - sw_2x["median"]), 3)
    sw_agrees = sw_median_disagreement <= 1.0

    # The mean rib angle plus 0/45/90 -- a spread across the whole circle, not just
    # the mark's own diagonal -- so the calibration is not silently overfit to one
    # angle. Computed from wing_facets, not hardcoded, so a future re-measurement
    # calibrates against whatever this mark's own ribs actually turn out to be.
    rib_angles = [r["angle_deg"] for r in wing_facets["ribs"]]
    mean_rib_angle = sum(rib_angles) / len(rib_angles)
    calibration = calibrate_stroke_width_method([0.0, round(mean_rib_angle, 2), 45.0, 90.0])

    stroke_width = {
        "method": "Chamfer (1, sqrt(2)) distance transform + Zhang-Suen thinning "
                  "on the rasterised ink mask (all 9 subpaths, fill-rule nonzero, "
                  "so the 8 counters are already cut out); width at each "
                  "skeleton pixel = 2 x the chamfer distance-to-boundary there. "
                  "min/max are tip-taper and junction-blob artefacts, not "
                  "typical stroke width -- p10/median/mean/p90 are the "
                  "representative figures. The calibration below reports this "
                  "method's own small residual overestimate (chamfer is a much "
                  "closer approximation to true Euclidean distance than a "
                  "4-connected BFS would be, but not exact); the headline "
                  "figures are reported RAW, never silently corrected by it.",
        "measurements_by_render_scale": stroke_width_results,
        "cross_check": {
            "max_median_disagreement_artboard_units": sw_median_disagreement,
            "agrees_within_1_unit": sw_agrees,
        },
        "primary_result_artboard_units": sw_2x,
        "calibration_self_test": calibration,
    }

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
        "wing_facet_angles": wing_facets,
        "stroke_width_along_centreline": stroke_width,
        "not_yet_measured": [
            "A true Euclidean distance transform for the inscribed-circle radii "
            "in interior_counters above -- the current estimate is a "
            "4-connected BFS approximation. (Deliberately NOT the same claim "
            "as stroke_width_along_centreline's own calibration above: that "
            "measures a chamfer transform's bias on a linear strip, a "
            "different geometric setup from a max-distance-within-a-2D-blob "
            "computation, and the two should not be assumed to share a bias "
            "direction without a separate calibration built for blob shapes.)",
            "wing_facet_angles.alternate_disputed_facet, if present above, is "
            "an unresolved judgement call needing a human eye-check against "
            "the rendered mark, not a settled reading.",
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
              f"~{c['inscribed_diameter_artboard_units_estimate']} artboard units, "
              f"elongation {c['elongation_estimate']}")
    print(f"  wing facet ribs ({wing_facets['wing_cluster_subpath_count']} "
          f"subpaths in the angle family, slits {wing_facets['selected_slit_subpaths']}):")
    for r in wing_facets["ribs"]:
        print(f"    {r['angle_deg']} deg")
    print(f"    spread: {wing_facets['spread_deg']} deg")
    if "alternate_disputed_facet" in wing_facets:
        print(f"    NOTE: disputed alternate 4th-facet candidate(s) exist -- "
              f"see wing_facet_angles.alternate_disputed_facet, needs eye-check.")
    print(f"  stroke width along centreline "
          f"({stroke_width_results[1]['n_skeleton_samples']} skeleton samples at "
          f"{stroke_width_results[1]['render_px']}px): median {sw_2x['median']}, "
          f"mean {sw_2x['mean']} artboard units "
          f"({'agrees' if sw_agrees else 'DISAGREES'} with 1x render, diff "
          f"{sw_median_disagreement})")
    print(f"    calibration: chamfer method's own mean overestimate ratio "
          f"{calibration['mean_overestimate_ratio']} on a synthetic known-width strip")
    if not agrees:
        print("  FAIL: the two render scales disagree by more than 2 artboard units.")
        sys.exit(1)
    if not sw_agrees:
        print("  FAIL: the two stroke-width render scales disagree by more than "
              "1 artboard unit.")
        sys.exit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
