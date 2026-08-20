#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""GRU953 — the mechanical half of a brand review.

This finds the boring failures exactly, so a human's attention goes to the
interesting ones. Every contrast figure is MEASURED from the values in the file,
not asserted; the WCAG formula is implemented here in four lines rather than
pulled from a dependency, so this runs anywhere Python does.

What it cannot check, it says it cannot check. A checker that quietly omits its
own blind spots reads as a clean bill of health, which is worse than a gap.

    python3 check.py path/to/file-or-directory
    python3 check.py . --html          # also parse HTML for accessibility basics
    python3 check.py . --json          # machine-readable, for CI
    python3 check.py . --quiet         # findings only, no summary
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

# ---------------------------------------------------------------- the brand, as data
PAPER, INK = "#FFFFFF", "#0B0E14"
MERIDIAN, ACCENT_LIGHT, ACCENT_DARK, EMBER = "#1A1753", "#B45A39", "#FFAB8E", "#EDB24D"
TAG_EN = "Simple technology. For everyone."
TAG_BN = "সহজ প্রযুক্তি। সবার জন্য।"

# hex -> (the token to use, a note for the human). The note is kept OUT of the
# token name, so the suggested fix is something that can be pasted verbatim.
TOKEN_FOR = {
    "#1a1753": ("--gru-brand", ""),
    "#b45a39": ("--gru-accent", "resolves to this in the light theme"),
    "#ffab8e": ("--gru-accent", "resolves to this in the dark theme"),
    "#edb24d": ("--gru-warning", "Ember also serves as the warning colour"),
    "#0b0e14": ("--gru-ink", ""),
    "#343583": ("--gru-brand-hover", ""),
}
NAMED = {
    "transparent": None, "currentcolor": None, "inherit": None, "initial": None,
    "unset": None, "revert": None, "revert-layer": None, "auto": None,
    # The CSS named colours, in full. Two of them used to be here and the rest were
    # silently unmeasurable: `.a{color:red;background:white}` is 4.00:1 and produced no
    # finding, while `#FF0000` on `#FFFFFF` produced a major. Same colours, same file.
    "aliceblue": "#F0F8FF", "antiquewhite": "#FAEBD7", "aqua": "#00FFFF",
    "aquamarine": "#7FFFD4", "azure": "#F0FFFF", "beige": "#F5F5DC", "bisque": "#FFE4C4",
    "black": "#000000", "blanchedalmond": "#FFEBCD", "blue": "#0000FF",
    "blueviolet": "#8A2BE2", "brown": "#A52A2A", "burlywood": "#DEB887",
    "cadetblue": "#5F9EA0", "chartreuse": "#7FFF00", "chocolate": "#D2691E",
    "coral": "#FF7F50", "cornflowerblue": "#6495ED", "cornsilk": "#FFF8DC",
    "crimson": "#DC143C", "cyan": "#00FFFF", "darkblue": "#00008B", "darkcyan": "#008B8B",
    "darkgoldenrod": "#B8860B", "darkgray": "#A9A9A9", "darkgrey": "#A9A9A9",
    "darkgreen": "#006400", "darkkhaki": "#BDB76B", "darkmagenta": "#8B008B",
    "darkolivegreen": "#556B2F", "darkorange": "#FF8C00", "darkorchid": "#9932CC",
    "darkred": "#8B0000", "darksalmon": "#E9967A", "darkseagreen": "#8FBC8F",
    "darkslateblue": "#483D8B", "darkslategray": "#2F4F4F", "darkslategrey": "#2F4F4F",
    "darkturquoise": "#00CED1", "darkviolet": "#9400D3", "deeppink": "#FF1493",
    "deepskyblue": "#00BFFF", "dimgray": "#696969", "dimgrey": "#696969",
    "dodgerblue": "#1E90FF", "firebrick": "#B22222", "floralwhite": "#FFFAF0",
    "forestgreen": "#228B22", "fuchsia": "#FF00FF", "gainsboro": "#DCDCDC",
    "ghostwhite": "#F8F8FF", "gold": "#FFD700", "goldenrod": "#DAA520", "gray": "#808080",
    "grey": "#808080", "green": "#008000", "greenyellow": "#ADFF2F",
    "honeydew": "#F0FFF0", "hotpink": "#FF69B4", "indianred": "#CD5C5C",
    "indigo": "#4B0082", "ivory": "#FFFFF0", "khaki": "#F0E68C", "lavender": "#E6E6FA",
    "lavenderblush": "#FFF0F5", "lawngreen": "#7CFC00", "lemonchiffon": "#FFFACD",
    "lightblue": "#ADD8E6", "lightcoral": "#F08080", "lightcyan": "#E0FFFF",
    "lightgoldenrodyellow": "#FAFAD2", "lightgray": "#D3D3D3", "lightgrey": "#D3D3D3",
    "lightgreen": "#90EE90", "lightpink": "#FFB6C1", "lightsalmon": "#FFA07A",
    "lightseagreen": "#20B2AA", "lightskyblue": "#87CEFA", "lightslategray": "#778899",
    "lightslategrey": "#778899", "lightsteelblue": "#B0C4DE", "lightyellow": "#FFFFE0",
    "lime": "#00FF00", "limegreen": "#32CD32", "linen": "#FAF0E6", "magenta": "#FF00FF",
    "maroon": "#800000", "mediumaquamarine": "#66CDAA", "mediumblue": "#0000CD",
    "mediumorchid": "#BA55D3", "mediumpurple": "#9370DB", "mediumseagreen": "#3CB371",
    "mediumslateblue": "#7B68EE", "mediumspringgreen": "#00FA9A",
    "mediumturquoise": "#48D1CC", "mediumvioletred": "#C71585",
    "midnightblue": "#191970", "mintcream": "#F5FFFA", "mistyrose": "#FFE4E1",
    "moccasin": "#FFE4B5", "navajowhite": "#FFDEAD", "navy": "#000080",
    "oldlace": "#FDF5E6", "olive": "#808000", "olivedrab": "#6B8E23", "orange": "#FFA500",
    "orangered": "#FF4500", "orchid": "#DA70D6", "palegoldenrod": "#EEE8AA",
    "palegreen": "#98FB98", "paleturquoise": "#AFEEEE", "palevioletred": "#DB7093",
    "papayawhip": "#FFEFD5", "peachpuff": "#FFDAB9", "peru": "#CD853F", "pink": "#FFC0CB",
    "plum": "#DDA0DD", "powderblue": "#B0E0E6", "purple": "#800080",
    "rebeccapurple": "#663399", "red": "#FF0000", "rosybrown": "#BC8F8F",
    "royalblue": "#4169E1", "saddlebrown": "#8B4513", "salmon": "#FA8072",
    "sandybrown": "#F4A460", "seagreen": "#2E8B57", "seashell": "#FFF5EE",
    "sienna": "#A0522D", "silver": "#C0C0C0", "skyblue": "#87CEEB",
    "slateblue": "#6A5ACD", "slategray": "#708090", "slategrey": "#708090",
    "snow": "#FFFAFA", "springgreen": "#00FF7F", "steelblue": "#4682B4", "tan": "#D2B48C",
    "teal": "#008080", "thistle": "#D8BFD8", "tomato": "#FF6347",
    "turquoise": "#40E0D0", "violet": "#EE82EE", "wheat": "#F5DEB3", "white": "#FFFFFF",
    "whitesmoke": "#F5F5F5", "yellow": "#FFFF00", "yellowgreen": "#9ACD32",
}

