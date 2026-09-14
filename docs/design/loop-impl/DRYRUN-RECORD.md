# The offline dry run, executed through the CLI — the record

The acceptance proof (`tests/loop/test_dry_run_end_to_end.py`) drives the same
`dry_run` entry in-process with the nine induced failures. **This file records
the other half**: the plain command an operator types, run end to end against a
real temporary checkout and a real temporary bare remote, with every provider
offline and no induction at all — the rehearsal that must pass before a live
run is authorised.

Everything below is verbatim. Nothing was written outside the temp tree,
nothing was committed in `scratchpad/loop-impl/repo`, no provider call was
made, and no credential was read, named or printed.

---

## 1. What the tree was, and why it is not the clone

The loop cannot run from a wheel and cannot run against a tree it is not
dispatching for: runner v2 publishes `Path(__file__).resolve()` as an input of
every wave and resolves it **inside the repository it is sending for**, so the
driver must be executed from a checkout of that repository. The rehearsal
therefore runs in a throwaway checkout with its own bare remote, prepared by
this script (ruling 8: repo copies are made with `git clone`, never a tar of a
working tree; the loop tree is untracked in the clone, so it is copied across
afterwards):

```sh
#!/bin/sh
# W6-DRYRUN — the operator's offline rehearsal, exactly as recorded in
# loop-impl/DRYRUN-RECORD.md.  Nothing here touches /home/user/miniReason and
# nothing here reads or names a credential.
set -eu
CLONE=/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-impl/repo
SCRATCH=/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad
TMP=${1:?usage: prepare_dry_run.sh <temp root>}

rm -rf "$TMP"
mkdir -p "$TMP"
git init --bare --initial-branch=main "$TMP/remote.git" >/dev/null
git clone --quiet "$CLONE" "$TMP/checkout"
# The loop tree is untracked in the clone, so it is copied across (ruling 8:
# git clone or rsync --exclude .env, never a tar of the working tree).
# (no rsync on this host; cp -a with .env excluded by construction - the loop
# tree carries none, and the clone itself was made with git clone.)
mkdir -p "$TMP/checkout/src/minireason/loop" "$TMP/checkout/tests/loop"
cp -a "$CLONE/src/minireason/loop/." "$TMP/checkout/src/minireason/loop/"
cp -a "$CLONE/tests/loop/." "$TMP/checkout/tests/loop/"
cp "$CLONE/tools/auto_loop.py" "$TMP/checkout/tools/auto_loop.py"
cp "$CLONE/docs/workflows/automated-loop.md" "$TMP/checkout/docs/workflows/automated-loop.md" 2>/dev/null || true
find "$TMP/checkout" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true

cd "$TMP/checkout"
git config user.name "W6 dry run"
git config user.email "w6-dryrun@example.invalid"
git config commit.gpgsign false
git remote remove origin
git remote add origin "$TMP/remote.git"

# The endpoint registry the dry run's seats are named from: synthetic's own,
# written through synthetic so no endpoint spelling is retyped.
PYTHONPATH="$PWD/src" python3 - <<'PY'
import json
from pathlib import Path
from minireason.loop import synthetic

# The two delivery endpoints are synthetic's own, because arms.json names
# them.  W1-SEATS refuses one endpoint in two seats, so the five seat roles
# get five endpoints of their own over five lineages and five credential
# NAMES - the shape tests/loop/test_auto_loop.py uses, and for its reason:
# one process holds one key_gate registry and a credential at two caps is
# refused.  No credential is read here; only names are written.
document = json.loads(json.dumps(synthetic.endpoints_document()))
for role in ("critic", "defender", "judge-a", "judge-b", "variator"):
    document["endpoints"].append({
        "name": "dryrun/" + role,
        "base_url": "https://" + role + ".dryrun.invalid/v1",
        "model": "dryrun-" + role + "-1",
        "key_env": "DRYRUN_" + role.replace("-", "_").upper() + "_KEY",
        "family": "dryrun/" + role + "-lineage",
        "chat_path": "/chat/completions",
        "native": False, "max_concurrency": 5, "timeout_seconds": 120,
    })
Path("src/minireason/data/endpoints.json").write_bytes(
    json.dumps(document, indent=1, sort_keys=True).encode())
PY

# The config: loop-prereg/config.json with the study-specific declarations
# replaced by the synthetic ones, and provider_mode offline.
PYTHONPATH="$PWD/src" python3 - "$SCRATCH" <<'PY'
import json, sys
from pathlib import Path
from minireason.loop import synthetic

scratch = Path(sys.argv[1])
config = json.loads((scratch / "loop-prereg" / "config.json").read_text())
run_id = "DRYRUN-2026-09-14-offline"
config["run_id"] = run_id
config["study"] = ("the offline dry run of the automated loop: L001's frozen "
                   "declarations over the synthetic occurrence and its "
                   "contrast leg, with every provider offline")
config["occurrences"] = ["occurrence-01"]
config["publish_ref"] = "origin/main"
config["reading_set"] = [
    "h005-row/{}#{}/{}/{}".format(*identity)
    for identity in synthetic.READING_COORDINATES.values()]
config["obligations_path"] = f"experiments/loops/{run_id}/obligations.json"
config["graph_root"] = f"experiments/loops/{run_id}/graph"
config["seats"] = {"critic": "dryrun/critic", "defender": "dryrun/defender",
                   "judges": ["dryrun/judge-a", "dryrun/judge-b"],
                   "variator": "dryrun/variator", "min_judge_families": 2,
                   "paraphrase_n": 2, "schema_repair_budget": 0}
config["contrast"] = {"attached": True, "study": "contrast-study",
                      "occurrences": ["contrast-study/occurrence-01"]}
config["provider_mode"] = "offline"

run_root = Path("experiments/loops") / run_id
run_root.mkdir(parents=True, exist_ok=True)
for name in ("obligations.json", "calibration.json"):
    (run_root / name).write_bytes((scratch / "loop-prereg" / name).read_bytes())
Path("dry-run-config.json").write_bytes(
    json.dumps(config, indent=1, sort_keys=True).encode())
seats = {row["name"] for row in json.loads(
    Path("src/minireason/data/endpoints.json").read_text())["endpoints"]}
missing = [s for s in [config["seats"]["critic"], config["seats"]["defender"],
                       *config["seats"]["judges"], config["seats"]["variator"]]
           if s not in seats]
print("seats missing from the registry:", missing)
PY

git add -A
git commit -q -m "the tree the offline dry run is published from"
git push -q --set-upstream origin HEAD:refs/heads/main
echo "prepared $TMP/checkout"
```

