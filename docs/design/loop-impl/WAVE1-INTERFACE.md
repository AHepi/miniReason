# Wave 1 — the integrated public interface

Read this before reading any wave-1 module, and read `WAVE0-INTERFACE.md` first.
It is the integrator's record of what the six wave-1 modules actually expose
after reconciliation, what changed in wave 0's modules to let them agree, and
what the six authors left open for waves 2-6.

Clone: `scratchpad/loop-impl/repo` at `9045a94`.
Sources: `src/minireason/loop/{surface,seats,obligations,graph,steps,synthetic}.py`;
tests: `tests/loop/test_{surface,seats,obligations,graph,steps,synthetic}.py`.

Verified on the quiesced tree: loop-only `704 tests OK` (before: 683, 4 failures
+ 1 error); full suite `1947 tests OK (skipped=1)` under
`PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests` (before: 1926,
4 failures + 1 error, skipped=1).

---

## 0. The one-page map

```
types ──► standard ──► contracts ──┬──► surface
  │  (LoopError)  (every vocabulary)│
  ├──► custody ──┐                  ├──► seats
  ├──► receipts ─┼──► steps          ├──► graph  (also ◄── standard)
  ├──► publish ──┘                  └──► synthetic (also ◄── standard)
  └──► obligations            (types only: it mirrors UNRESOLVED_TOKEN)
```

Exactly, as `tests/loop/test_contracts.py` walks it:

| module | imports (siblings only) |
|---|---|
| `surface` | `contracts`, `types` |
| `seats` | `contracts`, `types` |
| `obligations` | `types` |
| `graph` | `contracts`, `standard`, `types` |
| `steps` | `custody`, `publish`, `receipts`, `types` |
| `synthetic` | `contracts`, `standard`, `types` |

**No wave-1 module imports another wave-1 module.** Where two of them must
agree, the agreement is stated in a docstring and asserted by a test that
imports both — never by an import between them. There are two such agreements:

* `graph`'s `record` tokens ↔ `obligations.RECORD_KINDS` (decision 2), asserted
  by `tests/loop/test_obligations.py::AGraphW1GraphPopulatedIsReadByThesePredicates`;
* `obligations.UNRESOLVED_RELATION` ↔ `standard.UNRESOLVED_TOKEN` ↔
  `graph.UNRESOLVED` (obligations deviation 8), asserted in the same class.

---

## 1. `surface.py` — W1-SURFACE

G2(a) referential integrity by uniqueness, and G3 operative target. It opens no
file, writes nothing, and says where a quote *is*, never whether it is apt.

```python
SURFACE_SCHEMA = "minireason.loop.surface.v1";  ARTIFACT_CATEGORY = "artifacts"
SIDE_REFERRING_RECORD / SIDE_TARGET_RECORD / SIDE_REFERRING_BODY_PASSAGE / SIDE_FRAMING
DECLARED_SIDES: tuple[str, ...]          # the three G3 admits
SIDES: tuple[str, ...]                   # those three + "framing"
SOURCE_FIELDS: Mapping[str, str]         # side -> "commitments" | "body"
FIELD_COMMITMENTS = "commitments";  FIELD_BODY = "body"
LABEL_OPEN = "--- ";  LABEL_CLOSE = " ---";  LABEL_TERMINATOR = b"\n";  BLOCK_SEPARATOR = b"\n\n"
REFERENTIAL_INTEGRITY_BLOCK = "blocked:referential-integrity"   # via types.block_code
OPERATIVE_TARGET_BLOCK = "blocked:operative-target"
NEW_CODES: Mapping[str, str]             # 3, all now in types.FAILURE_CODES

build_surface(use_row: Any) -> Surface                     # a UseRow or its mapping; nothing else
resolve_unique(surface: Surface, quote: Any) -> Offset | None      # None ⇒ G2 block
within_declared_span(surface: Surface, offset: Offset | None) -> bool   # False ⇒ G3 block

class Span:    side start end occurrence_path source_field file_start file_end
               coordinate_key record_id ordinal; .length; contains(start,end); as_dict()
class Offset:  start end side occurrence_path file_start file_end
               .length .is_framing .source_field; as_dict()
class Surface: text: bytes; spans; referring_coordinate_key target_coordinate_key
               referring_record_id target_record_id ref_field ref_verbatim ref_grain schema
               .digest .decoded; occurrences(quote); count(quote); span_at(start,end); as_dict()
```

**Exception.** `SurfaceInvalid(LoopError, ValueError)` with `(code, detail="")`.
Codes: `SURFACE_ROW_MALFORMED`, `SURFACE_SPAN_DISAGREES`, `SURFACE_NO_MATERIAL`.

**Two coordinate systems, on purpose.** `Surface.text` is **bytes** and
`Offset.start/end` are utf-8 **byte** offsets into it; `Offset.file_start/file_end`
are **code-point** offsets into one named string field of one occurrence artifact
(`commitments` for a record, `body` for a passage), which is the coordinate
system `use_relation_h005` itself publishes. Never mix them.

