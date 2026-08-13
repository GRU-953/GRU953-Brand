# GRU953 — design rules

The parts of the system that are not colour, type or the logo file itself: how the mark
is placed, how a page is laid out, how icons and pictures behave, how things move, and
what accessibility actually requires rather than what it is usually reduced to.

---

## 0. When the thing you need is not in the system

This is the first section because it is the question that actually comes up, and a system
with no answer to it gets abandoned the first time it is inconvenient.

**You need a colour the palette does not have.** Work down this list and stop at the first
answer that works.

1. **Use a role token instead of a new colour.** Nine times out of ten the need is "a
   warning" or "a muted surface", and there is already a token for it.
2. **Group the data.** If a chart needs a seventh series, the honest fix is usually fewer
   series: group the tail into "other", or split it into two charts. Seven colours is the
   point at which a reader stops distinguishing them anyway.
3. **Use a different step of a colour already in the palette.** Every family has eleven, and
   `CONTRAST.md` records what each one clears.
4. **Only then add a hue** — and add it properly, in `04_colour/engine.py`, as a family with
   a stated meaning. Then re-run the engine, which will refuse to write anything if the new
   hue is illegible or too close to an existing one. Never paste a hex code into a stylesheet
   to get past an afternoon; that is how a palette becomes a paint shop.

**You need a size, weight or spacing the scale does not have.** Round to the nearest step on
the scale. If the layout genuinely breaks, the layout is the problem, not the scale.

**You need to break a rule in this document.** Write down which rule and why, in the same
place as the work. A rule broken with a reason is a decision; a rule broken quietly is drift.

## 1. Using the logo

### 1.1 Which file, at which size

There is one bird. Choosing is mechanical:

| If the mark will be shown at | Use | File |
|---|---|---|
| 24px and above | The mark itself | `GRU953-bird.svg` |
| Below 24px | **The tile**, not a shrunken bird | `GRU953-appicon.svg` |

Below 24px the bird's strokes thin out and the wing's *counters* begin to close — counters
being the small enclosed gaps inside a shape, like the hole in an *o*. They are always the
first thing to blur shut as a drawing gets smaller. The tile
solves that honestly: a block of colour is recognisable at a size where a line drawing is
not. Shrinking the bare mark to 16px and hoping is the single most common way to make this
identity look amateur.

This floor is checked mechanically. `03_logo/marks.py` rasterises the mark at 24px on every
build and refuses to write the file if the counters have closed.

### 1.2 Minimum sizes

- Horizontal lockup: **120px** on screen, **25mm** in print. Below that the wordmark's
  digits start to close up.
- Lockup with the tagline: **260px** on screen, **55mm** in print.
- The bird alone: **24px** on screen, **6mm** in print.
- The tile: **16px**.

These are floors, not targets. If a layout can only give the logo 90px, use the mark alone
rather than shrinking the lockup.

### 1.3 Clear space

**One half of the mark's own height, on all four sides.** So a 64px bird needs 32px of
empty space around it. Nothing enters that space: no text, no rule, no border, no second
logo, no photograph edge, no button.

The `.gru-logo-safe` class in `layout.css` enforces this, so it does not have to be
remembered every time.

### 1.4 Colour combinations that are approved

| Ground | Mark colour | Ratio | Notes |
|---|---|---|---|
| Meridian `#1A1753` | Daybreak `#FFAB8E` | 8.88:1 | The primary pairing. |
| Meridian | Paper `#FFFFFF` | 16.26:1 | For maximum formality — a CV, an invoice, a legal page. |
| Ink `#0B0E14` | Daybreak `#FFAB8E` | 10.55:1 | Dark theme. |
| Paper `#FFFFFF` | Meridian | 16.26:1 | The default on light. |
| Paper | Daybreak `#B45A39` | 4.71:1 | When the mark must be warm on white. |
| Paper | Ink | 19.32:1 | Single-colour printing, stamps, engraving. |
| A photograph | Ink or Paper only | — | See 1.5. |

Nothing else. **Daybreak `#FFAB8E` on paper is not approved:** at 1.83:1 the bird
disappears. That pairing is exactly why the signature has two values — on a light ground
the correct Daybreak is `#B45A39`.

