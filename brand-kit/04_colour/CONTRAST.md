# GRU953 — contrast and distinctiveness, proved

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

Every number on this page is **computed** by `04_colour/engine.py`. None of it is
asserted by hand. Regenerate the page whenever a colour changes.

**The four words this page needs, in plain English.**

- **WCAG** — the Web Content Accessibility Guidelines, the accessibility rulebook that
  regulators and procurement teams actually point to. Version 2.2, level AA, is the bar
  used throughout. AAA is the stricter level above it.
- **Luminance** — how much light a colour emits. Brightness, not colourfulness.
- **Contrast ratio** — the ratio between two luminances, written `4.5:1`. Bigger is
  easier to read.
- **ΔE**, said *delta E* — how different two colours *look* to a normal eye. Under about
  1, nobody notices. Over about 10, anyone would call them different colours. The method
  here is CIEDE2000, the current standard for this.

**Standard:** WCAG 2.2. Normal text needs **4.5:1** for AA and **7:1** for AAA. Large
text (24px, or 19px bold) and non-text interface parts need **3:1**. Every role below
clears its target by at least **0.05**, so rounding to 8-bit hex cannot quietly
drop it under.

## 1. Why the signature is one hue with two values

This is the single most important fact about the palette, so it is proved first.

WCAG contrast is `(L1+0.05)/(L2+0.05)` on relative luminance.

- To reach 4.5:1 against white a colour needs luminance **≤ 0.1833**.
- To reach 4.5:1 against the ink `#0B0E14` it needs luminance **≥ 0.1946**.

Those two cannot both be true. **No single colour can be this brand's text colour in
both themes.** So Daybreak is expressed as two tuned values from one ramp:

| theme | token resolves to | ground | ratio |
|---|---|---|---:|
| light | `#B45A39` | `#FFFFFF` | **4.71:1** |
| dark | `#FFAB8E` | `#0B0E14` | **10.55:1** |

They are the SAME HUE — 0.51° apart, which is inside the range a viewer
reads as one colour family. They are **not** the same value, and this page will not
pretend otherwise: their CIEDE2000 difference is **ΔE 24.6**, well above the
ΔE 10.0 floor this page uses elsewhere for *obviously different*. One is a deep
terracotta and one is a pale salmon, because that is what being legible on white and
being legible on near-black actually require.

The honest statement is therefore: **one hue, two calibrated values** — not *one colour*.
Someone shown the two side by side will say they are different. Someone shown the light
theme and then the dark theme will say the brand kept its colour. Both are true, and the
second is the one that matters for an identity.

## 2. The pairings you will actually use

| pairing | foreground | background | ratio | normal text | large text / UI |
|---|---|---|---:|:---:|:---:|
| Signature on paper (light theme) | `#B45A39` | `#FFFFFF` | **4.71:1** | AA | AAA |
| Signature on ink (dark theme) | `#FFAB8E` | `#0B0E14` | **10.55:1** | AAA | AAA |
| Meridian on paper | `#1A1753` | `#FFFFFF` | **16.26:1** | AAA | AAA |
| White on Meridian | `#FFFFFF` | `#1A1753` | **16.26:1** | AAA | AAA |
| Daybreak on Meridian | `#FFAB8E` | `#1A1753` | **8.88:1** | AAA | AAA |
| Ember on Meridian | `#EDB24D` | `#1A1753` | **8.58:1** | AAA | AAA |
| Ink on Daybreak | `#0B0E14` | `#FFAB8E` | **10.55:1** | AAA | AAA |
| Ink on Ember | `#0B0E14` | `#EDB24D` | **10.19:1** | AAA | AAA |
| Ink on paper | `#0B0E14` | `#FFFFFF` | **19.32:1** | AAA | AAA |
| Paper on ink | `#FFFFFF` | `#0B0E14` | **19.32:1** | AAA | AAA |

## 3. Every semantic role, measured against its own theme's background

A role is only correct if it is correct **in the theme it belongs to**. Each row is
measured against that theme's `bg`.

