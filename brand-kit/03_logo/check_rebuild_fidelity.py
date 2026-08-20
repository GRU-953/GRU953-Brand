#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""The mark-rebuild fidelity harness -- its targets fixed here, before any
grid-based rebuild of the bird exists to be measured against them.

The plan this rebuild follows says exactly why the order matters: "Fidelity
to your drawing is measured, with the targets set *before* they are run...
If the rebuild misses a target, the rebuild is fixed -- never the target."
Shipping the checker and its thresholds first, with no rebuild yet to please
them, is what makes that rule real rather than a slogan.

FIVE TARGETS, ALL MEASURING A CANDIDATE AGAINST THE ORIGINAL DRAWING
---------------------------------------------------------------------
- silhouette overlap >= 0.92 (IoU of the two rendered ink masks)
- contour deviation <= 1.5% of the artboard (outer-boundary nearest-point
  matching, both directions)
- every one of the original's counters maps to exactly one of the
  candidate's, and vice versa (centroid correspondence)
- the four wing-facet angles: EACH rebuilt angle within 1.5 degrees of its
  own corresponding ORIGINAL angle. This is a rebuild-vs-original fidelity
  claim, not a claim that the original's own four angles must agree with
  each other -- v0.11.0's tag message stated it that second, wrong way; see
  the correction recorded in this project's memory. The original's own four
  angles (28.37 / 27.74 / 25.71 / 25.89 degrees) are what a rebuild's own
  four angles are actually measured against, below.
- ink centroid within 1% of the artboard

Deliberately RENDER-based throughout, never a parse of the candidate's own
path data: it works identically whether a candidate is drawn with the
original's cubic Beziers or a grid rebuild's straight polygon lines, because
it never assumes either vocabulary.

SELF-TEST
---------
Compare the original mark against itself. Every metric must land at its
trivial best value -- proof the harness measures what it claims, run before
it is ever used to judge a real candidate. This caught two real bugs during
development: an outer-silhouette-only facet search that (like a design-panel
prototype building toward this same idea) picked three tail edges instead of
wing edges, and a Douglas-Peucker-based straight-edge finder that split one
genuinely straight run into pieces near a curvature transition, both of
which gave the original a nonzero "deviation" from itself before they were
fixed. A second negative control -- a plain circle in the same viewBox,
checked separately, not shipped as a fixture here -- proved every one of the
five metrics correctly FAILS on a genuinely different shape too.

Run:
    PLAYWRIGHT_BROWSERS_PATH="$(pwd)/00_sandbox/browsers" ./.venv/bin/python \
        brand-kit/03_logo/check_rebuild_fidelity.py [candidate.svg]

With no argument: self-test only, writes fidelity-self-test.json.
With a candidate SVG path: checks it against the original, writes
fidelity-report.json, and exits 1 if any target is missed.
"""
import collections
import io
import json
import math
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
ORIGINAL_SVG = HERE / "original" / "GRU953-logo-master.svg"
ARTBOARD = 1024
INK_THRESHOLD = 128

# The original's own four wing-facet angles (analyse_wing_facets, in
# measure_original.py / original-measurements.json), restated here as the
# fixed comparison point every candidate rebuild is measured against.
ORIGINAL_RIB_ANGLES = [28.37, 27.74, 25.71, 25.89]

TARGETS = {
    "silhouette_overlap_min": 0.92,
    "contour_deviation_max_pct": 1.5,
    "facet_angle_deviation_max_deg": 1.5,
    "centroid_offset_max_pct": 1.0,
}


def preflight_chromium():
    """See measure_original.py's own preflight_chromium for the reasoning --
    a missing browser install must exit 2 (not equipped), never crash into
    exit 1 (a real failure) or silently pass."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
    except Exception as e:
        print(f"NOT EQUIPPED: Chromium did not launch ({e}). Run: "
              f"sh 00_sandbox/setup.sh (with PLAYWRIGHT_BROWSERS_PATH set to "
              f"$(pwd)/00_sandbox/browsers) and re-run this script.")
        sys.exit(2)


