# Open-subject Forge configuration pack

## What this adds

This pack supplies four configuration templates, an additive source-copy seat and a public-text transport adapter for the Forge code inspected at commit `712be48267e973cfa001848c71a2ab3428becf53`. It leaves the existing Forge engine, historical configurations and experiment observations unchanged. The accompanying [research program](RESEARCH_PROGRAM.md) investigates meaning-preserving languages with open-ended expressive resources rather than a fixed compression objective.

The templates do not require a problem to have a defined search space, agreed interpretation, formal language, executable test, target answer or success criterion. A participant can criticise the framing, introduce new notation or conceptual distinctions, retain ambiguity, change the question, or leave a contribution unfinished. These permissions do not guarantee reasoning or comprehension; they remove particular admission barriers so those phenomena can be investigated.

## The four templates

`open_turn` offers one unrestricted contribution and one continuation turn per cycle. It is the least role-prescriptive option. It does not ask for a conjecture/criticism ritual or require a conclusion.

`critical_return` offers conjecture, criticism, return and continuation. The titles are invitations, not enforced semantic categories. A critic need not invent an objection; a return need not repair something; a continuation need not select a winner. Earlier participant text remains available across cycles.

`language_workshop` offers invention, use, challenge and continuation. No initial grammar, ontology, mandatory operator inventory, Lean target or compression ratio is prescribed. The user can begin with an ill-defined concern. Participants may keep prose, propose partial conventions or decide that an apparent language problem is really a problem with the question.

`blind_roundtrip` offers encoding, source-isolated reading, comparison and continuation. Only the current encoding and its included conventions reach the reader's Forge prompt. The comparator receives the source and relevant discussion. This is an optional diagnostic condition, not the default access policy for all inquiry. Provider sessions must also be stateless for the source isolation to be meaningful.

All four begin with a deterministic full-source-copy stage. This is transport work, not an AI reasoning contribution. Only model seats consume the declared model-call budget.

## Findings in the actual Forge code

The [manifest compiler](../../src/creib/forge/mini/manifest.py) requires exactly one `mini.verdict.v1` stage before the end marker. The pack retains that internal identifier but gives the stage a continuation instruction and no semantic decision authority. The [stop implementation](../../src/creib/forge/mini/stops.py) and runner host-stop path do not interpret that stage's prose as a decision. The templates explicitly use `mini.stop.never`; finite resource boundaries still apply.

The [response reader](../../src/creib/forge/mini/kinds.py) requires a JSON envelope. The [runner](../../src/creib/forge/mini/runner.py) additionally requires nonblank body and commitments strings and can drop malformed responses. Merely setting `format: null` does not remove this envelope requirement. The new `VerbatimEnvelopeResponder` therefore wraps the entire returned public text without interpreting it. Unknown notation, malformed JSON and undeclared fields inside the returned text remain ordinary body content. Host-written commitments are explicitly transport metadata, not an inferred participant belief. Empty text remains in the sidecar and receives a clearly labelled host marker, not a fabricated model contribution.

The [evidence renderer](../../src/creib/forge/mini/evidence.py) clips each paragraph legend to 160 characters. Retaining full source bytes in storage is not the same as showing them to a model. The new machine seat copies permitted source files into complete text artifacts, respecting its evidence ports, windows, read permissions and explicit evidence routes. Source text is not semantically filtered. Input files, rather than the short manifest problem field, carry the original opening and materials. This avoids treating the 8,192-character problem field as the maximum size of an admissible concern.

The default two-call path asks for commitments separately and can omit the original context. These templates instead use one public-response call per model stage. The entire returned text remains available; no successful commitment-extraction call is required for an idea to reach later turns.

The [attention implementation](../../src/creib/forge/mini/attention.py) offers a count-based preference policy as well as an off policy. This pack uses `mini.attention.off`, so no unanswered-criticism count or content score controls ordering. All-history discussion ports preserve earlier participant artifacts; they do not replace the discussion with a preferred answer. The source-copy artifact is read from the current cycle to avoid repeatedly displaying identical historical copies.