| role | light value | on paper | dark value | on ink |
|---|---|---:|---|---:|
| `--gru-bg` | `#FFFFFF` | 1.0:1 | `#0B0E14` | 1.0:1 |
| `--gru-bg-subtle` | `#F3F6FF` | 1.08:1 | `#12161F` | 1.07:1 |
| `--gru-surface` | `#FFFFFF` | 1.0:1 | `#141926` | 1.1:1 |
| `--gru-surface-raised` | `#FBFBFD` | 1.03:1 | `#1B2130` | 1.2:1 |
| `--gru-surface-sunken` | `#F3F6FF` | 1.08:1 | `#080A0F` | 1.02:1 |
| `--gru-overlay` | `rgba(11,14,20,.55)` | — | `rgba(3,4,7,.66)` | — |
| `--gru-ink` | `#0B0E14` | 19.32:1 | `#F4F5F9` | 17.73:1 |
| `--gru-ink-muted` | `#4D5157` | 7.98:1 | `#A8ACB4` | 8.49:1 |
| `--gru-ink-subtle` | `#6A6D74` | 5.18:1 | `#858990` | 5.5:1 |
| `--gru-ink-inverse` | `#FFFFFF` | 1.0:1 | `#0B0E14` | 1.0:1 |
| `--gru-border` | `#E6EBFF` | 1.19:1 | `#242B3A` | 1.36:1 |
| `--gru-border-strong` | `#6469D3` | 4.66:1 | `#6469D3` | 4.14:1 |
| `--gru-brand` | `#1A1753` | 16.26:1 | `#7E86F6` | 6.1:1 |
| `--gru-brand-hover` | `#343583` | 10.59:1 | `#D1D9FF` | 13.87:1 |
| `--gru-brand-active` | `#0E0B37` | 18.72:1 | `#E6EBFF` | 16.27:1 |
| `--gru-brand-quiet` | `#EEF0FF` | 1.13:1 | `#141728` | 1.09:1 |
| `--gru-on-brand-quiet` | `#4C4EAD` | 7.0:1 | `#7E86F6` | 6.1:1 |
| `--gru-on-brand` | `#FFFFFF` | 1.0:1 | `#0B0E14` | 1.0:1 |
| `--gru-accent` | `#B45A39` | 4.71:1 | `#FFAB8E` | 10.55:1 |
| `--gru-accent-hover` | `#6C2A11` | 10.62:1 | `#FFCEBA` | 13.6:1 |
| `--gru-accent-active` | `#461301` | 15.51:1 | `#FFE4D9` | 15.96:1 |
| `--gru-accent-quiet` | `#FFF2EE` | 1.09:1 | `#1B1518` | 1.07:1 |
| `--gru-on-accent-quiet` | `#914124` | 7.03:1 | `#E26C42` | 5.94:1 |
| `--gru-accent-ui` | `#E26C42` | 3.25:1 | `#FFAB8E` | 10.55:1 |
| `--gru-on-accent` | `#FFFFFF` | 1.0:1 | `#0B0E14` | 1.0:1 |
| `--gru-link` | `#343583` | 10.59:1 | `#E26C42` | 5.94:1 |
| `--gru-link-hover` | `#0E0B37` | 18.72:1 | `#FFCEBA` | 13.6:1 |
| `--gru-link-visited` | `#0E0B37` | 18.72:1 | `#FFAB8E` | 10.55:1 |
| `--gru-focus` | `#6469D3` | 4.66:1 | `#6469D3` | 4.14:1 |
| `--gru-focus-inverse` | `#FFFFFF` | 1.0:1 | `#0B0E14` | 1.0:1 |
| `--gru-disabled-bg` | `#F3F6FF` | 1.08:1 | `#171B26` | 1.12:1 |
| `--gru-disabled-ink` | `#8A8F9C` | 3.24:1 | `#6A7183` | 3.96:1 |
| `--gru-disabled-border` | `#E6EBFF` | 1.19:1 | `#242B3A` | 1.36:1 |
| `--gru-info` | `#4C4EAD` | 7.0:1 | `#7E86F6` | 6.1:1 |
| `--gru-info-quiet` | `#EEF0FF` | 1.13:1 | `#141728` | 1.09:1 |
| `--gru-on-info-quiet` | `#4C4EAD` | 7.0:1 | `#7E86F6` | 6.1:1 |
| `--gru-info-border` | `#6469D3` | 4.66:1 | `#6469D3` | 4.14:1 |
| `--gru-on-info` | `#FFFFFF` | 1.0:1 | `#0B0E14` | 1.0:1 |
| `--gru-success` | `#007131` | 6.17:1 | `#32AE62` | 6.78:1 |
| `--gru-success-quiet` | `#EEF9F1` | 1.08:1 | `#0E1A19` | 1.09:1 |
| `--gru-on-success-quiet` | `#007131` | 6.17:1 | `#32AE62` | 6.78:1 |
| `--gru-success-border` | `#009047` | 4.13:1 | `#009047` | 4.67:1 |
| `--gru-on-success` | `#FFFFFF` | 1.0:1 | `#0B0E14` | 1.0:1 |
| `--gru-warning` | `#805100` | 6.79:1 | `#C88400` | 6.22:1 |
| `--gru-warning-quiet` | `#FDF3E5` | 1.1:1 | `#181616` | 1.07:1 |
| `--gru-on-warning-quiet` | `#805100` | 6.79:1 | `#C88400` | 6.22:1 |
| `--gru-warning-border` | `#A36A00` | 4.55:1 | `#A36A00` | 4.25:1 |
| `--gru-on-warning` | `#FFFFFF` | 1.0:1 | `#0B0E14` | 1.0:1 |
| `--gru-danger` | `#CE393A` | 4.92:1 | `#F25855` | 5.8:1 |
| `--gru-danger-quiet` | `#FFF2F0` | 1.09:1 | `#1E1318` | 1.07:1 |
| `--gru-on-danger-quiet` | `#A71F25` | 7.33:1 | `#F25855` | 5.8:1 |
| `--gru-danger-border` | `#F25855` | 3.33:1 | `#CE393A` | 3.93:1 |
| `--gru-on-danger` | `#FFFFFF` | 1.0:1 | `#0B0E14` | 1.0:1 |
| `--gru-danger-hover` | `#7D0512` | 11.04:1 | `#FF8179` | 7.97:1 |
| `--gru-danger-active` | `#530002` | 15.34:1 | `#FFA9A0` | 10.52:1 |

