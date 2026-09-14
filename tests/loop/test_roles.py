"""W2-ROLES - tests for :mod:`minireason.loop.roles`.

Every acceptance clause of the section 7 wave-plan entry has at least one test
here, and every one of them runs on ``OfflineProvider`` fixtures with the socket
layer removed from under the process, so a call that tried to open one would
fail loudly rather than pass quietly.
"""

from __future__ import annotations

import ast
import contextlib
import json
import socket
import tempfile
import threading
import time
import unittest
from pathlib import Path

from minireason import provider_openai_compat as transport
from minireason.loop import contracts, obligations, roles, seats, standard, synthetic
from minireason.loop import types as loop_types

PACKAGE = Path(roles.__file__).resolve()

#: A pack that says "json", so the same bytes are admissible in both response
#: modes and no test has to keep two packs.
PACK = b"Read the material below and return one JSON object.\n--- material ---\nx\n"


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


class _SocketsUsed(AssertionError):
    """Raised the instant anything in the process reaches for a socket."""


#: The pristine socket layer, captured once at import - before any block has
#: swapped it - so that restoring it can never restore a refusal.  Saving the
#: three globals at *enter* time was a real leak: six threads enter
#: :func:`no_sockets` concurrently in
#: ``NoSixthConcurrentCallIsPossibleOnOneKeyEnv``, the second thread to enter
#: saved the first thread's ``refuse``, and the last thread to leave restored
#: it permanently - after which every later test in the same process, in this
#: file or in ``tests/test_provider_openai_compat.py``, met a refusal that no
#: block had asked for.  A nested block would have done the same thing on one
#: thread.  Captured once, restored once, at depth zero.
_PRISTINE_SOCKETS = (socket.socket, socket.create_connection, transport._open)

#: Depth and its lock, so concurrent and nested blocks install the refusal once
#: and remove it when the last of them leaves.
_SOCKET_GUARD_LOCK = threading.Lock()
_SOCKET_GUARD_DEPTH = 0


def _refuse_socket(*args, **kwargs):
    raise _SocketsUsed("a test opened a socket")


@contextlib.contextmanager
def no_sockets():
    """Remove the socket layer for the duration of the block.

    Stronger than counting calls: ``socket.socket``, ``socket.create_connection``
    and the transport's own ``_open`` all raise, so a call that reached the
    network would fail the test rather than merely be counted.

    Re-entrant and thread-safe: what is restored is always
    :data:`_PRISTINE_SOCKETS`, never whatever happened to be installed when this
    block began, and only the outermost block restores anything.
    """

    global _SOCKET_GUARD_DEPTH
    with _SOCKET_GUARD_LOCK:
        _SOCKET_GUARD_DEPTH += 1
        socket.socket = _refuse_socket
        socket.create_connection = _refuse_socket
        transport._open = _refuse_socket
    try:
        yield
    finally:
        with _SOCKET_GUARD_LOCK:
            _SOCKET_GUARD_DEPTH -= 1
            if _SOCKET_GUARD_DEPTH == 0:
                (socket.socket, socket.create_connection,
                 transport._open) = _PRISTINE_SOCKETS


def seat_for(role: str, endpoint: str = "synthetic/alpha", index: int = 0) -> seats.Seat:
    """One seat over the synthetic registry. No credential, no socket."""

    return seats.Seat(role, index, synthetic.endpoints_registry()[endpoint])


def scripted(*replies):
    """A factory in the loop's own shape, over a script this test wrote."""

    def factory(role, coordinate, records_dir, *, seat=None, endpoint=None):
        return transport.OfflineProvider(endpoint, records_dir, list(replies))

    return factory


class TheSocketGuardLeavesTheProcessAsItFoundIt(unittest.TestCase):
    """The guard is a fixture; a fixture that does not clean up is a defect.

    Found by the checkpoint publisher: with the whole repository suite in one
    process, ``tests/test_provider_openai_compat.py``'s two no-network tests
    failed with ``_SocketsUsed`` - a refusal installed by THIS file and never
    removed. :class:`NoSixthConcurrentCallIsPossibleOnOneKeyEnv` runs six
    threads that each enter :func:`no_sockets`; each saved the three globals at
    *enter* time, so the second thread in saved the first thread's ``refuse``
    and the last thread out restored it permanently. A nested block would have
    done the same on one thread.

    The repair is to capture the pristine layer once at import and restore it
    once, at depth zero, under a lock. These tests are that repair's teeth.
    """

    def test_a_single_block_restores_all_three_globals(self):
        before = (socket.socket, socket.create_connection, transport._open)
        with no_sockets():
            self.assertIs(socket.socket, _refuse_socket)
        self.assertEqual(
            (socket.socket, socket.create_connection, transport._open), before)

    def test_a_nested_block_does_not_leave_the_refusal_installed(self):
        before = (socket.socket, socket.create_connection, transport._open)
        with no_sockets():
            with no_sockets():
                self.assertIs(transport._open, _refuse_socket)
            self.assertIs(transport._open, _refuse_socket)
        self.assertEqual(
            (socket.socket, socket.create_connection, transport._open), before)

    def test_six_threads_entering_the_guard_leave_the_originals_in_place(self):
        """The exact shape that leaked: six concurrent entries, one exit each."""

        before = (socket.socket, socket.create_connection, transport._open)
        started = threading.Barrier(6)
        seen: list[bool] = []
        errors: list[BaseException] = []

        def run() -> None:
            try:
                with no_sockets():
                    started.wait(timeout=10)
                    seen.append(socket.socket is _refuse_socket)
            except BaseException as exc:      # pragma: no cover - a failure path
                errors.append(exc)

        threads = [threading.Thread(target=run) for _ in range(6)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)
        self.assertEqual(errors, [])
        self.assertEqual(seen, [True] * 6)
        self.assertEqual(
            (socket.socket, socket.create_connection, transport._open), before,
            "the socket layer this file borrows must be given back")

    def test_the_guard_restores_the_pristine_layer_and_not_what_it_found(self):
        """Why saving at enter time was the bug, stated as an assertion."""

        self.assertEqual(_PRISTINE_SOCKETS[0], socket.socket)
        self.assertNotIn(_refuse_socket, _PRISTINE_SOCKETS)

    def test_an_exception_inside_the_block_still_restores_the_layer(self):
        before = (socket.socket, socket.create_connection, transport._open)
        with self.assertRaises(ZeroDivisionError):
            with no_sockets():
                raise ZeroDivisionError("the block did not finish")
        self.assertEqual(
            (socket.socket, socket.create_connection, transport._open), before)


