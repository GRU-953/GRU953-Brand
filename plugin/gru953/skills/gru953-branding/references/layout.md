# GRU953 — layout, motion and accessibility

> **A note on the sources named here.** `BRAND-SPEC.md`, `DESIGN-RULES.md`,
> `LICENSING-EXPLAINED.md`, `TRADEMARKS.md` and `LOGO-USAGE.md` live in the GRU953
> brand kit, which is a separate deliverable and does **not** ship inside this
> plugin. Where one of them is cited below, the rule it decides is stated here in
> full — the citation records where the decision was made, not a file you need.


Source: `02_strategy/DESIGN-RULES.md`. Token values are read from
`08_guidebook/assets/layout.css` (space, shape, depth, motion) and from this skill's
`assets/tokens.css` (colour roles, including `--gru-focus`). Where `08_guidebook/build.py`
is cited, that is the guidebook's own working implementation of a rule — shown as a
demonstrated pattern, not as an extra requirement on top of the rule itself.

---

## When the thing you need is not in the system

This comes first because it is the question that actually comes up, and a system with no
answer to it gets abandoned the first time it is inconvenient.

**You need a colour the palette does not have.** Work down this list and stop at the first
answer that works:

1. **Use a role token instead of a new colour.** Nine times out of ten the need is "a
   warning" or "a muted surface", and a token for it already exists — see `references/colour.md`.
2. **Group the data.** A chart needing a seventh series usually means fewer series is the
   honest fix: group the tail into "other", or split it into two charts. Seven colours is
   the point at which a reader stops distinguishing them anyway.
3. **Use a different step of a colour already in the palette.** Every family has eleven
   steps, and `04_colour/CONTRAST.md` records what each one clears.
4. **Only then add a hue** — properly, in `04_colour/engine.py`, as a family with a stated
   meaning, then re-run the engine (it refuses to write anything illegible or too close to
   an existing hue). Never paste a hex code into a stylesheet to get past an afternoon.

**You need a size, weight or spacing the scale does not have.** Round to the nearest step on
the scale below. If the layout genuinely breaks at that step, the layout is the problem, not
the scale.

**You need to break a rule in this document.** Write down which rule and why, in the same
place as the work. A rule broken with a reason is a decision; a rule broken quietly is drift.

---

## Space

**The grid:** 12 columns on desktop, 6 on tablet, 4 on phone, 24px gutter. Content is capped
at **1216px**; a page that is mostly prose is capped at **736px** instead — a line of text
longer than about 68 characters is measurably harder to read.

| Token | Value | Use |
|---|---|---|
| `--gru-columns` | `12` (`6` ≤60rem, `4` ≤40rem) | grid column count, set automatically by breakpoint |
| `--gru-gutter` | `--gru-space-5` (24px), `--gru-space-4` (16px) ≤40rem | gap between grid columns |
| `--gru-container` | `76rem` (1216px) | the widest content ever goes |
| `--gru-container-narrow` | `46rem` (736px) | a page that is mostly prose |
| `--gru-page-padding` | `clamp(1rem, 4vw, 3rem)` | left/right page padding |

Two ready-made classes do this without re-deriving it: `.gru-container` /
`.gru-container-narrow` (max-width + centred + side padding) and `.gru-grid` (the column
grid, gap already set to `--gru-gutter`).

**The spacing scale** is a 4px base: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 — in `rem`, so the
whole layout scales when a reader increases their default text size.

| Token | Value | Use |
|---|---|---|
| `--gru-space-1` | 0.25rem (4px) | inside a badge, between an icon and its label |
| `--gru-space-2` | 0.5rem (8px) | tight internal padding |
| `--gru-space-3` | 0.75rem (12px) | between related controls |
| `--gru-space-4` | 1rem (16px) | **the default gap — when unsure, use this** |
| `--gru-space-5` | 1.5rem (24px) | between paragraphs, inside a card |
| `--gru-space-6` | 2rem (32px) | between components |
| `--gru-space-7` | 3rem (48px) | between subsections |
| `--gru-space-8` | 4rem (64px) | between sections |
| `--gru-space-9` | 6rem (96px) | above and below a hero |
| `--gru-space-10` | 8rem (128px) | page top and tail on a wide screen |

Every gap in the system is one of these ten numbers — nothing else. The one habit that does
most of the work of an organised-looking layout: **two things that belong together get a
smaller gap than the gap to whatever comes next.**

