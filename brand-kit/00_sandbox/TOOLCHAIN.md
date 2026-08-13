# GRU953 Branding — Sandbox & Toolchain

**Set up:** 12 August 2026 · Sandbox root: `GRU953_Branding/` (isolated cloud workspace)

Everything below was installed and **smoke-tested** (a small real job was run through each
one to prove it works, not just that it was installed).

## What each tool is for, in plain English

### Drawing and vector graphics (the logo)
| Tool | What it does | Status |
|---|---|---|
| `rsvg-convert` | Turns a scalable logo file (SVG) into a picture file (PNG) at any size | ✅ verified |
| `svgo` 4.0.2 | Shrinks the logo file without changing how it looks | ✅ verified |
| `potrace` | Traces a bitmap picture back into clean vector outlines | ✅ installed |
| `cairosvg`, `svgwrite` | Python libraries to generate and convert SVG by code | ✅ installed |
| ImageMagick (`convert`) | General image conversion, resizing, comparison | ✅ present |
| `sharp` (via libvips 8.18.3) | Very fast, high-quality image resizing and export | ✅ verified |
| `optipng` | Makes PNG files smaller with no quality loss | ✅ installed |

### Typography (the fonts)
| Tool | What it does | Status |
|---|---|---|
| `fontTools` | Inspects, subsets and converts font files | ✅ verified |
| `fontforge` | Full font editor — for custom letterforms in the wordmark | ✅ installed |
| `woff2_compress` + `brotli`, `zopfli` | Makes web-ready font files that load fast | ✅ installed |
| Font library | **29 open-licence families, 51 font files** downloaded for comparison | ✅ verified |

Families pulled for the typography shortlist (all SIL Open Font Licence, free for
commercial use): Noto Sans, Noto Sans Bengali, Noto Serif, Noto Serif Bengali, Inter,
Manrope, Space Grotesk, Sora, Instrument Sans, Instrument Serif, Bricolage Grotesque,
Fraunces, IBM Plex Sans, JetBrains Mono, Anek Bangla, Hind Siliguri, Tiro Bangla,
Baloo Da 2, Outfit, Plus Jakarta Sans, Geist, Geist Mono, Schibsted Grotesk, Figtree,
Onest, Archivo, Chivo, Epilogue, Familjen Grotesk. All installed system-wide so they
render correctly in generated documents.

### Colour (the palette)
| Tool | What it does | Status |
|---|---|---|
| `coloraide` | Converts between colour systems and **measures contrast**, so the palette is provably readable | ✅ verified |
| `colour-science` | Research-grade colour maths, for perceptually even palette steps | ✅ installed |

### Making the actual documents
| Tool | What it does | Status |
|---|---|---|
| Playwright + Chromium 1194 | Renders web pages into pixel-perfect PNG and PDF | ✅ verified |
| `reportlab`, `ghostscript`, `qpdf`, `pdftoppm` | Build, compress and check PDFs | ✅ installed |
| `python-pptx`, `python-docx`, `openpyxl` | Build PowerPoint, Word and Excel files | ✅ installed |
| `matplotlib`, `jinja2`, `pandas` | Charts, templating, data tables | ✅ installed |
| `qrcode` | Generates QR codes for cards and print items | ✅ installed |
| `exiftool` | Writes authorship/licence metadata into delivered files | ✅ installed |

### Connected services already available (no install needed)
| Service | Use for this project |
|---|---|
| **Canva** | Optional: publish the palette + logo as a live Canva Brand Kit and templates |
| **Figma** (via your Mac) | Optional: read/write design context if you use Figma |
| **Magic Patterns** | Optional: generate a design-system web page from the tokens |
| **Mobbin** | Reference library of real product UI, for benchmarking |
| **Google Drive**, **Gmail** | Optional delivery/backup routes |

### Skills already on hand
`canvas-design` (original poster/art generation), `pdf`, `docx`, `pptx`, `xlsx`
(document building), `dataviz` (charts), `design:design-system`,
`marketing:brand-review`, `brand-voice:*` (tone-of-voice generation and checking),
`gru953-studio:brand-guardian` (keeps future projects on-brand).

## What the build actually requires

Run these from the kit's root, in this order, and each one reads the output of the ones
above it:

```
python3 05_type/install-fonts.py       # once, before any lockup is built
cd 04_colour   && python3 engine.py
cd 03_logo     && python3 marks.py && python3 lockups.py
cd 06_assets   && python3 exports.py && node outreach.mjs
python3 08_guidebook/build.py
python3 00_sandbox/verify.py
cd 00_sandbox  && node check.mjs ../08_guidebook/GRU953-Brand-Guidebook.html
```

**Inkscape is required**, and this is the one dependency that is easy to miss.
`03_logo/lockups.py` uses it to convert the Bangla tagline to outlines, because Bangla needs
real text shaping — conjuncts join and some vowel signs are written before the consonant
they follow, and pulling glyphs out of a font by code point produces nonsense. Inkscape
shapes through HarfBuzz and gets it right.

It also needs the three instanced fonts that `05_type/install-fonts.py` puts in `~/.fonts`.
Without them fontconfig does not fail — it silently substitutes a different typeface and the
lockup is drawn in the wrong font. `lockups.py` checks the family names by hand before it
draws anything, and refuses to run if the check fails.

Also needed: `rsvg-convert` (PNG rendering), Node with the `00_sandbox/node_modules` here
(`svgo` and `playwright`), and a Chromium — `00_sandbox/render.mjs` finds one, or you can
point `GRU953_CHROME` at a binary.

## One thing that could not be installed, and why it does not matter

**`scour`** (an SVG cleaner) fails to build on Python 3.11 here. `svgo` does the same job
better, is installed and working, and its configuration is in `00_sandbox/svgo.config.mjs`.

## Where things live
```
GRU953_Branding/
├── 00_sandbox/      tools, scripts, render helpers
├── 01_research/     competitor scan, name/handle checks, sources
├── 02_strategy/     positioning, personality, tone of voice
├── 03_logo/         logo suite (SVG, PNG, favicon)
├── 04_colour/       palette + contrast proofs
├── 05_type/         font candidates, specimens, final type system
├── 06_assets/       icons, patterns, imagery rules
├── 07_templates/    README, social, docs, cards
├── 08_guidebook/    the brand guidebook (HTML + PDF)
└── 09_delivery/     final packaged kit
```

## One important note
Packages are installed in **this cloud workspace**, not on your Mac. Nothing was
installed on your own computer and nothing was changed there. Finished files get
copied into your `GRU953_Branding` folder at the end.
