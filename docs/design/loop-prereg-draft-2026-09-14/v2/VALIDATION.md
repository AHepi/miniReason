# VALIDATION — L001 pre-registration bundle

**Regenerated wholesale at the pre-registration review of 2026-09-14 (REVIEW-PREREG PR-08,
recomputation order §D(3) step 7).** The previous `VALIDATION.md` recorded a `config.json` digest
and an `audit={…}` line that predated two edits to `config.json` and a demonstration
`loop_plan_id` that no longer computed. It was **not patched**: a stale line in this file is how
PR-08 happened, and AGENTS.md forbids modifying a published observation. Everything below is the
output of the run actually performed, transcribed, with nothing added by hand.

Run from the bundle directory
`/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-prereg`
with `PYTHONPATH` pointing at the wave-3/4 staging clone
`/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-impl/repo/src`.
The published repository `/home/user/miniReason` was opened **read-only**: nothing under it was
written, and no `git add`, `commit`, `checkout`, `stash` or `reset` was run there. The staging
clone was read only: **no file in `loop-impl/repo` was edited by this revision.**
**No provider call was made; nothing in this bundle has been dispatched.** No credential was read
or printed; the one place the bundle touches a secret at all is `validate.py`'s comparison of
`os.environ.get(env)` against the bundle text, which prints nothing and carries no value into any
failure message.

---

## 1. The command, and its exit status

```
$ cd /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-prereg
$ PYTHONPATH=/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-impl/repo/src python3 validate.py
$ echo $?
0
```

## 2. The full transcript