The [H004 report](../../experiments/diagnostics/H004-partial-language-continuation/REPORT.md) contains a particularly relevant historical failure: a participant treated a prose claim as illegitimate because the supplied formal vocabulary lacked the property it discussed. This pack does not convert that vocabulary limitation into a host admission rule. The historical report is evidence, not authority to fix the new inquiry's subject or method.

## Generate usable manifests

Work in a checkout of the branch containing `src/minireason/open_inquiry.py`, with the repository installed in the usual way:

```sh
python -m pip install -e .
python -m minireason.open_inquiry --opening concern.txt --out open-language-run --cycles 2
```

The command writes four actual Forge JSON manifests under `open-language-run/configs`, complete input files under `inputs`, byte-count and SHA-256 input receipts, and a separate execution-envelope record. It makes no model call. An existing output directory is not overwritten. An empty UTF-8 opening file is permitted. Additional complete text sources can be supplied with repeated `--source path.txt` options.

The example's two cycles are an operator-selected finite occurrence, not a research requirement or semantic stopping rule. The CLI deliberately requires a cycle choice rather than silently inventing one. Optional `--max-calls`, `--max-completion-tokens` and `--completion-tokens-per-call` arguments expose existing Forge budget controls. The last two must be supplied together, and a live responder must enforce the same per-call cap.

The downloadable pack also includes ready-generated example manifests. Their concern is deliberately unresolved, and their two-cycle envelope is illustrative only. Change the source material or generate a new bundle without turning it into a formal task specification.

## Compile and exercise the real engine offline

Use the companion entry point rather than passing these manifests directly to an unextended generic Forge CLI. The source-copy kind must be registered, and the wrapper supplies the non-filtering public-text envelope.

```python
from pathlib import Path
from creib.forge.mini.executor import Reply
from creib.forge.mini.manifest import compile_manifest
from minireason.open_inquiry import install_source_bridge, run_open_inquiry

class OfflineDemo:
    def reply(self, request):
        return Reply(
            text=f"This is a scripted routing demonstration at {request.stage_id}; the problem remains unsettled.",
            prompt_tokens=0,
            completion_tokens=0,
        )

install_source_bridge()
plan = compile_manifest(Path("open-language-run/configs/critical_return.json"))
outcome = run_open_inquiry(
    plan,
    Path("new-offline-output"),
    OfflineDemo(),
    responder_id="offline demonstration; no model used",
)
print(outcome.stop_reason)
```

This checks a route through the actual engine using scripted text. It is not evidence of model reasoning. For an authorised live occurrence, pass an explicitly configured object implementing Forge's `Responder.reply(Request) -> Reply` interface, together with its actual identity. The module does not select a model, retrieve credentials or start a provider automatically. Provider-specific settings and approvals remain separate from semantic admissibility.

The wrapper does not rewrite the upstream request. In particular, Forge's existing `LiveResponder` still sends its JSON-format instructions when used as the delegate. The wrapper prevents returned public text from being lost merely because it violates that format; it does not pretend that the original format request has vanished. A separate unconstrained-output provider adapter would be a further, independently identified prompting intervention.

## What is recorded and what is not

Every textual response returned by the supplied responder is stored exactly in a `verbatim-transport` sidecar with the request object, hashes, reported token counts and the host envelope. The Forge log stores the framed reply through its existing route. These are public responses only. The wrapper does not request or extract native hidden reasoning.

A provider exception is recorded by exception class, without copying possibly sensitive exception text, and propagated without automatic retry. A provider that refuses a length-stopped response before returning a `Reply` cannot be made to expose those missing bytes by this wrapper. Full HTTP-wire custody, completion-status recovery, crash-safe pre-dispatch receipts and exactly-once provider execution are not established by these sidecars. Those require the provider adapter and an appropriate execution system.

