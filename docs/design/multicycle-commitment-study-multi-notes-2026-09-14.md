> Published verbatim, body unedited: this document was written against the staging tree `scratchpad/runner-multi/`, so `NOTES.md`, `FIXES.md` and the staged `src`/`tests`/`tools` paths it names are that scratchpad tree and not any path in this repository. Here the fork is `tools/multicycle_commitment_study_multi.py`, its suite is `tests/test_multicycle_commitment_study_multi.py`, the register and its six occurrences are under `experiments/diagnostics/F001-fork5-multifamily/`, the review closure this file's §-numbers refer to is `docs/sources/multicycle-commitment-study-multi-review-fixes.md`, and the operating summary is `docs/workflows/fork5-multifamily.md`. The build inputs it lists — `src/minireason/provider_openai_compat.py`, `src/minireason/data/endpoints.json` and `src/minireason/graph_import_h005.py` — are this repository's already published files, byte-identical to the staged copies at publication (`cdc4b571…`, `03eff16b…`, `e5bd327a…`), and were not republished.

# Staging notes — multi-provider fork of the H005 runner

Staged at
`/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/runner-multi/`
in repository layout. **`/home/user/miniReason` was not modified**
(`git status --porcelain` empty, HEAD `8a99d3fb4f9ab39e2a061d8a1389c11fb6c4be5b`,
before and after).

```
tools/multicycle_commitment_study_multi.py                    the fork (1840 lines)
tests/test_multicycle_commitment_study_multi.py               69 offline tests
experiments/diagnostics/F001-fork5-multifamily/
    material.json                                             H005's material verbatim + study_id
    PLAN.md                                                   the pre-registration
    occurrence-0{1..6}/arms.json                              19 arms, six families,
                                                              each scoped to daily / cycle 1
NOTES.md                                                      this file
```

Build inputs, copied in so the staged tree is a runnable repository layout and
so `provider_pins` is real. **None of these is a deliverable of this task**; each
is byte-identical to its source and must come from that source at publication:

| Staged path | Source | sha256 |
|---|---|---|
| `src/creib/**`, `src/deepreason_core/**`, `src/minireason/**` (less the two below), `tools/multicycle_language_probe.py`, `docs/sources/FW5-explanatory-construction.md` | `/home/user/miniReason` | unchanged |
| `src/minireason/provider_openai_compat.py` | the concurrent provider staging tree | `cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db` |
| `src/minireason/data/endpoints.json` | the concurrent provider staging tree | `03eff16b8f575c113871a1266439874b2622a75d200ecb84a1b79464aa98aee7` |

The staged `src/minireason/graph_import_h005.py` is byte-identical to the
published importer (`e5bd327a…`); a test asserts that equality by hash, so the
end-to-end proof below is against the published importer, not a copy that has
drifted.

**Both of those moved under this fork during the session, and both were
re-synced and re-proved rather than pinned to a stale copy.** The provider
module went `3cbdd566…` → `cdc4b571…` (it now refuses a DeepSeek call whose
reasoning presence disagrees with the thinking control — see §3.8), and the
owner's importer went `fc9f4a76…` → `e5bd327a…` as `/home/user/miniReason`
advanced from HEAD `8a99d3fb` through several commits (`d0e5d343` at the final
run); those importer bytes are committed there, and the staged copy is
byte-identical to them. The suite below was run against those current bytes. Nothing in `/home/user/miniReason` was modified by this work
(the staged tree only ever reads it), and the drift is why the equality is a
test rather than a sentence: if either source moves again, the suite says so.

Run:

```
cd <staging>
python3 -m unittest discover -s tests
```

---

## 1. Provenance header and what "fork" means here

The fork's module docstring opens with

> Forked from tools/multicycle_commitment_study.py at
> `9b8463bb33cbca131e050763720c12a0f68ffdad07cb4e25df666e17400d2a72` under this
> session; differences listed below.

and then lists (a)–(k). Every difference is marked `# MULTI:` at the point of
change. Of the owner's 41 module-level definitions, **41 are present, 0 removed**:
16 are byte-identical, 25 changed. 35 definitions are new (76 in the fork).

That census is no longer prose: `test_every_changed_definition_carries_a_multi_marker`
re-derives it from the AST of both files on every run, pins the sixteen
byte-identical names and the count of changed ones, and **fails if any changed
definition carries no `# MULTI` marker** — the claim in the header is checked,
not asserted.

**Byte-identical (16):** `sha`, `encoded`, `load`, `utc`, `identifier`,
`safe_source`, `kind`, `projection_id`, `manifest_for`, `runtime_pins`,
`problem_for`, `coordinate`, `label`, `provider_dir`, `wave_path`, `git`.

That list is the point of the fork: manifest compilation, the projection id
scheme, the coordinate label, the runtime pin rule and the canonical encoding
are the things the published importer reads, and none of them moved.

