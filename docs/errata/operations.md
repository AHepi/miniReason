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
