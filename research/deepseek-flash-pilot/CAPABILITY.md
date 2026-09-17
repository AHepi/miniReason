# DeepSeek Flash capability matrix

Read on 2026-09-17 UTC. W33 made no live provider calls. Opening branch `claude/project-state-direction-j5rbun`, HEAD `836b5c155a30537eafdaec3bd047e7ac5665de51`. No source observation was changed. Source hashes identify the bytes read despite concurrent unrelated work.

## Population and method

Evidence: [R001/R002 per-call census](evidence/r12-calls.json), [summary](evidence/r12-summary.json), [R003 per-call census](evidence/r003-calls.json), [summary](evidence/r003-summary.json), [root sources](evidence/root-sources.json). These supply exact source paths/hashes, usage, ceilings, latency and provider identities for **314 logical Flash seats / 342 attempt records**: R001 112/119; R002 calibration 24/24; R002 main 67/68; R003 111/131. All requested live occurrences, including unsuccessful archives, are included. R001 BARE/NATIVE custody aliases are excluded to avoid double counting canonical LOOP trees; archived old1/old2 remain distinct. Four R001 transport failures have unknown usage, and one missing outer outcome remains unknown despite a retained provider response.

R003 covers all 40 cells under `runs/R003-open-v1/o001` and `o002`: all models 170 logical / 198 attempts / 1,018,064 tokens; actual Flash subset 111/131/696,491. Other-model critic failures are excluded from Flash rates. The manifests retain cell state/RUN and provider receipts. No current parser replay silently replaces historical outcomes.

First JSON means the whole public string parses with ordinary Python json.loads; this permits duplicate keys. Host acceptance means the recorded role check passed, which is stricter than syntax. Repair success means a failed schema attempt became accepted; it does not imply corrected mathematics. Missing content, invalid syntax, contract rejection, ceiling fallback and substantive error are separate categories. These dependent, differently configured samples are not population estimates of reliability.

## (a) Structured output reliability

**Typed R003: 103/103 first responses parse as JSON; 83/103 (80.6%) pass their host contract first time; 10/20 repairs succeed; 93/103 (90.3%) finally pass.** Eight additional schema-free native controls complete and parse, giving 91/111 first and 101/111 final overall; they are not evidence of typed compliance.

