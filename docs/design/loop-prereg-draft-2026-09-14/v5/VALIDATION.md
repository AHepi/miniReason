NOT RUN as a pre-registration validation

## Judge rerun after corrections

At 2026-09-15T21:03:26.156765+00:00 the authorized offline validator was rerun after the judge corrections. Exit **1**, **FAIL (UNRESOLVED)**: rows remain empty and the builder is unimplemented. All printed structural/custody checks passed. The subprocess changed no v5 file or any of the three shared documents; source inspection found only standard-library reads/prints, with no provider, driver import, credential access, minting or file write. Source/check receipt: reports/review-10/notes/judge-validator-receipt.json; stdout/stderr are preserved beside it. These checks do not qualify an execution route or approve semantics.

Command: Python311 -B -X utf8 docs/design/loop-prereg-draft-2026-09-14/v5/validate.py.

```text
OFFLINE DRAFT CHECK ONLY - no pre-registration validation
PASS 13 required bundle files present
PASS draft status, unimplemented builder and unminted placeholder explicit
PASS reading arrays empty; frozen occurrence retained; no contrast attachment
PASS invalid execution sentinels present; closed-schema status stored separately
NOTE max_calls=0 alone does not enforce a stop; runtime counts spending-step receipts
PASS all six fixed source pins present
PASS 139 draft source file hashes match
PASS eleven response texts retained as source inventory, not reading rows
PASS obligations canonical-body digest matches
PASS obligations complete-file digest matches
CANONICAL_BODY_SHA256 511dc114e9f6b4a6c3f7cf4a6123b3ae26a866f62bc70db24ce20651a30561cb
FILE_SHA256 9d50cea379f768ef66da0283a77fac98ffa8010c8bc68f8eeb92106e90b75d97
PASS five active O, ten active P and five explicit retired dispositions
PASS nine inherited anchor constructions retain source provenance; documented judge corrections; no L004 pin completion
PASS bundle JSON keys contain no forbidden evaluation fields; quoted prose is not rewritten
PASS calibration UTF-8 string hashes/byte lengths, source values and quoted spans match
PASS proposed grammar is admissible and injective over its six hypothetical positions
PASS conditional Windows path bounds: original=175, order-swapped=189, paraphrase=188; all <240
UNRESOLVED actual key admissibility, injectivity and output paths: no admitted rows
PASS conditional call arithmetic retained; R and finalized budget unresolved
UNRESOLVED builder/source-map pin and future S0 coverage: NOT FOUND
UNRESOLVED audit O5, relation-only stop semantics and executable budget enforcement
UNRESOLVED/FAIL rows: rows=[]; awaiting proposed row builder; not a finding about material
RESULT FAIL (UNRESOLVED): draft is not ready for pre-registration or execution
```

Exit code: 1. Obligations digests were independently recomputed using PREREG.md section 5; they remain 511dc114e9f6b4a6c3f7cf4a6123b3ae26a866f62bc70db24ce20651a30561cb (canonical body) and 9d50cea379f768ef66da0283a77fac98ffa8010c8bc68f8eeb92106e90b75d97 (complete file). No obligations byte needed correction. Later report-only edits do not change the checked config, calibration, source manifest, obligations or validator.

## Historical worker check (pre-correction)


The worker offline draft check was invoked at 2026-09-15T20:32:45.960936+00:00. No auto_loop command, identity function, credential query or provider call was run. The validator exited **1** because row readiness is UNRESOLVED. These checks concern draft custody and structure only; they do not approve the row contract or authorize execution.

Command: `python -B -X utf8 docs/design/loop-prereg-draft-2026-09-14/v5/validate.py` using the discovered Python311 interpreter. No historical v4 PASS or suite claim is inherited.

## Actual validator stdout

```text
OFFLINE DRAFT CHECK ONLY - no pre-registration validation
PASS 13 required bundle files present
PASS draft status, unimplemented builder and unminted placeholder explicit
PASS reading arrays empty; frozen occurrence retained; no contrast attachment
PASS invalid execution sentinels present; closed-schema status stored separately
NOTE max_calls=0 alone does not enforce a stop; runtime counts spending-step receipts
PASS all six fixed source pins present
PASS 139 draft source file hashes match
PASS eleven response texts retained as source inventory, not reading rows
PASS obligations canonical-body digest matches
PASS obligations complete-file digest matches
CANONICAL_BODY_SHA256 511dc114e9f6b4a6c3f7cf4a6123b3ae26a866f62bc70db24ce20651a30561cb
FILE_SHA256 9d50cea379f768ef66da0283a77fac98ffa8010c8bc68f8eeb92106e90b75d97
PASS five active O, ten active P and five explicit retired dispositions
PASS nine inherited calibration rows and full provenance retained; no L004 pin completion
PASS calibration source-string hashes and quoted spans match
PASS proposed grammar is admissible and injective over its six hypothetical positions
PASS conditional Windows path bounds: original=175, order-swapped=189, paraphrase=188; all <240
UNRESOLVED actual key admissibility, injectivity and output paths: no admitted rows
PASS conditional call arithmetic retained; R and finalized budget unresolved
UNRESOLVED builder/source-map pin and future S0 coverage: NOT FOUND
UNRESOLVED audit O5, relation-only stop semantics and executable budget enforcement
UNRESOLVED/FAIL rows: rows=[]; awaiting proposed row builder; not a finding about material
RESULT FAIL (UNRESOLVED): draft is not ready for pre-registration or execution
```

Exit code: `1`.

At the worker handoff, no second invocation had been made. Completed reporting receipts and the handoff report were written afterward; between that worker invocation and the worker handoff, no validator input affecting the checked source, obligations, config, calibration or row contract changed. The judge later changed calibration and validator inputs, as recorded above.
