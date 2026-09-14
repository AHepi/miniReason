# A001 v2 adversarial review (round 2), pre-publication

Read-only on `/home/user/miniReason` and `a001/`. Read `REVIEW.md`, `CHANGES.md`, `STAGING-v2.md`, `CELLS-v2.md` in full;
re-read **every** FW5 line cited in `STAGING-v2.md` at the line (89 distinct refs, not a sample; edition sha256 re-verified,
1,502 lines); re-hashed all five pins; re-derived the whole cell list from the pinned JSON (22 golden rows, all 46 F001 rows).
Nothing in the repository was written, staged or committed. 21 findings, F30-F50.

**VERDICT: not publishable as v2.** Five blockers; none needs a re-run, all are staging edits. F30 is the serious one: v2's
*one published positive result* — the D6 narrowing — rests on an enumeration that is not exhaustive, and the
counter-construction is three lines. There v2 is smaller than the evidence supports: the mirror of the re-inflation §8.7 warns
of, and equally a regression.

## 1. BLOCKERS

**F30 [blocker] §5(a)(i): the (α)/(β) dilemma is not exhaustive, so the D6 narrowing is wrong.** Claim: "Two cases exhaust it
… **So no endpoint-level abstraction satisfies Anchoring** for a two-route organization whose routes are the anchored
components. This is a stated restriction, not an undefined admissibility condition." Evidence, :176 s1: "the anchoring data
include a port translation for each component, **depending only on the ports of its anchored subnetwork and the explicitly
declared boundary**." s1 restricts what the *port translation* may depend on; it says nothing about how coarse the *declared
abstraction* of s3 may be, and no other line fixes that. **Case (γ), omitted:** route 2's anchored subnetwork in the priority
target has ports {i₂, g, o₂} (g the gate from route 1); declare the abstraction sending any relation over those ports to the
full product over {i₂, o₂} — a function of route 2's own ports alone, so s1 is met. The projected target relation and the
parallel route-2 relation then have the same image, s3's equality holds, and s4 translates every component edit to the same
replacement on both sides. (γ) is neither (α) — it *does* coarsen the component relation — nor (β) — it never mentions
assembled endpoint values. It does exactly what :176 s5 says is prevented: "this prevents local relation matches from silently
losing constraints shared between components." s5 states an effect s1-s4 do not deliver without an admissibility condition on
the abstraction. **That is v1's D6.** A-S does not revive (F31); the narrowing falls. *Fix:* delete the enumeration and the
universal conclusion; restore D6 to "undefined: no stated condition ties the declared abstraction's coarseness to κ or to
constraints shared between components", citing :176 s5 as FW5's own statement of what the missing condition is for; keep
(α)/(β) as what they show — two natural abstractions fail.

**F31 [blocker] §5(a)(i): "neither does any endpoint-level abstraction of FW5's own discriminating pair" is false, and the
heading over-asks its answer.** Heading: "Can **any** endpoint-level abstraction satisfy Anchoring and non-circular dependence
together?" Answer: "**Anchoring: no.**" The proof is guarded to "whose routes are the anchored components"; another λ escapes
it. Carve E as **one** component (the whole parallel network), anchored to the target's whole network as one subnetwork.
:174's "Every active explanatory component has a stated target interpretation under λ" then has one instance; that
subnetwork's projected relation, hidden ports projected away, is the endpoint relation, and by :1402 "Their endpoint outputs
agree", so s3 holds with the port translation depending only on that subnetwork's endpoint ports. Anchoring and (F) hold at
endpoint grain with no coarsening at all. The case still dies — under horn 2 (A) fails at :208 for *every* λ; under horn 1 the
attribution is true. **The clause doing the work is :208 alone, not :176.** *Fix:* narrow the heading to the
routes-as-components carving, delete the quoted sentence, rest A-S's disposition on :208 (and :236 under horn 1).

