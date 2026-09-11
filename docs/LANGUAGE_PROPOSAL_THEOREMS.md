# Relative expression, candidate languages and Mini

The initial study asks what different representational schemes let Mini express and use under its actual material, time and resource conditions, and how added or removed components help or hinder that process. It does **not** require a proposed language to pass an adequacy gate before it can be studied. Initial proposals are frozen as specimens. Prose, Lean-oriented languages and other semantic classes are legitimate candidates; their particular capabilities and limits remain questions.

The results below are conditional deductions from ECS 2.0's stated relations and elementary constructions. They import no external incompleteness, computability, learning or proof-theoretic theorem. Some are direct consequences of definitions; the counterexamples and preservation arguments do additional work. A proof checker, a model distribution and a faithful translation are engineering assumptions where invoked, not facts derived from ECS. No result certifies creativity.

The supplied [ECS PDF](sources/ECS-2.0.pdf) has missing mathematical glyphs, an incomplete displayed formula in §2.3 and a cropped formula in §3.4; several constructions are retained by reference to an unavailable earlier version. These deductions use the legible accounting clauses and the explicit premises stated here. They neither recover the missing graded formula nor establish an intrinsic variation family from damaged notation. Their labels identify arguments for later reference, not a count of independent discoveries or implemented ECS guarantees.

## Notation and the object being compared

Fix a target question p with organization D, respect, baseline, contrast contract C and obligations, as in ECS §§1.1–1.2. Fix the representation relation, grain ell and system boundary beta before examining the relevant contrasts (§9.4). A representational scheme L supplies possible carriers or descriptions S_L and an interpretation I_L. Its admissible uses may include explanation, criticism, transformation, prediction or execution. Formation and proof rules are optional components: a semantic class need not be an executable grammar or a Lean program.

Let M name the actual Mini arrangement: model endpoint, input ports, rendering, storage, tools, controller, initial state and resource budget B. Distinguish a raw-record route, a model-context route and an execution route. A content may be represented in one without being usable in another.

Write Enc(L,M,B) for contents for which a permitted carrier and interpretation exist on the named route within B. Reach(L,M,B) restricts this to contents an admitted continuation of the presently owned processes can actually produce there. Wit(L,M,B) contains the interpreted contents of occurrences actually observed in the declared trials. All three sets therefore contain contents, not carrier strings. Raw occurrences whose interpretation remains unresolved are retained separately as specimens; they are not silently assigned empty content or excluded from investigation. These are study definitions, not replacements for ECS Understanding, Build, New or Can. Calling an occurrence an expression makes no claim that it is explanatory, originative or true.

A frozen specimen includes the scheme, interpretation, rendering and use rules, model and tool settings, resource conditions, initial inputs and scope. Write its semantic package as P_v=(L_v,I_v,e_v,d_v,registry_v,contract_v), with e_v and d_v denoting any proposed encoding and answer maps, and bind that package to M_v and B_v. Maps can be partial or undeclared in an initial specimen; that is recorded, not repaired by an admission gate. A language file alone does not determine the arrangement.

## LP-01. Witnessed expression establishes a lower bound, not latent capacity

**Assumptions.** Every recorded witness has a valid interpretation on the named route, and the recorded run was an admitted continuation under the declared resources.

**Result.** Wit is contained in Reach, which is contained in Enc. Failure to witness c does not entail that c is outside either larger set.

**Proof.** An actual admitted production supplies the existential continuation required by Reach. That continuation also supplies a permitted carrier, so it supplies the witness required by Enc. Conversely, a carrier can be permitted while the model never emits it; a continuation can be possible while the trials take other continuations. For a concrete counterexample, let the format permit carriers for two distinct contents and let an admitted generator have one possible continuation producing each. A finite trial that takes only the first continuation leaves the second content reachable and representable but unobserved. A different generator with only the first continuation additionally shows that representability need not imply reachability.

This is a direct consequence of the study definitions and ECS's distinction between representation, present repertoire and owned capability (§§1.3, 6.1, 7.2). It prevents a language inventory from being mistaken for a generation result and prevents an unsuccessful sample from being called an expressiveness barrier.

## LP-02. Failing an execution interface does not erase represented prose

**Assumptions.** A retained prose occurrence represents c under P1 at the fixed grain. The host separately attempts to translate another occurrence into an executable program. The failed translation does not alter the retained occurrence or its interpretation.

**Result.** Translation or execution failure does not logically negate that representation of c.

