# GRU953 — verbal identity (English)

**Date:** 12 August 2026 · Built on `02_strategy/BRAND-SPEC.md`, which is final.
**Scope:** the English voice. Bangla is a first-class original written by the Bangla lead, never a
translation of anything in this file. Where a surface must ship bilingually, this file gives the
English half and says so.

> Two words you will see a lot, in plain terms:
> **Voice** is what never changes about how GRU953 sounds. **Tone** is how that voice bends for the
> situation. Same person, different room.

## Read this first: what is real here, and what is stage dressing

The **rules** in this file are the deliverable. Most of the **examples** are not.

| Part of the file | Status |
|---|---|
| Every rule, list and table | Real. Use it. |
| Sections 1, 2, 3 and 6 examples | **Unverified.** They use an imaginary app called "Ledger" and invented figures: speeds, file sizes, version numbers, dates, error codes, package names, domains and the BDT rates in section 2. |
| Sections 4 and 5 (elevator lines and bios) | Written to be pasted, but **not yet approved by Aninda**, and some lines only become true once at least one app is public. Each one carries its own note. |

Never paste an invented number into anything public. Measure it, then write the real one.
Anything marked `[placeholder]` is a blank Aninda must fill before that line is used.

Two licence names appear throughout, so here they are in plain words. **Apache-2.0** is an
open source licence that lets anyone use, change and sell the code, as long as they keep the
copyright notice and the NOTICE file. It covers the **system** — the colour tokens, the
stylesheets and the scripts. **PolyForm Noncommercial 1.0.0** covers the **writing** — this
guide, the guidebook, the templates and the documentation. It permits any noncommercial use
freely; selling needs permission. It is source-available, not open source. Neither licence
grants any right to the GRU953 name or marks.

---

## 1. Voice

### In one line

**GRU953 sounds like a careful person explaining their own work to someone they respect: plain,
exact, warm, and never selling.**

That line is the test. If a sentence could have come from a marketing department, a lawyer, or a
robot, it is not GRU953. Read it aloud. If you would not say it to a person sitting next to you,
rewrite it.

### Two rules that come straight from the locked spec

These are not style preferences. They are decided, and they bind every sentence.

**1. The first mention always says what GRU953 is** (BRAND-SPEC §7a). To a developer, "GRU" already
means Gated Recurrent Unit, a standard piece of neural-network machinery. So someone skimming could
read "GRU953" as the name of an AI model. The fix is contextual. Wherever the name appears for the
first time in any piece of writing, what it is follows immediately.

- Yes: "GRU953 — a solo software studio". "GRU953 · Simple technology. For everyone."
- Yes: "Built by GRU953, a one-person studio in Bangladesh."
- No: "GRU953" alone at the top of a profile with nothing after it.

**2. It is said as one word: "Groo-nine-five-three"** (BRAND-SPEC §1). Not spelled out letter by
letter. Not "nine hundred and fifty-three". This matters in a call, a video, a talk, or a voice
note, so it belongs here and not only in the guidebook.

### The four attributes

#### 1. Plain

**What it means:** ordinary words, short sentences, one idea at a time. The shortest version that is
still true. The BRAND-SPEC rule applies to writing as well as design: when there is a choice,
choose the simpler option.

*Situation: the opening line of a README.*

- **Say this:** "Ledger keeps track of small shop takings. It works offline, on an old phone, in
  Bangla or English."
- **Not this:** "Ledger is a lightweight, offline-first financial tracking solution
  engineered to empower micro-enterprise stakeholders across low-connectivity environments."

Why the second one fails: it is longer, it says less, and a shopkeeper cannot see themselves in it.

#### 2. Exact

**What it means:** every claim carries its number, its date, or its limit. If you have not measured
it, you do not claim it. If you cannot verify it, you write "unverified" and move on. This is the
BRAND-SPEC rule "claims are computed and stated with their number", applied to prose.

*Situation: a release note.*

- **Say this:** "Startup is faster. Cold start on a Redmi 9A dropped from 4.1s to 1.6s, measured
  over ten runs."
- **Not this:** "Massive performance improvements. The app is now blazing fast!"

Why the second one fails: "blazing fast" is a feeling, not a fact, and it cannot be checked, argued
with, or trusted next time.