**F32 [blocker] §5(b): the outcome classes are not exhaustive.** Claim: "**every cell now lands in exactly one of X0-X5**."
Two outcomes have no class. **(a) AGREE-NEGATIVE:** \(\mathcal E_c\) exhibited, (E) **fails**, defect **does not** obtain —
X1/X2 need (E) to hold, X3 needs the defect to obtain, X4 needs disagreement/E3/(b5), X5 needs a free declaration. Homeless,
and it is the concordant case that most supports (K1). **(b) UNDECIDABLE-DEFECT:** both readers agree the quoted passage does
not settle whether the defect obtains — X1 needs "the defect obtains", X2 "demonstrably does not obtain", X4 disagreement.
Homeless. *Fix:* add **X1b AGREE-NEGATIVE** (one supported instance, negative direction, charge none); extend X4 with "or the
two readers agree the quoted passage does not settle the defect"; re-assert exhaustiveness only after the table closes.

**F33 [blocker] §5(b): the charge rule defines an Account-alone charge and denies it in the same paragraph.** "It is charged to
**Account alone** only if \(\mathcal E_c\) is supplied in full by the record's own fields under no A001 bridge and both readers
agree. … **If some cell nevertheless meets it** … the charge is still to (K1)∧(E), not to Account." Literally the third branch
exists and fires; by the closing sentence it never does. So **yes — a cell can charge Account alone under one reading of the
pre-declared rule**, contradicting X2/X3's "never to Account alone" and §6's "no cell of the executable leg can charge
Account". *Fix:* delete the third branch: "There is no Account-alone charge; a cell meeting that condition is recorded as such
and still charged to (K1)∧(E)."

**F34 [blocker] §5(b): X3 is a necessity class inside a leg declared two sentences earlier to have no necessity direction.**
X3: "the defect demonstrably obtains, and the exhibited \(\mathcal E_c\) **fails** (E)" → "a counterexample to (K1)∧(E)".
Against: "there is no necessity direction left in this leg." One failed \(\mathcal E_c\) does not show that none satisfies (E)
— :1364's "cannot satisfy the conditions **under any interpretation** preserving its actual organization", the quantifier used
to kill B-N (F6). As written X3 licenses a counterexample from a failed reconstruction. *Fix:* rename to **X3
RECONSTRUCTION-FAILED**, recording finding 2 at D14/D21 with no counterexample language; or put "under any interpretation"
into the condition and pre-declare that no cell meets it.

## 2. SHOULD-FIX

