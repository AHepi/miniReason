# R002 A2: delivery repair and critic allowance

Registered 2026-09-17T03:03:56.465874+00:00, REC-20260917-A. [PLAN A2](PLAN.md) explicitly declares registration AFTER occurrence-001 dispatch, a deviation, with effect only for separately identified occurrence-002. This page is an engineering diagnosis and limitation supplement; it does not replace any observation.

## Diagnosis

The sixth call in each LOOP-DECOMPOSED occurrence is `calls/c0002-critic/a00`, GLM5.3 native route with thinking off and16384 allowance. C05/C06/C12 return provider COMPLETE/stop, then fail the JSON parser at line1 column1 with prose. C09 reaches length at16384. All four have6calls and1completed cycle. Source prefix: `runs/r002-main-review22/main-occurrence-001/<case>/LOOP-DECOMPOSED/`.

| Case | Completion used | Terminal status | Public output UTF8 bytes |
|---|---:|---|---:|
| C05 |10355|SCHEMA_FAILURE|37921|
| C06 |11854|SCHEMA_FAILURE|42706|
| C09 |16384|CEILING_HIT|27543|
| C12 |6590|SCHEMA_FAILURE|20470|

C09 CROSS, TESTED and CHECKER all stop at their third call, `calls/c0001-signal-b/a00`, also GLM5.3 thinking off/16384, length at16384. Their initial DeepSeek native calls and first Qwen critics completed;0cycles were completed. Prompt/completion usage respectively2267/16384,2297/16384,2139/16384. Those three arms are not rerun by A2.

C05's completed cycle1 critic is Qwen, not GLM. Its system message and the cycle2 system message are identical1093bytes; the JSON command begins at character159 (`JSON` at178). The user prompt grows5495->6847characters (5507->6853UTF8bytes), wire7242->8592bytes. Accepted dependencies grow2->1053bytes and current step930->1190bytes. The same2192-byte response schema starts at user character3111->4463. This is explicit prior-step state inside a two-message request, not an added chat-message history. Endpoint, step and context changed together; the record does not isolate prompt length as the cause.

Provider JSON mode **was already wired and present** on every inspected failed request: `src/minireason/reason/adapter.py:129` supplies response_format=json_object, `src/minireason/provider_openai_compat.py:513` translates it, line515 writes top-level format, and lines740-749 map json_object to `json`. The actual native wires have `format:"json"`, `think:false`, `options.num_predict:16384`. Provider-level format did not guarantee JSON on this route; no adapter/provider edit is needed. The prose failures are instrument delivery failures, not findings about criticism.

## Implemented A2 conditions

The separately pinned v2 recipe retains three one-step cycles, unchanged task/contract/public limits and synthesis obligations. The independent judge correction uses Qwen/Qwen/Qwen, replacing only the step2 GLM seat before occurrence002. All off critics receive32768, motivated by the observed GLM exhaustion and an equal critic allowance. STEP/use stay16384; native seats32768. A schema failure permits one repair using full own invalid output and the same contract/seat/ceiling; a second failure stops. Every attempt is retained and counted, and repaired reach is read separately. CEILING_HIT remains terminal, with no fallback or repair. No other five arms are selected.

Full route:13logical calls,344064completion without repair; at most26attempts/688128completion with repairs. Four cases:52logical/104attempts maximum,2752512completion/3407872input/6160384combined,31200aggregate supervised seconds. These are declared revised aggregates; they are not A1's old13/294912. Every attempt keeps32768input and300s wall. See the exact projection in the launcher phase receipt and `work/w24/OCC2-LAUNCH.md`.

## Known repair-input limit

**C05 and C06's saved full prose cannot fit the unchanged conservative30720-byte Ollama wire cap.** The outputs alone are37921/42706bytes; adding only the compact contract gives40113/44898, before escaping, wrappers or instructions. A2 correctly stops these attempted repairs at PROMPT_TOKEN_CAP before intent/send. C12's20470-byte output may fit; exact-wire offline verification decides. C09 is a ceiling stop and is not eligible for schema repair.

This makes the prediction conditional: A2 can reach later steps when the response parses, or when its one repair fits preflight and parses; it does not establish that the saved C05/C06 prose would be recoverable. No hidden truncation or unqualified bound increase is introduced. A qualified alternative input counter or an explicitly different intervention would require separate engineering/judgment. Increasing the output allowance does not cure this input limit and can produce even longer invalid prose.

