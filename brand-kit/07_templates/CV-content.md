# CV content — Aninda Sundar Howlader / GRU953

**GRU953 · written content only.** This file is the words. The layout,
the type sizes and the colours come from the design kit and are wired in later.

**How to use it.** Everything in `[square brackets]` is a fact about you that I was not
given, so I have not invented it. Replace the brackets too. Everything outside brackets is
finished copy in GRU953's voice and can be pasted as it stands.

**One term explained:** *ATS* means "applicant tracking system" — the software many
employers use to read a CV before a person does. Where I mention it below, I say plainly
whether the advice is measured or simply common practice.

---

## 1. Personal statement

This is approved copy. Use it as it is.

> Solo developer with a bias for small, finished things. I design, build and support
> complete applications on my own, from first conversation to bug reports, and I do it for
> people on old phones and slow connections in Bangla and English. I keep scope honest and
> name limits early. My own design system is published under Apache-2.0. I would
> rather ship one clear screen than five clever ones.

*68 words.*

### A shorter version, for a one-page CV

> Solo developer. I design, build and support complete applications on my own, in Bangla
> and English, for people on old phones and slow connections. I keep scope honest and name
> limits early. I would rather ship one clear screen than five clever ones.

*43 words.*

### If a role is specific, add one sentence — never more

Put it as the second sentence, and make it a fact rather than an enthusiasm.

> [I have spent the last [N] months on [the specific thing the job is about], most recently
> [what you built].]

Do not write "I am passionate about", "I am excited by the opportunity", or "I am a fast
learner". None of them can be checked, so none of them earns its line.

### Bangla version

Use this only where the CV itself is in Bangla — a Bangladeshi government post, an NGO, a
local employer who asked for Bangla. Do not paste a Bangla paragraph into an otherwise
English CV; it reads as decoration rather than as a language you work in.

> সলো ডেভেলপার। অ্যাপ ডিজাইন করা, বানানো, তারপর চালু রাখা — পুরো কাজটাই একা করি, প্রথম
> আলোচনা থেকে বাগ রিপোর্টের উত্তর দেওয়া পর্যন্ত। যাঁদের ফোন পুরোনো আর ইন্টারনেট দুর্বল,
> তাঁদের জন্য বাংলা আর ইংরেজিতে বানাই। কাজের সীমা আগেই স্পষ্ট করে বলি। পাঁচটা চালাক
> পর্দার চেয়ে একটা পরিষ্কার পর্দা বানানো ভালো মনে করি।

> ⚠ **Unverified:** the Bangla spelling of your name. "Aninda" maps to **অনিন্দ**;
> "Anindya" would be **অনিন্দ্য**. A Bangla CV needs your name in Bangla script, and a
> brand guide must not guess a person's own name. Confirm which one is right, then use it
> everywhere.

---

## 2. Section headings

Plain nouns, in this order. Headings are in English on an English CV; the bracketed Bangla
is there for when the whole CV is in Bangla.

| # | Heading | Bangla heading | Include it when |
|---|---|---|---|
| 1 | [Your name] | [আপনার নাম] | Always. Largest thing on the page. |
| 2 | Contact | যোগাযোগ | Always. Email, phone, GitHub, site, city. |
| 3 | Profile | পরিচিতি | Always. The statement from section 1. |
| 4 | Selected work | নির্বাচিত কাজ | Always — this is your strongest section, so it goes above everything else. |
| 5 | Technical skills | কারিগরি দক্ষতা | Always. |
| 6 | Experience | কাজের অভিজ্ঞতা | If you have employment or client work to list. |
| 7 | Education | শিক্ষা | Always, even if brief. |
| 8 | Open source | ওপেন সোর্স | If your published work is separate from Selected work. |
| 9 | Languages | ভাষা | Always — Bangla and English is a working skill here, not a footnote. |
| 10 | [Certifications] | [সনদ] | Only if you hold one that the reader will recognise. |

