# Adversarial review — `src/minireason/loop/contracts.py` (W0-CONTRACTS)

Read first: `notes/WAVE0-INTERFACE.md`, then the module, then
`design/design-s2-roles-and-guard.md` §2.3/§2.4 and the `W0-CONTRACTS` entry of
`design/design-s7-wave-plan.md`. Every finding below was produced by running a
probe under `probe/` with `python3 probe/<name>.py` from the sandbox root. Line
numbers are `src/minireason/loop/contracts.py` unless another file is named.

Findings are ordered BLOCKER, SHOULD-FIX, NOTE, and are not ranked within a
group. Two arms of the same claim (`check` "never raises") appear in different
groups because the inputs that reach them are different occasions, not because
one matters more.

---

## BLOCKER

### B1 — `check` raises `RecursionError` on ~2 KB of provider text, and the `not-json` reason the module promises never appears

**Claim.** The published seam `check(...)` is documented "never raises" and
documented to turn a parse failure into the reason `not-json`; roughly 1000
levels of JSON nesting — about 2 KB of text — makes it raise `RecursionError`
out of `json.loads` instead.

**Where.** `_as_object`, lines 658–667 (the guard is the `except` clause on line
662); reached from `check`, lines 793–796.

**What it contradicts.**

`contracts.check` docstring, line 786:

> Never raises. A failure carries the reason (a member of :data:`SCHEMA_REASONS`), the path inside the output and a message.

Module docstring, deviation 3, lines 69–71:

> **``raw`` may arrive as JSON text.** A provider hands back bytes. Passing ``str``/``bytes`` is accepted and parsed; a parse failure is the reason ``not-json`` rather than a ``json`` exception escaping the contract layer.

`notes/WAVE0-INTERFACE.md` §3:

> `check(role: str, raw: Any, *, register: str | None = None) -> Validation     # never raises`

**Probe.** `python3 probe/p02_not_json_depth.py`

```
str  depth=    1 (     2 chars): Validation(ok=False, reason='not-an-object')
str  depth=  100 (   200 chars): Validation(ok=False, reason='not-an-object')
str  depth=  500 (  1000 chars): Validation(ok=False, reason='not-an-object')
str  depth=  900 (  1800 chars): Validation(ok=False, reason='not-an-object')
str  depth=  990 (  1980 chars): Validation(ok=False, reason='not-an-object')
str  depth=  995 (  1990 chars): RAISED RecursionError
str  depth= 1000 (  2000 chars): RAISED RecursionError
str  depth= 5000 ( 10000 chars): RAISED RecursionError
bytes depth=  900 ( 16201 bytes): Validation(ok=False, reason='missing-field')
bytes depth=  990 ( 17821 bytes): Validation(ok=False, reason='missing-field')
bytes depth= 1000 ( 18001 bytes): RAISED RecursionError
bytes depth= 5000 ( 90001 bytes): RAISED RecursionError
recursionlimit: 1000
```

and `python3 probe/p01_check_never_raises.py`, line 7 of its output:

```
check('critic', '[' * 200000 + ']' * 200000)  (200k-deep JSON text): RAISED RecursionError: maximum recursion depth exceeded while decoding a JSON array from a unicode string
```

**Why it is a blocker and not a curiosity.** This is the one input shape the
module says it exists to absorb: bytes off a provider. G1 says a schema-invalid
output is a block with a named reason, and W2-ROLES turns an invalid output into
`unresolved` at `schema_repair_budget = 0`. A `RecursionError` escaping
`contracts` is neither: it is not a `LoopError`, so `except LoopError` — the
package's own convention (`notes/WAVE0-INTERFACE.md` §7: "Every wave-0 exception
is a `types.LoopError`") — does not catch it, and the cell gets no block code,
no reason and no record. The escape is also not deterministic in the way the
rest of the module is: the threshold moved between 995 and 1000 levels purely
with how deep the caller's own stack already was, so the same provider bytes can
block on one call path and crash the step on another.

**Repair.** Bound the parse rather than the exception type. Either catch
`RecursionError` beside `ValueError` in `_as_object` and report `not-json`, or —
better, because it does not depend on the interpreter's stack — refuse text
whose nesting exceeds a declared bound before parsing, with the same reason.
Either way the bound is a declared **resource boundary** on the parse, not a
statement about the output, and the record should say which one was reached.

**Test that would hold it.**

```python
def test_deeply_nested_provider_text_is_not_json_and_never_escapes(self):
    for depth in (990, 1000, 5000, 50000):
        with self.subTest(depth=depth):
            raw = "[" * depth + "]" * depth
            out = contracts.check("critic", raw)          # must not raise
            self.assertFalse(out.ok)
            self.assertIn(out.reason, contracts.SCHEMA_REASONS)
            with self.assertRaises(contracts.SchemaInvalid):
                contracts.validate("critic", raw)
```

---

### B2 — `assert_no_aggregate_fields` passes an open object, which is the case its own docstring names

**Claim.** The guard's docstring says a role schema may hold "no open object
through which one could arrive"; `{"type": "object"}` passes it, and so do eight
other schemas that each admit a numeric or a scoring field.

**Where.** Lines 605–637. The closedness test on lines 619–624 only runs when a
`properties` key is present, and the descent on lines 632–637 never enters
`additionalProperties`, `patternProperties`, `propertyNames`, `$defs`/`$ref`,
`if`/`then`/`else` or `dependentSchemas`.

**What it contradicts.** `assert_no_aggregate_fields` docstring, lines 606–611:

> Raise :class:`ContractError` if a schema could express an aggregate.
> A role output may name no quantity and hold none: no property name in :data:`FORBIDDEN_KEYS` or :data:`AGGREGATE_KEYS`, no ``number`` or ``integer`` type, and no open object through which one could arrive.

and the `W0-CONTRACTS` acceptance clause in `design/design-s7-wave-plan.md`:

> no ordering is defined on the vocabulary and **no aggregate field is expressible**

