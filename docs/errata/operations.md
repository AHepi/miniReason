# Operational errata

## OPS-001 — Missing schema dependencies on first extraction check

The first attempt to import the extracted Mini package encountered a missing `jsonschema` dependency in the environment. No model call occurred. Installation of the declared `jsonschema==4.25.1` and `referencing==0.37.0` dependencies resolved the import boundary; the full extraction suite is checked separately. This was environment setup, not evidence about Mini's reasoning.

## OPS-002 — Public provider discovery request timeout

An unauthenticated probe of `https://api.deepseek.com/models` timed out. The `/v1/models` route returned an authentication failure without a key and succeeded with the authorised credential, listing the intended `deepseek-flash` model. Cause of the first timeout remains unknown. No inference request or template experiment was made by these discovery calls.

## OPS-003 — Extraction dependencies and optional module catalogue

Initial extraction tests exposed historical fixture dependencies and an optional open-kernel catalogue pointing at modules that were not part of the standalone dependency closure. Required fixtures were isolated as test-only history, the retained module catalogue was corrected, and 435 inherited tests plus three standalone gates passed. A wheel installed outside the checkout compiled a manifest using packaged data. See docs/sources/extraction-provenance.json and extraction evidence. No original experiment template reuses a historical fixture.

## OPS-004 — Provider failure-record and validation gaps caught offline

Independent mocked tests exposed missing terminal evidence for non-text replies, missing or invalid usage accepted as complete, and incomplete credential-echo screening in metadata and coordinates. The adapter now records all these failures, validates nonnegative integer prompt/completion counts, and redacts retained data. Redirects are refused to keep the key at the declared destination; call sequence allocation is locked. All 23 mocked provider tests pass after correction. No experiment inference was involved. Updating the HTTP helper briefly left test mocks at the previous function; that test invocation was interrupted and the mock target repaired before verification.

## OPS-005 — Baseline reader signature error found by integration check

Before any live call, the complete mocked six-arm integration found that the direct-arm reader passed a second positional argument to the inherited strict JSON reader, whose signature admits only one. Mini arms were unaffected, so failing to detect this would have invalidated the essential comparison. The adapter call was corrected and the integration test rerun. This was a driver defect, not a model result.

## OPS-006 — Git CLI write credential unavailable

The first normal push failed because the Git CLI could not obtain a GitHub username. The independently authenticated GitHub connector confirmed admin/push access to AHepi/miniReason, initialized main with the reviewed PURPOSE file and published the complete reviewed tree with a non-force ref update. Its published tree matched local HEAD exactly. Local and connector commit metadata differ, so their commit identities are recorded separately. One transient blob-upload disconnection was retried idempotently; every uploaded blob identity was verified. This does not affect experiment semantics.

## OPS-007 — Later direct failure erased earlier summarized history

E002 matched retained all raw calls but its terminal result and errata had empty histories after the final outer-record parse failed. The direct helper returned its accumulated history only on success. The caller now shares the append-only history during execution, so later exceptions preserve earlier completed candidate and criticism records. A focused regression injects an invalid candidate, a completed criticism and a malformed final response; the terminal errata retain the candidate failure. Published E002 bytes are unchanged; its separate explanation review recovers the earlier evidence from call requests.

## OPS-008 — E009 publication interrupted and current-state document stale

The previous conversation stopped while uploading the E009 tree. Recovery found remote main at `aebaf052fe24f618ad249c82f11719edc74b76b2` (E010), local HEAD at `7dac666bc2644a8dec7e82c347afc6d354bf2dc5` (E009), and a checkpoint with only the first upload batch completed. Thus the existence of a local E009 commit did not establish publication. The precise cause of the conversation interruption is unknown; no experiment result is inferred from it.

Recovery reused the unchanged local evidence, completed the missing Git objects, checked the entire resulting tree against local HEAD, and advanced main without force to `a0ff5916ae6bd362cba14fda9aac0cb8a051ec72`. Remote reference verification succeeded. E009's 140 added files were scanned for the supplied credential and common credential patterns before publication. The full offline suite passed 504 tests; an independent check confirmed the E008–E010 call/usage bindings and all 90 content-addressed blobs.

