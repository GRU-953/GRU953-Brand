---
disable-model-invocation: true
description: Generate a GRU953 brand asset — a mark, a lockup, an icon set or the tokens
argument-hint: [what you need, e.g. "the horizontal lockup in Meridian" or "favicons"]
---

Produce the GRU953 asset described in "$ARGUMENTS".

Follow the **gru953-branding** skill. Use `skills/gru953-branding/scripts/asset.py`, which
refuses any combination the brand does not permit — a mark below its size floor, or a colour
on a ground it is not approved against. If it refuses, do not work around it: it is telling
you a rule, and the message names the fix.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/gru953-branding/scripts/asset.py list
```

Before writing any file, settle three things and say what you settled:

1. **Where will it be used**, and therefore which file — the bird at 24px and above, the tile
   below that, a lockup where there is width, the wordmark where the bird would be too small.
2. **What ground will it sit on** — pass `--on paper|meridian|ink` so the pairing is checked.
3. **Vector or raster** — SVG unless the destination genuinely cannot take one.

Then write it, and say in one line why that file, that colour and that size.
