#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""GRU953 — brand guidebook builder.

Assembles one self-contained HTML file: fonts, logos, artwork, tokens and every chapter
are embedded, so the guidebook works with no internet connection and no missing assets.
Re-run this after editing any chapter markdown or regenerating the tokens.

    python3 08_guidebook/build.py
"""
import base64, json, os, pathlib, re, subprocess, html as ihtml
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
GB = ROOT / "08_guidebook"
A = GB / "assets"
DATE = "13 August 2026"
# The taglines are LOCKED. They appear in the hero, the running header, the footer and the
# print header, and nothing may paraphrase or shorten them.
TAGLINE_EN = "Simple technology. For everyone."
TAGLINE_BN = "সহজ প্রযুক্তি। সবার জন্য।"

# ------------------------------------------------------------------ embedded resources
def b64(p, mime):
    return f"data:{mime};base64,{base64.b64encode(pathlib.Path(p).read_bytes()).decode()}"

def font_face(family, file, extra=""):
    return (f'@font-face{{font-family:"{family}";'
            f'src:url({b64(A / "fonts" / file, "font/woff2")}) format("woff2");'
            f'font-weight:100 900;font-style:normal;font-display:block;{extra}}}')

BENGALI_RANGE = ("unicode-range:U+0951-0952,U+0964-0965,U+0980-09FE,"
                 "U+200C-200D,U+20B9,U+25CC,U+A8F1;")
LATIN_RANGE = ("unicode-range:U+0000-00FF,U+0100-02BA,U+02BD-02C5,U+02C7-02CC,"
               "U+02CE-02D7,U+02DD-02FF,U+0131,U+0152-0153,U+1E00-1E9F,"
               "U+2000-206F,U+20AC,U+2122;")

def specimen_face(name, file):
    """A rejected candidate, subset to the characters the comparison actually shows.

    These four faces are SIL OFL 1.1 like the five that were chosen, and their licences
    travel with them in assets/fonts/specimen/. Subsetting is a permitted modification;
    none of them declares a Reserved Font Name, so the subsets keep their own names.

    The first version of the comparison named these faces in CSS without loading them, so all
    five specimens rendered in the same fallback and the page presented five identical words
    as evidence for a decision. Subsetting each to "GRU9530123456789" costs 2-10 kB and makes
    the comparison true.
    """
    return (f'@font-face{{font-family:"{name}";'
            f'src:url({b64(A / "fonts/specimen" / file, "font/woff2")}) format("woff2");'
            f'font-weight:100 900;font-style:normal;font-display:block}}')


SPECIMENS = [("Spec Space Grotesk", "Space_Grotesk.woff2"),
             ("Spec Chivo", "Chivo.woff2"),
             ("Spec Bricolage", "Bricolage_Grotesque.woff2"),
             ("Spec Geist", "Geist.woff2")]

FONTS_CSS = "".join([sf for sf in
                     (specimen_face(n, f) for n, f in SPECIMENS
                      if (A / "fonts/specimen" / f).exists())] + [
    font_face("GRU953 Display", "sora-latin.woff2", LATIN_RANGE),
    font_face("GRU953 Display", "notosansbengali.woff2", BENGALI_RANGE),
    font_face("GRU953 Text", "notosans-latin.woff2", LATIN_RANGE),
    font_face("GRU953 Text", "notosansbengali.woff2", BENGALI_RANGE),
    font_face("GRU953 Mono", "jetbrainsmono-latin.woff2"),
])

_svg_seq = [0]


def svg_inline(name, cls="", style=""):
    """Inline a logo SVG with UNIQUE ids.

    Every logo file uses id="t" and id="d" for its title and description. Inlining several
    into one page duplicates those ids, and `aria-labelledby` then resolves to the FIRST
    match — so 28 of 29 marks were announced with the wrong name. Each inline copy gets its
    own suffix.
    """
    s = (ROOT / "03_logo" / name).read_text()
    s = re.sub(r'\s(width|height)="[^"]*"', "", s, count=2)
    _svg_seq[0] += 1
    n = _svg_seq[0]
    s = s.replace('id="t"', f'id="t{n}"').replace('id="d"', f'id="d{n}"')
    s = s.replace('aria-labelledby="t d"', f'aria-labelledby="t{n} d{n}"')
    s = s.replace('aria-labelledby="lt ld"', f'aria-labelledby="lt{n} ld{n}"')
    s = s.replace('id="lt"', f'id="lt{n}"').replace('id="ld"', f'id="ld{n}"')
    s = s.replace('aria-labelledby="at ad"', f'aria-labelledby="at{n} ad{n}"')
    s = s.replace('id="at"', f'id="at{n}"').replace('id="ad"', f'id="ad{n}"')
    s = s.replace('aria-labelledby="gt gd"', f'aria-labelledby="gt{n} gd{n}"')
    s = s.replace('id="gt"', f'id="gt{n}"').replace('id="gd"', f'id="gd{n}"')
    s = s.replace("<svg ", f'<svg class="{cls}" style="{style}" ')
    return s

# Every mark the guidebook inlines. One bird, one tile, six lockups.
LOGOS = {n: (ROOT / "03_logo" / n).read_text() for n in [
    "GRU953-bird.svg", "GRU953-appicon.svg",
    "GRU953-lockup-horizontal.svg", "GRU953-lockup-horizontal-tagline.svg",
    "GRU953-lockup-stacked.svg", "GRU953-lockup-stacked-tagline.svg",
    "GRU953-wordmark.svg", "GRU953-tagline.svg"]}

TOKENS = json.loads((A / "tokens.json").read_text())
SIG = TOKENS["families"]
ROLES = TOKENS["roles"]
ACC = TOKENS["accent"]
TH = TOKENS["thresholds"]
INK, PAPER = TOKENS["ground"]["ink"], TOKENS["ground"]["paper"]


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _ratio(a, b):
    def lum(h):
        h = h.lstrip("#")
        r, g, bl = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(bl)
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def label_on(bg):
    """Ink or paper on this swatch — MEASURED, not guessed from the step number.

    Choosing by step looked right and was wrong: Verdant and Signal Red are light enough at
    step 500 that white on them measures 2.85:1. The labels on the pages whose whole subject
    is legibility were themselves illegible, and the guidebook's own contrast tables sat two
    screens below them saying so.
    """
    return INK if _ratio(INK, bg) >= _ratio(PAPER, bg) else PAPER
STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]

# ------------------------------------------------------------------ markdown -> html
MD = markdown.Markdown(extensions=[
    "tables", "attr_list", "def_list", "fenced_code", "sane_lists", "md_in_html",
    "pymdownx.tilde", "pymdownx.caret", "toc"])

def md(path_or_text, is_text=False):
    MD.reset()
    src = path_or_text if is_text else pathlib.Path(path_or_text).read_text()
    src = re.sub(r"^---\n.*?\n---\n", "", src, flags=re.S)   # strip any front matter
    out = MD.convert(src)
    # tag Bangla-bearing blocks so the CSS can give them the right leading
    def mark(m):
        """Tag a block lang="bn" only when it is PREDOMINANTLY Bangla.

        The first version tagged any block containing a single Bangla character. That put
        lang="bn" on bilingual paragraphs and on table cells that were mostly English — which
        told a screen reader to pronounce English with Bangla rules, and made the EN-only
        toggle delete thousands of English characters along with the Bangla. A block only
        counts as Bangla if Bangla letters outnumber Latin ones.
        """
        tag, attrs, body = m.group(1), m.group(2), m.group(3)
        if 'lang="bn"' in attrs:
            return m.group(0)
        text = re.sub(r"<[^>]+>", "", body)
        bn = len(re.findall(r"[ঀ-৿]", text))
        latin = len(re.findall(r"[A-Za-z]", text))
        if bn and bn > latin:
            return f"<{tag}{attrs} lang=\"bn\" class=\"has-bn\">{body}</{tag}>"
        return m.group(0)
    out = re.sub(r"<(p|li|td|h[1-6]|blockquote)([^>]*)>(.*?)</\1>", mark, out, flags=re.S)
    # Each chapter already owns the page's <h2>. Demote the markdown's own headings by one
    # level so the document outline is h2 > h3 > h4 > h5 rather than two competing h2s —
    # a flat outline is genuinely hard to navigate with a screen reader.
    for a, b in ((5, 6), (4, 5), (3, 4), (2, 3), (1, 2)):
        out = out.replace(f"<h{a}", f"<h{b}").replace(f"</h{a}>", f"</h{b}>")
    return out

PRINT_MODE = False


def wrap_tables(html):
    """Put every table in a horizontally scrollable box.

    A table with five columns cannot reflow onto a 320px screen. Left alone it either
    crushes its cells into unreadable slivers or pushes the whole page sideways, and the
    second one breaks every other section too. Scrolling the table inside its own box is
    the only answer that keeps the rest of the page intact.
    """
    def one(m):
        if m.group(0).startswith('<div class="tw">'):
            return m.group(0)
        return f'<div class="tw">{m.group(0)}</div>'
    return re.sub(r'(?:<div class="tw"[^>]*>)?<table.*?</table>', one, html, flags=re.S)


def dl(filename, label, data_uri):
    # In the print build the data is left out: a paper page cannot be clicked, and embedding
    # 24 MB of base64 makes Chromium's PDF pipeline emit blank pages.
    if PRINT_MODE:
        return f'<span class="mono dlp">{label}</span>'
    # The visible label is short so the table stays readable, but the accessible name has to
    # say WHAT is being downloaded — 198 links all called "SVG" are useless to a screen reader.
    return (f'<a class="dl" download="{filename}" href="{data_uri}" '
            f'aria-label="Download {filename}">'
            f'<span class="dl-i" aria-hidden="true">↓</span>'
            f'<span aria-hidden="true">{label}</span></a>')

# ------------------------------------------------------------------ generated chapters
def ch_colour():
    h = [f'<p class="lead">Three colours carry the brand, two more carry meaning, and the '
         f'signature is <b>one hue with two tuned values</b> so it is correct in a light '
         f'theme and a dark one. Every number on this page was computed by '
         f'<code>04_colour/engine.py</code>, not chosen by eye and hoped for.</p>']

    # ---- the rule that shapes everything, stated before the swatches
    h.append(f'''<div class="rulebox">
      <h3 class="rb-h">Why the signature has two values</h3>
      <p><b>Luminance</b> is how much light a colour actually emits \u2014 not how colourful
      it looks, just how bright. Contrast is a ratio between two luminances, so it is a
      measure of brightness difference and nothing else.</p>
      <p>To clear 4.5:1 against white a colour must be <em>darker</em> than luminance
      {TH["max_luminance_on_paper"]}; to clear 4.5:1 against the Ink it must be
      <em>lighter</em> than {TH["min_luminance_on_ink"]}. Both cannot be true, so <b>no single
      colour can be this brand\u2019s text colour in both themes</b> \u2014 that is
      arithmetic, not taste. Every figure on this page comes from
      <code>tokens.json</code>, computed at build time; none of them is typed by hand.</p>
      <p>Daybreak is therefore two values from one ramp. Use <code>--gru-accent</code> and
      let the theme choose.</p>
      <p><b>Said precisely: one hue, two calibrated values \u2014 not one colour.</b> The two
      sit {ACC["hue_drift_degrees"]}\u00b0 apart in hue, which is the same colour family, but
      \u0394E {ACC["delta_e_between_values"]} apart in appearance, which is obviously
      different. Side by side a reader will call them two colours; switching from the light
      theme to the dark one, the same reader will say the brand kept its colour. Both are
      true, and the second is the one an identity lives or dies by. This book publishes the
      number rather than claiming the friendlier version.</p>
      <div class="twoup">
        <div class="tv" style="background:#FFFFFF;color:{ACC["light"]}">
          <div class="tv-l mono">light theme</div>
          <div class="tv-h">{ACC["light"]}</div>
          <div class="tv-r mono">{ACC["light_ratio_on_paper"]}:1 on paper</div></div>
        <div class="tv" style="background:{TOKENS["ground"]["ink"]};color:{ACC["dark"]}">
          <div class="tv-l mono">dark theme</div>
          <div class="tv-h">{ACC["dark"]}</div>
          <div class="tv-r mono">{ACC["dark_ratio_on_ink"]}:1 on ink</div></div>
      </div></div>''')

    h.append('<h3>The signature</h3><div class="sigrow">')
    for key in ("meridian", "daybreak", "ember"):
        sg = SIG[key]
        fg = "#FFFFFF" if key == "meridian" else "#0B0E14"
        h.append(f'''<div class="sigcard tilt" style="background:{sg['anchor']};color:{fg}">
          <div class="sig-n">{sg['label']}</div>
          <div class="sig-bn" lang="bn">{sg['bangla']}</div>
          <div class="sig-h mono">{sg['anchor']}</div>
          <div class="sig-note">{sg['note']}</div>
          <div class="sig-meta mono">step {sg['anchor_step']} \u00b7 hue {sg['hue_oklch']}\u00b0</div>
        </div>''')
    for nm, bn, hx, fg, note in [
            ("Ink", "\u0995\u09be\u09b2\u09bf", TOKENS["ground"]["ink"], "#FFFFFF",
             "The dark ground, and body text on paper."),
            ("Paper", "\u0995\u09be\u0997\u099c", TOKENS["ground"]["paper"], "#0B0E14",
             "The light ground. Plain white, deliberately.")]:
        # Both grounds get a border: Paper vanishes on a light page and Ink vanishes on a
        # dark one, so neither can be left to rely on its own fill being visible.
        h.append(f'''<div class="sigcard tilt" style="background:{hx};color:{fg};
          border:1px solid var(--gru-border)">
          <div class="sig-n">{nm}</div><div class="sig-bn" lang="bn">{bn}</div>
          <div class="sig-h mono">{hx}</div><div class="sig-note">{note}</div></div>''')
    h.append("</div>")

    h.append('<h3>The signature gradient \u2014 \u201cfirst light\u201d</h3>'
             '<p>Hero artwork only. Never behind body text, never on the mark itself.</p>'
             f'<div class="gradbar" style="background:linear-gradient(112deg,'
             f'{",".join(TOKENS["gradient_firstlight"])})"></div>')

    h.append("<h3>The full ramps</h3><p>Eleven steps each, monotonic in perceived "
             "lightness, with the brand colour sitting inside its own ramp rather than "
             "bolted on beside it. Hover or focus a swatch to read its value.</p>")
    for key in ("meridian", "daybreak", "ember", "success", "danger"):
        sg = SIG[key]
        h.append(f'<div class="ramp-l mono">{sg["label"]} <span>--gru-{key}-*</span></div>'
                 '<div class="ramp">')
        for st in STEPS:
            hx = sg["ramp"][str(st)] if str(st) in sg["ramp"] else sg["ramp"][st]
            fg = label_on(hx)
            brand = " brand" if st == sg["anchor_step"] else ""
            # No tabindex. The value is printed on the swatch, so there is nothing a
            # keyboard user could reach by focusing it — and 55 empty tab stops between the
            # reader and the next real control is a worse problem than the one it solved.
            h.append(f'<div class="sw{brand}" style="background:{hx};color:{fg}">'
                     f'<b>{st}</b><span class="mono">{hx}</span></div>')
        h.append("</div>")

    h.append("<h3>Which step to use for text</h3><p>Chosen by measurement, not by feel. "
             "Each is the most colourful step that still clears its WCAG 2.2 target with "
             "a safety margin, so rounding to hex can never quietly drop it below.</p>")
    h.append('<div class="tw"><table><thead><tr><th>Family</th><th>Body text on paper<br>'
             '<span class="mono">4.5:1</span></th><th>Emphasis on paper<br>'
             '<span class="mono">7:1</span></th><th>Body text on ink<br>'
             '<span class="mono">4.5:1</span></th><th>UI parts<br>'
             '<span class="mono">3:1</span></th></tr></thead><tbody>')
    for key in ("meridian", "daybreak", "ember", "success", "danger"):
        sg, r = SIG[key], SIG[key]["roles"]
        def c(step):
            if step is None:
                return "\u2014"
            hx = sg["ramp"][str(step)] if str(step) in sg["ramp"] else sg["ramp"][step]
            return (f'<code>{key}-{step}</code><br><span class="chip" style="background:{hx}">'
                    f'</span> <span class="mono">{hx}</span>')
        h.append(f'<tr><td><b>{sg["label"]}</b></td><td>{c(r["text_on_paper"])}</td>'
                 f'<td>{c(r["aaa_on_paper"])}</td><td>{c(r["text_on_ink"])}</td>'
                 f'<td>{c(r["ui_on_paper"])}</td></tr>')
    h.append("</tbody></table></div>")

    # ---- semantic roles, both themes, side by side
    h.append('<h3>Every role, in both themes</h3>'
             '<p>These are the tokens to reach for in an interface. Each one is defined in '
             'both themes and each was measured against its own theme\u2019s background \u2014 '
             'a role is only correct in the theme it belongs to.</p>')
    GROUPS = [("Surfaces", ["bg", "bg-subtle", "surface", "surface-raised", "surface-sunken"]),
              ("Text", ["ink", "ink-muted", "ink-subtle", "ink-inverse"]),
              ("Lines", ["border", "border-strong"]),
              ("The brand", ["brand", "brand-hover", "brand-active", "brand-quiet",
                             "on-brand-quiet", "on-brand"]),
              ("The signature", ["accent", "accent-hover", "accent-active", "accent-quiet",
                                 "on-accent-quiet", "accent-ui", "on-accent"]),
              ("Links", ["link", "link-hover", "link-visited"]),
              ("Focus and disabled", ["focus", "focus-inverse", "disabled-bg", "disabled-ink",
                                      "disabled-border"]),
              ("Meaning", ["info", "info-quiet", "on-info-quiet", "info-border", "on-info",
                           "success", "success-quiet", "on-success-quiet", "success-border",
                           "on-success",
                           "warning", "warning-quiet", "on-warning-quiet", "warning-border",
                           "on-warning",
                           "danger", "danger-quiet", "on-danger-quiet", "danger-border",
                           "danger-hover", "danger-active", "on-danger"]),
              ("Depth", ["overlay"])]
    # A hand-written list of keys beside a generated token file drifts, and `.get(k, "\u2014")`
    # made the drift silent: six roles existed in tokens.json and appeared in no group, so
    # the chapter titled "Every role" was missing six of them and said nothing.
    listed = [k for _, keys in GROUPS for k in keys]
    missing = [k for k in ROLES["light"] if k not in listed]
    extra = [k for k in listed if k not in ROLES["light"]]
    dupes = [k for k in listed if listed.count(k) > 1]
    if missing or extra or dupes:
        raise SystemExit(f"role groups are out of step with tokens.json \u2014 "
                         f"missing {missing}, unknown {extra}, duplicated {sorted(set(dupes))}")
    h.append('<div class="roles">')
    for gname, keys in GROUPS:
        h.append(f'<div class="rolegrp"><div class="rolegrp-n mono">{gname}</div>')
        for k in keys:
            lv, dv = ROLES["light"][k], ROLES["dark"][k]
            h.append(f'<div class="role"><code>--gru-{k}</code>'
                     f'<span class="rsw" style="background:{lv}"></span>'
                     f'<span class="mono rv">{lv}</span>'
                     f'<span class="rsw" style="background:{dv}"></span>'
                     f'<span class="mono rv">{dv}</span></div>')
        h.append("</div>")
    h.append('</div><p class="note">Left swatch is the light theme, right swatch the dark '
             'one. Full values in <code>assets/tokens.css</code> and '
             '<code>assets/tokens.json</code>.</p>')

    # ---- the chart sequence
    h.append('<h3>The chart sequence</h3><p>Six series, spread around the colour wheel and '
             'anchored on the brand\u2019s own two. Every one clears 3:1 against its own '
             'theme\u2019s background, and no two are within \u0394E 10 of each other \u2014 so '
             'they cannot be confused, and colour is never the only thing telling them '
             'apart.</p><div class="charts">')
    for theme in ("light", "dark"):
        bgc = TOKENS["ground"]["paper"] if theme == "light" else TOKENS["ground"]["ink"]
        fgc = TOKENS["ground"]["ink"] if theme == "light" else TOKENS["ground"]["paper"]
        h.append(f'<div class="chartcard" style="background:{bgc};color:{fgc};'
                 f'border:1px solid var(--gru-border)">'
                 f'<div class="mono cc-h">{theme} theme</div><div class="ccbars">')
        for i, sgm in enumerate(TOKENS["charts"][theme], 1):
            h.append(f'<div class="ccbar"><i style="background:{sgm["hex"]};'
                     f'height:{28 + i * 11}px"></i>'
                     f'<span class="mono">{sgm["name"]}</span>'
                     f'<span class="mono cc-r">{sgm["ratio"]}:1</span></div>')
        h.append("</div></div>")
    h.append("</div>")

    h.append("<h3>The measured proof</h3>")
    # CONTRAST.md is a standalone document with its own title and tagline. Inside this
    # chapter both are duplicates, so they are dropped and only the argument is kept.
    proof = md(ROOT / "04_colour" / "CONTRAST.md")
    proof = re.sub(r"^\s*<h2[^>]*>.*?</h2>\s*(<p[^>]*>[^<]*Simple technology[^<]*</p>)?",
                   "", proof, flags=re.S)
    h.append(proof.split("<h3", 1)[0])
    h.append('<details><summary>Open the full computed contrast tables</summary>'
             + "<h3" + proof.split("<h3", 1)[1] + "</details>")
    return "".join(h)


def ch_logo():
    h = ['<p class="lead">The Soaring Bird is Aninda\u2019s own drawing, and what ships is '
         'that drawing \u2014 the master path, unmodified. Nothing is re-traced, thickened or '
         'simplified.</p>']

    h.append('''<div class="rulebox">
      <h3 class="rb-h">There is one bird</h3>
      <p>There were once three size-graded builds. They were three separate constructions,
      they drifted apart, and the smallest one ended up with its wing severed from its body.
      <b>One drawing cannot drift from itself</b>, so one drawing is what ships.</p>
      <p>Below 24px a line drawing stops working \u2014 the strokes thin out and the wing\u2019s
      counters begin to close. The honest answer is not a thinner bird but a different
      object: <b>the tile</b>, where a block of colour carries recognition. That 24px floor
      is checked mechanically on every build; if the counters close, the file is not
      written.</p></div>''')

    h.append('<div class="buildrow">')
    for name, file, rng, note in [
        ("The mark", "GRU953-bird.svg", "24px and above",
         "The bird alone. Set the colour with CSS \u2014 it is drawn with currentColor."),
        ("The tile", "GRU953-appicon.svg", "below 24px, and any filled icon",
         "The same bird in Daybreak on Meridian, at the squircle radius \u2014 a rounded "
         "square, rounder than a normal button corner \u2014 which iOS and Android "
         "expect. Favicon, app icon, avatar.")]:
        h.append(f'''<div class="buildcard lift">
          <div class="buildart{" tile" if "appicon" in file else ""}">{svg_inline(file, "mk")}</div>
          <div class="build-n">{name}</div>
          <div class="build-r mono">{rng}</div>
          <div class="build-note">{note}</div>
          <div class="ladder">{"".join(
            f'<span style="width:{sz}px">{svg_inline(file, "mk")}</span>' for sz in (48, 32, 24, 16))}
          </div></div>''')
    h.append("</div>")

    h.append('<h3>The lockups</h3><p>Every lockup embeds the same bird path and the same '
             'outlined wordmark, so nothing in the set can drift out of step. All text is '
             'converted to outlines \u2014 including the Bangla, which is properly shaped '
             'rather than assembled letter by letter.</p><div class="lockrow">')
    for file, label, note in [
        ("GRU953-lockup-horizontal.svg", "Horizontal",
         "The default. Use wherever there is width \u2014 README headers, site headers, letterheads."),
        ("GRU953-lockup-horizontal-tagline.svg", "Horizontal with the tagline",
         "Use where there is room to say what GRU953 is. This is the form that answers the "
         "\u201cGRU\u201d reading risk before it can start."),
        ("GRU953-lockup-stacked.svg", "Stacked",
         "For square and narrow spaces: a social avatar area, a poster, a business card."),
        ("GRU953-lockup-stacked-tagline.svg", "Stacked with the tagline",
         "Posters, covers, title cards \u2014 anywhere the brand introduces itself."),
        ("GRU953-wordmark.svg", "Wordmark alone",
         "When the mark is already present nearby, or the space is too small for both."),
        ("GRU953-tagline.svg", "The tagline alone",
         "Both languages, as artwork. Use as a footer or a sign-off.")]:
        h.append(f'<div class="lockcard lift"><div class="lockart">'
                 f'{svg_inline(file, "lk")}</div><div class="build-n">{label}</div>'
                 f'<div class="build-note">{note}</div></div>')
    h.append("</div>")

    h.append('<h3>Clear space and minimum size</h3>'
             '<p>Clear space is <b>half the mark\u2019s own height on every side</b>. Nothing '
             'enters it \u2014 no text, no rule, no border, no second logo, no photograph edge. '
             'The diagram shows the rule at 120px.</p>'
             '<div class="clearspace"><div class="csbox">'
             f'<div class="csmark">{svg_inline("GRU953-bird.svg", "mk")}</div></div>'
             '<div class="cslabels mono"><span>\u00bd h</span><span>the mark, height h</span>'
             '<span>\u00bd h</span></div></div>')
    h.append('<div class="tw"><table><thead><tr><th>Asset</th><th>Never smaller than</th>'
             '<th>In print</th></tr></thead><tbody>'
             '<tr><td>Horizontal lockup</td><td><code>120px</code></td><td>25mm wide</td></tr>'
             '<tr><td>Lockup with the tagline</td><td><code>260px</code></td><td>55mm wide</td></tr>'
             '<tr><td>The bird alone</td><td><code>24px</code></td><td>6mm</td></tr>'
             '<tr><td>The tile</td><td><code>16px</code></td><td>\u2014</td></tr>'
             '<tr><td>Anything below 16px</td><td colspan="2">Use no mark at all. '
             'A logo nobody can resolve is worse than no logo.</td></tr></tbody></table></div>')

    h.append('<h3>Approved colour combinations</h3><div class="combos">')
    for bgc, fgc, lab, ratio in [
        ("#1A1753", ACC["dark"], "Daybreak on Meridian", "8.88:1"),
        ("#1A1753", "#FFFFFF", "Paper on Meridian", "16.26:1"),
        ("#0B0E14", ACC["dark"], "Daybreak on Ink", "10.55:1"),
        ("#FFFFFF", "#1A1753", "Meridian on paper", "16.26:1"),
        ("#FFFFFF", ACC["light"], "Daybreak on paper", f'{ACC["light_ratio_on_paper"]}:1'),
        ("#FFFFFF", "#0B0E14", "Ink on paper \u2014 single colour", "19.32:1")]:
        h.append(f'<div class="combo lift" style="background:{bgc};color:{fgc};'
                 f'{"border:1px solid var(--gru-border)" if bgc == "#FFFFFF" else ""}">'
                 f'{svg_inline("GRU953-lockup-horizontal.svg", "lk")}'
                 f'<div class="mono">{lab} \u00b7 {ratio}</div></div>')
    # This ONE panel is deliberately wrong — it is how the rule gets taught. The marker
    # tells the brand checker to skip it, so the counter-example does not read as a defect
    # every time the guidebook is reviewed.
    h.append('<!-- gru953-review: counter-example -->')
    h.append(f'<div class="combo bad"><div class="badart" style="background:#FFFFFF;'
             f'color:{ACC["dark"]}">'
             f'{svg_inline("GRU953-lockup-horizontal.svg", "lk")}</div>'
             f'<div class="mono">{ACC["dark"]} on paper \u00b7 1.83:1 \u00b7 <b>not approved</b> '
             f'\u2014 use {ACC["light"]} instead</div></div>')
    h.append("</div>")

    h.append('<h3>The mark does not move</h3>'
             '<p>No animation, no transition, no hover state on the bird itself. A mark that '
             'moves can be caught mid-movement looking broken \u2014 in a screenshot, in a '
             'thumbnail, on a slow connection. Everything else in this book may animate; the '
             'bird does not.</p>')
    return "".join(h)


def ch_type():
    h = ['<p class="lead">Four faces, each with exactly one job. All five files are SIL '
         'Open Font Licence 1.1, free for any purpose including commercial, and their '
         'licences travel with them in <code>assets/fonts/</code>.</p>']
    h.append('<table><thead><tr><th>Role</th><th>Face</th><th>Why this one</th></tr></thead><tbody>'
             '<tr><td>Display, wordmark, headings</td><td><b>Sora</b></td>'
             '<td>Its numerals decide it. GRU953 contains three digits, and Sora’s 9, 5 and 3 '
             'have flat geometric terminals that read like instrument dials.</td></tr>'
             '<tr><td>Body, Latin</td><td><b>Noto Sans</b></td>'
             '<td>Carried forward. Nothing breaks and nothing is relicensed.</td></tr>'
             '<tr><td>All Bangla</td><td><b>Noto Sans Bengali</b></td>'
             '<td>Carried forward, and genuinely excellent.</td></tr>'
             '<tr><td>Code, labels, metadata</td><td><b>JetBrains Mono</b></td>'
             '<td>Replaces the generic system-monospace stack, so a hash, a hex value or a '
             'file path looks the same on every machine.</td></tr>'
             '<tr><td>Large Bangla display <span class="opt">optional</span></td>'
             '<td><b>Anek Bangla</b></td><td>For a big Bangla headline where Noto Sans Bengali '
             'Bold reads a little even.</td></tr></tbody></table>')
    h.append('<h3>Why Sora, in one picture</h3>'
             '<p>The same six characters in the five faces that made the shortlist, each set '
             'in its own real typeface — the four rejected ones are embedded in this page, '
             'subset to these characters, so this is evidence rather than an assertion. '
             'Watch the digits.</p><div class="typecmp">')
    for fam in ("GRU953 Display", "Space Grotesk", "Chivo", "Bricolage Grotesque", "Geist"):
        chosen = fam == "GRU953 Display"
        h.append(f'<div class="tilt tc{" pick" if chosen else ""}">'
                 f'<div class="tilt tcw" style="font-family:\'{fam}\',sans-serif">GRU953</div>'
                 f'<div class="tilt tcn mono">{"Sora — chosen" if chosen else fam}</div></div>')
    h.append('</div><p class="note">Rejected, and why, so it is on the record: '
             '<b>Geist</b> is excellent but it is Vercel’s brand face, so it borrows someone '
             'else’s association. <b>Space Grotesk</b> is strong but its 5 and 3 read as '
             'fashionable. <b>Chivo</b> is too editorial. <b>Bricolage Grotesque</b> is too '
             'busy at display weight.</p>')

    h.append("<h3>The scale</h3><p>A modular scale on a ratio of 1.25, anchored at 16px, "
             "clamped so it shrinks on a phone without needing a media query. Every size "
             "is in <code>rem</code>, so a reader who enlarges their default text is obeyed.</p>")
    h.append('<div class="scale">')
    for tok, label, size in [("4xl", "Hero", "clamp(2.9rem, 1.9rem + 5vw, 5.96rem)"),
                             ("3xl", "h1", "clamp(2.3rem, 1.75rem + 2.75vw, 3.82rem)"),
                             ("2xl", "h2", "clamp(1.85rem, 1.55rem + 1.5vw, 2.44rem)"),
                             ("xl", "h3", "clamp(1.5rem, 1.34rem + .8vw, 1.75rem)"),
                             ("lg", "h4", "clamp(1.25rem, 1.15rem + .5vw, 1.4rem)"),
                             ("md", "Lead", "1.125rem"), ("base", "Body", "1rem"),
                             ("sm", "Small", ".9rem"), ("xs", "Caption", ".8rem")]:
        disp = "gru-display" if tok in ("4xl", "3xl", "2xl", "xl", "lg") else ""
        h.append(f'<div class="scalerow"><span class="mono scaletok">--gru-text-{tok}</span>'
                 f'<span class="{disp}" style="font-size:{size}">Simple technology</span>'
                 f'<span class="mono scalelab">{label}</span></div>')
    h.append("</div>")

    h.append('<h3>Bangla is not Latin with different letters</h3>'
             '<p>Two things must change, and both are easy to get wrong.</p>'
             '<div class="twocol"><div class="do"><div class="mono lab">Do</div>'
             '<p><b>Leading of 1.85.</b> Bangla stacks marks above and below the মাত্রা, the '
             'headline running across the top of most letters. At Latin’s 1.6 those marks '
             'nearly touch the line below.</p>'
             '<p lang="bn" style="line-height:1.85">সহজ প্রযুক্তি, সবার জন্য। কোনো টুল যেন '
             'মানুষকে বিশেষজ্ঞ হতে বাধ্য না করে।</p></div>'
             '<div class="dont"><div class="mono lab">Don’t</div>'
             '<p><b>Never all-caps, never letter-spacing, never a faux bold.</b> Bangla has no '
             'capital letters, so <code>text-transform</code> does nothing useful, and both '
             'letter-spacing and synthetic bolding break conjunct characters.</p>'
             '<p lang="bn" style="line-height:1.35;letter-spacing:.12em">সহজ প্রযুক্তি, সবার জন্য।</p>'
             '<p class="note">That example is deliberately wrong, so the damage is visible.</p>'
             '</div></div>')
    h.append('<h3>The wordmark as live text</h3>'
             '<p>The logo is always the SVG file. But when the word appears as text — an HTML '
             'title, an email signature, a heading — set it with <code>.gru-wordmark</code>: '
             'Sora 700, the wordmark’s own tracking, tabular figures so 953 stays even-width, '
             'and <code>white-space:nowrap</code> so GRU953 never breaks across a line.</p>'
             '<p><span class="gru-wordmark" style="font-size:2rem">GRU953</span></p>')
    return "".join(h)


def ch_assets():
    """Every single file in the kit, embedded in this page and individually downloadable.

    The whole kit is walked, not a hand-picked list, so nothing can be quietly left out — and
    the count in the heading is produced by the walk rather than typed by hand.
    """
    import mimetypes
    mimetypes.add_type("font/woff2", ".woff2")
    mimetypes.add_type("image/svg+xml", ".svg")

    SKIP_DIRS = {".git", "node_modules", "__pycache__", "parts", "candidates", "build",
                 "09_delivery"}
    SKIP_NAMES = {".DS_Store"}
    GROUPS = [
        ("03_logo", "Logo files", "The Soaring Bird, the tile and every lockup, as scalable "
         "vectors \u2014 plus the master drawing they are all built from."),
        ("06_assets/outreach", "Ready-made artwork",
         "Sized exactly for the platform named in each file."),
        ("06_assets/favicon", "Favicon and app icons", "For a website and for the apps."),
        ("06_assets/png", "Logo raster exports",
         "Every mark in every approved colour, for anything that cannot use a vector."),
        ("08_guidebook/assets", "Design tokens, stylesheets and webfonts",
         "Paste these straight into code. The fonts carry their own licences."),
        ("07_templates", "Templates", "Written and ready to use; change the bracketed parts."),
        ("08_guidebook/governance", "Licence and policy documents",
         "The licence, the notice, and the two mark policies."),
        ("02_strategy", "The specification", "The decisions themselves, in full."),
        ("04_colour", "Colour engine and proof",
         "The generator and the computed contrast tables."),
        ("05_type/source-fonts", "Source typefaces",
         "The original variable fonts, each with its licence."),
        ("00_sandbox", "Build tooling", "How the kit was made, and how it is checked."),
        ("08_guidebook/chapters", "Guidebook source", "The chapters as plain markdown."),
        ("01_research", "Research and verification",
         "What was checked, when, against which source, and what could not be verified."),
    ]
    seen, blocks, total, total_bytes = set(), [], 0, 0
    for rel, title, note in GROUPS:
        base = ROOT / rel
        if not base.exists():
            continue
        # os.walk with pruning, not rglob: rglob descends into node_modules and every other
        # skipped directory before throwing the results away, which takes seconds.
        files = []
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS
                                 and not d.startswith("."))
            for fn in sorted(filenames):
                files.append(pathlib.Path(dirpath) / fn)
        keep = []
        for f in files:
            if not f.is_file() or f.name in SKIP_NAMES:
                continue
            if any(part in SKIP_DIRS for part in f.relative_to(ROOT).parts):
                continue
            if f in seen or f.name.startswith("."):
                continue
            if f.suffix.lower() in (".html", ".pdf") and "guidebook" in f.name.lower():
                continue          # do not embed this page inside itself
            seen.add(f)
            keep.append(f)
        files = keep
        if not files:
            continue
        rows = []
        for f in files:
            mime = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
            kb = f.stat().st_size / 1024
            total_bytes += f.stat().st_size
            rows.append(f'<tr><td><code>{f.relative_to(ROOT)}</code></td>'
                        f'<td class="mono num">{kb:,.1f} kB</td>'
                        f'<td>{dl(f.name, f.suffix.lstrip(".").upper() or "FILE", b64(f, mime))}'
                        f'</td></tr>')
        total += len(files)
        blocks.append(
            f'<details class="assetgrp" open><summary><b>{title}</b> '
            f'<span class="mono">{len(files)} file{"s" if len(files) != 1 else ""}</span>'
            f'</summary><p class="note">{note}</p>'
            f'<table class="assets"><thead><tr><th>File</th><th class="num">Size</th>'
            f'<th>Get it</th></tr></thead><tbody>{"".join(rows)}</tbody></table></details>')

    # The whole-kit zip is NOT embedded here, deliberately.
    #
    # Every file that would be inside it already has its own download button on this page, a
    # few lines below. Embedding the zip as well meant carrying a second, compressed copy of
    # the entire kit inside a document that already contains the first copy — about 13 MB of
    # base64 for nothing, and a book that took noticeably longer to open. The zip still ships,
    # in 09_delivery/, for when you want the lot in one move.
    z = ROOT / "09_delivery/GRU953-Brand-Kit.zip"
    zip_row = ""
    if z.exists():
        zip_row = (f'<p class="wholekit note">Want everything in one move? '
                   f'<code>09_delivery/{z.name}</code> '
                   f'({z.stat().st_size / 1048576:,.1f} MB) is the whole kit as a single '
                   f'archive. It is not embedded in this page, because every file in it '
                   f'already has its own button below and carrying both would double the '
                   f'size of this book for nothing.</p>')

    return (f'<p class="lead">Every file in the kit — <b>{total}</b> of them, '
            f'{total_bytes / 1048576:,.1f} MB — is embedded in this page. These buttons work '
            f'with no internet connection, because the data is inside the document you are '
            f'reading.</p>{zip_row}' + "".join(blocks))


# ------------------------------------------------------------------ chapter list
def opt(path, fallback_note):
    p = ROOT / path
    if p.exists():
        return md(p)
    return (f'<div class="pending"><b>Not yet written.</b> This chapter comes from '
            f'<code>{path}</code>, which is not present. {fallback_note}</div>')

def chap(slug):
    return lambda: md(GB / "chapters" / f"{slug}.md")

CHAPTERS = [
    ("welcome", "Welcome", "স্বাগত", chap("welcome")),
    ("brand", "The brand", "ব্র্যান্ড", chap("brand")),
    ("name", "The name", "নাম", chap("name")),
    ("voice", "Voice and tone", "কণ্ঠস্বর ও সুর",
     lambda: opt("02_strategy/VERBAL-IDENTITY.md", "Run the content workflow.")),
    ("bangla", "Writing in Bangla", "বাংলায় লেখা",
     lambda: opt("02_strategy/VERBAL-IDENTITY-BN.md", "Run the content workflow.")),
    ("logo", "The logo", "লোগো", ch_logo),
    ("colour", "Colour", "রং", ch_colour),
    ("type", "Typography", "টাইপোগ্রাফি", ch_type),
    ("design", "Design rules", "ডিজাইন নিয়ম",
     lambda: md(ROOT / "02_strategy/DESIGN-RULES.md")),
    ("apply", "Applications", "প্রয়োগ", chap("apply")),
    ("governance", "Licence and governance", "লাইসেন্স ও পরিচালনা", lambda: ch_governance()),
    ("assets", "Every asset", "সব অ্যাসেট", ch_assets),
]


def ch_governance():
    """The licence answer up front, then the policy documents, then the licences verbatim."""
    h = ['<p class="lead">Four parts, four answers. <b>The system is open</b> under '
         'Apache-2.0 \u2014 use the colours, tokens and CSS for anything, including making '
         'money. <b>The book is source-available</b> under PolyForm Noncommercial 1.0.0 \u2014 '
         'read it, copy it, adapt it, share it, but do not sell it. <b>The marks are not '
         'licensed at all.</b> <b>The typefaces</b> keep their own SIL Open Font Licence.</p>']
    h.append('''<div class="tw"><table class="lic"><thead><tr><th>What</th><th>Licence</th>
      <th>SPDX</th><th>OSI-approved?</th><th>Commercial use?</th></tr></thead><tbody>
      <tr><td><b>The system</b> \u2014 colour tokens, stylesheets, every script in the kit</td>
        <td><b>Apache License 2.0</b></td><td><code>Apache-2.0</code></td>
        <td><b>Yes</b></td>
        <td><b>Yes.</b> Keep the copyright notice and the NOTICE file, and say if you
        changed a file.</td></tr>
      <tr><td><b>The book and the writing</b> \u2014 this guidebook, the chapters, the
        templates, the documentation</td>
        <td><b>PolyForm Noncommercial 1.0.0</b></td>
        <td><code>PolyForm-Noncommercial-1.0.0</code></td>
        <td><b>No</b> \u2014 source-available, not open source</td>
        <td><b>Not without asking.</b> Everything noncommercial is already permitted.</td></tr>
      <tr><td><b>The marks</b> \u2014 the name, the Soaring Bird, the tile, the wordmark,
        any lockup</td>
        <td><b>Not licensed</b></td><td>\u2014</td><td>n/a</td>
        <td><b>No.</b> You may show the unmodified mark to refer to GRU953. Nothing
        more.</td></tr>
      <tr><td><b>The bundled typefaces</b></td>
        <td><b>SIL Open Font Licence 1.1</b></td><td><code>OFL-1.1</code></td>
        <td><b>Yes</b></td>
        <td><b>Yes.</b> Their licences travel with the files.</td></tr>
      <tr><td><b>Colour values</b></td><td>Not restrictable</td><td>\u2014</td><td>n/a</td>
        <td><b>Yes.</b> A hexadecimal number is not property.</td></tr>
      </tbody></table></div>
      <p class="note"><b>Said plainly, because it matters:</b> PolyForm Noncommercial is
      <em>not</em> an open source licence and never will be \u2014 the Open Source Definition
      forbids restricting a field of use, and \u201cnoncommercial only\u201d is exactly that
      restriction. The correct word is <b>source-available</b>. Anyone who calls this book
      open source is wrong, and this book will not be the reason they thought so.</p>
      <p class="note"><b>This is not legal advice.</b> It is a plain-English summary written
      by the kit\u2019s author, who is not a lawyer. The licence files are what actually
      govern.</p>''')

    h.append('<h3>Why this split, and not one licence for everything</h3>'
             '<p>An earlier edition of this kit put <em>everything</em> under Apache-2.0 on '
             'the argument that the boundary could not be drawn cleanly. The boundary can be '
             'drawn cleanly, and it is worth drawing.</p>'
             '<p><b>The system is a component.</b> Colour tokens and stylesheets are the kind '
             'of thing another developer should be able to lift, use and sell without asking '
             'anyone \u2014 which is precisely what an OSI-approved licence guarantees. '
             'Apache-2.0 also states outright that its grant is <em>\u201cperpetual, '
             'worldwide, non-exclusive, no-charge, royalty-free, irrevocable\u201d</em>, so '
             'permanence is written down rather than inferred; and its section 6 reserves the '
             'licensor\u2019s trademarks inside the licence itself, putting the most important '
             'fact about this kit in the document everyone actually reads.</p>'
             '<p><b>The book is an identity.</b> This guidebook is what GRU953 looks and '
             'sounds like. A permissive licence would have let someone sell it, or sell a '
             'rebadged copy of it. That is not a freedom worth granting, and PolyForm '
             'Noncommercial says exactly that and nothing more. It was chosen over the other '
             'PolyForm licences \u2014 Small Business, Perimeter, Shield \u2014 because the '
             'boundary that matters here is commercial versus not, rather than company size '
             'or competition.</p>'
             '<p class="note">One honest limit: the PolyForm licences are drafted for '
             '<em>software</em>, and their text says \u201cthe software\u201d throughout. '
             'Applying one to a document works by defining the document as the licensed work, '
             'which the NOTICE file does \u2014 but that is not the use the drafters had in '
             'mind, and no lawyer has reviewed it.</p>')

    for f, title in [("LICENSING-EXPLAINED.md", "What you may do \u2014 the plain-English answer"),
                     ("TRADEMARKS.md", "Trademark and brand-usage policy"),
                     ("LOGO-USAGE.md", "Logo and visual identity usage policy")]:
        q = GB / "governance" / f
        if not q.exists():
            raise SystemExit(f"governance/{f} is missing \u2014 refusing to build a guidebook "
                             f"that silently omits part of its own licence")
        h.append(f'<details><summary><b>{title}</b> <span class="mono">{f}</span></summary>'
                 f'{md(q)}</details>')

    # The licences and the notice are shipped VERBATIM, never reformatted. All three are
    # required: a guidebook that quietly omits a licence it is distributed under is worse
    # than one with no licence chapter at all, so a missing file fails the build.
    GUARDS = {
        "NOTICE": ("PolyForm Noncommercial License 1.0.0",
                   "NOTICE \u2014 the mark reservation that travels downstream"),
        "LICENSE": ("TERMS AND CONDITIONS FOR USE",
                    "Apache License, Version 2.0 \u2014 the full text, verbatim"),
        "LICENSE-GUIDEBOOK.md": ("PolyForm Noncommercial License 1.0.0",
                                 "PolyForm Noncommercial License 1.0.0 \u2014 the full text, "
                                 "verbatim"),
    }
    for f, (must_contain, title) in GUARDS.items():
        q = GB / "governance" / f
        if not q.exists():
            raise SystemExit(f"governance/{f} is missing \u2014 refusing to build")
        body = q.read_text()
        if must_contain not in body:
            raise SystemExit(f"governance/{f} does not contain {must_contain!r} \u2014 it is "
                             f"not the licence it claims to be. Refusing to build.")
        h.append(f'<details><summary><b>{title}</b> <span class="mono">{f}</span></summary>'
                 f'<pre>{ihtml.escape(body)}</pre></details>')
    return "".join(h)


# ------------------------------------------------------------------------- the shell
CSS = r"""
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:5.5rem}
body{margin:0;background:var(--gru-bg);color:var(--gru-ink);
  font-family:var(--gru-font-text);font-size:1rem;line-height:1.6;
  -webkit-font-smoothing:antialiased}
