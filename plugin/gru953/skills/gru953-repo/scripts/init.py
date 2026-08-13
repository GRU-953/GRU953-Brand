#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""GRU953 — set a repository up, or bring an existing one up to standard.

Nothing here is overwritten silently. Every file that already exists is reported
and left alone unless --force says otherwise, because a script that quietly
replaces someone's README is a script nobody runs twice.

    python3 init.py --dir . --name "Ledger" --what "keeps a record of daily takings"
    python3 init.py --dir . --web --writing
    python3 init.py --dir . --dry-run
"""
from __future__ import annotations
import argparse, datetime, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
SKILL = HERE.parent
LICENCES = SKILL / "assets/licences"
BRANDING = SKILL.parent / "gru953-branding"

WROTE, SKIPPED, FAILED = [], [], []


def put(dest: pathlib.Path, content: str | bytes, force: bool, dry: bool) -> None:
    if dest.exists() and not force:
        SKIPPED.append(dest)
        return
    if dry:
        WROTE.append(dest)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        dest.write_bytes(content)
    else:
        dest.write_text(content, encoding="utf-8")
    WROTE.append(dest)


def copy(src: pathlib.Path, dest: pathlib.Path, force: bool, dry: bool) -> None:
    if not src.exists():
        FAILED.append((dest, f"source missing: {src}"))
        return
    put(dest, src.read_bytes(), force, dry)


BRAND_CHECK = r'''#!/usr/bin/env node
// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader (GRU953)
/*
 * GRU953 brand check.
 *
 * Runs over a repository and fails on the mistakes that actually happen. It is
 * deliberately small and dependency-free: a check nobody can read is a check
 * nobody keeps.
 *
 *   node scripts/brand-check.mjs .
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(process.argv[2] || '.');
const SKIP = new Set(['node_modules', '.git', 'dist', 'build', 'vendor', '.next',
                      'coverage', '__pycache__', '.venv']);
const fails = [], notes = [];

function walk(dir, out = []) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (err) {
    // A directory that cannot be read is a finding, not a crash and not a silence.
    fails.push(`${path.relative(ROOT, dir) || '.'} could not be read (${err.code})`);
    return out;
  }
  for (const e of entries) {
    if (e.name.startsWith('.') && e.name !== '.github') continue;
    if (SKIP.has(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

const files = walk(ROOT);
const rel = f => path.relative(ROOT, f);
// null, not '': an unreadable or empty file must be distinguishable from one that
// simply has no matching content, or a zero-byte LICENSE passes the licence gate.
const text = f => { try { return fs.readFileSync(f, 'utf8') } catch { return null } };
// m?js and m?ts included: this checker is itself an .mjs, and so is every ESM file in
// a modern project. Without them it could not see its own defects, or theirs.
const CODE = /\.(css|scss|less|m?js|cjs|jsx|m?ts|cts|tsx|vue|svelte|astro|html)$/i;
const PROSE = /\.(md|markdown|txt|html)$/i;

// 1. the licence files
for (const req of ['LICENSE', 'NOTICE']) {
  if (!fs.existsSync(path.join(ROOT, req))) fails.push(`missing ${req} in the repository root`);
}
const licence = text(path.join(ROOT, 'LICENSE'));
if (fs.existsSync(path.join(ROOT, 'LICENSE')) &&
    !(licence || '').includes('TERMS AND CONDITIONS FOR USE'))
  fails.push('LICENSE is present but is not the Apache-2.0 text');

// 2. the two colour mistakes, and hard-coded brand hex where a token exists
// The note is kept OUT of the token name, so the suggested fix is something that can be
// pasted verbatim. `use var(--gru-accent (dark))` is not valid CSS, and it was what this
// printed for the brand's most common mistake.
const BRAND_HEX = {
  '#1a1753': ['--gru-brand', ''],
  '#b45a39': ['--gru-accent', 'which resolves to this in the light theme'],
  '#ffab8e': ['--gru-accent', 'which resolves to this in the dark theme'],
  '#edb24d': ['--gru-warning', 'Ember also serves as the warning colour'],
  '#0b0e14': ['--gru-ink', ''],
};
const OPT_OUT = 'gru953-review: colours-are-the-subject';
for (const f of files.filter(f => CODE.test(f))) {
  if (/tokens\.(css|json)$/.test(f)) continue;      // the tokens are where hex belongs
  let t = text(f) || '';
  // A document whose SUBJECT is colour has to print colour values. It says so in a
  // marker, the same one gru953-review reads, rather than this file carrying a list of
  // filenames it has to keep in step.
  if (t.includes(OPT_OUT)) continue;
  // An inlined <svg> carries its own artwork, and the app-icon tile in particular has one
  // fixed colourway baked into it by design. That is a mark, not a component naming a
  // colour — gru953-review strips these before scanning and this did not, so any page
  // that inlined the tile failed CI for shipping the tile correctly.
  t = t.replace(/<svg[\s\S]*?<\/svg>/gi, m => '\n'.repeat((m.match(/\n/g) || []).length));
  t.split('\n').forEach((ln, i) => {
    const low = ln.toLowerCase();
    // A hex written NEXT TO the token that replaces it is a lookup table or a comment
    // explaining the rule — the shape of every tool that maps one to the other, including
    // this file. Flagging it asks a checker to describe its own rule without naming the
    // value the rule is about, and made every scaffolded repo fail its own check.
    if (low.includes('--gru-') || /^\s*(\/\/|\/\*|\*|#|<!--)/.test(ln)) return;
    for (const [hex, [tok, note]] of Object.entries(BRAND_HEX)) {
      if (low.includes(hex))
        fails.push(`${rel(f)}:${i + 1} hard-coded ${hex} — use var(${tok})` +
                   (note ? `, ${note}` : ''));
    }
  });
}
// The "#FFAB8E on a light ground" rule used to test the WHOLE FILE for a light background,
// so a stylesheet that correctly confined the dark accent to a [data-theme="dark"] block
// AND set a light page background failed CI on correct code, with a ratio that did not
// apply to the line it named. The hard-coded-hex rule above already covers every one of
// these lines, so the second, sometimes-false message is gone.

// 3. the bare bird below its 24px floor
for (const f of files.filter(f => CODE.test(f))) {
  const t = text(f);
  // matchAll, not match: without /g this inspected only the FIRST bird reference in a
  // file and missed every later one. And the unit is checked, because `width:1.5rem` is
  // 24px and correct, while `(\d+)` alone read it as 1px.
  const re = /GRU953-bird\.svg[\s\S]{0,240}?(?:width|height)\s*[:=]\s*["']?(\d+(?:\.\d+)?)\s*(px|rem|em|%|vw|vh|pt)?/gi;
  for (const m of (t || '').matchAll(re)) {
    if (m[2] && m[2].toLowerCase() !== 'px') continue;
    if (Number(m[1]) < 24)
      fails.push(`${rel(f)} renders the bare bird at ${m[1]}px — below 24px use GRU953-appicon.svg`);
  }
}

// 4. the name, spelled wrong, in prose
//
// Run over VISIBLE text, not raw markup — the same treatment gru953-review gives it. A
// guidebook that lists the forbidden spellings in an HTML table was failing this check
// for teaching the rule, because `<td>Gru953</td>` is not a markdown table row and the
// cell guard never fired.
const visibleText = s => s
  .replace(/<(style|script|svg|pre|code)\b[\s\S]*?<\/\1>/gi,
           m => '\n'.repeat((m.match(/\n/g) || []).length))
  .replace(/<\/(td|th)>/gi, ' | ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/[ \t]{2,}/g, ' ');
for (const f of files.filter(f => PROSE.test(f))) {
  const raw = text(f) || '';
  (/\.html?$/i.test(f) ? visibleText(raw) : raw).split('\n').forEach((ln, i) => {
    // Backticked, quoted, in a two-column "wrong | right" row, or on a line that also
    // carries the correct spelling: that is a mention, not a lapse. A style guide must be
    // able to write down the thing it forbids.
    const bare = ln.replace(/`[^`]*`/g, '\u2423');
    const inCell = (ln.match(/\|/g) || []).length >= 2 || /\|\s*$/.test(ln);
    const alsoCorrect = /GRU953/.test(ln.replace(/\b(Gru953|GRU 953|gru-953|GRU_953)\b/g, ''));
    // Quoted, it is a mention. A style guide has to be able to write down what it forbids.
    const quoted = /["\u201c\u201d\u2018\u2019][^"\u201c\u201d\u2018\u2019]{0,20}\b(Gru953|GRU 953|gru-953|GRU_953)\b/.test(ln);
    // GRU-953 after a slash or an @ is the GitHub handle, which is spelled that way.
    const handle = /[/@]GRU-953\b/.test(ln);
    if (/\b(Gru953|GRU 953|gru-953|GRU_953)\b/.test(bare) && !inCell && !alsoCorrect &&
        !quoted && !handle &&
        !/never|\bnot\b|wrong|avoid|incorrect|don.t|instead/i.test(ln))
      fails.push(`${rel(f)}:${i + 1} the name is GRU953 — one word, uppercase, no hyphen`);
  });
}

// 5. calling PolyForm content open source
const readme = text(path.join(ROOT, 'README.md'));
// A line that says "source-available, NOT open source" is teaching the rule, not
// breaking it. Only an unqualified claim counts.
if (fs.existsSync(path.join(ROOT, 'LICENSE-GUIDEBOOK.md'))) {
  // The qualification may sit on the line ABOVE or BELOW: prose wraps, so
  // "source-available, not open" and "source" routinely land on different lines. Judging
  // one line at a time reported a README that states the distinction correctly as a
  // README that blurs it. gru953-review already used a two-line window; this now matches.
  const rl = (readme || '').split('\n');
  const claims = rl.filter((ln, i) =>
    /open[- ]source/i.test(ln) &&
    !/not\s+open[- ]source|source-available|rather than open|never\b|Apache|OSI|Open Source Definition|Open Source Initiative/i
      .test(rl.slice(Math.max(0, i - 2), i + 3).join(' ')));
  if (claims.length)
    fails.push('README.md calls this open source while shipping PolyForm content — ' +
               'PolyForm Noncommercial is source-available, not open source: ' +
               JSON.stringify(claims[0].trim().slice(0, 80)));
}

// 6. the taglines, if either appears, must be complete
if (/Simple technology/i.test(readme || '') &&
    !(readme || '').includes('Simple technology. For everyone.'))
  fails.push('README.md has a shortened English tagline — it is locked and used complete');
if (/সহজ প্রযুক্তি/.test(readme || '') &&
    !(readme || '').includes('সহজ প্রযুক্তি। সবার জন্য।'))
  fails.push('README.md has a shortened Bangla tagline — it is locked and used complete');

// 7. things worth a look, not a failure
if (readme && !/^#{1,2} /m.test(readme)) notes.push('README.md has no heading');
// Determinism: readdirSync does not promise an order, so two machines could report the
// same repository's problems in different sequences. Sorting makes the output comparable.
fails.sort(); notes.sort();
if (!fs.existsSync(path.join(ROOT, '.github/social-preview.png')))
  notes.push('no .github/social-preview.png — GitHub shows a generic card without it');

console.log(`GRU953 brand check — ${files.length} files under ${ROOT}`);
for (const n of notes) console.log(`  ! ${n}`);
if (!fails.length) { console.log('  PASS'); process.exit(0); }
console.log(`\nFAILED — ${fails.length} problem(s):`);
for (const f of fails) console.log(`  ✗ ${f}`);
process.exit(1);
'''


def build_notice(name: str, writing: bool) -> str:
    """The NOTICE this repository actually needs, with nothing in it that is not here."""
    year = datetime.date.today().year
    prose = f"""