#### 3. Warm, not chummy

**What it means:** the reader is a person having a normal day, not a "user", and not your mate. Warm
means taking responsibility, never blaming them, and always saying what to do next. Chummy means
jokes, slang, exclamation marks and forced cheer, which stop being funny the moment someone is
actually stuck.

*Situation: an error message shown in the app.*

- **Say this:** "Your entry didn't save. The phone has no space left. Free up about 20 MB and tap
  Save again. Nothing you typed has been lost."
- **Not this:** "Oops! Something went wrong 😅 Please try again later!"

Why the second one fails: it is cheerful about the reader's problem, names no cause, and gives no
action. "Try again later" is not an instruction.

#### 4. Steady

**What it means:** the same flat calm whether the news is good, bad, or embarrassing. No drama when
something breaks, no grovelling, no defensiveness, no hype when something ships. Apologise once,
plainly, then say what you are doing about it.

*Situation: replying to a bug report from a stranger.*

- **Say this:** "Thanks, I can reproduce this. The date field breaks on months with fewer than 31
  days, so it has been wrong since 2.3.0. I'll fix it this week and reply here when it's released."
- **Not this:** "Oh no, I'm SO sorry, this is really embarrassing, I can't believe I missed
  this, I'll try to look at it as soon as I possibly can, so sorry again!!"

Why the second one fails: three apologies, no diagnosis, no date. It asks the reporter to manage the
developer's feelings.

---

## 2. The tone dial

Same voice, four rooms. The dial has two settings you actually turn: **how much warmth** and **how
much detail**.

| Situation | Warmth | Detail | The move | Never |
|---|---|---|---|---|
| Welcoming someone new | High | Low | Get them to one working thing fast | A tour of the features |
| Explaining a limitation | Medium | High | Name the limit, then the workaround | Apologising for the design |
| Apologising for a bug | Medium | High | Own it once, give a date | Excuses, or three sorries |
| Asking for money | Medium | High | State the number and what it buys | Hinting, or discounting yourself |

### Welcoming someone new

Warm, short, and pointed at one action. Do not explain the studio, the licence, or the roadmap yet.

> Welcome. Ledger is ready to use. There is no account to make.
> Add your first sale and see whether it fits how you work. If it doesn't, nothing is lost.

### Explaining a limitation

Flat and confident. A named limit is a feature of an honest product, so do not write about it in an
embarrassed voice. Give the reason, then the way round it.

> Ledger holds one shop, not several. That keeps the whole thing to two screens, which is the point.
> If you run two shops, install it twice under two profiles. If you need ten, Ledger is the wrong
> tool and I'd rather say so now.

### Apologising for a bug

One apology. What broke, who it hit, what you have done, what they should do.

> Version 2.4.0 saved March entries to April. It affected anyone who added entries between 2 and 6
> August. Sorry. 2.4.1 is out now and repairs the dates on the way in, so update and open the app
> once. If a figure still looks wrong, open an issue and I'll go through it with you.

### Asking for money

This is the tone most solo developers get wrong, in both directions: either apologetic and cheap, or
suddenly corporate. GRU953 stays itself and states the number without a wobble. No hinting, no
"whatever you think is fair", no burying the figure at the bottom.

Every figure below is a `[placeholder]`. Aninda must set his own real numbers before any of this
copy is sent to a client.

> **Invoice covering note:** Invoice [GRU953-2026-014] is attached, for the work agreed on
> [14 July]: the offline sync and the two report screens. The total is BDT [amount], due
> [30] days from today. Bank details are on the invoice. Anything unclear, ask me. I'll amend it
> the same day.

> **Reply to a paid licence enquiry:** Happy to help. The design system itself is free under
> Apache-2.0. You can use the colours, tokens and CSS in a commercial product, with no payment
> and no permission needed. The guidebook and the written templates are a different matter —
> those are PolyForm Noncommercial, so commercial use of the writing needs a quick word with
> me first. What isn't free at all is the GRU953 name and the bird mark. Those stay with the
> studio. If what you want is the system fitted to your own product and brand, that is paid work. My
> rate is BDT [rate] an hour, and a job like that is usually [range] hours. I'll quote a fixed price
> once I've seen your screens.

