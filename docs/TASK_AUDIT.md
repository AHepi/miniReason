# Independent audit of the initial task and templates

**Scope:** source inspection and deterministic calibration of `src/minireason/tasks.py` and `src/minireason/templates.py`, before inspecting live campaign results. This is an audit of the experimental instrument and claim scope. It contains no model result and no creativity verdict.

The initial reservation task is coherent, solvable on the declared finite cases, and suitable for establishing that a model can construct a working program through Mini's actual ports. It is a weak discriminator of creativity. The task statement already supplies the key conceptual order, while much of the remaining difficulty is expression in a novel JSON language. The templates do wire candidate prose, the operative program and executable observations into criticism, which addresses a real failure mode of the inherited work. Several controls and attribution obligations remain absent.

See [the semantic guide](SEMANTIC_GUIDE.md) for ECS claim scope and [the experimental method](EXPERIMENT_METHOD.md) for the required comparisons. This audit does not certify the separate runner or provider; their actual effective settings, prompts, outputs and token accounts require inspection when records exist.

## Audited source identity

| File | SHA-256 at inspection |
|---|---|
| `src/minireason/tasks.py` | `35c443e653197236737431432175294a55ee395a706729f82c7c9fec0e445068` |
| `src/minireason/templates.py` | `4d8c763e5eddd1d331cbd778266a48a22b497524f9759a91ed4ae6dae15c552b` |

Any correction after this snapshot should append its disposition here or in the errata, with new source identity. The findings below are statements about these bytes, not claims that later corrected versions retain the same defects.

## What the task actually asks

Imagine several replicas delivering records about stock reservations. Records may arrive repeatedly and out of order. A booking's larger revision replaces all its earlier revisions. Its current version reserves its quantity only when it is a hold whose expiry is strictly after the declared logical time. A release or an expired latest hold reserves nothing. Older holds do not return when the latest one expires. Results include every stock item in sorted order, and negative available stock is deliberately retained to expose oversubscription.

This is a snapshot aggregation problem. It does not implement a distributed admission protocol, consensus, transactional reservation, rejection ordering or a continuing service under concurrent requests. The input excludes conflicting contents at the same booking/revision and excludes item changes for a booking. Those exclusions remove a major source of distributed interpretive difficulty.

The unrestricted prose body asks for mechanism, assumptions, defeating observations and preservation obligations. The commitments field contains the executable expression. The exact checker evaluates that expression only. It does not verify the account in the prose body.

## Solvability and the conditional account

A supplied calibration program in `tests/test_tasks.py` passes all five public cases and all twelve held-out cases. I independently executed that fixture against both batteries. This establishes that the implemented expression language can express a successful procedure for the cases; the fixture must stay out of live model packs and must not be reported as a model achievement.

There is also a straightforward conditional argument for the intended procedure. Partition events by booking. Nonconflicting versions and the maximum-revision rule make the retained version unique up to duplicate copies of the same record. Replaying or reordering deliveries therefore preserves that retained version. Test kind and expiry on that version, so an expired replacement cannot reveal an older hold. The immutable-item assumption places each active version in exactly one item total. Sum these quantities and subtract from capacity without clamping. Iterate the stock list, rather than only represented event items, to retain empty items. Sorting that list establishes output order.

That argument depends on the published contract, not empirical success alone. It also shows why the first task may be easy: the specification states almost every step of the conceptual procedure directly. It does not deliver a functioning JSON program, so nontrivial binding and assembly can still occur, but its contribution should not be described as independently inventing the reservation algorithm.

No maximum number of events, stock items or integer magnitude is declared in the task's input contract. An evaluator with a fixed 30,000-step ceiling cannot promise completion for arbitrarily large inputs. The available calibration algorithm repeatedly scans events by booking and scans stock by item, so ordinary input growth can exceed the ceiling. The valid engineering claim is completion on a declared bounded input domain, or correctness conditional on completion. Size ceilings should be supplied before any claim of total executable conformance.

## Findings and their consequences