**Probe.** `python3 probe/p03_aggregate_guard.py`

```
- bare open object
    guard: PASSED the guard
    instance {"total": 3} against that schema: no errors
- open object, no `properties` key, numeric additionalProperties
    guard: PASSED the guard
    instance {"mean": 0.5} against that schema: no errors
- closed at the top, open object nested under a declared property
    guard: PASSED the guard
    instance {"case": {"score": 9}} against that schema: no errors
- patternProperties carrying a number
    guard: PASSED the guard
    instance {"xtally": 4} against that schema: no errors
- propertyNames only
    guard: PASSED the guard
    instance {} against that schema: no errors
- numeric hidden behind $defs/$ref
    guard: PASSED the guard
    instance {"case": 7} against that schema: no errors
- numeric hidden in then/else
    guard: PASSED the guard
    instance {"case": 12} against that schema: no errors
- integer enumerated without a `type`
    guard: PASSED the guard
    instance {"case": 2} against that schema: no errors
- dependentSchemas carrying a number
    guard: PASSED the guard
    instance {"mark": "same"} against that schema: no errors
- a property literally named `count` (the control: this must be refused)
    guard: REFUSED: count: aggregate field name
    instance {"count": "x"} against that schema: no errors
- a top-level `number` (the control: this must be refused)
    guard: REFUSED: <root>: numeric field in a role schema
    instance 3 against that schema: no errors
```

The third case is the sharpest: a schema that is closed at the top level, with
one declared property whose sub-schema is a bare `{"type": "object"}`, passes the
guard and then validates `{"case": {"score": 9}}` without an error — a scoring
key arriving through a schema the guard has just cleared.

**Scope, stated honestly.** The five schemas wave 0 actually ships are clean:
`probe/p13_no_ordering_no_number.py` walks all five and finds no `number`, no
`integer` and no banned property name, and the import-time self-check on lines
836–839 passes. So nothing in wave 0 is presently mis-cleared. The defect is in
the published callable, which `notes/WAVE0-INTERFACE.md` §3 lists as part of this
module's surface and which later waves that add a schema will reach for.

**Repair.** Make closedness a property of every object schema rather than of
object schemas that happen to declare `properties`: if `type` includes `object`
(or the node has any object-shaped keyword), require `additionalProperties is
False`, and descend `additionalProperties`, `patternProperties`, `propertyNames`,
`$defs`, `if`/`then`/`else` and `dependentSchemas` as well. Refuse `$ref`
outright rather than following it — a role schema has no need of one, and a
guard that follows references has to decide what to do about cycles. Refuse an
`enum` or `const` whose members are numbers, since that is a numeric field
without a numeric `type`.

**Test that would hold it.**

```python
OPEN_OR_NUMERIC = [
    {"type": "object"},
    {"type": "object", "additionalProperties": {"type": "number"}},
    {"type": "object", "additionalProperties": False,
     "properties": {"case": {"type": "object"}}},
    {"type": "object", "additionalProperties": False, "properties": {},
     "patternProperties": {"^x": {"type": "number"}}},
    {"type": "object", "additionalProperties": False,
     "properties": {"case": {"enum": [0, 1, 2]}}},
]

def test_no_open_or_numeric_schema_is_cleared(self):
    for schema in OPEN_OR_NUMERIC:
        with self.subTest(schema=schema):
            with self.assertRaises(contracts.ContractError):
                contracts.assert_no_aggregate_fields(schema)

def test_the_five_shipped_schemas_still_pass(self):
    for role in contracts.SCHEMAS:
        contracts.assert_no_aggregate_fields(contracts.SCHEMAS[role])
```

---

## SHOULD-FIX

### S1 — an unhashable `role` or `register` raises `TypeError` out of every entry point

**Claim.** `check`, `validate`, `schema_for`, `difference_kinds_for` and the
`VALIDATORS` mapping all test membership before testing type, so a `list` or a
`dict` in either position raises `TypeError: unhashable type` instead of
returning or raising the module's own refusal.

**Where.** Line 791 (`if role not in SCHEMAS`), line 547 (`schema_for`), line 554
(`difference_kinds_for`), lines 731 and 748 (`_marker_failure`'s two
`register not in DIFFERENCE_KINDS` tests), line 829 (the `VALIDATORS` lambda
forwards into the same path).

**What it contradicts.** Same two sentences as B1 — `check` docstring line 786
("Never raises.") and the `# never raises` annotation in
`notes/WAVE0-INTERFACE.md` §3 — plus the `unknown-role` / `unknown-register`
members of `SCHEMA_REASONS` (lines 289–290), which exist precisely to be the
answer here.

**Probe.** `python3 probe/p01_check_never_raises.py`

```
check(role=['critic'], raw={}): RAISED TypeError: unhashable type: 'list'
check(role={'a':1}, raw={}): RAISED TypeError: unhashable type: 'dict'
check(role=None, raw={}): returned Validation(ok=False, reason='unknown-role')
check('marker', good, register=['T']): RAISED TypeError: unhashable type: 'list'
check('marker', mark=same, register={'T':1}): RAISED TypeError: unhashable type: 'dict'
check('critic', good, register=['T'])  (register ignored for critic): returned Validation(ok=True, reason=None)
check('critic', '[' * 200000 + ']' * 200000)  (200k-deep JSON text): RAISED RecursionError: maximum recursion depth exceeded while decoding a JSON array from a unicode string
VALIDATORS['marker'](good, register=['T']): RAISED TypeError: unhashable type: 'list'
schema_for(['critic']): RAISED TypeError: unhashable type: 'list'
difference_kinds_for(['T']): RAISED TypeError: unhashable type: 'list'
validate(['critic'], {}): RAISED TypeError: unhashable type: 'list'
python: 3.11.15 recursionlimit: 1000
```

`role=None` is handled correctly (`unknown-role`), which shows the intent: the
membership test is meant to be the type test too, and it is not one for
unhashable values.

