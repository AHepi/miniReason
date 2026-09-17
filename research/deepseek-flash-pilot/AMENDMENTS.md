# Pilot amendments

## P-A1 - owner-directed self-continuation and spend guard (2026-09-17)

**Status:** prospective amendment. P-A1 changes the host contract and its
offline qualification. It is not evidence of live provider acceptance,
owner-task reliability, better answers, creativity, or an advantage over a
matched multi-call control.

The owner set the priority in these words: "the token spend isn't as important as the capability. And the ability for V4 flash to decide to keep running a loop or two." The owner then clarified: "More loops."

The owner also recorded this condition verbatim on 2026-09-17: "the DeepSeek balance is about USD 26 and cannot be topped up for a week; the Ollama credit may run out within a day." Capability remains the priority: the ceiling is a guard against runaway loops, not a target.

### Declared before/after contract

| Setting | Published pilot before P-A1 | P-A1 |
|---|---|---|
| Full passes | Exactly one `route -> spawn -> assemble -> verify` pass | No fixed pass count. After every verification the pilot records `continue_or_stop`; `continue` starts another complete numbered pass. |
| Continue authority | None; verification ends the run | The pilot decides, subject to host validation, its saved stop rule, duplicate-pass refusal, the logical-call ceiling, and the spend ceiling. |
| Call ceiling | `max_calls` default and maximum 24 physical attempts, including repairs | `max_calls` is a positive logical-call ceiling, default 300; a task may declare a higher positive value. One schema repair is a second physical attempt within the same logical call. Every attempt contributes usage and estimated spend. |
| Spend ceiling | No host-computed task spend ceiling | `max_spend_usd` defaults to USD 6.00 and may be overridden by the task. The host estimates cumulative spend from recorded usage and `PRICES.json`; reaching the ceiling stops the task. |
| Spawn fan-out | Default 3, hard maximum 8 | Each pass admits 1 through 24 outer subtasks; at least one matches the routed primary template. Later passes may use a different valid template mix. |
| Spawn depth | Maximum 2 | Maximum 3 within a pass. Deeper recursion is refused; another pass is required. |
| Repeated work | No cross-pass identity because there is only one pass | Before workers run, the host rejects a pass with the same template mix and canonical normalized subtask-input hashes as any earlier pass. The pilot may decide again twice; a third identical proposal stops the run with the host reason recorded. |
| Verification input to control | Verification terminates | The exact verification reference and outcome, including checker result, cross-lineage objections, or unavailability, are supplied to every continuation decision. |
| Reports | One route/spawn/assembly/verification view | `TRACE.md` and `RUN.md` show every numbered pass, routed template, spawned work, assembly, verification, continuation decision verbatim, per-pass usage/estimated spend, and cumulative calls/usage/estimated spend. |
| Tool manifest | `route`, `spawn`, `assemble`, `verify` | Adds `continue_or_stop`; the other tools retain their published authority. |

P-A1 does not change provider-key handling. Keys remain environment-only and
never enter tasks, prompts, reports, or custody records. It does not change the
published checker sandbox, checker allowlist, wall limit, output limits, or
durability rules. It does not add filesystem, shell, network, publication, or
self-modification authority.

### `continue_or_stop` contract

The tool body has exactly four required fields and rejects extra fields:

```json
{
  "decision": "continue",
  "reason": "sha256:<exact verification_ref supplied in the decision input>: the checker reports an unresolved boundary case",
  "what_changes_next": "Switch the primary template to decompose_synthesize and split the boundary analysis from the counterexample search.",
  "stop_rule": "Stop when verification has no unresolved checker failure or critic objection that can be addressed with available inputs."
}
```

`decision` is exactly `continue` or `stop`. `reason` and `stop_rule` are nonempty strings. `what_changes_next` is a required string and may be empty on `stop`. `reason` must contain the exact verification
reference supplied to the decision and explain how that result bears on the
choice. When verification is unavailable, the supplied unavailable reference
and status must be named instead. For `continue`, `what_changes_next` must say
which template or subtask mix will change and why; the host rejects an
identical pass before worker dispatch. For `stop`, `what_changes_next` may be empty because there is no next pass.

The first valid decision saves the stop rule. A later decision may repeat that
string exactly or add a nonempty earlier-stop condition by returning the exact
previous string followed by ` OR ` and the added condition. The host permits
no other change. The original rule therefore remains operative; an added OR
condition can only create another stop event. It cannot silently weaken or
replace the rule.