img,svg{max-width:100%}
a{color:var(--gru-link);text-decoration-thickness:1px;text-underline-offset:.18em}
a:hover{text-decoration-thickness:2px}
code,.mono{font-family:var(--gru-font-mono);font-size:.88em;font-variant-ligatures:none}
code{background:var(--gru-bg-subtle);padding:.12em .38em;border-radius:4px;
  border:1px solid var(--gru-border)}
pre{background:var(--gru-bg-subtle);border:1px solid var(--gru-border);
  border-radius:var(--gru-radius-sm);padding:1rem 1.15rem;overflow-x:auto;font-size:.84rem;
  line-height:1.55}
pre code{background:none;border:0;padding:0}

/* ---------- skip link ---------- */
.skip{position:absolute;left:-9999px}
.skip:focus{left:1rem;top:1rem;z-index:200;background:var(--gru-surface);
  color:var(--gru-link);padding:.6rem 1rem;border-radius:8px;
  border:1px solid var(--gru-border-strong);box-shadow:var(--gru-shadow-2)}

/* ---------- header ---------- */
header.top{position:sticky;top:0;z-index:60;background:var(--gru-bg);
  border-bottom:1px solid var(--gru-border);
  backdrop-filter:saturate(160%) blur(10px)}
.top-in{max-width:96rem;margin:0 auto;padding:.7rem clamp(1rem,3vw,2rem);
  display:flex;align-items:center;gap:1rem}
