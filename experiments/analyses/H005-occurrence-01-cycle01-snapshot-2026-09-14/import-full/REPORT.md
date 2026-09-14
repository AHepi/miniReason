# H005 -> spec-v1.3 import report

> **No label produced by this import is a semantic attribution.** Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).

- occurrence: `occurrence-01`
- plan_id: `21e3cf1dff73423785d2e6faab5d32971cd2295cb5ce7c5ca07bbd45eb2396a6`
- importer: `import_h005/1`
- scope: `daily/bare/cycle01/answer`, `daily/native/cycle01/answer`, `daily/matched/cycle01/account`, `daily/mini_prose/cycle01/account`, `daily/mini_fcl/cycle01/account`, `daily/matched/cycle01/objection`, `daily/mini_prose/cycle01/objection`, `daily/mini_fcl/cycle01/objection`, `daily/matched/cycle01/rival`, `daily/mini_prose/cycle01/rival`, `daily/matched/cycle01/response`, `daily/mini_prose/cycle01/response`, `daily/mini_fcl/cycle01/rival`, `daily/matched/cycle01/carry`, `daily/mini_prose/cycle01/carry`, `daily/mini_fcl/cycle01/response`, `daily/mini_fcl/cycle01/carry`
- events: 50 (`seq` 0..49), every `Event.llm` is null and every `ts` comes from the occurrence's `finished_utc`
- references: 82/84 resolved, 2 admitted by extension, 0 dangling

## What this is, and what it is not

The statuses below are **computed standing inside the imported attack relation**: the grounded extension of the attacks the authors themselves declared, then the support cascade over declared dependence. They are not a semantic verdict on any contribution, not a rubric judgement, and not an interpretation of the root problem. No provider was called, no `demonstrative` warrant was minted, and no transport status (`delivery_status`, `envelope_status`, `finish_reason`, `status`) was ever read as a verdict. An unattacked artifact is `accepted` **by position** - accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.

This scope contains 4 arms (bare, matched, mini_prose, native) whose declared commitment surface is prose and 1 arm (mini_fcl) whose surface is FCL-1. A prose commitment surface is never parsed, so no warrant, no attack edge and no refuted label can arise from a prose arm under this import. The distribution of statuses across arms is therefore a property of the carrier this importer reads, not a comparison between the arms. Any cross-arm reading is root's, not this instrument's.

**On the 2 artifact(s) with an empty commitments string.** The commitments string is empty because the study harness's strict JSON decode of the returned envelope failed and `decode_contribution` took its failure branch, storing the whole returned text as `body` and `""` as `commitments` (`commitments_sha256` is the sha256 of the empty string). Root's published review, `docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md`, measured that the same bytes parsed non-strictly do contain a commitments field: the commitments were authored and lost in decoding. The commitment surface is therefore **UNAVAILABLE, not absent**, and this is not evidence that the author declined to commit. This import does not repair it (I4): the artifact carries an empty Interface - no commitment surface, no refs - and the recorded envelope_status is metadata, never a verdict (I2).

## Custody

Every row says how many subjects the check actually ran over. A check that could not run over a coordinate - no receipt, no attempt, no request record, no provider call - is not a failure and not a verification; the coordinate is admitted with its absent inputs recorded in `side_table.json.artifacts[].absent_inputs`.

### Cross-file custody

Each of these compares two independently written files, so a coherent rewrite of any one of them is detected.

