# A001 v3 → v4: disposition of every round-3 finding, F51-F67

`REVIEW-3.md` returned 17 findings — **three blockers (F51-F53)**, ten
should-fix (F54-F63) and four notes (F64-F67). Every one is dispositioned below
as **fixed**, **withdrawn** or **declined, with reason**. `STAGING.md` (v1),
`STAGING-v2.md`, `STAGING-v3.md`, `CELLS-v2.md`, `CELLS-v3.md`, `CHANGES.md`,
`CHANGES-v3.md`, `REVIEW.md`, `REVIEW-2.md` and `REVIEW-3.md` are retained
unedited; the revision is `STAGING-v4.md` with `CELLS-v4.md`.

**Headline.** All three blockers are the same defect in three places: **v3 wrote
a rule it could not run.** F51 — a disposal resting on a premise the edition
does not supply. F52 — a class no cell could reach. F53 — a class every cell
reached. v4 fixes them by **naming the premise instead of hiding it** and by
**rebuilding the class table so that exhaustiveness is definitional and
reachability is exhibited cell by cell**. It also applies §3's own strict match
test consistently for the first time (F58), which **moves five cells out of a
respect and empties one branch entirely**.

**Count: 17 of 17 addressed. 16 fixed; 1 (F62's second half) fixed by
re-measurement *and* by stamping rather than by the reviewer's first option, the
reason given. None left open. Nothing declined outright.**

**Direction of travel, stated because both directions are regressions.** v4 is
**smaller** than v3 in what it asserts about FW5's clauses (the every-λ sentence
is withdrawn; five cells lose a respect; one branch empties) and **larger** in
what it discloses against its own bridge (four fitted branches become five;
(b1)'s single surviving cell is the one it was fitted to). No claim was
stretched to close a finding.

---

## 1. The three blockers

### F51 — §5(a)(i) horn 2, §0, §6, receipt: the disposal rested on an unstated premise

**Verified before fixing. Measured at the edition (sha256 `8105925b…e33ee63a`,
1,502 lines, re-hashed at this revision):** `\operatorname{Ans}_E` occurs at
exactly **:162** and **:202**. :162 — "An explanatory candidate for \(p\)
**supplies** an organization \(E\), an answer profile \(\operatorname{Ans}_E\),
and an interpretation of its active commitments." (Q) at :128-130 defines only
\(\operatorname{Ans}_p(a,b)=\mathcal Q(D,a,b)\), over the target. :125 — "The
query operator \(\mathcal Q\) is a specified set-theoretic operation on **the
relevant organization**, its solutions, and, where needed, its component
structure" — does not say which organization is relevant for a candidate.
:210 s1 — "The answer follows by evaluating **the anchored organization** under
its declared independent boundary conditions." :197 — "Equations (F) and (C) are
applied at the stated abstraction and scope" — names neither (A) nor
\(\mathcal Q\). **The reviewer is right on every count: no line states
\(\operatorname{Ans}_E=\mathcal Q(E,\cdot,\cdot)\).**

**Disposition: fixed by the second of the two routes the task allowed — the
disposal is restated as conditional on a named, quoted premise, and the
alternative reading is recorded as a further undefined D-item. No definition
FW5 does not give is invented.**

**Before (`STAGING-v3.md` §5(a)(i), horn 2):**

> **(A) Question fidelity fails, at :208, and it fails for every \(\lambda\).**
> … **\(\operatorname{Ans}_E\) is a function of \(E\) and the declared question,
> not of \(\lambda\)**: no choice of anchoring changes which routes the parallel
> organization makes active. So (A) fails under **every** \(\lambda\), and the
> case is over at :199-208 before any other conjunct is consulted.

**After (`STAGING-v4.md` §5(a)(i), horn 2) — the premise is lifted out, named
and quoted as A001's own:**

> **(P-Ans) — A001's premise, not FW5's text.** A candidate's answer profile is
> the query operator applied to the **candidate's own organization**:
> \(\operatorname{Ans}_E(a',b')=\mathcal Q(E,a',b')\). Under (P-Ans),
> \(\operatorname{Ans}_E\) is a function of \(E\) and the declared question and
> **not** of \(\lambda\).
>
> * **Under (P-Ans): (A) Question fidelity fails, at :208, under every
>   \(\lambda\).** … **This whole bullet is an Interpretation conditional on
>   (P-Ans).**
> * **Without (P-Ans), the case is not disposed of at :208**, and A001 records
>   the construction that shows it [the reviewer's \(\lambda_w\) construction
>   and the :197 route, **both quoted verbatim from `REVIEW-3.md`**].

**Four further changes F51 forces, all made.**

1. **New §2 row, D22**, derived from the text and not from the case (the §5(a)
   proviso requires this): "**\(\operatorname{Ans}_E\): how a candidate's answer
   profile is arrived at** | :162; (Q) :128-130; :125; :210 s1 | **undefined**",
   with the Measured two-occurrence fact, the (Q)/target scope, :125's "the
   relevant organization", and the note that **":210 s1's 'the anchored
   organization' is not a defined term of the edition"** and admits at least two
   readings. The :197 route is recorded in the same row as a second locus.
2. **The disposition of Case A-S is restated as a table by horn and by reading.**
   Horn 1: no finding. Horn 2 under (P-Ans): **(r1)**, fails at :208. Horn 2
   without (P-Ans): **(r2)**, **finding 1**, with the missing condition named
   exactly — *a stated rule fixing how \(\operatorname{Ans}_E\) is arrived at,
   and at which abstraction*.
3. **The claim ceiling is preserved and the case is still not a counterexample,
   by a stated argument rather than by assertion:** (r3) requires that **no
   candidate gap-filling condition** exclude the case; **(P-Ans) is exactly such
   a condition**, it is available, and under it the case fails at :208.
   Therefore **(r3) is unmet on both readings**, and §6's "A001 offers no
   counterexample to sufficiency" stands unweakened.
4. **"for every λ" is deleted as an unconditional claim from §0, §5(a)(i), §6
   and the receipt.** §6 gains an explicit line recording the withdrawal, and
   §8(8)(i) names (P-Ans) as "the single most attackable sentence in the
   document". A new proposal **P9** (a stated rule for \(\operatorname{Ans}_E\))
   is added to §5(c), with the pre-declaration that **proposing it does not make
   A-S's disposal unconditional**.

**One thing recorded and deliberately not relied on.** :210 s2 — "The target
answer is not an unanalysed boundary input or a copied target assertion among
its premises" — is the clause a reply would engage against the \(\lambda_w\)
construction. **A001 does not rest the disposal on it**, because whether
evaluating the anchored organization at \(\lambda_w\) is "copying the target
assertion" is itself undetermined at D22, and using it would re-close at (r1) a
case (r1) cannot reach. It is listed in §8 as a place to attack the document.

**Why A-S was not made a live case with worksheet rows and two-reader cells (the
task's other permitted route), declined with reason.** The two-reader machinery
is built for cells whose subject is a published record; a prose case has no
record, no `bearing` field and no bridge, so the cells would be
two-readers-on-A001's-own-prose, which tests nothing the §5(a) rule does not
already decide. More decisively, a live A-S would be a **candidate
counterexample carried forward**, and (r3) is unmet on both readings — carrying
it live would be exactly the "possible counterexample" §0 refuses.

---

### F52 — §5(b): X6 UNDECIDABLE-DEFECT was unreachable

**Verified: the reviewer is right.** In `STAGING-v3.md` X4 sat at order 2 and
fired on "or **either reader records a judgement as undetermined**"; X6 sat at
order 4 and required "both readers agree the quoted passage **does not settle**
whether the defect obtains" — a state in which both record that judgement
undetermined. First match wins, so **no cell could ever be X6.**

**Disposition: fixed, by restructuring rather than by re-ordering alone,
because re-ordering alone leaves the same trap for the next class.**

**Before:** X4 at order 2 bundled four unlike conditions — the bridge returning
(b5), membership in E3, reader disagreement, and either reader recording a
judgement undetermined — and pre-empted every class below it.

**After:**

* **The two pre-reading conditions become a gate, not an ordered row.** A cell
  whose bridge returns (b5), or which is in E3, is pre-declared X4 in
  `CELLS-v4.md` and **no reader is assigned to it**; a record-level absence is
  pre-declared X0. **19 cells are gated to X4, one to X0, and 13 are read.**
* **X4's reading-level conditions move to the bottom of the table as the
  "otherwise" row.** Rows 1-7 are conditions; row 8 is the residue.
  **Exhaustiveness therefore becomes definitional rather than argued**, which is
  a strictly stronger property than v3's argued exhaustiveness.
* **Every "both readers" class is stated as "both", never "either".** X3
  requires both readers to report no \(\mathcal E_c\) **and name the same absent
  component**; X6 requires **both** to record J2 undetermined. A single reader
  recording undetermined, or the two recording *different* judgements
  undetermined, is a disagreement and falls to the residue row.
* **The class set is still nine** — X0, X3, X6, X5, X2, X2b, X1, X1b, X4 — so
  the nine-class exhaustiveness the task required is preserved, not traded away.

**Reachability is now shown, not asserted (the second half of F52's fix).** §5(b)
carries a **reachability table with one concrete cell per class**, each naming a
reader state argued from that cell's own bytes — X3 at **A15** (an inconsistency
spanning three records against a single-record grain), X6 at **A11**, X5 at
**A04**, X2 at **A03**, X2b at **A05**, X1 at **A16**, X1b at **A12**, with X0
(A32) and X4 (19 cells) already assigned. **All seven read-cell classes have a
witness over the 13 read cells, so none is reachable only in principle.** The
table carries, in bold, that these are **not predictions and not assignments**,
and that a class the reading leaves empty is reported as empty over 13 cells and
never as evidence.

---

### F53 — §5(b): X5 swallowed rows 6-9

**Verified: the reviewer is right on both horns.** The Modality paragraph
requires every row to write out \(p_\delta=(D,\Sigma,b_0,\kappa,\mathcal C,
\mathcal Q,O_p)\); \(\kappa\) is D3 and \(\mathcal C\) is D4, both marked
undefined in §2, and \(\kappa\) comes from A001's own bridge. So v3's "only
because a reader supplied a free declaration" was **trivially true of every cell
reaching order 5**, X1/X1b/X2/X2b were dead code, and the leg could record
neither agreement nor conflict. And "free declaration" was nowhere defined, so
two readers had no test.

**Disposition: fixed, by defining the test operationally and by separating the
register-level fact from the per-cell exhibit.**

**Before (`STAGING-v3.md` §5(b), order 5):**

> **X5 FREE-DECLARATION** | \(\mathcal E_c\) exhibited and both judgements
> determinate and agreed, **but only because a reader supplied a free
> declaration** at D3, D4, **D6**, D7, D8 or D10's materiality input

**After — three parts.**

1. **Declared constants, named and fixed before any reading.** \(\ell\) (D7),
   \(\beta\) (D12), the contrast **requirement** (D4 as declared in §3), and the
   \(\kappa\) delivered by that cell's frozen bridge branch (D3 via D21) are the
   leg's declared constants, identical for both readers, and **not free
   declarations**. §3's contrast declaration is restated as declaring the
   *requirement*, not a family: **the concrete contrast family for a cell
   remains a per-cell declaration.**
2. **The register-level record, so the finding is kept and not re-earned.**
   §5(b) adds, before any cell is read: "**Declaring them constants does not
   make them defined.** That they had to be declared at all is a finding-1 fact
   about FW5's text, it is recorded **once, here, at the register level**, and
   it is **not re-earned per cell**." §6 gains a matching ceiling line.
3. **The operational test, which two readers can apply to the same cell and
   disagree about.** For each **per-cell** declaration \(d\) the reader writes
   into the row, the reader records one of two values **with its evidence**:

   > * **`free`** — the reader **writes out** an alternative \(d'\), admissible
   >   at the same §2 row (the reader can name no line of the edition excluding
   >   it), under which **that reader's own J1 or J2 comes out differently**.
   >   The row records the §2 row, \(d\), \(d'\), and which judgement flips.
   > * **`not-free`** — **either** a quoted line of the edition excluding every
   >   such \(d'\), **or** the sentence "searched, none exhibited" with what was
   >   tried. **The two are distinguished in the row.**
   >
   > **X5 fires if and only if both readers record `free` at the same §2 row and
   > each writes out its own \(d'\).** Exactly one reader recording `free` is a
   > disagreement → X4. Neither → the cell goes on to the four Boolean rows.

**Why this is not the trivial test.** It does not fire on the fact that a
declaration was made; it fires only on an **exhibited** alternative that
**flips a judgement**, agreed at the same row by both readers. **X1, X1b, X2 and
X2b are therefore reachable**, and §5(b)'s reachability table names a cell for
each.

**A second trap of the same shape, found while fixing this one and closed.** X3
would have swallowed everything for the mirror-image reason: no record in the
register carries \(\Sigma\), \(b_0\), \(\mathcal Q\) or \(O_p\). The Modality
paragraph now states, in bold, that **supplying them is the reader's job** and
that **"the record does not carry it" is never a reason to mark a cell X3**; X3
fires only where a reader, having tried, can write **no** admissible value at
all, and both readers name the same absent component.

---

## 2. The ten should-fixes, F54-F63

| id | disposition | where, and what changed |
|---|---|---|
| **F54** — two readers exhibit *different* \(\mathcal E_c\) | **fixed, and by construction rather than by adding a disjunct** | §5(b). The reviewer asked for "or the two readers exhibit different \(\mathcal E_c\)" to be added to X4. v4 makes **X4 the residue row** ("otherwise"), which catches this state and every other one the table does not name. The state is nonetheless **named explicitly** in X4's row — "the readers disagree on the exhibited \(\mathcal E_c\), **or exhibit different \(\mathcal E_c\)**" — so a reader does not have to derive it from the residue. |
| **F55** — X5's D-row list omits D13 | **fixed, and generalised past the reviewer's proposal** | §5(b). The enumerated six are **gone**. The free-declaration test now ranges over **per-cell declarations at any §2 row marked undefined, defined-but-unmapped, or declared primitive**, and the text lists what that includes in this register: \(\delta\) (D14/D15), active-commitment selection (D8), the declared abstraction and component carving (D6), **the identification of the record's represented target with the quoted passage (D13)**, D10's materiality input over D4, and **\(\operatorname{Ans}_{\mathcal E_c}\) (D22)**. |
| **F56** — rule 6 names (K1) as the universal in reach, which the class table bans | **fixed** | §5(b) rule 6. **Before:** "**The universal claim in reach here is (K1)**". **After:** "**The universals in reach here are A001's own**" — (i) the **bridge's coverage claim**, that the frozen branch supplies for every cell it fires on a respect that concerns that record's own alleged defect (:620), defeated by one cell failing the :620 check; and (ii) the **register-level D14 claim**, that no cell's \(\mathcal E_c\) is supplied in full by the record's own fields. Followed by: "**No cell defeats (K1)**, because every \(\mathcal E_c\) in this register carries an A001-reconstructed \(\delta\)". |
| **F57** — two fitted branches disclosed, at least four exist | **fixed, and the count is five, not four** | §3, P8, `CELLS-v4.md`. Re-read at the bytes: **(b1)'s second limb** paraphrases golden row 2 ("the test has lower discriminating power than the account implies"); **(b4)** paraphrases golden 16/17 ("If a reader takes k2 at face value … the probe will be over-read"). Both added to the disclosure. **Beyond what the review asked: (b6) is fitted too** — its stated example, "(e.g. 'alleges an internal inconsistency between …')", **is the `bearing` text of six cells verbatim**. So **five of the six branches that fire or were written to fire are fitted; only (b7) is not, and it fires on nothing.** §3 and `CELLS-v4.md` both carry the consequence as **the strongest available charge against D21**: after F58's rule, **every branch that fires at all fires only on cells whose text its own condition paraphrases**, and A001 records that rather than repairing it. |
| **F58** — the match test says nothing about conditionals, and three frozen assignments turn on it | **fixed, in the direction that fires fewer branches** | §3, `CELLS-v4.md`. The rule is declared: *a form stated solely inside the antecedent of a conditional, or solely inside the consequent of a conditional whose antecedent the same `bearing` text does not itself assert, is not an explicit assertion; "Unless P, Q" counts as a conditional.* Reason given at the line: v3 disqualified A01/A02 and A24 **as** conditionals while branching A06-A08 and A09/A10 on forms inside conditionals, and exactly one treatment can stand. **All 33 cells re-verified against the rule at the bytes. Measured consequence: A06, A07, A08 move (b1)→(b5); A09, A10 move (b4)→(b5); nothing moves the other way. (b4) is emptied. Read cells fall from 18 to 13; (b5) rises from 14 to 19.** |
| **F59** — :620 constrains D21, and the bridge reads the field the defect is not in | **fixed, with a named check and a named charge** | §2 D14 and D21, §3, §5(b). FW5:620 s2 — "The alleged defect must concern the stated target and respect" — is stated as a **constraint on D21**, beside the Measured fact from `docs/reviews/fw5-vs-harness-spec-2026-09-14.md`:299 ("No \(\delta\) slot — the defect lives in free `text`"). It is **not left to the reader**: the reading procedure gains **the :620 check**, performed on every read cell before J1 and J2, in which each reader records whether the \(\delta\) reconstructed from `text` concerns the \(\kappa\) supplied from `bearing`, quoting both. **Both readers recording a mismatch → X4 with a charge to D21** (the one exception in the charge table's X4 row); disagreement → X4 with no charge. |
| **F60** — A32 counted inside (b5)=15 and simultaneously outside the bridge | **fixed** | §3, `CELLS-v4.md`. **(b5) is reported as 14 under v3's branching**, and as **19** after F58; **A32 is listed separately as *(bridge not consulted)*, 1 cell**, because X0 fires before the bridge is consulted and a cell the bridge was never consulted on is not a (b5) return. The distribution table gains a dedicated row for it. |
| **F61** — (r1)-(r3) leave a residual case with no outcome | **fixed, in the reviewer's own words** | §5(a). **(r4)** added: "**Otherwise** — no stated clause excludes the case, no gap-filling condition is needed, and the case fails one of (q1)-(q4) — the case **fails on the named qualifier of :1364 and yields no finding**. The report names the qualifier and quotes it." |
| **F62** — two Measured counts already drifted | **fixed by re-measurement, by stamping, *and* by stating the counting definition; the reviewer's first option (drop them) declined, reason given** | §7. **Re-derived from the bytes at commit `f191f48116a286c2ddcdc54e4663ff307ea9f36b` (tree `0d040f47f9d3282b5f46fcab3a42afe6cccd47fa`), 2026-09-14 14:58 UTC**, over a file of **1,495 lines / 728,439 bytes**. §7 now carries a table in which **every figure names the rule that produced it**, because a bare "entry count" over this file is not reproducible: **lines *containing* `REC-20260914` = 109; lines *beginning* with it = 108; distinct `REC-20260914-<letters>` identifiers = 26, exactly `-A`…`-Z`**; and the two differ by **line 1378**, inside `REC-20260914-S`, which cites `-Q` and `-R` in its text without opening a receipt. A whole-file line-start rule gives 381 `REC-` lines and a paragraph rule 364. **Closing `Prior verified commit/tree:` lines = 25.** The house-style figures are re-verified as staged, each as *lines containing the string*: `Choice:` 96, `Why:` 86, `Reason:` 9, `Contribution:` 90, `Contribution to the end goal:` 0, `Letter:` 5, and **37 CRLF-terminated lines**. *v3 staged "104 entries" and "24", with no definition; the values were stale and the first was undefined — which is why v4 fixes the definition as well as the number.* *Dropping the two counts is **declined**: the receipt's own house-style claim needs a stated denominator to be checkable; instead both are **stamped with the commit and time read**, declared to adjudicate nothing, and declared to be **re-read under a stated definition at the moment of the append** rather than carried from this document.* **Cross-checked against an independent mechanical audit of the same file at the same commit** (1,495 lines; 37 CRLF; 25 `Prior verified commit/tree:`; 26 ids `-A`…`-Z`; no identifier of more than one letter anywhere; 77 `VERIFIED <40hex> TREE <40hex>` lines): **every overlapping figure agrees, and every figure in v4 was re-derived here from the bytes rather than adopted.** |
| **F63** — the identifier is the one instruction a publisher cannot execute | **fixed, by stating the rule as a proposal and by recording that choosing it is itself a decision** | §7, and §3 of this file. **Verified at the same commit:** `REC-20260914-A` … `-Z` are all taken (26 distinct identifiers, over 108 lines opening a `REC-20260914` receipt; `-Z` opened 11:14 UTC); the earlier series ran `20260912` B-H and `20260913` I-L; **no identifier of more than one letter occurs anywhere in the file**; and **neither `AGENTS.md`, `docs/DECISION_LEDGER.md` nor `skills/minireason-experiment-operations/SKILL.md` states any rule for a twenty-seventh receipt in one day.** §7 now proposes **`REC-20260914-AA`** explicitly, records that **A001 does not mint it**, and states that if it is adopted **the `Letter:` field must record the choice as a decision**. The justification a publisher can append as a ledger note is §3 below. |

---

## 3. The notes, F64-F67

| id | disposition | what changed |
|---|---|---|
| **F64** | **fixed** | §1(iii) and the §5(b) survey. The display \(\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A\) is at **:893**; :896 carries only "states that a reason bears on a work in an aesthetic respect". The survey row now reads "**:893** *(display)* **/ :896** *(prose)*", and §1(iii) names the correction as the pointer defect §2's own rule forbids. |
| **F65** | **fixed** | §2. **D13:** `:738-746` → content line \(d\equiv_\ell c\) at **:742**, **(N) tag :743**, quoted sentence at **:746**. **D18:** `:642-651` → standing at **:638**, the \(\operatorname{Live}_j\) definition at **:642**, **(K2) tag :650** (display :644-650). Beyond the note: the inexplicit-representation citation in §5(a)(ii) moves from ":857-859" to **:859**, the line that carries "partial, distributed, or temporally extended" and "memory, imagery, action rehearsal, or interaction with an artifact"; and :1372's branch citation gains its heading line, **:1370**. |
| **F66** | **fixed, in the reviewer's own words** | §5(a)(i) horn 1. **Before:** "**(q2) the original question preserved fails**". **After:** "**Stated precisely: the candidate does not fail (q2)** — it preserves the endpoint question throughout, and \(\mathcal Q\) is unchanged. **What switches is the challenger's complaint, not the candidate's question.**" Horn 1's outcome is restated as **no finding**, and no qualifier of :1364 is recorded as failed by the candidate. |
| **F67** | **fixed** | §5(b). X3 and X6 both take X0's wording: "**one instance of the already-declared register-level finding**", X3 "naming the absent component", X6 "the record did not supply a defect determinate enough for either side to be evaluated" — each with "**never a second independent instance**". |

---

## 4. The receipt identifier — proposal, and the note a publisher can append

**A001 does not mint the receipt.** What follows is a proposal for the publisher
to adopt or reject, and a paragraph the publisher may append to
`docs/DECISION_LEDGER.md` as a note if the proposal is adopted.

**Proposed scheme: `REC-20260914-AA`.** Two letters, lexical continuation, so
that a day's series runs A … Z, AA, AB, … AZ, BA, ….

> **Note for the ledger, if the scheme is adopted.** The 2026-09-14 receipt
> series reached `REC-20260914-Z` at 11:14 UTC, and at commit
> `f191f48116a286c2ddcdc54e4663ff307ea9f36b` the file carries 26 distinct
> `REC-20260914-<letter>` identifiers, `-A` through `-Z`, over 108 lines opening
> a `REC-20260914` receipt (109 lines mention one). No rule for a
> twenty-seventh receipt in one day is stated in `AGENTS.md`, in this ledger, or
> in `skills/minireason-experiment-operations/SKILL.md`, and no identifier of
> more than one letter occurs anywhere in this file; the earlier series (
> `20260912` B-H, `20260913` I-L) never reached Z, so there is no precedent
> either way. The scheme adopted here is **two letters in lexical continuation
> — `-AA`, then `-AB`, and so on — chosen because it extends the existing
> single-letter convention without reinterpreting any identifier already
> appended, because it sorts after every single-letter identifier under the
> ordinary lexical comparison a reader or a grep would apply within a fixed
> date, and because it leaves the `REC-<date>-<identifier>` shape and every
> existing cross-reference untouched.** The three alternatives considered and
> not taken were: rolling to the next date (rejected — the receipt is not from
> the next day, and backdating or postdating a receipt is the one thing the
> cadence rule forbids); a numeric suffix such as `-27` (rejected — it makes
> identifiers of two kinds within one day and breaks the lexical ordering
> against A-Z); and reusing a letter with a discriminator such as `-A2`
> (rejected — a reader grepping `REC-20260914-A` would match two receipts).
> **Choosing this scheme is itself a decision, and it is recorded as one here
> rather than performed silently in the identifier.** The `Letter:` field of the
> receipt that first uses it states what was found in the ledger, that the
> single-letter series was complete, which scheme was adopted and why, and that
> the identifier taken was free at the moment the ledger was read.

**If the publisher rejects the scheme**, the receipt takes whatever identifier
the publisher's own rule yields and the `Letter:` field records that rule
instead. `STAGING-v4.md` §7 says so explicitly, so no version of this staging
hands a publisher an unexecutable step.

---

## 5. What v4 left exactly alone

Kept unchanged, as verified by three reviews: the **:1364 quotation in full
without ellipsis**; **:1368 quoted whole**; the **:1390 list** exactly as "(M1),
(M2), (I2), (O1), (T2), or the retention fixed-point result"; **:851's list
"(G), (P), or (EK)" with Account absent**; the **8 PARTIAL / 11 FAILED** split
with its lines and its labelled inference; the **five pins**, re-hashed exact,
and the **edition hash at 1,502 lines**; the **33-cell register** in its two
sub-registers with the 12 declared-use rows; the **five E2-reachable cells** and
the three-cell overlap with the read cells; the **E3 exclusions**; the
**eight-locus bearing survey** and its Measured word list; **case (γ)** and
**\(\lambda_w\)**, both verbatim; the **:212 s3 strict reading**; the
**two-reader rule** (FW5:634; C001 PLAN §8a:743-745 — no vote, no majority, no
threshold); the **charge table's "no" in every row**; and the **non-interference
facts**, re-verified mechanically at this revision: zero `runtime_files` entries
under `experiments/` or `docs/` in any `experiments/**/*.json`;
`campaign.source_identity()` (`src/minireason/campaign.py`:35-47) hashes
`src/**/*.{py,json}` plus `pyproject.toml` only; the string `A001` appears
nowhere in the repository; neither target directory exists.

**No metric, score, rate, percentage, threshold, majority, average, ranking or
progress meter appears in v4**, and the branch and cell counts are declared
non-evidence in three places. **No "exhaustion" language appears**; the
2026-09-14 single-letter identifier series is described as **complete** and as a
**naming boundary**, never as exhausted.

**Nothing in the repository was written, moved, staged or committed by this
revision.** All work is under `scratchpad/a001/`: `STAGING-v4.md`,
`CELLS-v4.md`, `CHANGES-v4.md`, beside the unedited `STAGING.md`,
`STAGING-v2.md`, `STAGING-v3.md`, `CELLS-v2.md`, `CELLS-v3.md`, `CHANGES.md`,
`CHANGES-v3.md`, `REVIEW.md`, `REVIEW-2.md` and `REVIEW-3.md`.

---

## 6. What a fourth reviewer should attack first

In this order. The first three are where v4 is most likely to be wrong; the last
four are where it is most likely to have overcorrected.

1. **(P-Ans), §5(a)(i).** The premise horn 2's disposal now rests on. Attack it
   two ways: (i) find a line of the edition that *does* fix
   \(\operatorname{Ans}_E\), which would make D22 wrong and restore v3's
   unconditional sentence; or (ii) argue that :210 s1's "the anchored
   organization" **must** mean the explanatory organization under its anchoring,
   which would also restore it. Either way, check that A001 has not quietly used
   (P-Ans) anywhere it is not labelled — search for every sentence about
   \(\operatorname{Ans}_E\) and confirm each is marked conditional.
2. **The conditional rule of §3, and the five cells it moved.** It is a rule
   about English, not a reading of FW5, and it is the single change with the
   largest effect on the register. Re-read A06-A10's `bearing` fields at the
   bytes and ask whether a second reader would branch them the other way — and
   whether the rule, applied strictly, should also have moved A29 (which asserts
   "the account leaves untouched" outright) or A18-A20.
3. **The reachability witnesses, §5(b) and `CELLS-v4.md`.** Seven claims, each
   that a named cell could be placed in a named class by a state a reader could
   record. **The X3 witness at A15 is the weakest**: it argues that a
   three-record inconsistency has no admissible single-record \(D\), which may be
   a reason to vary the grain rather than to fail the reconstruction — and the
   grain is declared constant. If that witness fails, X3 may be unreachable and
   the table needs rebuilding a third time.
4. **The free-declaration test's `not-free` branch.** "Searched, none exhibited"
   is a weak record that could become a default, which would make X5 unreachable
   — the mirror of the defect F53 caught. Check whether the worksheet's columns
   force a reader to say which of the two `not-free` evidences was given.
5. **The :620 check's placement.** It charges D21 from inside X4, which is the
   only row of the charge table with an exception. Ask whether an exception in
   the one class that charges nothing is a seam, and whether a :620 mismatch
   should have its own class instead — and if so, whether the table can stay at
   nine.
6. **§3's disclosure, in the other direction.** v4 now says five of six branches
   are fitted and that every firing branch fires only on cells it paraphrases.
   Check that against the bytes; if it is **overstated**, A001 has conceded more
   than the evidence supports, which §8(7) names as a regression of the same
   kind as re-inflation.
7. **The receipt.** A count table stamped at one commit, and a proposed
   identifier scheme A001 does not mint. **Attack the definitions before the
   numbers**: v4 claims 109 lines *containing* `REC-20260914` and 108 *opening*
   a receipt, differing at line 1378 — check both rules at the bytes, check that
   every other figure in the table names its rule, and check that no sentence
   anywhere in v4 treats any of them as adjudicating anything. Then re-count at
   the ledger's bytes at the moment of reading, since all of them move.

---

## Appended review round 4 — 2026-09-15 05:14:18 UTC — REC-20260915-C

This dated entry records [A001 round 4, F68-F72](../A001-account-challenge-2026-09-14.md#review-round-4), applied after the eleven carried open items from a draft by one Astra worker and the authoritative independent judgement of a second. All preceding history bytes are preserved. These are corrected successor specifications and withdrawals, with no completed reading or adopted section-5 contribution.

| Carried item | Finding | Disposition | Successor location and remaining obligation |
|---|---|---|---|
| 3 | F68 | **fixed** | A001 round 4 section A; correct (b6) provenance, retaining the rule and assignments. A substantive assessment of fitting remains owed. |
| 4 | F69 | **withdrawn** | Section B; A15 witness and completed reachability claim withdrawn, A16 conditional. Replacement witnesses and the full reachability demonstration remain owed. |
| 5 | F70 | **fixed** as conditional specification | Sections B and D; shared Boolean condition and A05-specific alternative assessment. Completed exhibits are **NOT FOUND**. |
| 6 | F71 | **fixed** as proposed specification; overstated draft premise **declined with reason** | Section C; existing evidence requirement is acknowledged; explicit incomplete status and evidence types recorded. Actual worksheet is **NOT FOUND**. |
| 7 | F72 | **fixed** as prospective specification | Section D; consistent gates, exits and complete Boolean conditions. Strengthened evidence/routing proposal remains **proposed, not adopted**. |

**Earlier claims qualified by this new round:** CHANGES-v4:14-15,159-168,224-226's demonstrated-reachability assertions are superseded by F69-F70's withdrawals and outstanding exhibits. CHANGES-v4:245's (b6) stated-example disclosure is superseded by F68's dated correction. The earlier paragraphs themselves are unchanged; the distinct E2 accessibility claims are retained. The companion receives a dated correction for Cells:158-159,186,192-211,307-326.

Items 8-11 are assessments only. Section E's A001:661-662 wording is recorded as an item-9 assessment proposal; (r2), (r3), (P-Ans), A29, the charge table and all recorded case verdicts are unchanged. A-S failed under (P-Ans), with the D22 alternative; B-N dropped; no counterexample to sufficiency or necessity; the executable leg cannot charge Account. Judge section 5's four contributions are explicitly **proposed, not adopted**. The independent technical case and counterexample-and-clause deliverable remain owed. No provider calls or publication under this receipt.
