# Adversarial review — W0-CONTRACTS (`src/minireason/loop/contracts.py`)

Subject: the five role schemas, the closed vocabularies as `standard` owns them,
and the G12 forbidden-key guard. Reviewed against `notes/WAVE0-INTERFACE.md`
(the integrator's record), `design/design-s2-roles-and-guard.md` (§2.3, §2.4 G1/G4/
G9/D4/G12) and `design/design-s7-wave-plan.md` (the W0-CONTRACTS acceptance clause),
and cross-checked against `standard.py`, `types.py`, `use_relation_h005.py` and
`deepreason_core.harness`.

Method note: every finding below was executed by a script under `probe/` run with
`python3 probe/<name>.py` from the sandbox root; the sandbox root and `src` were put
on `sys.path`. The whole package imports in this sandbox (jsonschema 4.25.1).
`tests/loop/test_contracts.py` is not shipped in this snapshot, so claims the
interface pins on that file are checked by probe against the reachable code instead
and are flagged where only the test was said to enforce them.

Verdict in one sentence: the module does what its docstrings, the interface entries
and the design clauses it names say it does; the findings are one SHOULD-FIX seam
and four NOTEs. No BLOCKER was reproduced.

---

## BLOCKER

None reproduced. Three candidate seams were attacked and held; see "Tried, and could
not break".

## SHOULD-FIX

### F1 — The published, digest-pinned "same objects" are mutable in place, so the guard content can be edited at runtime without touching the proxy and without changing the pinned digest

Defect location: `src/minireason/loop/contracts.py` lines 143–165 (the import of
`SCHEMAS`, `WORD_LIMITS`, the five role schemas and the per-role constants from
`minireason.loop.standard`), together with the live validator built over those same
objects at lines 644–646 (`_VALIDATORS = MappingProxyType({role:
Draft202012Validator(schema) ...})`) and consumed at line 799 inside `check`. The
underlying objects are `standard.py` lines 770 (`WORD_LIMITS = MappingProxyType`),
787–908 (the five schemas as plain `dict`s, `SCHEMAS = MappingProxyType`, and
`ROLE_SCHEMAS_SHA256` frozen once at import at line 908).

