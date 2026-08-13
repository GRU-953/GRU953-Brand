#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""GRU953 — build the Claude Design project.

Every preview in this project is GENERATED from one place: the component CSS in
src/components.css, the tokens in tokens/, and the markup below. Nothing is
hand-maintained twice, so no card can drift out of step with the stylesheet it is
supposed to be demonstrating.

Each preview is fully self-contained — the tokens and the component CSS are
inlined — so a card renders correctly on its own, with no build step and no
network.

Every card's first line carries the `@dsCard` marker that Claude Design reads to
build its index.

    python3 build.py            # write every preview
    python3 build.py --check    # verify, write nothing
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
SRC, TOK = HERE / "src", HERE / "tokens"

def _css() -> str:
    """The four stylesheets, concatenated, with the font paths corrected.

    typography.css declares its @font-face rules with a path relative to itself
    (`fonts/…`), which is right when it is loaded as a stylesheet from tokens/. Inlined
    into a preview one directory down, that path resolves to nothing and the browser
    fires a failed request for every face on every load. Every preview in this project
    sits exactly one level deep, so `../tokens/fonts/…` is correct from all of them.
    """
    parts = []
    for f in ("tokens.css", "typography.css", "layout.css"):
        t = (TOK / f).read_text(encoding="utf-8")
        if f == "typography.css":
            t = t.replace('url("fonts/', 'url("../tokens/fonts/')
        parts.append(t)
    parts.append((SRC / "components.css").read_text(encoding="utf-8"))
    return "\n".join(parts)


CSS = _css()

TAG_EN = "Simple technology. For everyone."
TAG_BN = "সহজ প্রযুক্তি। সবার জন্য।"
TOKENS = json.loads((TOK / "tokens.json").read_text(encoding="utf-8"))


_MARK_N = {"n": 0}


def mark(name: str, cls: str = "gru-mark") -> str:
    """Inline a mark, with unique ids and an honest accessible name.

    Two things here are not cosmetic.

    The width/height strip is anchored to the ROOT element. A bare
    `re.sub(r'\s(width|height)="[^"]*"', "", s, count=2)` removes the first two it finds
    anywhere, so an SVG whose root carries neither would have had them stripped off its
    first child instead — a rect sized 10x10 becomes a rect sized nothing. It happened to
    work only because every mark here puts both on the root.

    And the `<desc>` is moved out of the accessible NAME. Every mark shipped
    `aria-labelledby="t d"`, which points at the title AND the long design note, so the
    computed name of the logo inside a top bar became "GRU953 Soaring Bird The GRU953
    Soaring Bird: a climbing bird drawn in fine lines... Ledger" — authoring notes read
    aloud on every page. The title names it; the desc describes it.
    """
    s = (SRC / "marks" / f"{name}.svg").read_text(encoding="utf-8")
    open_tag = re.match(r"<svg\b[^>]*>", s)
    if not open_tag:
        raise SystemExit(f"{name}.svg does not start with an <svg> element")
    head = re.sub(r'\s(?:width|height)="[^"]*"', "", open_tag.group(0))
    s = head + s[open_tag.end():]
    # Unique per INSTANCE, not per mark name: the same mark is inlined more than once on
    # several cards, and two elements sharing an id make every ARIA reference on the page
    # resolve to whichever came first.
    _MARK_N["n"] += 1
    uniq = f"{name}-{_MARK_N['n']}"
    for i in ("t", "d", "at", "ad", "lt", "ld"):
        s = s.replace(f'id="{i}"', f'id="{uniq}-{i}"')
        s = re.sub(rf'aria-labelledby="([^"]*)\b{i}\b', rf'aria-labelledby="\1{uniq}-{i}', s)
    # -t/-d for the bird, -at/-ad for the tile, -lt/-ld for a lockup. Matching only the
    # first pair left every lockup and the app icon with the long design note still inside
    # their accessible NAME — measured at 311 characters on the horizontal lockup.
    s = re.sub(r'aria-labelledby="([\w-]+-(?:t|at|lt)) ([\w-]+-(?:d|ad|ld))"',
               r'aria-labelledby="\1" aria-describedby="\2"', s)
    return s.replace("<svg ", f'<svg class="{cls}" ', 1)


def reid(html: str, suffix: str) -> str:
    """Suffix every id in a fragment, and every reference to one.

    The dual-theme shell renders the SAME markup twice in one document. Without this,
    `id="dt"` exists twice and `aria-labelledby="dt"` in the dark panel resolves to the
    light panel's heading — as does every `for=`, every `aria-controls`, every `href="#…"`.
    """
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    if not ids:
        return html
    out = re.sub(r'(\sid=")([^"]+)(")',
                 lambda m: f'{m.group(1)}{m.group(2)}{suffix}{m.group(3)}', html)

    def _refs(m):
        attr, val = m.group(1), m.group(2)
        parts = [f"{v}{suffix}" if v in ids else v for v in val.split()]
        return f'{attr}="{" ".join(parts)}"'

    out = re.sub(r'\b(for|aria-labelledby|aria-describedby|aria-controls|aria-owns'
                 r'|aria-activedescendant)="([^"]*)"', _refs, out)
    out = re.sub(r'href="#([^"]+)"',
                 lambda m: f'href="#{m.group(1)}{suffix}"' if m.group(1) in ids
                 else m.group(0), out)
    return out


# ---------------------------------------------------------------- the preview shell
SHELL = """<!-- @dsCard group="{group}" -->{optout}
<!doctype html>
<html lang="en"{theme}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GRU953 — {name}</title>
<meta name="description" content="{subtitle} · GRU953 design system · {tag_bn} · {tag_en}">
<style>{css}</style>
<style>
/* preview chrome — not part of the design system */
html,body{{margin:0;background:var(--gru-bg)}}
.dsp{{padding:var(--gru-space-6) var(--gru-page-padding);display:grid;gap:var(--gru-space-6)}}
.dsp__head{{display:flex;align-items:baseline;gap:var(--gru-space-4);flex-wrap:wrap;
  border-bottom:1px solid var(--gru-border);padding-bottom:var(--gru-space-4)}}
.dsp__name{{font-family:var(--gru-font-display);font-weight:700;
  font-size:var(--gru-text-xl);letter-spacing:var(--gru-tracking-display);margin:0}}
.dsp__sub{{color:var(--gru-ink-subtle);font-size:var(--gru-text-sm)}}
.dsp__spacer{{flex:1}}
.dsp__themes{{display:grid;gap:var(--gru-space-5);
  grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr))}}
.dsp__panel{{border:1px solid var(--gru-border-strong);border-radius:var(--gru-radius-md);
  overflow:hidden}}
.dsp__label{{font-family:var(--gru-font-mono);font-size:var(--gru-text-2xs);
  letter-spacing:var(--gru-tracking-caps);text-transform:uppercase;
  padding:var(--gru-space-2) var(--gru-space-4);border-bottom:1px solid var(--gru-border)}}
.dsp__stage{{padding:var(--gru-space-5)}}
.dsp__notes{{font-size:var(--gru-text-sm);color:var(--gru-ink-muted);max-width:var(--gru-measure)}}
.dsp__notes code{{background:var(--gru-bg-subtle);padding:.1em .35em;border-radius:4px}}
</style>
</head>
<body class="gru">
<main class="dsp">
  <header class="dsp__head">
    <h1 class="dsp__name">{name}</h1>
    <span class="dsp__sub">{subtitle}</span>
    <span class="dsp__spacer"></span>
    <span class="gru-eyebrow">GRU953</span>
  </header>
{body}
{notes}
</main>
</body>
</html>
"""

DUAL = """  <div class="dsp__themes">
    <section class="dsp__panel gru" data-theme="light" aria-label="Light theme">
      <div class="dsp__label">light theme</div>
      <div class="dsp__stage">{light}</div>
    </section>
    <section class="dsp__panel gru" data-theme="dark" aria-label="Dark theme">
      <div class="dsp__label">dark theme</div>
      <div class="dsp__stage">{dark}</div>
    </section>
  </div>
"""

CARDS: list[dict] = []


def card(folder: str, slug: str, group: str, name: str, subtitle: str,
         stage: str = "", full: str = "", notes: str = "",
         width: int = 900, height: int = 620, theme: str | None = "light",
         allow_literals: bool = False) -> None:
    """One preview. `stage` is shown in both themes side by side; `full` is shown once.

    `theme=None` emits no `data-theme` attribute at all, which is the third state a real
    product ships with and the one most often left untested. An empty string is NOT the
    same thing: `data-theme=""` matches neither theme block and silently inherits.
    """
    body = DUAL.format(light=reid(stage, "-l"), dark=reid(stage, "-d")) if stage else full
    note_html = f'  <p class="dsp__notes">{notes}</p>' if notes else ""
    # A card whose SUBJECT is colour has to print colour values. It says so, in a marker
    # the review checker reads, rather than the checker having a hard-coded exception list.
    optout = ("\n<!-- gru953-review: colours-are-the-subject -->" if allow_literals else "")
    html = SHELL.format(group=group, name=name, subtitle=subtitle, css=CSS,
                        body=body, notes=note_html, tag_en=TAG_EN, tag_bn=TAG_BN,
                        theme=f' data-theme="{theme}"' if theme else "", optout=optout)
    CARDS.append(dict(path=f"{folder}/{slug}.html", name=name, subtitle=subtitle,
                      group=group, html=html, width=width, height=height,
                      allow_literals=allow_literals))


