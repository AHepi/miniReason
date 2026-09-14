"""W1-SYNTHETIC — the synthetic occurrence and the canned offline deliveries.

Acceptance (design §7, ``W1-SYNTHETIC``): the occurrence imports cleanly and
yields at least one cross-document reference row; the contrast leg differs on
exactly one register at a known ``difference_kind``; each token in ``INDUCIBLE``
produces exactly the intended failure and nothing else; generation is
deterministic from the seed. The build adds: the occurrence passes the fcl1
schema, the use table carries at least one row per reading-vocabulary value
plus rows designed to be unresolved, and zero sockets are opened.
"""

from __future__ import annotations

import hashlib
import json
import os
import socket
import sys
import tempfile
import unittest
from pathlib import Path

from minireason import graph_import_h005, use_relation_h005
from minireason.loop import contracts, custody, standard, synthetic, types
from minireason.provider_openai_compat import Endpoint, ProviderFailure

REPOSITORY = Path(graph_import_h005.__file__).resolve().parents[2]


def _tree(root: Path) -> dict[str, str]:
    """Every file under ``root``, relative POSIX path -> sha256 of its bytes."""

    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


class _Temp(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory(prefix="w1-synthetic-")
        self.addCleanup(self._temp.cleanup)
        self.tmp = Path(self._temp.name)

    def build(self, name: str = "occ", **kwargs) -> synthetic.Occurrence:
        return synthetic.build_occurrence(self.tmp / name, **kwargs)


class NoSockets:
    """Every socket constructor raises for the duration of the block."""

    def __init__(self, case: unittest.TestCase) -> None:
        self.case = case

    def __enter__(self) -> "NoSockets":
        def refuse(*args, **kwargs):  # pragma: no cover - the point is it never runs
            raise AssertionError("a socket was opened")

        self._saved = (socket.socket, socket.create_connection)
        socket.socket = refuse           # type: ignore[assignment]
        socket.create_connection = refuse  # type: ignore[assignment]
        return self

    def __exit__(self, *exc) -> None:
        socket.socket, socket.create_connection = self._saved  # type: ignore[assignment]


# --------------------------------------------------------------------- #
# determinism                                                            #
# --------------------------------------------------------------------- #


class GenerationIsDeterministic(_Temp):
    def test_two_generations_at_one_seed_are_byte_identical(self) -> None:
        left = self.build("left")
        right = self.build("right")
        self.assertEqual(_tree(left.root), _tree(right.root))
        self.assertEqual(left.plan_id, right.plan_id)

    def test_two_generations_with_one_induction_are_byte_identical(self) -> None:
        first = self.build("a", induce=("provider_arm_failure", "custody_mismatch"))
        second = self.build("b", induce=("custody_mismatch", "provider_arm_failure"))
        self.assertEqual(_tree(first.root), _tree(second.root))

    def test_a_different_seed_changes_the_bytes(self) -> None:
        base = self.build("base")
        other = self.build("other", seed=synthetic.DEFAULT_SEED + 1)
        self.assertNotEqual(_tree(base.root), _tree(other.root))
        self.assertEqual(set(_tree(base.root)), set(_tree(other.root)))

    def test_the_script_is_a_pure_function_of_seed_and_induce(self) -> None:
        first = synthetic.canned_responses(synthetic.DEFAULT_SEED, induce=("ensemble_split",))
        second = synthetic.canned_responses(synthetic.DEFAULT_SEED, induce=("ensemble_split",))
        self.assertEqual(first, second)
        self.assertNotEqual(
            first, synthetic.canned_responses(synthetic.DEFAULT_SEED + 1,
                                              induce=("ensemble_split",)))

    def test_nothing_here_reads_a_clock(self) -> None:
        source = Path(synthetic.__file__).read_text(encoding="utf-8")
        for forbidden in ("time.time", "datetime.now", "utcnow", "import random",
                          "uuid4", "monotonic"):
            self.assertNotIn(forbidden, source, forbidden)

    def test_every_recorded_moment_is_used_and_fixed(self) -> None:
        occurrence = self.build()
        stamps = sorted(
            json.loads(path.read_text(encoding="utf-8"))["finished_utc"]
            for path in (occurrence.root / "responses").rglob("*.json")
        )
        self.assertEqual(stamps, sorted(synthetic.RECORDED_MOMENTS))


# --------------------------------------------------------------------- #
# the occurrence                                                         #
# --------------------------------------------------------------------- #


class TheOccurrenceIsWellFormed(_Temp):
    def test_it_declares_two_arms_and_one_problem_with_cycles(self) -> None:
        occurrence = self.build()
        arms = json.loads(occurrence.arms.read_text(encoding="utf-8"))
        self.assertEqual(sorted(arms["arms"]), sorted(synthetic.ARM_NAMES))
        self.assertEqual(arms["provider"], "offline")
        self.assertEqual(arms["scope"], {"problems": [synthetic.PROBLEM_ID], "cycles": [1]})
        material = json.loads(occurrence.material.read_text(encoding="utf-8"))
        self.assertEqual([p["id"] for p in material["problems"]], [synthetic.PROBLEM_ID])
        self.assertEqual(len(material["problems"][0]["templates"]), 3)

    def test_the_fcl_arm_is_the_importers_own_declared_fcl_surface_arm(self) -> None:
        self.assertIn(synthetic.FCL_ARM, graph_import_h005.FCL_SURFACE_ARMS)
        self.assertNotIn(synthetic.PROSE_ARM, graph_import_h005.FCL_SURFACE_ARMS)

    def test_every_fcl_commitment_surface_passes_the_fcl1_schema(self) -> None:
        occurrence = self.build()
        validator = graph_import_h005.fcl1_validator()
        seen = 0
        for path in sorted((occurrence.root / "artifacts").rglob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            if record["coordinate"]["arm"] != synthetic.FCL_ARM:
                continue
            document, failure, detail = graph_import_h005.parse_fcl1_document(
                record["commitments"], validator)
            self.assertIsNone(failure, f"{path}: {detail}")
            self.assertIsNotNone(document)
            seen += 1
        self.assertEqual(seen, len(synthetic.NODE_IDS))

    def test_the_contrast_legs_documents_also_pass_the_fcl1_schema(self) -> None:
        validator = graph_import_h005.fcl1_validator()
        leg = synthetic.contrast_leg()
        for case in leg["cases"].values():
            for replicate in case["replicates"].values():
                for side in ("ORIGINAL", "CONTROL"):
                    _document, failure, detail = graph_import_h005.parse_fcl1_document(
                        replicate[side], validator)
                    self.assertIsNone(failure, detail)

    def test_the_plan_identity_is_the_importers_own_and_holds(self) -> None:
        occurrence = self.build()
        plan = json.loads(occurrence.plan.read_text(encoding="utf-8"))
        body = {key: value for key, value in plan.items() if key != "plan_id"}
        self.assertEqual(graph_import_h005.study_digest(body), plan["plan_id"])
        self.assertEqual(plan["schema"], graph_import_h005.PLAN_RECORD_SCHEMA)

    @unittest.skipUnless((REPOSITORY / "tools"
                          / "multicycle_commitment_study_multi_v2.py").exists(),
                         "runner v2 is not in this checkout")
    def test_material_and_arms_satisfy_runner_v2s_own_validators(self) -> None:
        if str(REPOSITORY) not in sys.path:
            sys.path.insert(0, str(REPOSITORY))
        runner = __import__("tools.multicycle_commitment_study_multi_v2",
                            fromlist=["validate_material"])
        occurrence = self.build()
        runner.validate_material(json.loads(occurrence.material.read_text(encoding="utf-8")))
        saved = runner._REGISTRY_OVERRIDE
        runner.set_registry(synthetic.endpoints_registry())
        try:
            _raw, arms, scope = runner.read_arms(occurrence.arms)
            self.assertEqual(sorted(arms), sorted(synthetic.ARM_NAMES))
            self.assertEqual(scope, {"problems": [synthetic.PROBLEM_ID], "cycles": [1]})
            self.assertEqual(runner.provider_mode(arms), "offline")
            self.assertEqual(sorted(runner.key_caps(arms)),
                             sorted(synthetic.SYNTHETIC_KEY_ENVS))
        finally:
            runner.set_registry(saved)

    @unittest.skipUnless((REPOSITORY / "tools"
                          / "multicycle_commitment_study_multi_v2.py").exists(),
                         "runner v2 is not in this checkout")
    def test_runner_v2_can_freeze_the_plan_through_the_freeze_seam(self) -> None:
        if str(REPOSITORY) not in sys.path:
            sys.path.insert(0, str(REPOSITORY))
        runner = __import__("tools.multicycle_commitment_study_multi_v2",
                            fromlist=["verify"])
        saved = runner._REGISTRY_OVERRIDE
        try:
            occurrence = self.build("frozen",
                                    freeze=synthetic.runner_freeze(REPOSITORY))
            _material, plan = runner.verify(REPOSITORY, occurrence.root)
            self.assertEqual(plan["plan_id"], occurrence.plan_id)
            self.assertEqual(plan["provider_mode"], "offline")
            self.assertEqual(plan["max_calls"],
                             len(synthetic.ARM_NAMES) * len(synthetic.NODE_IDS))
            # and the occurrence still reads
            table = use_relation_h005.build_use_table(occurrence.root)
            self.assertEqual(len(table.rows), 8)
        finally:
            runner.set_registry(saved)


# --------------------------------------------------------------------- #
# import and use-relation, offline                                       #
# --------------------------------------------------------------------- #


class TheOccurrenceImportsAndReads(_Temp):
    def test_the_graph_import_succeeds_with_no_socket(self) -> None:
        occurrence = self.build()
        with NoSockets(self):
            report = graph_import_h005.import_occurrence(occurrence.root, self.tmp / "graph")
        self.assertTrue((self.tmp / "graph" / "report.json").is_file())
        self.assertEqual(json.loads(report.to_json())["schema"],
                         graph_import_h005.REPORT_SCHEMA)

    def test_the_use_table_carries_a_row_for_every_planned_reading(self) -> None:
        occurrence = self.build()
        with NoSockets(self):
            table = use_relation_h005.build_use_table(occurrence.root)
        keys = {(row.referring_coordinate_key, row.referring_record_id,
                 row.ref_field, row.ref_verbatim) for row in table.rows}
        for name, planned in synthetic.READING_COORDINATES.items():
            self.assertIn(planned, keys, name)
        self.assertGreaterEqual(len(table.rows), len(standard.READING_VOCABULARY))

    def test_every_reading_vocabulary_value_has_at_least_one_row(self) -> None:
        planned = set(synthetic.READING_PLAN.values())
        self.assertEqual(planned, set(standard.READING_VOCABULARY))
        self.assertIn(standard.UNRESOLVED_TOKEN, planned)

    def test_rows_designed_to_be_unresolved_carry_no_lexical_overlap(self) -> None:
        occurrence = self.build()
        table = use_relation_h005.build_use_table(occurrence.root)
        rows = {(row.referring_coordinate_key, row.referring_record_id,
                 row.ref_field, row.ref_verbatim): row for row in table.rows}
        row = rows[synthetic.READING_COORDINATES["read/unresolved-a"]]
        self.assertEqual(row.lexical_overlap_note, use_relation_h005.NO_OVERLAP_NOTE)
        self.assertEqual(row.referring_body_passages, ())

    def test_the_refs_written_to_resolve_to_nothing_do(self) -> None:
        occurrence = self.build()
        table = use_relation_h005.build_use_table(occurrence.root)
        dangling = {(entry.referring_coordinate_key, entry.referring_record_id,
                     entry.ref_field, entry.ref_verbatim) for entry in table.unresolved_refs}
        for planned in synthetic.UNRESOLVABLE_REFS:
            self.assertIn(planned, dangling)

    def test_the_prose_arm_is_reported_as_unread_and_never_parsed(self) -> None:
        occurrence = self.build()
        table = use_relation_h005.build_use_table(occurrence.root)
        unread = {node.coordinate_key for node in table.nodes_not_read}
        self.assertEqual(
            unread,
            {f"{synthetic.PROBLEM_ID}/{synthetic.PROSE_ARM}/cycle01/{node}"
             for node in synthetic.NODE_IDS})
        for node in table.nodes_not_read:
            self.assertEqual(node.commitment_surface, "prose_not_parsed")

    def test_a_cross_document_row_names_a_different_coordinate(self) -> None:
        occurrence = self.build()
        table = use_relation_h005.build_use_table(occurrence.root)
        self.assertTrue(table.rows)
        for row in table.rows:
            self.assertNotEqual(row.referring_coordinate_key, row.target_coordinate_key)


# --------------------------------------------------------------------- #
# the scripted outputs                                                   #
# --------------------------------------------------------------------- #


class TheScriptedOutputsAreValid(_Temp):
    def _drive(self, factory: synthetic.ScriptedProviders) -> dict[tuple[str, str, str], dict]:
        """Run every scripted role coordinate through a real OfflineProvider."""

        produced: dict[tuple[str, str, str], dict] = {}
        with NoSockets(self):
            for index, ((role, coordinate), _script) in enumerate(sorted(factory.script.items())):
                if role == "delivery":
                    continue
                seats = list(synthetic.JUDGE_SEATS) if role == "judge" else [None]
                register = coordinate.split("/")[2] if role == "marker" else None
                for seat in seats:
                    provider = factory.provider(
                        role, coordinate, self.tmp / "records" / f"{index:04d}-{seat}",
                        seat=seat)
                    result = provider.complete(
                        [{"role": "user", "content": "Return one json object."}],
                        response_format={"type": "json_object"},
                        max_tokens=4096, reasoning_effort="low")
                    body = json.loads(result.content)
                    validation = contracts.check(role, body, register=register)
                    self.assertTrue(validation.ok,
                                    f"{role} {coordinate} {seat}: "
                                    f"{validation.reason} {validation.message}")
                    produced[(role, coordinate, seat or "")] = body
        return produced

    def test_every_scripted_output_validates_against_its_contract(self) -> None:
        produced = self._drive(synthetic.provider_factory(induce=synthetic.INDUCIBLE))
        self.assertGreater(len(produced), len(synthetic.READING_COORDINATES))
        roles = {role for role, _coordinate, _seat in produced}
        self.assertEqual(roles, set(contracts.ROLE_NAMES))

    def test_no_socket_is_opened_and_the_factory_counts_every_provider(self) -> None:
        factory = synthetic.provider_factory()
        produced = self._drive(factory)
        self.assertEqual(factory.calls, len(produced))
        self.assertEqual(len(factory.handed), factory.calls)

    def test_the_offline_provider_records_say_nothing_was_contacted(self) -> None:
        factory = synthetic.provider_factory()
        with NoSockets(self):
            provider = factory.provider("critic", "read/retains", self.tmp / "one")
            provider.complete([{"role": "user", "content": "json"}],
                              response_format={"type": "json_object"},
                              max_tokens=4096, reasoning_effort="low")
        # the provider module's own counter, and the kind it records
        self.assertEqual(provider.kind, "offline-scripted")
        self.assertEqual(provider.calls, 1)
        record = json.loads((self.tmp / "one" / "call-0001.request.json")
                            .read_text(encoding="utf-8"))
        self.assertIsNone(record["url"])
        self.assertEqual(record["request_header_names"], [])
        self.assertIn("not_contacted_url", record)

    def test_an_unscripted_coordinate_is_synthesised_loosely_and_refused_strictly(self) -> None:
        loose = synthetic.provider_factory()
        body = json.loads(loose.script_for("critic", "read/made-up")[0]["content"])
        self.assertTrue(contracts.check("critic", body).ok)
        strict = synthetic.provider_factory(strict=True)
        with self.assertRaises(synthetic.SyntheticError) as raised:
            strict.script_for("critic", "read/made-up")
        self.assertEqual(raised.exception.code, "SYNTHETIC_COORDINATE_UNSCRIPTED")

    def test_the_runner_shaped_factory_reads_the_coordinate_off_the_records_dir(self) -> None:
        factory = synthetic.provider_factory()
        records = (self.tmp / "provider" / synthetic.PROBLEM_ID / synthetic.FCL_ARM
                   / "cycle01" / "account")
        self.assertEqual(factory.coordinate_of(records),
                         f"{synthetic.PROBLEM_ID}/{synthetic.FCL_ARM}/cycle01/account")
        with NoSockets(self):
            provider = factory(synthetic.SYNTHETIC_ENDPOINTS[0], records)
            result = provider.complete([{"role": "user", "content": "json"}],
                                       response_format={"type": "json_object"},
                                       max_tokens=4096, reasoning_effort="low")
        envelope = json.loads(result.content)
        self.assertEqual(sorted(envelope), ["body", "commitments"])

    def test_the_delivered_bytes_are_the_occurrences_own(self) -> None:
        occurrence = self.build()
        script = synthetic.canned_responses()
        for arm in synthetic.ARM_NAMES:
            for node in synthetic.NODE_IDS:
                key = f"{synthetic.PROBLEM_ID}/{arm}/cycle01/{node}"
                text = (occurrence.root / "responses" / synthetic.PROBLEM_ID / arm
                        / "cycle01" / f"{node}.txt")
                self.assertEqual(script[("delivery", key)][0]["content"],
                                 text.read_text(encoding="utf-8"))


# --------------------------------------------------------------------- #
# the induced failures, one at a time                                    #
# --------------------------------------------------------------------- #


class EachInductionProducesItsOwnFailure(_Temp):
    def test_describe_lists_every_inducible_token_with_its_code(self) -> None:
        described = synthetic.describe()
        self.assertEqual(tuple(row.token for row in described), synthetic.INDUCIBLE)
        for row in described:
            self.assertEqual(row.code, synthetic.INDUCED_CODES[row.token])
            self.assertIn(row.step, types.STEP_KINDS)
            self.assertTrue(row.note)
        self.assertEqual(len(synthetic.describe(("ensemble_split",))), 1)

    def test_every_code_named_is_declared_somewhere(self) -> None:
        for token, code in synthetic.INDUCED_CODES.items():
            declared = (code in types.FAILURE_CODES or code in types.BLOCK_CODES
                        or code in synthetic.NEW_CODES)
            self.assertTrue(declared, f"{token} -> {code}")
        for code, reason in synthetic.NEW_CODES.items():
            self.assertRegex(code, r"^[A-Z][A-Z0-9_]*$")
            self.assertTrue(reason.strip())
        self.assertEqual(sorted(synthetic.INDUCED_CODES), sorted(synthetic.INDUCIBLE))

    def test_an_unknown_induction_token_is_refused(self) -> None:
        with self.assertRaises(synthetic.SyntheticError) as raised:
            self.build("bad", induce=("no_such_failure",))
        self.assertEqual(raised.exception.code, "SYNTHETIC_INDUCTION_UNKNOWN")
        with self.assertRaises(synthetic.SyntheticError):
            synthetic.canned_responses(induce=("no_such_failure",))
        with self.assertRaises(synthetic.SyntheticError):
            synthetic.describe(("no_such_failure",))

    # -- provider failure ------------------------------------------------ #

    def test_a_provider_failure_ends_one_arm_and_leaves_the_others_running(self) -> None:
        factory = synthetic.provider_factory(induce=("provider_arm_failure",))
        with NoSockets(self):
            ended = factory.provider("delivery", synthetic.FAILED_COORDINATE,
                                     self.tmp / "ended")
            with self.assertRaises(ProviderFailure) as raised:
                ended.complete([{"role": "user", "content": "json"}],
                               response_format={"type": "json_object"},
                               max_tokens=4096, reasoning_effort="low")
            self.assertEqual(raised.exception.code,
                             synthetic.INDUCED_CODES["provider_arm_failure"])
            key = f"{synthetic.PROBLEM_ID}/{synthetic.FCL_ARM}/cycle01/response"
            other = factory.provider("delivery", key, self.tmp / "other")
            self.assertTrue(other.complete(
                [{"role": "user", "content": "json"}],
                response_format={"type": "json_object"},
                max_tokens=4096, reasoning_effort="low").content)

    def test_the_ended_arm_leaves_a_failed_receipt_and_no_artifact(self) -> None:
        occurrence = self.build("ended", induce=("provider_arm_failure",))
        stem = synthetic.FAILED_COORDINATE
        self.assertFalse((occurrence.root / "artifacts" / f"{stem}.json").exists())
        receipt = json.loads(
            (occurrence.root / "responses" / f"{stem}.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["status"], "FAILED")
        self.assertEqual(receipt["failure_code"],
                         synthetic.INDUCED_CODES["provider_arm_failure"])
        self.assertNotIn(stem, occurrence.coordinates)
        # every other coordinate still delivered, and the table still reads
        table = use_relation_h005.build_use_table(occurrence.root)
        self.assertEqual(len(table.rows), 8)

    # -- step timeout ---------------------------------------------------- #

    def test_a_step_timeout_is_raised_with_the_step_timeout_code(self) -> None:
        factory = synthetic.provider_factory(induce=("step_timeout",))
        key = f"{synthetic.PROBLEM_ID}/{synthetic.FCL_ARM}/cycle01/response"
        with self.assertRaises(synthetic.SyntheticStepTimeout) as raised:
            factory.provider("delivery", key, self.tmp / "timeout")
        self.assertEqual(raised.exception.code, "STEP_TIMEOUT")
        self.assertIn("STEP_TIMEOUT", types.FAILURE_CODES)
        without = synthetic.provider_factory()
        self.assertIsNotNone(without.provider("delivery", key, self.tmp / "fine"))

    # -- ensemble split -------------------------------------------------- #

    def test_an_ensemble_split_is_one_cell_and_is_never_voted(self) -> None:
        split = synthetic.canned_responses(induce=("ensemble_split",))
        plain = synthetic.canned_responses()
        for coordinate in synthetic.READING_COORDINATES:
            rulings = [json.loads(entry["content"])["sustained"]
                       for entry in plain[("judge", coordinate)]]
            self.assertEqual(len(set(rulings)), 1, coordinate)
        splits = [coordinate for coordinate in synthetic.READING_COORDINATES
                  if len({json.loads(entry["content"])["sustained"]
                          for entry in split[("judge", coordinate)]}) > 1]
        self.assertEqual(splits, ["read/qualifies"])
        self.assertEqual(len(split[("judge", "read/qualifies")]),
                         len(synthetic.JUDGE_SEATS))

    # -- paraphrase flip ------------------------------------------------- #

    def test_a_paraphrase_flip_is_one_row_and_only_on_the_paraphrase(self) -> None:
        flipped = synthetic.canned_responses(induce=("paraphrase_flip",))
        rows = set()
        for (role, coordinate), entries in flipped.items():
            if role != "judge":
                continue
            if any(not json.loads(entry["content"])["sustained"] for entry in entries):
                rows.add(coordinate)
        self.assertEqual(rows, {"read/repairs" + suffix
                                for suffix in synthetic.PARAPHRASE_SUFFIXES})
        # the first, unparaphrased ruling still sustains
        self.assertTrue(all(json.loads(entry["content"])["sustained"]
                            for entry in flipped[("judge", "read/repairs")]))

    def test_a_paraphrase_holds_the_quoted_span_byte_identically(self) -> None:
        script = synthetic.canned_responses()
        for coordinate in synthetic.READING_COORDINATES:
            quote = json.loads(
                script[("critic", coordinate)][0]["content"])["passage_quote"]
            if not quote:
                continue
            paraphrases = json.loads(
                script[("variator", coordinate)][0]["content"])["paraphrases"]
            self.assertTrue(paraphrases)
            for paraphrase in paraphrases:
                self.assertIn(quote, paraphrase, coordinate)

    # -- referential integrity ------------------------------------------- #

    def test_a_non_unique_offset_quotes_a_phrase_the_surface_carries_twice(self) -> None:
        occurrence = self.build()
        table = use_relation_h005.build_use_table(occurrence.root)
        rows = {(row.referring_coordinate_key, row.referring_record_id,
                 row.ref_field, row.ref_verbatim): row for row in table.rows}
        row = rows[synthetic.READING_COORDINATES["read/rejects"]]
        surface = (row.referring_record_verbatim or "") + (row.target_record_verbatim or "")
        self.assertEqual(surface.count(synthetic.DUPLICATED_PHRASE), 2)
        quote = json.loads(synthetic.canned_responses()[
            ("critic", "read/rejects")][0]["content"])["passage_quote"]
        self.assertEqual(quote, synthetic.DUPLICATED_PHRASE)

    def test_every_other_critic_quote_resolves_exactly_once(self) -> None:
        occurrence = self.build()
        table = use_relation_h005.build_use_table(occurrence.root)
        rows = {(row.referring_coordinate_key, row.referring_record_id,
                 row.ref_field, row.ref_verbatim): row for row in table.rows}
        script = synthetic.canned_responses()
        for name, key in synthetic.READING_COORDINATES.items():
            if name == "read/rejects":
                continue
            quote = json.loads(script[("critic", name)][0]["content"])["passage_quote"]
            if not quote:
                continue
            row = rows[key]
            if row.ref_grain == "artifact":
                # The ref names the whole contribution, so the target side of
                # the resolvable surface is the owning document, not one record.
                target = json.loads((occurrence.root / "artifacts"
                                     / f"{row.target_coordinate_key}.json")
                                    .read_text(encoding="utf-8"))["commitments"]
            else:
                target = row.target_record_verbatim or ""
            surface = "\n".join(filter(None, [
                row.referring_record_verbatim, target,
                *[passage.text for passage in row.referring_body_passages]]))
            self.assertEqual(surface.count(quote), 1, name)

    def test_a_decisive_point_absent_from_the_surface_is_one_row(self) -> None:
        induced = synthetic.canned_responses(induce=("decisive_point_absent",))
        plain = synthetic.canned_responses()
        absent = "a phrase that appears in neither the case nor the answer"
        rows = {coordinate for (role, coordinate), entries in induced.items()
                if role == "judge"
                and any(json.loads(e["content"])["decisive_point"] == absent
                        for e in entries)}
        self.assertEqual(rows, {"read/re-deploys",
                                *("read/re-deploys" + suffix
                                  for suffix in synthetic.PARAPHRASE_SUFFIXES)})
        for (role, _coordinate), entries in plain.items():
            if role != "judge":
                continue
            for entry in entries:
                self.assertNotEqual(json.loads(entry["content"])["decisive_point"], absent)

    def test_a_decisive_point_otherwise_occurs_exactly_once_in_the_exchange(self) -> None:
        script = synthetic.canned_responses()
        for coordinate in synthetic.READING_COORDINATES:
            case = json.loads(script[("critic", coordinate)][0]["content"])["case"]
            answer = json.loads(script[("defender", coordinate)][0]["content"])["answer"]
            exchange = case + "\n" + answer
            for entry in script[("judge", coordinate)]:
                decisive = json.loads(entry["content"])["decisive_point"]
                self.assertEqual(exchange.count(decisive), 1, coordinate)

    # -- the baseline collision ------------------------------------------ #

    def test_the_contrast_leg_differs_on_exactly_one_register_per_case(self) -> None:
        leg = synthetic.contrast_leg()
        self.assertEqual(sorted(leg["cases"]), sorted(synthetic.CONTRAST_CASES))
        registers = set()
        for name, case in leg["cases"].items():
            self.assertEqual(sorted(case["replicates"]),
                             sorted(synthetic.CONTRAST_REPLICATES))
            self.assertIn(case["register"], standard.REGISTER_IDS)
            self.assertIn(case["difference_kind"],
                          standard.DIFFERENCE_KINDS[case["register"]])
            registers.add(case["register"])
        self.assertEqual(registers, set(standard.REGISTER_IDS))

    def test_one_case_collides_with_the_sealed_baseline_kind_set(self) -> None:
        leg = synthetic.contrast_leg()
        colliding = sorted(name for name, case in leg["cases"].items()
                           if case["collides_with_baseline"])
        self.assertEqual(colliding, ["case-b"])
        marker = json.loads(synthetic.canned_responses()[
            ("marker", "mark/case-b/E/rep-1")][0]["content"])
        self.assertEqual(marker["mark"], "differs")
        self.assertIn(marker["difference_kind"], synthetic.BASELINE_KINDS["E"])
        self.assertTrue(contracts.check("marker", marker, register="E").ok)

    def test_one_replicate_is_byte_identical_for_the_identity_defeater(self) -> None:
        leg = synthetic.contrast_leg()
        identical = [(name, replicate)
                     for name, case in leg["cases"].items()
                     for replicate, sides in case["replicates"].items()
                     if sides["byte_identical"]]
        self.assertEqual(identical, [("case-d", "rep-1")])
        sides = leg["cases"]["case-d"]["replicates"]["rep-1"]
        self.assertEqual(sides["ORIGINAL"], sides["CONTROL"])

    # -- the re-read refusal --------------------------------------------- #

    def test_the_reread_coordinate_is_scripted_and_nominates_a_relation(self) -> None:
        script = synthetic.canned_responses()
        key = ("critic", "read/unresolved-a" + synthetic.REREAD_SUFFIX)
        self.assertIn(key, script)
        body = json.loads(script[key][0]["content"])
        self.assertIn(body["relation"], standard.NOMINABLE_RELATIONS)
        # the first reading of that row ended at one call with "none"
        first = json.loads(script[("critic", "read/unresolved-a")][0]["content"])
        self.assertEqual(first["relation"], standard.NONE_TOKEN)
        self.assertEqual(synthetic.READING_PLAN["read/unresolved-a"],
                         standard.UNRESOLVED_TOKEN)

    def test_the_other_unresolved_row_is_forced_by_outside_vocabulary(self) -> None:
        body = json.loads(synthetic.canned_responses()[
            ("critic", "read/unresolved-b")][0]["content"])
        self.assertTrue(body[contracts.OUTSIDE_VOCABULARY_FIELD])
        self.assertEqual(synthetic.READING_PLAN["read/unresolved-b"],
                         standard.UNRESOLVED_TOKEN)

    # -- the custody mismatch -------------------------------------------- #

    def test_the_custody_fixture_drifts_only_when_induced(self) -> None:
        clean = self.build("clean")
        pins = json.loads((clean.custody / "pins.json").read_text(encoding="utf-8"))
        self.assertEqual(custody.verify_pins(pins, clean.custody), [])

        drifted = self.build("drifted", induce=("custody_mismatch",))
        pins = json.loads((drifted.custody / "pins.json").read_text(encoding="utf-8"))
        findings = custody.verify_pins(pins, drifted.custody)
        self.assertEqual([finding.code for finding in findings],
                         [synthetic.INDUCED_CODES["custody_mismatch"]])
        self.assertEqual(findings[0].path, "pinned_source.txt")

    # -- the appellate ruling -------------------------------------------- #

    def test_the_appellate_ruling_file_is_written_and_names_its_reopen_reason(self) -> None:
        occurrence = self.build("appeal", induce=("appellate_ruling",))
        ruling = json.loads(occurrence.appeal.read_text(encoding="utf-8"))
        self.assertTrue(ruling["induced"])
        self.assertEqual(ruling["against"], "validity_node")
        self.assertIn(ruling["reopen_reason"], standard.REOPEN_REASONS)
        self.assertEqual(ruling["expected_code"], "APPELLATE_RULING_APPLIED")
        self.assertIn("APPELLATE_RULING_APPLIED", synthetic.NEW_CODES)
        self.assertEqual(ruling["reading_coordinate"], "read/retains")
        self.assertFalse(json.loads(
            self.build("plain").appeal.read_text(encoding="utf-8"))["induced"])


# --------------------------------------------------------------------- #
# the synthetic endpoint registry                                        #
# --------------------------------------------------------------------- #


class TheRegistryIsAFiction(unittest.TestCase):
    def test_it_declares_two_families_and_two_key_env_names(self) -> None:
        registry = synthetic.endpoints_registry()
        self.assertEqual(len(registry), 2)
        self.assertEqual({endpoint.family for endpoint in registry.values()},
                         set(synthetic.SYNTHETIC_FAMILIES))
        self.assertEqual({endpoint.key_env for endpoint in registry.values()},
                         set(synthetic.SYNTHETIC_KEY_ENVS))
        for endpoint in registry.values():
            self.assertIsInstance(endpoint, Endpoint)
            self.assertIn(".invalid/", endpoint.base_url)

    def test_no_real_credential_name_and_no_credential_value_appears(self) -> None:
        real = set(custody.ALWAYS_SCANNED_ENVS)
        self.assertFalse(real & set(synthetic.SYNTHETIC_KEY_ENVS))
        for name in synthetic.SYNTHETIC_KEY_ENVS:
            self.assertIsNone(os.environ.get(name),
                              "the synthetic key_env names must name nothing")
        source = Path(synthetic.__file__).read_text(encoding="utf-8")
        self.assertNotIn("os.environ", source)
        self.assertNotIn("getenv", source)

    def test_the_two_judge_seats_carry_distinct_families(self) -> None:
        factory = synthetic.provider_factory()
        families = {factory.endpoint_for("judge", seat).family
                    for seat in synthetic.JUDGE_SEATS}
        self.assertEqual(len(families), len(synthetic.JUDGE_SEATS))
        critic = factory.endpoint_for("critic").family
        defender = factory.endpoint_for("defender").family
        self.assertNotEqual(critic, defender)

    def test_the_registry_document_reloads_through_the_providers_own_loader(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "endpoints.json"
            path.write_text(json.dumps(synthetic.endpoints_document()), encoding="utf-8")
            from minireason.provider_openai_compat import load_endpoints
            loaded = load_endpoints(path)
        self.assertEqual(sorted(loaded), sorted(synthetic.endpoints_registry()))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