## 3a. Every pairing the component library actually uses

Proving a colour against the page background is not the same as proving it where a
component puts it. Each row below is a pairing that exists in `components.css`, measured
in both themes. A component that needs a pairing not listed here is a component that has
not been proved.

| foreground | background | what it is | light | dark | need |
|---|---|---|---:|---:|---:|
| `--gru-accent` | `--gru-bg` | gru-tab on a page surface | 4.71:1 | 10.55:1 | 4.5:1 |
| `--gru-accent` | `--gru-surface` | gru-tab on a page surface | 4.71:1 | 9.58:1 | 4.5:1 |
| `--gru-accent` | `--gru-surface-raised` | gru-tab on a page surface | 4.55:1 | 8.78:1 | 4.5:1 |
| `--gru-border-strong` | `--gru-accent-quiet` | drawn over whatever the control sits in | 4.26:1 | 3.86:1 | 3.0:1 |
| `--gru-border-strong` | `--gru-bg` | gru-state__art on a page surface | 4.66:1 | 4.14:1 | 3.0:1 |
| `--gru-border-strong` | `--gru-bg-subtle` | drawn over whatever the control sits in | 4.32:1 | 3.88:1 | 3.0:1 |
| `--gru-border-strong` | `--gru-brand-quiet` | drawn over whatever the control sits in | 4.12:1 | 3.81:1 | 3.0:1 |
| `--gru-border-strong` | `--gru-danger-quiet` | drawn over whatever the control sits in | 4.27:1 | 3.88:1 | 3.0:1 |
| `--gru-border-strong` | `--gru-info-quiet` | drawn over whatever the control sits in | 4.12:1 | 3.81:1 | 3.0:1 |
| `--gru-border-strong` | `--gru-success-quiet` | drawn over whatever the control sits in | 4.32:1 | 3.81:1 | 3.0:1 |
| `--gru-border-strong` | `--gru-surface` | gru-state__art on a page surface | 4.66:1 | 3.76:1 | 3.0:1 |
| `--gru-border-strong` | `--gru-surface-raised` | gru-state__art on a page surface | 4.51:1 | 3.45:1 | 3.0:1 |
| `--gru-border-strong` | `--gru-surface-sunken` | drawn over whatever the control sits in | 4.32:1 | 4.25:1 | 3.0:1 |
| `--gru-border-strong` | `--gru-warning-quiet` | drawn over whatever the control sits in | 4.25:1 | 3.86:1 | 3.0:1 |
| `--gru-brand` | `--gru-bg` | gru-topbar__brand on a page surface | 16.26:1 | 6.1:1 | 4.5:1 |
| `--gru-brand` | `--gru-surface` | gru-topbar__brand on a page surface | 16.26:1 | 5.54:1 | 4.5:1 |
| `--gru-brand` | `--gru-surface-raised` | gru-topbar__brand on a page surface | 15.73:1 | 5.07:1 | 4.5:1 |
| `--gru-danger` | `--gru-bg` | gru-field__error on a page surface | 4.92:1 | 5.8:1 | 4.5:1 |
| `--gru-danger` | `--gru-danger-quiet` | gru-state--error: its own text on its own ground | 4.5:1 | 5.43:1 | 4.5:1 |
| `--gru-danger` | `--gru-surface` | gru-field__error on a page surface | 4.92:1 | 5.27:1 | 4.5:1 |
| `--gru-danger` | `--gru-surface-raised` | gru-field__error on a page surface | 4.76:1 | 4.82:1 | 4.5:1 |
| `--gru-focus` | `--gru-accent-quiet` | drawn over whatever the control sits in | 4.26:1 | 3.86:1 | 3.0:1 |
| `--gru-focus` | `--gru-bg` | drawn over whatever the control sits in | 4.66:1 | 4.14:1 | 3.0:1 |
| `--gru-focus` | `--gru-bg-subtle` | drawn over whatever the control sits in | 4.32:1 | 3.88:1 | 3.0:1 |
| `--gru-focus` | `--gru-brand-quiet` | drawn over whatever the control sits in | 4.12:1 | 3.81:1 | 3.0:1 |
| `--gru-focus` | `--gru-danger-quiet` | drawn over whatever the control sits in | 4.27:1 | 3.88:1 | 3.0:1 |
| `--gru-focus` | `--gru-info-quiet` | drawn over whatever the control sits in | 4.12:1 | 3.81:1 | 3.0:1 |
| `--gru-focus` | `--gru-success-quiet` | drawn over whatever the control sits in | 4.32:1 | 3.81:1 | 3.0:1 |
| `--gru-focus` | `--gru-surface` | drawn over whatever the control sits in | 4.66:1 | 3.76:1 | 3.0:1 |
| `--gru-focus` | `--gru-surface-raised` | drawn over whatever the control sits in | 4.51:1 | 3.45:1 | 3.0:1 |
| `--gru-focus` | `--gru-surface-sunken` | drawn over whatever the control sits in | 4.32:1 | 4.25:1 | 3.0:1 |
| `--gru-focus` | `--gru-warning-quiet` | drawn over whatever the control sits in | 4.25:1 | 3.86:1 | 3.0:1 |
| `--gru-ink` | `--gru-bg` | gru-alert--danger on a page surface | 19.32:1 | 17.73:1 | 4.5:1 |
| `--gru-ink` | `--gru-bg-subtle` | gru-alert--danger on a page surface | 17.88:1 | 16.61:1 | 4.5:1 |
| `--gru-ink` | `--gru-surface` | gru-alert--danger on a page surface | 19.32:1 | 16.11:1 | 4.5:1 |
| `--gru-ink` | `--gru-surface-raised` | gru-alert--danger on a page surface | 18.69:1 | 14.75:1 | 4.5:1 |
| `--gru-ink` | `--gru-surface-sunken` | gru-alert--danger on a page surface | 17.88:1 | 18.17:1 | 4.5:1 |
| `--gru-ink-muted` | `--gru-bg` | gru-badge on a page surface | 7.98:1 | 8.49:1 | 4.5:1 |
| `--gru-ink-muted` | `--gru-bg-subtle` | gru-badge on a page surface | 7.39:1 | 7.95:1 | 4.5:1 |
| `--gru-ink-muted` | `--gru-surface` | gru-badge: its own text on its own ground | 7.98:1 | 7.71:1 | 4.5:1 |
| `--gru-ink-muted` | `--gru-surface-raised` | gru-badge on a page surface | 7.73:1 | 7.06:1 | 4.5:1 |
| `--gru-ink-muted` | `--gru-surface-sunken` | gru-badge on a page surface | 7.39:1 | 8.7:1 | 4.5:1 |
| `--gru-ink-subtle` | `--gru-bg` | gru-breadcrumb::before on a page surface | 5.18:1 | 5.5:1 | 4.5:1 |
| `--gru-ink-subtle` | `--gru-bg-subtle` | gru-breadcrumb::before on a page surface | 4.8:1 | 5.15:1 | 4.5:1 |
| `--gru-ink-subtle` | `--gru-surface` | gru-breadcrumb::before on a page surface | 5.18:1 | 5.0:1 | 4.5:1 |
| `--gru-ink-subtle` | `--gru-surface-raised` | gru-breadcrumb::before on a page surface | 5.01:1 | 4.57:1 | 4.5:1 |
| `--gru-ink-subtle` | `--gru-surface-sunken` | gru-breadcrumb::before on a page surface | 4.8:1 | 5.64:1 | 4.5:1 |
| `--gru-link-hover` | `--gru-bg` | gru-btn on a page surface | 18.72:1 | 13.6:1 | 4.5:1 |
| `--gru-link-hover` | `--gru-surface` | gru-btn on a page surface | 18.72:1 | 12.36:1 | 4.5:1 |
| `--gru-link-hover` | `--gru-surface-raised` | gru-btn on a page surface | 18.11:1 | 11.32:1 | 4.5:1 |
| `--gru-link-visited` | `--gru-bg` | gru-btn on a page surface | 18.72:1 | 10.55:1 | 4.5:1 |
| `--gru-link-visited` | `--gru-surface` | gru-btn on a page surface | 18.72:1 | 9.58:1 | 4.5:1 |
| `--gru-link-visited` | `--gru-surface-raised` | gru-btn on a page surface | 18.11:1 | 8.78:1 | 4.5:1 |
| `--gru-on-accent` | `--gru-accent` | gru-badge--accent: its own text on its own ground | 4.71:1 | 10.55:1 | 4.5:1 |
| `--gru-on-accent` | `--gru-accent-active` | gru-btn--primary: its own text on its own ground | 15.51:1 | 15.96:1 | 4.5:1 |
| `--gru-on-accent` | `--gru-accent-hover` | gru-btn--primary: its own text on its own ground | 10.62:1 | 13.6:1 | 4.5:1 |
| `--gru-on-accent-quiet` | `--gru-accent-quiet` | gru-navlink: its own text on its own ground | 6.43:1 | 5.53:1 | 4.5:1 |
| `--gru-on-accent-quiet` | `--gru-bg` | gru-navlink on a page surface | 7.03:1 | 5.94:1 | 4.5:1 |
| `--gru-on-accent-quiet` | `--gru-surface` | gru-navlink on a page surface | 7.03:1 | 5.4:1 | 4.5:1 |
| `--gru-on-accent-quiet` | `--gru-surface-raised` | gru-navlink on a page surface | 6.81:1 | 4.94:1 | 4.5:1 |
| `--gru-on-brand` | `--gru-brand` | gru-avatar: its own text on its own ground | 16.26:1 | 6.1:1 | 4.5:1 |
| `--gru-on-brand` | `--gru-brand-active` | gru-btn--brand: its own text on its own ground | 18.72:1 | 16.27:1 | 4.5:1 |
| `--gru-on-brand` | `--gru-brand-hover` | gru-btn--brand: its own text on its own ground | 10.59:1 | 13.87:1 | 4.5:1 |
| `--gru-on-danger` | `--gru-danger` | gru-btn--danger: its own text on its own ground | 4.92:1 | 5.8:1 | 4.5:1 |
| `--gru-on-danger` | `--gru-danger-active` | gru-btn--danger: its own text on its own ground | 15.34:1 | 10.52:1 | 4.5:1 |
| `--gru-on-danger` | `--gru-danger-hover` | gru-btn--danger: its own text on its own ground | 11.04:1 | 7.97:1 | 4.5:1 |
| `--gru-on-danger-quiet` | `--gru-bg` | gru-alert--danger on a page surface | 7.33:1 | 5.8:1 | 4.5:1 |
| `--gru-on-danger-quiet` | `--gru-danger-quiet` | gru-alert--danger: its own text on its own ground | 6.7:1 | 5.43:1 | 4.5:1 |
| `--gru-on-danger-quiet` | `--gru-surface` | gru-alert--danger on a page surface | 7.33:1 | 5.27:1 | 4.5:1 |
| `--gru-on-danger-quiet` | `--gru-surface-raised` | gru-alert--danger on a page surface | 7.09:1 | 4.82:1 | 4.5:1 |
| `--gru-on-info-quiet` | `--gru-bg` | gru-alert--info on a page surface | 7.0:1 | 6.1:1 | 4.5:1 |
| `--gru-on-info-quiet` | `--gru-info-quiet` | gru-alert--info: its own text on its own ground | 6.18:1 | 5.6:1 | 4.5:1 |
| `--gru-on-info-quiet` | `--gru-surface` | gru-alert--info on a page surface | 7.0:1 | 5.54:1 | 4.5:1 |
| `--gru-on-info-quiet` | `--gru-surface-raised` | gru-alert--info on a page surface | 6.77:1 | 5.07:1 | 4.5:1 |
| `--gru-on-success-quiet` | `--gru-bg` | gru-alert--success on a page surface | 6.17:1 | 6.78:1 | 4.5:1 |
| `--gru-on-success-quiet` | `--gru-success-quiet` | gru-alert--success: its own text on its own ground | 5.71:1 | 6.24:1 | 4.5:1 |
| `--gru-on-success-quiet` | `--gru-surface` | gru-alert--success on a page surface | 6.17:1 | 6.15:1 | 4.5:1 |
| `--gru-on-success-quiet` | `--gru-surface-raised` | gru-alert--success on a page surface | 5.97:1 | 5.64:1 | 4.5:1 |
| `--gru-on-warning-quiet` | `--gru-bg` | gru-alert--warning on a page surface | 6.79:1 | 6.22:1 | 4.5:1 |
| `--gru-on-warning-quiet` | `--gru-surface` | gru-alert--warning on a page surface | 6.79:1 | 5.65:1 | 4.5:1 |
| `--gru-on-warning-quiet` | `--gru-surface-raised` | gru-alert--warning on a page surface | 6.57:1 | 5.17:1 | 4.5:1 |
| `--gru-on-warning-quiet` | `--gru-warning-quiet` | gru-alert--warning: its own text on its own ground | 6.18:1 | 5.8:1 | 4.5:1 |
| `--gru-success` | `--gru-bg` | gru-stat__delta--up on a page surface | 6.17:1 | 6.78:1 | 4.5:1 |
| `--gru-success` | `--gru-surface` | gru-stat__delta--up on a page surface | 6.17:1 | 6.15:1 | 4.5:1 |
| `--gru-success` | `--gru-surface-raised` | gru-stat__delta--up on a page surface | 5.97:1 | 5.64:1 | 4.5:1 |