Run as:

```
sh scratchpad/w6/prepare_dry_run.sh <temp root>
```

### What the config carries from `loop-prereg/config.json`, and what it replaces

Carried **verbatim** from the pre-registered L001 config: `schema`, `runner`,
`cycle_budget` (3), `max_calls` (396), `reopen_reasons`, the whole `audit`
block including both settled accounts, the whole `timeouts` block, and
`max_per_key`. The run root also carries `loop-prereg/obligations.json` and
`loop-prereg/calibration.json` **unmodified**, so the obligations the dry run
evaluates and the calibration set its audit window reads are the
pre-registered ones.

Replaced, and only these, because each names the live world this rehearsal must
not touch:

| key | replaced with | why |
|---|---|---|
| `run_id` | `DRYRUN-2026-09-14-offline` | a run root of its own |
| `study` | the dry run's own sentence | it is not L001 |
| `occurrences` | `["occurrence-01"]` | the synthetic occurrence `dry-run` stages |
| `contrast` | `contrast-study/occurrence-01` | the synthetic contrast leg it stages |
| `reading_set` | `synthetic.READING_COORDINATES`' eight rows | the H005 rows name records this tree does not carry |
| `seats` | five `dryrun/*` endpoints over five lineages | W1-SEATS refuses one endpoint in two seats, and the two synthetic endpoints are the delivery arms' |
| `publish_ref` | `origin/main` | the temp bare remote |
| `obligations_path`, `graph_root` | under the temp run root | the run writes only inside its own tree |
| `provider_mode` | `offline` | the mode is inside `loop_plan_id`; a flag cannot change it |

