# W0-STANDARD — adversarial review of `src/minireason/loop/standard.py`

Read against `notes/WAVE0-INTERFACE.md`, `design/design-s2-roles-and-guard.md`
§§2.1–2.5, and `design/design-s7-wave-plan.md`'s W0-STANDARD acceptance clause.
Every finding below was executed. Probes are in `probe/`; each is run with
`python3 probe/<name>.py` from the sandbox root. Nothing under `src/` was edited.

Sandbox note: `tests/loop/` carries only an empty `__init__.py`
(`python3 run_tests.py` → `Ran 0 tests in 0.000s OK`;
`python3 run_tests.py tests.loop.test_standard` → `FAILED (errors=1)`), and
`contracts.py`, `custody.py`, `receipts.py`, `publish.py` and
`tools/contrast_triple_study.py` are absent. Claims that rest on those files are
recorded under "What I could not determine" rather than asserted here.

---

## BLOCKER

### B1. `build_standard` does not honour the arguments it takes: a successor body contradicts itself, and the contradiction *widens* G11's reopen list

**Where.** `src/minireason/loop/standard.py:1270–1344`; the specific lines that
read a module constant where the caller supplied an argument are 1304
(`"rubric"`), 1315 (`"marks"`), 1333 (`"reopen_reasons"`) and 1334
(`"role_contracts"`).

**What it contradicts.** `build_standard`'s own docstring, lines 1280–1282:

> `None` means "the module's own frozen default" for each argument, which is what
> the loop registers; a caller narrowing the vocabulary or the guard parameters
> is minting a successor standard and therefore a new `loop_plan_id`.

and the declaration on `REOPEN_REASONS`, lines 985–986:

> The pre-registered reasons a cell whose prior outcome was `unresolved` may be
> re-read at all (design §2.4 G11). Anything else is refused at the write.

and `assert_config_matches_standard`'s statement of the direction G11 permits,
lines 1070–1073:

> G11: the reopen list "is the only mechanical defence against retrying until
> something sticks", so a run may narrow it and may not widen it

Design §2.4 G11 itself: "A cell whose prior outcome was `unresolved` may not be
re-read unless the call record carries a `reopen_reason` from the pre-registered
list — *new material*, *repaired guard*, *appellate ruling*. **Enforced by
refusing the write**, not by a convention."

**Probe.** `python3 probe/p02_successor_body.py`, verbatim:

```
[vocabulary] argument                 = ('retains', 'unresolved')
[vocabulary] body.vocabulary.closed   = True
[vocabulary] body.vocabulary.values   = ['retains', 'unresolved']
[vocabulary] body.vocabulary.nominable= ['retains']
[vocabulary] body.rubric.relation.values = ['re-deploys', 'qualifies', 'rejects-with-reason', 'repairs', 'retains', 'unresolved']
[vocabulary] rubric R7 sentence still reads:
             R7. The vocabulary is closed to the six published values for this run, and the closing is
[vocabulary] refused? no - build_standard returned 22807 bytes

[reopen] params['reopen_reasons']             = ('appellate-ruling',)
[reopen] body.guard_parameters.reopen_reasons = ['appellate-ruling']
[reopen] body.reopen_reasons (top level)      = ['new-material', 'repaired-guard', 'appellate-ruling']
[reopen] the two sections agree               = False

[kinds] body.registers.T.difference_kinds = ['target_set_membership', 'target_prefix_source', 'target_arm']
[kinds] MARKER_SCHEMA enum (whose digest the body pins) = ['disposition_carrier_field', 'disposition_value', 'engagement_form', 'grounds_source', 'record_engaged', 'target_prefix_source', 'target_set_membership', None]
[kinds] body.role_contracts.schemas_sha256 unchanged = True
```

Three disagreements inside one pinned artifact:

* a successor that narrows the reopen list ships the **narrowed** list under
  `guard_parameters` and the **unnarrowed** list at top level — and
  `standard_body`'s own required-section list (line 1370) names `reopen_reasons`
  as a top-level section, so the section a consumer is guaranteed to find is the
  widened one. This is the one direction G11 forbids;
* a successor that narrows the vocabulary ships `vocabulary.values` with two
  values while `rubric.relation.values` still enumerates six and rubric clause
  R7 still says "closed to the six published values for this run";
* a successor that adds a `difference_kind` ships a register whose token set the
  pinned `role_contracts.schemas_sha256` does not cover — the marker schema a
  seat is held to still enumerates the old seven tokens, and the digest that is
  supposed to make "editing any byte of any schema change
  `STANDARD_BODY_SHA256`" (docstring lines 885–886) does not move.

**Repair.** Either build every section from the arguments — `"reopen_reasons":
list(params["reopen_reasons"])`, `rubric` values from `values`, the critic and
marker enums and `schemas_sha256` recomputed from the passed `vocabulary` and
`registers` — or, the smaller change and the one that matches "a revised rubric
is a successor artifact … never an edit": have `build_standard` refuse any
argument that is not the module default, raising `StandardInvalid` with
`VOCABULARY_NOT_CLOSED` / `GUARD_PARAMETER_INVALID` / `REGISTER_SET_MISMATCH`,
so that minting a successor is a source edit and a new digest rather than a call.

**Test that would hold it.** For each of the three arguments, build a narrowed
body and assert the body is internally consistent: parse it and assert
`body["reopen_reasons"] == body["guard_parameters"]["reopen_reasons"]`,
`body["rubric"]["relation"]["values"] == body["vocabulary"]["values"]`, and that
every token in every `body["registers"][r]["difference_kinds"]` appears in the
marker schema the body's `schemas_sha256` addresses. Under the refusal repair,
assert instead that each non-default argument raises the named code.