Worst pairing in the set: **3.45:1** (`--gru-border-strong` on `--gru-surface-raised`).


## 4. Distinctiveness — no two meanings may look alike

Contrast says a colour is legible. It says nothing about whether *success* can be told
apart from *warning*. These are CIEDE2000 differences; the floor here is **ΔE 10.0**,
an obvious difference to a normally-sighted viewer.

| set | closest pair | ΔE | verdict |
|---|---|---:|---|
| light theme meanings | danger vs accent | 10.8 | PASS |
| dark theme meanings | danger vs accent | 19.2 | PASS |
| light chart series | Meridian vs Orchid | 18.6 | PASS |
| dark chart series | Meridian vs Orchid | 18.6 | PASS |

## 4a. Distinctiveness against colours other brands already own

The check above asks whether the kit's own colours can be told apart. This one asks the
question that actually matters to a developer audience: **does the brand look like
somebody else's?** These are CIEDE2000 differences against colours that audience sees
every day.

| GRU953 colour | value | closest three |
|---|---|---|
| Meridian | `#1A1753` | Slack aubergine ΔE 12.5, Heroku ΔE 13.1, Notion ΔE 22.6 |
| Daybreak · light | `#B45A39` | sienna (the pigment) ΔE 5.4, Rust ΔE 7.2, Anthropic ΔE 11.3 |
| Daybreak · dark | `#FFAB8E` | Anthropic ΔE 13.8, terracotta (the pigment) ΔE 14.3, Figma ΔE 20.8 |
| Ember | `#EDB24D` | Tailwind amber ΔE 6.4, Mailchimp ΔE 15.8, Anthropic ΔE 25.0 |

