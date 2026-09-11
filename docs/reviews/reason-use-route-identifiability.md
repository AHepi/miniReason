# What the frozen reason-use routes can distinguish

For the frozen E016–E020 plans, matched direct and actual Mini implement the same conditional policy for messages delivered to the provider. Given the same provider transition law and successful host transport, they therefore permit the same model-output traces and induce the same distribution over those traces. Different independently sampled answers cannot, by themselves, identify a benefit from Mini's reasoning mechanism. Mini's additional persistence and routing receipts remain real system features, but this configuration does not expose them as an additional source of reasoning to the model.

This is a bounded source-and-plan argument. It uses [the study runner](../../src/minireason/reason_use_study.py), [the Mini adapter](../../src/minireason/reason_use_mini.py), [the provider adapter](../../src/minireason/provider.py) and the five frozen plans. It draws no substantive conclusion about E019 and selects no further live experiment. At the parent's reported final execution checkpoint, E020 remains unrun: there is no no-return outcome available. Its row below describes a frozen plan only. The source-level argument does not substitute for that missing observation; the experimental block remains blocked rather than evidentially closed.

## Decision receipts

| Receipt | Choice | Why | Contribution to the end goal |
|---|---|---|---|
| ROUTE-D1 | Compare actual provider payload construction rather than arm names or archived Mini briefs. | Host labels and a different execution engine do not necessarily change anything available to generation. | Identify whether the comparison contains the proposed causal mechanism. |
| ROUTE-D2 | Prove equality conditionally on the provider law and host transport, and separate that from operational behavior. | Backend state and route-specific failures can invalidate unconditional equality of observed completed records. | Make the scope and possible defeaters of the argument explicit. |
| ROUTE-D3 | Treat persistence, route checks and model-facing construction as distinct possible contributions. | Their benefits require different observations; none is established merely by the presence of a ledger or a good answer. | Preserve useful engineering functions without attributing an untested creativity effect. |
| ROUTE-D4 | State the necessary change for a discriminating successor without choosing a live trial. | More draws from the same conditional policy do not create the missing intervention. | Direct subsequent allocation toward a concrete, refutable mechanism while preserving the frozen block. |

## What reaches the model

`reason_use_study._direct` calls the shared `stage_prompt` and sends two messages: the frozen system message and its rendered user message. `reason_use_mini._ProseResponder.reply` first validates the complete Mini brief, reconstructs the designated prior response from the actual response port, then calls that same renderer and sends those same two messages. Mini's artifact IDs, port headings, `mini_kind` coordinate and JSON return contract are recorded locally; the adapter does not add them to the provider messages.

The model returns ordinary prose. Mini's adapter subsequently duplicates it into host-generated `body` and `commitments` fields for storage. That wrapper is not another model call, a separate criticism, an independent commitment or a model-visible constraint. Both direct and Mini validate the public response through `validate_response`. The selected Mini kinds are freeform, use one call each, have no retries and install no proposed changes. Attention is off in the compiled configuration.

| Element | Matched direct and corresponding Mini route |
|---|---|
| Respond messages | Same frozen system, response instruction, complete common source, J and selected supplemental criticism |
| Use messages with return enabled | Same frozen system, use instruction, finite data, questions and exact prior response text |
| Use messages with return disabled | Same preceding fields, with an identically empty returned-account field |
| Model and endpoint | `deepseek-flash` at the declared DeepSeek chat-completions endpoint |
| Thinking-disabled pair | `matched` and `mini` both send `thinking.type=disabled`; no reasoning-effort field is sent |
| Thinking-enabled pair | `matched_native` and `mini_native` both send `thinking.type=enabled` and `reasoning_effort=high` |
| Other wire settings | `stream=false`, `max_tokens=32768`; neither route requests a JSON response format or sends seed, temperature or top-p |
| Host allowance | Two model calls, the same 180-second per-request timeout setting, and no automatic retry |

Provider-default sampling is an omission from the wire request, not a guarantee that backend defaults never change. Comparing native and disabled-thinking arms crosses a real provider setting; the equivalence claim pairs routes within the same setting.

The frozen plans share prompt-policy identity `e0572517bab06248b53691aaca9483eed703b50110b47714f32b4d5296b2733b` and probe-source identity `1e40b47c8f601f8d149bc97a13a4ad4f5cf6d273f22664f26e0b824ad1e67ba8`.

| Frozen plan | Supplemental criticism | Return path | Relevant route pairs |
|---|---|---|---|
| [E016](../../experiments/plans/E016-reason-original.json) | Original R | Present | Both thinking settings |
| [E017](../../experiments/plans/E017-reason-recoded.json) | Reviewed recoding | Present | Both thinking settings |
| [E018](../../experiments/plans/E018-reason-different.json) | Capacity criticism | Present | Both thinking settings |
| [E019](../../experiments/plans/E019-reason-omitted.json) | Empty | Present | Both thinking settings |
| [E020](../../experiments/plans/E020-reason-no-return.json) | Original R | Absent | Both thinking settings |

