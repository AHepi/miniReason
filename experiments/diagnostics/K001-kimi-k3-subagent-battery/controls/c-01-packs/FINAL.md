# W2-PACKS — `src/minireason/loop/packs.py`

Two files written, both inside the sandbox:

* `src/minireason/loop/packs.py` (1457 lines)
* `tests/loop/test_packs.py` (831 lines)

Nothing under `src/` was edited; `packs.py` did not exist and is the only file
created there. `src/minireason/loop/types.py` was not touched.

Command and its result, together:

```
python3 run_tests.py tests.loop.test_packs
Ran 61 tests in 0.220s
OK
```

`python3 run_tests.py` (full sandbox discovery) reports the same 61 tests OK;
`test_packs` is the only test module the sandbox carries.

---

## 1. The acceptance clauses, and how each is tested

The wave-plan acceptance list has five clauses. Each has a test class named
after it, in the house style of `docs/examples/test_custody_example.py`.

### "Identical inputs give identical bytes"

**Satisfied.** Every renderer is a pure function of its arguments: no clock, no
environment, no randomness, no file read, no write, no provider call. The one
ordering that could have been unstable — the precedent slice — is taken over the
harness's registration order, which the replayed log fixes.

`IdenticalInputsGiveIdenticalBytes` renders one pack of every role twice and
asserts `pack.encoded`, dataclass equality and `pack_sha` all agree
(`test_identical_inputs_give_identical_bytes`), and asserts the converse — that a
changed surface, a dropped framing, a different seal and a swapped presentation
order each change the bytes and the sha
(`test_a_changed_input_changes_the_bytes_and_the_sha`,
`test_a_marker_packs_sha_moves_with_the_seal_and_the_presentation_order`). It
also pins that the material section is the surface's own bytes unaltered,
including a non-ASCII em dash
(`test_the_rendered_material_is_the_surfaces_own_bytes_unaltered`), that a
standard given as bytes, as text or as a mapping renders one pack
(`test_a_standard_given_as_bytes_or_as_a_mapping_renders_the_same_pack`), and
that rendering mutates nothing it was handed
(`test_rendering_mutates_nothing_it_was_handed`). Byte stability across
*processes* was checked separately: three fresh `python3` invocations print the
same five pack shas.

### "no pack contains a label, att, dep, status, another cell's outcome or another seat's output"

**Satisfied, and enforced structurally rather than by a token scan.** A token
scan is impossible here and it is worth saying why: the frozen rubric's clause R8
reads "No reading of any value mints an `att` or a `dep` on any node under
study", and the instrument's banner reads "it has no `att`, no `dep`, no status
and no label". A pack that carries the pinned standard therefore carries those
words, and a scan that banned them would delete the sentences that state the
rule — exactly the collision W0-STANDARD already had to settle for the token
"exhaustion". So the guarantee is made three other ways:

1. **A closed section vocabulary.** `SECTION_IDS` is a closed tuple and
   `ROLE_SECTIONS` says which of them each role admits, in order. `_pack` is the
   only constructor and refuses any id that is not declared, any section the role
   does not admit, and any reordering. There is no section for a label, an edge,
   a status or an outcome, so there is nowhere for one to ride.
   (`test_the_section_vocabulary_is_closed_and_names_no_label_edge_or_status`,
   `test_a_pack_cannot_be_given_a_section_its_role_does_not_admit`.)
2. **Closed input key sets.** `framing` may carry only the four published
   `UseRow` columns §2.3 names (`FRAMING_KEYS`); `cell` may carry only
   `CELL_KEYS`. Anything else is refused, not dropped — tested by smuggling
   `status`, `label`, `att`, `dep`, `root_reading`, `outcome`, `cell_state` and
   `other_seat_ruling` into the framing and `marks`/`status`/`outcome`/`baseline`
   into the cell (`test_a_framing_key_outside_the_closed_set_is_refused_not_dropped`,
   `test_a_cell_key_outside_the_closed_set_is_refused`). A role output carrying
   an undeclared field is refused by the W0 schema through `PACK_OUTPUT_INVALID`
   (`test_a_role_output_carrying_an_undeclared_field_is_refused`).
