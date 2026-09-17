# Prepared probe plan

**PREPARED, NOT EXECUTED LIVE.** The orchestrator executes this plan separately. The script's offline self-check and dry-run are not model evidence. No plugin is built.

From `C:\Dev\miniReason`, with `DEEPSEEK_API_KEY` already in the process environment, the required command is:

```powershell
python research/deepseek-flash-pilot/probes/run_probes.py --out research/deepseek-flash-pilot/probes/records
```

This host's explicit interpreter equivalent is:

```powershell
$env:PYTHONPATH='src;tests'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:TMP='C:\tw33'
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -B -X utf8 research/deepseek-flash-pilot/probes/run_probes.py --out research/deepseek-flash-pilot/probes/records
```

C:/tw33 was created during preparation. No env file is loaded. Key values are never printed. The default command is live; to inspect without credentials, network or record writes add `--dry-run` or `--self-check`. Do not run the default command to perform an offline check.

## Calls, evidence and pass criteria

Each row names one maximum HTTP call. All are sequential with no retries. A tool continuation is skipped if its initial turn fails validation; skipped calls do not get reallocated. Total maximum **12 calls / 21,504 completion tokens**, excluding inputs. The endpoint timeout remains 180 seconds per transport operation, not a guaranteed whole-run wall-time bound. Calls are bounded by explicit output ceilings even if the service defaults change.

| # / record name | Mode / completion ceiling | What it establishes | Local pass criterion |
|---|---|---|---|
| 1 `tool-normal-initial` | off / 2048 | Standard OpenAI function schema with two independent tools: choose_template and verify_contract; asks for both in one turn. | Exactly the two expected function names, distinct nonempty IDs, correct function type, valid strict-JSON arguments satisfying local types/enums/required fields, finish tool_calls, no hidden-reasoning field. Actual parallel scheduling is not exercised. |
| 2 `tool-normal-followup` | off / 1024 | Matching tool-result IDs and voluntary stopping. Both tool results are fixed local simulations. | Nonempty public answer, stop finish, no further tool call, no unexpected reasoning. tool_choice stays auto, so stopping is observed rather than forced by none. |
| 3 `tool-strict-initial` | off / 2048 | Beta constrained function arguments, both definitions strict:true; requests only choose_template. | Exactly that valid tool call, no extra arguments, correct enum/types, unique ID, tool_calls finish, no hidden reasoning. API rejection is preserved as a failed feature probe. |
| 4 `tool-strict-followup` | off / 1024 | Strict-mode tool roundtrip and stopping after the local result. | Same voluntary-stop criterion as 2. |
| 5 `router-direct` | off / 1024 | Route simple arithmetic. | JSON exactly template_id + justification, ID direct_answer, one-sentence nonempty reason, stop finish. |
| 6 `router-evidence` | off / 1024 | Route reading saved records with source citation. | Same contract, expected evidence_read. |
| 7 `router-engineer` | off / 1024 | Route a bounded parser patch and test task. | Same contract, expected engineer_patch. It does not execute the proposed patch. |
| 8 `router-critic` | off / 1024 | Route judging a supplied answer/contract and requesting repair. | Same contract, expected critic_return. |
| 9 `router-decompose` | off / 1024 | Route independent security/cost/operability analyses plus assembly. | Same contract, expected decompose_synthesize. |
| 10 `spawn` | off / 2048 | Produce narrower child tasks with template IDs and inputs. | JSON exactly subtasks; 2-4 uniquely named objects with id/template_id/input/depends_on; nonempty inputs, allowlisted templates and only earlier dependency IDs, stop finish. No children actually run. |
| 11 `thinking-on` | native high / 4096 | Native mode on a short inverse arithmetic task. | Exactly integer JSON input 11, stop below 4096 with known numeric usage and reasoning-presence true. Reasoning text is discarded. |
| 12 `thinking-off` | off / 4096 | Same task/input/output contract with explicit disabled thinking. | Same correct result and below-ceiling usage, reasoning-presence false. |

The router's one-sentence test is a bounded lexical check; the orchestrator should also read whether the reason supports the selected template. Spawn validates a DAG envelope, not whether its tasks are sufficient, nonoverlapping or correctly solved. Its generic 2-4-node probe is wider than the proposed plugin's maximum 3 children; a 4-node response can pass this interface probe but would not pass that production policy. Usage/latency and all public output remain available for separate assessment.

## Documented feature scope

Official docs read 2026-09-17: [tool calling and beta strict schemas](https://api-docs.deepseek.com/guides/tool_calls/), [thinking control](https://api-docs.deepseek.com/guides/thinking_mode/), [JSON objects](https://api-docs.deepseek.com/guides/json_mode/), [Chat reference](https://api-docs.deepseek.com/api/create-chat-completion/). Full identifier/capacity/pricing/rate URLs are in [API-NOTES](API-NOTES.md).

Free-response `response_format.type=json_schema` is **NOT FOUND** in the Chat reference, which lists text/json_object; it is intentionally not sent. The strict-tool probe is the documented schema-constrained feature. No undocumented parallel_tool_calls parameter is sent. Standard and strict tools stay thinking-disabled because current thinking-tool continuation requires hidden reasoning replay, incompatible with durable custody policy. Router, spawn and thinking pair use json_object plus local schema validation.

## Recorded custody

[run_probes.py](probes/run_probes.py) reuses the repository endpoint registry, canonical digest and validated payload builder. It uses a local HTTP/response layer to retain public tool_calls that the current text transport drops. Standard route is the registry's `/v1/chat/completions`; strict route is `/beta/chat/completions`. Requested and returned identities remain distinct. HTTP redirects are refused.

Every actual call writes `probes/records/<name>.request.json` before network and `<name>.response.json` afterward. Every request/response also binds the exact runner, provider transport and endpoint-registry file hashes, plus the assessor qualified name and contract version. Requests contain exact structured payload, documented UTF-8 compact serialization, exact sent-body SHA256/byte count, canonical repository digest, endpoint/settings and epoch. The exact wire bytes are reconstructed unambiguously by the recorded serialization and are the bytes actually sent. Responses contain start/end epoch, monotonic latency, usage where reported, public answer/tool calls, returned identity, finish reason, raw-response digest/length, hidden-reasoning presence and host assessment. Raw native reasoning is never stored. Missing usage remains unknown; failed transport does not imply zero spend.

The key is read only from DEEPSEEK_API_KEY at dispatch time, checked for echoes in raw/escaped/decoded forms and never written. Raw HTTP error bodies are suppressed. An echo preserves digest/length and a failure marker, not content. Strict JSON decoding rejects duplicates and non-finite numbers. All text writes are Python UTF-8 with newline=''. No real filesystem/network/engineering tool is given to the model; tool results are deterministic local fixtures.

Output is restricted to a child directory under research/deepseek-flash-pilot/probes. A nonempty directory refuses before credential access and files use exclusive creation. On interruption, retain partial request/response records; a missing response can represent a spent request. There is no resume/retry/automatic new-directory behavior. Any new attempt needs its own orchestrator decision and identity.

## Reading the results

Report individual pass/fail/unknown outcomes, returned tool choices and arguments, router confusion, spawn dependencies, finish reasons, usage and latency. Tool/API failures do not establish that template-based JSON orchestration is impossible. All-green results show initial interface viability only: this tiny purposive sample cannot estimate production reliability or demonstrate engineering, long-context use, full synthesis, recovery, substantive judgment or superiority over matched multi-call controls.
