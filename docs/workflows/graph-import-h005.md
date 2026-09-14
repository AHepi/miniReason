# H005 graph import

> **I7.** No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).

Read [the decision ledger](../DECISION_LEDGER.md), [STATUS](../STATUS.md) and [the experiment workflow](experiment.md) first. This route replays a finished, hash-pinned H005 occurrence into a harness-spec-v1.3 epistemic graph. It adds no evidence: it re-expresses evidence that already exists in a second vocabulary, and reports what that vocabulary cannot carry.

The importer's design notes, deviations and open questions are [h005-import-notes-2026-09-14.md](../design/h005-import-notes-2026-09-14.md); read them before changing the mapping.

## What it does

`python tools/import_h005.py <occurrence-dir> <out-root> [--problem daily] [--arm mini_fcl] [--cycle 1] [--dry-run] [--why <artifact-id>]` reads one occurrence directory and writes one new `deepreason_core` graph root: `objects/`, `blobs/`, `log.jsonl`, plus `REPORT.md`, `report.json`, `side_table.json` and `residue.json`. The library entry point is `minireason.graph_import_h005.import_occurrence`.

Each H005 node contribution becomes one `Artifact` whose content is the authored `body`. Its FCL-1 `commitments` document becomes a second artifact (codec `json`) that the node artifact mentions, so the document stays addressable without acquiring an attack surface. Each FCL `commitment` record becomes an observation-valued `Commitment` plus the research problem spec §12 spawns when no evidence covers it. Each FCL `objection` with an external target becomes an argumentative `Warrant` and a validity node. Each FCL `problem` becomes a `Problem`. `claim` and `use` records map to no spec construct at all and are reported, one residue entry each. Every artifact this import mints — node, FCL-1 document, validity node — carries `provenance.role = import`.

Event order is the occurrence's own: wave ordinal, then position inside the wave. Every `Event.ts` is a `finished_utc` from the occurrence's receipts, so two imports of the same bytes produce byte-identical roots. `Event.llm` is always null.

**Core dependency.** `Event.ts` is pinned only because the vendored `deepreason_core.harness.Harness` accepts one optional `clock` callable (see the notes, §4). That parameter is a hard dependency of this route, not a nicety: without it the timestamp comes from the wall clock, two imports of the same occurrence differ, and replay determinism is gone. If the core is republished without it, the library refuses with `MappingError(CORE_CLOCK_UNSUPPORTED)` rather than writing a root it cannot reproduce.

## What it does NOT do

- **No semantic verdict.** The importer never calls a provider, never runs a rubric judge and never mints a `demonstrative` warrant. Every warrant is `argumentative` with `commitment`, `verdict` and `trace_ref` null.
- **Statuses are not standing in the world.** `accepted` / `refuted` are the grounded extension of the attack relation *the authors themselves declared*, nothing more. An unattacked artifact is **accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.**
- **No cross-arm comparison.** A prose commitment surface is never parsed, so no warrant, no attack edge and no refuted label can arise from a prose arm. Whenever a scope spans more than one arm, `REPORT.md` says so in a paragraph naming the arms actually in that scope — everything the paragraph *claims* is a module constant that no run can soften — twice — in "What this is, and what it is not" and immediately above the labels table — and the CLI prints it before the labels. Any cross-arm reading is root's, not this instrument's.
- **No interpretation.** Reading these labels as evidence about FCL-1, about Mini, or about any contribution's merit is reserved to root (PROTOCOL.md:62). The report says so in its own banner.
- **No transport status becomes a verdict.** `delivery_status`, `envelope_status`, `finish_reason`, `failure_type` and `status` are provenance only, recorded in the side table.
- **An empty `commitments` string is not a missing commitment.** Where a node's `commitments` string is empty, the study harness's strict JSON decode of the returned envelope failed and `decode_contribution` took its failure branch, storing the whole returned text as `body` and `""` as `commitments`. Root's published review, [`docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md`](../reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md), measured that the same bytes parsed non-strictly *do* contain a commitments field: the commitments were authored and lost in decoding. The commitment surface is therefore **UNAVAILABLE, not absent**, and this is not evidence that the author declined to commit. The importer does not repair it (I4) and records `commitment_surface_state = "unavailable_decode_failure"` in the side table.
- **No inferred dependence.** Visibility is not dependence. Only an explicit FCL `depends` ref that resolves to a *different* artifact becomes a dependence ref.
- **No repair.** A commitments string that is empty, prose, or claims FCL-1 and fails to parse leaves the artifact with an empty `Interface`, reported, never reconstructed.
- **No writes into the occurrence.** The occurrence is opened read-only; the output root is created with `exist_ok=False` and may not lie inside it.

## Custody

The importer refuses to run — before creating anything — unless the occurrence's own bytes verify. Two kinds of check are reported separately in `REPORT.md` and in `report.json` (`custody.cross_file`, `custody.self_consistency`), because they are worth different amounts:

**Cross-file** — two independently written files must agree, so a coherent rewrite of either is detected:

| check | source |
|---|---|
| `plan.material_sha256 == sha256(material.json)` | `plan.json` |
| `plan.manifests[tid] == sha256(manifests/<tid>.json)` | every manifest the plan pins |
| artifact bytes `== receipt.artifact_sha256` | `responses/.../<node>.json` |
| `receipt.status == delivery_status`, `receipt.envelope_status == envelope_status` | recorded, never read as a verdict |
| `sha256(responses/<node>.txt) == public_text_sha256` | the raw provider text |
| `attempt.request_sha256 == receipt.request_sha256` | attempts and responses |
| `study_digest(requests/<node>.json) == attempt.request_sha256 == receipt.request_sha256` | the request record |
| `request.trace_sha256 == study_digest(traces/<node>.json)` | the request record pins the trace — counted as run only where the request record is itself pinned by an attempt or a receipt |
| `sha256(provider/<coord>/call-0001.{request,response}.json) == receipt.provider_{request,response}_sha256` | the provider call bytes |
| `attempt.wave_id` is the wave listing the coordinate, and `wave.request_hashes[coord] == attempt.request_sha256` | attempts and waves |
| each projection's `selected_source` hashes equal the authored artifact record it names | traces, counted **per projection**, for every node |

**Internal consistency only** — a file compared against itself. These catch truncation and incoherent edits; they cannot detect a coherent rewrite:

| check | source |
|---|---|
| `plan_id == study_digest(plan without plan_id)` | `plan.json` |
| `sha256(body)`, `sha256(commitments)` match their recorded digests, and `<field>_ref == <field>_sha256` | the artifact record |
| the artifact record's own coordinate is the one it is filed under | the artifact record |
| `sha256(trace.original_brief) == original_brief_sha256` | the trace |
| the brief's `[label]` lines index the projection slots they name, and the label sets agree | the trace |
| the exposed task label agrees with `trace.task_artifact.artifact_id` | the trace |

**The trace is pinned before it is used, and never used unpinned.** `requests/<coord>.json` fixes the trace by `trace_sha256`, and the request record is itself fixed by `attempt.request_sha256` and `receipt.request_sha256`. That whole chain is verified inside per-node custody, *before* the trace reaches the label index or the projection resolver, so a rewritten `selected_source` cannot steer a reference (`TRACE_NOT_PINNED`, `REQUEST_RECORD_MISMATCH`, `PROVIDER_BYTES_CHANGED`, `PROVIDER_HASH_MISSING`).

The chain is only as strong as its first link, and the report says which link it got:

- **No request record at all → refused** (`REQUEST_RECORD_MISSING:<coordinate>`). The trace is the most load-bearing input this import has — the label index, the projection index and every two-hop reference are read off it — so a coordinate whose trace nothing pins is not admitted. This is the same posture as `NO_LEADING_RECEIPT`, and it costs nothing here: all 22 request records exist in `occurrence-01`.
- **A request record pinned by neither an attempt nor a receipt** (both absent) → admitted, but `request.trace_sha256 == digest(trace)` is then one file agreeing with another file that nothing independent pins. `trace_pinned` and `request_record` are counted as **not run** for that coordinate and the absent input is named in the rendered row; neither is ever spelled as a bare "verified".
- **A non-`FAILED` receipt** must carry both `provider_{request,response}_sha256` as non-null strings **and** both call files must exist. A null hash beside a deleted file used to compare equal (`None == None`) and pass; it now raises `PROVIDER_HASH_MISSING:<coordinate>:<part>`.

**What of `read_terminal()` is reproduced.** `tools/multicycle_commitment_study.py::read_terminal` is the study's own terminal check. Reproduced here: the coordinate agreement across request/trace/attempt/receipt; `request.trace_sha256 == digest(trace)`; `attempt.request_sha256 == receipt.request_sha256 == digest(request)`; the provider call byte hashes against the receipt (skipped only for a `FAILED` receipt, as there); `sha256(artifact record) == receipt.artifact_sha256`; `responses/<node>.txt` against the recorded public-text digest; and `receipt.status`/`envelope_status` against the artifact record. **Not** reproduced: `request.messages_sha256 == digest(request.messages)`, `request.provider_payload == payload_for(...)` and `request.settings == settings_for(arm).to_dict()`, and the re-derivation of the artifact through `decode_contribution` / `authored_artifact`. Those need `payload_for`, `settings_for` and `decode_contribution` from the repository, and importing that module would execute `sys.path.insert` at import time and pull in the live DeepSeek transport — which invariant I1 forbids. An occurrence directory alone cannot supply them.