**Repair.** Test the type first — `if not isinstance(role, str) or role not in
SCHEMAS` — in all five places. `unknown-role` and `unknown-register` already
exist for the outcome.

**Test that would hold it.**

```python
def test_a_non_string_role_or_register_is_a_named_refusal(self):
    for bad in ([], {}, 3, None, object()):
        with self.subTest(bad=bad):
            self.assertEqual(contracts.check(bad, {}).reason, "unknown-role")
            with self.assertRaises(contracts.SchemaInvalid):
                contracts.schema_for(bad)
            with self.assertRaises(contracts.SchemaInvalid):
                contracts.difference_kinds_for(bad)
            self.assertEqual(
                contracts.check("marker", MARKER_DIFFERS, register=bad).reason,
                "unknown-register")
```

---

### S2 — the pre-registered guard content is reachable and editable through the module's own published names, and the pinned digest does not move

**Claim.** `contracts.CRITIC_SCHEMA` (and the other four) is a live mutable dict
that `_VALIDATORS` validates against, and `contracts.DIFFERENCE_KINDS` is a
mutable `dict`. Appending to the critic's `relation` enum in-process makes
`check` admit a relation outside the six published values — G4's closed
vocabulary — while `standard.STANDARD_BODY_SHA256`, the digest a plan pins, is
unchanged.

**Where.** The names are imported at lines 143–165 and re-exported at lines
168–214; `_VALIDATORS` binds the live objects at lines 644–646. The objects
themselves are defined in `src/minireason/loop/standard.py` at lines 736–738
(`DIFFERENCE_KINDS`, a plain `dict`) and 787–867 (the five schema `dict`s, whose
`enum` values are plain `list`s). `schema_for` (lines 545–549) is the only path
that hands out a copy.

**What it contradicts.** Module docstring, lines 44–47 and 49–53:

> The names on both sides are the *same objects*: there is nothing left to drift.

> The schemas moved for one reason: a plan pins the standard body by sha256, and until §2.3 was inside that body, editing a schema or a word limit changed **no digest at all** - so §5's "changing any threshold after first look mints a new ``loop_plan_id``" did not reach the guard content this module holds.

**Probe.** `python3 probe/p06_schema_mutability.py`

```
SCHEMAS is a MappingProxyType: mappingproxy
SCHEMAS itself refuses assignment: 'mappingproxy' object does not support item assignment
CRITIC_SCHEMA['properties']['relation']['enum'] is a list -> ['re-deploys', 'qualifies', 'rejects-with-reason', 'repairs', 'retains', 'none']
before: check('critic', relation='outperforms') -> not-in-enum
after enum.append('outperforms'): check(...) -> ok= True  value.relation= outperforms
standard.STANDARD_BODY_SHA256 unchanged: True b4dc7f6a62543079...
standard.ROLE_SCHEMAS_SHA256 unchanged: False
restored: check('critic', relation='outperforms') -> not-in-enum

the same question for the per-register token set:
  type(contracts.DIFFERENCE_KINDS) = dict
  difference_kinds_for('Q') -> SchemaInvalid(unknown-register)
  after DIFFERENCE_KINDS['Q'] = ('invented_kind',): ('invented_kind',)
  check('marker', differs/grounds_source, register='Q') -> difference-kind-unknown
  restored; registers now: ['D', 'E', 'G', 'T']
  WORD_LIMITS type: mappingproxy   FORBIDDEN_KEYS type: frozenset   AGGREGATE_KEYS type: frozenset
```

The probe mutates only in-process objects and restores them; no file was
touched.

`ROLE_SCHEMAS_SHA256 unchanged: False` is the line that matters: recomputing the
digest **would** catch the change, but nothing recomputes it, and
`STANDARD_BODY_SHA256` — the value a plan actually pins — was frozen at import
and reads the same either way. So the sentence the module gives as the reason
the schemas moved is true of a source edit and not true of a run-time one.

**Repair.** Freeze the guard content the way the module already freezes
`WORD_LIMITS`, `FORBIDDEN_KEYS` and `AGGREGATE_KEYS`: build the schemas into a
deeply immutable form (nested `MappingProxyType` and tuples) at import, keep
`DIFFERENCE_KINDS` in a `MappingProxyType`, and have `schema_for` be the only
mutable view. `Draft202012Validator` accepts mappings, so `_VALIDATORS` is
unaffected.

**Test that would hold it.**

```python
def test_the_pinned_guard_content_is_not_writable(self):
    with self.assertRaises(TypeError):
        contracts.CRITIC_SCHEMA["properties"]["relation"]["enum"].append("x")
    with self.assertRaises(TypeError):
        contracts.DIFFERENCE_KINDS["Q"] = ("invented",)
    self.assertEqual(standard.ROLE_SCHEMAS_SHA256,
                     standard._role_contracts_section()["schemas_sha256"])
```

---

### S3 — `nominated_relation` does not survive `.as_dict()`, which the same docstring calls the record

**Claim.** D6 normalisation keeps the nominated token on the object and says
"nothing is lost"; `.as_dict()` — which the next sentence calls what is
recorded — does not emit it, so a record written from `as_dict` and re-read
through `validate` has lost it.

**Where.** `CriticOutput`, lines 403–451: the claim at lines 415–417, the
normalisation at lines 429–432, the emitter at lines 444–451.

**What it contradicts.** `CriticOutput` docstring, lines 414–418:

> So the output is **normalised, not refused**: ``.relation`` becomes :data:`NONE_RELATION`, the nominated token is kept on :attr:`nominated_relation` so nothing is lost, and the ``outside_vocabulary`` text is carried through unaltered. ``.as_dict()`` emits the normalised relation, so what is recorded is what a renderer reads.

**Probe.** `python3 probe/p08_d6_normalisation.py`

