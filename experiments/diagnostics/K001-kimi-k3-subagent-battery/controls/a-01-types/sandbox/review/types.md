# Adversarial review — `src/minireason/loop/types.py` (W0-TYPES)

Read first: `notes/WAVE0-INTERFACE.md`, then the module, then
`design/design-s2-roles-and-guard.md` and `design/design-s7-wave-plan.md`.

Everything below was executed. Probes are under `probe/` and were run as
`python3 probe/<name>.py` from the sandbox root; each probe puts the sandbox root
and `src` on `sys.path` exactly as `run_tests.py` does and imports nothing else.
`python3 run_tests.py tests.loop.test_types` reports
`ModuleNotFoundError: No module named 'tests.loop.test_types'` in this snapshot,
and `python3 run_tests.py` discovers `Ran 0 tests`, so the module's own suite is
not available here as a cross-check; the probes are the whole evidence base.

Findings are ordered BLOCKER, SHOULD-FIX, NOTE. Nothing is ranked inside a band.

---

## BLOCKER 1 — `_digests` folds two spellings of one path into one key, so `loop_plan_id` depends on pin order and a changed pin can leave the identity unchanged

**Where.** `src/minireason/loop/types.py:580-590` (`_digests`), reached from
`loop_plan_id` at `:943-947` and from `StepReceipt.key` at `:1101-1110`.

```python
def _digests(value: Any, where: str, code: str = "CONFIG_INVALID_VALUE") -> dict[str, str]:
    out: dict[str, str] = {}
    for key, digest in _mapping(value, where).items():
        out[_relative(key, f"{where} key", code)] = (...)
    return dict(sorted(out.items()))
```

`_relative` ends `return Path(text).as_posix()` (`:536`), which normalises
`./src/a.py`, `src//a.py`, `src/./a.py` and `src/a.py/.` all to `src/a.py`. The
loop writes each normalised key into `out` with no collision check, so the last
spelling in iteration order wins and the earlier one is dropped.

**What it contradicts.**

* `src/minireason/loop/__init__.py:100-103`: "**`loop_plan_id(config, pins)`
  refuses a null pin.** A pin whose value is `None`, not a lowercase sha256, or
  keyed by an absolute or `..`-bearing path is `PIN_INVALID`: an unpinned file
  inside a plan identity pins nothing. Pin *order* does not affect the identity;
  a declared config value does."
* `notes/WAVE0-INTERFACE.md:366-367`: "Pin *order* does not affect the identity; a
  declared config value does."
* `types.py:936-939`: "Formatting, key order and resolved defaults are therefore
  not part of the identity, but every declared value is. `pins` maps a
  repo-relative path to its lowercase sha256; a null pin is refused, since an
  unpinned file inside a plan identity pins nothing."
* `design/design-s7-wave-plan.md:11`, the W0-TYPES acceptance line: "Two loads of
  one config give the same plan_id; **a changed pin changes it**; …"

**Probe.** `probe/p01_pin_key_normalisation.py`, verbatim:

```
--- 1. two spellings of one path, both accepted by _digests
_digests: {'src/a.py': '2222222222222222222222222222222222222222222222222222222222222222'}

--- 2. a pin that changes does NOT change the plan id
pins A = {'src/a.py': H1, './src/a.py': H2} -> 04981a7c38977cd70edd45515489020fd6b15d6a8373f9a83d75a816bede6741
pins B = {'src/a.py': H3, './src/a.py': H2} -> 04981a7c38977cd70edd45515489020fd6b15d6a8373f9a83d75a816bede6741
H1 != H3 but ids equal: True

--- 3. an added pin is silently dropped
one pin  -> 48ca352b161a02319606a69d28d20b82b9c1eaa0332048f6c0f3bf06f2bebfc8
two pins -> 48ca352b161a02319606a69d28d20b82b9c1eaa0332048f6c0f3bf06f2bebfc8
ids equal: True

--- 4. pin ORDER changes the identity
order 1 -> 04981a7c38977cd70edd45515489020fd6b15d6a8373f9a83d75a816bede6741
order 2 -> 48ca352b161a02319606a69d28d20b82b9c1eaa0332048f6c0f3bf06f2bebfc8
ids equal: False

--- 5. the same hole in StepReceipt.key (inputs_sha256)
inputs {x: H1, ./x: H2} -> 2b06c2f31d5339035b2fb6f93e392dfe6bba655ed1622f17f9847f0f7f9fb8f6
inputs {x: H3, ./x: H2} -> 2b06c2f31d5339035b2fb6f93e392dfe6bba655ed1622f17f9847f0f7f9fb8f6
step keys equal: True

--- 6. contrast: _relatives (occurrences) DOES refuse the same collision
_relatives: raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: occurrences must not repeat a path'

--- 7. other spellings that normalise together
  'src/a.py'       -> 'src/a.py'
  './src/a.py'     -> 'src/a.py'
  'src//a.py'      -> 'src/a.py'
  'src/./a.py'     -> 'src/a.py'
  'src/a.py/.'     -> 'src/a.py'
```

