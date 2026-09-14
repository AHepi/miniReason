# A001 cell list, revision 3 — the pre-registration, with the bridge branch frozen per cell

Frozen with `STAGING-v3.md`. `CELLS-v2.md` is retained unedited beside it.
**Measured** throughout: every row index, record id, target id and `bearing`
string below was re-derived from the pinned JSON at this revision, not copied
from `CELLS-v2.md`. Assessment columns do not appear here; they belong to
`WORKSHEET.md` and are published empty.

**What is new in revision 3.** (i) The **bridge branch for every one of the 33
cells is frozen here, before the reading**, because §3 now discloses that the
bridge rule is **not independent of the cells** (F36) — a post-hoc rule whose
per-cell application is left open would be fitted twice. (ii) Two cells whose
v2 status a reviewer could have read either way are **pre-declared**: golden
rows 0/1 (F37) and B01 (F47). (iii) The `RECODING_TABLE.md` record coverage is
corrected from three records to eight (F39).

**Pins** (all five re-hashed by both adversarial reviews, exact):

| artifact | sha256 |
|---|---|
| `experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-golden/use_table.json` | `875d674f85f95f09eb1be1354c194f8a79c04298a0556033df52781bef8c723a` |
| `…/use-table-full/use_table.json` | `39981b3c1923472243d89c7c78e0e0ded99bc6a7d9eef451fa46e798caca0a4f` |
| `experiments/diagnostics/C001-contrast-triple/occurrence-01/comparison.json` | `00452db2586b5f33e3eed58c8a7d01efe6da9d6616ce3423fb76d8795af9d31d` |
| `…/occurrence-02/comparison.json` | `4e7ea3894cfe125ba2507dd761f30d13b5226818fe77f9a91665d05c67bc109b` |
| `experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md` | `dcaebaf8336c1943700a762b4836679307349d6ff8dfad082e4cd77e23fd7ae7` |
| `docs/sources/FW5-explanatory-construction.md` (reading edition, 1,502 lines) | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` |

**Cell criterion (§3).** One row of a published use table whose **referring
record carries a non-empty `bearing` field** and which names a declared target
record. **The v1 list of 32 is retained** — in `STAGING.md` §5(b) and as
sub-register A here — exactly as P7 requires.

**Branch legend (§3).** (b1) DISCRIMINATION → inferential identification;
(b2) RIVAL-FRAME → inferential identification; (b3) PRESCRIPTION → achievement
of an aim; (b6) INCONSISTENCY → impossibility; (b7) MISSING-DISTINCTION →
inferential identification; (b4) MISREADING → inferential identification,
`bridge-strained`; (b5) → none, cell is **X4 UNRESOLVED** and read no further.
Match test: a branch fires only where the `bearing` text **explicitly asserts**
that branch's form.

---

## Sub-register A — 32 cells, referring record typed `objection` with a non-empty `bearing`

*This is the v1 list, unchanged. Both reviews verified it row by row against the
pinned JSON.*

| # | table | row | referring → target | branch | \(\kappa\) | pre-declared class |
|---|---|---|---|---|---|---|
| A01 | H005 golden | 0 | `objection#o1` → `account#c1` | **(b5)** | — | **X4** |
| A02 | H005 golden | 1 | `objection#o1` → `account#c2` | **(b5)** | — | **X4** |
| A03 | H005 golden | 2 | `objection#o2` → `account#c2` | (b1) | inferential identification | open |
| A04 | H005 golden | 3 | `objection#o3` → `account#c2` | (b3) | achievement of an aim | open |
| A05 | H005 golden | 4 | `objection#o3` → `account#c3` | (b3) | achievement of an aim | open |
| A06 | H005 golden | 10 | `response#k3` → `rival#r6` | (b1) | inferential identification | open |
| A07 | H005 golden | 11 | `response#k3` → `rival#r9` | (b1) | inferential identification | open |
| A08 | H005 golden | 13 | `response#k7` → `rival#r9` | (b1) | inferential identification | open |
| A09 | H005 golden | 16 | `carry#n3` → `response#k2` | (b4) `bridge-strained` | inferential identification | open |
| A10 | H005 golden | 17 | `carry#n3` → `response#k7` | (b4) `bridge-strained` | inferential identification | open |
| A11 | F001 occ-01 | 0 | `objection#o1` → `account#c1` | (b2) | inferential identification | open |
| A12 | F001 occ-01 | 1 | `objection#o1` → `account#c2` | (b2) | inferential identification | open |
| A13 | F001 occ-01 | 2 | `objection#o1` → `account#c3` | (b2) | inferential identification | open |
| A14 | F001 occ-01 | 3 | `objection#o1` → `account#c4` | (b2) | inferential identification | open |
| A15 | F001 occ-01 | 4 | `objection#o2` → `account#c6` | **(b6)** | impossibility | open |
| A16 | F001 occ-01 | 5 | `objection#o2` → `account#c3` | **(b6)** | impossibility | open |
| A17 | F001 occ-01 | 6 | `objection#o2` → `account#c4` | **(b6)** | impossibility | open |
| A18 | F001 occ-01 | 7 | `objection#o3` → `account#c2` | **(b5)** | — | **X4** |
| A19 | F001 occ-01 | 8 | `objection#o3` → `account#c5` | **(b5)** | — | **X4** |
| A20 | F001 occ-01 | 19 | `carry#r5` → `response#m5` | **(b5)** | — | **X4** |
| A21 | F001 occ-01 | 20 | `carry#r6` → `account#c3` | **(b6)** | impossibility | open |
| A22 | F001 occ-01 | 21 | `carry#r6` → `account#c4` | **(b6)** | impossibility | open |
| A23 | F001 occ-01 | 22 | `carry#r6` → `account#c6` | **(b6)** | impossibility | open |
| A24 | F001 occ-05 | 3 | `objection#o1` → `account#u1` | **(b5)** | — | **X4** |
| A25 | F001 occ-05 | 4 | `objection#o2` → `account#u1` | **(b5)** | — | **X4** |
| A26 | F001 occ-05 | 5 | `objection#o2` → `account#c4` | **(b5)** | — | **X4** |
| A27 | F001 occ-05 | 6 | `objection#o3` → `account#u1` | **(b5)** | — | **X4** |
| A28 | F001 occ-05 | 7 | `objection#o3` → `account#c3` | **(b5)** | — | **X4** |
| A29 | F001 occ-05 | 8 | `objection#o4` → `account#c2` | **(b5)** | — | **X4** |
| A30 | F001 occ-05 | 9 | `objection#o5` → `account#u1` | **(b5)** | — | **X4** |
| A31 | F001 occ-05 | 10 | `objection#o5` → `account#c1` | **(b5)** | — | **X4** |
| A32 | F001 occ-07 | 1 | `rival#r5` → `account` — **target record id absent** | — *(bridge not consulted)* | — | **X0** |

