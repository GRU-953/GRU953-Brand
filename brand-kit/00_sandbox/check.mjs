// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader (GRU953)
/*
 * GRU953 — the guidebook's browser-side check.
 *
 * verify.py checks the files. This checks the BUILT PAGE, in a real browser, because a
 * guidebook can pass every file-level test and still overflow on a phone, throw a script
 * error, or fail to switch theme. Three viewports, both themes, and a horizontal-overflow
 * sweep that names the offending element rather than just saying "something is too wide".
 *
 * Run:  cd 00_sandbox && node check.mjs ../08_guidebook/GRU953-Brand-Guidebook.html
 */
import { browser } from './render.mjs';
import path from 'node:path';

const file = path.resolve(process.argv[2] || '../08_guidebook/GRU953-Brand-Guidebook.html');
const b = await browser();
const fails = [], notes = [];

// Words that must not survive anywhere in the rendered text. Each one is either a
// superseded edition, a deleted mark build, or a licence the kit no longer uses.
const FORBIDDEN = ['bird-detail', 'bird-core', 'bird-glyph', 'LOCKED-SPEC',
                   'CC BY 4.0', 'MIGRATING', 'v5-tokens'];
const TAG_EN = 'Simple technology. For everyone.';
const TAG_BN = 'সহজ প্রযুক্তি। সবার জন্য।';

