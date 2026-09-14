# H005 occurrence-01 — snapshot analysis outputs, 2026-09-14

> **I7.** No label in any file under this directory is a semantic attribution. Every status, count, edge and residue code here is mechanism bookkeeping over material the occurrence's own authors declared; none of it bears on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Every interpretive cell of both use tables is **empty**: the instrument records juxtapositions, and the reading is root's (PROTOCOL.md §Interpretation).

Four outputs of the two published offline instruments, run over the frozen
H005 occurrence `experiments/diagnostics/H005-open-prose-commitments/occurrence-01`.
Nothing here is new evidence. It re-expresses evidence that already exists,
in two vocabularies, and reports what each vocabulary cannot carry. Published
under receipt REC-20260914-R.

Nothing under `experiments/diagnostics/` was written, moved or touched. Both
tools open the occurrence read-only and both refuse a destination inside it;
this directory is a sibling under `experiments/analyses/`.

## The snapshot these outputs were taken from

| what | value |
|---|---|
| repository commit at generation | `6114aedb3de0d06a0861229d310d7a5a40932526` |
| tree at generation | `3a110e1fa0d4d0f7e4f19b98b08f8252055f4eb4` |
| occurrence | `experiments/diagnostics/H005-open-prose-commitments/occurrence-01` |
| occurrence `plan_id` | `21e3cf1dff73423785d2e6faab5d32971cd2295cb5ce7c5ca07bbd45eb2396a6` |
| occurrence `material_sha256` | `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927` |
| importer | `src/minireason/graph_import_h005.py`, `importer_version` `import_h005/1` |
| instrument | `src/minireason/use_relation_h005.py`, `instrument_version` `use_relation_h005/1` |

**Custody digest.** Each output records the sha256 of every occurrence file it
actually read. The single digest below is that map hashed with the
repository's canonical structure digest,
`minireason.provider.digest` — `sha256(json.dumps(value, ensure_ascii=False,
sort_keys=True, separators=(",", ":")).encode())` — over
`report.json["custody"]["files"]` for an import and over
`use_table.json["files_read"]` for a use table:

| output | files read | custody digest |
|---|---|---|
| `import-golden/` | 51 | `555dfb6dc05572a2446848d0d3cf1d8eaabcf0b6fe09ad2e021ca0f83215c8e8` |
| `import-full/` | 147 | `396c47ada42e8b298a3b40d64bdf6cff10d71eb32086b5c1f506ba570e2d44d3` |
| `use-table-golden/` | 51 | `2c85b586f1e06490e51f2294e817773795efa523335761ae176eb82e52f3165e` |
| `use-table-full/` | 147 | `5ef0ffad26b9d177caa941bdb6ec7799620138c2c9b96cd6f276f821a2fbd734` |

Both importer runs report every cross-file and self-consistency custody check
verified, and `error_severity_residue` empty.

## The exact commands

Run from the repository root, with the tools as published:

```
python -X utf8 tools/import_h005.py \
    experiments/diagnostics/H005-open-prose-commitments/occurrence-01 \
    experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/import-golden \
    --problem daily --arm mini_fcl --cycle 1

python -X utf8 tools/import_h005.py \
    experiments/diagnostics/H005-open-prose-commitments/occurrence-01 \
    experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/import-full

python -X utf8 tools/use_relation_h005.py \
    experiments/diagnostics/H005-open-prose-commitments/occurrence-01 \
    experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-golden \
    --problem daily --arm mini_fcl --cycle 1

python -X utf8 tools/use_relation_h005.py \
    experiments/diagnostics/H005-open-prose-commitments/occurrence-01 \
    experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14/use-table-full
```

Each destination must not already exist; both tools create it with
`exist_ok=False` and refuse to overwrite. To re-run, name a fresh directory
outside the repository and compare, which is what the byte-identity check
below does.

## What is in each directory

| directory | scope | contents |
|---|---|---|
| `import-golden/` | `daily/mini_fcl/cycle01`, 5 coordinates | a `deepreason_core` graph root: `objects/`, `blobs/`, `log.jsonl`, plus `REPORT.md`, `report.json`, `side_table.json`, `residue.json` — 60 files |
| `import-full/` | the whole occurrence, 17 coordinates over `bare`, `native`, `matched`, `mini_prose`, `mini_fcl` | the same shape — 95 files |
| `use-table-golden/` | `daily/mini_fcl/cycle01`, 5 coordinates | `USE_TABLE.md` and `use_table.json` |
| `use-table-full/` | the whole occurrence, 17 coordinates | `USE_TABLE.md` and `use_table.json` |

