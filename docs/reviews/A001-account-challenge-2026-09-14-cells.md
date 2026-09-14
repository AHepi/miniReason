# A001 cell list, revision 4 — the pre-registration, with the bridge branch frozen per cell

Frozen with `STAGING-v4.md`. `CELLS-v2.md` and `CELLS-v3.md` are retained
unedited beside it. **Measured** throughout: every row index, record id, target
id and `bearing` string below was re-derived from the pinned JSON at this
revision, not copied from `CELLS-v3.md`.

**Why this file changed (F58, F60).** `CELLS-v3.md` did not change because the
register changed; it changes because **§3's strict match test acquired the rule
it was missing**. v3's match test said a branch fires only where the `bearing`
text "explicitly asserts" that branch's form, and said nothing about a form
stated inside a conditional — while simultaneously disqualifying A01/A02 and A24
*as* conditionals and branching A06-A08 and A09/A10 on forms that sit inside
conditionals. **`STAGING-v4.md` §3 states the rule** (a form stated solely in an
antecedent, or solely in the consequent of a conditional whose antecedent the
text does not assert, is not an explicit assertion), and **five cells move out
of a respect: A06, A07, A08 from (b1); A09, A10 from (b4). Nothing moves the
other way.** A second correction: **A32 is no longer counted inside (b5)** — X0
fires before the bridge is consulted, so A32 is not a (b5) return (F60).

Assessment columns do not appear here; they belong to `WORKSHEET.md` and are
published empty.

**Pins** (all five re-hashed at each review, exact):

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
sub-register A here — exactly as P7 requires. **The register itself is
unchanged from v3: the same 33 cells, the same two sub-registers, the same 12
declared-use rows.** Only branch and class assignments move.

**Branch legend (§3).** (b1) DISCRIMINATION → inferential identification;
(b2) RIVAL-FRAME → inferential identification; (b3) PRESCRIPTION → achievement
of an aim; (b6) INCONSISTENCY → impossibility; (b7) MISSING-DISTINCTION →
inferential identification; (b4) MISREADING → inferential identification,
`bridge-strained`; (b5) → none, cell is **X4 UNRESOLVED** and read no further.

**Match test, with the conditional rule (§3, new at v4).** A branch fires only
where the `bearing` text **explicitly asserts** that branch's form **outright**.
A form stated **solely inside the antecedent of a conditional**, or **solely
inside the consequent of a conditional whose antecedent the same `bearing` text
does not itself assert**, is **not** an explicit assertion. "Unless P, Q" counts
as a conditional.

---

## Sub-register A — 32 cells, referring record typed `objection` with a non-empty `bearing`

*The cell list is the v1 list, unchanged. Three reviews verified it row by row
against the pinned JSON. The `branch` and `class` columns are v4's.*

