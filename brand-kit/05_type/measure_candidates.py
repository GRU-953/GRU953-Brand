#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Measure every typography candidate directly from its font file.

Nothing here comes from a foundry's marketing page or a secondhand summary.
Every figure is read with fontTools from the actual .ttf bytes fetched by
fetch_candidates.py. This is the FILE-based half of the measurement; the
RENDERED half (real ink extents in a browser) is a separate pass, because a
font's own declared metrics and what a browser actually draws are two
different facts, and the gap between them is exactly where bugs live.

WHAT IS MEASURED, AND WHY EACH THING MATTERS
---------------------------------------------
- unitsPerEm, x-height, cap-height: the raw numbers a "16px body text" claim
  actually rests on. Two fonts both set at 16px can have visibly different
  apparent size if their x-height-to-em ratios differ.
- THREE metric sources (hhea, OS/2.typo*, OS/2.usWin*) AND whether they
  agree: mismatched metrics are a real, documented cause of a font rendering
  with a different line-box height in different browsers, because each
  engine has its own rule for which of the three it trusts.
- Variable axes and their ranges: whether a claimed "weight 100-800" axis
  genuinely spans that range, and whether the specific weight the brand
  would use is a real instance or an interpolated guess.
- Bengali shaping-feature coverage in GSUB (akhn, rphf, blwf, half, pstf,
  vatu, pres, abvs, blws, psts, haln): a Bengali font MISSING these does not
  shape correctly, it merely renders code points as separate glyphs -- this
  is the difference between a font that can set Bengali and one that cannot.
- Reserved Font Name (name IDs 0, 13, 14): decides whether a subset of this
  font could keep its own name if GRU953 ever needed to modify it.

