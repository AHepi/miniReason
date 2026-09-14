# A001 v4 — narrow verification of the staging (not a fourth adversarial review)

Scope fixed by the owner's ruling that review rounds stop after v4: this file decides only
(a) whether the three round-3 blockers F51-F53 are closed, and (b) whether v4 is internally
consistent enough to publish as an **in-progress** challenge record with residual should-fixes
listed as open items. It is not a new round of findings and it does not re-open settled matters.

**Read first, as instructed:** `SESSION_RULINGS.md` rulings 7 (metric-creep lens), 9 (governing
purpose; A001 staged from the fw5/ critiques with claim, dependencies, grain, boundary, contrasts
and relinquishment fixed before evidence) and 16 (routing); then `REVIEW-3.md` F51-F53 and the ten
should-fixes F54-F63; then `CHANGES-v4.md`; then `STAGING-v4.md` (1,540 lines) and `CELLS-v4.md`
(334 lines) in full.

**Read-only.** Nothing in `/home/user/miniReason` was written, staged or committed.
`git status --porcelain` is empty at `f191f48116a286c2ddcdc54e4663ff307ea9f36b`. No API key was
read or printed.

**Edition hash verified before any line was relied on.**
`sha256sum docs/sources/FW5-explanatory-construction.md` =
`8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a`, `wc -l` = **1502**, exactly as
`STAGING-v4.md`:14-16 declares. **All five register pins re-hashed exact** (both `use_table.json`,
both `comparison.json`, `RECODING_TABLE.md`).

---

## 1. F51 — the A-S disposal, (P-Ans), D22, "for every λ", and the ceiling

### VERDICT: **CLOSED**

**(a) The disposal is conditional on a named premise stated as A001's, not FW5's.** `STAGING-v4.md`
§5(a)(i):606-611 renders the premise as its own block:

> **(P-Ans) — A001's premise, not FW5's text.** A candidate's answer profile is the query operator
> applied to the **candidate's own organization**: \(\operatorname{Ans}_E(a',b')=\mathcal Q(E,a',b')\).

and :612-621 gives the Measured warrant, **which I re-derived at the edition rather than adopting**:
`grep -n 'Ans}_E' docs/sources/FW5-explanatory-construction.md` returns **exactly two lines, :162 and
:202**, and nothing else in 1,502 lines. :162 reads "An explanatory candidate for \(p\) **supplies**
an organization \(E\), an answer profile \(\operatorname{Ans}_E\) …"; :202 is the left side of (A)'s
display. (Q) at :128-130 is `\operatorname{Ans}_p(a,b)` / `=` / `\mathcal Q(D,a,b).` — over the
target only. :125 reads "a specified set-theoretic operation on **the relevant organization**"
without saying which organization is relevant for a candidate. :210 s1 reads, verbatim, "The answer
follows by evaluating the anchored organization under its declared independent boundary
conditions." **No line states \(\operatorname{Ans}_E=\mathcal Q(E,\cdot,\cdot)\).** v4's claim that
(P-Ans) is A001's and not the edition's is therefore correct at the bytes.

The disposal table at :663-666 carries the conditionality into the outcome rather than the prose
only: horn 2 **under (P-Ans)** → "(r1): the case fails"; horn 2 **without (P-Ans)** → "(r2):
finding 1", with the missing condition named exactly. Horn 1 (:566) is explicitly marked as holding
"**under either reading of D22**", so it does not lean on (P-Ans) either. I checked every occurrence
of `Ans_E` and `P-Ans` in the file (22 hits): **no sentence uses (P-Ans) unlabelled.**

**(b) The alternative reading is present as an undefined D-row derived from the text.** §2 carries
**D22** (:224) — "\(\operatorname{Ans}_E\): how a candidate's answer profile is arrived at | :162;
(Q) :128-130; :125; :210 s1 | **undefined**" — with the two-occurrence Measured fact, the (Q)/target
scope, :125's "the relevant organization", and the note that "**':210 s1's ''the anchored
organization'' is not a defined term of the edition**"; the :197 route is recorded in the same row
as a second locus. §5(a)'s proviso (:522-527) states the derivation direction explicitly: "**D22 is
added to §2 from :162, :125, (Q) :128-130 and :210 s1 directly, not from how Case A-S goes**; that a
case then turns on it is a consequence, not the warrant." That satisfies §5(a)'s own bar against
back-deriving a dependency row from a case outcome.

**(c) "for every λ" is gone as an unconditional claim — with one scoped survival, recorded here so
the record is exact.** Grepped across the file (the phrase wraps a line, so both halves were
searched):
* **§0** — no occurrence of any kind.
* **§6** — the only occurrence is the withdrawal itself (:1247): "**New at v4: A001 does not claim
  that (A) fails under every \(\lambda\) for Case A-S.** That sentence is **withdrawn** as an
  unconditional claim."