| # | table | row | referring → target | branch (v4) | \(\kappa\) | pre-declared class | change since v3 |
|---|---|---|---|---|---|---|---|
| A01 | H005 golden | 0 | `objection#o1` → `account#c1` | **(b5)** | — | **X4** | — |
| A02 | H005 golden | 1 | `objection#o1` → `account#c2` | **(b5)** | — | **X4** | — |
| A03 | H005 golden | 2 | `objection#o2` → `account#c2` | (b1) | inferential identification | open (read) | — |
| A04 | H005 golden | 3 | `objection#o3` → `account#c2` | (b3) | achievement of an aim | open (read) | — |
| A05 | H005 golden | 4 | `objection#o3` → `account#c3` | (b3) | achievement of an aim | open (read) | — |
| A06 | H005 golden | 10 | `response#k3` → `rival#r6` | **(b5)** | — | **X4** | **was (b1), open** |
| A07 | H005 golden | 11 | `response#k3` → `rival#r9` | **(b5)** | — | **X4** | **was (b1), open** |
| A08 | H005 golden | 13 | `response#k7` → `rival#r9` | **(b5)** | — | **X4** | **was (b1), open** |
| A09 | H005 golden | 16 | `carry#n3` → `response#k2` | **(b5)** | — | **X4** | **was (b4), open** |
| A10 | H005 golden | 17 | `carry#n3` → `response#k7` | **(b5)** | — | **X4** | **was (b4), open** |
| A11 | F001 occ-01 | 0 | `objection#o1` → `account#c1` | (b2) | inferential identification | open (read) | — |
| A12 | F001 occ-01 | 1 | `objection#o1` → `account#c2` | (b2) | inferential identification | open (read) | — |
| A13 | F001 occ-01 | 2 | `objection#o1` → `account#c3` | (b2) | inferential identification | open (read) | — |
| A14 | F001 occ-01 | 3 | `objection#o1` → `account#c4` | (b2) | inferential identification | open (read) | — |
| A15 | F001 occ-01 | 4 | `objection#o2` → `account#c6` | **(b6)** | impossibility | open (read) | — |
| A16 | F001 occ-01 | 5 | `objection#o2` → `account#c3` | **(b6)** | impossibility | open (read) | — |
| A17 | F001 occ-01 | 6 | `objection#o2` → `account#c4` | **(b6)** | impossibility | open (read) | — |
| A18 | F001 occ-01 | 7 | `objection#o3` → `account#c2` | **(b5)** | — | **X4** | — |
| A19 | F001 occ-01 | 8 | `objection#o3` → `account#c5` | **(b5)** | — | **X4** | — |
| A20 | F001 occ-01 | 19 | `carry#r5` → `response#m5` | **(b5)** | — | **X4** | — |
| A21 | F001 occ-01 | 20 | `carry#r6` → `account#c3` | **(b6)** | impossibility | open (read) | — |
| A22 | F001 occ-01 | 21 | `carry#r6` → `account#c4` | **(b6)** | impossibility | open (read) | — |
| A23 | F001 occ-01 | 22 | `carry#r6` → `account#c6` | **(b6)** | impossibility | open (read) | — |
| A24 | F001 occ-05 | 3 | `objection#o1` → `account#u1` | **(b5)** | — | **X4** | — |
| A25 | F001 occ-05 | 4 | `objection#o2` → `account#u1` | **(b5)** | — | **X4** | — |
| A26 | F001 occ-05 | 5 | `objection#o2` → `account#c4` | **(b5)** | — | **X4** | — |
| A27 | F001 occ-05 | 6 | `objection#o3` → `account#u1` | **(b5)** | — | **X4** | — |
| A28 | F001 occ-05 | 7 | `objection#o3` → `account#c3` | **(b5)** | — | **X4** | — |
| A29 | F001 occ-05 | 8 | `objection#o4` → `account#c2` | **(b5)** | — | **X4** | — |
| A30 | F001 occ-05 | 9 | `objection#o5` → `account#u1` | **(b5)** | — | **X4** | — |
| A31 | F001 occ-05 | 10 | `objection#o5` → `account#c1` | **(b5)** | — | **X4** | — |
| A32 | F001 occ-07 | 1 | `rival#r5` → `account` — **target record id absent** | — *(bridge not consulted)* | — | **X0** | **no longer counted inside (b5) (F60)** |

**A32's resolver note, quoted:** "bare exposed-artifact label with no
'#LocalName'; local resolution was tried first, so it resolves to the owning
artifact (deviation D2)". A32 is pre-declared **X0 NOT-RECONSTRUCTIBLE** on the
missing target record id, not read and then failed; X0's condition fires before
the bridge is consulted. **It is therefore not a (b5) return and is not counted
as one.**

## Sub-register B — 1 cell, bearing-carrying record not typed `objection`

| # | table | row | referring → target | type | branch | pre-declared class |
|---|---|---|---|---|---|---|
| B01 | F001 occ-01 | 12 | `carry#r2` → `response#m2` | `claim` | **(b5)** | **X4** |

`bearing`, verbatim: "narrows the commitment to a cost rule with an explicit
scope, rather than a trigger condition".