**No key name was needed anywhere.** The endpoints this run declares are
`SYNTHETIC_ALPHA_KEY`, `SYNTHETIC_BETA_KEY` and five `DRYRUN_*_KEY` names, and
`env | grep -cE '^(DRYRUN_|SYNTHETIC_)'` printed `0` in the shell that ran the
command. The walk completed anyway, which is the point: in offline mode the
driver reads no credential and the provider module never constructs a live
transport, so an operator rehearsing a live run needs nothing in the
environment at all.

---

## 2. The command, and its exit code

```
cd <temp root>/checkout
PYTHONPATH=$PWD/src python3 tools/auto_loop.py dry-run \
    --config dry-run-config.json --dry-run-out <temp root>/out
```

```
PLAIN EXIT=0
```

Standard output and standard error were both **empty**: the driver prints
nothing on success and writes its verdict to `--dry-run-out`.

### The same command under a provider-module counter

To make "zero provider network calls" a fact about the module rather than an
absence of evidence, the identical `main(...)` entry was invoked once more on a
fresh temp tree with `provider_openai_compat._open`, `socket.socket` and
`socket.create_connection` replaced by refusals and a counter on the provider
module's own two classes (`scratchpad/w6/counted_cli.py`):

```
EXIT 0
provider module: live transports constructed = 0 | requests opened = 0 | offline providers constructed = 218
```

Zero live transports, zero opened requests, and a positive offline count, so
"nothing networked" cannot pass as "nothing ran".

---

## 3. What the one command did

`dry-run` staged the synthetic material every occurrence the config names,
walked **S0 PREREGISTER** and **S1 PREFLIGHT** because the run carried no plan,
and then walked S2 through S15. 43 step receipts, 11 of them
publications, each with its own `VERIFIED` sidecar:

```
0001-PUBLISH_PLAN.json
0002-CYCLE_OPEN.json
0003-PREPARE.json
0004-PUBLISH_IN.json
0005-SEND.json
0006-PUBLISH_EV.json
0007-PREPARE.json
0008-PUBLISH_IN.json
0009-SEND.json
0010-PUBLISH_EV.json
0011-PREPARE.json
0012-PUBLISH_IN.json
0013-SEND.json
0014-PUBLISH_EV.json
0015-PREPARE.json
0016-IMPORT.json
0017-USE_TABLE.json
0018-READ.json
0019-MARK.json
0020-ADJUDICATE.json
0021-DECIDE.json
0022-PUBLISH_CY.json
0023-CYCLE_OPEN.json
0024-PREPARE.json
0025-IMPORT.json
0026-USE_TABLE.json
0027-READ.json
0028-MARK.json
0029-AUDIT.json
0030-ADJUDICATE.json
0031-DECIDE.json
0032-PUBLISH_CY.json
0033-CYCLE_OPEN.json
0034-PREPARE.json
0035-IMPORT.json
0036-USE_TABLE.json
0037-READ.json
0038-MARK.json
0039-ADJUDICATE.json
0040-DECIDE.json
0041-PUBLISH_CY.json
0042-CLOSE.json
0043-PUBLISH_CY.json
```

First and last `VERIFIED` lines, verbatim:

```
VERIFIED 8d8ad6773d70e8bc809e72d8dcce656d0a654b39 TREE 3612a1ceb10773b8bd6ffb295be5b645e67a7552 at 2026-09-14T20:34:52Z local=8d8ad6773d70e8bc809e72d8dcce656d0a654b39 remote=8d8ad6773d70e8bc809e72d8dcce656d0a654b39 ref=origin/main paths=7
VERIFIED 519db70095f3287a277b7c21f44cc82164e55a07 TREE e60955e86b0498d2478e5c4dd0bbf4d589cce8e9 at 2026-09-14T20:35:00Z local=519db70095f3287a277b7c21f44cc82164e55a07 remote=519db70095f3287a277b7c21f44cc82164e55a07 ref=origin/main paths=1
```

The bare remote's `refs/heads/main` is `519db70095f3287a277b7c21f44cc82164e55a07` — the commit the last
publication recorded, so every git operation really went through `publish()`
against a real repository.

---

## 4. `dry-run.json`, the verdict

The whole verdict with the two large sub-records (`preregister.opened_cells`
and the full `preflight` check list) summarised; the file itself is at
`<temp root>/out/dry-run.json`.

```json
{
 "induced": [],
 "inducible": [
  "provider_arm_failure",
  "custody_mismatch",
  "step_timeout",
  "ensemble_split",
  "paraphrase_flip",
  "non_unique_offset",
  "decisive_point_absent",
  "baseline_kind_collision",
  "reread_without_reason",
  "appellate_ruling"
 ],
 "occurrence": "/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/w6/dryrun/out/occurrence",
 "preflight": {
  "loop_plan_id": "4fac89d95f097d9e86b37153f0c7a7deacfc3b8cfc16477552b3d40b839fc293",
  "max_calls": 396,
  "mode": "offline",
  "planned_calls": 232,
  "provider_calls": 0
 },
 "preregister": {
  "calibration_sha256": "eaf41d3eed98f7ba839ab604367c3daf3f92d7cf07a658694bd9cdd5539a5e38",
  "cycle_budget": 3,
  "loop_plan_id": "4fac89d95f097d9e86b37153f0c7a7deacfc3b8cfc16477552b3d40b839fc293",
  "preregistration_receipt": "REC-20260914-V"
 },
 "ran": true,
 "run": {
  "closing": {
   "closing": "/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/w6/dryrun/checkout/experiments/loops/DRYRUN-2026-09-14-offline/CLOSING.md",
   "loop_plan_id": "4fac89d95f097d9e86b37153f0c7a7deacfc3b8cfc16477552b3d40b839fc293",
   "stop_reason": "no_new_reading_changes"
  },
  "cycles_completed": 3,
  "loop_plan_id": "4fac89d95f097d9e86b37153f0c7a7deacfc3b8cfc16477552b3d40b839fc293",
  "stop_reason": "no_new_reading_changes"
 },
 "seed": 9005,
 "staged": {
  "contrast": [
   "contrast-study/occurrence-01"
  ],
  "occurrences": [
   "occurrence-01"
  ]
 }
}
```

`preflight` in full, as written:

```json
{
 "checks": [
  {
   "check": "pins",
   "findings": [],
   "pins": 20
  },
  {
   "check": "seats",
   "digest": "5cb3b14a6f2409712758f2640b50f981b0e9b18044ac6245618bc06d221c9113",
   "panel": [
    "judge#1",
    "judge#2"
   ]
  },
  {
   "check": "reading_cells",
   "rows": 8
  },
  {
   "check": "block_streak",
   "definition": "consecutive guard blocks per role, over that role's trials in dispatch order within the reading arm, reset by any trial of that role whose outcome is not a block"
  },
  {
   "cells": 16,
   "check": "register_cells"
  },
  {
   "anchors": 5,
   "calibration_sha256": "eaf41d3eed98f7ba839ab604367c3daf3f92d7cf07a658694bd9cdd5539a5e38",
   "check": "calibration"
  },
  {
   "audit_allowance": 164,
   "check": "planned_calls",
   "mark_cells": 16,
   "mark_cost": 9,
   "planned_calls": 232,
   "row_cost": 11,
   "row_cost_arithmetic": "1 critic + 1 defender + 2 judges + 2 order-swapped + 1 variator + 2 judges x 2 paraphrases = 11",
   "rows": 8
  }
 ],
 "loop_plan_id": "4fac89d95f097d9e86b37153f0c7a7deacfc3b8cfc16477552b3d40b839fc293",
 "max_calls": 396,
 "mode": "offline",
 "planned_calls": 232,
 "provider_calls": 0,
 "schema": "minireason.loop.preflight.v1",
 "status": "OK"
}
```