The decision is one logical call. If its public JSON fails the schema, the one
permitted repair is a second physical attempt carrying the rejected public
answer and exact validation error. The repair does not create another logical
call, but its recorded tokens and estimated cost are charged. A second schema
failure stops with the actual schema reason.

Each decision input carries the numbered pass, exact verification result,
cumulative logical calls and physical attempts, remaining logical calls,
cumulative recorded usage, estimated task spend, remaining estimated dollars,
and the saved stop rule. A continuation never raises either ceiling. If the
logical-call budget cannot admit the next required action, the host stops with
`CALL_BUDGET`; if the spend estimate reaches the ceiling, it stops with
`SPEND_CEILING`.

### Spend estimation and uncertainty

`research/deepseek-flash-pilot/PRICES.json` is the price authority for this
amendment. It records the official documentation URL, date read, token units,
and applicable prompt, completion, and reasoning treatment for every
listed DeepSeek Flash and Ollama route. Future or otherwise unmapped
routes remain token-accounted with price `unknown`; they do not receive a
fabricated dollar value.

Estimation uses provider-recorded usage, the rates in `PRICES.json` and the
component rules in `src/minireason/pilot/budget.py`, without double-counting reasoning tokens when a provider reports
them as part of completion tokens. A dispatched price-known call whose required
usage is absent stops the run as `SPEND_UNKNOWN`; unknown is never treated as
zero. Because actual usage is known only after a response, the estimate can
cross the ceiling by the final in-flight response. No later pass or call is
admitted after that result. `RUN.md` labels per-pass and total dollars as an
estimate from published prices, not a provider bill.

### Expected effect, possible loss, and falsifier

The expected effect is that DeepSeek Flash can inspect verification and decide
whether another materially changed construction pass is warranted, allowing
more loops while retaining finite host guards. The possible losses are higher
spend, prompt growth, repeated low-value work, and a later pass damaging an
earlier useful answer. Numbered immutable passes and explicit change reasons
make those losses inspectable.

P-A1 is falsified as an implementation claim if the offline scripted pilot
cannot complete three distinct passes and then stop under its own saved rule,
if an identical pass reaches workers, if a ceiling fails to stop with its
reason recorded, if verification or remaining budgets are absent from a
decision input, or if the transport-boundary double does not exercise the live
path. Passing those fixtures establishes only host wiring and accounting. It
does not establish live acceptance or substantive benefit.

Unaccepted child outputs remain inadmissible dependencies. If assembly is refused, the host records verification as unavailable with the preserved child results and still asks for a continuation decision; no checker success or accepted assembly is invented. Completed pass artifacts live under `passes/pNNNN/`.

Offline qualification: 77/77 pilot,346/346 reason (child TMP=C:/tr36) and26/26docs pins passed. See work/w38/INDEX.md for full test evidence, lesson IDs, failures and handoff limits. No provider call or Git mutation occurred in this engineering task.


## P-A2 - content-addressed inputs and scoped source reads (2026-09-17)

Declared and implemented offline in W45 from the W44 staged DeepReason port.
The owner's instruction is: "The parsing input machinery exists in DeepReason. Maybe just take it from there. It went through many cycles of iteration already".
The standing instruction is: "lean on all the fail modes and lessons learned when building new configurations."

