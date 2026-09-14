# H005 -> spec-v1.3 import report

> **No label produced by this import is a semantic attribution.** Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).

> **Error-severity residue fired in this import:** `ref_unresolved` (153). An `error` severity means a construct the mapping could not carry at all - a reference that resolved to nothing, a projection that exposed nothing, or a commitments string that claimed FCL-1 and did not parse. Read the Residue section and `residue.json` before reading any label below.

- occurrence: `occurrence-02`
- plan_id: `a59debaf6382ce7c01c4c07d14894890736e2a960b66d4323f9eb84ac72b1163`
- importer: `import_h005/1`
- scope: `daily/mini_fcl/cycle01/account`, `daily/mini_fcl/cycle01/objection`, `daily/mini_fcl/cycle01/rival`, `daily/mini_fcl/cycle01/response`, `daily/mini_fcl/cycle01/carry`
- events: 41 (`seq` 0..40), every `Event.llm` is null and every `ts` comes from the occurrence's `finished_utc`
- references: 63/216 resolved, 0 admitted by extension, 153 dangling

## What this is, and what it is not

The statuses below are **computed standing inside the imported attack relation**: the grounded extension of the attacks the authors themselves declared, then the support cascade over declared dependence. They are not a semantic verdict on any contribution, not a rubric judgement, and not an interpretation of the root problem. No provider was called, no `demonstrative` warrant was minted, and no transport status (`delivery_status`, `envelope_status`, `finish_reason`, `status`) was ever read as a verdict. An unattacked artifact is `accepted` **by position** - accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.

## Custody

Every row says how many subjects the check actually ran over. A check that could not run over a coordinate - no receipt, no attempt, no request record, no provider call - is not a failure and not a verification; the coordinate is admitted with its absent inputs recorded in `side_table.json.artifacts[].absent_inputs`.

### Cross-file custody

Each of these compares two independently written files, so a coherent rewrite of any one of them is detected.

| check | result |
|---|---|
| plan.material_sha256 == sha256(material.json) | verified (1/1 occurrence) |
| plan.manifests[tid] == sha256(manifests/<tid>.json) | verified (3/3 manifests) |
| per node: receipt present (responses/<node>.json) | verified (5/5 nodes) |
| per node: sha256(artifacts/<node>.json) == receipt.artifact_sha256 | verified (5/5 nodes) |
| per node: receipt.status == delivery_status and receipt.envelope_status == envelope_status (recorded, never read as a verdict) | verified (5/5 nodes) |
| per node: sha256(responses/<node>.txt) == artifact.public_text_sha256 | verified (5/5 nodes) |
| per node: attempt.request_sha256 == receipt.request_sha256 | verified (5/5 nodes) |
| per node: study_digest(requests/<node>.json) == attempt.request_sha256 == receipt.request_sha256 | verified (5/5 nodes) |
| per node: request.trace_sha256 == study_digest(traces/<node>.json), checked before the trace is read by the label index or the projection resolver; counted as run only where the request record is itself pinned by an attempt or a receipt | verified (5/5 nodes) |
| per node: sha256(provider/<coord>/call-0001.{request,response}.json) == receipt.provider_{request,response}_sha256 (skipped only for a FAILED receipt) | verified (5/5 nodes) |
| per node: attempt.wave_id is the wave listing the coordinate and wave.request_hashes[<coordinate>] == attempt.request_sha256 | verified (5/5 nodes) |
| per projection: selected_source artifact_id/body_sha256/commitments_sha256 equal the authored artifact record it names | verified (8/10 projections; 2 projection(s) had no exposed source (the slot is absent): `daily/mini_fcl/cycle01/account#p.account.0`, `daily/mini_fcl/cycle01/carry#p.carry.3`) |
| event ts nondecreasing | no - and that is a **declared deviation**, not a fault: a wave runs several arms concurrently and their `finished_utc` values interleave. Spec §14 requires contiguous `seq`, not ordered `ts`. Clamping would report a time that was never observed, so the import reports the fact instead. |
| files read and hashed | 49 |

### Internal consistency only

These compare a file against **itself**. They catch a truncated or incoherently edited file; they cannot detect a coherent rewrite, because nothing independent pins the value they check against.