# ---------------------------------------------------------------- rendering

def render_mask(svg_path: pathlib.Path, px: int) -> list:
    svg_text = svg_path.read_text(encoding="utf-8")
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
    return [[data[x, y] < INK_THRESHOLD for x in range(px)] for y in range(px)]


# ---------------------------------------------------------------- silhouette overlap

def silhouette_overlap(mask_a: list, mask_b: list) -> float:
    """Intersection over union of two ink masks -- 1.0 for identical
    silhouettes, 0.0 for silhouettes that never overlap at all."""
    h, w = len(mask_a), len(mask_a[0])
    inter = union = 0
    for y in range(h):
        ra, rb = mask_a[y], mask_b[y]
        for x in range(w):
            a, b = ra[x], rb[x]
            if a or b:
                union += 1
                if a and b:
                    inter += 1
    return inter / union if union else 1.0


# --------------------------------------------------------- boundary trace (Moore)
#
# Format-agnostic by construction: walks whatever pixels are lit in a mask,
# never the SVG's own path commands. Works identically on the original's
# outer silhouette, on each of its interior counters (given that counter's
# own standalone mask, see region_mask_from_pts), and on a candidate drawn
# with an entirely different vocabulary of path commands.

DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def _get(mask, x, y, w, h):
    return mask[y][x] if 0 <= x < w and 0 <= y < h else 0


def find_start_pixel(mask: list, w: int, h: int):
    """First ink pixel in raster order -- guaranteed to be on the region's
    OUTER boundary (or, for a standalone counter mask, that counter's own
    outer boundary): it is the first ink reached scanning in from the
    background, so it cannot be inside an enclosed hole."""
    for y in range(h):
        row = mask[y]
        for x in range(w):
            if row[x]:
                return x, y
    return None


def moore_boundary_trace(mask: list, w: int, h: int, start) -> list:
    """Standard Moore-neighbour boundary trace (Jacob's stopping criterion,
    approximate termination), returning an ordered list of (x, y) boundary
    pixels walking the region's outer edge once around."""
    sx, sy = start

    def next_boundary(cur, back_idx):
        cx, cy = cur
        for i in range(1, 9):
            idx = (back_idx + i) % 8
            dx, dy = DIRS[idx]
            nx, ny = cx + dx, cy + dy
            if _get(mask, nx, ny, w, h):
                return (nx, ny), idx
        return None, None

    current = (sx, sy)
    back_idx = 4
    first_next, first_idx = next_boundary(current, back_idx)
    if first_next is None:
        return [current]  # an isolated single pixel
    boundary = [current, first_next]
    c1 = first_next
    back_idx = (first_idx + 4) % 8
    current = first_next
    safety_cap = 40 * (w + h)
    while True:
        nxt, idx = next_boundary(current, back_idx)
        if nxt is None:
            break
        if current == (sx, sy) and nxt == c1:
            break
        boundary.append(nxt)
        back_idx = (idx + 4) % 8
        current = nxt
        if len(boundary) > safety_cap:
            raise RuntimeError("boundary trace did not terminate within safety cap")
    return boundary


