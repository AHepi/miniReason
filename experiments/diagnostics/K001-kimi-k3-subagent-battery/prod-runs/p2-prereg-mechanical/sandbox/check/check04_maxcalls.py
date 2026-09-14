"""Check 4: max_calls derivation arithmetic vs config.
 - reading_set.json entry count, per-entry budgeted_calls, per-leg subtotals
 - quoted derivation sentence(s) from PREREG.md (located by computation)
 - compare with config.max_calls and config.cycle_budget
"""
import json
from pathlib import Path

cfg = json.loads(Path("loop-prereg/config.json").read_bytes())
rs = json.loads(Path("loop-prereg/reading_set.json").read_bytes())
pre = Path("loop-prereg/PREREG.md").read_text(encoding="utf-8")

entries = rs["entries"]
marks = [e for e in entries if e["leg"] == "c001-mark"]
rows = [e for e in entries if e["leg"] == "h005-row"]

deriv = rs["max_calls_derivation"]
legs = deriv["legs"]
leg_sum = sum(l["subtotal"] for l in legs)
leg_check = [{
    "leg": l["leg"],
    "cells": l["cells"],
    "cost_each": l["cost_each"],
    "declared_subtotal": l["subtotal"],
    "cells_x_cost": l["cells"] * l["cost_each"],
    "subtotal_consistent": l["cells"] * l["cost_each"] == l["subtotal"],
} for l in legs]

marks_budget = sum(e["budgeted_calls"] for e in marks)
rows_budget = sum(e["budgeted_calls"] for e in rows)
entry_budget_total = sum(e["budgeted_calls"] for e in entries)

h005_cost = deriv["guarded_row_cost_h005"]
c001_cost = deriv["guarded_mark_cost_c001"]
h005_component_sum = sum(v for k, v in h005_cost.items()
                         if isinstance(v, int) and k not in ("total_worst_case", "best_case"))
c001_component_sum = sum(v for k, v in c001_cost.items()
                         if isinstance(v, int) and k != "total_worst_case")

# audit window arithmetic, recomputed from the 'why' components
audit_leg = next(l for l in legs if l["leg"] == "audit window")
audit_components = {"calibration_9x2": 9 * 2,
                    "paraphrase_4_plus_2x2x4": 4 + 2 * 2 * 4,
                    "premise_deletion_2x4": 2 * 4,
                    "ensemble_disagreement": 0}

# sentences in PREREG.md that mention max_calls
n = 0
prereg_sentences = []
for line in pre.splitlines():
    if "max_calls" in line:
        prereg_sentences.append(line.strip())
# clause-5 line in stop rule
clause5 = [l.strip() for l in pre.splitlines() if "max_calls` = 396" in l or "max_calls` = " in l]

report = {
    "reading_set_entries": len(entries),
    "reading_set_size_block": rs["size"],
    "config_reading_set_len": len(cfg["reading_set"]),
    "config_max_calls": cfg["max_calls"],
    "config_cycle_budget": cfg["cycle_budget"],
    "c001_mark_entries": len(marks),
    "h005_row_entries": len(rows),
    "marks_budgeted_calls_sum": marks_budget,
    "rows_budgeted_calls_sum": rows_budget,
    "entries_budgeted_calls_sum": entry_budget_total,
    "per_leg_check": leg_check,
    "leg_subtotal_sum": leg_sum,
    "derivation_max_calls_field": deriv["max_calls"],
    "derivation_arithmetic_string": deriv["arithmetic"],
    "leg_sum_equals_max_calls": leg_sum == deriv["max_calls"] == cfg["max_calls"],
    "h005_row_cost_components_sum_to_total": (h005_component_sum, h005_cost["total_worst_case"],
                                              h005_component_sum == h005_cost["total_worst_case"]),
    "c001_mark_cost_components_sum_to_total": (c001_component_sum, c001_cost["total_worst_case"],
                                               c001_component_sum == c001_cost["total_worst_case"]),
    "audit_components_recomputed": audit_components,
    "audit_components_sum": sum(audit_components.values()),
    "audit_leg_declared": audit_leg["subtotal"],
    "deviation_note_in_reading_set": h005_cost["deviation_from_design"],
    "prereg_lines_mentioning_max_calls": prereg_sentences,
    "prereg_clause5_lines": clause5,
}
Path("out/check4-maxcalls.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