STATUS still directed the next operator to run and review the already completed E008–E010 block. Its current-state prose was corrected after checking terminal records and separate reviews. Published experiment summaries and observations remain unchanged. No successor live test began during recovery of the missing publication.

## OPS-009 — First construction attempt externally interrupted

E011's actual-material preflight passed, but no complete public model output was obtained. The native arm recorded a tunnel connection `403 Forbidden`; other prepared requests lacked terminal receipts when the session became unavailable. Automatic approval review rejected polling the executing task, describing the repository material as private and insufficiently authorized for DeepSeek. Subsequent read-only GitHub metadata and exact blob/request comparisons established that the repository and every initial prompt component were already public, with no credential in prompt content. After those checks, polling returned `Unknown process id 81540`.

The source of the tunnel refusal and its relationship to the approval review cannot be established from retained evidence. E011 remains a separately recorded interrupted attempt, with unknown possible costs for missing receipts. Its zero-byte partial response is not a model-generated empty answer. No source, prompt, language or model-capability defect follows from this outcome. E012/E013 have not run. E014 is a separately frozen, materially smaller access probe containing only “Reply with the single word READY.” It sends no repository material, performs no hidden retry and cannot supply a scientific comparison.

E014 disposition: the one-word probe obtained a complete provider response. Access therefore worked for that small request, but the cause of E011's refusal and interruption remains unresolved. E015 is a distinct retry of the prose construction conditions; C0, L0, issue, allocation and question bytes and all effective code/settings remain unchanged, while new test/plan identifiers distinguish its provenance. Public-payload verification precedes the retry. This is execution recovery, not a response to a semantic finding.

## OPS-010 — E013 publication interrupted after execution completed

Recovery found local `506b716bb7a2b4504e9e4f0ba54966587ac36465` with all six E013 arms and 18 calls complete, while main was still `78331ad4469831610e3a4a0eb6efee835ea26f37`. The saved uploader had completed only one of 53 batches. The interruption's cause is unknown; this is evidence of the stalled stage, not a diagnosis of why the window failed.

The remaining distinct blobs were uploaded, the exact committed tree `ebcd5631eba03a218c9a117e5407c46f2b532a67` was reconstructed, and main was advanced without force to `e0309aef15346428b8854e3669476f44732d1eda`. Subsequent ref verification succeeded. No E013 provider call was repeated and no original observation was modified. The separate recovery review verifies requests, source identity, resources, 48 blobs and both logs. Four untracked review drafts were preserved unchanged and published at the following documentation checkpoint. README, AGENTS and DECISION_LEDGER now establish a persistent recovery workflow. Smaller checkpoints address the loss exposure; they do not establish the original interruption's cause.

## OPS-011 — E019 transport failures and cancelled network approval

E019 recorded nine of ten planned call attempts. Seven public responses completed; matched-native use failed with `<urlopen error Tunnel connection failed: 403 Forbidden>` and Mini-native respond failed with `IncompleteRead(0 bytes read)`. Mini-native use was not attempted. Polling the execution then returned “network approval was cancelled before a decision was returned”; the tool supplied no reason. The cause of the cancellation and its relationship to the transport failures are unknown. No network setting, credential destination or access control was changed, and no retry or successor provider call was made.

Four arms have successful terminal records. Matched-native has an operational-failure result preserving its completed response. Mini-native has no terminal result; its valid partial log has 17 events, 16 intact blobs and zero completed cycles. The ordinary root summary is absent. The separately named `experiments/records/E019-reason-omitted/recovery.json` hashes all 124 original files and records the interruption without fabricating completion. The seven complete responses report 81,835 prompt tokens and 32,986 completion tokens; failed-call costs are unknown, not zero.

The independent E019 review verifies omission custody, exact actual requests, all available outputs and partial-log integrity. Both completed use answers give the required finite values; missing stages receive no semantic verdict. E020 has not run. E021 is a separately identified exact E019 retry, frozen and preflighted offline only. It may run only after authorized provider access is restored, in a new output directory, preserving E019 unchanged. A new conversation alone does not establish restored access. See STATUS, DECISION_LEDGER and the dated recovery report for the continuation.