Section 2 is the acceptance clause failing directly: the digest pinned for
`src/a.py` changes from `H1` to `H3` and the plan id does not move. Section 4 is
the order claim failing: the same two key/value pairs in the other insertion
order mint a different id — and, read against section 3, the id a reordered map
produces is the id of a *different pin set*. Section 5 carries both faults into
`step_key`, which W1-STEPS uses as the resume coordinate: two steps whose input
digests genuinely differ are one step.

Section 6 is the strongest internal evidence that this is an oversight rather
than a policy: `_relatives` (`:562-567`) applies the same normalisation and then
*does* refuse a post-normalisation duplicate. Two sibling helpers, one guard.

**Repair.** In `_digests`, detect the collision instead of overwriting:

```python
for key, digest in _mapping(value, where).items():
    path = _relative(key, f"{where} key", code)
    if path in out:
        raise _fail(code, f"{where} names {path!r} twice")
    out[path] = ...
```

(`code` is already threaded through, so pins get `PIN_INVALID` and
`inputs_sha256` gets `STEP_RECEIPT_INVALID` — subject to SHOULD-FIX 3.)

**Test that would hold it.**
`loop_plan_id(cfg, {"src/a.py": H1, "./src/a.py": H2})` raises `LoopError` with
`.code == "PIN_INVALID"`; and, as a property, for every pair of distinct pin maps
drawn from `{"a.py","./a.py","a//b.py"} × {H1,H2}` either both are refused or the
ids differ; and `loop_plan_id(cfg, dict(reversed(list(pins.items())))) ==
loop_plan_id(cfg, pins)` for every accepted `pins`. The same three assertions
against `StepReceipt.key(..., inputs_sha256=...)`.

---

## BLOCKER 2 — `_sequence`'s "a list, not a string" guard does not fire on two of the three doors into `CustodyReport`, so a custody block of one code is recorded as one check per character

**Where.** `src/minireason/loop/types.py:967-1009`. The guard is at `:548-551`:

```python
def _sequence(value: Any, where: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise _fail("CONFIG_INVALID_VALUE", f"{where} must be a list")
```

`__post_init__` (`:967-972`) routes `checks` through it. But `from_mapping`
(`:974-980`) calls `tuple(raw.get("checks", ()))` **before** `__post_init__` sees
the value, and `from_findings` (`:1001`) calls `rows = tuple(findings)`. By the
time `_sequence` runs, a string has already become a tuple of one-character
strings, each of which passes `_text`. The corrupted block reaches a published
receipt through `StepReceipt.from_dict` (`:1146`).

**What it contradicts.**

* `types.py:956-962` (`CustodyReport`): "`checks` holds stable codes — a
  `FAILURE_CODES` member, a pinned path — not prose: a receipt is read by a
  program."
* `types.py:995-998` (`from_findings`): "`checks` keeps one code per finding, in
  the order `verify_pins` returned them (sorted by path, then code), and does
  **not** de-duplicate: two files that moved are two checks, and a receipt that
  collapsed them would under-report the halt."
* `notes/WAVE0-INTERFACE.md:117-118`: "`checks` keeps **one code per finding**, in
  `verify_pins`' order, and does not de-duplicate."

One code per finding is the invariant; nineteen checks for one finding breaks it
in the opposite direction from the one the docstring guards against.

**Probe.** `probe/p03_custody_checks_string.py`, verbatim:

```
--- door 1: the constructor (goes through _sequence)
constructor: raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: custody.checks must be a list'

--- door 2: from_mapping (tuple() before _sequence sees it)
from_mapping: accepted, len(checks) = 19
from_mapping: as_dict() = {'verified': False, 'checks': ['S', 'O', 'U', 'R', 'C', 'E', '_', 'P', 'I', 'N', '_', 'M', 'I', 'S', 'M', 'A', 'T', 'C', 'H']}

--- door 3: from_findings on a bare string
from_findings: accepted, len(checks) = 19
from_findings: verified = False

--- it reaches a published step receipt through from_dict
receipt accepted; custody block re-emitted as:
  {'verified': False, 'checks': ['S', 'O', 'U', 'R', 'C', 'E', '_', 'P', 'I', 'N', '_', 'M', 'I', 'S', 'M', 'A', 'T', 'C', 'H']}
number of custody checks recorded: 19

--- and the honest record, for comparison
from_findings([one finding]): {'verified': False, 'checks': ['SOURCE_PIN_MISMATCH']}
```

Door 1 shows the guard exists and works. Doors 2 and 3 show it is bypassed, and
the fourth block shows the result surviving `StepReceipt.from_dict` and being
re-emitted by `as_dict` — a halt receipt that a reader or a W3-REPORT block
register would read as nineteen custody findings.

Note the reachability: door 2 is exactly the path a receipt read back off disk
takes, and a hand-edited or hand-written `custody: {"checks": "SOURCE_PIN_MISMATCH"}`
is the most natural mistake a human makes in that JSON.

**Repair.** Pass the raw value through, and let `_sequence` decide:

```python
return cls(verified=raw.get("verified", False), checks=raw.get("checks", ()))
```

and in `from_findings`, refuse a bare string/bytes argument before iterating:

```python
if isinstance(findings, (str, bytes)):
    raise _fail("STEP_RECEIPT_INVALID", "custody findings is a sequence of findings")
rows = tuple(findings)
```

**Test that would hold it.** `CustodyReport.from_mapping({"checks": "X_Y"})`,
`CustodyReport.from_findings("X_Y")` and
`StepReceipt.from_dict({... "custody": {"checks": "X_Y"}})` each raise `LoopError`;
and for every finding list `f`, `len(CustodyReport.from_findings(f).checks) == len(f)`.

---

## SHOULD-FIX 3 — the `code` argument is not honoured on every refusal path, so pin and step-receipt refusals surface under `CONFIG_INVALID_VALUE`, and a receipt's out-of-range cycle does not use `CYCLE_OUT_OF_RANGE`

**Where.** `src/minireason/loop/types.py:497-500` (`_text`), `:509-514` (`_whole`),
`:539-545` (`_mapping`) hard-code `"CONFIG_INVALID_VALUE"`, while `_identifier`
(`:503-506`), `_relative` (`:529-536`) and `_digests` (`:580-586`) take a `code`
parameter. `_relative` calls `_text` first (`:532`) and `_digests` calls
`_mapping` first (`:582`), so the caller's `code` is lost on those paths.
Consumers: `loop_plan_id` `:946` passes `"PIN_INVALID"`; `StepReceipt.__post_init__`
`:1055, :1058-1061` and `StepReceipt.key` `:1105, :1108-1109` pass
`"STEP_RECEIPT_INVALID"`.

**What it contradicts.**

* `src/minireason/loop/__init__.py:100-103`: "A pin whose value is `None`, not a
  lowercase sha256, or keyed by an absolute or `..`-bearing path is `PIN_INVALID`".
  The three refusals below are pin refusals and are not `PIN_INVALID`.
* `types.py:1310` declares a dedicated code for exactly this fact —
  `raise _fail("CYCLE_OUT_OF_RANGE", "a cycle index is a whole number 1..99")` —
  and the receipt path for the same fact reports `CONFIG_INVALID_VALUE`.
* `notes/WAVE0-INTERFACE.md:122-125` publishes the eleven codes `types` raises;
  all three of `PIN_INVALID`, `CYCLE_OUT_OF_RANGE` and `STEP_RECEIPT_INVALID` are
  in it, so a caller that dispatches on `.code` is entitled to expect the one that
  names the fact.

**Probe.** `probe/p02_code_routing.py`, verbatim (excerpt):

```
--- pins: the package docstring promises PIN_INVALID
pins is not a mapping        : raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: pins must be an object'
pin key is the empty string  : raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: pins key must be a non-empty string'
pin key is whitespace        : raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: pins key must be a non-empty string'
pin key is not a string      : raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: pins keys must be strings'
  for comparison, the paths the docstring names:
pin key is absolute          : raised LoopError code='PIN_INVALID' msg='PIN_INVALID: pins key must be a relative path inside the repository'
pin key bears ..             : raised LoopError code='PIN_INVALID' msg='PIN_INVALID: pins key must be a relative path inside the repository'
pin value is null            : raised LoopError code='PIN_INVALID' msg="PIN_INVALID: pins['src/a.py'] must be a lowercase sha256 hex digest"

--- step receipts: the module has CYCLE_OUT_OF_RANGE and STEP_RECEIPT_INVALID
RunPaths.cycle(0)            : raised LoopError code='CYCLE_OUT_OF_RANGE' msg='CYCLE_OUT_OF_RANGE: a cycle index is a whole number 1..99'
StepReceipt.key cycle=0      : raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: cycle must be a whole number from 1 to 99'
StepReceipt.key cycle=100    : raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: cycle must be a whole number from 1 to 99'
StepReceipt.build cycle=0    : raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: cycle must be a whole number from 1 to 99'
StepReceipt.key inputs=[]    : raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: inputs_sha256 must be an object'
StepReceipt.key inputs {'':h}: raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: inputs_sha256 key must be a non-empty string'

--- CustodyReport: from_findings' docstring says STEP_RECEIPT_INVALID
finding carries code=None    : raised LoopError code='STEP_RECEIPT_INVALID' msg='STEP_RECEIPT_INVALID: custody finding 0 carries no code'
finding carries code=''      : raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: custody.checks[0] must be a non-empty string'
finding carries code=7       : raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: custody.checks[0] must be a non-empty string'
```

The last block is the same defect inside one method: a finding whose `.code` is
`None` gets `STEP_RECEIPT_INVALID` from the hand-written check at `:1006`, and a
finding whose `.code` is `""` or `7` gets `CONFIG_INVALID_VALUE` from `_text` one
line later.