| check | result |
|---|---|
| plan_id == study_digest(plan without plan_id) | verified (1/1 occurrence) |
| per node: sha256(body) == body_sha256, sha256(commitments) == commitments_sha256, and <field>_ref == <field>_sha256 | verified (5/5 nodes) |
| per node: the artifact record's own coordinate is the one it is filed under | verified (5/5 nodes) |
| per node: sha256(trace.original_brief) == trace.original_brief_sha256 | verified (5/5 nodes) |
| per node: every [label] line in the brief indexes the projection slot it names, and the brief's label set equals the projection set | verified (5/5 nodes) |
| per node: the exposed task label agrees with trace.task_artifact.artifact_id | verified (5/5 nodes) |

## Labels

The **surface** column is the commitment surface this import actually read for that artifact: `read` (an FCL-1 document was parsed), `NOT READ (prose)` (the arm declared a prose surface, never parsed), `UNAVAILABLE (decode)` (the commitments string is empty because the study harness's strict decode failed), `PARSE FAILURE` / `SCHEMA FAILURE` (an FCL-surface arm's document did not parse or did not validate), or `n/a` for an artifact that has no commitment surface - a validity node or an FCL-1 document. A status computed over a surface that was not read carries no information about the contribution; read the two columns together.

| artifact | id | status | surface | attacked by | carries |
|---|---|---|---|---|---|
| `daily/mini_fcl/cycle01/account` | `93d07e37f88e7da4` | **accepted** | read | - | - |
| `daily/mini_fcl/cycle01/account#commitments` | `a607a7e41503c361` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/carry` | `db2a2adfc9f419ca` | **accepted** | read | - | - |
| `daily/mini_fcl/cycle01/carry#commitments` | `5bd8ebc5cd5b204a` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/objection` | `983099fb06b575eb` | **accepted** | read | - | - |
| `daily/mini_fcl/cycle01/objection#commitments` | `d7d8d1e0c56509f2` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/response` | `7771193a8a9a90af` | **accepted** | read | - | - |
| `daily/mini_fcl/cycle01/response#commitments` | `5a24f84a15791961` | **accepted** | n/a | - | - |
| `daily/mini_fcl/cycle01/rival` | `f5ad66e26fa0cf22` | **accepted** | read | - | - |
| `daily/mini_fcl/cycle01/rival#commitments` | `086989040489592e` | **accepted** | n/a | - | - |

`|att|` = 0, `|dep|` = 0, warrants = 0, artifacts = 10.

### Attack edges

- (none)

### Support edges (`dep`)

- **none.** All 14 `depends` refs in this scope were document-local, so at node granularity each would have been a `dep` self-loop - a cycle, which spec §1 forbids - and each was dropped and reported under `depends_intra_document`. That is a property of the node-granularity mapping, not a result about the occurrence. Pass 2 is a no-op and `suspended_unsupported` is unreachable in this scope.

## Warrants

| warrant | carrier | target | target kind | validity node |
|---|---|---|---|---|
| (none) | | | | |

Every warrant is `argumentative` with `commitment = null`, `verdict = null` and `trace_ref = null`: no kappa was run and a bare verdict is never an edge. A warrant whose target kind is `validity_node` is criticism of a criticism: spec §1 closure lifts it onto the attacked warrant and every carrier of it.

## Commitments and spawned problems

| commitment | observation-valued | eval | research problem |
|---|---|---|---|
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#cm1` | true | `observation:h005.fcl1@78a0a7d4fabae7c5967efb...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#cm1` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#cm2` | true | `observation:h005.fcl1@1162fc7fd683c189330aea...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#cm2` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#cm3` | true | `observation:h005.fcl1@239913e90ec1e4ec192c42...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#cm3` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/account#cm4` | true | `observation:h005.fcl1@3821b73beadc71400a9c25...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/account#cm4` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/rival#r5` | true | `observation:h005.fcl1@47b912a432a94d11aa2e6e...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/rival#r5` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/response#k2` | true | `observation:h005.fcl1@a641812964a9c881a71903...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/response#k2` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/response#k3` | true | `observation:h005.fcl1@ce6e76416d76689a4a0aa8...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/response#k3` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/response#k4` | true | `observation:h005.fcl1@412073a718f5708d15d210...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/response#k4` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/response#k5` | true | `observation:h005.fcl1@ad9c8f05dbcdfadca9de3a...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/response#k5` |
| `k:h005.fcl1:daily/mini_fcl/cycle01/carry#d2` | true | `observation:h005.fcl1@8cc108dd394e1d53c113ef...` | `pi:h005.fcl1.research:k:h005.fcl1:daily/mini_fcl/cycle01/carry#d2` |

