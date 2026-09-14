# F001 — one fork5 invocation across six model families

> **Mechanism facts only. Root reads the content.** This study reports what the
> published instruments can *compute* about six occurrences of the same frozen
> material — parse outcomes, reference resolution, edges, labels, counts. It
> reports nothing about whether any criticism was good, whether any dependence
> was real, or whether any amendment repaired anything. No count here ranks a
> family, and invariant I7 of the importer holds throughout: no label it
> computes is a semantic attribution.

Read [the decision ledger](../DECISION_LEDGER.md), [STATUS](../STATUS.md), the
[experiment workflow](experiment.md) and the register itself —
[`experiments/diagnostics/F001-fork5-multifamily/PLAN.md`](../../experiments/diagnostics/F001-fork5-multifamily/PLAN.md)
— before running anything. Where this page is silent, the register governs;
where the register is silent, H005's `PROTOCOL.md` governs.

## What F001 is

One complete `fork5` invocation of the `daily` problem, cycle 1, on H005's
material verbatim (plus one `study_id` key), run once on each of six model
families. Six occurrences, **19 arms, 67 provider calls**:

| Occurrence | Endpoint | Key | Arms | Calls |
|---|---|---|---|---|
| occurrence-01 | `deepseek-flash` | `DEEPSEEK_API_KEY` | `bare`, `native`, `mini_fcl`, `mini_prose` | 12 |
| occurrence-02 | `ollama/gpt-oss-120b` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 11 |
| occurrence-03 | `ollama/qwen3.5-397b` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 11 |
| occurrence-04 | `ollama/glm-5.3` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 11 |
| occurrence-05 | `ollama/kimi-k3` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 11 |
| occurrence-06 | `ollama/gemma4-31b` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 11 |

The family lives in the **occurrence**, never in the arm name: the published
importer decides whether to parse a commitment surface as FCL-1 by exact
membership, `graph_import_h005.FCL_SURFACE_ARMS == ("mini_fcl",)`, so an arm
called `mini_fcl@kimi-k3` would be read as prose and the study's first fact
would vanish silently after the calls were spent.

Three asymmetries are declared, not corrected, and any cross-occurrence reading
must carry them:

* **`native` is available on one family only.** DeepSeek carries a thinking
  control on the wire; the five Ollama families do not, and the runner refuses
  the arm at plan time with `ARM_NATIVE_WIRE_UNKNOWN` rather than guessing at
  dispatch. The comparison is marked unavailable there, not dropped.
* **`bare` is not the same control everywhere.** Reasoning-disabled direct
  baseline on occurrence-01; default direct baseline on 02–06, where reasoning
  cannot be switched off through this surface.
* **OPAQUE rates are not comparable with H005 occurrence-01.** The fork declares
  two decode repairs and no others — strip one outer Markdown fence, then
  re-parse with `strict=False` — before the same strict shape check. The
  comparable figure is `strict_parse_would_succeed`, recorded per node beside
  `envelope_repairs`. A fence is a formatting habit, not a reasoning failure.

## The command sequence

`S=experiments/diagnostics/F001-fork5-multifamily`, and every command runs with
`PYTHONPATH=src python -X utf8 tools/multicycle_commitment_study_multi.py`.

Once, per occurrence — zero provider calls:

```
... initialize --study $S --output $S/occurrence-0N
... verify     --study $S --output $S/occurrence-0N
```

then **commit and push** the six frozen `plan.json`/`preflight.json` pairs.

Then four rounds. Per round, in this order and no other:

```
# 1. prepare, per occurrence with ready coordinates -- zero calls
... prepare-wave --study $S --output $S/occurrence-0N --problem daily --cycle 1

# 2. ONE commit + push covering every prepared wave's required input paths

# 3. one process, all six occurrences, against that one published commit
... send-round --study $S --publish-ref origin/<branch> \
      --occurrences occurrence-01 occurrence-02 occurrence-03 \
                    occurrence-04 occurrence-05 occurrence-06

# 4. ONE commit + push of every new record, then read the audit signal
```

`send-wave`/`send-round` refuse unless HEAD equals the publication ref **and**
every path in the wave's transitive closure — plan, material, arms, manifests,
the runner, the runtime pins, the provider module, the endpoint registry, and
every request, trace, attempt, receipt, artifact, raw response text and provider
call record a dependency reaches — is byte-identical to the committed bytes.
That closure includes the *previous* round's receipts, so a round cannot be sent
until the previous round's results are published: **one push per round**, five
in all. A moved ref is `PUBLISH_REF_CHANGED`; one changed byte is
`INPUT_NOT_PUBLISHED`. Neither constructs a provider.

