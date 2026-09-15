# A001 — Account sufficiency / necessity challenge: in-progress record

**Published under `REC-20260914-AB`, 2026-09-14, on branch
`claude/project-state-direction-j5rbun` (publication to `main` pending owner merge).**

**What this is.** An **in-progress record** of the task PURPOSE.md names: "In parallel, an
independent Account sufficiency or necessity challenge tests FW5 itself." It is not a result. It
has passed **three adversarial review rounds** (F1–F29, F30–F50, F51–F67, each mapped to fixed /
withdrawn / declined-with-reason) and a **narrow verification** which returned seven verdicts and
the judgement **"PUBLISHABLE AS IN-PROGRESS RECORD: yes"**; both are in
`A001-account-challenge-2026-09-14-history/`.

**Open items are carried, not hidden.** The narrow verification's **eleven residual open items** are
appended **verbatim** as this document's final section, **"Open items carried into this record"**,
so that a later reviewer attacks them first. Two of them are defects in A001's own instrument and
its own housekeeping, and none of them strengthens A001 against FW5. Items 1, 2 and 11, which the
verification asked to be fixed at the ledger append, are handled **in `REC-20260914-AB` itself
rather than by editing this record**: the false lexical-sort justification for the `-AA` scheme is
**not adopted** there, the receipt's identifier is `-AB` because `-AA` was already taken, and the
§7 sentence "no identifier of more than one letter occurs anywhere in the file" stands here as its
authors wrote it, corrected by open item 2 below.

**No provider call was made for A001 — zero calls.** Every leg is offline: the two prose cases are
authored, and the executable leg reads published records only. No credential was read.

**What follows is `STAGING-v4.md` verbatim**, the revision-4 staging as its authors froze it,
including its references to scratchpad files (each identifies where the work was done) and its own
sentence "Staging only. Nothing here is published" — which remains true of what it claims: no cell
is filled, no reading is offered, and publishing this document does not perform its reading step.
The cell register is published beside it as `A001-account-challenge-2026-09-14-cells.md`; the
earlier revisions, the revision-history maps, the three review rounds and the narrow verification
are the audit trail in `A001-account-challenge-2026-09-14-history/`. **The remaining paths §7
proposes — `docs/reviews/A001-gap-filling-proposals-2026-09-14.md` and
`experiments/diagnostics/A001-account-challenge/` (PLAN.md, material.json, CELLS.md, WORKSHEET.md)
— are NOT published by this receipt, so the executable leg is not pre-registered.**

---

# A001 — Account sufficiency / necessity challenge: staging, revision 4

Supersedes `STAGING-v3.md`. `STAGING.md` (v1), `STAGING-v2.md`, `STAGING-v3.md`,
`CELLS-v2.md`, `CELLS-v3.md`, `REVIEW.md`, `REVIEW-2.md` and `REVIEW-3.md` are
retained unedited beside it, so every step is diffable. `CHANGES.md` maps
F1-F29; `CHANGES-v3.md` maps F30-F50; `CHANGES-v4.md` maps F51-F67 to fixed /
withdrawn / declined-with-reason. `CELLS-v4.md` carries the revised
pre-registered cell list with the frozen per-cell bridge branch.

Staging only. Nothing here is published, no cell is filled, no reading is
offered, and no provider call was made or is planned. Sentences are marked
**Measured** (readable off a named file at a named line) or **Interpretation**
(a reading that could be wrong). Every claim traces to an FW5 line of the
designated reading edition, sha256
`8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a`
(1,502 lines, **re-verified at this revision, and every FW5 line cited below
re-read at the line**), or to a published record path.

**What revision 4 does.** Round 3 returned three blockers, ten should-fixes and
four notes. All three blockers say the same kind of thing: **v3 asserted a rule
it could not run.** (i) The disposal of Case A-S rested on an unstated premise
about \(\operatorname{Ans}_E\) that the edition does not supply and one of its
own lines cuts against (F51). (ii) One outcome class was unreachable and another
swallowed four more (F52, F53), so the table that was v2's fix did not work as a
first-match-wins ordering. Revision 4 fixes all three **by naming the premise
instead of hiding it, and by rebuilding the class table so that exhaustiveness
is definitional and reachability is exhibited.** It also applies §3's own strict
match test consistently for the first time (F58), which **moves five cells out
of a respect and into unresolved**. **A001 is smaller at v4 than at v3 in what
it asserts, and larger in what it discloses against its own bridge.**

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

**Authority, and the deliverable A001 does not deliver. (Measured.)** The two
prose legs are written against the "Testing FW5 itself" row of
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

1. a **dependency table** over (E)'s primitives (§2), in which D6 is undefined
   (the declared abstraction is a free declaration) and, **new at v4, D22 is
   undefined — the reading edition does not state how a candidate's answer
   profile \(\operatorname{Ans}_E\) is arrived at** (F51);
2. the **recorded reasons two authored prose cases fail** — Case A-S at
   **FW5:208 under a named premise A001 supplies and FW5 does not**, with the
   alternative reading recorded and the residue filed as a missing definition;
   Case B-N at **FW5:1372** with :188, :174, :170, :244 (§5(a));
3. a pre-registered **(K1)-mapping test** over 33 published cells with **nine
   outcome classes whose exhaustiveness is definitional, whose reachability is
   exhibited cell by cell**, and a **decision-table charge rule under which no
   row names Account** (§5(b));
4. a declared **`bearing`→κ bridge (D21)** with its coverage measured, its
   dependence on the cells disclosed in full, its per-cell branch assignment
   frozen in advance, and — **new at v4 — the measured fact that every branch
   which fires at all fires only on cells whose text that branch's own condition
   paraphrases** (§3, `CELLS-v4.md`).

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
its four qualifiers do the work:**

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

**What Claim N's failure would and would not touch.** It would touch **:228** in
the necessity direction and the \(\operatorname{Account}(c,p_c)\) conjunct's
force in **(EK) at :831**. It would **not** show that the explanation falls
outside the base class. FW5:1192 defines \(\mathsf{FW5}\) as "interpretations
supplying the data above, respecting their typing, and satisfying the
physical-realization and reference-coherence conditions", and says it "can
describe irrational systems, false conjectures, obstructed inquiry, missing
evidence, and failed attempts". An interpretation whose \(\mathcal E\) fails (E)
is not thereby outside \(\mathsf{FW5}\); it is a member describing a failed
account. **v1's relinquishment chain through :1192 is withdrawn.**

**Two claims FW5 makes that A001 does NOT challenge, named so they are not
absorbed.**

(i) **The results protected by :1390.** :1390's list is exactly "(M1), (M2),
(I2), (O1), (T2), or the retention fixed-point result", and a counterexample to
one of those while all stated assumptions hold "would expose a mathematical
error" — a different finding. The finite monotone theorem is (M1) at :306 and
(M2) at :315 (:296 is its heading). (I2) is at :429, (O1) at :497, (T2) at
:582. **The retention fixed-point result is at :947 and :950-:952**: :941 is the
section heading "## The retention fixed point"; **(CT2)** is the tag at **:947**
(display :945-948); the monotonicity and greatest-fixed-point statement is at
**:950** and its proof at **:952**.

(ii) **Two further proved results, named without :1390's protection.**
Equivariance under genuine recoding (**statement :1202**, proof :1204, scope
limit :1206) and the projection theorem (**heading :1208; statement :1210-1218**,
proof :1220, instance :1222, scope limit :1224) are proved results that A001
does not challenge. **They carry no :1390 tag**, and v1's sentence putting them
inside :1390's protected list was wrong.

(iii) **The declared-input boundary for normative and physical content**
(:1384-1386, :902): a complaint that FW5 does not derive \(\mathcal N\) is not a
counterexample, because FW5 states the dependence rather than concealing it.
**Measured, pointer corrected at this revision (F64):** the display
\(\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A\) is at
**:893**; :896 is the prose that follows it. *v3 cited :896 for the display; that
is the pointer defect §2's own rule forbids, and it is fixed here and in §5(b).*

---

## 2. Primitive dependencies, marked

**Interpretation** throughout this table; the FW5 lines are Measured.
"Defined" = the reading edition fixes it in declared mathematical data.
"Undefined" = the reading edition uses it as load-bearing without fixing it.
"Defined-but-unmapped" = fixed in the source, with no stated route from a
published record to it.

**Pointer discipline.** Where a cited datum sits inside a display, the row cites
the **content** line, not the `\[` delimiter or the section heading. Corrected at
v3: D1's `:85` → **:86**; (O) → **tag :106**; D2's `:117` → **tuple :120**, (Q)
→ **tag :131**; D5's `:166` → **tuple :167**; D14's → **tag :617**; D20's →
**statement :1210-1218**. **Corrected at this revision (F65):** D13's
`:738-746` → the content line \(d\equiv_\ell c\) at **:742**, **(N) tag :743**,
quoted sentence at **:746**; D18's `:642-651` → standing at **:638**, the
\(\operatorname{Live}_j\) definition at **:642**, **(K2) tag :650** (display
:644-650). Also corrected: the inexplicit-representation citation, which is at
**:859** ("partial, distributed, or temporally extended"), :857 being the
preceding paragraph.

| # | dependency | FW5 line | status | why |
|---|---|---|---|---|
| D1 | organization \(D=(V,(X_v),J,B,A,L,\mathrm{role})\); solutions (O) | :86; (O) tag :106 | defined | typed tuple; (O) is set equality |
| D2 | question \(p=(D,\Sigma,b_0,\kappa,\mathcal C,\mathcal Q,O_p)\); (Q) | :120, :123, :125; (Q) tag :131 | defined | typed tuple |
| D3 | respect \(\kappa\) | :123 | **undefined** | fixed by an open example list ("production, inferential identification, impossibility, rule-governed status, achievement of an aim, or aesthetic value"); no membership condition, no individuation of two respects |
| D4 | contrast contract \(\mathcal C\) | :123 | **undefined** | "distinctions **material to that question**"; materiality is the load-bearing word and is not defined |
| D5 | the maps \(\pi,\tau,\sigma,\lambda\) with declared domains | :167, :170 | defined | declared data; many-to-one permitted for \(\pi\); ":170 Their meanings are held fixed across the comparison" |
| **D6** | "the declared abstraction" at which the projected target relation must equal the explanatory component relation | :176 | **undefined** | **the abstraction is a free declaration; no condition ties an admissible abstraction to \(\kappa\).** :176 s1 restricts what the *port translation* may depend on ("only on the ports of its anchored subnetwork and the explicitly declared boundary"); it does not restrict how coarse the *declared abstraction* of s3 may be, and no other line does. **:176 s5 is FW5's own statement of what the missing condition is for**: "Together with (F), which checks the assembled organization, this prevents local relation matches from silently losing constraints shared between components" — an effect s1-s4 do not deliver without an admissibility condition on the abstraction. See construction (γ) at §5(a)(i), recorded verbatim. **Second unconstrained input at the same locus, recorded and deliberately not given its own row:** the *component carving* is also free — the whole-network \(\lambda_w\) of §5(a)(i) satisfies :174 with a single component. |
| D7 | grain \(\ell\) | :154 | **undefined** | "A grain fixes which structural distinctions count as differences for the attribution at issue" — a stipulation; no admissibility condition relative to \(\kappa\) or \(\mathcal C\). Note :154 also constrains coarsening ("Coarsening is not automatically an isomorphism"; bundling "can change the answer to a question about individual contribution") but states no test |
| D8 | active commitments vs incidental remarks | :162 | **undefined** | "part of the interpreted claim"; no procedure, and FW5 explicitly forbids an assessor selecting fragments |
| D9 | (F), (C), (A) | tags :185, :194, :205 | defined | equalities and an indexing condition, all ranging over "the comparisons specified in \(\Sigma\cap\mathcal C\)" (:179, :199); (C) is restricted to "every composition **for which a claim is made**" (:188) and (A) "includes the respect \(\kappa\)" (:208) |
| D10 | non-circular dependence: the :210 contrast clause **and :212's third sentence** | :210, **:212 s3** | defined, on D4/D7/D8 | :210 requires "at least one admitted contrast that removes or changes a nonempty block of active organizational commitments … for which the answer profile changes or ceases to be determined in the claimed way". **:212 s3 — "A contrast family containing only notational variants, or one defined to exclude every change that could matter, does not meet non-circular dependence" — is printed under the Non-vacuity heading but its stated predicate is non-circular dependence; it is filed here.** Its inputs (what "could matter") are D4. **At the A-S locus this clause does no work (§5(a)(i)): the strict reading of "every" is correct, and the clause is kept in this row because the row is about the dependency, not about A-S.** |
| D11 | non-vacuity | **:212 s1-s2 only** | defined | "The baseline organization has a compatible state or history"; and an impossibility claim "may correctly assert that a specified goal has no compatible realization, but not infer a substantive result merely from an inconsistent baseline" |
| D12 | boundary \(\beta\), representation \(\operatorname{Rep}_{\beta,\ell}\) | :149 (display :148-150), :152, :156 | declared primitive | FW5 says so: ":156 The representation relation is an explicit semantic primitive" |
| D13 | structural equivalence at grain, \(d\equiv_\ell c\) | **:742** (content), (N) tag **:743**, gloss **:746** | defined, unmapped | ":746 The equivalence is structural at the stated grain, not string equality or similarity"; no record-level test |
| D14 | Bearing (K1): \(\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal E_c,p_\delta)\) | tag :617 (display :613-618), gloss :620 | defined, **mapping unsupported** | identifies criticism-bearing with accounting; the route from an authored criticism to \(\mathcal E_c\) is not stated. **:620 s2 — "The alleged defect must concern the stated target and respect" — is a stated side condition and is carried into §3 as a constraint on A001's own bridge (F59).** The survey of every other bearing locus is at §5(b) and is stated as a survey, not as a universal. |
| D15 | criticism constituents \(z,\delta,g\), connection | :609 | defined | four-part; ":609 A defect is a specified failure condition on the target or its application", whose **first named kind is inconsistency** |
| D16 | active route; nonconstant dependence on the represented distinction | :601 | defined, unmapped | requires actual occurrences, ports, component relations; "not inferred from the presence of a similar sentence in a record" |
| D17 | reason-use witness and its three-case contrast contract | :628, :630 | defined, unmapped | ":628 The map must preserve internal role bindings, not merely the endpoint string"; C001 PLAN §9 records that a transcript supplies none |
| D18 | standing \(\operatorname{Live}_j\), (K2) | **:638** (standing), **:642** (definition), **(K2) tag :650** | defined, unmapped | appraisal-indexed; FW5:640 — prompt appearance is a delivery fact, actual use is "not automatically machine-maintainable" |
| D19 | repair (P) with \(O\), \(P\), \(\operatorname{ProducedBy}\) | :787-800 | defined, unmapped | not challenged here; named because (EK) carries Account |
| D20 | reading Account off an output projection | :1210-1218, with :1220-:1224 | **unavailable by FW5's own theorem** | ":1218 no function of \(P(M)\) alone agrees with the accounting predicate on both models"; ":1222 … when the projection retains only endpoint values and the question concerns the active route"; ":1224 The theorem identifies missing information in a projection" — and see §5(a)(i) on what the theorem does **not** say |
| **D21** | **A001's own `bearing`→\(\kappa\) bridge** | — (not an FW5 dependency); constrained by **:620 s2** | **A001's declared mapping, criticizable, and NOT independent of the cells** | none of the ten golden `bearing` fields names a respect in :123's sense; the bridge rule is declared in §3 with its provenance disclosed and its per-cell assignment frozen, and an adverse cell charges the bridge before it charges anything of FW5's |
| **D22** *(new, F51)* | **\(\operatorname{Ans}_E\): how a candidate's answer profile is arrived at** | **:162**; (Q) **:128-130**; **:125**; **:210 s1** | **undefined** | **Measured: `\operatorname{Ans}_E` occurs in the reading edition at exactly two lines, :162 and :202** (the second inside (A)'s display :201-205). **:162 makes it supplied by the candidate** — "An explanatory candidate for \(p\) **supplies** an organization \(E\), an answer profile \(\operatorname{Ans}_E\), and an interpretation of its active commitments." **(Q) at :128-130 defines only \(\operatorname{Ans}_p(a,b)=\mathcal Q(D,a,b)\)**, over the **target** \(D\). **:125 says \(\mathcal Q\) is "a specified set-theoretic operation on the relevant organization"** without saying which organization is the relevant one for a candidate. **No line states \(\operatorname{Ans}_E=\mathcal Q(E,\cdot,\cdot)\).** The one line saying how a candidate's answer is arrived at is **:210 s1** — "The answer follows by evaluating **the anchored organization** under its declared independent boundary conditions" — and **"the anchored organization" is not a defined term of the edition**; it admits at least two readings (the explanatory organization taken under its anchoring; the target subnetwork that \(\lambda\) names), and no line fixes which. **A second locus makes the same gap visible: :197 says "Equations (F) and (C) are applied at the stated abstraction and scope" and names neither (A) nor \(\mathcal Q\)** — so whether the query is evaluated at the declared abstraction is itself D6/D7. **Consequence, stated once and carried:** any disposal of a case at (A) must name which reading of \(\operatorname{Ans}_E\) it uses. §5(a)(i) horn 2 does so. |

