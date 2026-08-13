---
disable-model-invocation: true
description: Review something against the GRU953 brand and WCAG 2.2 AA
argument-hint: [a file, a directory, or nothing for the whole project]
---

Review `$ARGUMENTS` (default: the current directory) against the GRU953 brand and against
WCAG 2.2 AA.

Follow the **gru953-review** skill. In order:

1. Run the mechanical checks and read their output:
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/gru953-review/scripts/check.py $ARGUMENTS --html`
2. Read `gru953-review/references/checklist.md` and work the checklist for the surface you
   actually have — a repository, a page, a document, a post or a piece of writing. Do not run
   a repository checklist over a single social post.
3. Read anything the script cannot: the writing, the Bangla, the structure, the judgement.
4. Report findings most severe first, one line each:
   `SEVERITY | where | what is wrong | the rule it breaks | the fix`
5. End with what you could not check.

Be adversarial. Praise nothing — if something is genuinely fine, leave it out. A review that
opens with what works is a review the reader stops trusting.
