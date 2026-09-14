"""Tests for W0-TYPES, the loop's shared types and closed vocabularies.

Every test below whose name begins ``test_clause_`` is named after one clause
of the module's wave-plan acceptance list; the rest cover the remainder of the
declared public interface.
"""
from __future__ import annotations

import ast
import importlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

STAGING = Path(__file__).resolve().parents[2]
if str(STAGING / "src") not in sys.path:
    sys.path.insert(0, str(STAGING / "src"))

from minireason.loop import contracts, custody, publish, receipts, standard  # noqa: E402
from minireason.loop import types as loop_types  # noqa: E402
from minireason.loop.types import (  # noqa: E402
    BLOCK_CODES,
    CONFIG_SCHEMA,
    FAILURE_CODES,
    LOOPS_ROOT,
    PINNED_SOURCE_PATHS,
    PROVIDER_MODES,
    REPLAYABLE_STEPS,
    SPENDING_STEPS,
    STEP_KINDS,
    STEP_SCHEMA,
    STEP_STATUSES,
    STOP_REASONS,
    AuditConfig,
    ContrastConfig,
    CustodyReport,
    LoopConfig,
    LoopError,
    RunPaths,
    SeatsConfig,
    StepReceipt,
    TimeoutsConfig,
    is_failure_code,
    is_stop_reason,
    loop_plan_id,
    run_paths,
)

PACKAGE = Path(loop_types.__file__).resolve().parent
#: W5-DRIVER. Outside the package by the wave plan's own path, and folded into
#: the tables like any module of it (see ``collect``).
DRIVER_SOURCE = PACKAGE.parents[2] / "tools" / "auto_loop.py"

CONFIG = {
    "schema": CONFIG_SCHEMA,
    "run_id": "LOOP-01",
    "study": "h005",
    "occurrences": ["experiments/h005/occurrence-01"],
    "runner": "tools/multicycle_commitment_study_multi_v2.py",
    "cycle_budget": 3,
    "max_calls": 240,
    "reading_set": ["p1/mini_fcl/cycle-1/n1#r3"],
    "obligations_path": "experiments/loops/LOOP-01/obligations.json",
    "graph_root": "experiments/loops/LOOP-01/graph",
    "reopen_reasons": ["new-material", "repaired-guard", "appellate-ruling"],
    "audit": {
        "period": 2,
        "judge_err_max": 0.2,
        "judge_err_max_account": (
            "The calibration set is five anchors, so 0.2 is one anchor: this run "
            "declines to read on the first anchor a seat gets wrong, and says so "
            "rather than carrying a margin nobody stated."
        ),
        "streak_max": 5,
        "streak_max_account": (
            "Five consecutive guard blocks on one role is longer than any run of "
            "blocks the dry run produced, so a streak of five is the instrument "
            "declining to read rather than a hard row."
        ),
    },
}
#: Every member of ``PINNED_SOURCE_PATHS`` (``loop_plan_id`` requires the six
#: fixed pins) plus one run-specific pin, which is the one a test may drop.
PINS = {path: chr(ord("a") + index) * 64
        for index, path in enumerate(PINNED_SOURCE_PATHS)}
PINS["experiments/loops/loop-001/plan.json"] = "f" * 64
PLAN = "c" * 64


def write_config(directory: Path, **overrides) -> Path:
    body = dict(CONFIG)
    body.update(overrides)
    path = Path(directory) / "config.json"
    path.write_text(json.dumps(body, indent=2), encoding="utf-8")
    return path


# ------------------------------------------------------------------ clauses


class AcceptanceClauses(unittest.TestCase):
    """One test per clause of the W0-TYPES acceptance list."""

    def test_clause_two_loads_of_one_config_give_the_same_plan_id(self):
        with tempfile.TemporaryDirectory() as directory:
            path = write_config(Path(directory))
            first, second = LoopConfig.load(path), LoopConfig.load(path)
            self.assertEqual(first, second)
            self.assertEqual(loop_plan_id(first, PINS), loop_plan_id(second, PINS))
            # ... and a reformatted file declaring the same values is the same
            # plan: the identity is over the canonical config, not its bytes.
            other = Path(directory) / "reformatted.json"
            other.write_text(json.dumps(CONFIG, indent=4, sort_keys=True) + "\n",
                             encoding="utf-8")
            self.assertEqual(loop_plan_id(LoopConfig.load(other), PINS),
                             loop_plan_id(first, PINS))
            # ... and the raw mapping and the loaded object agree.
            self.assertEqual(loop_plan_id(CONFIG, PINS), loop_plan_id(first, PINS))

    def test_clause_a_changed_pin_changes_the_plan_id(self):
        config = LoopConfig.from_mapping(CONFIG)
        base = loop_plan_id(config, PINS)
        moved = dict(PINS)
        moved["src/minireason/use_relation_h005.py"] = "9" * 64
        self.assertNotEqual(base, loop_plan_id(config, moved))
        added = dict(PINS, **{"docs/CEILING.md": "e" * 64})
        self.assertNotEqual(base, loop_plan_id(config, added))
        dropped = {k: v for k, v in PINS.items() if "plan.json" not in k}
        self.assertNotEqual(base, loop_plan_id(config, dropped))
        # A declared value changing changes it too, and pin ORDER does not.
        self.assertNotEqual(base, loop_plan_id(dict(CONFIG, cycle_budget=4), PINS))
        self.assertEqual(base, loop_plan_id(config, dict(reversed(list(PINS.items())))))

    def test_clause_an_unknown_config_key_is_refused(self):
        for raw, code in (
            (dict(CONFIG, tempterature=1), "CONFIG_UNKNOWN_KEY"),
            (dict(CONFIG, seats={"critic": "a", "judge": "b"}), "CONFIG_UNKNOWN_KEY"),
            (dict(CONFIG, audit={**CONFIG["audit"], "slack": 1}), "CONFIG_UNKNOWN_KEY"),
            (dict(CONFIG, audit={k: v for k, v in CONFIG["audit"].items()
                                 if k != "judge_err_max_account"}), "CONFIG_MISSING_KEY"),
            (dict(CONFIG, audit={k: v for k, v in CONFIG["audit"].items()
                                 if k != "streak_max_account"}), "CONFIG_MISSING_KEY"),
            (dict(CONFIG, contrast={"attached": False, "extra": 1}), "CONFIG_UNKNOWN_KEY"),
            (dict(CONFIG, timeouts={"step_seconds": {}, "wall": 1}), "CONFIG_UNKNOWN_KEY"),
            ({k: v for k, v in CONFIG.items() if k != "audit"}, "CONFIG_MISSING_KEY"),
            (dict(CONFIG, schema="minireason.loop.config.v2"), "CONFIG_SCHEMA_UNKNOWN"),
        ):
            with self.subTest(code=code):
                with self.assertRaises(LoopError) as caught:
                    LoopConfig.from_mapping(raw)
                self.assertEqual(caught.exception.code, code)
        with tempfile.TemporaryDirectory() as directory:
            path = write_config(Path(directory), unknown_key=True)
            with self.assertRaises(LoopError) as caught:
                LoopConfig.load(path)
            self.assertEqual(caught.exception.code, "CONFIG_UNKNOWN_KEY")

    def test_clause_the_token_exhaustion_appears_in_no_vocabulary(self):
        vocabularies = {
            "STOP_REASONS": STOP_REASONS, "BLOCK_CODES": BLOCK_CODES,
            "FAILURE_CODES": FAILURE_CODES, "STEP_KINDS": STEP_KINDS,
            "REPLAYABLE_STEPS": REPLAYABLE_STEPS, "SPENDING_STEPS": SPENDING_STEPS,
            "STEP_STATUSES": STEP_STATUSES, "PROVIDER_MODES": PROVIDER_MODES,
        }
        for name, vocabulary in vocabularies.items():
            for token in vocabulary:
                with self.subTest(vocabulary=name, token=token):
                    self.assertNotIn("exhaust", token.lower())
        # The boundary the ceiling is actually named by is present instead.
        self.assertIn("resource_boundary", STOP_REASONS)
        self.assertTrue(is_stop_reason("resource_boundary"))

    def test_clause_every_block_code_used_anywhere_in_the_package_is_a_member(self):
        pattern = re.compile(r"blocked:[A-Za-z0-9][A-Za-z0-9_-]*")
        used: set[str] = set()
        sources = sorted(PACKAGE.rglob("*.py"))
        self.assertTrue(sources, f"no package sources under {PACKAGE}")
        for source in sources:
            used.update(pattern.findall(source.read_text(encoding="utf-8")))
        self.assertTrue(used, "the scan found no block code at all")
        self.assertEqual(used - set(BLOCK_CODES), set(),
                         "a block code outside BLOCK_CODES is used in the package")


# ------------------------------------------------------- the rest of W0-TYPES