**A32's resolver note, quoted:** "bare exposed-artifact label with no
'#LocalName'; local resolution was tried first, so it resolves to the owning
artifact (deviation D2)". A32 is pre-declared **X0 NOT-RECONSTRUCTIBLE** on the
missing target record id, not read and then failed; X0's condition fires before
the bridge is consulted.

## Sub-register B — 1 cell, bearing-carrying record not typed `objection`

| # | table | row | referring → target | type | branch | pre-declared class |
|---|---|---|---|---|---|---|
| B01 | F001 occ-01 | 12 | `carry#r2` → `response#m2` | `claim` | **(b5)** | **X4** |

`bearing`, verbatim: "narrows the commitment to a cost rule with an explicit
scope, rather than a trigger condition".

**Why B01 is in the register and why it is unreadable (F47).** §3's unit
definition is a non-empty `bearing` field; this row has one, and v1's list was
built on the `type` field instead, so the pre-registration did not match its own
definition — that is why it was added at v2. But **the bridge reads the
`bearing` field alone**, and this `bearing` alleges no defect and matches no
branch. v2 justified the cell by its `text` ("The prior m2's condition … was not
licensed by the prior body"), which §3 forbids the bridge to read. **B01 is
therefore retained as a datum about the FCL-1 `type` field — it does not track
FW5:609's criticism constituents — and is pre-declared unreadable.** Extending
the bridge to `text` was considered and declined (§3).

**Total: 33 cells.**

---

## The frozen branch distribution

**Coverage fact about A001's own bridge. Not evidence, on any side, under
§5(b) rule 6.**

| branch | cells | which |
|---|---|---|
| (b1) DISCRIMINATION | **4** | A03, A06, A07, A08 |
| (b2) RIVAL-FRAME | **4** | A11, A12, A13, A14 |
| (b3) PRESCRIPTION | **2** | A04, A05 |
| (b6) INCONSISTENCY *(new)* | **6** | A15, A16, A17, A21, A22, A23 |
| (b7) MISSING-DISTINCTION *(new)* | **0** | **none** |
| (b4) MISREADING | **2** | A09, A10 |
| (b5) unresolved | **15** | A01, A02, A18, A19, A20, A24-A31, A32, B01 |

**18 of 33 cells reach a respect. 14 are pre-declared X4 and one (A32) X0.**
Against the v2 rule the two new branches move six cells (A15-A17, A21-A23) from
unresolved to a respect, and nothing moves the other way.

**(b7) fires on nothing, and that is recorded rather than repaired.** It exists
because :609 names "a missing distinction" among defect kinds, not because a
cell needed it. Loosening it until it caught a cell would be the fitting §3
already has to concede once.

### The (b5) assignments, each with its reason

| cells | `bearing`, in brief | why no branch fires |
|---|---|---|
| A01, A02 | "If the driver is renegotiation or legitimacy rather than ambiguity, the specification move in c2 treats a symptom, and the account's sequencing … is misplaced." | no discrimination claim ((b1)); a conditional, not a rival asserted to be on the table ((b2)); "misplaced" is weaker than (b3)'s "does work its stated evidence does not carry"; no inconsistency, no missing distinction, no misreading claim. **Declared (b5) rather than loosening (b2) (F37).** |
| A18, A19 | "counters the choice architecture implied by the format-change suggestion" | asserts no discrimination failure, no rival-as-frame, no evidential over-reach in those words, no inconsistency, no missing distinction, no misreading |
| A20 | "counters treating the rival's diagnostic as a complete first move; it may leave the flat without a next step" | an incompleteness claim about a rival's procedure; matches no branch's explicit form |
| A24 | "If this holds, the recommendations need ordering by unilateral feasibility …, with shared institutions treated as proposals contingent on that groundwork rather than as the core fix." | a conditional re-ordering demand; (b3) requires an explicit assertion that the prescription does work its **stated evidence** does not carry |
| A25, A26 | "Unless the one-on-one establishes what is being avoided, the review should be specified as asynchronous or opt-in, or dropped as the load-bearing element." | a conditional repair proposal; no branch's explicit form |
| A27, A28 | "If the review fails or is rejected, zones and written agreements decay on schedule and the account has no fallback; the effective remedy set is smaller and more fragile than u1 presents." | a claim about the remedy's efficacy versus its presentation, not about what the **stated evidence** carries |
| A29 | "… disputes relocate more than settle, and what happens when a written agreement is still not met is a question the task text gives no leverage on and the account leaves untouched." | names an unaddressed **question**, not a distinction the target fails to draw; (b7)'s explicit form is absent |
| A30, A31 | "If a large share of chores can be de-collectivized, the allocation mechanism may be over-engineering …; at minimum the account should say why governance rather than dissolution." | a demand for a reason, not an explicit allegation that a needed distinction is undrawn; (b7) does not fire |
| B01 | "narrows the commitment to a cost rule with an explicit scope, rather than a trigger condition" | alleges no defect at all in the `bearing` field (F47) |
| A32 | *(not reached)* | X0 fires first on the absent target record id |

**Zero-row occurrences.** F001 occurrences **02, 03, 04, 06 and 08** — **five
occurrences (F44)** — contribute **zero** cells; their use tables carry zero
rows. That is a fact about those documents' authored refs, not about their
authors. It is recorded as a cell count of zero and never as a negative finding.

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

## E2 — the equivariance check, its reach, and its one disposition

**Scope.** The C001 ORIGINAL objection block against the RECODING block, unit by
unit over the **fcl arm's 50 units** of `RECODING_TABLE.md` (28 `B.*` body units
+ 22 `K.*` record-field units). The table's other **35 units** (20 `B.*` + 15
`C.*`) are the `mini_prose` arm and bear on no cell here. **Counts re-derived at
this revision: 28 + 22 + 20 + 15 = 85.**