* **Receipt paragraph (§7, :1328-1466)** — no occurrence of `\lambda` at all.
* **§5(a)(i)** — two occurrences. :675 is the withdrawal note ("It costs v3's sentence that (A)
  fails 'for every \(\lambda\)' as an unconditional claim: that sentence is **withdrawn** …").
  :623-624 retains the phrase *inside* the conditional bullet — "**Under (P-Ans): (A) Question
  fidelity fails, at :208, under every \(\lambda\)**" — and that bullet closes (:630-631) "**This
  whole bullet is an Interpretation conditional on (P-Ans).**"

So the phrase is deleted everywhere the review named it **as an unconditional claim**, which is what
`CHANGES-v4.md` claims and what F51's fix required; it survives once, syntactically governed by
"Under (P-Ans)" and explicitly labelled an Interpretation. v4 took a hybrid of F51's routes (i) and
(ii) rather than route (ii) alone. **Recorded, not charged.**

**(d) The ceiling argument holds as stated and does not smuggle a claim.** §5(a)(i):668-672: "(r3)
requires that **no candidate gap-filling condition** exclude the case. **(P-Ans) is exactly such a
condition, it is available, and under it the case fails at :208.** So (r3) is not met on either
reading". Two things make this clean:
1. **(r3) is not new.** Its wording is **byte-identical in `STAGING-v2.md`:305-307, `STAGING-v3.md`
   :448-450 and `STAGING-v4.md`:511-513**. It was not written at v4 to rescue the ceiling from F51.
2. The inference is a direct application, not an extension: (r3) is a conjunction, one conjunct is
   falsified by an exhibited condition, so (r3) is unmet under both readings and §6's "A001 offers
   no counterexample to sufficiency" stands without being re-argued.

**One property of (r3) worth the record, which is not a defect:** because (r3) fails as soon as
*any* admissible gap-filling condition can be named that excludes the case, counterexample status is
very hard to reach under A001's own rule, and for A-S the "no counterexample" result is closer to
analytic than evidential. That direction lowers the ceiling rather than raising it, and it is what
ruling 9 asks of a study that must not carry "possible counterexamples" forward — so it is listed as
an open item for a later reviewer, not as a finding against v4.

---

## 2. F52 — nine classes, the gate, X4 as residue, and the seven witnesses

### VERDICT: **CLOSED WITH RESIDUE**

**The blocker itself is closed.** v3's defect was that X4 sat at order 2 and fired on "either reader
records a judgement as undetermined", so X6 (order 4, "both readers agree … does not settle") could
never fire. In v4 (§5(b):986-1008) the two pre-reading conditions are a **gate** ((b5) or E3 → X4
unread; record-level absence → X0), the reading-level X4 conditions are **row 8, "otherwise"**, and
**every "both readers" class is stated as "both", never "either"** — X6 (order 2) now reads "**both**
record **J2** as *undetermined*", and a single reader recording undetermined falls to row 8. X6 is
therefore no longer pre-empted, and exhaustiveness is definitional rather than argued. **The class
set is still nine** — X0, X3, X6, X5, X2, X2b, X1, X1b, X4.

**Every class has a witness, and I re-derived all seven read-cell witnesses from `CELLS-v4.md` and
the pinned JSON register** (`experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/
use-table-golden/use_table.json` and `experiments/analyses/F001-fork5-multifamily-2026-09-14/
occurrence-0{1,5,7}/use-table/use_table.json`, all pins re-hashed exact), reading each cell's
`bearing` and target record out of `referring_record_verbatim` / `target_record_verbatim`:

| class | cell | re-derived from the bytes | lands in the claimed class? |
|---|---|---|---|
| X0 | A32 = F001 occ-07 row 1 | `rival#r5` → `account`, **`target_record_id` is genuinely `None`** | **yes**, assigned at the gate; bridge not consulted |
| X4 | 19 cells | every one returns (b5) under §3's rule (checked cell by cell below) | **yes**, assigned at the gate |
| X3 | A15 = F001 occ-01 row 4 | `objection#o2` → `account#c6`; `bearing` = "alleges an internal inconsistency between raising c6 and leaving c3 and c4 unchanged" — the defect spans **three** records against a **single-record** frozen grain | **yes** at order 1 — but see residue (i) |
| X6 | A11 = F001 occ-01 row 0 | `objection#o1` → `account#c1`; `bearing` = "counters treating c1 and c2 as the frame rather than as one hypothesis among at least two"; `account#c1`'s `text` asserts the ambiguity claim without saying it is the frame | **yes** at order 2; E_c is exhibited so X3 cannot pre-empt |
| X5 | A04 = golden row 3 | `objection#o3` → `account#c2`; `bearing` = "The ordering of the account's recommendations is doing prescriptive work that the stated evidence does not carry" — D6 can retain or project away that ordering | **yes** at order 3 |
| X2 | A03 = golden row 2 | `objection#o2` → `account#c2`; `bearing` = "Weakens the claim that falling recurrence would confirm c1 and rising recurrence would refute it; the test has lower discriminating power than the account implies". **`account#c2` does carry a `consequence` field**, verbatim: "If two or three concrete items stop recurring after being specified more tightly, this supports c1; if they keep recurring, c1 is weakened …" | **yes** at order 4 — the witness's factual anchor is real |
| X2b | A05 = golden row 4 | `objection#o3` → `account#c3`; `account#c3`'s `grounds` say "this is a conjecture, not an established fact", so "the prescriptive over-reach obtains" is grounded | **yes** at order 5 — but see residue (ii) |
| X1 | A16 = F001 occ-01 row 5 | `objection#o2` → `account#c3`; **identical `bearing` to A15** | **yes** at order 6 — but see residue (i) |
| X1b | A12 = F001 occ-01 row 1 | `objection#o1` → `account#c2`; identical `bearing` to A11 | **yes** at order 7 |

**Can two classes both fire on one cell?** No cell can be *assigned* two classes: rows 1-7 are
ordered, row 8 is "otherwise", and the gate is pre-reading. The conditions are mutually exclusive
for X3/X6 (E_c exhibited or not), for X6/X5 (J2 undetermined vs both judgements determinate), and
among X2/X2b/X1/X1b (the four Boolean combinations of agreed J1 × J2). **Three seams exist and are
resolved only by the ordering or by prose outside the table** — they are residue, not defects:

* **(iii) X5 literally overlaps rows 4-7.** X5's condition (both `free` at the same §2 row) and
  X2/X2b/X1/X1b's conditions (agreed J1/J2) can both hold on one cell; the Boolean rows do not carry
  "and neither reader records `free`". The ordering decides it, and §5(b):983-985 states the intent
  in prose ("Neither recording `free` sends the cell on to the four Boolean rows"), so the outcome is
  determinate — but the table alone is not self-contained.
* **(iv) The :620 check is an exit that is not a row of the ordered table.** Procedure step 3
  (§5(b):930-937) sends a both-readers mismatch to X4 with a charge to D21 **before** J1 and J2 are
  recorded, i.e. before rows 1-7 are consulted. The charge table's X4 row carries the exception; the
  class table does not. `CHANGES-v4.md` §6 item 5 raises this against itself.
* **(v) The gate's internal order is stated two ways.** The class table lists the **X0** gate row
  before the **X4** gate row, and §3 / `CELLS-v4.md` say "X0's condition fires before the bridge is
  consulted"; procedure step 1 (§5(b):916-922) lists the (b5)/E3 gate **first** and X0 second. It
  makes no difference to A32 (its bridge is never consulted), but a cell that was both would be
  decided differently by the two passages.

**The residue that matters most, and it is sharper than the doubt v4 raises against itself:**

* **(i) The X3 witness at A15 and the X1 witness at A16 rest on incompatible readings of the same
  bytes.** Re-derived from the JSON: **six cells share one identical `bearing` string** — A15, A16,
  A17 (F001 occ-01 rows 4, 5, 6) and A21, A22, A23 (rows 20, 21, 22) all read "alleges an internal
  inconsistency between raising c6 and leaving c3 and c4 unchanged". The X3 witness argues that no
  admissible \(D\) exists **because the alleged inconsistency spans c6, c3 and c4 — three records —
  against the single-record grain**. That argument is a property of the *defect*, not of the target
  record, so it applies verbatim to A16. X3 is order 1 and X1 is order 6, so **if the X3 witness is
  sound it pre-empts the X1 witness on A16**; and if a reader can write out \(D\) on A16, the X3
  argument fails on A15 too, leaving X3 with no witness. `CHANGES-v4.md` §6 item 3 already names A15
  as "the weakest" witness; what it does not say is that A15 and A16 cannot both be occupiable under
  one reader's reasoning. X1 is not thereby unreachable over the 13 cells — a (b2) cell such as A13
  or A14 has no three-record problem — but the witness **as named** is in tension.
* **(ii) The four Boolean witnesses do not discharge the precondition they need.** X2, X2b, X1 and
  X1b sit below X5, so a cell reaches them only if the free-declaration test does **not** fire. None
  of the four witness states says anything about `free`/`not-free`. This bites hardest at A04/A05:
  they share one referring record (`objection#o3`) and **one identical `bearing` string**, and A04's
  X5 witness exhibits a flipping D6 alternative ("one declared abstraction retains the ordering of
  the account's recommendations and one projects it away") while A05's X2b witness asserts (E) fails
  "at the declared abstraction" — the same D6 locus. A reader who exhibits A04's alternative at A05
  sends A05 to X5, not X2b.

---

## 3. F53 — "free declaration" as an operational test

### VERDICT: **CLOSED WITH RESIDUE**

**It is now operational, and it is not the trivial test.** §5(b):939-985 defines, per **per-cell**
declaration \(d\), two recordable values with required evidence:

> * **`free`** — the reader **writes out** an alternative \(d'\), admissible at the same §2 row (that
>   is: the reader can name no line of the reading edition excluding it), under which **that reader's
>   own J1 or J2 comes out differently**. The row records the §2 row, \(d\), \(d'\), and which
>   judgement flips.
> * **`not-free`** — … **either** a quoted line of the reading edition that excludes every such
>   \(d'\), **or** the sentence "searched, none exhibited", with what was tried. …
>
> **X5 fires if and only if both readers record `free` at the same §2 row and each writes out its own
> \(d'\).** Exactly one reader recording `free` is a **disagreement** and the cell is X4.

This meets every element the task asked for: **a written-out admissible alternative**, **that flips
the reader's own J1 or J2**, **by both readers**, **at the same §2 row**. Two further pieces close
F53's second horn: the declared constants (\(\ell\), \(\beta\), the contrast *requirement*, and the
frozen-branch \(\kappa\)) are named before any reading and may not be varied (§5(b):941-947), and the
fact that they had to be declared at all is recorded **once at the register level** and "**not
re-earned per cell**" (§5(b):886-894), with a matching §6 ceiling line. So the "only because a
declaration was made" counterfactual that made v3's X5 trivially true of every cell is gone.

**Can a cell now reach X1/X1b/X2/X2b? Yes — one worked example, re-derived from the bytes.**
**A03** (H005 golden row 2, `objection#o2` → `account#c2`, branch (b1), read). Its `bearing` is
"Weakens the claim that falling recurrence would confirm c1 and rising recurrence would refute it;
the test has lower discriminating power than the account implies." Its target `account#c2` carries a
`consequence` field whose text is a confirm/refute rule: "If two or three concrete items stop
recurring after being specified more tightly, this supports c1; if they keep recurring, c1 is
weakened and the problem is more likely relational or about the living arrangement." A reader who
exhibits \(\mathcal E_c\), passes the :620 check (κ = inferential identification from (b1); δ = the
test's discriminating power — the same respect), records **J1 = (E) holds** and **J2 = the defect
does not obtain** (reading the `consequence` field as discriminating the two readings the `bearing`
says it cannot), and then records **`not-free`** at each per-cell row, lands at **order 4 = X2
CONFLICT-POSITIVE**: X3 does not fire (E_c is exhibited), X6 does not fire (J2 is determinate), X5
does not fire (no `free`). The charge is "D21 first, then D14", the residue is recorded as a conflict
among (K1), (E) and (O), and **no row of the charge table names Account**. The class is genuinely
occupiable.

**Residue.** The `not-free` branch admits "searched, none exhibited", which is a weak record that
could silently become the default — `CHANGES-v4.md` §6 item 4 names this as the mirror of the defect
F53 caught, and `STAGING-v4.md` does not state that the worksheet's columns force a reader to say
which of the two `not-free` evidences was given (the §7 layout lists "the per-declaration free/not-
free records" without that distinction). Conversely, the D6 alternative A04's own X5 witness exhibits
is available at other cells, so the opposite failure — X5 firing nearly everywhere at a higher
evidentiary bar — is not excluded by argument either. **The test is sound; its calibration is
untested and can only be tested by the reading step.**

---

## 4. `CELLS-v4.md` consistency and the F58 moves

### VERDICT: **CLOSED**

The register was **re-derived from the pinned JSON, not spot-checked**: every row of the golden table
and of all eight F001 occurrence tables was parsed, `bearing` read out of `referring_record_verbatim`,
and the rows with a non-empty `bearing` enumerated.

* **33 cells, exactly.** Golden rows 0, 1, 2, 3, 4, 10, 11, 13, 16, 17 (10); F001 occ-01 rows 0-8,
  12, 19-22 (14); occ-05 rows 3-10 (8); occ-07 row 1 (1). **Total 33.** Every referring→target pair,
  node prefix and record type in `CELLS-v4.md` matches the JSON row for row — including A20
  (`carry#r5`→`response#m5`), A29 (`objection#o4`→`account#c2`), B01 (F001 occ-01 row 12,
  `carry#r2`→`response#m2`, **`type: "claim"`**) and A32 (`rival#r5`→`account`, `target_record_id`
  genuinely `None`).
* **Five zero-row occurrences confirmed:** F001 occurrences 02, 03, 04, 06 and 08 all have `rows` = 0.
* **The F58 moves are right at the bytes.** The rule §3 declares — "A form stated **solely inside the
  antecedent of a conditional**, or **solely inside the consequent of a conditional whose antecedent
  the same `bearing` text does not itself assert**, is **not** an explicit assertion" — applied to the
  five moved cells:
  * **A06, A07** (golden 10, 11): "**If** the opening question itself triggers withdrawal, … you
    cannot tell pullback-from-the-idea from pullback-from-a-heavy-question." (b1)'s form is in the
    **consequent** of an unasserted conditional → (b5). Correct.
  * **A08** (golden 13): "**If** pullback-from-form cannot distinguish those, the test is weaker than
    k2 suggests …" (b1)'s form is in the **antecedent** → (b5). Correct. *(The consequent limb "the
    test is weaker than k2 suggests" is a second (b1)-second-limb candidate that the row's stated
    reason does not mention; the rule disposes of it anyway, since the antecedent is unasserted.)*
  * **A09, A10** (golden 16, 17): "**If** a reader takes k2 at face value …, the probe will be
    over-read …" (b4)'s form is in the **consequent** of an unasserted conditional → (b5), **which
    empties (b4)**. Correct.
  * **Nothing moves the other way**, as claimed: the (b1)/(b2)/(b3)/(b6) cells that remain all assert
    outright (A03 "the test has lower discriminating power than the account implies"; A04/A05 "is
    doing prescriptive work that the stated evidence does not carry"; A11-A14 "counters treating c1
    and c2 as the frame …"; the six (b6) cells "alleges an internal inconsistency between …").
* **A32 is listed separately** as *(bridge not consulted)*, 1 cell, with its resolver note quoted;
  it is no longer inside (b5).
* **Every number agrees, in all six places it is stated.** Branch distribution (`CELLS-v4.md` and
  §3): (b1) 1, (b2) 4, (b3) 2, (b6) 6, (b7) 0, (b4) 0, (b5) **19**, bridge-not-consulted **1**,
  **total 33**. Read/gated split: **13 read, 19 X4, 1 X0** — stated identically at `STAGING-v4.md`
  :367, :920, :1021, :1436, :1506-1507 and `CELLS-v4.md`:144, :186, :200. The 19 gated cells
  enumerate to exactly 19 (A01, A02, A06-A10, A18-A20, A24-A31, B01) and the 13 read cells to
  exactly 13 (A03-A05, A11-A17 minus none, A21-A23). **No stale v3 figure (18 read, 15 or 14 in
  (b5)) survives anywhere except in the explicit "*was*" columns.**
* **Supporting counts re-derived independently and exact:** `RECODING_TABLE.md` = **85** units, fcl
  arm **50** (28 `B.*` + 22 `K.*`), prose arm **35** (20 `B.*` + 15 `C.*`); the 22 `K.*` units cover
  exactly the eight records `o1, o2, o3, o4, c1, c2, p1, u1`. E3: `use-table-full` `nodes_not_read`
  = **12** (10 `prose_not_parsed` + 2 `unavailable_decode_failure`); the eight F001 tables =
  **7, 8, 6, 5, 6, 9, 6, 7**; C001 occurrence-01 `deepseek-flash`/`fcl` = **11 FAILED + 8 PARTIAL +
  1 COMPLETE** over `COMPARISON.md` lines 38-57, heading at :34, "Unresolved in this cell" at :59.
  The eight-locus `bearing` survey is exact: case-insensitively the term occurs at **:607, :614,
  :622, :773, :896, :900, :1182** plus the compounds at :800, :912, :1005, :1320 — nothing else in
  1,502 lines — and :893 does carry the display while :896 carries the prose (F64's fix). F65's
  pointer fixes check out at the line (:742 content, :743 `\tag{N}`, :746 gloss; :638, :642, :650
  `\tag{K2}`; :859; :1370 heading).

**One inconsistency found, and it is a should-fix rather than a blocker.** The (b6) branch condition
**changed between v3 and v4 and the change is not recorded anywhere**. Diffed row by row, exactly one
of the seven branch conditions differs:

* v3 (:292): "explicitly alleges that **two or more of the target's own commitments cannot jointly
  hold** (e.g. \"alleges an internal inconsistency between …\")"
* v4 (:343): "explicitly alleges that **two or more of the target's own commitments cannot jointly
  hold**" — **the parenthetical example is gone.**

Meanwhile §3's fitting disclosure (:270-273) still says "**(b6)** is written from :609's own defect
list, but **its stated example** — \"(e.g. 'alleges an internal inconsistency between …')\" — **is
the `bearing` text of F001 occurrence-01 rows 4, 5, 6, 20, 21 and 22 verbatim**", and `CELLS-v4.md`
repeats it ("(b6) on the six cells whose `bearing` is the text its own stated example quotes"). So
v4's strongest self-charge against D21 cites a clause of its own frozen rule that v4 no longer
states. **No cell assignment changes** — the six (b6) cells still satisfy the general condition — but
(a) the bridge rule is declared frozen and pre-registered, and this is an unrecorded edit to it, and
(b) §8(7) names "any sentence that withdraws a disclosure about A001's own bridge" as a regression of
the same kind as re-inflation. Either the example should be restored to the (b6) row, or the
disclosure should be rewritten to charge (b6) on the general condition.

---

## 5. The receipt's ledger figures, re-counted at HEAD

### VERDICT: **CLOSED**

**Commit stated and verified: `f191f48116a286c2ddcdc54e4663ff307ea9f36b`, tree
`0d040f47f9d3282b5f46fcab3a42afe6cccd47fa`** — both exactly as §7 declares, and `git status
--porcelain docs/DECISION_LEDGER.md` is empty, so HEAD bytes are the working-tree bytes (blob sha256
`f6e71978…fb94b` both ways). File: **1,495 lines / 728,439 bytes** — as staged.

Every figure re-derived from the bytes, each under the definition §7 states beside it:

| figure | definition as stated in §7 | v4 | re-counted | ok |
|---|---|---|---|---|
| `REC-20260914` lines | lines **containing** the string | 109 | **109** | ✓ |
| receipt openings | lines **beginning** with the string | 108 | **108** | ✓ |
| identifiers | distinct `REC-20260914-<letters>` | 26, `-A`…`-Z` | **26, exactly `-A`…`-Z`** | ✓ |
| closing lines | lines containing `Prior verified commit/tree:` | 25 | **25** | ✓ |
| total lines | `wc -l` | 1,495 | **1,495** | ✓ |
| bytes | file size | 728,439 | **728,439** | ✓ |
| CRLF lines | occurrences of `\r\n` in the bytes | 37 | **37** (and 37 lines contain `\r`) | ✓ |
| house style | lines containing each string | `Choice:` 96 / `Why:` 86 / `Reason:` 9 / `Contribution:` 90 / `Contribution to the end goal:` 0 / `Letter:` 5 | **96 / 86 / 9 / 90 / 0 / 5** | ✓ |
| whole-file rules | line-start `REC-` / blank-line paragraphs | 381 / 364 | **381 / 364** | ✓ |
| cross-check | `VERIFIED <40hex> TREE <40hex>` | 77 | **77** | ✓ |

**The 109/108 difference is exactly where v4 says it is.** Line **1378** contains "both the values
REC-20260914-Q and REC-20260914-R …" inside a paragraph that does not open a receipt, and the last
receipt-opening line at or before it is **1374**, `REC-20260914-S`. **`-Z` opened at 11:14 UTC**
(line 1481). The earlier series are `20260912` **B-H** and `20260913` **I-L**, as stated. **No
identifier-succession rule exists** in `AGENTS.md`, in the ledger, or in
`skills/minireason-experiment-operations/SKILL.md` — all three checked.

**Two precision defects in the identifier discussion, both should-fixes, neither adjudicating
anything:**

1. **"no identifier of more than one letter occurs anywhere in the file" is true of receipt
   identifiers but not of the string.** `grep -oE 'REC-[0-9]{8}-[A-Za-z]{2,}'` returns two hits, both
   **filenames**, not identifiers: `docs/errata/REC-20260913-windows-execution.md` (lines 902, 1252)
   and `docs/errata/REC-20260913-h003-preparation.md` (line 930). The sentence should say "no receipt
   **identifier**", since a publisher checking it by grep will find two matches.
2. **The stated justification for `-AA` is false, and it sits inside a paragraph a publisher is
   invited to append to the ledger verbatim.** `CHANGES-v4.md`:286-289 justifies the scheme "because
   it **sorts after every single-letter identifier under the ordinary lexical comparison** a reader or
   a grep would apply within a fixed date". Under ordinary lexical (byte) comparison
   `REC-20260914-AA` sorts **before** `REC-20260914-B` and before `REC-20260914-Z` — verified with
   `LC_ALL=C sort` and in Python (`'REC-20260914-AA' > 'REC-20260914-Z'` is `False`). The scheme may
   still be the right one (it is shortlex/spreadsheet-column continuation, and the other three
   candidates are rejected for good reasons), but **that clause must be corrected or deleted before
   the note is appended**, or a false Measured-shaped statement enters the published ledger.

Everything else in §7 is sound: each figure names its rule, the whole table is declared to
"**adjudicate nothing**" and to "**be re-read — under a stated definition — at the moment of the
append rather than carried from this document**", `-AA` is offered as a proposal A001 "**does not
mint**", and the fallback ("If the publisher rejects the scheme, the receipt takes whatever
identifier the publisher's own rule yields and the `Letter:` field records that rule instead") means
the staging no longer hands the publisher an unexecutable step — which is what F63 asked for.


**Observed during this check, and material to items 1-2 below.** While this file was being written, a
concurrent session agent (`publisher-loop-checkpoint`) appended a line to `docs/AGENT_ACTIVITY.jsonl`
carrying `"decision": "REC-20260914-AA"` — so **the `-AA` scheme is already in use elsewhere in this
session**, before A001 appends anything. Two consequences: the identifier A001's §7 proposes may no
longer be free at the moment of A001's own append, which is exactly the condition §7's `Letter:` field
is written to check; and the false sorting justification (item 1) becomes more urgent, since the
paragraph containing it may now be appended to the ledger for a receipt that already exists. It also
means the §7 count table will be stale at the append, as §7 itself pre-declares. *(That working-tree
modification is not this check's: nothing in the repository was written, staged or committed here, and
`docs/DECISION_LEDGER.md` is still byte-identical to HEAD, so every figure above stands.)*

---

## 6. Metric-creep lens (ruling 7)

### VERDICT: **no metric, rate, ranking or threshold has entered an adjudication. Counts are present in four rendered tables, each explicitly declared non-evidence at the point of use.**

A lexical scan of `STAGING-v4.md` and `CELLS-v4.md` for `rate|ratio|percent|%|threshold|majority|
average|mean|median|score|scoring|rank|ranking|proportion|frequency|tally|aggregate` returns **zero
hits in both files**. There is no vote, no majority, no averaging (the two-reader rule says
disagreement is "recorded, never averaged"), no cross-family comparison, and no progress meter.

The counts that do appear in rendered tables, each with the guard that governs it:

1. **The branch distribution** (§3 and `CELLS-v4.md`) — 1 / 4 / 2 / 6 / 0 / 0 / 19 / 1 / 33. Headed
   "**Coverage fact about A001's own bridge. Not evidence, on any side**", guarded again by §6 ("the
   branch counts of §3 and the cell counts of §8.5 are coverage facts, never evidence") and by rule 6
   ("**A count of cells, of any kind, on any side** … no count adjudicates anything").
2. **The read/gated split** — 13 / 19 / 1. Descriptive; the gate is a per-cell predicate ((b5) or E3,
   or a record-level absence), never a count or a cut-off.
3. **The receipt count table** (§7) — declared to "adjudicate nothing" and to be re-read at the
   append.
4. **The E3 exclusion table** — 19 of 20 coordinates, 8 PARTIAL / 11 FAILED, 12 nodes, 7/8/6/5/6/9/6/7.
   Each exclusion is defined per coordinate or per node; §4 finding 3 says the cell "supplies no
   evidence for or against S or N, and **no cell of that kind may be counted on either side**", and
   FW5:688 is quoted against it.

**The two places a count comes closest to argumentative work, named so a later reviewer can go
straight to them:**
* **"five of the six branches are fitted"** (§3, P8, §8(3), `CELLS-v4.md`). It is a summary of a
  charge **against A001's own bridge**, and the charge itself is stated as a universal with per-branch
  exhibits ("every branch that fires at all fires **only** on cells whose `bearing` text that branch's
  own condition paraphrases"), not as a count crossing a bar. It charges A001, never FW5.
* **"every one of the seven read-cell classes has a witness over the 13 read cells"** (§5(b),
  `CELLS-v4.md`, §6). This is a structural claim about the table's own well-formedness, with each
  witness named and argued individually; §6 forbids reporting any class as reachable "in principle",
  and an empty class "is reported as empty over 13 cells, never as evidence".

The only thresholds anywhere in the material are instrument bounds of the kind ruling 7 permits (the
8192 `max_tokens` ceiling recorded as a resource fact under FW5:688). **No threshold on a reading's
standing exists in v4.**

---

## 7. Claim ceiling, two-reader rule, "exhaustion" language, published observations

### VERDICT: **CLOSED — all four intact**

* **Ceiling extended, never relaxed.** Parsed §6 of v3 and v4: **all 14 v3 items are retained** (three
  lose only their "New at v3:" prefix; the text is otherwise unchanged) and **four v4 items are
  added** — the every-λ withdrawal, the prose leg's yield being one finding 1 and no more, "five cells
  lost a respect and none gained one", and "no class of §5(b) may be reported as reachable 'in
  principle'". Nothing was dropped or weakened. §6 still carries "**A001 offers no counterexample to
  sufficiency and none to necessity**", "**No cell of the executable leg can charge Account**", and
  the still-owed deliverable.
* **Two-reader rule intact and verbatim.** §5(b): "Two readers per cell; where they disagree the cell
  is `unresolved` and the disagreement is recorded, never averaged (FW5:634; C001 PLAN §8a:743-745)."
  Both sources read at the line: FW5:634 is "An observer may lack the data needed to establish the
  witness. That makes the attribution unresolved; it does not prove either understanding or its
  absence."; `experiments/diagnostics/C001-contrast-triple/PLAN.md`:743-745 is "**Two readers.** …
  Where two readers disagree on a register, that register is `unresolved` for that cell and the
  disagreement is recorded, never averaged (FW5:634)." No vote, no majority, no threshold.
* **No "exhaustion" language.** The only stems are "exhaustiveness" (the class table's definitional
  property), "exhaustive enumeration" (describing FW5:1402's own four-assignment check) and "the
  enumeration is not exhaustive" (about v2's two-horn dilemma). The 2026-09-14 identifier series is
  described as "**all taken**" and as a naming boundary, never as exhausted. Nothing claims a search
  space was exhausted.
* **No published observation modified.** `git status --porcelain` is empty at HEAD; the string `A001`
  appears **nowhere** in the repository (`grep -rl`, 0 files); neither
  `docs/reviews/A001-account-challenge-2026-09-14.md` nor
  `experiments/diagnostics/A001-account-challenge/` exists; **zero** `runtime_files` entries across
  246 entries in all `experiments/**/*.json` point under `experiments/` or `docs/`; and
  `campaign.source_identity()` at `src/minireason/campaign.py`:35-47 hashes `src/**/*.{py,json}` plus
  `pyproject.toml` only. All five register pins and the edition hash re-hashed exact.

---

## PUBLISHABLE AS IN-PROGRESS RECORD: yes

All three round-3 blockers are closed — F51 outright, F52 and F53 with residue that is disclosed in
the document itself and that only the reading step can settle. The register, the branch distribution,
the read/gated split and every ledger figure reproduce exactly from the pinned bytes at the stated
commit. The claim ceiling, the two-reader rule and the non-interference facts are intact, and no
count, rate, ranking or threshold has entered an adjudication. Nothing found here inflates a claim;
the two defects with real content (the unrecorded (b6) edit and the false `-AA` sort justification)
both cut against A001's own instrument or its own housekeeping, not against FW5.

---

## Residual open items, to be carried into the published record **verbatim**

*Numbered for citation. Items 1-2 should be fixed before or at the append; items 3-9 are for the
reading step and for whoever attacks this record next.*

1. **The `-AA` justification contains a false statement about sorting, and it sits in a paragraph a
   publisher is invited to append to `docs/DECISION_LEDGER.md` verbatim.** `CHANGES-v4.md`:286-289
   says the scheme was chosen partly "because it sorts after every single-letter identifier under the
   ordinary lexical comparison a reader or a grep would apply within a fixed date". It does not:
   `REC-20260914-AA` sorts **before** `REC-20260914-B` under byte-order comparison. Correct or delete
   that clause before appending; the scheme itself may stand on its other two reasons.
2. **"No identifier of more than one letter occurs anywhere in the file" should read "no receipt
   identifier".** Two `REC-<date>-<letters>` strings of more than one letter do occur, both as
   filenames: `docs/errata/REC-20260913-windows-execution.md` and
   `docs/errata/REC-20260913-h003-preparation.md`.
3. **The (b6) branch condition was edited between v3 and v4 without the edit being recorded, and §3's
   fitting disclosure still cites the deleted clause.** v3's (b6) row carried "(e.g. 'alleges an
   internal inconsistency between …')"; v4's does not, while §3 and `CELLS-v4.md` both charge (b6) as
   fitted on the ground that "its stated example" is six cells' `bearing` verbatim. Restore the
   example to the rule, or rewrite the disclosure to charge (b6) on its general condition. The frozen
   cell assignments are unaffected.
4. **The X3 witness (A15) and the X1 witness (A16) cannot both be occupiable under one reader's
   reasoning.** Six cells share one identical `bearing` string ("alleges an internal inconsistency
   between raising c6 and leaving c3 and c4 unchanged": A15, A16, A17, A21, A22, A23). X3's witness
   argues that no admissible \(D\) exists because the defect spans three records against a
   single-record grain — an argument about the defect, not the target — so it applies to A16 as well,
   and X3 (order 1) pre-empts X1 (order 6). Attack this before the A15-only doubt `CHANGES-v4.md` §6
   item 3 raises.
5. **The X2, X2b, X1 and X1b witnesses do not state the `not-free` condition they need to pass X5.**
   Sharpest at A04/A05, which share one referring record and one identical `bearing`: A04's X5 witness
   exhibits a flipping D6 alternative while A05's X2b witness asserts (E) fails "at the declared
   abstraction" at the same locus. A reader applying A04's alternative at A05 sends A05 to X5.
6. **The `not-free` branch's "searched, none exhibited" is a weak record that could become a default,
   which would make X5 unreachable — the mirror of the defect F53 caught.** `STAGING-v4.md` does not
   state that the worksheet forces a reader to say which of the two `not-free` evidences was given;
   the §7 layout lists "the per-declaration free/not-free records" without that distinction. Fix the
   worksheet's columns before the reading step.
7. **Three seams in the class table, each resolved only by ordering or by prose outside the table:**
   (a) X5's condition and the four Boolean rows' conditions can both hold on one cell, and the Boolean
   rows do not carry "and neither reader records `free`"; (b) the :620 check is an exit to X4 that is
   not a row of the ordered table and fires before J1/J2; (c) the gate's internal order is stated as
   X0-then-X4 in the class table and §3/`CELLS-v4.md`, and as X4-then-X0 in §5(b) procedure step 1.
8. **(r3) makes counterexample status very hard to reach under A001's own rule.** Because it fails as
   soon as *any* admissible gap-filling condition excluding the case can be named, "A001 offers no
   counterexample to sufficiency" is, for Case A-S, closer to analytic than evidential. The rule is
   unchanged since v2 and the direction is conservative, so this is recorded, not charged — but a
   later reviewer should decide whether (r3) is the rule A001 wants to keep.
9. **The literal phrase "under every \(\lambda\)" survives once, at §5(a)(i):623-624**, inside the
   "Under (P-Ans)" bullet that closes "This whole bullet is an Interpretation conditional on (P-Ans)".
   It is gone as an unconditional claim from §0, §6 and the receipt, which is what F51 required; a
   reader who quotes the sentence out of its bullet will misreport A001.
10. **Carried forward unchanged from `CHANGES-v4.md` §6, and still owed:** (P-Ans) is the single most
    attackable sentence in the document; the conditional rule of §3 is a rule about English, not a
    reading of FW5, and a second reader could reject it (and could ask whether it should also have
    moved A29, which asserts "the account leaves untouched" outright); §3's disclosure may be
    **over**stated in the self-charging direction, which §8(7) names as a regression of the same kind
    as re-inflation; and the "Testing FW5 itself" deliverable — a candidate counterexample and the
    clause that would have to change — **remains owed**, as does the independently sourced
    interpretive technical case.
11. **The `-AA` identifier is already taken elsewhere in this session.** A concurrent agent
    (`publisher-loop-checkpoint`) has recorded `REC-20260914-AA` in `docs/AGENT_ACTIVITY.jsonl` for the
    automated-loop checkpoint receipt. A001's §7 proposal must therefore be re-checked against the
    ledger at the moment of the append — which §7 already requires — and the `Letter:` field must record
    what was actually free, not what this staging proposed.