```
PASS  LoopConfig.load(config.json) -> schema minireason.loop.config.v1, run_id L001-loop-first-live-2026-09-14
PASS  cycle_budget=3 max_calls=396 provider_mode=live max_per_key=5 publish_ref='origin/claude/project-state-direction-j5rbun'
PASS  audit={'period': 2, 'judge_err_max': 0.2, 'judge_err_max_account': "SETTLED at pre-registration review, 2026-09-14, and inside loop_plan_id from S0. What the rate is over: the planted-flaw leg of one audit window, which asks the five anchor kinds the frozen standard body carries - the set audits.build_calibration_set seeds and the only set the share reads - of both judge seats, so the denominator is the (anchor, seat) pairs that window actually exercised, at most five anchors x two judge seats = ten. A pair that returned no ruling went unexercised and is not in the denominator. What 0.2 does over that denominator: the rail fires on strictly greater, so with all ten exercised two disagreeing exercises give 0.2 and do not fire and three give 0.3 and do - the third, not the first. Where fewer were exercised the same bound fires sooner, which is stated here rather than discovered in a stop paragraph. Why here: every anchor's ground truth is true by construction, so a panel disagreeing with three of ten exercises it was asked is not disputing the material - there is nothing in the material to dispute - but failing a set the material cannot make hard; one or two disagreements are left to register as their own demonstrative warrants against that seat's window of readings under design 2.5, which is the finer instrument, and the rail is reserved for the case where that instrument is what is broken. What crossing it means and does not mean: it is a panel-level quantity, one share for the judging panel, never computed per seat, never compared between seats and never rendered as a per-endpoint rate - seats are occasions, not contestants (FW5:849). Crossing it names instrument_fault: it stops the reading arm and Spawns audit-the-reader. It adjudicates no cell, discharges and defeats no obligation of O or P, and carries no evidential reading whatever about the material - a stopped reading arm is the instrument declining to read, never an absence of relations. This figure is itself attackable, and the first run's calibration record is the first occasion on which it can be checked; the four further rows calibration.json pins beyond the standard's five are guard probes and audit-arm exemplars and never enter this share.", 'streak_max': 12, 'streak_max_account': "SETTLED at pre-registration review, 2026-09-14, and inside loop_plan_id from S0. What is counted: consecutive guard blocks per role, over that role's trials in dispatch order within the reading arm, reset by any trial of that role whose outcome is not a block - the definition WAVE3-INTERFACE records for decide.Instrument.block_streak and PREFLIGHT asserts. Per role rather than per run, because the Spawn it fires is audit-the-reader and the roles are the instruments; consecutive in dispatch order rather than cell order, because the fault it detects is temporal. What the earlier account claimed and why it is withdrawn: that twelve is longer than any block run the C001 and H005 published material produced. That premise is false and is withdrawn here - neither study ran this guard and neither emits a block register, so there is no published block run to compare against, and an account may not rest on a quantity the record does not contain. What twelve is anchored to instead, which a reader can check against this bundle: the reading set is 38 declared cells - 4 baseline mark cells costing no call, 12 cross-case mark cells and 22 H005 rows - so a streak of twelve on one role is that role declining an unbroken run as long as the entire cross-case mark leg, or more than half the row leg, without one intervening trial it did not decline. No legitimate stretch of this pre-registered set is expected to produce it; a set whose material really were that uniformly unreadable would show it in the block register long before, and the register prints every refusal under its own reason code so that the declining is visible rather than inferred. What crossing it means and does not mean: it names instrument_fault, stops the reading arm and Spawns audit-the-reader. It adjudicates no cell, is no clause of the O/P repair condition, and is never a finding about the material: a high block rate is the instrument declining to read and is never an absence of relations. The figure is attackable and this run's own block register is the first evidence against which it can be attacked; changing it after first look mints a new loop_plan_id."}
PASS  contrast={'attached': True, 'study': 'experiments/diagnostics/C001-contrast-triple', 'occurrences': ['experiments/diagnostics/C001-contrast-triple/occurrence-02']}
PASS  pin  src/minireason/data/endpoints.json                   03eff16b8f575c113871a1266439874b2622a75d200ecb84a1b79464aa98aee7
PASS  pin  src/minireason/graph_import_h005.py                  e5bd327a8637e8d6a87c0a3440ca6d0e6f2290989df0fba4339fcc8b1d17092a
PASS  pin  src/minireason/provider_openai_compat.py             cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db
PASS  pin  src/minireason/use_relation_h005.py                  568d1cfcc8f55dd9579e632b8f8d4f830584cf3d01c377f3fca97ef0d45bca16
PASS  pin  tools/contrast_triple_study.py                       f5f9dfcadd8bdd769821213b5c09d569480daa20db3a5e8d8d763efd9e08688b
PASS  pin  tools/multicycle_commitment_study_multi_v2.py        8f7eb9d73e8c497f6a2aabf826a8409bb3c60682b36aaa361f650a9e870adbd0
PASS  loop_plan_id over the six required pins is one id from file and object (0ec5ec6abb8faf6293abe5e40a9586c0775f7fabcaff574649a1d2d787445125); a changed pin changes it (4045d671509b022c...); a five-entry map is refused PIN_INVALID
PASS  publish_ref is explicit (ruling 2 branch); both guard-rail accounts are SETTLED, non-empty, and carry no PROVISIONAL and no promise to change themselves
PASS  refused as CONFIG_UNKNOWN_KEY
PASS  refused as CONFIG_MISSING_KEY
PASS  refused as CONFIG_MISSING_KEY
PASS  refused as CONFIG_INVALID_VALUE
PASS  refused as CONFIG_INVALID_VALUE
PASS  refused as CONFIG_INVALID_VALUE
PASS  seat critic    ollama/kimi-k3           family=ollama-cloud/kimi      key_env=OLLAMA_API_KEY     timeout_seconds=180
PASS  seat defender  ollama/gemma4-31b        family=ollama-cloud/gemma     key_env=OLLAMA_API_KEY     timeout_seconds=180
PASS  seat variator  deepseek-flash           family=deepseek               key_env=DEEPSEEK_API_KEY   timeout_seconds=180
PASS  seat judge-1   ollama/gpt-oss-120b      family=ollama-cloud/gpt-oss   key_env=OLLAMA_API_KEY     timeout_seconds=180
PASS  seat judge-2   ollama/qwen3.5-397b      family=ollama-cloud/qwen      key_env=OLLAMA_API_KEY     timeout_seconds=180
PASS  G0 constitution: 2 judge families distinct; critic not in judge families; defender distinct from critic and from judge families; 5 distinct families over 5 seats
PASS  reopen_reasons, paraphrase_n, schema_repair_budget and min_judge_families equal standard.REOPEN_REASONS / standard.GUARD_PARAMETERS
PASS  reading_set.json entries == config.reading_set, 38 unique keys (16 c001-mark + 22 h005-row)
PASS  max_calls derivation: 0 (baseline) + 108 (12 cross-case x 9) + 242 (22 rows x 11) + 46 (one audit window) + 0 (dispatch) = 396 == config.max_calls
PASS  obligations.json canonical-body sha256 3bda592108ac11aee8fe34da5b4317001156d18417af397ee6957f310ce55900 reproduces over canonical bytes; |O|=7 |P|=12; every clause carries a why_not_a_count note
PASS  obligations.pin() (the digest folded into loop_plan_id) = 910282bb43de93bd9fdd1498ec279a177fcaee3b815ebdc8e8a6eea4a9179045; obligations.canonical_pin() (the digest the prose publishes) = 3bda592108ac11aee8fe34da5b4317001156d18417af397ee6957f310ce55900; the two are different values over one document and both are named
PASS  contracts.assert_no_scoring_keys passes over all four bundle JSON documents (calibration.json's former `scoring` key is now `error_rule`)
PASS  calibration.json: 16 source-byte digests re-verify against the published files; every quoted span occurs exactly once in its source record
PASS  cal-05's framing-only quote occurs once in the banner and in no record; cal-07's duplicated sentence occurs once in o2 before the construction adds its second copy
PASS  cal-08's two order-swap pairs re-read from the published comparison.json: (empty, empty) -> same; ({n1,n2,n4}, {n1,n2}) -> differs
PASS  calibration.json carries 9 rows covering every standard.CALIBRATION_ANCHORS id (5 kinds) plus 4 bundle-pinned guard probes the standard body does not carry, declared as such in anchor_set_extension (PR-21)
PASS  cal-01 probe (REVIEW-WAVE1 B3 / PR-06): the referring-region-only construction resolves uniquely inside a declared span at every window (20, 40, 80, 657), and the former two-copy construction resolves at none of them; the module anchor and the bundle row both carry the repaired construction
PASS  C001 occurrence-02: 20/20 replicates COMPLETE, unresolved_cells empty - the order rationale holds
PASS  H005 golden and full use tables carry byte-identical row lists (22 rows); the published 90-row figure counts them twice and the reading set names them once
PASS  reading_set.json vocabularies: six reading values, five nominable relations, three marks, four per-register difference-kind sets, ten block codes, nine ceiling reasons, ten printed register headings, four cell states, three reopen reasons, seven stop reasons and five calibration anchor kinds all equal their module constants
PASS  bound critic    ollama/kimi-k3           wall=min(180,300)=180s  wall_ceiling=8100  max_tokens sent=2048  thinking=not sent
PASS  bound defender  ollama/gemma4-31b        wall=min(180,300)=180s  wall_ceiling=8100  max_tokens sent=1024  thinking=not sent
PASS  bound judge     ollama/gpt-oss-120b      wall=min(180,300)=180s  wall_ceiling=8100  max_tokens sent=2048  thinking=not sent
PASS  bound judge     ollama/qwen3.5-397b      wall=min(180,300)=180s  wall_ceiling=8100  max_tokens sent=2048  thinking=not sent
PASS  bound variator  deepseek-flash           wall=min(180,300)=180s  wall_ceiling=8100  max_tokens sent=4096  thinking=False
PASS  reading_set.json resource_conditions reproduce roles.ROLE_MAX_TOKENS, the min(timeout, 300) gateway-wall rule, the 8100-token wall ceiling and the thinking=False-on-deepseek-only rule exactly
PASS  PREREG.md contains standard.CEILING_TEXT byte-for-byte, all 11 CEILING_REQUIRED_SENTENCES, all 10 PREREGISTRATION_REQUIRED_SENTENCES, both obligations digests, and the three clone-side pins with their re-read sentence
PASS  PREREG.md prints every enumerated token, names twelve unread C001 occurrence-01 juxtapositions, carries the impossible receipt placeholder, the ruling-2 branch deviation and the Account non-goal sentence, and no longer carries the word PROVISIONAL
PASS  every bundle file passes the standard's forbidden-stop-token scan
PASS  the bundle names DEEPSEEK_API_KEY and OLLAMA_API_KEY only as key_env names; no key value, no assignment form and no secret-shaped token appears anywhere

ALL CHECKS PASSED
```