class TheRecordSaysWhichGateWasHeldByWhat(unittest.TestCase):
    """Wave-1 integration decision 42(c): never acquire ``slots_for`` twice.

    ``OpenAICompatProvider`` acquires the inner gate inside ``complete``;
    ``OfflineProvider`` holds none. This module acquires only the outer one, and
    the record says so per call - ``inner_held_by`` null for a provider that
    holds no inner gate, so a reader can tell "not held" from "not recorded".
    """

    def test_the_two_gates_are_named_with_their_holders(self):
        self.assertEqual(roles.GATE_ORDER,
                         ("seats.key_gate_for",
                          "provider_openai_compat.slots_for"))
        self.assertEqual(set(roles.GATE_HELD_BY), set(roles.GATE_ORDER))
        self.assertIn("call_role", roles.GATE_HELD_BY[roles.GATE_ORDER[0]])
        self.assertIn("complete", roles.GATE_HELD_BY[roles.GATE_ORDER[1]])

    def test_an_offline_call_records_no_inner_holder(self):
        with tempfile.TemporaryDirectory() as tmp:
            with no_sockets():
                result = roles.call_critic(
                    seat_for("critic"), PACK, Path(tmp),
                    coordinate="read/retains",
                    provider_factory=synthetic.provider_factory(strict=True))
        gates = result.record["settings"]["gates"]
        self.assertEqual(gates["order"], list(roles.GATE_ORDER))
        self.assertEqual(gates["outer_held_by"],
                         roles.GATE_HELD_BY[roles.GATE_ORDER[0]])
        self.assertIsNone(gates["inner_held_by"])

    def test_this_module_never_acquires_the_inner_gate_itself(self):
        """A CALL to ``slots_for``, not a mention of its name in prose."""

        tree = ast.parse(PACKAGE.read_text(encoding="utf-8"))
        called = {getattr(node.func, "id", getattr(node.func, "attr", ""))
                  for node in ast.walk(tree) if isinstance(node, ast.Call)}
        self.assertNotIn("slots_for", called)
        self.assertNotIn("Semaphore", called)
        self.assertNotIn("BoundedSemaphore", called)
        imported = {alias.asname or alias.name
                    for node in ast.walk(tree)
                    if isinstance(node, ast.ImportFrom) for alias in node.names}
        self.assertNotIn("slots_for", imported)


class RolesTestCase(unittest.TestCase):
    """A temp records directory and the synthetic script, per test."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.records = Path(self._tmp.name)
        self.factory = synthetic.provider_factory(strict=True)
        self.addCleanup(self._tmp.cleanup)

    def call(self, role: str, **kwargs):
        seat = kwargs.pop("seat", None) or seat_for(role)
        kwargs.setdefault("provider_factory", self.factory)
        with no_sockets():
            return roles.call_role(role, seat, kwargs.pop("pack", PACK), None,
                                   self.records, **kwargs)


# --------------------------------------------------------------------------
# The five callers, end to end, with zero sockets
# --------------------------------------------------------------------------


class EveryRoleRunsEndToEndOnOfflineProvidersWithZeroSockets(RolesTestCase):
    """Acceptance 1."""

    def test_the_critic_caller_returns_a_validated_critic_output(self):
        with no_sockets():
            result = roles.call_critic(seat_for("critic"), PACK, self.records,
                                       coordinate="read/retains",
                                       provider_factory=self.factory)
        self.assertTrue(result.ok)
        self.assertIsInstance(result.output, contracts.CriticOutput)
        self.assertEqual(result.output.relation, "retains")
        self.assertIsNone(result.block)

    def test_the_defender_caller_returns_a_validated_defender_output(self):
        with no_sockets():
            result = roles.call_defender(seat_for("defender", "synthetic/beta"), PACK,
                                         self.records, coordinate="read/retains",
                                         provider_factory=self.factory)
        self.assertTrue(result.ok)
        self.assertIsInstance(result.output, contracts.DefenderOutput)
        self.assertFalse(result.output.concedes)

    def test_the_judge_caller_returns_one_ruling_per_seat_of_the_pair(self):
        rulings = []
        for index, token, endpoint in ((0, "judge-a", "synthetic/alpha"),
                                       (1, "judge-b", "synthetic/beta")):
            with no_sockets():
                rulings.append(roles.call_judge(
                    seat_for("judge", endpoint, index), PACK, self.records,
                    coordinate="read/retains", seat_token=token,
                    provider_factory=self.factory))
        for ruling in rulings:
            self.assertTrue(ruling.ok)
            self.assertIsInstance(ruling.output, contracts.JudgeRuling)
        self.assertEqual([r.coordinate.token for r in rulings],
                         ["judge#1@read/retains", "judge#2@read/retains"])

    def test_the_variator_caller_returns_the_paraphrases_of_the_exchange(self):
        with no_sockets():
            result = roles.call_variator(seat_for("variator", "synthetic/beta"), PACK,
                                         self.records, coordinate="read/retains",
                                         provider_factory=self.factory)
        self.assertTrue(result.ok)
        self.assertIsInstance(result.output, contracts.VariatorOutput)
        self.assertEqual(len(result.output.paraphrases), 2)

    def test_the_marker_caller_returns_one_mark_for_one_register(self):
        with no_sockets():
            result = roles.call_marker(seat_for("judge"), PACK, self.records,
                                       coordinate="mark/case-a/T/rep-1", register="T",
                                       provider_factory=self.factory)
        self.assertTrue(result.ok)
        self.assertIsInstance(result.output, contracts.MarkerOutput)
        self.assertEqual(result.output.difference_kind, "target_set_membership")

    def test_no_provider_but_an_offline_one_is_ever_built(self):
        with no_sockets():
            roles.call_critic(seat_for("critic"), PACK, self.records,
                              coordinate="read/retains", provider_factory=self.factory)
        self.assertEqual(self.factory.handed, [("critic", "read/retains")])
        self.assertEqual(self.factory.calls, 1)


# --------------------------------------------------------------------------
# Write-once, and NO_REPLAY
# --------------------------------------------------------------------------


class ASpentCoordinateIsNeverSentASecondTime(RolesTestCase):
    """Acceptance 2."""

    def test_a_second_call_on_one_coordinate_raises_no_replay(self):
        self.call("critic", coordinate="read/retains")
        with self.assertRaises(roles.RoleRefused) as caught:
            self.call("critic", coordinate="read/retains")
        self.assertEqual(caught.exception.code, roles.NO_REPLAY)

    def test_the_replay_is_refused_before_any_provider_is_built(self):
        self.call("critic", coordinate="read/retains")
        before = self.factory.calls
        with self.assertRaises(roles.RoleRefused):
            self.call("critic", coordinate="read/retains")
        self.assertEqual(self.factory.calls, before)

    def test_the_coordinate_directory_is_the_atomic_claim(self):
        result = self.call("critic", coordinate="read/retains")
        claimed = self.records / "read/retains/critic"
        self.assertTrue(claimed.is_dir())
        self.assertEqual(Path(result.record_path), claimed / "call.json")

    def test_the_call_record_itself_is_write_once(self):
        result = self.call("critic", coordinate="read/retains")
        from minireason.loop import custody
        with self.assertRaises(custody.WriteOnceViolation):
            custody.write_new(result.record_path, {"a": 1})

    def test_two_judge_seats_write_two_coordinates_and_neither_is_a_replay(self):
        for index, token, endpoint in ((0, "judge-a", "synthetic/alpha"),
                                       (1, "judge-b", "synthetic/beta")):
            self.call("judge", seat=seat_for("judge", endpoint, index),
                      coordinate="read/retains", seat_token=token)
        self.assertTrue((self.records / "read/retains/judge-1/call.json").exists())
        self.assertTrue((self.records / "read/retains/judge-2/call.json").exists())

    def test_the_record_declares_an_empty_replay_of_rather_than_omitting_it(self):
        result = self.call("critic", coordinate="read/retains")
        self.assertIn("replay_of", result.record)
        self.assertEqual(result.record["replay_of"], "")


# --------------------------------------------------------------------------
# The two gates
# --------------------------------------------------------------------------


class TheTwoGatesAreAcquiredInOneFixedOrderAndNothingIsReimplemented(RolesTestCase):
    """Acceptance 3, and the wave-1 interface's seats Q5."""

    def test_the_declared_gate_order_is_outer_then_inner(self):
        self.assertEqual(roles.GATE_ORDER,
                         ("seats.key_gate_for", "provider_openai_compat.slots_for"))

    def test_the_outer_gate_is_runner_v2s_own_and_is_imported_not_copied(self):
        seat = seat_for("critic")
        self.assertIs(roles.key_gate_for, seats.key_gate_for)
        runner = seats.runner_module()
        self.assertIs(seats.key_gate_for(seat),
                      runner.key_gate(seat.key_env, seats.key_cap_for(seat)))

    def test_the_module_constructs_no_semaphore_of_its_own(self):
        tree = ast.parse(PACKAGE.read_text(encoding="utf-8"))
        built = {
            node.func.attr if isinstance(node.func, ast.Attribute) else
            getattr(node.func, "id", "")
            for node in ast.walk(tree) if isinstance(node, ast.Call)
        }
        for forbidden in ("Semaphore", "BoundedSemaphore", "Lock", "RLock"):
            self.assertNotIn(forbidden, built,
                             "the loop adds no third gate (design 4.6)")

    def test_the_inner_gate_is_the_providers_and_is_acquired_by_it(self):
        source = Path(transport.__file__).read_text(encoding="utf-8")
        self.assertIn("self._slots = slots_for(endpoint.key_env, endpoint.max_concurrency)",
                      source)
        self.assertIn("with self._slots:", source)

    def test_the_record_names_the_gate_order_and_the_cap_in_force(self):
        result = self.call("critic", coordinate="read/retains")
        self.assertEqual(result.record["settings"]["gate_order"], list(roles.GATE_ORDER))
        self.assertEqual(result.record["settings"]["key_cap"],
                         seats.key_cap_for(seat_for("critic")))

    def test_no_more_calls_run_at_once_than_the_credential_authorises(self):
        seat = seat_for("critic")
        cap = seats.key_cap_for(seat)
        state = {"now": 0, "peak": 0}
        lock = threading.Lock()

        class Counting(transport.OfflineProvider):
            def complete(self, *args, **kwargs):
                with lock:
                    state["now"] += 1
                    state["peak"] = max(state["peak"], state["now"])
                time.sleep(0.02)
                try:
                    return super().complete(*args, **kwargs)
                finally:
                    with lock:
                        state["now"] -= 1

        reply = json.dumps({"relation": "none", "passage_quote": "", "case": "",
                            "outside_vocabulary": "",
                            "role_bindings": {"target": "", "defect": "",
                                              "grounds": "", "bearing": ""}})

        def factory(role, coordinate, records_dir, *, seat=None, endpoint=None):
            return Counting(endpoint, records_dir, [reply])

        errors: list[BaseException] = []

        def run(index: int) -> None:
            try:
                with no_sockets():
                    roles.call_critic(seat, PACK, self.records,
                                      coordinate=f"read/row-{index}",
                                      provider_factory=factory)
            except BaseException as exc:          # pragma: no cover - a failure path
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(6)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(errors, [])
        self.assertLessEqual(state["peak"], cap)
        self.assertLessEqual(cap, seats.MAX_PER_KEY)


