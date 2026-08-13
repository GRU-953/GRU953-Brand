---
name: gru953-repo
description: >
  Sets a whole repository up to GRU953's standard, or brings an existing one up to it. Writes
  the LICENSE and NOTICE files, a bilingual README from the GRU953 template, the licence
  headers, and a brand check that runs in CI; it calls gru953-branding for the artwork it
  places. Use it when the unit of work is a REPOSITORY rather than a file: starting a new
  project, or making an existing one GRU953-compliant before it is pushed or made public.
  Triggers on "new repo", "new project", "set up a repository", "start a project", "scaffold",
  "bootstrap", "init", "add the licence FILES to this repo", "LICENSE file", "NOTICE file",
  "README for this project", "make this repo look like mine", "brand this project", "GitHub
  profile", "publish this repo". ALWAYS use it before a GRU953 repository is first pushed. For
  ONE asset — a logo, a banner, an icon set — use gru953-branding. REQUIRES gru953-branding
  installed beside it.
license: Apache-2.0 for scripts/; PolyForm-Noncommercial-1.0.0 for the README template. NOTICE has the terms; the GRU953 marks are not licensed.
---

# GRU953 — repository setup

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

This skill puts the seven things a GRU953 repository needs into place, in the
order that matters. It does not write the project's own code.

**This skill depends on `gru953-branding`,** which must be installed beside it. Read
`gru953-branding/references/licence.md` before touching a licence file, and
`gru953-branding/references/voice.md` before writing a word of the README. If those
files are not there, say so rather than guessing the rules — `init.py` will report
the same thing when it cannot find the artwork.

---

## What "set up" means here

| # | The file | Why it exists |
|---|---|---|
| 1 | `LICENSE` | Apache-2.0, verbatim. The system is genuinely open. |
| 2 | `NOTICE` | Required by Apache-2.0 §4(d). Carries the trademark reservation downstream to anyone who redistributes. |
| 3 | `LICENSE-GUIDEBOOK.md` | PolyForm Noncommercial 1.0.0, verbatim — **only** if the repository ships GRU953 long-form writing. |
| 4 | `README.md` | Bilingual, in the GRU953 voice, with the licence line correct. |
| 5 | `.github/social-preview.png` | 1280×640. Without it GitHub shows a generic card on every share. |
| 6 | `public/` icons | `favicon.ico`, `icon.svg`, `apple-touch-icon.png`, `mask-icon.svg` and the PNG set. |
| 7 | `styles/tokens.css` + `scripts/brand-check.mjs` | The design tokens, and a check that fails the build if the brand breaks. |

## Run it

```bash
python3 scripts/init.py --dir . --name "Ledger" --what "keeps a record of daily takings"
```

Useful flags:

| Flag | Effect |
|---|---|
| `--dir PATH` | Where to write. Default: the current directory. |
| `--name NAME` | The product's own name. Omit for a repository that is GRU953 itself. |
| `--what "…"` | One plain sentence saying what it does. Goes in the README's first line. |
| `--writing` | Also add `LICENSE-GUIDEBOOK.md` — the repository ships GRU953 prose. |
| `--web` | Also add the icon set and `styles/tokens.css`. |
| `--dry-run` | Print what would change, write nothing. |
| `--force` | Replace a file that already exists. Without it, nothing is overwritten. |

It never overwrites a file silently. Anything that already exists is reported,
and left alone unless you say otherwise.

---

## The naming decision, before anything is created

GRU953 is a **parent brand over apps that carry their own names**, so the
default is the **endorsement form**: `Ledger by GRU953` on first mention, then
`Ledger` alone. Use the prefix form `GRU953 Notes` **only** when the name is too
generic to stand alone in a listing. Never both in one document.

The repository name is lowercase with hyphens: `gru953-ledger`.

Full rules in `gru953-branding/references/naming.md`. Get this right before the
first commit — a repository is renamed at some cost, and a package name at more.

---

## The README, in the GRU953 voice

The order is fixed, because it is the order a reader needs.

1. **What it is, in one sentence, immediately.** Not a tagline, not a badge wall.
   Because of the "GRU" reading risk, the first line must say what this is.
2. The bilingual tagline.
3. **The screenshot or the one-line demo** — whichever shows it working faster.
4. **Install**, as commands that can be pasted.
5. **Use**, with the smallest example that does something real.
6. What it deliberately does **not** do. This is more useful than another feature.
7. **Licence**, in the exact wording from `references/licence.md`.
8. The Bangla half — an original, not a translation.

**No badge wall.** Four badges at most, in this order: licence, version, tests,
size. No visitor counter, no trophy case, no animated typing banner. Those read
as decoration to a recruiter and as noise to a developer.

The template is `assets/README.template.md`; `init.py` fills it in.

---

## The theme-switching banner

GitHub honours `prefers-color-scheme` in markdown through `<picture>`. It is the
only reliable way to make a banner correct in both themes:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/readme-header-dark.png">
  <img src=".github/readme-header-light.png" alt="GRU953 — simple technology, for everyone." width="100%">
</picture>
```

The `alt` says what the banner **means**, not that it is a banner.

---

## The brand check

`scripts/brand-check.mjs` is written into the repository so the rules keep applying
after this session ends. It is a *token and licence* check, not a contrast checker —
measuring contrast needs `gru953-review`'s `check.py`, which the repository does not
ship. It fails the build on:

- a hard-coded brand hex value in component code where a token exists;
- the bare bird rendered below 24px;
- a missing `LICENSE` or `NOTICE`;
- a README that calls the project "open source" while shipping PolyForm content;
- `Gru953`, `GRU 953` or `gru-953` in prose.

Wire it in:

```yaml
# .github/workflows/brand.yml
name: brand
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: node scripts/brand-check.mjs .
```

---

## Publishing

**Private first.** Push to a private repository, look at it as a stranger would,
then make it public in a separate, deliberate step. The order costs nothing and
has saved every developer who has ever done it.

Before making it public, check:

- [ ] No secrets, tokens, `.env` files or personal data in the history — not just
      the working tree. `git log -p` is not paranoia.
- [ ] `LICENSE` and `NOTICE` present; `LICENSE-GUIDEBOOK.md` if prose ships.
- [ ] README's first line says what this is.
- [ ] The social preview is set: **Settings → Social preview → upload**
      `.github/social-preview.png`. Twenty seconds, and it is the first
      thing a stranger sees before they see any of the code.
- [ ] Description and topics filled in.
- [ ] The brand check passes.

---

## An existing repository

Same script, same order, but nothing is overwritten without being reported. Work
through it in this sequence:

1. **Licences first.** They are the thing most likely to be wrong, and the
   thing most expensive to get wrong.
2. **Then the README licence line**, which usually contradicts the files.
3. **Then the artwork**, which is cosmetic and can wait.
4. **Then the check**, so it cannot drift back.

Do not rewrite the project's own documentation in one pass. Fix what is wrong,
leave what works, and say which is which.
