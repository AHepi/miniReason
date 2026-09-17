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
