# GRU953 — the brand specification

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

**Confirmed by Aninda Sundar Howlader in interview.** Everything in this file is decided.
Build on it; do not re-open it without a reason and a decision.

The kit is identified by the date on the guidebook's cover, not by a version number. Anything
dated later supersedes anything dated earlier. There is no changelog and no release history.

---

## 1. Who and what

- **Brand:** `GRU953` — one word, uppercase, no hyphen, never translated, never "Gru953",
  "gru-953" or "GRU 953" in prose or in an interface. Lowercase `gru953` is a filesystem and
  package-naming convention only. The GitHub account handle is `GRU-953`, a platform
  requirement, and is **not** the brand name.
- **Said aloud:** one word — "Groo-nine-five-three".
- **Owner:** Aninda Sundar Howlader. Solo developer, Bangladesh.
- **What it is:** a solo developer's studio brand, built to grow into a software product
  house — a parent brand over individually-named apps. It is not one today, and the brand
  never pretends otherwise.
- **Audiences, in priority order:** (1) developers and the open-source community,
  (2) employers and recruiters, (3) paying clients, (4) end users of the apps.
- **Surfaces, in priority order:** GitHub (profile, README, social preview) → portfolio site
  → the apps' own interfaces → documents (CV, proposals, invoices, decks).

## 2. Fixed and not up for discussion

- **Tagline, English:** *Simple technology. For everyone.*
- **Tagline, Bangla:** *সহজ প্রযুক্তি। সবার জন্য।*
  Both are locked. Use them complete, in both languages, and do not shorten, extend or
  reword either one.
- **Purpose:** GRU953 exists to make genuinely simple, honest technology that anyone can
  use — whatever their money, language, or ability.
- **Three pillars:** Simple by design · For everyone · Honest craft.
- **Four values:** Simplicity first · Care for every user · Honesty · Craft.
- **The one rule above all:** when the guide offers a choice, choose the simpler option.
- **Bilingual English and Bangla, everywhere, by default.**

## 3. Colour

Three signature colours, two functional ones, two grounds. Named for the sky a bird climbs
into and the light that breaks over it.

| Role | Name | Bangla | Value | Use |
|---|---|---|---|---|
| Ground | **Meridian** | মেরিডিয়ান | `#1A1753` | The deep sky. Brand ground, hero panels, the wordmark on light. Also the colour of information. |
| Signature, light grounds | **Daybreak** | ভোরের আলো | `#B45A39` | The accent on white and near-white. |
| Signature, dark grounds | **Daybreak** | ভোরের আলো | `#FFAB8E` | The same hue, on Meridian and Ink. |
| Support | **Ember** | অঙ্গার | `#EDB24D` | Warm mid-tone. Gradient midpoint, secondary emphasis, and warnings. |
| Functional | **Verdant** | সবুজ | hue 152° | The only hue that means "this worked". |
| Functional | **Signal Red** | লাল | hue 25° | The only hue that means "this failed". |
| Ground | **Ink** | কালি | `#0B0E14` | Dark-theme ground; body text on paper. |
| Ground | **Paper** | কাগজ | `#FFFFFF` | Light-theme ground. |

### The rule that shapes the whole palette

**The signature is one hue with two tuned values.** *Luminance* is how much light a colour
emits — brightness, not colourfulness — and contrast is a ratio between two luminances.
To clear 4.5:1 against white a colour must be darker than luminance **0.1833**; to clear
4.5:1 against the Ink it must be lighter than **0.1946**. Both cannot be true. So no single
colour can be this brand's text colour in both themes, and pretending otherwise is how brand
guides end up with an accent that is invisible in one of them.

Both figures are computed by `04_colour/engine.py` and published in `tokens.json` under
`thresholds`, so nothing has to retype them.

`--gru-accent` therefore resolves to `#B45A39` on light grounds and `#FFAB8E` on dark ones.

**Say it precisely: one hue, two calibrated values — not one colour.** The two sit **0.51°**
apart in hue, which is one colour family, and **ΔE 24.6** apart in appearance, which is
obviously different. Side by side they read as two colours; across a theme switch they read
as the brand keeping its colour. The kit publishes both numbers rather than claiming the
friendlier one.

**Two of the three signature colours do double duty, and that is deliberate.** Ember is also
the warning colour; Meridian is also the colour of information. Five hues is a palette and
nine is a paint shop, so rather than invent new ones the system reuses these. Only Daybreak
is purely expressive. Anyone reading `--gru-warning` should expect Ember, not a surprise.

**Signature gradient** ("first light"): `#1A1753` → `#343583` → `#EDB24D` → `#FFAB8E`. Four
stops, not three: the second is Meridian's own step 800, which keeps the indigo from
jumping straight to gold across a hard seam. Hero art only, never behind body text, never on
the mark.

Every ratio, every ramp and every distinctiveness check is computed by `04_colour/engine.py`
and proved in `04_colour/CONTRAST.md`. Nothing about colour in this kit is asserted by hand.

## 4. Typography

