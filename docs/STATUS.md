# Current research status

## The automated loop is published complete through wave 6, and it has run end to end offline — 2026-09-14

REC-20260914-AF publishes the **driver**, the **operator page** and the **end-to-end acceptance
proof**, with the three documents that record them and the record of the executed dry run. Ruling
6's standing requirement — that the harness run end to end without a human in the loop — is **met
offline**: one command walks S0 to S15 against a real bare git remote with every provider offline.

**What completed.** [`tools/auto_loop.py`](../tools/auto_loop.py) is the S0…S15 driver, and
[`docs/workflows/automated-loop.md`](workflows/automated-loop.md) is the operator page, now at
`docs/workflows/` because it is integrated and its code tables are generated from the modules as
published. `tests/loop/` grows from twenty-two files to **twenty-five** — `test_auto_loop.py`,
`test_dry_run_end_to_end.py` (the 51-test acceptance proof) and `test_docs_pins.py`, which pins the
page against the modules from inside `tests/` where the suite discovers it. `src/minireason/loop/`
stays at **24 files**; three modules changed (`types.py`, eight driver codes folded and
`AuditConfig.period_account` made optional; `roles.py`; and `synthetic.py`, three wave-6 changes).
`types.FAILURE_CODES` now carries **218** members, `types.BLOCK_CODES` **10** and
`types.STOP_REASONS` **7**. Waves 5 and 6 were **drafted by Kimi K3 under ruling 16 and integrated
by Opus 5**, and the kept-versus-rewritten record, with the reason for each and a "Declined"
section, is [`WAVE5-INTERFACE.md`](design/loop-impl/WAVE5-INTERFACE.md) §5 and
[`WAVE6-INTERFACE.md`](design/loop-impl/WAVE6-INTERFACE.md) §2 — the draft's six declared seam
dependencies D1–D6, five of them deleted — and §3, the ten defects the acceptance proof found and
the change that closed each. Gate: `PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests`
reports **`Ran 3112 tests in 352.621s`, `OK (skipped=2)`** — the 2,989 on record at
`REC-20260914-AE` plus the loop's 123 new tests, and the arithmetic is exact.
`PYTHONPATH=src python3 …/v2/validate.py` from the repository root still reports **48 `PASS` lines
and `ALL CHECKS PASSED`**, so the module edits moved no pin the bundle carries. **The dry run was
re-executed by the publisher** against a fresh temp run root and a fresh temp bare remote and
reproduces [`DRYRUN-RECORD.md`](design/loop-impl/DRYRUN-RECORD.md): exit **0** with empty output,
the same `loop_plan_id`, **three cycles**, **43 step receipts** of which **eleven are publications
each carrying its own `VERIFIED` sidecar** (the last one's commit is the temp remote's `main`),
`stop_reason` **`no_new_reading_changes`**, **`planned_calls` 232** inside the pre-registered
**`max_calls` 396**, and under a provider-module counter **0 live transports, 0 requests opened,
218 offline providers**. Neither `DEEPSEEK_API_KEY` nor `OLLAMA_API_KEY` was in the child
environment, asserted by name before the call. **Zero provider calls under this receipt and no
credential read.** `docs/design/loop-impl/W6-DOC-draft/` is **removed as superseded by content** —
the integrated page carries all ten of the draft's sections plus three new subsections, every one of
the draft's 204 backticked codes and all ten `blocked:` codes, and the ceiling byte-identical, while
the draft's own text says the driver does not exist yet and pins the code table at 201.

