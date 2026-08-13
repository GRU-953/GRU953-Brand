This book is the single source of truth for how GRU953 looks, speaks and behaves. If you
make anything that carries the GRU953 name — a screen, a repository, a document, a post —
start here.
{: .lead }

এই বইটি GRU953-এর চেহারা, ভাষা আর আচরণের একমাত্র নির্ভরযোগ্য উৎস। GRU953 নামে কিছু বানালে —
স্ক্রিন, রিপোজিটরি, ডকুমেন্ট বা পোস্ট — শুরু করুন এখান থেকেই।

## The promise this book exists to keep

> ## Simple technology. For everyone.
> ### সহজ প্রযুক্তি। সবার জন্য।

Four words in each language. Every rule in this book is downstream of them. When a
decision is genuinely difficult, the tie-breaker is always: *which option keeps that promise?*

## How to use this book

Everything is inside this one file, and it works with no internet connection. The **Contents**
list jumps between chapters. The **theme** button cycles automatic, light and dark. The
**EN + বাং** button hides the Bangla if you want to read faster. Printing the page, or saving
it as a PDF, gives you the whole book. The layout scales itself to whatever screen you are
on, from a small phone to a large display — there is nothing to switch.

Every asset — logos, artwork, fonts, tokens, templates, licence documents — is embedded in the
page itself, so the download buttons in **Every asset** work offline too. Nothing here depends
on a server staying up.

## The one rule above all

> When this book offers you a choice, choose the simpler option. Simplicity is not a
> style here; it is the promise the brand makes.

> এই বই যেখানে বেছে নিতে বলে, সেখানে সহজটিই বেছে নিন। সরলতা এখানে কোনো স্টাইল নয়; এটিই
> ব্র্যান্ডের প্রতিশ্রুতি।

## The whole system in one page

If you read nothing else, read this table. Everything after it is detail.

| | The decision | Where it is set out |
|---|---|---|
| **Name** | `GRU953` — one word, uppercase, no hyphen, never translated. Said as one word: "Groo-nine-five-three". Always immediately followed by what it is. | **The name** |
| **Voice** | Precise and quietly confident, and warm. Plain UK English. No hype, no jargon, no guess presented as fact. | **Voice and tone** |
| **Mark** | The Soaring Bird — one drawing, used at 24px and above; below that, the tile. The mark does not move. | **The logo** |
| **Colour** | **Meridian** `#1A1753` as the ground; **Daybreak** as the signature — one hue with two tuned values, `#B45A39` on light grounds and `#FFAB8E` on dark; **Ember** `#EDB24D` in support. Why two values is worked out once, in **Colour**. | **Colour** |
| **Type** | **Sora** for display and the wordmark, **Noto Sans** for body, **Noto Sans Bengali** for all Bangla, **JetBrains Mono** for code. | **Typography** |
| **Space** | A 4px scale, a 12-column grid, four radii, three depths. When unsure, use 16px. | **Design rules** |
| **Language** | Bilingual by default. Bangla is written as an original, never translated. | **Writing in Bangla** |
| **Licence** | **Apache-2.0** for the system, **PolyForm Noncommercial 1.0.0** for the book. The marks are not licensed at all. | **Licence and governance** |

## Words this book uses

This book measures things, so it uses a few technical words. Each one is explained here
once, in plain English, and then used without ceremony.

| Word | What it means, plainly |
|---|---|
| **WCAG** | The Web Content Accessibility Guidelines — the accessibility rulebook that regulators and procurement teams actually point to. Version 2.2, level AA, is the bar this kit holds itself to. |
| **Contrast ratio** | How different two colours are in brightness, written like `4.5:1`. Bigger is easier to read. WCAG wants at least 4.5:1 for body text and 3:1 for large text, icons and borders. |
| **Luminance** | How much light a colour emits — its brightness, not how colourful it is. Contrast is a ratio between two luminances and nothing else. |
| **ΔE (delta E)** | How different two colours *look* to a normal eye. Under about 1, nobody notices. Over about 10, anyone would call them different colours. The method used here is called CIEDE2000. |
| **OKLCH** | A way of writing a colour as lightness, colourfulness and hue, built so that equal steps look equal to the eye. Ordinary hex codes are not like that, which is why the palette is built in OKLCH and then converted. |
| **Monotonic** | A ramp is monotonic when every step is reliably lighter, or reliably darker, than the last — it never doubles back. An unpredictable ramp is unusable for an interface. |
| **Counters** | The small enclosed gaps inside a shape, like the hole in an *o*. They are the first thing to blur shut as a drawing gets smaller, which is why the bird has a size floor. |
| **Squircle** | A rounded square, rounder than a normal button corner. It is the exact shape iOS and Android use for app icons. |
| **Token** | A named value you use instead of a literal one — `--gru-accent` rather than `#B45A39`. Change the token once and everything using it changes with it. |
| **Source-available** | Code or writing you can read and copy but not sell. It is *not* the same as open source, and this book never blurs the two. |
| **Outlines** | Letters converted into shapes, so they do not need the font installed to look right. Every lockup in this kit is outlines. |

## What this book is honest about

A brand guide that only lists strengths is marketing. These are the real limits.

- **Nothing here has been tested with a real screen reader by a real user.** The contrast is
  computed and proved; lived accessibility is not the same thing.
- **Every colour in this edition is measured.** There is no carried-over palette taking its
  correctness on trust; the earlier one was removed rather than left unverified. Every ramp,
  every role and every chart colour on these pages was computed and checked on this build.
- **To a developer audience, "GRU" already means *Gated Recurrent Unit*.** That reading risk is
  real, it was measured, and the decision to keep the name was taken with it in view. See
  **The name**.
- **The marks are reserved but not registered.** That is a statement of position, not a legal
  shield. See **Licence and governance**.
- **The brand has one person behind it.** Wherever this book might read as though it has a team,
  it is wrong.