**Record coverage, corrected (F39). Measured:** the 22 `K.*` units cover **eight
records** of `daily/mini_fcl/cycle01/objection` — **`o1`, `o2`, `o3`, `o4`,
`c1`, `c2`, `p1`, `u1`**. *v2 said "records o1, o2, o3"; that is false of the
table.* **Of the eight, only `o1`, `o2` and `o3` carry a referring row in the
golden use table** — `o4` carries none — which is why the reachable set is
unchanged even though the coverage sentence was wrong.

**Reachable cells — five, and only these.**

| # | cell | why reachable |
|---|---|---|
| A01 | golden row 0 | referring record `o1`, covered by `K.o1.*` |
| A02 | golden row 1 | `o1`, same |
| A03 | golden row 2 | `o2`, covered by `K.o2.*` |
| A04 | golden row 3 | `o3`, covered by `K.o3.*` |
| A05 | golden row 4 | `o3`, same |

**Note against over-reading the five.** A01 and A02 are pre-declared **X4** on
the bridge, so E2's reach and the leg's readable cells overlap in **three**
cells only (A03, A04, A05). That is stated here so no reader discovers it as a
result.

**Unreachable, stated so no reader tries.** Golden rows 10, 11, 13 refer from
the `response` node (`k3`, `k7`) and rows 16, 17 from the `carry` node (`n3`);
the recoding table covers neither node. **No F001 cell is reachable by E2 at
all.**

