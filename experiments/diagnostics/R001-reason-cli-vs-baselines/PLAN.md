# R001 - reason CLI versus baselines

**Draft pre-registration, staged and not run**

Prepared 2026-09-16 in the durable checkout. This is a diagnostic design and offline plumbing proof. No R001 provider/model call has occurred. The independent JUDGE opened REC-20260916-F on 2026-09-16 for this corrected draft. This review made no provider call or Git mutation. The subsequent live occurrence and cross-lineage reading follow under that receipt after the operator freezes the reviewed files; this is not evidence that a live run occurred.

## Owner question and source

Owner standard, verbatim, 2026-09-16:

> it needs to work to improve reasoning in a substantive way that supports error correction and therefore a type of creativity. If you cannot find anything that is better than baseline with prose and an LLM native reasoning, then explain why. Even the failure is informative and worth documenting.

The comparison is read **per problem**: which conditions reached the oracle-correct answer, and by what visible route. Correctness is a bounded fact under the explicit problem premises, fixed before participant execution by a computation or derivation. An independent reader interprets whether a public answer asserts that fact; the reader's impression does not determine the fact.

Governing sources are [PURPOSE](../../../PURPOSE.md), [SEMANTIC_GUIDE](../../../docs/SEMANTIC_GUIDE.md), and [owner rulings 7, 10, 17](../../../docs/reviews/session-rulings-2026-09-14.md). FW5 alone is the semantic target: [designated reading edition](../../../docs/sources/FW5-explanatory-construction.md), SHA-256 8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a. ECS 2.0 is archived and supplies no hypothesis here.

FW5 lines 599-601 require an actual active route with role bindings and content dependence, rather than a similar sentence in an archive. Lines 622-634 distinguish an objection's existence, validity, use, and the content-changing/recoding/carrier contrast contract. Lines 655-672 permit bounded machine checks without a truth machine immune to criticism. Lines 771-777 distinguish complete critical episodes, originative contributions and closure. R001 observes problem-specific public traces; it does not claim to discharge the whole contrast contract, historical New, attributable epistemic repair with all protected uses, or recursive capacity. "Substantive error correction witnessed" below is a declared narrow observational predicate.

The instrument is [tools/reason.py](../../../tools/reason.py), with [workflow](../../../docs/workflows/reason-cli.md) and frozen recipe, prompt, engine, configuration and endpoint identities in SOURCE_PINS.json. Three preserved personal smokes motivated this diagnostic. Smoke-1 stopped after 2 attempts, smoke-2 after 5; both report CEILING_HIT. Smoke-3, 20260916T082621Z-3aaeecdc85-2af16e, completed two cycles with 13 attempts. Its TRACE c0002-k01-o001 took up a retained-left guard, while the objection itself said the concrete trace was already correct. That is visible rule clarification, not evidence that a wrong answer became right beyond NATIVE. Its later use objection repeats the guard after uptake. All originals remain unchanged.

## Fixed eight-problem set

Every problems/PNN.txt is the complete exact task text supplied through --problem, plus the CLI's existing role contract. All conditions receive identical task bytes. Participant seats have prose only: no execution, retrieval, oracle output, sealed answers or study interpretation. The host runs oracles now; it does not reveal them during R001. "Sealed" is an input-exclusion and frozen-hash boundary, not encryption.

All parameters were deliberately selected without random generation, a parameter sweep or participant pretesting. Seed: not applicable; no random generator is used. Difficulty is conjectured from the required reasoning and plausible error mechanisms, not established by model failure. The named traps instantiate familiar reasoning mistakes, but their frequency on these fresh instances is unmeasured. Easy outcomes and baseline success stay in the record. No replacement problem is selected after seeing answers. Independent review expects P04 and especially P06 to be easier than P02 or P08: P06 admits a two-case span argument, while P02 admits a finite Burnside calculation and P08 a finite prefix/dominance proof. These are qualitative difficulty limitations, not provider-tested success probabilities. Baseline-sufficient cases expose where no correction benefit was needed and supply no affirmative evidence that the loop improves reasoning; a null on easy cases cannot establish failure on difficult tasks.

