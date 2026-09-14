"""W6-DRYRUN: the acceptance proof - the whole loop, offline, against a real
temporary bare git repository, with every induced failure named by code in the
closing receipt.

**Nothing here is a fake, and nothing is hand-staged onto the ledger.**  The
walk is the driver's own ``dry_run`` entry - S0 PREREGISTER through S15 CLOSE -
over the real ``trial``, ``audits``, ``report``, ``reader``, ``marker``,
``markprep``, ``packs``, ``decide``, ``steps``, ``publish``, ``receipts``,
``custody`` and ``graph``, over the real ``graph_import_h005`` and
``use_relation_h005``, and over runner v2 imported in-process from the fixture
checkout.  Every git operation runs through ``publish()`` against a real bare
repository in a temp directory, so ``VERIFIED`` is exercised rather than
stubbed.  The one seam bound is ``provider_factory`` - W6-DRYRUN's own, and the
only provider seam in the loop - and the socket layer is removed from under all
of it and counted on the provider module itself.

The run is **one run directory across six invocations**, because that is the
only honest way to prove a resumable machine: a halt is recorded by the
invocation it stops, and the closing receipt is minted by a later one.

===== ======================================================================
inv    what it does, and what it proves
===== ======================================================================
1     ``dry_run(config, out)``: S0, S1, then S2 onward.  The SEND body of the
      first wave outruns the ``timeouts.step_seconds["SEND"]`` deadline the
      frozen config declares; W1-STEPS records ``STEP_TIMEOUT`` on a spending
      step and **leaves the open marker standing**.
2     ``run()`` again: the standing marker halts the resume with
      ``UNRESOLVED_STEP`` and the SEND body is never re-entered.
3     ``run --acknowledge <timeout step key> --reason ...``: cycle 1 completes
      (one arm ended by a provider failure, the others dispatched to their
      terminal nodes, the reading and mark legs read and marked), then cycle
      2's CYCLE_OPEN finds a pinned source moved and **halts** -
      ``SOURCE_PIN_MISMATCH``, an erratum stub, exit 1.
4     ``run`` with the bytes restored: still refused.  The halt is sticky.
5     ``reopen --reason <not pre-registered>``: refused ``REOPEN_REFUSED``,
      and the refusal is filed on the run's own record.  The appellate ruling
      is staged here, against a bearing **the loop itself registered**;
      staging alone moves no label.
6     ``run --acknowledge <halted step key> --reason ...``: the ruling is
      ingested at S3 before any receipt of the invocation, cycle 2 runs, S15
      writes CLOSING.md.
===== ======================================================================

Reconciliation of the draft's six seam dependencies (D1-D6)
-----------------------------------------------------------

*D1, D2* - **gone.**  The draft injected fakes through a ``Modules`` table of
eleven slots.  The integrated ``Modules`` has three fields and exactly one of
them is a seam onto behaviour, so every fake has been deleted and every
assertion is made against the real module's own record.

*D3* - **gone.**  The draft wrote its naming lines into the private
``_run.json`` because the draft driver's ``_fallback_closing`` printed nothing
else.  The integrated ``close()`` mints the naming section from the run's own
step ledger, run state and written records
(``auto_loop.recorded_failures``); this module asserts that section, and
writes nothing into the run tree.

*D4* - **kept as a fact, not as a seam.**  ``_ingest_rulings`` really does
ingest every staged ruling at cycle open, before any receipt of the
invocation, and ``rulings_applied_this_run`` really does salt the replayable
steps.  Nothing here stages anything to make that true.

*D5* - **gone.**  ``dry_run`` is no longer a thin gate entry: it stages the
synthetic material every occurrence the config names, walks S0 and S1 when the
run carries no plan, and walks S2-S15.  This module drives that entry.

*D6* - **gone.**  The draft hand-opened a ``PREPARE`` step with a jumped
monotonic clock because a deadline hit inside ``run()`` re-raised.  The
deadline is declared in the frozen config and hit inside the **spending SEND
body**; the marker stands, the resume halts, and the acknowledgement is an
operator act with a reason on the record.

The one condition still built by this fixture, and why
------------------------------------------------------

``synthetic.contrast_leg()`` **declares** a case whose difference kind collides
with the sealed within-ORIGINAL baseline, but ``markprep.baseline_kinds``
computes an *empty* set for every register of every case from the replicates it
actually writes - so no canned marker answer can collide with anything and G9
is unreachable from the canned material.  That finding is asserted here as its
own test rather than worked around.  Design 4.7 gives the contrast material to
the fixture and WAVE5-INTERFACE §9 item 5 routed the choice to this module
explicitly, so the material half is built here by the recipe
``tests/loop/test_marker.py`` already carries - two of three ORIGINAL
replicates gain a ``revises`` the first does not - and the gate supplies
**one** seat answer: ``differs`` at the kind that baseline really exhibits,
quoting two spans computed from the cell's own pairwise surface.  Every other
answer is ``synthetic``'s, and the downgrade to ``same`` is entirely the
program's: the seat says ``differs``, and G9 is what decides whether it stands.

The fixture also moves one pinned source **under the running loop**, at the
first marker call of cycle 1 - after the reading arm has registered and before
the next cycle's custody check.  That is the event the custody layer exists to
catch, and it is the one point in a two-cycle walk where a halt still leaves a
cycle for a later invocation to run, which is what the appellate clause needs.
"""
from __future__ import annotations

import io
import json
import re
import subprocess
import tempfile
import time
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from deepreason_core.ontology import Status

from minireason.loop import contracts as contracts_module
from minireason.loop import custody
from minireason.loop import graph as graph_module
from minireason.loop import markprep as markprep_module
from minireason.loop import report as report_module
from minireason.loop import standard as standard_module
from minireason.loop import steps as steps_module
from minireason.loop import synthetic
from minireason.loop import types as loop_types
from minireason.loop.types import LoopConfig, LoopError, run_paths

# W5's fixture vocabulary, imported rather than retyped: one spelling of the
# socket guard, the provider-module counter, the fixture source list, the seat
# registry and the coordinate-mapping script, and one driver module object.
from tests.loop.test_auto_loop import (
    FIXTURE_SOURCES,
    RUNNER_NAME,
    GateProviders,
    ProviderCounter,
    auto_loop,
    no_sockets,
    reading_key,
    seat_registry_document,
)

RUN_ID = "RUN-W6-DRYRUN"

#: The nine the design's acceptance clause lists, by ``synthetic``'s own token.
NAMED: tuple[str, ...] = (
    "provider_arm_failure",
    "custody_mismatch",
    "step_timeout",
    "ensemble_split",
    "paraphrase_flip",
    "non_unique_offset",
    "baseline_kind_collision",
    "reread_without_reason",
    "appellate_ruling",
)

#: The SEND deadline the gate's frozen config declares, and the delay one
#: delivery spends against it.  Both are the fixture's; the enforcement is
#: W1-STEPS' and the code is its own.
SEND_DEADLINE_SECONDS = 3
SEND_OVERRUN_SECONDS = 3.6

