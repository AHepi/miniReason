# Harness lessons register: September 2026

Required reading before building a configuration, recipe, contract, seat, launcher or study. Owner instruction, verbatim: "lean on all the fail modes and lessons learned when building new configurations."

This register implements that mandate through 53 source-bound lessons. A rule applies to its named version and occurrence; a later amendment does not change an earlier observation. Checks below are questions for a new brief or prospective qualification, not claims that W41 executed experiments. Mechanism checks do not define explanatory bearing. [Source and scope: PURPOSE.md][purpose], [docs/SEMANTIC_GUIDE.md][semantic], [docs/lessons/README.md][lessons].

Reading cutoff: 2026-09-17 UTC, durable working checkout, opening HEAD `b8c43a179ec830c3ab9d29b79c2b19e621b07194`. Some sources were concurrently uncommitted. W41 source hashes, ranges and later-change checks are in [work/w41/INDEX.md][w41]; this is a source reading, not publication verification. The REC-20260917-F receipt is a draft there. Referenced judge rounds are engineering or reading judgments with their stated limits, not additional participant trials.

## Model behaviour

### L1. Thinking can consume the answer budget

**Fail mode:** Native reasoning can consume the entire completion allowance without producing a public answer.

**Where it bit:** Smoke-1 used all 8192 completion tokens as reasoning; R002 hard-case initials repeated empty length stops at 32768. [docs/DECISION_LEDGER.md, REC-20260916-D and REC-20260917-A][ledger]; [R002 REPORT][r2].

**Rule now:** Preserve `CEILING_HIT` as a resource outcome; R002/A2 stops immediately without fallback or schema repair, while the personal CLI has a separately versioned fallback policy. [R002 PLAN A2.2][r2plan]; [reason-cli workflow, recovery policies][cli].

**Check:** Does the brief identify reasoning exposure, completion allowance, public-answer availability and the exact version's stop/fallback policy? Can an empty length stop reach a critic by accident?

### L2. Delivered prose can fail a JSON seat

**Fail mode:** A provider can finish normally with useful public prose that is not the JSON document required by its seat.

**Where it bit:** R002 C05/C06/C12 cycle-2 GLM critics finished `stop` but failed parsing at character zero, despite requested JSON mode. [R002 PLAN A2.1-A2.2][r2plan]; [judge round 24][j24]; REC-20260917-A.

**Rule now:** Preserve provider completion and contract failure separately; a permitted schema repair is bounded, and prose remains available for reading. JSON mode is not contract certification. [reason-cli workflow][cli]; [R002 PLAN A2.2][r2plan].

**Check:** Does the saved outcome distinguish complete prose, malformed JSON, schema-invalid JSON and length termination, and retain the actual failed text?

### L3. Exploratory objections can withdraw themselves

**Fail mode:** A critic can place a long retrace in an objection object even though its own final conclusion withdraws the objection.

**Where it bit:** Smoke-3 delivered an 18326-character retrace; R001 preserved twelve self-withdrawing or confirmatory objects in eight critic attempts. [judge round 12b][j12b]; [R001 REPORT][r1]; REC-20260916-D/F.

**Rule now:** The personal CLI separates visible `working` from final objection `text`, limits that text to 1200 characters, and excludes working from downstream objection history. Faithful repair may yield an empty list. [reason-cli workflow, CRITIC][cli].

**Check:** Does each delivered objection actually maintain a defeater at its end, and can the reader inspect the original retrace without the harness passing it off as the maintained objection?

### L4. Formalisation can spend the budget without commitment

**Fail mode:** Accepted definitions and setup steps can consume every cycle while leaving the decisive calculation or construction for later.

**Where it bit:** R002 A2 accepted three preliminary steps in three cases without synthesis; R003 o001 O07 planned eight steps for three cycles. [R002 REPORT][r2]; [R003 PLAN R3-A1][r3plan]; REC-20260917-A/B.

**Rule now:** R3-A1 requires an admitted plan of at most three steps, a decisive step within it, and a refutable commitment in every accepted step; definitions alone do not consume an accepted-step slot. [R003 PLAN judge supplement][r3plan].

**Check:** Which accepted step supplies the decisive claim, which later call uses it, and can that entire path run within the actual call and cycle envelope?

### L5. Same-lineage criticism is fallible, not independent proof

**Fail mode:** A same-lineage critic can reinforce a wrong answer or miss a local error even while satisfying its interface.

**Where it bit:** Archived R001 P02-SINGLE proposed the wrong count 38, adopted before use corrected it to 41; R002 C05 had a localized blind first-step window. R001 did not witness the broader shared-wrong-answer attractor. [R001 REPORT][r1]; [R002 REPORT][r2]; REC-20260916-F / REC-20260917-A.

**Rule now:** Declare actual lineages and available evidence; a blindness claim needs an exposed erroneous target and an available critic, and causal comparisons need matched conditions. [R002 PLAN][r2plan]; [reason-cli workflow, CRITIC][cli].

**Check:** Is independence established by lineage and information conditions, or merely by different seat names? Is the alleged missed error quoted from what that critic actually saw?

### L6. Seat failures must be counted by lineage and exposure

**Fail mode:** Pooling failed attempts, repaired logical calls and untested lineages can make an unreliable seat appear qualified.

**Where it bit:** GLM repeatedly length-stopped or returned non-JSON prose; Qwen had schema failures often recovered by repair; Kimi had no historical exposure when selected. [R003 PLAN R3-A1 census][r3plan]; [judge rounds 24 and 30][j24], [30][j30]; REC-20260917-A/B.

**Rule now:** Keep study, route, seat, mode, allowance, first attempt, repair and terminal logical outcome separate; zero exposure is `NOT FOUND`, not demonstrated reliability. The Kimi substitution is prospective, not a merit ranking. [R003 PLAN R3-A1 judge supplement][r3plan].

**Check:** What exact observed failure motivates this seat choice, under which envelope, and what evidence would show that the substituted seat still fails?

## Contracts

### L7. Envelope strictness must match the declared version

**Fail mode:** An overstrict envelope can reject a valid answer or a known resolved objection ID, while indiscriminate leniency can erase a real contract violation.

**Where it bit:** Smoke bare answers had valid JSON plus extra fields; eight R001 return attempts failed the historical known/open-ID contract. [judge rounds 12b and 15][j12b], [15][j15]; REC-20260916-D/F.

**Rule now:** Personal `public-working-v2` retains validated top-level extras and carries omitted resolved dispositions, but requires new/open IDs and validates every supplied ID; R002/R003 keep their own strict schemas. Never upgrade frozen runs on resume. [reason-cli workflow, RETURN and version policy][cli].

**Check:** Do saved outputs reproduce their original verdict under the original parser, and do the new version's positive and negative fixtures test the intended field and ID policy?

### L8. A repair needs its source and a bounded mandate

**Fail mode:** A stateless repair cannot reliably restore an exact quote when it receives only the faulty output, error and schema.

