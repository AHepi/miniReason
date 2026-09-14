# A001 — Account sufficiency / necessity challenge: staging

Staging only. Nothing here is published, no cell is filled, no reading is
offered, and no provider call was made or is planned. Sentences are marked
**Measured** (readable off a named file at a named line) or **Interpretation**
(a reading that could be wrong). Every claim traces to an FW5 line of the
designated reading edition, sha256
`8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a`, or to a
published record path.

This stage implements PURPOSE.md's "In parallel, an independent Account
sufficiency or necessity challenge tests FW5 itself" and the third row of
`docs/reviews/FW5-research-plan-decision.md`'s "Proposed work" table ("Testing
FW5 itself"). It is separately identified from the construction-and-use study
and from C001; it borrows C001's records and never its claim.

---

## 1. The particular semantic claims under challenge

The predicate. FW5:172 — "The following conditions define
\(\operatorname{Account}(\mathcal E)\)" — over the structural account
\(\mathcal E=(E,p,\pi,\tau,\sigma,\lambda)\) (FW5:164-168), with the five
conjuncts Anchoring (:174-176), Structural fidelity (F) (:179-186) with
composition (C) (:188-195), Question fidelity (A) (:199-208), Non-circular
dependence (:210) and Non-vacuity (:212), collected at (E), FW5:216-224.

**Claim S (sufficiency).** FW5:226 — "The right side is determined by the
specified structures and maps. It contains no predicate that already means
'really explains.'" FW5:228 — "Its strongest claim is that these structural
requirements, correctly interpreted, capture explanatory accounting." The
sufficiency half: satisfying the five conjuncts suffices for the
explanatory-accounting attribution FW5 then makes of \(\mathcal E\), including
its downstream uses — Bearing at (K1), FW5:614-620, and the
\(\operatorname{Account}(c,p_c)\) conjunct of (EK), FW5:831.
FW5 states its own defeater at :1364 — "a fully specified candidate satisfying
(E) ... which nevertheless provides no explanatory account. That would refute
the sufficiency claim."

**Claim N (necessity).** The same sentence's other half, FW5:1364 — "A genuine
explanation that cannot satisfy the conditions under any interpretation
preserving its actual organization would refute necessity." Restated at
FW5:1502 — "Its strongest unresolved issue is whether the proposed structural
conditions capture all and only the intended explanatory organization." The
membership consequence is at FW5:1192: the base class \(\mathsf{FW5}\) consists
of interpretations supplying the data and satisfying the typing and
realization conditions; a genuine explanation outside it is outside the class.

**Two claims FW5 makes that A001 does NOT challenge, named so they are not
absorbed.** (i) The mathematical results — equivariance (:1200-1206), the
projection theorem (:1208-1224), the finite monotone theorem (:296), the
retention fixed point — where FW5:1390 says a counterexample "would expose a
mathematical error", a different finding. (ii) The declared-input boundary for
normative and physical content (:37-41, :902-904); a complaint that FW5 does
not derive \(\mathcal N\) is not a counterexample, because FW5 states the
dependence rather than concealing it.

---

## 2. Primitive dependencies, marked

**Interpretation** throughout this table; the FW5 lines are Measured.
"Defined" = the reading edition fixes it in declared mathematical data.
"Undefined" = the reading edition uses it as load-bearing without fixing it.
"Defined-but-unmapped" = fixed in the source, with no stated route from a
published record to it.

