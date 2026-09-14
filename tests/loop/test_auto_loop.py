"""W5-DRIVER: the S0-S15 walk, driven over the real modules, offline.

Every class is named for one clause of the W5-DRIVER acceptance list and every
test in it is one reading of that clause.

**Nothing here is a fake.**  The driver is wired to the real ``trial``,
``audits``, ``report``, ``reader``, ``marker``, ``decide``, ``steps``,
``synthetic``, ``publish``, ``receipts`` and ``custody``, to the real
``graph_import_h005`` and ``use_relation_h005``, and to runner v2 imported
in-process.  Every git operation runs through ``publish()`` against a real
temporary **bare** repository, so ``VERIFIED`` is exercised rather than stubbed.
The one seam bound is ``provider_factory`` - W6-DRYRUN's own - which replaces
the transport and nothing else: every guard, pack, write-once record and custody
check is the real one, and the socket layer is removed from under all of it.

Two fixture facts worth their own sentences, because they are findings and not
conveniences:

* **The fixture checkout carries its own runner v2 and the process imports
  THAT copy.**  ``required_paths`` publishes ``Path(__file__).resolve()`` -
  runner v2's own source - as an input of every wave and resolves it inside the
  repository it is dispatching for, so a runner imported from somewhere else
  cannot send for this tree.  One process holds one runner (design 4.6), so the
  fixture installs the tree's copy under the one canonical name and restores the
  previous module afterwards.  This answers WAVE3 §8 question 7 in the concrete:
  the loop cannot run from a wheel while runner v2 publishes its own path.
* **``synthetic.canned_responses`` scripts no ``#order-swapped`` coordinate**,
  and its loose fallback hands the second judge seat an empty script (so every
  swapped ruling would be ``blocked:provider``).  The fixture answers the
  swapped presentation from the seat's own script - a scripted seat answering
  alike in both orders is a seat that did not flip, which is what G6 asks - and
  §8 of the wave-5 interface routes the gap to W6-DRYRUN.
"""
from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
import json
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from deepreason_core.ontology import Status

from minireason import provider_openai_compat as transport
from minireason.loop import custody
from minireason.loop import decide as decide_module
from minireason.loop import graph as graph_module
from minireason.loop import markprep as markprep_module
from minireason.loop import roles as roles_module
from minireason.loop import seats as seats_module
from minireason.loop import standard as standard_module
from minireason.loop import steps as steps_module
from minireason.loop import synthetic
from minireason.loop.types import FAILURE_CODES, BLOCK_CODES, LoopConfig, LoopError
from minireason.loop.types import OUTCOME_CODES, run_paths

REPOSITORY = Path(__file__).resolve().parents[2]
DRIVER_SOURCE = REPOSITORY / "tools" / "auto_loop.py"
RUNNER_NAME = "tools.multicycle_commitment_study_multi_v2"

_spec = importlib.util.spec_from_file_location("auto_loop", DRIVER_SOURCE)
auto_loop = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("auto_loop", auto_loop)
_spec.loader.exec_module(auto_loop)


# --------------------------------------------------------------------------
# The socket guard and the provider-module counter (design 4.7)
# --------------------------------------------------------------------------

class _SocketsUsed(AssertionError):
    """Raised the instant anything in the process reaches for a socket."""


_PRISTINE = (socket.socket, socket.create_connection, transport._open)


def _refuse_socket(*_args, **_kwargs):
    raise _SocketsUsed("a test opened a socket")


class ProviderCounter:
    """The provider module's own count of live transports and opened requests.

    Two numbers, both read off ``provider_openai_compat`` itself: how many
    ``OpenAICompatProvider`` objects were constructed (a live transport bound to
    an endpoint) and how many times ``_open`` - the module's one urlopen - was
    entered.  A dry run asserts both are zero; the ``OfflineProvider`` count is
    printed beside them so "nothing ran" and "only the offline provider ran" are
    two different statements.
    """

    def __init__(self) -> None:
        self.live = 0
        self.offline = 0
        self.opened = 0


@contextlib.contextmanager
def no_sockets(counter: ProviderCounter):
    live_init = transport.OpenAICompatProvider.__init__
    offline_init = transport.OfflineProvider.__init__

    def counted_live(self, *args, **kwargs):
        counter.live += 1
        return live_init(self, *args, **kwargs)

    def counted_offline(self, *args, **kwargs):
        counter.offline += 1
        return offline_init(self, *args, **kwargs)

    def counted_open(*args, **kwargs):
        counter.opened += 1
        raise _SocketsUsed("the provider module opened a request")

    transport.OpenAICompatProvider.__init__ = counted_live
    transport.OfflineProvider.__init__ = counted_offline
    socket.socket = socket.create_connection = _refuse_socket
    transport._open = counted_open
    try:
        yield counter
    finally:
        transport.OpenAICompatProvider.__init__ = live_init
        transport.OfflineProvider.__init__ = offline_init
        socket.socket, socket.create_connection, transport._open = _PRISTINE


# --------------------------------------------------------------------------
# The fixture
# --------------------------------------------------------------------------

RUN_ID = "RUN-W5-GATE"

#: The six ``types.PINNED_SOURCE_PATHS`` plus the two further sources runner
#: v2's ``runtime_pins`` digests.  Every one is copied from this checkout, so the
#: fixture's pins are real bytes and a moved pin is a real custody event.
FIXTURE_SOURCES = (
    "src/minireason/graph_import_h005.py",
    "src/minireason/provider_openai_compat.py",
    "src/minireason/use_relation_h005.py",
    "tools/contrast_triple_study.py",
    "tools/multicycle_commitment_study_multi_v2.py",
    "src/minireason/provider.py",
    "tools/multicycle_language_probe.py",
    # The loop sources the plan pins by path beside its module constants: the
    # declared resource conditions are ``roles``' (CLONE-PATCH item 4) and the
    # stop rule is ``decide``'s, so a fixture whose tree lacks them cannot show
    # the pin being verified against bytes.
    "src/minireason/loop/roles.py",
    "src/minireason/loop/decide.py",
    "src/minireason/loop/standard.py",
    "src/minireason/loop/audits.py",
    "src/minireason/loop/data/ceiling_v1.md",
    # design 4.5: the activity logger is SHELLED and never reimplemented, so a
    # tree the loop runs in carries it.
    "tools/repo_activity.py",
)

#: Five seats over five lineages and five credentials.  The key_env NAMES are
#: this wave's own: runner v2's ``key_gate`` registry is process-wide and refuses
#: one credential at two caps, so nothing here reuses ``SYNTHETIC_*_KEY``.
SEATS = (("w5/critic", "w5-critic-lineage", "W5_CRITIC_KEY"),
         ("w5/defender", "w5-defender-lineage", "W5_DEFENDER_KEY"),
         ("w5/judge-a", "w5-judge-a-lineage", "W5_JUDGE_A_KEY"),
         ("w5/judge-b", "w5-judge-b-lineage", "W5_JUDGE_B_KEY"),
         ("w5/variator", "w5-variator-lineage", "W5_VARIATOR_KEY"))


def seat_registry_document() -> dict:
    return {"schema_version": "minireason.endpoints.v1",
            "endpoints": [
                {"name": name,
                 "base_url": "https://%s.invalid/v1" % name.split("/")[-1],
                 "model": "model-" + name.split("/")[-1], "key_env": key_env,
                 "family": family, "chat_path": "/chat/completions",
                 "native": False, "max_concurrency": 5, "timeout_seconds": 120}
                for name, family, key_env in SEATS]}