CODE_EXT = {".css", ".scss", ".less", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".mts",
            ".cts", ".tsx", ".vue", ".svelte", ".astro", ".html"}
PROSE_EXT = {".md", ".markdown", ".txt", ".html"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "vendor", ".next", "coverage",
             "__pycache__", ".venv", ".svelte-kit", "target"}
# Hex belongs in the tokens, and a third-party licence is not ours to restyle.
SKIP_NAMES = {"tokens.css", "tokens.json"}
SKIP_PATTERNS = (
    re.compile(r"^(LICENSE|LICENCE|NOTICE|COPYING)"),      # licence texts, verbatim by design
    re.compile(r"^OFL[-.]", re.I),                          # bundled font licences
    re.compile(r"\.min\.(css|js)$"),                        # nobody hand-wrote this
    re.compile(r"(^|[-.])lock(file)?\.|^package-lock\.json$"),
)
# The generated tokens carry this line. A file that INLINES them is not hand-authoring a
# colour, so its copy of the stylesheet is excluded from the hex-literal check — otherwise
# every self-contained page in a project reports every token in the palette.
TOKENS_SIGNATURE = "GRU953 — design tokens"
# A file whose SUBJECT is colour — a swatch sheet, a palette page, a contrast proof — has to
# print colour values, and flagging every one of them teaches people to ignore this output.
# Such a file says so with this marker. It suppresses the hard-coded-colour check ONLY;
# every measured-contrast and accessibility check still applies, because a swatch whose own
# label is illegible is a real defect and one has shipped before.
OPT_OUT = "gru953-review: colours-are-the-subject"
# A deliberate WRONG example — the "never do this" panel a guide needs in order to teach the
# rule — carries this marker on the element. The contrast checks skip that one block, and
# only that one.
COUNTER = "gru953-review: counter-example"

findings: list[dict] = []
CANNOT: list[str] = []


def add(sev: str, where: str, what: str, rule: str, fix: str) -> None:
    findings.append(dict(severity=sev, where=where, what=what, rule=rule, fix=fix))


# ---------------------------------------------------------------- WCAG, from scratch
def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexv: str) -> float | None:
    h = hexv.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) == 8:                      # #RRGGBBAA — ignore the alpha, flag separately
        h = h[:6]
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        return None
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float | None:
    la, lb = luminance(a), luminance(b)
    if la is None or lb is None:
        return None
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def show(r: float) -> str:
    """Two decimals, unless two decimals would round across a threshold and mislead.

    This checker gates a build, so rounding BEFORE the comparison is the worst version of
    this bug: #0B8855 on white is 4.499612:1, `round(...,2)` made it exactly 4.5, and the
    `r < 4.5` test then produced no finding at all. A pair at 2.9998 was graded `major`
    and exited 0, so it did not fail the build either.
    """
    for edge in (3.0, 4.5, 7.0):
        if r < edge <= round(r, 2):
            return f"{r:.4f}"
    return f"{r:.2f}"