---

## Shape

Four radii, and no more. Reusing a fifth number anywhere is a sign the layout needs one of
these four, not a new one.

| Token | Value | For |
|---|---|---|
| `--gru-radius-xs` | 4px | badges, tags, inline code |
| `--gru-radius-sm` | 8px | buttons, inputs, small cards |
| `--gru-radius-md` | 14px | cards, panels, images |
| `--gru-radius-lg` | 24px | hero panels, modal sheets |
| `--gru-radius-full` | 9999px | pills, avatars, fully round controls |

**The one exception:** `--gru-radius-appicon` is **22.46%**, not a pixel value — the
*squircle* (a rounded square, rounder than a normal button corner) that both Apple and
Google expect for an app icon. It exists only for that one job. Do not reuse 22.46%
anywhere else, and do not use one of the four radii above for an app icon.

---

## Depth

Three shadow levels, all tinted with Meridian rather than black — a grey shadow on a
coloured brand always looks slightly dirty.

| Token | Value | When |
|---|---|---|
| `--gru-shadow-1` | `0 1px 2px rgb(26 23 83/.06), 0 1px 3px rgb(26 23 83/.08)` | resting elevation — a card just barely off the page |
| `--gru-shadow-2` | `0 4px 8px rgb(26 23 83/.07), 0 8px 24px rgb(26 23 83/.09)` | a clearly raised element — a screenshot (see Images below), a focused skip link, a popover |
| `--gru-shadow-3` | `0 12px 24px rgb(26 23 83/.10), 0 24px 56px rgb(26 23 83/.14)` | the highest elevation — a hovered/lifted card, a modal sheet |

**In dark mode shadows do not work at all** — on a dark background a dark shadow is
invisible. Depth there is carried instead by a lighter surface (`--gru-surface-raised`) plus
a `--gru-border-width` (1px) border. Never simply darken the shadow and hope; switch the
technique instead.

The guidebook's own build (`08_guidebook/build.py`) demonstrates this: its `.lift` class
sits at rest with a border only, then moves to `--gru-shadow-3` on `:hover`/`:focus-within`.
That hover-lift is a decorative flourish of the guidebook itself, not a general rule — the
rule is the three levels and the dark-mode substitution.

---

## Motion

**Two durations, two curves — nothing else:**

| Token | Value | For |
|---|---|---|
| `--gru-duration-fast` | 120ms | a colour change, a hover, a focus ring |
| `--gru-duration-base` | 220ms | something arriving or leaving — a panel, a reordering list |
| `--gru-ease-out` | `cubic-bezier(0.22, 1, 0.36, 1)` | things arriving |
| `--gru-ease-in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` | things moving in place |

Anything above 300ms on an interface element reads as broken, not elegant. A ready-made
`.gru-transition` class in `layout.css` wires colour, background, border and box-shadow to
`--gru-duration-fast`, and `transform` to `--gru-duration-base`, both eased with
`--gru-ease-out`.

**What may move:** a panel sliding in, a list reordering, a loading indicator, a focus ring,
a number counting up to its value once.

**What may never move: the logo.** The Soaring Bird does not flap, fly across the screen,
draw itself in, or pulse — a logo that performs is asking for attention rather than earning
it, and it dates within a year. The single permitted exception is a fade-in on first page
load, at 220ms, once.

**`prefers-reduced-motion` is not a nice-to-have.** Honouring it costs four lines of CSS, and
a brand whose second pillar is "for everyone" does not get to skip it. The guidebook's own
reduced-motion block is the pattern to copy:

```css
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1 !important; transform: none !important; transition: none !important; }
  .lift, .tilt { transition: none !important; }
  .lift:hover, .lift:focus-within, .tilt:hover { transform: none !important; }
}
```

Written the other way round — hiding content by default and only revealing it once a script
adds a class — is a trap: anyone whose JavaScript is blocked, or has not run yet, never sees
the content at all. Scope any "hidden until revealed" state to a class JavaScript itself
adds (the guidebook uses `.js-anim`), never to the bare element.

---

## Icons

Material Symbols (Apache-2.0, free for any purpose), **Rounded** style, **weight 300**,
optical size matched to the text beside it. This was the right choice already made — there
is no reason to churn it.

