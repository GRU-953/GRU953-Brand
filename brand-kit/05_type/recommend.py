#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Rank the typography candidates on what has actually been measured, and write the
recommendation with its numbers shown -- never a preference stated without the figures
that produced it.

WHAT THIS SCORES, AND WHAT IT DOES NOT
----------------------------------------
Scored, because it is measured: whether the font's three metric sources agree (a real
cross-browser risk if they don't); whether a variable font's OWN default instance is a
normal weight (400) rather than something that silently renders heavier or lighter than
expected everywhere it is used without an explicit weight; and whether the x-height-to-
cap-height ratio sits in a commonly cited well-balanced range (0.68-0.76) rather than
reading as spindly or crowded.

NOT scored, because it has not been measured yet, and this file says so rather than
inventing a number: numeral distinguishability at small sizes (5/S, 3/8), how the face
looks set as GRU953's own wordmark, and a genuine side-by-side legibility read. A
recommendation missing these inputs is a partial one, and this file's own output states
that plainly rather than presenting a false completeness.

Sora is scored exactly like every other candidate. If it does not win on these numbers,
it does not win.

Run:  python3 brand-kit/05_type/recommend.py
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
MEASUREMENTS_PATH = HERE / "measurements.json"
RENDERED_PATH = HERE / "rendered_measurements.json"
OUT_PATH = HERE / "RECOMMENDATION.md"

GEIST_BORROWED_ASSOCIATION_NOTE = (
    "Vercel's own brand face. Scored on its numbers like every other candidate, but "
    "flagged: winning on numbers alone would not be enough to recommend it, because "
    "the borrowed-association cost is a brand judgement a metric cannot weigh."
)


def score_latin(m: dict) -> dict:
    score = 0
    reasons = []

    if m.get("metric_sources_agree_within_2pct"):
        score += 2
        reasons.append("+2 the three metric sources agree within 2% of the em")
    else:
        reasons.append("+0 the three metric sources DISAGREE by more than 2% of the em "
                       "-- a real cross-browser line-height risk")

    axes = {a["tag"]: a for a in m.get("variable_axes", [])}
    wght = axes.get("wght")
    if wght:
        default_is_normal = abs(wght["default"] - 400) < 1
        if default_is_normal:
            score += 2
            reasons.append("+2 the variable font's own default weight instance is 400 "
                           "(normal) -- using it without setting a weight looks right")
        else:
            reasons.append(f"+0 the variable font's own DEFAULT weight is "
                           f"{wght['default']:.0f}, not 400 -- every use needs an "
                           f"explicit weight or it silently renders "
                           f"{'heavier' if wght['default'] > 400 else 'lighter'} than "
                           f"expected")

    xh, ch = m.get("x_height_over_em"), m.get("cap_height_over_em")
    ratio = None
    if xh and ch:
        ratio = round(xh / ch, 3)
        if 0.68 <= ratio <= 0.76:
            score += 2
            reasons.append(f"+2 x-height/cap-height = {ratio} -- inside the commonly "
                           f"cited well-balanced range (0.68-0.76)")
        else:
            reasons.append(f"+0 x-height/cap-height = {ratio} -- outside 0.68-0.76 "
                           f"({'spindly lowercase' if ratio < 0.68 else 'crowded, small caps read weak'})")

    # The three criteria above are each a coarse +0/+2 bucket, so a genuine 11-way tie
    # on total score is possible (and, on first run, actually happened -- 11 of 15 Latin
    # candidates all scored 4). A tie at the SCORE is not a tie in the underlying numbers,
    # so three continuous tie-break figures are carried alongside the score, each computed
    # from data already measured here, never invented: how far the ratio sits from the
    # ideal centre of its accepted range, how far the variable font's own default weight
    # sits from 400, and how far the three metric sources actually spread apart (not just
    # whether they cross the 2% line). Missing data gets the WORST possible tie-break
    # value (never the best), so an unmeasured font is never flattered by its own gap.
    ratio_distance = round(abs(ratio - 0.72), 4) if ratio is not None else None
    weight_distance = abs(wght["default"] - 400) if wght else None
    line_heights = m.get("line_heights_normalised_by_source", [])
    metric_spread = round(max(line_heights) - min(line_heights), 4) if len(line_heights) > 1 else None

    return {
        "score": score, "reasons": reasons, "x_over_cap_ratio": ratio,
        "ratio_distance_from_ideal": ratio_distance,
        "weight_distance_from_400": weight_distance,
        "metric_spread": metric_spread,
    }


