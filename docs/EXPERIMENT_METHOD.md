# Designing and interpreting experiments

Read [the purpose](../PURPOSE.md) and [the semantic guide](SEMANTIC_GUIDE.md) before proposing a template. Every template answers a specific causal hypothesis about information flow, criticism, revision or deployment. A configuration search is not an evolutionary competition: diagnose the observed failure, explain the mechanism of the proposed repair, and test the prediction on declared conditions.

The current initial stage freezes model-proposed languages and semantic classes, including non-Lean proposals, to study relative expression under Mini's actual resources. Correctness of capture is not an admission requirement, and prose need not pass a formal translation gate. Repair and adequacy tests below apply when those stronger claims become the declared question; they do not replace the initial exploratory question. Preserve each first proposal unchanged and identify later integrations as successor experiments.

This method distinguishes required comparison obligations from capabilities implemented in a particular runner. A missing arm, ablation or semantic witness remains missing; the method is not a claim that all its experiments have run.

## Freeze a concrete claim

Before relevant model evidence, record the question, task family, instance construction, source/version hashes, model and software identity, full effective configuration, resource ceilings, interpretation registry, grain, system boundary, contrast contract, repair obligations O and protected obligations P. State the expected difference between arms and the observation that would defeat the proposed mechanism. Hash the actual rendered material and record which artifacts and evidence each stage consumes.

Commit the preregistration before the first live test. A subsequent revision has its own identity and claim. Development failures may guide that revision, but evaluation then needs fresh instances or a clearly named assisted-repair comparison. Do not treat an example inserted into a revised prompt as an independent held-out success.

The initial campaign can use exact executable or constraint-checking tasks with interactions such as replay, expiry, atomicity, duplicate delivery, parsing or preservation of protected cases. Machine checks establish bounded correctness. Explanatory claims receive separate review against §2.2 of ECS, with the task outcome and its interpretation kept distinct.

## Required comparisons

| Arm | Operation | Claim it helps assess |
|---|---|---|
| Direct bare baseline | Frozen model answers from the same task and source; native reasoning disabled where supported | What the model can do without Mini |
| Native reasoning | Same model, same initial information and answer contract; a supported native reasoning setting is enabled and its effective setting recorded | Whether native reasoning already provides the observed benefit |
| Mini candidate | Same model under one frozen, justified Mini template | What the configured system contributes |
| Repeated direct attempts | Independent bare attempts under the same aggregate resource ceiling and declared selection rule | Whether extra sampling explains a Mini advantage |
| Prompt-equivalent workflow without Mini | Comparable instructions and feedback executed without Mini's graph, routing or stored return machinery | Whether prompt decomposition or the machinery causes the difference |

The first three arms are required by the project request. The additional controls become necessary before attributing a benefit specifically to machinery. They can be applied to an informative main comparison instead of multiplying every initial pilot.

A prompt requesting more thought is not a native-reasoning manipulation. The arm needs a real supported provider capability and a recorded setting. If the endpoint cannot disable reasoning, describe the bare arm as a default direct baseline. If native mode is unsupported, mark that comparison unavailable. Switching model families changes the model and cannot silently substitute for toggling reasoning on the same model.

Keep model calls, input tokens, output tokens, provider-reported reasoning tokens, retries, tool calls and elapsed time visible. Equal ceilings do not imply equal expenditure. Mini's separate body and commitment generation can cost two calls; count both. Missing usage is unknown, not zero. A missing final answer caused by a provider or delivery failure is not evidence about semantic capability.

All compared arms receive the same available source facts and tool affordances unless access is the declared intervention. A tool-enabled Mini arm against a source-starved baseline tests the combined access change. Its advantage cannot be credited to routing alone.

## Mechanisms worth constructing

