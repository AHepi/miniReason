# A001 v3 adversarial review (round 3), pre-publication

Read-only on `/home/user/miniReason` and `a001/`. Read `REVIEW.md`, `REVIEW-2.md`, `CHANGES.md`, `CHANGES-v3.md`,
`STAGING-v3.md`, `CELLS-v3.md` in full. Every FW5 line cited in `STAGING-v3.md` re-read at the line (edition sha256
re-verified, 1,502 lines) — including all of :947/:950-:952, occurrence-02/material.json:1483, the eight `K.*` records,
the five zero-row occurrences, :1368 whole, and the eight-locus survey with :896/:900 and :1182. All five pins re-hashed.
The 33-cell register re-derived from the pinned JSON; all 22 golden and all 46 F001 rows read; ledger letters counted
at today's bytes. Nothing written, staged or committed except this file. 17 findings, F51-F67.

**VERDICT: not publishable as v3.** Three blockers. None needs a re-run; all are staging edits. F51 is the serious one:
the single clause v3's whole A-S disposal now rests on carries an unstated premise that the reading edition contradicts
at the line v3's own D10 row cites, and under v3's own λ_w a construction makes (A) hold. F52 and F53 are mechanical:
of the nine outcome classes, **X6 is unreachable and X5 swallows rows 6-9**, so the table that was v2's F32/F34 fix
does not work as a first-match-wins ordering.

## 1. BLOCKERS