---

## 2. `seats.py` — W1-SEATS

`(registry, config) -> SeatPlan`, byte-stable, and the one place the loop
computes a per-credential ceiling or touches runner v2's outer key gate.

```python
SEATS_SCHEMA = "minireason.loop.seats.v1";  SELECTION_RULE = "sorted family name, then sorted endpoint name"
REUSED_ROLES = {"marker": "judge"};  SEAT_ROLES = ("critic","defender","judge","variator")
HOST_SEPARATOR = "/";  MAX_PER_KEY = 5
FAMILY_COUNT_INSUFFICIENT / SEAT_COUNT_INSUFFICIENT / REGISTRY_INVALID / RUNNER_NOT_IMPORTABLE
NEW_CODES: Mapping[str, str]             # 3, all now in types.FAILURE_CODES

lineage(family: str) -> str                        # "ollama-cloud/deepseek" -> "deepseek"
load_registry(path=ENDPOINTS_PATH) -> Registry
select_seats(registry, config=None) -> SeatPlan    # None | LoopConfig | SeatsConfig | either as a mapping
require_cross_family_judges(plan) -> tuple[str, ...]        # SeatPlan, pins() mapping, or a plan body
key_cap_for(seat: Seat, max_per_key=5) -> int
key_gate_for(seat: Seat, max_per_key=5) -> threading.BoundedSemaphore   # runner v2's, imported
runner_module() -> Any

class Relaxation: seat constraint reason; as_dict()
class Seat:     role index endpoint; .name .model .family .lineage .key_env
                .timeout_seconds .max_concurrency .native .label; identity(); as_dict()
class Registry: endpoints; .names .families .lineages .key_envs .digest
                of(source); in_family(family); view()
class SeatPlan: critic defender judges variator max_per_key relaxations registry_digest families
                .seats .judge_families .judge_lineages .digest
                marker_seats(); for_role(role, index=0); key_envs(); key_caps()
                table(); canonical_bytes(); pins(); as_dict()
```

**Exception.** `SeatsRefused(LoopError)` with `(code, detail="")`.

**Lineage (integration decision 3).** `endpoints.json` spells a family as route
*and* lineage, so `deepseek` and `ollama-cloud/deepseek` are two labels over one
model — and sorted family order puts them adjacent, so the old label comparison
seated deepseek on **both** judge seats and reported two distinct families. Every
family comparison in the assignment now runs over `lineage()`; the table
publishes the labels **and** `judge_lineages`. The default table's digest moved:

```
before 10b34e4438d97c7b2e7d35bb89d83c822aee746f2b770217fabcf071c0877e95
after  2fe7829302ef88a3e239f0550a93d4a047996b394757b849b853034ed3994ed7
```

pinned as a literal in `tests/loop/test_seats.py`. The L001 bundle is unaffected:
its five seats are pinned by name and are already lineage-distinct
(kimi / gemma / gpt-oss / qwen / deepseek).

---

## 3. `obligations.py` — W1-OBLIGATIONS

O and P, their named program predicates over a registered graph, `ProducedBy`,
and the `losses_outside_P` register. **It decides nothing**, and no predicate
takes or returns a count, rate, threshold or score.

```python
OBLIGATIONS_SCHEMA = "minireason.loop.obligations.v1"
MEMBERSHIPS = ("O","P");  FAILED_SET = "O";  PROTECTED_SET = "P"
RECORD_FIELD = "record";  RECORD_KINDS: tuple[str, ...]        # 20, what a predicate reads
READING_KINDS = ("reading_row","cell_mark");  UNRESOLVED_RELATION = "unresolved"
DISPOSITION_REASONS: frozenset[str];  CELL_STATES = ("read","unresolved","machine-unresolved","unread")
APPELLATE_TOKENS: frozenset[str];  NEW_CODES: Mapping[str, str]   # 18, all now in FAILURE_CODES
PREDICATES / PREDICATE_QUESTIONS / PREDICATE_READS: Mapping      # 19 named programs

predicate(name: str) -> Predicate                      # "obligations.<name>" prefix stripped
load_obligations(path) -> Obligations
pin(obligations: Obligations) -> str                   # the FILE's sha256, not the structure digest
evaluate(obligations, situation) -> Evaluation
produced_by(situation, obligation_id) -> frozenset[str]        # attribution AND dependence
losses_outside_p(prev: Situation | None, curr) -> list[Loss]   # present even when empty
protected_losses(prev: Situation | None, curr) -> list[Loss]

class Verdict(str, Enum):  SATISFIED | NOT_SATISFIED | NOT_EVALUABLE      # no fourth, no order
class Check:      verdict evidence detail; .holds; satisfied()/not_satisfied()/not_evaluable(); as_dict()
class Node:       id status role record text; .kind .stands
class Situation:  cycle obligations nodes attacks supports registered; .cycle_token
                  from_harness(harness, *, cycle, obligations, registered=()) -> Situation
                  without(ids); records(kind); standing(kind); one(kind)
class Obligation: id membership statement check reads detail why; .is_protected .predicate; as_dict()
class Obligations: entries source_bytes path preamble structure_digest
                  .failed .protected .ids .pin; by_id(id); as_dict()
class Loss:       kind subject was now membership detail; as_dict()
class Evaluation: pin cycle obligations checks produced_by
                  verdict(id); .satisfied .not_satisfied .not_evaluable .failed
                  .every_o_satisfied .protected_not_evaluable .discharged; as_dict()
```