| Candidate design | Mechanism and required paths | Distinguishing test |
|---|---|---|
| Anchored critique and repair | Source → conjecture; original content plus its machine reading plus execution → criticism; criticism → revised conjecture | Expose a mistaken reading that the critic cannot diagnose from prose alone, then compare a template that actually supplies the missing layer |
| Validity challenge | Checker assumptions and exact input/output are criticizable alongside the candidate | Compare a faulty checker with a sound negative checker; blanket rejection cannot succeed in both |
| Return and deployment | A constructed operative rule is installed and consumed on the next case | Preserve the proposed bytes in a no-return control but do not install them |
| Complementary conjecture schools | Distinct initial interpretations generate alternatives while relevant criticisms are shared | Compare changed generator variety with actual repair and independent verification; variety alone is insufficient |
| Grounding intervention | Live execution or evidence is supplied on a declared schedule, with a final oracle withheld from all arms | Compare closed and grounded loops under matched task/model ceilings; inspect both candidate and critic failures |

These are design families, not promises that named configuration fields exist. Read the extracted Mini implementation and its effective rendered inputs. A port declared in a file may have no producer, be empty at its stage, hide the commitments that matter, or have no consumer. Verify the actual path before a live causal claim.

Start with the simplest configuration that exercises the intended path. Add schools, sampling, embeddings, attention rules or extra stages only when a documented failure gives the proposed change a reason. A change that combines instruction and wiring may be useful but requires an ablation before their effects are separated.

## Concrete technical task patterns

An idempotency task can combine tenant-scoped request identifiers, payload conflicts during a live record, a declared logical expiry boundary, original-result replay, and durable side effects that survive cache eviction. A correct solution must distinguish expiration of deduplication metadata from reversal of the completed operation. Protected checks include ordinary unique requests, cross-tenant isolation, exact boundary times and sound rejection of conflicting reuse. The prompt supplies the contract; it must not supply the final policy as a worked example disguised as background.

An inventory task can combine duplicate deliveries, positive and negative adjustments, reservation limits, cancellation referring to an earlier reservation, and independently ordered arrival. The exact consistency and expiry model must be declared before testing: a requirement to merge replicas is different from centralized sequential execution, and a check must not assume both without justification. Final states and rejected events are independently checkable; an explanation must identify the operative relations and preserve protected behavior.

A parsing task can combine quoted delimiters, escapes, nested or length-delimited framing, and invalid-input handling. It should require a rule that generalizes beyond visible examples. Tests distinguish changing a structural delimiter from renaming irrelevant payload text. A patched regular expression that passes one example but consumes forbidden trailing input fails the protected contract.

If a safe policy DSL replaces arbitrary generated code, record its primitives, interpreter and expressive limits as supplied enabling organization. Exact finite search can still evaluate configuration usefulness. It cannot by itself establish unrestricted creativity or exclude solutions outside that language.

## Separate verification from explanatory review

The verifier executes only the declared task contract and records exact witnesses. It should include unseen combinations and protected behavior. An independent explanatory review checks structural anchors, the question and respect actually answered, compositional claims, non-circular dependence and a compatible baseline. Review outcomes may remain unresolved where the source or model trace does not supply the necessary evidence. Do not ask a judge for an ungrounded overall creativity score.

A verifier's success does not immunize the specification, interpretation or relevance of its checks (ECS §5.4). A failed check contradicts a conjunction of candidate, auxiliaries and interpretation. Preserve the original account, the machine reading and the test assumptions so that a diagnosis can land on the layer that actually failed.

All final holdout data stays outside live conjecture, critic, translator and summarizer packs. If the experiment reveals feedback during a run, name it development feedback and keep a separate final holdout. Revisions informed by final holdouts require new instances for independent evaluation. Holdout identity can be committed without exposing its bytes to live arms.

## Reason-use and return-path contrasts

A readable criticism or artifact citation demonstrates exposure. ECS §§5.1–5.2 additionally requires content-governed dependence. A continuation probe therefore compares a content-preserving recoding, a relevant content change, removal of the operative reason and irrelevant padding. The preserved meaning should preserve the relevant response; changing the bound reason should change it as the declared deliberative rule predicts. Use matched inputs where possible so length or salience does not explain the change.

For operative return, compare installing a constructed change with retaining identical bytes without installation. Then ask both resulting systems to address the same fresh case. Evidence of a difference supports a bounded active-route attribution at the declared boundary. It does not reveal the complete model's prior repertoire or prove universal capability.

