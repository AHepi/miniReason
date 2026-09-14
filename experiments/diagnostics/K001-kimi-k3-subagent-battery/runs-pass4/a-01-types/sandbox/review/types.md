# Adversarial review — W0-TYPES (`src/minireason/loop/types.py`)

Reviewed against `notes/WAVE0-INTERFACE.md` (§1, §7), the module's own
docstrings, and the acceptance clause it is answerable to in
`design/design-s7-wave-plan.md`:

> `"acceptance":"Two loads of one config give the same plan_id; a changed pin
> changes it; an unknown config key is refused; the token 'exhaustion' appears
> in no vocabulary; every block code used anywhere in the package is a member
> of BLOCK_CODES."`

and against `design/design-s2-roles-and-guard.md` §2.4/§2.5 for the seats,
guard-parameter and code-table claims.

All findings below were executed with probes under `probe/` (run as
`python3 probe/<name>.py` in this sandbox; verbatim output is quoted). Probes
import the package from the in-sandbox `src/`. I did not edit anything under
`src/`.

Note on scope of evidence: the sandbox snapshot ships **no**
`tests/loop/test_types.py` (`tests/loop/` contains only an empty
`__init__.py`), so the source-scanning completeness test the docstrings
reference could not be executed; I re-ran its cheap halves myself in
`probe/p07_acceptance.py`.

---

## BLOCKER

### B1 — `CustodyReport.from_mapping` (and `from_findings`) silently shred a bare-string `checks` into single characters, while the constructor refuses the same input

**Where.** `src/minireason/loop/types.py:1018` (`from_mapping` body:
`checks=tuple(raw.get("checks", ()))`) and `:1046` (`from_findings` body:
`rows = tuple(findings)`). Both bypass `_sequence()`, which is the helper that
forbids `str`/`bytes` (`:549`: `if isinstance(value, (str, bytes)) or not
isinstance(value, Sequence): raise ...`). The constructor path
(`__post_init__`, `:995–1002`) does use `_sequence`.

