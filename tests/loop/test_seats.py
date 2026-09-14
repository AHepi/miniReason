"""Tests for ``minireason.loop.seats`` (wave-plan module ``W1-SEATS``).

Every clause of the module's acceptance list has at least one test named after
it:

* ``Two judge seats always carry distinct family labels``
* ``selection is a pure byte-stable function of (registry, config)``
* ``a registry with one family raises FAMILY_COUNT_INSUFFICIENT rather than
  degrading silently``
* ``the gate is multicycle_commitment_study_multi_v2.key_gate imported, not
  reimplemented, and never admits a sixth concurrent call per key_env``
* ``the pins record key_env per seat``

and so does every clause the wave brief adds: a config that names a seat pins
it; the pinned table is canonical JSON with a sha256; substituting an endpoint
mints a new plan; nothing in the module orders endpoints by anything but a
sorted family label and a sorted endpoint name.

No test here writes a file, opens a socket, or reads a credential: the only
values put into ``os.environ`` are obvious fakes, removed again by
``patch.dict``, and they exist solely to prove that no credential can reach the
seat table.
"""

from __future__ import annotations

import ast
import dataclasses
import hashlib
import json
import os
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

STAGING = Path(__file__).resolve().parents[2]
if str(STAGING / "src") not in sys.path:
    sys.path.insert(0, str(STAGING / "src"))
if str(STAGING) not in sys.path:
    sys.path.insert(0, str(STAGING))

from minireason.loop import seats as S  # noqa: E402
from minireason.loop.contracts import ROLE_NAMES  # noqa: E402
from minireason.loop.seats import (  # noqa: E402
    FAMILY_COUNT_INSUFFICIENT,
    MAX_PER_KEY,
    NEW_CODES,
    REGISTRY_INVALID,
    RUNNER_NOT_IMPORTABLE,
    SEAT_COUNT_INSUFFICIENT,
    SEAT_ROLES,
    SEATS_SCHEMA,
    Registry,
    Seat,
    SeatPlan,
    SeatsRefused,
    key_cap_for,
    key_gate_for,
    lineage,
    load_registry,
    require_cross_family_judges,
    runner_module,
    select_seats,
)
from minireason.loop.types import FAILURE_CODES, LoopConfig, LoopError, SeatsConfig  # noqa: E402
from minireason.provider_openai_compat import ENDPOINTS_PATH, Endpoint  # noqa: E402

from tools import multicycle_commitment_study_multi_v2 as runner  # noqa: E402

SOURCE_PATH = Path(S.__file__).resolve()
SOURCE = SOURCE_PATH.read_text(encoding="utf-8")

#: A fake, obviously not a credential, long enough to clear the 8-byte floor.
FAKE_KEY = "fake-not-a-credential-0123456789"


def endpoint(name: str, family: str, *, key_env: str = "OLLAMA_API_KEY",
             model: str | None = None, max_concurrency: int = 5,
             timeout_seconds: int = 180) -> Endpoint:
    return Endpoint(name=name, base_url="https://example.invalid/v1",
                    model=model or f"{name}-model", key_env=key_env,
                    family=family, max_concurrency=max_concurrency,
                    timeout_seconds=timeout_seconds)


def registry(*specs: tuple[str, str]) -> Registry:
    return Registry.of([endpoint(name, family) for name, family in specs])


#: Two families, five endpoints: enough for the judges, not enough to keep the
#: critic and the defender out of a judge family.
NARROW = registry(("a1", "A"), ("a2", "A"), ("a3", "A"), ("b1", "B"), ("b2", "B"))

#: Six families, one endpoint each: every family constraint is satisfiable.
WIDE = registry(("e1", "F1"), ("e2", "F2"), ("e3", "F3"),
                ("e4", "F4"), ("e5", "F5"), ("e6", "F6"))


class TheRegistryLoads(unittest.TestCase):

    def test_the_shipped_registry_loads_and_is_ordered_by_family_then_name(self):
        loaded = load_registry()
        ordered = sorted(loaded.endpoints, key=lambda e: (e.family, e.name))
        self.assertEqual(list(loaded.endpoints), ordered)
        self.assertEqual(loaded.families, tuple(sorted(set(loaded.families))))

    def test_the_default_path_is_the_transports_own_endpoints_file(self):
        self.assertEqual(load_registry().names, load_registry(ENDPOINTS_PATH).names)

    def test_a_missing_registry_file_is_refused_as_registry_invalid(self):
        with self.assertRaises(SeatsRefused) as caught:
            load_registry(STAGING / "src" / "minireason" / "data" / "no-such.json")
        self.assertEqual(caught.exception.code, REGISTRY_INVALID)

    def test_a_registry_of_the_wrong_shape_is_refused_not_coerced(self):
        for bad in ({"x": "not an endpoint"}, [object()], 7):
            with self.subTest(bad=bad), self.assertRaises(SeatsRefused) as caught:
                Registry.of(bad)
            self.assertEqual(caught.exception.code, REGISTRY_INVALID)

    def test_an_empty_registry_is_refused(self):
        with self.assertRaises(SeatsRefused) as caught:
            Registry.of({})
        self.assertEqual(caught.exception.code, REGISTRY_INVALID)

    def test_the_registry_view_names_the_key_environment_and_never_a_value(self):
        with patch.dict(os.environ, {"OLLAMA_API_KEY": FAKE_KEY}, clear=False):
            rendered = json.dumps(WIDE.view())
        self.assertIn("OLLAMA_API_KEY", rendered)
        self.assertNotIn(FAKE_KEY, rendered)

    def test_an_unknown_endpoint_name_is_refused_by_the_registry(self):
        with self.assertRaises(SeatsRefused) as caught:
            WIDE["no-such-endpoint"]
        self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")


