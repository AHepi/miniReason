# Current research status

## The automated loop's waves 0-2 checkpoint was verified and refused — 2026-09-14

REC-20260914-AA set out to make the automated end-to-end harness loop **recoverable work on this
branch** rather than an ephemeral scratchpad directory, per AGENTS.md's "publish small reviewed
checkpoints". **It did not publish it.** The transplant was made, every file confirmed
byte-identical to the frozen snapshot, `pyproject.diff` applied cleanly, and all seventeen import
targets returned OK under `python3 -W error`. Then the suite this ledger records reported **`Ran
2610 tests in 233.947s`, `FAILED (failures=3, skipped=2)`**, so under the receipt's own declared
gate nothing was staged, the transplant was removed, and the restored tree reports **`Ran 1450
tests in 193.542s`, `OK (skipped=1)`** — the figure already on record. None of the three failures
is pre-existing.

**What actually completed.** The opening receipt, published and verified at
`02c639e12b6499d045e0b0b06f2fee18b644c9d2` / tree `faf174cfa205cbada4459ad24af71c42d0c1099c`,
which declares the checkpoint's limits before action: never run, no provider call authorised,
wave 2 implemented but **not** integrated, waves 3-6 unbuilt, the pre-registration bundle a draft,
and the two declared narrowings of `use_relation_h005` applied nowhere. Then the verification
itself, and its two findings, recorded as errata with their commands and their evidence:
**`OPS-20260914-LOOPSUITE`** (a `no_sockets()` guard in `tests/loop/test_roles.py` entered from six
concurrent threads reinstalls its own patch of `socket.socket`, `socket.create_connection` and
`minireason.provider_openai_compat._open` process-wide, failing two pre-existing provider tests;
and `data/plan_8a_mirror.json` pins the C001 `PLAN.md` at the digest it had before `2d7239a`
appended §15 to it, 88 added lines and nothing edited) and **`SRC-003`** (the `use_relation_h005`
reading banner cites `fw5-vs-harness-spec-review.md` and `NOTES.md`, two staging basenames that
name no tracked file; the instrument is **not** edited and the twenty-four published analysis
artifacts keep the banner they carry). Credential scan: 53 candidate files and 13 repository
files, **0 matches**. **No provider call was made and no credential was read.** Nothing published
was modified.

**Next authorized task**, in order. (1) The two named repairs: make `no_sockets()` safe under
concurrent entry with a regression test asserting the three globals are restored, and re-pin
`plan_8a_mirror.json` against this branch — which moves `loop_plan_id` and therefore belongs to
the receipt that mints the pre-registration. (2) Re-run the full suite to a clean `Ran N tests …
OK` line and publish the checkpoint. (3) Wave-2 integration: items **24-28, 42 and 48-54** of the
staging integration list, and `WAVE2-INTERFACE.md`, which does not exist. (4) Waves 3-6: trial
runner, marker, driver, report, operator page. (5) Revise the pre-registration bundle against its
own review's thirteen blockers **PR-01 through PR-13** and re-mint it; its pins are known stale.
(6) A dry run. **Only then** is any live run a question, and it would be a new decision with its
own receipt — no provider call is authorised by anything above.

**Cadence, recorded truthfully and not backdated.** During today's scratchpad work on the loop the
five-minute verified-push rule **was not met for several hours**: the implementation, its reviews,
the design of record and the pre-registration draft were all built in an ephemeral directory with
no verified push behind them, and a container restart today would have taken them. This receipt is
the recovery, and it is a partial one — the record is now on the branch and the code is not.

## F002 occurrence-03 dispatched — the 300-second close recurs — 2026-09-14

REC-20260914-Z added a **third occurrence** to the published F002 study and dispatched it, to ask one
question: does the `"Remote end closed connection without response"` that ended occurrence-01's `response`
node at **300,270 ms** recur? **It does.** Occurrence-03 re-ran the same `mini_fcl` arm chain from `account`
on `ollama/glm-5.3` at `max_tokens` 32,768, `timeout_seconds` 600 and `seed` 7, with an `arms.json`
byte-identical to occurrence-01's, and its `objection` node FAILED with the same error at **300,453 ms**
against an applied 600-second clock.

**A re-run of an identical `arms.json` does not get a new `plan_id`, and this was recorded before the run
rather than discovered after it.** `plan_id` digests the material, the frozen arms and scope, the runtime and
provider pins and the runner, and carries **no occurrence name**, so occurrence-03 minted occurrence-01's own
`9aa92a837569bd56a86b172eb56dd80dbc69c519a86286d3387b020c2709a0d5`; `plan.json`, `material.json` and all
three manifests are byte-identical, and so is `wave0001`'s `account` request hash. The runner has no
plan-level replay refusal to evade, so the seed stayed at 7 deliberately — changing it to manufacture a
distinct identity would have changed the condition under observation. Occurrence-03 has its own **occurrence**
identity and shares occurrence-01's **plan** identity by construction.

