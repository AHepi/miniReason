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


**REC-20260915-B publication verified ? 2026-09-15T07:43:14Z.** Session-branch checkpoint `f57924339a419e91f6fcf688aca9123a2d185473`, tree `969d22e8d81f9062c1beb971d92cf5555309c781`, contains the 17 reviewed paths. Non-forced push and fresh fetch succeeded; advertised remote, fetched remote and local commit are identical, and remote/local trees are equal. Repair/publication checkpoint complete; this receipt is the separate acknowledgement. Main remains pending owner merge (ruling 2). Live L003 resume and further A001 work remain pending later operator actions; this task made no provider calls. Existing Git identity was incomplete, so both publisher commits use the authorized miniReason orchestrator / noreply@local fallback and the requested co-author trailer. The first verified push completed 292 seconds after the opening receipt, within the five-minute publication cadence.


## L003 closed on 2026-09-15

**Recorded at 2026-09-15T08:25:20Z, under REC-20260915-B.** Appended after the preserved L003/AQ recovery and publication sections. Here, R is experiments/loops/L003-loop-first-live-2026-09-14; recon-R.md is the verified read-only report named in the completion ledger.

**Repair and resume.** The reviewed recovery checkpoint landed under `f57924339a419e91f6fcf688aca9123a2d185473`, acknowledged by `3a2211415231252431b0b77d159337f9d2013333` (ledger:1712,1716,1718). The recorded scope is the publish-step repair, Windows locking/cleanup, and resume-state reload with newline neutrality. `review-6e.md` says **APPROVE WITH exact edits**, satisfied by `work-6f.md` under the owner's publication approval; `review-8.md` and applied `work-8b.md`/`work-8c.md` are named, but the literal review-8 verdict is **NOT FOUND** in the admitted sources. Separate corroboration/review verdicts for the specifically requested receipt locking and RunLock holder read subfixes are **NOT FOUND** there. The recorded newline comparison is at AGENT_ACTIVITY.jsonl:2702.

