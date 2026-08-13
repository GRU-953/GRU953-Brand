# GRU953 — the plugin

**The GRU953 brand, as something Claude can actually apply.**

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

---

## What it is

Three skills and four commands. Together they do the three things a brand needs doing on an
ordinary day: **apply it**, **set it up**, and **check it**.

| Skill | What it does | Where it fires |
|---|---|---|
| **gru953-branding** | Enforces every rule of the identity, and generates its assets — marks, lockups, icon sets, social artwork, design tokens. Holds the reference documents the other two read. | Claude and Claude Code |
| **gru953-repo** | Sets a repository up to standard, or brings an existing one up to it: licences, NOTICE, a bilingual README, icons, social preview, tokens, and a brand check that runs in CI. | Claude Code, mostly |
| **gru953-review** | The independent second pass. Reviews any file, page, repository or piece of writing against the brand and against WCAG 2.2 AA, and reports the rule broken and the fix. | Claude and Claude Code |

| Command | What it does |
|---|---|
| `/gru953:check [path]` | Review something. Mechanical checks first, then judgement, then what could not be checked. |
| `/gru953:asset [what you need]` | Produce a mark, a lockup, an icon set or the tokens — and refuse anything the brand does not permit. |
| `/gru953:init [product name]` | Set the current repository up. Dry run first, always. |
| `/gru953:design [what to build]` | Build a screen or component from the role tokens, correct in both themes. |

Claude Code namespaces a plugin's commands, so the full form is `/gru953:check`. The bare
`/check` also works unless something else has claimed the name. The four commands are typed,
never fired automatically — the three skills carry the automatic triggers, and a command
that also auto-fired would double every trigger word in the plugin.

## Install

**Claude Code.** Drop the whole `gru953` folder into a directory Claude Code scans for
plugins, or add it to a marketplace you control and install it from there. The skills and
commands are discovered automatically; there is no separate registration step.

**Claude (the app).** Each skill also works on its own. The three files in `skills/` —
`gru953-branding.skill`, `gru953-repo.skill`, `gru953-review.skill` — are ordinary zip
archives with `SKILL.md` at the root. Upload one, or unpack it into your skills directory.
They use only the six frontmatter fields the Agent Skills specification defines (`name`,
`description`, `license`, `compatibility`, `metadata`, `allowed-tools`), so they load
unchanged in Claude Code, in the Claude app and through the Skills API.

`gru953-repo` and `gru953-review` both read `gru953-branding`'s reference documents. Each
says so, and each still runs without it — with the half it cannot do stated plainly rather
than skipped.

Nothing here needs a network or an API key. The scripts use the Python standard library;
`favicon.ico` additionally wants Pillow, and PNG output wants `rsvg-convert`, `cairosvg` or
Inkscape. Each says so plainly, by name, if it is not present — and writes everything else
regardless.

## Try it in one minute

```bash
# what exists, and what is approved on what
python3 gru953/skills/gru953-branding/scripts/asset.py list

# the rule the brand is built on, measured rather than asserted
python3 gru953/skills/gru953-branding/scripts/asset.py check "#FFAB8E" "#FFFFFF"
python3 gru953/skills/gru953-branding/scripts/asset.py check --role accent --theme light

# what it refuses, and why
python3 gru953/skills/gru953-branding/scripts/asset.py svg bird daybreak-dark --on paper -o /tmp/x.svg
```

That last command fails on purpose. `#FFAB8E` on white measures **1.83:1** and the bird all
but disappears — which is exactly why the signature has two values, and why a script that
refuses is more useful than a document that warns.

## The one thing to understand

**The signature is one hue with two tuned values.**

Contrast is a ratio between two luminances. To clear WCAG's 4.5:1 against white, a colour must
be darker than luminance 0.1833; to clear 4.5:1 against the Ink `#0B0E14`, it must be lighter
than 0.1946. Both cannot be true.

> No single colour can be this brand's text colour in both themes. That is arithmetic, not
> taste.

So Daybreak is `#B45A39` on light grounds and `#FFAB8E` on dark ones. Use `--gru-accent` and
let the theme choose. Everything else in this plugin follows from taking that seriously.

## What is inside

```
gru953/
├── .claude-plugin/plugin.json
├── LICENSE  NOTICE               Apache-2.0, and what it does and does not cover
├── commands/                     four typed slash commands
└── skills/
    ├── gru953-branding/
    │   ├── SKILL.md              the eight non-negotiables, and which reference to read
    │   ├── NOTICE                what in THIS skill is Apache-2.0 and what is not
    │   ├── references/           colour · logo · typography · voice · bangla · licence
    │   │                         layout · naming
    │   ├── assets/               tokens, components.css, the five typefaces with their
    │   │                         OFL licences, the eight marks, the ready-made artwork
    │   └── scripts/asset.py      emits any asset; refuses what the brand does not permit
    ├── gru953-repo/
    │   ├── SKILL.md   NOTICE
    │   ├── assets/README.template.md   the bilingual README every repo starts from
    │   ├── assets/licences/      Apache-2.0 and PolyForm, verbatim
    │   └── scripts/init.py       sets a repository up; never overwrites silently
    └── gru953-review/
        ├── SKILL.md   NOTICE
        ├── references/checklist.md   by surface: page, repository, document, post, writing
        └── scripts/check.py          measured contrast, no dependencies, states its blind spots
```

## Licence

**The plugin, the scripts, the tokens and `components.css`:** Apache-2.0. `LICENSE` and
`NOTICE` are at the root of this plugin, and each skill carries its own `NOTICE` so a
standalone install still says what it covers.

**The reference documents:** PolyForm Noncommercial 1.0.0 — free to read, copy, adapt and
share for any noncommercial purpose; selling needs permission. It is **source-available, not
open source**, and this plugin will not blur the two.

**Not licensed:** the name **GRU953**, the Soaring Bird mark, the app-icon tile, the GRU953
wordmark and any lockup of them. They identify the studio, so they stay with it. Fork the system freely — the licence
permits it — but replace the identity with your own.

*Not legal advice. Written by the kit's author, who is not a lawyer.*

---

Copyright © 2026 Aninda Sundar Howlader (GRU953) · aninda.sh15@gmail.com
