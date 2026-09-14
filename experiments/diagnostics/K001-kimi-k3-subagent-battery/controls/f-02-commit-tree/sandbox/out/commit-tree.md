# Commit and tree identities in REC-20260914-U and REC-20260914-X, joined against the frozen branch log

Produced by `python3 check/commit_tree_join.py` inside the sandbox. It reads
`docs/ledger/REC-20260914-U.md`, `docs/ledger/REC-20260914-X.md` and
`evidence/git-log-branch.txt` and writes this file; it modifies nothing.

The log is a frozen extract, and its own header records how it was taken:

    # Frozen git-log extract — branch claude/project-state-direction-j5rbun
    # Produced read-only from /home/user/miniReason at battery build time with:
    #   git log --format='%H %T %h %ad %an %s' --date=iso-strict 40bd5de..HEAD
    # Columns: full-commit-sha  full-tree-sha  short-commit  author-date(ISO)  author  subject

It carries **122 commit lines**, counted by this script from `evidence/git-log-branch.txt`.

## What was extracted, and by what pattern

Every identity below was taken out of the receipt text by regular expression,
never transcribed by hand. A git object id is matched as exactly 40 lowercase
hex characters with no hex character touching either end, which is what keeps
the receipts' 64-character sha256 digests (plan ids, material digests, file
digests) out of the extraction. Patterns are applied in order and a span
already claimed by an earlier pattern is not re-read by a later one.

| Pattern | Form | Rows |
| --- | --- | --- |
| P1 | `VERIFIED <commit> TREE <tree>` | 3 |
| P2 | `at <commit>, tree <tree>` | 2 |
| P3 | `<commit> / <tree>  (the 'Prior verified commit/tree' form)` | 3 |
| P4 | `VERIFIED <commit>  (no TREE beside it)` | 3 |
| P5 | `a bare 40-hex commit id not already taken by P1-P4` | 3 |
| P6 | `a bare 7-hex short commit id carrying at least one of a-f, not already taken by P1-P5` | 18 |

Nothing git-id-shaped was left unread. Counted independently of the patterns
above, by a second regular expression over the whole of each file:

* `REC-20260914-U.md`: 6 maximal 40-hex runs, 2 maximal 7-hex runs
* `REC-20260914-X.md`: 16 maximal 40-hex runs, 16 maximal 7-hex runs
* patterns P1-P5 consumed **22 of 22** 40-hex runs (a pair consumes two: the
  commit and the tree beside it); P6 consumed **18 of 18** 7-hex runs.
* mixed- or upper-case 7- or 40-character hex runs, which the lowercase
  patterns would not have matched: **0**.

## The join

One row per identity claimed. The verdict is a join against the log's own
`%H %T` columns: where a receipt names a tree beside a commit, the log's tree
for that commit decides the row.

