---
disable-model-invocation: true
description: Set a repository up to GRU953's standard, or bring an existing one up to it
argument-hint: [the product name, e.g. "Ledger" — omit for a GRU953 repository itself]
---

Set up the repository in the current directory for GRU953. If "$ARGUMENTS" names a product,
that is the product's own name.

Follow the **gru953-repo** skill.

1. **Settle the name first**, before anything is created. GRU953 is a parent brand over apps
   that carry their own names, so the default is `<Name> by GRU953`, with the repository named
   `gru953-<name>`. Read `gru953-branding/references/naming.md`. A repository is renamed at
   some cost and a package name at more.
2. Run a dry run and show the user what would change:
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/gru953-repo/scripts/init.py --dir . --dry-run`
3. Run it for real once they have seen the list. Add `--web` for a site or app, `--writing` if
   the repository ships GRU953 long-form prose.
4. **Fill in the README yourself.** The template has `[bracketed]` slots; the first line must
   say what this is, because to a developer audience "GRU" already reads as Gated Recurrent
   Unit. Write the Bangla half as an original, not a translation — read
   `gru953-branding/references/bangla.md`.
5. Run `node scripts/brand-check.mjs .` and fix anything it finds.
6. Tell the user the remaining manual steps: push private first, upload the social preview in
   Settings, then make it public as a separate deliberate step.

Never overwrite a file the user already has without showing them first.
