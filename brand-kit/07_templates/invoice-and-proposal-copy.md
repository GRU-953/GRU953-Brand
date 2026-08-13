# Invoice and proposal copy — GRU953 

The standard wording for freelance money conversations, in GRU953's voice. This file is the
words only; the invoice layout, the logo placement and the type come from the design kit.

**How to use it.** Replace every `[bracketed]` slot, brackets included. Everything outside
brackets is finished copy.

**The tone, in one line.** This is the tone most solo developers get wrong, in both
directions: apologetic and cheap, or suddenly corporate. GRU953 stays itself and states the
number without a wobble. No hinting, no "whatever you think is fair", no burying the figure
at the bottom, and no sudden legal register on page two.

> ⚠ **What I could not verify, and you must check.** Nothing in this file is tax or legal
> advice, and I have not verified any Bangladeshi requirement for VAT, withholding tax, a
> trade licence, or the wording an invoice must legally carry. Every tax line below is a
> `[placeholder]`. Ask an accountant once, write the real wording into your own template,
> and then it is settled forever. Marked **unverified**.

---

## Part 1 — The invoice

### 1.1 The fields, and the exact words for each

| Field | Wording to use | Note |
|---|---|---|
| Title | `Invoice` / `ইনভয়েস` | Not "Bill", not "Tax Invoice" unless your accountant says that is required. |
| Invoice number | `GRU953-[YYYY]-[NNN]` | Sequential, never reused, never restarted mid-year. `GRU953-2026-014`. |
| Invoice date | `[12 August 2026]` | Written out. Never `12/08/2026` — that is ambiguous across countries. |
| Due date | `[11 September 2026]` | A real date, not "Net 30". The client should not have to count. |
| From | `[Aninda Sundar Howlader]`<br>`GRU953 — a one-person software studio`<br>`[address]` · `[email]` · `[phone]`<br>`[Tax or trade licence number, if you have one]` | The studio line is followed by what it is, every time. |
| To | `[Client's registered name]`<br>`[Attention: name, role]`<br>`[address]` | Use their registered name, not their brand name, or accounts may reject it. |
| Reference | `[Your PO or reference: ]` | Leave the field in even when empty. Many finance teams cannot pay without one. |
| Line items | See 1.2 | |
| Subtotal | `Subtotal` | |
| Tax | `[VAT / tax, at [0]%]` | **Unverified — confirm with an accountant.** |
| Total | `Total due: [BDT 00,000]` | The largest number on the page, and the only bold one. |
| Payment details | See 1.3 | |
| Terms | See 1.4 | |
| Closing line | See 1.5 | |

### 1.2 Line items — how to word the work

One line per deliverable the client can recognise. Never one line reading "Development
work". Never a line reading "Misc".

**The shape:** *what it is* — *what it covers*, then quantity and rate.

> | Description | Qty | Rate | Amount |
> |---|---|---|---|
> | [Offline sync — writes queue on the device and send when the connection returns; includes conflict handling for same-record edits] | [1] | [BDT 00,000] | [BDT 00,000] |
> | [Report screens (2) — daily takings and monthly summary, both exportable to CSV] | [2] | [BDT 0,000] | [BDT 00,000] |
> | [Bangla and English strings for the new screens, written as originals] | [1] | [BDT 0,000] | [BDT 0,000] |
> | [Fixes and support, [Month] — [N] hours at [BDT 0,000]] | [N] | [BDT 0,000] | [BDT 00,000] |

**If the work was hourly**, say the hours and the rate on the line. A single total with no
hours behind it invites the one question you do not want three weeks later.

**If something was agreed and then dropped**, put it on the invoice at zero with a note. It
costs a line and prevents an argument:

> | [Multi-shop switcher — agreed [14 July], dropped [28 July] at your request] | — | — | [BDT 0] |

### 1.3 Payment details

