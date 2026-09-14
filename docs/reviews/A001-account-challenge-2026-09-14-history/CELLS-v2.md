# A001 cell list, revision 2 — the pre-registration

Frozen with `STAGING-v2.md`. **Measured** throughout: every row index, record
id and target id below was re-derived from the pinned JSON, not copied from
`STAGING.md`. Assessment columns do not appear here; they belong to
`WORKSHEET.md` and are published empty.

**Pins** (all five re-hashed by the adversarial review, exact):

| artifact | sha256 |
|---|---|
| `experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-golden/use_table.json` | `875d674f85f95f09eb1be1354c194f8a79c04298a0556033df52781bef8c723a` |
| `…/use-table-full/use_table.json` | `39981b3c1923472243d89c7c78e0e0ded99bc6a7d9eef451fa46e798caca0a4f` |
| `experiments/diagnostics/C001-contrast-triple/occurrence-01/comparison.json` | `00452db2586b5f33e3eed58c8a7d01efe6da9d6616ce3423fb76d8795af9d31d` |
| `…/occurrence-02/comparison.json` | `4e7ea3894cfe125ba2507dd761f30d13b5226818fe77f9a91665d05c67bc109b` |
| `experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md` | `dcaebaf8336c1943700a762b4836679307349d6ff8dfad082e4cd77e23fd7ae7` |
| `docs/sources/FW5-explanatory-construction.md` (reading edition) | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` |

**Cell criterion (§3, revised).** One row of a published use table whose
**referring record carries a non-empty `bearing` field** and which names a
declared target record. v1's criterion was the referring record's
`type: "objection"`; the two do not pick out the same rows, which is why one
cell is added below with its reason. **The v1 list of 32 is retained** — in
`STAGING.md` §5(b) and as sub-register A here — exactly as P7 requires.

---

## Sub-register A — 32 cells, referring record typed `objection` with a non-empty `bearing`

*This is the v1 list, unchanged, and the adversarial review verified it row by
row against the pinned JSON.*

| # | source table | row | referring | target |
|---|---|---|---|---|
| A01 | H005 golden | 0 | `objection#o1` | `account#c1` |
| A02 | H005 golden | 1 | `objection#o1` | `account#c2` |
| A03 | H005 golden | 2 | `objection#o2` | `account#c2` |
| A04 | H005 golden | 3 | `objection#o3` | `account#c2` |
| A05 | H005 golden | 4 | `objection#o3` | `account#c3` |
| A06 | H005 golden | 10 | `response#k3` | `rival#r6` |
| A07 | H005 golden | 11 | `response#k3` | `rival#r9` |
| A08 | H005 golden | 13 | `response#k7` | `rival#r9` |
| A09 | H005 golden | 16 | `carry#n3` | `response#k2` |
| A10 | H005 golden | 17 | `carry#n3` | `response#k7` |
| A11 | F001 occ-01 | 0 | `objection#o1` | `account#c1` |
| A12 | F001 occ-01 | 1 | `objection#o1` | `account#c2` |
| A13 | F001 occ-01 | 2 | `objection#o1` | `account#c3` |
| A14 | F001 occ-01 | 3 | `objection#o1` | `account#c4` |
| A15 | F001 occ-01 | 4 | `objection#o2` | `account#c6` |
| A16 | F001 occ-01 | 5 | `objection#o2` | `account#c3` |
| A17 | F001 occ-01 | 6 | `objection#o2` | `account#c4` |
| A18 | F001 occ-01 | 7 | `objection#o3` | `account#c2` |
| A19 | F001 occ-01 | 8 | `objection#o3` | `account#c5` |
| A20 | F001 occ-01 | 19 | `carry#r5` | `response#m5` |
| A21 | F001 occ-01 | 20 | `carry#r6` | `account#c3` |
| A22 | F001 occ-01 | 21 | `carry#r6` | `account#c4` |
| A23 | F001 occ-01 | 22 | `carry#r6` | `account#c6` |
| A24 | F001 occ-05 | 3 | `objection#o1` | `account#u1` |
| A25 | F001 occ-05 | 4 | `objection#o2` | `account#u1` |
| A26 | F001 occ-05 | 5 | `objection#o2` | `account#c4` |
| A27 | F001 occ-05 | 6 | `objection#o3` | `account#u1` |
| A28 | F001 occ-05 | 7 | `objection#o3` | `account#c3` |
| A29 | F001 occ-05 | 8 | `objection#o4` | `account#c2` |
| A30 | F001 occ-05 | 9 | `objection#o5` | `account#u1` |
| A31 | F001 occ-05 | 10 | `objection#o5` | `account#c1` |
| A32 | F001 occ-07 | 1 | `rival#r5` | `account` — **target record id absent** |

**A32's resolver note, quoted:** "bare exposed-artifact label with no
'#LocalName'; local resolution was tried first, so it resolves to the owning
artifact (deviation D2)". A32 is pre-declared **X0 NOT-RECONSTRUCTIBLE** on
the missing target record id, not read and then failed.

**Zero-row occurrences.** F001 occurrences **02, 03, 04, 06 and 08** contribute
**zero** cells; their use tables carry zero rows. That is a fact about those
documents' authored refs, not about their authors. It is recorded as a cell
count of zero and never as a negative finding.

---

## Sub-register B — 1 cell, bearing-carrying record not typed `objection`

