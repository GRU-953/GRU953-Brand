# GRU953 — typography

> **A note on the sources named here.** `BRAND-SPEC.md`, `DESIGN-RULES.md`,
> `LICENSING-EXPLAINED.md`, `TRADEMARKS.md` and `LOGO-USAGE.md` live in the GRU953
> brand kit, which is a separate deliverable and does **not** ship inside this
> plugin. Where one of them is cited below, the rule it decides is stated here in
> full — the citation records where the decision was made, not a file you need.


Everything below is read straight from `08_guidebook/assets/typography.css` (the tokens
and CSS that actually ship), cross-checked against `02_strategy/BRAND-SPEC.md` section 4
(the decision) and `02_strategy/DESIGN-RULES.md` (the layout and accessibility rules that
touch type). Every value quoted here exists in `typography.css` under the name given —
if a token name in this file doesn't match the CSS, the CSS wins; say so and fix this file.

## 1. The four faces, and the one job each has

| Role | Face | Licence | The one job |
|---|---|---|---|
| Display, wordmark, headings (Latin) | **Sora** | SIL OFL 1.1 | Carries the brand's voice at size. Never body text. |
| Body (Latin) | **Noto Sans** | SIL OFL 1.1 | Every paragraph, list, label and UI string in Latin script. |
| All Bangla, every size | **Noto Sans Bengali** | SIL OFL 1.1 | Every Bangla character, in both the body face and the display face (see §4). |
| Code, data labels, metadata | **JetBrains Mono** | SIL OFL 1.1 | Anything that must look identical on every machine: code, hashes, versions, timestamps. |
| Large Bangla headings — *optional* | **Anek Bangla** | SIL OFL 1.1 | Only loaded where a big Bangla display line is wanted and Noto Sans Bengali Bold reads too even. |

Four faces do the everyday work; Anek Bangla is the fifth, optional one, loaded on demand.

**Why Sora — remember this one, it's the decision that matters:** its numerals decide it.
GRU953 contains three digits, and Sora's 9, 5 and 3 have flat geometric terminals that read
like instrument dials — exactly right for a name built from digits. It is also wide,
confident, and uncommon in developer branding, which is why it was chosen over Geist
(borrows Vercel's association), Space Grotesk (its 5 and 3 read as fashionable), Chivo (too
editorial) and Bricolage Grotesque (too busy at display weight). `BRAND-SPEC.md` also lists
Fraunces as rejected ("charming, wrong register"); the guidebook's own generated comparison
chapter (`build.py`, `ch_type`) shows only the first four against Sora and drops Fraunces
from both the visual comparison and its prose — a minor gap between the two, not a
contradiction, and `BRAND-SPEC.md` is the confirmed source of record.

## 2. The token list — real values, from `typography.css`

Copy the name, not the number. If the scale ever changes, only the CSS file needs editing.

**Font-family tokens** (§2 of the CSS):

| Token | Value | Use it for |
|---|---|---|
| `--gru-font-display` | `"GRU953 Display", "Sora", ui-sans-serif, system-ui, sans-serif` | h1–h4, `.gru-display`, the wordmark |
| `--gru-font-text` | `"GRU953 Text", "Noto Sans", ui-sans-serif, system-ui, sans-serif` | body copy, everything else |
| `--gru-font-bangla-display` | `"GRU953 Bangla Display", "GRU953 Display", sans-serif` | `.gru-bn-display` only |
| `--gru-font-mono` | `"GRU953 Mono", "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace` | code, `.gru-mono`, `.gru-label` |

**Size scale** — a modular scale on a ratio of 1.25, anchored at 16px, in `rem` so a
reader's own text-size setting is respected:

| Token | Value | ≈ px at default zoom | Documented use |
|---|---|---|---|
| `--gru-text-2xs` | `0.694rem` | 11.1px | legal lines, table footnotes |
| `--gru-text-xs` | `0.8rem` | 12.8px | metadata, captions, badge text |
| `--gru-text-sm` | `0.9rem` | 14.4px | secondary body, table cells |
| `--gru-text-base` | `1rem` | 16px | body — never smaller for running prose |
| `--gru-text-md` | `1.125rem` | 18px | lead paragraphs |
| `--gru-text-lg` | `clamp(1.25rem, 1.15rem + 0.5vw, 1.4rem)` | 20–22.4px | h4 |
| `--gru-text-xl` | `clamp(1.5rem, 1.34rem + 0.8vw, 1.75rem)` | 24–28px | h3 |
| `--gru-text-2xl` | `clamp(1.85rem, 1.55rem + 1.5vw, 2.44rem)` | 29.6–39px | h2 |
| `--gru-text-3xl` | `clamp(2.3rem, 1.75rem + 2.75vw, 3.82rem)` | 36.8–61.1px | h1 |
| `--gru-text-4xl` | `clamp(2.9rem, 1.9rem + 5vw, 5.96rem)` | 46.4–95.4px | hero / display |

