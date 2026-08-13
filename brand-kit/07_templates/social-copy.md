# Social copy — GRU953

Three posts, each in a long and a short version, each in English and Bangla:

1. **The brand launch** — post once, when the kit is public.
2. **A project release** — reusable for every version you ship.
3. **"Now open source"** — reusable for every repository you open.

Replace every `[bracketed]` slot, brackets included. Everything else is finished copy.

---

## How to read the character counts

Every count below was measured on **12 August 2026** with `len()` on the text exactly as it
appears here, **including the placeholder text**. So the count changes the moment you
replace a placeholder. Recount before posting anything near a limit.

**Four practical notes:**

- **X (Twitter) replaces every link with a fixed-length short link.** Historically that is
  counted as 23 characters no matter how long your URL is, so a short post with one link is
  `count − length of the [link] placeholder + 23`. I could not re-check X's current figure
  today, so treat 23 as practice and verify before a tight post: **unverified**.
- **Bangla characters count as one each on X.** Bengali sits in the Unicode range
  U+0980–U+09FF, which falls inside X's low-weight band, unlike Chinese or Japanese where
  each character counts as two. Also **unverified** as of today's configuration, but it is
  what X's published counting rules have long specified.
- **The platform limits used below**, for the versions to choose between:
  X 280 · Bluesky 300 · Mastodon 500 (default) · LinkedIn post 3,000 ·
  GitHub release note, dev.to, a blog: no meaningful limit.
- **Bangla says the same thing in fewer characters** than English, consistently, in all six
  pairs below. That is normal, not a sign the Bangla is thinner.

## Hashtags — the rule

**Two at most, and only where the platform genuinely uses them to find things.** A wall of
tags is a request for attention rather than a piece of writing, and it dates the post.

- **X, Mastodon, Bluesky:** at most two, at the very end, never mid-sentence.
- **LinkedIn:** at most two, on their own line after the post.
- **Bangla posts:** an English tag inside a Bangla sentence breaks the reading. Put tags on
  their own line, and use a Bangla tag only if people actually search that word in Bangla —
  most technical terms are searched in English even by Bangla speakers.
- **Never:** `#dev #coding #programming #software #tech #opensource #buildinpublic`, or a
  tag naming a company you have nothing to do with.

If you want two, these are safe and honest: `#opensource` for post 3, and the project's own
name as a tag for post 2. The launch post needs none.

---

# 1. The brand launch

## 1a. Long, English — 2,129 characters

For LinkedIn (limit 3,000), a blog post, dev.to, or a pinned GitHub release note.

```text
GRU953 is my one-person software studio, and from today it has a new identity.

What changed, and why:

Colour. Three signature colours instead of a paint shop: Meridian, a deep indigo ground (#1A1753); Daybreak, first light; and Ember in support. The interesting part is Daybreak. No single colour can clear 4.5:1 against both white and near-black — that is arithmetic, not taste — so the signature is one hue with two tuned values: #B45A39 on light grounds, #FFAB8E on dark. They sit 0.51 degrees apart in hue, so they are one colour family — and 24.6 CIEDE2000 apart in appearance, so side by side they are plainly two values. Across a theme switch a reader sees the brand keeping its colour, which is the part that matters. Both numbers are published rather than just the flattering one. Every ratio in the kit is computed by a script, not eyeballed.

Type. Sora for display, decided by its numerals: the 9, 5 and 3 have flat geometric terminals that read like instrument dials, and the name has three digits in it. Noto Sans stays for body text, Noto Sans Bengali for Bangla, JetBrains Mono for code.

The logo. The Soaring Bird is the same bird, and now it is exactly one drawing — my own master path, shipped unmodified. It is used at 24px and above. Below that a line drawing stops working, so the tile is used instead: the same bird on a solid ground. Shrinking a line drawing and hoping is how an identity ends up looking amateur at small sizes.

The licence, which is the part that matters. The system — colour tokens, stylesheets, scripts — is Apache-2.0, an OSI-approved open source licence: use it commercially, no permission needed. The guidebook and the written templates are PolyForm Noncommercial 1.0.0, which is source-available rather than open source: read it, copy it, adapt it, share it, just do not sell it. The GRU953 name, the wordmark and the bird mark stay with the studio, because those identify who made a thing.

Everything is bilingual, English and Bangla, and the Bangla is written as Bangla rather than translated.

Simple technology. For everyone. / সহজ প্রযুক্তি। সবার জন্য।

[link to the kit]
```

**Attach:** one image — the horizontal lockup on Meridian, or the first-light gradient with
the two hex codes and the two contrast figures on it. One image, not a carousel.

## 1b. Short, English — 259 characters

Fits X (280) and Bluesky (300). With a real link counted as 23 characters, this comes to
**276** — inside X's limit, with almost no room spare, so do not add a word.