**Where it bit:** R003 o001 O03/O04 a00 had the source; a01 omitted it. Earlier workers also misread JSON-escaped source as absent. [R003 PLAN repair-context supplement][r3plan]; [R3-A1 erratum][a1err]; REC-20260917-B.

**Rule now:** R3-A1/A2 repairs include original rendered public context, prior output, precise failed check and schema, with the candidate target shown where required; only one same-seat repair is permitted. Preserve both attempts; do not solve afresh. [R003 PLAN R3-A1/R3-A2][r3plan].

**Check:** Can the repair copy the required target from its actual decoded request, and does that full request pass input preflight without truncating the prior response?

### L9. Prose locators need an explicit source field and grain

**Fail mode:** Whole-paragraph equality can reject a genuine excerpt, while a real sentence from the wrong field can look like a valid locator.

**Where it bit:** Six o002 DECOMPOSED critics failed locators; O01 CROSS quoted a claim rather than its indexed derivation, whereas O02 and O07 supplied genuine targeted excerpts. [R3-A2 erratum][a2err]; [judge round 32][j32]; REC-20260917-B.

**Rule now:** R3-A2 accepts a valid step index with empty quote, or a nonempty targeted substring of at least 40 characters after declared quote/whitespace/case normalization. Invalid nonempty text cannot fall back to index mode; lookup uses the declared step ID. [R003 PLAN R3-A2][r3plan].

**Check:** Do genuine excerpts and explicit indexes pass, while wrong-field text, fabricated quotes, invalid IDs and changed mathematical symbols fail?

### L10. Duplicate keys are not harmless redundancy

**Fail mode:** Ordinary JSON parsing can silently keep only the last of duplicate members, hiding an authored ambiguity or contradiction.

**Where it bit:** R003 o002 O01 USE repeated `result_depends_on_change`, with both values true; older embedded-program specimens also duplicated keys. [R3-A2 erratum][a2err]; [configuration errata CFG-004][cfgerr]; REC-20260917-B.

**Rule now:** R3-A2 rejects equal and conflicting duplicate keys; its repair identifies the key and demands one intended occurrence. [R003 PLAN, Locator custody][r3plan].

**Check:** Do fixtures reject both identical and conflicting duplicates at every nesting level, rather than relying on default `json.loads` acceptance?

### L11. The admitted plan must fit the runnable budget

**Fail mode:** A valid-looking plan can require more accepted steps than the run can execute.

**Where it bit:** R002 plans demanded six or seven steps under three cycles; R003 o001 O07 demanded eight. [R002 REPORT][r2]; [R003 PLAN R3-A1][r3plan]; REC-20260917-A/B.

**Rule now:** R3-A1 enforces `PLAN_FITS_BUDGET`, at most three steps, a decisive step and dependency-respecting order. Refuse or perform the declared repair before executing an impossible plan. [R003 PLAN, judge supplement][r3plan].

**Check:** After reserving criticism, repairs, returns and use, can every admitted dependency and decisive step actually finish within the declared resources?

### L12. A commitment needs a possible refuter

**Fail mode:** Definitions, intentions or vague promises can satisfy a prose field while committing to nothing that subsequent work can contradict.

**Where it bit:** R002 A2 stopped after formalisation; R3-A1 added a commitment requirement after o001. [R002 REPORT][r2]; [R003 PLAN R3-A1][r3plan]; REC-20260917-A/B.

**Rule now:** Each accepted R3 step ends with `COMMITMENT: <claim>`, matching its structured commitment and giving a value, relation or decision with a check or counterexample. The contract admits refutable prose and is not a correctness oracle. [R003 PLAN, commitment supplement][r3plan].

**Check:** What observable result would contradict this specific claim, where is that refuter carried, and is the claim more than a definition or postponed calculation?

### L13. Use must receive the derivation and refuter it needs

**Fail mode:** A downstream seat can be asked to depend on an accepted step while its actual request omits the relevant derivation or check.

**Where it bit:** R3-A2 review found `check_or_counterexample` missing from the rendered USE port; another critique demanded a future result from a current preliminary step. [R3-A2 erratum][a2err]; [judge round 32][j32]; REC-20260917-B.

**Rule now:** Carry the accepted claim, derivation, commitment and refuter through the actual USE request; assess the current step against its own goal and accepted dependencies. [R003 PLAN R3-A2][r3plan].

**Check:** Does a decoded saved USE request contain the exact accepted premise and its refuter, and can the requested derivation cite them without inventing unseen material?

### L14. A local return must repair its dependent suffix

**Fail mode:** A changed premise can be declared resolved while its dependent suffix still uses the old premise or leaves open objections undisposed.

**Where it bit:** Return disposition failures interrupted R001; R3-A2 deliberately retained full dependency and suffix obligations while relaxing locators. [R001 REPORT][r1]; [R3-A2 erratum][a2err]; REC-20260916-F / REC-20260917-B.

**Rule now:** A locator amendment does not relax dependency quotes, before/after custody, required dispositions or full affected-suffix rederivation. Apply the active RETURN contract rather than importing personal-CLI carry-forward into a frozen strict study. [R003 PLAN R3-A2][r3plan]; [reason-cli workflow, RETURN][cli].

**Check:** For each changed premise, which later steps must be rebuilt, and does every still-open objection receive the required supported disposition?

### L15. Prose bounds are part of the instrument

**Fail mode:** Oversized critic prose can prevent delivery of an otherwise meaningful objection, and increasing a field limit can merely move the failure to transport.

**Where it bit:** R001 critic-text bounds rejected self-confirmatory retraces; R3-A1 enlarged selected prose fields, while R002 full-output repairs exceeded the old input cap. [R001 REPORT][r1]; [R002 PLAN A2.2][r2plan]; [R003 PLAN R3-A1][r3plan]; REC-20260916-F / REC-20260917-A/B.

**Rule now:** Declare per-field bounds, working-text treatment and repair policy in the pinned schema; preflight the complete repair envelope, not just the nominal field limit. [reason-cli workflow][cli]; [R002 PLAN A2.2][r2plan].

**Check:** Can maximal allowed public fields, schema, context and previous output coexist in one repair request under this route's input limit?

### L16. A return/archive contrast needs the same concrete use task

**Fail mode:** Independently generated use questions can make returned and archived branches incomparable even when each looks locally valid.

**Where it bit:** R3-A3's initial EC-01 implementation allowed that divergence; judge round 36 required a frozen common question. [judge round 36][j36]; [R003 PLAN R3-A3][r3plan]; REC-20260917-B.

**Rule now:** Freeze the initial working position's concrete use task and query ID before return; both branches echo them, including inability. Archive removal is limited to the declared contiguous objection/signal block, with exact rendered and wire deletion evidence and preserved critic records. [R003 PLAN R3-A3][r3plan].

**Check:** Are the two use tasks byte-identical before either result exists, and does the branch diff show only the declared information intervention?

## Transport and hosts

### L17. A ceiling belongs to a particular exposure

**Fail mode:** Treating every numeric completion cap as the same usable public-answer budget hides reasoning consumption and route-specific accounting.

