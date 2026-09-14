# FW5 versus harness spec v1.3 — findings appendix

**This is supporting material for
[`fw5-vs-harness-spec-2026-09-14.md`](fw5-vs-harness-spec-2026-09-14.md). The
review's Appendix A is authoritative wherever the two differ.** The review is
the document root reads; this file exists so that every raised finding, and the
refuter's verdict on it, can be inspected in full rather than in the review's
one-line summary. A finding recorded below may have been narrowed, re-aimed,
split or struck in the review, and the review's disposition governs.

This file is generated mechanically from the critics' `critiques.json` and the
refuters' `refutations.json` by `render_findings.py`, kept with those sources in
the session scratchpad. No field is edited, abridged or reworded here; the
script adds only headings, field labels and this header. 47 findings were
raised across 6 axes; 19 carry a refuter verdict of `stands: true`.

Field meanings are the critics' and refuters' own. A critic's `verdict` is one
of helps / hinders / neutral / mixed / split / absent-in-spec, and `confidence`
is that critic's stated confidence in the finding — it is not a score of any
artifact, model or claim, and nothing here aggregates. A refuter's `stands`,
`misreads_fw5` and `misreads_spec` are that refuter's judgement after checking
every citation at source; `corrected_finding` is the refuter's restatement of
what survives.

No label, count or confidence value in this file is a semantic attribution. The
conclusions are offered to root, who alone interprets them.

Published under receipt REC-20260914-P.

---

## Axis 1 — construction-vs-adjudication: FW5 on how explanations are CONSTRUCTED (accounts, reasons, bearing) versus harness-spec v1.3's attack/support relations and computed accepted/refuted/suspended statuses

**Critic's overall assessment.**

On this axis the spec is mostly orthogonal machinery wearing semantic clothes, and the clothes are what hinder. FW5's central object is a construction — a structural account E=(E,p,π,τ,σ,λ) whose adequacy is the five-conjunct predicate (E) at FW5:217-224, which "contains no predicate that already means 'really explains'" (FW5:226) and which "No separate approval event creates" (FW5:244). The spec's central object is a computed label over two edge sets ("Inputs to adjudication are `att` and `dep` ONLY", spec:229). These are not rivals: the spec's four labels are silent on every conjunct of (E), and (E) is silent on whether anyone attacked anything. Read as bookkeeping — which is exactly how the repo already reads it (AGENTS.md:11 "mechanism guide"; the importer's I7 banner "No label produced by this import is a semantic attribution") — the spec helps in two specific places: `overrun` honours FW5:688 ("The inability to evaluate a proposition is not a falsifying observation"), and the ν/closure apparatus gives a recomputed, non-curated record of why a criticism stopped counting, which is the mechanical form of FW5's demand that scrutiny "be able to affect the operative target" (FW5:63) and that an interpretation "not silently lose its actual dependencies" (FW5:690). It hinders in four: (i) grounded semantics makes silence a warrant, and on the one real FW5-shaped corpus this produces 14 accepted of 17 artifacts including two unparseable ones — "accept-by-position ... no standing is implied" is a residue note, not a spec sentence; (ii) `dep`'s conjunctive `supported(a) = all(...)` cannot hold two distinct sufficient routes, contradicting FW5:657 and FW5:682 directly, and on H005 `dep` was empty and pass 2 the identity; (iii) §7's `hv-floor` launders a survivor-count into `refuted`, which FW5:381/851 forbids as a numerical warrant; (iv) §0's "Status is computed, never stored as ground truth" collides with FW5's *standing* (FW5:638), and the repo's engine consequently drops the authored `uptake` record "from the mechanism" (engine-design-of-record:372) — deleting the only field in the H005 material that records what an author actually took up. "Status" is therefore not an FW5-meaningful quantity: FW5's three nearest objects are appraisal-indexed Usable_j (K2, FW5:642), receipt sets that are "descriptions of available arguments, not four kinds of reality" (FW5:684), and episode-closing engagement decisions that "do not prove that the problem is solved" (FW5:777) — none of which is a single global function of an edge set. What an account must contain and the artifact/interface cannot express: λ (anchoring), κ (respect), Σ∩C (contrast contract), the grain ℓ, the boundary β, and — measurably — a criticism's grounds and its grounds→defect connection, for which the importer had to mint the residue code `grounds_absent_on_objection` with the note "the validity node carries text + bearing (+ scope) only; no grounds field exists". Keep §0's measure/adjudication firewall, §1's ν and closures, and budget honesty; drop or rename the verdict vocabulary; replace conjunctive `dep` with route sets; and make operative consequence, not label, the primitive the mechanism computes.

**Refuter's axis summary.**

Checked all eight findings against FW5 at the cited lines and against harness-spec-v1.3 in full. No finding misquotes FW5; every quoted line says what the critic reports. The damage is on the spec side and in how FW5 lines are applied.

Two findings collapse as written. CA-4 ("no field for grounds; bearing inexpressible") contradicts spec:115 ("a bare verdict is never an edge"), spec:102 (`trace_ref`) and spec:199-204 (mandatory trial transcript with a resolvable `decisive_point`); ν's "sound & relevant" (spec:103) is the spec's bearing carrier, so the verdict should be "hinders on granularity", not "absent-in-spec". CA-5's §0-breach charge inverts §0:33, which names the commitment route as a licensed channel and states the invariant as "MUST NOT appear as inputs to label computation" — ŝ is not a §4 input; it also drops FW5:851's decisive word "automatic" (the hv-floor warrant carries four attackable ν assertions, spec:303/307) and strawmans §17 two sentences after quoting §17:580, which names the tension exactly.

CA-6 stands only in its "neutral" half: K3's disjunctive conclusion IS expressible via spec:227 plus spec:226 (conjunction artifact with dependence refs on T, B, I), and case-law reinstatement is per-warrant with §4 recomputation (spec:187), not wholesale.

CA-1, CA-2, CA-3 and CA-7 stand in narrowed form. CA-1 loses its agency limb (Refl spec:173, N1 spec:233 make appraisal error and the adjudication rule attackable) and its modality limb (spec:410 + spec:32); the surviving core is the missing application/respect index and §4's silence about what its labels are. CA-2 loses the schema limb — content is Σ* and §0:30/§10.1 make an account declaration a content convention, so adding a typed block would violate untypedness — leaving a placement complaint about §4's normative text. CA-3 loses the interference and collective-block limbs (conjunction already models collective contribution; interference belongs on the attack side) and the record-granularity limb (an importer choice, not §1), leaving the genuine disjunctive-route gap in spec:219. CA-7 keeps its core — grep confirms no obligation or Repair vocabulary anywhere in the spec — but loses the FW5:657 framing and the indistinguishability claim, which spec:244 and spec:366 refute.

CA-8 survives both attacks intact, including its "operative consequence is derived from status" line, which spec:181/185/191/251/269/280 support.

Sources read: /home/user/miniReason/docs/sources/FW5-explanatory-construction.md and /home/user/miniReason/docs/sources/harness-spec-v1.3.md. No files modified; no scratch files written.

### CA-1

**Finding id.**

CA-1

**FW5 claim.**

FW5:684 "The record can indicate that neither set, one set, or both sets are nonempty. These are descriptions of available arguments, not four kinds of reality." FW5:638 "Standing is the system's enacted permission to use a content in a particular application and respect. It may be explicit or inexplicit." FW5:642 (K2) Usable_j(u) ⟺ Lic_j(u) ∧ Scope_j(u) ∧ ∀d∈Prem(u), Live_j(d;u), with FW5:653 "The actor can violate this coherence condition." FW5:777 "Closing an episode is an engagement decision ... It does not prove that the problem is solved."

**Spec mechanism.**

§0 spec:32 "Status is computed, never stored as ground truth"; §4 spec:206-229, four terminal labels accepted/refuted/suspended/suspended_unsupported, with spec:229 "Inputs to adjudication are `att` and `dep` ONLY."

**Verdict.**

hinders

**Argument.**

The spec's status and FW5's nearest objects differ on three structural properties at once, so the word "status" imports a quantity FW5 does not have. (a) Indexing: K2 is relative to an appraisal j and an application u; the spec's status is a single global function of the graph per artifact id. (b) Agency: standing is *enacted by the system whose content it is* and can be violated by that actor (FW5:653) — an error the model then represents; a computed fixpoint cannot be violated, so it cannot represent an appraisal error at all. (c) Modality: receipt sets are records of what arguments are available (FW5:684), episode closure is an engagement decision (FW5:777); a label is neither. The collision is not merely terminological: because §0 forbids stored status, the repo's engine explicitly deletes the one authored field that carries FW5-shaped standing. Note the spec is not naive here — it never claims its labels are truth — but it also never supplies a name for what they are, and the repo had to invent one (the I7 banner).

**Repository evidence.**

/home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md:372 — "| `uptake: [Ref]` | **drop from the mechanism** | A self-declared standing label; §0:32 says status is computed, never stored. Rendered and reported only ... never an input to §4". The H005 FCL-1 documents carry `uptake` lists; the importer's closed residue vocabulary records `uptake_refs_unmapped` at severity **unmapped** with 32 refs on the full occurrence, and `uptake_lists_unmapped` at document unit (/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/importer/src/minireason/graph_import_h005.py:99-100, NOTES.md §6.6). The importer's own I7 banner (graph_import_h005.py:88-93) states the disclaimer the spec omits: "No label produced by this import is a semantic attribution."

**Testable consequence.**

Decidable offline on existing H005 evidence: for each artifact in the imported occurrence, ask whether the computed label is invariant under change of appraiser and of application. It is, by construction — the label is one scalar per id with no j and no u index — while the authored `uptake` lists differ per node, i.e. the material already carries appraisal-indexed standing that the label cannot represent. Count: 32 unmapped uptake refs versus 17 labels.

**Proposed change.**

Rename the §4 output from `status` to `adjudication_record`, and rename the labels to what they mechanically are: `no_surviving_attacker` / `attacked_by_surviving_critic` / `contested` / `dependency_not_standing`. Separately, reinstate `uptake` as a first-class *recorded* relation (author-asserted standing, never computed, never an input to §4) rather than dropping it — FW5:638 makes standing an enacted fact, and §0's prohibition is on computed status masquerading as ground truth, not on recording what an author declared it used.

**Confidence.**

0.85

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

All four FW5 quotations are accurate (684, 638, 642-651, 653, 777). But two of the three limbs fail against the spec's actual text. Limb (b) — 'a computed fixpoint cannot be violated, so it cannot represent an appraisal error at all' — ignores spec:173 (Refl: 'adjudication semantics ... are registered artifacts in A, attackable'), spec:233 (N1: every status admits an exit, nothing is ever marked final), and the ν apparatus (spec:107). FW5:653's own follow-on sentence is 'A record declaring a dependency does not establish that the dependency is actually essential; an error in that declaration is another criticism target' — which is exactly what attacking the declaring artifact does in the spec. So appraisal error is representable; what is not representable is the appraiser index. Limb (c) is also overstated: spec:410 says in terms 'Grounded semantics is exactly as skeptical as its attack supply (unattacked ⇒ accepted)', which makes the label a description of attack availability, i.e. the same species of object as FW5:684's receipt-set description, and spec:32 already denies it ground-truth standing. Limb (a) partly fails too: FW5's index j is an appraisal, and the harness is a single appraiser with 'one global graph; one global court' (spec:416), so a fixed j is a stipulation, not an omission; the u/respect index is the genuine gap. Finally the repo_evidence mis-attributes: v1.3 has no `uptake` field, so the spec did not 'delete' anything; the repo's engine note is one reading of §0:32, and §0:32 forbids stored status treated as ground truth, not recording an author's declaration — the finding's own proposed_change concedes this. Confidence 0.85 is too high.

**Refuter — Corrected finding.**

The §4 output is named `status` and its labels (`accepted`/`refuted`) are borrowed from a vocabulary of standing, but the computed object is indexed only by artifact id — it carries no application/respect index, whereas FW5's Usable_j(u) (FW5:642-651) is indexed to an application u and a respect. The spec never states in normative text what its labels are or are not, leaving the naming hazard unmitigated inside §4 itself. It is NOT true that the spec cannot represent an appraisal error (Refl spec:173, N1 spec:233, ν closure spec:107 all make declarations and the adjudication rule attackable), nor that labels masquerade as reality (spec:32, spec:410). Recommended change reduces to: name the §4 output for what it computes, and say in §4/§17 that a label carries no application- or respect-index.

### CA-2

**Finding id.**

CA-2

**FW5 claim.**

FW5:217-224 (E) Account(𝓔) ⟺ Anchor ∧ Fidelity ∧ QuestionFidelity ∧ NonCircularDependence ∧ NonVacuity, over 𝓔=(E,p,π,τ,σ,λ) (FW5:167-170). FW5:226 "It contains no predicate that already means 'really explains.'" FW5:244 "No separate approval event creates an account. The maps can exist before anyone discovers them."

**Spec mechanism.**

§4 spec:205-207 `label0(a) = accepted if a ∈ G`, where G is the grounded extension — i.e. an unattacked artifact is accepted. §1 spec:37-64 Artifact schema: `{content_ref, codec, interface:{commitments, refs:[{target, role}]}, warrants, provenance}`.

**Verdict.**

hinders

**Argument.**

Grounded semantics makes absence of criticism into positive standing. FW5 makes adequacy acceptance-independent in the *other* direction: an account is adequate or not before anyone appraises it (FW5:244), and correspondingly no non-appraisal makes it adequate. So `accepted` and `Account(𝓔)` are logically independent — an artifact with no anchoring, no declared question and no contrast contract is `accepted` the moment nobody attacks it, and a fully anchored account is `refuted` the moment one unattacked critic lands. The spec knows its court "is exactly as skeptical as its attack supply" (spec:410) but supplies no vocabulary that keeps a reader from reading `accepted` as standing. This is the axis's core: adjudication computes a property of the *criticism supply*, construction is a property of the *artifact and its target*. The spec's own §0 firewall shows it understands the difference for measures; it does not apply the same firewall to its own labels.

**Repository evidence.**

The importer had to write the disclaimer into the residue detail verbatim: "accept-by-position: unparseable contribution receives a label because nothing criticises it; no standing is implied", and the `why` text for an unattacked artifact says "accept-by-position, not merit" (NOTES.md §2.1). Golden graph on daily/mini_fcl/cycle01: |att| = 4, dep = ∅, 17 artifacts, **14 accepted / 3 refuted / 0 suspended** (NOTES.md §3) — including the two `opaque_envelope` artifacts whose commitment surface could not be parsed at all. NOTES.md §3 closes: "`A_carry` is accepted because nothing came after it, and `A_rival` is reinstated because `A_carry` happened to attack `A_response`. One cycle of `fork5` has no more criticism in it."

**Testable consequence.**

Already decided offline on H005 occurrence-01: 14 of 17 artifacts are `accepted` and not one of them had any of (E)'s five conjuncts assessed, because the spec's schema has no field in which π, τ, σ, λ, p or κ could have been declared. The discriminating observation for any future occurrence: exhibit one artifact labelled `accepted` that fails anchoring (FW5:174) — trivial to produce, and the two OPAQUE artifacts already are such cases.

**Proposed change.**

Spec §4 must state, in the normative text and not only in the repo's downstream banners, that `accepted` means "carries no surviving warranted attack in this graph" and entails nothing about explanatory adequacy; and §17's residue should add this as a named non-goal alongside "Does not manufacture good conjectures" (spec:578). Optionally add a distinct, never-computed `account_declaration` block to the Artifact interface (question, respect, grain, boundary, anchors) so that the absence of an (E) assessment is visible in the graph rather than invisible behind a green label.

**Confidence.**

0.88

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

FW5:217-224, 226, 244 are quoted correctly and the logical-independence claim between `accepted` and Account(E) is right. But three supporting limbs misdescribe v1.3. (i) 'The spec knows its court is exactly as skeptical as its attack supply but supplies no vocabulary that keeps a reader from reading accepted as standing' — spec:410 IS that vocabulary, and §17:578 adds 'Guarantees faithful bookkeeping (statuses, reinstatement, no relapse, replayable trace). Does not manufacture good conjectures.' The complaint is that these sit in §11/§17 rather than §4, which is a placement point, not an absence. (ii) 'The spec's own §0 firewall shows it understands the difference for measures; it does not apply the same firewall to its own labels' — spec:32 ('Status is computed, never stored as ground truth') is precisely a firewall on labels; the finding reads §0 as measures-only. (iii) The testable_consequence's load-bearing claim — 'the spec's schema has no field in which π, τ, σ, λ, p or κ could have been declared' — is a misreading of §0:31 (content is Σ*, opaque bytes + codec) together with §0:30 (discipline enters 'through problem criteria, content conventions, standard artifacts' — never through types) and §10.1, where exactly such a declaration is shown being made as a content convention plus a `skeleton-wf` program commitment. An account-declaration block is therefore already constructible; adding it as a typed interface field would violate the spec's untypedness invariant, so the proposed_change's optional half is at odds with §0.

**Refuter — Corrected finding.**

`accepted` in §4 names survival of the criticism supply, not adequacy, and the two are logically independent of Account(E) (FW5:217-224, 244) in both directions. The spec states this correctly but only at spec:410 and §17:578, never in §4's normative text where the label is defined; §4's bullets stop at 'orphaned ≠ false' (spec:226). Fix is a one-line normative gloss in §4 plus a named §17 non-goal. Drop the schema claim: content is Σ* and §0:30/§10.1 make a structural-account declaration a content convention plus pinned criteria, which is the spec's designated mechanism, not a missing field.

### CA-3

**Finding id.**

CA-3

**FW5 claim.**

FW5:657 "Suppose a system withdraws an essential premise of u ... Another argument v for the same conclusion can remain usable. The conclusion is not thereby false." FW5:682 "Distinct sufficient routes remain distinct receipts ... A refutation by an independent disjunct must not inherit the disputed assumptions of an unused disjunct." FW5:267 "No upward closure is assumed. Adding an active, incompatible premise can spoil a route. No minimal member is assumed. The whole family, rather than a selected minimal subset, is the basic support object."

**Spec mechanism.**

§4 spec:211-213 `supported(a) = all(final(b) == accepted for (a,b) in dep)`; `if label0(a)==accepted and not supported(a): final(a) = suspended_unsupported`. §1 spec:53, 62 — a `dependence` ref "contributes a support edge"; "`dep` MUST remain a DAG. Reject any dependence ref that would create a cycle."

**Verdict.**

hinders

**Argument.**

`dep` is a single conjunctive relation: every declared dependence must stand for the dependent to stand. FW5's support object is a *family of sets* S_{E,p} (FW5:254-262) — several distinct sufficient routes, none minimal, none upward-closed. Three consequences the spec cannot express. (1) Disjunctive support: if a conclusion has two independent routes and one premise falls, the spec labels the conclusion `suspended_unsupported` even though FW5:657 says another argument for the same conclusion can remain usable. The spec has no way to say "this dependence belongs to route 1 of 2". (2) Interference: FW5:344 — adding an active commitment can destroy an account. The spec's support edge can only *help*; there is no edge whose addition removes standing except an attack, which is a different relation with different semantics. (3) Non-minimality and collective blocks (FW5:281, 350: "a support but no minimal support and no singleton deletion witness"): a DAG of pairwise dependences cannot represent a block that contributes with no singleton in it contributing. The spec's own text concedes the deviation ("compiled into Dung; deviation from vanilla", spec:216) but not its cost.

**Repository evidence.**

On real FW5-shaped material the support half does no work at all. The importer's REPORT generator has a dedicated branch for it: "**none.** All {intra} `depends` refs in this scope were document-local, so at node granularity each would have been a `dep` self-loop - a cycle, which spec §1 forbids - and each was dropped and reported under `depends_intra_document`. ... Pass 2 is a no-op and `suspended_unsupported` is unreachable in this scope." (graph_import_h005.py:2871-2877). Golden graph: `dep = ∅` (NOTES.md §3). The authored FCL-1 `depends` refs in the H005 carry record (`"depends":["n1","n3"]` on record n4, /home/user/miniReason/experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/carry.json) are *record*-level, i.e. exactly FW5's within-organization commitment structure, and they vanish at the spec's artifact granularity. LP-15 (docs/LANGUAGE_PROPOSAL_THEOREMS.md:161) already states the interference case the spec cannot model.

**Testable consequence.**

Offline on existing evidence: count `depends_intra_document` versus `dep` edges on any H005 import — the design note asserts the ratio is all-to-zero for occurrence-01, so pass 2 is provably inert on the only corpus the repo has. New occurrences would decide the disjunctive case: construct one node whose conclusion is supported by two independent routes and refute one route's premise; FW5 predicts the conclusion remains usable, the spec predicts `suspended_unsupported`. Both outcomes are observable in a single cycle.

**Proposed change.**

Replace the single `dep` relation with declared *routes*: `refs[].role = "dependence"` gains a `route` label, and pass 2 becomes `supported(a) = ∃ route r: all deps in r accepted`. Keep the DAG constraint per route. Add a separate `interferes` role for FW5:344 (an edge whose presence removes standing from the *carrier*, not the target), or state in §17 that non-monotone support is out of scope. Also permit record-granularity artifacts so that within-document dependence survives import instead of being dropped as a self-loop.

**Confidence.**

0.87

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

FW5:254-267, 657, 682 are quoted correctly, and consequence (1) — no way to declare 'this dependence belongs to route 1 of 2' under the conjunctive `supported(a) = all(...)` of spec:219 — survives. The other two consequences do not. (2) 'The spec's support edge can only help; there is no edge whose addition removes standing except an attack, which is a different relation' — FW5:344's interference case is a failure of Account for the full candidate, i.e. a defect; registering it as a criticism against the composite artifact is the correct home for it, not a support edge, so this is a demand that the spec model a defect as support. (3) 'A DAG of pairwise dependences cannot represent a block that contributes with no singleton in it contributing' has it backwards: conjunctive `dep` is collective by construction — every dependence must stand and no singleton is privileged — so FW5:281/350's collective block is the case the spec models best; what conjunction cannot express is individual contribution differentials. The repo_evidence and proposed_change also assume the spec fixes artifact granularity ('permit record-granularity artifacts'); it does not — content is Σ* (spec:31) and the node granularity that turned document-local `depends` into self-loops was the importer's choice, not a §1 requirement. Finally the spec's spec:226 ('Refuting a premise ⇒ dependents become suspended_unsupported, NOT refuted (orphaned ≠ false)') is already FW5:657's 'the conclusion is not thereby false', so the spec agrees with two of that line's three clauses.

**Refuter — Corrected finding.**

`dep` is a single conjunctive relation (spec:219), so disjunctive support — FW5's family of distinct sufficient routes, S_{E,p} (FW5:254-262), with FW5:682's rule that distinct routes remain distinct receipts — has no representation: a `dependence` ref cannot say which route it belongs to, so refuting one route's premise suspends the conclusion even where an independent route survives. Fix: a `route` label on dependence refs and `supported(a) = ∃ route r: all deps in r accepted`. Withdraw the interference and collective-block limbs (interference belongs on the attack side; conjunction already models collective contribution) and the record-granularity limb (not a spec constraint).

### CA-4

**Finding id.**

CA-4

**FW5 claim.**

FW5:609 "A criticism has a represented target z, an alleged defect δ, grounds g, and a proposed connection from g to δ relative to a question." FW5:620 (K1) Bearing(c,z,p) ⟺ Account(𝓔_c, p_δ). FW5:622 "A criticism occurrence can exist when (K1) is false ... A mere adverse signal is not made into a criticism by giving it a negative label." FW5:174 anchoring; FW5:208 "This includes the respect κ, not just a matching number."

**Spec mechanism.**

§1 spec:93-104 Warrant = `{target, type, commitment, verdict, trace_ref, validity_node}` with ν "asserts the test is sound & relevant"; §1 spec:37-43 Artifact interface = `{commitments:[id], refs:[{target, role: dependence|mention|evidence}]}`; §1 spec:115 "a bare verdict is never an edge".

**Verdict.**

absent-in-spec

**Argument.**

FW5's criticism is a four-part object; the spec's is a two-part one (target + an assertion that the test is sound and relevant), and the two missing parts are exactly the ones that carry bearing. There is no field for *grounds*, and no field for the *connection* from grounds to defect: ν collapses soundness and relevance into one attackable proposition, so the only criticisms of a criticism the graph can express are "the test is unsound" and "the test is irrelevant", never "your grounds do not support this defect for this question". Nor is there any slot for the respect κ or the defect question p_δ, so (K1) — bearing as an Account of the defect question — is not expressible at all. Consequently the spec's `att` edge is precisely what FW5:622 warns against: a negative label whose existence is not evidence of bearing. The spec's own §1 rule "a bare verdict is never an edge" shows it saw the danger and addressed a weaker version of it (verdicts must be packaged in artifacts) without reaching the FW5 requirement (the *bearing* must itself be an account).

**Repository evidence.**

The importer had to mint a residue code for the missing field: `"grounds_absent_on_objection"` with detail "the validity node carries text + bearing (+ scope) only; no grounds field exists" (graph_import_h005.py:107, 1925-1935). The authored H005 objections do carry both: `objection.json` record o1 has `"target":[...]` and `"bearing":"If the driver is renegotiation or legitimacy rather than ambiguity, the specification move in c2 treats a symptom..."`, and carry record n1 carries a separate `"grounds"` field. The importer also had to weaken the ν text — "The ν no longer asserts soundness. Its first line is now `nu: <source>#<record> is an authored criticism directed at <target>; its soundness and relevance are not asserted by this import.`" — and log `validity_node_minted_unasserted` seven times (NOTES.md §2.8), i.e. it could not truthfully instantiate the spec's own ν semantics on authored material. SEMANTIC_GUIDE.md:25 sets the same bar the spec misses: reason use is "a role-preserving map from the represented objection into an active response route", and "Prompt inclusion, a citation, self-reported usefulness or endpoint differences alone" do not suffice.

**Testable consequence.**

Offline and already observed: 7 of 7 ν artifacts in the golden import are `validity_node_minted_unasserted`, and every `grounds` string in the material is carried only in the side table, never in the graph. The decisive further test needs no new occurrence: take any authored objection with grounds and ask whether the graph can distinguish "these grounds do not establish this defect" from "this test is unsound". It cannot — both must attack the same ν.

**Proposed change.**

Split ν into two attackable assertions — `soundness_node` and `bearing_node` — and give the Warrant schema a `grounds_ref` and a `defect_question` (the respect and target under which the defect is alleged). Then a criticism of a criticism can land on bearing without collapsing the whole warrant, which is what FW5:620/622 requires and what the spec's wholesale reinstatement currently prevents.

**Confidence.**

0.86

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

FW5:609/620/622 are quoted accurately but applied to a spec that does not say what the finding reports. 'There is no field for grounds' contradicts spec:115 — 'Both warrant types are contentful (packaged in artifacts); a bare verdict is never an edge' — whose entire purpose is to force grounds into the carrier artifact; demonstrative warrants additionally carry `trace_ref` (spec:102) and rubric warrants a full trial transcript with a resolvable `decisive_point` (spec:199-204). The carrier artifact's content is Σ*, so grounds are carried, not absent. 'No slot for the respect κ or the defect question p_δ, so (K1) is not expressible at all' overlooks that ν 'asserts the test is sound & relevant' (spec:103) — relevance to the stated target and question is the spec's bearing carrier — and that a critic artifact is bound by `addr` to a problem, whose `criteria` and `description` are the spec's question index. Calling the `att` edge 'precisely what FW5:622 warns against: a negative label' also misapplies FW5: FW5:622 warns about a mere adverse signal given a negative label, and §1/§3 exist to prevent exactly that (contentful warrant, attackable ν, trial guard, order-swap, paraphrase spot-check). The verdict 'absent-in-spec' is therefore wrong: bearing is present but coarse. The repo_evidence supports the corrected claim, not the stated one: the importer minted `grounds_absent_on_objection` for its own validity-node shape, and rewrote ν to stop asserting soundness — an importer decision about authored material, not a §1 defect.

**Refuter — Corrected finding.**

ν bundles soundness and relevance into one attackable proposition (spec:103), so a criticism of a criticism cannot land on bearing alone: 'your grounds do not establish this defect for this question' and 'this test is unsound' must attack the same node, and either attack retracts the whole warrant and reinstates the target. FW5:620 makes bearing its own Account over the defect question p_δ, which wants a separately attackable handle. Fix: split ν into `soundness_node` and `bearing_node`. Drop the claims that grounds have no field (spec:115, spec:102, spec:199-204) and that (K1) is inexpressible; the verdict should be 'hinders' (coarse granularity), not 'absent-in-spec'.

### CA-5

**Finding id.**

CA-5

**FW5 claim.**

FW5:381 "'Hard to vary' is therefore an articulated pattern of constrained changes, relative to an explanatory job ... Nor is it a numerical warrant." FW5:379 "Counting jobs is not a replacement for the missing comparison." FW5:851 "No quantity of endorsements, surviving tests, repeated observations, or partitioned features enters (G), (P), or (EK) as an automatic warrant." FW5:802 "Equation (P) does not rank alternatives."

**Spec mechanism.**

§0 spec:33 "Measures never adjudicate ... They MUST NOT appear as inputs to label computation (§4)"; §11.7 spec:469 "**Never a status**; an artifact off the frontier is merely unfunded, not demoted". Against these: §7 spec:286-316 `hv-floor` — "HV floor as criterion, never as gate", where `ŝ` is a survivor fraction over k∈[5,10] edits, "Verdict: `pass` iff `1 − ŝ ≥ HV_MIN`; else `fail`", and "a fresh, unattacked critic is in G ⇒ the relation is **refuted** — never `suspended`".

**Verdict.**

hinders

**Argument.**

The spec's §0 firewall is a genuine, independent reconstruction of FW5's no-merit-function commitment, and it is stricter than FW5 needs; that part helps. But §7 breaches it by a route the spec presents as compliance. A survivor count over k≈8 sampled edits, thresholded at HV_MIN, produces `fail`, which produces a demonstrative warrant, which produces `refuted`. That is a numerical quantity entering the status of an artifact — exactly FW5:381's "numerical warrant" and FW5:851's "quantity of ... surviving tests" as an automatic warrant. The laundering step is the phrase "criterion, never gate": routing the number through a commitment does not stop it being the number that decided the label. Two aggravations: (i) the spec's own §17 concedes "HV at k≈8 is a spot-check, not a measurement" (spec:580), yet the spot-check yields the same terminal label as a demonstrative program refutation — the single `refuted` label conflates demonstrative and statistical defeat; (ii) µ is LLM-produced, so ŝ measures the variator's imagination as much as the artifact's rigidity, which FW5:381's "splitting one feature into ten cannot create knowledge" is precisely about.

**Repository evidence.**

The repo enforces the prohibition harder than the spec does and never adopts §7: PURPOSE.md:15 "invent a progress meter" forbidden; AGENTS.md:15 "No ... scalar progress meter"; SEMANTIC_GUIDE.md:59 "A scalar novelty/progress score cannot adjudicate content"; SEMANTIC_GUIDE.md:57 "Reach or edit-survival counts supply no numerical warrant" — the last is a direct, named rejection of the hv-floor construction. The engine design of record scopes §7 out entirely and sets the P1 Pareto axes to `coverage`/`conn`/`attack_survival` "attention and reporting only" (engine-design-of-record-2026-09-14.md:292).

**Testable consequence.**

Offline, by inspection of the spec's own control flow: trace whether any path exists from a scalar to a §4 label. §7 supplies one (`ŝ → fail → demonstrative warrant → refuted`) and §11.7 does not. Empirically testable on a new occurrence: run `hv_estimator` twice with two different variator endpoints on the same artifact and record whether the terminal label flips — FW5:381 predicts the verdict tracks the variator's edit distribution rather than the artifact, and a flip refutes the claim that the number is a property of the explanation.

**Proposed change.**

Either delete `hv-floor` as a warrant-producing commitment and let low HV act only through the §3 remove-arbitrariness Spawn (which §0 already licenses), or make `hv-floor` fail produce a distinct, non-terminal marker (`contested_by_estimate`) that never equals the label produced by a program refutation. At minimum, §17 should name the conflict: the spec currently asserts both "measures never adjudicate" (spec:33) and a measure-derived `refuted` (spec:307) without acknowledging the tension.

**Confidence.**

0.8

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The charge that §7 'breaches' §0 by a route 'the spec presents as compliance' inverts §0:33, which names the route explicitly as one of three licensed channels: measures influence the graph by '(b) being packaged as budgeted commitments whose fail verdicts generate warranted attacks (§7)'. The invariant §0:33 actually states is that measures 'MUST NOT appear as inputs to label computation (§4)', and ŝ does not: the input is an attack edge from a contentful critic artifact. Calling this 'laundering' is an argument against the spec's stated design, not a demonstration of self-contradiction. The FW5 side is misread on the decisive word: FW5:851 forbids a quantity entering '(G), (P), or (EK) as an automatic warrant', and adds that counts 'are not outlawed as information'. The hv-floor warrant is the opposite of automatic — spec:307 requires a ν asserting kernel fairness, k-sufficiency, ≈_{B₀} adequacy and B₀-for-B adequacy, and spec:303 states B₀ is 'a declared surrogate for Def 3.6, asserted in the validity node, hence attackable'. FW5:381's 'nor is it a numerical warrant' is about the concept hard-to-vary, and the spec does not claim ŝ is that concept. Aggravation (ii) is the spec's own text: spec:307 clause (i) and §17:580 park the variator-imagination worry in ν by name. The claim that '§17 should name the conflict: the spec currently asserts both ... without acknowledging the tension' is a strawman of §17 — the finding quotes §17:580 ('HV at k≈8 is a spot-check, not a measurement ... stands on LLM-dependent assumptions ... visible and attackable, not eliminated') two sentences earlier. The repo_evidence shows the repo declining to adopt §7, which is a repo choice, not evidence of a spec contradiction.

**Refuter — Corrected finding.**

One narrow point survives: §4 has a single `refuted` label, so a target defeated by an eight-sample HV spot-check (spec:305-307) is labelled identically to one defeated by a program refutation, even though §17:580 concedes the two differ in kind. Fix is on the reporting side — a distinct non-terminal marker for estimate-derived defeat, or a §4/§17 note that `refuted` does not distinguish demonstrative from statistical defeat. The §0-breach charge should be withdrawn: §0:33 licenses the commitment route by name, ŝ is not a §4 input, and the ν clauses plus §17:580 mean the warrant is defeasible and declared, hence not FW5:851's 'automatic warrant'.

### CA-6

**Finding id.**

CA-6

**FW5 claim.**

FW5:663-676 (K3): from T∧B∧I ⟹ O and established ¬O, "an established ¬O yields ¬(T∧B∧I) ... It does not yield ¬T without additional premises about B and I." FW5:688 "Eligibility is a separate predicate ... The inability to evaluate a proposition is not a falsifying observation of the proposition." FW5:661 "A passing execution cannot make the program's specification, the model of the experiment, or the claimed relevance immune to prose criticism." FW5:1340 "whether a mechanical label can stand for semantic refutation. FW5 allows the former [operative elimination] without granting the latter infallibility."

**Spec mechanism.**

§1 spec:78-88 verdict `V(κ,c) ∈ {pass, fail, overrun}` with "`overrun` therefore means 'the verdict is unobtainable within the declared deterministic budget' ... never 'the machine was slow'" and "**Oracle isolation is not adjudication** ... A containment kill produces no epistemic verdict and MUST NOT mint a warrant"; §1 spec:107 validity-node closure; §4 spec:205-207 `refuted` if an attacker is in G.

**Verdict.**

neutral

**Argument.**

Mixed, and worth separating. Genuinely helpful: `overrun` is an exact mechanisation of FW5:688 — non-evaluability is quarantined from falsity, and containment kills are explicitly excluded from `V`. The ν requirement is a mechanisation of FW5:661 and FW5:240: no execution is self-certifying, and the soundness/relevance claim stays attackable. Genuinely hindering: the spec has one target per warrant, so (K3)'s disjunctive conclusion is inexpressible. A failed commitment attacks the artifact (`T`); the auxiliaries `B` and the observation interpretation `I` are folded into ν, so the only way to say "the test contradicted *something*, and it may have been the auxiliary" is to attack ν — which retracts the warrant wholesale and reinstates the target to `accepted`, asserting more than the evidence supports in the opposite direction. FW5 wants the test's contradiction preserved while its allocation stays open; the spec offers only refuted-or-reinstated. Similarly, wholesale case-law reinstatement (spec:108 "refute a standard ⇒ ... targets reinstated") erases verdicts that were independently good under a bad rubric, which FW5:682's disjunct rule forbids.

**Repository evidence.**

The repo aligns with the spec on exactly the point where the spec is right, and cites both sources together: docs/EXPERIMENT_METHOD.md:93 "V1.3 §1 explicitly says a containment kill must not mint a warrant. FW5 likewise separates failed delivery from content evidence" — the only place in the repo where the two documents are aligned on a point rather than ranked. docs/TASK_AUDIT.md:65 restates it. Against the disjunctive gap: docs/reviews/commitment-interface-source-2026-09-14.md:23 refuses v1.3's "pass/fail/overrun evaluators" as semantic authority, and the H005 protocol's interpretation clause (PROTOCOL.md:64) "Parser success, agreement with root, adoption of a standard answer ... do not establish repair" reflects the same worry about single-target allocation.

**Testable consequence.**

Offline, by construction: exhibit a commitment failure whose true locus is the auxiliary. Ask the graph to represent "¬(T∧B∧I)" — it cannot; the warrant names exactly one `target`. On existing H005 evidence the weaker version is already visible: the matched-arm envelope fault (docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md:26-30) is a case where a carrier failure would have been read as a content fact — "reading `commitments_sha256 = e3b0c442…` at face value would score an encoding fault as an arm that declined to commit" — and nothing in §1's verdict vocabulary distinguishes the two; only human interpretation did.

**Proposed change.**

Keep `overrun` and the oracle-isolation rule unchanged — they are the spec's best FW5 concordance. Add a `disjunctive` warrant type whose `target` is a *set* {T, B, I} and which registers as a criticism of the conjunction, spawning an allocation problem rather than a refutation; and make standard-refutation reinstatement per-verdict rather than wholesale, so a verdict with an independent sufficient route survives its standard's fall.

**Confidence.**

0.78

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The helping half is accurate: `overrun` (spec:79) and the oracle-isolation rule (spec:80-88) do mechanize FW5:688 and FW5:661, and ν mechanizes FW5:240/661. The hindering half fails twice. (1) '(K3)'s disjunctive conclusion is inexpressible ... the only way to say the test contradicted something is to attack ν' ignores spec:227 — 'Attacking a relation artifact directly ⇒ that relation refuted while its endpoints may stay accepted' — and spec:226, 'Refuting a premise ⇒ dependents become suspended_unsupported, NOT refuted'. Register T, B and I as artifacts and the tested conjunction as an artifact with `dependence` refs on all three; a failed commitment targets the conjunction, which is refuted, while T, B and I keep their own labels. That is ¬(T∧B∧I) without ¬T, built from §1/§4 as written, so the claim of inexpressibility is false. (2) 'Wholesale case-law reinstatement (spec:108) erases verdicts that were independently good under a bad rubric, which FW5:682's disjunct rule forbids' misdescribes both. spec:108 attacks each ν citing the refuted standard; §4 then recomputes G, so a target with an independent surviving attacker (a program warrant, say) is not reinstated — reinstatement is derived, not decreed (spec:187). The mechanism is per-warrant and per-graph, which is what FW5:682 asks for, not 'wholesale'. FW5:682's actual prohibition — that a refutation by an independent disjunct must not inherit an unused disjunct's disputed assumptions — is not violated by dropping warrants that genuinely rest on the refuted standard.

**Refuter — Corrected finding.**

Keep the concordance half unchanged. The residual gap is not expressive but default: the K3 construction (a conjunction artifact with dependence refs on T, B and I) is available under spec:227/226 but nothing in §1, §3 or §7 requires or prompts an author to pre-structure a test that way, so a single-artifact test with an auxiliary-located fault lands its refutation on T by default, and the only repair available after the fact is attacking ν, which retracts the warrant entirely. Recommendation: a §1 note (or a §3 registration prompt) that a test whose auxiliaries are in dispute should be registered against a conjunction artifact. Withdraw the case-law-reinstatement limb — §4 recomputation already preserves independently warranted attacks.

### CA-7

**Finding id.**

CA-7

**FW5 claim.**

FW5:810 "progress need not increase the number of accepted claims. Withdrawing an unsupported numerical mass and replacing it with a correct account of underdetermination can improve the inquiry ... The improvement concerns the removal of a false claim to have identified it and the acquisition of the relevant limitation." FW5:791-797 (P) Repair_{O,P}(ξ,ξ';Δ) with FW5:800 "ProducedBy ... is not satisfied by temporal succession alone." FW5:816 "The new content can be an account, an account of a defect, a revised interpretation, or an explained limitation."

**Spec mechanism.**

§3 spec:165-186 transition rules Conj / Crit / Adj / Spawn / Refl; §0 spec:32 "Nothing is deleted (D8)"; §4 the four labels. There is no Repair, Withdraw, or Limitation rule, and no relation corresponding to O (claimed repair obligations) or P (protected obligations).

**Verdict.**

absent-in-spec

**Argument.**

FW5's unit of progress is a repair: a named failed obligation becomes satisfied, named protected obligations survive, and the change is produced by an identified contribution on an active route. Every one of those three components is missing from the spec. There is no obligation vocabulary at all, so "this artifact repaired that defect while preserving those achievements" has no representation; the closest available move is to register a successor artifact and an attack, whose graph consequence is that the predecessor becomes `refuted` — which is FW5:657's forbidden inference (withdrawal is not falsity) and loses the positive half of the repair entirely. Worse for FW5:810: a contribution whose whole content is "no probe available here; state the limit plainly" is, in the spec, an artifact that nobody attacked, i.e. `accepted` — indistinguishable from a bold unexamined assertion. The spec's honest §17 residue says it "Does not manufacture good conjectures" (spec:578); what it does not say is that it also cannot record a repair, which is the quantity FW5 makes progress consist in.

**Repository evidence.**

The H005 material contains a textbook FW5:810 case. /home/user/miniReason/experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/carry.json body: "I do not think there is a probe that fixes this from inside the chore frame ... Rather than invent a cleverer test, I would state the limit plainly", and record n5: "No further refinement of the probe is available from the material in front of me. Adding a third observation track would be invention, not inference." In the import, that artifact is `A_carry`, `accepted`, and the derivation note says why: "`A_carry` is accepted because nothing came after it" (NOTES.md §3). The FCL-1 vocabulary that could have carried the repair is unmapped by name: `revises_unmapped` and `withdraws_unmapped`, both severity **unmapped**, alongside `claim_record_unmapped` and `use_record_unmapped` (graph_import_h005.py:96-112). The repo's own contract states the missing quantity: "Root will assess whether an identifiable error was corrected, what grounds bear on the claim, what changed in actual later use, and what remains disputed or was lost" (docs/reviews/multi-cycle-research-contract-2026-09-14.md:13) — none of which is a label.

**Testable consequence.**

Decidable now on existing H005 evidence: the carry artifact's label (`accepted`) is identical to the label a bare unchallenged assertion would receive, so the graph provably fails to distinguish FW5:810's progress-by-removal from the null case. A sharper test needing one new occurrence: register a limitation account that withdraws a prior identification claim and check whether any graph-derivable quantity differs from the case where the prior claim is simply attacked. Under the current rules it does not.

**Proposed change.**

Add a `Repair` transition and an obligation vocabulary: a repair artifact declares O (the obligation it claims to discharge) and P (the achievements it claims to protect), both fixed before assessment per FW5:787; the harness records the declaration and never computes its satisfaction. Add a `withdraws` ref role whose graph consequence is de-licensing the withdrawn artifact's *use* (removal from pack rendering) and explicitly not `refuted` — this is FW5:1340's "operative elimination" without the "mechanical label standing for semantic refutation".

**Confidence.**

0.83

**Refuter verdict.** stands: true, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The central claim is right: v1.3 contains no Repair transition and no O/P vocabulary — grep over the spec finds 'obligation' nowhere and 'repair' only at spec:138 (log repair) and spec:559 (schema-repair retries) — so FW5:787-802's comparison object has no representation. But three supports are wrong. (i) 'the closest available move is to register a successor artifact and an attack, whose graph consequence is that the predecessor becomes refuted — which is FW5:657's forbidden inference (withdrawal is not falsity)': FW5:657 is about withdrawing an essential premise, not about registering a warranted criticism; a successor need not attack its predecessor at all (spec:179, 'failed verdict ⇒ successor problem'), and when a warranted attack does land, `refuted` is not a withdrawal. This is a misapplication of FW5:657. (ii) 'there is no obligation vocabulary at all' overstates: Problem.criteria are commitment schemas — specified predicates instantiated per candidate — with a Popper battery auto-pinned (spec:123), which is a protected-set analogue; what is missing is the comparison across situations, not the predicate vocabulary. (iii) 'a contribution whose whole content is no probe available here; state the limit plainly is, in the spec, an artifact nobody attacked, i.e. accepted — indistinguishable from a bold unexamined assertion' is false in the informal-domain configuration: §6:244 `crit(a) ⇔ interface.commitments ≠ ∅` and spec:366 `skeleton-wf passes iff the skeleton parses AND forbidden ≠ ∅` mean a limitation statement that forbids nothing fails demarcation and is refuted by a program. And 'no graph-derivable quantity differs' from the null case ignores addr, refs, provenance and the event log, which differ by construction.

**Refuter — Corrected finding.**

FW5 makes progress consist in Repair_{O,P}(ξ,ξ';Δ) (FW5:787-798): a named failed obligation discharged, named protected obligations preserved, and the change ProducedBy an identified contribution (FW5:800, not satisfied by temporal succession alone). v1.3 has predicate material (Problem.criteria, the auto-pinned Popper battery) but no comparison object: nothing records that a successor discharged a named prior defect while preserving named prior achievements, and no ProducedBy condition, so FW5:810's progress-by-withdrawal — replacing an unsupported identification with an account of underdetermination — is not a recordable event. Fix: a `Repair` registration that declares O and P before assessment (FW5:787) and is recorded, never computed, plus a `withdraws` ref role whose consequence is de-licensing a use rather than `refuted` (FW5:1340). Drop the FW5:657 framing, the 'no obligation vocabulary at all' phrasing, and the indistinguishability claim (spec:244, spec:366 refute it).

### CA-8

**Finding id.**

CA-8

**FW5 claim.**

FW5:63 "A result of that inquiry must be able to affect the operative target. Scrutiny that can never change anything is not the recursive capacity described here." FW5:1052 return relevance — "A decorative transcript channel permanently disconnected from the operative state does not satisfy the condition." FW5:690 "an interpretation of its reasoning must not silently lose its actual dependencies." FW5:1218 projection theorem — "no function of P(M) alone agrees with the accounting predicate on both models"; FW5:1238 "record-state equality does not entail equality of semantic satisfaction".

**Spec mechanism.**

§1 spec:107-114 the three closures (validity, case-law, evidence), "computed, not curated"; §4 spec:228 "Recompute after every registration"; §13 spec:497 `why <id>` prints the attack/defence chain; §8 spec:328 `theory(id)` "Deterministic function of the graph ⇒ cannot drift".

**Verdict.**

helps

**Argument.**

This is the spec's real contribution on this axis, and it is a contribution to *construction*, not to adjudication. FW5 requires that criticism be able to change the operative target and that a reasoning interpretation not lose its dependencies; before this machinery the repo had, in its own words, "no mechanical notion of a criticism landing: no att edge, no warrant, no label". The closures supply a recomputed, non-curated record of why a criticism stopped counting — a receipt in FW5:682's sense — and the ν apparatus keeps the reason for that change attackable rather than editorial. The important qualification is directional: the useful output is the *operative consequence* (what the next invocation sees, what is de-licensed), not the label. FW5:1218 guarantees no function of the record alone fixes the account-claim, so the labels can never be the finding; but the record can still be the thing that makes a criticism land. The spec's error is only that it derives operative consequence from status rather than treating operative consequence as primary — FW5's standing (FW5:638) is enacted first and described after.

**Repository evidence.**

docs/reviews/engine-path-decision-2026-09-14.md:25-31 states the gap the mechanism fills: the repository's research question "is at present asked with **no mechanical notion of a criticism *landing*: no att edge, no warrant, no label**, nothing that distinguishes a criticism taken up from one written down beside the thing it criticises". The import demonstrates the closure doing exactly the FW5:690 job: "what changed is that the graph now records **why** the response's objection against the rival stopped counting" (NOTES.md §3), via the criticism-of-criticism retarget onto ν(W_k7). And the pre-registered falsifier is already the right test: engine-design-of-record-2026-09-14.md:890 — "if, under the new engine, attack edges land on H005 criticisms and root still cannot identify a single episode in which a warranted criticism changed a later operative use, then the missing ingredient was never the bookkeeping, the engine bought auditability rather than error correction, and that outcome will be reported as evidence with the same weight as a positive one."

**Testable consequence.**

Needs new occurrences, and the test is already pre-registered: run H005 occurrence-02 under the closure-bearing engine and ask whether any episode exists in which a warranted criticism changed a later operative use (what a subsequent node saw or did), not merely a later label. FW5:1052's return-relevance probe is the discriminator: at least one alternative subsidiary result must be able to produce a different use-state. A partial offline check exists today — the import's order-sensitivity finding (NOTES.md §6.4: "the shape of `att` depends on the scope imported") shows that where a criticism lands is not scope-invariant, which must be reported before any landing claim is made.

**Proposed change.**

Invert the dependency: make the operative consequence the computed primitive — a per-invocation `operative_set` (which artifacts and fields the next node actually receives, and which are de-licensed) — and expose labels only as a derived summary of that set, never as its cause. Keep the three closures and `why` unchanged; they are the mechanism worth keeping from v1.3. Add to §17 the honest statement that the graph records where criticism landed and cannot record whether it bore (FW5:620), so that a landed edge is never reported as bearing.

**Confidence.**

0.82

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

I tried two lines and neither holds. First, that the finding over-credits the closures: it does not — spec:107-114 does compute, rather than curate, why a criticism stopped counting, and spec:328's `theory(id)` is a deterministic function of the graph, which is what FW5:690 ('an interpretation of its reasoning must not silently lose its actual dependencies') asks of a record. The FW5:1218 qualification is stated correctly and in the right direction: the projection theorem bars any function of the record from fixing the account-claim, which is why the finding refuses to let the label be the finding. Second, that 'the spec derives operative consequence from status' is a misreading, since §11:412 says capture control steers attention 'never status' and §11.7:469 says an off-frontier artifact 'is merely unfunded, not demoted'. But the claim survives: several operative consequences are gated on labels — anti-relapse blocks on refuted-equivalents (spec:191-193), remove-arbitrariness and integration Spawns fire on `accepted` artifacts (spec:181, 185), HV runs on accepted artifacts only (spec:251), reach cross-evaluates accepted artifacts (spec:269), and conn counts accepted dependence edges (spec:280). So status is upstream of what the next invocation sees, and the proposed inversion is a real, if partial, change. The pre-registered falsifier quoted from the repo is the right discriminator and is honestly stated.

**Refuter — Corrected finding.**

---

## Axis 2 — criticism-and-use: FW5 on criticism being taken up and USED in later reasoning (reason-use, uptake, repair) versus harness spec v1.3's warrants/attack edges

**Critic's overall assessment.**

On this axis the spec hinders, and it hinders in a specific, measurable way that the repo has half-noticed and mis-diagnosed. FW5 draws four distinct relations — a criticism existing (L609), its bearing (K1, L611-618), a later organization actually using it (L626-628), and a repair produced via that use (ProducesVia, L839) — and insists none is recoverable from a label, a record field, or an endpoint (L601, L640, L332, L1218). Harness v1.3 supplies exactly one relation on that axis, `att`, and one derived object, a status; it defines no construct for use, and its only near-neighbours are `dep` (which couples status, forbidden by L630/L657) and `mention` (which is "explicitly non-load-bearing", spec L61). The empirical result on H005 occurrence-01 `daily/mini_fcl/cycle01` is decisive and reproducible offline today: 20 cross-document `target` refs were authored, of which the 10 carried by `objection` records became 7 warrants and 4 `att` edges, while the 10 carried by `claim` and `use` records — including `response.k1` ("The objection is right that the account's recurrence test has low discriminating power", targeting `objection#o2`), `response.k2` (endorsing `rival#r7`), `carry.n4` (repairing `response#k5` in light of the carry's own n1/n3) and `carry.n7` (retaining `response#k8`) — produced no edge, no ref and no label effect, and were logged under a residue code the importer itself grades merely "informational" (`target_on_non_objection_record`, 7 records; `use_record_unmapped` 9; `claim_record_unmapped` 15). All 17 intra-document `depends` refs, 12 of them declaring that a `use` record depends on the author's own claims and objections — the authored shape of ProducesVia — were annihilated by one-artifact-per-node granularity. Meanwhile the graph asserts things no use occurred to justify: `A_rival` is `accepted` by Lemma 3.1 reinstatement purely because `A_carry` attacked `A_response`, though nothing in the carry restores the rival to use, and `A_rival`'s own author withheld `uptake` from 7 of its 11 records including two of its own commitments. A landed attack edge is therefore neither necessary nor sufficient for a used criticism: on this one cycle it is wrong in both directions, and its errors are not noise but systematic (it tracks authored negative polarity at node granularity, and nothing else). The spec is not at fault for failing to define use — it never claimed to — but the programme is at fault for reading "criticism landed" off `att` and for wording its own falsifier (engine design-of-record :890, :914) so that the spec's bookkeeping is credited or blamed for a relation it does not model. The fix is small and mostly already paid for: sub-artifact addressing (`<artifact-id>#<local-id>`, resolvable against the surface blob the harness already pins), a `use` ref role that is adjudication-inert by construction but reported, and a separation of the author's *declared* use from an observer's *witnessed* reason-use with `unresolved` as a legal third value (L634).

**Refuter's axis summary.**

All 18 FW5 line citations across the seven findings check out verbatim, and I independently recomputed the H005 ref census (52 refs; 20 cross-document targets split 10/7/3; 17 intra-document depends split 12/3/2; 9 intra mentions; 4 dropped self-targets; 7 target_on_non_objection records = k1,k2,k6,n1,n4,n5,n7) and the golden graph (att = 4 edges, dep empty, 14 accepted / 3 refuted) — the critic's arithmetic is right almost everywhere. The disagreements are about what those facts license. TWO FINDINGS FAIL ON MISREADING. CU-3 inverts both documents: FW5 K2 (L642-651) plus the elimination paragraph (L657, "the conclusion is not thereby false") IS the support cascade, and spec L226 ("orphaned != false") reproduces it almost word for word — so §4 pass 2 mechanizes FW5 rather than violating it; the supporting claim that a suspended_unsupported artifact is treated as refuted by §7/§11.5 is also false (§11.5 indexes refuted artifacts only, and §3 L195 says blocking occurs "only for relapse onto refuted-equivalents"). CU-6's second move misreads §11.5: what is withheld from packs is the negative-atlas RECORD (centroids, exemplar ids), not the refuted artifact, which stays in A, attackable under N1 and renderable by why/theory — which is precisely what FW5 L659 asks for, and L659 positively licenses removal from current working use; its (RC) L1062 citation is repurposed from self-referential target chains to prompt rendering. CU-7's headline also fails: the engine falsifier's structure is "we performed the intervention; if the outcome does not follow, the intervention was not the bottleneck", which is the negation of the att-equals-use claim rather than an instance of it, and the critic's two "competing readings" are the same conclusion restated. THREE STAND WITH CORRECTIONS. CU-1's substance holds and its sharpest evidence is exact — docs/reviews/engine-path-decision-2026-09-14.md:27-31 literally calls an att edge "a mechanical notion of a criticism landing" that "distinguish[es] a criticism taken up from one written down" — but the verdict belongs on the repo, not the spec (the finding's own spec_mechanism field concedes absence, and FW5 L640 makes abstention the licensed posture), and "no polarity other than attack" is false since dependence is a support relation. CU-4 stands on evidence and on the spec's real lack of sub-artifact resolution, but the harm is attributable to the repo's node-granularity election rather than a spec prohibition (record-grain artifacts are spec-legal, as its own test proposal assumes), and "every cross-document reference is <16-hex>#<record>" is wrong (objection uses p.objection.0#c1). CU-5's absent-in-spec verdict stands but its instrument charge is refuted by the importer's own code: graph_import_h005.py:_map_mention_refs appends "target" to the mention fields for non-objection records, so those 7 relations are carried as node-level mention refs and "informational" is the coherent grade — the proposed re-grade would make the instrument wrong by its own definitions. CU-2 fails as written on a factual slip (account is 5/6, not 5/7), on a self-inconsistency (calling the label a "contradiction" of author standing when its own testable consequence says the two are incommensurable), and because design-of-record:372 already prescribes the remedy it demands ("Rendered and reported only ... never an input to §4"); what survives is a one-line correction swapping §0:32 for FW5 L640 as the justification. The strongest surviving material across the whole set is CU-1's repo-level conflation citation, CU-4's granularity census, and CU-7's ablation requirement (FW5 L800 + L630's three-case contrast contract), which is the one change that actually gates occurrence-02.

### CU-1

**Finding id.**

CU-1

**FW5 claim.**

FW5 L626: "A response uses a reason when the represented content of the objection participates in the organization's deliberative transition. The response state includes interpretations, provisional uses, methods, and continuing questions, not just a terminal action label." L628: the reason-use witness is "a structural map from the represented objection organization into that suborganization... The map must preserve internal role bindings, not merely the endpoint string." L601: the mapped objection must be "on an active dependency route" with "nonconstant dependence on the relevant represented distinction under its declared contrasts", and "is not inferred from the presence of a similar sentence in a record."

**Spec mechanism.**

harness-spec-v1.3 §1 L53-58 (warrant carriage `carry ⊆ A × W`; "Each pair contributes an attack edge `(artifact → warrant.target)` to `att`"); §4 L206-229 (two-pass grounded adjudication; L229 "**Inputs to adjudication are `att` and `dep` ONLY.**"). No mechanism in v1.3 names, records, or computes use.

**Verdict.**

hinders

**Argument.**

An `att` edge records that some author declared an adverse relation between two artifacts; a use records that a later organization's deliberative transition depended on the earlier content. These come apart in both directions and do so systematically, not marginally. An edge without use: v1.3's Lemma 3.1 reinstatement (spec L187) relabels an artifact `accepted` on purely positional grounds, with no event of anyone taking it back up. A use without an edge: endorsement, qualification, incorporation and repair are the commonest ways criticism gets used, and none of them is adverse, so none mints a warrant. The spec's own vocabulary has no polarity other than attack, so the whole positive half of uptake is structurally invisible. This is not a gap the spec conceals — §4 L229 is explicit that only `att` and `dep` feed labels — but it means the label layer cannot be read as evidence about use, and the repo reads it that way.

**Repository evidence.**

`/home/user/miniReason/experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/`. Golden att (scratchpad importer NOTES.md §3): `att = {(A_objection,A_account),(A_response,A_rival),(A_carry,A_response),(A_carry,ν(W_k7))}`, |att|=4, dep=∅, labels 14 accepted / 3 refuted. (a) Use without edge: `response.json` record k1 is `type:"claim"` with `target: ['b5dbbb04b5acd035#c2','bdbdf50a52b8b1fe#o2']` and text "The objection is right that the account's recurrence test has low discriminating power: falling recurrence on specified items is compatible with the ambiguity reading, a renegotiation reading, and a load-imbalance reading" — a verbatim re-deployment of `objection` record c2's content. It mints nothing. Likewise k2 endorsing `rival#r7` ("The rival's distinguishing observation is the sharpest available move"). (b) Edge without use: NOTES.md §3 states plainly "`A_rival` is reinstated because `A_carry` happened to attack `A_response`"; the carry's own records (n1, n3, n4, n5, n7) narrow the response and n7 says "Keep the carry's records as they stand" — nothing restores the rival's r6, which k3 rejected and which the carry body records as "dropped the rival's loaded opening question."

**Testable consequence.**

Offline on existing H005 evidence, now: classify every cross-document record reference in the five cycle-01 FCL-1 documents by the relation its own text enacts (attack / endorse / qualify / repair / retain) and compare with the 4 computed `att` edges. Prediction, already borne out on this cycle: the edge set covers the attacks (3 objection→account collapsed, k3+k7→rival, n3→response) and zero of the endorsements/repairs, and additionally asserts one reinstatement (A_rival) that no record enacts. A second, stronger consequence needs new occurrences: deliver to an otherwise identical successor call (i) a content-changed objection, (ii) a content-preserving recoding of the same objection, (iii) the same objection with a carrier disturbance (FW5 L630's three declared cases); a genuine reason-use witness requires the response to change under (i), not under (ii), not under (iii). Occurrence-01 supplies none of these contrasts, so no reason-use witness can be established from it at all.

**Proposed change.**

Add to the spec a third `refs[].role` — `use` — carrying `{used: <artifact-id>#<local-id>, by: <artifact-id>#<local-id>, mode: endorse|qualify|reject-with-reason|repair|retain}`, declared adjudication-inert in §4 (never an input to label computation, like school membership at §1 L64) but reported by `why` and by the CLI. Independently, the repo should stop describing an `att` edge as a criticism "landing" (docs/reviews/engine-path-decision-2026-09-14.md:25-31 already frames the missing notion this way) and should say instead that v1.3 supplies no landing notion at all.

**Confidence.**

0.9

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

FW5 L626/L628/L630/L601 all verified verbatim; the composite quotation is accurate (minor: 'on an active dependency route' is L628's phrase, L601 supplies the active-route definition and the nonconstant-dependence condition). Spec mechanism verified: L53-58 carriage, L57-58 'Each pair contributes an attack edge', L229 'Inputs to adjudication are att and dep ONLY'. Repo evidence verified independently: golden att = 4 edges, dep = empty, 14 accepted / 3 refuted; response k1 is type 'claim' with target ['b5dbbb04b5acd035#c2','bdbdf50a52b8b1fe#o2'] and mints nothing; the import notes say verbatim 'A_rival is reinstated because A_carry happened to attack A_response'. THREE PRESSURE POINTS. (1) The verdict 'hinders' overreaches against the SPEC. The finding's own spec_mechanism field concedes 'No mechanism in v1.3 names, records, or computes use', which is the definition of absent-in-spec; and FW5 L640 positively supports abstention ('Actual use ... are semantic attributions. They are not automatically machine-maintainable facts merely because a host can maintain corresponding labels'). A spec that declines to mint machine-maintained use labels is FW5-aligned, not FW5-hindering. (2) 'The spec's own vocabulary has no polarity other than attack' is FALSE as written: L53 defines refs[].role == 'dependence' as a positive SUPPORT edge into dep, and the finding itself builds CU-3 on that relation. Incorporation — one of the four positive modes it lists — is exactly what dep encodes. The true claim is narrower: the spec has no non-cascading, record-grained, polarity-labelled uptake relation. (3) Minor citation slip: k1's endorsed content is objection record o2 ('The account's proposed test ... does not distinguish the ambiguity hypothesis from the alternatives'), not 'objection record c2'; k1's other target b5dbbb04b5acd035#c2 is the ACCOUNT's c2. WHAT SURVIVES, AND IS STRONG: the repo-level charge. docs/reviews/engine-path-decision-2026-09-14.md:27-31 reads verbatim 'the repository's research question — whether a criticism returns to operative use — is at present asked with no mechanical notion of a criticism *landing*: no att edge, no warrant, no label, nothing that distinguishes a criticism taken up from one written down beside the thing it criticises.' That sentence does equate an att edge with 'a criticism taken up', which is precisely the equation FW5 L332/L1224 and L626/L628 forbid. The finding's repo citation is exact and load-bearing.

**Refuter — Corrected finding.**

Verdict should be absent-in-spec (spec side) plus a repo-level correction (repo side). Spec side: v1.3 supplies no relation whose semantics is 'a later organization's deliberative transition took up this earlier content'; att is adverse-only and dep carries a status cascade, so neither is a use relation. FW5 L640 makes this abstention defensible, not a defect — the defect is only that nothing is reported either. Repo side (this is where 'hinders' bites): docs/reviews/engine-path-decision-2026-09-14.md:27-31 describes the att edge as supplying a 'mechanical notion of a criticism landing' and as 'distinguish[ing] a criticism taken up from one written down'. That is the reason/use conflation FW5 L332 and the L1218 projection theorem rule out, and it should be corrected in place. Drop the claim that attack is the spec's only polarity (dependence is a support relation). Fix 'objection record c2' to 'objection record o2'. The evidence and both testable consequences stand unchanged.

### CU-2

**Finding id.**

CU-2

**FW5 claim.**

FW5 L638: "Standing is the system's enacted permission to use a content in a particular application and respect. It may be explicit or inexplicit. An appraisal can change it without having earned prior certification." (K2, L642-651) `Usable_j(u) ⟺ Lic_j(u) ∧ Scope_j(u) ∧ ∀d∈Prem(u), Live_j(d;u)` — appraisal-indexed by `j`. L653: "The actor can violate this coherence condition. The model then represents an error in its appraisal."

**Spec mechanism.**

harness-spec-v1.3 §0 L32 "Status is computed, never stored as ground truth"; §4 L209-214, which computes exactly one global label per artifact from the unique skeptical grounded extension. Engine design-of-record `/home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md:372`: "| `uptake: [Ref]` | **drop from the mechanism** | A self-declared standing label; §0:32 says status is computed, never stored."

**Verdict.**

hinders

**Argument.**

The engine reaches the right operational answer (uptake must never feed §4) from the wrong premise, and the wrong premise costs it the construct. FW5 standing is not a status: it is appraisal-indexed (`Usable_j`), it is enacted rather than certified, it can be inexplicit, and — decisively — it is violable, so the model must be able to represent an actor whose declared standing is incoherent with its own use. The spec's label is global, unique, computed and by construction non-violable; nothing in it can hold two appraisers' differing standing, and nothing can record that an author granted itself permission it then failed to exercise. So `uptake` is not a duplicate of the spec's status that §0:32 rules out; it is a different object for which the spec has no slot. Citing §0:32 makes the omission look like hygiene when it is a missing primitive. The correct ground for keeping uptake out of adjudication is FW5 L640 ("A named field asking for a criticism is an invitation fact... not automatically machine-maintainable facts merely because a host can maintain corresponding labels"), which also tells you what to do with it instead: keep it, report it, never promote it.

**Repository evidence.**

`artifacts/daily/mini_fcl/cycle01/rival.json`: 11 records, `uptake: ['r2','r6','r7','r9']` — the author withheld standing from r1, r3, r4, r5, r8, r10, r11, including two of its own `commitment` records (importer residue `commitment_record_not_in_uptake` = 2, on r10 and r11; scratchpad NOTES.md §2(6)). The mechanism labels `A_rival` `accepted` as a single node, contradicting the author's own declared partial standing on 7 of 11 records. Importer residue: `uptake_lists_unmapped` 5 (document unit), `uptake_refs_unmapped` 32 (ref unit), reason recorded verbatim as "uptake is a local claim about standing, never a harness verdict, status or acceptance" (graph_import_h005.py:1656). Engine test obligation (design-of-record:857): "'uptake' never appears in any status computation."

**Testable consequence.**

Offline, now: for each of the five cycle-01 documents compute (records in uptake) / (records total) — account 5/7, objection 6/8, rival 4/11, response 9/9, carry 8/8 — and check whether the spec's single node label agrees with the author's own standing profile on any of them. Prediction: it cannot disagree or agree, because it is not the same kind of fact; the observable consequence is that on `rival` the mechanism reports one `accepted` where the author reported 4 live and 7 withheld, and no downstream reader of the graph can recover the difference. A further consequence, testable across cycles once occurrence-02 runs: a record withheld from uptake at cycle n but targeted by a later node at cycle n+1 is a case where the author's own standing was overridden by use — FW5 L653's violation case — which the spec can represent nowhere.

**Proposed change.**

Introduce `standing` as a first-class authored, appraisal-indexed field on the artifact interface (`standing: {appraiser, live: [<local-id>], withheld: [<local-id>]}`), reported by `why` and never an input to §4, and delete the §0:32 justification for dropping it — replace it with FW5 L640. Correct the engine reduction table row at design-of-record:372 accordingly, and record the correction in DIVERGENCES.md rather than silently.

**Confidence.**

0.85

**Refuter verdict.** stands: false, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

The FW5 reading is exact — L638 (enacted permission, explicit or inexplicit, changeable without prior certification), K2 at L642-651 (appraisal-indexed by j), L653 ('The actor can violate this coherence condition') all verified. The spec reading is exact — L32 and §4 L209-221 compute one global label. The engine table row at design-of-record:372 is verbatim. But three things break the finding as written. (1) FACTUAL ERROR in the repo evidence and the testable consequence: account.json has SIX records (c1,c2,c3,o1,u1,p1) and uptake of 5, so the ratio is 5/6, not the stated 5/7. (Objection 6/8, rival 4/11, response 9/9, carry 8/8 all verified correct.) (2) SELF-INCONSISTENCY: the repo_evidence says the single accepted label 'contradict[s] the author's own declared partial standing on 7 of 11 records', while the testable_consequence says 'it cannot disagree or agree, because it is not the same kind of fact'. The second is right; the first is the very category error the finding exists to diagnose, committed inside the finding. (3) THE REMEDY IS ALREADY IN PLACE, so 'the wrong premise costs it the construct' is overstated. design-of-record:372 does not discard uptake: it says 'Rendered and reported only (the §10.1 prose_notes precedent: "rendered, never adjudicated"), never an input to §4' — which is exactly the finding's own prescription ('keep it, report it, never promote it'). The importer likewise preserves it in full: uptake_lists_unmapped records the list verbatim (graph_import_h005.py:1652-1659) and commitment_record_not_in_uptake fires on rival.r10/r11. What remains is a narrow criticism of one justification clause, not a missing primitive. (4) The FW5 L653 violation case — an author using a premise whose standing it withheld — is unrepresentable in the SPEC's label layer, which is true; but the spec has no field for it precisely because FW5 L640 says such attributions are not automatically machine-maintainable. Absence of a slot is the licensed posture, not a hindrance.

**Refuter — Corrected finding.**

Verdict: absent-in-spec, with a narrow documentation correction. Claim: (a) FW5 standing (L638, K2, L653) is appraisal-indexed, enacted, inexplicit-capable and violable; the spec's §4 label is global, unique and non-violable, so the two are different objects and the spec has no slot for the first. (b) The engine reduction table at docs/design/engine-design-of-record-2026-09-14.md:372 cites the wrong ground for dropping uptake from the mechanism: §0:32 ('status is computed, never stored') would only apply if uptake were a duplicate of the spec's status, which it is not. The correct ground is FW5 L640. This is a one-line correction to a justification, recordable in DIVERGENCES.md; the operational disposition ('Rendered and reported only ... never an input to §4') is already right and needs no change. Drop the 'contradicting the author's own declared partial standing' framing (the labels are not commensurable, as the finding's own testable consequence says) and correct account to 5/6.

### CU-3

**Finding id.**

CU-3

**FW5 claim.**

FW5 L630: "**Understanding and using an invalid objection does not make it valid.** The definition concerns whether the system used the content, not whether it responded ideally." L657: "Withdrawing a criticism likewise does not establish the truth of its target." L632: "An invalid criticism can lead to a mistaken revision." L622: "A criticism occurrence can exist when (K1) is false."

**Spec mechanism.**

harness-spec-v1.3 §1 L53 (`refs[].role == "dependence"` ⇒ support edge in `dep`); §4 pass 2, L215-219: `supported(a) = all(final(b)==accepted for (a,b) in dep)`; `if label0(a)==accepted and not supported(a): final(a) = suspended_unsupported`; L226 "Refuting a premise ⇒ dependents become `suspended_unsupported`, NOT `refuted` (orphaned ≠ false)."

**Verdict.**

hinders

**Argument.**

`dep` is the only spec relation whose semantics is "this later thing rests on that earlier thing", so it is the obvious candidate for encoding use — and it is the wrong one, because it carries a status cascade that implements exactly the inference FW5 forbids. If a response `dep`-depends on the objection it used, and the objection is later refuted, §4 pass 2 flips the response to `suspended_unsupported`, i.e. the mechanism records that using a bad criticism degrades the user's own standing. FW5 says the opposite twice over: using an invalid objection neither validates it (L630) nor invalidates the response's content, and withdrawing a criticism does not establish anything about its target (L657). The spec's L226 disclaimer ("orphaned ≠ false") softens the label but not the coupling — an artifact that has been demoted out of `accepted` is, for every downstream consumer in §7, §11.5 and the scheduler, no longer the same thing. So any faithful `use` relation must be status-inert by construction, which `dep` is not and cannot be made to be without breaking the support pass it exists for.

**Repository evidence.**

`dep = ∅` in the golden H005 import (scratchpad NOTES.md §3), so the coupling is currently latent rather than realised: the 17 authored `depends` refs in cycle-01 are all intra-document and were dropped by node granularity. But the engine reduction table (design-of-record:372 area) commits to `depends: [Ref]` → "`interface.refs[].role = "dependence"` — a real `dep` edge, so the support cascade is live for H005", and the pre-registration (design-of-record:890) explicitly warns that pass 2 will move artifacts the frozen engine called `accepted` into `suspended_unsupported`. The moment a later node declares a cross-document `depends` on an objection, the forbidden coupling is live.

**Testable consequence.**

Offline, now, on the existing deterministic importer: construct a synthetic variant of the golden scope adding one `dependence` ref A_response → A_objection and one synthetic attacker of A_objection, and re-run. Prediction: A_response flips from `refuted` (its current label, via A_carry) or from `accepted` in an attacker-free variant to `suspended_unsupported`, while none of k1/k4/k8's content has changed and no author has withdrawn anything — a machine-generated instance of the inference FW5 L630/L657 prohibits. The variant is buildable from the fixture with no provider call.

**Proposed change.**

State in the spec (§1, beside the `mention` clause at L61) that `dependence` is a *support* relation whose status cascade is deliberate, and that it MUST NOT be used to record that an artifact used a criticism; supply the separate `use` role of CU-1 for that. In the repo, add a test that no compiled H005 `use` or endorsing-`claim` record ever produces a `dependence` ref.

**Confidence.**

0.85

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

This finding inverts both documents. FW5 L642-657 is not a prohibition on the support cascade — it IS the support cascade. K2 (L642-651) says an application u is usable only if every essential premise is live: Usable_j(u) requires forall d in Prem(u), Live_j(d;u). L657 then states the consequence in terms the spec reproduces almost word for word: 'Suppose a system withdraws an essential premise of u. Equation (K2) no longer licenses u. Another argument v for the same conclusion can remain usable. THE CONCLUSION IS NOT THEREBY FALSE.' Spec §4 L221/L226: 'elif label0(a) == accepted: final(a) = suspended_unsupported' and 'Refuting a premise => dependents become suspended_unsupported, NOT refuted (orphaned != false).' That is K2's licence-withdrawal plus L657's non-falsity clause, mechanized. L226 is therefore not a 'disclaimer [that] softens the label but not the coupling' — it is the semantics, and the coupling is the one FW5 specifies. SECOND MISREADING: what L630 and L657 forbid is an inference about VALIDITY or TRUTH ('Understanding and using an invalid objection does not make it valid'; 'Withdrawing a criticism likewise does not establish the truth of its target'). suspended_unsupported asserts neither; §4 L226 says so explicitly. The finding's paraphrase — 'the mechanism records that using a bad criticism degrades the user's own standing' — is exactly FW5's own K2 result, and FW5 L653 adds the further point the spec honours via N1: 'A record declaring a dependency does not establish that the dependency is actually essential; an error in that declaration is another criticism target' — i.e. attack the dependence declaration, which §4 L227 supports ('Attacking a relation artifact directly => that relation refuted while its endpoints may stay accepted'). THIRD MISREADING, of the spec: 'an artifact demoted out of accepted is, for every downstream consumer in §7, §11.5 and the scheduler, no longer the same thing.' §11.5's index is the REFUTED-artifact index, and §3 stage 1/3 blocks 'only for relapse onto refuted-equivalents' (L195); suspended_unsupported never enters it. §7's conn(a) does count accepted dependence edges, but §0 fixes that as attention/measure, never status — which FW5 L57 expressly permits. FOURTH: the finding's substantive worry is conditional on someone encoding 'used a criticism' as a dependence ref; nothing in v1.3 licenses that, and the design-of-record maps FCL-1 'depends' (an author-declared premise relation, i.e. Prem(u)) to dependence, which is FW5-faithful. FIFTH: dep is empty in the golden import, so nothing is realised, and the synthetic-variant test would demonstrate K2, not a violation of it. The 'hinders' verdict does not survive.

**Refuter — Corrected finding.**

Downgrade from a finding to a one-line spec caution, verdict: no defect. The spec's pass-2 cascade is a faithful mechanization of FW5 K2 (L642-651) and the elimination paragraph (L657): withdrawing an essential premise withdraws the licence for that application without making the conclusion false, which is exactly suspended_unsupported != refuted (L226). The only residue worth recording is a naming caution, and it belongs beside CU-1's proposed use role rather than as an attack on dep: if a future compiler ever encodes 'this record took up that criticism' as a dependence ref, it would import a licence cascade that FW5 attaches to essential premises and not to uptake. State that in §1 beside the mention clause, and add the repo test the finding proposes (no compiled H005 endorsing record emits a dependence ref). Delete the claim that §4 implements an inference FW5 forbids, and the claim that a suspended_unsupported artifact is treated as refuted by §7/§11.5.

### CU-4

**Finding id.**

CU-4

**FW5 claim.**

FW5 L628: the reason-use witness maps "the represented objection organization" — target, grounds, defect connection — into "a response suborganization `D_s` with represented target, grounds, defect connection, and response-role ports", and "must preserve internal role bindings, not merely the endpoint string." L609: "A criticism has a represented target \(z\), an alleged defect \(\delta\), grounds \(g\), and a proposed connection from \(g\) to \(\delta\) relative to a question." L839: ProducesVia "requires the construction account of the repair to contain the relevant binding of \(c\) on its active route."

**Spec mechanism.**

harness-spec-v1.3 §1 L38 artifact id = `sha256(canonical(content_ref, codec, interface))` with `content_ref` a single blob; L96 `"target": "<artifact-id>"` on a Warrant; `refs[].target: "<artifact-id>"`. There is no sub-artifact address anywhere in v1.3. The H005 mapping (design-of-record §6) is one artifact per node.

**Verdict.**

hinders

**Argument.**

FW5's criticism and its use are both four-part objects addressed at the grain of a represented content, not of a conversational turn. H005's authors wrote at exactly that grain: every cross-document reference in the corpus is of the form `<16-hex node label>#<record id>`. The spec can only address the node, so every such reference is either truncated to the node (losing which claim was criticised and which was used) or dropped entirely. The damage is not cosmetic: it is what forced `response#k7` — an objection whose text says "My own two-track test inherits a version of the objection I am endorsing against the account... my k2 does not fully solve it", i.e. a self-directed criticism of the author's own k2 — to be routed as an attack on `A_rival`, because its other ref `rival#r9` happened to be the only one that could resolve to a node (NOTES.md §2(7)). A criticism of one's own commitment was recorded as an attack on someone else's artifact. FW5 L609's "represented target" is precisely what was lost.

**Repository evidence.**

Exact counts over the five cycle-01 FCL-1 documents (computed offline from the artifacts, 52 refs total): cross-document `target` refs = 20 (10 on `objection` records, 7 on `claim` records, 3 on `use` records); intra-document `depends` = 17 (12 of them on `use` records, 3 on `commitment`, 2 on `claim`); intra-document `mentions` = 9. All 17 `depends` collapse to nothing because both endpoints are the same artifact (importer code `mentions_intra_document`, 9 at ref unit; workflow doc `docs/workflows/graph-import-h005.md:47` lists "the 17 document-local `depends` references" among the largest residue entries). Importer residue `objection_target_self_ref_dropped` = 4 refs (three on `objection.o4`, one on `response.k7`). Scratchpad NOTES.md §6(2) names the remedy itself: "If record-level structure ever matters, the granularity decision (`mapping.md` §1: one artifact per node) is the thing to revisit."

**Testable consequence.**

Offline, now: re-run the importer at record granularity (one artifact per FCL-1 record, node artifact retained as a container with `dependence` refs to its records) on the same fixture and recount. Prediction: all 20 cross-document targets resolve to their intended record, `response#k7` retargets to `response#k2` and `rival#r9` rather than to `A_rival`, the 17 intra-document `depends` become real edges, and `objection_target_self_ref_dropped` falls to 0 — with no new evidence and no provider call. The counter-prediction worth checking is that record granularity multiplies artifacts ~7x and makes node-level labels meaningless, which is the real cost and should be reported as such.

**Proposed change.**

Extend the spec's address space: permit `<artifact-id>#<local-id>` as a `Warrant.target` and as a `refs[].target`, resolved deterministically against the pinned surface blob the harness already stores (it must already, since `theory(id)` renders it). Keep artifact identity unchanged; sub-addresses are resolution, not identity. Failing that, the repo must stop using node-granularity artifacts for H005 and say in every H005 report that record-level criticism targets were discarded.

**Confidence.**

0.88

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

I recomputed the corpus independently and the arithmetic is exactly right: 52 refs total; 20 cross-document target refs split 10 objection / 7 claim / 3 use; 17 intra-document depends split 12 use / 3 commitment / 2 claim; 9 intra-document mentions; 4 objection_target_self_ref_dropped (three on objection.o4, one on response.k7). FW5 L609/L628/L839 verified verbatim. The spec claim is verified by exhaustion: Warrant.target and refs[].target are both '<artifact-id>' and nothing in v1.3 defines a sub-artifact address. The k7 routing is confirmed by the import notes §2(7) verbatim: 'response.k3/k7 -> ...#r9 do not [retarget], because rival.r9 is untargeted and minted nothing, so they fall back to A_rival', and the golden att table lists '...response#k7->.../rival'. THREE CORRECTIONS. (1) FACTUAL: 'every cross-document reference in the corpus is of the form <16-hex node label>#<record id>' is false. objection.json's o1/o2/o3 use the PORT-label form 'p.objection.0#c1', and carry.n6 mentions a bare node label with no '#' at all. The claim should be 'every cross-document reference is record-addressed (<node-or-port label>#<record id>)', which is what the argument actually needs. (2) ATTRIBUTION: the spec does not force node granularity. Content is opaque bytes (§0), and one artifact per FCL-1 record with a container node carrying dependence refs is fully spec-legal — the finding's own testable consequence proposes exactly that and expects it to work without a spec change. So the loss is caused by the repo's mapping.md §1 election, not by a spec prohibition; the notes' own open question §6(2) names it that way ('the granularity decision ... is the thing to revisit'). The 'hinders' verdict should be re-scoped accordingly: the spec's defect is that it offers no sub-artifact RESOLUTION, which forces an all-or-nothing granularity election in which coarse grain silently discards FW5 L609's represented target. (3) CHARACTERIZATION: 'A criticism of one's own commitment was recorded as an attack on someone else's artifact' is half right. k7's authored target list is ['k2','935f7779b91148f4#r9'] — it names the rival's r9 itself. The distortion is subtler and worth stating precisely: k7 cites r9 as CONCEDING the problem ('The rival's r9 admits this and my k2 does not fully solve it'), so the mechanism converted a shared concession plus a self-qualification into a one-directional attack on A_rival, and that attack is what Lemma 3.1 then reinstates A_rival out of.

**Refuter — Corrected finding.**

Same evidence, re-scoped verdict. Claim: FW5 addresses a criticism and its use at the grain of a represented content (L609 target/defect/grounds/connection; L628 'must preserve internal role bindings, not merely the endpoint string'), and the H005 authors wrote at that grain — 20 of 21 cross-document references are record-addressed. v1.3 has no sub-artifact resolution: Warrant.target and refs[].target are both whole-artifact ids. That does not forbid record-grain artifacts (the spec's content is opaque bytes, so one artifact per record is legal), but it forces an all-or-nothing granularity election, and the repo's node-granularity election (mapping.md §1) then discards exactly what FW5 L609 calls the represented target. Concrete cost: response#k7 — which names its own k2 and cites rival#r9 as conceding the same point — loses its self-target to objection_target_self_ref_dropped and lands as a one-directional attack on A_rival, which Lemma 3.1 then reinstates A_rival out of. Drop 'every cross-document reference is of the form <16-hex>#<record>' (objection uses p.objection.0#c1). Proposed change should lead with the granularity re-run (which needs no spec change) and offer '<artifact-id>#<local-id>' resolution as the alternative, not the requirement.

### CU-5

**Finding id.**

CU-5

**FW5 claim.**

FW5 L640: "A source's appearance in a prompt is a delivery fact. A named field asking for a criticism is an invitation fact. Actual use of the source as a premise, actual understanding, and actual criticism are semantic attributions. They are not automatically machine-maintainable facts merely because a host can maintain corresponding labels." L634: "An observer may lack the data needed to establish the witness. That makes the attribution unresolved; it does not prove either understanding or its absence."

**Spec mechanism.**

harness-spec-v1.3 §1 L61 "Plain `mention` refs remain non-load-bearing." Engine reduction table, `/home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md` §6: "| `type: "use"` | **drop as a type** | `refs[].role = "mention"` |" and "| `type: "claim"` | **drop** | Every artifact is a claim; the marker adds nothing |".

**Verdict.**

absent-in-spec

**Argument.**

Two independent mismatches compound here. First, FCL-1's `use` record is not FW5 use at all: the importer's own gloss is "a use record proposes future uptake; it is neither a testable commitment nor a criticism and has no spec construct" (graph_import_h005.py:1602). It is prospective and authored — an invitation-grade fact in FW5 L640's sense — whereas FW5 use is retrospective and causal-organizational. So neither document currently has the relation FW5 names. Second, the one construct the spec does offer for it is the one it explicitly defines as inert. Mapping `use → mention` is therefore not a lossy approximation but a formal guarantee that nothing downstream reads it. The consequence for the programme is that the FCL-1 arm's headline contribution — making uptake visible — is discharged into a relation the spec's own §1 says nothing depends on, while FCL-1's `claim` marker (which is where the actual endorsing uses live, see CU-1) is dropped outright on the grounds that "every artifact is a claim" — true of the marker, false of the `target` field that rides on it.

**Repository evidence.**

Importer residue on the golden scope: `use_record_unmapped` 9 (record unit, severity "unmapped"), `claim_record_unmapped` 15 (record unit, severity "unmapped"), `target_on_non_objection_record` 7 (record unit, severity **"informational"**) with the reason string "'target' here means 'about', not 'attacks'; only type == 'objection' mints a warrant" (graph_import_h005.py:1642-1646). Those 7 records are exactly k1, k2, k6, n1, n4, n5, n7 — the endorsements, the repaired use and the retention decision. The repo's own instrument grades the refs that carry use as merely informational while grading the unused `claim` bodies as "unmapped"; that severity assignment is itself a criticism-and-use error inside the measuring apparatus.

**Testable consequence.**

Offline, now: re-grade `target_on_non_objection_record` from "informational" to "unmapped" and re-run `test_graph_import_h005.py`; the residue totals change and the REPORT.md table then states, truthfully, that 7 record-level relations to earlier criticism were carried by the language and lost by the mechanism. Across cycles (needs occurrence-02, ≥3 cycles): a prospective `use` record can be checked for discharge — did a later cycle report the outcome its `consequence` field predicted? Cycle-01 alone cannot answer this for any of the 9 `use` records, which is itself the finding: FCL-1 `use` is unobservable within one cycle by construction.

**Proposed change.**

Split the FCL-1 `use` type into `proposed_use` (prospective, authored, rendered only) and `used` (retrospective, carrying `{used: <id>#<local>, by: <id>#<local>, mode, witness_status ∈ {witnessed, declared-only, unresolved}}`), and map only the latter to the new `use` ref role of CU-1. Stop dropping `type:"claim"`: drop the marker, keep the `target` field, and route it to the `use` role rather than discarding it.

**Confidence.**

0.87

**Refuter verdict.** stands: false, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

The FW5 half is exact (L640 delivery/invitation/semantic-attribution, L634 unresolved != absent) and so is the spec half ('Plain mention refs remain non-load-bearing', spec L62). The residue counts are exactly right — I recounted from the artifacts: 9 use records (account u1, objection u1, response k5/k6, rival r6/r7/r8, carry n4/n7), 15 claim records, and target_on_non_objection_record fires on precisely k1, k2, k6, n1, n4, n5, n7 = 7 (k5 has depends but no target, and the finding correctly omits it). The importer's gloss at :1602 is verbatim. BUT THE INSTRUMENT CHARGE IS FALSE, and it is load-bearing for the verdict, the repo_evidence paragraph, the testable consequence and half the proposed change. graph_import_h005.py:_map_mention_refs reads: 'fields = ["mentions","revises","withdraws"]; if record.get("type") != "objection": fields.append("target")'. Non-objection target refs ARE mapped — to node-level mention refs. So 'informational' is the coherent grade (the relation is carried, inertly, at node grain; what is lost is the record grain, which is CU-4's finding, and the polarity, which is CU-1's), and 'unmapped' is the coherent grade for a claim RECORD that maps to no construct at all. Re-grading target_on_non_objection_record to 'unmapped' would make the instrument wrong by its own definitions. Correspondingly, 'FCL-1's claim marker ... is dropped outright on the grounds that "every artifact is a claim" — true of the marker, false of the target field that rides on it' misstates what happens: the design-of-record row drops the MARKER only, and the ref fields are handled by their own rows; in the importer the target survives as a mention. The second half of the proposed change ('Stop dropping type:"claim": drop the marker, keep the target field') asks for what is already done. Residual real point in that area: the design-of-record's reduction table has no row for a target on a non-objection record, so the importer's handling is an unrecorded elaboration of it — worth a table row, not a finding.

**Refuter — Corrected finding.**

Verdict absent-in-spec stands; delete the instrument charge. Claim: two constructs named 'use' are both absent. (a) FCL-1's use record is prospective and authored — an invitation-grade fact in FW5 L640's sense, per the importer's own gloss 'a use record proposes future uptake; it is neither a testable commitment nor a criticism and has no spec construct' — whereas FW5 use (L626-L628) is retrospective and causal-organizational. (b) The only spec construct offered for it, mention, is defined inert (spec L62), which is FW5-compatible abstention (L640) but guarantees nothing downstream reads it. Consequence for the programme: the FCL-1 arm's headline contribution, making uptake visible, is discharged into a relation nothing depends on, and cycle-01 alone cannot check whether any of the 9 prospective use records was ever discharged. Remove the claim that the importer's severity assignment is itself an error (non-objection target refs are mapped to node-level mention refs by _map_mention_refs, so 'informational' is correct) and remove the 'keep the target field' half of the proposed change (already done). Keep the proposed split of FCL-1 use into proposed_use and used, and the cross-cycle discharge test.

### CU-6

**Finding id.**

CU-6

**FW5 claim.**

FW5 L332: "Two systems with the same output table can have different active routes... A token-level authorship or causal attribution requires the internal event structure. Endpoint agreement establishes neither identity of active causes nor identity of contributors." L1218 (projection theorem): "Then no function of \(P(M)\) alone agrees with the accounting predicate on both models." L659: "The thinker can remove a rejected conjecture from its current working use while retaining its occurrence for comparison or later criticism... Availability as a current target requires some representation of that target."

**Spec mechanism.**

harness-spec-v1.3 §3 L189-195 anti-relapse: stage 3 "candidate's verdict-vector over the active battery matches a refuted prior's (`≈_B`, Def 3.5) ⇒ block **unless** the candidate carries a warrant against that prior's refuter." §11.5 L459-461: the refuted-artifact index "**is** the negative atlas... and are **never rendered into packs**... Enforce tabu at the door, not in the prompt."

**Verdict.**

hinders

**Argument.**

Anti-relapse is the only place in v1.3 where an earlier criticism constrains later content production at all, so it is the spec's closest approach to a use construct — and it fails FW5 on both of its two moves. (i) It individuates "the same explanation" extensionally, by agreement of verdict vectors over a finite battery (`≈_B`). FW5 L332 and the projection theorem at L1208-1224 say exactly that no function of endpoint behaviour agrees with the accounting predicate; so `≈_B`-difference is evidence that something changed, never evidence that the criticism was used, and `≈_B`-sameness is not evidence that it was not. (ii) The response is a *block* at the gate, with the refuted record deliberately withheld from packs. FW5 L659 requires that a rejected conjecture remain re-presentable as a current critical target, and (RC) L1062 requires target chains that "include criticisms, interpretations, methods, and prior appraisal practices" and forbids "silently deleting a chain because it concerns the actual evaluator." A tabu enforced at the door and invisible in the prompt removes precisely the representation those clauses require. The spec has an engineering reason for this (L461: "negative conditioning primes the very content it bans"), which is a real finding about generators; it is simply not compatible with FW5's account of how a criticism stays usable.

**Repository evidence.**

H005 gives the cleanest available instance of use being view-bounded rather than graph-bounded. `material.json` fork5 inputs: `rival <- [{"source":"account","view":"body"}]`; `carry <- [response both, account commitments, objection commitments, origin both]`; `response <- [account both, objection both, rival both]`. The `rival` never saw the objection and never references an `o*` record. The `response`, given the objection in full, produced k1 and k2 — the two clearest uses in the corpus. The `carry`, given the objection's *commitments only*, produced eight records (n1-n8) and referenced no `o*` record at all, targeting only the response's k-records. So within one cycle, full exposure yielded use and commitments-only exposure yielded none, while the `att` layer records nothing about either. What the spec's pack policy withholds is doing the work its `att` layer is being credited with.

**Testable consequence.**

Offline, now: over all five arms and all completed cycle-01 coordinates, cross-tabulate (view granted by material.json) × (cross-document references actually authored). Prediction on the evidence already in the tree: zero cross-document references to any source not exposed to that node (the harness never invented one), and a strictly lower reference rate from `commitments`-only views than from `both` views. n is small (17 COMPLETE coordinates per `occurrence-01/checkpoints/wave0005.json`), so this is a hypothesis to pre-register for occurrence-02, not a result. A sharper test needs new occurrences: hold the successor call fixed and vary only whether the refuted prior is rendered into its pack, and measure whether the successor can make that prior a critical target (FW5 L659) — which §11.5 as written forecloses.

**Proposed change.**

Amend §11.5 to distinguish the *generation* pack from the *criticism* pack: negative case law stays out of the conjecture pack (the priming argument holds) but MUST be renderable into a pack whose task is to criticise or re-target a prior appraisal, or §11.5 silently forecloses (RC). Add to §17 residue an explicit line that `≈_B`-difference is an endpoint criterion and is not evidence of a changed route. In the repo, record that H005 use is view-bounded and never read a null reference count as absence of uptake without checking the view.

**Confidence.**

0.72

**Refuter verdict.** stands: false, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

The FW5 citations are exact (L332, L1218 projection theorem, plus L1224 'The same argument applies to attribution from identical emitted text and to semantic use inferred from delivery logs', L659, RC L1062). The H005 view evidence is exact: material.json fork5 gives rival only {source: account, view: body}, carry {response both, account commitments, objection commitments, origin both}, response {account/objection/rival all both}; the rival authors no o-reference and the carry authors none either, targeting only k-records. Move (i) therefore has a real kernel. Move (ii) MISREADS §11.5. What §11.5 withholds from packs is the NEGATIVE ATLAS ENTRY — 'Refuted-region records (cluster centroid, exemplar ids, model-version tag, which response worked)' — not the refuted artifact. Refuted artifacts are not deleted (§0 D8), stay in A, stay attackable and reinstateable (N1 at L233: 'refuted->accepted by reinstatement ... No artifact ... is ever marked final'), are rendered by 'why <id>' and 'theory <id>' (§13 L497), and §10's precedent slices are pack-side. FW5 L659 asks for exactly this and no more: 'Availability as a current target requires some representation of that target, not an append-only history of every earlier thought' — the graph IS that representation, and L659's whole point is that removal from CURRENT WORKING USE is legitimate, which is precisely what a registration gate does. So 'removes precisely the representation those clauses require' is false. The (RC) L1062 citation is also repurposed: its 'does not authorize silently deleting a chain because it concerns the actual evaluator' governs self-referential target chains, not prompt rendering, and RC's own 'owned enabling continuation' is satisfied by an attackable refuted node. TWO FURTHER OMISSIONS ON MOVE (i). First, the gate's escape hatch is exactly the route-level condition the finding says is missing: stage 3 blocks 'unless the candidate carries a warrant against that prior's refuter' (L193), so a candidate that used the criticism to attack the refuter is admitted. Second, §17 already declares part of the residue: '≈_B in informal domains is irreducibly judgment-laden; paraphrase-invariance audits bound the damage.' Finally, the framing 'anti-relapse is the spec's closest approach to a use construct' is the finding's own construction, not the spec's claim, so faulting the gate for not being a use construct is a strawman.

**Refuter — Corrected finding.**

Keep only move (i), as a §17 residue item. Claim: anti-relapse stage 3 individuates 'the same explanation' by agreement of verdict vectors over a finite battery (≈_B, §3 L193). FW5 L332 and the projection theorem at L1208-1224 establish that no function of endpoint behaviour agrees with the accounting predicate, and L1224 extends this to 'semantic use inferred from delivery logs'. Therefore ≈_B-sameness is not evidence that a criticism was not used, and a candidate that genuinely took up the criticism but lands on the same verdict vector — without attacking the prior's refuter, which is the gate's only escape hatch — is blocked. §17 already concedes ≈_B is judgment-laden in informal domains; it should additionally state that ≈_B-difference is an endpoint criterion and is not evidence of a changed route. DELETE move (ii) entirely: §11.5 withholds negative-atlas records (centroids, exemplar ids) from packs, not refuted artifacts, which remain in A, attackable under N1, and renderable via why/theory — which is exactly what FW5 L659 requires, and L659 positively licenses removal from current working use. The view-boundedness observation (full exposure yielded uptake, commitments-only exposure yielded none) is sound and worth pre-registering for occurrence-02 as stated.

### CU-7

**Finding id.**

CU-7

**FW5 claim.**

FW5 L839: "\(\operatorname{ProducesVia}\) requires the construction account of the repair to contain the relevant binding of \(c\) on its active route. These are additional conditions, not inferences from temporal co-occurrence." L800 (ProducedBy): "It is not satisfied by temporal succession alone." (P) L791-797: repair = some `o∈O` goes from unsatisfied to satisfied, every `r∈P` preserved, and the change is `ProducedBy` the contribution.

**Spec mechanism.**

harness-spec-v1.3 §3 L179 Spawn trigger "failed verdict ⇒ successor problem (P2)"; §5 L231-237 N1/N2 fallibilism axioms; §3 L193 anti-relapse. Nothing in v1.3 records that a successor's content was produced via the criticism; the successor relation is a scheduling fact plus an `≈_B` non-equality obligation. Repo falsifier: `/home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md:890` and `:914` — "if, under the new engine, attack edges land on H005 criticisms and root still cannot identify a single episode in which a warranted criticism changed a later operative use, then the missing ingredient was never the bookkeeping."

**Verdict.**

hinders

**Argument.**

The programme's own stated falsifier for the engine intervention is mis-specified against both documents. It treats "attack edges land" as the antecedent and "a warranted criticism changed a later operative use" as the consequent, as though the first were the mechanism for the second. But v1.3 never claimed `att` tracks use (§4 L229 is explicit about what feeds labels), and FW5 L839/L800 require that a repair claim carry a construction account binding the criticism on its active route — a positive object nothing in v1.3 produces or even names. As worded, the falsifier cannot discriminate: if root fails to find an episode, that may be because the engine bought auditability instead of error correction (the intended reading), or because the engine records a relation orthogonal to the one root is looking for (the actual situation); and if root succeeds, it will have succeeded by reading text, as I did here, with the graph contributing nothing. FW5's repair is a positive, attributable, route-bearing change; the spec's nearest analogue is the absence of relapse, which is a negative endpoint condition. Repo doctrine already forbids exactly this substitution: `experiments/diagnostics/H005-open-prose-commitments/PROTOCOL.md:64` — "Parser success, agreement with root, adoption of a standard answer, more objections, novelty of wording and longer memory do not establish repair."

**Repository evidence.**

The best-formed repair in the corpus is invisible to the mechanism. `carry.json`: n1 and n3 are the criticism (n3 targets `response#k2` and `#k7`: "Stating k2 at that strength while keeping k7 in the record presents the track as sharper than the carry's own concession allows"); n4 is the repaired use targeting `response#k5` ("Treat a pullback-from-form outcome as *raising* the unit-versus-privacy reading, not as confirming it") and carries `depends: ['n1','n3']` — the author's own declared binding of the criticism to the repair, i.e. the authored shape of ProducesVia. n7 (`depends: ['n1','n3']`) records the protected obligations: "Keep the carry's records as they stand and add n1, n3, n4, n5 alongside them... my additions narrow their claims rather than replace them" — an explicit `P`-set preservation in FW5 (P)'s sense. Every one of these relations is lost: n4/n7's `depends` are intra-document (collapsed by CU-4), n4/n7's cross-document `target` refs fall under `target_on_non_objection_record`, and the only computed effect is `A_carry` attacking `A_response`.

**Testable consequence.**

Offline, now: take `carry.n1/n3/n4/n7` as a candidate (P)-instance, name O = {the confirmatory-ceiling obligation n4 installs} and P = {the sequencing and stopping commitments n7 names as preserved}, and check FW5 (P)'s three clauses by reading. Prediction: clauses 1 and 2 are satisfiable on the text; clause 3, `ProducedBy`, is satisfiable only as an *authored declaration* (n4's `depends`), never as an observer's construction account, because occurrence-01 supplies no contrast under which n4 would have differed had n3 been absent or recoded. That is the decisive limit: FW5 L800 says temporal succession alone does not satisfy `ProducedBy`, and a single linear cycle supplies nothing but temporal succession. Establishing repair therefore requires new occurrences with a criticism-ablated arm — same topology, same views, criticism node's content replaced by a content-preserving recoding and by a substantively different objection.

**Proposed change.**

Reword the engine falsifier to name what the graph must show rather than what root can find by reading: e.g. "if, with record-level `att` edges and a reported `use` relation, the graph exhibits no (criticism, later-record) pair whose `use` entry root independently confirms by reading, the bookkeeping bought auditability rather than error correction." And add a criticism-ablation arm to the occurrence-02 plan before any provider call, since without a contrast no `ProducedBy` and hence no (P) instance is establishable from H005 at all.

**Confidence.**

0.8

**Refuter verdict.** stands: false, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

The FW5 citations are exact (L791-797 (P), L800 'It is not satisfied by temporal succession alone', L839 ProducesVia 'requires the construction account of the repair to contain the relevant binding of c on its active route ... not inferences from temporal co-occurrence'), and the carry.n1/n3/n4/n7 reading is accurate: n3 targets response#k2 and #k7, n4 targets #k5 with depends ['n1','n3'], n7 targets #k8 with depends ['n1','n3'] and names the preserved obligations. PROTOCOL.md verbatim confirms 'Parser success, agreement with root, adoption of a standard answer, more objections, novelty of wording and longer memory do not establish repair.' BUT THE HEADLINE CLAIM — that the falsifier is mis-specified — does not survive reading the falsifier. Its form is: (att edges land on H005 criticisms) AND (root still cannot identify an episode in which a warranted criticism changed a later operative use) => 'the missing ingredient was never the bookkeeping, the engine bought auditability rather than error correction.' That is not a claim that att tracks use; it is the negation of that claim held open as a testable outcome — the standard shape of 'we performed the intervention; if the outcome does not follow, the intervention was not the bottleneck.' The finding's own discrimination objection collapses on inspection: its two disjuncts, 'the engine bought auditability instead of error correction' and 'the engine records a relation orthogonal to the one root is looking for', are the same conclusion in different words, and both are what the falsifier says it will report. The asymmetry complaint ('if root succeeds, it will have succeeded by reading text') is also misplaced: the sentence is stated as a falsifier only, and the receipt commits in advance that 'that outcome will be reported as evidence with the same weight as a positive one' — it claims no confirmatory power for a positive result. SECONDARY: 'the only computed effect is A_carry attacking A_response' undercounts — the golden att also carries (A_carry, nu(W_k7)), which the import notes call out as the graph now recording 'why the response's objection against the rival stopped counting'. The ProducesVia point is untouched by that, but the sentence as written is inaccurate. WHAT SURVIVES INTACT: the ablation argument. FW5 L800 ('not satisfied by temporal succession alone') plus L630's required contrast contract (a content-changing case, a content-preserving recoding, and a carrier disturbance) plus L839 together mean no ProducedBy and hence no (P) instance is establishable from a single linear cycle, which is what occurrence-01 is. That is correct, decisive, and actionable.

**Refuter — Corrected finding.**

Drop the falsifier critique; keep and lead with the ablation requirement. Claim: the best-formed candidate repair in the corpus — carry n1/n3 (the criticism), n4 (the repaired use, depends ['n1','n3']), n7 (the declared preservation of the sequencing and stopping commitments) — satisfies FW5 (P)'s first two clauses on the text, but clause 3, ProducedBy, is satisfiable only as the AUTHOR'S declaration, never as an observer's construction account, because occurrence-01 supplies no contrast under which n4 would have differed had n3 been absent or recoded. FW5 L800 forbids inferring it from temporal succession, L630 fixes the required contrast contract, and L839 requires the binding of c on its active route. Therefore: add a criticism-ablation arm to the occurrence-02 plan before any provider call — same topology, same views, criticism node's content replaced once by a content-preserving recoding and once by a substantively different objection — since without it no (P) instance is establishable from H005 at all. Remove the claim that the engine falsifier is mis-specified (its antecedent-and-null-result structure is exactly 'the bookkeeping was not the bottleneck', and both of the alleged competing readings are that same conclusion; the receipt pre-commits to reporting the negative with equal weight), and correct 'the only computed effect is A_carry attacking A_response' — att also carries (A_carry, nu(W_k7)).

---

## Axis 3 — error-correction: FW5's fallibility, criticism-bearing, reason-use and repair against harness spec v1.3's N1/N2, grounded reinstatement (Lemma 3.1), anti-relapse, and validity-node attacks

**Critic's overall assessment.**

On error correction the spec is strong exactly where FW5 is thin and weak exactly where FW5 is specific. Its best work is negative-hygiene: "a bare verdict is never an edge" (L115), N1's guarantee that no artifact is ever final (L233), Refl's registration of standards, adjudication semantics and guard procedures as attackable artifacts (L173), and the validity node as the place where a test's auxiliaries and its relevance interpretation are parked and made attackable (L103, L307). That last is a real mechanization of FW5's (K3) at L663-676 — the one place the spec gives FW5 something FW5 does not give itself. But the spec's core error-correction primitive, grounded reinstatement, does not model FW5's "criticism answered". Lemma 3.1 reinstates a target whenever its attacker is attacked by an unattacked node, with no condition that the counter-attack bear on the alleged defect; FW5 makes bearing a substantive Account of the defect question (K1, L611-620) and separately warns that withdrawing a criticism "does not establish the truth of its target" (L657). What reinstatement actually computes is closer to FW5's de-licensing under (K2) than to repair, and the spec then feeds the resulting `accepted` label into HV, reach, Pareto and cross-evaluation, so the mis-modelling is not inert. The H005 record makes the divergence concrete rather than theoretical: in the one arm that yields machine-readable criticism, the only records that would generate attack edges under the repo's own reduction table are the authors' self-qualifications (o4, k7, n3), while the record that actually shows a criticism landing — "The objection is right that the account's recurrence test has low discriminating power", followed by a redesigned probe — generates no edge at all and is pre-registered as invisible to status computation. The anti-relapse gate then compounds this: it makes sameness-of-explanation a function of an endpoint verdict vector, which FW5's own projection theorem (L1208-1224, enumerated at L1402) says cannot track the accounting predicate, and it conditions re-entertaining a refuted content on already possessing a counter-warrant, inverting FW5's "an idea may be entertained without first being justified" (L55). Finally, FW5's actual unit of error correction — Repair (P) at L791-797, with its protected obligations and its rule that losses outside P must be exposed — has no counterpart anywhere in v1.3; the repo has already written the FW5-side version into RESEARCH_AGENDA.md:81 and H005 PROTOCOL.md:62 and assigned it to root rather than to any mechanism. Net: keep §1's warrant/ν architecture and N1/Refl; treat reinstatement, `≈_B` and the anti-relapse block as mechanisms whose FW5 warrant has not been shown.

**Refuter's axis summary.**

Four of eight findings survive; four do not.

REFUTED: EC-1, EC-2, EC-4, EC-5.

EC-1 and EC-2 share one defect: both demand that the harness mechanize a FW5 predicate that FW5 L640 explicitly declares not machine-maintainable ("Actual use of the source as a premise, actual understanding, and actual criticism are semantic attributions... not automatically machine-maintainable facts merely because a host can maintain corresponding labels"), and both overlook machinery the spec already has — the validity_node plus §1 L107 closure, which lets "your reinstating attack did not address my defect" be registered as an ordinary attack on the reinstater's ν; and the `mention` role, which is already the adjudication-inert declaration channel EC-2 proposes to add as `uses`. Both also fail on the repo data. Reading occurrence-01/artifacts/daily/mini_fcl/cycle01 directly: o4's targets are bare local ids (`["o1","o2","c2"]`), which the reduction's own resolution rule leaves unresolved and which in any case name records inside the same single artifact, so no reinstating edge arises; and the claimed edge inventory omits o1/o2/o3 (→ account), k3 (→ rival) and misdescribes n3 (→ the prior carry artifact `b998d514348ed94e`, not itself). Outward attack edges outnumber self-directed ones roughly 5:1, which inverts EC-2's headline.

EC-4 reads §3's anti-relapse as firing on verdict-vector equality alone; §3 L192 gates stage 3 behind stage 2's embedding-neighbour trigger, and the finding patches the hole with the P1 implementation's declared stage-2 divergence rather than the spec under review. EC-5's "completed counter-criticism" bar does not exist: an argumentative warrant is uncertified and conjectural (§1 L99, L115), so the sentence EC-5 offers as its blocked test case is itself registrable; and FW5 L659 expressly licenses withholding a refuted conjecture from working use while its occurrence stays available as a target. EC-5 and EC-7 are also mutually inconsistent — EC-5 attacks the ν-escape that EC-7 praises as the spec's best K3 engineering.

STAND: EC-3, EC-6, EC-7, EC-8. EC-3's gap is real (§4 L219 is a flat conjunction; no schema field expresses alternative sufficient routes), though FW5 L690 makes receipts optional descriptive mathematics and FW5 L653 offers criticism-of-the-declaration as the native remedy. EC-8's absence is confirmed by grep and is honestly labelled "absent-in-spec" rather than a violation, consistent with §17 L578 and FW5 L1274.

EC-6 and EC-7 stand as "helps" but each contains an error worth striking. EC-6 imports FW5 L628 (a reason-use witness condition on a response occurrence) into L1052's return-relevance condition, after correctly noting that L1052 admits "attention state" — and misses §11.4 L452's complement directives, which do return refutation-derived content to the pack. EC-7's residue claim ("nothing in the spec ever proposes that B or I might be at fault") is false: §3 L183's audit-the-critic trigger, §10 L389's audit warrants aimed at ν nodes and standards, and §11.3/§11.4's validity-node-attack-rate flag all automate exactly that. Its surviving half — that every demonstrative ν should enumerate its auxiliary claims the way §7 L307 does — is the better recommendation.

Files read: /home/user/miniReason/docs/sources/FW5-explanatory-construction.md, /home/user/miniReason/docs/sources/harness-spec-v1.3.md, /home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md, /home/user/miniReason/docs/SEMANTIC_GUIDE.md, /home/user/miniReason/docs/RESEARCH_AGENDA.md, /home/user/miniReason/docs/EXPERIMENT_METHOD.md, /home/user/miniReason/docs/mini/ERRATA.md, /home/user/miniReason/PURPOSE.md, /home/user/miniReason/experiments/diagnostics/H005-open-prose-commitments/PROTOCOL.md and .../occurrence-01/artifacts/daily/mini_fcl/cycle01/*.json. No files modified.

### EC-1

**Finding id.**

EC-1

**FW5 claim.**

FW5 L611-620 (K1): "Bearing(c,z,p) ⟺ Account(𝓔_c, p_δ)" … "The alleged defect must concern the stated target and respect." FW5 L622: "A criticism occurrence can exist when (K1) is false. Its grounds may be mistaken, its target misidentified, its inference invalid, or its relevance wrong." FW5 L657: "Withdrawing a criticism likewise does not establish the truth of its target."

**Spec mechanism.**

harness-spec-v1.3 §3 L187 "Reinstatement is derived, not a rule (Lemma 3.1): if `k` attacks `a`, `j` attacks `k`, `j` unattacked, then `{j,a} ⊆ G`."; §4 L209-214 grounded fixpoint; §1 L107-108 validity-node and case-law closures ("refute a standard ⇒ … targets reinstated (Lemma 3.1 mechanics)").

**Verdict.**

hinders

**Argument.**

Grounded reinstatement is a topological property of the attack graph: a is restored on the sole condition that some unattacked j attacks a's attacker k. Nothing requires j to address δ, the defect k alleged, or a's question p. FW5 makes being-answered substantive: the counter-criticism must itself be an Account of the defect question p_δ. So a j that attacks k on an incidental ground — a scope quibble, a mistaken premise k did not need, the critic's own hedge — reinstates a exactly as strongly as a j that shows the alleged defect is not a defect. What Lemma 3.1 actually computes has a FW5 counterpart, but it is (K2) de-licensing at L642-653 (Usable_j(u) fails when an essential premise loses standing), and FW5 L657 states in the same breath that de-licensing is not truth restoration and that another argument for the same conclusion can remain usable. The spec knows status is not truth (§0 L32 "Status is computed, never stored as ground truth"), but `accepted` is the gate for HV estimation (L251 "lazy, accepted artifacts only"), reach cross-evaluation (L267), Pareto retention and the low-HV Spawn trigger (L181) — so a reinstatement obtained by an off-target counter-attack buys real downstream standing.

**Repository evidence.**

/home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md:185-186 spells the closures out as carrier-level attacks whose point is "what makes the carrier fall out of G and the target reinstate in pass 1"; :229 and :232 are the two reinstatement tests, the second asserting "no status rule outside `att`/`dep` ran". /home/user/miniReason/docs/mini/ERRATA.md:82-84 records the opposite failure in the frozen engine ("nothing could be refuted or reinstated"), which is why reinstatement was adopted uncritically as the repair. Nothing in docs/reviews/ tests whether a reinstating attack bore on the original defect.

**Testable consequence.**

Offline on existing H005 evidence, no new occurrences. Build `att` from the FCL-1 `objection.target` fields per the repo's own reduction table (engine-design-of-record :367) over experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/. In objection.json, record `o4` (type objection) targets `[o1, o2, c2]` and nothing targets `o4`; grounded semantics therefore puts o4 in G, refutes o1 and o2, and reinstates the account. Then read o4's own text: "My own objection may over-reach… If ambiguity is in fact the plainest reading, the objection reduces to a complaint about sequencing rather than about substance." That is a conditional self-qualification, not an Account of a defect in o1 — K1 is false of it. The decisive observation is the mismatch with what the author downstream actually did: response.json `k1` says "The objection is right that the account's recurrence test has low discriminating power". Status says reinstated; use says the criticism landed.

**Proposed change.**

To the spec: require an argumentative warrant's validity node to carry two declared fields — the defect question p_δ and the grounds→defect connection — mirroring FW5 L609's four-part criticism. Derive a reinstating edge only from an attack registered against the grounds or the connection; an attack on other content of the critic artifact registers as `mention` and does not reinstate. Additionally, record `reinstated_by: <warrant-id>` on the label so `why <id>` (§13 L497) shows which attack did the reinstating and a reader can check whether it addressed the defect. To the programme: do not report a reinstated H005 artifact as "criticism answered" without a separate bearing argument.

**Confidence.**

0.85

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The FW5 quotations (L609, L611-620, L622, L657) are verbatim-accurate and the description of Lemma 3.1 (spec L187) is accurate. Three things defeat the finding as written.

(1) FW5 misread. The finding treats Bearing(c,z,p) as something the harness ought to compute or gate on. FW5 L640 says the opposite in terms: 'Actual use of the source as a premise, actual understanding, and actual criticism are semantic attributions. They are not automatically machine-maintainable facts merely because a host can maintain corresponding labels.' L634: an observer lacking the witness data leaves the attribution 'unresolved'. And L622 expressly countenances the very case the finding calls a defect — 'A criticism occurrence can exist when (K1) is false... its relevance wrong.' A framework that registers non-bearing criticism occurrences as occurrences is FW5-conformant; one that computed a Bearing predicate at the gate would be exactly the machine-maintainable-label error FW5 warns against, and would also violate spec §0 L33.

(2) Spec misread — the bearing hook already exists. Every warrant carries a `validity_node` (§1 L103), and §1 L107's closure rule makes any attacker of ν an attacker of the warrant and hence of its carrier's attack edge. So 'j's attack does not address the defect k alleged' is registrable, today, as an argumentative warrant against j's warrant's ν; the closure then restores k's edge and un-reinstates a — in pass 1, with no new rule. This is the same mechanism EC-7 praises. The finding's proposed change converts an available criticism into a mandatory gate, which is the move §0 forbids and FW5 L640 counsels against.

(3) The downstream-standing list overstates. HV estimation (§6 L251), reach cross-evaluation (§6 L269) and Pareto retention (§11.7) are attention and budget, explicitly declared 'Never a status; an artifact off the frontier is merely unfunded, not demoted' (L469) and fenced by §0 L33. FW5 L1052 itself lists 'attention state' as a legitimate locus of operative return, so attention consequences are not illicit standing.

(4) The decisive empirical demonstration is wrong on the repo's own data. In occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json, o4's `target` is `["o1","o2","c2"]` — bare local ids, not the `exposed-artifact-label#local-ID` form the reduction requires; engine-design-of-record's reference-resolution rule ('A reference to an unexposed label mints no ref and is recorded as unresolved; the harness never invents an id') means o4 mints no warrant at all. Even granting resolution, o1, o2, c2 and o4 all live inside one artifact (406eff78…), and §1's warrant `target` is an artifact id — so o4 would be a self-attack on the objection artifact, which under the grounded fixpoint (§4 L210-214) keeps that artifact out of G and leaves the account `suspended`, not `accepted`. Either way the account is not 'reinstated', so the claimed mismatch with response.json k1 does not arise.

**Refuter — Corrected finding.**

Spec §3 L187 and §13 L497 should say explicitly that reinstatement is a bookkeeping consequence of the attack topology and carries no claim that the reinstating warrant bore on the defect (FW5 L622, L640, L657), and `why <id>` should name the reinstating warrant and its ν so a reader can raise that question as an ordinary attack on the ν. No new gate, no new schema field: FW5 L640 forbids treating bearing as a host-maintainable fact, and §1 L107's closure already supplies the contest route.

### EC-2

**Finding id.**

EC-2

**FW5 claim.**

FW5 L626-628: "A response uses a reason when the represented content of the objection participates in the organization's deliberative transition… the mapped objection is on an active dependency route of this response occurrence. The map must preserve internal role bindings, not merely the endpoint string." FW5 L630: "Understanding and using an invalid objection does not make it valid. The definition concerns whether the system used the content, not whether it responded ideally."

**Spec mechanism.**

§4 L229: "**Inputs to adjudication are `att` and `dep` ONLY.**"; §1 L37-43 — the only ref roles are `dependence`, `mention`, `evidence`, and only `dependence` makes a support edge; §3 Crit L169 requires a warrant to make an attack edge.

**Verdict.**

hinders

**Argument.**

FW5's unit of error correction is reason-use: the objection's content on an active dependency route of the response. The spec's adjudication has exactly two inputs, and neither can express it. An artifact that says "the objection is right, so I replace my two-item probe with a one-item probe" carries no warrant against anything (it is not attacking) and declares no `dependence` on the objection (the objection is not a premise it uses to derive a conclusion — it is a reason that changed a design). So endorsement-of-a-criticism, which is FW5's positive signal, produces no edge and no label movement. Meanwhile self-qualification — "my own objection may over-reach" — has exactly the syntactic shape (`type: objection` + `target`) that the reduction table turns into a ν plus an argumentative warrant plus an att edge. The graph therefore moves on hedges and stands still on uptake. This is not an incidental gap: §0 L33 forbids anything but `att`/`dep` from entering label computation, so the fix cannot be a measure.

**Repository evidence.**

In occurrence-01/artifacts/daily/mini_fcl/cycle01, the only records with local targets are `o4` (objection.json, targets o1/o2/c2) and `k7` (response.json, targets k2) — both self-directed; carry.json `n3` attacks the same k2 again. The uptake is carried in fields the repo has already ruled mechanically inert: docs/design/engine-design-of-record-2026-09-14.md:27 "the verdict that `claim` and `uptake` contribute nothing mechanical", :718 "`claim` and `uptake` produce NO commitment, NO ref and NO warrant", :857 "'uptake' never appears in any status computation". The pre-registered falsifier at :890 names the same worry from inside: "if… root still cannot identify a single episode in which a warranted criticism changed a later operative use, then the missing ingredient was never the bookkeeping, the engine bought auditability rather than error correction".

**Testable consequence.**

Offline on existing evidence. Over the five FCL-1-bearing artifacts of occurrence-01/daily/mini_fcl, count (a) edges derived under the reduction table and (b) records that state uptake of a named prior criticism. Present ratio is 3 self-directed attack edges to at least two explicit uptakes (response k1 endorsing o2; carry n1 endorsing k7) that produce nothing. If the ratio holds on cycles 2-3 and on the physics/philosophy/sociology chains, the graph is systematically anti-correlated with reason-use. Deciding whether uptake is *correctly* attributed needs FW5's contrast contract (L630: content-change / content-preserving recoding / carrier disturbance) and therefore new occurrences; establishing the invisibility does not.

**Proposed change.**

To the spec: add a fourth `refs[].role` — `uses` — declaring which prior criticism record an artifact's change depends on. Keep §0's invariant by making it adjudication-inert: `uses` enters neither `att` nor `dep`, but is exported by `why`/`theory` and is the anchor a reason-use claim must cite. To the programme: stop treating the FCL-1/prose edge asymmetry as the measured contribution (engine :890) without also recording that the derived edges are dominated by self-qualification; report the uptake records alongside the edge count so root's "what subsequent use actually changed" (PROTOCOL.md:62) is not silently competing with a graph that scores the opposite thing.

**Confidence.**

0.8

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

(1) FW5 misread. The finding equates FW5's reason-use with endorsement-of-a-criticism ('endorsement-of-a-criticism, which is FW5's positive signal'). FW5 L630-632 explicitly separates them: 'Understanding and using an invalid objection does not make it valid... A valid criticism can lead to retention when its alleged force has been misunderstood.' Retention — non-endorsement — is as much reason-use as revision. A harness that logged endorsements would not be tracking L628's witness; it would be tracking the terminal action label L626 rules out ('not just a terminal action label'). L634 adds that an observer lacking the witness data leaves the attribution unresolved, which is the spec's honest position.

(2) Spec misread. The spec has three ref roles, and `mention` (§1 L46, L62: 'Plain `mention` refs remain non-load-bearing') is already the adjudication-inert declared channel the finding asks for; the proposed `uses` role duplicates it. Further, an artifact whose standing turns on a prior criticism can declare `dependence` on it — nothing in §1 L53 restricts `dependence` to syllogistic premises, and the repo's own reduction table does exactly this for `revises`: 'Successor artifact with a `dependence` ref to the revised artifact plus an argumentative warrant against it.' So 'endorsement produces no edge and no label movement' is false in the repo's own mapping.

(3) The empirical ratio is wrong. Reading the cycle01 commitment surfaces: objection.json's o1, o2, o3 are all `type: objection` targeting `p.objection.0#c1/#c2/#c3` — outward attacks on the account. response.json's k3 targets `935f7779b91148f4#r6` and `#r9` — an outward attack on the rival. k7 targets `935f7779b91148f4#r9` as well as a bare `k2`. carry.json's n3 targets `b998d514348ed94e#k2` and `#k7` — the prior carry artifact, not itself. So the claim that 'the only records with local targets are o4 and k7 — both self-directed' and 'carry.json n3 attacks the same k2 again' misdescribes the data: n3 attacks a different artifact, k3 is omitted entirely, and outward attack edges outnumber self-directed ones roughly 5:1. 'The graph moves on hedges and stands still on uptake' is not what the record shows.

(4) The reduction table is an engine-design artifact, not spec v1.3; §0 L30 makes dispatch structural and mandates nothing about turning prose `objection` fields into warrants. A defect in the repo's reduction is not a defect in the spec under review.

**Refuter — Corrected finding.**

The spec cannot represent a reason-use witness in FW5 L628's sense, and FW5 L640/L634 say it should not try to; what it can and should do is render declared uptake. Recommend: require an artifact that changes because of a prior criticism to declare either a `dependence` ref (when its standing turns on that criticism) or a `mention` ref (when it does not), and export both in `why`/`theory` — no new role, no adjudication change. Drop the empirical ratio claim: cycle01's derived edges are predominantly outward-directed (o1/o2/o3 → account, k3 → rival, n3 → prior carry), not self-qualifying.

### EC-3

**Finding id.**

EC-3

**FW5 claim.**

FW5 L657: "Suppose a system withdraws an essential premise of u. Equation (K2) no longer licenses u. **Another argument v for the same conclusion can remain usable.** The conclusion is not thereby false." FW5 L682: "Distinct sufficient routes remain distinct receipts… **A refutation by an independent disjunct must not inherit the disputed assumptions of an unused disjunct.**" FW5 L1348 (h-EPI D2): "an independent sufficient disjunct must not inherit a defeated unused premise".

**Spec mechanism.**

§4 L219: `supported(a) = all(final(b) == accepted for (a,b) in dep)`; L226: "Refuting a premise ⇒ dependents become `suspended_unsupported`, NOT `refuted` (orphaned ≠ false)."

**Verdict.**

hinders

**Argument.**

The label is right and the propagation is wrong. `suspended_unsupported` is close to a quotation of FW5 L657's second half — orphaned is not false — and is a genuine improvement on the frozen engine's two-valued scheme. But `supported` is a flat conjunction over every `dependence` ref, so an artifact with two independent sufficient supporting routes falls the moment either falls. FW5's receipts keep distinct sufficient routes distinct precisely so that defeat of one does not reach the other, and FW5 endorses the h-EPI review's D2 finding in those words. The spec's schema also creates a perverse incentive: an author who honestly declares both routes is worse off than one who declares only the stronger, which runs against the repo's own declaration rule.

**Repository evidence.**

/home/user/miniReason/docs/SEMANTIC_GUIDE.md:39 "Declare unused dependencies rather than inventing them." /home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md:857 already tests the conjunctive behaviour as correct: "a refuted premise moves its dependent to `suspended_unsupported`". FW5's own reconciliation section cites the h-EPI D1-D5 findings approvingly at L1348, so the repo's semantic authority has already ruled on this case.

**Testable consequence.**

Offline, on the P0 engine, no provider calls. Register `a` with `dependence` refs on `b1` and `b2` where either alone is stated to support `a`; refute `b1` with an ordinary warrant; observe `a` → `suspended_unsupported` while `b2` remains `accepted`. That is the D2 failure mode with no way to express the disjunction. Decisive: there is no field in the §1 schema that could make the two refs alternatives rather than conjuncts.

**Proposed change.**

Add an optional `refs[].route: "<label>"` grouping dependence refs; `supported(a) = ∃ route R : ∀ b ∈ R, final(b) == accepted`, with the default (no label) being one route, i.e. exactly today's behaviour. Add a test named for FW5 L682 / h-EPI D2 asserting that refuting one route leaves a dependent supported by an intact second route `accepted`. This is a two-line change to §4 and a schema field, and it removes the incentive to under-declare.

**Confidence.**

0.75

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

Both citations check out: §4 L219 is a flat conjunction over every `dependence` ref, §4 L226 does yield `suspended_unsupported`, and §1's schema has no field grouping refs into alternative routes. FW5 L682 and L1348 say what the finding says they say. The available rebuttals only narrow the claim, they do not defeat it.

(a) Scope of L682. It sits inside 'Evidence receipts without false certainty', and FW5 L690 immediately declares that construction 'optional descriptive mathematics' — 'Ordinary prose need not arrive with a tree, source fields, or a machine-verifiable witness to enter inquiry.' So L682 is not a requirement FW5 imposes on any adjudicator; L1348 reports the h-EPI D2 concern and says FW5's own receipt/application distinctions give it 'a semantic expression'. The finding's phrase 'the repo's semantic authority has already ruled on this case' is a shade stronger than L1348 licenses.

(b) FW5 supplies a different remedy. K2 (L642) defines Prem(u) as the *declared* essential premises, and L653 says 'A record declaring a dependency does not establish that the dependency is actually essential; an error in that declaration is another criticism target.' Under FW5, over-declaring both routes as dependence is an error in the interface that is itself criticisable — and the spec permits that (the interface is part of the content-addressed artifact; a successor declaring only the surviving route registers freely under N2).

(c) The harm is bounded and the finding concedes it. §4 L226's `suspended_unsupported` is precisely FW5 L657's 'the conclusion is not thereby false'; nothing inherits defeat in the truth sense, and N1 keeps the label revisable.

(d) The 'perverse incentive' cite is strained. SEMANTIC_GUIDE.md:39's 'Declare unused dependencies rather than inventing them' sits in a paragraph about declaring the *interpretation* claim before the evidence; it is an honesty rule about attribution claims, not a rule about §1 `dependence` refs.

None of this touches the core: there is no expressible disjunction, the proposed `refs[].route` grouping is a two-line change that defaults to today's behaviour, and D2 is a real failure mode. The verdict word 'hinders' is arguably strong for a gap that produces the correct label — but the gap is real.

**Refuter — Corrected finding.**

### EC-4

**Finding id.**

EC-4

**FW5 claim.**

FW5 L1208-1218: "Let P be a projection from full organization models to an observed input–output description… Then no function of P(M) alone agrees with the accounting predicate on both models." L1222: "Parallel and priority wiring provide a concrete instance when the projection retains only endpoint values and the question concerns the active route." L1402: "All four Boolean input assignments were checked… Their endpoint outputs agree, while the active second route differs when both inputs are on." FW5 L144: "Contents are not identified merely because they have the same truth value or final output."

**Spec mechanism.**

§3 L193 anti-relapse stage 3: "candidate's verdict-vector over the active battery matches a refuted prior's (`≈_B`, Def 3.5) ⇒ block"; §6 L257 "Count only inequivalent survivors (a rename is the same explanation)"; §17 L582 "`≈_B` in informal domains is irreducibly judgment-laden".

**Verdict.**

hinders

**Argument.**

Stage 3 makes identity-of-explanation a function of the endpoint verdict vector over the active battery. FW5 proves that no function of an input–output projection can agree with the accounting predicate across two models that differ in active route, and checked an instance exhaustively. So `≈_B` can classify as 'the same refuted explanation' a candidate with different anchoring, a different active dependency route, and therefore a different Account verdict — and unlike everywhere else in the spec, the consequence is not a label but non-entry: the content never becomes an artifact, never becomes a target, and never appears in the trace except as a blocked-registration log line. The spec concedes `≈_B` is judgment-laden (L582) but uses it hardest at the one place where a false identification is unrecoverable by criticism. Note also that the very same projection theorem is what makes the spec's own anti-behaviourism (FW5 L232, spec §10 skeletons) coherent — the spec accepts the theorem for judging explanations and then violates it for individuating them.

**Repository evidence.**

/home/user/miniReason/docs/SEMANTIC_GUIDE.md:57 records FW5's licensing of "nonmonotone, redundant and infinitary support families" and that "Reach or edit-survival counts supply no numerical warrant" — i.e. the repo already holds that behavioural surrogates do not fix content identity. /home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md:681,684 pin the implemented signature: `anti_relapse.check(..., refuted_vectors, candidate_vector, ...)`, with the test "a candidate whose battery vector equals a refuted prior's is blocked at stage 3". Stage 2 (semantic NN) is declared absent and fails open (:262), so in this repository the whole burden of stage 2+3 falls on the verdict vector.

**Testable consequence.**

Offline against the implemented `anti_relapse.check`, no new occurrences and no provider calls. Construct two candidates with identical verdict vectors on a stub battery but distinct declared `dependence` structure (parallel vs priority wiring, exactly FW5's enumerated instance at L1402 — the arithmetic is already checked in FW5, so no new mathematics is needed); refute the first; submit the second. It is blocked. That is a FW5-certified false identification produced by a mechanism whose failure mode is silent non-entry.

**Proposed change.**

Demote stage 3 from a block to a flag: log the battery equivalence, Spawn a discrimination problem ("does this candidate differ from the refuted prior in any respect the active battery does not test?"), withhold criticism budget, and block only on stage 1 (exact id equality, which is a true identity). If a block is retained, require as a precondition that the active battery contain at least one commitment testing the structural respect in which the two candidates could differ — a condition the current schema cannot state, which is itself the finding.

**Confidence.**

0.7

**Refuter verdict.** stands: false, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

FW5 L1208-1224, L1402 and L144 are quoted accurately. The finding fails on the spec side.

(1) Stage 3 is not reached by verdict-vector equality alone. §3 L192 makes stage 2 the *trigger*: 'embedding nearest-neighbor against the refuted index within `NEAR_DUP_EPS` ⇒ run stage 3 against that prior.' The finding's constructed counterexample — two candidates with identical verdict vectors but distinct declared dependence structure (parallel vs priority wiring) — is blocked only if it is *also* an embedding near-duplicate of the refuted prior. The finding repairs this hole with repo evidence ('stage 2 is declared absent and fails open (:262), so in this repository the whole burden of stage 2+3 falls on the verdict vector'), but that is the P1 implementation's declared divergence, not spec v1.3. The axis is the spec.

(2) The block is not the unrecoverable non-entry the finding describes. By stage 3's own hypothesis the candidate is ≈_B-equivalent to a prior that *is* registered, *is* a target, and has every N1 exit (§5 L233). §3 L193 admits outright on a warrant against the refuter. FW5 L659 expressly licenses this shape: 'The thinker can remove a rejected conjecture from its current working use while retaining its occurrence for comparison or later criticism... Availability as a current target requires some representation of that target, not an append-only history of every earlier thought.'

(3) The projection theorem is not violated because stage 3 makes no accounting claim. L1218 says 'no function of P(M) alone agrees with **the accounting predicate**'; stage 3 decides budget-spend, not Account(E). L1224 is explicit that the theorem 'identifies missing information in a projection' rather than forbidding its use. §0 L33 and §17 L582 keep ≈_B out of adjudication and declare its judgment-ladenness.

(4) The counterexample needs a degenerate battery. §6 L249 makes `crit` real via the skeleton discipline ('each forbidden case compiles to a commitment'), and §6 L261's `µ_struct` requires role-level substitution — 'swap the mechanism, the motive, the causal link, the scope — not merely reword.' A 'stub battery' on which parallel and priority wiring are verdict-identical is precisely the battery §10 exists to forbid.

What survives is smaller and better placed: §6 L259's gloss 'a rename is the same explanation' is a content-identity claim standing on verdict equivalence, which does sit in tension with FW5 L144.

**Refuter — Corrected finding.**

The tension is in §6's ≈_B gloss, not in the anti-relapse gate. §6 L259's 'a rename is the same explanation' asserts content identity on the strength of a verdict projection, which FW5 L144 denies ('Contents are not identified merely because they have the same truth value or final output'). Recommend: restate ≈_B as an explicitly declared, attackable surrogate for explanation identity (as §7 L303 already does for B₀-for-B), and add to §17 that a ≈_B judgement inherits the projection limit of FW5 L1208-1222. The stage-3 block itself is defensible: it is gated behind stage 2's embedding trigger, carries the §3 L193 escape, and leaves a registered ≈_B-equivalent representative in A with all N1 exits (FW5 L659).

### EC-5

**Finding id.**

EC-5

**FW5 claim.**

FW5 L55: "An idea may be entertained without first being justified. Its generation neither proves it nor obliges a thinker to use it. Conjecture precedes criticism in the sense that a criticism has a target… A criticism is itself conjectural." FW5 L65: "No inquiry must first complete a proof of the legitimacy of all its methods. Present methods can be used provisionally while particular difficulties in them are examined." FW5 L676 (K3): an established ¬O yields ¬(T∧B∧I) and "does not yield ¬T without additional premises about B and I."

**Spec mechanism.**

§3 L189-195, stage 3: block "**unless** the candidate carries a warrant against that prior's refuter"; L195 "Blocking occurs **only** for relapse onto refuted-equivalents. Near-duplicates of *accepted* artifacts are never blocked… (Blocking non-refuted content would be a diversity gate adjudicating — forbidden by §0.)"

**Verdict.**

hinders

**Argument.**

The escape hatch has the right target — since ν asserts the test is sound and relevant, attacking ν is close to attacking B and I, which is where K3 says the fault may lie. What is wrong is the order. The gate requires the criticism of the refuter to be in hand at the moment of registration, so a re-proposal whose author suspects the earlier refutation was wrong but cannot yet say why is refused entry; and because every N1 exit path (L233: new warranted attack, reinstatement, attack on ν, attack on a standard) presupposes registration, an unregistered content has no exits at all. N1 is a guarantee about artifacts, and the gate operates one step upstream of artifacthood, which is exactly where N1 cannot reach. The spec's own reasoning at L195 also generalises against it: blocking non-refuted content would be a diversity gate adjudicating — but under K3 the prior refutation established only ¬(T∧B∧I), so blocking T alone is a gate adjudicating the disjunction. Note the spec's D1 gate ("No problem, no conjecture", L175) is FW5-compatible, because FW5 also makes criticism target-dependent; this gate is not, because it makes re-entertaining conditional on a completed counter-criticism.

**Repository evidence.**

/home/user/miniReason/PURPOSE.md:11 and AGENTS.md:11 make prose conjectures and criticisms legitimate "even when a formal translation fails" and forbid making executable success the definition of bearing — the same principle applied at the door. /home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md:681 shows the implemented interface offers exactly one way past the gate: `candidate_warrant_targets: frozenset[str]` — a set of completed warrant targets. There is no representation for "this is questioned but not yet refuted", so provisional re-entertaining is not expressible.

**Testable consequence.**

Offline against the implemented `anti_relapse.check`. Submit a candidate whose verdict vector matches a refuted prior, accompanied by an artifact that questions the refuter's ν without carrying a warrant against it (e.g. "the ≈_{B₀} surrogate in this ν looks inadequate; I cannot yet show it"). It is blocked, because `candidate_warrant_targets` is empty. That establishes the ordering defect with no new occurrences. Whether the blocked contents would have been worth anything needs live cycles.

**Proposed change.**

Admit on declared intent rather than on completed criticism: register the candidate together with an auto-Spawned audit-the-critic problem naming the specific ν, and withhold criticism budget from the candidate until that problem is addressed. This preserves anti-relapse's actual purpose (do not spend the loop re-refuting the same thing) without making entertainment conditional on justification, and it uses machinery §3 already has (the audit-the-critic trigger, L183). Add the K3 wording to §3's rationale so the asymmetry with L195 is visible.

**Confidence.**

0.75

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

(1) The bar the finding objects to does not exist. §3 L193's escape is 'the candidate carries a warrant against that prior's refuter.' §1 L99 makes `argumentative` a first-class warrant type, §1 L115 makes both types merely 'contentful (packaged in artifacts)', and the rubric-verdict guard (§3 L197-204) applies only to *rubric-derived* warrants. So the finding's own test-case sentence — 'the ≈_{B₀} surrogate in this ν looks inadequate; I cannot yet show it' — is itself a registrable argumentative warrant. Nothing in the spec requires it to be certified, completed, or to survive anything; it registers and becomes attackable in turn. The escape is an encoding formality, not an epistemic ordering requirement, so FW5 L55's 'an idea may be entertained without first being justified' and 'a criticism is itself conjectural' are satisfied, not violated.

(2) FW5 misread on exclusion. The finding says 'an unregistered content has no exits at all.' But the block fires only where the candidate is ≈_B-equivalent to a *registered, refuted* prior — a representative of that content is in A with every N1 exit (§5 L233). FW5 L659 expressly licenses this: removing a rejected conjecture from current working use while retaining its occurrence as a target is the described capacity, not a violation of it. FW5 L65's 'present methods can be used provisionally' is about not requiring a prior legitimation proof of one's methods; it says nothing about re-registering refuted-equivalents.

(3) The K3 argument is a non sequitur. Blocking assigns no status and generates no warrant; §0 L33 and §3 L195 keep it out of adjudication entirely, and the near-miss is logged as a capture diagnostic. 'A gate adjudicating the disjunction' mistakes a registration decision for a label. Worse, the finding's own remedy for K3 — go after B and I — is exactly the §3 L193 escape it complains about, and exactly the mechanism EC-7 praises; EC-5 and EC-7 cannot both be right in the terms each is stated.

(4) The repo evidence is about the implementation. `candidate_warrant_targets: frozenset[str]` (engine :681) is the P1 interface; the spec's clause is prose. What it does reveal is a genuine but much smaller point, below.

**Refuter — Corrected finding.**

§3 L193's escape clause is under-specified in one respect: it names a warrant against 'that prior's refuter', while §1 L107's closure makes an attacker of the refuter's `validity_node` an attacker of the refuter. The implemented `anti_relapse.check(candidate_warrant_targets, refuters, …)` compares ids against refuters only, so an attack aimed at the ν — the K3-correct target, where B and I live — may not open the gate. Recommend one clarifying sentence in §3: a warrant against the refuter's ν counts as a warrant against the refuter for gate purposes, by the §1 L107 closure. The broader ordering objection does not stand: an argumentative warrant is uncertified and conjectural (§1 L99/L115), so the gate never requires a completed counter-criticism, and FW5 L659 licenses withholding a refuted-equivalent from working use while its registered representative retains every N1 exit.

### EC-6

**Finding id.**

EC-6

**FW5 claim.**

FW5 L63: "A problem, value, standard, observation model, interpretation, inferential practice, attention policy, attribution boundary, or conjecture-generating restriction can itself become a problem. **A result of that inquiry must be able to affect the operative target. Scrutiny that can never change anything is not the recursive capacity described here.**" FW5 L140: "The question contract is not immune. It can be criticized and replaced." FW5 L1272 (retained core): "conjecture without prior justification, criticism as itself conjectural, fallible action, recursive scrutiny with operative return".

**Spec mechanism.**

§5 L233 (N1): "every status admits an exit… No artifact — rule-artifacts, standards, school policies, user rulings included — is ever marked final."; §3 L173 (Refl): "rule-artifacts, demarcation criterion, adjudication semantics, standards, guard procedures, and school-policy artifacts are registered artifacts in `A`, attackable"; §1 L107-108 the two closures.

**Verdict.**

helps

**Argument.**

FW5 L63 makes two demands and gives no construction for either. Refl satisfies the first structurally: the adjudication semantics, the demarcation criterion and the guard procedures are themselves artifacts in A, so the assessment apparatus is a legitimate target — which is FW5 L140's "the question contract is not immune" made mechanical rather than exhortatory. The case-law closure satisfies the second without a special status rule: refuting a standard attacks every ν citing it, every warrant under it falls, and its targets return, all inside pass 1. That is a working instance of scrutiny that can change something, and it is more than FW5 supplies. The qualification is what the change reaches. §11.5 L461 keeps the refuted-region atlas out of packs entirely — "negative conditioning primes the very content it bans… Enforce tabu at the door, not in the prompt" — so the accumulated record of what has been refuted and why never reaches γ as content. FW5 L1052 requires a path from a subsidiary result to "the parent's relevant use, method, interpretation, or attention state", and warns that "a decorative transcript channel permanently disconnected from the operative state does not satisfy the condition". Attention is on FW5's list, so §11.5 is not a violation — but it does mean the return is to scheduling and admission, never to the generator's represented content, and FW5 L628 requires the objection to be on an active dependency route of the response occurrence, which a never-rendered atlas entry cannot be.

**Repository evidence.**

/home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md:232 implements and tests the closure with the strong assertion "no status rule outside `att`/`dep` ran"; :218 records that the pass-2 rule and the `suspended_unsupported` label are themselves "registered as a Refl rule-artifact at root creation, attackable under N1" — the recursion applied to its own bookkeeping. :371 registers self-criticism (`withdraws`) as "a self-directed argumentative warrant… legitimate under N1". Against the return: :910 records that §11's negative atlas is out of scope entirely at P0/P1, so the repo cannot yet test either side of the L1052 question.

**Testable consequence.**

For the helping half: offline, refute a standard artifact and assert that every target of every warrant citing it returns to `accepted` in pass 1 with no rule outside att/dep — already the pinned test at engine :232. For the qualification: a live discriminating test needs new occurrences — run one chain with refutation content rendered into the conjecturer's pack and one with only the gate, and check whether a later conjecture is content-sensitive to the refutation (FW5 L630's contrast triple: content change, content-preserving recoding, carrier disturbance). That cannot be settled on occurrence-01.

**Proposed change.**

Keep N1, Refl and both closures unchanged; they are the spec's strongest FW5-aligned mechanisms and should survive any trimming. Amend §11.5's rationale to state that withholding the atlas from packs is a conditioning hypothesis about the generator, not an epistemic principle, and to name the FW5 L1052 return-relevance requirement it must eventually answer; make the withholding a configured policy with a logged alternative arm rather than a fixed rule, so the claim can be tested instead of assumed.

**Confidence.**

0.8

**Refuter verdict.** stands: true, misreads_fw5: true, misreads_spec: false

**Refuter — Rebuttal.**

The 'helps' verdict is right and well supported: §3 L173 (Refl) does put adjudication semantics, standards and guard procedures into A as attackable artifacts, §1 L108's case-law closure does deliver FW5 L63's 'result... must be able to affect the operative target' inside pass 1, and the engine's :232 test with its 'no status rule outside `att`/`dep` ran' assertion is real. The qualification, however, contains a FW5 misreading and one spec omission.

(1) FW5 misread. The finding closes with 'FW5 L628 requires the objection to be on an active dependency route of the response occurrence, which a never-rendered atlas entry cannot be.' L628 defines the reason-use witness for a *response occurrence* (§'Reason use is causal organization'); the return condition is L1050-1052 in a different construction ('Target closure and return'). L1052's own list of admissible return targets is 'the parent's relevant use, method, interpretation, or **attention state**' — the finding quotes this and concedes §11.5 is not a violation, then re-imports L628 to reinstate the complaint. That import is not licensed; the two conditions have different relata.

(2) Spec omission. §11.4 L452 does return refutation-derived content to the generator's pack — 'add complement directives to the pack ("produce the attempt these summaries make least likely")' — so the claim that the return is 'never to the generator's represented content' is not quite right. And the gate's block is itself an operative effect on the parent's subsequent activity, which is what L1050 asks for.

Neither point damages the verdict. The proposed change — mark §11.5's withholding as a conditioning hypothesis with a logged alternative arm — is cheap and correct, and the finding's own note that engine :910 puts §11 out of scope at P0/P1 is accurate, so the qualification is honestly flagged as untestable on occurrence-01.

**Refuter — Corrected finding.**

### EC-7

**Finding id.**

EC-7

**FW5 claim.**

FW5 L663-676 (K3): from T∧B∧I ⇒ O and an established ¬O, "an established ¬O yields ¬(T∧B∧I). **It does not yield ¬T without additional premises about B and I.** Here B can include auxiliaries and I the observation interpretation… It states exactly what the test contradicts and where further criticism can matter." FW5 L661: "A passing execution cannot make the program's specification, the model of the experiment, or the claimed relevance immune to prose criticism." FW5 L622: "A mere adverse signal is not made into a criticism by giving it a negative label."

**Spec mechanism.**

§1 L103 `validity_node: ν(κ): asserts the test is sound & relevant`; L107 closure rule; L115 "a bare verdict is never an edge"; §5 L233 "demonstrative refutation reopens via attack on its `validity_node`"; §7 L307 the four-clause hv-floor ν (kernel fairness, k sufficiency, ≈_{B₀} adequacy, B₀-for-B adequacy).

**Verdict.**

helps

**Argument.**

This is the spec's best piece of FW5 engineering. K3 says a failed test contradicts a conjunction, and the spec's ν is exactly where the non-T conjuncts live and are made separately attackable: B is the auxiliaries (the variator kernel, k, the surrogate battery B₀) and I is the soundness-and-relevance interpretation. §7 L307 is an unusually honest instance — it enumerates in advance the four auxiliary claims a reopening attack would have to reach, and names the canonical one ("the counted survivors are ≈-equivalent under a fairer surrogate; ŝ is inflated"). L115's rule that a bare verdict is never an edge is the same rule as FW5 L622's refusal to let an adverse signal become a criticism by labelling. The residue is that grounded semantics resolves the K3 disjunction by default and in one direction: an unattacked ν is accepted, so the warrant stands, so T is refuted; and the only automatic consequence, "failed verdict ⇒ successor problem" (L179), already presupposes that T is the faulty conjunct and needs a successor. Nothing in the spec ever proposes that B or I might be at fault unless a human or a critic role happens to think of it.

**Repository evidence.**

/home/user/miniReason/docs/EXPERIMENT_METHOD.md:63 states the FW5 rule the ν implements: "A verifier's success does not immunize the specification, interpretation or relevance of its checks (FW5 'Evidence receipts without false certainty')." /home/user/miniReason/docs/mini/ERRATA.md C4 records that Mini had no eval, no budget and no verdict, so "attack surface is a metaphor here rather than a count" — the ν architecture is what the repo lacked and is adopting. /home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md:185 and :237 build and test the closure (`test_validity_node_closure_disables_every_carrier`).

**Testable consequence.**

Offline. Over any recorded set of demonstrative refutations in the engine's log, count how many were followed by (a) a successor problem on T and (b) any attack registered against the ν. If (b) is near zero while (a) tracks (a) one-for-one, the K3 disjunction is being charged to T by default — which is also the spec's own capture diagnostic at §11.3 L442 ("if no test is ever attacked, D3 has died in practice while remaining true on paper") pointed at itself. Needs no new occurrences once P1 logs exist; the diagnostic is already specified.

**Proposed change.**

Add an eighth Spawn trigger, symmetric with the existing successor trigger: failed demonstrative verdict ⇒ audit-the-auxiliaries problem naming the ν's own declared clauses as candidate targets. It reuses existing machinery, costs one line in §3's trigger list, and makes K3's disjunction visible rather than silently assigned. Also require every demonstrative ν to enumerate its auxiliary claims the way §7 L307 already does, so the audit problem has something to point at; a ν whose whole content is "the test is sound & relevant" gives an attacker nothing to grip.

**Confidence.**

0.75

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

The 'helps' verdict is right and the K3 mapping is accurate: §1 L103's ν is where FW5's B and I live, §7 L307 enumerates four auxiliary claims in advance, and §1 L115's 'a bare verdict is never an edge' is the same rule as FW5 L622's 'A mere adverse signal is not made into a criticism by giving it a negative label.' EXPERIMENT_METHOD.md:63 checks out verbatim.

The residue claim is materially overstated. 'Nothing in the spec ever proposes that B or I might be at fault unless a human or a critic role happens to think of it' is false three times over: §3 L183's audit-the-critic Spawn trigger fires on 'judge-ensemble disagreement, rubric-guard failure streaks, calibration error rate > JUDGE_ERR_MAX, paraphrase-flip audit hits (§10), and adjudication-ritual flags (§11.3)' — all of these are auxiliary-and-interpretation faults; §10 L389 routes audit outputs as 'ordinary demonstrative warrants (`eval:program`) against the relevant ν nodes or standards', which is an automatic, warranted attack on B/I; and §11.3's validity-node-attack-rate metric feeds the §11.4 'Adjudication ritual ⇒ ... audit-the-critic Spawn' rule, so an era in which no ν is ever attacked mechanically produces a B/I audit problem. The finding cites §11.3 L442 for its own diagnostic while treating it as reporting-only; §11.4 makes it a trigger.

What remains true is narrower: the existing mechanism is windowed and statistical, whereas 'failed verdict ⇒ successor problem' (§3 L179) is per-verdict and unconditionally charges T. The proposed eighth trigger is therefore a refinement of granularity, not a missing capability, and the companion recommendation — that every demonstrative ν enumerate its auxiliary claims the way §7 L307 does — is the more load-bearing half and is well motivated by K3.

**Refuter — Corrected finding.**

### EC-8

**Finding id.**

EC-8

**FW5 claim.**

FW5 L791-797 (P): Repair_{O,P}(ξ,ξ';Δ) ⟺ ∃o∈O[¬o(ξ)∧o(ξ')] ∧ ∀r∈P[r(ξ)⇒r(ξ')] ∧ ProducedBy(Δ,ξ,ξ';O). FW5 L802: "It states that a particular defect was repaired, that declared protected achievements were not lost, and that the contribution produced the change. **Losses outside P must be exposed.**" FW5 L808: "A system that acquires an account of a trivial feature while destroying its only account of the main difficulty has acquired something. It has not thereby improved the whole situation." FW5 L814: an epistemic obligation "requires a correct structural account to be deployable… An endorsement count or an ungrounded satisfaction report is not such an obligation."

**Spec mechanism.**

No counterpart. The nearest mechanisms are §3 L177-186 Spawn triggers, §4 L226 `suspended_unsupported`, §0 L32 "Nothing is deleted", and §11.7 L467-469 Pareto retention.

**Verdict.**

absent-in-spec

**Argument.**

The spec's entire error-correction vocabulary is status change plus problem generation. FW5's is a two-sided comparison of situations: a failed obligation now holds, every *protected* obligation that held still holds, and the contribution actually produced the change. The spec records no protected set, so it cannot detect FW5 L808's case — a successor that repairs a small defect while destroying the only account of the main difficulty registers as a normal successor Spawn plus a refutation, i.e. as progress. §0's "nothing is deleted" preserves the artifact, not the achievement: the lost account stays in the log labelled `refuted` or `suspended_unsupported`, and nothing asks whether the loss was exposed. Pareto retention is the closest structure and is explicitly not this — it ranks over HV, reach and coverage, which FW5 L851 rules out as automatic warrants ("No quantity of endorsements, surviving tests, repeated observations, or partitioned features enters (G), (P), or (EK) as an automatic warrant"), and it governs funding, not preserved achievements. The absence matters most for the repo's stated research question, which is a repair question, not a status question.

**Repository evidence.**

The repo has already written the FW5 side and assigned it to a human: /home/user/miniReason/docs/RESEARCH_AGENDA.md:81 "The protected condition is that the new organization still supports the declared earlier expressions or uses of C0 when those old conditions are reinstated… Record which protected uses were actually witnessed; an untested preservation promise is not an observed success." /home/user/miniReason/experiments/diagnostics/H005-open-prose-commitments/PROTOCOL.md:62 makes "what useful commitments were lost" part of the unit of argument and :64 rules out surrogates ("Parser success, agreement with root, adoption of a standard answer, more objections… do not establish repair"). /home/user/miniReason/docs/SEMANTIC_GUIDE.md:28 states (P) in full as a claim-ladder row. None of this has a mechanism; PROTOCOL.md:62 assigns it to root alone.

**Testable consequence.**

Offline on existing evidence, to establish the absence: take any cycle-1 → cycle-2 transition in occurrence-01 and ask whether the recorded graph can distinguish a change that repaired a defect while preserving the prior account's live uses from one that repaired it by dropping them. It cannot — there is no field naming a protected obligation, so the distinction is not representable, independently of what the models did. Showing that the absence *costs* something requires cycle-2/cycle-3 records where a later node drops a commitment an earlier node relied on; those exist in the plan but are not yet run.

**Proposed change.**

To the spec: add `interface.protects: [<commitment-id>]` on a successor artifact, plus a standard program commitment `protected-preserved` that re-runs each named prior commitment against the successor; its `fail` produces an ordinary demonstrative warrant with a ν asserting the re-run was faithful. This stays inside §0's invariant — it is a budgeted commitment, not a measure, so it acts through `att` exactly as §7's `hv-floor` does — and it gives (P)'s second conjunct and L802's exposure rule a mechanism. Do not attempt ProducedBy: FW5 L800 makes it a construction account, not temporal succession, and it should remain with root. To the programme: record the protected set before each H005 cycle rather than reconstructing it in review, per FW5 L787 ("Their definitions… must not shift inside its assessment").

**Confidence.**

0.85

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

The absence is verified: grepping harness-spec-v1.3.md for protect/preserve/loss/repair returns only well-formedness preservation, lossy-summary safety, and `RETRY_MAX` schema-repair — nothing resembling a protected-obligation set or a two-sided situation comparison. FW5 L787-808 and L814 are quoted accurately, and the repo citations check out (RESEARCH_AGENDA.md:81 verbatim; PROTOCOL.md:62 'what useful commitments were lost' and :64's surrogate exclusions).

The strongest counter is that the spec does not claim otherwise. §17 L578 states plainly: 'Guarantees faithful bookkeeping (statuses, reinstatement, no relapse, replayable trace). Does not manufacture good conjectures.' And FW5 L1274 declines to make implementation choices conditions of the class: 'A rotating scheduler, JSON interface, token allowance, or storage policy is not a condition of this class.' So the absence is not a violation — which is exactly why the finding's verdict label 'absent-in-spec' rather than 'hinders' is the right one, and the finding does not overclaim. Two corrections at the margin, neither fatal: (a) the aside that Pareto retention ranks over quantities 'which FW5 L851 rules out as automatic warrants' implies a violation that §11.7 L469 pre-empts ('Never a status; an artifact off the frontier is merely unfunded, not demoted'); (b) the proposed `protected-preserved` program commitment would be nominal exactly where PROTOCOL.md:62 needs it — the FCL-1 reduction's predicate checks only that a named record exists and is well-formed, and the engine design itself concedes 'Its *substantive* obligation is not machine-checkable before §10', so in informal domains the re-run would certify form, not preserved achievement. The finding's own restraint about ProducedBy (FW5 L800: 'not satisfied by temporal succession alone') is correctly applied and should extend to this clause too.

**Refuter — Corrected finding.**

---

## Axis 4 — measures-and-capture

**Critic's overall assessment.**

On this axis the spec hinders more than it helps, but not uniformly, and the pattern is legible: wherever the spec records a *structure* it converges with FW5, and wherever it collapses that structure to a number it collides with FW5's explicit prohibitions. The convergences are real and worth keeping — `crit` reconstructs something close to FW5 non-circular dependence as a well-formedness condition rather than a rubric item; Pareto retention (§11.7) is a principled refusal of the common currency FW5 forbids at L804, and is the one measure whose form FW5 licenses; §11.3's stated limit ("these detect stalled dynamics, not wrong-but-stable ones") is FW5's own epistemic ceiling honestly declared; and §11.8's λ experiment executes FW5's fix-the-contract-before-evidence discipline (L787, L1101, L1129) better than anything else in either document. The collisions are equally clear. `HV_B(a) = 1 − s(a)` collapses FW5's Pres(F) — a set, whose only licensed inference is a possibly non-strict containment (H) — into a scalar over an undeclared, model-version-dependent variation family, which is exactly the "numerical warrant" L381 refuses; `hv-floor` then relocates a removed acceptance gate into a commitment whose k≈8 sample produces the terminal label `refuted`, which is FW5 L851's count-as-automatic-warrant with an extra mechanism hop, and the spec's own residue ("HV at k≈8 is a spot-check, not a measurement") makes the conflation with demonstrative refutation worse rather than better; reach-as-cross-evaluation-hit is endpoint agreement (L232, L332) with "raises standing" attached, omitting FW5's constitutive requirement of a stated anchor; `mod` makes modifiability constitutive of explanation-hood, which FW5 never asserts, and makes it a property of a sampler; λ counts verdict *kinds*, which is host bookkeeping of the sort L640 names as not constituting the relation it labels. Underneath all of them sits `≈_B`, extensional equivalence over a battery, at the exact point where FW5's projection theorem (L1208–1224, enumerated at L1402) proves no function of the endpoint projection can agree with the accounting predicate — which makes anti-relapse's verdict-vector blocking the most serious single defect, since it can refuse registration to a structurally distinct explanation. The repo has already, independently and without saying so, performed several of the repairs this analysis recommends — `mod -> bool | None` (unknown, never False), integer-count Pareto axes at P1, and the wholesale exclusion of HV, reach, λ and capture control from the built engine — which is evidence that the spec's measure layer is not load-bearing for the programme and can be kept, as `AGENTS.md:11` has it, strictly as a mechanism guide: retain Pareto's shape, `crit`'s structural placement, §11.3's honesty and §11.8's design; drop or demote to attention every scalar that currently reaches a status.

**Refuter's axis summary.**

Verified every FW5 citation at source and every spec mechanism in context. Three findings survive in some form (MC-05, MC-08, and the µ-declaration half of MC-01); five do not stand as written. The dominant failure mode across the refuted findings is a systematic omission of two governing spec clauses — §0 L37 and §4 L229 ("Measures... MUST NOT appear as inputs to label computation... they act upstream — via Spawn, via commitments whose fail verdicts generate warranted attacks, or via attention") and §5 N1 ("no absorbing status; demonstrative refutation reopens via attack on its validity_node") — combined with two truncated FW5 quotations. The truncations are load-bearing: (a) L851 continues "Mathematical counts can appear inside an explanation... They are not outlawed as information", and L1302 adds "This does not prohibit mathematics about counts", so FW5 forbids a count *serving as warrant*, not the computation or logging of a count — this defeats the "scalar = numerical warrant" prong of MC-01 and the "reach-count orders explanations" prong of MC-04; (b) L232 continues "A table that really encodes an entire relevant organization under its interventions is a different case... Anti-behaviorism is a distinction about organization, not a ban on a data structure", which blunts the endpoint-agreement charge against ≈_B and against reach, since a verdict-vector over a battery of commitments is a table under interventions, not a table of observed answers. The single most consequential error is MC-02's: it calls `refuted` a "terminal label" and a "terminal state" while its own spec_mechanism quotes the reinstatement clause, and §5 N1 plus the P2 acceptance test ("lands `refuted`, reinstates via ν-attack") contradict terminality outright; with terminality gone, both the K3 (L663-676) and L688 arguments collapse — indeed the ν(i)-(iv) clauses *are* the B and I of K3 made attackable, and L688's inability-to-evaluate case is exactly what `overrun` handles. MC-02 also inverts FW5 L622: "A mere adverse signal is not made into a criticism by giving it a negative label. It can become grounds for a criticism when an organization represents how it bears on a target" — the contentful critic artifact with trace and ν is that organization, so the v1.1 gate→criterion relocation is precisely the move FW5 licenses, not a smuggle. MC-03's `mod` half fails on a checkable fact: `active(a)` occurs once in the entire spec (L246) and gates nothing; the "fails demarcation" consequence at L249 and its only enforcement (`skeleton-wf`, L366, "passes iff the skeleton parses AND forbidden ≠ ∅") attach to the `crit` conjunct alone, and FW5 L210 — the critic's own lead citation — requires an admitted contrast "for which the answer profile changes", which is what `mod` formalizes, so "FW5 nowhere makes variability constitutive" contradicts the quoted line. MC-04 additionally misses §10.5 L393's seal (holdout bytes "excluded from all packs by the deterministic renderer"), which supplies informational isolation rather than the mere timestamp-provenance the finding attacks. MC-07's metric half treats attackability of evidence as proof of closed-loopness, which would convict FW5's own fallibilism (L45-51) of the same defect. What genuinely survives: µ's identity is not in the commitment content though k, HV_MIN and B₀ are (L301), so the variation family is frozen only post hoc by replay and never declared before assessment, against FW5 L358/L1300's fixed-V requirement; HV_MIN is a bare config constant (L541 "tune") whose decision margin carries no account, with ν(ii) asserting sufficiency *at* a margin it does not justify; PARETO_AXES is likewise a config knob (L555) and not a Refl artifact, which is a real gap against FW5 L605's "potential criticism targets"; and anti-relapse stage 3 (L193) is the one place a measures-layer surrogate produces an outcome with no attack surface at all — a blocked candidate registers nothing, so there is no ν and no reinstatement path, which is the sharpest and best-supported claim in the set.

### MC-01

**Finding id.**

MC-01

**FW5 claim.**

FW5 L358-366 defines Pres(F) = {v∈V : ∀f∈F, Account(E_v,f)} over a *fixed* organization, interpretation and variation family V; L381: "'Hard to vary' is therefore an articulated pattern of constrained changes, relative to an explanatory job. It is not the requirement that every detail of a complete theory be individually indispensable. Nor is it a numerical warrant." L379: "Counting jobs is not a replacement for the missing comparison." L1300: "The valid containment result holds when the organization, interpretation, and variation family stay fixed while preservation requirements are added. It may be non-strict."

**Spec mechanism.**

§6 L251-259: "s(a) = Pr[ a' passes B(a) ∧ a' ≉_B a ]", "HV_B(a) = 1 - s(a)", "k ∈ [5,10] local… Estimable to (ε,δ) by Hoeffding. Log the estimate + k; it is a spot-check". Variator kernel µ(·|a) is an LLM role (§9 L332-346); µ_struct at L261-263.

**Verdict.**

hinders (partly helps)

**Argument.**

The *set* HV ranges over is FW5's object: {a' : a' passes B(a)} is Pres(F) with F = the active battery. That much is a real convergence — the spec is computing survivors-under-constrained-change, which is what Deutsch's criterion is about, and the spec's own µ_struct correction (L261 "Rewording-only µ measures phrasing rigidity and is declared insufficient for D5"; L265 "Claim-level HV alone measures phrasing rigidity only") independently reconstructs FW5 L381's splitting-features objection. Two things then break it. First, the collapse |Pres| → [0,1] is precisely the "numerical warrant" FW5 refuses; FW5's only licensed inference is the containment (H) between job families, which a scalar cannot express (a non-strict containment and a strict one give the same number). Second, and worse, FW5 requires V to be *fixed* — declared as part of the claim. µ is an LLM sampling distribution: it is not declared, it is not stable across endpoints or model versions, and it is not equivariant under the structure-preserving recodings FW5 L1202-1206 requires verdicts to be preserved under. So HV_B measures the variator's imagination jointly with the artifact's rigidity, and the two are not separable from the number. The spec half-concedes this by parking µ-kernel fairness in the validity node (L309) — visible and attackable, but not eliminated (L580).

**Repository evidence.**

The repo has already refused the scalar: `AGENTS.md:15` "No random configuration mutation, automatic evolutionary optimisation or scalar progress meter"; `docs/SEMANTIC_GUIDE.md:57` "Reach or edit-survival counts supply no numerical warrant"; `docs/reviews/FW5-research-plan-decision.md:15` records the preservation lemma as fixing "organization, interpretation and variation family" and treats ECS 2.0's intrinsic-variation repair as a *successor* hypothesis, not an FW5 conclusion. `docs/design/engine-design-of-record-2026-09-14.md:910` excludes "no HV estimator, no µ_struct, no hv-floor, no variator kernel" from the built engine — the measure is unimplemented here, so nothing in the repo yet depends on it.

**Testable consequence.**

Run hv_estimator twice on one frozen artifact with two different variator endpoints (or two seeds) at the same k, same B₀. If HV_B moves by more than the declared (ε,δ) band, the quantity is variator-relative and cannot be read as a property of the artifact's organization; the (H) containment it is supposed to proxy is then untestable from the number. This needs new occurrences (no variator exists in the repo), but a cheap offline proxy already exists: the skew-matrix fixture at `experiments/diagnostics/fw5-account-skew-matrix/check.py`, where the Leibniz expansion and the transpose/parity proof have identical preservation behaviour under the frozen contrasts (remove skew-symmetry, remove oddness) and must therefore receive identical HV — any variator that separates them is measuring prose, not organization.

**Proposed change.**

Demote HV_B to a logged attention statistic and make the *recorded* object the survivor set under a variation family V declared before evidence, with (H)-style containments between job families reported as containments (⊆, possibly non-strict), never as a difference of numbers. Where the spec says "Estimable to (ε,δ) by Hoeffding", add that the estimand is defined only relative to a declared µ, and that µ must be pinned in the commitment content alongside k and B₀ (the spec already content-addresses k, HV_MIN and B₀ at L301 — extend that to µ's identity, including endpoint and model version).

**Confidence.**

0.85

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

Two prongs; the first fails. FW5 L381's "Nor is it a numerical warrant" sits in a sentence defining hard-to-vary as "an articulated pattern of constrained changes" — it denies that a number *warrants*, not that a number may be computed. L851 says so explicitly in the clause the finding truncates: "Mathematical counts can appear inside an explanation of a particular counting problem or a physical resource condition. They are not outlawed as information"; L1302 repeats "This does not prohibit mathematics about counts or numerical accounting of resources." So the collapse |Pres|→[0,1] is not per se what FW5 refuses. The finding then never engages the clause that decides the question for §6: §0 L37 and §4 L229 — measures "MUST NOT appear as inputs to label computation (§4)" — and §6's own L259 "Log the estimate + k; it is a spot-check, re-estimable later." Within §6 the number's only consequences are a remove-arbitrariness Spawn (§3 L181) and Pareto focus (attention). The finding's own proposed_change ("Demote HV_B to a logged attention statistic") is therefore a restatement of what §0/§6 already say. The "(H) containment cannot be expressed by a scalar" point is true but idle: §6 nowhere claims HV_B proves (H). The equivariance appeal also overstates — L1202 is a theorem that (E),(G),(P),(EK) are preserved under structure-preserving bijections, not a requirement imposed on harness verdicts. The second prong survives: FW5 L358 fixes "an organization, interpretation, variation family V" and L1300 restricts the containment to "when the organization, interpretation, and variation family stay fixed"; §7 L301 content-addresses k, HV_MIN and B₀ but not µ, and §7 L303's replay-determinism freezes a draw *after* it is taken, which is not pre-declaration.

**Refuter — Corrected finding.**

hinders (narrow): §6/§7 estimate hard-to-vary against a variation family µ that is never declared. FW5 L358/L1300 make (H) and Pres(F) meaningful only relative to a *fixed* V; §7 L301 freezes k, HV_MIN and B₀ into the commitment content but omits µ's identity (role endpoint, model version, kernel selection), and L303's logged-raws replay determinism fixes a draw post hoc rather than declaring the family in advance. Two estimates at the same k and B₀ are therefore not comparable as properties of the artifact. Fix: extend the L301 content-addressing to µ's identity. Drop the claim that computing or logging a scalar is itself the numerical warrant FW5 refuses — L851 and L1302 expressly permit counts as information, and §0 L37/§4 L229 keep §6's HV out of label computation.

### MC-02

**Finding id.**

MC-02

**FW5 claim.**

FW5 L851: "No quantity of endorsements, surviving tests, repeated observations, or partitioned features enters (G), (P), or (EK) as an automatic warrant." L849: "There is no further generic predicate defined as 'withstanding criticism well enough to merit preference.'" L1264: "None of (E), (G), (P), (EK), or (U3) depends on an empirical-frequency update or a merit maximization." L688: "The inability to evaluate a proposition is not a falsifying observation of the proposition."

**Spec mechanism.**

§7 Brake 1, L286-316. L288 "HV floor as criterion, never as gate." L304 "ŝ = fraction of edits that pass B₀". L306 "Verdict: pass iff 1 − ŝ ≥ HV_MIN; else fail". L307-309 "V = fail ⇒ the harness registers (Crit) a critic artifact carrying an ordinary demonstrative warrant… a fresh, unattacked critic is in G ⇒ the relation is **refuted** — never `suspended`". Changelog L238: the v1.1 removal of the `HV_MIN` acceptance gate, "floor relocated into connection-problem criteria as `hv-floor`".

**Verdict.**

hinders

**Argument.**

This is the single clearest place a merit ordering is smuggled. The v1.1 changelog is candid that the same threshold was moved rather than dropped: it used to be an acceptance gate; it is now a commitment whose fail produces the terminal label `refuted`. The epistemic fact is unchanged — a configured scalar threshold crossed by a k≈8 sample changes an artifact's status. That is exactly FW5 L851's "quantity of surviving tests… as an automatic warrant". The spec's own residue makes the conflation sharper, not softer: L580 "HV at k≈8 is a spot-check, not a measurement", yet L307 insists the resulting label is `refuted` and "never `suspended`". A statistical spot-check and a demonstrative program refutation therefore land in the same terminal state, which FW5 forbids twice over — K3 (L663-676) says a failed test yields only ¬(T∧B∧I), and L688 says inability to evaluate is not falsification. The `overrun` discipline (L307 "`overrun` packages no warrant; only `fail` does") is right and should have been extended: a sampled shortfall is epistemically nearer to `overrun` than to `fail`. Note the framing move to interrogate: "criterion, never a gate" is a claim about the *mechanism path*, not about whether a number adjudicates. Under FW5 the path is irrelevant — L294 "it does not assign a probability or a score" is a constraint on what the record contains, not on how the score reaches the record.

**Repository evidence.**

`AGENTS.md:15` "Do not let an operational alarm adjudicate content." `docs/EXPERIMENT_METHOD.md:93` "V1.3 §1 explicitly says a containment kill must not mint a warrant" — the spec already holds this discipline for oracle isolation (L80-88) and abandons it for hv-floor. `docs/SEMANTIC_GUIDE.md:24` lists "a successful parser" among things that do not establish Account; the symmetric point (a failed sample does not establish its absence) is `docs/sources/FW5-explanatory-construction.md:634`. The repo's engine declines the mechanism outright: `docs/design/engine-design-of-record-2026-09-14.md:910` "no `hv-floor`".

**Testable consequence.**

Construct two connection artifacts with identical B₀ and identical true survivor structure but ŝ straddling HV_MIN by one edit out of k=8 (the decision margin the validity node ν(ii) already names). One lands `refuted`, one `accepted`. Under FW5 both have the same Pres(F) at the declared grain, so the label difference is produced by the sampler, not by the organization. Testable offline today using the skew-matrix contrast set as B₀ and a hand-enumerated edit family — no provider call needed.

**Proposed change.**

Amend §7 so `hv-floor` fail Spawns the existing **remove-arbitrariness** problem (already a §3 trigger at L181) and registers *no* warrant; if the fail must register, give it a distinct non-terminal label (`suspended_low_hv`) so that a sampled shortfall never occupies the same state as a demonstrative refutation. Alternatively state explicitly, as L307 does not, that reinstatement-by-ν-attack is the *expected* path rather than the exception — but the label conflation remains under that reading, so the Spawn-only version is the FW5-legal one.

**Confidence.**

0.9

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The finding's load-bearing premise is that `refuted` is terminal — "the terminal label `refuted`", "land in the same terminal state". The spec says the opposite in the section the finding does not quote: §5 N1, "every status admits an exit... demonstrative refutation reopens via attack on its `validity_node`... No artifact — rule-artifacts, standards, school policies, user rulings included — is ever marked final"; and §16 P2's acceptance test requires an easy-to-vary relation to "land `refuted`, reinstate via ν-attack, replay byte-for-byte". The finding even quotes the reinstatement clause in its own spec_mechanism and then argues from terminality. With terminality removed, both FW5 arguments collapse. K3 (L663-676) says an established ¬O yields ¬(T∧B∧I), not ¬T — and §7 L307's ν is exactly that decomposition made attackable: (i) kernel fairness and (ii) k-sufficiency are B; (iii) ≈_{B₀} adequacy and (iv) B₀-for-B adequacy are I. The harness implements K3 rather than violating it. L688 ("The inability to evaluate a proposition is not a falsifying observation") is honored, not breached: §7 step 4 routes unobtainability to `overrun`, and L307 closes "`overrun` packages no warrant; only `fail` does" — the finding quotes this approvingly then asks for it to be extended to a case that is not an inability to evaluate (ŝ is obtained; only its precision is at issue). "never `suspended`" is a statement about grounded-semantics mechanics — an unattacked attacker yields refuted, not undecided — with the spec's own gloss attached ("suspension would require the critic itself to be under unresolved attack"), not a claim of finality. The "path is irrelevant" move inverts FW5 L622, which makes the path decisive: "A mere adverse signal is not made into a criticism by giving it a negative label. It can become grounds for a criticism when an organization represents how it bears on a target." The v1.1 relocation supplies exactly that organization — a contentful critic artifact (§1: "a bare verdict is never an edge"), `trace_ref = {k edits, per-edit verdict vectors, ŝ, logged raws}`, and ν — where the v1 gate had none. §0 L37 anticipates this path in terms: measures may influence the graph by "being packaged as budgeted commitments whose `fail` verdicts generate warranted attacks (§7)". L851's prohibition is on a quantity entering (G)/(P)/(EK) "as an automatic warrant"; nothing here is automatic (the warrant is defeasible at ν) and the harness's Dung label is not (G)/(P)/(EK). Finally "merit ordering" is a misdescription: a single defeasible pass/fail criterion on connection problems induces no order over alternatives. The testable consequence also mis-states the spec — passing hv-floor yields no warrant and does not make an artifact `accepted`; `accepted` is the §4 default for the unattacked.

**Refuter — Corrected finding.**

neutral-to-hinders (narrow): the FW5-relevant residue in §7 is not that a number adjudicates — L622's bearing condition is met by the contentful warrant plus ν, and N1 keeps the label revisable — but that HV_MIN is a bare config constant (§15 L541, "tune") whose placement carries no account, while ν(ii) asserts only "`k` sufficiency at the decision margin" and never justifies the margin itself. Under FW5 L849 (no generic predicate of "withstanding criticism well enough") and L1101 (an enabling condition is inadmissible if its only description is "the conditions under which the system succeeds"), the threshold should be registered as a Refl artifact with a stated account of what ŝ ≥ 1−HV_MIN is supposed to mean for the connection claim, and fixed before the evidence window it governs (L787). Retract the terminality, K3 and L688 arguments.

### MC-03

**Finding id.**

MC-03

**FW5 claim.**

FW5 L210 (non-circular dependence): "There is at least one admitted contrast that removes or changes a nonempty block of active organizational commitments, while preserving the other declared boundary conditions, for which the answer profile changes or ceases to be determined in the claimed way." L212: "A contrast family containing only notational variants, or one defined to exclude every change that could matter, does not meet non-circular dependence." L634: "That makes the attribution unresolved; it does not prove either understanding or its absence."

**Spec mechanism.**

§6 L241-249: "crit(a) ⇔ interface.commitments ≠ ∅", "mod(a) ⇔ Pr_{a'~µ(·|a)}[a' ≉_B a] > 0", "active(a) ⇔ crit(a) ∧ mod(a)"; L249 "an artifact that forbids nothing has an empty attack surface and fails demarcation — Deutsch's sense, made structural."

**Verdict.**

helps (crit) / hinders (mod)

**Argument.**

`crit` is the spec's best structural move and is close to something FW5 genuinely asserts: an account whose contrast family excludes every change that could matter fails non-circular dependence (L212), and FW5 non-vacuity requires the baseline to admit a compatible state. Making a nonempty attack surface a well-formedness condition rather than a rubric item is the right shape. The gap is that `crit` is satisfied by a *self-declared* list field, whereas FW5's condition is a property of the anchored target organization under admitted contrasts; the spec knows this (L582 "Skeletons can be gamed by toothless forbidden cases"). `mod` is a different matter. It makes modifiability *constitutive of explanation-hood*: an artifact no LLM variator can perturb into an inequivalent survivor is not `active`, hence fails demarcation. FW5 nowhere makes variability constitutive; hard-to-vary is a property of the pattern of constrained change (L381), and an account maximally constrained by its anchoring is the *best* case under (H), not a non-explanation. Since µ is a sampler, `mod` also makes explanation-hood a property of a configured role, violating the recoding equivariance of L1202-1206. Notably the repo has already performed the FW5 repair for the missing-variator case and should generalise it.

**Repository evidence.**

`docs/design/engine-design-of-record-2026-09-14.md:661` implements `demarcation.mod(artifact, variator_available) -> bool | None  # None when no variator is configured (P1): unknown, never False` — exactly FW5 L634's unresolved-not-absent discipline, made executable. `docs/mini/ERRATA.md:98` records the `crit(a) ⇔ interface.commitments ≠ ∅` form as the one Mini tracks. `docs/sources/deepreason-core-vendor-notes.md:416` flags that a reader expecting demarcation checks to actually run should read the vendor code otherwise. The H005 material makes the `crit` hazard concrete: `material.json` instructs "Do not invent a source, an observation, an earlier event, or a dependency to fill a field" — i.e. a nonempty commitments field is exactly what an agent under field pressure will produce whether or not there is a contrast behind it.

**Testable consequence.**

Offline on existing H005 cycle-1 evidence: compute `crit` over the five `mini_fcl` and `mini_prose` artifacts in `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/`, then hand-check, per artifact, whether any declared commitment names a contrast that would change the answer profile. If `crit` is true for artifacts with no such contrast, `crit` is measuring a field's occupancy, not FW5's non-circular dependence. For `mod`: run any variator twice with different seeds on one artifact; a flip of `active` refutes `mod` as a content property. The matched-arm case already shows the failure class — `commitments_sha256 = e3b0c442…` (empty string) on two nodes would make `crit` false for a carrier reason, and `docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md:26` says reading it at face value "would score an encoding fault as an arm that declined to commit".

**Proposed change.**

Keep `crit` but require each commitment to name the contrast it is a commitment *about*, so `crit` tests FW5 L210 rather than list length. Generalise the repo's existing `mod -> bool | None` repair: `mod` returns None (unresolved) whenever µ is not a *declared* variation family — which, under FW5 L1300, an LLM sampler never is — so `active` is `crit ∧ (mod is not False)` and an un-perturbable artifact is never demarcated out. Drop the claim at L249 that this is "Deutsch's sense, made structural" for the `mod` conjunct; it is not in FW5.

**Confidence.**

0.8

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The `crit` half is sound and I do not contest it. The `mod` half fails twice. (1) Spec: the claim that `mod` "makes modifiability constitutive of explanation-hood" and that an unperturbable artifact "is not `active`, hence fails demarcation" attributes to `mod` a consequence the spec assigns to `crit`. `active(a)` appears exactly once in the document — its definition at L246 — and gates nothing; §0 L37 and §4 L229 bar measures from label computation, and the only place demarcation acquires teeth is §10.1 L366, `skeleton-wf`, which "passes iff the skeleton parses AND `forbidden ≠ ∅`" — the `crit` conjunct alone. L249's "an artifact that forbids nothing has an empty attack surface and fails demarcation" is a sentence about forbidding, i.e. about `crit`; the finding reads it as covering `mod`, then asks that the phrase "Deutsch's sense, made structural" be withdrawn from a conjunct it does not describe. (2) FW5: "FW5 nowhere makes variability constitutive" contradicts the finding's own lead citation. L210 (non-circular dependence, a conjunct of (E)) requires "at least one admitted contrast that removes or changes a nonempty block of active organizational commitments... for which the answer profile changes or ceases to be determined in the claimed way", and L212 adds that "A contrast family... defined to exclude every change that could matter, does not meet non-circular dependence." `mod(a) ⇔ Pr[a' ≉_B a] > 0` — some bounded edit changes the verdict profile — is a recognizable structural surrogate for that existential clause. So the claim that "an account maximally constrained by its anchoring is the *best* case under (H), not a non-explanation" is backwards on FW5's own terms: an account no admitted contrast can move fails (E) at L210/L212. (H)'s limiting case Pres(F)=∅ is not the optimum; L381 explicitly denies that maximal indispensability is what hard-to-vary means.

**Refuter — Corrected finding.**

helps (crit) / neutral (mod). Keep the crit critique unchanged, including the L210 sharpening that each commitment should name the contrast it is about rather than occupying a list slot (L582 concedes "Skeletons can be gamed by toothless forbidden cases"; the H005 field-pressure evidence is apt). Drop the mod critique: `mod` is a structural surrogate for FW5 L210's difference-making-contrast clause, not an alien variability requirement, and `active` gates nothing in the spec. The one transferable repair remains worth proposing on measurement grounds alone: since µ is a sampler, a null draw should read as unresolved rather than false (FW5 L634, "That makes the attribution unresolved; it does not prove either understanding or its absence"), matching the repo's `mod -> bool | None` and the spec's own `overrun`-for-no-variator discipline at §7 step 4.

### MC-04

**Finding id.**

MC-04

**FW5 claim.**

FW5 L383: "Reach occurs when an unchanged organizational core participates in an account of another question **through a stated anchor and additional background**. The new bridge is itself content and can be a creative contribution." L851: "no special count of 'independent reach' is licensed to choose explanations by itself." L232: "Matching the table therefore does not establish (E)." L332: "Endpoint agreement establishes neither identity of active causes nor identity of contributors."

**Spec mechanism.**

§6 L267-269: "Periodic budgeted cross-evaluation of accepted artifacts against other problems' criteria; **a hit raises standing** and Spawns an explanation-debt problem… the event log timestamps what an artifact was built for, so 'accounts for something it wasn't built for' is verifiable in the trace, and reach hits on **held-out** material are the highest-signal event the informal side produces." §10.5 L391-393 (Reveal, "Lakatos's novel-fact criterion, mechanized").

**Verdict.**

hinders (with one clause that helps)

**Argument.**

A cross-evaluation hit is an artifact passing another problem's *criteria* — that is endpoint agreement, and FW5 L232/L332 say endpoint agreement establishes nothing about the active route. FW5's reach is stronger and different: it requires an unchanged core to participate *through a stated anchor*, and it says the bridge is itself content that must be accounted for. So the spec's reach detects the symptom FW5 cares about while omitting the condition that makes it explanatory. "A hit raises standing" is the merit smuggle: standing determines what survives and is funded, so reach-count orders explanations — precisely L851. The redeeming clause is that a hit Spawns an explanation-debt problem, which is the demand for FW5's bridge — but it is a *consequence* of the hit rather than a precondition for recording it, so the ordering effect lands before the anchoring work is done. The timestamp criterion is separately interrogable: temporal priority in a log is provenance, not independence, and L393's own appeal to Lakatos mechanizes the temporal-novelty reading of a criterion whose contested content is *use*-novelty. FW5 L640's warning applies directly — a timestamp is a host-maintainable fact and "not automatically machine-maintainable facts merely because a host can maintain corresponding labels".

**Repository evidence.**

`docs/SEMANTIC_GUIDE.md:57` "Reach or edit-survival counts supply no numerical warrant"; `docs/reviews/FW5-research-plan-decision.md:15` "reach does not supply a numerical warrant". `docs/design/engine-design-of-record-2026-09-14.md:910` excludes "no reach cross-evaluation" from the engine, and §11.7's default axes were replaced at P1 partly because "reach require[s] the variator and cross-evaluation, which are P2" (`:292`). The skew-matrix challenge is the offline analogue: the Leibniz expansion and the short transpose/parity proof reach identically across all odd dimensions, and `docs/reviews/FW5-account-skew-matrix-challenge.md:51` insists "relative clarity does not establish that the expansion has no bearing" — coverage did not discriminate; anchoring had to.

**Testable consequence.**

On any run with reach enabled: for each recorded hit, ask whether an anchoring artifact exists that states how the core participates in the second question. If hits accumulate without such artifacts, reach is measuring criteria-satisfaction across problems, not FW5 reach, and the "raises standing" edge is a count-based ordering. Needs new occurrences. Offline proxy available now: take two H005 cycle-1 artifacts from different arms that satisfy the same problem criteria and check whether either supplies a stated anchor between the two questions — the four-way view design (`PROTOCOL.md:15-19`) exposes commitments precisely so this is inspectable.

**Proposed change.**

Make the explanation-debt Spawn a *precondition*: a cross-evaluation hit is logged as a candidate, and becomes a reach record only when a bridge artifact stating the anchor is registered and itself survives adjudication. Delete "raises standing" from L269 — a reach hit should Spawn and steer attention, never alter status or selection weight. Restate L393 to say the log establishes temporal priority only, and that temporal priority is not use-novelty.

**Confidence.**

0.82

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

"A hit raises standing" is read as an epistemic ordering ("standing determines what survives and is funded, so reach-count orders explanations"). The spec's statuses are enumerated at §4 L212-223 — accepted / refuted / suspended / suspended_unsupported — and "standing" is none of them; §4 L229 states "Measures, school membership, novelty/diversity signals, and Pareto rank MUST NOT enter label computation", and §11.7 L469 spells out the intended sense: "Never a status; an artifact off the frontier is merely unfunded, not demoted." Survival and funding are exactly the two things the spec separates, and the finding's gloss fuses them. L851 forbids counts entering (G)/(P)/(EK) as automatic warrant; FW5 L605 is permissive about attention policy — "The class imposes no maximizing attention function" is a statement that FW5 requires none, coupled with the demand that attention's "organization and the values affecting it are potential criticism targets". The L232/L332 endpoint charge is weakened by the sentence the finding truncates: "A table that really encodes an entire relevant organization under its interventions is a different case... Anti-behaviorism is a distinction about organization, not a ban on a data structure." Cross-evaluation runs another problem's *commitments* (program / predicate / rubric evals over content, §1) — constraints under intervention, not a table of observed answers. The finding also drops the disclaimer inside the very sentence it quotes: L269 continues "Reach tracks coupling (Prop 4.1), asserted as a modelling commitment (attackable), not a proven bound" — an explicit refusal of the inference the finding says is being made. The Lakatos prong misses §10.5 L393's actual mechanism: holdout evidence is "registered **sealed**: content-addressed (hash visible; bytes excluded from all packs by the deterministic renderer)". That is informational isolation — the artifact demonstrably could not have used the material — which addresses use-novelty directly; the timestamp parenthetical is corroboration on top of the seal, not the criterion. FW5 L640's target is a host label standing in for a semantic attribution; a seal that withholds bytes is a carrier fact of the kind FW5 L1238 says can be reliably checked.

**Refuter — Corrected finding.**

neutral (one clause to tighten): a cross-evaluation hit passes another problem's commitments without exhibiting FW5 L383's "stated anchor" through which the unchanged core participates in the second question, so the recorded object should be named a coupling candidate rather than reach, and the explanation-debt Spawn is the demand for the missing bridge. The ordering charge does not survive §4 L229 and §11.7 L469 — "standing" is scheduler focus, not status — and the Lakatos charge does not survive §10.5 L393's seal, which supplies informational isolation rather than mere temporal priority. Residual worth keeping: L269's "raises standing" is ambiguous between attention and status on its face and should be reworded to the §11.7 formula ("funding, never status"), and reach as a PARETO axis inherits whatever is unfixed about its coordinate (see MC-05).

### MC-05

**Finding id.**

MC-05

**FW5 claim.**

FW5 L802: "Equation (P) does not rank alternatives." L804: "This class does not manufacture a common currency or smuggle in 'sufficient merit' as a circularly defined predicate." L896: aesthetic respects are "a set of aesthetic respects, not an ordered scale." L605: "The class imposes no maximizing attention function… Attention is itself an activity in the history. Its organization and the values affecting it are potential criticism targets." L787: O and P are "both fixed for that comparison… they must not shift inside its assessment."

**Spec mechanism.**

§11.7 L467-469: "Scheduler focus… and run reports keep the **Pareto frontier** over `PARETO_AXES` (default: `HV_B`, reach `R_t`, criteria-coverage) rather than argmax-HV. Greedy single-metric selection collapses the population onto one basin of the measure itself… **Never a status**; an artifact off the frontier is merely unfunded, not demoted."

**Verdict.**

helps

**Argument.**

This is the one spec measure whose *form* is what FW5 requires. A Pareto frontier is a refusal of a common currency: it is a partial order, it declines to trade axes against one another, and L469's stated reason ("collapses the population onto one basin of the measure itself") is the same worry FW5 states at L804 and again at L849 about merit-preference circularity. FW5 has no objection to multiple incommensurable obligations being tracked side by side — (P) is explicitly a conjunction over O and P with "Losses outside P must be exposed" (L802), which is structurally a non-aggregating multi-criterion record. Two caveats keep this from being unqualified. (i) Legality of the order does not launder the coordinates: two of the three default axes (HV_B, reach) are the scalars indicted in MC-01 and MC-04, so the frontier is a partial order over smuggled quantities. (ii) "Unfunded, not demoted" is exactly the distinction FW5 L605 declines to grant automatically — a frontier that determines successor budget *is* a maximizing attention function over a chosen measure vector, and FW5's response is not to forbid attention policy but to require that the policy be a criticism target with its own account. The spec half-supplies this (school-policy artifacts are registered via Refl and attackable, L414), but PARETO_AXES is a config knob, not an artifact.

**Repository evidence.**

The repo's P1 profile already repairs coordinate (i) without saying so: `docs/design/engine-design-of-record-2026-09-14.md:292` sets `PARETO_AXES = ("coverage","conn","attack_survival")` with `coverage(a) = {num: #criteria of addressed problems with a pass verdict, den: #criteria}` and `attack_survival(a) = #warranted attacks on a that are themselves refuted`, and states "An artifact off the frontier is unfunded, never demoted." `src/deepreason_core/adjudication/__init__.py:5` enforces "novelty/diversity signals, and Pareto rank MUST NOT enter label computation", and `:220` records a unit test that `grounded.py` and `support.py` import nothing but types and stdlib — the never-a-status invariant is mechanically checked here, which is more than the spec does.

**Testable consequence.**

Testable offline on the existing engine design: register the same artifact set twice under two different PARETO_AXES tuples and confirm (a) labels are byte-identical (the import-allowlist test already secures this) and (b) the funded set differs. If (b) holds — it will — then the axis choice determines which explanations receive successor budget, which is a substantive commitment requiring its own account under FW5 L605, and it must be registered as an attackable artifact rather than a config knob. `attack_survival` is the axis to watch: it counts *occurrences* of refuted attacks, and FW5 L622 separates criticism occurrence from bearing.

**Proposed change.**

Keep §11.7 essentially as written — it is the FW5-compatible shape. Require each axis to name the obligation o it tracks in (P)'s sense, and require PARETO_AXES to be fixed before the evidence window it governs (FW5 L787) and registered as a Refl artifact so it is attackable like a school policy. Demote any axis that is not an obligation-predicate (conn, as a bare edge count, falls to FW5 L381's splitting-features objection) to report-only.

**Confidence.**

0.75

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

Checked and largely confirmed. A Pareto frontier is a partial order and refuses the common currency FW5 L804 warns against; (P) at L787-802 is a conjunction over fixed O and P with "Losses outside P must be exposed", which is a non-aggregating multi-criterion record; L896's "a set of aesthetic respects, not an ordered scale" and L882's "No scalar utility or maximizing selection is required" are consistent. Caveat (ii) is verified at source: PARETO_AXES is a config knob (§15 L555, default "HV, reach, coverage"), and §3 L173's Refl row enumerates "rule-artifacts, demarcation criterion, adjudication semantics, standards, guard procedures, and school-policy artifacts" — scheduler axis selection is not on that list, so the gap the finding names is real, and L605's "Attention is itself an activity in the history. Its organization and the values affecting it are potential criticism targets" is the right citation for closing it. Two softenings. First, "FW5 L605 declines to grant automatically" the unfunded/demoted distinction over-reads: L605 says FW5 imposes no maximizing attention function, which withholds a *requirement*, not a *permission*; FW5 separates choice events from content throughout (L847: "A participant's choice is an event. An argument for that choice is content"), so a funding policy that touches no status is not thereby a merit order. The demand is that the policy be accountable, and that demand the finding states correctly. Second, caveat (i) inherits whatever survives MC-01 and MC-04; on my reading HV_B's coordinate defect is the undeclared µ rather than scalarity as such.

**Refuter — Corrected finding.**

helps (verdict unchanged). Trim the L605 caveat from "FW5 declines to grant the unfunded/demoted distinction" to "FW5 grants no automatic exemption for attention policy: L605 makes the organization of attention and the values affecting it criticism targets, so a frontier that allocates successor budget must be registered as an attackable artifact rather than a §15 config knob." Restate caveat (i) as inheriting MC-01's surviving defect (µ undeclared) rather than scalarity per se, since FW5 L851/L1302 permit counts as information. The substantive asks stand: each axis names the obligation o it tracks in (P)'s sense; PARETO_AXES fixed before the window it governs (L787, "both fixed for that comparison... they must not shift inside its assessment") and registered via Refl; conn as a bare edge count demoted to report-only under L381.

### MC-06

**Finding id.**

MC-06

**FW5 claim.**

FW5 L622: "A criticism occurrence can exist when (K1) is false… A mere adverse signal is not made into a criticism by giving it a negative label." L1052: "No requirement says a failed objection must change the conclusion." L1264: "None of (E), (G), (P), (EK), or (U3) depends on an empirical-frequency update or a merit maximization." L1074: "A finite list of failures is not, by itself, that proof."

**Spec mechanism.**

§11.3 L436-448. Adjudicator-surface metrics: "**attack-target entropy**… **criticism debt**… **G-churn**… **reinstatement rate** (a Popperian system where nothing is ever reinstated is suspicious — band, not floor); **validity-node attack rate** (if no test is ever attacked, D3 has died in practice while remaining true on paper)." Flags are conjunctions with hysteresis. L448: "Honest limit, stated: these detect **stalled** dynamics, not **wrong-but-stable** ones." Response ladder §11.4 L450-457.

**Verdict.**

neutral (helps as alarm, hinders as diagnosis)

**Argument.**

L448 is the most FW5-compatible sentence in the spec: it states its own blind spot in FW5's own terms, and it matches FW5 L1074 and L1258 on what finite records cannot establish. Keeping the whole section to attention (L412 "steers **attention**… never status") is the correct architecture, and the response ladder's refusal of a learned controller (L457, meta-attractor risk) is the same self-application FW5 demands at L605. The defect is in what the individual flags count. Every adjudicator metric is a rate of *occurrences* — attacks registered, tests attacked, statuses changed, reinstatements — and FW5's central separation is occurrence ≠ bearing ≠ use. A window with no validity-node attacks because the tests are good is indistinguishable, by this metric, from a window with none because criticism has ritualized; the spec asserts the second reading ("D3 has died in practice"). `reinstatement rate` as a *band* is worse: it legislates a target frequency of error-correction, which is an empirical-frequency criterion of exactly the kind L1264 excludes from every FW5 predicate. FW5's own diagnostic is available and is not a rate: L601's active-route condition — does the criticism sit on a route with nonconstant dependence on the represented distinction — and L1052's return-relevance probe (at least one alternative subsidiary result must be able to produce a different use-state).

**Repository evidence.**

`AGENTS.md:15` "Do not let an operational alarm adjudicate content"; `docs/SEMANTIC_GUIDE.md:59` "Capture alarms concern behavior under declared assumptions, not truth or creativity." The repo's own version of the missing diagnostic is its stated falsifier: `docs/design/engine-design-of-record-2026-09-14.md:890` — "if… root still cannot identify a single episode in which a warranted criticism changed a later operative use, then the missing ingredient was never the bookkeeping". That is an episode-level use question, not a rate. `docs/reviews/engine-path-decision-2026-09-14.md:25-31` states the repo currently has "no mechanical notion of a criticism *landing*". §11 is excluded wholesale from the built engine (`engine-design…:910`).

**Testable consequence.**

Offline, on the frozen H005 occurrence-01 cycle-1 artifacts: count objection→response pairs (five-node templates in `artifacts/daily/{mini_fcl,mini_prose,matched}/cycle01/`) and compute a crude attack-rate; separately, root-inspect each pair for FW5 L601 nonconstant dependence — did the response's later use change with the objection's *content*? If the rate is high and the dependence count is zero, the rate metric is measuring criticism occurrence, not criticism landing, and cannot discriminate ritual from health. This is decidable on the evidence already in the tree.

**Proposed change.**

Relabel all §11.3 adjudicator metrics explicitly as occurrence counts, with a one-line note that occurrence is not bearing (FW5 L622). Replace `reinstatement rate`'s band with a no-target diagnostic (report the distribution; do not declare a suspicious region). Add one metric FW5 actually licenses: per criticism, whether a content-changing contrast and a content-preserving recoding were both available and produced different/identical downstream use (FW5 L630) — that is the contrast contract, and it is graph-native in the same way the rest of §11.3 claims to be.

**Confidence.**

0.78

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The descriptive observation — every §11.3 adjudicator metric is a rate of occurrences, and FW5 separates occurrence from bearing — is correct and worth recording. The "hinders" inference does not follow. FW5 L622's prohibition is that an adverse signal must not "be made into a criticism by giving it a negative label"; §11 flags are not criticisms and produce no warrants — §11 opens at L412 with "Everything in this section steers **attention** — pack rendering, scheduling, budgets, registration gates — never status (§0)", and the one route to content is the audit-the-critic *Spawn*, a problem rather than an attack. L1264 ("None of (E), (G), (P), (EK), or (U3) depends on an empirical-frequency update or a merit maximization") is a statement about the scope of FW5's own predicates; it does not forbid a scheduler from computing a frequency, and no harness predicate is being made to depend on one. So the reinstatement band "legislates a target frequency of error-correction" only for attention, which FW5 neither licenses nor forbids — L605 requires that the policy be criticizable, which is a different (and MC-05's) demand. The spec is also misdescribed on the validity-node metric: the finding treats "if no test is ever attacked, D3 has died in practice" as the flag's reading, but L446 defines "Adjudication ritual = **any two of** {attack-entropy < floor, criticism debt > ceiling, reinstatement outside band, validity-attack rate ≈ 0} sustained", and L436 states the design reason — "flags are **conjunctions** with hysteresis — similarity alone is ambiguous... progress alone is ambiguous." A zero validity-attack rate is explicitly insufficient on its own. What remains is a design-quality objection — these rates may not discriminate ritual from health — and the spec states that limit itself at L448 in FW5's own register, which the finding calls "the most FW5-compatible sentence in the spec." An axis judging spec-against-FW5 cannot convict a section of hindering on a ground the section concedes and that FW5 does not regulate.

**Refuter — Corrected finding.**

helps (weakly), with one labelling repair: §11.3's adjudicator metrics are occurrence rates, and FW5 L622 separates occurrence from bearing, so each should be labelled an occurrence count and none should be glossed as a diagnosis of what criticism is doing (the gloss "D3 has died in practice" overstates what a zero rate shows, even inside a 2-of-4 conjunction). The L1264 charge should be withdrawn: it bounds FW5's own predicates, not a scheduler's arithmetic, and §11 touches no status (L412, §0 L37). The additive proposal is the valuable part and is independently FW5-grounded: add a per-criticism record of whether a content-changing contrast and a content-preserving recoding were both available and produced different/identical downstream use (L601's nonconstant-dependence condition, L630's contrast contract, L1052's return relevance). That is a diagnostic FW5 licenses and §11.3 lacks.

### MC-07

**Finding id.**

MC-07

**FW5 claim.**

FW5 L640: "A source's appearance in a prompt is a delivery fact… They are not automatically machine-maintainable facts merely because a host can maintain corresponding labels." L661: "A passing execution cannot make the program's specification, the model of the experiment, or the claimed relevance immune to prose criticism." L174: "A causal assignment must be anchored to a causal assignment or a derived causal suborganization, not merely to an observed association." L1101: "An enabling condition is inadmissible if its only description is 'the conditions under which the system succeeds.'"

**Spec mechanism.**

§11.3 L444: "*Grounding ratio λ:* windowed fraction of verdicts from `program`/`observation` evals vs. `rubric`; evidence-artifact entry rate; fraction of accepted artifacts whose support chains bottom out in an exogenous anchor (evidence, program check, user ruling) rather than pure conjecture. `LAMBDA_FLOOR` is the closed-loop alarm line." §11.8 L471-480, the pre-registered dose-response experiment; L479 "**Falsifier, stated in advance:** if λ=full tracks λ=0, the anchoring as built does not earn the theorem's exemption." §12 L490-493: evidence "enters as an artifact depending on a source-reliability assertion".

**Verdict.**

helps (as experiment) / hinders (as health metric)

**Argument.**

Split the two uses. §11.8 as an *experiment* is the most FW5-disciplined thing in the document: pre-registered thresholds committed before first look, oracle-blind arms, distributions not means, and a falsifier stated in advance. That is FW5's fix-before-assess rule (L787, L1101, L1129) executed, and it is exactly the posture the repo demands everywhere. λ as a *metric* is a different object and fails on two counts. First, it counts verdict *kinds* — `program`/`observation` vs `rubric` — which is host bookkeeping, the thing FW5 L640 names as not constituting the semantic relation it labels. FW5's anchoring is typed by the target's component kind (L174), not by which evaluator produced a verdict; a program check whose specification is wrong is a closed-loop artifact with a `program` label, and FW5 L661 says the passing execution immunizes nothing. Second, §12 makes evidence itself an attackable artifact depending on a source-reliability assertion, so "bottoms out in an exogenous anchor" bottoms out in another node in the same graph; the ratio then measures a distribution of node types, not contact with anything outside the loop. The spec's own L448 admits the exogenous anchors are "the only lever" against wrong-but-stable consensus and L584 calls LAMBDA_FLOOR "load-bearing, not decorative" — which makes the weakness of the operationalisation consequential rather than cosmetic.

**Repository evidence.**

The repo's H005 carrier finding is the same failure class at small scale: `docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md:26` — reading `commitments_sha256 = e3b0c442…` (the sha of the empty string) at face value "would score an encoding fault as an arm that declined to commit"; the review's whole point is that a count over record-kinds absorbs carrier facts as semantic facts. `docs/SEMANTIC_GUIDE.md:20` "A delivered answer is evidence of delivery. A schema check establishes an interface fact." `docs/EXPERIMENT_METHOD.md:63` "A verifier's success does not immunize the specification, interpretation or relevance of its checks (FW5 'Evidence receipts without false certainty')." §11's λ is absent from the built engine (`engine-design…:910`).

**Testable consequence.**

Offline, on occurrence-01: compute any kind-ratio over the 19 recorded nodes (COMPLETE 17 / OPAQUE 2 per `checkpoints/wave0005.json`) and observe that the two OPAQUE nodes shift it for a raw-newline JSON reason documented at `h005-matched-arm-envelope-asymmetry…:  the mechanism`. Any λ-style ratio inherits this: it cannot distinguish a missing anchor from a carrier fault. Positively: §11.8's falsifier is testable as stated, and requires new long-horizon runs; its pre-registration discipline is offline-checkable now against `docs/SEMANTIC_GUIDE.md:43` ("Changing the question, grain, anchors or protected obligations makes a new claim").

**Proposed change.**

Keep §11.8's experimental design verbatim; it needs no FW5 repair. Replace λ-as-floor with a per-artifact typed anchoring record: for each accepted artifact, whether its anchoring is to a target component of the right kind (FW5 L174), recorded as a list of unmet anchoring obligations rather than a ratio — the un-supplied conjuncts *are* the alarm, which is how ECS 2.0 §10.3 itself frames its contract. If a ratio is retained for scheduling, require it to exclude nodes whose envelope status is degraded, so a carrier fault can never move it.

**Confidence.**

0.8

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The split is right and the §11.8 half is correct; the metric half does not land. (1) L640's target is a host label substituting for a semantic attribution — "Actual use of the source as a premise, actual understanding, and actual criticism are semantic attributions. They are not automatically machine-maintainable facts merely because a host can maintain corresponding labels." λ attributes nothing semantic: it is a windowed ratio of which evaluator produced a verdict, and a `program` verdict is an actual execution, i.e. a narrow record fact of exactly the kind FW5 L661 concedes ("A machine check can establish a limited proposition") and L1238 affirms ("This is compatible with reliable checks of narrower record facts"). The finding's own second citation, L661, says a passing execution immunizes nothing — true, and the spec agrees at §1 ("Oracle isolation is not adjudication... A containment kill produces no epistemic verdict and MUST NOT mint a warrant") and routes specification criticism through the ν and the evidence closure. That bears on individual verdicts, not on whether a kind-ratio is a usable stall alarm; λ is never claimed to certify any verdict. (2) The "bottoms out in another node in the same graph" argument proves too much. §12 L490-493 makes evidence an attackable artifact depending on a source-reliability assertion; the finding treats that attackability as showing the anchor is inside the loop. But attackability is fallibilism (FW5 L45-51; spec N1), not endogeneity: the *content* of a fetch, a user ruling or an execution entered from outside the conjecture stream regardless of whether its status is revisable. Requiring an anchor to be unattackable to count as exogenous would convict FW5's own commitments of the same defect. (3) L174 is cited for the claim that FW5's anchoring "is typed by the target's component kind, not by which evaluator produced a verdict" — correct about (E)'s Anchoring conjunct, but λ is not an anchoring predicate and does not purport to compute one; §11.3 presents it as an alarm line and L448 states what it can and cannot reach. The carrier-fault caution from H005 is a genuine implementation risk and the proposed exclusion of degraded-envelope nodes is a good engineering fix, but it is not an FW5 conflict.

**Refuter — Corrected finding.**

helps (experiment) / neutral (metric). Keep §11.8 verbatim as the finding recommends. Restate the metric half as an implementation caution rather than an FW5 conflict: a windowed ratio over verdict kinds is a real record fact (L661, L1238) and never claims to be an anchoring predicate, so L640 does not apply; but the H005 carrier finding shows a kind-ratio absorbs envelope faults as semantic facts, so λ should exclude nodes whose envelope status is degraded, and the per-artifact typed anchoring record (unmet anchoring obligations in FW5 L174's sense, listed rather than averaged) should be added *alongside* λ rather than replacing it — it answers a question λ was never posed to answer. Withdraw the claim that making evidence attackable makes the anchor endogenous.

### MC-08

**Finding id.**

MC-08

**FW5 claim.**

FW5 L332: "Two systems with the same output table can have different active routes… A token-level authorship or causal attribution requires the internal event structure. Endpoint agreement establishes neither identity of active causes nor identity of contributors." L154: "A genuine recoding is an isomorphism of the retained structure at that grain. Coarsening is not automatically an isomorphism." L746: "The equivalence is structural at the stated grain, not string equality or similarity." L1206: equivariance "does not apply to arbitrary compression, loss of event identity, a changed boundary, or a coarsening that identifies a relevant distinction."

**Spec mechanism.**

`≈_B` (Def 3.5), the equivalence relation underneath every measure in this axis: §6 L245 `mod`, L255 `s(a)`, L259 "Count only inequivalent survivors (a rename is the same explanation)", §7 L304 `≉_{B₀}`, and §3 L193 anti-relapse stage 3: "candidate's verdict-vector over the active battery matches a refuted prior's (`≈_B`, Def 3.5) ⇒ block **unless** the candidate carries a warrant against that prior's refuter." Residue L582: "`≈_B` in informal domains is irreducibly judgment-laden."

**Verdict.**

hinders

**Argument.**

This is the load-bearing defect of the whole measures layer, because `≈_B` is upstream of HV, mod, hv-floor and the registration gate. `≈_B` is extensional: sameness of explanation is sameness of verdict-vector over a battery. FW5 L332 is the direct denial — two things with the same output table can have different active routes — and L1208-1224's projection theorem proves the general form: no function of the input/output projection agrees with the accounting predicate on both the parallel and priority constructions, which FW5 checked by enumeration over all four Boolean assignments (L1402). The consequence in the spec is not abstract. Anti-relapse stage 3 *blocks registration* of a candidate whose verdict-vector matches a refuted prior's; by FW5's theorem, that candidate may be a structurally different explanation with a different active route that the battery cannot see. The spec's care elsewhere — "Blocking occurs **only** for relapse onto refuted-equivalents… Blocking non-refuted content would be a diversity gate adjudicating — forbidden by §0" (L195) — shows it understood the hazard of blocking and then located the safeguard in the wrong place: the risk is not blocking accepted content, it is that `≈_B` misidentifies what "the same content" is. And the parenthetical at L259, "a rename is the same explanation", is the one case where extensional equivalence and FW5's grain agree; every other case is unlicensed.

**Repository evidence.**

FW5's own enumeration is recorded at `docs/sources/FW5-explanatory-construction.md:1402`: "All four Boolean input assignments were checked for the parallel and priority constructions. Their endpoint outputs agree, while the active second route differs when both inputs are on." The repo's applied version: `docs/SEMANTIC_GUIDE.md:25` "Prompt inclusion, a citation, self-reported usefulness or **endpoint differences alone**" do not establish reason use; `experiments/diagnostics/H005-open-prose-commitments/PROTOCOL.md:64` "Parser success, agreement with root, adoption of a standard answer, more objections, novelty of wording and longer memory do not establish repair." The engine's identity choice is the counter-model: `engine-design…:890` records that the frozen engine "folds the registration `seq` into artifact identity" and the new engine makes a commitment a first-class object — identity by declared structure, not by behaviour.

**Testable consequence.**

Directly testable offline with no provider call: implement the FW5 parallel/priority pair as two artifacts with an identical battery and identical verdict-vectors, submit the second after refuting the first, and observe that anti-relapse stage 3 blocks it. Blocking a structurally distinct explanation on verdict-vector identity is the observation that decides this finding, and FW5 has already supplied the fixture and enumerated it. The same pair gives HV_B and `mod` identical values for two artifacts FW5 distinguishes.

**Proposed change.**

Make `≈_B` a *surrogate* everywhere it is currently an equivalence: it may license "same" only when accompanied by a declared grain ℓ and a structure-preserving map between the two artifacts' retained organizations (FW5 L154, L1202). Concretely: (a) anti-relapse stage 3 must require a structural witness in addition to verdict-vector identity, and on its absence must log the near-miss and admit rather than block — the spec's existing "Verdicts differ ⇒ admit; log the near-miss" branch generalises; (b) `s(a)`'s "inequivalent survivors" must count at the declared grain, with the ν clause that already names "`≈_{B₀}` adequacy as equivalence surrogate" (L309) promoted from a validity-node assertion to a required declaration fixed before the estimate.

**Confidence.**

0.88

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

Best-supported finding in the set, though overstated in two places. Confirmed: ≈_B (Def 3.5) is extensional, it is upstream of `mod` (L245), `s(a)` (L255), `hv-floor` (L304) and the registration gate (L193), and L1208-1224's projection theorem is real and was checked by enumeration (L1402: "All four Boolean input assignments were checked for the parallel and priority constructions. Their endpoint outputs agree, while the active second route differs when both inputs are on"). The decisive asymmetry the finding identifies is genuine and, as far as I can find, uncovered anywhere in the spec: a `fail` verdict yields a contentful warrant with a ν that can be attacked (§7 L307) and a status that N1 guarantees an exit from, whereas a stage-3 block registers nothing at all — no artifact, no ν, no attack surface, no reinstatement path. §0 L37 files registration gates under attention, but a gate that prevents registration is not attention in the sense the rest of §11 uses; nothing downstream can criticize what was never admitted. Two overstatements. First, L1208's theorem is conditioned on a projection that discards the distinction — L1222 says parallel/priority is an instance "when the projection retains only endpoint values" — and a commitment in the spec is `program|rubric|predicate` over content that is Σ* (§0), so a battery may contain route-sensitive structural predicates; L1224 adds "The theorem identifies missing information in a projection. It does not say that no physical or organizational evidence can ever establish the distinction." FW5 L232 makes the same allowance in the sentence the finding truncates: "A table that really encodes an entire relevant organization under its interventions is a different case... Anti-behaviorism is a distinction about organization, not a ban on a data structure." So the theorem shows battery-adequacy to be a substantive assumption rather than showing ≈_B unlicensed in every case but renaming. Second, the spec already declares the surrogacy the finding says is missing: §7 L303 "`B₀ ⊂ B` is a declared surrogate for Def 3.6, asserted in the validity node, hence attackable", ν(iii) "`≈_{B₀}` adequacy as equivalence surrogate", and residue L582 "`≈_B` in informal domains is irreducibly judgment-laden". That is a declaration, not a repair — but it means the charge is under-specification at the gate, not an undeclared conflation throughout.

**Refuter — Corrected finding.**

hinders (sharpened): the defect is not that ≈_B is extensional per se — FW5 L232 admits a table that encodes the organization under its interventions, L1224 denies that the projection theorem closes the question, and a spec commitment may be a route-sensitive structural predicate — but that battery-adequacy is a substantive, battery-dependent assumption which §7 declares and attaches to a ν (L303, ν(iii), residue L582) in the warrant path and leaves entirely unaccounted in the *gate* path. Anti-relapse stage 3 (L193) blocks registration on verdict-vector identity; a blocked candidate produces no artifact, hence no ν, hence no attack surface and no reinstatement, so N1's "every status admits an exit" has nothing to apply to. FW5's enumerated parallel/priority pair (L1402) supplies the decisive fixture whenever the active battery is endpoint-only. Fix: stage 3 must either require a structural witness at a declared grain (L154, L746, L1202) in addition to verdict-vector identity, or — the cheaper and strictly safer option — log the near-miss and admit, generalising the existing "Verdicts differ ⇒ admit" branch, so that no measures-layer surrogate ever produces an outcome with no attack surface. `s(a)`'s "inequivalent survivors" should likewise count at a grain declared before the estimate rather than asserted afterwards in ν.

---

## Axis 5 — language-and-informal: FW5 on expression, prose vs formal carriers, and what a candidate language must let one say, judged against harness-spec v1.3 §6 demarcation, §8 views, §10.1 skeleton/forbidden-case discipline, §10.2–10.4 rubric trials and standards-as-case-law, and the repo's FCL-1.

**Critic's overall assessment.**

On this axis the spec hinders more than it helps, but it hinders in two recoverable places and helps in two places the repo currently has nothing to replace. The damage is concentrated in §8 and §10.1: "prose is a view, not the content" and "forbid nothing, fail `skeleton-wf`, get refuted by a program" together make the carrier constitutive of criticisability and convert a formulation defect into a content verdict — both denied outright by FW5 L857, L690, L69 and L688, and both already overridden in this repository (docs/PROBLEM_PROMOTION.md:7, PURPOSE.md:11, LP-02/LP-05). The frozen H005 evidence makes the cost concrete rather than theoretical: two of seventeen artifacts lose their commitment surface to a raw-newline decode fault, and under §6/§10.1 as written they are undemarcated and refutable for a transport reason — precisely the misreading the repo's own envelope-asymmetry review warns against. What the spec does supply, and FW5 has no mechanism for, is §10.4's audit triple (paraphrase invariance, premise-deletion sensitivity, ensemble disagreement never averaged), which is an independent reconstruction of FW5 L630's content-change / content-preserving-recoding / carrier-disturbance contrast contract, and §10.3's case-law closure, which mechanizes FW5 L63's demand that scrutiny of a standard be able to change the operative target — the exact mechanism docs/reviews/engine-path-decision-2026-09-14.md:25-31 says the repository lacks. On the head-to-head question, FCL-1 is clearly closer to what FW5 says a language must let one say: it carries bearing as a constituent distinct from grounds (L609, L622; exercised in 9 of 9 frozen objection records), it distinguishes declared dependence from mention without inferring either from citation (L640, L653; 11 `depends` against 5 `mentions`), it treats criticism as fallible and usable while invalid (L630), and it lets an author say that a view is insufficient or that nothing can be committed (L688, L438, L468) — the §10 skeleton has no slot for any of these and its one structural advantage, an attackable validity node, is bought in this repo's translation by concatenating grounds and bearing into a single blob. The two things I would not concede to FCL-1 are that the skeleton's `forbidden` list is a real if mis-shaped operationalisation of FW5's non-circular-dependence contrast (L210, L212), and that the FCL carrier mints several times more commitments than the prose carrier for the same content, which FW5 L381 and L851 make inadmissible as evidence and neither document currently forbids.

**Refuter's axis summary.**

Three of eight findings survive intact (LI-5, LI-6, LI-3-with-corrections); LI-4 survives with one of its two defects struck; four fail as written (LI-1, LI-2, LI-7, LI-8). Every FW5 quotation in the batch is verbatim and correctly located — the critic did not fabricate a single line. The failures are all on the spec side or in the application of true quotations to mechanisms they do not govern.

The recurring error is reading the spec's status labels as semantic verdicts while elsewhere granting they are not. LI-1 treats `refuted` as a truth claim about content, though §0 L32, §4 L228 and §5 N1 make it computed, non-absorbing and reinstateable via ν — and LI-4 cites those very lines. LI-1 also fails on FW5's own text: the two-balances limitation account excludes plenty (b_B−b_A=2, and no identification of x from these readings), so it passes `skeleton-wf`; L688/L686 are about observation eligibility and receipts, not about a program verdict on inspected bytes; `mod(a)` is a variation-kernel property, not a rigidity penalty, and is measure-only; and the skew-matrix citation concerns whether a determinant expansion has explanatory bearing, nothing to do with demarcation.

The second recurring error is inverting a spec clause. LI-2's whole diagnosis rests on `forbidden` being 'performed trials' (§10.1 compiles each into a conditional commitment, and §10.5 attaches observation-valued ones to sealed holdout — exactly FW5 L208's unperformed changes) and on §7's 'criterion, never as gate' meaning attention-only (it means not an acceptance gate; §7 L304 and spec L23 route `hv-floor` fail → demonstrative warrant → refuted). LI-7 drops §8 L330's scope clause 'for skeleton-codec artifacts (§10)' and generalises a schema footnote (`prose_notes`) into a doctrine about prose; the real collision is §10.1's pinned skeleton criterion, which the corrected finding retargets.

LI-8 fails on arithmetic I checked directly against the frozen tree: design-of-record:364 mints one Commitment per `type:"commitment"` record, and those number 0/1/0/1/2 across the five mini_fcl nodes, giving 3–5 commitments per FCL node against the prose arm's 3 — not the alleged 7 vs 3. Its proposed invariance rule also overshoots FW5, which makes criticality grain-relative (L154, L352) and asks only that the grain be declared.

Verified counts for the surviving findings: 42 FCL records (claim 15 / objection 9 / use 9 / problem 5 / commitment 4), all 9 objection records carrying `bearing` (9/9), 17 `depends` refs across 11 records, 5 `mentions`, 17 artifacts with the 2 empty `commitments_sha256` both in the `matched` arm. Two citation slips worth flagging to the critic: there are 5 frozen mini_fcl surfaces, not 6, and the objection/rival view lines are transposed (both at material.json:64, body at :74) — and that pair is confounded by differing instructions (:60 vs :70), so LI-3's proposed offline test cannot attribute a difference to the withheld commitment content.

Files read: /home/user/miniReason/docs/sources/FW5-explanatory-construction.md, /home/user/miniReason/docs/sources/harness-spec-v1.3.md, /home/user/miniReason/docs/design/engine-design-of-record-2026-09-14.md, /home/user/miniReason/docs/reviews/{FW5-account-skew-matrix-challenge.md, h005-matched-arm-envelope-asymmetry-2026-09-14.md, engine-path-decision-2026-09-14.md, fcl1-language-proposition-2026-09-14.md}, /home/user/miniReason/docs/{PROBLEM_PROMOTION.md, LANGUAGE_PROPOSAL_THEOREMS.md, SEMANTIC_GUIDE.md}, /home/user/miniReason/AGENTS.md, and the frozen H005 tree under /home/user/miniReason/experiments/diagnostics/H005-open-prose-commitments/. Nothing was modified.

### LI-1

**Finding id.**

LI-1

**FW5 claim.**

FW5 makes a limitation account a legitimate terminal answer. L438: the complete answer "can remain the uncertainty set \(f[Z_y]\)"; L468: "the readings identify \(b_B-b_A=2\), but not \(x\). This is an account of a limitation, not a failure to produce a preferred number"; L810: "progress need not increase the number of accepted claims. Withdrawing an unsupported numerical mass and replacing it with a correct account of underdetermination can improve the inquiry"; L688: "The inability to evaluate a proposition is not a falsifying observation of the proposition."

**Spec mechanism.**

§10.1 L366: "`skeleton-wf` passes iff the skeleton parses AND `forbidden ≠ ∅`" … "demarcation is real (§6) — forbid nothing, fail `skeleton-wf`, get refuted by a program." §6 L246/L249: `crit(a) ⇔ interface.commitments ≠ ∅`, `active(a) ⇔ crit(a) ∧ mod(a)`.

**Verdict.**

hinders

**Argument.**

The skeleton rule converts an artifact's *failure to forbid* into `refuted` — a semantic verdict — by a program. FW5 forbids exactly that inference twice over. First, non-committal is not falsity: L688 separates inability-to-evaluate from a falsifying observation, and L686 blocks turning an absent receipt into a negative one. Second, FW5's own paradigm cases of good work forbid nothing observationally: the two-balances episode (L462–468), which the repo elevates to its worked (G)/(P)/(EK) witness (FW5 L1240–1248), *is* an account of a limitation, and L810 makes the withdrawal of an unsupported claim a repair. Under §10.1 that contribution is refuted at registration. Note the routing precisely: §6's `crit` is a measure and §0 L33/L229 bar measures from label computation, so demarcation alone is attention-only; the refutation route is §10.1's compiled `skeleton-wf` *commitment*, whose fail is a demonstrative warrant. The spec's own §17 L582 concedes the complementary failure ("Skeletons can be gamed by toothless forbidden cases"), so the rule is simultaneously too harsh on honest underdetermination and too lax on fake risk. Separately, `mod(a)` in `active(a)` penalises a rigid obstruction proof — and the repo's one live FW5 stress case (`experiments/diagnostics/fw5-account-skew-matrix/`) is precisely an obstruction account whose ruling was that "relative clarity does not establish that the expansion has no bearing" (FW5-account-skew-matrix-challenge.md:51).

**Repository evidence.**

/home/user/miniReason/experiments/diagnostics/H005-open-prose-commitments/material.json:3 (system prompt): "An empty commitment surface is allowed when none can be identified." The live instrument explicitly permits the state §10.1 refutes. Frozen evidence: of 17 artifacts under occurrence-01/artifacts/daily, 2 carry `commitments_sha256 = e3b0c442…` (empty) — matched/cycle01/response.json and carry.json — and /home/user/miniReason/docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md:26,30 establishes these are a raw-newline JSON decode fault: "the commitments are absent by contract, not because the model omitted them"; "reading `commitments_sha256 = e3b0c442…` at face value would score an encoding fault as an arm that declined to commit." Under `crit` those two artifacts are undemarcated and under §10.1 they would be refuted by a program, for a transport reason. The repo already holds the theorem against this: docs/LANGUAGE_PROPOSAL_THEOREMS.md:29 (LP-02), translation/execution failure does not negate the prose representation.

**Testable consequence.**

Offline on existing H005 evidence, now: run `crit(a)` and a `skeleton-wf`-analogue over the 17 frozen artifacts in occurrence-01/artifacts/daily, and partition the failures into (a) authored non-commitment and (b) carrier fault. The prediction under this finding is that every failure in the current tree is type (b) — 2/2 — i.e. the demarcation predicate as specified measures the encoder, not the reasoner. A second offline check: hand-classify how many of the 15 authored commitment surfaces state at least one defeat condition; on my read all 15 do, in prose, with no schema requiring it — so the schema buys nothing here and only risks the false negative.

**Proposed change.**

Amend §10.1: `skeleton-wf` passes if the content declares *either* a nonempty `forbidden` list *or* an explicit limitation/underdetermination record naming what the evidence cannot settle. And amend L366: a `skeleton-wf` fail must yield `suspended_unresolved` (a formulation defect) and never `refuted` — a content verdict — with the artifact's bytes retained verbatim. Delete `mod(a)` from `active(a)` or exempt obstruction/necessity claims, per FW5 L487–504 and the repo's skew-matrix ruling.

**Confidence.**

0.86

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

Every FW5 quotation is verbatim, but each is applied to something it does not govern, and two spec mechanisms are described wrongly.

(1) The paradigm-case argument fails on FW5's own text. FW5 L462-468 does not exhibit an account that forbids nothing: it identifies b_B-b_A=2 (which excludes every other offset difference) and establishes that x is NOT identified from these readings (which forbids any procedure claiming to identify x from them). L468's contrast is 'an account of a limitation, not a failure to produce a preferred number' — limitation vs. failure-to-answer, not limitation vs. having-a-forbidden-case. The §10.1 schema has scope{covers,excludes} and forbidden[]; the two-balances account fills both. Nothing in FW5 supports 'FW5's paradigm cases of good work forbid nothing observationally'. L810 likewise says withdrawal of an unsupported mass plus acquisition of the limitation account is progress — the limitation account is contentful and exclusionary, which is exactly why L810 counts it as an improvement.

(2) L688 and L686 are misapplied. Both sit inside 'Evidence receipts without false certainty' and concern eligibility of observations: a timeout is evidence about delivery, not about the proposition; negation does not turn an absent receipt into a negative one. `skeleton-wf` is not an inability to evaluate. It is a determinate program verdict on inspected bytes: the submission carries no declared attack surface against the criterion the problem pinned. Calling that 'turning an absent receipt into a negative one' equivocates between missing evidence about the world and a present, inspected artifact missing a declared field.

(3) The spec's `refuted` is misdescribed as 'a semantic verdict'. §0 L32: 'Status is computed, never stored as ground truth'; §4 L228: recompute after every registration; §5 N1: no absorbing status, `refuted→accepted` by reinstatement, 'demonstrative refutation reopens via attack on its validity_node'. §7 L304 shows the exact mechanics for a program-fail warrant, including the canonical reinstatement attack. The finding itself grants precisely this machinery in LI-4 ('§0 L32 Status is computed, never stored as ground truth') and withholds it here.

(4) The `mod(a)` sub-claim misreads §6. `mod(a) ⇔ Pr_{a'~µ(·|a)}[a' ≉_B a] > 0` is a property of whether the variation kernel can emit any inequivalent neighbour at all — it is satisfied trivially by an obstruction claim (swap 23 tokens for 24, odd n for even n, and the variant is inequivalent). It is not a hard-to-vary penalty; the finding conflates `mod` with HV, where LOW variability is the virtue. And `active(a)` is a §6 measure, barred from label computation by the very lines the finding cites (§0 L33, §4 L229) — so `mod` cannot 'penalise' anything at label level.

(5) The skew-matrix citation is a non-sequitur. docs/reviews/FW5-account-skew-matrix-challenge.md is a review of an attempted *counterexample to (E)* over odd-order skew-symmetric matrices; its ruling (line 51, verified) is that the absence-of-bearing argument fails and that a shorter proof's greater clarity does not show the long expansion lacks bearing. It says nothing about variation surfaces, demarcation, or a harness penalising rigidity.

(6) The repo evidence is doubly counterfactual. The two empty `commitments_sha256` artifacts are in the `matched` arm (verified: matched/cycle01/{carry,response}.json), which is rendered outside Mini with free-prose commitments and is not skeleton-codec; and design-of-record:382 already mints a `prose_surface_present` Commitment for that arm, so it is demarcated under §6:244 regardless. §10.1 could only bite on a skeleton-codec artifact under a problem pinning `skeleton-wf`, which is neither this arm nor this study (design:910 puts all of §10 out of scope).

What survives: §10.1 pins `skeleton-wf` on every informal problem, so any contribution must be re-expressed into the schema's slots to pass a criterion — an admission form in FW5 L69's sense — and §17 L582 concedes the complementary gaming failure. That is a real but much narrower point, and it is a point about the admission schema, not about refuting limitation accounts.

**Refuter — Corrected finding.**

§10.1 pins a `skeleton-wf` commitment on every informal problem, so any contribution addressing such a problem must be re-expressed into {claim, mechanism, scope, forbidden} to pass a pre-registered criterion. FW5 L69 denies that the mathematical representation is 'an admission form that every thought must complete', and L857 makes the semantic question whether the distinctions are instantiated and used rather than written in a format. The exposure is the admission schema, not the treatment of underdetermination: an account of a limitation has nonempty exclusions (FW5 L462-468) and passes `skeleton-wf` unproblematically. Proposed change accordingly narrows to: permit an explicit limitation/underdetermination record as an alternative satisfier of the schema's `forbidden` obligation, and drop the claims about `refuted` being a truth verdict (it is computed, non-absorbing, reinstateable via ν) and about `mod(a)` penalising obstruction proofs (it does not, and it is measure-only).

### LI-2

**Finding id.**

LI-2

**FW5 claim.**

FW5 L210 (non-circular dependence): "There is at least one admitted contrast that removes or changes a nonempty block of active organizational commitments … for which the answer profile changes or ceases to be determined in the claimed way." L212 (non-vacuity): "A contrast family containing only notational variants, or one defined to exclude every change that could matter, does not meet non-circular dependence." But L208: the contract "ranges over the declared class of changes, including unperformed changes, not merely over the trials on which the candidate succeeded", and L123: it "is not identified with a collection of performed experiments."

**Spec mechanism.**

§10.1 L352–366 (forbidden cases compiled into budgeted commitments); §6 L261 (`µ_struct`): "µ MUST substitute at role level — swap the mechanism, the motive, the causal link, the scope — not merely reword. This is the Persephone test: if any god and any crime slot in and the account still 'passes,' survivors abound and HV is low. Rewording-only µ measures phrasing rigidity and is declared insufficient for D5." §7 L288: "HV floor as criterion, never as gate." §0 L33/L229: measures never adjudicate.

**Verdict.**

helps

**Argument.**

The Persephone test at L261 is, almost verbatim, FW5 L212's ban on a contrast family "defined to exclude every change that could matter", and `µ_struct`'s role-level substitution over {mechanism, motive/causal-link, scope} is an implementable reading of FW5's edit semantics over active commitments (L91, L109). This is the single best mechanical import the spec offers an FW5 programme, and the repo currently has nothing like it. But the spec gates on the wrong half. `forbidden` is a list of *cases* — a battery of performed trials, which FW5 L123/L208 explicitly refuses as the contract — and it is what admission turns on; `µ_struct`/HV, which ranges over *unperformed* role-level changes and is the FW5-shaped half, is confined to attention by L288 and L229 and is a k∈[5,10] spot-check by the spec's own admission (L259, L580). So the mechanism that would discharge FW5's non-vacuity clause is structurally barred from mattering, and the mechanism that does matter is the form FW5 rules out.

**Repository evidence.**

The repo has implemented neither half: docs/design/engine-design-of-record-2026-09-14.md:910 lists as out of scope "no HV estimator, no `µ_struct`, no `hv-floor`, no variator kernel" and "§10 informal domains entirely: no skeleton criteria, no forbidden-case compilation". FCL-1's `consequence` field is the nearest live analogue and is exercised 13 times across the 6 frozen mini_fcl surfaces (e.g. account record c2: "if they keep recurring, c1 is weakened and the problem is more likely relational"). The repo's standing prohibition (docs/SEMANTIC_GUIDE.md:57, AGENTS.md:15) bars a *numerical* HV warrant, which FW5 L381 also bars — but neither bars a role-level variation family as a declaration.

**Testable consequence.**

Needs new occurrences, but cheaply: take the 15 authored H005 commitment surfaces, have a variator perform role-level substitution on the account's mechanism (swap "ambiguity in spoken agreements" for "unequal baseline load", "conflict fatigue") and re-ask the objection node. Prediction under FW5 L212: an account whose stated defeat conditions survive every mechanism swap is vacuous and should be marked so; an account whose commitment surface changes under the swap has a real contrast family. This is not offline-testable on occurrence-01 — it requires new provider calls — and must be pre-declared as a contrast family, not scored.

**Proposed change.**

Invert §10.1's gate: make well-formedness turn on a declared *role-level variation family* for the artifact's mechanism (what would have to change for this to stop accounting for the problem), with `forbidden` cases optional supporting detail. Keep the variation family as a declaration, never a count — FW5 L381: "splitting one feature into ten cannot create knowledge. Nor is it a numerical warrant."

**Confidence.**

0.72

**Refuter verdict.** stands: false, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

The FW5 quotations are exact and the positive half of the finding is correct: §6 L261's Persephone test ('if any god and any crime slot in and the account still passes') is a near-verbatim mechanisation of FW5 L212's ban on a contrast family 'defined to exclude every change that could matter', and role-level substitution over {mechanism, motive, causal link, scope} implements FW5's edit semantics (L91, L109). But the finding's diagnosis — 'the spec gates on the wrong half' — inverts both halves of the spec.

(1) `forbidden` is NOT 'a battery of performed trials'. §10.1: the harness 'compiles each forbidden case into a commitment in I(a): "if this case obtains, I fail"'. That is a conditional commitment over unperformed cases. §10.5 makes this explicit: observation-valued forbidden cases plug into sealed holdout with scheduled `Reveal`, and 'Sealed evidence does not count as covering (§1) — no premature research Spawn; the commitment is scheduled-pending, not failed'; problems 'SHOULD pin novel-case criteria: the candidate commits, via its skeleton, to expectations over unseen cases'. This is precisely FW5 L208's contract 'ranging over the declared class of changes, including unperformed changes, not merely over the trials on which the candidate succeeded', and FW5 L123's 'not identified with a collection of performed experiments'. The finding attributes to the spec the exact form FW5 rules out, when the spec does the opposite.

(2) µ_struct/HV is NOT 'structurally barred from mattering'. §0's measure rule has three routes, and clause (b) is 'being packaged as budgeted commitments whose fail verdicts generate warranted attacks (§7)'. §7 L288's heading 'HV floor as criterion, never as gate' means it is not an *acceptance gate* — it is pinned into a problem's `criteria`. §7 L304 spells out the fail path: 'V = fail ⇒ the harness registers (Crit) a critic artifact carrying an ordinary demonstrative warrant … a fresh, unattacked critic is in G ⇒ the relation is refuted — never suspended'. The changelog at spec L23 states it outright: 'floor relocated into connection-problem criteria as hv-floor; fail ⇒ demonstrative warrant ⇒ refuted, reinstateable via ν'. So the FW5-shaped half adjudicates, with an attackable validity node carrying exactly the assumptions FW5 would want exposed (kernel fairness, k sufficiency, ≈_{B₀} adequacy, B₀-for-B adequacy). The finding cites L288 and L229 to prove confinement to attention, reading 'never as gate' as 'never adjudicates' — the opposite of what §7 then does for four paragraphs.

(3) The residual concern is real but small: `hv-floor` is pinned by default only on connection problems ('any other problem MAY pin the same schema'), and §10.1's well-formedness turns on `forbidden`, not on a declared variation family. That is a question of which criterion is default, not of one half being barred.

Repo evidence checks out (design:910 non-goals verified; FCL-1 `consequence` used 13 times across 5 — not 6 — frozen surfaces, verified).

**Refuter — Corrected finding.**

§6's µ_struct/Persephone test is the spec's best mechanical import of FW5 L212's non-vacuity clause, and both it and the forbidden-case discipline are FW5-shaped, not opposed: forbidden cases are declared conditional commitments over unperformed cases (§10.1, §10.5 holdout/Reveal), which is FW5 L208's contract, and µ_struct enters adjudication through §0 clause (b) and §7's `hv-floor` fail path (demonstrative warrant ⇒ refuted, reinstateable via ν). The residue is only that `hv-floor` is pinned by default on connection problems while `skeleton-wf` is pinned on all informal ones, so the role-level variation family is the optional criterion and the forbidden list the mandatory one. Proposed change: make a declared role-level variation family a co-equal default criterion on informal problems, keeping it a declaration and never a count (FW5 L381).

### LI-3

**Finding id.**

LI-3

**FW5 claim.**

FW5 L630: a reason-use "contrast contract must include a content-changing case, a content-preserving recoding, and the distinction between a change in the objection and an irrelevant carrier disturbance wherever those distinctions are claimed. These are semantic comparisons, not a mandatory battery of physical tests." L1202–1204: "(E), (G), (P), and (EK) is preserved" under structure-preserving bijections. L628: the map "must preserve internal role bindings, not merely the endpoint string."

**Spec mechanism.**

§10.4 L379–389 judge audits: "Paraphrase invariance: re-run logged rulings on variator paraphrases; flips are hits." "Premise-deletion sensitivity: delete the cited `decisive_point` from the transcript; the verdict SHOULD flip; a verdict that survives the removal of its own stated grounds is easy to vary." Plus planted-flaw calibration and ensemble disagreement (L387, "never averaged away").

**Verdict.**

helps

**Argument.**

§10.4 independently reconstructs FW5's L630 triple and L1202's equivariance requirement, and it is the one place in v1.3 where a *procedure* exists for distinguishing content-sensitivity from carrier-sensitivity. Paraphrase invariance is FW5's content-preserving-recoding leg; premise-deletion sensitivity is FW5's content-changing leg applied to grounds. The spec aims both at the judge rather than at the system under study — L381: "Informal *truth* cannot be program-checked; judge *behavior* can" — which is a defensible scoping move but leaves FW5's actual target (does the responder use the objection's content?) unaddressed. The third leg, carrier disturbance, is absent from §10.4 entirely, and it is the leg the repo has already stumbled into empirically. Redirecting the same three probes at the arms, not at a judge, would give the repo the reason-use instrument its own review says it lacks.

**Repository evidence.**

H005 fork5 already contains a content-*subtraction* contrast in frozen data: in occurrence-01/traces/daily/mini_fcl/cycle01, `objection` and `rival` both take the identical parent artifact `cd6e3e2f307e0dac…` (body sha `360ee14f…`) but with `"view": "both"` and `"view": "body"` respectively (material.json:74 vs :64). The carrier-disturbance leg is supplied accidentally by the envelope fault (h005-matched-arm-envelope-asymmetry-2026-09-14.md:26). The repo states the gap outright: docs/reviews/engine-path-decision-2026-09-14.md:25-31 — "no mechanical notion of a criticism *landing*: no att edge, no warrant, no label". docs/reviews/reason-use-design-audit.md and docs/reviews/reason-use-route-identifiability.md are the prior attempts.

**Testable consequence.**

Offline on existing H005 evidence, now: compare the `objection` output (saw body+commitments) with the `rival` output (saw body only) on the same parent artifact, and ask whether the difference is traceable to the withheld commitment content or is generic. That is one arm of FW5 L630 already paid for. The paraphrase leg needs new occurrences: re-run one node on a recoded objection (same content, different wording) and check the response's commitment surface is structurally unchanged; FW5 L1202 predicts invariance, and a flip refutes the reason-use attribution rather than the model.

**Proposed change.**

Adopt §10.4's probe triple as H005's reason-use instrument applied to the arms, adding the missing carrier-disturbance leg (perturb whitespace/encoding of the objection while holding content fixed). Keep §10.4's rule that ensemble disagreement is "never averaged away" (L387), which is FW5 L634-compatible: unresolved attribution, not a score.

**Confidence.**

0.8

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

The verdict and the core proposal survive; two sub-claims do not.

(1) 'The third leg, carrier disturbance, is absent from §10.4 entirely' is false. §10.4's bias probes include 'verbosity pairs (same content, padded vs. terse)' — a carrier disturbance with content held fixed, which is exactly FW5 L630's third leg. §9's anti-self-conditioning rule ('self-generated prose re-enters packs only re-voiced by the summarizer') is a second instance. So all three of FW5 L630's legs are present in v1.3, and the finding's 'missing leg' addition to the proposal is already spec'd, though only as a bias probe rather than as a reason-use contract.

(2) The content-preserving-recoding leg is not confined to periodic audits: §3's mandatory rubric-verdict guard, applied before any rubric-derived warrant registers, includes 'Paraphrase spot-check: re-run the ruling on TRIAL_PARAPHRASE_N variator-generated paraphrases of the exchange; any flip ⇒ no warrant'. That is stronger than the finding credits.

(3) The 'offline on existing H005 evidence, now' test is confounded and should not be run as stated. The objection and rival nodes differ in instruction as well as view: material.json:60 instructs 'Develop criticism of the account where you have grounds', material.json:70 instructs 'Explore another way of posing or addressing the problem. You see the account's body; its commitment field is not supplied.' (Also the line cites are transposed: view 'both' is at :64 on the objection node and view 'body' at :74 on rival, not the reverse.) A difference between these two outputs is not attributable to the withheld commitment content, because the task differs too. FW5 L628 demands the map 'preserve internal role bindings, not merely the endpoint string' — a confounded pair cannot support the attribution either way.

FW5 L630, L628 and L1202-1204 are quoted exactly and used correctly; the gap the finding names in the repo (engine-path-decision:25-31, 'no mechanical notion of a criticism landing') is verbatim.

**Refuter — Corrected finding.**

Same verdict and same proposal, with three corrections: §10.4 already contains the carrier-disturbance leg as a verbosity probe (padded vs terse, content fixed) and §3's registration guard already applies the paraphrase leg to every rubric warrant, so the adoption is a redirection of existing probes at the arms rather than a completion of a missing triple; and the proposed offline test on the frozen objection/rival pair must be dropped or re-scoped, because those nodes differ in instruction (material.json:60 vs :70) as well as in view, so the pair confounds withheld-commitment-content with task.

### LI-4

**Finding id.**

LI-4

**FW5 claim.**

FW5 L63: "A problem, value, standard, observation model, interpretation, inferential practice, attention policy, attribution boundary, or conjecture-generating restriction can itself become a problem. A result of that inquiry must be able to affect the operative target. Scrutiny that can never change anything is not the recursive capacity described here." L1052: "At least one alternative subsidiary result in the contract must permit a different use-state … A decorative transcript channel permanently disconnected from the operative state does not satisfy the condition." Against this: L620 Bearing(c,z,p) ⟺ Account(𝓔_c, p_δ); L622 "A criticism occurrence can exist when (K1) is false."

**Spec mechanism.**

§10.3 L375–377: standards are registered artifacts, "attackable, reinstateable, succeedable"; "the productive attack in informal domains usually lands on the standard, not the work — and when it lands, every verdict issued under that standard falls with it, and every target reinstates, computed in pass 1." Enforced by the §1 L107–114 case-law closure.

**Verdict.**

helps

**Argument.**

This is the spec's most direct service to FW5 L63 and L1052: it makes the standard an object that can be criticised *and* makes the result of that criticism change what is operative, by construction rather than by curation. FW5's recursive-criticality observable is precisely downstream effect on the operative target, and §10.3 supplies a computed one. The repo has no such mechanism and says so. Two defects keep this from being unqualified. (i) The standard's fall is structural: the closure fires on the existence of an attack edge, with no check that the criticism *bears*. FW5 L620 makes bearing itself an Account of the defect-question, and L622 insists a criticism occurrence can exist while bearing fails — the spec's only stand-in is the validity node ν, which L103 defines as a single assertion that "the test is sound & relevant", conflating soundness with relevance in one attackable boolean. (ii) Automatic reinstatement of every target reads as truth-restoration; FW5 L657 is explicit that "Withdrawing a criticism likewise does not establish the truth of its target." The spec partly defuses this (L32 "Status is computed, never stored as ground truth"; L226 orphaned ≠ false), but `accepted` is nonetheless the label a reader will read as standing, and grounded semantics makes *silence* the warrant for it — which FW5 L47 and L851 both refuse.

**Repository evidence.**

docs/reviews/engine-path-decision-2026-09-14.md:25-31 names the missing mechanism. docs/design/engine-design-of-record-2026-09-14.md:910 records that the §1:108 case-law closure is built at P0 "because P0 test 5 requires it" while §10.3 standards authoring is deferred to P5 — i.e. the repo has adopted the enforcement teeth without the object they bite. docs/design/…:890 pre-registers the correct reading of the label change: "artifacts the frozen engine labelled `accepted` can be labelled `suspended_unsupported` here; that is a correction of bookkeeping, not a result."

**Testable consequence.**

Needs new occurrences plus the P5 build. Decisive test: register the H005 root criteria as a standard artifact, have a later cycle attack the standard, and check whether the artifacts that reinstate are ones root independently judges still defective. FW5 L657 predicts reinstatement will over-fire — some targets will reinstate whose defects were correctly identified under a bad standard. Offline precursor available now: root can read the 6 frozen mini_fcl objection records (9 objections, all with `bearing`) and mark which allege a defect *in the standard of assessment* rather than in the account; the spec predicts the former class is the productive one.

**Proposed change.**

Require the attack on a standard to carry its own defect-question artifact (FW5 L609's four constituents), not merely an edge; and on standard-collapse, reinstate targets to `suspended_unresolved`, never to `accepted` — the verdict is withdrawn, the question is reopened, nothing is established (FW5 L657). Split ν into two attackable nodes, soundness and relevance, so the two FW5 criticism targets at L242 stay separable.

**Confidence.**

0.74

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

The verdict and defect (i) survive in weakened form; defect (ii) should be struck.

(ii) fails. 'Automatic reinstatement of every target reads as truth-restoration' argues against a position the spec states nowhere and denies repeatedly: §0 L32 'Status is computed, never stored as ground truth'; §4 L226 'Refuting a premise ⇒ dependents become suspended_unsupported, NOT refuted (orphaned ≠ false)'; §5 N1 'No artifact — rule-artifacts, standards, school policies, user rulings included — is ever marked final.' When a standard falls, the ν falls, the warrant falls, and the target returns to whatever its *remaining* attackers leave it — the graph does not assert anything about it. That is exactly FW5 L657's position ('Withdrawing a criticism likewise does not establish the truth of its target'), not a violation of it. The residual move — 'accepted is nonetheless the label a reader will read as standing' — is a complaint about reader psychology, not about the mechanism, and the appeal to L851 misapplies it: L851 bars counts from entering (G), (P) or (EK) 'as an automatic warrant'; a defeasible graph label is not (G)/(P)/(EK), and §0 separates them by construction. The appeal to L47 is likewise off-target: L47 says adequacy is independent of acceptance, which is the spec's own position.

(i) survives but overstates. 'The closure fires on the existence of an attack edge, with no check that the criticism bears' understates the structural filter: an edge exists only where an artifact 'carries a warrant against a target', 'a bare verdict is never an edge' (§1), a rubric-derived warrant exists only downstream of §3's four-stage trial guard, and for ν actually to be defeated the attacker must itself survive pass 1's grounded fixpoint. So graph-survival is the spec's stand-in for bearing. What is genuinely absent is FW5 L620's K1 — Bearing(c,z,p) ⟺ Account(E_c, p_δ) — which the spec concedes at L381 ('Informal truth cannot be program-checked; judge behavior can'). That concession is honest, so the finding should report a declared limit rather than an unnoticed defect.

The ν point is the strongest part and stands unchallenged: §1 L103 defines validity_node as one assertion that 'the test is sound & relevant', while FW5 L242 insists that a wrong anchor, a wrong application and a contract omitting a distinction 'are different criticism targets'. Splitting ν is a well-founded proposal.

FW5 L63, L1052, L620, L622, L657 all verified verbatim; §10.3 L375-377 and the §1 closure extension verified; design:910 ('the §1:108 closure that makes standards work is built at P0, because P0 test 5 requires it') verified.

**Refuter — Corrected finding.**

§10.3 plus the §1 case-law closure is the spec's most direct service to FW5 L63 and L1052: a standard is an attackable artifact and the result of attacking it changes the operative target by computation. Two residues, one of them declared: (a) the closure fires on graph survival — an attacker carrying a contentful warrant that survives pass 1 — not on FW5 L620's K1, Account(E_c, p_δ); the spec concedes this at §10.4 L381 ('informal truth cannot be program-checked'), so it is a declared limit, not a hidden defect; (b) §1 L103's validity node conflates soundness and relevance in one assertion, whereas FW5 L242 makes them different criticism targets — splitting ν into two attackable nodes is the warranted change. Strike the reinstatement-as-truth-restoration objection: §0 L32, §4 L226 and §5 N1 already implement FW5 L657, and a defeasible graph label is not a (G)/(P)/(EK) warrant under L851.

### LI-5

**Finding id.**

LI-5

**FW5 claim.**

FW5 L609: "A criticism has a represented target \(z\), an alleged defect \(\delta\), grounds \(g\), and a proposed connection from \(g\) to \(\delta\) relative to a question." L620: Bearing is an Account of the defect-question. L622: "A criticism occurrence can exist when (K1) is false. Its grounds may be mistaken, its target misidentified, its inference invalid, or its relevance wrong." L630: "Understanding and using an invalid objection does not make it valid."

**Spec mechanism.**

§10.1's skeleton schema (L352–362) has slots `claim | mechanism | scope{covers,excludes} | forbidden[] | prose_notes` — no target, no defect, no grounds, no bearing. Criticism enters only as a verdict on a compiled forbidden case, or as an `att` edge whose `validity_node` ν "asserts the test is sound & relevant" (L103). FCL-1: `type: objection` with `target`, `grounds`, `bearing` as separate authored fields (docs/reviews/fcl1-language-proposition-2026-09-14.md, grammar block).

**Verdict.**

helps

**Argument.**

On FW5's own criterion for what a candidate language must carry, FCL-1 is closer than the skeleton, and not marginally. FW5 makes bearing a fourth constituent distinct from grounds — the *connection* — and makes it fallible independently of the grounds (L622 enumerates four ways a criticism can fail, of which 'relevance wrong' is one). FCL-1 gives that constituent its own field and its own fallibility clause ("an objection alleges a defect whose bearing can itself be criticized", material.json:5). The §10 skeleton has no criticism record type at all; the nearest structure, ν, folds soundness and relevance into one assertion. Worse, the repo's own reduction of FCL-1 to spec v1.3 *destroys* the distinction it had: docs/design/engine-design-of-record-2026-09-14.md:372 maps `type: objection` + `grounds`/`bearing` to a single ν artifact whose "content = `grounds` + `bearing` bytes" — a concatenation. That reduction is defended on the ground that ν is itself attackable ("strictly more than FCL-1 offers"), which is true and valuable, but attackability of a blob does not restore the separation FW5 needs: an objection with right grounds and wrong bearing and one with wrong grounds and right bearing become the same node.

**Repository evidence.**

Across the 6 frozen mini_fcl surfaces (occurrence-01/artifacts/daily/mini_fcl/*/*.json), 42 records: claim 15, objection 9, use 9, problem 5, commitment 4. Every one of the 9 objection records carries a `bearing` field (9 `bearing` fields, 9 objections) — e.g. account record o1: "bearing: If load imbalance or relational conflict is the real driver, the specification move in c2 may treat a symptom, and step 5 arrives too late." The carrier elicits FW5's connection constituent at a 100% rate in this sample. The free-prose arms express bearing too (mini_prose/rival: "Its relevance is that the answer would discriminate between the competing readings"), which is FW5 L857 vindicated — but only FCL-1 makes it separately addressable.

**Testable consequence.**

Offline now: root can read the 9 frozen objection records and classify each of FW5 L622's four failure modes (grounds mistaken / target misidentified / inference invalid / relevance wrong). Prediction: the `bearing` field makes 'relevance wrong' separately assessable without re-reading the body; the prose arms' equivalent requires reading the whole surface. A stronger test needs new occurrences: give a downstream node an objection whose grounds are true and whose bearing is wrong, and check whether the response distinguishes them — FW5 L630 says using it does not validate it.

**Proposed change.**

Do not concatenate. Amend docs/design/engine-design-of-record-2026-09-14.md:372 so an FCL-1 objection registers `grounds` and `bearing` as two separately attackable blobs referenced by ν, and add a `defect` slot (FW5 L609's δ) so a target can be attacked for the defect alleged rather than for the criticism as a whole. In the spec, add an optional `bearing` slot to the §10.1 skeleton for criticism artifacts, or state plainly that §10 has no criticism vocabulary and defers to §1 warrants.

**Confidence.**

0.83

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

I could not refute this one. Every element verified independently.

FW5 L609 lists four constituents (target z, defect δ, grounds g, and 'a proposed connection from g to δ relative to a question'); L620 makes bearing an Account of p_δ; L622 enumerates four independent failure modes including 'its relevance wrong'; L630 'Understanding and using an invalid objection does not make it valid.' All verbatim.

Spec side verified: §10.1's skeleton schema is exactly {claim, mechanism, scope{covers,excludes}, forbidden[], prose_notes} — no target, no defect, no grounds, no bearing; §1 L103's ν is one assertion 'the test is sound & relevant'. Criticism enters §10 only as a verdict on a compiled forbidden case or as an att edge. Accurate.

Repo side verified by direct computation over the frozen surfaces: 42 records across the mini_fcl nodes with types claim 15 / objection 9 / use 9 / problem 5 / commitment 4 — the finding's counts are exact; and all 9 objection records carry a `bearing` field, 9/9, so the '100% rate' claim is measured, not estimated. design-of-record:372 maps `type:objection` + target + grounds/bearing to a ν whose 'content = grounds + bearing bytes' — a literal concatenation, confirmed.

Two factual corrections that do not touch the verdict: there are 5 frozen mini_fcl surfaces, not 6 (cycle01 account/carry/objection/response/rival; cycle02 has a body_route trace but no artifact). And FCL-1 has no separate δ slot either — the alleged defect lives inside the objection's free-text `text` — so FCL-1 is closer than the skeleton on three of FW5 L609's four constituents (target, grounds, bearing), not four; the finding's own proposed_change already says as much by asking for a `defect` slot.

**Refuter — Corrected finding.**

### LI-6

**Finding id.**

LI-6

**FW5 claim.**

FW5 L640: "A source's appearance in a prompt is a delivery fact. A named field asking for a criticism is an invitation fact. Actual use of the source as a premise, actual understanding, and actual criticism are semantic attributions. They are not automatically machine-maintainable facts merely because a host can maintain corresponding labels." L653: "A record declaring a dependency does not establish that the dependency is actually essential; an error in that declaration is another criticism target." L1312: "A claim about what the thinker actually used needs an interpretation of its activity."

**Spec mechanism.**

§1 L53–63 `dep` edges; §4 L226 "Refuting a premise ⇒ dependents become `suspended_unsupported`". §10.1's skeleton has no reference vocabulary at all. FCL-1: `depends` vs `mentions`, with "Neither is automatically inferred from citation or lexical overlap" (fcl1-language-proposition-2026-09-14.md:37).

**Verdict.**

helps

**Argument.**

FCL-1 is closer again: it gives the author a slot for FW5's exact distinction and states its fallibility. The skeleton gives nothing, and the spec's `dep` is a graph relation the harness maintains — the shape FW5 L640/L1312 warns against. But the repo's translation reintroduces the very error FW5 names: docs/design/…:372 maps `depends` as "drop the concept, keep the notation → `interface.refs[].role = \"dependence\"` — a real `dep` edge, so the support cascade is live for H005." That promotes a fallible self-report directly into an adjudicative input (§4 pass 2), which is precisely what FW5 L653 forbids: the declaration is itself a criticism target, not an established dependence. The effect is asymmetric by carrier — the design pre-registers that mini_fcl yields derived dep/att edges while mini_prose and matched yield none — and the design correctly forbids reading that as a defect of prose (:385), but it does not forbid reading it as a *merit* of FCL, which is the live risk once labels start moving.

**Repository evidence.**

In the 6 frozen mini_fcl surfaces, `depends` is used 11 times and `mentions` 5 — the distinction is actually exercised, not decorative. The prose arms express the same relation in prose without a slot: matched/cycle01/account.json commitments — "The proposal also carries a dependency I am not able to discharge from the material"; mini_prose/rival — "it depends on the reading above, so it inherits that reading's uncertainty". So the *idea* is carrier-independent (LP-05, docs/LANGUAGE_PROPOSAL_THEOREMS.md:59; H005 PROTOCOL.md:44), and only its machine-addressability is not. docs/design/…:890 pre-registers the asymmetry; docs/LANGUAGE_PROPOSAL_THEOREMS.md:101 (LP-09) is the standing warning that a language label with no additional channel yields no effect.

**Testable consequence.**

Needs the engine plus new occurrences for the full test, but a decisive offline precursor exists: for each of the 11 `depends` edges in the frozen FCL surfaces, root reads the corresponding body and judges whether the declared dependence is actually essential to the use proposed. FW5 L653 predicts some are not. Every such case is a live counterexample to promoting `depends` into a `dep` edge. The full test: run occurrence-02 and check whether any `suspended_unsupported` label traces to a mis-declared `depends` rather than to a real loss of support.

**Proposed change.**

Register an authored `depends` as a *claim artifact* ("I claim this use relies on X"), not directly as a `dep` edge; require a separate warrant — root's reading or a program check — before it becomes adjudicative. Log the divergence between authored `depends` and the dependence root independently reads out of the body, in both FCL and prose arms, as the study's actual measurement (that divergence is the FW5 L653 object).

**Confidence.**

0.79

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

Largely unrefutable; the FW5 quotations are exact and the mechanism description is right.

FW5 L640 ('A source's appearance in a prompt is a delivery fact … not automatically machine-maintainable facts merely because a host can maintain corresponding labels'), L653 ('A record declaring a dependency does not establish that the dependency is actually essential; an error in that declaration is another criticism target') and L1312 ('A claim about what the thinker actually used needs an interpretation of its activity') all verified verbatim. fcl1-language-proposition:37 verified: 'depends asserts reliance; mentions only locates material. Neither is automatically inferred from citation or lexical overlap.' design-of-record:~372 verified: `depends` → 'drop the concept, keep the notation → interface.refs[].role = "dependence" — a real dep edge, so the support cascade is live for H005.' §4's pass 2 then makes that self-report adjudicative via supported()/suspended_unsupported. The finding's core claim is exactly right and the strongest available reading of L653.

The best available rebuttal is partial: the repo does not promote `depends` silently. design-of-record risk 5 registers it as 'a semantic commitment that can be wrong and that materially changes what lands. It is published in this document and in the receipt as a criticisable claim before any live call', and design:890's pre-registration says the same. But declaring a mapping criticisable does not stop it entering §4 pass 2 as an input, which is precisely L653's point: the declaration is a criticism target, not an established dependence. So the mitigation blunts the charge of concealment, not the charge itself.

One count correction: 11 records carry a `depends` field, but they carry 17 dependence refs in total (use 12, commitment 3, claim 2); `mentions` 5 is exact. The offline precursor should therefore be run over 17 declared dependences, not 11.

**Refuter — Corrected finding.**

Same verdict and same proposal, with two adjustments: the frozen FCL surfaces carry 17 `depends` refs across 11 records (use 12, commitment 3, claim 2), not 11 edges; and the repo already registers the `depends`→`dep` mapping as a criticisable claim (design-of-record risk 5 and the §8 pre-registration receipt), so the charge is not concealment but that a declared-fallible self-report still enters §4 pass 2 as an adjudicative input, which is what FW5 L653 forbids.

### LI-7

**Finding id.**

LI-7

**FW5 claim.**

FW5 L857: "The semantic question is whether the relevant distinctions and transformations are instantiated and used, not whether they are written in a particular format." L690: "Ordinary prose need not arrive with a tree, source fields, or a machine-verifiable witness to enter inquiry. The point is that an interpretation of its reasoning must not silently lose its actual dependencies." L69: "No complete translation into a formal language is required of the thinker. The mathematical representation is an account of the relevant organization, not an admission form that every thought must complete." L696: "The outcomes are changes in represented organization, not necessarily sentences."

**Spec mechanism.**

§8 L330: "**Prose is a view, not the content:** for skeleton-codec artifacts (§10), `prose(id)` renders the readable narrative from the skeleton via the summarizer role, cached and logged; the skeleton is what gets criticized." §10.1 L362: `"prose_notes": "string (optional; rendered, never adjudicated)"`.

**Verdict.**

hinders

**Argument.**

This is the spec's sharpest collision with FW5 and the repo has already ruled against it. Making the skeleton "what gets criticized" and `prose_notes` unadjudicable makes the carrier constitutive of criticizability, which FW5 L857 denies as the semantic question and L69 denies as a requirement on the thinker. It also inverts the direction of loss FW5 cares about: L690's worry is that an interpretation "must not silently lose its actual dependencies" — and a skeleton-first pipeline in which the narrative is regenerated by a summarizer from the skeleton loses exactly whatever the author put in the prose and not in the slots. FW5 L228 is the general form: if a genuine explanation requires a distinction no such structure can preserve, the structure must change. The repo's override is already on record and is correct; what is not on record is the residue — once prose is un-demoted, §10 supplies no demarcation for prose at all, and the repo's substitute (`prose_surface_present`, a presence check) is admitted to be shallow.

**Repository evidence.**

docs/PROBLEM_PROMOTION.md:7: "This instruction takes precedence over V1.3 §§8 and 10 wherever their skeleton-only treatment would demote prose." PURPOSE.md:11 and README.md:5 hold the same line; AGENTS.md:11 "syntax and executable tests cannot be made the definition of bearing or creativity"; LP-05 (docs/LANGUAGE_PROPOSAL_THEOREMS.md:59) proves medium confers nothing under an isomorphism of retained organization. The live instrument follows FW5, not the spec: material.json:5 — "The body remains unrestricted prose", "Express uncertainty or an unrepresentable relation in prose rather than inventing a relation". The residue is admitted at docs/design/engine-design-of-record-2026-09-14.md:903: "`fcl1_record_wf` checks that a record exists and is well-formed, not that its substantive obligation holds. §17 already names this failure mode."

**Testable consequence.**

Offline now: the frozen data already runs the experiment §8 would forbid. mini_prose/cycle01/objection.json's commitment surface states a defeat condition, a contestable distinction, and an explicit non-commitment ("What I'm not committing to: I have no basis for proposing a mediator…") entirely in prose, with no schema. Under §8 that content is `prose_notes`, never adjudicated. Root's reading of whether it is criticisable is the test, and it can be done today on 15 authored surfaces. Prediction under FW5 L857: the prose surfaces carry every constituent the FCL surfaces carry, and differ only in addressability.

**Proposed change.**

Strike "the skeleton is what gets criticized" from §8 L330 and "never adjudicated" from L362. Redefine `crit` over authored commitment records in any carrier — which is what H005 already does — and demote the skeleton codec from a content requirement to one optional convention among others. Record in DIVERGENCES.md that v1.3 §§8 and 10.1 are declined here on FW5 L857/L690 grounds, so the decline is a criticisable claim rather than a silent local habit.

**Confidence.**

0.88

**Refuter verdict.** stands: false, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

The FW5 quotations (L857, L690, L69, L696, L228) are all verbatim and the repo evidence (PROBLEM_PROMOTION.md:7, AGENTS.md:11, material.json:5, design:903) is accurate. The verdict may well be right, but the finding as written misidentifies its target and misreads §8.

(1) §8 L330 is scoped, and the finding drops the scope clause while quoting it: 'Prose is a view, not the content: **for skeleton-codec artifacts (§10)**, prose(id) renders the readable narrative from the skeleton via the summarizer role'. For a `codec: utf8` prose artifact the content IS the prose — §0: 'Content is Σ* (Def 3.1, Thm 2.1): opaque bytes + codec. Text, numeric, CSV, code all in scope.' So §8 does not demote prose in general. Within a skeleton artifact, 'the skeleton is what gets criticized' says: criticise the authored source, not the summarizer's regenerated rendering of it. That is the correct call and it is what FW5 L690 wants — an interpretation of prose 'must not silently lose its actual dependencies', and criticising a lossy auto-generated cache in place of the source is exactly that loss. Nothing is lost or silent: §0 'Nothing is deleted', the prose view is 'cached and logged', and §9's safety property is 'any substantive claim about a summarized blob is program-checked against the real bytes; a lossy summary cannot corrupt a verdict.'

(2) 'Makes the carrier constitutive of criticizability' is false on the spec's own definition. A prose candidate addressing an informal problem still carries that problem's instantiated `skeleton-wf` commitment in its battery, so `crit(a) ⇔ interface.commitments ≠ ∅` holds; it is demarcated, attackable, can carry warrants and be a premise. It fails a pinned criterion. Failing a criterion is not being rendered uncriticisable — it is being criticised.

(3) `prose_notes: 'rendered, never adjudicated'` is a field inside the skeleton schema, not a rule about prose artifacts. It means the notes slot does not compile to a commitment. Reading it as 'prose content is unadjudicable' overgeneralises a schema footnote into a doctrine.

(4) §10.1 closes with 'D2 intact: this constrains what survives, not what γ may emit' — the finding's own framing ('makes the carrier constitutive') is the reading that sentence exists to deny.

What survives, and it is worth keeping: §10.1 pins `skeleton-wf` on every informal problem, so passing an informal problem's criteria requires re-expressing the contribution into the schema's slots. That is an admission form in FW5 L69's sense and is a genuine collision. But it is §10.1's criterion, not §8's view rule and not `prose_notes`, and the repo's override in PROBLEM_PROMOTION.md:7 names §§8 and 10 together without separating them either.

**Refuter — Corrected finding.**

The collision with FW5 L69/L857 is §10.1's pinning of a schema-conforming skeleton as a criterion on every informal problem — an admission form every informal contribution must complete to pass — not §8's view rule. §8 L330 is scoped 'for skeleton-codec artifacts (§10)': for a utf8 prose artifact the prose is the content (§0, Σ*), and within a skeleton artifact 'the skeleton is what gets criticized' correctly directs criticism at the authored source rather than at the summarizer's regenerated rendering, with bytes retained (§0) and summary claims program-checked against them (§9). A prose candidate under an informal problem is still demarcated (it carries the instantiated `skeleton-wf` commitment) and still attackable; it fails a criterion, it is not made uncriticisable. Proposed change accordingly: leave §8 L330 alone, and amend §10.1 so `skeleton-wf` is one admissible convention among others rather than a pinned criterion on every informal problem; record that decline in DIVERGENCES.md on FW5 L69/L857 grounds, and separate it there from the §8 claim, which PROBLEM_PROMOTION.md:7 currently bundles with it.

### LI-8

**Finding id.**

LI-8

**FW5 claim.**

FW5 L381: "Two descriptions can divide the same work into different numbers of features; splitting one feature into ten cannot create knowledge. Nor is it a numerical warrant." L154: "Bundling two commitments into one can change the answer to a question about individual contribution while preserving an answer about their joint organization." L851: "No quantity of endorsements, surviving tests, repeated observations, or partitioned features enters (G), (P), or (EK) as an automatic warrant."

**Spec mechanism.**

Nothing in v1.3 bars a measure whose value is a function of how finely a carrier partitions one commitment. §6 L244 `crit(a) ⇔ interface.commitments ≠ ∅` is partition-insensitive, but §11.7 Pareto axes (L467–469), §7 `conn`/`iso` (L280–281), coverage, and any battery-survival count are not; §10.1 L366 compiles "each forbidden case into a commitment", so the count is authored.

**Verdict.**

absent-in-spec

**Argument.**

FW5 states the invariance requirement explicitly and twice; v1.3 states its converse nowhere and builds several measures that violate it. The concrete exposure is already designed into H005: docs/design/engine-design-of-record-2026-09-14.md:372–385 gives `mini_fcl` "one `fcl1_record_wf` Commitment per commitment record" plus a 3-check battery, and gives `mini_prose`/`matched` a 2-check battery plus a single `prose_surface_present` Commitment. In the frozen cycle-1 data that is roughly 7 commitments per FCL node against 3 per prose node, for content that on my reading carries the same constituents. Any downstream measure over `interface.commitments` — Pareto `attack_survival`, coverage, `conn` — is then partly a function of carrier granularity, which is exactly FW5 L381's "splitting one feature into ten". The design forbids reading the asymmetry as a defect of prose (:385) but nowhere forbids reading it as a merit of FCL, and FW5 L851's ban is symmetric.

**Repository evidence.**

Record counts in the frozen mini_fcl surfaces: 42 records across 6 nodes (claim 15, objection 9, use 9, problem 5, commitment 4), against one prose commitment surface per prose node. The repo's own prohibitions are adjacent but do not cover this: PURPOSE.md:15 and AGENTS.md:15 ban a scalar progress meter; docs/SEMANTIC_GUIDE.md:57 bans reach/edit-survival counts as numerical warrants; docs/SEMANTIC_GUIDE.md:59 — "A scalar novelty/progress score cannot adjudicate content." None of these names partition-sensitivity of a commitment count, which is a different failure. H005 PROTOCOL.md:64 comes closest: "more objections … do not establish repair."

**Testable consequence.**

Offline now, and this is a strong check: re-encode one frozen mini_prose commitment surface into FCL-1 records without changing a word of its content, and count the commitments the design's compiler would mint. If the count rises from 1 to ~6 with identical content, every measure keyed to commitment count is measuring the encoder. FW5 L381 predicts exactly this and treats any measure that moves as invalid; the converse — a measure that is invariant under the re-encoding — would license its use.

**Proposed change.**

Add a partition-invariance rule to the spec's §0 measure discipline and to the repo's AGENTS.md prohibition list: no measure may be reported whose value changes under a content-preserving re-partition of an artifact's commitment surface, and every count over `interface.commitments` must be reported alongside its value under the coarsest and finest admissible partition. Pre-register, before occurrence-02's first live call, that commitment count is never evidence for either arm (FW5 L851, L381).

**Confidence.**

0.75

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The bare claim 'v1.3 states no partition-invariance rule' is true — grep for partition/invariance/granularity over the spec returns only §10.4's paraphrase invariance and unrelated hits. Everything the finding builds on it fails.

(1) The concrete exposure is arithmetically wrong. design-of-record:364 mints 'One §1 Commitment per record' in the row for `type: "commitment"` records specifically; :382's 'one fcl1_record_wf Commitment per commitment record' refers to that same row. I counted the frozen surfaces directly: commitment-type records per mini_fcl node are 0 (account), 1 (carry), 0 (objection), 1 (response), 2 (rival). So the FCL arm carries 3 battery + {0,1,0,1,2} = 3, 4, 3, 4, 5 commitments per node against the prose arm's 2 battery + 1 `prose_surface_present` = 3. Not 'roughly 7 per FCL node against 3 per prose node'. Two of five FCL nodes are exactly level with prose. The 42-record total is real but 33 of those records are claim/objection/use/problem, which mint no commitment.

(2) The named measures are attention-only by the spec's own explicit text, which the finding omits. §11.7: Pareto retention is 'attention and reporting only … Never a status; an artifact off the frontier is merely unfunded, not demoted.' §7: `iso(a) > 0 ⇒ Spawn` — Spawn only. §0 clause and §4 L229 bar all of them from label computation. FW5 L851 bars counts from entering (G)/(P)/(EK) 'as an automatic warrant'; scheduler attention is not a warrant, and L851 explicitly adds that counts 'are not outlawed as information'.

(3) The one measure that does adjudicate, `hv-floor`, is plausibly invariant under exactly the re-partition at issue: HV_B is 1 − Pr[an edit passes battery B₀ and is inequivalent]. Splitting one commitment into a conjunction of parts leaves the pass-set unchanged, so ŝ and the verdict are unchanged. §6 also already imposes an equivalence discipline in the same spirit ('Count only inequivalent survivors (a rename is the same explanation)'). So the finding's headline exposure does not reach the adjudicating route.

(4) The proposed rule overshoots FW5. FW5 L154 says bundling 'can change the answer to a question about individual contribution while preserving an answer about their joint organization', and the grain discussion (L352, cited in the précis) makes criticality verdicts legitimately grain-relative. FW5's demand is that the grain be declared and held fixed across a comparison (L170), not that every reported quantity be partition-invariant. 'No measure may be reported whose value changes under a content-preserving re-partition' would forbid FW5's own grain-relative criticality talk.

**Refuter — Corrected finding.**

v1.3 states no partition-invariance discipline anywhere (verified by grep), and FW5 L381/L851 warn that a partitioned feature count is not a warrant. But the concrete exposure alleged does not exist: design-of-record:364 mints one Commitment per `type:"commitment"` record, so the frozen FCL nodes carry 3, 4, 3, 4, 5 commitments against the prose arm's 3 — not 7 vs 3 — and the measures named (Pareto axes, conn/iso, coverage) are barred from adjudication by §11.7's 'Never a status; merely unfunded, not demoted', §7's Spawn-only rule, and §0/§4. The adjudicating measure, `hv-floor`, is invariant under conjunctive re-partition of the battery. The residue worth pre-registering is narrower and is a reporting rule, not an invariance law: commitment count is never evidence for either arm, and any count reported over `interface.commitments` must name the grain at which it was taken and hold that grain fixed across the comparison (FW5 L154, L170) — not the stronger requirement that every measure be partition-invariant, which would forbid FW5's own grain-relative criticality verdicts.

---

## Axis 6 — experiment-design

**Critic's overall assessment.**

On experiment design the spec is mostly a hindrance and in two narrow places a real help. It hinders because its three strongest evidence types — temporal priority in a delivery log (§6 L269, §10.5 L393), the grounded label (§4 L206-229), and the survivor frequency HV_B (§6 L251-259, §7) — are precisely the three things FW5 rules out as evidence about explanatory organization: the projection theorem (1218-1222) kills log-inferred use, bearing is an Account of the defect-question rather than a graph property (611-620), and hard-to-vary is "not a numerical warrant" (381, 851). More seriously, the spec is silent where FW5 is most demanding: it has no protected-obligation set and no loss register, so nothing in it can state (P) at 791-802 or the FW5:808/810 cases, and it does not list this among its residue (§17). It helps in two places. Its §10.4 paraphrase-invariance and premise-deletion probes are two of the three cases FW5:630 requires, re-targetable from judges to responders; and its §1 budget-honesty and oracle-isolation semantics (L79, L80-88) state FW5:688's delivery/content separation cleanly, which the repo has already adopted. The programme can test more than it currently claims: the uptake-divergence ledger (I-1) and the payload-difference precondition (I-4) and the grain/scope invariance probe (I-5) all run offline today on occurrence-01 plus the import's index, and the loss ledger (I-3) can be dry-run retrospectively on H004's conversion18/19 case to calibrate the instrument. What genuinely needs new occurrences is the delivery side: the content-changing / content-preserving-recoding / carrier-disturbance triple (I-2) has only its accidental carrier cell instantiated, by the matched arm's decode loss, and a repair claim under (P) needs O and P frozen before the cycle runs. Every ceiling here is low and should stay low — one problem, one template, one provider, one cycle; each instrument yields at most a finite attributed account of a particular change, never a witness, and an unresolved cell stays unresolved (FW5:634). The residual risk the spec would make worse rather than better, and that none of these instruments fixes on its own, is the observer's selection rule: §10.6 would set the evidence base by machine confusion, which is the FW5:1101 inadmissible-enabling-condition structure applied to the reading rather than the subject.

**Refuter's axis summary.**

Verified every FW5 citation against /home/user/miniReason/docs/sources/FW5-explanatory-construction.md and every spec citation against /home/user/miniReason/docs/sources/harness-spec-v1.3.md; all quotations are textually accurate, so the failures are failures of scope and mechanism-reading, not of quotation. Two of eight findings survive: XD-4 (no protected-obligation set, no loss register, no ProducedBy anywhere in the spec — confirmed by full-text search; §17 L576-588 genuinely omits it; the two candidate rebuttals, §11.7's coverage axis and §0's 'nothing is deleted', both fail) and XD-5 (≈_B is a coarsening, licensed as a critique by FW5:154 rather than FW5:1206, and the spec's own §7 L307 / §17 L582 concede it, which is what the critic's 'helps' verdict says). Six fail as written. Three fail by over-extending an FW5 passage past its own stated scope: XD-1 stops one line before FW5:1224 and ignores FW5:1238's 'compatible with reliable checks of narrower record facts' — the spec's reach hit is a commitment evaluation on revealed material, with the timestamp doing only anti-fitting work; XD-6 drops the word 'automatic' from FW5:851 and its 'not outlawed as information' sentence, when §7 L307 builds an explicitly attackable warrant with four named assumptions in ν; XD-8 applies FW5:1101/1105 (enabling conditions, universal-class domains) to attention allocation, which FW5:605 addresses separately and permissively. Three fail on the spec side: XD-2 reads §4's labels as pretending to be bearing verdicts when §0 L32-33, §4 L229, §5 N1 and §17 L578/L582 all say they are att/dep bookkeeping; XD-3's claim that the carrier-vs-content case is absent is contradicted by §6 L261, §10.7 L401 and §10.4 L386's verbosity probe (and by the critic's own XD-6 evidence); XD-7 treats V's three-valued codomain as a ceiling on the programme's status vocabulary when §1 L86-88's sandbox_abort is the spec's own out-of-band pattern. Two findings additionally strawman §17: XD-6 presses an objection §17 L580 states first, and XD-1 uses L578's unrelated §11 concession to allege a non-concession about reach. Every proposed instrument (I-1 through I-5) survives as programme policy; what does not survive is the claim that FW5 licenses them against the spec in the form given. Corrected findings supplied for all six.

### XD-1

**Finding id.**

XD-1

**FW5 claim.**

FW5:1218 "Then no function of \(P(M)\) alone agrees with the accounting predicate on both models." and FW5:1222 "The same argument applies to attribution from identical emitted text and to semantic use inferred from delivery logs." Reinforced at FW5:152 "It is not a host's claim that the token was supplied to a prompt" and FW5:332 "Endpoint agreement establishes neither identity of active causes nor identity of contributors."

**Spec mechanism.**

§6 Reach, L269: "the event log timestamps what an artifact was built for, so 'accounts for something it wasn't built for' is verifiable in the trace"; §10.5 Holdout, L393: "timestamps in the log prove the artifact predates the evidence — Lakatos's novel-fact criterion, mechanized."

**Verdict.**

hinders

**Argument.**

The spec's strongest informal-side evidence type is temporal priority read off a delivery log. FW5's projection theorem (1208-1224) is precisely the claim that a record of what was emitted and when cannot decide the accounting predicate, and 1222 names delivery-log inference as an instance. A timestamp shows that bytes existed before other bytes; it does not show that the later contribution's organization depends on the earlier content rather than on material both shared. The spec's own §17 L578 concedes the gap in the adjacent case ("it forces variation, which is not the same as producing a creative conjecture") but never applies the concession to reach. For H005 this matters because every arm's artifacts are timestamped and hash-chained already: adopting the spec's criterion would let the study mint reach hits out of custody metadata it built for a different purpose.

**Repository evidence.**

/home/user/miniReason/docs/reviews/reason-use-route-identifiability.md establishes the same point empirically for E016-E020: matched direct and Mini "implement the same conditional policy for messages delivered to the provider" and therefore "permit the same model-output traces"; ROUTE-D1 chose to "Compare actual provider payload construction rather than arm names or archived Mini briefs." /home/user/miniReason/docs/LANGUAGE_PROPOSAL_THEOREMS.md:101-109 (LP-09) states the theorem form. /home/user/miniReason/docs/reviews/configuration-space-and-ecs-gaps-2026-09-12.md:20: "More samples from equivalent policies do not identify a Mini-specific reasoning input."

**Testable consequence.**

INSTRUMENT I-4, "payload-difference precondition" (offline on existing evidence, then prospective). Inputs: the frozen /home/user/miniReason/experiments/diagnostics/H005-open-prose-commitments/occurrence-01/requests/*.json bytes for every coordinate in a chain, pinned by attempt/receipt sha256 as the importer's verify_custody already does. Procedure: for each pair of nodes the design claims are a route contrast (fork5 objection vs rival; weave7 body_route vs commitment_route), diff the two delivered payloads and record, in prose, which represented distinction is present in one and absent in the other; a difference in field names, artifact labels or node headings does not count. Evidence for a real contrast: a distinction the design says the routes differ about is literally absent from one payload. Evidence against: the payloads differ only in labels, in which case the chain carries no route contrast and any downstream difference is sampling. Offline now for cycle01/daily (fork5 ran); weave7 and return6 need new occurrences. Claim ceiling: this is a precondition, not evidence of use — passing it establishes only that the comparison contains the proposed difference, exactly the ROUTE-D1 claim level, and never that the model used it.

**Proposed change.**

Delete the spec's timestamp-as-novel-fact criterion from anything the programme adopts (§6 L269 sentence, §10.5 L393 sentence). Replace it with I-4 as a gate on chain design: no H005 chain may be described as containing a route contrast, and no reach or return claim may be made, until the payload diff is published. Record the result as a custody fact alongside delivery_status, never as a semantic verdict.

**Confidence.**

0.85

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

Both the quotation and the mechanism are misused. (a) FW5. The critic cites FW5:1218/1222 but stops one line short of the theorem's own scope note at FW5:1224: 'The theorem identifies missing information in a projection. It does not say that no physical or organizational evidence can ever establish the distinction.' And the neighbouring result at FW5:1238 says in terms: 'record-state equality does not entail equality of semantic satisfaction without the relevant application premises. This is compatible with reliable checks of narrower record facts.' Temporal priority of an artifact over sealed bytes is exactly a narrower record fact. FW5:1222's named instance is 'semantic use inferred from delivery logs' — inference of use FROM the log. (b) Spec. The spec does not infer use from the log. §10.5 L393's reach hit is 'Pass on held-out material' — the artifact's own skeleton commitments instantiated and evaluated at Reveal ('evaluate (program where possible, anchored-rubric otherwise)'); the timestamp does only the anti-fitting job of showing the artifact was not built against the evidence. Likewise §6 L269 opens 'Periodic budgeted cross-evaluation of accepted artifacts against other problems' criteria' and closes 'Reach tracks coupling (Prop 4.1), asserted as a modelling commitment (attackable), not a proven bound.' The clause the critic quotes verifies the 'wasn't built for' half in the trace; the 'accounts for' half comes from the cross-evaluation, not the timestamp. So 'the spec's strongest informal-side evidence type is temporal priority read off a delivery log' is not the spec's mechanism, and 'mint reach hits out of custody metadata' does not follow. The §17 move is also weak: L578 is about §11 forcing variation, an unrelated clause, and a concession made elsewhere is not evidence of a non-concession here.

**Refuter — Corrected finding.**

Narrower and differently grounded: the spec's reach notion is a pass on other problems' criteria, which is not FW5:383's reach (an unchanged organizational core participating in an account of another question 'through a stated anchor and additional background' — the new bridge being itself content). Verdict should be 'absent-in-spec' for the stated-anchor requirement, not 'hinders' for the timestamp. §6 L269's phrase 'verifiable in the trace' should be rewritten to say the trace verifies scope-of-construction only, never the accounting. I-4 (payload-difference precondition) is worth keeping on its own merits as a custody gate, but it is not licensed by deleting §10.5's priority criterion, which is a legitimate narrow record check under FW5:1238.

### XD-2

**Finding id.**

XD-2

**FW5 claim.**

FW5:611-620 "\(\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal E_c,p_\delta)\)" with FW5:622 "A criticism occurrence can exist when (K1) is false. Its grounds may be mistaken, its target misidentified, its inference invalid, or its relevance wrong." And FW5:690: "an interpretation of its reasoning must not silently lose its actual dependencies."

**Spec mechanism.**

§4 L206-229 two-pass grounded adjudication and its four labels; L229 "**Inputs to adjudication are `att` and `dep` ONLY.**"; L210-211 the grounded fixpoint (unattacked ⇒ accepted); L226 "orphaned ≠ false."

**Verdict.**

hinders

**Argument.**

Grounded semantics answers "who was attacked and by what" and calls an unattacked node accepted. FW5 makes bearing an Account of the defect-question — anchoring, fidelity, question fidelity, non-circular dependence, non-vacuity at the defect's own respect — none of which is a graph property. So the label is not a weakened bearing verdict; it is a different object that reads as one. The split is already made concrete in this repo: the importer's ACCEPT_BY_POSITION wording says an unattacked H005 artifact is accepted only because "no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised" — and in the golden scope A_rival is reinstated purely because A_carry happened to attack A_response, with the note "One cycle of fork5 has no more criticism in it." The *index* underneath the labels is, however, exactly what FW5:690 demands be preserved: which record alleged what defect against which passage, and which records the author declared they would take up.

**Repository evidence.**

/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/importer/docs/design/h005-import-notes-2026-09-14.md §2.1, §3 (golden graph: 7 warrants, |att|=4, 14 accepted / 3 refuted; "still position-determined"), invariant I7 "no label here is a semantic attribution, and root alone interprets substantive output". §2.3: refs 84, resolved 82. §6.6: daily/mini_fcl/cycle01/rival declares uptake = ["r2","r6","r7","r9"], so claims r1, r3, r4 "were reported by nothing at all" — hence claim_record_unmapped (15). Also commitment_record_not_in_uptake (2: rival.r10, r11); uptake_refs_unmapped (32). /home/user/miniReason/experiments/diagnostics/H005-open-prose-commitments/PROTOCOL.md:62 "Root alone reviews substantive outputs."

**Testable consequence.**

INSTRUMENT I-1, "uptake-divergence ledger" (fully offline on existing evidence; the import's graph used ONLY as a lookup). Inputs: the five daily/mini_fcl/cycle01 FCL-1 documents; the importer's side_table.json records[] and validity_nodes (target id, target kind, carrier) used purely as an index of which record targets which artifact; each node's declared `uptake` array; the exposed views in material.json; no labels, no att, no accepted/refuted. Procedure: for each targeted pair (objection record -> target passage), root reads the targeted passage, the objecting record's own text, and the later node's body, and writes one paragraph: what defect was alleged, at which respect, what the later node's text now commits to, and whether any *other* exposed material would equally account for that change. Then the three divergences are read separately: records the author declared in uptake but whose target this import could not resolve (uptake_refs_unmapped, 32); commitments the author made but left out of uptake (rival.r10, r11); claims outside uptake entirely (r1, r3, r4). Evidence for content-dependence: a later commitment changes in a way that only the objection's content distinguishes, and the sibling branch that saw a different view did not make it. Evidence against: the same change appears in the branch that never saw the objection, or tracks position (last node) rather than content. Claim ceiling: one problem, one template, one cycle, one provider; produces at most a finite attributed account of a particular change, in PROTOCOL.md:62's own terms. It is not a reason-use witness — FW5:628 requires a structural map into an active response suborganization, and a transcript cannot supply one (FW5:634: the attribution is then unresolved, not negative).

**Proposed change.**

Keep the importer; forbid its labels from entering any H005 reading. Concretely: add to the import's I7 banner the standing rule that `label0`/`final_labels` are not to be quoted in a root review at all, and publish a labels-free projection (records, targets, uptake, residue) as the artifact root actually reads. Do not adopt §4's adjudication as an instrument; adopt only its dependence bookkeeping.

**Confidence.**

0.8

**Refuter verdict.** stands: false, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

The FW5 quotations are exact (611-620, 622, 690) and the underlying observation — grounded labels are not Bearing — is correct. But the verdict 'hinders' attributes to the spec a claim it explicitly disclaims, so the finding is a strawman of the spec's own §0/§17. §0 L32: 'Status is computed, never stored as ground truth.' §0 L33: 'Measures never adjudicate.' §4 L229 (the critic's own quotation): 'Inputs to adjudication are att and dep ONLY.' §5 N1 L233: 'No artifact ... is ever marked final.' §17 L578: the spec 'Guarantees faithful bookkeeping (statuses, reinstatement, no relapse, replayable trace). Does not manufacture good conjectures.' §17 L582: '§10 does not make informal verdicts reliable.' An att edge exists only where an artifact 'carries a warrant against a target' (§0 L30), so 'accepted' means precisely 'no surviving warranted attack in this graph' — which is verbatim what the critic's own ACCEPT_BY_POSITION evidence says. The spec and the importer agree; there is no hindrance to rebut, only a limit the spec states itself. A reader who mistakes label0 for a bearing verdict is violating §0, not following §4.

**Refuter — Corrected finding.**

Reclassify as 'absent-in-spec' with the helps-half named: §4 supplies dependence bookkeeping that satisfies FW5:690's demand that an interpretation 'must not silently lose its actual dependencies', and supplies nothing that evaluates Bearing (FW5:611-620), because no spec mechanism checks anchoring, question fidelity, non-circular dependence or non-vacuity of a criticism's own account — the rubric-verdict guard (§3 L197-204) screens procedurally (referential integrity, order-swap, paraphrase) and never semantically. The proposed change (labels-free projection; adopt only the dependence index) survives unchanged; it is a programme hygiene rule, not a correction to the spec.

### XD-3

**Finding id.**

XD-3

**FW5 claim.**

FW5:630 "Its contrast contract must include a content-changing case, a content-preserving recoding, and the distinction between a change in the objection and an irrelevant carrier disturbance wherever those distinctions are claimed. These are semantic comparisons, not a mandatory battery of physical tests." With FW5:601: the response subnetwork "must also have a nonconstant dependence on the relevant represented distinction under its declared contrasts."

**Spec mechanism.**

§10.4 Judge audits, L383-384: "**Paraphrase invariance:** re-run logged rulings on variator paraphrases; flips are hits" and "**Premise-deletion sensitivity:** delete the cited `decisive_point` from the transcript; the verdict SHOULD flip; a verdict that survives the removal of its own stated grounds is easy to vary."

**Verdict.**

helps

**Argument.**

These two probes are, structurally, two of FW5's three required contrast cases, and the spec gets both directions right: invariance expected under recoding, change expected under content deletion. That is a genuine contribution the programme does not currently have as a design. Two defects. First, the spec aims them at the *judge* — an apparatus FW5 has no use for, since no approval event creates an account (FW5:244) — rather than at the deliberative transition the programme actually wants to characterise. Second, FW5's third case is absent: the spec nowhere distinguishes a change in the objection from an irrelevant carrier disturbance, and without it a system that merely reacts to any perturbation passes both probes. H005 has already produced an accidental carrier disturbance, so the third case is not hypothetical.

**Repository evidence.**

/home/user/miniReason/docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md:26,30: the matched arm's returned JSON carried raw newlines, strict json.loads raised, and "the commitments are absent by contract, not because the model omitted them"; reading commitments_sha256 = e3b0c442… at face value "would score an encoding fault as an arm that declined to commit". Confirmed in the artifacts: matched/cycle01/response.json and carry.json both have envelope_status OPAQUE and empty commitments; importer commitment_surface_state = unavailable_decode_failure, opaque_envelope count 2. /home/user/miniReason/docs/reviews/reason-use-design-audit.md already demonstrates the recoding half: a line-by-line correspondence table over R with two named corrections ("tied-holds and over-capacity" → the exact subjects; "refusal to infer" → "refusal to assert"), i.e. the repo has a worked method for certifying a recoding content-preserving before it is used.

**Testable consequence.**

INSTRUMENT I-2, "three-case contrast triple at one node" (one case testable offline now; the other two need new occurrences). Inputs: one frozen objection artifact O with an identified target; a recoding recode(O) certified by a published correspondence table in the reason-use-design-audit form, frozen before any response is obtained; a carrier variant carrier(O) with identical content and perturbed carriage (field order, whitespace, FCL record ids renamed, prose/FCL surface swapped at fixed content); and a no-objection control. Procedure: deliver each to the same successor node under otherwise identical payloads (verified by I-4), then root writes, per condition, which commitment the successor changed and against what. Evidence for content-dependence: the successor's operative commitment differs between O and control, does not differ between O and recode(O), and does not differ between O and carrier(O). Evidence against: any difference under carrier(O) alone, or none under O vs control. OFFLINE NOW, partially: the matched arm's decode loss is an unplanned carrier disturbance on two coordinates (response, carry) whose downstream views differed from mini_prose's while the authored content did not; root can read those two coordinates today and report whether the successor's commitments track the lost surface or the retained body. That is one cell of the triple, n=2, with the carrier change uncontrolled. Claim ceiling: one system, one problem, one respect; the profile is consistent-with, never a witness (FW5:628), and an unresolved cell stays unresolved (FW5:634). A single frozen recoding is "evidence about this particular expression change only" (reason-use-design-audit).

**Proposed change.**

Adopt §10.4's two probes, re-targeted from judges to responder nodes, and add FW5's missing third case as a first-class arm. Write the triple into PROTOCOL.md's contrast declaration for any cycle that claims reason use, so the three cases are frozen before the cycle runs (FW5:787: "they must not shift inside its assessment"). Do not adopt the rest of §10.4 (planted-flaw error rates, bias probes) — those are rate measures over a judge, which FW5:851 refuses as warrants.

**Confidence.**

0.75

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The 'helps' verdict is right and FW5:630/601 are quoted exactly, but both stated defects fail. Defect (b) — 'the spec nowhere distinguishes a change in the objection from an irrelevant carrier disturbance' — is false twice over. §6 L261, which the critic themselves endorse in XD-6: 'µ MUST substitute at role level ... not merely reword ... Rewording-only µ measures phrasing rigidity and is declared insufficient for D5.' §10.7 L401 restates it normatively: 'Rewording-only variation is banned as the sole kernel for skeleton content.' And §10.4 L386's verbosity probe is the control case in the required direction: 'verbosity pairs (same content, padded vs. terse)' — a carriage change at fixed content whose effect on the verdict is measured and logged as bias. That is FW5's third case aimed at the judge. Defect (a) — 'a judge is an apparatus FW5 has no use for, since no approval event creates an account (FW5:244)' — misreads 244, whose second sentence is 'An investigator's successful argument for their existence is evidence for the attribution, not its truth-maker by decree.' FW5 makes assessors evidence-producers, and FW5:847 makes an argument for a choice ordinary criticizable content. The spec's judge is exactly that: rulings register as attackable, reinstateable artifacts (§10.6 L397 'Appellate, not oracle'; §10.3 standards attackable with closure collapse).

**Refuter — Corrected finding.**

Keep verdict 'helps' and keep the re-targeting proposal, but on the correct ground: §10.4's two probes plus §6 L261/§10.7's rewording ban already instantiate all three of FW5:630's cases against the judge; what is absent is any application of the triple to the responder node — the deliberative transition FW5:626-628 actually defines reason use over. The finding's real content is a scope gap, not a missing case. I-2 stands as written; drop the claim that FW5 has no use for a judge and the claim that the carrier case is missing from the spec.

### XD-4

**Finding id.**

XD-4

**FW5 claim.**

FW5:791-797 (P): "\exists o\in O\,[\neg o(\xi)\land o(\xi')]\ \land\forall r\in P\,[r(\xi)\Rightarrow r(\xi')]\ \land\operatorname{ProducedBy}(\Delta,\xi,\xi';O)"; FW5:802 "Losses outside \(P\) must be exposed. The result is local progress, not an all-things-considered verdict"; FW5:808 the trivial-gain/main-loss case; FW5:810 "progress need not increase the number of accepted claims."

**Spec mechanism.**

Whole spec. The only removal-shaped mechanisms are §4 L226 ("Refuting a premise ⇒ dependents become `suspended_unsupported`, NOT `refuted`"), §3 L189-195 anti-relapse, and §11.7 L469 ("an artifact off the frontier is merely unfunded, not demoted"). §7 L318 rent rule gates Spawn only. No protected-obligation set, no loss register, and §17 L576-588 does not list the omission.

**Verdict.**

absent-in-spec

**Argument.**

Every spec mechanism is additive: register, attack, spawn, fund. Refutation removes standing but the spec explicitly declines to read orphaning as loss, and nothing anywhere records that a previously achieved thing stopped holding. FW5's progress criterion is the conjunction of a gain with the *survival of a declared protected set*, plus an exposure duty for losses outside it — and FW5:810 makes the decisive case that progress can be a net withdrawal. A programme instrumented only with the spec's vocabulary literally cannot state the H004 finding it already has (a correction retained alongside the criticism it should have withdrawn). This is the sharpest absence on this axis, and the repo has the evidence to exercise the missing instrument today.

**Repository evidence.**

/home/user/miniReason/experiments/diagnostics/H004-partial-language-continuation/REPORT.md: "WHL conversion18 falsely calls its complete cycle17 input a truncated prefix. Conversion19 states that input was complete while retaining the criticism about its supposedly missing ending" — a flipped O with a surviving defect; and the positive case "cycle18 correctly notices that a sentence classified as truncated by cycle17 is actually complete; cycle19 retains that correction." Also "identifying the disagreement does not ensure correct use of it." PROTOCOL.md:62 already names the unit in FW5's terms: "what was alleged, what grounds were available, what subsequent use actually changed, what remains disputed, and what useful commitments were lost." /home/user/miniReason/docs/SEMANTIC_GUIDE.md:28 requires "protected prior successes remain"; :43 forbids changing protected obligations after adverse evidence.

**Testable consequence.**

INSTRUMENT I-3, "loss ledger" — the instrument that ignores the spec entirely (its vocabulary is FW5's (P) and nothing else). Inputs: for a given chain, two situations ξ (end of cycle n) and ξ' (end of cycle n+1) as the frozen artifact sets; a set O of failed obligations alleged in cycle n, written as prose predicates over readable artifacts; a set P of obligations already satisfied at ξ that must survive, written in the same form — both published before cycle n+1 is dispatched, as one file with a sha256 pinned in the plan. Procedure: after cycle n+1, root evaluates each o and each r by reading, records satisfied/violated/unresolved per predicate with the passage cited, then writes separately every loss observed that is in neither set (FW5:802) and a construction account connecting the change to a particular content (ProducedBy, FW5:800 — "not satisfied by temporal succession alone"). Evidence for a repair: some o flips, every r in P still holds, and the account names the binding. Evidence against: any r fails (no (P) even if o flipped — the FW5:808 case), or the only connection available is succession. NEEDS NEW OCCURRENCES for a repair claim, because P must be prospective. OFFLINE NOW as calibration only: run the whole procedure retrospectively over the H004 conversion18/19 pair and over the daily fork5 account→objection→response→carry chain, and publish the result explicitly labelled as an instrument dry run whose pre-declaration condition is violated, therefore establishing nothing about repair. Claim ceiling: local progress on one comparison; "not an all-things-considered verdict" (FW5:802); a retrospective run establishes nothing at all.

**Proposed change.**

Add I-3 to PROTOCOL.md as a required pre-dispatch artifact for any cycle whose purpose is a repair claim: a published O/P file with sha256 pinned in plan.json, and a post-cycle loss ledger with a mandatory "losses outside P" section that must be present even when empty. Take nothing from the spec here; it has nothing to take.

**Confidence.**

0.8

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

I could not refute this. FW5:787-797, 802, 808, 810 are quoted exactly, including 'Losses outside P must be exposed' and 'progress need not increase the number of accepted claims'. A full-text search of the spec for protected/loss/withdraw/regress vocabulary returns only §10 L342 ('a lossy summary cannot corrupt a verdict') and §17 L584 ('meta-attractor regress') — neither is a loss register, neither is a protected-obligation set, and §17 L576-588 does not list the omission, as claimed. The two candidate rebuttals both fail: §11.7's criteria-coverage Pareto axis keeps a lower-coverage successor from displacing a predecessor in FUNDING only ('Never a status; an artifact off the frontier is merely unfunded'), and §0 L32's 'Nothing is deleted' preserves artifacts, not the achievements they realized; neither fixes O and P before a comparison, neither supplies ProducedBy (FW5:800: 'not satisfied by temporal succession alone'), and neither imposes an exposure duty. Two minor blemishes that do not touch the verdict: §4 L226 ('orphaned ≠ false') and §11.7 L469 are refusals to OVER-read a status, not refusals to record loss — FW5:686 endorses the first of those refusals in terms; and the programme is not in fact 'instrumented only with the spec's vocabulary', since SEMANTIC_GUIDE.md:28 already states (P) almost verbatim ('At least one failed obligation becomes satisfied; protected prior successes remain; the contribution produces the change', excluding 'temporal succession or undisclosed losses'), so I-3 formalizes an existing programme commitment rather than importing a new one.

**Refuter — Corrected finding.**

### XD-5

**Finding id.**

XD-5

**FW5 claim.**

FW5:1202 "Suppose all carriers, component relations, role bindings, maps, histories, question contracts, and attribution indices are transported along bijections preserving their structure. Then the truth of (E), (G), (P), and (EK) is preserved"; FW5:1206 "The result does not apply to arbitrary compression, loss of event identity, a changed boundary, or a coarsening that identifies a relevant distinction"; FW5:381 "splitting one feature into ten cannot create knowledge."

**Spec mechanism.**

§3 L193 battery-equivalence `≈_B` (Def 3.5) as the identity criterion for explanations; §6 L253-259 "Count only inequivalent survivors (a rename is the same explanation)"; §17 L582 "`≈_B` in informal domains is irreducibly judgment-laden."

**Verdict.**

helps

**Argument.**

The spec is right that an instrument needs a declared sameness relation and right that it must be stated and attackable rather than assumed; §17 L582's admission is honest. But `≈_B` is extensional — same verdict vector over a battery — which is exactly the identity criterion FW5:1206 excludes, since two contents can agree on every battery entry while differing in a distinction the question turns on. The programme's own instruments have an untested version of the same problem, and it is currently invisible: the importer's open questions record that the graph shape depends on which scope was imported and on which criticisms happened to be reified earlier. That makes a scope choice — an experimenter's bookkeeping decision — capable of changing what a reader would take the episode to show, which is the split-features failure at FW5:381 in a new dress.

**Repository evidence.**

importer notes §6.7: "Two importers, one occurrence, different scopes produce different artifact ids for the same node when the ref set differs… 'the spec id of daily/mini_fcl/cycle01/carry' is only well defined relative to a scope." §6.4: "Criticism-of-criticism retargeting is order-sensitive by construction… it means the shape of `att` depends on the scope imported. A scope that excludes the rival would change where `n3`'s attack lands." §2.2: the prose/FCL dispatch change "removed 10 spurious parse_failure entries" — i.e. a carrier-classification decision moved 10 residue entries. /home/user/miniReason/docs/SEMANTIC_GUIDE.md:57: "Reach or edit-survival counts supply no numerical warrant."

**Testable consequence.**

INSTRUMENT I-5, "grain and scope invariance probe" (fully offline on existing evidence). Inputs: the same H005 occurrence-01, imported at two scopes (single-arm golden scope; full 17-coordinate occurrence); plus one hand-made coarsening of a single commitment surface in which n FCL records with the same target are merged into one record with the same prose content, and one hand-made splitting in which one record is divided into three, neither touching the body. Procedure: for each variant, produce the labels-free projection of I-1 (records, targets, uptake, residue codes with units) and have root write the same one-paragraph reading of one fixed pair. Compare readings, not counts. Evidence that the instrument is sound: the reading is unchanged under the splitting and the merging, and any change under the scope change is confined to pairs the narrower scope does not contain. Evidence that it is unsound: the reading of a pair present in both scopes changes; or the merge/split changes which criticism is taken to bear — in which case the instrument measures the partition, and FW5:381 rules it out as evidence. Claim ceiling: this tests the *instrument*, never the model; a pass says the reading survives a recoding, not that it is correct. A coarsening that does change the reading is informative and permitted (FW5:1206 does not promise invariance under coarsening) — what is forbidden is reporting a reading whose grain was never declared.

**Proposed change.**

Adopt the spec's discipline (declare the sameness relation, make it attackable) and reject `≈_B` as its content. Require every H005 reading to name its grain and its import scope in the same sentence as the claim, and require I-5 to be run before any import-assisted reading is published. Add the merge/split variants to the importer's offline test suite as an instrument-validity check, not as evidence.

**Confidence.**

0.7

**Refuter verdict.** stands: true, misreads_fw5: false, misreads_spec: false

**Refuter — Rebuttal.**

The strongest case against is that FW5:1206 does not 'exclude' an extensional identity criterion — it states the equivariance theorem's scope ('The result does not apply to ... a coarsening that identifies a relevant distinction'), i.e. it promises no invariance rather than forbidding the coarsening. But FW5:154 supplies the missing step directly ('A genuine recoding is an isomorphism of the retained structure at that grain. Coarsening is not automatically an isomorphism'), so the conclusion survives the wording quibble. The second possible rebuttal — that the spec does not actually treat ≈_B as an identity criterion — in fact supports the critic's own 'helps' verdict and proposed change: §7 L307 parks '≈_{B₀} adequacy as equivalence surrogate' in the validity node as an explicitly attackable assumption, and §17 L582 concedes '≈_B in informal domains is irreducibly judgment-laden'. That is exactly 'declare the sameness relation, make it attackable', which is what the critic proposes adopting. The FW5:381 analogy to import scope is looser than the rest (381 is about re-partitioning a description under a hard-to-vary verdict, while the importer's scope-dependence is about artifact identity), but the critic signals this as an analogy ('in a new dress') and the programme-side risk it names is real and documented in the importer's own §6.4/§6.7.

**Refuter — Corrected finding.**

### XD-6

**Finding id.**

XD-6

**FW5 claim.**

FW5:212 Non-vacuity: "A contrast family containing only notational variants, or one defined to exclude every change that could matter, does not meet non-circular dependence." FW5:381: hard-to-vary "is an articulated pattern of constrained changes, relative to an explanatory job… Nor is it a numerical warrant." FW5:438: "the complete answer can remain the uncertainty set \(f[Z_y]\)."

**Spec mechanism.**

§6 L251-261 HV: "`s(a) = Pr[ a' passes B(a) ∧ a' ≉_B a ]`, `HV_B(a) = 1 - s(a)`" with §6 L261 `µ_struct`: "µ MUST substitute at role level — swap the mechanism, the motive, the causal link, the scope — not merely reword. This is the Persephone test." §7 L286-316 `hv-floor` packaging a fail as a demonstrative warrant.

**Verdict.**

hinders

**Argument.**

Split verdict, and the split is the useful part. `HV_B = 1 - s(a)` is a survivor frequency and therefore precisely the numerical warrant FW5:381 and FW5:851 refuse; §7 then lets that frequency produce a `refuted` label identical to a demonstrative one, which the programme's prohibitions already outlaw (AGENTS.md:15, SEMANTIC_GUIDE.md:59). So the measure must go. But the *edit kernel* under it is a genuinely FW5-shaped generator: role-level substitution of mechanism, motive, causal link and scope is a recipe for constructing the content-changing case FW5:630 demands, and the Persephone test is close to FW5's non-vacuity probe at 212 — a contrast family in which any filler passes is one "defined to exclude every change that could matter." The repo has no such generator; its contrasts are hand-built per study (the skew-matrix challenge's three removals, the E016-E020 criticism variants).

**Repository evidence.**

/home/user/miniReason/docs/reviews/FW5-account-skew-matrix-challenge.md:13 fixes admitted contrasts in advance — "remove skew-symmetry, remove oddness, or both; the two removals commute" — a hand-built role-level family, exactly what µ_struct automates. /home/user/miniReason/docs/SEMANTIC_GUIDE.md:57: FW5 "allows nonmonotone, redundant and infinitary support families… Reach or edit-survival counts supply no numerical warrant." /home/user/miniReason/docs/LANGUAGE_PROPOSAL_THEOREMS.md:161 (LP-15): adding an active commitment can empty the solution intersection — the non-monotone case a survivor frequency averages away.

**Testable consequence.**

Fold the kernel into I-2 rather than building a sixth instrument: use µ_struct's four substitutions (mechanism, motive, causal link, scope) to generate the content-changing variants of a frozen objection, and report the outcome as a *set* of surviving variants with root's reading of each — the FW5:438 uncertainty-set form — never as ŝ, HV_B, or a pass/fail against HV_MIN. Decisive observation for the FW5 side of the split: take one H005 objection, generate k role-level variants, and check whether any single variant changes the successor's operative commitment while the aggregate survivor fraction stays flat. If it does, the frequency and the reading come apart on the same evidence, and the frequency is the thing to drop. Offline now only in weak form (the variants must be delivered, so new occurrences are needed); offline today one can at least apply the Persephone probe to the existing daily commitment surfaces by substituting the flatmates, the chore and the schedule and asking whether the authored commitments still read as stated — a vacuity check on the contrast family, not on the model.

**Proposed change.**

Adopt §6 L261's `µ_struct` substitution recipe as a contrast generator inside I-2. Reject `s(a)`, `HV_B`, `HV_MIN`, and the whole of §7's `hv-floor` (the criterion/gate distinction at L288 does not rescue it: a frequency that mints a `refuted` label is adjudicating). Add the Persephone substitution as a standing vacuity check on any frozen contrast family before a cycle runs, reported as satisfied/violated/unresolved per FW5:212, never counted.

**Confidence.**

0.7

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The µ_struct half is sound and the quotations at FW5:212/381 are exact. The rejection half misreads both documents. (a) FW5:851 reads: 'No quantity of endorsements, surviving tests, repeated observations, or partitioned features enters (G), (P), or (EK) as an AUTOMATIC warrant. Mathematical counts can appear inside an explanation of a particular counting problem or a physical resource condition. THEY ARE NOT OUTLAWED AS INFORMATION.' The critic drops 'automatic' and drops the permission sentence. What §7 constructs is the opposite of automatic: L307 packages the fail as a demonstrative warrant carrying a validity node ν asserting four named, attackable assumptions (kernel fairness, k sufficiency at the decision margin, ≈_{B₀} adequacy, B₀-for-B adequacy), with the canonical reinstatement attack spelled out. (b) The critic's argument nowhere engages §17 L580, which concedes precisely the point being pressed: 'HV at k≈8 is a spot-check, not a measurement. The hv-floor verdict is program-computed but stands on LLM-dependent assumptions ... parked in its validity node: visible and attackable, not eliminated.' Pressing an objection the residue section states first is a strawman of §17. (c) The changelog at L23 records that the HV_MIN ACCEPTANCE GATE was already removed in v1.1→v1.2 for the critic's reason, with 'Measures-never-adjudicate invariant added' — the surviving hv-floor is scoped to connection problems only (L316: 'the floor is a property of connection problems, not of relation artifacts'). (d) The equation of a spec graph status with an FW5 predicate is unargued: 'refuted' in §4 is bookkeeping over att/dep, revisable by N1, and is not (G), (P) or (EK). FW5:438 is also used analogically — it is about measurement fibres and identifiability, and licenses reporting an uncertainty set but does not prohibit a frequency.

**Refuter — Corrected finding.**

Verdict should be split explicitly rather than delivered as 'hinders'. Helps: §6 L261 / §10.7 L401's µ_struct role-level substitution kernel is an FW5-shaped generator of FW5:630's content-changing case and a mechanized form of FW5:212's non-vacuity probe; the programme has no such generator. Absent/limited: nothing in §7 supplies an Account-level check on the criticism the fail verdict carries. The programme-policy recommendation (report the surviving variant set with root's reading, not ŝ, and never let a frequency drive a programme status) can stand on AGENTS.md:15 and SEMANTIC_GUIDE.md:57, which are stricter than FW5:851 — but it must not be presented as FW5 refusing the spec's construction, because FW5:851 refuses automatic warrants and §7 builds an attackable one.

### XD-7

**Finding id.**

XD-7

**FW5 claim.**

FW5:688 "Eligibility is a separate predicate… A timeout may instead be evidence about delivery. The inability to evaluate a proposition is not a falsifying observation of the proposition." FW5:508: for a rule query, "Existence, uniqueness, ambiguity, and inapplicability are separate cases." FW5:686: "It does not turn an absent receipt into a negative observation."

**Spec mechanism.**

§1 L77-79 budget honesty: "`overrun` therefore means 'the verdict is unobtainable within the declared deterministic budget' … never 'the machine was slow'"; §1 L80-88 oracle isolation: "A containment kill produces no epistemic verdict and MUST NOT mint a warrant… it is outside `V` and must not be written as evidence"; §7 L305-307 "`overrun` packages no warrant; only `fail` does."

**Verdict.**

helps

**Argument.**

This is the one spec mechanism that is FW5-concordant on its own terms and already cited approvingly in the repo. It gets the semantics right in the way FW5:688 demands: non-evaluability is neither a pass nor a refutation, and a containment event is outside the verdict domain. The limit is expressive: three values cannot carry the case H005 actually produced. An authored commitment surface destroyed in decoding is not pass, not fail, and not overrun — nothing was unobtainable within a budget; the evaluation ran and the input had already been corrupted. FW5:508's four-case vocabulary for a status query is the closer model, and the importer independently converged on five values, which is evidence that three is too few for this evidence class.

**Repository evidence.**

/home/user/miniReason/docs/EXPERIMENT_METHOD.md:93 aligns the two documents explicitly: "V1.3 §1 explicitly says a containment kill must not mint a warrant. FW5 likewise separates failed delivery from content evidence." /home/user/miniReason/docs/TASK_AUDIT.md:65 same. The counterexample: h005-matched-arm-envelope-asymmetry-2026-09-14.md:26,30 — commitments "authored and lost in decoding"; the importer's closed value set commitment_surface_state = read_fcl1 | prose_not_parsed | unavailable_decode_failure | parse_failure | schema_failure, with the renaming from opaque_reason because the old name "invited the reading that the artifact was opaque *because of* something the author did" (importer notes §2.2).

**Testable consequence.**

Offline and already decided by existing evidence: the matched arm's two OPAQUE coordinates are a case that the three-valued vocabulary misclassifies and the five-valued one does not, and the review shows exactly what the misclassification would have cost ("would score an encoding fault as an arm that declined to commit"). A decisive further observation, offline: scan every H005 coordinate's recorded status fields and check whether any reading anywhere in the repo treats a non-COMPLETE delivery or an empty commitments hash as content evidence. Finding none confirms the discipline holds; finding one is a defect to repair. No new occurrences needed.

**Proposed change.**

Keep §1's `overrun` semantics and oracle-isolation rule as the programme's standing wording for delivery-versus-content (they are already effectively adopted). Reject the three-value ceiling: fix the importer's five-valued commitment_surface_state, plus delivery_status and envelope_status, as the recorded vocabulary, and add a one-line rule to EXPERIMENT_METHOD.md that no status value in that set may appear in a semantic reading — which is the FW5:688 point stated once rather than per study.

**Confidence.**

0.75

**Refuter verdict.** stands: false, misreads_fw5: false, misreads_spec: true

**Refuter — Rebuttal.**

The 'helps' verdict and the FW5 citations (688, 686, 508) are correct, and EXPERIMENT_METHOD.md:93 does align the two documents. The 'expressive limit' half misdescribes the mechanism. {pass, fail, overrun} is the codomain of V(κ,c) — the verdict of a COMMITMENT EVALUATION (§1 L78) — not the spec's vocabulary for evidence-class or delivery status. The spec already demonstrates the extension pattern the critic asks for, in the very lines quoted: §1 L86-88 routes containment kills through 'the existing overrun API envelope PLUS sandbox_abort; it is outside V and must not be written as evidence.' A decode failure is a codec fact under §0 L31 ('Content is Σ*: opaque bytes + codec'), recordable as an out-of-band condition exactly like sandbox_abort, and nothing in the spec forbids a five-valued commitment_surface_state alongside V — only its entry into adjudication is forbidden (§0 L33, §4 L229), which is the discipline the critic wants. So 'three values cannot carry the case H005 produced' attacks a ceiling the spec does not impose, and 'the importer independently converged on five values, which is evidence that three is too few' compares two different objects.

**Refuter — Corrected finding.**

Keep 'helps' and keep the proposed change, restated: §1's overrun semantics and oracle-isolation rule are adoptable as-is and are already effectively adopted; the H005 envelope case is not a counterexample to the spec but an instance of its own out-of-band pattern (§1 L86-88), and the programme should record commitment_surface_state / delivery_status / envelope_status as evidence-class metadata outside V, with a one-line EXPERIMENT_METHOD.md rule barring any of those values from a semantic reading. Drop the claim that the spec's three-value set is a ceiling on the programme's status vocabulary.

### XD-8

**Finding id.**

XD-8

**FW5 claim.**

FW5:1101 "An enabling condition is inadmissible if its only description is 'the conditions under which the system succeeds.' It must identify physically and semantically meaningful resources and contributions independently of that success claim." FW5:1105 "Both domains are specified independently of the candidate's successes." FW5:244 "No separate approval event creates an account… An investigator's successful argument for their existence is evidence for the attribution, not its truth-maker by decree."

**Spec mechanism.**

§10.6 L395-397: "a **disagreement-ranked queue** (ensemble splits, guard-block streaks, audit hits, maximum-entropy rivalries), never round-robin… the user is the scarce calibration resource and MUST be spent where the machine is most confused"; "**Appellate, not oracle.** … authority is pack ordering, never status privilege."

**Verdict.**

hinders

**Argument.**

The standing half is right and matches the programme: a human ruling is an ordinary attackable artifact, not a truth-maker, which is FW5:244 and the repo's root-only-but-fallible rule. The selection half is the problem, and it is an experiment-design problem the programme has not solved. H005's reading is already selective — H004's review says custody is checked for every call but "semantic review is targeted, not a sentence-by-sentence census" — and no rule says which coordinates root reads. §10.6 would supply one: read where a machine measure is most uncertain. That makes the evidence base a function of a divergence statistic over the candidate's own outputs, which is the structure FW5:1101/1105 forbids when it forbids defining conditions and domains by where the candidate succeeds or fails. The failure mode is concrete: root reads the loud disagreements, and the quiet chains — where a criticism was ignored without contest — are systematically unexamined, which is exactly where FW5:601's dead branch and FW5:632's "refusal with no evidenced or modeled content-sensitive route" live.

**Repository evidence.**

/home/user/miniReason/experiments/diagnostics/H004-partial-language-continuation/REPORT.md: "Custody is checked for every call; semantic review is targeted, not a sentence-by-sentence census of every intermediate response. Missing endings are not assessed as if they existed." /home/user/miniReason/docs/SEMANTIC_GUIDE.md:43: "Changing the question, grain, anchors or protected obligations makes a new claim. It cannot rescue the same assessment after adverse evidence." /home/user/miniReason/docs/reviews/multi-cycle-research-contract-2026-09-14.md:11: "Problem statements must contain no scoring function, grade, target answer, seeded error list or implicit evaluation checklist" — the same prohibition, not yet extended to the reading set. PROTOCOL.md:66: "No fourth/fifth call is justified merely by a desire to obtain a favorable result."

**Testable consequence.**

Offline and decidable on existing evidence: reconstruct, from the published H003/H004 wave reviews, which coordinates root actually read, and check whether the read set correlates with where the arms disagreed or where an error was loud. If it does, the existing findings' coverage is a function of salience and must be reported with that limit; if the read set is closer to a declared census within a frozen slice, no change is needed. Then, prospectively: a pre-registered reading list (e.g. every coordinate of one named chain per problem, plus any coordinate a published falsifier names) makes the coverage of any negative finding — 'root could not identify a single episode in which a warranted criticism changed a later operative use' — mean something, because the episodes searched were fixed before the search.

**Proposed change.**

Adopt §10.6's standing rule (a root ruling is an attackable artifact with no status privilege; it is already the repo's practice) and reject its queue. Replace it with a pre-registered reading set published in PROTOCOL.md before dispatch: name the coordinates root will read in full, allow additions only with a recorded reason and the original list retained, and require every negative finding to state the reading set it was searched over. This is the FW5:1101 admissibility condition applied to the observer rather than to the subject, which is where the programme's remaining vulnerability is.

**Confidence.**

0.65

**Refuter verdict.** stands: false, misreads_fw5: true, misreads_spec: true

**Refuter — Rebuttal.**

The methodological worry is good; the FW5 grounding and the spec reading are both wrong. (a) FW5:1101 governs ENABLING CONDITIONS in a capacity claim ('An enabling condition is inadmissible if its only description is "the conditions under which the system succeeds"') and FW5:1105 governs the DOMAINS 𝔈_Θ and 𝔓^adv_Θ in the universal-class definition. Both constrain the specification of a claim's content, not the allocation of an assessor's attention. FW5 addresses attention separately and permissively at 605: 'Attention is itself an activity in the history. Its organization and the values affecting it are potential criticism targets. The class imposes no maximizing attention function and no rule that the most recent objection receives priority.' FW5 declines to legislate an attention policy and makes attention criticizable — it does not forbid a confusion-ranked one. (b) The conflation is load-bearing: §10.6 L397 ranks by ensemble splits, guard-block streaks, audit hits and maximum-entropy rivalries — disagreement among ASSESSORS, not a measure of where the candidate succeeds. FW5:1101/1105 forbid defining conditions or domains by candidate success; a judge-disagreement statistic is neither. (c) §10.6's queue allocates USER RULINGS as a calibration resource for judges and standards, and is explicitly attention policy quarantined from status (§0 L33; §11 L412 'Everything in this section steers attention ... never status'). Translating it into 'which coordinates root reads for a scientific finding' is the critic's analogy, not the spec's mechanism.

**Refuter — Corrected finding.**

Same proposal, correct citation. The real FW5 constraint on the reading set is FW5:208 — 'The contract ranges over the declared class of changes, including unperformed changes, not merely over the trials on which the candidate succeeded' — together with FW5:787 ('their definitions ... must not shift inside its assessment') and FW5:634 (an unestablished witness leaves the attribution unresolved, not negative). On those grounds a pre-registered reading set published before dispatch is warranted, and every negative finding must state the set it was searched over. §10.6 should be recorded as helps-in-part (the standing rule) and out-of-scope (the queue), not 'hinders': the spec is allocating judge-calibration budget, not defining an evidence base.