```text
GRU953 — my one-person studio — has a new identity: a signature colour with two tuned values, so it is right in light and dark themes; a display face chosen for its numerals; one bird. The system is open under Apache-2.0. The name and the mark are not. [link]
```

## 1c. Long, Bangla — 1,849 characters

```text
GRU953 — বাংলাদেশ থেকে চালানো আমার একজনের সফটওয়্যার স্টুডিও — আজ থেকে নতুন চেহারায়।

কী বদলাল, আর কেন:

রঙ। এখন তিনটে মূল রঙ — Meridian, গাঢ় নীল জমি (#1A1753); Daybreak, ভোরের প্রথম আলো; আর সহযোগী Ember। মজার জায়গাটা Daybreak-এ। সাদা আর প্রায়-কালো, দুটোর উপরেই 4.5:1 কনট্রাস্ট একটা রঙ দিয়ে হয় না — এটা হিসাবের কথা, পছন্দের নয়। তাই সিগনেচার একটাই রঙ, কিন্তু দুটো মাপে বাঁধা: হালকা জমিতে #B45A39, গাঢ় জমিতে #FFAB8E। দুটোর হিউয়ের ফারাক মাত্র 0.51 ডিগ্রি — অর্থাৎ একই রঙের পরিবার; আর দেখতে ফারাক 24.6 CIEDE2000, অর্থাৎ পাশাপাশি রাখলে স্পষ্ট আলাদা। থিম বদলালে পাঠক দেখেন ব্র্যান্ড তার রঙ ধরে রেখেছে — আসল কথা সেটাই। দুটো সংখ্যাই প্রকাশ করা হয়, শুধু সুবিধেজনকটা নয়। কিটের প্রতিটা অনুপাত স্ক্রিপ্ট দিয়ে হিসাব করা, চোখের আন্দাজে নয়।

টাইপ। হেডিং আর ওয়ার্ডমার্কে Sora। সিদ্ধান্তটা হয়েছে এর সংখ্যাগুলো দেখে: 9, 5 আর 3-এর মাথা সোজা আর মাপা, যন্ত্রের ডায়ালের মতো — আর নামের ভিতরেই তো তিনটে সংখ্যা। বডিতে Noto Sans, বাংলায় Noto Sans Bengali, কোডে JetBrains Mono।

লোগো। Soaring Bird — পাখিটা একই, আর এখন ড্রয়িংও একটাই: আমার নিজের আঁকা মাস্টার পাথ, অপরিবর্তিত। 24px ও তার উপরে ওটাই ব্যবহার হয়। তার নিচে সরু লাইনের ড্রয়িং আর কাজ করে না, তাই বদলে যায় টাইল — একই পাখি, নিরেট রঙের উপরে। লাইন-ড্রয়িং ছোট করে দিয়ে আশা করে বসে থাকলেই ছোট মাপে লোগো ঘেঁটে যায়।

লাইসেন্স, আর আসল কথা এটাই। সিস্টেমটা — রঙের টোকেন, স্টাইলশিট, স্ক্রিপ্ট — Apache-2.0-এর অধীনে, যেটা OSI-স্বীকৃত ওপেন সোর্স লাইসেন্স: বাণিজ্যিক কাজেও ব্যবহার করতে পারেন, আলাদা অনুমতি লাগবে না। গাইডবুক আর লেখা টেমপ্লেটগুলো PolyForm Noncommercial 1.0.0-এর অধীনে — সোর্স খোলা, তবে ওপেন সোর্স নয়: পড়ুন, কপি করুন, বদলান, ছড়ান; শুধু বিক্রি করবেন না। GRU953 নামটা, ওয়ার্ডমার্ক আর পাখির মার্কটা স্টুডিওর নিজের থাকছে — কারণ ওগুলো দিয়েই বোঝা যায় জিনিসটা কে বানিয়েছে।

সবকিছুই দুই ভাষায় — বাংলা আর ইংরেজি। আর বাংলাটা অনুবাদ নয়, বাংলা হিসেবেই লেখা।

সহজ প্রযুক্তি। সবার জন্য।

[কিটের লিংক]
```

## 1d. Short, Bangla — 249 characters

Fits X and Bluesky. With a real link at 23 characters: **266**.

```text
GRU953 — আমার একজনের সফটওয়্যার স্টুডিও — নতুন চেহারায়: হালকা আর গাঢ়, দুই থিমেই কাজ করে এমন দুই মাপে বাঁধা একটাই সিগনেচার রঙ, সংখ্যা দেখে বেছে নেওয়া ডিসপ্লে ফন্ট, আর একটাই পাখি। ডিজাইন সিস্টেম খোলা: Apache-2.0। নাম আর মার্ক স্টুডিওর নিজের। [লিংক]
```

---

# 2. A project release

