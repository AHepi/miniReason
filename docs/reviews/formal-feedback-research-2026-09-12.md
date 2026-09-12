# Can explicit formal arguments help an LLM answer a prose problem?

2026-09-12 UTC. Research continuation under R20260912-01 through R20260912-07.

The proposal is worth testing as an optional criticism mechanism: let the model produce an explicit argument, check its declared inferences, and return concrete failures or alternative models for the next response to address. A working local prototype now demonstrates that mechanism. It also demonstrates how a formally successful argument can evade the original question. No new live model calls were made, so whether this helps an LLM, Mini or problem promotion remains an empirical question.

The checked artifact is a public candidate argument, not a record or revelation of native hidden reasoning. The model's prose answer and objections remain legitimate independently of whether the optional formal artifact parses. A language failure can itself become the subject of criticism.

## What was actually completed

The [diagnostic package](../../experiments/diagnostics/formal-feedback-v1) contains a standard-library Boolean checker, eleven operator-authored fixtures, nineteen focused tests, raw execution receipts, an explicitly supplied revision replay, and a separate intermediate-dependency demonstration. The [integrated test receipt](../../experiments/diagnostics/formal-feedback-v1/results/integration-receipt.json) records nineteen passing tests from the installed project location. The original engine source and old frozen plans were not changed; its earlier 569-test verification was not rerun or represented as new evidence.

The [prospective protocol](../FORMAL_FEEDBACK_PROTOCOL.md) defines shared-draft feedback comparisons, matched prose review and bare/native baselines. It is not an implemented model runner or generated E026 plan. A new one-cycle Mini adapter and actual-material preflight are still required before this additional protocol can run through Mini. Existing E023/E024/C001 preparation remains separate.

The progress skill **minireason-progress-ledger** is installed and named in AGENTS. It supplies a four-minute warning and five-minute deadline check, requiring acknowledgment of newly appended evidence. Thirteen focused timer checks passed. A fresh-context accelerated trial detected and truthfully recovered from a missed ten-second deadline. This establishes a usable reminder and recovery mechanism, not a guarantee that an inactive assistant or blocked tool will wake on time.

## The important distinctions

For a declared finite vocabulary, let S be the set of valuations satisfying the submitted premises A. The checker enumerates the full supported Boolean domain, with at most ten atoms. It distinguishes these results before returning a possible next inquiry.

| Result | What the receipt establishes |
|---|---|
| Inconsistent | S is empty. No conclusion is certified through classical explosion. |
| Entailed | S is nonempty and every member satisfies the goal q. |
| Refuted | S is nonempty and every member satisfies the negation of q. |
| Undetermined | A q model and a not-q model both exist under A. |
| Invalid or unsupported | This checker has no logical result for the submitted artifact or resource scope. |

A countermodel to q alone does not establish that not-q follows. A typecheck is also different from a proof, and a checked proof is different from a faithful account of the prose problem. The prototype is exhaustive model checking in a small fragment; it does not verify arbitrary Lean proofs, quantifiers, temporal claims, probabilistic statements or a general theory's consistency.

## A persistent concrete case

The illustrative question concerns a service with two replicas, A and B: after acknowledging a write, can it promise survival after permanent loss of either replica, and what should it do when only one replica has persisted the write?

The declared meanings distinguish acknowledgement, durable persistence on A, durable persistence on B, and survival of either single-replica loss. The finite language has no temporal semantics: timing and durability meanings are part of the criticizable interpretation. These fixtures are transparent operator constructions, not sampled model answers or a study of a production storage system.

The [underdetermination receipt](../../experiments/diagnostics/formal-feedback-v1/results/fixture-run-v1/underdetermined_claim.result.json) contains a concrete pair of compatible premise models. In one, acknowledgement is true, only B has persisted the write, and the required survival guarantee is false. In another, acknowledgement and both persistence facts are true, and the guarantee is true. The existing formal premises do not distinguish them.

That pair suggests an operator-proposed next question: what does an acknowledgement establish about persistence on each replica, and which observation or policy would distinguish one-copy from two-copy completion? This is an example of a question supported by the diagnostic. It is not a model-generated promotion result, and it does not establish that either proposed policy is already in force.

## Actual local outcomes

Every expected classification in the [fixture summary](../../experiments/diagnostics/formal-feedback-v1/results/fixture-run-v1/summary.json) matched. That count describes instrument verification; it is not a model-accuracy or creativity score.