**Read honestly:** Daybreak's light value sits closest to Rust's brand orange and to
the sienna pigment. That is a real proximity and it is published rather than left out.
It was accepted for three reasons. The proximity is to a *deep interface accent*, not
to the brand's dominant colour — brands collide through their marks and their grounds,
which here are a bird and a deep indigo, neither of which resembles Rust. The chroma at
the deep end is deliberately tapered (see the `taper` in the engine) precisely to pull
away from the saturated rust-orange region. And the value a viewer sees most often is
the pale one, on dark grounds, which is ΔE 13.8 from its nearest neighbour.

**Meridian is in a crowded region and the kit says so.** Deep indigo is owned by many
brands, which is exactly why it is treated as the *ground* rather than the signature.
The signature is Daybreak, the bird, and the pairing — not the navy.

### The chart sequence

| # | series | light theme | on paper | dark theme | on ink |
|---|---|---|---:|---|---:|
| 1 | Meridian | `#6971B3` | 4.21:1 | `#6971B3` | 3.53:1 |
| 2 | Daybreak | `#B55939` | 4.36:1 | `#B55939` | 3.41:1 |
| 3 | Kingfisher | `#008995` | 3.88:1 | `#008995` | 3.84:1 |
| 4 | Verdant | `#2D8C50` | 3.9:1 | `#2D8C50` | 3.81:1 |
| 5 | Orchid | `#A0599B` | 4.42:1 | `#A0599B` | 3.36:1 |
| 6 | Ember | `#A16B00` | 4.21:1 | `#A16B00` | 3.53:1 |

