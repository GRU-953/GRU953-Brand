<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/readme-header-dark.png">
  <img src=".github/readme-header-light.png" alt="GRU953 — simple technology, for everyone." width="100%">
</picture>

# GRU953 — brand

**The visual and verbal identity of GRU953, the tooling that applies it, and the component
library built from it.** GRU953 is the studio name of Aninda Sundar Howlader, a solo
developer in Bangladesh. This repository is the identity itself, not an app that uses it.

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

[![Licence Apache-2.0](https://img.shields.io/badge/licence-Apache--2.0-1A1753?style=flat-square&labelColor=0B0E14)](LICENSE)
[![Writing PolyForm NC](https://img.shields.io/badge/writing-PolyForm--NC--1.0.0-B45A39?style=flat-square&labelColor=0B0E14)](LICENSE-GUIDEBOOK.md)

---

## What is in here

| Folder | What it is |
|---|---|
| **`brand-kit/`** | The identity, and everything that generates it: the palette engine, the marks, the type, the guidebook, and the 167 checks that prove it. |
| **`plugin/`** | The same rules, as something Claude can apply — a Claude Code plugin with three skills and four commands, plus each skill packaged to install on its own. |
| **`design-system/`** | 27 preview cards over 15 components, in both themes, bilingual, ready to push to Claude Design. |

Three folders, one repository, because the three share one set of design tokens. Kept apart
they drift — and they did: an audit found the plugin's copy of the tokens carrying two roles
the design system's did not. `sync-tokens.py` at the root is what stops that happening
again, and it can only do its job if all three are versioned together.

## The one thing to understand

**The signature is one hue with two tuned values.**

Contrast is a ratio between two luminances. To clear WCAG's 4.5:1 against white, a colour
must be darker than luminance **0.1833**; to clear 4.5:1 against the ink `#0B0E14`, it must
be lighter than **0.1946**. Both cannot be true.

> No single colour can be this brand's text colour in both themes. That is arithmetic, not
> taste.

So Daybreak is `#B45A39` on light grounds and `#FFAB8E` on dark ones — the same hue, 0.51°
apart, and ΔE 24.6 apart in appearance. Both numbers are published, not only the flattering
one. Use `--gru-accent` and let the theme choose. Everything else here follows from taking
that seriously.

## Try it in one minute

```bash
# what exists, and what is approved on what
python3 plugin/gru953/skills/gru953-branding/scripts/asset.py list

# the rule the brand is built on, measured rather than asserted
python3 plugin/gru953/skills/gru953-branding/scripts/asset.py check "#FFAB8E" "#FFFFFF"

# what it refuses, and why
python3 plugin/gru953/skills/gru953-branding/scripts/asset.py \
        svg bird daybreak-dark --on paper -o /tmp/x.svg
```

That last command fails on purpose. `#FFAB8E` on white measures **1.83:1** and the bird all
but disappears — which is why the signature has two values, and why a script that refuses is
more useful than a document that warns.

Open `brand-kit/08_guidebook/GRU953-Brand-Guidebook.html` in any browser to read the whole
thing. It is one self-contained file: no build step, no network, no dependency.

## Rebuild everything

```bash
cd brand-kit/04_colour && python3 engine.py     # every colour, computed and proved
cd ../..              && python3 sync-tokens.py # copy the tokens into the other two
cd design-system      && python3 build.py       # rewrite all 27 cards
node check.mjs                                  # render them and measure
cd ..                 && python3 package.py     # check everything, then build the archives
python3 brand-kit/00_sandbox/verify.py          # the kit's own 167 checks
```

`engine.py` writes nothing if any check fails. `package.py` packages nothing if any check
fails. That is deliberate: a build that half-succeeds is worse than one that stops.

Every push runs four of these in GitHub Actions — see `.github/workflows/brand.yml`. The
first job regenerates the palette and fails if the committed tokens differ from what the
engine produces, so a hand-edited output cannot survive a pull request.

## What this repository deliberately does not do

- **It does not version the brand.** No version number on the identity, the guidebook or
  the design system, and no changelog for them. A brand that ships a `v7` has told everyone
  the `v6` they are using is wrong.
- **It does not measure taste.** Contrast is measured; whether a colour feels right is not,
  and every check here ends by naming what it could not check rather than implying it did.
- **It does not carry a badge wall**, a visitor counter or a trophy case.

## Licence

**The system** — every script, the design tokens, `components.css`, the plugin and the
design system's own files: **Apache-2.0**. Use them, change them, sell what you build with
them. No permission needed. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

**The writing** — the guidebook, the reference documents and the words inside the preview
cards: **PolyForm Noncommercial 1.0.0**. Free to read, copy, adapt and share for any
noncommercial purpose; selling needs permission. It is **source-available, not open
source** — the Open Source Definition forbids restricting a field of use, so PolyForm is
not and will not be OSI-approved. See [`LICENSE-GUIDEBOOK.md`](LICENSE-GUIDEBOOK.md).

**Not licensed:** the name **GRU953**, the Soaring Bird mark, the app-icon tile, the GRU953
wordmark and any lockup of them. They identify the studio, so they stay with it. Fork the
system freely — the licence permits it — but replace the identity with your own.

**The typefaces** are SIL Open Font Licence 1.1, and each licence file travels beside them.

*Not legal advice. Written by the author, who is not a lawyer.*

---

## বাংলায়

**GRU953-এর পরিচয়, সেই পরিচয় প্রয়োগ করার টুল, আর তার উপর তৈরি কম্পোনেন্ট লাইব্রেরি।** GRU953
অনিন্দ্য সুন্দর হাওলাদারের স্টুডিওর নাম — বাংলাদেশের একজন সলো ডেভেলপার। এই রিপোজিটরিতে
পরিচয়টাই আছে, পরিচয় ব্যবহার করা কোনো অ্যাপ নয়।

সহজ প্রযুক্তি। সবার জন্য।

### এখানে কী আছে

- **`brand-kit/`** — রং, মার্ক, টাইপ, গাইডবুক, আর সব কিছু যাচাই করার স্ক্রিপ্ট।
- **`plugin/`** — একই নিয়ম, Claude-এর জন্য: তিনটি স্কিল আর চারটি কমান্ড।
- **`design-system/`** — ২৭টি প্রিভিউ কার্ড, আলো আর অন্ধকার দুই থিমেই, দুই ভাষায়।

### মূল কথাটা

কনট্রাস্ট দুটো উজ্জ্বলতার অনুপাত। সাদার উপর ৪.৫:১ পেতে রং হতে হবে গাঢ়, আর কালোর উপর ৪.৫:১
পেতে হতে হবে হালকা। **একটা রঙে দুটোই সম্ভব নয় — এটা হিসাব, পছন্দ নয়।** তাই Daybreak-এর দুটো
মান: হালকা জমিনে `#B45A39`, গাঢ় জমিনে `#FFAB8E`। একই hue, ০.৫১° তফাত। `--gru-accent`
ব্যবহার করুন, থিম নিজেই বেছে নেবে।

### শুরু করতে

গাইডবুকটা খুলুন — `brand-kit/08_guidebook/GRU953-Brand-Guidebook.html`। একটাই ফাইল,
ইন্টারনেট ছাড়াই চলে, কিছু ইনস্টল করতে হয় না।

### লাইসেন্স

**সিস্টেম** (স্ক্রিপ্ট, টোকেন, কম্পোনেন্ট, প্লাগইন): Apache-2.0 — যা খুশি করুন, বাণিজ্যিক
কাজেও, অনুমতি লাগবে না।

**লেখা** (গাইডবুক আর রেফারেন্স): PolyForm Noncommercial 1.0.0 — অবাণিজ্যিক যে-কোনো কাজে
মুক্ত, বিক্রির জন্য অনুমতি লাগবে। এটি **সোর্স-অ্যাভেইলেবল, ওপেন সোর্স নয়** — OSI-অনুমোদিত
নয়, কারণ বাণিজ্যিক ব্যবহারে বাধা আছে।

**লাইসেন্সের বাইরে:** **GRU953** নাম, Soaring Bird মার্ক, অ্যাপ-আইকন টাইল, ওয়ার্ডমার্ক আর
এগুলোর যে-কোনো লকআপ। ওগুলো স্টুডিওর পরিচয়, তাই স্টুডিওর কাছেই থাকে। সিস্টেমটা নির্দ্বিধায়
fork করুন — শুধু পরিচয়টা নিজের বসিয়ে নিন।

*এটি আইনি পরামর্শ নয়।*

---

<sub>Copyright © 2026 Aninda Sundar Howlader (GRU953) · [aninda.sh15@gmail.com](mailto:aninda.sh15@gmail.com)</sub>