.brandmark{display:flex;align-items:center;gap:.7rem;color:var(--gru-brand);
  text-decoration:none;flex:none}
.brandmark svg{height:30px;width:auto}
.vtag{font-family:var(--gru-font-mono);font-size:.68rem;font-weight:600;letter-spacing:.1em;
  text-transform:uppercase;color:var(--gru-ink-subtle);border:1px solid var(--gru-border-strong);
  border-radius:99px;padding:.22rem .6rem;white-space:nowrap}
.spacer{flex:1}
.ctl{display:flex;gap:.4rem;align-items:center}
button.b{font:inherit;font-size:.8rem;font-weight:600;cursor:pointer;
  background:var(--gru-surface);color:var(--gru-ink);border:1px solid var(--gru-border-strong);
  border-radius:99px;padding:.4rem .85rem;display:inline-flex;align-items:center;gap:.4rem}
button.b:hover{border-color:var(--gru-brand);color:var(--gru-brand)}
button.b[aria-pressed=true]{background:var(--gru-brand);color:var(--gru-on-brand);
  border-color:var(--gru-brand)}
:focus-visible{outline:3px solid var(--gru-focus);outline-offset:2px;border-radius:3px}

/* ---------- layout ---------- */
.wrap{max-width:96rem;margin:0 auto;padding:0 clamp(1rem,3vw,2rem);
  display:grid;grid-template-columns:16rem minmax(0,1fr);gap:clamp(1.5rem,4vw,3.5rem)}