| Finding | Evidence | Consequence and needed treatment |
|---|---|---|
| TA-01: integer output equality is not type-exact | `evaluate` uses Python `actual == expected`. Replacing all output integers zero and one with `False` and `True` still passes every public and held-out case | The claimed integer output contract is not fully checked. Use recursive type-sensitive comparison or validate result types. Re-evaluate prior outputs if this defect could affect them |
| TA-02: charged expression steps do not bound built-in work | `len(mul([0],100000))` returns 100,000 while charging five steps | Python's overloaded multiplication allocates a large list in one arithmetic node. Sorting, uniqueness serialization and integer arithmetic also do work outside node accounting. Restrict types and sizes, charge relevant work, or declare node-count semantics and contain process resources separately |
| TA-03: a clear task can saturate before criticism is needed | The prompt specifies latest-first replacement, no resurrection, strict expiry and no clamping; only two examples are shown, but the procedure is substantially supplied in prose | Initial all-pass outcomes would be a task ceiling, not evidence that additional configurations or creativity mechanisms have been exhausted |
| TA-04: execution feedback adds information | `task_prompt` shows only the first two public examples; the machine seat tests all five and supplies expected outputs plus the input for failures | A Mini versus direct comparison includes extra case evidence unless the baseline receives an equivalent feedback opportunity. Name that contribution separately |
| TA-05: no-return bundles multiple removals | `return_path=False` removes the critic and observations from revision; for multiple cycles it also removes the previous completed revision from the next proposal | A difference cannot isolate criticism carriage, raw feedback carriage or inter-cycle retention. Split the relevant ablations when the main result merits causal attribution |
| TA-06: no-return is not the operative installation control described in the guide | The initial template passes a prior final artifact into a later prompt. It does not install a newly constructed independent control program for a fresh task | This tests contextual return of content. It does not yet establish ECS deployment or retained owned capability |
| TA-07: held-out cases are a fixed, correlated battery | Four cases plus eight related replay/revision/expiry variants are generated deterministically; they are present in source before calls | Good regression coverage does not supply twelve independent draws or broad generalization. Exclude their bytes from packs and use new independent families after holdout-informed revision |
| TA-08: verifier and contract share authorship | `reference` is a separate Python implementation, but it embodies the same author's reading of the prose used to generate task and cases | Independence is implementation separation, not independent semantic authority. An outside account review and targeted checker counterexamples remain necessary |
| TA-09: explanatory criteria are unmeasured by task execution | `evaluate` parses commitments and compares outputs; the body is not examined | Exact passes cannot establish the five ECS accounting clauses, reason use, New, Build, Repair or CreateEK without their additional witnesses |
| TA-10: manifest display identity omits a resource override | `manifest_id` includes task/template, feedback, return and cycle settings but omits `completion_tokens_per_call` | Treat the complete effective manifest hash as the configuration identity. The human-readable ID alone cannot identify an experimental condition |
| TA-11: the language is more permissive than its description | Unknown fields on known operation objects are ignored; `if`, `not`, `and` and `or` use Python truthiness while only `filter` demands booleans | The phrase 'every field is exact' is not enforced as an exact schema. Either tighten validation or document the interpreter that actually runs |
| TA-12: the three templates manipulate several instruction features | The preservation and rival templates change proposals, criticism and revision wording together | Main comparisons test complete template packages. A later ablation is required before crediting one instruction clause or mechanism |

TA-01 and TA-02 are concrete instrument defects, not objections to ECS. TA-03 through TA-12 bound the claim or identify missing comparisons. None justifies throwing away a completed record. Invalidated measurements stay in the history with their corrections.

## Deterministic audit receipts

The audit made **zero model calls**. A supplied calibration program succeeded on both batteries. A wrapper replaced every numeric zero/one in its `reserved` and `available` outputs with booleans, retaining other numbers. Both batteries still reported `all_pass: true`. JSON booleans are not integers under the declared task language; this is an actual unsound acceptance of that part of the output contract.

The work-accounting witness is small and reproducible:

```json
{"op":"len","value":{"op":"mul","args":[[0],100000]}}
```

At the audited revision, `execute` returns `(100000, 5)`. This witness does not attempt resource exhaustion. It establishes the mismatch between expression-node counting and bounded runtime work. The solution is not to turn an operating-system containment failure into a semantic refutation; V1.3 §1 expressly forbids that move.

## What is already well designed

