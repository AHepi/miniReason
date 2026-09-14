# Commit/tree join check — REC-20260914-U and REC-20260914-X against the branch log

**Result: every published pair verifies.** 32 identities were extracted from the two receipts by the patterns below; 8 of them claim a tree beside the commit and all 8 are `VERIFIED` — in each case exactly one log row carries both the claimed commit and the claimed tree. There is no `MISMATCH_TREE` row (a commit in the log whose log tree differs from the tree claimed beside it), no `COMMIT_NOT_IN_LOG` row, and no `AMBIGUOUS_SHORT_ID` row. This is a clean check, and the extraction set underneath it is itemised so a reader can tell that from an incomplete one.

## Inputs

- Receipts: `docs/ledger/REC-20260914-U.md` (9 paragraphs, U-01..U-09) and `docs/ledger/REC-20260914-X.md` (9 paragraphs, X-01..X-09); a paragraph is a blank-line-separated block, numbered by position in the file.
- Log: `evidence/git-log-branch.txt`, 122 rows (comment headers excluded), columns `%H %T %h %ad %an %s`, produced read-only with `git log --format='%H %T %h %ad %an %s' --date=iso-strict 40bd5de..HEAD`. The verdict is a JOIN against this table, not a membership test: a claimed pair verifies only when one log row carries **both** ids; a commit present with a different tree is `MISMATCH_TREE`, not a pass.
- Checker: `check/commit_tree.py`; run `python3 check/commit_tree.py` from the sandbox root. It re-reads the inputs and rewrites this report deterministically. Tests: `python3 -m unittest check.test_commit_tree`.

## Extraction patterns and hit counts

Every claimed string in the rows table came out of one of these patterns; nothing is transcribed by hand. Patterns that hit zero times are listed too, so the reader can see what was looked for and not found in these receipts. All hex patterns are boundary-checked, so a prefix of a 64-hex SHA-256 digest can never masquerade as a 40-hex git id.

