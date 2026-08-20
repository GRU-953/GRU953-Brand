# This folder — the kit's own build helpers

`brand-kit/00_sandbox/` holds the scripts specific to *this kit's* build —
`verify.py` (its 167 mechanical checks), `render.mjs` and `pdf.mjs` (SVG/PDF
rendering for the guidebook), `check.mjs` (renders the built guidebook and
sweeps it for layout faults), `svgo.config.mjs`. Its own `package.json`
(`css-tree`, `playwright`, `svgo`) is installed the same way it always was —
`npm ci` from inside this folder — and CI still does exactly that.

**The repo-wide sandbox — the pinned Python environment, the project-local
Chromium, the font installer, the hermetic build-with-nothing-on-PATH proof —
now lives one level up, at the repository root: `../../00_sandbox/`.** That is
the sandbox every part of this repository builds against, not just this kit,
because `design-system/` and `plugin/` need the same pinned tools too. See
**`../../00_sandbox/TOOLCHAIN.md`** for the full toolchain, the substitution
table, and how to rebuild it with one command.

Historical note: before 20 August 2026 this folder's own `TOOLCHAIN.md`
described an isolated cloud workspace with Inkscape, system-installed fonts
and hardcoded container paths that made the kit unbuildable anywhere else.
That description now lives at the repository root, corrected and replaced —
see the note at the top of `../../00_sandbox/TOOLCHAIN.md` for what changed
and why.
