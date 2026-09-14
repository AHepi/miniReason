> Published verbatim, body unedited: this document was written against the staging tree, so `NOTES.md`, `FIXES.md` and the staged `src`/`tests`/`tools` paths it names are that scratchpad tree and not any path in this repository, where the files it describes are `src/minireason/provider_openai_compat.py`, `src/minireason/data/endpoints.json`, `tools/provider_smoke.py`, `tests/test_provider_openai_compat.py`, `docs/workflows/provider-openai-compat.md` and `docs/sources/provider-openai-compat-smoke-notes-2026-09-14.md`.

# Review closure — multi-endpoint transport (staging)

Every finding of the four-lens review of this tree, at every severity, with the
change that closes it and the test that pins it. Nothing here was applied to
`/home/user/miniReason`; this is a staging tree and the repository is untouched
(`git status --porcelain` empty at `8a99d3f`).

**Tests.** `env -u DEEPSEEK_API_KEY -u OLLAMA_API_KEY PYTHONPATH=$P/src python3
-m unittest tests.test_provider_openai_compat` → **Ran 91 tests, OK** (was 59;
the 59 are still there and still green, one fixture adjusted — see 2.2). No
socket is opened, no provider is contacted, every credential in the suite is a
synthetic sentinel, and `/home/user/miniReason/.env` was never read.

Lens 1 is credential discipline; lens 2 is correctness and record fidelity.

---

## Lens 1 — credential discipline

### 1.1 (medium) `SECRET_IN_REQUEST` attaches an unredacted record

*Finding:* the refusal raised `ProviderFailure(..., record=record)` where
`record["request"]` is, by definition, the payload that carried the credential.
The disk copy was redacted; the exception attribute was not.

*Change:* `ProviderFailure.__init__` now redacts whatever record it is handed
(`_redacted_record`, a JSON round-trip through `redact`). Done at the exception
rather than at each raise site, so no future raise site can reintroduce the
exposure. `provider_openai_compat.py`, `ProviderFailure`,
`_refuse_credential_in_request`.

*Pinned by:* `FailureRecordTests.test_secret_in_request_failure_record_carries_no_key_fragment`
— asserts the payload is still on the record (it carries `[REDACTED_CREDENTIAL]`)
and that no 6-, 12- or full-length fragment of either sentinel key appears in
`json.dumps(failure.record)` or in `str(failure)`.

### 1.2 (medium) `list_models` CREDENTIAL_ECHO attaches the raw model body

*Finding:* `models=body` is the one raw provider body a record keeps; on the
echo branch it reached the exception verbatim.

*Change:* the same `ProviderFailure` redaction covers it; `list_models`'
docstring now states the carve-out and that the attached record is redacted like
the one on disk. `docs/workflows/provider-openai-compat.md` "What is never
recorded" carves out the model list explicitly instead of claiming the raw body
is never stored.

*Pinned by:* `FailureRecordTests.test_list_models_credential_echo_failure_record_carries_no_key_fragment`
(both the exception and `failure.record["models"]["leaked"] == REDACTION`) and
`.test_chat_credential_echo_failure_record_carries_no_key_fragment` (the other
path), plus `ListModelsTests.test_an_echoed_credential_in_a_model_list_is_a_loud_failure`
for the on-disk record.

### 1.3 (low) a JSON-escaped key would survive redaction

*Change:* `_renderings(secret)` returns the raw value and `json.dumps(secret)[1:-1]`,
and `redact_with_names` replaces both, escaped form first.

