# miniReason

**Purpose: discover how model-proposed languages and semantic classes expand or hinder what Mini can express and do, with bare-model and native-reasoning comparisons.** Read [PURPOSE.md](PURPOSE.md) before changing the study. Freeze initial proposals for their first trials, then integrate components through separately identified successors. The experiment must permit Mini to lose.

The initial question is relative expressibility under Mini's actual model, ports, context, time and resources. Correct capture of the posed problem is not an admission gate. Lean-oriented proposals, other formal languages and non-Lean semantic classes are all legitimate specimens. Prose conjectures and criticisms remain fully legitimate even when a formal translation fails. Record what is representable, what the configured system can reach, and what is actually witnessed as distinct claims.

Mini is extracted from [AHepi/h-EPI, claude/mini-experiments](https://github.com/AHepi/h-EPI/tree/b2a33283dc1e05fb83c3357b26e2cc12115f6b6c/src/creib/forge/mini). This project creates its own experimental templates from the supplied ECS 2.0 and harness v1.3 guides. Existing upstream experimental templates and findings are not presented as new work.

The experiment model is DeepSeek V4.1 Flash, using the official `deepseek-flash` identifier. The same model is called with explicit thinking disabled or enabled. See [provider settings](docs/PROVIDER.md) for what those comparisons control and leave uncontrolled.

## Start here

**If a window failed, read [DECISION_LEDGER.md](docs/DECISION_LEDGER.md) first, then [PURPOSE.md](PURPOSE.md) and [STATUS.md](docs/STATUS.md), and follow [the continuation and recovery workflow](docs/workflows/continue.md).** The ledger records choices and publication receipts; STATUS separates completed, interrupted and pending work. Compare the surviving checkout with remote `main` before running anything new. A local commit or a partial upload does not establish publication. Finish and verify any pending publication before starting its successor experiment.

Every decision needs an append-only ledger receipt stating the choice, why it was made, how it contributes to the purpose, and its outcome or pending state with evidence. Record the choice before acting, then append dated outcomes and corrections. This includes design, implementation, experiments, interpretation, delegation, publication and stopping decisions. Mechanical executions of an already recorded choice belong in its evidence. Keep a running record and publish small reviewed checkpoints to `main`, including failed or interrupted work, so recovery does not depend on this conversation. Follow [the publication workflow](docs/workflows/publish.md) and record the verified remote commit and tree; connector-created commits can differ from local commits while containing the same tree.

[Current state](docs/STATUS.md) records what ran and what remains open. [The workflow index](docs/workflows/README.md) tells a future operator where to read and write. [The semantic guide](docs/SEMANTIC_GUIDE.md) separates task behavior from claims about creativity. [The experiment method](docs/EXPERIMENT_METHOD.md) states the comparisons and their limits. [Language Proposal Theorems](docs/LANGUAGE_PROPOSAL_THEOREMS.md) works through twenty conditional results about expression, resources, language changes and epistemic claims. [Problem promotion](docs/PROBLEM_PROMOTION.md) explains how an encountered issue becomes a successor inquiry without turning its diagnosis into an accepted fact. [The branching research agenda](docs/RESEARCH_AGENDA.md) supplies discriminating follow-ups, an original second-domain scenario and a proposed construction-and-promotion configuration after the frozen first studies.

| Location | Use |
|---|---|
| `src/creib/forge/mini/` | Extracted Mini engine; existing import namespace retained for provenance |
| `src/minireason/` | Original templates, task interpreters, DeepSeek adapter and experiment driver |
| `experiments/plans/` | Frozen questions, initial-proposal conditions and methods, written before their runs |
| `experiments/templates/` | Generated original configurations with their rationale |
| `experiments/records/` | Original proposal bytes and complete run evidence, including unsuccessful and interrupted work |
| `docs/errata/` | Failures, evidence, causes and corrections |
| `docs/lessons/` | Separate lessons about configuration, method, semantics and operations |
| `docs/workflows/` | Hooks for continuing, freezing proposals, testing, diagnosis, publication and review |
| `docs/DECISION_LEDGER.md` | Append-only decision receipts, outcomes and publication checkpoints for recovery |
| `docs/reviews/` | Independent substantive readings of explanations, criticisms and realized behavior |
| `tests/` | Offline checks for engine integrity and experiment machinery |

The [construction inquiry workflow](docs/workflows/inquiry-study.md) now supports four-stage construction, criticism, proposed revision and unresolved problem promotion. It preserves the original source packet and proposed languages, provides the same conditional prompts through direct and Mini routes, and records each new output separately. Queuing a problem does not endorse its diagnosis or install a language change.

## Local setup

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
```

Live calls read `DEEPSEEK_API_KEY` from the process environment. Keep it out of files that are committed. Calls, content, usage and failures are recorded; native hidden reasoning text is discarded. Live commands and the current experiment state are documented in [the continuation workflow](docs/workflows/continue.md).

Up to five configuration tests may run concurrently. After every configuration test, preserve the original proposal, result, causes and decision receipts, then commit and push to `main` immediately. One publisher verifies the remote checkpoint before successor work starts. Do not wait for a successful outcome before publishing. Every finite stopping point must explain the remaining alternatives; reaching a resource ceiling does not mean the search space is exhausted.
