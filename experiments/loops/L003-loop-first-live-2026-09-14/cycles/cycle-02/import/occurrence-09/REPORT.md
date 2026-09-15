# H005 -> spec-v1.3 import report

> **No label produced by this import is a semantic attribution.** Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).

> **Error-severity residue fired in this import:** `ref_unresolved` (63), `schema_failure` (2). An `error` severity means a construct the mapping could not carry at all - a reference that resolved to nothing, a projection that exposed nothing, or a commitments string that claimed FCL-1 and did not parse. Read the Residue section and `residue.json` before reading any label below.

- occurrence: `occurrence-09`
- plan_id: `04c26f24812a4e48d41cfd6f6ef16785ba25ea183894bfafe86d6eb0e35af8ee`
- importer: `import_h005/1`
- scope: `daily/bare/cycle01/answer`, `daily/mini_fcl/cycle01/account`, `daily/mini_prose/cycle01/account`, `daily/mini_fcl/cycle01/objection`, `daily/mini_prose/cycle01/objection`, `daily/mini_fcl/cycle01/rival`, `daily/mini_prose/cycle01/rival`, `daily/mini_fcl/cycle01/response`, `daily/mini_prose/cycle01/response`, `daily/mini_fcl/cycle01/carry`, `daily/mini_prose/cycle01/carry`
- events: 32 (`seq` 0..31), every `Event.llm` is null and every `ts` comes from the occurrence's `finished_utc`
- references: 54/117 resolved, 0 admitted by extension, 63 dangling

## What this is, and what it is not

The statuses below are **computed standing inside the imported attack relation**: the grounded extension of the attacks the authors themselves declared, then the support cascade over declared dependence. They are not a semantic verdict on any contribution, not a rubric judgement, and not an interpretation of the root problem. No provider was called, no `demonstrative` warrant was minted, and no transport status (`delivery_status`, `envelope_status`, `finish_reason`, `status`) was ever read as a verdict. An unattacked artifact is `accepted` **by position** - accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.

This scope contains 2 arms (bare, mini_prose) whose declared commitment surface is prose and 1 arm (mini_fcl) whose surface is FCL-1. A prose commitment surface is never parsed, so no warrant, no attack edge and no refuted label can arise from a prose arm under this import. The distribution of statuses across arms is therefore a property of the carrier this importer reads, not a comparison between the arms. Any cross-arm reading is root's, not this instrument's.

## Custody

Every row says how many subjects the check actually ran over. A check that could not run over a coordinate - no receipt, no attempt, no request record, no provider call - is not a failure and not a verification; the coordinate is admitted with its absent inputs recorded in `side_table.json.artifacts[].absent_inputs`.

### Cross-file custody

Each of these compares two independently written files, so a coherent rewrite of any one of them is detected.