# ============================================================ FOUNDATIONS
def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def contrast(a: str, b: str) -> float:
    def lum(h: str) -> float:
        h = h.lstrip("#")
        r, g, bl = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(bl)
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def label_on(bg: str) -> str:
    """Ink or paper, whichever is legible ON this swatch — MEASURED, not guessed.

    Choosing by step number looked right and was wrong: the green family's step 500 is
    light enough that white on it measures 2.85:1, so the label on the one card in the
    project whose whole subject is legibility was itself illegible.
    """
    ink, paper = TOKENS["ground"]["ink"], TOKENS["ground"]["paper"]
    return ink if contrast(ink, bg) >= contrast(paper, bg) else paper


def ramp(family: str) -> str:
    fam = TOKENS["families"][family]
    steps = sorted(fam["ramp"], key=int)
    cells = "".join(
        f'<div class="gru-swatch" style="background:{fam["ramp"][s]};'
        f'color:{label_on(fam["ramp"][s])}">'
        f'<b>{s}</b><span class="gru-mono">{fam["ramp"][s]}</span></div>' for s in steps)
    return (f'<div class="gru-eyebrow">{fam["label"]} · --gru-{family}-*</div>'
            f'<div class="ramprow">{cells}</div>')


RAMP_CSS = """
<style>
.ramprow{display:grid;grid-template-columns:repeat(auto-fit,minmax(4.6rem,1fr));
  border-radius:var(--gru-radius-sm);overflow:hidden;
  border:1px solid var(--gru-border);margin:var(--gru-space-2) 0 var(--gru-space-5)}
.gru-swatch{min-width:0;height:72px;display:flex;flex-direction:column;
  justify-content:flex-end;padding:6px 5px;font-size:.6rem;line-height:1.2}
.gru-swatch b{font-family:var(--gru-font-mono);font-size:.64rem}
.gru-swatch span{font-size:.56rem}
.twoval{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr));
  gap:var(--gru-space-4);margin:var(--gru-space-4) 0}
.tv{border:1px solid var(--gru-border-strong);border-radius:var(--gru-radius-md);
  padding:var(--gru-space-4)}
.tv b{display:block;font-family:var(--gru-font-display);font-size:var(--gru-text-2xl);
  line-height:1.1;margin:.2em 0 .1em}
/* This panel pins its own ground, so it must pin its own foregrounds too. The eyebrow and
   the ratio line inherited theme colours while sitting on a fixed ground, and measured
   4.01:1 in the dark preview and 3.08:1 in the light one — on the card about contrast. */
.tv--paper{color:var(--gru-ground-ink)}
.tv--ink{color:var(--gru-ground-paper)}
.tv--paper .gru-eyebrow,.tv--paper .gru-mono{color:var(--gru-meridian-800)}
.tv--ink .gru-eyebrow,.tv--ink .gru-mono{color:var(--gru-meridian-200)}
.rolerow{display:grid;grid-template-columns:1fr auto auto auto auto;align-items:center;
  gap:var(--gru-space-2);padding:.25rem 0;border-top:1px solid var(--gru-border);
  font-size:var(--gru-text-xs)}
.rolerow:first-of-type{border-top:0}
.rsw{width:18px;height:18px;border-radius:4px;border:1px solid var(--gru-border-strong)}
.rv{font-family:var(--gru-font-mono);font-size:.66rem;color:var(--gru-ink-subtle);
  min-width:5.2em;text-align:right}
</style>
"""

ACC = TOKENS["accent"]
TH = TOKENS["thresholds"]

card("foundations", "colour", "Foundations", "Colour",
     "Three signature colours, two functional, two grounds — and one signature with two values",
     full=RAMP_CSS + f"""
  <div class="gru-prose">
    <h2>The rule that shapes the palette</h2>
    <p>Contrast is a ratio between two luminances. To clear 4.5:1 against white a
    colour must be darker than luminance <b>{TH['max_luminance_on_paper']}</b>; to clear
    4.5:1 against the Ink it must be lighter than <b>{TH['min_luminance_on_ink']}</b>.
    Both cannot be true, so <b>no single colour can be this brand's text colour in
    both themes</b> — that is arithmetic, not taste.</p>
    <p>So the signature is <b>one hue with two calibrated values</b>. Use
    <code>--gru-accent</code> and let the theme choose. They sit
    {ACC['hue_drift_degrees']}° apart in hue, which is one colour family, and
    ΔE&nbsp;{ACC['delta_e_between_values']} apart in appearance, which is plainly
    different side by side. This project publishes both numbers rather than only
    the flattering one.</p>
  </div>
  <div class="twoval">
    <div class="tv tv--paper" style="background:var(--gru-ground-paper)">
      <span class="gru-eyebrow">light theme</span>
      <b style="color:{ACC['light']}">{ACC['light']}</b>
      <span class="gru-mono">{ACC['light_ratio_on_paper']}:1 on paper</span></div>
    <div class="tv tv--ink" style="background:var(--gru-ground-ink)">
      <span class="gru-eyebrow">dark theme</span>
      <b style="color:{ACC['dark']}">{ACC['dark']}</b>
      <span class="gru-mono">{ACC['dark_ratio_on_ink']}:1 on ink</span></div>
  </div>
  <h2>The ramps</h2>
  {"".join(ramp(f) for f in ("meridian", "daybreak", "ember", "success", "danger"))}
  <h2>Every role, in both themes</h2>
  <p class="dsp__notes">Left swatch is the light theme, right the dark. Reach for a
  role, never a raw ramp step — a role is defined in both themes, so one stylesheet
  covers each.</p>
  <div class="gru-grid">
""" + "".join(
    f'<div class="gru-card"><div class="gru-card__meta">{gname}</div>' + "".join(
        f'<div class="rolerow"><code>--gru-{k}</code>'
        f'<span class="rsw" style="background:{TOKENS["roles"]["light"][k]}"></span>'
        f'<span class="rv">{TOKENS["roles"]["light"][k]}</span>'
        f'<span class="rsw" style="background:{TOKENS["roles"]["dark"][k]}"></span>'
        f'<span class="rv">{TOKENS["roles"]["dark"][k]}</span></div>' for k in keys)
    + "</div>"
    for gname, keys in [
        ("Surfaces", ["bg", "bg-subtle", "surface", "surface-raised", "surface-sunken"]),
        ("Text", ["ink", "ink-muted", "ink-subtle", "ink-inverse"]),
        ("Lines", ["border", "border-strong"]),
        ("Brand", ["brand", "brand-hover", "brand-active", "brand-quiet", "on-brand"]),
        ("Signature", ["accent", "accent-hover", "accent-active", "accent-quiet",
                       "accent-ui", "on-accent"]),
        ("Links", ["link", "link-hover", "link-visited"]),
        ("Focus and disabled", ["focus", "disabled-bg", "disabled-ink", "disabled-border"]),
        ("Meaning", ["info", "info-quiet", "info-border", "success", "success-quiet",
                     "success-border", "warning", "warning-quiet", "warning-border",
                     "danger", "danger-quiet", "danger-border"]),
    ]) + "</div>",
     height=1500, allow_literals=True)

TYPE_ROWS = [("4xl", "Hero"), ("3xl", "h1"), ("2xl", "h2"), ("xl", "h3"), ("lg", "h4"),
             ("md", "Lead"), ("base", "Body"), ("sm", "Small"), ("xs", "Caption"),
             ("2xs", "Label")]
card("foundations", "typography", "Foundations", "Typography",
     "Sora for display, Noto Sans for body, Noto Sans Bengali for Bangla, JetBrains Mono for code",
     stage="".join(
         f'<div style="display:flex;align-items:baseline;gap:1rem;padding:.4rem 0;'
         f'flex-wrap:wrap;border-bottom:1px solid var(--gru-border)">'
         f'<code class="gru-mono" style="font-size:.66rem;min-width:min(9rem,100%);'
         f'color:var(--gru-ink-subtle)">--gru-text-{t}</code>'
         f'<span style="font-size:var(--gru-text-{t});min-width:0;overflow-wrap:anywhere;'
         f'font-family:var(--gru-font-{"display" if t in ("4xl","3xl","2xl","xl","lg") else "text"});'
         f'letter-spacing:var(--gru-tracking-display);line-height:1.1">{label} GRU953</span></div>'
         for t, label in TYPE_ROWS)
     + '<p style="margin-top:1.5rem" lang="bn">সহজ প্রযুক্তি। সবার জন্য। — বাংলা একই '
       'ফন্ট-ফ্যামিলিতে, শুধু Bengali unicode-range দিয়ে। দ্বিভাষিক বাক্যে কোনো markup লাগে না।</p>'
       '<pre class="gru-code" tabindex="0" role="region" aria-label="Code sample" style="margin-top:1rem">const gru = "GRU953";  // JetBrains Mono</pre>',
     notes="Both families declare Bangla through a Bengali <code>unicode-range</code>, so a "
           "bilingual sentence needs no markup and no manual font switching. The numerals "
           "decided Sora: GRU953 contains three digits, and its 9, 5 and 3 have flat "
           "geometric terminals.",
     height=1000)