--------------------------------------------------------------------------------
2. THE WRITING — PolyForm Noncommercial License 1.0.0
--------------------------------------------------------------------------------
The GRU953 long-form writing shipped in this repository.

Required Notice: Copyright {year} Aninda Sundar Howlader (GRU953)

   Licensed under the PolyForm Noncommercial License 1.0.0. You may use, copy,
   modify and share it for any noncommercial purpose. Commercial use requires
   separate permission from the licensor.

       https://polyformproject.org/licenses/noncommercial/1.0.0

The full text is in LICENSE-GUIDEBOOK.md.

PolyForm Noncommercial 1.0.0 is a source-available licence. It is NOT approved by
the Open Source Initiative, because it restricts commercial use. That is stated
plainly rather than glossed over.
""" if writing else ""
    return f"""{name}
Copyright {year} Aninda Sundar Howlader (GRU953)

সহজ প্রযুক্তি। সবার জন্য।
Simple technology. For everyone.

--------------------------------------------------------------------------------
1. THE CODE — Apache License, Version 2.0
--------------------------------------------------------------------------------
   Licensed under the Apache License, Version 2.0 (the "License"); you may not use
   these files except in compliance with the License. You may obtain a copy of the
   License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software distributed
   under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied. See the License for the
   specific language governing permissions and limitations under the License.

