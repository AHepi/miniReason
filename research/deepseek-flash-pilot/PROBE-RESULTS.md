# DeepSeek Flash probe results

Read 2026-09-17 UTC from the 24 immutable request/response records under
`probes/records/` and the orchestrator launcher log. The launcher reports 12
HTTP calls, 12 assessments, and 12 passes. This report quotes only public
answer or tool-call fields. Native reasoning text was not persisted or read.

## Result

**POSSIBLE WITH PROBED FEATURES.** All 12 calls passed the local criteria
declared in `PROBE-PLAN.md`. Standard and beta-strict tool turns produced the
requested function calls and then stopped after fixed host results. The five
router tasks chose their obvious catalogue entries with coherent one-sentence
reasons. Spawn produced a valid three-node ordered DAG. Both thinking modes
returned the required answer below the 4,096-token ceiling.

These are interface qualification results from one purposive example per
behavior, not reliability estimates. They do not demonstrate real child
execution, engineering success, long-context reading, recovery, full
synthesis, independent criticism, substantive answer correctness beyond the
small fixtures, or an advantage over matched multi-call controls.

## Per-probe results

Usage is `prompt + completion = total` tokens. Quotes preserve the decisive
public response text or function name and argument string.

### 1. `tool-normal-initial`

- Criterion: exactly `choose_template` and `verify_contract`, distinct
  nonempty IDs, valid typed arguments, `tool_calls` finish, and no hidden
  reasoning field.
- Returned: `choose_template` with
  `{"task_id": "tool-fixture", "template_id": "evidence_read", "task_summary": "Read evidence from a.json for the tool-fixture task."}`;
  `verify_contract` with
  `{"candidate_id": "candidate-1", "valid": true, "issue": "none"}`.
- Result: **PASS**. Two valid calls, distinct IDs, finish reason `tool_calls`,
  reasoning absent. Latency 1,937 ms; usage `543 + 159 = 702`.

### 2. `tool-normal-followup`

- Criterion: nonempty public answer, `stop`, no further tool call, and no
  unexpected reasoning.
- Returned: "Both calls were accepted: the evidence_read template was selected for task tool-fixture, and candidate-1 was verified as valid with no issues."
- Result: **PASS**. Zero further tool calls, finish reason `stop`, reasoning
  absent. Latency 1,125 ms; usage `807 + 29 = 836`.

### 3. `tool-strict-initial`

- Criterion: beta strict mode emits exactly one valid `choose_template` call
  with no extra arguments, correct types and enum, a unique ID, `tool_calls`
  finish, and no hidden reasoning.
- Returned: `choose_template` with
  `{"task_id": "tool-fixture", "task_summary": "Inspect candidate-1 fixture and select the evidence_read template.", "template_id": "evidence_read"}`.
- Result: **PASS**. One valid call, finish reason `tool_calls`, reasoning
  absent. Latency 1,218 ms; usage `527 + 87 = 614`.

### 4. `tool-strict-followup`

- Criterion: the same voluntary-stop criterion as probe 2 after the fixed
  strict-tool result.
- Returned: "The evidence_read template was accepted for task tool-fixture with the given summary hash."
- Result: **PASS**. Zero further tool calls, finish reason `stop`, reasoning
  absent. Latency 812 ms; usage `704 + 17 = 721`.

### 5. `router-direct`

- Criterion: exact two-field JSON, `direct_answer`, a nonempty one-sentence
  reason, and `stop`.
- Returned: `{"template_id": "direct_answer", "justification": "The request is a simple arithmetic computation that can be answered directly without additional tools or decomposition."}`
- Result: **PASS**. The reason coherently identifies a closed arithmetic task.
  Latency 1,046 ms; usage `95 + 32 = 127`.

### 6. `router-evidence`

- Criterion: the same routing contract with expected ID `evidence_read`.
- Returned: `{"template_id": "evidence_read", "justification": "The task requires reading and citing multiple saved records to compare their token counts, which matches the evidence_read template."}`
- Result: **PASS**. The reason connects saved-record comparison and citation to
  evidence reading. Latency 1,358 ms; usage `100 + 36 = 136`.

### 7. `router-engineer`

- Criterion: the same routing contract with expected ID `engineer_patch`.
- Returned: `{"template_id": "engineer_patch", "justification": "The request requires modifying code, adding a test, and reporting changed paths, which matches the engineer_patch template."}`
- Result: **PASS**. The reason identifies the bounded code-and-test work. The
  probe did not execute a patch. Latency 907 ms; usage `102 + 39 = 141`.

### 8. `router-critic`