The candidate and its commitments are rendered together. The critic can inspect the actual executable expression, rather than a prose summary alone. The machine feedback retains per-case failure inputs and expected outputs, making causal diagnosis possible. Criticism instructions permit uncertainty and explicitly distinguish a language/translation error from a false prose account. Revision can retain a candidate when an objection fails instead of manufacturing an accusation. Programs are data with no explicit file, import or network operation, making the execution boundary inspectable.

These are substantive improvements in experimental legibility. They are still mechanisms to be checked in actual run receipts: a port declaration is not proof that relevant content reached a particular call, and receiving it is not proof that its meaning governed the response.

## Missing controls for interpretation

The user-required bare, candidate-template and supported native-reasoning comparisons must be visible in the actual runner evidence. Neither `tasks.py` nor `templates.py` implements the direct/native arms, so this audit cannot certify them. Freeze the same model, task and initial material, and retain effective provider settings and actual token accounting. A native mode must be a supported provider control, not a stronger instruction.

Extra model calls and extra executable feedback need separate controls. Repeated direct attempts under the same aggregate ceiling reveal sampling gains. A serialized workflow with equivalent instructions and feedback but no Mini artifact/routing machinery helps isolate what Mini adds. Giving the direct model the same visible public feedback after its initial program is a particularly useful comparison here because the first task is deterministic and narrowly specified.

For return, preserve raw observations while removing only criticism; preserve criticism while removing raw observations; for multiple cycles, vary prior-final carriage separately. Those conditions identify what is being returned. Installation versus archival custody on a later fresh task is a further test, not another name for these prompt ablations.

For reason use, compare a content-preserving recoding, a relevant changed criticism, removal of the operative reason and irrelevant padding. Use the resulting program's behavior as well as the explanation. A cited identifier alone does not establish the active route required by ECS §5.2.

Independent explanatory review should read the exact body and program, inspect source-to-operation anchors, identify the question and respect actually answered, and seek a counterexample to compositional and non-circular claims. It should record unresolved obligations rather than turn program success into a holistic creativity score.

## The next task should require repair of an assumption

If the first task is solved immediately, changing temperatures or adding more criticism stages has little discriminatory value. The next useful condition is a **conflicting-revision reservation snapshot**, with a new task identity and fresh cases. Keep the original task and its results intact.

In that new protocol, disconnected replicas may supply different records at the same highest revision. Neither delivery order nor an unprovided authority identifies a winner. Lower revisions remain superseded, but all distinct highest-revision records are compatible candidate versions. The question is which reservation totals are forced and which remain underdetermined. Ask for exact per-item minimum and maximum compatible reservation totals, and the corresponding availability bounds. Cases with no conflict must collapse to the old exact result; this is the protected behavior. Include conflicts between hold and release, different quantities, and active versus expired holds, with duplication and order changed independently.

This deliberately attacks the old uniqueness assumption instead of adding arbitrary formatting difficulty. A program that chooses the first tie may continue passing ordinary cases but cannot justify a unique answer where the evidence leaves alternatives. The correct account must say what the observations do and do not identify. ECS §9.1 explicitly allows repair by replacing a false identification with a correct account of underdetermination.

The experiment begins from a prior executable organization that worked on the original task. Compare direct repair, native repair, and Mini repair with equivalent access to the changed contract and feedback. Record the change actually used, preserve old unambiguous behavior, and test fresh conflicting cases. A program rewritten wholesale can still succeed, but it gives different evidence about retained structure than a localized, explained change. Do not force minimal edits as a merit criterion.

This is still a bounded program-construction task and the DSL remains an enabling contribution. It is better aligned with explanatory repair because a load-bearing assumption must change and an unwarranted definite answer is a real failure. It still cannot certify historical novelty or refute ECS by itself.

## Scope of the first result

A first live run can show whether the provider delivered a usable program, whether the template's paths actually operated, whether an observed failure was repaired under the finite tests, and whether a matched baseline already suffices. It cannot prove creativity from seventeen passing examples. A null difference on this task does not establish that Mini is useless; an advantage does not establish that the artifact machinery caused it. Any stronger conclusion needs the missing controls and the semantic conjuncts identified above.

## Live-output review pending

No live response was read for this audit. Once the first run is available, append a separate review of its exact prose, program, criticisms, revision and bounded outcomes. Preserve this pre-result task diagnosis so the interpretation cannot be rewritten around whichever arm wins.