class Vocabularies(unittest.TestCase):

    def test_the_token_exhaustion_is_absent_from_this_module_source(self):
        """Outside one marked region, which exists only to refuse the token.

        The region is delimited in ``types.py`` by ``BEGIN/END REFUSED TOKEN``
        and holds ``_REFUSED_STOP_STEM`` and :func:`is_stop_reason`. A guard
        must name what it refuses - the same exemption the ceiling's denial
        sentence has in W0-STANDARD - and nothing else in the file may.
        """

        source = (PACKAGE / "types.py").read_text(encoding="utf-8")
        head, _, rest = source.partition("# ---- BEGIN REFUSED TOKEN")
        region, _, tail = rest.partition("# ---- END REFUSED TOKEN")
        self.assertTrue(region, "the marked region is gone; so is the exemption")
        self.assertNotIn("exhaust", (head + tail).lower())
        self.assertIn("exhaust", region.lower())
        # The region does what it says: it refuses, it does not declare.
        for table in (STOP_REASONS, FAILURE_CODES, BLOCK_CODES):
            for token in table:
                self.assertNotIn("exhaust", token.lower())

    def test_item17_a_preregistered_condition_may_not_name_exhaustion(self):
        """Item 17: the one parameterised stop token admitted any id.

        ``preregistered_condition:inquiry_exhausted`` is the one door through
        which the claim the ceiling denies could reach the closing record.
        """

        for stem in ("exhaust", "Exhaust", "EXHAUST", "eXhAuSt"):
            for shape in ("{}", "inquiry_{}ed", "{}ion", "c3-{}", "pre.{}.post"):
                token = "preregistered_condition:" + shape.format(stem)
                with self.subTest(token=token):
                    self.assertFalse(is_stop_reason(token))
        # ... and every other identifier still passes, so this refuses one word
        # rather than narrowing the vocabulary.
        for good in ("c3", "obligation-o3", "no.new.material", "A1", "x" * 64):
            with self.subTest(token=good):
                self.assertTrue(is_stop_reason("preregistered_condition:" + good))

    def test_item15_a_bare_string_is_never_a_list_of_custody_checks(self):
        """Item 15: three doors turned one code into nineteen one-letter checks."""

        for door in (lambda v: CustodyReport(checks=v),
                     lambda v: CustodyReport.from_mapping({"checks": v}),
                     CustodyReport.from_findings,
                     lambda v: StepReceipt.from_dict(
                         {**self.a_receipt(), "custody": {"checks": v}})):
            for value in ("SOURCE_PIN_MISMATCH", b"SOURCE_PIN_MISMATCH",
                          bytearray(b"SOURCE_PIN_MISMATCH")):
                with self.subTest(door=door, value=value):
                    with self.assertRaises(LoopError) as caught:
                        door(value)
                    self.assertEqual(caught.exception.code, "STEP_RECEIPT_INVALID")
        # The honest record, for contrast: one finding is one check.
        report = CustodyReport.from_findings(["SOURCE_PIN_MISMATCH"])
        self.assertEqual(report.checks, ("SOURCE_PIN_MISMATCH",))
        self.assertFalse(report.verified)
        self.assertTrue(CustodyReport.from_findings(()).verified)
        # A findings argument that is not iterable at all is the same refusal.
        with self.assertRaises(LoopError) as caught:
            CustodyReport.from_findings(7)
        self.assertEqual(caught.exception.code, "STEP_RECEIPT_INVALID")

    @staticmethod
    def a_receipt():
        return StepReceipt.build(
            loop_plan_id="c" * 64, index=1, kind="SEND", cycle=1,
            started_utc="2026-09-14T09:00:00+00:00").as_dict()

    def test_item16_every_public_door_refuses_with_its_own_code(self):
        """Item 16: ``code`` was not threaded through the shared helpers.

        A pin refusal surfaced as CONFIG_INVALID_VALUE, a receipt's cycle range
        as CONFIG_INVALID_VALUE, and a custody finding mixed two codes. The
        table below is the whole of what each public door may answer.
        """

        plan = "c" * 64
        good = "2026-09-14T09:00:00+00:00"
        cases = (
            ("pins not an object",
             lambda: loop_plan_id(CONFIG, ["src/a.py"]), "PIN_INVALID"),
            ("pin key not a string",
             lambda: loop_plan_id(CONFIG, {7: "a" * 64}), "PIN_INVALID"),
            ("pin key empty",
             lambda: loop_plan_id(CONFIG, dict(PINS, **{"   ": "a" * 64})),
             "PIN_INVALID"),
            ("pin key absolute",
             lambda: loop_plan_id(CONFIG, dict(PINS, **{"/a.py": "a" * 64})),
             "PIN_INVALID"),
            ("pin value null",
             lambda: loop_plan_id(CONFIG, dict(PINS, **{"a.py": None})),
             "PIN_INVALID"),
            ("receipt cycle 0",
             lambda: StepReceipt.key(plan, "SEND", 0, None, {}),
             "CYCLE_OUT_OF_RANGE"),
            ("receipt cycle 100",
             lambda: StepReceipt.key(plan, "SEND", 100, None, {}),
             "CYCLE_OUT_OF_RANGE"),
            ("receipt cycle 0 through build",
             lambda: StepReceipt.build(loop_plan_id=plan, index=1, kind="SEND",
                                       cycle=0, started_utc=good),
             "CYCLE_OUT_OF_RANGE"),
            ("receipt inputs not an object",
             lambda: StepReceipt.key(plan, "SEND", 1, None, []),
             "STEP_RECEIPT_INVALID"),
            ("receipt inputs key empty",
             lambda: StepReceipt.key(plan, "SEND", 1, None, {"": "a" * 64}),
             "STEP_RECEIPT_INVALID"),
            ("receipt not an object",
             lambda: StepReceipt.from_dict([]), "STEP_RECEIPT_INVALID"),
            ("custody finding with an empty code",
             lambda: CustodyReport.from_findings([""]), "STEP_RECEIPT_INVALID"),
            ("custody finding that is not a string",
             lambda: CustodyReport.from_findings([7]), "STEP_RECEIPT_INVALID"),
            ("custody block with an unknown key",
             lambda: CustodyReport.from_mapping({"verifed": True}),
             "STEP_RECEIPT_INVALID"),
            ("custody block that is not an object",
             lambda: CustodyReport.from_mapping(7), "STEP_RECEIPT_INVALID"),
            ("a misspelled build field",
             lambda: StepReceipt.build(loop_plan_id=plan, index=1, kind="SEND",
                                       started_utc=good, failure_codes="X"),
             "STEP_RECEIPT_INVALID"),
            ("a config that is not an object",
             lambda: LoopConfig.from_mapping([]), "CONFIG_NOT_A_MAPPING"),
            ("a config with an unknown key",
             lambda: LoopConfig.from_mapping(dict(CONFIG, nope=1)),
             "CONFIG_UNKNOWN_KEY"),
            ("a bad run_id", lambda: LoopConfig.from_mapping(dict(CONFIG, run_id="a b")),
             "RUN_ID_INVALID"),
        )
        for label, call, code in cases:
            with self.subTest(door=label):
                with self.assertRaises(LoopError) as caught:
                    call()
                self.assertEqual(caught.exception.code, code)
                self.assertIn(caught.exception.code, FAILURE_CODES)

    def test_stop_reasons_are_design_4_4_and_admit_a_preregistered_condition(self):
        self.assertEqual(set(STOP_REASONS), {
            "protected_loss", "obligations_discharged", "no_new_reading_changes",
            "resource_boundary", "custody_halt", "all_arms_ended", "instrument_fault"})
        self.assertTrue(is_stop_reason("preregistered_condition:c3"))
        for bad in ("preregistered_condition:", "preregistered_condition:../x",
                    "stopped", "", None, 3, "protected_loss "):
            with self.subTest(token=bad):
                self.assertFalse(is_stop_reason(bad))

    def test_block_codes_cover_every_blocking_guard_step_of_design_2_4(self):
        self.assertEqual(set(BLOCK_CODES), {
            "blocked:constitution", "blocked:schema", "blocked:referential-integrity",
            "blocked:operative-target", "blocked:ensemble-split", "blocked:order-swap",
            "blocked:paraphrase-flip", "blocked:outside-vocabulary",
            "blocked:provider", "blocked:baseline-forced-same"})
        # A block is a reason code, never a status of the material.
        for code in BLOCK_CODES:
            self.assertTrue(code.startswith(loop_types.BLOCK_CODE_PREFIX))
            self.assertNotIn(code, FAILURE_CODES)

    def test_block_code_builds_only_a_declared_code(self):
        self.assertEqual(loop_types.block_code("ensemble-split"),
                         "blocked:ensemble-split")
        for bad in ("made-up", "", "blocked:schema", "SCHEMA"):
            with self.subTest(reason=bad):
                with self.assertRaises(LoopError) as caught:
                    loop_types.block_code(bad)
                self.assertEqual(caught.exception.code, "BLOCK_CODE_UNKNOWN")

    def test_failure_codes_carry_the_provider_custody_and_step_codes_named_by_design(self):
        for code in ("HTTP_429", "KEY_MISSING", "TRANSPORT_OR_RESPONSE_ERROR",
                     "SECRET_IN_REQUEST", "TIMEOUT_NOT_APPLIED", "SOURCE_PIN_MISMATCH",
                     "TRANSPORT_PIN_MISMATCH", "PROVIDER_REQUEST_FILE_CHANGED",
                     "REQUEST_NOT_FROM_PLAN", "ARTIFACT_NOT_DERIVED_FROM_DELIVERY",
                     "UNRESOLVED_STEP", "STEP_NONDETERMINISTIC", "STEP_TIMEOUT",
                     "PLAN_ID_MISMATCH", "BUDGET_RAISED", "NO_REPLAY",
                     "BASELINE_NOT_FIRST", "SCORING_KEY_FORBIDDEN", "NOT_DISPATCHED",
                     "INDETERMINATE", "NEW_PREREGISTRATION_REQUIRED",
                     "FAMILY_COUNT_INSUFFICIENT"):
            with self.subTest(code=code):
                self.assertTrue(is_failure_code(code))
        self.assertFalse(is_failure_code("blocked:schema"))
        self.assertFalse(is_failure_code("made_up"))

    def test_step_kinds_cover_s0_to_s15_and_classify_replay_and_spend(self):
        for kind in ("PREREGISTER", "PREFLIGHT", "PUBLISH_PLAN", "CYCLE_OPEN", "PREPARE",
                     "PUBLISH_IN", "SEND", "PUBLISH_EV", "IMPORT", "USE_TABLE", "READ",
                     "MARK", "ADJUDICATE", "DECIDE", "PUBLISH_CY", "CLOSE", "AUDIT"):
            self.assertIn(kind, STEP_KINDS)
        self.assertEqual(len(set(STEP_KINDS)), len(STEP_KINDS))
        self.assertLessEqual(REPLAYABLE_STEPS | SPENDING_STEPS, set(STEP_KINDS))
        self.assertEqual(REPLAYABLE_STEPS & SPENDING_STEPS, set(),
                         "a step cannot be both replayable and spending")
        for kind in STEP_KINDS:
            if kind.startswith("PUBLISH"):
                self.assertIn(kind, SPENDING_STEPS)

    def test_pinned_source_paths_all_exist_in_this_checkout(self):
        for relative in PINNED_SOURCE_PATHS:
            with self.subTest(path=relative):
                self.assertTrue((STAGING / relative).exists(), relative)

    def test_loop_error_carries_a_stable_upper_snake_code(self):
        error = LoopError("PLAN_ID_MISMATCH", "the config moved")
        self.assertEqual(error.code, "PLAN_ID_MISMATCH")
        self.assertIn("PLAN_ID_MISMATCH", str(error))
        for bad in ("lower_case", "blocked:schema", "", "Has Space", 7):
            with self.subTest(code=bad):
                with self.assertRaises(ValueError):
                    LoopError(bad, "x")


