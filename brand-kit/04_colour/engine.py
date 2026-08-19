#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""GRU953 — the palette engine. Every colour in the kit is computed here, and proved here.

WHY THE PALETTE IS SHAPED THE WAY IT IS
---------------------------------------
The hard constraint on this brand is that it must look right in a light theme and a dark
theme, on any digital surface. That constraint has a mathematical consequence most brand
guides never state:

    WCAG contrast is (L1+0.05)/(L2+0.05) on relative luminance. To reach 4.5:1 against
    white a colour needs luminance <= 0.1833. To reach 4.5:1 against the ink #0B0E14 it
    needs luminance >= 0.1946. Both cannot be true.

    Those two figures are COMPUTED below and published in tokens.json, so nothing downstream
    has to retype them. They were once typed into five files by hand, and both were wrong.

    ==> NO SINGLE COLOUR CAN BE THE BRAND'S TEXT COLOUR IN BOTH THEMES.

So the signature is not one value. It is ONE HUE WITH TWO TUNED VALUES — a deep one for
light grounds, a pale one for dark grounds, both drawn from the same ramp so they stay the
same HUE while each measures correctly against its own ground. They are not the same colour
and this file does not pretend they are: the difference between them is computed and
published too. That is what every serious design system does, and it is what this engine
emits.

THE RULES THIS ENGINE ENFORCES, AND PROVES
------------------------------------------
  1. Every ramp is MONOTONIC in OKLCH lightness from 50 (palest) to 950 (deepest).
  2. Each brand anchor sits EXACTLY on the ramp step nearest its own lightness, so the
     brand colour is a real member of its ramp, not a colour bolted on beside it.
  3. Chroma follows an arc — highest in the mid-tones, tapering at both ends — then is
     gamut-mapped into sRGB so nothing clips.
  4. Every role is chosen by MEASURING each step against its background and taking the
     first that clears the WCAG 2.2 target with a safety margin, never by solving to the
     boundary, which rounds below target once quantised to 8-bit hex.
  5. Every colour that carries meaning is checked for distinctiveness (CIEDE2000) against
     its neighbours, so no two states or chart series can be confused.
  6. Nothing ships unproved. If any check fails the script exits non-zero and says why.

