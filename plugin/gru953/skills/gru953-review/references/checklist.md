# GRU953 — the review checklists

Work the surface you actually have. Running a repository checklist over a single
social post produces noise, and noise is how a checklist stops being used.

Every list is ordered so that the earliest failures make the later checks worth
doing. Anything marked **blocker** stops the thing shipping.

---

## Every surface, always

- [ ] **blocker** — every factual claim, number, date and licence statement is
      correct. A beautiful page that lies is worse than an ugly one.
- [ ] **blocker** — every text colour clears **4.5:1** against its own
      background, in **both** themes.
- [ ] **blocker** — every border or icon that must be seen clears **3:1**, in
      both themes.
- [ ] The name is `GRU953` — one word, uppercase, no hyphen, no space.
- [ ] The first mention says what GRU953 *is*, because "GRU" already reads as
      Gated Recurrent Unit.
- [ ] Both taglines present and complete, or neither.
- [ ] No hype, no exclamation mark manufacturing enthusiasm, no "we".
- [ ] Every claim carries its number. Every limit is stated out loud.
- [ ] Nothing relies on colour alone to carry meaning.
- [ ] **What could be removed with no loss?** Remove it. This is a brand rule.

---

## A web page or an app screen

**Colour and theme**
- [ ] Not one literal hex value outside the tokens file.
- [ ] `--gru-accent` used, never one of its two values hard-coded.
- [ ] The page is correct with `data-theme="light"`, with `data-theme="dark"`,
      and with neither set. Check all three, not one.
- [ ] Anything whose subject *is* colour carries `forced-color-adjust: none`.

**Keyboard and focus**
- [ ] **blocker** — every interactive element is reachable by Tab, in a sensible
      order.
- [ ] **blocker** — focus is visible on every one of them, in both themes.
      An `outline:none` with no `:focus-visible` replacement is a keyboard trap
      in everything but name.
- [ ] The sticky header does not hide the element that has just received focus
      (WCAG 2.2 2.4.11).
- [ ] No tab stop on anything that does nothing. A focusable element with no
      role, no name and no behaviour is noise between the reader and the next
      real control.
- [ ] Any horizontally scrolling region *is* focusable — otherwise its far side
      is unreachable without a mouse.

**Structure and names**
- [ ] `<html lang>` set; `lang="bn"` on Bangla passages.
- [ ] One `<h1>`, and headings that descend without skipping.
- [ ] Every image has `alt`, and the `alt` says what the image **means**.
- [ ] Every SVG has a `<title>`, an `aria-label`, or `aria-hidden="true"` — one
      of the three, never none and never two.
- [ ] **blocker** — every `aria-labelledby` and `aria-describedby` points at an
      id that exists. A name that resolves to nothing is worse than no name,
      because the source still looks correct.
- [ ] Every form control has a real `<label>`, not a placeholder pretending.
- [ ] Error messages are associated with their field, and say what to do next.

**Size, motion, reflow**
- [ ] Interactive targets at least **24×24** CSS px (WCAG 2.2 2.5.8).
- [ ] No horizontal scrolling of the page at 320px wide. A wide table scrolls
      inside its own box instead.
- [ ] Text survives 200% zoom, and the viewport does not block zooming.
- [ ] `prefers-reduced-motion` respected.
- [ ] The mark is not animated.

**The mark**
- [ ] Right file for the size: the bird at 24px and above, the tile below.
- [ ] An approved colour-on-ground pairing.
- [ ] Colour set with `color:`, not `fill:`.
- [ ] Clear space of half the bird's height on all four sides.

---

## A repository

- [ ] **blocker** — `LICENSE` present, and byte-identical to canonical Apache-2.0.
- [ ] **blocker** — `NOTICE` present.
- [ ] `LICENSE-GUIDEBOOK.md` present if the repository ships GRU953 prose.
- [ ] **blocker** — nothing calls PolyForm-licensed content "open source".
- [ ] The README's **first line** says what this is.
- [ ] README licence section matches the files, and reserves the marks.
- [ ] Four badges at most: licence, version, tests, size. No visitor counter, no
      trophy case, no animated typing banner.
- [ ] The Bangla half is an original, not a translation.
- [ ] **blocker** — no secrets, tokens, `.env` files or personal data anywhere in
      the git *history*, not just the working tree.
- [ ] `.github/social-preview.png` present, and actually uploaded in Settings.
- [ ] Repository description and topics filled in.
- [ ] Source files that are likely to be copied out carry an SPDX line.
- [ ] The brand check runs in CI.
- [ ] It was private first, and made public as a separate deliberate step.

---

## A document, report or CV

- [ ] The lockup at 120px or more, Meridian on white, one position, one size.
- [ ] Sora for headings, Noto Sans for body, JetBrains Mono for anything technical.
- [ ] Body text at 16px equivalent or larger. No 9pt to fit one more line.
- [ ] Tables have real header rows, and no cell is coloured as its only meaning.
- [ ] Page numbers, and a date. A document with no date cannot be superseded.
- [ ] If it names a figure, it says where the figure came from.
- [ ] If it is a PDF, it has a title in its metadata and its text is selectable.
- [ ] For a CV: no photograph for a UK or US employer; a photograph is normal in
      Bangladesh and much of South Asia. Match the market you are applying to.

---

## A social post

- [ ] It fits the platform's limit **with a real link counted at 23 characters**,
      not with the `[link]` placeholder.
- [ ] One image, not a carousel. The image has alt text.
- [ ] The first line works alone, because that is all most people read.
- [ ] Both languages, if the audience is bilingual — as two posts or one, but
      never English with the Bangla as an afterthought.
- [ ] No hashtag wall. No "thread 🧵" unless there genuinely is one.
- [ ] Any number in it is one you can point at.

---

## Writing, in either language

- [ ] Plain UK English. No American spelling outside a quoted name.
- [ ] Active voice; a control says exactly what happens when it is used.
- [ ] The same word for the same thing throughout. "Save" does not become
      "Submit" three screens later.
- [ ] No "we". No "excited", "thrilled", "seamless", "effortless",
      "revolutionary", "game-changing", "cutting-edge", "unleash", "supercharge".
- [ ] No unbracketed gap where text was deleted — a double space mid-sentence, an
      empty `""`, a dangling colon. These read as finished copy with a typo,
      which is exactly why nobody fixes them.
- [ ] Bangla in চলিত register, honorific, conjuncts correct, Latin numerals,
      দাঁড়ি not a full stop.
- [ ] Bangla not justified, not letter-spaced, not in ALL CAPS — it has none.
- [ ] Errors say what happened and what to do next, and never blame the reader.
- [ ] An empty state is an invitation to act, not an apology.

---

## What to write at the end of every review

Two things, always:

**1. The findings**, most severe first, each in this shape:

```
SEVERITY | where | what is wrong | the rule it breaks | the fix
```

**2. What you could not check.** Almost always includes: whether the Bangla reads
naturally to a native speaker; whether it works with a real screen reader used by
a real person; whether a colour feels right; whether any claim about the world is
actually true; and anything whose contrast depends on a computed style, an image
behind text, or an opacity.

A review that omits its own blind spots reads as a clean bill of health. That is
worse than a stated gap, and it is the one failure a reviewer cannot be forgiven.
