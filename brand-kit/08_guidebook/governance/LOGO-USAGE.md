# Logo usage — the Soaring Bird and the GRU953 wordmark

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

Copyright © 2026 Aninda Sundar Howlader (GRU953)

The marks are not licensed. This page says what may be done with them anyway, so that
honest use never needs an email. `TRADEMARKS.md` is the governing policy; this is the
practical half of it.

*Plain-English note, written once: this was written by the kit's author, who is not a
lawyer. It is not legal advice.*

---

## 1. Without asking

- Show an unaltered logo where the subject **is** GRU953: a screenshot, a slide about the
  studio, a link card, a directory entry, a press mention.
- Use the logo as a link to GRU953's site or repositories.
- Scale it, as long as it stays above the minimum sizes in section 4.
- Pick any of the approved colour-on-background pairings in section 3. Not any colour on
  any background: some pairings are too faint to read and are not approved.

## 2. Not without written permission

- Any use where the logo stands for **you** or your product: your icon, avatar, header,
  packaging, app-store listing.
- Any use implying endorsement, partnership or affiliation.
- Any altered version. If you changed it, you needed permission.
- Merchandise or print goods.
- Keeping the logo on a fork of the kit.

Ask: **aninda.sh15@gmail.com**

---

## 3. The files, the colours, and which goes on what

### There is one bird

There is exactly one drawing of the Soaring Bird. There used to be three, built separately
for different sizes, and they drifted apart — the smallest one ended up with its wing cut
away from its body. One drawing cannot drift from itself, so one drawing is what ships.

| File | What it is | Use it |
|---|---|---|
| `03_logo/GRU953-bird.svg` | The mark alone | At 24px and above |
| `03_logo/GRU953-appicon.svg` | The same bird, in Daybreak on a Meridian tile, at the *squircle* radius — a rounded square, rounder than a normal button corner, which is the exact shape iOS and Android use for app icons | Below 24px, and anywhere a filled icon is expected |
| `03_logo/GRU953-lockup-horizontal.svg` | Bird beside the wordmark | The default for headers and banners |
| `03_logo/GRU953-lockup-horizontal-tagline.svg` | The same, with both taglines | Where there is room to say what GRU953 is |
| `03_logo/GRU953-lockup-stacked.svg` | Bird above the wordmark | Square and narrow spaces |
| `03_logo/GRU953-lockup-stacked-tagline.svg` | The same, with both taglines | Posters, covers, title cards |
| `03_logo/GRU953-wordmark.svg` | The wordmark alone | Where the bird would be too small to read |
| `03_logo/GRU953-tagline.svg` | Both taglines alone | As a footer or a sign-off |

Every one of these embeds the same bird path and the same outlined wordmark. Nothing in
the set can drift out of step with anything else.

### The approved colours

| Colour | Value | What it is for |
|---|---|---|
| **Meridian** | `#1A1753` | The mark on light grounds |
| **Daybreak** (dark grounds) | `#FFAB8E` | The mark on Meridian or Ink |
| **Daybreak** (light grounds) | `#B45A39` | The signature, when the mark must be warm on white |
| **Ink** | `#0B0E14` | Single-colour print, stamps, engraving |
| **Paper** | `#FFFFFF` | Reversed out of a dark ground |

No colour beyond these five is approved. The SVGs are drawn with `fill="currentColor"`, so
you set the colour yourself — in CSS, `color: #1A1753`.

**The tile is the exception: it has one colourway and is not recolourable.** Daybreak on
Meridian, always. There is no dark-on-light tile and none will be added — an icon that
changes colour stops being a recognisable object at the sizes the tile exists to serve. If a
surface needs some other colour, it is big enough for the bare bird, which is recolourable.

### Which colour on which background

Only these pairings are approved.

| Background | Mark colour | Contrast |
|---|---|---|
| Paper `#FFFFFF` | Meridian | 16.26:1 |
| Paper | Daybreak (light) `#B45A39` | 4.71:1 |
| Paper | Ink | 19.32:1 |
| Meridian `#1A1753` | Daybreak `#FFAB8E` | 8.88:1 |
| Meridian | Paper | 16.26:1 |
| Ink `#0B0E14` | Daybreak `#FFAB8E` | 10.55:1 |
| A photograph | Ink or Paper only | See section 6, item 6 |

**Daybreak `#FFAB8E` on Paper is not approved.** It measures 1.83:1 and the bird all but
disappears. This is the one pairing people reach for by mistake — and it is exactly why the
signature has two values. On a light ground, use `#B45A39`.

**Daybreak `#B45A39` on Meridian is not approved either.** At 3.46:1 it is legible but
muddy, and the pale value exists precisely for that ground.

Every figure comes from `04_colour/CONTRAST.md`, where it is computed rather than asserted.
A note on what they mean: WCAG's 4.5:1 threshold applies to text, and logos are explicitly
exempt from it. These numbers are quoted for legibility, not to claim the logo must pass a
standard.

---

## 4. Minimum sizes

| What | On screen | In print |
|---|---|---|
| Horizontal lockup | **120px** wide | **25mm** wide |
| Lockup with the tagline | **260px** wide | **55mm** wide |
| The bird alone | **24px** | **6mm** |
| The tile (`GRU953-appicon.svg`) | **16px** | — |

These are floors, not targets. If a layout can only give the lockup 90px, use the bird
alone rather than shrinking the lockup.

**Below 24px, use the tile, not the bare bird.** The bird's strokes are fine lines; below
24px they thin out and the wing's *counters* begin to close — counters being the small
enclosed gaps inside a shape, like the hole in an *o*. The tile carries recognition at
those sizes because a block of colour survives where a line drawing cannot. This is
checked mechanically every time the mark is generated — `03_logo/marks.py` refuses to write
the file if the counters have closed at 24px.

## 5. Clear space

Keep empty space on all four sides equal to **half the height of the bird**. For a 32px
mark, that is 16px of clear space. For a lockup, measure the bird, not the whole lockup.

Nothing goes inside that space: no text, no icons, no rules, no page edge, no other logo.
One number, four sides, and that is the whole rule.

On the web you can let CSS do it. Wrap the logo in the `gru-logo-safe` class from
`08_guidebook/assets/layout.css`. It adds the padding for you. One condition: it is only
correct when the logo's own height is set to `1em`. If you size the logo in pixels instead,
set the padding yourself.

---

## 6. The don'ts

Never:

1. **Stretch or squash it.** Scale both dimensions together, always.
2. **Rotate or tilt it.** The bird climbs; it does not lean.
3. **Animate it.** The mark is still. A logo that moves is a logo that can be caught
   mid-movement looking broken.
4. **Recolour it** outside the five approved colours. No gradients on the mark, no
   brand-adjacent near-misses, no your-client's-blue. The signature gradient is for hero
   art, never for the mark itself.
5. **Add effects** — drop shadows, glows, outlines, bevels, strokes, textures.
6. **Re-typeset the wordmark or the tagline.** Both are artwork, not live text. The Bangla
   in particular needs real text shaping; retyping it in a font will produce broken
   conjuncts. Use the supplied files.
7. **Place it on a busy photograph.** Put it on a plain area, or on a solid panel of
   Meridian, Ink or Paper.
8. **Combine it with another mark** — no lockups with someone else's logo, no
   "GRU953 × …", no enclosing it in a badge or shape that is not in the kit.

Also: do not rebuild a lockup by hand. The spacing between bird, wordmark and tagline is
part of the artwork. Use the supplied files.

---

*Questions and permissions: aninda.sh15@gmail.com*
