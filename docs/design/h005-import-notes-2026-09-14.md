# `import_h005` — design notes, deviations, open questions

Published as `docs/design/h005-import-notes-2026-09-14.md` and linked from
`docs/workflows/graph-import-h005.md`. This revision folds in a second
adversarial review; the per-finding record of what changed is `FIXES.md` in the
staging tree.

Staged at `scratchpad/importer/` in repository layout:

```
src/minireason/graph_import_h005.py     the library
src/minireason/data/fcl1.schema.json    the vendored FCL-1 syntactic schema
src/minireason/__init__.py              STAGING SHIM ONLY - do not publish (see §8)
tools/import_h005.py                    the CLI
tests/test_graph_import_h005.py         60 offline tests, over the REAL occurrence
tests/data/h005_import_pins.json        sha256 of every occurrence file the tests read
docs/workflows/graph-import-h005.md     the workflow doc
docs/design/h005-import-notes-2026-09-14.md   this file
```

**There is no fixture copy.** The tests read
`experiments/diagnostics/H005-open-prose-commitments/occurrence-01` read-only
and re-hash it against `tests/data/h005_import_pins.json` in `setUpModule`
(skip if the occurrence is absent, hard failure if a pin differs). The copy that
used to live under `tests/fixtures/` lacked the matched arm's `responses/` and
`attempts/`, so it silently exercised a receipt-less path that does not exist in
the occurrence, and its golden numbers were a property of the copy. Tamper tests
`shutil.copytree` the occurrence (narrowed to the arms they need) into a
`TemporaryDirectory` and corrupt the copy.

Run:

```
PYTHONPATH=<importer>/src:/home/user/miniReason/src \
  python -X utf8 -m unittest discover -s <importer>/tests -v
```

The staged `src` comes **first**: `deepreason_core` is published in the
repository (`/home/user/miniReason/src/deepreason_core`, with the `clock`
parameter of §4), so there is no separate `vendor-core` entry, and the staged
`minireason.graph_import_h005` must win over the repository's package.

---

## 1. What the importer is for, and what it is not

It re-expresses a finished H005 occurrence in a second vocabulary and reports
what that vocabulary cannot carry. It produces no new evidence. The labels it
computes are the grounded extension of the attack relation the *authors*
declared, plus a support cascade over declared dependence — mechanism
bookkeeping, nothing else. Invariant **I7** is stated in the module docstring,
printed as the first line of every `REPORT.md`, repeated at the end of every
`why(...)` chain, carried in `report.json` as `invariant_i7`, and stated in the
workflow doc: no label here is a semantic attribution, and root alone
interprets substantive output (PROTOCOL.md §Interpretation).

The other standing invariants (I1 offline, I2 transport status is never a
verdict, I3 dependence is never inferred, I4 nothing is repaired, I6
deterministic) are `mapping.md` §0 unchanged. **I5 is narrowed**: everything
unmapped is reported *at the granularities the closed residue vocabulary names*
(`ref`, `record`, `document`, `edge`, `artifact`, `problem`, `file`). Every FCL
record in scope is either mapped to a spec construct or carries a residue code —
`claim` and `use` records, which map to nothing, each get one — and
`side_table.json.records[]` shows which, per record. That is record-level
completeness, not a claim that a mapped record's every nuance survived, and the
report now says exactly that instead of "nothing was dropped silently".

---

## 2. Corrections from the adversarial review, as applied

The review overrides `mapping.md`/`expected_graph.md` where they conflict. Each
correction, what changed, and what it cost:

**(1) OPAQUE artifacts are `accepted`, not `suspended`.** `mapping.md` §5
claimed an unattacked, unattacking OPAQUE artifact is `suspended`. That is
false against the vendored adjudicator: `grounded_extension` seeds `F(∅)` with
*every* node that has no attacker, so an unattacked artifact is in `G` and
`label0` is `accepted`. (`expected_graph.md` §5 already says the same thing
about `A_carry`: "unattacked — the last node in the invocation always is".) The
importer keeps such an artifact in the graph with an empty `Interface`, and its
residue detail says so verbatim: *"accept-by-position: no warrant in this import
targets it. This import reified criticism only from an FCL-1 commitment surface,
so the absence of an attacker is not evidence that the contribution was
uncriticised."* That is now the single wording — one module constant,
`ACCEPT_BY_POSITION` — used by every residue reason, every `why` chain and
`REPORT.md`. The earlier phrasing, "nothing criticises it", was false as
written: nothing criticised it **in this import**, which reads only an FCL-1
commitment surface and cannot see criticism carried any other way. A test
asserts the old phrase appears nowhere in the report or in `report.json`. Where
the surface was not read at all, the `why` chain additionally ends with that
artifact's `commitment_surface_state` and what it does and does not mean.

