#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""GRU953 -- build and prove the four colour directions, before any one of them is chosen.

Reuses the ramp-construction method already proven in engine.py (OKLCH, anchor-snapped,
gamut-mapped) rather than reinventing it, applied to four structurally different premises
instead of one. This script does NOT replace engine.py -- the shipping kit's tokens are
untouched until GATE 1 is decided; this only builds the comparison material.

WHAT "STRUCTURALLY DIFFERENT" MEANS
------------------------------------
A hue rotation changes one number. Each direction here differs from the others on at
least three of: ground strategy (chromatic / near-black / neutral), signature structure
(one hue two values / one value / three-key), temperature relationship, and how the dark
theme is built. See brand-kit/04_colour/directions/*.json for each premise in full.

PESSIMISTIC CONTRAST, THE SAME RULE AS engine.py
-------------------------------------------------
Every ratio published here is measured on the 8-bit hex that would actually ship, with
every +/-1 channel perturbation of BOTH colours checked (27 x 27 = 729 combinations per
pair) and the WORST published -- never the ideal continuous-OKLCH number, which no
browser, OS colour pipeline or P3 round-trip is obliged to reproduce exactly.

D2'S CENTRAL CLAIM, SOLVED NOT ASSUMED
----------------------------------------
D2 claims a single accent value can clear 4.5:1 against both a white light-theme ground
and a near-black dark-theme ground. The continuous-OKLCH arithmetic says the window is
real but under 0.00001 luminance units wide at the extremes (white, and a ground at
luminance <=0.00185) -- narrower than 8-bit rounding can necessarily hit. This script
SEARCHES for an actual achievable hex value, applies the same pessimistic +/-1 check as
everything else, and reports PASS or FAIL with the real numbers -- it does not assume
the premise survives contact with a real colour pipeline just because the continuous
maths allows it in principle.

Run:  cd 04_colour && python3 build_directions.py
"""
from coloraide import Color
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
DIRECTIONS_DIR = HERE / "directions"
GENERATED_DIR = HERE / "generated"

MARGIN = 0.05   # same margin engine.py uses: clear the target by this much before rounding
PAPER = "#FFFFFF"

STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
NOMINAL_L = {50: 0.975, 100: 0.945, 200: 0.895, 300: 0.830, 400: 0.755,
             500: 0.665, 600: 0.570, 700: 0.475, 800: 0.375, 900: 0.270, 950: 0.190}
CHROMA_ARC = {50: 0.14, 100: 0.26, 200: 0.44, 300: 0.68, 400: 0.86, 500: 1.00,
              600: 0.98, 700: 0.90, 800: 0.78, 900: 0.64, 950: 0.50}


def mk(l, c, h):
    return Color("oklch", [l, c, h]).convert("srgb").fit("srgb", method="oklch-chroma")


def hexof(c):
    return c.convert("srgb").to_string(hex=True).upper()


def relative_luminance(hexstr):
    return Color(hexstr).luminance()


def K(a, b):
    return round(Color(a).contrast(b), 3)


def build_ramp(spec):
    """Same method as engine.py's build_ramp: anchor the ramp on a real brand colour
    where one exists; otherwise build from a stated hue and chroma ceiling."""
    if spec.get("anchor"):
        a = Color(spec["anchor"]).convert("oklch")
        hue, aL, aC = a["hue"], a["lightness"], a["chroma"]
        home = min(STEPS, key=lambda s: abs(NOMINAL_L[s] - aL))
        ceiling = aC / CHROMA_ARC[home] if CHROMA_ARC[home] else aC
    else:
        hue = spec["hue"]
        ceiling = spec.get("max_chroma", 0.05) / CHROMA_ARC[500]
        home = None
    ramp = {s: (spec["anchor"].upper() if (spec.get("anchor") and s == home)
                else hexof(mk(NOMINAL_L[s], ceiling * CHROMA_ARC[s], hue)))
            for s in STEPS}
    return ramp, home, round(hue, 1)


def hex_neighbours(hexstr):
    """Every +/-1-per-channel perturbation of an 8-bit hex colour, 27 total (including
    itself). This is what makes a published ratio a measured floor rather than a
    continuous-maths ideal a real browser or OS colour pipeline is not obliged to hit."""
    c = Color(hexstr).convert("srgb")
    r, g, b = (round(c[ch] * 255) for ch in ("red", "green", "blue"))
    out = []
    for dr in (-1, 0, 1):
        for dg in (-1, 0, 1):
            for db in (-1, 0, 1):
                rr = min(255, max(0, r + dr))
                gg = min(255, max(0, g + dg))
                bb = min(255, max(0, b + db))
                out.append(f"#{rr:02X}{gg:02X}{bb:02X}")
    return out


def worst_case_ratio(fg_hex, bg_hex):
    """The published figure: round both colours to the 8-bit hex that ships, then check
    every one of the 729 combinations of their +/-1-channel neighbours, and publish the
    WORST ratio found -- not the nominal one. Replaces a guessed safety margin with a
    measured one."""
    fg_hex = hexof(Color(fg_hex))
    bg_hex = hexof(Color(bg_hex))
    worst = None
    for f in hex_neighbours(fg_hex):
        for b in hex_neighbours(bg_hex):
            r = Color(f).contrast(b)
            if worst is None or r < worst:
                worst = r
    return round(worst, 3)


def solve_single_value_across_grounds(hue, light_ground, dark_ground, target=4.5):
    """For D2's claim specifically: does ONE hex value clear `target`+MARGIN against both
    `light_ground` and `dark_ground`? Searches OKLCH lightness AND chroma at a fixed hue,
    evaluating the PESSIMISTIC (rounded + perturbed) ratio at each point, not the ideal
    continuous value.

    A single-chroma search here once reported the claim FAILS by a shortfall of only
    0.144 -- close enough that the true answer depended on whether a different chroma
    would have closed the gap. It was not a safe thing to report as the final word
    without checking, so this searches multiple chroma values, not one representative
    guess, before concluding either way.

    Returns the found value and its two worst-case ratios if one exists that clears both,
    at ANY of the tried chroma values; otherwise returns the single closest miss across
    every chroma tried, so a genuine failure is reported with evidence, not silently
    converted into "not applicable".
    """
    # Two phases, so the expensive 729-combination pessimistic check runs only near the
    # actual optimum, not at every point of an 8 x 999 grid (the first version of this
    # search did that and took over two minutes -- fine once, unworkable for something
    # meant to run in CI on every push).
    #
    # Phase 1 -- coarse, on the IDEAL (unrounded, unperturbed) ratio, which is cheap:
    # find where in (chroma, lightness) space the ideal ratio is closest to clearing
    # both grounds at all.
    candidates_by_ideal = []
    for chroma in (0.02, 0.04, 0.06, 0.08, 0.10, 0.13, 0.16, 0.20):
        for i in range(1, 200):
            l = i / 200
            hx = hexof(mk(l, chroma, hue))
            ideal_light = Color(hx).contrast(light_ground)
            ideal_dark = Color(hx).contrast(dark_ground)
            candidates_by_ideal.append(
                (min(ideal_light, ideal_dark), hx, chroma, l))
    candidates_by_ideal.sort(key=lambda t: -t[0])

    # Phase 2 -- the real, pessimistic measurement (8-bit + 729-neighbour check), but
    # only on the strongest candidates the cheap phase surfaced. 40 is generous headroom
    # over the handful that could plausibly change the verdict.
    best = None
    closest_miss = None
    for _, hx, chroma, l in candidates_by_ideal[:40]:
        candidate = hx
        ratio_light = worst_case_ratio(candidate, light_ground)
        ratio_dark = worst_case_ratio(candidate, dark_ground)
        gap = min(ratio_light, ratio_dark) - (target + MARGIN)
        if closest_miss is None or gap > closest_miss[0]:
            closest_miss = (gap, candidate, ratio_light, ratio_dark, chroma, l)
        if ratio_light >= target + MARGIN and ratio_dark >= target + MARGIN:
            if best is None or chroma > best[4]:
                best = (candidate, ratio_light, ratio_dark, l, chroma)
    if best:
        return {"found": True, "hex": best[0], "ratio_on_light": best[1],
                "ratio_on_dark": best[2], "oklch_lightness": round(best[3], 4),
                "oklch_chroma": best[4],
                "note": "the highest-chroma passing value found, since a real signature "
                        "colour needs to be visibly a colour, not the barest grey that "
                        "technically clears the target"}
    return {"found": False, "closest_attempt_hex": closest_miss[1],
            "closest_ratio_on_light": closest_miss[2],
            "closest_ratio_on_dark": closest_miss[3],
            "closest_attempt_chroma": closest_miss[4],
            "closest_attempt_oklch_lightness": round(closest_miss[5], 4),
            "shortfall_below_target_plus_margin": round(-closest_miss[0], 3),
            "chromas_tried": [0.02, 0.04, 0.06, 0.08, 0.10, 0.13, 0.16, 0.20]}


def build_direction(spec_path):
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    key = spec["key"]
    families = spec["families"]

    ramps = {}
    for fam_key, fam_spec in families.items():
        ramp, home, hue = build_ramp(fam_spec)
        ramps[fam_key] = {
            "label": fam_spec["label"], "label_bn": fam_spec["label_bn"],
            "kind": fam_spec["kind"], "anchor_step": home, "hue": hue,
            "ramp": ramp,
        }

    ground_anchor = families["ground"]["anchor"]
    accent_light_anchor = families["accent_light"]["anchor"]
    accent_dark_anchor = families["accent_dark"]["anchor"]

    # The dark theme's own ground: for directions whose ground family IS the dark
    # ground (the incumbent structure), that is the anchor itself. D2 declares a
    # separate, deliberately near-black ground distinct from its "ground" family
    # anchor's own ramp -- both are real values worth recording.
    dark_ground = spec.get("dark_theme_ground", ground_anchor)

    light_pair = {
        "fg": accent_light_anchor, "bg": PAPER,
        "worst_case_ratio": worst_case_ratio(accent_light_anchor, PAPER),
    }
    dark_pair = {
        "fg": accent_dark_anchor, "bg": dark_ground,
        "worst_case_ratio": worst_case_ratio(accent_dark_anchor, dark_ground),
    }

    out = {
        "key": key, "name": spec["name"], "name_bn": spec["name_bn"],
        "premise": spec["premise"], "structure": spec["structure"],
        "families": ramps,
        "light_theme_ground": PAPER,
        "dark_theme_ground": dark_ground,
        "primary_pairing_proof": {
            "light_theme": light_pair,
            "dark_theme": dark_pair,
            "method": "8-bit hex, then every +/-1-per-channel neighbour of both colours "
                      "checked (729 combinations); the worst ratio found is published, "
                      "never the ideal continuous-OKLCH value.",
            "target": "WCAG 2.2 SC 1.4.3, 4.5:1 normal text, cleared by a further "
                      f"{MARGIN} margin before rounding",
        },
    }

    if spec["structure"]["signature_structure"] == "one-value":
        hue = Color(accent_light_anchor).convert("oklch")["hue"]
        solve = solve_single_value_across_grounds(hue, PAPER, dark_ground)
        out["single_value_claim_solved"] = solve
        out["single_value_claim_solved"]["hue_searched"] = round(hue, 1)
        out["single_value_claim_solved"]["light_ground"] = PAPER
        out["single_value_claim_solved"]["dark_ground"] = dark_ground

    return out


def main():
    GENERATED_DIR.mkdir(exist_ok=True)
    spec_paths = sorted(DIRECTIONS_DIR.glob("*.json"))
    if not spec_paths:
        print("FAIL: no direction specs found in directions/")
        return 1

    results = []
    for p in spec_paths:
        result = build_direction(p)
        out_path = GENERATED_DIR / f"{result['key']}.proof.json"
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")
        results.append(result)
        print(f"{result['key']}: light {result['primary_pairing_proof']['light_theme']['worst_case_ratio']}:1, "
              f"dark {result['primary_pairing_proof']['dark_theme']['worst_case_ratio']}:1")
        if "single_value_claim_solved" in result:
            s = result["single_value_claim_solved"]
            if s["found"]:
                print(f"  single-value claim: PASSES -- {s['hex']} clears "
                      f"{s['ratio_on_light']}:1 on light, {s['ratio_on_dark']}:1 on dark")
            else:
                print(f"  single-value claim: FAILS -- best attempt {s['closest_attempt_hex']} "
                      f"falls short by {s['shortfall_below_target_plus_margin']}")

    print(f"\nwrote {len(results)} direction proofs to {GENERATED_DIR.relative_to(HERE.parent.parent)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