# --------------------------------------------------------------------------
# Schema, the repair budget, and the absent re-ask
# --------------------------------------------------------------------------


class ASchemaInvalidReplyBlocksAndIsNeverReAsked(RolesTestCase):
    """Acceptance 4."""

    BROKEN = json.dumps({"relation": "not-a-relation", "passage_quote": "x",
                         "case": "y", "outside_vocabulary": "",
                         "role_bindings": {"target": "", "defect": "",
                                           "grounds": "", "bearing": ""}})

    def test_an_invalid_reply_returns_blocked_schema_and_not_an_exception(self):
        with no_sockets():
            result = roles.call_critic(seat_for("critic"), PACK, self.records,
                                       coordinate="read/retains",
                                       provider_factory=scripted(self.BROKEN))
        self.assertTrue(result.blocked)
        self.assertEqual(result.block, loop_types.block_code("schema"))
        self.assertIn(result.reason, contracts.SCHEMA_REASONS)
        self.assertIsNone(result.output)

    def test_the_block_code_is_the_one_the_ceiling_declares(self):
        self.assertIn(roles.SCHEMA_BLOCK, loop_types.BLOCK_CODES)
        self.assertIn(roles.PROVIDER_BLOCK, loop_types.BLOCK_CODES)

    def test_nothing_is_re_asked_and_exactly_one_call_is_spent(self):
        calls = {"n": 0}

        def factory(role, coordinate, records_dir, *, seat=None, endpoint=None):
            calls["n"] += 1
            return transport.OfflineProvider(endpoint, records_dir, [self.BROKEN])

        with no_sockets():
            roles.call_critic(seat_for("critic"), PACK, self.records,
                              coordinate="read/retains", provider_factory=factory)
        self.assertEqual(calls["n"], 1)
        spent = sorted(p.name for p in
                       (self.records / "read/retains/critic/provider").iterdir())
        self.assertEqual(spent, ["call-0001.request.json", "call-0001.response.json"])

    def test_the_pre_registered_repair_budget_is_zero_in_all_three_owners(self):
        self.assertEqual(roles.SCHEMA_REPAIR_BUDGET, 0)
        self.assertEqual(standard.GUARD_PARAMETERS["schema_repair_budget"], 0)
        self.assertEqual(loop_types.SeatsConfig().schema_repair_budget, 0)

    def test_a_repair_past_the_budget_is_refused_rather_than_sent(self):
        with self.assertRaises(roles.RoleRefused) as caught:
            self.call("critic", coordinate="read/retains", repair=1)
        self.assertEqual(caught.exception.code, roles.ROLE_REPAIR_REFUSED)
        self.assertEqual(self.factory.calls, 0)

    def test_the_budget_is_pinned_into_every_call_record(self):
        result = self.call("critic", coordinate="read/retains")
        self.assertEqual(result.record["settings"]["schema_repair_budget"], 0)
        self.assertEqual(result.record["settings"]["repair"], 0)
        self.assertEqual(result.record["settings"]["retries"], 0)