| # | dependency | FW5 line | status | why |
|---|---|---|---|---|
| D1 | organization \(D=(V,(X_v),J,B,A,L,\mathrm{role})\); solutions (O) | :85, :99 | defined | typed tuple; (O) is set equality |
| D2 | question \(p=(D,\Sigma,b_0,\kappa,\mathcal C,\mathcal Q,O_p)\); (Q) | :117-121, :125-131 | defined | typed tuple |
| D3 | respect \(\kappa\) | :123 | **undefined** | fixed by an open example list ("production, inferential identification, impossibility, rule-governed status, achievement of an aim, or aesthetic value"); no membership condition, no individuation of two respects |
| D4 | contrast contract \(\mathcal C\) | :123 | **undefined** | "distinctions **material to that question**"; materiality is the load-bearing word and is not defined |
| D5 | the maps \(\pi,\tau,\sigma,\lambda\) with declared domains | :166-170 | defined | declared data; many-to-one permitted for \(\pi\) |
| D6 | "the declared abstraction" at which the projected target relation must equal the explanatory component relation | :176 | **undefined** | the abstraction is a free declaration; no condition ties an admissible abstraction to \(\kappa\) |
| D7 | grain \(\ell\) | :154 | **undefined** | "A grain fixes which structural distinctions count as differences for the attribution at issue" — a stipulation, with no admissibility condition relative to \(\kappa\) or \(\mathcal C\) |
| D8 | active commitments vs incidental remarks | :162 | **undefined** | "part of the interpreted claim"; no procedure, and FW5 explicitly forbids an assessor selecting fragments |
| D9 | (F), (C), (A) | :185, :194, :205 | defined | equalities and an indexing condition |
| D10 | non-circular dependence, incl. "at least one admitted contrast that removes or changes a nonempty block of active organizational commitments" | :210 | defined, on D4/D7/D8 | the clause is exact; its inputs are not |
| D11 | non-vacuity, incl. "one defined to exclude every change that **could matter**" | :212 | **undefined** | "could matter" is undefined and is the clause's whole force |
| D12 | boundary \(\beta\), representation \(\operatorname{Rep}_{\beta,\ell}\) | :148-152, :156 | declared primitive | FW5 says so: "an explicit semantic primitive" |
| D13 | structural equivalence at grain, \(d\equiv_\ell c\) | :738-746 | defined, unmapped | "structural at the stated grain, not string equality or similarity"; no record-level test |
| D14 | Bearing (K1): \(\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal E_c,p_\delta)\) | :614-620 | defined, **mapping unsupported** | identifies criticism-bearing with accounting; the route from an authored criticism to \(\mathcal E_c\) is not stated |
| D15 | criticism constituents \(z,\delta,g\), connection | :609 | defined | four-part |
| D16 | active route; nonconstant dependence on the represented distinction | :601 | defined, unmapped | requires actual occurrences, ports, component relations; "not inferred from the presence of a similar sentence in a record" |
| D17 | reason-use witness and its three-case contrast contract | :628, :630 | defined, unmapped | a structural map preserving internal role bindings; C001 PLAN §9 records that a transcript supplies none |
| D18 | standing \(\operatorname{Live}_j\), (K2) | :638, :642-651 | defined, unmapped | appraisal-indexed; FW5:640 — prompt appearance is a delivery fact, actual use is "not automatically machine-maintainable" |
| D19 | repair (P) with \(O\), \(P\), \(\operatorname{ProducedBy}\) | :787-800 | defined, unmapped | not challenged here; named because (EK) carries Account |
| D20 | Account from a record | :1208-1224 | **unmappable by FW5's own theorem** | "no function of \(P(M)\) alone agrees with the accounting predicate" (:1218); "semantic use inferred from delivery logs" (:1222); the theorem "identifies missing information in a projection" (:1224) |

**The one published mapping candidate.** The C001 correspondence table
(`experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md`, sha256
`dcaebaf8336c1943700a762b4836679307349d6ff8dfad082e4cd77e23fd7ae7`; 85 units,
five declared rules, published before dispatch) is a proposed, checkable
instance of D13 for one criticism document. A001 uses it as a *candidate*
mapping and tests it; it does not assume it.

---

## 3. Grain, boundary, contrasts — fixed before any evidence

Declared under `docs/SEMANTIC_GUIDE.md` "Declare the interpretation before the
evidence" and FW5:728 ("Fix a system boundary, grain, history, and continuity
criterion before assessing an event").

