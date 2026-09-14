> **Status: design of record, NOT executed** (see
> [`../reviews/engine-path-decision-2026-09-14.md`](../reviews/engine-path-decision-2026-09-14.md)).
> Produced by delegated Opus 5 agents (three architects, three judges, one
> synthesizer) under REC-20260914-M.

# `src/deepreason/` — final design of record

**Target:** harness-spec v1.3 §0–§4 and §14–§16 P0, then P1 offline, then H005 occurrence-02.
**Repository:** `/home/user/miniReason`, branch `claude/project-state-direction-j5rbun`. All paths absolute or repo-relative as marked.
**Normative sources consulted for this document:** `docs/sources/harness-spec-v1.3.md` (588 lines, read in full), `AGENTS.md`, `PURPOSE.md`, `docs/DECISION_LEDGER.md`, `docs/STATUS.md`, `docs/reviews/{fcl1-language-proposition,multi-cycle-research-contract,h005-matched-arm-envelope-asymmetry}-2026-09-14.md`, `experiments/diagnostics/H005-open-prose-commitments/{material.json,PROTOCOL.md}`, `src/creib/{canonical.py,forge/mini/{log,ports,kinds,runner,adjudication}.py}`, `src/minireason/provider.py`, `tools/multicycle_commitment_study.py`, `tests/mini/test_architecture.py`, and the upstream clone at `/home/user/ahepi/deepreason` (`AHepi/DeepReason`, commit `9607fba6f0a3066fbcab282c9ae0fad823e52e0c`, MIT).

---

## 1. Thesis and decision record

### Thesis

Build a new, self-contained package `src/deepreason/` that implements harness-spec v1.3 §0–§4 and §14–§16 literally and deterministically, touches nothing frozen, imports nothing from `creib.forge.mini`, and depends on no copied upstream bytes on its critical path — because the one thing this repository sells is an audited tree whose every line has a receipt, and because `AGENTS.md` authorises extraction from `AHepi/h-EPI`, not from `AHepi/DeepReason`. The engine's job is narrow and mechanical: make a commitment a first-class object rather than a string inside a string; make a view a deterministic projection of `interface` rather than a helper-authored body (`src/creib/forge/mini/ports.py:18` ships exactly `("text","list_bodies","list_bodies_and_commitments","legend")` and `:97-98` raises `MINI_RENDER_RULE_UNKNOWN`, which is why H005's `view: commitments` cannot compile today); make a criticism land a computed `att` edge with an attackable validity node; and make a refuted premise drag its dependents to `suspended_unsupported` instead of leaving them `accepted` — the single place where the frozen engine is positively wrong rather than merely silent. Everything above §4 is deferred by name. The reward is that §16 P0's six acceptance tests fall out of the same ~1,600 lines that unblock H005 occurrence-02, that every LLM-touching test runs offline from a keyed raw tape, and that the FCL-1 arm and the free-prose arm both receive real §1 Commitment objects so the comparison is about a *carrier*, not about whether one arm has a mechanism at all.

### Decision record