An observation-valued commitment with no covering evidence is **scheduled-pending, never failed** (spec §12): it spawns a research problem instead of a verdict. The `eval` string is outside every executable class, so nothing can dispatch it.

## Residue

| code | severity | unit | count |
|---|---|---|---|
| `adjudication_batched` | informational | file | 1 |
| `bare_label_ref` | extension | ref | 0 |
| `claim_record_unmapped` | unmapped | record | 10 |
| `commitment_not_executable` | informational | record | 10 |
| `commitment_record_not_in_uptake` | informational | record | 0 |
| `consequence_on_non_commitment_record` | informational | record | 0 |
| `criticism_of_criticism_intra_document_dropped` | lossy | ref | 0 |
| `criticism_of_criticism_retargeted` | informational | edge | 0 |
| `dependence_cycle_rejected` | error | edge | 0 |
| `depends_cross_document` | informational | ref | 0 |
| `depends_intra_document` | lossy | ref | 14 |
| `grounds_absent_on_objection` | informational | record | 8 |
| `mentions_intra_document` | lossy | ref | 6 |
| `objection_self_target_only` | lossy | record | 7 |
| `objection_target_self_ref_dropped` | lossy | ref | 2 |
| `objection_untargeted` | lossy | record | 1 |
| `opaque_envelope` | informational | artifact | 0 |
| `parse_failure` | error | document | 0 |
| `problem_trigger_approximated` | lossy | problem | 10 |
| `problem_trigger_research_not_in_v13_enum` | informational | problem | 10 |
| `projection_absent` | informational | document | 2 |
| `projection_exposed_unreferenced` | informational | document | 8 |
| `prose_commitment_surface` | informational | artifact | 0 |
| `qualified_ref_body_pseudo_local` | extension | ref | 0 |
| `ref_through_absent_projection` | error | ref | 0 |
| `ref_through_unexposed_view` | error | ref | 0 |
| `ref_to_task_artifact` | informational | ref | 0 |
| `ref_to_unregistered_target_dropped` | error | ref | 0 |
| `ref_unresolved` | error | ref | 153 |
| `revises_unmapped` | unmapped | ref | 5 |
| `schema_failure` | error | document | 0 |
| `target_on_non_objection_record` | informational | record | 0 |
| `uptake_lists_unmapped` | unmapped | document | 5 |
| `uptake_refs_unmapped` | unmapped | ref | 100 |
| `use_record_unmapped` | unmapped | record | 4 |
| `validity_node_minted_unasserted` | informational | artifact | 0 |
| `warrant_edge_deduplicated` | informational | edge | 0 |
| `withdraws_unmapped` | unmapped | ref | 0 |

Counts follow the unit column: `ref` counts references, `record` counts FCL records, `document` counts FCL-1 documents or trace documents, `edge` counts attack or dependence edges, `artifact` counts artifacts, `problem` counts problems, `file` counts occurrence files. Full entries, each with the verbatim source text that was not mapped, are in `residue.json`.

**What this table does and does not claim.** Every FCL record in scope is accounted for at record granularity: each record is either mapped to a spec construct or reported under a residue code, and `side_table.json.records[]` shows which, per record, with the codes it raised. The same holds for every reference this import resolved. It is **not** a claim that every nuance inside a mapped record survived the mapping: a record that became a `Commitment` kept its text and lost its prose structure, and the codes above are the granularities the closed vocabulary names (`ref`, `record`, `document`, `edge`, `artifact`, `problem`, `file`), not a proof of semantic completeness.

## Declared deviations