def reading_key(identity) -> str:
    coordinate, record, field, verbatim = identity
    return f"h005-row/{coordinate}#{record}/{field}/{verbatim}"


class GateProviders:
    """``synthetic.ScriptedProviders`` addressed by the driver's coordinates.

    The driver mints an admissible coordinate for each pre-registered row
    (``auto_loop.cell_key_for``); the synthetic script is keyed by its own row
    names.  This maps one onto the other and changes nothing else: the reply the
    guard reads is the script's own, and every guard runs on it.
    """

    SWAP = "#order-swapped"

    def __init__(self, mapping, *, seed=synthetic.DEFAULT_SEED, induce=()):
        self.inner = synthetic.ScriptedProviders(seed=seed, induce=induce)
        self.mapping = dict(mapping)
        self.seen: list[tuple[str, str]] = []

    def _translate(self, coordinate: str) -> str:
        if coordinate.endswith(self.SWAP):
            coordinate = coordinate[:-len(self.SWAP)]
        for prefix in sorted(self.mapping, key=len, reverse=True):
            if coordinate == prefix or coordinate.startswith(prefix + "#"):
                return self.mapping[prefix] + coordinate[len(prefix):]
        parts = coordinate.split("/")
        if len(parts) >= 4 and parts[0] == "contrast":
            return f"mark/{parts[1]}/{parts[3]}/rep-1"
        return coordinate

    @staticmethod
    def _seat(role: str, seat) -> str | None:
        # W2-ROLES hands the factory the coordinate TOKEN (``judge#1@<key>``);
        # the synthetic script is keyed by its own two judge seat names.
        if role != "judge" or not seat:
            return None
        label = str(seat).split("@", 1)[0]
        index = 1
        if "#" in label:
            try:
                index = int(label.rsplit("#", 1)[1])
            except ValueError:
                index = 1
        return synthetic.JUDGE_SEATS[min(index, len(synthetic.JUDGE_SEATS)) - 1]

    def provider(self, role, coordinate, records_dir, *, seat=None, endpoint=None):
        self.seen.append((role, coordinate))
        return self.inner.provider(role, self._translate(coordinate), records_dir,
                                   seat=self._seat(role, seat), endpoint=endpoint)

    def __call__(self, endpoint, records_dir):
        return self.inner(endpoint, records_dir)