| check | result |
|---|---|
| plan.material_sha256 == sha256(material.json) | verified (1/1 occurrence) |
| plan.manifests[tid] == sha256(manifests/<tid>.json) | verified (3/3 manifests) |
| per node: receipt present (responses/<node>.json) | verified (11/11 nodes) |
| per node: sha256(artifacts/<node>.json) == receipt.artifact_sha256 | verified (11/11 nodes) |
| per node: receipt.status == delivery_status and receipt.envelope_status == envelope_status (recorded, never read as a verdict) | verified (11/11 nodes) |
| per node: sha256(responses/<node>.txt) == artifact.public_text_sha256 | verified (11/11 nodes) |
| per node: attempt.request_sha256 == receipt.request_sha256 | verified (11/11 nodes) |
| per node: study_digest(requests/<node>.json) == attempt.request_sha256 == receipt.request_sha256 | verified (11/11 nodes) |
| per node: request.trace_sha256 == study_digest(traces/<node>.json), checked before the trace is read by the label index or the projection resolver; counted as run only where the request record is itself pinned by an attempt or a receipt | verified (11/11 nodes) |
| per node: sha256(provider/<coord>/call-0001.{request,response}.json) == receipt.provider_{request,response}_sha256 (skipped only for a FAILED receipt) | verified (11/11 nodes) |
| per node: attempt.wave_id is the wave listing the coordinate and wave.request_hashes[<coordinate>] == attempt.request_sha256 | verified (11/11 nodes) |
| per projection: selected_source artifact_id/body_sha256/commitments_sha256 equal the authored artifact record it names | verified (16/20 projections; 4 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/account#p.account.0`, `daily/mini_fcl/cycle01/carry#p.carry.3`, `daily/mini_prose/cycle01/carry#p.carry.3`) |
| event ts nondecreasing | no - and that is a **declared deviation**, not a fault: a wave runs several arms concurrently and their `finished_utc` values interleave. Spec §14 requires contiguous `seq`, not ordered `ts`. Clamping would report a time that was never observed, so the import reports the fact instead. |
| files read and hashed | 97 |

### Internal consistency only

These compare a file against **itself**. They catch a truncated or incoherently edited file; they cannot detect a coherent rewrite, because nothing independent pins the value they check against.

| check | result |
|---|---|
| plan_id == study_digest(plan without plan_id) | verified (1/1 occurrence) |
| per node: sha256(body) == body_sha256, sha256(commitments) == commitments_sha256, and <field>_ref == <field>_sha256 | verified (11/11 nodes) |
| per node: the artifact record's own coordinate is the one it is filed under | verified (11/11 nodes) |
| per node: sha256(trace.original_brief) == trace.original_brief_sha256 | verified (11/11 nodes) |
| per node: every [label] line in the brief indexes the projection slot it names, and the brief's label set equals the projection set | verified (11/11 nodes) |
| per node: the exposed task label agrees with trace.task_artifact.artifact_id | verified (11/11 nodes) |

## Labels

This scope contains 2 arms (bare, mini_prose) whose declared commitment surface is prose and 1 arm (mini_fcl) whose surface is FCL-1. A prose commitment surface is never parsed, so no warrant, no attack edge and no refuted label can arise from a prose arm under this import. The distribution of statuses across arms is therefore a property of the carrier this importer reads, not a comparison between the arms. Any cross-arm reading is root's, not this instrument's.

The **surface** column is the commitment surface this import actually read for that artifact: `read` (an FCL-1 document was parsed), `NOT READ (prose)` (the arm declared a prose surface, never parsed), `UNAVAILABLE (decode)` (the commitments string is empty because the study harness's strict decode failed), `PARSE FAILURE` / `SCHEMA FAILURE` (an FCL-surface arm's document did not parse or did not validate), or `n/a` for an artifact that has no commitment surface - a validity node or an FCL-1 document. A status computed over a surface that was not read carries no information about the contribution; read the two columns together.

| artifact | id | status | surface | attacked by | carries |
|---|---|---|---|---|---|
| `daily/bare/cycle01/answer` | `ada1aa533bb6e8a5` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_fcl/cycle01/account` | `69a0bdc03022b058` | **accepted** | read | - | - |
| `daily/mini_fcl/cycle01/account#commitments` | `a97407d10075b584` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/carry` | `a0ef91bca4ac24e7` | **accepted** | read | - | - |
| `daily/mini_fcl/cycle01/carry#commitments` | `48857183188270ef` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/objection` | `63e83b7357bdd4ae` | **accepted** | read | - | - |
| `daily/mini_fcl/cycle01/objection#commitments` | `304e78ec2f46ad16` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/response` | `a878bf0083f35c7c` | **accepted** | SCHEMA FAILURE | - | - |
| `daily/mini_fcl/cycle01/rival` | `f77173f345277352` | **accepted** | SCHEMA FAILURE | - | - |
| `daily/mini_prose/cycle01/account` | `082b64a18aa061b1` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/carry` | `daa7e54a5f6dd331` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/objection` | `54acf9f0b3b66b52` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/response` | `e59f5ef3c5f9111f` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/rival` | `0d6930295e540b2e` | **accepted** | NOT READ (prose) | - | - |

`|att|` = 0, `|dep|` = 0, warrants = 0, artifacts = 14.

### Attack edges

- (none)

### Support edges (`dep`)

- **none.** All 3 `depends` refs in this scope were document-local, so at node granularity each would have been a `dep` self-loop - a cycle, which spec §1 forbids - and each was dropped and reported under `depends_intra_document`. That is a property of the node-granularity mapping, not a result about the occurrence. Pass 2 is a no-op and `suspended_unsupported` is unreachable in this scope.

## Warrants

| warrant | carrier | target | target kind | validity node |
|---|---|---|---|---|
| (none) | | | | |

Every warrant is `argumentative` with `commitment = null`, `verdict = null` and `trace_ref = null`: no kappa was run and a bare verdict is never an edge. A warrant whose target kind is `validity_node` is criticism of a criticism: spec §1 closure lifts it onto the attacked warrant and every carrier of it.

## Commitments and spawned problems

| commitment | observation-valued | eval | research problem |
|---|---|---|---|
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#a1` | true | `observation:h005.fcl1@7cde9fe54660b748efdca9...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#a1` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#a2` | true | `observation:h005.fcl1@de04dfb912ef01bc34380b...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#a2` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#a3` | true | `observation:h005.fcl1@4e18dc521488a40c09defa...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#a3` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#a4` | true | `observation:h005.fcl1@c0fe3010280ea933c46c41...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#a4` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#a5` | true | `observation:h005.fcl1@eaab540eb054a02f82cf06...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#a5` |

An observation-valued commitment with no covering evidence is **scheduled-pending, never failed** (spec §12): it spawns a research problem instead of a verdict. The `eval` string is outside every executable class, so nothing can dispatch it.

## Residue

| code | severity | unit | count |
|---|---|---|---|
| `adjudication_batched` | informational | file | 1 |
| `bare_label_ref` | extension | ref | 0 |
| `claim_record_unmapped` | unmapped | record | 10 |
| `commitment_not_executable` | informational | record | 5 |
| `commitment_record_not_in_uptake` | informational | record | 0 |
| `consequence_on_non_commitment_record` | informational | record | 0 |
| `criticism_of_criticism_intra_document_dropped` | lossy | ref | 0 |
| `criticism_of_criticism_retargeted` | informational | edge | 0 |
| `dependence_cycle_rejected` | error | edge | 0 |
| `depends_cross_document` | informational | ref | 0 |
| `depends_intra_document` | lossy | ref | 3 |
| `grounds_absent_on_objection` | informational | record | 6 |
| `mentions_intra_document` | lossy | ref | 20 |
| `objection_self_target_only` | lossy | record | 8 |
| `objection_target_self_ref_dropped` | lossy | ref | 1 |
| `objection_untargeted` | lossy | record | 0 |
| `opaque_envelope` | informational | artifact | 0 |
| `parse_failure` | error | document | 0 |
| `problem_trigger_approximated` | lossy | problem | 7 |
| `problem_trigger_research_not_in_v13_enum` | informational | problem | 5 |
| `projection_absent` | informational | document | 4 |
| `projection_exposed_unreferenced` | informational | document | 16 |
| `prose_commitment_surface` | informational | artifact | 6 |
| `qualified_ref_body_pseudo_local` | extension | ref | 0 |
| `ref_through_absent_projection` | error | ref | 0 |
| `ref_through_unexposed_view` | error | ref | 0 |
| `ref_to_task_artifact` | informational | ref | 0 |
| `ref_to_unregistered_target_dropped` | error | ref | 0 |
| `ref_unresolved` | error | ref | 63 |
| `revises_unmapped` | unmapped | ref | 2 |
| `schema_failure` | error | document | 2 |
| `target_on_non_objection_record` | informational | record | 3 |
| `uptake_lists_unmapped` | unmapped | document | 3 |
| `uptake_refs_unmapped` | unmapped | ref | 30 |
| `use_record_unmapped` | unmapped | record | 3 |
| `validity_node_minted_unasserted` | informational | artifact | 0 |
| `warrant_edge_deduplicated` | informational | edge | 0 |
| `withdraws_unmapped` | unmapped | ref | 0 |

Counts follow the unit column: `ref` counts references, `record` counts FCL records, `document` counts FCL-1 documents or trace documents, `edge` counts attack or dependence edges, `artifact` counts artifacts, `problem` counts problems, `file` counts occurrence files. Full entries, each with the verbatim source text that was not mapped, are in `residue.json`.

**What this table does and does not claim.** Every FCL record in scope is accounted for at record granularity: each record is either mapped to a spec construct or reported under a residue code, and `side_table.json.records[]` shows which, per record, with the codes it raised. The same holds for every reference this import resolved. It is **not** a claim that every nuance inside a mapped record survived the mapping: a record that became a `Commitment` kept its text and lost its prose structure, and the codes above are the granularities the closed vocabulary names (`ref`, `record`, `document`, `edge`, `artifact`, `problem`, `file`), not a proof of semantic completeness.

## Declared deviations

- **`adjudication_batched`** (1 in this scope) - no separate terminal Adj event is emitted. spec §3 recomputes after every registration and the vendored P0 Harness does exactly that inside each registration event, but it exposes no public Adj emitter; the import writes through the registration API only and never forges a log line, so the terminal adjudication is the state after the last event.
- **`problem_trigger_approximated`** (7 in this scope) - imported FCL problem records use SpawnTrigger.SEED. the vendored enum has no 'import' member; 'seed' is the only trigger that does not assert an in-graph derivation. The clean fix is an enum addition, requested rather than papered over.
- **`problem_trigger_research_not_in_v13_enum`** (5 in this scope) - research problems use SpawnTrigger.RESEARCH with empty criteria. the vendored enum has the member and §12 is exactly this path, but the trigger is not part of the v1.3 enum text; criteria stay empty because no instantiated commitment id is a criterion.
- **`depends_intra_document`** (3 in this scope) - document-local depends refs are dropped, not turned into dep edges. at node granularity they would be dep self-loops, i.e. cycles; toposort rejects them and a self-loop asserts nothing the author declared.
- **`objection_self_target_only`** (8 in this scope) - a self-targeting objection mints no warrant. a Dung self-attack means 'this argument is self-defeating', which is not what an intra-document caveat asserts; minting it would flip two labels for reasons that have nothing to do with the evidence.
- **`criticism_of_criticism_retargeted`** **(not triggered in this scope)** - an objection against a record this import reified as a warrant attacks that warrant's validity node, not the node artifact. spec §1 closure: attackers of a validity node attack the warrant and every carrier of it, so criticism of a criticism keeps its force instead of collapsing into a plain edge onto the carrier.
- **`criticism_of_criticism_intra_document_dropped`** **(not triggered in this scope)** - the retargeting rule above has ONE exception: an objection against a criticism carried by the SAME artifact is not retargeted. the §1 closure lifts an attack on a validity node onto every carrier of the warrant, and for an intra-document criticism of a criticism that carrier is the objector itself, so retargeting would mint a self-attack through the closure and make the artifact self-defeating - which is not what an author asserts by qualifying their own earlier objection. `objection.o4` against `o1`/`o2` is exactly this case; it is dropped, not retargeted, and counted under its own code so the loss is visible rather than silent.
- **`claim_record_unmapped`** (10 in this scope) - an FCL `claim` record maps to no spec construct. a claim asserts content without proposing a test, so it is neither an observation-valued commitment nor a criticism nor a problem; it survives in the artifact body and in the FCL-1 document artifact, and is reported here because `uptake_refs_unmapped` covers only the claims the author put in `uptake`.

## How to read this report

1. **Labels** is the standing of each artifact inside the imported relation; read it together with the attack edges, never alone, and never as merit.
2. **`side_table.json`** maps every H005 coordinate to its spec id and back, names every validity node and FCL-1 document artifact, and records which FCL record produced which object. Nothing in it may be read by adjudication.
3. **`residue.json`** is the honest cost of the mapping: what the spec ontology could not carry, with verbatim source text and a counting unit per code.
4. **Why** below is the attack/defence chain behind each label.

## Why

```
why(ada1aa533bb6e8a5cabaf76e24d327f020e4792ee5e0932d17c67a6f1c114e7a)
  artifact : daily/bare/cycle01/answer
  status   : accepted

  daily/bare/cycle01/answer [ada1aa533bb6] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(69a0bdc03022b058496fa56cd2a884b7c453ae2710cb99d3833fa60b5a443d6e)
  artifact : daily/mini_fcl/cycle01/account
  status   : accepted

  daily/mini_fcl/cycle01/account [69a0bdc03022] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(a97407d10075b5845bfc9de46dbb365079c4cc657ea8bca08c64a7f9b513fa12)
  artifact : daily/mini_fcl/cycle01/account#commitments
  status   : accepted

  daily/mini_fcl/cycle01/account#commitments [a97407d10075] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(a0ef91bca4ac24e7f7072ec046951641852cb9a6947bdb52f1814fc6b419f1fc)
  artifact : daily/mini_fcl/cycle01/carry
  status   : accepted

  daily/mini_fcl/cycle01/carry [a0ef91bca4ac] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(48857183188270efe8ede2ffc04c10f1881cc30b985f2cd21210c1b8109979b2)
  artifact : daily/mini_fcl/cycle01/carry#commitments
  status   : accepted

  daily/mini_fcl/cycle01/carry#commitments [488571831882] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(63e83b7357bdd4ae26ae7bfaa1df1a1ff2223d63c11823bc9340b509530af08f)
  artifact : daily/mini_fcl/cycle01/objection
  status   : accepted

  daily/mini_fcl/cycle01/objection [63e83b7357bd] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(304e78ec2f46ad16aa227e0b4758f5071f8c6c11c2560da9a6ea97752c429e0c)
  artifact : daily/mini_fcl/cycle01/objection#commitments
  status   : accepted

  daily/mini_fcl/cycle01/objection#commitments [304e78ec2f46] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(a878bf0083f35c7c0dd2908f6966fb95e9be9c1ef1d7aa1fa86cd6736916041e)
  artifact : daily/mini_fcl/cycle01/response
  status   : accepted

  daily/mini_fcl/cycle01/response [a878bf0083f3] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: UNAVAILABLE (schema_failure). The arm declares an FCL-1 surface and the document did not validate against fcl1.schema.json; nothing was repaired (I4), so no commitment surface was read and the label above is silent about what the author committed to.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(f77173f34527735260d5b8e8f52a5f80397f7bb192977c388a2a7d1e7c8f5c7a)
  artifact : daily/mini_fcl/cycle01/rival
  status   : accepted

  daily/mini_fcl/cycle01/rival [f77173f34527] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: UNAVAILABLE (schema_failure). The arm declares an FCL-1 surface and the document did not validate against fcl1.schema.json; nothing was repaired (I4), so no commitment surface was read and the label above is silent about what the author committed to.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(082b64a18aa061b14e6c5510d977175a7ac7a27a894022160bb4bb8687e07635)
  artifact : daily/mini_prose/cycle01/account
  status   : accepted

  daily/mini_prose/cycle01/account [082b64a18aa0] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(daa7e54a5f6dd3316f9c67411fd65fd9ce6ad5db42082d4b15d115fc5b7057cb)
  artifact : daily/mini_prose/cycle01/carry
  status   : accepted

  daily/mini_prose/cycle01/carry [daa7e54a5f6d] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(54acf9f0b3b66b525b1a14beb20c457d9cf1b92f71438de756639cdd386daceb)
  artifact : daily/mini_prose/cycle01/objection
  status   : accepted

  daily/mini_prose/cycle01/objection [54acf9f0b3b6] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(e59f5ef3c5f9111f323ccab8c9a3be5cb9938e749a6e75da421f905276c49a5e)
  artifact : daily/mini_prose/cycle01/response
  status   : accepted

  daily/mini_prose/cycle01/response [e59f5ef3c5f9] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(0d6930295e540b2e4b68d76eab69d0dc55b5c509f6c1d75a089d975c81f7dbdb)
  artifact : daily/mini_prose/cycle01/rival
  status   : accepted

  daily/mini_prose/cycle01/rival [0d6930295e54] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