**Exception.** `ObligationsError(LoopError)` with `(token, detail="")`.

`Situation.from_harness` is the one adapter from a `deepreason_core` harness,
and it is how W5-DRIVER builds a situation. It reads statuses from the two-pass
adjudication and writes nothing.

---

## 4. `graph.py` — W1-GRAPH

The six artifact shapes, the rubric-typed demonstrative warrant, the audit and
appellate paths, and the read-back of a cell's standing. Every label comes from
the vendored adjudicator; this module never writes `status`.

```python
CELL_OPEN_SCHEMA / READING_SCHEMA / VALIDITY_SCHEMA / AUDIT_SCHEMA / APPEAL_SCHEMA
PRODUCED_SCHEMAS: tuple[str, ...]                      # those five
RECORD_FIELD = "record"
RECORD_KINDS: Mapping[str, str]        # token -> schema; cell_open, reading_row, cell_mark,
                                       # validity_node, audit_record, appellate_ruling
RECORDS_NOT_READ: Mapping[str, str]    # validity_node, appellate_ruling, with the reason each
KAPPA_READ_PREFIX = "kappa:read:";  KAPPA_AUDIT_PREFIX = "kappa:audit:"
AUDIT_KINDS = ("paraphrase-invariance","premise-deletion","planted-flaw-calibration")
CELL_STATES = ("unresolved","read","contested","suspended","unsupported")
UNRESOLVED / READ / CONTESTED / SUSPENDED / UNSUPPORTED
G12_EXEMPT: Mapping[str, str]          # the two vendored shapes the scan does not walk (O2)
NEW_CODES: Mapping[str, str]           # 19, all now in types.FAILURE_CODES

fixed_clock(stamp="2026-01-01T00:00:00+00:00") -> Callable[[], str]
resolve_graph_root(repo_root, graph_root: str) -> Path         # O1: the declared root wins
open_graph(root, *, clock=None, upto_seq=None, read_only=None) -> Harness
register_standard(harness, body=STANDARD_BODY, *, mention=None) -> str
register_kappa_read(harness, spec_id="reading-v1") -> str
register_material(harness, row: bytes | str, *, codec="json", role="import") -> str
open_cells(harness, keys, *, material_id=None, commitment_id=None) -> dict[str, str]
register_transcript(harness, transcript: Transcript) -> str            # trace_ref
split_validity_nodes(harness, result, standard_id) -> ValidityNodes
register_reading(harness, result: ReadingResult, standard_id: str) -> ReadingIds
register_mark(harness, result: ReadingResult, standard_id: str) -> ReadingIds
validity_nodes_for_seat(harness, seat: str) -> tuple[str, ...]
register_audit_warrant(harness, finding: AuditFinding) -> str
apply_appeal(harness, ruling: AppellateRuling) -> str
appellate_rulings(harness) -> tuple[str, ...]                  # an ordering, never a standing
cell_standing(harness, key) -> CellStanding;  cell_state(harness, key) -> str
cell_standings(harness) -> tuple[CellStanding, ...]
mark_triples(harness) -> frozenset[tuple[str, str, str]]       # W2-DECIDE's comparison set
produced(harness, *, since_seq=0) -> Production                # ProducedBy's intersection set

class CellKey:        cell register comparison; .token .is_register_cell .mode; as_dict(); coerce(v)
class Transcript:     case answer decisive_point checks meta; .exchange; validated()
class ReadingResult:  key relation seat transcript body roles difference_kind school
                      material_id llm; validated()
class ReadingIds:     key target reading soundness bearing evidence transcript warrant; .artifact_ids
class ValidityNodes:  soundness bearing evidence
class AuditFinding:   seat kind detail targets body; validated()
class AppellateRuling: ruling_id target ground standard_id body; validated()
class CellStanding:   key state default_id default_status standing accepted relation register
class Production:     artifact_ids upto_seq
```

**Exception.** `GraphError(LoopError)` with `(code, detail="")`.

**`graph` is the writer of `record` (decision 2).** Every loop-authored body
carries `record: <token>` from `RECORD_KINDS` beside its `schema`. The **material
carries none**: §3(b) registers the instrument's bytes exactly as emitted, so the
`material` record `p1` and `o3` read is a record *about* the material that
W5-DRIVER registers beside it.

---

## 5. `steps.py` — W1-STEPS

One run's `<run_root>/steps/` directory: step keys, `.open` markers, write-once
receipts, halts, acknowledgements, resume, the run lock, and publication.