**Notes on the order.** "Selected work" sits above "Experience" on purpose. A solo
developer's evidence is the work itself, so the reader should meet it on the first screen
rather than after a list of dates.

**Two headings not to use:** *Objective* (it is about what you want, and the reader is
reading for what you can do) and *References available on request* (assumed, so it only
spends a line).

**On layout, honestly.** It is common practice that plain single-column headings and real
text — not text inside an image or a two-column table — survive ATS parsing better. I
cannot give you a measured figure for that, so treat it as widely-followed practice rather
than a proven number: **unverified**.

---

## 3. How to phrase a solo project so it reads as strong engineering

This is the part most solo developers get wrong, in both directions: either the project is
undersold as "a personal project I made for fun", or it is inflated with words like
*robust* and *scalable* that a reader cannot check.

GRU953's way out is the brand's own rule. **A claim arrives with its number.** Numbers are
what turn a solo project into engineering evidence, because a number is a thing you had to
measure, and measuring is the work.

### The four-part shape

Every project entry has the same four parts, in this order:

1. **What it is, in one plain sentence.** What it does and who for. No adjectives.
2. **The constraint you chose to work inside.** The constraint is the engineering. "Had to
   run offline on a 2 GB phone" tells a reader more about your judgement than any framework
   list.
3. **The decisions, with their trade-offs.** Two or three. Each one says what you chose,
   what you gave up, and why. A named trade-off proves you understood the problem; a
   feature list only proves you typed.
4. **The measured outcome.** Size, speed, test count, users, uptime, crash rate — whatever
   you actually measured. If you measured nothing, measure something before you send the
   CV. One real number beats five adjectives.

Then, and only then, the stack — as a short line at the end, not as the headline.

### The shape, filled in

> **[Project name]** — [what it does, in one sentence, and who for]
> [Month YYYY – Month YYYY or "ongoing"] · [Solo] · [link]
>
> - Built to run [the constraint: offline on Android 7 and up, on phones with 2 GB of RAM],
>   because [the reason that constraint is real for the people using it].
> - Chose [decision] over [the alternative] to [what it bought]; the cost was [what you
>   gave up], which was acceptable because [why].
> - [Second decision, same shape.]
> - [The measured result: cold start [0.0]s on a [device], measured over [N] runs] ·
>   [[N] tests] · [[0.0] MB installed] · [[N] people using it since [Month YYYY]].
> - [Stack: language, framework, database, in one line.]

### Worked example — before and after

The figures in this example are **invented, for shape only**. Never publish them.

**Weak:**

> **Ledger** — a personal project. A simple and user-friendly expense tracking app for
> small shops, built with React Native. Focused on performance and a beautiful,
> intuitive UI. Robust offline support.

Four claims, none checkable: *simple*, *user-friendly*, *beautiful*, *robust*. "Personal
project" apologises before the reader has decided anything. "Focused on performance" is not
a result.

**Strong:**

> **Ledger** — keeps a record of daily takings for a one-person shop
> March 2026 – ongoing · Solo · github.com/GRU-953/gru953-ledger
>
> - Built to work with no connection at all, on Android 7 and 2 GB of RAM, because the
>   shopkeepers I designed it for lose signal for hours at a time.
> - Chose SQLite with a write-ahead log over a sync-first cloud store: entries survive the
>   app being killed mid-write, at the cost of no multi-device sync, which none of the six
>   shopkeepers I interviewed asked for.
> - Cut the multi-shop switcher after testing: it needed a third screen and a settings
>   menu, and two Android user profiles do the same job.
> - Cold start 1.6s on a Redmi 9A, down from 4.1s, measured over ten runs · 1,412 tests ·
>   5.3 MB installed · used by 40 shopkeepers since May 2026, no reported data loss.
> - React Native, SQLite, Bangla and English from the first screen.

Same project. The second version is evidence.

### Five phrases to strike out