| ID and exact task | Domain and tempting error | Oracle and relation required by later use |
|---|---|---|
| [P01](problems/P01.txt) | Conditional probability: replace an auditor's uniformly selected amber report by mere existence of amber in positions 1-2; wrong 39/86 | Enumerate mode, amber set and selected marker with exact rational weights; correct 7/20. Later inference about position 6 requires selection-weighted evidence, not an existence event. |
| [P02](problems/P02.txt) | Twelve-bead necklaces, four of each named color, adjacent colors different: halve 70 rotation classes to get 35 | Exhaust balanced words, canonicalize the full dihedral orbit and independently use Burnside; correct 41. Reflection-fixed rotation classes must remain unpaired in the later quotient. |
| [P03](problems/P03.txt) | Three-state register automaton: sequentially update registers whose right-hand sides use the same pre-step snapshot | Literal synchronous interpreter plus step trace. Later transitions/output require the pre-step pair, not one old and one new register. Exact output and final state are sealed in answers/P03.md. |
| [P04](problems/P04.txt) | Defined SQL LEFT JOIN and aggregates: ON rejection discards a left row; wrong empty result | SQLite in-memory execution plus independent bag interpreter and grouped derivation. Ordered result Blue,2,1,15 then Gold,1,0,4. Later HAVING/COALESCE use requires synthetic NULL rows and distinct COUNT meanings. |
| [P05](problems/P05.txt) | Trapped air and hydrostatics: use the rim depth for air pressure, giving rise 1.117 m and 177.6 kPa | High-precision quadratic root plus equilibrium check; rise 1.028 m and absolute pressure 167.5 kPa at requested precision. Later Boyle/hydrostatic balance requires interface depth D-y. |
| [P06](problems/P06.txt) | Seven-position constraints: satisfy local order and omit a global inclusive-span equality; wrong AFDCGBE | Exhaust all 5040 permutations and independently check constraints; unique DAFECGB. Later placement must incorporate span(A,B)=span(D,G). |
| [P07](problems/P07.txt) | Finite modular encoder: infer injectivity from an everywhere nonzero formal derivative | Exhaust 19 residues and square-residue derivation. Derivative premise true, conclusion false; preimages of 13 are 3,5,11; absent outputs 4,7,8,11,12,15. Later decoding requires actual fibers. |
| [P08](problems/P08.txt) | Released weighted jobs: never idle when any job is ready; tempting objective 256 | Exhaust all 720 orders plus subset/finish dynamic program; unique minimum 253, E-B-D-F-C-A, idle 6-7. Later dispatch requires the blocking cost for future released F. |

The reusable [reading template](READING_TEMPLATE.md) records the case-level facts and guarded interpretation. Each answers/PNN.md fixes the exact required answer facts, a full derivation, concrete wrong answer and the relation whose uptake changes the answer. Each oracle/PNN.py is independent of participant outputs and emits a JSON answer and diagnostic evidence. oracle/run_all.py checks all eight against the one sealed JSON block per answer and preserves oracle/PNN.output.json. [VALIDATION.md](VALIDATION.md) pastes the actual execution output. The answer facts remain subject to criticism of premises, task wording or the checker; discovering a defect suspends that case and produces a separately named correction, never a rewritten observation.

## Conditions, information and execution

Order is fixed P01 through P08. Complete the four conditions for one problem before starting the next. Within each problem the order is BARE, NATIVE, LOOP-CROSS, LOOP-SINGLE. No inter-problem context is carried; each run's requests contain only the explicit problem and that loop's own public history.

- BARE: deepseek-flash, thinking off, one direct answer logical call, completion allowance 8192.
- NATIVE: same deepseek-flash and baseline prompt, native thinking, requested medium effort, completion allowance 32768 including hidden reasoning and public answer.
- LOOP-CROSS: cross-family recipe, up to three cycles, DeepSeek native conjecture/returns, Qwen3.5-397b.native and GLM-5.3.native critics with thinking off, Qwen off use. One conditional closing return is enabled.
- LOOP-SINGLE: single-family recipe, up to three cycles, DeepSeek native conjecture, one critic, return and use. One conditional closing return is enabled.

Every attempt has the existing 300-second wall and --retry-transport 0. Recipe requested effort and actual wire controls are retained; internal compliance is not inferred. Both recipes set closing_return=true; there is no closing-return CLI switch. An early no_new_objections stop is allowed by the existing instrument and does not establish correctness. A closing call occurs only after cycle_budget when a use objection remains open; absence of a closing call is therefore not an omitted required attempt.

