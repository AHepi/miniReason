# DeepSeek Flash self-piloting study

This directory contains the capability reading, twelve live interface probes,
their immutable public records, and a minimum viable host-controlled pilot.
The probes passed 12/12 declared criteria: all five obvious routes were
selected coherently, three emitted function calls satisfied their schemas,
the tool follow-ups stopped voluntarily, spawn returned a valid three-node
DAG, and both 4,096-token thinking fixtures completed. See
[`PROBE-RESULTS.md`](PROBE-RESULTS.md) for the per-call evidence and limits.

The implementation is in `src/minireason/pilot/`. It provides the five
catalogue templates, deterministic route correction, bounded spawning,
assembly, checker-or-critic verification, immutable call custody, run reports,
an offline/live CLI, and an OpenAI-compatible function manifest. It is a host
orchestrator. It does not grant the model filesystem, shell, network, or
self-modification powers.

## First offline run

From `C:\Dev\miniReason`:

```powershell
$env:PYTHONPATH='src;tests'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:TMP='C:\tw34'
New-Item -ItemType Directory -Force -Path 'C:\tw34' | Out-Null
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -B -X utf8 -m minireason.pilot run `
  --task research/deepseek-flash-pilot/examples/direct.task.json `
  --mode offline `
  --scripted research/deepseek-flash-pilot/examples/direct.scripted.json `
  --out C:\tw34\pilot-direct `
  --max-calls 24
```

`--mode offline` is the default, but it is explicit above. Offline mode
requires `--scripted <JSON-list>`; it does not fabricate answers. An
`--env-file` argument is ignored and left unopened offline. The output path
must be a fresh, short directory. The direct fixture consumes three scripted
provider-shaped responses: route, spawn, and answer. Its local checker adds no
provider call.

Read these outputs in order:

1. `ANSWER.md` for the working answer and terminal status.
2. `RUN.md` for limits, attempt receipts, modes, and stop detail.
3. `TRACE.md` for state transitions and tool decisions.
4. `verification/result.json` for exactly what the checker or critic tested.
5. `calls/` for per-attempt decision, request, response, usage, latency, and
   custody evidence.

`task.json`, `catalogue.json`, `tools.json`, `endpoints.json`, and
`config.json` freeze the run inputs and implementation identities. Original
attempts remain separate from the Markdown views.

## Owner-controlled live run

Start with the checked-in direct task below, then create your own task JSON and
choose a new output directory. This command needs only the DeepSeek key; its
sealed arithmetic checker makes no additional provider call. Supply provider
keys through existing environment names, or opt into the existing restricted
reason CLI loader with `--env-file`. Never place a key in the task, scripted
responses, command output, or run directory.

```powershell
$env:PYTHONPATH='src;tests'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:TMP='C:\tw34'
New-Item -ItemType Directory -Force -Path 'C:\tw34' | Out-Null
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -B -X utf8 -m minireason.pilot run `
  --task research/deepseek-flash-pilot/examples/direct.task.json `
  --mode live `
  --env-file .env `
  --out C:\tw34\pilot-live-001 `
  --max-calls 24
```

The env-file loader accepts only its declared provider key names and does not
log values. Live mode is opt-in. The integrated pilot was not exercised with
a provider during this build, so inspect every public result and custody
record rather than treating a completed state as an accuracy certificate.

The task file is one JSON object. `task` is required. Optional top-level
fields are `features`, `inputs`, `check`, and `critic_seats`. `features.kind`
may be `direct`, `evidence`, `engineer`, `critic`, or `decompose`; the host
corrects an invalid or unsuitable model route deterministically. Omitted input
fields receive empty defaults, but fields required by the selected template
must be nonempty. See the checked-in [task and scripted response examples](examples/)
for complete starter shapes. The env file must be ignored and untracked inside this checkout.

## External function-calling harness

`src/minireason/pilot/tools.json` is the generated manifest for `route`,
`spawn`, `assemble`, and `verify`. It carries `strict:true` for the beta strict
tool endpoint whose small probe passed; the full manifest has only offline
validation so far. Unsupported string/array length keywords are omitted from
the wire schema and enforced by the stronger host schemas. When using an ordinary endpoint, remove
the `strict` member from each function definition. Keep every control turn at
thinking disabled.

Instantiate the stateful host with:

```python
from minireason.pilot.pilot import Pilot

total_budget, control_budget = 24, 8
# The harness enforces at most eight control attempts, including repairs/final answer.
pilot = Pilot(task, out, mode="live", max_calls=total_budget-control_budget, scripted=None)
```

Each model tool call must arrive in the ordinary OpenAI shape:

```json
{
  "id": "call_001",
  "type": "function",
  "function": {
    "name": "route",
    "arguments": "{\"template_id\":\"direct_answer\",\"reason\":\"A short closed task.\"}"
  }
}
```

Call `pilot.dispatch(tool_call)`. It validates order and arguments, records the
host action, and returns a message shaped as:

