<!--
  GRU953 — reusable README skeleton for any GRU953 project.
  Copy this file into a new repository as README.md, then replace every [bracketed] slot.

  THE FOUR RULES THIS SKELETON ENFORCES, so you do not have to remember them:

  1. The first paragraph answers three questions and nothing else — what is this, who is
     it for, what does it cost. Three sentences, four at most.
  2. Badges go BELOW that paragraph, never above it. A reader should learn what the thing
     is before they learn what its build status is.
  3. A screenshot comes next. No table of contents before the reader knows what this is.
  4. "What this does not do" is not optional. A named limit builds more trust than a
     hidden one, and it saves you the issue thread later.

  Order of the file is fixed: intro → badges → screenshot → install → use → limits →
  contributing → licence. Delete a section only if it is genuinely empty, and if you
  delete "What this does not do", write it instead.
-->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-horizontal-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo-horizontal-light.svg">
    <img src="assets/logo-horizontal-light.svg" alt="GRU953" width="220">
  </picture>
</p>

# [Project Name]

<!-- First mention in prose uses the endorsement form: "[Project Name] by GRU953".
     After that, the project name alone. Never "GRU953 [Project Name]" unless the name
     on its own is a bare common noun such as Notes or Timer. -->

**[Project Name]** by GRU953 [does one thing, said in plain words — for example: keeps a
record of daily takings for a one-person shop]. It works [offline / online], on
[Android 7 and up / Node 20 and up / a browser], in Bangla and English, and there is
[no account to create]. [Free], [Apache-2.0] licensed, [0.0] MB.

**[প্রজেক্টের নাম]** — GRU953-এর তৈরি। [এক লাইনে কাজটা কী: যেমন, ছোট দোকানের দিনের
হিসাব রাখে]। [ইন্টারনেট ছাড়াই] চলে, [অ্যান্ড্রয়েড 7 বা তার পরের ভার্সনে], বাংলা আর
ইংরেজি দুই ভাষাতেই, আর [কোনো অ্যাকাউন্ট খুলতে হয় না]। [ফ্রি], লাইসেন্স [Apache-2.0], আকার
[0.0] MB।

<!-- BADGES. Four at most, in this order: licence, version, tests, size.
     Brand convention: flat-square, Meridian #1A1753 as the colour, Ink #0B0E14 as the
     label ground. UK spelling on the licence badge: "licence".
     The [bracketed] parts inside these URLs must be replaced or the badge will not
     render — that is the intended reminder. Delete any badge you cannot yet earn:
     a tests badge with no tests behind it is a claim without a number. -->

