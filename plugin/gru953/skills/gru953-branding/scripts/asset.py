#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""GRU953 — emit a brand asset, correctly.

Everything this produces is derived from the files in ../assets/, so nothing it
writes can drift from the brand kit. It also refuses to produce a combination the
brand does not permit — a mark below its size floor, or a colour on a ground it
is not approved against — because the whole point of a rule is that it is easier
to follow than to break.

Only the standard library is needed for SVG, tokens and contrast. PNG output
additionally needs `rsvg-convert` (tried first), or `cairosvg`, or Inkscape.

    python3 asset.py list
    python3 asset.py svg lockup-horizontal meridian -o header.svg
    python3 asset.py svg bird daybreak-dark --on meridian -o mark.svg
    python3 asset.py png bird meridian --width 512 -o mark.png
    python3 asset.py favicons -o ./public
    python3 asset.py tokens --format css -o tokens.css
    python3 asset.py check "#FFAB8E" "#FFFFFF"
    python3 asset.py check --role accent --theme light
"""
from __future__ import annotations
import argparse, json, os, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
MARKS = ASSETS / "marks"

# ---------------------------------------------------------------- the rules, as data
COLOURS = {
    "meridian":      "#1A1753",
    "daybreak-light": "#B45A39",
    "daybreak-dark":  "#FFAB8E",
    "ink":           "#0B0E14",
    "paper":         "#FFFFFF",
}
GROUNDS = {"paper": "#FFFFFF", "meridian": "#1A1753", "ink": "#0B0E14"}

# ground -> the mark colours approved on it. Anything absent is refused.
APPROVED = {
    "paper":    {"meridian", "daybreak-light", "ink"},
    "meridian": {"daybreak-dark", "paper"},
    "ink":      {"daybreak-dark", "paper"},
}
# the two people reach for by mistake, with the reason and the fix
# The RATIO IS NOT TYPED HERE. It is computed at the point of use, from the same two
# colours the refusal is about. A hand-typed figure went wrong exactly as you would expect:
# "daybreak-light on ink: 2.19:1" was published and printed on every refusal, and the real
# measurement is 4.10:1. Only the words are written down.
REFUSED = {
    ("paper", "daybreak-dark"): ("the bird all but disappears",
                                 "use daybreak-light (#B45A39) on a light ground"),
    ("meridian", "daybreak-light"): ("legible but muddy, and it fights the ground",
                                     "use daybreak-dark (#FFAB8E) on Meridian"),
    ("ink", "daybreak-light"): ("too dark to read as first light on a dark ground",
                                "use daybreak-dark (#FFAB8E) on Ink"),
}

# name -> (file, minimum width in px, note)
MARK_SET = {
    "bird":                     ("GRU953-bird.svg", 24, "the mark alone"),
    "tile":                     ("GRU953-appicon.svg", 16, "the bird on a Meridian tile; one fixed colourway"),
    "lockup-horizontal":        ("GRU953-lockup-horizontal.svg", 120, "the default for headers and banners"),
    "lockup-horizontal-tagline": ("GRU953-lockup-horizontal-tagline.svg", 260, "with both taglines"),
    "lockup-stacked":           ("GRU953-lockup-stacked.svg", 120, "square and narrow spaces"),
    "lockup-stacked-tagline":   ("GRU953-lockup-stacked-tagline.svg", 260, "posters, covers, title cards"),
    "wordmark":                 ("GRU953-wordmark.svg", 90, "when the bird would be too small"),
    "tagline":                  ("GRU953-tagline.svg", 200, "both languages, as artwork"),
}


def die(msg: str, fix: str = "") -> None:
    print(f"REFUSED — {msg}", file=sys.stderr)
    if fix:
        print(f"          {fix}", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------- WCAG, from scratch
def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    """WCAG 2.2 relative luminance. No dependency; the formula is four lines."""
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        die(f"{hex_colour!r} is not a 6-digit hex colour")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return (0.2126 * _srgb_to_linear(r) + 0.7152 * _srgb_to_linear(g)
            + 0.0722 * _srgb_to_linear(b))


def contrast(a: str, b: str) -> float:
    """The UNROUNDED ratio. Round only to print it.

    Rounding before the comparison is a real defect, not a nicety: #0B8855 on white is
    4.499612:1, which rounds to "4.5" and was graded AA by a `>= 4.5` test on the rounded
    value. It fails. Every threshold test in this file uses the raw number and every
    printed figure is formatted at the print site.
    """
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def show(ratio: float) -> str:
    """Two decimals, unless two decimals would round across a threshold and mislead.

    #0B8855 on white is 4.499612:1 — it FAILS AA for body text, and printing "4.50:1"
    beside the word FAIL reads like a bug in the tool rather than a fact about the colour.
    """
    for edge in (3.0, 4.5, 7.0):
        if ratio < edge <= round(ratio, 2):
            return f"{ratio:.4f}"
    return f"{ratio:.2f}"


def grade(ratio: float, large: bool = False) -> str:
    aaa, aa = (4.5, 3.0) if large else (7.0, 4.5)
    return "AAA" if ratio >= aaa else ("AA" if ratio >= aa else "FAIL")


# ---------------------------------------------------------------- the commands
def cmd_list(_a) -> None:
    print("MARKS")
    for name, (f, floor, note) in MARK_SET.items():
        ok = "present" if (MARKS / f).exists() else "MISSING"
        print(f"  {name:26s} min {floor:>4}px   {note}   [{ok}]")
    print("\nCOLOURS")
    for name, hexv in COLOURS.items():
        print(f"  {name:26s} {hexv}")
    print("\nGROUNDS AND WHAT IS APPROVED ON THEM")
    for ground, allowed in APPROVED.items():
        print(f"  on {ground:10s} {', '.join(sorted(allowed))}")
    print("\nREFUSED PAIRINGS")
    for (g, c), (why, fix) in REFUSED.items():
        r = show(contrast(COLOURS[c], GROUNDS[g]))
        print(f"  {c} on {g}: {r}:1 — {why}\n      -> {fix}")


def _resolve(mark: str, colour: str, on: str | None, width: int | None):
    if mark not in MARK_SET:
        die(f"no mark called {mark!r}", f"try one of: {', '.join(MARK_SET)}")
    filename, floor, _ = MARK_SET[mark]
    src = MARKS / filename
    if not src.exists():
        die(f"{src} is missing from the skill's assets")

    if mark == "tile":
        # The tile has one colourway and is not recolourable. Saying so is kinder
        # than silently ignoring a --colour that was asked for in good faith.
        # `colour` is None when the user named no colour, which is the ONLY way to ask for
        # the tile. It used to default to "meridian" before reaching here, so
        # `asset.py svg tile` was impossible — the tile being the mark the brand mandates
        # below 24px, and the app icon.
        if colour not in (None, "tile"):
            die("the tile has one fixed colourway and cannot be recoloured",
                "for another colour use `bird`, which is drawn with currentColor")
        if width is not None and width < floor:
            die(f"the tile's floor is {floor}px; {width}px was asked for")
        return src, None, floor, colour

    if colour is None:
        colour = "meridian"
    if colour not in COLOURS:
        die(f"{colour!r} is not an approved colour",
            f"the five are: {', '.join(COLOURS)}")
    if on is not None:
        if on not in GROUNDS:
            die(f"{on!r} is not a ground", f"grounds are: {', '.join(GROUNDS)}")
        if (on, colour) in REFUSED:
            why, fix = REFUSED[(on, colour)]
            r = show(contrast(COLOURS[colour], GROUNDS[on]))
            die(f"{colour} on {on} is not approved: {r}:1 — {why}", fix)
        if colour not in APPROVED[on]:
            die(f"{colour} on {on} is not an approved pairing",
                f"on {on}, use one of: {', '.join(sorted(APPROVED[on]))}")
    if width is not None and width < floor:
        alt = "the tile (`tile`)" if mark == "bird" else "the mark alone (`bird`)"
        die(f"{mark} has a floor of {floor}px; {width}px was asked for",
            f"below the floor, use {alt}")
    return src, COLOURS[colour], floor, colour


def _svg_text(src: pathlib.Path, hexv: str | None) -> str:
    s = src.read_text(encoding="utf-8")
    return s if hexv is None else s.replace("currentColor", hexv)


def _outfile(path: str) -> pathlib.Path:
    out = pathlib.Path(path)
    if out.is_dir():
        die(f"{out} is a directory, not a file", "give -o a filename")
    return out


def _mkparent(out: pathlib.Path) -> None:
    """Create the parent directory, refusing in this file's own voice if it cannot.

    Every error path here exits 2 with a sentence a person can act on. A read-only
    directory, or a parent that is a file, used to exit 1 with a raw OSError traceback.
    """
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        die(f"could not create {out.parent}", e.strerror or str(e))


def _write(out: pathlib.Path, data, binary: bool = False) -> None:
    try:
        out.write_bytes(data) if binary else out.write_text(data, encoding="utf-8")
    except OSError as e:
        die(f"could not write {out}", e.strerror or str(e))


def cmd_svg(a) -> None:
    src, hexv, _, colour = _resolve(a.mark, a.colour, a.on, None)
    out = _outfile(a.output)
    _mkparent(out)
    _write(out, _svg_text(src, hexv))
    note = f" in {colour}" if hexv else " (its one fixed colourway)"
    print(f"{out}  <-  {a.mark}{note}, {out.stat().st_size:,} bytes")
    if hexv:
        print(f"  The colour is baked in as {hexv}. For a mark that follows its\n"
              f"  surroundings instead, copy assets/marks/ directly \u2014 those keep\n"
              f"  fill=\"currentColor\", and you set `color:` in CSS.")


def _run(cmd: list[str], tool: str) -> None:
    """Run a renderer, and refuse in this file's own voice if it fails.

    Every other error path here exits 2 with a sentence a person can act on. A renderer
    that failed used to exit 1 with a CalledProcessError traceback, which is neither.
    """
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        msg = (r.stderr or b"").decode("utf-8", "replace").strip().splitlines()
        die(f"{tool} could not render the mark",
            msg[-1] if msg else f"{tool} exited {r.returncode} and said nothing")


def _rasterise(svg_text: str, width: int, out: pathlib.Path) -> str:
    """Render to a temporary file and move it into place only on success.

    Writing straight to `out` means a renderer that opens the file and then fails has
    already destroyed the previous good PNG.
    """
    tmp_svg = out.with_suffix(".tmp.svg")
    tmp_png = out.with_suffix(".tmp.png")
    tmp_svg.write_text(svg_text, encoding="utf-8")
    try:
        engine = ""
        if shutil.which("rsvg-convert"):
            _run(["rsvg-convert", "-w", str(width), str(tmp_svg), "-o", str(tmp_png)],
                 "rsvg-convert")
            engine = "rsvg-convert"
        else:
            try:
                import cairosvg  # type: ignore
                cairosvg.svg2png(url=str(tmp_svg), write_to=str(tmp_png),
                                 output_width=width)
                engine = "cairosvg"
            except ImportError:
                if shutil.which("inkscape"):
                    _run(["inkscape", "--export-type=png", f"--export-width={width}",
                          f"--export-filename={tmp_png}", str(tmp_svg)], "inkscape")
                    engine = "inkscape"
        if not engine:
            die("no PNG renderer found",
                "install one of: rsvg-convert (librsvg), cairosvg (pip), or Inkscape.\n"
                "          Or use `svg` — the vector is better everywhere that takes it.")
        if not tmp_png.exists() or tmp_png.stat().st_size == 0:
            die(f"{engine} exited cleanly but wrote nothing")
        os.replace(tmp_png, out)
        return engine
    finally:
        tmp_svg.unlink(missing_ok=True)
        tmp_png.unlink(missing_ok=True)


def cmd_png(a) -> None:
    src, hexv, _, _colour = _resolve(a.mark, a.colour, a.on, a.width)
    out = _outfile(a.output)
    _mkparent(out)
    engine = _rasterise(_svg_text(src, hexv), a.width, out)
    print(f"{out}  <-  {a.mark} at {a.width}px via {engine}, "
          f"{out.stat().st_size:,} bytes")
    print("  the background is transparent; the ground is yours to set.")


def cmd_favicons(a) -> None:
    """The whole icon set. The favicon IS THE TILE, because a 16px tab cannot
    hold a line drawing — the same rule as everywhere else, applied honestly."""
    out = pathlib.Path(a.output)
    out.mkdir(parents=True, exist_ok=True)
    tile = (MARKS / MARK_SET["tile"][0]).read_text(encoding="utf-8")
    made = []
    for w in (16, 32, 48, 64, 128, 256):
        p = out / f"favicon-{w}.png"
        _rasterise(tile, w, p)
        made.append(p)
    _rasterise(tile, 180, out / "apple-touch-icon.png")
    made.append(out / "apple-touch-icon.png")
    (out / "icon.svg").write_text(tile, encoding="utf-8")
    made.append(out / "icon.svg")
    # Safari's pinned tab wants a single-colour silhouette on a transparent ground
    (out / "mask-icon.svg").write_text(
        (MARKS / "GRU953-bird.svg").read_text(encoding="utf-8")
        .replace("currentColor", "#000000"), encoding="utf-8")
    made.append(out / "mask-icon.svg")
    try:
        from PIL import Image  # type: ignore
        ims = [Image.open(out / f"favicon-{w}.png").convert("RGBA")
               for w in (16, 32, 48, 64)]
        ims[0].save(out / "favicon.ico", format="ICO",
                    sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
                    append_images=ims[1:])
        made.append(out / "favicon.ico")
    except ImportError:
        print("  ! Pillow is not installed, so favicon.ico was not built.\n"
              "    The PNGs and icon.svg cover every current browser; .ico is for old ones.")
    for p in made:
        print(f"{p}  {p.stat().st_size:,} bytes")
    print("""