**What this does not establish.** **The loop has still never run live.** Every number above is a
test result or an offline rehearsal result, and the dry run read `synthetic`'s **eight fabricated
rows**, not the pre-registered twenty-two H005 rows: nothing here is evidence about any arm, model,
family or account. The pre-registration bundle is **still a DRAFT** and stops being one only when
the driver mints it at S0 under its own receipt. `WAVE6-INTERFACE.md` §5 lists eleven questions the
rehearsal could not reach; three of them are the live run's first act — the **300 s host gateway
wall** (rulings 13 and 14; a `TRANSPORT_OR_RESPONSE_ERROR` at ~300 s is the host closing the arm,
never a verdict), the **key gates**, never contended because no credential was ever acquired, and
the **real `publish_ref`**, a non-forcing push onto this shared branch where the dry run pushed to
`origin/main` of a throwaway bare repository. The cadence receipt is still unwired by an explicit
decision. One condition in the acceptance proof is **built by the fixture and says so**. The
cold-cache `-W error` defect in `src/minireason/use_relation_h005.py:301` is **not repaired**; the
repair stays with `SRC-003`.

**Next authorized task: the first live run, L001.** It is launched by the operator command sequence
in [`WAVE6-INTERFACE.md`](design/loop-impl/WAVE6-INTERFACE.md) §6 — `preregister`, `preflight`,
`run`, from the repository root with the two credential names present in that shell and nowhere else
— and it **mints its own receipt at S0**; no receipt written in advance can name it, as this
checkpoint's own re-execution showed by minting the next free letter from the ledger in the tree it
dispatched for. It is a new decision and needs its own opening receipt before the first command.
**No other publisher may run while the driver holds the branch**: the driver publishes to
`origin/claude/project-state-direction-j5rbun` at every `PUBLISH_*` step and verifies each push, and
a concurrent publisher would move the ref under it and turn a verified publication into three
non-converging attempts.

## The automated loop's waves 3-4 are published as a recoverable checkpoint — 2026-09-14

REC-20260914-AE publishes the **trial runner, the audits, the report renderer, the cross-family
reader and the pairwise marker**, the two integrator interface documents that record them, the
**revised pre-registration bundle** as a labelled DRAFT, and the **W6-DOC operator-page draft**.
All of it existed only in an ephemeral session scratchpad until now.

**What completed.** `src/minireason/loop/` carries **twenty-one modules** plus `__init__.py` and
`data/`, and `tests/loop/` twenty-two files. The five new modules —
[`trial.py`](../src/minireason/loop/trial.py), [`audits.py`](../src/minireason/loop/audits.py),
[`report.py`](../src/minireason/loop/report.py) (wave 3),
[`reader.py`](../src/minireason/loop/reader.py), [`marker.py`](../src/minireason/loop/marker.py)
(wave 4) — were **drafted by Kimi K3 under ruling 16 and integrated by Opus 5**, and the
kept-versus-rewritten record, with the reason for each and a "Declined" section, is
[`WAVE3-INTERFACE.md`](design/loop-impl/WAVE3-INTERFACE.md) §6 and
[`WAVE4-INTERFACE.md`](design/loop-impl/WAVE4-INTERFACE.md) §5. Not one Kimi draft was known to be
green when it was handed over — two runs hit the 90-iteration cap and two were cut by the ruling-13
gateway close — and both documents print the delivered `FAILED` lines beside the integrated `OK`
lines. `types.FAILURE_CODES` now carries **210** members (five folded in at each wave);
`types.BLOCK_CODES` is unmoved at ten. Gate: `PYTHONPATH=src python3 -X utf8 -m unittest discover -s
tests` reports **`Ran 2989 tests in 236.810s`, `OK (skipped=2)`** — the 2,673 already on record plus
the loop's 316 new tests, and the arithmetic is exact. The revised bundle is
[`docs/design/loop-prereg-draft-2026-09-14/v2/`](design/loop-prereg-draft-2026-09-14/v2/README.md):
thirteen blockers closed, four new files (`CHANGES-PREREG.md`, `CLONE-PATCH.md` and the
`bundle-worksheet` pair), and `PYTHONPATH=src python3 …/v2/validate.py` from the repository root
reports **48 `PASS` lines and `ALL CHECKS PASSED`** against the modules as published. The v1
directory's bytes are **unedited**; one appended line points at v2. Credential scan over the 36 staged
paths and over all 81 files under the published directories: **zero key-shaped matches**,
line numbers only. **Zero provider calls under this receipt and no
credential read.**