Read off it: the mode is `offline`, `provider_calls` is `0` **before** anything
was dispatched, and the planned figure `232` is inside the pre-registered
`max_calls` `396`, with the arithmetic printed beside it rather than asserted.

---

## 5. `CLOSING.md`, the closing receipt, verbatim

```markdown
# Closing record - 4fac89d95f097d9e86b37153f0c7a7deacfc3b8cfc16477552b3d40b839fc293

- loop_plan_id: 4fac89d95f097d9e86b37153f0c7a7deacfc3b8cfc16477552b3d40b839fc293
- ceiling_sha256: 1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e
- ceiling_pinned_at: src/minireason/loop/data/ceiling_v1.md

## the frozen ceiling block

CEILING.md is pinned into the plan at sha256 `1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e`. Every invariant sentence of it is printed verbatim below; the per-cell claim template it also carries is a clause a cell asserts and this table states no cell's claim.

**This run cannot claim FW5:628's witness of reason use.** A transcript supplies no structural map from the represented objection organization into a response suborganization preserving internal role bindings on an active dependency route, and neither does an ensemble of readers of that transcript. The strongest positive outcome available is *consistent-with*.

**A null on the recoding or the carrier leg leaves those rival explanations unrefuted and unsupported, not excluded.** At N = 5 this is a limit of the design, not a finding.

**Agreement between two cross-family readers is agreement between two conditioned generators, not corroboration by two independent observers.** The guard measures behavioural stability under paraphrase, order and adversarial answer — not truth. Ten `family` labels over 24 endpoints and two credentials is a delivery fact, not an independence proof.

**An unresolved cell proves neither presence nor absence** (FW5:634). Ended arms, guard blocks, PARTIAL deliveries, bare-token ambiguity and under-replication are silent about content; non-evaluability is not refutation.

**Three cell states are distinct and are printed as three things.** An *unread* cell is one nobody and nothing has read. An *unresolved* cell is a deliberate reading that stays unresolved. A *machine-unresolved* cell is one the guard declined to resolve, and it names the block code that declined it. Conflating any two would let an unfinished worksheet read as a finding.

**A high block rate is the instrument declining to read. It is never an absence of relations.** The block register by reason code — `ensemble-split`, `referential-integrity`, `operative-target`, `order-swap`, `paraphrase-flip`, `outside-vocabulary`, `schema`, `provider`, `baseline-forced-same` — is printed with counts on every table.

**No count is an automatic warrant** (FW5:851). Marks are reported per register and are never summed, averaged, weighted or ranked. Endpoints are independent occasions to look for one pattern, never competitors (FW5:849).

**A reached ceiling is a declared resource boundary, not exhaustion of the inquiry**, and this record states which was reached and what would reopen the question.

**`appellate_rulings: N`.** Where N = 0, this record does not describe the run as validated, checked or confirmed. That the loop ran without a human is a fact about the loop, not a fact about the readings.

**Two published instruments were narrowed to make these cells machine-fillable, and the narrowing is part of the claim.** `ROOT_READING_VOCABULARY` is published as a suggestion that a row may exceed and that root may write outside; this run closes it to six values and routes anything outside to `unresolved:outside-vocabulary` with the text preserved. And where the published instrument says "the reading is root's", this table says the reading is a guarded `judge`-role artifact and **root has not read it**.

**What would reopen this:** an appellate ruling; a successful attack on `std:reading-rubric/v1` or on a register definition, which collapses every ν citing it in pass 1; a custody correction; a third judge family; more replicates; a raised budget under a new `loop_plan_id`.

## block register by reason code

| reason code | cell |
| --- | --- |
| `ensemble-split` x0 | - |
| `referential-integrity` x4 | contrast/case-b|E|ORIGINAL vs CONTROL, contrast/case-c|D|ORIGINAL vs CONTROL, contrast/case-d|G|ORIGINAL vs CONTROL, h005-row/synth/mini_fcl/cycle01/objection#o3/target/p.objection.0#a3#9536acfc8c9d |
| `operative-target` x0 | - |
| `order-swap` x0 | - |
| `paraphrase-flip` x0 | - |
| `outside-vocabulary` x1 | h005-row/synth/mini_fcl/cycle01/response#r3/mentions/p.response.0#BODY#e25b211ebe08 |
| `schema` x0 | - |
| `provider` x0 | - |
| `baseline-forced-same` x0 | - |
| `constitution` x0 | - |

## the audit record in force

The audit record in force is the appellate and audit artifacts registered in the graph; each is printed as entered, and none of the audit results is reduced to a measure of the reader.

- planted-flaw-calibration for judge#1: the seat answered True on no-shared-reference, whose ground truth (False) is true by construction: Nothing in either record can bind a role in the other, so no relation from the vocabulary is established and the critic's answer is `none`.
- planted-flaw-calibration for judge#2: the seat answered True on no-shared-reference, whose ground truth (False) is true by construction: Nothing in either record can bind a role in the other, so no relation from the vocabulary is established and the critic's answer is `none`.
- planted-flaw-calibration for judge#1: the seat answered True on clean-control-lexical-overlap-only, whose ground truth (False) is true by construction: A lexical overlap is not evidence of use (FW5:628, FW5:640); a seat that sustains a relation here is reading the overlap, not the material.
- planted-flaw-calibration for judge#2: the seat answered True on clean-control-lexical-overlap-only, whose ground truth (False) is true by construction: A lexical overlap is not evidence of use (FW5:628, FW5:640); a seat that sustains a relation here is reading the overlap, not the material.
- planted-flaw-calibration for judge#1: the seat answered True on clean-control-framing-only-passage, whose ground truth (False) is true by construction: A reading grounded in the prompt's own scaffolding is not a reading of the material; the guard must decline it on the operative-target check.
- planted-flaw-calibration for judge#2: the seat answered True on clean-control-framing-only-passage, whose ground truth (False) is true by construction: A reading grounded in the prompt's own scaffolding is not a reading of the material; the guard must decline it on the operative-target check.

## the stopping sentence

STOP: no_new_reading_changes
- clause: clause_four_set_identity
- detail: the two cycles' triple sets are identical
- would_reopen: Any of the declared reopen reasons would move the triple set and reopen the chain.

This cycle's (cell, register, mark) triples are the same set as the previous cycle's. The comparison is set identity: which triples moved is the whole reading, and nothing here was enumerated or read as a magnitude.

No clause of this program reads a magnitude. Clause four compares two sets for identity and clause five compares the cycle index with the declared budget; nothing else in this decision is numeric.

A cycle may be net withdrawal and still be progress, and it may add and still be no progress. The register below is written every cycle, present even when it is empty.

## losses_outside_P

A cycle may be net withdrawal and still be progress, and it may add and still be no progress. The register below is written every cycle, present even when it is empty.

- none

## INDETERMINATE - requests and attempts without a response

An INDETERMINATE coordinate is a request or an attempt that has no response on record. It is a delivery fact, never a reading, and it is listed rather than counted because the run must answer for every one.

- none

## the unread / unresolved / machine-unresolved trichotomy

| cell | states as three things | block reason that declined it |
| --- | --- | --- |
| contrast/case-a|D|ORIGINAL vs CONTROL | unresolved | - |
| contrast/case-a|E|ORIGINAL vs CONTROL | unresolved | - |
| contrast/case-a|G|ORIGINAL vs CONTROL | unresolved | - |
| contrast/case-a|T|ORIGINAL vs CONTROL | read: differs | - |
| contrast/case-b|D|ORIGINAL vs CONTROL | unresolved | - |
| contrast/case-b|E|ORIGINAL vs CONTROL | machine-unresolved (referential-integrity) | `referential-integrity` |
| contrast/case-b|G|ORIGINAL vs CONTROL | unresolved | - |
| contrast/case-b|T|ORIGINAL vs CONTROL | read: same | - |
| contrast/case-c|D|ORIGINAL vs CONTROL | machine-unresolved (referential-integrity) | `referential-integrity` |
| contrast/case-c|E|ORIGINAL vs CONTROL | unresolved | - |
| contrast/case-c|G|ORIGINAL vs CONTROL | unresolved | - |
| contrast/case-c|T|ORIGINAL vs CONTROL | read: same | - |
| contrast/case-d|D|ORIGINAL vs CONTROL | unresolved | - |
| contrast/case-d|E|ORIGINAL vs CONTROL | unresolved | - |
| contrast/case-d|G|ORIGINAL vs CONTROL | machine-unresolved (referential-integrity) | `referential-integrity` |
| contrast/case-d|T|ORIGINAL vs CONTROL | read: same | - |
| h005-row/synth/mini_fcl/cycle01/objection#o1/mentions/p.objection.0#a1#525b3af1b886 | unresolved | - |
| h005-row/synth/mini_fcl/cycle01/objection#o2/depends/p.objection.0#a2#38d939f72410 | unresolved | - |
| h005-row/synth/mini_fcl/cycle01/objection#o3/target/p.objection.0#a3#9536acfc8c9d | unresolved | - |
| h005-row/synth/mini_fcl/cycle01/objection#o6/mentions/p.objection.0#a6#19601384de43 | unresolved | - |
| h005-row/synth/mini_fcl/cycle01/response#r1/revises/p.response.0#a4#ff38a1f8f95a | unresolved | - |
| h005-row/synth/mini_fcl/cycle01/response#r2/depends/p.response.1#o1#815280d4a6bc | unresolved | - |
| h005-row/synth/mini_fcl/cycle01/response#r3/mentions/p.response.0#BODY#e25b211ebe08 | unresolved | - |
| h005-row/synth/mini_fcl/cycle01/response#r4/target/p.response.1#o2#1e775847e680 | unresolved | - |

### unread

- none

### unresolved

- contrast/case-a|D|ORIGINAL vs CONTROL: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- contrast/case-a|E|ORIGINAL vs CONTROL: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- contrast/case-a|G|ORIGINAL vs CONTROL: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- contrast/case-b|D|ORIGINAL vs CONTROL: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- contrast/case-b|G|ORIGINAL vs CONTROL: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- contrast/case-c|E|ORIGINAL vs CONTROL: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- contrast/case-c|G|ORIGINAL vs CONTROL: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- contrast/case-d|D|ORIGINAL vs CONTROL: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- contrast/case-d|E|ORIGINAL vs CONTROL: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- h005-row/synth/mini_fcl/cycle01/objection#o1/mentions/p.objection.0#a1#525b3af1b886: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- h005-row/synth/mini_fcl/cycle01/objection#o2/depends/p.objection.0#a2#38d939f72410: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- h005-row/synth/mini_fcl/cycle01/objection#o3/target/p.objection.0#a3#9536acfc8c9d: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- h005-row/synth/mini_fcl/cycle01/objection#o6/mentions/p.objection.0#a6#19601384de43: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- h005-row/synth/mini_fcl/cycle01/response#r1/revises/p.response.0#a4#ff38a1f8f95a: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- h005-row/synth/mini_fcl/cycle01/response#r2/depends/p.response.1#o1#815280d4a6bc: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- h005-row/synth/mini_fcl/cycle01/response#r3/mentions/p.response.0#BODY#e25b211ebe08: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.
- h005-row/synth/mini_fcl/cycle01/response#r4/target/p.response.1#o2#1e775847e680: the deliberate reading of this cell stays unresolved; it proves neither presence nor absence.

### machine-unresolved

- contrast/case-b|E|ORIGINAL vs CONTROL: `referential-integrity`
- contrast/case-c|D|ORIGINAL vs CONTROL: `referential-integrity`
- contrast/case-d|G|ORIGINAL vs CONTROL: `referential-integrity`

## appellate_rulings

`appellate_rulings: 0`.

This record does not describe the run as validated, checked or confirmed. That the loop ran without a human is a fact about the loop, not a fact about the readings.

## failures and refusals this run recorded

Each line names the code the run's own receipt or refusal carried. A refusal is an act of the instrument, never a reading of the material, and mints no warrant either way.

- nothing in this run was refused or failed
```