nav.toc{position:sticky;top:5rem;align-self:start;max-height:calc(100vh - 7rem);
  overflow-y:auto;padding:1.5rem 0 3rem;font-size:.87rem}
nav.toc ol{list-style:none;margin:0;padding:0;counter-reset:c}
nav.toc li{counter-increment:c;margin:.1rem 0}
nav.toc a{display:flex;gap:.6rem;padding:.42rem .6rem;border-radius:7px;
  text-decoration:none;color:var(--gru-ink-muted);border-left:2px solid transparent}
nav.toc a::before{content:counter(c,decimal-leading-zero);
  font-family:var(--gru-font-mono);font-size:.72rem;color:var(--gru-ink-subtle);
  padding-top:.12em}
nav.toc a:hover{background:var(--gru-bg-subtle);color:var(--gru-ink)}
nav.toc a[aria-current=true]{background:var(--gru-accent-quiet);color:var(--gru-brand);
  font-weight:600;border-left-color:var(--gru-accent)}
nav.toc a[aria-current=true]::before{color:var(--gru-brand)}
.toc-h{font-family:var(--gru-font-mono);font-size:.68rem;font-weight:600;letter-spacing:.11em;
  text-transform:uppercase;color:var(--gru-ink-subtle);padding:0 .6rem .6rem}