Contradicted sentence. Module docstring, lines 44–53: *"The names on both sides are
the *same objects*: there is nothing left to drift … The body now carries the word
limits and ``sha256(canonical(SCHEMAS))``."* — and standard deviation 6
(`standard.py` module docstring): *"Editing either changes
`:data:`STANDARD_BODY_SHA256`."* That is true of an *edit on disk*. It is not true of
an in-place edit at runtime, which changes the live validator and leaves
`STANDARD_BODY_SHA256` / `ROLE_SCHEMAS_SHA256` unchanged.

Probe (`probe/p06b_restore.py`), verbatim:

```
pristine: check('defender', {}) ok=False reason=missing-field
mutated : check RAISED KeyError: 'answer' -- 'never raises' broken under in-place mutation
mutated : full body ok=True value=DefenderOutput(answer='a', concedes=True)
mutated : recomputed digest == pinned digest: False  (False means the digest still points at the PRE-mutation schemas)
restored: check('defender', {}) ok=False reason=missing-field
restored: recomputed digest == pinned digest: True
```

The top-level `MappingProxyType` blocks `SCHEMAS["defender"] = …` (probe
`p06_schemas.py`: `top-level proxy blocks SCHEMAS['defender']=...: True`), but the
nested `dict`s the proxy wraps are the same `dict` objects the live
`Draft202012Validator` reads. `contracts.DEFENDER_SCHEMA["required"].clear()` — a
one-line in-place edit by any code that can import the module — turns
`check("defender", {})` from `missing-field` into a `KeyError` escaping the function
whose docstring (lines 783–786) says **"Never raises"**, because the schema gate now
passes `{}` to `_build` (line 765), which assumes the schema gate passed. The pinned
digest does not move. This is exactly the failure mode deviation 6 was introduced to
close ("editing a schema or a word limit changed no digest at all"), reproduced at
runtime rather than on disk.

`schema_for` (line 545) hands out `copy.deepcopy(SCHEMAS[role])`, so the intended
pattern exists; the published `SCHEMAS` itself still exposes the originals to any
caller.

Repair: freeze the schema objects structurally before the validators are built —
construct each schema (and `SCHEMAS`, and `WORD_LIMITS`) through a recursive
freeze-to-`MappingProxyType`/tuple pass in `standard.py`, so no `dict`/`list` inside
is reachable for in-place edit. `StandardInvalid` on mutation attempt is not needed;
unreachable mutable state is enough.

Test that would hold the repair: a wave-0 contract test that does
`pytest.raises(TypeError)` on `contracts.CRITIC_SCHEMA["required"].append("x")` and
on `contracts.SCHEMAS["defender"]["properties"]["answer"].clear()`, and then asserts
`check("defender", {})` still returns `ok=False, reason="missing-field"`.

---

## NOTE

### F2 — The variator schema admits any non-empty unique list; `paraphrase_n = 2` is a pinned guard parameter the schema does not encode

Defect location: `standard.py` lines 853–862 (`VARIATOR_SCHEMA`: `minItems: 1,
uniqueItems: true, items: {minLength: 1}`; no `maxItems`, no fixed length). Probed at
`probe/p06_schemas.py`.

Contradicted/partial clause. Design §2.3 publishes the variator contract as
`{"paraphrases": ["…", "…"]}` (two entries), §2.1 freezes `TRIAL_PARAPHRASE_N = 2`,
and G7 runs exactly `TRIAL_PARAPHRASE_N` paraphrases. Probe output, verbatim:

```
variator paraphrases schema: {"items": {"minLength": 1, "type": "string"}, "minItems": 1, "type": "array", "uniqueItems": true}
has maxItems: False  has fixed-length constraint: False
guard paraphrase_n frozen at: 2
check 3 paraphrases: ok=True  -> VariatorOutput(paraphrases=('a', 'b', 'c'))
```

A three-paraphrase variator output validates. This is not necessarily a guard hole —
the G7 caller in W2-ROLES will request `paraphrase_n` and may drop extras — but the
schema is the module's own claim of what a model "is allowed to hand back" (module
docstring line 5), and a length-2 contract is expressible in JSON Schema
(`minItems: 2, maxItems: 2`). As shipped, the schema does not encode the count the
standard freezes.

Repair: either set `minItems == maxItems == GUARD_PARAMETERS["paraphrase_n"]` in
`VARIATOR_SCHEMA` (and let the schema say so), or state in the variator docstring
that count enforcement is the caller's. Test: `check("variator", {"paraphrases":
["a","b","c"]})` must not be `ok`.

### F3 — `AGGREGATE_KEYS` is documented as "NOT applied to artifacts", and probed so; the schemas can therefore *express* a numeric content value even though property *names* are banned

Defect location: `contracts.py` lines 276–281 (`AGGREGATE_KEYS` frozenset),
610–638 (`assert_no_aggregate_fields`, which bans `number`/`integer` *types* and
aggregate *property names*), and the interface §3 entry: *"AGGREGATE_KEYS …
schema-name ban, wider than FORBIDDEN_KEYS; NOT applied to artifacts."* Probed at
`probe/p12_aggregate.py`, verbatim:

```
artifact with 'count'/'total' keys under assert_no_scoring_keys: passed
artifact with numeric values under assert_no_scoring_keys: passed
schema with integer property: raised ContractError code=CONTRACT_VIOLATION
schema open object (no additionalProperties False): raised ContractError code=CONTRACT_VIOLATION
schema with property named 'tally': raised ContractError code=CONTRACT_VIOLATION
AGGREGATE_KEYS disjoint from FORBIDDEN_KEYS: True
```

This is internally consistent and matches the interface line, so it is a NOTE, not a
SHOULD-FIX: the schema audit works on schemas, and the key guard (G12) works on
keys. But the module's own "What this is NOT" paragraph (lines 30–33) says there is
"no field of any schema numeric" — true of the *owned* five — while an artifact whose
keys are clean can still carry a bare number in a value and pass both guards
(`"cycle": 3, "word_total": 42` passed). That is by design (a block register prints
counts by reason code), but a reader of the docstring could miss that G12 over an
artifact is a *key-name* scan only, never a value scan.

Repair: none required against the code; the interface line already records it. The
module docstring could carry one sentence saying numeric *content* in an artifact is
not scanned, beside the key-name scan it does describe.

### F4 — `contracts.py` holds a `SCHEMAS` the wave plan published, but the `SCHEMA_REASONS` table and `AGGREGATE_KEYS` are its own two vocabularies; the interface records both, and probes confirm neither leaks into the other's grain

Defect location: `contracts.py` lines 288–307 (`SCHEMA_REASONS`, 18 members) and
276–281 (`AGGREGATE_KEYS`); the ownership boundary the interface §0 draws. Probed at
`p02_exceptions.py`:

```
2d reasons emitted by check(): ['case-required', 'difference-kind-forbidden', 'difference-kind-required', 'difference-kind-unknown', 'missing-field', 'not-an-object', 'not-in-enum', 'not-json', 'passage-quote-required', 'quote-required', 'too-few-items', 'unexpected-field', 'unknown-register', 'word-limit', 'wrong-type']
2d reasons emitted but NOT in SCHEMA_REASONS: []
2d SCHEMA_REASONS members not produced by this sweep: ['empty-field', 'not-unique', 'unknown-role']
```

Every reason `check()` emits is a declared `SCHEMA_REASONS` member; the three not
produced by that sweep are all reachable (probe `p03_outside_vocabulary.py`:
`unknown-role` from a bad role name, `empty-field` from a minLength breach,
`not-unique` from a duplicated paraphrase). All 18 are spelled `lower-with-hyphens`,
disjoint from both `BLOCK_CODES` and `FAILURE_CODES` (types.py's partition rule), and
`str(ScoringKeyForbidden()) == 'SCORING_KEY_FORBIDDEN'` exactly, so the loop's
`code_of` reads it unchanged. No repair.

### F5 — The O2 collision is real in this sandbox: `verdict` is in `FORBIDDEN_KEYS`, the vendored `Warrant` carries it, and the guard refuses the vendored record — and the test said to pin it is not shipped here

Defect location: none in code — this is confirmation of a documented open question.
Interface O2: *"Design D2 gives the reading warrant `verdict: "fail"`; `verdict` is
a member of … `FORBIDDEN_KEYS` … pinned with
`tests/loop/test_contracts.py::test_the_guard_refuses_the_vendored_warrants_own_verdict_field_name`."*
Probed at `probe/p04b_warrant.py`, verbatim:

```
Warrant dict keys: ['commitment', 'id', 'target', 'trace_ref', 'type', 'validity_node', 'verdict']
verdict value: 'fail'
guard over Warrant record: raised ScoringKeyForbidden code=SCORING_KEY_FORBIDDEN path=('verdict',)
Commitment source lines w/ forbidden tokens: []
```

and at `p10_misc.py`: `'verdict' in FORBIDDEN_KEYS: True`. The collision premise O2
describes holds exactly as recorded. The O2 recommendation — run the guard over
artifact *content* only, never over the vendored record — is a W1-GRAPH
responsibility, not a `contracts.py` defect. The one caveat for this module: the
pinning test name appears only in `notes/WAVE0-INTERFACE.md` in this sandbox (probe
output: `O2 pinned test name FOUND in …/notes/WAVE0-INTERFACE.md`; `not found under
sandbox (tests not shipped)`), so in this frozen snapshot the guard's refusal of the
vendored record is verified by probe only, not by the named test.

Repair: none here. W1-GRAPH's docstring must say it never runs
`assert_no_scoring_keys` over vendored records, as O2 already recommends.

---

## Tried, and could not break

**1. `check()` never raises, over boundary inputs** (`probe/p01_totality.py`,
`p08_shapes.py`). Fed: `None`, bare `[]`, non-JSON text, invalid-UTF-8 bytes,
UTF-8-BOM bytes, a `str` with U+FEFF prefix, wrong-typed values in every field of
every role, and a `MappingProxyType` body. Every case `returned` a `Validation`
(`ok=False` with a declared reason); none raised. Dict and JSON-text forms of the
same value agree (`8c`). I suspected a `dict`-vs-`Mapping` or a `float('nan')`
crash; none reproduced. The one way `check` raises is the deliberate in-place schema
mutation of F1, which is a caller reaching around the published seam, not an input.

**2. G4/D6 normalisation and the transcript gate** (`probe/p03_outside_vocabulary.py`,
`p07_transcript.py`). A critic naming a relation with a non-empty
`outside_vocabulary` is normalised to `relation='none'` with the nominated token kept
on `nominated_relation` and `claims_relation=False`, so it never reaches a
transcript; a `none` row with empty case/quote validates and never claims a relation;
and a fully-populated nominal exchange passes the vendored
`deepreason_core.harness.conforming_transcript` gate (`7a
gate(case='c', answer='a', decisive='c'): True`). I suspected the normalisation
either dropped the outside-vocabulary text or let a relation through; it does
neither, and `.as_dict()` round-trips through `check` for nominal, `none` and
outside-vocabulary rows alike.

**3. The G12 guard's three subjects** (`probe/p04_g12.py`, `p09_headers.py`).
Key-structure: case-folded `SCORE` nested in dicts/lists/tuples and through an
`OrderedDict` root all raise `ScoringKeyForbidden` with a precise path. Rendered
file: a bare `str`/`bytes`/`bytearray` raises `ContractError` (the documented
refusal, code `CONTRACT_VIOLATION`), and `assert_no_scoring_headers` (the
`contracts` re-export *is* `standard`'s object; `9i … is standard's: True`) catches
a scoring word in a table header, an implicit-table header, and an ATX heading —
while passing the word in a table *body* row, in prose, and in a non-ATX seven-hash
line. I suspected a non-contiguous second table or a pipe inside a heading would
slip past or false-positive; the scanner handled both per its own docstring
("the header row … of each contiguous block of pipe rows").