**(2) Commitment handling dispatches on the parse outcome, not on
`envelope_status`.** `envelope_status` is recorded in the side table and never
read for a decision (I2). The dispatch is now: empty `commitments` string →
`opaque_envelope` (and see below on what that is *not* evidence of); an arm whose declared surface is prose (`bare`, `native`,
`matched`, `mini_prose`) → `prose_commitment_surface` and no parse attempt,
because the author was never asked for FCL-1; an FCL-surface arm (`mini_fcl`)
→ strict parse and schema validation, failures reported as `parse_failure` /
`schema_failure` with the artifact left opaque. This removed 10 spurious
`parse_failure` entries on the full occurrence — the prose arms were being
judged against a grammar they never claimed. Full-occurrence run (all 5 arms,
17 coordinates): `prose_commitment_surface` 10, `opaque_envelope` 2,
`parse_failure` 0.

**What an empty `commitments` string means here, and what it does not.** Root's
published review, `docs/reviews/h005-matched-arm-envelope-asymmetry-2026-09-14.md`,
measured the mechanism: the returned JSON contains raw newline control
characters, strict `json.loads` raises, `decode_contribution` takes its failure
branch, and the harness stores the whole returned text as `body` and `""` as
`commitments`. Parsed non-strictly the same bytes yield a commitments field of
2,346 and 2,363 characters. The commitments were **authored and lost in
decoding**. So the residue reason attributes the empty string to that decode
failure, cites the review by path, and says the commitment surface is
**UNAVAILABLE, not absent** — this is not evidence that the author declined to
commit. The same wording is in the workflow doc's "What it does NOT do" list and
in `REPORT.md` wherever the count is nonzero.

The side-table field that used to be called `opaque_reason` is now
`commitment_surface_state`, with the closed value set
`read_fcl1 | prose_not_parsed | unavailable_decode_failure | parse_failure |
schema_failure`. "Opaque reason" invited the reading that the artifact was
opaque *because of* something the author did; the new name says only what this
import did with the string.

The `prose_commitment_surface` reason was also wrong on a point of fact. It said
the artifact "is not adjudicated". It is: it is registered, it is in the graph,
and it is labelled. What is true is narrower — with no commitment surface read it
has no attacker, so grounded semantics labels it accepted by position, and **that
label carries no information about the arm**.

**Whenever a scope spans more than one arm** `REPORT.md` carries a fixed
paragraph twice (in "What this is, and what it is not", and immediately above the
labels table) and the CLI prints it before the labels: N arms declare a prose
commitment surface and M declare FCL-1; a prose surface is never parsed, so no
warrant, no attack edge and no refuted label can arise from a prose arm under
this import; the distribution of statuses across arms is a property of the
carrier this importer reads, not a comparison between the arms; any cross-arm
reading is root's, not this instrument's. The paragraph is a module constant, not
a per-run sentence, so it cannot be softened.

**(3) Reference counts asserted at 82/84.** The importer now resolves *every*
ref it sees, `uptake` included, and reports
`{"refs": 84, "resolved": 82, "extensions": 2, "dangling": 0, "task": 0}`.
Per document: account 8, objection 17, rival 14, response 25, carry 20. The two
extensions are `rival.r1 → e3647350a300c0ed#BODY` and
`carry.n6 → b998d514348ed94e` (bare label). Asserted in
`test_references_resolve_eighty_two_of_eighty_four`.

**(4) Commitment `eval` is outside every executable class.**
`observation:h005.fcl1@<sha256(canonical_json(record))>`. The vendored
`Commitment.eval` is a plain `str` with no validator, so the scheme is accepted
as-is; **no fallback and no `commitment_eval_placeholder` code was needed.** An
importer guard raises `COMMITMENT_EVAL_LOOKS_EXECUTABLE` if a future edit ever
produces a `program:` / `rubric:` / `predicate:` prefix. This replaces
`mapping.md` §3.2's literal `predicate:h005.fcl1.observation@…`, which would
have put an English-sentence commitment in the one class a careless executor
dispatches.

**(5) Research problems carry no criteria.** `criteria = []`; the originating
commitment id is `provenance.from[1]` (with the carrier artifact as
`from[0]`); trigger `research`; one `problem_trigger_research_not_in_v13_enum`
residue entry per research problem (4). `mapping.md` §3.2 had
`criteria=[commitment.id]`, which confuses an *instantiated* commitment with a
commitment **schema** id — criteria are schema ids (spec §1). FCL `problem`
records keep `seed` + `problem_trigger_approximated` (5).

