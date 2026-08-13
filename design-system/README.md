# GRU953 — design system

**27 previews over 15 components, in both themes, bilingual, ready to push to Claude Design.**

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

---

## What is here

27 cards, in three groups. Every one carries the tokens and the component CSS **inlined**, so
it renders with no build step and no network. The one thing not inlined is the five typefaces:
each card loads them from `../tokens/fonts/`, so a card copied somewhere else on its own falls
back to the system stack. Everything else about it still works.

| Group | Cards |
|---|---|
| **Foundations** (5) | Colour · Typography · Space, shape and depth · The marks · Motion |
| **Components** (15) | Button · Text fields · Checkbox, radio and switch · Card · Alert · Badge · Table · Tabs · Navigation · Dialog and toast · Progress and loading · Empty and error states · Stat · Code · Chart |
| **Patterns** (7) | A landing page · A settings screen · A documentation page · A dashboard · A sign-in screen · Following the system · A 404 page |

**Components and foundations show both themes side by side.** That is deliberate: the central
fact about this brand is that its signature has two values, and a library that showed only one
theme would be hiding the interesting half.

**One pattern — *Following the system* — pins no theme at all.** Three states exist and all
three need checking: `data-theme="light"`, `data-theme="dark"`, and neither. The third is what
a product actually ships with, and it is the one most often left untested.

## What needs JavaScript

CSS gives these components their position and their look. It cannot give them behaviour, and
a library that let you believe otherwise would be worse than one that says so.

| Component | What CSS does | What you must write |
|---|---|---|
| **Switch** | The track, the knob, the checked state | **One line, not optional.** The `on`/`off` label is a text node; CSS cannot rewrite it, so it will say the wrong thing after the first toggle unless a `change` listener updates it. The snippet is in the comment above `.gru-switch__state`. |
| **Dialog** | The panel, the backdrop, the layout | Use the real `<dialog>` element and `showModal()`. Escape, the focus trap and returning focus to the opener come free — and every one of them is easy to get wrong by hand. |
| **Toast** | Position, stacking, the look | Showing one, dismissing it, and removing it after a timeout. The close button has an accessible name and no handler; wire it or remove it. |
| **Tabs** | The strip, the selected state | Arrow keys to move between tabs and Tab to leave the set. If you are not going to write it, use links instead — a wrong ARIA pattern is worse than none. |
| **Table** | The scroll box, the focus ring | Adding `tabindex="0"` and `role="region"` only when the table actually overflows, and removing them when it does not. A tab stop on a table that fits is noise. |

## The file that matters

`src/components.css` **is** the design system. Everything else in this project is a preview of
what it does. It keeps three rules so nobody downstream has to remember them:

1. **Not one literal colour.** Every value comes from a role token in `tokens/tokens.css`,
   which is defined in both themes. A screen built from this file is correct in light and dark
   with no second stylesheet and no media query of yours.
2. **Focus is always visible.** There is no `outline: none` anywhere without a replacement.
3. **Nothing relies on colour alone** — in every example it ships. Each state carries a word,
   an icon or a shape as well as a colour. CSS cannot enforce this, though: an empty
   `<span class="gru-badge gru-badge--danger"></span>` is valid against every rule here and
   breaks the rule anyway. The library makes the right thing easy; it cannot make the wrong
   thing impossible.

To use it in a project, load four files in this order and then use the classes:

```html
<link rel="stylesheet" href="tokens/tokens.css">
<link rel="stylesheet" href="tokens/typography.css">
<link rel="stylesheet" href="tokens/layout.css">
<link rel="stylesheet" href="src/components.css">
<body class="gru"> … </body>
```

## Themes, and the one detail that makes them work

```html
<html>                        <!-- follows the reader's system setting -->
<html data-theme="light">     <!-- explicit light -->
<html data-theme="dark">      <!-- explicit dark -->
<div data-theme="dark">       <!-- a dark island inside a light page -->
```