```
seat sent relation      : qualifies
out.relation            : none
out.nominated_relation  : qualifies
out.is_outside_vocabulary: True
out.claims_relation     : False
UNRESOLVED token        : unresolved
NONE_RELATION token     : none
out.relation == UNRESOLVED: False

as_dict() (what is recorded): {"case": "the case", "outside_vocabulary": "reads as a partial concession with a repair", "passage_quote": "the quoted passage", "relation": "none", "role_bindings": {"bearing": "b", "defect": "d", "grounds": "g", "target": "t"}}
'nominated_relation' in the record: False
re-validated from the record -> relation= none  nominated_relation= ''
round trip preserves the nomination: False

a plain `none` answer: relation= none  is_outside_vocabulary= False  claims_relation= False
the two cases are distinguishable in the record only by `outside_vocabulary` being non-empty: True
```

D6 exists to preserve what the seat wrote. The `outside_vocabulary` text is
preserved; the token the seat nominated is preserved in memory and dropped from
the record. Whether that matters is a design question — but the docstring
answers it with "nothing is lost", and on the record something is.

**Repair.** Either emit the nomination in `as_dict()` under a name that is not a
claim (the schema is closed, so a record carrying an extra key would no longer
round-trip through `validate` — which argues for a separate record shape rather
than an extra key), or narrow the sentence to say what is true: the nominated
token is kept on the object and is deliberately not recorded, and here is where
a caller that wants it should read it.

**Test that would hold it** (either direction — this is the round-trip form):

```python
def test_the_nomination_survives_the_record_or_is_documented_as_dropped(self):
    out = contracts.validate("critic", NOMINATED_WITH_OUTSIDE_VOCABULARY)
    self.assertEqual(out.nominated_relation, "qualifies")
    back = contracts.validate("critic", json.dumps(out.as_dict()))
    self.assertEqual(back.nominated_relation, out.nominated_relation)
```

---

### S4 — the module docstring says G4 forces `unresolved`; the code forces `none`, which the same module defines as not `unresolved`

**Claim.** Two sentences in this file cannot both be true of the same code path.

**Where.** The claim at lines 22–23; the definition that contradicts it at lines
250–253; the code at lines 429–432.

**What it contradicts.** Module docstring, lines 22–23:

> **G4** (closed vocabulary; a non-empty ``outside_vocabulary`` forces ``unresolved`` and the text is preserved)

`NONE_RELATION`, lines 250–253:

> The critic's own "no relation is established here" answer. It is *not* a reading of ``unresolved``: the cell was read and nothing was found, which ends the row at one call (§2.3) and leaves the cell where it started.

and `design/design-s2-roles-and-guard.md` §2.3, which gives the two outcomes
different reasons:

> `relation: "none"` ends the row at one call: no trial, cell stays unresolved.
> A non-empty `outside_vocabulary` forces `unresolved` with that reason and preserves the text.

**Probe.** Same run as S3. The two lines that carry it:

```
out.relation            : none
out.relation == UNRESOLVED: False
```

**What I am not claiming.** The code's choice looks forced rather than careless:
`unresolved` is not a member of `CRITIC_RELATIONS`
(`probe/p00_smoke.py`: `CRITIC_RELATIONS: ('re-deploys', 'qualifies',
'rejects-with-reason', 'repairs', 'retains', 'none')`), so writing `unresolved`
into `.relation` would put the record outside the critic's own closed enum and
break the round-trip. `.is_outside_vocabulary` and `.claims_relation` both give
the right answer, and `outside_vocabulary` being non-empty is what separates the
two cases in the record. So this is a documentation defect, not an unsound
seam — but it is one a later wave will read as licence to treat the two §2.3
outcomes as one.

**Repair.** Reword lines 22–23 to say what the code does: a non-empty
`outside_vocabulary` normalises `.relation` to `NONE_RELATION`, sets
`.is_outside_vocabulary`, and leaves the *cell* unresolved with reason
`outside-vocabulary` — the cell state being W2/W3's to write, not this
module's.

**Test that would hold it** (pins the behaviour so the prose has something to
match):

```python
def test_outside_vocabulary_normalises_to_none_and_never_to_unresolved(self):
    out = contracts.validate("critic", NOMINATED_WITH_OUTSIDE_VOCABULARY)
    self.assertEqual(out.relation, contracts.NONE_RELATION)
    self.assertNotEqual(out.relation, contracts.UNRESOLVED)
    self.assertTrue(out.is_outside_vocabulary)
    self.assertFalse(out.claims_relation)
    self.assertNotIn(contracts.UNRESOLVED, contracts.CRITIC_RELATIONS)
```

---

### S5 — `"differs"` is retyped as a literal at the two program sites, while the enum it must agree with is read from a shipped data file

**Claim.** The module says no vocabulary is retyped here. `"differs"` — a member
of `MARKS` — is written as a literal twice, and those two sites are the only
things that make a `differs` mark owe a `difference_kind` and two quotes.

**Where.** Line 493 (`MarkerOutput.claims_difference`) and line 724
(`_marker_failure`).

**What it contradicts.** Module docstring, lines 11–14 and 44–46:

> It also carries the forbidden-key guard (G12) and re-exports, under the spellings the wave plan published for this module, the closed vocabularies W0-STANDARD owns - including the reading vocabulary and the instrument's banner, which no module of this package retypes.

> **And it owns no shared vocabulary** [...] The names on both sides are the *same objects*: there is nothing left to drift.

**Probe.** `python3 probe/p05_retyped_tokens.py` — scans the source with
docstrings and comments stripped, for every member of `MARKS`,
`CRITIC_RELATIONS`, `READING_VOCABULARY`, `ALL_DIFFERENCE_KINDS` and `REGISTERS`
as a quoted literal:

```
code lines (docstrings and comments stripped) carrying a vocabulary token as a quoted literal:
  line 493: return self.mark == "differs"
      -> 'differs' is a member of MARKS
  line 724: if body["mark"] == "differs":
      -> 'differs' is a member of MARKS
total code-line hits: 2
```

and `python3 probe/p04_ownership_claims.py`, which shows where the enum the
literal must agree with actually comes from:

```
MARKS: ('differs', 'same', 'unresolved')
MARKS comes from the shipped data file, not a literal:
  plan_8a_mirror.json['marks'] == ['differs', 'same', 'unresolved']   tuple(...) == standard.MARKS: True
```

**Why it matters.** `MARKER_SCHEMA`'s `mark` enum is `list(MARKS)`, which is
`tuple(PLAN_8A_MIRROR["marks"])` — it tracks `src/minireason/loop/data/plan_8a_mirror.json`.
The two program sites do not. Re-spelling the mark in the mirror (a successor
standard, which the design explicitly allows as a new `loop_plan_id`) would move
the schema enum and leave `_marker_failure` matching a token no output can carry
any more: every mark would take the `mark != "differs"` branch, `difference_kind`
would become forbidden rather than required, and the D4/G9 kind-grain check
would stop firing in silence rather than failing.

**Repair.** Name the token once. `standard` already derives `MARKS` from the
mirror; give it a `DIFFERS_MARK` (or `MARKS[0]` behind a name) and import it,
exactly as `UNRESOLVED` and `NONE_RELATION` are imported at lines 247 and 253.

**Test that would hold it.**

```python
def test_contracts_retypes_no_vocabulary_token(self):
    source = (SRC / "minireason" / "loop" / "contracts.py").read_text("utf-8")
    code = strip_docstrings_and_comments(source)
    vocabulary = set(standard.MARKS) | set(standard.CRITIC_RELATIONS) \
        | set(standard.READING_VOCABULARY) | set(standard.ALL_DIFFERENCE_KINDS)
    for token in vocabulary:
        self.assertNotRegex(code, rf"""['"]{re.escape(token)}['"]""")
```

---

## NOTE

### N1 — `AGGREGATE_KEYS` is disjoint from `FORBIDDEN_KEYS`, not wider than it

**Where.** Lines 271–281 (the docstring at 271–275); repeated in
`notes/WAVE0-INTERFACE.md` §3 (`AGGREGATE_KEYS: frozenset[str]  # schema-name
ban, wider than FORBIDDEN_KEYS`).

**Docstring, line 271:**

> Names an *output schema* may not use. Wider than :data:`FORBIDDEN_KEYS` and deliberately not part of :func:`assert_no_scoring_keys`

**Probe.** `python3 probe/p04_ownership_claims.py`

```
AGGREGATE_KEYS >= FORBIDDEN_KEYS (i.e. 'wider'): False
AGGREGATE_KEYS & FORBIDDEN_KEYS: []
len(AGGREGATE_KEYS)= 28  len(FORBIDDEN_KEYS)= 25
in FORBIDDEN_KEYS but NOT in AGGREGATE_KEYS: ['best', 'better', 'creativity', 'grade', 'grades', 'merit', 'novelty', 'percentile', 'points', 'quality', 'rank', 'ranking', 'ranks', 'rating', 'ratings', 'score', 'scores', 'scoring', 'verdict', 'weight', 'weights', 'win', 'winner', 'worse', 'worst']
```

The *ban* the guard applies is wider, because line 627 tests
`lowered in FORBIDDEN_KEYS or lowered in AGGREGATE_KEYS`. The *set* is not. A
caller who reads the docstring or the interface line and imports `AGGREGATE_KEYS`
alone as "the wider one" gets a set in which `score`, `rank` and `verdict` are
absent.

**Repair.** Either say "applied alongside `FORBIDDEN_KEYS`; together they are the
schema-name ban" in both places, or define `SCHEMA_NAME_BAN = FORBIDDEN_KEYS |
AGGREGATE_KEYS` and publish that as the thing a caller should import.

**Test:** `self.assertTrue(contracts.AGGREGATE_KEYS.isdisjoint(contracts.FORBIDDEN_KEYS))`
plus an assertion that whatever name the docstring calls "wider" really is a
superset.

---

### N2 — `assert_no_scoring_keys` passes five container shapes in silence, including this module's own record objects and a `memoryview` of a rendered file

**Where.** Lines 565–589 (the `str`/`bytes`/`bytearray` refusal at 582) and
592–602 (the descent; `list`/`tuple` only, at 600).

**Docstring, lines 566–580** — the reason the `str` refusal exists:

> Handing the whole guard a ``str`` or ``bytes`` is a different matter and is refused with :class:`ContractError`. [...] a rendered file passed here used to answer ``None`` in silence - so a ``READING_TABLE.md`` with a ``score`` column satisfied §5's protected obligation *p4* without being looked at.

**Probe.** `python3 probe/p09_g12_coverage.py`

```
{'score': 1}                       (the control)     REFUSED at ('score',)
[{'score': 1}]                     (the control)     REFUSED at ('0', 'score')
({'score': 1},)                    (the control)     REFUSED at ('0', 'score')
{'a': {'b': [{'score': 1}]}}       (the control)     REFUSED at ('a', 'b', '0', 'score')
a frozen dataclass with a `score` field              silent pass
a list holding that dataclass                        silent pass
SimpleNamespace(score=1)                             silent pass
collections.deque([{'score': 1}])                    silent pass
a set of one frozenset-of-items                      silent pass
a generator over [{'score': 1}]                      silent pass
dict_values of {'k': {'score': 1}}                   silent pass
memoryview(b'| score |')                             silent pass
'| score |' (a rendered file)                        ContractError: <root>: a str is a rendered file, not a key structure; scan 
b'| score |' (rendered bytes)                        ContractError: <root>: a bytes is a rendered file, not a key structure; sca
...
what the module's own published record objects are:
  type(validate('critic', ...)) = CriticOutput - a dataclass: True
  that CriticOutput handed straight to the guard     silent pass