```python
MARKER_SCHEMA / ACK_SCHEMA / LOCK_SCHEMA;  VERIFIED_SUFFIX = ".verified"
PUBLICATION_STEPS = ("PUBLISH_PLAN","PUBLISH_IN","PUBLISH_EV","PUBLISH_CY")
RESUME_ACTIONS = ("SKIP","REPLAY","RETRY","HALT")
STEP_OUTCOMES = ("COMPLETE","FAILED","HALTED","SKIPPED","REPLAYED")
MARKER_KEPT_CODES = {"STEP_TIMEOUT","STEP_BODY_FAILED"};  CUSTODY_HALT_CODES: frozenset[str]
NEW_CODES: Mapping[str, str]           # 5, all now in types.FAILURE_CODES

completed_coordinates(out_dir) -> set[str]
scan_coordinates(out_dir) -> CoordinateScan            # complete / indeterminate / started
erratum_text(receipt: StepReceipt, *, reason=None) -> str

class RunLock(path, loop_plan_id, *, pid=None, clock=None): .held; holder(); acquire(); release()
class CoordinateScan: complete indeterminate started
class ResumeAction:   action index kind step_key code detail; .halting
class StepRecord:     receipt path; .index .step_key
class StepOutcome:    status kind step_key index receipt value outputs verified_line; .ran
class StepHandle:     record_output(name, value); record_custody(findings); .custody
                      .elapsed_seconds; check_deadline(); complete(returned=None)
                      fail(code, detail=""); halt(code, detail=""); fail_from(exc)
class StepLedger(run_root, loop_plan_id, *, timeouts=None, ledger_path=None,
                 receipt_id=None, clock=None, monotonic=None)
      now(); monotonic(); records(); markers(); marker_body(path); acknowledgements()
      next_index(); step_key(kind, cycle=None, wave=None, inputs=None)
      latest(step_key); completed(step_key); attempts_for(step_key)
      pending_publication(); verified_line(step_key); resume_plan(); blocking()
      guard(step_key=None); begin(kind, ...); run_step(kind, cycle, inputs, fn, spending=None, ...)
      publish_step(kind, repo, paths, message, *, ref=None, cycle=None, wave=None,
                   inputs=None, publisher=None, git=None, sleep=None, now=None)
      unresolved_for(step_key); acknowledge(step_key, reason)
```

**Exceptions.** `StepError(LoopError)` with `(code, detail="")`, and
`UnresolvedStep` (`UNRESOLVED_STEP`), `StepNondeterministic`
(`STEP_NONDETERMINISTIC`), `StepTimeout` (`STEP_TIMEOUT`), `PublishBlocked`
(`PUBLISH_PENDING`), `RunLocked` (`RUN_LOCKED`), and `StickyHalt(code, ...)`,
which re-raises the halted receipt's **own** code.

**The ledger rule.** `ledger_path=` names a ledger that **already exists**; the
loop never creates one (`receipts.ledger_append` is called with `create=False`).
A missing path is `LEDGER_NOT_FOUND` at the first publication — a misconfigured
driver named at once, rather than a second `DECISION_LEDGER.md` started quietly
beside the real one. Tests create their temp ledger first (or call
`ledger_append(..., create=True)` themselves); the driver resolves the path from
the run's own repository root and never from `receipts.DEFAULT_LEDGER_PATH`,
which is `None` outside a source checkout.

---

## 6. `synthetic.py` — W1-SYNTHETIC

The material half of the offline dry-run gate: one small H005 occurrence and the
scripted role outputs, from a seed and nothing else. No socket, no credential.

```python
SYNTHETIC_SCHEMA = "minireason.loop.synthetic.v1";  DEFAULT_SEED = 9005
PROBLEM_ID = "synth";  TEMPLATE_ID = "probe";  NODE_IDS = ("account","objection","response")
FCL_ARM = "mini_fcl";  PROSE_ARM = "mini_prose";  ARM_NAMES;  JUDGE_SEATS = ("judge-a","judge-b")
SYNTHETIC_FAMILIES / SYNTHETIC_KEY_ENVS / SYNTHETIC_ENDPOINTS;  endpoints_registry()
INDUCIBLE: tuple[str, ...]             # 10 tokens
INDUCED_CODES: Mapping[str, str]       # token -> the code the receipt must name
NEW_CODES: Mapping[str, str]           # 3: two in FAILURE_CODES, one in OUTCOME_CODES
READING_PLAN / READING_COORDINATES / REREAD_SUFFIX / PARAPHRASE_SUFFIXES
UNRESOLVABLE_REFS / FAILED_COORDINATE / DUPLICATED_PHRASE / RECORDED_MOMENTS
CONTRAST_CASES / CONTRAST_REPLICATES / BASELINE_KINDS

material_document(seed=9005); arms_document(); endpoints_document()
delivery_content(arm, node, seed=9005) -> str
build_occurrence(directory, *, induce=(), seed=9005, freeze=None) -> Occurrence
runner_freeze(repo) -> Callable[[Path, Path, Path], Mapping[str, Any]]
canned_responses(seed=9005, *, induce=()) -> dict[tuple[str, str], tuple[dict, ...]]
provider_factory(*, seed=9005, induce=(), strict=False) -> ScriptedProviders
contrast_leg(seed=9005) -> dict;  appellate_ruling(seed=9005) -> dict
describe(induce=INDUCIBLE) -> tuple[Induced, ...]

class Induced:  token code step subject aggregate_code note; as_dict()
class Occurrence: root material arms plan manifests contrast appeal custody endpoints ...; as_dict()
class ScriptedProviders(*, seed=9005, induce=(), strict=False)
      script_for(role, coordinate, *, seat=None); endpoint_for(role, seat=None)
      provider(role, coordinate, records_dir, *, seat=None, endpoint=None)
      coordinate_of(records_dir)
```

