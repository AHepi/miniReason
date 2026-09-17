# UC3 run reading

> Current **P-A1 qualification** below supersedes opening MVP bounds and projections. Live semantic task: **NOT RUN**.

Status: **NOT RUN**. Complete this sheet only from the immutable run records and the separately verified sealed brief manifest. Reasonable alternate readings are not errors merely because they differ from the reference brief; judge their textual support, discriminating evidence, and conformance protection.

Preparation-only offline validation: **PASS with zero provider calls**. The current pilot accepted the top-level task fields, normalized inputs, and `evidence_read` route. The embedded source exactly matched `inputs/cases.md`; the sealed brief matched its manifest; and the restricted local checker executed to `COMPLETE/agrees` on a synthetic field-complete artifact. This validates packet mechanics only. The serialized spawn packet is 5,532 UTF-8 bytes before the model returns the required full-input echo, so the 2,048-token spawn ceiling remains a launch risk.

## Launch and envelope

- Launcher: `python C:\Dev\minireason-launch\launch_pilot.py --label UC3 --task research/deepseek-flash-pilot/usecases/UC3-reading-between-lines/task.json`
- Declared policy: 300 logical calls; no loop-count cap; every post-verification continuation decision and reason recorded.
- Projected current one-pass path: 3 provider calls (`route`, `spawn`, `evidence_read`) plus host-local assemble/checker verification; 12,288 requested completion tokens before repairs (2,048 + 2,048 + 8,192), or 24,576 if all three calls use their one schema repair.
- Desired 300-logical-call envelope: at most 2,457,600 requested completion tokens if the ceiling counts all attempts, or 4,915,200 physical-attempt tokens if each logical call may also receive one 8,192-token repair. This is a conservative completion-token envelope, not a price or usage prediction.

## What the pilot routed and spawned

**NOT RUN**

- Routed template and stated reason:
- Host correction, if any:
- Spawned calls, dependencies, and result references:
- Each pass's continuation decision and reason:

## Call count and usage

**NOT RUN**

- Logical calls:
- Physical attempts and repairs:
- Calls by role/model/lineage:
- Prompt/completion/reasoning token usage, preserving unknowns:
- Stop reason and remaining call allowance:

## Output commitments quoted

**NOT RUN**

Quote the artifact's working reading, evidence lines, conformance check, and prohibited pre-confirmation action for each C1-C8. Quote every `CONTINUATION_DECISION` and `CONTINUATION_REASON` from the control record.

## Anticipated vs found vs invented

**NOT RUN**

After verifying `briefs/MANIFEST.json`, compare with `briefs/UC3.md`:

| Case | Anticipated in brief | Found by pilot | Missed | Invented or unsupported | Reasonable alternate reading? |
|---|---|---|---|---|---|
| C1 | NOT OPENED FOR RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| C2 | NOT OPENED FOR RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| C3 | NOT OPENED FOR RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| C4 | NOT OPENED FOR RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| C5 | NOT OPENED FOR RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| C6 | NOT OPENED FOR RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| C7 | NOT OPENED FOR RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| C8 | NOT OPENED FOR RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

## Conformance and verification

**NOT RUN**

- Structural checker result and exact scope:
- Exact-quote/source custody result:
- Human conformance judgment per case:
- Unsupported certainty, unsafe action, or generic "ask for clarification" findings:
- Why any alternate reading was accepted or rejected:

## Instrument failures

**NOT RUN**

Known pre-run blockers in the current pilot source:

1. `Pilot` and `RecordedCalls` reject `max_calls > 24`, so the owner-required 300-call ceiling cannot launch through the current CLI.
2. The state machine terminates after one route/spawn/assemble/verify pass and has no post-verification continuation transition or continuation-decision record.
3. The spawn control response is limited to 2,048 tokens while it must echo the complete normalized task inputs; this packet may fail before the reader call even though its source is short.
4. Fan-out is at most 8 and depth at most 2. Eight cases fit the fan-out count in principle, but the built-in outer spawn requires exactly one subtask and the evidence template does not independently fan out cases.

Record actual failures without inferring model incapacity. Do not count a pre-dispatch refusal as a provider call. Do not infer semantic success from exit zero, valid JSON, a complete status, or the local structural checker.

## P-A1 qualification: current source supplement

UTC 2026-09-17T11:26:11.190829+00:00. Earlier max-24, one-pass, fanout-8 and depth-2 statements describe the opening source before concurrent P-A1 changes. They are historical observations, superseded here.

The tested P-A1 source accepts top-level `max_calls: 300`, accounts for logical calls separately from repair attempts, and records a real `continue_or_stop` call after verification. It supports repeated passes without a fixed pass-count cap, outer fan-out up to 24 and depth up to 3. All four task files impose no loop-count cap. The exact launcher can pass the task-level budget through the current CLI default; RUN-CONTRACT.json is explanatory, not an independently consumed configuration.

Current P-A1 budget and remaining limits: the later owner budget addendum requires a default **USD 6** per-task spend guard, overridable in the task file, and delivers remaining calls and estimated dollars to every `continue_or_stop` decision. These four tasks omit `max_spend_usd` and therefore inherit that default. Reaching the ceiling or missing usable priced usage is a recorded resource stop, not the pilot's substantive STOP and not research exhaustion. Identical spawn fingerprints are refused with at most two redecisions as P-A1's anti-repeat guard; readers must distinguish that recorded host refusal from the pilot's own stop. First-pass routing replaces model choices that disagree with the deterministic route; later passes accept valid choices. The complete normalized input must still be echoed in a 2,048-token spawn response: UC4 needs input references or a separately qualified larger envelope, and UC1/UC3 also face delivery risk. Scripted tests do not qualify token-window fit. No tool retrieves source paths. UC1's standalone static check and separate fallible review are not yet combined with built-in pilot verification. These remain disclosed live-fit and instrument limits; offline validation does not waive them.

Resource envelope per task: **300 logical calls**, at most **600 physical attempts** with one repair per call, **2,457,600 completion tokens without repairs** or **4,915,200 with all repairs**. Actual control calls use 2,048, plan calls 4,096 and workers up to 8,192. Input tokens are additional and unknown; if independently certified at 64,000 per attempt, conditional input is 38,400,000 and combined input/output 43,315,200. That estimate is neither an enforced limit nor a new tighter cap. Live loop count is model-decided, not forecast from the two-pass fixture.

A continuation section inside an answer is only a provisional self-check proposal. The authoritative decision is the later `continue_or_stop` record in `passes/pNNNN/pass.json`, with actual verification reference, reason and stop rule. Readers must quote that control record. The two-pass fixture stop rule applies only to offline validation, never to the live task.

Current clean selected path `evidence_read`: **4 logical calls / 14,336 completion-token ceiling per pass**, including post-verification continuation; at most 8 attempts / 28,672 with all repairs.

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

Current task SHA-256: `b91384192c4bc111746a02bc128dca3d6bf42116c1fe6b076ce4578706670a60`.
[New offline validation](OFFLINE-VALIDATION-PA2.md): PASS, 2 passes,
8 logical calls / 8 attempts, zero provider calls/usage.
Every prepared call passes the declared route-specific byte bound; this is
conditional host-wiring evidence, not live acceptance or a semantic result.
P-A1 continuation, budget/spend, checker sandbox and lineage rules are unchanged.
The earlier OFFLINE-VALIDATION records describe their original task/source pins.
