# Licensing, explained in plain English

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

**This is not legal advice.** It was written by the kit's author, who is not a lawyer. It
explains what the licences say and why they were chosen. If a real decision turns on it,
read the licences themselves — both are included in full, unmodified — or ask a lawyer.

---

## 1. The one-paragraph version

The kit is split into four parts, and each part has the licence that actually fits it. The
**machine-readable system** — colours, tokens, stylesheets, scripts — is under
**Apache-2.0**, a genuinely open licence approved by the Open Source Initiative: anyone may
use it for anything, including making money. The **book and the writing** are under
**PolyForm Noncommercial 1.0.0**: free to read, copy, adapt and share, but not to sell. The
**marks** — the bird, the wordmark, the lockups — are **not licensed to anyone**. The
**typefaces** keep their own **SIL Open Font Licence 1.1**.

---

## 2. The table

| What | Licence | Approved by the OSI? | May I use it commercially? |
|---|---|:---:|---|
| Colour tokens, CSS, every script in this kit | **Apache-2.0** | **Yes** | Yes, freely |
| The guidebook, the chapters, the templates, the documentation | **PolyForm Noncommercial 1.0.0** | **No** | Not without asking |
| The Soaring Bird, the GRU953 wordmark, the lockups, the app icon | **Not licensed** | n/a | No |
| Sora, Noto Sans, Noto Sans Bengali, JetBrains Mono | **SIL OFL 1.1** | **Yes** | Yes, per the OFL |

---

## 3. Why Apache-2.0 for the system

Three reasons, in the order they mattered.

1. **It is an OSI-approved open source licence.** That is not a slogan; it is a checkable
   fact, and it is what makes the "for everyone" pillar true rather than decorative.
   Verified against the Open Source Initiative's approved list on 13 August 2026.
2. **Section 6 protects the marks without any extra work.** Apache-2.0 grants copyright and
   patent permissions and expressly does *not* grant permission to use the licensor's trade
   names or trademarks. So someone can copy every colour value in this kit and still have
   no right to present their work as GRU953's. A licence like MIT would have needed a
   separate trademark notice bolted on beside it.
3. **It carries an express patent grant and a patent-retaliation clause.** MIT and BSD do
   not. For anything that might grow into a product, that is worth having.

The one cost of Apache-2.0 is that it is longer than MIT and asks redistributors to keep a
NOTICE file. That cost is real and it was accepted deliberately.

## 4. Why PolyForm Noncommercial for the book

The guidebook is not a component. It is GRU953's own brand book — the thing that says how
GRU953 looks and speaks. Putting it under a permissive licence would have permitted someone
to sell it, or to sell a rebadged version of it, which is not a freedom worth granting.

**PolyForm Noncommercial 1.0.0** says exactly the intended thing and nothing else: use it,
copy it, change it, share it, for any noncommercial purpose. Learn from it. Teach from it.
Just do not sell it.

It was chosen from the PolyForm family — the alternatives being Small Business, Perimeter
and Shield — because the boundary that matters here is *commercial versus not*, not company
size and not competition.

### Two honest limits of this choice

- **PolyForm Noncommercial is not an open source licence.** The Open Source Initiative has
  not approved it and will not, because the Open Source Definition forbids restricting a
  field of use, and "noncommercial only" is exactly that restriction. Anyone who calls this
  book "open source" is wrong. It is *source-available*. Verified on 13 August 2026.
- **The PolyForm licences are drafted for software.** Their text says "the software"
  throughout. Applying one to a document works by defining the document as the licensed
  work — which is what the NOTICE file does — but it is not the use the drafters had in
  mind, and no lawyer has reviewed this application of it.

## 5. Why the marks are not licensed at all

A trademark and a copyright licence do different jobs. Copyright decides who may copy a
file. A trademark decides who may claim to *be* GRU953. Giving away the second one would
make the brand meaningless.

So neither licence touches the marks, and both say so. The rules for using them are in
**TRADEMARKS.md**; the rules for drawing them correctly are in **LOGO-USAGE.md**.

## 5a. Which licence applies to which file

The rule is: **anything a machine reads is Apache-2.0; anything a person reads is
PolyForm; anything that identifies GRU953 is neither.** This table resolves every file in
the kit, so there is no grey area to argue about.

