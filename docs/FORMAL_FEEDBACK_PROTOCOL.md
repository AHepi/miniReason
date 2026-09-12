# Explicit formal arguments as feedback for a prose problem

Status: prospective research protocol, 2026-09-12 UTC. This is a design, not a generated runnable E026 plan and not a live observation. No model request has been made under it. E023, E024 and C001 retain their existing identities and ordering. The current external DeepSeek disclosure blocker remains.

## Question and scope

Does giving an LLM a checkable, explicit argument and the checker's actual diagnostics help it revise an answer to a prose question or identify a useful next investigation? Does the same arrangement instead encourage it to delete troublesome assumptions, weaken the question or suppress a criticism that its chosen language cannot express?

The object checked is a public candidate argument requested as an output artifact. It is not a disclosure or measurement of the model's native hidden reasoning. The original prose, proposed interpretations and unformalized objections remain available throughout. An unsuccessful formal translation is an observed limitation of this route, not grounds for rejecting the prose conjecture.

The first diagnostic language is a deliberately small propositional fragment with an exact finite interpretation. Its operator-supplied grammar is a declared enabling contribution. Results from it will not measure the whole expressibility of a model-proposed language, Lean, Mini or ECS. A later language-proposal experiment must preserve each initial proposal unchanged and identify any checker-compatible revision separately.

## Why this is worth testing

