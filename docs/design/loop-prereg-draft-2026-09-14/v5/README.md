# The pre-registration bundle, revision v5 (L004) — still a DRAFT, and still not a pre-registration

This is the proposed reading-only successor over published F001 occurrence-09. Its central new content is a **proposed row-construction contract**, a separate criticizable contribution under PURPOSE.md:7,19. The builder is unimplemented, both reading arrays are empty and the reading set is UNRESOLVED. No identifiers are minted and no run is authorized.

docs/STATUS.md:732 authorizes:

> **Next authorized task:** the successor pre-registration to **READ the new F001 occurrence-09 material**.

docs/design/loop-prereg-draft-2026-09-14/v4/PREREG.md:214-216 states:

> **What that makes this run.** L003 dispatches F001's own next occurrence, under F001's frozen plan,
> whose material is **material for a successor pre-registration to read**; and it reads and marks only
> published bytes. That is a smaller claim than L001's and it is the honest one available.

## Why a new row contract is needed

L003's instrument produced **zero reading rows for occurrence-09**. Two separate facts explain this:

- Its selected reading set contained only sixteen C001 mark keys, while plan.opened_cells.reading_cells was empty (experiments/loops/L003-loop-first-live-2026-09-14/config.json:26-43; plan.json:112,170-187). Both READ steps recorded planned/dispatched output digests equal to SHA-256 of serialized numeric zero (steps/0022-READ.json:18,20,28; steps/0032-READ.json:18,20,28, under that same run).
- Independently, the occurrence-09 use-table builder walked 117 references and produced zero cross-document rows, 54 intra-document references and 63 unresolved references. Prose was not parsed; mini_fcl rival/response had schema_failure; the remaining parsed references stayed local or unresolved (experiments/loops/L003-loop-first-live-2026-09-14/cycles/cycle-01/use-table/occurrence-09/USE_TABLE.md:93-106,110-161,167,189-194). Both cycle JSON row arrays are empty at use_table.json:523.

That is an **instrument limitation**, never absence of relations. The contract in [PREREG.md](PREREG.md#row-construction-contract-proposal) proposes exact earlier/later contribution pairs and keeps missing record referents unresolved.

## What is here

The thirteen required files follow recon-S section 7: README, PREREG, config, reading_set, obligations, calibration, CLONE-PATCH, validate.py, VALIDATION, CHANGES-PREREG, REVIEW-PREREG and the two bundle worksheets. Source identities and the eleven-text inventory are in reading_set.json; they are draft custody evidence, not a pre-registration or admitted rows. DRAFT-REPORT.md additionally preserves the worker snapshot; REVIEW-PREREG.md records the separate judge correction round.

The proposed run label is L004-loop-read-f001-occ09-2026-09-16, using the worker-proposed suffix. The convention is base directory=v1, v2=L001, v3=L002, v4=L003, v5=L004 (v2/README.md:1-10; v3/README.md:1-8; v4/README.md:1-7, each beside this directory). No run directory is created. The receipt placeholder remains REC-YYYYMMDD-X at <minted at S0>; loop_plan_id remains <UNMINTED>.

config.json is intentionally **not executable**: empty rows, cycle_budget=0, max_calls=0 and provider_mode=DRAFT-NO-RUN. Zero max_calls alone disables the runtime stop, so it is not used as the safety guarantee (tools/auto_loop.py:2491). The closed schema forces reading_set_status into reading_set.json; its exact value is UNRESOLVED: awaiting row builder (src/minireason/loop/types.py:1150-1154,1188).

## Open decisions

Owner approval or revision of the row contract; lossless builder/adapter implementation and source pinning; actual admitted R and budget 11R + 46W; audit O5 semantics; a reading-only stop comparison and scoped ceiling; all actual paths and safe reopening. The short grammar's initial path bound is 189 < 240; an actual longest key/path is NOT FOUND.

The worker invocation and judge rerun of the offline validator are recorded in [VALIDATION.md](VALIDATION.md), which must report rows UNRESOLVED/FAIL. It is not driver PREFLIGHT or pre-registration validation. Historical v4 reviews are not new approval.

All v1-v4 and experiment bytes stay unchanged. This worker makes no provider calls, reads no credentials and performs no state-changing Git command. A separate publisher follows; no publication is claimed here. FW5 alone supplies semantic clauses at line; ECS 2.0 has no weight (docs/reviews/session-rulings-2026-09-14.md:29).