**Weights actually assigned in the CSS** (each face is a variable font covering a wider
range — Sora 100–800, Noto Sans and Noto Sans Bengali 100–900, Anek Bangla 100–800,
JetBrains Mono 100–800 — but the system only calls on these three):

| Element | Weight |
|---|---|
| `body` | 400 |
| `h1`, `h2`, `h3`, `.gru-display` | 700 |
| `h4` | 600 |
| `.gru-label`, `.gru-wordmark` | 600 / 700 (label 600, wordmark 700) |

**Line-height ("leading") tokens:**

| Token | Value | Use |
|---|---|---|
| `--gru-leading-tight` | `1.08` | display sizes only (h1 uses this) |
| `--gru-leading-snug` | `1.25` | headings generally (h1–h4) |
| `--gru-leading-normal` | `1.6` | Latin body |
| `--gru-leading-bangla` | `1.85` | Bangla body |

Bangla headings (h1–h3 with `:lang(bn)` or `.gru-bn`) get **`1.45`**, set directly in the
CSS rather than as a named token — tighter than Bangla body's 1.85, looser than Latin
headings' 1.25.

**Letter-spacing ("tracking") tokens:**

| Token | Value | Use |
|---|---|---|
| `--gru-tracking-display` | `-0.022em` | the wordmark's own tracking, and h1 |
| `--gru-tracking-tight` | `-0.014em` | headings generally |
| `--gru-tracking-normal` | `0` | body |
| `--gru-tracking-caps` | `0.09em` | small caps / mono labels (`.gru-label`) |

**Measure (maximum line length) tokens:**

| Token | Value | Why |
|---|---|---|
| `--gru-measure` | `68ch` | a Latin line longer than about 68 characters is measurably harder to read (also the reason `DESIGN-RULES.md` caps a prose page at 736px) |
| `--gru-measure-bn` | `60ch` | Bangla characters run wider, so fewer of them fit a comfortable line |

## 3. Copy-paste CSS

This reproduces the live rules in `typography.css`, using only tokens confirmed above.
`.gru-caption` and `.gru-legal` are suggested selectors built from the real `xs`/`2xs`
tokens — they are not literal class names already defined in the file, so check before
assuming they exist elsewhere.

```css
/* body copy */
body {
  font-family: var(--gru-font-text);
  font-size: var(--gru-text-base);
  line-height: var(--gru-leading-normal);
  font-weight: 400;
  letter-spacing: var(--gru-tracking-normal);
}
p, li { max-width: var(--gru-measure); }   /* stop a line running past ~68 characters */

/* headings — h1 gets its own tighter, larger treatment */
h1, h2, h3, h4, .gru-display {
  font-family: var(--gru-font-display);
  line-height: var(--gru-leading-snug);
  letter-spacing: var(--gru-tracking-tight);
  font-weight: 700;
}
h1 { font-size: var(--gru-text-3xl); line-height: var(--gru-leading-tight);
     letter-spacing: var(--gru-tracking-display); }
h2 { font-size: var(--gru-text-2xl); }
h3 { font-size: var(--gru-text-xl); }
h4 { font-size: var(--gru-text-lg); font-weight: 600; }

/* small print — captions, badges, table footnotes, legal lines */
.gru-caption { font-family: var(--gru-font-text); font-size: var(--gru-text-xs); }
.gru-legal   { font-family: var(--gru-font-text); font-size: var(--gru-text-2xs); }

/* code, data labels, metadata */
code, kbd, pre, samp, .gru-mono {
  font-family: var(--gru-font-mono);
  font-variant-ligatures: none;   /* no "=>" arrows in a brand guide — clarity wins */
  font-size: 0.92em;
}
.gru-label {
  font-family: var(--gru-font-mono);
  font-size: var(--gru-text-xs);
  font-weight: 600;
  letter-spacing: var(--gru-tracking-caps);
  text-transform: uppercase;
}

/* Bangla — see §5 for why every line here is deliberate */
:lang(bn), .gru-bn {
  line-height: var(--gru-leading-bangla);
  max-width: var(--gru-measure-bn);
  text-transform: none;
  letter-spacing: normal;
}
:lang(bn) h1, :lang(bn) h2, :lang(bn) h3, .gru-bn h1, .gru-bn h2, .gru-bn h3 {
  line-height: 1.45;
  letter-spacing: normal;
}
```

## 4. The bilingual trick — no markup, no manual font-switching

Both `"GRU953 Text"` and `"GRU953 Display"` are declared **twice** — once pointing at
their Latin file (Noto Sans, Sora), once pointing at Noto Sans Bengali — and the second
declaration is restricted to Bangla characters only, using `unicode-range`:

```css
unicode-range: U+0951-0952, U+0964-0965, U+0980-09FE, U+200C-200D, U+20B9, U+25CC, U+A8F1;
```