| Operator-authored probe | Actual result | What the case shows |
|---|---|---|
| Conditional consequence | Entailed | The declared acknowledgement and retention assumptions entail the conditional goal. |
| Contradictory commitments | Inconsistent | No compatible premise valuation exists; the goal is not certified. |
| Contrary claim | Refuted | Every compatible valuation defeats the goal. |
| Missing distinction | Undetermined | Both goal values remain possible under the same premises. |
| Easier substituted question | Entailed | Present existence on one replica was substituted for survival of either replica loss. |
| Meaning collision | Entailed | One symbol was used across an at-least-one/both-replicas distinction. |
| Bijective symbol recoding | Entailed | Complete premise models and goal values agree after reversing the symbol map. |
| Undeclared symbol | Invalid | Formal evaluation stops while the prose and objections remain retained. |
| Eleven declared atoms | Unsupported | The fixed ten-atom limit is exceeded; no semantic rejection follows. |
| Impossible antecedent | Entailed | Premises forbid acknowledgement, making the acknowledged-write conditional vacuous. |
| Conclusion supplied as premise | Entailed | The desired result has been assumed instead of independently established. |

The four successful-but-inadequate cases are not checker bugs. They locate work that the checker does not do: preserving the target question, interpreting symbols consistently, covering active cases and avoiding circular support. Their inadequacy is argued from the original prose obligations, not inferred from a parser flag or a model vote.

## What checking the chain adds

The [dependency diagnostic](../../experiments/diagnostics/formal-feedback-v1/results/chain-diagnostic.json) checks each declared intermediate statement before allowing its reuse. A valid three-step example produces entailed, entailed, entailed. Removing the assumption that acknowledgement implies persistence on B produces entailed, undetermined, blocked. Contradictory starting assumptions produce inconsistent, blocked, blocked. Self-dependence, forward reference and shadowed base identifiers are rejected.

The comparison also deliberately inserts the missing B-persistence statement as a premise into a final-only check. That endpoint returns entailed. Its conditional deduction is correct, but it has not established the added premise. A separate [unchanged-base endpoint check](../../experiments/diagnostics/formal-feedback-v1/results/unchanged-base-final-check.json), preserving the weaker original assumptions, returns undetermined. Thus the chain adds localization and controlled reuse; it adds no deductive power to an exact checker given the same assumptions.

Every step receives all original base assumptions plus its named established predecessors. The dependency field records reuse prerequisites. It does not certify that only the named supports suffice, that those supports are necessary, or that the dependency graph is a complete explanatory account. The demonstration is a small operator-authored probe, not a hardened general proof-assistant interface.

There is a useful conditional invariant. Suppose the initial premises A have a model, the checker is sound for its fixed interpretation, and every added step is accepted only when it follows from A plus earlier accepted steps. Then every accepted step follows from A. The first step does by the rule; inductively, every A model satisfies the earlier steps and therefore the newly accepted consequence. This explains why an unchecked intermediate must not enter the accepted-premise store. It says nothing about whether A captures the original phenomenon.

## Why consistency repair can undermine the inquiry

Deleting a troublesome premise can make an inconsistent set satisfiable. It does not establish that deleting that commitment is legitimate for the original task. Likewise, replacing q with a weaker q-prime can produce a proof while abandoning the question. Adding q as a premise guarantees conditional entailment whenever the enlarged premises have a model. These are elementary constructions and declared failure cases, not newly discovered results about LLMs.

The constructive use of checking is to return a localized difficulty that the next response can examine. The model might repair a genuine inference, propose a distinction absent from the vocabulary, criticize an assumption, or explain why the checker is addressing a different question. It might reasonably leave the issue unresolved. A controller that rewards only acceptance would remove these alternatives and change the research object.

The model therefore proposes statements and revisions, while configured machinery controls scheduling and tool access. No checker status automatically endorses the answer, grants more calls, installs a new language or starts another episode. Prose criticism can challenge the checker, its interpretation or the inference itself. This is consistent with existing LP-02, LP-03 and LP-10–LP-12; it is not a new semantic authority.

## Relevant primary research