*Correction.* An earlier draft of this paragraph added "and the Popper battery
is pinned into the same list at registration". `Harness.register_problem` does
execute that line, but `deepreason_core.ontology.problem.POPPER_BATTERY` is the
**empty tuple** in the vendored slice, so nothing is pinned and every imported
problem's `criteria` stays `[]` exactly as written. The argument for empty
criteria rests on the schema-id point alone; the battery is inert here and must
not be cited as though it did work.

**(6) New codes and a `unit` on every code.** Added `mentions_intra_document`
(ref, 9), `commitment_record_not_in_uptake` (record, 2 — `rival.r10`,
`rival.r11`), `validity_node_minted_unasserted` (artifact, 7 — one per ν),
`claim_record_unmapped` (record, 15 — see §6.6),
`criticism_of_criticism_intra_document_dropped` (ref, 2 — see §2.7),
plus `prose_commitment_surface`, `ref_to_unregistered_target_dropped`,
`ref_to_task_artifact`, `problem_trigger_research_not_in_v13_enum`,
`criticism_of_criticism_retargeted`. Every code declares one of
`ref|record|document|edge|artifact|problem|file` and counts follow it; the
units are echoed in `residue.json` (`units`) and in the REPORT.md table.
`objection_target_self_ref_dropped` is now counted at **ref** unit: 4 (three
local targets on `objection.o4`, one on `response.k7`), where `mapping.md` §9
counted 2 records.

**(7) Criticism of a criticism attacks the validity node — with one stated
exception.** When an objection's
target ref resolves to a record this same import has reified as a warrant, the
new warrant targets that warrant's ν instead of the node artifact. Only
`carry.n3 → b998d514348ed94e#k7` qualifies (`k7` was reified into `W_k7`);
`response.k3`/`k7 → …#r9` do not, because `rival.r9` is untargeted and minted
nothing, so they fall back to `A_rival`. This changes the golden graph: **7
warrants and 7 ν artifacts, not 6**, and `|att| = 4`. Hand derivation and the
machine result are in §3 below.

**The exception: intra-document criticism of a criticism is NOT retargeted.**
`objection.o4` criticises `o1` and `o2`, which this import *did* reify — so by
the rule above it would attack ν(W_o1) and ν(W_o2). It does not, and that is
deliberate. The spec §1 closure lifts an attack on a validity node onto **every
carrier of the warrant**, and the carrier of W_o1 and W_o2 is
`daily/mini_fcl/cycle01/objection` — the very artifact that carries `o4`.
Retargeting would therefore mint a self-attack through the closure and make the
objection artifact self-defeating, which is not what an author asserts by
qualifying their own earlier objection. The refs are dropped; and because a
silent drop is exactly the failure this importer exists to avoid, each one also
emits `criticism_of_criticism_intra_document_dropped` (unit `ref`, severity
`lossy`, 2 in the golden scope) beside the existing
`objection_target_self_ref_dropped`. The deviation table states it, and
`test_intra_document_criticism_of_criticism_is_a_declared_exception` pins o4's
outcome as a deliberate exception rather than an oversight.

**(8) The ν no longer asserts soundness.** Its first line is now
`nu: <source>#<record> is an authored criticism directed at <target>; its
soundness and relevance are not asserted by this import.` Refs stay in the
literal order `[target, carrier]`, both `mention` (provably inert in
`build_att`: the case-law closure is gated on a `rubric:` commitment, and every
imported warrant has `commitment = None`). Every ν id, name, content sha256,
carrier, target, target kind and register seq is in
`side_table.json.validity_nodes`, and one `validity_node_minted_unasserted`
residue entry per ν records that the import is not endorsing the criticism.

**(9) The FCL-1 document is its own artifact.** codec `json`, `content_ref` =
the recorded `commitments_sha256` (the bytes go to the blob store, so
`theory(id)` can render them), empty `Interface`, `provenance.role = import`.
The node artifact carries a `mention` ref to it. Only successfully parsed FCL-1
documents get one: a prose or empty commitments string is still written to the
blob store and recorded in the side table, but minting an artifact for it would
assert a document where the author produced none. (Open question in §6.)

**(10) Carriage lives only in the harness relation.** `register_batch` is the
only way the P0 API accepts a new `(artifact, warrant)` pair, and it reads the
pair off the *transient* argument's `warrants` list; because the content
artifact already exists, the **stored** record is never rewritten, so
`objects/artifact/*.json` keeps `"warrants": []` and `state.carries` is the
sole record. `_verify_event_log` asserts both directions after every import
(`CARRIAGE_NOT_RECORDED`, `CARRIAGE_WRITTEN_ONTO_ARTIFACT`), and
`test_carriage_lives_in_the_harness_relation_only` asserts it through
`Harness.carried_warrant_ids`.