class DriverFixture(unittest.TestCase):
    """One run tree under ``tempfile``, with a real bare git remote.

    Nothing outside the temporary directory is written, and the runner module
    the process holds is restored when the test ends.
    """

    INDUCE: tuple[str, ...] = ()
    CONTRAST = False
    BUDGET = 2

    def setUp(self) -> None:
        super().setUp()
        self.counter = ProviderCounter()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.repo = self.root / "checkout"
        self._build_tree()
        self.paths = run_paths(self.repo, RUN_ID)
        self.mapping = {auto_loop.cell_key_for(reading_key(identity)): name
                        for name, identity in synthetic.READING_COORDINATES.items()}
        self.factory = GateProviders(self.mapping, induce=self.INDUCE)

    # -- the tree ---------------------------------------------------------

    def _git(self, where: Path, *argv: str) -> None:
        subprocess.run(["git", "-C", str(where), *argv], check=True,
                       capture_output=True)

    def _install_runner(self) -> None:
        previous = (sys.modules.get(RUNNER_NAME), seats_module._RUNNER)
        spec = importlib.util.spec_from_file_location(
            RUNNER_NAME, self.repo / "tools" / "multicycle_commitment_study_multi_v2.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[RUNNER_NAME] = module
        spec.loader.exec_module(module)
        module.set_registry(synthetic.endpoints_registry())
        seats_module._RUNNER = module
        self.runner = module

        def restore() -> None:
            if previous[0] is None:
                sys.modules.pop(RUNNER_NAME, None)
            else:
                sys.modules[RUNNER_NAME] = previous[0]
            seats_module._RUNNER = previous[1]

        self.addCleanup(restore)

    def _build_tree(self) -> None:
        self._git(self.root, "init", "--bare", "--initial-branch=main", str(self.remote))
        self._git(self.root, "init", "--initial-branch=main", str(self.repo))
        for key, value in (("user.name", "W5 gate"),
                           ("user.email", "w5-gate@example.invalid"),
                           ("commit.gpgsign", "false"),
                           ("core.autocrlf", "false")):
            self._git(self.repo, "config", key, value)
        for rel in FIXTURE_SOURCES:
            path = self.repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((REPOSITORY / rel).read_bytes())
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
                 "statement": "the audit record in force is not older than AUDIT_PERIOD cycles",
                 "check": "audit_in_force"},
                {"id": "p7", "set": "P",
                 "statement": "no reading mints an att or dep edge on a node under study",
                 "check": "no_edges_on_studied_nodes"},
            ]}).encode())
        (run_root / "calibration.json").write_bytes(json.dumps({
            "schema": "minireason.loop.calibration.v1",
            "rows": [], "error_rule": "one wrong anchor is one error"}).encode())

        self._install_runner()
        occurrence = self.repo / "occurrence-01"
        occurrence.mkdir(parents=True, exist_ok=True)
        (occurrence / "material.json").write_bytes(
            json.dumps(synthetic.material_document(), sort_keys=True).encode())
        (occurrence / "arms.json").write_bytes(
            json.dumps(synthetic.arms_document(), sort_keys=True).encode())
        self.runner.initialize(self.repo, occurrence,
                               occurrence / "material.json",
                               occurrence / "arms.json")
        if self.CONTRAST:
            leg = self.repo / "contrast-study" / "occurrence-01"
            leg.mkdir(parents=True, exist_ok=True)
            (leg / "contrast.json").write_bytes(
                json.dumps(synthetic.contrast_leg()).encode())

        self.config_path = self.repo / "loop-config.json"
        self.config_path.write_bytes(
            json.dumps(self.config_body(), indent=1).encode())
        self._git(self.repo, "add", "--", ".")
        self._git(self.repo, "commit", "-m", "the published tree")
        self._git(self.repo, "remote", "add", "origin", str(self.remote))
        self._git(self.repo, "push", "--set-upstream", "origin", "HEAD:refs/heads/main")

    def config_body(self, **overrides) -> dict:
        body = {
            "schema": "minireason.loop.config.v1",
            "run_id": RUN_ID,
            "study": "the W5-DRIVER acceptance gate over the synthetic occurrence",
            "occurrences": ["occurrence-01"],
            "runner": "tools/multicycle_commitment_study_multi_v2.py",
            "publish_ref": "origin/main",
            "cycle_budget": self.BUDGET,
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
            "contrast": ({"attached": True, "study": "contrast-study",
                          "occurrences": ["contrast-study/occurrence-01"]}
                         if self.CONTRAST else {"attached": False}),
            "provider_mode": "offline",
        }
        body.update(overrides)
        return body

    # -- driving ----------------------------------------------------------

    def modules(self, **overrides) -> auto_loop.Modules:
        table = {"provider_factory": self.factory, "repo_root": self.repo,
                 "sleep": lambda _seconds: None}
        table.update(overrides)
        return auto_loop.Modules(**table)

    def config(self) -> LoopConfig:
        return LoopConfig.load(self.config_path)

    def walk(self, *, preflight=True, **kwargs):
        """S0, S1 and S2..S15, all inside the socket guard."""

        modules = kwargs.pop("modules", None) or self.modules()
        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=modules)
            if preflight:
                auto_loop.preflight(self.config_path, modules=modules)
            return auto_loop.run(self.config_path, modules=modules, **kwargs)

    def ledger(self) -> steps_module.StepLedger:
        plan = json.loads(self.paths.plan.read_text(encoding="utf-8"))
        return steps_module.StepLedger(self.paths.run_root, plan["loop_plan_id"])

    def kinds(self) -> list[str]:
        return [row.receipt.kind for row in self.ledger().records()]

    def receipt(self, index: int, kind: str) -> dict:
        return json.loads(self.paths.step_path(index, kind).read_text(encoding="utf-8"))

    def plan(self) -> dict:
        return json.loads(self.paths.plan.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# Clause 1 - one command walks S0 to S15 offline with zero sockets
# --------------------------------------------------------------------------

class OneCommandWalksSZeroToSFifteenOffline(DriverFixture):

    def test_every_step_is_bracketed_in_the_activity_log(self):
        self.walk()
        log = self.repo / "docs" / "AGENT_ACTIVITY.jsonl"
        self.assertTrue(log.is_file(), "no activity record was written")
        rows = [json.loads(line) for line in
                log.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertTrue(rows)
        # Design 4.5's list is "every search, read, modification, test and
        # dispatch": the acts this driver performs on the repository are the
        # publications and the dispatch, and each is here twice — once begun,
        # once outcome.  A step that writes only inside the run's own tree has
        # its write-once receipt and is not recorded a second time.
        actions = {row["action"] for row in rows}
        for kind in ("PUBLISH_PLAN", "PUBLISH_IN", "PUBLISH_EV", "PUBLISH_CY"):
            with self.subTest(kind=kind):
                self.assertIn(f"publish {kind}", actions)
        self.assertIn("loop step SEND", actions)
        self.assertNotIn("loop step READ", actions)
        for action in actions:
            with self.subTest(action=action):
                self.assertEqual(
                    len([r for r in rows if r["action"] == action
                         and r["phase"] == "begin"]),
                    len([r for r in rows if r["action"] == action
                         and r["phase"] == "outcome"]))
        for row in rows:
            self.assertEqual(row["agent"], "auto_loop")
            self.assertRegex(row["decision"], r"\AREC-\d{8}-[A-Z]+\Z")
            self.assertIn(row["phase"], ("begin", "outcome"))
            # never raw command text (design 4.5)
            self.assertNotIn("command", row)

    def test_the_walk_reaches_s15_and_the_provider_module_opened_nothing(self):
        result = self.walk()
        self.assertEqual(result["cycles_completed"], 2)
        self.assertEqual(self.counter.opened, 0, "the provider module opened a request")
        self.assertEqual(self.counter.live, 0, "a live transport was constructed")
        self.assertGreater(self.counter.offline, 0,
                           "no provider ran at all; the walk proved nothing")
        self.assertTrue(self.paths.closing.is_file())

    def test_every_state_s2_to_s15_filed_exactly_one_receipt_in_order(self):
        self.walk()
        kinds = self.kinds()
        self.assertEqual(kinds[0], "PUBLISH_PLAN")
        self.assertEqual(kinds.count("CLOSE"), 1)
        for cycle_kind in ("CYCLE_OPEN", "IMPORT", "USE_TABLE", "READ", "MARK",
                           "ADJUDICATE", "DECIDE"):
            self.assertEqual(kinds.count(cycle_kind), 2, cycle_kind)
        first = kinds.index("CYCLE_OPEN")
        self.assertEqual(
            kinds[first:first + 6],
            ["CYCLE_OPEN", "PREPARE", "PUBLISH_IN", "SEND", "PUBLISH_EV", "PREPARE"])
        # one receipt per step key, and every one of them write-once
        indices = [row.index for row in self.ledger().records()]
        self.assertEqual(len(indices), len(set(indices)))

    def test_the_closing_record_carries_every_required_ceiling_sentence(self):
        self.walk()
        closing = self.paths.closing.read_text(encoding="utf-8")
        for sentence in standard_module.CEILING_REQUIRED_SENTENCES:
            self.assertIn(sentence, closing)
        standard_module.assert_no_exhaustion_claim(closing, "CLOSING.md")

    def test_the_state_walk_is_the_declared_one(self):
        self.assertEqual(len(auto_loop.STATE_RESPONSIBILITIES), 16)
        self.assertEqual(auto_loop.STATE_RESPONSIBILITIES[0][:2], ("S0", "PREREGISTER"))
        self.assertEqual(auto_loop.STATE_RESPONSIBILITIES[-1][:2], ("S15", "CLOSE"))
        for label, kind, function in auto_loop.STATE_RESPONSIBILITIES:
            with self.subTest(state=label):
                self.assertRegex(label, r"\AS\d{1,2}\Z")
                self.assertTrue(hasattr(auto_loop, function.split("/")[0]))

    def test_the_run_wrote_nothing_outside_its_own_tree(self):
        self.walk()
        inside = {p for p in self.repo.rglob("*") if ".git" not in p.parts}
        for path in inside:
            self.assertTrue(str(path).startswith(str(self.repo)))
        self.assertFalse((REPOSITORY / "experiments" / "loops" / RUN_ID).exists())


# --------------------------------------------------------------------------
# Clause 2 - publication precedes every dispatch; a PublishPending blocks it
# --------------------------------------------------------------------------

class PublicationPrecedesEveryDispatch(DriverFixture):

    def test_every_send_is_preceded_by_a_verified_publication(self):
        self.walk()
        records = self.ledger().records()
        seen_plan = seen_inputs = False
        for row in records:
            if row.receipt.kind == "SEND":
                self.assertTrue(seen_plan and seen_inputs,
                                "a dispatch preceded its publication")
            if row.receipt.kind == "PUBLISH_PLAN" and row.receipt.status == "COMPLETE":
                seen_plan = True
            if row.receipt.kind == "PUBLISH_IN" and row.receipt.status == "COMPLETE":
                seen_inputs = True
        verified = sorted(p.name for p in self.paths.steps.glob("*.verified"))
        self.assertTrue(verified, "no VERIFIED line was written")
        for name in verified:
            line = (self.paths.steps / name).read_text(encoding="utf-8")
            self.assertTrue(line.startswith("VERIFIED "), line)

    def test_a_publish_pending_blocks_the_next_dispatch(self):
        # A real rejected push: a second clone advances the ref, so the driver's
        # non-forcing push is refused and the publication is PENDING.  Nothing
        # is stubbed and no publisher is injected.
        other = self.root / "other"
        subprocess.run(["git", "clone", str(self.remote), str(other)],
                       check=True, capture_output=True)
        for key, value in (("user.name", "someone else"),
                           ("user.email", "other@example.invalid"),
                           ("commit.gpgsign", "false")):
            self._git(other, "config", key, value)
        (other / "MOVED.md").write_text("the ref moved under this run\n")
        self._git(other, "add", "--", "MOVED.md")
        self._git(other, "commit", "-m", "advance the ref")
        self._git(other, "push", "origin", "HEAD:refs/heads/main")

        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=self.modules())
            with self.assertRaises(steps_module.PublishBlocked):
                auto_loop.run(self.config_path, modules=self.modules())
        body = self.receipt(1, "PUBLISH_PLAN")
        self.assertEqual(body["status"], "FAILED")
        self.assertEqual(body["failure_code"], "PUBLISH_PENDING")
        self.assertEqual(self.kinds(), ["PUBLISH_PLAN"],
                         "a step ran after a pending publication")
        with self.assertRaises(steps_module.PublishBlocked):
            self.ledger().run_step("SEND", 1, {"cycle": 1}, lambda _h: None)


# --------------------------------------------------------------------------
# Clause 3 - runner v2 is imported and send_round is called in-process
# --------------------------------------------------------------------------

class RunnerV2IsImportedAndSendRoundIsCalledInProcess(DriverFixture):

    def test_send_round_is_called_in_process_and_nothing_but_git_is_shelled(self):
        calls: list[int] = []
        original = self.runner.send_round
        spawned: list[str] = []
        original_run = subprocess.run
        original_popen = subprocess.Popen
        original_output = subprocess.check_output

        def watching_send_round(repo, outputs, **kwargs):
            calls.append(len(list(outputs)))
            return original(repo, outputs, **kwargs)

        def watching(argv, *args, **kwargs):
            spawned.append(" ".join(str(part) for part in argv)
                           if isinstance(argv, (list, tuple)) else str(argv))
            return original_run(argv, *args, **kwargs)

        def watching_popen(argv, *args, **kwargs):
            spawned.append(" ".join(str(part) for part in argv)
                           if isinstance(argv, (list, tuple)) else str(argv))
            return original_popen(argv, *args, **kwargs)

        def watching_output(argv, *args, **kwargs):
            spawned.append(" ".join(str(part) for part in argv)
                           if isinstance(argv, (list, tuple)) else str(argv))
            return original_output(argv, *args, **kwargs)

        self.runner.send_round = watching_send_round
        subprocess.run = watching
        subprocess.Popen = watching_popen
        subprocess.check_output = watching_output
        try:
            self.walk()
        finally:
            self.runner.send_round = original
            subprocess.run = original_run
            subprocess.Popen = original_popen
            subprocess.check_output = original_output
        self.assertTrue(calls, "send_round was never called")
        self.assertTrue(spawned, "no subprocess ran at all; the check is vacuous")
        logged = 0
        for argv in spawned:
            # Two programs, and design 4.5 names both: git, through publish(),
            # and the activity logger, which receipts.activity SHELLS rather
            # than reimplements.  The runner is never a program this driver
            # launches.  (``git show <sha>:tools/…`` names the runner's path as
            # a blob, which is publication reading it, not the driver running
            # it.)
            head = argv.split()[0]
            if "repo_activity.py" in argv:
                logged += 1
                self.assertNotIn("--command", argv)
                continue
            self.assertTrue(head.endswith("git"), argv)
        self.assertGreater(logged, 0, "no repository act was bracketed")

    def test_the_driver_resolves_the_runner_through_the_one_canonical_import(self):
        self.assertIs(auto_loop.runner_v2(), self.runner)
        self.assertIs(auto_loop.runner_v2(), seats_module.runner_module())


# --------------------------------------------------------------------------
# Clause 4 - a second driver on the same run is refused
# --------------------------------------------------------------------------

class ASecondDriverOnTheSameRunIsRefused(DriverFixture):

    def test_a_second_driver_on_the_same_run_is_refused(self):
        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=self.modules())
        first = steps_module.RunLock(self.paths.lock, self.plan()["loop_plan_id"])
        first.acquire()
        self.addCleanup(first.release)
        with self.assertRaises(steps_module.RunLocked) as caught:
            auto_loop.run(self.config_path, modules=self.modules())
        self.assertEqual(caught.exception.code, "RUN_LOCKED")

    def test_the_lock_is_released_when_the_run_ends(self):
        self.walk()
        second = steps_module.RunLock(self.paths.lock, self.plan()["loop_plan_id"])
        second.acquire()
        second.release()


