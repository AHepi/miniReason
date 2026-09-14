#!/usr/bin/env python3
"""Usage and envelope profile of C001 occurrence-02.

Reads the twenty receipt records under

    experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/

and writes the profile to out/occ02-usage.md.

Everything computed here is a resource observation: statuses, finish
reasons, token totals and ranges, the per-call reasoning share of the
completion budget, a count against the 8,192-token ceiling the same
endpoint ran under in occurrence-01, prompt token totals, envelope
repairs, strict-parse flags and failure codes. No semantic claim is
made. Ranges are reported instead of medians or means.

Run with:  python3 check/occ02_usage.py
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESP = ROOT / "experiments/diagnostics/C001-contrast-triple/occurrence-02/responses"
OUT = ROOT / "out/occ02-usage.md"
CEILING = 8192  # completion-token ceiling this endpoint ran under in occurrence-01

FAILURE_FIELDS = (
    "failure_class",
    "failure_type",
    "validation_failure_class",
    "validation_failure_type",
    "unresolved_reason",
)


def coord(rec):
    c = rec.get("coordinate", {})
    return "{endpoint}/{arm}/{case}/rep{n}".format(
        endpoint=c.get("endpoint_slug", "?"),
        arm=c.get("arm", "?"),
        case=c.get("case", "?"),
        n=c.get("replicate", "?"),
    )


def fmt(n):
    return f"{n:,}"


def fmtval(v, places):
    if places is not None:
        return f"{v:.{places}f}"
    return fmt(v)


def extremum_note(values, label, places=None):
    """Describe which single removals move the range of `values`."""
    lo, hi = min(values), max(values)
    lo_n = sum(1 for v in values if v == lo)
    hi_n = sum(1 for v in values if v == hi)
    if lo == hi:
        return f"every removal leaves the {label} unchanged (all values are equal)"
    parts = []
    if lo_n == 1:
        parts.append(f"removing the sole minimum holder ({fmtval(lo, places)}) moves its lower end")
    else:
        parts.append(f"no single removal moves its lower end ({lo_n} records sit at the minimum {fmtval(lo, places)})")
    if hi_n == 1:
        parts.append(f"removing the sole maximum holder ({fmtval(hi, places)}) moves its upper end")
    else:
        parts.append(f"no single removal moves its upper end ({hi_n} records sit at the maximum {fmtval(hi, places)})")
    return f"{label}: " + "; ".join(parts)


def main():
    paths = sorted(RESP.rglob("*.json"))
    records = [(p, json.loads(p.read_text(encoding="utf-8"))) for p in paths]

    rows = []
    for path, rec in records:
        usage = rec.get("usage") or {}
        details = usage.get("completion_tokens_details") or {}
        completion = usage.get("completion_tokens")
        reasoning = details.get("reasoning_tokens")
        prompt = usage.get("prompt_tokens")
        share = None
        if isinstance(completion, (int, float)) and completion and isinstance(reasoning, (int, float)):
            share = reasoning / completion
        rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "coord": coord(rec),
                "status": rec.get("status"),
                "finish_reason": rec.get("finish_reason"),
                "envelope_status": rec.get("envelope_status"),
                "envelope_repairs": rec.get("envelope_repairs") or [],
                "strict": rec.get("strict_parse_would_succeed"),
                "timeout": rec.get("timeout_seconds"),
                "completion": completion,
                "reasoning": reasoning,
                "prompt": prompt,
                "share": share,
                "failures": {f: rec.get(f) for f in FAILURE_FIELDS if rec.get(f) is not None},
            }
        )

    n = len(rows)
    status_counts = Counter(r["status"] for r in rows)
    finish_counts = Counter(r["finish_reason"] for r in rows)
    envelope_status_counts = Counter(r["envelope_status"] for r in rows)
    timeout_counts = Counter(r["timeout"] for r in rows)

    completions = [r["completion"] for r in rows if isinstance(r["completion"], (int, float))]
    reasonings = [r["reasoning"] for r in rows if isinstance(r["reasoning"], (int, float))]
    prompts = [r["prompt"] for r in rows if isinstance(r["prompt"], (int, float))]
    shares = [r["share"] for r in rows if r["share"] is not None]

    comp_total = sum(completions)
    comp_min, comp_max = min(completions), max(completions)
    comp_min_rows = [r for r in rows if r["completion"] == comp_min]
    comp_max_rows = [r for r in rows if r["completion"] == comp_max]

    reason_total = sum(reasonings)
    reason_min, reason_max = min(reasonings), max(reasonings)
    reason_min_rows = [r for r in rows if r["reasoning"] == reason_min]
    reason_max_rows = [r for r in rows if r["reasoning"] == reason_max]

    share_min, share_max = min(shares), max(shares)
    share_min_rows = [r for r in rows if r["share"] == share_min]
    share_max_rows = [r for r in rows if r["share"] == share_max]

    over_ceiling = [r for r in rows if isinstance(r["completion"], (int, float)) and r["completion"] > CEILING]
    prompt_total = sum(prompts)

    repaired = [r for r in rows if r["envelope_repairs"]]
    strict_true = [r for r in rows if r["strict"] is True]
    strict_other = [r for r in rows if r["strict"] is not True]

    failure_counter = Counter()
    for r in rows:
        for field, value in r["failures"].items():
            failure_counter[f"{field}={value}"] += 1

    lines = []
    a = lines.append
    a("# C001 occurrence-02 — usage and envelope profile")
    a("")
    a("Source: the twenty receipt records under")
    a("`experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/`")
    a("(`<endpoint_slug>/<arm>/<case>/rep<n>.json`). Computed by")
    a("`check/occ02_usage.py`, run as `python3 check/occ02_usage.py`; every figure below")
    a("was computed by that script from those records.")
    a("")
    a("These are resource observations only. A reasoning share is a fact about how a")
    a("completion budget was spent, not a merit figure. The 8,192 comparison is against")
    a("the completion-token ceiling the same endpoint ran under in occurrence-01, not")
    a("against another family. Ranges are reported rather than medians or means: a")
    a("median convention is a choice and the range is not.")
    a("")
    a("## Receipts, statuses, finish reasons")
    a("")
    a(f"- Receipts: {n} (expected grid: 1 endpoint × 1 arm × 4 cases × 5 replicates = 20).")
    a("- `status`: " + ", ".join(f"{k} × {v}" for k, v in sorted(status_counts.items())))
    a("- `finish_reason`: " + ", ".join(f"{k} × {v}" for k, v in sorted(finish_counts.items())))
    a("")
    a("## Completion tokens (`usage.completion_tokens`)")
    a("")
    a(f"- Total over {len(completions)} calls: {fmt(comp_total)}.")
    a(
        f"- Range: {fmt(comp_min)} ({', '.join(r['coord'] for r in comp_min_rows)})"
        f" to {fmt(comp_max)} ({', '.join(r['coord'] for r in comp_max_rows)})."
    )
    a("")
    a("## Reasoning tokens (`usage.completion_tokens_details.reasoning_tokens`)")
    a("")
    a(f"- Total over {len(reasonings)} calls: {fmt(reason_total)}.")
    a(
        f"- Range: {fmt(reason_min)} ({', '.join(r['coord'] for r in reason_min_rows)})"
        f" to {fmt(reason_max)} ({', '.join(r['coord'] for r in reason_max_rows)})."
    )
    a("")
    a("## Per-call reasoning share of the completion")
    a("")
    a("`reasoning_tokens / completion_tokens`, reported as a range over the twenty")
    a("calls, not an average:")
    a("")
    a(
        f"- {share_min:.4f} ({', '.join(r['coord'] for r in share_min_rows)})"
        f" to {share_max:.4f} ({', '.join(r['coord'] for r in share_max_rows)})."
    )
    a("")
    a(f"## Calls exceeding {fmt(CEILING)} completion tokens")
    a("")
    a(
        f"- {len(over_ceiling)} of {n}. {fmt(CEILING)} is the completion-token ceiling the"
        " same endpoint ran under in occurrence-01; the comparison is to that ceiling"
        " and to nothing else."
    )
    if over_ceiling:
        for r in sorted(over_ceiling, key=lambda r: r["completion"], reverse=True):
            a(f"  - {r['coord']}: {fmt(r['completion'])}")
    a("")
    a("## Prompt tokens (`usage.prompt_tokens`)")
    a("")
    a(f"- Total over {len(prompts)} calls: {fmt(prompt_total)}.")
    a("")
    a("## Envelope")
    a("")
    a("- `envelope_status`: " + ", ".join(f"{k} × {v}" for k, v in sorted(envelope_status_counts.items())))
    if repaired:
        a(f"- Non-empty `envelope_repairs`: {len(repaired)} of {n}.")
        for r in repaired:
            a(f"  - {r['coord']}: {json.dumps(r['envelope_repairs'], ensure_ascii=False)}")
    else:
        a(f"- Non-empty `envelope_repairs`: 0 of {n}; no receipt carries any repair.")
    a(
        f"- `strict_parse_would_succeed`: true × {len(strict_true)}"
        + "".join(f"; false ({r['coord']})" for r in strict_other)
        + "."
    )
    a(
        "- `timeout_seconds`: "
        + ", ".join(f"{k} × {v}" for k, v in sorted(timeout_counts.items(), key=lambda kv: str(kv[0])))
    )
    a("")
    a("## Failure codes")
    a("")
    if failure_counter:
        for code, count in sorted(failure_counter.items()):
            carriers = [r["coord"] for r in rows if any(f"{f}={v}" == code for f, v in r["failures"].items())]
            a(f"- `{code}` × {count} ({', '.join(carriers)})")
    else:
        a(
            "- None present. In every record `failure_class`, `failure_type`,"
            " `validation_failure_class`, `validation_failure_type` and"
            " `unresolved_reason` are null."
        )
    a("")
    a("## Sensitivity to a single missing record")
    a("")
    a("Which figures would change if one of the twenty records were missing:")
    a("")
    a("Would change:")
    a("- Receipt count (20 → 19), for any removal.")
    a(
        "- `status` and `finish_reason` counts, for any removal: the missing record's"
        " value-count drops by one. (The set of distinct values would survive any"
        " single removal here, since every observed value appears more than once.)"
        if all(v > 1 for v in status_counts.values()) and all(v > 1 for v in finish_counts.values())
        else "- `status` and `finish_reason` counts, for any removal; a value appearing only once would also leave the distinct-value set."
    )
    a(
        "- Total completion tokens, total reasoning tokens and total prompt tokens,"
        " for any removal: every value is positive, so each total drops by the"
        " missing record's value."
    )
    if over_ceiling:
        a(
            f"- The over-{fmt(CEILING)} completion-token count changes if and only if the"
            f" missing record is one of the {len(over_ceiling)} calls listed above; a"
            " removal at or below the ceiling leaves it unchanged."
        )
    else:
        a(
            f"- The over-{fmt(CEILING)} completion-token count is 0 and no single removal"
            " can change that."
        )
    if 0 < len(strict_true) < n:
        a(
            f"- The `strict_parse_would_succeed`-true count changes if and only if the"
            f" missing record is one of the {len(strict_true)} true cases."
        )
    elif len(strict_true) == n:
        a(f"- The `strict_parse_would_succeed`-true count (currently {len(strict_true)}) changes for any removal.")
    else:
        a("- The `strict_parse_would_succeed`-true count is 0 and no single removal can change that.")
    if repaired:
        a(
            f"- The envelope-repair count changes if and only if the missing record is the"
            f" repair carrier ({', '.join(r['coord'] for r in repaired)})."
            if len(repaired) == 1
            else
            f"- The envelope-repair count changes if and only if the missing record is one"
            f" of the {len(repaired)} repair carriers."
        )
    else:
        a("- The envelope-repair count is 0 and no single removal can change that.")
    if failure_counter:
        sole = [c for c, k in failure_counter.items() if k == 1]
        a(
            "- The failure-code set changes if and only if the missing record is the sole"
            f" carrier of a code; sole-carrier codes here: {', '.join(sole) if sole else 'none'}."
        )
    a("")
    a("Would change only for a specific removal (computed from the current extremum")
    a("holders):")
    a(f"- {extremum_note(completions, 'Completion-token range')}.")
    a(f"- {extremum_note(reasonings, 'Reasoning-token range')}.")
    a(f"- {extremum_note(shares, 'Reasoning-share range', places=4)}.")
    a("")
    a("Would not change:")
    a(f"- The comparison ceiling itself ({fmt(CEILING)}), which is occurrence-01's value,")
    a("  not a quantity computed from these records.")
    if all(v > 1 for v in status_counts.values()):
        a("- The set of distinct `status` values (every value appears more than once).")
    if all(v > 1 for v in finish_counts.values()):
        a("- The set of distinct `finish_reason` values (every value appears more than once).")
    a(f"- The {fmt(CEILING)}-exceedance status of any record that is not removed.")
    a("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")

    summary = {
        "receipts": n,
        "status": dict(sorted(status_counts.items())),
        "finish_reason": dict(sorted(finish_counts.items())),
        "completion_total": comp_total,
        "completion_range": [comp_min, comp_max],
        "reasoning_total": reason_total,
        "reasoning_range": [reason_min, reason_max],
        "share_range": [round(share_min, 6), round(share_max, 6)],
        f"over_{CEILING}": len(over_ceiling),
        "prompt_total": prompt_total,
        "repaired": len(repaired),
        "strict_true": len(strict_true),
        "failure_codes": dict(sorted(failure_counter.items())),
        "wrote": OUT.relative_to(ROOT).as_posix(),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