Reusable. The shape follows GRU953's release-note rules: the version and what it is first,
then numbers, then the limits — bad news near the top, not buried at the end.

## 2a. Long, English — 946 characters

```text
[Project name] [1.0.0] is out. [One plain sentence: what it does and who for.]

What it does: [the one thing], [the second thing], and [the third thing]. It works [offline], on [Android 7] and up, in Bangla and English, and there is [no account to create].

Numbers, so you can judge it rather than take my word for it:
- [0.0] MB installed
- opens in [0.0]s on a [device name], measured over [10] runs
- [0,000] tests
- [free], [Apache-2.0] licensed

What it does not do:
- [Limit] — [why, in one sentence]. [The workaround, or "there is no workaround yet".]
- [Not planned: thing people will ask for] — [why not].

[If you tried an earlier version: [what changed and whether your data moves].]

It is [free] and the code is at [link]. If something breaks, open an issue and I will reply with a next step, even if the next step is "I am not going to fix this, and here is why".

[Project name], a GRU953 product. Simple technology. For everyone.
```

**Attach:** one screenshot of the app doing the actual thing, on a phone frame if you have
one. Not a logo. Not a feature grid. Write real alt text.

## 2b. Short, English — 212 characters

With a real link at 23 characters: **229**.

```text
[Project name] [1.0.0] is out. [It does one thing: keeps a record of daily takings for a one-person shop.] Offline, Bangla and English, no account, [5.3] MB, Apache-2.0. Known limit: [one photo per entry]. [link]
```

**Note the last sentence.** A known limit inside a 280-character announcement is unusual,
and it is the single most GRU953 thing on this page. Keep it.

## 2c. Long, Bangla — 866 characters

```text
[প্রজেক্টের নাম] [1.0.0] বেরোল। [এক লাইনে: কী কাজ করে, কার জন্য।]

কী করে: [প্রথম কাজ], [দ্বিতীয় কাজ] আর [তৃতীয় কাজ]। [ইন্টারনেট ছাড়াই] চলে, [অ্যান্ড্রয়েড 7] বা তার পরের ভার্সনে, বাংলা আর ইংরেজি দুই ভাষাতেই — আর [কোনো অ্যাকাউন্ট খুলতে হয় না]।

কিছু সংখ্যা, যাতে আমার কথায় বিশ্বাস না করে নিজেই যাচাই করতে পারেন:
- ইনস্টল হলে আকার [0.0] MB
- [ফোনের নাম]-এ চালু হতে [0.0] সেকেন্ড, [10] বার চালিয়ে মাপা
- [0,000] টেস্ট
- [ফ্রি], লাইসেন্স [Apache-2.0]

যা এটা করে না:
- [সীমা] — [কেন, এক বাক্যে]। [এখন যে উপায়ে চালানো যায়, বা "এখনও কোনো উপায় নেই"।]
- [যা যোগ করার পরিকল্পনা নেই] — [কেন নেই]।

[আগের ভার্সন ব্যবহার করে থাকলে: [কী বদলেছে, আর আপনার ডেটার কী হবে]।]

[ফ্রি], আর কোড আছে এখানে: [লিংক]। কিছু ভেঙে গেলে issue খুলুন — পরের ধাপটা জানিয়ে উত্তর দেব, সেটা "এটা সারাব না, কারণ এই" হলেও।

[প্রজেক্টের নাম], GRU953-এর একটি প্রোডাক্ট। সহজ প্রযুক্তি। সবার জন্য।
```

## 2d. Short, Bangla — 204 characters

With a real link at 23 characters: **221**.

```text
[প্রজেক্টের নাম] [1.0.0] বেরোল। [এক কাজই করে: ছোট দোকানের দিনের হিসাব রাখে।] ইন্টারনেট ছাড়াই চলে, বাংলা আর ইংরেজি, অ্যাকাউন্ট লাগে না, [5.3] MB, Apache-2.0। একটা সীমা: [প্রতি এন্ট্রিতে একটাই ছবি]। [লিংক]
```

---

# 3. "Now open source"

## 3a. Long, English — 1,201 characters

```text
[Project name] is now open source. The code is at [link], under Apache-2.0.

Why now, plainly: [the real reason — for example: it has been running for [N] months without data loss, so the code is honest enough to show; or: I want [the specific thing] fixed by someone who knows [the domain] better than I do].

What is in the repository: [the app itself], [the tests], [the Bangla and English strings], and a README that says what the thing does not do.

What Apache-2.0 means here, for anyone who has not read a licence lately: you can use it, change it, ship it in a paid product, and you do not need to ask me. Keep the copyright line. That is the whole deal.

What is not in the licence: the name GRU953, the GRU953 wordmark and the Soaring Bird mark. You may say your work is built on GRU953's code. You may not present your work as GRU953's. That distinction is the only thing the studio keeps for itself.

Issues and pull requests are welcome, and I read every one myself. [Small fixes: send them. Anything larger: open an issue first so neither of us wastes an evening.] I answer with a next step, even when the answer is no.

[Project name], a GRU953 product. Simple technology. For everyone.
```