**A receipt-less coordinate is admitted, not refused.** If `responses/<node>.json` or the attempt is missing (the request record is not optional — see above), the coordinate is still imported: the absent inputs are listed in `side_table.json.artifacts[].absent_inputs`, and every check that could not run over it is counted as not-run rather than as verified. `REPORT.md` renders `verified (n/m nodes; k coordinate(s) had no receipt: …)` and names them; it never says a bare "verified" for a check that did not run everywhere. The one exception is the leading coordinate: a receipt-less coordinate inherits the *previous* coordinate's `finished_utc`, and the first coordinate in registration order has no previous one, so a scope whose first coordinate has no receipt is refused with `NO_LEADING_RECEIPT` rather than back-dated to a time that belongs to some later node. A scope with no receipt at all is refused with `NO_FINISHED_UTC_IN_SCOPE`.

**Path containment.** Every coordinate component — problem, arm, node, wave id, cycle — is validated against `^[A-Za-z0-9_-]+$` before it is ever joined onto a path (`COORDINATE_COMPONENT_UNSAFE`), and every read and existence probe additionally asserts that the resolved path is the occurrence root or a descendant of it (`PATH_ESCAPES_OCCURRENCE`). Coordinates arrive from files — `waves/*.json`, `material.json`, each record's own `coordinate` block — and are concatenated into read paths, so they are checked at the boundary rather than trusted. `material.json` and every `waves/*.json` are parsed through the same wrapping reader as everything else, so a truncated one is `OCCURRENCE_FILE_MALFORMED_JSON` rather than a bare `ValueError`, and a wave id that is not `wave<digits>` is `WAVE_ID_MALFORMED`.

A failure raises `CustodyError` and the CLI exits 2 with nothing written. `report.json` records the sha256 of every file read.

**Nothing is written at the out-root until everything is written.** The graph root and the four report files are built in a uniquely named temporary sibling directory of `out_root` and renamed into place only after the last file is written and the event log has been verified; on any failure the temporary directory is removed. "Nothing was written" therefore holds for a mapping failure (exit 3) exactly as it does for a custody refusal (exit 2), and an operator is never handed a root with a log and no report. The out-root is still write-once: if it already exists the import is refused (exit 4) **before any occurrence byte is read**.

## Exit codes

| code | meaning | stderr |
|---|---|---|
| 0 | the import succeeded | — (an unresolvable `--why` prints `WHY_UNRESOLVED:` and still exits 0: the root is written, only the display selector was wrong) |
| 2 | custody refusal — a custody check failed, including a missing occurrence file (`OCCURRENCE_FILE_MISSING`) or malformed JSON (`OCCURRENCE_FILE_MALFORMED_JSON`), both raised as `CustodyError` by the reader | `CUSTODY_REFUSED: <code>` |
| 3 | the occurrence is well-custodied but could not be mapped (`MappingError`), including `EMPTY_SCOPE` — the occurrence holds no coordinate at all | `IMPORT_FAILED: <code>` |
| 4 | the destination is refused (`OutRootRefused`: `OUT_ROOT_INSIDE_OCCURRENCE`, or the root already exists) — the occurrence is fine | `OUT_ROOT_REFUSED: <code>` |
| 5 | the occurrence holds coordinates but `--problem`/`--arm`/`--cycle` matched none of them (`SelectorMatchedNothing`, a subclass of `MappingError`) — the occurrence and the destination are both fine and the selector is wrong; stderr lists the selectors given and the problems, arms and cycles that exist | `SELECTOR_MATCHED_NOTHING: …` |

`argparse` keeps its own usage-error behaviour and this tool does not remap it; a usage error is told apart from a custody refusal by the `usage:` line argparse prints and by the absence of `CUSTODY_REFUSED:`.

## Residue

`residue.json` is the honest cost of the mapping. Every code carries a `severity` (`lossy`, `extension`, `unmapped`, `informational`, `error`) and a counting `unit` (`ref`, `record`, `document`, `edge`, `artifact`, `problem`, `file`); counts follow the unit, so 17 `depends_intra_document` means 17 references, while 2 `warrant_edge_deduplicated` means 2 attack edges. Each entry carries the verbatim source text that was not mapped, the carrier coordinate, the carrier's spec artifact id and the reason.

**What "reported" claims, exactly.** Every FCL record in scope is accounted for *at record granularity*: each record is either mapped to a spec construct or carries a residue code, and `side_table.json.records[]` shows which, per record, with the codes it raised. The same holds for every reference the importer resolved. It is **not** a claim that every nuance inside a mapped record survived the mapping, and it is not a claim of semantic completeness — the codes are the granularities the closed vocabulary names, nothing finer. `claim_record_unmapped` exists because the earlier "`uptake_refs_unmapped` already covers every claim" reasoning was false: in `daily/mini_fcl/cycle01/rival`, claims `r1`, `r3` and `r4` are not in the document's `uptake` list, so nothing reported them.