- **1.5px stroke at 24px**, scaling proportionally. Never mix stroke weights in one view.
- Icons **inherit the text colour** they sit beside. An icon is not an opportunity for
  colour.
- **An icon never carries meaning alone.** Every icon that means something has a text
  label, or an `aria-label` if it genuinely cannot — a screen reader announces nothing at
  all for a bare icon. This is not optional politeness.
- Do not draw custom icons unless Material Symbols has no equivalent. One inconsistent
  custom icon is more noticeable than a slightly imperfect standard one.

---

## Images and alt text

**Alt text says what an image *means*, not what it *is*.** The logo's alt text is
`GRU953`, not "logo". Decorative art gets `alt=""` so a screen reader skips it rather than
narrating it uselessly. The logo SVGs already carry `<title>` and `<desc>`, so an inline SVG
is announced correctly with no extra work.

The picture policy behind this, in order: no picture first (type, space, one colour beat a
decorative image most of the time); failing that, the real thing (an actual screenshot, an
actual desk, the actual person — real and slightly imperfect beats polished and generic);
failing that, generated abstract art built from the brand's own geometry (the first-light
gradient, the wing's facet angles, the grid); never stock photos of people, handshakes,
glowing brains or circuit-board overlays, and never anything implying a team that does not
exist.

Screenshots get a fixed treatment: `--gru-radius-md` (14px), a 1px border, and
`--gru-shadow-2`. Nothing else.

---

## Accessibility

The floors, none of them negotiable:

| Requirement | The rule |
|---|---|
| Text contrast | 4.5:1 normal text, 3:1 large (24px, or 19px bold) |
| Non-text contrast | 3:1 for UI parts, focus rings, meaningful graphics |
| Focus visible | a 3px ring at 2px offset, on every interactive thing |
| Keyboard | everything reachable and operable without a mouse — test it, don't assume it |
| Text size | body text never below 16px; every size expressed in `rem` |
| Reduced motion | honoured — see Motion above |
| Target size | 24×24px minimum for anything tappable, 44×44px preferred |

The focus ring uses the `--gru-focus` colour role token (defined per theme in
`tokens.css`) and looks like this in practice:

```css
:focus-visible { outline: 3px solid var(--gru-focus); outline-offset: 2px; }
```

**Colour is never the only signal.** Every state carries a second cue: an error is red
*and* says "Error" *and* has an icon; a required field is marked with a word, not a colour;
a chart series is distinguished by a shape or a direct label, not by hue alone. Roughly one
man in twelve has some form of colour-vision deficiency — this rule is the difference
between a design that works for them and one that doesn't.

**Language must be declared.** Every page sets `lang`, and every Bangla passage inside an
English page sets `lang="bn"`. Without it a screen reader tries to pronounce Bangla with
English rules and the result is unintelligible — for a bilingual brand this is the single
highest-value accessibility line of code there is.

**Forced colours (Windows High Contrast and similar):** the default is to let the operating
system replace the palette — do not fight it. `tokens.css` remaps only the handful of roles
that must still make sense (`--gru-focus`, `--gru-link`, `--gru-ink`, `--gru-bg`,
`--gru-border`) to system colour keywords under `@media (forced-colors: active)`. The one
exception to "let it win" is content whose actual subject is colour itself — a swatch, a
palette ramp, a chart bar — which opts out with `forced-color-adjust: none` so the thing
being shown does not collapse into a single flat system colour.

**What this does not claim:** passing a contrast ratio does not make a screen readable —
size, weight, line length and the sheer amount of text all matter and none of them is
measured by a ratio; nothing in this kit has been tested with a real screen reader by a real
user, which is a genuine gap stated plainly rather than papered over.

---

## A copy-paste CSS starter

This sets a page up correctly from the tokens. Load `tokens.css` (colour roles) and
`layout.css` (space, shape, depth, motion — the subset used below is reproduced here so this
block is self-contained) before it, then use these classes directly.