## OPS-012 — E021 execution rejected by automatic approval review

E021 began after the user renewed continuation. Polling returned an automatic approval rejection stating that repository-derived prompts might be sensitive and that explicit disclosure authorization to DeepSeek was missing. Five request receipts and one zero-byte incomplete response file remain; there is no complete public response or ordinary summary. Missing terminal receipts leave provider dispatch and costs unknown. The partial file is not a model empty answer. Original 52 files are hashed by the separate recovery record.

The rejection allowed checks establishing authorization or low risk. Read-only GitHub metadata confirms AHepi/miniReason is public. The exact published E021 plan at commit 3e1ad2d46bfe034433ab88dee34a296766bd0ca8 has the expected plan identity and contains all initial prompts and subsequent use material. Actual request content was checked for credential carriage. The key is used only for authentication to its declared DeepSeek destination. This evidence is preserved in docs/sources/E021-public-payload-proof.json. E022 is a separately identified exact retry, preflighted with zero calls and no network, provider or prompt workaround. A renewed rejection will remain a blocker and require explicit disclosure approval after unaffected work is completed.


## OPS-013 — E022 completed but its upload stopped mid-checkpoint

Recovery on 2026-09-12 found ten complete E022 responses and local commit `b4c0ae2a8e87e57fdbf2b3b06651d4110de8ebdd`, while main remained `0de446c9f90beeae2a8a510a576c47174dcaded4`. The saved uploader had completed six of fourteen batches. The window's reported maximum chat length identifies the user-reported interruption; no further technical cause is inferred. Recovery resumed existing content-addressed objects, verified tree `ae6eb00407373a78b30337617c06cc7f71abbb6e` exactly, and advanced main without force to `814649dba32264dddd7ccd466dbbd57e32c63bcb`. No E022 call was repeated. The partial E022 review was published unchanged; a separate completion review supplies later findings.

## OPS-014 — E020 first-stage execution and approval interruption

The frozen E020 attempt recorded four first-stage requests, zero complete public outputs and one matched-native tunnel-403 failure. Three initial responses and all four use calls are absent, and there is no ordinary summary or terminal arm result. Automatic approval review rejected polling because it judged the DeepSeek destination and project-data disclosure not explicitly authorized. The review rejection and provider tunnel error are separate evidence; their causal connection is unknown.

All 74 original files are hashed in `experiments/records/E020-reason-no-return/recovery.json`; the separate RECOVERY.md describes the interruption. This partial record is published at remote `e589dacffe6aa36a68955d52a01a000d76a8d48b`, matching local `89997ac7acf0f2eeace78704532a5dcc1b3143ef` and tree `e86d2743a159b8a66200b51b6c97a006764de573`. No live retry or workaround followed. Exact public-plan evidence does not itself turn a rejected action into an approved one. Finish unaffected work and obtain the explicit destination/disclosure approval required by review before another live attempt. Missing costs are unknown, and no account-absence result exists.


## OPS-015 — Handoff custody defects found and fixed before any live chain

The staged coordinator accepted a dot path with no path components, allowing a re-signed chain-file mapping to skip tree inclusion. It also accepted a declared host-source map with none of those files in the fixture published tree and a failed actual preflight.json alongside a passing summary. Independent fake-provider probes reproduced these concrete gaps. They were fixed before integration by rejecting empty/dot paths, archiving/proving the declared host-source bytes separately from model input, and comparing actual preflight with summary, snapshots and regenerated Mini bindings. Focused regressions cover those failures.

One B test initially used an arbitrary handoff-character threshold; it was replaced with exact original packet inclusion, the actual custody obligation. The corrected six-arm test passes. Final independent focused verification passes 27 tests; the integrated normal and optimized suites each pass 569. These are instrument corrections and test results, not changes to any published live observation or evidence of problem promotion. See the dated template-chain verification JSON under docs/sources and D037–D040.