3. **Content assertions where content is this module's own.** No pack's text
   carries any member of the vendored `Status` enum
   (`test_no_pack_carries_a_status_token_anywhere_in_its_text`); no pack record
   has a key naming a label, an edge, a status or an outcome
   (`test_no_pack_record_carries_a_label_an_edge_a_status_or_an_outcome`); a
   marker pack shows one register's definition, one register's token set and only
   the two sides its comparison names, with the other two arms of the cell absent
   (`test_a_marker_pack_shows_one_register_and_only_the_two_sides_named`); a
   variator pack carries the exchange and never the material
   (`test_the_variator_is_shown_the_exchange_and_never_the_material`); a defender
   pack carries the material and the case and not the answer
   (`test_the_defender_is_shown_the_material_and_the_case_and_nothing_else`); and
   one judge seat's pack cannot carry another seat's answer
   (`test_one_judge_seats_pack_cannot_carry_another_seats_answer`,
   `test_a_judge_pack_carries_no_second_seats_ruling_and_no_ruling_field`).

**This clause found one real defect in my first draft, and the module changed.**
The pinned `MARKER_SCHEMA` closes `difference_kind` over the seven-token union
(`ALL_DIFFERENCE_KINDS`), because a schema does not know which register was
asked. Rendering it showed a register-T marker the tokens of registers E, D and
G — the one thing §2.3 says a marker call may not see — and it offered tokens
that `contracts.check(..., register=)` then refuses (O11), so a seat could be
blocked with `blocked:schema` for answering with a token the pack put in front of
it. The marker pack now renders a copy of the pinned schema with that one enum
narrowed to `difference_kinds_for(register)`; the pinned schema and the digest
the standard body carries for it are untouched. Tested both ways in
`test_a_marker_is_offered_exactly_the_tokens_its_register_admits`.

### "the lexical-overlap banner is present verbatim"

**Satisfied.** The banner section's body is the banner and nothing else — no
re-wrapping, no truncation, no heading inside it. It is taken off the *pinned
standard body*, which took it from `use_relation_h005.USE_RELATION_BANNER` by
import, so it cannot drift and is not retyped anywhere in this module.
`TheLexicalOverlapBannerIsPresentVerbatim` asserts `pack.section("banner").body
== READING_BANNER` and `READING_BANNER in pack.text` for the critic pack and the
judge pack, asserts `READING_BANNER is USE_RELATION_BANNER` (identity, not
equality), and asserts that the sentence "A lexical overlap is not evidence of
use" does not occur in `packs.py`'s source at all.

### "a register pack without baseline_sha raises BaselineNotFirst"

**Satisfied.** `render_register` checks the seal **first**, before the standard,
the register, the cell or the comparison, so a malformed everything-else cannot
steal the failure. `None` and `""` raise; so does a non-string, an uppercase hex
string, a 63- or 65-character string, an integer, a bytes object and `True`. The
sealed digest rides in the BASELINE section and in the pack record, therefore in
`pack_sha` — which is what makes revising a sealed baseline change a hash that
already-published call records carry.
(`ARegisterPackWithoutBaselineShaRaisesBaselineNotFirst`, six tests, including
`test_the_seal_is_refused_before_anything_else_is_looked_at` and
`test_a_sealed_baseline_rides_in_the_pack_and_therefore_in_its_sha`.)

### "the precedent query text is recorded with the pack and ranks appellate rulings first"

**Satisfied, with one deliberate reading of "recorded with".**
`precedent_slice` returns a `PrecedentSlice` — a real `list`, so the wave plan's
`-> list` holds — carrying `.query`, the deterministic query text, **including
when the slice is empty**, which is the one case where the query text is the only
evidence the question was asked at all. `render_exchange` records it on
`Pack.precedent_query` and refuses a non-empty precedent sequence that arrives
without it (`PRECEDENT_QUERY_MISSING`).

The query text is recorded *with* the pack and is deliberately **not rendered
into** it: the query names `accepted` as its selection predicate, and §2.3 says a
pack never contains a status. `test_the_precedent_query_text_is_recorded_with_the_pack`
asserts both halves — the query is on the record and equals
`precedent_query(standard_id, k)`, and neither it nor the token `accepted`
appears in the prompt.