**F35 [should-fix] §3: no branch for the defect kind FW5 names first; ≥11 of 33 cells die at (b5) unread.** :609:
"**inconsistency**, a false dependency, **a missing distinction**, an unsupported reference, a failed task, a misapplied rule".
(b1)-(b4) cover discrimination failure, frame-vs-rival, prescription-beyond-evidence and reader misreading — neither
inconsistency nor a missing distinction. Measured, on the `bearing` text alone: F001 occ-01 rows 4, 5, 6, 20, 21, 22 ("alleges
an internal inconsistency between raising c6 and leaving c3 and c4 unchanged") → (b5); rows 7, 8 ("counters the choice
architecture implied by the format-change suggestion") → (b5); row 19 → (b5); occ-05 row 8 ("…a question the task text gives
no leverage on and the account leaves untouched") → (b5). With A32 that is 11 of 33 dead before reading. :123 supplies the
missing respect: an internal-inconsistency charge is **impossibility** (cf. :212 s2, "no compatible realization"). *Fix:* add
branches for "two or more of the target's own commitments cannot jointly hold" → κ = impossibility, and for a distinction the
target does not draw → inferential identification; restate §8.5's reach.

**F36 [should-fix] §3: the branches are fitted to the cells they will be applied to, and §3 discloses half the corpus it
read.** §3 declares the rule "**before the reading**" and reports as Measured only "all ten golden `bearing` fields". But (b3)
— "the target's recommendation, ordering or prescription does work its stated evidence does not carry" — paraphrases golden
rows 3/4: "The ordering of the account's recommendations is doing prescriptive work that the stated evidence does not carry."
And (b2) — "treats one reading as **the frame**" — tracks F001 occ-01 rows 0-3: "counters treating c1 and c2 as **the frame**
rather than as one hypothesis among at least two", a corpus §3 never says was read. PURPOSE.md: "fixing the grain, boundary
and contrasts **before examining the relevant evidence**". *Fix:* disclose that both corpora's `bearing` fields were read
first, name the rows (b2)/(b3) derive from, and record in P8 that the rule is not independent of the cells.

**F37 [should-fix] §3: (b2) matches no golden cell; golden rows 0/1 match no branch.** Rows 0/1 (`o1`): "If the driver is
renegotiation or legitimacy rather than ambiguity, the specification move in c2 treats a symptom, and the account's sequencing
… is misplaced." (b1) needs a discrimination claim — absent; (b2) needs a rival "**equally consistent with the same stated
evidence**" — the text is a conditional; (b3) needs "does work its stated evidence does not carry" — "misplaced" is weaker.
First-match-wins ⇒ (b5). *Fix:* declare rows 0/1 (b5), or loosen (b2) and record the loosening as an amendment.

**F38 [should-fix] §5(b): (b5) has two homes and first-match-wins picks the wrong one.** X0 ends "or the bridge returns (b5)"
and charges **D14**; X4 ends "or κ is unresolved at (b5)"; §3 (b5) says "the cell is **unresolved**"; §3's consequence says "an
adverse cell charges **D21 before** it charges D14". First match ⇒ every (b5) cell is X0 at D14, contradicting all three; with
F35 that is ~11 cells. *Fix:* delete "or the bridge returns (b5)" from X0.

**F39 [should-fix] §2, §5(b), CELLS-v2: "records o1, o2, o3 of the objection document" is wrong — the fcl arm covers eight.**
Measured from the pinned table, its 22 `K.*` units cover **o1, o2, o3, o4, c1, c2, p1, u1**. The E2-reachability conclusion
survives (o4 carries no referring row), but the Measured sentence is false and appears three times. *Fix:* name the eight; say
only o1, o2, o3 carry a referring row.

**F40 [should-fix] §5(b): E2's second permitted disposition is unavailable.** "…or a challenge to FW5:1202's applicability at
this grain." :1202: "Suppose **all** carriers, component relations, role bindings, maps, histories, question contracts, and
attribution indices are transported along bijections preserving their structure." The table recodes one document (the
criticism side); the targets `account#c1-c3` are not recoded at all, and :1206 excludes what is not "the stipulated
bijections". No E2 outcome bears on :1202. *Fix:* delete the disjunct; E2 reaches only finding 2 against the table's own
content-preservation argument (D13).

**F41 [should-fix] §5(b): "no second, non-Account route to Bearing **anywhere in the reading edition**" is refuted by the
edition; the survey behind it covers three of eight occurrences.** :900: "effects belong to \(\mathcal R\), purposes to \(G\),
**normative bearing to \(\mathcal N\)**, judgments to appraisal events … **None is defined as another.**" :896: "states that a
reason **bears** on a work in an aesthetic respect" — bearing as a declared normative input, not as Account. The survey (":620
… :622 … :609") also omits :607, :773 ("The objection need not have actual bearing"), and the one that would have helped:
**:1182, "Critical bearing is accounting for the specified defect question."** *Fix:* narrow to "no second route to
\(\operatorname{Bearing}(c,z,p)\)", cite :1182 as the edition's own restatement, and name :896/:900's \(\mathcal N\)-bearing
as a relation the edition keeps separate.

**F42 [should-fix] §5(a)(i): (r1) and the D6 finding-1 contradict each other.** (r1): "the case **fails**, and the finding is
**neither finding 1 nor a counterexample**." Later: "**The one positive result A-S leaves.** D6 is narrowed … That is a
smaller and more defensible **finding-1** than v1's, and it is the form in which A001 publishes it." *Fix:* amend (r1) — "a
case failing under (r1) may still exhibit a missing definition, provided it is stated as a property of the dependency and
charged to the D-row, not as the case's outcome."