**Note on the realization conditions.** The conditions FW5 defers to its
constructor section are at **:989-991**. :995-1012 is the Marletto/CTK material
and is a different subject.

**The one published mapping candidate.** The C001 correspondence table
(`experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md`, sha256
`dcaebaf8336c1943700a762b4836679307349d6ff8dfad082e4cd77e23fd7ae7`) is a
proposed, checkable instance of D13 for one criticism document. **Measured:** it
carries **85 units in two arms** — the `fcl` arm (source `mini_fcl`) has **50**
(28 `B.*` body units + 22 `K.*` record-field units), the `prose` arm (source
`mini_prose`) has **35** (20 `B.*` + 15 `C.*`). **The 22 `K.*` units cover eight
records of the objection document — `o1`, `o2`, `o3`, `o4`, `c1`, `c2`, `p1`,
`u1` — and of those only `o1`, `o2` and `o3` carry a referring row in the golden
use table.** **Only the fcl arm's 50 units bear on E2.** A001 uses the table as a
*candidate* mapping and tests it; it does not assume it.

---

## 3. Grain, boundary, contrasts — and the bridge, with its provenance disclosed

Declared under `docs/SEMANTIC_GUIDE.md` "Declare the interpretation before the
evidence" and FW5:728 ("Fix a system boundary, grain, history, and continuity
criterion before assessing an event").

### Disclosure, first

* **Both corpora were read before the rule was written.** The ten golden
  `bearing` fields *and* all 23 F001 `bearing` fields were read first.
* **Four of the branches paraphrase cells they will be applied to — not two.
  Corrected and extended at this revision (F57). Measured, at the bytes:**
  * **(b3)** — "does work its stated evidence does not carry" — paraphrases
    golden rows 3 and 4 verbatim: "The ordering of the account's recommendations
    is doing prescriptive work that the stated evidence does not carry."
  * **(b2)** — "treats one reading as **the frame**" — was tuned on F001
    occurrence-01 rows 0-3: "counters treating c1 and c2 as **the frame** rather
    than as one hypothesis among at least two". **(b2) matches zero golden
    cells.**
  * **(b1)'s second limb** — "or has **less discriminating power** than the
    target claims" — paraphrases golden row 2: "the test has **lower
    discriminating power** than the account implies". *v3 disclosed (b1) as
    unfitted; that was false and is corrected here.*
  * **(b4)** — "asserts only that **a reader will misread** the target" —
    paraphrases golden rows 16 and 17: "**If a reader takes k2 at face value**
    and does not read k7 as limiting it, the probe will be **over-read** as a
    test of the unit-versus-privacy axis." *Also not disclosed at v3.*
  * **(b6)** is written from :609's own defect list, but its stated example —
    "(e.g. 'alleges an internal inconsistency between …')" — **is the `bearing`
    text of F001 occurrence-01 rows 4, 5, 6, 20, 21 and 22 verbatim**. It is
    fitted too, and is disclosed as fitted at this revision.
  * **(b7)** is the one branch written from :609 without a cell in view, and it
    fires on nothing.
* **Consequence, pre-declared:** D21 is **not independent of the cells**, P8
  records it, and **no outcome of the executable leg may be reported as a test
  of the bridge's independence or as a confirmation of the bridge.** The bridge
  can only be *charged*, never *supported*, by this leg.
* **Consequence, second:** because the rule is post-hoc with respect to the
  cells, the **branch assignment for all 33 cells is frozen now**, in
  `CELLS-v4.md`, before the reading step. No cell may be re-assigned after a
  reading, and a cell whose assignment a reader contests is X4, not re-branched.

| item | A001 declaration |
|---|---|
| **unit that counts as a case** | Prose legs: one fully specified \(\mathcal E=(E,p,\pi,\tau,\sigma,\lambda)\) with its target organization and question, **written out in this document**. Executable leg: one **record carrying a non-empty `bearing` field** **together with one declared target record**, i.e. one row of a published use table. The `type: "objection"` disjunct of v1 is **dropped as a separate criterion** and becomes a **sub-register label**. Not a document, not a node, not a cell of C001. |
| **grain \(\ell\)** | the FCL-1 record keyed by id, with its `text`, `scope`, `grounds`, `bearing`, `action`, `consequence` fields and its ref arrays retained; ids and prefixes retained. This is C001's own declared grain (C001 PLAN §10) and the use-relation instrument's own subject definition. If it is changed later the claim changes with it (**FW5:140** — "What is prohibited is changing it during an assessment without recording the resulting change in what is claimed"). |
| **boundary separating the studied system from its inputs** | The studied system is the **criticism content** and the **target content** as published bytes. Outside it: the model, the endpoint, Mini's graph, the scheduler, the store, the operator-supplied FCL-1 language, the H005 instructions, the decoder, the importer and the use-relation instrument. A001 makes **no attribution to any model or endpoint**. |
| **respect \(\kappa\), and the bridge that supplies it (D21)** | **Measured:** all ten golden `bearing` fields are consequence-if-true clauses (e.g. golden row 2, `o2`→`c2`: "Weakens the claim that falling recurrence would confirm c1 and rising recurrence would refute it; the test has lower discriminating power than the account implies"). **None names a respect in :123's sense.** So \(\kappa\) cannot be "quoted verbatim from the record". A001 therefore declares the bridge rule below, declares its provenance above, and declares that the bridge is **A001's own criticizable contribution (D21)**, not a reading of FW5. |
| **why a bridge rather than "unresolved by construction"** | The round-1 reviewer's alternative — declare the whole leg unresolved by construction — is available and is recorded as such. It is not taken, because it ends the leg without producing anything checkable, whereas a declared, published, pre-registered bridge is a separately identified gap-filling contribution of the kind PURPOSE.md requires. **Consequence, pre-declared: an adverse cell charges D21 before it charges D14, and D14 before anything of FW5's** (§5(b)). |
| **contrast used** | Account's own contrast *requirement*, **FW5:210** with **:212 s3** — at least one admitted contrast removing or changing a nonempty block of active organizational commitments of the target, with the answer profile changing or ceasing to be determined; and the family must not consist only of notational variants nor be defined to exclude every change that could matter. **Not** FW5:630's three-case contract. **This declares the requirement, not a family: the concrete contrast family for a given cell is a per-cell declaration and is subject to the free-declaration test of §5(b).** |
| **FW5:630's three-case contract, where it does enter** | only in leg E2, and only as a check on D13. C001's registers T/E/D/G are reason-use registers; A001 does not fill them, does not reuse their marks, and does not read an Account result off them. |
| **history / continuity** | none claimed. A001 compares contents, not episodes. |
| **normative relation invoked** | none. No merit, adequacy-of-the-model, or progress predicate is applied to any model or output. |
| **enabling contributions** | FW5 itself, the FCL-1 language, the H005/F001 material and instructions, the two published instruments, the C001 recoding table. |

### The bridge rule (D21), first match wins, applied to the `bearing` text alone

**Match test, declared strictly:** a branch fires only where the `bearing` text
**explicitly asserts** that branch's stated form. A text from which the branch's
form must be *inferred* by the reader does **not** fire it; it falls to (b5).

**The conditional rule, declared at this revision because three frozen
assignments turned on a question v3's match test did not answer (F58).**

> A branch's form counts as **explicitly asserted** only where the `bearing`
> text asserts it **outright**. A form stated **solely inside the antecedent of
> a conditional**, or **solely inside the consequent of a conditional whose
> antecedent the same `bearing` text does not itself assert**, is **not** an
> explicit assertion. **A conditional whose antecedent the text does not assert
> fires no branch.** "Unless P, Q" is a conditional for this purpose.

**Why this rule and not its negation.** v3 already disqualified A01/A02 as "a
conditional, not a rival asserted to be on the table" and A24 as "a conditional
re-ordering demand", while branching A06-A08 and A09/A10 on forms that sit
inside conditionals. Exactly one of the two treatments can stand. A001 takes the
one that **fires fewer branches**, because the alternative would move eight
further cells into a respect on the strength of hypotheses their own texts do
not assert, and because a `bearing` that says "*if* the test cannot distinguish
those, …" has not alleged that the test cannot distinguish those. **Measured
consequence: five cells move out of a respect and into unresolved** (A06, A07,
A08 from (b1); A09, A10 from (b4)). **Nothing moves the other way.** All 33
cells were re-verified against the rule at the bytes, not re-derived from v3.

**The :620 constraint on D21, declared here (F59).** FW5:620 — "**The alleged
defect must concern the stated target and respect.**" The bridge supplies
\(\kappa\) from the `bearing` field alone, while **Measured
(`docs/reviews/fw5-vs-harness-spec-2026-09-14.md`:299): "(i) No \(\delta\) slot
— the defect lives in free `text`".** So the bridge can supply a respect that
does not concern the record's own alleged defect, and :620 is the stated clause
that makes that a defect **of A001's bridge**, not a curiosity. It is therefore
a pre-declared check in the reading procedure (§5(b), "the :620 check"), with a
named class and a named charge, rather than something left to a reader's
discretion. *v3 treated the `text`/`bearing` split only as a fitting risk.*

| order | branch | condition on the `bearing` text | \(\kappa\) supplied | source of the respect |
|---|---|---|---|---|
| 1 | **(b1) DISCRIMINATION** | explicitly asserts that the target's test, evidence or inference **cannot distinguish** two or more stated readings, or has **less discriminating power** than the target claims | **inferential identification** | :123's list |
| 2 | **(b2) RIVAL-FRAME** | explicitly asserts that the target treats one reading **as the frame** while at least one rival is on the table | **inferential identification** | :123's list |
| 3 | **(b3) PRESCRIPTION** | explicitly asserts that the target's recommendation, ordering or prescription **does work its stated evidence does not carry** | **achievement of an aim** | :123's list; the aim is the one the target's own recommendation states |
| 4 | **(b6) INCONSISTENCY** | explicitly alleges that **two or more of the target's own commitments cannot jointly hold** | **impossibility** | :123's list; :609 names **inconsistency first** among defect kinds; :212 s2's "no compatible realization" is the same shape |
| 5 | **(b7) MISSING-DISTINCTION** | explicitly alleges **a distinction the target does not draw** and needs | **inferential identification** | :123's list; :609's "a missing distinction" |
| 6 | **(b4) MISREADING** | asserts only that **a reader will misread** the target | **inferential identification**, cell flagged `bridge-strained` | :123's list |
| 7 | **(b5) UNRESOLVED** | otherwise | **none** | — |

**Pre-declared consequence of (b5): the cell is X4 UNRESOLVED and is read no
further.** It supplies no evidence on any side.

**Measured, at this revision, with the branch assignment frozen in
`CELLS-v4.md`** — reported as a **coverage fact about A001's own bridge, never
as evidence about FW5, about the records, or about their authors:**

| branch | cells | which |
|---|---|---|
| (b1) | **1** | golden 2 |
| (b2) | **4** | F001 occ-01 rows 0, 1, 2, 3 |
| (b3) | **2** | golden 3, 4 |
| (b6) | **6** | F001 occ-01 rows 4, 5, 6, 20, 21, 22 |
| (b7) | **0** | no cell matches it |
| (b4) | **0** | **no cell matches it under the conditional rule.** Golden 16 and 17, on which (b4) was fitted, are conditionals whose antecedent their texts do not assert |
| (b5) | **19** | golden 0, 1, 10, 11, 13, 16, 17; F001 occ-01 rows 7, 8, 12, 19; occ-05 rows 3-10 |
| *(bridge not consulted)* | **1** | F001 occ-07 row 1 — **X0 fires on the absent target record id before the bridge is consulted**, so this cell is not a (b5) return and is not counted as one (F60) |
| | **33** | |

