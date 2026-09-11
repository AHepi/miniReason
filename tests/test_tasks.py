import json
import unittest

from minireason.tasks import ProgramError, evaluate, exact_equal, execute, parse_program, private_cases, reference, task_prompt


def variable(name):
    return {"var": name}


def get(value, key):
    return {"op": "get", "value": value, "key": key}


def binary(op, a, b):
    return {"op": op, "args": [a, b]}


def mapping(items, name, expression):
    return {"op": "map", "items": items, "as": name, "do": expression}


def filtering(items, name, expression):
    return {"op": "filter", "items": items, "as": name, "do": expression}


def correct_program():
    """Supplied-solution instrument calibration only; never included in model packs."""
    inp, event, booking, item = map(variable, ["input", "e", "booking", "item"])
    events = get(inp, "events")
    latest = mapping({"op": "unique", "items": mapping(events, "e", get(event, "booking"))}, "booking",
                     {"op": "max_by", "items": filtering(events, "e", binary("eq", get(event, "booking"), booking)),
                      "as": "e", "key": get(event, "revision")})
    active = filtering(variable("latest"), "e", binary("and", binary("eq", get(event, "kind"), "hold"),
                                                      binary("gt", get(event, "expires_at"), get(inp, "now"))))
    total = {"op": "sum", "value": mapping(filtering(variable("active"), "e", binary("eq", get(event, "item"), item)), "e", get(event, "quantity"))}
    capacity = get({"op": "max_by", "items": filtering(get(inp, "stock"), "s", binary("eq", get(variable("s"), "item"), item)),
                    "as": "s", "key": 0}, "capacity")
    row = {"op": "let", "name": "total", "value": total, "do": {"op": "object", "fields": {
        "item": item, "reserved": variable("total"), "available": binary("sub", capacity, variable("total"))}}}
    return {"op": "let", "name": "latest", "value": latest, "do": {
        "op": "let", "name": "active", "value": active, "do": mapping({"op": "sort", "items": mapping(get(inp, "stock"), "s", get(variable("s"), "item"))}, "item", row)}}


class TaskTests(unittest.TestCase):
    def test_supplied_solution_passes_public_and_unseen_variations(self):
        program = json.dumps(correct_program())
        self.assertTrue(evaluate(program)["all_pass"])
        self.assertTrue(evaluate(program, holdout=True)["all_pass"])

    def test_expiry_does_not_resurrect_old_version(self):
        from minireason.tasks import PUBLIC_CASES
        case = next(c for c in PUBLIC_CASES if c["name"] == "latest_expired_does_not_resurrect_old")
        self.assertEqual(reference(case["input"])[0]["reserved"], 0)

    def test_bad_program_cannot_pass_by_merely_being_valid_json(self):
        result = evaluate("[]")
        self.assertTrue(result["runnable"])
        self.assertFalse(result["all_pass"])
        self.assertTrue(all("input" in c for c in result["cases"]))

    def test_unknown_operator_is_a_loud_execution_failure(self):
        result = evaluate('{"op":"read_environment"}')
        self.assertFalse(result["runnable"])
        self.assertIn("DSL_UNKNOWN_OPERATOR", result["cases"][0]["error"])

    def test_step_limit_and_branch_laziness(self):
        with self.assertRaisesRegex(ProgramError, "DSL_STEP_LIMIT"):
            execute([1, 2, 3], {}, step_limit=2)
        result, _ = execute({"op": "if", "test": True, "then": 7, "else": {"var": "secret"}}, {})
        self.assertEqual(result, 7)

    def test_holdout_case_bytes_do_not_enter_task_prompt(self):
        prompt = task_prompt()
        for case in private_cases():
            self.assertNotIn(case["name"], prompt)

    def test_lexical_scope_prevents_variable_leak(self):
        with self.assertRaisesRegex(ProgramError, "DSL_UNBOUND_VARIABLE"):
            execute([{"op": "let", "name": "x", "value": 1, "do": {"var": "x"}}, {"var": "x"}], {})

    def test_output_equality_does_not_turn_booleans_into_integer_quantities(self):
        self.assertFalse(exact_equal([{"reserved": False}], [{"reserved": 0}]))
        self.assertFalse(exact_equal([{"reserved": True}], [{"reserved": 1}]))
        self.assertFalse(exact_equal([{"reserved": 0.0}], [{"reserved": 0}]))
        wrapped = {"op": "map", "items": correct_program(), "as": "r", "do": {"op": "object", "fields": {
            "item": get(variable("r"), "item"),
            "available": get(variable("r"), "available"),
            "reserved": {"op": "if", "test": binary("eq", get(variable("r"), "reserved"), 0),
                         "then": False, "else": get(variable("r"), "reserved")}}}}
        self.assertFalse(evaluate(json.dumps(wrapped))["all_pass"])

    def test_arithmetic_cannot_allocate_sequences_or_accept_boolean_numbers(self):
        for value in ["x", [0], True]:
            with self.subTest(value=value), self.assertRaisesRegex(ProgramError, "DSL_NUMBERS_REQUIRED"):
                execute({"op": "mul", "args": [value, 1_000_000_000]}, {})

    def test_unknown_fields_and_duplicate_keys_are_rejected(self):
        with self.assertRaisesRegex(ProgramError, "DSL_FIELDS_INVALID"):
            execute({"op": "len", "value": [], "invented": 1}, {})
        with self.assertRaisesRegex(ProgramError, "duplicate key"):
            parse_program('{"op":"len","value":[],"value":[1]}')

    def test_boolean_conditions_are_typed_and_numbers_are_bounded(self):
        with self.assertRaisesRegex(ProgramError, "DSL_BOOLEAN_REQUIRED"):
            execute({"op": "if", "test": 1, "then": 7, "else": 8}, {})
        with self.assertRaisesRegex(ProgramError, "DSL_NUMBER_LIMIT"):
            execute({"op": "mul", "args": [2 ** 200, 2 ** 200]}, {})


if __name__ == "__main__":
    unittest.main()
