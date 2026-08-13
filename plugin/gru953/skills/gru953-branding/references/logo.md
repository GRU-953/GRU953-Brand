# GRU953 — the mark

The Soaring Bird is Aninda's own drawing. What ships is that drawing — the
master path, unmodified. Nothing is re-traced, thickened or simplified.

---

## There is one bird

There were once three size-graded builds. They were three separate
constructions, they drifted apart, and the smallest ended up with its wing
severed from its body. **One drawing cannot drift from itself**, so one drawing
is what ships.

| File | What it is | Use it |
|---|---|---|
| `GRU953-bird.svg` | The mark alone | **24px and above** |
| `GRU953-appicon.svg` | The same bird in Daybreak on a Meridian tile | **Below 24px**, and anywhere a filled icon is expected |
| `GRU953-lockup-horizontal.svg` | Bird beside the wordmark | The default for headers and banners |
| `GRU953-lockup-horizontal-tagline.svg` | The same, with both taglines | Where there is room to say what GRU953 is |
| `GRU953-lockup-stacked.svg` | Bird above the wordmark | Square and narrow spaces |
| `GRU953-lockup-stacked-tagline.svg` | The same, with both taglines | Posters, covers, title cards |
| `GRU953-wordmark.svg` | The wordmark alone | Where the bird would be too small to read |
| `GRU953-tagline.svg` | Both taglines alone | A footer or a sign-off |

They are in `assets/marks/`. Every one embeds the same bird path and the same
outlined wordmark, so nothing in the set can drift out of step.

## Below 24px, use the tile — not a smaller bird

The bird is drawn in fine lines. Below 24px those lines thin out and the wing's
*counters* — the small enclosed gaps inside a shape, like the hole in an *o* —
begin to close. The honest answer is not a thinner bird but a different object:
a block of colour survives where a line drawing cannot.

This is not an opinion. The mark's generator rasterises it, finds the eight
enclosed counters at 512px, and checks each one is still open at 24px. If any
has silted up, the file is not written. At 16px only six of the eight survive —
which is precisely why the tile exists.

---

## Colour

The SVGs are drawn with `fill="currentColor"`. **Set `color`, not `fill`.**

```html
<div style="color: var(--gru-brand)"> <!-- the mark inherits this --> </div>
```

Setting `fill` on a parent does nothing: the child path's own `fill` wins, and
the bird renders black. This has caught people before.

| Colour | Value | For |
|---|---|---|
| Meridian | `#1A1753` | The mark on light grounds |
| Daybreak, dark grounds | `#FFAB8E` | The mark on Meridian or Ink |
| Daybreak, light grounds | `#B45A39` | When the mark must be warm on white |
| Ink | `#0B0E14` | Single-colour print, stamps, engraving |
| Paper | `#FFFFFF` | Reversed out of a dark ground |

**No sixth colour is approved.**

### Which colour on which ground

| Ground | Mark | Ratio | |
|---|---|---|---|
| Paper `#FFFFFF` | Meridian | 16.26:1 | ✓ |
| Paper | Daybreak light `#B45A39` | 4.71:1 | ✓ |
| Paper | Ink | 19.32:1 | ✓ |
| Meridian `#1A1753` | Daybreak `#FFAB8E` | 8.88:1 | ✓ |
| Meridian | Paper | 16.26:1 | ✓ |
| Ink `#0B0E14` | Daybreak `#FFAB8E` | 10.55:1 | ✓ |
| A photograph | Ink or Paper only | — | ✓ |
| **Paper** | **Daybreak `#FFAB8E`** | **1.83:1** | **✗** |
| **Meridian** | **Daybreak `#B45A39`** | **3.46:1** | **✗** |

A note on what those numbers mean: WCAG's 4.5:1 threshold applies to *text*, and
logos are explicitly exempt from it. They are quoted here for legibility, not to
claim the logo must pass a standard.

### The tile is the one exception

`GRU953-appicon.svg` has **one colourway** — Daybreak on Meridian — and is **not
recolourable**. There is no dark-on-light tile and none will be added: an icon
that changes colour stops being a recognisable object at the sizes the tile
exists to serve. If a surface needs another colour, it is large enough for the
bare bird, which *is* recolourable.

---

## Minimum sizes

| What | On screen | In print |
|---|---|---|
| Horizontal lockup | **120px** wide | **25mm** |
| Lockup with the tagline | **260px** wide | **55mm** |
| The bird alone | **24px** | **6mm** |
| The tile | **16px** | — |

Floors, not targets. If a layout can only give the lockup 90px, use the bird
alone rather than shrinking the lockup. Below 16px, use no mark at all.

## Clear space

**Half the bird's own height, on all four sides.** A 64px bird needs 32px of
clear space. For a lockup, measure the *bird*, not the whole lockup.

Nothing enters that space: no text, no rule, no border, no page edge, no second
logo, no button. One number, four sides, and that is the whole rule.

On the web, `.gru-logo-safe` in `assets/layout.css` does it for you — correct
only when the logo's own height is set to `1em`.

---

## The mark does not move

No animation, no transition, no hover state on the bird itself. A mark that
moves can be caught mid-movement looking broken — in a screenshot, in a
thumbnail, on a slow connection. Everything else may animate; the bird does not.

This has been asked for and refused once already.

## The other nine don'ts

1. **Stretch or squash it.** Scale both dimensions together, always.
2. **Rotate or tilt it.** The bird climbs; it does not lean.
3. **Recolour it** outside the five. No gradients on the mark, no
   brand-adjacent near-misses. The signature gradient is for hero art only.
4. **Add effects** — shadows, glows, outlines, bevels, strokes, textures.
5. **Re-typeset the wordmark or the tagline.** Both are artwork, not live text.
   The Bangla in particular needs real shaping; retyping it in a font produces
   broken conjuncts.
6. **Put it on a busy photograph.** Use a plain area, or a solid panel.
7. **Combine it with another mark.** No "GRU953 × …", no badge or shape that is
   not in the kit.
8. **Rebuild a lockup by hand.** The spacing between bird, wordmark and tagline
   is part of the artwork. Use the supplied file.
9. **Use it as your own identity.** The marks are not licensed. See
   `references/licence.md`.

---

## Accessibility

Every mark ships with a `<title>` and a `<desc>`, referenced by
`aria-labelledby` on the root. **Do not strip them, and do not let an SVG
optimiser rename their ids** — six lockups once shipped with `aria-labelledby`
pointing at ids that no longer existed, which is worse than no label at all,
because the file still looks correct in source.

When the mark is decorative and its meaning is already carried by nearby text,
mark it `aria-hidden="true"` instead. Do not do both.

---

## Checklist

- [ ] Right file for the size — the bird at 24px+, the tile below.
- [ ] An approved colour-on-ground pairing.
- [ ] Colour set with `color:`, not `fill:`.
- [ ] Clear space of half the bird's height on all four sides.
- [ ] Not stretched, rotated, recoloured outside the five, or animated.
- [ ] The wordmark and tagline are the supplied artwork, not retyped text.
- [ ] `<title>` and `<desc>` intact, or `aria-hidden` if decorative.