card("foundations", "space-shape-depth", "Foundations", "Space, shape and depth",
     "A 4px scale, four radii, three elevations",
     stage="""
  <div class="gru-eyebrow">space</div>
  <div class="gru-stack-2" style="margin:.5rem 0 1.5rem">""" + "".join(
         f'<div style="display:flex;align-items:center;gap:.75rem">'
         f'<code class="gru-mono" style="font-size:.66rem;min-width:min(8rem,60%);'
         f'color:var(--gru-ink-subtle)">--gru-space-{n}</code>'
         f'<span style="height:12px;width:var(--gru-space-{n});background:var(--gru-accent);'
         f'border-radius:2px"></span></div>' for n in range(1, 11)) + """</div>
  <div class="gru-eyebrow">shape</div>
  <div class="gru-row" style="margin:.5rem 0 1.5rem">""" + "".join(
         f'<div style="width:76px;height:56px;background:var(--gru-brand-quiet);'
         f'border:1px solid var(--gru-border-strong);border-radius:var(--gru-radius-{r});'
         f'display:grid;place-items:center;font-family:var(--gru-font-mono);font-size:.6rem">'
         f'{r}</div>' for r in ("xs", "sm", "md", "lg", "full")) + """</div>
  <div class="gru-eyebrow">depth</div>
  <div class="gru-row" style="margin:.5rem 0 0">""" + "".join(
         f'<div style="width:96px;height:64px;background:var(--gru-surface-raised);'
         f'border:1px solid var(--gru-border);border-radius:var(--gru-radius-md);'
         f'box-shadow:var(--gru-shadow-{n});display:grid;place-items:center;'
         f'font-family:var(--gru-font-mono);font-size:.6rem">shadow-{n}</div>'
         for n in (1, 2, 3)) + "</div>",
     notes="When unsure, use <code>--gru-space-4</code> (16px). Radii carry meaning: 4px for "
           "badges and inline code, 8px for buttons and inputs, 14px for cards, 24px for hero "
           "panels. The app icon's 22.46% squircle is used nowhere else.",
     height=920)

card("foundations", "marks", "Foundations", "The marks",
     "One bird, one tile, six lockups — and the size floor that decides between them",
     stage=f"""
  <div class="gru-grid">
    <div class="gru-card" style="text-align:center">
      <div style="color:var(--gru-brand);width:120px;margin:0 auto 1rem">{mark("GRU953-bird")}</div>
      <div class="gru-card__meta">the mark · 24px and above</div>
      <div class="gru-row" style="justify-content:center;align-items:flex-end;gap:1rem">
        <span style="color:var(--gru-brand);width:48px">{mark("GRU953-bird", "gru-mark b48")}</span>
        <span style="color:var(--gru-brand);width:32px">{mark("GRU953-bird", "gru-mark b32")}</span>
        <span style="color:var(--gru-brand);width:24px">{mark("GRU953-bird", "gru-mark b24")}</span>
      </div>
    </div>
    <div class="gru-card" style="text-align:center">
      <div style="width:120px;margin:0 auto 1rem">{mark("GRU953-appicon")}</div>
      <div class="gru-card__meta">the tile · below 24px</div>
      <div class="gru-row" style="justify-content:center;align-items:flex-end;gap:1rem">
        <span style="width:32px">{mark("GRU953-appicon", "gru-mark t32")}</span>
        <span style="width:24px">{mark("GRU953-appicon", "gru-mark t24")}</span>
        <span style="width:16px">{mark("GRU953-appicon", "gru-mark t16")}</span>
      </div>
    </div>
  </div>
  <div style="color:var(--gru-brand);max-width:420px;margin:1.5rem 0">
    {mark("GRU953-lockup-horizontal-tagline")}</div>
  <div style="color:var(--gru-brand);max-width:260px">{mark("GRU953-lockup-stacked")}</div>""",
     notes="Below 24px the wing's counters close, so the tile is used instead — a block of "
           "colour survives where a line drawing cannot. The floor is checked mechanically "
           "when the mark is generated. Set <code>color:</code>, never <code>fill:</code>. "
           "<b>The mark does not move.</b>",
     height=1050)

card("foundations", "motion", "Foundations", "Motion",
     "Two durations, two easings, and one thing that never moves",
     full=f"""
  <style>
  .mo{{display:grid;gap:var(--gru-space-4);max-width:34rem}}
  .mo__row{{display:flex;align-items:center;gap:var(--gru-space-4)}}
  .mo__track{{flex:1;height:36px;background:var(--gru-bg-subtle);
    border:1px solid var(--gru-border);border-radius:var(--gru-radius-full);position:relative}}
  .mo__dot{{position:absolute;top:5px;left:5px;width:24px;height:24px;border-radius:50%;
    background:var(--gru-accent)}}
  .mo__fast .mo__dot{{animation:mo 1.6s var(--gru-ease-out) infinite alternate}}
  .mo__base .mo__dot{{animation:mo 2.4s var(--gru-ease-in-out) infinite alternate}}
  @keyframes mo{{to{{left:calc(100% - 29px)}}}}
  @media (prefers-reduced-motion:reduce){{.mo__dot{{animation:none!important;left:50%!important}}}}
  </style>
  <div class="mo">
    <div class="mo__row mo__fast"><code class="gru-mono" style="min-width:11rem">
      --gru-duration-fast</code><div class="mo__track"><div class="mo__dot"></div></div></div>
    <div class="mo__row mo__base"><code class="gru-mono" style="min-width:11rem">
      --gru-duration-base</code><div class="mo__track"><div class="mo__dot"></div></div></div>
  </div>
  <div class="gru-alert gru-alert--info" style="max-width:34rem;margin-top:1.5rem">
    <span class="gru-alert__icon" aria-hidden="true">i</span>
    <div class="gru-alert__body"><div class="gru-alert__title">The mark never moves</div>
    <p style="margin:0">A logo that animates can be caught mid-movement looking broken — in a
    screenshot, in a thumbnail, on a slow connection. Everything else here may animate; the
    bird does not.</p></div>
  </div>
  <p class="dsp__notes" style="margin-top:1.5rem"><code>prefers-reduced-motion</code> is
  honoured throughout, and means it: the dots above stop, and the spinner loses its rotation
  rather than spinning at a millisecond a turn.</p>""",
     height=560)

# ============================================================ COMPONENTS
BTN_STAGE = """
  <div class="gru-row" style="margin-bottom:1rem">
    <button class="gru-btn gru-btn--primary">Save changes</button>
    <button class="gru-btn gru-btn--brand">Publish</button>
    <button class="gru-btn gru-btn--secondary">Cancel</button>
    <button class="gru-btn gru-btn--ghost">More</button>
    <button class="gru-btn gru-btn--danger">Delete for ever</button>
  </div>
  <div class="gru-row" style="margin-bottom:1rem">
    <button class="gru-btn gru-btn--primary gru-btn--sm">Small</button>
    <button class="gru-btn gru-btn--primary">Default</button>
    <button class="gru-btn gru-btn--primary gru-btn--lg">Large</button>
  </div>
  <div class="gru-row">
    <button class="gru-btn gru-btn--primary" disabled>Disabled</button>
    <button class="gru-btn gru-btn--primary" aria-busy="true">
      <span class="gru-spinner" aria-hidden="true"></span> Saving<span class="gru-sr">, please wait</span>
    </button>
    <a class="gru-btn gru-btn--secondary" href="#">A link that looks like a button</a>
  </div>"""
card("components", "button", "Components", "Button",
     "Five intents, three sizes, every state",
     stage=BTN_STAGE,
     notes="One primary action per view. A button says exactly what happens when it is used — "
           "\"Save changes\", not \"Submit\" — and keeps that name through the whole flow, so "
           "the button that says \"Publish\" produces a message that says \"Published\". The "
           "loading state keeps its width so the layout does not jump, and announces itself: "
           "a spinner alone tells a screen reader nothing.")

card("components", "input", "Components", "Text fields",
     "Label, hint, error and disabled — wired together",
     stage="""
  <div class="gru-field">
    <label class="gru-field__label" for="a1">Shop name <span class="gru-req" aria-hidden="true">*</span>
      <span class="gru-sr">(required)</span></label>
    <input class="gru-input" id="a1" value="Rahman Stores" required aria-describedby="a1h">
    <span class="gru-field__hint" id="a1h">The name your customers know.</span>
  </div>
  <div class="gru-field">
    <label class="gru-field__label" for="a6">Shop code</label>
    <input class="gru-input" id="a6" value="RS-001" disabled aria-describedby="a6h">
    <span class="gru-field__hint" id="a6h">Set when the shop was created. It cannot
      be changed.</span>
  </div>
  <div class="gru-field">
    <label class="gru-field__label" for="a2">Daily takings</label>
    <div class="gru-input-group">
      <input class="gru-input" id="a2" inputmode="decimal" placeholder="0.00">
      <button class="gru-btn gru-btn--secondary" type="button">BDT</button>
    </div>
  </div>
  <div class="gru-field">
    <label class="gru-field__label" for="a3">Email</label>
    <input class="gru-input" id="a3" type="email" value="rahman@" aria-invalid="true"
           aria-describedby="a3e">
    <span class="gru-field__error" id="a3e">Add the part after the @ — for example
      rahman@example.com.</span>
  </div>
  <div class="gru-field">
    <label class="gru-field__label" for="a4">Note</label>
    <textarea class="gru-textarea" id="a4" placeholder="Anything worth remembering"></textarea>
  </div>
  <div class="gru-field" style="margin-bottom:0">
    <label class="gru-field__label" for="a5">Branch</label>
    <select class="gru-select" id="a5"><option>Dhaka</option><option>Khulna</option></select>
  </div>""",
     notes="A real <code>&lt;label&gt;</code> every time — a placeholder is not a label, and it "
           "disappears the moment someone types. The error is joined to its field with "
           "<code>aria-describedby</code>, says what to do next, and never blames the reader. "
           "The required marker is a shape for sighted readers and a word for everyone else.",
     height=880)

