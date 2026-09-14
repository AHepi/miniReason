"""Offline tests for W0-CONTRACTS (`src/minireason/loop/contracts.py`).

Every test of the first six classes is named after one clause of the module's
acceptance list in §7 of the automated-loop design of record:

  1. READING_VOCABULARY is imported from use_relation_h005.ROOT_READING_VOCABULARY,
     not retyped
  2. a scoring key nested anywhere raises SCORING_KEY_FORBIDDEN
  3. no ordering is defined on the vocabulary
  4. no aggregate field is expressible
  5. every malformed fixture raises SchemaInvalid naming its reason
  6. validators are pure

No provider is called, no credential is read, and nothing is written anywhere.
The two files this module must not drift from -- the C001 material's frozen
reading rule and the existing scoring-key guard -- are read as bytes and parsed,
never imported, so no test here has an import side effect on the rest of the
suite.
"""
from __future__ import annotations

import ast
import copy
import json
import unittest
from pathlib import Path
from typing import Any

from minireason import use_relation_h005
from minireason.loop import contracts as c
from minireason.loop import standard, types as loop_types

REPO = Path(__file__).resolve().parents[2]
CONTRACTS_PY = REPO / "src/minireason/loop/contracts.py"
CONTRAST_TOOL = REPO / "tools/contrast_triple_study.py"
C001_MATERIAL = REPO / "experiments/diagnostics/C001-contrast-triple/material.json"

CRITIC_OK: dict[str, Any] = {
    "relation": "qualifies",
    "passage_quote": "the objection's own words",
    "role_bindings": {"target": "z", "defect": "d", "grounds": "g", "bearing": "b"},
    "case": "The record takes up the objection and narrows it.",
    "outside_vocabulary": "",
}
DEFENDER_OK: dict[str, Any] = {"answer": "The juxtaposition shows no such thing.",
                               "concedes": False}
JUDGE_OK: dict[str, Any] = {"sustained": True, "decisive_point": "narrows it",
                            "reading_note": "The cited passage does the work."}
MARKER_OK: dict[str, Any] = {"mark": "differs", "difference_kind": "target_set_membership",
                             "left_quote": "o1", "right_quote": "c1", "case": "different sets"}
VARIATOR_OK: dict[str, Any] = {"paraphrases": ["first wording", "second wording"]}

WELL_FORMED: dict[str, dict[str, Any]] = {
    "critic": CRITIC_OK,
    "defender": DEFENDER_OK,
    "judge": JUDGE_OK,
    "marker": MARKER_OK,
    "variator": VARIATOR_OK,
}


def module_source() -> str:
    return CONTRACTS_PY.read_text(encoding="utf-8")


