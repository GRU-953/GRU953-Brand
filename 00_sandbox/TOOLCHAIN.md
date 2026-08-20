# GRU953 — sandbox and toolchain

**Rebuilt 20 August 2026.** Sandbox root: this repository (`GRU953-Brand/`), on the
owner's own Mac. This replaces the toolchain below, which described an isolated
cloud workspace this kit could no longer be built in:

> *Packages are installed in this cloud workspace, not on your Mac. Nothing was
> installed on your own computer and nothing was changed there.*

That sentence was true and it was also the problem: the scripts it produced —
`03_logo/marks.py`, `lockups.py`, `04_colour/engine.py` — hardcoded paths that
existed only inside that container (`/home/claude/GRU953_Branding/…`,
`GRU953_Build/…`) and needed Inkscape and system-installed fonts that were never
going to be on this machine. The kit was unbuildable the moment it left the
container it was built in.

**Everything below runs from a clean checkout with one command:**

```
sh 00_sandbox/setup.sh
```

It installs nothing outside this repository. No Homebrew, no system fonts, no
setting on the Mac itself is touched. Deleting `.venv`, `00_sandbox/node_modules`
and `00_sandbox/browsers` removes the whole build environment — nothing else on
the machine knows this project was ever here.

## What runs where

| | Lives at | Committed? |
|---|---|---|
| Python, pinned exactly | `.venv/`, from `requirements.txt` | No — rebuilt by `setup.sh` |
| Node, from the lock file | `00_sandbox/node_modules/`, from `brand-kit/00_sandbox/package.json` | No |
| Chromium | `00_sandbox/browsers/`, via `PLAYWRIGHT_BROWSERS_PATH` | No |
| The three brand typefaces, for your own use in Pages/Keynote/Figma | `~/Library/Fonts/GRU953/`, via `00_sandbox/install-fonts.command` | **Optional, and the build never depends on it** — see below |

## The substitution table

Every system tool the kit's original toolchain needed has a project-local
replacement. Each one was chosen because it does the same job in a way that
travels inside a `pip install` or an `npm ci`, never a system installer.

| The old toolchain needed | Replaced by | Why |
|---|---|---|
| **Inkscape** (≈1 GB), to shape the Bangla tagline into outlines | `uharfbuzz` + `fontTools`, pinned in `requirements.txt` | The **same HarfBuzz shaping engine** Inkscape itself calls, as a plain pip package. Proven working in this sandbox: shaping ক্ষ (ka + virama + ssa — three Unicode code points) correctly collapses to one glyph, which is what conjunct formation looks like when it has actually happened. `00_sandbox/smoke.py` runs this exact check every time the sandbox is built. |
| `rsvg-convert` / `cairosvg`, to rasterise SVG to PNG | Chromium via Playwright | It is the renderer the artwork will actually be viewed in on the web — rasterising with the same engine as the audience removes a whole class of "looks right in the tool, wrong in the browser" bug. |
| ghostscript, qpdf, `pdftoppm` | Chromium's own PDF export (`page.pdf(...)`), read back with `pypdfium2` | One renderer produces both the screen build and the print build, so they cannot drift apart from each other. `pypdfium2` then lets a script read the PDF back — page count, extracted text — to prove the export actually happened, rather than trusting that `page.pdf()` returned without an exception. |
| `woff2_compress` | `fontTools[woff]` + `brotli` | Same WOFF2 format, pure pip. **The `[woff]` extra is not optional** — the bare `fonttools` package does not include the Brotli decoder, and this kit's own CI history records that gap being mistaken for five broken fonts (see the comment beside this pin in `.github/workflows/ci.yml`). |
| `optipng`, ImageMagick | Pillow | Only resize, convert and `.ico` export are ever needed; Pillow does all three without a system binary. |
| 29 typefaces installed **system-wide** so documents rendered correctly | The five shipping families live in `brand-kit/05_type/source-fonts/`, loaded by every script **from that repo-relative path**, never by font-family name | A script that asks the operating system for "Sora" gets whatever "Sora" happens to be installed as on that machine — which is exactly how a font substitution goes unnoticed. Loading the file directly means the same bytes render everywhere the repo is checked out. |

## The optional Font Book installer

`00_sandbox/install-fonts.command` is a double-clickable script — no terminal
needed — that copies the three shipping typefaces into
`~/Library/Fonts/GRU953/`, **user-level only**, so no administrator password and
no system-wide change. It exists purely so you can use the brand's own
typefaces in Pages, Keynote or Figma. `00_sandbox/uninstall-fonts.command`
removes exactly that folder and nothing else.

**The build never depends on this having been run.** Every generator resolves
fonts by the repo-relative path above, never by asking the OS for a family by
name — and `scripts/no-system-path.sh` (once it exists) proves this by building
with a throwaway `HOME`, so even an installed font cannot secretly help.

## Smoke-tested, not just installed

`00_sandbox/smoke.py` runs a **real piece of work** through every pinned tool —
converts a real colour, opens a real font and reads its character map, shapes a
real Bangla conjunct and checks it actually formed, writes and rereads a real
image, parses real SVG, renders a real template, launches Chromium and reads a
computed style back, exports a real PDF and reads its page count. An import
alone cannot tell you Brotli is missing, or that Chromium cannot launch under
this user — this can.

```
PLAYWRIGHT_BROWSERS_PATH=$(pwd)/00_sandbox/browsers .venv/bin/python 00_sandbox/smoke.py
```

Exit 0 means every tool did its job. Exit 2 means something could not run —
printed as **NOT EQUIPPED**, never silently counted as a pass.

## Historical record — the tools this kit no longer needs

Kept for the record, not as instructions: the original toolchain (12 August
2026) additionally listed `potrace`, `svgwrite`, `colour-science`, `fontforge`,
`zopfli`, `reportlab`, `python-pptx`/`python-docx`/`openpyxl`, `matplotlib`,
`pandas`, `qrcode` and `exiftool`. None of these is used by anything this kit
actually builds today; if a later phase genuinely needs one, it is added to
`requirements.txt` with a stated reason, the way every entry above has one.
