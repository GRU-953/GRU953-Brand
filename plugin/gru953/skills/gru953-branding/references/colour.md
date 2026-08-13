# GRU953 — colour

Every figure on this page was computed by the brand kit's palette engine, not
chosen by eye. Where a number appears, it was measured.

---

## The one thing to understand first

**The signature is one hue with two tuned values.**

Contrast is a ratio between two luminances — luminance being how much light a
colour emits, its brightness rather than its colourfulness. To clear WCAG's
4.5:1 against white, a colour must be *darker* than luminance **0.1833**. To
clear 4.5:1 against the Ink `#0B0E14`, it must be *lighter* than **0.1946**.

Both cannot be true.

> **No single colour can be this brand's text colour in both themes.** That is
> arithmetic, not taste.

So Daybreak is two values from one ramp:

| Theme | `--gru-accent` resolves to | Ground | Ratio |
|---|---|---|---|
| light | `#B45A39` | `#FFFFFF` | **4.71:1** |
| dark | `#FFAB8E` | `#0B0E14` | **10.55:1** |

They are **0.51°** apart in hue — one colour family — and **ΔE 24.6** apart in
appearance, which is plainly different side by side. Say it precisely: *one hue,
two calibrated values*, **not** "one colour". Across a theme switch a reader sees
the brand keeping its colour; that is the part that matters for an identity.

**The practical consequence:** use `--gru-accent` and let the theme choose.
Never hard-code either value into a component.

---

## The palette

### Signature — the three colours the brand is made of

| Name | Bangla | Value | Job |
|---|---|---|---|
| **Meridian** | মেরিডিয়ান | `#1A1753` | The deep sky. The ground, hero panels, the wordmark on light. Also the colour of *information*. |
| **Daybreak** | ভোরের আলো | `#B45A39` light / `#FFAB8E` dark | First light. The signature. |
| **Ember** | অঙ্গার | `#EDB24D` | Warm mid-tone. Gradient midpoint, secondary emphasis. Also the colour of a *warning*. |

**Two of the three do double duty, deliberately.** Ember is the warning colour;
Meridian is the information colour. Five hues is a palette and nine is a paint
shop, so the system reuses these rather than inventing more. Only Daybreak is
purely expressive.

### Functional — hues that exist only to carry a meaning

| Name | Bangla | Hue | Job |
|---|---|---|---|
| **Verdant** | সবুজ | 152° | The only hue that means "this worked". Never decorative. |
| **Signal Red** | লাল | 25° | The only hue that means "this failed, or cannot be undone". Never decorative. |

### Grounds

| Name | Bangla | Value |
|---|---|---|
| **Ink** | কালি | `#0B0E14` |
| **Paper** | কাগজ | `#FFFFFF` |

### The signature gradient — "first light"

`linear-gradient(112deg, #1A1753 0%, #343583 32%, #EDB24D 76%, #FFAB8E 100%)`

Four stops, not three: the second is Meridian's own step 800, which stops the
indigo jumping straight to gold across a hard seam.

**Hero artwork only.** Never behind body text. Never on the mark.

---

## Use the role tokens, not the ramps

The ramps exist so the roles can be derived from them. In interface code, reach
for a role. Reaching past it to `--gru-meridian-600` is how a system starts to
drift.

Every role below is defined in **both** themes, so a screen built from them is
correct in light and dark with no second stylesheet and no `@media` block of
your own.

| Group | Tokens |
|---|---|
| Ground and surfaces | `--gru-bg` `--gru-bg-subtle` `--gru-surface` `--gru-surface-raised` `--gru-surface-sunken` `--gru-overlay` |
| Text | `--gru-ink` `--gru-ink-muted` `--gru-ink-subtle` `--gru-ink-inverse` |
| Lines | `--gru-border` (decorative hairline) `--gru-border-strong` (must be seen: clears 3:1) |
| The brand | `--gru-brand` `--gru-brand-hover` `--gru-brand-active` `--gru-brand-quiet` `--gru-on-brand` |
| The signature | `--gru-accent` `--gru-accent-hover` `--gru-accent-active` `--gru-accent-quiet` `--gru-accent-ui` `--gru-on-accent` |
| Links | `--gru-link` `--gru-link-hover` `--gru-link-visited` |
| Focus and disabled | `--gru-focus` `--gru-focus-inverse` `--gru-disabled-bg` `--gru-disabled-ink` `--gru-disabled-border` |
| Meaning | `--gru-info` `--gru-success` `--gru-warning` `--gru-danger`, each with `-quiet` (a tinted background) and `-border` |
| Charts | `--gru-chart-1` … `--gru-chart-6` |

`--gru-border` is the one token deliberately **not** held to 3:1 — it is a
decorative hairline. When the line itself must be seen, use `--gru-border-strong`.

### The pattern that gets it right

```css
@import url("tokens.css");           /* or paste its contents in */

.card{
  background: var(--gru-surface-raised);
  color: var(--gru-ink);
  border: 1px solid var(--gru-border);
  border-radius: var(--gru-radius-lg);
  padding: var(--gru-space-5);
}
.card a{ color: var(--gru-link) }
.card .meta{ color: var(--gru-ink-subtle) }

.button-primary{
  background: var(--gru-accent);
  color: var(--gru-on-accent);
  border: 0;
}
.button-primary:hover{ background: var(--gru-accent-hover) }
.button-primary:active{ background: var(--gru-accent-active) }
.button-primary:focus-visible{ outline: 3px solid var(--gru-focus); outline-offset: 2px }
.button-primary[disabled]{
  background: var(--gru-disabled-bg);
  color: var(--gru-disabled-ink);
  border: 1px solid var(--gru-disabled-border);
}
```