| pattern | layout | regex | hits | first match (abridged) |
|---|---|---|---|---|
| PAIR_FULL | commit+tree | `Prior verified commit/tree: `?(?P<c>(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f]))`? / `?(?P<t>(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f]))`?` | 3 | `Prior verified commit/tree: f50db28cafd4f84683564aab7f594339…` |
| PAIR_MARKED | commit+tree | `VERIFIED (?P<c>(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])) TREE (?P<t>(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f]))` | 3 | `VERIFIED 96ca2eb3188beeb3ca1d399cddb203a9d38ec8a9 TREE da1d4…` |
| PAIR_PROSE | commit+tree | `remote `[^`]*` at (?P<c>(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])), tree (?P<t>(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f]))` | 2 | `remote `claude/project-state-direction-j5rbun` at ad3e347b7c…` |
| PAIR_MARKED_C | commit-only | `VERIFIED (?P<c>(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f]))(?! TREE)` | 3 | `VERIFIED e9d9c47d96f45f8e9f356d7300ff7a8b4796b044` |
| PAIR_PROSE_C | commit-only-short | `remote `[^`]*` at (?P<c>(?<![0-9a-f])[0-9a-f]{7}(?![0-9a-f])),` | 0 | — |
| PROSE_CTX | commit-only | `the published commit `(?P<c>(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f]))`` | 3 | `the published commit `a1e516c54673c8a3ea2968ca3362ec6d1d725f…` |
| FROM_RANGE | commit-range | `in (?:seven|fifteen) commits from `(?P<c>(?<![0-9a-f])[0-9a-f]{7}(?![0-9a-f]))` through the closing one` | 2 | `in seven commits from `ad3e347` through the closing one` |
| SINGLE_SHORT | short-tag | ``(?P<c>(?<![0-9a-f])[0-9a-f]{7}(?![0-9a-f]))`` | 16 | ``ad3e347`` |

`SINGLE_SHORT` is admitted only inside subject-mention prose (paragraphs carrying one of “The decision's fifteen commits”, “in fifteen commits from”, “in seven commits from”, “in one commit,”), and a token already claimed by `FROM_RANGE` is reported once, as the range row. 18 raw backticked 7-hex tokens sit in such prose — U-02's `ad3e347` mention, X-09's fifteen labels, and the two range starts — yielding 16 `SINGLE_SHORT` rows plus the 2 `FROM_RANGE` rows.

## Rows

| # | receipt | ¶ | pattern | claimed commit | claimed tree | verdict | detail |
|---|---|---|---|---|---|---|---|
| 1 | REC-20260914-U | U-01 | PAIR_FULL | `f50db28cafd4f84683564aab7f5943393ed5e99c` | `4e7c6622aa734d0ceebc523daaa1aa5bd842a893` | VERIFIED | one log row (f50db28) carries both the claimed commit and the claimed tree |
| 2 | REC-20260914-U | U-02 | SINGLE_SHORT | `ad3e347` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “Publish the C001 contrast-triple study and freeze occurren” |
| 3 | REC-20260914-U | U-02 | PAIR_PROSE | `ad3e347b7c629414582a952c2bea8e4031bea702` | `89c4f9142b3c9c7eef12e7a33b3e28adfe48efab` | VERIFIED | one log row (ad3e347) carries both the claimed commit and the claimed tree |
| 4 | REC-20260914-U | U-08 | FROM_RANGE | `ad3e347` (7-hex) | — | FROM_RANGE_TIP_IN_LOG | start of the seven-commit range resolves; the closing commit verifies as this paragraph's own PAIR_PROSE row; the six middle rows of the range carry no ids in the receipt text (see final section) |
| 5 | REC-20260914-U | U-08 | PAIR_PROSE | `d6b7e30fbb15d86834bef0e6f86ed9239a6768fc` | `14b776dbe7b8d651f3d418a9546e83361cf1bffa` | VERIFIED | one log row (d6b7e30) carries both the claimed commit and the claimed tree |
| 6 | REC-20260914-X | X-01 | PAIR_FULL | `8b25a306332cd0c560b53214d94550eddf673919` | `fe03802edd79351f6cace4e1d3862cd4f10215b2` | VERIFIED | one log row (8b25a30) carries both the claimed commit and the claimed tree |
| 7 | REC-20260914-X | X-02 | PAIR_MARKED | `96ca2eb3188beeb3ca1d399cddb203a9d38ec8a9` | `da1d4bff5619b9a189575e11058c3b7a66d6be7b` | VERIFIED | one log row (96ca2eb) carries both the claimed commit and the claimed tree |
| 8 | REC-20260914-X | X-02 | PAIR_MARKED | `7bff688f89cbb7cdbb5a6f76c63fed6db8cb80e9` | `9b354336e5cc54c20e63a0795f69de7914a42c85` | VERIFIED | one log row (7bff688) carries both the claimed commit and the claimed tree |
| 9 | REC-20260914-X | X-03 | PROSE_CTX | `a1e516c54673c8a3ea2968ca3362ec6d1d725fb8` | — | SINGLE_VERIFIED | no tree claimed beside it here; log row a1e516c carries tree 3e106bbe980a0c3d4c52b3679e7c6bed7200f214 |
| 10 | REC-20260914-X | X-03 | PAIR_MARKED_C | `e9d9c47d96f45f8e9f356d7300ff7a8b4796b044` | — | SINGLE_VERIFIED | no tree claimed beside it here; log row e9d9c47 carries tree ea54c83cfa753dc5f702b9f979a68580a49cc757 |
| 11 | REC-20260914-X | X-05 | PROSE_CTX | `48ca127540a40dee7dee62b7d1f4a8386174d0ba` | — | SINGLE_VERIFIED | no tree claimed beside it here; log row 48ca127 carries tree 1d86a801fbdfa472ed478c809b61b39c90d71a8a |
| 12 | REC-20260914-X | X-05 | PAIR_MARKED_C | `7b0303f182289142bc0d79794aa95a1823b12a10` | — | SINGLE_VERIFIED | no tree claimed beside it here; log row 7b0303f carries tree cdf240b8f25f82b0fb419fbab806be06dabc39b2 |
| 13 | REC-20260914-X | X-07 | PROSE_CTX | `e8357c3d236c4c837a27920c96ae8c7301c447c4` | — | SINGLE_VERIFIED | no tree claimed beside it here; log row e8357c3 carries tree 1112033545960cc750f0f4a5cf7707666745ab24 |
| 14 | REC-20260914-X | X-07 | PAIR_MARKED_C | `d6157cf39f07aa60abf209e32c46ae0d57535c7d` | — | SINGLE_VERIFIED | no tree claimed beside it here; log row d6157cf carries tree 398fc28d76ffa1684d6505cb368a9e3ae12460ba |
| 15 | REC-20260914-X | X-08 | FROM_RANGE | `96ca2eb` (7-hex) | — | FROM_RANGE_TIP_IN_LOG | start of the fifteen-commit range resolves; the closing commit verifies as X-09's PAIR_MARKED row and the fifteen are enumerated in X-09 (15 SINGLE_SHORT rows below) |
| 16 | REC-20260914-X | X-08 | PAIR_FULL | `f25b4a93723c88a40ade062c065df20fd22490e9` | `908d0f5ee884a989772eecd00cb68aaf44bb8a87` | VERIFIED | one log row (f25b4a9) carries both the claimed commit and the claimed tree |
| 17 | REC-20260914-X | X-09 | PAIR_MARKED | `958f2f4173da679283388c1820d218a209dffdbb` | `79cbdfe9d1a03192d4bea8d84dc605d7862abdb8` | VERIFIED | one log row (958f2f4) carries both the claimed commit and the claimed tree |
| 18 | REC-20260914-X | X-09 | SINGLE_SHORT | `96ca2eb` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “Open REC-20260914-X to publish and dispatch F002, the fork” |
| 19 | REC-20260914-X | X-09 | SINGLE_SHORT | `7bff688` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “Publish the F002 register, the v3 successor runner and bot” |
| 20 | REC-20260914-X | X-09 | SINGLE_SHORT | `9967e3c` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “Record the verified publication of F002 in REC-20260914-X” |
| 21 | REC-20260914-X | X-09 | SINGLE_SHORT | `a1e516c` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “F002 round 1: publish wave0001's frozen inputs for both oc” |
| 22 | REC-20260914-X | X-09 | SINGLE_SHORT | `e9d9c47` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “F002 round 1 records: wave0001 terminal on both occurrence” |
| 23 | REC-20260914-X | X-09 | SINGLE_SHORT | `48ca127` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “F002 round 2: publish wave0002's frozen inputs and checkpo” |
| 24 | REC-20260914-X | X-09 | SINGLE_SHORT | `73d193f` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “REC-20260914-X cadence checkpoint: round 2 in flight, both” |
| 25 | REC-20260914-X | X-09 | SINGLE_SHORT | `7b0303f` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “F002 round 2 records: wave0002 terminal on both occurrence” |
| 26 | REC-20260914-X | X-09 | SINGLE_SHORT | `e8357c3` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “F002 round 3: publish wave0003's frozen inputs and checkpo” |
| 27 | REC-20260914-X | X-09 | SINGLE_SHORT | `d99ab67` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “REC-20260914-X cadence checkpoint: round 3 in flight, one ” |
| 28 | REC-20260914-X | X-09 | SINGLE_SHORT | `d6157cf` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “F002 round 3 records: wave0003 terminal, 8 of 10 calls, on” |
| 29 | REC-20260914-X | X-09 | SINGLE_SHORT | `63ae4b6` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “F002 round 4: publish wave0004's frozen input and checkpoi” |
| 30 | REC-20260914-X | X-09 | SINGLE_SHORT | `ff29eca` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “F002 round 4 records: wave0004 terminal, the dispatch is f” |
| 31 | REC-20260914-X | X-09 | SINGLE_SHORT | `e1a6f1a` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “F002 analyses: both published instruments at full scope, p” |
| 32 | REC-20260914-X | X-09 | SINGLE_SHORT | `f25b4a9` (7-hex) | — | SINGLE_VERIFIED | short id resolves to exactly one log row — log subject “Refresh STATUS and append the F002 section to the fork5 wo” |

## Strings in the receipts the extraction would NOT have caught

Named here so the coverage above is falsifiable. Conclusion: every string in either receipt that has the form of a git commit or tree identity is extracted above; the classes below either carry no identity in the text or are not git identities at all.

1. **U-08's range sentence has no ids for its middle commits.** *"in seven commits from `ad3e347` through the closing one, each pushed and each ref read back externally"* names ids only at its two endpoints (both extracted and verified — the `FROM_RANGE` row and the paragraph's own `PAIR_PROSE` row). The middle commits exist only as subjects in U's earlier paragraphs, so there is no id to extract and nothing to join. For the record, read off `evidence/git-log-branch.txt`, the rows strictly between `ad3e347` and the closing commit `d6b7e30` are exactly six — `04654a3` (Record the REC-20260914-U publication and freeze outcome), `1629af7` (C001 dispatch checkpoint 1: records through wave 14), `ee22ee4` (C001 dispatch checkpoint 2: records through wave 25), `865a800` (C001 dispatch checkpoint 3: records through wave 33), `c18d723` (C001 dispatch checkpoint 4: records through wave 43), `f353ac4` (C001 dispatch complete: all 240 coordinates, audit, and the comparison table) — so the sentence's "seven" is the start commit plus those six, the same construction X makes explicit: X-08's "fifteen commits" are enumerated in X-09 as the fifteen rows from `96ca2eb` through `f25b4a9`, with the closing commit `958f2f4` following them. Both counts are consistent with the log.
2. **Backticked 7-hex tokens outside subject-mention prose: 0.** Every backticked 7-hex token in the two receipts was admitted (the four marker phrases above cover all of them); none was excluded by the paragraph-shape test.
3. **Plain number-words are never extracted** — "47 waves", "85-row", "37 historical CRLF lines", and the ceiling figures `8192` / "8,192" (4 digits, not 7-hex tokens). None has the shape of a git identity, so the extractor never sees them; treating them as ids would manufacture false misses.
4. **64-hex SHA-256 file digests are not git identities** — the `plan_id` values, `material` and `runner_sha256` pins (e.g. `328b9452…`, `ccbb1165…`, `cdc4b571…`) fold into plan identities, not into `%H`/`%T`. All patterns here are length-anchored to 40-hex or 7-hex tokens with hex boundaries, so these digests cannot leak in as git ids; they are out of scope by construction.
5. **`PAIR_PROSE_C` hit zero times** — no receipt strings a bare 7-hex id after "remote … at"; wherever that phrasing occurs the id is full 40-hex and caught by `PAIR_PROSE`. The layout is listed so its absence is visible rather than silent.

## Cross-checks

- No tree claimed in either receipt appears in the log attached to a **different** commit than the one claimed beside it (checked over all 8 tree-claiming rows: 0 violations).
- `SINGLE_SHORT` resolution is a prefix scan over all 122 log rows; every one of the 16 admitted short ids (15 in X-09 plus U-02's `ad3e347` mention) resolves to exactly one row, so no ambiguity case arose.
- `PAIR_FULL` rows in U-01 and X-01 name the *prior* verified checkpoints (the closing commits of REC-20260914-T and -W respectively); both are log rows of their own and each verifies against its claimed tree.
- X-09's descriptions after each short id ("the opening receipt alone", "the v3 runner, its nineteen tests, …") are restatements rather than the log's subject strings; the join key for those rows is the short id alone, and the log subject of the row it resolves to is quoted in the detail column.