card("components", "choice", "Components", "Checkbox, radio and switch",
     "Choices, with a note where a note helps",
     stage="""
  <fieldset style="border:0;padding:0;margin:0 0 1.5rem">
    <legend class="gru-field__label" style="padding:0 0 .5rem">Backups</legend>
    <label class="gru-choice"><input type="checkbox" checked>
      <span class="gru-choice__text">Keep a copy on this phone
      <span class="gru-choice__note">Works with no connection.</span></span></label>
    <label class="gru-choice"><input type="checkbox">
      <span class="gru-choice__text">Copy to a memory card</span></label>
    <label class="gru-choice"><input type="checkbox" disabled>
      <span class="gru-choice__text">Copy to the cloud
      <span class="gru-choice__note">Not available offline.</span></span></label>
  </fieldset>
  <fieldset style="border:0;padding:0;margin:0 0 1.5rem">
    <legend class="gru-field__label" style="padding:0 0 .5rem">Language</legend>
    <label class="gru-choice"><input type="radio" name="l" checked>
      <span class="gru-choice__text" lang="bn">বাংলা</span></label>
    <label class="gru-choice"><input type="radio" name="l">
      <span class="gru-choice__text">English</span></label>
    <label class="gru-choice"><input type="radio" name="l">
      <span class="gru-choice__text">Follow the phone</span></label>
  </fieldset>
  <label class="gru-switch"><input type="checkbox" checked role="switch">
    <span class="gru-switch__track" aria-hidden="true"></span>
    <span class="gru-choice__text">Round to the nearest taka</span>
    <span class="gru-switch__state" aria-hidden="true">on</span></label>
  <label class="gru-switch" style="margin-top:.5rem"><input type="checkbox" role="switch">
    <span class="gru-switch__track" aria-hidden="true"></span>
    <span class="gru-choice__text">Show last year beside this year</span>
    <span class="gru-switch__state" aria-hidden="true">off</span></label>""",
     notes="The switch prints <b>on</b> or <b>off</b> beside itself, because a knob's position "
           "is a shape a colour-blind reader can miss and a low-vision reader may not resolve "
           "at all. Grouped choices sit in a <code>&lt;fieldset&gt;</code> with a "
           "<code>&lt;legend&gt;</code>, so the question is announced with the answers.",
     height=880)

card("components", "card", "Components", "Card",
     "Flat, raised, sunken, and the whole-card link",
     stage="""
  <div class="gru-grid">
    <article class="gru-card">
      <div class="gru-card__meta">13 August 2026</div>
      <h3 class="gru-card__title">Offline saving</h3>
      <p class="gru-muted" style="margin:0">Entries are kept on the phone and sent when there
      is a connection. Nothing waits for a network.</p>
    </article>
    <article class="gru-card gru-card--raised gru-card--link">
      <div class="gru-card__meta">Guide</div>
      <h3 class="gru-card__title"><a href="#">Setting up a second shop</a></h3>
      <p class="gru-muted" style="margin:0">Four minutes, one screen at a time.</p>
      <div class="gru-card__foot"><span class="gru-badge"><span class="gru-badge__dot"
        aria-hidden="true"></span>Updated</span></div>
    </article>
    <article class="gru-card gru-card--sunken">
      <div class="gru-card__meta">Note</div>
      <p style="margin:0">A sunken card is for something set apart from the page rather than
      lifted off it — a quotation, an aside, a preformatted block.</p>
    </article>
  </div>""",
     notes="On the middle card the anchor covers the whole card, so the hit area is the card "
           "while the accessible name is still just the title. The card takes the focus ring "
           "through <code>:focus-within</code>, so a keyboard user sees what a mouse user "
           "hovers.")

card("components", "alert", "Components", "Alert",
     "The four meanings — each with an icon and a word, never colour alone",
     stage="""
  <div class="gru-stack">
    <div class="gru-alert gru-alert--info" role="note">
      <span class="gru-alert__icon" aria-hidden="true">i</span>
      <div class="gru-alert__body"><div class="gru-alert__title">Information</div>
      <p style="margin:0">Backups run once a day, at whatever time the phone is on charge.</p></div>
    </div>
    <div class="gru-alert gru-alert--success" role="status">
      <span class="gru-alert__icon" aria-hidden="true">✓</span>
      <div class="gru-alert__body"><div class="gru-alert__title">Saved</div>
      <p style="margin:0">Fourteen entries were sent. Nothing is waiting.</p></div>
    </div>
    <div class="gru-alert gru-alert--warning" role="note">
      <span class="gru-alert__icon" aria-hidden="true">!</span>
      <div class="gru-alert__body"><div class="gru-alert__title">Worth knowing</div>
      <p style="margin:0">The memory card is 92% full. At 100% new entries stay on the phone.</p></div>
    </div>
    <div class="gru-alert gru-alert--danger" role="alert">
      <span class="gru-alert__icon" aria-hidden="true">✗</span>
      <div class="gru-alert__body"><div class="gru-alert__title">March entries saved as April</div>
      <p style="margin:0">Entries added between 2 and 6 August have the wrong month. They are
      corrected when you next open the app — nothing was lost.</p></div>
    </div>
  </div>""",
     notes="Bad news goes at the top, not the bottom. An error says what happened and what to "
           "do next, and never apologises in a person's voice. <code>role=\"alert\"</code> is "
           "for something that has just gone wrong; <code>role=\"status\"</code> for something "
           "that has just succeeded; a static note gets neither, so it does not interrupt.",
     height=760)

card("components", "badge", "Components", "Badge",
     "Status and labels, with a dot so status is never colour alone",
     stage="""
  <div class="gru-row" style="margin-bottom:1rem">
    <span class="gru-badge">Draft</span>
    <span class="gru-badge gru-badge--brand">Apache-2.0</span>
    <span class="gru-badge gru-badge--accent">New</span>
  </div>
  <div class="gru-row">
    <span class="gru-badge gru-badge--info"><span class="gru-badge__dot" aria-hidden="true"></span>Queued</span>
    <span class="gru-badge gru-badge--success"><span class="gru-badge__dot" aria-hidden="true"></span>Sent</span>
    <span class="gru-badge gru-badge--warning"><span class="gru-badge__dot" aria-hidden="true"></span>Retrying</span>
    <span class="gru-badge gru-badge--danger"><span class="gru-badge__dot" aria-hidden="true"></span>Failed</span>
  </div>""",
     notes="The word inside the badge is the meaning; the colour and the dot only reinforce it. "
           "A badge that says nothing and relies on being red is unreadable to about one man in "
           "twelve.", height=440)

card("components", "table", "Components", "Table",
     "A real header row, tabular numerals, and sideways scrolling instead of a broken page",
     stage="""
  <div class="gru-tablewrap" tabindex="0" role="region" aria-label="Daily takings">
    <table class="gru-table">
      <caption>Daily takings · last five days · BDT</caption>
      <thead><tr><th scope="col">Date</th><th scope="col">Shop</th>
        <th scope="col" class="num">Takings</th><th scope="col" class="num">Entries</th>
        <th scope="col">State</th></tr></thead>
      <tbody>
        <tr><td>13 Aug</td><td>Rahman Stores</td><td class="num">12,480</td><td class="num">31</td>
          <td><span class="gru-badge gru-badge--success"><span class="gru-badge__dot"
            aria-hidden="true"></span>Sent</span></td></tr>
        <tr><td>12 Aug</td><td>Rahman Stores</td><td class="num">9,120</td><td class="num">24</td>
          <td><span class="gru-badge gru-badge--success"><span class="gru-badge__dot"
            aria-hidden="true"></span>Sent</span></td></tr>
        <tr><td>11 Aug</td><td>Second shop</td><td class="num">4,300</td><td class="num">11</td>
          <td><span class="gru-badge gru-badge--warning"><span class="gru-badge__dot"
            aria-hidden="true"></span>Retrying</span></td></tr>
        <tr><td>10 Aug</td><td>Rahman Stores</td><td class="num">15,905</td><td class="num">38</td>
          <td><span class="gru-badge gru-badge--success"><span class="gru-badge__dot"
            aria-hidden="true"></span>Sent</span></td></tr>
        <tr><td>9 Aug</td><td>Second shop</td><td class="num">0</td><td class="num">0</td>
          <td><span class="gru-badge"><span class="gru-badge__dot" aria-hidden="true"></span>Closed</span></td></tr>
      </tbody>
    </table>
  </div>""",
     notes="A five-column table cannot reflow onto a 320px screen, so it scrolls inside its own "
           "box. When that box <b>actually overflows</b> it also needs <code>tabindex=\"0\"</code>, "
           "or its far side is unreachable from the keyboard \u2014 and when it does not overflow "
           "it must not have one, because a tab stop on a table that fits is noise. Only "
           "JavaScript can tell the two apart (<code>el.scrollWidth &gt; el.clientWidth</code>), "
           "so the attribute is not in this markup. Numbers are right-aligned and "
           "<code>tabular-nums</code>, so columns of figures line up.", height=640)

card("components", "tabs", "Components", "Tabs",
     "Selected by weight, colour and an underline — not by colour alone",
     stage="""
  <div class="gru-tabs" role="tablist" aria-label="Report period">
    <button class="gru-tab" role="tab" id="tw" aria-controls="tp" aria-selected="true"
      tabindex="0">This week</button>
    <button class="gru-tab" role="tab" id="tm" aria-controls="tp" aria-selected="false"
      tabindex="-1">This month</button>
    <button class="gru-tab" role="tab" id="ty" aria-controls="tp" aria-selected="false"
      tabindex="-1">This year</button>
    <button class="gru-tab" role="tab" id="te" aria-controls="tp" aria-selected="false"
      tabindex="-1">Everything</button>
  </div>
  <div role="tabpanel" id="tp" aria-labelledby="tw" tabindex="0" style="padding-top:1.25rem">
    <p style="margin:0">Six days of entries, 31 in total. The highest single day was Tuesday.</p>
  </div>""",
     notes="The relationships are in the markup: every tab has an <code>id</code> and an "
           "<code>aria-controls</code>, the panel names its tab with <code>aria-labelledby</code>, "
           "and the roving <code>tabindex</code> makes the set one Tab stop rather than four. "
           "What is still missing is <b>behaviour</b>: arrow keys must move the selection and "
           "move that roving <code>tabindex</code> with it, and that is JavaScript this CSS "
           "cannot provide. If you are not going to write it, use links instead of a tablist "
           "— a wrong ARIA pattern is worse than none.", height=450)