class ARepairIsANewCoordinateWithItsOwnWriteOnceRecord(RolesTestCase):
    """Acceptance 5. Reachable only where a successor standard raised the budget."""

    def test_a_repair_coordinate_is_spelled_the_way_the_design_spells_it(self):
        where = roles.Coordinate("critic", "read/retains", repair=1)
        self.assertEqual(where.token, "critic@read/retains#repair1")
        self.assertEqual(where.slug, "read/retains/critic.repair1")

    def test_a_repair_writes_a_second_record_beside_the_first_and_replaces_nothing(self):
        first = self.call("critic", coordinate="read/retains")
        second = self.call("critic", coordinate="read/retains", repair=1, repair_budget=1)
        self.assertNotEqual(first.record_path, second.record_path)
        self.assertTrue(Path(first.record_path).exists())
        self.assertTrue(Path(second.record_path).exists())
        self.assertNotEqual(first.record["coordinate"], second.record["coordinate"])

    def test_a_repair_coordinate_is_itself_write_once(self):
        self.call("critic", coordinate="read/retains", repair=1, repair_budget=1)
        with self.assertRaises(roles.RoleRefused) as caught:
            self.call("critic", coordinate="read/retains", repair=1, repair_budget=1)
        self.assertEqual(caught.exception.code, roles.NO_REPLAY)

    def test_the_repair_number_rides_in_the_record(self):
        result = self.call("critic", coordinate="read/retains", repair=1, repair_budget=1)
        self.assertEqual(result.record["settings"]["repair"], 1)
        self.assertEqual(result.record["settings"]["schema_repair_budget"], 1)


# --------------------------------------------------------------------------
# What every record carries
# --------------------------------------------------------------------------


class EveryRecordCarriesWhatTheWavePlanRequires(RolesTestCase):
    """Acceptance 6, and the wave brief's own list."""

    def record(self):
        return self.call("critic", coordinate="read/retains")

    def test_the_record_carries_the_seat_its_family_and_its_key_env(self):
        result = self.record()
        seat = result.record["seat"]
        self.assertEqual(seat["name"], "synthetic/alpha")
        self.assertEqual(seat["family"], synthetic.SYNTHETIC_FAMILIES[0])
        self.assertEqual(seat["key_env"], synthetic.SYNTHETIC_KEY_ENVS[0])
        self.assertEqual(result.family, seat["family"])
        self.assertEqual(result.key_env, seat["key_env"])

    def test_the_record_carries_the_whole_of_seat_identity(self):
        seat = seat_for("critic")
        result = self.record()
        for key, value in seat.identity().items():
            self.assertEqual(result.record["seat"][key], value)

    def test_the_record_carries_the_pack_digest_of_the_bytes_that_were_sent(self):
        from minireason.loop import custody
        result = self.record()
        self.assertEqual(result.pack_sha, custody.sha256_bytes(PACK))
        self.assertEqual(result.record["pack_bytes"], len(PACK))

    def test_the_record_carries_max_tokens_the_timeout_and_the_seed(self):
        result = self.record()
        settings = result.record["settings"]
        self.assertEqual(settings["max_tokens"],
                         roles.max_tokens_for(seat_for("critic"), "critic").max_tokens)
        self.assertEqual(settings["timeout_seconds"], seat_for("critic").timeout_seconds)
        self.assertEqual(settings["seed"], roles.seed_for(result.coordinate))
        self.assertEqual(settings["seed_source"], "sha256(coordinate.token)[:8]")

    def test_the_record_carries_the_prompt_ref_and_the_raw_ref(self):
        result = self.record()
        self.assertTrue(Path(result.prompt_ref.path).is_file())
        self.assertTrue(Path(result.raw_ref.path).is_file())
        self.assertEqual(result.record["outcome"]["prompt_ref"], result.prompt_ref.as_dict())
        self.assertEqual(result.record["outcome"]["raw_ref"], result.raw_ref.as_dict())
        sent = json.loads(Path(result.prompt_ref.path).read_text(encoding="utf-8"))
        self.assertEqual(sent["request_sha256"], result.prompt_ref.sha256)

    def test_the_record_is_readable_by_the_predicate_that_waits_for_it(self):
        result = self.record()
        self.assertEqual(roles.RECORD_FIELD, obligations.RECORD_FIELD)
        self.assertIn(roles.RECORD_KIND, obligations.RECORD_KINDS)
        self.assertEqual(result.record[obligations.RECORD_FIELD], roles.RECORD_KIND)
        self.assertEqual(obligations.PREDICATE_READS["write_once_no_replay"],
                         (roles.RECORD_KIND,))
        for field in ("coordinate", "digest", "replay_of"):
            self.assertIn(field, result.record)

    def test_the_digest_covers_the_identity_and_not_the_outcome(self):
        from minireason.loop import custody
        result = self.record()
        identity = {key: value for key, value in result.record.items()
                    if key not in ("digest", "outcome")}
        self.assertEqual(result.record["digest"], custody.digest(identity))

    def test_the_record_carries_no_scoring_key_anywhere(self):
        contracts.assert_no_scoring_keys(self.record())

    def test_the_record_names_no_credential_value_anywhere(self):
        from minireason.loop import custody
        written = Path(self.record().record_path).read_bytes()
        self.assertEqual(custody.credential_names_in(written), [])


# --------------------------------------------------------------------------
# Provider failures are returned, never raised
# --------------------------------------------------------------------------


