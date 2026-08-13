---
disable-model-invocation: true
description: Build a screen or component with the GRU953 design system
argument-hint: [what to build, e.g. "a settings screen" or "an empty state for the reports page"]
---

Build "$ARGUMENTS" using the GRU953 design system.

Follow the **gru953-branding** skill, and read `references/colour.md` and `references/layout.md`
before writing any CSS.

The rules that decide whether this is right:

1. **Not one literal colour.** Every value comes from a role token — `--gru-bg`, `--gru-ink`,
   `--gru-accent`, `--gru-border`, and the rest. They are defined in both themes, so what you
   build is correct in light and dark with no second stylesheet. Paste
   `${CLAUDE_PLUGIN_ROOT}/skills/gru953-branding/assets/tokens.css` in and use the names.
2. **Check all three theme states**, not one: `data-theme="light"`, `data-theme="dark"`, and
   neither set (which follows the reader's system).
3. **Focus is visible on everything interactive**, in both themes. An `outline: none` with no
   `:focus-visible` replacement is a keyboard trap in everything but name.
4. **Nothing relies on colour alone.** Every state that has a colour also has a word, an icon
   or a shape.
5. **One primary action per view.** If two things are shouting, one of them is wrong.
6. **The mark does not move**, and below 24px it is the tile, not a smaller bird.

**The component library ships with this plugin.** Load
`${CLAUDE_PLUGIN_ROOT}/skills/gru953-branding/assets/components.css` beside the tokens and
reuse its classes — `gru-btn`, `gru-card`, `gru-alert`, `gru-field`, `gru-table`,
`gru-shell`, and the rest — rather than writing new CSS. Every one of them is measured in
both themes; a new one is not.

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="typography.css">
<link rel="stylesheet" href="layout.css">
<link rel="stylesheet" href="components.css">
<body class="gru"> … </body>
```

When you are done, run `/gru953:check` on what you built.