class TheAssignmentIsDeterministic(unittest.TestCase):
    """Acceptance: selection is a pure byte-stable function of (registry, config)."""

    def test_clause_two_independent_calls_give_the_same_seats(self):
        first, second = select_seats(WIDE), select_seats(WIDE)
        self.assertEqual(first, second)
        self.assertEqual(first.canonical_bytes(), second.canonical_bytes())

    def test_clause_selection_is_stable_across_a_registry_reload(self):
        first = select_seats(load_registry())
        second = select_seats(load_registry())
        self.assertIsNot(load_registry(), load_registry())
        self.assertEqual(first.pins(), second.pins())
        self.assertEqual(first.digest, second.digest)

    def test_clause_the_rule_is_sorted_family_then_sorted_endpoint_name(self):
        """Sorted family label, then sorted endpoint name - and, since wave-1
        integration decision 3, the first endpoint of each distinct *lineage*
        in that order.  ``deepseek`` and ``ollama-cloud/deepseek`` are two
        routes to one lineage, so the second is passed over once the first is
        seated rather than seating deepseek on both judge seats.
        """

        plan = select_seats(load_registry())
        loaded = load_registry()
        wanted: list = []
        seen: set[str] = set()
        for endpoint in loaded:              # already in (family, name) order
            if lineage(endpoint.family) in seen:
                continue
            seen.add(lineage(endpoint.family))
            wanted.append(endpoint)
        for index, seat in enumerate(plan.judges):
            with self.subTest(judge=index):
                self.assertEqual(seat.family, wanted[index].family)
                self.assertEqual(seat.name, wanted[index].name)
                self.assertEqual(seat.name, sorted(e.name for e in
                                                   loaded.in_family(seat.family))[0])

    def test_the_input_order_of_the_registry_does_not_change_the_seats(self):
        shuffled = Registry.of(list(reversed(WIDE.endpoints)))
        self.assertEqual(select_seats(WIDE).pins(), select_seats(shuffled).pins())

    def test_a_mapping_registry_and_a_registry_object_agree(self):
        as_map = {e.name: e for e in WIDE.endpoints}
        self.assertEqual(select_seats(as_map).pins(), select_seats(WIDE).pins())

    def test_selection_mutates_neither_the_registry_nor_the_config(self):
        config = SeatsConfig(critic="e3")
        before = tuple(WIDE.endpoints)
        select_seats(WIDE, config)
        self.assertEqual(tuple(WIDE.endpoints), before)
        self.assertEqual(config, SeatsConfig(critic="e3"))