**Proof.** The witness to representation is the unchanged occurrence together with the unchanged interpretation. The failed operation concerns a distinct relation: whether another occurrence supplies an executable realization. Removing that realization leaves the original representation witness intact. ECS §6.1 already distinguishes representation and storage from owned deployment; §5.4 limits what a failed test contradicts.

This does not make the prose correct or explanatory. It establishes that a malformed Lean file, JSON program or other translation cannot be used as a universal semantic rejection of the accompanying conjecture or criticism. An instrument may report an execution failure while preserving that content for continued inquiry.

## LP-03. A collision destroys a distinction on the affected route

**Assumptions.** Two admitted situations x and y require different answers in the fixed respect. A scheme's complete retained representation on a downstream route is e(x)=e(y). That route has no other source of the distinction, and its answer is a single-valued function d of that representation.

**Result.** The route cannot answer both situations correctly.

**Proof.** Equality of its inputs gives d(e(x))=d(e(y)). Correctness for both would make this common value equal to two different required answers, a contradiction. No theorem about every formal language is involved; this is a property of this particular encoding and route.

The result gives a relative loss witness under ECS's question-fidelity and representation conditions (§2.2, P1). It does not require whole-language adequacy as an initial gate. A single declared distinction can be tested after freezing a proposal. If prose or another channel still supplies the distinction, the no-other-source premise fails and the conclusion does not apply to the whole system.

## LP-04. Preserving baseline answers need not preserve contrastive expression

**Assumptions.** Evaluation checks a scheme at a baseline and a single application of an edit a from that baseline, while the intended use also includes the composable edit a followed by a again.

**Result.** A scheme can match the baseline and every tested one-step answer while failing the two-step use.

**Construction and proof.** Let the target state initially be zero, with a taking zero to one and one to two. Let the candidate use agree at zero but send one back to one. Both give zero before the edit and one after a single edit. After two edits, target and candidate give two and one respectively. Thus the tested equalities do not entail equality on the composite contrast.

ECS §2.2's composition and question fidelity are distinct obligations. This construction does not demand arbitrary complex tests first; it identifies a concrete later probe for schemes claimed to express transformations. A language's ability to name the initial state does not establish its ability to preserve the organization under use.

## LP-05. Medium alone does not confer explanatory standing

**Assumptions.** Two occurrences, one prose and one formal, represent isomorphic retained organizations at the fixed grain. The isomorphism preserves the question, anchors, component roles, solution sets, boundary and edit maps, active commitments, their typed restriction operations and admitted contrasts.

**Result.** One satisfies the accounting conditions of ECS §2.2 exactly when the other does.

**Proof.** Transport the structural, composition and question equalities through the isomorphism. The inverse transports them back. A compatible baseline maps to a compatible baseline. The active commitment block witnessing non-circular dependence maps to a corresponding block with the same contrasting answer. Hence every accounting condition is preserved in both directions.

The substantive premise is the claimed preservation of organization; it is not established merely by calling a formal file a translation. The result gives equal semantic legitimacy to equivalent contents without pretending that every prose statement is formalizable, that every formal expression has bearing, or that the two carriers provide identical ease of checking.

## LP-06. A conservative expressive extension preserves old possibilities only under preserved conditions

**Assumptions.** L' contains a carrier for every old L expression, with the same interpretation and admitted use on old contents. The embedding preserves relevant bindings and costs; Mini retains the same access, resource allowance and means of producing old expressions.

**Result.** Enc(L,M,B) is contained in Enc(L',M',B). If the old production continuations also remain admitted with the same effects and costs, the corresponding inclusion holds for Reach.

**Proof.** Take a witness in the old set. Its embedded carrier supplies the same representation within the same budget, proving the first inclusion. For the second, reproduce the old owned continuation through the stipulated embedding; its resulting occurrence supplies the old content in the new arrangement.

The added premises matter. Keeping old strings syntactically legal while changing their meanings, removing their producing tool or charging more than B does not preserve the witness. This is conditional preservation, not the claim that adding vocabulary always helps a running model.

## LP-07. More possible expressions does not imply better finite generation

**Assumptions.** L' conservatively extends L as in the first part of LP-06. The generator or scheduler can change when the extended description is supplied.

**Result.** There is no general implication from increased Enc to more successful witnessed expressions or more creative episodes within a fixed run budget.

**Construction and proof.** Let L permit a carrier for a useful content c and let its generator emit that carrier on the only funded call. Extend L with a carrier for a distinct content d, formerly outside Enc, while preserving the carrier and interpretation for c. Let the new conditioning or scheduler emit the carrier for d on that call, where d does not address the current task. The set of possible contents grows, while the witnessed task-relevant content disappears. Both arrangements satisfy the stated extension premise.