**Contradicted text.** The module's own loading doctrine, `LoopConfig`
docstring (`:713–714`): *"Loading is strict: an unknown key is refused rather
than ignored, because a key the loader drops is a pre-registration the run
does not honour."* And the `CustodyReport` docstring (`:988–990`):
*"``checks`` holds stable codes - a :data:`FAILURE_CODES` member, a pinned
path - not prose: a receipt is read by a program."* A JSON receipt reading
`"checks": "SOURCE_PIN_MISSING"` (a string where a list belongs — the single
most likely authoring slip for this field) is not refused; it is retyped into
19 one-character "codes" that a program will read as 19 distinct custody
failures. The invariant *verified ⇔ no findings* also breaks: the same
mistake through the interface record's advertised `from_findings(findings)`
adapter (`notes/WAVE0-INTERFACE.md` §1: *"accepts any object with a `.code`,
or a bare string"* — singular finding) explodes one finding into many.

**Probe** — `probe/p01_custody_checks_string.py`:

```
constructor(bare string): refused CONFIG_INVALID_VALUE: custody.checks must be a list
from_mapping(bare string): ACCEPTED, checks = ('S', 'O', 'U', 'R', 'C', 'E', '_', 'P', 'I', 'N', '_', 'M', 'I', 'S', 'S', 'I', 'N', 'G')
as_dict: {'verified': False, 'checks': ['S', 'O', 'U', 'R', 'C', 'E', '_', 'P', 'I', 'N', '_', 'M', 'I', 'S', 'S', 'I', 'N', 'G']}
from_findings(bare string): verified = False checks = ('S', 'O', 'U', 'R', 'C', 'E', '_', 'P', 'I', 'N', '_', 'M', 'I', 'S', 'S', 'I', 'N', 'G')
```

The same receipt, whether constructed directly or loaded from disk, therefore
produces two different `CustodyReport` values for what was meant to be one
record — and `StepReceipt.from_dict` routes through `CustodyReport.from_mapping`
(`:1103`), so this lands on the receipt round-trip seam.

**Repair.** In `from_mapping`, pass `checks` through `_sequence` (or through
the constructor unchanged, since `__post_init__` already validates); in
`from_findings`, refuse `isinstance(findings, (str, bytes))` and iterate
otherwise.
**Test that holds it.** `tests/loop/test_types.py`:
`with self.assertRaises(LoopError): CustodyReport.from_mapping({"checks": "SOURCE_PIN_MISSING"})`
and the same for `from_findings("SOURCE_PIN_MISSING")`; plus a round-trip
assertion `CustodyReport.from_mapping(x.as_dict()).as_dict() == x.as_dict()`
for a string-injection fixture.

---

## SHOULD-FIX

### S1 — `_utc` admits timestamps that are not ISO-8601 dates at all

**Where.** `src/minireason/loop/types.py:457`
(`_UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)\Z")`)
and its one consumer `_utc` (`:596–600`).

**Contradicted text.** The refusal message itself (`:598`):
*"``{where}`` must be an ISO-8601 UTC timestamp (Z or +00:00)"*. ISO-8601
months run 01–12 and hours 00–23; the regex is a shape check, not a timestamp
check, and the refusal text claims the stronger predicate. A receipt is a
write-once record read by programs; a step that "started" on the 40th of
month 13 at 25:61 passes self-validation.

**Probe** — `probe/p02_utc_impossible.py`:

```
'2026-01-01T12:00:00Z': ACCEPTED, receipt.started_utc = '2026-01-01T12:00:00Z'
'2026-13-40T25:61:61Z': ACCEPTED, receipt.started_utc = '2026-13-40T25:61:61Z'
'2026-02-30T00:00:00+00:00': ACCEPTED, receipt.started_utc = '2026-02-30T00:00:00+00:00'
'2026-01-01 12:00:00Z': refused STEP_RECEIPT_INVALID
```

**Repair.** After the regex match, parse with
`datetime.strptime(value, ...)` / `datetime.fromisoformat` (which in
3.11+ accepts `Z`) and let `ValueError` become `STEP_RECEIPT_INVALID`; require
the parsed offset to be UTC.
**Test that holds it.** `StepReceipt.build(..., started_utc="2026-13-40T25:61:61Z")`
raises `LoopError` with `.code == "STEP_RECEIPT_INVALID"`, and
`"2026-02-29T00:00:00Z"` (a leap day in a non-leap year) likewise.

### S2 — `RunPaths.reading_dir` writes the row key near-verbatim into the directory name; only the digest suffix is a secret-keeper, and nothing says truncation is injective

**Where.** `src/minireason/loop/types.py:1191–1201` (`reading_dir`).

**What it does versus what it says.** The docstring (`:1192–1198`) promises
*"a path-safe, collision-free directory"* whose *"mapping stays a pure
function of the key"*. The collision-freedom claim is true in effect because a
12-hex-char sha256 prefix is appended; but the *folded* prefix is the row key
with unsafe characters replaced by `_`, truncated to 80 chars — i.e. the
coordinate text (`problem/arm/cycle-1/node#r3`, which includes the run's own
identifiers and reading-set row keys from the config) is stored in cleartext
in every `readings/` listing, for up to 80 characters. That is not forbidden
by any clause I can quote — the docstring advertises it — so this is a design
note more than a code contradiction; but the same docstring's "collision-free"
is unqualified while the folded prefix portion *is* lossy by construction.
A reviewer reading the docstring could believe the visible name is unique; it
is not, and two keys differing only after the 80th character share a folded
prefix.

**Probe** — `probe/p03_reading_dir.py`:

```
similar key 1 -> run_alpha_arm_cycle-1_node_r3-424c38fab3e2
similar key 2 -> run_alpha_arm_cycle-1_node_r3-89b842358d12
distinct: True
plaintext run_id/leak check: True
unicode fold: caf__x-2aac9a7e759d | cafexq-3ff99c1cae50 distinct: True
same-slug pair: a_b_c-f0dad2cf5f3e | a_b_c_c-b4587b2cb04b folded slugs: ['a_b_c', 'a_b_c_c'] distinct dirs: True
```

**Repair.** Either state in the docstring that the folded prefix is
(1) cleartext coordinate text and (2) lossy (uniqueness lives entirely in the
digest), or hash the whole thing and drop the folded prefix. The first repair
is one sentence.
**Test that holds it.** Assert `reading_dir(a) != reading_dir(b)` for a pair
of keys sharing their first 80 characters and folding alike, and assert the
folded prefix is *not* claimed injective: the test should pin the documented
contract, whichever repair is chosen.

---

## NOTE

### N1 — `_relative` silently canonicalises `a/./b` to `a/b`, so two syntactically different config files can compute the same `loop_plan_id`

**Where.** `src/minireason/loop/types.py:526–537` (`_relative`: returns
`Path(text).as_posix()`, which collapses `.` segments).

**Observation.** `loop_plan_id` claims identity over "every declared value"
(docstring `:937–941`: *"Formatting, key order and resolved defaults are
therefore not part of the identity, but every declared value is"*). A declared
occurrence `"a/./b"` and a declared occurrence `"a/b"` are different bytes in
the config file but hash identically. This is almost certainly the intended
normalisation (both denote the same repo path, and refusing the `.` form would
be the alternative), but the docstring's "every declared value" is slightly
stronger than the implementation. Probe output (`probe/p08_more.py`,
re-run version):

```
'a/../b' occurrence refused: CONFIG_INVALID_VALUE
'a/./b' occurrence accepted as: ('a/b',)
```

(`..` is refused; only the `.` segment is collapsed. `//a`, `~`-prefixed,
backslash-bearing and absolute forms are all refused — see `p09_ids.py` and
`p08_more.py`.)

**Repair.** One clause in the `loop_plan_id` docstring: "repo-relative path
fields are canonicalised (`a/./b` is `a/b`) before hashing."
**Test.** Two configs differing only as `"a/./b"` vs `"a/b"` produce equal
`loop_plan_id`s, pinning the normalisation as deliberate.

### N2 — `max_calls` admits 0 while `cycle_budget` admits no less than 1, and `provider_mode` still defaults to `offline`; a config can declare a run that can take one cycle with zero calls

**Where.** `src/minireason/loop/types.py:877`
(`max_calls=_whole(raw["max_calls"], "max_calls", low=0, high=1_000_000)`).

**Observation.** Nothing in the design or interface assigns `max_calls = 0` a
meaning; design §4.2 lists it as a budget and `cycle_budget`'s floor is 1.
This is plausibly deliberate (0 = "no provider calls at all", consistent with
the `offline` default), but no docstring says so, and a run configured this
way stops at `resource_boundary` having spent nothing — by boundary, not by
inquiry outcome, which is fine, but it deserves one line. Probe
(`probe/p05_tables.py`): `max_calls=0 accepted: 0`.

**Repair.** Either set `low=1` or document that 0 is the never-spend
declaration. **Test.** Pin whichever is chosen.

### N3 — `REPLAYABLE_STEPS ∪ SPENDING_STEPS` does not cover `STEP_KINDS`; four kinds are neither

**Where.** `src/minireason/loop/types.py:634–645` vs `:619–625`.

**Observation.** `probe/p05_tables.py` printed:
`kinds in neither: ['CLOSE', 'CYCLE_OPEN', 'PREPARE', 'PREREGISTER']`.
The docstrings describe `REPLAYABLE_STEPS` (`:631`) and `SPENDING_STEPS`
(`:635`) as disjoint subsets but never claim they partition `STEP_KINDS`, and
the interface record (`notes/WAVE0-INTERFACE.md` §1) says the same. The gap is
load-bearing only in W1-STEPS' resume logic, which must decide what an open
marker for `PREREGISTER` means on resume. If the intended reading is "neither
replayable nor spending ⇒ treated like replayable" (all four are offline and
deterministic), that rule lives nowhere in this module.

**Repair.** Export a third named set (`NON_SPENDING_STEPS`) or state the
resume rule for unclassified kinds in the module docstring.
**Test.** A test asserting the four unclassified kinds by name, so a future
edit that adds a kind without classifying it fails loudly.

### N4 — `SeatsConfig` admits `judges` named without any family-distinctness or count check beyond `min_judge_families`, and cannot say so

**Where.** `src/minireason/loop/types.py:678–698`.

**Observation.** §2.2 (G0 constitution, `design-s2-roles-and-guard.md`)
requires *"≥2 judge seats with distinct `family` values"*. This module sees
endpoint **names**, and family lives in `endpoints.json` (W1-SEATS), so the
check cannot run here — the docstring acknowledges the deferral. But
`min_judge_families` is a family *count* bound (low=2, high=8) applied to
`len(judges)` (`:693–695`) as if judges-per-seat equalled families-per-seat;
`judges: ["a", "b"]` from one family passes the loader and only fails later.
Deliberate layering, but the field name invites the misreading. No code change
proposed; document that the loader checks seat count as a proxy and G0/W1-SEATS
owns the family check.

---

## Tried, and could not break

Attack probes that failed are evidence; each is quoted from a run.

1. **Plan-identity malleability.** Pin *order* independence, null-pin
   refusal, id stability across two file loads, and non-string pin-key refusal
   — the identity function behaved as the docstring and the interface record
   (§7: *"Pin order does not affect the identity; a declared config value
   does"*) promise. `probe/p04_pins.py`:
   ```
   pin order irrelevant: True
   null pin refused: PIN_INVALID
   two loads one id: True
   int pin key refused: CONFIG_INVALID_VALUE
   ```
   (A pin *rename* changes the id — `pin rename changes id: True` — which is
   correct: the path is part of what is pinned.)

2. **Receipt self-validation seam.** I tried to smuggle a receipt whose
   `step_key` did not recompute from its own bytes, a `spending` flag
   contradicting the kind classification, a `FAILED` receipt without a
   `failure_code`, and a `COMPLETE` one with one. All four are refused before
   the record can exist (`probe/p06_receipt.py`):
   ```
   tampered inputs refused: STEP_KEY_MISMATCH
   spending mismatch refused: STEP_RECEIPT_INVALID
   FAILED w/o failure_code refused: STEP_RECEIPT_INVALID
   COMPLETE with failure_code refused: STEP_RECEIPT_INVALID
   round trip equal dicts: True
   ```
   The receipt's "a record that can disagree with the rule it was written
   under is a record that can lie" claim (`:966–968`) holds on these axes.

3. **Path and identifier escapes.** `run_paths` with `run_id` of `a/b`, `..`,
   `a b`, `a\b`; `step_path` with index −1 and 10000; `cycle()` with 0, 100
   and `True` (bool is refused, `type(value) is not int` does its job);
   occurrences with `a/../b`, `//a`, `~`-prefixed, backslash forms
   (`probe/p08_more.py`, `probe/p09_ids.py`). All refused with the correct
   codes (`RUN_ID_INVALID` / `STEP_RECEIPT_INVALID` / `CYCLE_OUT_OF_RANGE` /
   `CONFIG_INVALID_VALUE`). The run tree cannot be reached from outside
   `experiments/loops/<run_id>` by any of these inputs.

4. **The wave-plan acceptance clause, executed whole** (`probe/p07_acceptance.py`):
   two loads give one plan id; a changed pin changes it; an unknown config key
   is refused with `CONFIG_UNKNOWN_KEY`; no vocabulary contains the token
   `exhaust` (`probe/p05_tables.py` scanned all four tables); and a scan of
   every `blocked:<name>` literal in `src/minireason/loop/*.py` finds none
   outside `BLOCK_CODES`:
   ```
   acceptance 5: blocked: literals beyond BLOCK_CODES members: []
   ```
   Also verified there: canonical digest byte-agreement with
   `provider_openai_compat.digest` (`True`), `STEP_KINDS` is 17 distinct kinds,
   `REPLAYABLE_STEPS ∩ SPENDING_STEPS = ∅`, `block_code("ensemble_split")`
   (underscore) is refused, and the `preregistered_condition:` stop reason
   rejects an empty or `..` id.

5. **Cross-module digest claim.** The module docstring claims byte-identity of
   `canonical_json` with `provider_openai_compat.digest`'s serialisation;
   `probe/p05_tables.py` printed `canonical agrees with
   provider_openai_compat.digest: True` (and `src/deepreason_core/canonical.py`
   uses `sort_keys=True, separators=(",", ":"), ensure_ascii=False` — the same
   recipe on both sides, at `provider_openai_compat.py:145–148`).

---

## Suspected and could not reproduce

- I suspected `_digests`' conditional-expression style
  (`digest if ... else _refuse_digest(...)`) might swallow a non-string digest
  silently in some path; it does not — every path either returns a validated
  lowercase hex string or raises (`probe/p04_pins.py` exercised the null and
  mis-typed cases).
- I suspected `from_dict` might accept a receipt whose `schema` is absent but
  whose other fields lie; it defaults `schema` to `STEP_SCHEMA` and the
  `__post_init__` re-key check catches all lies in the five hashed fields
  (`probe/p06_receipt.py`).
- The interface record's O1 (`graph_root` vs `RunPaths.graph` disagreement) is
  real and unresolved by the code — both names exist and nothing ties them —
  but it is a *recorded* open question with an owner (W1-GRAPH), not a finding
  I can pin on this module beyond what the integrator already wrote, so it is
  not repeated as one.