**Three calls spent of five authorised, in two rounds and not four: 2 COMPLETE, 1 FAILED, 2 never
dispatched.** `account` COMPLETE, `"stop"`, 12,489 completion tokens, 114,364 ms; `rival` COMPLETE,
`"stop"`, 19,700 tokens, **234,864 ms** — past the 180-second wall the endpoint record declares, and the
third F002 call to run past it and return; `objection` **FAILED**, `TRANSPORT_OR_RESPONSE_ERROR`, no
`finish_reason`, no usage, zero bytes, **300,453 ms**. The no-retry truncation rule then ended the arm, so
`response` and `carry` were never dispatched. **Neither declared bound was reached**: `finish_reason:
"length"` occurs zero times and the largest completion is 19,700 of 32,768.

**The wall is undeclared and sits below the declared clock.** Five closes carrying that exact error string
are now known, inside a **183-millisecond band around 300.3 s**: 300.270 s and 300.453 s on
`ollama/glm-5.3` (F002 occurrences 01 and 03, 63 minutes apart, at *different* nodes), and 300.286 /
300.348 / 300.377 s on `ollama/kimi-k3` from a separate worker process also at 600 s and 32,768 — those
three cited in REC-20260914-Z with their provenance and their limits, being another harness's untracked
transcripts and **not** `minireason.call.v2` records. Two model families, two client processes, two different
fork5 nodes. **A host gateway closes a request still open at about 300 seconds, so F002's declared
600-second clock cannot be exercised past 300 s on this host, and the arithmetic that justified 600 s
describes calls this host will close before the slower half of them can finish.** Why it closes is **not
known and is not guessed at**, and **no retry was made at any layer**.

The [analyses](../experiments/analyses/F002-fork5-raised-clock-2026-09-14/README.md) carry occurrence-03's
audit and both instruments at full scope. The import exits 0 with custody **verified 18 of 18**: 26 events,
4 artifacts, **0 `att` edges, 0 warrants**, 52 references of which all 52 resolved and none dangled, and **no
error-severity residue fired at all**. FCL-1 surface on the two nodes that reached the importer: `read_fcl1`
**2 of 2**, no `parse_failure`, no `schema_failure`, no `unavailable_decode_failure`. The use table has **0
rows** (`cross_document_rows` is 0) with every interpretive column empty.

**F001 occurrence-07's residue is still open.** `mini_fcl/response` and `mini_fcl/carry` have **no terminal
COMPLETE record anywhere**: three occurrences have now ended that arm early, for three different reasons at
three different nodes, and that is reported as the outcome rather than dressed as anything else.

**Nothing semantic follows from any of it.** A closed socket is a resource fact and never a verdict; no
family is ranked, and no F001 or F002 record is modified, relabelled, repaired, re-sent or superseded.
Suite: `PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests` reports **Ran 1450 tests, OK
(skipped=1)**. Dispatch held `OLLAMA_API_KEY` alone with `DEEPSEEK_API_KEY` removed, at most **two** requests
in flight on a credential shared with a concurrent worker battery, zero retries at every layer, each round's
inputs committed, pushed and read back before that round was sent.

**No further F002 provider call is authorized.** A fourth occurrence, a retry of either closed coordinate, or
a run under a clock chosen against the ~300-second wall would each be a new decision needing its own receipt.
**The next authorized task is still the reading, which is root's and is not done.** Publication to `main`
remains pending owner merge.

## B001 published as a register, its dispatch refused — 2026-09-14

REC-20260914-Y published **B001, the commissioned bare-model and native-reasoning matched comparison, as an
offline register that corrects its own commissioning premise**, and refused its dispatch. **Zero provider
calls were planned and zero were made.** B001 was commissioned on the premise that no published study yet
has a bare-model arm. **The committed bytes refute that premise, and the gap this programme has is a reading
gap, not a dispatch gap.**

Published at `bfc5c8e7e18ca4797566a742f94df3d4b69df1f5` / tree
`03937a46aa681b69caf7ba4203c195c440c8cc6d`, after the opening receipt alone at
`228e33ff931b69994e40d333701f6efac905421b`:

* the register [`B001-bare-and-native/PLAN.md`](../experiments/diagnostics/B001-bare-and-native/PLAN.md)
  with its frozen proposal `proposal-bare-deepseek.json`;
* the design note [`b001-reasoning-persistence-2026-09-14.md`](design/b001-reasoning-persistence-2026-09-14.md)
  — which the register refers to by its staging basename `REASONING_PERSISTENCE.md`, the two staged
  documents having been copied byte-for-byte without editorial repair;
* the offline instrument `tools/arm_inventory.py` with `tests/test_arm_inventory.py`, 34 tests;
* its output, regenerated in the publication tree and not copied, at
  [`B001-arm-inventory-2026-09-14`](../experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md) —
  11 occurrences, 122 files digested, 101 terminal coordinates, 9 proposal rows.