**4. The closed-marker `difference_kind` per register** (`probe/p05_identity.py`).
`VALIDATORS["marker"]` forwards `register=`; a `target_set_membership` kind passes
the union and register `T`, and is refused on register `G`
(`difference-kind-unknown`). `ALL_DIFFERENCE_KINDS` is the 7 tokens, sorted, exactly
as the interface records.

---

## What was verified to hold (no finding)

* **One owner, same objects**: every re-exported name (`READING_VOCABULARY`,
  `CRITIC_RELATIONS`, `REGISTERS`, `DIFFERENCE_KINDS`, `FORBIDDEN_KEYS`, `SCHEMAS`,
  `WORD_LIMITS`, `ROLE_NAMES`, `READING_BANNER`, `MARKS`, the five schemas,
  `UNRESOLVED`, `assert_no_scoring_headers`) is the *identical* object to
  `standard`'s; `READING_VOCABULARY is use_relation_h005.ROOT_READING_VOCABULARY`
  and the banner is the instrument's own string (`probe/p05_identity.py`). The
  acceptance clause "imported, not retyped" holds by `is`, not merely by equality.
* **The digest pin**: `recomputed sha256(canonical(SCHEMAS)) == body
  role_contracts.schemas_sha256 == standard.ROLE_SCHEMAS_SHA256` (`p06_schemas.py`).
  Editing a schema on disk would move the digest; F1 is the runtime seam beside this.