**F43 [should-fix] §5(a)(i): F17's exhibition rule binds the worksheet but not the prose case, though :1364 binds it there.**
"Each worksheet row must **exhibit** one \(\mathcal E_c\) … (:1364 'a fully specified candidate')." A-S is never written out:
no Σ, no \(\mathcal C\), no \(O_p\). The :212 s3 dissent then rests on an unexhibited contract — "it still admits deleting the
block of both routes" is asserted, not shown. *Fix:* write A-S's \(p=(D,\Sigma,b_0,\kappa,\mathcal C,\mathcal Q,O_p)\) and
maps into §5(a)(i) under both horns, or mark the dissent **Interpretation, unexhibited**.

**F44 [should-fix] §8.5: a Measured count is wrong — five occurrences supply none, not "four".** F001 occurrences 02, 03, 04,
06, 08 all have `rows` = 0, as §5(b) and `CELLS-v2.md` both say.

**F45 [should-fix] §1(i): ":941" is a heading — the defect F15 fixed elsewhere.** :941 is "`## The retention fixed point`";
the result is (CT2) at :947, statement and proof :950-952, and §1(i) is the one place claiming exact pointers for :1390's
list. *Fix:* cite :947, :950-952.

**F46 [should-fix] §4 finding 3, CELLS-v2: the "no `finish_reason`" half is not at the cited line.**
`material-occurrence-02.json`:1519 reads "…11 FAILED with NO_PUBLIC_CONTENT **and no usage**". "no finish_reason" is at
`…/occurrence-02/material.json`:1483 (and `occurrence-02/plan.json`:82): "every FAILED carries INCOMPLETE_GENERATION with
validation_failure_type NO_PUBLIC_CONTENT, **no finish_reason and no usage at all**". All else verified exact (11 FAILED +
8 PARTIAL + 1 COMPLETE over `occurrence-01/COMPARISON.md` 38-57; "Unresolved in this cell" at 59). *Fix:* cite the second
line, and say **which** `COMPARISON.md` — two exist.

**F47 [should-fix] CELLS-v2: B01 is admitted on a field A001's own bridge forbids reading.** §3: "the bridge rule … **applied
to the `bearing` text alone**." B01's admission rests on its `text` ("whose `text` alleges a defect of the prior m2"); its
`bearing` — "narrows the commitment to a cost rule with an explicit scope, rather than a trigger condition" — alleges no
defect and matches no branch, so B01 → (b5) → dead. *Fix:* pre-declare B01 (b5)/X4, retained as a datum about the `type`
field rather than as a readable cell; or extend the bridge to `text` as a recorded change.

## 3. NOTES

**F48** Delimiter pointers persist: D1's ":85" is `\[` (the tuple is :86); §1(ii)'s projection theorem ":1208-1218" starts at
the section heading (statement :1210-1218). **F49** §6 truncates :1368 mid-sentence with no ellipsis — "not a missing proof of
a theorem" drops "asserted to follow from set theory" — in a document that quotes :1364 "in full, without ellipsis".
**F50** §0 does not say the "Testing FW5 itself" row's deliverable — "A candidate counterexample and the clause or
constitutive claim that would have to change" — is unmet; §6 concedes the owed case, §0's "The two prose legs implement the …
row" does not. The receipt omits the `Letter:` field and the insertions-only / `OPS-20260914-LEDGERCRLF` append note that
`REC-20260914-Y` itself carries (10 of 101 entries); **-Z is the last free letter**.

## 4. What I tried and could not break

