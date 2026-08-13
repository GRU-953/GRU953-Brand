# GRU953 — naming

> **A note on the sources named here.** `BRAND-SPEC.md`, `DESIGN-RULES.md`,
> `LICENSING-EXPLAINED.md`, `TRADEMARKS.md` and `LOGO-USAGE.md` live in the GRU953
> brand kit, which is a separate deliverable and does **not** ship inside this
> plugin. Where one of them is cited below, the rule it decides is stated here in
> full — the citation records where the decision was made, not a file you need.


## The brand name itself

`GRU953` — **one word, uppercase, no hyphen, no space, never translated.**

| Context | Form | Why |
|---|---|---|
| Prose, interfaces, documents, anywhere a reader sees it | `GRU953` | The name. |
| Filenames, packages, folders, domains | `gru953` | A filesystem convention, not the name. |
| The GitHub account | `GRU-953` | A platform requirement, not the name. |
| Said aloud | "Groo-nine-five-three" | One word. |

Never `Gru953`, `GRU 953`, `gru-953`, `GRU_953` or `953` alone in prose.

## The reading risk, and the rule that answers it

To a developer audience, **"GRU" already means *Gated Recurrent Unit*** — a
standard neural-network component. Someone skimming a GitHub profile can read
"GRU953" as the name of an AI model.

This is a *reading* risk, not a legal one, and the name stays. The mitigation is
a rule, not a hope:

> **Wherever GRU953 first appears, follow it immediately with what it is.**

- ✅ "GRU953 — a solo software studio."
- ✅ "GRU953 is my one-person software studio."
- ❌ "GRU953 v2.1 released."  *(reads as a model release)*

That is also why the kit ships lockups with the tagline built into the artwork:
the reading is settled before it can drift.

The three other "GRU" associations — Russian military intelligence, the
*Despicable Me* character, São Paulo's airport code — were checked and are low
risk, because none of them is ever written with digits after it.

---

## Naming a product

GRU953 is a **parent brand over apps that carry their own names**. So the
default is the **endorsement form**.

> **`<Name> by GRU953`** on first mention, then the name alone.

- ✅ `Ledger by GRU953`, then simply `Ledger`
- ✅ `Tally by GRU953`
- ❌ `GRU-Ledger`, `Gru953Ledger`, `953 Ledger`, `LedgerGRU`
- ❌ `Ledgerly`, `Ledgerify`, `Ledgr` — invented words age badly and are hard to
  say in two languages

**One exception.** When a name is too generic to stand alone in a listing —
`Notes`, `Files`, `Camera` — put the studio first: `GRU953 Notes`. Never both
forms in the same document.

This settled a disagreement that once existed between two documents in the kit.
If a GRU953 document ever contradicts this rule, **this rule wins**: the endorsement form is the decision, recorded in the brand kit's `BRAND-SPEC.md` §9 and restated here in full so a plugin user never has to open that file to settle it.

### The written form, by surface

| Where | Form | Example |
|---|---|---|
| First mention in prose | `<Name> by GRU953` | "Ledger by GRU953 keeps a record of daily takings." |
| Every mention after | `<Name>` alone | "Ledger works offline." |
| App store or directory title | `<Name> by GRU953` | "Ledger by GRU953" |
| Inside the app's own interface | `<Name>` alone, with the bird | "Ledger" |
| Repository, package, folder, domain | lowercase, hyphens | `gru953-ledger`, `ledger.gru953.dev` |
| Legal, invoices, licence headers | `<Name>, a GRU953 product` | "Ledger, a GRU953 product" |

### What makes a good product name here

A real word; sayable by a Bangla speaker and an English speaker without
hesitation; spellable after hearing it once; and descriptive of what the thing
does. Check three things before committing: is the `.com` or `.dev` free, is the
npm and PyPI name free, and does the word mean something unfortunate in Bangla?

---

## Versioning

**The brand kit has no version number.** It is identified by the date on the
guidebook's cover; anything dated later supersedes anything dated earlier. There
is no changelog and no release history for the kit.

**Products are different.** An app GRU953 ships uses Semantic Versioning
normally — `2.4.1`, `2.5.0`, `3.0.0` — and its release notes put the version and
the date on the first line. The kit's own rule does not apply to them.

---

## Availability, checked 13 August 2026

Verified by RDAP against the registries themselves, and by each package
registry's own API. **These go stale quickly** — re-check before acting.

| Name | Status |
|---|---|
| `gru953.com` `.dev` `.io` `.org` `.net` | All **unregistered** |
| npm `gru953` | **Unregistered** |
| PyPI `gru953` | **Unregistered** |
| US trademark register | No result for `gru953` |
| GitHub / X handle `gru953` | Appears unclaimed — a strong signal, not a guarantee |
| Registers outside the USA | **Unknown.** Bangladesh's DPDT, EUIPO and WIPO all need a human search. |

**No trademark search was performed.** Nothing here says the GRU953 name or mark
is free of prior registered rights in any jurisdiction.

---

## Checklist

- [ ] `GRU953` spelled as one uppercase word everywhere a reader sees it.
- [ ] First mention followed immediately by what it is.
- [ ] Product names use `<Name> by GRU953`, or the prefix form only when generic.
- [ ] Never both forms in one document.
- [ ] Lowercase `gru953` only in paths, packages and domains.
- [ ] No version number attached to the brand kit itself.
