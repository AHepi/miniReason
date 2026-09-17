# UC1 reading sheet: Blender blocking

> Current **P-A1 qualification** below supersedes opening MVP bounds and projections. Live semantic task: **NOT RUN**.

Status: **PREPARED; NOT RUN**. No provider/model or Blender call was made.

## Launcher

`python C:\Dev\minireason-launch\launch_pilot.py --label UC1 --task research/deepseek-flash-pilot/usecases/UC1-blender-blocking/task.json`

The launcher contract is 300 logical calls, at most 600 physical attempts when each logical call uses its sole schema repair, no per-task loop-count cap, and as many route/spawn/assemble/verify passes as the pilot chooses under its recorded stop rule. Every continuation decision must preserve its reason. The worst-case completion-token envelope is 4,915,200 tokens (600 x 8,192); route/spawn/plan calls have lower configured caps, so this is an intentionally loose ceiling, not an expected spend or price promise. Prompt tokens are unknown until exact wires exist.

The current P-A1 pilot accepts the task's top-level `max_calls: 300`, counts logical calls separately from each call's sole repair, records `continue_or_stop` after verification, has no fixed pass limit, permits fan-out up to 24 and depth up to 3. It still does not run this task's standalone AST checker or scripted fallible review as part of `verify`. Its default USD 6 spend guard is the later owner-required per-task runaway-loop guard, overridable in a task file; this task omits the field and inherits the default. Remaining call and dollar budgets feed every `continue_or_stop` decision, and a ceiling stop is a recorded resource boundary rather than the pilot's substantive stop or research exhaustion.

With no template-forcing feature or kind, the current task shape deterministically selects `direct_answer`. A first pass uses route, spawn, answer, and post-verification continue/stop = 4 logical calls and at most 14,336 configured completion tokens on first attempts, or 8 attempts and 28,672 tokens if each call uses its repair. The separately scripted fallible review adds 1 logical call at 8,192 tokens. If wired into the pass, the nominal combined pass is 5 logical calls / 22,528 tokens first attempts, or 10 attempts / 45,056 tokens with all repairs. Later passes may deliberately change route/subtask mix and therefore have different counts. These are projections, not expected spend or a price promise.

## What the pilot routed and spawned

- Route/template: NOT RUN.
- Spawned children/dependencies: NOT RUN.
- Continuation decisions and reasons: NOT RUN.

## Call count and usage

- Logical calls: NOT RUN.
- Physical attempts/repairs: NOT RUN.
- Prompt/completion/reasoning tokens: NOT RUN / unknown.
- Provider/model identity and settings: NOT RUN.

## Output commitments quoted

- NOT RUN. Quote exact output commitments here without paraphrase.

## Anticipated vs found vs invented

- Anticipated reference: `briefs/UC1.md`, sealed by `briefs/MANIFEST.json` before launch.
- Found: NOT RUN. Record which exact constraints and construction obligations were satisfied.
- Missed: NOT RUN. Record each brief item absent or contradicted.
- Invented: NOT RUN. Record APIs, plugin interfaces, scene facts, execution claims, or constraints not present in the task.
- Trap comparison: NOT RUN. Check for prose-only output, timing discontinuity, script/spec divergence, unsupported API/I/O, or a false Blender execution claim.

## Conformance and verification result

- Pilot structural checker: NOT RUN. Its scope is markers/core fields/obvious tokens only.
- Standalone `inputs/verify_uc1.py` spec + AST/API check: NOT RUN on pilot output.
- Scripted fallible review using `inputs/review-template.json`: NOT RUN on pilot output. The positive preparation fixture executed once offline and deliberately returned `needs_revision` plus `continue` because projected S02 drone visibility is unverified.
- Conjunction verdict: NOT RUN. Never infer it from the structural checker alone.
- Blender runtime/visual review: NOT PERFORMED by this task.

## Instrument failures

- P-A1 now implements the 300-logical-call ceiling and repeated passes together with the later owner-required default USD 6 per-task runaway-loop guard. This task omits `max_spend_usd` and therefore inherits that default; remaining calls and estimated dollars feed every continuation decision.
- Current restricted checker omits `ast` from allowed imports and forbids `compile`, so the standalone AST checker cannot be executed as `check.source` without a reviewed host change.
- Current task format cannot combine a deterministic checker and a model review in one verification stage.
- The separate scripted Flash review is same-lineage and fallible; it cannot be misreported as independent verification.
- Spawn repeats complete normalized inputs under a 2,048-token cap. This task is intentionally compact, but exact live preflight is still required (register L20/L21).
- The first offline review-helper attempt at `C:\tw37\uc1-review-fixture-01` stopped before its adapter call because concurrently changing pilot source imported a not-yet-present `minireason.pilot.budget`. No provider/model call occurred. The task-local helper was made independent of that incomplete pilot package; its second offline fixture completed at `C:\tw37\uc1-review-fixture-02`.

## Offline fixture evidence