class TheJudgeSeatsAreCrossFamily(unittest.TestCase):
    """Acceptance: two judge seats always carry distinct family labels - and,
    after wave-1 integration decision 3, distinct model *lineages*."""

    def test_the_lineage_of_a_label_is_the_label_with_its_host_route_stripped(self):
        self.assertEqual(lineage("ollama-cloud/deepseek"), "deepseek")
        self.assertEqual(lineage("deepseek"), "deepseek")
        self.assertEqual(lineage("ollama-cloud/gpt-oss"), "gpt-oss")
        # A trailing separator names no lineage of its own, so the label stands.
        self.assertEqual(lineage("vendor/"), "vendor/")
        self.assertEqual(lineage(""), "")

    def test_clause_the_default_table_never_seats_one_lineage_twice_on_the_judges(self):
        """The shipped registry labels deepseek twice - once directly and once
        through ollama-cloud - and sorted family order puts the two labels
        adjacent, so a family-label comparison would have seated one model on
        both judge seats.  G0 is about independent occasions, so the comparison
        is over the lineage.
        """

        loaded = load_registry()
        self.assertIn("deepseek", loaded.families)
        self.assertIn("ollama-cloud/deepseek", loaded.families)
        plan = select_seats(loaded)
        self.assertEqual(len(set(plan.judge_lineages)), len(plan.judges))
        self.assertEqual(len(set(plan.judge_families)), len(plan.judges))
        # ... and the table publishes both, so a reader of plan.json sees the
        # label that was assigned and the value that was compared.
        self.assertEqual(plan.pins()["judge_lineages"], list(plan.judge_lineages))
        self.assertEqual(plan.pins()["judge_families"], list(plan.judge_families))
        # The critic and the defender are outside every judge lineage too; the
        # variator is not, and is not meant to be - section 2.2 constrains its
        # family to *any*, and the default plan seats it on the first endpoint
        # left, which here shares the deepseek lineage with a judge.
        self.assertNotIn(plan.critic.lineage, set(plan.judge_lineages))
        self.assertNotIn(plan.defender.lineage, set(plan.judge_lineages))
        self.assertNotEqual(plan.defender.lineage, plan.critic.lineage)
        self.assertEqual(plan.relaxations, ())

    def test_two_labels_over_one_lineage_cannot_take_both_judge_seats(self):
        two_routes = registry(("a1", "vendor/alpha"), ("a2", "alpha"),
                              ("b1", "vendor/beta"), ("c1", "gamma"),
                              ("d1", "delta"))
        plan = select_seats(two_routes)
        self.assertEqual(len(set(plan.judge_lineages)), 2)
        config = SeatsConfig(judges=("a1", "a2"))
        with self.assertRaises(SeatsRefused) as caught:
            select_seats(two_routes, config)
        self.assertEqual(caught.exception.code, FAMILY_COUNT_INSUFFICIENT)

    def test_require_cross_family_judges_refuses_two_labels_of_one_lineage(self):
        pinned = select_seats(load_registry()).pins()
        pinned["judge_families"] = ["deepseek", "ollama-cloud/deepseek"]
        with self.assertRaises(SeatsRefused) as caught:
            require_cross_family_judges(pinned)
        self.assertEqual(caught.exception.code, FAMILY_COUNT_INSUFFICIENT)
        self.assertIn("lineage", caught.exception.detail)

    def test_clause_two_judge_seats_carry_distinct_family_labels(self):
        for source in (WIDE, NARROW, load_registry()):
            with self.subTest(registry=len(source)):
                plan = select_seats(source)
                self.assertEqual(len(plan.judges), 2)
                self.assertEqual(len(set(plan.judge_families)), 2)

    def test_clause_a_one_family_registry_raises_family_count_insufficient(self):
        one = registry(("a1", "A"), ("a2", "A"), ("a3", "A"),
                       ("a4", "A"), ("a5", "A"))
        with self.assertRaises(SeatsRefused) as caught:
            select_seats(one)
        self.assertEqual(caught.exception.code, FAMILY_COUNT_INSUFFICIENT)

    def test_the_refusal_never_degrades_to_two_judges_of_one_family(self):
        one = registry(("a1", "A"), ("a2", "A"), ("a3", "A"))
        with self.assertRaises(SeatsRefused):
            select_seats(one)

    def test_three_judge_seats_need_three_families(self):
        config = SeatsConfig(min_judge_families=3)
        two = registry(("a1", "A"), ("a2", "A"), ("b1", "B"), ("b2", "B"))
        with self.assertRaises(SeatsRefused) as caught:
            select_seats(two, config)
        self.assertEqual(caught.exception.code, FAMILY_COUNT_INSUFFICIENT)
        plan = select_seats(WIDE, config)
        self.assertEqual(len(plan.judges), 3)
        self.assertEqual(len(set(plan.judge_families)), 3)

    def test_a_config_pinning_two_judges_of_one_family_is_refused(self):
        config = SeatsConfig(judges=("a1", "a2"))
        with self.assertRaises(SeatsRefused) as caught:
            select_seats(NARROW, config)
        self.assertEqual(caught.exception.code, FAMILY_COUNT_INSUFFICIENT)

    def test_require_cross_family_judges_reads_a_plan_a_mapping_or_a_plan_body(self):
        plan = select_seats(WIDE)
        pinned = plan.pins()
        for shape in (plan, pinned, {"seats": pinned}):
            with self.subTest(shape=type(shape).__name__):
                self.assertEqual(require_cross_family_judges(shape),
                                 plan.judge_families)

    def test_require_cross_family_judges_refuses_a_repeated_family(self):
        pinned = select_seats(WIDE).pins()
        pinned["judge_families"] = ["F1", "F1"]
        with self.assertRaises(SeatsRefused) as caught:
            require_cross_family_judges(pinned)
        self.assertEqual(caught.exception.code, FAMILY_COUNT_INSUFFICIENT)

    def test_require_cross_family_judges_refuses_a_single_judge_seat(self):
        with self.assertRaises(SeatsRefused) as caught:
            require_cross_family_judges({"judge_families": ["F1"]})
        self.assertEqual(caught.exception.code, FAMILY_COUNT_INSUFFICIENT)

    def test_require_cross_family_judges_refuses_a_plan_with_no_judge_seats(self):
        with self.assertRaises(SeatsRefused) as caught:
            require_cross_family_judges({"seats": {}})
        self.assertEqual(caught.exception.code, "CONFIG_MISSING_KEY")