> **How to pay**
> Bank transfer to:
> Account name: `[Aninda Sundar Howlader]`
> Account number: `[00000000000]`
> Bank and branch: `[Bank name], [branch]`
> Routing number: `[000000000]`
> [SWIFT / BIC, for payment from outside Bangladesh: `[XXXXXXXX]`]
>
> [Or bKash / Nagad to `[+880 0000 000000]`, if that is easier for you.]
>
> Please quote invoice `GRU953-[YYYY]-[NNN]` on the transfer so I can match it.
>
> [Bank charges on an international transfer are the sender's; if your bank deducts a fee
> from the amount, the invoice stays open for the difference.]

That last line is the honest kind of small print: it is one sentence, it is in plain words,
and it appears before the problem rather than after it.

### 1.4 Payment terms — three phrasings, pick one and keep it

**A. Standard, 30 days.**

> Payment is due by **[11 September 2026]**, which is 30 days from the invoice date.

**B. On delivery, for small jobs.**

> Payment is due on receipt of this invoice. The work is delivered and yours to use from
> today, whether or not payment has cleared.

**C. Split, for anything over [BDT 00,000] or [N] weeks.**

> This job is invoiced in two parts: **[40]% to start** and **[60]% on delivery**. This
> invoice is the **[first]** part. Work begins when the first payment clears, and I will tell
> you the day it does.

**And in every case, one line that most invoices are missing:**

> If anything on this invoice looks wrong, tell me and I will check it the same day. I would
> rather correct an invoice than chase one.

### 1.5 The closing line

> Thank you for the work. Anything unclear, ask me.

Nothing more. No "we appreciate your business", no exclamation mark.

### 1.6 The covering email that goes with the invoice

Approved copy. Change the bracketed facts only.

> **Subject:** Invoice `GRU953-[2026-014]` — [the offline sync and the two report screens]
>
> Hello [Name],
>
> Invoice `GRU953-[2026-014]` is attached, for the work agreed on [14 July]: [the offline
> sync and the two report screens]. The total is **[BDT 85,000]**, due [30] days from today,
> on **[11 September 2026]**. Bank details are on the invoice.
>
> [Everything is on [the staging build / the main branch] and working. [One thing to know:
> [the honest caveat, if there is one].]]
>
> Anything unclear, ask me and I will amend it the same day.
>
> [Aninda]

### 1.7 Bangla — the invoice blocks that a Bangladeshi client will read

Use Bangla when the client corresponds in Bangla. Keep the numbers, the invoice number, the
account number and the currency code in Latin characters.

> **শর্ত**
> এই ইনভয়েসের টাকা পরিশোধের শেষ তারিখ **[11 সেপ্টেম্বর 2026]** — ইনভয়েসের তারিখ থেকে
> 30 দিন।
>
> **টাকা পাঠানোর তথ্য**
> ব্যাংক ট্রান্সফার — অ্যাকাউন্টের নাম `[Aninda Sundar Howlader]`, অ্যাকাউন্ট নম্বর
> `[00000000000]`, `[ব্যাংকের নাম]`, `[শাখা]`, রাউটিং নম্বর `[000000000]`।
> [বিকাশ / নগদ: `[+880 0000 000000]` — এভাবে সহজ হলে এটাও চলবে।]
> ট্রান্সফারের সময় ইনভয়েস নম্বর `GRU953-[2026-014]` উল্লেখ করবেন, যাতে আমি হিসাব
> মেলাতে পারি।
>
> এই ইনভয়েসে কোথাও ভুল মনে হলে জানাবেন — একই দিনে দেখে ঠিক করে দেব। ইনভয়েসের পিছনে
> ছোটার চেয়ে ইনভয়েস সংশোধন করা আমার কাছে ভালো।
>
> কাজটার জন্য ধন্যবাদ। কিছু বুঝতে অসুবিধা হলে জিজ্ঞেস করবেন।

**Covering email in Bangla:**

