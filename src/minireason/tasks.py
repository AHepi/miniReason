"""Bounded, compositional program synthesis tasks with independently computed answers.

Candidate programs are data. They cannot import, write files, inspect process state,
or call a network. The DSL deliberately exposes generic collection operations, not
named reservation algorithms. Success is finite task behavior, never an ECS verdict.
"""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any


class ProgramError(ValueError):
    pass


_FIELDS = {
    "object": {"fields"}, "list": {"items"}, "get": {"value", "key"},
    "if": {"test", "then", "else"}, "let": {"name", "value", "do"},
    **{name: {"items", "as", "do"} for name in ("map", "filter", "flatmap")},
    **{name: {"items", "as", "key"} for name in ("max_by", "min_by")},
    **{name: {"items"} for name in ("unique", "sort")},
    **{name: {"value"} for name in ("sum", "len", "not")},
    **{name: {"args"} for name in ("add", "sub", "mul", "eq", "ne", "lt", "le", "gt", "ge", "and", "or", "in")},
}


def _validate_program(program: Any) -> None:
    nodes = 0

    def visit(value: Any, depth: int = 0) -> None:
        nonlocal nodes
        nodes += 1
        if nodes > 4_000 or depth > 100:
            raise ProgramError("DSL_PROGRAM_SIZE_LIMIT")
        if isinstance(value, list):
            if len(value) > 4_096:
                raise ProgramError("DSL_COLLECTION_LIMIT")
            for child in value:
                visit(child, depth + 1)
            return
        if not isinstance(value, dict):
            if value is not None and type(value) not in (str, int, float, bool):
                raise ProgramError("DSL_JSON_LITERAL_REQUIRED")
            if type(value) is int and value.bit_length() > 256:
                raise ProgramError("DSL_NUMBER_LIMIT")
            if type(value) is float and not math.isfinite(value):
                raise ProgramError("DSL_FINITE_NUMBER_REQUIRED")
            if isinstance(value, str) and len(value) > 100_000:
                raise ProgramError("DSL_STRING_LIMIT")
            return
        if set(value) == {"var"}:
            if type(value["var"]) is not str or not value["var"]:
                raise ProgramError("DSL_VARIABLE_NAME_REQUIRED")
            return
        op = value.get("op")
        if type(op) is not str or op not in _FIELDS:
            raise ProgramError(f"DSL_UNKNOWN_OPERATOR: {op}")
        required = _FIELDS[op] | {"op"}
        allowed = required | ({"default"} if op == "get" else set())
        if not required <= set(value) or not set(value) <= allowed:
            raise ProgramError(f"DSL_FIELDS_INVALID: {op}; required={sorted(required)}; received={sorted(value)}")
        for key, child in value.items():
            if key == "op":
                continue
            if key in {"as", "name"}:
                if type(child) is not str or not child:
                    raise ProgramError(f"DSL_VARIABLE_NAME_REQUIRED: {key}")
            elif op == "object" and key == "fields":
                if not isinstance(child, dict) or any(type(k) is not str for k in child):
                    raise ProgramError("DSL_OBJECT_FIELDS_REQUIRED")
                for field in child.values():
                    visit(field, depth + 1)
            else:
                if key == "args" and (not isinstance(child, list) or len(child) != 2):
                    raise ProgramError(f"DSL_BINARY_ARITY: {op}")
                if op == "list" and not isinstance(child, list):
                    raise ProgramError("DSL_LIST_REQUIRED: list items")
                visit(child, depth + 1)

    visit(program)


def _check_output_size(value: Any) -> None:
    pending = [value]
    nodes = 0
    while pending:
        current = pending.pop()
        nodes += 1
        if nodes > 20_000:
            raise ProgramError("DSL_OUTPUT_SIZE_LIMIT")
        if isinstance(current, dict):
            pending.extend(current.values())
        elif isinstance(current, list):
            pending.extend(current)