---

### B2. The frozen data files are loaded with no shape check: a short `ceiling_v1.md` publishes `CEILING_REQUIRED_SENTENCES = ()` and the claim ceiling disappears without a refusal

**Where.** `src/minireason/loop/standard.py:339–364` (`_DATA`,
`PLAN_8A_MIRROR`, `CEILING_TEXT`, `_CEILING_CLAUSES`, `CEILING_CLAIM_TEMPLATE`,
`CEILING_REQUIRED_SENTENCES`) and `715–732` (`_build_registers`).

**What it contradicts.** The module docstring's opening, lines 12–13:

> Nothing here reads anything, calls anything or decides anything: it is data
> plus the two pure functions that serialise and parse it.

deviation 3, lines 55–58:

> `CEILING_REQUIRED_SENTENCES` holds the eleven invariant clauses, each a single
> unwrapped paragraph.

`notes/WAVE0-INTERFACE.md` §2: "`CEILING_REQUIRED_SENTENCES: tuple[str, ...]
# the 11 invariant clauses (W3-REPORT imports this)"; §7: "Every wave-0
exception is a `types.LoopError` and keeps its original base." And W3-REPORT's
acceptance clause in `design/design-s7-wave-plan.md:32`: "every required ceiling
sentence appears verbatim in every table and in the closing record".

**Probe.** `python3 probe/p10_import_time_reads.py`, verbatim:

```
import-time file reads in standard.py:
   line 348: PLAN_8A_MIRROR_PATH.read_text(encoding="utf-8")
   line 351: CEILING_TEXT: Final[str] = CEILING_PATH.read_text(encoding="utf-8")
   line 352: CEILING_SHA256: Final[str] = sha256_hex(CEILING_PATH.read_bytes())

intact copy (control)                    imported
ceiling_v1.md absent                     FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-0/-hom
ceiling_v1.md truncated to one clause    imported
plan_8a_mirror.json missing register G   KeyError: 'G'
plan_8a_mirror.json truncated            JSONDecodeError: Expecting property name enclosed in double quotes: line 
plan_8a_mirror.json marks widened        imported

what a widened `marks` list does to the published mark vocabulary:
   MARKS                        = ('differs', 'same', 'unresolved', 'better')
   MARKER_SCHEMA mark enum      = ['differs', 'same', 'unresolved', 'better']
   body.marks                   = ['differs', 'same', 'unresolved', 'better']
   'better' is in FORBIDDEN_KEYS: True
   build_standard refused it    : False

what a truncated ceiling does to the published tuple:
   CEILING_REQUIRED_SENTENCES = ()
   CEILING_CLAIM_TEMPLATE     = **What this run claims.** Under registered standard.
   the body still built, sha256 = a7d40b4df83530f69d7eb50fcd53b9897c2c1b81f74e19e05b4cc2b8b6474afe
```

(The probe executes the module's own source in a fresh namespace whose
`__file__` points at a fixture directory under `probe/`; `src/` is read, never
written, and the fixture directory is removed at the end.)

Four distinct consequences, all reached:

* a ceiling file with one paragraph yields an **empty** required-sentence tuple.
  W3-REPORT imports that tuple and asserts each member appears verbatim; over an
  empty tuple the assertion is vacuous, the closing record is published with no
  ceiling clause in it, and every check reports success. The body still builds
  and still has a digest, so nothing downstream sees a difference it can name;
* a `marks` list edited in the mirror puts `better` into `MARKS`, into the
  marker schema's `enum` and into the shipped body. `better` is a member of this
  module's own `FORBIDDEN_KEYS` (line 220) and of the house rule this package
  exists to keep; `_refuse_forbidden_keys` (302–311) inspects keys only, so a
  mark *value* passes;
* a mirror missing a register raises `KeyError: 'G'` out of `_build_registers`
  (line 720), not `REGISTER_SET_MISMATCH` — the declared code for exactly this
  shape of failure exists at line 1210 and is not reached at import;
* a missing or malformed data file raises `FileNotFoundError` /
  `json.JSONDecodeError`, neither of which is a `LoopError`, so the interface's
  "every wave-0 exception is a `types.LoopError`" does not hold for this
  module's own load path.

Neither data file is covered by `types.PINNED_SOURCE_PATHS`
(`python3 -c` over `types.PINNED_SOURCE_PATHS` prints the six paths; none is
under `src/minireason/loop/`), which deviation 6 states as a known fact about
`loop_plan_id`. The only binding is `STANDARD_BODY_SHA256`, computed from
whatever bytes are on disk at import — so within one run a damaged ceiling is
self-consistent.

**Repair.** Validate the two files at import and raise `StandardInvalid` with a
declared code: that the ceiling splits into exactly twelve clauses, that clause
0 opens `**What this run claims.**`, that `CEILING_EXHAUSTION_DENIAL` occurs in
the required set, that every `types.CEILING_BLOCK_REASONS` token occurs in the
block-register clause, that `PLAN_8A_MIRROR["marks"]` is exactly
`("differs", "same", "unresolved")`, and that `PLAN_8A_MIRROR["registers"]` has
exactly the four ids — the last through `_validate_registers`' existing codes.

**Test that would hold it.** A fixture data directory per damage (ceiling
truncated, ceiling missing, mirror missing a register, mirror with a widened
`marks`, mirror not JSON), each asserted to raise `StandardInvalid` with the
named code, plus an assertion that
`len(CEILING_REQUIRED_SENTENCES) == 11` on the shipped file.

