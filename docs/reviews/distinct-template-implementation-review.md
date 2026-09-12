# Distinct-template implementation review

Completed 2026-09-12 UTC under D037/HA1–HA3 and the bounded D039 corrections. This reviews the finalized staged implementation for integration. No external model call was made. The recorded outputs in these checks are scripted fixtures, not research observations.

The reviewed implementation supports one `joint_construction_v1` episode followed by one distinct `successor_discrimination_v1` episode. No remaining defect was found within the tested custody, comparison and interruption contract. Root still owns integrated verification, publication and any later live activation; this review does not complete the interrupted E020 control or establish a problem-promotion result.

## Corrections established by review

| Initial defect | Reproducible evidence | Final behavior |
|---|---|---|
| An empty tree path could skip proof traversal. | The coordinator owner identified that `PurePosixPath(".").parts` is empty; a re-signed handoff could bypass that path's tree inclusion. | Empty parts are rejected. The dedicated regression passes. |
| Declared A host source had no independently checked archive. | Independent temporary fixture declared 75 source files, had none of those files in its Git tree, and still produced an accepted handoff. | Every declared source file is retained separately, matched to the declared SHA-256 map and aggregate identity, and proved at its original path in the supplied Git tree. Missing or changed source evidence is rejected. |
| The actual A preflight file could contradict the summary. | Independent probe changed and committed `record/preflight.json` to report failure while leaving the summary unchanged; handoff freeze still accepted it. | The actual preflight file is included and proved, must equal the summary entry, and must match recomputed material snapshots and prepared Mini bindings. The same contradiction now raises `PARENT_PREFLIGHT_CHANGED`. |

These corrections concern evidence consistency. They do not turn source hashes, replay or a publisher assertion into authentication of external execution.

## What the implementation preserves

The coordinator fixes A's source arm to `mini-r01`, requires its four actual stages, and rejects arm substitution, an additional cycle or repetition, and a renamed copy of the same template. A and B have distinct registered contracts, instructions, stage graphs and separate one-cycle manifests and logs. The coordinator has no provider dispatcher.

The handoff retains the whole original packet, carrier, selected occurrence and parent material, plus the complete construction, criticism, revision and promotion outputs. It checks occurrence identities against the actual result, adjacent request/response records, regenerated prepared source material and completed Mini replay. Text remains exact, including Unicode, whitespace and a no-promotion answer. Custody proof and host source archives are outside the model-visible rendering.

Every B arm receives the same frozen handoff. Bare and native arms address the complete follow-up endpoint in one response. Matched and Mini arms locate the issue and then discriminate its live readings in two calls; the second prompt receives the actual preceding locate text. Their conditional messages and settings match under the same scripted preceding output. This is a routing parity check, not evidence that Mini improves reasoning. Actual token costs and native reasoning remain distinct experimental conditions.

The B tests reject changed material, instructions, handoff, source identity, provider settings and the tested compiled runtime fields before provider dispatch. A contaminated second-stage route stops after the first call. An independent duplicate-dispatch probe submitted each actual Mini request twice; both repeated requests were refused before another call, while the ordinary run completed with exactly two scripted provider calls.

A failed B second call retains its actual locate output, records an operational failure, creates no discriminate artifact and leaves every original A record byte unchanged. Reusing its output directory is refused. Ordinary no-promotion or suspension prose remains legitimate: no semantic standing, installed language change or automatic third episode follows from recording it.

## Verification and exact files

An independent disposable overlay containing the finalized files passed all 27 focused tests in 16.927 seconds: 16 coordinator tests and 11 B tests. Reproduce after integration with:

```sh
PYTHONPATH=src:tests python -m unittest test_template_chain test_successor_mini test_successor_study -v
```

A separate subprocess check executed `template_chain verify-handoff`, `successor_study plan` and `successor_study preflight` on an actual scripted A record. Preflight reported `CONFIGURATION_PREFLIGHT_PASSED` with zero model calls. All 77 source files declared by that combined fixture were present in its verified source archive. Independent rechecks rejected missing source evidence and the previously accepted contradictory preflight. All commands after D038 were wrapped by the repository activity logger.

| Reviewed file | SHA-256 |
|---|---|
| `src/minireason/template_chain.py` | `7d2224ec7b872c5db1834ff8d201fda63a50ddd9111de9d32942cace8e7d66af` |
| `src/minireason/successor_data.py` | `46544f8ed51af610f34072e071fcd0741838c825bcd5eff0f1803b77fd687089` |
| `src/minireason/successor_mini.py` | `68b38867bc2a2a2e9fa9568852b67acfa7f7a9de63171e695c0b482b9d493997` |
| `src/minireason/successor_study.py` | `142ea81b3a033d3737679cec7ccff08867120d7dcdf37dbe59f3e01c297a19b6` |
| `tests/test_template_chain.py` | `b7c3b570c9fc37030511dcd5d1ca6c2c1c8e7749e116540d2549b0a3374e6fde` |
| `tests/test_successor_mini.py` | `12d57c92d00a7e37ce021224219b46459b55184830ff0def708e55be4d955ca4` |
| `tests/test_successor_study.py` | `7b0ec7ab62b39fef32d8282f116509308191abe4c863843bb52dd94498da026c` |

## Boundary of the finding

Portable verification establishes that retained bytes belong to the supplied Git tree and that the declared records agree. The publisher must independently establish that the real remote commit has that tree, that the chain was frozen before A, that A was published before handoff preparation, and that the handoff/B plan was published before B. `remote_verified=true` records that external assertion; it does not perform the remote check. The verifier also cannot independently prove which code an external process executed or authenticate provider authorship from a locally written trace.

The tests establish these finite operational properties. They establish neither creativity nor the merit of any proposed diagnosis, and they supply no live A-to-B comparison. Those questions require the separately authorized experiment and substantive reading of its actual outputs.
