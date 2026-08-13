This chapter is the practical half of the book: what to actually do on each surface, in the
order those surfaces matter.
{: .lead }

## 1. GitHub — the most-seen surface

More people will judge GRU953 from a GitHub page than from anything else. Three things do
almost all the work.

### 1.1 The profile README

Your profile README is the front door. The written version is in
`07_templates/github-profile-README.md`, ready to commit to a repository named `GRU-953`.

The structure that works:

1. The header banner (light and dark, switched by the reader's theme).
2. One sentence saying what GRU953 is — **immediately**, because of the “GRU” reading risk.
3. The tagline, in both languages.
4. What you are building now. Two or three things, with links.
5. How to reach you.
6. A licence line.

Nothing else. No badge wall, no visitor counter, no trophy case, no animated typing banner.
Those read as decoration to a recruiter and as noise to a developer.

### 1.2 The theme-switching banner

GitHub honours `prefers-color-scheme` in markdown through a `<picture>` element. This is the
only reliable way to make a banner look right in both themes:

```html
<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="assets/readme-header-dark.png">
  <img src="assets/readme-header-light.png"
       alt="GRU953 — simple technology, for everyone." width="100%">
</picture>
```

Note the `alt` text says what the banner *means*, not “banner image”.

### 1.3 The social preview

Every repository has a **Settings → Social preview** field. It is the image that appears when
anyone shares the link — in Slack, on X, in a LinkedIn post. GitHub specifies **1280×640**,
and `06_assets/outreach/github-social-preview.png` is exactly that size.

Most repositories leave this empty and get a grey default. Setting it takes twenty seconds per
repository and is the highest-return brand action available on GitHub.

### 1.4 Repository conventions

| Thing | The GRU953 way |
|---|---|
| Repository name | lowercase, hyphenated: `gru953-ledger`, not `GRU953_Ledger` |
| README first line | what it does, in one plain sentence — never a logo with no explanation |
| A “what this does not do” section | Required. This is *Honest craft* made concrete, and it prevents the most common kind of disappointed issue. |
| Licence | Apache-2.0 for code, Apache-2.0 for content, marks reserved. See **Licence and governance**. |
| Badges | At most three, and only ones that are true and current: licence, build, version. |
| `lang` on any HTML | Always set. Always mark Bangla passages `lang="bn"`. |

## 2. The portfolio site

### 2.1 Wiring the tokens in

Three stylesheets, in this order. They are plain CSS custom properties — no build step, no
framework, no dependency.

```html
<link rel="stylesheet" href="assets/tokens.css">
<link rel="stylesheet" href="assets/typography.css">
<link rel="stylesheet" href="assets/layout.css">
```

Then use the semantic role tokens rather than the raw colours, so light and dark modes come
for free:

```css
.card {
  background: var(--gru-surface);
  color: var(--gru-ink);
  border: 1px solid var(--gru-border);
  border-radius: var(--gru-radius-md);
  padding: var(--gru-space-5);
  box-shadow: var(--gru-shadow-1);
}
.card a { color: var(--gru-link); }
```

**Use `--gru-brand`, not `--gru-meridian-900`.** The role tokens change with the theme; the
raw ramp tokens do not. Reaching past the role into the ramp is how a dark mode ends up with
navy text on a navy background.

### 2.2 The head of every page

```html
<html lang="en">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#1A1753">
<meta property="og:image" content="og-card-1200x630.png">
```

All five files are in `06_assets/favicon/` and `06_assets/outreach/`.

**Plain HTML site:** put those files next to your `index.html` and the paths above work as
written.

**Framework or bundler** (Next.js, Astro, Vite, a single-page app): put the same files in
whatever folder the tool serves untouched — usually `public/`, sometimes `static/` — and put
the same five tags in the file that controls the page `<head>`. In Next.js's App Router that
is `app/layout.tsx`; in Astro it is your layout component; in a plain Vite app it is
`index.html`. The tags do not change; only where you write them does.

### 2.2a Setting type from the scale

Colour has a worked example above; type deserves the same one. The scale is a set of tokens,
so use the token and never a raw pixel value:

```css
h1 { font-family: var(--gru-font-display); font-size: var(--gru-text-3xl);
     line-height: 1.05; letter-spacing: -.022em }
h2 { font-family: var(--gru-font-display); font-size: var(--gru-text-2xl); line-height: 1.15 }
h3 { font-family: var(--gru-font-display); font-size: var(--gru-text-xl) }
p, li { font-family: var(--gru-font-text); font-size: var(--gru-text-base); line-height: 1.6 }
code, .mono { font-family: var(--gru-font-mono); font-size: .88em }
:lang(bn) { line-height: 1.85 }   /* Bangla needs the extra room for its matra */
```

Every one of those sizes is fluid — it grows with the window, so there are no breakpoints to
maintain. The only line you may need to change is the Bangla leading, and only upwards.

### 2.3 The page shape that carries the brand

A deep Meridian hero with a great deal of empty space, one Daybreak element, and everything
aligned to one strong left edge. Then plain white below it for the reading. Restraint is doing
the work — if a page feels flat, add space and fix the alignment before adding colour.

## 3. Documents

| Document | Logo | Notes |
|---|---|---|
| CV | Horizontal lockup, Meridian on white, top-left, 140px | Content in `07_templates/CV-content.md`. Photograph conventions differ by market: a photo is normal on a CV in Bangladesh and much of South Asia, and is best left off for a UK or US employer. Match the market you are applying to. |
| Letterhead | Horizontal lockup top-left, 120px, 25mm clear space | Ink for body text, Meridian for headings. |
| Invoice · proposal | Wordmark only, or lockup at 120px | Wording in `07_templates/invoice-and-proposal-copy.md`. |
| Slide deck | Stacked lockup on the title slide; the tile bottom-right elsewhere at 24px | Title slides Meridian; content slides white. Never put body text on the gradient. |
| Email signature | No image — a text wordmark | Images in signatures get blocked or stripped. Three versions in `07_templates/email-signature.md`. |

For print, use the single-colour Ink build unless colour is definitely available, and check
that the lockup is at least **25mm** wide.

## 4. Social and posts

- **Avatar:** `avatar-512.png` — the bird on Meridian. Most platforms crop it to a circle,
  so the mark is kept well inside a safe circle.
- **X header:** `x-header-1500x500.png`. X crops the edges on small screens; nothing important
  sits within 90px of an edge.
- **LinkedIn banner:** `linkedin-banner-1584x396.png`. LinkedIn puts your profile photo over
  the lower left, so that area is deliberately empty.
- **Post images:** use the `og-card` proportions (1200×630) — it renders well on Facebook,
  LinkedIn, Slack and X alike.

Post copy is in `07_templates/social-copy.md`, in both languages. The voice rules apply as much
to a 200-character post as to a document: no hype, no hashtag spam, no manufactured urgency.

## 5. The apps themselves

- App icon: `GRU953-appicon.svg` and the PNG set in `06_assets/png/`. The 22.46% squircle
  radius is what iOS and Android expect.
- Splash: Meridian ground, the bird centred, nothing else. No spinner unless something is
  genuinely loading.
- Interface colour: use the **role** tokens — `--gru-bg`, `--gru-ink`, `--gru-accent` and the
  rest. They are defined in both themes, so a screen built from them is correct in light and
  dark without a second stylesheet. For status use `--gru-info`, `--gru-success`,
  `--gru-warning` and `--gru-danger`; for charts use `--gru-chart-1` to `--gru-chart-6`.
  Never reach past the roles to a raw ramp step in interface code.
- In-app text: bilingual, plain, and never blames the user. An error says what happened and
  what to do next.

## 6. The five-minute check before anything ships

1. Is the logo the right **build** for its size, and is its **clear space** clear?
2. Does every colour pairing pass its contrast target? (`04_colour/CONTRAST.md` has the numbers.)
3. Is `lang` set (the HTML attribute that tells a screen reader which language it is reading), and is every Bangla passage marked `lang="bn"`?
4. Does every image have alt text that says what it **means**?
5. Can you reach and operate everything with the keyboard alone, and see where the focus is?
6. Is anything claimed that has not been checked? If so, either check it or say it is unverified.
7. Is there anything here that has not earned its place? Remove it.
