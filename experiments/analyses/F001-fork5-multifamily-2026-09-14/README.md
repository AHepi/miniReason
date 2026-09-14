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