```json
{
  "role": "tool",
  "tool_call_id": "call_001",
  "content": "{...public host result...}"
}
```

Append both the assistant tool-call message and the returned tool message to
the control conversation, then request the next action. Serialize these
stateful actions in the order `route`, `spawn`, `assemble`, `verify`. Reusing a
tool-call ID with identical arguments returns the recorded result; reusing it
with different arguments refuses. Call `pilot.finish(detail)` once the host
has reached a terminal state so `result.json`, `ANSWER.md`, `RUN.md`, and
`TRACE.md` are written.

The external harness owns the control-model HTTP exchange. It must preserve
the exact wire request and public response, returned model, tool-call IDs and
arguments, epoch and latency, usage, finish reason, and reasoning-presence
flag. It must not persist hidden reasoning. Count control calls and their
repairs in the same global run budget as worker calls. Reserve a control allowance
C before construction, give the Pilot at most N-C worker attempts, and enforce
at most C control attempts in the harness. The example reserves 8 of 24. Stop
when either reservation is reached; do not silently transfer or raise limits.
Keep control request/response receipts beside the run and bind their tool-call
IDs to the host action receipts. The manifest alone does not provide that HTTP
recording or control-budget enforcement. The current built-in
CLI uses the probed JSON control envelopes because the existing reason
`Adapter` does not retain and round-trip tool calls.

## Bounds and interpretation

- Default fan-out is 3; the hard host bound is 8. Maximum depth is 2, and a
  decomposition already at depth 2 cannot decompose again. A nested spawn
  needs a new host receipt.
- `--max-calls` is at most 24 and includes recorded schema-repair attempts.
  The built-in host dispatches children sequentially. Any external scheduler
  must serialize stateful tools and keep active provider requests at or below
  five.
- Each schema-invalid public worker answer gets at most one repair. There is
  no transport retry, overwrite, automatic resume, or replay of an uncertain
  delivery. A new occurrence needs a new directory and decision.
- Thinking is disabled for control and current worker calls. Hidden reasoning
  is never a required custody input and is not persisted.
- The engineering template produces a patch proposal only. It does not change
  files or execute claimed tests, and it remains partial until the owner does
  that work and records it separately.
- Critic-dependent work requires an owner-supplied, thinking-off-capable
  endpoint from a different model lineage. If it is unavailable, the result
  is partial or cannot-decide rather than an invented independent check.
- A local checker establishes only its sealed proposition. A critic verdict
  is fallible. Contract-valid JSON, agreement, and terminal `complete` do not
  establish general correctness or creativity.
- There is no price guarantee. Input counts, current provider prices, control
  calls, worker calls, and repairs must be budgeted by the owner. The pilot
  does not self-modify or raise its ceilings.


## Offline qualification

The W34 build passed 46/46 tests under the specified Windows Python 3.11.9,
including all five template paths, recorded repairs, dependency bounds, source
quotes, checker agreement/disagreement/refusal, independent-lineage checks,
replay refusal, assembly tamper refusal and invalid-router fallback. Two
separate CLI fixtures completed with three scripted calls each. No live
provider call was made by this build. Run the suite with:

```powershell
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -B -m unittest discover -s tests/pilot -t . -v
```

Task JSON is sealed as canonical data; the original task string and supplied
document strings retain their characters. Checker source/expected values are
host-sealed and excluded from worker and router prompts. Checker qualification
is the existing personal Windows guard, not a new OS sandbox or durable
scheduler qualification.

## Judge qualification limits - 2026-09-17

The CLI env-file route requires this source checkout's `tools/reason.py`; it
is not a standalone wheel entry point. The first live command above uses the
same shipped task exercised with a transport double. That test is not a new
provider run. A normal first pass is three provider calls, with at most one
schema repair for each and the declared global cap.

This MVP suits short task packets. The spawn control must echo the complete
normalized inputs within its 2,048-token output cap, so large source documents
can fail before a worker runs. Input-reference spawning and near-window
handling are NOT FOUND. Quote custody failures stop the template; only JSON
syntax/schema failures receive the current automatic repair. These limits
also apply to owner evidence-reading tasks.

The independent judge added live child transport regressions: the full pilot
suite passes 49 tests, including normal three-call and repaired four-attempt
CLI paths, with zero real provider calls. An observed live wire-order custody
failure was fixed in the pilot only; equal-byte verification was not relaxed.


### Judge completion supplement - 2026-09-17T10:20:26.963723+00:00

A final refusal-state regression found and corrected assembly exposing an
unrecorded answer before validation. Rejected assembly now preserves state,
action IDs and absence of an assembly file. The final corrected pilot suite
passes **50 tests**; normal/repair live CLI transport doubles are included.
Earlier 46/49-test observations remain historical. Overall delivery judgment
is **REJECT** because the required reason suite still has seven fixture-root
failures under mandated `TMP=C:\tr34`; concurrent reason changes are outside
this qualification. No real provider/owner-task reliability is established.
See `work/review34/REPORT.md` for evidence and reopening conditions.