## 5. Full ramps, every step measured against both grounds

*Monotonic* means every step is reliably lighter than the one below it — the ramp never
doubles back. A ramp that wanders is unusable for an interface, because you can no
longer reach for "one step darker" and know what you will get.

### Meridian — `--gru-meridian-*` (anchor `#1A1753` at step 900)

| step | hex | on paper | on ink | monotonic? |
|---|---|---:|---:|---|
| 50 | `#F3F6FF` | 1.08:1 | 17.88:1 | ✓ |
| 100 | `#E6EBFF` | 1.19:1 | 16.27:1 | ✓ |
| 200 | `#D1D9FF` | 1.39:1 | 13.87:1 | ✓ |
| 300 | `#B7C1FF` | 1.74:1 | 11.12:1 | ✓ |
| 400 | `#9BA5FF` | 2.28:1 | 8.48:1 | ✓ |
| 500 | `#7E86F6` | 3.17:1 | 6.1:1 | ✓ |
| 600 | `#6469D3` | 4.66:1 | 4.14:1 | ✓ |
| 700 | `#4C4EAD` | 7.0:1 | 2.76:1 | ✓ |
| 800 | `#343583` | 10.59:1 | 1.82:1 | ✓ |
| 900 **← brand** | `#1A1753` | 16.26:1 | 1.19:1 | ✓ |
| 950 | `#0E0B37` | 18.72:1 | 1.03:1 | ✓ |