| check | result |
|---|---|
| plan.material_sha256 == sha256(material.json) | verified (1/1 occurrence) |
| plan.manifests[tid] == sha256(manifests/<tid>.json) | verified (3/3 manifests) |
| per node: receipt present (responses/<node>.json) | verified (17/17 nodes) |
| per node: sha256(artifacts/<node>.json) == receipt.artifact_sha256 | verified (17/17 nodes) |
| per node: receipt.status == delivery_status and receipt.envelope_status == envelope_status (recorded, never read as a verdict) | verified (17/17 nodes) |
| per node: sha256(responses/<node>.txt) == artifact.public_text_sha256 | verified (17/17 nodes) |
| per node: attempt.request_sha256 == receipt.request_sha256 | verified (17/17 nodes) |
| per node: study_digest(requests/<node>.json) == attempt.request_sha256 == receipt.request_sha256 | verified (17/17 nodes) |
| per node: request.trace_sha256 == study_digest(traces/<node>.json), checked before the trace is read by the label index or the projection resolver; counted as run only where the request record is itself pinned by an attempt or a receipt | verified (17/17 nodes) |
| per node: sha256(provider/<coord>/call-0001.{request,response}.json) == receipt.provider_{request,response}_sha256 (skipped only for a FAILED receipt) | verified (17/17 nodes) |
| per node: attempt.wave_id is the wave listing the coordinate and wave.request_hashes[<coordinate>] == attempt.request_sha256 | verified (17/17 nodes) |
| per projection: selected_source artifact_id/body_sha256/commitments_sha256 equal the authored artifact record it names | verified (16/20 projections; 4 projection(s) had no exposed source (the slot is absent): `daily/mini_prose/cycle01/account#p.account.0`, `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_prose/cycle01/carry#p.carry.3`, `daily/mini_fcl/cycle01/carry#p.carry.3`) |
| event ts nondecreasing | no - and that is a **declared deviation**, not a fault: a wave runs several arms concurrently and their `finished_utc` values interleave. Spec §14 requires contiguous `seq`, not ordered `ts`. Clamping would report a time that was never observed, so the import reports the fact instead. |
| files read and hashed | 147 |

### Internal consistency only

These compare a file against **itself**. They catch a truncated or incoherently edited file; they cannot detect a coherent rewrite, because nothing independent pins the value they check against.

| check | result |
|---|---|
| plan_id == study_digest(plan without plan_id) | verified (1/1 occurrence) |
| per node: sha256(body) == body_sha256, sha256(commitments) == commitments_sha256, and <field>_ref == <field>_sha256 | verified (17/17 nodes) |
| per node: the artifact record's own coordinate is the one it is filed under | verified (17/17 nodes) |
| per node: sha256(trace.original_brief) == trace.original_brief_sha256 | verified (17/17 nodes) |
| per node: every [label] line in the brief indexes the projection slot it names, and the brief's label set equals the projection set | verified (17/17 nodes) |
| per node: the exposed task label agrees with trace.task_artifact.artifact_id | verified (17/17 nodes) |

## Labels

This scope contains 4 arms (bare, matched, mini_prose, native) whose declared commitment surface is prose and 1 arm (mini_fcl) whose surface is FCL-1. A prose commitment surface is never parsed, so no warrant, no attack edge and no refuted label can arise from a prose arm under this import. The distribution of statuses across arms is therefore a property of the carrier this importer reads, not a comparison between the arms. Any cross-arm reading is root's, not this instrument's.

The **surface** column is the commitment surface this import actually read for that artifact: `read` (an FCL-1 document was parsed), `NOT READ (prose)` (the arm declared a prose surface, never parsed), `UNAVAILABLE (decode)` (the commitments string is empty because the study harness's strict decode failed), `PARSE FAILURE` / `SCHEMA FAILURE` (an FCL-surface arm's document did not parse or did not validate), or `n/a` for an artifact that has no commitment surface - a validity node or an FCL-1 document. A status computed over a surface that was not read carries no information about the contribution; read the two columns together.

