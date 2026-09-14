# AHepi/DeepReason at 9607fba6: an inventory

Root review, REC-20260914-M, 2026-09-14. Sentences are marked **Measured** (read
from the clone) or **Interpretation**.

## Provenance and method

**Measured.** The inventory was taken from a read-only clone of
[AHepi/DeepReason](https://github.com/AHepi/DeepReason) at
`/home/user/ahepi/deepreason`, branch `main`, HEAD
`9607fba6f0a3066fbcab282c9ae0fad823e52e0c` ("Merge defended-trial authority
census fix", 2026-09-10), working tree clean at read time, so every hash below is
of committed bytes. `git rev-list --count HEAD` reports 1,578 in a depth-limited
window; the full history is 3,806 reachable commits with root
`377e5965ad20b22b07274655a9151d913d76db0a`, as
[`commitment-interface-source-2026-09-14.md`](commitment-interface-source-2026-09-14.md)
already recorded. Disk: 1.2 GB working tree, 155,204 files.

This inventory was produced by delegated Opus 5 agents under this session's
orchestration mandate, working read-only against clones outside this repository.
Nothing in `AHepi/DeepReason` was modified and its test suite was not run here;
gate figures below are read from committed records, not from an execution. The
selection, the marking of measurement against interpretation, and the
publication are this session's.

## Layout and size

**Measured** (`src/deepreason/`, `mini/`, `tools/`, `scripts/`, `tests/`,
`experiments/`, `config/`, `zoo/`, `runs/`, `skills/`).

| Area | .py files | LOC | Contents |
|---|---|---|---|
| `src/` | 351 | 154,537 | one package, `deepreason` |
| `mini/` | 51 | 11,235 | package `minireason` (17 modules) + scripts + 26 test files |
| `tools/` | 20 | 5,806 | `blast_radius`, `diff_budget`, `docs_verify`, `record_claims`, vendored `treadle` |
| `scripts/` | 66 | 27,972 | experiment drivers, live-run and gate harnesses |
| `tests/` | 421 (416 `test_*.py`) | 154,881 | flat, plus `fixtures/` |
| `experiments/` | 307 | 52,085 | 163 dated tranche directories |

**Measured.** Largest subpackages: `llm/` 15,025 LOC, `workflow/` 12,983,
`bridge/` 12,276, `application/` 8,198, `scratch/` 7,843, `rules/` 7,374, `cli/`
6,446, plus ~35,000 LOC of top-level modules (`harness.py`, `invariants.py`,
`config.py`). Python 3.11+, pydantic v2 throughout; declared dependencies
`pydantic>=2.7`, `pyyaml>=6.0`, `fastembed>=0.3`.

## Spec coverage

**Measured.** Every structural item of harness-spec v1.3 is present in code.
`config.Config` at `src/deepreason/config.py:273` carries all 22 §15 knob rows.
The ontology is `src/deepreason/ontology/{artifact,commitment,warrant,problem,event,state,frozen}.py`.
`att`/`dep` construction and all four closures are `adjudication/edges.py`; the
two-pass adjudicator is `adjudication/grounded.py:12-38` (Kleene fixpoint) plus
`adjudication/support.py:14-33` (topological support cascade); the four labels
are `ontology/state.py:16-22`. `DependenceCycleError` is raised at `edges.py:77`
and enforced at registration in `harness.py:517`. Anti-relapse, the
rubric-verdict guard, the seven spawn triggers, the hv-floor estimator, reach,
schools/capture, and `objects/<schema>/<sha256>.json` storage all exist at named
paths.

**Measured.** `docs/REPORT.md:104-115` states "All phases P0–P6 of the spec are
implemented" with a per-phase acceptance table, and code presence corroborates
each phase (`informal/` for P5, `research/` for P4, `storage/merge.py` for P3, a
`report` verb for P6). **Interpretation.** P0–P6 are reached; current upstream
work is past the v1.3 phase ladder. **Measured, caveat.** `docs/REPORT.md` is
dated 2026-07-05 and its own "84 tests" figure is two orders of magnitude stale.

**Measured — CLI.** §13 coverage is partial. Present in
`src/deepreason/cli/main.py`: `frontier`, `run`, `why`, `theory`, `prose`,
`docket`, `rule`, `schools`, `capture`, `reseed`, `merge`, `trace`. Absent:
`focus`, `expand`, `attack`, `step`. **Measured.** The absence is deliberate:
`README.md:345-349` lists those four, with `make`, `prove`, `check-proof`, `code`
and `simulate`, as "removed" and "outside installed public operation." The
shipped public surface is question-first — `setup / qualify / status / reason /
results`.

## The spec document, and the amendments not adopted here

**Measured.** `docs/harness-spec-v1.3.md` upstream and
[`../sources/harness-spec-v1.3.md`](../sources/harness-spec-v1.3.md) here are
byte-identical: both sha256
`9116c8592387ce22d436cde600d77077d2b08176225f49d1c01613eb8dfb5ca8`, 61,921
bytes, 588 lines. **Measured.** Upstream additionally carries an append-only
amendment chain (`docs/INDEX.md:18-27` — "never edit an earlier file, only add a
new one"): v1.4 (normative — advisory scratch ontology, bounded attention,
RunManifest v3, grounded final-output bridge), v1.5 (normative for RunManifest
v4 — authority boundary, school lineage vs route topology), v1.6 (opt-in
RunManifest v5 autonomous-inquiry boundary, immutable attached evidence), v1.7
(descriptive only). **Measured.** None of the four is present in this
repository, and none is adopted by this publication. **Measured.**
`docs/STATE_OF_THE_PROGRAM_2026-08-14.md` §5 further records three doctrine
amendments that contradict v1.3, including H1, the deletion of "failed verdict ⇒
successor problem", confirmed in code at `rules/spawn.py:62`.

**Interpretation.** Anything designed against v1.3 alone is designed against a
document whose author has since amended it four times. This repository holds
v1.3 as a mechanism guide only (`AGENTS.md:13`), so the amendments are a fact
about the upstream, not an obligation here.

## Providers

**Measured.** One generic OpenAI-compatible transport:
`src/deepreason/llm/endpoints.py:341`, `class OpenAICompatEndpoint`; the only
other endpoint classes are `MockEndpoint` (`:251`) and `EndpointError` (`:105`).
Provider families are a thin quirk layer: `llm/providers.py:100-102` maps
`deepseek`, `openai` and `ollama` to reasoning-knob translators, with
`infer_provider(base_url)` sniffing the URL. Shipped profiles are
`config/deepseek.yaml` and `config/ollama-live.yaml`. **Measured.** There is no
Anthropic support: a case-insensitive grep for `anthropic|claude-3` over
`src/deepreason/llm/*.py` returns nothing.

## Relationship to miniReason's Mini

**Measured.** The two "Mini" packages are unrelated code. DeepReason's
`mini/minireason/` is its own reduced scheduler — "the measured 20% of DeepReason
at ~800 lines" (`mini/minireason/__init__.py:1`) — 17 modules, **no ontology of
its own**, with `log.py` a compatibility view over the parent Harness; it "does
not fork what remains: canonical artifacts, commitments, fail warrants,
attack/support construction, grounded adjudication … all execute in the parent
Harness" (`mini/README.md:24-31`). This repository's `src/creib/forge/mini/` is
29 modules extracted from `AHepi/h-EPI` with a complete independent ontology and
a hash-chained log. Same-named files differ completely (`log.py`: 247 LOC
upstream against 417 here). **Measured.** Upstream contains no statement of why
miniReason was split off; its only references to the other lineage are
read-only operational ones (`experiments/2026-09-06-change-record-claims/`,
which clones h-EPI beside itself under an explicit "never modify or vendor"
constraint) and `docs/CLAIMS_SCHEMA.md:14`, which says the claims-ledger shape
"is adopted from the operator's other harness (h-EPI, …)".

**Interpretation.** DeepReason is neither this repository's predecessor nor its
successor; it is a sibling of this repository's upstream and the source of the
spec document held here. Mini's status-free design is recorded in Mini's own
authority (`../mini/DESIGN.md` §13), not inherited from or lost against v1.3.
Porting between the two Minis would be a rewrite, not a merge.

## DeepReason-Redvar

**Measured.** `AHepi/DeepReason-Redvar` (clone at
`/home/user/ahepi/deepreason-redvar`, HEAD `66b720c`, 2026-09-07) shares no code
with DeepReason: a stdlib-only CLI, 3,868 LOC source and 2,642 LOC tests,
implementing `docs/spec/open-inquiry-0.4.md`, "Open Inquiry 0.4", dated
2026-09-07, whose semantic authority is a Deutsch reading, not the harness spec.
Its §65 states the engine "has no merit ordering, truth probability, novelty
score, argument-strength accumulator, reputation weight, agreement vote,
reward-trained scheduler, best-of selection, or ranked semantic retrieval gate."
**Interpretation.** It is the same operator's prose-first successor line, and it
declines the adjudication semantics that v1.3 §1–§4 is built on — independently
of, and for different stated reasons than, this repository.

## Health signals

**Measured.** The last gate result recorded in a commit body is
`b3f08fd18` (2026-09-10): "full gate 5215 passed, 0 failed, 6 skipped". CI runs
only a wheel smoke across three platforms (`.github/workflows/wheel-smoke.yml`);
the full gate is a local operator instrument (`README.md:373-376`).
`docs/AUDIT_BASELINES.md:12-27` records 0 failed, five tests flaky under `-n 4`
but green serially, and a container-conditional `docs_verify` difference.
**Measured, unresolved.** Two delegated reports disagree on the collected-test
figure — 416 test files with 4,232 `def test_` occurrences against a "5,390-test
gate" headline; the commit-recorded 5,215/0/6 is the figure carried here, and the
discrepancy is left open rather than reconciled.

**Interpretation.** The signals read healthy and disciplined, and the main
structural exposure is that the gate's green state depends on operator practice
rather than on CI.
