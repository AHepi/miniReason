# DeepSeek Flash self-piloting pilot

The owner calls this endpoint V4 flash; the repository route is `deepseek-flash`.
[P-A1](AMENDMENTS.md), declared 2026-09-17, lets the pilot decide to run more
full passes after inspecting verification. The priority is: "the token spend isn't as important as the capability. And the ability for V4 flash to decide to keep running a loop or two." Then: "More loops."

One pass is `route -> spawn -> assemble -> verify`, followed by a recorded
`continue_or_stop` tool call. There is no fixed pass count. By the owner's
decision, spending is bounded by the task ceilings, not a target number of
loops: **300 logical calls and estimated USD 6.00 by default**. Both are
positive task-file overrides (`max_calls`, `max_spend_usd`); `max_calls` may
exceed 300. CLI `--max-calls` overrides the task value. Calls include all
control, worker and critic roles. One schema repair is another physical
attempt within the same logical call, charged to usage and spend.

## Continuation decision

Exactly these four fields are required; additional fields are refused:

```json
{
  "decision": "continue",
  "reason": "sha256:<supplied verification_ref>: the checker failure needs a boundary-case investigation",
  "what_changes_next": "Switch to decompose_synthesize and separate the boundary analysis from the counterexample search because verification exposed that gap.",
  "stop_rule": "Stop when verification supports the answer or no supported next change remains."
}
```

`decision` is `continue` or `stop`. The reason must cite the exact supplied
verification reference and explain its outcome. `what_changes_next` must be
nonempty on `continue` and may be empty on `stop`. The host supplies the full
checker result, cross-lineage objections, or unavailable result, along with
remaining logical calls and estimated dollars, cumulative usage and attempts.
The first decision saves `stop_rule`. Later decisions must preserve it exactly
or append ` OR ` plus another early-stop condition; replacement is refused.
This preserves the stated condition mechanically; its substantive application
remains the pilot's fallible judgment. Malformed decisions get one recorded
repair with the original input, public response and precise error.

A continued pass must change its template mix or subtask inputs. Before workers
run, the host hashes canonical inputs and compares the template/input multiset
with prior passes. Identical work is refused with a recorded reason. The pilot
gets at most two redecisions; a third identical proposal stops the run. Resource
stops and other terminal failures are recorded separately from the pilot's
choice, and never mean the inquiry is exhausted.

## Bounds and source authority

Spawn permits up to **24** children per batch, with depth at most **3** inside
each pass. At least one outer child implements the routed template. Decomposition
can nest at depths 1 and 2, with leaves at 3. Dependencies remain ordered and
sub-calls retain their own immutable records. Changed tasks and premises are
fallible work requests; original documents, allowed files, test commands,
behavior contract and protected obligations remain sealed. The built-in
scheduler is sequential. Stateful external tools must be serialized, with at
most five active provider requests under the existing operating limit.

The checker sandbox, its allowlist, wall and output limits are unchanged.
`engineer_patch` still proposes changes; it neither edits files nor runs claimed
tests. A refused partial dependency cannot become an accepted assembly: the
host instead delivers an unavailable-verification record to the decision.
Controls and workers remain thinking-off. Keys remain in the environment;
hidden reasoning and credentials are never stored. There is no transport retry,
uncertain-delivery replay, self-modification or automatic ceiling increase.

## Spend guard

[PRICES.json](PRICES.json) freezes the official provider URLs and 2026-09-17
reading date. It uses published peak prices where applicable and cache prices
when the recorded usage identifies cache hits. Every attempt contributes prompt
and completion tokens; reasoning tokens are reported as part of completion and
are not charged twice. The table is copied exactly into each run as `prices.json`.
An unmapped route remains token-accounted with unknown dollars. Missing required
usage on a priced dispatched call stops further dispatch as `SPEND_UNKNOWN`.
`CALL_BUDGET` or `SPEND_CEILING` records a reached resource boundary.