This is not a cosmetic complaint. `LoopError` carries no structured field but
`.code`, W1-STEPS records exactly one code on a halt receipt (`types.py:93-96`:
"a halt receipt records one code, so there is one place a reader looks it up"),
and W6-DOC's acceptance is "Every failure code … the driver can emit appears on
the page". A pin failure filed under a configuration code is filed in the wrong
place on the operator page.

**Repair.** Give `_text`, `_whole` and `_mapping` the same
`code: str = "CONFIG_INVALID_VALUE"` parameter the other three helpers have, and
thread it: `_relative` → `_text`; `_digests` → `_mapping` and `_relative`;
`StepReceipt.__post_init__` and `.key` → `_whole(self.cycle, "cycle", low=1,
high=99, code="CYCLE_OUT_OF_RANGE")`; `CustodyReport` → `_text(code=
"STEP_RECEIPT_INVALID")`.

**Test that would hold it.** A table-driven test over every public entry point,
asserting the `.code` of the refusal: every malformed `pins` argument to
`loop_plan_id` gives `PIN_INVALID`; every malformed `inputs_sha256`, `wave`,
`started_utc` or `checks` in a receipt gives `STEP_RECEIPT_INVALID`; every
out-of-range cycle, from `RunPaths.cycle`, `StepReceipt.key`, `StepReceipt.build`
and `StepReceipt.from_dict` alike, gives `CYCLE_OUT_OF_RANGE`.

---

## SHOULD-FIX 4 — the one parameterised member of the stop vocabulary is unfiltered, so `is_stop_reason` admits a stop reason that names exhaustion

**Where.** `src/minireason/loop/types.py:435-444`.

```python
    if not token.startswith(PREREGISTERED_CONDITION_PREFIX):
        return False
    return bool(_ID.fullmatch(token[len(PREREGISTERED_CONDITION_PREFIX):]))
```

`_ID` is `[A-Za-z0-9][A-Za-z0-9_.-]{0,63}\Z` (`:482`) and admits `exhaustion`.

**What it contradicts.**

* `types.py:12-16`: "`resource_boundary` names a declared budget — an
  attention-and-spend boundary, never a claim that an inquiry ran out of things to
  say — and the stop vocabulary carries no token that would say otherwise
  (`tests/loop/test_types.py` names the token it must never carry)."
* `design/design-s7-wave-plan.md:11`: "the token 'exhaustion' appears in no
  vocabulary".
* `src/minireason/loop/data/ceiling_v1.md:17`: "**A reached ceiling is a declared
  resource boundary, not exhaustion of the inquiry**".

**Probe.** `probe/p05_stop_vocabulary.py`, verbatim (excerpt):

```
--- the parameterised tail
  'preregistered_condition:obligation-o3'      -> True
  'preregistered_condition:exhaustion'         -> True
  'preregistered_condition:inquiry_exhausted'  -> True
  'preregistered_condition:nothing_left_to_say' -> True
  'preregistered_condition:'                   -> False
  'preregistered_condition:../x'               -> False
  'exhaustion'                                 -> False
  'resource_boundary '                         -> False

--- the same token through block_code, for contrast
  block_code('exhaustion') -> BLOCK_CODE_UNKNOWN

--- and there is no is_block_reason/assert helper that would scan it
  names exported by types: ['is_stop_reason', 'is_failure_code']
```

The literal tables are clean — `probe/p04_acceptance_clauses.py` printed
`STOP_REASONS: 7 members, 'exhaust' hits: []` and the same for the other eight
tables — so the acceptance clause holds of the *constants*. It does not hold of
the *predicate*, which is what the rest of the package will call, and
`is_stop_reason` is the exported seam (`__all__`, `types.py:132`;
`notes/WAVE0-INTERFACE.md:87`). A pre-registered condition id flows into the
closing record as the stop reason, where W3-REPORT's acceptance is "no rendered
artifact contains … the token 'exhaustion'".

I am stating this as SHOULD-FIX rather than BLOCKER on one ground: the scan that
would catch it at render time is `standard.assert_no_exhaustion_claim`, which is
not in this snapshot, so I could not determine whether the token would in fact
reach a rendered artifact. The hole in `types` is real and executed; its
downstream consequence is not something I can show here.

**Repair.** Refuse the token inside the condition id, in the one place that owns
the stop vocabulary:

```python
tail = token[len(PREREGISTERED_CONDITION_PREFIX):]
if "exhaust" in tail.lower():
    return False
return bool(_ID.fullmatch(tail))
```

A blanket ban on the substring anywhere would be wrong — the ceiling's own denial
sentence contains it, which is why `standard.CEILING_EXHAUSTION_DENIAL` is
exempted — but a pre-registered *condition id* is a name the operator chooses,
and there is no sentence to preserve inside it.

**Test that would hold it.** `is_stop_reason("preregistered_condition:exhaustion")`
is `False`, and for every `t` in `STOP_REASONS` plus every token `is_stop_reason`
accepts, `"exhaust" not in t.lower()` — a property asserted over a generated set of
condition ids, not over a fixed list.

---

