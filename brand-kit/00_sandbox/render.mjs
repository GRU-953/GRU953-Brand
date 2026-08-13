// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader (GRU953)
/*
 * GRU953 brand-kit render helper: HTML -> PNG / PDF.
 *
 * The Chromium path is DISCOVERED, not hardcoded. It used to name one exact Playwright
 * build directory, so the whole kit stopped rendering the moment Playwright updated — with
 * an ENOENT that said nothing about why.
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

function findChrome() {
  // 1. an explicit override always wins
  if (process.env.GRU953_CHROME && fs.existsSync(process.env.GRU953_CHROME)) {
    return process.env.GRU953_CHROME;
  }
  // 2. whatever Playwright itself resolves to, if it is actually installed
  try {
    const p = chromium.executablePath();
    if (p && fs.existsSync(p)) return p;
  } catch { /* Playwright has no browser registered; fall through */ }
  // 3. any chromium under the browsers root, newest first
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  if (fs.existsSync(root)) {
    const dirs = fs.readdirSync(root).filter(d => d.startsWith('chromium')).sort().reverse();
    for (const d of dirs) {
      for (const rel of ['chrome-linux/chrome', 'chrome-linux/headless_shell', 'chrome']) {
        const p = path.join(root, d, rel);
        if (fs.existsSync(p)) return p;
      }
    }
  }
  // 4. a system browser
  for (const p of ['/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome']) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error(
    'No Chromium found. Set GRU953_CHROME to a Chromium binary, or install one with\n' +
    '  npx playwright install chromium');
}

export const CHROME = findChrome();

export async function browser() {
  return chromium.launch({
    executablePath: CHROME,
    args: ['--no-sandbox', '--font-render-hinting=none', '--allow-file-access-from-files'],
  });
}
