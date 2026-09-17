# Conditional router and plugin design

Verdict dependency: **POSSIBLE WITH PROBED FEATURES** in [FEASIBILITY](FEASIBILITY.md). This is an implementable proposal, not an installed plugin or evidence that Flash already pilots reliably. First qualify the prepared probes. A JSON-object action envelope is a possible fallback if function calls fail; routing and spawn competence still need their own evidence.

## Router data

Catalogue version `flash-pilot-v1`, immutable and content-hashed per run. Each row below becomes a registry object with `id`, `version`, `purpose`, `input_schema`, `output_schema`, `seats`, `ceilings`, `failure_rules`, `cost_envelope` and `evidence_refs`. The five IDs exactly match the probes. The router sees this data plus the task, allowed source references and host budget. It cannot invent a template, change a contract or declare a check passed.

All envelopes contain `status` (complete/partial/cannot_decide/failed), `answer`, `source_refs`, `unresolved` and `verification_refs`. References resolve to sealed immutable bytes. Empty lists/strings represent absent optional data; no omitted strict-tool properties. This is a new contract, not a retroactive replacement of historical schemas.

| ID / purpose | Required inputs and public output contract | Seats and completion caps; maximum attempts including one repair per seat | Known failure and bounded repair | Evidence / price bound |
|---|---|---|---|---|
| `direct_answer` / short self-contained answer | Task, premises, required answer shape; answer plus explicit uncertainty and source refs | One Flash answer, thinking off, 8192; at most 2 attempts | Wrong arithmetic despite valid JSON; check independently. One schema-only repair cannot establish correctness. Long derivations route elsewhere rather than silently raising caps. | R001 BARE/NATIVE and R003 conjecture; 2M |
| `evidence_read` / read supplied material and locate support | Task, sealed documents, requested claims; claim/source/locator/exact-quote tuples, contradictions and NOT FOUND fields | One Flash reader off, 8192; at most 2 attempts | Invented or altered quote, wrong source scope; host verifies each quoted span and ID. One repair gets the exact source and failing locator, preserving original. | R003 propagation-use quote failures; dedicated reader competence NOT FOUND; 2M |
| `engineer_patch` / propose a bounded change | Task, allowed files, source snapshots, behavior contract, test command allowlist; patch proposal, rationale and test claims linked to actual receipts | Flash proposer off8192, different-lineage critic off8192, Flash return off8192; at most 6 attempts | Unsupported test claim or unsafe scope; host rejects patch outside allowlist, applies only in isolated authorized workspace and runs fixed checks. Critic model does not execute code. | Reason CLI composition/checker mechanism only; live Flash repository engineering success NOT FOUND; Flash portion <=4M plus separately priced critic <=2 attempts |
| `critic_return` / challenge and revise a supplied candidate | Candidate, premises, stable objection IDs and protected obligations; objections with targets/grounds, disposition per open ID, revision and dependent use result | Two independently prompted critics of different available lineages from proposer, Flash return off8192 and Flash use off8192; at most 8 attempts | Empty valid list is not proof; unavailable critic is not empty. Reject unknown/duplicate IDs; quote source-bound targets; preserve rejected content. If only one critic available, label reduced independence. | R001 SINGLE/CROSS; R002 return/use; R003 return/use. Flash portion <=4M plus <=4 separately priced critic attempts |
| `decompose_synthesize` / dependencies exceed one bounded leaf | Task, decisive question, <=3 executable steps with dependencies and falsifiable result commitments; accepted step results, explicit dependencies, synthesis or partial record | Flash plan off4096, <=3 Flash steps off8192, one different-lineage critic off8192, Flash synthesis off8192; at most 12 attempts | Restatement instead of a result, decisive work outside budget, accepted local error, missing synthesis. Reject infeasible DAG before calls; source IDs replace fragile full-suffix recopying. Failed step prevents full synthesis. | R002 eight plans and R003 sixteen plans deliver, but zero synthesis in requested records; Flash portion <=10M plus <=2 critic attempts |

`M = (64000 * 0.30 + 8192 * 1.20)/1000000 = USD0.0290304`, a proposed Flash per-attempt upper estimate at documented peak cache-miss prices, with **host-verified <=64000 actual prompt tokens**. It is not an observed charge or an upper bound if input tokens are merely guessed. Require an exact tokenizer or a conservative certified bound and reserve known message overhead; otherwise the cost guarantee is NOT FOUND and the run refuses its price promise. Native leaves, if separately selected, reserve 32768 completion tokens: corresponding M is USD0.0585216, with exhaustion still possible. Other providers need their own current declared prices; this study did not consult them. Price source/read date: [API notes](API-NOTES.md), 2026-09-17.