**So 13 of 33 cells reach a respect; 19 are X4 before the reading and one is
X0.** *v3 reported 18 and 15, with the X0 cell wrongly inside (b5).*

**The strongest available charge against A001's own bridge, recorded here
because no reading step can produce it (F57).** **Measured, after the
conditional rule:** every branch that fires at all fires **only** on cells whose
`bearing` text that branch's own condition paraphrases — (b1) on golden 2 alone,
whose "lower discriminating power" its second limb restates; (b3) on golden 3
and 4 alone, which it restates verbatim; (b2) on F001 occurrence-01 rows 0-3
alone, on which it was tuned; (b6) on the six cells whose `bearing` is the text
its own stated example quotes. **(b4) and (b7) fire on nothing.** **A001 records
this and does not repair it by loosening a branch**: loosening a branch until it
catches a cell is the fitting §3 has already had to concede. **Interpretation:**
this is consistent with the bridge having no reach beyond the sentences it was
written from, and a fourth reviewer should attack D21 here first.

**Assignments recorded against earlier revisions, because a reader would
otherwise expect the other answer.**

* **Golden rows 0 and 1 are (b5).** Their `bearing` — "If the driver is
  renegotiation or legitimacy rather than ambiguity, the specification move in
  c2 treats a symptom, and the account's sequencing (chores first, relationship
  later) is misplaced" — is a conditional whose antecedent it does not assert,
  and "misplaced" is in any case weaker than (b3)'s "does work its stated
  evidence does not carry".
* **Golden rows 10, 11 and 13 move from (b1) to (b5) at this revision.** Rows 10
  and 11: "**If** the opening question itself triggers withdrawal, the rival's
  own distinguishing observation is contaminated: you cannot tell
  pullback-from-the-idea from pullback-from-a-heavy-question" — the
  non-distinguishability sits in the consequent of an unasserted conditional.
  Row 13: "**If** pullback-from-form cannot distinguish those, the test is
  weaker than k2 suggests, and the honest state is that neither reading is being
  confirmed" — the non-distinguishability sits in the antecedent.
* **Golden rows 16 and 17 move from (b4) to (b5) at this revision.** "**If** a
  reader takes k2 at face value and does not read k7 as limiting it, the probe
  will be over-read" — an unasserted conditional. **This empties (b4).**
* **B01 (F001 occ-01 row 12) is (b5) and therefore X4.** Its admission to the
  register rests on its non-empty `bearing`; but the bridge reads the `bearing`
  **alone**, and that field — "narrows the commitment to a cost rule with an
  explicit scope, rather than a trigger condition" — alleges no defect and
  matches no branch. **B01 is retained in the register as a datum about the
  `type` field and is pre-declared unreadable by this leg.** Extending the
  bridge to `text` was considered and **declined**: it would re-open the fitting
  problem on a second field.

---

## 4. What a counterexample would require FW5 to relinquish

**If Claim S falls** (a fully specified \(\mathcal E\) with all five conjuncts
true at a defensible \(\ell\) and \(\kappa\), meeting :1364's four qualifiers,
which is not an explanatory account of its target): the repair is a sixth
condition, and the only candidates are (a) a further substantive structural
condition, (b) a primitive of the kind banned at :37 (`Because`,
`ExplanatoryWork`), or (c) an admissibility condition on
\(\ell,\kappa,\mathcal C\) that the reading edition does not state.

**The relinquishment is conditional on which repair is taken.**

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
  kind and defers rather than refutes. **D6 and D22 are of this kind and are not
  counterexamples of any kind.**

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

**What no counterexample here can require.** FW5:1392 — "A physical or semantic
counterexample to an application can defeat that application without changing
the model-class definition." FW5:688 — "The inability to evaluate a proposition
is not a falsifying observation of the proposition." FW5:1404 — "No experiment
established the class's adequacy as a theory of human or artificial creativity.
The validation boundary is mathematical construction checking, not semantic
certification." *v1 cited :1336-1344 for this; that section concerns one
supplied audit of executable spec 0.2 against the packet's 0.1, and :1342 cuts
the other way. The citation is withdrawn.*

### Three different findings, kept apart

1. **A missing definition** (**D3, D4, D6, D7, D8, D22**, and the materiality
   input of D10). Shows that (E) is not yet determinate for a given (target,
   question) pair: a claimant can make (E) true or false by a free declaration.
   This **defers** both S and N; it refutes neither, and it must not be reported
   as a counterexample. Its remedy is a separately identified gap-filling
   proposal (§5(c)), which must not be back-fitted to whatever the evidence
   turns out to be. **D22 is added at this revision and is the one finding of
   this kind that §5(a) itself now reaches** (§5(a)(i) horn 2).
2. **An unsupported mapping** (D14, D16-D18, D20, D21, and D13 if the C001
   recoding table fails its own content-preservation argument). Shows that a
   bridge from published records to an FW5 relation is unwarranted. It defeats
   the application, not the class (FW5:1392). It is the finding the executable
   leg can actually reach (§5(b)).
3. **An operational failure. Measured:** the `deepseek-flash` × `fcl` cell of
   C001 occurrence-01 has **19 of its 20 coordinates unusable at the 8192
   ceiling — 8 PARTIAL at `finish_reason` "length" with `completion_tokens`
   exactly 8192, and 11 FAILED with `NO_PUBLIC_CONTENT`** — read off
   **`experiments/diagnostics/C001-contrast-triple/occurrence-01/COMPARISON.md`**
   (the table at lines 38-57, "Unresolved in this cell" at line 59; **two
   `COMPARISON.md` files exist under that study and this is the occurrence-01
   one**). The "8 PARTIAL … 11 FAILED … **and no usage**" wording is at
   `material-occurrence-02.json`:1519. **The "no `finish_reason`" half is not at
   that line**: it is at
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
below, with a fourth clause added at this revision (F61).** For any authored
case:

> **(r1)** If FW5 supplies any **stated clause** excluding the case, the case
> **fails**, and the finding is neither finding 1 nor a counterexample. The
> report names the clause at the line.
> **(r2)** If the only reply available to FW5 is a **condition the reading
> edition does not contain**, the finding is **finding 1** (a missing
> definition), and the missing condition is named exactly.
> **(r3)** A **counterexample** requires that no stated clause and no candidate
> gap-filling condition excludes the case, **and** that it meets all four of
> :1364's qualifiers (q1)-(q4).
> **(r4)** *(new)* **Otherwise** — no stated clause excludes the case, no
> gap-filling condition is needed, and the case fails one of (q1)-(q4) — the
> case **fails on the named qualifier of :1364 and yields no finding**. The
> report names the qualifier and quotes it.
> No case may be upgraded after the argument is examined. This rule is fixed
> before §5(a)(i) and §5(a)(ii) are read.

**Proviso.** **No entry in §2 is derived from a case's outcome.** The dependency
table is a reading of FW5's own text and stands or falls on that text alone.
**D22 is added to §2 from :162, :125, (Q) :128-130 and :210 s1 directly, not
from how Case A-S goes**; that a case then turns on it is a consequence, not the
warrant. *The round-2 reviewer's alternative — amend (r1) to permit a case to
yield a missing definition "provided it is stated as a property of the
dependency" — remains **declined**, for the reason given at v3: it re-opens the
upgrade path (r1) exists to close, and it is unnecessary once the D-row is
derived from the source.*

#### 5(a)(i) Case A-S (sufficiency) — **FAILS, and the reason is now stated conditionally**