*Pinned by:* `RedactionScopeTests.test_a_json_escaped_key_is_redacted_too` —
uses a key containing `"` and `\`, asserts the fixture really is escaped by
`json.dumps`, and asserts the round-trip value is the redaction marker.

### 1.4 (low) the 8-character redaction floor was undocumented

*Change:* stated in the module docstring, on `_MIN_SECRET_LENGTH` itself, and in
the redaction row of `docs/workflows/provider-openai-compat.md` — including what
the floor means (not redacted, not echo-checked, not a refusal).

*Pinned by:* `RedactionScopeTests.test_a_value_under_the_documented_floor_is_not_a_secret`.

### 1.5 (low) `load_env_file` loads names the redaction set does not cover

*Change:* the suffix scan of `os.environ` is gone (see 2.6). The set is now the
registry's `key_env` values, `_ALWAYS_SECRET_ENVS`, and whatever a caller
declares through the new `register_secret_envs(names)`;
`tools/provider_smoke.py:load_env_file` registers every name it sets.

*Pinned by:* `RecordCollisionTests.test_the_smoke_tool_registers_the_names_its_env_file_loaded`
— an env file declaring `OLLAMA_TOKEN` (outside the old convention) puts that
name in the secret set and its value gets redacted.

---

## Lens 2 — correctness and record fidelity

### 2.1 (high) `--headroom` always crashed, after the calls were spent

*Finding:* `probe()` built a second provider into the records directory the
first probe used; every provider restarts at `call-0001`, so `write_new`'s `"x"`
mode raised a bare `FileExistsError` that escaped every `except ProviderFailure`
and lost `smoke-summary.json`.

*Change (two):* `records_dir_for(root, endpoint, label)` gives every probe its
own `<endpoint>/<label>/` directory; and `_open_record` converts a stem
collision into `ProviderFailure("RECORD_EXISTS", ...)`, so no caller that spent
a credential can lose its evidence to an uncaught `OSError`.

*Pinned by:* `RecordCollisionTests.test_a_second_provider_on_one_records_dir_fails_as_a_provider_failure`
and `.test_the_smoke_tool_gives_every_probe_its_own_records_directory`. Also
re-checked out of band: an offline `provider_smoke.main([root, '--only',
'ollama/gpt-oss-120b', '--headroom', '512'])` with `compat._open` mocked now
completes, prints both tables and writes the summary.

### 2.2 (medium) `THINKING_MODE_MISMATCH` was silently absent

*Change:* re-added in `_finish`, after `USAGE_UNAVAILABLE`, exactly as
`provider.py:169-170` does it, with the requested `thinking` threaded in from
both `complete()` implementations: for `family == "deepseek"`, when a thinking
value was sent, `reasoning_present != thinking` fails the call. Added to the
status list in the workflow doc and to NOTES.md's review-closure section.
`COMPLETION_CEILING_VIOLATED` remains absent and remains disclosed.

*Pinned by:* `ThinkingModeTests` — reasoning text with `thinking=False`,
no reasoning text with `thinking=True`, a matching answer is `COMPLETE`, and
the check does not fire where no control was sent.

*One existing test adjusted:* `test_deepseek_thinking_controls_are_sent_for_the_deepseek_family`
sent `thinking=True` against a body with no reasoning text — the exact shape the
restored check fails. Its fixture now carries `reasoning_content`, and the test
additionally asserts that text is not persisted.

### 2.3 (medium) `CompatMiniResponder` changed the DeepSeek arm's default

*Change:* for an endpoint whose `family` is `deepseek`, the responder defaults
`thinking` to `False`, mirroring `provider.Settings.thinking`; documented on the
class and in the workflow doc. Other families are unchanged (no control is sent,
and asking for one is still a `ValueError`).

*Pinned by:* `ThinkingModeTests.test_the_responder_defaults_deepseek_thinking_to_disabled`
(asserts `thinking: {"type": "disabled"}` on the wire) and
`.test_the_responder_sends_no_thinking_control_to_another_family`.

### 2.4 (medium) `extra` overrode module-built payload keys

*Change:* `_validate_call_args` refuses an `extra` key that collides with a key
this module builds (`model`, `messages`, `stream`, `max_tokens`/`format`,
`temperature`, `seed`, `response_format`, `thinking`, `reasoning_effort`) with a
`ValueError` raised before a call number is spent; on a native endpoint
`extra["options"]` is **deep-merged** into the built options instead, so
`options.num_predict` cannot be deleted while `settings.max_tokens` still claims
a ceiling.

*Pinned by:* `ExtraArgumentTests` — collision refusal (and that no call number
was consumed), the deep merge keeping `num_predict` while the record and the
wire agree, a non-mapping `options` refused, and a non-colliding key still
passing through.

### 2.5 (medium) an Ollama prompt-cache hit failed a good answer

*Change:* `_normalise_native` reads a missing `prompt_eval_count` alongside a
present `eval_count` as `prompt_tokens: 0` — Ollama's own semantics for a full
cache hit — and records `usage_source: "native-normalised"` so the count can
never be read as provider-reported. A missing `eval_count` is still
`USAGE_UNAVAILABLE`. `usage_source` is now on every response record
(`"provider-reported"` otherwise) and is documented.

*Pinned by:* `NativeUsageTests` — the cache-hit shape is `COMPLETE` with the
answer intact and `usage_source: "native-normalised"`; a normal body says
`"provider-reported"`; a missing completion count still fails.

### 2.6 (medium) the secret set was a name-shape scan of `os.environ`

*Change:* `_secret_env_names()` is now a declared set — registry `key_env`
values, `_ALWAYS_SECRET_ENVS`, and names registered through
`register_secret_envs` — with the reasoning in its docstring. Separately, every
record that had a credential replaced on the way to disk now names the
environment variables whose values were replaced, under `credentials_redacted`
(`redact_with_names`, `_note_redactions`), so a reader can tell a real hit from
a false positive without seeing either value.

*Pinned by:* `RedactionScopeTests.test_the_secret_set_is_declared_not_discovered_by_name_shape`
(an `INTERNAL_API_KEY` holding an ordinary phrase no longer refuses a prompt or
rewrites content — and does once a caller declares the name),
`.test_redaction_names_the_env_vars_whose_values_it_replaced`, and
`.test_a_record_with_no_credential_in_it_names_none`.

### 2.7 (low) offline skipped the `reasoning_effort` guard the live path performs

*Change:* both checks (and the new `extra` check) live in one
`_RecordedCaller._validate_call_args`, called from both `complete()`
implementations. Documented on `OfflineProvider`.

*Pinned by:* `ExtraArgumentTests.test_offline_and_live_refuse_exactly_the_same_arguments`
— four bad argument sets, each refused by both, with neither spending a call
number and the transport never touched.

### 2.8 (low) `list_models` had zero coverage and stored a provider body

*Change:* tests added (below); the body-storage carve-out is now stated in the
method's docstring and in the workflow doc's "What is never recorded".

*Pinned by:* `ListModelsTests` — `COMPLETE` (asserting the recorded
`request_header_names == ["Accept", "Authorization"]`, the GET URL, the
recorded request stub and coordinate, and that no key survives),
`CREDENTIAL_ECHO`, `HTTP_307` (the redirect-refusal shape, asserting one call
and a redacted detail) and `KEY_MISSING` (recorded before any request).

### 2.9 (low) the offline record described a request it never made

*Change:* `_open_record(..., contacted=False)` for `OfflineProvider`: `url` is
`null`, the destination appears as `not_contacted_url`, `request_header_names`
is `[]`, and the would-be size and digest are `would_send_bytes` /
`would_send_bytes_sha256`. Documented on the class and in the workflow doc.

*Pinned by:* `OfflineRecordShapeTests.test_an_offline_record_names_the_request_it_did_not_make`
(including that the string `Authorization` appears nowhere in it) and
`.test_the_live_record_still_names_the_request_it_did_make`.

### 2.10 (low) five assertions that cannot fail

*Change, item by item:*
(a) `test_endpoints_json_loads_and_every_entry_is_well_formed` is replaced by
`test_endpoints_json_is_well_formed_as_shipped`, which asserts over the **raw
JSON** before `Endpoint.__post_init__` can raise, plus a name-uniqueness check
and a final check that the registry's keys are exactly the shipped names.
(b) `assertGreaterEqual(result.elapsed_ms, 0)` deleted.
(c) the two `reasoning_content_persisted` assertions kept, with comments saying
they pin a documented constant and naming the assertions that verify the
behaviour.
(d) `NoNetworkTests` no longer patches `compat._open`, so the call really goes
through urllib and the connection guard is what stops it; the guard now covers
`http.client.HTTPConnection` as well (a proxy in the environment routes an https
URL through it) and the test asserts the guard was reached, that the failure is
`TRANSPORT_OR_RESPONSE_ERROR`, and that the record says so.

### 2.11 (low) a failure from a normaliser carried `record=None`

*Change:* `complete()`'s `except ProviderFailure` arm attaches the closed record
before re-raising when the exception carries none.

*Pinned by:* `FailureRecordTests.test_a_failure_raised_inside_a_normaliser_still_carries_the_closed_record`
— `choices=[]` now yields a failure whose record carries `status`, `elapsed_ms`
and the same `request_sha256` as the record on disk.

### 2.12 (info) run-03's 12th call cannot be reproduced by the shipped tool

*Change:* NOTES.md's live-smoke paragraph now says the 12th call was the
pre-fix tool's model-list request against the native base (the source of finding
6's `HTTP_307` record), that the shipped tool issues 11, and that a replay one
call short is not a discrepancy. It also notes the new per-probe records layout,
so the paths in the tables are read correctly.

---

## What changed, by file

| file | change |
|---|---|
| `src/minireason/provider_openai_compat.py` | `ProviderFailure` redacts its record; declared secret set + `register_secret_envs`; `redact_with_names` (raw and JSON-escaped) and `credentials_redacted`; `_validate_call_args` (ceiling, effort, `extra` collisions); native `extra["options"]` deep merge; `contacted=False` offline record shape; `RECORD_EXISTS`; `THINKING_MODE_MISMATCH`; `usage_source` and the native cache-hit normalisation; record attached to every re-raised failure; docstring states the redaction floor and scope |
| `tools/provider_smoke.py` | `records_dir_for(root, endpoint, label)`; `load_env_file` registers the names it sets |
| `tests/test_provider_openai_compat.py` | 8 new classes (32 tests); one fixture adjusted; four unfalsifiable assertions replaced or deleted |
| `docs/workflows/provider-openai-compat.md` | redaction row, status list, `extra` rule, offline record shape, `usage_source`, responder defaults, per-probe records dir, model-list carve-out |
| `NOTES.md` | run-03 replay note, records layout, review-closure section |