Put these five tags in the page <head>:

  <link rel="icon" href="favicon.ico" sizes="32x32">
  <link rel="icon" href="icon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="mask-icon" href="mask-icon.svg" color="#1A1753">
  <meta name="theme-color" content="#1A1753">

Using a framework? Put the files wherever it serves untouched — usually
public/ or static/ — and the same tags in whatever controls the <head>.""")


def cmd_tokens(a) -> None:
    src = ASSETS / ("tokens.css" if a.format == "css" else "tokens.json")
    if not src.exists():
        die(f"{src} is missing from the skill's assets")
    out = _outfile(a.output)
    _mkparent(out)
    shutil.copyfile(src, out)
    print(f"{out}  <-  {src.name}, {out.stat().st_size:,} bytes")
    if a.format == "css":
        print("  Use the ROLE tokens (--gru-bg, --gru-ink, --gru-accent, …).\n"
              "  They are defined in both themes, so one stylesheet covers light and dark.")


def cmd_check(a) -> None:
    if a.role and (a.foreground or a.background):
        die("--role and a pair of colours are two different questions",
            "ask one: `check \"#FFAB8E\" \"#FFFFFF\"` or `check --role accent`")
    if a.role:
        if not (ASSETS / "tokens.json").exists():
            die(f"{ASSETS / 'tokens.json'} is missing from the skill's assets",
                "give two colours instead, or reinstall the skill")
        tok = json.loads((ASSETS / "tokens.json").read_text(encoding="utf-8"))
        roles = tok["roles"][a.theme]
        if a.role not in roles:
            die(f"no role called --gru-{a.role}",
                f"try: {', '.join(sorted(roles)[:12])} …")
        if a.against not in roles:
            die(f"no role called --gru-{a.against}",
                f"try: {', '.join(sorted(roles)[:12])} …")
        fg, bg = roles[a.role], roles[a.against]
        label = f"--gru-{a.role} on --gru-{a.against} ({a.theme} theme)"
    else:
        if not (a.foreground and a.background):
            die("give two colours, or use --role NAME --theme light|dark")
        fg, bg = a.foreground, a.background
        label = f"{fg} on {bg}"
    r = contrast(fg, bg)
    print(f"{label}\n  {fg}  on  {bg}")
    print(f"  contrast          {show(r)}:1")
    print(f"  normal text       {grade(r)}      (AA needs 4.5, AAA needs 7)")
    print(f"  large text / UI   {grade(r, True)}      (AA needs 3.0, AAA needs 4.5)")
    if r < 3.0:
        print("\n  This pairing carries nothing legibly. Do not ship it.")
    elif r < 4.5:
        print("\n  Large text, icons and borders only. Not body text.")
    sys.exit(0 if r >= 3.0 else 1)


# ---------------------------------------------------------------- wiring
def main() -> None:
    p = argparse.ArgumentParser(
        prog="asset.py", description="Emit a GRU953 brand asset, correctly.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="every mark, colour and approved pairing").set_defaults(fn=cmd_list)

    for name, fn, needs_width in (("svg", cmd_svg, False), ("png", cmd_png, True)):
        s = sub.add_parser(name, help=f"write one mark as {name.upper()}")
        s.add_argument("mark", help="bird | tile | lockup-horizontal | … (see `list`)")
        # No default. `tile` takes no colour at all, and a default of "meridian" made
        # the tile impossible to produce by any documented invocation.
        s.add_argument("colour", nargs="?", default=None,
                       help="meridian | daybreak-light | daybreak-dark | ink | paper "
                            "(omit for `tile`, which has one fixed colourway; "
                            "defaults to meridian for every other mark)")
        s.add_argument("--on", help="the ground it will sit on; checked against the rules")
        if needs_width:
            s.add_argument("--width", type=int, required=True, help="pixels")
        s.add_argument("-o", "--output", required=True)
        s.set_defaults(fn=fn)

    s = sub.add_parser("favicons", help="the whole icon set, built from the tile")
    s.add_argument("-o", "--output", required=True, help="directory")
    s.set_defaults(fn=cmd_favicons)

    s = sub.add_parser("tokens", help="copy the design tokens out")
    s.add_argument("--format", choices=("css", "json"), default="css")
    s.add_argument("-o", "--output", required=True)
    s.set_defaults(fn=cmd_tokens)

    s = sub.add_parser("check", help="measure a colour pairing")
    s.add_argument("foreground", nargs="?")
    s.add_argument("background", nargs="?")
    s.add_argument("--role", help="check a role token instead, e.g. accent")
    s.add_argument("--against", default="bg",
                   help="the role it sits on, with --role (default: bg)")
    s.add_argument("--theme", choices=("light", "dark"), default="light")
    s.set_defaults(fn=cmd_check)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