---

## 6. The metric-creep lens over this record (ruling 7)

* The only counts in `CLOSING.md` are the block register's `xN`, which the
  frozen ceiling requires ("printed with counts on every table"), and they
  count cells a reason declined — not occasions, not seats, not cycles. One
  cell declined once for one reason is one entry however many cycles re-met it.
* No count, rate, score, rank or share is used as evidence anywhere. The
  stopping sentence is `no_new_reading_changes` under
  `clause_four_set_identity`, which is a **set identity** between two cycles'
  `(cell, register, mark)` triples; the record says so in its own words.
* A word lens for `score`, `scored`, `rank`, `ranked`, `ranking`, `weighted`,
  `aggregate`, `percent`, `rate`, `average`, `mean`, `tally`, `majority`,
  `vote` and `exhaustion` over `CLOSING.md` finds **four** occurrences and
  every one of them is inside the frozen ceiling's own *denial* of the thing:
  "never summed, averaged, weighted or ranked" (`weighted`, `ranked`), "a high
  block **rate** is the instrument declining to read", and "a declared resource
  boundary, not **exhaustion** of the inquiry". Nothing outside the ceiling
  block carries any of them. `standard.assert_no_exhaustion_claim`,
  `standard.assert_no_scoring_headers` and `contracts.assert_no_scoring_keys`
  all pass over the whole text, and all three run again in the acceptance
  proof.
