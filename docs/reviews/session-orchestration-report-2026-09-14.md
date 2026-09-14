# Session orchestration report — 2026-09-14

Branch `claude/project-state-direction-j5rbun`. Written for root. Sentences are
**Measured** (read out of the tree, the ledger, or a command run here),
**Interpretation**, or **Staged** (true of a scratchpad staging tree and *not* of
the published record — every such sentence says so). No scalar score appears
here, no merit claim is made about any model family, arm or contribution, and no
count is a substitute for reading an artifact. Root interprets.

---

## 1. What the session did, and the branch facts

**Measured.** Between REC-20260914-C (00:14 UTC) and REC-20260914-V closed
(09:31 UTC) this session ran as an orchestrator under `CLAUDE.md`: it repaired
the repository's own record-keeping (an after-the-fact `CLAUDE.md` receipt, a CI
gate, a stop decision and then a narrow correction on the E028 `stages_entered`
defect), merged the owner's live H005 work in twice, recovered Mini's requirement
register from `AHepi/h-EPI`, decided and recorded an engine path, vendored the
harness-spec-v1.3 P0 core from `AHepi/DeepReason`, published five offline
instruments and a line-cited review of FW5 against the spec with a dated
correction to its own decision record, ran the two read-only instruments over the
owner's frozen H005 occurrence, pre-registered and dispatched one live study
(F001) across six model families and then two successors at a raised ceiling,
and pre-registered and dispatched a second live study (C001) in two occurrences —
240 calls across six endpoints and two arms, then 20 more on the one cell the
first occurrence could not resolve. **Measured.** `git log --oneline 40bd5de..HEAD
| wc -l` reports **101** commits: 82 are this session's (`Claude`) on the
first-parent line, 19 arrived from `main` (`AHepi`, the owner's live H005 waves)
through two `--no-ff` merges. First branch commit `b55832f` "Record the missing
CLAUDE.md receipt after the fact" (00:25:40 UTC); the last commit before this
report's own publication is `dd2e067` "Correct a commit count in REC-20260914-V"
(09:33:11 UTC). Receipts C through **V** all carry a verified outcome or a close,
the last of them `REC-20260914-V correction at 2026-09-14 09:33 UTC`; this report
is published under **REC-20260914-W**, whose opening receipt precedes it in the
ledger and whose outcome paragraph carries the commit and tree this file lands in.
**Measured.** `PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests`, run
here once against the current tree, reports **`Ran 1397 tests`** and **`OK
(skipped=1)`**; the skip is the pre-existing Windows filesystem-rejection test.
The invocation is recorded beside the number because the count depends on it
(`docs/lessons/operations.md`, E028). **Measured.** `runtime_files` — the 60
paths frozen plans pin — is unchanged all session at `4365421b30be…`, recomputed
here at `dd2e067`; no frozen plan identity moved. `campaign.source_identity()`
changed three times, each disclosed in the opening receipt before the action per
`docs/lessons/operations.md:20`: `3d633011…` (82 files) → `1d163e3e…` (103, the
vendored core, REC-N) → `f7ef0a4f…` (105, the importer, REC-O) → `e198b1a5…`
(108, the transport and use-relation instrument, REC-Q), and it is unchanged
through R, S, T, **U and V** — the two C001 drivers live in `tools/`, not in
`src/`, so 108 files and `e198b1a5fdceb946…` still hold at `dd2e067`. Every
publication went to the working branch; `main` publication remains pending owner
merge.

---

## 2. Findings about the project state, in order of consequence

**Mini was never specified against harness spec v1.3, and the register that
settles it now exists here.** *Measured*
(`docs/reviews/mini-register-recovery-2026-09-14.md`, REC-K): before this session
`docs/mini/`, `docs/kernel.md` and `docs/failure-modes.md` did not exist here, so
twelve by-path citations out of `src/creib/` and 55 annotation labels at 77
`file:line` sites across 25 engine modules could not be looked up at all — Mini's
obligations were unverifiable from inside the repository that runs Mini. Fifteen
documents were recovered byte-identical from `AHepi/h-EPI@b2a3328`, the twelve
path citations now resolve, and 54 of 55 labels resolve to a named file and line.
*Interpretation*, marked as such in the review: `v1.3` and the spec's title occur
nowhere in the fifteen; Mini's authority chain `REQUEST.md` → `DESIGN.md` →
`SPEC.md` is closed; `DESIGN.md` §13 states "No status, no standing, no
elimination." Mini's lack of status machinery is a design decision in Mini's own
authority, not a capability eroded here — which settles the provenance of the
absence and says nothing about whether that is right for this research.

**Harness spec v1.3 is implemented in full upstream; this repository held only
the document.** *Measured*
(`docs/reviews/upstream-deepreason-inventory-2026-09-14.md`, REC-M): every
structural item of v1.3 is present in code at `AHepi/DeepReason@9607fba` — all 22
§15 knob rows, the ontology, all four att/dep closures, the Kleene-fixpoint
grounded pass and the support cascade, the four labels, anti-relapse, the seven
spawn triggers, reach and schools/capture — and upstream's `docs/REPORT.md`
states P0–P6 implemented, with a commit-recorded gate of 5,215 passed / 0 failed
/ 6 skipped at `b3f08fd18`. The spec document here is byte-identical to
upstream's. One item is left openly unresolved: two delegated reports disagree on
the collected-test figure (416 test files, 4,232 `def test_` occurrences, against
a "5,390-test gate" headline); 5,215/0/6 is carried. *Interpretation*: DeepReason
is a sibling of this repository's upstream, not its predecessor.

**H005 is running live on Mini, and this branch carries it only to cycle 1.**
*Measured*: the owner's occurrence-01 reached this branch unchanged at `6d11ae7`;
`checkpoints/wave0005.json` counts COMPLETE 17, OPAQUE 2, PARTIAL 0, FAILED 0,
unresolved attempts 0, **unvisited 223** against the protocol's 240-call initial
schedule, with wave0006 (daily cycle 2) prepared on `main` after the merge point.
Every analysis published here over H005 is therefore of **daily, cycle 1**.

**The matched control arm lost its commitment surface twice in cycle 1, and the
loss is in the carrier.** *Measured*
(`docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md`, CFG-007,
REC-L): `responses/daily/matched/cycle01/response.json` and `carry.json` both
record `envelope_status: OPAQUE` with `status: COMPLETE` and `finish_reason:
stop`, while `mini_prose` and `mini_fcl` recorded five AUTHORED nodes each and no
OPAQUE. Each public text carries raw newline control characters inside JSON
string values — twelve and sixteen — so strict `json.loads` fails;
`decode_contribution` then stores the raw text as `body` and the empty string as
`commitments`, giving the sha256 of the empty string. Parsed with `strict=False`
the same bytes yield exactly `{body, commitments}`, the commitments 2,346 and
2,363 characters. *Interpretation*: the commitments were authored and lost in
decoding — absent by contract (`PROTOCOL.md:56`), not omitted by the model — so a
later cross-arm comparison of commitment persistence that reads the empty digest
at face value would score an encoding fault as an arm that declined to commit.
Two nodes in one cycle establish no systematic asymmetry; no change to the frozen
run is recommended.

**The FW5 review's net judgment is split by role, and it forced a correction to
this session's own decision record.** *Measured*
(`docs/reviews/fw5-vs-harness-spec-2026-09-14.md`, REC-P; 47 findings across six
axes, 19 standing unchanged after refutation): §4 finds that as offline
bookkeeping over authored criticism v1.3 **helps** — the three closures, ν, N1,
Refl, `overrun`, oracle isolation and the audit triple are worth keeping; as an
admission rule it **hinders** (`skeleton-wf` on every informal problem is the
admission form FW5:69 refuses); as a progress meter it hinders most (`accepted`
is silence, not standing; no repair, no protected set, no loss register): "The
spec is not the wrong tool; it is the wrong *primitive*." *Measured*: the dated
`Correction (2026-09-14, REC-20260914-P)` appended to
`docs/reviews/engine-path-decision-2026-09-14.md` retracts that record's claim
that the question is asked "with no mechanical notion of a criticism *landing*" —
under FW5 at the line (FW5:628, :638, :640, :642-651, :653) an adverse edge is
neither necessary nor sufficient for a criticism being taken up, and one finished
cycle exhibits both failures: a `response` conceding an objection in its own words
while minting no edge, and a reinstatement following only from an edge between two
other artifacts. The corrected instrument named is the review's P1. Appended, not
edited (`AGENTS.md:17`).

**F001's mechanism facts: the carrier is read differently by different families,
and four facts did not move at all.** *Measured*
(`experiments/analyses/F001-fork5-multifamily-2026-09-14/README.md`, REC-S and
REC-T): across six families on identical frozen material, topology and rendering,
the register's falsifier is **not met** — `mini_fcl` `read_fcl1` is 5/3/5/0/2/2
(neither all 5/5 nor all 0/5), `resolved/refs` and `dangling` differ (dangling
14/11/19/0/0/0), and the grounded label multiset differs. The declared positive
reading is "this carrier is read differently by different families", explicitly
**not** "family X is better". *Measured*, the four that did not differ:
`depends_cross_document` is **0 in all eight F001 occurrences**, at either
ceiling, on every family; `criticism_of_criticism_retargeted`, ν nodes in `att`,
and reinstatements are 0 everywhere. *Measured*, the constraints: at `max_tokens`
8,192 all seven non-COMPLETE terminal records on occurrences 04 and 05 are
`INCOMPLETE_GENERATION` / `finish_reason: length` at exactly 8,192, five
returning zero bytes; at 32,768 on the same two families `finish_reason: length`
occurs **zero** times, the largest completion is 16,871 tokens, and ten of
eighteen COMPLETE nodes exceeded 8,192 — while both failures there are a
different fact, `TRANSPORT_OR_RESPONSE_ERROR`, "The read operation timed out" at
180,368 ms and 180,456 ms against a **180-second endpoint timeout that is not a
per-arm declaration and did not move with the ceiling**. *Interpretation*: a
ceiling is a transport budget; nothing says the raised ceiling repaired, improved
or degraded anything.

**C001 is published, dispatched in full across two occurrences, and every one of
its reading cells is empty.** *Measured*, against the published record at
`dd2e067` — this replaces the earlier draft of this report, written at `f50db28`,
which described C001 as untracked, unreceipted and undispatched; all of that is
now false. The study implements review proposal **P2** — FW5:630's three-case
contrast triple re-aimed from the judge to the responder at the fork5 `response`
node — delivering one criticism in four codings (ORIGINAL, a content-preserving
RECODING, a CARRIER disturbance, and a no-objection CONTROL) to **one** node with
its instruction and its `account`/`rival` inputs frozen verbatim from H005.

*Occurrence-01* (REC-20260914-U, `plan_id` `328b9452…41c8`, driver
`tools/contrast_triple_study.py`): the driver, the 121-test suite, `PLAN.md`, the
material, the 85-row `RECODING_TABLE.md`, the workflow page and the frozen
`plan.json`/`preflight.json` were published and the remote verified **before the
first provider call existed**. **240 of 240** authorised calls were then spent in
47 waves at no more than five per credential, none retried, none re-sent
(`run` reports `{"dispatched": 240, "planned_calls": 240, "waves": 47, "resumed":
false, "skipped_already_terminal": 0}`). `audit.json` reports COMPLETE **220**,
PARTIAL 9, FAILED 11, `unresolved_attempts` 0, `not_dispatched` 0, envelope
AUTHORED 211 / OPAQUE 18, `envelope_repaired` 93 of 240; `comparison.json`
carries `comparable: true` on exactly **220** of the 240 cells. The only two
failure codes in the run are `INCOMPLETE_GENERATION` 20 and `NO_PUBLIC_CONTENT`
11; there were zero read timeouts on any of the 240 calls. Eleven of the twelve
(endpoint, arm) cells carry all four cases at or above the replicate floor of
three that `PLAN.md` §8 sets; ten carry 5/5 in every case, and `ollama/glm-5.3` ×
`fcl` carries 4/5 on CONTROL. **One cell yields no reading at all, and the cause
named in the record is a ceiling, not a family.** `deepseek-flash` × `fcl`
resolved **1 of 20** usable deliveries — 0/5 ORIGINAL, 0/5 RECODING, 1/5 CARRIER,
0/5 CONTROL: 19 of its 20 coordinates carry `completion_tokens` exactly **8,192**,
that endpoint's own declared ceiling, of which eleven spent the *entire* ceiling
on reasoning (`reasoning_tokens` 8,192) and returned no public content, while the
other nine spent 5,488–7,890 on reasoning and stopped at `finish_reason:
"length"`. The control on that reading is inside the same run: **the same
endpoint, at the same 8,192 ceiling, on the same four cases, is 20 of 20 COMPLETE
on the `prose` arm**, at completion tokens 3,621–6,985. What differs between the
two arms is the FCL-1 instruction, which asks for a second authored document
inside the reply. `PLAN.md` §5 left that endpoint at 8,192 on the stated ground
that it "sends no reasoning on the wire"; 29 of its 40 receipts record
`reasoning_content_present: true`, so the ground is refuted by the run it was
written for. It is **recorded, not repaired**: the plan was frozen before dispatch
and is not edited after the evidence (`PLAN.md` §13), all twenty coordinates are
marked `comparable: false` with their mechanical columns withheld and compared
against nothing, and all four cases of that cell are unresolved under FW5:634. Of
the nine PARTIAL, eight are that cell at 8,192 and **one is `ollama/glm-5.3` ×
`fcl` CONTROL rep2 at exactly 32,768** — the only delivery in the run to reach the
raised Ollama ceiling, AUTHORED but truncated, and rescued by nothing.

*Occurrence-02* (REC-20260914-V, `plan_id` `1d9f47ac…eb83`, successor driver
`tools/contrast_triple_study_v2.py`, a byte copy of v1 with eight `# V2:`-marked
differences proved by `V2DiffProof` and `V1Parity`): the same frozen study on
that one cell at `max_tokens` **32768** and `timeout_seconds` **600**, published
and remote-verified before its first call. **20 of 20 COMPLETE**, every case 5/5,
every one `finish_reason: "stop"`, envelope AUTHORED 20 of 20, `failure_codes` the
empty object — zero `INCOMPLETE_GENERATION`, zero `NO_PUBLIC_CONTENT`, zero
`TRANSPORT_OR_RESPONSE_ERROR`, zero `finish_reason: "length"`, zero read timeouts,
zero retries. One envelope repair (`control/rep2`, `json_strict_false`), so
`strict_parse_would_succeed` is 19 of 20. `completion_tokens` ran **5,783 …
15,470** (total 207,238) and `reasoning_tokens` **3,733 … 12,470** (total
159,324), so reasoning took **64.6 % to 84.7 % of every one of the twenty
completions**; **15 of the 20 exceeded 8,192 completion tokens**, which is the
region in which occurrence-01's nineteen unusable cells died. The largest
delivery is 47 % of the 32,768 ceiling and elapsed time ran 29.1–60.6 s against a
600 s wall clock, so neither bound was approached. *Interpretation*, and it is the
one the receipts themselves insist on: **this is a resource observation, not a
semantic one.** It says the FCL-1 envelope fits beside this model's reasoning at
32,768. It says nothing about any of the four cases, about whether they differ, or
about criticism use. Occurrence-01 is untouched — `git diff --stat` over
`occurrence-01/`, its material, its table, its driver and its suite is empty from
`9045a94` to the closing commit — its nineteen unusable cells stay unresolved, its
denominator is not repaired, and no reader may substitute occurrence-02's cells
for its missing ones. Two ceilings are published side by side, which is what
E001/E002 already require.

*Both occurrences, and this is the point of the study*: **every interpretive cell
is empty by design.** `comparison.json` for occurrence-01 carries 72 of 72
`root_reading` cells and 192 of 192 register-mark cells as empty strings, and
occurrence-02 carries 6 of 6 and 16 of 16 — verified here by reading both files,
not taken from the receipts. No agent filled a column, proposed a reading, or
evaluated a falsifier. The driver refuses to write one (`SCORING_KEY_FORBIDDEN`,
pinned by a test). Nothing in either occurrence marks a comparison, and no count
above warrants one (FW5:851).

---

## 3. What was built and published

| instrument | path | tests | does / does not do | receipt |
|---|---|---|---|---|
| Vendored v1.3 P0 core | `src/deepreason_core/` (21 modules + upstream MIT `LICENSE`) | `tests/graph_core/`, **50** | Ontology, att/dep with the three v1.3 closures, grounded + support passes, event log, object store, P0 harness slice. Not P1–P6, no LLM path, no CLI; adds `pydantic>=2.7` | N |
| H005 graph importer | `graph_import_h005.py`, `tools/import_h005.py`, `data/fcl1.schema.json` | `test_graph_import_h005.py`, **79** → **85** after the Q patch | Replays a finished occurrence's hash-pinned evidence into a spec graph: labels, att edges, warrants, residue table, custody ledger. No provider call, no new arm, nothing written under `experiments/diagnostics/`; invariant **I7** — no label is a semantic attribution | O (patched Q) |
| Use-relation instrument (review P1) | `use_relation_h005.py`, `tools/use_relation_h005.py` | `test_use_relation_h005.py`, **54** | Places each authored cross-document reference beside candidate passages, and stops. No label, no `att`, no `dep`, no score; root's four cells empty in every row | Q |
| OpenAI-compatible transport | `provider_openai_compat.py`, `data/endpoints.json` (24 endpoints), `tools/provider_smoke.py` | `test_provider_openai_compat.py`, **91** | Second transport beside an untouched `provider.py`, mirroring its credential discipline obligation for obligation: request bytes hashed before the socket, write-once records, redaction on write, credential-echo refusal, key read from the environment at call time, native reasoning never persisted | Q |
| Fork5 runner v1 | `tools/multicycle_commitment_study_multi.py` | **69** | Per-occurrence arm declarations, a frozen `scope`, a per-`key_env` gate, publication-before-dispatch, zero retries. Does not edit the owner's runner; does not execute Mini's scheduler | S |
| Fork5 runner v2 | `tools/multicycle_commitment_study_multi_v2.py` | **76** | Byte copy of v1 with four declared differences (header; `CAP` split into `MAX_CEILING = 393216` and `DEFAULT_CEILING = 8192`; `manifest_for` derived from declared arm ceilings; docstring). Does **not** move the default an undeclared arm receives; v1 untouched | T |
| C001 contrast-triple driver v1 (review P2) | `tools/contrast_triple_study.py`; register `experiments/diagnostics/C001-contrast-triple/` with `PLAN.md`, `NOTES.md`, `material.json`, `RECODING_TABLE.md` (85 rows) and `build/` | `test_contrast_triple_study.py`, **121** | One node, one instruction, one system message, two frozen inputs, one varying block; publication before dispatch; per-endpoint ceiling and timeout frozen into the plan and re-tied by `audit`; `prepare`/`verify`/`run`/`audit`/`table`. Writes no score, rank or merit field (`SCORING_KEY_FORBIDDEN`), fills no reading cell, and edits `src/minireason/data/endpoints.json` not at all | U |
| C001 contrast-triple driver v2 | `tools/contrast_triple_study_v2.py`, `material-occurrence-02.json`, `build/build_occurrence02_material.py`, `docs/sources/contrast-triple-deepseek-ceiling-probe-2026-09-14.md`, `probe-2026-09-14/` | `test_contrast_triple_study_v2.py`, **154** | Byte copy of v1 with eight `# V2:`-marked differences, proved exhaustive by `V2DiffProof` and shown plan-equivalent on v1's own material by `V1Parity` except `helper_sha256`. Adds an optional `dispatch_scope` that narrows what is **sent** and narrows nothing that is **frozen**; v1 byte-untouched, occurrence-01 untouched | V |
| Offline CI gate | `.github/workflows/tests.yml` | — | Push/PR gate, Python 3.11/3.12 plus a `pydantic`-floor leg. Leaves `e028-recovery.yml` byte-identical; reaches no provider | E, N |
| Mini requirement register | `docs/mini/` (13) + `docs/kernel.md` + `docs/failure-modes.md` + provenance, review, `SRC-002` | — | 15 documents byte-identical from h-EPI; 12 path citations and 54/55 labels resolved. Does not recover the nine further h-EPI documents the register names | K |
| Snapshot analyses | `experiments/analyses/H005-…-snapshot-2026-09-14/` (160 files); `…/F001-fork5-multifamily-2026-09-14/` (334 + 119) | — | Instrument output over frozen evidence; byte-identity proved by triple generation and eight `diff -rq` runs. Adds no evidence, states no finding | R, S, T |
| C001 occurrences | `…/C001-contrast-triple/occurrence-01/` (240 coordinates, `audit.json`, `comparison.json`, `COMPARISON.md`, 12 juxtapositions) and `occurrence-02/` (20 coordinates, one juxtaposition) | — | Terminal records, custody-checked against the frozen plan (`REQUEST_NOT_FROM_PLAN` and `ARTIFACT_NOT_DERIVED_FROM_DELIVERY` silent on every coordinate). Fills no reading cell and evaluates no falsifier | U, V |
| Reviews, design, errata | the five dated reviews; `docs/design/engine-design-of-record-2026-09-14.md` (13,685 words, **NOT executed**); seven errata (OPS-CLAUDEMD/STAGES/LOGGERUTF8/LEDGERCRLF, CFG-007, INT-009, SRC-002) | — | Record what was found, decided and declined | K, L, M, O, P, Q |

---

## 4. Live spend

| study | authorised | spent | terminal outcome |
|---|---|---|---|
| F001 occurrences 01–06 (runner v1) | **67** | **63** | COMPLETE 56, PARTIAL 2, FAILED 5, OPAQUE 2, unresolved 0, out-of-scope 0 |
| F001 occurrences 07–08 (runner v2) | **22** | **20** | COMPLETE 18, PARTIAL 0, FAILED 2, OPAQUE 1, unresolved 0, out-of-scope 0 |
| C001 occurrence-01 (driver v1) | **240** | **240** | COMPLETE 220, PARTIAL 9, FAILED 11, OPAQUE 18, `unresolved_attempts` 0, `not_dispatched` 0 |
| C001 occurrence-02 (driver v2) | **20** | **20** | COMPLETE 20, PARTIAL 0, FAILED 0, OPAQUE 0, `unresolved_attempts` 0, `not_dispatched` 0 |
| C001 ceiling probe (published records) | **1** | **1** | COMPLETE, `finish_reason` stop, 1,837 ms, 81 reasoning tokens of 100 |
| Transport smoke (scratchpad, outside the repository) | — | **52** (46 chat, 6 model-list) | COMPLETE 32, INCOMPLETE_GENERATION 19, HTTP_307 1 |

**Measured.** The six unspent calls are all F001's and are accounted for — four on
F001 (three on occurrence-04, one on 05) and two on occurrence-07 — all removed
from the queue by the no-retry truncation rule and **never dispatched** rather
than dispatched and lost. C001 spent its authorisation exactly, in both
occurrences, with no coordinate re-sent and no resume needed. **Failure profile by
code.** `INCOMPLETE_GENERATION`: 7 in F001 v1, every one at `finish_reason:
length` and exactly 8,192 completion tokens, five returning zero bytes; **20 in
C001 occurrence-01**, the eleven FAILED plus the nine PARTIAL of the
`deepseek-flash` × `fcl` cell, the provider raising it on both; 19 in the smoke,
all a 64-token ceiling effect. `NO_PUBLIC_CONTENT`: **11 in C001 occurrence-01**,
the validation code on the eleven empty deliveries. `TRANSPORT_OR_RESPONSE_ERROR`:
2, both on F001 07/08, both a 180-second read timeout, and **zero in all 260 C001
calls** — the per-endpoint timeout C001 declared (180 on `deepseek-flash`, 600 on
the five Ollama endpoints in occurrence-01; 600 throughout occurrence-02) reached
the wire on every request record and every provider `settings` block and was never
exercised by a failure. `HTTP_307`: 1 in the smoke — the redirect refusal firing
rather than replaying a credentialed request elsewhere. Zero authentication or
routing failures anywhere; C001 records zero `HTTP_429`, zero `KEY_MISSING`, zero
`PROVIDER_CAP_EXCEEDED`, zero `CREDENTIAL_IN_OUTPUT` and zero `NO_REPLAY`
refusals. **Decode.** F001: `fence_stripped` 20 (v1) and 11 (07/08),
`lenient_control_chars` **0** in both — the control-character loss the register
cites from the owner's frozen H005 `matched` arm did not recur on any family in
scope. C001 occurrence-01: `envelope_repairs` on **93 of 240** calls
(`strip_outer_code_fence` 92, `json_strict_false` 1) against
`strict_parse_would_succeed` **122 of 240**, reported side by side precisely so a
code fence is never read as a reasoning failure, with 18 OPAQUE envelopes that no
declared repair rescued, each preserved whole with its raw delivered bytes
untouched; occurrence-02: one repair, 19 of 20 strict. **The concurrency rule kept
throughout:** at most **five concurrent requests per credential**, enforced by a
module-level semaphore keyed by `key_env`, re-checked in `ready_coordinates`,
refused again in `send-wave` before any attempt marker exists, and guarded at the
socket by `slots_for`; C001 held it twice, by the driver's own `KeyGate` and by
the transport's process-wide semaphore. Because the gate is process-wide, **one
coordinator process** drove all six F001 occurrences, later both successors, and
each C001 occurrence in turn; two processes on one credential were not
authorised. Keys were read only from the gitignored env file into each dispatching
process by a wrapper running with tracing off — occurrence-02 loading
`DEEPSEEK_API_KEY` alone, with `OLLAMA_API_KEY` removed from that environment
because it dispatches no Ollama coordinate — and every credential scan found no
value.

---

## 5. Decisions root may reverse, with the reversal path

**Vendoring from `AHepi/DeepReason`.** `AGENTS.md:7` authorises extraction from
`AHepi/h-EPI` and says nothing about DeepReason; the vendoring proceeded under
this session's user instruction, not a standing authorisation, and the decision
record says so. *Reversal*: revert `c2366dd` (the core) and, if the instrument
goes with it, `6e7dac0` (the importer); `runtime_files` is unchanged by both, so
no frozen plan identity is disturbed. Decision 2 — a fresh vendor-free
`src/deepreason/`, 25 modules in 8 waves with no new dependency — is published
unbuilt and can be adopted instead, or neither.

**Forking a driver rather than editing it (F001's runner v1 then v2; C001's
driver v1 then v2).** The owner's `tools/multicycle_commitment_study.py` writes
its own sha256 into every plan it has built, and C001's `plan_body` writes the
driver's sha256 into every plan as `helper_sha256`, folded into `plan_id`. One
changed byte of either would invalidate published plans — `328b9452…` among them —
and the published C001 v1 cannot express occurrence-02 anyway (`ENDPOINT_COUNT = 6`,
`PLANNED_CALLS = 240` and the arm check each refuse a one-endpoint, one-arm,
twenty-call plan). *Reversal*: all four fork files and their suites are
self-contained and can be deleted; the owner's runner and C001's v1 are
byte-unchanged. Note the coupling first — the eight F001 `plan_id` values and both
C001 `plan_id` values are digests over driver bytes, so removing a driver leaves
those plans unverifiable.

**Per-endpoint ceilings and timeouts, declared before dispatch and never applied
backwards.** F001: `max_tokens` 8,192 (01–06) and 32,768 (07–08) as per-arm
declarations in `arms.json`, with `timeout_seconds` 180 read from
`endpoints.json` and deliberately **not** a per-arm field. C001 occurrence-01:
`timeout_seconds` raised to 600 on the five Ollama endpoints, evidenced by F001's
own two timeout failures, applied to the resolved `Endpoint` value by
`dataclasses.replace` so the registry file is never edited, and proved to change
no request byte by a test on the payload digest. C001 occurrence-02: `max_tokens`
32,768 and `timeout_seconds` 600 on `deepseek-flash`, the ceiling evidenced by one
published probe call and the clock by arithmetic over occurrence-01's own observed
rates. *Reversal*: change the endpoint record or a future occurrence's
declarations. It cannot be applied backwards — every occurrence is frozen, and a
different ceiling is a new pre-registration with its own `plan_id`, as C001's
`PLAN.md` §13 states and occurrence-02 already is relative to occurrence-01.

**Publishing to the working branch rather than `main`.** *Reversal*: root merges
the branch or declines it. `origin/main` was merged in twice, every conflict
resolved by keeping both sides in full with zero deletions, so the histories
reconcile rather than diverge.

**Delegated reviews and staging.** The upstream inventory, the candidate designs
and judgements, the FW5 review (six readers, six critics, six refuters, one
synthesizer), the automated-loop design competition and every instrument's
adversarial review rounds were produced by delegated Opus 5 agents, read-only,
with this session the single publisher. *Reversal*: every finding is offered, not
adopted.

---

## 6. Automated end-to-end loop: decision record

This section records a decision and a design. **Nothing in it is published**, and
every sentence about implementation is marked *Staged*.

**The requirement.** *Measured* (`SESSION_RULINGS.md`, ruling 6, the owner's own
words on 2026-09-14): the harness must run end to end **without a human in the
loop**, as an automated reasoning harness. Interpretive steps — readings, contrast
marks, next-cycle decisions — are performed by harness roles under spec
§10-style guards: cross-family readers, paraphrase and order-swap audits,
program-checked decisive points, disagreement resolving to `unresolved`, and
everything logged as attackable artifacts. **A human is an optional appellate,
never a required step.** That is the standing requirement the design answers, and
it is the reason the question is being asked at all: three instruments in this
repository — `use_relation_h005`, `contrast_triple_study` and the fork5 runner —
stop exactly where interpretation begins, and this branch now carries 13
juxtapositions and 90 use-table rows that nobody has read.

**The competition and its outcome.** *Measured*: three delegated architects each
produced a full design from a declared angle — FW5-faithful automation
(`design-fw5.md`), minimal spec §9/§10 machinery (`design-spec10.md`), and loop
driver and operations (`design-loop.md`) — and two delegated judges scored them
independently. `design-loop` was the consensus winner, 28/30 from both judges.
The design of record is a synthesis, not the winner unaltered: it keeps
`design-loop`'s driver, state machine and operations, and **grafts** `design-fw5`'s
obligations-based stop rule and its write-time guards, and `design-spec10`'s guard
interior, ceiling discipline and grounded-default artifact. Eleven decisions are
recorded with the repository fact that forced each, every one re-read against the
tree at `865a800` — among them that `provenance.role` must be `CRITIC` because the
vendored `ProvenanceRole` enum has no `judge` member and is not to be edited
(vendoring drift); that the reading warrant must be `DEMONSTRATIVE` carrying
commitment `rubric:reading-v1`, because both the transcript gate and the case-law
closure test the commitment's `eval` prefix and neither tests `WarrantType`; that
the C001 baseline rule is enforced at *kind* grain by a program rather than
delegated to a marker; and that the runner is imported in-process rather than
shelled, because `slots_for` is backed by a module-level registry that a
subprocess would silently duplicate.

**The wave plan.** *Measured* (design of record §7): **24 modules in seven waves
of 6 / 6 / 4 / 3 / 2 / 1 / 2**, every `depends_on` naming a module in a strictly
earlier wave, so each wave can be handed to that many parallel agents at once.
Wave 0 is shared types, schemas, the standard artifact, custody, receipts and
publication; waves 1–4 build the surface resolver, seats, obligations, the graph
registration, the step ledger, packs, roles, the C001 pre-pass, the decision
program, the guard trial, the judge audits, the renderers, the reader and the
marker; wave 5 is the driver `tools/auto_loop.py`; wave 6 is the offline
end-to-end acceptance proof and the operator page. Every module lands under
`src/minireason/loop/`, `tools/` or `tests/loop/`. **Nothing in the plan touches
`src/creib/**`, `deepreason_core`, `src/minireason/provider.py`, the owner's
runner, any published occurrence or any frozen plan** — the plan says so module by
module (`touches_frozen: false` on all 24) and the non-goals repeat it.

**The claim ceiling, in one paragraph.** *Measured* (design of record §6, which is
frozen into the pre-registration and which the renderer refuses to emit any table
without): a reading produced by this loop is **a registered, attackable artifact
of a judge role** — `provenance.role = critic` carrying the literal role name —
and never a finding. It **cannot be FW5:628's witness of reason use**: a
transcript supplies no structural map from a represented objection organisation
into a response suborganisation preserving internal role bindings on an active
dependency route, and neither does an ensemble of readers of that transcript, so
the strongest positive outcome available is *consistent-with*. **Unresolved is
first-class and reinstates by computation**: every cell is registered before any
call as an artifact meaning *this cell is unresolved*, a reading attacks it, and
refuting the standard, sustaining an audit hit against the seat's validity node,
or entering an appellate ruling disables the reading's warrant in adjudication
pass 1 so the unresolved artifact returns — no delete, no curation, no status rule
outside `att`/`dep`. Three cell states print as three things (unread, unresolved,
machine-unresolved with its block code), a high block rate is the instrument
declining to read and is never an absence of relations, agreement between two
cross-family readers is agreement between two conditioned generators and not
corroboration by independent observers, a null on the recoding or carrier leg
leaves those rivals unrefuted rather than excluded, **no count is a warrant**
(FW5:851), marks are reported per register and never summed, weighted or ranked,
endpoints are independent occasions to look for one pattern and never competitors
(FW5:849), a reached ceiling is a declared resource boundary and the record must
say which was reached and what would reopen the question, and where
`appellate_rulings: 0` the record may not describe the run as validated, checked
or confirmed. **The stop rule is FW5 R8's repair condition over pre-registered
obligations**, not a count: continue only when a pre-registered *failed*
obligation became satisfied and the artifacts that make it satisfied were
registered by this cycle, with every *protected* obligation preserved and every
loss outside the protected set written down — present and empty rather than
absent when there are none.

**Named risks, kept rather than resolved.** *Measured* (§9.1): the guard buys
behavioural stability, not truth, and two cross-family seats can be stably wrong
in the same direction — the design states this as the largest risk, not fixable
from inside, with the planted-flaw calibration set and the optional appellate the
only levers. Uniqueness of a citation is satisfiable vacuously by a long neutral
span. The variator is unaudited in both directions. A synthetic green dry run
proves the *loop*, not the readings. And the deepest risk is presentational: a
filled table looks more settled than an empty one, and no structural countermeasure
stops a later reader quoting a cell without its provenance.

**Where it actually stands.** *Staged, and not published.* **Wave 0 is
implemented** — `types.py`, `contracts.py`, `standard.py`, `custody.py`,
`receipts.py`, `publish.py` under `src/minireason/loop/`, with the data files
`ceiling_v1.md` and `plan_8a_mirror.json`, and six test modules under
`tests/loop/` — in an **isolated staging clone** of this repository at commit
`9045a94`, where `git status --short` shows both directories as untracked and
nothing else. Its own tests run **197 OK** there, and the clone's whole suite runs
1440 OK (skipped=1) against that clone's 1243 baseline. **Integration is in
progress.** None of it is on this branch: no wave-0 module, no test, no
`tools/auto_loop.py`, no configuration and no pre-registration receipt exists in
the published record, and the published suite figure of **1397** in §1 contains
none of it. *Interpretation*: a design competition, a decision record and a
passing wave-0 in a staging clone are evidence that the plan is buildable; they
are not evidence that the loop reads anything well, and the design says so itself
before anyone else can.

---

## 7. What is waiting on root

**The empty reading cells, in two families.** *Measured*, use-relation: **90
use-table rows carry 360 empty interpretive cells** — H005 `use-table-golden` and
`use-table-full` at 22 rows each, and F001 at 28 + 12 + 6 rows on occurrences 01,
05 and 07 (the other five tables have 0 rows). Every `root_reading`,
`root_passage_cited`, `root_notes` and `root_initials_date` is the empty string.
*Measured*, C001: **78 empty `root_reading` cells and 208 empty register-mark
cells** across the two occurrences (72 + 192 in occurrence-01's twelve tables,
6 + 16 in occurrence-02's one). A blank cell is an **unread row**, not a reading
of `unresolved`; no instrument writes one and none ever will.
`docs/workflows/use-relation-h005.md` §"How root fills the four cells" gives the
vocabulary and states that offsets are code-point offsets into the decoded string;
`PLAN.md` §8a gives C001's four registers, the `differs`/`same`/`unresolved` mark
set, the replicate baseline that must be written first, and the rule that the four
registers are never summed, averaged, weighted or reduced to one mark.

**C001's reading.** *Measured*: thirteen juxtaposition files are published and
unread — `occurrence-01/juxtaposition/<endpoint>__<arm>.md`, twelve of them, and
`occurrence-02/juxtaposition/deepseek-flash__fcl.md`. The declared order is fixed:
root reads the five ORIGINAL replicates and writes the within-ORIGINAL spread on
all four registers into `COMPARISON.md` **before** opening any other case's
juxtaposition for that cell, and the baseline note is not revised afterwards.
Separately, and by a reader rather than by any instrument, occurrence-01's
`deepseek-flash`/`fcl` cell may be set beside occurrence-02's — same node, same
instruction, same frozen inputs, same four codings, same five seeds, two ceilings —
remembering that the two occurrences differ in ceiling *and* wall clock, so a
difference read between them is a resource observation and never a semantic one.
**No further C001 provider call is authorised**: a third ceiling would be a new
pre-registration with its own `plan_id`. **The F001 analysis tables** state counts
and nothing else, with both banners in force; the contributions are unread.

**FW5 proposals P3–P7 are not executed.** P1 was built as the use-relation
instrument (REC-Q) and **P2 was built, published and dispatched as C001** (REC-U,
REC-V); **P3** (criticism-ablation arm), **P4** (loss ledger with O and P pinned
before the later cycle), **P5** (custody and grain preconditions), **P6** (FCL-1's
fields against FW5:622 on the nine objection records) and **P7** (pre-registered
reading set) remain proposals.

**The design of record for the engine is not built**, by decision. **The
automated-loop design of record is not built either**, and nothing of its wave 0
is published (§6).

**The H005 cycle-2+ import.** The branch carries occurrence-01 through
`wave0005`, 17 delivered and 223 unvisited; the owner's run continues on `main`.
Re-running both tools over a longer occurrence is a one-command follow-up — and
the importer's own note stands that the shape of `att` depends on the scope
imported.

---

## 8. Open follow-ups the agents named

- **The endpoint timeout, now moved twice and never exercised** (REC-T, REC-U,
  REC-V): F001 took both its 07/08 failures on a fixed 180-second read timeout
  that was not a per-arm declaration and did not move with the ceiling. C001
  raised it to 600 — the transport's own validation maximum, reached rather than
  invented — for the five Ollama endpoints in occurrence-01 and for
  `deepseek-flash` in occurrence-02, and **no call timed out in 260**. That is not
  evidence the raise was unnecessary: `ollama/glm-5.3` spent 640,721 completion
  tokens over its forty occurrence-01 calls and `ollama/kimi-k3` 419,399, and the
  arithmetic that justified the second raise put a full-ceiling call at 144–215 s
  against the old 180.
- **The `deepseek-flash` ceiling ground is refuted and the correction is an
  append** (REC-V, `PLAN.md` §15): occurrence-01's material and `PLAN.md` §5 give
  `deepseek-flash` 8,192 because it "sends no reasoning on the wire, and 8192 was
  ample for it"; 29 of 40 occurrence-01 receipts and 20 of 20 occurrence-02
  receipts record `reasoning_content_present: true`, and C001's briefs are far
  longer than the H005 briefs that reason was formed on. The published text stays
  exactly as it is, because it is the pre-registration a completed occurrence was
  dispatched under; the correction lives in §15, in the workflow page and in the
  ledger.
- **One delivery reached 32,768** — `ollama/glm-5.3` × `fcl` CONTROL rep2 in
  occurrence-01, a single PARTIAL, reported so a successor's ceiling choice has
  something to land on, and explicitly not a trend.
- **Occurrence-07's six `ref_extension`** (REC-T closed): the first non-zero count
  of that kind anywhere in F001, read by nobody.
- **INT-009, the 39-vs-47 miscount**: the review's body says "39 findings" where
  its mechanically rendered appendix carries 47, of which 19 stand. The review is
  not edited; the banner and appendix header carry the right figures.
- **The H005 `view: commitments` note** (import notes §5 item 12): under
  `view == "commitments"` no BODY section is rendered, so the pseudo-local `#BODY`
  ref has no rendered target — a declared deviation, not repaired.
- **Seed handling**: *I could not find a "seed-echo tri-state" anywhere in the
  published record, and say so rather than invent one.* What is on record is (a)
  the declared asymmetry that `seed: 7` is honoured on every Ollama arm and null
  on DeepSeek, "a property of the providers … reported, not corrected"; (b) the
  importer's `problem_trigger_approximated` code, where imported FCL `problem`
  records must use `SpawnTrigger.seed` because the enum has no `import` member and
  `seed` "slightly over-claims", the named fix being a one-line upstream enum
  addition; and (c) C001's own aggregate, where all six endpoints sent seeds 1..5,
  `honors_seed` was constant within each endpoint and `seed_echoes_reported` was
  **0 on every one** — unknown, and not denied (FW5:634), so the five replicates of
  a case are five samples whose seed effect is unestablished.
- **The E028 `stages_entered` successor plan is still owed** (OPS-20260914-STAGES):
  three writers still place a tuple in the in-memory outcome, unrepairable under
  E026's and E028's live pins.
- **SRC-002 / P-08**, the nine further h-EPI documents the recovered register names
  and did not get, and the missing `extraction-provenance.json` disposition for
  `tests/mini/test_audit_findings.py`.
- **Use-relation open questions**: no read-back validator for a completed table;
  the scope-dependent distinctive-token rule (P5's question, unanswered); a `#BODY`
  ref falling back to the whole owning document's prose; record grain, for which
  the spec has no address.
- **Importer open questions**: whether a prose or empty commitments string should
  also mint a document artifact; `mentions_intra_document` surviving only in the
  side table; criticism-of-criticism retargeting being order- and scope-sensitive.
- **Two disclosed residues**: the use-relation banner cites the review by its
  staging filename `fw5-vs-harness-spec-review.md`; and C001's `.gitignore`
  exception, a single negation line `!experiments/diagnostics/C001-contrast-triple/build/`
  added beneath the blanket `build/` rule so the provenance scripts the receipt
  promised were not silently excluded.
- **Three cadence misses**, recorded at real time and not backdated: ≈510 s
  (REC-L), ≈4,298 s (REC-M), ≈4,167 s (REC-O) against the five-minute deadline.
  The practice adopted — checkpoint the opening receipt before touching a file —
  held the intervals after REC-O, and U and V ran on a per-wave checkpoint cadence
  throughout their dispatches.
- **Two receipt corrections, both by append**: REC-U's register-mark arithmetic
  (48 where the figure is 192; re-verified as 72 of 72 `root_reading` and 192 of
  192 register-mark cells empty) and REC-V's commit count (seven where the
  enumeration it headed lists eight). A published receipt is never rewritten.

---

## 9. Appendix — receipts C to V, one line each

- **C** — After-the-fact receipt for `40bd5de` (`CLAUDE.md`); bytes kept, not backdated.
- **D** — Stop on the `stages_entered` normalization: unappliable without breaking a
  verifying frozen plan identity; defect recorded, nothing changed.
- **E** — Offline push/PR CI gate plus a `work/` ignore rule; `e028-recovery.yml`
  left byte-identical.
- **F** — Closeout of C/D/E: 681 tests, one real failure.
- **G** — First `--no-ff` merge of `origin/main`, resolving only the two append-only
  log files by keeping both sides in full.
- **H** — The E028 test's over-asserting comparison corrected and `campaign.py:151`
  normalised; two code lines, frozen adapters untouched.
- **I** — Closeout of G/H: suite green for the first time at 697 / OK;
  OPS-20260914-LOGGERUTF8 recorded.
- **J** — Second merge of `origin/main`: the owner's 162 live H005 occurrence files,
  12,610 insertions, zero deletions.
- **K** — Mini's requirement register recovered: 15 byte-identical documents, 12 path
  citations and 54/55 labels resolved, `SRC-002` for P-08.
- **L** — The matched-arm envelope asymmetry reviewed and `CFG-007` appended; three
  framing errors corrected in the published text.
- **M** — Upstream inventory, engine-path decision record, and the design of record
  published unbuilt; core and importer named but not published.
- **N** — Decision 1 executed: the core vendored, 50 tests, `pydantic>=2.7`, a third
  CI leg; `source_identity` moved as disclosed; 747 OK.
- **O** — The graph importer published (79 tests, 162 occurrence files pinned) plus
  the three follow-ups REC-N left open; 826 OK.
- **P** — The FW5 review, its 47-finding appendix and the reader précis published,
  with a dated correction appended to the decision record.
- **Q** — The transport and use-relation instrument published with an additive
  importer patch; golden output proved byte-identical; 977 OK; `INT-009` recorded.
- **R** — Both instruments run over the frozen H005 occurrence; byte-identity proved
  by eight `diff -rq` comparisons; all 88 root cells per table empty.
- **S** — The runner fork and F001 pre-registration published, then F001 dispatched:
  six occurrences, four rounds, 63 of 67 calls; falsifier not met.
- **T** — Runner v2 with four proved-exhaustive differences; occurrences 07 and 08
  dispatched at 32,768; 20 of 22 calls; zero `finish_reason: length`; two
  180-second read timeouts; closed 07:31 UTC.
- **U** — C001 published before dispatch (driver, 121 tests, register, material,
  85-row correspondence table, workflow page, frozen plan and preflight at zero
  provider calls), then dispatched in full: 240 of 240 in 47 waves, COMPLETE 220 /
  PARTIAL 9 / FAILED 11, both custody checks silent, one dead cell at an 8,192
  ceiling with the same endpoint's prose arm 20 of 20 as the control, 1243 OK
  (skipped=1); every reading cell left empty; closed 09:05 UTC, corrected 09:06.
- **V** — Successor driver v2 (154 tests, eight proved-exhaustive differences) and
  occurrence-02 published before dispatch, then 20 of 20 COMPLETE at 32,768/600 s
  with no failure code of any kind; reasoning 64.6–84.7 % of every completion and
  fifteen deliveries above 8,192; occurrence-01 proved untouched; 1397 OK
  (skipped=1); the reading left to root; closed 09:31 UTC, with its verified
  closing commit recorded at 09:32 and a commit count corrected at 09:33.