## 3b. Short, English — 255 characters

With a real link at 23 characters: **278**.

```text
[Project name] is now open source, under Apache-2.0: [link]. [It has been running since [Month YYYY] for [N] people.] Use it, change it, sell it, no permission needed. The GRU953 name and bird mark stay with the studio. Issues welcome; I read them myself.
```

## 3c. Long, Bangla — 1,143 characters

```text
[প্রজেক্টের নাম] এখন থেকে ওপেন সোর্স — কোড সবার জন্য খোলা। কোড আছে এখানে: [লিংক], লাইসেন্স Apache-2.0।

এখন কেন, সোজা কথায়: [আসল কারণ — যেমন: [N] মাস ধরে চলছে, একবারও ডেটা হারায়নি, তাই কোডটা দেখানোর মতো অবস্থায় আছে; বা: [নির্দিষ্ট জিনিসটা] আমার চেয়ে ভালো বোঝেন এমন কেউ ঠিক করে দিলে ভালো হয়]।

রিপোজিটরিতে কী আছে: [অ্যাপটা নিজে], [টেস্ট], [বাংলা আর ইংরেজি লেখাগুলো], আর একটা README — যেখানে অ্যাপটা কী করে না, সেটাও লেখা আছে।

Apache-2.0 মানে এখানে কী, যাঁরা অনেকদিন লাইসেন্স পড়েননি তাঁদের জন্য: ব্যবহার করতে পারেন, বদলাতে পারেন, টাকার প্রোডাক্টেও দিতে পারেন — আমাকে জিজ্ঞেস করার দরকার নেই। শুধু কপিরাইট লাইনটা রেখে দেবেন। এটুকুই শর্ত।

লাইসেন্সের বাইরে যা: GRU953 নাম, GRU953 ওয়ার্ডমার্ক আর Soaring Bird মার্ক। আপনি বলতে পারেন আপনার কাজ GRU953-এর কোডের উপর বানানো। কিন্তু কাজটা GRU953-এর, এমনভাবে দেখাতে পারবেন না। এই তফাতটুকুই স্টুডিও নিজের কাছে রাখে।

issue আর pull request দুটোই স্বাগত, আর প্রতিটা আমি নিজে পড়ি। [ছোট সারাই হলে সোজা পাঠিয়ে দিন। বড় কিছু হলে আগে issue খুলুন, যাতে দুজনের কারও একটা সন্ধ্যা নষ্ট না হয়।] উত্তরে পরের ধাপটা জানাব — উত্তর "না" হলেও।

[প্রজেক্টের নাম], GRU953-এর একটি প্রোডাক্ট। সহজ প্রযুক্তি। সবার জন্য।
```

## 3d. Short, Bangla — 234 characters

With a real link at 23 characters: **257**.

```text
[প্রজেক্টের নাম] এখন ওপেন সোর্স, লাইসেন্স Apache-2.0: [লিংক]। [[মাস 2026] থেকে চলছে, [N] জন ব্যবহার করছেন।] ব্যবহার করুন, বদলান, টাকার কাজেও লাগান — অনুমতি লাগবে না। GRU953 নাম আর পাখির মার্ক স্টুডিওর নিজের। issue দিলে আমি নিজেই পড়ব।
```

---

## Posting notes

- **Do not post the English and the Bangla as one long doubled post.** Post them as two
  posts, or as a post and its first reply. A doubled post is twice the length and is read
  as a template.
- **Which language where:** English on LinkedIn and X for the recruiter and open-source
  audiences; Bangla on Facebook, and in a reply on X, for the people the apps are actually
  for. Both, always, on the blog and in the GitHub release.
- **One image, with real alt text.** Describe what is in it, not what it is called. Not
  "screenshot.png".
- **Never edit a claim's number to make it sound better.** If the figure changes, post the
  new figure.
- **If a launch slips**, say the new date once. Do not delete the old post.

## Before you post

1. Is every `[bracket]` replaced, brackets included?
2. Does every claim carry a number, a date, or a limit?
3. Recount the characters — the count changed when you replaced the placeholders.
4. Is `GRU953` one word, uppercase, and followed the first time by what it is?
5. Bangla only: every sentence ending in দাঁড়ি ( । ), all numerals Latin, no তুমি, and
   nothing that reads like a translation?
6. Two hashtags at most, on their own line?

---

*Licensed under the PolyForm Noncommercial License 1.0.0. Required Notice: Copyright 2026 Aninda Sundar Howlader (GRU953). Free for any noncommercial use; selling needs permission. The wording you adapt for your own work is yours. The GRU953 name and marks are not licensed.*
