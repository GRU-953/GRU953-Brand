#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""GRU953 sandbox smoke test.

Runs a REAL job through every pinned tool — not an import, which proves only that
a package exists on disk. An import cannot tell you Brotli is missing from
fontTools, that Chromium cannot actually launch under this user, or that uharfbuzz
was installed without its font-shaping tables. Every check here does the smallest
piece of real work that would fail if the tool were broken, misconfigured, or
missing an optional extra.

Exit 0: every tool did its job. Exit 2: something could not run — printed as
"NOT EQUIPPED", never silently swallowed as a pass.

    PLAYWRIGHT_BROWSERS_PATH=$(pwd)/00_sandbox/browsers .venv/bin/python 00_sandbox/smoke.py
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
FONT_BENGALI = ROOT / "brand-kit/05_type/source-fonts/Noto_Sans_Bengali/NotoSansBengali[wdth,wght].ttf"

failures = []
not_equipped = []


def ok(label):
    print(f"  ✓ {label}")


def fail(label, detail):
    print(f"  ✗ {label} — {detail}")
    failures.append(label)


def missing(label, detail):
    print(f"  ! {label} — NOT EQUIPPED — {detail}")
    not_equipped.append(label)


print("GRU953 sandbox smoke test")
print()

# ---------------------------------------------------------------- coloraide
try:
    from coloraide import Color
    c = Color("oklch(70% 0.15 250)").convert("srgb")
    hexval = c.to_string(hex=True)
    ratio = Color("white").contrast(Color("black"), method="wcag21")
    assert hexval.startswith("#") and len(hexval) == 7
    assert abs(ratio - 21.0) < 0.01, f"white-on-black contrast should be 21:1, got {ratio}"
    ok(f"coloraide: OKLCH→sRGB ({hexval}), white/black contrast = {ratio:.2f}:1")
except Exception as e:
    fail("coloraide", str(e))

# ---------------------------------------------------------------- fontTools + brotli (woff2)
try:
    from fontTools.ttLib import TTFont
    import brotli  # noqa: F401  — proves the woff2 decoder's actual dependency is present
    if FONT_BENGALI.exists():
        font = TTFont(str(FONT_BENGALI))
        cmap = font.getBestCmap()
        assert 0x09AC in cmap, "Bengali letter ব (U+09AC) missing from cmap"
        ok(f"fontTools + brotli: opened {FONT_BENGALI.name}, {len(cmap)} cmap entries, ব present")
    else:
        missing("fontTools + brotli", f"{FONT_BENGALI} not found — cannot prove a real font opens")
except ImportError as e:
    missing("fontTools + brotli", f"{e}. Install: pip install 'fonttools[woff]'")
except Exception as e:
    fail("fontTools + brotli", str(e))

# ---------------------------------------------------------------- uharfbuzz — real Bangla shaping
try:
    import uharfbuzz as hb
    if FONT_BENGALI.exists():
        blob = hb.Blob.from_file_path(str(FONT_BENGALI))
        face = hb.Face(blob)
        font = hb.Font(face)
        buf = hb.Buffer()
        # ক্ষ — a real Bengali conjunct (ka + virama + ssa). Shaped correctly, this
        # collapses three Unicode code points into fewer glyphs, because HarfBuzz
        # forms the conjunct ligature. Shaped naively (one glyph per code point) it
        # would not.
        conjunct = "ক্ষ"
        buf.add_str(conjunct)
        buf.guess_segment_properties()
        hb.shape(font, buf)
        glyph_count = len(buf.glyph_infos)
        codepoint_count = len(conjunct)
        assert glyph_count < codepoint_count, (
            f"shaping did not reduce {codepoint_count} codepoints to fewer glyphs "
            f"(got {glyph_count}) — the conjunct did not form"
        )
        ok(f"uharfbuzz: shaped ক্ষ — {codepoint_count} codepoints → {glyph_count} glyph(s), "
           f"conjunct formed")
    else:
        missing("uharfbuzz", f"{FONT_BENGALI} not found")
except Exception as e:
    fail("uharfbuzz", str(e))

# ---------------------------------------------------------------- Pillow
try:
    from PIL import Image
    img = Image.new("RGB", (4, 4), (255, 0, 0))
    buf_path = HERE / "_smoke_test.png"
    img.save(buf_path)
    img2 = Image.open(buf_path)
    assert img2.getpixel((0, 0)) == (255, 0, 0)
    buf_path.unlink()
    ok("Pillow: wrote and re-read a 4×4 PNG, pixel round-tripped")
except Exception as e:
    fail("Pillow", str(e))

# ---------------------------------------------------------------- lxml
try:
    from lxml import etree
    svg = etree.fromstring(b'<svg xmlns="http://www.w3.org/2000/svg"><rect/></svg>')
    assert svg.tag.endswith("svg")
    ok("lxml: parsed a minimal SVG fragment")
except Exception as e:
    fail("lxml", str(e))

# ---------------------------------------------------------------- Jinja2 + Markdown
try:
    import jinja2
    import markdown
    rendered = jinja2.Template("{{ n }} + {{ m }} = {{ n + m }}").render(n=2, m=3)
    assert rendered == "2 + 3 = 5"
    html = markdown.markdown("**bold**")
    assert "<strong>bold</strong>" in html
    ok("Jinja2 + Markdown: rendered a template, converted Markdown to HTML")
except Exception as e:
    fail("Jinja2 + Markdown", str(e))

# ---------------------------------------------------------------- Playwright + Chromium
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content('<div id="t" style="color:#B45A39">x</div>')
        colour = page.eval_on_selector("#t", "el => getComputedStyle(el).color")
        page.close()
        browser.close()
    assert colour == "rgb(180, 90, 57)", f"unexpected computed colour: {colour}"
    ok(f"Playwright + Chromium: launched, rendered, read a computed style ({colour})")
except Exception as e:
    missing("Playwright + Chromium", f"{e}. Run: python -m playwright install chromium "
            "(with PLAYWRIGHT_BROWSERS_PATH set)")

# ---------------------------------------------------------------- pypdfium2 — real PDF export via Chromium
try:
    import pypdfium2 as pdfium
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content("<h1>smoke test</h1>")
        pdf_path = HERE / "_smoke_test.pdf"
        page.pdf(path=str(pdf_path))
        page.close()
        browser.close()
    doc = pdfium.PdfDocument(str(pdf_path))
    n_pages = len(doc)
    doc.close()
    pdf_path.unlink()
    assert n_pages == 1
    ok(f"pypdfium2: read back a Chromium-exported PDF, {n_pages} page")
except Exception as e:
    missing("pypdfium2", str(e))

print()
if failures:
    print(f"FAILED — {len(failures)} tool(s) did not do their job: {', '.join(failures)}")
    sys.exit(1)
if not_equipped:
    print(f"NOT EQUIPPED — {len(not_equipped)} tool(s) could not run: {', '.join(not_equipped)}")
    sys.exit(2)
print("PASS — every pinned tool did a real piece of work.")
sys.exit(0)