class TheOtherSeatsFollowTheFamilyRules(unittest.TestCase):

    def test_the_critic_is_outside_every_judge_family_where_the_registry_allows(self):
        plan = select_seats(WIDE)
        self.assertNotIn(plan.critic.family, plan.judge_families)

    def test_the_defender_is_outside_the_critics_family_where_allowed(self):
        plan = select_seats(WIDE)
        self.assertNotEqual(plan.defender.family, plan.critic.family)
        self.assertNotIn(plan.defender.family, plan.judge_families)

    def test_every_seat_is_a_distinct_endpoint(self):
        plan = select_seats(load_registry())
        names = [seat.name for seat in plan.seats]
        self.assertEqual(len(set(names)), len(names))

    def test_a_narrow_registry_records_what_it_could_not_satisfy(self):
        plan = select_seats(NARROW)
        self.assertTrue(plan.relaxations)
        constraints = {(r.seat, r.constraint) for r in plan.relaxations}
        self.assertIn(("critic", "family-distinct-from-every-judge"), constraints)
        for relaxation in plan.relaxations:
            self.assertTrue(relaxation.reason)
        self.assertEqual(plan.pins()["relaxations"],
                         [r.as_dict() for r in plan.relaxations])

    def test_a_wide_registry_records_no_relaxation_at_all(self):
        self.assertEqual(select_seats(WIDE).relaxations, ())
        self.assertEqual(select_seats(load_registry()).relaxations, ())

    def test_a_registry_with_fewer_endpoints_than_seats_is_refused_by_name(self):
        thin = registry(("a1", "A"), ("b1", "B"))
        with self.assertRaises(SeatsRefused) as caught:
            select_seats(thin)
        self.assertEqual(caught.exception.code, SEAT_COUNT_INSUFFICIENT)

    def test_the_variator_takes_any_family_and_is_merely_the_next_free_endpoint(self):
        plan = select_seats(load_registry())
        seated = {seat.name for seat in plan.seats} - {plan.variator.name}
        first_free = next(e for e in load_registry() if e.name not in seated)
        self.assertEqual(plan.variator.name, first_free.name)


class AConfigPinsASeat(unittest.TestCase):
    """Acceptance clause of the brief: a config that names a seat pins it."""

    def test_clause_a_named_critic_is_the_critic(self):
        plan = select_seats(WIDE, SeatsConfig(critic="e5"))
        self.assertEqual(plan.critic.name, "e5")

    def test_clause_every_named_seat_is_honoured_at_once(self):
        config = SeatsConfig(critic="e5", defender="e6", variator="e4",
                             judges=("e2", "e3"))
        plan = select_seats(WIDE, config)
        self.assertEqual(plan.critic.name, "e5")
        self.assertEqual(plan.defender.name, "e6")
        self.assertEqual(plan.variator.name, "e4")
        self.assertEqual([seat.name for seat in plan.judges], ["e2", "e3"])

    def test_the_unnamed_seats_are_assigned_around_the_named_ones(self):
        plan = select_seats(WIDE, SeatsConfig(critic="e1"))
        self.assertEqual(plan.critic.name, "e1")
        self.assertNotIn("e1", [seat.name for seat in plan.judges])
        self.assertEqual(len(set(seat.name for seat in plan.seats)), 5)

    def test_a_named_seat_the_registry_does_not_carry_is_refused(self):
        with self.assertRaises(SeatsRefused) as caught:
            select_seats(WIDE, SeatsConfig(critic="absent"))
        self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")

    def test_one_endpoint_may_not_hold_two_seats(self):
        with self.assertRaises(SeatsRefused) as caught:
            select_seats(WIDE, SeatsConfig(critic="e1", defender="e1"))
        self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")

    def test_a_pinned_critic_inside_a_judge_family_is_recorded_not_refused(self):
        config = SeatsConfig(critic="a2", judges=("a1", "b1"))
        plan = select_seats(NARROW, config)
        self.assertEqual(plan.critic.name, "a2")
        self.assertIn(("critic", "family-distinct-from-every-judge"),
                      {(r.seat, r.constraint) for r in plan.relaxations})

    def test_a_loop_config_a_seats_config_and_a_mapping_agree(self):
        mapping = {"critic": "e5", "judges": ["e2", "e3"]}
        by_mapping = select_seats(WIDE, mapping)
        by_dataclass = select_seats(WIDE, SeatsConfig(critic="e5",
                                                      judges=("e2", "e3")))
        self.assertEqual(by_mapping.pins(), by_dataclass.pins())
        loop_config = {"seats": mapping, "max_per_key": 5}
        self.assertEqual(select_seats(WIDE, loop_config).pins(), by_mapping.pins())

    def test_a_loop_config_object_carries_its_own_seats_and_max_per_key(self):
        config = LoopConfig.from_mapping(CONFIG)
        plan = select_seats(load_registry(), config)
        self.assertEqual(plan.max_per_key, config.max_per_key)
        self.assertEqual(plan.critic.name, "deepseek-v4-pro")

    def test_a_config_of_no_recognised_shape_is_refused(self):
        with self.assertRaises(SeatsRefused) as caught:
            select_seats(WIDE, ["e1"])
        self.assertEqual(caught.exception.code, "CONFIG_NOT_A_MAPPING")