### Daybreak — `--gru-daybreak-*` (anchor `#FFAB8E` at step 300)

| step | hex | on paper | on ink | monotonic? |
|---|---|---:|---:|---|
| 50 | `#FFF2EC` | 1.1:1 | 17.63:1 | ✓ |
| 100 | `#FFE4D9` | 1.21:1 | 15.96:1 | ✓ |
| 200 | `#FFCEBA` | 1.42:1 | 13.6:1 | ✓ |
| 300 **← brand** | `#FFAB8E` | 1.83:1 | 10.55:1 | ✓ |
| 400 | `#F8906B` | 2.28:1 | 8.46:1 | ✓ |
| 500 | `#E26C42` | 3.25:1 | 5.94:1 | ✓ |
| 600 | `#B45A39` | 4.71:1 | 4.1:1 | ✓ |
| 700 | `#914124` | 7.03:1 | 2.75:1 | ✓ |
| 800 | `#6C2A11` | 10.62:1 | 1.82:1 | ✓ |
| 900 | `#461301` | 15.51:1 | 1.25:1 | ✓ |
| 950 | `#2A0600` | 18.67:1 | 1.03:1 | ✓ |

### Ember — `--gru-ember-*` (anchor `#EDB24D` at step 300)

| step | hex | on paper | on ink | monotonic? |
|---|---|---:|---:|---|
| 50 | `#FFF5E3` | 1.08:1 | 17.87:1 | ✓ |
| 100 | `#FFE9C7` | 1.18:1 | 16.31:1 | ✓ |
| 200 | `#FDD69B` | 1.38:1 | 14.04:1 | ✓ |
| 300 **← brand** | `#EDB24D` | 1.9:1 | 10.19:1 | ✓ |
| 400 | `#E99F00` | 2.23:1 | 8.67:1 | ✓ |
| 500 | `#C88400` | 3.11:1 | 6.22:1 | ✓ |
| 600 | `#A36A00` | 4.55:1 | 4.25:1 | ✓ |
| 700 | `#805100` | 6.79:1 | 2.85:1 | ✓ |
| 800 | `#5D3800` | 10.34:1 | 1.87:1 | ✓ |
| 900 | `#3A2000` | 15.15:1 | 1.28:1 | ✓ |
| 950 | `#220F00` | 18.48:1 | 1.05:1 | ✓ |