Generated bundle files are new files only. Existing run records and old experimental evidence are not rewritten. When a new occurrence is selected, give it a new output root and preserve its predecessors.

## Remaining boundaries

The pack remains a finite text implementation. Forge retains schema bounds, a fixed compiled stage schedule, a mandatory end marker, provider context limits, filesystem requirements and resource limits. None is treated as proof that an ill-defined subject is inadmissible. Host errors should be reported as host errors, not as semantic refutations.

Participants may revise the language or operative problem in their public contributions without changing the host plan. They cannot execute their prose as a permission change, alter the provider budget or install code automatically. Dynamic stage-topology replacement, autonomous retrieval, cross-process resume and automatic promotion into a separately scheduled research program are not implemented here.

All-history visibility can exceed a provider's context capacity. This pack does not silently prune context or claim to solve that problem. A later retrieval or compressed-memory intervention must keep its omissions and original source available for inspection. The source-isolated diagnostic is deliberately narrower than the open discovery routes and is not evidence of complete independence from shared model pretraining.

## Verification boundary

The local unit suite is run with:

```sh
python -m unittest discover -s tests -p test_open_inquiry_unit.py -v
python -m unittest discover -s tests -p test_open_inquiry_routes.py -v
```

The real-engine integration suite is:

```sh
python -m unittest discover -s tests -p test_open_inquiry_forge.py -v
```

The latter tests compilation, two-cycle routing, full text beyond the old excerpt boundary, an empty or absent source, reader isolation, explicit evidence-route isolation and resource stopping. The repository's existing offline CI discovers these files. Actual results and limits belong in `VALIDATION.md`; test definitions alone do not establish a pass. Neither suite measures creativity, universal meaning preservation or the quality of live reasoning.


## Live responder and owner commands: local observation 2026-09-16

REC-20260916-E, 2026-09-16. No provider call was made during this engineering run.

### Feasibility and prerequisite

The pack's eight committed files matched their SHA256SUMS entries. The nine missing example files are now preserved exactly in the repository. Fresh two-cycle configs match all four pack configs both structurally and byte-for-byte.

Native Windows Python cannot currently run the unchanged durable Forge engine: its exclusive blob publisher requires directory fsync and raises PermissionError on this host. The live CLI deliberately stops with TARGET_FILESYSTEM_DURABILITY_UNAVAILABLE before any provider call. No local WSL distribution, Docker or Podman is available. A Linux/POSIX host with a supporting output filesystem must pass the actual Forge tests before a live occurrence. Installing such a host or changing the protected Forge durability implementation is outside this run. A test-only filesystem substitute passing is not a qualification.

The new responder is ready for that supporting-host qualification. It selects an endpoint from the existing registry, sends precisely one user message containing each complete Forge Request.brief, does not request JSON output mode, and reuses the existing recorded transport, subprocess worker and 300-second wall. The Forge brief itself remains unchanged, including any format wording produced by Forge. This adapter does not erase that wording. No retry, schema repair, fallback, hidden conversation state, or automatic successor is added.

### Choose the first template

For an ordinary unsettled concern, begin with open_turn. RESEARCH_PROGRAM.md, “Beginning an inquiry without supplying its answer”, says: “Use open_turn to see what participants do without prescribed argumentative roles.” Start with language_workshop instead when representation itself is the opening concern. critical_return is a separate role-structured configuration; blind_roundtrip is a local communication comparison once there is a concrete preservation question.

The owner still chooses the opening, template, endpoint, thinking setting and resource budget. The commands below propose deepseek-flash with thinking off and a per-call allowance of 8192 completion tokens; those are explicit example choices, not an observed live result or a price quotation.

### Windows: write the concern and generate the bounded bundle

From C:\Dev\miniReason in PowerShell:

~~~powershell
$py = 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe'
$env:PYTHONPATH = 'src;tests'
$env:PYTHONUTF8 = '1'
$env:TMP = 'C:\tw13'
$env:TEMP = 'C:\tw13'
@'
from pathlib import Path
Path(r"C:\tw13").mkdir(parents=True, exist_ok=True)
with Path(r"C:\tw13\concern.txt").open("x", encoding="utf-8", newline="") as handle:
    handle.write("Two descriptions seem to concern the same thing, but combining them loses a distinction I cannot yet name.\n")
'@ | & $py -X utf8 -
& $py -X utf8 -m minireason.open_inquiry --opening C:\tw13\concern.txt --out C:\tw13\owner-ol-bundle --cycles 2 --max-calls 4 --max-completion-tokens 32768 --completion-tokens-per-call 8192
~~~

Edit the Python string to the actual concern before running it. An empty opening is also allowed. All output paths must be new; choose a fresh suffix when files already exist. Additional complete UTF-8 source files can be supplied with repeated --source arguments.

This generator creates four configs with the SAME envelope. The 4-call envelope above is tailored to open_turn; it will stop the other templates before completing both cycles. To give any of the other three templates their complete two-cycle schedule, generate a NEW bundle with --max-calls 8 --max-completion-tokens 65536 --completion-tokens-per-call 8192.

The requested Windows live command is:

~~~powershell
& $py -X utf8 -m minireason.open_inquiry_live --config C:\tw13\owner-ol-bundle\configs\open_turn.json --out C:\tw13\owner-ol-live --endpoint deepseek-flash --thinking off
~~~

On this host it currently exits 2 with TARGET_FILESYSTEM_DURABILITY_UNAVAILABLE and sends nothing. Do not remove the guard or rerun a used output root.

### Supporting host: qualify, then run

After the separate publisher has provided the reviewed checkout on a Linux/POSIX host, use its native Python environment with the repository dependencies installed. Keep the output on a filesystem supporting the unchanged Forge file and directory fsync contract. The following commands assume the owner's concern.txt has been supplied to that host and credentials have been placed in its process environment without printing them.

~~~sh
export PYTHONPATH=src:tests
export PYTHONUTF8=1
python3 -m unittest tests.test_open_inquiry_unit tests.test_open_inquiry_routes tests.test_open_inquiry_forge tests.test_open_inquiry_live -v
python3 -m minireason.open_inquiry --opening concern.txt --out /tmp/owner-ol-bundle --cycles 2 --max-calls 4 --max-completion-tokens 32768 --completion-tokens-per-call 8192
python3 -m minireason.open_inquiry_live --config /tmp/owner-ol-bundle/configs/open_turn.json --out /tmp/owner-ol-live --endpoint deepseek-flash --thinking off
~~~

Do not proceed to the live command if the actual Forge suite or durability preflight fails. This host qualification has not been performed by w13. The E028-specific historical CI workflow is not an open-language execution instruction.

Optionally append --env-file followed by a gitignored, untracked file INSIDE that checkout. The loader admits only DEEPSEEK_API_KEY and OLLAMA_API_KEY, rejects unknown/duplicate names and invalid syntax before changing the environment, and refuses tracked, nonignored or outside-checkout paths including resolved symlink targets. The loader is reused from tools/reason.py. No real .env file was opened during w13; tests use dummy fixtures only.

For Ollama explicit control use an existing .native endpoint such as ollama/qwen3.5-397b.native; --thinking off maps to think:false, native to think:true. A /v1 Ollama endpoint has no supported explicit off/native control in this checkout: omit --thinking to retain its gateway default, or choose its named .native entry. DeepSeek accepts explicit off/native. The default is off where supported and gateway-default otherwise. Endpoint availability and the providers honoring these settings have not been live-tested in w13.

### Two-cycle resource arithmetic

Counts come from the actual manifests: the source-copy machine stage spends no model call; every model stage makes one call, with no retry.