The CLI does not offer a baselines-only zero-cycle run: cycles must be at least one. Therefore one cross-family --baseline invocation provides BARE, NATIVE and LOOP-CROSS, followed by one single-family invocation. The two baseline outputs are separate calls and are never assigned to the loop answer/history. This implements four conditions with two subprocesses, not duplicated baseline occurrences. The baseline instruction differs slightly from the conjecture instruction, which asks for a working answer.

Run labels are R001-PNN-BARE, R001-PNN-NATIVE, R001-PNN-LOOP-CROSS, R001-PNN-LOOP-SINGLE, occurrence 01 only. BARE and NATIVE select calls/base-bare and calls/base-native in the CROSS run; CROSS selects calls/initial, cNNNN roles and final answer in that same run. Each alias records the generated CLI run_id, actual path, condition selector, mode and stop reason in the launcher manifest. A terminal failure is retained and skipped on resume, never silently replaced.

Exact PowerShell commands, from C:\Dev\miniReason, substituting PNN with each fixed ID in order and using fresh short run paths:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH='src;tests'
$env:TMP='C:\tr13'
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -B tools/reason.py run --problem experiments/diagnostics/R001-reason-cli-vs-baselines/problems/PNN.txt --recipe cross-family --cycles 3 --baseline --retry-transport 0 --env-file .env --mode live --out runs/R001-live/R001-PNN-cross
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -B tools/reason.py run --problem experiments/diagnostics/R001-reason-cli-vs-baselines/problems/PNN.txt --recipe single-family --cycles 3 --retry-transport 0 --env-file .env --mode live --out runs/R001-live/R001-PNN-single
```

These are prospective commands, not commands executed in preparation. The complete launcher command and the tested offline command are in VALIDATION.md. The launcher invokes these CLI routes sequentially, accepts --run-root as the manifest directory (including an external directory), maps that absolute path deterministically to runs/R001-<mode>-<10-character-path-hash>, writes a four-condition manifest, and resumes only an existing nonterminal occurrence. The CLI's own custody checks refuse unknown delivered requests as INTERRUPTED_CALL; the launcher never creates a fresh occurrence to circumvent that refusal. Keys go only through the CLI's --env-file option; the launcher never opens that file, emits values or stores them. Offline runs omit --env-file entirely.

## Comparison limits fixed before results

LOOP-SINGLE tests whether the shipped cross-lineage composition changes what is reached, but it is not a lineage-only intervention. It also changes critic multiplicity (two versus one), critic/use identity, thinking mode, completion allowance and fallback opportunities. The larger loop resources also differ from either one-call baseline. Declare these on each reading; neither a correct endpoint nor the witness definition identifies a unique causal mechanism.

A positive diagnostic motivates a separately receipted matched multi-call comparison with the same information, call opportunities, seat multiplicity and completion/wall allowances, plus content-preserving and content-changing objection contrasts. Those controls are required before attributing an advantage specifically to the loop or cross-lineage criticism. They are not extra authorized R001 arms, and their absence cannot be hidden by calling LOOP-SINGLE matched.

## Reading protocol

A later Astra worker, whose actual model identity is recorded before reading and whose lineage differs from all DeepSeek, Qwen and GLM participants, performs the guarded reading under ruling 10. It receives frozen task, oracle and actual public artifacts after participant execution. No future model call is included in this preparation. The reader must not be one of the participant seats. Oracle authoring by this preparation team is not evidence of participant reasoning.

For every condition, record problem ID, label, run ID, source hashes, actual provider/model/settings, attempt IDs, parser/checker identity, terminal state and available final answer. Preserve raw wire requests, public responses, token counts and all repairs/fallbacks. Never persist API keys or native hidden reasoning. Unknown usage stays unknown. Calls, tokens and timing describe resources only.

The reader records:

1. Quote the final task-answer assertions and compare every required fact against the sealed oracle: correct, incorrect or undecidable. Correct requires all requested answer facts at the specified precision with no contradictory task-answer assertion. Incorrect requires an explicit false requested fact or incompatible proposed solution. Missing/incomplete output, refusal, ambiguity or absent essential facts is undecidable with the reason, never imputed incorrect. Explanation validity is separately criticized; output correctness alone is not an explanation finding.
2. For LOOP runs, extract the cycle-0 answer from calls/initial, each returned answer and any closing-return answer. Quote every substantive change from what to what, marking oracle-incorrect to correct, correct to incorrect, unchanged or undecidable. A different wording with the same task commitments is not an answer correction.
3. Quote each critic objection alleged to name the actual trap, its exact challenged claim and its occurrence ID. Verify the allegation against the oracle derivation, not the objection's confidence. Check the actual request delivery to return, then record taken-up, rejected or unresolved; preserve raw rejected-with-reason and the supplied reason. Self-report of uptake alone does not establish changed operative use.
4. For every use call, record its question, problem_derivation and working_derivation. Record whether the problem-derived conclusion reaches the oracle answer: yes, no, undecidable or not the same task. If it asks a subquestion/counterfactual, do not pretend the PNN oracle automatically covers it. Establish a separate explicit derivation under stated premises or mark its bearing unresolved. Record whether the sealed required relation is exercised; a merely confirmatory question may miss it.
5. Record false objections that would move an oracle-correct answer away, the incorrect conclusion they imply, their dispositions and any actual change. Record valid criticisms rejected, stale objections, useful objections left unresolved, unavailable seats, repaired schemas and thinking fallbacks, preserving all failed/partial attempts. Rejected false objections are successful resistance, not missed correction.
6. Write one per-problem comparison naming which conditions reached the answer, the exact visible route and remaining alternative explanations. No pooled quality number, model ordering or aggregate optimization objective is produced. Any adjudicative disagreement or uncertain mapping remains unresolved, with citations and a separate correction artifact if later resolved.

**Substantive error correction witnessed** for one LOOP occurrence requires all five conjuncts: its cycle-0 answer was oracle-incorrect; an actual critic-seat objection named that actual error; the return received and took up that content in the answer; the final answer is oracle-correct; and the same problem's NATIVE baseline was oracle-incorrect. Quote evidence for each conjunct. A use-seat-only correction is separately reported and does not satisfy the critic-seat conjunct. Missing NATIVE output does not satisfy oracle-incorrect. Temporal order plus uptake is a narrow witness, not full FW5 causal identification.

Negative or limiting descriptions are fixed in advance:

- **Criticism failed to return:** an objection names the actual error but return rejects it. Quote both. If it remains unresolved, record that distinct disposition rather than substituting rejection.
- **Criticism blind:** while an answer is oracle-incorrect, no delivered objection names the actual error. Unavailable critics are an operational limit, not evidence they considered and missed it.
- **Criticism harmful:** a previously oracle-correct answer changes to an incorrect one following uptake of an objection. Preserve the false objection, operative change and later recovery if any. A later recovery does not erase the harmful transition.
- **Baseline sufficient:** NATIVE is already oracle-correct. Loop correctness then adds no endpoint correction beyond native thinking on that occurrence.
- Correct loop with incorrect NATIVE but no five-conjunct witness: endpoint difference, route unestablished.
- Resource/schema/transport failure or ambiguous artifact: incomplete comparison, not a content verdict.

## Predictions, falsifiers and successor

Prediction for the claimed mechanism: a delivered content-specific criticism may revise an erroneous conjecture, and its required relation may be applied in the return/use route to reach the oracle answer when NATIVE did not. The predeclared supportive pattern is at least one five-conjunct witness and no harmful correction in either loop across the observed study. A complete supportive study reading requires readable initial/final streams and NATIVE outcomes on all eight cases; if any are missing, retain any local witness but label the study incomplete. It supports only the scoped diagnostic statement that this composition can exhibit correction beyond the native occurrence under these resources. It does not settle why it happened or generalize to tasks outside this set.

The predeclared null pattern is either no fully observed problem on which any LOOP is oracle-correct while NATIVE is oracle-incorrect, or helpful correction events are accompanied by harmful correction events at least as often. For the latter, identify the actual helpful and harmful transitions by problem/arm/cycle, pairing each helpful event with a distinct harmful one where possible. A helpful event is incorrect-to-correct uptake of an objection naming the actual error; a harmful event is defined above. This is falsifier bookkeeping over named events, not a quality measurement or model ordering. Mixed outcomes failing both declared patterns are mixed, not forced into support or null. Incomplete comparisons are explicitly censored and cannot establish the fully observed null. Report the individual cases, including failures, whatever the overall pattern.

A null would make the following explanations live hypotheses for these instances: critic and conjecturer share relevant priors or blind spots despite different lineages; the use check is another fallible inference from substantially the same text and context, not an independent epistemic route; objections may never reach a changed operative decision; false objections may harm correct conjectures. The traces must discriminate these possibilities where possible. FW5 lines 655-672 explain why withdrawing a premise or criticism does not establish its conclusion's falsity or its target's truth; a failure of this instrument does not refute FW5 by itself. A successful oracle also checks only its interpreted premises.

The natural separately preregistered successor is a **checker seat**: use proposes an executable check, the host runs it under declared containment and resource limits, and its actual result returns to the conjecturer. Preserve the proposed check, specification, host execution and criticism of relevance. Do not supply this study's sealed answer to the seat or pretend the result is infallible. Freeze matched multi-call conditions and any recoding/content contrasts before that successor. R001 runs no participant code.

## Budget and claim ceiling

Let L be logical calls including each conditional closing allowance, K native loop logical calls, S the sum of initial completion ceilings and T=32768*K. At zero transport retries, the CLI allows at most one schema repair per logical call plus at most one native-to-off ceiling fallback per native loop logical call: maximum attempts 2L+K, completion allowance 2S+T. A fallback keeps the current messages and native ceiling. Baselines have no ceiling fallback. These are recovery attempts, not a retry of a completed study occurrence. --retry-transport 0 forbids transport retries; the existing CLI has no switch disabling the separate schema repair/fallback policies.

| Condition | Logical allowance | Initial completion allowance | Maximum attempts | Maximum completion allowance |
|---|---:|---:|---:|---:|
| BARE | 1 | 8,192 | 2 | 16,384 |
| NATIVE | 1 | 32,768 | 2 | 65,536 |
| LOOP-CROSS | 14 | 237,568 | 33 | 638,976 |
| LOOP-SINGLE | 11 | 360,448 | 33 | 1,081,344 |
| Per problem | 27 | 638,976 | 70 | 1,802,240 |
| Eight problems | 216 | 5,111,808 | 560 | 14,417,920 |

CROSS subprocess including both baselines: L=16, K=5, S=278528, maximum37 attempts and720896 completion tokens. SINGLE: L=11, K=11, S=360448, maximum33 attempts and1081344 completion tokens. Without conditional closings, there are25 scheduled logical calls/problem (200 across eight); the extra16 closing allowances yield216. Input tokens are additional and unbounded by this completion envelope. Actual billing and reachable provider output may differ; no price estimate is inferred. Sequential worst-case provider-attempt wall allowance is70*300=21000 seconds/problem and560*300=168000 seconds overall (46h40m), plus orchestration overhead. Early termination can reduce all these totals.


Measured-usage planning reference (not a ceiling or a price): independently summing smoke-3 RUN.md gives 13 attempts over 11 logical calls, 70,133 prompt tokens and 41,619 completion tokens, 111,752 total. For CROSS, retain its measured baselines and initial conjecture, scale its two measured cycles to three and add the mean of its two ordinary returns as a conditional-closing proxy: about 110,482 prompt and 54,591 completion tokens per problem. For SINGLE, use that smoke's native baseline completion usage as a proxy for each native critic/use, its native initial/return usage for those roles, and its same-role prompt averages: about 81,641 prompt and 65,579 completion tokens per problem. Across eight problems this explicit planning scenario is approximately 1.54 million prompt plus 0.96 million completion tokens (2.50 million total), far below the 14.42 million completion-only maximum. The reviewer preserved the recomputation as work/review13/budget_check.py and budget-recomputed.json. There is no measured SINGLE-family run, no adjustment validated for these problem difficulties, and smoke-3 used an earlier recipe without closing return. Repairs, growth of public histories, native reasoning and stops can move actual usage substantially; the hard envelope governs spend. No monetary amount is inferred.

Eight fresh instances and one occurrence each cannot certify creativity, establish historical novelty or the model's pretraining repertoire, compare general model standing, or prove a universal capability. Every reading is a guarded, attackable judge-role artifact. This design preserves prose criticism as legitimate and allows the loop to fail. Ending this preparation means the requested draft and offline checks are complete, not that inquiry is exhausted. Reopen for a concrete oracle/task defect, launcher/custody defect, authorized live observation or separately justified matched/checker-seat successor. REC-20260916-F now records the corrected design and budget. Subsequent publication and live execution remain operator work, outside this no-Git-mutation/no-provider-call JUDGE task.