| item | A001 declaration |
|---|---|
| **unit that counts as a case** | Prose legs: one fully specified \(\mathcal E=(E,p,\pi,\tau,\sigma,\lambda)\) with its target organization and question, authored in this document. Executable leg: one **authored criticism record** (an FCL-1 record of `type: "objection"`, or a record carrying a `bearing` field) **together with one declared target record**, i.e. one row of a published use table. Not a document, not a node, not a cell of C001. |
| **grain \(\ell\)** | the FCL-1 record keyed by id, with its `text`, `scope`, `grounds`, `bearing`, `action`, `consequence` fields and its ref arrays retained; ids and prefixes retained. This is C001's own declared grain (C001 PLAN §10) and the use-relation instrument's own subject definition. Chosen before reading; if it is changed later the claim changes with it (FW5:133; `docs/SEMANTIC_GUIDE.md`, "Changing the question, grain, anchors or protected obligations makes a new claim"). |
| **boundary separating the studied system from its inputs** | The studied system is the **criticism content** and the **target content** as published bytes. Outside it: the model, the endpoint, Mini's graph, the scheduler, the store, the operator-supplied FCL-1 language, the H005 instructions, the decoder, the importer and the use-relation instrument. A001 makes **no attribution to any model or endpoint**, so the usual "model + Mini + configuration" boundary is not invoked and no model-only argument is owed. |
| **respect \(\kappa\)** | for each case, the respect the criticism record's own `bearing` field names, quoted verbatim into the worksheet. Where the record names no respect, the case is **unresolved** and is not supplied with one. |
| **contrast used** | Account's own contrast requirement, **FW5:210** — at least one admitted contrast removing or changing a nonempty block of active organizational commitments of the target, with the answer profile changing or ceasing to be determined. **Not** FW5:630's three-case contract. |
| **FW5:630's three-case contract, where it does enter** | only in leg E2, and only as a check on D13 (equivariance of (E) under a genuine recoding, FW5:1200-1206). C001's registers T/E/D/G are reason-use registers; A001 does not fill them, does not reuse their marks, and does not read an Account result off them. |
| **history / continuity** | none claimed. A001 compares contents, not episodes. |
| **normative relation invoked** | none. No merit, adequacy-of-the-model, or progress predicate is applied to any model or output. |
| **enabling contributions** | FW5 itself, the FCL-1 language, the H005/F001 material and instructions, the two published instruments, the C001 recoding table. |

---

## 4. What a counterexample would require FW5 to relinquish

**If Claim S falls** (a fully specified \(\mathcal E\) with all five conjuncts
true at a defensible \(\ell\) and \(\kappa\), which is not an explanatory
account of its target): FW5 must relinquish **:226**, that the right side of
(E) "contains no predicate that already means 'really explains'" — because the
repair is a sixth condition, and the only candidates are (a) a further
substantive structural condition, (b) a primitive of the kind banned at :37
(`Because`, `ExplanatoryWork`), or (c) an admissibility condition on
\(\ell,\kappa,\mathcal C\) that the reading edition does not state. It must
also relinquish **:228**'s "capture explanatory accounting" in the sufficiency
direction, and, downstream, **(K1) at :620** (bearing would no longer follow
from accounting) and the \(\operatorname{Account}(c,p_c)\) conjunct's force in
**(EK) at :831**. It does **not** require relinquishing (O), (Q), the
equivariance theorem, the projection theorem, (CT4), (RC), or any mathematical
result (FW5:1390).

**If Claim N falls** (a genuine explanation that cannot satisfy the conditions
under **any** interpretation preserving its actual organization): FW5 must
relinquish **:228** in the necessity direction and the **Membership** clause at
:1192 as an account of which interpretations contain explanation, and must
either widen (E) or concede that explanation has instances the class cannot
represent. FW5:1372 already names the shape — "If they exclude a genuine
inexplicit or distributed understanding, it is too strong."

**What no counterexample here can require.** FW5:1392 — "A physical or semantic
counterexample to an application can defeat that application without changing
the model-class definition." FW5:1336-1344 ("What the executable audit does and does not settle") and
PURPOSE.md — an implementation failure refutes nothing about the class.

### Three different findings, kept apart

1. **A missing definition** (D3, D4, D6, D7, D8, D11). Shows that (E) is not
   yet determinate for a given (target, question) pair: a claimant can make
   (E) true or false by a free declaration. This **defers** both S and N; it
   refutes neither, and it must not be reported as a counterexample. Its
   remedy is a separately identified gap-filling proposal (§7), which must not
   be back-fitted to whatever the evidence turns out to be.
2. **An unsupported mapping** (D14, D16-D18, D20, and D13 if the C001 recoding
   table fails its own content-preservation argument). Shows that a bridge
   from published records to a FW5 relation is unwarranted. It defeats the
   application, not the class (FW5:1392). It is also the finding that would
   land on **(K1)** rather than on Account: if a criticism plainly bears and
   its \(\mathcal E_c\) plainly fails, the first suspect is K1's
   identification, and the report must say which of the two it charges.