# --------------------------------------------------------------------------
# Clause 5 - --cycles may only lower the budget
# --------------------------------------------------------------------------

class CyclesMayOnlyLowerTheBudget(DriverFixture):

    def test_an_upward_override_is_budget_raised(self):
        config = self.config()
        with self.assertRaises(LoopError) as caught:
            auto_loop.effective_budget(config, config.cycle_budget + 1)
        self.assertEqual(caught.exception.code, "BUDGET_RAISED")
        self.assertEqual(auto_loop.effective_budget(config, 1), 1)
        self.assertEqual(auto_loop.effective_budget(config, None), config.cycle_budget)

    def test_the_cli_refuses_upward_before_anything_is_written(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            code = auto_loop.main(
                ["preregister", "--config", str(self.config_path), "--cycles", "9"],
                modules=self.modules())
        self.assertEqual(code, 1)
        self.assertIn("BUDGET_RAISED", stderr.getvalue())
        self.assertFalse(self.paths.plan.exists())

    def test_a_mode_or_a_ref_that_disagrees_with_the_frozen_config_is_refused(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            code = auto_loop.main(
                ["preregister", "--config", str(self.config_path),
                 "--mode", "live"], modules=self.modules())
        self.assertEqual(code, 1)
        self.assertIn("CONFIG_INVALID_VALUE", stderr.getvalue())
        stderr2 = io.StringIO()
        with redirect_stderr(stderr2):
            code = auto_loop.main(
                ["preregister", "--config", str(self.config_path),
                 "--publish-ref", "origin/somewhere-else"],
                modules=self.modules())
        self.assertEqual(code, 1)
        self.assertIn("CONFIG_INVALID_VALUE", stderr2.getvalue())
        self.assertFalse(self.paths.plan.exists())

    def test_a_lowered_budget_is_the_budget_the_run_honours(self):
        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=self.modules(),
                                  budget_override=1)
            result = auto_loop.run(self.config_path, modules=self.modules())
        self.assertEqual(result["cycles_completed"], 1)
        self.assertEqual(self.plan()["cycle_budget"], 1)
        self.assertEqual(self.kinds().count("CYCLE_OPEN"), 1)


# --------------------------------------------------------------------------
# Clause 6 - a killed run resumes without re-sending an asked coordinate
# --------------------------------------------------------------------------

class ResumeNeverResendsAnAskedCoordinate(DriverFixture):

    def test_a_killed_spending_step_halts_on_resume_and_re_enters_nothing(self):
        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=self.modules())
        # Kill mid-SEND: the open marker stands on disk and the process is gone.
        ledger = self.ledger()
        handle = ledger.begin("SEND", cycle=1, inputs={"cycle": 1, "wave": "wave0001"},
                              wave="wave0001")
        key = handle.step_key
        self.assertTrue(any(name.endswith(".json.open")
                            for name in (p.name for p in self.paths.steps.iterdir())))
        sent: list[str] = []
        original = self.runner.send_round

        def watching(repo, outputs, **kwargs):
            sent.append("dispatched")
            return original(repo, outputs, **kwargs)

        self.runner.send_round = watching
        self.addCleanup(setattr, self.runner, "send_round", original)
        with no_sockets(self.counter):
            with self.assertRaises(steps_module.UnresolvedStep):
                auto_loop.run(self.config_path, modules=self.modules())
        self.assertEqual(sent, [], "a step with an unresolved marker was re-entered")

        with no_sockets(self.counter):
            auto_loop.run(self.config_path, modules=self.modules(),
                          acknowledge=key,
                          reason="the provider log shows no dispatch for this wave")
        self.assertTrue(sent, "the acknowledged run never dispatched")
        # No coordinate carries a request or attempt without a response.
        for occurrence in (self.repo / "occurrence-01",):
            scan = steps_module.scan_coordinates(occurrence)
            self.assertEqual(sorted(scan.indeterminate), [])

    def test_a_claimed_reading_coordinate_is_reported_indeterminate_and_not_resent(self):
        self.walk()
        # Claim a coordinate by hand, exactly as a killed reader leaves one, and
        # re-read under a pre-registered reason: the row is INDETERMINATE and
        # never re-sent.
        row_key = self.config().reading_set[0]
        claim = custody.fenced(self.paths.readings, row_key)
        coordinate = roles_module.Coordinate(
            role="critic", key=auto_loop.cell_key_for(row_key) + "#reread")
        # W2-ROLES claims a coordinate by making its directory and its
        # ``provider`` subdirectory BEFORE anything can be sent; a claim with no
        # call record beside it is exactly section 4.3's asked-and-unanswered.
        (claim / coordinate.slug / "provider").mkdir(parents=True, exist_ok=True)
        from minireason.loop import reader as reader_module
        claimed = reader_module.unanswered_coordinates(claim)
        self.assertTrue(claimed, "a claim with no call record read as answered")
        # And the two layouts really are two: W1-STEPS' scan of the dispatch
        # tree sees nothing here (WAVE4-INTERFACE section 8, question 2).
        self.assertEqual(sorted(steps_module.scan_coordinates(claim).indeterminate),
                         [])