```

The docstring is honest about the descent covering mappings, lists and tuples,
so this is not a contradiction — it is a gap between the documented descent and
the acceptance clause "a scoring key nested anywhere raises
SCORING_KEY_FORBIDDEN". Two cases are worth naming. `memoryview(b"| score |")`
is the same rendered bytes the guard refuses as `bytes`, one type away, and it
answers `None` in exactly the silence lines 574–578 set out to end. And the
module's own published outputs are frozen dataclasses, so a caller who reaches
for the guard before calling `.as_dict()` gets a pass that means nothing.

**Repair.** Refuse what the guard does not understand rather than passing it: at
the leaf, accept `Mapping`, `list`, `tuple`, `str`, `int`, `float`, `bool`, and
`None` (the JSON shapes), and raise `ContractError` for anything else, naming the
type — including `memoryview` and any object with a `__dataclass_fields__`, for
which the message can say "call `.as_dict()` first".

**Test:** a parametrised case asserting that each of the shapes above either
refuses with `ScoringKeyForbidden` or refuses with `ContractError`, and that none
returns `None`.

---

### N3 — `_schema_failure` sorts stringified path parts, so array index 10 is reported before index 2

**Where.** Lines 670–691; the sort key at 671–679.

**Docstring, line 670:**

> The first schema error, chosen deterministically (path, validator, text).

**Probe.** `python3 probe/p12_path_order_and_edges.py`

```
(a) two type errors, at index 2 and index 10
    reported path: ('paraphrases', '10')  reason: wrong-type
    sorted as strings: sorted(['2','10']) == ['10', '2']
```

Determinism — the property the docstring claims — holds. "First" does not mean
first by position once an array has more than nine items. A variator's
`paraphrases` is the only array in the five schemas and `TRIAL_PARAPHRASE_N` is
2, so nothing in wave 0 reaches it; a later wave with a longer array would get a
path that points at the wrong element.

**Repair.** Sort on `tuple((0, part) if isinstance(part, int) else (1, part) for
part in err.absolute_path)` so integer indices order numerically and stay
separated from string keys.

---

### N4 — `SchemaInvalid` breaks the `str(exc) == f"{code}: {detail}"` relation every other wave-0 exception keeps

**Where.** Lines 355–367; the reassignment at line 367.

`types.LoopError.__init__` builds the exception argument once, as
`f"{code}: {detail}" if detail else code`. `SchemaInvalid` passes a composed
detail to `super().__init__` on line 366 and then rebinds `self.detail` to the
bare message on line 367.

**Probe.** `python3 probe/p10_exception_shape.py`

```
SchemaInvalid:
  str(exc)                 = "SCHEMA_INVALID: defender: missing-field: concedes: 'concedes' is a required property"
  exc.code                 = 'SCHEMA_INVALID'
  exc.detail               = "'concedes' is a required property"
  exc.role/.reason/.path   = defender missing-field ('concedes',)
  LoopError invariant str(exc) == f'{code}: {detail}': False
  the same invariant on a plain LoopError:
     True
```

Everything the interface promises about this exception is true — `.code`,
`.reason`, `.path`, `.detail`, and `str(exc)` naming all three. The note is that
a receipt writer that reconstructs a line from `.code` and `.detail` and a log
line that used `str(exc)` will not match, and the mismatch is invisible unless
you read line 367.

**Repair.** Either keep the composed string in `.detail` and put the bare message
on a second attribute, or record in the docstring that `.detail` is deliberately
the bare message and `str(exc)` the composed one.

---

### N5 — a bogus `register` is accepted in silence on the four non-marker roles

**Where.** Lines 783–811; the dispatch at 805–808 passes `register` only into
`_marker_failure`.

**Probe.** `python3 probe/p12_path_order_and_edges.py`

```
(b) check('critic', ..., register='NOT-A-REGISTER') -> ok=True, reason=None
(b) check('judge', ..., register='NOT-A-REGISTER') -> ok=True, reason=None
(b) check('defender', ..., register='NOT-A-REGISTER') -> ok=True, reason=None
(b) check('variator', ..., register='NOT-A-REGISTER') -> ok=True, reason=None
    check('marker', ..., register='NOT-A-REGISTER') -> unknown-register
```

O11's recommendation is that W2-MARKPREP "always pass `register=`". A caller that
follows that advice uniformly and mistypes a register gets a refusal only on
marker calls. `unknown-register` already exists; validating the keyword
whenever it is supplied costs one line and closes the difference between "this
caller knows the register" and "this caller thinks it does".

---

### N6 — duplicate keys in provider text collapse silently, last one wins

**Where.** Line 661 (`raw = json.loads(raw)`).

**Probe.** `python3 probe/p14_parse_seam.py`

```
duplicate `relation` key in the provider's text:
  raw text says       : "relation": "retains"  ... "relation": "none"
  check -> ok= True  value.relation= none
  json.loads on the same bytes gives: none
```

This is `json.loads`' documented behaviour, not a bug in the module. It is worth
recording because the raw bytes are what gets stored as the blob and the parsed
object is what gets validated and recorded, and the two are not in one-to-one
correspondence for every byte string a seat can emit. If that matters to G1's
"invalid output is a block, never a repair", the refusal belongs here (a
`object_pairs_hook` that refuses a repeated key, reason `unexpected-field`), not
downstream.

---

## Tried, and could not break

Each of these was an attempt to find a defect. Each failed, and the failure is
evidence about the module.

**1. Ownership by identity.** I tried to find one re-exported name in
`contracts` that is a copy rather than W0-STANDARD's object, which would make
the "nothing left to drift" claim false at the seam rather than at the literal.
Sixteen names, all the same object, and `READING_VOCABULARY` is the instrument's
own tuple rather than a rebuild of it. `python3 probe/p04_ownership_claims.py`:

```
READING_VOCABULARY is ROOT_READING_VOCABULARY: True
type(ROOT_READING_VOCABULARY): tuple
READING_BANNER is USE_RELATION_BANNER: True
  contracts.READING_VOCABULARY is standard.READING_VOCABULARY: True
  contracts.CRITIC_RELATIONS is standard.CRITIC_RELATIONS: True
  contracts.MARKS is standard.MARKS: True
  contracts.REGISTERS is standard.REGISTERS: True
  contracts.DIFFERENCE_KINDS is standard.DIFFERENCE_KINDS: True
  contracts.ALL_DIFFERENCE_KINDS is standard.ALL_DIFFERENCE_KINDS: True
  contracts.FORBIDDEN_KEYS is standard.FORBIDDEN_KEYS: True
  contracts.WORD_LIMITS is standard.WORD_LIMITS: True
  contracts.SCHEMAS is standard.SCHEMAS: True
  contracts.ROLE_NAMES is standard.ROLE_NAMES: True
  contracts.ROLE_BINDING_FIELDS is standard.ROLE_BINDING_FIELDS: True
  contracts.CRITIC_SCHEMA is standard.CRITIC_SCHEMA: True
  contracts.DEFENDER_SCHEMA is standard.DEFENDER_SCHEMA: True
  contracts.JUDGE_SCHEMA is standard.JUDGE_SCHEMA: True
  contracts.MARKER_SCHEMA is standard.MARKER_SCHEMA: True
  contracts.VARIATOR_SCHEMA is standard.VARIATOR_SCHEMA: True