| # | Receipt, paragraph | Pattern | Claimed commit | Claimed tree | Verdict | Log |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | REC-20260914-U p1 (line 1, REC-20260914-U opened at 2026-09-14 07:57 UTC) | P3 | `f50db28cafd4f84683564aab7f5943393ed5e99c` | `4e7c6622aa734d0ceebc523daaa1aa5bd842a893` | **PAIR VERIFIED** | log tree 4e7c6622aa734d0ceebc523daaa1aa5bd842a893 |
| 2 | REC-20260914-U p2 (line 3, REC-20260914-U publication outcome at 2026-09-14 07:58:54 UTC) | P6 | `ad3e347` | — | **COMMIT VERIFIED** | resolves to ad3e347b7c629414582a952c2bea8e4031bea702, tree 89c4f9142b3c9c7eef12e7a33b3e28adfe48efab (no tree claimed beside it) |
| 3 | REC-20260914-U p2 (line 3, REC-20260914-U publication outcome at 2026-09-14 07:58:54 UTC) | P2 | `ad3e347b7c629414582a952c2bea8e4031bea702` | `89c4f9142b3c9c7eef12e7a33b3e28adfe48efab` | **PAIR VERIFIED** | log tree 89c4f9142b3c9c7eef12e7a33b3e28adfe48efab |
| 4 | REC-20260914-U p8 (line 15, REC-20260914-U closed at 2026-09-14 09:05 UTC) | P6 | `ad3e347` | — | **COMMIT VERIFIED** | resolves to ad3e347b7c629414582a952c2bea8e4031bea702, tree 89c4f9142b3c9c7eef12e7a33b3e28adfe48efab (no tree claimed beside it) |
| 5 | REC-20260914-U p8 (line 15, REC-20260914-U closed at 2026-09-14 09:05 UTC) | P2 | `d6b7e30fbb15d86834bef0e6f86ed9239a6768fc` | `14b776dbe7b8d651f3d418a9546e83361cf1bffa` | **PAIR VERIFIED** | log tree 14b776dbe7b8d651f3d418a9546e83361cf1bffa |
| 6 | REC-20260914-X p1 (line 1, REC-20260914-X opened at 2026-09-14 10:06 UTC) | P3 | `8b25a306332cd0c560b53214d94550eddf673919` | `fe03802edd79351f6cace4e1d3862cd4f10215b2` | **PAIR VERIFIED** | log tree fe03802edd79351f6cace4e1d3862cd4f10215b2 |
| 7 | REC-20260914-X p2 (line 3, REC-20260914-X publication outcome at 2026-09-14 10:13 UTC) | P1 | `96ca2eb3188beeb3ca1d399cddb203a9d38ec8a9` | `da1d4bff5619b9a189575e11058c3b7a66d6be7b` | **PAIR VERIFIED** | log tree da1d4bff5619b9a189575e11058c3b7a66d6be7b |
| 8 | REC-20260914-X p2 (line 3, REC-20260914-X publication outcome at 2026-09-14 10:13 UTC) | P1 | `7bff688f89cbb7cdbb5a6f76c63fed6db8cb80e9` | `9b354336e5cc54c20e63a0795f69de7914a42c85` | **PAIR VERIFIED** | log tree 9b354336e5cc54c20e63a0795f69de7914a42c85 |
| 9 | REC-20260914-X p3 (line 5, REC-20260914-X dispatch checkpoint 1 at 2026-09-14 10:15 UTC) | P5 | `a1e516c54673c8a3ea2968ca3362ec6d1d725fb8` | — | **COMMIT VERIFIED** | log tree 3e106bbe980a0c3d4c52b3679e7c6bed7200f214 (no tree claimed beside it) |
| 10 | REC-20260914-X p3 (line 5, REC-20260914-X dispatch checkpoint 1 at 2026-09-14 10:15 UTC) | P4 | `e9d9c47d96f45f8e9f356d7300ff7a8b4796b044` | — | **COMMIT VERIFIED** | log tree ea54c83cfa753dc5f702b9f979a68580a49cc757 (no tree claimed beside it) |
| 11 | REC-20260914-X p5 (line 9, REC-20260914-X dispatch checkpoint 2 at 2026-09-14 10:20 UTC) | P5 | `48ca127540a40dee7dee62b7d1f4a8386174d0ba` | — | **COMMIT VERIFIED** | log tree 1d86a801fbdfa472ed478c809b61b39c90d71a8a (no tree claimed beside it) |
| 12 | REC-20260914-X p5 (line 9, REC-20260914-X dispatch checkpoint 2 at 2026-09-14 10:20 UTC) | P4 | `7b0303f182289142bc0d79794aa95a1823b12a10` | — | **COMMIT VERIFIED** | log tree cdf240b8f25f82b0fb419fbab806be06dabc39b2 (no tree claimed beside it) |
| 13 | REC-20260914-X p7 (line 13, REC-20260914-X dispatch checkpoint 3 at 2026-09-14 10:26 UTC) | P5 | `e8357c3d236c4c837a27920c96ae8c7301c447c4` | — | **COMMIT VERIFIED** | log tree 1112033545960cc750f0f4a5cf7707666745ab24 (no tree claimed beside it) |
| 14 | REC-20260914-X p7 (line 13, REC-20260914-X dispatch checkpoint 3 at 2026-09-14 10:26 UTC) | P4 | `d6157cf39f07aa60abf209e32c46ae0d57535c7d` | — | **COMMIT VERIFIED** | log tree 398fc28d76ffa1684d6505cb368a9e3ae12460ba (no tree claimed beside it) |
| 15 | REC-20260914-X p8 (line 15, REC-20260914-X closed at 2026-09-14 10:34 UTC) | P6 | `96ca2eb` | — | **COMMIT VERIFIED** | resolves to 96ca2eb3188beeb3ca1d399cddb203a9d38ec8a9, tree da1d4bff5619b9a189575e11058c3b7a66d6be7b (no tree claimed beside it) |
| 16 | REC-20260914-X p8 (line 15, REC-20260914-X closed at 2026-09-14 10:34 UTC) | P3 | `f25b4a93723c88a40ade062c065df20fd22490e9` | `908d0f5ee884a989772eecd00cb68aaf44bb8a87` | **PAIR VERIFIED** | log tree 908d0f5ee884a989772eecd00cb68aaf44bb8a87 |
| 17 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P1 | `958f2f4173da679283388c1820d218a209dffdbb` | `79cbdfe9d1a03192d4bea8d84dc605d7862abdb8` | **PAIR VERIFIED** | log tree 79cbdfe9d1a03192d4bea8d84dc605d7862abdb8 |
| 18 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `96ca2eb` | — | **COMMIT VERIFIED** | resolves to 96ca2eb3188beeb3ca1d399cddb203a9d38ec8a9, tree da1d4bff5619b9a189575e11058c3b7a66d6be7b (no tree claimed beside it) |
| 19 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `7bff688` | — | **COMMIT VERIFIED** | resolves to 7bff688f89cbb7cdbb5a6f76c63fed6db8cb80e9, tree 9b354336e5cc54c20e63a0795f69de7914a42c85 (no tree claimed beside it) |
| 20 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `9967e3c` | — | **COMMIT VERIFIED** | resolves to 9967e3c8419506bfc6e147bdcf49592d255662e0, tree ff9c3f911a3929345c12eaa9faa8a3979e29badf (no tree claimed beside it) |
| 21 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `a1e516c` | — | **COMMIT VERIFIED** | resolves to a1e516c54673c8a3ea2968ca3362ec6d1d725fb8, tree 3e106bbe980a0c3d4c52b3679e7c6bed7200f214 (no tree claimed beside it) |
| 22 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `e9d9c47` | — | **COMMIT VERIFIED** | resolves to e9d9c47d96f45f8e9f356d7300ff7a8b4796b044, tree ea54c83cfa753dc5f702b9f979a68580a49cc757 (no tree claimed beside it) |
| 23 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `48ca127` | — | **COMMIT VERIFIED** | resolves to 48ca127540a40dee7dee62b7d1f4a8386174d0ba, tree 1d86a801fbdfa472ed478c809b61b39c90d71a8a (no tree claimed beside it) |
| 24 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `73d193f` | — | **COMMIT VERIFIED** | resolves to 73d193f8fc4756afdc7b7379a0b546bbbaf5986d, tree 2620a66f0a6d53d815dc8ac38fac41ac7eee9d37 (no tree claimed beside it) |
| 25 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `7b0303f` | — | **COMMIT VERIFIED** | resolves to 7b0303f182289142bc0d79794aa95a1823b12a10, tree cdf240b8f25f82b0fb419fbab806be06dabc39b2 (no tree claimed beside it) |
| 26 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `e8357c3` | — | **COMMIT VERIFIED** | resolves to e8357c3d236c4c837a27920c96ae8c7301c447c4, tree 1112033545960cc750f0f4a5cf7707666745ab24 (no tree claimed beside it) |
| 27 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `d99ab67` | — | **COMMIT VERIFIED** | resolves to d99ab67c76f433c53e1eba0cd2beb6798f62d98c, tree 2f9da90b8671019a1ef774a7fed07ab37d42d2be (no tree claimed beside it) |
| 28 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `d6157cf` | — | **COMMIT VERIFIED** | resolves to d6157cf39f07aa60abf209e32c46ae0d57535c7d, tree 398fc28d76ffa1684d6505cb368a9e3ae12460ba (no tree claimed beside it) |
| 29 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `63ae4b6` | — | **COMMIT VERIFIED** | resolves to 63ae4b63942c919ab957f643c0be9b83420ff40b, tree 9a94b00c1006d61e8eda80dec67ce018dc34f746 (no tree claimed beside it) |
| 30 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `ff29eca` | — | **COMMIT VERIFIED** | resolves to ff29eca5fa80f3a8cb3f5981be18498044033243, tree 791747e76c39f2772f41da8e30d7d2c8d1be4677 (no tree claimed beside it) |
| 31 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `e1a6f1a` | — | **COMMIT VERIFIED** | resolves to e1a6f1ae01e1b6c7b233c46f5122c0ebeb4233b9, tree 87f17faf38612a75a4bcb92a8550c12c3490b23e (no tree claimed beside it) |
| 32 | REC-20260914-X p9 (line 17, REC-20260914-X verified publication at 2026-09-14 10:36 UTC) | P6 | `f25b4a9` | — | **COMMIT VERIFIED** | resolves to f25b4a93723c88a40ade062c065df20fd22490e9, tree 908d0f5ee884a989772eecd00cb68aaf44bb8a87 (no tree claimed beside it) |