> **বিষয়:** ইনভয়েস `GRU953-[2026-014]` — [অফলাইন সিঙ্ক আর দুটো রিপোর্ট স্ক্রিন]
>
> [নাম], আসসালামু আলাইকুম / নমস্কার,
>
> ইনভয়েস `GRU953-[2026-014]` সঙ্গে দিলাম — [14 জুলাই] যে কাজটা ঠিক হয়েছিল, তার জন্য:
> [অফলাইন সিঙ্ক আর দুটো রিপোর্ট স্ক্রিন]। মোট **[BDT 85,000]**, শেষ তারিখ
> **[11 সেপ্টেম্বর 2026]**। ব্যাংকের তথ্য ইনভয়েসেই আছে।
>
> [কাজটা [স্টেজিং বিল্ডে] আছে আর চলছে। [একটা কথা জানিয়ে রাখি: [সীমাটা]।]]
>
> কিছু অস্পষ্ট থাকলে বলবেন, একই দিনে ঠিক করে দেব।
>
> [অনিন্দ]

*Choose one greeting and use it consistently with that client. If you do not know which
they would prefer, `[নাম], শুভেচ্ছা।` is safe for everybody.*

---

## Part 2 — The late-payment reminder

Three messages, in order. Each one is short, states the fact, and gives one action. The
voice does not change between them: it gets *plainer*, not angrier. There is no threat in
any of them, because a threat you cannot carry out costs you more than the invoice.

**Rules that apply to all three:**

- Never write "please be patient", "gentle reminder", or "just following up".
- Never apologise for asking. You did the work.
- Never send the second one before the first is genuinely overdue.
- Every reminder repeats the invoice number, the amount and the due date. Finance teams lose
  emails, and a reminder without the number cannot be actioned.

### 2.1 First reminder — [3] days after the due date

> **Subject:** Invoice `GRU953-[2026-014]` — [BDT 85,000], due [11 September]
>
> Hello [Name],
>
> Invoice `GRU953-[2026-014]` for **[BDT 85,000]** was due on **[11 September]** and I have
> not seen the payment yet. It may well be sitting with [your finance team / in a batch] —
> if you can tell me where it is, that is enough for now.
>
> The invoice is attached again so nobody has to search for it.
>
> [Aninda]

### 2.2 Second reminder — [14] days after the due date

> **Subject:** Invoice `GRU953-[2026-014]` — [14] days overdue
>
> Hello [Name],
>
> Invoice `GRU953-[2026-014]` for **[BDT 85,000]** is now [14] days past its due date of
> **[11 September]**. I have had no reply to my message of [14 September].
>
> Two things would help:
>
> 1. Tell me the date the payment is scheduled for. Any date is workable; not knowing is the
>    hard part.
> 2. If something about the work or the invoice is the reason for the delay, say so plainly
>    and I will deal with it today.
>
> [While this is outstanding I have paused [the next piece of work / the [Month] support
> hours]. Nothing is lost and nothing is deleted; it restarts the day the invoice is
> settled.]
>
> [Aninda]

### 2.3 Third reminder — [30] days after the due date

> **Subject:** Invoice `GRU953-[2026-014]` — [30] days overdue, next step
>
> Hello [Name],
>
> Invoice `GRU953-[2026-014]` for **[BDT 85,000]** is [30] days overdue. I have written on
> [14 September] and [25 September] and had no reply.
>
> I would rather settle this between us than take it further. So: if the full amount is not
> workable this month, tell me what is, and I will accept a schedule in writing today.
>
> If I have no reply by **[date, at least 7 days away]**, I will [the one step you are
> genuinely willing and able to take — for example: refer the invoice to [a lawyer / a
> collections service], or stop work on [contract] under clause [N]]. I am telling you now
> so it is not a surprise.
>
> [Aninda]

**Only write a consequence you will actually carry out.** A threat you abandon teaches the
client that your dates mean nothing, and it will cost you on the next invoice.

**On late fees.** You can only charge one if it was agreed in writing *before* the work
started. If it was, say it once, with its number: `[A late fee of [0]% per month applies
from [date], as agreed in the contract of [date].]` If it was not agreed, do not invent it
now — put it in the next contract instead.

### 2.4 Bangla reminder — first and second