**The facts were checked against bytes before the register was published, not carried over from its own
prose.** H005 occurrence-01 declares all five arms — `bare`, `native`, `matched`, `mini_prose`, `mini_fcl` —
and carries 17 terminal artifacts beside 17 provider call records; F001 occurrence-01 declares `bare`,
`native`, `mini_fcl` and `mini_prose` with `kind` and `surface` per arm and has 12 call records; and **every
one of F001's eight occurrences declares a `bare` arm with a terminal `daily/bare/cycle01/answer`
artifact**. A BARE proposal at F001 occurrence-01's own conditions is identical to the published arm on
every compared field.

**The dispatch is refused for three independent reasons**: re-sending arm (a) or (b) is a replay the runner
refuses (`NO_REPLAY`); `graph_import_h005._Node.surface` tests `coord.arm in FCL_SURFACE_ARMS` with
`FCL_SURFACE_ARMS = ("mini_fcl",)`, an exact arm-**name** test, so of five published arms the permitted
instrument reads exactly one and a bare-shaped arm can never be read by it; and six confounds move at once
from a one-call arm to the five-call chain, at N = 1 per arm with no replicate baseline. **No claim is made
that the comparison is uninformative** — the claim is that it already exists in published bytes and its
obstacle is an instrument.

**On reasoning persistence the recommendation is that the text stays unpersisted.** A digest-only successor
transport is specified and deliberately not written. The step that costs nothing and has never been taken is
already in the tree: `usage.completion_tokens_details.reasoning_tokens` is **2,979** at F001 occurrence-01
and **886** at H005 occurrence-01, absent from both `bare` records, whose `messages` are byte-identical to
the `native` ones.

Two problems are promoted under `PROBLEM_PROMOTION.md`'s discipline, which endorses no diagnosis: **B001-P1**
the reading gap, and **B001-P2** reasoning legibility, whose unresolved component is an owner decision about
provider terms that no agent may take.

**No further B001 provider call is authorized.** Only two things reopen it: a reading route for prose
single-document arms (B001-P1), or a completed Mini chain at 32,768/600 — which F002 occurrence-01 can never
supply, its arm being ended by a FAILED node. **The next authorized task is the reading, which is root's and
is not done**, and its sharpest available piece needs no code and no call: read H005 occurrence-01's
`matched` arm against its `mini_prose` arm on the four C001 §8a registers.

## F002 published and dispatched — 2026-09-14

REC-20260914-X published a **second successor runner** for the H005 multi-provider fork and a new
pre-registration, F002, and dispatched it: `tools/multicycle_commitment_study_multi_v3.py` (a byte copy of
the published v2 with seven `# V3:`-marked differences in eight hunks, proved line for line by
`tests/test_multicycle_commitment_study_multi_v3.py`), the register
[`F002-fork5-raised-clock/PLAN.md`](../experiments/diagnostics/F002-fork5-raised-clock/PLAN.md), its
material, two provenance scripts each re-checkable with `--check`, and two occurrences under `plan_id`
`9aa92a837569bd56a86b172eb56dd80dbc69c519a86286d3387b020c2709a0d5` (`ollama/glm-5.3`) and
`a59debaf6382ce7c01c4c07d14894890736e2a960b66d4323f9eb84ac72b1163` (`ollama/kimi-k3`). The register, the
material, both `arms.json`, both frozen plans and all six manifests were published and the remote verified
**before the first provider call existed**, and each wave's inputs were published before that wave was sent.

The one behavioural difference from v2 is a **per-arm wall clock**, declared in `arms.json` beside the
ceiling and applied to the resolved `Endpoint` **value** by `dataclasses.replace` at dispatch.
`src/minireason/data/endpoints.json` is a pinned published file that C001's two occurrences and all eight
F001 plans hash into their own identities and it is **never written**; a dispatch that did not apply the
declared clock is refused as `TIMEOUT_NOT_APPLIED` before any provider is constructed. 600 seconds is the
transport's own validation maximum (`Endpoint.__post_init__` admits 1…600 and refuses 601), reached rather
than invented.

**The dispatch is finished: nine calls spent of ten authorised, 8 COMPLETE, 1 FAILED, 1 never dispatched**,
in four rounds of 2 / 4 / 2 / 1, one process, `OLLAMA_API_KEY` alone in its environment with
`DEEPSEEK_API_KEY` removed, at most five requests in flight process-wide, zero retries at every layer. Each
wave's inputs were committed, pushed and read back before that wave was sent.

**Neither declared bound was reached.** `finish_reason: "length"` occurs **zero** times; the largest
completion is **23,257 tokens of 32,768** and the longest call that returned is **223,839 ms of 600,000**.
Three calls ran past the 180-second wall the endpoint record declares and returned — occurrence-01
`objection` at 223,839 ms, occurrence-02 `response` at 188,623 ms and occurrence-02 `carry` at 196,250 ms —
and two of those, `glm-5.3 objection` and `kimi-k3 carry`, are precisely the coordinates F001's occurrences
07 and 08 lost as `TRANSPORT_OR_RESPONSE_ERROR` at 180,368 ms and 180,456 ms.

