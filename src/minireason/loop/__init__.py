"""The automated end-to-end harness loop.

This package implements *The automated end-to-end harness loop — FINAL design of
record*.  It automates the labour of three acts the published instruments reserve
for root — the ``use_relation_h005`` reading cells, the C001 PLAN §8a
contrast-register marks, and the continue/stop decision — together with the
dispatch, import and publication that produce the material they read.  It
automates none of the authority: every reading is a registered, attackable
artifact, an unresolved cell is a first-class outcome, and a reached ceiling is a
declared resource boundary.

This file is a docstring and nothing else.  It imports no submodule, so importing
``minireason.loop`` costs nothing and can never make a cycle; the conventions below
are recorded here because they are the ones a module of a later wave has to know
before it reads any source, and because five of them were settled by the wave-0
integration rather than by any single module.

A repository-level defect a wave-3 author will meet: on a cold ``.pyc`` cache,
``python3 -W error -c "import minireason.loop.contracts"`` fails with
``SyntaxError: invalid escape sequence`` for a backslash-s.  It is not this package's: the
import chain reaches the frozen ``src/minireason/use_relation_h005.py``, whose
docstring writes a regex in a non-raw string.  Ten modules here reach it
(``contracts``, ``standard``, ``surface``, ``seats``, ``graph``, ``synthetic``,
``packs``, ``roles``, ``markprep``, ``decide``); ``types``, ``custody``,
``receipts``, ``obligations``, ``publish`` and ``steps`` import clean.  Editing
that instrument bumps its ``source_identity`` and invalidates every frozen plan
that pins it, so the repair is the SRC-003 erratum's; nothing in this package
runs under ``-W error``, and a test asserts that no module here adds to it.

Wave 0 — who owns what
======================

``types``      the config schema and its strict loader, ``loop_plan_id``, the step
               receipt and ``step_key``, the run layout, and the four closed code
               tables: ``STOP_REASONS``, ``BLOCK_CODES``, ``FAILURE_CODES``,
               ``STEP_KINDS`` (with ``REPLAYABLE_STEPS`` / ``SPENDING_STEPS``).
               It imports **no sibling**, so it is the root of the package graph.
``standard``   the ``std:reading-rubric/v1`` body, and the single owner of every
               shared vocabulary: ``READING_VOCABULARY``, ``NOMINABLE_RELATIONS``,
               ``CRITIC_RELATIONS``, ``NONE_TOKEN``, ``UNRESOLVED_TOKEN``,
               ``OUTSIDE_VOCABULARY_FIELD``, ``READING_BANNER``, ``MARKS``,
               ``REGISTER_IDS`` (also exported as ``REGISTERS``),
               ``DIFFERENCE_KINDS``, ``FORBIDDEN_KEYS``, ``REOPEN_REASONS``,
               ``FALSIFIER_MAP``, ``GUARD_PARAMETERS``, ``CALIBRATION_ANCHORS``
               and ``CEILING_REQUIRED_SENTENCES``.
``contracts``  the five role schemas and their validators.  It **imports** every
               vocabulary above from ``standard`` and defines none of them; the
               names on both sides are the same objects.
``custody``    pins, pin verification, digests, write-once writes, the path fence.
``receipts``   the locked byte-mode ledger append, receipt-id minting, the
               ``tools/repo_activity.py`` wrapper, the cadence clock.
``publish``    explicit-path add, credential scan, commit, non-forcing push,
               read-back, and the ``VERIFIED`` line.

The import graph is ``types -> standard -> contracts`` plus ``types -> custody``,
``types -> receipts``, ``types -> publish``.  It is acyclic, and a test asserts it.

Wave 1 — who owns what
======================

``surface``      the frozen material surface ``M`` of one use-relation row, its
                 offset table back to the occurrence files, and the
                 unique-substring resolver.  G2(a) and G3, and nothing else: it
                 opens no file and says where a quote *is*, never whether it is apt.
``seats``        ``(registry, config) -> SeatPlan``, the canonical seat table that
                 goes into ``plan.json``, the per-credential ceiling
                 (``key_cap_for``) and the one import of runner v2's outer key
                 gate.  "Distinct family" is compared over the model **lineage**:
                 ``seats.lineage`` strips the host route, so ``deepseek`` and
                 ``ollama-cloud/deepseek`` never take both judge seats.
``obligations``  the pre-registered O and P, their named program predicates over a
                 registered graph, ``ProducedBy``, and the ``losses_outside_P``
                 register.  A verdict is one of three tokens and never a quantity.
``graph``        how readings and marks enter the graph: the six artifact shapes,
                 the rubric-typed demonstrative warrant, the audit and appellate
                 paths, and the read-back of a cell's standing.  It is **the writer
                 of** ``record``: every loop-authored body carries the token
                 ``obligations`` reads (``graph.RECORD_KINDS``), and the material's
                 own bytes deliberately carry none.
``steps``        the write-once step ledger under ``<run_root>/steps/``: open
                 markers, resume plans, replay, the run lock, and the publication
                 steps that file a ``VERIFIED`` line three ways.
``synthetic``    the offline dry-run fixture — scripted providers, a synthetic
                 occurrence and registry, and the inducible failures W6 exercises.
                 It calls no provider and reads no credential.

The wave-1 import graph, which keeps the package acyclic:

    ``surface -> contracts, types``
    ``seats -> contracts, types``
    ``obligations -> types``          (only; it mirrors ``UNRESOLVED_TOKEN``)
    ``graph -> contracts, standard, types``
    ``steps -> custody, publish, receipts, types``
    ``synthetic -> contracts, standard, types``

No wave-1 module imports another wave-1 module.  Where two of them must agree -
``graph``'s ``record`` tokens with ``obligations``' ``RECORD_KINDS``,
``graph.mark_triples`` with W2-DECIDE's comparison - the agreement is stated in a
docstring and asserted by a test that imports both, never by an import between them.

Wave 2 — who owns what
======================

``packs``      the deterministic render of every role's pack, the exchange surface
               ``E`` of G2(b), the order swap, the paraphrase input, and the
               precedent slice with the query text that selected it.  It calls no
               provider, writes nothing and decides nothing: it lays out what a
               seat is asked, never what the answer is worth.
``roles``      the one place the loop speaks to a model: one ``provider.complete``
               per call, two gates in one fixed order (``seats.key_gate_for``
               outside, the transport's ``slots_for`` inside), one write-once call
               record per coordinate, and **no retry anywhere**.  A provider
               failure is *returned* as a blocked result carrying the transport's
               own code, never raised.
``markprep``   the C001 program pre-pass: the byte-identity finding, the
               under-replication rule, register E's prefix resolution and shared
               bare-token forcing, registers T and D parsed off the FCL arm, the
               sealed within-ORIGINAL baseline and the residue a marker trials.
``decide``     the pre-registered stop/continue program: the three guard rails,
               the five clauses in the design's order, the declared-condition
               clause after them, and the decision record with its mandatory
               ``would_reopen`` and its ``losses_outside_P`` section.

The wave-2 import graph, and the two cross-wave edges the wave plan does not name
(wave-1 integration decision 54):

    ``packs -> contracts, standard, surface, types``
    ``roles -> contracts, custody, seats, types``
    ``markprep -> contracts, custody, standard, surface, types``
    ``decide -> graph, obligations, standard, types``

``markprep`` reaches **W1-SURFACE** because the pairwise surface is built out of
``Surface``/``Span`` and resolved with ``resolve_unique``: one resolver, not two.
Every wave-2 module reaches **W0-STANDARD** because the ceiling sentences and
``assert_no_exhaustion_claim`` have one owner, and a module that retyped either
would be a second.  No wave-2 module imports another wave-2 module, the graph is
acyclic, and ``tests/loop/test_contracts.py`` asserts both the exact edge set and
the acyclicity.

Conventions a later wave must not re-invent
===========================================

**Shared constants have one owner.**  Import a vocabulary from ``standard`` (or
from ``contracts``, which re-exports the same objects under the spellings the wave
plan published for the role schemas).  Never retype one.  ``BLOCK_CODES``,
``FAILURE_CODES`` and ``STOP_REASONS`` belong to ``types``; ``SCHEMA_REASONS``
belongs to ``contracts`` and is a *different grain* — its members are the
sub-reasons of the one block code ``blocked:schema``, not codes in their own right.

**Block codes are spelled** ``blocked:<name>``.  Nine of the ten names are exactly
the nine the frozen ceiling promises are "printed with counts on every table";
``blocked:constitution`` is the tenth.  Build one with ``types.block_code(reason)``
rather than concatenating.

**Every wave-0 exception is a** ``types.LoopError``, and keeps the base it already
had: ``ContractError`` and ``StandardInvalid`` are still ``ValueError``,
``WriteOnceViolation`` is still ``FileExistsError``, ``CredentialInOutput`` is
still ``ValueError``.  So ``except LoopError`` catches every refusal in the
package, and every existing ``except`` keeps working.  Each carries a ``.code``;
every UPPER_SNAKE code any of the sixteen modules can raise is a member of
``types.FAILURE_CODES``, and ``custody.CUSTODY_CODES`` is a slice of it, not a
rival table.  The one exception is ``types.OUTCOME_CODES``, which holds tokens
naming something the loop **did** rather than something it refused;
``APPELLATE_RULING_APPLIED`` is its only member, and the two tables are disjoint.
A module of a later wave declares its own ``NEW_CODES`` mapping - code to the
one-line reason it exists - and that wave's integrator folds it into one of the
two tables and adds the module to ``FOLDED_IN`` in the same commit (O9).

**An open step marker is** ``steps/NNNN-KIND.json.open`` — the layout block's
spelling, not the prose's ``.open.json``.  Get the path from
``RunPaths.step_path(index, kind, open_marker=True)`` so the two spellings cannot
drift apart.

**``run_paths(root, run_id)`` takes the repository root**, not a run directory.
The run tree is ``<root>/experiments/loops/<run_id>``, and ``LOOPS_ROOT`` is a
constant of ``types`` so no caller retypes it.  Occurrence trees are *referenced*
from there and never written into.

**``StepLedger(run_root, loop_plan_id)`` takes the run root** — the
``<root>/experiments/loops/<run_id>`` directory that ``run_paths`` returns as
``.run_root``, not the repository root and not the ``steps/`` directory.

**``Cadence.check(now)`` takes a timezone-aware ``datetime``**, fed from the
harness clock the driver already injects, never ``datetime.now()`` taken inside the
call.  A naive moment is refused: it has no UTC meaning.  The clock refuses to move
backwards, and a missed deadline is recorded at the moment it was noticed and never
backdated.

**``publish()`` returns the VERIFIED line and writes nothing to the ledger.**
``receipts`` owns ``docs/DECISION_LEDGER.md``; the driver wires the two together.
Likewise ``publish`` shells no activity logger — the driver brackets a publish step
with its own ``receipts.activity`` records.

**``custody.write_new(path, value)`` does not fence.**  Its signature carries no
root, so a caller writing under the run root passes
``write_new(fenced(run_root, relative), value)``.  ``write_new`` refuses an
existing path and refuses credential-bearing bytes; ``fenced`` refuses a path that
escapes the root.  They are two guards and both are needed.

**``loop_plan_id(config, pins)`` refuses a null pin.**  A pin whose value is
``None``, not a lowercase sha256, or keyed by an absolute or ``..``-bearing path is
``PIN_INVALID``: an unpinned file inside a plan identity pins nothing.  Pin *order*
does not affect the identity; a declared config value does.

**The provider wall-clock timeout is read off the endpoint, never off the config.**
It is the endpoint's own ``timeout_seconds`` as frozen into the plan (180 s for all
24 endpoints), re-read before each send and written into both the request and the
receipt; a disagreement is ``TIMEOUT_NOT_APPLIED``.  ``timeouts.step_seconds`` and
``timeouts.git_seconds`` are the *other two* layers and cannot change it.

**The credential floor is 8 bytes.**  A value shorter than
``custody.MIN_CREDENTIAL_LENGTH`` is not searched for, because a one-character
placeholder in a key variable occurs in almost every record by accident.  It equals
the transport's own ``provider_openai_compat._MIN_SECRET_LENGTH`` and a test pins
the agreement.  Credentials are read from the environment at call time by the
transport only, are never written anywhere, and a bearing record is **refused, not
redacted**.

**The token "exhaustion" is not in the stop vocabulary**, and
``standard.assert_no_exhaustion_claim(text)`` is the scan.  It exempts exactly one
phrase — ``standard.CEILING_EXHAUSTION_DENIAL``, the frozen ceiling's own denial —
because banning the token outright would delete the sentence that states the rule.
A reached ceiling is a declared resource boundary, and the record says which one
was reached and what would reopen the question.
"""