_VERIFIED_RE = re.compile(r"\AVERIFIED [0-9a-f]{7,64} ")


def _git(where: Path, *argv: str) -> None:
    subprocess.run(["git", "-C", str(where), *argv], check=True, capture_output=True)


# --------------------------------------------------------------------------
# The two declared overrides on the scripted provider
# --------------------------------------------------------------------------

class CollidingMarkScript(synthetic.ScriptedProviders):
    """``synthetic``'s script, with one marker answer the program will downgrade.

    ``synthetic`` answers ``differs`` for exactly one register per case, and
    never at a kind the sealed within-ORIGINAL baseline exhibits: its
    ``contrast_leg`` *declares* a colliding case in ``baseline_kinds``, but
    ``markprep.baseline_kinds`` computes an empty set from the replicates it
    writes, so no canned answer can collide with anything and G9 is
    unreachable from the canned material (WAVE5-INTERFACE §9 item 5 routes this
    here).  The gate therefore supplies one seat answer - ``differs`` at the
    kind the gate's own baseline really exhibits, quoting two spans that
    resolve exactly once on that cell's pairwise surface in both presentation
    orders - and changes no other answer.  The seat says ``differs``; whether
    that stands is the program's to decide, and G9 is what decides it.
    """

    def __init__(self, *, case: str, register: str, kind: str,
                 quotes: tuple[str, str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.case = str(case)
        self.register = str(register)
        self.kind = str(kind)
        self.quotes = quotes
        self.answered: list[str] = []

    def script_for(self, role, coordinate, *, seat=None):
        entries = super().script_for(role, coordinate, seat=seat)
        parts = str(coordinate).split("/")
        if role != "marker" or len(parts) < 3:
            return entries
        if (parts[1], parts[2]) != (self.case, self.register):
            return entries
        left, right = self.quotes
        body = {"mark": "differs", "difference_kind": self.kind,
                "left_quote": left, "right_quote": right,
                "case": "the two sides dispose of the quoted criticism "
                        "differently"}
        content = json.dumps(body, ensure_ascii=False, sort_keys=True)
        self.answered.append(str(coordinate))
        # The envelope is synthetic's own entry, so nothing about the offline
        # provider's record shape is retyped here.
        return tuple({**entry, "content": content} for entry in entries)


class DryRunProviders(GateProviders):
    """W5's coordinate mapping over the gate's script, plus one slow delivery.

    The slow delivery is how the SEND deadline is met by a body rather than by
    a clock: one delivery call spends longer than the frozen
    ``timeouts.step_seconds["SEND"]``, and W1-STEPS records the overrun on the
    step it happened in.  Nothing patches a clock and nothing shortens one.
    """

    def __init__(self, mapping, *, script: CollidingMarkScript,
                 delay_seconds: float = 0.0, at_first_mark=None) -> None:
        super().__init__(mapping)
        self.inner = script
        self.delay_seconds = float(delay_seconds)
        self.delayed: list[str] = []
        self.at_first_mark = at_first_mark
        self.marked: list[str] = []

    def __call__(self, endpoint, records_dir):
        if self.delay_seconds and not self.delayed:
            self.delayed.append(str(records_dir))
            time.sleep(self.delay_seconds)
        return super().__call__(endpoint, records_dir)

    def provider(self, role, coordinate, records_dir, *, seat=None, endpoint=None):
        if role == "marker" and not self.marked:
            self.marked.append(str(coordinate))
            if self.at_first_mark is not None:
                self.at_first_mark()
        return super().provider(role, coordinate, records_dir, seat=seat,
                                endpoint=endpoint)


# --------------------------------------------------------------------------
# The gate: one tree, one run directory, six invocations - built once
# --------------------------------------------------------------------------

class Gate:
    """Everything the walk produced, so every class below reads one run."""

    _instance: "Gate | None" = None

    @classmethod
    def instance(cls) -> "Gate":
        if cls._instance is None:
            gate = cls()
            gate.build()
            cls._instance = gate
        return cls._instance

    # -- construction ------------------------------------------------------

    def build(self) -> None:
        self.counter = ProviderCounter()
        self.temp = tempfile.TemporaryDirectory(prefix="w6-dryrun-")
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.repo = self.root / "checkout"
        self.out = self.root / "dry-run-out"
        self.spawned: list[str] = []
        self.outputs: dict[str, object] = {}
        #: Every provider factory this gate handed the driver.  The walk's own
        #: are snapshotted when it ends, so a later read-back that needs a
        #: ``Modules`` cannot dilute what the walk actually spent.
        self.factories: list[DryRunProviders] = []
        self._build_tree()
        self.paths = run_paths(self.repo, RUN_ID)
        self.mapping = {auto_loop.cell_key_for(reading_key(identity)): name
                        for name, identity in synthetic.READING_COORDINATES.items()}
        self.declared_leg = synthetic.contrast_leg()
        (self.leg, self.collision_case, self.collision_register,
         self.collision_kind) = self._colliding_leg()
        self.quotes = self._resolving_quotes()
        self._write_contrast_leg()
        original_popen = subprocess.Popen
        original_run = subprocess.run

        def watch(argv):
            self.spawned.append(" ".join(str(part) for part in argv)
                                if isinstance(argv, (list, tuple)) else str(argv))

        def watching_popen(argv, *args, **kwargs):
            watch(argv)
            return original_popen(argv, *args, **kwargs)

        def watching_run(argv, *args, **kwargs):
            watch(argv)
            return original_run(argv, *args, **kwargs)

        subprocess.Popen = watching_popen
        subprocess.run = watching_run
        try:
            with no_sockets(self.counter):
                self._walk()
        finally:
            subprocess.Popen = original_popen
            subprocess.run = original_run
            self._restore_runner()
        self.closing_text = self.paths.closing.read_text(encoding="utf-8")
        self.named_codes = closing_codes(self.closing_text)

    def providers(self, *, delay: float = 0.0,
                  at_first_mark=None) -> DryRunProviders:
        script = CollidingMarkScript(
            case=self.collision_case, register=self.collision_register,
            kind=self.collision_kind, quotes=self.quotes,
            seed=synthetic.DEFAULT_SEED,
            induce=("provider_arm_failure", "ensemble_split", "paraphrase_flip",
                    "non_unique_offset", "decisive_point_absent",
                    "reread_without_reason", "baseline_kind_collision"))
        return DryRunProviders(self.mapping, script=script, delay_seconds=delay,
                               at_first_mark=at_first_mark)

    def modules(self, *, delay: float = 0.0, at_first_mark=None) -> object:
        self.factory = self.providers(delay=delay, at_first_mark=at_first_mark)
        self.factories.append(self.factory)
        return auto_loop.Modules(provider_factory=self.factory,
                                 repo_root=self.repo,
                                 sleep=lambda _seconds: None)

    # -- the tree ----------------------------------------------------------

    def _install_runner(self) -> None:
        import importlib.util
        import sys

        from minireason.loop import seats as seats_module
        self._previous_runner = (sys.modules.get(RUNNER_NAME), seats_module._RUNNER)
        spec = importlib.util.spec_from_file_location(
            RUNNER_NAME,
            self.repo / "tools" / "multicycle_commitment_study_multi_v2.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[RUNNER_NAME] = module
        spec.loader.exec_module(module)
        module.set_registry(synthetic.endpoints_registry())
        seats_module._RUNNER = module
        self.runner = module

    def _restore_runner(self) -> None:
        import sys

        from minireason.loop import seats as seats_module
        previous, registry = self._previous_runner
        if previous is None:
            sys.modules.pop(RUNNER_NAME, None)
        else:
            sys.modules[RUNNER_NAME] = previous
        seats_module._RUNNER = registry

    def _build_tree(self) -> None:
        _git(self.root, "init", "--bare", "--initial-branch=main", str(self.remote))
        _git(self.root, "init", "--initial-branch=main", str(self.repo))
        for key, value in (("user.name", "W6 dry run"),
                           ("user.email", "w6-dryrun@example.invalid"),
                           ("commit.gpgsign", "false"),
                           ("core.autocrlf", "false")):
            _git(self.repo, "config", key, value)
        source = Path(auto_loop.__file__).resolve().parents[1]
        for rel in FIXTURE_SOURCES:
            path = self.repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((source / rel).read_bytes())
        endpoints = self.repo / "src/minireason/data/endpoints.json"
        endpoints.parent.mkdir(parents=True, exist_ok=True)
        endpoints.write_bytes(json.dumps(seat_registry_document(), indent=1,
                                         sort_keys=True).encode())
        (self.repo / "docs").mkdir(parents=True, exist_ok=True)
        (self.repo / "docs" / "DECISION_LEDGER.md").write_bytes(b"# Decision ledger\n")
        run_root = self.repo / "experiments" / "loops" / RUN_ID
        run_root.mkdir(parents=True, exist_ok=True)
        (run_root / "obligations.json").write_bytes(json.dumps({
            "schema": "minireason.loop.obligations.v1",
            "obligations": [
                {"id": "o1", "set": "O",
                 "statement": "every row carries a relation or a recorded reason",
                 "check": "row_disposition_complete"},
                {"id": "o5", "set": "O",
                 "statement": "the audit record in force is not older than "
                              "AUDIT_PERIOD cycles",
                 "check": "audit_in_force"},
                {"id": "p7", "set": "P",
                 "statement": "no reading mints an att or dep edge on a node "
                              "under study",
                 "check": "no_edges_on_studied_nodes"},
            ]}).encode())
        (run_root / "calibration.json").write_bytes(json.dumps({
            "schema": "minireason.loop.calibration.v1",
            "rows": [], "error_rule": "one wrong anchor is one error"}).encode())
        self._install_runner()
        self.config_path = self.repo / "loop-config.json"
        self.config_path.write_bytes(
            json.dumps(self.config_body(), indent=1).encode())
        _git(self.repo, "add", "--", ".")
        _git(self.repo, "commit", "-m", "the published tree")
        _git(self.repo, "remote", "add", "origin", str(self.remote))
        _git(self.repo, "push", "--set-upstream", "origin", "HEAD:refs/heads/main")

    def config_body(self) -> dict:
        return {
            "schema": "minireason.loop.config.v1",
            "run_id": RUN_ID,
            "study": "the W6-DRYRUN acceptance gate: the whole loop offline "
                     "over the synthetic occurrence and its contrast leg",
            "occurrences": ["occurrence-01"],
            "runner": "tools/multicycle_commitment_study_multi_v2.py",
            "publish_ref": "origin/main",
            "cycle_budget": 2,
            "max_calls": 400,
            "reading_set": [reading_key(identity)
                            for identity in synthetic.READING_COORDINATES.values()],
            "obligations_path": f"experiments/loops/{RUN_ID}/obligations.json",
            "graph_root": f"experiments/loops/{RUN_ID}/graph",
            "reopen_reasons": list(standard_module.REOPEN_REASONS),
            "audit": {"period": 2, "judge_err_max": 0.4,
                      "judge_err_max_account":
                          "the share is over the anchor-by-seat pairs this "
                          "window exercised and adjudicates no cell",
                      "streak_max": 12,
                      "streak_max_account": auto_loop.BLOCK_STREAK_DEFINITION},
            "seats": {"critic": "w5/critic", "defender": "w5/defender",
                      "judges": ["w5/judge-a", "w5/judge-b"],
                      "variator": "w5/variator",
                      "min_judge_families": 2, "paraphrase_n": 2,
                      "schema_repair_budget": 0},
            "contrast": {"attached": True, "study": "contrast-study",
                         "occurrences": ["contrast-study/occurrence-01"]},
            "timeouts": {"step_seconds": {"SEND": SEND_DEADLINE_SECONDS},
                         "git_seconds": 90},
            "provider_mode": "offline",
        }

    def _colliding_leg(self) -> tuple[dict, str, str, str]:
        """``synthetic``'s leg, with one case's baseline made to exhibit a kind.

        The recipe is the one ``tests/loop/test_marker.py`` already carries:
        two of the three ORIGINAL replicates gain a ``revises`` the first does
        not, so the sealed within-ORIGINAL baseline for that register holds a
        disposition kind.  The leg also gains the **address space** its own
        refs already use, derived from its own bytes rather than declared here:
        without it ``markprep`` reads no reference as engaging a criticism and
        every register's baseline computes empty, which is what makes G9
        unreachable from the canned leg.
        """

        leg = json.loads(json.dumps(self.declared_leg))
        leg["addresses"], leg["objection_ids"] = self._address_space(leg)
        case = sorted(leg["cases"])[0]
        replicates = leg["cases"][case]["replicates"]
        for name in sorted(replicates)[1:]:
            body = json.loads(replicates[name]["ORIGINAL"])
            body["records"][0]["revises"] = ["c0"]
            replicates[name]["ORIGINAL"] = json.dumps(body)
        cell = markprep_module.cell_from_contrast_leg(
            leg, case, addresses=leg["addresses"],
            objection_ids=leg["objection_ids"])
        markprep_module.write_baseline(cell, None, self.root / "collision-baseline")
        exhibited = {register: kinds
                     for register, kinds in markprep_module.baseline_kinds(cell).items()
                     if kinds}
        assert exhibited, "the gate's leg exhibits no baseline kind at all"
        register = sorted(exhibited)[0]
        return leg, case, register, exhibited[register][0]

    @staticmethod
    def _address_space(leg: dict) -> tuple[dict, list[str]]:
        """The address prefix and criticism ids the leg's own refs already use."""

        refs: set[str] = set()
        for body in leg["cases"].values():
            for sides in body["replicates"].values():
                for side in ("ORIGINAL", "CONTROL"):
                    document = json.loads(sides[side])
                    for record in document.get("records", ()):
                        for field in ("target", "revises", "mentions", "depends"):
                            for value in record.get(field, ()) or ():
                                if "#" in str(value):
                                    refs.add(str(value))
        prefixes = sorted({ref.split("#", 1)[0] for ref in refs})
        ids = sorted({ref.split("#", 1)[1] for ref in refs})
        assert len(prefixes) == 1, f"the leg addresses more than one document: {prefixes}"
        return {"objection": prefixes[0]}, ids

    def _write_contrast_leg(self) -> None:
        leg_dir = self.repo / "contrast-study" / "occurrence-01"
        leg_dir.mkdir(parents=True, exist_ok=True)
        (leg_dir / "contrast.json").write_bytes(custody.encoded(self.leg))

    def _resolving_quotes(self) -> tuple[str, str]:
        """Two spans of the colliding cell's own surface, each resolving once."""

        cell = markprep_module.cell_from_contrast_leg(
            self.leg, self.collision_case, addresses=self.leg["addresses"],
            objection_ids=self.leg["objection_ids"])
        # G8: the residue is readable only behind a sealed baseline.  This is a
        # throwaway cell under the gate's own temp directory, built from the
        # same leg bytes the run will build its cell from; the run seals its
        # own baseline at S0 and this one is never shown to it.
        markprep_module.write_baseline(cell, None, self.root / "quote-baseline")
        row = next(r for r in markprep_module.residue(cell)
                   if r.register == self.collision_register)
        left_key, right_key = row.left_replicates[0], row.right_replicates[0]
        surface = markprep_module.pairwise_surface(cell, left_key, right_key)
        swapped = markprep_module.pairwise_surface(cell, right_key, left_key)
        return (_unique_span(surface, swapped, cell.replicate(left_key).commitments),
                _unique_span(surface, swapped, cell.replicate(right_key).commitments))

    # -- the walk ----------------------------------------------------------

    def _walk(self) -> None:
        out = self.outputs

        # inv 1 - S0, S1, S2 onward; the SEND body outruns its own deadline.
        with self.expect(steps_module.StepTimeout) as caught:
            auto_loop.dry_run(self.config_path, self.out,
                              modules=self.modules(delay=SEND_OVERRUN_SECONDS),
                              induce=("provider_arm_failure",))
        out["timeout"] = caught.value
        self.plan = json.loads(self.paths.plan.read_text(encoding="utf-8"))
        self.plan_id = str(self.plan["loop_plan_id"])
        self.timeout_receipt = self._receipt_with("STEP_TIMEOUT")
        self.markers_after_timeout = self.ledger().markers()

        # inv 2 - the standing marker halts the resume; no body is re-entered.
        original = self.runner.send_round
        entered: list[str] = []

        def watching(repo, outputs, **kwargs):
            entered.append("dispatched")
            return original(repo, outputs, **kwargs)

        self.runner.send_round = watching
        try:
            with self.expect(steps_module.UnresolvedStep) as unresolved:
                auto_loop.run(self.config_path, modules=self.modules())
            out["unresolved"] = unresolved.value
            self.resend_after_marker = list(entered)
            self.blocked_status = dict(auto_loop.status(
                self.paths.run_root, modules=self.modules()))

            # inv 3 - acknowledge the overrun and complete cycle 1.  A pinned
            # source changes under the running loop at the first marker call -
            # after the reading arm has registered, before the next cycle's
            # custody check - which is the event the custody layer exists to
            # catch and the one point in a two-cycle walk where a halt still
            # leaves a cycle for a later invocation to run.
            self.moved = self.repo / "src/minireason/use_relation_h005.py"
            self.moved_bytes = self.moved.read_bytes()

            def move_the_pinned_source() -> None:
                self.moved.write_bytes(self.moved_bytes
                                       + b"\n# moved under the plan\n")

            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.custody_exit = auto_loop.main(
                    ["run", "--config", str(self.config_path),
                     "--acknowledge", self.timeout_receipt["step_key"],
                     "--reason", "the wave's provider records show no billed call"],
                    modules=self.modules(at_first_mark=move_the_pinned_source))
            out["custody_stderr"] = stderr.getvalue()
            self.dispatched_after_acknowledge = list(entered)
        finally:
            self.runner.send_round = original

        self.halted_receipt = self._receipt_with("SOURCE_PIN_MISMATCH")
        self.errata = sorted(p.name for p in self.paths.errata.iterdir()) \
            if self.paths.errata.is_dir() else []

        # inv 4 - restoring the bytes is not enough: the halt is sticky.
        self.moved.write_bytes(self.moved_bytes)
        sticky = io.StringIO()
        with redirect_stderr(sticky):
            self.sticky_exit = auto_loop.main(
                ["run", "--config", str(self.config_path)], modules=self.modules())
        out["sticky_stderr"] = sticky.getvalue()

        # inv 5 - a re-read refused for want of a pre-registered reason, and the
        # appellate ruling staged against a bearing the loop itself registered.
        refused = io.StringIO()
        with redirect_stderr(refused):
            self.reopen_exit = auto_loop.main(
                ["reopen", "--run", str(self.paths.run_root),
                 "--reason", "a reason this plan never pre-registered"],
                modules=self.modules())
        out["reopen_stderr"] = refused.getvalue()
        self.registered = self._registered_readings()
        self.target = self.registered[0]
        self.bystander = self.registered[1]
        ruling_path = self.root / "ruling.json"
        ruling_path.write_text(json.dumps({
            "ruling_id": "APP-001",
            "target": self.target["ids"]["bearing"],
            "standard_id": self.plan["standard_id"],
            "ground": "the read does not bear on the claim offered",
            "reopen_reason": "appellate-ruling", "body": {}}), encoding="utf-8")
        self.staged = auto_loop.appeal(self.paths.run_root, path=ruling_path,
                                       modules=self.modules())
        self.before_appeal = self._labels()

        # inv 6 - acknowledge the halt; the ruling is ingested at S3, cycle 2
        # runs, S15 writes the closing record.
        self.closed_exit = auto_loop.main(
            ["run", "--config", str(self.config_path),
             "--acknowledge", self.halted_receipt["step_key"],
             "--reason", "the pinned file was restored to its frozen bytes"],
            modules=self.modules())
        self.after_appeal = self._labels()
        self.state = json.loads(
            (self.paths.run_root / "_run.json").read_text(encoding="utf-8"))
        self.verdict = json.loads(
            (self.out / "dry-run.json").read_text(encoding="utf-8"))
        self.walk_factories = list(self.factories)

    # -- read-back ---------------------------------------------------------

    def expect(self, kind):
        class _Caught:
            value = None

            def __enter__(self_inner):
                return self_inner

            def __exit__(self_inner, exc_type, exc, _tb):
                if exc_type is not None and issubclass(exc_type, kind):
                    self_inner.value = exc
                    return True
                return False

        return _Caught()

    def ledger(self) -> steps_module.StepLedger:
        return steps_module.StepLedger(self.paths.run_root, self.plan_id)

    def rows(self) -> list[dict]:
        return [row.receipt.as_dict() | {"index": row.index}
                for row in self.ledger().records()]

    def _receipt_with(self, code: str) -> dict:
        found = [row for row in self.rows() if row.get("failure_code") == code]
        assert found, f"no receipt carries {code}"
        return found[-1]

    def _registered_readings(self) -> list[dict]:
        records = [json.loads(path.read_text(encoding="utf-8"))
                   for path in sorted(self.paths.readings.rglob("reading.json"))]
        assert len(records) >= 2, "the reading arm registered fewer than two readings"
        return records

    def _labels(self) -> dict:
        harness = graph_module.open_graph(
            graph_module.resolve_graph_root(self.repo, "experiments/loops/"
                                            f"{RUN_ID}/graph"),
            clock=graph_module.fixed_clock())
        return {
            "bearing": harness.state.status.get(self.target["ids"]["bearing"]),
            "reading": harness.state.status.get(self.target["ids"]["reading"]),
            "cell": graph_module.cell_state(harness, self.target["cell"]),
            "bearings": {record["row_key"]:
                         harness.state.status.get(record["ids"]["bearing"])
                         for record in self.registered},
            "rulings": graph_module.appellate_rulings(harness),
        }


def _unique_span(surface: str, swapped: str, text: str) -> str:
    """The longest prefix-anchored span of ``text`` resolving once in both orders."""

    for size in (120, 90, 70, 50, 40, 30):
        for start in range(0, max(1, len(text) - size), 7):
            candidate = text[start:start + size]
            if candidate and surface.count(candidate) == 1 \
                    and swapped.count(candidate) == 1:
                return candidate
    raise AssertionError("no uniquely resolving span in this side")


#: The register's rows are ``| `<reason>` xN | <cells> |`` - the bare reason
#: spelling W3-REPORT prints, which ``types.block_code`` turns back into the
#: code ``synthetic.INDUCED_CODES`` names.
_REGISTER_ROW = re.compile(r"^\|\s*`([a-z-]+)`\s*x(\d+)\s*\|\s*(.*?)\s*\|\s*$", re.M)


def closing_codes(text: str) -> set[str]:
    """Every code the closing receipt names, as a membership fact.

    Two registers, read the way each is written: the block register prints the
    bare reason and a row with no cell names nothing, so a row is read as a
    naming only where it names a cell; every other code is a bare token of
    ``types.FAILURE_CODES`` or ``types.OUTCOME_CODES``.
    """

    found: set[str] = set()
    for reason, _count, cells in _REGISTER_ROW.findall(text):
        if cells and cells != "-":
            found.add(loop_types.block_code(reason))
    for token in re.findall(r"[A-Z][A-Z0-9_]+", text):
        if token in loop_types.FAILURE_CODES or token in loop_types.OUTCOME_CODES:
            found.add(token)
    return found


class GateCase(unittest.TestCase):
    """Every class below reads the one walk; nothing here runs a second one."""

    gate: Gate

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.gate = Gate.instance()

    def code(self, token: str) -> str:
        return synthetic.INDUCED_CODES[token]

    def register_row(self, reason: str) -> tuple[str, str] | None:
        for found, count, cells in _REGISTER_ROW.findall(self.gate.closing_text):
            if found == reason:
                return count, cells
        return None


# --------------------------------------------------------------------------
# The walk itself
# --------------------------------------------------------------------------

class TheDryRunWalksSZeroToSFifteen(GateCase):

    def test_the_dry_run_entry_staged_the_material_and_walked_s0_and_s1(self):
        verdict = self.gate.verdict
        self.assertEqual(verdict["staged"]["occurrences"], ["occurrence-01"])
        # The contrast leg is the gate's own (it carries the collision
        # material), and an occurrence the tree already carries is left exactly
        # as it stands - which is the staging rule, asserted here by its
        # silence.
        self.assertEqual(verdict["staged"]["contrast"], [])
        self.assertTrue((self.gate.repo / "contrast-study" / "occurrence-01"
                         / "contrast.json").is_file())
        self.assertIn("preregister", verdict)
        self.assertEqual(verdict["preflight"]["provider_calls"], 0)
        self.assertEqual(list(verdict["inducible"]), list(synthetic.INDUCIBLE))
        self.assertEqual(verdict["seed"], synthetic.DEFAULT_SEED)

    def test_the_first_verdict_recorded_the_refusal_it_ended_on(self):
        # inv 1 ended in the induced overrun, and the verdict says so rather
        # than being lost with the exception.
        self.assertIsNotNone(self.gate.outputs["timeout"])
        self.assertEqual(self.gate.outputs["timeout"].code, "STEP_TIMEOUT")

    def test_every_state_from_s2_to_s15_filed_a_receipt_in_order(self):
        kinds = [row["kind"] for row in self.gate.rows()]
        self.assertEqual(kinds[0], "PUBLISH_PLAN")
        self.assertEqual(kinds[-1], "PUBLISH_CY")
        self.assertEqual(kinds.count("CLOSE"), 1)
        for kind in ("CYCLE_OPEN", "PREPARE", "PUBLISH_IN", "SEND", "PUBLISH_EV",
                     "IMPORT", "USE_TABLE", "READ", "MARK", "AUDIT",
                     "ADJUDICATE", "DECIDE"):
            with self.subTest(kind=kind):
                self.assertIn(kind, kinds)
        indices = [row["index"] for row in self.gate.rows()]
        self.assertEqual(len(indices), len(set(indices)))

    def test_the_run_closed_and_nothing_is_left_blocking(self):
        self.assertEqual(self.gate.closed_exit, 0)
        self.assertTrue(self.gate.paths.closing.is_file())
        summary = auto_loop.status(self.gate.paths.run_root,
                                   modules=self.gate.modules())
        self.assertIsNone(summary["blocking"])
        self.assertIsNone(summary["acknowledge"])
        for action in summary["actions"]:
            self.assertTrue(action["step_key"])
        # The overrun step's marker is still on disk and is meant to be: a
        # marker is resolved by an acknowledgement on the record, not erased,
        # so the one act that let the run past it stays readable beside it.
        standing = [kind for _index, kind, _path in self.gate.ledger().markers()]
        self.assertEqual(standing, ["SEND"])
        self.assertIn("no billed call",
                      json.dumps(list(self.gate.ledger().acknowledgements())))

    def test_the_run_wrote_nothing_outside_the_temporary_tree(self):
        source = Path(auto_loop.__file__).resolve().parents[1]
        self.assertFalse((source / "experiments" / "loops" / RUN_ID).exists())
        for path in (self.gate.paths.run_root, self.gate.out, self.gate.remote):
            self.assertTrue(str(path).startswith(str(self.gate.root)))


# --------------------------------------------------------------------------
# Zero provider network calls, by the provider module's own counter
# --------------------------------------------------------------------------

class ZeroProviderNetworkCalls(GateCase):

    def test_the_provider_module_opened_no_request_and_bound_no_live_transport(self):
        self.assertEqual(self.gate.counter.opened, 0,
                         "the provider module opened a request")
        self.assertEqual(self.gate.counter.live, 0,
                         "a live transport was constructed")

    def test_the_offline_provider_is_what_ran_so_nothing_passes_as_nothing(self):
        self.assertGreater(self.gate.counter.offline, 0,
                           "no provider ran at all; the walk proved nothing")
        self.assertGreater(
            sum(factory.inner.calls for factory in self.gate.walk_factories), 0)

    def test_the_frozen_plan_declares_the_offline_mode_it_ran_in(self):
        self.assertEqual(self.gate.plan["config"]["provider_mode"], "offline")


# --------------------------------------------------------------------------
# Every git operation through publish(), against a real bare repository
# --------------------------------------------------------------------------

class EveryGitOperationRanThroughPublish(GateCase):

    def test_every_completed_publication_filed_a_verified_line(self):
        ledger = self.gate.ledger()
        verified = 0
        for row in self.gate.rows():
            if not row["kind"].startswith("PUBLISH_") or row["status"] != "COMPLETE":
                continue
            line = ledger.verified_line(row["step_key"])
            self.assertIsNotNone(line, row["kind"])
            self.assertRegex(line or "", _VERIFIED_RE)
            verified += 1
        self.assertGreaterEqual(verified, 4)
        for kind in ("PUBLISH_PLAN", "PUBLISH_IN", "PUBLISH_EV", "PUBLISH_CY"):
            with self.subTest(kind=kind):
                self.assertIn(kind, [row["kind"] for row in self.gate.rows()])

    def test_the_bare_remote_really_holds_a_published_commit(self):
        head = subprocess.run(
            ["git", "-C", str(self.gate.remote), "rev-parse", "refs/heads/main"],
            capture_output=True, check=True).stdout.decode().strip()
        published = {row.get("published_commit") for row in self.gate.rows()}
        published.discard(None)
        self.assertIn(head, published)

    def test_nothing_but_git_and_the_activity_logger_was_ever_spawned(self):
        self.assertTrue(self.gate.spawned, "no subprocess ran at all")
        logged = 0
        for argv in self.gate.spawned:
            head = argv.split()[0]
            if "repo_activity.py" in argv:
                logged += 1
                self.assertNotIn("--command", argv)
                continue
            self.assertTrue(head.endswith("git"), argv)
        self.assertGreater(logged, 0, "no repository act was bracketed")


# --------------------------------------------------------------------------
# The ceiling, verbatim
# --------------------------------------------------------------------------

class TheClosingReceiptCarriesTheCeilingVerbatim(GateCase):

    def test_every_required_ceiling_sentence_appears_verbatim(self):
        sentences = standard_module.CEILING_REQUIRED_SENTENCES
        self.assertEqual(len(sentences), 11)
        for sentence in sentences:
            with self.subTest(sentence=sentence[:48]):
                self.assertIn(sentence, self.gate.closing_text)

    def test_the_closing_record_claims_no_exhaustion(self):
        standard_module.assert_no_exhaustion_claim(self.gate.closing_text,
                                                   "CLOSING.md")


# --------------------------------------------------------------------------
# Induction 1 - a provider failure ends one arm; the others run on
# --------------------------------------------------------------------------

class AProviderFailureEndedOneArm(GateCase):

    def test_one_arm_ended_by_its_own_code_and_the_closing_names_it(self):
        ended = self.gate.state["arms_ended"]
        self.assertEqual([row["arm"] for row in ended], [synthetic.PROSE_ARM])
        self.assertEqual(ended[0]["failure_code"],
                         self.code("provider_arm_failure"))
        self.assertEqual(ended[0]["text"], auto_loop.ARM_ENDED_TEXT)
        self.assertIn(auto_loop.ARM_ENDED_TEXT, self.gate.closing_text)
        self.assertIn(self.code("provider_arm_failure"), self.gate.named_codes)

    def test_the_other_arm_reached_its_terminal_node_in_the_same_cycle(self):
        terminal = (self.gate.repo / "occurrence-01" / "responses" / "synth"
                    / synthetic.FCL_ARM / "cycle01" / "response.json")
        self.assertTrue(terminal.is_file(), "the surviving arm did not finish")

    def test_the_ended_arm_minted_no_warrant(self):
        harness = graph_module.open_graph(
            graph_module.resolve_graph_root(
                self.gate.repo, f"experiments/loops/{RUN_ID}/graph"),
            clock=graph_module.fixed_clock())
        for key, _body in graph_module.reading_bodies(harness):
            self.assertNotIn(synthetic.PROSE_ARM, str(key))
        self.assertNotIn("overrun", self.gate.closing_text)


# --------------------------------------------------------------------------
# Induction 2 - a custody mismatch halts, writes an erratum, stays sticky
# --------------------------------------------------------------------------

class ACustodyMismatchHaltedAndStayedSticky(GateCase):

    def test_the_halt_exits_non_zero_and_names_its_code(self):
        self.assertEqual(self.gate.custody_exit, 1)
        self.assertIn(self.code("custody_mismatch"),
                      self.gate.outputs["custody_stderr"])

    def test_the_halted_step_is_the_cycle_open_and_wrote_an_erratum(self):
        receipt = self.gate.halted_receipt
        self.assertEqual(receipt["status"], "HALTED")
        self.assertEqual(receipt["kind"], "CYCLE_OPEN")
        self.assertTrue(self.gate.errata, "a custody halt wrote no erratum")

    def test_restoring_the_bytes_is_not_enough_and_the_halt_is_sticky(self):
        self.assertEqual(self.gate.sticky_exit, 1)
        self.assertIn(self.code("custody_mismatch"),
                      self.gate.outputs["sticky_stderr"])
        self.assertIn("sticky", self.gate.outputs["sticky_stderr"])

    def test_the_acknowledgement_is_itself_on_the_record(self):
        acknowledgements = json.dumps(list(self.gate.ledger().acknowledgements()))
        self.assertIn("restored to its frozen bytes", acknowledgements)
        self.assertIn(self.code("custody_mismatch"), self.gate.named_codes)


# --------------------------------------------------------------------------
# Induction 3 - a step timeout in a spending body leaves the marker standing
# --------------------------------------------------------------------------

class AStepTimeoutLeftItsMarkerStanding(GateCase):

    def test_the_overrun_was_recorded_on_the_spending_step_it_happened_in(self):
        receipt = self.gate.timeout_receipt
        self.assertEqual(receipt["kind"], "SEND")
        self.assertEqual(receipt["status"], "FAILED")
        self.assertEqual(receipt["failure_code"], "STEP_TIMEOUT")
        self.assertTrue(receipt["spending"])
        self.assertIn("STEP_TIMEOUT", steps_module.MARKER_KEPT_CODES)

    def test_the_marker_survived_the_failed_receipt(self):
        kinds = [kind for _index, kind, _path in self.gate.markers_after_timeout]
        self.assertEqual(kinds, ["SEND"])

    def test_status_printed_the_key_an_operator_must_acknowledge(self):
        # Read while the marker was standing, this is the flag value
        # ``--acknowledge`` takes; an operator should not have to open a
        # receipt to find it.
        self.assertEqual(self.gate.blocked_status["blocking"], "UNRESOLVED_STEP")
        self.assertEqual(self.gate.blocked_status["acknowledge"],
                         self.gate.timeout_receipt["step_key"])

    def test_the_resume_halted_and_re_entered_no_dispatch(self):
        self.assertIsNotNone(self.gate.outputs["unresolved"])
        self.assertEqual(self.gate.outputs["unresolved"].code, "UNRESOLVED_STEP")
        self.assertEqual(self.gate.resend_after_marker, [],
                         "a step with an unresolved marker was re-entered")
        self.assertTrue(self.gate.dispatched_after_acknowledge,
                        "the acknowledged run never dispatched")

    def test_the_closing_receipt_names_the_step_timeout_by_code(self):
        self.assertIn(self.code("step_timeout"), self.gate.named_codes)


# --------------------------------------------------------------------------
# Induction 4 - an ensemble split resolves to unresolved and is not voted
# --------------------------------------------------------------------------

class AnEnsembleSplitResolvedToUnresolved(GateCase):

    REASON = "ensemble-split"

    def test_the_register_names_the_split_and_the_cell_it_declined(self):
        row = self.register_row(self.REASON)
        self.assertIsNotNone(row)
        _count, cells = row
        self.assertNotEqual(cells, "-")
        self.assertIn(self.code("ensemble_split"), self.gate.named_codes)

    def test_the_split_row_registered_no_reading(self):
        _count, cells = self.register_row(self.REASON)
        registered = {row["cell"] for row in self.gate.registered}
        for cell in cells.split(", "):
            self.assertNotIn(cell, registered)

    def test_nothing_in_the_record_voted(self):
        lowered = self.gate.closing_text.lower()
        for word in ("majority", "vote", "voted", "average", "mean", "quorum"):
            with self.subTest(word=word):
                self.assertIsNone(re.search(r"\b" + word + r"\b", lowered))


# --------------------------------------------------------------------------
# Induction 5 - a paraphrase flip registers no warrant
# --------------------------------------------------------------------------

class AParaphraseFlipRegisteredNoWarrant(GateCase):

    REASON = "paraphrase-flip"

    def test_the_register_names_the_flip_and_no_reading_stands_for_it(self):
        row = self.register_row(self.REASON)
        self.assertIsNotNone(row)
        _count, cells = row
        self.assertNotEqual(cells, "-")
        registered = {record["cell"] for record in self.gate.registered}
        for cell in cells.split(", "):
            self.assertNotIn(cell, registered)
        self.assertIn(self.code("paraphrase_flip"), self.gate.named_codes)


# --------------------------------------------------------------------------
# Induction 6 - a quote resolving twice registers no warrant
# --------------------------------------------------------------------------

class ANonUniqueOffsetRegisteredNoWarrant(GateCase):

    REASON = "referential-integrity"

    def test_the_duplicated_phrase_really_stands_twice_in_the_material(self):
        # The material half of the induction is synthetic's own: one sentence
        # is deliberately in two records of the arm the row is read on, so a
        # critic quoting it cites a span that resolves twice.
        delivered = "".join(
            synthetic.delivery_content(synthetic.FCL_ARM, node)
            for node in synthetic.NODE_IDS)
        self.assertGreater(delivered.count(synthetic.DUPLICATED_PHRASE), 1)

    def test_the_register_names_the_refusal_and_no_reading_stands_for_it(self):
        row = self.register_row(self.REASON)
        self.assertIsNotNone(row)
        _count, cells = row
        self.assertNotEqual(cells, "-")
        registered = {record["cell"] for record in self.gate.registered}
        for cell in cells.split(", "):
            self.assertNotIn(cell, registered)
        self.assertIn(self.code("non_unique_offset"), self.gate.named_codes)


# --------------------------------------------------------------------------
# Induction 7 - a baseline-kind collision the program forced to same
# --------------------------------------------------------------------------

class ABaselineKindCollisionWasForcedToSame(GateCase):

    def marks(self) -> dict:
        paths = sorted((self.gate.paths.run_root / "cycles").glob(
            "*/contrast/*/marks.json"))
        for path in paths:
            body = json.loads(path.read_text(encoding="utf-8"))
            if body["cell"].endswith(self.gate.collision_case):
                return body
        raise AssertionError("the colliding cell was never marked")

    def test_the_canned_leg_declares_a_collision_its_own_replicates_do_not_bear(self):
        # The finding this class rests on, stated rather than assumed: the
        # shipped leg DECLARES a colliding case, and the baseline its own
        # replicates compute is empty for every register - so nothing the
        # canned marker can answer could ever collide.
        declared = self.gate.declared_leg
        colliding = [case for case, body in declared["cases"].items()
                     if body["collides_with_baseline"]]
        self.assertTrue(colliding)
        for case in sorted(declared["cases"]):
            cell = markprep_module.cell_from_contrast_leg(declared, case)
            markprep_module.write_baseline(
                cell, None, self.gate.root / "declared-baseline" / case)
            with self.subTest(case=case):
                self.assertEqual(
                    {register: kinds for register, kinds
                     in markprep_module.baseline_kinds(cell).items() if kinds},
                    {})

    def test_the_gates_own_baseline_really_exhibits_the_kind(self):
        cell = markprep_module.cell_from_contrast_leg(
            self.gate.leg, self.gate.collision_case,
            addresses=self.gate.leg["addresses"],
            objection_ids=self.gate.leg["objection_ids"])
        markprep_module.write_baseline(
            cell, None, self.gate.root / "assert-baseline")
        self.assertIn(self.gate.collision_kind,
                      markprep_module.baseline_kinds(cell)[self.gate.collision_register])
        self.assertTrue(
            any(factory.inner.answered for factory in self.gate.walk_factories),
            "the gate never supplied the colliding answer")

    def test_the_program_wrote_same_and_named_the_kind_it_came_from(self):
        body = self.marks()
        comparison = sorted(body["comparisons"])[0]
        row = body["comparisons"][comparison]["registers"][
            self.gate.collision_register]
        self.assertEqual(row["mark"], "same")
        self.assertEqual(row["source"], "program")
        self.assertIsNone(row["difference_kind"])
        self.assertTrue(row["forced_by"])
        self.assertEqual(row["evidence"]["downgraded_from_kind"],
                         self.gate.collision_kind)
        self.assertEqual(row["block"], self.code("baseline_kind_collision"))

    def test_the_closing_register_names_the_forced_same_by_code(self):
        row = self.register_row("baseline-forced-same")
        self.assertIsNotNone(row)
        _count, cells = row
        self.assertNotEqual(cells, "-")
        self.assertIn(self.code("baseline_kind_collision"), self.gate.named_codes)


# --------------------------------------------------------------------------
# Induction 8 - a re-read refused for want of a reopen_reason
# --------------------------------------------------------------------------

class AReReadWasRefusedForWantOfAReopenReason(GateCase):

    def test_the_reopen_entry_refused_by_code_and_exited_non_zero(self):
        self.assertEqual(self.gate.reopen_exit, 1)
        self.assertIn(self.code("reread_without_reason"),
                      self.gate.outputs["reopen_stderr"])

    def test_the_refusal_is_on_the_runs_own_record(self):
        refusals = self.gate.state["refusals"]
        self.assertEqual([row["code"] for row in refusals],
                         [self.code("reread_without_reason")])
        self.assertEqual(refusals[0]["entry"], "reopen")

    def test_the_later_cycle_re_read_no_spent_row_without_a_reason(self):
        # The reading tree is the run's, not the cycle's: with no reopen reason
        # in force the second cycle reads what is left and re-reads nothing.
        read_steps = [row for row in self.gate.rows() if row["kind"] == "READ"]
        self.assertGreaterEqual(len(read_steps), 2)
        self.assertIn("already_read", read_steps[-1]["outputs_sha256"])
        self.assertIn("reopen_reason", read_steps[-1]["outputs_sha256"])

    def test_the_closing_receipt_names_the_refusal_by_code(self):
        self.assertIn(self.code("reread_without_reason"), self.gate.named_codes)


# --------------------------------------------------------------------------
# Induction 9 - an appellate ruling flips a label through pass 1
# --------------------------------------------------------------------------

class AnAppellateRulingFlippedALabelThroughPassOne(GateCase):

    def test_staging_alone_moved_nothing(self):
        self.assertEqual(self.gate.staged["applies_at"], "next-run")
        self.assertEqual(self.gate.before_appeal["bearing"], Status.ACCEPTED)
        self.assertEqual(self.gate.before_appeal["reading"], Status.ACCEPTED)
        self.assertEqual(self.gate.before_appeal["rulings"], ())

    def test_the_next_invocation_flipped_the_label_through_pass_one(self):
        after = self.gate.after_appeal
        self.assertEqual(after["bearing"], Status.REFUTED)
        self.assertEqual(after["reading"], Status.REFUTED)
        self.assertEqual(after["cell"], graph_module.UNRESOLVED)
        self.assertEqual(len(after["rulings"]), 1)

    def test_it_flipped_that_bearing_and_no_other(self):
        # The ruling names one ν_bearing.  Every other bearing the reading arm
        # registered stands exactly where it stood: a label that moved for some
        # other reason moved through some other instrument, and a ruling that
        # reached further than the node it named would be the thing to catch.
        before = self.gate.before_appeal["bearings"]
        after = self.gate.after_appeal["bearings"]
        self.assertEqual(sorted(before), sorted(after))
        moved = [key for key in before if before[key] != after[key]]
        self.assertEqual(moved, [self.gate.target["row_key"]])
        self.assertEqual(before[self.gate.bystander["row_key"]], Status.ACCEPTED)
        self.assertEqual(after[self.gate.bystander["row_key"]], Status.ACCEPTED)

    def test_the_outcome_is_named_by_code_in_the_closing_receipt(self):
        applied = self.gate.state["applied_rulings"]
        self.assertEqual([row["outcome"] for row in applied],
                         [self.code("appellate_ruling")])
        self.assertIn(self.code("appellate_ruling"), self.gate.named_codes)
        self.assertIn(self.code("appellate_ruling"), loop_types.OUTCOME_CODES)


# --------------------------------------------------------------------------
# The clause itself - every induced failure named by code
# --------------------------------------------------------------------------

class TheClosingReceiptNamesEveryInducedFailureByCode(GateCase):

    def test_every_named_induction_is_in_the_closing_receipt(self):
        missing = [token for token in NAMED
                   if self.code(token) not in self.gate.named_codes]
        self.assertEqual(missing, [],
                         f"the closing receipt does not name {missing}; it "
                         f"names {sorted(self.gate.named_codes)}")

    def test_each_code_belongs_to_exactly_one_of_the_owners_tables(self):
        for token in NAMED:
            code = self.code(token)
            with self.subTest(token=token):
                tables = [code in loop_types.FAILURE_CODES,
                          code in loop_types.OUTCOME_CODES,
                          code in loop_types.BLOCK_CODES]
                self.assertEqual(tables.count(True), 1, code)

    def test_the_named_section_is_minted_from_the_runs_own_record(self):
        names = self.gate.state["closing_names"]
        self.assertTrue(names)
        for line in names:
            self.assertIn(line, self.gate.closing_text)
        self.assertIn(auto_loop.RECORDED_FAILURES_HEADING, self.gate.closing_text)
        self.assertIn(auto_loop.RECORDED_FAILURES_SENTENCE, self.gate.closing_text)


# --------------------------------------------------------------------------
# The metric-creep lens (ruling 7)
# --------------------------------------------------------------------------

class TheMetricCreepLens(GateCase):
    """Ruling 7, over the two artifacts this wave put a sentence into."""

    FORBIDDEN = ("score", "scored", "rank", "ranked", "ranking", "weighted",
                 "aggregate", "percent", "rate", "average", "mean", "tally",
                 "majority", "vote", "exhaustion")

    def added_sections(self) -> str:
        """The closing record's two driver-written sections, and only those.

        The rendered body is W3-REPORT's and its own scans govern it - and it
        must be excluded from a bare word lens, because the frozen ceiling's
        own text *denies* ranking, weighting and exhaustion by naming them.
        The lens that belongs to this wave is over the text this wave's driver
        writes.
        """

        marker = "## " + auto_loop.ARMS_ENDED_HEADING
        self.assertIn(marker, self.gate.closing_text)
        return self.gate.closing_text.split(marker, 1)[1]

    def test_the_sections_this_wave_added_carry_no_measure(self):
        lowered = self.added_sections().lower()
        for word in self.FORBIDDEN:
            with self.subTest(word=word):
                self.assertIsNone(re.search(r"\b" + word + r"\b", lowered), word)
        self.assertIsNone(re.search(r"\bx\d+\b", lowered),
                          "a count entered a section that is not the register")

    def test_the_owners_own_scans_pass_over_the_whole_record(self):
        standard_module.assert_no_exhaustion_claim(self.gate.closing_text,
                                                   "CLOSING.md")
        standard_module.assert_no_scoring_headers(self.gate.closing_text)
        contracts_module.assert_no_scoring_keys(
            report_module.rendered_files_record(
                {"CLOSING.md": self.gate.closing_text}))

    def test_the_only_counts_in_the_closing_record_are_the_registers_own(self):
        # The frozen ceiling requires the block register "printed with counts";
        # there is one such count per heading and nowhere else in the record.
        counts = re.findall(r"`[a-z-]+` x(\d+)", self.gate.closing_text)
        self.assertEqual(len(counts), len(report_module.BLOCK_REGISTER_HEADINGS))

    def test_the_verdict_carries_no_measure(self):
        blob = json.dumps(self.gate.verdict).lower()
        for word in self.FORBIDDEN:
            with self.subTest(word=word):
                self.assertIsNone(re.search(r"\b" + word + r"\b", blob), word)
        self.assertEqual(self.gate.verdict["refused"]["code"], "STEP_TIMEOUT")

    def test_every_stopping_decision_names_the_owners_vocabulary(self):
        decisions = sorted((self.gate.paths.run_root / "cycles").glob(
            "*/decision.json"))
        self.assertTrue(decisions)
        for path in decisions:
            body = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(decision=path.parent.name):
                if body.get("stop"):
                    self.assertIn(body["reason"], loop_types.STOP_REASONS)
                standard_module.assert_no_exhaustion_claim(body["text"],
                                                          path.name)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