| Source | What it supports | Limit relevant here |
|---|---|---|
| [Logic-LM, 2305.12295v2, §§3–4](https://arxiv.org/abs/2305.12295v2) | Prose-to-symbolic translation, external solving and solver-error-driven revision. | Its main benchmark table excludes self-refinement. Refinement increases executability without uniformly increasing executable accuracy; reported GPT-4 values fall from 80.4 to 79.9 on FOLIO and 60.0 to 58.8 on AR-LSAT. Package gains cannot be credited to feedback alone. |
| [LINC, 2310.15164, §5 and Appendix E](https://arxiv.org/abs/2310.15164) | Separating language-to-logic translation from external deduction can yield a different error profile. | Missing implicit information, poor predicate decomposition and syntax failures remain. Its bootstrapped majority-vote comparisons are not the same intervention as one shared draft with feedback. |
| [COPRA, 2310.04353v5, §§2–4](https://arxiv.org/abs/2310.04353v5) | Proof states and execution feedback are used to construct later tactic prompts. | It starts from formal obligations; it does not establish correct capture of an arbitrary prose question. |
| [ProofFlow, 2510.15981v1, §§3–4 and Appendix A.2](https://arxiv.org/abs/2510.15981v1) | Explicit step dependencies and separate formalization/proof work can make failures inspectable. | Intermediate statements with `by sorry` are not proved merely because they compile. Semantic fidelity uses an LLM judge; the kernel does not certify correspondence to prose. |
| [The Faithfulness Gap, 2606.16541v1, §§8 and 12](https://arxiv.org/abs/2606.16541v1) | A recent proposal uses contrastive consequences to probe changed meanings. | Its stated limits leave predicted probe labels, natural-language ambiguity and incomplete search as dependencies. It is a source of possible probes, not an adequacy certificate adopted here. |

These sources were located through alphaXiv and checked against primary arXiv material. Their empirical results are context, not evidence produced by miniReason and not derivations from ECS. Their scoring, voting, search priorities and optimization policies are not imported into this project.

## The next discriminating experiment

The published protocol holds one actual generated formal draft fixed before giving paired continuation calls no returned checker feedback, syntax-only feedback, or full bounded diagnostics. Matched prose self-review asks whether another call already provides the same repair; bare and native single-call answers retain the existing baselines. Actual revisions must be assessed against the original problem and protected distinctions, including reasonable resistance to bad formalization.

One complete initial problem block has fourteen distinct calls because its formal drafts are shared. The design tests feedback availability. It does not isolate formal syntax from changed draft content or added deductive information. A later carrier-only comparison would express identical checker facts in prose and formal syntax and count its additional calls separately. Offline adverse-case coverage does not guarantee those cases will arise in two generated drafts; absent live classes remain unobserved.

For subsequent problem promotion, preserve the whole original question, argument, checker receipt and revision as an explicitly frozen handoff into a distinct successor-discrimination template. It can investigate a language inadequacy or missing distinction, suspend, or conclude that no new problem is warranted. No automatic second use of the same template or automatic promotion is introduced.

## Reproduce the local diagnostic

From the repository root, check an existing specimen without modifying it:

```sh
python experiments/diagnostics/formal-feedback-v1/tools/formal_argument_check.py check --input experiments/diagnostics/formal-feedback-v1/fixtures/underdetermined_claim.json
python -m unittest discover -s experiments/diagnostics/formal-feedback-v1/tests -v
```

To reproduce all fixtures or the dependency demonstration, use fresh output locations outside the committed record:

```sh
python experiments/diagnostics/formal-feedback-v1/tools/formal_argument_check.py run-fixtures --fixtures experiments/diagnostics/formal-feedback-v1/fixtures --output /tmp/minireason-formal-fixtures-new
python experiments/diagnostics/formal-feedback-v1/tools/chain_diagnostic.py --fixtures experiments/diagnostics/formal-feedback-v1/fixtures --output /tmp/minireason-formal-chain-new.json
```

Both commands reject existing destinations in these modes. The fixture inventory binds the original staged package; the separate integration receipt binds the added dependency code. All generated examples and the supplied revision replay are explicitly operator-authored. No observed LLM correction, live advantage, new explanatory knowledge or actual problem-promotion outcome is claimed.

The current live continuation remains E023 after explicit permission to disclose the published experimental material and generated outputs to the declared DeepSeek endpoint. That requirement comes from the previous automatic approval rejection. This turn preserved the boundary and completed the independent local research. The next implementation for this new idea is the small optional Mini feedback adapter, exact material, frozen executable plan and preflight described in the protocol.