card("components", "nav", "Components", "Navigation",
     "Top bar, side navigation, breadcrumb and pagination",
     stage=f"""
  <nav class="gru-topbar" style="margin:-1.25rem -1.25rem 1.5rem;min-width:0"
       aria-label="Main">
    <a class="gru-topbar__brand" href="#">
      <span style="width:2em">{mark("GRU953-bird", "gru-mark nb")}</span> Ledger</a>
    <span class="gru-topbar__spacer"></span>
    <ul class="gru-navlist">
      <li><a class="gru-navlink" href="#" aria-current="page">Today</a></li>
      <li><a class="gru-navlink" href="#">Reports</a></li>
      <li><a class="gru-navlink" href="#">Settings</a></li>
    </ul>
  </nav>
  <div class="gru-shell" style="padding:0">
    <nav class="gru-sidenav" aria-label="Sections">
      <div class="gru-sidenav__group">Money</div>
      <ul><li><a href="#" aria-current="page">Takings</a></li>
        <li><a href="#">Expenses</a></li></ul>
      <div class="gru-sidenav__group">Setup</div>
      <ul><li><a href="#">Shops</a></li>
        <li><a href="#">Backups</a></li></ul>
    </nav>
    <div>
      <nav aria-label="Breadcrumb"><ol class="gru-breadcrumb">
        <li><a href="#">Ledger</a></li><li><a href="#">Reports</a></li>
        <li><span aria-current="page">August</span></li></ol></nav>
      <nav aria-label="Pages" style="margin-top:1.5rem"><ul class="gru-pagination">
        <li><a href="#">Previous</a></li>
        <li><a href="#" aria-current="page">1</a></li>
        <li><a href="#">2</a></li><li><a href="#">3</a></li>
        <li><span class="gru-gap">…</span></li><li><a href="#">9</a></li>
        <li><a href="#">Next</a></li></ul></nav>
    </div>
  </div>""",
     notes="<code>aria-current=\"page\"</code> is what tells a screen reader which item is the "
           "one you are on; the colour and the inset rule are for everyone else. Every "
           "navigation region has a name, so a screen reader can list them and tell them apart.",
     height=680)

card("components", "dialog", "Components", "Dialog and toast",
     "A real &lt;dialog&gt;, so Escape and the focus trap come for free",
     stage="""
  <dialog class="gru-dialog" open
          style="display:block;position:static;box-shadow:var(--gru-shadow-2)"
          aria-labelledby="dt" aria-describedby="db">
    <div class="gru-dialog__head"><h3 id="dt" style="margin:0">Delete this shop?</h3></div>
    <div class="gru-dialog__body" id="db">
      <p style="margin:0">Rahman Stores has 412 entries. Deleting the shop deletes them too,
      and it cannot be undone.</p>
    </div>
    <div class="gru-dialog__foot">
      <button class="gru-btn gru-btn--secondary">Keep it</button>
      <button class="gru-btn gru-btn--danger">Delete the shop and 412 entries</button>
    </div>
  </dialog>
  <div class="gru-toasts gru-toasts--inline" style="margin-top:1.5rem">
    <div class="gru-toast gru-toast--success" role="status">
      <span aria-hidden="true">✓</span>
      <div style="flex:1">Fourteen entries sent.</div>
      <button class="gru-toast__close" aria-label="Dismiss">
        <span aria-hidden="true">×</span></button>
    </div>
    <div class="gru-toast gru-toast--danger" role="alert">
      <span aria-hidden="true">✗</span>
      <div style="flex:1">Could not reach the server. The entries are safe on this phone and
      will be sent when there is a connection.</div>
      <button class="gru-toast__close" aria-label="Dismiss">
        <span aria-hidden="true">×</span></button>
    </div>
  </div>""",
     notes="This preview is a real <code>&lt;dialog&gt;</code> with the <code>open</code> "
           "attribute, laid out in the page so you can see it. <b>In a product, open it with "
           "<code>showModal()</code> instead</b> \u2014 that is what supplies Escape, the focus "
           "trap, the <code>::backdrop</code> and returning focus to the opener, and an "
           "<code>open</code> attribute alone supplies none of them. All four are easy to get "
           "wrong by hand, which is the argument for the element. The destructive button names "
           "what it destroys and how much of it \u2014 \"Delete\" alone is how people lose work.",
     height=700)

card("components", "feedback", "Components", "Progress and loading",
     "A bar, a spinner and a skeleton — each saying something different",
     stage="""
  <div class="gru-progress" style="margin-bottom:1.5rem">
    <div class="gru-progress__track"><div class="gru-progress__bar" style="width:64%"
      role="progressbar" aria-valuenow="64" aria-valuemin="0" aria-valuemax="100"
      aria-label="Sending entries"></div></div>
    <div class="gru-progress__label" id="pl">64% · 9 of 14 entries sent</div>
  </div>
  <div class="gru-row" style="margin-bottom:1.5rem">
    <span class="gru-spinner" aria-hidden="true"></span>
    <span>Checking for a connection<span class="gru-sr">, please wait</span></span>
  </div>
  <div class="gru-card gru-stack-2" aria-busy="true" aria-live="polite">
    <div class="gru-skel gru-skel--title"></div>
    <div class="gru-skel gru-skel--line"></div>
    <div class="gru-skel gru-skel--line"></div>
    <div class="gru-skel gru-skel--short"></div>
    <span class="gru-sr">Loading the report</span>
  </div>""",
     notes="A percentage always says what it is a percentage <em>of</em>. A spinner is never the "
           "only signal — there is always a word beside it, because a spinner alone tells a "
           "screen reader nothing and tells a waiting person even less. Under "
           "<code>prefers-reduced-motion</code> the spinner stops rotating rather than "
           "rotating imperceptibly.", height=620)

card("components", "state", "Components", "Empty and error states",
     "An invitation to act, not an apology",
     stage=f"""
  <div class="gru-state" style="margin-bottom:1.5rem">
    <div class="gru-state__art">{mark("GRU953-bird", "gru-mark sa")}</div>
    <h3 class="gru-state__title">No entries yet</h3>
    <p class="gru-state__body">Add today's takings and the report builds itself. It takes about
    ten seconds.</p>
    <button class="gru-btn gru-btn--primary">Add today's takings</button>
  </div>
  <div class="gru-state gru-state--error">
    <div class="gru-state__art" aria-hidden="true"
      style="font-size:3rem;line-height:1;font-family:var(--gru-font-display)">✗</div>
    <h3 class="gru-state__title">The report could not be built</h3>
    <p class="gru-state__body">Three entries have no date. Open them, add a date, and the report
    will build.</p>
    <div class="gru-row" style="justify-content:center">
      <button class="gru-btn gru-btn--primary">Show the three entries</button>
      <button class="gru-btn gru-btn--ghost">Try again</button>
    </div>
  </div>""",
     notes="An empty screen is the best chance the product gets to teach one thing, so it names "
           "the single next action and says roughly how long it takes. An error state names what "
           "went wrong, how many things are affected, and the action that fixes it — and offers "
           "that action, rather than describing it.", height=760)

card("components", "stat", "Components", "Stat",
     "A number, what it means, and where it came from",
     stage="""
  <div class="gru-stats">
    <div class="gru-stat"><div class="gru-stat__label">Takings, this week</div>
      <div class="gru-stat__value">41,805</div>
      <div class="gru-stat__note">BDT · <span class="gru-stat__delta gru-stat__delta--up">18%
        on last week</span></div></div>
    <div class="gru-stat"><div class="gru-stat__label">Entries</div>
      <div class="gru-stat__value">104</div>
      <div class="gru-stat__note">6 days · <span class="gru-stat__delta gru-stat__delta--down">4
        fewer than last week</span></div></div>
    <div class="gru-stat"><div class="gru-stat__label">Waiting to send</div>
      <div class="gru-stat__value">0</div>
      <div class="gru-stat__note">last sent 11 minutes ago</div></div>
  </div>""",
     notes="A number with no unit and no comparison is decoration. The arrow carries the "
           "direction so the colour only reinforces it, and the comparison says what it is "
           "compared <em>with</em> — \"18%\" alone means nothing.", height=440)

card("components", "code", "Components", "Code",
     "A block that can be copied, and a filename that says what it is",
     stage="""
  <div class="gru-code__head"><span>styles/app.css</span><span style="flex:1"></span>
    <button class="gru-btn gru-btn--ghost gru-btn--sm">Copy</button></div>
  <pre class="gru-code" tabindex="0" role="region" aria-label="A card, in CSS">@import url("tokens.css");

.card{
  background: var(--gru-surface-raised);
  color:      var(--gru-ink);
  border:     1px solid var(--gru-border);
  border-radius: var(--gru-radius-lg);
  padding:    var(--gru-space-5);
}</pre>
  <p class="gru-muted" style="margin-top:1rem">Inline code such as
  <code>--gru-accent</code> sits in the body text without breaking the line height.</p>""",
     notes="Not one literal colour in the example, which is the whole point: the same six lines "
           "are correct in the light theme and the dark one. JetBrains Mono has ligatures turned "
           "off in this system — <code>=&gt;</code> should look like two characters, because it "
           "is two characters.", height=520)

# The height of a bar is the only place the value lives in CSS, and a height is not
# readable by anything but an eye. Every bar therefore carries its figure as text, and the
# whole series is repeated as a table for a screen reader — because "44px tall" means
# nothing to somebody who cannot see it.
CHART_DATA = [(44, "Mon", "4,400"), (78, "Tue", "7,800"), (61, "Wed", "6,100"),
              (96, "Thu", "9,600"), (52, "Fri", "5,200"), (33, "Sat", "3,300")]