Control calls reserve <=8192 prompt and 2048 completion tokens each (peak <=USD0.0049152 under the same exact-input condition). Pilot max 24 total dispatches across control, workers, critics and repairs; max depth 2, <=3 children per spawn, <=5 dependency-ready concurrent calls, one owner-chosen wall-time/spend budget. These are proposed operational limits, not reasons to declare inquiry exhausted. Larger catalogue envelopes may be refused when remaining global budget is insufficient. No automatic cap escalation, lineage substitution or template mutation.

## Routing rules

1. Missing task-critical information produces `cannot_decide` with the missing input. Exact source questions choose `evidence_read`; bounded code changes choose `engineer_patch`; an existing disputed candidate chooses `critic_return`; a short closed task chooses `direct_answer`.
2. Choose `decompose_synthesize` when the task has separable dependencies, substantial derivation, or a prior leaf hit a ceiling and a **new occurrence** is authorized. Require a decisive result within three steps and budget. Definitions alone do not count as completed steps. An infeasible plan returns partial/cannot_decide before dispatch.
3. Criticism of a candidate uses a different underlying model lineage when independence matters. Re-prompting Flash is explicitly same-lineage. The host resolves lineage metadata; a pilot's assertion of independence is insufficient. All-Flash operation can provide a labeled same-lineage check but cannot meet the different-lineage condition.
4. Separate syntax, domain correctness, custody and substantive judgment. Deterministic checks cover only their declared propositions. Prose criticism and uncertainty remain legitimate even when a machine contract rejects their delivery; preserve rejected text for reading.
5. Stop complete only after required dependencies and checks pass and unresolved contradictions are either resolved or visible in a partial status. Stop failed on malformed/unknown action, two schema failures, unavailable mandatory verifier, custody mismatch, or provider error. Stop partial on resource boundary or missing evidence. Do not turn a transport alarm or agreement vote into a content verdict.

## Minimum state machine and spawn protocol

`SEALED_TASK -> ROUTE_PROPOSED -> ROUTE_VALIDATED -> CHILDREN_PROPOSED -> DAG_VALIDATED -> DISPATCHED -> CHILD_RESULTS_VALIDATED -> ASSEMBLED -> VERIFIED -> COMPLETE/PARTIAL/FAILED`.

The host mints run, action, child and attempt IDs; the pilot only references them. A spawn request names template ID, bounded inputs and parent references, dependency IDs, contract ID and resource request. The host validates registry version, task relevance, dependencies, no cycles, no duplicate action, allowed information and remaining budget before accepting it. Child prompts expose only their declared problem/input packet; a critic receives its candidate and sources, not hidden reasoning or an unrelated critic's conclusion.

The host returns a tool-result envelope such as:

```json
{"action_id":"a003","status":"accepted","children":[{"child_id":"c01","template_id":"evidence_read","state":"queued","request_ref":"sha256:..."}],"errors":[]}
```

Completed children return immutable public `result_ref`, `contract_check_ref`, usage/latency and status. Unaccepted outputs remain addressable evidence but are never silently supplied as accepted premises. Return receives exact objection IDs plus the sealed target. Synthesis receives only accepted dependencies, with unresolved/partial items clearly segregated. A model cannot satisfy a missing dependency by writing that it succeeded. No arbitrary shell, filesystem or network access is exposed by spawn.

## DeepSeek-facing function interface

All four tools use `type:function`, a JSON Schema parameters object, every property required, and `additionalProperties:false` recursively. Beta strict mode is optional only after its probes pass. Until then JSON envelopes get the same local validator. Host checks list/string bounds because documented strict mode does not enforce these limits. Unknown tool/field/template/source/contract IDs fail closed. Every tool is idempotent on host `action_id` and returns a status/ref/error envelope.