**One coordinate FAILED, and not on the clock.** occurrence-01 `mini_fcl/response` ended at **300,270 ms**
with `"Remote end closed connection without response"` against a declared and applied 600-second clock —
a *third* resource wall, distinct from F001's 8,192-token ceiling and from its 180-second read timeout.
Why the remote closed is not known and is not guessed at, and no retry was made. The no-retry truncation
rule then removed occurrence-01's `carry`, which is the tenth authorised call and was never dispatched.
**F002 therefore closes two of the four coordinates it was built to reach and not four**, and says so.

The [analyses](../experiments/analyses/F002-fork5-raised-clock-2026-09-14/README.md) carry the two published
instruments at full scope plus each audit. Both imports exit 0 with custody **verified 18 of 18** on each
occurrence. FCL-1 surface on `mini_fcl`: `read_fcl1` **3 of 3** on `ollama/glm-5.3` and **5 of 5** on
`ollama/kimi-k3`, no `parse_failure`, no `schema_failure`, no `unavailable_decode_failure`. Both use tables
have **0 rows** — every authored reference resolved intra-document or not at all — and all four interpretive
columns are empty, which here is no rows to fill. There are **no `att` edges and no warrants** on either
occurrence, so every `accepted` label is accept-by-position and no `refuted` label can arise.

**Any difference between F002 and any F001 occurrence is a resource observation, never a semantic one.** No
F001 record is modified, relabelled, repaired, re-sent or superseded, and nothing was written inside
`F001-fork5-multifamily/`. Suite: `PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests` reports
**Ran 1416 tests, OK (skipped=1)**.

**Next authorized task is the reading, which is root's and is not done.** F002's eight COMPLETE artifacts
and their commitment surfaces are published and unread, beside the thirteen C001 juxtapositions and ninety
use-table rows that remain unread. **No further F002 provider call is authorized**: a third clock, a retry
of the connection-closed coordinate, or a re-send of occurrence-01's arm would each be a new decision
needing its own receipt, and none is taken here. Publication to `main` remains pending owner merge.

## Session orchestration report published — 2026-09-14

REC-20260914-W refreshed the staged session orchestration report so that every statement in it is true of
the published record, and published it at
[`reviews/session-orchestration-report-2026-09-14.md`](reviews/session-orchestration-report-2026-09-14.md)
(VERIFIED `dc5491e0e6d992ecd2e36b2f6c2adf7e854fe91c` TREE `7034b1266a8aca02b39d368d00e10a1d131e2c9c`). The
draft had been written at HEAD `f50db28`, before REC-20260914-U and REC-20260914-V existed, and described
C001 as untracked, unreceipted and undispatched; that section is rewritten from the published receipts,
`audit.json`, `comparison.json` and the provider records of both occurrences, and the branch facts, the
receipt range, the suite figure (**1397 OK, skipped=1**) and the two source identities are re-measured.

The report adds one new section, **"Automated end-to-end loop: decision record"**, recording the owner's
standing requirement that the harness run end to end with no human in the loop (ruling 6, a human being an
optional appellate and never a required step), the three-angle design competition and the synthesis that
won it, the 24-module wave plan, and the claim ceiling of an automated run — a reading is a registered,
attackable judge-role artifact, never a finding and never FW5:628's witness; unresolved is first-class and
reinstates by computation; no count is a warrant. **None of that work is published**: its wave 0 exists
only in an isolated staging clone and every sentence about it is marked *Staged*.

Every sentence of the report is marked **Measured**, **Interpretation** or **Staged**. It adds no reading,
fills no cell and evaluates no falsifier.

**Next authorized task is unchanged: the reading, which is root's and is not done.** Thirteen C001
juxtapositions and ninety use-table rows are published and unread. No further C001 provider call is
authorized. Publication to `main` remains pending owner merge.

## C001 occurrence-02 completed — 2026-09-14

REC-20260914-V published a **successor** driver and a second occurrence of the frozen C001 contrast-triple
study on one cell at a raised ceiling: `tools/contrast_triple_study_v2.py` (a byte copy of the published v1
with eight `# V2:`-marked differences, proved by `V2DiffProof` and `V1Parity`), the material
[`material-occurrence-02.json`](../experiments/diagnostics/C001-contrast-triple/material-occurrence-02.json)
and the occurrence at
[`occurrence-02/`](../experiments/diagnostics/C001-contrast-triple/occurrence-02), under `plan_id`
`1d9f47acdc692146792e354afdd9c6944036cb7d55bd83cc32c905e7c4ffeb83`. The plan, preflight, material, the
85-row correspondence table and all eight briefs were published and the remote verified **before the first
provider call existed**.

What was dispatched: **20 calls and no more** — endpoint `deepseek-flash`, arm `fcl`, four cases, five
replicates, in four single-key waves of five on `DEEPSEEK_API_KEY`, zero retries, write-once records, at
`max_tokens` 32768 and `timeout_seconds` 600. Result: **20 of 20 COMPLETE**, every case 5/5, no failure code
of any kind, no `finish_reason: "length"`, no read timeout, one envelope repair. `completion_tokens`
5783…15470 (total 207,238), `reasoning_tokens` 3733…12470 (total 159,324), `prompt_tokens` 102,445.
Fifteen of the twenty exceeded 8192 completion tokens.