## Reported separately, as the check requires

**Identities that do not appear in the log at all: 0.**

Every extracted identity resolved in `evidence/git-log-branch.txt`.

**Short ids resolving to more than one commit: 0.**

Each extracted 7-character id resolves to exactly one commit in the log.

**Pairs that appear but do not match: 0.**

No commit in either receipt is published beside a tree other than the one
the log records for it.

## Does every published pair verify?

**Yes.** All **8** commit+tree pairs published in the two receipts verify
against the branch log: each commit appears in the log and the tree the
receipt names beside it is the tree the log records for that commit. The
further **24** identities published without a tree beside them — 6 full
40-character ids and 18 7-character short ids — each resolve to exactly one
commit in the log. No identity is absent, no short id is ambiguous, and no
pair is mismatched. This is a clean result, not an incomplete one: the
recount above shows the patterns consumed every git-id-shaped string in both
files.

## Counts, each with the file or command that produced it

From `python3 check/commit_tree_join.py` over the three files named above:

* identities extracted and joined: **32**
* of them full 40-hex commit ids: **14**; 7-hex short ids: **18**
* rows carrying a tree beside the commit (commit+tree pairs): **8**
* pairs verified: **8**; commit-only rows verified: **24**
* not in the log: **0**; ambiguous short ids: **0**; mismatched pairs: **0**
* distinct commits named across both receipts: **20** of the **122** in the log