Ordering is `(appellate first, then registration order)`, asserted against a real
`Harness` in a temporary directory where an appellate ruling is registered
*after* two plain readings and still comes first
(`test_the_precedent_query_ranks_appellate_rulings_first`), survives the bound
`k=1` (`test_the_slice_is_bounded_by_k_and_keeps_the_appellate_ruling`), and is
deterministic across two calls (`test_the_slice_is_a_list_and_is_deterministic`).
The slice reads the harness and writes nothing to it — the log bytes and the blob
listing are unchanged after the call
(`test_precedent_slice_reads_the_harness_and_writes_nothing_to_it`).

**On the word "ranks".** This is a presentation order over precedent, fixed by
the standard's own case-law rule: an appellate ruling is precedent *about* the
standard, so it is shown before precedent that merely applied the standard.
Nothing is scored, nothing is compared for quality, and no two seats, arms,
endpoints, model families or modules are ordered against each other anywhere in
this module.

### Supporting coverage beyond the five clauses

`DeclaredCodes` scans the module source and asserts `NEW_CODES` is exactly the
set of codes the module can emit, in both directions, sorted, disjoint from
`types.FAILURE_CODES`, with `BASELINE_NOT_FIRST` correctly *excluded* because
wave 0 already declared it. `ThePublicInterfaceOfTheWavePlanEntry` asserts every
wave-plan name is exported and every exported name exists, that every role the
standard names has a pack, and that each renderer refuses what it cannot render.
`TheGuardsEveryPackIsPutThrough` re-runs G12 over every pack's record keys and
over its headings, re-runs the exhaustion scan, and asserts no pack record field
outside `sections`/`text` is a number — no pack carries a count of anything.

---

## 2. What I implemented as a stub, and why

**Nothing.** Every name in the wave-plan public interface —
`render_row`, `render_exchange`, `render_register`,
`render_paraphrase_request`, `precedent_slice`, `pack_sha`, `BaselineNotFirst`
— is implemented and exercised by a test. There is no `NotImplementedError`, no
`pass` body and no placeholder return in the module.

Two things are *implemented but rest on a convention I had to declare*, because
the module that will write those records is in a wave I could not read (W1-GRAPH
is not in this sandbox and is not a declared dependency of W2-PACKS). They are
not stubs — they work, and a test exercises each against a real harness — but a
W1-GRAPH author could reasonably have chosen a different spelling:

* how an artifact declares that it is an **appellate ruling**
  (`provenance.school == "appellate"`), and
* the shape of the **cell** a marker pack is rendered from
  (`{"cell_key", "case", "sides"}`).

Both are in §3 below with what would change if the decision went the other way.

---

## 3. Questions the design entry, the wave-0 interface and the wave-1 decisions did not settle

### D1. Four renderers, five roles — where does the defender's pack come from?

The wave plan names `render_row`, `render_exchange`, `render_register` and
`render_paraphrase_request`, and §2.3 specifies five packs. Nothing says which
renderer builds the defender's.

**Decided:** `render_exchange(pack, critic, defender=None)`. With `defender`
absent it renders the **defender's** pack (§2.3: "pack: `M`, the critic's case");
with it present, the **judge's**. The wave plan's positional signature is
preserved exactly.

**If it went the other way** — a fifth renderer, say `render_case(pack, critic)`
— the public interface would gain a name the wave plan does not list, and
W3-TRIAL would call three renderers per trial instead of two. No pack bytes would
change; the section lists are the same either way.

### D2. How does the precedent slice reach the judge pack?

`render_exchange(pack, critic, defender)` has no harness parameter and
`precedent_slice(harness, standard_id, k)` is a separate public callable.

**Decided:** a keyword-only `precedent=` argument on `render_exchange`. A
renderer that reached into a harness itself would read a mutable graph at render
time and stop being a pure function of its arguments — which would break the
first acceptance clause, not just tidiness.

**If it went the other way** — `render_exchange(pack, critic, defender, harness,
standard_id, k)` — the renderer would no longer be byte-stable for a fixed
argument tuple, `pack_sha` would depend on when the call happened, and the
acceptance clause "identical inputs give identical bytes" would have to be
restated as "identical inputs and identical graph state".

### D3. Is the precedent query text rendered into the pack, or only recorded beside it?

The acceptance clause says "recorded with the pack" and does not say where.

