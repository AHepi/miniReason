# Adversarial review: W0-STANDARD (`src/minireason/loop/standard.py`)

Scope read first: `notes/WAVE0-INTERFACE.md`, `design/design-s2-roles-and-guard.md`,
`design/design-s7-wave-plan.md`, the module, its two data files, the vocabulary source
`src/minireason/use_relation_h005.py`, and the shared code tables in
`src/minireason/loop/types.py`. Two caveats about evidence before the findings:

1. The interface note publishes counts made on a quiesced tree that included
   `tests/loop/test_standard.py` ("loop-only 224 tests OK"). This snapshot carries no
   test modules under `tests/loop/` (only `__init__.py`), so nothing from that suite
   could be re-run; every claim below rests on the probes in `probe/` only.
2. The interface note and the module docstring make cross-module identity claims about
   `minireason.loop.contracts` ("`contracts.FORBIDDEN_KEYS` is this object",
   "`contracts.DIFFERENCE_KINDS` is this object"). `contracts.py` is not in this
   sandbox, so those claims are **unresolved** here, not findings either way.

## BLOCKER

None reproduced. Every published seam I attacked either held (round-trip, identity,
falsifier map, ceiling↔`BLOCK_CODES` correspondence) or failed in a way the module's
own docstring concedes (the read-side parse is shallow; the header scanner admits
non-pipe-row spellings it names out of scope). See "Tried, and could not break".

## SHOULD-FIX

### SF1 — `_validate_params` validates `unanimity_rule` and `reopen_reasons` by truthiness/iterability only: wrong types are silently converted, and two inputs escape as undeclared `TypeError`

**Claim:** the two non-int, non-bool guard parameters are checked with
`str(...).strip()` and `tuple(...)`, so values of the wrong type are silently
converted into the pinned body (`None` → a serialised `null` unanimity rule; a list →
a stringified rule accepted), while `reopen_reasons=0` or `None` raises a bare
`TypeError` that carries no code at all.

*Defect lives at:* `src/minireason/loop/standard.py:1260–1264` (`_validate_params`).

*Contradicted text:* the interface note's published exception contract for this module
("Codes: … `GUARD_PARAMETER_INVALID` … `REOPEN_REASON_SET_EMPTY`, `REOPEN_REASON_UNKNOWN`
…") and `build_standard`'s own docstring at line 1270: "Raises `StandardInvalid` with
a declared `code` for … an unknown, missing or out-of-range guard parameter, an
unlisted reopen reason". A `TypeError` is a declared refusal of nothing: it carries no
`code`, no receipt token, and the wave-0 convention "every wave-0 exception is a
`types.LoopError`" (interface §7) breaks on the seam the standard itself publishes.
Separately, R10 of the shipped rubric and design §2.4 G5 both state the unanimity
rule; a body carrying `unanimity_rule: null` states nothing, yet builds and pins.

*Probe:* `probe/guard_params2.py`, verbatim:

```
reopen_reasons=0: UNDECLARED TypeError: 'int' object is not iterable
reopen_reasons=None: UNDECLARED TypeError: 'NoneType' object is not iterable
unanimity_rule=0: accepted
unanimity_rule=None: accepted
unanimity_rule list ['x']: accepted
```

A majority-vote rule *string* is also accepted (`majority rule: accepted` in
`probe/guard_params.py`) — that one is by design (a successor standard mints a new
`loop_plan_id`). The type holes are not successor-standard material; they are
unvalidated garbage reaching the pinned digest.

*Repair:* check types before conversion — `isinstance(params["unanimity_rule"], str)`
(else `GUARD_PARAMETER_INVALID`), and
`isinstance(params["reopen_reasons"], (list, tuple))` (else `GUARD_PARAMETER_INVALID`).
*Test:* for each non-string `unanimity_rule` and each non-sequence `reopen_reasons`,
assert `StandardInvalid` with `code == "GUARD_PARAMETER_INVALID"`; assert no exception
other than `StandardInvalid` escapes `build_standard` for any mapping with all 12 keys.

### SF2 — `assert_config_matches_standard` reconciles only 3 of 12 guard parameters against a config, and deviation 8 overstates that reconciliation

**Claim:** the function described as refusing "a loop config whose `seats` block or
`reopen_reasons` contradict `GUARD_PARAMETERS`" only compares `min_judge_families`,
`paraphrase_n`, `schema_repair_budget`, and the length of the `judges` list. The four
seat *counts*, `marker_reuses_judge_seats`, `order_swap_both_orders` and
`min_resolved_replicates_per_case` are in the frozen map and are never reconciled.

*Defect lives at:* `src/minireason/loop/standard.py:1008–1024` (`GUARD_PARAMETERS`),
`1048–1052` (`_SEATS_TO_GUARD`), `1055–1100` (`assert_config_matches_standard`).

*Contradicted text:* deviation 8 of the module docstring:
"`assert_config_matches_standard` **refuses a loop config whose `seats` block or
`reopen_reasons` contradicts `GUARD_PARAMETERS`**" — unqualified, over a 12-key map of
which four keys have a config counterpart.

*Probe:* `probe/parse_and_reconcile.py` shows the check does fire where it claims to
(the default `SeatsConfig.as_dict()` reconciles; `paraphrase_n=3`, three named judges,
and `min_judge_families=3` all refuse with `GUARD_PARAMETER_INVALID`; a widened reopen
list refuses with `REOPEN_REASON_UNKNOWN`). What cannot be probed into existence is a
config contradiction of `judge_seats` or the two booleans: `SeatsConfig`
(`types.py:606`) declares no such key, so the reconciliation reaches the 4 expressible
parameters and not the other 8.

*Repair:* narrow deviation 8 and the function docstring to enumerate the reconciled
keys (or extend `SeatsConfig` and `_SEATS_TO_GUARD` together if a config is meant to
say more). *Test:* for each of the 12 keys, either a mock-config mutation that must
refuse with `GUARD_PARAMETER_INVALID`, or an explicit named entry in the docstring
recorded as standard-only.

### SF3 — `standard_body` validates shell, not content: a body with weakened guard parameters or rewritten register text parses without refusal

**Claim:** the parser checks the schema token, spec-id, section presence and scoring
keys, but never re-runs `_validate_params`, `_validate_registers` or
`_validate_vocabulary` on what it read — so bytes `build_standard` would refuse to
emit are returned as a standard body.

*Defect lives at:* `src/minireason/loop/standard.py:1347–1375` (`standard_body`).

*Contradicted text:* its docstring: "**Parse a serialised standard body and refuse
anything that is not one.**" A body with `guard_parameters.judge_seats = 1` (which
`build_standard` refuses at range `[2,8]`) or a `registers.T.plan_text` that no longer
matches the PLAN §8a mirror is not a body this module emits, and it is accepted.