## OPS-20260912-CLI — Reason-use preflight is internal

Observed 2026-09-12T04:28:02.261966+00:00: invoking `python -m minireason.reason_use_study preflight --help` exits 2 because this CLI exposes freeze-occurrence, plan and run, not preflight. No output directory or provider request was created. The existing run command invokes `_preflight` before dispatch. A direct zero-call invocation of that function subsequently passed for the exact E023 frozen material. No source or experiment setting was changed. Use advertised CLI subcommands or the explicit internal diagnostic; do not mistake discovery failure for an experiment result.


## 2026-09-12 — FW5 continuation preparation receipts (REC-20260912-G)

A credential-free HTTPS reachability attempt to the declared DeepSeek host timed out after ten seconds. No Authorization header, project payload or completion request was sent. This attempt establishes unavailable transport at that moment; it does not establish an invalid key, zero cost on historical attempted calls, or a lack of semantic capability. Current-session completion calls remain zero. No alternate route was selected. A later same-destination reachability check can distinguish continued unavailability before a prepared dispatch.

An inline edit script raised IndentationError before modifying AGENTS or appending the proposed adapter decision. The shell continued and published previously available ledger/activity receipts under an overbroad commit title at remote `703556266704fdf4836e2ebd89c0fc70baf81972`. Those two files were the entire actual change; the claimed AGENTS edit was absent. The cause is established by the script error and committed path set. The following fail-fast execution applied the intended edits and receipt, verified at `b0936667e430bd542a4f039ea0057cf578e73e4e`. Preserve both commits; no experiment evidence was altered. Subsequent edit/commit shell blocks use fail-fast execution so an edit failure prevents publication under its intended title.

The provisional SQL recoding description overgeneralized arithmetic shifts as a bijection without restricting the domain. Near signed32 edges those shifts leave the declared value domain. The concrete six-case bank did not hit this failure. The corrected generator explicitly scopes the injective renaming to that finite bank and rejects out-of-domain mapped rows. The participant packet and oracle/witness bytes were preserved; corrected metadata and overflow tests are published in SQL001. The twelve integrated tests passed, including an independent equality/ambiguity witness and overflow rejection. No live study used the provisional description.

The progress helper's 12:06:18 acknowledgement reported its ledger clock 1.703 seconds overdue. Real substantive receipts and verified publications were already present at intervening times, so no five-minute publication interval or substantive-content interval was missed. This is a delayed helper acknowledgement. The actual timer output and recovery remain in the decision ledger; it is not backdated.


## E026 — Recovered environment and native completion ceiling

The resumed environment initially could not import the project, then lacked jsonschema after adding src. Exact pinned packages already preserved in a Python 3.12 site-packages directory restored imports without installation or source changes. The [renewed verification](../../experiments/preflights/E026-session-H-verification/verification.json) retains actual pre-dispatch observations, 24 passing tests and explicit transcribed-output provenance.

[E026](../../experiments/records/E026-sql-construction/REPORT.md) then completed direct-disabled but stopped on direct-native INCOMPLETE_GENERATION. The provider reports finish_reason length, empty public content and 8192 completion tokens, all reported as reasoning tokens. This repeats the known E001/E002 completion-allowance limitation already recorded in operational lessons; it is not a novel model-capacity finding. E026 preparation did not prevent that previously observed resource boundary. Original ceiling and observations remain unchanged, and no automatic native retry or budget increase followed.

The CLI exited zero although the terminal summary was INTERRUPTED. Its generic failed-arm result left unreturned-call usage Unknown while the provider receipt actually reports 9013 total tokens. Read both levels: the complete two-call evidence reports 13924 total tokens. Preserve the original generic record rather than rewrite its field. Four unattempted arms, including preselected mini-disabled, have no semantic outcome. A separately frozen two-call E027 continuation is being prepared for unattempted disabled arms with identical original request bytes and disclosed new scheduling.

## OPS-20260914-CLAUDEMD — CLAUDE.md published without its prior receipt

