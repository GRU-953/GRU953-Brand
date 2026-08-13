# GRU953 — writing Bangla

You are writing or reviewing Bangla for GRU953. This file is the whole rulebook.
Everything below comes from `02_strategy/VERBAL-IDENTITY-BN.md` in the brand kit
— nothing here is invented. Where the source itself flags a wording as
unverified, that flag is kept, not quietly dropped.

## The one principle

**Bangla is an original, never a translation.** Do not draft in English and
convert it. Think the sentence in Bangla, the way a Bangladeshi developer would
actually say it out loud to a colleague. The test for every sentence you write:
if you read it aloud and your mouth trips, an English sentence is hiding
underneath it — rewrite from scratch, don't patch it.

Four voice attributes carry into Bangla exactly as in English: সহজ ও পরিষ্কার
(simple and clear), যত্নশীল (considerate), সৎ ও স্পষ্ট (honest and plain),
কারিগরি নিষ্ঠা (craft). Two things are always cut: অতিরঞ্জন (hype) and ভয়
দেখিয়ে কাজ আদায় (dark patterns) — no "এখনই!", no "শেষ সুযোগ!", no hidden terms.

## সাধু vs চলিত — চলিত always wins

Bangla has two written registers:

- **সাধু (sadhu)** — old literary register: *করিয়াছে, বলিতেছেন, তাহার, ইহা.*
  Belongs to old literature and some legal/government text. To a modern reader
  it sounds the way Shakespearean English sounds to us — dignified, and wrong
  for a button.
- **চলিত (cholit)** — modern standard register, based on educated everyday
  speech: *করেছে, বলছেন, তার, এটা.* Every newspaper, publisher, website and app
  uses it.

**GRU953 writes in চলিত, always. সাধু is never used** — not in headlines, not
in legal text, not for effect. Reason: চলিত is what the reader thinks in;
সাধু distances the brand from the reader, contradicting সবার জন্য; and mixing
the two registers in one document is the single most common mark of amateur
Bangla writing.

Two rulings that follow from the same logic:

1. **Bangladeshi standard, not Kolkata standard.** পানি (not জল), গোসল (not
   স্নান), খোঁজা / সার্চ (not অন্বেষণ).
2. **Avoid heavy Sanskritised (তৎসম) vocabulary**, even though it is technically
   চলিত: সমস্যা over ত্রুটি, অনুমতি over অনুমোদন, শুরু over আরম্ভ, জায়গা over
   স্থান.

Regional dialect (Dhakaiya, Barishali, Sylheti) is a third, separate thing —
GRU953 does not use it either.

## The honorific register — আপনি, always

**আপনি. Every time. For every reader** — user, contributor, recruiter, client,
stranger. তুমি is never used in interfaces, docs, READMEs, errors, marketing or
email. তুই is never used, anywhere. আপনি is safe for everyone from a teenager
to a grandmother; তুমি to a stranger reads as either presumed intimacy or
condescension, and there is no way to know in advance which.

The verb ending carries the form, so getting it wrong is visible everywhere —
stay consistent within one document:

| | আপনি (use) | তুমি (never) |
|---|---|---|
| Save | সেভ করুন | সেভ করো |
| Look / see | দেখুন | দেখো |
| Do you want to…? | আপনি কি … চান? | তুমি কি … চাও? |
| You are signed in | আপনি সাইন ইন করেছেন | তুমি সাইন ইন করেছ |

**The brand's own voice is আমি, never আমরা.** GRU953 has one person behind it,
and আমরা is exactly the "we" that `voice.md` forbids in English — a studio of
one pretending to be several. Where Aninda speaks, আমি; where the studio or a
product acts, name it: "GRU953 কোনো ডেটা সংগ্রহ করে না।" **Never mix আমি and
আমরা inside one document, and do not reach for আমরা at all.**

Impersonal phrasing is allowed and often kinder: "সেভ করা যায়নি।" (blames
nobody) beats "আপনি সেভ করতে ব্যর্থ হয়েছেন।" (blames the reader).

## The three-tier rule for English technical terms