CONFIG = {
    "schema": "minireason.loop.config.v1",
    "run_id": "LOOP-SEATS",
    "study": "h005",
    "occurrences": ["experiments/h005/occurrence-01"],
    "runner": "tools/multicycle_commitment_study_multi_v2.py",
    "cycle_budget": 3,
    "max_calls": 240,
    "reading_set": ["row-1"],
    "obligations_path": "experiments/loops/obligations.json",
    "graph_root": "experiments/loops/LOOP-SEATS/graph",
    "reopen_reasons": ["new-material"],
    # Wave-0 review S6: each audit margin carries the account that justifies it,
    # so the threshold is inside loop_plan_id and is attackable rather than bare.
    "audit": {
        "period": 2,
        "judge_err_max": 0.2,
        "judge_err_max_account": (
            "One anchor of the five-anchor calibration set: this fixture declines "
            "to read on the first anchor a seat gets wrong."
        ),
        "streak_max": 3,
        "streak_max_account": (
            "Three consecutive guard blocks is longer than any run of blocks this "
            "fixture's registry produces, so it names the instrument, not a row."
        ),
    },
    "seats": {"critic": "deepseek-v4-pro"},
    "max_per_key": 4,
}


class ThePinnedTableIsCanonical(unittest.TestCase):
    """Acceptance: the pinned seat table is canonical JSON under a sha256."""

    #: The default table's digest over the shipped registry, pinned as a
    #: literal so that a silent change to the assignment, to the registry, or
    #: to the table's own shape is visible in a diff rather than only in a
    #: rerun.  It **moved at the wave-1 integration** (decision 3): the judge
    #: pair became deepseek-flash + ollama/gemma4-31b rather than
    #: deepseek-flash + ollama/deepseek-v4.1-flash, because the two deepseek
    #: family labels are one lineage, and the table gained ``judge_lineages``.
    #:
    #:   before  10b34e4438d97c7b2e7d35bb89d83c822aee746f2b770217fabcf071c0877e95
    #:   after   2fe7829302ef88a3e239f0550a93d4a047996b394757b849b853034ed3994ed7
    #:
    #: A run pre-registered under the old digest is a different ``loop_plan_id``
    #: and a new pre-registration, never an amendment (design 5).
    DEFAULT_DIGEST = "2fe7829302ef88a3e239f0550a93d4a047996b394757b849b853034ed3994ed7"

    def setUp(self) -> None:
        self.plan = select_seats(load_registry())

    def test_the_default_table_digest_is_the_pinned_one(self):
        self.assertEqual(self.plan.digest, self.DEFAULT_DIGEST)
        self.assertEqual(self.plan.pins()["sha256"], self.DEFAULT_DIGEST)

    def test_clause_the_table_is_canonical_json(self):
        body = self.plan.table()
        expected = json.dumps(body, sort_keys=True, separators=(",", ":"),
                              ensure_ascii=False).encode()
        self.assertEqual(self.plan.canonical_bytes(), expected)

    def test_clause_the_sha256_covers_the_body_without_itself(self):
        pinned = self.plan.pins()
        digest = pinned.pop("sha256")
        self.assertEqual(digest, hashlib.sha256(
            json.dumps(pinned, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False).encode()).hexdigest())
        self.assertEqual(digest, self.plan.digest)

    def test_the_table_round_trips_through_json_unchanged(self):
        pinned = self.plan.pins()
        self.assertEqual(json.loads(json.dumps(pinned)), pinned)

    def test_the_table_declares_its_schema_and_its_rule(self):
        pinned = self.plan.pins()
        self.assertEqual(pinned["schema"], SEATS_SCHEMA)
        self.assertIn("sorted", pinned["rule"])

    def test_clause_the_pins_record_key_env_per_seat(self):
        pinned = self.plan.pins()
        recorded = [pinned["seats"]["critic"], pinned["seats"]["defender"],
                    pinned["seats"]["variator"], *pinned["seats"]["judge"]]
        for identity in recorded:
            with self.subTest(seat=identity["name"]):
                self.assertTrue(identity["key_env"])
                self.assertEqual(identity["key_env"],
                                 load_registry()[identity["name"]].key_env)
        seated = sorted({identity["key_env"] for identity in recorded})
        self.assertEqual(sorted(pinned["key_envs"]), seated)
        self.assertEqual(sorted(pinned["key_caps"]), seated)

    def test_seat_identity_is_name_model_family_key_env_and_the_two_limits(self):
        self.assertEqual(sorted(self.plan.critic.identity()),
                         ["family", "key_env", "max_concurrency", "model",
                          "name", "timeout_seconds"])

    def test_clause_substituting_an_endpoint_mints_a_new_plan(self):
        other = select_seats(load_registry(), SeatsConfig(critic="ollama/kimi-k3"))
        self.assertNotEqual(other.digest, self.plan.digest)

    def test_changing_a_seats_model_or_timeout_mints_a_new_plan(self):
        base = select_seats(WIDE)
        for change in ({"model": "other-model"}, {"timeout_seconds": 90},
                       {"max_concurrency": 2}, {"family": "F9"}):
            with self.subTest(change=change):
                swapped = [e for e in WIDE.endpoints if e.name != "e1"]
                first = [e for e in WIDE.endpoints if e.name == "e1"][0]
                fields = {"name": first.name, "base_url": first.base_url,
                          "model": first.model, "key_env": first.key_env,
                          "family": first.family,
                          "max_concurrency": first.max_concurrency,
                          "timeout_seconds": first.timeout_seconds}
                fields.update(change)
                altered = Registry.of(swapped + [Endpoint(**fields)])
                self.assertNotEqual(select_seats(altered).digest, base.digest)

    def test_the_marker_reuses_the_judge_pair_and_mints_no_seat_of_its_own(self):
        self.assertEqual(self.plan.marker_seats(), self.plan.judges)
        self.assertEqual(self.plan.pins()["reused_roles"], {"marker": "judge"})
        self.assertNotIn("marker", self.plan.pins()["seats"])
        self.assertIs(self.plan.for_role("marker", 1), self.plan.judges[1])

    def test_the_seated_roles_are_the_contract_roles_less_the_marker(self):
        self.assertEqual(set(SEAT_ROLES), set(ROLE_NAMES) - {"marker"})

    def test_for_role_refuses_a_role_the_plan_does_not_seat(self):
        for role, index in (("decider", 0), ("judge", 9), ("critic", 1)):
            with self.subTest(role=role), self.assertRaises(SeatsRefused) as caught:
                self.plan.for_role(role, index)
            self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")

    def test_the_record_form_carries_every_seat_and_its_pins(self):
        record = self.plan.as_dict()
        self.assertEqual(len(record["seats"]), 5)
        self.assertEqual(record["pins"], self.plan.pins())