# ---------------------------------------------------------------- the checks
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def strip_vendored(text: str) -> str:
    """Blank out what is not hand-authored code, keeping the line count intact.

    Two things: a <style> block that is a copy of the generated tokens, and any inlined
    <svg>. A mark's artwork legitimately carries its own colours — the app-icon tile has
    one fixed colourway baked in by design — and reporting them as hard-coded values is
    how a checker teaches people to ignore it.

    Line numbers are preserved exactly, so every finding still points at the right line.
    """
    def blank(m: re.Match) -> str:
        return "\n" * m.group(0).count("\n")

    def blank_if_tokens(m: re.Match) -> str:
        return blank(m) if TOKENS_SIGNATURE in m.group(0) else m.group(0)

    out = re.sub(r"<style\b[\s\S]*?</style>", blank_if_tokens, text, flags=re.I)
    out = re.sub(r"<svg\b[\s\S]*?</svg>", blank, out, flags=re.I)
    # <code> and <pre> quote a value rather than applying it — a table cell reading
    # "<code>#1A1753</code> as the ground" is documentation, not a hard-coded colour.
    return re.sub(r"<(code|pre)\b[\s\S]*?</\1>",
                  lambda m: re.sub(r"[^\n]", " ", m.group(0)), out, flags=re.I)


def check_code(path: pathlib.Path, text: str) -> None:
    rel = str(path)
    text = strip_vendored(text)
    lines = text.split("\n")

    # 1. a brand colour written as a literal where a role token exists
    for i, ln in enumerate(lines, 1) if OPT_OUT not in text else []:
        low = ln.lower()
        if "var(--gru-" in low:
            continue                      # already using a token on this line
        if re.search(r"<(meta|link)\b", low):
            continue    # theme-color and mask-icon need a literal; there is no token there
        # A hex written NEXT TO the token that replaces it is a lookup table, a comment or
        # a piece of documentation — the shape of every tool that maps one to the other,
        # including the brand check this plugin writes into each repository. Flagging it
        # asks the file to describe the rule without naming the value the rule is about.
        if "--gru-" in low:
            continue
        # A comment naming a colour is documentation. The generated brand-check.mjs has a
        # comment explaining WHY a #FFAB8E rule was removed, and this rule reported it —
        # so every repository this plugin scaffolds failed the plugin's own review.
        if re.match(r"\s*(//|/\*|\*|#|<!--)", ln):
            continue
        for hexv, (tok, note) in TOKEN_FOR.items():
            if hexv in low:
                add("major", f"{rel}:{i}",
                    f"the brand colour {hexv.upper()} is written as a literal",
                    "a role token is defined for it, and resolves correctly in both themes"
                    + (f" \u2014 {note}" if note else ""),
                    f"use var({tok})")

    # 2. measured contrast for anything that sets BOTH a colour and a background.
    #
    # A DECLARATION BLOCK, not a line. An earlier version matched line by line, which
    # reported every colour ramp in the design system as a failure: a whole ramp is one
    # line of markup, so "#FFAB8E appears" and "a white background appears" were both true
    # of it while no element actually paired them. Inline style attributes are scanned the
    # same way, since that is where a one-off mistake usually lives.
    blocks: list[tuple[int, str]] = []
    for m in re.finditer(r"\{([^{}]*)\}", text):
        blocks.append((text[:m.start()].count("\n") + 1, m.group(1)))
    for m in re.finditer(r"""style\s*=\s*(["'])(.*?)\1""", text, re.I | re.S):
        # Both quote styles. `style='color:#FFAB8E;background:#FFFFFF'` used to escape the
        # contrast check completely — the brand's single most common mistake, unreported.
        blocks.append((text[:m.start()].count("\n") + 1, m.group(2)))

    for line, block in blocks:
        # A block explicitly marked as a counter-example is allowed to be wrong — but only
        # the block on the marked line or the one immediately after it. The window used to
        # be lines-3 .. line+2, so one marker at the top of a file silenced three separate
        # blocks below it, including two genuine 1.83:1 blockers.
        if any(COUNTER in lines[i] for i in (line - 2, line - 1) if 0 <= i < len(lines)):
            continue
        fg = re.search(r"(?<![\w-])color\s*:\s*([^;]+)", block)
        bg = re.search(r"background(?:-color)?\s*:\s*([^;]+)", block)
        if not (fg and bg):
            continue
        f_raw, b_raw = fg.group(1).strip().lower(), bg.group(1).strip().lower()
        fm, bm = HEX_RE.search(f_raw), HEX_RE.search(b_raw)
        f_hex = fm.group(0) if fm else NAMED.get(f_raw)
        b_hex = bm.group(0) if bm else NAMED.get(b_raw)
        if not f_hex or not b_hex:
            continue
        r = contrast(f_hex, b_hex)
        if r is None:
            continue
        pair = {f_hex.upper(), b_hex.upper()}
        # the two pairings the brand refuses outright get their own message, because the
        # reason matters more than the ratio
        if pair == {"#FFAB8E", "#FFFFFF"}:
            add("blocker", f"{rel}:{line}",
                f"Daybreak #FFAB8E on a light ground measures {show(r)}:1",
                "the signature has two values precisely because one cannot serve both "
                "grounds (colour.md, approved pairings)",
                "use #B45A39 on light — or better, var(--gru-accent), which resolves to it")
        elif pair == {"#B45A39", "#1A1753"}:
            add("major", f"{rel}:{line}",
                f"Daybreak #B45A39 on Meridian measures {show(r)}:1",
                "the pale value exists for that ground",
                "use #FFAB8E on Meridian — or better, var(--gru-accent)")
        elif r < 3.0:
            add("blocker", f"{rel}:{line}",
                f"{f_hex.upper()} on {b_hex.upper()} measures {show(r)}:1",
                "WCAG 2.2 AA needs 4.5:1 for text and 3:1 for large text and UI parts",
                "use var(--gru-ink) on var(--gru-bg), or the matching -on- token")
        elif r < 4.5:
            add("major", f"{rel}:{line}",
                f"{f_hex.upper()} on {b_hex.upper()} measures {show(r)}:1",
                "WCAG 2.2 AA needs 4.5:1 for normal text; this clears only the 3:1 "
                "threshold for large text and UI parts",
                "large text (24px, or 19px bold) and icons only — never body text")

    # 4. the mark below its floor
    # `(\d+)` alone grabbed the integer part of ANY unit, so `width:1.5rem` — 24px, and
    # correct — was reported as "the bare bird is rendered at 1px" and failed CI.
    for m in re.finditer(r"GRU953-bird\.svg[\s\S]{0,240}?(?:width|height)\s*[:=]\s*"
                         r"[\"']?(\d+(?:\.\d+)?)\s*(px|rem|em|%|vw|vh|pt)?",
                         text, re.I):
        if m.group(2) and m.group(2).lower() != "px":
            continue
        px = float(m.group(1))
        if px < 24:
            line = text[:m.start()].count("\n") + 1
            add("blocker", f"{rel}:{line}",
                f"the bare bird is rendered at {px:g}px",
                "below 24px the wing's counters close; the floor is checked mechanically "
                "when the mark is generated (logo.md)",
                "use GRU953-appicon.svg, the tile, below 24px")

    # 5. the mark coloured with fill: instead of color:
    if "GRU953-" in text and re.search(r"fill\s*:\s*(#|var\(--gru)", text):
        line = text[:re.search(r"fill\s*:\s*(#|var\(--gru)", text).start()].count("\n") + 1
        add("minor", f"{rel}:{line}",
            "a GRU953 mark is being coloured with `fill:`",
            "the marks are drawn with fill=\"currentColor\", so a parent `fill` is "
            "overridden by the path's own and the bird renders black",
            "set `color:` on the wrapper instead")

    # 6. the mark animated
    if re.search(r"GRU953-bird[\s\S]{0,300}?(animation|@keyframes|transition\s*:[^;]*transform)",
                 text, re.I):
        add("major", rel, "the mark appears to be animated",
            "the mark does not move — it can be caught mid-movement looking broken",
            "remove the animation from the bird; everything else may animate")


