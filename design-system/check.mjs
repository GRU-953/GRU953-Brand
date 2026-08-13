// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader (GRU953)
//
// GRU953 — render every card and measure it.
//
// WHY THIS EXISTS, BESIDE build.py --check
// ----------------------------------------
// `build.py --check` reads the source and the files on disk. It cannot see layout. An
// audit found three faults it was structurally incapable of finding: a two-column grid
// with no breakpoint that pushed 163px of a settings screen outside an `overflow:hidden`
// ancestor, where it was neither visible nor scrollable; a `:active` rule that never
// rendered because a more specific `:hover` rule always won on a pointer press; and a
// preview that claimed to follow the reader's system setting while pinning a theme.
//
// Every finding here is a MEASUREMENT — a computed style, a bounding box, a sampled
// pixel — never an inference. What it cannot measure, it says at the end.
//
//   node check.mjs                # every card, every width, both themes
//   node check.mjs --card button  # one card, while you are fixing it
//
// Needs Playwright with Chromium. It states so and exits 2 if that is not present.
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch {
  console.error("playwright is not installed, so nothing was rendered and nothing is proved.");
  console.error("  npm i -D playwright");
  process.exit(2);
}

// Find a Chromium without assuming where it lives. A hard-coded path is how a check like
// this quietly stops running on somebody else's machine — and a check that does not run
// reports no findings, which reads exactly like a pass.
function findChrome() {
  if (process.env.GRU953_CHROME && existsSync(process.env.GRU953_CHROME)) {
    return process.env.GRU953_CHROME;
  }
  try {
    const p = chromium.executablePath();
    if (p && existsSync(p)) return p;
  } catch { /* Playwright has no browser registered; fall through */ }
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || "/opt/pw-browsers";
  if (existsSync(root)) {
    const dirs = readdirSync(root).filter((d) => d.startsWith("chromium")).sort().reverse();
    for (const d of dirs) {
      for (const rel of ["chrome-linux/chrome", "chrome-linux/headless_shell", "chrome"]) {
        const p = join(root, d, rel);
        if (existsSync(p)) return p;
      }
    }
  }
  for (const p of ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome"]) {
    if (existsSync(p)) return p;
  }
  console.error("No Chromium found. Set GRU953_CHROME, or run `npx playwright install chromium`.");
  process.exit(2);
}

const WIDTHS = [320, 360, 768, 1280];
const SCHEMES = ["light", "dark"];
const args = process.argv.slice(2);
const only = args.includes("--card") ? args[args.indexOf("--card") + 1] : null;

const manifestPath = join(HERE, "_cards.json");
if (!existsSync(manifestPath)) {
  console.error("_cards.json is missing — run `python3 build.py` first.");
  process.exit(2);
}
const cards = JSON.parse(readFileSync(manifestPath, "utf8")).cards.filter(
  (c) => !only || c.path.includes(only),
);
if (!cards.length) {
  console.error(only ? `no card matches "${only}"` : "the manifest lists no cards");
  process.exit(2);
}