This is a counterexample to monotonic improvement, not an empirical prediction that expansion usually hurts. ECS §9.3 supplies no merit function that could turn vocabulary size into a warrant. Whether a particular component broadens useful search or distracts it is a comparative experiment.

## LP-08. A larger language description can remove operative distinctions through context limits

**Assumptions.** A renderer has a fixed input budget and truncates or excludes content when a language description grows. A relevant distinction formerly supplied to the next call is thereby removed, and no other route supplies it. The downstream answer map is single-valued as in LP-03.

**Result.** The extension can reduce effective task expressibility even if its abstract language is conservative.

**Proof.** Choose x and y differing only in the removed content, with different required responses. Before expansion their rendered inputs differ. After expansion they coincide. LP-03 then forbids the downstream route from preserving both answers. The loss follows from the material rendering arrangement, not from the language's abstract syntax.

This is an architecture-level reason to measure actual request bytes and consumed context. It connects ECS's active-route condition (§5.1) to Mini's finite packs. A bigger expressive vocabulary and a smaller operative distinction set can coexist without contradiction.

For a stochastic downstream generator, identical complete conditioning instead gives identical conditional answer distributions under the same provider conditions. Such a route cannot guarantee the two different required answers with probability one in their respective situations. It can still answer both correctly by chance in separate samples; the deterministic conclusion is not a claim of inevitable sampled failure.

## LP-09. Equal effective request policies leave no additional language-label effect

**Assumptions.** Two arrangements construct identical next requests and tool results from corresponding histories, use the same output-selection rule, and encounter the same conditional provider behavior. A language label is recorded locally but has no additional channel to the model.

**Result.** The distributions of their effective request, tool-result and response transcripts coincide under those conditions. Local metadata containing the deliberately different labels is excluded from this projection.

**Proof.** The initial request is the same, so its conditional response law is the same. Corresponding responses yield identical next requests and tool results. Repeating the argument through the finite call sequence establishes equality of transcript laws. This is equality of distributions, not identical independently sampled outputs.

Thus an observed language effect must operate through conditioning, rendering, tools, feedback, selection or changed provider conditions. It cannot be credited to the label independently of those paths. Hidden provider state or an omitted request field defeats the premise. See [the request-control derivations](DERIVATIONS.md) for the corresponding practical controls.

## LP-10. A syntactic certificate cannot by itself establish bearing

**Assumptions.** A formation or proof checker operates on a candidate formalization. No independently supplied premise relates that formalization to the target organization and respect.

**Result.** Checker acceptance alone does not entail ECS Account or Bearing for the target.

**Proof.** The same accepted formal object can be paired with two asserted interpretations: one anchors its components to the target, while the other misidentifies a measurement as an assignment or fails to anchor a component at all. The checker result is unchanged because its input is unchanged. ECS §2.2 treats the anchor and its role interpretation as load-bearing. The accepted syntax therefore cannot discriminate the two attributions.

A Lean-oriented proposal is still useful and admissible before this relation has been established. Its initial study can measure expressibility and search effects. What is prohibited is silently promoting a later syntax or proof-checking receipt into a certificate that the language captures the intended phenomenon.

## LP-11. Proof transport needs an explicit engineering bridge

**Assumptions.** An optional checker is sound for a stated formal interpretation; it accepts a derivation of property phi; and the formal-to-target map preserves phi's relevant relations, quantifiers, boundaries and admitted cases.

**Result.** The formal property transports to the target over the preserved scope.

**Proof.** Checker soundness gives phi in the formal structure. The preservation premise maps each part of that satisfied property to its target counterpart, so the corresponding target assertion holds over the mapped cases. If a boundary, case or relation is absent from the map, the proof supplies no assertion about it.

Checker soundness and faithful compilation are added engineering bridges. ECS permits their representation as explicit, criticizable premises; it does not establish them. This positive conditional result explains what formal checking can contribute while leaving prose objections to the interpretation and bridge fully admissible. It is an optional instrument, not an initial admission condition for a semantic class.

## LP-12. Closed criticism vocabulary can obstruct a particular inquiry without proving universal incompleteness

**Assumptions.** A criticism c bears on an operative aspect of the inquiry at the fixed respect. No allowed expression in the current criticism channel represents the relevant distinction in c. The controller rejects c and supplies no other route by which it can become a represented target and affect use.

**Result.** That arrangement cannot realize the continuation requiring that criticism, despite any completeness claimed inside its allowed syntax.