**Winner: `purist`.** Two of three judges ranked it first (30/35 and 28/35); the third ranked it second (25) behind `research` (28). Weighing the rationales rather than the totals confirms the majority: the two purist-first judgements are argued from clause-level checks that I re-verified (complete `codec` enum including `f64le`/`i64le` at spec line 45; the `warrants` legacy shorthand at line 47; §14:505 `objects/<schema>/<sha256(id)>.json` with conflicting-registration rejection; §1:80-88 oracle isolation, which only purist implements; §16 P1's literal "returns the Pareto frontier of survivors", which only purist reaches). The dissenting judgement is argued from governance and research validity, and on those two points it is right — but both of its decisive objections are *repairable inside purist's skeleton* without touching its wave structure, whereas purist's parallel-build machinery (whole-file single-agent ownership, a Wave-0 freeze of every `__init__.py` and `pyproject.toml`, a fixture key that carries provider identity) is not reproducible inside research's explicitly unsplittable Wave 2. I therefore take purist's engineering spine and research's governance, epistemology and H005 mapping wholesale.

**Grafted from `research`:**

1. **Refusal to vendor.** The critical path copies zero upstream bytes. Upstream is used only as a *skip-by-default cross-check* (`tests/deepreason/test_upstream_agreement.py`) and as an optional, ledger-gated substitution that would change no interface in this document. This removes purist's schedule contingency on an authorisation nobody holds.
2. **The FCL-1 reduction table** (§6 below), including the verdict that `claim` and `uptake` contribute nothing mechanical and that `depends`/`mentions`/`objection.target` are notations for relations §1 already owns.
3. **The symmetric arm mapping.** Both H005 arms get real §1 Commitment objects. This repairs purist's only research-damaging choice (an empty `interface` for the prose arm, which under §6:244 makes prose artifacts undemarcated) and honours `docs/reviews/fcl1-language-proposition-2026-09-14.md:50` verbatim: *"The prose condition receives the same meaning of commitment, dependency versus mention, and fallible criticism, expressed as permission to write ordinary prose. This controls for adding those ideas rather than their formal notation."*
4. **The pack field manifest as a harness output** — `docs/reviews/multi-cycle-research-contract-2026-09-14.md:19` requires the study to "record which artifacts and fields each subsequent invocation actually sees", and only research supplies it as an engine output rather than helper bookkeeping.
5. **`views/projection.py`'s absence invariant** — "source absent at this coordinate", never "no such thing existed", asserted by test, taken from the material's own `system` instruction.
6. **Schema-validated structured node replies with bounded repair and a logged `FORMAT_FAILURE` that drops the cycle**, which kills the `commitments_sha256 = e3b0c442…` (sha256 of the empty string) failure at its source rather than downstream of `decode_contribution` (`tools/multicycle_commitment_study.py:329-341`).
7. **`docs/deepreason/DIVERGENCES.md`**, append-only, one line per departure and per omission, opening with the statement that frozen-engine results are not arm-for-arm comparable with new-engine results.
8. **A stated falsifier** for the design itself, and the pre-declared warning that pass 2 turns some formerly-`accepted` artifacts into `suspended_unsupported` — a correction, not a result.
9. **The waves-0–3 fallback** so engine work cannot silently displace the research.

**Grafted from `reuse`:**

10. **The no-float canonical profile.** `src/creib/canonical.py:13-29` rejects any float; we re-implement the same discipline in `deepreason/canon.py` and represent every estimate as an integer triple `{"num","den","k"}`. An IEEE double from a ratio computed on a different libm is exactly the machine-dependent value §1:79 bars from a content-addressed trace. Applied to the identity/JSON layer **only** — the `codec` enum keeps `f64le` and `i64le`, because §3.1/Thm 2.1 puts numeric bytes in scope as *content*.
11. **The AST import-allowlist test**, modelled on `tests/mini/test_architecture.py:36-48`, inverted: it asserts the new package imports **nothing** from `creib.*` or from the four frozen `src/minireason/*_mini.py` modules, and a companion test pins the tree hash of `src/creib/forge/mini/**` so an accidental edit fails loudly.
12. **Wrapping `src/minireason/provider.py` unchanged** for the DeepSeek family rather than re-implementing audited credential discipline (`provider.py:23` `BoundedSemaphore(5)`, `:100` key read at call time, `:120-123` `SECRET_IN_REQUEST`, `:157` `reasoning_content_persisted: False`). `provider.py` is not frozen; the four `*_mini.py` study modules are.
13. **Distinct id domains in the storage layout** (`objects/<schema>/…` where every schema name is `deepreason.*`), so an id from this engine can never be confused with a Mini `content_id`.

**Dropped, with reasons:**

- **Vendoring upstream `adjudication/`, `ontology/`, `log/`, `storage/` (purist Waves 0–2).** Dropped: unauthorised under `AGENTS.md`, and it would import three deliberate v1.3 reversals (`/home/user/ahepi/deepreason/src/deepreason/rules/spawn.py:58-66` documents the H1 deletion of "failed verdict ⇒ successor problem"; `measures/demarcation.py` supersedes `active(a)`; four §13 verbs are absent) plus four amendments (v1.4–v1.7) this repository has never adopted. §4 is verbatim pseudocode in the spec and safe to type; the closure fixpoint is the only genuinely risky code, and it gets the heaviest test battery plus the optional upstream agreement check.
- **Purist's honouring of v1.4's authority boundary.** Dropped: adopting an amendment we do not hold is the exact move `AGENTS.md` forbids, and it contradicts the spec-purist thesis.
- **Pydantic (§14:521 "Pydantic models throughout").** Dropped as a *declared divergence*, not an omission. Frozen dataclasses + a hand-written canonical encoder + `jsonschema==4.25.1` (already pinned) instead. Reasons: (i) P0 acceptance is byte-for-byte replay, and a third-party serializer inside the identity function makes replay hostage to a minor version; (ii) this repository's evidence discipline runs through one float-rejecting canonicaliser, and two canonicalisers in one tree is a drift class the errata already track; (iii) `AGENTS.md`/`PURPOSE.md` make the pinned, fully-audited two-dependency tree part of the deliverable. Pydantic 2.13.5 *is* present in this environment, so the divergence is about the dependency contract, not availability, and it is reversible: pydantic could later be added as a validation layer strictly outside id computation without changing one interface in §7 below.
- **Reuse's domain-framed ids** (`sha256:<hex>` over `domain\0canonical`). Dropped: §1:41 says `sha256(canonical(content_ref, codec, interface))`, and a framed id agrees with no other v1.3 implementation, which also forecloses the cross-check test.
- **Reuse's import of `creib.forge.mini.log.BlobStore` and `common.content_id`.** Dropped: it makes a frozen research specimen load-bearing for running code. We re-implement the *design* (write-once, self-verifying, hash-chained) as new bytes.
- **Reuse's deference to upstream on §13's `focus`/`expand`/`attack`/`step`.** Dropped: those verbs are in v1.3 at line 497 and are implemented.
- **Registering `eval:rubric` commitments before §10 lands.** Dropped on all arms. §1 says `<spec-id>` **MUST** resolve to a registered standard artifact and §2 makes it a well-formedness condition; leaving such a commitment "registered but unevaluated" does not cure the resolution defect. Until P5, every H005 commitment is `program:` or `predicate:` or it is not a Commitment.
- **Research's single-owner Wave 2.** Dropped: split into six parallel modules using purist's file-level ownership.
- **A `variator` role at P1.** Dropped: `≈_B` compares verdict vectors over the active battery and needs no edits; the variator is for HV (§6/§7), which is P2.

**Fatal flaws fixed (checklist).** Governance gate → vendor-free critical path. Float/canonicaliser collision → no-float profile + integer triples. Purist's H005 prose confound → symmetric commitment mapping. Missing FCL-1 `commitment` → `eval` mapping → specified in §6. Popper battery after the P0 gate → moved into Wave 1/2, inside the gate. Intra-wave dependencies (purist 1B→1A, 2D→2B, 4D→4A/4B/4C) → every wave below is dependency-free internally. Research's missing §14:505 object store → Wave 1 module M102. Research's truncated `codec` enum and dropped `warrants` shorthand → restored. Missing Pareto at P1 → Wave 2 module M203, axis-generic. Missing oracle isolation → Wave 1 module M105. Reuse's provider-blind fixture key → key carries endpoint, model, temperature, schema id. `addr` misuse for artifact-to-artifact `uptake` → `uptake` is rendered only. No falsifier → §9.

---

## 2. Package and module layout (exact paths)

New tree. `src/creib/**`, `src/minireason/{language_mini,inquiry_mini,reason_use_mini,successor_mini}.py`, `experiments/records/**`, `experiments/plans/**`, `experiments/diagnostics/H005-open-prose-commitments/material.json` and every published occurrence are never opened for write.

```
src/deepreason/
  __init__.py                    # version + re-exports only, written once in Wave 0
  errors.py                      # DeepReasonError + the frozen code list
  canon.py                       # canonical JSON (no floats), sha256 helpers, rationals
  types.py                       # enums/tuples: CODECS, REF_ROLES, RULES, STATUS, ...
  config.py                      # §15 Config (22 knobs + role seats), load(), render()
  harness.py                     # register / carry / spawn / adjudicate / replay / at(seq)
  loop.py                        # P1 single-problem Conj -> Crit -> Adj driver
  ontology/
    __init__.py artifact.py commitment.py warrant.py problem.py state.py
  log/
    __init__.py event_log.py chain.py
  storage/
    __init__.py blobs.py objects.py
  adjudication/
    __init__.py graph.py grounded.py support.py edges.py
  commitments/
    __init__.py registry.py popper.py predicate.py program.py sandbox.py
  rules/
    __init__.py conj.py crit.py spawn.py refl.py
  guards/
    __init__.py anti_relapse.py
  measures/
    __init__.py demarcation.py pareto.py
  unification/
    __init__.py isolation.py                 # conn/iso + stubbed driver (P0 scope row)
  views/
    __init__.py projection.py theory.py why.py prose.py
  llm/
    __init__.py roles.py schemas.py packs.py rawstore.py adapter.py gate.py endpoints.py
  h005/
    __init__.py fcl1.py material.py driver.py
  cli/
    __init__.py main.py
tests/deepreason/
  __init__.py
  test_boundaries.py test_canon.py test_config.py
  test_ontology.py test_event_log.py test_storage.py test_graph.py test_edges.py
  test_commitments.py test_harness.py test_projection.py test_views.py
  test_measures.py test_anti_relapse.py test_isolation.py test_fcl1.py
  test_p0_adjudication.py test_p0_closure.py test_p0_registration.py
  test_p0_log.py test_p0_replay.py test_p0_scope.py
  test_cli.py test_rules.py test_roles_schemas.py test_packs.py test_adapter.py
  test_p1_acceptance.py test_h005_topologies.py test_h005_driver.py
  test_endpoints.py test_upstream_agreement.py        # skipped unless upstream importable
  fixtures/raws/<key>.json                             # committed replay tape
docs/deepreason/DIVERGENCES.md                         # append-only
docs/deepreason/UPSTREAM_REFERENCE.md                  # clone commit, reversals, non-adoption
```

`pyproject.toml` gains nothing: dependencies stay `jsonschema==4.25.1`, `referencing==0.37.0`. The suite is discovered by the existing `PYTHONPATH=src python -X utf8 -m unittest discover -s tests`.

---

## 3. Data model

All ids are lowercase 64-hex `sha256` of canonical bytes, with **no prefix and no domain framing** (§1:41). Canonical JSON = `json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")` over the **float-free profile**: `None`, `bool`, `str`, `int` (exact type), `list`, `dict` with string keys. Any `float` raises `DeepReasonError("DR_CANONICAL_PROFILE", …)`. Arrays are **never reordered** — canonical JSON sorts keys, not lists — so two artifacts differing only in ref order are different artifacts, deliberately and by declared rule.

### Records

```json
// artifact  —  id = sha256(canonical({"codec":…,"content_ref":…,"interface":…}))
{ "id": "<64hex>",
  "content_ref": "<blob 64hex> | <inline-string>",
  "codec": "utf8|json|csv|f64le|i64le|code:<lang>|raw",
  "interface": { "commitments": ["<cid>"],
                 "refs": [{"target":"<aid>","role":"dependence|mention|evidence"}] },
  "warrants": ["<wid>"],
  "provenance": { "role":"conjecturer|critic|variator|synthesizer|seed|import|user",
                  "school": null, "event_seq": 0 } }
```
There is **no `kind` field** (§0:30) and a test asserts the field set. `warrants` is the §1 legacy/on-record shorthand: it is **not** part of the id, and at registration the harness normalises each entry into the explicit `carry` relation exactly once. `provenance.event_seq` is outside the id — the precise divergence from `src/creib/forge/mini/runner.py:393-411`, which hashes `{stage_id, kind_id, seq, body_ref, commitments_ref, extra}` so identical content at two seqs gets two ids, foreclosing anti-relapse stage 1 (§3:191) and P3 dedupe-by-id (§16:569).

```json
// commitment — id = sha256(canonical({"budget":…,"eval":…,"observation_valued":…}))
{ "id":"<64hex>", "eval":"program:<ref> | rubric:<spec-id> | predicate:<expr>",
  "budget": {"steps":100000,"time_ms":2000},   // extended structured keys allowed (§1, §7)
  "observation_valued": false }

// warrant — id = sha256(canonical({"commitment","target","trace_ref","type","validity_node","verdict"}))
{ "id":"<64hex>", "target":"<aid>", "type":"demonstrative|argumentative",
  "commitment":"<cid>|null", "verdict":"fail|null",
  "trace_ref":"<blob>|null", "validity_node":"<aid>" }

// problem — id = sha256(canonical({"criteria","description","provenance"}))
{ "id":"<64hex>", "description":"…", "criteria":["<commitment-schema-id>"],
  "provenance":{"trigger":"seed|successor|discrimination|remove-arbitrariness|
                           explanation-debt|audit-critic|connection|integration",
                "from":["<id>"]} }

// event — one JSONL line; §1:143-151 plus three declared additions marked (+)
{ "schema_version":"deepreason.event.v1",
  "seq":0, "ts":"2026-09-14T00:00:00Z",
  "prev":"<64hex>",                               // (+) previous event_id; genesis = run-header digest
  "rule":"Conj|Crit|Adj|Spawn|Refl|Register|Merge|Measure|Reveal|Reseed",
  "inputs":["<id>"], "outputs":["<id>"],
  "llm":{"role":"…","model":"…","endpoint":"…","prompt_ref":"<blob>","raw_ref":"<blob>",
         "tokens":0,"ms":0,"pack_manifest_ref":"<blob>"} | null,   // (+) manifest ref
  "state_diff":{"carry+":[],"att+":[],"dep+":[],"A+":[],"Pi+":[],"status_changed":[],
                "digest":"<64hex>"},              // (+) on Adj events only: state digest
  "event_id":"<64hex>" }                          // (+) sha256(canonical(event minus event_id))
```

Blob ref = `sha256(bytes)`. Run header = `{"schema_version":"deepreason.run.v1","root_id":…,"config_digest":sha256(canonical(config.to_dict())),"created_ts":…}`; its digest is the genesis `prev`.

**`ts` determinism rule (normative here).** `ts` is recorded (§1:145) and is inside `event_id` and the chain. It is excluded from every artifact/commitment/warrant/problem id, from every verdict, and from the state digest. Two harnesses replaying one log therefore agree byte-for-byte while `ts` remains a record of *when*, never an input to *what* (§1:79).

**Numbers.** No floats anywhere in a record. Every estimate — HV, reach, λ, typicality, coverage — is `{"num":int,"den":int,"k":int|null}`. Comparison is by cross-multiplication.

**Storage (§14:505-511).** `objects/<schema>/<sha256(id)>.json` for `deepreason.artifact.v1`, `…commitment.v1`, `…warrant.v1`, `…problem.v1`, plus `blobs/<hex[0:2]>/<hex>` write-once content-addressed bytes and `log.jsonl`. An id is globally unambiguous within a root: a conflicting registration of a known id with different canonical bytes is **rejected** (`DR_OBJECT_CONFLICT`), never silently resolved. `holdout/` namespace is reserved and empty at P1.

### `dep` derivation and cycle rejection

`dep = { (a.id, r.target) : r ∈ a.interface.refs, r.role == "dependence", both endpoints registered }` (§1:53). Edges materialise only when both endpoints are registered, so refs may dangle across import/merge order (§14:516-519). `dep` MUST remain a DAG (§1:63): before appending the registration event, the harness computes the prospective `dep` and runs `adjudication.graph.toposort`; a cycle raises `DeepReasonError("DR_DEP_CYCLE", …)` and **no event is appended, no object is written, no blob is written**. `toposort` is Kahn's algorithm over a lexicographic min-heap of ids — deterministic, and its output order is part of the replay contract.

### `att` derivation: base plus three closures to fixpoint (§1:54-62, :107-114)

Base: for every `(k, w) ∈ carry` with `k` and `w` registered and `w.target` registered, add `(k → w.target)`.

Then iterate until no edge is added:

- **C1 validity-node closure (§1:107).** For every warrant `w` with `validity_node ν`, for every `x` with `(x → ν) ∈ att`, add `(x → k)` for every carrier `k` of `w`. Encoding note: a warrant is not a node, so "attacker of ν attacks the warrant" is realised as an attack on each carrier — which is what makes the carrier fall out of `G` and the target reinstate in pass 1.
- **C2 case-law closure (§1:108).** For a rubric-derived warrant, its ν MUST carry a `mention` ref to the standard artifact `s` it applied. For every `x` with `(x → s) ∈ att`, add `(x → ν)`. C1 then propagates to every carrier. Refute a standard ⇒ every ν citing it is attacked ⇒ every warrant under it falls ⇒ targets reinstate, all in pass 1.
- **C3 evidence closure (§1:109-114).** For a ν carrying an `evidence` ref `e`, let `L(e) = {e} ∪ {y : e →*dep y}` (the transitive dependence lineage of the evidence). For every `y ∈ L(e)` and every `x` with `(x → y) ∈ att`, add `(x → ν)`.

Fixpoint, because C2/C3 create attackers of ν which C1 turns into attackers of carriers, which can change who attacks a standard or an evidence lineage. Iteration order is over sorted ids; the result is a set and therefore order-independent, but the deterministic order keeps traces comparable. A warrant naming an unregistered carrier, target, or ν is rejected at registration (`DR_UNREGISTERED_WARRANT`, §2:157). **`build_att` and `build_dep` read record dicts; `grounded`/`support` read `att` and `dep` and nothing else** (§4:229).

### Epistemic state and the state digest

`S = (A, Π, carry, att, dep, addr, status, hv, reach, conn)` — a materialized view, recomputable at any `seq` (§1:131). `state_record(S)` is a total, sorted, float-free projection: artifacts and problems as canonical records sorted by id; `carry`, `att`, `dep`, `addr` as sorted lists of pairs; `status` as an id→label object; `hv`/`reach`/`conn` as id→integer-triple/int objects. `state_digest(S) = sha256(canonical_bytes(state_record(S)))`. `ts` never appears in it.

---

## 4. Adjudication, the P0 test list, and replay

### Algorithm (§4:208-224, verbatim)

```
Pass 1 (Dung grounded extension, unique, skeptical, polynomial)
  F(X) = { a ∈ A : ∀ (b,a) ∈ att, ∃ c ∈ X with (c,b) ∈ att }
  G    = least fixed point of F from ∅        # Kleene iteration over sorted ids
  label0(a) = "accepted"  if a ∈ G
              "refuted"   if ∃ b ∈ G with (b,a) ∈ att
              "suspended" otherwise

Pass 2 (support, compiled into Dung; registered via Refl as a rule-artifact)
  for a in toposort(dep):                     # a -> b means "a depends on b"
      supported(a) = all(final(b) == "accepted" for (a,b) in dep)
      if   label0(a) == "accepted" and supported(a): final(a) = "accepted"
      elif label0(a) == "accepted":                  final(a) = "suspended_unsupported"
      elif label0(a) == "refuted":                   final(a) = "refuted"
      else:                                          final(a) = "suspended"
```

Three labels in pass 1, four terminal statuses. Recomputed **after every registration** (§3:171, §4:228), not once per cycle as `src/creib/forge/mini/adjudication.py:162-164` does. A mutual attack is `suspended`, data, not an alarm — directly replacing Mini's two-value `ACCEPTED, REFUTED` (`adjudication.py:51`) and its `MINI_ADJUDICATION_UNSETTLED` raise (`:134`), consistent with `AGENTS.md`'s "do not let an operational alarm adjudicate content". The pass-2 rule and the `suspended_unsupported` label are themselves registered as a Refl rule-artifact at root creation, attackable under N1.

Measures, school membership, novelty, Pareto rank never enter label computation (§0:33, §4:229); a unit test asserts `grounded.py` and `support.py` import nothing but `deepreason.types` and stdlib.

### P0 acceptance, mapped to §16:566

§16 P0 acceptance names six unit-test obligations and the P0 scope row additionally names the Popper battery, the isolation/integration driver stubbed with knobs, and the `why`/inspect CLI, with **no LLM**.

| §16 P0 clause | Test (all under `tests/deepreason/`) |
|---|---|
| grounded extension correctness | `test_p0_adjudication.py::test_unattacked_is_accepted`, `::test_attacked_by_G_member_is_refuted`, `::test_mutual_attack_is_suspended_both_ways` |
| reinstatement (Lemma 3.1) | `test_p0_adjudication.py::test_reinstatement_lemma_3_1` — `k→a`, `j→k`, `j` unattacked ⇒ `{j,a} ⊆ G`, `a` accepted |
| two-pass support cascade | `test_p0_adjudication.py::test_orphaned_is_not_false` — premise refuted ⇒ dependent `suspended_unsupported`, **never** `refuted`; `::test_relation_refuted_endpoints_accepted` |
| cycle rejection in `dep` | `test_p0_registration.py::test_dep_cycle_rejected_writes_nothing` — raises `DR_DEP_CYCLE`; log length, object count and blob count unchanged |
| standard-refutation ⇒ verdict collapse ⇒ reinstatement via closure | `test_p0_closure.py::test_standard_refutation_collapses_and_reinstates` — one standard `s`, one rubric ν `mention`ing `s`, one warrant, one target; attack `s` ⇒ target returns to `accepted`, with an assertion that **no status rule outside `att`/`dep` ran** (the labels recompute from the edge sets alone) |
| replay reproduces state byte-for-byte | `test_p0_replay.py::test_replay_state_bytes_identical`, `::test_every_adj_event_digest_matches_on_replay`, `::test_truncated_replay_matches_historical_view`, `::test_at_seq_writes_nothing` |

Scope-row tests: `test_p0_scope.py::test_artifact_has_no_kind_field`, `::test_codec_enum_is_complete` (all seven forms incl. `f64le`, `i64le`, `code:<lang>`), `::test_popper_battery_auto_pinned_into_every_problem`, `::test_isolation_knobs_present_and_driver_stubbed` (`FLOOR`, `K`, `INTEGRATION_BUDGET_SHARE` present; `conn`/`iso` computed; no Spawn wired), `::test_why_cli_prints_attack_defence_chain`, `::test_p0_run_makes_zero_llm_calls` (the adapter is constructed in `replay` mode with an empty tape and any call raises).

Hardening tests carried alongside: `test_p0_closure.py::test_validity_node_closure_disables_every_carrier`, `::test_evidence_closure_reinstates_target`; `test_p0_registration.py::test_unregistered_warrant_rejected`, `::test_conflicting_object_registration_rejected`, `::test_legacy_warrants_field_materialises_carry_once`; `test_p0_log.py::test_sequence_gap_dup_and_rewind_rejected`, `::test_chain_break_detected`, `::test_torn_tail_repaired_write_side_only`, `::test_read_only_open_creates_no_file`.

### Replay byte-for-byte strategy

1. The log is the source of truth; graph state is a materialized view (§0:32). `Harness.replay(root)` reads `log.jsonl`, verifies `seq == line_index` for `0..N-1` and `event.prev == previous.event_id` and `event_id == sha256(canonical(event minus event_id))` on every line, and applies events in order.
2. Every `Adj` event records `state_diff.digest = state_digest(S)`. Replay recomputes the digest after each `Adj` and compares. A divergence localises to one event rather than surfacing as a whole-run mismatch.
3. The acceptance test asserts `canonical_bytes(state_record(live)) == canonical_bytes(state_record(replayed))` — bytes, not just digests — and that `Harness.at(root, seq)` produces exactly the historical bytes.
4. `Harness.at(root, seq)` is physically read-only (§1:137-139): it opens the log with `read_only=True`, creates no directory, repairs no torn tail, writes no object, blob or event. Torn-tail repair happens only on a write-side open.
5. Determinism guards that make (3) hold: `ts` excluded from ids/verdicts/digest; lexicographic tie-break in `toposort` and in the grounded iteration; no floats; arrays never reordered; program evaluators budgeted by **step count only**; pack truncation by whole sections; LLM raws served from the keyed tape so a replayed verdict consumes the logged raw (§7:302).

---

## 5. P1: loop, roles, packs, contracts, guards, adapters

**Scope (§16:567).** Single-problem `Conj → Crit(program + argumentative) → Adj`; Popper battery; anti-relapse hash + battery stages; born-connected conjecture; VS conjecturer contract; theory render. **Acceptance:** point at a problem file → the Pareto frontier of survivors, a rendered theory document, a complete trace; anti-relapse blocks a re-submitted refuted idea; a γ-call yields `VS_K` schema-valid candidates. All of it offline.

**Loop** (`loop.py::run(harness, adapter, problem_id, cycles, config)`):

1. **Conj** (§3:169) gated on `Π ≠ ∅`. The pack carries the target problem's neighbourhood, so conjecture is born-connected (§7:275 L1). The conjecturer returns exactly `VS_K` candidates with integer-ratio typicality. Each candidate passes the anti-relapse gate before commit.
2. **Crit — program.** Each commitment in `I(a)` is evaluated by `commitments/registry.py::evaluate` under a deterministic step budget. `fail` mints a demonstrative warrant with a registered ν artifact and a critic artifact carrying it. `overrun` packages **no** warrant. `sandbox_abort` (a containment kill) produces no epistemic verdict, mints no warrant, is not cached, and is surfaced through the `overrun` envelope with the `sandbox_abort` flag (§1:80-88).
3. **Crit — argumentative.** The critic returns a case plus the ids it essentially relies on; those become `dependence` refs on the critic artifact, so withdrawing a premise collapses the critic through pass 2 rather than through a special rule. The warrant is `type: "argumentative"`, `commitment: null`, `verdict: null`, with a ν carrying the case's grounds.
4. **Adj** after every registration.

**Popper battery** (auto-pinned into every problem's `criteria`, §1:123): `surface-nonempty` (⇔ `crit(a)` of §6:244, compiled to a program so an artifact that forbids nothing is refuted *by a program*, not by a measure), `refs-resolve`, `no-self-dependence`. Each is `eval: "program:<name>@<params-hash>"`, content-addressed, replay-stable.

**Roles at P1** (§9:336): `conjecturer` (Verbalized Sampling contract, §11.6), `argumentative_critic`, `summarizer` (blob shape/stats/head rendering only). Declared and **not** implemented at P1: `defender`, `judge`, `variator`, `synthesizer`, `embedder` — each gets a `DIVERGENCES.md` line naming what it would unlock. Consequence: anti-relapse runs stages 1 and 3 only; stage 2 (semantic NN) is absent, fails open, and logs a degradation record.

**VS conjecturer contract** (`llm/schemas.py`, jsonschema, `RETRY_MAX` bounded repair):

```json
{"type":"object","required":["candidates"],"additionalProperties":false,
 "properties":{"candidates":{"type":"array","minItems":1,"maxItems":16,"items":{
   "type":"object","required":["content","typicality","interface"],"additionalProperties":false,
   "properties":{
     "content":{"type":"string"},
     "typicality":{"type":"object","required":["num","den"],"additionalProperties":false,
       "properties":{"num":{"type":"integer","minimum":0},"den":{"type":"integer","minimum":1}}},
     "interface":{"type":"object","required":["commitments","refs"],"additionalProperties":false,
       "properties":{"commitments":{"type":"array","items":{"type":"string"}},
                     "refs":{"type":"array","items":{"type":"object",
                       "required":["target","role"],"additionalProperties":false,
                       "properties":{"target":{"type":"string"},
                                     "role":{"enum":["dependence","mention","evidence"]}}}}}}}}}}}
```

The adapter asserts `len(candidates) == VS_K` after repair; a schema-invalid reply is fed back with the validator error, retried `RETRY_MAX` times, and then **the cycle is dropped and logged** (§9:344) — not the submission dropped and the run continued, which is `src/creib/forge/mini/runner.py`'s behaviour.

**Pack renderer** (`llm/packs.py::render(spec) -> Pack(text, digest, manifest)`, §9:340). Pure deterministic function of `(state, blobs, spec, config)`. Section order is stable-before-volatile: problem → compressed criteria → pinned Popper battery → target artifact → top-N attackers/defenders → neighbourhood (born-connected). Bounded by `PACK_TOKEN_BUDGET`; truncation removes **whole sections**, lowest-priority first, and writes an explicit elision marker — never mid-token — so pack bytes are reproducible and the fixture key is stable. Negative case law is never rendered (§11.5) — at P1 there is none, and the renderer has no code path that could. **The manifest** is the instrument: an ordered list of `{"section","artifact_id","view","fields","truncated"}` recording exactly which artifacts and which fields this invocation actually saw. It is stored as a blob and referenced from the event's `llm.pack_manifest_ref`. This discharges `docs/reviews/multi-cycle-research-contract-2026-09-14.md:19` as a harness output.

**Anti-relapse** (`guards/anti_relapse.py`, §3:189-195), MANDATORY before every Conj commit:
- *Stage 1 (hash):* candidate id equals the id of an existing **refuted** artifact ⇒ block. Meaningful only because `seq` is out of the id.
- *Stage 2:* absent at P1; fails open; logs `{"stage":2,"status":"unavailable","reason":"embedder role not configured"}`.
- *Stage 3 (battery equivalence):* candidate's verdict vector over the active battery equals a refuted prior's (`≈_B`) ⇒ block **unless** the candidate carries a warrant against that prior's refuter. Verdicts differ ⇒ admit and log the near miss.
- Blocking occurs **only** for relapse onto refuted-equivalents. Near-duplicates of *accepted* artifacts are never blocked (§3:195) — a test asserts it, because blocking them would be a diversity gate adjudicating.

**Pareto retention** (`measures/pareto.py`, §11.7, attention and reporting only). Axis-generic: `frontier(items, axes)` where each axis value is an integer or an integer triple and comparison is by cross-multiplication. `PARETO_AXES` is a config knob; the **P1 default profile** sets `("coverage","conn","attack_survival")` — all computable at P1 — because the §11.7 default axes `HV_B` and reach require the variator and cross-evaluation, which are P2. Declared in `DIVERGENCES.md`. `coverage(a) = {num: #criteria of addressed problems with a pass verdict, den: #criteria}`; `attack_survival(a) = #warranted attacks on a that are themselves refuted`; `conn(a) = #accepted dependence edges a participates in`. An artifact off the frontier is unfunded, never demoted.

**Views.** `views/theory.py::theory(state, id) -> str` walks `refs ∪ dep` closure and renders narrative + postulates + derivation DAG + per-component verdict history + open attack surface + measure profile — a deterministic function of the graph (§8:328). `views/why.py::why(state, id) -> str` prints the attack/defence chain justifying the status from grounded semantics. `views/prose.py::prose(state, id)` renders the `body` projection for non-skeleton content and raises a declared `P5` not-implemented for skeleton codec (the summarizer path).

### Fixture / replay strategy — every test before Wave 7 is offline

`llm/rawstore.py`:

```python
def raw_key(*, role: str, model: str, endpoint: str, temperature_milli: int,
            schema_id: str, pack_sha256: str, vs_k: int) -> str
    # sha256(canonical({"endpoint","model","pack_sha256","role","schema_id",
    #                   "temperature_milli","vs_k"}))
```

Provider identity, model, endpoint and temperature are **in the key**, so two arms differing only in model can never collide on one raw — the preservation `AGENTS.md` requires ("provider identity, settings, configurations"). Temperature is an integer in thousandths; no floats. Records live at `tests/deepreason/fixtures/raws/<key>.json`:

```json
{"key":"<64hex>","role":"…","model":"…","endpoint":"…","temperature_milli":0,
 "schema_id":"…","pack_sha256":"…","raw":"<verbatim provider text>",
 "recorded_by":"operator|provider","occurrence":"<id|null>","recorded_at":"…"}
```

`recorded_by` is load-bearing: an operator-authored fixture is never mistaken for provider evidence.

`llm/adapter.py::build_adapter(config, blob_store, *, mode="replay", tape=None) -> Adapter` — the §15:531 entry point. Modes:
- **`replay` (default)** — serves raws from the tape; a miss raises `DR_RAW_NOT_RECORDED`. It never opens a socket; there is no fallthrough.
- **`record`** — the only mode that touches the network; writes prompt, pack manifest and raw to blobs and appends to the tape.
- **`mock`** — deterministic canned candidates for unit tests.

### Live adapter (Wave 7): DeepSeek + Ollama, OpenAI-compatible

`llm/endpoints.py` defines one interface, two implementations, one gate:

- **`gate.py::LIVE_SLOTS = threading.BoundedSemaphore(5)`** — a single process-wide ceiling of five concurrent live requests across **both** families (`AGENTS.md`: "At most five live config tests concurrently"; `PROTOCOL.md`: "At most five independent requests may be active in one coordinator process"). Every live call acquires it. The DeepSeek path then additionally passes through `provider._SLOTS` internally, which is harmless: acquisition order is always `LIVE_SLOTS → provider._SLOTS`, at most five holders, no deadlock, and the effective ceiling is five. A test starts six threads and asserts the sixth blocks.
- **`DeepSeekEndpoint`** wraps `src/minireason/provider.py`'s `DeepSeek` **unchanged**. It already reads `DEEPSEEK_API_KEY` from the environment at call time (`provider.py:100`), refuses to send when the credential appears in prompt content (`:120-123`, status `SECRET_IN_REQUEST`), redacts an echoed key in returned content, records `reasoning_content_persisted: False` (`:157`), and writes a write-once request/response record. `Settings.__post_init__` (`:66-69`) hard-refuses any base URL or model other than DeepSeek Flash, so this endpoint is bound to that family by construction and we do not touch it.
- **`OpenAICompatEndpoint`** (new, in-package) for Ollama cloud and any OpenAI-compatible `/v1/chat/completions` host. Config supplies `base_url`, `model`, `family`, and `key_env` — **a variable name, never a key**. The key is read from `os.environ[key_env]` at call time only, is never stored in config, in a record, in a blob, or in the log. Before sending, the payload and coordinate are scanned and a hit raises `DR_SECRET_IN_REQUEST` with a written refusal record. Returned text has any occurrence of the key replaced with `[REDACTED_CREDENTIAL]` and `credential_redaction: true` recorded. Hidden reasoning is never persisted. Records use schema `deepreason.call.v1` with the same fields as `minireason.call.v1` plus `family`.
- **Cross-family rule (§9:338), enforced in `build_adapter`:** if the `judge` role is configured at all, it MUST map to ≥2 endpoints with distinct `family` values, else `DR_JUDGE_FAMILY_RULE`. The `argumentative_critic` for artifact `a` is selected deterministically as the configured critic endpoint whose `family` differs from the family of `a`'s conjecturer endpoint, tiebreak lexicographic by endpoint id; if no foreign family is configured, the sole endpoint is used and a `foreign_reviewer_unavailable` note is written into the event. At P1 no judge is configured (no rubric commitments exist — see the standard-resolution rule in §6), so the judge clause is enforced-if-present.
- **Keys only from env:** `Config` has no field that holds a credential. `config.render()` prints `key_env` names. A test asserts `Config.to_dict()` contains no value read from `os.environ` and that no field name matching `/key|token|secret/i` carries a non-name value.

---

## 6. H005 on the new engine

H005's `material.json` (schema `minireason.h005.material.v1`, published) is consumed **unmodified** and its sha256 pinned in the run record. Verified contents: four metric-free problems (`daily`, `physics`, `philosophy`, `sociology`) and three topologies with these exact node graphs and views —

| Topology | Nodes (in order) | `inputs` as `(source, view)` |
|---|---|---|
| `fork5` (5) | account, objection, rival, response, carry | account ←(previous,both); objection ←(account,both); rival ←(account,**body**); response ←(account,both)(objection,both)(rival,both); carry ←(response,both)(account,**commitments**)(objection,**commitments**)(origin,both) |
| `return6` (6) | reopen, challenge, reply, critique, amend, carry | reopen ←(previous,both); challenge ←(reopen,**commitments**); reply ←(reopen,both)(challenge,both); critique ←(challenge,both)(reply,both)(previous,**commitments**); amend ←(reply,both)(critique,both); carry ←(amend,both)(challenge,**commitments**)(origin,both) |
| `weave7` (7) | body_route, commitment_route, cross, body_return, commitment_return, join, carry | body_route ←(previous,**body**); commitment_route ←(previous,**commitments**); cross ←(body_route,both)(commitment_route,both); body_return ←(body_route,both)(cross,both); commitment_return ←(commitment_route,both)(cross,both); join ←(body_return,both)(commitment_return,both)(previous,**commitments**); carry ←(join,both)(cross,**commitments**)(origin,both) |

(Earlier drafts of this design mis-stated `weave7` as lacking `body_return`/`commitment_return` and mis-assigned several node names; the table above is read directly from the frozen material.)

**Mapping, introducing no type (§0:30).**

1. **Problems.** Each of the four registers as a §1 `Problem` with `provenance.trigger = "seed"` and `criteria` = the auto-pinned Popper battery only. No scoring commitment is pinned: the contract forbids an answer key and `AGENTS.md` forbids a scalar meter.
2. **Templates are scheduler programs, not ontology.** `h005/driver.py` reads the node DAG and emits a deterministic sequence of Conj/Crit calls with explicit `PackSpec`s. One complete template invocation = one cycle; the final `carry` node's artifact is the cycle's contribution; a sibling branch is not a cycle (PROTOCOL).
3. **Rule assignment.** **Crit**: `objection`, `challenge`, `critique`, `cross`. **Conj**: every other node (`account`, `rival`, `reopen`, `reply`, `amend`, `response`, `body_route`, `commitment_route`, `body_return`, `commitment_return`, `join`, `carry`). **Adj** runs after every registration, not once per cycle.
4. **`view` is a §8 view, not a port type.** `views/projection.py::project(view, artifact, blobs, commitments) -> str` with `view ∈ {"body","commitments","both"}` — `body` renders `content_ref` bytes under `codec`; `commitments` renders the artifact's `interface.commitments` as commitment objects (`eval`, `budget`, `observation_valued`) plus the authored surface bytes, and nothing of the body; `both` renders both with a stable separator. Every projection is headed by the artifact id. **Absence invariant:** when a source is unavailable at a coordinate, the renderer emits *"source absent at this coordinate"* and never *"no such thing existed"* — the material's own `system` field demands this, and a test asserts the exact string in both branches. This is the single function H005 is blocked on today.
5. **Source resolution.** `previous` → the prior cycle's `carry` artifact id; `origin` → the chain's cycle-1 first-node artifact when registered, else the seed problem record (PROTOCOL: "the original cycle's completed account when available", "on cycle two, the origin can be the same artifact as the previous completion"). The resolution taken is recorded in the pack manifest, so the trace preserves the fact rather than the assumption.
6. **Two-call protocol, genuinely.** Call 1 renders the node pack and returns the **body**; call 2 sees the node's own body plus only the ports the node declares, and returns the **commitment surface**. `independent_commitment_call` is therefore `true` by construction. Note the frozen default already allows this (`src/creib/forge/mini/kinds.py:71` `commitment_call: str = "two"`), while the current helper sets `'single'` (`tools/multicycle_commitment_study.py:147`) and mints a per-binding `'Explicit field projection'` pseudo-kind (`:168`) whose body is a helper-authored string — the inversion §0:29 forbids.
7. **Envelope failure killed at source.** A node's reply is schema-validated JSON (`{"body":str,"commitments":str}`) with bounded repair; a malformed reply logs `FORMAT_FAILURE` and **drops the cycle**. The published erratum's `commitments_sha256 = e3b0c442…` (the sha256 of the empty string, `docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md`, arising at `tools/multicycle_commitment_study.py:329-341`) cannot recur, because there is no branch that turns an unparseable envelope into an empty commitment field. Occurrence-01 stays frozen and its review stands; this engine runs **occurrence-02**, separately identified, never a repair of occurrence-01.
8. **Artifact shape per node.** `content_ref` = blob of `{"body":…, "commitments":…}`, `codec: "json"`, both strings the model's own bytes written once. `interface` is built by the arm's compiler.

### FCL-1 as a content convention (the §10.1 precedent), compiled at registration before id computation

`h005/fcl1.py::compile(document, node_id, label_map) -> CompiledSurface`. The reduction, checked row by row against the material's `formal_instruction` and spec §1:

| FCL-1 element | Verdict | Mapping |
|---|---|---|
| `type: "claim"` | **drop** | Every artifact is a claim; the marker adds nothing |
| `type: "commitment"` + `scope`/`action`/`consequence`/`grounds` | **keep — this is the language** | One §1 `Commitment` per record: `eval = "predicate:fcl1_record_wf(<surface-blob-sha256>,<local-id>)"`, `budget {"steps":100000,"time_ms":2000}`, `observation_valued: false` (or `true` when the record asserts a fact about the world, §12). The predicate is genuinely program-checkable: the named record exists in the pinned surface blob, is well-formed, and carries a non-empty scoped `action`/`consequence`. Its *substantive* obligation is not machine-checkable before §10 — declared in `DIVERGENCES.md` and in the pre-registration, not hidden |
| `depends: [Ref]` | **drop the concept, keep the notation** | `interface.refs[].role = "dependence"` — a real `dep` edge, so the support cascade is live for H005 |
| `mentions: [Ref]` | **drop, map** | `refs[].role = "mention"`, explicitly non-load-bearing |
| `type: "objection"` + `target` + `grounds`/`bearing` | **drop as a type** | Register ν artifact (content = `grounds` + `bearing` bytes) + `Warrant{target, type:"argumentative", commitment:null, verdict:null, validity_node:ν}` + `carry(critic_artifact, warrant)` ⇒ a computed `att` edge. This is strictly more than FCL-1 offers, because ν is itself attackable — `return6`'s `critique → challenge` becomes Lemma 3.1 in pass 1 |
| `type: "use"` | **drop as a type** | `refs[].role = "mention"` |
| `type: "problem"` | **keep** | A §1 `Problem` via Spawn, `trigger: "successor"`, `from: [node artifact id]` |
| `revises: [Ref]` | **drop as an assertion** | Successor artifact with a `dependence` ref to the revised artifact plus an argumentative warrant against it. Nothing is deleted (D8) |
| `withdraws: [Ref]` | **drop as an assertion** | The author's artifact carries an argumentative warrant against its own earlier artifact. Self-criticism is criticism; legitimate under N1 |
| `uptake: [Ref]` | **drop from the mechanism** | A self-declared standing label; §0:32 says status is computed, never stored. Rendered and reported only (the §10.1 `prose_notes` precedent: "rendered, never adjudicated"), never an input to §4 |

**Reference resolution.** `exposed-artifact-label#local-ID` resolves only through the `label_map` the pack manifest recorded for *that node* — i.e. only labels actually exposed to it. A reference to an unexposed label mints no ref and is recorded as unresolved; the harness never invents an id (the material forbids it). The `refs-resolve` battery commitment then returns `fail`, which is a demonstrative warrant — real, program-grounded criticism.

**Malformed FCL-1.** The surface is retained verbatim as the commitments blob; the artifact registers with the prose-arm mapping and an `fcl1-wf` `fail` verdict ⇒ demonstrative warrant. Never repaired, never reconstructed.

### The arms, and the pre-registered contrast

Both Mini arms receive **real §1 Commitment objects**; they differ in *carrier*, not in whether a mechanism exists:

- **`mini_fcl`**: battery (`surface-nonempty`, `no-body-duplication`, `refs-resolve`) + one `fcl1_record_wf` Commitment per commitment record + derived `dependence`/`mention` refs + derived ν/warrant/`att` edges from objections.
- **`mini_prose`** and **`matched`**: battery (`surface-nonempty`, `no-body-duplication`) + one `prose_surface_present(<surface-blob-sha256>)` Commitment. `no-body-duplication` is a deterministic program with a declared normalised-overlap criterion — it exists because the H003/H004 helper duplicated prose into body and commitments, which the contract names as the defect to fix.

Both arms are therefore **demarcated** under §6:244 (`crit(a) ⇔ interface.commitments ≠ ∅`), which is exactly the repair of the rejected design's empty-interface prose arm. The prose arm mints **no derived refs and no derived `att` edges**, because §0:30 and FCL-1 both forbid inferring dependence from prose or lexical overlap and the material forbids inventing relations. **That asymmetry is the measured condition of the comparison and is the language's claimed contribution; it is never to be reported as a defect of prose** (`PURPOSE.md`: prose conjectures and criticisms have the same semantic legitimacy as formal ones; syntax and executable tests cannot be made the definition of bearing). It must be pre-registered before any live call — see §8.

**Rubric bar (binding).** No `eval: "rubric:<spec-id>"` commitment may be registered until a **registered standard artifact** exists for that spec-id (§1, §2). §10 is P5. Therefore every H005 commitment at P1 is `program:` or `predicate:`, or it is not registered as a commitment at all.

---

## 7. WAVE PLAN

```json
{
  "package": "src/deepreason",
  "gates": [
    {"after_wave": 3, "name": "P0", "condition": "tests/deepreason/test_p0_*.py all green; zero LLM calls; zero bytes copied from any upstream repository. M401 also lands in this wave: it is declarative role/schema content with no runtime LLM path and is not part of the gate condition"},
    {"after_wave": 5, "name": "P1-offline", "condition": "tests/deepreason/test_p1_acceptance.py green under adapter mode=replay with the committed tape; no socket opened by the suite"},
    {"after_wave": 6, "name": "H005-offline", "condition": "all three topologies compile and run end-to-end on replayed raws with material.json unmodified"}
  ],
  "modules": [
    {
      "id": "M000",
      "wave": 0,
      "path": "src/deepreason/__init__.py, src/deepreason/errors.py, src/deepreason/canon.py, src/deepreason/types.py, src/deepreason/{ontology,log,storage,adjudication,commitments,rules,guards,measures,unification,views,llm,h005,cli}/__init__.py, tests/deepreason/__init__.py",
      "purpose": "Skeleton every other module imports: package init and sub-package re-export stubs (written once and frozen so no later agent edits a shared file), the single error type and its frozen code list, canonical JSON over the float-free profile, sha256 helpers, integer-rational helper, and the shared string enums.",
      "public_interface": [
        "class DeepReasonError(Exception): def __init__(self, code: str, message: str) -> None; .code: str; .message: str",
        "errors.CODES: tuple[str, ...] = ('DR_CANONICAL_PROFILE','DR_ID_MISMATCH','DR_EVENT_SEQUENCE','DR_EVENT_CHAIN','DR_LOG_READONLY','DR_BLOB_MISMATCH','DR_OBJECT_CONFLICT','DR_DEP_CYCLE','DR_UNREGISTERED_WARRANT','DR_SCHEMA_INVALID','DR_UNKNOWN_KNOB','DR_RAW_NOT_RECORDED','DR_SANDBOX_ABORT','DR_RELAPSE_BLOCKED','DR_RUBRIC_STANDARD_UNRESOLVED','DR_PROJECTION_VIEW_UNKNOWN','DR_FCL1_MALFORMED','DR_LIVE_DISABLED','DR_SECRET_IN_REQUEST','DR_JUDGE_FAMILY_RULE','DR_FORMAT_FAILURE')",
        "canon.canonical_bytes(value: Any) -> bytes  # sort_keys=True, separators=(',',':'), ensure_ascii=False, utf-8; raises DR_CANONICAL_PROFILE on float or non-profile value; lists never reordered",
        "canon.canonical_text(value: Any) -> str",
        "canon.sha256_hex(data: bytes) -> str  # 64 lowercase hex, no prefix",
        "canon.content_hash(value: Any) -> str  # sha256_hex(canonical_bytes(value))",
        "canon.blob_ref(data: bytes) -> str",
        "canon.rational(num: int, den: int, k: int | None = None) -> dict  # {'num','den','k'}",
        "canon.rat_cmp(a: dict, b: dict) -> int  # cross-multiplication, integers only",
        "types.CODECS: tuple[str, ...] = ('utf8','json','csv','f64le','i64le','raw')",
        "types.is_codec(value: str) -> bool  # members of CODECS or 'code:<lang>'",
        "types.REF_ROLES = ('dependence','mention','evidence')",
        "types.WARRANT_TYPES = ('demonstrative','argumentative')",
        "types.PROVENANCE_ROLES = ('conjecturer','critic','variator','synthesizer','seed','import','user')",
        "types.RULES = ('Conj','Crit','Adj','Spawn','Refl','Register','Merge','Measure','Reveal','Reseed')",
        "types.SPAWN_TRIGGERS = ('seed','successor','discrimination','remove-arbitrariness','explanation-debt','audit-critic','connection','integration')",
        "types.LABEL0 = ('accepted','refuted','suspended')",
        "types.STATUS = ('accepted','refuted','suspended','suspended_unsupported')",
        "types.VERDICTS = ('pass','fail','overrun')",
        "types.VIEWS = ('body','commitments','both')",
        "class types.BlobReader(Protocol): def get(self, ref: str) -> bytes"
      ],
      "depends_on": [],
      "tests": ["tests/deepreason/test_canon.py: asserts key-sorted compact UTF-8 output on nested fixtures; float at any depth raises DR_CANONICAL_PROFILE; list order preserved; sha256_hex returns 64 lowercase hex with no prefix; rat_cmp orders 1/3 < 1/2 without floats; known-answer vectors for content_hash pinned in the test file"],
      "acceptance": "canonical_bytes({'b':1,'a':[2,1]}) == b'{\"a\":[2,1],\"b\":1}'; canonical_bytes({'x':1.0}) raises DeepReasonError with code DR_CANONICAL_PROFILE; every sub-package imports cleanly with no other module present.",
      "est_size": "S",
      "touches_frozen": false
    },
    {
      "id": "M001",
      "wave": 0,
      "path": "src/deepreason/config.py",
      "purpose": "The §15 typed config: exactly the 22 knob rows plus per-role endpoint seats, frozen-dataclass defaults, partial-YAML/JSON profile loading with unknown-knob rejection, and the effective-configuration renderer. No credential ever lives here.",
      "public_interface": [
        "@dataclass(frozen=True) class RoleSeat: role: str; endpoint_id: str; model: str; temperature_milli: int",
        "@dataclass(frozen=True) class Endpoint: endpoint_id: str; family: str; base_url: str; model: str; key_env: str | None",
        "@dataclass(frozen=True) class Config: FLOOR:int=1; K:int=4; INTEGRATION_BUDGET_SHARE:dict=rational(3,10); HV_MIN:dict|None=None; HV_K:int=8; PRECEDENT_K:int=4; TRIAL_PARAPHRASE_N:int=2; JUDGE_ERR_MAX:dict|None=None; AUDIT_PERIOD:int=30; USER_RULINGS_BUDGET:int=2; HOLDOUT_SHARE:dict=rational(2,10); N_SCHOOLS:int=3; STANCE_DECAY:str='none'; XEXAM_SHARE:dict=rational(15,100); RESEED_DIST_MIN:dict|None=None; NEAR_DUP_EPS:dict|None=None; VS_K:int=4; PARETO_AXES:tuple=('coverage','conn','attack_survival'); LAMBDA_FLOOR:dict|None=None; CAPTURE_W:int=20; PACK_TOKEN_BUDGET:int=2500; RETRY_MAX:int=2; endpoints:tuple[Endpoint,...]=(); seats:tuple[RoleSeat,...]=()",
        "Config.to_dict(self) -> dict  # float-free, canonical-profile clean",
        "Config.digest(self) -> str",
        "config.load(path: str | None = None) -> Config  # partial profile; unknown top-level knob or unknown role-seat field raises DR_UNKNOWN_KNOB",
        "config.render(config: Config) -> str  # complete effective configuration, key_env names only"
      ],
      "depends_on": ["M000"],
      "tests": ["tests/deepreason/test_config.py: the set of Config field names equals exactly the §15:536-560 knob table plus {'endpoints','seats'}; an unknown top-level knob raises DR_UNKNOWN_KNOB; an unknown role-seat field raises; a partial profile inherits every omitted default; to_dict() passes canonical_bytes without raising; no field value is ever read from os.environ and no field name matching /key|token|secret/i holds anything but an env-var NAME"],
      "acceptance": "load() with no path returns defaults; load(profile with {'VS_K': 6}) returns VS_K==6 and every other default unchanged; load(profile with {'VS_KK': 6}) raises DR_UNKNOWN_KNOB; render(load()) prints 22 knob rows.",
      "est_size": "M",
      "touches_frozen": false
    },
    {
      "id": "M002",
      "wave": 0,
      "path": "tests/deepreason/test_boundaries.py",
      "purpose": "Mechanically enforce hard constraint 1 and the two-engine boundary: the new package imports nothing from the frozen engine, and the frozen trees are byte-unchanged.",
      "public_interface": ["(test module only; no importable API)"],
      "depends_on": ["M000"],
      "tests": ["tests/deepreason/test_boundaries.py: walks every .py under src/deepreason, parses with ast, and asserts no Import/ImportFrom names creib, creib.*, minireason.language_mini, minireason.inquiry_mini, minireason.reason_use_mini or minireason.successor_mini (minireason.provider is allowed ONLY inside src/deepreason/llm/endpoints.py); recomputes a sorted sha256 tree hash over src/creib/forge/mini/**.py and the four frozen *_mini.py modules and compares it with the constant pinned in the test file; asserts no file under experiments/records, experiments/plans or experiments/diagnostics/H005-open-prose-commitments/occurrence-01 is writable by the suite (no test fixture path resolves inside them)"],
      "acceptance": "Adding `from creib.forge.mini.log import BlobStore` anywhere under src/deepreason fails this test; editing one byte of src/creib/forge/mini/log.py fails this test.",
      "est_size": "S",
      "touches_frozen": false
    },
    {
      "id": "M100",
      "wave": 1,
      "path": "src/deepreason/ontology/{artifact,commitment,warrant,problem,state}.py",
      "purpose": "The §1 records as frozen dataclasses with exact id computation, jsonschema validation, and the EpistemicState view plus its canonical state_record/state_digest projection. Untyped by construction: no kind field anywhere.",
      "public_interface": [
        "@dataclass(frozen=True) class Ref: target: str; role: str",
        "@dataclass(frozen=True) class Interface: commitments: tuple[str,...]; refs: tuple[Ref,...]",
        "@dataclass(frozen=True) class Provenance: role: str; school: str | None; event_seq: int",
        "@dataclass(frozen=True) class Artifact: id: str; content_ref: str; codec: str; interface: Interface; warrants: tuple[str,...]; provenance: Provenance",
        "Artifact.compute_id(content_ref: str, codec: str, interface: Interface) -> str  # sha256(canonical({'codec','content_ref','interface'}))",
        "Artifact.to_dict(self) -> dict; Artifact.from_dict(d: Mapping) -> 'Artifact'",
        "@dataclass(frozen=True) class Commitment: id: str; eval: str; budget: dict; observation_valued: bool  (+ compute_id(eval, budget, observation_valued), to_dict, from_dict)",
        "@dataclass(frozen=True) class Warrant: id: str; target: str; type: str; commitment: str | None; verdict: str | None; trace_ref: str | None; validity_node: str  (+ compute_id(...), to_dict, from_dict)",
        "@dataclass(frozen=True) class Problem: id: str; description: str; criteria: tuple[str,...]; provenance: dict  (+ compute_id(...), to_dict, from_dict)",
        "@dataclass(frozen=True) class EpistemicState: artifacts: Mapping[str, Artifact]; problems: Mapping[str, Problem]; commitments: Mapping[str, Commitment]; warrants: Mapping[str, Warrant]; carry: frozenset[tuple[str,str]]; att: frozenset[tuple[str,str]]; dep: frozenset[tuple[str,str]]; addr: frozenset[tuple[str,str]]; status: Mapping[str,str]; hv: Mapping[str,dict]; reach: Mapping[str,dict]; conn: Mapping[str,int]",
        "state.state_record(s: EpistemicState) -> dict  # total, sorted, float-free; ts never present",
        "state.state_digest(s: EpistemicState) -> str",
        "ontology.validate(kind_name: str, record: Mapping) -> None  # jsonschema; raises DR_SCHEMA_INVALID"
      ],
      "depends_on": ["M000"],
      "tests": ["tests/deepreason/test_ontology.py: 'kind' not in Artifact.__dataclass_fields__ and never in to_dict(); id is stable across two constructions with different provenance.event_seq and different warrants tuples; id CHANGES when ref order changes (declared rule); every codec in types.CODECS plus 'code:lean' validates and 'code' alone does not; a ref role outside REF_ROLES raises DR_SCHEMA_INVALID; round-trip to_dict/from_dict is byte-identical under canonical_bytes; state_record of an empty state is canonical and contains no 'ts' key at any depth"],
      "acceptance": "Artifact.compute_id('abc','utf8',Interface((),())) equals the hex pinned in the test; two artifacts identical in content_ref/codec/interface but differing in provenance.event_seq share one id.",
      "est_size": "M",
      "touches_frozen": false
    },
    {
      "id": "M101",
      "wave": 1,
      "path": "src/deepreason/log/{event_log.py,chain.py}",
      "purpose": "Append-only JSONL event log over plain canonical dicts (it knows no ontology), with seq contiguity 0..N-1, a per-event hash chain, write-side-only torn-tail repair, and a physically read-only historical open.",
      "public_interface": [
        "chain.event_digest(event_without_id: Mapping) -> str  # sha256(canonical_bytes(event minus 'event_id'))",
        "chain.header_digest(header: Mapping) -> str",
        "chain.verify(events: Sequence[Mapping], header: Mapping) -> None  # raises DR_EVENT_SEQUENCE or DR_EVENT_CHAIN",
        "class EventLog: def __init__(self, root: str, *, read_only: bool = False, header: Mapping | None = None) -> None",
        "EventLog.append(self, partial: Mapping) -> Mapping  # assigns seq, prev, event_id; returns the stored event; raises DR_LOG_READONLY when read_only",
        "EventLog.read(self) -> Iterator[Mapping]  # verifies seq and chain on every line",
        "EventLog.read_until(self, seq: int) -> Iterator[Mapping]",
        "EventLog.length(self) -> int",
        "EventLog.header(self) -> Mapping"
      ],
      "depends_on": ["M000"],
      "tests": ["tests/deepreason/test_event_log.py: a renumbered, internally consistent rewrite of history is caught by the chain though seq is contiguous; a one-byte flip in event n breaks event n's own id and event n+1's prev; a gap, a duplicate seq and an out-of-order append each raise DR_EVENT_SEQUENCE; a truncated final line is repaired on a write-side open and RAISES on a read_only open; read_only=True creates no file and no directory (asserted by comparing a recursive directory listing before and after)"],
      "acceptance": "A 50-event log round-trips; after flipping one byte of line 20, read() raises DR_EVENT_CHAIN naming seq 20; EventLog(root, read_only=True) on a non-existent root raises rather than creating it.",
      "est_size": "M",
      "touches_frozen": false
    },
    {
      "id": "M102",
      "wave": 1,
      "path": "src/deepreason/storage/{blobs.py,objects.py}",
      "purpose": "Content-addressed write-once blobs with read-back verification, and the §14:505 schema-namespaced object store with conflicting-registration rejection.",
      "public_interface": [
        "class BlobStore: def __init__(self, root: str, *, read_only: bool = False) -> None",
        "BlobStore.put(self, data: bytes) -> str  # returns sha256 hex; O_EXCL create then read back and compare, else DR_BLOB_MISMATCH",
        "BlobStore.get(self, ref: str) -> bytes  # verifies the digest on read",
        "BlobStore.has(self, ref: str) -> bool",
        "class ObjectStore: def __init__(self, root: str, *, read_only: bool = False) -> None",
        "ObjectStore.put(self, schema: str, record: Mapping) -> str  # objects/<schema>/<sha256(record['id'])>.json; identical canonical bytes is idempotent; different bytes for a known id raises DR_OBJECT_CONFLICT",
        "ObjectStore.get(self, schema: str, object_id: str) -> Mapping",
        "ObjectStore.has(self, schema: str, object_id: str) -> bool",
        "ObjectStore.iter_schema(self, schema: str) -> Iterator[Mapping]  # lexicographic by file name",
        "storage.SCHEMAS = ('deepreason.artifact.v1','deepreason.commitment.v1','deepreason.warrant.v1','deepreason.problem.v1')"
      ],
      "depends_on": ["M000"],
      "tests": ["tests/deepreason/test_storage.py: put/get round-trip; a second put of identical bytes is a no-op and returns the same ref; a corrupted blob file makes get raise DR_BLOB_MISMATCH; registering id X under one schema with bytes A and then bytes B raises DR_OBJECT_CONFLICT and leaves bytes A on disk; registering the same id under two different schemas raises; read_only=True writes nothing"],
      "acceptance": "objects/deepreason.artifact.v1/<sha256(id)>.json exists after put and its bytes equal canonical_bytes(record); a conflicting put raises and the directory listing is unchanged.",
      "est_size": "M",
      "touches_frozen": false
    },
    {
      "id": "M103",
      "wave": 1,
      "path": "src/deepreason/adjudication/{graph.py,grounded.py,support.py}",
      "purpose": "The §4 core as pure graph functions over ids: deterministic toposort with cycle detection, the Kleene least fixed point of F, pass-1 labels, and the pass-2 support cascade. Reads att and dep and nothing else.",
      "public_interface": [
        "graph.toposort(nodes: Iterable[str], dep: Iterable[tuple[str,str]]) -> list[str]  # Kahn over a lexicographic min-heap; raises DR_DEP_CYCLE naming one cycle",
        "graph.has_cycle(nodes: Iterable[str], dep: Iterable[tuple[str,str]]) -> bool",
        "grounded.grounded_extension(nodes: Iterable[str], att: Iterable[tuple[str,str]]) -> frozenset[str]",
        "grounded.label0(nodes: Iterable[str], att: Iterable[tuple[str,str]]) -> dict[str,str]  # values in types.LABEL0",
        "support.final_labels(label0: Mapping[str,str], dep: Iterable[tuple[str,str]]) -> dict[str,str]  # values in types.STATUS"
      ],
      "depends_on": ["M000"],
      "tests": ["tests/deepreason/test_graph.py: toposort is lexicographically deterministic across 100 shuffled input orders; a 2-cycle and a 3-cycle each raise DR_DEP_CYCLE; grounded_extension on the empty graph is empty; a self-attacking node is suspended, not refuted; a 4-chain k1->k2->k3->k4 labels alternately accepted/refuted from the unattacked end; final_labels turns accepted-with-refuted-dependency into suspended_unsupported and never into refuted; grounded.py and support.py import only deepreason.types and stdlib (ast-checked in this test)"],
      "acceptance": "On att={(k,a),(j,k)} with j unattacked, grounded_extension=={j,a}; on dep={(d,x)} with label0[x]=='refuted', final_labels[d]=='suspended_unsupported'.",
      "est_size": "S",
      "touches_frozen": false
    },
    {
      "id": "M104",
      "wave": 1,
      "path": "src/deepreason/adjudication/edges.py",
      "purpose": "Build dep and att from registered record dicts: the dependence rule, the carry base, and the three closures (validity node, case law, evidence) iterated to fixpoint. Operates on the §3 JSON shapes as plain Mappings so it imports no ontology code.",
      "public_interface": [
        "edges.build_dep(artifacts: Mapping[str, Mapping]) -> frozenset[tuple[str,str]]  # role=='dependence', both endpoints registered",
        "edges.build_att(artifacts: Mapping[str, Mapping], warrants: Mapping[str, Mapping], commitments: Mapping[str, Mapping], carry: Iterable[tuple[str,str]], dep: Iterable[tuple[str,str]]) -> frozenset[tuple[str,str]]",
        "edges.normalise_carry(artifacts: Mapping[str, Mapping], warrants: Mapping[str, Mapping], carry: Iterable[tuple[str,str]]) -> frozenset[tuple[str,str]]  # folds the legacy artifact['warrants'] shorthand in exactly once",
        "edges.lineage(dep: Iterable[tuple[str,str]], start: str) -> frozenset[str]  # {start} plus everything start transitively depends on"
      ],
      "depends_on": ["M000"],
      "tests": ["tests/deepreason/test_edges.py: base carry edge appears only when carrier, warrant and target are all registered; an attacker of a validity node attacks EVERY carrier of that warrant, including one added later; a rubric warrant's ν without a mention ref to its standard is rejected as ill-formed; refuting a standard adds an edge to every ν mentioning it and, through C1, to every carrier; an attacker of an artifact three dependence hops below an evidence ref attacks the ν that cites that evidence; the fixpoint terminates on a graph where C2 and C3 feed each other; edges.build_att is order-independent (same frozenset over 50 shuffled input orders)"],
      "acceptance": "Given standard s, ν mentioning s, warrant w(target=t, validity_node=ν), carrier k, and attacker x of s: build_att contains (x,ν) and (x,k); with x unattacked the labels give t=='accepted'.",
      "est_size": "L",
      "touches_frozen": false
    },
    {
      "id": "M105",
      "wave": 1,
      "path": "src/deepreason/commitments/{registry.py,popper.py,predicate.py,program.py,sandbox.py}",
      "purpose": "Deterministic, step-budgeted commitment evaluation: the τκ registry, the three Popper-battery programs, the predicate evaluator, and §1:80-88 oracle isolation for untrusted code.",
      "public_interface": [
        "@dataclass(frozen=True) class Verdict: verdict: str; steps: int; trace: dict; sandbox_abort: bool = False  # verdict in types.VERDICTS",
        "registry.register(name: str, fn: Callable[[Mapping, Mapping, BlobReader, dict], Verdict]) -> None",
        "registry.evaluate(commitment: Mapping, artifact: Mapping, blobs: BlobReader) -> Verdict  # dispatches on eval prefix; 'rubric:' raises DR_RUBRIC_STANDARD_UNRESOLVED unless a registered standard artifact is supplied, which at P1 it never is",
        "registry.battery_vector(commitments: Sequence[Mapping], artifact: Mapping, blobs: BlobReader) -> tuple[str, ...]  # the ≈_B verdict vector, ordered by commitment id",
        "popper.POPPER_BATTERY: tuple[dict, ...]  # three commitment records: surface-nonempty, refs-resolve, no-self-dependence, each eval 'program:<name>@<params-hash>'",
        "popper.pin(problem_criteria: Sequence[str]) -> tuple[str, ...]  # auto-pins the battery ids, idempotent",
        "predicate.evaluate(expr: str, artifact: Mapping, blobs: BlobReader, budget: Mapping) -> Verdict  # closed grammar: named predicates with literal arguments only; no eval(), no import",
        "program.run_isolated(module_source: str, entry: str, payload: Mapping, budget: Mapping) -> Verdict  # fresh subprocess, deterministic step tracer installed BEFORE module top-level code runs, OS memory/CPU ceilings and a parent watchdog as containment only",
        "sandbox.SandboxAbort  # containment signal: surfaced as Verdict(verdict='overrun', sandbox_abort=True); mints no warrant, never cached"
      ],
      "depends_on": ["M000"],
      "tests": ["tests/deepreason/test_commitments.py: a program exceeding its step budget returns overrun with steps==budget['steps'] and identical results under artificial machine load (time_ms is never consulted — asserted by monkeypatching time to jump an hour mid-run and getting the same Verdict bytes); a containment kill yields sandbox_abort=True, verdict 'overrun', mints no warrant and is absent from the verdict cache; the step tracer is installed before module top-level by a fixture module whose top-level loop would otherwise never terminate; surface-nonempty fails on an artifact with interface.commitments == () and passes otherwise; refs-resolve fails on a dangling target; no-self-dependence fails on a dependence ref to self; an eval starting 'rubric:' raises DR_RUBRIC_STANDARD_UNRESOLVED; battery_vector is ordered by commitment id and stable"],
      "acceptance": "Two runs of the whole test module produce byte-identical Verdict.trace canonical bytes; a forbid-nothing artifact is refuted by a program, not by a measure.",
      "est_size": "L",
      "touches_frozen": false
    },
    {
      "id": "M200",
      "wave": 2,
      "path": "src/deepreason/harness.py",
      "purpose": "The registration and replay hub: append events, materialise S, reject dep cycles and unregistered warrants before appending, re-adjudicate after every registration, record the state digest on every Adj event, and provide read-only time travel.",
      "public_interface": [
        "class Harness: @classmethod def create(cls, root: str, config: Config) -> 'Harness'; @classmethod def open(cls, root: str, config: Config) -> 'Harness'",
        "Harness.register_artifact(self, *, content: bytes, codec: str, interface: Interface, provenance_role: str, rule: str = 'Register', inputs: Sequence[str] = ()) -> str",
        "Harness.register_commitment(self, commitment: Commitment) -> str",
        "Harness.register_problem(self, problem: Problem) -> str",
        "Harness.register_warrant(self, warrant: Warrant) -> str  # raises DR_UNREGISTERED_WARRANT if target, validity_node or commitment is unregistered",
        "Harness.carry(self, artifact_id: str, warrant_id: str, *, rule: str = 'Crit') -> None",
        "Harness.address(self, artifact_id: str, problem_id: str) -> None",
        "Harness.spawn(self, problem: Problem) -> str",
        "Harness.adjudicate(self) -> dict[str,str]  # recomputes edges + both passes; appends an Adj event carrying state_diff.digest",
        "Harness.state(self) -> EpistemicState",
        "Harness.append_llm_event(self, *, rule: str, role: str, model: str, endpoint: str, prompt_ref: str, raw_ref: str, pack_manifest_ref: str, tokens: int, ms: int, inputs: Sequence[str], outputs: Sequence[str]) -> Mapping",
        "harness.replay(root: str, config: Config) -> EpistemicState  # verifies every Adj digest en route",
        "harness.at(root: str, config: Config, seq: int) -> EpistemicState  # physically read-only"
      ],
      "depends_on": ["M000", "M100", "M101", "M102", "M103", "M104", "M105"],
      "tests": ["tests/deepreason/test_harness.py: adjudicate() runs after every single registration (asserted by counting Adj events); a registration that would close a dep cycle raises DR_DEP_CYCLE and leaves log length, object count and blob count unchanged; a warrant naming an unregistered target is refused; an artifact carrying the legacy warrants field produces exactly one carry pair; at(root, seq) on a run of 30 events creates no file (recursive listing compared before and after) and equals a truncated replay; replay verifies and would raise on a tampered Adj digest"],
      "acceptance": "state_record(live) canonical bytes == state_record(replay(root)) canonical bytes for a 30-event run; every Adj event's state_diff.digest recomputes on replay.",
      "est_size": "L",
      "touches_frozen": false
    },
    {
      "id": "M201",
      "wave": 2,
      "path": "src/deepreason/views/projection.py",
      "purpose": "The §8 view projection H005 is blocked on: a deterministic body|commitments|both projection of an artifact's own content and interface, with the absence invariant.",
      "public_interface": [
        "@dataclass(frozen=True) class Projection: text: str; artifact_id: str | None; view: str; fields: tuple[str,...]; absent: bool",
        "projection.project(view: str, artifact: Mapping | None, blobs: BlobReader, commitments: Mapping[str, Mapping]) -> Projection  # view not in types.VIEWS raises DR_PROJECTION_VIEW_UNKNOWN; artifact None yields absent=True",
        "projection.ABSENT_TEXT: str = 'source absent at this coordinate'"
      ],
      "depends_on": ["M000"],
      "tests": ["tests/deepreason/test_projection.py: view='commitments' renders the commitment objects and the authored surface bytes and contains NO byte of the body (asserted by a body containing a unique nonce); view='body' contains no commitment id; view='both' contains both with the stable separator; an unknown view raises DR_PROJECTION_VIEW_UNKNOWN; a None artifact renders exactly ABSENT_TEXT and never any phrase asserting non-existence (asserted against a forbidden-substring list including 'did not exist', 'never', 'no such')"],
      "acceptance": "For a json-codec artifact {'body':B,'commitments':C}, project('commitments',…).text contains C and not B; project(view, None, …).text == ABSENT_TEXT and .absent is True.",
      "est_size": "S",
      "touches_frozen": false
    },
    {
      "id": "M202",
      "wave": 2,
      "path": "src/deepreason/views/{theory.py,why.py,prose.py}",
      "purpose": "The §8 deterministic graph views: theory(id) walks refs ∪ dep and renders the full profile; why(id) prints the attack/defence chain justifying the status; prose(id) renders the body view and declares the skeleton path P5.",
      "public_interface": [
        "theory.theory(state: EpistemicState, artifact_id: str, blobs: BlobReader) -> str",
        "why.why(state: EpistemicState, artifact_id: str) -> str  # chain derived from grounded semantics only",
        "prose.prose(state: EpistemicState, artifact_id: str, blobs: BlobReader) -> str  # raises DeepReasonError('DR_SCHEMA_INVALID', 'skeleton prose view is P5') for skeleton codec"
      ],
      "depends_on": ["M000", "M100"],
      "tests": ["tests/deepreason/test_views.py: theory() on the same state twice is byte-identical; theory() of an artifact with a refuted dependency names the dependency and its status; why() of a reinstated artifact prints attacker, defender and the resulting status in that order; why() of a suspended_unsupported artifact names the unsupported dependency rather than an attacker; no view function reads any measure not already in the state"],
      "acceptance": "why(state, a) on the Lemma 3.1 fixture prints j -> k -> a and 'accepted'; theory bytes are stable across two calls and across a replayed state.",
      "est_size": "M",
      "touches_frozen": false
    },
    {
      "id": "M203",
      "wave": 2,
      "path": "src/deepreason/measures/{demarcation.py,pareto.py}",
      "purpose": "§6 demarcation predicates and §11.7 axis-generic Pareto retention over integers and integer rationals. Attention and reporting only; never an input to §4.",
      "public_interface": [
        "demarcation.crit(artifact: Mapping) -> bool  # interface.commitments != ()",
        "demarcation.mod(artifact: Mapping, variator_available: bool) -> bool | None  # None when no variator is configured (P1): unknown, never False",
        "demarcation.active(artifact: Mapping, variator_available: bool) -> bool | None  # crit and mod",
        "pareto.frontier(items: Mapping[str, Mapping[str, int | dict]], axes: Sequence[str]) -> tuple[str, ...]  # maximal, non-dominated, sorted by id; integer/rational comparison only",
        "pareto.coverage(state: EpistemicState, artifact_id: str) -> dict  # {'num','den','k':None}",
        "pareto.attack_survival(state: EpistemicState, artifact_id: str) -> int",
        "pareto.conn(state: EpistemicState, artifact_id: str) -> int"
      ],
      "depends_on": ["M000", "M100"],
      "tests": ["tests/deepreason/test_measures.py: crit is False exactly when interface.commitments is empty; active returns None rather than False when no variator is configured (unknown is not a verdict); frontier of a dominated point excludes it and of a tie includes both; frontier uses no float (a float axis value raises DR_CANONICAL_PROFILE); an ast check asserts adjudication/* never imports measures/*"],
      "acceptance": "frontier({'a':{'coverage':rational(1,2),'conn':2},'b':{'coverage':rational(1,3),'conn':1}}, ('coverage','conn')) == ('a',).",
      "est_size": "M",
      "touches_frozen": false
    },
    {
      "id": "M204",
      "wave": 2,
      "path": "src/deepreason/guards/anti_relapse.py",
      "purpose": "The §3:189-195 registration guard: stage 1 hash, stage 2 declared-unavailable and fail-open, stage 3 battery equivalence, blocking only relapse onto refuted-equivalents.",
      "public_interface": [
        "@dataclass(frozen=True) class Decision: admit: bool; stage: int | None; reason: str; prior_id: str | None; record: dict",
        "anti_relapse.check(candidate: Mapping, *, refuted_ids: frozenset[str], refuted_vectors: Mapping[str, tuple[str,...]], candidate_vector: tuple[str,...], refuters: Mapping[str, frozenset[str]], candidate_warrant_targets: frozenset[str], embedder_available: bool = False) -> Decision"
      ],
      "depends_on": ["M000", "M105"],
      "tests": ["tests/deepreason/test_anti_relapse.py: a candidate whose id equals a refuted artifact's id is blocked at stage 1; stage 2 with embedder_available=False returns a Decision whose record contains {'stage':2,'status':'unavailable'} and does NOT block; a candidate whose battery vector equals a refuted prior's is blocked at stage 3; the same candidate carrying a warrant against that prior's refuter is admitted; a candidate whose id or vector matches an ACCEPTED artifact is always admitted (asserted for both exact-id and exact-vector matches, because blocking those would be a diversity gate adjudicating)"],
      "acceptance": "check() never returns admit=False for any prior whose status is not 'refuted'; every blocked decision carries prior_id and a reason naming the stage.",
      "est_size": "M",
      "touches_frozen": false
    },
    {
      "id": "M205",
      "wave": 2,
      "path": "src/deepreason/unification/isolation.py",
      "purpose": "The §16 P0 scope row's stubbed isolation/integration driver with knobs: conn/iso computation and a ranked neighbour list, with no Spawn wired at P0.",
      "public_interface": [
        "isolation.conn(state: EpistemicState, artifact_id: str) -> int  # accepted dependence edges the artifact participates in",
        "isolation.iso(state: EpistemicState, artifact_id: str, floor: int) -> int  # max(0, floor - conn)",
        "isolation.neighbours(state: EpistemicState, artifact_id: str, k: int) -> tuple[str, ...]  # rank: shared problem > shared refs > id order; NO embedding term at P1",
        "isolation.would_spawn(state: EpistemicState, config: Config) -> tuple[str, ...]  # ids whose iso > 0; returns the list, spawns nothing (stub, P2 wires it)"
      ],
      "depends_on": ["M000", "M100"],
      "tests": ["tests/deepreason/test_isolation.py: conn counts only ACCEPTED dependence edges; iso is 0 when conn >= FLOOR; neighbours is deterministic and respects the documented rank order across shuffled inputs; would_spawn returns ids and appends no event (log length unchanged)"],
      "acceptance": "With FLOOR=1 and an isolated accepted artifact, would_spawn names it and the event log is unchanged.",
      "est_size": "S",
      "touches_frozen": false
    },
    {
      "id": "M206",
      "wave": 2,
      "path": "src/deepreason/h005/fcl1.py",
      "purpose": "The FCL-1 content-convention compiler: a pure function from an authored FCL-1 document to §1 commitments, refs, ν artifacts, warrants and problems, with no new type and no invented reference.",
      "public_interface": [
        "@dataclass(frozen=True) class CompiledSurface: commitments: tuple[dict,...]; refs: tuple[dict,...]; nu_nodes: tuple[dict,...]; warrants: tuple[dict,...]; problems: tuple[dict,...]; uptake_render: str; unresolved: tuple[dict,...]; malformed: bool",
        "fcl1.compile(document_text: str, *, surface_ref: str, node_id: str, label_map: Mapping[str,str]) -> CompiledSurface",
        "fcl1.prose_surface(document_text: str, *, surface_ref: str) -> CompiledSurface  # the symmetric free-prose mapping: one prose_surface_present commitment, zero derived refs",
        "fcl1.BATTERY_EXTRA: tuple[dict, ...]  # the no-body-duplication commitment record, shared by every arm"
      ],
      "depends_on": ["M000", "M100"],
      "tests": ["tests/deepreason/test_fcl1.py: one row per reduction-table entry — commitment->Commitment with predicate eval; depends->dependence ref; mentions->mention ref; objection->ν artifact plus argumentative warrant; use->mention ref; problem->Problem with trigger 'successor'; revises->dependence ref plus argumentative warrant; withdraws->self-directed argumentative warrant; claim and uptake produce NO commitment, NO ref and NO warrant, and uptake appears only in uptake_render; a reference to a label absent from label_map produces an entry in unresolved and NO ref; malformed JSON sets malformed=True, produces the prose mapping and never a repaired document; prose_surface produces exactly one commitment and zero refs"],
      "acceptance": "compile() of the material's own formal_instruction example yields commitments and refs whose canonical bytes are stable across runs; no output record contains a 'kind' or 'type' field.",
      "est_size": "L",
      "touches_frozen": false
    },
    {
      "id": "M300",
      "wave": 3,
      "path": "tests/deepreason/test_p0_adjudication.py, tests/deepreason/test_p0_closure.py, tests/deepreason/test_p0_registration.py, tests/deepreason/test_p0_log.py, tests/deepreason/test_p0_replay.py, tests/deepreason/test_p0_scope.py, tests/deepreason/test_upstream_agreement.py",
      "purpose": "The §16 P0 acceptance suite plus its hardening tests and the skip-by-default upstream cross-check. This module is the P0 gate.",
      "public_interface": ["(test modules only; shared builders live in tests/deepreason/_builders.py written by this module)"],
      "depends_on": ["M200", "M201", "M203", "M205"],
      "tests": ["exactly the table in §4 of the design: grounded correctness (3 cases), reinstatement, support cascade, dep cycle rejection with no write, standard-refutation collapse and reinstatement, replay byte-for-byte with truncated replay and a read-only at(seq); hardening: validity-node closure disabling every carrier, evidence closure, unregistered warrant, conflicting object registration, legacy warrants materialising carry once, log gap/dup/rewind, chain break, torn tail write-side only; scope: no kind field, complete codec enum, Popper battery auto-pinned, isolation knobs with a stubbed driver, why CLI chain, zero LLM calls; test_upstream_agreement.py imports deepreason_upstream.adjudication.grounded if importable and asserts identical grounded extensions on 200 generated graphs, otherwise skipUnless"],
      "acceptance": "PYTHONPATH=src python -X utf8 -m unittest discover -s tests runs the whole repo suite green including these; the P0 run opens no socket (asserted by monkeypatching socket.socket to raise) and copies no upstream byte (M002 still green).",
      "est_size": "L",
      "touches_frozen": false
    },
    {
      "id": "M301",
      "wave": 3,
      "path": "src/deepreason/cli/main.py, tests/deepreason/test_cli.py",
      "purpose": "The §13 CLI verbs reachable at P0/P1, including the four upstream deleted and the config renderer §15 requires.",
      "public_interface": [
        "main.main(argv: Sequence[str]) -> int",
        "verbs: 'frontier' | 'focus <id>' | 'expand' | 'attack <id>' | 'step' | 'why <id>' | 'theory <id>' | 'prose <id>' | 'trace <id>' | 'config' | 'run --budget <spec>'",
        "main.VERBS: tuple[str, ...]  # the tuple above, asserted against §13:497 in the test"
      ],
      "depends_on": ["M200", "M202", "M201", "M203", "M001"],
      "tests": ["tests/deepreason/test_cli.py: every verb in VERBS runs against a fixture root and exits 0; why prints the attack/defence chain; theory prints the §8 view; trace replays and prints per-event lines; config prints the complete effective configuration with key_env NAMES and no value that looks like a credential; a verb requiring an LLM exits non-zero with DR_LIVE_DISABLED under the default replay adapter and an empty tape; the docket/rule/schools/capture/reseed/merge verbs are absent and the help text says which phase each belongs to"],
      "acceptance": "`python -m deepreason.cli.main why <id> --root <fixture>` prints a chain whose final line is the artifact's status; `config` output parses back through config.load without error.",
      "est_size": "M",
      "touches_frozen": false
    },
    {
      "id": "M400",
      "wave": 4,
      "path": "src/deepreason/rules/{conj.py,crit.py,spawn.py,refl.py}",
      "purpose": "The §3:167-186 transition table as pure functions over the harness, including all seven Spawn triggers with §3:179 implemented as written and the counter-argument registered as an attackable Refl artifact.",
      "public_interface": [
        "conj.conj(harness: Harness, adapter: Adapter, problem_id: str, config: Config, guard: Callable) -> tuple[str, ...]  # gated on Π != ∅; born-connected pack; VS_K candidates; every candidate through the guard",
        "crit.crit_program(harness: Harness, artifact_id: str, blobs: BlobReader) -> tuple[str, ...]  # fail -> ν + demonstrative warrant + critic artifact + carry; overrun and sandbox_abort mint nothing",
        "crit.crit_argumentative(harness: Harness, adapter: Adapter, artifact_id: str, config: Config) -> tuple[str, ...]  # relied-on ids become dependence refs on the critic artifact",
        "spawn.scan(state: EpistemicState, config: Config) -> tuple[Problem, ...]  # all seven §3:178-186 triggers; the ones needing P2 measures return () with a logged 'unavailable' note",
        "spawn.RULE_ARTIFACTS: tuple[dict, ...]  # the pass-2 support rule, the §3:179 trigger, and the recorded upstream counter-argument to it, each registered via Refl as an attackable artifact",
        "refl.register_rule_artifacts(harness: Harness) -> tuple[str, ...]"
      ],
      "depends_on": ["M200", "M204", "M105", "M201"],
      "tests": ["tests/deepreason/test_rules.py: conj raises when Π is empty; every returned candidate passed the guard (asserted by a guard spy); a program fail produces exactly one ν, one demonstrative warrant, one critic artifact and one carry pair; an overrun and a sandbox_abort produce none of those; an argumentative critic's relied-on ids appear as dependence refs and withdrawing a premise moves the critic to suspended_unsupported through pass 2 with no special rule; spawn.scan emits a successor problem on a failed verdict (§3:179) and the Refl rule-artifact recording the upstream counter-argument is registered, attackable, and currently unattacked"],
      "acceptance": "A failed verdict produces both a demonstrative warrant and a successor Problem with trigger 'successor'; refuting the §3:179 rule-artifact does not change any label (rules are artifacts, not code paths, at P1) and is recorded.",
      "est_size": "L",
      "touches_frozen": false
    },
    {
      "id": "M401",
      "wave": 3,
      "path": "src/deepreason/llm/{roles.py,schemas.py}",
      "purpose": "Role definitions (template + JSON Schema + temperature + endpoint seat) for the three P1 roles, the declared-unimplemented five, and the VS contract schema.",
      "public_interface": [
        "@dataclass(frozen=True) class Role: name: str; template: str; schema_id: str; temperature_milli: int; implemented: bool",
        "roles.ROLES: Mapping[str, Role]  # conjecturer, argumentative_critic, summarizer implemented; defender, judge, variator, synthesizer, embedder declared not implemented",
        "roles.render_template(role: str, pack_text: str) -> list[dict]  # OpenAI-shaped messages; deterministic",
        "schemas.SCHEMAS: Mapping[str, dict]  # jsonschema documents keyed by schema_id; 'vs.candidates.v1' is the §5 document",
        "schemas.validate(schema_id: str, payload: Mapping) -> None  # raises DR_SCHEMA_INVALID with the validator message",
        "schemas.repair_prompt(schema_id: str, payload_text: str, error: str) -> str"
      ],
      "depends_on": ["M000", "M001"],
      "tests": ["tests/deepreason/test_roles_schemas.py: ROLES covers exactly the eight §9:336 role names; the five unimplemented roles raise a clear error if called; the VS schema rejects a reply with VS_K-1 candidates, a float typicality, an unknown property, and a ref role outside REF_ROLES; render_template is byte-deterministic for a fixed pack; no template contains a negative-case-law section (§11.5)"],
      "acceptance": "schemas.validate('vs.candidates.v1', reply) accepts exactly the §5 shape with integer-rational typicality and rejects a float.",
      "est_size": "M",
      "touches_frozen": false
    },
    {
      "id": "M402",
      "wave": 4,
      "path": "src/deepreason/llm/packs.py",
      "purpose": "The §9:340 deterministic pack renderer with whole-section truncation and the field manifest that records exactly what each invocation saw.",
      "public_interface": [
        "@dataclass(frozen=True) class PackSpec: role: str; problem_id: str | None; target_id: str | None; sources: tuple[tuple[str,str],...]; neighbourhood_k: int; include_battery: bool; token_budget: int",
        "@dataclass(frozen=True) class Pack: text: str; sha256: str; manifest: tuple[dict, ...]  # each {'section','artifact_id','view','fields','truncated'}",
        "packs.render(state: EpistemicState, blobs: BlobReader, spec: PackSpec, config: Config) -> Pack",
        "packs.SECTION_ORDER: tuple[str, ...] = ('problem','criteria','battery','target','attackers','defenders','neighbourhood','sources')",
        "packs.ELISION: str = '[section elided: pack token budget]'"
      ],
      "depends_on": ["M100", "M201", "M203"],
      "tests": ["tests/deepreason/test_packs.py: render is byte-identical across 20 runs and across a replayed state; sections appear in SECTION_ORDER; exceeding the budget drops whole lowest-priority sections and inserts ELISION, never truncating mid-token (asserted by re-parsing every rendered section); the manifest names every artifact id and field actually rendered and nothing else (cross-checked by searching the text for each manifest id and asserting no unlisted id appears); an absent source renders projection.ABSENT_TEXT and is marked absent in the manifest; no negative-case-law section exists in any code path"],
      "acceptance": "For a fixed state and spec, Pack.sha256 is stable; removing one artifact from the state changes both the text and the manifest.",
      "est_size": "L",
      "touches_frozen": false
    },
    {
      "id": "M403",
      "wave": 4,
      "path": "src/deepreason/llm/{rawstore.py,adapter.py,gate.py}",
      "purpose": "The §15:531 adapter entry point with three modes, the provider-identity-carrying raw tape, and the single process-wide five-slot live gate. No network in replay or mock.",
      "public_interface": [
        "rawstore.raw_key(*, role: str, model: str, endpoint: str, temperature_milli: int, schema_id: str, pack_sha256: str, vs_k: int) -> str",
        "class RawTape: def __init__(self, directory: str) -> None; def get(self, key: str) -> Mapping; def put(self, record: Mapping) -> None; def has(self, key: str) -> bool",
        "class Adapter(Protocol): def call(self, role: str, pack: Pack, *, schema_id: str) -> tuple[dict, Mapping]  # returns (validated payload, raw record)",
        "adapter.build_adapter(config: Config, blob_store: BlobStore, *, mode: str = 'replay', tape: RawTape | None = None, endpoints: Mapping | None = None) -> Adapter  # mode in {'replay','record','mock'}; raises DR_JUDGE_FAMILY_RULE when a configured judge seat lacks two distinct families; selects the foreign-family critic deterministically",
        "adapter.ReplayAdapter / adapter.RecordingAdapter / adapter.MockAdapter",
        "gate.LIVE_SLOTS: threading.BoundedSemaphore  # exactly 5 permits, process-wide, acquired by every live call of every family",
        "gate.live_slot() -> ContextManager[None]"
      ],
      "depends_on": ["M000", "M102", "M401"],
      "tests": ["tests/deepreason/test_adapter.py: a replay miss raises DR_RAW_NOT_RECORDED and opens no socket (socket.socket monkeypatched to raise); two keys differing only in model, only in endpoint, or only in temperature_milli are distinct; record mode is the ONLY mode whose code path can reach the network (ast check plus a socket spy); schema-invalid replayed output triggers RETRY_MAX repairs and then raises DR_FORMAT_FAILURE with 'cycle dropped' in the message; build_adapter with a judge seat on one family raises DR_JUDGE_FAMILY_RULE; the argumentative critic selected for an artifact is the lexicographically first configured endpoint of a family different from its conjecturer's; gate.LIVE_SLOTS has exactly 5 permits and a sixth concurrent acquisition blocks"],
      "acceptance": "The whole suite runs with an empty network stack; a recorded raw replays to a byte-identical payload.",
      "est_size": "L",
      "touches_frozen": false
    },
    {
      "id": "M500",
      "wave": 5,
      "path": "src/deepreason/loop.py, tests/deepreason/test_p1_acceptance.py, tests/deepreason/fixtures/raws/*.json",
      "purpose": "The §16 P1 single-problem loop and its acceptance test, fully offline on a committed operator-authored tape. This module is the P1 gate.",
      "public_interface": [
        "@dataclass(frozen=True) class LoopResult: frontier: tuple[str,...]; theory: str; trace: tuple[Mapping,...]; blocked: tuple[Mapping,...]; dropped_cycles: tuple[Mapping,...]",
        "loop.run(harness: Harness, adapter: Adapter, *, problem_id: str, cycles: int, config: Config) -> LoopResult",
        "loop.load_problem_file(path: str) -> Problem  # json: {description, criteria?}; the Popper battery is auto-pinned"
      ],
      "depends_on": ["M400", "M402", "M403", "M204", "M203", "M301"],
      "tests": ["tests/deepreason/test_p1_acceptance.py: point loop.run at tests/deepreason/fixtures/problem_p1.json under adapter mode='replay' and assert (a) LoopResult.frontier is the Pareto frontier of survivors over config.PARETO_AXES and every member is 'accepted', (b) LoopResult.theory is a non-empty deterministic theory render for the top frontier member, (c) LoopResult.trace contains every event of the run in seq order with a pack_manifest_ref on every llm event, (d) a re-submitted refuted candidate appears in LoopResult.blocked with stage 1 or 3 named, (e) a γ-call yields exactly config.VS_K schema-valid candidates, (f) the whole test opens no socket, (g) replay of the run's log reproduces the state bytes"],
      "acceptance": "All seven assertions green with mode='replay'; every fixture raw carries recorded_by='operator' and is declared as such in DIVERGENCES.md.",
      "est_size": "L",
      "touches_frozen": false
    },
    {
      "id": "M600",
      "wave": 6,
      "path": "src/deepreason/h005/{material.py,driver.py}, tests/deepreason/test_h005_topologies.py, tests/deepreason/test_h005_driver.py",
      "purpose": "Consume the frozen material.json unmodified, compile its four problems and three topologies, and run a complete template invocation per cycle with the two-call protocol, offline on replayed raws.",
      "public_interface": [
        "@dataclass(frozen=True) class Material: sha256: str; system: str; instructions: Mapping[str,str]; problems: tuple[dict,...]; templates: Mapping[str, dict]",
        "material.load(path: str) -> Material  # read-only; pins and returns the file sha256; validates the minireason.h005.material.v1 shape",
        "material.NODE_RULES: Mapping[str, str]  # node id -> 'Conj' | 'Crit'; Crit = {objection, challenge, critique, cross}",
        "driver.run_cycle(harness: Harness, adapter: Adapter, material: Material, *, topology: str, problem_id: str, arm: str, cycle: int, previous_carry: str | None, origin: str | None, config: Config) -> Mapping",
        "driver.resolve_source(source: str, *, previous_carry: str | None, origin: str | None, produced: Mapping[str,str]) -> str | None",
        "driver.ARMS: tuple[str, ...] = ('mini_fcl','mini_prose','matched')"
      ],
      "depends_on": ["M200", "M201", "M206", "M400", "M402", "M403"],
      "tests": ["tests/deepreason/test_h005_topologies.py: the loaded node graphs equal exactly the frozen material — fork5 (account, objection, rival, response, carry), return6 (reopen, challenge, reply, critique, amend, carry), weave7 (body_route, commitment_route, cross, body_return, commitment_return, join, carry) — with each node's (source, view) pairs asserted one by one; the material file's sha256 and mtime are unchanged after the whole test module runs. tests/deepreason/test_h005_driver.py: all three topologies run end-to-end for one cycle per arm on replayed raws with ZERO provider calls; every node produced exactly two calls and the second call's pack contains the node's own body and none of the ports the node did not declare (independent_commitment_call true by construction); a 'commitments' view renders no body byte; an absent source renders ABSENT_TEXT; a malformed envelope logs FORMAT_FAILURE, drops the cycle and NEVER produces an empty commitments string; an FCL-1 objection produces a computed att edge and a refuted premise moves its dependent to suspended_unsupported; the prose arm produces a non-empty interface.commitments (demarcated) and zero derived refs; 'uptake' never appears in any status computation"],
      "acceptance": "A daily/fork5 cycle runs for all three arms offline; the run record exposes artifact labels, selected fields, parent hashes and exact payloads per the research contract; material.json byte-unchanged.",
      "est_size": "L",
      "touches_frozen": false
    },
    {
      "id": "M700",
      "wave": 7,
      "path": "src/deepreason/llm/endpoints.py, tests/deepreason/test_endpoints.py",
      "purpose": "The live record-mode endpoints: DeepSeek by wrapping the audited provider unchanged, and an in-package OpenAI-compatible endpoint for Ollama cloud, both under one five-slot gate with credential discipline.",
      "public_interface": [
        "class LiveEndpoint(Protocol): family: str; endpoint_id: str; def complete(self, messages: list[dict], *, json_output: bool, coordinate: Mapping) -> Mapping",
        "class DeepSeekEndpoint: def __init__(self, settings, records_dir: str) -> None  # delegates to minireason.provider.DeepSeek unchanged; family='deepseek'",
        "class OpenAICompatEndpoint: def __init__(self, *, endpoint_id: str, family: str, base_url: str, model: str, key_env: str, records_dir: str, timeout_seconds: int, max_tokens: int) -> None  # Ollama cloud and any OpenAI-compatible host",
        "endpoints.build(config: Config, records_dir: str) -> Mapping[str, LiveEndpoint]",
        "record schema: 'deepreason.call.v1' — request, request_sha256, settings, family, coordinate, started_at, elapsed_ms, provider_response_sha256, returned_model, usage, finish_reason, content, reasoning_content_present, reasoning_content_persisted=False, credential_redaction"
      ],
      "depends_on": ["M403", "M401"],
      "tests": ["tests/deepreason/test_endpoints.py (no network; urlopen monkeypatched): the key is read from os.environ[key_env] at call time and never appears in any written record, blob or log line; a payload containing the key raises DR_SECRET_IN_REQUEST, writes a refusal record and sends nothing; an echoed key in the response is replaced by [REDACTED_CREDENTIAL] and credential_redaction is True; reasoning_content_persisted is always False and hidden reasoning text is never written; six concurrent calls across BOTH families never exceed five in flight (asserted with a counting fake transport); DeepSeekEndpoint constructs minireason.provider.DeepSeek and does not modify it (ast check: endpoints.py is the only module allowed to import minireason.provider, per M002)"],
      "acceptance": "With DEEPSEEK_API_KEY and OLLAMA_API_KEY unset, build() raises a clear KEY_MISSING-style error and no request is attempted; with a fake transport, both families write deepreason.call.v1 records and the in-flight counter never exceeds 5.",
      "est_size": "M",
      "touches_frozen": false
    }
  ]
}
```

---

## 8. Pre-registration receipt for `docs/DECISION_LEDGER.md`

Append verbatim (root substitutes the real UTC timestamp, the next unused receipt letter if `M` is taken, and the prior verified commit/tree):

> REC-20260914-M 2026-09-14 HH:MM:SS UTC: **Choice:** register a new mechanism intervention with its own identity per `PURPOSE.md` — a new package `src/deepreason/` implementing harness-spec v1.3 §0–§4 and §14–§16 P0 and P1, to be built in eight dependency-layered waves with a P0 gate after wave 3, an offline P1 gate after wave 5, and an offline H005 gate after wave 6 — and pre-register, before any provider call, the H005 occurrence-02 contrast this engine makes possible. This is a mechanism intervention, not a repair of an earlier one: occurrence-01 and its published envelope-asymmetry review remain frozen and unedited, and nothing in `src/creib/forge/mini/**`, `src/minireason/{language,inquiry,reason_use,successor}_mini.py`, `experiments/records/**`, `experiments/plans/**` or the published H005 material is modified; a test (`tests/deepreason/test_boundaries.py`) enforces both by AST import-allowlist and by a pinned tree hash. **Why:** the frozen engine cannot render `view: commitments` — `src/creib/forge/mini/ports.py:18` ships exactly `("text","list_bodies","list_bodies_and_commitments","legend")` and `:97-98` raises `MINI_RENDER_RULE_UNKNOWN` — so the current helper supplies a per-binding "Explicit field projection" pseudo-kind whose body is helper-authored (`tools/multicycle_commitment_study.py:147,168`), which inverts the harness/model boundary the spec's §0 fixes, and whose decode failure branch (`:329-341`) produced the recorded `commitments_sha256` `e3b0c442…` on two matched-arm nodes. The frozen engine also has two labels rather than three, raises `MINI_ADJUDICATION_UNSETTLED` on a mutual criticism, has no `dep` relation and no validity node, and folds the registration `seq` into artifact identity (`src/creib/forge/mini/runner.py:393-411`). The new engine makes a commitment a first-class object, a view a deterministic projection of `interface`, a criticism a computed `att` edge with an attackable validity node, and an orphaned conclusion `suspended_unsupported` rather than `accepted`. **Contribution:** it supplies the mechanism the current research contract requires — an authored body distinguished from an authored commitment surface, and a harness-owned record of which artifacts and fields each subsequent invocation actually saw — and it makes §16 P0's six acceptance obligations testable in this repository. It does not establish that any arm reasons better, and operational completion certifies nothing about creativity or explanatory bearing. **Pre-registered H005 statement, committed before first look:** both Mini arms receive real §1 Commitment objects, so both are demarcated under §6:244; the `mini_fcl` arm additionally yields derived `dependence`/`mention` refs and derived attack edges from objection records, while the free-prose and matched arms yield none, because inferring a dependence or an objection target from prose would be the harness inventing content, which §0 and the material both forbid. That asymmetry is the measured condition of the comparison and is exactly the language's claimed contribution; it will never be reported as a defect of prose, and `PURPOSE.md`'s clause that prose conjectures and criticisms hold the same semantic legitimacy as formal ones governs every interpretation of it. A second pre-registered statement: adding §4 pass 2 means artifacts the frozen engine labelled `accepted` can be labelled `suspended_unsupported` here; that is a correction of bookkeeping, not a result, and no reader may read the label shift as evidence about any arm. **Stated falsifier for this intervention:** if, under the new engine, attack edges land on H005 criticisms and root still cannot identify a single episode in which a warranted criticism changed a later operative use, then the missing ingredient was never the bookkeeping, the engine bought auditability rather than error correction, and that outcome will be reported as evidence with the same weight as a positive one. **Declared divergences from harness-spec v1.3, each with its own line in `docs/deepreason/DIVERGENCES.md` (append-only) before the corresponding wave lands:** §14's "Pydantic models throughout" is declined in favour of frozen dataclasses plus the existing pinned `jsonschema==4.25.1`, because byte-for-byte replay must not depend on a third-party serializer's minor version and because a second canonicaliser in this tree is a drift class the errata already track; the event record adds `prev`, `event_id` and, on `Adj` events, `state_diff.digest`, and the `llm` block adds `pack_manifest_ref`; §11.7's default Pareto axes (`HV_B`, reach) require the P2 variator and cross-evaluation, so the P1 profile uses `coverage`, `conn` and `attack_survival` and the module is axis-generic; anti-relapse stage 2 is absent, fails open and logs the degradation; no `eval:rubric` commitment may be registered until a standard artifact exists for its spec-id to resolve to (§1, §2), so every H005 commitment is `program:` or `predicate:` until §10 lands at P5; §§10–12, all of §11's capture control, §14 `Merge` and §16 P2–P6 are out of scope by name. **Upstream:** `AHepi/DeepReason` commit `9607fba6f0a3066fbcab282c9ae0fad823e52e0c` (MIT) is present at `/home/user/ahepi/deepreason` and implements the same byte-identical spec, and **no byte of it is copied**: `AGENTS.md` authorises extraction from `AHepi/h-EPI`, upstream has deliberately reversed three v1.3 clauses (`rules/spawn.py:58-66` deletes the failed-verdict successor trigger; `measures/demarcation.py` supersedes `active(a)`; four §13 verbs are absent) and holds amendments v1.4–v1.7 that this repository has never adopted, and neither old source-project authority nor executable success may silently redefine these sources. Upstream is recorded in `docs/deepreason/UPSTREAM_REFERENCE.md` and used only by a skip-by-default agreement test. **Provider posture:** no provider call is authorised by this receipt. Waves 0–6 are entirely offline on a committed, operator-authored raw tape whose records are marked `recorded_by: "operator"` so no fixture can be mistaken for provider evidence; wave 7 adds record-mode endpoints that read `DEEPSEEK_API_KEY` and `OLLAMA_API_KEY` from the environment at call time only, never store a credential, refuse to send when a credential appears in request content, redact an echoed credential, never persist hidden reasoning, and share one process-wide ceiling of five concurrent requests across both families. A live H005 occurrence-02 dispatch requires its own separate receipt and a frozen plan. **Fallback, declared now so engine work cannot displace the research:** if evidence is needed before wave 6, ship waves 0–3 and run occurrence-02 with the existing helper importing only `deepreason.views.projection`, recorded as a declared intermediate configuration with its own identity — never as a test of FCL-1 on the old projection. **State:** pending; evidence on completion is the green P0 suite, the offline P1 acceptance test, the three H005 topologies running on replayed raws with `material.json` byte-unchanged, and `docs/deepreason/DIVERGENCES.md` complete for every wave landed. Prior verified commit/tree: `<commit>` / `<tree>`.

---

## 9. Risks, non-goals, open questions

### Risks

1. **Two engines in one repository.** Frozen Mini and `deepreason` share vocabulary and disagree on semantics. Mitigations: the AST allowlist test, the frozen-tree hash pin, distinct storage layouts and schema names, and `DIVERGENCES.md` opening with the statement that H003/H004/H005-occurrence-01 results were produced on the frozen engine and are not arm-for-arm comparable with anything produced here.
2. **Package-name collision with upstream `deepreason`.** §15:525-531 makes `deepreason.config.Config` and `deepreason.llm.adapter.build_adapter` normative, so the name is claimed — but the two packages must never be installed in one environment. Recorded in `UPSTREAM_REFERENCE.md`. A rename is mechanical and changes no JSON.
3. **Re-deriving the closure fixpoint without an oracle.** `build_att` (M104) is the only genuinely risky code; §4 itself is verbatim pseudocode. Mitigation: the heaviest test battery in the plan, order-independence assertions, and the skip-by-default upstream agreement test — which covers `grounded_extension` only, so the closures remain the residual risk and are called out as such.
4. **Fixture-key brittleness.** Any change to `packs.render` changes every key. Mitigation: `packs.py` is snapshot-tested and frozen after wave 4; a render change is a new fixture generation with its own identity and its own receipt.
5. **FCL-1 compilation is an interpretation.** Mapping `depends` to a `dependence` ref is a semantic commitment that can be wrong and that materially changes what lands. It is published in this document and in the receipt as a criticisable claim before any live call.
6. **Predicate commitments are shallow at P1.** `fcl1_record_wf` checks that a record exists and is well-formed, not that its substantive obligation holds. §17 already names this failure mode ("skeletons can be gamed by toothless forbidden cases"). Declared in `DIVERGENCES.md`, not papered over; the substantive route is §10 at P5.
7. **Determinism hazards.** `ts` in the log (mitigated: excluded from ids, verdicts and the state digest); pack truncation (whole sections only); dict/set iteration order (canonical JSON, lexicographic tie-breaks, frozenset results); subprocess non-determinism (step budgets only, never wall clock); floats (rejected by the canonical profile at the boundary).
8. **Merge-conflict surface across worktrees.** Concentrated in `__init__.py`, `pyproject.toml` and `tests/deepreason/__init__.py`; all are written once in Wave 0 and frozen, and no later module's path list touches them.
9. **The engine displacing the research.** Waves 0–3 are ~1,600 lines and buy P0; `views/projection.py` (M201, size S) is the one file H005 is actually blocked on. The declared fallback in §8 exists precisely so the programme can produce evidence before wave 6.

### Non-goals (named, so silence is never read as coverage)

§6/§7 beyond `crit`, `conn`/`iso` and Pareto: no HV estimator, no `µ_struct`, no `hv-floor`, no variator kernel, no reach cross-evaluation, no rent rule. §10 informal domains entirely: no skeleton criteria, no forbidden-case compilation, no trial guard, no standards-as-case-law authoring, no anchored/pairwise modes, no judge audits, no holdout/`Reveal`, no appellate docket (the §1:108 closure that *makes* standards work is built at P0, because P0 test 5 requires it). §11 capture control entirely: no schools, no allocation policy, no detection surfaces, no λ, no response ladder, no negative atlas, no `Reseed`, no embedder, no anti-relapse stage 2. §12 research backends. §13's `docket`, `rule`, `schools`, `capture`, `reseed`, `merge` verbs. §14 `Merge`, so P3 is unreachable by construction. §16 P2–P6. Each gets a `DIVERGENCES.md` line naming what is missing and what would be needed.

### What would defeat this design

If, with `att` edges landing on H005 criticisms and the support cascade live, root still cannot identify one episode in which a warranted criticism changed a later operative use, then the bookkeeping was never the missing ingredient: this engine bought auditability, not error correction. That is evidence and is reported as such. Separately, if the two Mini arms' derived-edge asymmetry turns out to explain nothing about what later nodes actually do, the FCL-1 proposition loses its mechanical warrant even though the compiler works.

### Open questions for the repo owner

1. **Vendoring.** Do you want an explicit authorisation for `AHepi/DeepReason`? This design deliberately needs none, but with one, M103/M104/M100 could be replaced by a hash-pinned, provenance-headed port with no interface change and roughly four agent-days saved. The default answer here is no.
2. **Pydantic.** §14:521 says "Pydantic models throughout"; 2.13.5 is present in this environment but is not a pinned dependency. Confirm the declined-with-receipt posture, or authorise a third pin and I will add pydantic as a validation layer strictly outside id computation.
3. **Amendments v1.4–v1.7.** They exist upstream and are not in `docs/sources/`. Retrieving them is a separate user-authorised decision; v1.4's authority boundary in particular bears on the H005 template layer. This design implements v1.3 only and adopts nothing from them.
4. **§3:179 vs upstream H1.** We implement the v1.3 trigger as written and register upstream's counter-argument as an attackable Refl rule-artifact. Confirm that is the posture you want, or supply the argument document so it can be registered with its real content.
5. **Occurrence-02 scope.** Which problem/topology/arm chains, and how many cycles, should the first live dispatch cover? The engine supports all twelve chains; the five-request ceiling and the publication discipline are what bound them.
6. **Receipt letter.** `REC-20260914-M` assumes `M` is unused on 2026-09-14; renumber if not.