That last line works because the theme blocks in `tokens.css` are scoped to
`[data-theme="…"]` rather than to `:root[data-theme="…"]`. With `:root` only, a nested
`data-theme` silently does nothing and the panel renders in the page's theme. The dashboard
pattern is shown in the dark theme inside a light preview page for exactly this reason — it is
the clearest demonstration in the project that a themed island is possible at all.

## Rebuild it

```bash
python3 build.py            # write every card
python3 build.py --check    # verify against what is on disk, write nothing
node check.mjs              # render all 27, both themes, four widths, and measure
node check.mjs --card button   # one card, while you are fixing it
```

Every card is generated from `src/components.css`, `tokens/` and the markup in `build.py`, so
no card can drift out of step with the stylesheet it is demonstrating. `build.py` refuses to
write if a card's `@dsCard` marker is missing, if a path is duplicated, or if a literal colour
has crept into either the markup or **`components.css` itself** — the file that claims to
contain none was, for a while, the one file the check never looked at. `--check` compares
against **the files on disk**, not against the model it just built in memory, so a
hand-edited or deleted card fails it.

`check.mjs` does what neither of those can: it opens a browser. Three faults got past the
static checks — a two-column grid with no breakpoint that pushed 163px of a settings screen
outside a clipping ancestor where it was neither visible nor scrollable, a pressed-state rule
that never rendered because a more specific hover rule always won, and the one card that
claimed to follow the reader's system setting while pinning a theme. It measures contrast
against the *effective* background, finds content clipped by an ancestor, checks every ARIA
reference resolves, and confirms a focus indicator actually appears. What it cannot measure —
a real screen reader, forced colours, print, other engines — it prints at the end rather than
passing in silence.

`_cards.json` lists every path, name, group and viewport — that is what the push step reads.

## Pushing it to Claude Design

The push needs a design-system authorisation that a cloud session cannot obtain, so the last
step is yours. It takes about two minutes.

1. Open **Terminal** on your Mac.
2. Type this and press Enter:
   ```
   cd ~/Claude/Cowork/GRU953_Branding/design-system
   ```
3. Type `claude` and press Enter.
4. Type `/design-login` and press Enter. A browser window opens.
5. Approve the design-system access in that browser window, then return to Terminal.
6. Type `/design-sync .` and press Enter.
7. When it asks which project, choose **create a new project** and name it `GRU953`.
8. It shows you the exact list of files it will write. Read the list, then approve it.
9. When it finishes, open **claude.ai/design** and the GRU953 project will be there, with the
   27 cards grouped as Foundations, Components and Patterns.

If step 6 reports that nothing is set up yet, that is expected — `/design-sync` creates the
project on the first run.

The same steps, with nothing assumed and one action per line, are in
`../PUSH-TO-CLAUDE-DESIGN.md`.

**If `/design-login` is not available**, Claude Design's own **"Send to Claude Code Web"**
button does the same job from the other direction: it seeds a workspace with the project, and
you copy this folder into it.

## Licence

**`src/components.css`, `tokens/`, `build.py`, `check.mjs` and the 27 preview files:**
Apache-2.0. Use them, change them, sell
what you build with them. No permission needed.

**The preview copy** — the words inside the cards — is PolyForm Noncommercial 1.0.0:
source-available, not open source.

**Not licensed:** the name **GRU953**, the Soaring Bird mark, the app-icon tile, the GRU953
wordmark and any lockup of them — everything in `src/marks/`. Fork the system and replace
the identity with your own.

**The typefaces** in `tokens/fonts/` are SIL Open Font Licence 1.1, and each licence file
travels with them.

`LICENSE` and `NOTICE` are at the root of this folder. The NOTICE is the file Apache-2.0
section 4(d) requires; it must travel with anything you redistribute.

*Not legal advice.*

Permissions and questions: aninda.sh15@gmail.com

---

Copyright © 2026 Aninda Sundar Howlader (GRU953)