| artifact | id | status | surface | attacked by | carries |
|---|---|---|---|---|---|
| `daily/bare/cycle01/answer` | `c6cc27cd626f2fcf` | **accepted** | NOT READ (prose) | - | - |
| `daily/matched/cycle01/account` | `bb87148326681638` | **accepted** | NOT READ (prose) | - | - |
| `daily/matched/cycle01/carry` | `a4d1754623c56c8f` | **accepted** | UNAVAILABLE (decode) | - | - |
| `daily/matched/cycle01/objection` | `979c35936ff44f59` | **accepted** | NOT READ (prose) | - | - |
| `daily/matched/cycle01/response` | `dda6acf1081f1fc6` | **accepted** | UNAVAILABLE (decode) | - | - |
| `daily/matched/cycle01/rival` | `a4f353fa0888a012` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_fcl/cycle01/account` | `90120224a7ce7660` | **refuted** | read | daily/mini_fcl/cycle01/objection | - |
| `daily/mini_fcl/cycle01/account#commitments` | `a13234a01db59feb` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/carry` | `a9b80c5cdc56a2f9` | **accepted** | read | - | 2 warrant(s) |
| `daily/mini_fcl/cycle01/carry#commitments` | `776688a01aabfb8f` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/objection` | `67f20387535530c7` | **accepted** | read | - | 3 warrant(s) |
| `daily/mini_fcl/cycle01/objection#commitments` | `fa4c2a11ecf6f937` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/response` | `94eed68f0fad96b9` | **refuted** | read | daily/mini_fcl/cycle01/carry | 2 warrant(s) |
| `daily/mini_fcl/cycle01/response#commitments` | `b712ef52043769e2` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/rival` | `d4a384457635115a` | **accepted** | read | daily/mini_fcl/cycle01/response | - |
| `daily/mini_fcl/cycle01/rival#commitments` | `8087bd6e456c72b1` | **accepted** | n/a | - | - |
| `daily/mini_prose/cycle01/account` | `0b140f6edfbd5d4f` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/carry` | `e52ca7ac0f37d853` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/objection` | `01d6ef98e1be9af6` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/response` | `8b7f7f36c868d327` | **accepted** | NOT READ (prose) | - | - |
| `daily/mini_prose/cycle01/rival` | `99081c259abef7e6` | **accepted** | NOT READ (prose) | - | - |
| `daily/native/cycle01/answer` | `590f73567b6c7c12` | **accepted** | NOT READ (prose) | - | - |
| `nu:carry#n3->nu(response#k7)` | `a989d1be80522bc5` | **accepted** | n/a | - | - |
| `nu:carry#n3->response` | `df544e2b09282aa9` | **accepted** | n/a | - | - |
| `nu:objection#o1->account` | `841dd44622ea4f56` | **accepted** | n/a | - | - |
| `nu:objection#o2->account` | `86da4b2b5d3e6d33` | **accepted** | n/a | - | - |
| `nu:objection#o3->account` | `602dad4d16dd4148` | **accepted** | n/a | - | - |
| `nu:response#k3->rival` | `5236edd5a7a4e425` | **accepted** | n/a | - | - |
| `nu:response#k7->rival` | `7453e8770fcea694` | **refuted** | n/a | daily/mini_fcl/cycle01/carry | - |

`|att|` = 4, `|dep|` = 0, warrants = 7, artifacts = 29.

### Attack edges

- `daily/mini_fcl/cycle01/objection` -> `daily/mini_fcl/cycle01/account`
- `daily/mini_fcl/cycle01/response` -> `daily/mini_fcl/cycle01/rival`
- `daily/mini_fcl/cycle01/carry` -> `nu:response#k7->rival`
- `daily/mini_fcl/cycle01/carry` -> `daily/mini_fcl/cycle01/response`

### Support edges (`dep`)

- **none.** All 17 `depends` refs in this scope were document-local, so at node granularity each would have been a `dep` self-loop - a cycle, which spec §1 forbids - and each was dropped and reported under `depends_intra_document`. That is a property of the node-granularity mapping, not a result about the occurrence. Pass 2 is a no-op and `suspended_unsupported` is unreachable in this scope.

## Warrants

