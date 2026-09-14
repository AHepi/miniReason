# F001 — mechanism facts across six model families

**No label produced by these imports is a semantic attribution.** Statuses are
mechanism bookkeeping over the imported attack relation; they do not bear on the
FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone
interprets substantive output (H005 `PROTOCOL.md` §Interpretation). Every one of
the use tables leaves all four interpretive columns — `root_reading`,
`root_passage_cited`, `root_notes`, `root_initials_date` — empty in every row; a
blank cell is an unread row, not a reading of `unresolved`.

**No cross-family merit reading is made here, and none may be read off these
counts.** Every number below is a count of what the published instruments could
compute over six occurrences of identical frozen material. A family whose FCL-1
documents parse is not thereby correct, and a family whose documents do not parse
has not thereby failed to reason. Parser success, more objections, longer
documents, more refs, more ν nodes and a larger graph are not repair. A
`refuted` label is bookkeeping over the attack relation the authors themselves
declared; an `accepted` label on an unattacked artifact is accept-by-position,
and on a prose arm no warrant, no attack edge and no refuted label can arise at
all. Transport status is never a verdict: a `FAILED` coordinate and a ceiling
truncation are resource facts.

## What this directory is

The output of the two published instruments over the six F001 occurrences, at
**full scope** (no `--problem`/`--arm`/`--cycle` selector), plus each
occurrence's runner audit. Per occurrence:

```
occurrence-0N/import/      python -X utf8 tools/import_h005.py \
                             experiments/diagnostics/F001-fork5-multifamily/occurrence-0N \
                             experiments/analyses/F001-fork5-multifamily-2026-09-14/occurrence-0N/import
occurrence-0N/use-table/   python -X utf8 tools/use_relation_h005.py \
                             experiments/diagnostics/F001-fork5-multifamily/occurrence-0N \
                             experiments/analyses/F001-fork5-multifamily-2026-09-14/occurrence-0N/use-table
occurrence-0N/audit.json   PYTHONPATH=src python -X utf8 tools/multicycle_commitment_study_multi.py audit \
                             --study experiments/diagnostics/F001-fork5-multifamily \
                             --output experiments/diagnostics/F001-fork5-multifamily/occurrence-0N
```

All six imports exit 0. Every cross-file and self-consistency custody check is
**verified** in all six, with the same single skip pattern the owner's own H005
occurrence-01 produces: `projection_source` skips the structurally absent
`previous`/`origin` slots of the first invocation (4 of 20 on occurrences 01, 02,
03 and 06; 2 of 4 on occurrence-04; 2 of 9 on occurrence-05). `event_ts
nondecreasing` is `no` in all six, and that is the importer's own **declared
deviation**, not a fault: a wave runs several arms concurrently and their
`finished_utc` values interleave.

Register: `experiments/diagnostics/F001-fork5-multifamily/PLAN.md`.
Workflow: `docs/workflows/fork5-multifamily.md`. Receipt: REC-20260914-S.