## 2. The diff, function by function

### Unchanged in behaviour, changed only by a comment

* **`project`** — two comment lines added. The projected view text is what the
  importer's brief/label index is read against; not one character of output
  changed.

### (a) Arms are a per-occurrence declaration, not a module constant

* **module constants** — `ARMS`/`BASELINE_ARMS` become `SURFACES`, `KINDS`,
  `BASELINE_KINDS` and `ARM_COMPONENT`. `CAP`, `VIEWS`, `ID`, `ENVELOPE`,
  `PUBLIC_CONTRACT` are unchanged.
* **`canonical_arm`** *(new)* — folds `@`→`__` and `:`/`/`/`.`/space→`_`, then
  requires `[A-Za-z0-9][A-Za-z0-9_-]{0,63}`. A declaration may be written
  `mini_fcl@ollama/gpt-oss-120b`; the coordinate component becomes
  `mini_fcl__ollama_gpt-oss-120b` and the declared spelling is kept in the plan
  as `declared_name`, which is itself validated as printable non-empty text that
  folds to the arm it names (`ARM_DECLARED_NAME`) — it is frozen into the plan
  and hashed into `arms_sha256`, so it is checked like every other arm field.
  The stricter-of-the-two rule exists because the published importer
  re-validates every coordinate component against
  `graph_import_h005._SAFE_COMPONENT` = `^[A-Za-z0-9_-]+$`, which — unlike the
  owner's `ID` — rejects a dot. A name this runner accepts can never be refused
  downstream after the calls are spent. **Where that rule actually bites is
  `at()`**, not `canonical_arm`: by the time `canonical_arm` matches, the one
  character the two regexes disagree about (`.`) has already been folded to
  `_`, so the check there is a post-fold assertion. In `at()` the arm arrives
  from a coordinate that was never folded, and the strictness is load-bearing.
* **`validate_arms`, `read_arms`, `arm_spec`, `is_baseline`** *(new)* — freeze
  `arm -> {surface, kind, endpoint, declared_name, mode, max_tokens, seed}`
  against the endpoint registry. Refusals: `ARM_NAME_NOT_IMPORT_SAFE`,
  `ARM_NAME_COLLISION`, `ARM_FIELDS`, `ARM_SURFACE_OR_KIND`,
  `ARM_BASELINE_SURFACE`, `UNKNOWN_ENDPOINT`, `ARM_NATIVE_WIRE_UNKNOWN`,
  `ARM_CEILING`, `ARM_SEED`, `ARMS_SCHEMA`, `PROVIDER_MODE`.
* **`endpoints`, `set_registry`, `provider_module`, `endpoint_record`,
  `provider_kind`** *(new)* — the registry seam. `endpoint_record` is the
  key-free publishable record; endpoint names and families are registry labels
  (`ollama/gpt-oss-120b`), so they are checked for printable non-empty text and
  nothing more — only arm names are path components.
* **`EndpointSettings`** *(new)*, replacing the imported DeepSeek-locked
  `Settings`. `to_dict()` reproduces
  `provider_openai_compat._RecordedCaller._settings_view` for the call, field
  for field, because that dict is what the provider records and what
  `decode_contribution` compares the record against.
* **`settings_for(arm, arms, registry=None)`** — signature gains the arm
  mapping. Thinking is `None` on every family but `deepseek`; a `native` arm
  anywhere else raises `ARM_NATIVE_WIRE_UNKNOWN`.
* **`payload_for(messages, settings)`** — same signature, now mirrors
  `_build_payload` including the Ollama-native `options/num_predict`/`format`
  shape and the optional `temperature`/`seed` keys. On a DeepSeek endpoint the
  produced body is byte-identical to the owner's.
* **`dispatch_kwargs`, `default_provider_factory`** *(new)* — the exact keyword
  call handed to `complete(...)`, and the live factory.
* **`write_new`** — the credential guard reads every `key_env` in the registry
  (plus `DEEPSEEK_API_KEY`, via the new `key_environment_names`) instead of the
  one variable. Same refusal, `CREDENTIAL_IN_OUTPUT`, with one addition: a value
  shorter than `MIN_CREDENTIAL_LENGTH` (16 bytes) is not searched for. The guard
  is an unbounded substring scan, so a one-character placeholder in a key
  variable occurs in almost every record by accident — `DEEPSEEK_API_KEY=x`
  made `initialize` refuse to write a manifest — and the write it would refuse
  might be the receipt that resolves an attempt already spent. For the same
  reason the final receipt write is now guarded: a refusal there is rewritten
  once as a coordinates-and-hashes-only `FAILED` receipt carrying
  `validation_failure_type: RECEIPT_REFUSED`, so no spent call is stranded as a
  permanent `UNRESOLVED_ATTEMPT`.