* `dry-run.json` carries exactly three integers — `planned_calls`,
  `max_calls`, `provider_calls` — and none of the lens's words at all. All
  three are **bounds on spend**, which ruling 7 admits by name, and none is
  compared between seats, arms or cycles.
* The audit register prints each planted-flaw finding as entered, in the
  seat's own words, and no share of them is computed or rendered.

---

## 7. What this rehearsal did **not** exercise

Named here because a live run must be told them, and repeated in
`WAVE6-INTERFACE.md` §5:

1. **No induced failure.** The nine are the acceptance proof's, driven through
   the same entry with `induce=`; the CLI has no `--induce` flag and the
   design's CLI table does not give it one.
2. **The 300 s gateway wall** (ruling 13). Nothing offline can reach it.
3. **The key gate.** `slots_for` was never contended, because no credential was
   ever acquired.
4. **The real `publish_ref`.** This ran against `origin/main` of a temp bare
   repository, not `origin/claude/project-state-direction-j5rbun`.
5. **The repository's own decision ledger.** The receipt `REC-20260914-V` was
   minted in the temp checkout's copy of `docs/DECISION_LEDGER.md`, under the
   same lock a live run would use, but with no concurrent writer.
6. **The reading arm on published H005 material.** The rows here are
   `synthetic`'s eight, not the pre-registered twenty-two.