The full text is in LICENSE.
{prose}
--------------------------------------------------------------------------------
{"3" if writing else "2"}. THE GRU953 MARKS — not licensed
--------------------------------------------------------------------------------
The name GRU953, the GRU953 wordmark, the Soaring Bird, the app-icon tile, and any
lockup of them are trademarks of Aninda Sundar Howlader. They are NOT licensed by
the licence above. Apache-2.0 section 6 expressly withholds trademark permission.

Without asking anyone:
  · You MAY fork this repository, change it, and ship what you build with it.
  · You MAY show the marks to refer to GRU953 — a credit, a comparison, an article.
  · You MAY NOT put the marks on your own product, or on a fork, as if it were GRU953.
  · You MAY NOT use a name confusable with GRU953 for a competing tool.

Replace the identity with your own and everything else here is yours to use.

--------------------------------------------------------------------------------

This file is the NOTICE file required by section 4(d) of the Apache License, Version
2.0. If you redistribute this work, this file must travel with it.

Permissions and questions: aninda.sh15@gmail.com

This is not legal advice. It was written by the author, who is not a lawyer.
"""


def main() -> None:
    p = argparse.ArgumentParser(description="Set a GRU953 repository up.")
    p.add_argument("--dir", default=".", help="where to write (default: here)")
    p.add_argument("--name", help="the product's own name, e.g. Ledger")
    p.add_argument("--what", help="one plain sentence saying what it does")
    p.add_argument("--writing", action="store_true",
                   help="also add LICENSE-GUIDEBOOK.md (the repo ships GRU953 prose)")
    p.add_argument("--web", action="store_true",
                   help="also add the icon set and styles/tokens.css")
    p.add_argument("--force", action="store_true", help="overwrite existing files")
    p.add_argument("--dry-run", action="store_true", help="print, write nothing")
    a = p.parse_args()

    root = pathlib.Path(a.dir).resolve()
    if not root.exists():
        sys.exit(f"FAIL — {root} does not exist. Create it first.")
    if not root.is_dir():
        sys.exit(f"FAIL — {root} is a file, not a directory.")
    dry, force = a.dry_run, a.force

    # Everything this script needs to READ is checked before anything is WRITTEN. The
    # README template used to be read after LICENSE and NOTICE were already on disk, so a
    # missing template left a half-set-up repository, a bare traceback, and none of the
    # guidance that tells the user what to do next.
    sources = [LICENCES / "LICENSE", SKILL / "assets/README.template.md"]
    if a.writing:
        sources.append(LICENCES / "LICENSE-GUIDEBOOK.md")
    missing = [str(s) for s in sources if not s.exists()]
    if missing:
        sys.exit("FAIL — this skill is incomplete; nothing was written.\n  missing: "
                 + "\n           ".join(missing))

    # 1-3. the licences, verbatim and never edited
    copy(LICENCES / "LICENSE", root / "LICENSE", force, dry)
    # The NOTICE is BUILT for this repository, not copied. The shipped template was the
    # brand kit's own: every generated repo got a file headed "GRU953 Brand Kit" whose
    # trademark clause delegated to TRADEMARKS.md and LOGO-USAGE.md — neither of which is
    # ever created — and which described five bundled typefaces that are not there. A
    # section 4(d) notice whose trademark reservation dead-ends is misleading in the
    # legally operative direction, which is the one that matters.
    put(root / "NOTICE", build_notice(a.name or "This project", a.writing), force, dry)
    if a.writing:
        copy(LICENCES / "LICENSE-GUIDEBOOK.md", root / "LICENSE-GUIDEBOOK.md", force, dry)

    # 4. the README
    tpl = (SKILL / "assets/README.template.md").read_text(encoding="utf-8")
    name = a.name or "GRU953"
    tpl = tpl.replace("[NAME]", name).replace("[YEAR]", str(datetime.date.today().year))
    if a.what:
        tpl = tpl.replace(
            "**[One plain sentence saying what this is and who it is for. No adjectives, "
            "no tagline, no hype. If a stranger reads only this line, they should know "
            "whether to keep reading.]**",
            f"**{name} {a.what}.**")
    if not a.writing:
        # do not point at a licence file the repository does not have
        tpl = "\n".join(
            ln for ln in tpl.splitlines()
            if "LICENSE-GUIDEBOOK.md" not in ln and "Written content:" not in ln
            and "**লেখা:**" not in ln)
    if not BRANDING.exists():
        # ...and do not point at banner images this run cannot create either. The template
        # shipped a <picture> block referencing two files that init.py had just reported it
        # could not produce, so the README arrived with a broken image and nothing said so.
        tpl = re.sub(r"<picture>[\s\S]*?</picture>\n?", "", tpl)
    put(root / "README.md", tpl, force, dry)

    # 5-6. the artwork and the icons
    #
    # These live in the SIBLING skill. If only gru953-repo was installed, they are simply
    # not there — and a script that quietly skips half its job is worse than one that fails,
    # because the repository looks finished. So the dependency is reported, once, loudly.
    if not BRANDING.exists():
        FAILED.append((root / ".github/",
                       "the gru953-branding skill is not installed beside this one, so the "
                       "social preview, the README banners and the icon set were skipped. "
                       "Install the whole gru953 plugin, or copy gru953-branding next to "
                       "gru953-repo, then run this again."))
    art = BRANDING / "assets/artwork"
    for src, dest in (("github-social-preview.png", ".github/social-preview.png"),
                      ("readme-header-light.png", ".github/readme-header-light.png"),
                      ("readme-header-dark.png", ".github/readme-header-dark.png"),
                      ("og-card-1200x630.png", ".github/og-card.png"),
                      ("avatar-512.png", ".github/avatar-512.png")):
        if (art / src).exists():
            copy(art / src, root / dest, force, dry)
    # Every artwork file is named, so a missing one is reported rather than skipped in
    # silence. `--web` used to exit 0 having written no .github/ at all.
    for src, dest in (("github-social-preview.png", ".github/social-preview.png"),
                      ("readme-header-light.png", ".github/readme-header-light.png"),
                      ("readme-header-dark.png", ".github/readme-header-dark.png"),
                      ("og-card-1200x630.png", ".github/og-card.png"),
                      ("avatar-512.png", ".github/avatar-512.png")):
        if BRANDING.exists() and not (art / src).exists():
            FAILED.append((root / dest,
                           f"{art / src} is missing from the gru953-branding skill"))

    asset_py = BRANDING / "scripts/asset.py"
    ICONS = ("favicon.ico", "icon.svg", "mask-icon.svg", "apple-touch-icon.png",
             "favicon-16.png", "favicon-32.png", "favicon-48.png", "favicon-64.png",
             "favicon-128.png", "favicon-256.png")
    if a.web:
        if not asset_py.exists():
            FAILED.append((root / "public",
                           "gru953-branding/scripts/asset.py is not installed, so the "
                           "icon set was skipped"))
        elif (root / "public/icon.svg").exists() and not force:
            # The one thing this script used to overwrite unconditionally, in a file whose
            # docstring, SKILL.md and command all promise it never overwrites silently.
            # Tested BEFORE the dry-run branch, so a dry run on a repository that already
            # has an icon set reports "kept" — which is what a real run does. Tested after
            # it, the dry run promised ten files a real run would not have written.
            SKIPPED.append(root / "public/ (icon set)")
        elif dry:
            # A dry run has to list what a real run would write, or the list the user
            # approves is not the list they get. These ten were missing from it.
            for n in ICONS:
                WROTE.append(root / "public" / n)
        else:
            try:
                subprocess.run([sys.executable, str(asset_py), "favicons",
                                "-o", str(root / "public")], check=True, capture_output=True)
                for n in ICONS:
                    if (root / "public" / n).exists():
                        WROTE.append(root / "public" / n)
            except subprocess.CalledProcessError as e:
                FAILED.append((root / "public", e.stderr.decode()[:120]))

    # 7. the tokens and the check
    if a.web:
        copy(BRANDING / "assets/tokens.css", root / "styles/tokens.css", force, dry)
    put(root / "scripts/brand-check.mjs", BRAND_CHECK, force, dry)

    # ------------------------------------------------------------------ report
    tag = "would write" if dry else "wrote"
    print(f"GRU953 repository setup — {root}\n")
    for f in WROTE:
        print(f"  + {tag}   {f.relative_to(root) if f.is_relative_to(root) else f}")
    for f in SKIPPED:
        print(f"  = kept    {f.relative_to(root)}  (already there; --force to replace)")
    # The steps come BEFORE the failures, so the failures are the last thing on screen.
    # A step that tells the user to upload a file this run could not create is worse than
    # no step at all, so a step whose artefact is missing is not printed.
    have_preview = (root / ".github/social-preview.png").exists() or (dry and BRANDING.exists())
    steps = [
        'Fill in every [bracketed] slot in README.md. The first line must say what\n'
        '     this is — to a developer audience "GRU" already reads as Gated Recurrent Unit.',
        "Write the Bangla half as an original, not a translation.",
        "node scripts/brand-check.mjs .",
        "Push to a PRIVATE repository first. Look at it as a stranger would.",
    ]
    if have_preview:
        steps.append("GitHub -> Settings -> Social preview -> upload "
                     ".github/social-preview.png")
    steps.append("Make it public as a separate, deliberate step.")
    print("\nNext, in order:\n")
    for i, s in enumerate(steps, 1):
        print(f"  {i}. {s}")
    if FAILED:
        print("\nNOT DONE — this run could not finish everything:")
        for f, why in FAILED:
            rel = f.relative_to(root) if f.is_relative_to(root) else f
            print(f"  ! {rel}\n      {why}")
        sys.exit(1)


if __name__ == "__main__":
    main()