def visible_text(html: str) -> str:
    """Only what a reader sees, with the line numbers preserved.

    The prose checks are about writing. Run them over raw HTML and they fire on CSS
    property names (`accent-color`, `forced-color-adjust`) and on attribute values, which
    is how a style guide gets ignored: a checker that cries wolf 200 times teaches people
    to skip its output.
    """
    def blank(m: re.Match) -> str:
        return "\n" * m.group(0).count("\n")
    # <pre> goes too: it holds a transcript, a code sample or a verbatim quotation — and a
    # licence text quoted verbatim must keep its American spelling, which is exactly the
    # false positive this removes.
    out = re.sub(r"<(style|script|svg|pre|code)\b[\s\S]*?</\1>", blank, html, flags=re.I)
    # A cell boundary becomes a pipe, so the "avoid | say instead" guard that works on a
    # markdown table works on a rendered one too. Without this, every row of a guide's own
    # words-to-avoid table is reported as the guide using those words.
    out = re.sub(r"</(td|th)>", " | ", out, flags=re.I)
    # Every other tag becomes ONE space, and runs collapse. Padding tags out to their own
    # width kept the columns aligned but manufactured "double space" gaps out of nothing.
    out = re.sub(r"<[^>]+>", " ", out)
    return re.sub(r"[ \t]{2,}", " ", out)