**Decided:** recorded on `Pack.precedent_query` (and in `pack.as_dict()`), not
rendered into the prompt — because the query's selection predicate is a status
and §2.3 forbids a status in a pack.

**If it went the other way** — rendering the query into a PRECEDENT section
header — the judge would see the selection rule, which is arguably better
disclosure, at the cost of a status token in a prompt. The test
`test_the_precedent_query_text_is_recorded_with_the_pack` asserts the token is
absent; it is the test that would have to change, and so would the "no pack
contains a status" clause's scope.

### D4. What makes an artifact an appellate ruling?

The design says appellate rulings are ranked first. Neither the wave-0 interface
nor the wave-1 decisions say how one is recognised, and W1-GRAPH's
`apply_appeal(harness, ruling)` is not in this sandbox.

**Decided:** `provenance.school == APPELLATE_SCHOOL` (`"appellate"`). The
vendored `Provenance.school` docstring says the field "may shape packs and
scheduling, never adjudication" — this is precisely that use and no other, and it
keeps the appellate flag out of adjudication, which is where it must not be.

**If it went the other way** — a key in the artifact's JSON content, a ref role,
a dedicated commitment, or a W1-GRAPH-owned registry — `_is_appellate` is a
three-line function and `APPELLATE_SCHOOL` is one constant; the change is
localised, the ordering key and every test around it are unchanged, and the
fixture in `_Graph.reading(..., school=...)` is the only test-side edit. I
recommend W1-GRAPH's author either adopt this or tell the integrator, because
this is the kind of divergence that shows up as an empty precedent slice rather
than as an error.

### D5. What is "precedent citing this standard"?

The vendored `warrant.py` says "the nu of any rubric-derived warrant must carry a
mention ref to the standard it applied". That is the *validity node*, not the
reading.

**Decided:** any artifact whose `interface.refs` names the standard id, under any
`RefRole`, and whose adjudicated status is `accepted`, excluding the standard
itself. Accepting every ref role rather than `MENTION` alone means a reading that
depends on the standard is also precedent; narrowing it would have made the query
depend on a role convention W1-GRAPH has not published.

**If it went the other way** — `RefRole.MENTION` only, or "the artifact carrying
the warrant whose nu mentions the standard" — the slice would hold validity nodes
rather than readings, and `Precedent.text` would render a nu's content instead of
a reading's. `_cites` is the only function that changes.

### D6. What is the ordering *within* appellate and within non-appellate precedent?

"top-K" implies an order the design does not state.

**Decided:** registration order, which is deterministic under replay (W1-GRAPH's
own acceptance says "with a deterministic clock the log replays byte-identically")
and is the order the loop actually learned the precedent in.

**If it went the other way** — content-address order — the slice would still be
deterministic but the "top" of "top-K" would be an arbitrary hash order rather
than a chronological one. One `sort` key changes.

### D7. What is a `cell`, and what is a `comparison`?

`render_register(cell, register, comparison, baseline_sha, standard)` names
neither shape, and W2-MARKPREP (which produces them) is a sibling module in the
same wave.

**Decided:** `cell` is a mapping closed over `{"cell_key", "case", "sides"}`
where `sides` maps an arm label to that arm's commitment surface verbatim;
`comparison` is a pair of distinct side names, left first. The two sides render
as **SIDE LEFT** and **SIDE RIGHT** with their arm labels withheld, which is what
makes §2.4 G6's order-swap a real second pack with a second sha; which arm was on
which side is in the pack record, not in the prompt.

**If it went the other way** — a typed `Cell` object from W2-MARKPREP, or
`comparison` as a falsifier id (`"D1"`) rather than an arm pair — `_mapping`
already accepts any object with `as_dict()`, so a typed cell works today provided
its dict has those three keys; a falsifier id would need a lookup from
`standard.FALSIFIER_MAP[fid].comparison`, which is four lines and no change to
the rendered bytes.

### D8. Does this module render a within-ORIGINAL baseline pack?

G8 forbids a *cross-case* pack before the seal and says nothing about a
within-arm one.

**Decided:** no. `comparison` must name two distinct sides, and every
`render_register` call requires a sealed digest. The within-ORIGINAL grid is
W2-MARKPREP's `write_baseline`, computed by program before any call (G10), so
there is no model call to render a pack for.