Nothing above names a hex value, and nothing above needs a dark-theme
counterpart written by hand.

### How the theme is chosen

`tokens.css` ships three layers, and they compose:

1. The light roles on `:root` — the default.
2. `@media (prefers-color-scheme: dark)` on `:root:not([data-theme="light"])` —
   follows the reader's system setting.
3. `:root[data-theme="dark"]` — an explicit choice by the reader.

So: set nothing and the system decides; set `data-theme="light"` or
`data-theme="dark"` on `<html>` and that wins.

A `@media (forced-colors: active)` block hands control back to the operating
system for Windows High Contrast. Do not fight it — but do add
`forced-color-adjust: none` to any element whose *subject is colour itself*
(a swatch, a ramp, a chart bar), or the page becomes a list of hex codes with no
colours beside them.

---

## Approved pairings, and the two that are not

| Background | Foreground | Ratio | |
|---|---|---|---|
| Paper `#FFFFFF` | Meridian `#1A1753` | 16.26:1 | ✓ |
| Paper | Daybreak light `#B45A39` | 4.71:1 | ✓ |
| Paper | Ink `#0B0E14` | 19.32:1 | ✓ |
| Meridian `#1A1753` | Daybreak dark `#FFAB8E` | 8.88:1 | ✓ |
| Meridian | Paper `#FFFFFF` | 16.26:1 | ✓ |
| Ink `#0B0E14` | Daybreak dark `#FFAB8E` | 10.55:1 | ✓ |
| Meridian | Ember `#EDB24D` | 8.58:1 | ✓ |
| Ember | Ink | 10.19:1 | ✓ |
| **Paper** | **Daybreak dark `#FFAB8E`** | **1.83:1** | **✗ never** |
| **Meridian** | **Daybreak light `#B45A39`** | **3.46:1** | **✗ never** |

The first failure is the one people reach for by mistake, and it is exactly why
the signature has two values. On a light ground the correct Daybreak is
`#B45A39`.

---

## Distinctiveness, stated honestly

Contrast says a colour is legible. It says nothing about whether *success* can be
told apart from *warning*, or whether the brand looks like somebody else's.

**Internally**, no two meaning-bearing colours are within **ΔE 10** of each
other — the point at which any normally-sighted viewer would call two colours
different. That floor is enforced on every build.

**Externally**, against colours other developer brands already own:

| GRU953 colour | Closest three |
|---|---|
| Meridian `#1A1753` | Slack aubergine ΔE 12.5 · Heroku ΔE 13.1 · Notion ΔE 22.6 |
| Daybreak light `#B45A39` | sienna (the pigment) ΔE 5.4 · Rust ΔE 7.2 · Anthropic ΔE 11.3 |
| Daybreak dark `#FFAB8E` | Anthropic ΔE 13.8 · terracotta ΔE 14.3 · Figma ΔE 20.8 |
| Ember `#EDB24D` | Tailwind amber ΔE 6.4 · Mailchimp ΔE 15.8 |

**Daybreak's light value sits close to Rust's brand orange.** That is published
rather than hidden, and it was accepted for three reasons: the proximity is to a
*deep interface accent*, not to the brand's dominant colour; the chroma at the
deep end is deliberately tapered to pull away from the saturated rust-orange
region; and the value a reader sees most often is the pale one, which is ΔE 13.8
from its nearest neighbour.

**Meridian sits in a crowded region and the kit says so.** Deep indigo is owned
by many brands — which is exactly why it is treated as the *ground* rather than
the signature. The signature is Daybreak, the bird, and the pairing.

---

## Charts

Six series, spread around the wheel, anchored on the brand's own two: Meridian,
Daybreak, Kingfisher, Verdant, Orchid, Ember. Every one clears 3:1 against its
own theme's background, and no two are within ΔE 10.

Use `--gru-chart-1` through `--gru-chart-6`, in order — the first two series a
reader sees are then the brand's own colours.

**Colour is never the only carrier of meaning.** Every series also needs a label,
a shape, or a pattern. That, not the ΔE figure, is the actual protection for a
colour-blind reader.

---

## When you need a colour the palette does not have

Work down this list and stop at the first answer that works.

1. **Use a role token instead.** Nine times in ten the need is "a warning" or
   "a muted surface", and there is already a token for it.
2. **Group the data.** A chart needing a seventh series usually needs fewer
   series: group the tail into "other", or split it in two. Seven colours is
   where a reader stops distinguishing them anyway.
3. **Use a different step of a family already in the palette.** Each has eleven.
4. **Only then add a hue** — properly, in the palette engine, as a family with a
   stated meaning, so it is checked for legibility and distinctiveness before it
   ships. Never paste a hex code into a stylesheet to get past an afternoon.

---

## Checklist

- [ ] No literal hex value anywhere in component code.
- [ ] `--gru-accent` used, not one of its two values hard-coded.
- [ ] Every text colour clears 4.5:1 against its own background, **in both themes**.
- [ ] Every border or icon that must be seen clears 3:1, **in both themes**.
- [ ] Focus is visible on every interactive element, in both themes.
- [ ] Nothing relies on colour alone to carry meaning.
- [ ] Anything whose subject *is* colour carries `forced-color-adjust: none`.
- [ ] The gradient appears only in hero artwork, never behind text, never on the mark.