**Exceptions.** `SyntheticError(LoopError)`; `SyntheticStepTimeout(SyntheticError)`
with `.code == "STEP_TIMEOUT"`.

---

## 7. The code tables after wave 1

`types.FAILURE_CODES` now holds **159** codes and is complete for all twelve
modules: `tests/loop/test_types.py::TheCodeTablesAreComplete.FOLDED_IN` names
every one, and `test_every_module_of_the_package_is_folded_in` fails if a
thirteenth module appears without its codes. Folded in this wave:

| module | new codes | where |
|---|---|---|
| `surface` | 3 | `FAILURE_CODES` |
| `seats` | 3 | `FAILURE_CODES` |
| `obligations` | 18 | `FAILURE_CODES` |
| `graph` | 19 | `FAILURE_CODES` |
| `steps` | 5 | `FAILURE_CODES` |
| `synthetic` | 3 | 2 in `FAILURE_CODES`, `APPELLATE_RULING_APPLIED` in `OUTCOME_CODES` |

`types.OUTCOME_CODES` is new: an UPPER_SNAKE token naming **something the loop
did**, where `FAILURE_CODES` names something it refused. One member,
`APPELLATE_RULING_APPLIED`, with `is_outcome_code()` beside `is_failure_code()`.
The four tables — `BLOCK_CODES`, `SCHEMA_REASONS`, `FAILURE_CODES`,
`OUTCOME_CODES` — are pairwise disjoint and the scan asserts it. The scan's
`TOKEN_ARGUMENT` gained `("obligations","_refuse")`, `("obligations","ObligationsError")`,
`("graph","GraphError")`, `("steps","StepError")`, `("steps","StickyHalt")`,
`("synthetic","SyntheticError")`, each at index 0.
`STEP_BODY_FAILED` is in `UNREACHED`: `steps._classify` writes it onto a FAILED
receipt rather than raising it.

---

## 8. The reconciliations this integration made

1. **p7 refined, not relaxed** (decision 1). `no_edges_on_studied_nodes` now asks
   two questions: no `att` edge may target a studied node, and no studied node
   may be the **source** of any edge. A `dep` onto a studied node is permitted —
   it is the edge §3 requires so that refuting the material leaves a reading
   `suspended_unsupported` rather than refuted. *The bundle's p7 sentence must
   be reworded at the pre-registration review.*
2. **`record` has one writer** (decision 2). `graph` writes
   `obligations.RECORD_FIELD` into every body it authors; `obligations` reads
   exactly those tokens. The material is the named exception. The two extra
   tokens `graph` writes (`validity_node`, `appellate_ruling`) are declared in
   `graph.RECORDS_NOT_READ` with the reason each is unread.
3. **Judge distinctness is over the lineage** (decision 3) — §2 above.
4. **`mark_triples` is the identity W2-DECIDE compares** (decision 4), stated
   conjunct by conjunct in its docstring: membership is by `(cell, register,
   mark)` triple, an unresolved default contributes its `unresolved` triple, a
   contested or unsupported cell contributes none, a relation cell contributes
   none, and the comparison is set identity — no count, no fraction, no direction.
5. **o5 is a membership test** (decision 5), never `current_cycle - n < period`.
   *The bundle's o5 sentence must be reworded at the pre-registration review.*