The positive spec/script and negative cases are preparation fixtures, not pilot output. On the required Python 3.11 with `TMP=C:\tw37`, `inputs/test-verify.ps1` produced:

```text
{"errors": [], "ok": true}
positive: expected exit 0
{"errors": ["banned import", "banned name: open", "imports must be exactly unaliased import bpy; import math; from mathutils import Vector", "only build_scene() may be a top-level expression", "unapproved direct call: open"], "ok": false}
reject-file-access: expected exit 1
{"errors": ["missing required API calls: bpy.ops.object.camera_add", "unapproved bpy call: bpy.ops.object.imaginary_camera_add", "unpinned bpy chain: bpy.ops.object.imaginary_camera_add"], "ok": false}
reject-unknown-api: expected exit 1
{"errors": ["only build_scene() may be a top-level expression", "unapproved bpy call: bpy.ops.render.render", "unpinned bpy chain: bpy.ops.render", "unpinned bpy chain: bpy.ops.render.render"], "ok": false}
reject-render-write: expected exit 1
{"errors": ["unpinned bpy chain: bpy.context.scene.radians"], "ok": false}
reject-context-attribute: expected exit 1
{"errors": ["untyped or unapproved receiver call: fake.keyframe_insert", "untyped or unpinned receiver attribute: fake.keyframe_insert"], "ok": false}
reject-fake-receiver: expected exit 1
{"errors": ["S03 courier retreat", "embedded SHOT_SPEC differs from supplied spec"], "ok": false}
reject-shot-constraint: expected exit 1
{"errors": ["exactly three subject records", "duplicate or non-object subject record", "embedded SHOT_SPEC differs from supplied spec"], "ok": false}
reject-duplicate-subject: expected exit 1
{"errors": ["shot 2 exact motion count", "embedded SHOT_SPEC differs from supplied spec"], "ok": false}
reject-contradictory-motion: expected exit 1
{"errors": ["top-level fields", "embedded SHOT_SPEC differs from supplied spec"], "ok": false}
reject-unknown-field: expected exit 1
{"errors": ["fps", "embedded SHOT_SPEC differs from supplied spec"], "ok": false}
reject-wrong-type: expected exit 1
{"errors": ["ValueError: nonfinite JSON: NaN"], "ok": false}
reject-nonfinite: expected exit 1
```

The task-format/structural-check qualification produced:

```json
{"checker_source_utf8_bytes": 2226, "normalized_spawn_input_utf8_bytes": 3340, "route": "direct_answer", "structural_checker_comparison": "agrees", "structural_checker_status": "COMPLETE", "task_fields": ["check", "inputs", "max_calls", "task"]}
```

The separate review-helper fixture produced one recorded offline adapter attempt, zero provider calls, `needs_revision`, one high-severity camera-framing issue, and `continuation.decision=continue`; its immutable adapter request/response and public result are under `C:\tw37\uc1-review-fixture-02`. The would-send/wire SHA-256 is `c7d34bf9f6a363d8f57ad98b67bf19043b4e70eb18ce6e4913a0bb837273fce3`; the scripted response is `COMPLETE/stop`, reports zero usage, and records both reasoning-content-present and reasoning-content-persisted as false.

This is not a full pilot run. It establishes the current strict task shape including `max_calls:300`, deterministic first-pass route, a small echoed input packet, restricted-checker acceptance, standalone verifier positive acceptance, eleven targeted refusals, and an executable scripted review path. The later owner budget addendum resolves the common spend contract: this task inherits P-A1's default USD 6 per-task guard.

## Applied failure-register entries

Applied: L2/L19 (JSON remains locally validated); L4/L11 (decisive artifact work must fit a real envelope); L5/L6 (review is fallible and lineage/exposure recorded); L8 (repairs need exact source and error); L10 (duplicate-key JSON rejection); L12/L13 (commitments carry refuters into use/review); L15/L20/L21 (bounded prompts and exact preflight); L17/L31 (separate ceilings, logical calls, attempts and usage); L22 (preserve actual wire); L25/L26/L27 (short C:\tw37 root, exact Python, UTF-8); L28 (complete status is not artifact conformance); L30 (static fixture is not Blender/runtime qualification).

Set aside: L1/L18 because this task declares thinking-off through the current pilot; reopen if route settings change. L3/L7/L9/L14/L16 concern critic-return/locator/return-archive contracts not used by this task. L23/L24 remain orchestrator host duties at launch. L29 applies to future append-only run records; this preparation creates new files only.


## Pre-live instrument erratum: hidden constraints disclosed

Final read-only comparison of participant task bytes against `inputs/verify_uc1.py` found exact schema/camera literals and narrow AST provenance rules that the participant could not retrieve. The old task is preserved byte-for-byte as `inputs/task-before-visible-contract.json` (SHA-256 `4c58d9f6f7885e0abcd1597fd23b1f7986c94bce6ed278a3176694552005cd70`). Before any live use, `task.json` was corrected to state every enforced literal, allowed receiver type/attribute, exact required call and disallowed grammar; corrected SHA-256 `9a667d8718ce76a4790f571d62129d6d8d6d3c06a9081e7dff8458d640211dc8`. `briefs/CUSTODY-SUPPLEMENT.json` binds both tasks and the reason. The sealed expectation `briefs/UC1.md` and its `MANIFEST.json` remain byte-identical. No provider/model or Blender call occurred. This is an instrument correction, not a task result or softened expectation.