**(11) Determinism and the write path.** `interface.commitments` is sorted;
`interface.refs` is sorted by `(target, role)`; the ν keeps its literal
`[target, carrier]` order; artifact ids are computed in wave/coordinate order,
and a ref whose owner is not registered yet (or is outside the scope) is
dropped with `ref_to_unregistered_target_dropped` instead of raising. **The
write path is the harness registration API only** — `register_problem`,
`register_commitment`, `create_artifact`, `register_batch` — so the event count
is whatever that API produces (38 for the golden scope) and no log line is
forged. Consequence: `mapping.md` §8.2's single terminal `Adj` event is **not
emitted**, because the P0 `Harness` re-adjudicates inside every registration
and exposes no public `Adj` emitter. An earlier draft called
`Harness._commit(Rule.ADJ, …)`; that is a private method and was removed. The
`adjudication_batched` residue entry now records the true state of affairs
(status flips are in each registration event's `state_diff.status_changed`).

**(12) `#BODY` is a fallback, not a first choice.** A qualified ref now looks
the local id up in the *target* document first, so a document that really names
a record `BODY` wins; only when absent does the rendered-section-header
convention apply (`qualified_ref_body_pseudo_local`). The task artifact is in
the alias index under both spellings (its 16-hex label and `h005.task.v1`),
cross-checked against `trace.task_artifact.artifact_id`; a ref through it
resolves to the root `Problem` context, mints nothing, and is reported as
`ref_to_task_artifact` (0 observed).

**(13) I7 banner.** In `REPORT.md` (first line), in the workflow doc (first
line), in every `why` chain, and in `report.json`.

---

## 3. The golden graph, hand-derived and machine-checked

`att` after correction (7):

| warrant | carrier | target | kind |
|---|---|---|---|
| `…objection#o1->…/account` | A_objection | A_account | artifact |
| `…objection#o2->…/account` | A_objection | A_account | artifact |
| `…objection#o3->…/account` | A_objection | A_account | artifact |
| `…response#k3->…/rival` | A_response | A_rival | artifact |
| `…response#k7->…/rival` | A_response | A_rival | artifact |
| `…carry#n3->…/response` | A_carry | A_response | artifact |
| `…carry#n3->nu(…response#k7->…rival)` | A_carry | ν(W_k7) | **validity node** |

```
att = { (A_objection, A_account), (A_response, A_rival),
        (A_carry, A_response), (A_carry, nu(W_k7)) }          |att| = 4
dep = ∅
```

`build_att` in the vendored slice implements **three** closures, and it is worth
enumerating them exactly, because an earlier version of this paragraph named a
fourth that does not exist here:

1. **Validity-node closure** (always on). Every attacker of a warrant's
   `validity_node` becomes an attacker of every carrier of that warrant. This one
   is **active**: it would add `(A_carry, A_response)` from `(A_carry, ν(W_k7))`.
   That edge is already present from `n3`'s other warrant, so the fixpoint
   converges on the first iteration with 4 edges.
2. **Case-law extension** (§1/§10.3). Gated on `commitments.get(w.commitment)`
   having an `eval` that starts with `rubric:`. **Inert**: every imported warrant
   has `commitment = None`, so the lookup is skipped before any ref is read.
3. **Evidence closure.** Gated on the ν's interface carrying a ref with role
   `EVIDENCE`. **Inert**: every ν ref this import mints is a `mention`, and the
   node artifacts' refs are `mention`/`dependence` only.

There is **no source-artifact closure in the vendored core**. The earlier claim
that one exists and "reads `budget.extra["source_artifact"]` while the importer
writes the prefixed `h005_source_artifact`" was wrong: that closure is cut from
the vendored slice, and `grep -n source_artifact` over
`src/deepreason_core/` returns nothing. The prefixed key is still the right
thing to write — it costs nothing and it keeps the importer correct against a
fuller core that does have such a closure — but it must not be described as
neutralising a closure that is not there.

Hand derivation (Kleene iteration of `F(X) = {a : ∀(b,a)∈att, ∃c∈X, (c,b)∈att}`)
over the 17 artifacts — 5 node, 5 document, 7 ν:

- attacked nodes: `A_account ← {A_objection}`, `A_rival ← {A_response}`,
  `A_response ← {A_carry}`, `ν(W_k7) ← {A_carry}`. Everything else is
  unattacked.
- `X₀ = ∅` ⇒ `F(∅)` = the 13 unattacked artifacts (A_objection, A_carry, the 5
  documents, and 6 of the 7 ν — ν(W_k7) is excluded, it has an attacker).
- `X₁`: `A_account` needs an attacker of `A_objection` — none, excluded.
  `A_rival` needs an attacker of `A_response`: `A_carry ∈ X₁` and
  `(A_carry, A_response) ∈ att` ⇒ **included** (Lemma 3.1 reinstatement).
  `A_response` and `ν(W_k7)` need an attacker of `A_carry` — none, excluded.
- `X₂ = X₁ ∪ {A_rival}`; re-evaluating changes nothing. Fixed point, `|G| = 14`.

`label0` ⇒ `A_account` **refuted**, `A_response` **refuted**, `ν(W_k7)`
**refuted**, everything else **accepted**. `dep = ∅` ⇒ pass 2 is the identity.
The vendored adjudicator (`build_att` → `label0` → `final_labels`, run both
offline and through the written harness root, compared for equality on every
import) returns exactly that: **14 accepted, 3 refuted, 0 suspended, 0
suspended_unsupported**.

The substantive change against `expected_graph.md` §7 is `ν(W_k7)`: the carry's
criticism of the response's objection now lands where it belongs, and the
closure — not a hand-written rule — carries it onto `A_response`. `A_response`
was already refuted through the `n3 → k2` warrant, so the *node* labels are
unchanged; what changed is that the graph now records **why** the response's
objection against the rival stopped counting.

Still position-determined, and still worth saying: `A_carry` is accepted
because nothing came after it, and `A_rival` is reinstated because `A_carry`
happened to attack `A_response`. One cycle of `fork5` has no more criticism in
it.

---

## 4. Vendored-core extension

The staged core stamps `Event.ts` with `datetime.now(timezone.utc)` inside the
private `_commit`, and the P0 API has no way to pass a timestamp. Byte-identical
independent builds are impossible without one, so — per explicit instruction —
the staged `deepreason_core.harness` gained **one optional constructor
parameter** and nothing else. Exact diff:

```diff
--- a/src/deepreason_core/harness.py
+++ b/src/deepreason_core/harness.py
@@ -8,7 +8,7 @@
-from collections.abc import Iterable
+from collections.abc import Callable, Iterable
@@ -95,6 +95,7 @@ class Harness:
         *,
         upto_seq: int | None = None,
         read_only: bool | None = None,
+        clock: Callable[[], str] | None = None,
     ) -> None:
@@ -104,6 +105,11 @@
         self.root = Path(root)
+        # Optional deterministic event clock: a callable returning the iso8601
+        # string stamped on Event.ts. Default None keeps the wall-clock
+        # behavior. An offline importer replaying recorded evidence must not
+        # fork its log on machine load (spec §0 replay determinism).
+        self._clock = clock
         self._read_only = (upto_seq is not None) if read_only is None else read_only
@@ -411,7 +417,10 @@ class Harness:
         event = Event(
             seq=self._next_seq,
-            ts=datetime.now(timezone.utc).isoformat(),
+            ts=(
+                self._clock() if self._clock is not None
+                else datetime.now(timezone.utc).isoformat()
+            ),
```

Default behaviour is unchanged, so every existing core test and every existing
root is unaffected. The importer passes a `_Clock` whose value it sets from the
occurrence's `finished_utc` before each registration call. **Publication
dependency:** the parameter is present in the published
`/home/user/miniReason/src/deepreason_core/harness.py`, which is what the staged
suite now runs against; if that core is ever republished from upstream, the
parameter must be re-applied or the importer loses replay determinism (and
`test_two_imports_are_byte_identical` fails loudly, which is the intended
alarm). An earlier draft monkey-patched `harness.datetime` for the duration of
an import; the parameter replaces it.

---

## 5. Deviations from `mapping.md` not already covered above

1. **Event count is 38, not 28.** `mapping.md` §8.4 assumed one `Register`
   event could carry a node's commitments *and* its artifact; the P0 API emits
   one event per `register_commitment`. Add the 5 FCL-1 document artifacts
   (§2.9), the extra ν/`Crit` pair (§2.7), and subtract the terminal `Adj`
   (§2.11): 1 task Spawn + 5 document Registers + 4 commitment Registers + 5
   node Registers + 5 problem Spawns + 4 research Spawns + 7 ν Registers + 7
   `Crit` = 38, `seq` 0..37.
2. **`Event.ts` is not required to be nondecreasing.** It is for the golden
   single-arm scope (and asserted there), but a wave runs several arms
   concurrently and their `finished_utc` values interleave; the full-occurrence
   import is non-monotone at `seq` 3. Clamping would report a time that was
   never observed, so the importer reports the fact instead
   (`custody.event_ts_nondecreasing`). Spec §14 requires contiguous `seq`, not
   ordered `ts`.
3. **A coordinate with no receipt inherits the previous coordinate's `ts`.**
   Rather than invent a time or refuse the node, the importer carries the
   previous registration's timestamp forward and records the absent inputs in
   `side_table.artifacts[].absent_inputs`. If the whole scope has no receipt,
   the import is refused (`NO_FINISHED_UTC_IN_SCOPE`); so is a scope whose
   *leading* coordinate has none (`NO_LEADING_RECEIPT`), since there is no
   previous stamp to carry. A missing **request record** is a different matter
   and is refused outright (`REQUEST_RECORD_MISSING`): it is the trace's only
   pin, and the trace is what the label index and every two-hop reference are
   read from.
4. **Wave placement is read from `waves/`, not from `attempts/`.**
   `waves/<id>.coordinates` is the authoritative ordered array; the attempt file
   is used to cross-check `wave_id` and `request_sha256` when present. This is
   what lets a receipt-less coordinate still be ordered.
5. **`multicycle_commitment_study.verify()` is re-implemented, not imported.**
   Importing the module executes `sys.path.insert` twice at import time and
   pulls in `minireason.provider` (the live DeepSeek transport) and
   `creib.forge.*`; an offline importer must not load a provider module, and
   `verify()` additionally needs a repository checkout to recompute
   `runtime_pins` and to re-compile manifests, which an occurrence directory
   alone cannot supply. The occurrence-local subset is re-implemented in
   `verify_custody` / `_verify_node_custody`, and `study_digest` is pinned
   against the recorded `plan_id` by a test.

   **Which links of `read_terminal()` are reproduced, and which are not.**
   Reproduced: coordinate agreement across request/trace/attempt/receipt;
   `request.trace_sha256 == digest(trace)`; `attempt.request_sha256 ==
   receipt.request_sha256 == digest(request)`; the provider call byte hashes
   against `receipt.provider_{request,response}_sha256`, skipped only for a
   `FAILED` receipt exactly as `read_terminal` does; `sha256(artifact record) ==
   receipt.artifact_sha256`; `responses/<node>.txt` against
   `public_text_sha256`; `receipt.status`/`envelope_status` against the artifact
   record. **Not** reproduced: `request.messages_sha256 ==
   digest(request.messages)`, `request.provider_payload == payload_for(...)`,
   `request.settings == settings_for(arm).to_dict()`, and the re-derivation of
   the artifact through `decode_contribution`/`authored_artifact`. Those need
   repository code an occurrence directory cannot supply, and importing it would
   breach I1. The workflow doc says the same, so a reader of the report is not
   left to assume the study's full terminal check was re-run.

   The pinning happens **before the trace is used**. `requests/<coord>.json`
   fixes the trace by `trace_sha256` and is itself fixed by the attempt and the
   receipt, so a rewritten `selected_source` cannot steer the label index or the
   projection resolver. Previously a tampered projection source was caught only
   if some ref happened to travel through that slot — lazily, and incompletely.
   `TracePinningTest` tampers exactly one `selected_source` field and asserts
   `TRACE_NOT_PINNED` with nothing written.
6. **Scope-relative resolution.** A ref whose owning coordinate is outside the
   imported scope is dropped with `ref_to_unregistered_target_dropped` rather
   than reaching outside the scope for an id. Computing an out-of-scope spec id
   would require computing that artifact's whole interface, which is circular in
   the general case. 0 observed in any scope tried.
7. **`side_table.json` gained fields** `commitment_surface`,
   `commitment_surface_state` (renamed from `opaque_reason`, §2.2),
   `task_labels`, `document_spec_artifact_id`, `absent_inputs`, `documents[]`,
   and per-ν `name`/`target_kind`/`register_event_seq`. All are provenance;
   nothing in the side table is read by adjudication.
8. **Custody is counted per check, and split by what it is worth.**
   `custody.cross_file` and `custody.self_consistency` each carry, per check,
   `ran`/`total` and the subjects skipped with the input that was missing.
   `REPORT.md` renders them under separate headings — the second labelled
   "internal consistency only", with the sentence that such a check cannot detect
   a coherent rewrite — and each row reads `verified (n/n nodes)` or
   `verified (n/m nodes; k coordinate(s) had no receipt: …)`, never a bare
   "verified". Two rows were added: "per node: receipt present", which names the
   coordinates that have none, and "event ts nondecreasing | yes/no", which
   carries the declared-deviation wording when the answer is no. A receipt-less
   coordinate is **admitted with its absent inputs recorded, not refused** — a
   coordinate with no *request record* is refused, because nothing then pins
   its trace, and where the request record exists but neither an attempt nor a
   receipt pins *it*, `trace_pinned` and `request_record` are counted as not
   run rather than as verified. `projection_source` counts **projections**, not
   nodes, so one checkable slot can no longer make a whole node read as
   verified.
9. **Residue carrier ids are backfilled.** Most residue is raised before the
   carrier's content-addressed spec id exists (the id depends on the interface,
   which depends on the refs, which is what the residue is about), so
   `carrier.spec_artifact_id` used to be null for exactly the codes that matter
   most and `residue.json` could not be joined to `side_table.json`.
   `backfill_residue_carriers()` fills them in once every node is named; a test
   asserts that every entry with a carrier coordinate in scope has a non-null id
   present in the spec-id table.