3. **An operational failure** (e.g. the `deepseek-flash` × `fcl` cell of C001
   occurrence-01: 19 of 20 coordinates consumed by an 8192 completion ceiling,
   `COMPARISON.md` lines 40-59). Shows a resource fact. FW5:688 — "The
   inability to evaluate a proposition is not a falsifying observation of the
   proposition." It supplies no evidence for or against S or N, and no cell of
   that kind may be counted on either side.

---

## 5. The challenge as criticizable contributions

### 5(a) Prose-only leg — two authored cases

**Case A-S (sufficiency).** *A structural account that satisfies (E) while
anchoring a route that did no work.* Take FW5's own discriminating pair: the
parallel and priority wiring constructions it introduces at :1222 and checks by
exhaustive enumeration at :1402 ("All four Boolean input assignments were
checked for the parallel and priority constructions. Their endpoint outputs
agree, while the active second route differs when both inputs are on"). Let the
target \(D\) be the **priority** organization, in which route 2 is live only
when route 1 is off; let the candidate explanatory organization \(E\) be the
**parallel** one, with \(\lambda\) anchoring its two routes to the target's two
routes and \(\pi,\tau,\sigma\) the identity on the endpoint ports. Declare the
abstraction of :176 and the grain of :154 at endpoint level, and \(\kappa\) as
production of the output. Then: Anchoring holds at that declared abstraction
(each component's projected relation equals the explanatory component
relation); (F) and (C) hold on \(\Sigma\cap\mathcal C\) because the two
constructions agree on all four assignments; (A) holds, since the answer
profile is the same function; non-circular dependence holds, because deleting
the block of both routes changes the answer; non-vacuity holds, since the
baseline has compatible states. The attribution "\(E\) accounts for the
target's production of the output" is nevertheless false of the target when
both inputs are on, and FW5's own theorem at :1208-1218 is the reason it is
false. The case's declared dependencies are exactly D6, D7, D3 and D4: FW5's
available reply is that this abstraction is inadmissible for this \(\kappa\) —
and that reply needs an admissibility condition the reading edition does not
contain, so the case terminates in **either** a sufficiency counterexample
**or** finding 1 (a missing definition), and the report must say which and
why, before the grain is touched. Changing the grain after the fact to rescue
either side is exactly what `FW5-research-plan-decision.md` forbids and what
this staging pre-commits against.

**Case B-N (necessity).** *A genuine explanation whose actual organization
admits no determinate anchoring.* Take an inexplicit, distributed diagnostic
explanation of the kind FW5 itself admits at :857-861 ("partial, distributed,
or temporally extended", available "through memory, imagery, action rehearsal,
or interaction with an artifact") and at :246 ("A thinker need not possess the
maps in explicit notation to instantiate the relevant organization"): a
practitioner who correctly explains a recurring fault, acts on the explanation,
and repairs the fault, but whose realization has no decomposition into
components with stable footprints \(V_j\). (E) demands more than that the maps
exist unpossessed: it demands that they exist *determinately*, because (C) at
:194 requires \(\tau(a_2a_1)=\tau(a_2)\tau(a_1)\) "for every composition for
which a claim is made", and Anchoring at :176 requires a port translation "for
each component". If several inequivalent anchorings \(\lambda\) are each
compatible with the realization and (E) comes out true under one and false
under another, then either necessity fails (the explanation is genuine and no
interpretation preserving its actual organization satisfies the conditions) or
FW5 owes a determinacy condition on \(\lambda\) given a realization — again
findings 1 and 2 rather than a counterexample, and again the report must say
which. The case's declared dependencies are D5, D6, D8, D12 and the realization
conditions FW5 defers to its constructor section (:987-:1012). Its standing
limitation, stated in advance: FW5:1372 names this attack itself, so a version
of it that merely restates :1372 contributes nothing; the contribution has to
be the *determinacy* step, and if the determinacy step fails the case fails.

Neither case is an independently sourced interpretive technical document; that
gap, named at the end of `docs/reviews/FW5-account-skew-matrix-challenge.md`,
stays open and A001 does not close it.

### 5(b) Executable leg — published records and instruments only

No provider call. No new instrument. No cell of any published table is filled
by A001; A001 writes its own worksheet, whose rows cite published row ids.

**Route.** (K1) at FW5:614-620 makes Account the whole content of criticism
bearing. Each published use-table row carried by a criticism record is
therefore an instance of the Account predicate at \(p_\delta\) — the only place
in the repository where a published record addresses Account at all. The
executable leg reads those rows against (E) and records, per row, whether the
five conjuncts are satisfiable at the declared grain.

**Cells — frozen before reading (32 bearing cells).**

Pins: `use-table-golden/use_table.json` `875d674f85f95f09eb1be1354c194f8a79c04298a0556033df52781bef8c723a`;
`use-table-full/use_table.json` `39981b3c1923472243d89c7c78e0e0ded99bc6a7d9eef451fa46e798caca0a4f`;
C001 `occurrence-01/comparison.json` `00452db2586b5f33e3eed58c8a7d01efe6da9d6616ce3423fb76d8795af9d31d`;
`occurrence-02/comparison.json` `4e7ea3894cfe125ba2507dd761f30d13b5226818fe77f9a91665d05c67bc109b`;
`RECODING_TABLE.md` `dcaebaf8336c1943700a762b4836679307349d6ff8dfad082e4cd77e23fd7ae7`.

*E1 — bearing cells (10), H005 occurrence-01 snapshot, `use-table-golden`
rows 0, 1, 2, 3, 4, 10, 11, 13, 16, 17 (identical rows in `use-table-full`):*
`objection#o1→account#c1`, `objection#o1→account#c2`,
`objection#o2→account#c2`, `objection#o3→account#c2`,
`objection#o3→account#c3`, `response#k3→rival#r6`, `response#k3→rival#r9`,
`response#k7→rival#r9`, `carry#n3→response#k2`, `carry#n3→response#k7`.

*E1 — bearing cells (22), F001 analyses:* occurrence-01 rows 0-8 and 19-22
(`objection#o1→account#c1..c4`, `objection#o2→account#c6,c3,c4`,
`objection#o3→account#c2,c5`, `carry#r5→response#m5`,
`carry#r6→account#c3,c4,c6`); occurrence-05 rows 3-10
(`objection#o1..o5→account#u1,c1..c4`); occurrence-07 row 1
(`rival#r5→account`, target record id absent — see the unresolved rule).
Occurrences 02, 03, 04, 06 and 08 contribute **zero** cross-document rows;
that is a fact about those documents' authored refs, not about their authors,
and it is recorded as a cell count of zero, never as a negative finding.

*E1 — declared-use rows, a separate register (12 rows, `use-table-golden` rows
5-9, 12, 14, 15, 18-21):* carried by `claim`, `use` and `problem` records.
These are **not** bearing cells; FW5:640 makes a declared field a delivery
fact. They are read only to record what the language declared, and they can
never supply a counterexample to S or N.

*E2 — equivariance cells (1 criticism document × 2 codings):* the C001
ORIGINAL objection block (byte-identical to
`H005.../occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json`, which
`prepare` enforces: `ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES`) against the
RECODING block, unit by unit over the published 85-unit table. The reader
marks, per E1 bearing cell drawn from that document, whether its (E)
assessment is the same under both codings.

*E3 — non-evaluable cells, declared in advance and excluded from both sides:*
C001 occurrence-01 `deepseek-flash` × `fcl`, 19 of 20 coordinates
(`COMPARISON.md` "Unresolved in this cell", lines 40-59); the single PARTIAL at
`ollama-glm-5.3` × `fcl` CONTROL rep2; the 12 nodes whose commitment surface
was not read in `use-table-full` (`nodes_not_read`, 10 prose surfaces plus the
2 `unavailable_decode_failure` surfaces of
`docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md`); and the 7,
8, 6, 5, 6, 9, 6, 7 `nodes_not_read` of the eight F001 use tables.

**What would constitute a counterexample.**

* **Sufficiency counterexample (E1).** A bearing cell in which (i) all five
  conjuncts of (E) are satisfiable for \(\mathcal E_c\) at \(p_\delta\), at the
  §3 grain, with the respect quoted from the record's own `bearing` field, and
  (ii) the alleged defect demonstrably does not obtain of the quoted target
  passage — the target does not have the property the criticism's defect
  attributes to it — so the criticism does not bear while (E) holds. The report
  must exhibit the contrast of :210 it used and quote both passages.
* **Necessity counterexample (E1).** A bearing cell in which (i) the alleged
  defect demonstrably obtains of the quoted target passage at the record's own
  respect — the criticism bears — and (ii) **no** interpretation preserving the
  record's actual organization satisfies (E) at \(p_\delta\). "No
  interpretation" must be argued, not asserted from one failed reconstruction;
  `FW5-research-plan-decision.md` — "Failure of one selected encoding or grain
  is not that necessity result."
* **An equivariance failure (E2).** A bearing cell whose (E) assessment
  differs between the ORIGINAL and RECODING codings. This is **not** a
  counterexample to S or N. It is either finding 2 against the C001 table's
  content-preservation argument, or a challenge to FW5:1200-1206's
  applicability at this grain, and the report states which and why.

**What would NOT constitute a counterexample, pre-committed.**

1. A criticism whose `bearing` field is empty, or whose defect \(\delta\) is
   not separately addressable because FCL-1 has no \(\delta\) slot (the review's
   P6(i)). That cell is **unresolved** (FW5:634) and stays unresolved.
2. A bare id token shared between the objection and account documents; the same
   ambiguity C001's `E` register refuses to resolve.
3. A cell whose delivery is PARTIAL, FAILED, OPAQUE or undecoded (E3).
4. A lexical-overlap passage from the use table. The instrument's own banner:
   "A lexical overlap is not evidence of use."
5. Any difference between endpoints or families. A001 issues no cross-family
   comparison and none may be read off its worksheet (FW5:849, :851).
6. A count of cells on either side. Counts may defeat a claim of universality
   in the worksheet's own scope; none warrants an Account verdict (FW5:851).
7. A finding about C001's four registers. A001 does not fill or read them.

**Reading discipline.** Two readers per cell; where they disagree the cell is
`unresolved` and the disagreement is recorded, never averaged (FW5:634, C001
PLAN §8a). The worksheet's assessment columns are rendered empty by the
staging and are filled only by the reading step.

### 5(c) P3–P7, re-stated as separately identified gap-filling contributions

Source: `scratchpad/fw5/final-review-returned.md` §5 (published as
`docs/reviews/fw5-vs-harness-spec-2026-09-14.md`). Restated here under one
governing rule, taken verbatim from PURPOSE.md: "Proposed gap-filling
definitions, interpretations and mechanisms are separate criticizable
contributions; they must not silently rewrite the source or absorb adverse
evidence after the fact." Operationally, for each: it is published as its own
document with its own identity; it may not edit FW5 or any frozen PLAN; and
its acceptance condition is declared **before** A001's reading, so that an
adverse A001 result cannot be converted into a proposal's success.

| id | gap it fills | which A001 dependency | rule of engagement | offline today |
|---|---|---|---|---|
| **P3** criticism-ablation arm for F001 occurrence-02 | discharges `ProducedBy` (FW5:800), not Account | D19 | needs live calls; **out of A001's scope entirely**, named so it is not smuggled in as Account evidence | no |
| **P4** loss ledger (O, P pinned before the later cycle) | (P) at FW5:787-802 | D19 | must be pinned by sha256 *before* dispatch; a dry run over an existing pair is labelled as violating its own pre-declaration and establishes nothing | dry run only |
| **P5** custody and grain preconditions | D7, D13 | grain and partition-invariance preconditions on A001's own instrument; if P5 shows the §3 grain is not partition-invariant, A001's E1 readings are **preconditioned**, not rescued | yes |
| **P6** FCL-1's fields against FW5:609/:622 | D14, D15 | supplies the missing \(\delta\) slot diagnosis that decides how many E1 cells are unresolved by rule 1 above; it is a **language-adequacy** reading of one cycle, never an Account result | yes |
| **P7** pre-registered reading set | the observer, not the subject | all | A001's cell list in §5(b) **is** P7 applied to this stage: it is frozen here, and any addition is recorded with a reason with the original list retained | yes |

P3 and P4 are named and deferred. P5, P6 and P7 are the three that A001 can
carry offline, and P7 is already discharged by §5(b)'s frozen cell list.

---

## 6. Claim ceiling

* Nothing about creativity across all tasks, or about any model's repertoire.
  FW5:1256-1260; PURPOSE.md.
* No refutation of FW5 or ECS from an implementation failure, a ceiling, a
  decoder refusal or an unread surface. FW5:688; FW5:1336-1344 ("What the executable audit does and does not settle"); PURPOSE.md.
* A single failed candidate does not confirm FW5 — the precedent is
  `docs/reviews/FW5-account-skew-matrix-challenge.md`, whose own result is
  "this rejects one attempted witness; it neither confirms FW5 nor settles
  other sufficiency and necessity attacks."
* One reading of one cycle's records over 32 bearing cells cannot decide the
  constitutive conjecture. FW5:1368 — "These challenges concern the
  constitutive conjecture, not a missing proof of a theorem."
* A001 establishes no Origin (G), no Repair (P), no CreateEK, no reason-use
  witness, no standing, no recursive capacity.
* A001 issues no judgement about whether any H005 or F001 objection is a good
  objection. FW5:630 — "Understanding and using an invalid objection does not
  make it valid."
* A001 says nothing about ECS 2.0's graded accounting or intrinsic variation
  family; those are separately identified successor hypotheses.
* The two prose cases are authored by this study. The independently sourced
  interpretive technical case the skew-matrix review says is still owed
  remains owed.

---

## 7. File layout for publication, and why

**Choice: `docs/reviews/` for the documents, `experiments/diagnostics/` for the
executable leg.** Reason, from the repository's own conventions: there is no
`docs/challenges/` directory, and the single existing Account challenge —
`docs/reviews/FW5-account-skew-matrix-challenge.md` — already sits in
`docs/reviews/` with its offline check under
`experiments/diagnostics/fw5-account-skew-matrix/`. Creating a new top-level
`docs/` directory for one document would split the FW5-testing record across
two indexes for no gain, and would leave `docs/reviews/` holding one Account
challenge and not the other. `experiments/analyses/` is reserved in practice
for instrument outputs regenerated over frozen occurrences (H005 snapshot,
F001); A001's executable leg is a pre-registered reading with a frozen cell
list and falsifiers, which is what `experiments/diagnostics/` holds.

```
docs/reviews/A001-account-challenge-2026-09-14.md
    §1 claims with FW5 lines; §2 dependency table; §3 grain/boundary/contrast;
    §4 relinquishment + the three findings; §5(a) the two prose cases;
    §6 claim ceiling. Receipt paragraph at the head.
docs/reviews/A001-gap-filling-proposals-2026-09-14.md
    P3-P7 restated as separate criticizable contributions, each with its
    acceptance condition declared before the reading (§5(c)).
experiments/diagnostics/A001-account-challenge/PLAN.md
    Pre-registration of the executable leg: route via (K1), the frozen cell
    list, counterexample and non-counterexample conditions, the unresolved
    rules, the two-reader rule, claim ceiling, 0 planned provider calls.
experiments/diagnostics/A001-account-challenge/material.json
    source pins (FW5, both use_table.json, both comparison.json,
    RECODING_TABLE.md, both C001 materials) + the frozen cell list as data.
experiments/diagnostics/A001-account-challenge/CELLS.md
    the 32 bearing cells, 12 declared-use rows, E2 pairs and E3 exclusions,
    rendered from material.json.
experiments/diagnostics/A001-account-challenge/WORKSHEET.md
    one row per cell, assessment columns rendered EMPTY; filled only by the
    reading step, never by the staging.
docs/DECISION_LEDGER.md            one appended receipt (below)
docs/STATUS.md                     one row: A001 staged, reading not started
docs/workflows/README.md           one row if a workflow page is added later
```

No file under `experiments/diagnostics/C001-contrast-triple/`,
`experiments/diagnostics/H005-open-prose-commitments/`,
`experiments/diagnostics/F001-fork5-multifamily/` or
`experiments/analyses/` is written, moved or touched. A001 adds no identity
that any frozen plan depends on: no plan's `runtime_files` map contains a path
under `experiments/`, and `campaign.source_identity()` hashes `src/` and
`pyproject.toml` only.

### Receipt paragraph, house style

> REC-YYYYMMDD-X opened at HH:MM UTC: Stage A001, an independent Account
> sufficiency-and-necessity challenge to the designated FW5 reading edition
> (sha256 `8105925b…e33ee63a`), under PURPOSE.md ("In parallel, an independent
> Account sufficiency or necessity challenge tests FW5 itself") and the
> "Testing FW5 itself" row of `docs/reviews/FW5-research-plan-decision.md`.
> Choice: publish `docs/reviews/A001-account-challenge-2026-09-14.md` (the two
> named claims with their FW5 lines, the dependency table marking each
> primitive defined / undefined / defined-but-unmapped, the grain, boundary and
> contrast declared before any evidence, the relinquishment statement, the two
> authored prose cases, and the claim ceiling),
> `docs/reviews/A001-gap-filling-proposals-2026-09-14.md` (P3-P7 restated as
> separately identified contributions, each with its acceptance condition
> declared before the reading), and
> `experiments/diagnostics/A001-account-challenge/` (PLAN.md, material.json,
> CELLS.md and an empty WORKSHEET.md) — the executable leg over **existing
> published records only**: 32 bearing cells drawn from the H005 occurrence-01
> snapshot use tables and the eight F001 use tables, 12 declared-use rows kept
> in a separate register, one equivariance pair over C001's published 85-unit
> correspondence table, and a declared exclusion list of non-evaluable cells.
> Reason: the source's sufficiency and necessity claims are the place FW5
> itself says to attack it (FW5:1362-1364, :1502), and the repository has never
> tested them against its own published records; a missing definition, an
> unsupported mapping and an operational failure are recorded as three
> different findings and never as one. Contribution to the end goal: a
> separately identified test of the semantic source, with its dependencies
> named before the evidence, so that neither a favourable nor an adverse
> reading can be produced by moving the grain afterwards. State: pending —
> **zero provider calls planned and zero made**; no cell of any published table
> is filled by this stage and every assessment column of WORKSHEET.md is
> published empty; the reading step is a separate receipt. Evidence: pins
> recorded in `material.json`; nothing under `experiments/diagnostics/C001-*`,
> `H005-*`, `F001-*` or `experiments/analyses/` written or touched.

### What needs a live call

**Nothing.** Every leg is offline: the prose cases are authored, the executable
leg reads published bytes, and the equivariance check reads a published table.
The only step that could be argued to need a fresh reading is the two-reader
rule of §5(b). It is **not** a live provider call and it does **not** go to a
human as a blocking dependency: it routes to the automated loop's reader roles
— the same delegated-reader/refuter arrangement recorded in the provenance
paragraph of `docs/reviews/fw5-vs-harness-spec-2026-09-14.md` ("six readers …
six refuters checking every citation at source") — with every FW5 line and
every record path re-read at the line. P3 and P4 would need live calls; both
are deferred out of A001 in §5(c) and neither may be reported as Account
evidence.

---

## 8. Concerns carried into the reading step

1. **K1 is the weakest joint.** Everything the executable leg can reach passes
   through FW5:614-620. An adverse E1 result is at least as likely to be a
   finding against K1 as against Account, and the worksheet must force the
   reader to charge one of the two explicitly rather than write "Account
   fails".
2. **The FCL-1 records were not authored as \(\mathcal E\).** They were authored
   as criticisms in a language with `target`, `grounds` and `bearing` but no
   \(\delta\) slot (review P6(i)). Reconstructing \(\mathcal
   E_c=(E,p_\delta,\pi,\tau,\sigma,\lambda)\) from such a record is itself an
   interpretation, and a failed reconstruction is finding 1 or 2, not a
   necessity counterexample. This is the largest risk of over-claiming.
3. **Case A-S may be absorbed rather than answered.** FW5 can reply that the
   endpoint abstraction is inadmissible for a production respect. The reply is
   reasonable and undefined; the case must be published with that reply printed
   beside it, and the missing admissibility condition named as the finding,
   rather than the case being quietly upgraded to a refutation.
4. **The grain is C001's, not A001's.** Adopting the record-keyed grain keeps
   A001 comparable with the published material but inherits P5's open
   partition-invariance question. If P5 later shows the reading does not
   survive re-partition, A001's E1 cells are preconditioned, not rescued.
5. **Cell supply is thin and uneven.** 10 bearing cells in H005 golden; 22
   across F001, of which 13 come from one occurrence and four occurrences
   supply none. No universality claim of any kind may be built on that
   distribution, and the zero-row occurrences must be reported as zero rows,
   not as silence.
6. **Two published Account challenges will then exist.** The skew-matrix
   challenge concluded that its candidate failed. A001 must not be read as its
   successor or as an attempt to overturn it; it is a separate attack branch
   with a different route (K1 and published records rather than an authored
   mathematical case), and the published document should say so in its first
   paragraph.