The resume ran twice. First: **0027 PUBLISH_CY** published and verified; cycle **2** completed **0028-0036**; **0037 PUBLISH_CY** failed `GIT_OPERATION_FAILED`, **"Author identity unknown"** (R/steps/0037-PUBLISH_CY.json:7,16,20; C:/Dev/minireason-launch/l003-run.log:1,13). The publisher's identity is recorded as `miniReason orchestrator <noreply@local>` (STATUS:709); the missing usable checkout identity is consistent with the failure, but an admitted receipt proving the subsequent repo-local identity-setting action is **NOT FOUND**. Second: **0038 PUBLISH_CY** published and verified, **0039 CLOSE** completed, **0040 PUBLISH_CY** published and verified. The driver's own VERIFIED records name **0027: 3a2211415231252431b0b77d159337f9d2013333; 0038: 2ed6ba576d7f254ef16aa1b6a03900642a4b62ce; 0040: 4aeef3f5bf78a7b9c521273014fcae80f0b11675** (the corresponding R/steps/*.verified:1; full commit/tree lines copied in the completion receipt). The failed step's VERIFIED sidecar is **NOT FOUND**. The run reached its closing record; this recording does not claim a fresh remote check.

**Recorded stop.** Cycle **2** records `clause=clause_four_set_identity`, `reason=no_new_reading_changes`, `stop=true` (`R/cycles/cycle-02/decision.json:2-6`); `R/CLOSING.md:56-59` says the two cycles' triple sets are identical. Its `stop_reason` is `no_new_reading_changes`: the canonical JSON string reproduces the stored SHA-256 `a144eb43f2557cd860bb642c2deb33c077c6e51e6341fa12947ea8d1b2971941` (`R/steps/0039-CLOSE.json:19`). The **3-cycle** boundary was not reached (`R/config.json:16`); cycle-03 is **NOT FOUND**.

**Recorded states, without interpretation.** Cycle-2 marks: **same 5; differs 0; unresolved 7**. Blocks: **baseline-forced-same 5; provider 4; null 3**. Printed **ensemble-split, referential-integrity, operative-target, order-swap, paraphrase-flip, outside-vocabulary, schema and constitution** counts are each **0** (R/cycles/cycle-02/contrast/deepseek-flash__fcl/marks.json line pairs in recon-R section 4; R/READING_TABLE.md:7-16). Audit call states: **OK 5**, sustained **true 3 / false 2**, for judge#1; **BLOCKED 5 / INCOMPLETE_GENERATION 5 / blocked:provider 5** for judge#2, whose sustained field is **NOT FOUND** (the calibration call.json lines listed in recon-R section 4). The audit's `findings` array contains **one** `planted-flaw-calibration` entry at `audit-cal/no-shared-reference/judge#1`, with `collapsed=[]` and `targets=[]` (R/audits/cycle-02/audit.json:3,8-17); this is a schema-field record, never a finding. Paraphrase/order-swap/disagreement audit outcomes, `JUDGE_ERR` and actual streak counters are **NOT FOUND** in recon-R's searched scopes. READING_TABLE's state table records **unread 16, unresolved 16, machine-unresolved 4, read 5 (all same)** (:22-62); its separate machine-unresolved list records **9 entries, 5 baseline-forced-same and 4 provider** (:104-112), and its read list **5 same** (:115-119). COMPARISON records **same 5, unresolved 7, differs 0** (:20-31), with explicit unread/machine-unresolved/read result-row categories in its mark table **NOT FOUND**. CLOSING says **no audit record entered the graph** (R/CLOSING.md:52). These distinct printed scopes remain unchanged.

**Provider accounting.** Whole-run provider accounting, re-summed from every response listed in recon-R section 6: **35 calls**, **103,454 prompt + 113,659 completion = 217,113 total tokens**, with **22 COMPLETE** and **13 INCOMPLETE_GENERATION** records. Per endpoint (calls; prompt/completion/total): **ollama/kimi-k3: 11; 30,740/87,421/118,161 (11 COMPLETE)**; **ollama/gpt-oss-120b: 18; 62,624/14,962/77,586 (11 COMPLETE, 7 INCOMPLETE_GENERATION)**; **ollama/qwen3.5-397b: 6; 10,090/11,276/21,366 (6 INCOMPLETE_GENERATION)**. Pre-resume: **18 calls, 156,413 tokens**; resumed: **17 calls, 60,700 tokens**, comprising **7 marks + 10 audit calls**. These are provider-record arithmetic and delivery states only, not a driver counter or an evaluation of material. The declared **max_calls 165** was not reached: **130 calls below** (`R/config.json:18`). The completion receipt gives the exact response-field citation convention from recon-R section 6. Provider-response `failure_code` and `error` fields are **NOT FOUND**; `PROVIDER_GATEWAY_WALL`, `KEY_MISSING` and non-null `failure_code` are **NOT FOUND** in the resumed cycle/audit JSON scan. Recorded step failures remain `GIT_OPERATION_FAILED` at **0026** and **0037** (`R/CLOSING.md:154-155`).

**Host and workers.** Workers were **gpt-6-astra via Codex**, under the owner's **2026-09-15** instruction, a recorded deviation from ruling **16** (docs/DECISION_LEDGER.md:1698; docs/STATUS.md:690-692). Known host limits remain: **LongPathsEnabled=0**, so loop `readings/` paths exceed MAX_PATH in driver test fixtures; L003 had **zero reading rows**. The prior receipt reports Git-for-Windows `sh.exe` startup failure in the Codex sandbox and unsandboxed focused verification/dry-run publication evidence (docs/DECISION_LEDGER.md:1712); direct evidence establishing that the live driver itself ran unsandboxed is **NOT FOUND** in recon-R and the admitted repository record. The **300 s** host gateway wall remains the recorded limitation (docs/STATUS.md:47-48); this run does not establish that it changed.

**Claim ceiling.** FW5 is the sole semantic target (owner ruling **17**; PURPOSE.md:3). Under ruling **7**, no metric, score, rank or merit is assigned over the material. A reading or mark is a guarded `judge`-role artifact, never a finding and never FW5:628's witness of reason use; a high block rate is the instrument declining to read. A reached ceiling is a declared resource boundary, never exhaustion of inquiry. That the loop ran without a human is a fact about the loop, not about the readings. `appellate_rulings: 0` is recorded (`R/CLOSING.md:146,148`); this does not validate, check or confirm the readings. This run establishes **no finding about any arm, model, family or account; no Mini ranking; no FW5 verdict** (R/CEILING.md:3,9-23; PURPOSE.md:7,11,21). Reopening conditions remain an appellate ruling, a successful attack on the standard/register definition, a custody correction, a further judge family or replicates, or a new plan with a raised budget (R/CEILING.md:23).

**Publication residue.** The driver's own publications left **_run.json, graph/log.jsonl, run.lock, graph/blobs/06/, graph/blobs/88/, graph/blobs/b3/, the new graph artifact/commitment objects, steps 0027-0040 and the existing .verified sidecars for 0027, 0038 and 0040** uncommitted (recon-R section 3). The completion ledger lists every path exactly as recon-R gives it. The follow-up publisher will commit that residue unchanged under this receipt, as REC-20260914-AQ did for the first interruption. **No byte of any run file is altered. STATE: COMPLETE locally pending publication of this receipt and that residue.**

**Next authorized task:** the successor pre-registration to **READ the new F001 occurrence-09 material**. The exact reservation begins at docs/design/loop-prereg-draft-2026-09-14/v4/PREREG.md:214 and continues through :216:

> **What that makes this run.** L003 dispatches F001's own next occurrence, under F001's frozen plan,
> whose material is **material for a successor pre-registration to read**; and it reads and marks only
> published bytes. That is a smaller claim than L001's and it is the honest one available.

**Still owed, unchanged:** C001 root reading, with the owner's decision on delegation pending; A001 **items 8-10** and the owed replacements for withdrawn witnesses, reachability demonstration, independently sourced interpretive technical case, and counterexample-and-clause deliverable (STATUS:703; ledger:1703); **main merge pending owner (ruling 2)** (STATUS:709). This recording starts no successor, reading or provider call and makes no state-changing Git command.


### REC-20260915-B completion publication verified ? 2026-09-15T08:44:35Z

The L003 completion, approved wording corrections and all 27 unchanged driver residue files are published to `claude/project-state-direction-j5rbun` at commit `e44dc34506f4e9f7fc48b4725f3e894527b56acc`, tree `96dc8082d99792e0d29a0720894a30fa3d738cb1`. Fresh fetch and ls-remote agree with local HEAD, and local/remote trees are identical. **Completion publication: COMPLETE.** The separate acknowledgement commit is pending its own push verification. The next authorized task and owed items listed above remain unchanged; main merge remains pending owner action. This publisher made no provider calls.


### L004 v5 drafting handoff - 2026-09-15T20:34:17.564622+00:00

REC-20260916-A completed the DRAFT bundle at docs/design/loop-prereg-draft-2026-09-14/v5/. Its central proposal is a row-construction contract over frozen F001 occurrence-09; rows remain UNRESOLVED and no key is admitted. The single offline validate.py invocation exited 1 with the expected UNRESOLVED/FAIL for rows; exact output is in v5/VALIDATION.md. Open decisions: owner approval of the row contract, builder/adapter implementation and pinning, final R and budget (11R + 46W), audit O5 semantics, relation-only stop/ceiling and safe reopening. No identifiers minted, provider calls, run authorization or state-changing Git; publication remains a separate publisher step. Existing owed work and owner main merge remain unchanged (STATUS:738).


REC-20260916-A independent JUDGE correction round at 2026-09-15T21:09:58.539569+00:00: APPROVED-AS-CORRECTED for publication as a draft only (docs/design/loop-prereg-draft-2026-09-14/v5/REVIEW-PREREG.md:1). Applied J01-J26 in v5/CHANGES-PREREG.md:36 onward, including eleven-text grounding, exact source citations, inherited calibration byte/semantic corrections and validator coverage. Judge rerun exited 1, FAIL (UNRESOLVED), with all printed structure/custody checks passing (v5/VALIDATION.md:3-41). The row arrays remain empty. Owner contract/grain approval, calibration expectations, lossless builder/adapter implementation and full pins, actual R and provider/audit budget, O5 semantics, reading-only stop/scoped ceiling, path checks and safe reopening remain open. Owner approval to mint L004 or authorize a run is NOT FOUND; this paragraph authorizes no run. No provider calls, identity minting or Git mutations were performed. Publication is a separate publisher action. Obligations digests and all three committed prefixes were verified; final evidence and complete notes are under scratchpad reports/review-10/notes. The earlier worker receipt remains historical; this correction supersedes its one-invocation/current-calibration wording without changing its bytes.


### W11 offline engineering handoff - 2026-09-16 (UTC 2026-09-15T23:52:55.772297+00:00)

Under REC-20260916-B, F003-operative-return now contains a draft PLAN, native material/arms/manifests, source hashes and actual validation report. It remains "Draft pre-registration, staged and not run" and "NOT INITIALIZED - no plan_id minted". The new pairs-v1 adapter and explicit reading_rows_builder config path are implemented; legacy serialization and H005 behavior are preserved. WAVE7 and the appended workflow section describe the interface and limits (docs/design/loop-impl/WAVE7-INTERFACE.md:5; experiments/diagnostics/F003-operative-return/PLAN.md:3,13,136).

V6 at docs/design/loop-prereg-draft-2026-09-14/v6/ retains the fourteen-file structure, six admitted prior-exposed occurrence-09 slots and zero unresolved slots; exact references and source spans are retained. All admitted slots remain unread by guarded roles. F003 is a contingent second source, with no observations. V6 offline custody validation passes with 156 source hashes and both obligations digests; the proposed first-pass allowance is 112 calls, never launch authority (v6/PREREG.md:33-68; v6/VALIDATION.md:1). Longest computed full provider paths are 189 for F09 and 193 for contingent F003, below 240 (WAVE7-INTERFACE.md:59).

Verification: sixteen pair tests, twenty-six docs-pin tests and four final no-initialization integration tests pass. The full driver suite ran 67 checks: thirteen passed and 54 failed at sandbox temporary-directory setup. All seven resume tests stopped at the same boundary. C:/tw11 creation is denied; no test fallback was selected. F003 static native compilation/routes/budget checks pass, but its permitted throwaway initialize/verify qualification is BLOCKED before initialize at that directory guard. The known Git sh.exe fixture-push artifact was not reached, and no claim is made that it occurred. Exact summaries, prior failures and classification are in work/w11/TEST-SUMMARY.md and sandbox-errors-final.json. No provider/model calls, run identities, state-changing Git commands or publication occurred.

**Next authorized task:** owner review of F003 PLAN, especially the disclosed coordinate-banner envelope differences and operator-supplied inherited candidate; restore the required temporary-root access and complete the blocked qualification; then initialize F003 under its own receipt and authorized dispatch conditions; then consider L004/v6 minting with its actual available sources, budget and pins. O5, relation-only stop/scoped ceiling, actual call accounting and reopening remain explicit launch decisions (v6/CLONE-PATCH.md:14-20). Publication is a separate publisher step using work/w11/PUBLISH-CHECKLIST.md.

**Still owed, unchanged:** C001 root reading with the owner's delegation decision pending; A001 items 8-10 and replacements for withdrawn witnesses, reachability demonstration, independently sourced interpretive technical case, and counterexample-and-clause deliverable; main merge pending owner (STATUS.md:738). This handoff neither discharges those items nor changes published observations. All working notes, rejected designs, probes and evidence are indexed at work/w11/INDEX.md.


### W11 independent judge correction - 2026-09-16T00:29:05.502927+00:00

REJECT for publication qualification under the owner's required-test condition. Root applied complete-reference token matching (including UTF-8 continuations), real matched/direct visible_sources mapping, selected-view checks, O1 active/candidate separation, surface contract/citation/arm-order corrections and refreshed v6 custody evidence. Twenty corrected pair tests plus four fresh driver integration and twenty-six docs-pin tests pass. Six occurrence-09 slots remain admitted, zero unresolved; longest initial provider paths remain189/193. V6 validation passes all156 source pins,9 contingent F003 hashes and both recomputed obligations digests (work/review11/v6-validation-final.txt; v6/VALIDATION.md).

Initial full requested suites completed:346 tests,321 pass,2 Windows symlink-privilege skips,22 legacy261-character fixture path errors and1 stale resume assertion. No sh.exe failure was observed. The same-root shorter-prefix diagnostic still fails in unchanged custody.py:584-588 creating its longer atomic .part path; its redundant bulk rerun is explicitly partial/interrupted. L003 replay digests match, but tests/loop/test_resume_reload.py:181 expects26 records where the frozen run has40; HEAD reproduces it. That existing test is outside the authorized correction paths and remains unchanged. The reviewable OWNER-RESUME-FIX.patch passes all7 resume tests in an isolated proposed-source proof, not in the on-disk suite.

Next owner decisions: permit the narrowly proposed test-only stale-count correction and resolve the legacy fixture-host/path qualification; then review F003's operator candidate, topology, protected obligations, resource/seats and literal-envelope confound before its own initialization receipt. Actual initialize/verify output is NOT FOUND; current judge instruction forbids minting. Before L004/v6 minting, freeze completed F003 source evidence and actual admitted rows, budget, O5/calibration, runtime obligations, stop/scoped ceiling, source containment/pins and reopening. No source or provider observations were changed, no durable identity minted, and no git state change was made in the durable checkout. Publication remains separate and withheld by this verdict. Evidence/index and all33 explicit publication paths: work/review11/INDEX.md, REPORT.md and PUBLISH-CHECKLIST.md. C001/A001 and owner main-merge owed items remain unchanged (STATUS.md:738,764).


### W11B judge outcome and orchestrator disposition - 2026-09-16T00:57:31.652694+00:00

The independent judge's REJECT is preserved. The orchestrator approved and root applied the test-only resume patch (git apply --check and git apply exit 0); the six requested modules now pass 283 tests with 2 permitted Windows symlink skips. The single auto_loop run completed 67 tests: 45 passed and 22 recorded MAX_PATH errors, longest failing path 261 characters, with LongPathsEnabled=0; no other failures/errors. This is the orchestrator-disposed host limitation, not a delivery defect or a sh.exe waiver.

Actual F003 throwaway initialize/verify both PASS at C:/tf11/f003-proof. Its plan_id is confined to the throwaway proof and is NOT the study identity; no real initialization occurred. No F003 repair was needed. Append-only proof is in F003/VALIDATION.md; its v6 pin is refreshed and v6 validation passes. Owner decisions remain: envelope confound, operator candidate/task extension, topology/protected obligations, budget/resources/seats, then real initialization under its own receipt. L004/v6 minting follows completed F003 evidence and its actual source/row/budget/launch decisions. Existing C001/A001/main-merge obligations are unchanged.

Bounded fix-up complete locally; publication belongs to the following publisher. No provider calls or Git index/reference changes. Full commands, outputs, exact error paths and the 34-path publisher inventory: work/w11b/INDEX.md and work/w11b/PUBLISH-CHECKLIST.md.


## 2026-09-16T07:14:52.156689+00:00 Self-service reasoning CLI (offline delivery)

REC-20260916-C delivers tools/reason.py and src/minireason/reason/: explicit single-family, cross-family and cross-family-rival recipes; verbatim prose/objection delivery; per-objection return dispositions; dependent use questions; optional bare/native DeepSeek readings; complete personal run records under ignored runs/; terminal-response recovery without replay; explicit transport retries and a300second worker wall. Operator page: docs/workflows/reason-cli.md. This is a personal working tool; its output is a working answer with its objections, not a finding.

Offline verification completed:30reason tests passed;26unchanged docs-pin tests passed; three-cycle baseline CLI run/status/resume succeeded with15calls and60unchanged call JSON files. Initial fixture error and completed-resume key-order defect are preserved with corrections under work/w12; no failed evidence was erased. Inventory covers12mechanisms and24endpoint seats and identifies actual registry src/minireason/data/endpoints.json. No live provider/model/network call, study identity, Git staging, commit or push occurred. Only isolated offline personal fixture identifiers were created. Publication is separate and pending the publisher.

Next steps: publish the reviewed explicit paths in work/w12/PUBLISH-CHECKLIST.md; conduct the first live smoke under its own receipt using work/w12/LIVE-SMOKE.md; then owner use on pasted prose problems. Read work/w12/INDEX.md for all retained investigation, tests, failure evidence and receipt text. Live usefulness and comparative benefit remain unestablished; future comparison needs declared matched multi-call conditions.


### Self-service reasoning CLI judge correction round - 2026-09-16T07:32:21.280573+00:00

REC-20260916-C: independent offline judge corrections applied to per-seat native thinking, tolerant JSON with one recorded schema repair, separate problem/working-answer use derivations, checkable criticism, final open objections and per-cycle dispositions. Final reason suite: 59 passed; unchanged documentation pins: 26 passed. Two-cycle cross-family baseline fixture: 11 calls, 44 unchanged call records after status/resume. Judge evidence: work/review12/INDEX.md and REPORT.md; corrected live plan: work/review12/LIVE-SMOKE.md. Pending: separate publication using work/review12/PUBLISH-CHECKLIST.md, then separately receipted live smoke and owner use. No provider call or Git mutation in this judge round; live benefit remains unestablished.


### REC-20260916-C publisher / REC-20260916-D opening - 2026-09-16T07:46:04.775595+00:00

The approved 22-path CLI delivery is accepted for branch-only publication after preserving AHepi's eleven concurrent commits 94d6f5fa..fd0c4d34 by a verified nonoverlapping fast-forward. Publication is pending. REC-20260916-D is opened prospectively for the two-cycle cross-family baseline live smoke, at most 11 logical calls and one schema repair each, 8192 completion tokens and 300 seconds per call, no transport retry. No provider call occurred in this publisher task. Next: finish both verified branch publication commits, then the separate live operator executes the child-environment launcher and records actual calls, repairs, stop reason and plumbing outcome. No answer-quality claim. No merge to main.


### REC-20260916-C verified branch publication - 2026-09-16T07:47:45Z

The 22-path approved CLI and prospective REC-20260916-D opening are published at c4508af45c1e15b2cafeff3c125f20a5464d1b78, tree cf4236e0c7d6dd2b3eed79257b2e738e89b6968e, on claude/project-state-direction-j5rbun. Non-forced push, fresh fetch, ls-remote and local/remote commit/tree equality passed. AHepi's eleven concurrent commits remain ancestors. The verification acknowledgement is being published separately. REC-D smoke execution is pending; this publisher made no provider calls and no merge to main. Next authorized task belongs to the separate live operator under the recorded smoke limits and child-only credential environment.


REC-20260916-D fix-up status 2026-09-16T08:05:06.148439+00:00: Smoke-1, run 20260916T074920Z-85501e8a21-3958fe, began at 2026-09-16T07:49:20Z and stopped CEILING_HIT after 2 calls and 0 cycles. Bare/off completed with finish_reason stop, 1466 completion tokens and 7.3 s; native/high at max_tokens 8192 ended length after 40.9 s, using all 8192 completion tokens as reasoning with empty public content on the 663-character problem. No answer-quality claim follows. Offline fix-up now ships native ceiling 32768, off/gateway ceiling 8192 and explicit per-seat medium effort, preserves existing run policies, records named baseline failures without stopping the loop, and permits exactly one recorded native-to-off loop fallback at the same ceiling/context. DeepSeek currently maps requested medium to high; reduced internal effort is not established. Required suites pass: 78 reason tests in 23.876 s and 26 docs-pin tests in 0.017 s. All smoke evidence and protected paths remain unchanged. Next authorized step is the separate judge/publisher using work/w12b/PUBLISH-CHECKLIST.md, then separately authorized smoke-2 from work/w12b/LIVE-SMOKE-2.md: normally 11 attempts/188416 completion-token allowance, at most 25 attempts/475136 with repairs and fallbacks at zero transport retries. No provider/model calls, key-value inspection or Git mutation occurred in this fix-up. Publication and smoke-2 remain pending.


### REC-20260916-D w12c offline fix-up - 2026-09-16T08:24:07.329157+00:00

Smoke-2 run 20260916T080745Z-77460d5d32-667b38 stopped CEILING_HIT after 5 attempts and 0 cycles: bare completed after a00 schema failure/a01 repair; native baseline and initial conjecture completed at 32768 (28094 ms and 36561 ms). Qwen c0001-k01 gateway-default/8192 ended length with reasoning present and empty public content after 95530 ms (95.5 s). No answer-quality claim. The local fix preserves w12b, selects 32768 for native/gateway-default and 8192 for off, and uses existing Ollama .native /api/chat endpoints with think:false for shipped seats; Kimi control evidence is FOUND, while Qwen/GLM honoring remains unverified here. Named critic failures now record unavailable and permit continuation with a parsed peer; all critics failed stops with the last code. Named use failures complete the cycle without use objections. Missing critic/use output cannot satisfy early stop. New policy reasoning-exposure-v2 preserves older saved-run behavior. Required offline checks: 98 reason tests passed in 30.800 s; 26 docs-pin tests passed in 0.019 s. Next separately authorized task: review/publish the explicit local checklist and execute a fresh smoke-3 if authorized; this task made no calls or Git changes. Handoff: work/w12c/INDEX.md, PUBLISH-CHECKLIST.md and LIVE-SMOKE-3.md.


### REC-20260916-D judge correction round 2 - 2026-09-16T08:58:32.864785+00:00

APPROVED-AS-CORRECTED for separate publication. Preserved uncommitted w12b+w12c and all three original smokes; no provider/model calls, actual .env read, or Git mutation. Smoke-3 run20260916T082621Z-3aaeecdc85-2af16e completed2 cycles, cycle_budget,13 attempts=11 logical+2 schema repairs;282607ms summed provider elapsed and111752 reported tokens. The loop visibly took up a cycle2 retained-left guard; no superiority over baselines is claimed. Corrected separate local working plus1200-character final objection text, final-use closing return and budget, actual valid-JSON supplemental-field rejection, faithful own-output repair, frozen legacy contracts/resume, and run/resume --env-file with two-name/ignored/untracked validation. Raw-control baseline cause and dropped maintained GLM objection: NOT FOUND. Final exact suites:136 reason tests pass30.421s;26 docs pins pass0.018s. Copies of all three original runs resume with zero dispatch and unchanged calls/configs. Root report and corrections: work/review12b/REPORT.md; all evidence: INDEX.md; exact23-path handoff: PUBLISH-CHECKLIST.md (supersedes w12c); owner commands and measured envelope: OWNER-HOWTO.md. HEAD remains9e42f718e0318f97791b130ee97a02bc2ef9e46a on claude/project-state-direction-j5rbun; empty index. Next authorized task: separate publication, then owner-run new occurrence; new live closing-return/contract behavior is untested. Stop this completed offline judge task; reopen for a concrete boundary/custody/substantive failure or changed requirement. Publication remains pending under this task's no-Git-mutation restriction.


### REC-20260916-D correction publication - 2026-09-16T09:06:19.179009+00:00

The approved 23-path correction is published and verified on claude/project-state-direction-j5rbun at 3993a178256c9553359b78b1ec7f7e18ea12a2d5, tree f61000de8fb8b8153c56a269b4892f5878026ee1. Fresh fetch and ls-remote agree with local HEAD, and local/remote trees match. The accepted offline evidence remains 136 reason tests and 26 docs-pin tests passing; this publisher made no tests or provider calls and did not update main. The separate publication-receipt commit is verified in the publisher handoff. Next task requires the owner's direction; any new live occurrence remains distinct from the preserved three smokes, and new contract/closing-return live behavior is not claimed verified here.


### REC-20260916-E open-language Forge local engineering - 2026-09-16T09:28:58.651801+00:00

Completed the authorized offline integration/adapter work on durable checkout HEAD c1463e0a42521399ba218bafa8a30c60a0c609f5, branch claude/project-state-direction-j5rbun, with no Git mutation, real .env read or provider call. Eight existing pack files matched checksums; nine missing examples were copied exactly; all four freshly generated configs match pack bytes and JSON structure. Corrected one test fixture to the actual routing.evidence/from_tier/object-to schema; original open_inquiry.py and protected Forge/provider/loop/endpoint sources are unchanged.

Exact local results: original combined 24 tests in 0.463s FAILED (errors=10); corrected actual Forge suite 7 tests in 0.250s FAILED (errors=10), now entirely Windows directory-fsync failure. Separate unit suite 15 in 0.077s OK, routes 2 in 0.000s OK. Explicit file-only diagnostic Forge suite 7 in 0.812s OK, never durable qualification. Root live-responder suite 11 in 0.947s OK with scripted transport/no network. Retained diagnostics show critical_return two cycles/eight scripted calls/56 completion tokens and a separate one-call CEILING_HIT with public prefix/failure custody. The actual live CLI refuses this Windows host before dispatch with exit 2, TARGET_FILESYSTEM_DURABILITY_UNAVAILABLE. No local usable Linux/WSL runtime exists; no Linux qualification or live model result is claimed.

Added open_inquiry_live.py, 11 regressions, appended validation and complete owner commands/resource arithmetic. Shared reason worker supplies the 300-second wall and write-once public records; caps are declared on wire and checked against reported usage; no retries/repair/fallback. Forge propagates provider exceptions without RUN_ENDED; adapter and verbatim sidecars preserve them. Programme-grounded first general template is open_turn (four calls/two cycles); alternatives take eight. The preserved examples have null token limits and require a newly bounded bundle for live use.

Next owner-directed tasks: separate review/publisher, then qualify the actual Forge path on a supporting output filesystem/host, select template/endpoint/thinking/budget, and only then launch a distinct live occurrence. Windows execution cannot be enabled within the protected-core/no-OS-change scope. Stop this completed offline engineering handoff with that concrete blocker; reopen on a supporting host, authorized durability engineering or a concrete adapter defect, not on a claim of inquiry exhaustion. INDEX/HOWTO/ERRATA/LESSONS and exact evidence are under work/w13. W13-OWNED-PATHS lists 17 owned paths. Raw PUBLISH-CHECKLIST also contains concurrent untracked R001 study files; w13 did not create/edit/approve those, and PUBLISH-NOTES warns against blanket staging. All earlier ledger/STATUS/activity and pack observation prefixes are preserved; publication remains pending by current instruction.


## Independent JUDGE review13 - 2026-09-16T09:49:53.295788+00:00

REC-20260916-E: local delivery A approved as corrected, retaining the explicit Windows durability blocker. Nine added examples match the source pack exactly; transport/worker/300-second timeout reuse and one intact brief per user message verified. Fresh combined offline suite: 35 tests, ten Forge error cases only, all PermissionError at common.py:258 while opening the directory (line 260 fsync not reached). Actual guard probe exits 2 before socket/provider construction. Supporting-host live qualification remains unperformed.

REC-20260916-F: local R001 draft approved as corrected. Independent blind computations agree with all eight sealed facts and all worker oracles; oracle/run_all.py passes all eight. Clarified P03/P04 conventions, removed P05 evaluation clutter and P07 false-certificate hint; retained answer/oracle facts and re-sealed task hashes. Launcher now accepts an external manifest directory, puts occurrences under runs/, preserves TMP and forwards --env-file to reason.py only in live mode. P01/P02 offline completed four occurrences/eight condition aliases; rerun skipped all terminals with 250 files unchanged, maximum path 118 characters; separate actual nonterminal resume and unopened-path forwarding probes pass. All 18 pinned source files match published c1463e0a. Budget: 216 logical allowances, 560 attempts, 14,417,920 completion-token ceiling; measured-usage scenario roughly 2.50 million total tokens, not a ceiling or price. P04/P06 may be easy; problem difficulty and substantive benefit remain unmeasured.

No R001 provider call or .env read occurred. Next task is the operator's reviewed source/answer freeze and live R001 occurrence under F via run_R001.py --mode live --env-file .env, followed by a cross-lineage reader using the guarded case-level protocol; this JUDGE task does not execute it. Delivery A separately needs a supporting-host real Forge qualification before any live use. No Git state changes or publication were authorized; HEAD/branch are retained and changes remain uncommitted. Full report, raw transcripts, independent scripts, corrections and receipt-grouped publication checklist: work/review13/INDEX.md.


### REC-20260916-E/F approved branch publication - 2026-09-16T10:01:46.038090+00:00

Both review13 deliveries are APPROVED-AS-CORRECTED and selected for the requested branch-only publication: E14 delivery paths, F38 draft paths and three shared receipts, 55 unique paths. Fresh origin/claude/project-state-direction-j5rbun equals the starting c1463e0a42521399ba218bafa8a30c60a0c609f5; no owner advancement or fast-forward is needed. Exact scope, immutable document prefixes, credential-shape and whitespace checks passed. Publication and its acknowledgement are pending remote verification. E is completed engineering with supporting-host Forge qualification still outstanding; F is staged, live run pending. No provider calls or merge to main. Next: verify both publication commits; later live work is outside this publisher task.


### REC-20260916-E/F verified delivery - 2026-09-16T10:04:33.829461+00:00

Published the 55 reviewed paths on claude/project-state-direction-j5rbun at 3c642cbd67086e40336c87e3d83dcc936ffe16b8, tree 4dead437407523d068b2892518e98a1f41dce03d. Non-forced push, fresh fetch, ls-remote and exact local/remote commit/tree equality passed at 2026-09-16T10:03:30Z. Both deliveries were APPROVED-AS-CORRECTED: E is completed engineering with supporting-host qualification outstanding; F is staged, live run pending. Separate acknowledgement publication is being finalized and verified in the publisher handoff. No provider calls, secret reads or merge to main. Next task remains the separate owner-directed live operator/qualification and later cross-lineage reading; none runs in this publication task.


### Owner-requested mirror sync completed - 2026-09-16T10:13:16.345139+00:00

The git-less miniReason-claude-project-state-direction-j5rbun Desktop mirror now matches every tracked blob at fetched published branch commit d80b1d5d4036b8b8912e21b47ac169bda4bd1875 (tree 6dfa939e901355fea7987f7d50269028ecdf92bc). Total verified 9,347; SHA-256 mismatches 0. Created 49, updated 6, unchanged 9,292. No non-exempt leftovers; exempt local files preserved. Receipt: SYNC-RECEIPT-2026-09-16e.md in the mirror. No provider calls or publication; next action only on a new owner sync request or concrete mismatch.


### REC-20260916-F W16 offline corrective engineering - 2026-09-16T10:49:50.555875+00:00

R001 live stopped after three problems: P01/P02/P03 cross and P02-single failed SCHEMA_FAILURE; P01-single completed no_new_objections after one cycle; P03-single is interrupted at c0001-use/a00 with four intents/three outcomes and zero completed cycles. Exact replay finds resolved historical IDs rejected against an empty supplied-ID set, plus extra top-level type in two repairs; all eight finish_reason values are stop, no truncation. New public-working-v2 and detailed error reporting are implemented; launcher preserved-attempt reruns and final offline validation are pending. All original evidence remains unchanged. Next authorized task is finish offline tests/docs/checklist; future owner relaunch will archive failed evidence and allocate new occurrences with versioned source pins. No provider/model calls, .env reads or Git mutations in this fix-up. Existing mirror-sync status above is preserved.


### REC-20260916-F W16 completed local fix-up - 2026-09-16T11:02:57.815604+00:00

Offline fix-up completed and root-reviewed. Exact original-parser replay attributes six failed returns to extra known resolved IDs and two repair returns first to extra type (with the same latent ID mismatch); supplied-ID count is zero for all eight, finish_reason stop throughout. New public-working-v2 requires only new/open dispositions, validates optional known re-dispositions, carries omitted resolved status/reason with explicit history, retains valid top-level extras and propagates precise schema errors through repair/TRACE/RUN/CLI. Demonstrated truncation uses existing ceiling recovery. Launcher v2 archives failed/interrupted attempts byte-for-byte and records fresh identities/source snapshots via --rerun-failed or --rerun PNN:OCC, including unmatched-intent and archive-boundary recovery.

Final required tests: reason discovery 148 tests in 43.222s OK; docs pins 26 tests in 0.018s OK; real offline P01 initial/bulk failed+interrupted rerun/targeted rerun all exit 0 with equal archive hashes. All 353 original R001 files and all 33 sealed task hashes remain unchanged; HEAD/branch/index unchanged, diff check clean. Work/w16 contains DIAGNOSIS, TESTS, RELAUNCH, INDEX, exact PUBLISH-CHECKLIST and errata/lessons. No provider/model call, actual .env read, Git mutation or publication occurred. Next operator action is the documented future live relaunch using --mode live --env-file .env --run-root runs/r001-live --rerun-failed; it archives P01-cross first, skips good P01-single, separately reruns the other failures/interruption, then starts untouched P04-P08. Cross baselines repeat as new observations. Reopen engineering for a concrete custody/parser defect or failed offline check; no reasoning improvement or inquiry exhaustion is claimed.


### REC-20260916-F corrective publication underway - 2026-09-16T11:09:47.435503+00:00

State: corrected; live rerun in progress (owner-reported). The W16 corrective checklist contains 22 exact paths; publication to claude/project-state-direction-j5rbun is underway, with a separate verified-commit/tree acknowledgement to follow. Prior offline completion receipts remain unchanged. The concurrent live operator owns runs/ and study continuation; this publisher does not inspect or change live evidence, start provider calls or merge to main. Next publisher action is verify both non-forced branch pushes and a clean final index/worktree.


### REC-20260916-F corrective commit verified - 2026-09-16T11:11:09Z

State: corrected; live rerun in progress (owner-reported). Published 22 explicit checklist paths at 2564d36bce45181430baac9e20f7cc5e558cf2e5, tree 95024609a2d6117f711c9befb4de3df0941b38be, to claude/project-state-direction-j5rbun. Non-forced push, fresh fetch, ls-remote and exact local/remote commit/tree equality passed. The requested separate acknowledgement commit is pending final publication verification. The concurrent live operator retains study continuation; no runs/ access, provider call or main merge was performed by this publisher.


### REC-20260916-F publication acknowledgement checkpoint - 2026-09-16T18:41:17.137045+00:00

Corrective delivery is completed and verified at 2564d36bce45181430baac9e20f7cc5e558cf2e5, tree 95024609a2d6117f711c9befb4de3df0941b38be. This checkpoint carries the requested separate acknowledgement; its own commit/tree and final remote equality are reported in the publisher handoff and ignored work/w16/publisher-state.json. State: corrected; live rerun in progress (owner-reported). Next authorized substantive task remains the concurrent owner's study continuation and later evidence reading; the publisher task ends only after final remote and clean-tree gates pass.


### REC-20260916-F W15 R001 reading completed locally - 2026-09-16T20:15:04.848029+00:00

The eight guarded readings, SUMMARY and REPORT are complete in experiments/diagnostics/R001-reason-cli-vs-baselines. No completed correct-loop/wrong-native route is witnessed: NATIVE P01-P07 is correct; P08 BARE/NATIVE is CEILING_HIT and undecidable. Both selected loop initial answers already reach the correct required facts. P08-SINGLE visibly repairs its DP completeness argument; archived P02-SINGLE changes38 to41 through a use objection before a later schema stop. Neither meets the predeclared five-conjunct witness. P07 BARE has a correct recap plus a contradictory No; the strict reading and alternative implicit-retraction interpretation are retained for the judge. No harmful correct-to-incorrect loop endpoint transition is observed; the full study comparison is censored, not a fully observed null.

Custody:24 original occurrences,8 archived failures/interruption and16 selected current runs;1314 source files unchanged,3204 exact copied files at50 condition destinations, maximum152-character copied path. Operational total183 logical calls/206 attempts,21 repairs,2 fallbacks;489409 prompt+1254018 completion=1743427 known tokens,6 unknown-usage transport attempts. Current totals131 logical/144 attempts,1153389 tokens,27 cycles; archived completed cycles5. Nine current and four archived critic unavailabilities; no conditional closing calls. Recorded elapsed33078874ms includes a named26927141ms transport outlier whose cause remains unresolved. The archived P03-single inner use provider response is complete/5685 tokens while the outer run remains interrupted. No key value detected by name/context/shape scan; no .env read or hidden-reasoning persistence.

HEAD65a1a45cbf1722f339682488c46d27f5ba236d72, branch claude/project-state-direction-j5rbun and empty index are unchanged. No provider/model call or Git mutation occurred. Next authorized task: separate independent judge, then publisher using work/w15/INDEX.md, PUBLISH-CHECKLIST.md, PUBLISH-NOTES.md and EVIDENCE-PATHS.txt. The repository-wide runs/ ignore rule hides nested custody copies from ordinary status, so the separate exact evidence list is essential; .gitignore is unchanged. Publication remains pending under the current mandate. Reopen the reading for a concrete oracle/task defect, disputed mapping or recovered evidence; a matched/checker-seat successor requires its own preregistration, not an exhaustion claim.


## REC-20260916-F independent JUDGE review15 - 2026-09-16T20:39:06.812033+00:00

Delivery A (R001 reading/report): APPROVED-AS-CORRECTED. Delivery B (published2564d36b +65a1a45c return-contract fix): APPROVED-AS-CORRECTED; additional code defect NOT FOUND. All32 table cells independently verified; P07 BARE remains incorrect under PLAN's no-contradictory-assertion rule, P08 baselines remain undecidable at CEILING_HIT, and both P08 loops are correct. Ten draft documents corrected with61 exact old-to-new records: archive-specific predicates/comparators, resolved P07 mapping, P04 quotations/category, FW5 citation precision, neutral wording and GLM diagnosis. All9 selected unavailable GLM critics are output-length CEILING_HIT at8192 tokens with think:false, not schema/transport;12 self-withdrawing raw objects in8 attempts are confirmed. The3 episodes retain their narrow categories and the five-conjunct witness is NOT FOUND.

Independent custody:3204 byte-equal copies of1314 originals;80/80 archived P02-cross pre-fix hashes match. Eight original schema failures parse under v2 without answer changes; all21 saved repairs reconstruct exactly. Required offline suites pass148 reason +26 docs-pin tests. No additional source edits, provider/model calls, .env reads, Git mutations or R002/w18 content access. HEAD remains65a1a45cbf1722f339682488c46d27f5ba236d72 and the index is empty. Review notes, transcripts, original drafts, corrections, tests and REPORT/INDEX are under work/review15. Next authorized task: separate publisher reviews the filtered PUBLISH-CHECKLIST and explicit ignored-custody EVIDENCE-PATHS, publishes the judged delivery, and preserves R002 for its own handoff. No publication is claimed here.


### REC-20260916-F judged R001 publication underway - 2026-09-16T20:45:58.485731+00:00

Delivery A and the already-published Delivery B are APPROVED-AS-CORRECTED; no further source-code fix was required. The publisher reviewed3275 paths: REPORT, ten readings, three append-only records and3261 custody files. Fresh origin equals65a1a45cbf1722f339682488c46d27f5ba236d72; no fast-forward was needed. R001 retains no witnessed completed correct-loop/wrong-native error correction, P01-P07 baseline sufficiency and P08 censoring. Branch-only publication and separate verified acknowledgement are pending; no provider calls or main merge. R002 and work/w18 remain with the concurrent worker. Next: verify both requested pushes and hand off; further inquiry requires its separately authorized scope.


### REC-20260916-F R001 delivery verified - 2026-09-16T20:48:40.570644+00:00

Published3275 approved paths on claude/project-state-direction-j5rbun at 81bc2a76f25384fc77cebcafc3899b24e3373003, tree f0a540c993e9fb6e6bfc9fe92fb5a34eb1da135a. Non-forced push, fresh fetch, ls-remote and exact local/remote commit/tree equality passed at 2026-09-16T20:47:50Z. Delivery A is complete; the approved published Delivery B required no additional code correction. The negative endpoint finding and P08 censoring remain unchanged. This separate acknowledgement checkpoint is pending its own remote verification, which will be reported with final Git status and .env tracking check in the publisher handoff. Next authorized work remains the concurrent R002 worker scope or a separately directed follow-up; no provider calls or main merge occurred.


### MIRROR-SYNC-20260917a complete - 2026-09-16T21:09:17.814387+00:00

The designated git-less OneDrive mirror now matches all12621 tracked files at published branch claude/project-state-direction-j5rbun commit 0dc9182ebeb4dd350854cdbd229e5faf988d94ca, tree 40f2204ef35d2b17bd7196263ef444514b87b930. Copy counts:3274 created,20 updated,9327 unchanged. Independent fresh git-show SHA-256 verification:12621 verified,0 mismatches. No unexpected leftovers; allowed .env, work/ and sync markers preserved. Receipt: SYNC-RECEIPT-2026-09-17a.md in the mirror root. No provider calls or Git publication. Mirror task complete; existing concurrent research/publication scope is unaffected.


## 2026-09-16T21:34:45.127675+00:00 - REC-20260917-A: R002 episodes under calibrated difficulty (draft), review16

Independent judge verdict: **APPROVED-AS-CORRECTED for publication as a draft**. All24 original sealed answers independently agree; oracle disagreements NOT FOUND; problems replaced0. All six binding orchestrator amendments and the realistic-budget/optional-companion addendum are applied in R002 PLAN/INSTRUMENT/contracts/recipes/reading protocol, with append-only CHANGES rounds. Default five-condition target8 envelope:480 combined strict attempts/11010048 completion maximum; R001-derived working estimate384 calls/about1.95M completion, explicitly uncertain planning allowance2-5M. Calibration remains24 once-only NATIVE32768 calls; no-answer CEILING_HIT is eligible. Final offline C01 calibration/main and verified resume pass;11 launcher tests,12 schemas and7 recipes pass. No provider/model call, .env read, git mutation, live scientific run or episode. Current engine/checker live qualification remains NOT FOUND.

Handoff: work/review16/INDEX.md and REPORT.md, exact corrections/oracle recomputations, final launcher pastes, restricted PUBLISH-CHECKLIST.md; R002 VALIDATION-REVIEW16.md and MATERIAL_PINS-REVIEW16.json identify corrected bytes. HEAD as found remains0dc9182ebeb4dd350854cdbd229e5faf988d94ca; existing concurrent work and docs prefixes preserved. Next authorized task is separate publisher review/publication of these explicit draft paths; separate engineering must implement/qualify v2 before any later live authorization. Inquiry is not exhausted.


### REC-20260917-A draft publication - 2026-09-16T21:39:57.381829+00:00

Independent verdict APPROVED-AS-CORRECTED for publication as a draft confirmed; exact191-path scope and remote base checks passed. Publisher is preparing188R002 files plus the three append-only documentation records on claude/project-state-direction-j5rbun. Calibration pending; no provider calls, study execution or live qualification. Next authorized action: verify the draft commit and its separate publication acknowledgement. Further engineering/live work remains separately authorized.


### REC-20260917-A draft published; calibration pending - 2026-09-16T21:42:47.376117+00:00

Published191approved paths (188R002 plus three appended documentation records) on claude/project-state-direction-j5rbun at f3d6ea4fe7712f748adf799f71417a2445ec1163, tree 926c370407c1352444f3b2c5c76b553c449a435a. Non-forced push, fresh fetch, ls-remote and exact local/remote commit/tree equality passed at 2026-09-16T21:41:35Z. R002 remains a DRAFT under the independent APPROVED-AS-CORRECTED verdict; calibration and live engine/checker qualification remain pending. No provider calls, study execution or main merge. This separate acknowledgement is pending its own remote verification, reported in the final publisher handoff. Next work requires the separately authorized engineering/qualification scope before any live calibration.


### Mirror synchronization completed ? 2026-09-16T21:55:21.228463+00:00

MIRROR-SYNC-20260917b: the named OneDrive claude/project-state-direction-j5rbun mirror now matches all12809 tracked files at published commit `c61a04e269fdee60aa5b576def89e642ecd523d4`, tree `297672509ebc0925f3858fcac09377f0d79a3bed`. Created188, updated3, unchanged12618; independent fresh Git-show byte verification reports SHA-256 mismatches0. Requested SYNC-RECEIPT-2026-09-17b.md written and checked. No untracked leftovers outside preserved .env, mirror markers and work/. No provider calls or publication/staging of concurrent checkout edits. This bounded mirror task is complete; a later published head or concrete mismatch would justify another synchronization. Concurrent implementation status is unchanged.


### R002 offline engineering complete - 2026-09-16T22:32:19.425840+00:00

REC-20260917-A / root-w20: Engineering completion: implemented the judged R002 strict CLI/contracts and full schema request supply, fork-bound objections/checked returns, tail detection, tested and same-lineage recoded/carrier instruments, offline checker subprocess containment with exact evidence binding, stall instrument switches, immutable episode/readout counters, and the mutable calibration/main launcher with source-versioned resume/rerun custody. Required offline discovery passed 212 tests and documentation pins passed 26. Fresh standalone C01/C02 calibration, all five main conditions and both resumes passed with 560 phase files unchanged; final manifest pins equal current sources. Independent checker custody review closed its concrete finding after repair. Published draft files remain unchanged except this authorized VALIDATION append. No live call, root .env access or Git mutation occurred. Remaining work is the separate judge/publisher, then separately receipted 24-call live calibration with reviewed capability/local tokenizers; live CHECKER additionally needs qualified OS isolation. This bounded offline mandate is complete subject to final read-only scope audit; it is not scientific exhaustion or evidence of comparative benefit. Handoff evidence and exact future detached calibration command: work/w20/INDEX.md. Publication is intentionally pending because this mandate prohibits all Git mutations; the separate judge and publisher follow.


W20 scope correction - 2026-09-16T22:34:08.005009+00:00: The final byte-level audit found that the raw Git index hash differs from its opening fingerprint. HEAD and branch remain unchanged, and git diff --cached --exit-code --quiet HEAD returns 0: staged contents still exactly equal HEAD. W20 used only read-only Git verbs; such commands may refresh index stat-cache metadata, and exclusive attribution versus concurrent writers is unproven. No restoration or Git mutation command was attempted. Subsequent reads set GIT_OPTIONAL_LOCKS=0 and preserve the current index bytes. Earlier blanket no-Git-mutation statements mean no explicit mutating command; raw-index byte preservation was not achieved. Evidence: work/w20/INDEX-CACHE-OBSERVATION.json and SCOPE-AUDIT-INITIAL.json. This exception does not change source/test results or permit publication in this task.


## 2026-09-16T23:15:16.367059+00:00 - REC-20260917-A root-review20 independent JUDGE

APPROVED-AS-CORRECTED for publication of the uncommitted R002 engineering delivery. Final reason225 and docs-pin26 tests pass; corrected-source tools/run_R002.py offline calibration C01/C02, main C01 all five conditions, exact resumes and separately preserved failed-predecessor rerun pass. Profiler/frame sandbox escape was reproduced and repaired; all12 final hostile cases plus original exploit replay/runtime denial regressions pass. LOOP-CHECKER runnable on this Windows CPython3.11.9 host WITH ITS DECLARED LIMITS, verbatim in reason-cli workflow and R002 VALIDATION.

Capability supplied at work/review20/reviewed-engine-capability.json with exact schema/recipe digests and REC-20260917-A; unnecessary hand-made calibration tokenizer prerequisite removed in favor of independently reproduced pinned exact24-wire proof. Corrected public-serializer counts940-1192; future calibration remains24 native calls, completion ceiling786432, no retries. Final command and follow-up reading: work/review20/CALIBRATION-LAUNCH.md. Main dynamic tokenizer pins remain future work. No provider/model calls or .env read occurred. No git mutation/publication was attempted under the explicit judge restriction; HEAD/index/branch unchanged. Next: separate publisher reviews explicit PUBLISH-CHECKLIST paths and review receipt, publishes normally with verification, then a separately authorized operator may run the prepared calibration command. Full findings, limits, NOT FOUND results and reopening conditions: work/review20/REPORT.md.


Final audit supplement: Cadence correction at actual UTC: the final timer audit found a substantive-receipt gap of 324.051136 seconds from 2026-09-16T23:02:38.438303+00:00 to 2026-09-16T23:08:02.489439+00:00. This missed the300-second requirement by 24.051136 seconds. The explicit elapsed checks did not catch it before the deadline; do not backdate or describe cadence as continuously met. No publication deadline applies because the current judge explicitly forbids Git mutation. Engineering test/integrity results are unaffected. Final scope audit otherwise passed169 protected files, six append-only prefixes, unchanged HEAD/branch/raw index,32 filtered publication paths, zero credential-shaped literals or UTF8 errors and verbatim limits in workflow/VALIDATION/REPORT. Stop after recording this correction and handing back the bounded engineering verdict; reopening conditions are in REPORT.


### REC-20260917-A instruments publication prepared - 2026-09-16T23:21:49.275601+00:00

Independent judge verdict APPROVED-AS-CORRECTED accepted for the exact32 checklist paths. Final judged tests:225 reason and26 documentation-pin passes; reviewed offline calibration/main/resume/rerun evidence retained. Publisher scope, encoding, credential-shaped and whitespace checks passed; origin equals H0 c61a04e269fdee60aa5b576def89e642ecd523d4. Instruments commit and verified branch publication are pending. Calibration remains pending and requires its separate authorization; this publisher makes no provider calls and does not merge to main.


### REC-20260917-A instruments published; calibration pending - 2026-09-16T23:24:09Z

Published32 reviewed paths to claude/project-state-direction-j5rbun at 46b550789f1ef2127ff3cc8591d0e6ac9f4ca4ce, tree 7e6ea3d468675a0a6590274fb8a65479b250dd62. Non-forced push, fresh fetch, ls-remote and exact local/remote commit/tree equality passed at 2026-09-16T23:23:04Z. Judge verdict APPROVED-AS-CORRECTED; final judged225 reason and26 documentation-pin tests pass. This acknowledgement is pending its separate commit/push/verification, reported in the final publisher handoff. Instruments published; calibration pending. No provider calls or main merge. Next substantive task is separately authorized calibration under the judged capability/proof and host limits.


### REC-20260917-A guarded R002 calibration admission - 2026-09-17T00:01:18.982116+00:00

Guarded reader root-w21 (OpenAI lineage distinct from DeepSeek) completed all24 CAL-NATIVE readings:20 correct,0 incorrect,4 not answered,0 unresolved; all24 terminal and custody-complete. Admit C05,C06,C09,C12 under the pre-registered1-7 underfill rule (target8); each has CEILING_HIT/length and no usable public final answer. No derivation-only case qualifies.24 original calls/attempts report24995 prompt,363057 completion including344049 reasoning,388052 total tokens; provider elapsed1384.867s, supervised1392.677s, no wall breach. No claim beyond admission.

New calibration/CNN.md, ADMISSION.md and launcher-compatible admission.json are complete; pure live-schema validation returns the four IDs.700 trial files were copied unchanged to study runs/calibration/CNN with2 original provenance copies and a SHA-256 manifest; source/current reference pins and copied hashes match, maximum absolute path155, no secret-shaped credential values or native hidden reasoning retained. Source runs/ untouched. Work notes, inventory, custody and detached command: work/w21/INDEX.md. No provider/model endpoint call, .env read, git mutation or main launch was performed by this reader. Next: separate judge and publisher, then a tokenizer-qualification operator must produce reviewed calibration/main-tokenizer-pins.json for DeepSeek, Qwen and GLM dynamic prompts; the reviewed capability is already present. Main remains unlaunched. Reopen this reading only for a concrete requested-fact/proof/custody defect; do not rerun calibration or tune the pool.


W21 publication handoff supplement - 2026-09-17T00:04:14.313836+00:00: The requested filtered porcelain checklist contains29 paths, but existing ignore rules omit the703 new study custody files. The later publisher must also include the explicit work/w21/CUSTODY-PUBLISH-PATHS.txt list; publishing only the porcelain list would omit calibration custody and break the relative evidence links. No ignore/index change was made. Final root rehash passes1400 source/destination checks and188 protected study files; HEAD/branch/index and append-only prefixes pass. All916 additional long-string heuristic hits resolve to existing manifest path substrings, with no unresolved secret-shaped value.


### REC-20260917-A independent review21 JUDGE - 2026-09-17T00:22:17.416498+00:00

REJECT complete launch-ready delivery; calibration admission itself confirmed:20 correct,0 incorrect,4 not answered (C05,C06,C09,C12),0 unresolved. All24 public/sealed readings and decisive quotes checked by root; underfilled ordered set unchanged.700 copied trial files and2 provenance copies match;24 terminal trials report24995 prompt+363057 completion=388052 total, reasoning344049 included. Existing reader records are append-only and truthful; live-launcher-authored ledger/STATUS/activity appends NOT FOUND (run manifest/phase receipts do exist and reconcile). No missing historical receipt is fabricated.

PLAN6:154/7:168 requires input preflight, so main tokenizer gate retained. main-tokenizer-pins.json, transformers, and pinned Qwen/GLM tokenizer assets NOT FOUND; no truthful pins or certified runnable live command can be produced from installed material. Strict initial CEILING_HIT stops after1call/0cycles with no fallback; valid cannot_decide can enter a cycle, but is not synthesized from empty output. Main would yield no critical episode if the initial ceiling pattern repeats. Fresh main NATIVE remains required.

Applied only narrow C:/tr21 launcher output-root correction with boundary regression; actual tools/run_R002.py offline main consumed the exact admission across all20 case/condition occurrences,100 scripted calls,0 provider calls, allsaved hashes verified. Reviews, corrections, probes, blocked complete command syntax,180-call realistic working estimate and228-call hard envelope are under work/review21/INDEX.md and REPORT.md. No runs modification, .env read, Git mutation or publication. Next: resolve exact dynamic tokenizer/template/package qualification and prospectively decide any changed failure mechanism; separate publisher must include31 filtered paths plus703 ignored custody paths.

Review21 final audit acknowledgement - 2026-09-17T00:29:19.432628+00:00:751 original live-run files and700 copied trial files+2 provenance copies unchanged; HEAD/branch/raw index and append-only initial/HEAD prefixes pass.31 filtered paths and703 ignored custody paths retained. All2740 generic long-string findings explicitly resolve to actual paths, SHA256 annotations or public arithmetic; no unresolved credential value. Final substantive cadence maximum293.95415s, no overdue interval. Review stops with correct admission and REJECT main readiness on the documented missing qualification; no provider, .env, Git or runs mutation.


### REC-20260917-A calibration publication prepared - 2026-09-17T00:36:26.951022+00:00

Publisher accepts only the independent judge calibration/admission/custody pass under the owner split-verdict clarification. Publication scope is31 checklist paths plus703 immutable study custody files (734 total). Calibration24 calls:20 correct,0 incorrect,4 not answered; admission C05,C06,C09,C12 unchanged. Main phase remains unlaunched and blocked pending preflight bound and decomposition arm (REC-20260917-A continuation). Judge documentary records are retained in these appended records; work/review21 originals remain local and unstaged as directed. No provider calls or main merge. Next authorized publisher step: commit, non-forced branch push, exact remote verification and separate acknowledgement; substantive main work needs its own continuation receipt.
