import itertools
import json

labels = "ABCDEFG"

def slot_map(order):
    return {label: index + 1 for index, label in enumerate(order)}

def local_rules(slots):
    return (
        slots["F"] == slots["A"] + 1
        and slots["C"] == slots["F"] + 2
        and slots["G"] == slots["C"] + 1
        and slots["B"] > slots["G"]
    )

def inclusive_span(slots, left, right):
    return abs(slots[left] - slots[right]) + 1

local_candidates = []
solutions = []
span_diagnostics = {}
for order in itertools.permutations(labels):
    slots = slot_map(order)
    if not local_rules(slots):
        continue
    text = "".join(order)
    local_candidates.append(text)
    pair = [inclusive_span(slots, "A", "B"), inclusive_span(slots, "D", "G")]
    span_diagnostics[text] = pair
    if pair[0] == pair[1]:
        solutions.append(text)

expected_local = ["AFDCGBE", "AFDCGEB", "AFECGBD", "AFECGDB", "DAFECGB", "EAFDCGB"]
assert local_candidates == expected_local
assert solutions == ["DAFECGB"]

payload = {
    "problem_id": "P06",
    "answer": solutions[0],
    "diagnostics": {
        "local_candidate_count": len(local_candidates),
        "local_candidates": local_candidates,
        "span_pairs_ab_dg": span_diagnostics,
        "full_solution_count": len(solutions),
    },
}
print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