**Why B01 is in the register and why it is unreadable.** §3's unit definition is
a non-empty `bearing` field; this row has one, and v1's list was built on the
`type` field instead, so the pre-registration did not match its own definition —
that is why it was added at v2. But **the bridge reads the `bearing` field
alone**, and this `bearing` alleges no defect and matches no branch. v2
justified the cell by its `text` ("The prior m2's condition … was not licensed
by the prior body"), which §3 forbids the bridge to read. **B01 is therefore
retained as a datum about the FCL-1 `type` field — it does not track FW5:609's
criticism constituents — and is pre-declared unreadable.** Extending the bridge
to `text` was considered and declined (§3).

**Total: 33 cells.**

---

## The frozen branch distribution

**Coverage fact about A001's own bridge. Not evidence, on any side, under
`STAGING-v4.md` §5(b) rule 6.**

| branch | cells | which | v3 |
|---|---|---|---|
| (b1) DISCRIMINATION | **1** | A03 | *was 4* |
| (b2) RIVAL-FRAME | **4** | A11, A12, A13, A14 | 4 |
| (b3) PRESCRIPTION | **2** | A04, A05 | 2 |
| (b6) INCONSISTENCY | **6** | A15, A16, A17, A21, A22, A23 | 6 |
| (b7) MISSING-DISTINCTION | **0** | **none** | 0 |
| (b4) MISREADING | **0** | **none** | *was 2* |
| (b5) unresolved | **19** | A01, A02, A06, A07, A08, A09, A10, A18, A19, A20, A24-A31, B01 | *was 15, wrongly including A32* |
| *(bridge not consulted)* | **1** | A32 — X0 fires first | *counted inside (b5)* |

**13 of 33 cells reach a respect and are read. 19 are pre-declared X4 and one
(A32) X0.** *v3 reported 18 read, 14 X4, 1 X0.*

**Two branches fire on nothing, and that is recorded rather than repaired.**
(b7) exists because :609 names "a missing distinction" among defect kinds, and
never fired. **(b4) now fires on nothing either** — golden 16 and 17, the cells
it was written from, are conditionals whose antecedent their texts do not
assert. Loosening either branch until it caught a cell would be the fitting §3
already has to concede.

**The measured fact that charges the bridge hardest, recorded here as well as in
§3.** Every branch that fires at all fires **only** on cells whose `bearing`
text that branch's own condition paraphrases: (b1) on A03 alone, whose "lower
discriminating power" its second limb restates; (b3) on A04/A05 alone, restated
verbatim; (b2) on A11-A14 alone, on which it was tuned; (b6) on the six cells
whose `bearing` is the text its own stated example quotes. **A001 records this
and does not repair it.**

### The (b5) assignments, each with its reason

| cells | `bearing`, verbatim or in brief | why no branch fires |
|---|---|---|
| A01, A02 | "**If** the driver is renegotiation or legitimacy rather than ambiguity, the specification move in c2 treats a symptom, and the account's sequencing (chores first, relationship later) is misplaced." | a conditional whose antecedent the text does not assert; and "misplaced" is in any case weaker than (b3)'s "does work its stated evidence does not carry" |
| **A06, A07** | "**If** the opening question itself triggers withdrawal, the rival's own distinguishing observation is contaminated: you cannot tell pullback-from-the-idea from pullback-from-a-heavy-question." | **new at v4.** (b1)'s form ("cannot tell X from Y") sits in the **consequent** of a conditional whose antecedent the text does not assert |
| **A08** | "**If** pullback-from-form cannot distinguish those, the test is weaker than k2 suggests, and the honest state is that neither reading is being confirmed." | **new at v4.** (b1)'s form ("cannot distinguish") sits in the **antecedent** |
| **A09, A10** | "**If** a reader takes k2 at face value and does not read k7 as limiting it, the probe will be over-read as a test of the unit-versus-privacy axis." | **new at v4.** (b4)'s form ("a reader will misread") sits in the consequent of a conditional whose antecedent the text does not assert. **This empties (b4)** |
| A18, A19 | "counters the choice architecture implied by the format-change suggestion" | asserted outright, but matches no branch's stated form: no discrimination failure, no rival-as-frame, no evidential over-reach in those words, no inconsistency, no missing distinction, no misreading |
| A20 | "counters treating the rival's diagnostic as a complete first move; it may leave the flat without a next step" | asserted outright; an incompleteness claim about a rival's procedure, not (b2)'s "as the frame"; matches no branch |
| A24 | "**If** this holds, the recommendations need ordering by unilateral feasibility …, with shared institutions treated as proposals contingent on that groundwork rather than as the core fix." | a conditional re-ordering demand; and (b3) requires an explicit assertion that the prescription does work its **stated evidence** does not carry |
| A25, A26 | "**Unless** the one-on-one establishes what is being avoided, the review should be specified as asynchronous or opt-in, or dropped as the load-bearing element." | a conditional repair proposal; no branch's explicit form |
| A27, A28 | "**If** the review fails or is rejected, zones and written agreements decay on schedule and the account has no fallback; the effective remedy set is smaller and more fragile than u1 presents." | a conditional; and the asserted-sounding limb is a claim about the remedy's efficacy versus its presentation, not about what the **stated evidence** carries |
| A29 | "Writing agreements down still helps under this reading …, but expectations shift: disputes relocate more than settle, and what happens when a written agreement is still not met is a question the task text gives no leverage on and the account leaves untouched." | asserted outright, but it names an unaddressed **question**, not a distinction the target fails to draw; (b7)'s explicit form is absent |
| A30, A31 | "**If** a large share of chores can be de-collectivized, the allocation mechanism may be over-engineering …; at minimum the account should say why governance rather than dissolution." | a conditional, and the outright limb is a demand for a reason, not an explicit allegation that a needed distinction is undrawn |
| B01 | "narrows the commitment to a cost rule with an explicit scope, rather than a trigger condition" | alleges no defect at all in the `bearing` field |

**Zero-row occurrences.** F001 occurrences **02, 03, 04, 06 and 08** — **five
occurrences** — contribute **zero** cells; their use tables carry zero rows.
That is a fact about those documents' authored refs, not about their authors. It
is recorded as a cell count of zero and never as a negative finding.

---

## The 13 read cells, and the reachability witnesses

**The cells a reader is assigned:** A03, A04, A05 (H005 golden rows 2, 3, 4);
A11, A12, A13, A14, A15, A16, A17, A21, A22, A23 (F001 occurrence-01 rows 0-6,
20-22).

**Reachability witnesses (`STAGING-v4.md` §5(b)). These are NOT predictions,
NOT assignments, and no cell's class is decided here.** They name a reader state
that would place a named cell in a class, so that the class is shown to be
occupiable rather than merely defined.

| class | witness cell | the reader state |
|---|---|---|
| X0 | A32 | **assigned**, on the absent `target_record_id` |
| X4 | A01, A02, A06-A10, A18-A20, A24-A31, B01 | **assigned** at the gate, 19 cells |
| X3 | **A15** | both readers report no admissible target organization \(D\) for \(p_\delta\): the alleged inconsistency spans `c6`, `c3` and `c4` — three records — while the frozen grain is the single record keyed by id |
| X6 | **A11** | both readers record **J2 undetermined**: whether `account#c1` *treats* c1 and c2 as the frame is not settled by the passage either way |
| X5 | **A04** | both readers record `free` at **D6**, each exhibiting a declared abstraction under which (E) comes out the other way |
| X2 | **A03** | both agree (E) **holds**, and both judge the discrimination failure **does not obtain**, reading `account#c2`'s own `consequence` field as discriminating |
| X2b | **A05** | both judge the prescriptive over-reach **obtains** of `account#c3` while (E) **fails** at :176 s3 |
| X1 | **A16** | both agree (E) **holds** and the alleged inconsistency **obtains** |
| X1b | **A12** | both agree (E) **fails** and the framing allegation **does not obtain** |

**Every one of the seven read-cell classes has a witness over these 13 cells**,
so no class of the table is reachable only in principle. A class the reading
step leaves empty is reported as empty over 13 cells, never as evidence.

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
`C.*`) are the `mini_prose` arm and bear on no cell here. **28 + 22 + 20 + 15 =
85.**