---

## SHOULD-FIX

### S3. `standard_body` admits every body `build_standard` refuses to emit

**Where.** `src/minireason/loop/standard.py:1347–1376`.

**What it contradicts.** Its own first sentence, line 1348:

> Parse a serialised standard body and refuse anything that is not one.

**Probe.** `python3 probe/p06_parse_and_mutation.py`, verbatim (first block):

```
-- bodies build_standard would refuse, offered to standard_body --
ADMITTED round trip, untouched                                (17 sections)
ADMITTED vocabulary emptied                                   (17 sections)
ADMITTED vocabulary values outside the six                    (17 sections)
ADMITTED 'unresolved' removed from the vocabulary             (17 sections)
ADMITTED guard_parameters emptied                             (17 sections)
ADMITTED judge_seats = 0                                      (17 sections)
ADMITTED paraphrase_n = 0 (G7 switched off)                   (17 sections)
ADMITTED schema_repair_budget = 99                            (17 sections)
ADMITTED reopen_reasons widened                               (17 sections)
ADMITTED unanimity_rule emptied                               (17 sections)
ADMITTED registers reduced to one                             (17 sections)
ADMITTED a register's difference_kinds emptied                (17 sections)
ADMITTED G given a falsifier                                  (17 sections)
ADMITTED rubric mode flipped to pairwise                      (17 sections)
ADMITTED ceiling sha256 replaced                              (17 sections)
ADMITTED a required ceiling sentence deleted                  (17 sections)
REFUSED  a scoring key nested in the body (control)           SCORING_KEY_FORBIDDEN
```

The enumerated refusals in the rest of the docstring (lines 1350–1354 — malformed
JSON, non-object, schema, spec-id, missing section, nested scoring key) do match
the code; the overstatement is the opening sentence, and the consequence is that
the package's only validating parse of a standard body checks the section
*names* and not one guard value. `standard_body` is the natural gate for a body
read back off the graph, and `_validate_registers`, `_validate_vocabulary` and
`_validate_params` are all in this file already.

**Repair.** After the section check, re-run the three validators over
`parsed["vocabulary"]["values"]`, `parsed["guard_parameters"]` and
`parsed["registers"]`, reconstructing `Register` objects or, more cheaply,
factoring the checks to operate on the JSON shapes. Assert also that the two
reopen lists agree (B1).

**Test that would hold it.** Each mutation in the probe above asserted to raise
`StandardInvalid` with its own declared code, and `standard_body(STANDARD_BODY)`
asserted to round-trip.

---

### S4. `assert_config_matches_standard` reconciles the config against the module default, never against the standard the run registers

**Where.** `src/minireason/loop/standard.py:1051–1105` (the reads of
`GUARD_PARAMETERS` at 1084, 1093, 1097 and of `REOPEN_REASONS` at 1099).

**What it contradicts.** Its own docstring, lines 1056–1060:

> Both are folded into `loop_plan_id`, so a disagreement between them is *frozen*
> rather than caught, and a later wave has to guess which owner wins. This is the
> reconciliation that settles it: the standard wins, and a config that differs is
> refused before the first call rather than published as a pre-registration the
> run does not honour.

"The standard" here is the module default, not the body the run pins. The
function takes no body and no digest, so it cannot speak for a registered
standard that is not the module's own — which is precisely the artifact
`build_standard`'s docstring invites a caller to mint.

**Probe.** `python3 probe/p02_successor_body.py`, verbatim (last block):

```
[preflight] registered body guard_parameters: {'judge_seats': 3, 'paraphrase_n': 4}
[preflight] a config matching the registered body is REFUSED:
            code=GUARD_PARAMETER_INVALID detail=config.seats.paraphrase_n=4 contradicts the pinned standard's paraphrase_n=2; a successor standard is a new loop_plan_id, never a config override
[preflight] a config contradicting the registered body (paraphrase_n=2,
            judges=2) is ADMITTED: no exception
```

Both directions are wrong at once: the config that honours the registered
standard is refused, and the config that contradicts it is admitted — and the
refusal message says "the pinned standard's paraphrase_n=2" when the pinned
standard says 4.

**Repair.** Give the function the parameters it is reconciling against:
`assert_config_matches_standard(seats_mapping, reopen_reasons, where="config", *,
guard_parameters=GUARD_PARAMETERS)`, and have PREFLIGHT pass
`standard_body(registered_bytes)["guard_parameters"]`. The default keeps every
present caller working.

**Test that would hold it.** Build a body with `paraphrase_n=4`, parse it, pass
its `guard_parameters`, and assert the `paraphrase_n=4` config reconciles while
the `paraphrase_n=2` config raises `GUARD_PARAMETER_INVALID` naming 4.

---

### S5. The exhaustion exemption does not survive a blockquote or inline emphasis, so the guard refuses the ceiling's own denial in the rendering the design of record uses

**Where.** `src/minireason/loop/standard.py:400–402`.

**What it contradicts.** The function's own docstring, lines 386–389:

> The removal is **whitespace- and case-insensitive**. Deviation 3 stores the
> ceiling clauses unwrapped so that "appears verbatim" survives a renderer that
> re-wraps, and a byte-exact exemption would have refused exactly that: the
> denial re-wrapped across two lines, sentence-cased at the start of a sentence,
> or upper-cased in a heading.

and deviation 4, lines 59–61: "The design's §6 renders `CEILING.md` inside a
**blockquote**; the shipped `data/ceiling_v1.md` is the same text as plain
paragraphs."

