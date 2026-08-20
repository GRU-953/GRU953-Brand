# Mark rebuild — Round 1

**This is Round 1 of an iterative process, not the finished rebuild.** Nothing in this
folder replaces `brand-kit/03_logo/GRU953-bird.svg`, which keeps shipping unchanged.
Do not present `round1-candidate.svg` to the owner as "the new mark" — present it as
what it is: the first honest attempt, with real numbers, at the plan's own explicit
instruction that the bird's geometry be rebuilt on a construction grid.

## What was tried

Three independent construction approaches were built and measured against
`check_rebuild_fidelity.py` (the fidelity harness fixed in `v0.12.0`, before any
rebuild existed to be judged against it):

| Approach | Idea | Targets passing (of 5) |
|---|---|---|
| A — snap-and-repair | Trace the original's own shape, simplify, snap to the 64-unit grid, locally repair whatever the snap breaks | 1/5 (facet angle only) |
| B — parametric fan | Build the wing directly from the four measured facet angles as a fan of ribs; fit the rest by tracing | 0/5 |
| **C — boundary-trace-and-rebuild** | Trace the original's rendered outer boundary and each counter, grid-snap, rebuild as a single filled path with 8 holes | **3/5** |

C was independently re-verified (numbers reproduce exactly; all three candidates
re-rendered and visually checked; none has a severed wing — confirmed by an
independent flood-fill connected-components count, not just trusted from each
attempt's own report) and carried forward as the strongest candidate. No hybrid of
the three beat C outright on any checkable piece.

## Round 1 result — `round1-candidate.svg`

```
silhouette_overlap        0.432   (target >= 0.92)   FAIL
contour_deviation_pct     7.637   (target <= 1.5)     FAIL
counters_one_to_one       true    (target True)       PASS
facet_angle_max_dev_deg   0.13    (target <= 1.5)      PASS  (all 4 ribs within 0.01-0.13 deg)
centroid_offset_pct       0.600   (target <= 1.0)      PASS
```

Full detail in `round1-fidelity-report.json`. Visual evidence:
`round1-candidate-1024.png` (the candidate alone), `round1-overlay-vs-original.png`
(original in red, candidate in green, agreement in grey), `round1-candidate-16-zoomed.png`
(the actual 16px floor, nearest-neighbour zoomed).

**Three of five targets pass convincingly** — the counter positions, the facet
angles, and the overall centroid are all faithful to the original, some very
precisely (facet angles within 0.13 degrees; centroid within 0.6%).

**Two targets fail, and the reason is diagnosed, not mysterious.** Look at
`round1-overlay-vs-original.png`: the grey region (agreement) traces the original's
silhouette closely — same wingtip, same tail point, same beak. The green (extra ink
in the candidate) is concentrated in the wing, because the candidate is built as
**one solid dart with 8 holes punched in it** (15.8% ink coverage), where the
original is a **sparse rib-and-slit line drawing** (11.2% ink coverage per
`original-measurements.json`). Closing this gap needs the wing rebuilt as explicit
offset ribs/strips — separate ink shapes with real background between them, not one
solid mass with counters cut out — which is a structurally different construction,
not a parameter to tune. This is the clear, identified next step for Round 2.

## A tension worth the owner's own eye before Round 2

**None of the three Round-1 attempts actually built walls at the three stated
weights (64 / 128 / 192 artboard units) — every one measured a continuous spread of
wall thicknesses instead.** One attempt found an analytic reason why: a wall
between two grid-snapped lines at the wing's own ~26.5-degree slope is fixed by
simple lattice geometry at `sqrt(5) x 64 ~= 143` units, not at 64, 128 or 192 — so a
*perpendicular, uniform* wall of exactly one of those three values does not exist at
that angle on this grid, without redrawing the wing at a much larger scale than
1024x1024 allows. This may be solvable with a different wall-measurement convention
(e.g. "thickness along the grid's own dominant axis," rather than true perpendicular
thickness) or a finer/different construction grid — or it may be a genuine tension
between two of the plan's own numeric rules (16x16 grid, integer stroke multiples,
and the wing's own real facet angles) that is worth raising rather than quietly
resolving one way. **Flagging this here, not deciding it.**

## Recommendation

- Round 2 should rebuild the wing specifically as explicit offset ribs (fixed
  half-width per stroke-weight class, grid-snapped centreline endpoints), keeping
  Round 1's working parts: the counter-placement/search method, the facet-angle
  solution (already excellent), and the head/body/tail tracing.
- The stroke-weight tension above is worth the owner seeing directly, alongside
  `round1-overlay-vs-original.png`, before Round 2 spends further effort assuming
  one resolution over another.
- This has not been shown to the owner yet. Per the plan's own stated process, the
  mark rebuild gets a **human A/B gate** (the owner's own drawing beside the
  rebuild, toggled, before either is treated as final) — Round 1 is real progress
  toward that gate, not a substitute for it.