**What this does not establish.** The loop has **still never been run**: `W5-DRIVER` and
`W6-DRYRUN` are unbuilt, no cycle has executed and **no plan has been minted at any commit on any
ref**, so every number above is a test result and not a run result. The bundle is a **DRAFT** —
`CLONE-PATCH.md`'s **six items are all owed by the driver integration**, two of them required
(something must read `calibration.json` and pin its digest; `plan.json` must pin
`audits.CALIBRATION_EXCHANGES_SHA256`), and every pin in it is **to be re-read at S0 PREFLIGHT**
after the loop package freezes. The operator page is published at
[`docs/design/loop-impl/W6-DOC-draft/`](design/loop-impl/W6-DOC-draft/automated-loop.md) and **not**
at `docs/workflows/`, because it is not integrated: its failure-code table was generated at 201 rows
against the module's 210, its driver argv is a placeholder, and its `test_docs_pins.py` travels with
it under `docs/` where the suite does not discover it. The cold-cache `-W error` defect in
`src/minireason/use_relation_h005.py:301` is **re-checked and not repaired** — on a truly cold
bytecode cache 7 of the 22 import targets pass and 15 fail, up from 10 because the five new modules
reach the same import chain; the repair stays with `SRC-003`.

**Next authorized task, in order.** **(1) `W5-DRIVER` integration applying `CLONE-PATCH.md`** — the
state machine S0…S15, the two required clone-side items, and the four declared gaps taken or
declined explicitly, including the per-role guard-block streak counter PREFLIGHT must assert.
**(2) `W6-DRYRUN`**, with `W6-DOC` integrated to `docs/workflows/` and its code tables regenerated
against the modules then. **(3) Kimi pin recomputation** — every digest in the bundle re-derived
from the frozen tree, as a mechanical task under ruling 16 with Opus verifying. **(4) A dry run with
zero provider calls**, whose acceptance gate is the design's, **before any live run is proposed**.
Each is a new decision with its own receipt, and no provider call is authorised by any of them until
the dry run has passed.

## The Kimi K3 subagent workstream is published as a recoverable checkpoint — 2026-09-14

REC-20260914-AC publishes the **Kimi K3 worker harness, its battery, its run records, its fifteen
Opus controls, the seven Opus judgements, the owner's report and this session's rulings**. All of it
existed only in an ephemeral session scratchpad until now.