CHART_BARS = "".join(
    f'<div class="gru-chart__bar"><i class="gru-s{i}" style="height:{h}px" '
    f'aria-hidden="true"></i><span>{lab}</span></div>'
    for i, (h, lab, _) in enumerate(CHART_DATA, 1))
CHART_TABLE = ('<table class="gru-sr"><caption>Takings by day, in taka</caption><thead>'
               '<tr><th scope="col">Day</th><th scope="col">Taka</th></tr></thead><tbody>'
               + "".join(f'<tr><th scope="row">{lab}</th><td>{v}</td></tr>'
                         for _, lab, v in CHART_DATA) + "</tbody></table>")
card("components", "chart", "Components", "Chart",
     "Six series that clear 3:1 on their own ground and stay \u0394E 10 apart",
     stage=f"""
  <figure class="gru-chart" style="margin:0">
    <figcaption class="gru-eyebrow">Takings by day, in taka</figcaption>
    <div class="gru-chart__bars">{CHART_BARS}</div>
    {CHART_TABLE}
    <p class="gru-subtle" style="font-size:var(--gru-text-xs);margin:.6rem 0 0">Mon 4,400 \u00b7
    Tue 7,800 \u00b7 Wed 6,100 \u00b7 Thu 9,600 \u00b7 Fri 5,200 \u00b7 Sat 3,300</p>
  </figure>""",
     notes="Use <code>--gru-chart-1</code> to <code>--gru-chart-6</code> in order, so the first "
           "two series a reader sees are the brand's own colours. Every one clears 3:1 against "
           "its own theme's background and no two are within \u0394E 10. "
           "<b>A bar's height is not data anyone can read aloud.</b> The figures are printed "
           "under the chart and repeated in a visually-hidden table, so the chart is not the "
           "only copy of its own numbers \u2014 and a legend of palette names, which is what "
           "this card used to show beside six weekday bars, is not a legend at all.",
     height=560)

# ============================================================ PATTERNS
def page(inner: str, theme: str | None = "light") -> str:
    """A pattern's frame. `theme=None` omits the attribute; it does not blank it.

    `data-theme=""` matches neither `[data-theme="light"]` nor `[data-theme="dark"]`, so
    it inherits whatever the document pinned. The card that exists to demonstrate the
    unset state used to do exactly that, inside a document pinned to light — so it
    rendered light on every machine while three separate strings said it followed the
    reader's system setting.
    """
    attr = f' data-theme="{theme}"' if theme else ""
    return f'<div class="gru"{attr} style="border:1px solid var(--gru-border-strong);' \
           f'border-radius:var(--gru-radius-md);overflow:hidden">{inner}</div>'


card("patterns", "landing", "Patterns", "A landing page",
     "The hero as a thesis, then the reading",
     full=page(f"""
  <a class="gru-skip" href="#lm">Skip to the content</a>
  <nav class="gru-topbar" aria-label="Main">
    <a class="gru-topbar__brand" href="#"><span style="width:2em">
      {mark("GRU953-bird", "gru-mark pb")}</span> Ledger</a>
    <span class="gru-topbar__spacer"></span>
    <ul class="gru-navlist">
      <li><a class="gru-navlink" href="#">What it does</a></li>
      <li><a class="gru-navlink" href="#">Price</a></li>
    </ul>
    <a class="gru-btn gru-btn--primary gru-btn--sm" href="#">Get it</a>
  </nav>
  <main id="lm" style="padding:var(--gru-space-6) var(--gru-page-padding)">
    <section class="gru-hero">
     <div class="gru-hero__content">
      <div class="gru-hero__mark">{mark("GRU953-bird", "gru-mark hb")}</div>
      <h1 style="font-size:var(--gru-text-3xl);margin:0 0 .4em">A day's takings,<br>in ten seconds</h1>
      <p class="gru-hero__sub" style="font-size:var(--gru-text-md);margin:0 0 .3em;max-width:34ch">
        Ledger by GRU953 keeps a record of daily takings. It works with no connection, on a
        five-year-old phone, in Bangla or English.</p>
      <p lang="bn" class="gru-hero__sub" style="margin:0 0 1.5rem">সহজ প্রযুক্তি। সবার জন্য।</p>
      <div class="gru-row">
        <a class="gru-btn gru-btn--lg" href="#"
           style="background:var(--gru-ground-paper);color:var(--gru-meridian-900)">Get it free</a>
        <a class="gru-btn gru-btn--lg gru-btn--ghost" href="#">See a day</a>
      </div>
     </div>
    </section>
    <section style="margin-top:var(--gru-space-7)">
      <div class="gru-eyebrow">What it actually does</div>
      <div class="gru-grid" style="margin-top:var(--gru-space-4)">
        <article class="gru-card"><h3 class="gru-card__title">Works offline</h3>
          <p class="gru-muted" style="margin:0">Entries are kept on the phone and sent when
          there is a connection. Nothing waits for a network.</p></article>
        <article class="gru-card"><h3 class="gru-card__title">Two languages</h3>
          <p class="gru-muted" style="margin:0">Bangla and English from the first screen, not
          as a setting you find later.</p></article>
        <article class="gru-card"><h3 class="gru-card__title">7.4 MB</h3>
          <p class="gru-muted" style="margin:0">Measured on install, not estimated. It runs on
          Android 8 and later.</p></article>
      </div>
    </section>
    <section style="margin-top:var(--gru-space-7)" class="gru-prose">
      <h2>What it does not do</h2>
      <ul><li>No stock or inventory. It records money, and only money.</li>
      <li>One shop per phone. Two shops need two profiles.</li>
      <li>No cloud account. Nothing is uploaded unless you export it.</li></ul>
    </section>
  </main>
  <footer style="border-top:1px solid var(--gru-border);padding:var(--gru-space-5)
    var(--gru-page-padding);display:flex;gap:var(--gru-space-4);align-items:center;flex-wrap:wrap">
    <span style="color:var(--gru-brand);width:150px">{mark("GRU953-lockup-horizontal", "gru-mark fl")}</span>
    <span class="gru-spacer" style="flex:1"></span>
    <span class="gru-subtle" style="font-size:var(--gru-text-xs)">Apache-2.0 · the marks are
    not licensed</span>
  </footer>"""),
     notes="The hero opens with the most characteristic thing about the product — a number and a "
           "promise — and the gradient appears here and nowhere else. The third card is a file "
           "size rather than an adjective, which is the brand's habit: whenever something "
           "measurable is claimed, publish the measurement.", height=1400)

card("patterns", "settings", "Patterns", "A settings screen",
     "Grouped, plainly named, with the destructive thing kept apart",
     full=page(f"""
  <nav class="gru-topbar" aria-label="Main">
    <a class="gru-topbar__brand" href="#"><span style="width:2em">
      {mark("GRU953-bird", "gru-mark sb")}</span> Ledger</a>
    <span class="gru-topbar__spacer"></span>
    <ul class="gru-navlist">
      <li><a class="gru-navlink" href="#">Today</a></li>
      <li><a class="gru-navlink" href="#">Reports</a></li>
      <li><a class="gru-navlink" href="#" aria-current="page">Settings</a></li>
    </ul>
  </nav>
  <div class="gru-shell">
    <nav class="gru-sidenav" aria-label="Settings sections">
      <div class="gru-sidenav__group">Setup</div>
      <ul><li><a href="#" aria-current="page">Shop</a></li>
        <li><a href="#">Language</a></li><li><a href="#">Backups</a></li></ul>
      <div class="gru-sidenav__group">Account</div>
      <ul><li><a href="#">Export</a></li>
        <li><a href="#">Delete everything</a></li></ul>
    </nav>
    <main class="gru-stack">
      <nav aria-label="Breadcrumb"><ol class="gru-breadcrumb">
        <li><a href="#">Settings</a></li><li><span aria-current="page">Shop</span></li></ol></nav>
      <h1 style="font-size:var(--gru-text-2xl);margin:0">Shop</h1>
      <div class="gru-card">
        <div class="gru-field">
          <label class="gru-field__label" for="s1">Shop name</label>
          <input class="gru-input" id="s1" value="Rahman Stores">
          <span class="gru-field__hint">Shown at the top of every report.</span>
        </div>
        <div class="gru-field" style="margin-bottom:0">
          <label class="gru-field__label" for="s2">Currency</label>
          <select class="gru-select" id="s2"><option>BDT — Bangladeshi taka</option>
            <option>USD — US dollar</option></select>
        </div>
      </div>
      <div class="gru-card">
        <h2 class="gru-card__title" style="font-size:var(--gru-text-lg)">How numbers are shown</h2>
        <label class="gru-switch"><input type="checkbox" role="switch" checked>
          <span class="gru-switch__track" aria-hidden="true"></span>
          <span class="gru-choice__text">Round to the nearest taka</span>
          <span class="gru-switch__state" aria-hidden="true">on</span></label>
        <label class="gru-switch" style="margin-top:.5rem"><input type="checkbox" role="switch">
          <span class="gru-switch__track" aria-hidden="true"></span>
          <span class="gru-choice__text">Show last year beside this year</span>
          <span class="gru-switch__state" aria-hidden="true">off</span></label>
      </div>
      <div class="gru-row" style="justify-content:flex-end">
        <button class="gru-btn gru-btn--ghost">Cancel</button>
        <button class="gru-btn gru-btn--primary">Save changes</button>
      </div>
      <hr class="gru-hr">
      <div class="gru-card" style="border-color:var(--gru-danger-border)">
        <h2 class="gru-card__title" style="font-size:var(--gru-text-lg)">Delete everything</h2>
        <p class="gru-muted">This removes the shop and all 412 entries from this phone. It
        cannot be undone, and there is no cloud copy to restore from.</p>
        <button class="gru-btn gru-btn--danger">Delete the shop and 412 entries</button>
      </div>
    </main>
  </div>"""),
     notes="The destructive action is below a rule, in its own card, named with the number of "
           "things it destroys — and it is the only red on the page. Settings are named by what "
           "the person controls (\"How numbers are shown\"), never by how the system is built.",
     height=1250)