| Path | Licence | Why |
|---|---|---|
| `04_colour/*.py`, `03_logo/*.py`, `05_type/*.py`, `06_assets/*.py`, `06_assets/*.mjs`, `08_guidebook/build.py`, `00_sandbox/*.py`, `00_sandbox/*.mjs` | **Apache-2.0** | Code. Each file carries an `SPDX-License-Identifier` header. |
| `08_guidebook/assets/tokens.css`, `tokens.json`, `typography.css`, `layout.css` | **Apache-2.0** | The machine-readable system. |
| `*/MANIFEST.json`, `03_logo/lockup-manifest.json`, `09_delivery/VERIFICATION.txt` | **Apache-2.0** | Build output of Apache-2.0 scripts. |
| `08_guidebook/GRU953-Brand-Guidebook.html` and `.pdf`, `08_guidebook/chapters/*.md` | **PolyForm Noncommercial 1.0.0** | The book. |
| `02_strategy/*.md`, `01_research/*.md`, `04_colour/CONTRAST.md`, `START-HERE.md`, `00_sandbox/TOOLCHAIN.md` | **PolyForm Noncommercial 1.0.0** | Documentation written for a reader. |
| `07_templates/*.md` | **PolyForm Noncommercial 1.0.0** | Written content. The *wording you adapt for your own work* is yours; the templates themselves are not for resale. |
| `08_guidebook/governance/*` | The licence texts are the licensors' own; the explanatory files here are **PolyForm Noncommercial 1.0.0** | |
| `03_logo/*.svg`, `06_assets/png/*`, `06_assets/favicon/*`, `06_assets/outreach/*` | **Not licensed** | These are the marks, or artwork built from them. See `TRADEMARKS.md`. |
| `05_type/**`, `08_guidebook/assets/fonts/**` | **SIL OFL 1.1** | Third-party typefaces. Each `OFL.txt` travels beside its font. |

### Why there is no REUSE / SPDX manifest

The [REUSE specification](https://reuse.software) would put a licence header, or a `.license`
sidecar, on every one of the several hundred files here. That is the right answer for a
project with contributors. For a kit maintained by one person it is several hundred places
for the truth to drift, and the table above is one. The code files carry SPDX headers
because they are the files most likely to be copied out on their own; everything else is
resolved here.

## 6. What you must do when you redistribute

**If you use the Apache-2.0 parts** (tokens, CSS, scripts) in your own project:

1. Include a copy of `LICENSE`.
2. Include a copy of `NOTICE`, or the parts of it that apply.
3. Keep any copyright, patent, trademark and attribution notices in the files you took.
4. State that you changed the files, if you changed them.
5. Do not use the GRU953 name or marks to describe your work.

**If you share the book or the writing** under PolyForm Noncommercial:

1. Do not sell it, and do not use it in the course of making money.
2. Pass on a copy of `LICENSE-GUIDEBOOK.md`, or the URL for it.
3. Pass on the `Required Notice:` line, which is in `NOTICE`.
4. Do not use the GRU953 name or marks to describe your work.

## 7. Updating your own repositories

Do these in order. Each step is one action.

1. Open the repository you want to update.
2. Copy `08_guidebook/governance/LICENSE` into the repository root, named `LICENSE`.
3. Copy `08_guidebook/governance/NOTICE` into the repository root, named `NOTICE`.
4. If the repository ships the guidebook or long-form GRU953 writing, also copy
   `LICENSE-GUIDEBOOK.md` into the root.
5. Open the repository's `README.md`.
6. Find the licence line near the bottom. Replace it with:
   `Licensed under Apache-2.0. See LICENSE and NOTICE. The GRU953 marks are not licensed.`
7. If a source file carries an old licence header, replace that header with the standard
   Apache-2.0 header, which is at the very end of `LICENSE`.
8. Commit with the message `chore: adopt Apache-2.0 for the system, PolyForm for the book`.
9. Repeat for each repository.

## 8. Permissions

Anything the licences do not permit, ask for. Commercial use of the book, use of the
marks, a bundling arrangement, an exception: **aninda.sh15@gmail.com**.

A short, specific email describing exactly what you want to do gets a faster answer than a
general one.

---

Copyright © 2026 Aninda Sundar Howlader (GRU953).