- Criterion: the same routing contract with expected ID `critic_return`.
- Returned: `{"template_id": "critic_return", "justification": "The task is to judge a proposed answer against a JSON contract and return one targeted repair request, which matches the critic_return template."}`
- Result: **PASS**. The reason identifies candidate judgment and repair.
  Latency 1,343 ms; usage `99 + 41 = 140`.

### 9. `router-decompose`

- Criterion: the same routing contract with expected ID
  `decompose_synthesize`.
- Returned: `{"template_id": "decompose_synthesize", "justification": "The task requires comparing two architectures through independent security, cost, and operability analyses before synthesizing, which matches the decompose-then-synthesize pattern."}`
- Result: **PASS**. The reason identifies independent analyses followed by
  synthesis. Latency 1,281 ms; usage `101 + 49 = 150`.

### 10. `spawn`

- Criterion: exact `subtasks` JSON; two to four uniquely named objects with
  valid IDs, allowlisted templates, nonempty inputs, only earlier dependency
  IDs, and `stop`.
- Returned: `s1` and `s2` are independent `evidence_read` tasks; `s3` is
  `decompose_synthesize` with `depends_on:["s1","s2"]` and input "Compare the evidence from runs A and B and synthesize a verdict on contract compliance".
- Result: **PASS**. Three unique valid subtasks form an ordered acyclic graph.
  No child was executed. Latency 1,360 ms; usage `195 + 115 = 310`.

### 11. `thinking-on`

- Criterion: exact integer JSON input 11, `stop` below 4,096 completion
  tokens, known numeric usage, and reasoning-presence true without persisting
  the reasoning text.
- Returned: `{"input":11}`.
- Result: **PASS**. Completion 45 tokens, including 39 reported reasoning
  tokens; reasoning present and not persisted. Latency 766 ms; usage
  `102 + 45 = 147`.

### 12. `thinking-off`

- Criterion: the same answer and below-ceiling stop with reasoning-presence
  false.
- Returned: `{"input":11}`.
- Result: **PASS**. Completion 5 tokens; reasoning absent. Latency 1,078 ms;
  usage `77 + 5 = 82`.

## Aggregate assessment

- **Tool-call validity:** both initial tool turns passed. The standard endpoint
  emitted both requested calls (2/2) and beta strict emitted its requested
  call (1/1). Both follow-ups voluntarily stopped after the fixed local tool
  results (2/2), with no additional call. The four tool-turn records all had
  the expected finish reason and no hidden-reasoning field.
- **Schema adherence:** all three emitted function calls satisfied the local
  argument schemas; the one beta call also used the documented `strict:true`
  feature. All eight JSON-object outputs (five routes, spawn, and the thinking
  pair) passed their exact local contracts. Free-response
  `response_format.type=json_schema` was deliberately not sent and remains
  **NOT TESTED**; those eight probes used `json_object` plus local validation.
- **Router choice quality:** 5/5 routes selected the expected catalogue
  template. Manual reading finds each one-sentence justification coherent
  with the decisive feature of its task; there was no router confusion in
  this set.
- **Spawn-list validity:** 1/1 spawn response passed with three children. Two
  independent evidence reads feed one synthesis node. This validates envelope
  and DAG shape only; it does not establish sufficiency, nonoverlap, or child
  correctness.
- **Thinking at 4,096:** both modes returned the same correct JSON and stopped
  below the ceiling. Native-high used 45 completion tokens, of which 39 were
  reported reasoning tokens, versus 5 completion tokens with thinking off.
  Native-high was 312 ms faster in this single pair (766 vs 1,078 ms), which
  is not enough evidence for a general latency comparison.

Across all probes, recorded latency totals 14,231 ms (median 1,171.5 ms,
range 766-1,937 ms). Reported usage totals 3,452 prompt, 654 completion, and
4,106 total tokens. All 12 request/response pairs agree on probe name,
request digest, and exact request-body digest; all were contacted, returned
HTTP 200, reported no credential echo, and persisted no hidden reasoning.

## Evidence identity

- `PROBE-PLAN.md`: 8,482 bytes; SHA256
  `4d28f89a607c461ceb3e421223c805d202b1a1d94dfe15b538a7f0ed154d3b3f`.
- `C:/Dev/minireason-launch/probes-1.log`: 222 bytes; SHA256
  `6979f835c3d6c468c066366f230da46439dedab9d77cbb15ec04c7fd2be56b7e`.
  Its complete public summary is 12 calls, 12 records, and 12 passing
  assessments.
- The SHA256 of all 24 record files concatenated in ordinal filename order is
  `270e494a9cc1f3d8048f1eb1efec3cc0851b5c1eaf17ff5bb63e324abd587f9f`.
  This is a reading-set fingerprint, not a replacement for each record's
  embedded request, wire-body, and provider-response digests.