**If it went the other way** — a marker call inside the baseline construction —
the seal could not be required for that pack (it does not exist yet), and G8's
"any cross-case pack" would have to be discriminated at render time by comparing
the two sides' arm labels. That is a weaker guard: it would be satisfiable by
mislabelling an arm.

### D9. Does the judge pack carry the vocabulary, the banner and the row framing?

§2.3 lists the judge pack as "rubric body, `M`, case, answer, and the precedent
slice" — no vocabulary, no banner, no framing.

**Decided:** it carries them, as the *same section objects* the row pack carries
(a test asserts object identity, not equality), so the judge rules on
byte-identical material under byte-identical framing to what the critic read.
Withholding the banner from the judge would mean the seat asked to check whether
a lexical overlap was mistaken for use is the one seat not shown the rule about
it.

**If it went the other way** — the judge pack trimmed to §2.3's five items — the
judge's prompt shrinks by about 3 KB, `ROLE_SECTIONS["judge"]` loses three
entries, and the banner acceptance clause narrows to the critic pack alone.
Nothing else changes.

### D10. Is the defender shown the framing?

**Decided:** no — §2.3 says "pack: `M`, the critic's case", and I followed it
literally here while deviating in D9. The asymmetry is deliberate and I record it
as an asymmetry: the judge is checking a reading and needs the rule; the defender
is arguing the null and the design gives it the material and the case.

### D11. What does `pack_sha` address — the prompt, or the pack?

**Decided:** the whole pack record (`canonical_json(pack.as_dict())`, the one
digest path wave-0 integration decision 7 fixes), so two packs whose prompts
agree but whose sealed baseline or precedent selection differs are two packs with
two shas.

**If it went the other way** — sha over `pack.encoded` alone — a re-sealed
baseline would still change the sha (the digest is printed in the BASELINE
section), but a changed precedent *query* with an unchanged precedent *list*
would not, and neither would a changed `comparison` record on a pack whose two
side bodies happened to be equal.

### D12. `NEW_CODES` as a tuple or as a mapping?

The task says `NEW_CODES: tuple[str, ...]`; W1-SURFACE shipped a
`Mapping[str, str]` under the same name. **Decided:** follow the task — a sorted
`tuple[str, ...]` — and carry the prose separately in
`NEW_CODE_REASONS: Mapping[str, str]`, so the integrator gets both the token list
the task asked for and the one-line reason each code will be filed under. If the
integrator prefers W1-SURFACE's spelling, `NEW_CODE_REASONS` is already exactly
that object and `NEW_CODES` becomes `tuple(sorted(NEW_CODE_REASONS))`.

---

## 4. The new failure codes, and which table each belongs in