```css
/* ---- from layout.css: the tokens this starter uses ---- */
:root {
  --gru-space-4: 1rem;      /* 16px — default gap */
  --gru-space-5: 1.5rem;    /* 24px — inside a card */
  --gru-radius-sm: 8px;     /* buttons, inputs */
  --gru-radius-md: 14px;    /* cards */
  --gru-shadow-1: 0 1px 2px rgb(26 23 83 / 0.06), 0 1px 3px rgb(26 23 83 / 0.08);
  --gru-shadow-3: 0 12px 24px rgb(26 23 83 / 0.10), 0 24px 56px rgb(26 23 83 / 0.14);
  --gru-duration-fast: 120ms;
  --gru-duration-base: 220ms;
  --gru-ease-out: cubic-bezier(0.22, 1, 0.36, 1);
}

/* ---- the scene: one shared vanishing point, set once on a wrapper ---- */
/* Optional flourish, not a brand requirement — skip it for a flat, equally correct page. */
.scene { perspective: 1400px; perspective-origin: 50% 30%; }

/* ---- a card ---- */
.card {
  background: var(--gru-surface);
  border: var(--gru-border-width) solid var(--gru-border);
  border-radius: var(--gru-radius-md);
  padding: var(--gru-space-5);
  box-shadow: var(--gru-shadow-1);
  transition: box-shadow var(--gru-duration-base) var(--gru-ease-out),
              border-color var(--gru-duration-fast) var(--gru-ease-out);
}
.card:hover, .card:focus-within {
  box-shadow: var(--gru-shadow-3);
  border-color: var(--gru-border-strong);
}

/* ---- a button, with its states ---- */
.btn {
  font: inherit; font-weight: 600; cursor: pointer;
  background: var(--gru-brand);
  color: var(--gru-on-brand);
  border: var(--gru-border-width) solid var(--gru-brand);
  border-radius: var(--gru-radius-sm);
  padding: var(--gru-space-3) var(--gru-space-5);
  transition: background-color var(--gru-duration-fast) var(--gru-ease-out),
              border-color var(--gru-duration-fast) var(--gru-ease-out);
}
.btn:hover   { background: var(--gru-brand-hover); border-color: var(--gru-brand-hover); }
.btn:active  { background: var(--gru-brand-active); border-color: var(--gru-brand-active); }
.btn:disabled {
  background: var(--gru-disabled-bg);
  color: var(--gru-disabled-ink);
  border-color: var(--gru-disabled-border);
  cursor: not-allowed;
}

/* ---- the focus ring: on every interactive element, no exceptions ---- */
:focus-visible { outline: 3px solid var(--gru-focus); outline-offset: 2px; }

/* ---- reduced motion: switches all of the above off, honestly ---- */
@media (prefers-reduced-motion: reduce) {
  .card, .btn { transition: none !important; }
  .card:hover, .card:focus-within { box-shadow: var(--gru-shadow-1); }
}
```

Every token above is a real token: the space, radius, shadow, duration and ease values come
from `08_guidebook/assets/layout.css`; the colour roles (`--gru-brand`, `--gru-on-brand`,
`--gru-brand-hover`, `--gru-brand-active`, `--gru-border`, `--gru-border-strong`,
`--gru-disabled-bg`, `--gru-disabled-ink`, `--gru-disabled-border`, `--gru-surface`,
`--gru-focus`) come from this skill's `assets/tokens.css`, defined in both the light and
dark theme blocks.

---

## Layout checklist

1. **Missing colour, size or spacing?** Worked down the list in "When the thing you need is
   not in the system" before adding anything new.
2. **Every gap is one of the ten spacing-scale numbers.** Used `--gru-space-4` (16px) where
   unsure. Related things sit closer together than the gap to what's next.
3. **Every corner is one of the four radii** — or, for an app icon only, the 22.46% squircle.
4. **Depth uses a shadow token, never a hand-written `box-shadow`.** Dark mode gets a
   raised surface plus a border, not a darker shadow.
5. **Every transition uses `--gru-duration-fast`/`--gru-duration-base` and an ease token** —
   nothing slower than 300ms on an interface element.
6. **The logo does not move**, anywhere, ever — except the one permitted 220ms fade-in on
   first load.
7. **`prefers-reduced-motion: reduce` turns every transition and transform off.** Tested,
   not assumed.
8. **Every icon has a label or an `aria-label`,** inherits its neighbouring text colour, and
   matches the Rounded/300 style with no mixed stroke weights.
9. **Every image's alt text says what it means**, decorative images carry `alt=""`, and
   `lang`/`lang="bn"` is set wherever the language changes.
10. **Contrast, focus rings and target size all meet the floors in Accessibility above,**
    and colour is never the only carrier of a state.