**Probe.** `python3 probe/p03_exhaustion_scan.py`, verbatim (relevant blocks):

```
REFUSED  denial with the stem emphasised (inline bold)  RESOURCE_BOUNDARY_MISDESCRIBED | record describes a boundary as 'exhaustion of the inquir'; a reached c

-- the denial as the design of record renders it (deviation 4: blockquote) --
the ceiling clause carrying the denial =
    **A reached ceiling is a declared resource boundary, not exhaustion of the inquiry**, and this record states which was reached and what would reopen the question.
REFUSED  blockquote, wrapped at 40 columns              RESOURCE_BOUNDARY_MISDESCRIBED | record describes a boundary as 'exhaustion of the > inqu'; a reached c
ADMITTED blockquote, wrapped at 50 columns             
REFUSED  blockquote, wrapped at 60 columns              RESOURCE_BOUNDARY_MISDESCRIBED | record describes a boundary as 'exhaustion of the inquir'; a reached c
REFUSED  blockquote, wrapped at 70 columns              RESOURCE_BOUNDARY_MISDESCRIBED | record describes a boundary as 'exhaustion of > the inqu'; a reached c
REFUSED  blockquote, wrapped at 80 columns              RESOURCE_BOUNDARY_MISDESCRIBED | record describes a boundary as 'exhaustion of the > inqu'; a reached c

the 60-column blockquote, verbatim:
    > **A reached ceiling is a declared resource boundary, not
    > exhaustion of the inquiry**, and this record states which
    > was reached and what would reopen the question.

-- list-item and table renderings of the same clause --
ADMITTED bullet item, wrapped at 60                    
ADMITTED one table cell                                
```