That is a **resource** observation and not a semantic one: it shows the FCL-1 envelope fits beside this
model's reasoning at 32768, and says nothing about the four cases. **Occurrence-01 is unchanged** — its
nineteen unusable `fcl` cells stay unresolved, its denominator is not repaired, and no reader may substitute
occurrence-02's cells for its missing ones. Its PLAN §5 ground that `deepseek-flash` "sends no reasoning
on the wire" stays published and stays false; the correction is in PLAN §15 and REC-20260914-V.
Occurrence-02's prose arm is frozen and published but was never dispatched.

**Next authorized task: the reading, which is root's and is not done.** Root reads
[`occurrence-02/COMPARISON.md`](../experiments/diagnostics/C001-contrast-triple/occurrence-02/COMPARISON.md)
with `juxtaposition/deepseek-flash__fcl.md` beside it, writes the within-ORIGINAL replicate spread on all
four registers first, and only then fills the marks; the same is still owed for occurrence-01's twelve
juxtapositions. No agent has filled a column, proposed a reading or evaluated a falsifier, and no count in
these receipts warrants one (FW5:851). No further C001 provider call is authorized: a third ceiling would be
a new pre-registration with its own `plan_id` (PLAN §13). Publication to `main` remains pending owner
merge.

## H005 active preparation — 2026-09-14

The user redefined a cycle as one complete template invocation and authorized up to five cycles per selected chain. Root has published the [current research contract](reviews/multi-cycle-research-contract-2026-09-14.md), [earliest recovered commitment-interface interpretation](reviews/commitment-interface-source-2026-09-14.md), [FCL-1 language proposition](reviews/fcl1-language-proposition-2026-09-14.md), and [H005 protocol](../experiments/diagnostics/H005-open-prose-commitments/PROTOCOL.md).

H005 begins with three complete invocations per problem across daily life, complex physics, philosophy and sociology. Three templates contain five, six and seven calls and are ordered by domain-specific mechanism hypotheses. Five arms compare bare and native one-call continuation, matched multi-call prose outside Mini, Mini free prose and Mini FCL-1. The initial schedule permits 240 unique calls if all chains remain operational. No new H005 provider call has yet run.

Problem prose contains no answer key, scoring rule or seeded error. Commitment interfaces distinguish what taking content up entails from the prose body. FCL-1 adds typed, fallible references and scoped commitments; its advantage is unestablished. Root performs all scientific and acceptance reviews. Agents implement and run bounded offline checks only.

Next: finish and review the new outer fixture and its focused offline tests, freeze exact runtime/material identities, then run the three-cycle comparison with at most five concurrent DeepSeek requests. Preserve every attempt, partial and failed criticism. A fourth or fifth invocation requires a prospective reason grounded in the content of the first three, not a favorable-result target. Full durable Mini scheduling remains unqualified on Windows; H005 uses the canonical compiler/reducer/renderer within an explicitly declared memory-backed fixture.

The completed H004 findings and all older checkpoints below remain historical evidence. Their “no successor selected” and prospective next-question wording is superseded by this H005 section. Never replay H003/H004 coordinates.

## H004 completed and reviewed — 2026-09-13

The [terminal report](../experiments/diagnostics/H004-partial-language-continuation/REPORT.md), [final custody audit](../experiments/diagnostics/H004-partial-language-continuation/final-custody-audit.json), and [candidate card](reviews/prose-audit-return-candidate-2026-09-13.md) are published. All five arms cover 20 model steps across H003/H004: 100 unique calls, 50 complete answers and 50 preserved partial contributions. Twenty steps here are four five-stage blocks, not twenty complete blocks.

H004 made 65 new calls: 20 complete and 45 partial, zero stopped or pending. New reported usage: 951,170 prompt + 253,109 completion = 1,204,279 tokens. Combined H003/H004: 1,656,157 tokens. All original observations and protected source/plan/record trees remain unchanged. The audit verified every new canonical request/trace pair and scanned 4,081 files without credential-pattern matches. Provider sessions have exited and root cleared the session-store credential. No additional provider call or successor study is running or selected.

The candidate is **prose_audit_return_v1**, best suited to supervised auditing of prose specifications and stateful operating rules. It combines account, criticism, criticism of criticism, operative return and fresh use with selected earlier targets. Continuity supports later error discovery without requiring perfect memory. Root did all scientific reviews; Astra implemented/tested the helper and supplied operational drafts and mechanical assistance.

Every final arm computed correct contract D/A sets, but explanations and criticisms retained errors. Models sometimes invented missing inputs, truncation or reconstruction despite exact preserved evidence. Neither WHL nor RSS, including prose conversion, has established an advantage over prose. Historical novelty, reliable autonomous correction, a native-reasoning advantage, universal recursive capacity and full durable Mini qualification remain unestablished.