| Role | Typeface | Licence | Why |
|---|---|---|---|
| Display, wordmark, headings (Latin) | **Sora** | SIL OFL 1.1 | Its numerals decide it: the 9, 5 and 3 have flat geometric terminals that read like instrument dials — exactly right for a name containing three digits. Wide, confident, and uncommon in developer branding. |
| Body (Latin) | **Noto Sans** | SIL OFL 1.1 | Carried forward. Nothing breaks, nothing is relicensed. |
| Bangla, all sizes | **Noto Sans Bengali** | SIL OFL 1.1 | Carried forward, and genuinely excellent. |
| Bangla display (optional) | **Anek Bangla** | SIL OFL 1.1 | For large Bangla headings where Noto Sans Bengali Bold feels too even. |
| Code, data labels, metadata | **JetBrains Mono** | SIL OFL 1.1 | Replaces a generic monospace stack, so technical labels look the same everywhere. |

Rejected, and why, so it is on the record: **Geist** (excellent, but it is Vercel's brand
face — borrowed association); **Space Grotesk** (strong, but its 5 and 3 read as
fashionable); **Chivo** (too editorial); **Bricolage Grotesque** (too busy at display
weight); **Fraunces** (charming, wrong register for a developer brand).

## 5. The mark — the Soaring Bird

The concept, the silhouette and the drawing are Aninda's, and they are kept exactly. The
mark that ships is his master path, unmodified: no re-tracing, no thickening, no
simplification.

**There is one bird.** There were once three size-graded builds. They were separate
constructions, they drifted apart, and the smallest ended up with its wing severed from its
body. One drawing cannot drift from itself, so one drawing is what ships.

- `GRU953-bird.svg` — the mark, at 24px and above.
- `GRU953-appicon.svg` — the same bird in Daybreak on a Meridian tile, below 24px and
  anywhere a filled icon is expected. A block of colour survives where a line drawing
  cannot.

**The tile has exactly one colourway: Daybreak on Meridian.** It is not recolourable, and
there is no dark-on-light variant. That is a deliberate limit, not an oversight — an icon
that changes colour stops being a recognisable object at the sizes it exists to serve. If a
surface needs a mark in some other colour, it is large enough to use the bare bird, which
*is* recolourable.

The 24px floor is not an opinion: `03_logo/marks.py` rasterises the mark at 24px on every
build and refuses to write the file if the wing's counters have closed.

**The mark does not move.** No animation, no transition, no hover state on the bird itself.

Lockups: horizontal, horizontal with the tagline, stacked, stacked with the tagline, the
wordmark alone, and the tagline alone. All text in every lockup is converted to outlines —
including the Bangla, which is shaped through HarfBuzz rather than assembled by code point.

## 6. Licence

- **The marks are not licensed.** The Soaring Bird, the wordmark, the tile and any lockup.
  Governed by `TRADEMARKS.md` and `LOGO-USAGE.md`.
- **The system is open** under the **Apache License, Version 2.0** (SPDX `Apache-2.0`, and
  OSI-approved): colour tokens, stylesheets, build scripts. Commercial use is permitted.
- **The book and the writing** are under the **PolyForm Noncommercial License 1.0.0**
  (SPDX `PolyForm-Noncommercial-1.0.0`): free to read, copy, adapt and share, but not to
  sell. **This licence is not OSI-approved** — it is source-available, and the kit says so
  rather than blurring it.
- **The bundled typefaces** keep their own SIL Open Font Licence 1.1 terms.

Full explanation in `08_guidebook/governance/LICENSING-EXPLAINED.md`.

## 7. One reading risk, accepted with eyes open

To a developer audience, **"GRU" already means Gated Recurrent Unit** — a standard
neural-network building block. Someone skimming a GitHub profile could read "GRU953" as the
name of an AI model. This is not a legal risk (nobody owns a technical term) but it is a
*reading* risk, and it is the one collision that touches the priority audience. The three
other "GRU" associations — Russian military intelligence, the *Despicable Me* character,
São Paulo's airport code — are low risk, because none is ever written with digits after it.

**Decision: keep the name.** The mitigation is contextual, not cosmetic. Wherever GRU953
first appears it is immediately followed by what it is, and the tagline sits directly under
the wordmark — which is why the kit ships lockups with the tagline built in.

## 8. Voice rules that bind all written output

Plain UK English. Warm but exact. No hype, no dark patterns, no guess presented as fact.
Claims are computed and stated with their number. Limits are named out loud. Short
sentences. Bangla is a first-class original, never a machine translation of the English.

## 9. Naming future products

GRU953 is a parent brand over apps that carry their own names, so the default is the
**endorsement form**: `<Name> by GRU953` on first mention, then the name alone.

The **prefix form** `GRU953 <Name>` is correct only when the name is too generic to stand
alone in a listing — `GRU953 Notes` rather than `Notes by GRU953`. Never both forms in one
document.

This settles a disagreement that existed between `VERBAL-IDENTITY.md` and the guidebook's
name chapter. **This section is the tie-breaker if they ever diverge again.**