for (const [label, width, height, scheme] of [
  ['desktop-light', 1440, 900, 'light'],
  ['desktop-dark', 1440, 900, 'dark'],
  ['tablet-light', 834, 1112, 'light'],
  ['phone-light', 390, 844, 'light'],
  ['phone-dark', 360, 740, 'dark'],
  ['tiny', 320, 640, 'light'],
]) {
  const p = await b.newPage({ viewport: { width, height }, colorScheme: scheme });
  const errs = [];
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await p.goto('file://' + file, { waitUntil: 'load', timeout: 240000 });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1800);

  const r = await p.evaluate(({ width, FORBIDDEN, TAG_EN, TAG_BN }) => {
    // Reveal everything: the scroll-reveal animation hides sections that are off-screen,
    // and an element cannot be measured for overflow while it is hidden.
    document.documentElement.classList.remove('js-anim');
    document.querySelectorAll('.reveal').forEach(e => e.classList.add('in'));
    document.querySelectorAll('details').forEach(d => (d.open = true));
    // An element is only a problem if nothing CLIPS it. A wide table inside a box with
    // overflow-x:auto is scrolled, not broken — that is the intended design, and counting
    // it as a failure would make the check cry wolf on the one thing that was done right.
    const clipped = el => {
      for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
        const ox = getComputedStyle(a).overflowX;
        if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') return true;
      }
      return false;
    };
    const over = [];
    for (const el of document.querySelectorAll('body *')) {
      const rect = el.getBoundingClientRect();
      if (rect.width === 0) continue;
      if (el.classList.contains('skip')) continue;   // parked at left:-9999px on purpose
      if (rect.right > width + 1.5 || rect.left < -1.5) {
        if (clipped(el)) continue;
        const p = el.parentElement;
        // Report the outermost offender only; a wide table drags every cell with it.
        if (p && (p.getBoundingClientRect().right > width + 1.5)) continue;
        over.push(`${el.tagName.toLowerCase()}.${el.className || ''}`.slice(0, 70)
                  + ` -> ${Math.round(rect.right)}px`);
      }
    }
    const txt = document.body.innerText;
    return {
      chapters: document.querySelectorAll('section.ch').length,
      docWidth: document.documentElement.scrollWidth,
      overflow: [...new Set(over)].slice(0, 8),
      forbidden: FORBIDDEN.filter(w => txt.includes(w)),
      tagEN: (txt.match(new RegExp(TAG_EN.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length,
      tagBN: (txt.match(new RegExp(TAG_BN, 'g')) || []).length,
      bg: getComputedStyle(document.body).backgroundColor,
      accent: getComputedStyle(document.documentElement).getPropertyValue('--gru-accent').trim(),
      downloads: document.querySelectorAll('a.dl[download]').length,
      unlabelled: [...document.querySelectorAll('a.dl')].filter(a => !a.getAttribute('aria-label')).length,
      imgsNoAlt: [...document.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).length,
      svgsNoLabel: [...document.querySelectorAll('svg')]
        .filter(s => !s.querySelector('title') && !s.getAttribute('aria-label')
                     && s.getAttribute('aria-hidden') !== 'true').length,
    };
  }, { width, FORBIDDEN, TAG_EN, TAG_BN });

  const line = [];
  if (errs.length) fails.push(`${label}: ${errs.length} console/page error(s): ${errs[0]}`);
  if (r.docWidth > width + 2) fails.push(`${label}: page scrolls sideways (${r.docWidth}px > ${width}px)`);
  if (r.overflow.length) fails.push(`${label}: ${r.overflow.length} element(s) overflow: ${r.overflow.join(' | ')}`);
  if (r.forbidden.length) fails.push(`${label}: forbidden text present: ${r.forbidden.join(', ')}`);
  if (r.tagEN < 3) fails.push(`${label}: English tagline appears only ${r.tagEN} times`);
  if (r.tagBN < 3) fails.push(`${label}: Bangla tagline appears only ${r.tagBN} times`);
  if (r.unlabelled) fails.push(`${label}: ${r.unlabelled} download link(s) with no accessible name`);
  if (r.imgsNoAlt) fails.push(`${label}: ${r.imgsNoAlt} image(s) with no alt attribute`);
  if (r.svgsNoLabel) notes.push(`${label}: ${r.svgsNoLabel} svg(s) with neither <title> nor aria-hidden`);
  line.push(`chapters ${r.chapters}`, `downloads ${r.downloads}`,
            `accent ${r.accent}`, `body ${r.bg}`);
  console.log(`${label.padEnd(15)} ${line.join('  ·  ')}`);
  await p.close();
}

// theme switching actually changes something
{
  const p = await b.newPage({ viewport: { width: 1280, height: 800 }, colorScheme: 'light' });
  await p.goto('file://' + file, { waitUntil: 'load', timeout: 240000 });
  await p.waitForTimeout(1200);
  const before = await p.evaluate(() => getComputedStyle(document.body).backgroundColor);
  await p.click('#theme'); await p.waitForTimeout(300);
  await p.click('#theme'); await p.waitForTimeout(500);
  const after = await p.evaluate(() => ({
    bg: getComputedStyle(document.body).backgroundColor,
    attr: document.documentElement.getAttribute('data-theme'),
  }));
  if (before === after.bg) fails.push(`theme button does not change the page (${before})`);
  console.log(`theme switch    ${before} -> ${after.bg} (data-theme=${after.attr})`);
  // the language toggle must hide Bangla and put it back
  const n0 = await p.evaluate(() => document.body.innerText.length);
  await p.click('#lang'); await p.waitForTimeout(400);
  const n1 = await p.evaluate(() => document.body.innerText.length);
  await p.click('#lang'); await p.waitForTimeout(400);
  const n2 = await p.evaluate(() => document.body.innerText.length);
  if (!(n1 < n0)) fails.push('the EN-only toggle does not hide anything');
  if (Math.abs(n2 - n0) > 40) fails.push('the language toggle does not restore the page');
  console.log(`lang toggle     ${n0} -> ${n1} -> ${n2} characters`);
  await p.close();
}

await b.close();
console.log('\n' + '='.repeat(78));
if (notes.length) { console.log('LOOK AT BY HAND:'); notes.forEach(n => console.log('  ! ' + n)); }
if (fails.length) {
  console.log(`FAILED — ${fails.length} problem(s):`);
  fails.forEach(f => console.log('  ✗ ' + f));
  process.exit(1);
}
console.log('PASS — the built guidebook holds up in a real browser, at every width, in both themes.');
