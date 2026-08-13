#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Export every mark as PNG, and build the favicon set.

Why PNGs exist at all when the kit is SVG: a few places still cannot take an SVG — some
email clients, some app-store upload forms, older office software. These are for those
places, and nothing else. If SVG is an option, use the SVG.

Every file here is derived from the SVGs in 03_logo, so nothing can drift out of step.
Colours are read from the generated tokens, never retyped.

Run:  cd 06_assets && python3 exports.py
"""
import json, pathlib, subprocess, shutil, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGO, OUT, FAV = ROOT / "03_logo", ROOT / "06_assets/png", ROOT / "06_assets/favicon"
TOK = json.loads((ROOT / "08_guidebook/assets/tokens.json").read_text())

MERIDIAN = TOK["families"]["meridian"]["anchor"]
DAYBREAK = TOK["accent"]["dark"]
ACCENT_LIGHT = TOK["accent"]["light"]
INK, PAPER = TOK["ground"]["ink"], TOK["ground"]["paper"]

# Each colour is paired with the ground it is APPROVED on, so no PNG here can be an
# unusable combination. This is the same rule the guidebook states in Colour.
COLOURS = [
    ("meridian", MERIDIAN, PAPER),      # the mark on paper
    ("accent", ACCENT_LIGHT, PAPER),    # the signature, light ground
    ("daybreak", DAYBREAK, MERIDIAN),   # the signature, on the brand ground
    ("paper", PAPER, MERIDIAN),         # reversed out
    ("ink", INK, PAPER),                # one-colour print
]
MARKS = {
    "GRU953-bird": (256, 512, 1024),
    "GRU953-wordmark": (512, 1024),
    "GRU953-lockup-horizontal": (512, 1024, 2048),
    "GRU953-lockup-horizontal-tagline": (1024, 2048),
    "GRU953-lockup-stacked": (512, 1024),
    "GRU953-lockup-stacked-tagline": (1024, 2048),
    "GRU953-tagline": (512, 1024),
}


def render(svg_text, width, out, bg=None):
    tmp = pathlib.Path("/tmp/_export.svg")
    tmp.write_text(svg_text, encoding="utf-8")
    cmd = ["rsvg-convert", "-w", str(width), str(tmp), "-o", str(out)]
    if bg:
        cmd[1:1] = ["-b", bg]
    subprocess.run(cmd, check=True, capture_output=True)
    # rsvg writes correct but loosely-packed PNGs. optipng repacks them losslessly — the
    # pixels are bit-for-bit identical, the file is roughly a third smaller. That matters
    # here because every one of these is embedded in the guidebook as base64, where a byte
    # saved costs a byte and a third.
    if shutil.which("optipng"):
        subprocess.run(["optipng", "-quiet", "-o3", "-strip", "all", str(out)],
                       capture_output=True)


def main():
    # Build into a fresh directory and swap it in only when everything succeeded. Deleting
    # the real one first meant that any failure part-way through — a missing SVG, a
    # rsvg-convert error — destroyed a complete set of exports and left a partial one behind
    # that looked finished.
    staging = OUT.parent / (OUT.name + ".building")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    FAV.mkdir(parents=True, exist_ok=True)
    made = []

    for name, sizes in MARKS.items():
        src = LOGO / f"{name}.svg"
        if not src.exists():
            sys.exit(f"FAIL — {src} is missing. Run marks.py and lockups.py first.")
        raw = src.read_text()
        for cname, fg, ground in COLOURS:
            body = raw.replace("currentColor", fg)
            for w in sizes:
                # Transparent background: the caller decides the ground. The approved
                # ground is recorded in the manifest so nobody has to guess.
                p = staging / f"{name}-{cname}-{w}.png"
                render(body, w, p)
                made.append(dict(file=p.name, mark=name, colour=fg, on=ground, width=w))

    # the app icon, already coloured, at the sizes stores and launchers ask for
    icon = (LOGO / "GRU953-appicon.svg").read_text()
    for w in (128, 256, 512, 1024):
        p = staging / f"GRU953-appicon-{w}.png"
        render(icon, w, p)
        made.append(dict(file=p.name, mark="GRU953-appicon", colour=DAYBREAK,
                         on=MERIDIAN, width=w))

    # ---------------------------------------------------------------- favicons
    # A browser tab is 16px. The bare mark cannot survive that, so the FAVICON IS THE TILE.
    # This is the same rule as everywhere else in the kit, applied honestly.
    for w in (16, 32, 48, 64, 128, 256):
        render(icon, w, FAV / f"favicon-{w}.png")
    render(icon, 180, FAV / "apple-touch-icon.png")
    ims = [Image.open(FAV / f"favicon-{w}.png").convert("RGBA") for w in (16, 32, 48, 64)]
    ims[0].save(FAV / "favicon.ico", format="ICO",
                sizes=[(16, 16), (32, 32), (48, 48), (64, 64)], append_images=ims[1:])
    shutil.copyfile(LOGO / "GRU953-appicon.svg", FAV / "icon.svg")
    # Safari's pinned-tab icon must be a single-colour silhouette on a transparent ground.
    mask = (LOGO / "GRU953-bird.svg").read_text().replace("currentColor", "#000000")
    (FAV / "mask-icon.svg").write_text(mask)

    (staging / "MANIFEST.json").write_text(json.dumps(
        dict(note="Every PNG is rendered from the SVG in 03_logo. Backgrounds are "
                  "transparent; 'on' records the ground the colour is approved against.",
             files=made), indent=2) + "\n")
    # everything succeeded: swap the finished set in
    if OUT.exists():
        shutil.rmtree(OUT)
    staging.rename(OUT)
    print(f"{len(made)} PNGs -> 06_assets/png/")
    print(f"favicon set (tile-based, because a 16px tab cannot hold a line drawing) "
          f"-> 06_assets/favicon/")


if __name__ == "__main__":
    main()
