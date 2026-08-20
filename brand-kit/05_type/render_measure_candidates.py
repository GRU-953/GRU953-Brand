#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Measure every typography candidate's REAL rendered ink -- the other half of the
measurement, the half a font's own declared metrics cannot substitute for.

A font's OS/2 table states what its designer intended as the x-height. What a real
browser actually draws, at a real pixel size, through real hinting and anti-aliasing,
is a separate fact -- and the gap between the two is exactly where "the type looks
smaller than the numbers say" bugs live. Rendered through Chromium (Playwright), the
same renderer the mark and every other visual measurement in this kit already goes
through, with each font's own exact file embedded as a data: URI so there is no
ambiguity about which bytes are actually being measured.

WHAT IS MEASURED
----------------
Latin and mono candidates: a representative string ("Hxpqg", covering an ascender, an
x-height letter, and three different descender shapes) rendered at a large pixel size;
the INK bounding box is read off real pixels, and the x-height letter's own ink height
is isolated as the practical, rendered x-height -- not the file's declared one.

Bengali candidates: a representative string of real words is rendered, and the মাত্রা
(the headline stroke almost every Bengali letter shares) is found as the row of pixels
with the highest ink density across the string -- not assumed to be at any fixed
position, because vowel signs above and below the baseline would otherwise be
mistaken for it. মাত্রা-to-baseline distance is measured directly from that row to the
string's own ink floor.

The APPARENT-SIZE MULTIPLIER a Latin/Bengali pairing needs is then just the ratio of
two independently measured numbers -- rendered_x_height / rendered_matra_to_baseline --
never assumed, never taken from a foundry's own claimed metrics.

Run:
    PLAYWRIGHT_BROWSERS_PATH=$(pwd)/00_sandbox/browsers ../../.venv/bin/python \
        brand-kit/05_type/render_measure_candidates.py