![Licence Apache-2.0](https://img.shields.io/badge/licence-Apache--2.0-1A1753?style=flat-square&labelColor=0B0E14)
![Version](https://img.shields.io/badge/version-[0.0.0]-1A1753?style=flat-square&labelColor=0B0E14)
[![Tests](https://github.com/GRU-953/[repo-name]/actions/workflows/[test.yml]/badge.svg)](https://github.com/GRU-953/[repo-name]/actions)
![Size](https://img.shields.io/badge/size-[0.0]_MB-1A1753?style=flat-square&labelColor=0B0E14)

![[Plain description of what the screenshot shows, for anyone who cannot see it]](assets/screenshot-[name].png)

---

## Install

<!-- Give the shortest path that actually works, first. If there are two ways, the
     simpler one goes first and the other goes under a details block. -->

```bash
[git clone https://github.com/GRU-953/[repo-name].git]
[cd [repo-name]]
[npm install]
```

Then:

```bash
[npm start]
```

You need [Node 20 or newer / Android 7 or newer / nothing else]. [If you are on Windows,
[what changes]].

<details>
<summary>Other ways to install</summary>

- **[Package manager]** — `[install command]`
- **[Prebuilt download]** — [link], [0.0] MB, [what it contains]
- **[From source]** — [command]

</details>

## Use

[The one thing a new reader most wants to do, in three steps at most.]

1. [Step one — say exactly what to open, click or type.]
2. [Step two.]
3. [Step three.]

[If there is a second common task, one more short block. If there is a third, that belongs
in `docs/`, not here.]

### Bangla and English / বাংলা আর ইংরেজি

[How the language is chosen — for example: the app follows the phone's language and can be
changed in Settings. Say it in one sentence.]

[ভাষা কীভাবে ঠিক হয় — যেমন: ফোনের ভাষা দেখেই অ্যাপ ঠিক করে নেয়, আর সেটিংস থেকে
বদলানো যায়। এক বাক্যে বলুন।]

## What this does not do

<!-- This section is the honest-craft pillar doing real work. Write it in a flat voice.
     Do not apologise for a deliberate design decision — give the reason, then the way
     round it. Three to six lines is the right length. -->

- **[Limit, stated plainly.]** [Why, in one sentence — a reason, not an excuse.] [The
  workaround that does work today, or "there is no workaround".]
- **[Limit.]** [Why.] [Workaround.]
- **[Not planned: [thing people will ask for]].** [Why it is not planned.]
- **[Not yet: [thing that is coming]].** [What has to happen first. No date unless you
  can keep it — if you can, name the month.]

### যা এই [প্রজেক্টের নাম] করে না

- **[সীমাটা সোজা ভাষায়।]** [কেন, এক বাক্যে।] [এখন যে উপায়ে কাজ চালানো যায় — বা
  "কোনো উপায় নেই"।]
- **[সীমা।]** [কেন।] [উপায়।]
- **[যা যোগ করার পরিকল্পনা নেই: [যেটা মানুষ চাইবেন]]।** [কেন নেই।]
- **[যা এখনও নেই: [যেটা আসবে]]।** [আগে কী হতে হবে। তারিখ দিতে না পারলে তারিখ দেবেন না;
  পারলে মাসের নাম লিখুন।]

## Bugs, questions, contributions

Open an issue. Say what you did, what you expected, and what happened instead. A
screenshot usually saves us both a day. I read every issue myself and I will reply with a
next step, even if the next step is "I am not going to do this, and here is why".

Pull requests are welcome. [Small fixes: send them. Anything larger: open an issue first
so neither of us wastes an evening.] [Link to CONTRIBUTING.md, if there is one.]

**বাগ, প্রশ্ন, অবদান।** issue খুলুন — কী করেছিলেন, কী হওয়ার আশা করেছিলেন, আর আসলে কী
হল, এই তিনটে লিখলেই হয়। স্ক্রিনশট থাকলে দুজনেরই একটা দিন বাঁচে। প্রতিটি issue আমি নিজে
পড়ি, আর পরের ধাপটা জানিয়ে দিই — সেটা "এই কাজটা করব না, কারণ এই" হলেও।

## Licence

**Code:** Apache-2.0. Use it, change it, sell it, no permission needed. See [`LICENSE`](LICENSE).

**Written content** (this README, the documentation): PolyForm Noncommercial 1.0.0 — free
to read, copy, adapt and share for any noncommercial purpose; selling needs permission. It
is source-available, not open source. See [`LICENSE-GUIDEBOOK.md`](LICENSE-GUIDEBOOK.md).

**Not licensed:** the name **GRU953**, the Soaring Bird mark and the GRU953 wordmark. They
identify the studio, so they stay with it. You may say your work uses GRU953's system; you
may not present your work as GRU953's. See [`TRADEMARKS.md`](TRADEMARKS.md).

**লাইসেন্স।** কোড **Apache-2.0** — যা খুশি করতে পারেন, বাণিজ্যিক কাজেও, অনুমতি লাগবে না। লেখা
**PolyForm Noncommercial 1.0.0**: অবাণিজ্যিক যে-কোনো কাজে মুক্ত, বিক্রির জন্য অনুমতি লাগবে।
তবে **GRU953** নাম, Soaring Bird
মার্ক আর ওয়ার্ডমার্ক লাইসেন্সের বাইরে; ওগুলো স্টুডিওর পরিচয়, তাই স্টুডিওর কাছেই থাকে।
আপনি বলতে পারেন যে আপনার কাজে GRU953-এর সিস্টেম ব্যবহার করা হয়েছে; কিন্তু কাজটা
GRU953-এর, এমনভাবে দেখাতে পারবেন না।

---

<p align="center">
[Project Name], a GRU953 product · Simple technology. For everyone.<br>
[প্রজেক্টের নাম], GRU953-এর একটি প্রোডাক্ট · সহজ প্রযুক্তি। সবার জন্য।
</p>

---

*Licensed under the PolyForm Noncommercial License 1.0.0. Required Notice: Copyright 2026 Aninda Sundar Howlader (GRU953). Free for any noncommercial use; selling needs permission. The wording you adapt for your own work is yours. The GRU953 name and marks are not licensed.*