## 3. What each check establishes

| line | what it establishes |
|---|---|
| `LoopConfig.load(config.json) …` | the frozen config loads against `types.LoopConfig.from_mapping`, which refuses an unknown key rather than ignoring it and requires all three `AuditConfig` thresholds and both of its required accounts — a threshold appearing by default was never pre-registered |
| `cycle_budget=… publish_ref=…` | the declared budget, spend mode and **explicit** publication ref (PR-11; ruling 2) |
| `audit={…}` | the three guard-rail parameters with the two settled accounts printed in full, so the bytes that would be interpolated into an `instrument_fault` stop paragraph are visible here (PR-09) |
| `pin  <path> <sha256>` ×6 | every member of `types.PINNED_SOURCE_PATHS` pinned at its real digest; the one-entry map the old validator used is refused `PIN_INVALID` (PR-07) |
| `loop_plan_id over the six required pins …` | the identity is one value from file and from object, changes when a pin changes, and refuses an incomplete pin map |
| `publish_ref is explicit … both guard-rail accounts are SETTLED` | no `PROVISIONAL` and no promise-to-change survives in a field that is inside `loop_plan_id` (PR-09, §D(2)) |
| `refused as CONFIG_*` ×6 | negative controls: the loader refuses an unknown key, a missing block, a missing threshold, an unknown spend mode, an over-cap `max_per_key` and a duplicated reading-set entry |
| `seat …` ×5 | every seat exists in `endpoints.json` at its declared family, `key_env` and `timeout_seconds`; no endpoint and no family is invented |
| `G0 constitution …` | two judge seats from two distinct families, critic outside both, defender distinct from critic and from both judge families — five distinct families over five seats |
| `reopen_reasons, paraphrase_n …` | the config's guard parameters equal the frozen standard's, so the two owners cannot diverge |
| `reading_set.json entries == config.reading_set …` | 38 unique declared cells, 16 marks + 22 rows, in the pre-registered order |
| `max_calls derivation …` | `0 + 108 + 242 + 46 + 0 = 396` reproduces and equals `config.max_calls` |
| `obligations.json canonical-body sha256 …` | the declared digest reproduces over the canonical body; |O| = 7, |P| = 12; every clause carries its `why_not_a_count` note |
| `obligations.pin() … canonical_pin() …` | **both** digests of the one document, named and attributed, and asserted unequal (PR-02) |
| `contracts.assert_no_scoring_keys …` | no bundle JSON carries a key from `standard.FORBIDDEN_KEYS` — the check the old validator did not run, and the one that would have caught PR-01 |
| `calibration.json: … source-byte digests re-verify …` | every anchor is assembled from published bytes and every quoted span occurs exactly once in its source record |
| `cal-05's framing-only quote … cal-07's duplicated sentence …` | the two constructions that must block, checked against the published bytes before the construction adds its second copy |
| `cal-08's two order-swap pairs …` | the mark ground truth recomputed from `occurrence-02/comparison.json`, not asserted |
| `calibration.json carries 9 rows … plus 4 bundle-pinned guard probes …` | the anchor-set extension is declared, and the four rows outside the standard body are named by id (PR-21) |
| `cal-01 probe (REVIEW-WAVE1 B3 / PR-06) …` | the repaired referring-region-only construction resolves uniquely inside a declared span at every window, and the old two-copy construction resolves at none — the test the wave-1 review asked for, now permanent |
| `C001 occurrence-02: 20/20 …` / `H005 golden and full …` | the two published-material facts the reading order rests on, re-read from the published files rather than quoted |
| `reading_set.json vocabularies …` | every enumerated list equals its module constant, so the bundle's declared narrowings are checkable from the record (PR-25) |
| `bound <role> <seat> wall=min(180,300)=180s …` ×5 | the declared resource conditions are the bounds that will actually be sent, seat by seat (PR-10; rulings 13, 14) |
| `reading_set.json resource_conditions reproduce …` | `ROLE_MAX_TOKENS`, the gateway-wall rule, the 8100-token ceiling and the thinking-off-on-deepseek-only rule, all equal to `roles` |
| `PREREG.md contains standard.CEILING_TEXT …` | the frozen ceiling is present byte-for-byte, both required-sentence sets are complete, both obligations digests appear, and the three clone-side pins appear with their re-read sentence |
| `PREREG.md prints every enumerated token …` | twelve unread juxtapositions, the impossible receipt placeholder, the ruling-2 deviation, the Account non-goal, and no `PROVISIONAL` |
| `every bundle file passes …` | no file describes a reached boundary as the inquiry running out of things to say |
| `the bundle names DEEPSEEK_API_KEY …` | key **names** only; no value, no assignment form, no secret-shaped token |