**Next scientific question:** whether a specific warranted correction made operative changes later use, compared with the same content archived outside the active route under matched tasks and call budgets. H004 closes at its declared study boundary, not because Mini's configuration space is exhausted. A successor needs its own question and frozen occurrence. Do not rerun any H003/H004 coordinate.

The [failure guide](errata/REC-20260913-windows-execution.md) and [operations lessons](lessons/operations.md) record the new failures and terminal boundary. AGENTS and the installed/repository operations skill already route agents to that guidance.

H003 remains closed under its original full-delivery rule: 35 calls, 30 complete/5 partial, 451,878 tokens. H004's separate partial admission is an operator intervention, not a model-authored repair or retroactive H003 success. Original E028 remains unrecovered with unknown final outcome/usage; the unavailable Android workspace export must not be requested again. H002's separate completed use/return study and conditional Linux qualification retain their historical scope.

Earlier source-led checkpoints are preserved below as history. Their prospective H003/H004 wording is superseded by this terminal section.

Updated 2026-09-13. The overarching goal is to explore Mini's configuration space and test the designated FW5 explanatory-construction account to identify gaps that can be filled. ECS 2.0 is retained as a separately identified successor hypothesis source. Language expression, formal feedback and this distinct-template chain are subset tests. See [PURPOSE](../PURPOSE.md) and the append-only [ledger](DECISION_LEDGER.md).

## Current checkpoint and next action

**Trajectory decision — 2026-09-13 (REC-20260913-J).** The user says the original workspace cannot be exported and directs useful work to continue. Root completed the [trajectory assessment](reviews/trajectory-assessment-2026-09-13.md) against the revised FW5 authority and goals. Retain the construction/use/criticism/return/fresh-use sequence, but treat E028 as a preliminary criticism-delivery diagnostic, not a complete test of Mini advantage or FW5. Missing content contrasts, matched controls and the independent theory-side challenge remain explicit.

**Completed H002 — 2026-09-13:** the separate [DeepSeek routing exercise and root review](../experiments/diagnostics/H002-deepseek-routing/REPORT.md) completed six unique calls, all stop, totaling 66,144 tokens. Original routing checks confirmed eight deliveries with two shared-prefix reuses. All ten tested event occurrences and both U1 endpoint states matched the finite oracle, including retained rows and indexes. Criticism did not improve finite correctness and propagated unsupported claims; root also records parent-position and prose contradictions. This does not complete original E028 or qualify the full durable Mini scheduler. H001 remains prepared and unrun; the user selected DeepSeek before any Luna session.

**Candidate template:** `use_and_return_v1`, currently best suited to supervised maintenance/revision of stateful procedures with protected prior behavior. SQL LEFT JOIN maintenance is the demonstrated instance, not a general performance or creativity claim.

**Candidate languages already on record:** Warehouse History Language (WHL), a Lean-based domain vocabulary, and Rival-Story Semantics (RSS), a prose semantic proposal organizing stories, viewpoints, readings and disagreements. See the [E004 packet review](reviews/E004-language-packet-review.md). Both are incomplete custom proposals; historical novelty is unestablished. RSS is a proposed fit for prose conversion that preserves assumptions and alternatives, but existing source-conditioned mappings limit claims about unfamiliar prose.

**Current user instruction — reopened 2026-09-13:** continue source-led work and consider twenty cycles, with language-assisted discovery of errors/mistaken assumptions and new problems. This supersedes the temporary no-tests instruction. Root completed the [twenty-cycle decision](reviews/twenty-cycle-error-discovery-decision-2026-09-13.md): prepare H003 with five concurrent language/prose-use policies, actual return to selected earlier targets and fresh use. Perfect memory is not an admission condition. Root performs all reviews; at most five arms/five active DeepSeek requests, with only actual dependencies ordered. H003 is not yet dispatched; original H002 history stays unchanged.

**Operational guidance:** root reviewed and published the [failure guide](errata/REC-20260913-windows-execution.md) and [reusable operations skill](../skills/minireason-experiment-operations/SKILL.md). AGENTS requires root and subagents to read the repository skill before choosing an execution strategy. An identical personal copy is installed in `C:/Users/darre/.codex/skills/minireason-experiment-operations/SKILL.md`. No validators or new tests ran after the user's stop-testing instruction. Original E028 and optional Linux fallback remain historical/pending context below; do not request the unavailable export again.