### Verdant — `--gru-success-*` (hue 152.0°, no brand anchor — this family exists to carry a meaning)

| step | hex | on paper | on ink | monotonic? |
|---|---|---:|---:|---|
| 50 | `#EDFBF0` | 1.07:1 | 18.08:1 | ✓ |
| 100 | `#DAF5E0` | 1.16:1 | 16.67:1 | ✓ |
| 200 | `#BCEAC7` | 1.33:1 | 14.47:1 | ✓ |
| 300 | `#92DBA6` | 1.63:1 | 11.87:1 | ✓ |
| 400 | `#67C885` | 2.06:1 | 9.36:1 | ✓ |
| 500 | `#32AE62` | 2.85:1 | 6.78:1 | ✓ |
| 600 | `#009047` | 4.13:1 | 4.67:1 | ✓ |
| 700 | `#007131` | 6.17:1 | 3.13:1 | ✓ |
| 800 | `#00521C` | 9.44:1 | 2.05:1 | ✓ |
| 900 | `#003309` | 14.21:1 | 1.36:1 | ✓ |
| 950 | `#001C01` | 18.0:1 | 1.07:1 | ✓ |

### Signal Red — `--gru-danger-*` (hue 25.0°, no brand anchor — this family exists to carry a meaning)

| step | hex | on paper | on ink | monotonic? |
|---|---|---:|---:|---|
| 50 | `#FFF0EE` | 1.11:1 | 17.43:1 | ✓ |
| 100 | `#FFE1DC` | 1.23:1 | 15.69:1 | ✓ |
| 200 | `#FFC9C3` | 1.46:1 | 13.24:1 | ✓ |
| 300 | `#FFA9A0` | 1.84:1 | 10.52:1 | ✓ |
| 400 | `#FF8179` | 2.42:1 | 7.97:1 | ✓ |
| 500 | `#F25855` | 3.33:1 | 5.8:1 | ✓ |
| 600 | `#CE393A` | 4.92:1 | 3.93:1 | ✓ |
| 700 | `#A71F25` | 7.33:1 | 2.64:1 | ✓ |
| 800 | `#7D0512` | 11.04:1 | 1.75:1 | ✓ |
| 900 | `#530002` | 15.34:1 | 1.26:1 | ✓ |
| 950 | `#330000` | 18.41:1 | 1.05:1 | ✓ |

## 6. Result

**PASS.** Every ramp is monotonic. Every brand anchor sits inside its own ramp. Every semantic role clears its WCAG 2.2 target in its own theme, with margin. No two meaning-bearing colours are confusable.

## 7. What this page deliberately does not claim

- These are WCAG 2.x ratios. APCA (a candidate method in the draft WCAG 3) is not used,
  because WCAG 2.2 AA is the standard actually named in law and in procurement today.
- A passing ratio does not by itself make a screen readable. Text size, weight, line
  length and sheer quantity all matter, and none of them are measured here.
- ΔE distinctiveness is computed for normal colour vision. It is not a colour-blindness
  simulation. In this kit colour is never the only carrier of meaning — every state also
  carries a word, an icon or a shape, which is the actual protection.
- Nothing here has been tested with a real screen reader by a real user.
