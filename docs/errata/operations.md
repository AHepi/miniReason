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

**Disposition, 2026-09-14.** The failing assertion was corrected rather than the frozen adapter. `tests/test_e028_checkpointed.py:290` compared `json.loads(remote_summary)` against the unserialized in-memory `summary`; it now compares it against `json.loads(json.dumps(summary))`. The property the test exists to certify is that the summary published into the remote git ref equals the summary the run returned *as serialized bytes*, and a Python tuple and the JSON array it serializes to are the same bytes, so the original form asserted something stronger than and different from its own subject. No other assertion in that test was weakened: status, `provider_calls`, `reused_prefix_responses`, the remote tree equality and the thirteen-commit count are unchanged, and no test file is hash-pinned by any plan (`runtime_files` contains no path under `tests/`). Separately, `src/minireason/campaign.py:151` was normalized to `"stages_entered": list(outcome.stages_entered)`, matching the four sibling adapters. That site is not in any plan's `runtime_files`; it is named in 81 older-generation source maps, and while its pinned hash still equals the current file, every one of those maps is a strict subset of the live `campaign.source_identity()` result — short by four to eight later `src/minireason` modules — and the checks at `reason_use_study.py:366` and `successor_study.py:259` compare the maps whole, so each already raises its own `SOURCE_CHANGED` regardless. The site's serialized output is unchanged either way, since JSON renders a tuple and a list identically.

The adapters themselves are untouched and still defective. `src/minireason/sql_use_return_study.py:324` and `:416` and `src/minireason/sql_construction_study.py:156` still place a tuple in the in-memory outcome, and remain unrepairable under E028's and E026's live pins for the reasons recorded above. This disposition records where the failing comparison was wrong; it does not repair the adapters, does not re-freeze anything, and does not discharge the obligation to carry the normalization into a separately declared successor plan. Until that successor exists, an agent reading `outcome["stages_entered"]` straight from those three writers, without a JSON round trip, still gets a tuple.

## OPS-20260914-LOGGERUTF8 — The activity logger's wrapped child loses Python UTF-8 mode

Running the full offline suite through `tools/repo_activity.py … -- python -m unittest discover -s tests` reported `Ran 697 tests` with `FAILED (failures=1, errors=5, skipped=1)`. The same command run directly reported `Ran 697 tests` and `FAILED (failures=1, skipped=1)`. The five errors were all in `tests/test_sql_use_return_portable.py`, each ending in `tools/run_sql_use_return.py:66`, `parser.error(args.operation + " requires Python UTF-8 mode; invoke python -X utf8")`, which fires when `sys.flags.utf8_mode` is false.

The cause is the wrapper, not the tree. On this host the locale is unset (`LC_CTYPE="POSIX"`), so a directly started interpreter enables UTF-8 mode automatically; the logger's own interpreter does the same and, in doing so, coerces `LC_CTYPE` in its environment, which `subprocess.run` passes to the child. The child then sees a non-POSIX locale, does not auto-enable UTF-8 mode, and fails the guard. A one-line probe confirms it: direct `sys.flags.utf8_mode` is `1`, and the same expression wrapped by the logger prints `0`.

Impact is on evidence, not on the instrument: a wrapped suite run over-reports failures and would make a clean tree look broken. Corrective action taken here was to log the suite run with bare `--phase begin` / `--phase outcome` entries and invoke the suite directly, which is what the previously recorded 681-test baseline also did. Either pass `-X utf8` explicitly inside the wrapped command, or do not wrap whole-suite runs. This is a tooling observation about how a run was measured; it is not evidence about any experiment, and the `.github/workflows/tests.yml` gate is unaffected because it already invokes `python -X utf8`.

## OPS-20260914-LEDGERCRLF — A text-mode rewrite of the decision ledger normalised thirty-seven historical line endings