## Failure records that do not corrupt semantic verdicts

| Observed condition | Category | Required treatment |
|---|---|---|
| Endpoint failure, timeout, missing final response, containment kill | Operational delivery failure | Retain sanitized request/error/partial receipts; issue no semantic verdict |
| Unsupported native mode or unknown effective setting | Manipulation not established | Mark unavailable or uncertain; do not silently relabel |
| Invalid or ambiguous machine reading of substantive prose | Interface/translation failure | Keep both prose and reading; inspect the translation contract |
| Missing producer, empty required port, unused commitment or missing terminal receipt | Mechanism/protocol failure | Stop the affected claim loudly and record the exact path or stage |
| Candidate violates a task obligation | Substantive failure under stated assumptions | Record the witness and distinguish candidate, checker and interpretation hypotheses |
| Correct output without origin, reason-use or deployment evidence | Attribution incomplete | Preserve bounded task success; leave stronger claims unresolved |
| Holdout leakage or task changes after evidence | Comparison invalidity | Preserve the contaminated block; create a new claim and fresh evaluation |
| Effective inputs differ under one supposed configuration identity | Identity defect | Preserve conflicting bytes, repair identity and rerun affected comparisons |
| Publication fails or remote identity is unverified | Operational publication failure | Preserve locally and repair publication; do not claim the test is durably published |

V1.3 §1 explicitly says a containment kill must not mint a warrant. ECS §5.5 likewise separates failed delivery from content evidence. Operational failure may disqualify a comparison but is not evidence that the model lacks an explanatory capacity.

Each erratum includes the observation, affected run and config, initial diagnosis, competing causes, remediation and verification. Mark causes as established, supported hypotheses or unresolved. Later corrections append to the record instead of rewriting the earlier interpretation. Deterministic fixtures can establish that a repaired path now runs; they are instrumentation tests and do not join live semantic results.

## Revision, lessons and publication

A revision record states observed failure → causal diagnosis → changed mechanism → predicted distinguishing observation → new test. Preserve the previous effective configuration and evidence. If the scoring instrument was wrong, keep its original output as invalidated, correct the instrument and rerun the appropriate comparison. A post-hoc reinterpretation is not a preregistered result.

Separate lessons by configuration and wiring, semantics and attribution, evaluation, model/provider behavior, operations and source integrity. Each lesson links its supporting records and scope. A lesson such as 'the critic needs the translated commitment to diagnose this error' is grounded in a mechanism. A slogan such as 'more criticism makes models creative' is not supported by it.

Every completed config test, including failed tests, is committed and pushed to main immediately with its sanitized outputs, resource records, diagnosis and interpretation. Verify the resulting remote commit identity. Parallel workers use isolated run roots; publication is serialized so one push cannot hide or omit another test. At most five config tests run concurrently. Credentials never belong in a run artifact or published command receipt.

Repository hooks direct future work to the purpose, effective configuration map, experiment workflow, interpretation workflow, errata and lesson files. Reports preserve negative evidence, failed hypotheses and unresolved semantic conjuncts. General user updates stay human-readable; detailed results belong in the repository.

## When further testing has no grounded next step

The configuration space is open-ended. A campaign cannot prove that all possible configurations are exhausted or infer a universal barrier from one frozen implementation (ECS §8.2). Its stopping judgment is local and reasoned.

Inspect every remaining failure. Each currently supported causal hypothesis should have a tested repair, a tested reason that the repair does not help, or a named external dependency preventing a valid next test. Required comparisons and meaningful ablations must be complete. Apparent improvements need fresh instances and preserved obligations. Continue whenever the evidence supports a concrete new mechanism with a distinguishing prediction.

Stop when the completed record supplies no further such proposal within the declared model, task family, tools and resources, and explain that scope. Do not use a progress percentage, a scalar novelty target or an arbitrary fixed number of unsuccessful rounds as the exhaustion criterion. Missing credentials, an unavailable native-reasoning control, missing source mathematics or an unaffordable required test is a blocked comparison, not scientific exhaustion. State what new evidence or capability would reopen it.
