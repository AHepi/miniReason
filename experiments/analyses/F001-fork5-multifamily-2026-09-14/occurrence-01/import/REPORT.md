# H005 -> spec-v1.3 import report

> **No label produced by this import is a semantic attribution.** Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).

> **Error-severity residue fired in this import:** `ref_unresolved` (14). An `error` severity means a construct the mapping could not carry at all - a reference that resolved to nothing, a projection that exposed nothing, or a commitments string that claimed FCL-1 and did not parse. Read the Residue section and `residue.json` before reading any label below.

- occurrence: `occurrence-01`
- plan_id: `fd25a5a4ec8480b0aa9b29ba0d7ac771c16e32ce9d68709312b84c98296c3980`
- importer: `import_h005/1`
- scope: `daily/bare/cycle01/answer`, `daily/mini_fcl/cycle01/account`, `daily/mini_prose/cycle01/account`, `daily/native/cycle01/answer`, `daily/mini_fcl/cycle01/objection`, `daily/mini_prose/cycle01/objection`, `daily/mini_fcl/cycle01/rival`, `daily/mini_prose/cycle01/rival`, `daily/mini_fcl/cycle01/response`, `daily/mini_prose/cycle01/response`, `daily/mini_fcl/cycle01/carry`, `daily/mini_prose/cycle01/carry`
- events: 50 (`seq` 0..49), every `Event.llm` is null and every `ts` comes from the occurrence's `finished_utc`
- references: 66/80 resolved, 0 admitted by extension, 14 dangling

## What this is, and what it is not

The statuses below are **computed standing inside the imported attack relation**: the grounded extension of the attacks the authors themselves declared, then the support cascade over declared dependence. They are not a semantic verdict on any contribution, not a rubric judgement, and not an interpretation of the root problem. No provider was called, no `demonstrative` warrant was minted, and no transport status (`delivery_status`, `envelope_status`, `finish_reason`, `status`) was ever read as a verdict. An unattacked artifact is `accepted` **by position** - accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.

This scope contains 3 arms (bare, mini_prose, native) whose declared commitment surface is prose and 1 arm (mini_fcl) whose surface is FCL-1. A prose commitment surface is never parsed, so no warrant, no attack edge and no refuted label can arise from a prose arm under this import. The distribution of statuses across arms is therefore a property of the carrier this importer reads, not a comparison between the arms. Any cross-arm reading is root's, not this instrument's.

## Custody

Every row says how many subjects the check actually ran over. A check that could not run over a coordinate - no receipt, no attempt, no request record, no provider call - is not a failure and not a verification; the coordinate is admitted with its absent inputs recorded in `side_table.json.artifacts[].absent_inputs`.

### Cross-file custody

Each of these compares two independently written files, so a coherent rewrite of any one of them is detected.