`RUN.md` labels per-pass and total spend **an estimate from published prices,
not a bill**. Actual usage arrives after a response, so the last response may
carry the estimate over the ceiling; no later call is admitted. Unknown costs
are shown explicitly. The ceiling guards runaway loops and is not a target.

## Offline fixture

Use the specified Python with `PYTHONPATH=src;tests`, `PYTHONUTF8=1`,
`PYTHONIOENCODING=utf-8` and a short fresh output directory. This callable fixture
makes four scripted logical calls, including an explicit stop based on the
runtime checker receipt. It makes no provider call:

```python
import json
from pathlib import Path
from minireason.pilot.pilot import Pilot

examples = Path("research/deepseek-flash-pilot/examples")
task = json.loads((examples / "direct.task.json").read_text(encoding="utf-8"))
responses = iter(json.loads((examples / "direct.scripted.json").read_text(encoding="utf-8")))

def scripted(**context):
    if context["role"] == "continue_or_stop":
        packet = json.loads(context["messages"][1]["content"])
        return {"decision": "stop",
                "reason": packet["verification"]["verification_ref"] + " checker agrees; task answered",
                "what_changes_next": "", "stop_rule": "Stop when the checker agrees."}
    return next(responses)

result = Pilot(task, Path("C:/tw38/pilot-new-001"), scripted=scripted).run()
print(result["status"])
```

The CLI remains `python -B -m minireason.pilot run --task TASK.json --mode offline
--scripted RESPONSES.json --out FRESH_DIRECTORY`. Offline mode never opens an
env file. The JSON list must include explicit continuation responses; historical
three-response examples above are used as the first three turns, not a complete
P-A1 transcript. `--mode live` is owner opt-in and reads provider keys at call
time. No real provider or owner task was run for this amendment.

The task object requires `task`; optional fields are `inputs`, `features`,
`check`, `critic_seats`, `max_calls` and `max_spend_usd`. Initial routing retains
the published deterministic correction policy; later passes may select another
registered template with valid inputs to implement the declared change.

## Reading a run

1. `ANSWER.md`: latest available working answer and terminal status.
2. `RUN.md`: per-pass and cumulative calls, attempts, tokens, estimated dollars
   and stop detail.
3. `TRACE.md`: numbered state transitions, verbatim decision fields and refusals.
4. `passes/pNNNN/pass.json`: routed and spawned work, nested subcalls, assembly,
   verification, decisions and budgets; adjacent assembly/verification files
   retain original evidence.
5. `calls/cNNNN/aNN/`: each attempt's request, response, usage and wire custody.

Root assembly/verification are views of the latest available records. Earlier
passes and rejected responses remain immutable. `task.json`, `catalogue.json`,
`tools.json`, `endpoints.json`, `prices.json` and `config.json` seal the inputs
and implementation identities. A completed state does not establish accuracy
or creativity; an advantage from more calls needs matched multi-call controls.

## External tool harness

The generated manifest is `src/minireason/pilot/tools.json`: `route`, `spawn`,
`assemble`, `verify`, `continue_or_stop`. Host validation retains stronger
bounds than the exported beta strict-schema subset. The entire new manifest
has offline qualification only. `Pilot.dispatch(tool_call)` accepts the ordinary
OpenAI function-call shape and returns a tool message. Reused action IDs return
the existing result only for identical arguments; uncertain actions cannot replay.
For multiple outer children, assembly must reference a recorded synthesis.

The built-in runner records continuation as a host tool action from the JSON
control response because the inherited text Adapter does not retain native
function-call responses. An external native-tool harness must preserve its own
wire/tool-call evidence, account its control calls and spend in the same total
allowance, reserve that allowance before constructing the worker Pilot, and
feed verification plus remaining budgets to every decision. The manifest alone
is not an external HTTP recorder or external-budget enforcement layer.

## Historical qualification records

The observations below describe their original source versions. P-A1 changes
are declared separately and do not rewrite these earlier records.

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


## P-A1 offline qualification - 2026-09-17