**Where it bit:** Native smoke-1 exhausted 8192 without an answer; gateway smoke-2 reported 8194 against an 8192 request and also returned no public answer. [docs/DECISION_LEDGER.md, REC-20260916-D][ledger]; [reason-cli workflow, transport settings][cli].

**Rule now:** Preserve requested cap, actual provider usage, reasoning-token metadata, finish reason, route and mode separately; use the configured exposure's ceiling and recovery policy. [reason-cli workflow][cli].

**Check:** What budget reaches public text on this exact route, and does the record retain the provider's actual accounting even when it exceeds the request?

### L18. Thinking controls do not transfer across gateways

**Fail mode:** A host can accept a setting that does not disable thinking on the selected provider route.

**Where it bit:** Gateway smoke testing did not establish `think:false` control through the OpenAI-compatible route. [docs/DECISION_LEDGER.md, REC-20260916-D][ledger]; [reason-cli workflow, reasoning modes][cli].

**Rule now:** Use native Ollama `/api/chat` for its supported `think:false`; the personal CLI refuses an explicitly unsupported gateway-off request instead of silently promising that control. DeepSeek mode mapping is separately declared. [reason-cli workflow][cli].

**Check:** Which request field does this endpoint actually honor, what probe established that fact, and will an unsupported explicit mode fail before dispatch?

### L19. JSON mode is a route setting, not a guarantee

**Fail mode:** Applying a JSON knob from a different API, or trusting it as schema enforcement, can still deliver prose or invalid envelopes.

**Where it bit:** R002 GLM completed in prose despite JSON mode; the workflow distinguishes native and OpenAI-compatible transport fields. [R002 PLAN A2.1][r2plan]; [reason-cli workflow][cli]; REC-20260917-A.

**Rule now:** Native `/api/chat` uses `format: "json"`; OpenAI-compatible routes use `response_format` with `json_object`. Parse and validate the returned public text under the seat contract regardless. [transport payload construction and native JSON mapping][transport].

**Check:** Does the saved wire contain the correct route-specific knob, and can the parser still expose rather than discard a normal-stop non-JSON response?

### L20. Preflight the actual material with the actual runner

**Fail mode:** An offline estimate or a different runner can pass while the intended launcher's real request or interface fails before dispatch.

**Where it bit:** R002 full-output C05/C06 repairs exceeded the 32k input cap even though smaller fixtures could run. [R002 PLAN A2.2][r2plan]; [judge round 24][j24]; REC-20260917-A.

**Rule now:** Use runner-native inspection on the complete declared material and run a no-transport compatibility check; an input refusal remains a pre-dispatch refusal, not a provider attempt. [reason-cli workflow, preflight][cli]; [R002 PLAN A2.2][r2plan].

**Check:** Can the exact launcher inspect its own maximal initial and repair requests, with all source, schema and prior output included, before any socket is opened?

### L21. The byte bound has explicit premises

**Fail mode:** A convenient input-token estimate can undercount the actual request or be advertised as a provider-independent proof.

**Where it bit:** R3-A1 replaced the inherited small input cap with declared model-window bounds; earlier qualification had used stale or unsuitable tokenizer assumptions. [R003 PLAN R3-A1][r3plan]; [judge round 20][j20]; REC-20260917-A/B.

**Rule now:** The adopted bound is wire UTF-8 bytes no greater than context window minus completion reserve minus template reserve, under the stated byte-token and rendering premises. Endpoint windows, reserves and empirical qualification remain separately identified; one endpoint's probe does not qualify others. [R003 PLAN, context-bound supplement][r3plan].

**Check:** What dated window and tokenizer/rendering evidence supports this exact route, and do the full serialized bytes fit after every reserve without unsupported attachments or tools?

### L22. Serialize once and preserve the bytes actually sent

**Fail mode:** Prepared-request hashes can disagree with transport hashes even when decoded messages and byte lengths agree.

**Where it bit:** R002's prepared and provider requests serialized message members in different orders; the report preserved the mismatch instead of calling it exact custody. Judge34 later caught the same class of fault in the pilot's actual child-worker path. [R002 REPORT, wire custody][r2]; [judge round 34][j34]; REC-20260917-A/D.

**Rule now:** Exact custody requires the canonical prepared bytes, preflight bytes and sent wire to match, with no independent reserialization. The later R3-A3 judge checked the actual provider wires against their prepared records. [judge round 36][j36]; [reason-cli workflow, wire records][cli].

**Check:** Does a fake-HTTP integration capture the exact transmitted body and prove byte/hash equality to the preflight and durable request, rather than only decoded-object equality?

### L23. The wall limit needs an independent supervisor

**Fail mode:** A timeout setting can fail to bound elapsed wall time if worker or host behavior escapes supervision.

**Where it bit:** Archived R001 Qwen evidence recorded an approximately seven-hour call despite the nominal 300-second wall; its cause was not established. [R001 REPORT, archived operational limits][r1]; REC-20260916-F.

**Rule now:** The R002 strict worker uses a 300-second per-attempt wall with a supervised Windows Job Object and kill-on-close behavior; record actual elapsed time, worker exit and any wall breach. A timeout is not a semantic judgment. [reason-cli workflow, wall supervision][cli].

**Check:** Does the qualified host kill a deliberately stuck child, persist the refusal without another send, and expose measured wall time rather than merely printing the configured limit?

### L24. A sleeping host requires recovery evidence

**Fail mode:** Host suspension or loss of supervision can leave a run's completion and timing uncertain, making a blind resume unsafe.

**Where it bit:** R001 preserves the unexplained wall overrun; the named records do not establish sleep as its cause. Treat sleep as a host risk to check, not a diagnosed explanation. [R001 REPORT][r1]; [Windows recovery guide][win]; REC-20260916-F.

**Rule now:** Recovery checks recorded intent, child/attempt state and immutable receipts before authorizing a successor; do not infer success from a missing process or replay an uncertain send. [continuation workflow][continue]; [reason-cli workflow, resume][cli].

**Check:** Is the host kept awake for the declared window, and after any sleep or interruption can the operator distinguish completed, refused and uncertain attempts without replaying one?

### L25. Temporary roots and test-work roots are different contracts

**Fail mode:** An unadmitted scratch path, or a test-work directory outside the required ignored checkout subtree, can make a required suite fail before exercising the intended code.

**Where it bit:** Judges repeatedly added their exact allowed scratch descendants; pilot judge round 34 still rejected required-suite qualification under incompatible temp/work settings. [judge rounds 24, 34 and 36][j24], [34][j34], [36][j36]; [W39 controlled environmental verdict][w39] identifies the rejecting static allowlist at experiments/diagnostics/R003-open-problems-trial-series/run_R003.py:112 and distinguishes the unset-TMP fixture error. REC-20260917-A/B/D.

**Rule now:** Respect each launcher's explicit root allowlist and its strict-descendant checks; distinguish `TMP`, `MINIREASON_TEST_WORK` and `MINIREASON_TEST_LAUNCHER_WORK`. An offline root exception does not admit arbitrary siblings. The later owner disposition registers the static allowlist as a defect and defers accepting the process TMP root until the live launcher finishes; this is a pending change, not an already relaxed guard. [reason-cli workflow][cli]; [judge round 34][j34]; [ledger/STATUS, REC-20260917-D, 10:49:49 UTC][ledger], [STATUS][status].

