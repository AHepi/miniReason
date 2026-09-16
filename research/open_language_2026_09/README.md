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
