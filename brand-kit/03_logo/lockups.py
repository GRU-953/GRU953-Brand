#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Build every GRU953 lockup as a self-contained SVG.

THREE THINGS THIS FILE GUARANTEES, AND WHY EACH ONE MATTERS
-----------------------------------------------------------
1. THERE IS ONE BIRD. Every lockup embeds the same `GRU953-bird.svg` path. There is no
   "detail" build and no "core" build any more; those were separate constructions that
   drifted apart, and a mark that drifts is not a mark. One drawing cannot drift from
   itself.

2. ALL TEXT IS OUTLINES. The wordmark is Sora at weight 700; the taglines are Noto Sans
   and Noto Sans Bengali at weight 500. Every one is converted to paths, so a lockup
   renders identically on GitHub, in an email, in a PDF and on a machine with no fonts
   installed. It is also what makes the wordmark a fixed mark rather than editable text,
   which the trademark policy depends on.

3. THE BANGLA IS SHAPED, NOT CONCATENATED. Bangla needs real text shaping — conjuncts
   join, and some vowel signs are written before the consonant they follow. Pulling glyphs
   out of the font by code point produces nonsense. Inkscape (which shapes through
   HarfBuzz) does the conversion here, and the result is checked by eye in the guidebook.

Run:  cd 03_logo && python3 lockups.py
"""
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Identity
from svgpathtools import parse_path
import pathlib, subprocess, re, json, tempfile, sys

HERE = pathlib.Path(__file__).resolve().parent
# Resolved from THIS FILE, not typed. An absolute path baked in here worked on exactly
# one machine — the one the kit was built on — and made every clone of this
# repository fail at the first svgo call.
SANDBOX = str(pathlib.Path(__file__).resolve().parent.parent / "00_sandbox")
SRC_SORA = HERE / "../05_type/source-fonts/Sora/Sora[wght].ttf"
WORD = "GRU953"
WEIGHT = 700
TRACKING = -0.022        # em, matching the -.022em letter-spacing of the type system

TAGLINE_EN = "Simple technology. For everyone."
TAGLINE_BN = "সহজ প্রযুক্তি। সবার জন্য।"
# The instanced font families installed for Inkscape. Renamed to unique names so fontconfig
# cannot pick the wrong weight of a variable font that shares the family name.
FAM_EN = "GRUNotoSansFive"
FAM_BN = "GRUNotoBengaliFive"


# ------------------------------------------------------------------ the one bird
def bird():
    s = (HERE / "GRU953-bird.svg").read_text()
    d = re.search(r'\sd="([^"]+)"', s).group(1)
    x0, x1, y0, y1 = parse_path(d).bbox()
    return d, (x0, y0, x1 - x0, y1 - y0)


BIRD_D, BIRD_BB = bird()


# ------------------------------------------------------------------ the wordmark
font = instancer.instantiateVariableFont(TTFont(str(SRC_SORA)), {"wght": WEIGHT})
upem = font["head"].unitsPerEm
gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]

# IMPORTANT — one <path> PER GLYPH, and fill-rule="nonzero".
#
# An earlier version concatenated all six letter outlines into ONE path and set
# fill-rule="evenodd". With the negative tracking below, adjacent letters overlap very
# slightly; evenodd treats every overlap as a HOLE and punched white gashes through the G,
# the R, the 9, the 5 and the 3. One path per glyph with nonzero winding makes overlap
# simply overlap, which is what a wordmark needs. Do not "simplify" this back to one path.
glyph_ds, x = [], 0.0
for ch in WORD:
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}")
    gs[cmap[ord(ch)]].draw(TransformPen(pen, Identity.translate(x, 0).scale(1, -1)))
    if pen.getCommands():
        glyph_ds.append(pen.getCommands())
    x += hmtx[cmap[ord(ch)]][0] + TRACKING * upem
WORD_W = x - TRACKING * upem                      # drop the trailing letter-space
CAP = font["OS/2"].sCapHeight
WORD_MARKUP = "".join(f'<path d="{d}"/>' for d in glyph_ds)
# The wordmark's bounding box is MEASURED from the outlines, not assumed to be the font's
# cap height. GRU953's 9, 5 and 3 are round-topped, and round shapes overshoot the cap line
# by design so they look the same height as the flat-topped G, R and U. Taking sCapHeight as
# the box made every lockup render about 5.6% taller than the ratios below claimed.
_wx0, _wx1, _wy0, _wy1 = zip(*(parse_path(d).bbox() for d in glyph_ds))
WORD_BB = (min(_wx0), min(_wy0), max(_wx1) - min(_wx0), max(_wy1) - min(_wy0))


# ------------------------------------------------------------------ the taglines
def require_font(family):
    """Refuse to run if the font is missing, instead of quietly using a substitute.

    fontconfig never fails: ask it for a family it does not have and it hands back whatever
    it thinks is closest, with no error and no warning. Inkscape then outlines the WRONG
    typeface and the lockup ships looking almost right. So the family is checked by name
    before anything is drawn.
    """
    r = subprocess.run(["fc-match", "-f", "%{family}", family], capture_output=True, text=True)
    if family.lower() not in r.stdout.lower():
        sys.exit(
            f"FAIL \u2014 the font {family!r} is not installed, and fontconfig silently\n"
            f"substituted {r.stdout.strip()!r}. The lockup would be drawn in the wrong\n"
            f"typeface. Install the instanced fonts first:\n\n"
            f"    python3 05_type/install-fonts.py && fc-cache -f\n")


def outline_text(text, family, size=200.0):
    """Shape `text` in `family` and return (markup, bbox) with the text converted to paths.

    Inkscape shapes through HarfBuzz, so Bangla conjuncts and reordered vowel signs come
    out correct. Doing this by code point would not.
    """
    require_font(family)
    with tempfile.TemporaryDirectory() as td:
        src, dst = pathlib.Path(td) / "in.svg", pathlib.Path(td) / "out.svg"
        esc = text.replace("&", "&amp;").replace("<", "&lt;")
        src.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="8000" height="1200" '
                       'viewBox="0 0 8000 1200">'
                       f'<text x="0" y="800" font-family="{family}" font-size="{size}">'
                       f'{esc}</text></svg>', encoding="utf-8")
        res = subprocess.run(["inkscape", "--export-type=svg", "--export-plain-svg",
                              "--export-text-to-path", f"--export-filename={dst}", str(src)],
                             capture_output=True, text=True, timeout=300)
        if not dst.exists():
            sys.exit(f"FAIL — Inkscape did not convert the tagline to paths.\n{res.stderr}")
        ds = re.findall(r'\sd="([^"]+)"', dst.read_text())
    if not ds:
        sys.exit(f"FAIL — no outlines came back for {text!r}. Is the font {family} installed?")
    xs0, ys0, xs1, ys1 = [], [], [], []
    for d in ds:
        a, b, c, e = parse_path(d).bbox()
        xs0.append(a); xs1.append(b); ys0.append(c); ys1.append(e)
    bb = (min(xs0), min(ys0), max(xs1) - min(xs0), max(ys1) - min(ys0))
    return "".join(f'<path d="{d}"/>' for d in ds), bb


EN_MARKUP, EN_BB = outline_text(TAGLINE_EN, FAM_EN)
BN_MARKUP, BN_BB = outline_text(TAGLINE_BN, FAM_BN)


# ------------------------------------------------------------------ placement helpers
def place(markup, bb, height, left, top):
    """Scale `markup` so its inked height is `height`, and put its top-left at (left, top)."""
    x0, y0, w, h = bb
    s = height / h
    return (f'<g transform="translate({left - x0 * s:.2f} {top - y0 * s:.2f}) '
            f'scale({s:.6f})">{markup}</g>'), w * s


def width_at(bb, height):
    return bb[2] * height / bb[3]


def svg(title, desc, w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-labelledby="lt ld">'
            f'<title id="lt">{title}</title><desc id="ld">{desc}</desc>'
            f'<g fill="currentColor" fill-rule="nonzero">{body}</g></svg>')


def optimise(p):
    """Shrink the file without breaking it.

    cleanupIds MUST stay disabled. svgo renames <title id="lt"> to <title id="a">, and the
    root's aria-labelledby="lt ld" is an attribute value it does not rewrite — so the
    accessible name silently points at nothing and every one of these marks becomes an
    unlabelled graphic. It shipped that way once. Never again.

    svgo failing is also not allowed to pass quietly: an unoptimised file is fine, but a
    zero-byte or truncated one is not, so the result is checked before it is accepted.
    """
    before = p.read_bytes()
    r = subprocess.run(["npx", "--no-install", "svgo", "--config", "svgo.config.mjs",
                        str(p), "-o", str(p)], cwd=SANDBOX, capture_output=True, text=True)
    out = p.read_bytes()
    if r.returncode != 0 or len(out) < 200 or b"<svg" not in out:
        p.write_bytes(before)
        print(f"  ! svgo did not optimise {p.name}: "
              f"{(r.stderr or r.stdout).strip().splitlines()[:1]} \u2014 kept the original")


# ------------------------------------------------------------------ the proportions
# THE OPTICAL RULE THESE NUMBERS COME FROM, stated so they are not magic:
#
#   The bird is a diagonal drawing, wider than it is tall (its ink is 796 x 709 units), and
#   its mass sits low-left while the head reaches high-right. Setting the wordmark to the
#   bird's FULL height would make the type tower over a mark whose actual optical weight is
#   concentrated in the lower half. The rule used here is:
#
#     the wordmark's inked height = the height of the bird's BODY, not of its whole span.
#
#   The body — tail to head, excluding the raised wing — occupies just under two fifths of
#   the total ink height, which is where CAP_R = 0.40 comes from. The gap is set to the
#   type's own height times the golden-section complement (0.72 ~ 1/1.39), which is the
#   smallest gap at which the two elements read as adjacent-but-separate rather than
#   crowded. TAG_R 0.30 keeps the tagline a clear third-level voice under the wordmark, and
#   PAD_R 0.08 is half the clear-space rule applied to the file's own edge, so a lockup
#   dropped straight into a layout already carries part of its own protection.
#
# Change one of these and re-render every lockup; they are a set, not four independent
# knobs.
MARK = 1000.0                 # the bird's inked height; everything else is a fraction of it
CAP_R = 0.40                  # wordmark cap height, as a fraction of the bird's height
GAP_R = 0.72                  # gap between bird and wordmark, as a fraction of the cap height
TAG_R = 0.30                  # tagline height, as a fraction of the wordmark's cap height
PAD_R = 0.08                  # clear space around everything, as a fraction of the bird
CAP_H, PAD = MARK * CAP_R, MARK * PAD_R
TAG_H, LEAD = CAP_H * TAG_R, CAP_H * TAG_R * 1.5
built = []


def emit(name, title, desc, w, h, body):
    p = HERE / name
    p.write_text(svg(title, desc, w, h, body))
    optimise(p)
    built.append(p)


DESC_BIRD = ("The GRU953 Soaring Bird: a climbing bird drawn in fine lines, its wing fanned "
             "into four facets.")
DESC_WORD = f"The GRU953 wordmark, set in Sora at weight {WEIGHT} and converted to outlines."
DESC_TAG = ('The tagline in both languages: "Simple technology. For everyone." and '
            '"সহজ প্রযুক্তি। সবার জন্য।"')

# ---- 1. horizontal ------------------------------------------------------------------
bird_w = width_at(BIRD_BB, MARK)
word_w = width_at(WORD_BB, CAP_H)
gap = CAP_H * GAP_R
W = PAD * 2 + bird_w + gap + word_w
H = PAD * 2 + MARK
g1, _ = place(BIRD_D and f'<path d="{BIRD_D}"/>', BIRD_BB, MARK, PAD, PAD)
g2, _ = place(WORD_MARKUP, WORD_BB, CAP_H, PAD + bird_w + gap, PAD + (MARK - CAP_H) / 2)
emit("GRU953-lockup-horizontal.svg", "GRU953 \u2014 horizontal lockup",
     f"{DESC_BIRD} {DESC_WORD}", W, H, g1 + g2)

# ---- 2. horizontal with the tagline --------------------------------------------------
en_w, bn_w = width_at(EN_BB, TAG_H), width_at(BN_BB, TAG_H)
block_w = max(word_w, en_w, bn_w)
block_h = CAP_H + LEAD + TAG_H + LEAD * 0.75 + TAG_H
W = PAD * 2 + bird_w + gap + block_w
H = PAD * 2 + MARK
top = PAD + (MARK - block_h) / 2
left = PAD + bird_w + gap
g1, _ = place(f'<path d="{BIRD_D}"/>', BIRD_BB, MARK, PAD, PAD)
g2, _ = place(WORD_MARKUP, WORD_BB, CAP_H, left, top)
g3, _ = place(BN_MARKUP, BN_BB, TAG_H, left, top + CAP_H + LEAD)
g4, _ = place(EN_MARKUP, EN_BB, TAG_H, left, top + CAP_H + LEAD + TAG_H + LEAD * 0.75)
emit("GRU953-lockup-horizontal-tagline.svg", "GRU953 — horizontal lockup with the tagline",
     f"{DESC_BIRD} {DESC_WORD} {DESC_TAG}", W, H, g1 + g2 + g3 + g4)

# ---- 3. stacked ----------------------------------------------------------------------
word_w = width_at(WORD_BB, CAP_H * 0.72)
W = PAD * 2 + max(bird_w, word_w)
H = PAD * 2 + MARK + gap * 0.8 + CAP_H * 0.72
inner = W - PAD * 2
g1, _ = place(f'<path d="{BIRD_D}"/>', BIRD_BB, MARK, PAD + (inner - bird_w) / 2, PAD)
g2, _ = place(WORD_MARKUP, WORD_BB, CAP_H * 0.72, PAD + (inner - word_w) / 2,
              PAD + MARK + gap * 0.8)
emit("GRU953-lockup-stacked.svg", "GRU953 — stacked lockup",
     f"{DESC_BIRD} {DESC_WORD} For square and narrow spaces.", W, H, g1 + g2)

# ---- 4. stacked with the tagline -----------------------------------------------------
tag_h = CAP_H * 0.72 * TAG_R
en_w, bn_w = width_at(EN_BB, tag_h), width_at(BN_BB, tag_h)
lead = tag_h * 1.5
W = PAD * 2 + max(bird_w, word_w, en_w, bn_w)
H = PAD * 2 + MARK + gap * 0.8 + CAP_H * 0.72 + lead + tag_h + lead * 0.75 + tag_h
inner = W - PAD * 2
y = PAD + MARK + gap * 0.8
g1, _ = place(f'<path d="{BIRD_D}"/>', BIRD_BB, MARK, PAD + (inner - bird_w) / 2, PAD)
g2, _ = place(WORD_MARKUP, WORD_BB, CAP_H * 0.72, PAD + (inner - word_w) / 2, y)
g3, _ = place(BN_MARKUP, BN_BB, tag_h, PAD + (inner - bn_w) / 2, y + CAP_H * 0.72 + lead)
g4, _ = place(EN_MARKUP, EN_BB, tag_h, PAD + (inner - en_w) / 2,
              y + CAP_H * 0.72 + lead + tag_h + lead * 0.75)
emit("GRU953-lockup-stacked-tagline.svg", "GRU953 — stacked lockup with the tagline",
     f"{DESC_BIRD} {DESC_WORD} {DESC_TAG}", W, H, g1 + g2 + g3 + g4)

# ---- 5. the wordmark alone -----------------------------------------------------------
cap = 1000.0
pad = cap * 0.16
w = width_at(WORD_BB, cap)
g, _ = place(WORD_MARKUP, WORD_BB, cap, pad, pad)
emit("GRU953-wordmark.svg", "GRU953 — wordmark", DESC_WORD, w + pad * 2, cap + pad * 2, g)

# ---- 6. the tagline alone ------------------------------------------------------------
th = 200.0
pad = th * 0.6
en_w, bn_w = width_at(EN_BB, th), width_at(BN_BB, th)
w = max(en_w, bn_w)
g3, _ = place(BN_MARKUP, BN_BB, th, pad + (w - bn_w) / 2, pad)
g4, _ = place(EN_MARKUP, EN_BB, th, pad + (w - en_w) / 2, pad + th * 2.1)
emit("GRU953-tagline.svg", "GRU953 — the tagline, both languages", DESC_TAG,
     w + pad * 2, th * 3.1 + pad * 2, g3 + g4)

# ------------------------------------------------------------------ manifest and checks
meta = {}
for p in built:
    s = p.read_text()
    if "<text" in s:
        sys.exit(f"FAIL \u2014 {p.name} still contains live text. Every lockup must be outlines.")
    # The accessible name must actually resolve. aria-labelledby pointing at an id that does
    # not exist is worse than no label: assistive technology reports the graphic as unnamed
    # while the file looks correct to anyone reading the source.
    for ref in re.search(r'aria-labelledby="([^"]+)"', s).group(1).split():
        if f'id="{ref}"' not in s:
            sys.exit(f"FAIL \u2014 {p.name} labels itself with id={ref!r}, which is not in "
                     f"the file. The accessible name would resolve to nothing.")
    vb = re.search(r'viewBox="([^"]+)"', s).group(1).split()
    meta[p.name] = dict(bytes=p.stat().st_size, viewBox=" ".join(vb),
                        aspect=round(float(vb[2]) / float(vb[3]), 3))
    print(f"{p.name:42s} {p.stat().st_size:7,} bytes  aspect {meta[p.name]['aspect']:.3f}")
(HERE / "lockup-manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
print(f"\nwordmark: advance {WORD_W:.0f}/{upem} upem · cap {CAP} · {len(glyph_ds)} glyph paths")
print("every lockup embeds the SAME bird path — one drawing, no builds, nothing to drift")