---

## 3. Words we use, words we avoid

### Words we use

Not a vocabulary to sprinkle on. These are the words that carry GRU953's meaning, so reach for them
first.

| Word or phrase | How we use it |
|---|---|
| **simple**, **simpler** | The brand's own claim. "Simpler" is stronger than "simple" because it invites a comparison. |
| **works** / **doesn't work** | The plainest verdict there is. "It works offline." "Search doesn't work on very old Androids." |
| **free**, and what it is free of | Never bare. "Free to use. No account, no advert, no data leaves your phone." |
| **offline** | A real, checkable property, and central to who the apps are for. |
| **Bangla and English** | Written out, in that order, when talking about the apps. Not "localised" or "i18n" to a non-technical reader. |
| **old phone**, **slow connection** | Names the actual reader instead of "low-resource environments". |
| **small** | A virtue here, not an apology. "A small app that does one thing." |
| **fix**, **fixed**, **broke** | Say "I broke it" and "I fixed it". Not "an issue was identified and remediated". |
| **limit** | "Here is the limit." A named limit builds more trust than a hidden one. |
| **try** | Low-commitment invitation. "Try it for a week." |
| **you**, **your** | Second person, always. "Your entries stay on your phone." |
| **I** (Aninda) and **GRU953** (the studio) | "I" for the person doing the work, "GRU953" for the studio and its products. Never a royal "we" pretending to be a team. In app copy, use neither: say what happened. "Your entry didn't save", not "we couldn't save it". |
| **not yet** | Honest about the future without promising it. "There's no cloud backup yet." |
| **sorry** | Once, on its own line, when it is deserved. Then stop. |
| **plain** | "In plain words." Signals the effort we make. |
| **open** | Only about the licence, and always with the name: "open under Apache-2.0". |
| a number | Any claim about speed, size, price, or dates arrives with its figure attached. |

### Words we avoid

Every avoid has a reason, and the reason is the rule. In the "say instead" column, anything in
square brackets is a blank you fill with a real, measured figure. The shape is the lesson, not the
number.

| Avoid | Why | Say instead |
|---|---|---|
| blazing fast, lightning fast | A speed claim with no number is decoration. | "Opens in [0.8]s on a [Redmi 9A], measured over ten runs." |
| seamless, frictionless | Nobody can check it, and it usually means "we removed a step" without saying which. | "No sign-up screen." |
| revolutionary, game-changing | The reader decides that, not us; claiming it costs us credibility instantly. | "Does one thing: [the thing]." |
| cutting-edge, next-generation | Dates badly and says nothing about what the thing does. | Name the actual thing: "Built with [tool], [year]." |
| leverage, utilise | Long words doing a short word's job. | "use" |
| robust, enterprise-grade | Vague reassurance where a fact belongs. | "[N] tests. Running since [month year], no data loss reported." |
| delightful, magical, beautiful | Claims a feeling on the reader's behalf. | Show a screenshot and let them decide. |
| simply, just ("just click Export") | If it were simple they wouldn't be reading; it makes a stuck person feel stupid. | "Click Export." |
| obviously, of course, as you know | Same problem, ruder. | Delete the word. |
| unfortunately | A cushion before bad news that delays the news. | Lead with the news, then the reason. |
| we're excited to announce | Our mood is not the update. | "[version] adds [what it adds]." |
| best-in-class, world-class, industry-leading | Superlatives we cannot verify, and a one-person studio least of all. | Say what it does and let it stand. |
| solution, offering | Hides what the thing is. | Name it: "an app", "a script", "a CSS file". |
| users at scale, synergy, ecosystem | Consultant filler. Nobody talks like this. | "people who use it" |
| AI-powered (as a headline) | Describes our plumbing, not their benefit. | "Reads a photo of a receipt and fills the amount in." |
| 100% secure, bug-free, never fails | Absolutes no software can honour, so the first failure makes us liars. | "Encrypted on the phone. If you find a hole, tell me." |
| free forever, lifetime guarantee | A promise about a future one person cannot control. | Tie it to the licence, which is the part that really cannot be taken back: "Free today, under Apache-2.0. An Apache-2.0 licence already granted cannot be withdrawn." |
| sorry for any inconvenience caused | A formula, not an apology; it apologises to nobody in particular. | "Sorry. This cost you an afternoon's entries." |
| please be patient, please bear with us | Moves the burden onto the person we let down. | "Fixed by Friday. I'll reply here." |
| hey guys, hey folks | Assumes a crowd and a gender. | "Hello," or nothing at all. |
| coming soon, on the roadmap | Undated promises that quietly become debts. | "Not planned." Or a month you mean: "Aiming for [month year]." |
| an emoji standing in for a word | It carries no meaning for a screen reader, and half the audience reads it differently. | Write the word. |
| Gru953, GRU 953, gru-953 in prose | BRAND-SPEC: the brand is `GRU953`, one word, uppercase. Lowercase is a filename convention only. | GRU953 |

