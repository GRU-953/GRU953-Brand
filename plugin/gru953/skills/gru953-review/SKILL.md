---
name: gru953-review
description: >
  Reviews anything that already exists against the GRU953 brand and against WCAG 2.2 AA, and
  reports every violation with the rule it breaks and the fix. Checks colour and contrast in
  both themes, token use versus hard-coded values, mark usage and size floors, typography, the
  locked bilingual taglines, English voice, Bangla quality, licence and trademark statements,
  and accessibility basics. Use this skill whenever the user asks to check, review, audit,
  critique, proofread or approve something — a file, a page, a screenshot, a repository, a
  README, a document, a design, a post. Triggers on "review this", "check this", "is this on
  brand", "does this follow my brand", "audit", "brand review", "before I publish", "before I
  ship", "proofread", "any problems with this", "accessibility check", "contrast check", "is
  this accessible", "sign off". ALWAYS use it before anything carrying the GRU953 name is
  published, and after gru953-branding has produced something, as the independent second pass.
license: Apache-2.0 for scripts/; PolyForm-Noncommercial-1.0.0 for references/. NOTICE has the terms; the GRU953 marks are not licensed.
---

# GRU953 — review

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

You are the independent pass. Something has been made; your job is to find what
is wrong with it before anyone else does.

**The rules live in `gru953-branding/references/`.** This skill reads them; it does not
restate them. If that skill is not installed beside this one, the mechanical checks in
`scripts/check.py` still run — they carry the rules they need — but say plainly that the
judgement half of the review could not be done against the source.

**Be adversarial. Praise nothing.** A review that opens with what works is a
review the reader stops trusting. If something is genuinely fine, leave it out.

---

## How to run a review

### 1. Run the mechanical checks first

They are free, they are exact, and they find the boring failures so your
attention goes to the interesting ones.

```bash
python3 scripts/check.py path/to/file-or-directory
python3 scripts/check.py . --html            # also parse HTML for accessibility
python3 scripts/check.py styles/ --json      # machine-readable, for CI
```

The script measures contrast from the actual values, so its numbers are not
opinions. Everything it cannot check, it says it cannot check.

### 2. Then read, against the checklist

`references/checklist.md` has the full list by surface. Work the surface you
actually have — do not run a repository checklist over a single social post.

### 3. Then report

One line per finding, most severe first:

```
SEVERITY | where | what is wrong | the rule it breaks | the fix
```

- **blocker** — ships something false, illegible, or legally wrong.
- **major** — a rule broken that a careful reader would notice.
- **minor** — a rule broken that only the brand's owner would notice.

Nothing else. No summary paragraph of praise, no "overall this is strong".

### 4. Say what you could not check

End every review with it. A review that quietly omits its own blind spots reads
as a clean bill of health, which is worse than an honest gap. Things you almost
certainly could not check: whether the Bangla reads naturally to a native
speaker; whether it works with a real screen reader; whether a colour feels
right; whether a claim about the world is true.

---

## The order to check in

Severity is not the order of discovery. Check in this order, because each layer
makes the next one worth checking.

| # | Layer | The question |
|---|---|---|
| 1 | **True** | Is every factual claim, number and licence statement correct? A beautiful page that lies is worse than an ugly one. |
| 2 | **Legible** | Does every text colour clear 4.5:1 against its own background, in **both** themes? Every visible border and icon 3:1? |
| 3 | **Operable** | Keyboard-reachable, visible focus, targets at least 24×24px, nothing colour-only, `lang` set? |
| 4 | **On brand** | Name, taglines, mark, colour, type, voice, Bangla — the eight non-negotiables. |
| 5 | **Simple** | What could be removed with no loss? This is a brand rule, not a style note. |

## The eight failures to check for first

These are the ones that actually happen.

1. **`#FFAB8E` on a light ground.** 1.83:1. The single most common mistake. On
   light, the accent is `#B45A39`.
2. **A hard-coded hex where a role token exists.** It will be wrong in the other
   theme, and nobody will notice until someone switches.
3. **The bare bird below 24px.** Use the tile.
4. **The name spelled `Gru953`, `GRU 953` or `gru-953`** in prose.
5. **A shortened tagline**, or the Bangla missing entirely.
6. **"Open source"** used of the PolyForm-licensed writing. It is
   *source-available*.
7. **"We"** — there is one person behind this brand.
8. **A claim without its number.** "Much faster" is not a claim; "2.1× faster,
   measured on…" is.

## What a good finding looks like

> **blocker** | `styles/button.css:34` | `background:#FFAB8E` with
> `color:#FFFFFF` measures **1.83:1** | WCAG 2.2 AA needs 4.5:1 for text
> (`colour.md`, the approved-pairings table) | use `var(--gru-accent)` with
> `var(--gru-on-accent)`, which resolves to 4.71:1 on light and 10.55:1 on dark

It names the place, gives the measured number, names the rule, and gives the fix
in the form the codebase already uses. A finding without a fix is a complaint.

## What a bad finding looks like

> The colour palette could be more accessible.

No location, no measurement, no rule, no fix. Delete it.

---

## Reviewing a screenshot or a design

You cannot measure a JPEG's tokens, so say what you are inferring rather than
asserting. What you *can* judge from an image: whether the mark has its clear
space, whether it is above its size floor, whether text looks like it is fighting
its background, whether the Bangla is present, whether anything is animated in a
way a screenshot has caught mid-movement.

State plainly which findings are visual inference and which are measured.

---

## Reviewing writing

Read `gru953-branding/references/voice.md` and, for anything bilingual,
`bangla.md`. The failures worth naming:

- hype, exclamation marks manufacturing enthusiasm, "we're excited to";
- "we" for a one-person studio;
- a claim with no number;
- a limit softened or omitted;
- American spelling;
- Bangla that reads as a translation — the tells are in `bangla.md`;
- a `[bracketed]` placeholder left unfilled, or worse, an *unbracketed* gap where
  text was deleted. The second kind reads as finished copy with a typo, which is
  why it survives.

---

## When you find nothing

Say so in one line, and list what you could not check. Do not manufacture a
minor finding to look diligent — and do not manufacture reassurance either.