**In one sentence:** this tells the browser "only use this file for these specific
characters", so inside one paragraph — even inside one `<h1>` set in Sora — a Bangla
character automatically pulls the Bangla file and a Latin character automatically pulls
the Latin file, with no `<span lang="bn">`, no separate class, and no code deciding which
font to use. A sentence that mixes English and Bangla in the same line simply renders
correctly.

## 5. Bangla-specific setting

Bangla is not Latin with different letters swapped in. Four rules, in `typography.css`
unless marked otherwise:

1. **Line-height 1.85 for body text**, not Latin's 1.6. Bangla stacks marks above and
   below the মাত্রা (the headline stroke running across the top of most letters); at
   Latin's leading those marks from one line nearly touch the line below.
2. **Bangla headings (h1–h3) use 1.45**, not the 1.85 used for Bangla body and not the
   1.25 used for Latin headings — a middle value, set directly in the CSS.
3. **No letter-spacing** (`letter-spacing: normal`, always). Tracking damages Bangla
   conjunct characters — the combined letterforms Bangla builds from two or more base
   characters.
4. **No `text-transform: uppercase`, ever, and no synthetic/faux bold.** Bangla has no
   capital letters, so forcing case does nothing useful and can break conjuncts; always
   pick a real weight from the variable font instead of letting a browser fake one.
5. **Never justify Bangla text; keep it left-aligned.** Bangla words are long and break
   opportunities are fewer than in Latin text, so justification opens ugly rivers of white
   space down the page. This is standard Bangla-typesetting practice — it is **not**
   currently written into `typography.css` as an enforced rule (there is no
   `text-align` line for `:lang(bn)`), so treat it as a rule to apply by hand until it is
   codified.

## 6. Practical rules

- **Measure.** Cap a Latin line at `--gru-measure` (68ch) and a Bangla line at
  `--gru-measure-bn` (60ch). `DESIGN-RULES.md` caps a prose page at 736px width for the
  same reason — a line "measurably harder to read" past about 68 characters.
- **Weight.** 400 for body copy. 700 for headings and anything using `.gru-display`. 600
  for h4 and for `.gru-label`/mono labels. Never a faux/synthetic bold — every face here
  is a variable font, so a real weight is always available; this matters most for Bangla.
- **When NOT to use the display face.** Sora (`--gru-font-display`) is for h1–h4 and
  `.gru-display` only — that is, `--gru-text-lg` (20px) and above. Never set body copy,
  lead paragraphs, table cells or captions in it; those stay on `--gru-font-text`. And
  setting "GRU953" as live text with `.gru-wordmark` is still *text*, not the logo —
  the logo is always the SVG file, per `DESIGN-RULES.md` §1.6.
- **Numbers.** GRU953 contains three digits, which is the entire reason Sora was chosen
  (§1). The wordmark class carries that through mechanically: `.gru-wordmark` sets
  `font-feature-settings: "tnum" 1` — tabular figures — so "953" stays even-width rather
  than drifting as proportional digits would. Apply the same tabular-figure thinking
  anywhere digits must line up: version numbers, prices, table columns. JetBrains Mono
  (used for code, labels and metadata) is monospace, so every character — digits
  included — is already even-width there without any extra CSS.

## 7. Licences

All five faces — Sora, Noto Sans, Noto Sans Bengali, JetBrains Mono, Anek Bangla — ship
under the **SIL Open Font Licence 1.1**. In one line: OFL 1.1 permits using, studying,
modifying and redistributing the fonts freely, including bundling or embedding them in
commercial software, provided the font is never sold on its own. The one obligation:
where a licence reserves a font name (a **Reserved Font Name**), a modified version must
not keep using that name — so a changed version of a family is released under a new name,
never passed off as the original. Keep each `OFL-*.txt` licence file travelling alongside
its font file; that is the other half of the same condition.

## 8. Type checklist

Before anything ships:

- [ ] Sora only on h1–h4 and `.gru-display` — never on body copy, never on Bangla.
- [ ] Every size is a token (`var(--gru-text-*)`), never a hard-coded px or rem value.
- [ ] Body text is never set below `--gru-text-base` (16px).
- [ ] Bangla text carries `lang="bn"` (or `.gru-bn`) so the 1.85 leading, the 60ch measure
      and the no-caps/no-tracking rules all apply automatically.
- [ ] No `text-transform: uppercase` and no synthetic bold anywhere near Bangla.
- [ ] Bangla paragraphs are left-aligned, never justified.
- [ ] A bilingual line is written as plain mixed text — no manual font-switching, no
      extra spans; the `unicode-range` trick in §4 handles it.
- [ ] Digits that must line up (prices, versions, table columns) use tabular figures.
- [ ] Every bundled font's `OFL-*.txt` file is still sitting beside it.