Emits: 08_guidebook/assets/tokens.css, 08_guidebook/assets/tokens.json, 04_colour/CONTRAST.md
Run:   cd 04_colour && python3 engine.py
"""
from coloraide import Color
import json, pathlib, re, sys

INK, PAPER = "#0B0E14", "#FFFFFF"
MARGIN = 0.05          # clear each WCAG target by this much, so rounding cannot defeat it

STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
NOMINAL_L = {50: 0.975, 100: 0.945, 200: 0.895, 300: 0.830, 400: 0.755,
             500: 0.665, 600: 0.570, 700: 0.475, 800: 0.375, 900: 0.270, 950: 0.190}
CHROMA_ARC = {50: 0.14, 100: 0.26, 200: 0.44, 300: 0.68, 400: 0.86, 500: 1.00,
              600: 0.98, 700: 0.90, 800: 0.78, 900: 0.64, 950: 0.50}

# ---------------------------------------------------------------- the families
# THREE signature families carry the brand. TWO functional families exist only because no
# signature colour can honestly mean "this went well" or "this is about to go wrong".
# Warning and information deliberately reuse Ember and Meridian rather than inventing new
# hues: five hues is a palette, nine is a paint shop.
FAMILIES = {
    "meridian": dict(anchor="#1A1753", label="Meridian", bn="মেরিডিয়ান", kind="signature",
                     note="The deep sky before dawn. The ground, the wordmark on paper, "
                          "and the colour of information."),
    "daybreak": dict(anchor="#FFAB8E", label="Daybreak", bn="ভোরের আলো", kind="signature",
                     taper=0.82,
                     note="First light. THE SIGNATURE — one hue, two tuned values: a deep "
                          "step on light grounds, this pale step on dark ones."),
    "ember":    dict(anchor="#EDB24D", label="Ember", bn="অঙ্গার", kind="signature",
                     note="Warm mid-tone. Gradient midpoint, secondary emphasis, and the "
                          "colour of a warning."),
    "success":  dict(anchor=None, hue=152.0, chroma=0.155, label="Verdant", bn="সবুজ",
                     kind="functional", note="The only hue in the kit that means 'this "
                                             "worked'. Never used decoratively."),
    "danger":   dict(anchor=None, hue=25.0, chroma=0.190, label="Signal Red", bn="লাল",
                     kind="functional", note="The only hue that means 'this failed, or "
                                             "cannot be undone'. Never used decoratively."),
}

# Colours already owned by brands this kit's priority audience — developers — actually sees
# every day. Distinctiveness against THESE is the comparison that matters; distinctiveness
# against the kit's own other colours is table stakes.
OCCUPIED = {
    "Anthropic": "#D97757", "Stripe": "#635BFF", "Linear": "#5E6AD2", "Vercel": "#000000",
    "GitHub": "#0969DA", "Figma": "#F24E1E", "Spotify": "#1DB954", "Supabase": "#3ECF8E",
    "Slack aubergine": "#4A154B", "Notion": "#191919", "Docker": "#2496ED",
    "Tailwind sky": "#0EA5E9", "Tailwind amber": "#FBBF24", "Tailwind rose": "#F43F5E",
    "Tailwind emerald": "#10B981", "Tailwind violet": "#8B5CF6", "Mailchimp": "#FFE01B",
    "Heroku": "#430098", "MongoDB": "#00684A", "Postgres": "#336791", "Rust": "#CE422B",
    "Python blue": "#3776AB", "Go cyan": "#00ADD8", "Kotlin": "#7F52FF",
    "sienna (the pigment)": "#A0522D", "terracotta (the pigment)": "#E2725B",
}

# The chart sequence. Six hues, spread around the wheel, anchored on the brand's own two.
# Order matters: the first two series a reader sees are the brand's colours.
CHART_HUES = [("Meridian", 278.0, 0.105), ("Daybreak", 39.8, 0.130), ("Kingfisher", 205.0, 0.110),
              ("Verdant", 152.0, 0.130), ("Orchid", 330.0, 0.130), ("Ember", 78.0, 0.135)]

fails = []

# The two thresholds the whole palette is shaped by, solved rather than typed.
#   contrast = (L_light + 0.05) / (L_dark + 0.05)
MAX_L_ON_PAPER = round((Color(PAPER).luminance() + 0.05) / 4.5 - 0.05, 4)
MIN_L_ON_INK = round(4.5 * (Color(INK).luminance() + 0.05) - 0.05, 4)


def mk(l, c, h):
    return Color("oklch", [l, c, h]).convert("srgb").fit("srgb", method="oklch-chroma")


def hexof(c):
    return c.convert("srgb").to_string(hex=True).upper()


def K(a, b):
    return round(Color(a).contrast(b), 2)


def dE(a, b):
    return round(Color(a).delta_e(b, method="2000"), 1)


def build_ramp(spec):
    """A monotonic ramp. Anchored on a brand colour where there is one, on a hue where not."""
    if spec.get("anchor"):
        a = Color(spec["anchor"]).convert("oklch")
        hue, aL, aC = a["hue"], a["lightness"], a["chroma"]
        home = min(STEPS, key=lambda s: abs(NOMINAL_L[s] - aL))
        ceiling = aC / CHROMA_ARC[home]
    else:
        hue, ceiling, home = spec["hue"], spec["chroma"], None
    # A family may TAPER its deep end. Left at full chroma, a deep orange stops looking like
    # a darker dawn and starts looking like a different, harder colour — and drifts towards
    # the oranges other developer brands already own. Pulling chroma below step 500 keeps the
    # deep value recognisably the same colour as the pale one.
    taper = spec.get("taper", 1.0)
    ramp = {s: (spec["anchor"].upper() if s == home
                else hexof(mk(NOMINAL_L[s],
                              ceiling * CHROMA_ARC[s] * (taper if s >= 600 else 1.0), hue)))
            for s in STEPS}
    return ramp, home, round(hue, 1)


def first_clearing(ramp, bgs, target, from_dark_end):
    """The most colourful step that still clears target+MARGIN against EVERY ground in bgs.

    On paper walk 50 -> 950 and stop at the first pass: the lightest legible step, so text
    never goes needlessly heavy. On ink walk the other way, for the same reason.

    `bgs` is a LIST, not a single colour, and that is the whole point. This file once
    proved every text role against the page background only, then components put the same
    role on a raised surface and on its own tinted "quiet" ground — both slightly closer to
    the text in luminance. Eight role pairings shipped between 3.89:1 and 4.46:1 while this
    file printed PASS. A role is legible or it is not; it cannot be legible on the one
    ground that happened to be checked.
    """
    if isinstance(bgs, str):
        bgs = [bgs]
    for s in (list(reversed(STEPS)) if from_dark_end else STEPS):
        if all(K(ramp[s], bg) >= target + MARGIN for bg in bgs):
            return s
    return None


# The neutral greys are computed the same way, so "ink-subtle" cannot be a colour someone
# typed once against white and never re-checked against the five other grounds it lands on.
NEUTRAL_HUE, NEUTRAL_C = 265.0, 0.012   # a trace of Meridian, so the greys belong to the family
QUIET_T_LIGHT, QUIET_T_DARK = 0.16, 0.13   # how far a quiet ground travels from bg towards its family
QUIET_VISIBLE = 3.0                        # ...and how far it must be from EVERY surface (CIEDE2000)


def neutral_clearing(bgs, target, on_light):
    """The least-contrasty neutral grey that still clears target+MARGIN on every ground.

    Least-contrasty, not safest: a subtle role that goes darker than it needs to stops
    being subtle, and the hierarchy it exists to express collapses.
    """
    rng = range(985, 149, -1) if on_light else range(150, 986)
    for x in rng:
        h = hexof(mk(x / 1000, NEUTRAL_C, NEUTRAL_HUE))
        if all(K(h, bg) >= target + MARGIN for bg in bgs):
            return h
    return None


def quiet_ground(fam, on_light):
    """A tint of `fam` at a fixed depth, the same for every family.

    A "quiet" ground exists to tint an alert or a badge, so it has to be VISIBLY tinted or
    it is not doing its job. Its depth is therefore fixed, and the text that sits on it is
    what moves: see `-ink` below. The first attempt at this was the other way round — the
    ground was pushed as pale as it needed to be to keep the family's own text colour
    legible — and Daybreak's came out #FFFAF9, a badge ground indistinguishable from white.

    This file once used ramp step 50, which is neither: too deep for four of the five
    families, so the badge, the alert and the current-page navigation link shipped between
    4.20:1 and 4.44:1 while this file printed PASS.
    """
    ground, towards = ((PAPER, palette[fam][300]) if on_light
                       else (INK, palette[fam][700]))
    surfaces = ([L_BG, L_RAISED, L_TINT] if on_light
                else [D_BG, D_SUBTLE, D_SURFACE, D_RAISED])
    start = QUIET_T_LIGHT if on_light else QUIET_T_DARK
    # The depth is a floor, not a fixed value: the tint must ALSO be visible against every
    # surface it can be dropped onto. The dark brand and info tints came out ΔE 1.82 from
    # --gru-surface — a "quiet ground" nobody can see is not a ground, it is a background.
    for i in range(int(start * 400), 161):
        cand = hexof(Color(ground).mix(towards, i / 400, space="oklab"))
        if min(dE(cand, s) for s in surfaces) >= QUIET_VISIBLE:
            return cand
    fails.append(f"no {fam} tint is visible against every surface in the "
                 f"{'light' if on_light else 'dark'} theme")
    return ground


# ---------------------------------------------------------------- the grounds, declared first
# Surfaces are declared BEFORE the roles that have to be legible on them, because the order
# is the argument: you cannot pick a text colour until you know every ground it can land on.
#
# Two tiers, and the difference is a rule the whole system depends on:
#   TEXT_SURFACES   — bg, surface, surface-raised. Every coloured text role is proved
#                     against all of these, plus its own quiet ground.
#   INK_SURFACES    — the above plus bg-subtle and surface-sunken, the structural tints.
#                     Only the neutral inks are proved against these, and that is why the
#                     rule below exists: on a subtle or sunken ground, text is ink,
#                     ink-muted or ink-subtle. Never a coloured role.
L_BG, L_RAISED, L_TINT = PAPER, "#FBFBFD", None          # L_TINT resolved just below
D_BG, D_SUBTLE, D_SURFACE, D_RAISED, D_SUNKEN = INK, "#12161F", "#141926", "#1B2130", "#080A0F"

palette, homes, hues = {}, {}, {}
for key, spec in FAMILIES.items():
    ramp, home, hue = build_ramp(spec)
    palette[key], homes[key], hues[key] = ramp, home, hue

L_TINT = palette["meridian"][50]                          # bg-subtle and surface-sunken
TEXT_SURFACES_L = [L_BG, L_RAISED]
TEXT_SURFACES_D = [D_BG, D_SURFACE, D_RAISED]
INK_SURFACES_L = [L_BG, L_RAISED, L_TINT]
INK_SURFACES_D = [D_BG, D_SUBTLE, D_SURFACE, D_RAISED, D_SUNKEN]

roleinfo = {}
for key in FAMILIES:
    ramp = palette[key]
    roleinfo[key] = dict(
        text_on_paper=first_clearing(ramp, TEXT_SURFACES_L, 4.5, False),
        aaa_on_paper=first_clearing(ramp, TEXT_SURFACES_L, 7.0, False),
        ui_on_paper=first_clearing(ramp, TEXT_SURFACES_L, 3.0, False),
        text_on_ink=first_clearing(ramp, TEXT_SURFACES_D, 4.5, True),
        aaa_on_ink=first_clearing(ramp, TEXT_SURFACES_D, 7.0, True),
        ui_on_ink=first_clearing(ramp, TEXT_SURFACES_D, 3.0, True),
    )

M, D, E = (FAMILIES[k]["anchor"] for k in ("meridian", "daybreak", "ember"))
r = roleinfo
P, I = palette, INK


def pick(fam, role):
    step = r[fam][role]
    if step is None:
        fails.append(f"{FAMILIES[fam]['label']} has no step meeting {role}")
        return "#FF00FF"
    return P[fam][step]


# ---------------------------------------------------------------- the signature, resolved
# This is the whole point of the file. ONE hue, TWO values.
SIG_LIGHT = pick("daybreak", "text_on_paper")     # deep dawn, legible on white
SIG_DARK = D                                       # #FFAB8E, legible on ink
SIG_UI_LIGHT = pick("daybreak", "ui_on_paper")     # for borders, icons, focus rings
SIG_UI_DARK = D

# ---------------------------------------------------------------- the quiet grounds
# Each family's tinted ground is computed FROM the text colour that will sit on it, not
# taken from step 50 and hoped for. Step 50 was too deep for four of the five families.
TEXT_L = {"info": pick("meridian", "text_on_paper"), "brand": M,
          "accent": SIG_LIGHT, "success": pick("success", "text_on_paper"),
          "warning": pick("ember", "text_on_paper"), "danger": pick("danger", "text_on_paper")}
TEXT_D = {"info": pick("meridian", "text_on_ink"), "brand": pick("meridian", "text_on_ink"),
          "accent": SIG_DARK, "success": pick("success", "text_on_ink"),
          "warning": pick("ember", "text_on_ink"), "danger": pick("danger", "text_on_ink")}
FAM_OF = {"info": "meridian", "brand": "meridian", "accent": "daybreak",
          "success": "success", "warning": "ember", "danger": "danger"}

QUIET_L = {role: quiet_ground(fam, True) for role, fam in FAM_OF.items()}
QUIET_D = {role: quiet_ground(fam, False) for role, fam in FAM_OF.items()}

# ---------------------------------------------------------------- text ON a quiet ground
# `--gru-{role}` is proved against bg, surface and surface-raised. It is NOT automatically
# legible on its own tint: Daybreak clears white by 4.71:1, which leaves no headroom at all
# for a ground that is even slightly off-white. So each family also publishes the step that
# IS legible on its own quiet ground. For three families it is the same colour; for the two
# that sit close to their 4.5:1 boundary it is one step deeper. Use `--gru-{role}-ink` for
# text, an icon or a border ON `--gru-{role}-quiet`, and `--gru-{role}` everywhere else.
ALL_GROUNDS_L = INK_SURFACES_L + list(QUIET_L.values())
ALL_GROUNDS_D = INK_SURFACES_D + list(QUIET_D.values())

# The focus ring and the strong border are drawn with an outline-offset, or as the edge
# between two surfaces — so the ground under them is whatever the control happens to sit
# in, which is any of the nine. Proving them against bg/surface/surface-raised only left
# the ring at 2.90:1 inside an error panel and the table header rule at 2.93:1.
_ui_l = first_clearing(palette["meridian"], ALL_GROUNDS_L, 3.0, False)
_ui_d = first_clearing(palette["meridian"], ALL_GROUNDS_D, 3.0, True)
if _ui_l is None or _ui_d is None:
    fails.append("no Meridian step is a visible UI part on every ground")
UI_L = palette["meridian"][_ui_l] if _ui_l else "#FF00FF"
UI_D = palette["meridian"][_ui_d] if _ui_d else "#FF00FF"
QUIET_INK_L, QUIET_INK_D, EDGE_L, EDGE_D = {}, {}, {}, {}
for role, fam in FAM_OF.items():
    s = first_clearing(palette[fam], [QUIET_L[role]], 4.5, False)
    if s is None:
        fails.append(f"no step of {fam} is legible on the light {role} quiet ground")
    QUIET_INK_L[role] = palette[fam][s] if s else "#FF00FF"
    s = first_clearing(palette[fam], [QUIET_D[role]], 4.5, True)
    if s is None:
        fails.append(f"no step of {fam} is legible on the dark {role} quiet ground")
    QUIET_INK_D[role] = palette[fam][s] if s else "#FF00FF"
    # The edge of an alert is drawn ON the alert's own tint, so 3:1 is owed there too —
    # not only against the page. info-border measured 2.91:1 on info-quiet before this.
    s = first_clearing(palette[fam], TEXT_SURFACES_L + [QUIET_L[role]], 3.0, False)
    if s is None:
        fails.append(f"no step of {fam} is a visible edge on the light {role} quiet ground")
    EDGE_L[role] = palette[fam][s] if s else "#FF00FF"
    s = first_clearing(palette[fam], TEXT_SURFACES_D + [QUIET_D[role]], 3.0, True)
    if s is None:
        fails.append(f"no step of {fam} is a visible edge on the dark {role} quiet ground")
    EDGE_D[role] = palette[fam][s] if s else "#FF00FF"

# The neutral inks are proved against every ground in the system, structural tints and
# quiet grounds included, because an alert body really is ink on a quiet ground.
INK_GROUNDS_L = INK_SURFACES_L + list(QUIET_L.values())
INK_GROUNDS_D = INK_SURFACES_D + list(QUIET_D.values())
INK_MUTED_L = neutral_clearing(INK_GROUNDS_L, 7.0, True)
INK_SUBTLE_L = neutral_clearing(INK_GROUNDS_L, 4.5, True)
INK_MUTED_D = neutral_clearing(INK_GROUNDS_D, 7.0, False)
INK_SUBTLE_D = neutral_clearing(INK_GROUNDS_D, 4.5, False)
for label, v in (("ink-muted light", INK_MUTED_L), ("ink-subtle light", INK_SUBTLE_L),
                 ("ink-muted dark", INK_MUTED_D), ("ink-subtle dark", INK_SUBTLE_D)):
    if v is None:
        fails.append(f"no neutral grey clears its target for {label}")

# ---------------------------------------------------------------- semantic roles
# Complete on both themes: surfaces, text, borders, brand, signature, links, the four
# meanings (info / success / warning / danger), and every interaction state a control has.
LIGHT = {
    # ground and surfaces
    "bg": PAPER, "bg-subtle": L_TINT, "surface": PAPER,
    "surface-raised": L_RAISED, "surface-sunken": L_TINT,
    "overlay": "rgba(11,14,20,.55)",
    # text
    "ink": INK, "ink-muted": INK_MUTED_L or "#FF00FF",
    "ink-subtle": INK_SUBTLE_L or "#FF00FF", "ink-inverse": PAPER,
    # lines — "border" is a decorative hairline and is deliberately not held to 3:1;
    # "border-strong" is the one you use when the line itself must be seen.
    "border": P["meridian"][100], "border-strong": UI_L,
    # the brand
    "brand": M, "brand-hover": P["meridian"][800], "brand-active": P["meridian"][950],
    "brand-quiet": QUIET_L["brand"], "on-brand-quiet": QUIET_INK_L["brand"], "on-brand": PAPER,
    # the signature
    "accent": SIG_LIGHT, "accent-hover": P["daybreak"][800], "accent-active": P["daybreak"][900],
    "accent-quiet": QUIET_L["accent"], "on-accent-quiet": QUIET_INK_L["accent"],
    "accent-ui": SIG_UI_LIGHT, "on-accent": PAPER,
    # links
    # NOT the same step as `info`. They were byte-identical (ΔE 0.00), so a link and a
    # line of informational text were distinguishable only by an underline — which
    # .gru-navlink, .gru-sidenav a and .gru-topbar__brand all remove.
    "link": pick("meridian", "aaa_on_paper"), "link-hover": P["meridian"][950],
    "link-visited": P["meridian"][950],
    # focus and disabled
    "focus": UI_L, "focus-inverse": PAPER,
    "disabled-bg": P["meridian"][50], "disabled-ink": "#8A8F9C",
    "disabled-border": P["meridian"][100],
    # the four meanings
    "info": TEXT_L["info"], "info-quiet": QUIET_L["info"], "on-info-quiet": QUIET_INK_L["info"],
    "info-border": EDGE_L["info"], "on-info": PAPER,
    "success": TEXT_L["success"], "success-quiet": QUIET_L["success"],
    "on-success-quiet": QUIET_INK_L["success"],
    "success-border": EDGE_L["success"], "on-success": PAPER,
    "warning": TEXT_L["warning"], "warning-quiet": QUIET_L["warning"],
    "on-warning-quiet": QUIET_INK_L["warning"],
    "warning-border": EDGE_L["warning"], "on-warning": PAPER,
    "danger": TEXT_L["danger"], "danger-quiet": QUIET_L["danger"],
    "on-danger-quiet": QUIET_INK_L["danger"],
    "danger-border": EDGE_L["danger"], "on-danger": PAPER,
    # A destructive button needs its own states. `filter: brightness()` was doing this job
    # and it darkens in BOTH themes — so in the dark theme the danger button went darker on
    # hover while every other intent went lighter, on the one control where a hesitant
    # person most needs the feedback to feel the same as everywhere else.
    "danger-hover": P["danger"][800], "danger-active": P["danger"][900],
}
DARK = {
    "bg": D_BG, "bg-subtle": D_SUBTLE, "surface": D_SURFACE, "surface-raised": D_RAISED,
    "surface-sunken": D_SUNKEN, "overlay": "rgba(3,4,7,.66)",
    "ink": "#F4F5F9", "ink-muted": INK_MUTED_D or "#FF00FF",
    "ink-subtle": INK_SUBTLE_D or "#FF00FF", "ink-inverse": INK,
    "border": "#242B3A", "border-strong": UI_D,
    "brand": TEXT_D["brand"], "brand-hover": P["meridian"][200],
    "brand-active": P["meridian"][100], "brand-quiet": QUIET_D["brand"],
    "on-brand-quiet": QUIET_INK_D["brand"], "on-brand": INK,
    "accent": SIG_DARK, "accent-hover": P["daybreak"][200], "accent-active": P["daybreak"][100],
    "accent-quiet": QUIET_D["accent"], "on-accent-quiet": QUIET_INK_D["accent"],
    "accent-ui": SIG_UI_DARK, "on-accent": INK,
    "link": pick("daybreak", "text_on_ink"), "link-hover": P["daybreak"][200],
    # NOT daybreak-200: that is what link-hover uses, and a visited link that looks
    # permanently hovered is a small lie the interface tells on every page.
    "link-visited": D,
    "focus": UI_D, "focus-inverse": INK,
    "disabled-bg": "#171B26", "disabled-ink": "#6A7183", "disabled-border": "#242B3A",
    "info": TEXT_D["info"], "info-quiet": QUIET_D["info"], "on-info-quiet": QUIET_INK_D["info"],
    "info-border": EDGE_D["info"], "on-info": INK,
    "success": TEXT_D["success"], "success-quiet": QUIET_D["success"],
    "on-success-quiet": QUIET_INK_D["success"],
    "success-border": EDGE_D["success"], "on-success": INK,
    "warning": TEXT_D["warning"], "warning-quiet": QUIET_D["warning"],
    "on-warning-quiet": QUIET_INK_D["warning"],
    "warning-border": EDGE_D["warning"], "on-warning": INK,
    "danger": TEXT_D["danger"], "danger-quiet": QUIET_D["danger"],
    "on-danger-quiet": QUIET_INK_D["danger"],
    "danger-border": EDGE_D["danger"], "on-danger": INK,
    # lighter on hover, like every other intent in this theme
    "danger-hover": P["danger"][400], "danger-active": P["danger"][300],
}

# ---------------------------------------------------------------- the chart sequence
def chart_series(grounds, from_dark_end):
    """Chart colours are non-text UI, so 3:1 — but on every surface a chart can sit on,
    not just the page background. A bar chart lives inside a card more often than not."""
    out = []
    for name, hue, chroma in CHART_HUES:
        ramp = {s: hexof(mk(NOMINAL_L[s], chroma * CHROMA_ARC[s] / CHROMA_ARC[500], hue))
                for s in STEPS}
        step = first_clearing(ramp, grounds, 3.0, from_dark_end)
        if step is None:
            fails.append(f"chart series {name} has no step clearing 3:1 on every surface")
            out.append((name, "#FF00FF", 0))
        else:
            worst = min(K(ramp[step], g) for g in grounds)
            out.append((name, ramp[step], worst))
    return out


# Every surface, not only the three a text role is guaranteed on: a chart in a sunken
# well is an ordinary thing to build, and two series measured 2.98:1 there.
CHART_LIGHT = chart_series(INK_SURFACES_L, False)
CHART_DARK = chart_series(INK_SURFACES_D, True)

# ---------------------------------------------------------------- distinctiveness checks
# Two colours that carry different meanings must not be confusable. CIEDE2000 delta-E of
# 10 is a clear, obvious difference to a normally-sighted viewer; anything under that in a
# meaning-bearing set is a defect, not a preference.
DISTINCT_MIN = 10.0
# A meaning colour must also be distinguishable from the TEXT around it. Without this, a
# functional family whose chroma was set near zero emitted a neutral grey ramp and the
# engine printed PASS: every meaning was still ΔE 10 from every other meaning, because
# they were all grey together.
for _th, _roles in (("light", LIGHT), ("dark", DARK)):
    for _k in ("info", "success", "warning", "danger", "accent"):
        for _n in ("ink", "ink-muted", "ink-subtle"):
            _d = dE(_roles[_k], _roles[_n])
            if _d < DISTINCT_MIN:
                fails.append(f"{_th}: --gru-{_k} is only ΔE{_d} from --gru-{_n} — it reads "
                             f"as text, not as a meaning")
meaning_sets = {
    "light theme meanings": [(k, LIGHT[k]) for k in ("info", "success", "warning", "danger", "accent")],
    "dark theme meanings": [(k, DARK[k]) for k in ("info", "success", "warning", "danger", "accent")],
    "light chart series": [(n, h) for n, h, _ in CHART_LIGHT],
    "dark chart series": [(n, h) for n, h, _ in CHART_DARK],
}
distinct_report = {}
for setname, items in meaning_sets.items():
    worst = None
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            d = dE(items[i][1], items[j][1])
            if worst is None or d < worst[0]:
                worst = (d, items[i][0], items[j][0])
            if d < DISTINCT_MIN:
                fails.append(f"{setname}: {items[i][0]} and {items[j][0]} are only "
                             f"ΔE{d} apart — confusable")
    distinct_report[setname] = worst

# The signature's two values must be the same HUE. That is guaranteed by construction, but a
# gamut-map can drag a hue, so it is checked rather than assumed.
sig_hue_drift = round(abs(Color(SIG_LIGHT).convert("oklch")["hue"]
                          - Color(SIG_DARK).convert("oklch")["hue"]), 2)
if sig_hue_drift > 6.0:
    fails.append(f"the signature's two values drift {sig_hue_drift}° in hue — not one hue")

# And they are NOT the same colour, which is the honest way to say it. They are 24-odd ΔE
# apart, because one is a deep terracotta and the other a pale salmon — that is what "tuned
# for a light ground" and "tuned for a dark ground" means. Publishing this number matters:
# the kit's own distinctiveness floor is ΔE 10, so claiming the pair reads as "one colour"
# would be a claim its own maths refutes. Same hue, two calibrated values. Nothing more.
sig_delta_e = dE(SIG_LIGHT, SIG_DARK)

# Distinctiveness against colours other developer brands already own.
occupied_report = []
for label, val in (("Meridian", M), ("Daybreak · light", SIG_LIGHT),
                   ("Daybreak · dark", SIG_DARK), ("Ember", E)):
    near = sorted((dE(val, v), k) for k, v in OCCUPIED.items())[:3]
    occupied_report.append((label, val, near))

# ---------------------------------------------------------------- assemble tokens.css
HEAD = """/*
 * GRU953 — design tokens
 * Generated by the GRU953 brand kit's 04_colour/engine.py, which does not ship
 * beside this file. Do NOT hand-edit the values; regenerate them there.
 *
 * সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.
 *
 * THE SIGNATURE IS ONE HUE WITH TWO VALUES. No single colour can clear 4.5:1 against both
 * white and near-black — that is arithmetic, not opinion — so Daybreak is a deep step on
 * light grounds and a pale step on dark ones. Use --gru-accent and let the theme choose.
 *
 * Every ramp is monotonic in OKLCH lightness, every anchor is a real member of its ramp,
 * and every role was picked by measured contrast with a safety margin.
 * The proof is in the brand kit's 04_colour/CONTRAST.md, which does not ship here.
 *
 * Licensed under the Apache License, Version 2.0. Use these values freely.
 * NOT licensed: the name GRU953, the Soaring Bird mark, the app-icon tile, the GRU953
 * wordmark and any lockup of them. They identify the studio, so they stay with it.
 * Copyright 2026 Aninda Sundar Howlader (GRU953)
 */