class TheCodeTablesAreComplete(unittest.TestCase):
    """Wave-0 integration decision 3: one rule, stated in the types docstring.

    Every string literal in ``src/minireason/loop/**.py`` that can reach a record
    as a stable token -- the first argument of a loop exception constructor (or
    of ``super().__init__`` inside one of their subclasses, or of a
    module-private ``_fail`` helper that builds one), the ``reason`` argument of
    ``contracts.SchemaInvalid``, and any ``code = "..."`` class attribute --
    belongs to exactly one declared table, and its SPELLING says which:

    * ``blocked:<name>``      -> ``types.BLOCK_CODES``
    * ``<lower-with-hyphens>`` -> ``contracts.SCHEMA_REASONS``
    * ``UPPER_SNAKE_CASE``     -> ``types.FAILURE_CODES``

    The scan reads keyword arguments as well as positional ones, resolves a
    module-level ``NAME = "LITERAL"`` constant to its literal, and walks the
    package with ``rglob`` so a later wave's subpackage is not invisible. Each of
    those three was a hole: ``LoopError(code="X")``, ``_fail(CODE, ...)`` and a
    file one directory down all used to yield the empty set, which is the same
    answer the scan gives for a module that raises nothing.

    It also checks the other direction: a member of a table that no call site in
    the package reaches is either newly declared and unraisable, or a typo, and
    the only way to tell is to say which in :data:`UNREACHED`.
    """

    #: (module stem, callable name) -> index of the argument carrying the token,
    #: for every constructor of a wave-0 exception. ``_fail`` appears in three
    #: modules with two different signatures, which is why the key is a pair.
    TOKEN_ARGUMENT = {
        ("types", "LoopError"): 0,
        ("types", "_fail"): 0,
        # ``types``' validation helpers take the code they raise with as their
        # third argument, which is how RUN_ID_INVALID and PIN_INVALID reach a
        # receipt without ever appearing beside ``_fail``.
        ("types", "_identifier"): 2,
        ("types", "_relative"): 2,
        ("types", "_digests"): 2,
        ("standard", "StandardInvalid"): 0,
        ("custody", "CustodyMismatch"): 0,
        ("custody", "CredentialInOutput"): 0,
        ("custody", "WriteOnceViolation"): 0,
        ("custody", "CustodyFinding"): 0,
        ("receipts", "ReceiptError"): 0,
        ("receipts", "SecretInReceipt"): None,     # code is a literal in its body
        ("publish", "PublishError"): 0,
        ("contracts", "SchemaInvalid"): 1,
        ("contracts", "_fail"): 1,
        ("contracts", "ContractError"): 0,
        # W1 modules, folded into the tables by the wave-1 integrator with the
        # argument position each author asked for.
        # W5-DRIVER (tools/auto_loop.py). ``_fail`` is its own one-line
        # constructor and ``CustodyMismatch`` is custody's, raised here so that
        # a custody halt at CYCLE_OPEN or IMPORT carries custody's own code.
        ("auto_loop", "_fail"): 0,
        ("auto_loop", "CustodyMismatch"): 0,
        # PREFLIGHT's local ``refuse``: it writes the refused report before it
        # returns ``_fail(code, detail)``, so the literal is at ITS call sites.
        ("auto_loop", "refuse"): 0,
        ("seats", "_fail"): 0,
        ("seats", "SeatsRefused"): 0,
        ("surface", "SurfaceInvalid"): 0,
        ("obligations", "_refuse"): 0,
        ("obligations", "ObligationsError"): 0,
        ("graph", "GraphError"): 0,
        ("steps", "StepError"): 0,
        # ``StickyHalt(code, detail)`` re-raises the halted receipt's OWN code,
        # so its first argument is a variable at every call site; it is listed
        # for the one literal fallback the resume plan carries.
        ("steps", "StickyHalt"): 0,
        ("synthetic", "SyntheticError"): 0,
        # W2 modules, folded in by the wave-2 integrator with the argument
        # position each author asked for. ``markprep`` raises through module
        # constants rather than literals, so its NEW_CODES table is folded in by
        # key and the scan finds the constants through ``_module_constants``.
        ("packs", "_refuse"): 0,
        ("packs", "PackError"): 0,
        ("packs", "BaselineNotFirst"): None,   # code is a literal in its body
        ("roles", "_fail"): 0,
        ("roles", "RoleRefused"): 0,
        # ``ProviderArmEnded(code, detail)`` re-raises the transport's OWN code,
        # so its first argument is a variable at every call site.
        ("roles", "ProviderArmEnded"): 0,
        ("markprep", "MarkprepError"): 0,
        ("markprep", "BaselineNotFirst"): 0,
        ("markprep", "BaselineSealBroken"): 0,
        ("decide", "DecisionRefused"): 0,
        # W3 modules, folded in by the wave-3 integrator. ``audits`` declares an
        # empty NEW_CODES: every refusal it can raise is one ``types`` already
        # owns, and both of them are config refusals.
        ("audits", "_fail"): 0,
        ("audits", "AuditError"): 0,
        # ``report`` raises two shapes and neither code is its own: a ceiling or
        # pin refusal is ``custody``'s, and a malformed input is ``standard``'s.
        ("report", "ReportRefused"): 0,
        ("report", "StandardInvalid"): 0,
        # ``trial`` raises through module constants rather than literals, so the
        # scan finds them through ``_module_constants``.
        ("trial", "_refuse"): 0,
        ("trial", "TrialRefused"): 0,
        ("trial", "ReopenRefused"): None,   # code is a literal in its body
        # W4 modules, folded in by the wave-4 integrator. ``reader`` raises one
        # shape through module constants; ``marker`` raises through a ``_refuse``
        # helper whose first argument is the code.
        ("reader", "ReaderError"): 0,
        ("marker", "_refuse"): 0,
        ("marker", "MarkerRefused"): 0,
    }

    #: The keyword spelling of each argument index, so ``LoopError(code="X")``
    #: and ``SchemaInvalid(role, reason="y")`` are read like their positional forms.
    KEYWORD_FOR_INDEX = {0: "code", 1: "reason", 2: "code"}

    #: The modules whose codes the tables are declared complete for. A module
    #: absent from this tuple is being written in another wave right now: its
    #: tokens are still checked for spelling, and that wave's integrator folds
    #: its codes into ``FAILURE_CODES`` and adds its stem here in the same commit
    #: (O9). Listing the frontier is the honest alternative to a scan that goes
    #: red whenever a sibling agent saves a file.
    #:
    #: After wave 2 this was all sixteen modules with an empty frontier; wave 3
    #: adds ``audits`` and ``report`` (both with an empty NEW_CODES: every refusal
    #: either raises is one ``types`` already owns) and ``trial`` (five codes,
    #: folded into ``FAILURE_CODES`` in the same pass). A module added without its codes fails
    #: ``test_every_module_of_the_package_is_folded_in``.
    FOLDED_IN = ("types", "standard", "contracts", "custody", "receipts", "publish",
                 "seats", "surface", "obligations", "graph", "steps", "synthetic",
                 "packs", "roles", "markprep", "decide", "audits", "report",
                 "trial", "reader", "marker", "auto_loop")

    #: The wave being written now. Its modules' tokens are still checked for
    #: spelling by the scan above; that wave's integrator folds each module's
    #: NEW_CODES into ``FAILURE_CODES`` and moves its stem into ``FOLDED_IN`` in
    #: the commit that lands it (O9). This is the frontier the class docstring
    #: describes - the honest alternative to a scan that goes red whenever a
    #: sibling agent saves a file - and a module in NEITHER tuple still fails
    #: the test below. Wave 2 emptied it; wave 3 (trial, audits, report) refills
    #: it with its own three stems on the day those files land.
    FRONTIER: tuple[str, ...] = ()

    #: Declared codes that no call site in the package reaches yet, each with the
    #: reason it is declared anyway. The test is a SUBSET check: a code that a
    #: later wave starts raising simply stops being unreached and nobody has to
    #: edit this table, but a code added to ``FAILURE_CODES`` that nothing raises
    #: and nobody listed here fails.
    UNREACHED = {
        # Raised by the transport and by runner v2, which the loop records rather
        # than raises: the loop's receipts carry these codes verbatim.
        "HTTP_429": "provider_openai_compat",
        "KEY_MISSING": "provider_openai_compat",
        "TRANSPORT_OR_RESPONSE_ERROR": "provider_openai_compat",
        "SECRET_IN_REQUEST": "provider_openai_compat",
        "CONCURRENCY_LIMIT_CONFLICT": "runner v2's key gate",
        # roles.py raises it, but through ``types.NO_REPLAY`` imported rather
        # than a literal (wave-2 judge finding 2: one owner for the spelling),
        # and this scan reads literals. The raise site is
        # ``roles._claim_coordinate``; ``tests/loop/test_roles.py`` pins it.
        "NO_REPLAY": "runner v2; types owns the spelling and roles imports it",
        # A *reason* recorded on a returned blocked RoleResult beside the
        # transport's own code, never a raise: the route closing a request at
        # its 300 s wall is a delivery fact the record carries (ruling 13), and
        # the block code stays blocked:provider.
        "PROVIDER_GATEWAY_WALL": "roles.py records it on a result, never raises it",
        "NOT_DISPATCHED": "runner v2 / G0",
        "INDETERMINATE": "runner v2",
        "INPUT_NOT_PUBLISHED": "runner v2; publish.py carries it in a detail",
        "PUBLISH_REF_CHANGED": "publish.py carries it in a pending detail",
        "TIMEOUT_NOT_APPLIED": "W1-STEPS, the provider wall-clock check",
        "PROVIDER_REQUEST_FILE_CHANGED": "W1-STEPS",
        "REQUEST_NOT_FROM_PLAN": "W1-STEPS",
        "ARTIFACT_NOT_DERIVED_FROM_DELIVERY": "W1-GRAPH",
        "TRANSPORT_PIN_MISMATCH": "W1-STEPS / PREFLIGHT",
        # Aggregate names a caller records for a set of findings (custody
        # deviation 1), never a per-path or per-call refusal.
        "CUSTODY_MISMATCH": "the aggregate name for a halt",
        "RUNTIME_SOURCE_CHANGED": "the aggregate name for a non-empty verify_pins",
        "PUBLISH_PENDING": "the step ledger's name for a PublishPending result",
        # Later waves own these.
        "UNRESOLVED_STEP": "W1-STEPS",
        "STEP_NONDETERMINISTIC": "W1-STEPS",
        "STEP_TIMEOUT": "W1-STEPS",
        "PLAN_ID_MISMATCH": "W1-STEPS",
        "BUDGET_RAISED": "W1-STEPS / W5",
        "BASELINE_NOT_FIRST": "W2-MARKPREP, G8",
        "FAMILY_COUNT_INSUFFICIENT": "seats raises it through a module constant",
        "NEW_PREREGISTRATION_REQUIRED": "W5",
        "REOPEN_REFUSED": "W2, G11",
        "STOP_REASON_UNKNOWN": "W2-DECIDE",
        "PATH_INVALID": "declared for W1's own path checks",
        # Recorded on a receipt rather than raised: a step body that crashed
        # with no stable code gets this as its receipt's failure_code, which is
        # the point of it (steps._classify returns it, nothing raises it).
        "STEP_BODY_FAILED": "steps._classify writes it onto a FAILED receipt",
        # Raised through a helper this scan deliberately does not follow.
        "SECRET_IN_RECEIPT": "receipts.SecretInReceipt sets it in its own body",
        "SCORING_KEY_FORBIDDEN": "contracts.ScoringKeyForbidden sets it as a class "
                                 "attribute, which the scan reads under its own rule",
    }

    #: Members of ``SCHEMA_REASONS`` no ``_fail`` call names directly.
    UNREACHED_REASONS = {
        reason: "carried by contracts._JSONSCHEMA_REASONS, keyed by the jsonschema "
                "validator that produced the error"
        for reason in ("missing-field", "unexpected-field", "wrong-type", "not-in-enum",
                       "empty-field", "too-few-items", "not-unique")
    }

    UPPER = re.compile(r"[A-Z][A-Z0-9_]*\Z")
    LOWER = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")

    # -- the scan ---------------------------------------------------------- #

    @staticmethod
    def _module_constants(tree: ast.Module) -> dict[str, str]:
        """Module-level ``NAME = "LITERAL"`` bindings, so ``_fail(NAME)`` is read."""

        constants: dict[str, str] = {}
        for node in tree.body:
            targets = ([node.target] if isinstance(node, ast.AnnAssign)
                       else node.targets if isinstance(node, ast.Assign) else [])
            if not isinstance(getattr(node, "value", None), ast.Constant):
                continue
            if not isinstance(node.value.value, str):
                continue
            for target in targets:
                if isinstance(target, ast.Name):
                    constants[target.id] = node.value.value
        return constants

    def tokens_in(self, stem: str, source: str) -> set[str]:
        tree = ast.parse(source)
        constants = self._module_constants(tree)
        tokens: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                tokens.update(self._from_call(stem, node, constants))
            elif isinstance(node, (ast.AnnAssign, ast.Assign)):
                tokens.update(self._from_assign(node))
        return tokens

    def collect(self) -> dict[str, set[str]]:
        """Every stable token the package can put on an exception, by module.

        ``tools/auto_loop.py`` is walked beside the package: W5-DRIVER lives
        outside ``src/minireason/loop/`` by the wave plan's own path, and a
        scan that stopped at the package boundary would let the driver's codes
        into ``FAILURE_CODES`` unreached and unchecked. It is the one file
        outside the package this scan reads, and it is named here rather than
        globbed so a second tool cannot join it silently.
        """

        found: dict[str, set[str]] = {}
        sources = sorted(PACKAGE.rglob("*.py")) + [DRIVER_SOURCE]
        self.assertTrue(sources)
        for source in sources:
            found.setdefault(source.stem, set()).update(
                self.tokens_in(source.stem, source.read_text(encoding="utf-8")))
        return found

    def _from_call(self, stem: str, node: ast.Call,
                   constants: dict[str, str]) -> set[str]:
        func = node.func
        if isinstance(func, ast.Name):
            name = func.id
        elif isinstance(func, ast.Attribute):
            name = func.attr
            # ``LoopError.__init__(self, code, detail)`` and
            # ``super().__init__(code, detail)`` both name the base's ctor.
            if name == "__init__":
                index = 1 if isinstance(func.value, ast.Name) else 0
                return self._literals(node, index, constants)
        else:
            return set()
        index = self.TOKEN_ARGUMENT.get((stem, name), "absent")
        if index == "absent" or index is None:
            return set()
        return self._literals(node, index, constants)

    def _literals(self, node: ast.Call, index: int,
                  constants: dict[str, str]) -> set[str]:
        found: set[str] = set()
        candidates = [node.args[index]] if index < len(node.args) else []
        keyword = self.KEYWORD_FOR_INDEX.get(index)
        if keyword is not None:
            candidates += [kw.value for kw in node.keywords if kw.arg == keyword]
        for value in candidates:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                found.add(value.value)
            elif isinstance(value, ast.Name) and value.id in constants:
                found.add(constants[value.id])
        return found

    @staticmethod
    def _from_assign(node) -> set[str]:
        targets = ([node.target] if isinstance(node, ast.AnnAssign) else node.targets)
        names = {t.id for t in targets if isinstance(t, ast.Name)}
        if "code" not in names or not isinstance(node.value, ast.Constant):
            return set()
        return {node.value.value} if isinstance(node.value.value, str) else set()

    # -- what the scan must find ------------------------------------------- #

    def test_the_scan_finds_tokens_in_every_module_that_raises(self):
        found = self.collect()
        for stem in self.FOLDED_IN:
            with self.subTest(module=stem):
                self.assertTrue(found[stem], f"{stem}.py: the scan found no token")

    def test_the_scan_reads_a_keyword_argument_and_a_module_level_constant(self):
        source = (
            'CODE = "PLAN_ID_MISMATCH"\n'
            'def f():\n'
            '    raise LoopError(code="STEP_TIMEOUT")\n'
            'def g():\n'
            '    raise LoopError(CODE)\n'
            'def h():\n'
            '    return _fail(code="RUN_ID_INVALID", detail="x")\n'
        )
        self.assertEqual(self.tokens_in("types", source),
                         {"STEP_TIMEOUT", "PLAN_ID_MISMATCH", "RUN_ID_INVALID"})
        reason = 'def f():\n    raise SchemaInvalid("critic", reason="not-json", message="x")\n'
        self.assertEqual(self.tokens_in("contracts", reason), {"not-json"})

    def test_the_scan_reaches_a_file_below_the_package_directory(self):
        self.assertNotEqual(sorted(PACKAGE.rglob("*.py")), [])
        self.assertEqual(sorted(PACKAGE.rglob("*.py")),
                         sorted(set(PACKAGE.rglob("*.py"))))
        # rglob is a superset of glob, which is the whole point of using it.
        self.assertLessEqual(set(PACKAGE.glob("*.py")), set(PACKAGE.rglob("*.py")))

    def test_every_module_of_the_package_is_folded_in(self):
        """The frontier is empty after wave 1: every module's codes are declared."""

        self.assertTrue(DRIVER_SOURCE.is_file(), DRIVER_SOURCE)
        stems = ({path.stem for path in PACKAGE.rglob("*.py")}
                 | {DRIVER_SOURCE.stem}) - {"__init__"}
        self.assertEqual(stems - set(self.FOLDED_IN) - set(self.FRONTIER), set(),
                         "a module of the package declares none of its codes; fold its "
                         "NEW_CODES into FAILURE_CODES and add its stem to FOLDED_IN")
        self.assertEqual(set(self.FOLDED_IN) & set(self.FRONTIER), set(),
                         "a module is either folded in or on the frontier, never both")

    def test_every_stable_token_in_the_package_is_in_exactly_one_declared_table(self):
        schema_reasons = set(contracts.SCHEMA_REASONS)
        tables = {"BLOCK_CODES": set(BLOCK_CODES),
                  "SCHEMA_REASONS": schema_reasons,
                  "FAILURE_CODES": set(FAILURE_CODES),
                  "OUTCOME_CODES": set(loop_types.OUTCOME_CODES)}
        for stem, tokens in self.collect().items():
            for token in sorted(tokens):
                with self.subTest(module=stem, token=token):
                    if token.startswith(loop_types.BLOCK_CODE_PREFIX):
                        wanted = "BLOCK_CODES"
                    elif token in tables["OUTCOME_CODES"]:
                        # An UPPER_SNAKE token that names what the loop DID.
                        # Spelling cannot tell an outcome from a refusal, so the
                        # small closed table does, and disjointness is asserted
                        # below like every other pair.
                        wanted = "OUTCOME_CODES"
                    elif self.UPPER.fullmatch(token):
                        wanted = "FAILURE_CODES"
                    elif self.LOWER.fullmatch(token):
                        wanted = "SCHEMA_REASONS"
                    else:
                        self.fail(f"{stem}.py: {token!r} is spelled like no declared table")
                    if stem not in self.FOLDED_IN:
                        continue          # another wave's module, not yet folded in
                    self.assertIn(token, tables[wanted],
                                  f"{stem}.py: {token!r} is missing from {wanted}")
                    for other, members in tables.items():
                        if other != wanted:
                            self.assertNotIn(token, members,
                                             f"{token!r} is in {other} as well as {wanted}")

    def test_every_new_codes_table_a_later_wave_module_declares_is_folded_in(self):
        """O9's other direction: a module's own NEW_CODES table is the contract."""

        for stem in ("seats", "surface", "obligations", "graph", "steps", "synthetic",
                     "packs", "roles", "markprep", "decide"):
            module = importlib.import_module(f"minireason.loop.{stem}")
            for code, reason in module.NEW_CODES.items():
                with self.subTest(module=stem, code=code):
                    self.assertRegex(code, r"\A[A-Z][A-Z0-9_]*\Z")
                    self.assertTrue(reason.strip(), "every new code carries its reason")
                    declared = (code in FAILURE_CODES) ^ (code in loop_types.OUTCOME_CODES)
                    self.assertTrue(
                        declared,
                        f"{stem}.NEW_CODES[{code!r}] is in neither table, or in both")

    def test_every_declared_code_is_reached_by_the_package_or_allow_listed(self):
        reached: set[str] = set()
        for stem, tokens in self.collect().items():
            if stem in self.FOLDED_IN:
                reached |= tokens
        for table, declared, allowed in (
            ("FAILURE_CODES", set(FAILURE_CODES), self.UNREACHED),
            ("SCHEMA_REASONS", set(contracts.SCHEMA_REASONS), self.UNREACHED_REASONS),
        ):
            with self.subTest(table=table):
                unreached = declared - reached
                self.assertLessEqual(
                    unreached, set(allowed),
                    f"{table}: {sorted(unreached - set(allowed))} is declared and "
                    "nothing in the package raises it; raise it, or list it in "
                    "UNREACHED with the reason it is declared anyway")
                self.assertLessEqual(set(allowed), declared,
                                     f"{table}: the allow-list names a code the table "
                                     "does not declare")

    def test_no_module_of_this_package_carries_an_invalid_escape_sequence(self):
        """The loop's own half of a repository-level defect.

        On a cold ``.pyc`` cache, ``python3 -W error -c "import
        minireason.loop.contracts"`` fails with ``SyntaxError: invalid escape
        sequence '\\s'`` - not from this package, but from the frozen
        ``src/minireason/use_relation_h005.py``, whose docstring at line 304
        writes ``"records"\\s*:\\s*[`` inside a non-raw string. Ten loop
        modules reach it through the import chain (contracts, standard, surface,
        seats, graph, synthetic, packs, roles, markprep, decide); types,
        custody, receipts, obligations, publish and steps import clean.

        That file is a published instrument: editing it bumps its
        ``source_identity`` and invalidates every frozen plan that pins it, so
        the repair is the SRC-003 erratum's and not this integration's. What is
        in scope here is that the loop package adds nothing to the pile, which
        is what this test holds: every module of ``minireason.loop`` compiles
        with warnings promoted to errors.
        """

        import warnings

        for path in sorted(PACKAGE.rglob("*.py")):
            with self.subTest(module=path.name):
                with warnings.catch_warnings():
                    warnings.simplefilter("error")
                    try:
                        compile(path.read_text(encoding="utf-8"), str(path), "exec")
                    except SyntaxWarning as warning:      # pragma: no cover
                        self.fail(f"{path.name}: {warning}")

    def test_the_http_status_family_is_declared_and_bounded(self):
        """Wave-1 integration decision 42(b): one parameterised failure family.

        The transport raises ``HTTP_<status>`` for every status it meets, so a
        receipt could carry ``HTTP_503`` while the table named only
        ``HTTP_429``. The family is declared, and it is a family and not a
        licence: three digits, a real status class, nothing else.
        """

        for code in ("HTTP_429", "HTTP_503", "HTTP_200", "HTTP_100"):
            with self.subTest(code=code):
                self.assertTrue(loop_types.is_failure_code(code))
        for code in ("HTTP_999", "HTTP_4290", "HTTP_", "HTTP_42", "HTTPS_429",
                     "HTTP_OK", ""):
            with self.subTest(code=code):
                self.assertFalse(loop_types.is_failure_code(code))
        self.assertIn("HTTP_429", FAILURE_CODES)
        self.assertNotIn("HTTP_503", FAILURE_CODES)
        self.assertEqual(loop_types.HTTP_STATUS_PREFIX, "HTTP_")

    def test_the_custody_table_is_a_slice_of_the_failure_table_not_a_rival(self):
        self.assertLessEqual(set(custody.CUSTODY_CODES), set(FAILURE_CODES))

    def test_no_module_retypes_the_blocked_prefix(self):
        """REVIEW-PREREG PR-12: one owner for the block vocabulary, one spelling.

        ``types`` owns ``BLOCK_CODES`` (ten, prefixed), ``CEILING_BLOCK_REASONS``
        (nine, bare, in the ceiling's order) and ``block_code(reason)``, which is
        the only way to build a member and which refuses a reason the table does
        not carry. A module that wrote ``"blocked:schema"`` out would be a second
        spelling, and a rename in one of the two would be silent.
        """

        for path in sorted(PACKAGE.rglob("*.py")):
            if path.name == "types.py":
                continue
            source = path.read_text(encoding="utf-8")
            for line in source.splitlines():
                stripped = line.lstrip()
                if stripped.startswith("#") or "blocked:" not in line:
                    continue
                with self.subTest(module=path.name, line=line.strip()[:70]):
                    self.assertNotIn('"blocked:', line,
                                     "build it with types.block_code(reason)")
                    self.assertNotIn("'blocked:", line,
                                     "build it with types.block_code(reason)")

    def test_the_two_block_tables_agree_except_for_the_one_extra(self):
        prefixed = {loop_types.BLOCK_CODE_PREFIX + reason
                    for reason in loop_types.CEILING_BLOCK_REASONS}
        self.assertEqual(prefixed | {"blocked:constitution"}, set(BLOCK_CODES))
        self.assertEqual(len(loop_types.CEILING_BLOCK_REASONS), 9)
        self.assertEqual(len(BLOCK_CODES), 10)
        for reason in loop_types.CEILING_BLOCK_REASONS:
            with self.subTest(reason=reason):
                self.assertIn(loop_types.block_code(reason), BLOCK_CODES)
        with self.assertRaises(LoopError) as caught:
            loop_types.block_code("not-a-reason")
        self.assertEqual(caught.exception.code, "BLOCK_CODE_UNKNOWN")

    def test_the_three_tables_are_pairwise_disjoint(self):
        block, schema = set(BLOCK_CODES), set(contracts.SCHEMA_REASONS)
        failure = set(FAILURE_CODES)
        self.assertEqual(block & failure, set())
        self.assertEqual(block & schema, set())
        self.assertEqual(schema & failure, set())

    def test_every_wave_zero_exception_is_a_loop_error_that_keeps_its_old_base(self):
        for cls, old_base in (
            (contracts.ContractError, ValueError),
            (contracts.SchemaInvalid, ValueError),
            (contracts.ScoringKeyForbidden, ValueError),
            (standard.StandardInvalid, ValueError),
            (custody.CustodyMismatch, RuntimeError),
            (custody.CredentialInOutput, ValueError),
            (custody.WriteOnceViolation, FileExistsError),
            (receipts.ReceiptError, RuntimeError),
            (receipts.SecretInReceipt, RuntimeError),
            (publish.PublishError, RuntimeError),
            (publish.GitCommandFailed, RuntimeError),
            (publish.HistoryRewriteRefused, RuntimeError),
            (publish.CredentialInStagedDiff, RuntimeError),
            (publish.PublishNotConverging, RuntimeError),
        ):
            with self.subTest(exception=cls.__name__):
                self.assertTrue(issubclass(cls, LoopError))
                self.assertTrue(issubclass(cls, old_base))

    def test_types_imports_no_sibling_so_it_can_be_the_root_of_the_graph(self):
        tree = ast.parse((PACKAGE / "types.py").read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                self.assertFalse(node.module.startswith("minireason.loop"), node.module)
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertFalse(alias.name.startswith("minireason.loop"), alias.name)


class CustodyReportFromFindings(unittest.TestCase):
    """Wave-0 integration decision 8: one adapter, so W1-STEPS has one way."""

    class Finding:
        def __init__(self, code: str, path: str) -> None:
            self.code, self.path = code, path

    def test_an_empty_result_is_the_only_thing_that_verifies(self):
        report = CustodyReport.from_findings([])
        self.assertTrue(report.verified)
        self.assertEqual(report.checks, ())
        self.assertEqual(report.as_dict(), {"verified": True, "checks": []})

    def test_findings_become_one_stable_code_each_in_order(self):
        findings = [self.Finding("SOURCE_PIN_MISMATCH", "CEILING.md"),
                    self.Finding("SOURCE_PIN_MISSING", "tools/runner.py"),
                    self.Finding("SOURCE_PIN_MISMATCH", "tools/other.py")]
        report = CustodyReport.from_findings(findings)
        self.assertFalse(report.verified)
        self.assertEqual(report.checks, ("SOURCE_PIN_MISMATCH", "SOURCE_PIN_MISSING",
                                         "SOURCE_PIN_MISMATCH"))
        for code in report.checks:
            self.assertIn(code, FAILURE_CODES)

    def test_the_real_findings_of_verify_pins_go_straight_in(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            (repo / "tools").mkdir(parents=True)
            (repo / "tools" / "runner.py").write_bytes(b"one\n")
            plan = {"pins": custody.pins(repo, ["tools/runner.py"])}
            self.assertTrue(CustodyReport.from_findings(
                custody.verify_pins(plan, repo)).verified)
            (repo / "tools" / "runner.py").write_bytes(b"two\n")
            report = CustodyReport.from_findings(custody.verify_pins(plan, repo))
            self.assertFalse(report.verified)
            self.assertEqual(report.checks, ("SOURCE_PIN_MISMATCH",))
            receipt = StepReceipt.build(
                loop_plan_id=PLAN, index=3, kind="IMPORT",
                started_utc="2026-09-14T09:00:00+00:00", status="HALTED",
                failure_code="CUSTODY_MISMATCH", custody=report)
            self.assertEqual(receipt.as_dict()["custody"],
                             {"verified": False, "checks": ["SOURCE_PIN_MISMATCH"]})

    def test_a_bare_string_is_accepted_and_a_codeless_object_is_refused(self):
        self.assertEqual(CustodyReport.from_findings(["SOURCE_PIN_MISSING"]).checks,
                         ("SOURCE_PIN_MISSING",))
        with self.assertRaises(LoopError) as caught:
            CustodyReport.from_findings([object()])
        self.assertEqual(caught.exception.code, "STEP_RECEIPT_INVALID")


class ConfigLoading(unittest.TestCase):

    def test_defaults_are_the_design_declared_ones(self):
        config = LoopConfig.from_mapping(CONFIG)
        self.assertEqual(config.seats, SeatsConfig())
        self.assertEqual(config.seats.min_judge_families, 2)
        self.assertEqual(config.seats.paraphrase_n, 2)
        self.assertEqual(config.seats.schema_repair_budget, 0)
        self.assertEqual(config.contrast, ContrastConfig(attached=False))
        self.assertEqual(config.timeouts.git_seconds, 90)
        self.assertEqual(config.max_per_key, 5)
        self.assertIsNone(config.publish_ref)
        self.assertEqual(config.provider_mode, "offline",
                         "a config that declares no spending mode does not spend")
        self.assertEqual(config.as_dict()["schema"], CONFIG_SCHEMA)

    def test_invalid_values_are_refused_with_a_reason(self):
        cases = {
            "cycle_budget": (0, "CONFIG_INVALID_VALUE"),
            "max_calls": (-1, "CONFIG_INVALID_VALUE"),
            "max_per_key": (6, "CONFIG_INVALID_VALUE"),
            "provider_mode": ("dry", "CONFIG_INVALID_VALUE"),
            "publish_ref": ("origin", "CONFIG_INVALID_VALUE"),
            "run_id": ("../escape", "RUN_ID_INVALID"),
            "runner": ("/etc/passwd", "CONFIG_INVALID_VALUE"),
            "occurrences": ([], "CONFIG_INVALID_VALUE"),
            "reading_set": (["a", "a"], "CONFIG_INVALID_VALUE"),
            "graph_root": ("../graph", "CONFIG_INVALID_VALUE"),
        }
        for key, (value, code) in cases.items():
            with self.subTest(key=key):
                with self.assertRaises(LoopError) as caught:
                    LoopConfig.from_mapping(dict(CONFIG, **{key: value}))
                self.assertEqual(caught.exception.code, code)

    def test_a_boolean_is_not_a_whole_number(self):
        with self.assertRaises(LoopError):
            LoopConfig.from_mapping(dict(CONFIG, cycle_budget=True))

    def test_a_detached_contrast_leg_names_no_study(self):
        with self.assertRaises(LoopError):
            ContrastConfig.from_mapping({"attached": False, "study": "C001"})
        with self.assertRaises(LoopError):
            ContrastConfig.from_mapping({"attached": True, "study": "C001"})
        leg = ContrastConfig.from_mapping(
            {"attached": True, "study": "C001", "occurrences": ["experiments/c001/o1"]})
        self.assertEqual(leg.occurrences, ("experiments/c001/o1",))

    def test_audit_thresholds_have_no_defaults(self):
        with self.assertRaises(LoopError):
            AuditConfig.from_mapping({"period": 1, "judge_err_max": 0.1})
        with self.assertRaises(LoopError):
            AuditConfig.from_mapping({"period": 1, "judge_err_max": 2.0, "streak_max": 1})

    def test_the_audit_thresholds_each_carry_an_account(self):
        """S6: a margin with no account is a threshold nobody can attack."""

        for missing in ("judge_err_max_account", "streak_max_account"):
            with self.subTest(missing=missing):
                block = {k: v for k, v in CONFIG["audit"].items() if k != missing}
                with self.assertRaises(LoopError) as caught:
                    AuditConfig.from_mapping(block)
                self.assertEqual(caught.exception.code, "CONFIG_MISSING_KEY")
                self.assertIn(missing, caught.exception.detail)
        for empty in ("judge_err_max_account", "streak_max_account"):
            with self.subTest(empty=empty):
                with self.assertRaises(LoopError) as caught:
                    AuditConfig.from_mapping({**CONFIG["audit"], empty: "   "})
                self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")
        audit = AuditConfig.from_mapping(CONFIG["audit"])
        rendered = audit.as_dict()
        self.assertEqual(rendered["judge_err_max_account"],
                         CONFIG["audit"]["judge_err_max_account"])
        self.assertEqual(rendered["streak_max_account"],
                         CONFIG["audit"]["streak_max_account"])
        # The account travels inside the config, and therefore inside the plan id.
        self.assertIn(rendered["judge_err_max_account"],
                      LoopConfig.from_mapping(CONFIG).canonical_bytes().decode("utf-8"))
        self.assertNotEqual(
            loop_plan_id(CONFIG, PINS),
            loop_plan_id(dict(CONFIG, audit={**CONFIG["audit"],
                                             "streak_max_account": "because."}), PINS))

    def test_the_seat_ranges_are_the_ranges_the_standard_admits(self):
        """B3: the two owners of a guard parameter had disjoint ranges."""

        for value, code in ((0, "CONFIG_INVALID_VALUE"), (1, None), (2, None)):
            with self.subTest(paraphrase_n=value):
                if code is None:
                    self.assertEqual(
                        SeatsConfig.from_mapping({"paraphrase_n": value}).paraphrase_n,
                        value)
                else:
                    with self.assertRaises(LoopError) as caught:
                        SeatsConfig.from_mapping({"paraphrase_n": value})
                    self.assertEqual(caught.exception.code, code)
        self.assertEqual(
            SeatsConfig.from_mapping({"schema_repair_budget": 0}).schema_repair_budget, 0)
        with self.assertRaises(LoopError) as caught:
            SeatsConfig.from_mapping({"schema_repair_budget": 1})
        self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")
        with self.assertRaises(LoopError):
            SeatsConfig.from_mapping({"min_judge_families": 1})
        # Every value this loader admits, the standard admits too: the two
        # owners' ranges are no longer disjoint at either end.
        shared = sorted(set(standard._INT_PARAMS) & set(SeatsConfig._OPTIONAL))
        self.assertEqual(shared, ["min_judge_families", "paraphrase_n",
                                  "schema_repair_budget"])
        for key in shared:
            low, high = standard._INT_PARAMS[key]
            with self.subTest(parameter=key):
                for value in range(low, high + 1):
                    try:
                        SeatsConfig.from_mapping({key: value})
                    except LoopError:
                        continue          # narrower here is safe; wider is not
                    standard._validate_params({**standard.GUARD_PARAMETERS, key: value})

    def test_the_default_config_reconciles_with_the_standard_and_divergence_is_refused(self):
        """B3: PREFLIGHT's reconciliation, and each way a config can contradict it."""

        config = LoopConfig.from_mapping(CONFIG)
        self.assertIsNone(standard.assert_config_matches_standard(
            config.seats.as_dict(), config.reopen_reasons))
        self.assertIsNone(standard.assert_config_matches_standard(
            SeatsConfig().as_dict(), standard.REOPEN_REASONS))
        for key in ("min_judge_families", "paraphrase_n", "schema_repair_budget"):
            with self.subTest(parameter=key):
                diverged = dict(config.seats.as_dict())
                diverged[key] = standard.GUARD_PARAMETERS[key] + 1
                with self.assertRaises(standard.StandardInvalid) as caught:
                    standard.assert_config_matches_standard(diverged, config.reopen_reasons)
                self.assertEqual(caught.exception.code, "GUARD_PARAMETER_INVALID")
                self.assertIn(key, str(caught.exception))
        with self.assertRaises(standard.StandardInvalid) as caught:
            standard.assert_config_matches_standard(
                dict(config.seats.as_dict(), judges=["a", "b", "c"]), ())
        self.assertEqual(caught.exception.code, "GUARD_PARAMETER_INVALID")
        for reasons in (["because-i-said-so"], ["new-material", "try-again"]):
            with self.subTest(reopen_reasons=reasons):
                with self.assertRaises(standard.StandardInvalid) as caught:
                    standard.assert_config_matches_standard({}, reasons)
                self.assertEqual(caught.exception.code, "REOPEN_REASON_UNKNOWN")
        # A config the loader accepts can still contradict the standard: that is
        # the whole point of the reconciliation, and why PREFLIGHT must run it.
        loaded = LoopConfig.from_mapping(dict(CONFIG, reopen_reasons=["new-material"]))
        self.assertIsNone(standard.assert_config_matches_standard(
            loaded.seats.as_dict(), loaded.reopen_reasons))

    def test_timeouts_name_only_declared_step_kinds(self):
        with self.assertRaises(LoopError):
            TimeoutsConfig.from_mapping({"step_seconds": {"DISPATCH": 10}})
        timeouts = TimeoutsConfig.from_mapping({"step_seconds": {"SEND": 600}})
        self.assertEqual(dict(timeouts.step_seconds), {"SEND": 600})

    def test_seat_names_may_be_absent_and_judges_must_meet_the_family_floor(self):
        seats = SeatsConfig.from_mapping({})
        self.assertEqual((seats.critic, seats.defender, seats.variator, seats.judges),
                         (None, None, None, ()))
        with self.assertRaises(LoopError):
            SeatsConfig.from_mapping({"judges": ["one"]})
        with self.assertRaises(LoopError):
            SeatsConfig.from_mapping({"judges": ["one", "one"]})
        self.assertEqual(SeatsConfig.from_mapping({"judges": ["a", "b"]}).judges, ("a", "b"))

    def test_a_null_or_malformed_pin_is_refused(self):
        config = LoopConfig.from_mapping(CONFIG)
        for pins in ({"a.py": None}, {"a.py": "short"}, {"a.py": "A" * 64},
                     {"../a.py": "a" * 64}, {"/a.py": "a" * 64}):
            with self.subTest(pins=pins):
                with self.assertRaises(LoopError) as caught:
                    loop_plan_id(config, dict(PINS, **pins))
                self.assertEqual(caught.exception.code, "PIN_INVALID")

    # -- item 14: two spellings of one path may not fold into one identity -- #

    def test_item14_a_pin_map_with_two_spellings_of_one_path_is_refused(self):
        """Item 14: ``{"src/a.py": H1, "src//a.py": H2}`` used to mint one id.

        ``_relative`` normalises a key, so the second spelling overwrote the
        first: the identity then depended on pin ORDER, and a changed pin could
        leave it unchanged. Both doors - the plan identity and a receipt's
        ``inputs_sha256`` - refuse the collision now, each with its own code.
        """

        config = LoopConfig.from_mapping(CONFIG)
        for spelling in ("./src/minireason/use_relation_h005.py",
                         "src//minireason/use_relation_h005.py",
                         "src/./minireason/use_relation_h005.py"):
            with self.subTest(spelling=spelling):
                with self.assertRaises(LoopError) as caught:
                    loop_plan_id(config, dict(PINS, **{spelling: "d" * 64}))
                self.assertEqual(caught.exception.code, "PIN_INVALID")
                with self.assertRaises(LoopError) as caught:
                    StepReceipt.key(PLAN, "SEND", 1, None,
                                    {"in/x.json": "1" * 64, spelling: "2" * 64,
                                     "src/minireason/use_relation_h005.py": "3" * 64})
                self.assertEqual(caught.exception.code, "STEP_RECEIPT_INVALID")

    def test_item14_insertion_order_never_changes_an_accepted_identity(self):
        """Item 14, the other direction: every accepted map is order-blind."""

        config = LoopConfig.from_mapping(CONFIG)
        forwards = loop_plan_id(config, dict(PINS))
        backwards = loop_plan_id(config, dict(reversed(list(PINS.items()))))
        self.assertEqual(forwards, backwards)
        # ... and a changed digest changes the id, at every pin.
        for path in PINS:
            with self.subTest(path=path):
                moved = dict(PINS, **{path: "9" * 64})
                self.assertNotEqual(forwards, loop_plan_id(config, moved))

    def test_item18_the_plan_identity_requires_every_fixed_pin(self):
        """Item 18: PINNED_SOURCE_PATHS is the fixed part of the identity."""

        config = LoopConfig.from_mapping(CONFIG)
        for path in PINNED_SOURCE_PATHS:
            with self.subTest(missing=path):
                short = {k: v for k, v in PINS.items() if k != path}
                with self.assertRaises(LoopError) as caught:
                    loop_plan_id(config, short)
                self.assertEqual(caught.exception.code, "PIN_INVALID")
                self.assertIn(path, caught.exception.detail)
        self.assertTrue(loop_plan_id(config, PINS))

    def test_item19_a_config_path_that_cannot_be_read_is_a_loop_error(self):
        """Item 19: ``LoopConfig.load`` used to raise a bare ``OSError``."""

        with tempfile.TemporaryDirectory() as directory:
            for path in (Path(directory) / "absent.json", Path(directory)):
                with self.subTest(path=path):
                    with self.assertRaises(LoopError) as caught:
                        LoopConfig.load(path)
                    self.assertEqual(caught.exception.code, "CONFIG_NOT_FOUND")
        self.assertIn("CONFIG_NOT_FOUND", FAILURE_CODES)

    def test_item19_a_relative_path_is_spelled_one_way_only(self):
        """Item 19: ``.`` and whitespace-padded components folded away in silence."""

        for bad in (".", "./src/a.py", "src/./a.py", " src/a.py", "src/a .py/ b",
                    "src/a.py/."):
            with self.subTest(path=bad):
                with self.assertRaises(LoopError) as caught:
                    loop_types._relative(bad, "pins key", "PIN_INVALID")
                self.assertEqual(caught.exception.code, "PIN_INVALID")
        self.assertEqual(loop_types._relative("src/a.py", "x"), "src/a.py")


class StepReceipts(unittest.TestCase):

    def receipt(self, **overrides):
        fields = dict(loop_plan_id=PLAN, index=6, kind="SEND", cycle=2, wave="wave0001",
                      started_utc="2026-09-14T09:00:00+00:00",
                      inputs_sha256={"experiments/x/plan.json": "1" * 64},
                      finished_utc="2026-09-14T09:01:00+00:00", status="COMPLETE")
        fields.update(overrides)
        return StepReceipt.build(**fields)

    def test_a_receipt_round_trips_through_canonical_json(self):
        receipt = self.receipt()
        again = StepReceipt.from_dict(json.loads(json.dumps(receipt.as_dict())))
        self.assertEqual(receipt, again)
        self.assertEqual(receipt.as_dict()["schema"], STEP_SCHEMA)
        self.assertEqual(receipt.filename, "0006-SEND.json")

    def test_the_step_key_reads_plan_kind_cycle_wave_and_inputs(self):
        base = StepReceipt.key(PLAN, "SEND", 2, "wave0001", {"a": "1" * 64})
        self.assertEqual(base, StepReceipt.key(PLAN, "SEND", 2, "wave0001", {"a": "1" * 64}))
        for changed in (StepReceipt.key("d" * 64, "SEND", 2, "wave0001", {"a": "1" * 64}),
                        StepReceipt.key(PLAN, "READ", 2, "wave0001", {"a": "1" * 64}),
                        StepReceipt.key(PLAN, "SEND", 3, "wave0001", {"a": "1" * 64}),
                        StepReceipt.key(PLAN, "SEND", 2, "wave0002", {"a": "1" * 64}),
                        StepReceipt.key(PLAN, "SEND", 2, "wave0001", {"a": "2" * 64})):
            self.assertNotEqual(base, changed)

    def test_a_receipt_that_misstates_its_own_key_is_refused(self):
        with self.assertRaises(LoopError) as caught:
            StepReceipt(step_key="f" * 64, index=1, kind="SEND", loop_plan_id=PLAN,
                        status="COMPLETE", started_utc="2026-09-14T09:00:00+00:00")
        self.assertEqual(caught.exception.code, "STEP_KEY_MISMATCH")

    def test_spending_must_match_the_design_classification_of_the_kind(self):
        self.assertTrue(self.receipt().spending)
        self.assertFalse(self.receipt(kind="IMPORT", wave=None).spending)
        self.assertTrue(self.receipt(kind="IMPORT", wave=None).replayable)
        with self.assertRaises(LoopError):
            self.receipt(spending=False)
        with self.assertRaises(LoopError):
            self.receipt(kind="IMPORT", wave=None, spending=True)

    def test_a_failed_step_names_its_code_and_a_complete_step_carries_none(self):
        failed = self.receipt(status="FAILED", failure_code="HTTP_429")
        self.assertEqual(failed.as_dict()["failure_code"], "HTTP_429")
        with self.assertRaises(LoopError):
            self.receipt(status="FAILED")
        with self.assertRaises(LoopError):
            self.receipt(failure_code="HTTP_429")
        halted = self.receipt(status="HALTED", failure_code="CUSTODY_MISMATCH",
                              custody=CustodyReport(verified=False,
                                                    checks=("SOURCE_PIN_MISMATCH",)))
        self.assertFalse(halted.custody.verified)
        self.assertEqual(halted.custody.checks, ("SOURCE_PIN_MISMATCH",))

    def test_a_local_time_or_unknown_kind_or_unknown_status_is_refused(self):
        for overrides in ({"started_utc": "2026-09-14T09:00:00+02:00"},
                          {"started_utc": "2026-09-14 09:00:00"},
                          {"kind": "DISPATCH"},
                          {"status": "OK"},
                          {"cycle": 0}):
            with self.subTest(overrides=overrides):
                with self.assertRaises(LoopError):
                    self.receipt(**overrides)

    def test_an_unknown_receipt_key_is_refused_on_read(self):
        raw = self.receipt().as_dict()
        raw["retries"] = 1
        with self.assertRaises(LoopError) as caught:
            StepReceipt.from_dict(raw)
        self.assertEqual(caught.exception.code, "STEP_RECEIPT_INVALID")


class RunLayout(unittest.TestCase):

    def test_run_paths_lays_the_run_out_where_design_4_2_says(self):
        paths = run_paths("/repo", "LOOP-01")
        self.assertIsInstance(paths, RunPaths)
        self.assertEqual(paths.run_root, Path("/repo") / LOOPS_ROOT / "LOOP-01")
        for attribute, name in (("config", "config.json"), ("plan", "plan.json"),
                                ("preregistration", "preregistration.md"),
                                ("obligations", "obligations.json"),
                                ("ceiling", "CEILING.md"), ("preflight", "preflight.json"),
                                ("lock", "run.lock"), ("closing", "CLOSING.md"),
                                ("reading_table", "READING_TABLE.md"),
                                ("comparison", "COMPARISON.md")):
            with self.subTest(attribute=attribute):
                self.assertEqual(getattr(paths, attribute).name, name)
        for attribute in ("steps", "graph", "cycles", "readings", "audits",
                          "appeals", "errata"):
            self.assertEqual(getattr(paths, attribute).parent, paths.run_root)

    def test_a_cycle_directory_is_two_digits_and_carries_its_six_members(self):
        cycle = run_paths("/repo", "LOOP-01").cycle(7)
        self.assertEqual(cycle.root.name, "cycle-07")
        self.assertEqual(cycle.decision.name, "decision.json")
        self.assertEqual(cycle.cycle_md.name, "CYCLE.md")
        for attribute in ("import_dir", "use_table", "readings", "contrast"):
            self.assertEqual(getattr(cycle, attribute).parent, cycle.root)
        with self.assertRaises(LoopError) as caught:
            run_paths("/repo", "LOOP-01").cycle(0)
        self.assertEqual(caught.exception.code, "CYCLE_OUT_OF_RANGE")

    def test_a_step_path_and_its_open_marker_differ_only_by_the_suffix(self):
        paths = run_paths("/repo", "LOOP-01")
        self.assertEqual(paths.step_path(12, "SEND").name, "0012-SEND.json")
        self.assertEqual(paths.step_path(12, "SEND", open_marker=True).name,
                         "0012-SEND.json.open")
        with self.assertRaises(LoopError):
            paths.step_path(12, "DISPATCH")

    def test_a_reading_directory_is_a_pure_collision_free_function_of_the_row_key(self):
        paths = run_paths("/repo", "LOOP-01")
        first = paths.reading_dir("p1/mini_fcl/cycle-1/n1#r3")
        self.assertEqual(first, paths.reading_dir("p1/mini_fcl/cycle-1/n1#r3"))
        self.assertEqual(first.parent, paths.readings)
        self.assertNotIn("/", first.name)
        # Two keys that fold to the same characters still get two directories.
        self.assertNotEqual(paths.reading_dir("a/b"), paths.reading_dir("a#b"))
        with self.assertRaises(LoopError):
            paths.reading_dir("")

    def test_a_run_id_can_never_reach_outside_the_loops_root(self):
        for bad in ("../escape", "a/b", "", ".", "..", "/abs"):
            with self.subTest(run_id=bad):
                with self.assertRaises(LoopError) as caught:
                    run_paths("/repo", bad)
                self.assertEqual(caught.exception.code, "RUN_ID_INVALID")

    def test_run_paths_writes_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = run_paths(directory, "LOOP-01")
            paths.cycle(1)
            paths.step_path(0, "PREREGISTER")
            paths.reading_dir("p1/n1")
            self.assertEqual(sorted(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