def tool_literal(name: str) -> Any:
    """The value of a module-level literal in the contrast tool, without importing it."""
    tree = ast.parse(CONTRAST_TOOL.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if name not in targets:
            continue
        value = node.value
        if (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
                and value.func.id == "frozenset"):
            return frozenset(ast.literal_eval(value.args[0]))
        return ast.literal_eval(value)
    raise AssertionError(f"{name} not found in {CONTRAST_TOOL}")


def reading_rule() -> dict[str, Any]:
    return json.loads(C001_MATERIAL.read_bytes())["reading_rule"]


def without(body: dict[str, Any], field: str) -> dict[str, Any]:
    out = copy.deepcopy(body)
    out.pop(field)
    return out


def replacing(body: dict[str, Any], **fields: Any) -> dict[str, Any]:
    out = copy.deepcopy(body)
    out.update(fields)
    return out


class ReadingVocabularyIsImportedNotRetyped(unittest.TestCase):
    """Acceptance: READING_VOCABULARY is imported, not retyped."""

    def test_reading_vocabulary_is_imported_from_use_relation_h005_not_retyped(self):
        self.assertIs(c.READING_VOCABULARY, use_relation_h005.ROOT_READING_VOCABULARY)
        self.assertIs(c.READING_BANNER, use_relation_h005.USE_RELATION_BANNER)

    def test_no_member_of_the_vocabulary_is_a_literal_in_the_module(self):
        # Not "equal to the published tuple" -- *never written down here*. Any
        # string constant anywhere in the module (docstrings included) that
        # equals a published relation would be a second source of truth.
        constants = {
            node.value for node in ast.walk(ast.parse(module_source()))
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        retyped = sorted(constants & set(use_relation_h005.ROOT_READING_VOCABULARY)
                         - {c.UNRESOLVED})
        self.assertEqual(retyped, [])

    def test_critic_relations_are_the_vocabulary_less_unresolved_plus_none(self):
        self.assertEqual(
            c.CRITIC_RELATIONS,
            ("re-deploys", "qualifies", "rejects-with-reason", "repairs", "retains",
             "none"),
        )
        self.assertNotIn(c.UNRESOLVED, c.CRITIC_RELATIONS)
        self.assertEqual(list(c.CRITIC_SCHEMA["properties"]["relation"]["enum"]),
                         list(c.CRITIC_RELATIONS))

    def test_the_banner_is_carried_verbatim(self):
        self.assertIn("The tool records juxtapositions; the reading is root's.",
                      c.READING_BANNER)
        self.assertIn("A lexical overlap is not evidence of use.",
                      c.READING_BANNER.replace("**", ""))
        self.assertNotIn(c.READING_BANNER, module_source())


class AScoringKeyNestedAnywhereRaises(unittest.TestCase):
    """Acceptance: a scoring key nested anywhere raises SCORING_KEY_FORBIDDEN."""

    def test_a_scoring_key_nested_anywhere_raises_scoring_key_forbidden(self):
        for key in sorted(c.FORBIDDEN_KEYS):
            for value in (
                {key: "x"},
                {"a": {"b": [{"c": {key: 1}}]}},
                [[{"deep": ({"also": {key: None}},)}]],
                {"outer": [1, 2, {"inner": {key: []}}]},
            ):
                with self.subTest(key=key, shape=type(value).__name__):
                    with self.assertRaises(c.ScoringKeyForbidden) as caught:
                        c.assert_no_scoring_keys(value)
                    self.assertEqual(str(caught.exception), "SCORING_KEY_FORBIDDEN")
                    self.assertEqual(caught.exception.code, "SCORING_KEY_FORBIDDEN")
                    self.assertEqual(caught.exception.path[-1], key)
                    self.assertIsInstance(caught.exception, ValueError)

    def test_an_upper_case_scoring_key_is_refused_too(self):
        with self.assertRaises(c.ScoringKeyForbidden):
            c.assert_no_scoring_keys({"results": [{"Rank": 1}]})

    def test_a_clean_value_passes_and_a_scoring_word_in_content_is_not_a_key(self):
        for value in (
            {},
            {"mark": "differs", "case": "the score of the match is not a key here"},
            [None, True, "rank", ("merit",)],
            WELL_FORMED,
        ):
            with self.subTest(value=value):
                self.assertIsNone(c.assert_no_scoring_keys(value))

    def test_the_forbidden_key_set_has_not_drifted_from_the_existing_guard(self):
        self.assertEqual(c.FORBIDDEN_KEYS, tool_literal("FORBIDDEN_KEYS"))

    def test_the_guard_refuses_the_vendored_warrants_own_verdict_field_name(self):
        """A collision W1-GRAPH must know about before it writes a warrant.

        ``deepreason_core/ontology/warrant.py`` names its demonstrative field
        ``verdict``, and design D2 gives the reading warrant ``verdict: "fail"``.
        ``verdict`` is also a member of the contrast tool's FORBIDDEN_KEYS,
        which this guard mirrors and may not narrow: narrowing it would let a
        genuine scoring key through every other study that shares the set.

        So the two are and stay incompatible, and the boundary is the guard's
        SUBJECT: G12 scans "every emitted artifact, every table header and every
        rendered file" -- the artifact CONTENT the loop builds -- and never the
        vendored ontology record that carries it. This test pins the collision
        so a later wave meets it here rather than at registration time.
        """
        with self.assertRaises(c.ScoringKeyForbidden) as caught:
            c.assert_no_scoring_keys({
                "type": "DEMONSTRATIVE", "target": "C_open",
                "commitment": "rubric:reading-v1", "verdict": "fail",
                "trace_ref": "blob:...", "validity_node": "nu_soundness"})
        self.assertEqual(caught.exception.path, ("verdict",))
        self.assertIn("verdict", c.FORBIDDEN_KEYS)
        self.assertIn("verdict", tool_literal("FORBIDDEN_KEYS"))
        # The reading artifact's own content carries no such field and passes.
        self.assertIsNone(c.assert_no_scoring_keys({
            "cell": "p1/n1#r3", "relation": "qualifies",
            "difference_kind": None, "seats": ["a", "b"], "guard": {"order_swap": "agreed"}}))

    def test_every_role_output_passes_the_guard(self):
        for role, body in WELL_FORMED.items():
            with self.subTest(role=role):
                value = c.validate(role, body)
                c.assert_no_scoring_keys(value.as_dict())


class NoOrderingIsDefinedOnTheVocabulary(unittest.TestCase):
    """Acceptance: no ordering is defined on the vocabulary."""

    def test_no_ordering_is_defined_on_the_vocabulary(self):
        # (a) Nothing in the module maps a vocabulary member to a number.
        vocabulary = set(c.READING_VOCABULARY) | set(c.CRITIC_RELATIONS) | set(c.MARKS)
        for name in dir(c):
            attribute = getattr(c, name)
            if isinstance(attribute, dict) or hasattr(attribute, "items"):
                try:
                    items = list(attribute.items())
                except (TypeError, AttributeError):
                    continue
                for key, value in items:
                    if isinstance(key, str) and key in vocabulary:
                        self.assertNotIsInstance(
                            value, (int, float),
                            f"{name}[{key!r}] gives a vocabulary member a number")
        # (b) The module exports no ordering, ranking or precedence helper.
        for name in c.__all__:
            self.assertNotRegex(
                name.lower(),
                r"rank|order|sort|precede|precedence|severity|priority|degree",
                f"{name} names an ordering")
        # (c) The module invents no order: the critic enum is the published
        #     order, minus unresolved, plus none, and nothing else is ordered.
        published = [v for v in use_relation_h005.ROOT_READING_VOCABULARY
                     if v != c.UNRESOLVED]
        self.assertEqual(list(c.CRITIC_RELATIONS)[:-1], published)

    def test_the_registers_and_marks_match_the_frozen_c001_reading_rule(self):
        rule = reading_rule()
        self.assertEqual(list(c.REGISTERS), [r["id"] for r in rule["registers"]])
        self.assertEqual(list(c.MARKS), list(rule["marks"]))

    def test_the_difference_kind_token_set_is_closed_per_register(self):
        self.assertEqual(sorted(c.DIFFERENCE_KINDS), sorted(c.REGISTERS))
        for register in c.REGISTERS:
            tokens = c.difference_kinds_for(register)
            self.assertIsInstance(tokens, tuple)
            self.assertTrue(tokens)
            self.assertEqual(len(set(tokens)), len(tokens))
        with self.assertRaises(c.SchemaInvalid) as caught:
            c.difference_kinds_for("Z")
        self.assertEqual(caught.exception.reason, "unknown-register")

    def test_the_difference_kind_grain_is_finer_than_register_grain(self):
        # D4 rejects register-grain kinds as over-suppressing `differs`. This
        # module used to carry one token per register, which IS register grain;
        # the wave-0 integration deleted that set in favour of W0-STANDARD's.
        # A register whose kind set is a singleton makes G9's "kind grain"
        # coincide with register grain for that register, which PLAN 8a only
        # licenses for G (one axis, whose values already include "none").
        self.assertIs(c.DIFFERENCE_KINDS, standard.DIFFERENCE_KINDS)
        for register in ("T", "E", "D"):
            with self.subTest(register=register):
                self.assertGreater(len(c.DIFFERENCE_KINDS[register]), 1)
        self.assertEqual(len(c.DIFFERENCE_KINDS["G"]), 1)
        # Every token the design sketches survives, spelled identically.
        for register, token in (("T", "target_set_membership"),
                                ("E", "record_engaged"),
                                ("D", "disposition_value"),
                                ("G", "grounds_source")):
            with self.subTest(sketched=token):
                self.assertIn(token, c.DIFFERENCE_KINDS[register])
        # The marker schema is closed over exactly that set, and nothing else.
        self.assertEqual(
            [token for token in c.MARKER_SCHEMA["properties"]["difference_kind"]["enum"]
             if token is not None],
            list(c.ALL_DIFFERENCE_KINDS))
        self.assertEqual(set(c.ALL_DIFFERENCE_KINDS),
                         {token for tokens in standard.DIFFERENCE_KINDS.values()
                          for token in tokens})

    def test_no_mark_and_no_ruling_is_a_quantity(self):
        marker = c.validate("marker", MARKER_OK, register="T")
        self.assertIsInstance(marker.mark, str)
        judge = c.validate("judge", JUDGE_OK)
        self.assertIsInstance(judge.sustained, bool)


class NoAggregateFieldIsExpressible(unittest.TestCase):
    """Acceptance: no aggregate field is expressible."""

    def test_no_aggregate_field_is_expressible(self):
        for role, schema in c.SCHEMAS.items():
            with self.subTest(role=role):
                # Structural: closed objects, no numeric type, no aggregate name.
                self.assertIsNone(c.assert_no_aggregate_fields(schema))
                self.assertIs(schema["additionalProperties"], False)
                rendered = json.dumps(schema)
                self.assertNotIn('"number"', rendered)
                self.assertNotIn('"integer"', rendered)
                for name in schema["properties"]:
                    self.assertNotIn(name.lower(), c.FORBIDDEN_KEYS)
                    self.assertNotIn(name.lower(), c.AGGREGATE_KEYS)
                # Behavioural: an extra field is refused, so no caller can add one.
                for extra in ("count", "score", "confidence", "anything"):
                    invalid = replacing(WELL_FORMED[role], **{extra: "x"})
                    with self.assertRaises(c.SchemaInvalid) as caught:
                        c.validate(role, invalid)
                    self.assertEqual(caught.exception.reason, "unexpected-field")
                    self.assertEqual(caught.exception.path, (extra,))

    def test_the_aggregate_audit_catches_a_schema_that_could_express_one(self):
        for bad in (
            {"type": "object", "additionalProperties": False,
             "properties": {"count": {"type": "string"}}},
            {"type": "object", "additionalProperties": False,
             "properties": {"n": {"type": "integer"}}},
            {"type": "object", "properties": {"n": {"type": "string"}}},
            {"type": "object", "additionalProperties": False,
             "properties": {"items": {"type": "array",
                                      "items": {"type": "number"}}}},
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(c.ContractError):
                    c.assert_no_aggregate_fields(bad)

    def test_role_bindings_are_closed_too(self):
        nested = c.CRITIC_SCHEMA["properties"]["role_bindings"]
        self.assertIs(nested["additionalProperties"], False)
        self.assertEqual(list(nested["properties"]), list(c.ROLE_BINDING_FIELDS))
        invalid = replacing(CRITIC_OK,
                            role_bindings={**CRITIC_OK["role_bindings"], "rank": "1"})
        with self.assertRaises(c.SchemaInvalid) as caught:
            c.validate("critic", invalid)
        self.assertEqual(caught.exception.reason, "unexpected-field")


class EveryMalformedFixtureRaisesSchemaInvalid(unittest.TestCase):
    """Acceptance: every malformed fixture raises SchemaInvalid naming its reason."""

    FIXTURES: tuple[tuple[str, str, Any, dict[str, Any]], ...] = (
        ("unknown-role", "decider", {"stop": True}, {}),
        ("unknown-register", "marker", replacing(MARKER_OK, mark="same",
                                                 difference_kind=None), {"register": "Z"}),
        ("not-json", "critic", "{not json", {}),
        ("not-an-object", "critic", "[1, 2]", {}),
        ("missing-field", "critic", without(CRITIC_OK, "passage_quote"), {}),
        ("unexpected-field", "judge", replacing(JUDGE_OK, tally="2"), {}),
        ("wrong-type", "judge", replacing(JUDGE_OK, sustained=1), {}),
        ("not-in-enum", "critic", replacing(CRITIC_OK, relation="unresolved"), {}),
        ("empty-field", "defender", replacing(DEFENDER_OK, answer=""), {}),
        ("too-few-items", "variator", {"paraphrases": []}, {}),
        ("not-unique", "variator", {"paraphrases": ["same", "same"]}, {}),
        ("word-limit", "defender", replacing(DEFENDER_OK, answer="w " * 401), {}),
        ("case-required", "critic", replacing(CRITIC_OK, case=""), {}),
        ("passage-quote-required", "critic", replacing(CRITIC_OK, passage_quote=""), {}),
        ("difference-kind-required", "marker",
         replacing(MARKER_OK, difference_kind=None), {}),
        ("difference-kind-forbidden", "marker", replacing(MARKER_OK, mark="same"), {}),
        ("difference-kind-unknown", "marker",
         replacing(MARKER_OK, difference_kind="record_engaged"), {"register": "T"}),
        ("quote-required", "marker", replacing(MARKER_OK, left_quote=""),
         {"register": "T"}),
    )

    def test_every_malformed_fixture_raises_schema_invalid_naming_its_reason(self):
        for reason, role, raw, kwargs in self.FIXTURES:
            with self.subTest(reason=reason, role=role):
                with self.assertRaises(c.SchemaInvalid) as caught:
                    c.validate(role, raw, **kwargs)
                exception = caught.exception
                self.assertEqual(exception.reason, reason)
                self.assertEqual(exception.role, role)
                self.assertIn(reason, str(exception))
                self.assertIn(reason, c.SCHEMA_REASONS)
                self.assertIsInstance(exception, ValueError)
                self.assertIsInstance(exception, c.ContractError)

    def test_every_declared_reason_has_a_fixture(self):
        covered = {reason for reason, _role, _raw, _kwargs in self.FIXTURES}
        self.assertEqual(covered, set(c.SCHEMA_REASONS))

    def test_check_returns_the_same_failure_it_never_raises(self):
        for reason, role, raw, kwargs in self.FIXTURES:
            with self.subTest(reason=reason, role=role):
                result = c.check(role, raw, **kwargs)
                self.assertFalse(result.ok)
                self.assertIsNone(result.value)
                self.assertEqual(result.reason, reason)
                self.assertEqual(result.role, role)
                with self.assertRaises(c.SchemaInvalid):
                    result.raise_for_failure()

    def test_a_schema_invalid_output_is_a_block_not_a_repair(self):
        # G1/§2.3: the contract layer offers no repair and no default. There is
        # no coercion path: a failure carries no value at all.
        result = c.check("judge", replacing(JUDGE_OK, sustained="true"))
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)


class ValidatorsArePure(unittest.TestCase):
    """Acceptance: validators are pure."""

    def test_validators_are_pure(self):
        schemas_before = copy.deepcopy({k: v for k, v in c.SCHEMAS.items()})
        for role, body in WELL_FORMED.items():
            with self.subTest(role=role):
                raw = copy.deepcopy(body)
                first = c.check(role, raw)
                second = c.check(role, raw)
                self.assertTrue(first.ok)
                self.assertEqual(first, second)
                self.assertEqual(raw, body, "the input was mutated")
        for reason, role, raw, kwargs in EveryMalformedFixtureRaisesSchemaInvalid.FIXTURES:
            with self.subTest(reason=reason):
                snapshot = copy.deepcopy(raw)
                self.assertEqual(c.check(role, raw, **kwargs),
                                 c.check(role, raw, **kwargs))
                self.assertEqual(raw, snapshot, "the input was mutated")
        self.assertEqual(copy.deepcopy({k: v for k, v in c.SCHEMAS.items()}),
                         schemas_before, "a schema was mutated")

    def test_the_module_opens_nothing_and_imports_only_its_two_siblings(self):
        # W0-STANDARD reads its two shipped data files once, at import; no
        # callable here opens anything, and nothing else is reachable.
        allowed = {"__future__", "copy", "json", "dataclasses", "types", "typing",
                   "jsonschema", "minireason.loop.standard", "minireason.loop.types"}
        imported: set[str] = set()
        for node in ast.walk(ast.parse(module_source())):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        self.assertTrue(imported <= allowed, f"unexpected imports: {imported - allowed}")
        for forbidden in ("open(", "Path(", "os.environ", "subprocess", "read_text",
                          "read_bytes", "write_text", "write_bytes"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, module_source())

    def test_the_returned_values_are_frozen(self):
        value = c.validate("critic", CRITIC_OK)
        with self.assertRaises(Exception):
            value.relation = "retains"           # type: ignore[misc]
        with self.assertRaises(Exception):
            value.role_bindings.target = "x"     # type: ignore[misc]

    def test_schema_for_hands_back_a_copy_the_caller_may_edit(self):
        taken = c.schema_for("critic")
        self.assertEqual(taken, c.CRITIC_SCHEMA)
        self.assertIsNot(taken, c.CRITIC_SCHEMA)
        taken["properties"]["relation"]["enum"].append("anything")
        self.assertNotIn("anything", c.CRITIC_SCHEMA["properties"]["relation"]["enum"])
        with self.assertRaises(c.SchemaInvalid) as caught:
            c.schema_for("decider")
        self.assertEqual(caught.exception.reason, "unknown-role")


class WOneOwnerPerSharedConstant(unittest.TestCase):
    """Wave-0 integration decision 1: W0-STANDARD owns every shared vocabulary."""

    SHARED = (
        ("READING_VOCABULARY", "READING_VOCABULARY"),
        ("CRITIC_RELATIONS", "CRITIC_RELATIONS"),
        ("MARKS", "MARKS"),
        ("REGISTERS", "REGISTERS"),
        ("DIFFERENCE_KINDS", "DIFFERENCE_KINDS"),
        ("FORBIDDEN_KEYS", "FORBIDDEN_KEYS"),
        ("READING_BANNER", "READING_BANNER"),
        ("OUTSIDE_VOCABULARY_FIELD", "OUTSIDE_VOCABULARY_FIELD"),
        ("UNRESOLVED", "UNRESOLVED_TOKEN"),
        ("NONE_RELATION", "NONE_TOKEN"),
    )

    def test_every_shared_constant_is_the_standards_own_object(self):
        for here, there in self.SHARED:
            with self.subTest(constant=here):
                self.assertIs(getattr(c, here), getattr(standard, there),
                              f"contracts.{here} is not standard.{there}")

    def test_this_module_defines_none_of_them(self):
        # Not "equal to standard's" -- assigned from an import and nowhere else.
        tree = ast.parse(module_source())
        imported = {
            alias.asname or alias.name
            for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
            for alias in node.names
        }
        for here, _there in self.SHARED:
            if here in ("UNRESOLVED", "NONE_RELATION"):
                continue          # aliases: assigned from the imported name
            with self.subTest(constant=here):
                self.assertIn(here, imported,
                              f"{here} must be imported from W0-STANDARD, not defined here")

    #: Every cross-wave import the package actually makes, recorded because the
    #: wave plan's ``depends_on`` lists do not name all of them (wave-1
    #: integration decision 54): each wave-2 module reaches ``standard``, which
    #: is the one owner of the ceiling sentences and of the exhaustion scan, and
    #: ``markprep`` reaches W1-SURFACE for the one resolver. The graph stays
    #: acyclic, which is the property that matters, and this test asserts both.
    DECLARED_EDGES = {
        "types": set(),
        "standard": {"types"},
        "contracts": {"standard", "types"},
        "custody": {"types"},
        "receipts": {"types"},
        "publish": {"types"},
        "surface": {"contracts", "types"},
        "seats": {"contracts", "types"},
        "obligations": {"types"},
        "graph": {"contracts", "standard", "types"},
        "steps": {"custody", "publish", "receipts", "types"},
        "synthetic": {"contracts", "standard", "types"},
        "packs": {"contracts", "standard", "surface", "types"},
        "roles": {"contracts", "custody", "seats", "types"},
        "markprep": {"contracts", "custody", "standard", "surface", "types"},
        "decide": {"graph", "obligations", "standard", "types"},
    }

    @staticmethod
    def package_edges() -> dict:
        """module stem -> the siblings it imports, absolute AND relative.

        Reading only ``minireason.loop.<x>`` missed every ``from .types import``
        - which is how ten of the sixteen modules import their siblings - so the
        walk below used to run over a graph with most of its edges absent.
        """

        package = Path(c.__file__).resolve().parent
        edges: dict[str, set[str]] = {}
        for source in sorted(package.glob("*.py")):
            if source.stem == "__init__":
                continue
            siblings: set[str] = set()
            for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith("minireason.loop."):
                            siblings.add(alias.name.rsplit(".", 1)[1])
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    if module.startswith("minireason.loop."):
                        siblings.add(module.rsplit(".", 1)[1])
                    elif module == "minireason.loop" or (node.level and not module):
                        # ``from minireason.loop import custody`` and
                        # ``from . import types``: the SIBLING is the name.
                        siblings.update(alias.name for alias in node.names)
                    elif node.level:
                        # ``from .types import X``.
                        siblings.add(module.split(".")[0])
            siblings = {name for name in siblings
                        if (package / f"{name}.py").exists()} - {source.stem}
            edges[source.stem] = siblings
        return edges

    def test_the_import_graph_is_the_one_the_interface_documents(self):
        self.assertEqual(self.package_edges(), self.DECLARED_EDGES,
                         "a module's imports moved; record the edge in "
                         "WAVE2-INTERFACE.md and update this table")

    def test_the_wave_zero_import_graph_is_acyclic(self):
        # standard must not import contracts; types must import no sibling.
        edges = self.package_edges()
        self.assertNotIn("contracts", edges["standard"],
                         "standard must not import contracts: that is the cycle")
        self.assertEqual(edges["types"], set(),
                         "types is the root of the package graph and imports no sibling")
        self.assertIn("standard", edges["contracts"])
        # No cycle anywhere: a depth-first walk finds no back edge.
        state: dict[str, int] = {}

        def walk_module(name: str) -> None:
            state[name] = 1
            for other in sorted(edges.get(name, ())):
                self.assertNotEqual(state.get(other), 1, f"cycle at {name} -> {other}")
                if other not in state:
                    walk_module(other)
            state[name] = 2

        for name in sorted(edges):
            if name not in state:
                walk_module(name)

    def test_every_contract_failure_is_a_loop_error_with_a_declared_code(self):
        for error in (c.ContractError(c.CONTRACT_VIOLATION, "x"),
                      c.SchemaInvalid("critic", "not-json", "x"),
                      c.ScoringKeyForbidden(("rank",))):
            with self.subTest(error=type(error).__name__):
                self.assertIsInstance(error, loop_types.LoopError)
                self.assertIsInstance(error, ValueError)
                self.assertIn(error.code, loop_types.FAILURE_CODES)


class WellFormedOutputs(unittest.TestCase):
    """The contracts of §2.3, on output a seat is allowed to produce."""

    def test_every_role_round_trips_through_its_typed_output(self):
        for role, body in WELL_FORMED.items():
            with self.subTest(role=role):
                value = c.validate(role, body)
                self.assertEqual(value.as_dict(), body)
                self.assertEqual(c.validate(role, json.dumps(body)), value)
                self.assertEqual(c.validate(role, json.dumps(body).encode("utf-8")),
                                 value)

    def test_every_role_has_a_validator_of_its_own(self):
        self.assertEqual(sorted(c.VALIDATORS), sorted(c.ROLE_NAMES))
        self.assertEqual(sorted(c.SCHEMAS), sorted(c.ROLE_NAMES))
        for role, validator in c.VALIDATORS.items():
            with self.subTest(role=role):
                self.assertEqual(validator(WELL_FORMED[role]),
                                 c.check(role, WELL_FORMED[role]))

    def test_a_critic_answering_none_owes_no_case_and_no_quote(self):
        body = replacing(CRITIC_OK, relation="none", case="", passage_quote="")
        value = c.validate("critic", body)
        self.assertFalse(value.claims_relation)
        self.assertFalse(value.is_outside_vocabulary)

    def test_a_reading_outside_the_vocabulary_is_kept_and_claims_nothing(self):
        body = replacing(CRITIC_OK, relation="none", case="", passage_quote="",
                         outside_vocabulary="concedes one point while repairing another")
        value = c.validate("critic", body)
        self.assertTrue(value.is_outside_vocabulary)
        self.assertFalse(value.claims_relation)
        self.assertEqual(value.outside_vocabulary,
                         "concedes one point while repairing another")
        self.assertEqual(c.OUTSIDE_VOCABULARY_FIELD, "outside_vocabulary")

    def test_the_word_bounds_of_section_2_3_are_enforced(self):
        self.assertEqual(dict(c.WORD_LIMITS), {
            ("critic", "case"): 400, ("defender", "answer"): 400,
            ("judge", "reading_note"): 120, ("marker", "case"): 120})
        for (role, field), limit in c.WORD_LIMITS.items():
            with self.subTest(role=role, field=field):
                at_limit = replacing(WELL_FORMED[role], **{field: "word " * limit})
                self.assertTrue(c.check(role, at_limit, register=(
                    "T" if role == "marker" else None)).ok)
                over = replacing(WELL_FORMED[role], **{field: "word " * (limit + 1)})
                self.assertEqual(c.check(role, over).reason, "word-limit")

    def test_a_marker_is_asked_one_register_at_a_time(self):
        # §2.3: "Never sees more than one register, so no call can trade
        # registers off." There is no register field in the output at all.
        self.assertNotIn("register", c.MARKER_SCHEMA["properties"])
        for register in c.REGISTERS:
            with self.subTest(register=register):
                body = replacing(MARKER_OK,
                                 difference_kind=c.DIFFERENCE_KINDS[register][0])
                self.assertTrue(c.check("marker", body, register=register).ok)

    def test_an_unresolved_mark_carries_no_difference_kind_and_needs_no_quotes(self):
        body = {"mark": "unresolved", "difference_kind": None, "left_quote": "",
                "right_quote": "", "case": ""}
        value = c.validate("marker", body, register="E")
        self.assertFalse(value.claims_difference)
        self.assertIsNone(value.difference_kind)

    def test_a_judge_ruling_is_two_labels_and_a_note(self):
        value = c.validate("judge", JUDGE_OK)
        self.assertIs(value.sustained, True)
        self.assertEqual(value.decisive_point, "narrows it")
        # conforming_transcript (vendored) needs a non-empty decisive_point.
        self.assertEqual(c.check("judge", replacing(JUDGE_OK, decisive_point="")).reason,
                         "empty-field")

    def test_the_variator_paraphrases_the_exchange_and_nothing_else(self):
        self.assertEqual(list(c.VARIATOR_SCHEMA["properties"]), ["paraphrases"])
        value = c.validate("variator", VARIATOR_OK)
        self.assertEqual(value.paraphrases, ("first wording", "second wording"))

    def test_the_module_declares_every_name_the_wave_plan_names(self):
        for name in ("READING_VOCABULARY", "OUTSIDE_VOCABULARY_FIELD", "REGISTERS",
                     "DIFFERENCE_KINDS", "MARKS", "CriticOutput", "DefenderOutput",
                     "JudgeRuling", "MarkerOutput", "VariatorOutput", "validate",
                     "SchemaInvalid", "assert_no_scoring_keys", "READING_BANNER"):
            with self.subTest(name=name):
                self.assertIn(name, c.__all__)
                self.assertTrue(hasattr(c, name))

    def test_no_block_code_registry_lives_here(self):
        # BLOCK_CODES belongs to W0-TYPES; a second registry would fork it.
        self.assertFalse(hasattr(c, "BLOCK_CODES"))
        for reason in c.SCHEMA_REASONS:
            self.assertNotIn("blocked:", reason)


class G12ReachesEveryOneOfItsThreeSubjects(unittest.TestCase):
    """B2: the key guard used to pass a rendered file and a table header.

    §2.4 G12 runs ``assert_no_scoring_keys`` "over every emitted artifact, every
    table header and every rendered file", and §5 *p4* ("no scoring key appears
    anywhere") is a protected obligation whose failure is ``STOP protected_loss``.
    Handing a ``str`` to a key-structure guard answered ``None`` in silence, so a
    published ``READING_TABLE.md`` with a ``score`` column satisfied *p4* without
    being looked at. Two of the three subjects were unfalsifiable.
    """

    def test_a_rendered_file_is_refused_rather_than_silently_passed(self):
        for rendered in ("| cell | relation | score | rank |",
                         "READING_TABLE.md\n\n| best endpoint | merit |\n",
                         b"| cell | score |",
                         bytearray(b"# Merit"),
                         ""):
            with self.subTest(rendered=repr(rendered)[:40]):
                with self.assertRaises(c.ContractError) as caught:
                    c.assert_no_scoring_keys(rendered)
                self.assertEqual(caught.exception.code, c.CONTRACT_VIOLATION)
                self.assertIn("assert_no_scoring_headers", str(caught.exception))
                self.assertIsInstance(caught.exception, loop_types.LoopError)

    def test_a_string_inside_a_structure_is_still_a_value_and_still_passes(self):
        # The refusal is about what the GUARD was handed, not about every string
        # it meets: a scoring word in a value is not a scoring key.
        self.assertIsNone(c.assert_no_scoring_keys(
            {"case": "the score of the match is not a key here"}))
        self.assertIsNone(c.assert_no_scoring_keys([None, True, "rank", ("merit",)]))
        self.assertIsNone(c.assert_no_scoring_keys({"a": {"b": ["score", b"rank"]}}))

    def test_the_header_scanner_is_the_standards_own_function(self):
        self.assertIs(c.assert_no_scoring_headers, standard.assert_no_scoring_headers)
        self.assertIn("assert_no_scoring_headers", c.__all__)
        for key in sorted(c.FORBIDDEN_KEYS):
            with self.subTest(key=key):
                # A GFM table: the header row is the line immediately above the
                # delimiter row, which is the rule the scanner now uses (item 40d).
                with self.assertRaises(standard.StandardInvalid) as caught:
                    c.assert_no_scoring_headers(
                        f"| cell | {key} | note |\n|---|---|---|\n| a | b | c |\n",
                        "READING_TABLE.md")
                self.assertEqual(caught.exception.code, c.SCORING_KEY_FORBIDDEN)
                self.assertIsInstance(caught.exception, loop_types.LoopError)
        self.assertIsNone(c.assert_no_scoring_headers(standard.CEILING_TEXT))

    def test_a_rendered_role_output_table_passes_both_halves_of_the_guard(self):
        for role, body in WELL_FORMED.items():
            with self.subTest(role=role):
                value = c.validate(role, body, register="T" if role == "marker" else None)
                c.assert_no_scoring_keys(value.as_dict())
                header = "| " + " | ".join(value.as_dict()) + " |"
                c.assert_no_scoring_headers(header, f"{role} table")


class ADifferenceKindIsCheckedAgainstItsOwnRegister(unittest.TestCase):
    """S11: ``VALIDATORS`` could not pass ``register=``, so O11 was unreachable."""

    def test_a_validator_forwards_the_register_to_the_check(self):
        marker = replacing(MARKER_OK, difference_kind="target_set_membership")
        self.assertTrue(c.VALIDATORS["marker"](marker, register="T").ok)
        refused = c.VALIDATORS["marker"](marker, register="G")
        self.assertFalse(refused.ok)
        self.assertEqual(refused.reason, "difference-kind-unknown")
        # Omitted, the union is still used, and nothing a caller did before breaks.
        self.assertTrue(c.VALIDATORS["marker"](marker).ok)
        for role, body in WELL_FORMED.items():
            with self.subTest(role=role):
                self.assertEqual(c.VALIDATORS[role](body), c.check(role, body))
                self.assertEqual(c.VALIDATORS[role](body, register=None),
                                 c.check(role, body))

    def test_every_register_holds_its_own_tokens_through_the_validator(self):
        for register in c.REGISTERS:
            own = c.DIFFERENCE_KINDS[register][0]
            foreign = next(token for other in c.REGISTERS if other != register
                           for token in c.DIFFERENCE_KINDS[other]
                           if token not in c.DIFFERENCE_KINDS[register])
            with self.subTest(register=register):
                self.assertTrue(c.VALIDATORS["marker"](
                    replacing(MARKER_OK, difference_kind=own), register=register).ok)
                self.assertFalse(c.VALIDATORS["marker"](
                    replacing(MARKER_OK, difference_kind=foreign), register=register).ok)


class ACriticCannotClaimARelationAndStepOutsideTheVocabulary(unittest.TestCase):
    """N6: both at once used to leave ``.relation`` naming a relation.

    D6 forces such a cell to ``unresolved`` and preserves the text; a renderer
    reading ``.relation`` printed the relation anyway. Normalising preserves the
    text, which refusing would not.
    """

    BOTH = replacing(CRITIC_OK, outside_vocabulary="concedes one point while repairing "
                                                   "another")

    def test_the_relation_reads_as_none_and_the_text_is_preserved(self):
        value = c.validate("critic", self.BOTH)
        self.assertEqual(value.relation, c.NONE_RELATION)
        self.assertFalse(value.claims_relation)
        self.assertTrue(value.is_outside_vocabulary)
        self.assertEqual(value.outside_vocabulary, self.BOTH["outside_vocabulary"])
        self.assertEqual(value.case, self.BOTH["case"])
        self.assertEqual(value.passage_quote, self.BOTH["passage_quote"])

    def test_what_the_seat_nominated_is_kept_rather_than_thrown_away(self):
        value = c.validate("critic", self.BOTH)
        self.assertEqual(value.nominated_relation, "qualifies")
        self.assertEqual(value.as_dict()["relation"], c.NONE_RELATION)
        self.assertEqual(value.as_dict()[c.OUTSIDE_VOCABULARY_FIELD],
                         self.BOTH["outside_vocabulary"])
        # What is recorded is what a renderer reads: the normalised record
        # re-validates to itself.
        again = c.validate("critic", value.as_dict())
        self.assertEqual(again.relation, c.NONE_RELATION)
        self.assertEqual(again.nominated_relation, "")

    def test_an_ordinary_critic_output_is_untouched(self):
        value = c.validate("critic", CRITIC_OK)
        self.assertEqual(value.relation, "qualifies")
        self.assertEqual(value.nominated_relation, "")
        self.assertTrue(value.claims_relation)
        self.assertEqual(value.as_dict(), CRITIC_OK)
        none = c.validate("critic", replacing(CRITIC_OK, relation="none", case="",
                                              passage_quote=""))
        self.assertEqual(none.relation, c.NONE_RELATION)
        self.assertEqual(none.nominated_relation, "")


class HardeningFindings(unittest.TestCase):
    """One test per item of the wave-1 integration decisions, items 20-23."""

    def test_item20_check_returns_at_every_nesting_depth(self):
        """Item 20: ~1000 levels of nesting raised RecursionError out of check().

        ``check`` promises never to raise; a two-kilobyte output that raised
        instead of answering left the cell with no block at all.
        """

        for depth in (990, 1000, 5000, 50000):
            for shape in ("[" * depth + "]" * depth, '{"a":' * depth + "1" + "}" * depth):
                with self.subTest(depth=depth, shape=shape[:2]):
                    result = c.check("critic", shape)
                    self.assertFalse(result.ok)
                    self.assertEqual(result.reason, "not-json")
                    self.assertIn(result.reason, c.SCHEMA_REASONS)
                    with self.assertRaises(c.SchemaInvalid) as caught:
                        c.validate("critic", shape)
                    self.assertEqual(caught.exception.reason, "not-json")
                    # bytes travel the same road as text
                    self.assertEqual(c.check("critic", shape.encode("utf-8")).reason,
                                     "not-json")
        # The boundary is declared, not discovered: one level under it parses.
        shallow = "[" * 5 + "]" * 5
        self.assertEqual(c.check("critic", shallow).reason, "not-an-object")

    def test_item21_the_aggregate_guard_sees_every_door_a_number_arrives_by(self):
        """Item 21: closedness was tested only where ``properties`` appeared."""

        text = {"type": "string"}
        open_schemas = {
            "bare open object": {"type": "object"},
            "numeric additionalProperties": {"type": "object",
                                             "additionalProperties": {"type": "number"}},
            "open object under a declared property": {
                "type": "object", "additionalProperties": False,
                "properties": {"case": {"type": "object"}}},
            "patternProperties": {"type": "object", "additionalProperties": False,
                                  "patternProperties": {"^x": {"type": "number"}}},
            "propertyNames only": {"type": "object",
                                   "propertyNames": {"pattern": "^[a-z]+$"}},
            "$ref": {"type": "object", "additionalProperties": False,
                     "properties": {"case": {"$ref": "#/$defs/n"}},
                     "$defs": {"n": {"type": "number"}}},
            "then/else": {"type": "object", "additionalProperties": False,
                          "properties": {"case": text},
                          "if": {"const": "x"}, "then": {"type": "number"}},
            "numeric enum with no type": {"type": "object",
                                          "additionalProperties": False,
                                          "properties": {"case": {"enum": [1, 2]}}},
            "numeric const with no type": {"type": "object",
                                           "additionalProperties": False,
                                           "properties": {"case": {"const": 7}}},
            "dependentSchemas": {"type": "object", "additionalProperties": False,
                                 "properties": {"mark": text},
                                 "dependentSchemas": {"mark": {"type": "number"}}},
            "a true sub-schema": {"type": "object", "additionalProperties": False,
                                  "properties": {"case": True}},
            "an aggregate name behind a $defs-free dependentSchemas": {
                "type": "object", "additionalProperties": False,
                "properties": {"case": text},
                "dependentSchemas": {"count": {"type": "string"}}},
        }
        for label, schema in open_schemas.items():
            with self.subTest(schema=label):
                with self.assertRaises(c.ContractError) as caught:
                    c.assert_no_aggregate_fields(schema)
                self.assertEqual(caught.exception.code, c.CONTRACT_VIOLATION)
        # The controls still pass, and the five shipped schemas still pass.
        c.assert_no_aggregate_fields({"type": "object", "additionalProperties": False,
                                      "properties": {"case": text}})
        c.assert_no_aggregate_fields({"type": "object", "additionalProperties": False,
                                      "properties": {"case": {"enum": ["a", "b"]}}})
        for role in c.ROLE_NAMES:
            with self.subTest(role=role):
                self.assertIsNone(c.assert_no_aggregate_fields(c.schema_for(role)))

    def test_item22_an_unhashable_role_or_register_is_answered_not_raised(self):
        """Item 22(a): membership was tested before the type was."""

        for role in ([], {}, set(), 7, None):
            with self.subTest(role=role):
                answer = c.check(role, "{}")
                self.assertFalse(answer.ok)
                self.assertEqual(answer.reason, "unknown-role")
                with self.assertRaises(c.SchemaInvalid) as caught:
                    c.schema_for(role)
                self.assertEqual(caught.exception.reason, "unknown-role")
        for register in ([], {}, 7, "Q"):
            with self.subTest(register=register):
                with self.assertRaises(c.SchemaInvalid) as caught:
                    c.difference_kinds_for(register)
                self.assertEqual(caught.exception.reason, "unknown-register")
                answer = c.check("marker", json.dumps(MARKER_OK), register=register)
                self.assertFalse(answer.ok)
                self.assertEqual(answer.reason, "unknown-register")
                # ... and a bogus register is no longer silent on another role
                other = c.check("defender", json.dumps(DEFENDER_OK), register=register)
                self.assertFalse(other.ok)
                self.assertEqual(other.reason, "unknown-register")

    def test_item22_the_differs_mark_is_imported_not_retyped(self):
        """Item 22(e): the token was a literal at two program sites."""

        self.assertIs(c.DIFFERS_MARK, standard.DIFFERS_MARK)
        self.assertIn(c.DIFFERS_MARK, c.MARKS)
        source = Path(c.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        literals = [node for node in ast.walk(tree)
                    if isinstance(node, ast.Constant) and node.value == "differs"]
        self.assertEqual(literals, [], "'differs' is retyped in contracts.py")

    def test_item22_a_schema_invalid_keeps_the_loop_error_string_invariant(self):
        """Item 22 / 23: ``str(exc) == f"{code}: {detail}"`` was broken here."""

        with self.assertRaises(c.SchemaInvalid) as caught:
            c.validate("defender", {"answer": "a"})
        exc = caught.exception
        self.assertEqual(str(exc), f"{exc.code}: {exc.detail}")
        self.assertIn(exc.message, exc.detail)
        self.assertEqual(exc.code, c.SCHEMA_INVALID)

    def test_item23_a_leaf_the_scoring_guard_cannot_read_is_refused(self):
        """Item 23: a dataclass, a set, a generator walked past in silence."""

        from collections import deque
        from dataclasses import dataclass

        @dataclass
        class Holder:
            score: int = 3

        opaque = ({"a": {1, 2}}, {"a": deque([1])},
                  {"a": (x for x in ())}, {"a": {"b": 1}.values()},
                  {"a": memoryview(b"x")}, {"a": frozenset()})
        for value in opaque:
            with self.subTest(value=type(value["a"]).__name__):
                with self.assertRaises(c.ContractError) as caught:
                    c.assert_no_scoring_keys(value)
                self.assertEqual(caught.exception.code, c.CONTRACT_VIOLATION)
        # A dataclass is DESCENDED, not walked past and not refused: its field
        # names are its keys, and the loop's own records are frozen dataclasses.
        with self.assertRaises(c.ScoringKeyForbidden) as forbidden:
            c.assert_no_scoring_keys({"a": Holder()})
        self.assertEqual(forbidden.exception.path, ("a", "score"))

        @dataclass
        class Clean:
            note: str = "the score of the match"

        self.assertIsNone(c.assert_no_scoring_keys({"a": Clean()}))
        # Every JSON leaf still passes, and the guard still catches the key.
        self.assertIsNone(c.assert_no_scoring_keys(
            {"a": "score", "b": 1, "c": 1.5, "d": True, "e": None, "f": b"x",
             "g": [{"h": "i"}]}))
        with self.assertRaises(c.ScoringKeyForbidden):
            c.assert_no_scoring_keys({"a": [{"rank": "x"}]})

    def test_item23_a_repeated_json_key_is_refused_not_last_wins(self):
        raw = '{"mark": "same", "mark": "differs"}'
        answer = c.check("marker", raw)
        self.assertFalse(answer.ok)
        self.assertEqual(answer.reason, "unexpected-field")
        self.assertEqual(answer.path, ("mark",))

    def test_item23_an_array_index_in_a_schema_path_sorts_as_a_number(self):
        key = c._path_key(("paraphrases", 2))
        self.assertLess(key, c._path_key(("paraphrases", 10)))
        self.assertLess(c._path_key(("a",)), c._path_key(("b",)))

    def test_item22_editing_a_published_schema_cannot_widen_a_vocabulary(self):
        """Item 22(b): the validators read a copy nobody else holds."""

        enum = c.CRITIC_SCHEMA["properties"]["relation"]["enum"]
        self.assertEqual(c.check("critic", replacing(CRITIC_OK, relation="outperforms")
                                 ).reason, "not-in-enum")
        enum.append("outperforms")
        try:
            self.assertEqual(
                c.check("critic", replacing(CRITIC_OK, relation="outperforms")).reason,
                "not-in-enum", "an in-process edit widened the closed vocabulary")
        finally:
            enum.remove("outperforms")
        # The per-register token sets are read-only views.
        self.assertIsInstance(c.DIFFERENCE_KINDS, type(standard.DIFFERENCE_KINDS))
        with self.assertRaises(TypeError):
            c.DIFFERENCE_KINDS["Q"] = ("invented",)

    def test_item23_the_two_name_bans_are_disjoint_and_both_applied(self):
        self.assertEqual(set(c.AGGREGATE_KEYS) & set(c.FORBIDDEN_KEYS), set())
        for name in ("count", "score"):
            with self.subTest(name=name):
                with self.assertRaises(c.ContractError):
                    c.assert_no_aggregate_fields(
                        {"type": "object", "additionalProperties": False,
                         "properties": {name: {"type": "string"}}})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