> **প্রথম মনে করানো ([3] দিন পর)**
>
> [নাম], শুভেচ্ছা।
>
> ইনভয়েস `GRU953-[2026-014]`, পরিমাণ **[BDT 85,000]** — শেষ তারিখ ছিল
> **[11 সেপ্টেম্বর]**, টাকাটা এখনও আসেনি। হতে পারে [হিসাব বিভাগে] আটকে আছে — কোথায় আছে
> এটুকু জানালেই আপাতত হবে।
>
> ইনভয়েসটা আবার সঙ্গে দিলাম, যাতে কাউকে খুঁজতে না হয়।
>
> [অনিন্দ]

> **দ্বিতীয় মনে করানো ([14] দিন পর)**
>
> [নাম], শুভেচ্ছা।
>
> ইনভয়েস `GRU953-[2026-014]`, পরিমাণ **[BDT 85,000]** — শেষ তারিখ **[11 সেপ্টেম্বর]**
> থেকে [14] দিন পার হয়েছে। [14 সেপ্টেম্বরের] মেসেজের উত্তর পাইনি।
>
> দুটো কথা জানলে কাজ সহজ হয়:
>
> 1. টাকাটা কোন তারিখে পাঠানোর কথা আছে। যে তারিখই হোক, চলবে — না জানাটাই সমস্যা।
> 2. কাজ বা ইনভয়েস নিয়ে কোনো অসুবিধার কারণে দেরি হলে সোজা করে বলুন, আজই সেটার সমাধান
>    করব।
>
> [এটা বাকি থাকা পর্যন্ত [পরের কাজটা / [মাসের] সাপোর্টের ঘণ্টা] থামিয়ে রেখেছি। কিছু
> হারায়নি, কিছু মুছে যায়নি — ইনভয়েস মিটে গেলে যেখানে থেমেছিল সেখান থেকেই চলবে।]
>
> [অনিন্দ]

---

## Part 3 — The short project proposal

Two to three pages, never ten. A proposal's job is to make one decision easy, not to prove
how much you know. Nine sections, in this order.

### 3.1 What you asked for

Their problem, in their words, restated so they can see you understood it. This section is
first because it is the one they check hardest.

> You want [what they said they want, in plain words]. Today, [what happens now and why it
> costs them something: e.g. your three shop managers each keep a paper book, and the monthly
> total takes you a full evening to add up].
>
> The part that actually matters, as I understand it: **[the one thing that has to be true
> for this to be worth doing]**. If I have that wrong, stop reading and tell me — the rest
> of this proposal is built on it.

### 3.2 What I will build — the scope statement

The scope statement is the whole proposal in one paragraph. Write it so that in three months
either of you can read it and agree on whether it was done.

> I will build **[a name for the thing]**: [what it is]. It will [do this], [do this], and
> [do this]. It works [offline / on Android 7 and up / in a browser], in **Bangla and
> English**, and the Bangla is written as Bangla rather than run through a translator.
>
> **Delivered as:** [the app installed on [N] devices / a repository you own / a signed APK
> and its source]. **You own [the code and the data]** from the day the final invoice is
> settled.
>
> **Done means:** [the checkable definition — e.g. your three managers can each record a
> day's takings on their own phone with no connection, and you can export a month as a CSV
> in one tap]. When that is true, the work is finished.

### 3.3 What I will not build

Not a disclaimer. A design decision, stated in a flat voice, in the same document as the
price — which is the only place it protects both of you.

> To keep this small enough to finish well, these are outside the job:
>
> - **[Thing]** — [why it is out: e.g. it needs a server, which means a monthly cost and
>   somebody to watch it]. [If you want it later, it is [roughly [N] weeks / a separate
>   quote].]
> - **[Thing]** — [why].
> - **[Thing]** — [why. If a cheaper workaround exists, name it here.]
>
> If any of these turns out to matter more than something on the list above, say so now and
> we will swap them rather than add to the total.

### 3.4 How long it takes

