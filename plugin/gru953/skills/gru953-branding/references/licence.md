# GRU953 — licence and trademark

> **A note on the sources named here.** `BRAND-SPEC.md`, `DESIGN-RULES.md`,
> `LICENSING-EXPLAINED.md`, `TRADEMARKS.md` and `LOGO-USAGE.md` live in the GRU953
> brand kit, which is a separate deliverable and does **not** ship inside this
> plugin. Where one of them is cited below, the rule it decides is stated here in
> full — the citation records where the decision was made, not a file you need.


**This is not legal advice.** It was written by the kit's author, who is not a
lawyer. If a real decision turns on it, read the licence texts themselves — both
ship unmodified — or ask a lawyer.

---

## The whole answer in one table

| What | Licence | OSI-approved? | Commercial use? |
|---|---|:---:|---|
| **The system** — colour tokens, stylesheets, every script | **Apache-2.0** | **Yes** | Yes, freely |
| **The book and the writing** — the guidebook, chapters, templates, documentation | **PolyForm Noncommercial 1.0.0** | **No** | Not without asking |
| **The marks** — the name, the Soaring Bird, the tile, the wordmark, any lockup | **Not licensed** | n/a | No |
| **The bundled typefaces** | **SIL OFL 1.1** | **Yes** | Yes, per the OFL |
| **Colour values** | Not restrictable | n/a | Yes. A hexadecimal number is not property. |

The rule that resolves any file: **anything a machine reads is Apache-2.0;
anything a person reads is PolyForm; anything that identifies GRU953 is
neither.**

## Say this correctly

> **PolyForm Noncommercial 1.0.0 is not an open source licence, and never will
> be.** The Open Source Definition forbids restricting a field of use, and
> "noncommercial only" is exactly that restriction. The correct word is
> **source-available**.

Never describe the kit as "fully open source". Never claim every licence in it
is OSI-approved. The Apache-2.0 half is genuinely open; the writing is not, and
saying so plainly is part of the brand.

---

## Why this split

**The system is a component.** Colour tokens and stylesheets are the kind of
thing another developer should be able to lift, use and sell without asking —
which is exactly what an OSI-approved licence guarantees. Apache-2.0 also states
outright that its grant is *"perpetual, worldwide, non-exclusive, no-charge,
royalty-free, irrevocable"*, so permanence is written down rather than inferred;
and its **section 6** reserves the licensor's trademarks inside the licence
itself, putting the most important fact about the kit in the document everyone
actually reads. It carries an express patent grant and a retaliation clause,
which MIT and BSD do not.

**The book is an identity.** The guidebook is what GRU953 looks and sounds like.
A permissive licence would let someone sell it, or a rebadged copy of it. That
is not a freedom worth granting.

PolyForm Noncommercial was chosen over the other PolyForm licences — Small
Business, Perimeter, Shield — because the boundary that matters here is
*commercial versus not*, not company size and not competition.

**One honest limit:** the PolyForm licences are drafted for *software*, and their
text says "the software" throughout. Applying one to a document works by
defining the document as the licensed work, which the NOTICE file does — but it
is not the use the drafters had in mind, and no lawyer has reviewed it.

---

## What a repository needs

Copy these into the repository root:

| File | Contents |
|---|---|
| `LICENSE` | The canonical Apache-2.0 text, verbatim. |
| `NOTICE` | The notice: the Apache header, the PolyForm `Required Notice:` line, the trademark reservation, and the font licences. Required by Apache-2.0 §4(d). |
| `LICENSE-GUIDEBOOK.md` | The canonical PolyForm Noncommercial 1.0.0 text, verbatim — only if the repository ships GRU953 long-form writing. |

All three are in `assets/licences/` in the `gru953-repo` skill.

**Never edit a licence text.** A modified Apache-2.0 is not Apache-2.0, and
tools that detect licences by hash will simply fail to recognise it.

### The README licence line