* **Exception conventions**: `ScoringKeyForbidden`/`SchemaInvalid`/`ContractError`
  are all `LoopError` and all `ValueError`; `str(ScoringKeyForbidden())` is exactly
  `SCORING_KEY_FORBIDDEN` (`p02_exceptions.py`, `p10_misc.py`).
* **Purity and determinism**: three identical `check` calls return equal
  `Validation` objects; a multiply-broken body reports the same first error across
  runs (`p06b_restore.py`, `p08_shapes.py 8e`).
* **`SCHEMA_REASONS` completeness**: every reason `check()` emits is in the table;
  all 18 are reachable and spelled in the `lower-with-hyphens` grain types.py's rule
  assigns to them (`p02_exceptions.py`, final `run_command`).

---

## Probes left behind

`probe/p01_totality.py` … `probe/p12_aggregate.py` (with `p04b_warrant.py`,
`p06b_restore.py`). Each is self-contained, puts the sandbox root and `src` on
`sys.path`, and prints the executed evidence quoted above. Last full test run in the
sandbox: `python3 run_tests.py` → `Ran 0 tests … OK` (no test modules are shipped in
this snapshot); an attempted `python3 run_tests.py tests.loop.test_contracts`
failed with `ModuleNotFoundError: No module named 'tests.loop.test_contracts'`,
confirming the suite the interface cites is not present here.