**Record coverage. Measured:** the 22 `K.*` units cover **eight records** of
`daily/mini_fcl/cycle01/objection` — **`o1`, `o2`, `o3`, `o4`, `c1`, `c2`,
`p1`, `u1`**. **Of the eight, only `o1`, `o2` and `o3` carry a referring row in
the golden use table** — `o4` carries none.

**Reachable cells — five, and only these.**

| # | cell | why reachable |
|---|---|---|
| A01 | golden row 0 | referring record `o1`, covered by `K.o1.*` |
| A02 | golden row 1 | `o1`, same |
| A03 | golden row 2 | `o2`, covered by `K.o2.*` |
| A04 | golden row 3 | `o3`, covered by `K.o3.*` |
| A05 | golden row 4 | `o3`, same |

**Note against over-reading the five.** A01 and A02 are gated **X4** on the
bridge, so E2's reach and the leg's read cells overlap in **three** cells only —
A03, A04, A05. **The conditional rule of v4 touches none of the five**, so this
overlap is unchanged from v3. It is stated here so no reader discovers it as a
result.

**Unreachable, stated so no reader tries.** Golden rows 10, 11, 13 refer from
the `response` node (`k3`, `k7`) and rows 16, 17 from the `carry` node (`n3`);
the recoding table covers neither node. **No F001 cell is reachable by E2 at
all.**