```

The acceptance clause "READING_VOCABULARY is imported from
`use_relation_h005.ROOT_READING_VOCABULARY`, not retyped" holds by identity, not
just by equality.

**2. An unreachable or an out-of-table reason.** I tried to find a member of
`SCHEMA_REASONS` no fixture can produce (dead vocabulary) and a reason `check`
can produce that is not in the table (`_JSONSCHEMA_REASONS`' `"wrong-type"`
default was the candidate). Neither exists: one fixture per reason, all eighteen
reached, nothing outside the table. `python3 probe/p07_reason_coverage.py`:

```
unknown-role             check -> 'unknown-role'             validate -> SchemaInvalid(reason='unknown-role', path=())
not-json                 check -> 'not-json'                 validate -> SchemaInvalid(reason='not-json', path=())
not-an-object            check -> 'not-an-object'            validate -> SchemaInvalid(reason='not-an-object', path=())
missing-field            check -> 'missing-field'            validate -> SchemaInvalid(reason='missing-field', path=('concedes',))
unexpected-field         check -> 'unexpected-field'         validate -> SchemaInvalid(reason='unexpected-field', path=('score',))
wrong-type               check -> 'wrong-type'               validate -> SchemaInvalid(reason='wrong-type', path=('concedes',))
not-in-enum              check -> 'not-in-enum'              validate -> SchemaInvalid(reason='not-in-enum', path=('relation',))
empty-field              check -> 'empty-field'              validate -> SchemaInvalid(reason='empty-field', path=('answer',))
too-few-items            check -> 'too-few-items'            validate -> SchemaInvalid(reason='too-few-items', path=('paraphrases',))
not-unique               check -> 'not-unique'               validate -> SchemaInvalid(reason='not-unique', path=('paraphrases',))
word-limit               check -> 'word-limit'               validate -> SchemaInvalid(reason='word-limit', path=('case',))
case-required            check -> 'case-required'            validate -> SchemaInvalid(reason='case-required', path=('case',))
passage-quote-required   check -> 'passage-quote-required'   validate -> SchemaInvalid(reason='passage-quote-required', path=('passage_quote',))
difference-kind-required check -> 'difference-kind-required' validate -> SchemaInvalid(reason='difference-kind-required', path=('difference_kind',))
difference-kind-forbidden check -> 'difference-kind-forbidden' validate -> SchemaInvalid(reason='difference-kind-forbidden', path=('difference_kind',))
difference-kind-unknown  check -> 'difference-kind-unknown'  validate -> SchemaInvalid(reason='difference-kind-unknown', path=('difference_kind',))
quote-required           check -> 'quote-required'           validate -> SchemaInvalid(reason='quote-required', path=('left_quote',))
unknown-register         check -> 'unknown-register'         validate -> SchemaInvalid(reason='unknown-register', path=())

members of SCHEMA_REASONS no fixture above reached: []
reasons produced that are NOT in SCHEMA_REASONS: []
```

**3. Smuggling a quantity into a role output.** I tried ten ways to get a number
or a scoring key past the five shipped schemas, and walked the schemas for a
numeric type or a banned property name. Everything was refused; the schemas
declare only `array`, `boolean`, `null`, `object` and `string`.
`python3 probe/p11_attacks_that_failed.py` and
`python3 probe/p13_no_ordering_no_number.py`:

```
3. every numeric value offered to a shipped schema was refused: True -> ['not-in-enum', 'wrong-type']
6. critic with an extra 'score' key: unexpected-field | with 'verdict': unexpected-field | role_bindings with an extra 'rank': unexpected-field
```

```
(a) every `type` declared anywhere in the five schemas: ['array', 'boolean', 'null', 'object', 'string']
    'number' or 'integer' among them: False
(b) property names: 20 | any in FORBIDDEN_KEYS | AGGREGATE_KEYS: []
    assert_no_aggregate_fields on all five: no refusal
(c) ordering operations applied to a vocabulary name in contracts.py:
    total: 0