```markdown
## Licence

**Code:** Apache-2.0. Use it, change it, sell it, no permission needed. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

**Written content:** PolyForm Noncommercial 1.0.0 — free to read, copy, adapt and share for any noncommercial purpose; selling needs permission. Source-available, not open source. See [`LICENSE-GUIDEBOOK.md`](LICENSE-GUIDEBOOK.md).

**Not licensed:** the name **GRU953**, the Soaring Bird mark and the GRU953 wordmark. They identify the studio, so they stay with it. You may say your work uses GRU953's system; you may not present your work as GRU953's.
```

### Source-file headers

Apache-2.0 files that are likely to be copied out on their own carry an SPDX
line. Two lines, at the top, above the docstring:

```python
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
```

There is deliberately **no REUSE manifest**. REUSE would put a header or a
sidecar on every one of several hundred files — right for a project with
contributors, several hundred places for the truth to drift for a kit maintained
by one person. The file-map table in `LICENSING-EXPLAINED.md` is the single
place instead.

---

## Trademark

The name **GRU953**, the GRU953 **wordmark**, the **Soaring Bird**, the app-icon tile, and any
lockup combining them are the **Marks**. They identify the origin of GRU953's
work, and **they are not licensed by either licence**. Apache-2.0 §6 withholds
trademark permission expressly; PolyForm grants no trademark rights either.

### Always allowed, no permission needed

- Naming GRU953 truthfully in text — *"built with the GRU953 design tokens"*.
- Showing the **unmodified** mark to identify or link to GRU953: an article, a
  talk, a comparison table, press coverage.
- Compatibility statements — *"works with GRU953"* — provided your own branding
  is dominant and no endorsement is implied.
- Using the colour values. A hexadecimal number is not property.
- Using the token names and the CSS. Those are Apache-2.0.
- Using the typefaces. They are third-party OFL fonts and have nothing to do
  with this policy.

### Never without written permission

- The Marks, or anything confusingly similar, as or in **your** product name,
  company name, domain, app icon, repository name or social handle.
- Modifying the logo: recolouring outside the approved five, distorting,
  rotating, animating, adding effects, re-typesetting the wordmark or tagline,
  or combining it with another mark.
- Implying sponsorship, endorsement, affiliation or official status.
- Merchandise, or advertising for a paid product.
- **Keeping the Marks on a fork.** Fork the system freely — the licence permits
  it — but replace the identity with your own.

### Permissions

**aninda.sh15@gmail.com.** A short, specific email describing exactly what you
want to do gets a faster answer than a general one. Silence is not consent.

---

## When someone redistributes

**Apache-2.0 parts** (tokens, CSS, scripts):

1. Include `LICENSE`.
2. Include `NOTICE`, or the parts of it that apply.
3. Keep the copyright, patent, trademark and attribution notices in what you took.
4. State that you changed the files, if you did.
5. Do not use the GRU953 name or marks to describe your work.

**The writing** under PolyForm Noncommercial:

1. Do not sell it, and do not use it in the course of making money.
2. Pass on `LICENSE-GUIDEBOOK.md`, or the URL for it.
3. Pass on the `Required Notice:` line from `NOTICE`.
4. Do not use the GRU953 name or marks to describe your work.

---

## The fonts

Sora, Noto Sans, Noto Sans Bengali, Anek Bangla and JetBrains Mono are SIL OFL
1.1, and each font's own `OFL.txt` must travel with it. Subsetting and instancing
a variable font are permitted modifications. The one obligation that catches
people out: where a font declares a **Reserved Font Name**, a modified copy may
not keep that name. None of the fonts used here declares one.

---

## Checklist

- [ ] `LICENSE` present and byte-identical to canonical Apache-2.0.
- [ ] `NOTICE` present, and it travels with any Apache-2.0 redistribution.
- [ ] `LICENSE-GUIDEBOOK.md` present if the repository ships GRU953 long-form writing.
- [ ] The README names both licences and reserves the marks.
- [ ] Nothing anywhere calls the whole kit "open source".
- [ ] PolyForm is described as *source-available*, not open source.
- [ ] Any bundled font has its `OFL.txt` beside it.
- [ ] "Not legal advice" appears wherever the licence position is explained.