**Check:** Are all roots created, writable, short and actually admitted by the exact launcher, with repo-local test fixtures where required and escaped siblings refused?

### L26. MAX_PATH includes temporary atomic-write names

**Fail mode:** A final pathname can appear short enough while its atomic-write suffix crosses the Windows path limit.

**Where it bit:** Judge round 11 found 261-character legacy provider paths; even its shorter-prefix diagnostic failed on the longer atomic `.part` name. This remained a host qualification limit. [judge round 11][j11]; [docs/DECISION_LEDGER.md, REC-20260916-B][ledger].

**Rule now:** Qualify the deepest actual fixture and generated temporary name; shorten the authorized root rather than weakening the filesystem guard. [judge round 11][j11]; [Windows recovery guide][win].

**Check:** What is the longest resolved path after occurrence, arm, call, attempt and atomic suffix expansion, and does the actual write succeed under the intended host settings?

### L27. Launch syntax and encoding need their own qualification

**Fail mode:** Windows command length, nested quoting, interpreter assumptions or encoding conversion can prevent launch or corrupt authored bytes.

**Where it bit:** H005's roughly 700-line shell write failed with Windows error 206; recent reviews also preserved stripped-path quoting and missing-interpreter failures. [H005 erratum][h005]; [docs/DECISION_LEDGER.md, REC-20260914-B and REC-20260917-A/B][ledger].

**Rule now:** Use the verified interpreter, literal bounded chunks below the recorded 10000-character command limit, explicit UTF-8 and an inspected standalone launcher. Do not resend the same giant argument or claim an incomplete helper qualifies. [Windows recovery guide][win]; [H005 erratum][h005].

**Check:** Does the exact detached command parse and run an offline fixture with its real paths and environment, and do non-ASCII sentinel bytes survive without replacement characters?

### L28. Exit zero and COMPLETE do not mean an answer

**Fail mode:** A wrapper's successful exit or terminal label can be mistaken for successful reasoning.

**Where it bit:** Historical E026 exited zero with an interrupted result; R002 launch completion coexisted with censored or failed arms. [operations lessons][opsless]; [R002 REPORT][r2]; [ledger, REC-20260912-H and REC-20260917-A][ledger].

**Rule now:** Read terminal status, per-attempt finish reason, validation outcome and actual final public text; wrapper completion establishes that the launcher finished handling its scope. [operations lessons][opsless]; [reason-cli workflow, terminal outcomes][cli].

**Check:** Can the reporting path distinguish launcher completion, provider completion, contract acceptance and a delivered answer, including a zero-exit interrupted fixture?

### L29. Appending must preserve the original byte prefix

**Fail mode:** A text-mode rewrite can normalize CRLF or alter old ledger/report bytes while appearing to append a harmless paragraph.

**Where it bit:** Publication and review corrections repeatedly required exact original-prefix verification and explicit handling of CRLF-related whitespace findings. [operations errata][opserr]; [judge round 36][j36]; REC-20260917-B.

**Rule now:** Frozen observations are append-only or receive separate supplements; verify the original byte prefix after an append and preserve intentional newlines. W41 additionally requires Python UTF-8 `newline=''` writes. [operations lessons][opsless]; [W41 mandate and records][w41].

**Check:** Does a byte comparison prove that every pre-existing byte is unchanged, and is any whitespace exception narrow, explained and unrelated to content rewriting?

### L30. A test substitute cannot qualify filesystem durability

**Fail mode:** Replacing unsupported Windows directory durability with a file-only fixture can make functional tests look like live-host qualification.

**Where it bit:** The unchanged Forge directory-open operation failed before its fsync on Windows, surfaced as `MINI_BLOB_UNWRITABLE`; a diagnostic substitute exercised routing only. [docs/DECISION_LEDGER.md, REC-20260916-E][ledger]; [judge round 13][j13].

**Rule now:** Preserve the production durability requirement and refuse live operation before a socket when it is unavailable. Label the narrower fixture; do not suppress fsync or claim supported-host readiness. [docs/DECISION_LEDGER.md, REC-20260916-E][ledger]; [judge round 13][j13].

**Check:** Has the actual target filesystem passed the unchanged durability path, and can a simulated failure prove that no provider request follows it?

### L31. Resource and custody records need distinct categories

**Fail mode:** Missing usage, reasoning tokens, repairs, alias copies and refused preflights can be miscounted as comparable completed calls.

**Where it bit:** R002 initially labelled every repair attempt as successfully reached by repair; corrected reporting separated failures and retained both attempts' usage. [docs/DECISION_LEDGER.md, REC-20260917-A][ledger]; [judge round 24][j24].

**Rule now:** Keep logical calls, physical attempts, successful repairs, failed repairs and pre-dispatch refusals separate. Unknown usage stays unknown; reasoning-token metadata is part of completion accounting. Preserve public text and wire evidence, never credentials or hidden reasoning text. [reason-cli workflow, records and usage][cli].

**Check:** Can totals be reconstructed from unique actual attempts without counting archive copies twice, inventing missing usage or saving secret-bearing material?

## Process

### L32. An occurrence needs one declared change or an explicit exception

**Fail mode:** Bundling a new critic, allowance, schema and repair route can make a later result look like evidence for one isolated mechanism.

**Where it bit:** R002 A2 and R3-A1 changed several instrument conditions; the latter records the owner's explicit bundle exception. [R002 PLAN A2][r2plan]; [R003 PLAN R3-A1][r3plan]; REC-20260917-A/B.

**Rule now:** State the occurrence's before/after setting, reason, expected effect, possible loss and falsifier. Declare a permitted bundle and its causal limits; do not mutate configurations randomly or continue until a favorable result appears. [R003 PLAN, one-setting rule and R3-A1][r3plan]; [configuration lessons][cfgless].

**Check:** What exactly changes, which observed defect motivates it, and what result would defeat the proposed explanation under this design?

### L33. A post-dispatch amendment is not retrospective preregistration

**Fail mode:** A correction written after seeing results can be presented as though it governed the already dispatched occurrence.

**Where it bit:** R002 A2 was explicitly registered after occurrence-001 dispatch and applied only to separately identified occurrence-002. [R002 PLAN A2.2][r2plan]; [docs/DECISION_LEDGER.md, REC-20260917-A][ledger].

**Rule now:** Preserve the original plan and observation; append actual UTC, the deviation, evidence that motivated it and the first prospective occurrence to which it applies. [R002 PLAN A2][r2plan]; [method lessons][method].

**Check:** Was this rule written before the affected call, and if not, does the brief clearly label the amendment as post-dispatch and restrict its prospective use?

### L34. Freeze source while its launcher is alive

**Fail mode:** Editing runtime source during an active launcher can invalidate its source pins or make phases execute different code.

