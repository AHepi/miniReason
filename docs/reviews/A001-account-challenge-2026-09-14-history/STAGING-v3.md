# A001 — Account sufficiency / necessity challenge: staging, revision 3

Supersedes `STAGING-v2.md`. `STAGING.md` (v1), `STAGING-v2.md`, `CELLS-v2.md`,
`REVIEW.md` and `REVIEW-2.md` are retained unedited beside it, so every step is
diffable. `CHANGES.md` maps F1-F29; `CHANGES-v3.md` maps F30-F50 to fixed /
withdrawn / declined-with-reason. `CELLS-v3.md` carries the revised
pre-registered cell list **and the frozen per-cell bridge-branch assignment**.

Staging only. Nothing here is published, no cell is filled, no reading is
offered, and no provider call was made or is planned. Sentences are marked
**Measured** (readable off a named file at a named line) or **Interpretation**
(a reading that could be wrong). Every claim traces to an FW5 line of the
designated reading edition, sha256
`8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a`
(1,502 lines, re-verified at this revision), or to a published record path.

**What revision 3 does.** Round 2 returned five blockers. Four of them say that
v2 claimed more than it had: it enumerated two cases where there are three
(F30), asserted a universal over abstractions that a three-line construction
refutes (F31), declared outcome classes exhaustive when two outcomes were
homeless (F32), and wrote a charge rule with a branch that its own closing
sentence denies (F33), plus a necessity class inside a leg with no necessity
direction (F34). **Every one is fixed by deletion or by making a rule stricter.
Revision 3 is smaller than revision 2.** Its one published positive result of
v2 — the D6 narrowing — is **withdrawn as a deflation**, and D6 returns to what
v1 said.

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

**Authority, and the deliverable A001 does not deliver (F50). (Measured.)** The
two prose legs are written against the "Testing FW5 itself" row of
`docs/reviews/FW5-research-plan-decision.md`'s "Proposed work" table, which asks
for "an independent challenge to Account sufficiency or necessity in a demanding
mathematical, non-causal or interpretive technical case" and adds "Mini
performance, checker acceptance and model agreement cannot replace the
independent explanation argument". **That row's stated deliverable is "A
candidate counterexample and the clause or constitutive claim that would have
to change." A001 does not meet it.** It produces no candidate counterexample of
either kind (§5(a)), so the row's deliverable remains **owed**, and the prose
legs are published as *work against* that row rather than as its discharge. The
**executable leg does not implement that row at all**: it reads Mini's own FCL-1
records, which are neither one of the three named case types nor independently
sourced. It is carried instead under PURPOSE.md's "In parallel, an independent
Account sufficiency or necessity challenge tests FW5 itself" and under P5, P6,
P7 and P8. That decision note still reads
`Status: proposed, awaiting the user's approval`, so **PURPOSE.md carries the
authority for this stage and the decision note is cited as a statement of
intent, not as an approval.**

**Result of this revision, stated first.** A001 offers no candidate
counterexample and no positive result about FW5's stated clauses. It offers
four things:

1. a **dependency table** over (E)'s primitives (§2), in which **D6 is
   undefined — the declared abstraction is a free declaration** (restored from
   v1; v2's narrowing is withdrawn, F30);
2. the **recorded reasons two authored prose cases fail** — Case A-S at
   **FW5:208**, Case B-N at **FW5:1372** with :188, :174, :170, :244 (§5(a));
3. a pre-registered **(K1)-mapping test** over 33 published cells with
   **exhaustive outcome classes** and a **decision-table charge rule under
   which no row names Account** (§5(b));
4. a declared **`bearing`→κ bridge (D21)** with its **coverage measured, its
   dependence on the cells disclosed, and its per-cell branch assignment frozen
   in advance** (§3, `CELLS-v3.md`).

Under PURPOSE.md — "A missing definition, an unsupported mapping and an
operational failure are different findings" — that is a legitimate result and is
published as such.

---

## 1. The particular semantic claims under challenge

The predicate. FW5:172 — "The following conditions define
\(\operatorname{Account}(\mathcal E)\)" — over the structural account
\(\mathcal E=(E,p,\pi,\tau,\sigma,\lambda)\) (tuple at **:167**, maps at
**:170**), with the five conjuncts Anchoring (:174-176), Structural fidelity
(F) (tag at :185) with composition (C) (tag at :194, restriction at :188),
Question fidelity (A) (tag at :205, with :208), Non-circular dependence (:210)
and Non-vacuity (:212), collected at (E), **tag at :223**.

**Claim S (sufficiency).** FW5:226 — "The right side is determined by the
specified structures and maps. It contains no predicate that already means
'really explains.'" FW5:228 — "Its strongest claim is that these structural
requirements, correctly interpreted, capture explanatory accounting." The
sufficiency half: satisfying the five conjuncts suffices for the
explanatory-accounting attribution FW5 then makes of \(\mathcal E\), including
its downstream uses — Bearing at (K1), **tagged at :617** (display :613-618),
and the \(\operatorname{Account}(c,p_c)\) conjunct of (EK), FW5:831.

FW5 states its own defeater at :1364. **Quoted in full, without ellipsis, because
its four qualifiers do the work (F11):**

> The most important challenge is a fully specified candidate satisfying (E),
> with true target anchoring, the original question preserved, substantive
> contrasts, and no conclusion smuggling, which nevertheless provides no
> explanatory account. That would refute the sufficiency claim.

A sufficiency candidate must therefore survive four separate checks beyond
"(E) is satisfiable": **(q1)** true target anchoring, **(q2)** the original
question preserved, **(q3)** substantive contrasts, **(q4)** no conclusion
smuggling. **Note the antecedent:** the four qualifiers govern "a fully
specified candidate **satisfying (E)**". A candidate that fails a conjunct of
(E) never reaches them. §5(a)(i) applies this to Case A-S horn by horn.

**Claim N (necessity).** The same sentence's other half, FW5:1364 — "A genuine
explanation that cannot satisfy the conditions under any interpretation
preserving its actual organization would refute necessity." Restated at
FW5:1502 — "Its strongest unresolved issue is whether the proposed structural
conditions capture all and only the intended explanatory organization."

**What Claim N's failure would and would not touch (F12).** It would touch
**:228** in the necessity direction and the
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
:582. **The retention fixed-point result is at :947 and :950-:952 (F45)**: :941
is the section heading "## The retention fixed point"; **(CT2)** is the tag at
**:947** (display :945-948); the monotonicity and greatest-fixed-point
statement is at **:950** and its proof at **:952**. *v2 cited :941, a heading —
the defect F15 fixed elsewhere.*

(ii) **Two further proved results, named without :1390's protection (F9).**
Equivariance under genuine recoding (**statement :1202**, proof :1204, scope
limit :1206) and the projection theorem (**heading :1208; statement :1210-1218**,
proof :1220, instance :1222, scope limit :1224) are proved results that A001
does not challenge. **They carry no :1390 tag**, and v1's sentence putting them
inside :1390's protected list was wrong. *v2 cited the projection theorem as
":1208-1218", which begins at the heading; the statement begins at :1210 (F48).*

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

**Pointer discipline (F48).** Where a cited datum sits inside a display, the
row cites the **content** line, not the `\[` delimiter or the section heading.
Corrected at this revision: D1's `:85` (a `\[`; the tuple is at **:86**, display
:85-87) and (O) (lead-in :99; **tag at :106**, display :101-107); D2's
`:117-123` (lead-in :117; **tuple at :120**; (Q) **tagged at :131**); D5's
`:166-170` (**tuple at :167**; maps at :170); D14's `:614-617` (**tag at :617**,
display :613-618); D20's `:1208-1224` (**statement :1210-1218**).