**The single permitted disposition of an E2 failure (F40).** Finding 2 against
the C001 table's own content-preservation argument (**D13**). *v2's alternative
— "or a challenge to FW5:1202's applicability at this grain" — is **withdrawn**:
:1202 hypothesises that **all** carriers, component relations, role bindings,
maps, histories, question contracts and attribution indices are transported
along structure-preserving bijections; the table recodes one document while the
targets `account#c1-c3` are not recoded at all; and :1206 excludes what is not
"the stipulated bijections". No E2 outcome bears on :1202.*

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
| C001 occurrence-01 `deepseek-flash` × `fcl` | **19 of 20 coordinates unusable at the 8192 ceiling: 8 PARTIAL at `finish_reason` "length" with `completion_tokens` exactly 8192, and 11 FAILED with `NO_PUBLIC_CONTENT`.** Read off **`experiments/diagnostics/C001-contrast-triple/occurrence-01/COMPARISON.md`** — table lines 38-57, "Unresolved in this cell" line 59 (**two `COMPARISON.md` files exist under this study; this is the occurrence-01 one**). The "…and no usage" wording is at `material-occurrence-02.json`:1519; the **"no `finish_reason`"** half is at **`occurrence-02/material.json`:1483** (and `occurrence-02/plan.json`:82): "every FAILED carries INCOMPLETE_GENERATION with validation_failure_type NO_PUBLIC_CONTENT, **no finish_reason and no usage at all**" (F46). Because the 11 FAILED rows carry no usage, the ceiling is an **inference** for them and is labelled as one. |
| `ollama-glm-5.3` × `fcl` | the single PARTIAL coordinate, CONTROL rep2 |
| `use-table-full` | 12 nodes whose commitment surface was not read (`nodes_not_read`): 10 `prose_not_parsed` + 2 `unavailable_decode_failure` |
| the eight F001 use tables | `nodes_not_read` = 7, 8, 6, 5, 6, 9, 6, 7 |

FW5:688 — "The inability to evaluate a proposition is not a falsifying
observation of the proposition." No cell above is counted on either side.

---

## Outcome classes and the charge rule

Both are declared in `STAGING-v3.md` §5(b) **before** any cell is read, and are
reproduced in the published `PLAN.md` unchanged. First match wins, and the nine
classes are exhaustive by the argument given there:

**X0 NOT-RECONSTRUCTIBLE / X4 UNRESOLVED / X3 RECONSTRUCTION-FAILED /
X6 UNDECIDABLE-DEFECT / X5 FREE-DECLARATION / X2 CONFLICT-POSITIVE /
X2b CONFLICT-NEGATIVE / X1 AGREE-POSITIVE / X1b AGREE-NEGATIVE.**

**No row of the charge decision table names Account, there is no Account-alone
branch, and its deleted antecedent is false for every cell in this register
anyway** — FCL-1 supplies no \(\delta\) slot, so no cell's \(\mathcal E_c\) is
supplied in full by the record's own fields. The register-level finding 2
against D14 that this entails is declared **before** the reading and cannot be
strengthened by it.