**Where it bit:** R002 integration exposed a source-change refusal while delegated edits were still arriving; the later owner decision expressly deferred the TMP-root fix because occurrence 4 was live. [docs/DECISION_LEDGER.md, REC-20260917-A and REC-20260917-D, 10:49:49 UTC][ledger].

**Rule now:** Freeze the reviewed source before launch and leave it unchanged until all workers and children finish. Source drift refuses resume and requires a new occurrence under the workflow's `new` path. [reason-cli workflow, numbered occurrences][cli].

**Check:** Who owns the freeze, how are live launcher and child processes checked, and will a proposed source edit wait or move to an explicitly separate successor?

### L35. Shared ledger appends must honor the active wait rule

**Fail mode:** Concurrent appenders can break another worker's frozen-prefix evidence or misattribute historical decision times as new actions.

**Where it bit:** Review34 recorded review31's live log without an exit marker and deferred shared writes; review36 later transferred engineer records first after exit markers appeared. [docs/DECISION_LEDGER.md, REC-20260917-D][ledger]; [judge round 36, REC-20260917-B][j36].

**Rule now:** Honor the current shared-file exclusion; stage local records while waiting, then append original engineer text before judge outcomes with actual transfer UTC. The recorded 60-second checks and 45-minute timeout were that task's bound, not permission to append through a still-live exclusion. [docs/DECISION_LEDGER.md, REC-20260917-D][ledger].

**Check:** Which workers own these shared paths now, what marks their release, and where will local receipts remain if the wait ends without clearance?

### L36. The publisher owns explicit paths and must stop on mismatch

**Fail mode:** A publication can accidentally absorb concurrent work or proceed with a path set different from the one reviewed.

**Where it bit:** The R3-A2 publisher stopped on unlisted pilot changes, then proceeded only after a scoped exclusion was established. [docs/DECISION_LEDGER.md, REC-20260917-B][ledger]; [operations lessons][opsless].

**Rule now:** One publisher stages only reviewed explicit paths, respects worker exclusions, stops on unexplained changes, divergence or rejected push, and verifies actual remote/local commit identities and equal trees. Current task-specific no-Git instructions supersede publication duties; no local receipt substitutes for a push. [repository operations skill][skill]; [operations lessons][opsless].

**Check:** Is each included path owned and reviewed, are exclusions explicit, and what exact remote-main/tree evidence will complete publication when publication is authorized?

### L37. A judge can remove an unnecessary gate, not an owner condition

**Fail mode:** Treating an incidental implementation requirement as mandatory can block valid work; treating judge discretion as unlimited can waive an explicit required test.

**Where it bit:** Judge round 20 replaced a hand-made calibration tokenizer-file prerequisite with an allowed exact-wire proof; judge round 34 could not waive the owner's all-tests-green condition at its judgment. A later explicit owner disposition accepted the approved-root suite evidence and resolved that hold, preserving the rejection. [judge rounds 20 and 34][j20], [34][j34]; [ledger, REC-20260917-D, 10:49:49 UTC][ledger]; REC-20260917-A/D.

**Rule now:** Judge the actual purpose and permitted alternatives of the contract. Retain required capability and input gates; replace needless preparation only with evidenced compliance, and leave an unwaived owner condition unsatisfied. [judge round 20, gate adjudication][j20]; [judge round 34][j34].

**Check:** Which exact authority requires this gate, does it allow an equivalent proof, and does the proposed removal preserve every owner-imposed condition?

### L38. Verification must exercise the final source and real invocation

**Fail mode:** Warm imports, stale assertions, broken discovery or an overbroad audit guard can obscure whether the final implementation was actually tested.

**Where it bit:** Judge round 11 separated stale receipt-count assertions from runtime replay; review24's guard both missed a forbidden subprocess and falsely blocked read-only Git; review34 fixed missing discovery and added actual child-worker HTTP doubles. [judge rounds 11, 24 and 34][j11], [24][j24], [34][j34]; REC-20260916-B / REC-20260917-A/D.

**Rule now:** Preserve failed transcripts, correct only the diagnosed layer, and rerun required checks on frozen current source using the exact entry point and cold import conditions where relevant. Offline integration must cross the actual adapter/worker boundary. [judge round 34][j34]; [Windows recovery guide][win].

**Check:** Do the recorded command, interpreter, environment, source hashes and collection count identify what ran, and does the negative guard test itself avoid the prohibited operation?

### L39. Substantive progress and publication have separate clocks

**Fail mode:** Activity noise or a local ledger append can conceal a missed substantive receipt or an unfinished push.

**Where it bit:** Operations records distinguish partial uploads, failed publication and missing verification; recent no-Git judges explicitly declined to claim publication cadence. [operations errata][opserr]; [judge round 36][j36]; REC-20260917-B.

**Rule now:** During authorized active publication work, maintain separate five-minute substantive and verified-publication deadlines, checkpoint before long uploads, and record misses truthfully. An unavailable reminder requires manual elapsed-time checks; task-specific publication prohibition remains in force. [repository operations skill][skill]; [operations lessons][opsless].

**Check:** What was the last newly appended substantive receipt, what was the last verified remote checkpoint, and does the current mandate permit publication at all?

### L40. Failed and interrupted evidence remains immutable

**Fail mode:** Reusing an output directory, rerunning uncertain intent or rewriting an old report can turn a correction into lost evidence.

**Where it bit:** R001 retains archived failures separately; R002/R003 amendments preserve earlier occurrences; interrupted judge diagnostics retain missing-buffer limits instead of reconstruction. [R001 REPORT][r1]; [R003 PLAN][r3plan]; [judge round 11][j11]; REC-20260916-B/F / REC-20260917-B.

**Rule now:** Resume skips both successful and failed terminal cells; changed source or a new question requires a separately identified successor. Preserve partial reports unchanged and publish a named completion/correction supplement when authorized. [reason-cli workflow, occurrences][cli]; [continuation workflow][continue].

**Check:** Will this operation overwrite any prior intent, attempt, report or preflight artifact, and is the proposed successor linked to its preserved parent with a new reason?

### L41. Pins and manifests must identify the actual delivered tree

**Fail mode:** Stale capability pins, a wrong manifest base or a directory-copy count can falsely certify or falsely reject the intended evidence.

**Where it bit:** R3-A3 review found stale/unreviewed capability candidates and incomplete nested critic archives; earlier publication receipts corrected manifest-base and copy-versus-authentication confusions. [judge round 36][j36]; [docs/DECISION_LEDGER.md, REC-20260915-B and REC-20260917-B][ledger].

**Rule now:** Resolve each manifest against its declared base, hash every required nested artifact, refresh reviewed runtime/source pins after permitted changes, and preserve final request/answer/checker/provider/settings identities. A copied summary is not complete evidence authentication. [judge round 36][j36]; [operations lessons][opsless].

**Check:** Can an independent reader reconstruct the exact judged inputs, code and outputs from the manifest, including nested attempts and any post-review drift?

## Reading

### L42. No scalar score can adjudicate explanatory construction

**Fail mode:** Endpoint tallies, schema passes or a progress meter can be substituted for reading what a criticism changed and what later work depended on.