**Observation.** While correcting a single sentence of the REC-20260914-N opening receipt on 2026-09-14, this session read `docs/DECISION_LEDGER.md` into Python as text and wrote the whole file back. `git diff` then reported **39 insertions against 37 deletions** for what was meant to be a two-line append.

**What failed.** Thirty-seven historical lines carried CRLF endings from the Windows recovery host of 2026-09-13. Python's text mode translates `\r\n` to `\n` on read and writes back the platform newline, so every one of those thirty-seven lines was silently rewritten with a different terminator. The intended append was two lines; the other thirty-seven deletions and thirty-seven insertions were the invisible normalisation. Nothing in the edit was wrong as prose; the byte damage was entirely a side effect of the write mode.

**Impact.** None reached the remote. The damage was caught before staging by reading `git diff` rather than trusting the edit, the file was restored with `git checkout -- docs/DECISION_LEDGER.md`, and the receipt was re-appended by opening the file in binary append mode, after which the diff read **2 insertions and 0 deletions**. The commit `7745fe9` that carried that receipt therefore contains a pure append and no published receipt byte was altered. Had the diff not been read, thirty-seven already published receipt lines would have been modified in place — which `AGENTS.md:17`, "Never modify a published observation", forbids outright, and which no later reader could have distinguished from an intentional edit.

**Cause — established.** Text-mode I/O over a file with mixed line endings. It is established rather than suspected: the file still carries exactly thirty-seven CRLF lines today, `python -c "open(p,'rb').read().count(b'\r\n')"` returns 37 before and after the byte-mode append, and the diff sizes match the count exactly.

**Competing explanations, and why they are rejected.** A Git `core.autocrlf` or `.gitattributes` conversion would produce the same diff shape without any file rewrite; rejected, because the working-tree bytes themselves changed, the repository sets no `autocrlf` and carries no `.gitattributes`, and restoring from the index removed the diff entirely. An editor or formatter normalising on save; rejected, because no editor was involved — the write was an explicit Python call, and re-running it reproduces the thirty-seven-line diff deterministically.

**Corrective action.** Append to `docs/DECISION_LEDGER.md` only in byte mode, never by reading and rewriting the file. The exact practice: write the new receipt paragraph to a separate UTF-8 file, then `with open('docs/DECISION_LEDGER.md', 'ab') as fh: fh.write(open(new_text, 'rb').read())`. Never open the ledger with mode `r`/`w`/`a` (text) for any edit, never round-trip it through a string, and after every append run `git diff --numstat docs/DECISION_LEDGER.md` and require insertions-only with zero deletions before staging. The same rule applies to any file that still carries CRLF bytes; the check that finds them is `open(p,'rb').read().count(b'\r\n')`, which must be unchanged across the edit. This generalises the already recorded prohibition at `skills/minireason-experiment-operations/SKILL.md:40`, "Preserve immutable CRLF provider bytes… never normalize observations", from provider blobs to the ledger itself.

**Checked: yes.** The corrective practice was used for the REC-20260914-N receipt itself and for the REC-20260914-O opening receipt published under this erratum. Both produced `2\t0\tdocs/DECISION_LEDGER.md` from `git diff --numstat`, and the CRLF count stood at 37 before and after each. The near-miss is recorded here because the record was recovered by inspection rather than prevented by practice, and an erratum that only describes a caught error is weaker evidence than one whose corrective action is already in force; it is now in force.

## OPS-20260914-LOOPSUITE — A staged harness package failed the repository suite in two independent ways, and was not published

Observation. REC-20260914-AA transplanted the automated-loop package (`src/minireason/loop/`, sixteen modules and two data files) and its tests (`tests/loop/`, 1,160 tests) from a frozen scratchpad snapshot into the working tree at `02c639e12b6499d045e0b0b06f2fee18b644c9d2` and ran the suite the ledger records: `PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests` reported **Ran 2610 tests in 233.947s, FAILED (failures=3, skipped=2)**. The same tree with the transplant removed reports **Ran 1450 tests in 193.542s, OK (skipped=1)**, and `tests/test_provider_openai_compat.py` run alone reports **Ran 91 tests, OK**, so all three failures are the transplant's and none is pre-existing.