**F51 [blocker] §5(a)(i) horn 2, §0, §6, receipt: "(A) fails for every λ" rests on a premise the edition does not
supply and :210 s1 contradicts.** Claim: "**\(\operatorname{Ans}_E\) is a function of \(E\) and the declared question,
not of \(\lambda\)**: no choice of anchoring changes which routes the parallel organization makes active. So (A) fails
under **every** \(\lambda\)". **Evidence.** `Ans_E` occurs in the reading edition at exactly two lines — :162 and :202
(grep, whole file). :162: "An explanatory candidate for \(p\) **supplies** an organization \(E\), an answer profile
\(\operatorname{Ans}_E\), and an interpretation of its active commitments." (Q) at :128-130 defines only
\(\operatorname{Ans}_p(a,b)=\mathcal Q(D,a,b)\) — over the **target**. **No line states
\(\operatorname{Ans}_E=\mathcal Q(E,\cdot,\cdot)\).** The one line saying how a candidate's answer is arrived at is
:210 s1: "The answer follows by evaluating **the anchored organization** under its declared independent boundary
conditions." §2's D10 row quotes :210's *fifth* sentence and omits its first. **The construction, using v3's own
machinery and nothing else:** take \(\lambda_w\), which §5(a)(i) itself certifies ("Anchoring and (F) hold at endpoint
grain, with no coarsening at all") — \(E\) as one component anchored to the target's whole network as one subnetwork.
Evaluate the active-route query on *the anchored organization*, as :210 s1 directs: that organization is the target's
whole network, so \(\operatorname{Ans}_E(\tau(a),\sigma(b))=\operatorname{Ans}_p(a,b)\) on all four assignments and
**(A) holds under \(\lambda_w\)**. A second route to the same place: :197 says "(F) and (C) are applied at the stated
abstraction" and names **neither (A) nor \(\mathcal Q\)**, so whether the query is evaluated at the declared
abstraction is exactly **D6/D7**, which §2 marks *undefined*. Under case (γ)'s abstraction both sides' route-2
relation is the full product and the profiles agree. **v3 cannot have it both ways:** D6 is undefined *and* :208
disposes of A-S at a fixed route grain for every λ. *Fix, minimal:* add a §2 row — "\(\operatorname{Ans}_E\) | :162 |
**undefined**: supplied by the candidate; (Q) defines only \(\operatorname{Ans}_p=\mathcal Q(D,\cdot,\cdot)\); :210 s1
makes the answer follow from *the anchored organization*" — then either (i) argue the :210 s1 reading at the line and
mark the every-λ sentence an **Interpretation**, or (ii) record A-S as failing under **(r2)**, a finding 1 naming the
missing condition, and delete "for every λ" from §0, §5(a)(i), §6 and the receipt.

**F52 [blocker] §5(b): X6 UNDECIDABLE-DEFECT is unreachable, so the F32 fix does not hold.** X4 sits at order 2 and
now fires on "or **either reader records a judgement as undetermined**". X6 sits at order 4 and requires "both readers
agree the quoted passage **does not settle** whether the defect obtains" — a state in which both readers record that
judgement as undetermined. First match wins, so X4 always fires first and **no cell can ever be X6**. The homeless
outcome round 2 named is still homeless; it has only been given a dead label. *Fix:* order X6 before X4, or narrow
X4's disjunct to "exactly one reader records a judgement as undetermined".

**F53 [blocker] §5(b): X5 swallows rows 6-9, so X1, X1b, X2 and X2b are unreachable and the leg can record no
agreement and no conflict at all.** X5 (order 5) fires when the agreed determinate judgements hold "**but only because
a reader supplied a free declaration** at D3, D4, D6, D7, D8 or D10's materiality input". The Modality paragraph
requires every row to write out \(p_\delta=(D,\Sigma,b_0,\kappa,\mathcal C,\mathcal Q,O_p)\). **\(\kappa\) is D3 and
\(\mathcal C\) is D4, both marked undefined in §2**, and \(\kappa\) is supplied by A001's own bridge. No judgement on a
cell exists before those are declared, so the "only because" counterfactual is trivially true of every cell that
reaches order 5 — and "free declaration" is nowhere defined, so two readers have no test to apply. Either reading is
fatal: on the literal one the four Boolean combinations the exhaustiveness argument closes on are dead code; on the
undefined one X5 is undecidable and the register's readable cells have no determinate class. *Fix:* define free
declaration ("a declaration at a §2-undefined row whose variation, within the range §2 leaves open, flips either
judgement"), and pre-declare that the frozen bridge \(\kappa\) and §3's declared \(\mathcal C\), \(\ell\) and \(\beta\)
are the leg's declared constants and do not count as free declarations for X5.

## 2. SHOULD-FIX

**F54 [should-fix] §5(b): a state escapes rows 1-5 and is not one of the four Boolean combinations — the two readers
exhibit *different* \(\mathcal E_c\).** X3 requires that no \(\mathcal E_c\) can be written; X4 lists disagreement "on
the branch assignment, on whether (E) holds, or on whether the defect obtains", and undetermined judgements. Two
readers who each write out a different, internally determinate \(\mathcal E_c\) are in none of these, and the two
judgements are not judgements about one object, so rows 6-9 do not apply either. *Fix:* add "or the two readers
exhibit different \(\mathcal E_c\)" to X4.

**F55 [should-fix] §5(b): X5's D-row list omits the row a reader must actually declare per cell — D13.** §2: "D13 |
structural equivalence at grain … **defined, unmapped** | ':746 structural at the stated grain, not string equality or
similarity'; **no record-level test**". To judge that the defect obtains *of the quoted target passage* a reader must
identify the record's represented target with that passage — a D13 declaration with no stated test. A cell determinate
only because of it falls past X5 into X2/X2b/X1/X1b and is charged as a conflict or recorded as a supported instance.
*Fix:* X5 should name "any §2 row marked undefined, defined-but-unmapped, or declared primitive", not an enumerated six.

**F56 [should-fix] §5(b) rule 6 licenses exactly what the class table forbids.** Rule 6: "a single exhibited instance,
with both passages quoted, defeats a universal claim in the worksheet's own scope … **The universal claim in reach
here is (K1)**". X2: "**Never a counterexample to Account, never to (K1) alone**"; X2b the same; §6: "No cell of the
executable leg can charge Account." Naming (K1) as the universal in reach makes rule 6 a licence for the one output
the table bans. *Fix:* name the universals in reach as A001's own — the bridge's coverage claim and the register-level
D14 claim — and state that no cell defeats (K1), because every \(\mathcal E_c\) carries an A001-reconstructed \(\delta\).

**F57 [should-fix] §3: the tuning disclosure names two fitted branches and there are at least four.** §3 discloses
(b3) (paraphrases golden 3/4) and (b2) (tuned on F001 occ-01 rows 0-3). **Measured, not disclosed:** (b1)'s second
limb — "or has **less discriminating power** than the target claims" — against golden row 2's `bearing`, "the test has
**lower discriminating power** than the account implies"; and (b4) — "asserts only that **a reader will misread** the
target" — against golden rows 16/17's `bearing`, "**If a reader takes k2 at face value** and does not read k7 as
limiting it, the probe will be **over-read**". Four of the six firing branches are fitted, not two. *Fix:* name all
four in §3 and in P8; the disclosure's honesty is the only thing carrying D21.

**F58 [should-fix] §3 / `CELLS-v3.md`: the strict match test says nothing about conditionals, and three frozen
assignments turn on it.** Test: "a branch fires only where the `bearing` text **explicitly asserts** that branch's
stated form." A08's `bearing` (golden 13, `k7`): "**If** pullback-from-form cannot distinguish those, the test is
weaker than k2 suggests…" — the (b1) form appears in an antecedent. A06/A07 (`k3`): "**If** the opening question itself
triggers withdrawal, the rival's own distinguishing observation is contaminated: you cannot tell…". Meanwhile the (b5)
reasons disqualify A01/A02 partly as "**a conditional**, not a rival asserted to be on the table" and A24 as "a
**conditional** re-ordering demand". A second reader could branch A06-A08 either way, which is what freezing was for.
*Fix:* one sentence declaring whether a form stated in an antecedent or consequent counts as explicit assertion, then
re-verify A06-A08 and A24-A31 against it.

**F59 [should-fix] §3 / D21 against FW5:620: the bridge reads the field the defect is not in, and :620 constrains
that.** :620: "**The alleged defect must concern the stated target and respect.**" The bridge supplies \(\kappa\) from
`bearing` alone (§3), while `docs/reviews/fw5-vs-harness-spec-2026-09-14.md`:299 records "(i) No \(\delta\) slot — **the
defect lives in free `text`**". So D21 can supply a respect that does not concern the record's own alleged defect, and
:620 is the clause that makes that a defect of A001's bridge rather than a curiosity. §3 treats the `text`/`bearing`
split only as a fitting risk (B01). *Fix:* state :620 as a constraint on D21, and route a \(\kappa\)/\(\delta\)
mismatch to a named class rather than leaving it to the reader.

**F60 [should-fix] §3, `CELLS-v3.md`: A32 is counted inside (b5)=15 and simultaneously declared outside the bridge.**
§3: "(b5) | **15** | golden 0, 1; … occ-07 row 1", then "one (occ-07 row 1) is X0, because X0's condition … fires
**before the bridge is consulted**". `CELLS-v3.md` sub-register A gives A32's branch as "— *(bridge not consulted)*"
and its (b5) reason row as "*(not reached)*". A cell the bridge was never consulted on is not a (b5) return. *Fix:*
report (b5) = **14**, list A32 separately as bridge-not-consulted; the 18/15 readable split is unchanged.

**F61 [should-fix] §5(a): (r1)-(r3) still leave a residual case with no outcome.** A case that no stated clause
excludes (so not (r1)), that needs no gap-filling condition (so not (r2)), and that fails one of (q1)-(q4) (so not
(r3)) has no assigned disposition — the gap F20 closed for the worksheet and v3 closed again for the classes. *Fix:*
add a fourth clause: "otherwise the case fails on the named qualifier of :1364 and yields no finding."

**F62 [should-fix] §7 receipt: two Measured counts have already drifted, in a paragraph that says it re-measured them.**
Staged: "`docs/DECISION_LEDGER.md` now carries **104** `REC-20260914` entries … closing `Prior verified commit/tree:`
**24**". **Measured at today's bytes: 109 entries and 25** `Prior verified commit/tree:` lines. (`Choice:` 96, `Why:`
86, `Reason:` 9, `Contribution:` 90, `Contribution to the end goal:` 0, 37 CRLF lines — all as staged.) *Fix:* drop the
entry count and the `Prior verified` count, or stamp each with the time it was read; neither adjudicates anything and
both will be stale again at the append.

**F63 [should-fix] §7 receipt: the identifier is the one instruction a publisher cannot execute, and staging gives no
rule.** **Verified:** `REC-20260914-A` … `-Z` are all taken (26 distinct ids over 109 entries; `-Z` opened 11:14 UTC,
`Letter:` field and the `OPS-20260914-LEDGERCRLF` append note both verbatim as staged). The ledger's earlier series ran
`20260912` B-H and `20260913` I-L, so **there is no precedent for a post-Z scheme anywhere in the file.** Staging says
only that the identifier is "determined at the moment of the append, by the appender". *Fix:* state the rule the
appender applies, or say explicitly that choosing the scheme is itself a decision the `Letter:` field must record as
one — otherwise the staging hands the publisher an unexecutable step.

## 3. NOTES

**F64** §5(b) survey: the display \(\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A\) is at **:893**,
not :896; :896 carries only "states that a reason bears on a work in an aesthetic respect". v3's own pointer-discipline
rule. **F65** §2: the pointer fix stops short of two rows it did not list — D13's `:738-746` still opens on a `\[`
(content \(d\equiv_\ell c\) at :742, tag (N) at :743, the quoted sentence at :746), and D18's `:642-651` spans `\[` to
`\]` with the (K2) tag at **:650**. **F66** §5(a)(i) horn 1: "(q2) the original question preserved **fails**" is
imprecise — under horn 1 the candidate preserves the endpoint question throughout; what switches is the challenger's
complaint, not the candidate's \(\mathcal Q\). Say that, not that the candidate fails (q2). **F67** §5(b): X3 and X6
both read "finding 2 at D14 and D21" while the leg declares the D14 finding once and says the reading "cannot produce a
second independent instance of it". Give them X0's wording — one instance of the already-declared finding.

## 4. What I tried and could not break

- **Every FW5 citation in `STAGING-v3.md` checked at the line; no off-by-one found.** :86, (O) :106, :120, :123, :125,
  (Q) :131, :140, :149, :152, :154, :156, :162, :167, :170, :172, :174, :176, :179, (F) :185, :188, (C) :194, :199,
  (A) :205, :208, :210, :212, (E) :223, :226, :228, :236, :244, :296 (heading), (M1) :306, (M2) :315, (I2) :429,
  (O1) :497, (T2) :582, :601, :607, :609, (K1) :617 with display :613-618 and gloss :620, :622, :628, :630, :634, :638,
  :640, :688, :728, :746, :773, :787, :800, :831, :849, :851, :857-859, :896, :900, :902-904, :941 (named a heading),
  (CT2) :947 with display :945-948, statement :950, proof :952, :989-991, :1178, :1182, :1192, :1202-:1206,
  :1208/:1210-1218/:1220/:1222/:1224, :1256-1260, :1336/:1342, :1364, :1368, :1372, :1384-1386, :1390, :1392, :1402,
  :1404, :1502 — all exact. Every round-2 correction landed.
- **:1364 quoted in full without ellipsis; :1368 now quoted whole** with "asserted to follow from set theory" restored;
  :1390's list exactly "(M1), (M2), (I2), (O1), (T2), or the retention fixed-point result"; :851's list "(G), (P), or
  (EK)" with Account absent.
- **The eight-locus bearing survey is right and its Measured word list is exact.** `bearing`/`bears` occurs at :607,
  :614, :622, :773, :896, :900, :1182, plus the compounds at :800, :912 (`information-bearing`), :1005, :1320
  (`standing-bearing`) — nothing else in 1,502 lines. :900's "None is defined as another" is verbatim; :1182's reading
  ("adds the restatement and the placement, adds no test, constituent, predicate or route") is correct against
  :1178-1182.
- **All five pins re-hashed exact**, plus the edition hash `8105925b…e33ee63a` at 1,502 lines.
- **The 33-cell register re-derived independently, not spot-checked.** Rows with a non-empty `bearing` are exactly:
  golden 0,1,2,3,4,10,11,13,16,17 (all `objection`); F001 occ-01 0-8, 12, 19-22; occ-05 3-10; occ-07 1. Total **33**.
  Every referring→target pair in `CELLS-v3.md` matches the JSON row for row, including A20 (`r5`→`m5`), A29 (`o4`→`c2`)
  and A32 (`rival`→`account`, `target_record_id` genuinely `None`, resolver note verbatim). The 12 declared-use rows
  match row, type, referring and target. Golden's 22 rows are byte-identical to `use-table-full`'s.
- **F44's correction is right: five zero-row occurrences** — F001 02, 03, 04, 06, 08 all have `rows` = 0.
- **F39's correction is right.** `RECODING_TABLE.md` = 85 units: fcl 50 (28 `B.*` + 22 `K.*`), prose 35 (20 `B.*` +
  15 `C.*`). The 22 `K.*` units cover exactly **o1, o2, o3, o4, c1, c2, p1, u1**; only o1, o2, o3 carry a referring
  row, so the five-cell E2 reach survives. The golden rows' targets are `account#c1/c2/c3` (node `account`), which the
  table does not recode — so the :1202 withdrawal is correct on its facts.