> **[N] weeks from the day the first payment clears**, assuming [the one thing you need from
> them, e.g. I get the current paper records in the first week].
>
> - Week [1–2]: [what happens], and you see [what you will see].
> - Week [3–4]: [what happens].
> - Week [N]: [delivery, and [N] days of fixes after it].
>
> You will see something working at the end of week [2], not a document. If the schedule
> slips, I will tell you in the week it slips, not at the end.

### 3.5 The price

State it once, plainly, with what it buys. Do not stack it at the bottom under three pages
of qualifications.

> **[BDT 00,000]** for everything in "What I will build".
>
> Paid in [two] parts: **[40]% ([BDT 00,000]) to start** and **[60]% ([BDT 00,000]) on
> delivery**. [Or: [BDT 0,000] per hour, with an estimate of [N] to [N] hours, and I will
> tell you when I pass [N].]
>
> That price includes: [the design], [the build], [testing on [the devices you actually
> have]], [the Bangla and English strings], and **[N] days of fixes after delivery** for
> anything that does not do what this proposal says it does.
>
> [It does not include [the yearly Play Store fee / hosting / a paid font licence], which is
> [BDT 0,000] and is paid by you, directly, so you are not paying me a margin on it.]

### 3.6 What could change the price

The honest section, and the one that saves the relationship. Every item names *who* triggers
it, so nothing feels like a trap.

> A fixed price only works if the job stays the job. Four things would change it, and none of
> them can happen without you agreeing in writing first:
>
> 1. **You add something that was not in the scope.** I will quote it as a small separate
>    amount before I start it, so you can decide whether it is worth it. Nothing is added
>    quietly.
> 2. **Something you own turns out to work differently than described.** [For example: if
>    [the existing system] has no way to export its data, the import has to be built by hand
> — that is [roughly [N] days].] I will find this out in week [1] and tell you at once.
> 3. **A decision waits on you for more than [N] working days.** I do not charge for waiting,
>    but the delivery date moves by the same number of days, because [the next piece cannot
>    start without it].
> 4. **You need it faster than the schedule.** Compressing [N] weeks into [N] means
>    [what actually gives: e.g. I drop other work, so it is [+00]%]. I would usually rather
>    cut scope than charge a rush fee, and I will offer you that first.
>
> **What will not change the price:** my own estimating mistakes, bugs in what I built, and
> anything in "What I will build". If I underestimated the work, that is mine to absorb.

That last paragraph is the one that earns the trust, and it is safe to write because it is
what an honest developer does anyway.

### 3.7 What I need from you

> - [The [current records / logo files / access to [system]]], by [when].
> - **One person who can decide.** [Name], ideally — if two people can say opposite things,
>   the work stops while I wait.
> - [An hour of your time in week [1] and week [3], on a call or in person.]
> - [A phone like the ones your staff actually use, for testing. Not the newest one you own.]

### 3.8 How I work, in four lines

> I work alone, under the name GRU953 — a one-person software studio. That means you speak to
> the person writing the code, and there is no account manager in between.
>
> It also means my capacity is real: I take [N] job[s] at a time. If a job needs a team, I say
> so rather than take it and disappear.
>
> You will get [a short written update every [Friday]], whether or not there is good news in
> it. Bad news arrives first, not last.
>
> Everything I build for you is yours: [the code, the data, and the design files]. The GRU953
> name and the bird mark stay with the studio.

### 3.9 To go ahead

> Reply to this email with "[agreed]" and I will send invoice [1] and a start date. This
> proposal holds until **[date, 30 days out]**; after that I would need to look at the
> schedule again.
>
> If it is not right, tell me which part. I would rather rewrite a proposal than deliver the
> wrong thing.

### 3.10 Bangla — the four sections a Bangla-speaking client reads first

> **আপনি যা চেয়েছেন**
>
> আপনি চান [সোজা ভাষায় তাঁদের চাওয়াটা]। এখন হয় এই: [বর্তমান অবস্থা আর তার খরচ]।
>
> আমার বোঝা অনুযায়ী আসল কথাটা হল: **[যেটা সত্যি হলে এই কাজটা করার মানে আছে]**। এটা যদি ভুল
> বুঝে থাকি, বাকিটা না পড়ে আগে সেটাই জানান — পুরো প্রস্তাবটা এর উপরেই দাঁড়ানো।