---

## 4. Elevator description at three lengths

Word counts are exact and were counted on 12 August 2026. Two things before you use them. They are
drafts until Aninda approves them. The two longer ones describe apps, so they are only fully true
once at least one app is public. Until then, use the 12-word line.

**12 words**

> GRU953 is a one-person software studio: simple, honest tools for old phones.

**30 words**

> GRU953 is the studio name of Aninda Sundar Howlader, a solo developer in Bangladesh. He builds
> small bilingual tools that stay understandable, name their limits, and hide nothing from you.

**90 words**

> GRU953 is a one-person software studio run by Aninda Sundar Howlader from Bangladesh. It exists
> because most software assumes a fast phone, a good connection, an English reader, and money to
> spare. GRU953 assumes none of that. Every app is built to be understood on first use. Each one
> works in Bangla and English from the first screen, and names its limits plainly, up front. The
> design system behind the apps is published under Apache-2.0, so anyone can build on it. The
> brand marks are not.

Each one names GRU953 and then says what it is, which is the first-mention rule from section 1
doing its job.

---

## 5. Bios, ready to paste once Aninda has checked them

Counts below were measured on 12 August 2026. **Two warnings before you paste anything.**

**One: no invented numbers.** None of these bios contains a speed, size or price claim, on purpose.
If you want to add one, measure it first and write the figure and the device, as section 1 requires.

**Two: platform limits move.** Both limits quoted below were checked on 12 August 2026. GitHub's
160-character bio limit is **verified** against GitHub's own documented field limit. LinkedIn's
220-character headline limit is **verified against several independent third-party references, not
LinkedIn's own documentation**, which does not state it plainly. Treat 220 as reliable but not
official. Re-check both before any rewrite, because platforms change them without notice.

### GitHub profile bio (limit 160 characters)

> GRU953 · a one-person software studio in Bangladesh. I build small, honest tools in Bangla and
> English, for old phones. Simple technology. For everyone.

*152 characters. GitHub's bio field allows 160.*

This version names GRU953 and says what it is in the first six words. That matters more here than
anywhere else. The GitHub handle is `GRU-953`, so this bio is the one line standing between a visitor
and reading the name as a machine-learning model.

### GitHub profile README intro paragraph

> Hello, I'm Aninda. I write software on my own, under the name GRU953, from Bangladesh. The work is
> small tools built for people the industry tends to skip: someone on a five-year-old Android, on a
> patchy connection, reading Bangla. So the apps here work offline, and speak both languages from the
> first screen. The design system I build them with is open under Apache-2.0, so take any of
> it. The pinned repositories below are the ones worth your time first.

*84 words.* Delete the last sentence until you have actually pinned repositories, or it points at
nothing.

### LinkedIn headline (limit 220 characters)

> Solo software developer · GRU953, my one-person software studio · I build simple, offline-first
> apps in Bangla and English for people on old phones and slow connections · Open design system,
> honest scope

*203 characters. LinkedIn allows 220.* "Offline-first" means the app is built to work with no
network at all. A connection is a bonus, not a requirement.

### LinkedIn About (150–200 words)