All thirteen belong in **`types.FAILURE_CODES`**, in a group commented
`# pack rendering (loop/packs.py, W2-PACKS)`, exactly as wave-1 integration
decision 6 requires for every wave-1 module's `NEW_CODES`, and as O9 requires
("every later wave adds its own codes to `types.FAILURE_CODES` in the same commit
that raises them"). The exception class to add to
`tests/loop/test_types.py::TheCodeTablesAreComplete`'s `TOKEN_ARGUMENT` is
**`PackInvalid`** — every code below is raised through `packs._refuse(...)`,
which constructs a `PackInvalid`, and a test in `test_packs.py` scans the source
and fails if the two lists disagree.

| code | what it refuses |
|---|---|
| `PACK_CELL_INVALID` | a cell that is not a mapping, carries a key outside `CELL_KEYS`, or declares no side |
| `PACK_COMPARISON_INVALID` | a comparison that is not two distinct sides the cell declares |
| `PACK_EXCHANGE_INVALID` | a paraphrase request that is not an exchange, or a pack carrying half of one |
| `PACK_FRAMING_INVALID` | a framing that is not a mapping, or carries a key outside `FRAMING_KEYS` |
| `PACK_OUTPUT_INVALID` | a role output that is neither the contracts record nor a mapping that validates as one |
| `PACK_REGISTER_UNKNOWN` | a register the pinned standard does not carry |
| `PACK_ROLE_UNKNOWN` | a pack asked for a role no role contract names |
| `PACK_SECTION_UNKNOWN` | a section id undeclared, repeated, out of order, or not admitted by the role |
| `PACK_STANDARD_INVALID` | a standard that is not bytes, text or a mapping of the `std:reading-rubric/v1` body |
| `PACK_SURFACE_INVALID` | a `render_row` argument that is not a `surface.Surface` |
| `PRECEDENT_CONTENT_UNREADABLE` | a selected precedent whose content does not read back as utf-8 text |
| `PRECEDENT_QUERY_MISSING` | a non-empty precedent sequence arriving without the query text that produced it |
| `PRECEDENT_SLICE_INVALID` | no standard id, a bound that is not a whole number, or no materialised harness state |

**No block code is added.** `BLOCK_CODES` is unchanged: this module renders and
refuses; it does not block a cell.

**`BASELINE_NOT_FIRST` is not new.** `types.FAILURE_CODES` already carries it
(line 388 of `src/minireason/loop/types.py`), so `BaselineNotFirst` needs no
table edit — only the `TOKEN_ARGUMENT` entry above, since it is a `PackInvalid`
subclass with a fixed code and takes `(detail="")` rather than `(code, detail)`,
following W0-PUBLISH's precedent for single-code refusals.

---

## What I could not determine

* **Whether W1-GRAPH will spell an appellate ruling the way I did.** W1-GRAPH is
  not in this sandbox and `apply_appeal` is the function that would say. I chose
  `provenance.school == "appellate"` on the strength of the vendored field's own
  docstring ("may shape packs and scheduling, never adjudication"), and I could
  not check it against the module that writes the record. If W1-GRAPH marks
  appeals another way, `precedent_slice` will return a correctly-ordered slice in
  which nothing is flagged appellate — a silent wrong answer, not an error. This
  is the single highest-risk assumption in the module and the integrator should
  reconcile it before W3-TRIAL runs. Unresolved.
* **Whether §2.3's "another cell's outcome" forbids the precedent slice itself.**
  §2.3 says a pack never contains another cell's outcome and, three lines later,
  puts the precedent slice — readings of other cells — into the judge's pack. I
  could not settle the tension from the text I was given. I read the prohibition
  as governing the cell under trial (its own label, status, edges; a sibling
  cell's outcome; another seat's output for the same coordinate), and read the
  precedent slice as the explicit exception the same section grants, rendered
  without any status, label, edge or `sustained` value. If the prohibition is
  meant absolutely, the judge pack loses its PRECEDENT section and the fifth
  acceptance clause becomes unsatisfiable as written. I could not determine which
  reading was intended and have recorded both.
* **What the C001 cell and its `sides` actually look like on the wire.**
  W2-MARKPREP is a sibling in the same wave and its `program_marks(cell)` /
  `write_baseline(cell, replicates, out_dir)` are the producers. I declared a
  shape (D7) and made it accept any object with `as_dict()`, but I could not
  check it against the module that builds one. If the shapes disagree, the
  failure is loud (`PACK_CELL_INVALID` names the offending key), not silent.
* **Whether the pack text I authored reads well to a model.** The instructions,
  the section headings and the framing rendering are mine, and I have tested that
  they are deterministic, that they carry nothing forbidden and that they pass
  G12 and the exhaustion scan. I have not tested — and offline, with no provider
  call, could not test — whether a seat actually answers them well. That is
  W3-TRIAL's and W6-DRYRUN's evidence to produce, not mine to assert.
* **The wave-0 code-table edit itself.** I was instructed not to edit
  `src/minireason/loop/types.py` in this sandbox, so `types.FAILURE_CODES` does
  not yet carry the thirteen codes above and
  `tests/loop/test_types.py::TheCodeTablesAreComplete` is not present here to
  run against. I could not verify that the scan accepts them; §4 states exactly
  what the integrator has to add.
* **Anything about the other wave-2 modules.** `roles.py`, `markprep.py` and
  `decide.py` were not in the sandbox and I did not design against them beyond
  the interfaces the wave plan prints. In particular I did not check that
  W2-ROLES' "every record carries ... pack sha" means `pack_sha` as I defined it
  (D11) rather than a digest of the prompt bytes alone.
* **Line and test counts are counts.** "61 tests OK" is what
  `python3 run_tests.py tests.loop.test_packs` printed, quoted beside the command
  that produced it. It is information about what ran, not a warrant that the
  module is right.
