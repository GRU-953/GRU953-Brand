// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader (GRU953)
/*
 * GRU953 — outreach art generator.
 * Renders the profile and social artwork at exact platform pixel sizes via headless
 * Chromium, so what ships is what was designed. Re-run to regenerate everything.
 */
import { browser } from '../00_sandbox/render.mjs';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Derived from this file's own location, not hardcoded: the kit has to keep working after
// somebody copies it somewhere else, which is the whole point of shipping the scripts.
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(ROOT, '06_assets/outreach');
fs.mkdirSync(OUT, { recursive: true });

// READ from the generated tokens, not typed. This script paints raster artwork, so it
// cannot use a CSS custom property — but four hex values typed into a second file are
// four values that go stale the first time the palette moves, and nothing would say so.
const TOKENS = JSON.parse(
  fs.readFileSync(path.join(ROOT, '08_guidebook/assets/tokens.json'), 'utf8'));
const MERIDIAN = TOKENS.families.meridian.anchor;
const DAYBREAK = TOKENS.families.daybreak.anchor;
const EMBER    = TOKENS.families.ember.anchor;
const INK      = TOKENS.ground.ink;
for (const [n, v] of Object.entries({ MERIDIAN, DAYBREAK, EMBER, INK })) {
  if (!/^#[0-9A-F]{6}$/i.test(v || '')) throw new Error(`tokens.json has no ${n}`);
}
const svg = f => fs.readFileSync(path.join(ROOT, '03_logo', f), 'utf8')
 .replace(/<svg /, '<svg preserveAspectRatio="xMidYMid meet" ');

// There is ONE bird. Every piece of artwork below embeds the same file.
const BIRD = svg('GRU953-bird.svg');
const LOCKUP_H = svg('GRU953-lockup-horizontal.svg');
const LOCKUP_S = svg('GRU953-lockup-stacked.svg');

// The palette is read from the generated tokens, never retyped. If a colour changes in
// 04_colour/engine.py it changes here too, and the poster cannot go stale.
const TOK = JSON.parse(fs.readFileSync(path.join(ROOT, '08_guidebook/assets/tokens.json'), 'utf8'));
const ACC_LIGHT = TOK.accent.light, ACC_DARK = TOK.accent.dark;

const FONTS = `
@font-face{font-family:D;src:url("file://${ROOT}/08_guidebook/assets/fonts/sora-latin.woff2") format("woff2");font-weight:100 800}
@font-face{font-family:T;src:url("file://${ROOT}/08_guidebook/assets/fonts/notosans-latin.woff2") format("woff2");font-weight:100 900}
@font-face{font-family:T;src:url("file://${ROOT}/08_guidebook/assets/fonts/notosansbengali.woff2") format("woff2");font-weight:100 900;unicode-range:U+0980-09FE,U+200C-200D,U+25CC}
@font-face{font-family:M;src:url("file://${ROOT}/08_guidebook/assets/fonts/jetbrainsmono-latin.woff2") format("woff2");font-weight:100 800}`;

const BASE = `${FONTS}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:T,sans-serif;overflow:hidden}
.stage{position:relative;overflow:hidden;display:flex}
.d{font-family:D,sans-serif;font-weight:700;letter-spacing:-.022em}
.m{font-family:M,monospace;font-weight:600;letter-spacing:.11em;text-transform:uppercase}
.bn{line-height:1.75}
/* The signature 'first light' gradient, plus a soft glow where the light breaks. */
.sky{background:${MERIDIAN};position:relative}
.sky::before{content:"";position:absolute;inset:0;
  background:radial-gradient(120% 105% at 4% 108%, ${DAYBREAK}55 0%, ${EMBER}33 24%, transparent 58%)}
.sky::after{content:"";position:absolute;inset:0;opacity:.5;
  background:repeating-linear-gradient(0deg,#ffffff09 0 1px,transparent 1px 4px)}
.z{position:relative;z-index:2}
svg{display:block;width:100%;height:auto}`;

/* Each entry is one deliverable: exact pixel size, and the markup that fills it. */
const ART = [
  {
    file: 'github-social-preview.png', w: 1280, h: 640,
    why: 'GitHub repository social preview card. GitHub specifies 1280x640.',
    html: `<div class="stage sky" style="width:1280px;height:640px;align-items:center">
      <div class="z" style="padding:0 92px;width:100%">
        <div style="display:flex;align-items:center;gap:34px">
          <div style="color:${DAYBREAK};width:150px">${BIRD}</div>
          <div>
            <div class="d" style="font-size:88px;color:#fff;line-height:1">GRU953</div>
            <div class="m" style="font-size:19px;color:${DAYBREAK};margin-top:14px">Simple technology. For everyone.</div>
          </div>
        </div>
        <div class="bn" style="margin-top:46px;font-size:38px;color:#E6EBFF;max-width:900px">সহজ প্রযুক্তি। সবার জন্য।</div>
        <div style="margin-top:34px;display:flex;gap:12px">
          ${['Simple by design', 'For everyone', 'Honest craft'].map(t =>
            `<span class="m" style="font-size:14px;color:#fff;border:1.5px solid #ffffff40;padding:9px 17px;border-radius:99px">${t}</span>`).join('')}
        </div>
      </div>
    </div>`,
  },
  {
    file: 'avatar-512.png', w: 512, h: 512,
    why: 'Profile avatar for GitHub, LinkedIn and X. Square; renders as a circle on most platforms, so the mark is kept well inside a safe circle.',
    html: `<div class="stage sky" style="width:512px;height:512px;align-items:center;justify-content:center">
      <div class="z" style="color:${DAYBREAK};width:270px">${BIRD}</div>
    </div>`,
  },
  {
    file: 'x-header-1500x500.png', w: 1500, h: 500,
    why: 'X / Twitter profile header. X specifies 1500x500 and crops the edges on small screens, so nothing important sits within 90px of any edge.',
    html: `<div class="stage sky" style="width:1500px;height:500px;align-items:center">
      <div class="z" style="padding:0 130px;display:flex;align-items:center;gap:44px;width:100%">
        <div style="color:${DAYBREAK};width:118px;flex:none">${BIRD}</div>
        <div style="flex:1">
          <div class="d" style="font-size:62px;color:#fff;line-height:1.02">Simple technology.<br>For everyone.</div>
          <div class="m" style="font-size:15px;color:${EMBER};margin-top:20px">GRU953 &nbsp;·&nbsp; solo developer &nbsp;·&nbsp; Bangladesh</div>
        </div>
      </div>
    </div>`,
  },
  {
    file: 'linkedin-banner-1584x396.png', w: 1584, h: 396,
    why: 'LinkedIn profile banner. LinkedIn specifies 1584x396 and overlays the profile photo on the lower left, so that area is deliberately left empty.',
    html: `<div class="stage sky" style="width:1584px;height:396px;align-items:center;justify-content:flex-end">
      <div class="z" style="padding:0 96px 0 560px;text-align:right;width:100%">
        <div class="d" style="font-size:52px;color:#fff;line-height:1.05">Simple technology. For everyone.</div>
        <div class="bn" style="font-size:24px;color:${DAYBREAK};margin-top:16px">সহজ প্রযুক্তি। সবার জন্য।</div>
        <div class="m" style="font-size:14px;color:#C3CBFF;margin-top:22px">Aninda Sundar Howlader &nbsp;·&nbsp; GRU953</div>
      </div>
      <div class="z" style="position:absolute;right:70px;top:-40px;color:#ffffff14;width:330px">${BIRD}</div>
    </div>`,
  },
  {
    file: 'readme-header-light.png', w: 1600, h: 300,
    why: 'README banner for the light GitHub theme. Rendered at 1600px so it stays crisp on a high-density display when shown at 800px.',
    html: `<div class="stage" style="width:1600px;height:300px;background:#fff;align-items:center;border-bottom:6px solid ${MERIDIAN}">
      <div style="padding:0 72px;display:flex;align-items:center;justify-content:space-between;width:100%">
        <div style="color:${MERIDIAN};width:520px">${LOCKUP_H}</div>
        <div style="text-align:right">
          <div class="d" style="font-size:31px;color:${MERIDIAN}">Simple technology. For everyone.</div>
          <div class="bn" style="font-size:22px;color:#4C4EAD;margin-top:9px">সহজ প্রযুক্তি। সবার জন্য।</div>
        </div>
      </div>
    </div>`,
  },
  {
    file: 'readme-header-dark.png', w: 1600, h: 300,
    why: 'README banner for the dark GitHub theme. Pairs with the light version via a <picture> element so the banner follows the reader\'s theme.',
    html: `<div class="stage sky" style="width:1600px;height:300px;align-items:center;border-bottom:6px solid ${DAYBREAK}">
      <div class="z" style="padding:0 72px;display:flex;align-items:center;justify-content:space-between;width:100%">
        <div style="color:${DAYBREAK};width:520px">${LOCKUP_H}</div>
        <div style="text-align:right">
          <div class="d" style="font-size:31px;color:#fff">Simple technology. For everyone.</div>
          <div class="bn" style="font-size:22px;color:${DAYBREAK};margin-top:9px">সহজ প্রযুক্তি। সবার জন্য।</div>
        </div>
      </div>
    </div>`,
  },
  {
    file: 'og-card-1200x630.png', w: 1200, h: 630,
    why: 'Open Graph / Twitter Card image for the portfolio site. 1200x630 is the size Facebook, LinkedIn and Slack all render well.',
    html: `<div class="stage sky" style="width:1200px;height:630px;align-items:flex-end">
      <div class="z" style="padding:76px;width:100%">
        <div style="color:${DAYBREAK};width:120px;margin-bottom:38px">${BIRD}</div>
        <div class="d" style="font-size:76px;color:#fff;line-height:1.03;max-width:900px">Simple technology.<br>For everyone.</div>
        <div style="margin-top:30px;display:flex;align-items:baseline;gap:20px">
          <span class="d" style="font-size:27px;color:${DAYBREAK}">GRU953</span>
          <span class="m" style="font-size:15px;color:#B7C1FF">solo software studio · Bangladesh</span>
        </div>
      </div>
    </div>`,
  },
  {
    file: 'palette-poster.png', w: 1400, h: 900,
    why: 'A one-page palette reference, for pinning up or dropping into a slide.',
    html: `<div class="stage" style="width:1400px;height:900px;background:#fff;flex-direction:column">
      <div style="padding:48px 64px 22px">
        <div class="m" style="font-size:14px;color:#6C7280">GRU953 · signature palette</div>
        <div class="d" style="font-size:52px;color:${MERIDIAN};margin-top:12px">The deep sky, and the light that breaks over it</div>
        <div style="font-size:19px;color:#4A4F5C;margin-top:12px;max-width:1080px;line-height:1.45">The signature is one hue with two tuned values. No single colour can clear 4.5:1 against both white and near-black, so Daybreak is a deep step on light grounds and a pale one on dark ones.</div>
      </div>
      <div style="display:flex;flex:1;gap:0">
        ${[['Meridian', 'মেরিডিয়ান', MERIDIAN, '#fff', 'The deep sky. The ground.'],
           ['Daybreak · light', 'ভোরের আলো', ACC_LIGHT, '#fff', 'The signature on light grounds.'],
           ['Daybreak · dark', 'ভোরের আলো', ACC_DARK, INK, 'The same hue, on dark grounds.'],
           ['Ember', 'অঙ্গার', EMBER, INK, 'Warm mid-tone. Support, and warnings.'],
           ['Ink', 'কালি', INK, '#fff', 'Dark ground, body text.']]
 .map(([n, bn, hex, fg, note]) => `
          <div style="flex:1;background:${hex};color:${fg};padding:36px 30px;display:flex;flex-direction:column;justify-content:flex-end">
            <div class="d" style="font-size:34px">${n}</div>
            <div class="bn" style="font-size:20px;opacity:.85;margin-top:4px">${bn}</div>
            <div class="m" style="font-size:15px;margin-top:16px">${hex}</div>
            <div style="font-size:15px;opacity:.8;margin-top:8px;line-height:1.4">${note}</div>
          </div>`).join('')}
      </div>
      <div style="padding:26px 64px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid #E6EBFF">
        <div class="m" style="font-size:13px;color:#6C7280">Daybreak on paper ${TOK.accent.light_ratio_on_paper}:1 &nbsp;·&nbsp; Daybreak on ink ${TOK.accent.dark_ratio_on_ink}:1 &nbsp;·&nbsp; every ratio computed, see CONTRAST.md</div>
        <div style="color:${MERIDIAN};width:150px">${LOCKUP_H}</div>
      </div>
    </div>`,
  },
];

// The Chromium path is discovered by 00_sandbox/render.mjs rather than hardcoded here.
const b = await browser();
const manifest = [];
for (const a of ART) {
  const p = await b.newPage({ viewport: { width: a.w, height: a.h }, deviceScaleFactor: 1 });
  await p.setContent(`<meta charset="utf-8"><style>${BASE}</style>${a.html}`);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(280);
  const dest = path.join(OUT, a.file);
  await p.locator('.stage').screenshot({ path: dest });
  await p.close();
  const kb = (fs.statSync(dest).size / 1024).toFixed(1);
  manifest.push({ file: a.file, size: `${a.w}x${a.h}`, kB: +kb, purpose: a.why });
  console.log(`${a.file.padEnd(34)} ${String(a.w + 'x' + a.h).padEnd(11)} ${kb} kB`);
}
await b.close();
fs.writeFileSync(path.join(OUT, 'MANIFEST.json'), JSON.stringify(manifest, null, 2));
console.log(`\n${manifest.length} files -> 06_assets/outreach/`);