"""
import base64
import io
import json
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
CANDIDATES_DIR = HERE / "candidates"
REGISTRY_PATH = HERE / "candidates_registry.json"
OUT_PATH = HERE / "rendered_measurements.json"

RENDER_SIZE_PX = 400   # large, so a single pixel of noise is a rounding error, not the story
INK_THRESHOLD = 128

LATIN_TEST_STRING = "Hxpqg"
# A representative Bengali sentence fragment, real words, several matra-bearing
# consonants and a couple of vowel signs above/below -- not a synthetic alphabet run.
BENGALI_TEST_STRING = "সহজ প্রযুক্তি সবার জন্য"


def find_font_file(key: str) -> pathlib.Path:
    files = list((CANDIDATES_DIR / key).glob("*.ttf"))
    return files[0] if files else None


def font_data_uri(path: pathlib.Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:font/ttf;base64,{data}"


def render_string(browser, font_uri: str, text: str, size_px: int) -> Image.Image:
    html = f"""<!doctype html><html><head><style>
      @font-face {{ font-family: 'TestFace'; src: url('{font_uri}') format('truetype'); }}
      html, body {{ margin: 0; padding: 0; background: #fff; }}
      #t {{ font-family: 'TestFace', sans-serif; font-size: {size_px}px; line-height: 1;
            white-space: nowrap; position: absolute; top: 0; left: 0; color: #000; }}
    </style></head><body><div id="t">{text}</div></body></html>"""
    page = browser.new_page(viewport={"width": size_px * len(text) + 200, "height": size_px * 3})
    page.set_content(html)
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(80)
    box = page.eval_on_selector("#t", "el => { const r = el.getBoundingClientRect(); "
                                       "return {x: r.x, y: r.y, w: r.width, h: r.height}; }")
    png_bytes = page.screenshot(clip={"x": 0, "y": 0,
                                       "width": min(size_px * len(text) + 200, 4000),
                                       "height": size_px * 3})
    page.close()
    return Image.open(io.BytesIO(png_bytes)).convert("L")


def ink_rows_and_bbox(img: Image.Image):
    """Return (min_y, max_y, per-row ink pixel counts) over the whole image."""
    w, h = img.size
    px = img.load()
    row_counts = [0] * h
    min_y, max_y = h, -1
    for y in range(h):
        c = 0
        for x in range(w):
            if px[x, y] < INK_THRESHOLD:
                c += 1
        row_counts[y] = c
        if c > 0:
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
    return min_y, max_y, row_counts


def measure_latin(browser, font_uri: str) -> dict:
    img = render_string(browser, font_uri, LATIN_TEST_STRING, RENDER_SIZE_PX)
    min_y, max_y, row_counts = ink_rows_and_bbox(img)
    if max_y < 0:
        return {"error": "no ink rendered"}
    # The x-height letter is 'x' -- isolate its own column span by rendering the
    # single glyph alone and reusing the same row-ink logic, so ascenders/descenders
    # from the rest of the string cannot pollute the x-height reading.
    img_x = render_string(browser, font_uri, "x", RENDER_SIZE_PX)
    x_min_y, x_max_y, _ = ink_rows_and_bbox(img_x)
    img_h = render_string(browser, font_uri, "H", RENDER_SIZE_PX)
    h_min_y, h_max_y, _ = ink_rows_and_bbox(img_h)

    rendered_x_height_px = (x_max_y - x_min_y + 1) if x_max_y >= 0 else None
    rendered_cap_height_px = (h_max_y - h_min_y + 1) if h_max_y >= 0 else None
    return {
        "full_string_ink_bbox_px": {"top": min_y, "bottom": max_y, "height": max_y - min_y + 1},
        "rendered_x_height_px": rendered_x_height_px,
        "rendered_cap_height_px": rendered_cap_height_px,
        "rendered_x_height_over_font_size": (
            round(rendered_x_height_px / RENDER_SIZE_PX, 4) if rendered_x_height_px else None),
        "rendered_cap_height_over_font_size": (
            round(rendered_cap_height_px / RENDER_SIZE_PX, 4) if rendered_cap_height_px else None),
    }


def measure_bengali(browser, font_uri: str) -> dict:
    img = render_string(browser, font_uri, BENGALI_TEST_STRING, RENDER_SIZE_PX)
    min_y, max_y, row_counts = ink_rows_and_bbox(img)
    if max_y < 0:
        return {"error": "no ink rendered"}
    # The matra is the row with the most ink across the WHOLE string -- the one
    # nearly every consonant and most vowel signs touch, which no single fixed
    # y-offset assumption could safely predict across 8 different Bengali designs.
    matra_y = max(range(min_y, max_y + 1), key=lambda y: row_counts[y])
    matra_to_baseline_px = max_y - matra_y
    return {
        "full_string_ink_bbox_px": {"top": min_y, "bottom": max_y, "height": max_y - min_y + 1},
        "matra_row_y_px": matra_y,
        "baseline_row_y_px": max_y,
        "matra_to_baseline_px": matra_to_baseline_px,
        "matra_to_baseline_over_font_size": round(matra_to_baseline_px / RENDER_SIZE_PX, 4),
    }


def main():
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    results = []
    could_not_measure = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for category, families in registry["candidates"].items():
            for key, spec in families.items():
                path = find_font_file(key)
                if not path:
                    could_not_measure.append({"key": key, "family": spec["family"],
                                              "reason": "font file not found"})
                    continue
                try:
                    uri = font_data_uri(path)
                    if category == "bengali":
                        m = measure_bengali(browser, uri)
                    else:
                        m = measure_latin(browser, uri)
                    m.update({"key": key, "family": spec["family"], "category": category,
                             "incumbent": spec.get("incumbent", False)})
                    results.append(m)
                    if category == "bengali":
                        print(f"  {spec['family']}: matra/font-size = "
                              f"{m.get('matra_to_baseline_over_font_size')}")
                    else:
                        print(f"  {spec['family']}: x-height/font-size = "
                              f"{m.get('rendered_x_height_over_font_size')}, "
                              f"cap/font-size = {m.get('rendered_cap_height_over_font_size')}")
                except Exception as e:
                    could_not_measure.append({"key": key, "family": spec["family"],
                                              "reason": f"{type(e).__name__}: {e}"})
        browser.close()

    # The apparent-size multiplier for the incumbent pairing and every Bengali
    # candidate against the incumbent Latin face, since that is the pairing decision
    # actually on the table.
    sora = next((r for r in results if r["key"] == "sora"), None)
    pairings = []
    if sora and sora.get("rendered_x_height_over_font_size"):
        for r in results:
            if r["category"] == "bengali" and r.get("matra_to_baseline_over_font_size"):
                ratio = sora["rendered_x_height_over_font_size"] / r["matra_to_baseline_over_font_size"]
                pairings.append({
                    "latin": "Sora", "bengali": r["family"],
                    "latin_x_height_over_font_size": sora["rendered_x_height_over_font_size"],
                    "bengali_matra_over_font_size": r["matra_to_baseline_over_font_size"],
                    "bengali_size_multiplier_needed": round(ratio, 4),
                })

    out = {
        "$note": "The RENDERED half of the type measurement -- real ink through "
                 "Chromium, never a font's own declared metrics. Regenerate: "
                 "python3 brand-kit/05_type/render_measure_candidates.py",
        "render_size_px": RENDER_SIZE_PX,
        "latin_test_string": LATIN_TEST_STRING, "bengali_test_string": BENGALI_TEST_STRING,
        "measured_count": len(results), "could_not_measure_count": len(could_not_measure),
        "measurements": results, "could_not_measure": could_not_measure,
        "sora_bengali_pairings": pairings,
    }
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{len(results)} measured, {len(could_not_measure)} could not be measured.")
    for c in could_not_measure:
        print(f"  {c['family']}: {c['reason']}")
    return 0 if not could_not_measure else 1


if __name__ == "__main__":
    sys.exit(main())
