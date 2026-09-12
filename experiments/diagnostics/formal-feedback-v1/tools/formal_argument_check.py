#!/usr/bin/env python3
"""Bounded Boolean diagnostic for an explicit, inspectable argument artifact.

This is not a model's private reasoning trace or a semantic adequacy judge.
Grammar: atom string; {"not": formula}; or one of and/or/implies/iff mapped
to a formula list. and/or require at least two operands; implies/iff exactly two.
Only standard-library functions and exhaustive Boolean valuations are used.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import re
import sys


CHECKER_VERSION = "finite-explicit-argument-v1"
LIMITS = {
    "max_input_bytes": 131072,
    "max_atoms": 10,
    "max_premises": 64,
    "max_formula_nodes": 512,
    "max_total_formula_nodes": 2048,
    "max_formula_depth": 24,
    "max_text_chars": 20000,
}
SCOPE = (
    "Classical propositional logic with independent Boolean atoms, exhaustive "
    "valuations, and exactly the submitted premises. No quantifiers, time, "
    "probability, executable code, or external evidence are interpreted. "
    "Atom meanings and prose objections are preserved but not evaluated. "
    "Entailment, refutation, and consistency do not establish that a mapping "
    "captures the prose problem, that assumptions are true, or that a next "
    "inquiry should be promoted. Vacuity and circular support can pass."
)
IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9_]{0,63}\Z")


def issue(kind: str, path: str, message: str) -> dict:
    return {"kind": kind, "path": path, "message": message}


def validate_argument(argument: object) -> list[dict]:
    """Validate the entire supplied contract before evaluating any valuation.

    Formula traversal is iterative. Over-budget formulas are still inspected
    for malformed nodes; only an entirely valid and within-budget contract can
    reach evaluation. The byte-bound loader limits the traversal input size.
    """
    problems = []
    if not isinstance(argument, dict):
        return [issue("invalid", "$", "Argument must be a JSON object.")]
    required = {"schema_version", "problem", "atoms", "premises", "goal",
                "prose_objections", "provenance"}
    for key in sorted(required - argument.keys()):
        problems.append(issue("invalid", "$", f"Missing required field: {key}."))
    for key in sorted(argument.keys() - required):
        problems.append(issue("invalid", f"$.{key}", "Unknown contract field."))
    if type(argument.get("schema_version")) is not int or argument.get("schema_version") != 1:
        problems.append(issue("invalid", "$.schema_version", "Expected integer 1."))

    def text_field(value: object, path: str, nonempty: bool = True) -> None:
        if not isinstance(value, str) or (nonempty and not value.strip()):
            problems.append(issue("invalid", path, "Expected a nonempty string." if nonempty else "Expected a string."))
        elif len(value) > LIMITS["max_text_chars"]:
            problems.append(issue("unsupported", path, "Text exceeds max_text_chars."))

    text_field(argument.get("problem"), "$.problem")
    text_field(argument.get("provenance"), "$.provenance")
    objections = argument.get("prose_objections")
    if not isinstance(objections, list):
        problems.append(issue("invalid", "$.prose_objections", "Expected a list of opaque prose strings."))
    else:
        for index, objection in enumerate(objections):
            text_field(objection, f"$.prose_objections[{index}]", nonempty=False)
    atoms = argument.get("atoms")
    if not isinstance(atoms, dict) or not atoms:
        problems.append(issue("invalid", "$.atoms", "Expected a nonempty object of atom meanings."))
        atoms = {}
    elif len(atoms) > LIMITS["max_atoms"]:
        problems.append(issue("unsupported", "$.atoms", "Atom count exceeds max_atoms."))
    for atom, meaning in atoms.items():
        if not isinstance(atom, str) or not IDENTIFIER.fullmatch(atom):
            problems.append(issue("invalid", "$.atoms", "Atom names must be bounded ASCII identifiers."))
        text_field(meaning, f"$.atoms.{atom}")

    premises = argument.get("premises")
    if not isinstance(premises, list):
        problems.append(issue("invalid", "$.premises", "Expected a list of identified formulas."))
        premises = []
    elif len(premises) > LIMITS["max_premises"]:
        problems.append(issue("unsupported", "$.premises", "Premise count exceeds max_premises."))
    entries = [(item, f"$.premises[{index}]") for index, item in enumerate(premises)]
    entries.append((argument.get("goal"), "$.goal"))
    identifiers = set()
    total_nodes = 0
    for entry, path in entries:
        if not isinstance(entry, dict) or set(entry) != {"id", "formula"}:
            problems.append(issue("invalid", path, "Expected exactly id and formula fields."))
            continue
        name = entry["id"]
        if not isinstance(name, str) or not IDENTIFIER.fullmatch(name):
            problems.append(issue("invalid", path + ".id", "Formula ID must be a bounded ASCII identifier."))
        elif name in identifiers:
            problems.append(issue("invalid", path + ".id", "Formula IDs must be unique across premises and goal."))
        else:
            identifiers.add(name)
        stack = [(entry["formula"], path + ".formula", 1)]
        node_count, deepest = 0, 0
        while stack:
            node, node_path, depth = stack.pop()
            node_count += 1
            deepest = max(deepest, depth)
            if isinstance(node, str):
                if node not in atoms:
                    problems.append(issue("invalid", node_path, f"Undeclared atom: {node}."))
                continue
            if not isinstance(node, dict) or len(node) != 1:
                problems.append(issue("invalid", node_path, "Formula must be an atom string or a single-operator object."))
                continue
            operator, operands = next(iter(node.items()))
            if operator == "not":
                stack.append((operands, node_path + ".not", depth + 1))
            elif operator in ("and", "or", "implies", "iff"):
                if not isinstance(operands, list):
                    problems.append(issue("invalid", node_path, "This operator requires a formula list."))
                    continue
                if len(operands) < 2 or (operator in ("implies", "iff") and len(operands) != 2):
                    problems.append(issue("invalid", node_path, "and/or require 2+ operands; implies/iff require exactly 2."))
                stack.extend((child, f"{node_path}.{operator}[{index}]", depth + 1)
                             for index, child in reversed(list(enumerate(operands))))
            else:
                problems.append(issue("invalid", node_path, f"Unsupported operator: {operator}."))
        total_nodes += node_count
        if node_count > LIMITS["max_formula_nodes"]:
            problems.append(issue("unsupported", path + ".formula", "Formula exceeds max_formula_nodes."))
        if deepest > LIMITS["max_formula_depth"]:
            problems.append(issue("unsupported", path + ".formula", "Formula exceeds max_formula_depth."))
    if total_nodes > LIMITS["max_total_formula_nodes"]:
        problems.append(issue("unsupported", "$", "Formulas exceed max_total_formula_nodes."))
    return problems


def evaluate(formula: object, valuation: dict[str, bool]) -> bool:
    """Evaluate only a fully validated, bounded formula; never execute input."""
    if isinstance(formula, str):
        return valuation[formula]
    operator, operands = next(iter(formula.items()))
    if operator == "not":
        return not evaluate(operands, valuation)
    values = [evaluate(child, valuation) for child in operands]
    if operator == "and":
        return all(values)
    if operator == "or":
        return any(values)
    if operator == "implies":
        return not values[0] or values[1]
    if operator == "iff":
        return values[0] == values[1]
    raise ValueError("Unvalidated operator")


def feedback(classification: str) -> dict:
    alternatives = {
        "invalid": "Inspect the diagnostic, correct or replace the proposed formal artifact if useful, and continue considering the original prose and objections.",
        "unsupported": "Use a separately identified broader checker or a smaller justified formal scope if useful; the original prose inquiry remains available.",
        "inconsistent": "Scrutinize the listed premises, their meanings, and translation for a source of conflict; keep any proposed revision separate from the original.",
        "entailed": "Scrutinize whether premises and atom meanings capture the original question, including an impossible antecedent or an assumed conclusion; seek an independent prose objection or evidence.",
        "refuted": "Explain the goal-countermodel and scrutinize the premises or mapping before proposing a different claim or seeking contrary evidence.",
        "undetermined": "Compare both countermodels and seek discriminating evidence or a justified distinction in the prose problem; adding a premise needs its own case argument.",
    }
    return {"formal_limit": SCOPE, "possible_next_inquiry": alternatives[classification],
            "inquiry_is_suggestion_only": True, "automatic_problem_promotion": False,
            "semantic_endorsement": False}


def check_argument(argument: object) -> dict:
    problems = validate_argument(argument)
    result = {"checker": CHECKER_VERSION, "limits": dict(LIMITS),
              "original_argument": argument, "issues": problems,
              "valuations_checked": 0, "premise_model_count": None,
              "premise_ids": [], "satisfying_witness": None,
              "goal_countermodel": None, "negation_countermodel": None}
    if problems:
        classification = "invalid" if any(p["kind"] == "invalid" for p in problems) else "unsupported"
    else:
        names = sorted(argument["atoms"])
        premises = argument["premises"]
        goal = argument["goal"]["formula"]
        result["premise_ids"] = [entry["id"] for entry in premises]
        result["premise_model_count"] = 0
        for values in itertools.product((False, True), repeat=len(names)):
            valuation = dict(zip(names, values))
            result["valuations_checked"] += 1
            if not all(evaluate(entry["formula"], valuation) for entry in premises):
                continue
            result["premise_model_count"] += 1
            if result["satisfying_witness"] is None:
                result["satisfying_witness"] = valuation
            target = "negation_countermodel" if evaluate(goal, valuation) else "goal_countermodel"
            if result[target] is None:
                result[target] = valuation
        if result["premise_model_count"] == 0:
            classification = "inconsistent"
        elif result["goal_countermodel"] is None:
            classification = "entailed"
        elif result["negation_countermodel"] is None:
            classification = "refuted"
        else:
            classification = "undetermined"
    result["classification"] = classification
    result["feedback"] = feedback(classification)
    return result


class ContractLoadError(ValueError):
    def __init__(self, kind: str, message: str):
        super().__init__(message)
        self.kind = kind


def load_json(path: Path) -> object:
    with path.open("rb") as handle:
        raw = handle.read(LIMITS["max_input_bytes"] + 1)
    if len(raw) > LIMITS["max_input_bytes"]:
        raise ContractLoadError("unsupported", "Input exceeds max_input_bytes; original input file is retained.")

    def unique_object(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ContractLoadError("invalid", f"Duplicate JSON key: {key}.")
            obj[key] = value
        return obj

    try:
        return json.loads(raw, object_pairs_hook=unique_object,
                          parse_constant=lambda value: (_ for _ in ()).throw(ContractLoadError("invalid", "Nonfinite JSON number.")))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractLoadError("invalid", f"Invalid UTF-8/JSON: {exc}") from exc
    except RecursionError as exc:
        raise ContractLoadError("unsupported", "JSON nesting exceeds parser capacity; original input file is retained.") from exc


def check_file(path: Path) -> dict:
    try:
        result = check_argument(load_json(path))
    except (ContractLoadError, OSError) as exc:
        classification = exc.kind if isinstance(exc, ContractLoadError) else "invalid"
        result = {"checker": CHECKER_VERSION, "limits": dict(LIMITS),
                  "classification": classification, "original_argument": None,
                  "input_retained_at": str(path), "valuations_checked": 0,
                  "issues": [issue(classification, "$", str(exc))],
                  "feedback": feedback(classification)}
    return result


def supplied_revision_replay(draft: object, revision: object) -> dict:
    """Check two explicitly supplied artifacts; generate or accept no repair."""
    return {"provenance": "Operator-supplied replay, not an LLM observation.",
            "revision_generated_by_checker": False,
            "draft": check_argument(draft), "supplied_revision": check_argument(revision),
            "revision_semantically_accepted": False}


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_fixtures(fixture_dir: Path, output: Path) -> dict:
    manifest = load_json(fixture_dir / "manifest.json")
    output.mkdir(parents=True, exist_ok=False)
    results = []
    for entry in manifest["fixtures"]:
        source = fixture_dir / entry["input"]
        result = check_file(source)
        result_name = source.stem + ".result.json"
        write_json(output / result_name, result)
        results.append({"fixture_id": entry["id"], "input": entry["input"],
                        "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                        "expected_classification": entry["expected_classification"],
                        "actual_classification": result["classification"],
                        "expectation_matched": result["classification"] == entry["expected_classification"],
                        "result": result_name})
    summary = {"checker": CHECKER_VERSION,
               "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "fixture_manifest_sha256": hashlib.sha256((fixture_dir / "manifest.json").read_bytes()).hexdigest(),
               "python_version": platform.python_version(), "limits": dict(LIMITS),
               "provenance": manifest["provenance"], "model_calls": 0,
               "finding_scope": "Illustrative instrument diagnostics, not evidence of LLM benefit, semantic adequacy, or creativity.",
               "all_expectations_matched": all(row["expectation_matched"] for row in results),
               "fixtures": results}
    write_json(output / "summary.json", summary)
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Check one explicit argument JSON file.")
    check.add_argument("--input", required=True, type=Path)
    check.add_argument("--output", type=Path)
    fixtures = sub.add_parser("run-fixtures", help="Run operator-authored probes into a new output directory.")
    fixtures.add_argument("--fixtures", required=True, type=Path)
    fixtures.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command == "check":
        result = check_file(args.input)
        if args.output:
            write_json(args.output, result)
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        return 2 if result["classification"] in ("invalid", "unsupported") else 0
    result = run_fixtures(args.fixtures, args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["all_expectations_matched"] else 1


if __name__ == "__main__":
    sys.exit(main())