> I build software on my own, under the studio name GRU953, from Bangladesh.
>
> Most tools quietly assume a fast phone, a steady connection, an English reader and money to spare.
> A great many people have none of those, and they are the people I build for. In practice that means
> apps that keep working with the network switched off. They read equally well in Bangla and English,
> because the Bangla is written as Bangla and not run through a translator.
>
> I work end to end. I talk to the person who will use the thing, design it, build it, ship it, and
> answer the bug reports myself. I keep scope honest. If a job needs a team, I say so.
>
> The GRU953 design system — its colour tokens, type scale and stylesheets — is published
> openly under Apache-2.0 for anyone to use commercially.
>
> Open to product work, contract builds and collaborations. Simple technology. For everyone.

*156 words.* Two lines are Aninda's to confirm, not mine to assert. Delete "Open to product work,
contract builds and collaborations" if you are not currently looking for work. The paragraph about
the published design system becomes true on the day the kit actually goes public. Until then, cut
it, or write "will be published under".

### CV personal statement (60–80 words)

> Solo developer with a bias for small, finished things. I design, build and support complete
> applications on my own, from the first conversation to the bug reports. I do it for people on old
> phones and slow connections, in Bangla and English. I keep scope honest and name limits early. My
> own design system is published under Apache-2.0. I would rather ship one clear screen than
> five clever ones.

*73 words.* "Complete applications" is a claim about your record, so only use the plural if the CV
lists at least two. With one, write "a complete application". With none yet, cut the sentence.

### Email signature descriptor (one line)

> Aninda Sundar Howlader · GRU953, a one-person software studio · simple software, one thing at a time

*100 characters.*

---

## 6. How GRU953 writes the recurring things

> **Read this before copying anything below.** Every example here uses an imaginary app called
> "Ledger". Every file size, speed, version number, date, error code and package name in it is
> invented. All of it is **unverified** and none of it may be published. The examples show the shape
> of the writing. The rules are the deliverable.

### Commit messages

**Rules.** Subject line in the imperative ("add", "fix", not "added", "fixes"), under 50 characters,
no full stop. If the reason is not obvious from the code, put it in the body after a blank line and
say *why*, not *what*. Never "fix stuff", "wip", "final", or a bare emoji.

*Example 1, a fix:*

```
Fix month rollover in date picker

Months with fewer than 31 days rolled into the next month, so a
30 March entry saved as 30 April. Clamp the day to the month's
length before saving. Broken since 2.3.0.
```

*Example 2, a deliberate removal:*

```
Remove multi-shop switcher

Two shops needed a third screen and a settings menu, which is more
than the app is for. Two profiles do the same job. Closes #48.
```

### Release notes

**Rules.** Version and date on the first line. One sentence on who should care. Then fixed headings
in this order, dropping any that are empty: **Fixed**, **Added**, **Changed**, **Known limits**.
Every performance or size claim carries its number. Bad news goes at the top, not the bottom. No
"we're excited".

*Example 1, a patch:*

```markdown
## 2.4.1 — 8 August 2026

Update if you added entries between 2 and 6 August. This release repairs dates that 2.4.0 saved
into the wrong month.

**Fixed**
- March entries saved as April. Existing wrong dates are corrected when you next open the app.
- Export crashed when the shop name contained a comma.

**Known limits**
- Entries you already exported to CSV are not corrected. Export again after updating.
```

*Example 2, a feature release:*

```markdown
## 2.5.0 — 3 September 2026

Adds photo receipts. Nothing else changes, and no existing data moves.

**Added**
- Attach a photo to any entry. Photos stay on the phone and are never uploaded.

**Changed**
- The app is 2.1 MB larger (7.4 MB, up from 5.3 MB) because of the image library.

**Known limits**
- One photo per entry.
- Photos are not included in CSV export yet.
```

### Error messages people actually see

**Rules.** Three parts, in this order: **what happened**, **why (only if we actually know)**, **what
to do now**. Reassure about their data if it is safe. Never blame the person, never say "invalid",
never show a raw stack trace. Add a short code at the end only if it helps a search. Under 30 words
in English. The Bangla line is written as Bangla by the Bangla lead, not translated from this.

*Example 1, storage:*

> Couldn't save. The phone has no space left. Free up about 20 MB and tap Save again. What you typed
> is still here. (E-14)

*Example 2, a rejected file:*

> This file didn't open. Ledger reads .csv files, and this one is .xlsx. Save it as CSV in your
> spreadsheet app and try again. (E-31)