**Tier 1 — keep in Latin script.** Proper nouns, code, anything the reader
types or searches for: `GitHub`, `Apache-2.0`, `README.md`, `Ctrl`,
`git clone`, `.webp`, `#B45A39`. Never transliterate into Bangla script.

**Tier 2 — the English word, in Bangla script.** The default, largest bucket:
everyday computing words Bangladeshis already say in English, so writing them
in Bangla letters is the honest record of real speech (ফাইল, ফোল্ডার,
ডাউনলোড, আপডেট...).

**Tier 3 — a genuine Bangla word.** Only where that is what people actually
say (গোপনীয়তা, অনুমতি, সমস্যা, জায়গা, খোঁজা...).

**Both, once.** For a term a general reader may not know, give the GRU953 form
then the English in brackets, on first use only, never again in the same
document: "অ্যাকসেসিবিলিটি (accessibility) — অর্থাৎ প্রতিবন্ধকতা থাকলেও যেন
ব্যবহার করা যায়।"

**Two hard prohibitions.** (1) Never coin a new Bangla compound — no
সংগ্রহশালা for *repository*, no গণনাযন্ত্র for *computer*; if a word had to be
invented, it is wrong. (2) **The out-loud test**: would a Dhaka developer say
this word aloud to a colleague? If no, don't write it. This settles almost
every argument.

### শব্দকোষ / Glossary (condensed — GRU953-approved renderings)

| English | GRU953 Bangla | Tier | Note |
|---|---|---|---|
| file | ফাইল | 2 | নথি is Indian-formal — wrong here. |
| folder | ফোল্ডার | 2 | ডিরেক্টরি only in developer/CLI context. |
| download | ডাউনলোড (করুন) | 2 | Always with করুন in a button. |
| upload | আপলোড (করুন) | 2 | Same pattern as download. |
| settings | সেটিংস | 2 | Plural as spoken; not সেটিং. |
| error (user-facing) | সমস্যা | 3 | ত্রুটি is stiff; এরর only dev-to-dev. |
| update | আপডেট | 2 | হালনাগাদ is government register — avoid. |
| password | পাসওয়ার্ড | 2 | Never গুপ্তশব্দ. |
| offline | অফলাইন | 2 | Explain once: "ইন্টারনেট ছাড়া". |
| sign in | সাইন ইন (করুন) | 2 | Mirror the English UI: "Log in" → লগ ইন. |
| sign out | সাইন আউট | 2 | Bare, no করুন — dismissive action. |
| privacy | গোপনীয়তা | 3 | Real Bangla, universally understood. |
| licence | লাইসেন্স | 2 | Licence names stay Latin: Apache-2.0. |
| open source | ওপেন সোর্স | 2 | Gloss once: "কোড সবার জন্য খোলা". |
| repository | রিপোজিটরি | 2 | রিপো only in informal dev chat. |
| bug | বাগ | 2 | Gloss once: "সফটওয়্যারের ভুল". |
| release | রিলিজ | 2 | প্রকাশ only for written content, not software. |
| accessibility | অ্যাকসেসিবিলিটি | 2 | Always gloss on first use. |
| dark mode | ডার্ক মোড | 2 | And লাইট মোড. Not অন্ধকার মোড. |
| storage | স্টোরেজ | 2 | But জায়গা when meaning free space. |
| backup | ব্যাকআপ | 2 | Never প্রতিলিপি. |
| permission | অনুমতি | 3 | OS permissions too: "ক্যামেরার অনুমতি". |
| save | সেভ (করুন) | 2 | সংরক্ষণ করুন only in formal documents. |
| delete | মুছে ফেলুন | 3 | Never ডিলিট করুন in UI. |
| cancel | বাতিল | 3 | Bare noun on a button; বাতিল করুন in prose. |
| search | খুঁজুন / সার্চ | 3/2 | খুঁজুন on the button, সার্চ naming the feature. |
| share | শেয়ার (করুন) | 2 | Never বিতরণ. |
| notification | নোটিফিকেশন | 2 | বিজ্ঞপ্তি is newspaper register — avoid. |
| sync | সিঙ্ক (হচ্ছে) | 2 | "নিজে থেকেই সিঙ্ক হয়ে যাবে". |
| install | ইনস্টল (করুন) | 2 | Never স্থাপন. |
| version | ভার্সন | 2 | The number stays Latin: 2.5.0. |
| account | অ্যাকাউন্ট | 2 | আ-kar: অ্যা, not এ্যা. |
| data | ডেটা | 2 | Spell ডেটা, not ডাটা — never vary. |
| feature | ফিচার | 2 | Never বৈশিষ্ট্য in product copy. |

