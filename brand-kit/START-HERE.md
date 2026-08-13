# GRU953 — the brand kit

**সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.**

Built 13 August 2026 for Aninda Sundar Howlader.

---

## Read this first

**Open `08_guidebook/GRU953-Brand-Guidebook.html` in your browser.** That one file is the
whole brand: twelve chapters, every logo, every colour, every rule, and a download button
for every single file in the kit. It needs no internet connection, because every font,
image and asset is embedded inside it. If you only ever open one file from this kit, open
that one.

`GRU953-Brand-Guidebook.pdf` is the same book as A4 pages, for printing or emailing.

---

## The five things that decide everything else

| | The decision |
|---|---|
| **Name** | `GRU953` — one word, uppercase, no hyphen, never translated. Always followed immediately by what it is. |
| **Tagline** | *Simple technology. For everyone.* · *সহজ প্রযুক্তি। সবার জন্য।* Locked. Both languages, complete, never reworded. |
| **Mark** | One bird — your own drawing, shipped unmodified. Used at 24px and above; below that, the tile. The mark does not move. |
| **Colour** | Meridian `#1A1753` as the ground. Daybreak as the signature: **one hue, two tuned values** — `#B45A39` on light grounds, `#FFAB8E` on dark ones. One value cannot be legible on both; the guidebook's Colour chapter shows the arithmetic. |
| **Licence** | Apache-2.0 for the system. PolyForm Noncommercial 1.0.0 for the book. The marks are not licensed at all. |

---

## The seven things to do next, in order

1. **Open the guidebook.** Read the first three chapters, about ten minutes. They are the
   whole brand.
2. **Set the social preview on your repositories.** GitHub → each repository → Settings →
   Social preview → upload `06_assets/outreach/github-social-preview.png`. Twenty seconds
   per repository, and it is the highest-return brand action available on GitHub.
3. **Update your GitHub profile README** with `07_templates/github-profile-README.md`.
4. **Change your avatar** to `06_assets/outreach/avatar-512.png` on GitHub, LinkedIn and X.
5. **Register a domain while it is free.** As of 13 August 2026, `gru953.com`, `.dev`,
   `.io`, `.org` and `.net` were all unregistered — verified by RDAP lookup against the
   registries themselves, not guessed. They will not stay free, and they are cheap.
6. **Reserve the package names** `gru953` on npm and on PyPI. Both were free on the same
   date, checked against each registry's own API.
7. **Work through `08_guidebook/governance/LICENSING-EXPLAINED.md`** when you are ready to
   update your existing repositories. Section 7 is a numbered list of exactly what to change.

---

## What is in each folder

| Folder | What is in it | Do you need to open it? |
|---|---|---|
| `08_guidebook/` | **The guidebook** (HTML and PDF), the stylesheets, the webfonts, and the governance documents | **Yes — start here** |
| `03_logo/` | The Soaring Bird, the tile, six lockups. All SVG, all recolourable | When you need a logo file |
| `06_assets/outreach/` | Ready-made artwork at exact platform sizes: GitHub preview, avatar, X header, LinkedIn banner, README banners, Open Graph card, palette poster | Yes, for step 2 above |
| `06_assets/png/` | PNG exports of every mark in every approved colour | Only if something cannot use SVG |
| `06_assets/favicon/` | `favicon.ico`, the SVG icon, the Apple touch icon, and the PNG set | When you build your website |
| `07_templates/` | Profile README, repository README, CV content, email signature, invoice and proposal wording, social post copy | When you write one of those things |
| `02_strategy/` | The brand specification, the voice guide (English), the voice guide (Bangla), the design rules | Reference — it is all in the guidebook too |
| `04_colour/` | The palette engine, and `CONTRAST.md` — every ratio computed | Only if you change a colour |
| `01_research/` | What was verified, when, against which source — and a clearly marked list of what could not be verified | Worth reading once |
| `05_type/source-fonts/` | The typefaces as their original variable-font files, each with its licence | Only if you need the desktop fonts |
| `00_sandbox/` | `TOOLCHAIN.md` (what was installed and why) and `verify.py` (the mechanical checks) | Archive |
| `09_delivery/` | The packaged kit, and `VERIFICATION.txt` — the full pass/fail report | Worth a glance |

---

## Two honest things

**One reading risk.** To a developer audience, "GRU" already means *Gated Recurrent Unit* — a
standard neural-network component. Someone skimming your GitHub could read "GRU953" as the
name of an AI model. It is not a legal risk and the name stays, but it is why the tagline
sits directly under the wordmark everywhere: so the reading is settled before it can drift.
That is also why the kit ships lockups with the tagline built into the artwork. The other
three "GRU" associations — Russian intelligence, the *Despicable Me* character, São Paulo
airport — were all checked and are low risk, because none of them is ever written with
digits after it.

**One genuine gap.** Nothing in this kit has been tested with a real screen reader by a real
user. The contrast is computed and proved; lived accessibility is not the same thing. That
is stated in the guidebook too, rather than quietly omitted.

---

## How to regenerate anything

Every generated file has a script beside it, so nothing is a dead end. Run each from its
own folder:

```
python3 05_type/install-fonts.py         # ONCE per machine, before any lockup is built
cd 04_colour   && python3 engine.py      # colours -> tokens.css, tokens.json, CONTRAST.md
cd 03_logo     && python3 marks.py       # the bird and the tile, from your master drawing
cd 03_logo     && python3 lockups.py     # every lockup, from the bird + outlined type
cd 06_assets   && python3 exports.py     # every PNG, and the favicon set
cd 06_assets   && node outreach.mjs      # all the social and profile artwork
python3 08_guidebook/build.py            # the guidebook (add --print for the PDF source)
python3 00_sandbox/verify.py             # the mechanical checks
cd 00_sandbox  && node check.mjs ../08_guidebook/GRU953-Brand-Guidebook.html
```

Run them in that order: each one reads the output of the ones above it.

**The first line is not optional.** `lockups.py` needs three fonts installed by name, because
it uses Inkscape to convert the Bangla tagline to real shaped outlines. Without them it
refuses to run rather than quietly drawing the wrong typeface. It will tell you so, and tell
you this command.

`00_sandbox/TOOLCHAIN.md` lists every tool, what it is for, and what the build actually
requires — in plain English.

---

## Licence, in one line each

- **The marks** — the Soaring Bird, the wordmark, the tile, any lockup: **not licensed.**
  Yours alone.
- **The system** — colour tokens, CSS, scripts: **Apache-2.0**, an OSI-approved open source
  licence. Anyone may use it, including commercially.
- **The book and the writing** — this guidebook, the templates, the documentation:
  **PolyForm Noncommercial 1.0.0.** Free to read, copy, adapt and share. Not to sell. This
  licence is **not** OSI-approved; it is source-available, and the kit says so plainly.
- **The typefaces**: **SIL Open Font Licence 1.1.** Their licences travel with the files.

Full documents in `08_guidebook/governance/`. Permissions: **aninda.sh15@gmail.com** — that
address appears in `NOTICE`, `TRADEMARKS.md`, `LOGO-USAGE.md` and `LICENSING-EXPLAINED.md`.
Change it in those four files if you would rather use a different one.

*Not legal advice — written by the kit's author, who is not a lawyer.*

---

Copyright © 2026 Aninda Sundar Howlader (GRU953).