**What completed.** [The owner's report](reviews/kimi-k3-subagent-2026-09-14/REPORT.md) — the
deliverable ruling 11 authorised and ruling 16 asked for, published **verbatim** — with
[`PASS1-INTERIM.md`](reviews/kimi-k3-subagent-2026-09-14/PASS1-INTERIM.md),
[`RUNS-RECLASSIFIED.md`](reviews/kimi-k3-subagent-2026-09-14/RUNS-RECLASSIFIED.md) and the
[seven judgements](reviews/kimi-k3-subagent-2026-09-14/judgements/) (`family-A.md` … `family-F.md`,
`pass4.md`), each by a separate Opus 5 subagent instructed to re-execute what it certifies and to
name what it did not run. The harness is [`tools/kimi_harness/`](../tools/kimi_harness/) —
`kimi_agent.py`, `run_battery.py`, `reclassify.py`, its 49 offline tests, its README, `PRODUCTION.md`,
`PROBE-REASONING.md`, the three probe scripts and the fourteen live probe records they wrote. The evidence is
[`experiments/diagnostics/K001-kimi-k3-subagent-battery/`](../experiments/diagnostics/K001-kimi-k3-subagent-battery/):
the battery (26 tasks, four pass files, `evaluation.json`, `rubric.md`, `MANIFEST.sha256` over 432
frozen files, the judge-only `reference/`), **80 run records** across pass 1-4, the production runs
and the smoke runs — each one's `result.json` plus the directories the worker itself wrote — every
`SUMMARY.md`, the fifteen controls with their `FINAL.md` and `PROMPT.md`, and `TRANSCRIPTS.md`. This
session's rulings, including the owner instructions quoted in them, are
[`docs/reviews/session-rulings-2026-09-14.md`](reviews/session-rulings-2026-09-14.md). Gate:
`PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests` reports **`Ran 2673 tests in
222.409s`, `OK (skipped=2)`** — unchanged, because nothing was added under `src/` or `tests/`; the
harness's own suite reports **`Ran 49 tests`, `OK`**. Credential scan over all 558 staged files:
**zero key-shaped matches**. **Zero provider calls under this receipt and no credential read.**

**What this does not establish.** It is an **operations** record, not a finding about Mini or FW5.
It defines no metric, publishes no score and ranks nothing; the report's routing table is a decision
aid for the orchestrator. Every statement about the worker is about these occasions on this corpus —
no phrasing control, no repetition under identical conditions. Kimi output reaches the record only
after Opus verification (ruling 11). **The transcripts are not published**: 81 files, 444 MB, more
than this whole working tree, so `TRANSCRIPTS.md` records each one's path, byte size, line count and
sha256 and states that they stay in the ephemeral scratchpad. The frozen corpus `battery/material/`
is likewise omitted as a reproducible copy of repository files, every one of its 432 files pinned in
`MANIFEST.sha256`.

**Next authorized task.** **Kimi K3 drafts wave 3** under ruling 16 (`prod-tasks/tasks-w3.json`; the
battery was still running when this checkpoint was cut, and `w3-audits` has no record here),
**and Opus 5 integrates and reviews every draft before any of it reaches the record.** Ruling 11
holds: Opus remains the verifier of every Kimi output that touches the record, and Opus alone judges
Kimi's own battery, makes design decisions, argues over FW5, and publishes.

## The automated loop's waves 0-2 are published as a recoverable checkpoint — 2026-09-14

REC-20260914-AA, re-attempted under its own identifier after its first attempt failed its own
gate, publishes the **automated end-to-end harness loop's waves 0-2** on this branch. The
section below, "The automated loop's waves 0-2 checkpoint was verified and refused", records
that first attempt and is left standing unedited; **this section supersedes its outcome and
nothing else in it.**

**What completed.** The two defects that refused the first attempt are repaired and the repair
of each is proved by the test that caught it. `tests/loop/test_roles.py` now captures the
pristine `socket.socket`, `socket.create_connection` and `provider_openai_compat._open` once at
import and installs its refusal under a lock behind a depth counter, so six concurrent threads
can no longer leave the process patched; `tests/test_provider_openai_compat.py`'s two
no-network tests pass inside the full run. `src/minireason/loop/data/plan_8a_mirror.json` is
re-pinned to the C001 `PLAN.md` this branch carries (`a27fe94a…`), so
`tests/loop/test_standard.py`'s digest assertion passes rather than skipping. **Wave 2 is
integrated**, which discharges the opening receipt's limit (3):
[`WAVE2-INTERFACE.md`](design/loop-impl/WAVE2-INTERFACE.md) exists, items 24-28, 42 and 48-54 of
the integration list are dispositioned in it, twenty-nine failure codes were folded in so
`types.FAILURE_CODES` carries 201 and its frontier is empty, and `STANDARD_BODY_SHA256` has
moved twice to `a9007dc7…` (the second move is the `cal-01` repair, PR-06). The gate:
`PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests` reports **`Ran 2673 tests in
214.278s`, `OK (skipped=2)`** — the 1,450 already on record plus the loop's 1,223. Credential
scan over every staged file, **0 matches**. **Zero provider calls and no credential read.**

**Published paths.** `src/minireason/loop/` (sixteen modules, `__init__.py` and two data files),
`tests/loop/` (seventeen files), `.gitattributes` marking the loop's data and the ledger `-text`,
one `pyproject.toml` package-data line, the [design of
record](design/automated-loop-design-2026-09-14.md), six documents under
[`design/loop-impl/`](design/loop-impl/), and the eight-file L001 bundle under
[`design/loop-prereg-draft-2026-09-14/`](design/loop-prereg-draft-2026-09-14/) **as a labelled
draft**, with a README naming its stale pins and its thirteen open blockers.

**What this does not establish.** The loop has **never been run**: no driver exists, nothing has
executed end to end, and every number above is a test result and not a run result. **No provider
call is authorised by any of it.** Waves 3-6 are unbuilt — no trial runner, no marker, no driver,
no report, no operator page. The pre-registration bundle **is not a pre-registration**: it is not
minted until S0 PREFLIGHT against the tree that exists then, its `STANDARD_BODY_SHA256` is stale
by two generations, its `VALIDATION.md` pins a superseded `config.json`, and **all thirteen
blockers PR-01 through PR-13 are open as bundle edits** — five of them (PR-02, PR-05, PR-06,
PR-07, PR-12) have had their code half repaired and recorded in `WAVE2-INTERFACE.md` §10, and no
bundle edit is made. The two declared narrowings of `use_relation_h005` — the six-value reading
vocabulary and the "the reading is root's" banner a loop table would contradict — are applied
nowhere; the instrument is untouched and the twenty-four published analysis artifacts keep their
banner. A new finding is recorded and **not** fixed: on a cold bytecode cache, **ten** of the
seventeen import targets fail `python3 -W error` with `SyntaxError: invalid escape sequence '\s'`
raised from `src/minireason/use_relation_h005.py:301`; that is a repository defect belonging to
`SRC-003`, not to this package, and the first attempt's "all seventeen OK" was a warm-cache false
negative.

**Next authorized task, in order.** (1) **Build waves 3-6** — trial runner, marker, driver,
report, operator page — against `WAVE2-INTERFACE.md` §11's open list. (2) **Revise the
pre-registration bundle against `REVIEW-PREREG.md`**, closing PR-01 through PR-13, regenerating
`VALIDATION.md` **before** publication rather than after, and re-deriving every pin against the
tree that exists then. (3) **A dry run with zero provider calls**, on synthetic fixtures, before
any live run is a question at all. **Only then** is a live run a decision, and it would be a new
decision with its own receipt: **no provider call is authorised by anything above.** Ruling 7
holds throughout — the harness defines no metric and no optimisation target over the material —
and ruling 9's prohibition on an automatic search for a winning configuration holds with it.

## A001 is published as an in-progress record — the Account challenge of FW5 — 2026-09-14

REC-20260914-AB publishes **A001**, the independent Account sufficiency/necessity challenge to the
designated FW5 reading edition that PURPOSE.md names in parallel with the construction-and-use
programme ("an independent Account sufficiency or necessity challenge tests FW5 itself"), and that
session ruling 9(b) recorded as an untested gap. It existed only in an ephemeral scratchpad until
now.

**What completed.** [The record](reviews/A001-account-challenge-2026-09-14.md) — the revision-4
staging **verbatim** under a short added header — with its [cell
register](reviews/A001-account-challenge-2026-09-14-cells.md) and a twelve-file [audit
trail](reviews/A001-account-challenge-2026-09-14-history/) of three earlier staging revisions, two
earlier cell registers, three revision-history maps, three adversarial review rounds and the narrow
verification, all unchanged. The record passed **three adversarial review rounds** (F1–F29,
F30–F50, F51–F67) and a **narrow verification** returning seven verdicts and "PUBLISHABLE AS
IN-PROGRESS RECORD: yes"; its **eleven residual open items are carried verbatim as the record's
final section** so that a later reviewer attacks them first. The FW5 edition hash
`8105925b…e33ee63a` and all five register pins re-hashed **exact** at publication. **Zero provider
calls**: every leg is offline and no credential was read.

**What it does not establish.** A001 **does not refute FW5**, offers **no counterexample to
sufficiency and none to necessity**, and records two authored prose cases as failures — one of them
disposed only under **(P-Ans)**, a premise A001 supplies and the edition does not, with the
alternative reading filed as the missing definition **D22**. One reading of one cycle's records
cannot **decide the constitutive conjecture**. **No cell is filled and no reading is offered**, so
nothing here is a finding about the bare, native, matched, `mini_prose` or `mini_fcl` arms. The
"Testing FW5 itself" deliverable — a candidate counterexample and the clause that would have to
change — **remains owed**. The record's §7 proposes five publication paths; **two are published
here and the other four are not**, so `docs/reviews/A001-gap-filling-proposals-2026-09-14.md` and
`experiments/diagnostics/A001-account-challenge/` do not exist and **the executable leg is not
pre-registered**.

**Next authorized task for A001: attack the eleven open items**, in the record's own order — items
3–7 (the unrecorded (b6) edit, the X3/X1 witness collision, the missing `not-free` condition in the
X2/X2b/X1/X1b witnesses, the weak "searched, none exhibited" record, and the three seams in the
class table) before anything else, since each is a defect in A001's own instrument that the reading
step would otherwise inherit; then items 8–10 (whether (r3) is the rule A001 wants, the surviving
"under every λ" phrase at §5(a)(i), and the carried-forward debts including (P-Ans) and the owed
deliverable). **No re-run and no reading step is authorised**, and **no provider call is authorised
by anything above**; pre-registering the executable leg, filling any cell, or dispatching anything
would each be a new decision with its own receipt.

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

[Owner-relayed repair-mill critique](sources/owner-relayed-repair-mill-critique-2026-09-14.md) preserves both exact chat inputs with FW5 clause locators (2026-09-15); the T6/null-case proposal remains OPEN, with no provider call or publication.

## L003/AQ recovery onto the durable Windows checkout - 2026-09-15

**Recorded at 2026-09-15 05:01:14 UTC, under REC-20260915-B.** STATUS had not been updated for
REC-20260914-AQ until this appended section. The earlier **"Next authorized task: the first live
run, L001"** section is historical; L001 and L002 are closed operational failures, and this
recovery concerns the interrupted L003.

**What AQ preserved.** The last verified remote publication is **REC-20260914-AQ**, commit
`c76fc1ef78b5b35baadc23366c271610b0721e5a`, tree `9194745a177690bdae9773d4c6f3b4d362fc37c5`,
acknowledged by `8ad1f58a1664d9f8dc4498309e327ae5f9ec8806` on
`origin/claude/project-state-direction-j5rbun`. The preserved ledger receipt and local Git objects
confirm that boundary; no new remote verification is claimed here. L003's steps **0001-0025 are
COMPLETE**; **0026 PUBLISH_CY is FAILED, GIT_OPERATION_FAILED**, with no published-commit
acknowledgement, because the empty `readings/` directory was passed to Git as a pathspec. The
preserved `run.lock` records **lock released at 2026-09-14T23:59:17Z**, with `pid: null`.
**18 provider calls were preserved: 11 dispatch calls in F001 occurrence-09 and 7 cycle-1 marking
calls.** Cycle 1's decision is **CONTINUE / chain_open** (`no_clause_fired`). Its **12 mark results**
are **5 same, baseline-forced**, and **7 unresolved**. These are operational record counts and
guarded marks, not findings about an instrument, arm, model or account. AQ preserved the run's
outputs and receipts as the driver left them; completed coordinates must not be replayed.

**Recovery facts.** The owner reports that the cloud session which ran L003 has stopped and is
unrecoverable. `C:\Users\darre\OneDrive\Desktop\Codex\miniReason-claude-project-state-direction-j5rbun`
is a git-less mid-run snapshot exported approximately **00:37Z**, discarded as a source of state.
Its only salvaged content was the owner-inputs source file, re-applied under **REC-20260915-A**;
that receipt is now **COMPLETE locally**, with the source and earlier STATUS pointer unchanged.
The working checkout is **`C:\Dev\miniReason`**, cloned at **`8ad1f58a`**, with
**`core.autocrlf=false`** and **all 9,080 tracked files byte-verified at clone recovery**, as reported
by the owner; this recovery confirms the tracked-file count, HEAD and autocrlf setting. The host is
**Windows 11, Python 3.11.9, E. Australia Standard Time (UTC+10)**. Earlier ledger stamps labelled
UTC through pre-append line 1650 were local time; they remain unchanged. The clock evidence is
occurrence-09 provider epoch **1789430323 = 2026-09-14T23:58:43Z** and Git's AQ/acknowledgement
commit times **2026-09-15T00:35:10Z / 2026-09-15T00:35:35Z**. New receipts use real UTC.

**What remains pending.** The concurrent worker is implementing the publish-step repair under
REC-20260915-B in `tools/auto_loop.py` and `src/minireason/loop/publish.py`, with
`src/minireason/loop/steps.py` if needed and tests in `tests/loop/`. Each publish step must pass
only file paths to Git; an empty publication records `published=false` and no VERIFIED line;
already-committed paths count as published. The offline host log
[`work/tests-durable/unittest.log`](../work/tests-durable/unittest.log) reports **`Ran 3040 tests
in 215.360s`, `FAILED (failures=62, errors=480, skipped=8)`**, against the recorded Linux baseline
**3,129 tests, OK (skipped=2)**. This is a **host-portability limitation to be triaged**, not evidence
about any instrument. By the owner's **2026-09-15 instruction**, workers are **gpt-6-astra via the
Codex CLI**, a declared session deviation superseding **ruling 16**, recorded in the manner of
ruling 3. No provider calls under REC-20260915-B so far; no credential write, commit or push in
this documentation task. Publication is a separate later step; REC-20260915-B stays **PENDING**
until the repair is reviewed and the resume runs.

**Next authorized task: land the publish-step repair under REC-20260915-B, then resume L003 with run; no other publisher while the driver holds the branch.**
The recorded resume command is `run --config docs/design/loop-prereg-draft-2026-09-14/v4/config.json`
from the repository root, with both key names in the shell only, after the repair is reviewed and
landed. This documentation update does not run that command.

---

**A001 continuation — 2026-09-15 05:14:18 UTC, REC-20260915-C.** Appended [review round 4, F68-F72](reviews/A001-account-challenge-2026-09-14.md#review-round-4) after the carried open items, from one Astra worker's draft independently judged by a second. This continues the A001 section at STATUS:246-266 and is appended after the preserved REC-20260915-A/B and L003 recovery tail. Items 3-7 now have a dated disposition map: the (b6) disclosure is corrected, the defective witness and completed reachability claim are withdrawn, and the missing antecedents, evidence states and table exits are recorded as corrected successor specifications. Companion and history notices are appended; every earlier byte is retained. **Next authorized A001 task:** address items 8-10, including (r2)/(r3), the conditional wording and (P-Ans), the English conditional rule/A29 and the remaining disclosure argument; supply replacements for withdrawn witnesses, the reachability demonstration, the independently sourced interpretive technical case and the counterexample-and-clause deliverable. Those deliverables remain owed. Items 8-11 are assessments only and the separate instrument/semantic contributions are **proposed, not adopted**. A-S remains failed under (P-Ans), with the D22 alternative; B-N dropped; no counterexample to sufficiency or necessity; the executable leg cannot charge Account. No reading step, provider calls or publication under this receipt.


**REC-20260915-B publication checkpoint ? 2026-09-15T07:42:07Z.** The publish/steps/receipts repairs and resume-reload fixes are approved for publication under the owner's explicit acceptance of review-6e.md plus its applied exact patch in work-6f.md. Final recorded focused verification: 263 run, zero failures/errors, two symlink privilege skips; real L003 0024/0025 output digest maps reproduced. A001 F68-F72 (review-7 APPROVE as-is), its companion/history appends and the owner-inputs source are included. Publication state is pending the verified session-branch push and acknowledgement; main remains pending owner merge (ruling 2). The historical Windows offline-suite failures remain a host-portability limitation: recon-M2 accounts for all 542 entries; LongPathsEnabled=0 still affects readings/ fixtures, while L003 has zero reading rows. No provider call or live resume occurred in this publisher task. **Next authorized task:** after this checkpoint is verified, the later operator may follow the existing REC-B L003 resume instructions; A001 items 8-10 and owed deliverables remain separate pending work. Prior STATUS and stop-receipt bytes are preserved.