## 4. Bundle digests at the time of validation

*(`VALIDATION.md` itself is absent from the table: a file cannot carry its own digest.
`REVIEW-PREREG.md` is absent because it is the review this bundle answers, not part of what the
run pins.)*

| file | sha256 |
|---|---|
| `PREREG.md` | `0dbfae63f8f49b583e31e341c6149f4b6352a7497e387907fc5ef2867739ae28` |
| `CHANGES-PREREG.md` | `6d6264b66338c57531ad109ae54705e7f0607452a47759081ad5a60409e7ae25` |
| `CLONE-PATCH.md` | `1e598cb7352c14dbbdb3ef0de6f9bee6b4bbcbe1e7400992497aa1c4d37c030d` |
| `calibration.json` | `eaf41d3eed98f7ba839ab604367c3daf3f92d7cf07a658694bd9cdd5539a5e38` |
| `config.json` | `63879991dd632f016e9917ab336fca872b29f16a527e4b67621e189478c38ec0` |
| `obligations.json` | `910282bb43de93bd9fdd1498ec279a177fcaee3b815ebdc8e8a6eea4a9179045` |
| `reading_set.json` | `929868e8869788c8483029c1a36246b1cc9429f7fb90f0ab3934b80795e238e7` |
| `validate.py` | `5f47c46bb2e80264ae56b316a4ab17b4162052c055150875cf7599247ea9d265` |