main{padding:0 0 6rem;min-width:0}

/* ---------- hero ---------- */
.hero{background:var(--gru-meridian-900);color:#fff;border-radius:var(--gru-radius-lg);
  padding:clamp(2rem,5vw,4rem);margin:1.5rem 0 3rem;position:relative;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;background:
  radial-gradient(115% 100% at 3% 108%,#FFAB8E55 0%,#EDB24D30 25%,transparent 58%)}
.hero::after{content:"";position:absolute;inset:0;opacity:.45;
  background:repeating-linear-gradient(0deg,#ffffff0a 0 1px,transparent 1px 4px)}
.hero>*{position:relative;z-index:2}
.hero .hb{width:clamp(76px,9vw,116px);color:var(--gru-daybreak-300);margin-bottom:1.4rem}
.hero h1{font-family:var(--gru-font-display);font-weight:700;letter-spacing:-.03em;
  font-size:clamp(2.2rem,6vw,3.8rem);line-height:1.02;margin:0 0 .5rem;color:#fff}
.hero .sub{font-family:var(--gru-font-display);font-weight:600;
  font-size:clamp(1.1rem,2.4vw,1.6rem);color:var(--gru-daybreak-300);margin:0 0 .3rem}
.hero .subbn{font-size:clamp(1rem,2vw,1.35rem);color:#DDE3FF;line-height:1.8}
.hero .meta{margin-top:1.9rem;display:flex;flex-wrap:wrap;gap:.5rem}
.hero .meta span{font-family:var(--gru-font-mono);font-size:.7rem;font-weight:600;
  letter-spacing:.09em;text-transform:uppercase;border:1px solid #ffffff33;
  border-radius:99px;padding:.35rem .8rem;color:#fff}

/* ---------- chapters ---------- */
section.ch{margin:0 0 4.5rem;scroll-margin-top:5.5rem}
.chnum{font-family:var(--gru-font-mono);font-size:.72rem;font-weight:600;letter-spacing:.12em;
  color:var(--gru-accent);text-transform:uppercase}
section.ch>h2{font-family:var(--gru-font-display);font-weight:700;letter-spacing:-.025em;
  font-size:clamp(1.7rem,4vw,2.4rem);line-height:1.1;margin:.25rem 0 .3rem;
  color:var(--gru-brand)}
section.ch>.h2bn{font-size:1.05rem;color:var(--gru-ink-subtle);margin:0 0 1.6rem;
  padding-bottom:1.1rem;border-bottom:2px solid var(--gru-border)}
section.ch h3{font-family:var(--gru-font-display);font-weight:700;letter-spacing:-.015em;
  font-size:1.3rem;margin:2.4rem 0 .7rem;color:var(--gru-ink)}
section.ch h4{font-family:var(--gru-font-display);font-weight:600;font-size:1.06rem;
  margin:1.7rem 0 .5rem}
section.ch p,section.ch li{max-width:68ch}
p.lead{font-size:1.12rem;line-height:1.55;color:var(--gru-ink-muted);max-width:64ch}
.note{font-size:.87rem;color:var(--gru-ink-subtle);border-left:3px solid var(--gru-border-strong);
  padding-left:.9rem;margin:1rem 0}
blockquote{margin:1.4rem 0;padding:1.1rem 1.4rem;background:var(--gru-bg-subtle);
  border-left:4px solid var(--gru-accent);border-radius:0 var(--gru-radius-sm) var(--gru-radius-sm) 0}
blockquote>*:first-child{margin-top:0}blockquote>*:last-child{margin-bottom:0}
blockquote h2,blockquote h3{margin:.2rem 0;color:var(--gru-brand)}
:lang(bn),.has-bn{line-height:1.85;letter-spacing:normal}
h1:lang(bn),h2:lang(bn),h3:lang(bn),h2.has-bn,h3.has-bn{line-height:1.45}
table{border-collapse:collapse;width:100%;margin:1.3rem 0;font-size:.9rem}
th,td{text-align:left;padding:.65rem .8rem;border-bottom:1px solid var(--gru-border);
  vertical-align:top}
th{font-family:var(--gru-font-mono);font-size:.72rem;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;color:var(--gru-ink-subtle);
  border-bottom:2px solid var(--gru-border-strong)}
tbody tr:hover{background:var(--gru-bg-subtle)}
details{margin:1.2rem 0;border:1px solid var(--gru-border);border-radius:var(--gru-radius-sm);
  background:var(--gru-surface)}
summary{cursor:pointer;padding:.8rem 1rem;font-weight:600;font-size:.94rem}
summary:hover{color:var(--gru-brand)}
details[open] summary{border-bottom:1px solid var(--gru-border)}
details>*:not(summary){padding:0 1rem}
details>*:not(summary):last-child{padding-bottom:1rem}
.pending{border:1px dashed var(--gru-border-strong);border-radius:var(--gru-radius-sm);
  padding:1rem 1.2rem;color:var(--gru-ink-subtle);font-size:.92rem}

/* ---------- colour chapter ---------- */
.sigrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.9rem;
  margin:1.2rem 0 2rem}
.sigcard{border-radius:var(--gru-radius-md);padding:1.2rem 1.1rem;min-height:190px;
  display:flex;flex-direction:column}
.sig-n{font-family:var(--gru-font-display);font-weight:700;font-size:1.35rem;letter-spacing:-.02em}
.sig-bn{font-size:.95rem;opacity:.86;margin-top:.1rem}
.sig-h{font-size:.82rem;font-weight:600;margin-top:.7rem;opacity:.95}
.sig-note{font-size:.83rem;line-height:1.45;margin-top:.7rem;opacity:.88;flex:1}
.sig-meta{font-size:.68rem;opacity:.7;margin-top:.6rem}
.gradbar{height:88px;border-radius:var(--gru-radius-md);margin:.8rem 0 1.5rem}
.ramp-l{font-size:.75rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  margin:1.3rem 0 .35rem;color:var(--gru-ink-muted)}
.ramp-l span{font-weight:400;text-transform:none;letter-spacing:0;color:var(--gru-ink-subtle)}
.ramp{display:flex;border-radius:var(--gru-radius-sm);overflow:hidden;
  border:1px solid var(--gru-border)}
.sw{flex:1;min-width:0;height:76px;display:flex;flex-direction:column;justify-content:flex-end;
  padding:.45rem .35rem;font-size:.62rem;line-height:1.25;position:relative}
.sw b{font-family:var(--gru-font-mono);font-size:.66rem}
.sw span{opacity:.82;font-size:.55rem;overflow:hidden}
.sw.brand::before{content:"●";position:absolute;top:.35rem;left:.4rem;font-size:.6rem;opacity:.9}
/* A scroll box needs a visible ring of its own: it is a tab stop, and a tab stop nobody can
   see is a keyboard trap in everything but name. */
.tw:focus-visible{outline:3px solid var(--gru-focus);outline-offset:-3px}
.chip{display:inline-block;width:.85em;height:.85em;border-radius:3px;
  border:1px solid var(--gru-border);vertical-align:-.1em}

/* ---------- logo chapter ---------- */
.buildrow,.lockrow{display:grid;gap:1rem;margin:1.2rem 0 2rem}
.buildrow{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}
.lockrow{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.buildcard,.lockcard{border:1px solid var(--gru-border);border-radius:var(--gru-radius-md);
  padding:1.1rem;background:var(--gru-surface)}
.buildart{color:var(--gru-brand);height:110px;display:flex;align-items:center;
  justify-content:center;margin-bottom:.8rem}
.buildart svg{height:100%;width:auto}
.lockart{color:var(--gru-brand);min-height:88px;display:flex;align-items:center;
  padding:.5rem 0 1rem}
.lockart.tile{justify-content:center}.lockart.tile svg{width:88px}
.build-n{font-family:var(--gru-font-display);font-weight:700;font-size:1.05rem}
.build-r{font-size:.72rem;color:var(--gru-accent);font-weight:600;margin-top:.15rem}
.build-note{font-size:.84rem;line-height:1.45;color:var(--gru-ink-muted);margin-top:.45rem}
.ladder{display:flex;align-items:flex-end;gap:.9rem;margin-top:.9rem;
  padding-top:.8rem;border-top:1px solid var(--gru-border);color:var(--gru-brand)}
.ladder span{display:block;flex:none}.ladder svg{width:100%;height:auto}
.clearspace{margin:1.2rem 0}
.csbox{width:240px;height:240px;background:
  repeating-linear-gradient(45deg,var(--gru-accent-quiet) 0 6px,transparent 6px 12px);
  border:1px dashed var(--gru-accent);border-radius:var(--gru-radius-sm);
  display:flex;align-items:center;justify-content:center}
.csmark{width:120px;height:120px;background:var(--gru-surface);
  outline:1px solid var(--gru-border-strong);color:var(--gru-brand);
  display:flex;align-items:center;justify-content:center}
.csmark svg{width:100%;height:auto}
.cslabels{display:flex;gap:1.5rem;width:240px;justify-content:space-between;
  font-size:.68rem;color:var(--gru-ink-subtle);margin-top:.5rem}
.combos{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.9rem;
  margin:1.1rem 0}
.combo{border-radius:var(--gru-radius-md);padding:1.2rem 1.1rem}
.combo svg{width:170px;height:auto;display:block;margin-bottom:.9rem}
.combo .mono{font-size:.7rem;opacity:.92}
.combo.bad{border:1px solid var(--gru-daybreak-700);padding:0;overflow:hidden}
.combo.bad .badart{padding:1.2rem 1.1rem}
.combo.bad>.mono{display:block;padding:.7rem 1.1rem;background:var(--gru-daybreak-700);
  color:#fff;font-size:.7rem}

/* ---------- type chapter ---------- */
.typecmp{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.8rem;
  margin:1rem 0}
.tc{border:1px solid var(--gru-border);border-radius:var(--gru-radius-sm);padding:.9rem;
  text-align:center;background:var(--gru-surface)}
.tc.pick{border-color:var(--gru-accent);border-width:2px;background:var(--gru-accent-quiet)}
.tcw{font-size:1.9rem;font-weight:700;letter-spacing:-.022em;color:var(--gru-brand)}
.tcn{font-size:.66rem;color:var(--gru-ink-subtle);margin-top:.4rem}
.tc.pick .tcn{color:var(--gru-brand);font-weight:700}
.scale{margin:1rem 0;border-top:1px solid var(--gru-border)}
.scalerow{display:grid;grid-template-columns:11rem minmax(0,1fr) 5rem;gap:1rem;
  align-items:baseline;padding:.75rem 0;border-bottom:1px solid var(--gru-border)}
.scaletok{font-size:.68rem;color:var(--gru-ink-subtle)}
.scalelab{font-size:.68rem;color:var(--gru-ink-subtle);text-align:right}
.scalerow .gru-display{font-family:var(--gru-font-display);font-weight:700;
  letter-spacing:-.025em;line-height:1.05;color:var(--gru-brand);overflow:hidden}
.twocol{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem;
  margin:1rem 0}
.do,.dont{border-radius:var(--gru-radius-md);padding:1.1rem 1.2rem;
  border:1px solid var(--gru-border)}
.do{border-left:4px solid #056F45}.dont{border-left:4px solid var(--gru-daybreak-700)}
.do .lab,.dont .lab{font-size:.68rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;
  margin-bottom:.5rem}
.do .lab{color:#056F45}.dont .lab{color:var(--gru-daybreak-700)}
.opt{font-family:var(--gru-font-mono);font-size:.6rem;background:var(--gru-bg-subtle);
  border:1px solid var(--gru-border);border-radius:99px;padding:.1rem .45rem;
  color:var(--gru-ink-subtle);text-transform:uppercase;letter-spacing:.08em}

/* ---------- assets chapter ---------- */
table.assets td:last-child{white-space:nowrap}
/* min-height 24px is not decoration: WCAG 2.2 success criterion 2.5.8 sets 24x24 CSS px as
   the minimum target size, and these are the most-tapped controls in the book. */
a.dl{display:inline-flex;align-items:center;justify-content:center;gap:.35rem;
  font-family:var(--gru-font-mono);
  font-size:.7rem;font-weight:700;letter-spacing:.05em;text-decoration:none;
  background:var(--gru-brand);color:var(--gru-on-brand);
  border-radius:99px;padding:.32rem .75rem;min-height:24px;min-width:24px}
a.dl:hover{background:var(--gru-brand-hover)}
.dl-i{font-size:.8rem}

/* ---------- footer ---------- */
footer.f{border-top:1px solid var(--gru-border);margin-top:2rem;padding:2.5rem 0 4rem;
  font-size:.85rem;color:var(--gru-ink-subtle)}
footer.f svg{width:150px;color:var(--gru-brand);margin-bottom:1rem}

/* ---------- Bangla-hidden mode ---------- */
body.no-bn [lang="bn"]:not(.keep-bn),body.no-bn .has-bn:not(.keep-bn){display:none}
body.only-bn .en-only{display:none}

/* ---------- responsive ---------- */
@media(max-width:64rem){
 .wrap{grid-template-columns:1fr}
  nav.toc{position:static;max-height:none;border-bottom:1px solid var(--gru-border);
    padding-bottom:1rem}
  nav.toc ol{display:flex;flex-wrap:wrap;gap:.2rem}
  nav.toc a{border-left:0;border-bottom:2px solid transparent}
  nav.toc a[aria-current=true]{border-left:0;border-bottom-color:var(--gru-accent)}
}

/* ---------- print ---------- */
@media print{
  /* Everything must be visible on paper. The scroll-reveal only ever reveals what is in the
     viewport, and a printer has no viewport — without this the PDF came out as 107 blank
     pages, which is exactly how a silent CSS failure looks. */
  .js-anim .reveal,.reveal{opacity:1!important;transform:none!important;transition:none!important}
  .lift,.tilt,.hero .hb,.hero h1,.hero .meta{transform:none!important}
  .scene{perspective:none}
  .tw{overflow:visible!important}
  header.top,nav.toc,.ctl,a.dl,.skip,.dlp{display:none!important}
  body{background:#fff;color:#000;font-size:10.5pt}
 .wrap{display:block;max-width:none;padding:0}
  section.ch{break-before:page;margin-bottom:1.5rem}
  section.ch:first-of-type{break-before:avoid}
 .hero{background:#1A1753!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 .sigcard,.sw,.combo,.badart,.tv,.rsw,.ccbar i,.gradbar,.buildart.tile{
   -webkit-print-color-adjust:exact;print-color-adjust:exact}
  details{border:0}details>*:not(summary){padding:0}
  details:not([open])>*:not(summary){display:revert}
  a{text-decoration:none;color:#000}
  a[href^="http"]::after{content:" (" attr(href) ")";font-size:8pt;color:#444}
  table,figure,.buildcard,.lockcard{break-inside:avoid}
  h2,h3,h4{break-after:avoid}
}
"""
CSS += r"""
/* ============================================================================
   FORCED COLOURS — Windows High Contrast and similar.
   The operating system replaces every colour with its own, which is correct for text and
   catastrophic for a page whose subject IS colour: every swatch, ramp step, chart bar and
   gradient would collapse into one flat system colour and the Colour chapter would become
   a list of hex codes with no colours beside them. These elements, and only these, opt out.
   ============================================================================ */
@media (forced-colors: active){
  .sw,.chip,.sigcard,.gradbar,.combo,.badart,.tv,.rsw,.ccbar i,.buildart.tile{
    forced-color-adjust:none}
}

/* ============================================================================
   THE RULE BOX — used where a decision needs its reasoning beside it, not in a
   footnote. It is a card, so it reads as a statement rather than as body text.
   ============================================================================ */
.rulebox{background:var(--gru-brand-quiet);border:1px solid var(--gru-border-strong);
  border-left:4px solid var(--gru-accent);border-radius:var(--gru-radius-lg,14px);
  padding:clamp(1.1rem,3vw,1.9rem);margin:1.8rem 0}
.rulebox .rb-h{margin:0 0 .6rem;font-size:var(--gru-size-xl,1.5rem)}
.rulebox p{margin:.6rem 0}
.rulebox p:last-child{margin-bottom:0}

.twoup{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr));
  gap:1rem;margin-top:1.2rem}
.tv{border-radius:var(--gru-radius-md,10px);padding:1.1rem 1.2rem;
  border:1px solid var(--gru-border-strong)}
.tv-l{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;opacity:.82}
.tv-h{font-size:clamp(1.5rem,4vw,2.1rem);font-family:var(--gru-font-display);
  font-weight:700;line-height:1.15;margin:.25rem 0 .15rem}
.tv-r{font-size:.82rem;opacity:.9}

/* ============================================================================
   ROLE TOKENS — the light value and the dark value of every role, side by side,
   so a reader can see at a glance that both themes are actually complete.
   ============================================================================ */
.roles{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr));
  gap:1rem;margin:1.2rem 0}
.rolegrp{border:1px solid var(--gru-border);border-radius:var(--gru-radius-md,10px);
  padding:.9rem 1rem;background:var(--gru-surface-raised)}
.rolegrp-n{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--gru-ink-subtle);margin-bottom:.55rem}
.role{display:grid;grid-template-columns:1fr auto auto auto auto;align-items:center;
  gap:.4rem;padding:.22rem 0;border-top:1px solid var(--gru-border)}
.role:first-of-type{border-top:0}
.role code{font-size:.78em;overflow-wrap:anywhere}
.rsw{width:1.05rem;height:1.05rem;border-radius:4px;display:inline-block;
  border:1px solid var(--gru-border-strong);flex:none}
.rv{font-size:.68rem;color:var(--gru-ink-subtle);min-width:5.2em;text-align:right}
@container (max-width:34rem){ .role .rv{display:none} }

/* ============================================================================
   CHART SEQUENCE — shown as bars rather than as swatches, because a data colour
   is only honest when you can see it at the size data is actually drawn.
   ============================================================================ */
.charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,17rem),1fr));
  gap:1rem;margin:1.2rem 0}
.chartcard{border-radius:var(--gru-radius-md,10px);padding:1rem 1.1rem}
.cc-h{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;opacity:.8;
  margin-bottom:.9rem}
.ccbars{display:flex;align-items:flex-end;gap:.55rem;min-height:8.5rem}
.ccbar{display:flex;flex-direction:column;align-items:center;gap:.3rem;flex:1;
  justify-content:flex-end}
.ccbar i{display:block;width:100%;border-radius:4px 4px 0 0}
.ccbar span{font-size:.6rem;text-align:center;line-height:1.2;overflow-wrap:anywhere}
.cc-r{opacity:.7}

/* ============================================================================
   WIDE TABLES — a table with five columns cannot reflow on a 360px phone, so it
   scrolls sideways inside its own box instead of forcing the whole page to.
   ============================================================================ */
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:1rem 0;
  border-radius:var(--gru-radius-md,10px)}
.tw table{margin:0;min-width:28rem}
.tw:focus-visible{outline:2px solid var(--gru-focus);outline-offset:2px}
.tw table.assets{min-width:22rem}

/* ============================================================================
   FLUID SCALE — one root size that tracks the viewport, so every rem-based
   value in the kit scales together. 320px phone to 2560px display, no jumps and
   no per-breakpoint overrides. The clamp floor is 15px, never smaller, and the
   ceiling stops the type ballooning on a television.
   ============================================================================ */
html{font-size:clamp(15px, 0.92rem + 0.22vw, 19px)}
@media (min-width:120rem){html{font-size:20px}}

/* Every surface uses a role token, so light and dark are complete by
   construction rather than by patching. The only literal colours anywhere below
   are inside the two theme blocks in tokens.css. */

/* ============================================================================
   DEPTH — a restrained 3D. Cards lift towards the reader on hover and sections
   arrive with a slight rotation on the X axis, which reads as paper turning
   rather than as a slideshow. Perspective is set once, on a wrapper, so the
   whole page shares one vanishing point instead of each card having its own.
   ============================================================================ */
.scene{perspective:1400px;perspective-origin:50% 30%;transform-style:preserve-3d}

.lift{transition:transform var(--gru-duration-base) var(--gru-ease-out),
                 box-shadow var(--gru-duration-base) var(--gru-ease-out),
                 border-color var(--gru-duration-fast) var(--gru-ease-out)}
.lift:hover,.lift:focus-within{
  transform:translate3d(0,-4px,22px) rotateX(1.4deg);
  box-shadow:var(--gru-shadow-3);
  border-color:var(--gru-border-strong)}

/* Section arrival. Driven by IntersectionObserver adding .in, so nothing depends
   on scroll position maths and nothing animates twice. */
/* CRITICAL: the hidden state is scoped to html.js-anim, a class only JavaScript can add.
   Written the obvious way — .reveal{opacity:0} — the whole guidebook is invisible to anyone
   whose JavaScript is blocked or has not run yet. Content must never need a script to appear. */
.js-anim .reveal{opacity:0;transform:translate3d(0,26px,-40px) rotateX(4deg);
  transition:opacity 620ms var(--gru-ease-out),transform 720ms var(--gru-ease-out)}
.js-anim .reveal.in{opacity:1;transform:none}
.reveal.d1{transition-delay:70ms}.reveal.d2{transition-delay:140ms}
.reveal.d3{transition-delay:210ms}

/* The hero gets a gentle parallax on its own layers, set from JS as a custom
   property so the browser only ever composites transforms. */
.hero{transform-style:preserve-3d}
.hero .hb{transform:translate3d(0,calc(var(--par,0)*-16px),60px)}
.hero h1{transform:translate3d(0,calc(var(--par,0)*-8px),30px)}
.hero .meta{transform:translateZ(14px)}

/* Swatches and build cards tilt very slightly towards the pointer. 3deg is the
   most that still looks deliberate; beyond that it reads as a gimmick. */
.tilt{transition:transform 160ms var(--gru-ease-out)}
.tilt:hover{transform:perspective(700px) rotateX(calc(var(--ty,0)*-3deg))
  rotateY(calc(var(--tx,0)*3deg)) translateZ(10px)}

/* ============================================================================
   REDUCED MOTION — the whole of the above is decoration. Anyone who has asked
   their system for less motion gets the finished page immediately, with every
   element in its final position. This is not a lesser version; it is the
   destination without the journey.
   ============================================================================ */
@media (prefers-reduced-motion:reduce){
  .js-anim .reveal{opacity:1!important;transform:none!important;transition:none!important}
  .lift,.tilt{transition:none!important}
  .lift:hover,.lift:focus-within,.tilt:hover{transform:none!important}
  .hero .hb,.hero h1,.hero .meta{transform:none!important}
  .scene{perspective:none}
}
/* Some people have reduced transparency or high contrast switched on; honour both. */
@media (prefers-contrast:more){
  .hero::before,.hero::after{display:none}
  a.dl{outline:2px solid currentColor;outline-offset:1px}
  th,td{border-bottom-color:var(--gru-ink-subtle)}
}

/* ============================================================================
   RESPONSIVE — container queries so a component reacts to the space it is in,
   not to the size of the window. That is what makes the same card work in the
   sidebar of a desktop and full-width on a phone.
   ============================================================================ */
main{container-type:inline-size}
@container (max-width:46rem){
  .sigrow,.buildrow,.lockrow,.combos,.twocol,.typecmp{grid-template-columns:1fr}
  .scalerow{grid-template-columns:1fr;gap:.2rem}
  .scalelab{text-align:left}
  .ramp{flex-wrap:wrap}.sw{min-width:22%;height:58px}
  table.assets td:first-child{word-break:break-all}
}
@container (max-width:30rem){
  .ramp .sw span{display:none}
  .hero{padding:1.5rem}
}

/* The header is OUTSIDE main, so a container query on main cannot reach it — it needs real
   media queries. Its controls plus the tagline chip are ~460px of content, more than a phone
   has, so the chip goes (the hero carries the tagline) and the buttons shorten. */
@media (max-width:52rem){ .top-in{gap:.6rem} .vtag.taglock{display:none} }
@media (max-width:34rem){
  .top-in{padding:.55rem .8rem}
  .brandmark svg{height:24px}
  button.b{padding:.38rem .6rem;font-size:.72rem}
  .ctl{gap:.3rem}
  button.b .full{display:none}
}
@media (max-width:22rem){ .brandmark{max-width:38%} button.b{padding:.34rem .5rem} }
/* Tables are the one thing that genuinely cannot reflow; let them scroll rather
   than letting them break the page width. */


/* Long words and code strings must never widen the page on a phone. */
p,li,td,th,summary{overflow-wrap:break-word}
code{overflow-wrap:anywhere}

.num{text-align:right;white-space:nowrap}
.assetgrp{background:var(--gru-bg-subtle)}
.assetgrp>table{margin-top:0}
.wholekit{margin:1rem 0 1.6rem}
.wholekit a.dl{font-size:.82rem;padding:.6rem 1.2rem}
.dlp{font-size:.68rem;color:var(--gru-ink-subtle)}
.taglock{font-family:var(--gru-font-display);font-weight:600;color:var(--gru-accent);
  font-size:.82rem;letter-spacing:-.01em}
"""

JS = r"""
(function(){
  var root=document.documentElement, body=document.body;
  /* ---- theme: auto -> light -> dark, remembered only in memory (no storage APIs) ---- */
  var themes=['auto','light','dark'], ti=0, tb=document.getElementById('theme');
  function paintTheme(){
    var t=themes[ti];
    if(t==='auto'){root.removeAttribute('data-theme')}else{root.setAttribute('data-theme',t)}
    tb.innerHTML = '<span class="full">Theme: </span>' +
      (t==='auto' ? 'auto' : (t==='light' ? 'light' : 'dark'));
    tb.setAttribute('aria-label','Colour theme, currently '+t+'. Activate to change.');
  }
  tb.addEventListener('click',function(){ti=(ti+1)%3;paintTheme()});
  paintTheme();

  /* ---- language: both -> English only ---- */
  var lb=document.getElementById('lang'), bnOff=false;
  lb.addEventListener('click',function(){
    bnOff=!bnOff; body.classList.toggle('no-bn',bnOff);
    lb.setAttribute('aria-pressed',String(bnOff));
    lb.innerHTML = bnOff ? 'EN<span class="full"> only</span>'
                         : 'EN<span class="full"> + </span><span lang="bn">বাং</span>';
  });

  /* ---- which chapter am I in ---- */
  var links=[].slice.call(document.querySelectorAll('nav.toc a'));
  var secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))})
 .filter(Boolean);
  function current(){
    var y=window.scrollY+120, best=0;
    secs.forEach(function(s,i){ if(s.offsetTop<=y) best=i });
    links.forEach(function(a,i){
      if(i===best){a.setAttribute('aria-current','true')}else{a.removeAttribute('aria-current')}
    });
  }
  var raf=null;
  window.addEventListener('scroll',function(){
    if(raf) return; raf=requestAnimationFrame(function(){raf=null;current()});
  },{passive:true});
  current();


  /* ---- section arrival, once each, and never when motion is reduced ---- */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  function arm(){
    var els = [].slice.call(document.querySelectorAll('.reveal'));
    if (reduce.matches || !('IntersectionObserver' in window)) {
      els.forEach(function(e){ e.classList.add('in') }); return;
    }
    // Only now is it safe to hide anything: the observer that will reveal it exists.
    document.documentElement.classList.add('js-anim');
    els.forEach(function(e){
      var b = e.getBoundingClientRect();
      if (b.top < window.innerHeight * 0.94) e.classList.add('in');
    });
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if (en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target) }
      });
    }, {rootMargin:'0px 0px -12% 0px', threshold:0.04});
    els.forEach(function(e){ io.observe(e) });
    /* Last resort. If the observer never fires for an element — a very tall section whose top
       is already above the viewport, a browser quirk, a stalled frame — the content would stay
       invisible for ever. After three seconds, everything is shown regardless. Content must
       never depend on an animation succeeding. */
    setTimeout(function(){
      els.forEach(function(e){ e.classList.add('in') });
    }, 3000);
  }
  arm();
  reduce.addEventListener('change', function(){
    document.querySelectorAll('.reveal').forEach(function(e){ e.classList.add('in') });
  });

  /* ---- hero parallax, composited only, and skipped entirely when reduced ---- */
  var hero = document.querySelector('.hero');
  if (hero && !reduce.matches){
    var pending = false;
    window.addEventListener('scroll', function(){
      if (pending) return; pending = true;
      requestAnimationFrame(function(){
        pending = false;
        var r = hero.getBoundingClientRect();
        var t = Math.min(1, Math.max(-1, -r.top / Math.max(1, r.height)));
        hero.style.setProperty('--par', t.toFixed(3));
      });
    }, {passive:true});
  }

  /* ---- pointer tilt on cards. Pointer only: a touch should never tilt ---- */
  if (!reduce.matches && window.matchMedia('(hover:hover)').matches){
    document.querySelectorAll('.tilt').forEach(function(el){
      el.addEventListener('pointermove', function(ev){
        var b = el.getBoundingClientRect();
        el.style.setProperty('--tx', (((ev.clientX-b.left)/b.width)*2-1).toFixed(3));
        el.style.setProperty('--ty', (((ev.clientY-b.top)/b.height)*2-1).toFixed(3));
      });
      el.addEventListener('pointerleave', function(){
        el.style.setProperty('--tx',0); el.style.setProperty('--ty',0);
      });
    });
  }

  /* ---- tables: give a scroll box a tab stop, but only when it actually scrolls ----
     The box itself is added at build time. What cannot be decided at build time is whether
     a given table overflows at THIS window width, so that part happens here.

     Two rules. A scroll container that cannot be focused cannot be scrolled from the
     keyboard, so the far side of a wide table would be unreachable without a mouse — hence
     the tab stop. But a tab stop on a table that fits is pure noise in the tab order, so
     tables that fit do not get one, and the state is re-evaluated when the window resizes.

     The accessible name is taken from the nearest heading above the table. A hundred
     regions all called "Table" tells a screen-reader user nothing about which one they have
     landed in. */
  function labelFor(box){
    var n = box, h = null;
    while (n && !h) {
      var q = n.previousElementSibling;
      while (q && !h) { if (/^H[2-6]$/.test(q.tagName)) h = q; q = q.previousElementSibling; }
      n = n.parentElement;
    }
    return (h ? h.textContent.trim() : 'Data') + ' — table, scrolls sideways';
  }
  var boxes = [].slice.call(document.querySelectorAll('main .tw'));
  /* anything the build missed still gets a box, so nothing can widen the page */
  [].forEach.call(document.querySelectorAll('main table'), function(t){
    if (t.parentElement && t.parentElement.classList.contains('tw')) return;
    var w = document.createElement('div'); w.className = 'tw';
    t.parentNode.insertBefore(w, t); w.appendChild(t); boxes.push(w);
  });
  function syncTables(){
    boxes.forEach(function(w){
      if (w.scrollWidth > w.clientWidth + 1) {
        if (!w.hasAttribute('role')) {
          w.tabIndex = 0;
          w.setAttribute('role', 'region');
          w.setAttribute('aria-label', labelFor(w));
        }
      } else if (w.hasAttribute('role')) {
        w.removeAttribute('role'); w.removeAttribute('aria-label'); w.removeAttribute('tabindex');
      }
    });
  }
  requestAnimationFrame(syncTables);
  var tblT; window.addEventListener('resize', function(){
    clearTimeout(tblT); tblT = setTimeout(syncTables, 150);
  });

  /* ---- print: open every <details> so nothing is lost in the PDF ---- */
  var opened=[];
  window.addEventListener('beforeprint',function(){
    opened=[];
    [].forEach.call(document.querySelectorAll('details:not([open])'),function(d){
      opened.push(d); d.open=true;
    });
  });
  window.addEventListener('afterprint',function(){
    opened.forEach(function(d){d.open=false}); opened=[];
  });
})();
"""


def build():
    toc, chunks = [], []
    for i, (slug, title, bn, fn) in enumerate(CHAPTERS, 1):
        toc.append(f'<li><a href="#{slug}">{title}</a></li>')
        body = wrap_tables(fn()) if fn else '<div class="pending"><b>Not yet written.</b></div>'
        chunks.append(
            f'<section class="ch reveal" id="{slug}" aria-labelledby="{slug}-h">'
            f'<div class="chnum">Chapter {i:02d}</div>'
            f'<h2 id="{slug}-h">{title}</h2>'
            f'<div class="h2bn" lang="bn">{bn}</div>{body}</section>')

    hero_bird = svg_inline("GRU953-bird.svg", "hb")   # still, always
    head_lock = svg_inline("GRU953-lockup-horizontal.svg")
    foot_lock = svg_inline("GRU953-lockup-horizontal.svg")

    # typography.css declares its @font-face rules with RELATIVE urls, for the stylesheet's
    # own life outside this book. Inlined here they would point at files that are not beside
    # the HTML, so the browser fires two failed requests on every load. FONTS_CSS already
    # supplies the same faces with the font data embedded, so the relative ones are removed.
    TYPO_CSS = re.sub(r"@font-face\s*\{[^}]*\}", "", (A / "typography.css").read_text())

    doc = f"""<!doctype html>