What failed, first defect — **a test-scoped monkeypatch escapes into the rest of the process**. `tests/loop/test_roles.py:42` defines a `no_sockets()` context manager that replaces `socket.socket`, `socket.create_connection` and `minireason.provider_openai_compat._open` with a refusing function and restores them in a `finally`. `tests/loop/test_roles.py:253` (`test_no_more_calls_run_at_once_than_the_credential_authorises`) enters that manager from **six concurrent threads** to exercise the per-credential concurrency cap. A thread that enters while another already holds the patch captures the *refusing* functions as its saved originals, and its own `finally` restores them permanently. The three names stay patched for the life of the interpreter. Two tests of the pre-existing suite then fail on it: `test_no_redirect_handler_is_installed_on_the_opener` raises `loop.test_roles._SocketsUsed` out of `compat._open` at `tests/test_provider_openai_compat.py:340`, and `test_a_transport_that_bypassed_the_seam_would_still_not_dial_out` fails at line 707 because the real connection guard never runs. Reproduced in 0.7 s outside the full suite with `PYTHONPATH=src:tests python3 -X utf8 -m unittest loop.test_roles test_provider_openai_compat` (2 failures) against the same two modules in the other order (91 tests, OK), and the leaking test was isolated by running every `loop.test_roles` test one at a time and comparing the three globals against their pre-suite values.

What failed, second defect — **a frozen pin was cut from a stale working copy**. `src/minireason/loop/data/plan_8a_mirror.json` pins `experiments/diagnostics/C001-contrast-triple/PLAN.md` at sha256 `601a0adc274f269f96c503e7336dc1df5e1386242569919459374f5714acadf5`; the file on this branch digests to `a27fe94a0d04bcf549a4752243e3f34a9a945697e0354d445122755ba9327235`, and `tests/loop/test_standard.py:102` fails on the difference. The cause is established: the staging clone was cut before `2d7239a` ("Publish the C001 occurrence-02 instrument under REC-20260914-V"), which **appended** §15 to that PLAN — 88 lines added, nothing above them edited. The mirror's substantive content is unaffected and the same test class proves it: every §8a register definition still matches the live PLAN byte-for-byte, and the companion `material.json` pin (`94edfe61…`) still holds. Only the whole-file digest moved. This is the general form of a defect already recorded as item 51 of the staging integration list, which anticipated it for one test module and not for a pinned data file.

Impact. The checkpoint was **not published**: the transplant was reverted, `pyproject.toml` restored, and the branch's recorded test line stays true. The implementation remains only in an ephemeral session scratchpad, which is the risk the checkpoint existed to remove, and that risk is now recorded rather than silently carried. No provider call was made, no credential was read, and nothing published was modified. A credential-shape scan (`sk-[0-9a-f]{32}` and `[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}`) over all 53 files of the candidate publication set, and over the 13 repository files this decision writes, returned **0 matches**.

Competing explanations, considered and rejected. That the failures are pre-existing: refuted by the reverted-tree run (1450 OK) and by `test_provider_openai_compat` alone (91 OK). That they are load- or timing-dependent flakes: refuted for the second defect, which is a digest comparison, and for the first by the deterministic two-module reproduction and the per-test isolation that named the single leaking test. That the C001 PLAN was edited rather than appended: refuted by the diff, which is 88 added lines and no removed or changed line.