* **`at`** — the arm is validated for shape (`ARM_COMPONENT`) rather than for
  membership in a module constant; membership is checked wherever the mapping is
  in hand. The problem/node/cycle/category/suffix checks are the owner's.
* **`nodes_for(…, arms)`, `final_coordinate(…, arms)`,
  `source_coordinate(…, arms)`, `arm_stopped(…, arms)`,
  `prepare_wave` (passes `plan['arms']` and `plan['scope']` on),
  `ready_coordinates(…, arms, scope)`, `read_terminal(…, arms=None)`,
  `read_artifact(…, arms=None)`** — one extra parameter each, so the arm's kind
  and endpoint are reachable. `read_terminal` reads the mapping back from the
  occurrence's own frozen `arms.json` when a caller has none.
* **`occurrence_arms`** *(new)* — that read-back.
* **`key_environment_names`** *(new)* — the `key_env` vocabulary the credential
  guard in `write_new` compares against (below).
* **the registry seam** — `set_registry` is the *only* one. An earlier draft
  also threaded a `registry=` keyword through `settings_for`, `read_arms`,
  `initialize`, `verify`, `plan_body`, `read_terminal`, `read_artifact` and
  `send_wave`, but `render_node`, `ready_coordinates` and `wave_capacity` never
  took it and always resolved the global — so a caller who passed one would have
  had a wave built against one registry compared with settings built against
  another, and spent the calls before finding out. The keyword is gone; every
  function resolves through `endpoints()`. `validate_arms(declared, registry,
  mode)` keeps its explicit, *required* registry argument because it is the
  function that freezes the mapping. A test asserts that no public function
  takes a `registry` parameter and that a narrowed registry refuses everywhere
  at once.
* **`render_node`** — signature unchanged. `arm in BASELINE_ARMS` becomes
  `spec['kind'] in BASELINE_KINDS`; `arm.startswith('mini_')` becomes
  `spec['kind'] == 'mini'`; `arm == 'mini_fcl'` (policy text) becomes
  `spec['surface'] == 'fcl'`. The rendered brief, the trace record and the
  request record are otherwise character-for-character the owner's.
* **`audit`** — iterates the arm mapping; each invocation row gains `endpoint`.
* **`validate_material`** — accepts an optional `study_id` and validates its
  shape. Every other rule is the owner's.

### (b) Per-key concurrency — two lines, both of which can bind

* **`arm_key_env`, `key_caps`, `key_cap`, `wave_capacity`** *(new)*. Every
  endpoint names a credential (`endpoint_record` and
  `EndpointSettings.__post_init__` both refuse an empty `key_env`), so there is
  no unkeyed group and none is invented. `key_cap` is `min(5,
  endpoint.max_concurrency)` over the endpoints on that credential: five is the
  owner's authorisation and an endpoint may ask for less, never more, so
  `plan.json` cannot state a ceiling wider than the transport will take.
* **`ready_coordinates`** — *the first line.* The round-robin over per-arm
  queues and the per-arm fairness are the owner's; the single ceiling of five
  becomes `key_cap` per `key_env`, so a wave holds up to the sum of the caps and
  never more than `key_cap` that spend one credential. A `progressed` guard
  replaces the owner's `any(queues)`-only loop, which could not terminate once a
  key is saturated.
* **`send_wave`** — re-refuses a wave carrying more than `key_cap` on one
  credential (`WAVE_SIZE_INVALID`), before any attempt marker or provider
  object exists, and then holds every in-flight call under the gate below.
  `max_workers` is one thread per coordinate; the gate, not the pool, is the
  ceiling.
* **`key_gate`, `_reset_gates`** *(new)* — *the second line, and the one this
  fork got wrong at first.* The gate is a **module-level registry keyed by
  `key_env`**, memoised, mirroring `provider_openai_compat.slots_for` including
  its refusal to change a ceiling already in force
  (`CONCURRENCY_LIMIT_CONFLICT`). A semaphore built inside one `send_wave` call
  — which is what this file had — could never block: wave construction has
  already held that call to `key_cap`, so at most `key_cap` threads ever
  contend for a semaphore of `key_cap`. It was dead code, and NOTES said it was
  a second enforcement. Process-wide, it is: two `send_wave` calls on one
  credential now share one semaphore, so they are five in flight *between* them.
  The gate is acquired **before** the attempt marker is written, so an attempt
  only ever exists for a call this process is about to make.
* **`pending_wave`, `send_round`** *(new)* — one round over several
  occurrences: each occurrence's prepared wave, sent concurrently against one
  published commit, under the shared gate. Nothing is relaxed — each occurrence
  still runs its own publication check, wave validation and `NO_REPLAY` refusal.
  `main` gains the `send-round` operation and `--occurrences`.