## SHOULD-FIX 5 — `loop_plan_id` never requires the six `PINNED_SOURCE_PATHS`, so a plan identity that pins none of them is minted without complaint

**Where.** `src/minireason/loop/types.py:179-190` (the constant) and `:930-947`
(`loop_plan_id`, which reads only its `pins` argument).

**What it contradicts.** `types.py:179-182`, the constant's own docstring: "The
fixed repo-relative files design 4.2 pins into `loop_plan_id`. The rest of that
list — prompt templates, `obligations.json`, `CEILING.md`, the standard body, each
attached study's `PLAN.md` and `material.json` — is run-specific and is supplied
by the caller of :func:`loop_plan_id`." The sentence distinguishes a *fixed* part
from a *caller-supplied* part; in the code both parts are caller-supplied and
neither is required.

**Probe.** `probe/p06_smaller.py`, verbatim (excerpt):

```
--- PINNED_SOURCE_PATHS is exported but loop_plan_id never requires it
PINNED_SOURCE_PATHS = ('src/minireason/data/endpoints.json', 'src/minireason/graph_import_h005.py', 'src/minireason/provider_openai_compat.py', 'src/minireason/use_relation_h005.py', 'tools/contrast_triple_study.py', 'tools/multicycle_commitment_study_multi_v2.py')
loop_plan_id(cfg, {}) -> 03aff401826ba09a2d9e229e4d71e8099a550004b11e851f30530977205374cc
loop_plan_id(cfg, {'unrelated.txt': H1}) -> 46c2db6848469ae3e1f121781b2677edd6f07fd9532174a860e2448aeab32037
present in this snapshot:
  src/minireason/data/endpoints.json                       exists=True
  src/minireason/graph_import_h005.py                      exists=True
  src/minireason/provider_openai_compat.py                 exists=True
  src/minireason/use_relation_h005.py                      exists=True
  tools/contrast_triple_study.py                           exists=False
  tools/multicycle_commitment_study_multi_v2.py            exists=False
```

A run whose plan identity pins the transport and one whose plan identity pins
nothing are equally well-formed to this function; the second mints an id that
says "these sources were frozen" while freezing nothing. Since substituting a
source is supposed to mint a new `loop_plan_id`
(`design-s2-roles-and-guard.md:42-45`), the omission is silent where the
substitution would have been loud.

(The two `exists=False` rows are a fact about this snapshot, which carries no
`tools/` directory, not a claim about the staging clone.)

**Repair.** One of two, and the module should say which it chose:
either require the set —

```python
missing = sorted(set(PINNED_SOURCE_PATHS) - set(digests))
if missing:
    raise _fail("PIN_INVALID", f"plan identity does not pin: {missing}")
```

— or, if W1-STEPS is meant to own that check, change the constant's docstring to
say so and name the module, as the `graph_root` / PREFLIGHT note at `:620-626`
already does for `assert_config_matches_standard`.

**Test that would hold it.** `loop_plan_id(cfg, {})` raises `PIN_INVALID` naming
all six; `loop_plan_id(cfg, pins_for(PINNED_SOURCE_PATHS))` succeeds; dropping any
one of the six raises and names that one.

---

## NOTE 6 — `LoopConfig` and its four sub-records validate only through `from_mapping`; the exported constructors do not, and `loop_plan_id` passes a `LoopConfig` through untouched

`src/minireason/loop/types.py:857-860` short-circuits
(`if isinstance(raw, LoopConfig): return raw`) and `:942` relies on it. None of
the five config dataclasses has a `__post_init__`, unlike `StepReceipt` and
`CustodyReport`. `probe/p06_smaller.py`:

```
--- LoopConfig is a public dataclass with no __post_init__
LoopConfig has __post_init__: False
StepReceipt has __post_init__: True
hand-built config accepted by the constructor; its run_id is '../../etc'
loop_plan_id(hand-built, {}) -> 6001386c220cff93411435d4d438a989d35f20aed5436d19220eb42151187a33
LoopConfig.from_mapping(hand.as_dict()): raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: occurrences[0] must be a relative path inside the repository'
```

The last line is the mitigation: a config that skipped the loader cannot be
*re-loaded* from its own `as_dict`, so the damage does not survive a round trip
through a file. `types.py:813-815` says "Loading is strict: an unknown key is
refused rather than ignored, because a key the loader drops is a pre-registration
the run does not honour" — which is about loading, and is true. I record this as
a NOTE, not a finding against a claim: nothing in the interface promises the bare
constructor validates. The repair, if wanted, is a `__post_init__` on `LoopConfig`
that re-runs the field checks, or making `loop_plan_id` call
`LoopConfig.from_mapping(config.as_dict())` unconditionally.

## NOTE 7 — a step receipt's self-check binds five of its sixteen fields

`src/minireason/loop/types.py:1086-1090` recomputes the key from
`loop_plan_id, kind, cycle, wave, inputs_sha256`. `probe/p08_followups.py`:

```
--- 2. what the receipt's self-check binds, field by field
  edit index             -> ACCEPTED, step_key unchanged: True
  edit status            -> ACCEPTED, step_key unchanged: True
  edit outputs_sha256    -> ACCEPTED, step_key unchanged: True
  edit finished_utc      -> ACCEPTED, step_key unchanged: True
  edit published_commit  -> ACCEPTED, step_key unchanged: True
  edit custody           -> ACCEPTED, step_key unchanged: True
  edit spending          -> ACCEPTED, step_key unchanged: True
  fields in as_dict(): 16
```

This is correct behaviour for a *coordinate* — `step_key` names which step this
is, and `index`/`status`/`outputs` are what happened at it, which must be free to
change between the open marker and the close. But `types.py:38-41` says "A receipt
validates its own `step_key` … Both are derivable, and a record that could
disagree with the rule it is written under is a record that can lie", and
`:28-30` says "A receipt that cannot recompute its own key from its own bytes is
not checkable". A reader could take those sentences for tamper-evidence over the
record; they are not. Worth one sentence in the docstring naming the five bound
fields, so W1-STEPS does not lean on `step_key` for write-once-ness it does not
provide.

## NOTE 8 — the frozen records that carry a `MappingProxyType` are not hashable

`:785-787` and `:1058-1061` install `MappingProxyType` on frozen dataclasses,
which generate a `__hash__` from their fields. `probe/p06_smaller.py`:

```
--- frozen dataclasses that are not hashable
  frozen=True  hash(TimeoutsConfig()): raised TypeError code=None msg="unhashable type: 'mappingproxy'"
  frozen=True  hash(LoopConfig (loaded)): raised TypeError code=None msg="unhashable type: 'mappingproxy'"
  frozen=True  hash(StepReceipt): raised TypeError code=None msg="unhashable type: 'mappingproxy'"
  frozen=True  hash(CustodyReport()): returned -5190988587195632635
  frozen=True  hash(RunPaths): returned -3522383325734539194
```

`@dataclass(frozen=True)` ordinarily means hashable, and two of the five are. A
later wave that puts receipts in a set — W1-STEPS publishes
`completed_coordinates(out_dir) -> set` — meets a `TypeError`, not a `LoopError`.
Repair: `eq=True, frozen=True` with an explicit `__hash__` over
`tuple(sorted(...))` of the proxied mappings, or store the mappings as sorted
tuples of pairs and expose a mapping view.

## NOTE 9 — `LoopConfig.load` on a missing or unreadable path raises `OSError`, not a `LoopError`

`:846-855` catches `ValueError` (so a JSON syntax error becomes
`CONFIG_NOT_A_MAPPING`) but `Path(path).read_bytes()` runs first.
`probe/p06_smaller.py`:

```
LoopConfig.load('no-such-file.json'): raised FileNotFoundError code=None msg="[Errno 2] No such file or directory: ...
LoopConfig.load(<a directory>): raised IsADirectoryError code=None msg="[Errno 21] Is a directory: ...
```

`src/minireason/loop/__init__.py:64-65` says "So `except LoopError` catches every
refusal in the package". A driver wrapping `LoopConfig.load` in `except LoopError`
gets a traceback instead of a named refusal. `FAILURE_CODES` already carries
`LEDGER_NOT_FOUND` for the analogous receipts case; a `CONFIG_NOT_FOUND` (or
reusing `CONFIG_NOT_A_MAPPING` with the OSError chained) would close it.

## NOTE 10 — `StepReceipt.build` forwards `**rest` to the constructor, so a misspelled field is a `TypeError` where `from_dict` gives a named refusal

`:1112-1123` vs `:1125-1138`. `probe/p06_smaller.py`:

```
build(..., nonsense=1): raised TypeError code=None msg="StepReceipt.__init__() got an unexpected keyword argument 'nonsense'"
build(..., step_key='x'): raised TypeError code=None msg="minireason.loop.types.StepReceipt() got multiple values for keyword argument 'step_key'"
from_dict, by contrast:
from_dict({... 'nonsense': 1}): raised LoopError code='STEP_RECEIPT_INVALID' msg="STEP_RECEIPT_INVALID: unknown receipt keys: ['nonsense']"
```

Repair: validate `set(rest)` against the same `known` set `from_dict` uses,
minus the six `build` takes positionally, and raise `STEP_RECEIPT_INVALID`.

## NOTE 11 — `_relative` accepts spellings that are odd as repository paths

From `probe/p08_followups.py`:

```
--- 4. a few _relative spellings that are accepted
  _relative('.'): returned '.'
  _relative('a '): returned 'a '
  _relative('C:/x'): returned 'C:/x'
  _relative('a/b/'): raised LoopError code='CONFIG_INVALID_VALUE' msg='CONFIG_INVALID_VALUE: where must be a relative path inside the repository'
  _relative('a.py\t'): returned 'a.py\t'
  _relative('․․/x'): returned '․․/x'
```