| # | dependency | FW5 line | status | why |
|---|---|---|---|---|
| D1 | organization \(D=(V,(X_v),J,B,A,L,\mathrm{role})\); solutions (O) | :86; (O) tag :106 | defined | typed tuple; (O) is set equality |
| D2 | question \(p=(D,\Sigma,b_0,\kappa,\mathcal C,\mathcal Q,O_p)\); (Q) | :120, :123, :125; (Q) tag :131 | defined | typed tuple |
| D3 | respect \(\kappa\) | :123 | **undefined** | fixed by an open example list ("production, inferential identification, impossibility, rule-governed status, achievement of an aim, or aesthetic value"); no membership condition, no individuation of two respects |
| D4 | contrast contract \(\mathcal C\) | :123 | **undefined** | "distinctions **material to that question**"; materiality is the load-bearing word and is not defined |
| D5 | the maps \(\pi,\tau,\sigma,\lambda\) with declared domains | :167, :170 | defined | declared data; many-to-one permitted for \(\pi\); ":170 Their meanings are held fixed across the comparison" |
| **D6** | "the declared abstraction" at which the projected target relation must equal the explanatory component relation | :176 | **undefined** — *restored to v1's status; v2's narrowing is withdrawn (F30, §5(a)(i))* | **v1's words, restored verbatim: the abstraction is a free declaration; no condition ties an admissible abstraction to \(\kappa\).** :176 s1 restricts what the *port translation* may depend on ("only on the ports of its anchored subnetwork and the explicitly declared boundary"); it does not restrict how coarse the *declared abstraction* of s3 may be, and no other line does. **:176 s5 is FW5's own statement of what the missing condition is for**: "Together with (F), which checks the assembled organization, this prevents local relation matches from silently losing constraints shared between components" — an effect s1-s4 do not deliver without an admissibility condition on the abstraction. See the reviewer's construction (γ) at §5(a)(i), recorded verbatim. **Second unconstrained input at the same locus, recorded and deliberately not given its own row:** the *component carving* is also free — the whole-network \(\lambda_w\) of §5(a)(i) satisfies :174 with a single component. |
| D7 | grain \(\ell\) | :154 | **undefined** | "A grain fixes which structural distinctions count as differences for the attribution at issue" — a stipulation; no admissibility condition relative to \(\kappa\) or \(\mathcal C\). Note :154 also constrains coarsening ("Coarsening is not automatically an isomorphism"; bundling "can change the answer to a question about individual contribution") but states no test |
| D8 | active commitments vs incidental remarks | :162 | **undefined** | "part of the interpreted claim"; no procedure, and FW5 explicitly forbids an assessor selecting fragments |
| D9 | (F), (C), (A) | tags :185, :194, :205 | defined | equalities and an indexing condition, all ranging over "the comparisons specified in \(\Sigma\cap\mathcal C\)" (:179, :199); (C) is restricted to "every composition **for which a claim is made**" (:188) and (A) "includes the respect \(\kappa\)" (:208) |
| D10 | non-circular dependence: the :210 contrast clause **and :212's third sentence** | :210, **:212 s3** | defined, on D4/D7/D8 | :210 requires "at least one admitted contrast that removes or changes a nonempty block of active organizational commitments … for which the answer profile changes or ceases to be determined in the claimed way". **:212 s3 — "A contrast family containing only notational variants, or one defined to exclude every change that could matter, does not meet non-circular dependence" — is printed under the Non-vacuity heading but its stated predicate is non-circular dependence; it is filed here (F3).** Its inputs (what "could matter") are D4. **At the A-S locus this clause does no work (§5(a)(i), F2 upheld-against by both reviewers): the strict reading of "every" is correct, and the clause is kept in this row because the row is about the dependency, not about A-S.** |
| D11 | non-vacuity | **:212 s1-s2 only** | defined | "The baseline organization has a compatible state or history"; and an impossibility claim "may correctly assert that a specified goal has no compatible realization, but not infer a substantive result merely from an inconsistent baseline". *v1 filed :212 s3 here; that misfiling is corrected (F3)* |
| D12 | boundary \(\beta\), representation \(\operatorname{Rep}_{\beta,\ell}\) | :149 (display :148-150), :152, :156 | declared primitive | FW5 says so: ":156 The representation relation is an explicit semantic primitive" |
| D13 | structural equivalence at grain, \(d\equiv_\ell c\) | :738-746 | defined, unmapped | ":746 structural at the stated grain, not string equality or similarity"; no record-level test |
| D14 | Bearing (K1): \(\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal E_c,p_\delta)\) | tag :617, gloss :620 | defined, **mapping unsupported** | identifies criticism-bearing with accounting; the route from an authored criticism to \(\mathcal E_c\) is not stated. **The survey of every other bearing locus in the reading edition is at §5(b) and is stated as a survey, not as a universal (F41).** |
| D15 | criticism constituents \(z,\delta,g\), connection | :609 | defined | four-part; ":609 A defect is a specified failure condition on the target or its application", whose **first named kind is inconsistency** |
| D16 | active route; nonconstant dependence on the represented distinction | :601 | defined, unmapped | requires actual occurrences, ports, component relations; "not inferred from the presence of a similar sentence in a record" |
| D17 | reason-use witness and its three-case contrast contract | :628, :630 | defined, unmapped | a structural map preserving internal role bindings; C001 PLAN §9 records that a transcript supplies none |
| D18 | standing \(\operatorname{Live}_j\), (K2) | :638, :642-651 | defined, unmapped | appraisal-indexed; FW5:640 — prompt appearance is a delivery fact, actual use is "not automatically machine-maintainable" |
| D19 | repair (P) with \(O\), \(P\), \(\operatorname{ProducedBy}\) | :787-800 | defined, unmapped | not challenged here; named because (EK) carries Account |
| D20 | reading Account off an output projection | :1210-1218, with :1220-:1224 | **unavailable by FW5's own theorem** | ":1218 no function of \(P(M)\) alone agrees with the accounting predicate on both models"; ":1222 semantic use inferred from delivery logs"; ":1224 the theorem identifies missing information in a projection" — and see §5(a)(i) on what the theorem does **not** say |
| **D21** | **A001's own `bearing`→\(\kappa\) bridge** | — (not an FW5 dependency) | **A001's declared mapping, criticizable, and NOT independent of the cells (F36)** | none of the ten golden `bearing` fields names a respect in :123's sense; the bridge rule is declared in §3 with its provenance disclosed and its per-cell assignment frozen, and an adverse cell charges the bridge before it charges anything of FW5's (F25) |

**Note on the realization conditions (F15).** The conditions FW5 defers to its
constructor section are at **:989-991**. :995-1012 is the Marletto/CTK material
and is a different subject.

**The one published mapping candidate.** The C001 correspondence table
(`experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md`, sha256
`dcaebaf8336c1943700a762b4836679307349d6ff8dfad082e4cd77e23fd7ae7`) is a
proposed, checkable instance of D13 for one criticism document. **Measured,
re-derived at this revision:** it carries **85 units in two arms** — the `fcl`
arm (source `mini_fcl`) has **50** (28 `B.*` body units + 22 `K.*` record-field
units), the `prose` arm (source `mini_prose`) has **35** (20 `B.*` + 15 `C.*`).
**The 22 `K.*` units cover eight records of the objection document — `o1`, `o2`,
`o3`, `o4`, `c1`, `c2`, `p1`, `u1` — and of those only `o1`, `o2` and `o3`
carry a referring row in the golden use table (F39).** *v2 said "records o1, o2,
o3"; that was false of the table and is corrected here and everywhere it
appeared.* **Only the fcl arm's 50 units bear on E2** (F23). A001 uses the
table as a *candidate* mapping and tests it; it does not assume it.

---

## 3. Grain, boundary, contrasts — and the bridge, with its provenance disclosed

Declared under `docs/SEMANTIC_GUIDE.md` "Declare the interpretation before the
evidence" and FW5:728 ("Fix a system boundary, grain, history, and continuity
criterion before assessing an event").

**Disclosure, first, because v2 put it last or not at all (F36).** v2 said the
bridge rule was declared "**before the reading**" and reported as Measured only
"all ten golden `bearing` fields". That was misleading in two ways, and both are
corrected here:

* **Both corpora were read before the rule was written.** The ten golden
  `bearing` fields *and* all 23 F001 `bearing` fields were read first.
