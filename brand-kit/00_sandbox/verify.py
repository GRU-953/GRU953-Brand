#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""GRU953 — kit verification.

Mechanically checks the things that can be checked mechanically, and prints a pass/fail
line for each. Anything that cannot be checked by a machine is listed at the end as an
explicit gap rather than silently passing.

Run:  python3 00_sandbox/verify.py
"""
import json, pathlib, re, subprocess, sys
from coloraide import Color
from fontTools.ttLib import TTFont
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
ok, bad, warn = [], [], []


def check(name, passed, detail=""):
    (ok if passed else bad).append(f"{name}" + (f" — {detail}" if detail else ""))


def note(name, detail=""):
    warn.append(f"{name}" + (f" — {detail}" if detail else ""))


# ---------------------------------------------------------------- 1. contrast, recomputed
TOK = json.loads((ROOT / "08_guidebook/assets/tokens.json").read_text())
INK, PAPER = TOK["ground"]["ink"], TOK["ground"]["paper"]
M = TOK["families"]["meridian"]["anchor"]
D = TOK["families"]["daybreak"]["anchor"]
E = TOK["families"]["ember"]["anchor"]
ACC = TOK["accent"]

# The signature is one hue with two values. Check BOTH against their own ground — this is
# the check the old kit did not have, and its absence is how an accent measuring 1.83:1 on
# white shipped as "the signature".
check("signature works on light grounds", round(Color(ACC["light"]).contrast(PAPER), 2) >= 4.5,
      f'{ACC["light"]} = {round(Color(ACC["light"]).contrast(PAPER), 2)}:1 on paper')
check("signature works on dark grounds", round(Color(ACC["dark"]).contrast(INK), 2) >= 4.5,
      f'{ACC["dark"]} = {round(Color(ACC["dark"]).contrast(INK), 2)}:1 on ink')
check("the signature's two values are one hue", ACC["hue_drift_degrees"] <= 6.0,
      f'{ACC["hue_drift_degrees"]}\u00b0 apart')

for label, fg, bg, target in [
        ("white on Meridian", PAPER, M, 4.5), ("Daybreak on Meridian", D, M, 4.5),
        ("Ember on Meridian", E, M, 4.5), ("Ink on Daybreak", INK, D, 4.5),
        ("Ink on Ember", INK, E, 4.5), ("Meridian on paper", M, PAPER, 4.5),
        ("Daybreak on Ink", D, INK, 4.5), ("Ink on paper", INK, PAPER, 4.5)]:
    r = round(Color(fg).contrast(bg), 2)
    check(f"contrast · {label}", r >= target, f"{r}:1 (needs {target}:1)")

# every semantic role pair that carries text
for theme, pairs in {
    "light": [("ink", "bg"), ("ink-muted", "bg"), ("ink-subtle", "bg"), ("link", "bg"),
              ("link-visited", "bg"), ("accent", "bg"), ("brand", "bg"),
              ("info", "bg"), ("success", "bg"), ("warning", "bg"), ("danger", "bg"),
              ("on-brand", "brand"), ("on-accent", "accent"), ("ink", "surface"),
              ("ink", "surface-raised"), ("ink", "bg-subtle")],
    "dark": [("ink", "bg"), ("ink-muted", "bg"), ("ink-subtle", "bg"), ("link", "bg"),
             ("link-visited", "bg"), ("accent", "bg"), ("brand", "bg"),
             ("info", "bg"), ("success", "bg"), ("warning", "bg"), ("danger", "bg"),
             ("on-brand", "brand"), ("on-accent", "accent"), ("ink", "surface"),
             ("ink", "surface-raised"), ("ink", "bg-subtle")],
}.items():
    roles = TOK["roles"][theme]
    for fgk, bgk in pairs:
        r = round(Color(roles[fgk]).contrast(roles[bgk]), 2)
        check(f"role contrast · {theme}: {fgk} on {bgk}", r >= 4.5,
              f"{r}:1 ({roles[fgk]} on {roles[bgk]})")

# ramp monotonicity, independently of the engine that produced them
for fam, spec in TOK["families"].items():
    ls = [Color(spec["ramp"][k]).convert("oklch")["lightness"]
          for k in sorted(spec["ramp"], key=lambda x: int(x))]
    check(f"ramp monotonic · {fam}", all(a >= b - 1e-9 for a, b in zip(ls, ls[1:])),
          f"{len(ls)} steps")
    if spec.get("anchor"):
        anchor_in = spec["anchor"].upper() in [v.upper() for v in spec["ramp"].values()]
        check(f"anchor inside ramp · {fam}", anchor_in, spec["anchor"])

# every UI part that must be seen, in both themes, at the 3:1 non-text threshold
for theme in ("light", "dark"):
    roles = TOK["roles"][theme]
    for k in ("border-strong", "focus", "accent-ui", "info-border", "success-border",
              "warning-border", "danger-border"):
        r = round(Color(roles[k]).contrast(roles["bg"]), 2)
        check(f"ui contrast · {theme}: {k}", r >= 3.0, f"{r}:1 (needs 3:1)")

# chart series must be legible AND mutually distinguishable
for theme in ("light", "dark"):
    ser = TOK["charts"][theme]
    for sgm in ser:
        check(f"chart · {theme}: {sgm['name']}", sgm["ratio"] >= 3.0, f"{sgm['ratio']}:1")
    worst = min((round(Color(a["hex"]).delta_e(b["hex"], method="2000"), 1), a["name"], b["name"])
                for i, a in enumerate(ser) for b in ser[i + 1:])
    check(f"chart series distinguishable · {theme}", worst[0] >= 10.0,
          f"closest pair {worst[1]}/{worst[2]} at \u0394E {worst[0]}")

# every semantic role must exist in BOTH themes, or the dark theme is not really finished
missing = sorted(set(TOK["roles"]["light"]) ^ set(TOK["roles"]["dark"]))
check("every role is defined in both themes", not missing,
      f"{len(TOK['roles']['light'])} roles each" if not missing else f"missing: {missing}")

# ---------------------------------------------------------------- 2. every SVG parses
svgs = sorted((ROOT / "03_logo").glob("*.svg")) + \
       sorted((ROOT / "06_assets/favicon").glob("*.svg"))
for p in svgs:
    try:
        ET.fromstring(p.read_text())
        s = p.read_text()
        has_label = "<title" in s or 'aria-label' in s
        vb = 'viewBox="' in s
        check(f"svg · {p.name}", has_label and vb,
              f"{p.stat().st_size} bytes"
              + ("" if has_label else " MISSING <title>")
              + ("" if vb else " MISSING viewBox"))
    except ET.ParseError as e:
        check(f"svg · {p.name}", False, f"will not parse: {e}")

# recolourability: currentColor must survive optimisation on the marks
for n in ("GRU953-bird.svg", "GRU953-lockup-horizontal.svg",
          "GRU953-lockup-horizontal-tagline.svg", "GRU953-lockup-stacked.svg",
          "GRU953-lockup-stacked-tagline.svg", "GRU953-wordmark.svg",
          "GRU953-tagline.svg"):
    s = (ROOT / "03_logo" / n).read_text()
    check(f"recolourable · {n}", "currentColor" in s)

# ---------------------------------------------------------------- 3. CSS parses
node = subprocess.run(
    ["node", "-e", """