class AProviderFailureIsADeliveryFactAndNeverAnException(RolesTestCase):

    def test_an_exhausted_route_returns_blocked_provider(self):
        with no_sockets():
            result = roles.call_critic(seat_for("critic"), PACK, self.records,
                                       coordinate="read/retains",
                                       provider_factory=scripted())
        self.assertTrue(result.blocked)
        self.assertEqual(result.block, loop_types.block_code("provider"))
        self.assertEqual(result.reason, "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertIsNone(result.output)

    def test_a_provider_failure_still_writes_its_record_and_its_refs(self):
        with no_sockets():
            result = roles.call_critic(seat_for("critic"), PACK, self.records,
                                       coordinate="read/retains",
                                       provider_factory=scripted())
        self.assertTrue(Path(result.record_path).is_file())
        self.assertTrue(Path(result.prompt_ref.path).is_file())
        self.assertTrue(Path(result.raw_ref.path).is_file())

    def test_an_arm_ending_code_is_named_and_carries_its_reason(self):
        self.assertIn("TRANSPORT_OR_RESPONSE_ERROR", roles.ARM_ENDING_CODES)
        for reason in roles.ARM_ENDING_CODES.values():
            self.assertTrue(reason.strip())

    def test_the_arm_end_is_a_predicate_and_the_exception_is_opt_in(self):
        with no_sockets():
            result = roles.call_critic(seat_for("critic"), PACK, self.records,
                                       coordinate="read/retains",
                                       provider_factory=scripted())
        self.assertTrue(result.arm_ended)
        with self.assertRaises(roles.ProviderArmEnded) as caught:
            result.raise_if_arm_ended()
        self.assertEqual(caught.exception.code, "TRANSPORT_OR_RESPONSE_ERROR")
        self.assertIs(caught.exception.result, result)

    def test_a_call_that_did_not_end_an_arm_returns_itself_unchanged(self):
        result = self.call("critic", coordinate="read/retains")
        self.assertFalse(result.arm_ended)
        self.assertIs(result.raise_if_arm_ended(), result)

    def test_the_three_hundred_second_wall_is_named_rather_than_left_bare(self):
        failure = transport.ProviderFailure(
            "TRANSPORT_OR_RESPONSE_ERROR", "Remote end closed connection without response",
            record={"elapsed_ms": 300270})
        reason, carried = roles.provider_reason(failure)
        self.assertEqual(reason, roles.PROVIDER_GATEWAY_WALL)
        self.assertEqual(carried, "TRANSPORT_OR_RESPONSE_ERROR")

    def test_a_prompt_failure_well_inside_the_wall_keeps_the_transports_own_code(self):
        failure = transport.ProviderFailure("TRANSPORT_OR_RESPONSE_ERROR", "reset",
                                            record={"elapsed_ms": 1200})
        self.assertEqual(roles.provider_reason(failure),
                         ("TRANSPORT_OR_RESPONSE_ERROR", None))

    def test_a_failure_that_is_not_a_transport_error_is_never_read_as_the_wall(self):
        failure = transport.ProviderFailure("HTTP_429", "slow down",
                                            record={"elapsed_ms": 400000})
        self.assertEqual(roles.provider_reason(failure), ("HTTP_429", None))


# --------------------------------------------------------------------------
# The response format
# --------------------------------------------------------------------------


class TheReplyIsAskedForUnderAStrictSchemaWhereTheEndpointSupportsOne(RolesTestCase):

    def test_a_compat_endpoint_is_asked_in_strict_json_schema_mode(self):
        mode, form, schema = roles.response_format_for(seat_for("critic"), "critic")
        self.assertEqual(mode, roles.JSON_SCHEMA_MODE)
        self.assertTrue(form["json_schema"]["strict"])
        self.assertEqual(form["json_schema"]["schema"], schema)
        self.assertEqual(form["json_schema"]["name"], "loop.critic.v1")

    def test_the_schema_on_the_wire_is_the_contracts_own(self):
        _, _, schema = roles.response_format_for(seat_for("critic"), "critic")
        self.assertEqual(schema, contracts.schema_for("critic"))

    def test_a_deepseek_endpoint_is_asked_in_json_object_mode_instead(self):
        endpoint = transport.Endpoint(
            name="deepseek-flash", base_url="https://api.deepseek.invalid/v1",
            model="d", key_env="DEEPSEEK_API_KEY", family="deepseek")
        mode, form, _ = roles.response_format_for(seats.Seat("critic", 0, endpoint), "critic")
        self.assertEqual(mode, roles.JSON_OBJECT_MODE)
        self.assertEqual(form, {"type": "json_object"})
        self.assertIn("deepseek", roles.JSON_OBJECT_ONLY_FAMILIES)

    def test_a_json_object_seat_refuses_a_pack_that_never_says_json(self):
        endpoint = transport.Endpoint(
            name="deepseek-flash", base_url="https://api.deepseek.invalid/v1",
            model="d", key_env="DEEPSEEK_API_KEY", family="deepseek")
        with self.assertRaises(roles.RoleRefused) as caught:
            with no_sockets():
                roles.call_critic(seats.Seat("critic", 0, endpoint), b"no such word here",
                                  self.records, coordinate="read/retains",
                                  provider_factory=scripted("{}"))
        self.assertEqual(caught.exception.code, roles.ROLE_PACK_NOT_JSON_MODE_READY)

    def test_a_native_endpoint_still_gets_the_schema_the_transport_unwraps(self):
        native = transport.Endpoint(
            name="ollama/x.native", base_url="https://ollama.invalid/v1", model="x",
            key_env="OLLAMA_API_KEY", family="ollama-cloud/x", native=True)
        mode, form, schema = roles.response_format_for(seats.Seat("critic", 0, native), "critic")
        self.assertEqual(mode, roles.JSON_SCHEMA_MODE)
        self.assertEqual(transport._native_format(form), schema)

    def test_the_mode_is_recorded_so_no_reader_has_to_infer_it(self):
        result = self.call("critic", coordinate="read/retains")
        self.assertEqual(result.record["settings"]["response_format_mode"],
                         roles.JSON_SCHEMA_MODE)
        self.assertTrue(result.record["settings"]["response_format_strict"])
        self.assertEqual(result.record["settings"]["schema_title"], "loop.critic.v1")

    def test_a_marker_sees_only_its_own_registers_closed_token_set(self):
        for register in standard.REGISTER_IDS:
            _, _, schema = roles.response_format_for(seat_for("judge"), "marker",
                                                     register=register)
            self.assertEqual(schema["properties"]["difference_kind"]["enum"],
                             list(contracts.difference_kinds_for(register)) + [None])

    def test_a_marker_call_without_a_register_is_refused(self):
        with self.assertRaises(roles.RoleRefused) as caught:
            self.call("marker", seat=seat_for("judge"), coordinate="mark/case-a/T/rep-1")
        self.assertEqual(caught.exception.code, roles.ROLE_REGISTER_REQUIRED)

    def test_a_marker_reply_is_validated_against_its_own_register(self):
        wrong = json.dumps({"mark": "differs", "difference_kind": "grounds_source",
                            "left_quote": "l", "right_quote": "r", "case": "c"})
        with no_sockets():
            result = roles.call_marker(seat_for("judge"), PACK, self.records,
                                       coordinate="mark/case-a/T/rep-1", register="T",
                                       provider_factory=scripted(wrong))
        self.assertTrue(result.blocked)
        self.assertEqual(result.reason, "difference-kind-unknown")


# --------------------------------------------------------------------------
# The token bound
# --------------------------------------------------------------------------


class MaxTokensIsPinnedPerSeatAndCarriesItsArithmetic(unittest.TestCase):
    """Seats Q1 and Q7."""

    def shipped(self, role: str) -> roles.TokenBound:
        endpoint = transport.Endpoint(
            name="ollama/kimi-k3", base_url="https://ollama.invalid/v1", model="k",
            key_env="OLLAMA_API_KEY", family="ollama-cloud/kimi", timeout_seconds=180)
        seat_role = seats.REUSED_ROLES.get(role, role)
        return roles.max_tokens_for(seats.Seat(seat_role, 0, endpoint), role)

    def test_the_table_covers_every_role_and_nothing_else(self):
        self.assertEqual(tuple(sorted(roles.ROLE_MAX_TOKENS)), tuple(sorted(roles.ROLES)))

    def test_the_pinned_table_is_the_one_the_docstring_derives(self):
        self.assertEqual(dict(roles.ROLE_MAX_TOKENS),
                         {"critic": 2048, "defender": 1024, "judge": 2048,
                          "marker": 1024, "variator": 4096})

    def test_the_wall_in_force_is_the_smaller_of_the_timeout_and_the_gateway(self):
        bound = self.shipped("critic")
        self.assertEqual(bound.seat_timeout_seconds, 180)
        self.assertEqual(bound.wall_seconds, 180)
        self.assertEqual(roles.GATEWAY_WALL_SECONDS, 300)

    def test_the_wall_ceiling_is_the_arithmetic_the_docstring_states(self):
        bound = self.shipped("critic")
        self.assertEqual(bound.rate_tokens_per_second, 90)
        self.assertEqual(bound.generation_share, 0.5)
        self.assertEqual(bound.wall_ceiling, int(180 * 0.5 * 90))
        self.assertEqual(bound.wall_ceiling, 8100)

    def test_on_the_shipped_registry_the_contract_and_not_the_wall_sets_the_bound(self):
        for role, pinned in roles.ROLE_MAX_TOKENS.items():
            bound = self.shipped(role)
            self.assertEqual(bound.max_tokens, pinned)
            self.assertFalse(bound.clamped)

    def test_every_pinned_bound_stays_well_under_the_three_hundred_second_wall(self):
        for role in roles.ROLES:
            bound = self.shipped(role)
            self.assertLess(bound.expected_seconds, roles.GATEWAY_WALL_SECONDS / 2)
            self.assertLessEqual(bound.expected_seconds, bound.wall_seconds * 0.5)

    def test_the_expected_seconds_of_each_role_are_the_docstrings_figures(self):
        self.assertEqual(
            {role: self.shipped(role).expected_seconds for role in roles.ROLES},
            {"critic": 22.8, "defender": 11.4, "judge": 22.8,
             "marker": 11.4, "variator": 45.5})

    def test_a_tighter_seat_is_clamped_by_its_wall_and_the_record_says_so(self):
        bound = roles.max_tokens_for(seat_for("critic"), "critic")
        self.assertEqual(bound.wall_seconds, 30)
        self.assertEqual(bound.wall_ceiling, 1350)
        self.assertEqual(bound.max_tokens, 1350)
        self.assertTrue(bound.clamped)
        self.assertTrue(bound.as_dict()["clamped_by_wall"])

    def test_the_arithmetic_rides_with_the_number(self):
        arithmetic = self.shipped("variator").arithmetic()
        for fragment in ("180s", "300s", "0.5", "90 tokens/s", "8100", "4096"):
            self.assertIn(fragment, arithmetic)

    def test_the_variator_bound_is_paraphrase_n_paraphrases_and_scales_with_it(self):
        self.assertEqual(roles.ROLE_MAX_TOKENS["variator"],
                         2 * roles.VARIATOR_TOKENS_PER_PARAPHRASE)
        endpoint = transport.Endpoint(
            name="e", base_url="https://e.invalid/v1", model="m",
            key_env="OLLAMA_API_KEY", family="f", timeout_seconds=600)
        seat = seats.Seat("variator", 0, endpoint)
        self.assertEqual(roles.max_tokens_for(seat, "variator", paraphrase_n=3).role_budget,
                         3 * roles.VARIATOR_TOKENS_PER_PARAPHRASE)

    def test_a_declared_timeout_past_the_gateway_wall_never_raises_the_bound(self):
        endpoint = transport.Endpoint(
            name="e", base_url="https://e.invalid/v1", model="m",
            key_env="OLLAMA_API_KEY", family="f", timeout_seconds=600)
        bound = roles.max_tokens_for(seats.Seat("critic", 0, endpoint), "critic")
        self.assertEqual(bound.wall_seconds, roles.GATEWAY_WALL_SECONDS)
        self.assertEqual(bound.wall_ceiling, int(300 * 0.5 * 90))

    def test_a_seat_too_tight_for_any_conforming_reply_is_refused(self):
        endpoint = transport.Endpoint(
            name="e", base_url="https://e.invalid/v1", model="m",
            key_env="OLLAMA_API_KEY", family="f", timeout_seconds=2)
        with self.assertRaises(roles.RoleRefused) as caught:
            roles.max_tokens_for(seats.Seat("critic", 0, endpoint), "critic")
        self.assertEqual(caught.exception.code, roles.ROLE_TOKEN_BUDGET_UNREACHABLE)

    def test_the_bound_reaches_the_provider_and_not_only_the_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            with no_sockets():
                result = roles.call_critic(
                    seat_for("critic"), PACK, Path(tmp), coordinate="read/retains",
                    provider_factory=synthetic.provider_factory(strict=True))
            sent = json.loads(Path(result.prompt_ref.path).read_text(encoding="utf-8"))
        self.assertEqual(sent["request"]["max_tokens"], result.max_tokens)
        self.assertEqual(sent["settings"]["max_tokens"], result.max_tokens)


# --------------------------------------------------------------------------
# Packs, coordinates and seats
# --------------------------------------------------------------------------


class ThePackIsSentByteForByteAndItsDigestIsRecorded(RolesTestCase):

    def test_the_bytes_that_reach_the_seat_are_the_bytes_that_were_handed_in(self):
        result = self.call("critic", coordinate="read/retains")
        sent = json.loads(Path(result.prompt_ref.path).read_text(encoding="utf-8"))
        self.assertEqual(sent["request"]["messages"],
                         [{"role": "user", "content": PACK.decode("utf-8")}])

    def test_the_material_reaching_seat_two_equals_the_material_reaching_seat_one(self):
        """Surface S7: the material is never paraphrased between seats."""

        sent = []
        for index, token, endpoint in ((0, "judge-a", "synthetic/alpha"),
                                       (1, "judge-b", "synthetic/beta")):
            result = self.call("judge", seat=seat_for("judge", endpoint, index),
                               coordinate="read/retains", seat_token=token)
            sent.append(json.loads(
                Path(result.prompt_ref.path).read_text(encoding="utf-8"))["request"]["messages"])
        self.assertEqual(sent[0], sent[1])

    def test_no_prompt_of_this_modules_own_is_added_beside_the_pack(self):
        result = self.call("critic", coordinate="read/retains")
        sent = json.loads(Path(result.prompt_ref.path).read_text(encoding="utf-8"))
        self.assertEqual(len(sent["request"]["messages"]), 1)
        self.assertEqual(roles.MESSAGE_ROLE, "user")

    def test_a_pack_is_accepted_as_bytes_as_text_and_as_an_object(self):
        from minireason.loop import custody

        class Pack:
            text = PACK
            sha256 = custody.sha256_bytes(PACK)

        for value in (PACK, PACK.decode("utf-8"), {"bytes": PACK}, Pack()):
            self.assertEqual(roles.role_pack(value).digest, custody.sha256_bytes(PACK))

    def test_a_declared_digest_is_recorded_and_compared_never_enforced(self):
        from minireason.loop import custody
        agreeing = roles.role_pack({"bytes": PACK, "sha256": custody.sha256_bytes(PACK)})
        self.assertTrue(agreeing.agrees)
        disagreeing = roles.role_pack({"bytes": PACK, "sha256": "0" * 64})
        self.assertFalse(disagreeing.agrees)
        self.assertEqual(disagreeing.digest, custody.sha256_bytes(PACK))

    def test_a_malformed_pack_or_digest_is_refused(self):
        for value in (b"", 17, {"bytes": PACK, "sha256": "nothex"}):
            with self.assertRaises(roles.RoleRefused) as caught:
                roles.role_pack(value)
            self.assertEqual(caught.exception.code, roles.ROLE_PACK_INVALID)


class TheCoordinateIsTheWriteOnceIdentity(unittest.TestCase):

    def test_a_single_seat_role_has_no_seat_number_in_its_token(self):
        self.assertEqual(roles.Coordinate("critic", "read/x").token, "critic@read/x")

    def test_a_multi_seat_role_names_the_seat_it_spent(self):
        self.assertEqual(roles.Coordinate("judge", "read/x", 1).token, "judge#2@read/x")
        self.assertEqual(roles.Coordinate("judge", "read/x", 1).slug, "read/x/judge-2")

    def test_the_suffixes_the_synthetic_fixture_publishes_are_admissible_keys(self):
        for key in synthetic.READING_COORDINATES:
            for suffix in ("",) + synthetic.PARAPHRASE_SUFFIXES + (synthetic.REREAD_SUFFIX,):
                self.assertTrue(roles.Coordinate("judge", key + suffix).token)

    def test_a_coordinate_that_could_escape_the_records_directory_is_refused(self):
        for key in ("", "/absolute", "read/", "../escape", "read/../x", "read/a b"):
            with self.assertRaises(roles.RoleRefused) as caught:
                roles.Coordinate("critic", key)
            self.assertEqual(caught.exception.code, roles.ROLE_COORDINATE_INVALID)

    def test_the_seed_is_derived_from_the_token_and_is_stable(self):
        where = roles.Coordinate("critic", "read/retains")
        self.assertEqual(roles.seed_for(where), roles.seed_for(where))
        self.assertNotEqual(roles.seed_for(where),
                            roles.seed_for(roles.Coordinate("critic", "read/other")))
        self.assertGreaterEqual(roles.seed_for(where), 0)


class TheSeatHandedInMustHoldTheRoleThatIsAsked(RolesTestCase):

    def test_a_role_that_is_not_a_role_is_refused(self):
        with self.assertRaises(roles.RoleRefused) as caught:
            with no_sockets():
                roles.call_role("decider", seat_for("critic"), PACK, None, self.records,
                                coordinate="read/x", provider_factory=self.factory)
        self.assertEqual(caught.exception.code, roles.ROLE_UNKNOWN)

    def test_a_critic_seat_may_not_answer_a_judge_call(self):
        with self.assertRaises(roles.RoleRefused) as caught:
            self.call("judge", seat=seat_for("critic"), coordinate="read/retains")
        self.assertEqual(caught.exception.code, roles.ROLE_SEAT_MISMATCH)

    def test_the_marker_reuses_a_judge_seat_and_mints_none_of_its_own(self):
        self.assertEqual(seats.REUSED_ROLES["marker"], "judge")
        with self.assertRaises(roles.RoleRefused) as caught:
            self.call("marker", seat=seat_for("variator", "synthetic/beta"),
                      coordinate="mark/case-a/T/rep-1", register="T")
        self.assertEqual(caught.exception.code, roles.ROLE_SEAT_MISMATCH)

    def test_a_schema_that_is_not_the_contracts_own_is_refused(self):
        with self.assertRaises(roles.RoleRefused) as caught:
            with no_sockets():
                roles.call_role("critic", seat_for("critic"), PACK,
                                {"type": "object"}, self.records,
                                coordinate="read/retains", provider_factory=self.factory)
        self.assertEqual(caught.exception.code, roles.ROLE_SCHEMA_NOT_THE_CONTRACT)

    def test_the_contracts_own_schema_is_accepted_when_it_is_passed_explicitly(self):
        with no_sockets():
            result = roles.call_role("critic", seat_for("critic"), PACK,
                                     contracts.schema_for("critic"), self.records,
                                     coordinate="read/retains",
                                     provider_factory=self.factory)
        self.assertTrue(result.ok)


# --------------------------------------------------------------------------
# Reasoning text
# --------------------------------------------------------------------------


class NoReasoningTextIsEverPersisted(RolesTestCase):

    def test_the_record_carries_the_presence_flag_and_no_text(self):
        result = self.call("critic", coordinate="read/retains")
        outcome = result.record["outcome"]
        self.assertIn("reasoning_content_present", outcome)
        self.assertFalse(outcome["reasoning_content_persisted"])
        self.assertIsNone(outcome["reasoning_content_sha256"])

    def test_a_reported_reasoning_token_count_is_kept_and_nothing_else_is(self):
        reply = {"content": json.dumps({"answer": "a", "concedes": False}),
                 "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3,
                           "completion_tokens_details": {"reasoning_tokens": 41}},
                 "reasoning_content_present": True}
        with no_sockets():
            result = roles.call_defender(seat_for("defender", "synthetic/beta"), PACK,
                                         self.records, coordinate="read/retains",
                                         provider_factory=scripted(reply))
        self.assertEqual(result.record["outcome"]["reasoning_tokens"], 41)
        self.assertTrue(result.record["outcome"]["reasoning_content_present"])
        # Every reasoning-named field is a flag, a count or nothing. None of
        # them is a string, which is the only shape reasoning TEXT could take.
        carried = {key: value for key, value in result.record["outcome"].items()
                   if "reasoning" in key}
        self.assertEqual(sorted(carried), ["reasoning_content_persisted",
                                           "reasoning_content_present",
                                           "reasoning_content_sha256",
                                           "reasoning_tokens"])
        for key, value in carried.items():
            self.assertNotIsInstance(value, str, key)

    def test_thinking_is_switched_off_on_a_deepseek_seat_and_absent_elsewhere(self):
        result = self.call("critic", coordinate="read/retains")
        self.assertIsNone(result.record["settings"]["thinking"])
        endpoint = transport.Endpoint(
            name="deepseek-flash", base_url="https://api.deepseek.invalid/v1",
            model="d", key_env="DEEPSEEK_API_KEY", family="deepseek")
        with no_sockets():
            deep = roles.call_critic(
                seats.Seat("critic", 0, endpoint), PACK, self.records,
                coordinate="read/other",
                provider_factory=scripted(json.dumps(
                    {"relation": "none", "passage_quote": "", "case": "",
                     "outside_vocabulary": "",
                     "role_bindings": {"target": "", "defect": "",
                                       "grounds": "", "bearing": ""}})))
        self.assertIs(deep.record["settings"]["thinking"], False)