10. **Custody runs for every node, not only for parsed ones.** The old
   `_build_label_index` did the brief hash, the projection-id shape check, the
   brief/index agreement and the task-label check — and it ran only for a node
   whose FCL-1 document parsed, so a whole prose arm went uncustodied. It is
   split: `_verify_projection_custody` runs for every node from `load_nodes`,
   `_verify_projection_sources` checks every projection's `selected_source`
   against the authored record for every node, and only the *use* of the index by
   `resolve_ref` is gated on a parsed document. Projection residue also now runs
   for every node (its reason says the surface was not read when that is why no
   ref cites a slot): on the full occurrence `projection_absent` goes 2 → 4 and
   `projection_exposed_unreferenced` 2 → 10.
11. **`dependence_cycle_rejected` cannot fire on a real occurrence.** A ref
   resolves through a projection whose source must already be registered, so
   every admitted `dep` edge points from a later coordinate to an earlier one and
   `dep` is acyclic by construction; the other half of a mutual dependence is
   dropped earlier as `ref_to_unregistered_target_dropped`. The guard is kept as
   insurance against a future change of ordering, and the synthetic test reaches
   it by seeding the mapper's edge accumulator. `REPORT.md` marks the code
   **(not triggered in this scope)** rather than implying it did work.
12. **`_BODY` under `view == "commitments"`.** The pseudo-local `#BODY`
   convention names a rendered section header. When the projection exposed
   `view == "commitments"`, no BODY section was rendered at all, so the ref
   travelled through a view that never carried it: the resolution still succeeds
   (deviation D1) and `ref_through_unexposed_view` is now emitted beside
   `qualified_ref_body_pseudo_local`. Not triggered in occurrence-01 — the one
   `#BODY` ref, `rival.r1`, goes through a `view == "body"` projection — but the
   asymmetry with the real-local-name case was arbitrary.