const t=require('css-tree'),fs=require('fs'),out=[];
for(const f of process.argv.slice(1)){
  let e=[]; t.parse(fs.readFileSync(f,'utf8'),{onParseError:x=>e.push(x.message)});
  out.push([f.split('/').pop(), e.length]);
}
console.log(JSON.stringify(out));
"""] + [str(ROOT / "08_guidebook/assets" / f)
        for f in ("tokens.css", "typography.css", "layout.css")],
    cwd=ROOT / "00_sandbox", capture_output=True, text=True)
try:
    for name, errs in json.loads(node.stdout.strip().splitlines()[-1]):
        check(f"css parses · {name}", errs == 0, f"{errs} parse errors")
except Exception:
    note("css parse check could not run", node.stderr.strip()[:120])

# ---------------------------------------------------------------- 4. fonts and licences
FONTS = ROOT / "08_guidebook/assets/fonts"
w2 = sorted(FONTS.glob("*.woff2"))
check("webfonts present", len(w2) == 5, f"{len(w2)} files, "
      f"{sum(f.stat().st_size for f in w2) // 1024} kB total")
for f in w2:
    # This used to be `check(name, True, ...)` — a check that could not fail, which is worse
    # than no check because it prints a tick. Actually open the file: a woff2 starts with the
    # signature "wOF2", and fontTools will refuse to parse a truncated one.
    try:
        head = f.read_bytes()[:4]
        TTFont(f)                      # parses the woff2 or raises
        check(f"webfont is a valid woff2 · {f.name}", head == b"wOF2",
              f"{f.stat().st_size // 1024} kB, signature {head!r}")
    except Exception as e:
        check(f"webfont is a valid woff2 · {f.name}", False, f"will not parse: {e}")
check("font licences shipped", len(list(FONTS.glob("OFL-*.txt"))) == 5,
      f"{len(list(FONTS.glob('OFL-*.txt')))} OFL files")
# source-fonts/, not candidates/. The five SHIPPING families live in source-fonts; the
# candidates folder held a second copy of them beside the four typefaces that were
# considered and rejected. Checking the copy meant the check passed on a tree that had the
# duplicates and failed on one that had only the fonts actually used — which is backwards.
for src, name in [("05_type/source-fonts/Sora/Sora[wght].ttf", "Sora"),
                  ("05_type/source-fonts/Noto_Sans/NotoSans[wdth,wght].ttf", "Noto Sans"),
                  ("05_type/source-fonts/Noto_Sans_Bengali/NotoSansBengali[wdth,wght].ttf",
                   "Noto Sans Bengali"),
                  ("05_type/source-fonts/JetBrains_Mono/JetBrainsMono[wght].ttf",
                   "JetBrains Mono"),
                  ("05_type/source-fonts/Anek_Bangla/AnekBangla[wdth,wght].ttf",
                   "Anek Bangla")]:
    p = ROOT / src
    if not p.exists():
        check(f"font source · {name}", False, "missing")
        continue
    lic = TTFont(p)["name"].getDebugName(13) or ""
    check(f"font is OFL 1.1 · {name}", "SIL Open Font License" in lic and "1.1" in lic,
          lic[:52])

# ---------------------------------------------------------------- 5. the guidebook itself
GB = ROOT / "08_guidebook/GRU953-Brand-Guidebook.html"
if GB.exists():
    h = GB.read_text()
    # Not `check(..., True, ...)`. A file that exists is not the same as a guidebook: assert
    # it is a real HTML document of a plausible size for one with every asset embedded.
    check("guidebook built", h.lstrip().lower().startswith("<!doctype html")
          and "</html>" in h[-2000:] and GB.stat().st_size > 2_000_000,
          f"{GB.stat().st_size // 1024} kB, well-formed document")
    check("guidebook is self-contained",
          not re.search(r'(src|href)="(?!data:|#|https?://)[^"]+"', h),
          "no unresolved local references")
    check("guidebook fonts embedded", h.count("data:font/woff2") >= 5,
          f"{h.count('data:font/woff2')} embedded font faces")
    check("guidebook has no unwritten chapters", 'class="pending"' not in h)
    check("guidebook declares language", 'html lang="en"' in h)
    bn_count = h.count('lang="bn"')
    check("guidebook marks Bangla", bn_count > 50, f"{bn_count} Bangla-marked elements")
    check("guidebook has skip link", 'class="skip"' in h)
    check("guidebook has print styles", "@media print" in h)
    # Check the SOURCES, not the built file: base64 font data contains arbitrary letter
    # runs and will match "XXX" by chance, which is a false alarm every time.
    srcs = list((ROOT / "08_guidebook/chapters").glob("*.md")) + \
           list((ROOT / "02_strategy").glob("*.md")) + \
           list((ROOT / "07_templates").glob("*.md")) + \
           list((ROOT / "08_guidebook/governance").glob("*.md")) + \
           list((ROOT / "08_guidebook/assets").glob("*.css"))
    dirty = [p.name for p in srcs
             if re.search(r"lorem ipsum|\bTODO\b|\bFIXME\b", p.read_text(errors="replace"))]
    check("no lorem or TODO in any source", not dirty, ", ".join(dirty) or "clean")
    # Exclude anything inside <code>: the guidebook legitimately EXPLAINS the
    # [placeholder] convention, and quoting the convention is not the same as leaving
    # an unfilled blank in prose.
    prose = re.sub(r"<code>.*?</code>", "", h, flags=re.S)
    stray = re.findall(r"\[(?:your|insert|placeholder|name here)[^\]]*\]", prose, re.I)
    check("no unfilled placeholder left in guidebook prose", not stray,
          f"{len(stray)} found: {stray[:2]}" if stray else "clean")
else:
    check("guidebook built", False, "file missing")

PDF = ROOT / "08_guidebook/GRU953-Brand-Guidebook.pdf"
check("guidebook PDF built", PDF.exists(),
      f"{PDF.stat().st_size // 1024} kB" if PDF.exists() else "missing")

# ---------------------------------------------------------------- 6. deliverables present
EXPECTED = [
    "START-HERE.md", "02_strategy/BRAND-SPEC.md", "02_strategy/DESIGN-RULES.md",
    "02_strategy/VERBAL-IDENTITY.md", "02_strategy/VERBAL-IDENTITY-BN.md",
    "01_research/RESEARCH.md", "04_colour/CONTRAST.md",
    "08_guidebook/assets/tokens.css", "08_guidebook/assets/tokens.json",
    "08_guidebook/assets/typography.css", "08_guidebook/assets/layout.css",
    "08_guidebook/governance/LICENSE", "08_guidebook/governance/NOTICE",
    "08_guidebook/governance/LICENSING-EXPLAINED.md",
    "08_guidebook/governance/TRADEMARKS.md",
    "08_guidebook/governance/LOGO-USAGE.md",
    "08_guidebook/governance/LICENSE-GUIDEBOOK.md",
    "07_templates/github-profile-README.md", "07_templates/repo-README-template.md",
    "07_templates/CV-content.md", "07_templates/email-signature.md",
    "07_templates/invoice-and-proposal-copy.md", "07_templates/social-copy.md",
    "06_assets/outreach/github-social-preview.png", "06_assets/outreach/avatar-512.png",
    "06_assets/outreach/og-card-1200x630.png", "06_assets/favicon/favicon.ico",
    "03_logo/GRU953-bird.svg", "03_logo/GRU953-appicon.svg",
    "03_logo/GRU953-lockup-horizontal.svg", "03_logo/GRU953-lockup-horizontal-tagline.svg",
    "03_logo/GRU953-lockup-stacked.svg", "03_logo/GRU953-lockup-stacked-tagline.svg",
    "03_logo/GRU953-wordmark.svg", "03_logo/GRU953-tagline.svg",
]
for rel in EXPECTED:
    check(f"deliverable · {rel}", (ROOT / rel).exists())

# ---------------------------------------------------- 6b. no stale references, no versions
# The kit is identified by date. Any kit version number, or any reference to a superseded
# edition or a deleted mark build, is a defect — this is the check that catches the ones a
# hand-edit misses.
STALE = re.compile(r"\bv[5-9]\.\d+\.\d+\b|\bGRU953-bird-(detail|core|glyph)\b"
                   r"|\blockup-horizontal-(detail|core)\b|\bLOCKED-SPEC\b"
                   r"|\bv5-tokens\b|\b10_v5_archive\b", re.I)
stale_hits = []
for p in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.py")) + list(ROOT.rglob("*.mjs")) \
         + list(ROOT.rglob("*.css")) + list(ROOT.rglob("*.json")):
    # 09_delivery is NOT skipped. It used to be, and that is exactly how a packaged zip and
    # a verification report describing a build with three separate bird drawings survived two
    # full audit rounds: the one folder whose job is to carry a snapshot of everything else
    # was the one folder nobody checked.
    if any(x in p.parts for x in ("node_modules", "candidates", "__pycache__")):
        continue
    # The two checkers have to NAME the forbidden strings in order to look for them.
    if p.name in ("verify.py", "check.mjs"):
        continue
    for i, ln in enumerate(p.read_text(errors="replace").splitlines(), 1):
        if STALE.search(ln):
            stale_hits.append(f"{p.relative_to(ROOT)}:{i}")
check("no references to superseded editions or deleted marks", not stale_hits,
      f"{len(stale_hits)} found: {stale_hits[:3]}" if stale_hits else "clean")

# The taglines are locked. Both must appear, complete, in the guidebook and in the marks.
TAG_EN, TAG_BN = "Simple technology. For everyone.", "\u09b8\u09b9\u099c \u09aa\u09cd\u09b0\u09af\u09c1\u0995\u09cd\u09a4\u09bf\u0964 \u09b8\u09ac\u09be\u09b0 \u099c\u09a8\u09cd\u09af\u0964"
if GB.exists():
    hh = GB.read_text()
    check("tagline present and complete · English", hh.count(TAG_EN) >= 3,
          f"{hh.count(TAG_EN)} occurrences")
    check("tagline present and complete · Bangla", hh.count(TAG_BN) >= 3,
          f"{hh.count(TAG_BN)} occurrences")
for n in ("GRU953-tagline.svg", "GRU953-lockup-horizontal-tagline.svg",
          "GRU953-lockup-stacked-tagline.svg"):
    q = ROOT / "03_logo" / n
    if q.exists():
        t = q.read_text()
        check(f"tagline artwork is outlines, not live text · {n}",
              "<text" not in t and TAG_EN in t,
              "both taglines in the accessible description, no live text")

# ------------------------------------------------- 6c. the social copy's own arithmetic
# social-copy.md states a character count for each of its twelve posts, and two of them sit
# right on X's 280-character limit. Those numbers went stale the moment the posts were edited.
SC = ROOT / "07_templates/social-copy.md"
if SC.exists():
    body = SC.read_text()
    blocks = re.findall(r"```text\n(.*?)```", body, re.S)
    claims = re.findall(r"^## ([123][a-d])\. [^—]+— ([\d,]+) characters\s*$", body, flags=re.M)
    if len(blocks) != len(claims):
        check("social copy claims a count for every post", False,
              f"{len(blocks)} posts, {len(claims)} counts")
    else:
        wrong = [(cid, int(c.replace(",", "")), len(b.strip()))
                 for (cid, c), b in zip(claims, blocks)
                 if int(c.replace(",", "")) != len(b.strip())]
        check("social copy's stated character counts are correct", not wrong,
              f"{len(blocks)} posts checked" if not wrong
              else "; ".join(f"{c}: says {a}, is {r}" for c, a, r in wrong))
        # Two separate things: the post must FIT, and the number the file PRINTS for it must
        # be right. Checking only the fit is how two wrong figures shipped once already.
        LINK = 23
        over, misprinted = [], []
        heads = re.findall(r"^## ([123][a-d])\. [^—]+— [\d,]+ characters\s*$",
                           body, flags=re.M)
        for (cid, _), b in zip(claims, blocks):
            t = b.strip()
            m = re.search(r"\[[^\]]+\]\s*$", t)
            n = len(t) - (len(m.group(0).strip()) if m else 0) + LINK
            if cid.endswith(("b", "d")) and n > 280:
                over.append(f"{cid}: {n}")
            # the prose figure between this heading and its code block
            a = body.index(f"## {cid}.")
            seg = body[a:body.index("```text", a)]
            printed = re.findall(r"\*\*([\d,]+)\*\*", seg)
            if printed and int(printed[-1].replace(",", "")) != n:
                misprinted.append(f"{cid}: prints {printed[-1]}, is {n}")
        check("every short post still fits X with a real link", not over,
              "all within 280" if not over else "; ".join(over))
        check("the stated with-a-real-link figures are correct", not misprinted,
              "every printed figure matches" if not misprinted else "; ".join(misprinted))

# ---------------------------------------------------------------- 7. naming discipline
for p in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.css")):
    if "00_sandbox" in str(p) or "candidates" in str(p) or "01_research" in str(p):
        continue
    t = p.read_text(errors="replace")
    # The kit deliberately QUOTES the wrong spellings as counter-examples, so only flag a
    # match that is not on a line marking it as wrong. Otherwise this fires on every
    # "never write it like this" table and the check becomes noise.
    # A line that QUOTES a wrong spelling is teaching the rule, not breaking it. Detect the
    # quoting itself as well as the warning words, otherwise every "never write it like
    # this" table fires and the check becomes noise nobody reads.
    NEG = re.compile(r"never|not\b|wrong|avoid|incorrect|don.t|❌|✗|instead"
                     r"|[\"“”`]\s*(Gru953|GRU 953|gru-953)", re.I)
    hits = [ln.strip()[:70] for ln in t.splitlines()
            if re.search(r"\bGru953\b|\bGRU 953\b|\bGRU_953\b", ln) and not NEG.search(ln)]
    if hits:
        note(f"name style · {p.relative_to(ROOT)}", f"{len(hits)} unexplained: {hits[0]}")

# ---------------------------------------------------------------- report
print("\n" + "=" * 78)
print(f"GRU953 — verification:  {len(ok)} passed, {len(bad)} failed, "
      f"{len(warn)} to look at by hand")
print("=" * 78)
if bad:
    print("\nFAILED — do not ship until these are fixed:")
    for b in bad:
        print(f"  ✗ {b}")
if warn:
    print("\nLOOK AT BY HAND:")
    for w in warn:
        print(f"  ! {w}")
print("\nPASSED:")
for o in ok:
    print(f"  ✓ {o}")

print("""
CANNOT BE CHECKED BY A MACHINE — stated rather than silently passed:
  · Whether the guidebook has been read by a real screen-reader user. It has not.
  · Whether the Bangla reads naturally to a native speaker. Written as an original,
    but not reviewed by a second Bangla speaker.
  · Whether Meridian and Daybreak feel right to Aninda. Only he can say.
  · Trademark clearance outside the USA (Bangladesh DPDT, EUIPO, WIPO) — needs a
    human search, and a trademark attorney if GRU953 ever becomes commercial.
  · Whether GitHub/X will actually release the `gru953` handles: a 404 is a strong
    signal, not a guarantee.""")
sys.exit(1 if bad else 0)