**The two digests of `obligations.json`, which are not the same value and are both published:**

| digest | value | where it goes |
|---|---|---|
| canonical body (`obligations.canonical_pin`) | `3bda592108ac11aee8fe34da5b4317001156d18417af397ee6957f310ce55900` | declared in `obligations.json:obligations_sha256`, published in `PREREG.md` §3 |
| file (`obligations.pin`) | `910282bb43de93bd9fdd1498ec279a177fcaee3b815ebdc8e8a6eea4a9179045` | **folded into `loop_plan_id`**, re-derived from the tree by `custody.verify_pins` |

## 5. The six source pins, as read at this validation

| path (under `/home/user/miniReason`) | sha256 |
|---|---|
| `src/minireason/data/endpoints.json` | `03eff16b8f575c113871a1266439874b2622a75d200ecb84a1b79464aa98aee7` |
| `src/minireason/graph_import_h005.py` | `e5bd327a8637e8d6a87c0a3440ca6d0e6f2290989df0fba4339fcc8b1d17092a` |
| `src/minireason/provider_openai_compat.py` | `cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db` |
| `src/minireason/use_relation_h005.py` | `568d1cfcc8f55dd9579e632b8f8d4f830584cf3d01c377f3fca97ef0d45bca16` |
| `tools/contrast_triple_study.py` | `f5f9dfcadd8bdd769821213b5c09d569480daa20db3a5e8d8d763efd9e08688b` |
| `tools/multicycle_commitment_study_multi_v2.py` | `8f7eb9d73e8c497f6a2aabf826a8409bb3c60682b36aaa361f650a9e870adbd0` |

## 6. Pins that live in the implementation clone, not in the bundle

These three were read from
`/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-impl/repo/src/minireason/loop/`
at this validation. The clone is under live edit by a wave-4 integrator and
`STANDARD_BODY_SHA256` has moved three times in the review window, so each carries the same
status sentence and none of them is treated here as final:

| pin | value at this validation | status |
|---|---|---|
| `standard.STANDARD_BODY_SHA256` | `a9007dc73c748cfff974a1a3d77098d380ec153b1b8cf93f513cafa3ea0572d7` | **to be re-read at PREFLIGHT after the clone freezes** |
| `standard.CEILING_SHA256` | `1e26be087483fd1b9c8e2c403cfae646fb07ebc773f23434a0c4dfab3ed04c1e` | **to be re-read at PREFLIGHT after the clone freezes** |
| `audits.CALIBRATION_EXCHANGES_SHA256` | `91c29e1e71719d815c21c2697f4aa68a7c983be21df945ad6b1e5042183981e5` | **to be re-read at PREFLIGHT after the clone freezes** |

## 7. The demonstration `loop_plan_id`, and what it is not

The `loop_plan_id` printed in the transcript is taken over the **real** six-entry pin map — unlike
the previous file's `cc7c137f…`, which was taken over a one-entry placeholder — but it is still a
**demonstration digest only**. It is shown to establish that the identity is a pure function of
(config, pins): one value from the file and from the object, and a different value when one pin
changes.

The run's real `loop_plan_id` is minted at S0 PREREGISTER over the full pin set — the six
`PINNED_SOURCE_PATHS`, every prompt template, `obligations.json`, `CEILING.md`, the `STD_READING`
body, `audits.CALIBRATION_EXCHANGES_SHA256`, and each attached study's `PLAN.md` and
`material.json` — and is written into `plan.json` and published before the first call. **Nothing in
this bundle mints it**, and nothing in this bundle mints a receipt id or a run timestamp: those
placeholders are labelled as placeholders in `PREREG.md` and are minted at S0.

## 8. What this validation does not establish

It does not establish that the clone will still be at these module digests when the plan is
minted; §6's three pins say so in terms. It does not establish that any cell will read, and
nothing in it is evidence about the material. It establishes that the bundle is internally
consistent, that its declared values are the values the program will use, and that it does not
fail its own protected obligations before the first call.