**The single permitted disposition of an E2 failure.** Finding 2 against the
C001 table's own content-preservation argument (**D13**). *v2's alternative —
"or a challenge to FW5:1202's applicability at this grain" — is **withdrawn**:
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
| C001 occurrence-01 `deepseek-flash` × `fcl` | **19 of 20 coordinates unusable at the 8192 ceiling: 8 PARTIAL at `finish_reason` "length" with `completion_tokens` exactly 8192, and 11 FAILED with `NO_PUBLIC_CONTENT`.** Read off **`experiments/diagnostics/C001-contrast-triple/occurrence-01/COMPARISON.md`** — table lines 38-57, "Unresolved in this cell" line 59 (**two `COMPARISON.md` files exist under this study; this is the occurrence-01 one**). The "…and no usage" wording is at `material-occurrence-02.json`:1519; the **"no `finish_reason`"** half is at **`occurrence-02/material.json`:1483** (and `occurrence-02/plan.json`:82): "every FAILED carries INCOMPLETE_GENERATION with validation_failure_type NO_PUBLIC_CONTENT, **no finish_reason and no usage at all**". Because the 11 FAILED rows carry no usage, the ceiling is an **inference** for them and is labelled as one. |
| `ollama-glm-5.3` × `fcl` | the single PARTIAL coordinate, CONTROL rep2 |
| `use-table-full` | 12 nodes whose commitment surface was not read (`nodes_not_read`): 10 `prose_not_parsed` + 2 `unavailable_decode_failure` |
| the eight F001 use tables | `nodes_not_read` = 7, 8, 6, 5, 6, 9, 6, 7 |

FW5:688 — "The inability to evaluate a proposition is not a falsifying
observation of the proposition." No cell above is counted on either side.

---

## Outcome classes and the charge rule

Both are declared in `STAGING-v4.md` §5(b) **before** any cell is read, and are
reproduced in the published `PLAN.md` unchanged. First match wins over read
cells, X0 and the gated X4 are assigned before reading, and **X4 is the
otherwise-row, so exhaustiveness is definitional rather than argued**:

**X0 NOT-RECONSTRUCTIBLE / X3 RECONSTRUCTION-FAILED / X6 UNDECIDABLE-DEFECT /
X5 FREE-DECLARATION / X2 CONFLICT-POSITIVE / X2b CONFLICT-NEGATIVE /
X1 AGREE-POSITIVE / X1b AGREE-NEGATIVE / X4 UNRESOLVED (residue).**

Three procedural rules belong to the register and are repeated here because a
reader works from this file: **the :620 check** (FW5:620 — "The alleged defect
must concern the stated target and respect"), performed on every read cell
before J1 and J2, with a both-readers mismatch landing the cell in X4 with a
charge to **D21**; **the free-declaration test**, which fires X5 only where both
readers exhibit an alternative declaration at the same §2 row that flips a
judgement; and the **two-reader rule** — where they disagree the cell is
unresolved and the disagreement is recorded, never averaged (FW5:634; C001 PLAN
§8a:743-745).

**No row of the charge decision table names Account, there is no Account-alone
branch, and its deleted antecedent is false for every cell in this register
anyway** — FCL-1 supplies no \(\delta\) slot, so no cell's \(\mathcal E_c\) is
supplied in full by the record's own fields. The register-level finding 2
against D14 that this entails, and the register-level finding-1 fact that
\(\ell\), \(\beta\), \(\mathcal C\) and \(\kappa\) had to be declared at all,
are both declared **before** the reading and cannot be strengthened by it.