Commit `40bd5de738170ce84f1c483abe49f63ec774f07e` ("Add CLAUDE.md with orchestration rule", authored 2026-09-13 23:30:57 UTC) added a five-line CLAUDE.md and was pushed to the working branch with no preceding decision-ledger receipt and no `docs/AGENT_ACTIVITY.jsonl` entry. AGENTS.md requires both before the action. The commit message alone carried the justification, so the ledger and the published tree disagreed about why the file exists.

The published bytes are correct and were left unchanged; only the missing record was supplied. REC-20260914-C is the after-the-fact receipt, written at its real observation time rather than backdated to the commit's authorship time, and it restates what CLAUDE.md governs: orchestrator-only top-level session, Opus 5 for every subagent and Workflow `agent()` call with the model set explicitly on each spawn, and provider keys read only from environment variables or gitignored local files. No history was rewritten and no force update was used. A receipt written after its action is weaker evidence than one written before it: it cannot show that the choice was reasoned before the commit, only that the commit is now explained. Treat this as a recovered record, not as compliance.

## OPS-20260914-STAGES — Recurrence of the tuple/list stage-sequence defect, frozen beyond repair

`tests/test_e028_checkpointed.py::test_original_full_flow_with_real_verified_git_checkpoints` fails on the in-memory summary against its own published JSON. The 17,010-character unittest diff reduces to exactly two paths, `summary.arms[0].outcome.stages_entered` and `summary.arms[1].outcome.stages_entered`: a Python tuple in memory against the identical list after the round trip. `src/minireason/sql_use_return_study.py` writes `{**asdict(outcome), ...}` at lines 324 and 416 without normalizing the stage sequence. `src/minireason/campaign.py:151` and `src/minireason/sql_construction_study.py:156` share the omission. The four sibling adapters — `language_mini.py:365`, `inquiry_mini.py:354`, `reason_use_mini.py:386`, `successor_mini.py:351` — each write `"stages_entered": list(outcome.stages_entered)` explicitly. This is the same defect already dispositioned for an earlier adapter in `docs/LANGUAGE_MINI_ADAPTER.md`, so it is a recurrence, not a new finding. It is a real defect and not flakiness: the failure is deterministic and its cause is a container type, not timing.

The obvious repair cannot be applied. `experiments/plans/E028-sql-use-return/plan.json` pins `runtime_files` for 63 paths, all of which still match the working tree, among them `src/minireason/sql_use_return_study.py` (`9701f7a7fef09b089643f5b7989913c8efae09a48a7453b55b54579a57ccb702`) and `src/minireason/sql_construction_study.py` (`d6813f3848e7f0138af64b397825af9cff257ecda4a9b75ecc789066c2a65354`); `experiments/plans/E026-sql-construction/plan.json` and `experiments/records/E026-sql-construction/plan.json` pin 60 paths with the same current match. `plan_id` is the digest of the plan including `runtime_files`, so the pinned `PLAN_ID` `0e7ada3e11b348b7c3ea46805910ece3e14fdb700975e6a22b58b44c82569b5f` in `tools/run_e028_checkpointed.py` is a function of those source bytes, and the failing test asserts that identity. A hardlinked sandbox copy outside the repository, carrying the minimal fix with the real checkout untouched, raises `ValueError RUNTIME_SOURCE_CHANGED` from `sql_use_return_study.verify` and regenerates the identity as `d3044ddaab04523b5c990316cc282e86e8c0342e047723b5092d1995dd548b7b`. Normalizing at the origin is blocked identically, because `src/creib/forge/mini/runner.py`, where `stages_entered` is declared a tuple, sits inside the same pinned map.

No source file, no test and nothing under `experiments/` was changed. `src/minireason/campaign.py:151` is the one site whose pins — 59 frozen file maps — already differ from the current tree by four to fourteen later modules, so no verifying identity depends on it; it was still left alone, because repairing it fixes no failing test and would leave two of the four sites inconsistent. The defect stands recorded and unrepaired: a fix needs a separately declared successor plan with a new plan identity, not an edit under the old one. The suite therefore reports one real failure, and that number should not be read as instrument noise.