6. **The wave-0 fix pass's behaviour changes, checked against every wave-1 call
   site** (decision 7):
   * `AuditConfig` accounts — only `tests/loop/test_seats.py`'s `CONFIG` fixture
     lacked them; it now carries both, and the L001 bundle's `config.json` gained
     two accounts marked `PROVISIONAL, to be settled at pre-registration review`.
   * `assert_no_scoring_keys` raising on `str`/`bytes` — no wave-1 call site
     passes a string (`surface:475`, `graph:750`, `graph:963-964` all pass
     mappings), and `test_graph` already asserts the `str` refusal indirectly.
   * `SeatsConfig` ranges — no wave-1 fixture declares `paraphrase_n=0` or
     `schema_repair_budget=1`.
   * `LocalGit` allow-list — no wave-1 module or test uses `LocalGit`; `steps`
     reaches `publish` only through `publish_module.publish`, and
     `tests/loop/test_steps.py` shells `git` itself through `subprocess`.
   * `verify_published` comparing the committed tree — no wave-1 caller.
   * `ledger_append(create=)` — `steps.py:1106`, §5 above.
   * `DEFAULT_REPO_ROOT` / `DEFAULT_LEDGER_PATH` possibly `None` — `steps` takes
     both explicitly and defaults to "no ledger wired", never to the module default.
   * `receipts.activity` under `check=True` — no wave-1 caller.
   * `custody.write_new` fsyncing the parent — `steps` is a caller and needs no change.
   * `STANDARD_BODY_SHA256` moving to `b4dc7f6a…` — no wave-1 module or bundle
     file names it.
   * the critic normalisation (relation + `outside_vocabulary` ⇒ relation `none`,
     `.nominated_relation` kept) — `synthetic._critic_output`'s
     `read/unresolved-b` coordinate is exactly this shape and is unaffected: it
     reads the record, never `.relation`.
7. **`__init__.py`** carries the wave-1 import graph and the "no wave-1 module
   imports another" rule (decision 8).

### The `not_evaluable` allow-list (decision 2)

On a graph populated **only** through `graph.py` — standard, material, two
unresolved defaults, one reading, one mark, one audit finding — four predicates
reach a verdict (`o3`, `o5`, `p6`, `p8`) and fifteen answer `not_evaluable`
because their records are W4-READER's and W5-DRIVER's. The list is pinned as
`NOT_EVALUABLE_UNTIL_W4_W5` in `tests/loop/test_obligations.py`:

| id | predicate | waiting for |
|---|---|---|
| o1 | `row_disposition_complete` | `reading_set` |
| o2 | `mark_disposition_complete` | `reading_set` |
| o4 | `blocks_named` | `disposition` |
| o6 | `baseline_sealed_and_carried` | `baseline` + `reading_set` |
| o7 | `trichotomy_rendered` | `rendered_states` + `reading_set` |
| p1 | `original_bytes_unchanged` | `material` |
| p2 | `recoding_table_complete` | `recoding_table` |
| p3 | `shared_envelope_intact` | `case_request` |
| p4 | `no_scoring_key` | `forbidden_keys` |
| p5 | `write_once_no_replay` | `call_record` |
| p7 | `no_edges_on_studied_nodes` | `study_set` |
| p9 | `baseline_still_pinned` | `baseline` |
| p10 | `published_unresolved_preserved` | `published_unresolved` |
| p11 | `published_tree_untouched` | `pinned_digests` + `observed_digests` |
| p12 | `ceiling_and_trichotomy_intact` | `ceiling` + `rendered_files` |

A predicate that silently stops reading a record `graph` *does* write fails that
test; a predicate that starts reading one only has to leave the table.

---

## 9. Open questions the six authors left, with a recommendation

The authors' own reports are not in the tree; the items below are the open
questions their modules' docstrings, deviations and notes leave for waves 2-6,
numbered as the integration brief numbers them.

### `surface`

**S1 — two coordinate systems.** Byte offsets into `Surface.text`, code-point
offsets into an artifact string field. *Recommendation (W2-PACKS, W4-READER):*
never convert; carry `Offset.as_dict()` whole into the reading record, and let
the re-resolution check be the published one —
`json.load(occurrence/path)[field][file_start:file_end] == quote`.

**S2 — `framing` is a fourth side and the two block codes are different facts.**
`resolve_unique` returning `None` is `blocked:referential-integrity`; returning a
`framing` offset is `blocked:operative-target`. *Recommendation (W3-REPORT):*
print the two codes separately in the block register — collapsing them loses the
distinction between "the quote is not in the material" and "the quote is in the
prompt's own scaffolding", which is the one G3 exists for.

**S3 — occurrences are counted overlapping**, which is strictly stronger than
`bytes.count`. *Recommendation (W4-READER):* call `Surface.count`, never
re-implement it; a second counter is a second thing to drift.