| warrant | carrier | target | target kind | validity node |
|---|---|---|---|---|
| `w:h005.fcl1:daily/mini_fcl/cycle01/objection#o1->daily/mini_fcl/cycle01/account` | `daily/mini_fcl/cycle01/objection` | `daily/mini_fcl/cycle01/account` | artifact | `841dd44622ea4f56` |
| `w:h005.fcl1:daily/mini_fcl/cycle01/objection#o2->daily/mini_fcl/cycle01/account` | `daily/mini_fcl/cycle01/objection` | `daily/mini_fcl/cycle01/account` | artifact | `86da4b2b5d3e6d33` |
| `w:h005.fcl1:daily/mini_fcl/cycle01/objection#o3->daily/mini_fcl/cycle01/account` | `daily/mini_fcl/cycle01/objection` | `daily/mini_fcl/cycle01/account` | artifact | `602dad4d16dd4148` |
| `w:h005.fcl1:daily/mini_fcl/cycle01/response#k3->daily/mini_fcl/cycle01/rival` | `daily/mini_fcl/cycle01/response` | `daily/mini_fcl/cycle01/rival` | artifact | `5236edd5a7a4e425` |
| `w:h005.fcl1:daily/mini_fcl/cycle01/response#k7->daily/mini_fcl/cycle01/rival` | `daily/mini_fcl/cycle01/response` | `daily/mini_fcl/cycle01/rival` | artifact | `7453e8770fcea694` |
| `w:h005.fcl1:daily/mini_fcl/cycle01/carry#n3->nu(w:h005.fcl1:daily/mini_fcl/cycle01/response#k7->daily/mini_fcl/cycle01/rival)` | `daily/mini_fcl/cycle01/carry` | `nu(w:h005.fcl1:daily/mini_fcl/cycle01/response#k7->daily/mini_fcl/cycle01/rival)` | validity_node | `a989d1be80522bc5` |
| `w:h005.fcl1:daily/mini_fcl/cycle01/carry#n3->daily/mini_fcl/cycle01/response` | `daily/mini_fcl/cycle01/carry` | `daily/mini_fcl/cycle01/response` | artifact | `df544e2b09282aa9` |

Every warrant is `argumentative` with `commitment = null`, `verdict = null` and `trace_ref = null`: no kappa was run and a bare verdict is never an edge. A warrant whose target kind is `validity_node` is criticism of a criticism: spec §1 closure lifts it onto the attacked warrant and every carrier of it.

## Commitments and spawned problems

| commitment | observation-valued | eval | research problem |
|---|---|---|---|
| `k:h005.fcl1:daily/mini_fcl/cycle01/rival#r10` | true | `observation:h005.fcl1@29a4f93a16b842271b5e56...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/rival#r10` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/rival#r11` | true | `observation:h005.fcl1@1bb063f6b521da01dc91e7...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/rival#r11` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/response#k8` | true | `observation:h005.fcl1@56b568d7530d67ed2887d6...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/response#k8` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/carry#n8` | true | `observation:h005.fcl1@2b085c30d079801538ac35...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/carry#n8` |

An observation-valued commitment with no covering evidence is **scheduled-pending, never failed** (spec §12): it spawns a research problem instead of a verdict. The `eval` string is outside every executable class, so nothing can dispatch it.

## Residue