| R003 occurrence / seat / frozen schema | First JSON | First host pass | Repairs succeeded / tried | Final failures |
|---|---:|---:|---:|---:|
| o001 / closing-return / `decomposed-closing.schema.json` | 2/2 (100.0%) | 2/2 (100.0%) | not attempted | 0 |
| o001 / conjecture / `answer.schema.json` | 8/8 (100.0%) | 8/8 (100.0%) | not attempted | 0 |
| o001 / conjecture / `none` | 8/8 (100.0%) | 8/8 (100.0%) | not attempted | 0 |
| o001 / decompose-initial / `initial-decompose.schema.json` | 8/8 (100.0%) | 8/8 (100.0%) | not attempted | 0 |
| o001 / return / `decomposed-return.schema.json` | 15/15 (100.0%) | 13/15 (86.7%) | 2/2 (100.0%) | 0 |
| o001 / step / `decomposed-step.schema.json` | 14/14 (100.0%) | 6/14 (42.9%) | 4/8 (50.0%) | 4 |
| o001 / use / `decomposed-use.schema.json` | 15/15 (100.0%) | 14/15 (93.3%) | 1/1 (100.0%) | 0 |
| o002 / closing-return / `prose-return.schema.json` | 3/3 (100.0%) | 3/3 (100.0%) | not attempted | 0 |
| o002 / conjecture / `answer.schema.json` | 8/8 (100.0%) | 8/8 (100.0%) | not attempted | 0 |
| o002 / decompose-initial / `initial-decompose-r3-a1.schema.json` | 8/8 (100.0%) | 6/8 (75.0%) | 2/2 (100.0%) | 0 |
| o002 / return / `decomposed-return-r3-a1.schema.json` | 2/2 (100.0%) | 2/2 (100.0%) | not attempted | 0 |
| o002 / return / `prose-return.schema.json` | 9/9 (100.0%) | 7/9 (77.8%) | 1/2 (50.0%) | 1 |
| o002 / step / `decomposed-step-r3-a1.schema.json` | 1/1 (100.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 1 |
| o002 / use / `decomposed-use.schema.json` | 2/2 (100.0%) | 2/2 (100.0%) | not attempted | 0 |
| o002 / use / `propagation-use.schema.json` | 8/8 (100.0%) | 4/8 (50.0%) | 0/4 (0.0%) | 4 |

Twenty typed first failures receive one repair each; ten still fail. Thirty failed attempts comprise 15 field-length violations, 4 before/after quote errors, 2 fork-locator errors, 2 additional-property errors, and one each duplicate key, final commitment mismatch, missing property, expected-empty field, rederivation suffix, uptake fork and uptake suffix mismatch. These are mainly role/custody obligations, not malformed JSON. DeepSeek critics and synthesis in R003: **NOT FOUND (zero calls)**.

| R001/R002 scope / role | Logical / attempts | First JSON | First host pass | Schema repair success | Final host pass |
|---|---:|---:|---:|---:|---:|
| R001-archive / baseline | 10/11 | 6/10 (60.0%) | 5/10 (50.0%) | 1/1 (100.0%) | 6/10 (60.0%) |
| R001-archive / conjecture | 8/9 | 5/8 (62.5%) | 5/8 (62.5%) | not attempted | 6/8 (75.0%) |
| R001-archive / critic | 4/4 | 4/4 (100.0%) | 4/4 (100.0%) | not attempted | 4/4 (100.0%) |
| R001-archive / return | 10/15 | 9/10 (90.0%) | 5/10 (50.0%) | 0/4 (0.0%) | 6/10 (60.0%) |
| R001-archive / use | 3/3 | 3/3 (100.0%) | 2/3 (66.7%) | not attempted | 2/3 (66.7%) |
| R001-current / baseline | 16/16 | 13/16 (81.2%) | 14/16 (87.5%) | not attempted | 14/16 (87.5%) |
| R001-current / conjecture | 16/16 | 16/16 (100.0%) | 16/16 (100.0%) | not attempted | 16/16 (100.0%) |
| R001-current / critic | 9/9 | 9/9 (100.0%) | 9/9 (100.0%) | not attempted | 9/9 (100.0%) |
| R001-current / return | 27/27 | 27/27 (100.0%) | 27/27 (100.0%) | not attempted | 27/27 (100.0%) |
| R001-current / use | 9/9 | 9/9 (100.0%) | 9/9 (100.0%) | not attempted | 9/9 (100.0%) |
| R002-calibration / answer | 24/24 | 20/24 (83.3%) | 20/24 (83.3%) | not attempted | 20/24 (83.3%) |
| R002-main-occurrence-001 / answer | 4/4 | 0/4 (0.0%) | 0/4 (0.0%) | not attempted | 0/4 (0.0%) |
| R002-main-occurrence-001 / conjecture | 16/16 | 3/16 (18.8%) | 3/16 (18.8%) | not attempted | 3/16 (18.8%) |
| R002-main-occurrence-001 / decomposed_return | 4/4 | 4/4 (100.0%) | 4/4 (100.0%) | not attempted | 4/4 (100.0%) |
| R002-main-occurrence-001 / decomposed_step | 4/4 | 4/4 (100.0%) | 4/4 (100.0%) | not attempted | 4/4 (100.0%) |
| R002-main-occurrence-001 / decomposed_use | 4/4 | 4/4 (100.0%) | 4/4 (100.0%) | not attempted | 4/4 (100.0%) |
| R002-main-occurrence-001 / initial_decompose | 4/4 | 4/4 (100.0%) | 4/4 (100.0%) | not attempted | 4/4 (100.0%) |
| R002-main-occurrence-002 / decomposed_return | 10/10 | 10/10 (100.0%) | 10/10 (100.0%) | not attempted | 10/10 (100.0%) |
| R002-main-occurrence-002 / decomposed_step | 7/8 | 7/7 (100.0%) | 6/7 (85.7%) | 1/1 (100.0%) | 7/7 (100.0%) |
| R002-main-occurrence-002 / decomposed_use | 10/10 | 10/10 (100.0%) | 10/10 (100.0%) | not attempted | 10/10 (100.0%) |
| R002-main-occurrence-002 / initial_decompose | 4/4 | 4/4 (100.0%) | 4/4 (100.0%) | not attempted | 4/4 (100.0%) |

R001 selected current loop seats are 61/61 first accepted. One host-valid baseline has a raw control character tolerated by the historical parser but rejected by strict whole-body JSON. Archived first acceptance is 21/35, final 24/35; schema repairs 1/5 and separate native-to-off fallbacks 2/2. Four archived return repairs still fail. Their historical resolved-objection-ID contract differs from later v2; retain the old failures without attributing every interface defect to the model.

R002 main whole-task answer/conjecture completion is 3/20, with 17 ceilings. Narrow decomposition roles deliver: plans 8/8 first, steps 10/11 first and 11/11 after one repair, returns 14/14, uses 14/14. The repaired step is accepted inability, not solved mathematics. Both main occurrences make zero synthesis calls.

## (b) Thinking, ceilings, latency and tokens

| Scope | Native attempts | Native ceiling hits | Ceiling | Native latency median/max seconds | Known reasoning tokens |
|---|---:|---:|---:|---:|---:|
| R001-archive | 34 | 2/34 (5.9%) | 32768 | 20.164/124.235 | 346,763 (31 receipts) |
| R001-current | 69 | 1/69 (1.4%) | 32768 | 20.953/131.906 | 619,438 (69 receipts) |
| R002-calibration | 24 | 4/24 (16.7%) | 32768 | 40.282/137.296 | 344,049 (24 receipts) |
| R002-main-occurrence-001 | 28 | 17/28 (60.7%) | 32768 | 107.805/164.375 | 659,438 (28 receipts) |
| R002-main-occurrence-002 | 14 | 0/14 (0.0%) | 32768 | 7.477/16.766 | 17,918 (14 receipts) |
| R003 combined | 77 | 0/77 (0.0%) | 32768 | 15.233/57.953 | 240,569 (77 receipts) |

R002 calibration is 20/24 correct and 4/24 exhausted at 32768 with no public answer. The selected hard cases then produce 17/20 whole-task initial exhaustions in main, including all four new native baselines. Across R001/R002 all 24 native ceiling hits have completion=reasoning=32768 and empty public content. Task selection matters: zero R003 ceilings does not cure long derivations. Three archived native transport errors have unknown token spend, so observed ceiling counts are lower bounds when delivery is missing.

Reasoning tokens are included in completion, never added again. R003 native median reasoning usage 2369, maximum 9069; completion sum 309,677. All 77 native records expose numeric reasoning usage without persisted reasoning text. The 54 off-mode attempts have median 3.164 s/max 15.264 s and 41,948 completion tokens, but no numeric reasoning field. Different roles/tasks prevent a causal speed comparison, and field absence is not proof of zero internal computation.

| Scope (all Flash modes) | Prompt | Completion | Total | Latency median/max seconds | Known usage |
|---|---:|---:|---:|---:|---:|
| R001-archive | 99,142 | 391,557 | 490,699 | 19.375/124.235 | 38/42 |
| R001-current | 104,489 | 672,514 | 777,003 | 20.515/131.906 | 77/77 |
| R002-calibration | 24,995 | 363,057 | 388,052 | 40.282/137.296 | 24/24 |
| R002-main-occurrence-001 | 45,793 | 670,107 | 715,900 | 92.953/164.375 | 36/36 |
| R002-main-occurrence-002 | 57,819 | 30,776 | 88,595 | 3.296/16.766 | 32/32 |
| R003 combined | 344,866 | 351,625 | 696,491 | 8.828/57.953 | 131/131 |

Per-call values remain in the linked census files. Smoke REC-20260916-D (`docs/DECISION_LEDGER.md:2070`) separately records 8192 native reasoning tokens, empty public content and 40.922 s at an 8192 ceiling; `:2073` says medium maps to high; `:2103` distinguishes ceilings by mode/route; `:2168` records valid JSON rejected for extra fields. REC-20260917-A/B preserve calibrated difficulty, main initial exhaustion and R003 quote/length failures. These lessons motivate bounded modes and explicit contracts, not blind ceiling increases.

## (c) Context handling

Largest observed Flash wire: **54,381 bytes / 11,697 reported prompt tokens**, completed after repair at `runs/R003-open-v1/o002/r/O03/x/calls/c0002-return/a01/response.json` and its provider/request siblings. It used 3418 completion tokens (564 reasoning), 13.639 s. R001 maximum 35,518 wire bytes; R002 maximum 9672. The actual-byte hashes are in the manifests. These are far below the documented 1M context: near-window retrieval, long-document fidelity and synthesis are **NOT FOUND**.

No Flash API context-limit or safety refusal was found. Task-semantic mentions of refusal are not API refusals; valid cannot_decide is not a safety refusal. R003 o001 had two local GLM repair input-budget refusals before dispatch (ledger`:3641`), which are neither sent Flash wires nor evidence about Flash's context limit.

## (d) Instruction following and exact failure examples

| Role | Evidence and limit | Failure/example |
|---|---|---|
| Conjecture | R001 current 16/16 and R003 typed 16/16 first acceptance, but R002 whole-task 3/20 completion. | Seventeen R002 initials have no public answer at all; quotation NOT FOUND. Correctness varies even when an answer contract passes. |
| Critic | R001 Flash 13/13 accepted across selected/archive; no Flash critic in R002/R003. | Archived P02 critic: "A correct Burnside count over the 24 dihedral symmetries gives 38." Correct answer 41; return initially accepts 38, later use corrects it. Source R001 REPORT`:32`, `runs/LOOP-SINGLE/P02/old1/calls/` below that study. |
| Return | R002 14/14 first; R003 22/26 first, 25/26 final, plus 5/5 closing. | O04 o002 return begins "I revise the proposal to a transparent lottery-plus-waiting-time-priority arrangement." Host: "Uptake must rederive from the challenged fork"; repair still fails suffix agreement. Source `runs/R003-open-v1/o002/r/O04/x/calls/c0001-return/a00/response.json` and a01. |
| Decompose | R002 8/8; R003 14/16 first and 16/16 final. | R002 REPORT`:66` records 6/7-step plans against 3-step budget; none of eight main decomposed cells synthesizes. A valid plan envelope can fail its resource purpose. |
| Step | R002 10/11 first; R003 6/15 first, 10/15 final. | O05 o002 a01 host: "R3-A1 step result must end with the exact final commitment as 'COMMITMENT: <claim>'". Public result COMMITMENT differs from final commitments object. Source `runs/R003-open-v1/o002/r/O05/d/calls/c0002-step/a01/response.json`. |
| Use | R002 14/14; R003 20/25 first, 21/25 final. Propagation subset 4/8 first, no successful repair in 4 tries. | O01/O07 o002 a01: "Fork locator does not quote the named derivation step exactly". Source `runs/R003-open-v1/o002/r/O01/x/calls/c0001-use/a01/response.json` and O07 equivalent. O01 a00 repeats `"result_depends_on_change": true`; duplicate-key JSON rejection is distinct. |
| Synthesis | No R002-main/R003 synthesis call, despite declared seat. | **NOT FOUND**: no compliance or correctness rate. Partial closing is not full synthesis. |

R002 REPORT`:41` additionally identifies wrong accepted local explanations/arithmetic; empty objection/disposition arrays mean 14/14 return delivery is not 14 substantive error corrections. R001 selected NATIVE is correct 7/8 with one ceiling; loops already begin with correct answers. Reports find local explanation repair but no demonstrated loop correction over a completed wrong native comparator. A critic may be useful and false; a source quote may be exact and substantively mistaken. None of these metrics defines creativity.

## (e) API features and repository transport

[API-NOTES](API-NOTES.md) records exact official URLs/read date 2026-09-17 for identifier mapping, context/output limits, prices, rate limits, thinking, JSON, tools/strict mode and streaming. `src/minireason/data/endpoints.json:5` sends official `deepseek-flash`, currently DeepSeek-V4.1-Flash, through the OpenAI route. Transport already supports response_format (`provider_openai_compat.py:523`) and thinking/effort (`:534`); stream:false is fixed (`:518`, override blocked`:447`). Extra tools can enter the payload (`:537`), but normalizer`:764` drops tool_calls and finish handler`:681` rejects non-stop results. An actual tool roundtrip therefore needs the probe-local adapter. Beta strict schemas are documented only for function arguments; free response json_schema is NOT FOUND. Thinking tool continuations require hidden reasoning replay, so this design disables thinking for tool-control turns.

## (f) NOT FOUND and source discipline

Actual self-routing choices, executed pilot spawn DAGs, function-call reliability, beta strict behavior, engineering patch/test success, independent final-judge accuracy, full synthesis, near-limit context fidelity, production reliability and pinned historical weights: **NOT FOUND** in the requested observations. No documented parallel_tool_calls switch was found; API tool_choice can request one or more calls, which the probes test without that flag.

Contract sources: `docs/workflows/reason-cli.md:23`; `src/minireason/reason/prompts.py:48` (role contracts); `r002.py:193` (unique-key parsing),`:223` (fork/return/use checks),`:461` (decomposition),`:1140` (repair); and `checker.py`. Nine R002 and eight current R003 recipes were inventoried and hashed. Current/draft recipes are design evidence; actual run copies/settings define observed conditions. R003 v3 concurrent work is not treated as o001/o002 evidence. R002's checker mechanism was reached for zero actual checker executions, not successful verification.

Custody caveat from REC-20260917-A: R002's 92 all-model prepared/sent bodies have equivalent decoded JSON and lengths but differ in message-member order; exact byte identity was not achieved. Preserve actual provider wires and both hashes. The new probe serializes once and hashes/sends the same bytes. Per `docs/SEMANTIC_GUIDE.md:20`, delivery, contract acceptance, bounded checking and substantive judgment remain separate.


## Later evidence boundary - 2026-09-17T09:30:12.146291+00:00

This matrix above is the W33 pre-probe census. Its NOT FOUND statements are
scoped to those R001/R002/R003 observations. Later interface evidence is in
[PROBE-RESULTS](PROBE-RESULTS.md): the prepared probes were executed separately.
Root independently reopened all 131 Flash R003 attempt outcomes and public
provider responses; per-seat first JSON, host acceptance and repair counts
match the table (103 typed seats, 83 first contract passes, 10 successful
repairs out of 20, 93 final passes). Root evidence: `work/review34/root-recount.json`.
Offline pilot fixtures and transport doubles are not additional model samples.
Production reliability, actual plugin child execution by a live provider,
full-manifest live acceptance and real owner-task success remain NOT FOUND.