Run:  python3 brand-kit/05_type/measure_candidates.py
"""
import json
import pathlib
import sys

from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).resolve().parent
REGISTRY_PATH = HERE / "candidates_registry.json"
CANDIDATES_DIR = HERE / "candidates"
OUT_PATH = HERE / "measurements.json"

# The Bengali shaping features a font must carry to shape Bengali correctly,
# not merely render its code points as separate, wrong-order glyphs.
BENGALI_SHAPING_FEATURES = ["akhn", "rphf", "blwf", "half", "pstf", "vatu",
                            "pres", "abvs", "blws", "psts", "haln"]

# A representative sample from the Bengali Unicode block (U+0980-U+09FF),
# covering vowels, consonants, vowel signs and digits -- enough to say
# whether a font's cmap covers the script, not just a few letters of it.
#
# Filtered through unicodedata to keep only codepoints the Unicode Standard
# actually ASSIGNS a character to. A blind range(0x0980, 0x09E0) once included
# 29 genuinely unassigned gaps in the Bengali block (U+0984, U+098D-098E,
# U+09A9, U+09B1... reserved, not missing) -- and every single one of 8
# Bengali candidates then "failed" to cover them, because no real font maps
# a codepoint nothing has ever been assigned to. That made the coverage
# score meaningless: it scored the same 0 whether a font was excellent or
# broken. Filtering to only-assigned codepoints is what makes the remaining
# score mean something again.
import unicodedata as _unicodedata
BENGALI_SAMPLE_CODEPOINTS = [
    cp for cp in list(range(0x0980, 0x09E0)) + list(range(0x09E6, 0x09FA))
    if _unicodedata.category(chr(cp)) != "Cn"  # Cn = "Unassigned"
]


def find_font_file(key: str, spec: dict) -> pathlib.Path:
    fam_dir = CANDIDATES_DIR / key
    candidates = list(fam_dir.glob("*.ttf"))
    return candidates[0] if candidates else None


def measure_one(key: str, spec: dict, path: pathlib.Path) -> dict:
    font = TTFont(str(path), lazy=True)
    upm = font["head"].unitsPerEm

    os2 = font.get("OS/2")
    hhea = font.get("hhea")

    x_height = getattr(os2, "sxHeight", None) if os2 else None
    cap_height = getattr(os2, "sCapHeight", None) if os2 else None

    metric_sources = {}
    if hhea:
        metric_sources["hhea"] = {
            "ascender": hhea.ascender, "descender": hhea.descender,
            "lineGap": hhea.lineGap,
        }
    if os2:
        metric_sources["os2_typo"] = {
            "ascender": os2.sTypoAscender, "descender": os2.sTypoDescender,
            "lineGap": os2.sTypoLineGap,
        }
        metric_sources["os2_win"] = {
            "ascent": os2.usWinAscent, "descent": os2.usWinDescent,
        }

    # Do the three sources agree, normalised to a fraction of the em? A
    # mismatch here is exactly the kind of thing that makes one browser's
    # line box taller than another's for the identical font at the identical
    # size.
    line_heights_normalised = []
    if "hhea" in metric_sources:
        h = metric_sources["hhea"]
        line_heights_normalised.append(
            round((h["ascender"] - h["descender"] + h["lineGap"]) / upm, 4))
    if "os2_typo" in metric_sources:
        t = metric_sources["os2_typo"]
        line_heights_normalised.append(
            round((t["ascender"] - t["descender"] + t["lineGap"]) / upm, 4))
    if "os2_win" in metric_sources:
        w = metric_sources["os2_win"]
        line_heights_normalised.append(
            round((w["ascent"] + w["descent"]) / upm, 4))
    metrics_agree = (max(line_heights_normalised) - min(line_heights_normalised) < 0.02
                      if len(line_heights_normalised) > 1 else None)

    # Variable axes
    axes = []
    if "fvar" in font:
        for a in font["fvar"].axes:
            axes.append({"tag": a.axisTag, "min": a.minValue,
                         "default": a.defaultValue, "max": a.maxValue})
        instances = [
            {"name": font["name"].getDebugName(inst.subfamilyNameID),
             "coords": inst.coordinates}
            for inst in font["fvar"].instances
        ]
    else:
        instances = []

    # Glyph coverage -- Latin-1 basics, and Bengali if this is a Bengali font.
    cmap = font.getBestCmap() or {}
    latin_basic = list(range(0x20, 0x7F))
    latin_covered = sum(1 for cp in latin_basic if cp in cmap)

    bengali_covered = sum(1 for cp in BENGALI_SAMPLE_CODEPOINTS if cp in cmap)
    bengali_total = len(BENGALI_SAMPLE_CODEPOINTS)

    # Bengali shaping features actually present in GSUB.
    shaping_features_present = []
    if "GSUB" in font:
        try:
            feature_list = font["GSUB"].table.FeatureList
            if feature_list:
                tags = {fr.FeatureTag for fr in feature_list.FeatureRecord}
                shaping_features_present = sorted(
                    f for f in BENGALI_SHAPING_FEATURES if f in tags)
        except Exception:
            pass

    # Reserved Font Name -- name IDs 0 (copyright), 13 (licence), 14 (licence URL)
    # often name an RFN explicitly; a simple, honest heuristic: does the licence
    # description (name ID 13, "OFL.txt" body already fetched separately) or the
    # family name itself get referenced as reserved. fontTools doesn't parse RFN
    # semantics from the name table alone -- that's stated in OFL.txt's own
    # prose, checked separately by check_licence_claims.py-style tooling. Record
    # what IS mechanically available: the exact family name string, so a later
    # cross-reference against each OFL.txt's declared RFN is exact, not fuzzy.
    name_table = font["name"]
    family_name = name_table.getDebugName(1) or name_table.getDebugName(16)

    return {
        "key": key, "family": spec["family"], "incumbent": spec.get("incumbent", False),
        "role": spec.get("role"), "role_source": spec.get("role_source"),
        "file": str(path.relative_to(HERE)),
        "units_per_em": upm,
        "x_height": x_height,
        "cap_height": cap_height,
        "x_height_over_em": round(x_height / upm, 4) if x_height else None,
        "cap_height_over_em": round(cap_height / upm, 4) if cap_height else None,
        "metric_sources": metric_sources,
        "line_heights_normalised_by_source": line_heights_normalised,
        "metric_sources_agree_within_2pct": metrics_agree,
        "variable_axes": axes,
        "named_instances": instances,
        "latin_basic_coverage": f"{latin_covered}/{len(latin_basic)}",
        "bengali_sample_coverage": f"{bengali_covered}/{bengali_total}",
        "bengali_shaping_features_present": shaping_features_present,
        "family_name_in_font": family_name,
    }


def main():
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    results = []
    could_not_measure = []

    for category, families in registry["candidates"].items():
        for key, spec in families.items():
            path = find_font_file(key, spec)
            if not path:
                could_not_measure.append({"key": key, "family": spec["family"],
                                          "reason": "font file not found"})
                continue
            try:
                m = measure_one(key, spec, path)
                m["category"] = category
                results.append(m)
                print(f"  {spec['family']}: upm={m['units_per_em']} "
                      f"x-height/em={m['x_height_over_em']} "
                      f"cap/em={m['cap_height_over_em']} "
                      f"metrics_agree={m['metric_sources_agree_within_2pct']}")
                if category == "bengali":
                    print(f"    Bengali coverage {m['bengali_sample_coverage']}, "
                          f"shaping features: {m['bengali_shaping_features_present']}")
            except Exception as e:
                could_not_measure.append({"key": key, "family": spec["family"],
                                          "reason": f"{type(e).__name__}: {e}"})

    out = {
        "$note": "File-based measurements only -- from the actual .ttf bytes via "
                 "fontTools, never a marketing page. The RENDERED half (real ink "
                 "extents, the Latin-to-Bangla apparent-size multiplier) is a "
                 "separate pass. Regenerate: "
                 "python3 brand-kit/05_type/measure_candidates.py",
        "measured_count": len(results), "could_not_measure_count": len(could_not_measure),
        "measurements": results, "could_not_measure": could_not_measure,
    }
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")
    print(f"\n{len(results)} measured, {len(could_not_measure)} could not be measured.")
    if could_not_measure:
        for c in could_not_measure:
            print(f"  {c['family']}: {c['reason']}")
    return 0 if not could_not_measure else 1


if __name__ == "__main__":
    sys.exit(main())