| check | result |
|---|---|
| plan.material_sha256 == sha256(material.json) | verified (1/1 occurrence) |
| plan.manifests[tid] == sha256(manifests/<tid>.json) | verified (3/3 manifests) |
| per node: receipt present (responses/<node>.json) | verified (12/12 nodes) |
| per node: sha256(artifacts/<node>.json) == receipt.artifact_sha256 | verified (12/12 nodes) |
| per node: receipt.status == delivery_status and receipt.envelope_status == envelope_status (recorded, never read as a verdict) | verified (12/12 nodes) |
| per node: sha256(responses/<node>.txt) == artifact.public_text_sha256 | verified (12/12 nodes) |
| per node: attempt.request_sha256 == receipt.request_sha256 | verified (12/12 nodes) |
| per node: study_digest(requests/<node>.json) == attempt.request_sha256 == receipt.request_sha256 | verified (12/12 nodes) |
| per node: request.trace_sha256 == study_digest(traces/<node>.json), checked before the trace is read by the label index or the projection resolver; counted as run only where the request record is itself pinned by an attempt or a receipt | verified (12/12 nodes) |
| per node: sha256(provider/<coord>/call-0001.{request,response}.json) == receipt.provider_{request,response}_sha256 (skipped only for a FAILED receipt) | verified (12/12 nodes) |
| per node: attempt.wave_id is the wave listing the coordinate and wave.request_hashes[<coordinate>] == attempt.request_sha256 | verified (12/12 nodes) |
| per projection: selected_source artifact_id/body_sha256/commitments_sha256 equal the authored artifact record it names | verified (16/20 projections; 4 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/account#p.account.0`, `daily/mini_fcl/cycle01/carry#p.carry.3`, `daily/mini_prose/cycle01/carry#p.carry.3`) |
| event ts nondecreasing | no - and that is a **declared deviation**, not a fault: a wave runs several arms concurrently and their `finished_utc` values interleave. Spec §14 requires contiguous `seq`, not ordered `ts`. Clamping would report a time that was never observed, so the import reports the fact instead. |
| files read and hashed | 105 |

### Internal consistency only

These compare a file against **itself**. They catch a truncated or incoherently edited file; they cannot detect a coherent rewrite, because nothing independent pins the value they check against.

| check | result |
|---|---|
| plan_id == study_digest(plan without plan_id) | verified (1/1 occurrence) |
| per node: sha256(body) == body_sha256, sha256(commitments) == commitments_sha256, and <field>_ref == <field>_sha256 | verified (12/12 nodes) |
| per node: the artifact record's own coordinate is the one it is filed under | verified (12/12 nodes) |
| per node: sha256(trace.original_brief) == trace.original_brief_sha256 | verified (12/12 nodes) |
| per node: every [label] line in the brief indexes the projection slot it names, and the brief's label set equals the projection set | verified (12/12 nodes) |
| per node: the exposed task label agrees with trace.task_artifact.artifact_id | verified (12/12 nodes) |

## Labels

This scope contains 3 arms (bare, mini_prose, native) whose declared commitment surface is prose and 1 arm (mini_fcl) whose surface is FCL-1. A prose commitment surface is never parsed, so no warrant, no attack edge and no refuted label can arise from a prose arm under this import. The distribution of statuses across arms is therefore a property of the carrier this importer reads, not a comparison between the arms. Any cross-arm reading is root's, not this instrument's.

The **surface** column is the commitment surface this import actually read for that artifact: `read` (an FCL-1 document was parsed), `NOT READ (prose)` (the arm declared a prose surface, never parsed), `UNAVAILABLE (decode)` (the commitments string is empty because the study harness's strict decode failed), `PARSE FAILURE` / `SCHEMA FAILURE` (an FCL-surface arm's document did not parse or did not validate), or `n/a` for an artifact that has no commitment surface - a validity node or an FCL-1 document. A status computed over a surface that was not read carries no information about the contribution; read the two columns together.

| artifact | id | status | surface | attacked by | carries |
|---|---|---|---|---|---|
| `daily/bare/cycle01/answer` | `66fa5b797cd00768` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_fcl/cycle01/account` | `53d4458cddcd2ddb` | **refuted** | read | daily/mini_fcl/cycle01/objection, daily/mini_fcl/cycle01/carry | - |
| `daily/mini_fcl/cycle01/account#commitments` | `04b6e71aa08c7e70` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/carry` | `9ed5ea7bc65ecd03` | **accepted** | read | - | 2 warrant(s) |
| `daily/mini_fcl/cycle01/carry#commitments` | `b508c107e002ae9a` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/objection` | `35a8da948ad43229` | **accepted** | read | - | 3 warrant(s) |
| `daily/mini_fcl/cycle01/objection#commitments` | `60ffc7a7a8aaed74` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/response` | `13eec7daf378e695` | **refuted** | read | daily/mini_fcl/cycle01/carry | - |
| `daily/mini_fcl/cycle01/response#commitments` | `aa4cc9621edd0a39` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/rival` | `c3aac4584d130ae0` | **accepted** | read | - | - |
| `daily/mini_fcl/cycle01/rival#commitments` | `adf518ec679e8c2e` | **accepted** | n/a | - | - |
| `daily/mini_prose/cycle01/account` | `02a2b5f630f1315f` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/carry` | `6a91826d8fcdf253` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/objection` | `e41077802962ea24` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/response` | `b18ef4e19ca9e5d0` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/rival` | `e4445ca32a9094ed` | **accepted** | NOT READ (prose) | - | - |
| `daily/native/cycle01/answer` | `19edfcaf985abe4e` | **accepted** | NOT READ (prose) | - | - |
| `nu:carry#r5->response` | `4976435cc60cc962` | **accepted** | n/a | - | - |
| `nu:carry#r6->account` | `9238f227f062ca14` | **accepted** | n/a | - | - |
| `nu:objection#o1->account` | `b1e7221e032a8930` | **accepted** | n/a | - | - |
| `nu:objection#o2->account` | `d3894886d9c052b1` | **accepted** | n/a | - | - |
| `nu:objection#o3->account` | `b2ecbcf7d7f143c0` | **accepted** | n/a | - | - |

`|att|` = 3, `|dep|` = 0, warrants = 5, artifacts = 22.

### Attack edges

- `daily/mini_fcl/cycle01/objection` -> `daily/mini_fcl/cycle01/account`
- `daily/mini_fcl/cycle01/carry` -> `daily/mini_fcl/cycle01/response`
- `daily/mini_fcl/cycle01/carry` -> `daily/mini_fcl/cycle01/account`

### Support edges (`dep`)

- **none.** All 13 `depends` refs in this scope were document-local, so at node granularity each would have been a `dep` self-loop - a cycle, which spec §1 forbids - and each was dropped and reported under `depends_intra_document`. That is a property of the node-granularity mapping, not a result about the occurrence. Pass 2 is a no-op and `suspended_unsupported` is unreachable in this scope.

## Warrants

| warrant | carrier | target | target kind | validity node |
|---|---|---|---|---|
| `w:h005.fcl1:daily/mini_fcl/cycle01/objection#o1->daily/mini_fcl/cycle01/account` | `daily/mini_fcl/cycle01/objection` | `daily/mini_fcl/cycle01/account` | artifact | `b1e7221e032a8930` |
| `w:h005.fcl1:daily/mini_fcl/cycle01/objection#o2->daily/mini_fcl/cycle01/account` | `daily/mini_fcl/cycle01/objection` | `daily/mini_fcl/cycle01/account` | artifact | `d3894886d9c052b1` |
| `w:h005.fcl1:daily/mini_fcl/cycle01/objection#o3->daily/mini_fcl/cycle01/account` | `daily/mini_fcl/cycle01/objection` | `daily/mini_fcl/cycle01/account` | artifact | `b2ecbcf7d7f143c0` |
| `w:h005.fcl1:daily/mini_fcl/cycle01/carry#r5->daily/mini_fcl/cycle01/response` | `daily/mini_fcl/cycle01/carry` | `daily/mini_fcl/cycle01/response` | artifact | `4976435cc60cc962` |
| `w:h005.fcl1:daily/mini_fcl/cycle01/carry#r6->daily/mini_fcl/cycle01/account` | `daily/mini_fcl/cycle01/carry` | `daily/mini_fcl/cycle01/account` | artifact | `9238f227f062ca14` |

Every warrant is `argumentative` with `commitment = null`, `verdict = null` and `trace_ref = null`: no kappa was run and a bare verdict is never an edge. A warrant whose target kind is `validity_node` is criticism of a criticism: spec §1 closure lifts it onto the attacked warrant and every carrier of it.

## Commitments and spawned problems

| commitment | observation-valued | eval | research problem |
|---|---|---|---|
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#c3` | true | `observation:h005.fcl1@50a156e772efd8fc3763c9...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#c3` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#c4` | true | `observation:h005.fcl1@171eb65e48158c484abdb1...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#c4` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/rival#r4` | true | `observation:h005.fcl1@63c0ae1a6732478d6d04d1...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/rival#r4` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/response#m2` | true | `observation:h005.fcl1@0c59dd13db835d65569d0d...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/response#m2` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/response#m4` | true | `observation:h005.fcl1@2e610d38ca8f690c3b1fe7...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/response#m4` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/carry#r4` | true | `observation:h005.fcl1@608f9266d8dc2db48fdfe2...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/carry#r4` |

An observation-valued commitment with no covering evidence is **scheduled-pending, never failed** (spec §12): it spawns a research problem instead of a verdict. The `eval` string is outside every executable class, so nothing can dispatch it.

## Residue

| code | severity | unit | count |
|---|---|---|---|
| `adjudication_batched` | informational | file | 1 |
| `bare_label_ref` | extension | ref | 0 |
| `claim_record_unmapped` | unmapped | record | 11 |
| `commitment_not_executable` | informational | record | 6 |
| `commitment_record_not_in_uptake` | informational | record | 1 |
| `consequence_on_non_commitment_record` | informational | record | 1 |
| `criticism_of_criticism_intra_document_dropped` | lossy | ref | 0 |
| `criticism_of_criticism_retargeted` | informational | edge | 0 |
| `dependence_cycle_rejected` | error | edge | 0 |
| `depends_cross_document` | informational | ref | 0 |
| `depends_intra_document` | lossy | ref | 13 |
| `grounds_absent_on_objection` | informational | record | 8 |
| `mentions_intra_document` | lossy | ref | 1 |
| `objection_self_target_only` | lossy | record | 3 |
| `objection_target_self_ref_dropped` | lossy | ref | 3 |
| `objection_untargeted` | lossy | record | 0 |
| `opaque_envelope` | informational | artifact | 0 |
| `parse_failure` | error | document | 0 |
| `problem_trigger_approximated` | lossy | problem | 10 |
| `problem_trigger_research_not_in_v13_enum` | informational | problem | 6 |
| `projection_absent` | informational | document | 4 |
| `projection_exposed_unreferenced` | informational | document | 12 |
| `prose_commitment_surface` | informational | artifact | 7 |
| `qualified_ref_body_pseudo_local` | extension | ref | 0 |
| `ref_through_absent_projection` | error | ref | 0 |
| `ref_through_unexposed_view` | error | ref | 0 |
| `ref_to_task_artifact` | informational | ref | 0 |
| `ref_to_unregistered_target_dropped` | error | ref | 0 |
| `ref_unresolved` | error | ref | 14 |
| `revises_unmapped` | unmapped | ref | 0 |
| `schema_failure` | error | document | 0 |
| `target_on_non_objection_record` | informational | record | 2 |
| `uptake_lists_unmapped` | unmapped | document | 5 |
| `uptake_refs_unmapped` | unmapped | ref | 21 |
| `use_record_unmapped` | unmapped | record | 3 |
| `validity_node_minted_unasserted` | informational | artifact | 5 |
| `warrant_edge_deduplicated` | informational | edge | 1 |
| `withdraws_unmapped` | unmapped | ref | 0 |

Counts follow the unit column: `ref` counts references, `record` counts FCL records, `document` counts FCL-1 documents or trace documents, `edge` counts attack or dependence edges, `artifact` counts artifacts, `problem` counts problems, `file` counts occurrence files. Full entries, each with the verbatim source text that was not mapped, are in `residue.json`.

**What this table does and does not claim.** Every FCL record in scope is accounted for at record granularity: each record is either mapped to a spec construct or reported under a residue code, and `side_table.json.records[]` shows which, per record, with the codes it raised. The same holds for every reference this import resolved. It is **not** a claim that every nuance inside a mapped record survived the mapping: a record that became a `Commitment` kept its text and lost its prose structure, and the codes above are the granularities the closed vocabulary names (`ref`, `record`, `document`, `edge`, `artifact`, `problem`, `file`), not a proof of semantic completeness.

## Declared deviations

- **`adjudication_batched`** (1 in this scope) - no separate terminal Adj event is emitted. spec §3 recomputes after every registration and the vendored P0 Harness does exactly that inside each registration event, but it exposes no public Adj emitter; the import writes through the registration API only and never forges a log line, so the terminal adjudication is the state after the last event.
- **`problem_trigger_approximated`** (10 in this scope) - imported FCL problem records use SpawnTrigger.SEED. the vendored enum has no 'import' member; 'seed' is the only trigger that does not assert an in-graph derivation. The clean fix is an enum addition, requested rather than papered over.
- **`problem_trigger_research_not_in_v13_enum`** (6 in this scope) - research problems use SpawnTrigger.RESEARCH with empty criteria. the vendored enum has the member and §12 is exactly this path, but the trigger is not part of the v1.3 enum text; criteria stay empty because no instantiated commitment id is a criterion.
- **`depends_intra_document`** (13 in this scope) - document-local depends refs are dropped, not turned into dep edges. at node granularity they would be dep self-loops, i.e. cycles; toposort rejects them and a self-loop asserts nothing the author declared.
- **`objection_self_target_only`** (3 in this scope) - a self-targeting objection mints no warrant. a Dung self-attack means 'this argument is self-defeating', which is not what an intra-document caveat asserts; minting it would flip two labels for reasons that have nothing to do with the evidence.
- **`criticism_of_criticism_retargeted`** **(not triggered in this scope)** - an objection against a record this import reified as a warrant attacks that warrant's validity node, not the node artifact. spec §1 closure: attackers of a validity node attack the warrant and every carrier of it, so criticism of a criticism keeps its force instead of collapsing into a plain edge onto the carrier.
- **`criticism_of_criticism_intra_document_dropped`** **(not triggered in this scope)** - the retargeting rule above has ONE exception: an objection against a criticism carried by the SAME artifact is not retargeted. the §1 closure lifts an attack on a validity node onto every carrier of the warrant, and for an intra-document criticism of a criticism that carrier is the objector itself, so retargeting would mint a self-attack through the closure and make the artifact self-defeating - which is not what an author asserts by qualifying their own earlier objection. `objection.o4` against `o1`/`o2` is exactly this case; it is dropped, not retargeted, and counted under its own code so the loss is visible rather than silent.
- **`claim_record_unmapped`** (11 in this scope) - an FCL `claim` record maps to no spec construct. a claim asserts content without proposing a test, so it is neither an observation-valued commitment nor a criticism nor a problem; it survives in the artifact body and in the FCL-1 document artifact, and is reported here because `uptake_refs_unmapped` covers only the claims the author put in `uptake`.

## How to read this report

1. **Labels** is the standing of each artifact inside the imported relation; read it together with the attack edges, never alone, and never as merit.
2. **`side_table.json`** maps every H005 coordinate to its spec id and back, names every validity node and FCL-1 document artifact, and records which FCL record produced which object. Nothing in it may be read by adjudication.
3. **`residue.json`** is the honest cost of the mapping: what the spec ontology could not carry, with verbatim source text and a counting unit per code.
4. **Why** below is the attack/defence chain behind each label.

## Why

```
why(66fa5b797cd007682f4fac797c053028015f96f846f761b6c7282d3cb299ecab)
  artifact : daily/bare/cycle01/answer
  status   : accepted

  daily/bare/cycle01/answer [66fa5b797cd0] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(53d4458cddcd2ddbb4fef6b3616932a9431a01f8d96fbadc8a3dc8dbdf36c7d8)
  artifact : daily/mini_fcl/cycle01/account
  status   : refuted

  daily/mini_fcl/cycle01/account [53d4458cddcd] -- refuted
  <- attacked by daily/mini_fcl/cycle01/objection [35a8da948ad4] -- accepted
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/objection#o1->daily/mini_fcl/cycle01/account
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/objection#o2->daily/mini_fcl/cycle01/account
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/objection#o3->daily/mini_fcl/cycle01/account
    (no attacker in the imported relation)
  <- attacked by daily/mini_fcl/cycle01/carry [9ed5ea7bc65e] -- accepted
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/carry#r6->daily/mini_fcl/cycle01/account
    (no attacker in the imported relation)

  refuted: attacked from the grounded extension by daily/mini_fcl/cycle01/objection [35a8da948ad4], daily/mini_fcl/cycle01/carry [9ed5ea7bc65e], and nothing in the imported relation attacks that attacker.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(04b6e71aa08c7e7051de251882d2abc72c97b0c4588e2801ce3dd0586cd57d58)
  artifact : daily/mini_fcl/cycle01/account#commitments
  status   : accepted

  daily/mini_fcl/cycle01/account#commitments [04b6e71aa08c] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(9ed5ea7bc65ecd034904a68ceffee7480e14cecb5a928cdabe94c29caf70b1f6)
  artifact : daily/mini_fcl/cycle01/carry
  status   : accepted

  daily/mini_fcl/cycle01/carry [9ed5ea7bc65e] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(b508c107e002ae9ab62646c85156ea4b5f00d5b4856a18bab2698255324cdf64)
  artifact : daily/mini_fcl/cycle01/carry#commitments
  status   : accepted

  daily/mini_fcl/cycle01/carry#commitments [b508c107e002] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(35a8da948ad432291d14540cae4eb92ad5d348258631d8b09c40a5f4f31269d2)
  artifact : daily/mini_fcl/cycle01/objection
  status   : accepted

  daily/mini_fcl/cycle01/objection [35a8da948ad4] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(60ffc7a7a8aaed74633f3ba66911da97bb94aeb93f3b33a48f8e27adcae0de5d)
  artifact : daily/mini_fcl/cycle01/objection#commitments
  status   : accepted

  daily/mini_fcl/cycle01/objection#commitments [60ffc7a7a8aa] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(13eec7daf378e69581082b6df5b297e987710d0c665011d5de9291eac67c9c75)
  artifact : daily/mini_fcl/cycle01/response
  status   : refuted

  daily/mini_fcl/cycle01/response [13eec7daf378] -- refuted
  <- attacked by daily/mini_fcl/cycle01/carry [9ed5ea7bc65e] -- accepted
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/carry#r5->daily/mini_fcl/cycle01/response
    (no attacker in the imported relation)

  refuted: attacked from the grounded extension by daily/mini_fcl/cycle01/carry [9ed5ea7bc65e], and nothing in the imported relation attacks that attacker.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(aa4cc9621edd0a39ad6683a331ff2df8d38e39f34786b479bf7c2c8cf5ab7ed1)
  artifact : daily/mini_fcl/cycle01/response#commitments
  status   : accepted

  daily/mini_fcl/cycle01/response#commitments [aa4cc9621edd] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(c3aac4584d130ae001c4d6be18952aaa53300fd7fdbf2053323ed1a6a0b8e851)
  artifact : daily/mini_fcl/cycle01/rival
  status   : accepted

  daily/mini_fcl/cycle01/rival [c3aac4584d13] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(adf518ec679e8c2ebea8ccbdf79cdeef807b0e94fe0d506f8d1a124f5f799f4a)
  artifact : daily/mini_fcl/cycle01/rival#commitments
  status   : accepted

  daily/mini_fcl/cycle01/rival#commitments [adf518ec679e] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(02a2b5f630f1315fa34c82be05811c39783fae7e8ab9b4e5611b28c03e17622e)
  artifact : daily/mini_prose/cycle01/account
  status   : accepted

  daily/mini_prose/cycle01/account [02a2b5f630f1] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(6a91826d8fcdf25361ed349dfa78734bdf1415a0d0c22c94689463204f26d9d7)
  artifact : daily/mini_prose/cycle01/carry
  status   : accepted

  daily/mini_prose/cycle01/carry [6a91826d8fcd] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(e41077802962ea2468f073808ad16cb48ebde2ed89dbb62acb1a85711bb959cf)
  artifact : daily/mini_prose/cycle01/objection
  status   : accepted

  daily/mini_prose/cycle01/objection [e41077802962] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(b18ef4e19ca9e5d0dd29bbca389c69b49d1526c05ff645f70afbf046a931ea87)
  artifact : daily/mini_prose/cycle01/response
  status   : accepted

  daily/mini_prose/cycle01/response [b18ef4e19ca9] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(e4445ca32a9094edb5147cb74869d868ed52d41d1f4b25c6e107e026d45d5c7f)
  artifact : daily/mini_prose/cycle01/rival
  status   : accepted

  daily/mini_prose/cycle01/rival [e4445ca32a90] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(19edfcaf985abe4ed7874de12c4571e697c7c8946a1d3e92073e7e29350f8006)
  artifact : daily/native/cycle01/answer
  status   : accepted

  daily/native/cycle01/answer [19edfcaf985a] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(4976435cc60cc9625e1904c12edcfd1f473bccb40766be18d51bda0d494f83ad)
  artifact : nu:carry#r5->response
  status   : accepted

  nu:carry#r5->response [4976435cc60c] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(9238f227f062ca146ed9393ac54b28f18c4adb2143ef3a1dc553eaa14cafc71b)
  artifact : nu:carry#r6->account
  status   : accepted

  nu:carry#r6->account [9238f227f062] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(b1e7221e032a893049818064759810c0e5efe1ff3e4dff030d6170b68687c045)
  artifact : nu:objection#o1->account
  status   : accepted

  nu:objection#o1->account [b1e7221e032a] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(d3894886d9c052b1dc851fb41ff5823144902f953ceff6be73eb389d8dbcbda4)
  artifact : nu:objection#o2->account
  status   : accepted

  nu:objection#o2->account [d3894886d9c0] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(b2ecbcf7d7f143c0f85f4d403600b144ec305909b4be2da0f79cf098ea86362c)
  artifact : nu:objection#o3->account
  status   : accepted

  nu:objection#o3->account [b2ecbcf7d7f1] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