Source: [AHepi/DeepReason](https://github.com/AHepi/DeepReason/tree/9607fba6f0a3066fbcab282c9ae0fad823e52e0c),
commit `9607fba6f0a3066fbcab282c9ae0fad823e52e0c`, MIT, Copyright (c) 2026 Aaron Hepi.
`inputs/canonical.py` and `frozen.py` retain the upstream bodies; `models.py`,
`parse.py`, `citations.py` and `preflight.py` carry the planned adaptations.
`adapters.py`, `service.py` and `__init__.py` are the scoped local bridge.
Provenance headers and the upstream LICENSE are retained. Every adaptation,
including the parser's UTF-8 boundary correction and disabled extraction
plugins, is listed in `work/w45/ADAPTATIONS.md`.

Task loading validates full SHA-256, byte length, strict UTF-8, role and exact
repository-relative path for each declared unit, then freezes the admitted
bytes. Legacy inline task inputs are registered as host-derived JSON units.
Route/spawn/planner controls use unit IDs and half-open byte ranges instead of
requiring the old 2,048-token normalized-input echo. Host resolution supplies
the actual input data to workers before the existing scope validation.
Mutable task/premise/candidate/objection overrides cannot replace sealed source
or protected obligations. Spawn receipts also carry content references.

`read_source` and each child's optional `source_reads` resolve only registered
units from sealed memory: no model path, filesystem search, shell or network.
Requested UTF-8 byte bounds must be valid. Model reads have a 65,536-byte limit;
host task JSON resolution is bounded at 262,144 bytes. A capped read reports
every omitted interval and its reason, without character replacement. Unpinned
paths/IDs, reader briefs, `.env` variants, `FW5-DERIVED-PROPERTIES.md` and other
derived-properties material are refused. Full FW5 and original episode files
are not added implicitly. UC1 checker/reviewer implementations remain host-only.

Every physical attempt, including the sole repair, preflights the exact
prepared wire body before dispatch or physical-attempt reservation. The rule is
`wire_utf8_bytes + completion_reserve + 8192 <= route_context_window`.
The recorded 2026-09-17 documentation premises are decimal 1,000,000 for
DeepSeek Flash and 256,000 for the explicitly declared hosted Qwen alias.
Each rendered text token consuming at least one UTF-8 byte and hidden rendering
fitting the reserve are assumptions, not measured tokenizer qualification.
Unknown routes, changed endpoint identities and native attachments/tools fail
closed. A refusal preserves prepared bytes, code and reason without dispatch.
Exact prepared, preflight and sent-wire hashes must still agree.

Per-attempt receipts distinguish literal source text/ranges from decoded JSON
object delivery; IDs in a catalogue are not exposure. Repairs keep the original
source and rejected public response. The byte-bound is not a spend guarantee.
Budgets, completion caps, P-A1 continuation/stop rules, checker sandbox, custody,
lineage, dependency and assembly rules retain their existing authority.

Final offline suites and four actual-task CLI fixtures are reported in
`work/w45/INDEX.md` and separately named `OFFLINE-VALIDATION-PA2` supplements.
No provider/model call, live acceptance, semantic result or comparative advantage
is established. Historical observations and sealed briefs remain unchanged.


### P-A2 independent judge correction supplement - 2026-09-17T13:07:44.232113+00:00

Pinned JSON task units now use the pilot strict duplicate-key parser and reject nonfinite values, including numeric overflow, before interpretation. All saved spawn-reference fields remain compact even for accepted legacy inline arguments. These corrections close the L10 parsing recurrence and the legacy spawn-record echo; original pinned bytes and provider observations remain unchanged. Root evidence, old-to-new custody and final offline qualification: `work/review45/INDEX.md`.


## P-A3 - live delivery repairs (2026-09-17 UTC)

Declared after the four preserved first live attempts at 2026-09-17T13:56Z,
under REC-20260917-D. The owner prioritizes capability and "More loops."
This amendment repairs delivery to the continuation path; it does not relax
custody to force a successful run. The four failures remain preserved in
`runs/pilot/UC*-attempt1-20260917T1356Z`; the owner reported combined spend under USD 0.03. The preserved
result estimates sum USD 0.031695504, slightly higher; per-task amounts
and this correction are in W46 DIAGNOSIS.

UC1 and UC3 reconstructed materially different input objects and first misplaced
`source_reads` at top level. Their sole schema repair removed that field but
left invented input text, triggering `OUTER_INPUTS_MUST_MATCH_SEALED_TASK`.
UC2's sealed task already has nonempty `documents`; its response supplied
`documents: []`, triggering `evidence_read requires nonempty inputs`.
These are class (b) prompt/delivery faults. No class (a) task-file correction
or class (c) normalization is justified: all four task/input pins stay unchanged.
UC4 is class (d): quote[4] inserts ellipses and cannot resolve to exact FW5
bytes; it also cites an unexposed source path. That refusal remains required.
Its missing exact-copy instructions and absent semantic repair were contributing
class (b) delivery defects.

The spawn prompt now includes an exact, copyable reference example for the
current task, explicit first-pass rules, and a per-child source-read example.
It distinguishes pinned hashes from paths, full JSON-unit bounds from excerpt
bounds, UTF-8 bytes from characters, and nested `source_reads` from top-level
fields. Tool descriptions state the same contract. The existing selected-template,
whole-input equality, source/scope, fan-out, dependency, depth and budget guards
remain enforced. No fabricated or undeclared input is admitted.

Outer spawn admission and evidence quote/reference checks now run within the
existing sole same-seat repair callback. Parseable schema and semantic errors
are collected together, including all detected quote and reference defects,
so one known error does not hide another until after the repair is spent.
The repair retains the original messages and exact rejected public response,
reports the precise failed fields/quote index and reason, and permits only a
bounded delivery correction. An unrepaired response is still refused after
one repair. There is no additional call retry or hidden-reasoning storage.

Evidence workers receive explicit source IDs, exact-copy examples and byte
locator rules. Every nonempty quote must resolve to exact UTF-8 bytes in its
named delivered source. `bytes:start:end` locators are checked against that
slice; historical prose locators remain hints and still require an exact
substring in the same source. No case, whitespace, punctuation or Unicode
normalization is used. Ellipsis-joined passages must become separate quotes;
paraphrase and uncertain attribution belong in the answer/unresolved fields.
Unauthorized `source_refs` and model-created verification refs remain refused.

Exact recorded public response bodies, custody hashes, wire evidence and replay
regressions are in `tests/pilot/fixtures/live-20260917/` and `work/w46/INDEX.md`.
Each task has separate `OFFLINE-VALIDATION-PA3` and `RUN-CONTRACT-PA3` successors;
earlier observations, validations, sealed briefs and manifests are unchanged.
Required suite transcripts and current source hashes are recorded in W46.
Offline replay and callable fixtures establish instrument behavior only; the
orchestrator owns any fresh live qualification. P-A1 continuation/stop rules,
spend/call ceilings, checker authority and lineage conditions remain in force.


## P-A4 - worker delivery under live returns (2026-09-17 UTC)

Declared after the four preserved second live attempts at
`runs/pilot/UC*-attempt2-20260917T1424Z`, under REC-20260917-D. P-A4 builds on
P-A3; it does not rewrite either live occurrence or relax sealed-input, source,
quote, budget, checker, sandbox, key-handling, or wire-custody authority.

The second attempt reached `ROUTE_VALIDATED` in all four tasks. UC1 then stopped
at logical call 7, pass 2: the nested `plan` worker received the complete
7,650-byte input range, was asked for as many as 24 structured steps under a
4,096-token cap, used exactly 4,096 completion tokens, and returned a 13,209-byte
prefix with `finish_reason=length`. UC2, UC3 and UC4 reached their
`evidence_read` workers and completed public JSON under the old 8,192-token cap,
but the host exhausted one repair and reported `SCHEMA_REJECTED`. Across those
six responses, all 45 quote strings resolve exactly once to their named exposed
source. All 29 authored numeric byte locators are false. The model also placed
nonempty prose in schema-permitted `verification_refs` on UC2 a00 and UC3 a00;
those model claims are not host verification receipts and remain refused.
Attempt-2 estimated spend is USD 0.058530000; with attempt 1 it is USD
0.090225504. Exact bodies, wires, ranges and per-run classifications are in
`tests/pilot/fixtures/live-20260917/ATTEMPT2-CUSTODY.json` and
`work/w47/DIAGNOSIS.md`.

### Delivery-tolerant response form

Every call receives its exact JSON Schema plus a filled `response_example`
built from that call's own task inputs, source IDs and input references. The
example demonstrates delivery form, not a solved answer. Declared prose fields
may arrive as a string, a list, or a nested prose object and are normalized to
the schema's canonical host shape before validation. Fields with declared
defaults may be omitted. The original provider bytes remain immutable beside
the normalized host value.

This tolerance does not apply to authority-bearing values. Exact identifiers,
source IDs, quote bytes, file paths, ranges, enums and unknown fields are never
normalized into validity. A model-created verification reference remains
unauthorized. Sealed task equality, source exposure, template input checks,
dependency order and assembly checks remain exact.

For evidence output, `source_id` and nonempty `quote` remain custody fields. The
quote must resolve as exact UTF-8 bytes in that exposed source, with no case,
space, punctuation, Unicode, or ellipsis normalization. `locator` is optional
prose and is an untrusted model hint. After exact resolution, the host records
all matching spans, preserves the authored locator in a
`quote-locations-resolved` event, and supplies a canonical
`bytes:<start>:<end>` downstream. A false authored numeric range is therefore
not relabelled true. Zero-match text, an unexposed source ID, an empty required
quote, or a model-authored verification reference still fails the contract.

### Output ceiling policy

Control roles `route`, `spawn` and `continue_or_stop` use 4,096 completion
tokens. Worker roles, including nested `plan`, default to 16,384. For each worker
the host records:

```text
needed output bound = routed range bytes + other work-product bytes + 4096 framing/prose bytes
```

The bound relies on the declared conservative premise `tokens <= UTF-8 bytes`;
it is an output envelope, not a prediction that arbitrary semantic work will
fit. If `needed <= 16384`, the worker uses 16,384. If it is larger, the host
raises the request to that route's reviewed maximum. If `needed` exceeds even
that maximum, `OUTPUT_RANGE_TOO_LARGE` refuses before dispatch and records the
policy and reason.

For `deepseek-flash`, the reviewed route maximum is 384,000, using the official
[DeepSeek 384K output statement](https://api-docs.deepseek.com/quick_start/pricing/)
with a conservative decimal interpretation. For
`ollama/qwen3.5-397b.native`, 65,536 is a P-A4 host-declared output maximum within
the [documented 256K total context](https://ollama.com/library/qwen3.5:397b-cloud);
it is not represented as an official Qwen
output limit. The complete serialized request must also pass the existing input
context preflight. Endpoint identity, documentation URL, scope and 2026-09-17
check date are written into each output policy receipt.

### Ceiling recovery and pass continuation

A worker `CEILING_HIT` records the call, exact public prefix, usage, finish
reason, range and policy. The prefix is never admitted as a complete worker
result. If the request was below the route maximum, the host sends the same
packet and range at the reviewed maximum as a new logical call. If a first
failure occurs at the maximum on one divisible unit range, the host creates two
nonempty UTF-8-safe half-ranges, records their exact read receipts, runs bounded
range workers, and synthesizes their accepted outputs under the original
schema. For multiple units the largest declared range is divided, with other
ranges recorded as deferred until synthesis. Public critic/assembly packets
without a unit are pinned as derived units first. Only an unsplittable UTF-8
range may be sent once more to establish repeated failure. Partial range
contributions remain partial; `WORKER_RANGE_INCOMPLETE` refuses an executable
plan synthesized from incomplete range work. `WORKER_CEILING_REPEATED` stops the pass after a
second failure of the same declared packet/range and records the reason.

`SCHEMA_REJECTED`, `CEILING_HIT`, `WORKER_CEILING_REPEATED`, and
`OUTPUT_RANGE_TOO_LARGE` no longer end the run merely because they stop one
pass. The host creates an unavailable verification result with its exact
failure reference and preserved children, then gives that result to the normal
`continue_or_stop` decision. The pilot may stop or select a materially changed
next pass under the P-A1 call, spend, duplicate-pass and stop-rule guards.

### Three repairs within one logical call

A logical call has initial attempt a00 and at most three schema/custody repairs,
a01 through a03. Every repair is separately recorded and charged. It retains
the original source/context and filled example, appends the immediately failing
public response bytes, and states the exact current validator reason and repair
number. It corrects delivery only; it is not a transport retry, task rewrite,
source invention, budget increase, or fresh solution authority. All four
physical attempts remain one logical call under P-A1 accounting.

If a03 still fails, the host raises `SCHEMA_REJECTED` with the last exact reason
and stops that pass. The failure becomes verification input for the bounded
continuation decision, which may route differently on the next pass. The run
still stops on its owner-set call or spend guard, an explicit pilot stop,
failure of the continuation control itself, or another concrete recorded
refusal. Repeated same-range worker failure ends its pass, not the run.

Keys remain environment-only. Hidden reasoning is not persisted. The checker
sandbox, allowlist, wall/output limits and P-A1 global budgets are unchanged.
P-A4 is prospective host behavior and offline qualification; it is not evidence
that a new live attempt succeeds, that more loops are useful, or that this arm
outperforms a matched multi-call control.


## P-A5 - multi-pass references and partial carry-forward (2026-09-17 UTC)

**Status:** prospective offline engineering amendment, resumed after the earlier
worker was interrupted by provider capacity. P-A3 and P-A4 remain in force.
Attempt 3 is preserved unchanged: UC1 reached 3 passes/10 logical calls then
`INPUT_REFERENCE_INVALID`; UC2 stopped after 1 pass/4 calls on an assembly
host-refusal; UC3 reached 2 passes/10 calls then `PLAN_NEEDS_BOUNDED_LEAF`;
UC4 reached 2 passes/7 calls then `INPUT_REFERENCE_INVALID`. The 31 logical
calls used 36 physical attempts and an estimated USD 0.136009704, not a bill.
The owner's capability and "More loops" priority motivates this change.

### Exact host reference menus and repairs

Before every delivered control/worker call the host generates and persists a
`reference_menu` at `passes/pNNNN/reference-menus/mNNNN.json`. It lists pinned
input units, recorded children, assemblies and verification results, with exact
IDs, byte counts, zero-based end-exclusive ranges, pass numbers, status and
ready-to-copy `source_read` objects. Prior-pass entries remain available. The
immutable host-artifact JSON envelope records its kind, original reference,
status and value; its content hash is the byte-read unit ID.

The namespaces are distinct. Compact `inputs` must select an entire JSON unit
whose role is `task_input` or `task_derived`; a public-source hash or raw source
slice is not task JSON. Source reads can select UTF-8-safe ranges of any exposed
unit, including recorded child/assembly/verification envelopes. Child `cNNNN`
references are dependency IDs; they are not byte-unit hashes. Nested plans may
name earlier steps or recorded child results as dependencies. The unchanged
outer-spawn schema exposes historical records through `source_reads`; it does
not acquire nested-plan-only `id` or `depends_on` fields.

Spawn/plan reference admission runs inside P-A4's recorded delivery validator.
An invalid ID, namespace, range, UTF-8 boundary or dependency receives the exact
failed response and predicate plus the valid-ID menu in a01-a03, within the
same logical call. No reference is silently aliased or invented. Synthesis and
worker output references likewise repair against their narrower allowed IDs;
being listed in the menu alone does not authorize a worker to cite unseen
bytes or to claim a host verification. Continuation repair names the required
actual verification ID. Failed repairs retain their original bytes and usage;
`SCHEMA_REJECTED` becomes pass-failure verification for the next decision.

### Bounded plan repair and recorded host splitting

The planner receives `bounded_leaf_contract`: at most 24 steps (or the lower
configured fan-out), maximum depth 3, allowed leaf templates `direct_answer`
and `evidence_read`, optional `decompose_synthesize` only below depth 2, a
strictly narrower task request per step, and the available unit sizes. A source
range alone does not make an unchanged parent task narrower. Attempt 3 UC3's
step16 used `critic_return` outside this template set; its 1,062-byte case source
was not proven too large. That original failure is not reclassified as a
measured size overflow.

`PLAN_NEEDS_BOUNDED_LEAF` now gets all three repairs with that explicit bound
and size list. If the last repair still fails this predicate, the host records
`host-plan-split`, selects the largest relevant input deterministically (size,
then unit ID), and partitions its exact bytes into contiguous UTF-8-safe ranges
of at most 4,096 bytes. Each `direct_answer` leaf receives its exact range read
and a narrower range-specific task. Sealed context remains available to
interpret a fragment; the work range does not claim smaller total context.
The host action records the parent, ranges, compact leaf inputs, failed call
and failure receipt. Global call/spend, fan-out and depth bounds remain active;
`PLAN_SPLIT_BOUND` or `CALL_BUDGET` can refuse an undispatchable split. There is
no random mutation or enlarged budget. Criticism and synthesis remain fallible.

### Partial carry, verification and readable outcomes

A coherent child with host `status=unaccepted`, `output_status=partial` and
nested `output.status=partial` can be carried. Its refusal reason, answer,
unresolved work and dependency digest are retained; the child is never
relabeled accepted or complete. Assembly produces a partial artifact. Nested
dependents and synthesis inherit partial status and unresolved refusal reasons.
Failed, cannot-decide or internally contradictory child records remain refused.

The normal checker or configured different-lineage critic runs on that partial
artifact. `continue_or_stop` receives the artifact and actual verification,
allowing the model to re-spawn work or change templates while preserving its
stop rule and declared source authority. It may still choose STOP; extra
passes are possible, not forced. A run with `status=partial` and at least one
recorded continuation decision is a readable outcome. `result.json` records
`readable_outcome`, the CLI exits successfully for that outcome, and `RUN.md`
explains that readable partial is not whole-task completion. Failed runs and
partial runs without a recorded decision remain unsuccessful CLI outcomes.

Credentials stay process-environment-only; `--env-file` is refused without
loading it. The checker sandbox, checker source and limits, global budgets,
P-A4 output ceilings/three repairs, sealed task authority and recorded usage
are unchanged. Task JSON and earlier offline companions remain unchanged; new
`OFFLINE-VALIDATION-PA5` and `RUN-CONTRACT-PA5` companions bind the qualified
source. Tests replay exact attempt-3 response bodies, execute real host paths
without provider calls, and exercise historical-artifact reads and repaired
synthesis. Offline scripted continuation does not establish attempt-4 success,
semantic merit or an advantage over matched multi-call controls.