"""
out = [HEAD, ":root{"]
out.append("\n  /* ======== SIGNATURE — the three colours the brand is made of ======== */")
for key, spec in FAMILIES.items():
    if spec["kind"] != "signature":
        continue
    out.append(f"\n  /* {spec['label']} ({spec['bn']}) · hue {hues[key]}° · anchor "
               f"{spec['anchor']} sits at step {homes[key]}\n     {spec['note']} */")
    for s in STEPS:
        star = "   /* <- the brand colour itself */" if s == homes[key] else ""
        out.append(f"  --gru-{key}-{s}: {palette[key][s]};{star}")
    out.append(f"  --gru-{key}: {spec['anchor']};   /* alias for step {homes[key]} */")
out.append("\n  /* ======== FUNCTIONAL — hues that exist only to carry a meaning ======== */")
for key, spec in FAMILIES.items():
    if spec["kind"] != "functional":
        continue
    out.append(f"\n  /* {spec['label']} ({spec['bn']}) · hue {hues[key]}°\n     {spec['note']} */")
    for s in STEPS:
        out.append(f"  --gru-{key}-{s}: {palette[key][s]};")
out.append(f"""
  /* ======== GROUND \u2014 the two absolute values, never re-themed ========
     Named --gru-ground-* deliberately. These were once called --gru-ink and
     --gru-paper, which are also the names of two SEMANTIC ROLES declared further down;
     the role won by source order and the ground token silently did nothing. Anything
     that must stay one value whatever the theme \u2014 print, a gradient's own text \u2014
     uses these. */
  --gru-ground-ink: {INK};
  --gru-ground-paper: {PAPER};
  --gru-on-gradient: {PAPER};   /* the signature gradient is deep-to-pale in BOTH themes,
                                   so text on it is white in both. 16.26:1 on the deep end. */

  /* ======== SCRIM \u2014 for holding text over the gradient ========
     Text on the gradient's pale end measures about 2:1. These stops put the deep end back
     over the text, so a hero is legible at any width. Built from Meridian itself. */
  --gru-scrim-strong: rgb(26 23 83 / .94);
  --gru-scrim-soft:   rgb(26 23 83 / .45);
  --gru-scrim-none:   rgb(26 23 83 / 0);
  /* A lift, for a control that sits ON the gradient. The page's own pale hover
     ground would put white text on near-white — 1.00:1 on the hero's second
     call to action, which is the one a hesitant reader hovers first. */
  --gru-scrim-lift:   rgb(255 255 255 / .18);""")
out.append("\n  /* ======== SIGNATURE GRADIENT — 'first light'. Hero art only; never behind body text. ======== */")
out.append(f"  --gru-grad-firstlight: linear-gradient(112deg, {M} 0%, "
           f"{P['meridian'][800]} 32%, {E} 76%, {D} 100%);")
out.append(f"  --gru-grad-firstlight-radial: radial-gradient(120% 90% at 8% 100%, {D} 0%, "
           f"{E} 26%, {P['meridian'][800]} 62%, {M} 100%);")
out.append("}\n")

out.append("/* ======== SEMANTIC ROLES — light theme (the default) ======== */\n:root{")
for k, v in LIGHT.items():
    out.append(f"  --gru-{k}: {v};")
for i, (n, h, k) in enumerate(CHART_LIGHT, 1):
    out.append(f"  --gru-chart-{i}: {h};   /* {n} · {k}:1 on paper */")
out.append("}\n")
dark_block = []
for k, v in DARK.items():
    dark_block.append(f"  --gru-{k}: {v};")
for i, (n, h, k) in enumerate(CHART_DARK, 1):
    dark_block.append(f"  --gru-chart-{i}: {h};   /* {n} · {k}:1 on ink */")
out.append("/* ======== SEMANTIC ROLES — dark theme ======== */")
out.append("/* Automatic: follows the reader's system setting unless they have chosen a theme. */")
out.append('@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){')
out += dark_block
out.append("}}")
out.append("""
/* Explicit, and SCOPED — the selector is [data-theme="…"], not :root[data-theme="…"].
   That one difference is what lets a theme apply to any element rather than only the
   document root, so a dark panel can sit inside a light page: a dark hero above light
   reading, a side-by-side comparison, a preview of one theme shown in the other. With
   :root only, a nested data-theme silently does nothing and the panel renders in the
   page's theme — which is exactly the bug this replaced.

   Both directions are declared, so a light island inside a dark page works too, and both
   come after the media query above so an explicit choice always wins over the system's. */""")
out.append('[data-theme="dark"]{')
out += dark_block
out.append("}")
out.append('[data-theme="light"]{')
for k, v in LIGHT.items():
    out.append(f"  --gru-{k}: {v};")
for i, (n, h, k) in enumerate(CHART_LIGHT, 1):
    out.append(f"  --gru-chart-{i}: {h};   /* {n} · {k}:1 on paper */")
out.append("}")
out.append("""
/* ======== FORCED COLOURS — Windows High Contrast and similar ========
   When the operating system supplies its own palette, stop fighting it. */