### 1.5 On a photograph

The mark goes on a photograph only in white or in Ink, and only over a part of the image
that is genuinely plain. If the area is busy, put a solid Meridian panel behind the mark
rather than trying to make it work — a panel is honest, a barely-visible logo is not.

### 1.6 The things never to do

1. **Do not stretch, squash, rotate or skew it.** The bird is already in flight; tilting
   it does not make it fly harder.
2. **Do not recolour it** outside the approved builds. No gradients on the mark itself —
   the gradient belongs to the background, never to the bird.
3. **Do not add effects.** No drop shadow, no outer glow, no bevel, no outline, no stroke.
4. **Do not re-typeset the wordmark.** It ships as outlines precisely so it cannot drift.
   If the wordmark is set as live text in Sora it is *text*, not the logo.
5. **Do not place it inside a shape** it was not given — no circles, no badges, no
   "roundel" versions. The app-icon tile is the one approved container.
6. **Do not combine it with another logo** in a way that reads as a joint venture.
7. **Do not use it as a decorative pattern**, a bullet point, or a texture.
8. **Do not animate the bird flapping.** See section 4.

### 1.7 What the bird means, for anyone who asks

A bird climbing rather than a bird arrived. The faceted wing is deliberate: it is a
constructed thing, drawn from parts, like software. That is the whole idea — something
made carefully, going somewhere. The mark is not a metaphor for freedom or for speed,
and the guidebook does not claim it is.

---

## 2. Layout

### 2.1 The grid

12 columns on a desktop, 6 on a tablet, 4 on a phone, with a 24px gutter. Content is
capped at **1216px**; a page that is mostly prose is capped at **736px** instead, because
a line of text longer than about 68 characters is measurably harder to read.

### 2.2 The spacing scale

A 4px base: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128. Every gap in the system is one of
those numbers. **When unsure, use 16px.** Two things that belong together get a smaller
gap than the gap to whatever is next — that single rule does most of the work of making
a layout look organised.

### 2.3 Shape

Four radii: 4px for badges and inline code, 8px for buttons and inputs, 14px for cards
and images, 24px for hero panels. The app icon uses 22.46% because that is the *squircle* —
a rounded square, rounder than a normal button corner — that Apple and Google both expect.
Do not reuse that number anywhere else.

### 2.4 Depth

Three shadow levels, all tinted with Meridian rather than black — a grey shadow on a
coloured brand always looks slightly dirty. **In dark mode shadows do not work at all**,
so depth is carried by a lighter surface plus a 1px border instead. Do not simply darken
the shadow and hope.

### 2.5 The composition habit that carries the brand

Most of the identity's character comes from one habit: **a deep Meridian field with a
great deal of empty space, one point of Daybreak, and everything aligned to a single
strong edge.** Restraint is doing the work, not decoration. If a layout feels flat, the
answer is more space and better alignment, not more colour.

---

## 3. Icons and pictures

### 3.1 Icons

Use **Material Symbols** (Apache 2.0, so free for any purpose), in the **Rounded** style,
at **weight 300**, optical size matched to the text beside it. Part of the system —
it was the right choice and there is no reason to churn it.

Rules:

- **1.5px stroke** at 24px, scaling proportionally. Never mix stroke weights in one view.
- Icons inherit the text colour they sit beside. An icon is not an opportunity for colour.
- **An icon never carries meaning alone.** Every icon that means something has a text
  label, or an `aria-label` if it genuinely cannot. This is not optional politeness; a
  screen reader announces nothing at all for a bare icon.
- Do not draw custom icons unless Material Symbols has no equivalent. A single
  inconsistent custom icon is more noticeable than a slightly imperfect standard one.

### 3.2 Pictures

The honest position: GRU953 is one person, and **stock photography of smiling strangers
in an office would be a lie**. So the picture policy is:

1. **First choice — no picture.** Type, space and one colour, done well, beat a
   decorative image every time.
2. **Second choice — the real thing.** A screenshot of the actual software, a photograph
   of the actual desk, the actual person. Real and slightly imperfect is better than
   polished and generic.