# --------------------------------------------------------------------------
# Clause 7 - a custody mismatch halts before dispatch, with an erratum,
#            a non-zero exit, and stays sticky until acknowledged
# --------------------------------------------------------------------------

class ACustodyMismatchHaltsBeforeDispatch(DriverFixture):

    def test_a_moved_pin_halts_at_the_cycle_open_with_an_erratum_and_stays_sticky(self):
        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=self.modules())
        moved = self.repo / "src/minireason/use_relation_h005.py"
        original = moved.read_bytes()
        moved.write_bytes(original + b"\n# the file moved under the plan\n")

        stderr = io.StringIO()
        with redirect_stderr(stderr), no_sockets(self.counter):
            code = auto_loop.main(["run", "--config", str(self.config_path)],
                                  modules=self.modules())
        self.assertEqual(code, 1)
        self.assertIn("SOURCE_PIN_MISMATCH", stderr.getvalue())
        kinds = self.kinds()
        self.assertIn("CYCLE_OPEN", kinds)
        self.assertNotIn("SEND", kinds, "a dispatch step ran after a custody halt")
        halted = [row for row in self.ledger().records()
                  if row.receipt.status == "HALTED"]
        self.assertEqual(len(halted), 1)
        self.assertEqual(halted[0].receipt.kind, "CYCLE_OPEN")
        self.assertEqual(halted[0].receipt.failure_code, "SOURCE_PIN_MISMATCH")
        stubs = sorted(p.name for p in self.paths.errata.iterdir())
        self.assertTrue(stubs, "a custody halt wrote no erratum")

        # Sticky: restoring the bytes is not enough; the halt stands until an
        # operator acknowledges it with a reason, which is itself recorded.
        moved.write_bytes(original)
        stderr2 = io.StringIO()
        with redirect_stderr(stderr2), no_sockets(self.counter):
            again = auto_loop.main(["run", "--config", str(self.config_path)],
                                   modules=self.modules())
        self.assertEqual(again, 1)
        # StickyHalt re-raises the halted receipt's OWN code, and says so.
        self.assertIn("SOURCE_PIN_MISMATCH", stderr2.getvalue())
        self.assertIn("sticky", stderr2.getvalue())

        with no_sockets(self.counter):
            result = auto_loop.run(
                self.config_path, modules=self.modules(),
                acknowledge=halted[0].receipt.step_key,
                reason="the pinned file was restored to its frozen bytes")
        self.assertEqual(result["cycles_completed"], 2)
        acknowledgements = self.ledger().acknowledgements()
        self.assertTrue(acknowledgements)
        self.assertIn("restored", json.dumps(list(acknowledgements)))


# --------------------------------------------------------------------------
# Clause 8 - a provider failure ends one arm, mints no warrant, and leaves
#            the other arms running
# --------------------------------------------------------------------------

class AProviderFailureEndsOneArm(DriverFixture):

    INDUCE = ("provider_arm_failure",)

    def test_one_arm_ends_by_its_own_code_and_the_others_keep_running(self):
        result = self.walk()
        state = json.loads((self.paths.run_root / "_run.json").read_text(encoding="utf-8"))
        ended = state["arms_ended"]
        self.assertEqual([row["arm"] for row in ended], [synthetic.PROSE_ARM])
        self.assertEqual(ended[0]["failure_code"],
                         synthetic.INDUCED_CODES["provider_arm_failure"])
        self.assertEqual(ended[0]["text"], auto_loop.ARM_ENDED_TEXT)
        # The other arm ran to its terminal node in the same cycle.
        terminal = (self.repo / "occurrence-01" / "responses" / "synth"
                    / synthetic.FCL_ARM / "cycle01" / "response.json")
        self.assertTrue(terminal.is_file(), "the surviving arm did not finish")
        self.assertEqual(result["cycles_completed"], 2)

    def test_the_ended_arm_mints_no_warrant_and_the_fixed_text_is_printed(self):
        self.walk()
        closing = self.paths.closing.read_text(encoding="utf-8")
        self.assertIn(auto_loop.ARM_ENDED_TEXT, closing)
        self.assertNotIn("overrun", closing)
        # No reading was registered for the ended arm's coordinates.
        harness = graph_module.open_graph(
            graph_module.resolve_graph_root(self.repo, self.config().graph_root),
            clock=graph_module.fixed_clock())
        for key, _body in graph_module.reading_bodies(harness):
            self.assertNotIn(synthetic.PROSE_ARM, str(key))

    def test_all_arms_ended_is_false_while_one_arm_is_still_running(self):
        self.walk()
        drv = auto_loop._load_driver_from_run(self.paths.run_root,
                                              self.modules())
        instrument = auto_loop._instrument(drv)
        self.assertFalse(instrument.arms_ended)
        self.assertIn(synthetic.PROSE_ARM, instrument.ended_arms)


# --------------------------------------------------------------------------
# Clause 9 - an appeal applied at the next invocation flips a label through
#            pass 1
# --------------------------------------------------------------------------