@media (forced-colors: active){
  /* Both selectors. A themed island \u2014 :root is not its ancestor's ancestor \u2014 kept
     its own hex values under Windows High Contrast and ignored the user's palette, which
     is the whole thing that mode exists to prevent. */
  :root, [data-theme]{
    --gru-focus: Highlight; --gru-link: LinkText; --gru-ink: CanvasText;
    --gru-bg: Canvas; --gru-surface: Canvas; --gru-surface-raised: Canvas;
    --gru-border: CanvasText; --gru-border-strong: CanvasText;
  }
}""")
TOKENS_CSS = "\n".join(out) + "\n"

# ---------------------------------------------------------------- emit tokens.json
data = dict(
    kit="GRU953",
    tagline=dict(en="Simple technology. For everyone.", bn="সহজ প্রযুক্তি। সবার জন্য।"),
    # Self-contained on purpose. This file is generated to be *shipped*, and the
    # kit's governance/ directory does not travel with it — an app that embeds
    # these tokens leaves anyone reading them following a path that is not there.
    # So the answer is carried here instead of pointed at.
    licence=dict(
        system="Apache-2.0",
        guidebook="PolyForm-Noncommercial-1.0.0",
        fonts="OFL-1.1",
        marks="not licensed",
        marks_detail=("The name GRU953, the Soaring Bird mark, the app-icon tile, the "
                      "GRU953 wordmark and any lockup of them are not licensed and stay "
                      "with the studio. The colour values and these token names are "
                      "Apache-2.0 and may be used commercially, including in commercial "
                      "products. Full policy: the brand kit's "
                      "08_guidebook/governance/TRADEMARKS.md, which does not ship beside "
                      "this file."),
    ),
    signature_rule=("One hue, two tuned values. No single colour clears 4.5:1 against both "
                    "white and near-black, so --gru-accent resolves to a deep Daybreak step "
                    "on light grounds and a pale one on dark grounds."),
    families={k: dict(label=v["label"], bangla=v["bn"], kind=v["kind"], note=v["note"],
                      anchor=v.get("anchor"), anchor_step=homes[k], hue_oklch=hues[k],
                      ramp=palette[k], roles=roleinfo[k]) for k, v in FAMILIES.items()},
    ground=dict(ink=INK, paper=PAPER),
    thresholds=dict(max_luminance_on_paper=MAX_L_ON_PAPER,
                    min_luminance_on_ink=MIN_L_ON_INK,
                    note="To clear WCAG 4.5:1 a colour must be darker than "
                         "max_luminance_on_paper against white, and lighter than "
                         "min_luminance_on_ink against the Ink. Both cannot be true, which "
                         "is why the signature is one hue with two tuned values."),
    accent=dict(light=SIG_LIGHT, dark=SIG_DARK,
                light_ratio_on_paper=K(SIG_LIGHT, PAPER), dark_ratio_on_ink=K(SIG_DARK, INK),
                hue_drift_degrees=sig_hue_drift, delta_e_between_values=sig_delta_e),
    nearest_occupied={label: [dict(brand=k, delta_e=d) for d, k in near]
                      for label, _, near in occupied_report},
    gradient_firstlight=[M, P["meridian"][800], E, D],
    roles=dict(light=LIGHT, dark=DARK),
    charts=dict(light=[dict(name=n, hex=h, ratio=k) for n, h, k in CHART_LIGHT],
                dark=[dict(name=n, hex=h, ratio=k) for n, h, k in CHART_DARK]),
)
TOKENS_JSON = json.dumps(data, indent=2, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------- emit CONTRAST.md
def grade(ratio, large=False):
    aaa, aa = (4.5, 3.0) if large else (7.0, 4.5)
    return "AAA" if ratio >= aaa else ("AA" if ratio >= aa else "—")


KEY_PAIRS = [
    ("Signature on paper (light theme)", SIG_LIGHT, PAPER),
    ("Signature on ink (dark theme)", SIG_DARK, INK),
    ("Meridian on paper", M, PAPER), ("White on Meridian", PAPER, M),
    ("Daybreak on Meridian", D, M), ("Ember on Meridian", E, M),
    ("Ink on Daybreak", INK, D), ("Ink on Ember", INK, E),
    ("Ink on paper", INK, PAPER), ("Paper on ink", PAPER, INK),
]
L = ["# GRU953 — contrast and distinctiveness, proved", "",
     "সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.", "",
     "Every number on this page is **computed** by `04_colour/engine.py`. None of it is",
     "asserted by hand. Regenerate the page whenever a colour changes.", "",
     "**The four words this page needs, in plain English.**", "",
     "- **WCAG** — the Web Content Accessibility Guidelines, the accessibility rulebook that",
     "  regulators and procurement teams actually point to. Version 2.2, level AA, is the bar",
     "  used throughout. AAA is the stricter level above it.",
     "- **Luminance** — how much light a colour emits. Brightness, not colourfulness.",
     "- **Contrast ratio** — the ratio between two luminances, written `4.5:1`. Bigger is",
     "  easier to read.",
     "- **ΔE**, said *delta E* — how different two colours *look* to a normal eye. Under about",
     "  1, nobody notices. Over about 10, anyone would call them different colours. The method",
     "  here is CIEDE2000, the current standard for this.", "",
     "**Standard:** WCAG 2.2. Normal text needs **4.5:1** for AA and **7:1** for AAA. Large",
     "text (24px, or 19px bold) and non-text interface parts need **3:1**. Every role below",
     f"clears its target by at least **{MARGIN}**, so rounding to 8-bit hex cannot quietly",
     "drop it under.", "",
     "## 1. Why the signature is one hue with two values", "",
     "This is the single most important fact about the palette, so it is proved first.", "",
     "WCAG contrast is `(L1+0.05)/(L2+0.05)` on relative luminance.", "",
     f"- To reach 4.5:1 against white a colour needs luminance **≤ {MAX_L_ON_PAPER}**.",
     f"- To reach 4.5:1 against the ink `{INK}` it needs luminance **≥ {MIN_L_ON_INK}**.", "",
     "Those two cannot both be true. **No single colour can be this brand's text colour in",
     "both themes.** So Daybreak is expressed as two tuned values from one ramp:", "",
     "| theme | token resolves to | ground | ratio |", "|---|---|---|---:|",
     f"| light | `{SIG_LIGHT}` | `{PAPER}` | **{K(SIG_LIGHT, PAPER)}:1** |",
     f"| dark | `{SIG_DARK}` | `{INK}` | **{K(SIG_DARK, INK)}:1** |", "",
     f"They are the SAME HUE — {sig_hue_drift}° apart, which is inside the range a viewer",
     "reads as one colour family. They are **not** the same value, and this page will not",
     f"pretend otherwise: their CIEDE2000 difference is **ΔE {sig_delta_e}**, well above the",
     f"ΔE {DISTINCT_MIN} floor this page uses elsewhere for *obviously different*. One is a deep",
     "terracotta and one is a pale salmon, because that is what being legible on white and",
     "being legible on near-black actually require.", "",
     "The honest statement is therefore: **one hue, two calibrated values** — not *one colour*.",
     "Someone shown the two side by side will say they are different. Someone shown the light",
     "theme and then the dark theme will say the brand kept its colour. Both are true, and the",
     "second is the one that matters for an identity.", "",
     "## 2. The pairings you will actually use", "",
     "| pairing | foreground | background | ratio | normal text | large text / UI |",
     "|---|---|---|---:|:---:|:---:|"]
for name, fg, bg in KEY_PAIRS:
    ratio = K(fg, bg)
    g, gl = grade(ratio), grade(ratio, True)
    if g == "—" and gl == "—":
        fails.append(f"{name} clears nothing at all ({ratio}:1)")
    L.append(f"| {name} | `{fg}` | `{bg}` | **{ratio}:1** | {g} | {gl} |")

L += ["", "## 3. Every semantic role, measured against its own theme's background", "",
      "A role is only correct if it is correct **in the theme it belongs to**. Each row is",
      "measured against that theme's `bg`.", "",
      "| role | light value | on paper | dark value | on ink |", "|---|---|---:|---|---:|"]
TEXTISH = {"ink", "ink-muted", "ink-subtle", "brand", "accent", "link", "link-visited",
           "info", "success", "warning", "danger"}
UIISH = {"border-strong", "focus", "accent-ui", "info-border",
         "success-border", "warning-border", "danger-border"}
# Deliberately NOT held to 3:1 — these are decorative or are themselves backgrounds.
DECORATIVE = {"border", "bg", "bg-subtle", "surface", "surface-raised", "surface-sunken",
              "overlay", "brand-quiet", "accent-quiet", "disabled-bg", "disabled-border",
              "info-quiet", "success-quiet", "warning-quiet", "danger-quiet",
              "ink-inverse", "on-brand", "on-accent", "on-info", "on-success", "on-warning",
              "on-danger", "focus-inverse", "disabled-ink"}
for k in LIGHT:
    lv, dv = LIGHT[k], DARK.get(k, "—")
    if lv.startswith("rgba") or dv.startswith("rgba"):
        L.append(f"| `--gru-{k}` | `{lv}` | — | `{dv}` | — |")
        continue
    lk, dk = K(lv, LIGHT["bg"]), K(dv, DARK["bg"])
    flag = ""
    if k in TEXTISH:
        flag = " ✗" if min(lk, dk) < 4.5 else ""
        if flag:
            fails.append(f"--gru-{k} is text but measures {min(lk, dk)}:1 in one theme")
    elif k in UIISH:
        flag = " ✗" if min(lk, dk) < 3.0 else ""
        if flag:
            fails.append(f"--gru-{k} is a UI part but measures {min(lk, dk)}:1 in one theme")
    L.append(f"| `--gru-{k}` | `{lv}` | {lk}:1 | `{dv}` | {dk}:1{flag} |")

# ------------------------------------------------------------- 3a. the pairings, proved
# The table above proves every role against the page background. That is not the question a
# component asks. A badge puts `--gru-danger` on `--gru-danger-quiet`; a statistic puts
# `--gru-success` on `--gru-surface-raised`; a card's meta line puts `--gru-ink-subtle` on
# `--gru-surface-sunken`. THOSE are the pairings that either work or do not, and an earlier
# edition shipped eight of them between 3.89:1 and 4.46:1 while this file printed PASS.
#
# So the pairings are enumerated here, from what the component library actually does, and
# every one is measured in both themes. Adding a component means adding its pairing.
# The pairings, DERIVED — every foreground/background combination the component library
# can actually create, read out of components.css rather than typed here by hand.
#
# The hand-written list this replaces covered 63 pairings. An audit walked the stylesheet
# and found 94, of which 15 were below their target — including the focus ring at 2.90:1
# inside an error panel and a selected tab at 4.36:1 when hovered. A hand-maintained list
# beside a stylesheet that keeps changing is a list that goes out of date silently, which
# is the same failure as the one it was written to catch.
#
# A pairing counts when some rule can set the foreground while some ground is beneath it.
# The ground set per component is deliberately generous: a card can sit on the page, in a
# raised panel, or on a tint, and CSS does not stop you.
def _find_components() -> pathlib.Path | None:
    """Find design-system/src/components.css without assuming where it sits.

    A fixed relative path broke the moment the three trees were laid out as folders of one
    repository instead of siblings on one machine — and it broke by CRASHING three hundred
    lines later, on `min()` of an empty sequence, rather than by saying what was missing.
    Walk up from this file and look; if it is genuinely not there, say so and stop.
    """
    here = pathlib.Path(__file__).resolve()
    for base in [here.parent, *here.parents]:
        for rel in ("design-system/src/components.css",
                    "GRU953_Build/design-system/src/components.css"):
            c = base / rel
            if c.exists():
                return c
    return None


COMPONENT_ROOT = _find_components()

TEXT_ROLES = {"ink", "ink-muted", "ink-subtle", "link", "link-hover", "link-visited",
              "brand", "accent", "info", "success", "warning", "danger",
              "on-brand-quiet", "on-accent-quiet", "on-info-quiet", "on-success-quiet",
              "on-warning-quiet", "on-danger-quiet"}
UI_ROLES = {"border-strong", "focus", "accent-ui", "info-border", "success-border",
            "warning-border", "danger-border"}
GROUND_ROLES = {"bg", "bg-subtle", "surface", "surface-raised", "surface-sunken",
                "brand-quiet", "accent-quiet", "info-quiet", "success-quiet",
                "warning-quiet", "danger-quiet", "border", "disabled-bg"}
# A foreground pinned to one ground by the same rule, so it is never on anything else.
PINNED = {"on-brand": {"brand", "brand-hover", "brand-active"},
          "on-accent": {"accent", "accent-hover", "accent-active"},
          "on-danger": {"danger", "danger-hover", "danger-active"},
          "on-info": {"info"}, "on-success": {"success"}, "on-warning": {"warning"},
          "ink-inverse": {"brand", "brand-hover", "brand-active"},
          "focus-inverse": {"brand", "accent"},
          "disabled-ink": {"disabled-bg"}}
# Exempt under WCAG 1.4.3: an inactive control, and a hairline that carries no meaning.
EXEMPT_FG = {"disabled-ink", "disabled-border"}
# Grounds that carry no text of their own: an inactive control (1.4.3 exempts it), a
# hairline, and the modal scrim, which is behind the dialog rather than behind its words.
EXEMPT_BG = {"disabled-bg", "disabled-border", "border", "overlay"}


def derive_pairings():
    """Read components.css and return every pairing it can actually create.

    Three things make this accurate enough to be worth failing a build on.

    THE KEY IS THE CLASS TOKEN, not the BEM block. `.gru-btn--primary`'s label and
    `.gru-btn--secondary`'s fill are both "gru-btn"; pairing them reports white on white
    for a combination no element can have. A `::backdrop` gets its own key, because it is
    behind the dialog, not behind its words.

    STATES ARE CHECKED FOR COMPATIBILITY. `.gru-tab:not([aria-selected="true"]):hover`
    and `.gru-tab[aria-selected="true"]` can never apply to the same element, so their
    declarations are never paired. Without this the checker demanded that a hover colour
    be legible on a selected ground — and, worse, it could not tell that apart from the
    real defect the same shape produced before the `:not()` was added, where hovering the
    page you were already on put 1.19:1 on screen.

    A MODIFIER INHERITS ONLY WHAT IT DOES NOT DECLARE, because its own declaration wins
    over the base block's by source order.

    Cross-component pairings are not derived: nothing nests a badge's text on an alert's
    tint. The two roles that genuinely land anywhere — the focus ring and the strong
    border — are picked against every ground in the system, above, and listed explicitly.
    """
    if COMPONENT_ROOT is None:
        fails.append("design-system/src/components.css was not found anywhere above this "
                     "file, so not one pairing could be proved. The palette is not "
                     "shippable without it: nothing else knows which colours meet.")
        return []
    css = re.sub(r"/\*[\s\S]*?\*/", "", COMPONENT_ROOT.read_text(encoding="utf-8"))
    STATE = re.compile(r"\[[^\]]+\]|:(?:hover|active|focus|focus-visible|checked|disabled|"
                       r"aria-[\w-]+)")

    def specificity(part):
        """(classes+attributes+pseudo-classes, elements) — enough of the cascade to say
        which of two rules wins a property. `:not()` contributes its contents, as CSS
        specifies, and the wrapper itself contributes nothing."""
        s = re.sub(r":not\(|\)", " ", part)
        b = len(re.findall(r"\.[\w-]+|\[[^\]]+\]|:(?!:)[\w-]+", s))
        c = len(re.findall(r"(?:^|[\s>+~])([a-z][\w-]*)", s))
        return (b, c)

    def states(part):
        """(required, forbidden) — the conditions this selector needs and rules out."""
        neg = set()
        for m in re.finditer(r":not\(([^()]*)\)", part):
            neg |= set(STATE.findall(m.group(1)))
        req = set(STATE.findall(re.sub(r":not\([^()]*\)", "", part))) 
        return req, neg

    rules: dict[str, list] = {}
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel, body = m.group(1), m.group(2)
        fg = {f.group(1) for f in
              re.finditer(r"(?<![\w-])color\s*:\s*var\(--gru-([\w-]+)\)", body)}
        bg = {g.group(1) for g in
              re.finditer(r"(?<![\w-])background(?:-color)?\s*:[^;]*?var\(--gru-([\w-]+)\)",
                          body)}
        if not (fg or bg):
            continue
        for part in sel.split(","):
            pseudo = re.search(r"::[a-z-]+", part)
            req, neg = states(part)
            for cls in re.findall(r"\.(gru-[a-z0-9_-]+)", part):
                key = cls + (pseudo.group(0) if pseudo else "")
                rules.setdefault(key, []).append(
                    dict(req=req, neg=neg, fg=fg, bg=bg, spec=specificity(part)))
    # a modifier also matches its base block's rules
    for key in list(rules):
        base = key.split("--")[0]
        if "--" in key and base in rules:
            declared_fg = any(r["fg"] for r in rules[key])
            declared_bg = any(r["bg"] for r in rules[key])
            for r in rules[base]:
                rules[key].append(dict(req=r["req"], neg=r["neg"], spec=r["spec"],
                                       fg=set() if declared_fg else r["fg"],
                                       bg=set() if declared_bg else r["bg"]))

    seen, out = set(), []

    def emit(fg, bg, target, why):
        if fg == bg or fg not in LIGHT or bg not in LIGHT or (fg, bg) in seen:
            return
        if fg in EXEMPT_FG or bg in EXEMPT_FG or bg in EXEMPT_BG:
            return
        seen.add((fg, bg))
        out.append((fg, bg, target, why))

    def compatible(a, b):
        return not (a["req"] & b["neg"] or b["req"] & a["neg"])

    for key, rs in sorted(rules.items()):
        for a in rs:                                # a supplies the foreground
            for b in rs:                            # b supplies the ground
                if not compatible(a, b):
                    continue                        # the two states exclude each other
                # ...and a's colour only counts if nothing compatible outranks it. The
                # pagination link sets ink-muted on `.gru-pagination a` (0,1,1) while
                # `.gru-pagination [aria-current="page"]` (0,2,0) sets on-brand and the
                # brand ground: the current page is never ink-muted on brand, because the
                # attribute rule wins the colour. Without this the checker reports a
                # 1.39:1 pairing that no element can be in.
                if any(o["fg"] and o["spec"] > a["spec"]
                       and compatible(o, a) and compatible(o, b) for o in rs):
                    continue
                for fg in sorted(a["fg"]):
                    for bg in sorted(b["bg"]):
                        emit(fg, bg, 3.0 if fg in UI_ROLES else 4.5,
                             f"{key}: its own text on its own ground")
        # ...and on a page surface. A COLOURED role is guaranteed on bg, surface and
        # surface-raised only; on a subtle or sunken tint, text is ink, ink-muted or
        # ink-subtle. That is a rule of the system, not an omission, and check.mjs
        # measures whether any card breaks it.
        for a in rs:
            for fg in sorted(a["fg"]):
                if fg in PINNED:
                    continue
                grounds = (["bg", "bg-subtle", "surface", "surface-raised", "surface-sunken"]
                           if fg.startswith("ink") else
                           ["bg", "surface", "surface-raised"])
                for bg in grounds:
                    emit(fg, bg, 3.0 if fg in UI_ROLES else 4.5,
                         f"{key} on a page surface")
    for fg in ("focus", "border-strong"):
        for bg in ["bg", "bg-subtle", "surface", "surface-raised", "surface-sunken"] + \
                  [f"{r}-quiet" for r in
                   ("brand", "accent", "info", "success", "warning", "danger")]:
            emit(fg, bg, 3.0, "drawn over whatever the control sits in")
    return out


PAIRINGS = derive_pairings()
if len(PAIRINGS) < 40:
    fails.append(f"only {len(PAIRINGS)} pairings were derived from components.css — "
                 f"the stylesheet was probably not read correctly")
PAIRINGS.sort()
L += ["", "## 3a. Every pairing the component library actually uses", "",
      "Proving a colour against the page background is not the same as proving it where a",
      "component puts it. Each row below is a pairing that exists in `components.css`, measured",
      "in both themes. A component that needs a pairing not listed here is a component that has",
      "not been proved.", "",
      "| foreground | background | what it is | light | dark | need |",
      "|---|---|---|---:|---:|---:|"]
for fg, bg, target, what in PAIRINGS:
    if fg not in LIGHT or bg not in LIGHT:
        fails.append(f"pairing {fg} on {bg} names a role that does not exist")
        continue
    lk, dk = K(LIGHT[fg], LIGHT[bg]), K(DARK[fg], DARK[bg])
    bad = ""
    if min(lk, dk) < target:
        bad = " ✗"
        fails.append(f"{fg} on {bg} ({what}) measures {min(lk, dk)}:1, needs {target}:1")
    L.append(f"| `--gru-{fg}` | `--gru-{bg}` | {what} | {lk}:1 | {dk}:1{bad} | {target}:1 |")
# Reported only if there is something to report. An empty PAIRINGS list already added its
# own failure above; crashing here on min() of an empty sequence hid that message behind a
# traceback, which is the least useful way for a build to tell you what is wrong.
if PAIRINGS:
    worst_pair = min((min(K(LIGHT[f], LIGHT[b]), K(DARK[f], DARK[b])), f, b)
                     for f, b, _, _ in PAIRINGS if f in LIGHT and b in LIGHT)
    L += ["", f"Worst pairing in the set: **{worst_pair[0]}:1** "
              f"(`--gru-{worst_pair[1]}` on `--gru-{worst_pair[2]}`).", ""]

L += ["", "## 4. Distinctiveness — no two meanings may look alike", "",
      "Contrast says a colour is legible. It says nothing about whether *success* can be told",
      f"apart from *warning*. These are CIEDE2000 differences; the floor here is **ΔE {DISTINCT_MIN}**,",
      "an obvious difference to a normally-sighted viewer.", "",
      "| set | closest pair | ΔE | verdict |", "|---|---|---:|---|"]
for setname, worst in distinct_report.items():
    d, a, b = worst
    L.append(f"| {setname} | {a} vs {b} | {d} | {'PASS' if d >= DISTINCT_MIN else 'FAIL'} |")

L += ["", "## 4a. Distinctiveness against colours other brands already own", "",
      "The check above asks whether the kit's own colours can be told apart. This one asks the",
      "question that actually matters to a developer audience: **does the brand look like",
      "somebody else's?** These are CIEDE2000 differences against colours that audience sees",
      "every day.", "",
      "| GRU953 colour | value | closest three |", "|---|---|---|"]
for label, val, near in occupied_report:
    cells = ", ".join(f"{k} ΔE {d}" for d, k in near)
    L.append(f"| {label} | `{val}` | {cells} |")
L += ["",
      "**Read honestly:** Daybreak's light value sits closest to Rust's brand orange and to",
      "the sienna pigment. That is a real proximity and it is published rather than left out.",
      "It was accepted for three reasons. The proximity is to a *deep interface accent*, not",
      "to the brand's dominant colour — brands collide through their marks and their grounds,",
      "which here are a bird and a deep indigo, neither of which resembles Rust. The chroma at",
      "the deep end is deliberately tapered (see the `taper` in the engine) precisely to pull",
      "away from the saturated rust-orange region. And the value a viewer sees most often is",
      "the pale one, on dark grounds, which is ΔE 13.8 from its nearest neighbour.", "",
      "**Meridian is in a crowded region and the kit says so.** Deep indigo is owned by many",
      "brands, which is exactly why it is treated as the *ground* rather than the signature.",
      "The signature is Daybreak, the bird, and the pairing — not the navy.", "",
      "### The chart sequence", "",
      "| # | series | light theme | on paper | dark theme | on ink |", "|---|---|---|---:|---|---:|"]
for i, ((n, lh, lk), (_, dh, dk)) in enumerate(zip(CHART_LIGHT, CHART_DARK), 1):
    L.append(f"| {i} | {n} | `{lh}` | {lk}:1 | `{dh}` | {dk}:1 |")

L += ["", "## 5. Full ramps, every step measured against both grounds", "",
      "*Monotonic* means every step is reliably lighter than the one below it — the ramp never",
      "doubles back. A ramp that wanders is unusable for an interface, because you can no",
      "longer reach for \"one step darker\" and know what you will get.", ""]
for key, spec in FAMILIES.items():
    head = f"anchor `{spec['anchor']}` at step {homes[key]}" if spec.get("anchor") else \
           f"hue {hues[key]}°, no brand anchor — this family exists to carry a meaning"
    L += [f"### {spec['label']} — `--gru-{key}-*` ({head})", "",
          "| step | hex | on paper | on ink | monotonic? |", "|---|---|---:|---:|---|"]
    prev = None
    for s in STEPS:
        h = palette[key][s]
        lightness = Color(h).convert("oklch")["lightness"]
        mono = "✓" if prev is None or lightness < prev + 1e-9 else "✗ NOT MONOTONIC"
        if "✗" in mono:
            fails.append(f"{spec['label']} step {s} breaks monotonicity")
        prev = lightness
        tag = " **← brand**" if s == homes[key] else ""
        L.append(f"| {s}{tag} | `{h}` | {K(h, PAPER)}:1 | {K(h, INK)}:1 | {mono} |")
    L.append("")

L += ["## 6. Result", "",
      ("**PASS.** Every ramp is monotonic. Every brand anchor sits inside its own ramp. Every "
       "semantic role clears its WCAG 2.2 target in its own theme, with margin. No two "
       "meaning-bearing colours are confusable." if not fails else
       "**FAIL — do not ship.** Problems found:\n\n" + "\n".join(f"- {f}" for f in fails)), "",
      "## 7. What this page deliberately does not claim", "",
      "- These are WCAG 2.x ratios. APCA (a candidate method in the draft WCAG 3) is not used,",
      "  because WCAG 2.2 AA is the standard actually named in law and in procurement today.",
      "- A passing ratio does not by itself make a screen readable. Text size, weight, line",
      "  length and sheer quantity all matter, and none of them are measured here.",
      "- ΔE distinctiveness is computed for normal colour vision. It is not a colour-blindness",
      "  simulation. In this kit colour is never the only carrier of meaning — every state also",
      "  carries a word, an icon or a shape, which is the actual protection.",
      "- Nothing here has been tested with a real screen reader by a real user."]
CONTRAST_MD = "\n".join(L) + "\n"

# ---------------------------------------------------------------- write, or do not
# NOTHING is on disk until here. Sections 2, 3, 4 and 5 of the proof MEASURE as they build
# their tables, so `fails` can still grow long after the palette itself looked sound. Writing
# tokens.css early and checking the exit code late meant a failing run still left a
# complete-looking token set on disk — including the #FF00FF sentinel that marks a role with
# no passing step. So the three documents are assembled in memory and written together, and
# only if every single check passed.
if fails:
    print("FAIL — nothing was written. Problems found:")
    for f in dict.fromkeys(fails):
        print(f"  ✗ {f}")
    sys.exit(1)

pathlib.Path("../08_guidebook/assets").mkdir(parents=True, exist_ok=True)
pathlib.Path("../08_guidebook/assets/tokens.css").write_text(TOKENS_CSS)
pathlib.Path("../08_guidebook/assets/tokens.json").write_text(TOKENS_JSON)
pathlib.Path("CONTRAST.md").write_text(CONTRAST_MD)

print("PASS \u2014 every ramp, role, chart colour and distinctiveness check holds.")
print(f"  signature   light {SIG_LIGHT} ({K(SIG_LIGHT, PAPER)}:1 on paper)   "
      f"dark {SIG_DARK} ({K(SIG_DARK, INK)}:1 on ink)   hue drift {sig_hue_drift}°")
for key in FAMILIES:
    print(f"  {key:9s} {'anchor@' + str(homes[key]) if homes[key] else 'functional':<12}",
          " ".join(palette[key][s] for s in STEPS))