**Where it bit:** R001's already-correct native answers and R002's delivery limits prevent a simple improvement claim; earlier lessons reject aggregation as adjudication. [R001 REPORT][r1]; [R002 REPORT][r2]; [method lessons][method]; REC-20260916-F / REC-20260917-A.

**Rule now:** Use the designated FW5 explanatory-construction reading edition and read quoted commitments, objections, returns and use with losses and live rivals. Harness v1.3 guides mechanism; ECS 2.0 additions remain separately identified hypotheses. [PURPOSE.md][purpose]; [semantic guide][semantic]; REC-20260915-A/C.

**Check:** Can the proposed reading explain the specific content-bearing change without ranking models, assigning an aggregate score or turning executable syntax into the definition of bearing?

### L43. Read the commitment and refuter, not the reassuring label

**Fail mode:** A parser-accepted commitment, an uncertainty paragraph or a declaration of dependence can be mistaken for substantive progress.

**Where it bit:** R003's accepted preliminary steps deferred decisive work; the R3-A1 judge explicitly limited commitment enforcement to declarations and custody. [R003 PLAN R3-A1][r3plan]; [judge round 30][j30]; REC-20260917-B.

**Rule now:** Quote the actual claim, its possible contradiction, the maintained objection and the subsequent derivation; leave their merit criticizable. A mislabeled definition can still fail the reading, and a valid prose conjecture need not be executable. [semantic guide][semantic]; [R003 PLAN, commitment supplement][r3plan].

**Check:** What claim became different, which reason bears on it, and which observable failure would defeat the reader's interpretation rather than merely fail formatting?

### L44. Not answered is never incorrect

**Fail mode:** Censoring, missing public text or a later critic failure can be counted as a wrong answer or erase an earlier completed answer.

**Where it bit:** R001 P08 and many R002 native calls hit ceilings; R002 C09 had an already completed initial answer before the later critic stopped. [R001 REPORT][r1]; [R002 REPORT][r2]; REC-20260916-F / REC-20260917-A.

**Rule now:** Keep no-answer, explicit inability, contract failure and an actually incorrect public claim separate. Preserve completed earlier stages and the absence of later evidence; never synthesize `cannot_decide` from empty text. [R002 PLAN][r2plan]; [R002 REPORT][r2].

**Check:** Is every correctness judgment attached to an actual quoted answer, with censored calls and completed-but-later-interrupted stages identified separately?

### L45. Readings are guarded artifacts with exposure histories

**Fail mode:** A reviewer can claim independence or blindness after seeing sealed material, or treat a digest seal as access isolation.

**Where it bit:** Review31 corrected reading attribution and exposure claims; review36 disclosed sealed-brief snippets printed by a delegated broad search and declined blindness. [judge round 31, REC-20260917-C][j31]; [judge round 36, REC-20260917-B][j36].

**Rule now:** Preserve reader identity, observed lineage, source edition, declared exposure and exact artifact custody. A corrected reading is a separately identified artifact; a hash seal does not prevent information exposure. Judge36 states: "This engineering review cannot claim zero brief exposure or a blind scientific reading." [judge rounds 31 and 36][j31], [36][j36].

**Check:** Who saw which briefs or outputs before judging, what supports the claimed lineage, and is every limitation visible in the reading handed to the next engineer?

### L46. Extra calls require matched controls for an advantage claim

**Fail mode:** A loop can look better than a one-call baseline because it received more calls, different information or an easier later task.

**Where it bit:** R001's P08 rescue and R003's local revisions lack a matched neutral multi-call contrast; EC-01 fixes paired use tasks but still cannot prove internal cause from one stochastic pair. [R001 REPORT][r1]; [R003 o003 REPORT][r3new]; [judge round 36][j36]; REC-20260916-F / REC-20260917-B.

**Rule now:** Declare bare, native and Mini information/resource conditions and matched multi-call controls before interpreting an extra-call advantage. Test actual active routes and rival explanations; equal endpoints do not prove non-use. [method lessons][method]; [R003 PLAN R3-A3][r3plan].

**Check:** What matched control separates the proposed mechanism from extra work or different information, and which quoted later-use difference would discriminate the live alternatives?

### L47. Inspect the actual stage before claiming absence or rejection

**Fail mode:** Raw substring searches, missing analyzer rows or final-only reading can hide supplied context, preserved prose or a commitment's actual stage.

**Where it bit:** R3-A1 workers mistook JSON-escaped source as absent; recent analyzer records distinguish unsupported instrument mappings from an absence of the relation. [R3-A1 erratum][a1err]; [docs/DECISION_LEDGER.md, REC-20260916-A and REC-20260917-B][ledger].

**Rule now:** Decode the actual request, identify the exact source field and stage, and distinguish `NOT FOUND` from an established absence. Keep rejected public prose available and identify instrument limits without silently repairing the observation. Judge35 corrected O06/O07 local exchanges to semantically complete through their public replies despite parser refusal; accepted propagation and later use remain absent. [interpretation errata][interpret]; [R3-A1 erratum][a1err]; [judge round 35, REC-20260917-B][j35].

**Check:** Was the disputed text searched in the decoded field the seat saw, and could the instrument's own admission or mapping rule explain a missing row?

### L48. A correction must preserve prior successes and expose losses

**Fail mode:** Crediting a helpful local revision can conceal a newly introduced error, a harmful critic or loss of a previously correct result.

**Where it bit:** Archived R001 criticism introduced the wrong count 38; judge35 confirms that R003 o003 O04 repairs a reserve omission introduced by the loop itself, with no established improvement over NATIVE. Possible losses remain distinct from demonstrated final comparative harm. [R001 REPORT][r1]; [R003 o003 REPORT][r3new]; [judge round 35][j35]; REC-20260916-F / REC-20260917-B.

**Rule now:** Compare the original and returned claims and downstream uses, retain protected successful cases, and quote actual losses. A rejected proposal is not automatically an adopted defect, and defeating one account does not establish its opposite. "All criticisms remain fallible, including operator review." [method lessons][method]; [semantic lessons][semless].

**Check:** What did this revision break, which earlier successes were rechecked, and are proposed, adopted, withdrawn and finally used claims distinguished?

## Pilot

### L49. Typed seat delivery does not establish whole-task reliability

**Fail mode:** Successful small JSON roles can be generalized into a claim that the same model reliably completes long tasks or an autonomous pilot.

**Where it bit:** The pilot census found typed seats more often deliver contract-accepted results than the difficult whole-task calls, while repairs and native ceilings remained; those populations had different tasks and envelopes. [pilot CAPABILITY][cap]; [judge round 34][j34]; REC-20260917-D.

**Rule now:** Report JSON delivery, first contract acceptance, repaired acceptance, explicit inability and substantive completion separately. The pilot conclusion is bounded possibility with probed features, not integrated reliability or a matched causal comparison. [pilot FEASIBILITY][feas]; [pilot PROBE-RESULTS][probe].

**Check:** Which exact typed roles have evidence, under what envelope, and what full-task or integrated execution remains untested despite their successful delivery?