*Probe:* `probe/parse_and_reconcile.py`, verbatim:

```
weakened guard params on read: accepted, judge_seats = 1
```

and `probe/more_attacks.py`, verbatim:

```
tampered register text on read: accepted; plan_text now: rewritten register text
```

In wave 1 the pinned digest makes such bytes detectable by identity, so this is a
latent rather than an active seam — but the docstring sentence is stronger than the
code, and any consumer that parses a body without checking its digest inherits the
gap.

*Repair:* either re-validate on read (compare a rebuild from parsed
registers/vocabulary/params against the raw bytes) or weaken the docstring to "refuse
anything whose shell is not this standard's; content identity is the digest pin's
job". *Test:* build the weakened body above, assert a `StandardInvalid` with a
declared code; assert the frozen body still round-trips.

### SF4 — the interface note's "FORBIDDEN_KEYS (G12, 24 keys)" is 25 tokens in the shipped module

**Claim:** the integrator's record of the shared constant says 24; the shipped object
carries 25.

*Defect lives at:* `src/minireason/loop/standard.py:217–221` (`FORBIDDEN_KEYS`);
contradicted record at `notes/WAVE0-INTERFACE.md:49`: "`FORBIDDEN_KEYS` (G12, 24 keys)".

*Probe:* `probe/secondary.py`, verbatim:

```
FORBIDDEN_KEYS count: 25
['best', 'better', 'creativity', 'grade', 'grades', 'merit', 'novelty', 'percentile',
 'points', 'quality', 'rank', 'ranking', 'ranks', 'rating', 'ratings', 'score',
 'scores', 'scoring', 'verdict', 'weight', 'weights', 'win', 'winner', 'worse',
 'worst']
```

Which side is off by one is unresolved from this sandbox: the upstream
`tools/contrast_triple_study.FORBIDDEN_KEYS` the set claims to mirror (deviation 5) is
not present to diff against. Per interface O2 the set may not narrow, so the repair
direction is to verify against the upstream set and fix whichever record disagrees.
*Test:* an equality test against the upstream set where it is importable, with the
count asserted, so drift of either side fails loudly.

## NOTE

### N1 — `assert_no_scoring_headers` cannot see setext headings, HTML table headers, or body rows; the safety property is held by renderer convention

`src/minireason/loop/standard.py:225–292`. The docstring scopes the scan itself
("every ATX Markdown heading, and the header row of every Markdown table"), and within
that scope my probes found no bypass: `## RANKING`, `| cell | score |`, a second
table's header after another table, and even a table inside a fenced code block (a
mild over-trigger) all refuse with `SCORING_KEY_FORBIDDEN`. Out of the named scope,
`probe/exhaustion_and_headers.py`:

```
setext heading with 'Scores': PASSED (no refusal)
HTML table header: PASSED (no refusal)
table body carrying word: PASSED (no refusal)   # declared: body rows are prose
```

G12's subject is "every emitted artifact, every table header and every rendered file";
a future renderer that emits a setext heading or an HTML table writes a header the
scan cannot see. The scanner is correct for this repository's Markdown spellings
today; a renderer adopting a new spelling must extend the scan in the same commit.

### N2 — the exhaustion scan's refusal detail quotes the flattened copy, not the record

`src/minireason/loop/standard.py:324–350`. Cosmetic: `e.detail` shows e.g.
`'exhausted'; a reached ceiling is a declared reso` — 24 chars of the *scanned*
string at the match offset, not a span of the original record. The refusal fires with
the right code in every probe, including the smuggle case (`probe/exhaustion_and_headers.py`:
"denial + real claim appended: refused -> RESOURCE_BOUNDARY_MISDESCRIBED"). If
receipts quote the detail, locating the passage in the record takes one extra step.

## Tried, and could not break

1. **Byte-stability and identity of the published object.** Suspected `STANDARD_BODY`
   might drift from a fresh `build_standard()` (import-time mutation, dict order), or
   that `READING_VOCABULARY` / `READING_BANNER` might be copies rather than the
   instrument's own objects. `probe/roundtrip.py`: `STANDARD_BODY ==
   build_standard(): True`; `STANDARD_BODY_SHA256 == sha256_hex(STANDARD_BODY): True`;
   `READING_VOCABULARY is ROOT_READING_VOCABULARY: True`; `READING_BANNER is
   USE_RELATION_BANNER: True`; `REGISTERS is REGISTER_IDS: True`; str-form and
   bytes-form of `standard_body` agree. The `tuple()`-identity comment is accurate.

2. **The integer oracle.** Suspected a stray integer outside `guard_parameters` /
   `role_contracts.word_limits` (notably from the role schemas). Full enumeration
   (`probe/int_oracle.py`, prefix test corrected in `probe/secondary.py`) found exactly
   12 integers, all inside the two admitted sections: `integers outside the two
   admitted sections: NONE`. Riding the schemas as a digest (deviation 6) does keep
   the oracle exact.

3. **The exhaustion-scan smuggle direction.** The docstring claims removing the
   whitespace-insensitive denial re-exposes any claim built around it. Probes ran the
   denial alone (rewrapped across lines, sentence-cased — admitted, as designed), the
   denial plus a real claim appended, a plain "context window was exhausted" claim,
   and the `exhaustive` / `exhausted` stems. Every real claim refused with
   `RESOURCE_BOUNDARY_MISDESCRIBED`; every denial spelling passed. The exemption is
   not a hole.

4. **Ceiling clause 7 ↔ `types.CEILING_BLOCK_REASONS` ↔ `BLOCK_CODES`.** Suspected
   drift of one code between the frozen ceiling bytes and the types tables.
   `probe/secondary.py` extracted the nine back-quoted codes from the shipped ceiling
   clause: `sets equal: True` against `CEILING_BLOCK_REASONS`, and all nine
   `blocked:<code>` forms are in `BLOCK_CODES`.

5. **Boundary and type values of every integer and boolean guard parameter.**
   `judge_seats=1`, `judge_seats=True`, `paraphrase_n=2.0`, `paraphrase_n=9`,
   `min_judge_families=1` while `judge_seats=2`, a string `order_swap_both_orders`,
   an int `marker_reuses_judge_seats` — all refused with `GUARD_PARAMETER_INVALID`
   (`probe/guard_params.py`). The bool-is-an-int trap is closed explicitly. The only
   un-refused inputs in this family are the type holes of SF1.

6. **Vocabulary closing on all four sides.** Narrowed, extended (seventh token),
   duplicated, and `unresolved`-less vocabularies each refuse with the matching
   declared code (`probe/guard_params2.py`). A bare string (`vocabulary="retains"`)
   is refused as `VOCABULARY_NOT_CLOSED`, with detail listing its characters — a
   string is a sequence of characters; declared, terse, and it will puzzle a reader of
   the detail for a minute, but it is a refusal with the right code.

7. **Register-set refusals.** A swapped id, a non-`Register` value, a blank
   `plan_text`, and empty/duplicated kind tuples each refuse with the matching code
   (blank `plan_text` shown: `empty plan_text register: refused -> REGISTER_TEXT_EMPTY`,
   `probe/guard_params2.py`).