class AnAppealAppliedAtTheNextInvocationFlipsALabel(DriverFixture):

    def test_a_staged_ruling_is_applied_at_the_next_run_and_flips_the_label(self):
        self.walk()
        graph_root = graph_module.resolve_graph_root(self.repo,
                                                     self.config().graph_root)
        harness = graph_module.open_graph(graph_root, clock=graph_module.fixed_clock())
        standard_id = graph_module.register_standard(harness)
        cell = "appeal/target"
        graph_module.open_cells(harness, [cell])
        transcript = graph_module.Transcript(
            case="the later record re-deploys the earlier term without qualification",
            answer="the defence disputes that the two terms are the same term",
            decisive_point="without qualification",
            checks={"unique_offset": True})
        result = graph_module.ReadingResult(
            key=graph_module.CellKey(cell), relation="re-deploys",
            seat="judge#1", transcript=transcript, body={"offsets": [[0, 21]]})
        ids = graph_module.register_reading(harness, result, standard_id)
        self.assertEqual(harness.state.status[ids.reading], Status.ACCEPTED)

        ruling_path = self.root / "ruling.json"
        ruling_path.write_text(json.dumps({
            "ruling_id": "APP-001", "target": ids.bearing,
            "standard_id": standard_id,
            "ground": "the read does not bear on the claim offered",
            "reopen_reason": "appellate-ruling", "body": {}}), encoding="utf-8")
        staged = auto_loop.appeal(self.paths.run_root, path=ruling_path,
                                  modules=self.modules())
        self.assertEqual(staged["applies_at"], "next-run")

        # Staging alone does not move the label.
        cold = graph_module.open_graph(graph_root, clock=graph_module.fixed_clock())
        self.assertEqual(cold.state.status[ids.reading], Status.ACCEPTED)

        with no_sockets(self.counter):
            auto_loop.run(self.config_path, modules=self.modules())
        after = graph_module.open_graph(graph_root, clock=graph_module.fixed_clock())
        self.assertEqual(after.state.status[ids.bearing], Status.REFUTED)
        self.assertEqual(after.state.status[ids.reading], Status.REFUTED)
        self.assertEqual(graph_module.cell_state(after, cell), graph_module.UNRESOLVED)
        state = json.loads((self.paths.run_root / "_run.json").read_text(encoding="utf-8"))
        self.assertEqual(state["applied_rulings"][0]["outcome"],
                         "APPELLATE_RULING_APPLIED")

    def test_an_appeal_with_no_target_and_no_path_is_refused_by_code(self):
        self.walk()
        with self.assertRaises(LoopError) as caught:
            auto_loop.appeal(self.paths.run_root, path=None, modules=self.modules())
        self.assertEqual(caught.exception.code, "APPEAL_PATH_INVALID")
        empty = self.root / "empty.json"
        empty.write_text(json.dumps({"ruling_id": "x"}), encoding="utf-8")
        with self.assertRaises(LoopError) as second:
            auto_loop.appeal(self.paths.run_root, path=empty, modules=self.modules())
        self.assertEqual(second.exception.code, "APPEAL_TARGET_INVALID")


# --------------------------------------------------------------------------
# S0 stages the bundle before anything reads it (the first live run's finding)
# --------------------------------------------------------------------------

class TheBundleIsStagedBeforeAnythingReadsIt(DriverFixture):
    """The first live ``preregister`` ended in a bare ``FileNotFoundError``.

    ``config.obligations_path`` names where the file lives **under the run
    root**; the bundle that supplies it sits beside ``config.json``, and
    nothing had copied it in when ``_stage_bundle`` read it.  These tests put
    the bundle where a real pre-registration keeps it - a directory of its own,
    outside the run root - and take the run root away.
    """

    def bundle(self) -> Path:
        """The config and its bundle beside it, with an empty run root."""

        bundle = self.repo / "bundle"
        bundle.mkdir(parents=True, exist_ok=True)
        run_root = self.paths.run_root
        for name in ("obligations.json", "calibration.json"):
            (bundle / name).write_bytes((run_root / name).read_bytes())
            (run_root / name).unlink()
        config_path = bundle / "config.json"
        config_path.write_bytes(json.dumps(self.config_body(), indent=1).encode())
        return config_path

    def test_s0_stages_every_bundle_file_from_the_configs_own_directory(self):
        config_path = self.bundle()
        self.assertFalse(self.paths.obligations.is_file())
        with no_sockets(self.counter):
            out = auto_loop.preregister(config_path, modules=self.modules())
        for name in ("obligations.json", "calibration.json", "CEILING.md",
                     "config.json", "plan.json"):
            with self.subTest(name=name):
                self.assertTrue((self.paths.run_root / name).is_file(), name)
        # What was staged is what the plan pins, byte for byte.
        plan = self.plan()
        staged = custody.sha256_path(self.paths.obligations)
        self.assertEqual(
            plan["pins"][self.paths.obligations.relative_to(self.repo).as_posix()],
            staged)
        self.assertEqual(out["calibration_sha256"],
                         custody.sha256_path(self.paths.run_root / "calibration.json"))
        self.assertIs(out["run_root_preexisted"], True)

    def test_a_run_root_left_empty_by_a_failed_staging_is_not_an_obstacle(self):
        config_path = self.bundle()
        shutil.rmtree(self.paths.run_root)
        self.paths.run_root.mkdir(parents=True)
        self.assertEqual(list(self.paths.run_root.iterdir()), [])
        with no_sockets(self.counter):
            out = auto_loop.preregister(config_path, modules=self.modules())
        self.assertIs(out["run_root_preexisted"], True)
        self.assertIs(self.plan()["run_root_preexisted"], True)
        self.assertTrue(self.paths.plan.is_file())

    def test_a_run_root_that_never_existed_says_so_too(self):
        config_path = self.bundle()
        shutil.rmtree(self.paths.run_root)
        with no_sockets(self.counter):
            out = auto_loop.preregister(config_path, modules=self.modules())
        self.assertIs(out["run_root_preexisted"], False)

    def test_a_second_preregistration_over_a_frozen_plan_is_refused_by_code(self):
        config_path = self.bundle()
        with no_sockets(self.counter):
            auto_loop.preregister(config_path, modules=self.modules())
        first = self.plan()["loop_plan_id"]
        with self.assertRaises(LoopError) as caught:
            auto_loop.preregister(config_path, modules=self.modules())
        self.assertEqual(caught.exception.code, "WRITE_ONCE_VIOLATION")
        self.assertIn(str(self.paths.plan), caught.exception.detail)
        self.assertEqual(self.plan()["loop_plan_id"], first,
                         "a refused pre-registration still rewrote the plan")

    def test_a_missing_bundle_file_is_a_coded_refusal_that_names_the_paths(self):
        config_path = self.bundle()
        (config_path.parent / "obligations.json").unlink()
        with self.assertRaises(LoopError) as caught:
            auto_loop.preregister(config_path, modules=self.modules())
        self.assertEqual(caught.exception.code, "OBLIGATIONS_FILE_MISSING")
        self.assertIn(str(self.paths.obligations), caught.exception.detail)
        self.assertIn(str(config_path.parent / "obligations.json"),
                      caught.exception.detail)
        self.assertFalse(self.paths.plan.exists())

    def test_a_missing_calibration_under_a_declared_schedule_is_refused_at_s0(self):
        config_path = self.bundle()
        (config_path.parent / "calibration.json").unlink()
        self.assertTrue(self.config().audit.period)
        with self.assertRaises(LoopError) as caught:
            auto_loop.preregister(config_path, modules=self.modules())
        self.assertEqual(caught.exception.code, "CALIBRATION_NOT_FOUND")
        self.assertIn("calibration.json", caught.exception.detail)

    def test_dry_run_hands_the_config_path_on_so_the_bundle_can_be_found(self):
        # The same defect one layer up: ``dry_run`` loaded the config into a
        # ``LoopConfig`` and passed THAT to S0, which left S0 with no directory
        # to stage the bundle from and a refusal naming no bundle at all.
        config_path = self.bundle()
        seen: list = []

        class Stop(Exception):
            pass

        def watching(config, **kwargs):
            seen.append(config)
            raise Stop()

        original = auto_loop.preregister
        auto_loop.preregister = watching
        self.addCleanup(setattr, auto_loop, "preregister", original)
        with self.assertRaises(Stop), no_sockets(self.counter):
            auto_loop.dry_run(config_path, self.root / "dry-out",
                              modules=self.modules())
        self.assertEqual(seen, [Path(config_path)])

    def test_the_cli_reports_the_code_and_exits_non_zero(self):
        config_path = self.bundle()
        (config_path.parent / "obligations.json").unlink()
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            code = auto_loop.main(["preregister", "--config", str(config_path)],
                                  modules=self.modules())
        self.assertEqual(code, 1)
        self.assertIn("OBLIGATIONS_FILE_MISSING", stderr.getvalue())