<!-- gru953-review: colours-are-the-subject -->
<!-- This book prints the palette's own hex values, on purpose. The marker above tells the
     brand checker to stand down on hard-coded colours for this one file; every measured
     contrast and accessibility check still applies. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GRU953 Brand Guidebook · {TAGLINE_EN}</title>
<meta name="description" content="The GRU953 brand guidebook: purpose, voice, the Soaring Bird,
 the Meridian and Daybreak palette, typography, design rules, applications and licence.
 {TAGLINE_EN} · {TAGLINE_BN} · {DATE}.">
<meta name="author" content="Aninda Sundar Howlader (GRU953)">
<meta name="theme-color" content="#1A1753">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{b64(ROOT / '06_assets/favicon/favicon.ico', 'image/x-icon')}">
<style>{FONTS_CSS}</style>
<style>{(A / 'tokens.css').read_text()}</style>
<style>{TYPO_CSS}</style>
<style>{(A / 'layout.css').read_text()}</style>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to the guidebook</a>
<header class="top">
  <div class="top-in">
    <a class="brandmark" href="#top" aria-label="GRU953 brand guidebook, back to top">{head_lock}</a>
    <span class="vtag taglock">{TAGLINE_EN}</span>
    <span class="spacer"></span>
    <div class="ctl">
      <button class="b" id="lang" type="button" aria-pressed="false">EN<span class="full"> + </span><span lang="bn">বাং</span></button>
      <button class="b" id="theme" type="button">Theme: auto</button>
      <button class="b" type="button" onclick="window.print()">Print<span class="full"> / PDF</span></button>
    </div>
  </div>