## Operational lesson and reading

Inspect the actual failed seat and wire before inferring an omitted format option or attributing prose to a model from the previous cycle. Distinguish provider completion, contract parsing, input refusal and completion exhaustion. Retain all attempts/usage and report reached by repair versus reached without repair; schema success alone is not a semantic result. A2's extra calls and larger critic allowance are confounds, and no matched control is rerun here.

All engineering validation is offline. This page now includes the independent judge correction; publication is a separate action. No provider call or occurrence001 edit is part of the A2 correction. Review-only execution errata are retained in work/review24. Detailed immutable path/hash/request-position facts are indexed under `work/w24/INDEX.md`.


## Exact offline qualification - 2026-09-17T03:16:38.938441+00:00

The exact C12 repair wire **fits**:25927bytes+2048reserve=27975counted, accepted. C05 and C06 wires are43975/48729bytes and count46023/50777, rejected before a01 intent. Full proof: `work/w24/full-a2-proof.json`. It also records a synthetic three-step A2 run with13logicalcalls/26attempts,26equal prepared/provider/preflight hashes and688128sumcompletionallowances. It proves the envelope and attempt custody, not faithful semantic conversion of the source prose. Current R002 suite118/118passes; a later completion receipt records the corrected launcher integration.


## Independent judge disposition - 2026-09-17T03:38:40.376642+00:00

The unchanged-GLM proposal is corrected: occurrence-001 GLM0/7 usable (3prose/schema,4length), Qwen7/7 parsed. Selected-current R001 GLM critic8/18 initially valid,1prose repaired,9length at8192off; eventual9/18 usable. Qwen critic7/18 initially valid and11JSON-schema failures,all11repaired,0length; eventual18/18 usable. Qwen use17/18valid plus1repair is a separate role. Archived GLM7critics:4valid,2length,1transport. Archived Qwen7critics:3valid,3repaired JSON-schema failures,1transport, plus3valid use calls. These are finite, different-condition delivery counts, not a model quality ranking or a forecast at32768. GLM32768-plus-repair success frequency: **NOT FOUND**.

The smallest further intervention replaces only v2 cycle2 GLM with Qwen; Qwen stays distinct from DeepSeek under ruling10. Multiple independent critic lineages are no longer present across decomposed cycles, and no such claim is made. Adding a second critic or Kimi would change multiplicity/resources or require another input-route qualification. The R001 unavailable-seat rule requires another returned critic; it is not imported into single-critic step acceptance. Exact resources remain those above. Immediate CEILING_HIT termination and one same-seat schema repair remain intact.

**The cap also governs fresh live repairs.** Source `_call` preflights every a01 before intent/send independent of live/offline mode. A2 never replays occurrence001; fresh equally oversized prose would be refused too. The input gate is unchanged, and Qwen substitution is not a guarantee against such failure. Reading must distinguish without repair, by repair, and not reached, then assess actual content preservation and later use separately.

The revised recipe and generated capability pin the corrected route. Root direct evidence, all correction diffs, test output and complete detached command are indexed in `work/review24/INDEX.md`; a final validation receipt records what actually passed. No new provider observation is claimed.


Custody qualification (2026-09-17T03:42:19.282263+00:00): occurrence001 retains actual sent provider wires. The50saved prepared-versus-provider wires differ in byte hash because sorted worker input reorders nested message keys, while all50decoded JSON bodies and byte lengths are equal. All14native Ollama wires retain format=json. Do not confuse the separate offline26matching-hash proof with an equal-byte claim about those historical live wires. Both original hashes and bodies remain preserved; this order difference changes neither the format field nor the length used by the bound. Evidence: work/review24/evidence-counts/WIRE-CUSTODY.md.


Final judge verification 2026-09-17T03:44:22.082458+00:00: exact reason discovery270/270 and documentation-pin26/26 pass; focused6/6 and full3cycle/26attempt proof pass. Actual four-case offline launcher selects only corrected v2, with104attempt/2752512completion phase budget. Complete transcripts, refusal probes and detached command are under work/review24; see the appended VALIDATION section. These are engineering checks only.