# --------------------------------------------------------------------------
# PREFLIGHT's self-tests (design 4.1 S1; CLONE-PATCH items 1, 2, 5 and 6)
# --------------------------------------------------------------------------

class PreflightSelfTestsWhatTheRunLeansOn(DriverFixture):

    def test_preflight_makes_no_call_and_names_every_check(self):
        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=self.modules())
            report = auto_loop.preflight(self.config_path, modules=self.modules())
        self.assertEqual(report["provider_calls"], 0)
        self.assertEqual(self.counter.offline + self.counter.live, 0)
        names = [check["check"] for check in report["checks"]]
        self.assertEqual(names, ["pins", "seats", "reading_cells", "block_streak",
                                 "register_cells", "calibration", "planned_calls"])

    def test_the_block_streak_definition_is_asserted_by_self_test(self):
        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=self.modules())
            report = auto_loop.preflight(self.config_path, modules=self.modules())
        check = [c for c in report["checks"] if c["check"] == "block_streak"][0]
        self.assertEqual(check["definition"], auto_loop.BLOCK_STREAK_DEFINITION)
        self.assertEqual(self.config().audit.streak_max_account,
                         auto_loop.BLOCK_STREAK_DEFINITION)
        self.assertEqual(self.plan()["block_streak_definition"],
                         auto_loop.BLOCK_STREAK_DEFINITION)

    def test_the_counter_is_per_role_and_resets_on_a_trial_that_did_not_block(self):
        def block(row, role):
            return auto_loop._ProbeBlock(
                row, f"{row}/{role}-1/provider/call-0001.request.json")

        blocked = decide_module.STOP_CUSTODY_HALT  # any non-outcome string
        self.assertEqual(auto_loop.block_streak(
            [block("r1", "judge"), block("r2", "judge")],
            [("r1", "blocked"), ("r2", "blocked")]), 2)
        self.assertEqual(auto_loop.block_streak(
            [block("r1", "judge"), block("r3", "judge")],
            [("r1", "blocked"), ("r2", "sustained"), ("r3", "blocked")]), 1)
        # Two roles keep two streaks; one role's clean trial resets only its own.
        self.assertEqual(auto_loop.block_streak(
            [block("r1", "judge"), block("r1", "critic"), block("r2", "judge")],
            [("r1", "blocked"), ("r2", "blocked")]), 2)
        self.assertNotEqual(blocked, "")

    def test_a_reading_key_the_roles_layer_would_refuse_is_named_at_preflight(self):
        # The pre-registered L001 spelling, which W2-ROLES refuses raw.
        raw = ("h005-row/daily/mini_fcl/cycle01/objection#o1/target/"
               "p.objection.0#c1->daily/mini_fcl/cycle01/account#c1")
        with self.assertRaises(LoopError):
            roles_module.Coordinate(role="critic", key=raw)
        minted = auto_loop.cell_key_for(raw)
        roles_module.Coordinate(role="critic", key=minted)
        self.assertNotEqual(minted, raw)
        self.assertEqual(auto_loop.cell_key_for(raw), minted, "the fold is not pure")
        self.assertNotEqual(auto_loop.cell_key_for(raw + "x"), minted)

    def test_the_plan_pins_the_calibration_digest_and_the_exchange_digest(self):
        from minireason.loop import audits as audits_module
        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=self.modules())
        plan = self.plan()
        body = (self.paths.run_root / "calibration.json").read_bytes()
        self.assertEqual(plan["calibration_sha256"], custody.sha256_bytes(body))
        self.assertEqual(
            plan["pins"]["minireason.loop.audits.CALIBRATION_EXCHANGES_SHA256"],
            audits_module.CALIBRATION_EXCHANGES_SHA256)
        self.assertEqual(plan["pins"][standard_module.CEILING_PIN_KEY],
                         standard_module.CEILING_SHA256)
        self.assertIn("src/minireason/loop/roles.py", plan["pins"])

    def test_the_audit_report_carries_the_calibration_digest_covers_and_seats(self):
        self.walk()
        audit = json.loads(
            (self.paths.audits / "cycle-02" / "audit.json").read_text(encoding="utf-8"))
        self.assertEqual(audit["calibration_sha256"], self.plan()["calibration_sha256"])
        self.assertEqual(audit["covers"], [2])
        self.assertEqual(audit["seats"], list(self.config().seats.judges))
        self.assertEqual(audit["panel"], ["judge#1", "judge#2"])

    def test_the_reader_supplies_the_unread_inventory_off_the_graph(self):
        self.walk()
        read_receipt = [row for row in self.ledger().records()
                        if row.receipt.kind == "READ"][0]
        self.assertIn("readings", read_receipt.receipt.outputs_sha256)
        harness = graph_module.open_graph(
            graph_module.resolve_graph_root(self.repo, self.config().graph_root),
            clock=graph_module.fixed_clock())
        opened = {str(standing.key) for standing in graph_module.cell_standings(harness)}
        self.assertEqual(len(opened), len(self.config().reading_set))