Three mutants that used to leave the suite green now fail: widening the per-key
admission in `ready_coordinates`, deleting the per-key half of
`WAVE_SIZE_INVALID`, and removing or per-wave-scoping the gate.

### (c) Configurable publication ref

* **`upstream_ref`, `split_publish_ref`** *(new)* — default is
  `git rev-parse --abbrev-ref --symbolic-full-name @{u}`; an unresolvable
  upstream is `PUBLISH_REF_UNRESOLVED`, a malformed ref `PUBLISH_REF_INVALID`.
* **`check_published(repo, output, wave, publish_ref=None)`** — `origin` /
  `refs/heads/main` were hardcoded; they are now derived from the ref. The
  error is `PUBLISH_REF_CHANGED` in place of `REMOTE_MAIN_CHANGED`. The
  byte-comparison loop over `required_paths` is unchanged.

### (d) Study id and occurrence root are parameters

* **`study_paths`** *(new)* and **`main`** — `--study`, `--arms`,
  `--publish-ref`; `--output` defaults to `<study>/occurrence-01`, `--material`
  to `<study>/material.json`, `--arms` to `<occurrence>/arms.json` when present
  and otherwise `<study>/arms.json`. `initialize` refuses when the material's
  `study_id` disagrees with the study directory (`STUDY_ID_MISMATCH`). The key
  prompt is now per `key_env` (`PROVIDER_KEY_INPUT=prompt`) and every prompted
  variable is popped in the `finally`.
* **`initialize`** — takes `arms_path`; the occurrence may pre-exist with
  `material.json` and/or `arms.json` and nothing else; both are frozen
  write-once and compared byte-for-byte if already present.
* **`verify`** — re-reads `arms.json` from the occurrence and recomputes the
  whole plan from it, so a tampered arm declaration is `IMMUTABLE_PLAN_MISMATCH`.

### (e) Plan fields

`plan.json` gains `arms` (the mapping), `arms_sha256`, `runner_sha256`,
`study_id`, `providers` (key-free endpoint records), `provider_pins`
(module + registry sha256, null when absent), `provider_mode`, `scope`,
`ceilings` (per-arm `max_tokens`/`timeout_seconds`/`seed`),
`envelope_repairs_declared`, `max_concurrent_requests_per_key_env` (a mapping
`key_env -> cap`, not a scalar), `max_concurrent_requests_total` (their sum),
`max_calls_envelope` and `key_environment_names`. `provider_mode` is now the
single declared mode and **raises `PROVIDER_MODE_MIXED`** on a mixed set: the
earlier `sorted(...)[0]` would have reported a mixed occurrence as `live`,
which is the wrong answer in the one direction that matters. `helper_sha256` is kept and equals `runner_sha256` by
construction (the fork *is* the helper); a test pins that. `runtime_pins` keeps
the owner's membership rule untouched — the new provider module is pinned under
`provider_pins`, not folded into it.

* **`plan_body`** — the owner's closed-form `max_calls` (`2 + 3 * nodes`, which
  assumed two baseline and three multi-call arms) becomes a sum over the arms
  actually declared. On the H005 five it still returns 240.
* **`provider_pins`** *(new)*; **`required_paths`** adds `arms.json` and the two
  pinned provider files, so `check_published` byte-compares them too.
* **`send_wave`** refuses a live occurrence whose provider module is unpinned
  (`PROVIDER_MODULE_UNPINNED`) and checks `KEY_MISSING` per key group.

### (g) The declared `envelope_unwrap` decode step — from the live smoke

Ollama cloud accepts `response_format: json_object` without enforcing it.
`strip_one_fence`, `parse_envelope`, `envelope_unwrap` *(new)* run **two
declared repairs and no others** before the owner's strict shape check: strip
one outer Markdown fence when the whole trimmed content is a single fenced
block, then re-parse with `strict=False`.

* `decode_contribution` returns two extra keys, `envelope_repairs` and
  `strict_parse_would_succeed`, and is otherwise the owner's function: same
  custody checks, same duplicate-key hook, same exact-two-string-fields shape
  test, same OPAQUE fallback to the raw text with an empty commitments string,
  same sha256s over the raw content. **The decoder is not "improved": an
  envelope that no declared repair rescues is still OPAQUE and is never
  repaired.**
* `authored_artifact` filters those two keys out, so the artifact record keeps
  exactly the owner's field set and the importer reads it unchanged.
* `send_wave` writes them into the receipt; `read_terminal` re-derives and
  compares them (`ARTIFACT_CUSTODY_MISMATCH` if a receipt is edited).
* `audit` counts `strict_parse_would_succeed`, `fence_stripped`,
  `lenient_control_chars`.