def score_bengali(m: dict) -> dict:
    score = 0
    reasons = []

    shaping = m.get("bengali_shaping_features_present", [])
    n_shaping = len(shaping)
    score += n_shaping   # 1 point per feature present, out of 11
    missing = sorted(set(["akhn", "rphf", "blwf", "half", "pstf", "vatu",
                          "pres", "abvs", "blws", "psts", "haln"]) - set(shaping))
    if missing:
        reasons.append(f"+{n_shaping} of 11 shaping features present; MISSING: "
                       f"{', '.join(missing)} -- these code points will not shape "
                       f"correctly without them")
    else:
        reasons.append(f"+{n_shaping} of 11 shaping features present -- complete")

    cov = m.get("bengali_sample_coverage", "0/0")
    covered, total = (int(x) for x in cov.split("/"))
    cov_pct = covered / total
    if cov_pct >= 0.98:
        score += 2
        reasons.append(f"+2 Bengali sample coverage {cov} -- essentially complete")
    else:
        reasons.append(f"+0 Bengali sample coverage {cov} -- {total - covered} sample "
                       f"code points missing from this font's cmap")

    return {"score": score, "reasons": reasons}


def latin_tie_break_key(e: dict):
    # Lower is better on every field here (score is negated to sort descending
    # alongside ascending tie-breaks). A missing figure gets the worst possible
    # value (999), never the best, so a font that was harder to measure is never
    # flattered by the gap in its own data.
    worst = 999
    r = e.get("ratio_distance_from_ideal")
    w = e.get("weight_distance_from_400")
    s = e.get("metric_spread")
    return (-e["score"], r if r is not None else worst,
            w if w is not None else worst, s if s is not None else worst)


