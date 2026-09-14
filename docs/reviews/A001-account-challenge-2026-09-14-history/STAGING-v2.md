# A001 — Account sufficiency / necessity challenge: staging, revision 2

Supersedes `STAGING.md` (v1) in this directory, which is retained unedited
beside it together with `REVIEW.md`, so the revision is diffable.
`CHANGES.md` maps every finding id F1-F29 to fixed / withdrawn /
declined-with-reason. `CELLS-v2.md` carries the revised pre-registered cell
list.

Staging only. Nothing here is published, no cell is filled, no reading is
offered, and no provider call was made or is planned. Sentences are marked
**Measured** (readable off a named file at a named line) or **Interpretation**
(a reading that could be wrong). Every claim traces to an FW5 line of the
designated reading edition, sha256
`8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a`, or to a
published record path.

---

## 0. What this is, and its relation to the skew-matrix challenge

A001 takes up one of the cases that
`docs/reviews/FW5-account-skew-matrix-challenge.md` names as still open in its
closing paragraph — "Cases involving interpretive scope, genuine inexplicit
understanding or the Account-to-epistemic-obligation connection remain open" —
and takes up the **interpretive-scope** case, in the form of the (K1) mapping
from published criticism records to Account. **A001 does not overturn that
review's result and does not reopen it**: its candidate failed, and A001 agrees
that it failed. A001 is a **second sufficiency attempt by a different route**:
the skew-matrix review authored a mathematical case, A001 begins from FW5's own
discriminating construction (parallel/priority wiring) and from published
records. Its sufficiency attempt also fails, and this document says so and says
why, rather than carrying the case forward as a "possible counterexample". The
**genuine-inexplicit-understanding** case was attempted here as Case B-N and is
**dropped** (§5(a)(ii)); it remains open, and A001 does not close it. The
**Account-to-epistemic-obligation** connection at (EK), FW5:831, is not touched.

**Authority. (Measured.)** The two prose legs implement the "Testing FW5
itself" row of `docs/reviews/FW5-research-plan-decision.md`'s "Proposed work"
table, which asks for "an independent challenge to Account sufficiency or
necessity in a demanding mathematical, non-causal or interpretive technical
case" and adds "Mini performance, checker acceptance and model agreement cannot
replace the independent explanation argument". The **executable leg does not
implement that row**: it reads Mini's own FCL-1 records, which are neither one
of the three named case types nor independently sourced. It is carried instead
under PURPOSE.md's "In parallel, an independent Account sufficiency or necessity
challenge tests FW5 itself" and under P5, P6 and P7 of
`docs/reviews/fw5-vs-harness-spec-2026-09-14.md` §5. That decision note still
reads `Status: proposed, awaiting the user's approval`, so **PURPOSE.md carries
the authority for this stage and the decision note is cited as a statement of
intent, not as an approval.**

**Result of this revision, stated first.** A001 no longer offers any candidate
counterexample. It offers three things: a dependency table over (E)'s
primitives; a pre-registered (K1)-mapping test over published cells whose
maximum reach is an unsupported-mapping finding; and the recorded reasons why
two authored prose cases fail. Under PURPOSE.md — "A missing definition, an
unsupported mapping and an operational failure are different findings" — that
is a legitimate result and is published as such.

---

## 1. The particular semantic claims under challenge

The predicate. FW5:172 — "The following conditions define
\(\operatorname{Account}(\mathcal E)\)" — over the structural account
\(\mathcal E=(E,p,\pi,\tau,\sigma,\lambda)\) (FW5:164-170), with the five
conjuncts Anchoring (:174-176), Structural fidelity (F) (:179-186) with
composition (C) (:188-195), Question fidelity (A) (:199-208), Non-circular
dependence (:210) and Non-vacuity (:212), collected at (E), FW5:216-224.

**Claim S (sufficiency).** FW5:226 — "The right side is determined by the
specified structures and maps. It contains no predicate that already means
'really explains.'" FW5:228 — "Its strongest claim is that these structural
requirements, correctly interpreted, capture explanatory accounting." The
sufficiency half: satisfying the five conjuncts suffices for the
explanatory-accounting attribution FW5 then makes of \(\mathcal E\), including
its downstream uses — Bearing at (K1), FW5:614-617, and the
\(\operatorname{Account}(c,p_c)\) conjunct of (EK), FW5:831.

FW5 states its own defeater at :1364. **Quoted in full, without ellipsis, because
its four qualifiers do the work (F11):**

> The most important challenge is a fully specified candidate satisfying (E),
> with true target anchoring, the original question preserved, substantive
> contrasts, and no conclusion smuggling, which nevertheless provides no
> explanatory account. That would refute the sufficiency claim.

A sufficiency candidate must therefore survive four separate checks beyond
"(E) is satisfiable": **(q1)** true target anchoring, **(q2)** the original
question preserved, **(q3)** substantive contrasts, **(q4)** no conclusion
smuggling. §5(a)(i) checks Case A-S against each and records which it fails.

**Claim N (necessity).** The same sentence's other half, FW5:1364 — "A genuine
explanation that cannot satisfy the conditions under any interpretation
preserving its actual organization would refute necessity." Restated at
FW5:1502 — "Its strongest unresolved issue is whether the proposed structural
conditions capture all and only the intended explanatory organization."

**What Claim N's failure would and would not touch, corrected (F12).** It
would touch **:228** in the necessity direction and the
\(\operatorname{Account}(c,p_c)\) conjunct's force in **(EK) at :831**. It
would **not** show that the explanation falls outside the base class. FW5:1192
defines \(\mathsf{FW5}\) as "interpretations supplying the data above,
respecting their typing, and satisfying the physical-realization and
reference-coherence conditions", and says it "can describe irrational systems,
false conjectures, obstructed inquiry, missing evidence, and failed attempts".
An interpretation whose \(\mathcal E\) fails (E) is not thereby outside
\(\mathsf{FW5}\); it is a member describing a failed account. **v1's
relinquishment chain through :1192 is withdrawn.**

**Two claims FW5 makes that A001 does NOT challenge, named so they are not
absorbed.**

(i) **The results protected by :1390.** :1390's list is exactly "(M1), (M2),
(I2), (O1), (T2), or the retention fixed-point result", and a counterexample to
one of those while all stated assumptions hold "would expose a mathematical
error" — a different finding. The finite monotone theorem is (M1) at :306 and
(M2) at :315 (:296 is its heading). (I2) is at :429, (O1) at :497, (T2) at
:582, the retention fixed point at :941.

(ii) **Two further proved results, named without :1390's protection (F9).**
Equivariance under genuine recoding (:1202, proof at :1204, scope limit at
:1206) and the projection theorem (:1208-1218, proof at :1220, scope limit at
:1224) are proved results that A001 does not challenge. **They carry no :1390
tag**, and v1's sentence putting them inside :1390's protected list was wrong.