* **Consequence, stated in PLAN.md:** a fork occurrence's OPAQUE rate is not
  comparable with H005 occurrence-01; `strict_parse_would_succeed` is.

### (h) Per-arm ceilings and seeds — and a timeout that is not one

`max_tokens` and `seed` are per-arm declarations (`ARM_OPTIONAL`), surfaced in
`plan['ceilings']`. **`timeout_seconds` is not a per-arm declaration**: it is
surfaced in `plan['ceilings']` beside them but read from the endpoint record,
it is not in `ARM_OPTIONAL`, and an arm that tries to declare one is
`ARM_FIELDS`. All three arms of occurrence-02 show 180 because that is the
endpoint's value, not because they asked for it. `decode_contribution` checks
`settings.max_tokens` rather than the module `CAP` (identical while every arm is
at 8192).
`finish_reason` and `usage` were already recorded per node and still are, so a
ceiling-truncated call is visible as `INCOMPLETE_GENERATION` / PARTIAL, treated
exactly as the owner treats it: preserved, usable, never retried, never
relabelled.

### (i) Reasoning on families with no thinking control

The owner refuses a record with `reasoning_content_present` when
`settings.thinking` is falsy. Every Ollama family except `gemma4:31b` emits
reasoning by default and offers no switch through this surface, so under that
rule every such node would be `FAILED`. The fork narrows the refusal to
`settings.thinking is False` — i.e. to a family where the runner actually set a
thinking control and set it to disabled, which today is DeepSeek only — and
**records** `reasoning_content_present` in the receipt otherwise.
`reasoning_content_persisted` stays a hard refusal everywhere.

### (j) The declared scope

`arms.json` may carry `"scope": {"problems": [...], "cycles": [...]}`, validated
by **`validate_scope`** *(new)*, frozen into `plan['scope']` and pinned by
`arms_sha256`. **`in_scope`, `call_count`** *(new)*: `ready_coordinates` — and
therefore `prepare-wave` and `send-wave` — refuses any other problem or cycle
with `SCOPE_EXCLUDED`; `plan['max_calls']` counts only what the scope admits, so
it *is* the authorisation, while `plan['max_calls_envelope']` keeps the full
material figure; `audit` reads the same scope and counts anything found outside
it as `out_of_scope`. Without a scope every one of these behaves exactly as
before (`scope: null`, `max_calls == max_calls_envelope`), so the owner's
semantics are unchanged where no scope is declared.

F001 uses it: all six occurrences declare `{"problems": ["daily"], "cycles":
[1]}`, and the plans then authorise 12 calls (occurrence-01, which carries the
`native` arm) and 11 each (occurrences 02–06) — 67 in all. A test builds all six
plans from the staged `arms.json` files and pins those numbers.

### (k) The failure code

`send_wave` records `failure_code` beside `failure_type` in every receipt: the
transport's own `ProviderFailure.code`. `failure_type` alone collapses
`HTTP_429`, `KEY_MISSING`, `TRANSPORT_OR_RESPONSE_ERROR` and
`THINKING_MODE_MISMATCH` into the single string `ProviderFailure`, and the code
then survives only inside `call-0001.response.json`. This matters because of
what one failure costs: `arm_stopped` scans cycles 1..N, so **one FAILED node
ends that arm for the rest of the occurrence** and the next `prepare-wave`
simply returns fewer coordinates without refusing anything. PLAN.md names the
audit signal (`FAILED` ≥ 1 with `unvisited` > 0 and a `"complete": false`
invocation row); a test drives a 429 and a KEY_MISSING through the fixture and
pins both the codes and the truncation.

---

## 3. Assumptions about the provider API

The module was delivered mid-task, so the fork codes against the real
`minireason.provider_openai_compat` and the earlier adapter TODOs are gone. What
remains assumed, and what would break if it changed:

1. **`Endpoint` carries exactly `ENDPOINT_FIELDS`.** `endpoint_record` refuses
   a missing one (`ENDPOINT_FIELD_MISSING`) rather than defaulting it, because a
   defaulted `key_env` would silently merge two credentials into one
   concurrency group.
2. **`complete(...)` writes `call-0001.request.json` and
   `call-0001.response.json` under `records_dir`, write-once, containing
   `request`, `request_sha256`, `settings`, `coordinate`, `content`, `usage`,
   `finish_reason`, `returned_model`, `status`, both reasoning flags and
   `credential_redaction`.** Verified by reading the module; exercised on every
   offline call, since the tests drive the module's own `OfflineProvider`.
   Extra fields it adds (`schema_version: minireason.call.v2`, `call_number`,
   `url`, `request_bytes_sha256`, `endpoint`, `started_at`, `elapsed_ms`, …) are
   ignored by every H005 check and by the importer.