### L50. Tool and routing probes qualify only their tested interface

**Fail mode:** A small successful tool probe can be treated as acceptance of a larger strict schema, arbitrary routing or a text adapter that discards tool calls.

**Where it bit:** Pilot normal/strict tool and routing probes exercised limited shapes; judge34 removed unsupported length keywords from the exported beta-strict manifest while retaining local bounds. [pilot PROBE-RESULTS][probe]; [judge round 34][j34]; REC-20260917-D.

**Rule now:** Separate provider-supported wire schema from full host validation; do not route tool calls through a normalizer that only retains text. Thinking-off probes avoid a hidden-reasoning replay dependency; free-form JSON-schema mode remains unqualified where untested. The current spawn packet must echo normalized inputs within 2048 output tokens, so large inputs can fail before a child runs. [pilot FEASIBILITY][feas]; [judge round 34][j34]; [pilot README, qualification limits][pilotreadme].

**Check:** Has this exact exported manifest and follow-up route been tested, which fields are host-only, and will hidden reasoning or dropped tool-call data be required to continue?

### L51. Spawn needs one global budget and a finite dependency graph

**Fail mode:** Locally bounded children can collectively exceed the parent's call allowance or recursively expand without a stopping condition.

**Where it bit:** The pilot spawn probe produced a graph shape, not executed children; feasibility therefore specifies bounded host scheduling rather than inferring working autonomy. [pilot PROBE-RESULTS][probe]; [pilot FEASIBILITY][feas]; REC-20260917-D.

**Rule now:** P-A1 permits up to 24 children per batch and depth 3 within each pass. One global positive logical-call ceiling defaults to 300, including control, worker and critic calls; the sole schema repair is a separately recorded physical attempt within its logical call and is charged to usage and spend. The estimated spend guard defaults to USD 6 per task. Both ceilings are owner-set guards, not targets; there is no fixed pass count. The previous default3/maximum8 fanout, depth2 and24physical-attempt limits remain historical. Preserve any external control-call reserve and dependency order. The built-in dispatcher is sequential; an external scheduler may have at most five active requests and must serialize stateful tools. These are pilot bounds, not new permission for live tests. [P-A1 before/after contract][pa1]; [pilot README, bounds][pilotreadme].

**Check:** Can every child and repair be charged to one remaining allowance, can cycles or duplicate task IDs be refused, and is deeper decomposition impossible at the depth boundary?

### L52. Validate an assembly before reserving or exposing it

**Fail mode:** A refused assembly can still become the visible final artifact if state is mutated before recorded-answer validation.

**Where it bit:** Judge34 reproduced an unrecorded answer resident after refusal; the corrected path validates before action reservation, then persists before exposing the candidate. [judge round 34, finding 3][j34]; REC-20260917-D.

**Rule now:** Assembly requires exact recorded-result references and answer equality before state mutation; rejection preserves state and action IDs. Proposal-only `engineer_patch` outputs do not establish that a patch was applied or tests ran. [judge round 34][j34]; [pilot README, bounds][pilotreadme].

**Check:** After a mismatched-answer or missing-reference refusal, can `finish()` expose the rejected text, and can a later valid action proceed without a consumed ID or fabricated test result?

### L53. Self-continuation is an explicit bounded host decision

**Fail mode:** A valid next-action packet can be mistaken for authority to retry, expand budgets, edit the harness or start an unregistered successor experiment.

**Where it bit:** Pilot evidence supports control-packet and routing probes, not demonstrated autonomous integrated reliability; R003 distinguishes a readable stopping condition from a censored occurrence. [pilot FEASIBILITY][feas]; [pilot PROBE-RESULTS][probe]; [R003 PLAN][r3plan]; REC-20260917-B/D.

**Rule now:** After verification, P-A1 records the pilot's `continue_or_stop` tool decision with exactly `decision`, `reason`, `what_changes_next` and `stop_rule`. The reason must cite the exact verification reference and explain its checker result, critic objections or unavailability; `continue` requires a changed template or subtask mix and why. Every decision receives verification and remaining calls/dollars. The first stop rule is preserved verbatim or tightened by appending ` OR ` and an additional earlier-stop condition; its substantive application remains fallible model judgment. An identical pass is refused before workers run, with at most two redecisions, then a recorded host stop. One schema repair is allowed; continuation cannot raise ceilings, self-modify or replay uncertain delivery. A new occurrence needs its own reason and authorization. Proposed episode kinds do not establish a stopping streak; censoring does not satisfy the R003 readable-occurrence stop rule. [P-A1 continuation contract][pa1]; [pilot README][pilotreadme]; [reason-cli workflow, occurrences][cli]; [judge round 35][j35].

**Check:** Who decides continue versus stop, which evidence and allowance permit the next action, and what concrete finding would justify reopening without calling a resource boundary exhaustion?

## Source handling

The [W41 source inventory][w41] records the required lesson/errata files, all named study reports and amendments, recent ledger and STATUS readings, workflow rules and judge reports. It distinguishes an absent optional pilot AMENDMENTS.md, the initially deferred REC-20260917-C association later imported into the shared ledger, and concurrently changed sources, including judge35's corrected o003 reading. Historical rules remain attached to their original editions and occurrences. The review38 correction separately reads the now-present P-A1 amendment and updates L51/L53 to its prospective contract; the earlier inventory's absent-file observation remains historical.

[a1err]: ../errata/REC-20260917-r3-a1-judge.md
[a2err]: ../errata/REC-20260917-r003-r3-a2.md
[cap]: ../../research/deepseek-flash-pilot/CAPABILITY.md
[cfgerr]: ../errata/configurations.md
[cfgless]: configuration.md
[cli]: ../workflows/reason-cli.md
[continue]: ../workflows/continue.md
[feas]: ../../research/deepseek-flash-pilot/FEASIBILITY.md
[h005]: ../errata/REC-20260914-h005-preflight.md
[interpret]: ../errata/interpretations.md
[j11]: ../../work/review11/REPORT.md
[j12b]: ../../work/review12b/REPORT.md
[j13]: ../../work/review13/REPORT.md
[j15]: ../../work/review15/REPORT.md
[j20]: ../../work/review20/REPORT.md
[j24]: ../../work/review24/REPORT.md
[j30]: ../../work/review30/REPORT.md
[j31]: ../../work/review31/REPORT.md
[j32]: ../../work/review32/REPORT.md
[j34]: ../../work/review34/REPORT.md
[j35]: ../../work/review35/REPORT.md
[j36]: ../../work/review36/REPORT.md
[ledger]: ../DECISION_LEDGER.md
[lessons]: README.md
[method]: method.md
[opserr]: ../errata/operations.md
[opsless]: operations.md
[pilotreadme]: ../../research/deepseek-flash-pilot/README.md
[probe]: ../../research/deepseek-flash-pilot/PROBE-RESULTS.md
[purpose]: ../../PURPOSE.md
[r1]: ../../experiments/diagnostics/R001-reason-cli-vs-baselines/REPORT.md
[r2]: ../../experiments/diagnostics/R002-episodes-under-calibrated-difficulty/REPORT.md
[r2plan]: ../../experiments/diagnostics/R002-episodes-under-calibrated-difficulty/PLAN.md
[r3new]: ../../experiments/diagnostics/R003-open-problems-trial-series/reports/o003-REPORT.md
[r3plan]: ../../experiments/diagnostics/R003-open-problems-trial-series/PLAN.md
[semantic]: ../SEMANTIC_GUIDE.md
[status]: ../STATUS.md
[semless]: semantics.md
[skill]: ../../skills/minireason-experiment-operations/SKILL.md
[pa1]: ../../research/deepseek-flash-pilot/AMENDMENTS.md
[transport]: ../../src/minireason/provider_openai_compat.py
[w39]: ../../work/w39/VERDICT.md
[w41]: ../../work/w41/INDEX.md
[win]: ../errata/REC-20260913-windows-execution.md