13. **CLI exit codes.** 0 success (including an unresolvable `--why`, which
   prints `WHY_UNRESOLVED:` plus the closest candidate names to stderr and still
   returns 0, because the root is written and only the display selector was
   wrong), 2 custody refusal (including `OCCURRENCE_FILE_MISSING` and
   `OCCURRENCE_FILE_MALFORMED_JSON`, both now raised as `CustodyError` by the
   reader), 3 mapping failure, 4 out-root refused via the distinct
   `OutRootRefused` class (it inherits both `ValueError` and `FileExistsError`,
   so callers written against either keep working). argparse keeps its own
   usage-error behaviour and is not remapped; the table is in the workflow doc.
   The I7 banner is printed before the LABELS header, with an error-severity
   banner under it when any `error`-severity code fired.

---

## 6. Open questions

1. **Should a prose or empty commitments string also get a document artifact?**
   Today only a parsed FCL-1 document does. Minting one for prose would make
   every arm's commitment surface addressable by `theory(id)` at the cost of
   asserting "this is a document" where the author wrote prose. The bytes are in
   the blob store either way.
2. **`mentions_intra_document` is `lossy` at ref unit, but nothing records the
   record-level relation in the graph.** It survives only in
   `side_table.records[].mapped_to` and in the FCL-1 document artifact. If
   record-level structure ever matters, the granularity decision
   (`mapping.md` §1: one artifact per node) is the thing to revisit, not this
   code.