3. **`payload_for` must equal `_build_payload`, and `EndpointSettings.to_dict()`
   must equal `_settings_view`.** These are two independent reimplementations of
   the same two dictionaries, and `decode_contribution` /
   `read_terminal` compare them on every node: a divergence is
   `PROVIDER_REQUEST_CUSTODY`, loudly, on the first call. That is deliberate —
   the runner declares the bytes in `requests/<coord>.json` before publication
   and the provider records the bytes it actually sent, and the study is only
   worth anything if those agree. **If the module's payload or settings view
   changes, `payload_for` and `EndpointSettings.to_dict()` are the only two
   places to change**, and the offline suite fails immediately if they are not.
4. **`thinking=` is accepted only for `family == "deepseek"`** (the module raises
   otherwise). This is why a `native` arm is refused at plan time on every other
   family, rather than guessed at dispatch time.
5. **Per-key semaphores of five are process-wide and shared across instances**
   (`slots_for`). The fork's own gate is now the same shape for the same reason
   (§2(b)), and the two are complementary rather than redundant: `slots_for`
   guards the socket, the fork's gate guards the *attempt marker* — the record
   that a coordinate was spent — which is written before the provider object is
   ever constructed. Where the fork's gate binds and the provider's cannot: two
   `send_wave` calls on one credential, which without it would write up to
   twice the authorised number of attempt markers while the wire stayed at five,
   so a crash in that window would leave coordinates permanently
   `UNRESOLVED_ATTEMPT` on calls that never went out. Both are *process*
   ceilings: nothing here holds a ceiling across processes, so PLAN.md
   authorises one runner process per credential — but that one process may now
   drive all six occurrences (`send-round`), which is what the earlier
   "one Ollama occurrence at a time" rule was standing in for.
6. **`OfflineProvider(endpoint, records_dir, script)`** shares the constructor
   and the `complete(...)` contract, and stamps `kind: "offline-scripted"` plus
   `offline: true` on the recorded settings. The fork models that as a declared
   occurrence-level `provider` mode (`live` | `offline`) in `arms.json`, frozen
   into `plan['provider_mode']`, so an occurrence's records say which transport
   actually ran.
7. **`seed` is honoured on Ollama and absent on DeepSeek.** Encoded as a per-arm
   declaration rather than a constant; the F001 arms set `seed: 7` on every
   Ollama arm and leave it null on DeepSeek.
8. **A DeepSeek call whose reasoning presence disagrees with the thinking
   control is not usable** (`THINKING_MODE_MISMATCH`), a rule the provider
   module added during this session and the fork now depends on: it is the only
   evidence that the control was honoured. Consequence for F001: the `native`
   arm on occurrence-01 must come back with reasoning present or the node is
   `FAILED` — a native arm that silently ran without reasoning is a refusal, not
   a mislabelled COMPLETE. The offline fixture scripts reasoning presence to
   match the control for the same reason; scripting otherwise would be scripting
   a response the wire cannot produce.

One assumption is **not** the provider's and is worth repeating: the published
importer's `FCL_SURFACE_ARMS == ("mini_fcl",)` is exact membership, so an arm
name carrying its endpoint is read as a prose arm. F001 keeps canonical arm
names and puts the family in the occurrence; a test pins the constant so the
coupling cannot rot unnoticed.

---

## 4. Offline test summary

```
$ cd <staging> && python3 -m unittest discover -s tests
Ran 69 tests in 13.3s — OK (0 failures, 0 errors, 0 skips; no socket opened)
```

(With `PYTHONPATH=<staging>/src:<provider staging>/src:/home/user/miniReason/src`,
against the current provider module `cdc4b571…` and the current published
importer `e5bd327a…`.)

Every call in the suite goes through `provider_openai_compat.OfflineProvider`,
subclassed only to script the answer and to count concurrency, so the request
bodies, the recorded settings view and the write-once record layout under test
are the real transport's.

**The owner's sixteen, ported (16).** Material custody and occurrence
no-clobber (extended to `arms.json`); invalid graphs, references and cycle
counts refused (plus a bad `study_id`); a cycle is a whole template invocation
with distinct node coordinates; body / commitments / both views separate and
bound to parent bytes; settings and envelopes explicit for every arm; a failed
publication starts no provider and no attempt; five independent ready calls
overlap and cannot be replayed; request tampering refused before provider
construction; a pending attempt marker is a no-retry boundary; a provider
coordinate mismatch fails usability and preserves the exact raw text; required
publication paths include transitive provider and artifact bytes; publication
checks actual bytes without Git mutation; partial delivery usable without retry
or relabelling; a mutated parent artifact refused before dependent rendering;
decode preserves authored fields, opaque text and a valid partial envelope;
decode refuses custody, delivery and hidden-reasoning mismatches.

Two ports differ in shape, and only these two:

* the coordinate-mismatch test exercises *both records wrong* and
  *response record wrong* instead of *request* and *response*: the real provider
  writes one coordinate into both records, so a request-only corruption is not
  reachable without rewriting a record the transport owns. Both branches of the
  runner's check are still exercised.
* the settings/envelope test asserts the thinking block for the DeepSeek family
  and its absence elsewhere, since that is now family-gated.

**Fork-only (53).**

* *Per-key concurrency, wave construction (6)* — two keys reach ten in flight and
  never exceed five per key (a `Barrier(10)` clears, and per-key peaks are
  exactly 5/5); one key is never widened past five; an oversized wave is refused
  before any call; **more than five ready on one key is truncated to five while
  the wave as a whole stays under capacity** (seven arms on one credential and
  three on the other: the wave is 5+3, and the two held back run in a later wave
  with every node still delivered); **a hand-edited wave carrying six on one
  credential and four on the other — ten in total, within capacity — is
  `WAVE_SIZE_INVALID` with zero calls**; an endpoint declaring
  `max_concurrency: 2` narrows its own key's cap in `key_caps`, in the plan and
  in the wave.
* *Per-key concurrency, the process-wide gate (4)* — `key_gate` is one memoised
  registry keyed by `key_env` and refuses a changed ceiling
  (`CONCURRENCY_LIMIT_CONFLICT`); **two concurrent `send_wave` calls on ONE
  credential never exceed five in flight** (the fixture holds the first five
  open, and the settle window shows five active, five attempt markers and five
  calls — with a per-wave gate all ten would have been admitted); two concurrent
  `send_wave` calls on TWO credentials reach ten (`Barrier(10)` clears);
  `send_round` sends several occurrences against one commit, reports an
  occurrence with no prepared wave, replays nothing on a second round and
  refuses a repeated occurrence.
* *Wave safety invariants (3)* — a prepared wave that was not sent blocks the
  next prepare (`PREPARED_WAVE_PENDING`); an attempt with no receipt stops the
  arm (`UNRESOLVED_ATTEMPT`) and shows in the audit; a wave whose coordinates
  drifted from the dependency frontier is refused
  (`WAVE_NOT_DEPENDENCY_READY`). All three with zero provider calls and zero
  provider constructions.
* *The registry seam (2)* — no public function takes a `registry` parameter, and
  a narrowed registry refuses in `settings_for`, `key_caps`, `wave_capacity`,
  `verify`, `render_node`, `prepare_wave` and `audit` alike.
* *Failure codes and arm truncation (1)* — a `ProviderFailure("HTTP_429")` and a
  `ProviderFailure("KEY_MISSING")` are recorded as `failure_code` beside
  `failure_type`, and the failed arms appear in no later wave; the audit shows
  `FAILED` 4, `unvisited` 48 and `"complete": false` on both arms.