```

The last line is the "no ordering is defined on the vocabulary" clause: I
scanned every source line naming a vocabulary for `sorted(`, `.index(`, `max(`,
`min(`, `.sort(`, a comparison operator or `enumerate(`, and found none. (O2's
collision is real and visible here — `verdict` is in `FORBIDDEN_KEYS` and is
refused as a critic key — exactly as the interface records it.)

**4. Impurity and state leaking between calls.** I tried to make `check` mutate
its argument, to make two identical calls differ, and to make the deep copy
`schema_for` hands out feed back into validation.
`python3 probe/p11_attacks_that_failed.py`:

```
1. argument unchanged after two checks: True | both ok: True | identical Validation: True
2. after editing schema_for('critic')'s copy, check() still refuses 'outperforms': not-in-enum
   schema_for returns a fresh object each call: True | equal to the live schema: True
```

**5. Non-determinism from key order, and the word-limit boundary.** I tried to
make the reported first error depend on the order the provider wrote its keys,
and to find an off-by-one at the 400-word bound.
`python3 probe/p11_attacks_that_failed.py`:

```
4. same (reason, path) under three key orders: True -> ('unexpected-field', ('extra',))
5. critic case of exactly 400 words: None | 401 words: word-limit | 400 words across newlines: None
7. every name in __all__ is importable: True | missing: []
8. the five §2.3 shapes validate and build: ['CriticOutput', 'DefenderOutput', 'JudgeRuling', 'MarkerOutput', 'VariatorOutput']
9. marker differs/'target_set_membership' with register=None: True | with register='G': difference-kind-unknown
```

Item 9 is O11 reproduced, behaving exactly as the interface records it: the
union fallback admits a T-register token when no register is named, and the same
token is refused when `register="G"` is passed.

**6. The exception shapes the interface publishes.** I tried to find one that
does not hold — in particular `str(ScoringKeyForbidden(...)) ==
"SCORING_KEY_FORBIDDEN"`, which the existing study's `code_of` depends on, and
`FAILURE_CODES` membership for all three codes.
`python3 probe/p10_exception_shape.py`:

```
ScoringKeyForbidden:
  str(exc)      = 'SCORING_KEY_FORBIDDEN'
  exc.code      = 'SCORING_KEY_FORBIDDEN'
  exc.detail    = ''
  exc.path      = ('a', 'rank')
  class attr code: 'SCORING_KEY_FORBIDDEN'
  isinstance LoopError/ValueError: True True
...
SCHEMA_INVALID in types.FAILURE_CODES: True
CONTRACT_VIOLATION in types.FAILURE_CODES: True
SCORING_KEY_FORBIDDEN in types.FAILURE_CODES: True
types.is_failure_code on each: [True, True, True]
blocked:schema is a BLOCK_CODE: True 'blocked:schema'
```

**7. Suspected and could not reproduce.** I suspected `_marker_failure` would
report `difference-kind-forbidden` for a `same` mark carrying a bogus register
and thereby hide the register error permanently; it does report
`difference-kind-forbidden` first, but the register error is reported on line
748 whenever the kind is absent, so no input both carries a bad register and can
never be told so. I also suspected `_schema_failure`'s `unexpected-field` branch
would fail on a boolean sub-schema (`error.schema` not a `Mapping`, so `.get`
would raise); I could not construct a body that reaches it through any of the
five shipped schemas, because none of them contains a boolean sub-schema. Both
are recorded as suspected-and-not-reproduced, not as findings.

---

## What I could not determine

* **Whether `FORBIDDEN_KEYS` still equals the tool's own literal.** The module
  docstring (lines 84–93) says "``tests/loop/test_contracts.py`` parses the
  tool's own literal and asserts the sets are equal, so drift from the tool
  fails a test rather than passing silently." Neither `tools/` nor
  `tools/contrast_triple_study.py` is in this sandbox. The listing, with the
  command beside it:

  ```
  python3 -c "
  import os
  for d in ('tests/loop','tools'):
      print(d, '->', sorted(os.listdir(d)) if os.path.isdir(d) else 'ABSENT')
  "
  tests/loop -> ['__init__.py', '__pycache__']
  tools -> ABSENT
  ```

  Unresolved: I could check that `contracts.FORBIDDEN_KEYS is
  standard.FORBIDDEN_KEYS` and that it holds 25 keys
  (`probe/p04_ownership_claims.py`), but not that it agrees with the tool it
  mirrors.
* **Every "and a test asserts it" claim in the module and in the interface.**
  `tests/loop/` holds only `__init__.py`, as the listing above shows;
  `python3 run_tests.py` reports `Ran 0 tests in 0.000s` / `OK`. So the
  import-graph acyclicity test, the
  `assertIs` ownership tests, the G12 vendored-`verdict` test named in O2 and the
  `FORBIDDEN_KEYS` equality test could not be run or read. I re-derived the
  ownership identities directly (see "Tried, and could not break" item 1) rather
  than trusting the claim, but the tests themselves are outside what I can see.
* **Cross-process determinism under hash randomisation.** The operating note
  forbids setting an environment variable on a command line, so I could not vary
  `PYTHONHASHSEED` across runs. I tested `_schema_failure`'s stability only
  within one process, across three key-insertion orders. The sort key on lines
  671–679 is a total order over strings and looks seed-independent, but I did
  not execute that and so do not claim it.
* **A single universal depth at which B1 fires.** The threshold moves with how
  deep the caller's own stack already is — 995 levels of nesting from a
  one-frame-deep helper, past 1000 from module level in the same interpreter.
  I report the behaviour and a range, not a constant.
* **Whether B2's holes bite any real schema.** The nine schemas in
  `probe/p03_aggregate_guard.py` are mine, written to probe the guard. No schema
  in this sandbox exhibits the hole: all five shipped ones are closed and
  non-numeric. Whether a later wave writes one that does is outside what the
  sandbox can answer.
* **Anything downstream of the contract layer.** `blocked:schema` mapping, G2
  uniqueness, G4's effect on cell state, G9's kind-grain comparison against a
  sealed baseline, and `conforming_transcript` registration all belong to W1–W3
  modules that are not in this sandbox. I read
  `deepreason_core.harness.conforming_transcript` to check the module's
  deviation-4 justification (it does require a non-empty `case`, `answer` and
  `decisive_point`, plus `decisive in exchange` and a `checks` dict) and went no
  further.
* **What I left out.** I did not review `standard.py`, `types.py`, `custody.py`,
  `receipts.py` or `publish.py` in their own right; I read only the parts of
  `standard.py` and `types.py` that `contracts.py` makes claims about. I did not
  attempt to evaluate the rubric prose, the ceiling text, the calibration
  anchors, or `build_standard`'s byte-stability — those are W0-STANDARD's
  acceptance clauses, not W0-CONTRACTS'.