**Proof.** Every admitted continuation through the channel lacks the represented distinction by hypothesis. The excluded criticism therefore has no active route into the stipulated response, so a continuation specifically requiring that content cannot be realized through this arrangement.

The result is conditional on a concrete excluded criticism. It is not a theorem that every formal language is incomplete, and it does not by itself refute ECS §8.1's recursive critical capacity. That condition requires an owned enabling continuation for every admitted target chain, not use of every particular objection. A different criticism could still scrutinize the same target. Defeating capacity for a chain requires showing that all its admitted enabling continuations are blocked. Allowing prose or a successor scheme can remove the local obstruction; merely storing rejected text without an operative route does not.

## LP-13. Preserving an independent prose route can avoid a local formal loss

**Assumptions.** Formal encoding e merges x and y, but an independently retained representation r distinguishes them at the fixed grain. The combined system can actually use r on the response route within its budget.

**Result.** The collision in e does not imply that the combined system loses the distinction.

**Proof.** The paired representations (e(x),r(x)) and (e(y),r(y)) differ. Therefore the equal-input premise of LP-03 does not hold for the combined route. A response function can distinguish the pair by its second component. Whether the system has the owned process that does so remains an additional empirical question.

Retained prose is consequently more than a courtesy attachment when it keeps an operative distinction that a candidate formal language omits. It is also not automatic salvation: lossy summaries, inaccessible archives or budget starvation can make the second route inert. ECS distinguishes storage, active use and deployment (§§5.1, 6.1).

## LP-14. Using an objection does not imply that it is sound or that it repairs anything

**Assumptions.** A system's transition genuinely depends on the content of an objection, with the representation-preserving contrasts required by ECS §5.2.

**Result.** Reason use alone entails neither that the objection bears correctly on its target nor that the resulting change satisfies Repair.

**Construction and proof.** Take a task where expiry is strictly after time t. A critic incorrectly demands inclusive expiry. A system understands that demand and changes its program from `>` to `>=`, preserving the same change under paraphrase and reversing it when the objection's content is reversed. This can satisfy the reason-use contrasts. It introduces a failure at the boundary and can violate a protected obligation. Thus reason use holds while repair fails.

ECS §5.2 explicitly permits use of an invalid objection, and §9.1 separately requires repair. This matters when measuring whether added critics help: stronger influence can amplify a mistake as readily as correct it.

## LP-15. Application of PP4: adding substantive commitments can destroy an account

**Assumptions.** The added component is an active rule in the account, not merely new unused syntax. Target, question and background stay fixed.

**Result.** More commitments do not generally preserve accounting, even when no existing commitment is deleted.