def main():
    measurements = json.loads(MEASUREMENTS_PATH.read_text(encoding="utf-8"))["measurements"]
    rendered = json.loads(RENDERED_PATH.read_text(encoding="utf-8"))
    pairings = {p["bengali"]: p for p in rendered["sora_bengali_pairings"]}

    latin_ranked, mono_ranked = [], []
    bengali_body_ranked, bengali_display_ranked = [], []
    for m in measurements:
        if m["category"] in ("latin", "mono"):
            s = score_latin(m)
            entry = {**m, **s}
            (latin_ranked if m["category"] == "latin" else mono_ranked).append(entry)
        else:
            s = score_bengali(m)
            entry = {**m, **s}
            # Ranking a display-only face against a body face conflates two different
            # design roles -- Anek Bangla is GRU953's OWN incumbent optional display
            # face (BRAND-SPEC.md), not a body-text candidate, and was previously
            # ranked as if it were one. Each candidate's role (checked against Google
            # Fonts' own METADATA.pb / description text, or GRU953's own brand spec
            # where the two disagree) now sends it to one table, or to both when the
            # font's own source claims both purposes (Mina).
            role = m.get("role")
            if role in ("body", "dual"):
                bengali_body_ranked.append(entry)
            if role in ("display", "dual"):
                bengali_display_ranked.append(entry)
            if role not in ("body", "display", "dual"):
                # No role on record -- do not silently omit it from the comparison,
                # and do not silently guess either. It appears in both tables, flagged.
                bengali_body_ranked.append(entry)
                bengali_display_ranked.append(entry)

    latin_ranked.sort(key=latin_tie_break_key)
    mono_ranked.sort(key=latin_tie_break_key)
    bengali_body_ranked.sort(key=lambda e: -e["score"])
    bengali_display_ranked.sort(key=lambda e: -e["score"])

    L = []
    L.append("# GRU953 — typography recommendation")
    L.append("")
    L.append("GENERATED — do not hand-edit. Produced by `scripts/recommend.py` (well, "
             "`brand-kit/05_type/recommend.py`) from `measurements.json` and "
             "`rendered_measurements.json`. Change a verdict by fixing the measurement, "
             "never this file directly.")
    L.append("")
    L.append("## What this recommendation covers, and what it does not")
    L.append("")
    L.append("Scored: whether a font's three metric sources agree (a real cross-browser "
             "risk if not), whether a variable font's own default weight instance is "
             "normal (400), whether x-height/cap-height sits in the commonly cited "
             "well-balanced range (0.68-0.76), and — for Bengali — shaping-feature "
             "completeness and glyph coverage.")
    L.append("")
    L.append("**Not yet covered, and not invented here:** numeral distinguishability at "
             "small sizes (5/S, 3/8), how each face actually looks set as the GRU953 "
             "wordmark, and a real side-by-side legibility read. This recommendation is "
             "a partial input to the decision, not the whole of it.")
    L.append("")

    def render_table(title, ranked, is_bengali=False, note=None, show_tie_break=False):
        out = [f"## {title}", ""]
        if note:
            out.append(f"> {note}")
            out.append("")
        if not ranked:
            out.append("*No candidate carries this role.*")
            out.append("")
            return out
        winner = ranked[0]
        out.append(f"**Leading: {winner['family']}, score {winner['score']}**"
                   + (" — the incumbent." if winner.get("incumbent") else ""))
        out.append("")
        if winner["key"] == "geist":
            out.append(f"> {GEIST_BORROWED_ASSOCIATION_NOTE}")
            out.append("")
        for e in ranked:
            marker = "**" if e is winner else ""
            out.append(f"### {marker}{e['family']}{marker} — score {e['score']}"
                       + (" (incumbent)" if e.get("incumbent") else ""))
            for r in e["reasons"]:
                out.append(f"- {r}")
            if show_tie_break and e["score"] == winner["score"] and len(ranked) > 1:
                tied_count = sum(1 for x in ranked if x["score"] == e["score"])
                if tied_count > 1:
                    out.append(
                        f"- tied at score {e['score']} with {tied_count - 1} other "
                        f"candidate(s) -- tie-break order: ratio distance from ideal "
                        f"(0.72) = {e.get('ratio_distance_from_ideal')}, weight "
                        f"distance from 400 = {e.get('weight_distance_from_400')}, "
                        f"metric-source spread = {e.get('metric_spread')} (lower wins "
                        f"each, in that order)")
            if e["key"] == "geist":
                out.append(f"- **{GEIST_BORROWED_ASSOCIATION_NOTE}**")
            if is_bengali:
                if e.get("role_source"):
                    out.append(f"- role: **{e.get('role', 'unrecorded')}** "
                              f"({e['role_source']})")
                if e["family"] in pairings:
                    p = pairings[e["family"]]
                    out.append(f"- measured apparent-size multiplier against Sora: "
                              f"**{p['bengali_size_multiplier_needed']}x**")
            out.append("")
        return out

    L += render_table("Latin display / UI", latin_ranked, show_tie_break=True)
    L += render_table(
        "Bengali — body text", bengali_body_ranked, is_bengali=True,
        note=("Candidates whose own source names them for continuous/body-text "
              "reading, or (Mina) whose own description claims both purposes. "
              "Anek Bangla is deliberately absent here -- GRU953's own BRAND-SPEC.md "
              "designates it a display-only face; ranking it against a body face "
              "was the earlier methodological error this split fixes."))
    L += render_table(
        "Bengali — display / large headings", bengali_display_ranked, is_bengali=True,
        note=("Candidates whose own source (Google Fonts' category or description) "
              "or GRU953's own brand spec names them for display use, plus Mina in "
              "both tables for the same reason as above. Not a body-text ranking -- "
              "a display face is not penalised here for being unsuited to long-form "
              "reading, because that was never its job."))
    L += render_table("Monospace", mono_ranked, show_tie_break=True)

    OUT_PATH.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH.name}")
    print(f"  Latin leader: {latin_ranked[0]['family']} (score {latin_ranked[0]['score']})")
    if bengali_body_ranked:
        print(f"  Bengali body leader: {bengali_body_ranked[0]['family']} "
              f"(score {bengali_body_ranked[0]['score']})")
    if bengali_display_ranked:
        print(f"  Bengali display leader: {bengali_display_ranked[0]['family']} "
              f"(score {bengali_display_ranked[0]['score']})")
    print(f"  Mono leader: {mono_ranked[0]['family']} (score {mono_ranked[0]['score']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