3. **`SpawnTrigger` has no `import` member.** Both `problem_trigger_approximated`
   (5) and `problem_trigger_research_not_in_v13_enum` (4) exist because the
   enum cannot say "carried in from another study". A one-line enum addition
   upstream would retire the first code entirely.
4. **Criticism-of-criticism retargeting is order-sensitive by construction.**
   `carry.n3 → response#k7` retargets because `k7` was reified *earlier in the
   same import*. If `k7` had minted nothing (as `rival.r9` does), the same
   authored criticism would land on the node artifact instead. That asymmetry is
   real — it reflects whether the criticised criticism actually entered the
   graph — but it means the shape of `att` depends on the scope imported. A
   scope that excludes the rival would change where `n3`'s attack lands.
5. **`provenance.role = import` on every artifact this import mints.** Node
   artifacts, FCL-1 document artifacts and validity nodes all carry it; a test
   asserts that the written root contains no other role. The validity nodes used
   to carry `CRITIC`, which says this process produced a criticism of its own. It
   did not: it transcribed one the authors wrote, and the ν's own first line
   already disclaims soundness and relevance. `IMPORT` is the honest role for all
   three.

   *Correction to an earlier version of this note.* It said `IMPORT` "excludes
   these artifacts from survivor sets" because "`state.counts_as_survivor()`
   treats `IMPORT` as admission bookkeeping". **The staged core has no survivor
   machinery at all** — `grep -rn "survivor\|counts_as" src/deepreason_core/`
   returns nothing — so there is no such exclusion to warn about today, and the
   warning as written invented a behaviour to explain a choice. `IMPORT` is
   chosen because it is true of these artifacts, and it is a **forward guard**:
   if a fuller core later distinguishes imported material from material this
   graph produced, imported material is already marked. If such a core also
   excludes `IMPORT` from a survivor report, then an empty survivor report over
   this root must not be read as "nothing survived" — but that is a conditional
   about a core that does not exist here, not a description of this one.