Logic-LM translates prose into symbolic formulations and uses solver errors during revision. Its main benchmark comparison excludes self-refinement, so its package gains do not establish the contribution of feedback. COPRA uses formal proof-state feedback to guide later tactics, but begins with formal obligations. These establish precedents for the mechanism and expose the need to test the prose-to-formal bridge separately. [Logic-LM, §§3–4](https://arxiv.org/abs/2305.12295v2); [COPRA, §§2–4](https://arxiv.org/abs/2310.04353v5).

The existing project already distinguishes checker acceptance from bearing in LP-10 and gives a conditional transport result in LP-11. This protocol adds a proposed intervention on the active feedback route. External research informs that intervention; it does not replace the project's semantic guide. See [Language Proposal Theorems](LANGUAGE_PROPOSAL_THEOREMS.md) and [Semantic Guide](SEMANTIC_GUIDE.md).

## Frozen objects and custody

Before activation, freeze the full prose question, source occurrences, independently stated obligations, protected distinctions, candidate-generation instructions, checker grammar and limits, provider settings, input/output renderers and declared comparisons. A public draft contains its atom meanings, premise identifiers and formulas, target formula, prose explanation, and any criticism or unformalized residue. Preserve its raw bytes even when parsing fails.

Generate one formal draft for each thinking setting. Publish the draft and its checker record before revision dispatch. Every feedback condition at that setting receives that exact draft; do not regenerate a nicer one, select by checker success, or silently repair syntax. A failed or unformalized candidate remains part of the record. If it cannot be checked, all applicable later conditions receive their predeclared status for that same failure.

The checker runs once on the full draft and its result is archived in every condition, including when withheld from the model. Only the declared view of that result changes. The archive is not a model-input channel. Count the shared generation once as shared cost, and also report the two-call path cost of each continuation. Branches sharing a draft are paired observations, not independent samples.

Raw provider requests, public responses, token counts, actual settings, errors, source identities and checker identities must be retained. Native hidden reasoning and credentials must not be recorded. Hashes establish custody, not truth or external execution by themselves.

## Initial direct comparison

This bounded design uses one predeclared prose problem. Its purpose is a mechanism witness with adverse cases, not a population estimate. The exact problem and atom meanings must be frozen before activation; the local illustrative fixtures are tool checks and are not the future model's generated draft.

| Condition | Calls on each path | Information in the final call | What it helps distinguish |
|---|---:|---|---|
| Bare answer | 1 | Original question, thinking disabled | Existing direct baseline |
| Native answer | 1 | Same original question, thinking enabled | Existing native baseline; not a matched feedback control |
| Prose self-review, disabled and enabled | 2 each | Original question and its own first prose answer | Benefit of another call and self-criticism |
| Formal, feedback withheld, disabled and enabled | 2 each | Original question and shared formal draft; explicit withholding marker | Formal drafting with no returned checker information |
| Formal, syntax-only feedback, disabled and enabled | 2 each | Same plus parsing/scope result; no entailment result or valuations | Tool-format assistance |
| Formal, full feedback, disabled and enabled | 2 each | Same plus scoped logical classification and available witness/countermodels | Added deductive information |

With one shared formal draft per thinking setting, this is fourteen distinct model calls: two one-call baselines, four prose calls, two formal drafts and six formal continuation calls. It is not eighteen independent two-call runs. All continuations use the same model identifier and inherited published provider policy; exact effective settings and resource allowances must be bound in the later executable plan. A configuration is not activated from this prose alone.

Thinking-enabled and disabled conditions remain distinct comparisons; do not pool their outputs or treat an unobserved provider implementation as controlled. No response is selected through a success score. No retry is automatic. Record a failed provider request as an execution boundary, not a negative semantic result.

The first final-call instruction is otherwise identical across the three formal conditions: retain, revise or suspend the answer for substantive reasons; explain any changed assumption or conclusion; preserve the original question; optionally state a new problem worth investigating, or explain why none is warranted. The prompt does not command agreement with the checker or require a successful proof.

## Checker contract and allowable response

Let A be the interpreted premises, q the interpreted goal and V the complete valuation set of the supported finite Boolean vocabulary. Compute S = {v in V : v satisfies A}. This is exhaustive model checking in the declared fragment, not proof of arbitrary mathematics or of the adequacy of A's interpretation.

| Receipt | Exact formal claim | Potential next inquiry, without automatic endorsement |
|---|---|---|
| Invalid or unsupported | This checker did not establish a logical result | Inspect the encoding or scope; retain the prose and consider another representation |
| Inconsistent | S is empty | Examine conflicting commitments, interpretation and checker assumptions; do not infer the desired answer by explosion |
| Entailed | S is nonempty and every member satisfies q | Scrutinize mapping, active cases and whether the conclusion was assumed or weakened |
| Refuted | S is nonempty and every member satisfies not-q | Inspect the argument and its interpretation in light of a contrary witness |
| Undetermined | S contains both a q model and a not-q model | Identify a distinction, premise or evidence that would discriminate the models, or retain uncertainty |

A single countermodel to q does not establish entailment of not-q. That distinction is essential to the returned feedback. Atom count and formula limits bound enumeration; reaching a limit says nothing about the rejected content's standing.

Do not add a scalar merit, creativity or progress score. A deterministic scheduler fixes stage order, available ports, bounded checker execution and the stopping boundary. The model contributes candidate content and reasons; it cannot increase its own calls, change the checker, or open a new episode through an output field. New assumptions, meanings or formulas are separately recorded proposed revisions. The original candidate remains unchanged.

## What would count as an informative result

The central positive case is an independently interpretable correction that appears after relevant full feedback, survives the original protected obligations, and is absent or differently handled under the paired withheld and syntax-only continuations. Even then a single sampled difference is a witness consistent with feedback use, not a causal population estimate. Counterfactual runs cannot force identical hidden provider state.

A negative case includes valid feedback ignored, a needless change that damages an adequate answer, a repaired proof obtained by assuming the conclusion, or an executable answer that loses a source distinction. A sensible rejection of a faulty formalization is an admissible outcome. Syntax failure, suspension and a decision against promotion are retained.

For each actual revision, report its changed premise or inference, the original problem obligation it affects, any protected behavior lost, whether the new representation is operative, and the exact feedback evidence it used. Separate an input-port receipt from a substantive reason-use interpretation. No historical-newness or general creativity attribution follows merely from a correct answer or useful new question.

The first task must include predeclared contrasts for inconsistent commitments, underdetermination, a consistent but inadequately mapped candidate, a vacuous implication and a conclusion supplied as its own premise. An independent case argument supplies their relevance to the prose question. The checker is not asked to certify that relevance. Record ambiguous readings rather than force a single answer by silently replacing the original question.

## Mini integration and successor inquiry

Implement a separately identified one-cycle draft-and-review template before claiming this experiment ran through Mini. Its checker adapter must consume public artifacts and return immutable scoped receipts. The direct runner and actual Mini route need exact model-visible request parity on controlled scripted traces, including invalid drafts and withheld feedback. Then freeze source and actual-material preflight identities. That adapter and generated run plan are not implemented by this protocol.

Live direct/Mini duplication is warranted only for a declared operational question or a documented difference in effective inputs or allowances. LP-09 forbids crediting a local route label with an independent model effect when effective request policies are identical. If a later study compares live routes, preserve matched stage counts and settings and report route costs separately.

Problem promotion remains a second, genuinely distinct template. Feed the whole published original question, public argument, diagnostic and proposed revision into a successor-discrimination episode through an explicitly frozen handoff. It may investigate a lost distinction, disputed assumption or inadequate language. It may also suspend or decline promotion. No checker status automatically starts it. This proposal does not replace or retroactively alter C001's predeclared source arm.

## Activation boundary

Complete the adapter, exact task material, generated plan, relevant parity/failure tests and zero-call preflight, then publish and verify those artifacts before any live request. Preserve E023's owed no-return control and review its bearing on the existing allocation before E024. The formal-feedback study is an additional candidate mechanism, not a reason to bypass that control.

Automatic approval review previously rejected disclosure of project material to the DeepSeek endpoint. This protocol does not supply the missing approval or authorize a workaround. Its current deliverable is a concrete design and local checker diagnostic. Live model benefit, actual Mini integration for this new protocol and the proposed successor investigation remain unobserved.
