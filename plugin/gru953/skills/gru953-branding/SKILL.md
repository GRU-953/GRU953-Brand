---
name: gru953-branding
description: >
  Applies the GRU953 brand identity, and produces any single brand asset. This is the skill
  that HOLDS THE RULES — the Soaring Bird mark and every lockup, the Meridian / Daybreak /
  Ember palette and its design tokens, Sora and Noto Sans, the locked bilingual taglines, the
  English and Bangla voice, and the licence and trademark position. Use it whenever something
  is written, designed or built that carries the GRU953 name, and for any ONE asset: a mark, a
  lockup, a favicon or app-icon set, a social preview or banner, an avatar, the tokens.
  Triggers on "GRU953", "brand colours", "brand kit", "the bird", "the logo", "the wordmark",
  "the tagline", "design tokens", "Meridian", "Daybreak", "Ember", "brand voice", "write this
  in my voice", "make a banner", "make an avatar", "export the logo", "favicon", "app icon",
  "social preview", and on any request to produce a GRU953 document, post, CV, invoice or
  screen. For a WHOLE REPOSITORY use gru953-repo; for CHECKING something that exists,
  gru953-review.
license: Apache-2.0 for scripts/ and assets/; PolyForm-Noncommercial-1.0.0 for references/. NOTICE has the terms; the GRU953 marks are not licensed.
---

# GRU953 — brand

You are producing or reviewing work that carries the **GRU953** name: the studio
brand of Aninda Sundar Howlader, a solo developer in Bangladesh.

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

Every rule here comes from the GRU953 brand kit, where every number is computed
rather than asserted. Where this skill states a figure, that figure was measured.

---

## The one rule above all

**When there is a choice, take the simpler option.** Simplicity is not a style
here; it is the promise the brand makes. A decision that serves one value by
betraying another is the wrong decision.

## The eight things you must never get wrong

These are the failures that actually happen. Check them before anything else.

| # | The rule | The failure it prevents |
|---|---|---|
| 1 | The name is **`GRU953`** — one word, uppercase, no hyphen, no space, never translated. | `Gru953`, `GRU 953`, `gru-953` in prose or an interface. `gru953` is for filenames and packages only; `GRU-953` is the GitHub handle, not the name. |
| 2 | The taglines are **locked**: *Simple technology. For everyone.* and *সহজ প্রযুক্তি। সবার জন্য।* Use them complete, in both languages. | Shortening to "Simple technology", rewording, or dropping the Bangla. |
| 3 | On a **light** ground the accent is **`#B45A39`**. On a **dark** ground it is **`#FFAB8E`**. | `#FFAB8E` on white measures **1.83:1** and vanishes. This is the single most common mistake. |
| 4 | There is **one bird**. Use it at 24px and above; below that use the **tile**. | Shrinking the bare mark to favicon size. The strokes silt up and the wing closes. |
| 5 | **The mark does not move.** No animation, no hover state on the bird. | A logo caught mid-movement in a screenshot or a thumbnail. |
| 6 | The wordmark and the taglines are **artwork, not text**. Never retype them in a font. | Broken Bangla conjuncts, and a wordmark that is no longer a fixed mark. |
| 7 | **The system is Apache-2.0. The book and writing are PolyForm Noncommercial. The marks are not licensed.** PolyForm is **not** OSI-approved. | Calling the whole kit "open source", which is false. |
| 8 | Plain **UK English**. No hype, no exclamation marks manufacturing enthusiasm, no guess presented as fact. Bangla is written as an original, never translated. | "We're excited to announce" — and the word "we" for a brand with one person behind it. |

## Which reference to read, and when

Read the one you need. Do not read them all.

| If the task involves | Read |
|---|---|
| Any colour, token, theme, contrast or chart | `references/colour.md` |
| The bird, a lockup, the wordmark, an icon, clear space, sizes | `references/logo.md` |
| Typefaces, sizes, weights, the type scale | `references/typography.md` |
| Writing anything in English — copy, docs, release notes, errors | `references/voice.md` |
| Writing anything in Bangla, or anything bilingual | `references/bangla.md` |
| A LICENSE, a NOTICE, a README licence line, trademark, permissions | `references/licence.md` |
| Spacing, grid, radii, depth, motion, icons, accessibility | `references/layout.md` |
| Naming a product, an app, a repository or a package | `references/naming.md` |

## Generating an asset

`scripts/asset.py` emits any mark, in any approved colour, at any size, and
refuses combinations the brand does not permit. It needs nothing installed
beyond Python; PNG output additionally needs `rsvg-convert` or `cairosvg`.

```bash
python3 scripts/asset.py list                                  # what exists
python3 scripts/asset.py svg lockup-horizontal meridian -o out.svg
python3 scripts/asset.py png bird daybreak-dark --width 512 -o out.png
python3 scripts/asset.py favicons -o ./public                  # the whole icon set
python3 scripts/asset.py tokens --format css -o tokens.css     # the design tokens
python3 scripts/asset.py check "#FFAB8E" "#FFFFFF"             # measure a pairing
```

If the script cannot run, the raw files are in `assets/marks/` and
`assets/tokens.css`. They are drawn with `fill="currentColor"`, so you set the
colour in CSS with `color:`, not `fill:`.

## Building an interface

Use the **role tokens**, never a raw ramp step and never a literal hex value.
They are defined in both themes, so a screen built from them is correct in light
and dark with no second stylesheet.

```css
/* the ones you will actually use */
--gru-bg  --gru-surface  --gru-surface-raised  --gru-border  --gru-border-strong
--gru-ink  --gru-ink-muted  --gru-ink-subtle
--gru-brand  --gru-accent  --gru-on-accent  --gru-link  --gru-focus
--gru-info  --gru-success  --gru-warning  --gru-danger   (+ -quiet and -border)
--gru-chart-1 … --gru-chart-6
```

Paste `assets/tokens.css` in, then use the names. Do not paste hex codes.

## Before you hand anything over

Five checks, in order. Any failure is a blocker.

1. **Contrast.** Every text colour clears 4.5:1 against its own background, and
   every border or icon that must be seen clears 3:1 — **in both themes**.
2. **The mark.** Right file for the size, an approved colour pairing, clear space
   of half the bird's height on all four sides, and it is not animated.
3. **The words.** Name spelled correctly, taglines complete and in both
   languages, no hype, no "we", every claim carrying its number.
4. **The Bangla.** Present, natural, and not a translation of the English.
5. **The licence.** The right one named, and the marks reserved.

If you cannot verify one of these, say so plainly rather than assuming it passes.
Stating a limit out loud is part of the brand.

## What this brand does not do

Stating this is more useful than another adjective. GRU953 is **not** a startup
(no growth language), **not** an agency or a team (there is no "we" pretending to
be several people), **not** enterprise software (no jargon used as a credential),
**not** a personal blog brand (the work is the subject), and **not** playful for
its own sake (warmth comes from clarity and care, not from jokes).