| Do not write | Write instead |
|---|---|
| "Just a personal project" | The project's name and what it does. Solo is a fact, not a confession. |
| "Robust", "scalable", "enterprise-grade" | The number: test count, request rate, uptime, users. |
| "Beautiful, intuitive UI" | What a person can now do, and how many steps it takes. |
| "Responsible for developing…" | The verb and the outcome: "Built X; it does Y in Zs." |
| "We built…", on a project you did alone | "I built…". A false "we" is caught in the first interview question. |

### Say "solo" plainly, and say what solo included

Do not hide that you worked alone, and do not let a reader assume it means "only wrote
code". One line, once, in Selected work:

> Solo on all of it: the interviews, the design, the code, the release, and every bug
> report since.

### If you have no measured numbers yet

Measure three things this week. They are cheap and they are the difference between a claim
and evidence.

1. **Cold start time** on the oldest device you own — average of ten runs, and write down
   the device name.
2. **Installed size**, in MB, from the device's own app list.
3. **Test count**, straight from the test runner's output.

If a number is genuinely not available, leave the claim out. An empty line is better than
one you cannot defend when someone asks.

---

## 4. Ready-to-use lines for the other sections

### Technical skills — how to write it

Group by what you can do with it, not by an alphabetical dump, and never rate yourself out
of five or draw a skill bar. A percentage on a skill is a number with nothing behind it,
which is the one thing GRU953 does not do.

> **Build:** [languages] · [frameworks]
> **Data:** [databases] · [what you use for migrations and backups]
> **Ship:** [build tooling] · [CI] · [where you deploy]
> **Design:** [design tools] · own design system, published under Apache-2.0
> **Test:** [test frameworks] · [what you actually test, in three words]

### Languages

> **Bangla** — [native]. **English** — [level, plainly stated: e.g. fluent, written and
> spoken].
>
> I ship every interface in both, and the Bangla is written as Bangla rather than run
> through a translator.

That second line is worth its space: it is a working skill, and most CVs cannot claim it.

### Experience — the same four-part shape, shortened

> **[Job title]** — [Organisation], [City]
> [Month YYYY – Month YYYY]
>
> - [What you owned, and the constraint it came with.]
> - [One decision, with its trade-off.]
> - [One measured outcome, with its number.]

### Open source

> **GRU953 design system** — colour tokens and stylesheets, published under Apache-2.0;
> the guidebook and templates under PolyForm Noncommercial 1.0.0 · [link]
> [Contrast for every brand pairing measured against WCAG 2.2; the lowest is [0.00]:1.]

> **[Repository name]** — [what it is] · [N] stars · [N] contributors · [link]

Only list stars if the figure helps you. A repository with 3 stars and a clear README is
better evidence than one with 300 stars and no documentation, but the reader cannot see
that from a number, so lead with what it does.

### Contact block

> [Aninda Sundar Howlader]
> [City], Bangladesh · [your.email@example.com] · [+880 phone]
> github.com/GRU-953 · [website] · [linkedin.com/in/handle]

Spell out the GitHub handle rather than hiding it behind the word "GitHub" — a printed CV
cannot be clicked.

---

## 5. Before you send it

Six checks. Any "no" means it is not ready.

1. Is every claim carrying a number, a date, or a limit?
2. Is there a word from the avoid list — *robust*, *seamless*, *passionate*,
   *cutting-edge*, *best-in-class*? Cut it.
3. Is the brand written `GRU953` — one word, uppercase — everywhere?
4. Is every `[bracket]` gone, including the brackets themselves?
5. Does any sentence say "we" about work you did alone?
6. Read it aloud. Would you say these sentences to a person sitting next to you?

---

*Licensed under the PolyForm Noncommercial License 1.0.0. Required Notice: Copyright 2026 Aninda Sundar Howlader (GRU953). Free for any noncommercial use; selling needs permission. The wording you adapt for your own work is yours. The GRU953 name and marks are not licensed.*