**Fixed spellings** (Bangla allows variants; GRU953 picks one, always):
**ডেটা** (not ডাটা) · **রিপোজিটরি** (not রিপোজিটোরি) · **অ্যাকাউন্ট** (not
এ্যাকাউন্ট) · **কোনো** (not কোন, meaning *any*) · **নেই** (not নাই).

## Numerals and dates — Latin, always

**Latin numerals (0–9) everywhere, including inside Bangla sentences.** Bengali
numerals (০১২৩৪৫৬৭৮৯) are never used in GRU953 product, brand or documentation
text. Three reasons: `GRU953`'s digits are part of a name, and `GRU৯৫৩` would
not match a search, a URL or a `git grep`; mixed numeral systems break sorting,
`parseInt()` and version comparison; and one system with no exceptions is the
simpler option. This is a judgement call, not a measured fact — Bangladeshi
practice is genuinely mixed (government forms use Bengali numerals; software
uses Latin). GRU953 is software, so it follows software.

Units stay Latin too, joined with a non-breaking space: **40 MB**, **16px**,
**80%** — never ৮০%.

**Dates in Bangla prose/UI:** Latin day, Bangla month name, Latin year, no
comma, no ordinal suffix — **12 আগস্ট 2026**. Month names: জানুয়ারি,
ফেব্রুয়ারি, মার্চ, এপ্রিল, মে, জুন, জুলাই, আগস্ট, সেপ্টেম্বর, অক্টোবর,
নভেম্বর, ডিসেম্বর. In code, changelogs, filenames, metadata: ISO only,
**2026-08-12**, in both languages. Never a numeric-only date like 12/08/2026 —
ambiguous across regions. The বঙ্গাব্দ (Bangla calendar) is never used for
product/version/legal dates; it may appear in a purely cultural post alongside
the Gregorian date, never instead of it. Times: 24-hour in technical contexts
(**14:30**); in prose, **বিকেল 2:30**.

## Punctuation

- **দাঁড়ি ( । )** ends every Bangla sentence — never a Latin full stop.
  `U+0964`, produced natively by Bangla keyboards. No space before it, one
  space after: **কাজ শেষ।** not **কাজ শেষ ।**
- **Question mark (?) and exclamation (!)** are the Latin characters — standard
  Bangla practice. A question ends in **?**, not দাঁড়ি. GRU953 uses **!**
  almost never.
- **Comma, colon, semicolon** are Latin characters, spaced as in English.
- **Quotes:** curly doubles — "এভাবে". No Bangla single quotes for emphasis.
- **Em dash (—):** allowed, sparingly, spaced, one per paragraph at most — it
  competes visually with the মাত্রা (headline stroke) and tires the eye faster
  than in Latin.
- **Ellipsis:** the single character … (U+2026), never three dots.

### `GRU953` inside a Bangla sentence

Always Latin, uppercase, unchanged. Never গ্রু৯৫৩, never "GRU 953" with a
space. Case markers attach with a plain ASCII hyphen, no space:

| Meaning | Form | Example |
|---|---|---|
| of / possessive | GRU953-এর | GRU953-এর লোগো তিনটি মাপে আসে। |
| to / object | GRU953-কে | GRU953-কে নিয়ে লেখা হয়েছে। |
| in / at | GRU953-এ | GRU953-এ সব কিছু বাংলা আর ইংরেজিতে আছে। |
| from | GRU953 থেকে | GRU953 থেকে টেমপ্লেট নামিয়ে নিতে পারেন। |
| and / with | GRU953 ও | GRU953 ও তার অ্যাপগুলো। |