None of these escapes the repository on POSIX — `.` is the root itself, `C:/x`
and `․․/x` (U+2024 ONE DOT LEADER, not `..`) are ordinary relative names — so this
is not a traversal finding. It matters only because these strings become keys in
a plan identity (`graph_root`, `obligations_path`, `occurrences`, pin keys) and,
downstream, directory names: `"a.py"` and `"a.py "` are two pins of one file.
Repair, if wanted: refuse a path whose components differ from their `strip()`,
and refuse a bare `.`.

---

# Tried, and could not break

Recorded because a failed attack is evidence about the module. Probes
`p04_acceptance_clauses.py`, `p07_attacks_that_failed.py`, `p08_followups.py`.

**1. Escaping the run tree.** Twelve `run_id` spellings — `../../etc`, `..`, `.`,
`a/b`, `a\b`, `""`, `~root`, `-x`, 65 characters, `․․/x` with U+2024, `a\n`,
`a%2f..%2fb` — every one `RUN_ID_INVALID`. `_ID`'s `\Z` anchor (not `$`) means a
trailing newline cannot be smuggled past it. Seven `reading_dir` row keys
including `../../../etc/passwd`, `..` and a 300-character key all produced a
directory inside `readings/`; `..` and `...` fold to the sentinel `row-<digest>`;
`a/b` and `a#b` fold alike and still got two directories
(`a_b-c14cddc033f6` and `a_b-8187fc8f7f00`), which is the property `:1323-1331`
claims. I did not attempt a birthday search against the 12-hex digest.

**2. Moving the plan identity without declaring a value.**
`probe/p04_acceptance_clauses.py` printed `load/load identical id: True`,
`mapping == object: True`, `config key order: True`, `defaults resolved: True`;
`probe/p07` printed `id stable across ensure_ascii True/False: True` for a config
carrying `é` and an em dash. Reflection over `dataclasses.fields` versus
`as_dict()` found no field of `LoopConfig`, `SeatsConfig`, `ContrastConfig`,
`AuditConfig` or `TimeoutsConfig` that fails to reach `as_dict` —
`fields-not-emitted = []` for all five — so every declared value is inside the
identity. A pin literally named `config` does not shadow the config block, which
is the named envelope earning its keep (`types.py:31-37`).

**3. Making a receipt lie.** `SEND` declared `spending=False` and `IMPORT`
declared `spending=True` are both `STEP_RECEIPT_INVALID`; a `COMPLETE` step with a
`failure_code` and a `HALTED` step without one are both refused; tampering with
any of `step_key`, `kind`, `cycle`, `wave`, `inputs_sha256` or `loop_plan_id` in
a serialised receipt gives `STEP_KEY_MISMATCH`. `from_dict(as_dict(r)) == r` and
`as_dict` is byte-stable. `cycle=1/wave=None` and `cycle=None/wave="1"` give
different keys, so the named envelope resists the type confusion a positional
tuple would allow.