The largest entries for `daily/mini_fcl/cycle01` are the 32 `uptake` references (a local standing claim, never a status), the 17 document-local `depends` references, the 15 `claim` records, the 9 `use` records, the 9 document-local `mentions`, and the 5 problems whose trigger had to be approximated.

When any `error`-severity code fires, `REPORT.md` carries a banner line under the I7 banner and the CLI prints one under its I7 line.

## How to read REPORT.md

1. The **I7 banner** is the first thing in the file and governs everything after it; an error-severity banner follows it when one is warranted.
2. **Custody** — split into cross-file and internal-consistency-only, each row saying how many subjects it ran over.
3. **Labels** — artifact, id, status, **surface**, who attacks it, how many warrants it carries, under the multi-arm paragraph when the scope spans arms. Read a status together with its attackers and its surface; never alone. The surface column is the commitment surface this import actually read for that artifact — `read`, `NOT READ (prose)`, `UNAVAILABLE (decode)`, `PARSE FAILURE`, `SCHEMA FAILURE`, or `n/a` for an artifact that has none (a validity node, an FCL-1 document). A status computed over a surface that was not read carries no information about the contribution.
4. **Attack / support edges** — `att` is the criticism the authors declared; `dep` is empty here because every `depends` ref in this occurrence is document-local and node granularity would turn it into a self-loop. That is a property of the mapping, not a result about the occurrence.
5. **Warrants** — a `target kind` of `validity_node` marks criticism of a criticism.
6. **Commitments** — observation-valued, with the research problem each one spawned.
7. **Residue** — the table of codes, severities, units and counts.
8. **Why** — the attack/defence chain behind each label, also available as `--why <artifact-id>`. For an artifact whose commitment surface was not read, the chain ends with that surface's state and what it means.

## Declared deviations

`REPORT.md` prints each of these with its count in the scope actually imported, or marked **(not triggered in this scope)**.

- **`adjudication_batched`** — the vendored P0 `Harness` re-adjudicates inside every registration event and exposes no public `Adj` emitter. The import writes through the registration API only and forges no log line, so there is no separate terminal `Adj` event; status flips are recorded in each registration event's `state_diff.status_changed`.
- **`problem_trigger_approximated`** — `SpawnTrigger` has no `import` member, so imported FCL `problem` records use `seed`, which slightly over-claims. The clean fix is an enum addition, requested rather than papered over.
- **`problem_trigger_research_not_in_v13_enum`** — research problems use `SpawnTrigger.RESEARCH` with empty `criteria`; the originating commitment is named in `provenance.from`.
- **`depends_intra_document`** — a `depends` ref resolving to its own carrier would be a `dep` self-loop, i.e. a cycle; it is dropped and reported, so this occurrence's `dep` is empty and pass 2 is a no-op.
- **`claim_record_unmapped`** — an FCL `claim` asserts content without proposing a test, so it maps to no spec construct; it survives in the artifact body and in the FCL-1 document artifact, and is reported once per record.
- **`objection_self_target_only`** — a wholly self-targeting objection mints nothing. A Dung self-attack means "this argument is self-defeating", which is not what an intra-document caveat asserts.
- **`criticism_of_criticism_retargeted`** — an objection against a record this import already reified as a warrant attacks that warrant's validity node, so the criticism keeps its force through the spec §1 closure instead of collapsing onto the carrier.
- **`criticism_of_criticism_intra_document_dropped`** — the one exception to the rule above. When the criticised criticism is carried by the *same* artifact (`objection.o4` against `o1`/`o2`), retargeting would become a **self-attack through the carrier closure**: an attack on the validity node is lifted onto every carrier of the warrant, and here the carrier is the objector itself. It is therefore not retargeted, and the loss is counted under its own code rather than left silent.

## Tests

`tests/test_graph_import_h005.py` reads the **real** occurrence,
`experiments/diagnostics/H005-open-prose-commitments/occurrence-01`, read-only; there is no fixture copy. `tests/data/h005_import_pins.json` pins the sha256 of all 162 files, and `setUpModule` re-hashes every one and refuses — naming each differing path — rather than adapting.

**The module fails, it does not skip, when the occurrence is absent.** CI runs on a full checkout, where the occurrence is always present, so its absence there means a broken checkout and must be loud: a skipped module is a green run that tested nothing. Set `H005_IMPORT_ALLOW_SKIP=1` to skip deliberately (a partial checkout, a tree without the experiments directory), or `H005_OCCURRENCE_ROOT` to point the tests at a checkout elsewhere.

## After an import

The graph root is evidence about a mapping, not about the world. Publish it with the occurrence path and plan id it came from, and record in the ledger which corrections to `mapping.md` were applied (see [the design notes](../design/h005-import-notes-2026-09-14.md)). Do not quote a label as a result.
