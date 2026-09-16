# Personal prose reasoning CLI

Paste a problem into a UTF-8 text file, choose cycles and a recipe, then run from `C:\Dev\miniReason`. This is a personal working tool. Its output is a working answer with its objections, not a finding. Offline delivery has exercised recording and routing with scripted responses; live usefulness remains to be inspected by the owner.

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONPATH='src;tests'
$env:TMP='C:\tr12'
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -c "from pathlib import Path; Path(r'C:\tr12').mkdir(exist_ok=True)"
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' tools/reason.py run --problem work/review12/smoke-problem.txt --cycles 2 --recipe cross-family --baseline --mode live
```

Supply `DEEPSEEK_API_KEY` and `OLLAMA_API_KEY` through the process environment using your existing secret setup. The CLI does not read `.env`, print key values or store them. The command above is a proposed live smoke run; this offline delivery has not executed it. To exercise plumbing without contacting any service, replace `--mode live` with `--mode offline`; offline is also the default. Offline answers are conspicuously labelled fixtures, not answers to the problem.

## Recipes

A recipe is a named, fixed composition. It is copied exactly into the run as `recipe.json`, and its SHA-256 appears in the run identifier and configuration. A custom JSON path is accepted by `--recipe`; supported schema and component paragraphs are illustrated by `src/minireason/reason/recipes/*.json`. The inventory cited by those recipes is retained in `work/w12/INVENTORY.md`, with complete source locations. That ignored engineering inventory is a local handoff artifact, not a published observation.

| Recipe | Seats and composition | Logical calls before baselines, repairs or retries |
|---|---|---|
| `single-family` | DeepSeek Flash conjecture, one critic and use; explicit return | `1 + 3 * cycles` |
| `cross-family` | DeepSeek Flash conjecture/return; Qwen3.5-397b and GLM5.3 critics; Qwen use | `1 + 4 * cycles` |
| `cross-family-rival` | Same cross-family composition, plus Kimi K3 alternative each cycle | `1 + 5 * cycles` |

Each seat is an object such as `{"endpoint": "deepseek-flash", "thinking": "native"}`. Thinking is `native`, `off` or `gateway-default`. All shipped direct DeepSeek seats use native thinking, including return, which reuses the conjecture seat. Ollama seats use gateway-default: this adapter has no explicit on/off control for them. Hidden native reasoning is discarded; public derivations are retained. Unsupported explicit gateway controls are refused.

CONJECTURE makes a working prose answer available while holding the exact problem, named endpoint and declared resource settings fixed. Its original text remains inspectable after any revision.

CRITIC makes objections available, each naming what it would defeat. The cross-family recipes use different underlying lineages from the conjecturer. Two critic seats read the same answer independently, with prior objections, their dispositions, prior cycle history and the current rival when present. Each objection must name the exact step or claim challenged and evidence or a derivation that would show it wrong; merely requesting more caveats is forbidden. The single-family recipe deliberately keeps one lineage and does not supply that separation. These arrangements are prospective compositions; the earlier record does not establish their general advantage.

RETURN delivers the exact objection strings and IDs to the conjecturer's next input. For every open objection the returned answer must supply `taken-up`, `rejected-with-reason`, or `unresolved`, with a reason. Omitting one triggers one recorded schema-repair call; a second invalid response stops the cycle as `SCHEMA_FAILURE`. This check preserves the accounting of criticism; it does not judge whether the prose criticism or response is sound.

USE poses a concrete question that depends on the working answer, derives its answer independently from the PROBLEM alone, then derives it separately from the WORKING ANSWER. The minimal response fields are `question`, `problem_derivation`, `working_derivation` and `objections`; both derivation strings include their conclusion. It must raise an objection if the conclusions disagree or the working answer cannot decide the question. The parser checks fields, not the truth or independence of either derivation. The use reader can be wrong. Its new objections are unresolved in the current trace and delivered to the next return; they are never silently treated as addressed. Arbitrary prose has no general external correctness oracle in this tool.

RIVAL, when selected, offers an alternative answer visible to criticism and return. The rest of the composition remains fixed. A rival is not an automatic decision about which answer the owner should accept.

STOP completes at `cycle_budget`, or earlier at `no_new_objections` when the current critic lists and use list are empty and no unresolved objection remains. These names describe the occurrence and its resource boundary. Silence is not a certificate of truth.

BASELINE with `--baseline` adds one bare call on the conjecturer and one with explicit native thinking if supported by the local adapter. Both receive only the original problem and the same answer instruction, with the same 8192 completion ceiling. The DeepSeek conjecturer supports both controls. Nothing is computed over the texts. The loop spends extra calls and tokens; this is not a matched multi-call experiment.

## Commands and artifacts

```powershell
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' tools/reason.py status --run runs/<printed-run-id>
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' tools/reason.py resume --run runs/<printed-run-id>
```

`run` accepts `--problem`, `--cycles` (1 to 9999), `--recipe`, `--baseline`, `--out`, `--mode live|offline` and `--retry-transport N` (default zero). `--out` must name a new directory. Runs default to the gitignored `runs/` directory; no study directory is created. Short paths are checked before initialization, reserving room for nested evidence below 200 characters. Keep a custom output root short.

Read `ANSWER.md` first (last returned answer with open objections beneath it), then `TRACE.md` (every objection and its disposition for each cycle from introduction), then the relevant `cycles/cNNNN/CYCLE.md` (including both use derivations). Read `BASELINE.md` alongside the working answer when requested. `RUN.md` states seats, per-attempt thinking controls, schema-repair count, recipe identity, cycles, attempted calls, completion ceilings, usage where supplied, stop reason and claim ceiling. `problem.txt`, `recipe.json`, `endpoints.json` and `config.json` freeze inputs. `calls/<logical-call>/aNN/` contains an epoch-stamped request intent, public response/outcome and underlying provider records including wire request custody. Native hidden reasoning text is discarded by the reused transport. `state.json` and Markdown are derived views; original provider observations remain in their distinct attempt directories.

Every call has an 8192 completion-token ceiling and a 300-second wall. A wall stop is `TRANSPORT_OR_RESPONSE_ERROR`; a token-length stop is `CEILING_HIT`. Input tokens are additional and grow with problem/history length. No transport retry occurs by default. If explicitly supplied, `--retry-transport N` permits up to N additional attempts per logical call for the named transport error, each with its own files and call count. A terminated remote request may still have incurred provider usage; unknown usage remains unknown. Fences and surrounding prose are tolerated by extracting the first top-level JSON object. A schema-invalid public output permits exactly one repair call for that logical call, in a new attempt directory: the model receives its own public output and the same contract, endpoint, thinking setting and ceiling. A second schema failure stops as `SCHEMA_FAILURE`; a failed repair is never retried, even with transport retries enabled. There is no retry for a ceiling stop. With L planned logical calls and N configured transport retries, the maximum attempt allowance is L * (2 + N), before early stopping. For cross-family, two cycles and baselines: 11 normal calls, at most 22 with schema repairs and zero transport retries.

Resume reconstructs completed calls from the run directory and uses their existing responses. It can continue after an interruption between completed calls, including when the provider response was saved before the outer recorder finished. A request whose delivery outcome is unknown stops as `INTERRUPTED_CALL` rather than replaying it. Resolve that evidence manually; if a fresh attempt is desired, create a separately identified new run. Simultaneous writers are refused as `RUN_BUSY`. Edited frozen problem, recipe or endpoint bytes refuse as `RUN_INTEGRITY_ERROR`.

A failed cycle is recorded and the run stops. Other named refusals include `KEY_MISSING`, `SCHEMA_FAILURE`, `INCOMPLETE_GENERATION` for a non-length incomplete response, `SECRET_IN_REQUEST`, `CREDENTIAL_ECHO`, provider `HTTP_<status>` and path/configuration errors. Preserve the failed directory. A model response can be a useful prose contribution even when it fails the custody schema; its public text remains in provider evidence. Any investigation of comparative benefit needs separately declared information conditions, matched multi-call controls and substantive reading.