* **Two branches paraphrase cells they will be applied to.** **(b3)** — "does
  work its stated evidence does not carry" — paraphrases golden rows 3 and 4
  verbatim ("The ordering of the account's recommendations is doing prescriptive
  work that the stated evidence does not carry"). **(b2)** — "treats one reading
  as **the frame**" — **was tuned on F001 occurrence-01 rows 0-3**, whose
  `bearing` reads "counters treating c1 and c2 as **the frame** rather than as
  one hypothesis among at least two". **(b2) matches zero golden cells.** Any
  claim that the branch set was derived from the golden cells alone is
  **withdrawn**; it was not.
* **The two branches added at this revision are written from :609's own defect
  list**, not from the cells — but they were written with the cells in view, and
  **(b6)** fires on six cells whose `bearing` contains the word "inconsistency".
  That is disclosed rather than presented as independence.
* **Consequence, pre-declared:** D21 is **not independent of the cells**, P8
  records it, and **no outcome of the executable leg may be reported as a test
  of the bridge's independence or as a confirmation of the bridge.** The bridge
  can only be *charged*, never *supported*, by this leg.
* **Consequence, second:** because the rule is post-hoc with respect to the
  cells, the **branch assignment for all 33 cells is frozen now**, in
  `CELLS-v3.md`, before the reading step. No cell may be re-assigned after a
  reading, and a cell whose assignment a reader contests is X4, not re-branched.

| item | A001 declaration |
|---|---|
| **unit that counts as a case** | Prose legs: one fully specified \(\mathcal E=(E,p,\pi,\tau,\sigma,\lambda)\) with its target organization and question, **written out in this document** (F43). Executable leg: one **record carrying a non-empty `bearing` field** **together with one declared target record**, i.e. one row of a published use table. The `type: "objection"` disjunct of v1 is **dropped as a separate criterion** and becomes a **sub-register label** (F24). Not a document, not a node, not a cell of C001. |
| **grain \(\ell\)** | the FCL-1 record keyed by id, with its `text`, `scope`, `grounds`, `bearing`, `action`, `consequence` fields and its ref arrays retained; ids and prefixes retained. This is C001's own declared grain (C001 PLAN §10) and the use-relation instrument's own subject definition. If it is changed later the claim changes with it (**FW5:140** — "What is prohibited is changing it during an assessment without recording the resulting change in what is claimed"). |
| **boundary separating the studied system from its inputs** | The studied system is the **criticism content** and the **target content** as published bytes. Outside it: the model, the endpoint, Mini's graph, the scheduler, the store, the operator-supplied FCL-1 language, the H005 instructions, the decoder, the importer and the use-relation instrument. A001 makes **no attribution to any model or endpoint**. |
| **respect \(\kappa\), and the bridge that supplies it (D21)** | **Measured:** all ten golden `bearing` fields are consequence-if-true clauses (e.g. golden row 2, `o2`→`c2`: "Weakens the claim that falling recurrence would confirm c1 and rising recurrence would refute it; the test has lower discriminating power than the account implies"). **None names a respect in :123's sense.** So \(\kappa\) cannot be "quoted verbatim from the record". A001 therefore declares the bridge rule below, declares its provenance above, and declares that the bridge is **A001's own criticizable contribution (D21)**, not a reading of FW5. |
| **why a bridge rather than "unresolved by construction"** | The round-1 reviewer's alternative — declare the whole leg unresolved by construction — is available and is recorded as such. It is not taken, because it ends the leg without producing anything checkable, whereas a declared, published, pre-registered bridge is a separately identified gap-filling contribution of the kind PURPOSE.md requires. **Consequence, pre-declared: an adverse cell charges D21 before it charges D14, and D14 before anything of FW5's** (§5(b)). |
| **contrast used** | Account's own contrast requirement, **FW5:210** with **:212 s3** — at least one admitted contrast removing or changing a nonempty block of active organizational commitments of the target, with the answer profile changing or ceasing to be determined; and the family must not consist only of notational variants nor be defined to exclude every change that could matter. **Not** FW5:630's three-case contract. |
| **FW5:630's three-case contract, where it does enter** | only in leg E2, and only as a check on D13. C001's registers T/E/D/G are reason-use registers; A001 does not fill them, does not reuse their marks, and does not read an Account result off them. |
| **history / continuity** | none claimed. A001 compares contents, not episodes. |
| **normative relation invoked** | none. No merit, adequacy-of-the-model, or progress predicate is applied to any model or output. |
| **enabling contributions** | FW5 itself, the FCL-1 language, the H005/F001 material and instructions, the two published instruments, the C001 recoding table. |

### The bridge rule (D21), first match wins, applied to the `bearing` text alone

**Match test, declared strictly:** a branch fires only where the `bearing` text
**explicitly asserts** that branch's stated form. A text from which the branch's
form must be *inferred* by the reader does **not** fire it; it falls to (b5).
This is stricter than v2's rule and it is what keeps the reading step from
re-branching a cell that reads awkwardly.

| order | branch | condition on the `bearing` text | \(\kappa\) supplied | source of the respect |
|---|---|---|---|---|
| 1 | **(b1) DISCRIMINATION** | explicitly asserts that the target's test, evidence or inference **cannot distinguish** two or more stated readings, or has **less discriminating power** than the target claims | **inferential identification** | :123's list |
| 2 | **(b2) RIVAL-FRAME** | explicitly asserts that the target treats one reading **as the frame** while at least one rival is on the table | **inferential identification** | :123's list |
| 3 | **(b3) PRESCRIPTION** | explicitly asserts that the target's recommendation, ordering or prescription **does work its stated evidence does not carry** | **achievement of an aim** | :123's list; the aim is the one the target's own recommendation states |
| 4 | **(b6) INCONSISTENCY** *(new, F35)* | explicitly alleges that **two or more of the target's own commitments cannot jointly hold** (e.g. "alleges an internal inconsistency between …") | **impossibility** | :123's list; :609 names **inconsistency first** among defect kinds; :212 s2's "no compatible realization" is the same shape |
| 5 | **(b7) MISSING-DISTINCTION** *(new, F35)* | explicitly alleges **a distinction the target does not draw** and needs | **inferential identification** | :123's list; :609's "a missing distinction" |
| 6 | **(b4) MISREADING** | asserts only that **a reader will misread** the target | **inferential identification**, cell flagged `bridge-strained` | :123's list |
| 7 | **(b5) UNRESOLVED** | otherwise | **none** | — |

**Pre-declared consequence of (b5): the cell is X4 UNRESOLVED and is read no
further.** It supplies no evidence on any side. *v2 routed (b5) cells to X0 as
well as X4 and first-match-wins sent them all to X0/D14; that contradiction is
removed (F38).*

**Measured, at this revision, with the branch assignment frozen in
`CELLS-v3.md`** — reported as a **coverage fact about A001's own bridge, never
as evidence about FW5, about the records, or about their authors:**

| branch | cells | which |
|---|---|---|
| (b1) | **4** | golden 2, 10, 11, 13 |
| (b2) | **4** | F001 occ-01 rows 0, 1, 2, 3 |
| (b3) | **2** | golden 3, 4 |
| (b6) | **6** | F001 occ-01 rows 4, 5, 6, 20, 21, 22 |
| (b7) | **0** | **no cell in the register matches it.** The branch is added because :609 names the defect kind, not because a cell needed it; that it fires on nothing is recorded, not repaired |
| (b4) | **2** | golden 16, 17 |
| (b5) | **15** | golden 0, 1; F001 occ-01 rows 7, 8, 12, 19; occ-05 rows 3-10; occ-07 row 1 |
| | **33** | |

Of the 15 at (b5), **14 are X4 UNRESOLVED** and **one (occ-07 row 1) is X0**,
because X0's condition — no target record id — fires before the bridge is
consulted. **So 18 of 33 cells reach a respect and 15 reach nothing.** Against
v2's rule the two new branches move **six** cells from unresolved to a respect
and nothing moves the other way. **This distribution is not evidence and no
part of the report may treat it as evidence** (§5(b) rule 6).

**Two assignments recorded against v2, because a reader would otherwise expect
the other answer:**

* **Golden rows 0 and 1 are (b5) (F37).** Their `bearing` — "If the driver is
  renegotiation or legitimacy rather than ambiguity, the specification move in
  c2 treats a symptom, and the account's sequencing (chores first, relationship
  later) is misplaced" — asserts no discrimination failure ((b1)), states a
  conditional rather than a rival "on the table" ((b2)), and says "misplaced",
  which is weaker than (b3)'s "does work its stated evidence does not carry".
  **A001 declares them unresolved rather than loosening (b2) to catch them**,
  because loosening a branch to catch a cell is the fitting the disclosure above
  already has to concede once.
* **B01 (F001 occ-01 row 12) is (b5) and therefore X4 (F47).** Its admission to
  the register rests on its non-empty `bearing`; but the bridge reads the
  `bearing` **alone**, and that field — "narrows the commitment to a cost rule
  with an explicit scope, rather than a trigger condition" — alleges no defect
  and matches no branch. v2 justified B01 by its `text`, which §3 forbids the
  bridge to read. **B01 is retained in the register as a datum about the `type`
  field and is pre-declared unreadable by this leg.** Extending the bridge to
  `text` was considered and **declined**: it would re-open the fitting problem
  on a second field.

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
  is **:228's present wording**, whose own sentence "If a genuine explanation
  requires a distinction no such structure can preserve, the proposal must
  change" would be the operative clause.
* Under **(b)**, :226 falls, and so does the whole no-`Because` programme.
* Under **(c)**, :226 survives as written but becomes uninformative until the
  admissibility condition is supplied; the finding is of the missing-definition
  kind and defers rather than refutes. **D6 is of this kind and is not a
  counterexample of any kind.**

Downstream, under (a), (b) or (c) alike, **(K1) at :617** loses the inference
from accounting to bearing, and the \(\operatorname{Account}(c,p_c)\) conjunct
of **(EK) at :831** loses its force. Nothing here requires relinquishing (O),
(Q), equivariance (:1202), the projection theorem (:1210-1218), (M1)/(M2),
(I2), (O1), (T2), the retention fixed point (:947, :950-:952), (CT4) or (RC).

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
0.1, and :1342 cuts the other way. The citation is withdrawn.*

### Three different findings, kept apart

1. **A missing definition** (**D3, D4, D6, D7, D8**, and the materiality input
   of D10). Shows that (E) is not yet determinate for a given (target, question)
   pair: a claimant can make (E) true or false by a free declaration. This
   **defers** both S and N; it refutes neither, and it must not be reported as a
   counterexample. Its remedy is a separately identified gap-filling proposal
   (§5(c)), which must not be back-fitted to whatever the evidence turns out to
   be. *v2 listed only "the materiality input of D6"; D6 is restored in full
   (F30).*
2. **An unsupported mapping** (D14, D16-D18, D20, D21, and D13 if the C001
   recoding table fails its own content-preservation argument). Shows that a
   bridge from published records to an FW5 relation is unwarranted. It defeats
   the application, not the class (FW5:1392). It is the finding the executable
   leg can actually reach (§5(b)).
3. **An operational failure.** **Measured, with both halves now at their own
   lines (F46):** the `deepseek-flash` × `fcl` cell of C001 occurrence-01 has
   **19 of its 20 coordinates unusable at the 8192 ceiling — 8 PARTIAL at
   `finish_reason` "length" with `completion_tokens` exactly 8192, and 11 FAILED
   with `NO_PUBLIC_CONTENT`** — read off
   **`experiments/diagnostics/C001-contrast-triple/occurrence-01/COMPARISON.md`**
   (the table at lines 38-57, "Unresolved in this cell" at line 59; **two
   `COMPARISON.md` files exist under that study and this is the
   occurrence-01 one**). The "8 PARTIAL … 11 FAILED … **and no usage**" wording
   is at `material-occurrence-02.json`:1519. **The "no `finish_reason`" half is
   not at that line**: it is at
   `experiments/diagnostics/C001-contrast-triple/occurrence-02/material.json`
   **line 1483** (and at `occurrence-02/plan.json`:82), which reads "every
   FAILED carries INCOMPLETE_GENERATION with validation_failure_type
   NO_PUBLIC_CONTENT, **no finish_reason and no usage at all**". Because the 11
   FAILED rows carry no usage, **"consumed by an 8192 ceiling" is an inference
   for them and is labelled as one.** Shows a resource fact. FW5:688. It
   supplies no evidence for or against S or N, and no cell of that kind may be
   counted on either side.