Not: "Invalid file format." Not: "An unexpected error occurred."

### README opening paragraphs

**Rules.** The first paragraph answers three questions and nothing else: **what is this**, **who is
it for**, **what does it cost**. Three sentences, maximum four. No badges above it, no logo wall, no
"Table of Contents" before the reader knows what the thing is. A screenshot comes straight after.
Then install.

*Example 1, an app:*

> **Ledger** keeps a record of daily takings for a one-person shop. It works offline on Android 7
> and up, in Bangla or English, and there is no account to create. Free, Apache-2.0 licensed, 5.3 MB.

*Example 2, a library:*

> **gru953-tokens** is the colour and type token set behind GRU953's apps: five colour families
> in OKLCH, a full set of semantic roles for light and dark, and the CSS variables to use them. It's for anyone building an interface who wants
> contrast ratios that already pass WCAG 2.2 AA. Apache-2.0, no dependencies, 11 kB.

### Issue replies

**Rules.** Four moves, in order. Thank them. Restate the problem in your own words, so they know you
understood. Say what you now know. Then commit to one next step with a date, or say plainly that you
won't do it. Never leave an issue with no next step. If you cannot reproduce it, say exactly what you
tried.

*Example 1, a confirmed bug:*

> Thanks for the detail, the screenshot made this quick. Confirmed: entries dated the 31st of a
> 30-day month move to the following month. It's been wrong since 2.3.0, which means some saved
> dates are already affected, so the fix has to repair old rows as well. I'm on it this week and
> will reply here when 2.4.1 is out.

*Example 2, a feature request being declined:*

> Thank you, and I can see why you'd want multi-shop support. I'm not going to add it. Ledger is
> deliberately two screens, and shops brings a switcher, a settings menu and a data model that
> undoes that. The workaround that does work today: install Ledger under a second Android user
> profile, one shop each. Closing this, but the reasoning is here if anyone wants to argue with it.

---

## 7. Naming rules for future products

GRU953 is a **parent brand over individually-named apps** (BRAND-SPEC §1). So the app's own name
does the work, and GRU953 stands behind it as the maker. In practice that means the **endorsement
form**, not the **prefix form**.

Those two terms in plain words. The **endorsement form** puts the product first and credits the
maker after it: "Ledger by GRU953". The **prefix form** puts the maker first and treats the product
as its sub-brand: "GRU953 Ledger".

> **This was an open decision. It is now settled: the endorsement form wins.**
>
> The two candidates were `<Name> by GRU953` (the **endorsement form** — product first,
> maker credited after) and `GRU953 <Name>` (the **prefix form** — maker first, product as
> a sub-brand).
>
> The endorsement form is the default because BRAND-SPEC §1 says GRU953 is a parent brand
> over *individually-named* apps. The prefix form contradicts that: it makes every app a
> sub-brand rather than a name of its own. It is also the safer order to teach — a name that
> already stands alone can have the maker's name put in front of it later, whereas a name
> people first learn as "GRU953 Ledger" never fully becomes "Ledger".
>
> **The prefix form is still correct in one case:** when the product's name is too generic to
> stand alone in a listing — "GRU953 Notes" reads better than "Notes by GRU953" in an app
> store search result. Never both forms in the same document.
>
> `08_guidebook/chapters/name.md` states the same rule. If the two ever disagree again,
> BRAND-SPEC §9 is the tie-breaker.

### The written form

| Where | Form | Example |
|---|---|---|
| First mention anywhere in prose | `<Name> by GRU953` | "Ledger by GRU953 keeps a record of daily takings." |
| Every mention after the first | `<Name>` alone | "Ledger works offline." |
| App store or directory listing title | `<Name> by GRU953` | "Ledger by GRU953" |
| Inside the app's own interface | `<Name>` alone, with the bird mark | "Ledger" |
| Repository, package, folder, domain | lowercase, hyphens | `gru953-ledger`, `ledger.gru953.dev` |
| Legal, invoices, licence headers | `<Name>, a GRU953 product` | "Ledger, a GRU953 product" |