## CHECKLIST: before you build

A new configuration brief must answer each question with a path to its evidence, an explicit assumption or a named unresolved limit. This is a compact design checklist, not a scorecard.

- **Purpose and evidence:** Which FW5 claim or concrete engineering defect motivates the change, and what refuter could defeat it? (L32, L42-L43)
- **Seats:** Which exact lineages, exposures and observed failure modes justify each seat? Which substitutions lack evidence? (L1-L6)
- **Envelope:** Which version defines fields, extra keys, duplicate-key handling, bounds and final dispositions? (L7, L10, L14-L15)
- **Repair:** Does the sole permitted repair receive the real source, prior output and failed check, and fit without truncation? (L8-L9, L20)
- **Construction:** Can the whole plan, decisive commitment, dependencies and later use finish within the admitted allowance? (L11-L13)
- **Comparison:** Are paired use questions frozen before results, information differences explicit and extra-call controls matched? (L16, L46)
- **Transport:** Which route honors thinking and JSON controls, and what requested and actual limits are recorded? (L17-L19)
- **Input and custody:** What supports the window/reserve premises, and are prepared, preflight and transmitted bytes exactly equal? (L21-L22)
- **Host:** Are the 300-second supervisor, awake window, recovery procedure, admitted temp roots and longest atomic paths qualified? (L23-L26)
- **Launcher:** Does the exact interpreter/command preserve UTF-8 and original newline bytes, expose true terminal states and retain durability? (L27-L30)
- **Accounting:** Are calls, attempts, repairs, refusals, unknown usage and nested custody records separately reconstructible? (L31, L41)
- **Change control:** Is this amendment prospectively scoped or honestly post-dispatch, with live launchers frozen and shared-file waits honored? (L33-L35)
- **Publication:** Who owns each path, which workers are excluded, which gates are required, and what stops publication? Are its clocks separate? (L36-L39)
- **Preservation:** Do failures, partial reports and uncertain intents remain unchanged, with separately named successors and qualified final-source tests? (L38, L40)
- **Reading:** Are no-answer, wrong answer, missing visibility, reviewer exposure and harmful uptake distinguished with quotes and protected successes? (L44-L45, L47-L48)
- **Pilot:** Which typed/tool routes are actually qualified, and how do global budgets, finite spawn, validate-before-expose and explicit stopping constrain continuation? (L49-L53)


## Judge43 operational supplements - 2026-09-17 UTC

### L54. A judge's append wait must exclude its own active log

**Fail mode:** A literal any-log guard can make a judge wait for its own exit marker, which cannot exist until the judge returns.

**Where it bit:** Review45 polled 46 times at 60-second intervals for 2700.39 seconds; its own `review-45.log` was the only unmatched marker. Shared records were deferred despite completed verification. [Review45 records](../../work/review45/RECORDS.md), entries at 2026-09-17T12:58:56.930025+00:00 and 13:46:14.790630+00:00; REC-20260917-D/F.

**Rule now:** Identify the current invocation explicitly and exclude only its own log from the judge's docs-append guard. Keep every other matching review/publisher log subject to the required exit check, 60-second polling and 45-minute limit. Recheck immediately before shared appends; retain actual-UTC deferred records if another invocation remains active. Never treat elapsed time as approval.

**Check:** Does the pending set name another invocation, or only the judge that must finish before its own exit file can be written?

### L55. Scripted fixtures do not qualify a live delivery path

**Fail mode:** Passing offline scripts can miss the source, quote, schema and later-pass reference shapes a live model actually returns.

**Where it bit:** After 125 passing pilot tests, all four first live tasks stopped at host checks after 2-3 logical calls. Attempt 2 exposed a planner output ceiling and exact quotes with false authored offsets; attempt 3 exposed source/task namespace confusion, a non-admitted planner template, and assembly refusal of a meaningful partial child. The cost included three separately recorded repair amendments, not learned model improvement. Preserved records: `runs/pilot/UCn-attempt1-20260917T1356Z`, `UCn-attempt2-20260917T1424Z`, `UCn-attempt3-20260917T1502Z` (n=1..4); [P-A3 diagnosis](../../work/w46/DIAGNOSIS.md), [P-A4 diagnosis](../../work/w47/DIAGNOSIS.md), [P-A5 diagnosis](../../work/w48/DIAGNOSIS.md), [amendments](../../research/deepseek-flash-pilot/AMENDMENTS.md). REC-20260917-D/F.

**Rule now:** Before any authorized live rerun, replay the recorded live public bytes through the corrected host path, including repair, admission, accounting, assembly and continuation. Preserve originals and assert both the corrected outcome and refusal of nonresolving quotations or undeclared inputs. Add changed-return fixtures without relabeling earlier tests as live qualification. Successful replay covers those returns; unseen live behavior remains unqualified.

**Check:** Which exact failed request/response hashes traverse the real corrected path, and do negative custody cases still refuse before a successor dispatch?

### L56. A chain waiter must inspect run status before starting a reader

**Fail mode:** Waiting only for exit-file existence launches a reader on failed runs without checking what evidence the reading contract requires.

**Where it bit:** On 2026-09-17 the UC1-UC4 attempt-1 waiter started work43 after all exit files appeared; all four runs had failed at host checks. The reader was killed and its aborted log retained. The orchestrator state log records the exit-only chain at line 258 and this incident at line 261; line 263 adds a `result.json` status gate. [Exact-source spot-check and SHA-256](../../work/review43/ORCHESTRATOR-SPOTCHECK.txt). The later attempt-4 mandate explicitly permits reading failed/partial outcomes for what they reached (lines 267/269); that is a changed reading contract, not evidence that exit alone establishes completion. REC-20260917-D/F.

**Rule now:** After an exit marker, inspect the actual terminal `result.json` status and available artifact/decision records against the next reader's declared contract. A successful process exit is not whole-task completion; a readable partial can qualify when explicitly allowed. If failed outcomes are intentionally to be read, pass their true statuses and reached evidence to the reader. Otherwise stop the chain with its reason; do not start and then kill a reader based only on marker existence.

**Check:** What terminal status and evidence made this particular run eligible for this particular reading, and where is that eligibility decision recorded?