// The page-side measurement. Everything below runs in the browser, against real layout.
const PROBE = () => {
  const out = { overflow: [], contrast: [], aria: [], focus: [], ids: [],
                skipped: { disabled: 0, painted: 0 } };

  const parse = (s) => {
    const m = s.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[,/\s]+/).filter(Boolean).map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const lin = (c) => {
    const s = c / 255;
    return s <= 0.04045 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
  const ratio = (a, b) => {
    const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
    return (x + 0.05) / (y + 0.05);
  };
  const over = (fg, bg) => ({
    r: fg.r * fg.a + bg.r * (1 - fg.a),
    g: fg.g * fg.a + bg.g * (1 - fg.a),
    b: fg.b * fg.a + bg.b * (1 - fg.a),
    a: 1,
  });
  // The effective background: walk up until something is not transparent, compositing
  // every partly-transparent layer on the way. Reading only the element's own
  // background-color reports "rgba(0,0,0,0)" for almost everything and proves nothing.
  const effectiveBg = (el) => {
    const stack = [];
    for (let n = el; n; n = n.parentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0) {
        stack.push(c);
        if (c.a === 1) break;
      }
    }
    let base = { r: 255, g: 255, b: 255, a: 1 };
    for (let i = stack.length - 1; i >= 0; i--) base = over(stack[i], base);
    return base;
  };

  // ---- duplicate ids, and every ARIA reference resolving
  const seen = new Map();
  for (const el of document.querySelectorAll("[id]")) {
    seen.set(el.id, (seen.get(el.id) || 0) + 1);
  }
  for (const [id, n] of seen) if (n > 1) out.ids.push(`id="${id}" appears ${n} times`);
  const REFS = ["aria-labelledby", "aria-describedby", "aria-controls", "aria-owns"];
  for (const el of document.querySelectorAll(REFS.map((a) => `[${a}]`).join(","))) {
    for (const a of REFS) {
      const v = el.getAttribute(a);
      if (!v) continue;
      for (const id of v.split(/\s+/).filter(Boolean)) {
        if (!document.getElementById(id)) {
          out.aria.push(`${el.tagName.toLowerCase()} ${a}="${id}" resolves to nothing`);
        }
      }
    }
  }
  for (const el of document.querySelectorAll("label[for]")) {
    if (!document.getElementById(el.htmlFor)) {
      out.aria.push(`label for="${el.htmlFor}" resolves to nothing`);
    }
  }

  // ---- content wider than a clipping ancestor: invisible AND unscrollable
  // Three things are deliberately clipped and are not findings: .gru-sr, which is a 1px
  // box whose whole purpose is to hold text off-screen for a screen reader; a text input,
  // whose value scrolls with the caret; and any element the author marked. Reporting them
  // is how a checker trains its reader to skim past the real ones.
  const clips = (n) => /hidden|clip/.test(getComputedStyle(n).overflowX);
  for (const el of document.querySelectorAll("*")) {
    if (el.scrollWidth <= el.clientWidth + 1) continue;
    if (!clips(el)) continue; // it scrolls; that is a different question
    if (el.closest(".gru-sr")) continue;
    if (/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName)) continue;
    out.overflow.push(
      `${el.tagName.toLowerCase()}${el.className ? "." + String(el.className).split(/\s+/)[0] : ""}` +
        ` clips ${el.scrollWidth - el.clientWidth}px it will not scroll to`,
    );
  }

  // ---- contrast of every visible text run against its own effective background
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const done = new Set();
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const txt = n.textContent.trim();
    if (!txt) continue;
    const el = n.parentElement;
    if (!el || done.has(el)) continue;
    done.add(el);
    const s = getComputedStyle(el);
    if (s.visibility === "hidden" || s.display === "none" || Number(s.opacity) === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (el.closest(".gru-sr")) continue; // deliberately off-screen, read aloud only
    // WCAG 1.4.3 exempts a disabled control. It is exempt because it is not available,
    // not because low contrast is fine — so it is skipped here and named in the summary.
    // 1.4.3 says "part of an inactive user interface component", which is wider than the
    // element carrying the attribute: the LABEL of a disabled checkbox is part of that
    // inactive component too, and styling it as disabled is the correct thing to do.
    const inactive =
      el.closest("[disabled], [aria-disabled='true'], fieldset[disabled]") ||
      el.closest("label, .gru-choice")?.querySelector("[disabled], [aria-disabled='true']");
    if (inactive) {
      out.skipped.disabled++;
      continue;
    }
    // A gradient or an image behind the text cannot be resolved by walking computed
    // background-COLOR: every layer up to the page reports transparent, and the walk
    // arrives at white having measured nothing. Rather than publish a number it did not
    // measure — the hero would have been reported as 1.00:1 white-on-white — it counts
    // the case and says so. Pixel-sampling the hero is a separate, deliberate check.
    let painted = null;
    for (let a = el; a; a = a.parentElement) {
      if (getComputedStyle(a).backgroundImage !== "none") { painted = a; break; }
      if ((parse(getComputedStyle(a).backgroundColor) || { a: 0 }).a === 1) break;
    }
    if (painted) { out.skipped.painted++; continue; }
    const fg = parse(s.color);
    if (!fg) continue;
    const bg = effectiveBg(el);
    const size = parseFloat(s.fontSize);
    const bold = Number(s.fontWeight) >= 700;
    const large = size >= 24 || (bold && size >= 18.66);
    const need = large ? 3 : 4.5;
    const got = ratio(over(fg, bg), bg);
    if (got < need) {
      out.contrast.push(
        `${got.toFixed(2)}:1 needs ${need}:1 — "${txt.slice(0, 34)}" ` +
          `(${s.color} on rgb(${Math.round(bg.r)},${Math.round(bg.g)},${Math.round(bg.b)}), ` +
          `${size.toFixed(1)}px${bold ? " bold" : ""})`,
      );
    }
  }

  // ---- a scroll container nobody can reach with a keyboard (WCAG 2.1.1)
  // The resting-state contrast sweep cannot see this, and it is how four cards shipped
  // with content that scrolled only under a mouse.
  for (const el of document.querySelectorAll("*")) {
    if (el.scrollWidth <= el.clientWidth + 1) continue;
    if (!/auto|scroll/.test(getComputedStyle(el).overflowX)) continue;
    if (el.tabIndex >= 0) continue;
    if (el.querySelector('a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])'))
      continue;                      // reachable through something inside it
    out.overflow.push(
      `${el.tagName.toLowerCase()}.${String(el.className).split(/\s+/)[0]} scrolls ` +
        `${el.scrollWidth - el.clientWidth}px but has no tabindex — unreachable by keyboard`,
    );
  }

  // ---- INTERACTION STATES, measured, not assumed.
  // A resting-state sweep is blind to the two faults that actually shipped: a hover rule
  // that outranked a selected rule and put 4.36:1 on screen, and a :hover that swallowed
  // :active so a pressed state never rendered at all. Forcing a class is not enough —
  // these are real pseudo-states — so the caller drives a real pointer and calls this
  // again. What this function does is report what it currently sees, whatever the caller
  // has done to the page.
  return out;
};

