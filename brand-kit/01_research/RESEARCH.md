# GRU953 — research and verification

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

**Checked on 13 August 2026.** Everything below was verified on that date against a primary
source, or is marked as unverified. Nothing here is asserted from memory. Availability
facts about domains and package names go stale quickly; the date matters.

---

## 1. The name

### The reading risk, stated plainly

To a developer audience, **"GRU" already means *Gated Recurrent Unit***, a standard
neural-network component. Someone skimming a GitHub profile can read "GRU953" as the name
of an AI model rather than a studio.

This is a real reading risk, not a legal one. It was measured and the name was kept
deliberately, because:

- the risk is *misreading*, not *confusion with a competitor*, and misreading is fixable
  with one sentence of context;
- the digits make the string unique in practice — no other "GRU" association is ever
  written with numbers after it;
- changing a name that already carries the owner's history has a cost of its own.

**The mitigation is a rule, not a hope:** the tagline sits directly under the wordmark
everywhere, so the reading is settled before it can drift. That rule is why the kit ships
lockups with the tagline built in.

### The other "GRU" associations, and why each is low risk

| Association | Why it does not collide |
|---|---|
| Russian military intelligence (GRU) | Never written with digits; the context is geopolitics, not software |
| *Despicable Me* character | A given name in a children's film; no digits, no software context |
| São Paulo–Guarulhos airport (IATA: GRU) | A three-letter airport code; digits after it are flight numbers, not part of the code |

*Method: reasoned assessment of context, not a trademark search. See section 5.*

## 2. Availability — domains and package names

Checked on **13 August 2026** by RDAP (the registry protocol that replaced WHOIS) and by
the registries' own APIs. A `404` from a registry's RDAP service means "no such registration".

| Name | Where | Method | Result on 13 Aug 2026 |
|---|---|---|---|
| `gru953.com` | Verisign, via rdap.org | RDAP lookup | **Unregistered** |
| `gru953.dev` | Google Registry, via rdap.org | RDAP lookup | **Unregistered** |
| `gru953.org` | PIR, via rdap.org | RDAP lookup | **Unregistered** |
| `gru953.net` | Verisign, via rdap.org | RDAP lookup | **Unregistered** |
| `gru953.io` | Identity Digital RDAP | RDAP lookup | **Unregistered** |
| `gru953` | npm registry | `registry.npmjs.org` returned 404 | **Unregistered** |
| `gru953` | PyPI | `pypi.org/pypi/gru953/json` returned 404 | **Unregistered** |

**These will not stay free.** Registering the domain and reserving the two package names is
the cheapest brand-protection action available, and it expires as an opportunity the moment
someone else takes it.

## 3. The licences — what was checked, and what was found

### Apache License, Version 2.0 — for the system

- **OSI approval:** confirmed present on the Open Source Initiative's approved licence
  list on 13 August 2026, categorised as "Popular / Strong Community".
  <https://opensource.org/licenses>
- **Text:** fetched from <https://www.apache.org/licenses/LICENSE-2.0.txt> and compared
  byte-for-byte against the file shipped in `08_guidebook/governance/LICENSE`. **Identical.**
  MD5 `3b83ef96387f14655fc854ddc3c6bd57`, 202 lines, 11,358 bytes.
- **Why it was chosen:** section 6 withholds trademark permission without needing a
  separate notice, and it carries an express patent grant with a retaliation clause, which
  MIT and BSD do not.

### PolyForm Noncommercial License 1.0.0 — for the book and the writing

- **OSI approval:** **not approved, and will not be.** Confirmed against the OSI list on
  13 August 2026 — no PolyForm licence appears on it. The Open Source Definition forbids
  restricting a field of use, and "noncommercial only" is exactly that restriction. The
  correct description of this licence is **source-available**, not open source.
- **SPDX identifier:** `PolyForm-Noncommercial-1.0.0`, listed by SPDX.
  <https://spdx.org/licenses/PolyForm-Noncommercial-1.0.0.html>
- **Text:** fetched verbatim from the PolyForm Project's own release tag,
  <https://github.com/polyformproject/polyform-licenses/blob/1.0.0/PolyForm-Noncommercial-1.0.0.md>,
  and shipped unmodified as `LICENSE-GUIDEBOOK.md`. 4,563 bytes, SHA-256
  `c0ea4a896d2c8c394b29f9427589996db826cd501c512279ff0ed3ef48fabbe5`.
- **Known limit:** the PolyForm licences are drafted for *software* — their text says "the
  software" throughout. Applying one to a document works by defining the document as the
  licensed work, which `NOTICE` does. **No lawyer has reviewed this application.**

### SIL Open Font License 1.1 — for the typefaces

Sora, Noto Sans, Noto Sans Bengali and JetBrains Mono all ship under OFL 1.1, and each
font's own `OFL.txt` travels with it in `05_type/source-fonts/`. OFL 1.1 is OSI-approved.
The one obligation that catches people out: where a font declares a **Reserved Font Name**,
a modified copy may not keep that name.

## 4. Why the split, in one line

The system is a component and is genuinely open, so it takes an OSI licence. The book is
GRU953's own identity and should not be sellable by someone else, so it takes a
noncommercial one. The marks are neither, so they are not licensed at all.

## 5. What could not be verified — stated, not hidden

- **No trademark search was performed.** Nothing here says the GRU953 name or mark is
  free of prior registered rights in any jurisdiction. A registry search is a separate
  piece of work and needs a professional.
- **No legal review.** Both licences are shipped verbatim, which is the safe way to use
  them, but the *choice* of licence and the way the kit is split between them have not
  been reviewed by a lawyer.
- **Availability is a snapshot.** Every result in section 2 was true at the moment it was
  checked on 13 August 2026 and could be false tomorrow.
- **No screen-reader testing with a real user.** Contrast is computed and proved in
  `04_colour/CONTRAST.md`; lived accessibility is not the same thing.
- **Social-handle availability was not re-checked** on this pass. Handles turn over faster
  than domains and a stale "available" is worse than no claim.

---

## Sources

- Open Source Initiative — approved licence list: <https://opensource.org/licenses>
- Apache License, Version 2.0 (canonical text): <https://www.apache.org/licenses/LICENSE-2.0.txt>
- PolyForm Noncommercial License 1.0.0: <https://polyformproject.org/licenses/noncommercial/1.0.0>
- PolyForm licence texts, release 1.0.0: <https://github.com/polyformproject/polyform-licenses/blob/1.0.0/PolyForm-Noncommercial-1.0.0.md>
- SPDX licence list entry: <https://spdx.org/licenses/PolyForm-Noncommercial-1.0.0.html>
- SIL Open Font License: <https://openfontlicense.org>
- RDAP bootstrap and registry services, via <https://rdap.org> and Identity Digital's RDAP endpoint
- npm registry API: <https://registry.npmjs.org/gru953> · PyPI JSON API: <https://pypi.org/pypi/gru953/json>

Copyright © 2026 Aninda Sundar Howlader (GRU953).