| code | severity | unit | count |
|---|---|---|---|
| `adjudication_batched` | informational | file | 1 |
| `bare_label_ref` | extension | ref | 1 |
| `claim_record_unmapped` | unmapped | record | 15 |
| `commitment_not_executable` | informational | record | 4 |
| `commitment_record_not_in_uptake` | informational | record | 2 |
| `consequence_on_non_commitment_record` | informational | record | 9 |
| `criticism_of_criticism_intra_document_dropped` | lossy | ref | 2 |
| `criticism_of_criticism_retargeted` | informational | edge | 1 |
| `dependence_cycle_rejected` | error | edge | 0 |
| `depends_cross_document` | informational | ref | 0 |
| `depends_intra_document` | lossy | ref | 17 |
| `grounds_absent_on_objection` | informational | record | 9 |
| `mentions_intra_document` | lossy | ref | 9 |
| `objection_self_target_only` | lossy | record | 1 |
| `objection_target_self_ref_dropped` | lossy | ref | 4 |
| `objection_untargeted` | lossy | record | 2 |
| `opaque_envelope` | informational | artifact | 2 |
| `parse_failure` | error | document | 0 |
| `problem_trigger_approximated` | lossy | problem | 5 |
| `problem_trigger_research_not_in_v13_enum` | informational | problem | 4 |
| `projection_absent` | informational | document | 4 |
| `projection_exposed_unreferenced` | informational | document | 10 |
| `prose_commitment_surface` | informational | artifact | 10 |
| `qualified_ref_body_pseudo_local` | extension | ref | 1 |
| `ref_through_absent_projection` | error | ref | 0 |
| `ref_through_unexposed_view` | error | ref | 0 |
| `ref_to_task_artifact` | informational | ref | 0 |
| `ref_to_unregistered_target_dropped` | error | ref | 0 |
| `ref_unresolved` | error | ref | 0 |
| `revises_unmapped` | unmapped | ref | 0 |
| `schema_failure` | error | document | 0 |
| `target_on_non_objection_record` | informational | record | 7 |
| `uptake_lists_unmapped` | unmapped | document | 5 |
| `uptake_refs_unmapped` | unmapped | ref | 32 |
| `use_record_unmapped` | unmapped | record | 9 |
| `validity_node_minted_unasserted` | informational | artifact | 7 |
| `warrant_edge_deduplicated` | informational | edge | 2 |
| `withdraws_unmapped` | unmapped | ref | 0 |

Counts follow the unit column: `ref` counts references, `record` counts FCL records, `document` counts FCL-1 documents or trace documents, `edge` counts attack or dependence edges, `artifact` counts artifacts, `problem` counts problems, `file` counts occurrence files. Full entries, each with the verbatim source text that was not mapped, are in `residue.json`.

**What this table does and does not claim.** Every FCL record in scope is accounted for at record granularity: each record is either mapped to a spec construct or reported under a residue code, and `side_table.json.records[]` shows which, per record, with the codes it raised. The same holds for every reference this import resolved. It is **not** a claim that every nuance inside a mapped record survived the mapping: a record that became a `Commitment` kept its text and lost its prose structure, and the codes above are the granularities the closed vocabulary names (`ref`, `record`, `document`, `edge`, `artifact`, `problem`, `file`), not a proof of semantic completeness.

## Declared deviations

- **`adjudication_batched`** (1 in this scope) - no separate terminal Adj event is emitted. spec §3 recomputes after every registration and the vendored P0 Harness does exactly that inside each registration event, but it exposes no public Adj emitter; the import writes through the registration API only and never forges a log line, so the terminal adjudication is the state after the last event.
- **`problem_trigger_approximated`** (5 in this scope) - imported FCL problem records use SpawnTrigger.SEED. the vendored enum has no 'import' member; 'seed' is the only trigger that does not assert an in-graph derivation. The clean fix is an enum addition, requested rather than papered over.
- **`problem_trigger_research_not_in_v13_enum`** (4 in this scope) - research problems use SpawnTrigger.RESEARCH with empty criteria. the vendored enum has the member and §12 is exactly this path, but the trigger is not part of the v1.3 enum text; criteria stay empty because no instantiated commitment id is a criterion.
- **`depends_intra_document`** (17 in this scope) - document-local depends refs are dropped, not turned into dep edges. at node granularity they would be dep self-loops, i.e. cycles; toposort rejects them and a self-loop asserts nothing the author declared.
- **`objection_self_target_only`** (1 in this scope) - a self-targeting objection mints no warrant. a Dung self-attack means 'this argument is self-defeating', which is not what an intra-document caveat asserts; minting it would flip two labels for reasons that have nothing to do with the evidence.
- **`criticism_of_criticism_retargeted`** (1 in this scope) - an objection against a record this import reified as a warrant attacks that warrant's validity node, not the node artifact. spec §1 closure: attackers of a validity node attack the warrant and every carrier of it, so criticism of a criticism keeps its force instead of collapsing into a plain edge onto the carrier.
- **`criticism_of_criticism_intra_document_dropped`** (2 in this scope) - the retargeting rule above has ONE exception: an objection against a criticism carried by the SAME artifact is not retargeted. the §1 closure lifts an attack on a validity node onto every carrier of the warrant, and for an intra-document criticism of a criticism that carrier is the objector itself, so retargeting would mint a self-attack through the closure and make the artifact self-defeating - which is not what an author asserts by qualifying their own earlier objection. `objection.o4` against `o1`/`o2` is exactly this case; it is dropped, not retargeted, and counted under its own code so the loss is visible rather than silent.
- **`claim_record_unmapped`** (15 in this scope) - an FCL `claim` record maps to no spec construct. a claim asserts content without proposing a test, so it is neither an observation-valued commitment nor a criticism nor a problem; it survives in the artifact body and in the FCL-1 document artifact, and is reported here because `uptake_refs_unmapped` covers only the claims the author put in `uptake`.