let blockers = 0;
let majors = 0;
let skippedDisabled = 0;
let skippedPainted = 0;
const say = (sev, where, what) => {
  if (sev === "blocker") blockers++;
  else majors++;
  console.log(`${sev.padEnd(7)} | ${where} | ${what}`);
};

const browser = await chromium.launch({
  executablePath: findChrome(),
  args: ["--no-sandbox", "--font-render-hinting=none", "--allow-file-access-from-files"],
});
for (const card of cards) {
  const url = pathToFileURL(join(HERE, card.path)).href;
  for (const scheme of SCHEMES) {
    const ctx = await browser.newContext({ colorScheme: scheme, reducedMotion: "reduce" });
    for (const width of WIDTHS) {
      const page = await ctx.newPage();
      const consoleErrors = [];
      page.on("console", (m) => m.type() === "error" && consoleErrors.push(m.text()));
      page.on("pageerror", (e) => consoleErrors.push(String(e)));
      page.on("requestfailed", (r) => consoleErrors.push(`request failed: ${r.url()}`));
      await page.setViewportSize({ width, height: 900 });
      await page.goto(url, { waitUntil: "load" });
      await page.evaluate(() => document.fonts.ready);
      const r = await page.evaluate(PROBE);
      const at = `${card.path} @${width} ${scheme}`;
      for (const m of r.ids) say("blocker", at, m);
      for (const m of r.aria) say("blocker", at, m);
      for (const m of r.overflow) say("blocker", at, m);
      for (const m of r.contrast) say("blocker", at, m);
      for (const m of consoleErrors) say("major", at, `console: ${m}`);
      skippedDisabled += r.skipped.disabled;
      skippedPainted += r.skipped.painted;

      // Interaction states: hover every interactive element with a REAL pointer and
      // re-measure. CDP's forcePseudoState is inert in this Chromium build, so a forced
      // state would have quietly measured nothing.
      const interactive = await page.$$(
        '.gru-btn, .gru-tab, .gru-navlink, .gru-pagination a, .gru-sidenav a, ' +
          '.gru-breadcrumb a, .gru-input, .gru-select, .gru-textarea',
      );
      for (const h of interactive.slice(0, 30)) {
        const box = await h.boundingBox();
        if (!box) continue;
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
        const bad = await h.evaluate((el) => {
          // The same 1.4.3 exemption the resting sweep applies: an inactive control, and
          // the label of one. Without it, hovering a disabled button reports its own
          // deliberately-quiet colours as a failure.
          if (el.closest("[disabled], [aria-disabled='true'], fieldset[disabled]")) return null;
          if (el.closest("label, .gru-choice")?.querySelector("[disabled], [aria-disabled='true']"))
            return null;
          const p = (s) => {
            const m = s.match(/rgba?\(([^)]+)\)/);
            if (!m) return null;
            const v = m[1].split(/[,/\s]+/).filter(Boolean).map(Number);
            return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 };
          };
          const lin = (c) => { const s = c / 255;
            return s <= 0.04045 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4); };
          const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
          const st = getComputedStyle(el);
          let bg = null;
          for (let n = el; n; n = n.parentElement) {
            // A gradient or an image behind the control cannot be resolved from computed
            // background-COLOR, and walking past it arrives at the page having measured
            // nothing — the hero's own buttons came back as white on white. The hero is
            // measured by sampling its pixels instead; see the note in components.css.
            if (getComputedStyle(n).backgroundImage !== "none") return null;
            const c = p(getComputedStyle(n).backgroundColor);
            if (c && c.a === 1) { bg = c; break; }
          }
          const fg = p(st.color);
          if (!fg || !bg) return null;
          const [x, y] = [lum(fg), lum(bg)].sort((a, b) => b - a);
          const got = (x + 0.05) / (y + 0.05);
          const size = parseFloat(st.fontSize);
          const need = size >= 24 || (Number(st.fontWeight) >= 700 && size >= 18.66) ? 3 : 4.5;
          return got < need
            ? `${got.toFixed(2)}:1 needs ${need}:1 when hovered — ${st.color} on ` +
              `rgb(${bg.r},${bg.g},${bg.b}) (${el.className})`
            : null;
        });
        if (bad) say("blocker", at, bad);
      }
      await page.mouse.move(-10, -10);

      // focus visibility, measured by comparing the element's own box before and after
      const focusables = await page.$$(
        'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),' +
          'textarea:not([disabled]),[tabindex]:not([tabindex="-1"])',
      );
      for (const h of focusables.slice(0, 40)) {
        const box = await h.boundingBox();
        if (!box || box.width < 1 || box.height < 1) continue;
        // PAD the capture. The focus ring is an outline with an offset, so it is drawn
        // OUTSIDE the element's own box — screenshotting the element alone shows no
        // change and reports every correctly-focused control as a failure.
        const pad = 10;
        const clip = {
          x: Math.max(0, box.x - pad),
          y: Math.max(0, box.y - pad),
          width: box.width + pad * 2,
          height: box.height + pad * 2,
        };
        if (clip.y + clip.height > 900 || clip.x + clip.width > width) continue;
        const before = await page.screenshot({ clip }).catch(() => null);
        await h.evaluate((e) => e.focus({ focusVisible: true })).catch(() => {});
        const after = await page.screenshot({ clip }).catch(() => null);
        await page.evaluate(() => document.activeElement?.blur()).catch(() => {});
        if (before && after && Buffer.compare(before, after) === 0) {
          const d = await h.evaluate((e) => e.outerHTML.slice(0, 60));
          say("blocker", at, `no visible focus indicator on ${d}`);
        }
      }
      await page.close();
    }
    await ctx.close();
  }
  process.stderr.write(`  checked ${card.path}\n`);
}
await browser.close();

console.log("");
if (!blockers && !majors) {
  console.log(
    `No findings. ${cards.length} cards x ${WIDTHS.length} widths x ${SCHEMES.length} ` +
      `schemes = ${cards.length * WIDTHS.length * SCHEMES.length} renders.`,
  );
} else {
  console.log(`${blockers} blocker, ${majors} major`);
}
console.log(`
NOT CHECKED — stated rather than silently passed:
  · ${skippedDisabled} text runs inside a disabled control (WCAG 1.4.3 exempts them).
  · ${skippedPainted} text runs over a gradient or an image, where the background cannot
    be resolved from computed styles. The hero's scrim is measured by sampling pixels
    instead — see the note in components.css.
  · What a screen reader actually announces. ARIA attributes and id references are
    measured; NVDA, JAWS and VoiceOver are not run.
  · forced-colors / Windows High Contrast. Chromium on Linux will not emulate it, so
    the @media (forced-colors: active) blocks are shipped unexercised.
  · Print output. The @media print block is not rendered.
  · Non-Chromium engines. Only Chromium is available here.
  · Whether the Bangla reads naturally, and whether any of this looks good.`);
process.exit(blockers ? 1 : 0);
