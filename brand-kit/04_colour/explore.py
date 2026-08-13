#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Signature-colour exploration, against a hard dual-theme constraint.

THE BRIEF: the signature colours must be visually compatible with light AND dark themes on
any digital platform, explored widely, and adopted only if they clearly beat what exists.

THE MATHS, FIRST — because it rules out the obvious answer.

WCAG contrast is (L1+0.05)/(L2+0.05) on relative luminance. For a colour to reach 4.5:1
against white (L=1.0) it needs luminance <= 0.1833. To reach 4.5:1 against the near-black
ink #0B0E14 (L=0.00436) it needs luminance >= 0.1946. Those cannot both be true.

    ==> NO single colour can serve as body text on both a white and a near-black ground.

At the 3:1 threshold — which is what WCAG requires for large text, icons, focus rings and
UI parts — the window is real: luminance between about 0.113 and 0.300. The script solves
both bounds rather than quoting them, so they cannot drift.

So a genuinely dual-theme signature is one of two things:
  (A) a single colour inside that narrow 3:1 window, usable for large text and UI on both
      grounds but never for body text on both; or
  (B) ONE hue with TWO tuned values, light-theme and dark-theme, which is what every serious
      design system actually ships.

This script tests candidates for both, measures distinctiveness against real brand colours,
and renders the survivors applied to a page in both themes.

Run:  python3 04_colour/explore.py
"""
from coloraide import Color
import json, pathlib

INK, PAPER = "#0B0E14", "#FFFFFF"

# Colours already owned by brands a developer audience actually sees.
OCCUPIED = {
    "Anthropic": "#D97757", "Stripe": "#635BFF", "Linear": "#5E6AD2", "Vercel": "#000000",
    "GitHub": "#0969DA", "Figma": "#F24E1E", "Spotify": "#1DB954", "Supabase": "#3ECF8E",
    "Slack aubergine": "#4A154B", "Notion": "#191919", "Docker": "#2496ED",
    "Tailwind sky": "#0EA5E9", "Tailwind amber": "#FBBF24", "Tailwind rose": "#F43F5E",
    "Tailwind emerald": "#10B981", "Tailwind violet": "#8B5CF6", "Mailchimp": "#FFE01B",
    "Heroku": "#430098", "MongoDB": "#00684A", "Postgres": "#336791", "Rust": "#CE422B",
    "Python blue": "#3776AB", "Go cyan": "#00ADD8", "Kotlin": "#7F52FF",
}


def lum(c):
    return Color(c).luminance()


def K(a, b):
    return round(Color(a).contrast(b), 2)


def dE(a, b):
    return round(Color(a).delta_e(b, method="2000"), 1)


def nearest(hx, n=1):
    d = sorted((dE(hx, v), k) for k, v in OCCUPIED.items())
    return d[:n]


def ok(l, c, h):
    return (Color("oklch", [l, c, h]).convert("srgb")
            .fit("srgb", method="oklch-chroma").to_string(hex=True).upper())


def dual_window():
    """The luminance band where a single colour clears 3:1 on BOTH grounds."""
    lo = 3.0 * (lum(INK) + 0.05) - 0.05
    hi = (1.0 + 0.05) / 3.0 - 0.05
    return lo, hi


LO, HI = dual_window()

# ---------------------------------------------------------------- the territories
# Explored widely, as asked: deep grounds, light grounds, near-monochrome, and colours
# rooted in Bangladesh. Each entry is a candidate IDENTITY — one hue, expressed as a ground,
# a light-theme accent and a dark-theme accent drawn from the same hue.
TERRITORIES = [
    # name,            ground L,C,H       accent hue, note
    ("Meridian · Daybreak", (0.255, 0.105, 278), 38,
     "The incumbent. Deep indigo ground, warm dawn accent."),
    ("Teal · Ember",        (0.290, 0.070, 205), 70,
     "Deep sea-teal ground with a warm ember. Cooler, more instrument-like."),
    ("Ink · Signal",        (0.220, 0.030, 265), 250,
     "Near-monochrome ground, one high-voltage blue signal. Maximum restraint."),
    ("Delta · Silt",        (0.300, 0.055, 165), 75,
     "River-green ground, alluvial ochre. Rooted in Bangladesh without cliché."),
    ("Aubergine · Marigold",(0.260, 0.095, 330), 85,
     "Deep aubergine with a marigold — the flower, not the mustard."),
    ("Slate · Kingfisher",  (0.275, 0.045, 250), 220,
     "Cool slate ground with a kingfisher blue-green. A bird's own colour."),
    ("Paper · Meridian",    (0.985, 0.004, 278), 278,
     "A LIGHT ground identity: near-white paper, the indigo itself as the accent."),
    ("Clay · Deepwater",    (0.955, 0.012, 60), 240,
     "Warm pale clay ground with a deep water accent. Light-first, warm."),
]

rows = []
for name, ground, accent_hue, note in TERRITORIES:
    g = ok(*ground)
    ground_is_light = lum(g) > 0.4

    # (A) one value inside the dual 3:1 window — solve lightness to land mid-window
    dual = None
    best = None
    for step in range(2, 90):
        l = step / 100
        cand = ok(l, 0.13, accent_hue)
        if LO <= lum(cand) <= HI:
            score = abs(lum(cand) - (LO + HI) / 2)
            if best is None or score < best[0]:
                best = (score, cand)
    dual = best[1] if best else None

    # (B) one hue, two tuned values — the design-system answer
    light_v = next((ok(l / 100, 0.14, accent_hue) for l in range(90, 20, -1)
                    if K(ok(l / 100, 0.14, accent_hue), PAPER) >= 4.55), None)
    dark_v = next((ok(l / 100, 0.14, accent_hue) for l in range(20, 100)
                   if K(ok(l / 100, 0.14, accent_hue), INK) >= 4.55), None)

    rows.append(dict(
        name=name, note=note, ground=g, ground_is_light=ground_is_light,
        dual=dual,
        dual_on_paper=K(dual, PAPER) if dual else None,
        dual_on_ink=K(dual, INK) if dual else None,
        light_accent=light_v, light_ratio=K(light_v, PAPER) if light_v else None,
        dark_accent=dark_v, dark_ratio=K(dark_v, INK) if dark_v else None,
        text_on_ground=K(PAPER if not ground_is_light else INK, g),
        nearest_ground=nearest(g)[0], nearest_dual=nearest(dual)[0] if dual else None,
    ))

print(f"The dual-theme 3:1 window is luminance {LO:.3f} to {HI:.3f}\n")
print(f"{'identity':22s} {'ground':9s} {'dual 3:1':9s} {'pap':>5s} {'ink':>5s} "
      f"{'light 4.5':9s} {'dark 4.5':9s}  nearest brand to the ground")
print("-" * 122)
for r in rows:
    print(f"{r['name']:22s} {r['ground']:9s} {str(r['dual'] or '—'):9s} "
          f"{r['dual_on_paper'] or 0:5.2f} {r['dual_on_ink'] or 0:5.2f} "
          f"{str(r['light_accent'] or '—'):9s} {str(r['dark_accent'] or '—'):9s}  "
          f"{r['nearest_ground'][1]} ΔE{r['nearest_ground'][0]}")

pathlib.Path("exploration.json").write_text(json.dumps(rows, indent=1))
print("\nwrote exploration.json")