class NoCredentialCanReachTheTable(unittest.TestCase):

    def test_the_table_names_the_key_environment_and_never_a_key_value(self):
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": FAKE_KEY,
                                     "OLLAMA_API_KEY": FAKE_KEY}, clear=False):
            rendered = select_seats(load_registry()).canonical_bytes().decode()
        self.assertIn("DEEPSEEK_API_KEY", rendered)
        self.assertNotIn(FAKE_KEY, rendered)

    def test_the_module_never_reads_the_environment_at_all(self):
        self.assertNotIn("os.environ", SOURCE)
        self.assertNotIn("getenv", SOURCE)
        self.assertNotIn("import os", SOURCE)


class TheKeyGateIsImportedNotReimplemented(unittest.TestCase):
    """Acceptance: the gate is runner v2's ``key_gate``, and holds five."""

    def setUp(self) -> None:
        runner._reset_gates()
        self.addCleanup(runner._reset_gates)
        self.plan = select_seats(load_registry())

    def test_clause_the_gate_is_runner_v2s_own_key_gate(self):
        self.assertIs(runner_module(), runner)
        seat = self.plan.judges[0]
        self.assertIs(key_gate_for(seat), runner.key_gate(seat.key_env, MAX_PER_KEY))

    def test_clause_the_module_reimplements_no_semaphore_of_its_own(self):
        self.assertNotIn("BoundedSemaphore(", SOURCE)
        self.assertNotIn("Semaphore(", SOURCE)

    def test_clause_a_sixth_concurrent_call_per_key_env_is_never_admitted(self):
        seat = self.plan.judges[0]
        gate = key_gate_for(seat)
        held = [gate.acquire(blocking=False) for _ in range(MAX_PER_KEY)]
        self.addCleanup(lambda: [gate.release() for _ in held if _])
        self.assertEqual(held, [True] * MAX_PER_KEY)
        self.assertFalse(gate.acquire(blocking=False))

    def test_two_seats_on_one_credential_share_one_gate(self):
        on_ollama = [seat for seat in self.plan.seats
                     if seat.key_env == "OLLAMA_API_KEY"]
        self.assertGreater(len(on_ollama), 1)
        gates = {id(key_gate_for(seat)) for seat in on_ollama}
        self.assertEqual(len(gates), 1)

    def test_seats_on_two_credentials_do_not_share_a_gate(self):
        by_key = {seat.key_env: key_gate_for(seat) for seat in self.plan.seats}
        self.assertEqual(len(by_key), 2)
        self.assertIsNot(by_key["OLLAMA_API_KEY"], by_key["DEEPSEEK_API_KEY"])

    def test_the_cap_is_the_lowest_of_five_the_config_and_the_endpoint(self):
        seat = self.plan.judges[0]
        self.assertEqual(key_cap_for(seat), MAX_PER_KEY)
        self.assertEqual(key_cap_for(seat, 2), 2)
        narrow = Seat("judge", 0, endpoint("n1", "N", max_concurrency=1))
        self.assertEqual(key_cap_for(narrow), 1)

    def test_a_cap_outside_one_to_five_is_refused(self):
        seat = self.plan.judges[0]
        for bad in (0, 6, 5.0, "5", True):
            with self.subTest(bad=bad), self.assertRaises(SeatsRefused) as caught:
                key_cap_for(seat, bad)
            self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")

    def test_two_caps_on_one_credential_are_a_conflict_not_a_widening(self):
        seat = self.plan.judges[0]
        key_gate_for(seat, 5)
        with self.assertRaises(SeatsRefused) as caught:
            key_gate_for(seat, 3)
        self.assertEqual(caught.exception.code, "CONCURRENCY_LIMIT_CONFLICT")

    def test_the_plan_records_the_cap_in_force_for_every_credential(self):
        plan = select_seats(load_registry(), {"max_per_key": 3})
        self.assertEqual(plan.max_per_key, 3)
        self.assertEqual(set(plan.key_caps().values()), {3})
        self.assertEqual(plan.pins()["key_caps"], plan.key_caps())

    def test_a_max_per_key_outside_one_to_five_is_refused(self):
        with self.assertRaises(SeatsRefused) as caught:
            select_seats(load_registry(), {"max_per_key": 6})
        self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")

    def test_this_module_mirrors_runner_v2s_own_authorisation(self):
        self.assertEqual(MAX_PER_KEY, runner.MAX_PER_KEY)