| Tool | Required parameters and types | Host operation / custody |
|---|---|---|
| `choose_template` | `action_id:string`, `task_ref:string`, `template_id:enum` of the five IDs, `reason:string` | Validate task/ref/enum/budget; freeze catalogue, choice, reason and routing-validation receipt. Does not dispatch. |
| `spawn` | `action_id:string`, `parent_ref:string`, `children:array` of objects `{child_id:string, template_id:enum, input_refs:array[string], contract_id:string, depends_on:array[string], thinking:enum[off,native], max_completion_tokens:integer}` | Resolve exact inputs; validate DAG and mode/ceiling; mint request/attempt receipts before actual calls. Pilot-requested native mode cannot override control policy. |
| `assemble` | `action_id:string`, `task_ref:string`, `accepted_child_refs:array[string]`, `proposed_answer:string`, `conflicts:array[string]`, `status:enum[complete,partial,cannot_decide]` | Validate sources and prerequisite status, freeze assembly and dependency map. Assembly complete is only a proposal until verify. |
| `verify` | `action_id:string`, `artifact_ref:string`, `check_ids:array[string]`, `scope:string` | Resolve fixed checker allowlist and pinned checker source; run host checks only within preauthorized scope; write exact inputs, command identity, stdout/stderr or judgment, status, limitations and hashes. Returns verified/failed/unavailable, never invented evidence. |

Tool results use required `action_id`, `status`, `result_ref`, `errors` fields; errors are public structured codes. The host can include returned public content and bounded diagnostic context in a subsequent pilot turn. Use `thinking:disabled` for **every control conversation carrying tools**: the current docs require hidden-reasoning replay in thinking tool conversations, which conflicts with durable custody policy. Thinking-enabled workers are independent no-tools calls with only their public answers returned. Volatile hidden-reasoning replay with an unrecoverable session is not accepted as equal custody.

## Durable records and recovery

Before dispatch: append decision receipt, source/template/schema/checker hashes, provider/model/settings, exact UTF-8 wire body, body hash, parent result hashes, authorized budget and attempt marker. Write a single canonical wire byte sequence and send those same bytes; R002's historical prepared/sent member-order discrepancy must not recur. Credentials occur only in the authorization header and are never saved.

After response: preserve public content and tool-call IDs/arguments, response identity/returned model/fingerprint, raw-response digest only, reasoning-presence flag and numeric usage, finish reason, epoch and monotonic latency, transport status, contract validation and disposition. Do not save raw responses containing hidden reasoning. Missing usage remains unknown. Length-stopped prefixes remain partial; accepted role status is separate from semantic assessment.

Append progress/decision receipts in the task's authorized ledger. A designated publisher performs required publication and verifies remote commit and equal tree before dependent work under a publication-gated plan. The model cannot acknowledge its own publication. In this W33 preparation run Git is read-only and all such publication is pending; no production custody loop has been built.

On restart, inventory immutable intent/outcome markers and source hashes. An intent without a response is possibly spent, not free to replay. Refuse overwrite and automatic retry; a separately authorized attempt gets a new identity. Local repair is at most one new bounded call with the original invalid public output, exact failing check and requisite source context. Preserve both attempts and whether repair changed only formatting or the substance.

## What the probes settle

Twelve bounded calls can show interface viability for two-tool emission and voluntary stopping, beta strict arguments, five obvious routes, spawn shape, and one short thinking pair. They do not estimate production reliability, test adversarial prompt injection, validate long-context retrieval, prove useful critic independence, or demonstrate full engineering/synthesis. Promotion beyond preparation requires a separately approved integrated pilot fixture and held-out tasks with failure frequencies, matched resource controls, custody recovery and human-readable judgment of substantive results. No plugin is built in this run.

## Implemented scope after judge corrections - 2026-09-17T09:30:12.146291+00:00

The earlier sections are the W33 proposal, retained unchanged. The W34 MVP
and judge corrections are implemented in `src/minireason/pilot/`; the
[README](README.md) and checked-in `tools.json` define the current interface.
The external tool is named `route` (the proposal called it `choose_template`).
The outer spawn implements exactly one selected template with sealed inputs;
internal decomposition has at most three leaves and no further decomposition.
The host runs sequentially. The configurable fan-out has a hard maximum of
eight and depth is at most two. No tool grants shell or filesystem authority.

`engineer_patch` only proposes patches; it never applies them or executes its
test claims. Only JSON/schema failures receive one automatic repair. A bad
source quote is preserved and refused, not automatically repaired. The stronger
host schemas retain length bounds, while the beta strict wire schema omits the
unsupported length keywords. Full-manifest live acceptance is NOT FOUND.

Live pilot messages now freeze mapping order before preparation and dispatch,
so the existing reason worker's JSON persistence cannot change their actual
wire hashes. This prospective pilot correction leaves all historical records,
the reason package and provider modules unchanged. Qualification uses a
transport double and cannot establish live owner-task reliability.