def _perp_dist(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    seg_len2 = dx * dx + dy * dy
    if seg_len2 == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / seg_len2
    projx, projy = x1 + t * dx, y1 + t * dy
    return math.hypot(px - projx, py - projy)


# ---------------------------------------------------------------- contour deviation

def _bucket_points(points, cell):
    buckets = collections.defaultdict(list)
    for (x, y) in points:
        buckets[(int(x // cell), int(y // cell))].append((x, y))
    return buckets


def _nearest_dist(buckets, cell, x, y, max_ring=8):
    """Nearest bucketed point to (x, y), searching an expanding ring of
    buckets outward until at least one point is found (or `max_ring` rings
    are exhausted). A fixed single-ring neighbourhood -- tried first --
    returns no candidate, and therefore an unbounded float('inf'), whenever
    two shapes sit further apart than one bucket's width; caught by checking
    this against a plain circle (a shape genuinely far from the bird in
    places), where it surfaced as a literal `Infinity` in the output JSON --
    not valid JSON, and a real bug waiting to break any consumer (a
    browser's JSON.parse, in particular) that reads this file later."""
    bx, by = int(x // cell), int(y // cell)
    for ring in range(max_ring + 1):
        best = float("inf")
        for dbx in range(-ring, ring + 1):
            for dby in range(-ring, ring + 1):
                if ring > 0 and max(abs(dbx), abs(dby)) != ring:
                    continue  # only the new outer shell each ring
                for (px, py) in buckets.get((bx + dbx, by + dby), ()):
                    d = math.hypot(px - x, py - y)
                    if d < best:
                        best = d
        if best < float("inf"):
            return best
    # Genuinely further apart than this search resolves precisely -- a finite
    # sentinel (the artboard's own diagonal) rather than an unbounded value,
    # since a percentage-of-artboard figure needs a finite numerator to mean
    # anything, and no two points on this canvas are further apart than this.
    return math.hypot(ARTBOARD, ARTBOARD)


def contour_deviation(boundary_a_px: list, boundary_b_px: list, scale: int,
                       sample_every: int = 4, cell: int = 16) -> dict:
    """Symmetric nearest-boundary-point distance between two OUTER boundaries
    (both at pixel resolution `scale`x), reported in artboard units. Sampled
    every `sample_every` pixels along each boundary to keep this O(n), and
    bucketed for near-O(1) nearest-neighbour lookup rather than a full scan."""
    a_pts = boundary_a_px[::sample_every]
    b_pts = boundary_b_px[::sample_every]
    buckets_b = _bucket_points(b_pts, cell)
    buckets_a = _bucket_points(a_pts, cell)
    d_a_to_b = [_nearest_dist(buckets_b, cell, x, y) for (x, y) in a_pts]
    d_b_to_a = [_nearest_dist(buckets_a, cell, x, y) for (x, y) in b_pts]
    all_d = sorted(d_a_to_b + d_b_to_a)
    n = len(all_d)
    to_units = lambda px: px / scale
    return {
        "max_artboard_units": round(to_units(all_d[-1]), 3),
        "p95_artboard_units": round(to_units(all_d[int(n * 0.95)]), 3),
        "mean_artboard_units": round(to_units(sum(all_d) / n), 3),
        "max_pct_of_artboard": round(100 * to_units(all_d[-1]) / ARTBOARD, 3),
    }


# ---------------------------------------------------------------- counters

def enclosed_mask(is_white: list) -> list:
    """Same method as measure_original.py's own enclosed_mask: white reachable
    from the border is background; anything left, enclosed on every side by
    ink, is a counter."""
    h, w = len(is_white), len(is_white[0])
    outside = [[False] * w for _ in range(h)]
    q = collections.deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_white[y][x] and not outside[y][x]:
                outside[y][x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if is_white[y][x] and not outside[y][x]:
                outside[y][x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and is_white[ny][nx] and not outside[ny][nx]:
                outside[ny][nx] = True
                q.append((ny, nx))
    return [[is_white[y][x] and not outside[y][x] for x in range(w)] for y in range(h)]


def find_counters(enclosed: list, min_area_px: int = 20) -> list:
    """Connected-component label the enclosed mask. Each region's own pixel
    list is kept (not just its centroid) so a candidate's counters can each
    have their OWN boundary traced later, for the facet-angle check below."""
    h, w = len(enclosed), len(enclosed[0])
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
    for pts in regions:
        cy = sum(p[0] for p in pts) / len(pts)
        cx = sum(p[1] for p in pts) / len(pts)
        out.append({"pixel_count": len(pts), "centroid": (cx / w, cy / h), "pts": pts})
    out.sort(key=lambda r: -r["pixel_count"])
    return out


def region_mask_from_pts(pts: list, h: int, w: int) -> list:
    """A standalone binary mask holding only this one region's own pixels --
    lets moore_boundary_trace walk a COUNTER's own boundary exactly as it
    walks the outer silhouette's, since the trace is generic to any 2D blob,
    not specific to ink-vs-background polarity."""
    mask = [[False] * w for _ in range(h)]
    for (y, x) in pts:
        mask[y][x] = True
    return mask


def counter_correspondence(counters_a: list, counters_b: list, max_dist: float = 0.05) -> dict:
    """Greedy nearest-centroid matching between two counter lists. An orphan
    on the candidate side (a counter the original does not have) is exactly
    as much a fidelity problem as one the candidate is missing."""
    remaining_b = list(range(len(counters_b)))
    matches, orphans_a = [], []
    for i, ca in enumerate(counters_a):
        best_j, best_d = None, float("inf")
        for j in remaining_b:
            cb = counters_b[j]
            d = math.hypot(ca["centroid"][0] - cb["centroid"][0],
                            ca["centroid"][1] - cb["centroid"][1])
            if d < best_d:
                best_j, best_d = j, d
        if best_j is not None and best_d <= max_dist:
            matches.append((i, best_j, round(best_d, 4)))
            remaining_b.remove(best_j)
        else:
            orphans_a.append(i)
    orphans_b = remaining_b
    return {
        "matched": len(matches),
        "orphans_in_original": len(orphans_a),
        "orphans_in_candidate": len(orphans_b),
        "one_to_one": (len(orphans_a) == 0 and len(orphans_b) == 0
                       and len(matches) == len(counters_a) == len(counters_b)),
        "match_detail": matches,
    }


# ---------------------------------------------------------------- facet angles

def _tls_angle_and_max_resid(points):
    n = len(points)
    mx = sum(p[0] for p in points) / n
    my = sum(p[1] for p in points) / n
    sxx = sum((p[0] - mx) ** 2 for p in points) / n
    syy = sum((p[1] - my) ** 2 for p in points) / n
    sxy = sum((p[0] - mx) * (p[1] - my) for p in points) / n
    theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
    dx, dy = math.cos(theta), math.sin(theta)
    max_resid = max(abs(-(x - mx) * dy + (y - my) * dx) for (x, y) in points)
    return math.degrees(theta) % 180.0, (mx, my), max_resid


def straight_long_edges(boundary: list, scale: int, sample_every: int = 2,
                         residual_max_units: float = 1.0,
                         min_len_units: float = 30.0) -> list:
    """Incremental residual-gated straight-run finding directly on boundary
    pixels (sampled every `sample_every` for speed) -- mirrors
    measure_original.py's own chains_for_subpath exactly (grow a run while
    the WHOLE accumulated set's own least-squares fit stays within a
    residual cap), operating on rendered boundary pixels instead of
    Bezier-sampled points, so it works on any candidate's own boundary
    regardless of what path commands drew it.

    Deliberately NOT a single-shot Douglas-Peucker simplification: DP's
    global epsilon can split one genuinely long straight run into several
    shorter pieces near a slight curvature transition -- an earlier version
    of this function did exactly that, and the self-test (compare the
    original against itself) caught it: it reported a nonzero 3.38-degree
    facet-angle "deviation" between the original and itself, which any
    correct method must report as ~0."""
    pts = boundary[::sample_every]
    n = len(pts)
    resid_cap = residual_max_units * scale

    runs = []
    cur = [pts[0]]
    i = 1
    while i <= n:
        p = pts[i % n]
        trial = cur + [p]
        if len(trial) < 3:
            cur = trial
            i += 1
            continue
        _, _, max_resid = _tls_angle_and_max_resid(trial)
        if max_resid <= resid_cap:
            cur = trial
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [p]
        i += 1
        if i > n * 2:  # safety: never loop more than twice around a closed boundary
            break
    if len(cur) >= 2:
        runs.append(cur)

    out = []
    for run in runs:
        p_start, p_end = run[0], run[-1]
        length = math.hypot(p_end[0] - p_start[0], p_end[1] - p_start[1])
        if (length / scale) < min_len_units:
            continue
        angle, centroid, _ = _tls_angle_and_max_resid(run)
        out.append({"length_units": round(length / scale, 2),
                     "angle_deg": round(angle, 2), "centroid": centroid})
    out.sort(key=lambda e: -e["length_units"])
    return out


def facet_angle_fidelity(original_ribs: list, candidate_edges: list) -> list:
    """Match each of the original's 4 rib angles to its closest remaining
    candidate edge angle (greedy -- only 4 items, so this is exact enough),
    and report the per-rib deviation."""
    remaining = list(candidate_edges)
    results = []

    def angdiff(a, b):
        d = abs(a - b) % 180.0
        return min(d, 180.0 - d)

    for orig_angle in original_ribs:
        if not remaining:
            results.append({"original_angle_deg": orig_angle, "matched": False})
            continue
        best = min(remaining, key=lambda e: angdiff(e["angle_deg"], orig_angle))
        remaining.remove(best)
        results.append({
            "original_angle_deg": orig_angle,
            "candidate_angle_deg": best["angle_deg"],
            "deviation_deg": round(angdiff(best["angle_deg"], orig_angle), 3),
            "candidate_edge_length_units": best["length_units"],
            "matched": True,
        })
    return results


# ---------------------------------------------------------------- centroid offset

def ink_centroid(mask: list):
    h, w = len(mask), len(mask[0])
    sx = sy = n = 0
    for y in range(h):
        row = mask[y]
        for x in range(w):
            if row[x]:
                sx += x
                sy += y
                n += 1
    return (sx / n, sy / n) if n else (0, 0)


# ---------------------------------------------------------------- top-level check

def check_fidelity(candidate_svg_path: pathlib.Path, render_scale: int = 2) -> dict:
    px = ARTBOARD * render_scale
    orig_mask = render_mask(ORIGINAL_SVG, px)
    cand_mask = render_mask(candidate_svg_path, px)

    overlap = silhouette_overlap(orig_mask, cand_mask)

    orig_start = find_start_pixel(orig_mask, px, px)
    cand_start = find_start_pixel(cand_mask, px, px)
    orig_boundary = moore_boundary_trace(orig_mask, px, px, orig_start)
    cand_boundary = moore_boundary_trace(cand_mask, px, px, cand_start)
    deviation = contour_deviation(orig_boundary, cand_boundary, render_scale)

    orig_white = [[not v for v in row] for row in orig_mask]
    cand_white = [[not v for v in row] for row in cand_mask]
    orig_counters = find_counters(enclosed_mask(orig_white))
    cand_counters = find_counters(enclosed_mask(cand_white))
    correspondence = counter_correspondence(orig_counters, cand_counters)

    # Long straight edges from the OUTER silhouette alone structurally cannot
    # see the wing's own nested facet-gap counters (a Moore-trace of the
    # exterior never touches an enclosed hole). Pool edges from the
    # silhouette AND every one of the candidate's own counters, mirroring
    # analyse_wing_facets' use of all 9 path subpaths (1 silhouette + 8
    # counters) on the original.
    cand_edges = straight_long_edges(cand_boundary, render_scale)
    for c in cand_counters:
        c_mask = region_mask_from_pts(c["pts"], px, px)
        c_start = find_start_pixel(c_mask, px, px)
        if c_start is None:
            continue
        c_boundary = moore_boundary_trace(c_mask, px, px, c_start)
        cand_edges += straight_long_edges(c_boundary, render_scale, min_len_units=10.0)
    cand_edges.sort(key=lambda e: -e["length_units"])
    facets = facet_angle_fidelity(ORIGINAL_RIB_ANGLES, cand_edges)
    max_facet_dev = max((r["deviation_deg"] for r in facets if r["matched"]), default=None)

    orig_centroid = ink_centroid(orig_mask)
    cand_centroid = ink_centroid(cand_mask)
    centroid_offset_pct = 100 * math.hypot(
        (orig_centroid[0] - cand_centroid[0]) / px,
        (orig_centroid[1] - cand_centroid[1]) / px)

    verdicts = {
        "silhouette_overlap": {
            "value": round(overlap, 4), "target": f">= {TARGETS['silhouette_overlap_min']}",
            "passes": overlap >= TARGETS["silhouette_overlap_min"]},
        "contour_deviation_pct": {
            "value": deviation["max_pct_of_artboard"],
            "target": f"<= {TARGETS['contour_deviation_max_pct']}",
            "passes": deviation["max_pct_of_artboard"] <= TARGETS["contour_deviation_max_pct"]},
        "counters_one_to_one": {
            "value": correspondence["one_to_one"], "target": "True",
            "passes": correspondence["one_to_one"]},
        "facet_angle_max_deviation_deg": {
            "value": max_facet_dev,
            "target": f"<= {TARGETS['facet_angle_deviation_max_deg']} per facet",
            "passes": (max_facet_dev is not None
                       and max_facet_dev <= TARGETS["facet_angle_deviation_max_deg"])},
        "centroid_offset_pct": {
            "value": round(centroid_offset_pct, 4),
            "target": f"<= {TARGETS['centroid_offset_max_pct']}",
            "passes": centroid_offset_pct <= TARGETS["centroid_offset_max_pct"]},
    }
    try:
        candidate_rel = str(candidate_svg_path.resolve().relative_to(HERE.parent.parent))
    except ValueError:
        candidate_rel = candidate_svg_path.name  # outside the repo (e.g. a scratch fixture)
    return {
        "candidate": candidate_rel,
        "render_scale": render_scale,
        "silhouette_overlap": round(overlap, 4),
        "contour_deviation": deviation,
        "counter_correspondence": correspondence,
        "facet_angle_fidelity": facets,
        "centroid_offset_pct": round(centroid_offset_pct, 4),
        "verdicts": verdicts,
        "all_pass": all(v["passes"] for v in verdicts.values()),
    }


def main():
    preflight_chromium()
    print("=== SELF-TEST: the original mark checked against itself ===")
    print("Every metric below must land at its trivial best value -- this is the")
    print("harness's own proof that it measures what it claims, before it is ever")
    print("used to judge a real rebuild candidate.")
    self_result = check_fidelity(ORIGINAL_SVG)
    print(json.dumps(self_result["verdicts"], indent=2))
    self_ok = self_result["all_pass"]
    print(f"self-test all_pass: {self_ok}")

    out = {
        "$note": "The mark-rebuild fidelity harness's own self-test: the original "
                 "mark checked against itself. Every metric must be at its trivial "
                 "best. Regenerate: python3 brand-kit/03_logo/check_rebuild_fidelity.py",
        "targets": TARGETS,
        "original_rib_angles_deg": ORIGINAL_RIB_ANGLES,
        "self_test": self_result,
    }
    (HERE / "fidelity-self-test.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {HERE / 'fidelity-self-test.json'}")

    if not self_ok:
        print("FAIL: the harness does not pass its own self-test -- do not trust it "
              "to judge a real candidate until this is fixed.")
        return 1

    if len(sys.argv) > 1:
        candidate_path = pathlib.Path(sys.argv[1]).resolve()
        if not candidate_path.exists():
            print(f"FAIL: candidate SVG not found: {candidate_path}")
            return 1
        print(f"\n=== CANDIDATE: {candidate_path} ===")
        result = check_fidelity(candidate_path)
        print(json.dumps(result["verdicts"], indent=2))
        (HERE / "fidelity-report.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {HERE / 'fidelity-report.json'}")
        if not result["all_pass"]:
            print("FAIL: the candidate misses at least one fidelity target above.")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