</header>

<div class="wrap scene" id="top">
  <nav class="toc" aria-label="Contents">
    <div class="toc-h">Contents · সূচি</div>
    <ol>{''.join(toc)}</ol>
  </nav>

  <main id="main">
    <div class="hero">
      {hero_bird}
      <h1>GRU953<br>Brand Guidebook</h1>
      <p class="sub">Simple technology. For everyone.</p>
      <p class="subbn" lang="bn">সহজ প্রযুক্তি। সবার জন্য।</p>
      <div class="meta">
        <span>{DATE}</span>
        <span>Marks reserved · System Apache-2.0 · Book PolyForm Noncommercial</span>
        <span>Aninda Sundar Howlader</span>
      </div>
    </div>
    {''.join(chunks)}
    <footer class="f">
      {foot_lock}
      <p class="taglock">{TAGLINE_EN} &nbsp;·&nbsp; <span lang="bn">{TAGLINE_BN}</span></p>
      <p>GRU953 Brand Guidebook, {DATE}.<br>
      Copyright 2026 Aninda Sundar Howlader (GRU953).</p>
      <p>Licensed under the <b>Apache License, Version 2.0</b>. The <b>GRU953 marks</b> — the
      Soaring Bird, the wordmark and any lockup — are <b>not licensed</b>; see the licence
      chapter. The bundled typefaces keep their own SIL Open Font Licence 1.1 terms.</p>
      <p>Built offline: every font, logo, image and token in this file is embedded. Nothing here
      needs a server.</p>
    </footer>
  </main>
</div>
<script>{JS}</script>
</body>
</html>"""
    out = GB / ("GRU953-Brand-Guidebook-print.html" if PRINT_MODE
                else "GRU953-Brand-Guidebook.html")
    out.write_text(doc, encoding="utf-8")
    kb = out.stat().st_size / 1024
    print(f"{out.name}  {kb:,.0f} kB  ({len(CHAPTERS)} chapters)")
    return out


if __name__ == "__main__":
    import sys
    if "--print" in sys.argv:
        globals()["PRINT_MODE"] = True
    build()