- **All 89 FW5 citations checked at the line.** Sound except F45/F48. :1364 verbatim and complete, both halves; :1390's list
  exactly "(M1), (M2), (I2), (O1), (T2), or the retention fixed-point result"; :1402, :1222 (with the "question concerns the
  active route" clause v1 elided), :851 ("(G), (P), or (EK)" — Account indeed absent), :176, :188, :174, :170, :244, :236,
  :212, :210, :208, :1192, :1218, :1224, :1372, :1392, :688, :1404, :989-991 exact. Every round-1 correction landed: :246→:244,
  :133→:140, :987-1012→:989-991, (K1) :614-617 with :620 as gloss, :296 named a heading, :1336-1344 withdrawn with :1342
  quoted against A001's own former use.
- **The :212 s3 dissent is right and costs A001 nothing.** "or one defined to exclude **every** change that could matter"
  reads as ∀x(could-matter(x) → excluded(x)); the second disjunct then has the same shape as the first ("containing only
  notational variants"), as a near-synonymous pair should — so a family admitting one mattering change escapes. **For D10:** it
  keeps :212 s3 and does no work at this locus. **For A001's size:** none either way — under the loose reading A-S fails at
  :210/:212 *as well as* :208, still under (r1), same published result. F2 was wrong on the clause, right that v1 ignored it.
- **All five pins re-hashed exact**, plus the FW5 edition hash.
- **Cell list re-derived, not spot-checked.** Golden rows with non-empty `bearing` are exactly 0,1,2,3,4,10,11,13,16,17, all
  `type: objection`; the 12 declared-use rows and types match row for row. F001 occ-01 bearing rows are exactly 0-8, 12, 19-22
  (A's 13 + B01); occ-05 exactly 3-10; occ-07 row 1 only, `target_record_id` genuinely `None`, resolver note verbatim.
  10+23 = 33. `use-table-full`'s 22 rows are the golden 22.
- **Bridge branches tested on real cells:** (b1) golden 2, 10, 11, 13 clean; (b3) golden 3, 4 clean (too clean — F36); (b4)
  golden 16, 17 clean, `bridge-strained` the right call; (b2) zero golden cells, F001 occ-01 rows 0-3 only; (b5) ≥11 (F35).
- **`RECODING_TABLE.md` exact:** 85 units, fcl 50 = 28 `B.*` + 22 `K.*`, prose 35 = 20 `B.*` + 15 `C.*`. E2's reachable set
  really is golden rows 0-4; 10/11/13 refer from `k3`/`k7`, 16/17 from `n3`, no F001 cell reachable. **E3 exact:**
  `use-table-full` `nodes_not_read` = 12 = 10 `prose_not_parsed` + 2 `unavailable_decode_failure`; F001 = 7, 8, 6, 5, 6, 9, 6, 7.
- **Non-interference re-verified mechanically, not inherited:** zero `runtime_files` entries under `experiments/` or `docs/`
  in any `experiments/**/*.json`; `source_identity()` hashes `src/**/*.{py,json}` + `pyproject.toml` only; `A001` appears
  nowhere in the repository; the two target directories do not exist; v2 adds no path under `src/`.
- **Receipt style re-counted at today's bytes:** 101 `REC-20260914` entries — `Choice:` 95, `Why:` 85 (`Reason:` 9),
  `Contribution:` 90, `Prior verified commit/tree:` 23, full-date stamps; the draft matches all four. `-A`…`-Y` taken, and
  `-Y`'s own text confirms the practice A001 cites.
- **Two-reader rule, ceiling, no ranking.** C001 PLAN:743-745 exact; no vote, majority, average, rate, score or threshold
  anywhere. Rule 6's rewrite is faithful, though it now puts a claim-*enabling* sentence inside a list titled "What would NOT
  constitute a finding" — the only universal claim in reach is (K1), so name it.
- **Withdrawals are real, not relabelled.** The :1218 sentence is gone and the reason given is correct: the theorem's
  hypotheses \(M_0\models\phi\), \(M_1\not\models\phi\) presuppose Account distinguishes the pair, the reverse of what A-S
  needed. B-N is dropped, not demoted. The relinquishment is properly conditional and :226 survives under (a) on its own
  gloss. S1's correction of the D20 label against :1224 is right. §0 discharges F29 in full.