Final source passes 77 pilot tests, including a scripted three-pass run stopped
by the pilot's own rule, identical-pass refusal, schema repair, logical-call
and spend ceilings, budget inputs, unavailable/critic verification, fan-out24,
depth3 and an actual child transport double with two complete passes. The exact
reason suite passes346tests under child `TMP=C:/tr36`; docs pins pass26tests.
Source and test evidence: `work/w38/INDEX.md`. A first reason run used an
unadmitted evidence-root override and failed; its full transcript is retained
alongside the passing rerun. No launcher code or checker limits were changed.
No real provider/model calls were made. These are offline host-wiring results,
not live full-manifest acceptance or demonstrated owner-task reliability.


## P-A2 input authoring and source reads - 2026-09-17

[P-A2](AMENDMENTS.md) replaces the historical full-input spawn echo and adds
scoped reads plus a complete-request preflight. The source-checkout implementation
is qualified offline; see `work/w45/INDEX.md` for the final test evidence.

A task author puts the former `inputs` object in a UTF-8 JSON file, hashes its
exact bytes, and writes a descriptor and full-unit reference in `task.json`:

```json
{
  "task": "Read the declared material and answer the question.",
  "inputs": {"unit_id": "<64 lowercase SHA-256 hex characters>", "start": 0, "end": 123, "encoding": "json"},
  "input_units": [{
    "unit_id": "<same SHA-256>", "sha256": "<same SHA-256>", "byte_count": 123,
    "path": "research/my-task/inputs/task-inputs.json",
    "media_type": "application/json", "role": "task_input"
  }]
}
```

The example's digest and length are placeholders: compute both from the exact
file bytes. Additional participant source files get descriptors with
`role: "public_source"`. Only these explicitly pinned files are admitted;
reader briefs, env files and derived-properties memoranda cannot be pinned.
Keep READING.md, sealed answers, checkers and private implementation details
outside the participant set. Paths are relative to `--repo-root` (default:
current directory). A modified file requires new pins and a fresh run.
Existing inline task files remain supported and get host-derived units at load.

The host normalizes input JSON once and supplies a compact reference/catalogue
to controls. A spawn response copies that reference, not the complete documents.
Later passes may add `overrides` containing only `task`, `premises`, `candidate`
or `objections`, while source/scope fields retain their sealed equality checks.
Workers receive resolved data. Each child may select up to eight `source_reads`:
`{"unit_id":"<pinned ID>","start":0,"end":123,"limit":123}`.
The external `read_source` tool uses the same shape. Offsets are zero-based
UTF-8 bytes, the end is exclusive, and the model limit is at most 65,536 bytes.
Omissions carry exact ranges/reasons; split-codepoint and out-of-unit requests
are refused. Reads use the frozen bytes, so a later path edit cannot change them.

`input-units/` stores exact frozen text and hashed manifests. Spawn records hold
references; worker and repair requests contain resolved content. Each attempt's
`decision.json`/`outcome.json` records its input preflight and source hashes;
`preflight-refusal.json` records a refused call before any physical attempt.
Literal text exposure and canonical JSON delivery have distinct receipt schemas.
The guard compares complete prepared wire bytes plus completion and template
reserves with the declared route window; see P-A2 for the conditional premises.

Use the existing offline CLI with `--repo-root C:/Dev/miniReason` when launching
from elsewhere. The four use-case task files demonstrate exact pins, including
UC4's FW5 excerpts by reference. `OFFLINE-VALIDATION-PA2` supplements report the
new fixture runs; original OFFLINE-VALIDATION records remain historical.
P-A1 continuation, budgets, checker sandbox and lineage rules continue to apply.
The tool manifest now also includes `read_source`; full native provider acceptance
of that manifest remains untested.


### P-A2 judge corrections - 2026-09-17T13:07:44.232113+00:00

JSON input units require unique member names at every nesting level and finite numbers. Malformed units fail before use. Legacy inline inputs remain supported; saved spawn records use resolved content references in every spawn field. See `work/review45/INDEX.md` for independent source diffs, corrections and final offline verification.
