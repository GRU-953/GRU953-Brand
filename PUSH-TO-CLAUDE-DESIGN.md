# Pushing the design system to Claude Design

**সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.**

The push needs a design-system authorisation that a cloud session cannot obtain, so this
last step is yours. It takes about two minutes, and every step below is one action.

You need the Claude Code command line on your Mac. If `claude` is not installed yet, stop
here and install it first — the rest will not work without it.

---

## Before you start

Everything is already on your Mac at:

```
~/Claude/Cowork/GRU953_Branding/
```

Inside that folder, the design system is at `design-system/`, and the plugin at `plugin/`.

---

## The push, step by step

1. Open **Terminal** on your Mac. (Press ⌘ + Space, type `Terminal`, press Enter.)

2. Type this exactly and press Enter:

   ```
   cd ~/Claude/Cowork/GRU953_Branding/design-system
   ```

3. Type `ls` and press Enter. You should see `build.py`, `_cards.json`, `foundations`,
   `components`, `patterns`. If you do not, you are in the wrong folder — go back to
   step 2 and check the spelling.

4. Type `claude` and press Enter. Wait for it to start.

5. Type `/design-login` and press Enter. A browser window opens.

6. In that browser window, approve the design-system access. Then return to Terminal.

7. Type `/design-sync .` and press Enter. The full stop at the end matters — it means
   "this folder".

8. When it asks which project, choose **create a new project** and name it `GRU953`.

9. It shows you the exact list of files it will write. **Read the list**, then approve it.
   There should be 27 HTML files plus the tokens and the fonts.

10. When it finishes, open **claude.ai/design**. The GRU953 project will be there, with the
    27 cards grouped as Foundations (5), Components (15) and Patterns (7).

**If step 5 says `/design-login` is not available**, Claude Design has a
**"Send to Claude Code Web"** button that does the same job from the other direction: it
creates a workspace with the project already set up, and you copy this folder into it.

*Both routes were correct at the time of writing (13 August 2026). I could not test either
from this session, because neither is reachable from a cloud container — that limit is the
whole reason this step is yours.*

---

## Installing the plugin in Claude Code

1. In Terminal, type this and press Enter:

   ```
   cd ~/Claude/Cowork/GRU953_Branding/plugin
   ```

2. Type `ls` and press Enter. You should see `gru953/`, `skills/`, and two `.zip` files.

3. Copy the `gru953` folder into the directory Claude Code scans for plugins on your
   machine. If you are not sure which that is, start `claude` and type `/plugin` — it
   will tell you, and it will let you install from a folder.

4. Restart `claude`. Type `/` and you should see four new commands:
   `/gru953:asset`, `/gru953:check`, `/gru953:design`, `/gru953:init`.

Claude will also load the three skills on its own when they are relevant — you do not have
to invoke them.

---

## Installing a single skill in the Claude app

The three files in `plugin/skills/` are ordinary zip archives with `SKILL.md` at the root:

| File | What it does |
|---|---|
| `gru953-branding.skill` | Holds the rules, and makes any single asset |
| `gru953-repo.skill` | Sets a whole repository up |
| `gru953-review.skill` | Checks something that already exists |

Upload one through the Claude app's skills interface, or unpack it into your skills folder.
`gru953-repo` and `gru953-review` both read `gru953-branding`'s reference documents, so
install that one too unless you only want the mechanical half.

---

## Rebuilding, if you change something

From `~/Claude/Cowork/GRU953_Branding/`:

```bash
cd 04_colour   && python3 engine.py       # regenerate every colour, and prove it
cd ..          && python3 sync-tokens.py  # copy the tokens into the plugin and the system
cd design-system && python3 build.py      # rewrite all 27 cards
node check.mjs                            # render them and measure
cd .. && python3 package.py               # check everything, then rebuild the archives
```

`engine.py` writes nothing if any check fails, and `package.py` packages nothing if any
check fails. That is deliberate: a build that half-succeeds is worse than one that stops.

---

Copyright © 2026 Aninda Sundar Howlader (GRU953) · aninda.sh15@gmail.com