**S4 — `build_surface` accepts only a `UseRow` or its mapping.**
*Recommendation (W1-STEPS' `USE_TABLE` step):* publish `use_table.json` rows in
exactly the instrument's own shape, and let `build_surface` be the only reader
of them.

**S5 — the label vocabulary is this module's choice and is inside
`Surface.digest`,** which is *not* inside `loop_plan_id`. Changing a label
silently changes every surface digest. *Recommendation (W2-PACKS):* pin
`Surface.digest` into the pack record so the change is visible in a diff; if a
future run wants it in the plan identity, that is a successor standard.

**S6 — which coordinate a row becomes is not this module's.**
*Recommendation (W4-READER):* mint `graph.CellKey` from the row key at the
reader, and never inside `surface`.

**S7 — the material is never paraphrased.** §2.3's variator paraphrases the
*exchange*. *Recommendation (W2-ROLES):* pass `Surface.text` unchanged to every
seat and paraphrase only `case`/`answer`; a test that the material bytes reaching
seat *n* equal the bytes reaching seat 0 belongs in W2.

### `seats`

**Q1 — `max_tokens` is not a registry field**, so it is not seat identity.
*Recommendation (W2-ROLES):* pin the `max_tokens` it passes into the **call
record**, and state it in the pack, so a changed bound is visible even though it
cannot be in the seat table. **And choose it against the 300 s wall, not against
the endpoint's declared timeout** — see Q7.

**Q7 — the Ollama cloud host closes any request still open at 300 s, whatever
`timeout_seconds` says** (observed four times on 2026-09-14: F002 occurrence-01
`glm-5.3` at 300,270 ms, and three `kimi-k3` calls from a separate worker
process, each closed 300-301 s after its request, with "Remote end closed
connection without response"). The endpoint's own `timeout_seconds` is what
design §4.4 layer 1 reads off the frozen plan and what `TIMEOUT_NOT_APPLIED`
guards — but a 600 s value **cannot be exercised past 300 s on that host**, and
at the observed ~90-100 tokens/s a 32768-token ceiling is not reachable inside
the wall. The registry's own 180 s entries are inside it; a raised one is not.
*Recommendation (W2-ROLES):* pin `max_tokens` **per seat** so that expected
generation stays well under 300 s on every `ollama-cloud/*` seat, and record the
arithmetic (tokens ÷ observed rate) beside the number, so the bound carries its
account like an audit threshold does. *Recommendation (W5-DRIVER):* the provider
block code must carry this wall as a **named reason** rather than as a bare
transport error — a call the host closed at 300 s is a delivery fact about the
route, not a reading, and a receipt that says only `TRANSPORT_OR_RESPONSE_ERROR`
loses the one thing that would let the next run plan around it. Neither this nor
`timeouts.step_seconds` may be used to *raise* the plan's layer-1 timeout: the
wall is shorter than the declaration, and the honest record says so.

**Q2 — `max_concurrency` is pinned although §2.2's list stops at
`timeout_seconds`,** because it is `key_cap_for`'s input. *Recommendation:*
leave it; it is the difference between an authorisation that is pre-registered
and one that can be widened without a new plan.

**Q3 — the judge seat count is `seats.min_judge_families`.**
*Recommendation (W5-PREFLIGHT):* assert it equals
`standard.GUARD_PARAMETERS["min_judge_families"]` through
`standard.assert_config_matches_standard`, which is already the one place the
standard wins.

**Q4 — the marker has no seat.** *Recommendation (W2-MARKPREP):* use
`plan.for_role("marker", index)`, which resolves to the judge at that index;
never mint a marker identity.

**Q5 — two gates, not three.** `key_gate_for` imports runner v2's `key_gate`;
the provider acquires `slots_for` itself. *Recommendation (W5-DRIVER):* acquire
the outer gate per `key_env` from `plan.key_caps()` and add nothing.

**Q6 — lineage and a successor registry.** The rule now refuses two judges of
one lineage; a registry that adds a third route to an existing lineage narrows
the admissible panel silently. *Recommendation (W5-PREFLIGHT):* assert on the
**frozen** plan (not a rebuild) that `judge_lineages` are distinct, by calling
`require_cross_family_judges(plan_body)`; a registry change that makes the frozen
plan unbuildable is then a named refusal rather than a surprise.

### `obligations`

**OB1 (W2-DECIDE) — `losses_outside_p` / `protected_losses` take *situations*,**
not evaluations, because a loss register needs both the verdicts and the
artifacts' standing. `prev` may be `None` before cycle 1 and the return is then
present and empty. *Recommendation:* `decide(prev, curr, ...)` holds the two
situations and calls both; it never recomputes a loss itself.

**OB2 (W5-DRIVER) — fifteen predicates are waiting for records the driver
writes** (§8 table). *Recommendation:* write them as ordinary registered
artifacts carrying `record: <kind>`, in the `CYCLE_OPEN`/`DECIDE` steps, and
treat the allow-list as the driver's checklist: when it is empty the obligations
document is fully readable.

**OB3 (W2) — the mirrored `UNRESOLVED_RELATION`.** Asserted now, in
`tests/loop/test_obligations.py`, against `standard.UNRESOLVED_TOKEN` and
`graph.UNRESOLVED`. *Recommendation:* leave the mirror; the import would put
`standard` in `obligations`' dependency set for one string.

**OB4 (pre-registration review) — p7 and o5 must be reworded**, §8 items 1 and 5.
*Recommendation:* reword both in the same review, and record in the bundle that
the program was written to the refined statement, not the other way round.

**OB5 (W2-DECIDE) — `Situation.without` restricts the view; it does not
re-adjudicate.** *Recommendation:* for the stronger counterfactual, build the
prior situation from `Harness.at(seq)` and compare; say in the record which of
the two was used, because they can disagree.

### `graph`

**G1 (W2-PACKS) — `appellate_rulings()` is an ordering, never a standing.**
*Recommendation:* rank precedents first in a judge pack, and let W3-REPORT state
when there are none — the ceiling already requires `appellate_rulings: N`.

**G2 (W3-REPORT) — two cell-state vocabularies, at two grains.**
`graph.CELL_STATES` is five adjudication states (`unresolved`, `read`,
`contested`, `suspended`, `unsupported`); `obligations.CELL_STATES` is the four
*printed* states the ceiling promises (`read`, `unresolved`,
`machine-unresolved`, `unread`). Nothing maps one to the other yet.
*Recommendation (W3-REPORT owns the map, and must publish it):* `read` → read;
`unresolved` with a reading attempt on record → unresolved; `contested`,
`suspended`, `unsupported` and every guard block → machine-unresolved, naming the
block code; a cell with no attempt at all → unread. The map is a claim and
belongs in the rendered record, not in a helper.

**G3 (W3-TRIAL / W4-MARKER) — `ReadingResult.body` passes through verbatim.**
That is where `citation`, `offsets` and the reader's own fields arrive in the
record `o3` reads. *Recommendation:* W4-READER writes `citation: {quote,
surface}` naming the W5 `material` record, which is what makes o3 satisfiable.

**G4 (W5-PREFLIGHT) — O1, `config.graph_root` vs `RunPaths.graph`.**
`resolve_graph_root` treats the declared root as authoritative.
*Recommendation:* assert `repo_root / config.graph_root == RunPaths(...).graph`
unless the operator declared otherwise, and record which.

**G5 (W3-REPORT) — G12's boundary is named, two artifacts wide** (`G12_EXEMPT`).
*Recommendation:* run `assert_no_scoring_keys` over loop-authored content only,
and `assert_no_scoring_headers` over every rendered file; never widen the
exemption and never narrow `FORBIDDEN_KEYS`.

### `steps`

**ST1 (W5-DRIVER) — O7, the publication attempt count.** `attempts_for(step_key)`
keeps it in the ledger and `publish_step` passes `attempt=`; a `PENDING` result
blocks every successor until a later attempt lands. *Recommendation:* never
reset the count by hand; `PublishNotConverging` at the third attempt is the
designed end.

**ST2 (W5-DRIVER) — the ledger is never created by the loop** (§5).
*Recommendation:* resolve `ledger_path` from the run's repo root at
`PREREGISTER` and assert it exists in `PREFLIGHT`, beside the
`tools/repo_activity.py` assertion O3 asks for.

**ST3 (W5-DRIVER / N5) — one publish step can exceed the 300 s cadence deadline
by construction** (5×90 s of git timeout + 30 s of backoff).
*Recommendation:* `Cadence.check` **before** a publish step starts and a
checkpoint receipt written on the way in; `CadenceMiss` already records the miss
honestly, and the point is to not be surprised by it. The same 300 s appears
again, for a different reason, in seats Q7: the Ollama cloud host closes a
request open at 300 s. The two are unrelated numbers that happen to coincide —
one is AGENTS.md's cadence rule, the other is a remote's socket — and a record
that conflates them would report a routine publish as a provider failure.

**ST4 (W6-DRYRUN) — the resume paths need an induced kill.**
*Recommendation:* the dry-run gate kills mid-`SEND` and mid-`IMPORT` and asserts
`UNRESOLVED_STEP` then `REPLAY`; `RunLock` should be exercised from two
processes, not two threads (the wave-0 review's S9 lesson).

**ST5 (W3-REPORT) — `scan_coordinates`' `indeterminate` set must reach the
record.** A coordinate with a request but no response is `INDETERMINATE` and
never an absence. *Recommendation:* print it as its own row, beside the block
register, and never fold it into "unread".

### `synthetic`

**SY1 (W6-DRYRUN) — D3: the canned `provider/` records are shaped like the
offline provider's, not recomputed from runner v2's `payload_for`,** so the
importer's custody chain is exercised and runner v2's
`read_terminal`/`decode_contribution` leg is not. *Recommendation:* drive
`send_round` with `provider_factory()` in the gate when that leg is wanted, and
say in the gate's record which of the two was exercised.

**SY2 (W5/W6) — D2: pass `freeze=runner_freeze(repo)`** so runner v2 writes
`plan.json` and `manifests/`; without it the manifests are honest stand-ins that
say so in their own bytes. *Recommendation:* the gate passes it; a run that did
not must print that its plan was frozen by the fixture.

**SY3 (W6-DRYRUN) — `APPELLATE_RULING_APPLIED` is an outcome.** It is now in
`types.OUTCOME_CODES`, disjoint from `FAILURE_CODES`. *Recommendation:* the
closing receipt names it in an *outcomes* line, never in the block register, and
W3-REPORT keeps the two lists apart.

**SY4 (W6-DRYRUN) — every induced token must be asserted in the receipt it
belongs to.** `describe()` gives `(token, code, step, subject, aggregate_code)`
for all ten. *Recommendation:* the gate asserts, per token, that the named code
appears on a receipt of the named step kind — the induction is worthless if
nothing checks where it landed.