Auxiliary, and **not** a verdict of this join: each receipt states how many
commits its decision spans, and the same script counts log lines between two
short ids, inclusive of both ends, in the log's own order.

* REC-20260914-U p8 (line 15): "in seven commits from `ad3e347` through the
  closing one". `ad3e347` to `f353ac4` is **7** log lines; `ad3e347` to
  `d6b7e30`, the commit that same paragraph verifies, is **8**.
* REC-20260914-X p9 (line 17): "in fifteen commits from `96ca2eb` through the
  closing one", followed by an enumeration of fifteen short ids ending at
  `f25b4a9`. `96ca2eb` to `f25b4a9` is **15** log lines; `96ca2eb` to
  `958f2f4`, the closing commit that paragraph verifies, is **16**.

X's own enumeration fixes what "through the closing one" counts in these two
sentences: the commits before the closing one, the closing one being verified
beside them. Read that way both counts agree with the log. Read as inclusive of
the closing commit, both would be one higher than stated. Which reading each
sentence intends is not settled here, and no verdict above turns on it: a commit
count is not a commit identity.

## Hex strings the patterns did not treat as commit or tree identities

Named so a reader can tell a clean check from an incomplete one.

* **64-character sha256 digests: 34 occurrences, 14 distinct.** These are file,
  material, runner and `plan_id` digests, not git object ids, and the 40-hex
  pattern excludes them by construction.
* **Truncated digests written with an ellipsis: 2.** `aadea004…` (REC-20260914-X p2), `ccbb1165…` (REC-20260914-X p2)
* **Other isolated hex-looking runs of length 8-39 or 41-63: 1.** `20260914` (REC-20260914-U p1; REC-20260914-U p2; REC-20260914-U p3; REC-20260914-U p4; REC-20260914-U p5; REC-20260914-U p6; REC-20260914-U p7; REC-20260914-U p8; REC-20260914-U p9; REC-20260914-X p1; REC-20260914-X p2; REC-20260914-X p3; REC-20260914-X p4; REC-20260914-X p5; REC-20260914-X p6; REC-20260914-X p7; REC-20260914-X p8; REC-20260914-X p9)
* **7-character runs of digits only, excluded from P6: 0.** none

The digits-only exclusion in P6 costs nothing here: of the 122 short ids in the
log, 0 are digits only.