In E016–E019, bare/native also use exactly the same first-call policy as their respective matched/Mini modes. They stop after that response. Their terminal answers therefore address the response task, not the later use task; comparing those unlike terminals cannot identify an advantage from additional stages.

## Conditional equivalence argument

Fix one plan and one thinking setting. Let `x` collect its frozen source, J, selected criticism, finite use material and instructions. Let `r` be the fixed return-path Boolean. Write `M1(x)` for the complete first-call payload and `M2(x,y,r)` for the complete second-call payload after public response `y`. By inspection of the two adapters, both routes implement these same functions. In particular, `M2` contains the exact text `y` when `r` is true and is independent of `y` when `r` is false.

Assume a provider transition law `K` that is the same for both routes given the delivered payload and the relevant provider state. Assume those provider states have the same relevant law across the compared routes, and that local routing, serialization, validation and persistence do not introduce different stopping or filtering for the considered outputs. These are explicit assumptions about the comparison, not facts established by an API model name.

For successful execution, the common public-content trace law has the form

\[
K_1(dy\mid M_1(x))\;K_2(dz\mid M_2(x,y,r)).
\]

The stage subscripts allow stage-dependent kernels, provided the corresponding stages have the same law across routes. Hidden provider state can instead be included explicitly in the transition; the equality requires its relevant initial and transition laws to agree as well.

The proof is two steps. The first payload is identical, so couple the first provider draws to obtain the same public response `y`. The adapters preserve that response exactly. The second payload is then identical, whether it carries `y` or an empty field. Couple the second draws and the public use response `z` is also identical. Thus each coupled admitted trace is shared, and any property of the resulting public contents has the same law under the stated assumptions. Actual experiments need not use coupled draws; the coupling explains the equality of distributions, not an expectation of verbatim equality between independent samples.

With return disabled and a stateless common provider kernel, the use payload and its law do not depend on the discarded first response. The host still spends and archives that first call. This is a genuine declared intervention relative to returning the account, but is the same intervention in direct and Mini. Likewise changing the supplemental criticism changes a real first-call input. These conditions can investigate criticism and account availability even though the route label adds no distinct model-facing mechanism.

## What the argument does not equate

Mini produces extra manifests, source-copy artifacts, port-validation receipts, content-addressed blobs and replayable events. Direct already preserves requests, outputs, occurrences and resource receipts, but does not produce that same engine record. Recoverability, refusal of misrouting, interruption behavior, human inspection effort and host overhead are therefore distinct system questions. This document neither assumes those benefits are absent nor claims they have been measured by the model-content contrast.

A host fault can also stop Mini after a response while direct continues, or vice versa. The full processes, including failures, wall-clock time, timestamps and archive formats, are not asserted identical. The theorem's common-transport assumption must not be replaced by silently discarding failed arms. If completion depends on route and output, conditioning only on completed traces can introduce selection differences; these would require an operational explanation before attribution to reasoning.

Equal payloads also do not guarantee equal actual backend state. Calls may encounter different cache contents, batching, service load, request timing, replicas, model revisions or other unobserved provider conditions. Cache counters measure reported usage, not proof of equal numerical execution. Mini's host work can change dispatch timing. Equal model labels and settings do not rule out these differences. Persistent outcome differences could challenge the assumed common kernel or reveal an operational effect, but would not by themselves identify a Mini reasoning advantage from information that this adapter never supplies.

This is consequently not a theorem that Mini is universally useless. It concerns this configuration's provider-facing policy, on its admitted execution domain, under named assumptions. It does not cover a Mini arrangement that selects different evidence, changes context after a criticism, invokes a tool, revises scheduling, or resumes a materially different continuation after interruption.

## What would make a successor discriminating

A proposed cognitive contribution needs a reachable history at which the candidate changes a model-observable input, available operation, continuation or resource allocation relative to its control. The change must have a stated reason linked to a task obligation and a possible outcome that would defeat that reason. Changing an arm name, retaining another host receipt or repeating these identical conditional policies is insufficient.

For example, a later design could test a deterministic context-selection rule under a binding context budget, an external check whose result becomes available to subsequent inquiry, or recovery that restores material a comparison route cannot otherwise access. Such mechanisms must preserve prose criticism's legitimacy and must not make a checker or scheduler decide semantic bearing. These are possible design families, not selected experiments.

The matched control must then isolate the claimed component: comparable information opportunity, model setting and resource conditions, with any added calls or evidence accounted for. The task must contain a specific unresolved dependency that the component could help expose or preserve; an exact-message control remains useful for transport parity but cannot simultaneously serve as a contrasting cognitive intervention.

If the proposed value is instead persistence or routing integrity, the discriminating observation should concern that function directly, such as a declared interruption or misrouting case and the resulting recovery or refusal. A change that helps a human maintain the inquiry can be valuable without being attributed to better model generation. No such successor is activated by this review.