Material: the H005 material verbatim plus one `study_id` key, sha256
`8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff` in all six
occurrences (H005's own is `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927`).
Plan ids:

| Occurrence | Endpoint | `plan_id` |
|---|---|---|
| occurrence-01 | `deepseek-flash` | `fd25a5a4ec8480b0aa9b29ba0d7ac771c16e32ce9d68709312b84c98296c3980` |
| occurrence-02 | `ollama/gpt-oss-120b` | `951ad3c58cb341f12ac922cab580e02879138d5d6cc626a0f9825af3ed29b3db` |
| occurrence-03 | `ollama/qwen3.5-397b` | `52d7b596c10fcc194dc326d6a47addecda93eb604baf1ce1dbc4e594e8bdeba4` |
| occurrence-04 | `ollama/glm-5.3` | `e2e3357ef2d67dda270a53f65151c6b1e94265000d487876e0cad735a9cc83c1` |
| occurrence-05 | `ollama/kimi-k3` | `620ee8bc7e6653dde7b16c221d8c2e0e2ace4968acdad2eeb34c4925380d1e4c` |
| occurrence-06 | `ollama/gemma4-31b` | `84a5fea6e8ad6f3184874cfad980df348e5b65265818f132f52b9669a5634264` |

## MECHANISM-FACTS — counts only

### Transport and decode (from `audit.json`)

| | 01 deepseek-flash | 02 gpt-oss-120b | 03 qwen3.5-397b | 04 glm-5.3 | 05 kimi-k3 | 06 gemma4-31b |
|---|---|---|---|---|---|---|
| authorised calls (`max_calls`) | 12 | 11 | 11 | 11 | 11 | 11 |
| COMPLETE | 12 | 11 | 11 | 4 | 7 | 11 |
| PARTIAL | 0 | 0 | 0 | 1 | 1 | 0 |
| FAILED | 0 | 0 | 0 | 3 | 2 | 0 |
| OPAQUE | 0 | 0 | 0 | 1 | 1 | 0 |
| unvisited (arm ended) | 0 | 0 | 0 | 3 | 1 | 0 |
| unresolved attempts | 0 | 0 | 0 | 0 | 0 | 0 |
| out of scope | 0 | 0 | 0 | 0 | 0 | 0 |
| envelope repairs — `fence_stripped` | 0 | 0 | 0 | 4 | 5 | 11 |
| envelope repairs — `lenient_control_chars` | 0 | 0 | 0 | 0 | 0 | 0 |
| `strict_parse_would_succeed` | 12 / 12 | 11 / 11 | 11 / 11 | 0 / 8 | 2 / 10 | 0 / 11 |
| `reasoning_content_present` | 1 | 11 | 11 | 8 | 10 | 0 |
| completion tokens | 18,815 | 12,365 | 35,900 | 51,830 | 58,950 | 4,173 |

Run total: **63 calls spent of 67 authorised**, 56 COMPLETE, 2 PARTIAL, 5 FAILED,
2 OPAQUE, 0 unresolved attempts, 20 `fence_stripped`, 0 `lenient_control_chars`,
36 `strict_parse_would_succeed`. The four unspent calls are the coordinates the
no-retry truncation rule removed from the queue (`mini_fcl/response`,
`mini_fcl/carry`, `mini_prose/carry` on occurrence-04 and `mini_fcl/carry` on
occurrence-05); they were never dispatched. Every one of the seven non-COMPLETE
terminal records carries `failure_code: INCOMPLETE_GENERATION` with
`finish_reason: length` at exactly 8,192 completion tokens, and the five FAILED
ones returned zero bytes of content.

**`strict_parse_would_succeed` is the figure comparable with H005 occurrence-01.
The OPAQUE rate is not** — this occurrence's decoder declares two repairs the
owner's strict-only decode does not have. A fence is a formatting habit, not a
reasoning failure, and the nine, five and four `fence_stripped` counts on
occurrences 06, 05 and 04 are counts of that habit.

**`bare` is not the same control across this row.** On occurrence-01 it is a
reasoning-disabled direct baseline (`thinking: {"type": "disabled"}` on the
wire); on 02–06 it is a default direct baseline, reasoning on and unswitchable
through this surface. **`native` exists on occurrence-01 only** — the one family
whose wire carries a thinking control; on the other five the comparison is
*marked unavailable* (`ARM_NATIVE_WIRE_UNKNOWN` at plan time), not dropped.

### FCL-1 commitment surface, `mini_fcl` arm only (from `import/report.json`)

| | 01 | 02 | 03 | 04 | 05 | 06 |
|---|---|---|---|---|---|---|
| `mini_fcl` nodes reaching the importer | 5 | 5 | 5 | 1 | 3 | 5 |
| `read_fcl1` | 5 | 3 | 5 | 0 | 2 | 2 |
| `parse_failure` | 0 | 2 | 0 | 0 | 0 | 0 |
| `schema_failure` | 0 | 0 | 0 | 1 | 0 | 3 |
| `unavailable_decode_failure` | 0 | 0 | 0 | 0 | 1 | 0 |
| `prose_commitment_surface` (all other arms) | 7 | 6 | 6 | 3 | 5 | 6 |

### Graph facts (from `import/report.json`)

| | 01 | 02 | 03 | 04 | 05 | 06 |
|---|---|---|---|---|---|---|
| events | 50 | 21 | 32 | 6 | 24 | 26 |
| artifacts labelled | 22 | 14 | 16 | 5 | 15 | 13 |
| refs seen | 80 | 15 | 36 | 0 | 34 | 4 |
| refs resolved | 66 | 4 | 17 | 0 | 34 | 4 |
| refs dangling | 14 | 11 | 19 | 0 | 0 | 0 |
| ref extensions | 0 | 0 | 0 | 0 | 0 | 0 |
| refs to task artifact | 0 | 0 | 3 | 0 | 0 | 0 |
| `depends_cross_document` | 0 | 0 | 0 | 0 | 0 | 0 |
| `depends_intra_document` | 13 | 4 | 0 | 0 | 7 | 0 |
| warrants | 5 | 0 | 0 | 0 | 5 | 0 |
| `att` edges | 3 | 0 | 0 | 0 | 1 | 0 |
| `dep` edges | 0 | 0 | 0 | 0 | 0 | 0 |
| ν artifacts (`validity_node_minted_unasserted`) | 5 | 0 | 0 | 0 | 5 | 0 |
| ν nodes appearing in `att` (ν-attacks) | 0 | 0 | 0 | 0 | 0 | 0 |
| `criticism_of_criticism_retargeted` | 0 | 0 | 0 | 0 | 0 | 0 |
| reinstatements | 0 | 0 | 0 | 0 | 0 | 0 |
| labels — `accepted` | 20 | 14 | 16 | 5 | 14 | 13 |
| labels — `refuted` | 2 | 0 | 0 | 0 | 1 | 0 |
| use-table rows | 28 | 0 | 0 | 0 | 12 | 0 |

Error-severity residue, as the importer prints it above its own label table:
occurrence-01 `ref_unresolved` 14; occurrence-02 `ref_unresolved` 11 and
`parse_failure` 2; occurrence-03 `ref_unresolved` 19; occurrence-04
`schema_failure` 1; occurrence-05 none; occurrence-06 `schema_failure` 3. Read
the residue before reading any label.

A use table has 0 rows wherever no FCL-1 surface was read, or where the surfaces
read declared no cross-document reference: the instrument walks authored refs
out of parsed commitment surfaces and nothing else, and it never parses a prose
surface.

## What a reader may and may not take from this

May: that these counts differ across the six occurrences, and by how much, on
this one `fork5` invocation of the `daily` problem, cycle 1, at `max_tokens`
8192 and `timeout_seconds` 180, with `seed: 7` on the five Ollama occurrences
and none on DeepSeek, on 2026-09-14.

May not: anything about model capability, about FCL-1's value, about Mini's
scheduler (which does not execute here), about any family's behaviour on another
problem or another cycle, or about any family not listed. Six families with one
invocation each is six observations, not a sample. **Root alone reads the
content**, and no count here is a substitute for reading the artifacts.

---

## Appended 2026-09-14 — occurrences 07 and 08, the same two families at a second ceiling

**Appended after the six-occurrence run; nothing above this line is altered, and
no record above it is re-sent, relabelled, repaired or superseded.** Everything
the banners at the top of this page say applies here without exception: these
are counts of what the published instruments could compute, no count ranks a
family, invariant I7 holds, and the four interpretive columns of both new use
tables are empty in every row.

Occurrences 07 (`ollama/glm-5.3`) and 08 (`ollama/kimi-k3`) are **the same two
families as occurrences 04 and 05**, on the same frozen material (`material.json`
sha256 `8a00ff1246d43dde4856d9850d8563bfd57579a42e456236ed8b22c7437c4eff`, the
same bytes as all six above), the same arms, the same scope
`{"problems": ["daily"], "cycles": [1]}`, the same `seed: 7`, the same
`timeout_seconds: 180` read from the endpoint record, `automatic_retries` 0 and
no thinking control anywhere. Two things differ and nothing else does: the
per-arm completion ceiling, **8,192 on 04/05 and 32,768 on 07/08**, and the
runner identity, `tools/multicycle_commitment_study_multi.py` on 04/05 and
`tools/multicycle_commitment_study_multi_v2.py` on 07/08.

**04/05 and 07/08 are the same families at two ceilings under two runner
identities whose only behavioural difference is the ceiling bound.** v2 is a byte
copy of v1 with four declared differences — a provenance header, the ceiling
constant split so that the bound becomes the provider's own `MAX_CEILING =
393216` while the default an undeclared arm receives stays `DEFAULT_CEILING =
8192`, `manifest_for` deriving its completion figures from the occurrence's
declared arm ceilings, and a docstring that says v2 — and
`tests/test_multicycle_commitment_study_multi_v2.py::V2DiffProofTests` proves
that list by normalising the module docstring away, diffing the two files and
refusing any hunk that is not on it. The register's *Successor occurrences 07 and
08 under runner v2* section carries the full statement. Pre-registration,
publication and dispatch are REC-20260914-T.

| Occurrence | Endpoint | `plan_id` |
|---|---|---|
| occurrence-07 | `ollama/glm-5.3` | `77aa01f46f57471838e6cb46c96eb3ad9adfc2c1053376051dc098edd58d306d` |
| occurrence-08 | `ollama/kimi-k3` | `04c26f24812a4e48d41cfd6f6ef16785ba25ea183894bfafe86d6eb0e35af8ee` |

Neither can collide with a v1 plan: v2 writes its own sha256
(`8f7eb9d73e8c497f6a2aabf826a8409bb3c60682b36aaa361f650a9e870adbd0`) as
`runner_sha256` and `helper_sha256`, both folded into `plan_id`.

### The two new rows

| Occurrence | Endpoint | ceiling | runner | authorised | spent | COMPLETE | PARTIAL | FAILED | OPAQUE | unvisited | unresolved | out of scope | `fence_stripped` | `lenient_control_chars` | `strict_parse_would_succeed` | `reasoning_content_present` | completion tokens | nodes over 8,192 | `finish_reason: length` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| occurrence-07 | `ollama/glm-5.3` | 32,768 | v2 | 11 | 9 | 8 | 0 | 1 | 0 | 2 | 0 | 0 | 7 | 0 | 1 / 8 | 8 / 8 | 85,266 | 6 of 8 | **0** |
| occurrence-08 | `ollama/kimi-k3` | 32,768 | v2 | 11 | 11 | 10 | 0 | 1 | 1 | 0 | 0 | 0 | 4 | 0 | 5 / 10 | 10 / 10 | 67,796 | 4 of 10 | **0** |

Run total: **20 calls spent of 22 authorised**, 18 COMPLETE, 0 PARTIAL, 2 FAILED,
1 OPAQUE, 0 unresolved attempts, 0 out of scope, 11 `fence_stripped`, 0
`lenient_control_chars`, 6 `strict_parse_would_succeed` of 18. The two unspent
calls are `mini_fcl/response` and `mini_fcl/carry` on occurrence-07, removed from
the queue by the no-retry truncation rule after that arm's round-2 failure; they
were never dispatched.

Beside the same two rows at the earlier ceiling, for reading the pair:

| | 04 glm-5.3 @ 8,192 (v1) | 07 glm-5.3 @ 32,768 (v2) | 05 kimi-k3 @ 8,192 (v1) | 08 kimi-k3 @ 32,768 (v2) |
|---|---|---|---|---|
| authorised calls | 11 | 11 | 11 | 11 |
| COMPLETE | 4 | 8 | 7 | 10 |
| PARTIAL | 1 | 0 | 1 | 0 |
| FAILED | 3 | 1 | 2 | 1 |
| OPAQUE | 1 | 0 | 1 | 1 |
| unvisited (arm ended) | 3 | 2 | 1 | 0 |
| unresolved attempts | 0 | 0 | 0 | 0 |
| out of scope | 0 | 0 | 0 | 0 |
| `fence_stripped` | 4 | 7 | 5 | 4 |
| `lenient_control_chars` | 0 | 0 | 0 | 0 |
| `strict_parse_would_succeed` | 0 / 8 | 1 / 8 | 2 / 10 | 5 / 10 |
| `reasoning_content_present` | 8 | 8 | 10 | 10 |
| completion tokens | 51,830 | 85,266 | 58,950 | 67,796 |
| terminal records with `failure_code: INCOMPLETE_GENERATION` | 4 | **0** | 3 | **0** |
| terminal records with `failure_code: TRANSPORT_OR_RESPONSE_ERROR` | 0 | **1** | 0 | **1** |

**Every non-COMPLETE terminal record changed kind.** At 8,192 all seven
non-COMPLETE records on 04 and 05 were `INCOMPLETE_GENERATION` /
`finish_reason: length` at exactly the ceiling, five of them with a zero-byte raw
response. At 32,768 **no node on either occurrence reached the ceiling at all**:
`finish_reason: length` occurs zero times, and the largest single completion is
16,871 tokens (occurrence-07 `mini_prose/response`). Ten of the eighteen
COMPLETE nodes — six of eight on occurrence-07 and four of ten on occurrence-08 —
spent more than 8,192 completion tokens, so ten calls that returned a
contribution here are calls the earlier ceiling would have cut off.

The two FAILED nodes are a different transport fact and are reported as such:
**occurrence-07 `mini_fcl/objection`** and **occurrence-08 `mini_fcl/carry`**,
both `failure_code: TRANSPORT_OR_RESPONSE_ERROR`, both `"The read operation timed
out"` at 180,368 ms and 180,456 ms against the endpoint record's **180-second
timeout, which is not a per-arm declaration and did not move with the ceiling**.
Neither carries a `finish_reason`, a `usage` or any content; neither was retried;
each ended `mini_fcl` for the rest of its occurrence, which is why occurrence-07
shows `unvisited` 2 and `"complete": false` on that arm's invocation row. That a
longer permitted generation can meet a fixed wall-clock timeout is a resource
fact about this transport, recorded here and not interpreted.

### FCL-1 commitment surface, `mini_fcl` arm only (from `import/report.json`)

| | 04 | 07 | 05 | 08 |
|---|---|---|---|---|
| `mini_fcl` nodes reaching the importer | 1 | 2 | 3 | 4 |
| `read_fcl1` | 0 | 2 | 2 | 3 |
| `parse_failure` | 0 | 0 | 0 | 0 |
| `schema_failure` | 1 | 0 | 0 | 1 |
| `unavailable_decode_failure` | 0 | 0 | 1 | 0 |
| prose-arm nodes reaching the importer (`bare` + `mini_prose`) | 3 | 6 | 5 | 6 |
| `prose_commitment_surface` | 3 | 6 | 5 | 5 |
| `unavailable_decode_failure` on a prose arm | 0 | 0 | 0 | 1 |

Occurrence-08's one prose `unavailable_decode_failure` is `mini_prose/rival`, the
occurrence's single OPAQUE node: a COMPLETE delivery whose envelope no declared
repair rescues, so the importer had no decodable commitment surface to read from
it. Occurrence-08's one `schema_failure` is `mini_fcl/rival`.

### Graph facts (from `import/report.json`)

| | 04 | 07 | 05 | 08 |
|---|---|---|---|---|
| events | 6 | 35 | 24 | 29 |
| artifacts labelled | 5 | 11 | 15 | 13 |
| refs seen | 0 | 39 | 34 | 66 |
| refs resolved | 0 | 33 | 34 | 30 |
| refs dangling | 0 | 0 | 0 | 36 |
| ref extensions | 0 | **6** | 0 | 0 |
| refs to task artifact | 0 | 0 | 0 | 0 |
| `depends_cross_document` | 0 | 0 | 0 | 0 |
| `depends_intra_document` | 0 | 13 | 7 | 10 |
| warrants | 0 | 1 | 5 | 0 |
| `att` edges | 0 | 1 | 1 | 0 |
| `dep` edges | 0 | 0 | 0 | 0 |
| ν artifacts (`validity_node_minted_unasserted`) | 0 | 1 | 5 | 0 |
| ν nodes appearing in `att` (ν-attacks) | 0 | 0 | 0 | 0 |
| `criticism_of_criticism_retargeted` | 0 | 0 | 0 | 0 |
| reinstatements | 0 | 0 | 0 | 0 |
| labels — `accepted` | 5 | 10 | 14 | 13 |
| labels — `refuted` | 0 | 1 | 1 | 0 |
| use-table rows | 0 | 6 | 12 | 0 |

`depends_cross_document` is **0 in all eight occurrences of this study**, at
either ceiling, on every family. Occurrence-07's six `ref_extension` are the
first non-zero count of that kind anywhere in F001; they are counted and not
interpreted. Error-severity residue, as the importer prints it above its own
label table: occurrence-07 **none**; occurrence-08 `ref_unresolved` 36 and
`schema_failure` 1. Read the residue before reading any label. A use table has 0
rows where the surfaces read declared no cross-document reference — occurrence-08
read three FCL-1 documents and still has 0 rows, because the refs its documents
declare resolve nowhere the instrument may follow.

### Custody

Both imports exit 0. Every cross-file and self-consistency check is **verified**
in both — material pin, manifest pins, receipt presence, artifact bytes against
receipt, status against receipt, public text, attempt against receipt, request
record, trace pinning, provider bytes, wave placement — with the one skip pattern
every F001 occurrence produces, `projection_source` skipping 3 of 12 structurally
absent `previous`/`origin` slots in each. `event_ts_nondecreasing` is `no` in
both, the importer's own declared deviation for concurrently run waves and not a
fault. The two occurrence audits report `max_calls` against COMPLETE + PARTIAL +
FAILED + unvisited exactly (8 + 0 + 1 + 2 and 10 + 0 + 1 + 0, both 11), with
`out_of_scope` 0 and `unresolved_attempts` 0.

### What a reader may and may not take from these two rows

**May**: that these counts differ between 8,192 and 32,768 on these two
families, and by how much, on this one `fork5` invocation of the `daily` problem,
cycle 1, at `timeout_seconds` 180 with `seed: 7`; and that at 32,768 no node
reached the ceiling while at 8,192 seven did.

**May not**: that either family reasons better, worse, or differently at the
higher ceiling; that a raised ceiling improves, repairs or degrades anything;
that more tokens, more refs, more events, more warrants, a larger graph or a
parsed FCL-1 document is a better contribution; or that the earlier records are
in any way corrected by these. A ceiling is a transport budget. Reasoning was not
manipulated on either family at either ceiling — no thinking control is available
on this surface and none was set — and `reasoning_content_present` is 8 of 8 and
10 of 10 here exactly as it was 8 and 10 there. The only comparison these rows
license is *what these two families returned at 8,192 completion tokens versus at
32,768*, and the reading of any contribution is root's, by reading it.