## P-A1 qualification: current source supplement

UTC 2026-09-17T11:26:11.190829+00:00. Earlier max-24, one-pass, fanout-8 and depth-2 statements describe the opening source before concurrent P-A1 changes. They are historical observations, superseded here.

The tested P-A1 source accepts top-level `max_calls: 300`, accounts for logical calls separately from repair attempts, and records a real `continue_or_stop` call after verification. It supports repeated passes without a fixed pass-count cap, outer fan-out up to 24 and depth up to 3. All four task files impose no loop-count cap. The exact launcher can pass the task-level budget through the current CLI default; RUN-CONTRACT.json is explanatory, not an independently consumed configuration.

Current P-A1 budget and remaining limits: the later owner budget addendum requires a default **USD 6** per-task spend guard, overridable in the task file, and delivers remaining calls and estimated dollars to every `continue_or_stop` decision. These four tasks omit `max_spend_usd` and therefore inherit that default. Reaching the ceiling or missing usable priced usage is a recorded resource stop, not the pilot's substantive STOP and not research exhaustion. Identical spawn fingerprints are refused with at most two redecisions as P-A1's anti-repeat guard; readers must distinguish that recorded host refusal from the pilot's own stop. First-pass routing replaces model choices that disagree with the deterministic route; later passes accept valid choices. The complete normalized input must still be echoed in a 2,048-token spawn response: UC4 needs input references or a separately qualified larger envelope, and UC1/UC3 also face delivery risk. Scripted tests do not qualify token-window fit. No tool retrieves source paths. UC1's standalone static check and separate fallible review are not yet combined with built-in pilot verification. These remain disclosed live-fit and instrument limits; offline validation does not waive them.

Resource envelope per task: **300 logical calls**, at most **600 physical attempts** with one repair per call, **2,457,600 completion tokens without repairs** or **4,915,200 with all repairs**. Actual control calls use 2,048, plan calls 4,096 and workers up to 8,192. Input tokens are additional and unknown; if independently certified at 64,000 per attempt, conditional input is 38,400,000 and combined input/output 43,315,200. That estimate is neither an enforced limit nor a new tighter cap. Live loop count is model-decided, not forecast from the two-pass fixture.

A continuation section inside an answer is only a provisional self-check proposal. The authoritative decision is the later `continue_or_stop` record in `passes/pNNNN/pass.json`, with actual verification reference, reason and stop rule. Readers must quote that control record. The two-pass fixture stop rule applies only to offline validation, never to the live task.

Current clean selected path `direct_answer`: **4 logical calls / 14,336 completion-token ceiling per pass**, including post-verification continuation; at most 8 attempts / 28,672 with all repairs. UC1 also requires a separate 8,192-token review call: combined nominal **5 logical calls / 22,528 completion tokens per pass**, or 10 attempts / 45,056 with repairs. Its standalone one-attempt review fixture is documented above and is not included in the two-pass host count.

Offline qualification **PASS**: 8 logical calls / 8 attempts, two closed passes, CONTINUE then STOP, zero provider calls/usage, unchanged source and task hashes. [Pasted result and command](OFFLINE-VALIDATION.md). The semantic reading fields remain NOT RUN.

Instrument erratum: the earlier CLI probe encountered initialization AttributeError during concurrent pilot changes, before a provider call. Preserve work/w37/validate-tasks-20260917T110951145635Z.log/.json and their C:/tw37 output paths. A source race is suspected, not proven; later successful source-pinned tests do not overwrite it.


## Current P-A2 input/validation supplement - 2026-09-17

P-A2 supersedes the earlier input-echo/no-source-read limitation. The active task
now declares exact content-addressed input units; controls emit IDs/ranges and
the host resolves pinned bytes before workers. `read_source`/child `source_reads`
are restricted to that task's units, with offsets, byte limits and omission
receipts. Full FW5, reader briefs, this READING file, derived-properties
memoranda and env files are not in the pinned set. No sealed brief or existing
MANIFEST file changed. UC4 retains its excerpt/projection scope.

Current task SHA-256: `c675b63e8683b8b1fc61a71b71d01bde284d0715decd4603a2200e395fb53ac8`.
[New offline validation](OFFLINE-VALIDATION-PA2.md): PASS, 2 passes,
8 logical calls / 8 attempts, zero provider calls/usage.
Every prepared call passes the declared route-specific byte bound; this is
conditional host-wiring evidence, not live acceptance or a semantic result.
P-A1 continuation, budget/spend, checker sandbox and lineage rules are unchanged.
The earlier OFFLINE-VALIDATION records describe their original task/source pins.