After round 4, per occurrence:

```
... audit --study $S --output $S/occurrence-0N
```

Expect `max_calls` = COMPLETE + PARTIAL, `unvisited` 0, `out_of_scope` 0.

## The per-key rule

**At most five concurrent requests per credential**, and **one coordinator
process**. Both halves matter.

Five is enforced in three places: `ready_coordinates` admits at most `key_cap`
per `key_env` when the wave is built; `send-wave` re-refuses an oversized wave
with `WAVE_SIZE_INVALID` before any attempt marker or provider object exists;
and a module-level gate keyed by `key_env` holds every in-flight call, acquired
**before** the attempt marker is written, so an attempt exists only for a call
this process is about to make. `provider_openai_compat.slots_for` is a fourth
ceiling around the socket itself.

Because that gate is process-wide, **one `send-round` may drive all six
occurrences**: the five Ollama occurrences share one gate of five on
`OLLAMA_API_KEY` while occurrence-01 overlaps them on `DEEPSEEK_API_KEY`. What
is not authorised is two coordinator *processes* on one credential — nothing in
this repository can hold a ceiling across processes.

Keys are read from the environment at call time only. Load them into the send
command's environment from a gitignored file; never write one into a tracked
file, a record, a log or a commit. The runner's `write_new` refuses any record
containing a credential (`CREDENTIAL_IN_OUTPUT`).

## No retries, and what one failure costs

`retries` is 0 at every layer: one `complete` is one request on the wire or
none, and an attempted coordinate with no terminal evidence is audited, never
re-sent. **One `FAILED` node ends that arm for the rest of the occurrence** —
the next `prepare-wave` simply returns fewer coordinates and refuses nothing.
The audit signal is `counts.FAILED` >= 1 together with `counts.unvisited` > 0
and that arm's `invocations` row reading `"complete": false`. Read it after
every round. Each `FAILED` receipt carries `failure_code` beside `failure_type`,
so `HTTP_429`, `KEY_MISSING` and `TRANSPORT_OR_RESPONSE_ERROR` are
distinguishable without opening the provider call records.

Scope is frozen in each `arms.json` as `{"problems": ["daily"], "cycles": [1]}`,
pinned by `arms_sha256` and enforced as `SCOPE_EXCLUDED`. There is no path from
this register to `physics`, `philosophy`, `sociology`, cycle 2 or cycle 3, or to
the `matched` arm. `plan["max_calls"]` counts only what the scope admits and
**is** the authorisation; `plan["max_calls_envelope"]` keeps the full material
figure visible beside it.

## The follow-up: importer, then use relation

The occurrences are evidence; the reading is separate. Per occurrence, offline
and against published bytes:

```
python -X utf8 tools/import_h005.py      $S/occurrence-0N <analysis>/occurrence-0N/import
python -X utf8 tools/use_relation_h005.py $S/occurrence-0N <analysis>/occurrence-0N/use-table
```

See [graph-import-h005](graph-import-h005.md) and
[use-relation-h005](use-relation-h005.md). Both open the occurrence read-only
and refuse a destination inside `experiments/diagnostics/`; outputs belong under
`experiments/analyses/`. The importer supplies the mechanism facts the register
names — FCL-1 parse/schema outcomes, `report.resolution`, cross-document
`depends`, warrants, `att` edges, ν-attacks, reinstatement, grounded labels —
and the use-relation table supplies the juxtaposition whose four interpretive
cells only root fills by reading. **No cross-family merit reading is made by
either instrument, and none may be read off their counts.**

## Design record

* Register and pre-registration: [`PLAN.md`](../../experiments/diagnostics/F001-fork5-multifamily/PLAN.md)
* Fork design notes and the offline proof: [`docs/design/multicycle-commitment-study-multi-notes-2026-09-14.md`](../design/multicycle-commitment-study-multi-notes-2026-09-14.md)
* Adversarial review closure: [`docs/sources/multicycle-commitment-study-multi-review-fixes.md`](../sources/multicycle-commitment-study-multi-review-fixes.md)
* Transport: [provider-openai-compat](provider-openai-compat.md)
* Suite: `PYTHONPATH=src python -X utf8 -m unittest tests.test_multicycle_commitment_study_multi`