থেকে, ও, দিয়ে, জন্য stay separate words with a normal space, no hyphen. Said
aloud: "গ্রু-নাইন-ফাইভ-থ্রি" (digits named individually), never "গ্রু নয়শো
তিপ্পান্ন". Keep `GRU953-এর` on one line (non-breaking space or
`white-space: nowrap`) — a break between `GRU953-` and `এর` misreads as a
hyphenated word.

## The locked tagline and pillars

**Tagline (locked, exact):**

> সহজ প্রযুক্তি। সবার জন্য।

Two sentences, two দাঁড়ি. Do not replace the first দাঁড়ি with a comma; never
drop the second sentence — "সবার জন্য" carries the promise, not decoration.

**There is no short form.** A tagline that is reworded to fit is a different
tagline, and a locked string that has three approved spellings is not locked.
Where the full form will not fit — a footer strip, a badge, an OG image at 40px
— the space is too small for a tagline, so use the mark alone. That is a real
answer; a shortened tagline is a compromise that spreads.

This paragraph used to publish two "approved short variants". They came from
`VERBAL-IDENTITY-BN.md`, which has been corrected to match — the lock had no
exception in it anywhere else, and every mechanical check that enforces the lock
treated the variants as violations, correctly.

**The three pillars (locked Bangla):**

| English | GRU953 Bangla |
|---|---|
| Simple by design | **গোড়া থেকেই সহজ** |
| For everyone | **সবার জন্য** |
| Honest craft | **সৎ কারিগরি** |

> **Honesty note (from the source):** the English-only brand spec carries these
> pillars forward without a recorded earlier Bangla wording, so that earlier
> wording could not be verified — **unverified**. The Bangla above is set as
> canonical for GRU953 regardless. Do not present it as anything other than
> the current canonical wording.

**The four values (locked Bangla):** সহজটাই আগে (Simplicity first) ·
প্রত্যেক ব্যবহারকারীর যত্ন (Care for every user) · সততা (Honesty) ·
কারিগরি নিষ্ঠা (Craft).

**Purpose, in Bangla:**

> GRU953-এর কাজ একটাই: সত্যিকারের সহজ আর সৎ প্রযুক্তি বানানো, যা যে কেউ
> ব্যবহার করতে পারেন — টাকা, ভাষা বা সামর্থ্য যেমনই হোক।

## Typography rules for Bangla

- **`line-height: 1.7` minimum** for Bangla body text (1.8 is safer). Bangla
  stacks marks above and below the baseline; Latin's 1.5 crowds them.
- **Never justify.** `text-align: left` for Bangla paragraphs — Bangla words
  are long with fewer break points, so justification opens ugly rivers of
  white space.
- **No `letter-spacing`** on Bangla, not even 0.01em — tracking pulls the
  মাত্রা apart into dashes and detaches vowel marks from letters. Set
  `letter-spacing: 0` explicitly on Bangla blocks so a global Latin tracking
  rule cannot leak in.
- **No ALL CAPS / `text-transform: uppercase`** — Bangla has no letter case; it
  silently uppercases only stray Latin words, creating an accidental mix.
- `hyphens: none` and `overflow-wrap: normal` — no reliable Bangla hyphenation
  dictionary exists; break only at real word boundaries.
- **Never `word-break: break-all`** — the single worst rule for Bangla. It
  splits inside যুক্তাক্ষর (conjuncts) and produces broken glyph clusters.
- **No synthetic italic/oblique** — Bangla has no italic tradition; a slanted
  Bangla word looks like a rendering fault. Use weight or colour for emphasis.
- **No manual `<br>` mid-phrase** and **no underline for emphasis** (reserve
  underline for links only — the মাত্রা already gives each word a horizontal
  line; a second one below reads as noise).
- Bangla body text runs 1–2px larger than the Latin equivalent (Latin 16px →
  Bangla 17px) — a working allowance from practice, **unverified as a formal
  figure**, not a measured standard.
- Keep a number and its unit together with a non-breaking space: `40 MB`,
  `24px`, `GRU953-এর`, `12 আগস্ট`.
- **The wordmark and tagline artwork are outlines, not live text.** Bangla in
  the marks was converted to shaped outlines because Bangla needs real
  shaping that a retyped font cannot reproduce safely — never retype the
  Bangla tagline or wordmark in a font; use the artwork file as-is.