def check_prose(path: pathlib.Path, text: str) -> None:
    rel = str(path)
    if path.suffix.lower() == ".html":
        text = visible_text(text)
    # \bnot\b, not `not\b`: the latter matches the tail of "cannot", so
    # "The Gru953 API cannot fail." exempted itself from the name-spelling rule.
    NEG = re.compile(r"never|\bnot\b|wrong|avoid|incorrect|don.t|instead|rather than", re.I)

    # Inside a fenced code block, aligned columns and doubled spaces are deliberate — a
    # directory tree, a table, a terminal transcript. Prose rules do not apply there.
    fenced = False
    prose = text.split("\n")
    # YAML frontmatter is metadata with its own conventions — `license:` is the field name
    # every skill uses, and correcting it to `licence:` would break the field.
    # ...but a thematic break is also `---`. Requiring the closing marker within the first
    # twenty lines AND every enclosed line to look like `key: value` keeps a document that
    # opens with a horizontal rule from having its first section silently unchecked.
    start = 1
    if prose and prose[0].strip() == "---":
        for j, ln in enumerate(prose[1:21], 2):
            if ln.strip() == "---":
                body = [x for x in prose[1:j - 1] if x.strip()]
                if body and all(re.match(r"^\s*[\w.-]+\s*:|^\s+\S", x) for x in body):
                    start = j + 1
                break
    for i, ln in enumerate(prose, 1):
        if i < start:
            continue
        if ln.lstrip().startswith("```") or ln.lstrip().startswith("~~~"):
            fenced = not fenced
            continue
        if fenced or ln.startswith("    ") or ln.startswith("\t"):
            continue
        # Anything in backticks is code or a quoted example, not prose. Blanked once here
        # and used by every rule below, so no rule can forget it.
        bare = re.sub(r"`[^`]*`", "\u2423", ln)
        # A line carrying BOTH a wrong spelling and the correct GRU953 is a "wrong -> right"
        # example, which is how a style guide teaches the rule.
        # `Gru953` in backticks is a checker naming what it rejects, not prose getting the
        # name wrong. So is a line that also carries the correct spelling.
        # Look for the correct spelling in the ORIGINAL line, not the backtick-stripped one:
        # a "wrong -> right" row usually puts the right answer in code formatting.
        # And prose wraps, so a "never write" warning may be a line or two above.
        near_prose = " ".join(prose[max(0, i - 3):i + 1])
        in_cell = ln.count("|") >= 2 or ln.rstrip().endswith("|")
        if re.search(r"\b(Gru953|GRU 953|gru-953|GRU_953)\b", bare) \
                and not NEG.search(near_prose) and not in_cell \
                and "GRU953" not in re.sub(r"\b(Gru953|GRU 953|gru-953|GRU_953)\b", "", ln):
            add("major", f"{rel}:{i}", f"the name is written {ln.strip()[:48]!r}",
                "GRU953 is one word, uppercase, no hyphen and no space",
                "write GRU953; lowercase gru953 is for paths and packages only")
        # Case-SENSITIVE, deliberately. "US dollar" and "a US employer" are not the brand
        # calling itself a team, and matching them case-insensitively reported both.
        # "us both", "neither of us", "let us know" — that is READER AND AUTHOR, which is
        # the opposite of the failure this rule exists to catch. The rule is about a
        # one-person studio calling itself a team; "a screenshot usually saves us both a
        # day" is ordinary, correct English and was being reported as a brand violation.
        READER_AND_AUTHOR = re.compile(
            r"\b(?:us|we)\s+both\b|\b(?:both|neither|either|each|any|all|one)\s+of\s+us\b"
            r"|\blet\s+us\b|\bbetween\s+us\b", re.I)
        bare_pron = READER_AND_AUTHOR.sub("\u2423", bare)
        pron = re.search(r"\b(we|We|our|Our|us)\b", bare_pron)
        # Anywhere inside a matched pair of quotes, backticks or emphasis — not only
        # tightly wrapped. `"we're excited to"` is a mention, exactly as the hype rule
        # below already understood, and this rule used to report it as a use.
        PQ = r"""["\u201c\u201d\u2018\u2019`*_]"""
        quoted_pron = pron and re.search(
            PQ + r"[^\n]{0,40}\b" + pron.group(1) + r"\b"
            + r"|\b" + pron.group(1) + r"\b[^\n]{0,40}" + PQ, ln)
        # A two-column "avoid | say instead" row is a lesson, not a lapse.
        if pron and not NEG.search(ln) and not quoted_pron \
                and not (ln.count("|") >= 2 or ln.rstrip().endswith("|")):
            add("minor", f"{rel}:{i}", "\"we\" or \"our\" used",
                "GRU953 has one person behind it; the brand never pretends to be a team",
                "write \"I\", or name GRU953 directly")
        # A guide has to NAME the words it forbids. Quoted or backticked, it is a mention;
        # in a two-column "avoid | say instead" row, it is a lesson.
        hype = re.search(r"\b(excited|thrilled|delighted|revolutionary|game.chang|cutting.edge|"
                         r"seamless|effortless|unleash|supercharge)\b", ln, re.I)
        # A quote mark on either side counts — prose wraps, so the opening quote may be on
        # the line above and only the closing one is here.
        # Quote marks, backticks and markdown emphasis all mean "I am naming this word,
        # not using it". A cell in a two-column table means the same thing.
        Q = r"""["\u201c\u201d\u2018\u2019`*_]"""
        quoted_hype = hype and re.search(
            Q + r"[^\n]{0,40}" + re.escape(hype.group(1))
            + r"|" + re.escape(hype.group(1)) + r"[^\n]{0,40}" + Q, ln, re.I)
        in_cell = ln.count("|") >= 2 or ln.rstrip().endswith("|")
        if hype and not NEG.search(ln) and not quoted_hype and not in_cell:
            add("major", f"{rel}:{i}", f"hype: {ln.strip()[:56]!r}",
                "no hype, and no exclamation mark manufacturing enthusiasm (voice.md)",
                "say what changed and give its number")
        # Run on `bare`, which already has backtick spans blanked, rather than on `ln`:
        # a single backtick anywhere used to switch the whole line off, so
        # "The `theme` uses American color and behavior spellings" produced nothing.
        #
        # The excluded spellings are the ones that are NOT ours to change:
        #   · CSS property and media-feature names — `color:`, `prefers-color-scheme`,
        #     `accent-color`, `forced-color-adjust`, `color-scheme`. Correcting
        #     `prefers-color-scheme` to `prefers-colour-scheme` breaks dark mode, and this
        #     rule used to fire on the README template every repository is built from.
        #   · `LICENSE` as a filename, `license:` as a frontmatter field, and SPDX ids.
        SPELL = re.compile(r"\b(color|behavior|organize|analyze|customize|license)\b", re.I)
        m_sp = SPELL.search(bare)
        exempt = re.compile(
            r"(?:prefers-|accent-|forced-|caret-|outline-|border-|background-|text-decoration-)"
            r"color|color(?:-scheme|-adjust|:)|--gru|\bCSS\b|\bLICENSE\b|license:"
            r"|SPDX|LicenseRef", re.I)
        # A markdown blockquote is a verbatim quotation — the same reasoning already
        # applied to <pre>/<code> in strip_html() above: a source quoted for its own
        # words must keep that source's own spelling. Rewriting an American source's
        # "color" to "colour" inside a quotation mark would be misquoting it, not
        # correcting it. First hit: this file's own research quotes from Material
        # Design, USWDS and Primer, all American-sourced and all genuinely verbatim.
        in_blockquote = ln.lstrip().startswith(">")
        if m_sp and not exempt.search(ln) and not in_blockquote:
            add("minor", f"{rel}:{i}", f"American spelling: {m_sp.group(1)!r}",
                "the house style is UK English",
                "colour, behaviour, organise, analyse, customise, licence (the noun)")
        # An UNBRACKETED gap, which reads as finished copy with a typo.
        #
        # Not in a .txt: a plain-text file is almost always a report or a transcript, where
        # aligned columns are the format rather than a hole in a sentence.
        if path.suffix.lower() == ".txt":
            pass
        elif re.search(r"(?<=[a-z,])  +(?=[a-z])", bare) or re.search(r'(?<!")""(?!")', bare) \
                or "****" in bare or re.search(r"[।.]\s+:", bare):
            add("major", f"{rel}:{i}", f"a gap in the text: {ln.strip()[:56]!r}",
                "an unbracketed gap reads as finished copy, so nobody fixes it",
                "restore the missing words, or mark the gap [like this]")

    # the taglines, complete or not at all
    # EVERY occurrence, not merely one. A presence test passes a file that carries the
    # tagline correctly once and mangles it three paragraphs later, which is exactly how a
    # locked string comes unlocked.
    for stem, whole, lang in (("Simple technology", TAG_EN, "English"),
                              ("\u09b8\u09b9\u099c \u09aa\u09cd\u09b0\u09af\u09c1\u0995\u09cd\u09a4\u09bf", TAG_BN, "Bangla")):
        for m in re.finditer(re.escape(stem), text):
            if text.startswith(whole, m.start()):
                continue
            line = text[:m.start()].count("\n") + 1
            ln = text.split("\n")[line - 1]
            # A document has to be able to NAME the shortened form in order to forbid it.
            # Quoted, backticked, or on a line that says never/do not/avoid, it is a
            # mention — the same guard the hype and pronoun rules already use.
            q = re.search(r"""["\u201c\u201d\u2018\u2019`*]\s*""" + re.escape(stem), ln)
            if q or re.search(r"never|\bnot\b|do not|don.t|avoid|shorten|wrong|instead"
                              r"|rewording|incorrect", ln, re.I):
                continue
            if True:
                add("blocker", f"{rel}:{line}",
                    f"the {lang} tagline is shortened or altered: "
                    f"{text[m.start():m.start() + len(whole) + 6].strip()!r}",
                    "the taglines are locked and used complete, in both languages",
                    f'write exactly "{whole}"')

    # the licence claim
    prose_lines = text.split("\n")
    for i, ln in enumerate(prose_lines, 1):
        # Only an unqualified claim counts. A line that says Apache-2.0 IS an OSI-approved
        # open source licence is true; a line that says PolyForm is not one is teaching the
        # rule. Both were reported as violations before this guard, in the very documents
        # that exist to state the distinction correctly.
        OK_CONTEXT = re.compile(
            r"not\s+open[- ]source|source-available|rather than open|never\b"
            r"|Apache|OSI|Open Source Definition|Open Source Initiative|OFL|SIL", re.I)
        # A QUOTED "open source" is a mention, not a claim — the documents that exist to
        # state this distinction quote the wrong phrase in order to forbid it. And prose
        # wraps, so the negation may sit on the line above or below.
        #
        # Bracketed by quote marks, not just preceded by one: the original regex only
        # matched "open source" sitting immediately after an opening quote, which missed
        # the far more common case of a longer quoted sentence with the phrase in the
        # middle -- e.g. a research quote reading `*"Material Design 3 is Google's
        # open-source design system..."*`. That is still a quotation, not GRU953 making
        # a claim about its own PolyForm-licensed work, and it was reported as a blocker
        # the first time this file quoted a real source describing itself as open source.
        _phrase = re.search(r"open[- ]source", ln, re.I)
        quoted = False
        if _phrase:
            _before, _after = ln[:_phrase.start()], ln[_phrase.end():]
            if re.search(r"[\"\u201c\u2018]", _before) and re.search(r"[\"\u201d\u2019]", _after):
                quoted = True
        near = " ".join(prose_lines[max(0, i - 2):i + 1])
        # A CLAIM needs a verb. "### Open source" is a heading about the concept and
        # "| Open source | ওপেন সোর্স |" is a glossary row; neither says this work is open
        # source. Requiring a linking verb or the word licence next to the phrase is what
        # separates a claim from a mention.
        claim = re.search(r"\b(is|are|as|under|released|licensed|licen[cs]e[ds]?)\b"
                          r"[^.\n]{0,40}open[- ]source"
                          r"|open[- ]source[^.\n]{0,25}\b(licen[cs]e|under)\b", ln, re.I)
        # PolyForm anywhere in what is being reviewed, not only in this one file. The
        # .mjs check written into every scaffolded repository already keyed off the
        # presence of LICENSE-GUIDEBOOK.md; this one required the word in the same file,
        # so a README claiming "open source" beside a PolyForm LICENSE-GUIDEBOOK.md passed
        # here and failed there. Two implementations of one rule, disagreeing.
        #
        # TREE["polyform"] is tree-wide: it goes true the moment ANY file anywhere in
        # what is being reviewed mentions PolyForm, which in this repository is nearly
        # always. Without a self-reference requirement that turns this into "any 'X is
        # open source' sentence in any file, anywhere, blocks the build" — and a
        # benchmark document doing exactly its job, accurately describing GOV.UK's
        # MIT-licensed design system or Ant Design's own open-source status, is not a
        # claim about GRU953's own PolyForm-licensed writing. First hit: this file
        # itself, describing "the open-source Ant Design project" — true, and nothing
        # to do with GRU953's licence.
        SELF_REF = re.compile(r"\bGRU953\b|\bthis (?:kit|guidebook|book|document|system"
                               r"|repository|writing)\b|\bour (?:writing|guidebook|book)\b",
                               re.I)
        if claim and (re.search(r"PolyForm", text, re.I) or TREE["polyform"]) \
                and SELF_REF.search(near) \
                and not OK_CONTEXT.search(near) and not quoted:
            add("blocker", f"{rel}:{i}",
                "PolyForm-licensed content described as open source",
                "the Open Source Definition forbids restricting a field of use, so "
                "PolyForm Noncommercial is not and will not be OSI-approved",
                "call it source-available")