**4. Turning a pre-registered guard parameter off from the config.**
`paraphrase_n=0` (G7 off), `schema_repair_budget=1` (a re-ask), and
`min_judge_families=1` (G0's cross-family rule) are each refused by range;
`judges=["a"]` with `min_judge_families=2` is refused; duplicate judge seats are
refused. `True` is refused as `cycle_budget`, `max_calls`, `max_per_key`,
`audit.period`, `audit.judge_err_max`, a cycle index and a step index — the
`type(value) is not int` idiom at `:511` does what its comment says.

**5. The ceiling reconciliation.** Parsing the block-register clause out of
`src/minireason/loop/data/ceiling_v1.md` gives
`['ensemble-split', 'referential-integrity', 'operative-target', 'order-swap',
'paraphrase-flip', 'outside-vocabulary', 'schema', 'provider',
'baseline-forced-same']`, identical to `CEILING_BLOCK_REASONS` *and in the same
order*; `BLOCK_CODES == {blocked:<r>} ∪ {blocked:constitution}` is `True` in both
directions; `block_code('made-up')` is `BLOCK_CODE_UNKNOWN`.

**6. The digest agreement.** `sha256_hex(canonical_json(v)) ==
provider_openai_compat.digest(v)` is `True` on a value carrying a nested object,
a null, a float, a bool and a non-ASCII string; `deepreason_core/canonical.py:14`
and `provider_openai_compat.py:148-149` use the same three options. The module
docstring's claim at `:18-22` holds for the transport half. `_MIN_SECRET_LENGTH`
is 8, matching `__init__.py:111-114`.

**7. The code table.** An AST walk of `types.py` (`probe/p08_followups.py`) finds
eleven literal codes reachable from a `_fail`/`LoopError` call or from a `code`
argument; all eleven are in `FAILURE_CODES`, and the set is *exactly* the eleven
`notes/WAVE0-INTERFACE.md:122-125` publishes — nothing missing, nothing extra.
`len(FAILURE_CODES) = 115` (both counts printed by that probe).

**8. Shape-check smuggling.** `LoopError("ABC\n")` and `LoopError("abc")` are both
`ValueError`; an uppercase 64-hex digest, a 63-character digest, a digest with a
trailing newline and a digest containing `g` are all `PIN_INVALID` (the uppercase
case had to be redone in `p08` — `p07` tested it with an all-digit digest, which
has no case, and that line of `p07`'s output should be disregarded). A naive
`started_utc` and a `+01:00` offset are both refused.

**9. Vocabulary hygiene.** Nine tables scanned for `exhaust`, zero hits:
`STOP_REASONS` (7), `BLOCK_CODES` (10), `CEILING_BLOCK_REASONS` (9),
`FAILURE_CODES` (115), `STEP_KINDS` (17), `STEP_STATUSES` (3), `PROVIDER_MODES`
(2), `REPLAYABLE_STEPS` (5), `SPENDING_STEPS` (8). `REPLAYABLE_STEPS` and
`SPENDING_STEPS` are disjoint subsets of `STEP_KINDS`, as
`notes/WAVE0-INTERFACE.md:79` says; the four kinds in neither are `CLOSE`,
`CYCLE_OPEN`, `PREPARE`, `PREREGISTER`. Unknown keys are refused at all five
levels of the config (`config`, `seats`, `audit`, `timeouts`, `contrast`).

---

# What I could not determine

* **The five sibling wave-0 modules are not in this snapshot.**
  `src/minireason/loop/` here contains only `__init__.py`, `types.py` and
  `data/`; `contracts.py`, `standard.py`, `custody.py`, `receipts.py` and
  `publish.py` are absent, and `tests/loop/` contains only `__init__.py`. So
  every cross-module claim that needs them is unresolved here, not confirmed and
  not refuted: `custody.CUSTODY_CODES ⊆ FAILURE_CODES`; the package-wide code
  scan the docstring attributes to `tests/loop/test_types.py`; the acyclic
  import-graph assertion; the claim that `SeatsConfig`'s ranges are
  `standard._INT_PARAMS`' own; and whether
  `standard.assert_no_exhaustion_claim` would catch SHOULD-FIX 4 downstream. I
  checked the ceiling correspondence against `src/minireason/loop/data/ceiling_v1.md`,
  the file `standard` is said to load — not against `standard.CEILING_TEXT` itself.
* **`python3 run_tests.py tests.loop.test_types` cannot run here** —
  `ModuleNotFoundError: No module named 'tests.loop.test_types'`, and a bare
  `python3 run_tests.py` discovers `Ran 0 tests`. I therefore could not check any
  finding against the module's own suite, or confirm the interface's "loop-only
  `224 tests OK`".
* **`tools/` is absent**, so the four "mirrors" claims are unresolved: that `_ID`
  is `multicycle_commitment_study_multi_v2.ID` (`:480-482`), that `_PUBLISH_REF`
  matches that module's `split_publish_ref` (`:486-490`), that `PROVIDER_MODES`
  mirrors its `PROVIDER_MODES` (`:431`), and that `max_per_key`'s ceiling of 5 is
  its `MAX_PER_KEY` (`:836-838`). On the one half I could check,
  `provider_openai_compat.slots_for(key_env, max_concurrency)` takes its ceiling
  from the caller and holds no constant 5, so "The real ceiling is
  `provider_openai_compat.slots_for`; this may not exceed it" is a claim I could
  neither verify nor contradict from this snapshot.
* **Design sections 4.1–4.4 and 5 are not in the sandbox** — only
  `design-s2-roles-and-guard.md` and `design-s7-wave-plan.md`. Where the module
  cites "design 4.2" or "design 4.3" I checked against its own docstring, the
  wave plan's one-line acceptance clause and `notes/WAVE0-INTERFACE.md`, not
  against the cited text. So I could not settle whether §4.2 requires
  `loop_plan_id` to fold `PINNED_SOURCE_PATHS` in (SHOULD-FIX 5 rests on the
  module's own sentence), whether the `step_key` field list is §4.3's, whether
  `LOOPS_ROOT` and the `.open` marker match §4.2's layout block, or whether
  `graph_root`'s "overrides" wording is §4.2's — which is open question O1's
  subject and is left to W1-GRAPH.
* **Suspected and could not reproduce.** I looked for a `reading_dir` collision
  between two row keys that fold alike *and* share a 12-hex digest prefix, and
  could not construct one; I did not run a birthday search, so this is unresolved
  rather than a finding. I also suspected that classing `AUDIT` as spending while
  `ADJUDICATE`, which §2.5 runs it inside, is replayable would show up as a
  defect in this module, and it does not: `types.py:407-409` states the nesting
  explicitly, the two sets are disjoint, and nothing in `types` decides resume
  behaviour — that is W1-STEPS'. I report both as unresolved and claim neither.
* **Left out.** I did not review `deepreason_core`, `graph_import_h005.py`,
  `use_relation_h005.py` or `provider_openai_compat.py` beyond the two specific
  cross-checks named above (`digest` serialisation, `_MIN_SECRET_LENGTH`). I did
  not attempt concurrency, filesystem or encoding attacks on `RunPaths`, since
  nothing in this module touches the filesystem. No finding here rests on a count;
  every count printed above names the probe that produced it.