card("patterns", "docs", "Patterns", "A documentation page",
     "Prose at a readable measure, bilingual, with the code beside it",
     full=page(f"""
  <div class="gru-shell gru-shell--wide">
    <nav class="gru-sidenav" aria-label="Documentation">
      <div class="gru-sidenav__group">Start</div>
      <ul><li><a href="#">Install</a></li>
        <li><a href="#" aria-current="page">Your first entry</a></li>
        <li><a href="#">Reports</a></li></ul>
      <div class="gru-sidenav__group">Reference</div>
      <ul><li><a href="#">Export format</a></li><li><a href="#">Keyboard</a></li></ul>
    </nav>
    <main class="gru-prose">
      <div class="gru-eyebrow">Start · 2 of 3</div>
      <h1 style="font-size:var(--gru-text-2xl);margin:.3em 0 .6em">Your first entry</h1>
      <p>An entry is one day's takings for one shop. Adding one takes about ten seconds, and
      you can do it with no connection.</p>
      <ol><li>Open Ledger and tap <b>Add</b>.</li>
      <li>Type the amount. The date is today unless you change it.</li>
      <li>Tap <b>Save</b>. The entry is on the phone immediately.</li></ol>
      <div class="gru-alert gru-alert--info" role="note">
        <span class="gru-alert__icon" aria-hidden="true">i</span>
        <div class="gru-alert__body"><p style="margin:0">Nothing is sent anywhere at this point.
        Entries leave the phone only when you export them, or when a backup runs.</p></div>
      </div>
      <h2 style="font-size:var(--gru-text-xl);margin-top:1.6em">From the command line</h2>
      <div class="gru-code__head"><span>terminal</span></div>
      <pre class="gru-code" tabindex="0" role="region" aria-label="Adding an entry from the command line">ledger add --amount 12480 --shop "Rahman Stores"
# saved entry 413 for 13 August 2026</pre>
      <h2 style="font-size:var(--gru-text-xl);margin-top:1.6em" lang="bn">বাংলায়</h2>
      <p lang="bn">একটা এন্ট্রি মানে একটা দোকানের একদিনের বিক্রি। যোগ করতে দশ সেকেন্ডের মতো লাগে,
      আর ইন্টারনেট ছাড়াও করা যায়।</p>
      <ol lang="bn"><li>Ledger খুলে <b>যোগ করুন</b>-এ চাপ দিন।</li>
      <li>টাকার পরিমাণ লিখুন। তারিখ নিজে থেকেই আজকের থাকবে।</li>
      <li><b>সেভ</b> চাপুন। এন্ট্রিটা সঙ্গে সঙ্গেই ফোনে থেকে যাবে।</li></ol>
      <hr class="gru-hr">
      <div class="gru-row" style="justify-content:space-between">
        <a href="#">← Install</a><a href="#">Reports →</a>
      </div>
    </main>
  </div>"""),
     notes="Prose is held to <code>--gru-measure</code> — about 68 characters — and the Bangla to "
           "its own slightly narrower measure, because Bangla words are longer and its matra "
           "needs the extra leading. The Bangla is written as Bangla, not translated: the "
           "steps are the same steps, but the sentences are not the English ones converted.",
     height=1250)

# The dashboard is shown in the DARK theme inside a light preview page — which is only
# possible because the token blocks are scoped to [data-theme], not to :root. It is the
# clearest demonstration in the project that a themed island works.
card("patterns", "dashboard", "Patterns", "A dashboard",
     "Numbers with their units, a chart with its legend, and one primary action",
     full=page(f"""
  <nav class="gru-topbar" aria-label="Main">
    <a class="gru-topbar__brand" href="#"><span style="width:2em">
      {mark("GRU953-bird", "gru-mark db")}</span> Ledger</a>
    <span class="gru-topbar__spacer"></span>
    <ul class="gru-navlist">
      <li><a class="gru-navlink" href="#" aria-current="page">Today</a></li>
      <li><a class="gru-navlink" href="#">Reports</a></li>
      <li><a class="gru-navlink" href="#">Settings</a></li>
    </ul>
    <span class="gru-avatar gru-avatar--sm" aria-hidden="true">A</span>
  </nav>
  <main style="padding:var(--gru-space-6) var(--gru-page-padding)" class="gru-stack">
    <div class="gru-row" style="justify-content:space-between">
      <div><div class="gru-eyebrow">Rahman Stores</div>
        <h1 style="font-size:var(--gru-text-2xl);margin:.2em 0 0">This week</h1></div>
      <button class="gru-btn gru-btn--primary">Add today's takings</button>
    </div>
    <div class="gru-stats">
      <div class="gru-stat"><div class="gru-stat__label">Takings</div>
        <div class="gru-stat__value">41,805</div>
        <div class="gru-stat__note">BDT · <span class="gru-stat__delta gru-stat__delta--up">18%
          on last week</span></div></div>
      <div class="gru-stat"><div class="gru-stat__label">Entries</div>
        <div class="gru-stat__value">104</div>
        <div class="gru-stat__note">6 days · <span class="gru-stat__delta gru-stat__delta--down">4
          fewer than last week</span></div></div>
      <div class="gru-stat"><div class="gru-stat__label">Best day</div>
        <div class="gru-stat__value">Thu</div>
        <div class="gru-stat__note">15,905 BDT · 38 entries</div></div>
      <div class="gru-stat"><div class="gru-stat__label">Waiting to send</div>
        <div class="gru-stat__value">0</div>
        <div class="gru-stat__note">last sent 11 minutes ago</div></div>
    </div>
    <div class="gru-card">
      <div class="gru-card__meta">Takings by day · BDT · 7–13 August 2026</div>
      <div class="gru-chart"><div class="gru-chart__bars">{CHART_BARS}</div></div>
    </div>
    <div class="gru-tablewrap" tabindex="0" role="region" aria-label="Recent entries">
      <table class="gru-table"><caption>Recent entries</caption>
        <thead><tr><th scope="col">Date</th><th scope="col" class="num">Amount</th>
          <th scope="col">State</th></tr></thead>
        <tbody>
          <tr><td>13 Aug</td><td class="num">12,480</td><td><span class="gru-badge
            gru-badge--success"><span class="gru-badge__dot" aria-hidden="true"></span>Sent</span></td></tr>
          <tr><td>12 Aug</td><td class="num">9,120</td><td><span class="gru-badge
            gru-badge--success"><span class="gru-badge__dot" aria-hidden="true"></span>Sent</span></td></tr>
          <tr><td>11 Aug</td><td class="num">4,300</td><td><span class="gru-badge
            gru-badge--warning"><span class="gru-badge__dot" aria-hidden="true"></span>Retrying</span></td></tr>
        </tbody></table>
    </div>
  </main>""", "dark"),
     notes="This one is shown in the <b>dark theme inside a light page</b>, which works only "
           "because the theme blocks are scoped to <code>[data-theme]</code> rather than to "
           "<code>:root</code> \u2014 so a themed island is possible at all. One primary action, "
           "top right, and nothing else competes with it. Every number carries its unit and its "
           "comparison, and the chart\u2019s own heading says what the bars are and over what "
           "period, so the picture is not the only thing carrying that.",
     height=1300)

card("patterns", "signin", "Patterns", "A sign-in screen",
     "One job per screen, and an error that helps",
     full=page(f"""
  <div style="display:grid;place-items:center;min-height:34rem;padding:var(--gru-space-6)">
    <main class="gru-card gru-card--raised" style="max-width:23rem;width:100%">
      <div style="color:var(--gru-brand);width:140px;margin-bottom:var(--gru-space-5)">
        {mark("GRU953-lockup-horizontal", "gru-mark si")}</div>
      <h1 style="font-size:var(--gru-text-xl);margin:0 0 .3em">Sign in</h1>
      <p class="gru-muted" style="font-size:var(--gru-text-sm)">To the shop you already set up
      on this phone.</p>
      <div class="gru-field">
        <label class="gru-field__label" for="e">Email</label>
        <input class="gru-input" id="e" type="email" autocomplete="email" value="rahman@example.com">
      </div>
      <div class="gru-field">
        <label class="gru-field__label" for="p">Password</label>
        <input class="gru-input" id="p" type="password" autocomplete="current-password"
          aria-invalid="true" aria-describedby="pe" value="········">
        <span class="gru-field__error" id="pe">That password does not match this email. Two
          attempts left before a five-minute wait.</span>
      </div>
      <button class="gru-btn gru-btn--primary gru-btn--block gru-btn--lg">Sign in</button>
      <div class="gru-row" style="justify-content:space-between;margin-top:var(--gru-space-4);
        font-size:var(--gru-text-sm)">
        <a href="#">Forgotten your password?</a><a href="#">Create an account</a>
      </div>
    </main>
  </div>"""),
     notes="The error says what is wrong <em>and</em> what happens next — how many attempts "
           "remain, and what the consequence is — because \"invalid credentials\" tells someone "
           "nothing they can act on. <code>autocomplete</code> is set properly, which is an "
           "accessibility feature as much as a convenience.", height=760)

