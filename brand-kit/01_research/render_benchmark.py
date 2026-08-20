#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""GRU953 — render 01_research/BENCHMARK.md from data. Nothing in the benchmark's tally
or per-criterion verdict is typed by hand in the Markdown; every number here is generated
from 01_research/_data/criteria.json and 01_research/findings.json.

WHY THIS EXISTS
---------------
A tally a human typed once is the least reliable sentence in a repository, because nobody
re-reads it after the numbers move. The old kit's own CI history has three different counts
for the same check (164, 167, "the kit's own verification") because each was typed once by
a different person on a different day. This script exists so a benchmark score can never
drift from the data that produced it: the counts below are len() of Python lists, not
someone's memory of how many there were.

    python3 scripts/render_benchmark.py            # write 01_research/BENCHMARK.md
    python3 scripts/render_benchmark.py --check     # compare only; exit 1 if stale

VERDICT RULE
------------
A criterion's `baseline_verdict` may be: meets, partial, gap, not-applicable, untested.
"untested" is counted as a gap in the headline tally -- the score cannot be flattered by
not having run a check yet. A criterion whose statement changes between two runs of this
repository's history is a bug: retire it (status: retired) and add a new id instead of
editing the wording, or the three convergence rounds are not comparable.
"""
import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
CRITERIA_PATH = HERE / "_data" / "criteria.json"
FINDINGS_PATH = HERE / "findings.json"
OUT_PATH = HERE / "BENCHMARK.md"

VERDICT_LABEL = {
    "meets": "Meets",
    "partial": "Partial",
    "gap": "Gap",
    "not-applicable": "N/A",
    "untested": "Untested (counts as a gap)",
}


def load():
    with open(CRITERIA_PATH, encoding="utf-8") as f:
        criteria = json.load(f)
    with open(FINDINGS_PATH, encoding="utf-8") as f:
        findings = json.load(f)
    findings_by_id = {f_["id"]: f_ for f_ in findings["findings"]}
    return criteria, findings, findings_by_id


def tally(criteria):
    counts = {"meets": 0, "partial": 0, "gap": 0, "not-applicable": 0, "untested": 0}
    for c in criteria["criteria"]:
        v = c["baseline_verdict"]
        counts[v] = counts.get(v, 0) + 1
    return counts


def render(criteria, findings, findings_by_id):
    L = []
    L.append("# GRU953 — the benchmark")
    L.append("")
    L.append("GENERATED — do not hand-edit. Produced by `scripts/render_benchmark.py` from")
    L.append("`01_research/_data/criteria.json` and `01_research/findings.json`. To change a")
    L.append("verdict or add a finding, edit those files and re-run the script.")
    L.append("")
    L.append(f"সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.")
    L.append("")
    counts = tally(criteria)
    total = sum(counts.values())
    real_gaps = counts["gap"] + counts["untested"]
    L.append(f"**{counts['meets']} meets · {counts['partial']} partial · {real_gaps} gap "
             f"(including {counts['untested']} not yet tested) · {counts['not-applicable']} "
             f"not applicable yet — out of {total} criteria, frozen {criteria['frozen_on']}, "
             f"before this rebuild's own artefacts existed to test against.**")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 0. What this benchmark is, and is not")
    L.append("")
    L.append("This compares GRU953 against **published guidance** from other organisations —")
    L.append("never against how well those organisations follow their own guidance, and never")
    L.append("against their private brand books, because neither Apple nor Google publishes")
    L.append("one. Every criterion below names the test that decides it, written and frozen")
    L.append(f"on **{criteria['frozen_on']}**, before the rebuilt kit existed — so a verdict")
    L.append("cannot be graded to an answer it already knew. `baseline_verdict` is scored")
    L.append("against the kit as it stood **before** this rebuild (13 August 2026); it exists")
    L.append("so the rebuild's own progress can be measured, not just claimed.")
    L.append("")
    L.append(f"Research behind this benchmark: **{len(findings['findings'])} findings**, each")
    L.append(f"carrying a primary source, a retrieval date, and — for any numeric claim — a")
    L.append(f"verbatim quote. **{len(findings['could_not_verify'])} questions** could not be")
    L.append("verified from a primary source and are listed as such, not guessed at. Full data:")
    L.append("`01_research/findings.json`.")
    L.append("")
    L.append("---")
    L.append("")

    groups = []
    seen = set()
    for c in criteria["criteria"]:
        if c["group"] not in seen:
            groups.append(c["group"])
            seen.add(c["group"])

    for group in groups:
        L.append(f"## {group}")
        L.append("")
        rows = [c for c in criteria["criteria"] if c["group"] == group]
        for c in rows:
            L.append(f"### {c['id']} — {VERDICT_LABEL[c['baseline_verdict']]}")
            L.append("")
            L.append(f"**Claim:** {c['statement']}")
            L.append("")
            L.append(f"**Test:** {c['test']}")
            L.append("")
            if c.get("baseline_note"):
                L.append(f"**Baseline:** {c['baseline_note']}")
                L.append("")
            for fid in c.get("evidence_finding_ids", []):
                f_ = findings_by_id.get(fid)
                if not f_:
                    continue
                L.append(f"> {f_['claim']}")
                # source_title is not required by the research schema -- several streams
                # omitted it. Fall back to the publisher name rather than crashing on a
                # KeyError, since a missing label is a formatting gap, not a reason to
                # lose the citation.
                title = f_.get("source_title") or f_.get("publisher", "source")
                if f_.get("quoted_line"):
                    L.append(f"> — *“{f_['quoted_line']}”* ({title},")
                    L.append(f">   {f_['source_url']}, read {f_['retrieved_date']})")
                else:
                    L.append(f"> — {title}, {f_['source_url']}, "
                              f"read {f_['retrieved_date']}")
                L.append(">")
            L.append("")
        L.append("---")
        L.append("")

    L.append("## What could not be verified")
    L.append("")
    L.append("Stated rather than silently dropped, grouped by research stream:")
    L.append("")
    by_stream = {}
    for item in findings["could_not_verify"]:
        by_stream.setdefault(item["stream"], []).append(item["question"])
    for stream, qs in by_stream.items():
        L.append(f"**{stream}**")
        for q in qs:
            L.append(f"- {q}")
        L.append("")

    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    criteria, findings, findings_by_id = load()
    rendered = render(criteria, findings, findings_by_id)

    if args.check:
        if not OUT_PATH.exists():
            print(f"{OUT_PATH} does not exist — run without --check first.")
            return 2
        current = OUT_PATH.read_text(encoding="utf-8")
        if current != rendered:
            print("BENCHMARK.md is stale — it does not match criteria.json + findings.json.")
            print("Run: python3 scripts/render_benchmark.py")
            return 1
        print(f"BENCHMARK.md in step with {len(criteria['criteria'])} criteria and "
              f"{len(findings['findings'])} findings.")
        return 0

    OUT_PATH.write_text(rendered, encoding="utf-8")
    counts = tally(criteria)
    print(f"wrote {OUT_PATH.name} — {len(criteria['criteria'])} criteria, "
          f"{counts['meets']} meets / {counts['partial']} partial / "
          f"{counts['gap'] + counts['untested']} gap / {counts['not-applicable']} n/a")
    return 0


if __name__ == "__main__":
    sys.exit(main())
