# W2-MARKPREP — `src/minireason/loop/markprep.py`

Written: `src/minireason/loop/markprep.py` (1217 lines) and
`tests/loop/test_markprep.py` (741 lines), both inside the sandbox. No other file was
created or changed; nothing under `src/` other than the new module was touched.

    python3 run_tests.py tests.loop.test_markprep
    Ran 56 tests in 0.129s
    OK

(56 is what that command printed; it is the number of test methods that ran, and it is
information about the run, not a warrant for anything.)

The module imports only `minireason.loop.{types,standard,contracts,custody}` and the
standard library. No provider, no socket, no environment variable, no wall clock, no RNG.
It writes exactly one file — the baseline — under the directory it is handed.

---

## New failure codes, and the table each belongs in

`src/minireason/loop/types.py` may not be edited in this sandbox, so the codes are
declared at the top of the module as `NEW_CODES`:

| code | table it belongs in |
|---|---|
| `BASELINE_ALREADY_SEALED` | `types.FAILURE_CODES` |
| `BASELINE_REPLICATE_UNKNOWN` | `types.FAILURE_CODES` |
| `CELL_MALFORMED` | `types.FAILURE_CODES` |

All three are `FAILURE_CODES` and none belongs in `BLOCK_CODES`, `STOP_REASONS` or
`STEP_KINDS`: none of them is a blocked reading of the material — each is the machinery
refusing to proceed, which is exactly what `FAILURE_CODES` names. Per wave-1 decision 6
they go into `types.FAILURE_CODES` in the same commit that raises them, and the scan in
`tests/loop/test_types.py::TheCodeTablesAreComplete` extends by adding `MarkPrepError` to
its `TOKEN_ARGUMENT` table (O9's recipe).

`BASELINE_NOT_FIRST` is also raised here and is deliberately **not** in `NEW_CODES`: wave
0 already carries it in `types.FAILURE_CODES`. G8 is one refusal with one name whether
W2-PACKS or W2-MARKPREP reaches it; this module raises it through its own
`BaselineNotFirst(MarkPrepError)` class, W2-PACKS through its own. Two classes, one code.
`tests/loop/test_markprep.py::DeclaredCodesAndTheImportedVocabularies::test_every_code_the_module_can_raise_is_declared`
scans the module source for raised codes and asserts every one is either in `NEW_CODES`
or already in `types.FAILURE_CODES`, and that the two sets are disjoint.

---

## Acceptance clauses: what is satisfied and how it is tested

Every clause has a test class named after it.

**1. "Baseline is written and sealed before any residue is offered for marking."**
Satisfied. `residue`, `program_marks` and `baseline_kinds` all go through `_sealed()` and
raise `BaselineNotFirst` (`BASELINE_NOT_FIRST`) on an unsealed cell; `write_baseline`
writes the grid through `custody.write_new` (write-once, credential-scanned) at a path
put through `custody.fenced`, and seals the cell with the sha256 of the bytes it wrote.
Every residue row and every program mark carries `baseline_sha256`.
Tested by `BaselineIsSealedBeforeAnyResidueIsOffered`:
`test_baseline_is_written_and_sealed_before_any_residue_is_offered` (all three callables
refuse before the seal, then residue appears and every row carries the sha),
`test_the_seal_is_the_sha_of_the_bytes_on_disk` (`custody.sha256_path(file) == returned
sha`; exactly one file in the directory; the record carries the plan §8a source and the
order-of-reading text), `test_every_program_mark_also_carries_the_seal`,
`test_a_baseline_path_may_not_escape_the_directory_it_is_given`.

**2. "A bare id token shared with the account document is forced unresolved and never
appears in the residue."**
Satisfied. The shared set is parsed out of the mirrored PLAN §8a text for register E
(`o1 c1 c2 p1 u1`), never retyped. A bare token in that set on either side makes the E
row a program mark of `unresolved` with reason `bare-token-shared-with-account`, and that
row is absent from the residue.
Tested by `ABareTokenSharedWithTheAccountIsForcedUnresolved`:
`test_a_bare_shared_id_token_is_forced_unresolved_and_never_differs` (mark is
`unresolved`, is asserted not to be `differs`, the note names the token, the row is not in
the residue), `test_the_forced_row_never_appears_in_the_residue`,
`test_register_e_reaches_the_residue_when_no_shared_token_appears` (the contrast case),
`test_a_prefix_qualified_reference_and_its_bare_form_read_the_same` (prefix resolution:
`o2` bare and `OBJ#o2` read as one record),
`test_a_shared_bare_token_inside_original_leaves_the_baseline_absent` and
`test_one_spoiled_replicate_does_not_blind_the_whole_baseline` (the token's effect on the
baseline grid), `test_a_bare_token_with_no_declared_objection_address_is_residue`.

**3. "T and D are program-computed wherever the FCL parse succeeds and the residue names
exactly the rows it could not."**
Satisfied. On the FCL arm, where both sides parse, T and D are marked by program with no
seat called. `program_marks` and `residue` are computed by one walk (`_settle`) and
partition the cell's rows.
Tested by `TAndDAreProgramComputedAndTheResidueNamesTheRest`:
`test_t_and_d_are_program_computed_wherever_the_fcl_parse_succeeds`,
`test_the_residue_names_exactly_the_rows_the_program_could_not_settle` (asserts
`set(marks) | set(residue)` equals the declared row set and `set(marks) & set(residue)` is
empty, and that an unparseable D row names the side it could not read),
`test_the_prose_arm_is_never_program_marked`,
`test_g_is_read_on_the_trial_arm_and_never_program_marked`,
`test_a_spread_inside_one_case_is_carried_into_the_comparison`,
`test_a_comparison_the_cell_does_not_declare_is_not_a_row_at_all`.

**4. "Byte-identical ORIGINAL/CONTROL commitments record D1-not-exhibited before any
call."**
Satisfied. `byte_identity_defeater` compares the sha256 of each case's resolved
commitment surfaces and, on identity, sets `finding: "D1-not-exhibited"`. It requires no
seal and no dispatch, so it is computable before anything at all.
Tested by `ByteIdenticalCommitmentsRecordD1NotExhibited`:
`test_byte_identical_commitments_record_d1_not_exhibited` (the finding token, the
falsifier id, the carrying registers T/E/D and the excluded register G, taken from
`standard.FALSIFIER_MAP`), `test_the_defeater_is_computed_before_any_call_and_before_the_seal`
(asserts the cell is unsealed and that nothing was written),
`test_a_cell_whose_sides_differ_records_no_finding`,
`test_two_sides_that_resolved_nothing_are_not_thereby_identical` (two empty sides are not
identical — absence is not identity), `test_a_cell_with_no_control_case_records_no_finding`.

**5. "Fewer than three resolved replicates of a case yields no residue for that case."**
Satisfied. The floor is `standard.GUARD_PARAMETERS["min_resolved_replicates_per_case"]`
(3), imported, not retyped. Every row of a comparison naming an under-replicated case is
a program mark of `unresolved` with reason `under-replicated` and is absent from the
residue; the note says "absent data", never an absence of difference.
Tested by `FewerThanThreeResolvedReplicatesYieldsNoResidue`:
`test_fewer_than_three_resolved_replicates_yields_no_residue_for_that_case` (the
under-replicated comparison contributes no residue row on any of the four registers while
a sibling comparison still does), `test_an_unresolved_replicate_does_not_count_towards_the_minimum`,
`test_an_under_replicated_original_leaves_the_whole_cell_unmarked`,
`test_the_written_baseline_says_when_original_is_under_replicated`.

**6. "Editing the baseline after sealing raises."**
Satisfied four ways: a second `write_baseline` raises `BASELINE_ALREADY_SEALED`; a direct
`Cell.seal` raises it; the sealed grid is a `MappingProxyType` inside a frozen dataclass,
so item assignment raises `TypeError` and attribute assignment raises
`FrozenInstanceError`; and the file itself is written through `custody.write_new`, so a
second write to the same path raises `WRITE_ONCE_VIOLATION`.
Tested by `EditingTheBaselineAfterSealingRaises`:
`test_editing_the_baseline_after_sealing_raises`, `test_the_sealed_grid_is_immutable`,
`test_editing_the_kind_set_a_caller_was_handed_changes_nothing`,
`test_the_baseline_file_is_written_once`, `test_write_baseline_needs_a_cell_it_can_seal_in_place`.

Supporting coverage beyond the six clauses: the replicate-baseline rule at kind grain
(`TheReplicateBaselineRuleAtKindGrain` — a kind already inside ORIGINAL is written `same`
with the forcing replicate pair recorded; a kind absent from the baseline stays `differs`
while the held-back kind is still recorded), the disposition/carrier-field distinction,
determinism (two builds byte-identical under `custody.encoded`), the G12 scan over every
emitted record, JSON-readiness, stable residue order, cell refusals by name, and the
identity assertions that no shared vocabulary was retyped
(`assertIs` against `standard.DIFFERENCE_KINDS`, `REGISTER_IDS`, `MARKS`, `FALSIFIER_MAP`).

---

## Stubs

**None.** All six callables of the published interface — `program_marks`,
`write_baseline`, `baseline_kinds`, `byte_identity_defeater`, `under_replicated`,
`residue` — are implemented and exercised.

What is deliberately *not* here, because the wave plan gives it to W4-MARKER, is: the
marker calls themselves, the mandatory order-swap on each pairwise trial (G6), and the
falsifier evaluation `falsifiers(marks, program_findings)`. This module produces the two
inputs that evaluation needs — the program marks and the byte-identity finding — and
stops. It also does not render packs (W2-PACKS) and does not decide anything (W2-DECIDE).

---

## Where the design entry, the wave-0 interface and the wave-1 decisions did not settle a
## question

Each entry: what was open, what I decided, and what changes if the decision goes the
other way.

**1. The shape of `cell`.** Nothing in the design entry, `notes/WAVE0-INTERFACE.md` or
`notes/WAVE1-INTEGRATION-DECISIONS.md` defines it; W1-GRAPH's `open_cells(harness, keys)`
takes only keys. *Decided:* this module publishes `Cell` / `Case` / `Replicate` frozen
records with `Cell.from_mapping`, so a caller may hand a JSON-shaped mapping. A cell is
`{key, arm, cases: {CASE: {replicates: [{id, commitment, resolved}]}},
artifact_addresses}`. *If it goes the other way:* the four register readers
(`_read_targets`, `_read_engagements`, `_read_disposition`, `_read_grounds`) and
`Cell.from_mapping` are the only places that would change; the G10 ordering, the seal and
the residue/marks partition are independent of the surface spelling.

**2. `write_baseline(cell, replicates, out_dir)` — what `replicates` is.** The signature
passes replicates separately from the cell, which already holds ORIGINAL's. *Decided:*
`replicates` is the caller's declaration of which ORIGINAL replicates it resolved and
read; each must be a replicate the cell declares **as resolved**, none may be named twice,
and the declaration need not be exhaustive. Anything else is `BASELINE_REPLICATE_UNKNOWN`.
The grid records `baseline_replicates`, `resolved_replicates` and `declared_replicates`
side by side so the three can be compared later. *If it goes the other way* (the parameter
is the raw material rather than a checked declaration): the check disappears and a caller
could silently seal a baseline over replicates the cell does not carry.

**3. Where the seal lives.** `residue(cell)` takes only the cell, so the cell must know
its own seal. *Decided:* `Cell` is mutable in exactly one slot and `write_baseline` seals
it in place; `write_baseline` therefore refuses a bare mapping with `CELL_MALFORMED`
("it seals the cell in place, so it takes a Cell"). *If it goes the other way* (the seal
is a value the caller carries): every call becomes `residue(cell, baseline_sha)` and the
published signature changes.

**4. Whether byte identity pre-empts the marker calls.** G10 lists (b), (c) and (d) as
call pre-empts and (a) only as a finding that "stands in the falsifier evaluation".
*Decided:* byte identity is a **finding, not a pre-empt**. A byte-identical
ORIGINAL/CONTROL still produces rows; on the FCL arm the comparator reads no difference
and marks them `same` anyway, and E and G still reach the residue. *If it goes the other
way:* the ORIGINAL/CONTROL residue would be empty on a byte-identical cell, saving marker
calls on a comparison where no difference is readable — a real saving of a resource
boundary, at the cost of departing from G10's own division of labour.

**5. Whether E and G are program-marked.** The design entry names "register E prefix
resolution and bare-token forcing" and "registers T and D parsed on the FCL arm"; G10(d)
names only T and D as program-computed. *Decided:* E is program-**resolved** (prefixes
resolved, shared bare tokens forced to `unresolved`) but never program-**marked**; G is
neither. Both otherwise go to the residue, carrying the program's own reading notes in
`program_notes`. *If it goes the other way* (E's resolved record sets are also compared by
program): every FCL E row would leave the residue and `PROGRAM_REGISTERS` would gain "E";
the comparator for E is already written and used for the baseline, so the change is one
constant.

**6. How a case with several replicates is compared with another case.** Unsettled
anywhere. My first implementation collapsed a case to one value and called the row
unreadable when its replicates disagreed — which made the replicate baseline unusable,
since a within-ORIGINAL spread is the normal case. *Decided:* both sides stay sets of
replicates and a kind holds between two cases when it holds between **some** replicate of
one and **some** replicate of the other; the first pair carrying each kind is recorded in
`difference_replicate_pairs`. This is PLAN §8a read literally ("the difference root reads
between the two cases" against "at least one pair of replicates inside ORIGINAL"). *If it
goes the other way:* a case whose own replicates spread would be `unresolved` rather than
compared, and the replicate baseline would have far less to hold back.

**7. `baseline_kinds` for a register no replicate pair was readable on.** *Decided:*
`None`, not `()`. An empty kind set admits every `differs`; absent data must not be
spelled the same way as "no difference inside ORIGINAL". The `-> dict` in the published
interface is honoured; the values are `tuple[str, ...] | None`. *If it goes the other way:*
callers get a uniform tuple type and a register the program never read would silently
admit every `differs` the rubric's M5 exists to hold back.

**8. Disposition precedence among the five FCL fields.** PLAN §8a lists `type`, `uptake`,
`revises`, `withdraws` and "the `action` field" without saying which governs when two
disagree. *Decided:* the reverse of the plan's listed order — `action`, `withdraws`,
`revises`, `uptake`, `type` — so the explicit `action` field governs where present. *If it
goes the other way:* rows where two carrier fields disagree get a different
`disposition_value`; the alternative worth considering is to call such a record
unreadable and send the row to the residue rather than pick a winner.

**9. Which disposition a list-valued carrier field states.** *Decided:* `uptake`→`use`,
`revises`→`revise`, `withdraws`→`withdraw`, declared in one visible mapping
(`_CARRIER_DISPOSITION`) and asserted at import to be a subset of the disposition list
parsed from the plan text, so a change to the plan refuses the import rather than leaving
a stale copy. `action` and `type` carry their own token verbatim. *If it goes the other
way:* the mapping moves into the standard as data and this module imports it — which is
where I think it belongs if a successor standard is ever minted.

**10. Whether register G's grounds vocabulary is closed.** PLAN §8a names four sources
(objection, account, rival, none) in prose. *Decided:* **not** closed here. The program
compares the normalised `grounds` value; a value outside the four is compared, not
refused. G never produces a program mark anyway, so this only affects the baseline's G
kind set. *If it goes the other way:* an out-of-vocabulary grounds value becomes
unreadable and the G baseline goes absent for that cell.

**11. The arm tokens.** No wave-0 module publishes an arm vocabulary. *Decided:* `"fcl"`
and `"prose"` (`ARMS`), declared as this module's own spelling in the docstring. *If it
goes the other way:* one constant changes; this is the single most likely reconciliation
point with W1-SYNTHETIC and W5-DRIVER.

**12. The `artifact_addresses` role key.** PLAN §8a §7 says prefixes resolve against
`arms.<arm>.artifact_addresses` but the sandbox holds no such file. *Decided:* the cell
carries `{role: label}` and the role a bare, unshared record id resolves into is
`"objection"` (`OBJECTION_ROLE`). A bare token with no objection address declared is a
residue row, not a forced `unresolved`. *If it goes the other way:* the role key changes,
or resolution is handed to an importer function.

**13. A bare token that is not one of the objection document's records.** *Decided:*
unreadable (residue), not forced `unresolved`. Rubric M6's forcing is specifically about
the *shared* tokens; a token naming no objection record is something the program simply
could not resolve. *If it goes the other way:* those rows leave the residue as
`unresolved` and are never offered to a seat.

**14. A comparison whose cases the cell does not declare.** *Decided:* not a row at all —
neither a mark nor a residue entry. A cell not on F3's arm should not report a spurious
`unresolved` for ORIGINAL/CARRIER. A caller who wants the absence recorded declares the
case with zero replicates, and G10(b) then reports it as absent data. *If it goes the
other way:* every cell reports twelve rows and most cells carry eight `unresolved`
rows that mean only "this cell was not part of that comparison".

**15. Under-replication measured against what.** *Decided:* against the cell's own
resolved replicates, not against the ids named to `write_baseline`. *If it goes the other
way:* a caller could suppress residue by naming fewer replicates in the baseline.

**16. O11 (`contracts.check(role, raw, register=None)` falls back to the union).** The
recommendation is addressed to W2-MARKPREP: "always pass `register=`". *Decided:* this
module calls neither `check` nor `validate`. A program mark is not a `MarkerOutput`: it
carries the cell, the comparison, the replicate pair and the read values, and
`MARKER_SCHEMA` is closed (`additionalProperties: false`) and requires `left_quote` and
`right_quote` on a `differs` — quotes a program reading a JSON field does not have and
should not manufacture. The obligation to pass `register=` therefore lands on W4-MARKER,
which validates the seats' outputs. *If it goes the other way* (program marks are coerced
into `MarkerOutput`): the program would have to synthesise quotes out of field values,
which would put text into a record that no one wrote. I declined that.

**17. Wave-1 decision 8 (extend the `__init__.py` import graph to the later waves).**
I may not edit any file under `src/` other than the one I am creating, so the package
docstring does not yet name `markprep`. The line it should gain is:
`markprep → contracts/standard/custody` (and `types`, through `LoopError`).

**18. Wave-1 decision 7 (the wave-0 fixer's `assert_no_scoring_keys` now raises on
`str`/`bytes`).** Checked against this call site: the guard is only ever handed dicts and
lists here, never a rendered string, so the narrowing does not bite. The module emits no
rendered file, so `standard.assert_no_scoring_headers` has nothing to scan.

---

## What I could not determine

* **Whether the `cell` shape I published is the one W4-MARKER and W5-DRIVER will hand
  me.** I could not determine this and here is why: no file in the sandbox defines a
  C001 cell. `design/design-s7-wave-plan.md:27` gives the signature `program_marks(cell)`
  and nothing else; `notes/WAVE0-INTERFACE.md` defines no cell; W1-GRAPH's `open_cells`
  takes bare keys. I authored `Cell`/`Case`/`Replicate` and said so above. This is the
  largest single interface risk in the module, and it is unresolved until W4-MARKER
  exists.
* **Whether the FCL commitment surface really carries an `engages` field.** The frozen
  C001 material (`experiments/diagnostics/C001-contrast-triple/material.json`, pinned at
  `94edfe61…` in `src/minireason/loop/data/plan_8a_mirror.json`) is not in the sandbox,
  and `src/minireason/use_relation_h005.py:166` publishes the *importer's* ref fields as
  `("target", "depends", "mentions", "revises", "withdraws")` — no `engages`. Register E
  reads "which of the objection document's records the successor takes up, by
  prefix-qualified reference or by quotation", which is not obviously any one of those
  fields. I could not determine which field carries it, so I declared `engages` with an
  explicit two-form entry (`reference` / `quotation`) because the quotation form has no
  home in the importer's ref fields at all. If the real material spells it differently,
  `_read_engagements` is the one function that changes.
* **Whether the registers T and D are the right program registers for the *prose* arm's
  baseline.** On the prose arm this module reads nothing at all, so every register's
  baseline kind set is `None` and every row is residue. That is honest — prose is not
  parsed — but it means the prose arm gets no replicate baseline from the program, and
  I could not determine from the design who is supposed to write one. G8 says the
  baseline must exist and be sealed; it does exist and is sealed, and it records that it
  could read nothing. Whether W4-MARKER may admit a `differs` against a baseline whose
  kind set is absent is a question I have left to W4-MARKER and flagged in the residue
  row (`baseline_kinds: null`, reason `baseline-register-not-readable`).
* **Whether `BASELINE_NOT_FIRST` should be one code shared with W2-PACKS or two.** I
  read the design's `⇒ BASELINE_NOT_FIRST` (design-s2 §2.4 G8) as one refusal with one
  name and reused the wave-0 code. If the integrator wants the two refusal sites
  distinguished in a receipt, a second code is needed and `NEW_CODES` grows by one.
* **What I did not cover.** I did not run the wider loop test suite: the sandbox contains
  only `tests/__init__.py` and `tests/loop/__init__.py` beside the file I wrote, so
  `python3 run_tests.py` with no arguments discovers exactly this one module (it reported
  the same 56 tests). I therefore have no evidence about interactions with
  `tests/loop/test_{types,contracts,standard,custody}.py`, which are not in the sandbox.
  I did not edit `src/minireason/loop/types.py` or `__init__.py` — the task forbids it —
  so `NEW_CODES` is declared but not yet in `FAILURE_CODES`, and the package docstring's
  import graph does not yet name this module. Both are listed above as work for the
  integrator.
* **No count in this report is a warrant.** The 56 came from
  `python3 run_tests.py tests.loop.test_markprep`; the line counts came from
  `python3 -c` over the two files. They say how much ran, not how much holds.