## Mistakes that mark text as machine-translated

| Wrong (translated) | Right (original Bangla) | Why |
|---|---|---|
| একটি অত্যাধুনিক অফলাইন-ফার্স্ট আর্কিটেকচারের মাধ্যমে ডেটা পার্সিস্টেন্স নিশ্চিত করা হয়েছে। | এই অ্যাপ ইন্টারনেট ছাড়াই চলে। আপনার কাজ ডিভাইসেই থাকে। | Four English words in Bangla clothing; tells the reader nothing actionable. |
| সবাই জানে রিপো ক্লোন করতে হয়। শুধু `git clone` মারুন। | রিপোজিটরি (repository) মানে কোড রাখার ফোল্ডার। প্রথমে সেটাই কপি করে নিতে হবে। | "সবাই জানে" tells the one reader who doesn't that they don't belong. |
| শীঘ্রই সব ভাষা সাপোর্ট করবে! | এখন শুধু বাংলা আর ইংরেজি আছে। পরিকল্পনা আছে, তবে তারিখ দিতে পারছি না। | "শীঘ্রই" with no date is a promise the brand cannot keep. |
| আমাদের লোগো ইন্ডাস্ট্রি-লিডিং, পিক্সেল-পারফেক্ট এবং সম্পূর্ণ ফিউচার-প্রুফ! | একটাই পাখি। ২৪ পিক্সেলের নিচে টাইল ব্যবহার করুন — ওই মাপে পাখির ডানার ফাঁকগুলো বুজে যায়। | Asserting quality vs. explaining the concrete reason for it. (The old "right" cell described three separate logo versions, which have not existed since the marks were rebuilt from one bird — a model sentence stating something false about the brand.) |
| আপনি সেভ করতে ব্যর্থ হয়েছেন। | সেভ করা যায়নি। | Blames the reader; impersonal phrasing is kinder and just as clear. |
| অজানা ত্রুটি সংঘটিত হয়েছে। | ঠিক কী হয়েছে বলা যাচ্ছে না। এটুকু নিশ্চিত: ফাইলটি সেভ হয়নি। | Sanskritised legalese vs. plain honest চলিত — and impersonal, so it needs no pronoun at all. |
| সংগ্রহশালা (coined for *repository*) | রিপোজিটরি | Never invent a Bangla compound; use the word Dhaka developers actually say. |
| GRU৯৫৩ / গ্রু৯৫৩ | GRU953 | The brand name's digits stay Latin — a Bengali-numeral version is a different string entirely. |
| কাজ শেষ । (space before দাঁড়ি) | কাজ শেষ। | No space before দাঁড়ি, one space after. |
| তুমি কি … চাও? (to an unknown reader) | আপনি কি … চান? | আপনি is the only safe form for a reader you don't know personally. |
| নানা রকম উন্নতি ও বাগ ফিক্স | তিনটি বাগ সারানো হয়েছে, আর অ্যাপটি চালু হতে আগের চেয়ে দ্রুত। | Vague hand-waving vs. a stated, countable claim. |

## Checklist before publishing any Bangla text

1. চলিত ভাষা — no সাধু has crept in anywhere?
2. আপনি everywhere — not one তুমি or তুই?
3. Every sentence ends in দাঁড়ি (।) — no Latin full stop anywhere?
4. All numerals are Latin (0–9); `GRU953` is untouched?
5. `GRU953` is Latin uppercase, suffixes joined with a hyphen?
6. No invented Bangla word — would a Dhaka developer say every word aloud?
7. Spelling is consistent throughout (ডেটা, রিপোজিটরি, অ্যাকাউন্ট, কোনো, নেই)?
8. No hype, no undated promises, every claim carries a number?
9. Read aloud, it sounds like Bangla written as Bangla — not English underneath?

If any answer is no, the text is not ready. Test 9 is the one that matters
most: if your mouth trips reading it aloud, rewrite from scratch.

---

*Source of record: `02_strategy/VERBAL-IDENTITY-BN.md`. Where this file and the
brand kit disagree, the brand kit wins.*