*The candidate.* FW5's own discriminating pair, introduced at :1222 and checked
by exhaustive enumeration at :1402 ("All four Boolean input assignments were
checked for the parallel and priority constructions. Their endpoint outputs
agree, while the active second route differs when both inputs are on").

**The candidate written out.**

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
  worked separately below.

**Horn 1 — \(\kappa\) = production of the endpoint output.** \(\mathcal Q\)
returns the produced value of \(o\).

* (A) **holds**: \(\operatorname{Ans}_E\) and \(\operatorname{Ans}_p\) are the
  same function of the four assignments (:1402) under either reading of D22, and
  :208's "This includes the respect \(\kappa\), not just a matching number" is
  satisfied, because the declared respect asks for the produced output value and
  nothing else.
* (E)'s other conjuncts can be made to hold — and it **does not matter**,
  because **the attribution is then true**. "\(E\) accounts for the target's
  production of the output", where the declared question's answer profile *is*
  the endpoint output function, is correct. **Nothing false is shown.** FW5:236
  licenses exactly this: "Explanatory depth is question-relative… Equation (E)
  is not a universal measure of elegance or merit."
* Against :1364: the four qualifiers govern a candidate *satisfying (E)*, so
  they are reached here. **The case looks adverse only if the reader switches,
  after the fact, from the endpoint question to the route question**, which is
  the move `FW5-research-plan-decision.md` forbids ("must not be repaired away
  by silently changing the question, grain, boundary or anchors after the
  failure"). **Stated precisely (F66): the candidate does not fail (q2)** — it
  preserves the endpoint question throughout, and \(\mathcal Q\) is unchanged.
  **What switches is the challenger's complaint, not the candidate's question.**
  (q1) is true of the question actually asked; **(q3) survives** on the strict
  reading of :212 s3 below; (q4) is not at issue. Horn 1 therefore terminates in
  **no finding**: the attribution is true and nothing false is exhibited.
* **v1's sentence "the attribution … is nevertheless false of the target when
  both inputs are on, and FW5's own theorem at :1208-1218 is the reason it is
  false" remains WITHDRAWN.** :1218 says only that "no function of \(P(M)\)
  alone agrees with the accounting predicate on both models" — a claim about a
  projection's information, not about the falsity of an attribution. Worse for
  the case: the theorem's hypotheses are \(M_0\models\phi\) and
  \(M_1\not\models\phi\) (:1214-1215), i.e. **it presupposes that the accounting
  predicate distinguishes the parallel and priority models**, which is the
  reverse of what A-S needs. :1224 confirms the scope.

**Horn 2 — \(\kappa\) concerns the active route.** This is the horn :1222 pins
the construction to: "Parallel and priority wiring provide a concrete instance
**when the projection retains only endpoint values and the question concerns the
active route**". \(\mathcal Q\) returns which routes are active.

**The premise the disposal needs, named and quoted, because the reading edition
does not supply it (F51).**

> **(P-Ans) — A001's premise, not FW5's text.** A candidate's answer profile is
> the query operator applied to the **candidate's own organization**:
> \(\operatorname{Ans}_E(a',b')=\mathcal Q(E,a',b')\). Under (P-Ans),
> \(\operatorname{Ans}_E\) is a function of \(E\) and the declared question and
> **not** of \(\lambda\).

**Why (P-Ans) is A001's and not FW5's. Measured.** `\operatorname{Ans}_E`
occurs in the reading edition at exactly **:162** and **:202**. :162 —
"An explanatory candidate for \(p\) **supplies** an organization \(E\), an
answer profile \(\operatorname{Ans}_E\), and an interpretation of its active
commitments" — makes it supplied, not computed. (Q) at :128-130 defines only
\(\operatorname{Ans}_p(a,b)=\mathcal Q(D,a,b)\), over the **target**. :125 makes
\(\mathcal Q\) "a specified set-theoretic operation on the relevant
organization" without fixing which organization is relevant for a candidate.
**No line states \(\operatorname{Ans}_E=\mathcal Q(E,\cdot,\cdot)\).** This is
§2's D22, and it is undefined there on the text, not on this case.

* **Under (P-Ans): (A) Question fidelity fails, at :208, under every
  \(\lambda\).** With both inputs on, \(\operatorname{Ans}_p\) is "route 1 alone
  is active" and \(\operatorname{Ans}_E\) is "routes 1 and 2 are active"
  (:1402). (A) at :205 equates \(\operatorname{Ans}_E(\tau(a),\sigma(b))\) with
  \(\operatorname{Ans}_p(a,b)\) over the comparisons in \(\Sigma\cap\mathcal C\),
  and :208 makes the respect part of what must match. No choice of anchoring
  changes which routes the parallel organization makes active, so the case is
  over at :199-208 before any other conjunct is consulted. **This whole bullet
  is an Interpretation conditional on (P-Ans).**
* **Without (P-Ans), the case is not disposed of at :208, and A001 records the
  construction that shows it (F51, recorded verbatim from `REVIEW-3.md`):**

  > take \(\lambda_w\), which §5(a)(i) itself certifies ("Anchoring and (F) hold
  > at endpoint grain, with no coarsening at all") — \(E\) as one component
  > anchored to the target's whole network as one subnetwork. Evaluate the
  > active-route query on *the anchored organization*, as :210 s1 directs: that
  > organization is the target's whole network, so
  > \(\operatorname{Ans}_E(\tau(a),\sigma(b))=\operatorname{Ans}_p(a,b)\) on all
  > four assignments and **(A) holds under \(\lambda_w\)**.

  and the second route to the same place:

  > :197 says "(F) and (C) are applied at the stated abstraction" and names
  > **neither (A) nor \(\mathcal Q\)**, so whether the query is evaluated at the
  > declared abstraction is exactly **D6/D7**, which §2 marks *undefined*.

* **A further reading, recorded and NOT relied on. (Interpretation.)** :210 s2
  — "The target answer is not an unanalysed boundary input or a copied target
  assertion among its premises" — is the clause a reply would engage against the
  \(\lambda_w\) construction, since under it the candidate's answer is read off
  the target's own network. **A001 does not rest the disposal on it**, because
  whether evaluating the anchored organization under \(\lambda_w\) is "copying
  the target assertion" is itself undetermined at D22 and :210 s1, and using it
  here would re-close at (r1) a case that (r1) cannot reach. It is listed in §8
  as a place to attack this document.

**Disposition of Case A-S, stated by horn and by reading, and shrunk
accordingly.**

| horn | reading | clause | outcome under §5(a)'s rule |
|---|---|---|---|
| **1** (production) | either reading of D22 | **:236**, with :208 satisfied | the attribution is **true**; nothing false is exhibited; **no finding**, and no qualifier of :1364 is failed by the candidate |
| **2** (active route) | **under (P-Ans)** | **:208** alone | **(r1): the case fails.** Not a counterexample, not finding 1 |
| **2** (active route) | **without (P-Ans)**, on :210 s1's "the anchored organization" | **none available in the edition** | **(r2): finding 1.** The missing condition, named exactly: *a stated rule fixing how a candidate's answer profile \(\operatorname{Ans}_E\) is arrived at — in particular whether the declared query is evaluated on the candidate's own organization or on the anchored target subnetwork — and at which abstraction (:197 names only (F) and (C))* |

**And under neither reading is Case A-S a counterexample.** (r3) requires that
**no candidate gap-filling condition** exclude the case. **(P-Ans) is exactly
such a condition, it is available, and under it the case fails at :208.** So
(r3) is not met on either reading, and the ceiling of §6 is unchanged: **A001
offers no counterexample to sufficiency.**

**What this costs and what it buys, stated plainly.** It costs v3's sentence
that (A) fails "for every \(\lambda\)" as an unconditional claim: that sentence
is **withdrawn** from §0, from here, from §6 and from the receipt, and survives
only as an Interpretation conditional on a premise A001 supplies. It buys one
**finding 1** the prose leg can actually record — **D22** — reached by (r2) on a
line of the edition rather than by an argument about a case. **Case A-S is still
recorded as a failed sufficiency candidate**, alongside the skew-matrix one, and
its value is still negative and bounded.

**Every sentence claiming that Anchoring defeats A-S remains deleted.** v2 wrote
that "Anchoring fails as well, on the clause :176 states", that the (α)/(β)
dilemma shows "**no endpoint-level abstraction satisfies Anchoring** for a
two-route organization whose routes are the anchored components", and that
"neither does any endpoint-level abstraction of FW5's own discriminating pair".
**All three are withdrawn.** The two subsections below record why.

##### Why the Anchoring argument fails: the omitted case (γ)

v2's dilemma had two horns — **(α)** an abstraction coarsening only the
assembled organization's ports, and **(β)** one coarsening each component's
relation down to assembled endpoint values, excluded by :176 s1 as a matter of
what the *anchoring data* may depend on. **The enumeration is not exhaustive.**
:176 s1 restricts what the **port translation** may depend on; it says nothing
about how coarse the **declared abstraction** of s3 may be, and no other line
fixes that. The round-2 reviewer's third case is recorded **verbatim**:

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
**D6 stands as undefined (§2).**

What (α) and (β) still show, and all they show: **two natural abstractions
fail.** That is kept, and it is not a universal.

##### The whole-network anchoring \(\lambda_w\)

> Carve \(E\) as **one** component — the whole parallel network — anchored to
> the target's whole network as one subnetwork. :174's "Every active explanatory
> component has a stated target interpretation under \(\lambda\)" then has
> exactly one instance. That subnetwork's relation, obtained by imposing its
> component constraints and projecting away its hidden ports as :176 s3 itself
> prescribes, **is** the endpoint relation; by **:1402** ("Their endpoint
> outputs agree") it equals the explanatory component relation at the endpoint
> abstraction. The port translation depends only on that subnetwork's endpoint
> ports and the declared boundary, so s1 is met. **(F) at :185 holds over
> \(\Sigma\cap\mathcal C\) at endpoint grain by the same enumeration.** So
> **Anchoring and (F) hold at endpoint grain, with no coarsening at all.**

\(\lambda_w\) is why §2's D6 row records the *component carving* as a second
unconstrained input at the same locus — **and, at this revision, it is also the
anchoring under which the D22 construction above makes (A) hold.** A001 does not
get to certify \(\lambda_w\) in one paragraph and ignore it two paragraphs
later; that was v3's defect and it is what F51 caught.

##### The :212 s3 reading, upheld

A001 read :212 s3 — "or one defined to exclude **every** change that could
matter" — strictly: as \(\forall x(\text{could-matter}(x)\to\text{excluded}(x))\),
so that a family admitting **one** mattering change escapes the clause. A-S's
endpoint-level family excludes the gating change but still admits deleting the
block of both routes, which changes the answer profile under either respect.
**Two reviews upheld this reading**, on the ground that the second disjunct then
has the same shape as the first ("containing only notational variants"), as a
near-synonymous pair should. So:

* **F2 was wrong on the clause** and right that v1 ignored it. That is recorded
  here rather than absorbed.
* **Consequence for D10:** the row **keeps** :212 s3 — the clause's stated
  predicate really is non-circular dependence — and **the clause does no work at
  this locus**. D10 is a statement about the dependency, not about A-S.
* **Consequence for A001's size: none either way.** Under the loose reading A-S
  would fail at :210/:212 *as well as* :208 under (P-Ans), with the same
  published result, and without (P-Ans) the loose reading does not reach the
  \(\lambda_w\) construction either.

#### 5(a)(ii) Case B-N (necessity) — **DROPPED**

*The candidate, as staged in v1.* An inexplicit, distributed diagnostic
explanation of the kind FW5 admits at **:859** ("The realization can use a
partial, distributed, or temporally extended representation. Its relevant
bindings can be available through memory, imagery, action rehearsal, or
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
* **The disjunction v1 offered is unavailable.** :1364's necessity defeater is
  "A genuine explanation that cannot satisfy the conditions **under any
  interpretation** preserving its actual organization". (E) coming out true
  under one \(\lambda\) **satisfies** necessity. The "either necessity fails"
  disjunct is deleted. `FW5-research-plan-decision.md` says the same: "Failure
  of one selected encoding or grain is not that necessity result."

**Does anything remain that :1372 does not already say? No.** :1372 — "If they
exclude a genuine inexplicit or distributed understanding, it is too strong" —
already states the whole of B-N's residue. **B-N is dropped.** It is not carried
as a "possible counterexample" and not reclassified as finding 1, because the
missing condition it named (determinacy) is not owed.

**Branch, recorded.** :1372 sits under "Representation and apparent reason use"
(heading :1370), not under :1362's "A structural account that still does not
explain", and `FW5-research-plan-decision.md` files representation/integration
as a distinct attack branch. Dropping B-N removes the misfiling; the branch
stays open and A001 does not work it.

**What a real necessity case would need, named so the gap is visible.** An
explanation whose **actual organization is independently attested** — not
stipulated in prose by the challenger — for which no \(\lambda\) over that
attested organization satisfies (E). Prose alone cannot supply the attestation.
A001 does not close that gap.

#### 5(a)(iii) What the prose leg leaves

Neither case is an independently sourced interpretive technical document; that
gap, named at the end of `docs/reviews/FW5-account-skew-matrix-challenge.md` and
again in the "Testing FW5 itself" row's deliverable (§0), stays open. **Two
recorded failures and one missing definition (D22) are the prose leg's whole
yield.**

### 5(b) Executable leg — a (K1)-mapping test over published records

No provider call. No new instrument. No cell of any published table is filled
by A001; A001 writes its own worksheet, whose rows cite published row ids.

#### The route problem, and the survey that replaces v2's universal

(K1), tagged at **:617**, reads
\(\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal E_c,p_\delta)\).
**Bearing is defined as Account.** v1's sufficiency condition — "the criticism
does not bear while (E) holds" — is therefore not a statement about Account at
all; it is the denial of a biconditional.

v2 then wrote that there is "**no second, non-Account route to Bearing anywhere
in the reading edition**". **That universal is withdrawn.** What replaces it is
a **survey, stated as a survey**, of every locus other than the definiens
itself. **Measured:** outside the compounds "obligation-bearing" (:800),
"information-bearing" (:912, :1005) and "standing-bearing" (:1320), which are a
different word, the term *bearing/bears* occurs at **:607, :614, :622, :773,
:896, :900, :1182**; :609 and :620 carry (K1)'s constituents and its side
condition without the term. **The eight loci besides the definiens (:613-618)
are these:**

| locus | what it says | does it supply a second route to \(\operatorname{Bearing}(c,z,p)\)? |
|---|---|---|
| **:607** | "## A criticism and its bearing" | **no** — a section heading |
| **:609** | "A criticism has a represented target \(z\), an alleged defect \(\delta\), grounds \(g\), and a proposed connection from \(g\) to \(\delta\) relative to a question. A defect is a specified failure condition on the target or its application: inconsistency, a false dependency, a missing distinction, an unsupported reference, a failed task, a misapplied rule, or another condition whose interpretation is supplied." | **no** — constituents and a list of defect kinds; it defines no bearing predicate over them |
| **:620** | "The alleged defect must concern the stated target and respect." | **no** — a side condition on \(\delta\). **It is, however, a stated constraint on A001's own bridge, and is applied as one (§3, and the :620 check below).** |
| **:622** | "A criticism occurrence can exist when (K1) is false… It can become grounds for a criticism when an organization represents how it bears on a target." | **no** — about occurrences and about what makes an adverse signal into grounds |
| **:773** | "The objection need not have actual bearing, and the response need not improve the situation." | **no** — asserts that bearing can fail; supplies no test for when it holds |
| **:893** *(display)* **/ :896** *(prose)* | the relation \(\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A\) is displayed at **:893**; **:896** says it "states that a reason **bears** on a work in an aesthetic respect" | **a different relation** — *normative* bearing, declared input data in \(\mathcal N\), not \(\operatorname{Bearing}(c,z,p)\). *v3 cited :896 for the display; corrected (F64)* |
| **:900** | "effects belong to \(\mathcal R\), purposes to \(G\), **normative bearing to \(\mathcal N\)**, judgments to appraisal events, and creative contribution to (G) and (EK). **None is defined as another.**" | **no, and it forbids the conflation**: the edition keeps \(\mathcal N\)-bearing separate by its own sentence |
| **:1182** | "**Critical bearing is accounting for the specified defect question.**" (in "Defined relations and dependence order", heading :1178) | **no** — see immediately below |

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

**Measured (P6(i), `docs/reviews/fw5-vs-harness-spec-2026-09-14.md`:299):**
FCL-1 supplies **no \(\delta\) slot** — "the defect lives in free `text`".
Therefore **\(\delta\) is supplied by an A001 reconstruction for every cell in
the register, without exception.** Two consequences are pre-declared:

* **The register as a whole already exhibits finding 2 against D14** — the route
  from a published criticism record to \(\mathcal E_c\) is neither stated by FW5
  nor supplied by the language. **That finding is recorded once, for the
  register, here, before any cell is read.** The reading step cannot strengthen
  it, cannot make it a counterexample, and cannot produce a second independent
  instance of it; 33 cells do not make it 33 times truer (rule 6 below).
* **Every cell's \(\mathcal E_c\) therefore contains at least one
  A001-reconstructed component by construction.** This is what makes an
  Account-alone charge **impossible rather than merely unexpected**, and it is
  why the charge table below has no such row.

**A second register-level record, declared here for the same reason (F53).**
**D3, D4, D7 and D12 are undefined or declared-primitive in §2, and §3 declares
\(\ell\), \(\beta\), the contrast *requirement* and — through the frozen bridge
— \(\kappa\) as this leg's constants.** **Declaring them constants does not make
them defined.** That they had to be declared at all is a finding-1 fact about
FW5's text, it is recorded **once, here, at the register level**, and it is
**not re-earned per cell**. What the per-cell test below adds is only whether a
*particular* declaration, varied within the range §2 leaves open, would have
changed that cell's reading.

**What the reading step can still add, and it is little:** per-cell records of
whether, once a reconstruction is exhibited, A001's declared observable and the
(E)-verdict on that reconstruction agree — i.e. **evidence about A001's own
bridges**, charged to D21 and D14. **It cannot reach an Account verdict, and no
row of its worksheet may carry one.**

**Modality.** "Satisfiable" is withdrawn. :1364 requires "a fully specified
candidate satisfying (E)" and :170 requires declared domains "held fixed across
the comparison". **Each worksheet row must exhibit one \(\mathcal E_c\) with
\(\pi,\tau,\sigma,\lambda\) and the question tuple
\(p_\delta=(D,\Sigma,b_0,\kappa,\mathcal C,\mathcal Q,O_p)\) written into the
row**, before any conjunct is marked, exactly as §5(a)(i) writes out A-S. **Note
what this does not mean:** no record in this register carries \(\Sigma\),
\(b_0\), \(\mathcal Q\) or \(O_p\), and supplying them is the reader's job under
this rule. **"The record does not carry it" is therefore never a reason to mark
a cell X3.**

#### The reading procedure, in the order a reader performs it

1. **Gate, before any reading.** A cell whose bridge returns **(b5)**, or which
   is in **E3**, is pre-declared **X4 UNRESOLVED** in `CELLS-v4.md`, **no reader
   is assigned to it**, and it supplies no evidence on any side. A cell with a
   record-level absence — in this register, no target record id — is
   pre-declared **X0**, likewise unread. **Measured: 19 cells are gated to X4
   and one to X0; 13 cells are read.**
2. **Exhibition.** Each of the two readers independently writes out
   \(\mathcal E_c\) and \(p_\delta\) in full, or records that no
   \(\mathcal E_c\) can be written and names the component.
3. **The :620 check (F59).** FW5:620 — "The alleged defect must concern the
   stated target and respect." Each reader records whether the \(\delta\) it
   reconstructed from the record's `text` concerns the \(\kappa\) the frozen
   bridge supplied from the record's `bearing`, and quotes both. **If both
   readers record that it does not, the cell is X4 and a charge to D21 is
   recorded against it** (charge table below). If they disagree, the cell is X4
   with no charge. Otherwise the cell proceeds.
4. **The two judgements.** Each reader records
   **J1** — "(E) holds on this \(\mathcal E_c\)" — and **J2** — "the alleged
   defect obtains of the quoted target passage" — as *holds* / *fails* /
   **undetermined**, each with the passage quoted.
5. **The free-declaration test**, below.
6. **Class assignment** by the ordered table, below. First match wins.

#### The free-declaration test, defined operationally (F53, F55)

**Declared constants of the leg**, fixed in §3 and `CELLS-v4.md` before any
reading, identical for both readers, and **not** free declarations: the grain
\(\ell\) (D7), the boundary \(\beta\) (D12), the contrast *requirement* (D4 as
declared in §3), and the respect \(\kappa\) delivered by that cell's frozen
bridge branch (D3 via D21). A reader may not vary them. Their being declarations
is recorded once at the register level, above.

**Per-cell declarations** are everything else a reader must supply to write out
\(\mathcal E_c\) and reach J1 and J2. In this register they include at least:
the reconstructed \(\delta\) (D14/D15); the selection of active commitments in
the target passage (D8); the declared abstraction (D6) and the component carving
at the same locus; the identification of the record's represented target with
the quoted passage (D13); the concrete contrast family, i.e. D10's materiality
input over D4; and **\(\operatorname{Ans}_{\mathcal E_c}\), how the candidate's
answer profile is arrived at (D22)**. **The test ranges over any §2 row marked
undefined, defined-but-unmapped, or declared primitive** — it is not an
enumerated six (F55).

**For each per-cell declaration \(d\), the reader records one of two values,
each with its required evidence written into the row:**

* **`free`** — the reader **writes out** an alternative \(d'\), admissible at
  the same §2 row (that is: the reader can name no line of the reading edition
  excluding it), under which **that reader's own J1 or J2 comes out
  differently**. The row records the §2 row, \(d\), \(d'\), and which judgement
  flips.
* **`not-free`** — the reader records **either** a quoted line of the reading
  edition that excludes every such \(d'\), **or** the sentence "searched, none
  exhibited", with what was tried. **The two are distinguished in the row**, and
  only the first is a record about FW5's text.

**X5 fires if and only if both readers record `free` at the same §2 row and each
writes out its own \(d'\).** Exactly one reader recording `free` is a
**disagreement** and the cell is X4. Neither recording `free` sends the cell on
to the four Boolean rows. **This is what two readers can disagree about**: one
exhibits a flipping alternative, the other quotes a line that excludes it.

**Why this is not the trivial test v3 had.** v3's X5 fired "only because a
reader supplied a free declaration", and since \(\kappa\) and \(\mathcal C\)
must be declared for every row, that was true of every cell — so X5 swallowed
the four Boolean rows and the leg could record neither agreement nor conflict.
**The test above does not fire on the fact that a declaration was made.** It
fires only on an **exhibited** alternative that **flips a judgement**, agreed by
both readers at the same row.

#### Pre-declared outcome classes — nine, first match wins, X4 the residue

Declared here, before any cell is read. **Rows 1-7 are conditions; row 8 is
"otherwise", and X0 is assigned at the gate.** Exhaustiveness is therefore
**definitional, not argued**: every read cell that matches no condition is X4.
What must be argued instead is the **opposite** — that rows 1-7 are each
reachable, so that X4 is not a dumping ground. That is the reachability table
below, which answers round 3's F52 at its own standard.

| order | class | condition | pre-assigned finding kind |
|---|---|---|---|
| *(gate)* | **X0 NOT-RECONSTRUCTIBLE** | a datum (K1)'s right side requires is absent from the **published record itself**, independently of any A001 reconstruction — in this register, **no target record id** (F001 occ-07 row 1, a `bare_label_ref` resolving only to the owning artifact) | **finding 2 at D14** — **one instance of the register-level finding already declared above; never a new or additional finding** |
| *(gate)* | **X4 UNRESOLVED** | the bridge returns **(b5)**, or the cell is in **E3** | **none.** The cell is not read |
| 1 | **X3 RECONSTRUCTION-FAILED** | **both** readers record that no \(\mathcal E_c\) can be jointly written out and **name the same absent component** of \((E,p_\delta,\pi,\tau,\sigma,\lambda)\). **Not** "the record does not carry it" — see the Modality note | **finding 2 at D21 and D14** — **one instance of the already-declared register-level finding, naming the absent component; never a second independent instance** (F67). **No counterexample language of any kind is permitted in this class** |
| 2 | **X6 UNDECIDABLE-DEFECT** | both readers exhibit \(\mathcal E_c\), the :620 check passed, and **both** record **J2** as *undetermined*, each quoting the passage that fails to settle it | **finding 2 at D21 and D14** — **one instance of the already-declared register-level finding**: the record did not supply a defect determinate enough for either side to be evaluated (F67) |
| 3 | **X5 FREE-DECLARATION** | both judgements determinate and agreed, **and** both readers record `free` at the same §2 row, each exhibiting its own \(d'\) | a **finding-1 exhibit** against the named §2 row: \(d\), \(d'\) and the flipped judgement are quoted. **No finding against FW5's mapping** |
| 4 | **X2 CONFLICT-POSITIVE** | both readers agree: (E) **holds** on the exhibited \(\mathcal E_c\) and the defect **does not obtain** of the quoted target passage | a **conflict** among three propositions — (K1), (E) on this \(\mathcal E_c\), and **(O)** — charged by the table below. **Never a counterexample to Account, never to (K1) alone** |
| 5 | **X2b CONFLICT-NEGATIVE** | both readers agree: (E) **fails** and the defect **does obtain** | the same three-way conflict, charged the same way. **Explicitly not a necessity result**: :1364's necessity defeater quantifies "under any interpretation", and **this leg cannot quantify over interpretations at all**, so no cell can ever produce that quantifier |
| 6 | **X1 AGREE-POSITIVE** | both readers agree: (E) **holds** and the defect **obtains** | one supported instance of the (K1) mapping. **Charge none** |
| 7 | **X1b AGREE-NEGATIVE** | both readers agree: (E) **fails** and the defect **does not obtain** | one supported instance of the (K1) mapping, **negative direction**. **Charge none** |
| 8 | **X4 UNRESOLVED** *(residue)* | **otherwise.** Including: the readers disagree on the exhibited \(\mathcal E_c\), **or exhibit different \(\mathcal E_c\)** (F54); or disagree on J1, on J2, or on the :620 check; or exactly one reader records a judgement *undetermined*; or the two record *different* judgements undetermined; or exactly one records `free` | **none.** Recorded with the disagreement, never averaged (FW5:634 — "An observer may lack the data needed to establish the witness. That makes the attribution unresolved; it does not prove either understanding or its absence") |

**No class may be upgraded after a reading, under any reading of this document.**

#### Reachability, exhibited cell by cell (F52)

**These are reachability witnesses. They are NOT predictions, NOT assignments,
and no cell's class is decided here.** Each names a real cell of the register
and a reader state that would place it in that class, so that the class is shown
to be *occupiable* rather than merely defined. The reading step decides every
one of them, and may put none of these cells where its witness sits.

| class | cell | the reader state that would place it there |
|---|---|---|
| **X0** | **A32** (F001 occ-07 row 1) | **assigned, not a witness.** `target_record_id` is genuinely absent; the resolver note is quoted in `CELLS-v4.md` |
| **X4** (gate) | **A01, A02, A06-A10, A18-A20, A24-A31, B01** | **assigned, not witnesses.** 19 cells, bridge returns (b5) |
| **X3** | **A15** (F001 occ-01 row 4, `o2`→`c6`) | both readers report that the target organization \(D\) of \(p_\delta\) cannot be written out at all: the alleged defect is an inconsistency **between** `c6` and `c3`/`c4`, three records, while the frozen grain \(\ell\) is the **single record keyed by id**, so no admissible \(D\) at that grain carries all three commitments and the grain may not be varied. Both name \(D\) as the absent component |
| **X6** | **A11** (F001 occ-01 row 0, `o1`→`c1`) | `bearing`: "counters treating c1 and c2 as the frame rather than as one hypothesis among at least two". Both readers record **J2 undetermined**: the quoted `account#c1` passage asserts a claim, and whether asserting it amounts to *treating it as the frame* is not settled by the passage either way |
| **X5** | **A04** (golden 3, `o3`→`c2`) | both readers record `free` at **D6**: one declared abstraction retains the ordering of the account's recommendations and one projects it away; under the first (E) fails and under the second it holds, and neither reader can name a line excluding the other. Each writes out its own \(d'\) |
| **X2** | **A03** (golden 2, `o2`→`c2`) | both agree (E) **holds** on the exhibited \(\mathcal E_c\), and both judge that the defect **does not obtain**: `account#c2`'s own `consequence` field states the confirm/refute test, and both readers read it as discriminating the readings the `bearing` says it cannot |
| **X2b** | **A05** (golden 4, `o3`→`c3`) | both judge the prescriptive over-reach **does obtain** of `account#c3`, while (E) **fails** on the exhibited \(\mathcal E_c\) because :176 s3's equality cannot be met at the declared abstraction |
| **X1** | **A16** (F001 occ-01 row 5, `o2`→`c3`) | both agree (E) **holds** and the alleged inconsistency **obtains** of `account#c3` |
| **X1b** | **A12** (F001 occ-01 row 1, `o1`→`c2`) | both agree (E) **fails** on the exhibited \(\mathcal E_c\) and the framing allegation **does not obtain** of `account#c2` |

**Stated so it is not over-read.** A witness shows a class is occupiable by a
state a reader could actually record on a named cell; it does not show that any
reader will record it. **Every one of the seven read-cell classes has a witness
over the 13 read cells, so no class in this table is reachable only in
principle.** If the reading step leaves a class empty, that is a fact about the
13 cells and is reported as one — never as evidence about FW5, about the records
or about their authors (rule 6).

#### The charge rule, as a decision table — one row per class

> **Read this table literally. It is the whole rule. There is no further branch,
> no residual clause, and no exception.**

| class | charged to | may the charge name Account? |
|---|---|---|
| **X0** | **D14** | **no** |
| **X4** | *(nothing)* — **except** that a cell both readers fail on the **:620 check** charges **D21**, and that charge is the whole record of the cell | **no** |
| **X3** | **D21 first, then D14** | **no** |
| **X6** | **D21 first, then D14** | **no** |
| **X5** | the named §2 row as a finding-1 exhibit, with \(d\), \(d'\) and the flipped judgement quoted | **no** |
| **X2** | **D21 first, then D14**; the residue, if any, is recorded as a conflict among (K1), (E) and **(O)**, and left as a conflict | **no** |
| **X2b** | **D21 first, then D14**; same residue treatment | **no** |
| **X1** | *(nothing)* | **no** |
| **X1b** | *(nothing)* | **no** |

**Closing sentences of the rule, which are part of the rule.**
**(i) No row names Account, and no composition of rows produces one.**
**(ii) There is no Account-alone charge.** v2 defined one and denied it two
sentences later; **that branch is deleted, not merely disclaimed**.
**(iii) Its antecedent is false for every cell in this register anyway**, and
that is Measured, not expected: FCL-1 has no \(\delta\) slot, so no cell's
\(\mathcal E_c\) is supplied in full by the record's own fields.
**(iv) A cell that somehow met the deleted condition would be recorded as an
anomaly in the worksheet's notes column and would still be charged by the row
its class assigns above.**
**(v) No upgrade of a class after a reading is available, under any reading of
this document.**

#### Cells — the revised pre-registration (33 cells)

Rendered as data in `CELLS-v4.md`, **with the bridge branch and, where already
determined, the outcome class frozen per cell**. Pins unchanged (all five
re-hashed at each review):
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
occurrences — contribute zero rows**; that is a fact about those documents'
authored refs, not about their authors, and it is recorded as a cell count of
zero, never as a negative finding.

*Sub-register B — one cell whose referring record is not typed `objection`.*
F001 occurrence-01 **row 12**, `carry#r2` → `response#m2`, `type: "claim"`.
**Pre-declared (b5) → X4.** It is retained as a datum about the FCL-1 `type`
field, not as a readable cell.

*Declared-use rows, a separate register (12 rows, `use-table-golden` rows 5-9,
12, 14, 15, 18-21).* Carried by `claim`, `use` and `problem` records with no
`bearing`. Not cells; FW5:640 makes a declared field a delivery fact. They are
read only to record what the language declared, and they can never supply a
counterexample to anything.

*E2 — equivariance check, with its reachability stated.* The C001 ORIGINAL
objection block against the RECODING block, **unit by unit over the fcl arm's 50
units** (28 `B.*` body + 22 `K.*` record-field), not over all 85 — the other 35
are the `mini_prose` arm. **Measured: the 22 `K.*` units cover eight records —
`o1`, `o2`, `o3`, `o4`, `c1`, `c2`, `p1`, `u1` — of which only `o1`, `o2`, `o3`
carry a referring row in the golden table**, so **E2 can reach at most golden
rows 0, 1, 2, 3, 4** — five cells. Golden rows 10, 11, 13 refer from the
`response` node (`k3`, `k7`) and rows 16, 17 from `carry` (`n3`), which the table
does not cover. No F001 cell is reachable by E2 at all. **Golden rows 0 and 1
are gated to X4, so E2's reach and the leg's read cells overlap in three cells:
A03, A04, A05** — unchanged by the conditional rule, which touches none of them.

*E2's provenance.* The ORIGINAL block is the H005 objection document "exactly as
the H005 `response` node saw it: the same `body` and `commitments` bytes,
projected by the same `project()` with view `both`" (C001 PLAN:184-188);
`prepare` refuses unless the case bytes equal the occurrence artifact bytes
(`ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES`). It is **identity of the
projection**, not of the artifact file.

*E3 — non-evaluable cells, declared in advance and excluded from every side:*
C001 occurrence-01 `deepseek-flash` × `fcl`, 19 of 20 coordinates as restated in
§4 finding 3; the single PARTIAL at `ollama-glm-5.3` × `fcl` CONTROL rep2; the
12 nodes whose commitment surface was not read in `use-table-full`
(`nodes_not_read`, 10 `prose_not_parsed` plus 2 `unavailable_decode_failure`);
and the 7, 8, 6, 5, 6, 9, 6, 7 `nodes_not_read` of the eight F001 use tables.

**An equivariance failure (E2).** A cell whose (E) assessment differs between
the ORIGINAL and RECODING codings. This is **not** a counterexample to S or N.
**It is finding 2 against the C001 table's own content-preservation argument
(D13), and nothing else.** *v2's second disposition — "or a challenge to
FW5:1202's applicability at this grain" — is **withdrawn**: :1202 hypothesises
that **all** carriers, component relations, role bindings, maps, histories,
question contracts and attribution indices are transported along
structure-preserving bijections, the recoding table recodes **one** document
while the targets `account#c1-c3` are not recoded at all, and :1206 excludes
what is not "the stipulated bijections". **No E2 outcome bears on :1202.***

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
6. **A count of cells, of any kind, on any side: a single exhibited instance,
   with both passages quoted, defeats a universal claim in the worksheet's own
   scope; no count adjudicates anything.** FW5:851's own list is "(G), (P), or
   (EK)" — "No quantity of endorsements, surviving tests, repeated observations,
   or partitioned features enters (G), (P), or (EK) as an automatic warrant" —
   and **Account is not in it**; the link from (EK) to Account is the conjunct at
   :831. **The universals in reach here are A001's own, and they are named so
   that this rule's claim-enabling half has a stated subject (F56):** (i) the
   **bridge's coverage claim** — that the frozen branch supplies, for every cell
   it fires on, a respect that concerns that record's own alleged defect (:620);
   one cell failing the :620 check defeats it; and (ii) the **register-level D14
   claim** — that no cell's \(\mathcal E_c\) is supplied in full by the record's
   own fields; one cell so supplied would defeat it. **No cell defeats (K1)**,
   because every \(\mathcal E_c\) in this register carries an A001-reconstructed
   \(\delta\), so no cell exhibits an instance of (K1)'s right side that is the
   record's own. *v3 named (K1) as the universal in reach, which made rule 6 a
   licence for the one output the class table bans; that is corrected here.*
   **The branch counts of §3 are coverage facts about A001's own bridge and are
   explicitly not evidence under this rule.**
7. A finding about C001's four registers. A001 does not fill or read them.

**Reading discipline.** Two readers per cell; where they disagree the cell is
`unresolved` and the disagreement is recorded, never averaged (FW5:634; C001
PLAN §8a:743-745). The worksheet's assessment columns are rendered empty by the
staging and are filled only by the reading step.

### 5(c) P3-P8, as separately identified gap-filling contributions

Source for P3-P7: `docs/reviews/fw5-vs-harness-spec-2026-09-14.md` §5. **P8 is
A001's own.** Governing rule, verbatim from PURPOSE.md: "Proposed gap-filling
definitions, interpretations and mechanisms are separate criticizable
contributions; they must not silently rewrite the source or absorb adverse
evidence after the fact." Each is published as its own document with its own
identity; none may edit FW5 or any frozen PLAN; each acceptance condition is
declared **before** A001's reading.

| id | gap it fills | which A001 dependency | rule of engagement | offline today |
|---|---|---|---|---|
| **P3** criticism-ablation arm for F001 occurrence-02 | discharges `ProducedBy` (FW5:800), not Account | D19 | needs live calls; **out of A001's scope entirely** | no |
| **P4** loss ledger (O, P pinned before the later cycle) | (P) at FW5:787-802 | D19 | must be pinned by sha256 *before* dispatch; a dry run over an existing pair is labelled as violating its own pre-declaration and establishes nothing | dry run only |
| **P5** custody and grain preconditions | D7, D13 | if P5 shows the §3 grain is not partition-invariant, A001's cell readings are **preconditioned**, not rescued | yes |
| **P6** FCL-1's fields against FW5:609/:622 | D14, D15 | supplies the \(\delta\)-slot diagnosis this leg's ceiling rests on; it is a **language-adequacy** reading of one cycle, never an Account result | yes |
| **P7** pre-registered reading set | the observer, not the subject | A001's cell list **is** P7 applied to this stage: frozen in `CELLS-v4.md`, with every change since v1 recorded and the v1 list retained | yes |
| **P8** the `bearing`→\(\kappa\) bridge | D21 | **declared with its provenance disclosed: it is NOT independent of the cells.** (b3) paraphrases golden 3/4; **(b1)'s second limb paraphrases golden 2**; **(b2) was tuned on F001 occ-01 rows 0-3** and matches zero golden cells; **(b4) paraphrases golden 16/17**; **(b6)'s stated example is the `bearing` text of six cells verbatim**; (b7) alone is unfitted and fires on nothing. **Consequence: this leg can charge the bridge and can never support it**, and no outcome may be reported as evidence that the bridge is right. **:620 constrains it and the :620 check applies it** | yes |
| **P9** *(new at v4)* a stated rule for \(\operatorname{Ans}_E\) | **D22** | the gap Case A-S reaches by (r2): a rule fixing whether a candidate's declared query is evaluated on the candidate's own organization or on the anchored target subnetwork, and at which abstraction. **It is a proposal, not a reading of FW5, and (P-Ans) is one candidate among others; proposing it does not make A-S's disposal unconditional** | yes |

P3 and P4 are named and deferred. P5, P6, P7, P8 and P9 are what A001 carries
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
  constitutive conjecture. **FW5:1368, quoted whole: "These challenges concern
  the constitutive conjecture, not a missing proof of a theorem asserted to
  follow from set theory. The distinction matters: a definition can be exact
  while being a poor theory of its intended subject."**
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
* **A001 makes no universal claim about which abstractions satisfy Anchoring.**
  v2's "no endpoint-level abstraction satisfies Anchoring…" and "neither does
  any endpoint-level abstraction of FW5's own discriminating pair" are
  withdrawn; case (γ) and \(\lambda_w\) are recorded against them (§5(a)(i)).
* **The executable leg's finding 2 against D14 is declared before the reading
  and cannot be strengthened by it.** A reading that reports the \(\delta\)-slot
  absence as a discovery, or reports it per cell, is a regression against this
  document. **The same now holds for the register-level finding-1 fact that
  \(\ell\), \(\beta\), \(\mathcal C\) and \(\kappa\) had to be declared at all**
  (§5(b)).
* **The branch counts of §3 and the cell counts of §8.5 are coverage facts,
  never evidence** (rule 6).
* **New at v4: A001 does not claim that (A) fails under every \(\lambda\) for
  Case A-S.** That sentence is **withdrawn** as an unconditional claim. It
  survives only as an Interpretation **conditional on (P-Ans)**, a premise A001
  supplies and the reading edition does not, and the alternative reading —
  under which (A) **holds** at \(\lambda_w\) — is recorded in §5(a)(i) and
  carried as **D22**, undefined, in §2.
* **New at v4: the prose leg's yield includes one finding 1 (D22) reached by
  (r2), and no more.** A reading of §5(a)(i) that treats D22 as a counterexample,
  or that reports Case A-S as undisposed rather than as disposed-under-a-named-
  premise, is a regression against this document.
* **New at v4: five cells lost a respect and none gained one.** A revision that
  restores a branch to golden 10, 11, 13, 16 or 17 without amending the stated
  conditional rule of §3 is a regression against this document.
* **New at v4: no class of §5(b) may be reported as reachable "in principle".**
  Each of the seven read-cell classes has a named witness cell in §5(b); a class
  the reading step leaves empty is reported as empty over 13 cells, never as
  evidence.
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
    table including D22; §3 grain/boundary/contrast, the bearing→κ bridge with
    its disclosed provenance, its conditional rule and its :620 constraint;
    §4 relinquishment + the three findings; §5(a) the two failed prose cases,
    both written out, the rule that disposes of them and the premise (P-Ans)
    that horn 2 needs; §6 claim ceiling. Receipt paragraph at the head.
docs/reviews/A001-gap-filling-proposals-2026-09-14.md
    P3-P9 as separate criticizable contributions, each with its acceptance
    condition declared before the reading (§5(c)).
experiments/diagnostics/A001-account-challenge/PLAN.md
    Pre-registration of the executable leg: the (K1)-mapping route with the
    eight-locus survey, the leg's declared ceiling, the frozen cell list, the
    reading procedure with the :620 check and the free-declaration test, the
    nine outcome classes with X4 as the residue row, the reachability table,
    the charge decision table, the two-reader rule, the claim ceiling,
    0 planned provider calls.
experiments/diagnostics/A001-account-challenge/material.json
    source pins (FW5, both use_table.json, both comparison.json,
    RECODING_TABLE.md, both C001 materials) + the frozen cell list as data.
experiments/diagnostics/A001-account-challenge/CELLS.md
    the 33 cells in two sub-registers with their frozen bridge branches, the
    12 declared-use rows, the five E2-reachable cells and the E3 exclusions,
    rendered from material.json.
experiments/diagnostics/A001-account-challenge/WORKSHEET.md
    one row per read cell, with columns for the exhibited π, τ, σ, λ and p_δ,
    the :620 check, J1, J2, the per-declaration free/not-free records, the
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

### Receipt paragraph

**Measured, re-counted at this revision's bytes, stamped, and with the counting
definition stated beside each number (F62).** A bare "entry count" is not
reproducible — `docs/DECISION_LEDGER.md` admits at least four defensible
definitions and they differ — so each figure below names the rule that produced
it. Read at **commit `f191f48116a286c2ddcdc54e4663ff307ea9f36b`** (tree
`0d040f47f9d3282b5f46fcab3a42afe6cccd47fa`), **2026-09-14 14:58 UTC**, over a
file of **1,495 lines** and **728,439 bytes**:

| figure | counting definition | value |
|---|---|---|
| `REC-20260914` **lines** | lines **containing** the string `REC-20260914` | **109** |
| `REC-20260914` **receipt openings** | lines **beginning** with `REC-20260914` | **108** |
| `REC-20260914` **identifiers** | distinct `REC-20260914-<letters>` ids | **26**, exactly `-A` … `-Z` |
| closing `Prior verified commit/tree:` | lines containing the string | **25** |
| `Choice:` / `Why:` / `Reason:` / `Contribution:` / `Contribution to the end goal:` / `Letter:` | lines containing each string | **96 / 86 / 9 / 90 / 0 / 5** |
| historical CRLF lines | occurrences of `\r\n` in the bytes | **37** |

**The 109 and the 108 differ by one line** — line **1378**, inside
`REC-20260914-S`, which cites `REC-20260914-Q` and `-R` in its text without
opening a receipt. **"109 entries" without its definition is therefore not a
reproducible figure**, and neither is any other bare count over this file: a
line-start rule gives 381 `REC-` lines for the whole file and a
blank-line-separated-paragraph rule gives 364. *v3 staged "104 `REC-20260914`
entries" and "`Prior verified commit/tree:` 24" with no definition; the values
were stale and the first was undefined.* **These counts are stamped with the
commit they were read at, adjudicate nothing, and must be re-read — under a
stated definition — at the moment of the append rather than carried from this
document.**

**Cross-checked, not adopted.** An independent mechanical audit of the same file
at the same commit reports 1,495 lines, 37 CRLF-terminated lines, 25
`Prior verified commit/tree:` lines, 26 distinct identifiers `-A` … `-Z` with no
identifier of more than one letter anywhere in the file, and 77 lines matching
`VERIFIED <40hex> TREE <40hex>`. **Every figure above was re-derived here from
the bytes independently and agrees with it on each overlapping figure.** The
audit is recorded as a cross-check, not as a source.

**Two conventions the receipt carries, both present in `REC-20260914-Y` and
`-Z`:** an opening **`Letter:`** field, which states which identifier closed
last, that the taken identifier was free, and that it is taken here; and the
**append note**: "appended in byte mode and staged only after an
insertions-only `git diff --numstat` (**OPS-20260914-LEDGERCRLF**; the file's
**37 historical CRLF lines must still be 37** after the append)".

**The identifier, and the one instruction a publisher could not execute (F63).**
**Measured at the commit above:** `REC-20260914-A` through `-Z` are **all
taken** — 26 distinct identifiers, over 108 lines opening a `REC-20260914`
receipt, `-Z` opened at 11:14 UTC.
**Measured:** the ledger's earlier series ran `20260912` B-H and `20260913` I-L;
**no identifier of more than one letter occurs anywhere in the file**, and
**neither `AGENTS.md`, `docs/DECISION_LEDGER.md` nor
`skills/minireason-experiment-operations/SKILL.md` states any rule for a
twenty-seventh receipt in one day.** v3 said only that the identifier is
"determined at the moment of the append, by the appender", which leaves the
publisher without a rule.

> **Proposed scheme, for the publisher to adopt or reject: `REC-20260914-AA`** —
> two letters, lexical continuation, so that the day's series runs A…Z, AA, AB,
> …, AZ, BA, …. **A001 does not mint it.** The proposal and the one-paragraph
> justification a publisher can append to the ledger as a note are in
> `CHANGES-v4.md`. **Choosing the scheme is itself a decision**, and if it is
> adopted the `Letter:` field must record it as one: that A-Z were all taken
> when the ledger was read, that no stated rule for a successor existed, that
> this scheme was chosen and why, and that the identifier taken was free at that
> moment. If the publisher rejects the scheme, the receipt takes whatever
> identifier the publisher's own rule yields and the `Letter:` field records
> that rule instead.

> REC-\<date\>-\<identifier determined at the append; `-AA` proposed above\>
> opened at YYYY-MM-DD HH:MM UTC: Letter: \<which receipt closed last, at what
> time; that `REC-20260914-A` through `-Z` were all taken when the ledger was
> read and no stated rule for a twenty-seventh identifier in one day exists;
> which scheme was adopted and why; that the taken identifier was free when the
> ledger was read, and that it is taken here\>. This receipt is appended in byte
> mode and staged only after an insertions-only `git diff --numstat`
> (OPS-20260914-LEDGERCRLF; the file's 37 historical CRLF lines must still be 37
> after the append). Stage A001, an independent Account sufficiency-and-necessity
> challenge to the designated FW5 reading edition (sha256
> `8105925b…e33ee63a`), under PURPOSE.md ("In parallel, an independent Account
> sufficiency or necessity challenge tests FW5 itself"); the prose leg is
> written against the "Testing FW5 itself" row of
> `docs/reviews/FW5-research-plan-decision.md`, which is still
> `Status: proposed, awaiting the user's approval` and is cited as intent, not
> approval, **and whose stated deliverable — a candidate counterexample and the
> clause that would have to change — A001 does NOT meet and records as still
> owed.** **A001 OFFERS NO COUNTEREXAMPLE AND NO POSITIVE RESULT ABOUT FW5'S
> STATED CLAUSES.** Choice: publish
> `docs/reviews/A001-account-challenge-2026-09-14.md` (the two named claims with
> their FW5 lines; the dependency table marking each primitive defined /
> undefined / defined-but-unmapped, **with D6 — the declared abstraction — and
> D22 — how a candidate's answer profile \(\operatorname{Ans}_E\) is arrived at
> — both marked undefined**; the grain, boundary, contrast and `bearing`→κ
> bridge declared before any evidence **with the bridge's dependence on the
> cells disclosed, its conditional match rule stated, and FW5:620 applied to it
> as a constraint**; the conditional relinquishment statement; and **two
> authored prose cases written out and recorded as failures — Case B-N at
> FW5:1372 with :188, :174, :170 and :244, and Case A-S at FW5:208 under a
> premise (P-Ans) that A001 supplies and the reading edition does not, with the
> alternative reading recorded and its residue filed as the missing definition
> D22**),
> `docs/reviews/A001-gap-filling-proposals-2026-09-14.md` (P3-P9 as separately
> identified contributions with acceptance conditions declared before the
> reading), and `experiments/diagnostics/A001-account-challenge/` (PLAN.md,
> material.json, CELLS.md and an empty WORKSHEET.md) — the executable leg over
> **existing published records only**, restated as a **(K1)-mapping test**: 33
> bearing cells in two sub-registers drawn from the H005 occurrence-01 snapshot
> use tables and the eight F001 use tables, of which **13 are read and 20 are
> gated unread before the reading begins**, **nine pre-declared outcome classes
> whose exhaustiveness is definitional (X4 is the otherwise-row), each with a
> named reachability witness, a charge decision table no row of which names
> Account, an operational free-declaration test and a pre-declared FW5:620
> check**, 12 declared-use rows kept in a separate register, five E2-reachable
> cells over the C001 correspondence table's 50 fcl units, and a declared
> exclusion list of non-evaluable cells. Why: the source's sufficiency and
> necessity claims are the place FW5 itself says to attack it (FW5:1362-1364,
> :1502), and the repository has never tested them against its own published
> records; this stage reports that the two authored attacks fail — one of them
> only under a premise A001 names rather than finds in the edition — that the
> executable leg's one finding against FW5 (no stated route from a published
> criticism record to \(\mathcal E_c\)) is declared **before** the reading and
> cannot be strengthened by it, and that FW5:617 defines bearing as accounting
> while the eight other bearing loci surveyed in the reading edition supply no
> second route. Contribution: a separately identified test of the semantic
> source with its dependencies named before the evidence, which returns two
> recorded failures, two missing definitions (D6, D22), one declared mapping gap
> and one disclosed, criticizable bridge rather than a counterexample it cannot
> support; a missing definition, an unsupported mapping and an operational
> failure are recorded as three different findings and never as one. State:
> PENDING — **zero provider calls planned and zero made**; no cell of any
> published table is filled by this stage and every assessment column of
> WORKSHEET.md is published empty; the reading step is a separate receipt.
> Evidence: pins recorded in `material.json`; nothing under
> `experiments/diagnostics/C001-*`, `H005-*`, `F001-*` or
> `experiments/analyses/` written or touched. Prior verified commit/tree: \<the
> last verified published commit\> / \<its tree\>, read at the moment of the
> append.

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
   charge to D21, D14, a named §2 row, or a recorded conflict, and offers no
   Account cell at all. Its one finding against FW5 is declared in advance.
2. **The FCL-1 records were not authored as \(\mathcal E\).** They were authored
   as criticisms in a language with `target`, `grounds` and `bearing` but no
   \(\delta\) slot. Reconstructing \(\mathcal E_c\) from such a record is itself
   an interpretation; X3, X5 and X6 are where that lands, and none is a finding
   against Account.
3. **The bridge (D21) is the leg's softest joint, and v4 makes that worse, not
   better.** §3 now discloses that **five of the six fitted-or-firing branches
   paraphrase the cells they fire on, that (b4) and (b7) fire on nothing, and
   that (b1) fires only on the single cell its second limb restates.** If the
   bridge rule is wrong, the respects are wrong and every downstream mark is
   wrong. It is published as its own contribution (P8) so that it can be
   rejected on its own, and the leg can charge it but never support it.
4. **The grain is C001's, not A001's.** Adopting the record-keyed grain keeps
   A001 comparable with the published material but inherits P5's open
   partition-invariance question. If P5 later shows the reading does not survive
   re-partition, A001's cells are preconditioned, not rescued. **The X3
   reachability witness at A15 is the same tension seen from the other side:**
   an alleged inconsistency spanning three records against a single-record
   grain.
5. **Cell supply is thin and uneven, and 20 of 33 cells are pre-declared
   unreadable.** 10 cells in H005 golden; 23 across F001, of which **14 come
   from one occurrence** and **five occurrences supply none**. Only five cells
   are E2-reachable and only three of those are read. **13 of 33 reach a respect
   under the bridge; 19 are X4 and one is X0 before the reading begins** (§3).
   No universality claim of any kind may be built on that distribution, and the
   zero-row occurrences must be reported as zero rows, not as silence.
6. **Two published Account challenges will then exist, and both report a failed
   candidate.** §0 states the relation. A001 must not be read as the skew-matrix
   review's successor or as an attempt to overturn it.
7. **The honest A001 shrinks at each revision, but not in every direction, and
   both directions are regressions.** v2 made itself smaller than the evidence
   supports at one place (the D6 narrowing). v3 made itself larger than the
   edition supports at another (the every-λ sentence). Whoever reads this next
   should check **both**: any sentence that offers a candidate counterexample,
   upgrades an outcome class after a reading, or lets a cell charge Account is a
   regression; and so is any sentence that concedes a dependency is defined when
   the reading edition does not define it, or that withdraws a disclosure about
   A001's own bridge.
8. **Five things in this document are arguments, not readings, and are the
   places to attack it.**
   (i) **(P-Ans)** — the premise horn 2's disposal rests on. It is named, it is
   not FW5's, and if a reader prefers the :210 s1 reading then Case A-S is a
   finding 1 and not an (r1) failure. **This is the single most attackable
   sentence in the document.**
   (ii) **The :210 s2 reading recorded and not relied on** in §5(a)(i) — whether
   evaluating the anchored organization at \(\lambda_w\) is "a copied target
   assertion among its premises". If it is, FW5 has a stated clause and A-S
   fails at (r1) on both readings; A001 does not claim that, and a reviewer who
   establishes it makes A001 smaller still.
   (iii) **The conditional rule of §3** — it fires fewer branches, which is the
   direction A001 chose deliberately, but it is a rule about English, not a
   reading of FW5, and a second reader could reject it.
   (iv) **The reachability witnesses of §5(b)** — each is a state a reader could
   record, argued from the cell's own bytes. If any of the seven is not in fact
   occupiable, that class is unreachable and the table needs rebuilding again.
   (v) **The strict reading of :212 s3**, which three reviews have now accepted
   but which is still a reading of the word "every".

---

## Open items carried into this record

The eleven residual open items of the narrow verification
(`A001-account-challenge-2026-09-14-history/CHECK-v4.md`), reproduced verbatim from its own closing
section, including its preamble as written.

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

---

<a id="review-round-4"></a>

# Review round 4 — 2026-09-15 — F68-F72

**REC-20260915-C; appended at 2026-09-15 05:12:48 UTC.** The supplied draft was written by one Astra worker and independently judged by a second. The judge's verdict is **ACCEPT WITH THE EXACT EDITS, as a new review round**; its corrections govern where the draft differs. Draft: `work-2-a001-draft.md`; judge: `judge-2.md`, both in the supplied `scratchpad/reports/` directory. Their SHA-256 identities are recorded below. The first three rounds remain F1-F29, F30-F50 and F51-F67. A prior F68 assignment was **NOT FOUND** in A001 and its history before this append; this round takes F68-F72.

**Preservation and scope.** Every byte before this append remains unchanged, including the v4 body and all eleven carried open items. The entries below are dated **old → new successor wording**, not edits to those earlier passages. A disposition of **fixed** records the corrected successor specification; it does not adopt the separately criticizable instrument proposals, fill a worksheet, assign a reading class, or demonstrate reachability. Sections A-E reproduce the judge's exact endorsed wording. Section E belongs to item 9's assessment only. FW5 is the sole semantic target under owner ruling 17 (`session-rulings-2026-09-14.md:27-29`); FW5 citations identify reading-edition lines only.

## Findings and appended open-item disposition map

| Finding / carried item | Finding and affected A001 locators | Disposition and reason | Remaining obligation |
|---|---|---|---|
| **F68 / item 3** | The (b6) example was deleted between v3 and v4 without disclosure, while the disclosure still invoked it: A001:309-312, 414-415, 1234; carried item at 1601-1606. | **Fixed** by section A's dated provenance correction and dependent fragments. A001:381 and the frozen assignments remain unchanged. Provenance alone does not establish that the general condition is defective or lacks application elsewhere. | Reassess the extent of fitting with a substantive argument; this leg still cannot confirm the bridge. |
| **F69 / item 4** | X3/A15's three-record obstruction conflicts with X1/A16's presumed reconstruction: A001:1050-1074, with the dependent locators in section B; carried item at 1607-1613. | **Withdrawn**: the A15 witness and the claimed completed reachability demonstration. A16 remains a conditional reader state; X6/A11 and X5/A04 are not implicitly certified. Record count or a changed target identifier does not establish the required obstruction or reconstruction. | Complete replacement witnesses and a reachability demonstration consistent with the fixed grain, boundary and references remain owed. The distinct E2 accessibility claims at A001:1141-1149,1544 are retained. |
| **F70 / item 5** | The four Boolean proposals omit their complete `not-free` antecedents; A05 lacks its own examination of A04's D6 alternative: A001:1000-1014,1056,1063-1066; carried item at 1614-1617. | **Fixed** as a conditional specification by section B's shared condition and A05 comparison, synchronized with section D's Boolean conditions. Adding an antecedent does not exhibit its satisfaction. | The required complete Boolean exhibits and target-specific A05 assessment are **NOT FOUND**; no witness is certified. |
| **F71 / item 6** | The worksheet specification omits explicit evidence types, an incomplete-assessment status and routing: A001:997-1008,1346-1350; carried item at 1618-1622. | **Fixed** in the proposed specification by section C. The draft's claim that the existing text supplied no rule against an unperformed search is **declined with reason**: A001:997-1008 already required evidence and a record of what was tried. Three statuses and evidence type NONE make the remaining gap explicit. | The actual diagnostic worksheet is **NOT FOUND**. Completed search records and exclusion arguments remain owed; SEARCH-NO-EXHIBIT proves only what the recorded search exhibited. |
| **F72 / item 7** | Overlapping Boolean/X5 conditions, an unstated table exit, reversed gate order and reconstruction disagreement: A001:954-975,1010-1014,1026-1031,1037,1040-1043; carried item at 1623-1627. | **Fixed** in section D's prospective procedure and table specification. An attempted unresolved :620 check is distinguished from a check not yet reached; exits apply only when their conditions are established. | The strengthened evidence and routing policy remains a separate proposal, not adopted. Complete exhibits remain owed; the disposition and charge columns are unchanged. |

Items 3-7 remain in their historical list at A001:1601-1627 and now point, through this appended map, to F68-F72 respectively. Their recorded corrections and withdrawals do not discharge the remaining obligations. Items 1, 2 and 11 retain the earlier REC-20260914-AB housekeeping disposition.

## Exact judge-endorsed old → new entries

The locators below refer to the preserved pre-append A001 and companion. **Old** reproduces the judge's specified old wording or locator description, including its abbreviations; the historical text itself is retained byte-for-byte.

## A. Item 3: disclosure

### A001:309–312

**Old:**

> **(b6)** is written from :609's own defect list, but its stated example - "(e.g. 'alleges an internal inconsistency between .')" - **is the `bearing` text of F001 occurrence-01 rows 4, 5, 6, 20, 21 and 22 verbatim**. It is fitted too, and is disclosed as fitted at this revision.

**New:**

> **(b6)** uses FW5:609’s named defect kind, inconsistency. Its general condition restates the inconsistency allegation in A15–A17 and A21–A23: “alleges an internal inconsistency between raising c6 and leaving c3 and c4 unchanged”. The branch was written with these cells in view. v3 included an abbreviated example; v4 deleted that example without recording the deletion. This correction records that deletion: the current rule contains the general condition, not the example. The deletion establishes no independence from the cells, and the frozen assignments remain unchanged. This provenance does not itself establish that the general condition is defective or lacks application elsewhere; the prohibition on confirming the bridge through this leg remains.

### Dependent fragments

| Location | Old → New |
|---|---|
| `A001:414–415` | “(b6) on the six cells whose `bearing` is the text its own stated example quotes” → “(b6) on the six cells whose inconsistency allegation its general condition restates” |
| `A001:1234` | “(b6)'s stated example is the `bearing` text of six cells verbatim” → “(b6)'s general condition restates the inconsistency allegation of six cells read before the rule was written” |

**A001:381 remains unchanged.** The companion’s corresponding fragment at `Cells:158–159` needs the same dated correction, preserving its earlier bytes. (`Draft:127–143`)

## B. Items 4–5: witnesses and reachability

### A001:1060 — X3/A15 reader-state text

**Old:**

> both readers report that the target organization \(D\) of \(p_\delta\) cannot be written out at all: the alleged defect is an inconsistency **between** `c6` and `c3`/`c4`, three records, while the frozen grain \(\ell\) is the **single record keyed by id**, so no admissible \(D\) at that grain carries all three commitments and the grain may not be varied. Both name \(D\) as the absent component

**New:**

> **The stated witness is withdrawn.** The fact that the alleged inconsistency spans `c6`, `c3` and `c4` does not, without an argument about the frozen grain and boundary, establish that no admissible \(D\) can be reconstructed. A complete obstruction establishing X3 on A15 is **NOT FOUND** in this record.

### A001:1065 — X1/A16 reader-state text

**Old:**

> both agree (E) **holds** and the alleged inconsistency **obtains** of `account#c3`

**New:**

> **Conditional reader state only.** Both readers must exhibit the same complete \(\mathcal E_c\) and \(p_\delta\), agree that the :620 check passes, agree that (E) holds and the alleged inconsistency obtains, and satisfy the shared Boolean-state condition. A complete exhibit satisfying those requirements is **NOT FOUND** in this record. The withdrawn A15 argument cannot simultaneously establish a reconstruction obstruction here.

### Before A001:1056

**No shared witness condition → add:**

> **Shared condition for the four Boolean reader states.** Both readers exhibit the same complete \(\mathcal E_c\) and \(p_\delta\), agree that the :620 check passes, and record determinate, agreed J1 and J2. For each reader and every per-cell declaration used to obtain those judgments, the worksheet records `not-free` with a completed TEXT-EXCLUSION or SEARCH-NO-EXHIBIT record. Neither reader records `free` at any such declaration. A blank or unperformed check does not satisfy this condition.
>
> **Required A05 comparison.** Each reader considers the D6 alternative proposed for A04 on A05’s own target and reconstruction. The record states the alternative, its admissibility assessment, and the resulting J1/J2, or quotes the FW5 clause and supplies the argument excluding it. Different target identifiers or identical `bearing` text alone settle neither admissibility nor effect. An admitted judgment-changing alternative cannot be recorded as `not-free`.
>
> These are requirements on proposed reader states, not completed observations. The required evidence is **NOT FOUND** in the current Boolean entries. SEARCH-NO-EXHIBIT records only the stated search.

### A001:1050–1054

**Old:**

> **These are reachability witnesses. They are NOT predictions, NOT assignments, and no cell's class is decided here.** Each names a real cell of the register and a reader state that would place it in that class, so that the class is shown to be *occupiable* rather than merely defined. The reading step decides every one of them, and may put none of these cells where its witness sits.

**New:**

> **These are proposed reader states, not demonstrated reachability witnesses.** No reading-class assignment is made here. Each retained proposal must satisfy its class’s complete antecedent on the named cell. This includes the reconstruction and :620 requirements for X6/A11 and the complete reconstruction, determinate agreed judgments, and flipping alternatives required for X5/A04.

### A001:1068–1074

**Old:**

> **Stated so it is not over-read.** A witness shows a class is occupiable by a state a reader could actually record on a named cell; it does not show that any reader will record it. **Every one of the seven read-cell classes has a witness over the 13 read cells, so no class in this table is reachable only in principle.** If the reading step leaves a class empty, that is a fact about the 13 cells and is reported as one - never as evidence about FW5, about the records or about their authors (rule 6).

**New:**

> **Correction to the reachability claim.** The table does not demonstrate that every reading class is occupiable over the registered cells. The A15/A16 entries do not establish joint occupiability. A replacement must interpret the fixed grain, boundary and references consistently across A15–A17 and A21–A23 and exhibit the claimed obstruction or successful reconstruction. Changing the target identifier alone does not answer the shared-defect objection. The Boolean entries lack their required complete exhibits; the X6 and X5 sketches are not certified by this correction. Failure of a proposed witness leaves reachability unestablished; it does not prove the class unreachable. No replacement witness is asserted here.

### Remaining dependent assertions

| Location | Old → New |
|---|---|
| `A001:64–65` | “reachability is exhibited” → “the previous assertion of demonstrated reachability is withdrawn” |
| `A001:123–124` | “whose reachability is exhibited cell by cell” → “whose reachability remains unestablished where the required exhibit is absent” |
| `A001:1048` | “Reachability, exhibited cell by cell (F52)” → “Proposed reader states and outstanding reachability obligations” |
| `A001:1336` | “the reachability table” → “the qualified proposed-reader-state table” |
| `A001:1476–1477` | “each with a named reachability witness” → “with proposed reader states whose reachability has not been fully demonstrated” |

**A001:1298–1301, old reachability assertion →**

> No class is reported as demonstrated reachable without an exhibit satisfying its full condition. A failed proposed witness leaves that obligation open. Any later empty class is reported only within the registered-cell scope and supplies no evidence about FW5.

**A001:1537–1540, old A15 witness assertion →**

> The withdrawn A15 witness identifies an unresolved grain-and-boundary question concerning a defect spanning three records. Record count alone does not establish the claimed reconstruction obstruction.

**A001:1574–1576, old inference from failed witness to unreachable class →**

> The proposed reader states remain attackable. If a proposal fails its class’s full condition, that proposal is withdrawn or corrected; the class’s reachability remains unestablished unless another complete witness supplies it.

These corrections also cover `Cells:186,192–211`. The new round should explicitly identify the corresponding superseded claims in `History/CHANGES-v4.md:14–15,159–168,224–226,245`, without changing that history. **Do not withdraw the distinct E2 accessibility claims.** (`A001:1141–1149,1544`)

## C. Item 6: evidence states

### A001:997–998

**Old:**

> For each per-cell declaration \(d\), the reader records one of two values, each with its required evidence written into the row:

**New:**

> For each per-cell declaration \(d\), the reader records `free`, `not-free`, or `NOT ASSESSED`, with the evidence or missing-assessment reason required for that status.

### A001:1005–1008

**Old:**

> **`not-free`** - the reader records **either** a quoted line of the reading edition that excludes every such \(d'\), **or** the sentence "searched, none exhibited", with what was tried. **The two are distinguished in the row**, and only the first is a record about FW5's text.

**New:**

> **`not-free` has two distinct evidence types:**
>
> - **TEXT-EXCLUSION:** identify all judgment-changing alternatives at the relevant §2 row that respect the leg’s fixed declarations, quote the FW5 clause, and argue why it excludes every such alternative. Excluding only a selected subclass does not complete this record.
> - **SEARCH-NO-EXHIBIT:** list the alternatives actually considered, why they were considered, their admissibility assessments, and the resulting J1/J2. Conclude only: “Among the alternatives recorded here, no admissible judgment-changing alternative was exhibited.”
>
> A quotation without its exclusion argument does not complete TEXT-EXCLUSION. An empty list, an unperformed search, or an unexplained assertion completes neither route. Record the missing assessment as **NOT ASSESSED**, with its reason and evidence type **NONE**. Missing required evidence prevents a Boolean classification; if neither an earlier exit nor X6 or X5 applies, the cell remains X4. SEARCH-NO-EXHIBIT does not establish that FW5 excludes every alternative.

### A001:1348

**Old:**

> the per-declaration free/not-free records

**New:**

> a declaration-evidence subtable keyed by cell, reader and declaration, recording: §2 dependency; original declaration \(d\); judgment supported; status (`free`, `not-free`, `NOT ASSESSED`); evidence type (`FLIPPING-EXHIBIT`, `TEXT-EXCLUSION`, `SEARCH-NO-EXHIBIT`, `NONE`); alternative \(d'\) or alternative class; reason for considering it; quoted FW5 clause where applicable; admissibility or exclusion argument; resulting J1/J2; search scope and limitations; and the reason for any missing assessment

The actual diagnostic worksheet is **NOT FOUND**; this corrects its proposed specification, not an existing filled artifact. (`A001:30–35,1346–1350`; `docs/STATUS.md:253–256`)

## D. Item 7: procedure and table

### A001:954–959 — entire gate step

**Old gate ordering:** (b5)/E3 → X4, then record absence → X0.

**New:**

> **Gate, before any reading: X0 first.** A cell with a record-level absence—in this register, no target record identifier—is X0, and its bridge is not consulted. Otherwise, a cell whose bridge returns (b5), or which is in E3, is X4. Both gated classes remain unread. The existing assignments remain nineteen gated X4 cells and one X0 cell; thirteen cells remain eligible for reading.

### A001:962 — after “names the component.”

**No immediate reconstruction decision → add:**

> Apply X3 immediately if its full condition holds. Otherwise, if the readers do not exhibit the same complete \(\mathcal E_c\) and \(p_\delta\), record X4 and stop reading that cell.

### A001:969

**Old:**

> Otherwise the cell proceeds.

**New:**

> The cell proceeds to J1/J2 only if both readers record that the :620 check passes. An attempted but unevaluable check leaves X4 with no charge.

### After A001:1037

**No explicit early X4 row → add:**

| Order | Class | Condition | Disposition |
|---|---|---|---|
| 1a | X4 UNRESOLVED — explicit exit | After X3 is ruled out, the completed exhibition step does not yield the same complete \(\mathcal E_c\) and \(p_\delta\); or the attempted :620 check fails or remains unresolved; or a disagreement specified by the reading procedure has been established. Apply the exit at the step establishing its condition. | D21 only when both readers record a :620 mismatch; otherwise no charge. Record the actual reason. |

### A001:1040–1043 — condition cells only

Replace their present abbreviated conditions with the following common prefix and respective ending:

> Both readers exhibit the same complete \(\mathcal E_c\) and \(p_\delta\), agree that the :620 check passes, satisfy the shared Boolean-state condition with completed `not-free` evidence for every per-cell declaration, and agree that:

| Class | Exact ending |
|---|---|
| X2 | “(E) holds and the alleged defect does not obtain of the quoted target passage.” |
| X2b | “(E) fails and the alleged defect obtains of the quoted target passage.” |
| X1 | “(E) holds and the alleged defect obtains of the quoted target passage.” |
| X1b | “(E) fails and the alleged defect does not obtain of the quoted target passage.” |

Their disposition and charge columns remain unchanged. (`A001:1040–1043,1088–1091`)

### A001:1010–1014 — entire X5 paragraph

**Old:** X5’s unconditional “if and only if” statement and the following disagreement/Boolean-routing sentences.

**New:**

> After earlier exits are ruled out, X5 fires if and only if the original J1 and J2 are determinate and agreed, and both readers record `free` at the same §2 row, each exhibiting its own judgment-changing alternative. A recorded disagreement about whether a declaration is `free` goes to X4. Alternatives recorded at different §2 rows do not constitute the required same-row agreement. The Boolean rows require neither reader to record `free` anywhere and require completed `not-free` evidence for every per-cell declaration. Missing evidence does not satisfy that requirement.

### A001:1026–1031 — entire ordering explanation

**Old:** the existing rows-1–7/residue explanation and claim that the reachability table answers F52.

**New:**

> X0 and gated X4 are assigned before reading, in that order. For read cells, X3 is followed by the explicit X4 exit at row 1a, then X6, X5 and the four Boolean rows; the final X4 row remains the residue. Apply an exit when the relevant procedural step establishes its condition. Exhaustiveness follows from the residue row. Reachability requires separate complete exhibits and remains subject to this round’s withdrawals and outstanding obligations.

### A001:975

**Old:**

> **Class assignment** by the ordered table, below. First match wins.

**New:**

> **Class assignment.** Retain any exit already established during exhibition or the :620 check. Otherwise apply the ordered table, including any disagreement established during J1/J2 or the free-declaration assessment. First match wins; states satisfying no earlier condition are X4.

The companion’s summary must receive the same dated successor procedure. (`Cells:307–326`)

## E. Item 9: conditional wording

### A001:661–662

**Old:**

> Under (P-Ans): (A) Question fidelity fails, at :208, under every \(\lambda\).

**New:**

> For the fixed parallel organization \(E\), active-route query and declared edit/boundary translations, assuming (P-Ans), (A) fails regardless of the choice of \(\lambda\) while those other data remain fixed.

The remainder of the bullet, its conditional disclaimer, and the alternative reading remain intact. (`A001:663–695`)

**No changes to (r2), (r3), A-S’s disposition, B-N’s disposition, or the charge table are endorsed.** Their reconsideration is separate from these instrument corrections. (`A001:549–560,700–710,829–833,1081–1095`)

## Items 8-11 — assessments only

- **Item 8: (r3), with (r2), remains open.** FW5:1364 supplies the direct sufficiency criterion; FW5:1368 distinguishes criticism of the theory from use of its definition. These do not require a counterexample to survive every proposed amendment. This corrects the draft's citation scope: FW5:228's explicit change example concerns necessity and is not the support for this sufficiency assessment. Neither (r2) nor (r3) is changed; any reassessment of A-S at A001:706-710 is separate.
- **Item 9: conditional wording only.** The current locator is A001:661-662, not the earlier staging locator preserved in item 9. Section E records the exact self-contained successor wording as an assessment proposal only. It neither adopts (P-Ans) nor changes the preserved bullet, its disclaimer, the alternative reading or its verdict (FW5:170,202-208,1402).
- **Item 10: carried debts remain owed.** The explicit candidate-profile equation `Ans_E = Q(E,.,.)` is **NOT FOUND** in FW5; compare FW5:125,128-130,162,202,210. The English conditional rule and the A29 assignment require separate arguments. Cells:175's distinction between an unaddressed question and an undrawn distinction is the companion's interpretation, not FW5's verdict. Disclosure still requires a proportionate argument; the independently sourced interpretive technical case and counterexample-and-clause deliverable remain owed (A001:337-363,1235,1302-1304,1637-1644).
- **Item 11: already handled.** A001:13-21 and REC-20260914-AB record use of `-AB` after `-AA` was taken and rejection of the lexical-sort rationale. This assessment preserves that historical housekeeping outcome and makes no fresh remote-verification claim.

## Separate criticizable contributions — judge section 5

1. **Strengthened evidence schema and prospective routing policy**, including NOT ASSESSED, completed evidence requirements and the early disagreement exit — **proposed, not adopted**; an instrument choice, not a FW5 clause.
2. **Any new grain/boundary interpretation or replacement reconstruction witness** — **proposed, not adopted**; an explicit argument is owed and withdrawal does not authorize boundary expansion (FW5:140,146,154).
3. **Any amendment of (r2)/(r3), adoption of (P-Ans), or other P9 answer-profile rule** — **proposed, not adopted**; separate semantic argument and any separately identified A-S reassessment must preserve its earlier verdict.
4. **Any revision of the English conditional rule or A29's assignment** — **proposed, not adopted**; discussion supplies no demonstrated replacement rule.

## Terminology correction and unchanged verdicts

Draft:378's “no standing determination under K2” → **“no standing determination under FW5:638 and no usability determination under K2 at FW5:642–653.”** K2 defines Usable and uses standing among its conditions; it does not define standing.

**Recorded verdicts unchanged:** A-S failed under **(P-Ans)**, with the missing-definition **D22 alternative**; B-N is **dropped**; A001 supplies **no counterexample to sufficiency or necessity**; the **executable leg cannot charge Account** (A001:700-710,829-833,1081-1095,1268-1272). No provider call or reading step occurred, and no new cell assessment or semantic attribution is recorded.

**Next authorized A001 task:** address items 8-10 and the carried debts as separate arguments. Replacements for the withdrawn witnesses, the complete reachability demonstration, the independent technical case and the counterexample-and-clause deliverable remain owed. Those completed deliverables are **NOT FOUND** in the supplied draft and judge report. This append does not pre-register the executable leg, authorize its reading step or adopt any section-5 contribution.

**Input identities.** Draft SHA-256 `0fe9b56b2fae907dce03f5a3746665ed9a5a9ec55bac41e34ce2a48dff33b400`; judge SHA-256 `def859bdc23865af8d70ed23efc716c75a6c564bd2a3e68c50b8ae3ce1b02b40`. Both supplied inputs remain unchanged.