# The ONE card with no data-theme attribute, so the automatic path — follow the reader's
# system setting — is actually exercised by the preview suite rather than only claimed.
card("patterns", "automatic", "Patterns", "Following the system",
     "The same page with no data-theme set at all",
     full=page(f"""
  <div style="padding:var(--gru-space-6) var(--gru-page-padding)" class="gru-stack">
    <div class="gru-eyebrow">no data-theme attribute</div>
    <h1 style="font-size:var(--gru-text-2xl);margin:.2em 0">This page follows your system</h1>
    <p class="gru-prose">Every other card in this project pins a theme so you can see both
    side by side. This one pins nothing. It is light if your computer is set to light, dark
    if it is set to dark, and it changes the moment you change that setting \u2014 no
    JavaScript, no second stylesheet, no flash of the wrong colours on load.</p>
    <div class="gru-row">
      <button class="gru-btn gru-btn--primary">Primary action</button>
      <button class="gru-btn gru-btn--secondary">Secondary</button>
      <span class="gru-badge gru-badge--success"><span class="gru-badge__dot"
        aria-hidden="true"></span>Following the system</span>
    </div>
    <div class="gru-alert gru-alert--info" role="note">
      <span class="gru-alert__icon" aria-hidden="true">i</span>
      <div class="gru-alert__body"><p style="margin:0">Set a theme only when the reader has
      asked for one. Guessing on their behalf is how a page ends up bright at midnight.</p></div>
    </div>
  </div>""", None),
     theme=None,
     notes="Three states exist and all three must be checked: <code>data-theme=\"light\"</code>, "
           "<code>data-theme=\"dark\"</code>, and \u2014 this card \u2014 <b>neither</b>, which "
           "follows <code>prefers-color-scheme</code>. The third is the default a product ships "
           "with, and it is the one most often left untested.",
     height=520)

card("patterns", "notfound", "Patterns", "A 404 page",
     "Say what happened, then offer the way out",
     full=page(f"""
  <div style="display:grid;place-items:center;min-height:26rem;padding:var(--gru-space-7);
    text-align:center">
    <div>
      <div style="color:var(--gru-border-strong);width:96px;margin:0 auto var(--gru-space-5)">
        {mark("GRU953-bird", "gru-mark nf")}</div>
      <div class="gru-eyebrow">404</div>
      <h1 style="font-size:var(--gru-text-2xl);margin:.3em 0 .4em">That page is not here</h1>
      <p class="gru-muted" style="max-width:36ch;margin:0 auto var(--gru-space-5)">
        The link may be old, or the page may have been renamed. Nothing is broken on your
        side.</p>
      <div class="gru-row" style="justify-content:center">
        <a class="gru-btn gru-btn--primary" href="#">Back to Today</a>
        <a class="gru-btn gru-btn--secondary" href="#">Search the documentation</a>
      </div>
    </div>
  </div>"""),
     notes="\"Nothing is broken on your side\" is doing real work: a 404 makes people think they "
           "typed something wrong. The mark appears here in <code>--gru-border-strong</code>, "
           "which is the one quiet use it is allowed — still an approved colour, still above "
           "its size floor, still not animated.", height=560)


# ---------------------------------------------------------------- write, or check
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify, write nothing")
    a = ap.parse_args()

    problems = []
    # Every card must carry its @dsCard marker on the FIRST line, or the index misses it.
    # This is checked against the SHELL template once rather than 27 times against strings
    # the template itself produced: `SHELL` literally begins with the marker, so a per-card
    # test could never fail and was reporting a pass it had not earned.
    if not SHELL.startswith("<!-- @dsCard group="):
        problems.append("the preview shell no longer starts with the @dsCard marker")
    for c in CARDS:
        first = c["html"].split("\n", 1)[0]
        if not first.startswith("<!-- @dsCard group="):
            problems.append(f'{c["path"]}: the @dsCard marker is not on the first line')
        # Test the actual <svg> tags, not whether the string "gru-mark" appears somewhere:
        # the stylesheet is inlined into every card and defines .gru-mark, so the old test
        # was true for every card including the one that inlines no mark at all.
        for m in re.finditer(r"<svg\b[^>]*>", c["html"]):
            if 'class="gru-mark' not in m.group(0):
                problems.append(f'{c["path"]}: a mark is inlined without the gru-mark class')
                break
    # No literal brand hex in the markup — the whole point of the system is that a
    # component never names a colour. The exception is a card whose SUBJECT is colour:
    # a swatch has to print the value it is a swatch of.
    #
    # components.css itself is linted too. Splitting the CSS away before the scan meant the
    # one file that CLAIMS to contain no literal colour was the one file never checked for
    # one — and it had four. The exemptions below are anchored to the DECLARATION, not
    # matched anywhere on the line: `TOKENFILE_OK` used to accept any line containing `/*`,
    # `@media` or `--gru-shadow`, so `.evil{color:#FF0000} /* note */` passed.
    COLOUR_RE = re.compile(
        r"#[0-9A-Fa-f]{3,8}\b|\brgba?\(|\bhsla?\(|\b(?:oklch|oklab|lab|lch|color)\("
        r"|\b(?:red|blue|green|yellow|orange|purple|pink|brown|gray|grey|cyan|magenta"
        r"|teal|navy|olive|maroon|lime|aqua|fuchsia|silver|gold|beige|ivory|salmon|coral"
        r"|khaki|indigo|violet|crimson|tomato|orchid|plum|tan|azure|rebeccapurple)\b", re.I)
    ALLOWED_DECL = re.compile(r"^\s*(?:--gru-scrim|--gru-shadow|forced-color)")
    css_src = (SRC / "components.css").read_text(encoding="utf-8")
    # Comments are removed, not exempted, so a trailing comment cannot shelter the code
    # in front of it. The blanked-out text keeps its newlines so line numbers stay true.
    css_scan = re.sub(r"/\*[\s\S]*?\*/",
                      lambda m: "\n" * m.group(0).count("\n"), css_src)
    for i, ln in enumerate(css_scan.split("\n"), 1):
        for decl in ln.split(";"):
            if COLOUR_RE.search(decl) and not ALLOWED_DECL.match(decl):
                problems.append(
                    f"src/components.css:{i}: literal colour \u2014 {ln.strip()[:60]}")
                break

    # White and the ink are the two values that are the same in both themes by definition,
    # so a card may name them. Nothing else. A third value lived on this list for a while —
    # #DDE3FF, which is not a token at all, and which coloured the one string in the whole
    # library that must never be tampered with: the Bangla tagline.
    ALLOWED = {"#FFFFFF", "#0B0E14"}
    for c in CARDS:
        if c["allow_literals"]:
            continue
        # Remove the <head> and EVERY <style> block. `split("</style>")[-1]` only skipped
        # up to the LAST one, so markup before a later style block went unscanned.
        body = re.sub(r"<style\b[\s\S]*?</style>", "", c["html"], flags=re.I)
        # An inlined mark carries its own artwork. The tile in particular has one fixed
        # colourway baked in, by design — that is not a component naming a colour.
        body = re.sub(r"<svg[\s\S]*?</svg>", "", body)
        for m in re.finditer(r"#[0-9A-Fa-f]{3,8}\b", body):
            if m.group(0).upper() not in ALLOWED:
                problems.append(f'{c["path"]}: literal colour {m.group(0)} in the markup')
    seen = set()
    for c in CARDS:
        if c["path"] in seen:
            problems.append(f'{c["path"]}: duplicate path')
        seen.add(c["path"])

    # --check has to look at the DISK. Re-validating the in-memory model it just built
    # proves only that the generator is self-consistent: a hand-edited card, a deleted
    # card and a bogus manifest entry all passed while the check printed PASS.
    if a.check:
        for c in CARDS:
            on_disk = HERE / c["path"]
            if not on_disk.exists():
                problems.append(f'{c["path"]}: listed but not on disk — run build.py')
            elif on_disk.read_text(encoding="utf-8") != c["html"]:
                problems.append(f'{c["path"]}: on disk but out of step with the source')
        wanted = {c["path"] for c in CARDS}
        for folder in ("foundations", "components", "patterns"):
            for f in sorted((HERE / folder).glob("*.html")):
                if f"{folder}/{f.name}" not in wanted:
                    problems.append(f"{folder}/{f.name}: on disk but not in the manifest")
        manifest = HERE / "_cards.json"
        if not manifest.exists():
            problems.append("_cards.json is missing — run build.py")
        elif sorted(c["path"] for c in json.loads(
                manifest.read_text(encoding="utf-8"))["cards"]) != sorted(wanted):
            problems.append("_cards.json does not list the same cards as build.py")

    if problems:
        print("FAIL — the bundle was not written:")
        for p in dict.fromkeys(problems):
            print(f"  ✗ {p}")
        sys.exit(1)

    if a.check:
        print(f"PASS — {len(CARDS)} cards, all markers correct, no literal brand colours.")
        return

    wanted = {c["path"] for c in CARDS}
    for c in CARDS:
        p = HERE / c["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(c["html"], encoding="utf-8")
    # A renamed or deleted card used to leave its old preview behind: absent from
    # _cards.json, present on disk, and still served by anything that lists the folder.
    for folder in ("foundations", "components", "patterns"):
        for f in sorted((HERE / folder).glob("*.html")):
            if f"{folder}/{f.name}" not in wanted:
                f.unlink()
                print(f"  removed stale preview {folder}/{f.name}")

    # an index for a human, and for the push guide
    index = {"project": "GRU953", "tagline": {"en": TAG_EN, "bn": TAG_BN},
             "cards": [{k: c[k] for k in ("path", "name", "group", "subtitle",
                                          "width", "height")} for c in CARDS]}
    (HERE / "_cards.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")

    groups: dict[str, int] = {}
    for c in CARDS:
        groups[c["group"]] = groups.get(c["group"], 0) + 1
    total = sum((HERE / c["path"]).stat().st_size for c in CARDS)
    print(f"{len(CARDS)} cards written, {total / 1048576:.1f} MB total")
    for g, n in groups.items():
        print(f"  {g:14s} {n} cards")
    print("\n_cards.json lists every path, for the push step.")


if __name__ == "__main__":
    main()