* *Scope (2)* — a declared scope bounds `max_calls` (17 of the fixture's 60),
  refuses every other cycle (`SCOPE_EXCLUDED`, including a hand-written wave
  file naming one), and drains to `unvisited` 0 / `out_of_scope` 0; eight
  malformed scopes and an unknown problem are refused.
* *The F001 register itself (2)* — all six plans are built from the staged
  `arms.json` files: scope `{daily, cycle 1}` each, per-arm call counts
  `bare 1 (+ native 1 on 01) + mini_fcl 5 + mini_prose 5`, `max_calls` 12/11,
  `max_calls_envelope` 168/156, one credential each, **67 calls in all**; and
  `native` is declared exactly on the family whose wire carries a thinking
  control and refused (`ARM_NATIVE_WIRE_UNKNOWN`) on the five that do not.
* *Fork hygiene (8)* — the AST census and the `# MULTI` marker claim; a
  credential too short to be one is not a leak, and a refused receipt never
  strands a spent attempt; `declared_name` must fold to the arm it names; a
  mixed provider mode is refused, not reduced; the timeout is the endpoint's and
  no arm may declare one; every endpoint names a credential, so the "unkeyed
  group" the old docstring described cannot exist; and the `ARM_COMPONENT` rule
  bites in `at()`, where an arm is unfolded, not in `canonical_arm`.
* *Publication ref (3)* — the default is the branch's upstream and never
  `refs/heads/main`, an explicit `--publish-ref` overrides it, a moved ref is
  `PUBLISH_REF_CHANGED`, one changed byte is `INPUT_NOT_PUBLISHED`; ref
  spellings validated; an unresolvable upstream is a refusal, not a guess.
* *Arm declaration (6)* — a native arm refused on every family with no thinking
  wire and accepted on DeepSeek; unknown endpoints, surfaces, kinds, baseline
  surfaces, ceilings and seeds refused; arm names canonicalised to what the
  importer accepts, with `declared_name` preserved; the `FCL_SURFACE_ARMS`
  coupling pinned; per-arm ceilings and seeds reach the plan and the wire, and
  no credential value reaches any record; and a DeepSeek arm's request body is
  byte-identical to the owner's runner's — thinking disabled and enabled both —
  while the fork's generalised `max_calls` sum still returns the owner's 240
  over the H005 material and five arms.
* *Envelope unwrap (8)* — a single outer fence stripped and recorded; raw
  control characters parsed leniently; both repairs together; **nothing else
  repaired** (seven negative cases, each still OPAQUE with the raw text as body
  and an empty commitments string); **the two H005 records PLAN.md cites for the
  control-character repair are read from the owner's own occurrence-01, checked
  by sha256, and shown to fail strictly, to be rescued by exactly
  `lenient_control_chars`, and to be recorded OPAQUE in the owner's frozen
  receipts** — the register's citation is executable, not decorative; a clean
  envelope records no repair;
  repairs are receipt-level and never reach the artifact record while the raw
  fenced text stays on disk; a tampered repair record fails terminal custody;
  reasoning without a thinking control is recorded, not refused, while a
  DeepSeek arm asked for thinking-disabled still refuses.
* *End-to-end (8)* — **the byte-compatibility proof.**

### The end-to-end test

A synthetic occurrence over H005's material verbatim + `study_id`, `daily`
problem, cycle 1 (`fork5`), two arms on two endpoints with two credentials
(`mini_fcl` on `deepseek-flash`, `mini_prose` on `ollama/gpt-oss-120b`, the
latter seeded), driven through `prepare_wave`/`send_wave` until no coordinate
remains — four waves, ten calls, all five nodes on both arms — and then handed
to `minireason.graph_import_h005.import_occurrence`.

The importer under test is asserted byte-identical to
`/home/user/miniReason/src/minireason/graph_import_h005.py`. It reports:

* **custody verified on every node.** Every declared check has `ran == total`
  with an empty skip list, except `projection_source`, whose only four skips are
  the first invocation's structurally absent `previous`/`origin` slots — the
  same skips the owner's occurrence-01 produces.
* **labels produced:** 18 artifacts, `daily/mini_fcl/…/account` **refuted**,
  `…/response` **refuted**, `nu:response#k1->rival` **refuted**, the rest
  accepted or suspended_unsupported; `daily/mini_prose/…/account` accepted
  (accept-by-position — a prose surface is never parsed, so no warrant can
  arise).
* **FCL-1 read on the fcl arm and not on the prose arm:** 5 `read_fcl1`,
  5 `prose_not_parsed`, 0 `parse_failure`, 0 `schema_failure`,
  5 `prose_commitment_surface`.
* **references resolve:** `{"refs": 12, "resolved": 12, "extensions": 0,
  "dangling": 0, "task": 0}`.
* **the mechanism facts the study exists to compare are all live:**
  3 warrants, `att` = {objection→account, response→rival, carry→ν(W_k1),
  carry→response (the validity-node closure)}, `depends_cross_document` 2,
  `criticism_of_criticism_retargeted` 1, `validity_node_minted_unasserted` 3,
  and a reinstatement path through the closure.
* **the fork's extra receipt fields do not disturb the import**
  (`envelope_repairs`, `strict_parse_would_succeed`,
  `reasoning_content_present` and `failure_code` are all present in the receipts
  and all ignored by the importer, which reads receipts with `.get`), and a
  second import of the same bytes produces identical labels and event count.
* **one error-severity residue fires, and it is the fixture's, not the
  layout's.** The published CLI prints, above the label table,
  `ERROR-SEVERITY RESIDUE FIRED: ref_through_unexposed_view (1) -- read the
  residue before reading any label.` It is there because the scripted `rival`
  document depends on `p.rival.0#c1`, a commitment-surface record reached
  through a projection the brief exposed as **body** only — a property of the
  test's FCL-1 content, not of the fork's record layout, and the import still
  exits 0 with `ref_unresolved` 0, `parse_failure` 0 and custody verified on
  every node. A test pins the count, so the summary above cannot go on quoting
  the importer selectively.

That is the claim "byte-compatible with the published importer" discharged by
execution rather than by inspection.

### What the offline suite does not show

It opens no socket, so nothing here is evidence about any model's behaviour, and
the scripted answers are the test's, not a provider's. It exercises two
endpoints (three where a narrowed `max_concurrency` is under test), not
twenty-four. The live per-key semaphore sharing across provider instances is the
provider module's own tested property; what is tested here is the fork's own
gate, which is the one that guards the attempt marker. No test drives two
runner *processes*: nothing in this repository can hold a ceiling across
processes, which is why PLAN.md authorises one. And
no part of this task ran anything live: `git status` on
`/home/user/miniReason` is empty, and the only `send-wave` invoked outside the
tests refused at the publication check with no attempt written.