class NothingOrdersEndpointsByMerit(unittest.TestCase):
    """Seats are occasions, not contestants: no ordering but name and family."""

    BANNED = re.compile(
        r"(?:^|(?<=[^A-Za-z]))"
        r"(score|scores|scored|scoring|rank|ranks|ranked|ranking|best|top)"
        r"(?:$|(?=[^A-Za-z]))", re.IGNORECASE)

    def test_clause_the_source_carries_no_score_rank_best_or_top_token(self):
        offending = [(n, line) for n, line in enumerate(SOURCE.splitlines(), 1)
                     if self.BANNED.search(line)]
        self.assertEqual(offending, [])

    def test_clause_no_identifier_in_the_module_carries_one_either(self):
        tree = ast.parse(SOURCE)
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.add(node.name)
                names.update(a.arg for a in getattr(node, "args", ast.arguments(
                    posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                    defaults=[])).args)
            elif isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.Attribute):
                names.add(node.attr)
        offending = sorted(n for n in names
                           for part in re.split(r"[^A-Za-z]+", n)
                           if part and self.BANNED.fullmatch(part))
        self.assertEqual(offending, [])

    def test_the_only_sort_keys_are_a_family_label_and_an_endpoint_name(self):
        tree = ast.parse(SOURCE)
        keys: list[str] = []
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "sorted"):
                keys.extend(ast.unparse(kw.value) for kw in node.keywords
                            if kw.arg == "key")
        for key in keys:
            with self.subTest(key=key):
                self.assertRegex(key, r"e\.family|e\.name")

    def test_seats_carry_no_ordering_of_their_own(self):
        plan = select_seats(WIDE)
        with self.assertRaises(TypeError):
            plan.critic < plan.defender          # noqa: B015
        with self.assertRaises(TypeError):
            sorted(plan.seats)

    def test_no_record_in_the_module_defines_a_comparison(self):
        for record in (Seat, SeatPlan, Registry, S.Relaxation):
            for method in ("__lt__", "__gt__", "__le__", "__ge__"):
                with self.subTest(record=record.__name__, method=method):
                    self.assertIsNone(record.__dict__.get(method))

    def test_no_dataclass_in_the_module_asks_for_an_order(self):
        tree = ast.parse(SOURCE)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    for keyword in decorator.keywords:
                        with self.subTest(record=node.name, keyword=keyword.arg):
                            self.assertNotEqual(keyword.arg, "order")


