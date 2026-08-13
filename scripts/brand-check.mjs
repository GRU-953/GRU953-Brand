#!/usr/bin/env node
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