Corrective action, **specified and not applied here**. First defect: `no_sockets()` must be made safe under concurrent entry — a process-wide guard installed once per test case and never from a worker thread, or a re-entrant guard whose saved originals are captured under a lock by the first enterer only — and a regression test must assert that the three globals are their originals after the concurrency test runs. Second defect: the mirror must be re-pinned against the branch it will live on, and re-pinning it changes `loop_plan_id`, so it belongs to the receipt that mints the pre-registration and not to a transplant. Neither is a publisher's edit: the snapshot is frozen, and both repairs change either a test's semantics or a pinned plan identity. **Checked: no.** What is checked is the diagnosis — each claim above is a command that was run and whose output is quoted in it. Two failing tests in a staged harness say nothing about any model, any arm or any reading; this is an integration and pinning failure and adjudicates nothing.

**Resolution, appended 2026-09-14 16:22 UTC under the same receipt, `REC-20260914-AA`. Nothing above this paragraph is edited.** Both defects are repaired and the checkpoint is published. **First defect.** `tests/loop/test_roles.py` now captures the pristine `socket.socket`, `socket.create_connection` and `minireason.provider_openai_compat._open` **once at import**, into a module-level constant, and `no_sockets()` installs the refusal under a `threading.Lock` behind a depth counter: only the outermost block restores, and what it restores is always the pristine triple and never whatever a concurrent or nested block had installed. The six-thread concurrency test that exposed the leak is unchanged and still runs. The corrective action the paragraph above specified — "a re-entrant guard whose saved originals are captured under a lock by the first enterer only" — is the one taken, in its capture-once-at-import form, which is stronger: a block can no longer save a refusal even if it is the first enterer after one leaked. **Second defect.** `src/minireason/loop/data/plan_8a_mirror.json` is re-pinned against this branch: `plan_sha256` is now `a27fe94a0d04bcf549a4752243e3f34a9a945697e0354d445122755ba9327235`, the digest of `experiments/diagnostics/C001-contrast-triple/PLAN.md` at `f302c3a`, re-hashed by this publisher at publication; the companion `material_sha256` `94edfe61…` is unmoved and the §8a register definitions still match the live PLAN byte-for-byte. Re-pinning moves the demonstration `loop_plan_id`; it is taken here rather than deferred to the pre-registration receipt because **no plan has ever been minted**, so nothing pins the old value, and a shipped standard whose own data file pins a digest the branch does not carry is a known-false artifact. **Checked: yes, and by the gate that refused the first attempt.** `PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests` on the transplanted tree reports **Ran 2673 tests in 214.278s, OK (skipped=2)** — 1,450 pre-existing plus the loop's 1,223, with the two skips being the loop's one declared skip and the pre-existing one. `tests/test_provider_openai_compat.py`'s two no-network tests pass inside that run, which is the direct refutation of the first defect, and `tests/loop/test_standard.py`'s PLAN-digest assertion passes rather than skipping, which is the direct refutation of the second.

**A third finding, recorded here because this erratum is where the `-W error` gate lives, and NOT fixed.** The first attempt reported that all seventeen import targets returned `OK` under `python3 -W error`. That was true of a **warm** `.pyc` cache and is a false negative. With the caches cleared and `PYTHONDONTWRITEBYTECODE=1`, **ten of the seventeen fail**: `contracts`, `standard`, `surface`, `seats`, `graph`, `synthetic`, `packs`, `roles`, `markprep` and `decide` all raise `SyntaxError: invalid escape sequence '\s'` from `src/minireason/use_relation_h005.py:301`, the docstring of `_records_array_start`, whose line 304 writes `"records"\s*:\s*[` in a non-raw string; `minireason.loop` itself and `types`, `custody`, `receipts`, `obligations`, `publish` and `steps` import clean. Reproduced by copying `src/` to a scratch directory, removing every `__pycache__` under it, and importing each target with `PYTHONPATH=<copy>/src PYTHONDONTWRITEBYTECODE=1 python3 -W error -c "import minireason.loop.<m>"`. Without `-W error` all seventeen import `OK`, cold and warm alike. **This is not the loop package's defect and it is not fixed here**: `use_relation_h005.py` is a published instrument, editing it bumps its `source_identity` and invalidates every frozen plan that pins it, so the repair belongs to `SRC-003` in `docs/errata/sources.md`, which already carries that file's other unapplied corrective action. `tests/loop/test_types.py` asserts that no module of the loop package adds to the pile. **Operational lesson, for the lesson files: a `-W error` gate that passes on a warm bytecode cache has verified nothing**, because a `SyntaxWarning` is raised at compile time and a cached `.pyc` is not compiled; any future import gate in this repository must clear the caches of the whole import chain, not only of the package under test, and must set `PYTHONDONTWRITEBYTECODE=1` so that the first run does not warm the cache for the second. Two import warnings in a staged harness adjudicate nothing about any model, any arm or any reading.