- **`adjudication_batched`** (1 in this scope) - no separate terminal Adj event is emitted. spec §3 recomputes after every registration and the vendored P0 Harness does exactly that inside each registration event, but it exposes no public Adj emitter; the import writes through the registration API only and never forges a log line, so the terminal adjudication is the state after the last event.
- **`problem_trigger_approximated`** (10 in this scope) - imported FCL problem records use SpawnTrigger.SEED. the vendored enum has no 'import' member; 'seed' is the only trigger that does not assert an in-graph derivation. The clean fix is an enum addition, requested rather than papered over.
- **`problem_trigger_research_not_in_v13_enum`** (10 in this scope) - research problems use SpawnTrigger.RESEARCH with empty criteria. the vendored enum has the member and §12 is exactly this path, but the trigger is not part of the v1.3 enum text; criteria stay empty because no instantiated commitment id is a criterion.
- **`depends_intra_document`** (14 in this scope) - document-local depends refs are dropped, not turned into dep edges. at node granularity they would be dep self-loops, i.e. cycles; toposort rejects them and a self-loop asserts nothing the author declared.
- **`objection_self_target_only`** (7 in this scope) - a self-targeting objection mints no warrant. a Dung self-attack means 'this argument is self-defeating', which is not what an intra-document caveat asserts; minting it would flip two labels for reasons that have nothing to do with the evidence.
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
why(93d07e37f88e7da49c54a950858f6f513573250c619f802f6d8d2abb0b7cf2be)
  artifact : daily/mini_fcl/cycle01/account
  status   : accepted

  daily/mini_fcl/cycle01/account [93d07e37f88e] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(a607a7e41503c361c8058d1aaa26261308aa78e0a89a0cb66c0874c30de92b24)
  artifact : daily/mini_fcl/cycle01/account#commitments
  status   : accepted

  daily/mini_fcl/cycle01/account#commitments [a607a7e41503] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(db2a2adfc9f419cad65e33023f103e3ab00862ed5cc8fac40c0aa97953b80862)
  artifact : daily/mini_fcl/cycle01/carry
  status   : accepted

  daily/mini_fcl/cycle01/carry [db2a2adfc9f4] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(5bd8ebc5cd5b204a58d3605417860325c39f1a2087cb456560705ca795f57791)
  artifact : daily/mini_fcl/cycle01/carry#commitments
  status   : accepted

  daily/mini_fcl/cycle01/carry#commitments [5bd8ebc5cd5b] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(983099fb06b575eb38cefad7b1eddab497fb152c00c5ee7168a642fe30b2d9a7)
  artifact : daily/mini_fcl/cycle01/objection
  status   : accepted

  daily/mini_fcl/cycle01/objection [983099fb06b5] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(d7d8d1e0c56509f234c5959e15b3b7b2ba55ca74d61b418c25960d60fc4f0725)
  artifact : daily/mini_fcl/cycle01/objection#commitments
  status   : accepted

  daily/mini_fcl/cycle01/objection#commitments [d7d8d1e0c565] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(7771193a8a9a90af0df43dfd2a17b1b8b132c6998f4bd2ae50e37d1c27911f35)
  artifact : daily/mini_fcl/cycle01/response
  status   : accepted

  daily/mini_fcl/cycle01/response [7771193a8a9a] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(5a24f84a15791961d50b209abcae2913a1b16f29bec2d3040e9a33361f0a3a6d)
  artifact : daily/mini_fcl/cycle01/response#commitments
  status   : accepted

  daily/mini_fcl/cycle01/response#commitments [5a24f84a1579] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(f5ad66e26fa0cf22a22b57d6654d4a6b6e8ded7629245c4789e221a2fb219699)
  artifact : daily/mini_fcl/cycle01/rival
  status   : accepted

  daily/mini_fcl/cycle01/rival [f5ad66e26fa0] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

```
why(086989040489592e4f07b776ce7c4702af1968ae3e96b24633c1e15936a067f6)
  artifact : daily/mini_fcl/cycle01/rival#commitments
  status   : accepted

  daily/mini_fcl/cycle01/rival#commitments [086989040489] -- accepted
  (no attacker in the imported relation)

  accepted: unattacked in the imported attack relation, so it enters the grounded extension at the first Kleene step. This is accept-by-position: no warrant in this import targets it. This import reified criticism only from an FCL-1 commitment surface, so the absence of an attacker is not evidence that the contribution was uncriticised.
  declared dependence (dep): none, so pass 2 is a no-op for this artifact.
  I7: No label produced by this import is a semantic attribution. Statuses are mechanism bookkeeping over the imported attack relation; they do not bear on the FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone interprets substantive output (PROTOCOL.md §Interpretation).
```