## How to read this report

1. **Labels** is the standing of each artifact inside the imported relation; read it together with the attack edges, never alone, and never as merit.
2. **`side_table.json`** maps every H005 coordinate to its spec id and back, names every validity node and FCL-1 document artifact, and records which FCL record produced which object. Nothing in it may be read by adjudication.
3. **`residue.json`** is the honest cost of the mapping: what the spec ontology could not carry, with verbatim source text and a counting unit per code.
4. **Why** below is the attack/defence chain behind each label.

## Why

```
why(c6cc27cd626f2fcfef9c009453bd865a3c73fd8cb15c33d21247965ff0c88d6a)
  artifact : daily/bare/cycle01/answer
  status   : accepted

  daily/bare/cycle01/answer [c6cc27cd626f] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(bb871483266816388d3044910650a2c7cf92dae46de04b7bf0e32aac1247e6cb)
  artifact : daily/matched/cycle01/account
  status   : accepted

  daily/matched/cycle01/account [bb8714832668] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(a4d1754623c56c8fa1fd64f76ab3d16e2e3f43b6d19d87a9c5440e15677b926e)
  artifact : daily/matched/cycle01/carry
  status   : accepted

  daily/matched/cycle01/carry [a4d1754623c5] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: UNAVAILABLE (unavailable_decode_failure). The authored commitments string is empty in the record because the study harness's strict JSON decode failed; root's review `docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md` measured that the returned bytes do contain commitments. This import read no commitment surface for this artifact, so it could mint no warrant from it and no warrant against it. The label above is silent about what the author committed to.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(979c35936ff44f59866c6f8428707709cfaba124ecca9fb3ad8f15ab2c75eeb0)
  artifact : daily/matched/cycle01/objection
  status   : accepted

  daily/matched/cycle01/objection [979c35936ff4] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(dda6acf1081f1fc61e907f5c4be7e570b908e1058fa9740928d4f8473db0afa5)
  artifact : daily/matched/cycle01/response
  status   : accepted

  daily/matched/cycle01/response [dda6acf1081f] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: UNAVAILABLE (unavailable_decode_failure). The authored commitments string is empty in the record because the study harness's strict JSON decode failed; root's review `docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md` measured that the returned bytes do contain commitments. This import read no commitment surface for this artifact, so it could mint no warrant from it and no warrant against it. The label above is silent about what the author committed to.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(a4f353fa0888a0124a238bb69b94031b328e0e31a150d24ad19ad531558a405b)
  artifact : daily/matched/cycle01/rival
  status   : accepted

  daily/matched/cycle01/rival [a4f353fa0888] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(90120224a7ce766080cfa556e6687c4da1ce554329a04ebff62a85f65ce1c2c4)
  artifact : daily/mini_fcl/cycle01/account
  status   : refuted

  daily/mini_fcl/cycle01/account [90120224a7ce] -- refuted
  <- attacked by daily/mini_fcl/cycle01/objection [67f203875355] -- accepted
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/objection#o1->daily/mini_fcl/cycle01/account
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/objection#o2->daily/mini_fcl/cycle01/account
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/objection#o3->daily/mini_fcl/cycle01/account
    (no attacker in the imported relation)

  refuted: attacked from the grounded extension by daily/mini_fcl/cycle01/objection [67f203875355], and nothing in the imported relation attacks that attacker.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(a13234a01db59feb62b1f430097ef431c4c8b17bd32f45397e1b2fd9f7fd1e15)
  artifact : daily/mini_fcl/cycle01/account#commitments
  status   : accepted

  daily/mini_fcl/cycle01/account#commitments [a13234a01db5] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(a9b80c5cdc56a2f90a3be6a2030929084d8188f5c3e56d94f8c40fb5f5abdaa9)
  artifact : daily/mini_fcl/cycle01/carry
  status   : accepted

  daily/mini_fcl/cycle01/carry [a9b80c5cdc56] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(776688a01aabfb8f9191e2ca1588f40eae729e020eb8bb973827f7000cd17520)
  artifact : daily/mini_fcl/cycle01/carry#commitments
  status   : accepted

  daily/mini_fcl/cycle01/carry#commitments [776688a01aab] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(67f20387535530c75d9ef834fc140a468d988097b300efd2bee93fbb8580f7b7)
  artifact : daily/mini_fcl/cycle01/objection
  status   : accepted

  daily/mini_fcl/cycle01/objection [67f203875355] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(fa4c2a11ecf6f9370d5435504a3dbf5472fe76d3727d5b9e8a49fa37defbd8b4)
  artifact : daily/mini_fcl/cycle01/objection#commitments
  status   : accepted

  daily/mini_fcl/cycle01/objection#commitments [fa4c2a11ecf6] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(94eed68f0fad96b9447ab817388501155294a1b60e5f081ca5ce604bb199db26)
  artifact : daily/mini_fcl/cycle01/response
  status   : refuted

  daily/mini_fcl/cycle01/response [94eed68f0fad] -- refuted
  <- attacked by daily/mini_fcl/cycle01/carry [a9b80c5cdc56] -- accepted
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/carry#n3->daily/mini_fcl/cycle01/response
    (no attacker in the imported relation)

  refuted: attacked from the grounded extension by daily/mini_fcl/cycle01/carry [a9b80c5cdc56], and nothing in the imported relation attacks that attacker.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(b712ef52043769e21e0919b7bd73327ea2b4333f4e668e48605c609f84f32314)
  artifact : daily/mini_fcl/cycle01/response#commitments
  status   : accepted

  daily/mini_fcl/cycle01/response#commitments [b712ef520437] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(d4a384457635115a605cfeeb43549f4c998a703560d1fcfe3d1901f5bd2dc605)
  artifact : daily/mini_fcl/cycle01/rival
  status   : accepted

  daily/mini_fcl/cycle01/rival [d4a384457635] -- accepted
  <- attacked by daily/mini_fcl/cycle01/response [94eed68f0fad] -- refuted
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/response#k3->daily/mini_fcl/cycle01/rival
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/response#k7->daily/mini_fcl/cycle01/rival
    <- attacked by daily/mini_fcl/cycle01/carry [a9b80c5cdc56] -- accepted
         via warrant w:h005.fcl1:daily/mini_fcl/cycle01/carry#n3->daily/mini_fcl/cycle01/response
      (no attacker in the imported relation)

  accepted by reinstatement (spec §4 pass 1, Lemma 3.1): every attacker is itself attacked from the grounded extension.
    reinstating attacker: daily/mini_fcl/cycle01/carry [a9b80c5cdc56]
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(8087bd6e456c72b1d31770f058e96f85399c0477dd3fbdc66efc8fde3271ce3e)
  artifact : daily/mini_fcl/cycle01/rival#commitments
  status   : accepted

  daily/mini_fcl/cycle01/rival#commitments [8087bd6e456c] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(0b140f6edfbd5d4fac47c1ea9b59fb3856ce633a518b2e7c2d66cdfab9db0294)
  artifact : daily/mini_prose/cycle01/account
  status   : accepted

  daily/mini_prose/cycle01/account [0b140f6edfbd] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(e52ca7ac0f37d853b28c3bb86f8c98f36dcd487d453c07ea4dacdb37b2879817)
  artifact : daily/mini_prose/cycle01/carry
  status   : accepted

  daily/mini_prose/cycle01/carry [e52ca7ac0f37] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(01d6ef98e1be9af6e6cefa9d46f3fe74db77c45b6b0378299df15ed0f2f8f7ae)
  artifact : daily/mini_prose/cycle01/objection
  status   : accepted

  daily/mini_prose/cycle01/objection [01d6ef98e1be] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(8b7f7f36c868d327817611616b4ada5bf045df82fed07345bf7961740b0842a1)
  artifact : daily/mini_prose/cycle01/response
  status   : accepted

  daily/mini_prose/cycle01/response [8b7f7f36c868] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(99081c259abef7e6d0acc3bc11c9ba5caa333e588d8aff1d7406959553aa356b)
  artifact : daily/mini_prose/cycle01/rival
  status   : accepted

  daily/mini_prose/cycle01/rival [99081c259abe] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(590f73567b6c7c1251717695556924abd633f081bec6b5cb0d9a7744e307d30d)
  artifact : daily/native/cycle01/answer
  status   : accepted

  daily/native/cycle01/answer [590f73567b6c] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  commitment surface: NOT READ (prose_not_parsed). This arm's declared commitment surface is prose; the author was never asked for FCL-1 and the string is never parsed as one. No warrant, no attack edge and no refuted label can arise from it under this import, so the label above is a property of the carrier, not of the contribution.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(a989d1be80522bc57e58439ee404d3323fb2b1af5f3268ab0064abb9d90f6f8b)
  artifact : nu:carry#n3->nu(response#k7)
  status   : accepted

  nu:carry#n3->nu(response#k7) [a989d1be8052] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(df544e2b09282aa91e329dde3de36ad371eba17288edd64d211558350153b5ef)
  artifact : nu:carry#n3->response
  status   : accepted

  nu:carry#n3->response [df544e2b0928] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(841dd44622ea4f56b09a46c80ee39a00fbb98d4ea94c8f596c08ef5301e2af77)
  artifact : nu:objection#o1->account
  status   : accepted

  nu:objection#o1->account [841dd44622ea] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(86da4b2b5d3e6d3357634152a57bb812a6a281aecf3b64a7088f111a55fccc51)
  artifact : nu:objection#o2->account
  status   : accepted

  nu:objection#o2->account [86da4b2b5d3e] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(602dad4d16dd414868929d61e6034e42716e6858766cd7a123cd911590dfa769)
  artifact : nu:objection#o3->account
  status   : accepted

  nu:objection#o3->account [602dad4d16dd] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(5236edd5a7a4e425723a35e7aafc795b75bedccc90d4c8bda5c7cb19c9038c0c)
  artifact : nu:response#k3->rival
  status   : accepted

  nu:response#k3->rival [5236edd5a7a4] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(7453e8770fcea694e86dd69872e988964850405a0f9c6229a8969ca61cafd422)
  artifact : nu:response#k7->rival
  status   : refuted

  nu:response#k7->rival [7453e8770fce] -- refuted
  <- attacked by daily/mini_fcl/cycle01/carry [a9b80c5cdc56] -- accepted
       via warrant w:h005.fcl1:daily/mini_fcl/cycle01/carry#n3->nu(w:h005.fcl1:daily/mini_fcl/cycle01/response#k7->daily/mini_fcl/cycle01/rival)
       (closure: attacking this validity node disables w:h005.fcl1:daily/mini_fcl/cycle01/response#k7->daily/mini_fcl/cycle01/rival and every carrier of it)
    (no attacker in the imported relation)

  refuted: attacked from the grounded extension by daily/mini_fcl/cycle01/carry [a9b80c5cdc56], and nothing in the imported relation attacks that attacker.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

