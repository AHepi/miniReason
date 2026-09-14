# Adversarial review — W0-CONTRACTS (`src/minireason/loop/contracts.py`)

Scope reviewed: the five role schemas as `standard` owns them and `contracts`
re-exports them, the closed vocabularies, and the G12 forbidden-key guard.
Reference texts: `notes/WAVE0-INTERFACE.md` (the integrator's record), design
`§2.3`/`§2.4` (`design/design-s2-roles-and-guard.md`), and W0-CONTRACTS' own
acceptance clause in `design/design-s7-wave-plan.md`.

Method: every finding below is executed by a probe under `probe/`, run with
`python3 probe/<name>.py` in this sandbox (`src` importable, jsonschema
4.25.1). Quoted prose is verbatim from the module under review, its owner
module, or the design.

A note on file boundaries: two findings live physically in
`src/minireason/loop/standard.py`. They are reported here because they are the
§2.3 contracts W0-CONTRACTS publishes and whose docstrings in `contracts.py`
make the claim being reviewed; the integrator's record assigns the schemas to
`standard` (deviation 6) and contracts re-exports them as "the same objects".

---

## BLOCKER

None. The two published seams I attacked most directly — the marker schema's
closed `difference_kind` enum, and the G12 guard over key structures with the
`SCORING_KEY_FORBIDDEN` code — both fire as documented. The pre-registered
guards contracts carries (G1 closed schemas, G4/D6 the outside-vocabulary
normalisation, G9/D4 the per-register kind set, G12 the forbidden-key guard)
all trigger on their intended inputs; see the failed attacks below for the
ones I could not break.

---

## SHOULD-FIX

### S1. `check`'s documented contract "Never raises" is breakable: a deeply nested byte string escapes the contract layer as `RecursionError`

**Defect location.** `src/minireason/loop/contracts.py:783-790` (the `check`
docstring states the contract, `Never raises`) and `:658-667` (`_as_object`'s
`json.loads` call site, whose `except (ValueError, UnicodeDecodeError)` does
not cover `RecursionError`).

**Claim contradicted.** The `check` docstring opens with "Validate ``raw`` as
``role``'s output and **return** the outcome. Never raises." Why the contract
must hold is stated in the module docstring's second deviation
(`contracts.py:62-68`): "The design asks for a validator that returns a
structured failure rather than raising (W2-ROLES turns an invalid output into
``unresolved`` at ``schema_repair_budget = 0``, which is a value, not an
exception). :func:`check` never raises". The third deviation
(`contracts.py:69-71`) commits to the framing that a parse failure is "the
reason ``not-json`` rather than a ``json`` exception escaping the contract
layer". A `RecursionError` escaping `_as_object` is exactly an exception
escaping the contract layer: at depth 1000 the input is unparseable, and the
surface is neither a `Validation` nor the declared `not-json` reason.

**Probe.** `python3 probe/never_raises.py` printed, verbatim:

```
malformed-JSON depth     100: returned Validation(ok=False, reason='not-an-object')
malformed-JSON depth    1000: ESCAPED as RecursionError: 'maximum recursion depth exceeded while decoding a JSON array from a un'
malformed-JSON depth   10000: ESCAPED as RecursionError: 'maximum recursion depth exceeded while decoding a JSON array from a un'
malformed-JSON depth  100000: ESCAPED as RecursionError: 'maximum recursion depth exceeded while decoding a JSON array from a un'
bytes depth 100000: ESCAPED as RecursionError
pre-parsed deep dict depth    100: Validation(ok=False, reason='unexpected-field', path0=('nested',))
pre-parsed deep dict depth    500: Validation(ok=False, reason='unexpected-field', path0=('nested',))
pre-parsed deep dict depth   1000: Validation(ok=False, reason='unexpected-field', path0=('nested',))
pre-parsed deep dict depth   5000: Validation(ok=False, reason='unexpected-field', path0=('nested',))
guard depth    100: PASSED silently
guard depth   1000: ESCAPED as RecursionError
guard depth   5000: ESCAPED as RecursionError
```

Depth 1000 suffices; CPython parses JSON recursively. The byte-string case is
the operational one: the module's third deviation says "A provider hands back
bytes", and a 2000-byte response of `[` × 1000 + `]` × 1000 is well inside
any provider's output. The same `RecursionError` reaches
`assert_no_scoring_keys` (`contracts.py:592-602`, `_scan_for_scoring_keys`),
which recurses with no depth guard — that one is the G12 *artifact* guard, not
the role-output contract, so I rank only the `check` escape as a
published-seam violation.

**Repair.** In `_as_object`, catch `RecursionError` alongside `ValueError` and
return the existing `not-json` reason (a parse failure is what it is), or
pre-reject on a cheap nesting bound before `json.loads`. The same catch
belongs in `_scan_for_scoring_keys` (or its public wrapper), which recurses
without a depth guard.

**Test that would hold it.** `test_check_never_raises_on_deep_nesting`:
`check("critic", "[" * 5000 + "]" * 5000)` returns `Validation(ok=False,
reason="not-json")`; `assert_no_scoring_keys` on a 5000-deep nested mapping
either returns or raises a `ContractError`, never a bare `RecursionError`.

### S2. The judge schema admits an empty `reading_note`; the critic/marker analogues contracts enforces non-emptiness for, the judge's is not

**Defect location.** `src/minireason/loop/standard.py:831`
(`"reading_note": _text_schema(),` — no `min_length`), inside
`JUDGE_SCHEMA`. Compare `:817` (`"answer": _text_schema(min_length=1)`) and
`:830` (`"decisive_point": _text_schema(min_length=1)`).

**Claim contradicted.** Design §2.3 fixes the judge's output shape as
`{"sustained": true, "decisive_point": "exact substring of case + \"\\n\" +
answer", "reading_note": "<=120 words"}`, and contracts' fourth deviation
(`contracts.py:72-83`) explains why program checks beyond JSON Schema exist:
"the vendored registration gate would otherwise reject the artifact later,
with less to say about why: ``deepreason_core.harness.conforming_transcript``
requires a non-empty ``case`` and ``answer`` and a non-empty
``decisive_point``, so a critic that claims a relation must supply a case and
a passage to quote, and a marker that claims ``differs`` must supply both
sides' quotes and a ``difference_kind``." The same logic reaches the judge.
On a `sustained: True` ruling with `reading_note: ""`, `check` returns
`ok=True` (probe below). The schema's `required` list gives the key, and the
schema's own `minLength`-to-`empty-field` mapping at `contracts.py:314` exists
precisely because an empty string is an invalid-output shape (`empty-field` is
one of the 18 `SCHEMA_REASONS`). But `reading_note` carries no `minLength` —
no G2 uniqueness floor either — while the two fields `conforming_transcript`
names (`decisive_point`, and the critic's `case`/`answer`) are floored. The
result is asymmetric: a registration without a note records a ruling with no
stated reading, and nothing refuses it.

I checked whether anything downstream makes the empty note unreachable: G2b
(`E.count(d) == 1`, design §2.4) constrains `decisive_point` only, and
`conforming_transcript` (`src/deepreason_core/harness.py:61-79`) requires
`case`, `answer`, `decisive` and a `checks` dict — it never reads
`reading_note`.

**Probe.** `python3 probe/validate_core.py` printed, verbatim:

```
judge: EMPTY reading_note                            ok=True  reason=None                         path=()
judge: empty decisive_point                          ok=False reason='empty-field'                path=('decisive_point',)
```

**Repair.** `"reading_note": _text_schema(min_length=1)` in
`standard.JUDGE_SCHEMA`. This changes `sha256(canonical(SCHEMAS))` and
therefore `STANDARD_BODY_SHA256` (`probe/ownership_body.py` confirms the
digest moves when a schema byte moves), so the repair is deliberately
digest-visible — a successor standard, not a silent edit, which is exactly
what standard's deviation 6 was built to make true.

**Test that would hold it.** `test_judge_reading_note_must_not_be_empty`:
`check("judge", {"sustained": True, "decisive_point": "p",
"reading_note": ""})` is `ok=False` with reason `empty-field` and path
`("reading_note",)`.

---

## NOTE

### N1. The judge's word limit is enforced; its floor is not — the same one-sided gap as S2, at the word-count layer

`contracts.py:694-702` (`_word_limit_failure`) enforces `WORD_LIMITS`
("judge/reading_note 120", per `standard.py:770-777` and WAVE0-INTERFACE §3)
as an upper bound only. §2.3's `"<=120 words"` is genuinely one-sided, so this
is not a deviation from the design's letter; it is recorded because S2's floor
absence means a judge ruling can satisfy every check contracts runs while
carrying no prose at all: `reading_note: ""` is both schema-valid and within
the word bound (0 ≤ 120). `probe/validate_core.py` printed `judge: EMPTY
reading_note ok=True`. If S2 is repaired, this note is discharged with it.
No separate repair.

### N2. `assert_no_scoring_keys`'s first-hit path is insertion-order dependent

**Defect location.** `contracts.py:594-599`: the mapping walk iterates
`value.items()`, so when two scoring keys are present, which one is named on
`ScoringKeyForbidden.path` depends on the caller's dict order, not on any
canonical rule. Contrast `_schema_failure` at `contracts.py:670-691`, whose
docstring (`:671`) says "The first schema error, chosen deterministically
(path, validator, text)" and implements exactly that with an explicit sort.

**Claim this sits against.** Nothing in the module promises a deterministic
first hit for the guard, so this is not a contradiction of a stated claim; it
is an inconsistency of discipline between the module's two "first failure"
selectors, one of which is canonicalised and one of which is not. The
operationally salient part is already safe: JSON objects preserve source order
through `json.loads`, so two emissions of the same bytes raise at the same
path; only a caller passing a dict assembled in another order sees a
different named key.

**Probe.** `python3 probe/guard_g12.py` printed, verbatim:

```
first hit for {'b': {'rank': 1}, 'a': {'rank': 2}} -> ('b', 'rank')
first hit for {'a': {'rank': 2}, 'b': {'rank': 1}} -> ('a', 'rank')
first hit for {'outer': {'z': [{'score': 1}, {'merit': 2}]}} -> ('outer', 'z', '0', 'score')
```

**Possible repair.** Sort each mapping's keys (e.g. `for key in sorted(value,
key=str)`) before descending, so the named path is a pure function of the
value's contents. A test would pin: for both orderings of `{"a": {"rank": 1},
"b": {"score": 2}}`, the raised `.path` is identical.

### N3. The tool-parity claim is unverifiable in this sandbox, and one half of it already overreaches on case

`contracts.py:91-93` claims: "The behaviour of the guard here is identical to
the tool's except that it also descends into tuples, which the tool's version
does not: it refuses strictly more scoring keys and accepts none that the
tool refuses."

`tools/contrast_triple_study.py` is **not in the sandbox** (it is named in
`types.PINNED_SOURCE_PATHS` and in standard's deviation 5, but the file itself
was not copied in), so the "identical except tuples" claim, and the drift
assertion "``tests/loop/test_contracts.py`` parses the tool's own literal and
asserts the sets are equal", are unverifiable here: the referenced test file
does not exist under `tests/loop/` in this snapshot either. I therefore cannot
execute the cross-check; what I can execute is the guard's own case behaviour,
and it already falsifies one half of the sentence. `probe/guard_g12.py`
printed, verbatim:

```
CASE-VARIANT key 'SCORE' (lowercased)                                  -> ScoringKeyForbidden(SCORING_KEY_FORBIDDEN)
```

The lowercasing at `contracts.py:597` (`str(key).lower() in FORBIDDEN_KEYS`)
means the guard refuses mixed-case spellings (`SCORE`, `Score`, `RANK`). If
the tool's guard does `key in FORBIDDEN_KEYS` without lowercasing — the usual
form for such a set-membership guard — then "identical … except tuples" is
false in a second respect (the lowercasing is stricter, i.e. refuses more).
This rests on a file I cannot read, so I record it as **unresolved**: the
claim is pinned against `tests/loop/test_contracts.py`, which is absent here,
and the direction of any second divergence is stricter, not weaker, so G12's
soundness is not at issue — only the sentence's exactness. The repair, if the
tool indeed does not lowercase, is to strike "except that it also descends
into tuples" and name the case-folding too.

### N4. The interface record's count of FORBIDDEN_KEYS ("G12, 24 keys") differs from the observed 25

WAVE0-INTERFACE §0's owner table lists "`FORBIDDEN_KEYS` (G12, 24 keys)";
`probe/identity.py` printed `FORBIDDEN_KEYS count: 25`. The set lives at
`standard.py:168-172` and enumerates 25 members (including `verdict`, the O2
collision key). This is a discrepancy between the integrator's record and the
module, not inside the module, and no schema or guard correctness rides on the
count — it is recorded because the interface file is the review's reference
text and the count is wrong in it by one. Unresolved which side drifted.

---

## Tried, and could not break

Attacks that failed are evidence about the module; these five were run as
probes and held.

**1. Closed vocabularies admit nothing outside — enum, union, and per-register narrowing all hold.** `probe/marker_enum.py` drove every member of
`ALL_DIFFERENCE_KINDS` plus off-set tokens through `check("marker", …)`.
A made-up token is refused at the schema with reason `not-in-enum` exactly as
the docstring at `contracts.py:104-107` promises ("a token outside it is
refused at the schema with reason ``not-in-enum`` before anything is
registered"); the message names the full enum including the `None` sentinel.
The per-register narrowing works: `target_set_membership` (a real T token) is
admitted union-wide, refused on `register="G"` as `difference-kind-unknown`,
and `difference-kind-required` / `difference-kind-forbidden` /
`unknown-register` all fire on their intended branches. Verbatim output:

```
allowed token 'disposition_carrier_field'    ok=True reason=None
...
unknown token, no register   : ok=False reason: 'not-in-enum' path: ('difference_kind',)
T-kind, union check          : ok=True reason: None
T-kind on register G         : ok=False reason: 'difference-kind-unknown'
differs + null kind          : ok=False reason: 'difference-kind-required'
```

`probe/fallback_and_transcript.py` also confirmed the one seam I thought
might leak an unnamed reason — an unmapped jsonschema validator word — maps
to `"wrong-type"`, which **is** a `SCHEMA_REASONS` member, so "every malformed
fixture … naming its reason" holds even off the table: `unmapped validator
word: 'maximum' -> maps to: wrong-type | 'wrong-type' in SCHEMA_REASONS: True`.

**2. G12 refuses scoring keys wherever a key structure can hide them, and refuses a rendered file handed in whole.** `probe/guard_g12.py`: nested in a
dict, in a list, in a **tuple** (the deliberate widening over the tool),
case-variant `SCORE`, and `verdict` (the O2 vendored-warrant collision field)
all raise `ScoringKeyForbidden` whose `str(exc)` is byte-exactly
`SCORING_KEY_FORBIDDEN` (so the existing study's `code_of` reads it
unchanged). A scoring word **in a value** is correctly never scanned ("the
score is not recorded here" passes), and a whole `str`/`bytes` argument — a
rendered `READING_TABLE.md` with a `score` column — is refused with
`ContractError` rather than answered `None` in silence, closing the p4 hole
the deviation names. The `AGGREGATE_KEYS` ban is correctly **not** applied to
artifacts ("artifact key 'count' … PASSED SILENTLY"). The schema audit
(`assert_no_aggregate_fields`) caught a numeric property, an open object, a
numeric under `oneOf`, `items`, `allOf`, `prefixItems`, `contains`, and an
aggregate field name nested in `anyOf`; all five owned schemas pass it at
import. Its one untraversed position, `if/then` (a conditional numeric
property is admissible via `{"if": …, "then": {"properties": {"count":
{"type": "number"}}}}`), is real but theoretical: the audit is an
import-time self-check over this module's five shipped schemas, none of which
uses conditionals, and I could not construct a way for a provider to smuggle
a number through it today.

**3. Purity, non-mutation, and no rebindable surface.** `probe/purity_mut.py`:
`check` mutates its argument on none of the success, schema-failure, or
program-failure paths; word limits fire at exactly 401/121 and hold at
400/120; `True`/`401` in a string field are `wrong-type` at the schema, never
a crash in the word counter; `check` raised on none of `None`, `42`, `3.14`,
invalid bytes, non-JSON text, bare `{"unexpected": 1}`, `Ellipsis`, or a bare
object. `contracts.SCHEMAS` and `contracts.WORD_LIMITS` refuse rebinding
(`TypeError`), and editing the deep copy `schema_for` returns does not open
the live enum — `check("critic", … "relation": "mimics")` still fails
`not-in-enum` afterwards. `probe/identity.py` confirmed all 21 re-exports are
`is`-identical with standard's objects, `READING_VOCABULARY is
use_relation_h005.ROOT_READING_VOCABULARY` and `READING_BANNER is
USE_RELATION_BANNER` are both `True`, the import graph direction is
`types -> standard -> contracts` with no reverse edge, and
`SCHEMA_REASONS` is disjoint from both `FAILURE_CODES` and `BLOCK_CODES`.

**4. The pinning story is load-bearing, not decorative.** `probe/ownership_body.py`: the standard body's `role_contracts.word_limits`
mirrors the live `WORD_LIMITS`; `schemas_sha256` equals
`sha256(canonical(SCHEMAS))` computed over the live schemas
(`ROLE_SCHEMAS_SHA256` agrees); `build_standard()` is byte-stable; editing one
byte of one schema moves the digest. The shipped body itself contains no
`FORBIDDEN_KEYS` member. So the deviation-6 claim — "editing a schema or a
word limit" now changes a pinned digest — is true as executed, which is also
why S2's repair would be digest-visible.

**5. The D6 normalisation does what its docstring says, and does not fake a claim.** `probe/validate_core.py`: a critic naming `relation: "repairs"`
with a non-empty `outside_vocabulary` is normalised, not refused:
`.relation` becomes `NONE_RELATION`, the nominated token is preserved on
`.nominated_relation` (`"repairs"`), the outside text is carried unaltered
(`"mimicry"`), `claims_relation` is `False`, and the frozen record refuses
mutation (`FrozenInstanceError`). `probe/fallback_and_transcript.py` closed
the remaining worry: building the vendored transcript shape from a normalised
output (`case=""`, `decisive_point=""`) fails `conforming_transcript`
(`False`), while the same shape filled (`'c'`/`'a'`/`'c'`) passes (`True`) —
so a normalised critic output cannot back a rubric-derived warrant through
the vendored gate, and G4's "forces unresolved, text preserved" is backed by
the registration seam downstream.

---

## Things suspected and not reproduced

* That `AGGREGATE_KEYS` might leak into artifact validation (the interface
  says it is "NOT applied to artifacts"): executed — `{"count": 3}` passes
  `assert_no_scoring_keys`. Not a defect.
* That an unmapped jsonschema validator would produce a `reason` outside
  `SCHEMA_REASONS`: executed — the fallback is `wrong-type`, a member. Not a
  defect.
* That `schemas_sha256` might be stale or divorced from the live schemas:
  executed — recomputed digest matches. Not a defect.
* Whether the guard's case-folding matches the tool's: **unresolved** —
  `tools/contrast_triple_study.py` is not in this sandbox, and the test that
  would pin it (`tests/loop/test_contracts.py`) is absent from the snapshot.
  Recorded under N3 rather than asserted.