class TheRegisterCellsAreOpenedBeforeAnyCall(DriverFixture):

    CONTRAST = True
    BUDGET = 1

    def test_every_register_cell_the_marker_writes_into_is_opened_at_s0(self):
        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=self.modules())
            report = auto_loop.preflight(self.config_path, modules=self.modules())
        opened = self.plan()["opened_cells"]["register_cells"]
        self.assertTrue(opened)
        check = [c for c in report["checks"] if c["check"] == "register_cells"][0]
        self.assertEqual(check["cells"], len(opened))
        leg = json.loads((self.repo / "contrast-study" / "occurrence-01"
                          / "contrast.json").read_text(encoding="utf-8"))
        cells = [markprep_module.cell_from_contrast_leg(leg, case)
                 for case in sorted(leg["cases"])]
        # G8 again, from the other side: ``program_marks`` refuses to answer at
        # all until the cell is sealed, so this recomputation has to seal its
        # own copies first - which is why the driver seals at S0.
        for cell in cells:
            markprep_module.write_baseline(
                cell, None, Path(self.temp.name) / "recompute" / cell.cell_id.replace("/", "_"))
        wanted = {graph_module.CellKey(cell=cell.cell_id, register=register,
                                       comparison=comparison).token
                  for cell in cells
                  for comparison, block
                  in markprep_module.program_marks(cell)["comparisons"].items()
                  for register in (block.get("registers") or {})}
        self.assertEqual(set(opened), wanted)

    def test_a_missing_register_cell_is_named_before_a_call_is_spent(self):
        with no_sockets(self.counter):
            auto_loop.preregister(self.config_path, modules=self.modules())
        plan = self.plan()
        plan["opened_cells"]["register_cells"] = plan["opened_cells"]["register_cells"][1:]
        self.paths.plan.write_bytes(custody.encoded(plan))
        with self.assertRaises(LoopError) as caught, no_sockets(self.counter):
            auto_loop.preflight(self.config_path, modules=self.modules())
        self.assertEqual(caught.exception.code, "REGISTER_CELLS_DISAGREE")

    def test_the_mark_step_seals_the_baseline_before_any_pack_renders(self):
        self.walk()
        marks = [row for row in self.ledger().records() if row.receipt.kind == "MARK"]
        self.assertEqual(len(marks), 1)
        self.assertEqual(marks[0].receipt.status, "COMPLETE")
        # The baseline is the RUN's, written once at S0 and never revised: a
        # cycle that rewrote it would be revising the thing G8 exists to freeze.
        sealed = sorted((self.paths.run_root / "contrast").rglob(
            markprep_module.BASELINE_FILENAME))
        self.assertTrue(sealed, "no baseline was sealed")
        self.assertEqual(len(sealed), len(self.plan()["opened_cells"]
                                          ["register_cells"]) // 4)


# --------------------------------------------------------------------------
# The module's own rules: codes, the fold, and the metric-creep lens
# --------------------------------------------------------------------------

class TheDriverKeepsItsOwnRules(unittest.TestCase):
    """``tools/`` is outside the package ``test_types.py`` walks, so the fold-in
    contract is asserted here, over this file's own source."""

    SOURCE = DRIVER_SOURCE.read_text(encoding="utf-8")

    def _raised_tokens(self) -> set[str]:
        tree = ast.parse(self.SOURCE)
        found: set[str] = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            if name not in {"_fail", "LoopError", "CustodyMismatch", "ReaderError"}:
                continue
            if node.args and isinstance(node.args[0], ast.Constant) \
                    and isinstance(node.args[0].value, str):
                found.add(node.args[0].value)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                    and node.value in auto_loop.NEW_CODES:
                found.add(node.value)
        return found

    def test_every_new_code_is_folded_into_failure_codes_and_no_other_table(self):
        for code, reason in auto_loop.NEW_CODES.items():
            with self.subTest(code=code):
                self.assertRegex(code, r"\A[A-Z][A-Z0-9_]*\Z")
                self.assertTrue(reason.strip())
                self.assertNotIn("\n", reason)
                self.assertIn(code, FAILURE_CODES)
                self.assertNotIn(code, BLOCK_CODES)
                self.assertNotIn(code, OUTCOME_CODES)

    def test_every_new_code_is_reached_by_this_module(self):
        reached = self._raised_tokens()
        for code in auto_loop.NEW_CODES:
            with self.subTest(code=code):
                self.assertIn(code, reached,
                              f"{code} is declared and no call site reaches it")

    def test_every_code_this_module_raises_is_a_member_of_a_declared_table(self):
        for token in sorted(self._raised_tokens()):
            with self.subTest(token=token):
                self.assertIn(token, set(FAILURE_CODES) | set(BLOCK_CODES)
                              | set(OUTCOME_CODES))

    def test_the_metric_creep_lens(self):
        lowered = self.SOURCE.lower()
        for word in ("majority", "average", "mean", "percent", "ratio", "score",
                     "rank", "ranking", "weighted", "aggregate", "exhaustion",
                     "vote", "tally"):
            with self.subTest(word=word):
                self.assertIsNone(re.search(r"\b" + word + r"\b", lowered), word)

    def test_no_division_in_this_module_is_arithmetic(self):
        """Every ``/`` here joins a path; none of them divides two numbers."""

        tree = ast.parse(self.SOURCE)
        for node in ast.walk(tree):
            if not isinstance(node, ast.BinOp) or not isinstance(node.op, ast.Div):
                continue
            text = ast.unparse(node)
            with self.subTest(expression=text):
                for side in (node.left, node.right):
                    self.assertNotIsInstance(
                        getattr(side, "value", None), (int, float),
                        "a numeric operand of / is arithmetic, not a path join")
                self.assertTrue(
                    re.search(r"(path|paths|root|dir|_dir|target|occurrence|"
                              r"records|repo|claim|out)\b", text.lower())
                    or "\"" in text or "'" in text, text)

    def test_the_two_integers_it_carries_are_spend_boundaries(self):
        derivation = auto_loop.planned_calls(
            LoopConfig.from_mapping({
                "run_id": "R", "study": "s", "occurrences": ["o"],
                "runner": "tools/multicycle_commitment_study_multi_v2.py",
                "cycle_budget": 1, "max_calls": 10,
                "reading_set": ["h005-row/a#b/c/d"],
                "obligations_path": "o.json", "graph_root": "g",
                "reopen_reasons": list(standard_module.REOPEN_REASONS),
                "audit": {"period": 1, "judge_err_max": 0.2, "streak_max": 2,
                          "judge_err_max_account": "x", "streak_max_account": "y"},
                "seats": {"judges": ["a/one", "b/two"], "paraphrase_n": 2,
                          "min_judge_families": 2, "schema_repair_budget": 0},
            }), mark_cells=2)
        self.assertEqual(derivation["row_cost"], 11)
        self.assertEqual(derivation["mark_cost"], 9)
        self.assertEqual(derivation["planned_calls"], 11 + 18)
        self.assertNotIn("rate", json.dumps(derivation))

    def test_the_arm_ended_text_is_this_module_s_and_is_never_a_verdict(self):
        self.assertIn("no semantic verdict is issued", auto_loop.ARM_ENDED_TEXT)
        self.assertNotIn("overrun", auto_loop.ARM_ENDED_TEXT)

    def test_the_seam_is_one_provider_factory_and_two_non_guards(self):
        fields = sorted(auto_loop.Modules.__dataclass_fields__)
        self.assertEqual(fields, ["provider_factory", "repo_root", "sleep"])

    def test_a_status_call_on_a_run_that_is_not_there_is_refused_by_code(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            code = auto_loop.main(["status", "--run", "never-existed"],
                                  modules=auto_loop.Modules(repo_root=REPOSITORY))
        self.assertEqual(code, 1)
        self.assertIn("CONFIG_NOT_FOUND", stderr.getvalue())

    def test_the_dry_run_entry_refuses_to_guess_a_config(self):
        with tempfile.TemporaryDirectory() as raw:
            verdict = auto_loop.dry_run(None, Path(raw) / "out")
            self.assertFalse(verdict["ran"])
            self.assertIn("provider_arm_failure", verdict["inducible"])
            self.assertTrue((Path(verdict["occurrence"]) / "plan.json").is_file())
            self.assertEqual(sorted(verdict["induced_codes"]),
                             sorted(synthetic.INDUCIBLE))


class TheStatusAndReopenEntries(DriverFixture):

    def test_status_reads_the_resume_plan_without_writing(self):
        self.walk()
        before = sorted(p.name for p in self.paths.steps.iterdir())
        summary = auto_loop.status(self.paths.run_root, modules=self.modules())
        self.assertEqual(summary["loop_plan_id"], self.plan()["loop_plan_id"])
        self.assertIsNone(summary["blocking"])
        self.assertEqual(sorted(p.name for p in self.paths.steps.iterdir()), before)

    def test_a_reopen_outside_the_declared_reasons_is_refused(self):
        self.walk()
        with self.assertRaises(LoopError) as caught:
            auto_loop.reopen(self.paths.run_root, None, modules=self.modules(),
                             reason="because I felt like it")
        self.assertEqual(caught.exception.code, "REOPEN_REFUSED")
        recorded = auto_loop.reopen(self.paths.run_root, None,
                                    modules=self.modules(),
                                    reason="appellate-ruling")
        self.assertEqual(recorded["reason"], "appellate-ruling")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