(iii) **The declared-input boundary for normative and physical content**
(:1384-1386, :902-904): a complaint that FW5 does not derive \(\mathcal N\) is
not a counterexample, because FW5 states the dependence rather than concealing
it.

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
| D2 | question \(p=(D,\Sigma,b_0,\kappa,\mathcal C,\mathcal Q,O_p)\); (Q) | :117-123, :125-131 | defined | typed tuple |
| D3 | respect \(\kappa\) | :123 | **undefined** | fixed by an open example list ("production, inferential identification, impossibility, rule-governed status, achievement of an aim, or aesthetic value"); no membership condition, no individuation of two respects |
| D4 | contrast contract \(\mathcal C\) | :123 | **undefined** | "distinctions **material to that question**"; materiality is the load-bearing word and is not defined |
| D5 | the maps \(\pi,\tau,\sigma,\lambda\) with declared domains | :166-170 | defined | declared data; many-to-one permitted for \(\pi\); ":170 Their meanings are held fixed across the comparison" |
| D6 | "the declared abstraction" at which the projected target relation must equal the explanatory component relation | :176 | **restricted, with one undefined input** — *v1's "undefined, a free declaration" is withdrawn (F4, §5(a)(i))* | :176 s1 restricts the anchoring data to "a port translation for each component, **depending only on the ports of its anchored subnetwork and the explicitly declared boundary**"; :176 s5 names the failure mode ("prevents local relation matches from silently losing constraints shared between components"); :174 adds that "derived" "does not authorize an unexplained explanatory arrow". What is left open is only **which changes must be in \(\mathcal C\)**, i.e. D4's materiality and D10's "could matter" |
| D7 | grain \(\ell\) | :154 | **undefined** | "A grain fixes which structural distinctions count as differences for the attribution at issue" — a stipulation; no admissibility condition relative to \(\kappa\) or \(\mathcal C\). Note :154 s3-s4 constrain coarsening ("Coarsening is not automatically an isomorphism"; bundling "can change the answer to a question about individual contribution") but state no test |
| D8 | active commitments vs incidental remarks | :162 | **undefined** | "part of the interpreted claim"; no procedure, and FW5 explicitly forbids an assessor selecting fragments |
| D9 | (F), (C), (A) | :185, :194, :205 | defined | equalities and an indexing condition; (C) is restricted to "every composition **for which a claim is made**" (:188) and (A) "includes the respect \(\kappa\)" (:208) |
| D10 | non-circular dependence: the :210 contrast clause **and :212's third sentence** | :210, **:212 s3** | defined, on D4/D7/D8 | :210 requires "at least one admitted contrast that removes or changes a nonempty block of active organizational commitments … for which the answer profile changes or ceases to be determined in the claimed way". **:212 s3 — "A contrast family containing only notational variants, or one defined to exclude every change that could matter, does not meet non-circular dependence" — is printed under the Non-vacuity heading but its stated predicate is non-circular dependence; it is filed here (F3).** Its inputs (what "could matter") are D4 |
| D11 | non-vacuity | **:212 s1-s2 only** | defined | "The baseline organization has a compatible state or history"; and an impossibility claim "may correctly assert that a specified goal has no compatible realization, but not infer a substantive result merely from an inconsistent baseline". *v1 filed :212 s3 here; that misfiling is corrected (F3)* |
| D12 | boundary \(\beta\), representation \(\operatorname{Rep}_{\beta,\ell}\) | :148-152, :156 | declared primitive | FW5 says so: ":156 The representation relation is an explicit semantic primitive" |
| D13 | structural equivalence at grain, \(d\equiv_\ell c\) | :738-746 | defined, unmapped | ":746 structural at the stated grain, not string equality or similarity"; no record-level test |
| D14 | Bearing (K1): \(\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal E_c,p_\delta)\) | :614-617, gloss at :620 | defined, **mapping unsupported** | identifies criticism-bearing with accounting; the route from an authored criticism to \(\mathcal E_c\) is not stated. **There is no second, non-Account route to Bearing anywhere in the reading edition** (§5(b)) |
| D15 | criticism constituents \(z,\delta,g\), connection | :609 | defined | four-part; ":609 A defect is a specified failure condition on the target or its application" |
| D16 | active route; nonconstant dependence on the represented distinction | :601 | defined, unmapped | requires actual occurrences, ports, component relations; "not inferred from the presence of a similar sentence in a record" |
| D17 | reason-use witness and its three-case contrast contract | :628, :630 | defined, unmapped | a structural map preserving internal role bindings; C001 PLAN §9 records that a transcript supplies none |
| D18 | standing \(\operatorname{Live}_j\), (K2) | :638, :642-651 | defined, unmapped | appraisal-indexed; FW5:640 — prompt appearance is a delivery fact, actual use is "not automatically machine-maintainable" |
| D19 | repair (P) with \(O\), \(P\), \(\operatorname{ProducedBy}\) | :787-800 | defined, unmapped | not challenged here; named because (EK) carries Account |
| D20 | reading Account off an output projection | :1208-1224 | **unavailable by FW5's own theorem** | ":1218 no function of \(P(M)\) alone agrees with the accounting predicate on both models"; ":1222 semantic use inferred from delivery logs"; ":1224 the theorem identifies missing information in a projection" — and see §5(a)(i) on what the theorem does **not** say |
| **D21** | **A001's own `bearing`→\(\kappa\) bridge** | — (not an FW5 dependency) | **A001's declared mapping, criticizable** | none of the ten golden `bearing` fields names a respect in :123's sense; the bridge rule is declared in §3 before the reading, and an adverse cell charges the bridge before it charges anything of FW5's (F25) |