**Recovery checkpoint — 2026-09-13.** The user verified that the earlier failures were an Android-app workspace issue, unrelated to GitHub. The API permission denial below concerns only the new fallback execution route; the Windows filesystem limitation concerns only this desktop recovery host. The Windows activity logger and guarded portable entry point are repaired and tested. The [manual checkpointed recovery workflow](https://github.com/AHepi/miniReason/actions/workflows/e028-recovery.yml) and its runner are published at `b82e7da3dbfda4e43a4ca8826f406e26ee4e7339`, independently verified tree `095ae4696413c0392ae549bd4f58000f00b749e2`. Independent review accepted the runner for publication and a zero-call Linux qualification attempt; that hosted qualification has not run. The repaired checkpoint suite passed 11 tests with 3 explicit POSIX skips; Linux integration is not yet qualified.

The current token received **HTTP 403, Resource not accessible by personal access token**, when dispatching the default `preflight` workflow. If fallback qualification is selected, a repository operator must start its zero-call run from Actions. No hosted run or live recovery was started by this session. Repository `DEEPSEEK_API_KEY` availability remains unknown: secret listing was also denied, and the hosted availability check has not run. No new paid provider calls or credential-storage changes occurred.

The original cloud E028 records remain unavailable through the current checkout and exposed prior-task history. The historical four-response receipt below is not a current process observation or a substitute for original bytes. Preserve any original export if it becomes available; unknown original usage remains unknown. The separately identified `experiments/records/E028-sql-use-return-recovery-01` occurrence remains unstarted.

**Original E026 is interrupted after two calls; no Mini construction was attempted.** The [original report](../experiments/records/E026-sql-construction/REPORT.md) and raw request/response/summary records preserve direct-disabled COMPLETE and direct-native INCOMPLETE_GENERATION. Known reported usage is 13,924 total tokens. Native used the 8192 completion-token ceiling entirely as reported reasoning tokens and returned empty public content. The frozen runner stopped, leaving four arms unattempted, including selected mini-disabled. This is a resource-bound operational result, not a content verdict or completed Mini comparison.

During the earlier cloud execution, the resumed exact-host check returned HTTP 401 at 20:56:20 UTC, and actual completion requests succeeded at transport level. [Reachability](../experiments/preflights/E026-session-H-network/reachability.json) and [renewed independent preflight](../experiments/preflights/E026-session-H-verification/verification.json) are preserved separately from prior evidence. All 24 focused tests and exact plan verification pass. Runtime is Python 3.12.14 with pinned jsonschema 4.25.1 and referencing 0.37.0. That historical environment prefix was `PYTHONPATH=src:/workspace/scratch/9be47893c9a9/h-EPI/.venv/lib/python3.12/site-packages` with current `python`; no frozen code or source-repository file changed.

Original plan identity remains `f8c3ab9ecb3285ea3d1d167427e413be2a30a1583a05fd5a411210430390a197`. Do not rerun the original command: its output directory now exists and is immutable. Inspect terminal status rather than CLI exit code; the interrupted CLI exited zero. No retry, increased native allowance, alternate selected candidate or B execution has been performed.

The designated FW5 source and roadmap update, [SQL construction/use/return protocol](SQL_CONSTRUCTION_RETURN_PROTOCOL.md) and [SQL001 material](../experiments/materials/SQL001-join-construction/manifest.json) remain published and unchanged. The information-need witness shows that identical old visible results and an insertion can require different successor bags; it does not prove candidate-account use. The [Account challenge](reviews/FW5-account-skew-matrix-challenge.md) remains a failed independent absence-of-bearing argument, neither a refutation nor confirmation of FW5.

**E027 continuation is complete.** The [original report](../experiments/records/E027-sql-construction-continuation/REPORT.md) preserves two COMPLETE/stop disabled responses, exact original request equality, full selected Mini prose custody, and 10,572 reported total tokens. E026 plus E027 this session totals four calls and 24,496 reported tokens. Selected E027/mini-disabled answer SHA256 is `b5fb115264eaff0a0466ea19012b58624a2669f95c4b6e47aab545c2074268c0`. No selected output is substituted, and no original E026 call was repeated. Native comparison remains incomplete; identical one-call prompts cannot establish multistage advantage.

The [selected-account review](reviews/E027-selected-account-review.md) and [three-sample comparison](reviews/E026-E027-construction-comparison.md) are complete and published. The literal NULL-left-delete omission and alternative invariant-guided reading are independently witnessed; controls have different explicit delta omissions. No source account was repaired or substituted.

**Original E028 use/criticism-return was dispatched in the prior cloud workspace.** The [exact workflow](workflows/sql-use-return.md) and [plan](../experiments/plans/E028-sql-use-return/plan.json) bind `0e7ada3e11b348b7c3ea46805910ece3e14fdb700975e6a22b58b44c82569b5f`. Two one-cycle four-stage configurations share the same actual first use and criticism through validated replay; four returned calls plus two new archive calls give at most six unique requests. Each is thinking-disabled,8192 completion tokens, sequential/no retries. All10 focused tests, actual-source preflight and independent operator material correspondence pass. Full candidate is quoted fallible material in a frozen system message; only stage tasks and actual input ports enter Mini briefs. Initial state cannot bypass U0/U1, and criticism enters apply only in the returned condition. The frozen study was dispatched after verified publication at0dcb69ddb09907c29998b35ad0f0fdf02170d861; its original record bytes are not present in the recovered checkout or verified published tree.

**Historical observation at 2026-09-12T21:43:22.987562+00:00:** the prior cloud workspace reported 4 parseable provider response records and no terminal summary. Current recovery has not obtained those bytes or established the process outcome. Do not recreate, replay or overwrite the original occurrence.

**Superseded recovery instruction:** the earlier request for an original-workspace export is closed by the user as unavailable. Follow the trajectory decision above. If actual frozen DeepSeek execution is selected later, preserve the separate occurrence identity and qualify a supporting host; the current GitHub dispatch token still lacks permission. No native retry or successor scientific experiment is automatic.

E025-retry-02 remains a partial experiment preserved at `e36c03bd26afffa639ea74a6068dd9b6dd90a373`: nine request records, six COMPLETE/stop public responses, three completed arm records and no terminal summary. Known completed-response usage is 146,174 total tokens; additional attempted-call costs are unknown. Its [recovery supplement](../experiments/records/E025-chain-successor-retry-02/RECOVERY.md) records the network-policy interruption after explicit payload/destination approval. No runner remains active and no E025 retry or third episode is selected. Preserve E023/E024 and every interrupted original record.

| Artifact | Verified state |
|---|---|
| [E023](../experiments/records/E023-reason-no-return-retry/REPORT.md) | Four arms, eight complete calls; [review](reviews/E023-no-return-review.md) published. Returned account unnecessary for the witnessed cued arithmetic; source/interpretation defects remain. Do not rerun. |
| [E024](../experiments/records/E024-chain-construction/REPORT.md) | Six arms, eighteen complete calls, 404,937 total tokens. Record remote 9c876cc21686bd0e309449a4ca7dcbd9b737539c; [review](reviews/E024-construction-review.md) remote 0d828bd7f7d4279ba6eef94682a6d0ba6f5c13fb. Do not rerun. |
| [C001 handoff](../experiments/materials/C001-handoff.json) | Actual whole selected A bundle; freeze/verification pass. Published at 90f0766dad2e9e578b50fc77b81957b2139df3cd. |
| [E025 plan](../experiments/plans/E025-chain-successor.json) | Plan fae51c195662a65dd70c7f096559c24c894e50567a41e30d8b955ab571e04727; published at c4dd5aa2dd7fc1dc8c0c1659aca9d14d94be709d. Six controls, ten calls, distinct locate/discriminate template, one cycle. |
| [E025 preflight](../experiments/preflights/E025-chain-successor) | Passed with actual source and handoff, zero provider calls; activation published at ecedc2e7489fd5f6d5d8f79a472df920e1ca35e1. |

The first attempt and retry 01 remain immutable operational interruptions, with zero complete public responses and unknown usage. The user explicitly approved the exact payload/destination for retry 02; its later network-policy failure is a different blocker. That disclosure approval must not be treated as missing again. The source-plan pause has been superseded by the current continuation instruction for its documentation/preparation scope. Do not dispatch an E025 retry or third episode without a fresh evidential decision.

The selected A proposed a contestable wording question. Its criticism and revision also carry source-attribution errors. B must be assessed for actual discrimination, added premises, preserved uncertainties and justified continuation/suspension/no-promotion; a queue entry is not a substantive result. This review is not supplied to the model.

## Research limits and preserved work

The [configuration-space and ECS-gap assessment](reviews/configuration-space-and-ecs-gaps-2026-09-12.md) is published at fb58b3fcca38e7f2d5126b518e4df5e4979300b7. It maps actual coverage versus untested engine controls. Independent challenge defeats the proposed P1 contradiction under a scoped-transition reading; only an optional wording clarification remains. Its 16-condition routing/deployment diagnostic is prospective, not a frozen experiment or evidence of criticism use, creativity or a filled semantic gap.

The [formal-feedback report](reviews/formal-feedback-research-2026-09-12.md), [protocol](FORMAL_FEEDBACK_PROTOCOL.md) and local diagnostic are complete. The prototype has eleven operator-authored fixtures, nineteen focused tests and chain-localization evidence. No live formal-feedback intervention exists; adapter/materials/frozen plan remain future work. These diagnostics do not establish semantic fidelity or creativity.

E019, E020 and E021 remain immutable interrupted records. E022 is complete and reviewed; original partial reviews remain unchanged. Existing source, frozen plans and observations are preserved. Normal/optimized integrated suites previously passed 569 tests; this continuation uses the specific actual-material preflight rather than repeating that suite.

The preserved successor ECS 2.0 is byte-identical to [the stored source](sources/ECS-2.0.pdf), SHA256 67bcb9512dd0fe93f2768cc429e71a8c5579a6a52b098d62da82a2f45d62138b. Gaps in definitions, candidate semantic counterexamples and implementation limitations must be reported separately. New interpretations or proposed repairs are new claims, not silent changes to ECS.

## Recovery discipline

Use minireason-progress-ledger when installed, one publisher and atomic activity logging. The skill was absent on the Windows recovery host, so explicit UTC receipts and the same publication duties were used. During active work, independently check both five-minute deadlines, publish every completed document immediately, and preserve stable partial evidence during larger uploads. Earlier cadence misses remain ledgered; no inactive period is claimed as monitored work. Verify remote main and exact local/remote trees. The [template-chain workflow](workflows/template-chain.md) supplies commands, but its original prepared-state descriptions are historical; this status and the latest ledger receipts give the current state.