3. **Third choice — generated abstract art** built from the brand's own geometry: the
   first-light gradient, the wing's facet angles, the grid. This is the only approved
   decorative imagery.
4. **Never** stock photos of people, handshakes, glowing brains, circuit-board overlays,
   or anything that implies a team or an office that does not exist.

Screenshots get a 14px radius, a 1px border, and shadow level 2. Nothing else.

### 3.3 Diagrams

Diagrams use the neutral ramp for structure and Daybreak for the one thing the reader
should look at first. If a diagram needs more than three colours it is showing more than
one idea and should be two diagrams.

---

## 4. Motion

### 4.1 Two durations, two curves

- **120ms** for a colour, a hover, a focus ring.
- **220ms** for something arriving or leaving.
- Anything above **300ms** on an interface element reads as broken, not elegant.
- Ease-out for things arriving, ease-in-out for things moving in place.

### 4.2 What may move, and what may not

May move: a panel sliding in, a list reordering, a loading indicator, a focus ring, a
number counting to its value once.

**May not move: the logo.** The Soaring Bird does not flap, fly across the screen, draw
itself in, or pulse. A logo that performs is asking for attention rather than earning it,
and it dates within a year. The single permitted exception is a fade-in on first page
load, at 220ms, once.

### 4.3 Reduced motion is not a nice-to-have

Every transition in this system is switched off by `prefers-reduced-motion: reduce`,
which is already wired into `typography.css`. For some people motion causes genuine
nausea and vertigo. Honouring that setting costs four lines of CSS. A brand whose second
pillar is "for everyone" does not get to skip it.

---

## 5. Accessibility

This is the chapter most brand guides reduce to a contrast table. Contrast is the easy
part. These are the commitments that actually matter.

### 5.1 The floors, which are not negotiable

| Requirement | The rule | Where it is proved |
|---|---|---|
| Text contrast | 4.5:1 normal, 3:1 large (24px, or 19px bold) | `04_colour/CONTRAST.md` — every ratio computed |
| Non-text contrast | 3:1 for UI parts, focus rings, meaningful graphics | same file |
| Focus visible | A 3px ring at 2px offset, on every interactive thing | `typography.css`, `:focus-visible` |
| Keyboard | Everything reachable and operable without a mouse | must be tested, not assumed |
| Text size | Body text never below 16px; all sizes in `rem` | `typography.css` |
| Reduced motion | Honoured | `typography.css` |
| Target size | 24×24px minimum for anything tappable, 44×44px preferred | — |

### 5.2 Colour is never the only signal

Every state carries a second cue. An error is red **and** says "Error" **and** has an
icon. A required field is marked with a word, not a colour. A chart series is
distinguished by a shape or a direct label, not by hue alone. Roughly one man in twelve
has some form of colour-vision deficiency; this rule is the difference between a design
that works for them and one that does not.

### 5.3 Language must be declared

Every page sets `lang`, and every Bangla passage inside an English page sets `lang="bn"`.
Without it a screen reader attempts to pronounce Bangla with English rules, and the
result is unintelligible. For a bilingual brand this is the single highest-value
accessibility line of code there is.

### 5.4 Alternative text, written properly

Every image gets alt text that says what it *means*, not what it *is*. The logo's alt text
is `GRU953`, not "logo". Decorative art gets `alt=""` so it is skipped rather than
narrated. The logo SVGs already carry `<title>` and `<desc>`, so an inline SVG is
announced correctly without extra work.

### 5.5 What this kit does not claim

- Passing a contrast ratio does not make a screen readable. Size, weight, line length and
  the sheer amount of text all matter and none of them is measured by a ratio.
- **Nothing here has been tested with a real screen reader by a real user.** That is a
  genuine gap, stated plainly rather than papered over.
- APCA, the candidate contrast method in the draft WCAG 3, is not used. WCAG 2.2 AA is the
  standard actually cited in law and procurement today.
- Distinctiveness is computed for normal colour vision. It is not a colour-blindness
  simulation. Colour is never the only carrier of meaning here — every state also carries a
  word, an icon or a shape — and that, not the ΔE figure, is the actual protection.
