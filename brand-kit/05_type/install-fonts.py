#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Install the three instanced fonts that 03_logo/lockups.py needs.

WHY THIS EXISTS
---------------
The taglines in the lockups are converted to outlines by Inkscape, because Bangla needs
real text shaping — conjuncts join, and some vowel signs are written before the consonant
they follow. Inkscape shapes through HarfBuzz and gets that right; pulling glyphs out of a
font by code point does not.

Inkscape finds fonts through fontconfig, and fontconfig has a dangerous habit: ask it for a
family it does not have and it silently hands back whatever it thinks is closest. No error,
no warning — just the wrong typeface, outlined into a mark that then looks almost right.

So the three faces are installed here under UNIQUE family names that nothing else can
match. A variable font installed system-wide under its real name ("Noto Sans Bengali")
could still be resolved at the wrong weight; "GRUNotoBengaliFive" can only be one thing.

Run:  python3 05_type/install-fonts.py && fc-cache -f
Then: cd 03_logo && python3 lockups.py
"""
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
import pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
DEST = pathlib.Path.home() / ".fonts"

JOBS = [
    ("Sora/Sora[wght].ttf", {"wght": 700}, "GRU-Sora-700.ttf", "GRUSoraSeven"),
    ("Noto_Sans/NotoSans[wdth,wght].ttf", {"wght": 500, "wdth": 100},
     "GRU-NotoSans-500.ttf", "GRUNotoSansFive"),
    ("Noto_Sans_Bengali/NotoSansBengali[wdth,wght].ttf", {"wght": 500, "wdth": 100},
     "GRU-NotoSansBengali-500.ttf", "GRUNotoBengaliFive"),
]

DEST.mkdir(parents=True, exist_ok=True)
for rel, location, filename, family in JOBS:
    src = HERE / "source-fonts" / rel
    if not src.exists():
        sys.exit(f"FAIL — {src} is missing. The source fonts must be in 05_type/source-fonts/.")
    f = instancer.instantiateVariableFont(TTFont(str(src)), location)
    nt = f["name"]
    # Strip every name record that fontconfig could match on, then set exactly one family
    # name. Leaving the original records in place is how two files end up claiming the same
    # family and fontconfig picks whichever it saw first.
    for rec in list(nt.names):
        if rec.nameID in (1, 3, 4, 6, 16, 17, 21, 22):
            nt.removeNames(rec.nameID, rec.platformID, rec.platEncID, rec.langID)
    for nid, value in ((1, family), (2, "Regular"), (4, family), (6, family)):
        nt.setName(value, nid, 3, 1, 0x409)
        nt.setName(value, nid, 1, 0, 0)
    f.save(str(DEST / filename))
    print(f"installed {filename:32s} as family {family}")

subprocess.run(["fc-cache", "-f"], capture_output=True)
bad = []
for *_, family in JOBS:
    r = subprocess.run(["fc-match", "-f", "%{family}", family], capture_output=True, text=True)
    ok = family.lower() in r.stdout.lower()
    print(f"  fc-match {family:22s} -> {r.stdout.strip():24s} {'OK' if ok else 'WRONG'}")
    if not ok:
        bad.append(family)
if bad:
    sys.exit(f"FAIL — fontconfig still resolves {bad} to something else. "
             f"Run `fc-cache -f` and try again.")
print("\nAll three families resolve to themselves. 03_logo/lockups.py can now run.")
print("These fonts are SIL Open Font Licence 1.1, like their sources. Instancing a variable")
print("font is a permitted modification; the licence travels with the source files in")
print("05_type/source-fonts/, each beside its own OFL.txt.")