Mechanism bookkeeping, quoted here only so a reader can see what the files
hold without opening them, and **not** a finding about anything:
`import-golden` mints 17 artifacts over 38 events with 7 warrants, 4 attack
edges and 0 dependence edges, and its grounded extension over the authors'
own declared attack relation is 14 `accepted` and 3 `refuted`; `import-full`
mints 29 artifacts over 50 events with the same 7 warrants, 4 attack edges and
0 dependence edges, 26 `accepted` and 3 `refuted`, and carries the importer's
multi-arm framing paragraph because its scope spans five arms. An `accepted`
label is accept-by-position — no warrant in the import targets that artifact —
and a prose commitment surface is never parsed, so no warrant and no `refuted`
label can arise from a prose arm at all. Read `residue.json` before reading
any label.

## Every root cell is empty

Both use tables carry 22 cross-document rows. In both, all four interpretive
columns are the empty string in every one of those rows:

| column | `use-table-golden` | `use-table-full` |
|---|---|---|
| `root_reading` | 22 / 22 empty | 22 / 22 empty |
| `root_passage_cited` | 22 / 22 empty | 22 / 22 empty |
| `root_notes` | 22 / 22 empty | 22 / 22 empty |
| `root_initials_date` | 22 / 22 empty | 22 / 22 empty |

A blank cell is an **unread row**, not a reading of `unresolved`. The
instrument writes none of the four and never will; `unresolved` is a legal
value for root to write and stays unresolved (FW5:634).

Both tables walk the same 84 authored refs — 22 cross-document, 62
intra-document, 0 to the exposed task artifact, 0 unresolved — because only
the `mini_fcl` arm carries an FCL-1 commitment surface. `use-table-full`
therefore lists **12 nodes whose commitment surface was not read**: ten prose
surfaces, which this instrument never parses, and the two
`unavailable_decode_failure` surfaces already recorded in
`docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md`, where the
commitments were authored and lost in decoding. That those twelve contribute
no rows is a fact about commitment-surface availability and about what this
instrument reads. It is not a fact about those contributions, and it is not
evidence that their authors declined to commit.

## Regenerating from the same snapshot is byte-identical

Proved, not asserted. Every one of the four outputs was generated three times
from this same snapshot: twice into temporary roots outside the repository —
the second under `PYTHONHASHSEED=12345`, the first with the variable unset —
and once into this directory under `PYTHONHASHSEED=0`. All eight resulting
comparisons were made with `diff -rq` and every one of them printed nothing
and exited 0:

```
diff -rq <tmp-a>/import-golden      <tmp-b>/import-golden        # no differences
diff -rq <tmp-a>/import-golden      ./import-golden              # no differences
diff -rq <tmp-a>/import-full        <tmp-b>/import-full          # no differences
diff -rq <tmp-a>/import-full        ./import-full                # no differences
diff -rq <tmp-a>/use-table-golden   <tmp-b>/use-table-golden     # no differences
diff -rq <tmp-a>/use-table-golden   ./use-table-golden           # no differences
diff -rq <tmp-a>/use-table-full     <tmp-b>/use-table-full       # no differences
diff -rq <tmp-a>/use-table-full     ./use-table-full             # no differences
```

No file differed and no file was present on one side only. This is what the
importer's `Event.ts` discipline buys: every timestamp is a `finished_utc`
read out of the occurrence's own receipts, never a wall clock, so two imports
of the same bytes produce the same root. The same run also demonstrates that
neither tool's output depends on Python's hash seed.

The only thing that changes between two runs is the destination path the CLI
echoes on its `out_root` / `out_dir` line, which is the name of the directory
you asked for.

## This directory is hash-pinned by nothing

Adding it changes no identity that any frozen plan or verifying check depends
on. `runtime_files` hashes `src/creib/**` plus `src/minireason/provider.py`;
`campaign.source_identity()` hashes `.py` and `.json` under `src/` plus
`pyproject.toml`; `tests/data/h005_import_pins.json` pins occurrence files
under `experiments/diagnostics/` only; and no plan's `runtime_files` map
contains any path under `experiments/`. Both digests were re-measured after
this directory was committed and are unchanged from the values recorded in
REC-20260914-Q. Nothing under `tests/` reads this directory, and no test
enumerates `experiments/`.

## Where to read further

- The import route and its custody table: `docs/workflows/graph-import-h005.md`.
- The importer's design notes, deviations and open questions: `docs/design/h005-import-notes-2026-09-14.md`.
- The use-relation route: `docs/workflows/use-relation-h005.md`.
- The instrument's design notes: `docs/design/use-relation-h005-notes-2026-09-14.md`.
- The review whose proposal P1 the instrument builds: `docs/reviews/fw5-vs-harness-spec-2026-09-14.md`, with `docs/errata/interpretations.md` INT-009 on its finding count.