| Template | Calls/cycle | Calls for 2 cycles | Full allowance at cap P | Example at P=8192 |
|---|---:|---:|---:|---:|
| open_turn | 2 | 4 | 4P | 32768 completion tokens |
| critical_return | 4 | 8 | 8P | 65536 completion tokens |
| language_workshop | 4 | 8 | 8P | 65536 completion tokens |
| blind_roundtrip | 4 | 8 | 8P | 65536 completion tokens |

The unchanged pack examples set max_calls, max_completion_tokens and completion_tokens_per_call to null. They declare no completion-token allowance; null does not mean zero. The live CLI refuses those uncapped examples. Regenerate a separately bounded bundle rather than editing the preserved examples.

Forge reserves one full per-call allowance before sending, then charges reported completion usage. The transport sends that cap as max_tokens or native options.num_predict. A provider reporting more than the requested cap is recorded and raises COMPLETION_CEILING_VIOLATED; its reported count is never clamped. A length stop raises CEILING_HIT, preserves its available public prefix and usage, and stops without retry. Failures and smaller budgets can shorten the schedule. Context/prompt tokens and currency spend are not bounded by the completion allowance; all-history prompts grow. The worker gives each call at most 300 seconds (plus local overhead), so four/eight calls have 1200/2400 seconds of summed per-call wall allowance, not a guaranteed whole-run duration.

### Run contents and failure custody

- live-config.json: compiled manifest header, endpoint registry snapshot and actual endpoint, thinking request, cap, zero retries, 300-second wall and epoch receipt.
- durability-probe/probe.txt and durability.json: actual Forge publication capability result. A failure occurs before dispatch.
- run-header.json, log.jsonl and blobs/: unchanged Forge provenance and content-addressed source, prompt and framed public-response artifacts.
- provider/000001/forge-request.json and forge-response.json (then increasing sequence numbers): Forge coordinate, public prompt, public answer/usage or a safe exception type/code, with epoch timestamps.
- provider/000001/transport/worker-input.json and call-0001.request.json / call-0001.response.json: existing worker input, exact request JSON/body hashes, endpoint/settings, public provider result, counts, finish status and epoch timestamps. A timeout can instead leave worker-failure.json plus partial evidence.
- verbatim-transport/000001.json: pack's exact public reply, host envelope and hashes; on failure, delegate-raised plus exception type.
- live-outcome.json: stop reason and completed counters on success, or a refusal/interruption receipt. Ctrl+C may leave only partial evidence; preserve it.

Native hidden reasoning text and credentials are never written. The raw provider chat response is not saved, because it can contain hidden reasoning; its hash and allowed public fields are retained. Exactly-once remote execution across crashes and cross-process resume are not claimed. The CLI refuses an existing root. A provider exception propagates through the real Forge runner: Forge has no provider-exception event and does not emit RUN_ENDED on that path. Custody comes from the adapter/provider JSON and open-inquiry sidecars, not an invented Forge terminal event. Missing usage remains unavailable, never zero.

### What one occurrence cannot establish

The pack's “Research claims not established” says:

> No paid model calls or live language experiments were run. Scripted responders check transport and control flow, not reasoning quality. No claim is made that these templates have demonstrated creativity, meaning preservation, conceptual expansion or combinatorial universality. Provider context growth, autonomous retrieval, cross-process resume, host-topology mutation and complete HTTP-wire custody remain outside this implementation.
>
> A later completed CI result should be recorded as a new dated observation, preserving this history. It must identify the actual tested commit and must not turn a transport test into a proof of semantic adequacy.

One fresh occurrence supplies an inspectable inquiry history. It cannot select a superior template, establish an advantage over bare/native reasoning or attribute a change to criticism without suitable comparisons. The programme calls for matched materials/settings, repeated occurrences and matched multi-call controls when additional calls could explain an apparent advantage.

Evidence and exact local results are indexed in work/w13/INDEX.md. Publication and the live occurrence belong to separate owner-directed tasks.