## Identities in either receipt that this pattern would not have caught

The patterns read hex strings. What they cannot read is an identity a receipt
refers to without writing it down, and that is the whole of the gap here.

1. **Commits referred to collectively and never written.** REC-20260914-U p8
   (line 15) says its decision ran "in seven commits from `ad3e347` through the
   closing one" and names only the first and the last. 6 commits of that span
   appear in no extracted identity, and no pattern over the receipt text could
   have caught them because the receipt does not contain them. From the log they
   are:
   * `f353ac4` f353ac40775efb4133ed429c99bc16dab7e4094d — C001 dispatch complete: all 240 coordinates, audit, and the comparison table
   * `c18d723` c18d72327ca5af3d7e7d7f7066209f8364bd277c — C001 dispatch checkpoint 4: records through wave 43
   * `865a800` 865a8004302ff433957d84ead284877d7c9d4bbb — C001 dispatch checkpoint 3: records through wave 33
   * `ee22ee4` ee22ee4852fb71d32ba84027cd04a23f342c248d — C001 dispatch checkpoint 2: records through wave 25
   * `1629af7` 1629af7b3f40b0cdb24533e9f6b30e37686531d1 — C001 dispatch checkpoint 1: records through wave 14
   * `04654a3` 04654a354c4b99d61906162d92e44a7a3976243b — Record the REC-20260914-U publication and freeze outcome
   The same check over REC-20260914-X's span `96ca2eb`..`958f2f4` leaves **0**
   commits unnamed: that receipt enumerates its whole span.

2. **A digest written truncated with an ellipsis.** REC-20260914-X p2 (line 3)
   carries `ccbb1165…` and `aadea004…`. Both are sha256 prefixes rather than git
   ids, so nothing is missed here, but a commit or tree abbreviated in that form
   would pass P1-P6 unread.

3. **An abbreviation of a length other than seven.** Git accepts any unambiguous
   prefix; P6 reads exactly seven. The isolated 8-to-39-character hex runs in the
   two files are `20260914` (the receipt-name date) and the two sha256 prefixes
   above, so no git id is lost to this — but a 10- or 12-character abbreviation
   would have been.

4. **An upper- or mixed-case id.** The patterns are lowercase-only. 0 such 7- or
   40-character run occurs in either file.

5. **Identities named in words with no hex beside them**, which are therefore
   unjoinable: "the closing one", "the publication tree", "the staging tree",
   "this working tree", "remote `claude/project-state-direction-j5rbun`" and the
   `--publish-ref origin/claude/...` argument. These name objects without
   publishing their identity.

6. **The 14 distinct sha256 digests**, excluded on purpose: a `plan_id`, a
   material digest, a runner digest and file digests are not commit or tree
   identities and the branch log carries nothing to join them against.

## What I could not determine

* **Whether the log extract itself is faithful to the repository.** Everything
  above is a join against `evidence/git-log-branch.txt`, a frozen file. There is
  no `git` in this sandbox, so I could not recompute a tree from object content,
  re-run `git log`, or read the remote ref. If a `%T` column in the extract were
  wrong, this check would report the receipt as verified. Unresolved by
  construction, and named rather than glossed.
* **Anything outside `40bd5de..HEAD`.** The extract's own header records that
  range. An identity published in either receipt but older than `40bd5de` would
  have come back NOT IN LOG as a limit of the extract rather than as a defect of
  the receipt. It did not arise — 0 rows are NOT IN LOG — but the boundary is
  real and I could not test past it.
* **Whether "seven commits" and "fifteen commits" are inclusive of the closing
  commit.** Both readings are reported above with the log lines each implies. I
  could not determine which the sentences intend, and a count is not an identity,
  so no verdict rests on it.
* **The receipts' non-git digests.** The 14 sha256 values — `plan_id`s, the
  material, the runner, the pinned provider files — are unchecked: the files they
  digest are not in this sandbox, and the branch log holds nothing to join them
  against.
* **Whether the two receipt files reproduce `docs/DECISION_LEDGER.md` verbatim.**
  The ledger is not in this sandbox, so that premise is taken as given and was
  not verified.
* **Everything the receipts assert that is not an identity** — file counts,
  insertion counts, token counts, test counts, timings, per-coordinate outcomes.
  None of it is checkable from a `%H %T %h` log and none of it was checked.