**Note on the realization conditions (F15).** The conditions FW5 defers to its
constructor section are at **:989-991** ("For every attributed use task, there
must be a relation between the physically admitted process and the semantic
organization that preserves the relevant role bindings and their
transformations"; "A realization may be distributed across people, tools,
memory, and artifacts"). :995-1012 is the Marletto/CTK material and is a
different subject. v1's ":987-:1012" is corrected.

**The one published mapping candidate.** The C001 correspondence table
(`experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md`, sha256
`dcaebaf8336c1943700a762b4836679307349d6ff8dfad082e4cd77e23fd7ae7`) is a
proposed, checkable instance of D13 for one criticism document. **Measured:**
it carries **85 units in two arms** — the `fcl` arm (source `mini_fcl`) has 50
(28 `B.*` body units + 22 `K.*` record-field units, over records o1, o2, o3 of
the objection document), the `prose` arm (source `mini_prose`) has 35 (20 `B.*`
+ 15 `C.*`). **Only the fcl arm's 50 units bear on E2** (F23). A001 uses the
table as a *candidate* mapping and tests it; it does not assume it.

---

## 3. Grain, boundary, contrasts — fixed before any evidence

Declared under `docs/SEMANTIC_GUIDE.md` "Declare the interpretation before the
evidence" and FW5:728 ("Fix a system boundary, grain, history, and continuity
criterion before assessing an event").

| item | A001 declaration |
|---|---|
| **unit that counts as a case** | Prose legs: one fully specified \(\mathcal E=(E,p,\pi,\tau,\sigma,\lambda)\) with its target organization and question, authored in this document. Executable leg: one **record carrying a non-empty `bearing` field** **together with one declared target record**, i.e. one row of a published use table. The `type: "objection"` disjunct of v1 is **dropped as a separate criterion** and becomes a **sub-register label** instead, because the two criteria do not pick out the same rows and the pre-registration must match its own definition (F24). Not a document, not a node, not a cell of C001. |
| **grain \(\ell\)** | the FCL-1 record keyed by id, with its `text`, `scope`, `grounds`, `bearing`, `action`, `consequence` fields and its ref arrays retained; ids and prefixes retained. This is C001's own declared grain (C001 PLAN §10) and the use-relation instrument's own subject definition. Chosen before reading; if it is changed later the claim changes with it (**FW5:140** — "What is prohibited is changing it during an assessment without recording the resulting change in what is claimed"; `docs/SEMANTIC_GUIDE.md`, "Changing the question, grain, anchors or protected obligations makes a new claim"). *v1 cited :133, a blank line (F8).* |
| **boundary separating the studied system from its inputs** | The studied system is the **criticism content** and the **target content** as published bytes. Outside it: the model, the endpoint, Mini's graph, the scheduler, the store, the operator-supplied FCL-1 language, the H005 instructions, the decoder, the importer and the use-relation instrument. A001 makes **no attribution to any model or endpoint**, so the usual "model + Mini + configuration" boundary is not invoked and no model-only argument is owed. |
| **respect \(\kappa\), and the bridge that supplies it (D21)** | **Measured:** all ten golden `bearing` fields are consequence-if-true clauses (e.g. row 2, `o2`→`c2`: "Weakens the claim that falling recurrence would confirm c1 and rising recurrence would refute it; the test has lower discriminating power than the account implies"). **None names a respect in :123's sense.** So \(\kappa\) cannot simply be "quoted verbatim from the record" as v1 said. A001 therefore declares, **before the reading**, the bridge rule below, and declares that the bridge is **A001's own criticizable contribution (D21)**, not a reading of FW5. |
| **the bridge rule, first match wins, applied to the `bearing` text alone** | (b1) the text asserts that the target's test, evidence or inference cannot distinguish two or more stated readings, or has less discriminating power than the target claims → \(\kappa=\) **inferential identification** (:123). (b2) the text asserts that the target treats one reading as the frame while at least one rival is equally consistent with the same stated evidence → \(\kappa=\) **inferential identification**. (b3) the text asserts that the target's recommendation, ordering or prescription does work its stated evidence does not carry → \(\kappa=\) **achievement of an aim** (:123), the aim being the one the target's own recommendation states. (b4) the text asserts only that a reader will misread the target → \(\kappa=\) **inferential identification**, and the cell is additionally flagged `bridge-strained`. (b5) otherwise → \(\kappa\) **unresolved**, and the cell is unresolved and is not supplied with a respect. |
| **why a bridge rather than "unresolved by construction"** | The reviewer's alternative — declare the whole leg unresolved by construction — is available and is recorded as such. It is not taken, because it ends the leg without producing anything checkable, whereas a declared, published, pre-registered bridge is a separately identified gap-filling contribution of the kind PURPOSE.md requires ("Proposed gap-filling definitions … are separate criticizable contributions; they must not silently rewrite the source or absorb adverse evidence after the fact"). **Consequence, pre-declared: an adverse cell charges D21 before it charges D14, and charges D14 before it charges Account** (§5(b)). |
| **contrast used** | Account's own contrast requirement, **FW5:210** with **:212 s3** — at least one admitted contrast removing or changing a nonempty block of active organizational commitments of the target, with the answer profile changing or ceasing to be determined; and the family must not consist only of notational variants nor be defined to exclude every change that could matter. **Not** FW5:630's three-case contract. |
| **FW5:630's three-case contract, where it does enter** | only in leg E2, and only as a check on D13 (equivariance of (E) under a genuine recoding, FW5:1202). C001's registers T/E/D/G are reason-use registers; A001 does not fill them, does not reuse their marks, and does not read an Account result off them. |
| **history / continuity** | none claimed. A001 compares contents, not episodes. |
| **normative relation invoked** | none. No merit, adequacy-of-the-model, or progress predicate is applied to any model or output. |
| **enabling contributions** | FW5 itself, the FCL-1 language, the H005/F001 material and instructions, the two published instruments, the C001 recoding table. |

---

## 4. What a counterexample would require FW5 to relinquish

**If Claim S falls** (a fully specified \(\mathcal E\) with all five conjuncts
true at a defensible \(\ell\) and \(\kappa\), meeting :1364's four qualifiers,
which is not an explanatory account of its target): the repair is a sixth
condition, and the only candidates are (a) a further substantive structural
condition, (b) a primitive of the kind banned at :37 (`Because`,
`ExplanatoryWork`), or (c) an admissibility condition on
\(\ell,\kappa,\mathcal C\) that the reading edition does not state.

**The relinquishment is conditional on which repair is taken (F13).**

* Under **(a)**, **:226 survives intact.** :226's own gloss of the right side is
  "Anchoring is a claim about the kind and organization of the target's
  components; fidelity is a collection of mathematical equalities; question
  fidelity is an indexing condition; non-circular dependence is a contrast
  property" — a further substantive structural condition is more of the same
  kind, not a predicate that "already means 'really explains'". What (a) touches
  is **:228's present wording**: the five conditions as stated would no longer
  "capture explanatory accounting" in the sufficiency direction, and :228's own
  sentence "If a genuine explanation requires a distinction no such structure
  can preserve, the proposal must change" would be the operative clause.
* Under **(b)**, :226 falls, and so does the whole no-`Because` programme.
* Under **(c)**, :226 survives as written but becomes uninformative until the
  admissibility condition is supplied; the finding is of the missing-definition
  kind and defers rather than refutes.

Downstream, under (a), (b) or (c) alike, **(K1) at :614-617** loses the
inference from accounting to bearing, and the
\(\operatorname{Account}(c,p_c)\) conjunct of **(EK) at :831** loses its force.
Nothing here requires relinquishing (O), (Q), equivariance (:1202), the
projection theorem (:1208-1218), (M1)/(M2), (I2), (O1), (T2), the retention
fixed point, (CT4) or (RC).

**If Claim N falls**: FW5 must relinquish **:228** in the necessity direction
and the \(\operatorname{Account}(c,p_c)\) conjunct's force in **(EK) at :831**,
and must either widen (E) or concede that explanation has instances the class
cannot represent. It does **not** follow that the explanation is outside
\(\mathsf{FW5}\) (:1192, see §1). FW5:1372 already names the shape — "If they
exclude a genuine inexplicit or distributed understanding, it is too strong."

**What no counterexample here can require (F10).** FW5:1392 — "A physical or
semantic counterexample to an application can defeat that application without
changing the model-class definition." FW5:688 — "The inability to evaluate a
proposition is not a falsifying observation of the proposition." FW5:1404 —
"No experiment established the class's adequacy as a theory of human or
artificial creativity. The validation boundary is mathematical construction
checking, not semantic certification." *v1 cited :1336-1344 for this; that
section concerns one supplied audit of executable spec 0.2 against the packet's
0.1, and :1342 cuts the other way — "its stated immunity of formally backed
conjectures to prose-only attacks cannot be a semantic principle here". The
citation is withdrawn.*

### Three different findings, kept apart

1. **A missing definition** (D3, D4, D7, D8, and the materiality input of D6
   and D10). Shows that (E) is not yet determinate for a given (target,
   question) pair: a claimant can make (E) true or false by a free declaration.
   This **defers** both S and N; it refutes neither, and it must not be
   reported as a counterexample. Its remedy is a separately identified
   gap-filling proposal (§5(c)), which must not be back-fitted to whatever the
   evidence turns out to be.
2. **An unsupported mapping** (D14, D16-D18, D20, D21, and D13 if the C001
   recoding table fails its own content-preservation argument). Shows that a
   bridge from published records to an FW5 relation is unwarranted. It defeats
   the application, not the class (FW5:1392). It is the finding the executable
   leg can actually reach (§5(b)).
3. **An operational failure.** **Measured, restated (F22):** the
   `deepseek-flash` × `fcl` cell of C001 occurrence-01 has **19 of its 20
   coordinates unusable at the 8192 ceiling — 8 PARTIAL at `finish_reason`
   "length" with `completion_tokens` exactly 8192, and 11 FAILED with
   `NO_PUBLIC_CONTENT` carrying no `finish_reason` and no usage at all** —
   `COMPARISON.md` lines 38-59 (table 38-57, "Unresolved in this cell" at 59),
   the terminal reading recorded at
   `experiments/diagnostics/C001-contrast-triple/material-occurrence-02.json`
   line 1519. *v1's "19 of 20 coordinates consumed by an 8192 completion
   ceiling, lines 40-59" was wrong twice: the 11 FAILED rows carry no usage, so
   the ceiling is an inference for them, and lines 40-59 drops
   `original/rep1`-`rep2`.* Shows a resource fact. FW5:688. It supplies no
   evidence for or against S or N, and no cell of that kind may be counted on
   either side.

---

## 5. The challenge as criticizable contributions

### 5(a) Prose leg — two authored cases, and why each fails

**The rule for choosing between permitted outcomes, declared here and applied
below (F18).** For any authored case:

> **(r1)** If FW5 supplies any **stated clause** excluding the case, the case
> **fails**, and the finding is neither finding 1 nor a counterexample. The
> report names the clause at the line.
> **(r2)** If the only reply available to FW5 is a **condition the reading
> edition does not contain**, the finding is **finding 1** (a missing
> definition), and the missing condition is named exactly.
> **(r3)** A **counterexample** requires that no stated clause and no candidate
> gap-filling condition excludes the case, **and** that it meets all four of
> :1364's qualifiers (q1)-(q4).
> No case may be upgraded after the argument is examined. This rule is fixed
> before §5(a)(i) and §5(a)(ii) are read.

#### 5(a)(i) Case A-S (sufficiency) — **FAILS under (r1)**

*The candidate.* FW5's own discriminating pair, introduced at :1222 and checked
by exhaustive enumeration at :1402 ("All four Boolean input assignments were
checked for the parallel and priority constructions. Their endpoint outputs
agree, while the active second route differs when both inputs are on"). Let the
target \(D\) be the **priority** organization, in which route 2 is live only
when route 1 is off; let the candidate explanatory organization \(E\) be the
**parallel** one, with \(\lambda\) anchoring its two routes to the target's two
routes and \(\pi,\tau,\sigma\) the identity on the endpoint ports.

**One respect \(\kappa\) must be fixed and carried through all five conjuncts
and the falsity claim (F1).** There are exactly two candidates, and A001 works
both.

**Horn 1 — \(\kappa\) = production of the endpoint output, grain and declared
abstraction at endpoint level.**

* (A) Question fidelity **holds**: \(\operatorname{Ans}_E\) and
  \(\operatorname{Ans}_p\) are the same function of the four assignments
  (:1402), and :208's "This includes the respect \(\kappa\), not just a matching
  number" is satisfied, because the declared respect asks for the produced
  output value and nothing else.
* (E)'s other conjuncts can be made to hold at that abstraction — but this does
  not matter, because **the attribution is then true**. "\(E\) accounts for the
  target's production of the output", where the declared question's answer
  profile *is* the endpoint output function, is correct. **Nothing false is
  shown.** FW5:236 licenses exactly this: "Explanatory depth is
  question-relative… Equation (E) is not a universal measure of elegance or
  merit."
* Against :1364's qualifiers: (q2) **the original question preserved** is what
  fails if one then complains that \(E\) gets the mechanism wrong — the
  mechanism question is a different question, and switching to it is the
  after-the-fact move (r1)-(r3) forbid.
* **v1's sentence "the attribution … is nevertheless false of the target when
  both inputs are on, and FW5's own theorem at :1208-1218 is the reason it is
  false" is WITHDRAWN.** :1218 says only that "no function of \(P(M)\) alone
  agrees with the accounting predicate on both models" — a claim about a
  projection's information, not about the falsity of an attribution. Worse for
  the case: the theorem's hypotheses are \(M_0\models\phi\) and
  \(M_1\not\models\phi\), i.e. **the theorem presupposes that the accounting
  predicate distinguishes the parallel and priority models.** A-S needs Account
  *not* to distinguish them. FW5's own theorem runs against the case, not for
  it. :1224 confirms the theorem's scope: "The theorem identifies missing
  information in a projection. It does not say that no physical or
  organizational evidence can ever establish the distinction."

**Horn 2 — \(\kappa\) concerns the active route.** This is the horn :1222 itself
pins the construction to: "Parallel and priority wiring provide a concrete
instance **when the projection retains only endpoint values and the question
concerns the active route**" (:1222, emphasis added).

* **(A) Question fidelity fails first, at :208.** With both inputs on,
  \(\operatorname{Ans}_p\) is "route 1 alone is active" and
  \(\operatorname{Ans}_E\) is "routes 1 and 2 are active" (:1402). The answer
  profiles differ, so (A) fails before Anchoring is reached. The case is over
  at :199-208.
* **Anchoring fails as well, on the clause :176 states (F4).** Quoted at the
  line: ":176 More formally, the anchoring data include a port translation for
  each component, **depending only on the ports of its anchored subnetwork and
  the explicitly declared boundary**. The target subnetwork's relation is
  obtained by imposing its component constraints and projecting away its hidden
  ports. **That projected relation must equal the explanatory component
  relation at the declared abstraction.** Port-role translations must agree…
  **Together with (F), which checks the assembled organization, this prevents
  local relation matches from silently losing constraints shared between
  components.**" A-S is a local relation match (endpoint ports, identity
  \(\pi,\tau,\sigma\)) losing a constraint shared between components (route 2's
  gating by route 1). :174 adds that "the word 'derived' does not authorize an
  unexplained explanatory arrow". **The Anchoring claim of v1 is withdrawn.**

**Can any endpoint-level abstraction satisfy Anchoring and non-circular
dependence together? Answered directly, as the revision requires.**

* **Anchoring: no.** The declared abstraction is the abstraction at which a
  *target subnetwork's projected relation* is compared with an *explanatory
  component relation*. Two cases exhaust it. **(α)** The abstraction coarsens
  only the assembled organization's ports, leaving each component's relation
  over its own ports: then route 2's projected target relation retains the
  gating constraint, the parallel route-2 relation does not, and the required
  equality fails. **(β)** The abstraction coarsens each component's relation
  down to the assembled organization's endpoint values: then the anchoring data
  are no longer "a port translation for each component depending **only on the
  ports of its anchored subnetwork** and the explicitly declared boundary",
  because the assembled organization's endpoint values are neither ports of
  route 2's subnetwork nor the declared boundary. :176 s1 excludes (β) as a
  matter of what the anchoring data may depend on. **So no endpoint-level
  abstraction satisfies Anchoring for a two-route organization whose routes are
  the anchored components.** This is a stated restriction, not an undefined
  admissibility condition.
* **Non-circular dependence: yes, separately.** This is where A001 **partly
  dissents from F2**, and records the dissent rather than absorbing it. F2 says
  A-S fails non-circular dependence on :212 s3, "one defined to exclude every
  change that could matter". On a strict reading of *every*, the endpoint-level
  family does **not** meet that description: it excludes the gating change, but
  it still admits deleting the block of both routes, which changes the answer
  profile under either respect. So :212 s3 does not by itself exclude A-S, and
  :210's own requirement ("at least one admitted contrast…") is met. **F2 is
  nevertheless right on its substantive charge**: v1 discharged non-vacuity on
  :212 s1 alone and never addressed :212 s3 at all. The clause is now addressed
  here, filed under D10 where its stated predicate puts it (F3), and answered:
  it does not exclude this case, and **:176 does.**
* **What that shows.** The sufficiency claim **is defended at this locus by
  stated clauses** — :208 on the respect, :176 s1/s3/s5 on the anchoring data —
  and not by an undefined admissibility condition. v1's claim that "FW5's
  available reply … needs an admissibility condition the reading edition does
  not contain" is **withdrawn**. A sufficiency challenge must find a case that
  **meets** :176 and :208 and still fails to explain; A-S does not, and neither
  does any endpoint-level abstraction of FW5's own discriminating pair.

**Case A-S against :1364's four qualifiers, one at a time (F11).** **(q1)
true target anchoring** — **fails** under horn 2, at :176 s1/s3 (above); under
horn 1 the anchoring is true of a question nobody disputes. **(q2) the original
question preserved** — **fails** under horn 1: the case only looks adverse if
the reader switches, after the fact, from the endpoint question to the route
question, which is the move (r1)-(r3) and
`FW5-research-plan-decision.md` ("must not be repaired away by silently
changing the question, grain, boundary or anchors after the failure") both
forbid. **(q3) substantive contrasts** — **survives**, on the strict reading of
:212 s3 argued above; A001 does not claim otherwise, and says so rather than
collecting a failure it cannot support. **(q4) no conclusion smuggling** — not
at issue; the target answer is not installed as a premise. **Two of the four
fail, and one failure is enough.**

**Disposition under (r1): Case A-S fails.** It is not a counterexample and it
is not finding 1. It is recorded as a **second failed sufficiency candidate**,
alongside the skew-matrix one, and its value is negative and bounded: it marks
where the sufficiency attack cannot go.

**The one positive result A-S leaves.** D6 is **narrowed, not deleted**: :176
does tie the declared abstraction to something (the ports of the anchored
subnetwork and the declared boundary), so the abstraction is not a free
declaration. What remains open is only **which changes must be in
\(\mathcal C\)** — :123's "distinctions material to that question" and :212
s3's "could matter" — i.e. D4 and D10's input. That is a smaller and more
defensible finding-1 than v1's, and it is the form in which A001 publishes it.

#### 5(a)(ii) Case B-N (necessity) — **DROPPED**

*The candidate, as staged in v1.* An inexplicit, distributed diagnostic
explanation of the kind FW5 admits at :857-859 ("partial, distributed, or
temporally extended", available "through memory, imagery, action rehearsal, or
interaction with an artifact") and at **:244** ("A thinker need not possess the
maps in explicit notation to instantiate the relevant organization") — *v1
cited :246 for that sentence; :246 is the "previous separation into a
mathematical claim, an application claim, and a relevance claim" paragraph
(F7)* — where the realization has no decomposition into components with stable
footprints, so that several inequivalent anchorings \(\lambda\) are compatible
with it.

**v1 pre-committed: "the contribution has to be the *determinacy* step, and if
the determinacy step fails the case fails."** The determinacy step fails.

* **:188 does not demand determinacy.** Its words are "The translation
  preserves identities and **every composition for which a claim is made**" — a
  restriction on which compositions are checked, not a demand that a
  realization have a determinate decomposition.
* **:174 does not demand it either.** "**Every active** explanatory component
  has a stated target interpretation under \(\lambda\)" — a condition on the
  components of a given \(\mathcal E\), quantified over the active ones, not a
  uniqueness claim about the realization.
* **:170 and :244 settle it.** The maps are declared data whose "meanings are
  held fixed across the comparison" (:170), and "The maps can exist before
  anyone discovers them" (:244). Several compatible \(\lambda\) therefore do not
  make (E) indeterminate: **each \(\lambda\) yields a different \(\mathcal E\),
  and Account is a predicate of \(\mathcal E\)**, not of the realization.
* **The disjunction v1 offered is unavailable (F6).** v1 said that if (E) is
  true under one \(\lambda\) and false under another, "either necessity fails …
  or FW5 owes a determinacy condition". :1364's necessity defeater is "A genuine
  explanation that cannot satisfy the conditions **under any interpretation**
  preserving its actual organization". (E) coming out true under one \(\lambda\)
  **satisfies** necessity. The "either necessity fails" disjunct is deleted.
  `FW5-research-plan-decision.md` says the same: "Failure of one selected
  encoding or grain is not that necessity result."

**Does anything remain that :1372 does not already say? No.** :1372 — "If they
exclude a genuine inexplicit or distributed understanding, it is too strong" —
already states the whole of B-N's residue, and :857-859 and :989-991 already
grant that the realization may be "partial, distributed, or temporally
extended" and "distributed across people, tools, memory, and artifacts". **B-N
is dropped.** It is not carried as a "possible counterexample" and not
reclassified as finding 1, because the missing condition it named (determinacy)
is not owed.

**Branch, recorded (F14).** :1372 sits under "Representation and apparent
reason use", not under :1362's "A structural account that still does not
explain", and `FW5-research-plan-decision.md` files it separately: "The source
also names representation/integration challenges (decorative reasons wrongly
admitted or genuine inexplicit understanding excluded) … These remain distinct
attack branches." So B-N was on the representation/integration branch, filed in
v1 under Account necessity. Dropping it removes the misfiling; the branch stays
open and A001 does not work it.

**What a real necessity case would need, named so the gap is visible.** An
explanation whose **actual organization is independently attested** — not
stipulated in prose by the challenger — for which no \(\lambda\) over that
attested organization satisfies (E). Prose alone cannot supply the attestation,
which is why this is the same gap the skew-matrix review left open. A001 does
not close it.

#### 5(a)(iii) What the prose leg leaves

Neither case is an independently sourced interpretive technical document; that
gap, named at the end of `docs/reviews/FW5-account-skew-matrix-challenge.md`,
stays open and A001 does not close it. Two recorded failures are the prose
leg's whole yield, plus the narrowing of D6.

### 5(b) Executable leg — a (K1)-mapping test over published records

No provider call. No new instrument. No cell of any published table is filled
by A001; A001 writes its own worksheet, whose rows cite published row ids.

**The route problem, stated plainly (F16).** (K1) at FW5:614-617 reads
\(\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal E_c,
p_\delta)\). **Bearing is defined as Account.** v1's sufficiency condition —
"the criticism does not bear while (E) holds" — is therefore not a statement
about Account at all; it is the denial of a biconditional. **Is there a second
route to Bearing in the reading edition? There is not.** :620 adds only a
side condition on the defect ("The alleged defect must concern the stated
target and respect"); :622 says a criticism occurrence can exist when (K1) is
false, which concerns occurrences, not bearing; :609 supplies the constituents
\(z,\delta,g\) and the connection but defines no bearing predicate over them.
So the only available left-hand side is a **reader's independent judgement that
the alleged defect does or does not obtain of the quoted target passage** — and
that judgement is **A001's own declared observable, not an FW5 relation.**

**The leg is therefore restated as a (K1)-mapping test.** It asks: *do the
repository's published criticism records supply what (K1)'s right-hand side
requires, and where a reconstruction is possible, do the two sides agree?* Its
maximum reach is a **finding 2** against D14 and against A001's own bridges
(D21 and the δ-slot reconstruction). **It cannot reach an Account verdict, and
no row of its worksheet may carry one.**

**Modality, corrected (F17).** "Satisfiable" is withdrawn. :1364 requires "a
fully specified candidate satisfying (E)" and :170 requires declared domains
"held fixed across the comparison"; satisfiability would let a reader choose a
favourable interpretation after seeing the cell. **Each worksheet row must
exhibit one \(\mathcal E_c\) with \(\pi,\tau,\sigma,\lambda\) and the question
tuple \(p_\delta\) written into the row**, before any conjunct is marked. (For
the dropped necessity direction the "under any interpretation" quantifier would
have been the right modality; there is no necessity direction left in this leg.)

**Pre-declared outcome classes. First that applies wins; declared here, before
any cell is read.**

| class | condition | what it records | charge |
|---|---|---|---|
| **X0 NOT-RECONSTRUCTIBLE** | the record does not supply a datum (K1)'s right side requires: no separately addressable \(\delta\) (FCL-1 has no \(\delta\) slot — review P6(i)); or no target record id (e.g. F001 occ-07 row 1, a `bare_label_ref` resolving only to the owning artifact); or the bridge returns (b5) | **finding 2 at D14**, naming which of \(E,p_\delta=(D,\Sigma,b_0,\kappa,\mathcal C,\mathcal Q,O_p),\pi,\tau,\sigma,\lambda\) is absent | D14 |
| **X1 AGREE-POSITIVE** | \(\mathcal E_c\) exhibited, (E) holds on it, and the defect obtains of the quoted target passage | one supported instance of the (K1) mapping | none |
| **X2 DISAGREE-SUFFICIENCY** | \(\mathcal E_c\) exhibited, (E) holds, and the defect demonstrably does not obtain of the quoted target passage | **a counterexample to (K1)∧(E)**, never to Account alone | by the charge rule below |
| **X3 DISAGREE-NECESSITY** | the defect demonstrably obtains, and the exhibited \(\mathcal E_c\) fails (E) | **a counterexample to (K1)∧(E)**, never to Account alone | by the charge rule below |
| **X4 UNRESOLVED** | two readers disagree; or the cell is in E3; or \(\kappa\) is unresolved at (b5) | unresolved, recorded with the disagreement, never averaged (FW5:634) | none |
| **X5 NO FINDING** | \(\mathcal E_c\) exhibited and the two sides agree, but only because the reader supplied a free declaration at D3, D4, D7, D8 or D10's materiality input | a **finding-1 exhibit**: the declaration that had to be supplied is quoted | none against FW5's mapping |

X5 and X4 give the residual disposition v1 lacked (F20): **every cell now
lands in exactly one of X0-X5, and "no finding" is a permitted worksheet
value.** The 1-vs-2 rule for a failed reconstruction is: **a missing FW5
primitive → finding 1; a missing route from a published record to an FW5
relation → finding 2.**

**The charge rule for X2 and X3, pre-declared (F16, F18).**

> An X2 or X3 cell charges the **conjunction (K1)∧(E)**. It is charged to
> **D21** (A001's bridge) whenever the cell's \(\kappa\) came from bridge rule
> (b4) or was contested by either reader. Otherwise it is charged to **D14**
> (the K1 mapping) whenever any part of \(\mathcal E_c\) — \(\delta\),
> \(\kappa\), \(\mathcal C\), or the anchoring \(\lambda\) — was fixed by an
> A001 reconstruction rather than by a field the record itself supplies. It is
> charged to **Account alone** only if \(\mathcal E_c\) is supplied in full by
> the record's own fields under no A001 bridge and both readers agree.
> **A001 pre-declares that no published cell is expected to meet that last
> condition**, because FCL-1 supplies no \(\delta\) slot and no \(\kappa\) in
> :123's sense. **If some cell nevertheless meets it, the report must quote the
> record's fields that supply each component of \(\mathcal E_c\) before the
> charge is written, and the charge is still to (K1)∧(E), not to Account.**
> No upgrade to an Account verdict is available after the fact, under any
> reading.

**Cells — the revised pre-registration (33 cells).** Rendered as data in
`CELLS-v2.md`. Pins unchanged (all five re-hashed by the review):
`use-table-golden/use_table.json`
`875d674f85f95f09eb1be1354c194f8a79c04298a0556033df52781bef8c723a`;
`use-table-full/use_table.json`
`39981b3c1923472243d89c7c78e0e0ded99bc6a7d9eef451fa46e798caca0a4f`;
C001 `occurrence-01/comparison.json`
`00452db2586b5f33e3eed58c8a7d01efe6da9d6616ce3423fb76d8795af9d31d`;
`occurrence-02/comparison.json`
`4e7ea3894cfe125ba2507dd761f30d13b5226818fe77f9a91665d05c67bc109b`;
`RECODING_TABLE.md`
`dcaebaf8336c1943700a762b4836679307349d6ff8dfad082e4cd77e23fd7ae7`.

*Sub-register A — objection-typed bearing cells (32).* H005 occurrence-01
snapshot `use-table-golden` rows 0, 1, 2, 3, 4, 10, 11, 13, 16, 17 (10, the
identical rows in `use-table-full`); F001 occurrence-01 rows 0-8 and 19-22
(13), occurrence-05 rows 3-10 (8), occurrence-07 row 1 (1). Occurrences 02, 03,
04, 06 and 08 contribute **zero** rows; that is a fact about those documents'
authored refs, not about their authors, and it is recorded as a cell count of
zero, never as a negative finding.

*Sub-register B — bearing cells whose referring record is not typed
`objection` (1), added with its reason (F24, P7).* F001 occurrence-01 **row
12**, `carry#r2` → `response#m2`, `type: "claim"`, `bearing` = "narrows the
commitment to a cost rule with an explicit scope, rather than a trigger
condition", whose `text` alleges a defect of the prior m2 ("was not licensed by
the prior body"). **Reason for the addition:** §3's unit definition is a
non-empty `bearing` field, and this row has one; v1's list was built on the
`type` field instead, so the pre-registration did not match its own definition.
The v1 list of 32 is retained in `STAGING.md` and in `CELLS-v2.md`. **This cell
is itself a datum for the leg**: the FCL-1 `type` field does not track :609's
criticism constituents.

*Declared-use rows, a separate register (12 rows, `use-table-golden` rows 5-9,
12, 14, 15, 18-21).* Carried by `claim`, `use` and `problem` records with no
`bearing`. Not cells; FW5:640 makes a declared field a delivery fact. They are
read only to record what the language declared, and they can never supply a
counterexample to anything.

*E2 — equivariance check, with its reachability stated (F23).* The C001
ORIGINAL objection block against the RECODING block, **unit by unit over the
fcl arm's 50 units** (28 `B.*` body + 22 `K.*` record-field), not over all 85 —
the other 35 are the `mini_prose` arm and bear on no cell here. **Measured:
E2 can reach at most golden rows 0, 1, 2, 3, 4** — five cells — because the
recoding table's fcl arm covers records o1, o2, o3 of
`daily/mini_fcl/cycle01/objection`, while golden rows 10, 11, 13 refer from the
`response` node (k3, k7) and rows 16, 17 from the `carry` node (n3), which the
table does not cover. No F001 cell is reachable by E2 at all.

*E2's provenance, restated (F26).* The ORIGINAL block is the H005 objection
document "exactly as the H005 `response` node saw it: the same `body` and
`commitments` bytes, projected by the same `project()` with view `both`"
(C001 PLAN:184-188); `prepare` refuses unless the case bytes equal the
occurrence artifact bytes (`ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES`). It is
**identity of the projection**, not of the artifact file; v1's "byte-identical
to … objection.json" is corrected.

*E3 — non-evaluable cells, declared in advance and excluded from every side:*
C001 occurrence-01 `deepseek-flash` × `fcl`, 19 of 20 coordinates as restated in
§4 finding 3; the single PARTIAL at `ollama-glm-5.3` × `fcl` CONTROL rep2; the
12 nodes whose commitment surface was not read in `use-table-full`
(`nodes_not_read`, 10 `prose_not_parsed` plus 2 `unavailable_decode_failure`);
and the 7, 8, 6, 5, 6, 9, 6, 7 `nodes_not_read` of the eight F001 use tables.

**An equivariance failure (E2).** A cell whose (E) assessment differs between
the ORIGINAL and RECODING codings. This is **not** a counterexample to S or N.
It is either finding 2 against the C001 table's content-preservation argument,
or a challenge to FW5:1202's applicability at this grain, and the report states
which and why.

**What would NOT constitute a finding against FW5, pre-committed.**

1. A record whose `bearing` field is empty, or whose defect \(\delta\) is not
   separately addressable because FCL-1 has no \(\delta\) slot (review P6(i)).
   That cell is **X0** or **X4** and stays there.
2. A bare id token shared between two documents; the same ambiguity C001's `E`
   register refuses to resolve.
3. A cell whose delivery is PARTIAL, FAILED, OPAQUE or undecoded (E3).
4. A lexical-overlap passage from the use table. The instrument's own banner:
   "A lexical overlap is not evidence of use."
5. Any difference between endpoints or families. A001 issues no cross-family
   comparison and none may be read off its worksheet (FW5:849, :851).
6. **A count of cells, of any kind, on any side (F21).** Rewritten: **a single
   exhibited instance, with both passages quoted, defeats a universal claim in
   the worksheet's own scope; no count adjudicates anything.** FW5:851's own
   list is "(G), (P), or (EK)" — "No quantity of endorsements, surviving tests,
   repeated observations, or partitioned features enters (G), (P), or (EK) as
   an automatic warrant" — and **Account is not in it**; the link from (EK) to
   Account is the conjunct at :831. v1's "Counts may defeat a claim of
   universality" was wrong: a count does not defeat a universal claim, one
   exhibited instance does.
7. A finding about C001's four registers. A001 does not fill or read them.

**Reading discipline.** Two readers per cell; where they disagree the cell is
`unresolved` and the disagreement is recorded, never averaged (FW5:634; C001
PLAN §8a:743-745). The worksheet's assessment columns are rendered empty by the
staging and are filled only by the reading step.

### 5(c) P3-P8, re-stated as separately identified gap-filling contributions

Source for P3-P7: `docs/reviews/fw5-vs-harness-spec-2026-09-14.md` §5. **P8 is
new in this revision and is A001's own** (F25). Restated under one
governing rule, verbatim from PURPOSE.md: "Proposed gap-filling definitions,
interpretations and mechanisms are separate criticizable contributions; they
must not silently rewrite the source or absorb adverse evidence after the
fact." Operationally, for each: it is published as its own document with its own
identity; it may not edit FW5 or any frozen PLAN; and its acceptance condition
is declared **before** A001's reading.

| id | gap it fills | which A001 dependency | rule of engagement | offline today |
|---|---|---|---|---|
| **P3** criticism-ablation arm for F001 occurrence-02 | discharges `ProducedBy` (FW5:800), not Account | D19 | needs live calls; **out of A001's scope entirely**, named so it is not smuggled in as Account evidence | no |
| **P4** loss ledger (O, P pinned before the later cycle) | (P) at FW5:787-802 | D19 | must be pinned by sha256 *before* dispatch; a dry run over an existing pair is labelled as violating its own pre-declaration and establishes nothing | dry run only |
| **P5** custody and grain preconditions | D7, D13 | grain and partition-invariance preconditions on A001's own instrument; if P5 shows the §3 grain is not partition-invariant, A001's cell readings are **preconditioned**, not rescued | yes |
| **P6** FCL-1's fields against FW5:609/:622 | D14, D15 | supplies the \(\delta\)-slot diagnosis that decides how many cells are X0; it is a **language-adequacy** reading of one cycle, never an Account result | yes |
| **P7** pre-registered reading set | the observer, not the subject | all | A001's cell list **is** P7 applied to this stage: it is frozen in `CELLS-v2.md`, and the one addition since v1 is recorded with its reason with the v1 list retained | yes |
| **P8 (new)** the `bearing`→\(\kappa\) bridge | D21 | declared in §3 before the reading; an adverse cell charges it before it charges D14; it is published as its own contribution and may be rejected without rejecting anything of FW5's | yes |

P3 and P4 are named and deferred. P5, P6, P7 and P8 are what A001 carries
offline.

---

## 6. Claim ceiling

*Unchanged from v1 except where a citation was wrong; the review verified that
no sentence of v1 exceeded it, and the revision adds to it rather than
relaxing it.*

* Nothing about creativity across all tasks, or about any model's repertoire.
  FW5:1256-1260; PURPOSE.md.
* No refutation of FW5 or ECS from an implementation failure, a ceiling, a
  decoder refusal or an unread surface. **FW5:688; FW5:1392; FW5:1404**;
  PURPOSE.md. *(v1 cited :1336-1344 here; withdrawn, see §4.)*
* A single failed candidate does not confirm FW5 — the precedent is
  `docs/reviews/FW5-account-skew-matrix-challenge.md`, whose own result is
  "this rejects one attempted witness; it neither confirms FW5 nor settles
  other sufficiency and necessity attacks." **A001 now contributes a second
  failed candidate, and the same sentence governs it.**
* One reading of one cycle's records over 33 cells cannot decide the
  constitutive conjecture. FW5:1368 — "These challenges concern the
  constitutive conjecture, not a missing proof of a theorem."
* A001 establishes no Origin (G), no Repair (P), no CreateEK, no reason-use
  witness, no standing, no recursive capacity.
* A001 issues no judgement about whether any H005 or F001 objection is a good
  objection. FW5:630 — "Understanding and using an invalid objection does not
  make it valid."
* A001 says nothing about ECS 2.0's graded accounting or intrinsic variation
  family; those are separately identified successor hypotheses.
* **New: no cell of the executable leg can charge Account** (§5(b) charge
  rule). Its maximum reach is (K1)∧(E), D14 and D21.
* **New: A001 offers no counterexample to sufficiency and none to necessity.**
  It records two failed candidates and the reasons they failed.
* The independently sourced interpretive technical case the skew-matrix review
  says is still owed remains owed.

---

## 7. File layout for publication, and why

**Choice: `docs/reviews/` for the documents, `experiments/diagnostics/` for the
executable leg.** Reason, from the repository's own conventions: there is no
`docs/challenges/` directory, and the single existing Account challenge —
`docs/reviews/FW5-account-skew-matrix-challenge.md` — already sits in
`docs/reviews/` with its offline check under
`experiments/diagnostics/fw5-account-skew-matrix/`. `experiments/analyses/` is
reserved in practice for instrument outputs regenerated over frozen occurrences
(H005 snapshot, F001); A001's executable leg is a pre-registered reading with a
frozen cell list and pre-declared outcome classes, which is what
`experiments/diagnostics/` holds.

```
docs/reviews/A001-account-challenge-2026-09-14.md
    §0 relation to the skew-matrix challenge and the authority for each leg;
    §1 claims with FW5 lines; §2 dependency table; §3 grain/boundary/contrast
    and the bearing→κ bridge; §4 relinquishment + the three findings;
    §5(a) the two failed prose cases and the rule that disposes of them;
    §6 claim ceiling. Receipt paragraph at the head.
docs/reviews/A001-gap-filling-proposals-2026-09-14.md
    P3-P8 as separate criticizable contributions, each with its acceptance
    condition declared before the reading (§5(c)).
experiments/diagnostics/A001-account-challenge/PLAN.md
    Pre-registration of the executable leg: the (K1)-mapping route and why no
    other route to Bearing exists, the frozen cell list, the six outcome
    classes, the charge rule, the unresolved rules, the two-reader rule, the
    claim ceiling, 0 planned provider calls.
experiments/diagnostics/A001-account-challenge/material.json
    source pins (FW5, both use_table.json, both comparison.json,
    RECODING_TABLE.md, both C001 materials) + the frozen cell list as data.
experiments/diagnostics/A001-account-challenge/CELLS.md
    the 33 cells in two sub-registers, the 12 declared-use rows, the five
    E2-reachable cells and the E3 exclusions, rendered from material.json.
experiments/diagnostics/A001-account-challenge/WORKSHEET.md
    one row per cell, with columns for the exhibited π, τ, σ, λ and p_δ, the
    outcome class, the charge, and the two readers; all assessment columns
    rendered EMPTY and filled only by the reading step.
docs/DECISION_LEDGER.md            one appended receipt (below)
docs/STATUS.md                     one row: A001 staged, reading not started
```

No file under `experiments/diagnostics/C001-contrast-triple/`,
`experiments/diagnostics/H005-open-prose-commitments/`,
`experiments/diagnostics/F001-fork5-multifamily/` or `experiments/analyses/` is
written, moved or touched. **Measured, verified mechanically by the review:**
no `runtime_files` map in any `experiments/**/*.json` holds a path under
`experiments/` or `docs/`, and `campaign.source_identity()` hashes
`src/**/*.{py,json}` + `pyproject.toml` only, so A001 adds no identity any
frozen plan depends on.

### Receipt paragraph, corrected to house style (F27)

**Measured by the review across the 97 `REC-20260914` entries that existed at
its time:** `Choice:` 94, `Why:` 85 (`Reason:` 9), `Contribution:` 89 (never
"Contribution to the end goal"), closing
`Prior verified commit/tree: <commit> / <tree>` 21, and the opening timestamp
carries the full date. (`REC-20260914-Y` has been appended since, so the
denominator has moved; the conventions have not, and each is re-checked at the
moment of the append rather than carried from here.) v1's draft used `Reason:`, `Contribution to
the end goal:`, an `HH:MM UTC` stamp and no commit/tree tail; all four are
fixed below. **The letter is not fixed in staging**: `REC-20260914-X` and
`REC-20260914-Y` are both taken as of this revision, so the letter is the next
free one **determined at the moment of the append**, exactly as REC-20260914-Y
itself records doing.

> REC-YYYYMMDD-\<next free letter\> opened at YYYY-MM-DD HH:MM UTC: Stage A001,
> an independent Account sufficiency-and-necessity challenge to the designated
> FW5 reading edition (sha256 `8105925b…e33ee63a`), under PURPOSE.md ("In
> parallel, an independent Account sufficiency or necessity challenge tests FW5
> itself"); the prose leg additionally under the "Testing FW5 itself" row of
> `docs/reviews/FW5-research-plan-decision.md`, which is still
> `Status: proposed, awaiting the user's approval` and is cited as intent, not
> approval. **A001 OFFERS NO COUNTEREXAMPLE.** Choice: publish
> `docs/reviews/A001-account-challenge-2026-09-14.md` (the two named claims
> with their FW5 lines, the dependency table marking each primitive defined /
> undefined / defined-but-unmapped, the grain, boundary, contrast and
> `bearing`→κ bridge declared before any evidence, the conditional
> relinquishment statement, and **two authored prose cases recorded as
> failures with the FW5 lines that exclude them**),
> `docs/reviews/A001-gap-filling-proposals-2026-09-14.md` (P3-P8 as separately
> identified contributions with acceptance conditions declared before the
> reading), and `experiments/diagnostics/A001-account-challenge/` (PLAN.md,
> material.json, CELLS.md and an empty WORKSHEET.md) — the executable leg over
> **existing published records only**, restated as a **(K1)-mapping test**: 33
> bearing cells in two sub-registers drawn from the H005 occurrence-01 snapshot
> use tables and the eight F001 use tables, six pre-declared outcome classes
> with a pre-declared charge rule that **forbids any cell from charging Account
> alone**, 12 declared-use rows kept in a separate register, five
> E2-reachable cells over the C001 correspondence table's 50 fcl units, and a
> declared exclusion list of non-evaluable cells. Why: the source's sufficiency
> and necessity claims are the place FW5 itself says to attack it (FW5:1362-1364,
> :1502), and the repository has never tested them against its own published
> records; this stage reports that the two authored attacks fail on stated
> clauses — Case A-S at FW5:176 and :208, Case B-N at :188, :174, :170 and :244
> — and that the executable leg can reach the (K1) mapping and nothing beyond
> it, because FW5:614-617 defines bearing as accounting and the reading edition
> supplies no second route. Contribution: a separately identified test of the
> semantic source with its dependencies named before the evidence, which
> returns two recorded failures and one reachable mapping test rather than a
> counterexample it cannot support; a missing definition, an unsupported
> mapping and an operational failure are recorded as three different findings
> and never as one. State: PENDING — **zero provider calls planned and zero
> made**; no cell of any published table is filled by this stage and every
> assessment column of WORKSHEET.md is published empty; the reading step is a
> separate receipt. Evidence: pins recorded in `material.json`; nothing under
> `experiments/diagnostics/C001-*`, `H005-*`, `F001-*` or
> `experiments/analyses/` written or touched. Prior verified commit/tree:
> \<the last verified published commit\> / \<its tree\>, read at the moment of
> the append.

### What needs a live call

**Nothing.** Every leg is offline: the prose cases are authored, the executable
leg reads published bytes, and the equivariance check reads a published table.
The two-reader rule of §5(b) is **not** a live provider call and does **not**
go to a human as a blocking dependency: it routes to the automated loop's
reader roles — the same delegated-reader/refuter arrangement recorded in the
provenance paragraph of `docs/reviews/fw5-vs-harness-spec-2026-09-14.md` — with
every FW5 line and every record path re-read at the line. P3 and P4 would need
live calls; both are deferred out of A001 and neither may be reported as
Account evidence.

---

## 8. Concerns carried into the reading step

1. **The leg reaches (K1) and stops there.** This is now stated in the route
   itself rather than noted as a risk. The worksheet forces a charge to D21,
   D14 or (K1)∧(E), and offers no Account cell at all.
2. **The FCL-1 records were not authored as \(\mathcal E\).** They were
   authored as criticisms in a language with `target`, `grounds` and `bearing`
   but no \(\delta\) slot (review P6(i)). Reconstructing
   \(\mathcal E_c=(E,p_\delta,\pi,\tau,\sigma,\lambda)\) from such a record is
   itself an interpretation; X0 and X5 are where that lands, and neither is a
   finding against Account.
3. **The bridge (D21) is the leg's softest joint.** If the bridge rule is
   wrong, the respects are wrong, and every downstream mark is wrong. It is
   published as its own contribution (P8) so that it can be rejected on its own.
4. **The grain is C001's, not A001's.** Adopting the record-keyed grain keeps
   A001 comparable with the published material but inherits P5's open
   partition-invariance question. If P5 later shows the reading does not survive
   re-partition, A001's cells are preconditioned, not rescued.
5. **Cell supply is thin and uneven.** 10 cells in H005 golden; 23 across F001,
   of which 14 come from one occurrence and four occurrences supply none. Only
   five cells are E2-reachable. No universality claim of any kind may be built
   on that distribution, and the zero-row occurrences must be reported as zero
   rows, not as silence.
6. **Two published Account challenges will then exist, and both report a failed
   candidate.** §0 states the relation. A001 must not be read as the
   skew-matrix review's successor or as an attempt to overturn it.
7. **The honest A001 is smaller than v1's.** Whoever reads this next should
   check whether it has been quietly re-inflated: any sentence that offers a
   candidate counterexample, upgrades an outcome class after a reading, or lets
   a cell charge Account is a regression against this document.