The domain in the fifth row shows the shape only. `gru953.dev` was checked on 12 August 2026 and is
**not registered to anyone**, GRU953 included (see `08_guidebook/chapters/name.md`). Do not print it
anywhere public until it has been bought.

**Use the prefix form `GRU953 Ledger` only** for a name too generic to stand alone: a bare common
noun such as "Notes" or "Timer". If you find yourself needing the prefix
often, the name is the problem, not the rule.

**Never write:** `GRU953Ledger` · `Gru953 Ledger` · `GRU-953 Ledger` · `GRU953's Ledger` ·
`ledger by gru953` in prose · the app name merged into the wordmark's letterforms.

**In the lockup** (the fixed arrangement of bird plus wordmark that ships as one file): the bird and
the GRU953 wordmark stay exactly as drawn. The app name is separate text set in Sora Regular, at
60–70% of the wordmark's height, in Ink or Paper. It never becomes part of the wordmark and never
changes the wordmark's spacing.

It also sits **outside the logo's clear space**. `02_strategy/DESIGN-RULES.md` §1.3 fixes that space
at half the mark's own height on all four sides, and nothing may enter it. So the app name goes below
or beside the lockup with that gap kept clear, never tucked up against it. The 60–70% figure is
this file's proposal for the text, not a locked design decision. The design workstream owns the final
geometry, so confirm it there before any artwork is cut.

### The five-question test, before a name is chosen

1. **Phone test.** Can you say it once, on a bad line, and have it typed correctly with no spelling?
2. **Bangla mouth test.** Does it sit comfortably in a Bangla sentence, said by a Bangla speaker, and
   does it mean nothing unfortunate in Bangla?
3. **Plain-noun test.** Does it tell a stranger roughly what the thing does, or at least not mislead?
4. **Two-syllable test.** Two syllables ideally, three at most. People shorten anything longer, and
   then they own the name, not you.
5. **Availability check.** Search the trademark register, the package registries (npm and PyPI), the
   domain and GitHub. Write down what you found, and the date you found it. Until that is done, the
   name is "unverified" in internal notes. Nothing here can be checked in advance for an app that
   does not exist yet, so this step is always Aninda's, and always dated. `name.md` shows the format:
   what was checked, the result, and how confident the result is.

### What makes a bad name here

| Bad name pattern | Why it is bad for GRU953 | Example to avoid |
|---|---|---|
| Invented tech-sounding words | Says nothing, and needs explaining every single time. | "Zynthara" |
| Dropped or swapped vowels | Fails the phone test on the first call. | "Ledgr", "Trakit" |
| `-ify`, `-ly`, `-io`, `-hub` suffixes | Dated startup dressing; contradicts a plain voice. | "Ledgerly", "Tallyify", "Ledger.io" |
| "AI" or "Smart" in the name | Describes plumbing, dates fast, and promises something the app must then prove. | "SmartLedger AI" |
| A version or year baked in | Guarantees the name is wrong later. | "Ledger 2026", "NextLedger" |
| Longer than three syllables | Gets shortened by users into something you did not choose. | "Accountability Companion" |
| English-only puns or wordplay | Dies in translation and breaks the bilingual promise. | "Sum Thing Else" |
| A word already owned by a large product | A fight GRU953 cannot afford, and confusing besides. | "Sheets", "Wallet", "Vault" |
| Reusing "GRU" or "953" inside the app name | Dilutes the parent mark and reads as a serial number. | "GRU Ledger 953" |
| A name that needs the tagline to make sense | If it only works with a sentence attached, it isn't the name. | "Everyone" |

**The one rule, applied to naming:** given two workable names, take the plainer one.

---

## Appendix: the quick check before anything is published

1. Is there a claim without a number, a date, or a limit? Add one or cut the claim.
2. Is any number in it a real measured one, not an example copied out of this file?
3. Is there a word from the avoid list? Replace it.
4. Read it aloud. Would you say this to a person? If not, rewrite.
5. Is the brand written `GRU953`, one word, uppercase?
6. Does the first mention of GRU953 say what GRU953 is, right after the name?
7. If this surface is bilingual, has the Bangla been written as Bangla, not translated?

Seven checks, so call it fifteen seconds rather than ten. It is still the cheapest fifteen seconds in
the whole kit.