class TheModuleIsWellFormed(unittest.TestCase):

    def test_every_public_name_is_exported_and_present(self):
        for name in S.__all__:
            with self.subTest(name=name):
                self.assertTrue(hasattr(S, name), f"__all__ names absent {name}")
        defined: set[str] = set()
        for node in ast.parse(SOURCE).body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                defined.add(node.name)
            elif isinstance(node, ast.Assign):
                defined.update(t.id for t in node.targets
                               if isinstance(t, ast.Name))
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                defined.add(node.target.id)
        public = {name for name in defined if not name.startswith("_")}
        self.assertEqual(sorted(public - set(S.__all__)), [],
                         "every name this module defines is exported or private")

    def test_the_docstring_states_purpose_design_section_and_deviations(self):
        doc = S.__doc__ or ""
        for heading in ("Purpose", "Design section", "Deviations"):
            with self.subTest(heading=heading):
                self.assertIn(heading, doc)
        self.assertIn("2.2", doc)
        self.assertIn("4.6", doc)

    def test_every_failure_is_a_loop_error_carrying_an_upper_snake_code(self):
        error = SeatsRefused(FAMILY_COUNT_INSUFFICIENT, "detail")
        self.assertIsInstance(error, LoopError)
        self.assertEqual(error.code, FAMILY_COUNT_INSUFFICIENT)
        self.assertEqual(error.detail, "detail")

    def test_the_declared_code_is_in_the_wave_zero_table(self):
        self.assertIn(FAMILY_COUNT_INSUFFICIENT, FAILURE_CODES)

    def test_new_codes_are_declared_with_a_reason_and_are_folded_into_the_table(self):
        """The wave-1 integrator folded these three in (O9); each still carries
        its reason here, which is what the table's comment points back at."""

        self.assertEqual(set(NEW_CODES), {SEAT_COUNT_INSUFFICIENT, REGISTRY_INVALID,
                                          RUNNER_NOT_IMPORTABLE})
        for code, reason in NEW_CODES.items():
            with self.subTest(code=code):
                self.assertRegex(code, r"\A[A-Z][A-Z0-9_]*\Z")
                self.assertTrue(reason.strip())
                self.assertIn(code, FAILURE_CODES)

    def test_every_code_the_module_can_raise_is_declared_somewhere(self):
        declared = set(FAILURE_CODES) | set(NEW_CODES)
        tree = ast.parse(SOURCE)
        raised = {node.args[0].value
                  for node in ast.walk(tree)
                  if isinstance(node, ast.Call)
                  and isinstance(node.func, ast.Name) and node.func.id == "_fail"
                  and node.args and isinstance(node.args[0], ast.Constant)
                  and isinstance(node.args[0].value, str)}
        self.assertTrue(raised)
        self.assertEqual(sorted(raised - declared), [])

    def test_the_module_imports_no_loop_sibling_but_types_and_contracts(self):
        siblings = set()
        for node in ast.walk(ast.parse(SOURCE)):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                siblings.add(node.module)
        self.assertEqual(siblings, {"types", "contracts"})

    def test_importing_the_module_opens_no_socket_and_reads_only_the_registry(self):
        self.assertNotIn("urllib", SOURCE)
        self.assertNotIn("socket", SOURCE)
        self.assertNotIn("requests", SOURCE)

    def test_a_seat_refuses_a_role_it_may_not_hold(self):
        with self.assertRaises(SeatsRefused) as caught:
            Seat("decider", 0, endpoint("x", "X"))
        self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")

    def test_a_seat_refuses_a_negative_index(self):
        with self.assertRaises(SeatsRefused):
            Seat("judge", -1, endpoint("x", "X"))

    def test_a_seat_label_names_the_role_and_the_judge_index(self):
        plan = select_seats(WIDE)
        self.assertEqual(plan.critic.label, "critic")
        self.assertEqual([seat.label for seat in plan.judges],
                         ["judge#1", "judge#2"])

    def test_a_seat_reads_its_identity_off_the_endpoint_it_holds(self):
        one = endpoint("x", "X", model="m", timeout_seconds=42)
        seat = Seat("critic", 0, one)
        self.assertEqual((seat.name, seat.model, seat.family, seat.key_env,
                          seat.timeout_seconds, seat.max_concurrency, seat.native),
                         (one.name, one.model, one.family, one.key_env,
                          one.timeout_seconds, one.max_concurrency, one.native))

    def test_a_seat_plan_and_a_seat_are_both_frozen(self):
        plan = select_seats(WIDE)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            plan.critic = plan.defender          # type: ignore[misc]
        with self.assertRaises(dataclasses.FrozenInstanceError):
            plan.critic.role = "defender"        # type: ignore[misc]

    def test_seats_on_refuses_a_credential_no_seat_spends(self):
        with self.assertRaises(SeatsRefused) as caught:
            select_seats(WIDE).seats_on("NO_SUCH_KEY")
        self.assertEqual(caught.exception.code, "CONFIG_INVALID_VALUE")

    def test_the_plan_is_a_seat_plan_of_five_seats_by_default(self):
        plan = select_seats(WIDE)
        self.assertIsInstance(plan, SeatPlan)
        self.assertEqual(len(plan.seats), 5)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