The flattening `" ".join(text.split())` removes a whitespace-only continuation
prefix (the bullet item's two spaces survive the scan) but keeps a `>`, which
lands inside the exemption phrase and defeats the match. The shipped file passes
(`probe/p05_body_oracles.py` confirms `CEILING_TEXT` and `STANDARD_BODY` both
pass both scans), so this bites the renderer, not the artifact — but it bites the
renderer in the rendering §6 itself specifies, and the failure mode is the guard
refusing the sentence it exists to protect.

**Repair.** Before removing the denial, strip Markdown line prefixes and inline
emphasis from the flattened copy: drop leading `>`/`-`/`*`/`+`/`N.` tokens per
line before joining, and delete runs of `*`, `_` and backtick. Equivalently,
match the denial with a regex whose inter-word gaps admit any run of
non-alphanumeric characters.

**Test that would hold it.** The denial clause rendered five ways — plain, hard
re-wrapped, blockquoted at several widths, as a bullet, with the stem emphasised
— each asserted to pass; and each of `"the inquiry is exhausted"`,
`"an exhaustive search"`, `"exhaustion of the inquiry"` (no `not`) asserted to
raise `RESOURCE_BOUNDARY_MISDESCRIBED`.

---

### S6. The header-row rule is not GFM's: a prose line ending in `|` hides the next table's header from G12

**Where.** `src/minireason/loop/standard.py:241–254` (`_is_pipe_row`) and
`296–297`:

```python
        if index and _is_pipe_row(lines, index - 1):
            continue                      # a body row, not the header row
```

**What it contradicts.** Design §2.4 G12: "`assert_no_scoring_keys` … is run over
every emitted artifact, **every table header and every rendered file**", and the
function's own docstring, lines 276–279: "silently answering `None` for a
`READING_TABLE.md` carrying a `score` column would make §5's protected
obligation *p4* ('no scoring key appears anywhere') unfalsifiable on two of its
three named subjects. This is the scanner for the other two."

**Probe.** `python3 probe/p04_scoring_headers.py`, verbatim (the two files differ
by one character):

```
REFUSED  rendered record whose prose line ends in a backtick SCORING_KEY_FORBIDDEN | READING_TABLE.md table header on line 4 carries the scoring word '
    the file offered:
      ## Block register
      
      Seat note, verbatim: the registers are written T|E|D|G`
      | reason | score |
      |---|---|
      | schema | 2 |
ADMITTED rendered record whose prose line ends in a pipe
    the file offered:
      ## Block register
      
      Seat note, verbatim: the registers are written T|E|D|G|
      | reason | score |
      |---|---|
      | schema | 2 |
```

In GFM both files render the same table with `score` as a column heading; the
scan admits one of them. The reachable path is not exotic: a rendered record
interleaves program prose with model-authored prose copied verbatim (a judge's
`reading_note`, a critic's `case` — both bounded by `WORD_LIMITS` and both
rendered into `READING_TABLE.md` / `CYCLE.md`), and a line that happens to end in
`|` silences the guard for the table beneath it.

**Repair.** Use GFM's own rule for what a header row is: the line immediately
above a delimiter row. That replaces both the contiguity heuristic and
`_is_pipe_row`'s lookahead, and it makes the "body rows are prose" exemption
exact rather than positional.

**Test that would hold it.** The two files above, asserted to raise the same
code; plus a table preceded by a paragraph, a table at line 0, and a body row
saying "score" asserted to pass.

---

## NOTE

### N7. `MappingProxyType` is applied to two of the eight published mappings

`WORD_LIMITS` (770), `SCHEMAS` (870) and `_SEATS_TO_GUARD` (1044) are read-only;
`PLAN_8A_MIRROR` (347), `RUBRIC_V1` (554), `PLAN_8A_REGISTERS` (732),
`DIFFERENCE_KINDS` (736), `FALSIFIER_MAP` (955) and `GUARD_PARAMETERS` (1008) are
plain `dict`s, though `notes/WAVE0-INTERFACE.md` §2 types each of them `Mapping`
and design §2.1 says "a revised rubric is a **successor artifact and a new
`loop_plan_id`**, never an edit". `python3 probe/p06_parse_and_mutation.py`,
verbatim (second block):

```
GUARD_PARAMETERS mutated in place  -> 7
rebuilt body guard_parameters.paraphrase_n = 7
rebuilt body marks                         = ['differs', 'same', 'unresolved']
DIFFERENCE_KINDS['G']                      = ('grounds_source', 'smuggled_kind')
STANDARD_BODY_SHA256 (frozen at import)    = b4dc7f6a6254307923a166c27b707b3c7b2b67e4d03d4f8349dec802f9d7e2e1
sha256 of a fresh build                    = 5963bc198bc71fe007d5cc7cbfb82fad4e45827273333c0d55ce19d8d61bed59
build_standard() == STANDARD_BODY          = False
```

An importer can edit the pre-registered guard parameters in place and every later
`build_standard()` in that process emits the edited body under the same module.
`DIFFERENCE_KINDS` is documented (734–735) as the one object `contracts` also
holds, so one edit moves both owners at once. Repair: wrap each in
`MappingProxyType`, as the module already does elsewhere. Test: assert each
published mapping raises `TypeError` on item assignment.

### N8. Two `plan_grounding` quotations are not the plan's bytes, inside a body whose own M2 says the register definitions are not paraphrased

`src/minireason/loop/standard.py:650–653` (T `target_prefix_source`) and
`660–662` (E `record_engaged`), against `_MARK_BODY` M2 at 534–535, which ships
inside the same body: "The register definitions are PLAN §8a's own, mirrored
byte-identically and not paraphrased here." The `difference_kinds` ride inside
`body["registers"][rid]`. `python3 probe/p07_mirroring.py`, verbatim:

```
   T target_set_membership        quoted verbatim from plan_text: True
   T target_prefix_source         quoted verbatim from plan_text: False
      grounding : read **with the source artifact prefix intact** - a reference into the account is not a reference into the objection.
      plan_text : * **T — target named.** The represented target of the successor's own engagement. FCL arm: the set of values in `target` arrays, read **with the source artifact prefix intact** — a reference into the account is not a reference into the objection. Prose arm: the phrase by which the successor says what it is responding to. `differs` iff the two sets of distinct targets are not the same set.
   E record_engaged               quoted verbatim from plan_text: False
      grounding : Which of the objection document's records the successor takes up.
      plan_text : * **E — objection record engaged, prefix-resolved.** Which of the objection document's records (`o1 o2 o3 c1 c2 o4 p1 u1`) the successor takes up, by prefix-qualified reference (resolved per §7) or by quotation of that record's own text. A bare id token shared with the account document (`o1 c1 c2 p1 u1`) is `unresolved` for this register and **never** `differs`.
```

T's grounding replaces the plan's em dash with a hyphen; E's elides the record
list and truncates the sentence. The other five are verbatim after whitespace
flattening. Repair: quote the plan's bytes (slice `plan_text`), or rename the
field to `plan_reading` so it does not assert a quotation. Test: assert every
`plan_grounding`, whitespace-flattened, is a substring of its register's
whitespace-flattened `plan_text`.

### N9. `VOCABULARY_NOTE` is retyped, not imported

`src/minireason/loop/standard.py:451–464`. Design §2.1 requires "the six-value
vocabulary **with its published non-exclusivity note reproduced verbatim** from
`ROOT_READING_VOCABULARY`'s docstring". It is byte-identical today —
`python3 probe/p07_mirroring.py` prints `byte-identical: True` — but the module's
own method for the two neighbouring constants is import, not transcription
(lines 413–415: "imported from the instrument rather than retyped … and cannot drift
from it"; `READING_VOCABULARY` and `READING_BANNER` are both the instrument's own
objects, confirmed by `probe/p01_published_shapes.py`). The note is a `#:`
comment in `use_relation_h005.py:137–144`, so it cannot be imported as an
attribute; that is the reason for the transcription and also the reason nothing
holds it. Repair: assert the match in `tests/loop/test_standard.py` by parsing the
comment block, which is what `probe/p07_mirroring.py` does in six lines.

### N10. Neither token scan normalises its input

`src/minireason/loop/standard.py:228` (`_MD_WORD`, ASCII-only) and `400–402`
(the stem scan). `python3 probe/p09_token_scans_unicode.py`, verbatim:

```
-- assert_no_exhaustion_claim --
REFUSED  plain ascii (control)                                RESOURCE_BOUNDARY_MISDESCRIBED
ADMITTED zero-width space inside the stem                     'the inquiry is exhaus​ted'
ADMITTED soft hyphen inside the stem                          'the inquiry is exhaus\xadted'
ADMITTED fullwidth letters                                    'the inquiry is ｅxhausted'
REFUSED  NFKD-decomposed nothing to fold (control)            RESOURCE_BOUNDARY_MISDESCRIBED

-- assert_no_scoring_headers --
REFUSED  plain ascii (control)                                SCORING_KEY_FORBIDDEN
ADMITTED zero-width space in the header cell                  '| cell | sc​ore |\n|---|---|\n'
ADMITTED fullwidth S in the heading                           '# Ｓcore by seat\n'
REFUSED  heading, plain ascii (control)                       SCORING_KEY_FORBIDDEN
```

Program-rendered text will not carry these; model-authored prose copied verbatim
into a rendered record can. Repair: `unicodedata.normalize("NFKC", text)` and
drop category `Cf` characters before scanning, in both functions.

### N11. Setext headings and HTML table headers are outside the scan's scope

`src/minireason/loop/standard.py:225` matches ATX headings only.
`python3 probe/p04_scoring_headers.py` prints `ADMITTED setext heading` for
`"Scores by seat\n==============\n"` and `ADMITTED HTML table header` for
`"<table><tr><th>cell</th><th>score</th></tr></table>"`. The docstring declares
the ATX scope (line 280), so this is a scope gap rather than a contradiction of
the code's own words; it is a gap in the claim that the function makes p4
falsifiable on headings. Repair: treat a line of `=` or `-` under a non-blank
line as a heading, and scan `<th>` cells.

### N12. `_INT_PARAMS["schema_repair_budget"]` is not the range the config owner enforces

`src/minireason/loop/standard.py:1032` gives `(0, 1)`;
`types.SeatsConfig.from_mapping` gives `low=0, high=0`, under a docstring
(`types.py:616–618`) that says "The admissible ranges below are
`standard._INT_PARAMS`' own, so the two owners can no longer have disjoint
ranges". `python3 probe/p08_config_reconciliation.py`, verbatim:

```
types.SeatsConfig.from_mapping bounds:
    "seats.min_judge_families", low=2, high=8),
    "seats.paraphrase_n", low=1, high=8),
    "seats.schema_repair_budget", low=0, high=0))
standard._INT_PARAMS:
    min_judge_families     (2, 8)
    paraphrase_n           (1, 8)
    schema_repair_budget   (0, 1)
design 2.3 says: 'where the config raises it to 1 the re-ask is a new coordinate'
  a config with schema_repair_budget=1 is refused by types with:
    CONFIG_INVALID_VALUE | seats.schema_repair_budget must be a whole number from 0 to 0
  and by the standard's reconciliation with:
    GUARD_PARAMETER_INVALID | config.seats.schema_repair_budget=1 contradicts the pinned standard's schema_rep
  while build_standard admits it as a successor standard's parameter: 22921 bytes
```

The two owners are not disjoint but they are not equal, and design §2.3's
"where the config raises it to 1 the re-ask is a **new coordinate**" is
unreachable through either. Both `types` and `standard` record the narrowing
deliberately (`types.py:618–621`), so the defect is the unqualified claim, not
the value. Repair: either make `_INT_PARAMS["schema_repair_budget"]` `(0, 0)` so
the two ranges are literally the same, or amend the `types` docstring to say the
ranges agree except where the standard pins a single value.

### N13. W0-STANDARD's declared `depends_on` is `[]` and the module imports a same-wave module

`src/minireason/loop/standard.py:131` imports `minireason.loop.types`;
`design/design-s7-wave-plan.md:3–4` says "Waves are dependency-free internally:
every module's `depends_on` lies in a strictly earlier wave", and line 13 gives
W0-STANDARD `"depends_on":[]`. `notes/WAVE0-INTERFACE.md` §0 records and accepts
the edge, and the graph stays acyclic, so this is a reconciled deviation rather
than a fault; it is listed because the wave plan's own text is the acceptance
document and still reads the other way. Repair: record the edge in the wave
plan, or in this module's deviation list.

---

## Tried, and could not break

**1. W0-STANDARD's four acceptance clauses.**
`design/design-s7-wave-plan.md:13` asks for four things and
`python3 probe/p01_published_shapes.py` and `python3 probe/p07_mirroring.py`
find all four holding on the shipped defaults:

```
   T plan_text identical=True  reads identical=True  differs_iff identical=True
   E plan_text identical=True  reads identical=True  differs_iff identical=True
   D plan_text identical=True  reads identical=True  differs_iff identical=True
   G plan_text identical=True  reads identical=True  differs_iff identical=True
   D1 rule is the material text: True
   F2 rule is the material text: True
   F3 rule is the material text: True
```
```
   D1 carries=('T', 'E', 'D') excludes=('G',) G? False
   F2 carries=('T', 'E', 'D') excludes=('G',) G? False
   F3 carries=('T', 'E', 'D') excludes=('G',) G? False
build twice byte-identical  = True
body rubric modes           = {'contrast-mark': 'pairwise', 'relation': 'absolute'}
```

I also tried to make `Falsifier.carries` over-narrow: the design says "G *alone*
never carries D1", and `carries("G")` is flatly `False`. It is not over-narrow —
`carries` is documented (line 925) as "Whether a difference on `register` can
fire this falsifier", and in a cell where T differs and G differs, `carries("T")`
still fires D1. The "alone" wording is preserved in `exclusion_reason`. The
digest is also stable across processes, not just across calls in one:
`python3 -c "…print(S.STANDARD_BODY_SHA256, len(S.STANDARD_BODY))"` run twice
prints `b4dc7f6a6254307923a166c27b707b3c7b2b67e4d03d4f8349dec802f9d7e2e1 22921`
both times.

**2. The body's integer oracle.** The docstring (lines 30–33) claims "every
integer in the built body lies under `guard_parameters` or under
`role_contracts.word_limits`, and each one is a declared resource, seat count or
prose bound". I walked the parsed body for every non-boolean integer;
`python3 probe/p05_body_oracles.py` prints twelve, and:

```
integers outside guard_parameters / role_contracts.word_limits: []
```

I tried to break it by counting booleans as integers (Python would), by looking
for counts smuggled into the PLAN mirror prose and by looking for a length or an
index in `plan_8a`, `registers`, `rubric`, `calibration_anchors` or `ceiling`.
There are none: every number in the mirrored prose is a citation or an id token
inside a string.

**3. The stem scan against real smuggles.** `python3 probe/p03_exhaustion_scan.py`,
verbatim:

```
-- the frozen artifacts --
ADMITTED CEILING_TEXT as shipped                       
ADMITTED STANDARD_BODY as shipped                      
ADMITTED every required sentence joined                

-- plain claims a stop record must not make --
REFUSED  'the inquiry is exhausted'                     RESOURCE_BOUNDARY_MISDESCRIBED | …
REFUSED  'exhaustive search'                            RESOURCE_BOUNDARY_MISDESCRIBED | …
REFUSED  upper case                                     RESOURCE_BOUNDARY_MISDESCRIBED | …

-- the smuggle the docstring names: a claim built around the exemption --
REFUSED  halves joined by the removal                   RESOURCE_BOUNDARY_MISDESCRIBED | record describes a boundary as 'exhaustion'; a reached ceiling is a de
ADMITTED halves with spaces around the exemption       
ADMITTED the denial repeated three times               
REFUSED  denial plus a real claim elsewhere             RESOURCE_BOUNDARY_MISDESCRIBED | record describes a boundary as 'exhausted.'; a reached ceiling is a de
```

The smuggle the docstring names at lines 391–393 — building a claim around the
exemption so that removing it rejoins the halves — is caught: `"exh" + denial +
"austion"` rejoins to `exhaustion` and is refused. The spaced variant (`"exh " +
denial + " austion"`) survives, because the halves rejoin as `"exh  austion"`;
that is not a claim a record could be making, so I record it as the exemption's
exact shape rather than as a bypass. Repeating the denial changes nothing. The
single occurrence of the stem in the shipped bytes is the ceiling's own denial:

```
occurrences of the stem 'exhaust' in the shipped bytes: 1
   ...","**A reached ceiling is a declared resource boundary, not exhaustion of the inquiry**, a...
```

**4. The seats reconciliation, over every field a `SeatsConfig` can carry.** I
expected to find a guard parameter the config can contradict without refusal —
seat counts are in `GUARD_PARAMETERS` but `_SEATS_TO_GUARD` (1044–1048) maps only
three keys. It holds: `SeatsConfig` carries `critic`, `defender` and `variator`
as seat *names* (at most one each, consistent with the counts of 1), `judges` as
a list whose length is checked at 1093, and the three integers that are mapped.
`python3 probe/p08_config_reconciliation.py`:

```
ADMITTED the default config                                
ADMITTED no seats block at all                             
REFUSED  min_judge_families raised                          GUARD_PARAMETER_INVALID | …
REFUSED  paraphrase_n lowered                               GUARD_PARAMETER_INVALID | …
REFUSED  schema_repair_budget raised                        GUARD_PARAMETER_INVALID | …
REFUSED  three judge seats named                            GUARD_PARAMETER_INVALID | …
ADMITTED two judge seats named                             
REFUSED  reopen reason outside the list                     REOPEN_REASON_UNKNOWN | …
ADMITTED reopen list narrowed to one                       
ADMITTED reopen list emptied                               
```

A typo'd or unknown seat key is silently ignored (`ADMITTED a typo'd seat key`),
but `LoopConfig.load` refuses unknown keys with `CONFIG_UNKNOWN_KEY` before
PREFLIGHT ever sees the block, so that path is closed upstream rather than here.
Narrowing the reopen list to nothing is admitted, which is the direction G11
permits.

**5. The ceiling ↔ `BLOCK_CODES` correspondence, in both directions.** The
docstring's last paragraph claims nine reason codes named by ceiling clause seven
correspond to `types.BLOCK_CODES` minus `blocked:constitution`, in the ceiling's
order. `python3 probe/p05_body_oracles.py`:

```
codes the clause names, in its order: ['ensemble-split', 'referential-integrity', 'operative-target', 'order-swap', 'paraphrase-flip', 'outside-vocabulary', 'schema', 'provider', 'baseline-forced-same']
types.CEILING_BLOCK_REASONS         : ['ensemble-split', 'referential-integrity', 'operative-target', 'order-swap', 'paraphrase-flip', 'outside-vocabulary', 'schema', 'provider', 'baseline-forced-same']
same object order                   : True
every named reason is a BLOCK_CODE  : yes
BLOCK_CODES not named by the ceiling: ['blocked:constitution']
```

**6. The scoring-header scan's body-row exemption.** I tried to smuggle a header
through by gluing a second table onto the first with no blank line; the scan
admits it — but GFM admits it too, rendering the line as a body row, which is the
case the docstring deliberately exempts ("a cell may *say* the word `score` in a
sentence"). This is the scan agreeing with the renderer, not a bypass. The
separated second table is refused (`table header on line 5`).

**7. `build_standard`'s validators on the paths they do cover.** Every
`_validate_registers` / `_validate_vocabulary` / `_validate_params` refusal I
could construct fired with its declared code.
`python3 probe/p11_build_refusals.py`, verbatim:

```
-- registers --
REFUSED  a register missing                             REGISTER_SET_MISMATCH        expected ['D', 'E', 'G', 'T'], got
REFUSED  a fifth register                               REGISTER_SET_MISMATCH        expected ['D', 'E', 'G', 'T'], got
REFUSED  a register that is not a Register              REGISTER_SET_MISMATCH        G is not a Register
REFUSED  a register whose id disagrees with its key     REGISTER_SET_MISMATCH        G carries id 'Q'
REFUSED  a register with empty plan_text                REGISTER_TEXT_EMPTY          G
REFUSED  a register with no difference_kinds            DIFFERENCE_KIND_SET_EMPTY    G
REFUSED  a register with a duplicate kind token         DIFFERENCE_KIND_DUPLICATE    G

-- vocabulary --
REFUSED  empty                                          VOCABULARY_EMPTY             
REFUSED  duplicated value                               VOCABULARY_DUPLICATE         ('retains', 'retains', 'unresolved
REFUSED  a value outside the six                        VOCABULARY_NOT_CLOSED        ['is-better-than']
REFUSED  no 'unresolved'                                UNRESOLVED_NOT_IN_VOCABULARY ('retains',)

-- guard parameters --
REFUSED  an unknown key                                 GUARD_PARAMETER_UNKNOWN      ['judge_families']
REFUSED  a missing key                                  GUARD_PARAMETER_MISSING      ['paraphrase_n']
REFUSED  a boolean where an integer is required         GUARD_PARAMETER_INVALID      judge_seats is not an integer
REFUSED  judge_seats below the floor                    GUARD_PARAMETER_INVALID      judge_seats=1 outside [2,8]
REFUSED  paraphrase_n = 0 (G7 switched off)             GUARD_PARAMETER_INVALID      paraphrase_n=0 outside [1,8]
REFUSED  min_resolved_replicates_per_case = 2           GUARD_PARAMETER_INVALID      min_resolved_replicates_per_case=2
REFUSED  an integer where a boolean is required         GUARD_PARAMETER_INVALID      order_swap_both_orders is not a bo
REFUSED  an empty unanimity rule                        GUARD_PARAMETER_INVALID      unanimity_rule is empty
REFUSED  an empty reopen list                           REOPEN_REASON_SET_EMPTY      
REFUSED  a reopen reason outside the list               REOPEN_REASON_UNKNOWN        ['retry-until-it-sticks']
ADMITTED the shipped defaults (control)
```

`isinstance(value, bool)` is checked before `isinstance(value, int)` at line
1251, so `judge_seats=True` is refused rather than read as 1. The gap is not in
these functions; it is that `standard_body` does not call them (S3) and that the
body ignores some of what they validated (B1).

---

## What I could not determine

* **"Every PLAN 8a register definition appears byte-identically against the
  frozen `PLAN.md`"** — the wave plan's first acceptance clause. The sandbox
  carries `src/minireason/loop/data/plan_8a_mirror.json` and its declared
  `plan_sha256` / `material_sha256`, but not
  `experiments/diagnostics/C001-contrast-triple/PLAN.md` or its `material.json`.
  I verified the four registers against the mirror (probe p07, all `True`) and
  stop there: whether the mirror is itself faithful to the frozen PLAN is
  **unresolved** in this sandbox.
* **The ceiling text against design §6.** Only `design-s2-roles-and-guard.md` and
  `design-s7-wave-plan.md` are present. Deviation 3's claim that the eleven
  clauses are the design's invariant ones, deviation 4's claim about the
  blockquote rendering, and O5's account of the claim template's placeholders are
  all statements about a §6 I cannot read. I could not determine whether the
  shipped `ceiling_v1.md` says what §6 says; I used it only as this module's own
  published text. In particular I noticed that the third ceiling clause (the second required
  sentence) fixes a numeral
  ("At N = 5 this is a limit of the design") while deviation 3 calls the eleven
  "invariant", and I could not settle whether that is intended without §6.
* **Every claim of the form "`contracts.X` *is* this object".** `contracts.py` is
  not in the sandbox, so the identity claims for `FORBIDDEN_KEYS`,
  `DIFFERENCE_KINDS`, `SCHEMAS`, `WORD_LIMITS`, `CRITIC_RELATIONS`, `REGISTERS`
  and `ALL_DIFFERENCE_KINDS`, and the claim that `contracts` defines none of
  them, are unverified here. Likewise `FORBIDDEN_KEYS`' claim to mirror
  `tools/contrast_triple_study.FORBIDDEN_KEYS`: neither that file nor any other
  definition of the name exists in this sandbox (searched `src/`; the only hits
  are `standard.py` and the package docstring).
* **Whether `tests/loop/test_standard.py` already catches B2 or N9.** The test
  module is not in the sandbox (`python3 run_tests.py tests.loop.test_standard`
  → `FAILED (errors=1)`; `python3 run_tests.py` → `Ran 0 tests`). The interface
  note says such a test exists and asserts the ceiling ↔ block-code
  correspondence. My findings are about what the module holds on its own; a test
  outside it may or may not hold some of the same ground, and I could not check.
* **Whether any wave-1+ caller mints a non-default standard body.** B1 and S4 are
  defects in a published API path that `build_standard`'s docstring invites. No
  caller exists in this sandbox, so I could not determine whether the path is
  exercised today; I report the seam, not a live failure.
* **What I left out.** I did not review `types.py` beyond the five constants and
  the two config classes W0-STANDARD is answerable to, and I did not attempt the
  O1–O11 open questions except where one bears on a line of `standard.py`
  (O4 and O10 are consistent with what I found; O2, O3, O6, O7, O8 and O11 are
  about modules not in the sandbox). I did not attempt to assess the *content* of
  the rubric prose, the calibration anchors' constructions or the ceiling's
  wording as readings — only their correspondence to the documents named above.