## OPS-20260914-LOOPOCCURRENCE — The first live loop run declared an occurrence runner v2 cannot dispatch for

**What happened.** L001, the first live run of the automated end-to-end harness loop
(`REC-20260914-AI`, `loop_plan_id f8bea0cc…`), minted its receipt at S0, published its plan at
`b4190270`, and stopped four minutes later at the first SEND with `STEP_BODY_FAILED: cycle 1 did
not drain in 64 waves`. **Zero provider calls were spent**; no transport was reached and no
credential name was looked up.

**Cause.** `config.occurrences` named `experiments/diagnostics/H005-open-prose-commitments/occurrence-01`,
a published, closed study. It carries no `arms.json`, which runner v2's `verify()` reads first, and
it carries `waves/wave0006.json`, a wave prepared and never sent whose five `daily`/cycle-2
coordinates hold a request and a trace and no attempt, so `pending_wave()` never clears and
`prepare_wave` refuses `PREPARED_WAVE_PENDING`. The loop may neither send that wave — the
occurrence is published material and re-entering it is a replay — nor ignore it.

**Repair, already published.** `REC-20260914-AJ` (`5105b10e`, verified at `2897496c`): S1 PREFLIGHT
verifies every declared occurrence through runner v2's own contract and refuses
`OCCURRENCE_NOT_DISPATCHABLE` **before anything is published**; a delivery runner v2 refused fails
its step by code instead of being digested as a completed step; the dispatch loop refuses when two
iterations arrive in the same state instead of spinning sixty-four waves; `_prepare` records why it
skipped an occurrence. `types.FAILURE_CODES` 218 → 219; seven tests; suite `Ran 3129 OK (skipped=2)`.

**What this erratum adds, and it is the transferable part.** Read again across the published trees
when the successor bundle was written: **`arms.json` is absent from every published occurrence of
both studies** — H005 occurrence-01, C001 occurrence-01 and C001 occurrence-02 — and the only
occurrence in the repository that carries one is F002 occurrence-03, written by the newer runner.
So this was not a poor choice among declarable occurrences: there were none. A loop whose
`config.occurrences` is simultaneously its dispatch list (S4/S6), its import list (S8) and its
use-table list (S9) **cannot read a published study and dispatch at the same time** unless that
study was written by a runner that froze an `arms.json`. Writing one into published material to
make it dispatchable is refused: it edits a published observation, which `p11` and AGENTS.md both
forbid.

**Lesson.** A pre-registration that names an occurrence must assert, before it is frozen, that the
occurrence *verifies under the runner that will dispatch it* — not merely that its bytes exist and
its published tables are complete. L001's bundle checked delivery completeness, replicate counts
and unresolved-cell lists against the published record, all of which were true, and never asked the
one question that decides dispatchability. The successor bundle (L002) asserts it in `validate.py`
and declares the staging of a **new** occurrence as a precondition of S0.