6. **~~Should `uptake` divergence be reported the other way too?~~ Resolved:
   the uptake-coverage claim was false.** This note used to say that a record
   *in* `uptake` which the import mapped to nothing "is already covered by
   `uptake_refs_unmapped` (32)". That reasoning fails for any record the author
   left **out** of `uptake`, and occurrence-01 has three:
   `daily/mini_fcl/cycle01/rival` declares `uptake = ["r2","r6","r7","r9"]`, so
   the claims `r1`, `r3` and `r4` were reported by nothing at all. `claim_record_
   unmapped` (severity `unmapped`, unit `record`, 15 in the golden scope) now
   fires once per `claim` record, with the verbatim record JSON, exactly as
   `use_record_unmapped` does. Its reason states that a claim in `uptake` is
   additionally covered by `uptake_refs_unmapped` and a claim outside it is
   covered by nothing else, which is why the code exists.
7. **Two importers, one occurrence, different scopes** produce different
   artifact ids for the same node when the ref set differs (a dropped
   out-of-scope ref changes the interface, which changes the content-addressed
   id). The side table makes this auditable, but it means "the spec id of
   `daily/mini_fcl/cycle01/carry`" is only well defined relative to a scope.

---

## 7. Publication checklist

* `src/minireason/graph_import_h005.py`, `src/minireason/data/fcl1.schema.json`,
  `tools/import_h005.py`, `tests/test_graph_import_h005.py`,
  `tests/data/h005_import_pins.json`,
  `docs/workflows/graph-import-h005.md` and
  `docs/design/h005-import-notes-2026-09-14.md` (this file) drop into the
  repository unchanged. There is **no** `tests/fixtures/` directory to publish:
  the tests read the occurrence itself and pin it by hash.
* **Do not publish `src/minireason/__init__.py` from this staging tree** — the
  repository already has one. The staged copy is a shim (`pkgutil.extend_path`)
  that exists only so the staged tree can be run ahead of `src/deepreason_core`
  landing in the repository; see §8.
* `pyproject.toml` needs the schema shipped as package data:
  `[tool.setuptools.package-data]` → `"minireason" = ["data/*.json"]`. The
  library also resolves the schema by filesystem path, so a source checkout
  works without it.
* `docs/workflows/README.md` should gain a row pointing at the new workflow.
* The workflow doc links this file; keep both moves together.
* The tests locate the occurrence by walking up from `__file__`, then from the
  installed `minireason` package, then from the cwd, and honour
  `H005_OCCURRENCE_ROOT`. In the repository the first candidate already matches,
  so publication needs no change. If the occurrence is absent the module
  **fails** — CI runs on a full checkout, so an absent occurrence there is a
  broken checkout and a skip would be a green run that tested nothing. A
  deliberate skip needs `H005_IMPORT_ALLOW_SKIP=1`.
* The `clock` parameter of §4 must be present in the published
  `src/deepreason_core/harness.py`.

## 8. The staging shim

With `PYTHONPATH=<importer>/src:<repo>/src` — the staged tree first, and no
separate `vendor-core` entry now that `deepreason_core` is published in the
repository — Python resolves
`minireason` to the first entry that is a *regular* package; a directory with no
`__init__.py` is only a namespace portion and loses to the repository's regular
package regardless of order. The staged `__init__.py` therefore re-declares the
package and calls `pkgutil.extend_path`, so `minireason.graph_import_h005`
comes from the staging tree while `minireason.provider` and friends still
resolve from the repository. At publish time the module simply joins the
repository package and the shim is discarded.
