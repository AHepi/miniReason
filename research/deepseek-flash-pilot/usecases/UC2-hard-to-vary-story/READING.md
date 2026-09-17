# UC2 run reading: hard-to-vary story

> Current **P-A1 qualification** below supersedes opening MVP bounds and projections. Live semantic task: **NOT RUN**.

Status: **NOT RUN**. Complete this sheet only from immutable run records. Do not alter the sealed brief or its manifest after seeing the output.

Source: “The Fox and the Grapes,” *Aesop’s Fables*, translated by George Fyler Townsend, Project Gutenberg eBook 21: https://www.gutenberg.org/files/21/21-h/21-h.htm

Launcher:

```powershell
python C:\Dev\minireason-launch\launch_pilot.py --label UC2 --task research/deepseek-flash-pilot/usecases/UC2-hard-to-vary-story/task.json
```

## What the pilot routed and spawned

NOT RUN. Record the proposed route, any host correction, every spawned subtask and dependency, and each pass-level continuation decision with its stated reason.

## Call count and usage

NOT RUN. Record logical calls, physical attempts, repairs, requested ceilings, actual prompt/completion/reasoning tokens, finish reasons, provider/model identities, and unknown usage separately.

Projected current single-pass first attempt: 3 provider calls (route 2,048; spawn 2,048; evidence worker 8,192) and 12,288 maximum completion tokens. With one schema repair per call: at most 6 physical attempts and 24,576 maximum completion tokens. Local assembly and the sealed checker add no provider call.

Requested future envelope: at most 300 logical calls, no pass-count cap, and a conservative 2,457,600 completion-token allowance at 8,192 per logical call. Repair attempts are extra physical attempts; if every logical call used its one permitted repair, the conservative physical-attempt envelope would be 600 attempts and 4,915,200 completion tokens. Actual route/spawn calls use lower 2,048 ceilings, so report actual usage rather than treating this conservative envelope as a forecast or spend target.

## Output commitments quoted

NOT RUN. Quote each `[HTV-n]` commitment, its exact story evidence and paired `[REFUTER-n]`. Quote the final CONTINUE or STOP record.

## Anticipated vs found vs invented

Anticipated: compare the output to sealed `briefs/UC2.md` by its manifest hash. The brief expects the linked relations desire before failure; inaccessible goal despite pursuit; post-failure devaluation conflicting with earlier evidence; disappointment management; and their causal order. It treats actors, props and wording as replaceable when those relations survive.

Found: NOT RUN.

Missed: NOT RUN.

Invented: NOT RUN. Count unsupported events or motives, while allowing clearly labelled theoretical interpretations that are tested against the text.

## Conformance and verification result

NOT RUN. Record the evidence template quote-custody result and the local checker result separately. The checker tests headings, commitment/refuter markers, four exact textual anchors and a continuation decision; it is not an oracle for explanatory quality.

## Instrument failures

Known pre-run blockers in the current pilot source:

- `Pilot` and `RecordedCalls` reject `--max-calls 300` because both hard-cap physical attempts at 24 (`MAX_CALLS_1_TO_24`).
- `Pilot.run()` performs exactly one route/spawn/assemble/verify pass and has no state transition for a second route, so it cannot honor a model CONTINUE decision or record unlimited self-decided loops.
- The outer spawn call must echo the complete normalized input packet under a 2,048-token output ceiling. This UC2 packet uses a 56-word story to reduce the risk, but exact echo can still fail before the worker runs.
- Fan-out is at most 8 and depth at most 2. Those bounds do not themselves prevent repeated top-level passes, but the current state machine does.

The orchestrator should commission a prospective pilot amendment before live launch: raise the configured call ceiling to at least 300 logical calls; distinguish logical calls from repair attempts; accept and record a post-verification CONTINUE/STOP decision; transition safely into a fresh pass without overwriting evidence; retain every pass and decision; and avoid requiring a 2,048-token full-input echo. Until that amendment is reviewed, the launcher cannot execute the owner’s requested UC2 contract. Do not silently downgrade to one pass or 24 attempts.

Run-specific failures: NOT RUN.

## P-A1 qualification: current source supplement

UTC 2026-09-17T11:26:11.190829+00:00. Earlier max-24, one-pass, fanout-8 and depth-2 statements describe the opening source before concurrent P-A1 changes. They are historical observations, superseded here.

The tested P-A1 source accepts top-level `max_calls: 300`, accounts for logical calls separately from repair attempts, and records a real `continue_or_stop` call after verification. It supports repeated passes without a fixed pass-count cap, outer fan-out up to 24 and depth up to 3. All four task files impose no loop-count cap. The exact launcher can pass the task-level budget through the current CLI default; RUN-CONTRACT.json is explanatory, not an independently consumed configuration.

Current P-A1 budget and remaining limits: the later owner budget addendum requires a default **USD 6** per-task spend guard, overridable in the task file, and delivers remaining calls and estimated dollars to every `continue_or_stop` decision. These four tasks omit `max_spend_usd` and therefore inherit that default. Reaching the ceiling or missing usable priced usage is a recorded resource stop, not the pilot's substantive STOP and not research exhaustion. Identical spawn fingerprints are refused with at most two redecisions as P-A1's anti-repeat guard; readers must distinguish that recorded host refusal from the pilot's own stop. First-pass routing replaces model choices that disagree with the deterministic route; later passes accept valid choices. The complete normalized input must still be echoed in a 2,048-token spawn response: UC4 needs input references or a separately qualified larger envelope, and UC1/UC3 also face delivery risk. Scripted tests do not qualify token-window fit. No tool retrieves source paths. UC1's standalone static check and separate fallible review are not yet combined with built-in pilot verification. These remain disclosed live-fit and instrument limits; offline validation does not waive them.

Resource envelope per task: **300 logical calls**, at most **600 physical attempts** with one repair per call, **2,457,600 completion tokens without repairs** or **4,915,200 with all repairs**. Actual control calls use 2,048, plan calls 4,096 and workers up to 8,192. Input tokens are additional and unknown; if independently certified at 64,000 per attempt, conditional input is 38,400,000 and combined input/output 43,315,200. That estimate is neither an enforced limit nor a new tighter cap. Live loop count is model-decided, not forecast from the two-pass fixture.

A continuation section inside an answer is only a provisional self-check proposal. The authoritative decision is the later `continue_or_stop` record in `passes/pNNNN/pass.json`, with actual verification reference, reason and stop rule. Readers must quote that control record. The two-pass fixture stop rule applies only to offline validation, never to the live task.

Current clean selected path `evidence_read`: **4 logical calls / 14,336 completion-token ceiling per pass**, including post-verification continuation; at most 8 attempts / 28,672 with all repairs.

Offline qualification **PASS**: 8 logical calls / 8 attempts, two closed passes, CONTINUE then STOP, zero provider calls/usage, unchanged source and task hashes. [Pasted result and command](OFFLINE-VALIDATION.md). The semantic reading fields remain NOT RUN.

Instrument erratum: the earlier CLI probe encountered initialization AttributeError during concurrent pilot changes, before a provider call. Preserve work/w37/validate-tasks-20260917T110951145635Z.log/.json and their C:/tw37 output paths. A source race is suspected, not proven; later successful source-pinned tests do not overwrite it.