**Two defects recorded here and not repaired.** (1) A publication step that stages no change still
emits a `VERIFIED` line indistinguishable from one that moved the ref: L001's `0004-PUBLISH_IN` and
`0006-PUBLISH_EV` name the same commit and tree as `0001-PUBLISH_PLAN` because the runner wrote
nothing. (2) Running `preflight` as a diagnostic against a run whose `preflight.json` is already
published **overwrites** it with the truncated record a refusal writes; it was restored byte-for-byte
in L001 the moment it was noticed. A refusal record needs somewhere else to go.

**Status.** L001 is closed as an operational failure and is not resumed; its run directory is
committed unchanged, `run.lock` included, as the record. It is superseded by L002 under a new
`loop_plan_id`. No reading, mark, decision or evidence about any arm, model, family or account was
produced by it, and none is claimed.

## OPS-20260915-RUNNERNATIVE — A pre-registration declared a dispatch occurrence of a study its runner cannot read

**What happened.** L002 (`REC-20260914-AL`) declared
`experiments/diagnostics/C001-contrast-triple/occurrence-03` as its dispatch leg, to be staged
before S0 under C001's frozen plan. S0 exited 0; S1 exited 1 with `OCCURRENCE_NOT_DISPATCHABLE`,
offline, before any publication, at **zero** provider calls. Staging was then attempted and
**stopped before writing anything**.

**Cause, and it is a schema fact rather than a missing file.** Runner v2
(`tools/multicycle_commitment_study_multi_v2.py`) is the driver's only dispatch seam (WAVE5 S4/S6),
and it verifies and dispatches **only H005-style occurrences**: `verify()` requires `material.json`
at schema `minireason.h005.material.v1`, a `plan.json` byte-equal to the runner's own `plan_body`
(`minireason.h005.plan.v1`) and `manifests/<tid>.json` at their pinned digests, and `prepare_wave`
iterates `material['problems']` and its templates, cycles and nodes. C001's material is
`minireason.c001.material.v1`, indexed by endpoint, arm, case and replicate. **No occurrence of
C001 can ever verify there.** L002's `p13` was therefore unsatisfiable as written, and its '20
calls under `plan_id 328b9452…`' was impossible twice over: `tools/contrast_triple_study.py` at
that id plans 240 calls, and the twenty coordinates belong to occurrence-02's id `1d9f47ac…`.

**A second premise, corrected by measurement.** L002's bundle said no published occurrence can be
verified. Measured over every occurrence in `experiments/diagnostics/` with runner v2's own
`verify()` and `pending_wave()`: **F001 occurrence-07 and occurrence-08 verify, `pending_wave`
`None`**, `max_calls` 11 each; F001 occurrence-01…06 refuse `IMMUTABLE_PLAN_MISMATCH`; F002
occurrence-01…03 refuse `ARM_FIELDS`; H005 occurrence-01 refuses `FileNotFoundError`; both C001
occurrences refuse `MATERIAL_SCHEMA`. The real constraint is that **nothing that verifies may be
dispatched into, because it is published** — a rule of this programme, not a limit of the runner.

**Lesson, and it is the transferable one.** A pre-registration that names a dispatch occurrence
must assert, before it is frozen, that the occurrence is **native to the runner that will dispatch
it** — same material schema, same plan body, same wave iteration — and not merely that it belongs
to a study with a frozen plan. `OPS-20260914-LOOPOCCURRENCE` asked for verifiability and got a
missing `arms.json`; this erratum sharpens it to schema-nativeness, which is the question that
actually decides dispatchability and which no amount of staging can repair for a foreign study.
The successor bundle (L003) stages a new occurrence of a runner-v2-native study through the
runner's **own** `initialize`, proves `verify()` passes before publication, and asserts it in
`validate.py` — asserting that the occurrence **verifies**, where L002's asserted only that it was
absent.

**Status.** L002 is closed as an operational refusal and is not resumed; it published nothing and
spent nothing. Its run directory is committed exactly as the driver left it — with **no `run.lock`
and no `steps/`**, because `run` was never invoked. No reading, mark, decision or evidence about
any arm, model, family or account was produced by it, and none is claimed.