> **আমি যা বানাব**
>
> বানাব **[জিনিসটার নাম]** — [কী জিনিস]। এটি [এই কাজ], [এই কাজ] আর [এই কাজ] করবে।
> [ইন্টারনেট ছাড়াই] চলবে, [অ্যান্ড্রয়েড 7 বা তার পরে], বাংলা আর ইংরেজি দুই ভাষাতেই — আর
> বাংলাটা অনুবাদ নয়, বাংলা হিসেবেই লেখা।
>
> **কাজ শেষ মানে:** [যাচাই করা যায় এমন সংজ্ঞা]। এটা সত্যি হলেই কাজ শেষ।

> **আমি যা বানাব না**
>
> কাজটা যাতে ছোট থাকে আর ঠিকভাবে শেষ হয়, তাই এগুলো এই কাজের বাইরে:
>
> - **[জিনিস]** — [কেন বাইরে]। [পরে দরকার হলে সেটা আলাদা হিসাব।]
> - **[জিনিস]** — [কেন]।
>
> এর কোনোটা যদি উপরের তালিকার কিছুর চেয়ে বেশি দরকারি মনে হয়, এখনই বলুন — মোট টাকা না
> বাড়িয়ে আমরা একটার জায়গায় আরেকটা রাখব।

> **যে কারণে দাম বদলাতে পারে**
>
> নির্দিষ্ট দাম তখনই কাজ করে, যখন কাজটা একই থাকে। চারটে কারণে দাম বদলাতে পারে, আর কোনোটাই
> আপনার লিখিত সম্মতি ছাড়া হবে না:
>
> 1. **স্কোপের বাইরে নতুন কিছু যোগ করলে।** শুরু করার আগেই আলাদা করে দাম জানিয়ে দেব, যাতে
>    আপনি ঠিক করতে পারেন। চুপচাপ কিছু যোগ হবে না।
> 2. **আপনার দিকের কোনো জিনিস বর্ণনার চেয়ে আলাদা হলে।** [যেমন: [পুরোনো সিস্টেম] থেকে ডেটা
>    বের করার উপায় না থাকলে হাতে কাজটা করতে হবে — [প্রায় [N] দিন]।] এটা প্রথম সপ্তাহেই
>    বুঝে যাব আর তখনই জানাব।
> 3. **কোনো সিদ্ধান্ত আপনার দিকে [N] কর্মদিবসের বেশি আটকে থাকলে।** অপেক্ষার জন্য টাকা নিই
>    না, তবে ডেলিভারির তারিখ ততদিন সরে যাবে।
> 4. **সময়ের আগে দরকার হলে।** [N] সপ্তাহের কাজ [N] সপ্তাহে করতে হলে [কী ছাড়তে হবে], তাই
>    [+00]%। তবে বাড়তি টাকার চেয়ে কাজ কমানোই আমি আগে প্রস্তাব করব।
>
> **যে কারণে দাম বদলাবে না:** আমার নিজের হিসাবের ভুল, আমার বানানো জিনিসের বাগ, আর "আমি যা
> বানাব"-তে লেখা কোনো কিছু। হিসাব কম করে ফেললে সেটা আমারই দায়।

---

## Before you send anything from this file

1. Is every `[bracket]` replaced, brackets included?
2. Is the total stated once, in words the client cannot misread, and not buried?
3. Is there a date on the page instead of "Net 30"?
4. Does "What I will not build" exist? If not, write it.
5. Have you named who triggers each price change, so nothing reads as a trap?
6. Is any tax or legal wording still a placeholder? Ask an accountant before it goes out.
7. Read it aloud. Would you say these sentences to the client's face?

---

*Licensed under the PolyForm Noncommercial License 1.0.0. Required Notice: Copyright 2026 Aninda Sundar Howlader (GRU953). Free for any noncommercial use; selling needs permission. The wording you adapt for your own work is yours. The GRU953 name and marks are not licensed.*