def check_html(path: pathlib.Path, text: str) -> None:
    """Accessibility basics that can be found without a browser. Structural only —
    anything needing layout or computed style is out of reach here, and said so."""
    rel = str(path)
    if re.search(r"<html\b", text, re.I) and not re.search(r"<html[^>]*\blang=", text, re.I):
        add("major", rel, "<html> has no lang attribute",
            "WCAG 2.2 3.1.1 — a screen reader cannot choose a voice without it",
            'add lang="en" (and lang="bn" on the Bangla passages)')
    for m in re.finditer(r"<img\b(?![^>]*\balt=)[^>]*>", text, re.I):
        add("major", f"{rel}:{text[:m.start()].count(chr(10)) + 1}",
            "an <img> has no alt attribute",
            "WCAG 2.2 1.1.1 — and alt says what the image MEANS, not what it is",
            'add alt="…", or alt="" if it is purely decorative')
    for m in re.finditer(r"<svg\b(?![^>]*aria-hidden)(?![^>]*aria-label)[^>]*>(?![\s\S]{0,200}?<title)",
                         text, re.I):
        add("minor", f"{rel}:{text[:m.start()].count(chr(10)) + 1}",
            "an <svg> has neither a <title>, an aria-label, nor aria-hidden",
            "WCAG 2.2 1.1.1 — it is announced as an unlabelled graphic",
            "add a <title>, or aria-hidden=\"true\" if it is decorative")
    for m in re.finditer(r'aria-labelledby="([^"]+)"', text):
        for ref in m.group(1).split():
            # Both quote styles. Matching only `id="x"` reported valid HTML that used
            # single quotes as a broken ARIA reference, and failed CI on it.
            if not re.search(rf"""\bid\s*=\s*(["']){re.escape(ref)}\1""", text):
                add("blocker", rel,
                    f'aria-labelledby points at id="{ref}", which is not in the document',
                    "the accessible name resolves to nothing, which is worse than no "
                    "label — the source still looks correct",
                    "fix the id, or stop an SVG optimiser renaming it (cleanupIds)")
    if re.search(r"outline\s*:\s*(none|0)\b", text, re.I) and \
            not re.search(r":focus-visible[^{]*\{[^}]*outline\s*:\s*(?!none|0)", text, re.I):
        add("blocker", rel, "outline removed with no :focus-visible replacement",
            "WCAG 2.2 2.4.7 — a keyboard user loses their place entirely",
            "give :focus-visible an outline of 3px solid var(--gru-focus)")
    if re.search(r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1", text, re.I):
        add("major", rel, "the viewport blocks zooming",
            "WCAG 2.2 1.4.4 — text must scale to 200%",
            "remove user-scalable=no and maximum-scale")


# ---------------------------------------------------------------- walking
unreadable: list[str] = []
# Facts about the whole tree under review, not about one file. Set once in main().
TREE = {"polyform": False}


def walk(target: pathlib.Path) -> list[pathlib.Path]:
    """Every checkable file under `target`, and a record of anything that could not be read.

    Two defects lived here.

    SKIP_DIRS was tested against the ABSOLUTE path, so a project living anywhere under a
    directory called `build`, `dist`, `target`, `vendor` or `coverage` was skipped
    entirely and reported as clean — with exit code 0. The test is now relative to what
    was asked for: a `dist/` inside the project is still skipped, the project's own
    ancestry is not.

    And an unreadable subtree was swallowed in silence, so "no findings" could not be
    told apart from "could not look". Anything unreadable is now a finding of its own.
    """
    if target.is_file():
        return [target] if target.suffix.lower() in CODE_EXT | PROSE_EXT else []
    out = []
    stack = [target]
    while stack:
        d = stack.pop()
        try:
            entries = sorted(d.iterdir())
        except OSError as e:
            unreadable.append(f"{d}: {e.strerror or e}")
            continue
        for p in entries:
            try:
                rel_parts = p.relative_to(target).parts
            except ValueError:                      # a symlink out of the tree
                continue
            if any(part in SKIP_DIRS for part in rel_parts):
                continue
            if p.is_symlink():
                continue                            # never follow one; a loop is fatal
            if p.is_dir():
                stack.append(p)
            elif p.is_file() and p.suffix.lower() in CODE_EXT | PROSE_EXT:
                out.append(p)
    return sorted(out)


def skipped(p: pathlib.Path, extra: list[str]) -> bool:
    if p.name in SKIP_NAMES or any(r.search(p.name) for r in SKIP_PATTERNS):
        return True
    return any(pat in str(p) for pat in extra)


def main() -> None:
    ap = argparse.ArgumentParser(description="The mechanical half of a GRU953 review.")
    # nargs="?" so a bare invocation works. The command that wraps this documents a default
    # of "the current directory", and argparse was making that documentation a lie.
    ap.add_argument("target", nargs="?", default=".", help="a file or a directory (default: .)")
    ap.add_argument("--html", action="store_true", help="also parse HTML for accessibility")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--quiet", action="store_true",
                    help="findings only, with no header, summary or blind-spot list")
    ap.add_argument("--skip", action="append", default=[], metavar="TEXT",
                    help="skip any path containing TEXT (repeatable)")
    a = ap.parse_args()
    if a.json and a.quiet:
        ap.error("--json and --quiet ask for two different things; pick one")

    target = pathlib.Path(a.target).resolve()
    if not target.exists():
        sys.exit(f"FAIL — {target} does not exist.")
    # The skip list is applied HERE, so `files` is what was actually examined.
    # Applied inside the loop instead, a directory holding nothing but skipped files
    # printed "No mechanical findings." and exited 0 — a clean bill of health for a
    # run that read nothing at all.
    files = [f for f in walk(target) if not skipped(f, a.skip)]
    # Does anything in this tree ship PolyForm-licensed content? A licence claim in a
    # README is about the repository, not about the README.
    if target.is_dir():
        for name in ("LICENSE-GUIDEBOOK.md", "LICENCE-GUIDEBOOK.md"):
            if (target / name).exists():
                TREE["polyform"] = True
        if not TREE["polyform"]:
            for f in files:
                try:
                    if "polyform" in f.read_text(encoding="utf-8", errors="replace").lower():
                        TREE["polyform"] = True
                        break
                except OSError:
                    pass
    for u in unreadable:
        add("blocker", u, "this path could not be read, so nothing in it was checked",
            "a review that cannot see a file must say so; silence reads as a pass",
            "fix the permissions, or pass --skip to exclude it deliberately")
    # A file whose extension is not checkable, or a directory with nothing checkable in
    # it, used to print "No mechanical findings." and exit 0 — a clean bill of health for
    # a run that examined nothing.
    if not files:
        sys.exit(f"FAIL — nothing under {target} was checkable, so nothing is proved.\n"
                 f"       It reads: {', '.join(sorted(CODE_EXT | PROSE_EXT))}\n"
                 f"       (generated token files and third-party licence texts are\n"
                 f"       skipped by design — name a file directly to force one)")

    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            add("blocker", str(p), f"could not be read: {e.strerror or e}",
                "a review that cannot see a file must say so",
                "fix the permissions, or pass --skip to exclude it deliberately")
            continue
        rel = p.relative_to(target) if target.is_dir() else p.name
        if p.suffix.lower() in CODE_EXT:
            check_code(pathlib.Path(str(rel)), text)
        if p.suffix.lower() in PROSE_EXT:
            check_prose(pathlib.Path(str(rel)), text)
        if a.html and p.suffix.lower() == ".html":
            check_html(pathlib.Path(str(rel)), text)

    CANNOT.extend([
        "A colour inside a stylesheet copied into a page (the generated tokens) is not "
        "counted as a hard-coded value \u2014 only hand-authored code is.",
        "Third-party licence texts, lockfiles and minified files are skipped entirely.",
        "Colours inside an inlined <svg> \u2014 a mark's own artwork \u2014 are not counted "
        "as hard-coded values.",
        "Whether the Bangla reads naturally to a native speaker. Nothing here judges that.",
        "Whether it works with a real screen reader, used by a real person.",
        "Whether a colour feels right. Contrast is measured; taste is not.",
        "Any claim about the world — a figure, a date, a licence fact — is not verified here.",
        "Contrast that depends on a computed style, an image behind text, or an opacity. "
        "Only literal foreground/background pairs in the same rule are measured.",
        "A block marked `gru953-review: counter-example` is skipped by the contrast checks "
        "\u2014 that is how a guide shows a wrong example on purpose.",
        "Whether the design is any good. This is a floor, not a ceiling.",
    ])

    order = {"blocker": 0, "major": 1, "minor": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["where"]))

    if a.json:
        print(json.dumps(dict(target=str(target), files=len(files),
                              findings=findings, not_checked=CANNOT), indent=2,
                         ensure_ascii=False))
        sys.exit(1 if any(f["severity"] == "blocker" for f in findings) else 0)

    if not a.quiet:
        print(f"GRU953 review — {len(files)} files under {target}\n")
    if not findings and not a.quiet:
        print("No mechanical findings.\n")
    for f in findings:
        print(f"{f['severity'].upper():8s} {f['where']}")
        print(f"         {f['what']}")
        print(f"         rule: {f['rule']}")
        print(f"         fix:  {f['fix']}\n")
    counts = {s: sum(1 for f in findings if f["severity"] == s)
              for s in ("blocker", "major", "minor")}
    if not a.quiet:
        print(f"{counts['blocker']} blocker, {counts['major']} major, {counts['minor']} minor\n")
        print("NOT CHECKED HERE — stated rather than silently passed:")
        for c in CANNOT:
            print(f"  · {c}")
    # Exit 1 on a blocker so this can gate a build. Majors and minors do not fail
    # the run: a checker that blocks on a style note gets removed from CI.
    sys.exit(1 if counts["blocker"] else 0)


if __name__ == "__main__":
    main()