def exact_equal(a: Any, b: Any) -> bool:
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return set(a) == set(b) and all(exact_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(exact_equal(x, y) for x, y in zip(a, b))
    return a == b


DSL_GUIDE = """Write a JSON expression program in the commitments string, optionally wrapped as
{"program": EXPR}. The body is unrestricted prose: explain the mechanism, assumptions,
which observations would defeat it, and what successful behavior a change must preserve.
An expression is a JSON literal (numbers, strings, booleans, null, lists), {"var":"name"},
or an operation object. Literal dictionaries use {"op":"object","fields":{"key":EXPR}}.
Input is {"var":"input"}. The available operations and exact fields are:
get: value EXPR, key EXPR, optional default EXPR (missing keys otherwise fail).
if: test EXPR, then EXPR, else EXPR (only selected branch evaluates).
let: name STRING, value EXPR, do EXPR (lexical scope).
map/filter: items EXPR, as STRING, do EXPR (filter do is boolean).
flatmap: same fields; do returns a list; concatenate the lists.
unique: items EXPR (first occurrence order; values compared structurally).
sort: items EXPR (ascending numbers or strings).
max_by/min_by: items EXPR, as STRING, key EXPR (first tie wins; empty fails).
sum/len/not: value EXPR. sum takes a list of numbers; len a list/string/dictionary.
add/sub/mul/eq/ne/lt/le/gt/ge/and/or/in: args [EXPR, EXPR]. Arithmetic takes numbers
only (never booleans, strings, or lists). Boolean operations and if require booleans.
and/or short circuit. Output values must match the task's declared JSON types exactly.
list: items [EXPR,...] (ordinary JSON lists also evaluate their elements).
Every field is exact: no Python, string interpolation, implicit lambdas, or unknown operators.
Programs are limited to 30,000 expression/collection work units, 100 nesting levels,
4,000 syntax nodes, 4,096 items per collection, 256-bit integers and finite floats,
and 20,000 expanded output nodes. Errors are
execution failures, not refutations of prose. Do not encode the supplied examples as a lookup.
"""


def execute(program: Any, source: Any, *, step_limit: int = 30_000) -> tuple[Any, int]:
    """Interpret an expression with deterministic work accounting and no ambient authority."""
    _validate_program(program)
    steps = 0

    def ev(expr: Any, env: dict[str, Any], depth: int = 0) -> Any:
        nonlocal steps
        steps += 1
        if steps > step_limit:
            raise ProgramError("DSL_STEP_LIMIT")
        if depth > 100:
            raise ProgramError("DSL_DEPTH_LIMIT")
        result = calc(expr, env, depth)
        if isinstance(result, (list, dict)) and len(result) > 4_096:
            raise ProgramError("DSL_COLLECTION_LIMIT")
        if type(result) is int and result.bit_length() > 256:
            raise ProgramError("DSL_NUMBER_LIMIT")
        if type(result) is float and not math.isfinite(result):
            raise ProgramError("DSL_FINITE_NUMBER_REQUIRED")
        return result

    def charge_work(amount: int) -> None:
        nonlocal steps
        steps += amount
        if steps > step_limit:
            raise ProgramError("DSL_STEP_LIMIT")

    def calc(expr: Any, env: dict[str, Any], depth: int) -> Any:
        rec = lambda value, scope=env: ev(value, scope, depth + 1)
        if isinstance(expr, list):
            return [rec(x) for x in expr]
        if not isinstance(expr, dict):
            return expr
        if set(expr) == {"var"}:
            name = expr["var"]
            if name not in env:
                raise ProgramError(f"DSL_UNBOUND_VARIABLE: {name}")
            return env[name]
        op = expr.get("op")
        if op == "object":
            return {name: rec(value) for name, value in expr["fields"].items()}
        if op == "list":
            return [rec(value) for value in expr["items"]]
        if op == "get":
            value, key = rec(expr["value"]), rec(expr["key"])
            if isinstance(value, dict) and type(key) is not str:
                raise ProgramError("DSL_STRING_KEY_REQUIRED")
            if isinstance(value, (list, str)) and type(key) is not int:
                raise ProgramError("DSL_INTEGER_INDEX_REQUIRED")
            if not isinstance(value, (dict, list, str)):
                raise ProgramError("DSL_INDEXABLE_VALUE_REQUIRED")
            try:
                return value[key]
            except (KeyError, IndexError):
                if "default" in expr:
                    return rec(expr["default"])
                raise ProgramError(f"DSL_MISSING_KEY: {key}") from None
        if op == "if":
            test = rec(expr["test"])
            if type(test) is not bool:
                raise ProgramError("DSL_BOOLEAN_REQUIRED: if")
            return rec(expr["then"] if test else expr["else"])
        if op == "let":
            return rec(expr["do"], {**env, expr["name"]: rec(expr["value"])})
        if op in {"map", "filter", "flatmap", "max_by", "min_by"}:
            items = rec(expr["items"])
            if not isinstance(items, list):
                raise ProgramError(f"DSL_LIST_REQUIRED: {op}")
            charge_work(len(items))
            if op in {"max_by", "min_by"}:
                if not items:
                    raise ProgramError(f"DSL_EMPTY_SELECTION: {op}")
                pairs = [(rec(expr["key"], {**env, expr["as"]: item}), index, item)
                         for index, item in enumerate(items)]
                best = (max if op == "max_by" else min)(p[0] for p in pairs)
                return next(item for key, _, item in pairs if key == best)
            results = [rec(expr["do"], {**env, expr["as"]: item}) for item in items]
            if op == "map":
                return results
            if op == "filter":
                if any(type(value) is not bool for value in results):
                    raise ProgramError("DSL_BOOLEAN_REQUIRED: filter")
                return [item for item, keep in zip(items, results) if keep]
            if any(not isinstance(value, list) for value in results):
                raise ProgramError("DSL_LIST_REQUIRED: flatmap result")
            charge_work(sum(len(group) for group in results))
            if sum(len(group) for group in results) > 4_096:
                raise ProgramError("DSL_COLLECTION_LIMIT")
            return [item for group in results for item in group]
        if op in {"unique", "sort"}:
            items = rec(expr["items"])
            if not isinstance(items, list):
                raise ProgramError(f"DSL_LIST_REQUIRED: {op}")
            charge_work(len(items) * max(1, len(items).bit_length()) if op == "sort" else len(items))
            if op == "sort":
                if any(type(item) not in (str, int, float) for item in items):
                    raise ProgramError("DSL_SORTABLE_SCALARS_REQUIRED")
                return sorted(items)
            out, keys = [], set()
            for item in items:
                _check_output_size(item)
                key = json.dumps(item, sort_keys=True, separators=(",", ":"))
                if key not in keys:
                    keys.add(key)
                    out.append(item)
            return out
        if op in {"sum", "len", "not"}:
            value = rec(expr["value"])
            if op == "not":
                if type(value) is not bool:
                    raise ProgramError("DSL_BOOLEAN_REQUIRED: not")
                return not value
            if op == "len":
                if not isinstance(value, (list, str, dict)):
                    raise ProgramError("DSL_COLLECTION_REQUIRED: len")
                return len(value)
            if not isinstance(value, list) or any(type(v) not in (int, float) for v in value):
                raise ProgramError("DSL_NUMBERS_REQUIRED: sum")
            charge_work(len(value))
            return sum(value)
        if op in {"add", "sub", "mul", "eq", "ne", "lt", "le", "gt", "ge", "and", "or", "in"}:
            args = expr["args"]
            if not isinstance(args, list) or len(args) != 2:
                raise ProgramError(f"DSL_BINARY_ARITY: {op}")
            a = rec(args[0])
            if op == "and":
                if type(a) is not bool:
                    raise ProgramError("DSL_BOOLEAN_REQUIRED: and")
                b = rec(args[1]) if a else False
                if type(b) is not bool:
                    raise ProgramError("DSL_BOOLEAN_REQUIRED: and")
                return a and b
            if op == "or":
                if type(a) is not bool:
                    raise ProgramError("DSL_BOOLEAN_REQUIRED: or")
                b = True if a else rec(args[1])
                if type(b) is not bool:
                    raise ProgramError("DSL_BOOLEAN_REQUIRED: or")
                return a or b
            b = rec(args[1])
            if op in {"add", "sub", "mul"} and any(type(v) not in (int, float) for v in (a, b)):
                raise ProgramError(f"DSL_NUMBERS_REQUIRED: {op}")
            _check_output_size(a)
            _check_output_size(b)
            return {"add": lambda: a + b, "sub": lambda: a - b, "mul": lambda: a * b,
                    "eq": lambda: a == b, "ne": lambda: a != b,
                    "lt": lambda: a < b, "le": lambda: a <= b,
                    "gt": lambda: a > b, "ge": lambda: a >= b,
                    "in": lambda: a in b}[op]()
        raise ProgramError(f"DSL_UNKNOWN_OPERATOR: {op}")

    try:
        answer = ev(program, {"input": source})
        _check_output_size(answer)
    except ProgramError:
        raise
    except (KeyError, TypeError, ValueError, IndexError, OverflowError) as error:
        raise ProgramError(f"DSL_INVALID_EXPRESSION: {type(error).__name__}: {error}") from None
    return answer, steps


def _event(booking: str, revision: int, kind: str, quantity: int = 0,
           expiry: int = 999, item: str = "widget") -> dict[str, Any]:
    return {"booking": booking, "revision": revision, "kind": kind,
            "quantity": quantity, "expires_at": expiry, "item": item}


RESERVATION_TASK = """Build an executable account of a replicated stock-reservation snapshot.
Deliveries are an unordered bag of immutable event records. The same record may be delivered
many times. Each booking has exactly one immutable item. For each booking, a strictly higher
integer revision replaces ALL lower revisions. A booking/revision pair never has conflicting
contents. The latest revision may be a hold or release. A latest hold is active exactly when
expires_at > input.now; a latest release reserves zero. An expired latest hold does NOT make an
older unexpired hold reappear. Revision order, not delivery order, determines the latest event.
Quantity is the total quantity of that booking version, never an incremental delta.
Stock is input.stock, a list of {item, capacity}; item names are unique. Events only name
listed stock items. Produce a list in ascending item-name order, including items with no events:
[{"item":NAME,"reserved":TOTAL_ACTIVE_LATEST_QUANTITY,"available":CAPACITY-TOTAL},...].
Oversubscription must be visible as negative availability; never clamp, invent rejection order,
or silently discard a booking. Capacity, quantities, revisions, and logical times are integers.
The task is to derive one general procedure from these obligations, not memorize examples.
Explain why replay, reordering, expiry, and later cancellation interact correctly. State what
would falsify your account and which previously successful behavior a revision preserves.
"""


def _case(name: str, events: list[dict[str, Any]], *, now: int = 10,
          stock: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {"name": name, "input": {"now": now, "stock": stock or [{"item": "widget", "capacity": 10}],
                                     "events": events}}


PUBLIC_CASES = [
    _case("empty_and_unused_stock", [], stock=[{"item": "z", "capacity": 3}, {"item": "a", "capacity": 8}]),
    _case("duplicate_delivery_is_not_extra_stock", [_event("b", 1, "hold", 3, 20)] * 3),
    _case("reordering_and_replacement", [_event("b", 3, "hold", 4, 20), _event("b", 1, "hold", 7, 20)]),
    _case("release_stays_released", [_event("b", 2, "release"), _event("b", 1, "hold", 3, 20)]),
    _case("latest_expired_does_not_resurrect_old", [_event("b", 1, "hold", 2, 40), _event("b", 2, "hold", 5, 10)]),
]


def private_cases() -> list[dict[str, Any]]:
    """Held out from task prompts; recorded with experiment evidence after calls finish."""
    cases = [
        _case("expiry_boundary", [_event("x", 2, "hold", 7, 10), _event("y", 4, "hold", 2, 11)]),
        _case("oversubscription_is_visible", [_event("x", 1, "hold", 9, 20), _event("y", 1, "hold", 6, 20)]),
        _case("new_hold_after_release", [_event("x", 2, "release"), _event("x", 3, "hold", 5, 12), _event("x", 1, "hold", 8, 50)]),
        _case("multiple_items_and_zero_capacity", [_event("x", 1, "hold", 2, 20, "a"), _event("y", 1, "hold", 1, 20, "z")],
              stock=[{"item": "z", "capacity": 0}, {"item": "empty", "capacity": 6}, {"item": "a", "capacity": 10}]),
    ]
    for offset in range(8):
        events = [_event("x", 1, "hold", 3, 100), _event("x", 7, "hold", offset, 13),
                  _event("y", 2, "hold", 4, 12), _event("y", 3, "release"),
                  _event("z", 1, "hold", 2, 20)]
        ordered = events[offset % 5:] + events[:offset % 5]
        if offset % 2:
            ordered = list(reversed(ordered))
        cases.append(_case(f"metamorphic_replay_revision_expiry_{offset}", ordered + ordered[:offset % 4], now=10 + offset))
    return cases


def reference(source: dict[str, Any]) -> list[dict[str, Any]]:
    """Independent Python reading of the published contract, never rendered to a model."""
    latest: dict[str, dict[str, Any]] = {}
    for event in source["events"]:
        previous = latest.get(event["booking"])
        if previous is None or event["revision"] > previous["revision"]:
            latest[event["booking"]] = event
    totals = {row["item"]: 0 for row in source["stock"]}
    for event in latest.values():
        if event["kind"] == "hold" and event["expires_at"] > source["now"]:
            totals[event["item"]] += event["quantity"]
    return [{"item": row["item"], "reserved": totals[row["item"]],
             "available": row["capacity"] - totals[row["item"]]}
            for row in sorted(source["stock"], key=lambda row: row["item"])]


def task_prompt(task_id: str = "reservation_replay_v1") -> str:
    if task_id != "reservation_replay_v1":
        raise KeyError(task_id)
    examples = [{**case, "expected": reference(case["input"])} for case in PUBLIC_CASES[:2]]
    return RESERVATION_TASK + "\n" + DSL_GUIDE + "\nPublic examples:\n" + json.dumps(examples, indent=2)


def parse_program(commitments: str) -> Any:
    text = commitments.strip()
    if len(text) > 500_000:
        raise ProgramError("PROGRAM_TEXT_SIZE_LIMIT")
    if text.startswith("```") and text.endswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    def unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate key: {key}")
            value[key] = item
        return value

    try:
        value = json.loads(text, object_pairs_hook=unique_keys,
                           parse_constant=lambda word: (_ for _ in ()).throw(ValueError(f"nonfinite: {word}")))
    except (ValueError, TypeError, RecursionError) as error:
        raise ProgramError(f"PROGRAM_NOT_JSON: {error}") from None
    if isinstance(value, dict) and "program" in value:
        if set(value) != {"program"}:
            raise ProgramError("PROGRAM_WRAPPER_FIELDS_INVALID")
        return value["program"]
    return value


def evaluate(commitments: str, *, holdout: bool = False,
             task_id: str = "reservation_replay_v1") -> dict[str, Any]:
    if task_id != "reservation_replay_v1":
        raise KeyError(task_id)
    cases = private_cases() if holdout else PUBLIC_CASES
    results = []
    try:
        program = parse_program(commitments)
    except ProgramError as error:
        return {"schema": "minireason.evaluation.v1", "task_id": task_id, "holdout": holdout,
                "runnable": False, "all_pass": False, "error": str(error), "cases": []}
    for case in cases:
        expected = reference(case["input"])
        try:
            actual, steps = execute(program, case["input"])
            row = {"name": case["name"], "pass": exact_equal(actual, expected), "actual": actual,
                   "expected": expected, "steps": steps}
            if not row["pass"]:
                row["input"] = case["input"]
        except ProgramError as error:
            row = {"name": case["name"], "pass": False, "error": str(error), "input": case["input"], "expected": expected}
        results.append(row)
    return {"schema": "minireason.evaluation.v1", "task_id": task_id, "holdout": holdout,
            "runnable": all("error" not in row for row in results),
            "all_pass": all(row["pass"] for row in results), "cases": results,
            "program_sha256": hashlib.sha256(json.dumps(program, sort_keys=True).encode()).hexdigest()}