- **F46's correction is right, both halves and the ambiguity.** occurrence-01/`COMPARISON.md` §"deepseek-flash / fcl"
  (heading :34): table lines 38-57 = 11 FAILED + 8 PARTIAL + 1 COMPLETE, "Unresolved in this cell" at 59. "no
  finish_reason and no usage at all" is verbatim at `occurrence-02/material.json`:1483 and `occurrence-02/plan.json`:82;
  "and no usage" at `material-occurrence-02.json`:1519. `ollama-glm-5.3 / fcl` has exactly one unresolved coordinate,
  control/rep2, PARTIAL. E3's `nodes_not_read` = 12 (10 `prose_not_parsed` + 2 `unavailable_decode_failure`) and
  7, 8, 6, 5, 6, 9, 6, 7.
- **Case (γ) is reproduced verbatim** — word-for-word identical to `REVIEW-2.md` after whitespace normalisation — and
  D6 is restored in v1's exact words. The \(\lambda_w\) record is sound: :174 has one instance, s1 is met, :1402 gives
  s3, (F) at :185 holds. v2's three Anchoring sentences are gone, not relabelled.
- **F33's fix holds literally.** No row of the charge decision table names Account; the third branch is deleted, not
  disclaimed; the antecedent is Measured false (no \(\delta\) slot). **F34's fix holds:** no class carries necessity
  language, and the "under any interpretation" quantifier is pre-declared unreachable.
- **No metric creep.** No count, rate, score, threshold, majority, average or ranking anywhere; branch counts declared
  non-evidence three times; two-reader rule verbatim against C001 PLAN:743-745; ceiling extended, never relaxed.
- **§0 states the skew-matrix relation correctly** — the closing sentence is quoted exactly, the review's result is not
  overturned, A001 is named a second failed candidate — and the "Testing FW5 itself" row's deliverable is quoted
  verbatim from `docs/reviews/FW5-research-plan-decision.md`:27 and recorded as **not met and still owed** in §0, §6
  and the receipt. `Status: proposed, awaiting the user's approval` verified at :3. PURPOSE.md:7 and :19 quoted exactly.
- **Non-interference re-verified mechanically.** Zero `runtime_files` entries under `experiments/` or `docs/` in any
  `experiments/**/*.json`; `source_identity()` is `src/minireason/campaign.py`:35-47 and hashes `src/**/*.{py,json}` +
  `pyproject.toml` only; the string `A001` appears nowhere in the repository; neither target path exists. **The :212 s3
  strict reading still stands**, and it still costs A001 nothing either way.