---

## 5. The challenge as criticizable contributions

### 5(a) Prose leg — two authored cases, and why each fails

**The rule for choosing between permitted outcomes, declared here and applied
below (F18), unchanged from v2.** For any authored case:

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

**Proviso added at this revision (F42).** **No entry in §2 is derived from a
case's outcome.** The dependency table is a reading of FW5's own text and stands
or falls on that text alone; v2's "the one positive result A-S leaves" made a
D-row's status depend on how a case went, which (r1) forbids in one direction
and v2 then did in the other. **That sentence is deleted** and D6 is back to
what §2 reads off :176 directly. *The round-2 reviewer's alternative fix — amend
(r1) to permit a case to yield a missing definition "provided it is stated as a
property of the dependency" — is **declined**: it re-opens exactly the upgrade
path (r1) exists to close, and it is unnecessary once the D-row is derived from
the source instead of from the case.*

#### 5(a)(i) Case A-S (sufficiency) — **FAILS under (r1), at FW5:208**

*The candidate.* FW5's own discriminating pair, introduced at :1222 and checked
by exhaustive enumeration at :1402 ("All four Boolean input assignments were
checked for the parallel and priority constructions. Their endpoint outputs
agree, while the active second route differs when both inputs are on").

**The candidate written out, as F17's exhibition rule requires of a worksheet
row and F43 requires of a prose case (F43).**

* Target \(D\): the **priority** organization. Ports
  \(V=\{i_1,i_2,g,o_1,o_2,o\}\); components \(J=\{c_1,c_2,c_\vee\}\), with
  \(c_1\) computing \(o_1\) from \(i_1\), \(c_2\) computing \(o_2\) from
  \(i_2\) **gated by** \(g\) (route 2 is live only when route 1 is off), and
  \(c_\vee\) assembling \(o\).
* Candidate \(E\): the **parallel** organization, same ports minus the gate,
  components \(e_1,e_2,e_\vee\), route 2 ungated.
* \(\Sigma\): the four Boolean input assignments with the declared boundary,
  baseline \((1,b_0)\) = both inputs off.
* \(\mathcal C\): the same four assignments, plus the block-deletion contrast
  that removes both routes (this is what discharges :210 and, on the strict
  reading, :212 s3).
* \(\mathcal Q\), \(O_p\): \(\mathcal Q\) returns the value the respect asks
  for, below; \(O_p=\varnothing\) (no obligation is at issue).
* Maps: \(\pi\) the identity on endpoint ports (many-to-one on hidden ports,
  which :170 permits); \(\tau,\sigma\) the identity on the declared edits and
  boundary conditions; \(\lambda\) **as declared per carving**, below.
* \(\kappa\): **the whole case turns on this**, and two candidate respects are
  worked separately below, exactly as F1 required.

**Horn 1 — \(\kappa\) = production of the endpoint output.** \(\mathcal Q\)
returns the produced value of \(o\).

* (A) **holds**: \(\operatorname{Ans}_E\) and \(\operatorname{Ans}_p\) are the
  same function of the four assignments (:1402), and :208's "This includes the
  respect \(\kappa\), not just a matching number" is satisfied, because the
  declared respect asks for the produced output value and nothing else.
* (E)'s other conjuncts can be made to hold — and it **does not matter**,
  because **the attribution is then true**. "\(E\) accounts for the target's
  production of the output", where the declared question's answer profile *is*
  the endpoint output function, is correct. **Nothing false is shown.** FW5:236
  licenses exactly this: "Explanatory depth is question-relative… Equation (E)
  is not a universal measure of elegance or merit."
* Against :1364: the four qualifiers govern a candidate *satisfying (E)*, so
  they are reached here. **(q2) the original question preserved fails**: the
  case only looks adverse if the reader switches, after the fact, from the
  endpoint question to the route question, which is the move (r1)-(r3) and
  `FW5-research-plan-decision.md` ("must not be repaired away by silently
  changing the question, grain, boundary or anchors after the failure") both
  forbid. (q1) is true of the question actually asked; **(q3) survives** on the
  strict reading of :212 s3 below; (q4) is not at issue.
* **v1's sentence "the attribution … is nevertheless false of the target when
  both inputs are on, and FW5's own theorem at :1208-1218 is the reason it is
  false" remains WITHDRAWN.** :1218 says only that "no function of \(P(M)\)
  alone agrees with the accounting predicate on both models" — a claim about a
  projection's information, not about the falsity of an attribution. Worse for
  the case: the theorem's hypotheses are \(M_0\models\phi\) and
  \(M_1\not\models\phi\), i.e. **it presupposes that the accounting predicate
  distinguishes the parallel and priority models**, which is the reverse of what
  A-S needs. :1224 confirms the scope.

**Horn 2 — \(\kappa\) concerns the active route.** This is the horn :1222 pins
the construction to: "Parallel and priority wiring provide a concrete instance
**when the projection retains only endpoint values and the question concerns the
active route**". \(\mathcal Q\) returns which routes are active.

* **(A) Question fidelity fails, at :208, and it fails for every \(\lambda\).**
  With both inputs on, \(\operatorname{Ans}_p\) is "route 1 alone is active" and
  \(\operatorname{Ans}_E\) is "routes 1 and 2 are active" (:1402). (A) at :205
  equates \(\operatorname{Ans}_E(\tau(a),\sigma(b))\) with
  \(\operatorname{Ans}_p(a,b)\) over the comparisons in \(\Sigma\cap\mathcal C\),
  and :208 makes the respect part of what must match. **\(\operatorname{Ans}_E\)
  is a function of \(E\) and the declared question, not of \(\lambda\)**: no
  choice of anchoring changes which routes the parallel organization makes
  active. So (A) fails under **every** \(\lambda\), and the case is over at
  :199-208 before any other conjunct is consulted.
* Because (E) fails, **:1364's four qualifiers are not reached under this horn**
  — they govern "a fully specified candidate **satisfying (E)**". *v2 recorded
  "(q1) fails under horn 2 at :176 s1/s3"; that is withdrawn with the Anchoring
  claim (below).*

**Disposition under (r1): Case A-S fails, and the clause that does the work is
:208 alone** (with :236 under horn 1, where nothing false is shown). It is not a
counterexample and it is not finding 1. It is recorded as a **second failed
sufficiency candidate**, alongside the skew-matrix one, and its value is
negative and bounded: it marks where the sufficiency attack cannot go.

**Every sentence claiming that Anchoring defeats A-S is deleted (F30, F31).**
v2 wrote that "Anchoring fails as well, on the clause :176 states", that the
(α)/(β) dilemma shows "**no endpoint-level abstraction satisfies Anchoring** for
a two-route organization whose routes are the anchored components", and that
"neither does any endpoint-level abstraction of FW5's own discriminating pair".
**All three are withdrawn.** The two subsections below record why.

##### Why the Anchoring argument fails: the omitted case (γ)

v2's dilemma had two horns — **(α)** an abstraction coarsening only the
assembled organization's ports, and **(β)** one coarsening each component's
relation down to assembled endpoint values, excluded by :176 s1 as a matter of
what the *anchoring data* may depend on. **The enumeration is not exhaustive.**
:176 s1 restricts what the **port translation** may depend on; it says nothing
about how coarse the **declared abstraction** of s3 may be, and no other line
fixes that. The round-2 reviewer's third case is recorded **verbatim**, as the
reason:

> **Case (γ), omitted:** route 2's anchored subnetwork in the priority target
> has ports {i₂, g, o₂} (g the gate from route 1); declare the abstraction
> sending any relation over those ports to the full product over {i₂, o₂} — a
> function of route 2's own ports alone, so s1 is met. The projected target
> relation and the parallel route-2 relation then have the same image, s3's
> equality holds, and s4 translates every component edit to the same replacement
> on both sides. (γ) is neither (α) — it *does* coarsen the component relation —
> nor (β) — it never mentions assembled endpoint values.

(γ) does exactly what :176 s5 says is prevented — "this prevents local relation
matches from silently losing constraints shared between components" — which is
why s5 is the right citation for **what the missing condition is for**, and why
**D6 is restored to v1's status: the declared abstraction is a free declaration
(§2).** *The narrowing recorded as `CHANGES.md` S3 — "D6 narrowed rather than
deleted … a smaller and more defensible finding-1 … the form A001 publishes" —
is **withdrawn in full as a deflation**: it made A001 smaller than the evidence
supports, which is a regression of the same kind as re-inflation.*

What (α) and (β) still show, and all they show: **two natural abstractions
fail.** That is kept, and it is not a universal.

##### Can an endpoint-level abstraction satisfy Anchoring for **the carving whose components are the two routes**? (heading narrowed, F31)

Even so narrowed, the answer is no longer used to dispose of A-S, because
another \(\lambda\) escapes any such proof and the case dies elsewhere.
**Recorded, because v2's universal sentence was false of the edition:**

> **The whole-network anchoring \(\lambda_w\).** Carve \(E\) as **one**
> component — the whole parallel network — anchored to the target's whole
> network as one subnetwork. :174's "Every active explanatory component has a
> stated target interpretation under \(\lambda\)" then has exactly one instance.
> That subnetwork's relation, obtained by imposing its component constraints and
> projecting away its hidden ports as :176 s3 itself prescribes, **is** the
> endpoint relation; by **:1402** ("Their endpoint outputs agree") it equals the
> explanatory component relation at the endpoint abstraction. The port
> translation depends only on that subnetwork's endpoint ports and the declared
> boundary, so s1 is met. **(F) at :185 holds over \(\Sigma\cap\mathcal C\) at
> endpoint grain by the same enumeration.** So **Anchoring and (F) hold at
> endpoint grain, with no coarsening at all.**

The case still dies — under **horn 2** (A) fails at :208 for every \(\lambda\),
\(\lambda_w\) included; under **horn 1** the attribution is true. **The clause
doing the work is :208 alone, not :176.** \(\lambda_w\) is also why §2's D6 row
records the *component carving* as a second unconstrained input at the same
locus.

##### The :212 s3 reading, upheld

A001 read :212 s3 — "or one defined to exclude **every** change that could
matter" — strictly: as \(\forall x(\text{could-matter}(x)\to\text{excluded}(x))\),
so that a family admitting **one** mattering change escapes the clause. A-S's
endpoint-level family excludes the gating change but still admits deleting the
block of both routes, which changes the answer profile under either respect.
**The round-2 review upholds this reading**, on the ground that the second
disjunct then has the same shape as the first ("containing only notational
variants"), as a near-synonymous pair should. So:

* **F2 was wrong on the clause** and right that v1 ignored it. That is recorded
  here rather than absorbed.
* **Consequence for D10:** the row **keeps** :212 s3 — the clause's stated
  predicate really is non-circular dependence, which is why F3's move from D11
  to D10 stands — and **the clause does no work at this locus**. D10 is a
  statement about the dependency, not about A-S.
* **Consequence for A001's size: none either way.** Under the loose reading A-S
  would fail at :210/:212 *as well as* :208, still under (r1), with the same
  published result.

#### 5(a)(ii) Case B-N (necessity) — **DROPPED**

*The candidate, as staged in v1.* An inexplicit, distributed diagnostic
explanation of the kind FW5 admits at :857-859 ("partial, distributed, or
temporally extended", available "through memory, imagery, action rehearsal, or
interaction with an artifact") and at **:244** ("A thinker need not possess the
maps in explicit notation to instantiate the relevant organization"), where the
realization has no decomposition into components with stable footprints, so that
several inequivalent anchorings \(\lambda\) are compatible with it.

**v1 pre-committed: "the contribution has to be the *determinacy* step, and if
the determinacy step fails the case fails."** The determinacy step fails.

* **:188 does not demand determinacy.** "The translation preserves identities
  and **every composition for which a claim is made**" — a restriction on which
  compositions are checked.
* **:174 does not demand it either.** "**Every active** explanatory component
  has a stated target interpretation under \(\lambda\)" — a condition on the
  components of a given \(\mathcal E\), not a uniqueness claim about the
  realization.
* **:170 and :244 settle it.** The maps are declared data whose "meanings are
  held fixed across the comparison" (:170), and "The maps can exist before
  anyone discovers them" (:244). **Each \(\lambda\) yields a different
  \(\mathcal E\), and Account is a predicate of \(\mathcal E\)**, not of the
  realization.
* **The disjunction v1 offered is unavailable (F6).** :1364's necessity defeater
  is "A genuine explanation that cannot satisfy the conditions **under any
  interpretation** preserving its actual organization". (E) coming out true
  under one \(\lambda\) **satisfies** necessity. The "either necessity fails"
  disjunct is deleted. `FW5-research-plan-decision.md` says the same: "Failure
  of one selected encoding or grain is not that necessity result."

**Does anything remain that :1372 does not already say? No.** :1372 — "If they
exclude a genuine inexplicit or distributed understanding, it is too strong" —
already states the whole of B-N's residue. **B-N is dropped.** It is not carried
as a "possible counterexample" and not reclassified as finding 1, because the
missing condition it named (determinacy) is not owed.

**Branch, recorded (F14).** :1372 sits under "Representation and apparent reason
use", not under :1362's "A structural account that still does not explain", and
`FW5-research-plan-decision.md` files representation/integration as a distinct
attack branch. Dropping B-N removes the misfiling; the branch stays open and
A001 does not work it.

**What a real necessity case would need, named so the gap is visible.** An
explanation whose **actual organization is independently attested** — not
stipulated in prose by the challenger — for which no \(\lambda\) over that
attested organization satisfies (E). Prose alone cannot supply the attestation.
A001 does not close that gap.

#### 5(a)(iii) What the prose leg leaves

Neither case is an independently sourced interpretive technical document; that
gap, named at the end of `docs/reviews/FW5-account-skew-matrix-challenge.md` and
again in the "Testing FW5 itself" row's deliverable (§0), stays open. **Two
recorded failures are the prose leg's whole yield.** *v2 added "plus the
narrowing of D6"; that is withdrawn (F30).*

### 5(b) Executable leg — a (K1)-mapping test over published records

No provider call. No new instrument. No cell of any published table is filled
by A001; A001 writes its own worksheet, whose rows cite published row ids.

#### The route problem, and the survey that replaces v2's universal (F41)

(K1), tagged at **:617**, reads
\(\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal E_c,p_\delta)\).
**Bearing is defined as Account.** v1's sufficiency condition — "the criticism
does not bear while (E) holds" — is therefore not a statement about Account at
all; it is the denial of a biconditional.

v2 then wrote that there is "**no second, non-Account route to Bearing anywhere
in the reading edition**". **That universal is withdrawn.** It was asserted on a
survey of three loci, and the edition has more. What replaces it is a **survey,
stated as a survey**, of every locus other than the definiens itself.
**Measured:** outside the compounds "obligation-bearing" (:800),
"information-bearing" (:912, :1005) and "standing-bearing" (:1320), which are a
different word, the term *bearing/bears* occurs at **:607, :614, :622, :773,
:896, :900, :1182**; :609 and :620 carry (K1)'s constituents and its side
condition without the term. **The eight loci besides the definiens (:613-618)
are these:**

| locus | what it says | does it supply a second route to \(\operatorname{Bearing}(c,z,p)\)? |
|---|---|---|
| **:607** | "## A criticism and its bearing" | **no** — a section heading |
| **:609** | "A criticism has a represented target \(z\), an alleged defect \(\delta\), grounds \(g\), and a proposed connection from \(g\) to \(\delta\) relative to a question. A defect is a specified failure condition on the target or its application: inconsistency, a false dependency, a missing distinction, an unsupported reference, a failed task, a misapplied rule, or another condition whose interpretation is supplied." | **no** — constituents and a list of defect kinds; it defines no bearing predicate over them |
| **:620** | "The alleged defect must concern the stated target and respect." | **no** — a side condition on \(\delta\) |
| **:622** | "A criticism occurrence can exist when (K1) is false… It can become grounds for a criticism when an organization represents how it bears on a target." | **no** — about occurrences and about what makes an adverse signal into grounds |
| **:773** | "The objection need not have actual bearing, and the response need not improve the situation." | **no** — asserts that bearing can fail; supplies no test for when it holds |
| **:896** | \(\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A\) "states that a reason **bears** on a work in an aesthetic respect" | **a different relation** — *normative* bearing, declared input data in \(\mathcal N\), not \(\operatorname{Bearing}(c,z,p)\) |
| **:900** | "effects belong to \(\mathcal R\), purposes to \(G\), **normative bearing to \(\mathcal N\)**, judgments to appraisal events, and creative contribution to (G) and (EK). **None is defined as another.**" | **no, and it forbids the conflation**: the edition keeps \(\mathcal N\)-bearing separate by its own sentence |
| **:1182** | "**Critical bearing is accounting for the specified defect question.**" (in "Defined relations and dependence order", :1178) | **no** — see immediately below |

**What :1182 does and does not add.** It **adds** two things: FW5's own prose
restatement of (K1) outside the definition block, and its **placement in the
dependence order** — critical bearing is listed among the *defined* relations,
downstream of (E), beside "Reason use is a representation-preserving map…". It
**does not add**: any test, any constituent, any predicate independent of
Account, or any route from a record. **Its effect on A001 is to strengthen the
narrow claim and to remove the wide one:** within the reading edition, the eight
loci surveyed supply no second route to \(\operatorname{Bearing}(c,z,p)\), and
:1182 says why — bearing is *defined from* accounting rather than alongside it.
A001 states the claim **with its coverage attached** and makes no claim about
loci it has not surveyed.

So the only available left-hand side is a **reader's independent judgement that
the alleged defect does or does not obtain of the quoted target passage** — and
that judgement is **A001's own declared observable, not an FW5 relation.** Call
that identification **(O)**; it is A001's, it is criticizable, and it is a
conjunct of everything this leg can reach.

#### The leg's ceiling, declared before the reading, not discovered after it

**Measured (P6(i)):** FCL-1 supplies **no \(\delta\) slot**. Therefore
**\(\delta\) is supplied by an A001 reconstruction for every cell in the
register, without exception.** Two consequences are pre-declared:

* **The register as a whole already exhibits finding 2 against D14** — the route
  from a published criticism record to \(\mathcal E_c\) is neither stated by FW5
  nor supplied by the language. **That finding is recorded once, for the
  register, here, before any cell is read.** The reading step cannot strengthen
  it, cannot make it a counterexample, and cannot produce a second independent
  instance of it; 33 cells do not make it 33 times truer (rule 6 below).
* **Every cell's \(\mathcal E_c\) therefore contains at least one
  A001-reconstructed component by construction.** This is what makes the
  Account-alone charge that v2 defined and denied (F33) **impossible rather than
  merely unexpected**, and it is why the charge table below has no such row.

**What the reading step can still add, and it is little:** per-cell records of
whether, once a reconstruction is exhibited, A001's declared observable and the
(E)-verdict on that reconstruction agree — i.e. **evidence about A001's own
bridges**, charged to D21 and D14. **It cannot reach an Account verdict, and no
row of its worksheet may carry one.**

**Modality (F17).** "Satisfiable" is withdrawn. :1364 requires "a fully
specified candidate satisfying (E)" and :170 requires declared domains "held
fixed across the comparison". **Each worksheet row must exhibit one
\(\mathcal E_c\) with \(\pi,\tau,\sigma,\lambda\) and the question tuple
\(p_\delta=(D,\Sigma,b_0,\kappa,\mathcal C,\mathcal Q,O_p)\) written into the
row**, before any conjunct is marked, exactly as §5(a)(i) writes out A-S.

#### Pre-declared outcome classes — exhaustive, first match wins (F32, F34)

Declared here, before any cell is read.

| order | class | condition | pre-assigned finding kind |
|---|---|---|---|
| 1 | **X0 NOT-RECONSTRUCTIBLE** | a datum (K1)'s right side requires is absent from the **published record itself**, independently of any A001 reconstruction — in this register, **no target record id** (occ-07 row 1, a `bare_label_ref` resolving only to the owning artifact) | **finding 2 at D14** — one instance of the register-level finding already declared above, never a new or additional finding |
| 2 | **X4 UNRESOLVED** | the bridge returns **(b5)**; or the cell is in **E3**; or the two readers **disagree** on the branch assignment, on whether (E) holds, or on whether the defect obtains; or **either reader records a judgement as undetermined** | **none.** Recorded with the disagreement, never averaged (FW5:634) |
| 3 | **X3 RECONSTRUCTION-FAILED** | no \(\mathcal E_c\) can be jointly written out: some component of \((E,p_\delta,\pi,\tau,\sigma,\lambda)\) cannot be supplied at all | **finding 2 at D14 and D21**, naming the absent component. **No counterexample language of any kind is permitted in this class** (F34) |
| 4 | **X6 UNDECIDABLE-DEFECT** | \(\mathcal E_c\) exhibited and **both readers agree the quoted passage does not settle** whether the defect obtains | **finding 2 at D14 and D21** — the record did not supply a defect determinate enough for either side to be evaluated |
| 5 | **X5 FREE-DECLARATION** | \(\mathcal E_c\) exhibited and both judgements determinate and agreed, **but only because a reader supplied a free declaration** at D3, D4, **D6**, D7, D8 or D10's materiality input | a **finding-1 exhibit** against the named D-row: the declaration that had to be supplied is quoted. **No finding against FW5's mapping** |
| 6 | **X2 CONFLICT-POSITIVE** | (E) **holds** on the exhibited \(\mathcal E_c\) and the defect **does not obtain** of the quoted target passage | a **conflict** among three propositions — (K1), (E) on this \(\mathcal E_c\), and **(O)** — charged by the table below. **Never a counterexample to Account, never to (K1) alone** |
| 7 | **X2b CONFLICT-NEGATIVE** | (E) **fails** on the exhibited \(\mathcal E_c\) and the defect **does obtain** | the same three-way conflict, charged the same way. **Explicitly not a necessity result**: :1364's necessity defeater quantifies "under any interpretation", and **this leg cannot quantify over interpretations at all**, so no cell can ever produce that quantifier (F34) |
| 8 | **X1 AGREE-POSITIVE** | (E) **holds** and the defect **obtains** | one supported instance of the (K1) mapping. **Charge none** |
| 9 | **X1b AGREE-NEGATIVE** | (E) **fails** and the defect **does not obtain** | one supported instance of the (K1) mapping, **negative direction**. **Charge none** (F32) |

**Why these are exhaustive, argued rather than asserted.** Rows 1-5 remove, in
order, every way a cell can fail to reach a state in which (i) an
\(\mathcal E_c\) is written out, (ii) both readers agree, (iii) both judgements
are determinate, and (iv) no free declaration was needed. A cell that survives
rows 1-5 is in exactly that state, so each of the two judgements — "(E) holds on
this \(\mathcal E_c\)" and "the defect obtains of this passage" — has a
determinate agreed truth value, and rows 6-9 enumerate **all four** Boolean
combinations. **The table closes on the enumeration, and exhaustiveness is
asserted only here, after it.** First match wins, so exactly one class applies.
*v2 had no home for the (E)-fails/defect-does-not-obtain cell, which is the
concordant case most supporting (K1), and none for a passage that settles
nothing (F32); both now have one.*

The 1-vs-2 rule for a failed reconstruction is unchanged: **a missing FW5
primitive → finding 1; a missing route from a published record to an FW5
relation → finding 2.**

#### The charge rule, as a decision table — one row per class (F33)

> **Read this table literally. It is the whole rule. There is no further branch,
> no residual clause, and no exception.**

| class | charged to | may the charge name Account? |
|---|---|---|
| **X0** | **D14** | **no** |
| **X4** | *(nothing)* | **no** |
| **X3** | **D21 first, then D14** | **no** |
| **X6** | **D21 first, then D14** | **no** |
| **X5** | the named D-row (D3, D4, D6, D7, D8 or D10) as a finding-1 exhibit | **no** |
| **X2** | **D21 first, then D14**; the residue, if any, is recorded as a conflict among (K1), (E) and **(O)**, and left as a conflict | **no** |
| **X2b** | **D21 first, then D14**; same residue treatment | **no** |
| **X1** | *(nothing)* | **no** |
| **X1b** | *(nothing)* | **no** |

**Closing sentences of the rule, which are part of the rule.**
**(i) No row names Account, and no composition of rows produces one.**
**(ii) There is no Account-alone charge.** v2 defined one ("only if
\(\mathcal E_c\) is supplied in full by the record's own fields under no A001
bridge and both readers agree") and denied it two sentences later; **that branch
is deleted, not merely disclaimed** (F33).
**(iii) Its antecedent is false for every cell in this register anyway**, and
that is Measured, not expected: FCL-1 has no \(\delta\) slot, so no cell's
\(\mathcal E_c\) is supplied in full by the record's own fields.
**(iv) A cell that somehow met the deleted condition would be recorded as an
anomaly in the worksheet's notes column and would still be charged by the row
its class assigns above.**
**(v) No upgrade of a class after a reading is available, under any reading of
this document.**

#### Cells — the revised pre-registration (33 cells)

Rendered as data in `CELLS-v3.md`, **with the bridge branch and, where already
determined, the outcome class frozen per cell**. Pins unchanged (all five
re-hashed by both reviews):
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
snapshot `use-table-golden` rows 0, 1, 2, 3, 4, 10, 11, 13, 16, 17 (10); F001
occurrence-01 rows 0-8 and 19-22 (13), occurrence-05 rows 3-10 (8),
occurrence-07 row 1 (1). **F001 occurrences 02, 03, 04, 06 and 08 — five
occurrences — contribute zero rows (F44)**; that is a fact about those
documents' authored refs, not about their authors, and it is recorded as a cell
count of zero, never as a negative finding.

*Sub-register B — one cell whose referring record is not typed `objection`
(F24, P7).* F001 occurrence-01 **row 12**, `carry#r2` → `response#m2`,
`type: "claim"`. **Pre-declared (b5) → X4 (F47)**, for the reason in §3: the
bridge reads the `bearing` field alone and this row's `bearing` matches no
branch. It is retained as a datum about the FCL-1 `type` field, not as a
readable cell.

*Declared-use rows, a separate register (12 rows, `use-table-golden` rows 5-9,
12, 14, 15, 18-21).* Carried by `claim`, `use` and `problem` records with no
`bearing`. Not cells; FW5:640 makes a declared field a delivery fact. They are
read only to record what the language declared, and they can never supply a
counterexample to anything.

*E2 — equivariance check, with its reachability stated (F23, F39).* The C001
ORIGINAL objection block against the RECODING block, **unit by unit over the
fcl arm's 50 units** (28 `B.*` body + 22 `K.*` record-field), not over all 85 —
the other 35 are the `mini_prose` arm. **Measured: the 22 `K.*` units cover
eight records — `o1`, `o2`, `o3`, `o4`, `c1`, `c2`, `p1`, `u1` — of which only
`o1`, `o2`, `o3` carry a referring row in the golden table**, so **E2 can reach
at most golden rows 0, 1, 2, 3, 4** — five cells. Golden rows 10, 11, 13 refer
from the `response` node (`k3`, `k7`) and rows 16, 17 from `carry` (`n3`), which
the table does not cover. No F001 cell is reachable by E2 at all.

*E2's provenance (F26).* The ORIGINAL block is the H005 objection document
"exactly as the H005 `response` node saw it: the same `body` and `commitments`
bytes, projected by the same `project()` with view `both`" (C001 PLAN:184-188);
`prepare` refuses unless the case bytes equal the occurrence artifact bytes
(`ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES`). It is **identity of the
projection**, not of the artifact file.

*E3 — non-evaluable cells, declared in advance and excluded from every side:*
C001 occurrence-01 `deepseek-flash` × `fcl`, 19 of 20 coordinates as restated in
§4 finding 3; the single PARTIAL at `ollama-glm-5.3` × `fcl` CONTROL rep2; the
12 nodes whose commitment surface was not read in `use-table-full`
(`nodes_not_read`, 10 `prose_not_parsed` plus 2 `unavailable_decode_failure`);
and the 7, 8, 6, 5, 6, 9, 6, 7 `nodes_not_read` of the eight F001 use tables.

**An equivariance failure (E2), with its second disposition deleted (F40).** A
cell whose (E) assessment differs between the ORIGINAL and RECODING codings.
This is **not** a counterexample to S or N. **It is finding 2 against the C001
table's own content-preservation argument (D13), and nothing else.** *v2 offered
a second disposition — "or a challenge to FW5:1202's applicability at this
grain" — which is **withdrawn**: :1202 hypothesises that **all** carriers,
component relations, role bindings, maps, histories, question contracts and
attribution indices are transported along structure-preserving bijections, the
recoding table recodes **one** document (the criticism side) while the targets
`account#c1-c3` are not recoded at all, and :1206 excludes what is not "the
stipulated bijections". **No E2 outcome bears on :1202.***

**What would NOT constitute a finding against FW5, pre-committed.**

1. A record whose `bearing` field is empty, or whose defect \(\delta\) is not
   separately addressable because FCL-1 has no \(\delta\) slot. The \(\delta\)
   point is the register-level finding 2 already declared above; it is not
   re-earned per cell.
2. A bare id token shared between two documents; the same ambiguity C001's `E`
   register refuses to resolve.
3. A cell whose delivery is PARTIAL, FAILED, OPAQUE or undecoded (E3).
4. A lexical-overlap passage from the use table. The instrument's own banner:
   "A lexical overlap is not evidence of use."
5. Any difference between endpoints or families. A001 issues no cross-family
   comparison and none may be read off its worksheet (FW5:849, :851).
6. **A count of cells, of any kind, on any side (F21): a single exhibited
   instance, with both passages quoted, defeats a universal claim in the
   worksheet's own scope; no count adjudicates anything.** FW5:851's own list is
   "(G), (P), or (EK)" — "No quantity of endorsements, surviving tests, repeated
   observations, or partitioned features enters (G), (P), or (EK) as an
   automatic warrant" — and **Account is not in it**; the link from (EK) to
   Account is the conjunct at :831. **The universal claim in reach here is
   (K1)**, and it is named so that this rule's claim-enabling half has a stated
   subject. **The branch counts of §3 are coverage facts about A001's own
   bridge and are explicitly not evidence under this rule.**
7. A finding about C001's four registers. A001 does not fill or read them.

**Reading discipline.** Two readers per cell; where they disagree the cell is
`unresolved` and the disagreement is recorded, never averaged (FW5:634; C001
PLAN §8a:743-745). The worksheet's assessment columns are rendered empty by the
staging and are filled only by the reading step.

### 5(c) P3-P8, as separately identified gap-filling contributions

Source for P3-P7: `docs/reviews/fw5-vs-harness-spec-2026-09-14.md` §5. **P8 is
A001's own** (F25). Governing rule, verbatim from PURPOSE.md: "Proposed
gap-filling definitions, interpretations and mechanisms are separate
criticizable contributions; they must not silently rewrite the source or absorb
adverse evidence after the fact." Each is published as its own document with its
own identity; none may edit FW5 or any frozen PLAN; each acceptance condition is
declared **before** A001's reading.

| id | gap it fills | which A001 dependency | rule of engagement | offline today |
|---|---|---|---|---|
| **P3** criticism-ablation arm for F001 occurrence-02 | discharges `ProducedBy` (FW5:800), not Account | D19 | needs live calls; **out of A001's scope entirely** | no |
| **P4** loss ledger (O, P pinned before the later cycle) | (P) at FW5:787-802 | D19 | must be pinned by sha256 *before* dispatch; a dry run over an existing pair is labelled as violating its own pre-declaration and establishes nothing | dry run only |
| **P5** custody and grain preconditions | D7, D13 | if P5 shows the §3 grain is not partition-invariant, A001's cell readings are **preconditioned**, not rescued | yes |
| **P6** FCL-1's fields against FW5:609/:622 | D14, D15 | supplies the \(\delta\)-slot diagnosis this leg's ceiling rests on; it is a **language-adequacy** reading of one cycle, never an Account result | yes |
| **P7** pre-registered reading set | the observer, not the subject | A001's cell list **is** P7 applied to this stage: frozen in `CELLS-v3.md`, with every change since v1 recorded and the v1 list retained | yes |
| **P8** the `bearing`→\(\kappa\) bridge | D21 | **declared with its provenance disclosed: it is NOT independent of the cells (F36).** (b3) paraphrases golden rows 3/4; **(b2) was tuned on F001 occurrence-01 rows 0-3** and matches zero golden cells; (b6)/(b7) are written from :609's list with the cells in view. **Consequence: this leg can charge the bridge and can never support it**, and no outcome may be reported as evidence that the bridge is right | yes |

P3 and P4 are named and deferred. P5, P6, P7 and P8 are what A001 carries
offline.

---

## 6. Claim ceiling

*Extended at each revision, never relaxed.*

* Nothing about creativity across all tasks, or about any model's repertoire.
  FW5:1256-1260; PURPOSE.md.
* No refutation of FW5 or ECS from an implementation failure, a ceiling, a
  decoder refusal or an unread surface. **FW5:688; FW5:1392; FW5:1404**;
  PURPOSE.md. *(v1 cited :1336-1344 here; withdrawn, see §4.)*
* A single failed candidate does not confirm FW5 — the precedent is
  `docs/reviews/FW5-account-skew-matrix-challenge.md`, whose own result is
  "this rejects one attempted witness; it neither confirms FW5 nor settles
  other sufficiency and necessity attacks." **A001 contributes a second failed
  candidate, and the same sentence governs it.**
* One reading of one cycle's records over 33 cells cannot decide the
  constitutive conjecture. **FW5:1368, quoted whole (F49): "These challenges
  concern the constitutive conjecture, not a missing proof of a theorem
  asserted to follow from set theory. The distinction matters: a definition can
  be exact while being a poor theory of its intended subject."** *v2 stopped the
  quotation at "theorem" with no ellipsis, dropping "asserted to follow from set
  theory", in a document that quotes :1364 in full without ellipsis.*
* A001 establishes no Origin (G), no Repair (P), no CreateEK, no reason-use
  witness, no standing, no recursive capacity.
* A001 issues no judgement about whether any H005 or F001 objection is a good
  objection. FW5:630 — "Understanding and using an invalid objection does not
  make it valid."
* A001 says nothing about ECS 2.0's graded accounting or intrinsic variation
  family.
* **No cell of the executable leg can charge Account** (§5(b) charge table). Its
  maximum reach is D21 and D14, plus a recorded conflict among (K1), (E) and
  A001's own observable (O).
* **A001 offers no counterexample to sufficiency and none to necessity.** It
  records two failed candidates and the reasons they failed.
* **New at v3: A001 makes no universal claim about which abstractions satisfy
  Anchoring.** v2's "no endpoint-level abstraction satisfies Anchoring…" and
  "neither does any endpoint-level abstraction of FW5's own discriminating pair"
  are withdrawn; case (γ) and \(\lambda_w\) are recorded against them (§5(a)(i)).
* **New at v3: the executable leg's finding 2 against D14 is declared before the
  reading and cannot be strengthened by it.** A reading that reports the
  \(\delta\)-slot absence as a discovery, or reports it per cell, is a
  regression against this document.
* **New at v3: the branch counts of §3 and the cell counts of §8.5 are coverage
  facts, never evidence** (rule 6).
* The independently sourced interpretive technical case the skew-matrix review
  says is still owed **remains owed**, and so does the "Testing FW5 itself"
  row's stated deliverable (§0).

---

## 7. File layout for publication, and why

**Choice: `docs/reviews/` for the documents, `experiments/diagnostics/` for the
executable leg.** Reason, from the repository's own conventions: there is no
`docs/challenges/` directory, and the single existing Account challenge —
`docs/reviews/FW5-account-skew-matrix-challenge.md` — already sits in
`docs/reviews/` with its offline check under
`experiments/diagnostics/fw5-account-skew-matrix/`. `experiments/analyses/` is
reserved in practice for instrument outputs regenerated over frozen occurrences;
A001's executable leg is a pre-registered reading with a frozen cell list and
pre-declared outcome classes, which is what `experiments/diagnostics/` holds.

```
docs/reviews/A001-account-challenge-2026-09-14.md
    §0 relation to the skew-matrix challenge, the authority for each leg and the
    deliverable A001 does not deliver; §1 claims with FW5 lines; §2 dependency
    table; §3 grain/boundary/contrast, the bearing→κ bridge and its disclosed
    provenance; §4 relinquishment + the three findings; §5(a) the two failed
    prose cases, both written out, and the rule that disposes of them;
    §6 claim ceiling. Receipt paragraph at the head.
docs/reviews/A001-gap-filling-proposals-2026-09-14.md
    P3-P8 as separate criticizable contributions, each with its acceptance
    condition declared before the reading (§5(c)).
experiments/diagnostics/A001-account-challenge/PLAN.md
    Pre-registration of the executable leg: the (K1)-mapping route with the
    eight-locus survey, the leg's declared ceiling, the frozen cell list, the
    nine outcome classes with the exhaustiveness argument, the charge decision
    table, the unresolved rules, the two-reader rule, the claim ceiling,
    0 planned provider calls.
experiments/diagnostics/A001-account-challenge/material.json
    source pins (FW5, both use_table.json, both comparison.json,
    RECODING_TABLE.md, both C001 materials) + the frozen cell list as data.
experiments/diagnostics/A001-account-challenge/CELLS.md
    the 33 cells in two sub-registers with their frozen bridge branches, the
    12 declared-use rows, the five E2-reachable cells and the E3 exclusions,
    rendered from material.json.
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
written, moved or touched. **Measured, re-verified mechanically at this
revision, not inherited:** zero `runtime_files` entries in any
`experiments/**/*.json` point under `experiments/` or `docs/`;
`campaign.source_identity()` (`src/minireason/campaign.py`:35-47) hashes
`src/**/*.{py,json}` plus `pyproject.toml` only, so A001 adds no identity any
frozen plan depends on; the string `A001` appears nowhere in the repository; and
neither target path above exists.

### Receipt paragraph, corrected to house style (F27, F50)

**Measured, re-counted at this revision's bytes** (the denominator has moved
again since round 2): `docs/DECISION_LEDGER.md` now carries **104**
`REC-20260914` entries; lines carrying `Choice:` 96, `Why:` 86 (`Reason:` 9),
`Contribution:` 90, closing `Prior verified commit/tree:` 24, with full-date
opening timestamps. The draft below matches all four.

**Two conventions v2's draft omitted, both carried by `REC-20260914-Y` and
`-Z` themselves (F50), now present:**

* an opening **`Letter:`** field, which states which letter closed last, that
  the taken letter was free, and that it is taken here;
* the **append note**: "appended in byte mode and staged only after an
  insertions-only `git diff --numstat` (**OPS-20260914-LEDGERCRLF**; the file's
  **37 historical CRLF lines must still be 37** after the append)".

**A fact that has moved since round 2 and must not be carried from staging.**
Round 2 recorded "`-Z` is the last free letter". **Measured now: `-A` through
`-Z` are all taken** (`REC-20260914-Z` opened at 11:14 UTC). **So the
2026-09-14 single-letter series is exhausted, and this staging does not invent
a successor scheme.** The identifier is determined **at the moment of the
append**, by the appender, against the ledger's bytes at that moment — exactly
as `-Y` and `-Z` each record doing — and the `Letter:` field states what was
found and what was taken. Staging names no identifier.

> REC-\<date\>-\<identifier determined at the append\> opened at YYYY-MM-DD
> HH:MM UTC: Letter: \<which receipt closed last, at what time, that the taken
> identifier was free when the ledger was read, and that it is taken here; the
> 2026-09-14 single-letter series A-Z was already exhausted when A001 was
> staged\>. This receipt is appended in byte mode and staged only after an
> insertions-only `git diff --numstat` (OPS-20260914-LEDGERCRLF; the file's 37
> historical CRLF lines must still be 37 after the append). Stage A001, an
> independent Account sufficiency-and-necessity challenge to the designated FW5
> reading edition (sha256 `8105925b…e33ee63a`), under PURPOSE.md ("In parallel,
> an independent Account sufficiency or necessity challenge tests FW5 itself");
> the prose leg is written against the "Testing FW5 itself" row of
> `docs/reviews/FW5-research-plan-decision.md`, which is still
> `Status: proposed, awaiting the user's approval` and is cited as intent, not
> approval, **and whose stated deliverable — a candidate counterexample and the
> clause that would have to change — A001 does NOT meet and records as still
> owed.** **A001 OFFERS NO COUNTEREXAMPLE AND NO POSITIVE RESULT ABOUT FW5'S
> STATED CLAUSES.** Choice: publish
> `docs/reviews/A001-account-challenge-2026-09-14.md` (the two named claims with
> their FW5 lines; the dependency table marking each primitive defined /
> undefined / defined-but-unmapped, **with D6 — the declared abstraction — marked
> undefined, a free declaration**; the grain, boundary, contrast and
> `bearing`→κ bridge declared before any evidence **with the bridge's dependence
> on the cells disclosed**; the conditional relinquishment statement; and **two
> authored prose cases written out and recorded as failures with the FW5 lines
> that exclude them — Case A-S at FW5:208, Case B-N at FW5:1372 with :188,
> :174, :170 and :244**),
> `docs/reviews/A001-gap-filling-proposals-2026-09-14.md` (P3-P8 as separately
> identified contributions with acceptance conditions declared before the
> reading), and `experiments/diagnostics/A001-account-challenge/` (PLAN.md,
> material.json, CELLS.md and an empty WORKSHEET.md) — the executable leg over
> **existing published records only**, restated as a **(K1)-mapping test**: 33
> bearing cells in two sub-registers drawn from the H005 occurrence-01 snapshot
> use tables and the eight F001 use tables, **nine pre-declared outcome classes
> with an argued exhaustiveness and a charge decision table no row of which
> names Account**, 12 declared-use rows kept in a separate register, five
> E2-reachable cells over the C001 correspondence table's 50 fcl units, and a
> declared exclusion list of non-evaluable cells. Why: the source's sufficiency
> and necessity claims are the place FW5 itself says to attack it (FW5:1362-1364,
> :1502), and the repository has never tested them against its own published
> records; this stage reports that the two authored attacks fail on stated
> clauses, that the executable leg's one finding against FW5 — no stated route
> from a published criticism record to \(\mathcal E_c\) — is declared **before**
> the reading and cannot be strengthened by it, and that FW5:617 defines bearing
> as accounting while the eight other bearing loci surveyed in the reading
> edition supply no second route. Contribution: a separately identified test of
> the semantic source with its dependencies named before the evidence, which
> returns two recorded failures, one declared mapping gap and one disclosed,
> criticizable bridge rather than a counterexample it cannot support; a missing
> definition, an unsupported mapping and an operational failure are recorded as
> three different findings and never as one. State: PENDING — **zero provider
> calls planned and zero made**; no cell of any published table is filled by
> this stage and every assessment column of WORKSHEET.md is published empty; the
> reading step is a separate receipt. Evidence: pins recorded in
> `material.json`; nothing under `experiments/diagnostics/C001-*`, `H005-*`,
> `F001-*` or `experiments/analyses/` written or touched. Prior verified
> commit/tree: \<the last verified published commit\> / \<its tree\>, read at
> the moment of the append.

### What needs a live call

**Nothing.** Every leg is offline: the prose cases are authored, the executable
leg reads published bytes, and the equivariance check reads a published table.
The two-reader rule of §5(b) is **not** a live provider call and does **not**
go to a human as a blocking dependency: it routes to the automated loop's
reader roles, with every FW5 line and every record path re-read at the line.
P3 and P4 would need live calls; both are deferred out of A001 and neither may
be reported as Account evidence.

---

## 8. Concerns carried into the reading step

1. **The leg reaches D21 and D14 and stops there.** The worksheet forces a
   charge to D21, D14 or a recorded conflict, and offers no Account cell at all.
   Its one finding against FW5 is declared in advance.
2. **The FCL-1 records were not authored as \(\mathcal E\).** They were authored
   as criticisms in a language with `target`, `grounds` and `bearing` but no
   \(\delta\) slot. Reconstructing \(\mathcal E_c\) from such a record is itself
   an interpretation; X3, X5 and X6 are where that lands, and none is a finding
   against Account.
3. **The bridge (D21) is the leg's softest joint, and it is not independent of
   the cells.** §3 discloses which branches were tuned on which rows. If the
   bridge rule is wrong, the respects are wrong and every downstream mark is
   wrong. It is published as its own contribution (P8) so that it can be
   rejected on its own, and the leg can charge it but never support it.
4. **The grain is C001's, not A001's.** Adopting the record-keyed grain keeps
   A001 comparable with the published material but inherits P5's open
   partition-invariance question. If P5 later shows the reading does not survive
   re-partition, A001's cells are preconditioned, not rescued.
5. **Cell supply is thin and uneven, and 15 of 33 cells are pre-declared
   unreadable.** 10 cells in H005 golden; 23 across F001, of which **14 come
   from one occurrence** and **five occurrences supply none (F44)**. Only five
   cells are E2-reachable. **18 of 33 reach a respect under the bridge; 14 are
   X4 and one is X0 before the reading begins** (§3). No universality claim of
   any kind may be built on that distribution, and the zero-row occurrences must
   be reported as zero rows, not as silence.
6. **Two published Account challenges will then exist, and both report a failed
   candidate.** §0 states the relation. A001 must not be read as the skew-matrix
   review's successor or as an attempt to overturn it.
7. **The honest A001 is smaller than v2's, which was smaller than v1's — but
   not everywhere.** v2 made itself smaller than the evidence supports at one
   place (the D6 narrowing) and that was a regression of the same kind as
   re-inflation. Whoever reads this next should check **both directions**: any
   sentence that offers a candidate counterexample, upgrades an outcome class
   after a reading, or lets a cell charge Account is a regression; and so is any
   sentence that concedes a dependency is defined when the reading edition does
   not define it.
8. **Three things in this document are arguments, not readings, and are the
   places to attack it.** (i) The claim that (A) fails under **every**
   \(\lambda\) under horn 2 — it rests on \(\operatorname{Ans}_E\) being a
   function of \(E\) and the declared question rather than of \(\lambda\).
   (ii) The exhaustiveness argument for the nine outcome classes. (iii) The
   strict reading of :212 s3, which two reviews have now accepted but which is
   still a reading of the word "every".