**Construction and proof.** Apply [PP4's derived-output construction](PROBLEM_PROMOTION.md#pp4--accumulating-commitments-need-not-preserve-an-account): the input boundary fixes x=0, an active rule determines z=x+1, and the question concerns z. Removing that rule leaves z undetermined; thus the answer z=1 is derived through an active relation rather than supplied as its own unexplained premise. The specified identity maps, role-preserving anchor and deletion contrast establish the original account's five accounting conditions. Adding an active rule z=x+2 while retaining the first rule makes the solution intersection empty. Non-vacuity fails even though all old commitments remain recorded.

This is an application of PP4, not a second independent theorem or discovery. Its relevance here is to distinguish conservative extension of expressive means from accumulation of substantive assertions. The same counterexample instantiates ECS §3.1's refusal to assume upward closure: adding formal axioms, explanatory bindings or criticisms is not monotonic epistemic improvement.

## LP-16. A frozen first proposal becomes part of the later baseline

**Assumptions.** The first phase constructs and installs a functioning language/interpreter package, or a semantic organization that already supplies a target solution. Later trials initialize from that frozen functioning package.

**Result.** Later expression of that supplied organization does not establish historical New relative to the later initialization.

**Proof.** ECS §6.2 includes functioning initialization in the baseline repertoire. If the target content is already deployable there at the fixed grain, an equivalent later content has a prior repertoire member. The negated existential required for New is false. This says nothing about whether its construction in the first phase was originative; that requires the first phase's own history and boundary.

The initial model-generated language must therefore remain in the provenance account. A language can hide the whole solution behind one primitive. Subsequent fluent use of that primitive may be activation or transfer rather than fresh construction. Freeze and inspect initial proposals without prematurely deciding which historical attribution they satisfy.

## LP-17. Finite success leaves historical novelty underdetermined

**Assumptions.** Observations cover a finite set of outputs and recorded episodes. For the particular target content at the fixed grain, both a history with a prior deployable equivalent and a history without one remain compatible with the evidence and all other stated premises. Incomplete knowledge of unrelated parts of the repertoire alone is not enough to establish this assumption.

**Result.** Those successes alone do not entail ECS New, even if the output strings or proposed language names were absent from the recorded run.

**Proof.** Take the two compatible histories supplied by the premise. In one, the system previously possessed a deployable equivalent at the fixed grain; in the other, no such prior equivalent exists and it constructs that organization during the episode. The first history satisfies the observations while falsifying New. Therefore those observations and premises do not entail New. The second history establishes that the prior-equivalent alternative is also not forced by the evidence; the exact remaining attribution conditions must be assessed separately.

This is an evidential underdetermination argument, not a claim that novelty can never be established. It allows reporting witnessed expression, local construction changes and novelty relative to a recorded initial program while leaving the broader pretrained-system claim unresolved (§§6.1–6.3).

## LP-18. A local expressive obstruction is not a universal barrier

**Assumptions.** A frozen arrangement L,M,B cannot represent or use a needed distinction. A successor scheme or another admitted resource condition remains possible within the broader system boundary.

**Result.** The local failure does not establish an explanatory barrier for that broader system.

**Proof.** ECS §8.2's barrier claim quantifies over all admitted non-question-begging enabling conditions in an independently characterized domain. The observed failure concerns one such condition. If a permitted successor adds a distinction-preserving carrier and an owned use route, that condition supplies a counterexample to the universal negative. Even before such a successor succeeds, failure to examine it leaves the barrier inference unsupported.

This is why expressiveness results must name Mini's actual ports, model, tools, renderer, time and resource conditions. It also prevents the opposite exaggeration: editable language files do not prove the competence to construct a useful successor. Extension in principle and owned successful extension remain different claims.

## LP-19. Frozen specimens identify a comparison only when their material interpretation is also fixed

**Assumptions.** A language text is unchanged, but its interpreter, renderer, permitted tools, token allowance or initial operative content changes.

**Result.** The old text's identity alone does not identify the same expressive or generation condition.

**Proof.** A changed interpreter can give the same symbol a different role; a changed renderer can remove a distinction by LP-08; a changed allowance can exclude an old production witness by LP-06. Each construction leaves the language bytes fixed while changing the set of represented or reachable contents. Therefore the text hash is insufficient to identify the studied arrangement.

Freeze the whole initial proposal package and its material conditions. Later integrations receive successor identities and separate comparisons. This is the engineering expression of ECS's named primitive supplies and grain/boundary discipline (Part 0, §9.4), not a claim that language proposals need prior adequacy approval.

## LP-20. Finite protected-obligation repair can be established without deciding creativity

**Assumptions.** A fixed finite obligation set O and protected set P are exhaustively evaluated under a named interpreter. A recorded change makes at least one failed O obligation pass, preserves every previously satisfied member of P, and is the installed change that produces those behaviors.

**Result.** These observations establish the corresponding finite Repair O,P instance, conditional on the interpreter and provenance supplies.

**Proof.** The changed obligation supplies the first conjunct of ECS §9.1. Exhaustive preservation over P supplies its second conjunct. The actual installation and execution trace supplies ProducedBy for that change and respect. Nothing in those conjuncts supplies New, explanatory bearing or the remaining CreateEK requirements of §9.2.

This is a positive result the later integration study can seek without a scalar creativity score. A proposed language component might enable such a repair, prevent it, or make no difference. Comparisons can establish the local effect while leaving stronger historical and semantic attributions open.

## Consequences for the first study

Freeze independently generated initial schemes before adaptive integration. Record what they permit in principle, what Mini can actually carry and use, and what appears in observed runs. Keep Lean-oriented and non-Lean schemes comparable at the same task respect and material boundary without requiring identical internal syntax. Preserve prose conjectures and criticisms as legitimate contents; record failed translations as separate failures of a route.

A useful first intervention changes one component or resource condition and asks for a distinguishing expression or use. A later integration can test whether the component improves a concrete repair or active reason path. Theorems about conservative possibility, collision or conditional proof transport explain what those observations would mean; they do not predetermine whether a candidate language is good, adequate or creative.

Semantic promotion of encountered issues into new problems requires its own bearing and attention account. [Problem promotion](PROBLEM_PROMOTION.md) treats that next step. Initial language proposals need not wait for it to be fully settled, and later integrations must not rewrite the initial specimens or their observed limitations.