# --------------------------------------------------------------------------
# The module's own declarations
# --------------------------------------------------------------------------


class TheModuleDeclaresItsVocabularyOnceAndRaisesNoBareLiteral(unittest.TestCase):

    def test_the_role_vocabulary_is_the_one_contracts_owns(self):
        self.assertIs(roles.ROLES, contracts.ROLE_NAMES)

    def test_every_new_code_is_upper_snake_and_carries_a_reason(self):
        self.assertTrue(roles.NEW_CODES)
        for code, reason in roles.NEW_CODES.items():
            self.assertRegex(code, r"\A[A-Z][A-Z0-9_]*\Z")
            self.assertTrue(reason.strip())

    def test_no_replay_is_reused_and_is_not_declared_new(self):
        self.assertIn(roles.NO_REPLAY, loop_types.FAILURE_CODES)
        self.assertNotIn(roles.NO_REPLAY, roles.NEW_CODES)

    def test_every_new_code_is_folded_into_the_failure_table(self):
        """O9, the wave-2 integrator's side of it.

        While this module was on the frontier the assertion was the opposite -
        a key of ``NEW_CODES`` the table already carried was not new - which is
        what "new" meant on the day the module landed. The fold-in makes
        ``types`` the owner of all ten, so the contract is now membership: a
        code declared here and absent from the table would be one a call record
        could carry that no reader can look up.
        """

        for code in roles.NEW_CODES:
            with self.subTest(code=code):
                self.assertIn(code, loop_types.FAILURE_CODES)
                self.assertNotIn(code, loop_types.OUTCOME_CODES)

    def test_no_replay_is_imported_from_types_and_never_retyped_here(self):
        """Wave-2 judge finding 2: one owner for the spelling of one token.

        ``types`` declares it, ``FAILURE_CODES`` is built from that constant and
        this module imports it. A module-level ``NO_REPLAY = "NO_REPLAY"`` here
        would be a second spelling, and a rename in one of the two would have
        been silent.
        """

        self.assertIs(roles.NO_REPLAY, loop_types.NO_REPLAY)
        self.assertIn("NO_REPLAY", roles.__all__)
        source = PACKAGE.read_text(encoding="utf-8")
        self.assertNotIn('NO_REPLAY = "NO_REPLAY"', source)
        self.assertIn("from .types import NO_REPLAY", source)

    def test_every_code_this_module_raises_is_a_module_constant_not_a_literal(self):
        tree = ast.parse(PACKAGE.read_text(encoding="utf-8"))
        declared = {name for name, value in
                    ((t.id, n.value.value)
                     for n in tree.body if isinstance(n, ast.Assign)
                     for t in n.targets
                     if isinstance(t, ast.Name) and isinstance(n.value, ast.Constant)
                     and isinstance(n.value.value, str))}
        # A code this module IMPORTS rather than assigns is still a named
        # constant, and after the wave-2 fold-in ``NO_REPLAY`` is exactly that:
        # ``types`` owns the spelling and this module imports it (judge finding
        # 2). The name has to resolve to a string on the imported module, so an
        # imported callable cannot sneak into the set.
        declared |= {
            alias.asname or alias.name
            for node in tree.body if isinstance(node, ast.ImportFrom)
            for alias in node.names
            if isinstance(getattr(roles, alias.asname or alias.name, None), str)
        }
        offenders = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = getattr(node.func, "id", getattr(node.func, "attr", ""))
            if name not in ("_fail", "RoleRefused", "ProviderArmEnded"):
                continue
            if not node.args:
                continue
            first = node.args[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                offenders.append(first.value)
            elif isinstance(first, ast.Name):
                self.assertIn(first.id, declared | {"code"})
        self.assertEqual(
            [token for token in offenders if token != "CONFIG_INVALID_VALUE"], [],
            "a stable code is raised as a literal instead of a module constant")

    def test_the_block_codes_this_module_uses_are_declared_block_codes(self):
        self.assertEqual(roles.SCHEMA_BLOCK, "blocked:schema")
        self.assertEqual(roles.PROVIDER_BLOCK, "blocked:provider")
        self.assertIn("schema", loop_types.CEILING_BLOCK_REASONS)
        self.assertIn("provider", loop_types.CEILING_BLOCK_REASONS)

    def test_the_module_exports_exactly_what_it_declares(self):
        for name in roles.__all__:
            self.assertTrue(hasattr(roles, name), name)

    def test_the_record_schema_and_kind_mirror_the_predicate_that_reads_them(self):
        self.assertEqual(roles.ROLES_SCHEMA, "minireason.loop.roles.v1")
        self.assertEqual(roles.RECORD_FIELD, obligations.RECORD_FIELD)
        self.assertIn(roles.RECORD_KIND, obligations.RECORD_KINDS)

    def test_this_module_imports_no_sibling_of_its_own_wave(self):
        tree = ast.parse(PACKAGE.read_text(encoding="utf-8"))
        siblings = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                siblings.add(node.module.split(".")[0])
        self.assertEqual(siblings, {"contracts", "custody", "seats", "types"})


if __name__ == "__main__":       # pragma: no cover
    unittest.main()