| # | source table | row | referring | target | type | `bearing`, verbatim |
|---|---|---|---|---|---|---|
| B01 | F001 occ-01 | 12 | `carry#r2` | `response#m2` | `claim` | "narrows the commitment to a cost rule with an explicit scope, rather than a trigger condition" |

**Reason for the addition, recorded as P7 requires.** §3's unit definition is a
non-empty `bearing` field; this row has one, and v1's list was built on the
`type` field instead, so the pre-registration did not match its own definition.
The row's own `text` alleges a defect of its target — "The prior m2's condition
… was not licensed by the prior body, which said choose by cost" — so it is
criticism-shaped in :609's sense while being typed `claim`. **B01 is itself a
datum for the (K1)-mapping test**: the FCL-1 `type` field does not track
FW5:609's criticism constituents. It is kept in its own sub-register so that
every count from v1 remains recoverable.

**Total: 33 cells.**

---

## Declared-use rows — a separate register, never cells (12)

`use-table-golden` rows 5, 6, 7, 8, 9, 12, 14, 15, 18, 19, 20, 21, carried by
`claim`, `use` and `problem` records with no `bearing` field.

| row | type | referring | target |
|---|---|---|---|
| 5 | claim | `rival#r1` | `account` (record id absent) |
| 6 | claim | `response#k1` | `account#c2` |
| 7 | claim | `response#k1` | `objection#o2` |
| 8 | claim | `response#k2` | `rival#r7` |
| 9 | claim | `response#k2` | `account#c3` |
| 12 | use | `response#k6` | `rival#r6` |
| 14 | claim | `carry#n1` | `response#k5` |
| 15 | claim | `carry#n1` | `response#k7` |
| 18 | use | `carry#n4` | `response#k5` |
| 19 | claim | `carry#n5` | `response#k9` |
| 20 | problem | `carry#n6` | `response` (record id absent) |
| 21 | use | `carry#n7` | `response#k8` |

FW5:640 makes a declared field a delivery fact. These rows are read only to
record what the language declared. **They can supply no finding against
anything.**

---

## E2 — the equivariance check and what it can reach

**Scope.** The C001 ORIGINAL objection block against the RECODING block, unit
by unit over the **fcl arm's 50 units** of `RECODING_TABLE.md` (28 `B.*` body
units + 22 `K.*` record-field units over records o1, o2, o3 of
`daily/mini_fcl/cycle01/objection`). The table's other **35 units** (20 `B.*` +
15 `C.*`) are the `mini_prose` arm and bear on no cell here.

**Reachable cells — five, and only these.**

| # | cell | why reachable |
|---|---|---|
| A01 | golden row 0 | referring record `o1` of the objection document, covered by `K.o1.*` |
| A02 | golden row 1 | `o1`, same |
| A03 | golden row 2 | `o2`, covered by `K.o2.*` |
| A04 | golden row 3 | `o3`, covered by `K.o3.*` |
| A05 | golden row 4 | `o3`, same |

**Unreachable, stated so no reader tries.** Golden rows 10, 11, 13 refer from
the `response` node (`k3`, `k7`) and rows 16, 17 from the `carry` node (`n3`);
the recoding table covers neither node. **No F001 cell is reachable by E2 at
all** — the table is for the C001/H005 occurrence-01 objection document.

**Provenance of the ORIGINAL block.** C001 PLAN:184-188 — the H005 objection
document "exactly as the H005 `response` node saw it: the same `body` and
`commitments` bytes, projected by the same `project()` with view `both`";
`prepare` refuses unless the case bytes equal the occurrence artifact bytes
(`ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES`). This is identity of the
**projection**, not of the artifact file.

---

## E3 — non-evaluable, declared in advance, excluded from every side

| exclusion | measured content |
|---|---|
| C001 occurrence-01 `deepseek-flash` × `fcl` | **19 of 20 coordinates unusable at the 8192 ceiling: 8 PARTIAL at `finish_reason` "length" with `completion_tokens` exactly 8192, and 11 FAILED with `NO_PUBLIC_CONTENT` carrying no `finish_reason` and no usage at all.** `COMPARISON.md` table lines 38-57, "Unresolved in this cell" line 59; terminal reading at `material-occurrence-02.json` line 1519. The ceiling is an inference for the 11 FAILED rows and is labelled as one. |
| `ollama-glm-5.3` × `fcl` | the single PARTIAL coordinate, CONTROL rep2 |
| `use-table-full` | 12 nodes whose commitment surface was not read (`nodes_not_read`): 10 `prose_not_parsed` + 2 `unavailable_decode_failure` |
| the eight F001 use tables | `nodes_not_read` = 7, 8, 6, 5, 6, 9, 6, 7 |

FW5:688 — "The inability to evaluate a proposition is not a falsifying
observation of the proposition." No cell above is counted on either side.

---

## Outcome classes and the charge rule

Both are declared in `STAGING-v2.md` §5(b) **before** any cell is read, and are
reproduced in the published `PLAN.md` unchanged. Every cell lands in exactly
one of **X0 NOT-RECONSTRUCTIBLE / X1 AGREE-POSITIVE / X2 DISAGREE-SUFFICIENCY /
X3 DISAGREE-NECESSITY / X4 UNRESOLVED / X5 NO FINDING**, and no cell may charge
Account alone.
