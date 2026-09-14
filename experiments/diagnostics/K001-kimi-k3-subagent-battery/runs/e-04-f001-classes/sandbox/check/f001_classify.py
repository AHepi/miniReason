# check/f001_classify.py
#
# Classifies every unresolved coordinate of the F001-fork5-multifamily study
# from its records and writes out/f001-classes.md.
#
# Run:  python3 check/f001_classify.py
#
# What it computes (nothing is read off prose):
#   * the planned coordinate set, derived per occurrence from
#     arms.json/plan.json (arms, kind, scope) and manifests/fork5.json
#     (the model-called node sequence of the mini template);
#   * the receipt map under responses/<problem>/<arm>/cycle01/<node>.json;
#   * the class of every coordinate whose state is not COMPLETE:
#       ceiling   -- finish_reason == "length" at exactly the arm's declared
#                    max_tokens ceiling (a partial delivery still counts);
#       timeout   -- a transport failure whose error is a read timeout at an
#                    elapsed time at the declared timeout_seconds;
#       blocked   -- planned but never dispatched: no receipt at all, and an
#                    earlier node of the same arm is FAILED (the no-retry
#                    truncation rule ended the arm);
#       unclassified -- the record does not settle a class; stated, not guessed.
#
# Evidence note: this sandbox copy of the study contains the receipts, arms,
# plans and the manifest only.  Provider call records, attempt markers and raw
# response text files are not part of this copy, so the receipt schema is the
# whole evidence for per-call fields.  The union of receipt keys (printed to
# stdout at run time, computed over every receipt) contains no elapsed-time
# field and no error text; raw-content byte counts for the seven
# ceiling-truncated coordinates of occurrences 04/05 exist only in the
# published table appended to PLAN.md ("Why: what occurrence-04 and
# occurrence-05 actually recorded", the raw `responses/*.txt` column,
# sandbox-file lines 431-437), so those seven cells are quoted from that
# record and say so in place.

import json
import os
import sys
from collections import OrderedDict

STUDY = os.path.join("experiments", "diagnostics", "F001-fork5-multifamily")
MANIFEST = os.path.join(STUDY, "manifests", "fork5.json")
PLAN_MD = os.path.join(STUDY, "PLAN.md")
OUT = os.path.join("out", "f001-classes.md")

SINGLE_NODE = "answer"  # bare/native single call; the node name on every bare/native receipt

# Raw-content byte counts as published in PLAN.md (the only record of them in
# this copy of the study).  Key: (occurrence, arm, node).
PLAN_MD_CONTENT_BYTES = {
    ("occurrence-04", "mini_fcl", "objection"): "0 (per PLAN.md table, raw `responses/*.txt` column)",
    ("occurrence-04", "mini_fcl", "rival"): "0 (per PLAN.md table, raw `responses/*.txt` column)",
    ("occurrence-04", "mini_prose", "objection"): "288 (per PLAN.md table, raw `responses/*.txt` column)",
    ("occurrence-04", "mini_prose", "response"): "0 (per PLAN.md table, raw `responses/*.txt` column)",
    ("occurrence-05", "mini_fcl", "response"): "0 (per PLAN.md table, raw `responses/*.txt` column)",
    ("occurrence-05", "mini_fcl", "rival"): "7112 (per PLAN.md table, raw `responses/*.txt` column)",
    ("occurrence-05", "mini_prose", "carry"): "0 (per PLAN.md table, raw `responses/*.txt` column)",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def mini_node_sequence():
    """Model-called stages of the fork5 template, in template order.

    A stage is model-called here iff its entry carries no "seat" (machine
    stages: the task and the p.* projections) and is not the 'end' marker.
    """
    manifest = load_json(MANIFEST)
    seq = [
        s["stage_id"]
        for s in manifest["stages"]
        if "seat" not in s and not s.get("end")
    ]
    return seq


def planned_coordinates(occ_dir):
    """The coordinates the plan authorises for one occurrence."""
    arms = load_json(os.path.join(occ_dir, "arms.json"))["arms"]
    plan = load_json(os.path.join(occ_dir, "plan.json"))
    scope = plan["scope"]
    nodes_mini = mini_node_sequence()
    planned = []
    for arm in sorted(arms):
        kind = arms[arm]["kind"]
        nodes = nodes_mini if kind == "mini" else [SINGLE_NODE]
        for problem in scope["problems"]:
            for cycle in scope["cycles"]:
                for node in nodes:
                    planned.append(
                        {
                            "problem": problem,
                            "arm": arm,
                            "cycle": cycle,
                            "node": node,
                            "kind": kind,
                        }
                    )
    return plan, planned


def receipt_path(occ_dir, coord):
    return os.path.join(
        occ_dir,
        "responses",
        coord["problem"],
        coord["arm"],
        "cycle%02d" % coord["cycle"],
        coord["node"] + ".json",
    )


def cell(value):
    """Render one table cell, quoting a JSON null literally."""
    if value is None:
        return "null"
    return str(value)


def main():
    # ---- collect -----------------------------------------------------------
    occurrences = sorted(
        d
        for d in os.listdir(STUDY)
        if os.path.isdir(os.path.join(STUDY, d)) and d.startswith("occurrence-")
    )
    all_receipt_keys = set()
    occ_data = OrderedDict()
    for occ in occurrences:
        occ_dir = os.path.join(STUDY, occ)
        plan, planned = planned_coordinates(occ_dir)
        rows = []
        for coord in planned:
            path = receipt_path(occ_dir, coord)
            if os.path.isfile(path):
                receipt = load_json(path)
                all_receipt_keys.update(receipt.keys())
            else:
                receipt = None
            rows.append({"coord": coord, "receipt": receipt, "path": path})
        occ_data[occ] = {"plan": plan, "planned": planned, "rows": rows}

    # The mini node sequence is also confirmed by the mini-arm receipts
    # themselves (every mini receipt node is in the sequence).
    nodes_mini = mini_node_sequence()
    for occ, data in occ_data.items():
        for row in data["rows"]:
            c = row["coord"]
            if c["kind"] == "mini" and row["receipt"] is not None:
                assert row["receipt"]["coordinate"]["node"] in nodes_mini, (occ, c)
                assert c["node"] in nodes_mini, (occ, c)

    # ---- classify ----------------------------------------------------------
    # A coordinate is unresolved iff its receipt status is not COMPLETE, or it
    # has no receipt at all (planned but never dispatched).
    unresolved = []
    for occ, data in occ_data.items():
        plan = data["plan"]
        for row in data["rows"]:
            coord = row["coord"]
            receipt = row["receipt"]
            ceiling = plan["ceilings"][coord["arm"]]["max_tokens"]
            timeout_seconds = plan["ceilings"][coord["arm"]]["timeout_seconds"]
            arm = plan["arms"][coord["arm"]]
            entry = {
                "occurrence": occ,
                "endpoint": arm["endpoint"],
                "ceiling": ceiling,
                "timeout_seconds": timeout_seconds,
                "arm": coord["arm"],
                "cycle": coord["cycle"],
                "node": coord["node"],
                "kind": coord["kind"],
                "status": None,
                "failure_code": None,
                "finish_reason": None,
                "completion_tokens": None,
                "content_bytes": "not recorded (the receipt schema carries no such field)",
                "elapsed_ms": "not recorded (no record in this copy carries one)",
                "cls": None,
                "evidence_gap": None,
                "truncated_by": None,
                "truncated_by_code": None,
                "truncated_by_reason": None,
                "runner_sha256_8": plan["runner_sha256"][:8],
            }
            if receipt is None:
                # blocked requires: no receipt AND an earlier node of the same
                # arm already FAILED (the no-retry truncation rule).
                earlier_failed = None
                if coord["kind"] == "mini":
                    idx = nodes_mini.index(coord["node"])
                    for prior in nodes_mini[:idx]:
                        prior_row = next(
                            r
                            for r in data["rows"]
                            if r["coord"]["arm"] == coord["arm"]
                            and r["coord"]["node"] == prior
                        )
                        if (
                            prior_row["receipt"] is not None
                            and prior_row["receipt"].get("status") == "FAILED"
                        ):
                            earlier_failed = prior
                            entry["truncated_by_code"] = prior_row["receipt"].get(
                                "failure_code"
                            )
                            entry["truncated_by_reason"] = prior_row["receipt"].get(
                                "finish_reason"
                            )
                            break
                if earlier_failed is not None:
                    entry["cls"] = "blocked"
                    entry["truncated_by"] = earlier_failed
                    entry["status"] = "no receipt"
                    entry["failure_code"] = "no record"
                    entry["finish_reason"] = "no record"
                    entry["completion_tokens"] = "no record"
                    entry["content_bytes"] = "no record"
                else:
                    entry["cls"] = "unclassified"
                    entry["status"] = "no receipt"
                    entry["evidence_gap"] = (
                        "planned coordinate with no receipt and no earlier "
                        "FAILED node in its arm; the record does not show why "
                        "it was not dispatched"
                    )
                unresolved.append(entry)
                continue

            status = receipt.get("status")
            if status == "COMPLETE":
                continue  # ok; not part of the unresolved table

            usage = receipt.get("usage") or {}
            entry["status"] = status
            entry["failure_code"] = receipt.get("failure_code")
            entry["finish_reason"] = receipt.get("finish_reason")
            entry["completion_tokens"] = (
                usage.get("completion_tokens")
                if receipt.get("usage") is not None
                else None
            )
            is_ceiling = (
                receipt.get("finish_reason") == "length"
                and receipt.get("usage") is not None
                and usage.get("completion_tokens") == ceiling
            )
            if is_ceiling:
                entry["cls"] = "ceiling"
                key = (occ, coord["arm"], coord["node"])
                if key in PLAN_MD_CONTENT_BYTES:
                    entry["content_bytes"] = PLAN_MD_CONTENT_BYTES[key]
            else:
                # timeout would need: a transport failure whose error is a
                # read timeout AND an elapsed time at the declared
                # timeout_seconds.  The union of receipt keys carries no
                # elapsed-time field and no error text.
                entry["cls"] = "unclassified"
                entry["evidence_gap"] = (
                    "FAILED with failure_type=%s, failure_code=%s, "
                    "finish_reason=null, usage=null. `ceiling` is excluded: "
                    "finish_reason is null and usage is null (nothing shows "
                    "the declared ceiling of %d was met). `timeout` is not "
                    "settled: the class requires an error that is a read "
                    "timeout at an elapsed time of %d s, and the receipt "
                    "carries neither an error text nor an elapsed time (the "
                    "key union over all receipts has no such field). Left "
                    "unclassified rather than guessed."
                    % (
                        receipt.get("failure_type"),
                        receipt.get("failure_code"),
                        ceiling,
                        entry["timeout_seconds"],
                    )
                )
            unresolved.append(entry)

    # ---- integrity assertions ---------------------------------------------
    planned_total = sum(len(d["planned"]) for d in occ_data.values())
    receipt_total = sum(
        1 for d in occ_data.values() for r in d["rows"] if r["receipt"] is not None
    )
    blocked = [e for e in unresolved if e["cls"] == "blocked"]
    ceilings_hits = [e for e in unresolved if e["cls"] == "ceiling"]
    timeouts = [e for e in unresolved if e["cls"] == "timeout"]
    unclassified = [e for e in unresolved if e["cls"] == "unclassified"]
    for occ, data in occ_data.items():
        assert data["plan"]["max_calls"] == len(data["planned"]), occ
    assert planned_total == receipt_total + len(
        [r for d in occ_data.values() for r in d["rows"] if r["receipt"] is None]
    )
    # every ceiling row really sits at its arm's declared ceiling
    for e in ceilings_hits:
        assert e["completion_tokens"] == e["ceiling"], e
    # whole-study cross-checks used in the report
    counts_by_status = {}
    for d in occ_data.values():
        for r in d["rows"]:
            if r["receipt"] is not None:
                s = r["receipt"]["status"]
                counts_by_status[s] = counts_by_status.get(s, 0) + 1
    length_total = sum(
        1
        for d in occ_data.values()
        for r in d["rows"]
        if r["receipt"] is not None and r["receipt"].get("finish_reason") == "length"
    )
    assert length_total == len(ceilings_hits), (length_total, len(ceilings_hits))

    # ---- report ------------------------------------------------------------
    lines = []
    add = lines.append

    add("# F001-fork5-multifamily — classification of unresolved coordinates")
    add("")
    add("Computed by `check/f001_classify.py` (run: `python3 check/f001_classify.py`)")
    add("from the records under `experiments/diagnostics/F001-fork5-multifamily/`.")
    add("Every value below traces to a named record; the same command prints its")
    add("integrity cross-checks and totals to stdout.")
    add("")
    add("This is a classification, not a comparison. A completion-token ceiling,")
    add("a wall clock and the no-retry truncation rule are resource boundaries;")
    add("none of them is exhaustion of the inquiry, and none of them says")
    add("anything about how any family reasons. No ordering of endpoints, no")
    add("reliability claim and no failure rate is made or implied by these rows.")
    add("Endpoints and occurrences are independent occasions.")
    add("")

    # planned set
    add("## Planned coordinate set (derived)")
    add("")
    add("Derivation. Each occurrence's `plan.json` freezes the scope")
    add("`{\"problems\": [\"daily\"], \"cycles\": [1]}`. For every arm in its")
    add("`arms.json`: an arm of `kind: \"mini\"` is planned once per model-called")
    add("node of the fork5 template; `kind: \"bare\"` and `kind: \"native\"` are")
    add("single calls (node `answer`). The model-called node sequence is taken")
    add("from `manifests/fork5.json` as the stages that carry no machine `seat`")
    add("and are not the `end` marker: "
        + ", ".join("`%s`" % n for n in nodes_mini)
        + ". The same sequence is confirmed by the receipts themselves (every")
    add("mini-arm receipt node is one of these five). A planned coordinate with")
    add("no receipt at `responses/daily/<arm>/cycle01/<node>.json` was never")
    add("dispatched.")
    add("")
    add("| Occurrence | Runner (sha256 prefix) | Arms | Coordinates per arm | Planned | `plan.max_calls` | Receipts present | No receipt |")
    add("|---|---|---|---|---|---|---|---|")
    for occ, data in occ_data.items():
        plan = data["plan"]
        arms = plan["arms"]
        per_arm = []
        for name in sorted(arms):
            n = len(nodes_mini) if arms[name]["kind"] == "mini" else 1
            per_arm.append("%s ×%d" % (name, n))
        receipts_here = sum(1 for r in data["rows"] if r["receipt"] is not None)
        add(
            "| %s | %s | %d | %s | %d | %d | %d | %d |"
            % (
                occ,
                plan["runner_sha256"][:8],
                len(arms),
                ", ".join(per_arm),
                len(data["planned"]),
                plan["max_calls"],
                receipts_here,
                len(data["planned"]) - receipts_here,
            )
        )
    add(
        "| **total** |  |  |  | **%d** | **%d** | **%d** | **%d** |"
        % (
            planned_total,
            sum(d["plan"]["max_calls"] for d in occ_data.values()),
            receipt_total,
            planned_total - receipt_total,
        )
    )
    add("")
    add(
        "Total planned coordinates: **%d** = 12 (occurrence-01: `bare`, `native`,"
        % planned_total
    )
    add("plus two 5-node mini arms) + 7 × 11 (occurrences 02–08: `bare` plus two")
    add("5-node mini arms) — the script asserts each equals the frozen")
    add("`plan.max_calls` of its occurrence. This agrees with the register's own")
    add("arithmetic in `PLAN.md`: 67 for occurrences 01–06 under runner v1")
    add("(sha256 prefix `a56fed41`, arm ceiling 8,192) plus 22 for occurrences")
    add("07–08 under runner v2 (`8f7eb9d7`, arm ceiling 32,768). A coordinate's")
    add("declared ceiling and timeout below are the arm's `max_tokens` and")
    add("`timeout_seconds` from its occurrence's `plan.json` ceilings; the")
    add("timeout is 180 s on every arm of every occurrence.")
    add("")

    # classes
    add("## The three classes and their evidence")
    add("")
    add("* `ceiling` — the call met its declared completion-token ceiling:")
    add("  `finish_reason` is `length` at exactly the arm's `max_tokens`. A")
    add("  partial delivery still counts as `ceiling` if that is what ended it.")
    add("* `timeout` — the call was refused by the wall clock: a transport")
    add("  failure whose error is a read timeout, at an elapsed time at the")
    add("  declared `timeout_seconds` (180 s on every arm here).")
    add("* `blocked` — the coordinate was never dispatched: the no-retry")
    add("  truncation rule ended its arm at an earlier node. There is no receipt")
    add("  at all.")
    add("")
    add("A coordinate whose record does not settle one of these is left")
    add("unclassified, with the gap stated — it is not guessed.")
    add("")

    # main table
    add("## Unresolved coordinates — one row per coordinate not in state `ok`")
    add("")
    add("`ok` is read as receipt status `COMPLETE`. Unresolved therefore means:")
    add("a receipt with status `PARTIAL` or `FAILED`, or a planned coordinate")
    add("with no receipt. Receipts found in this copy: %d (%s). Unresolved: **%d**."
        % (
            receipt_total,
            ", ".join("%s %d" % (k, counts_by_status[k]) for k in sorted(counts_by_status)),
            len(unresolved),
        ))
    add("")
    add("Every populated cell is taken from the record named. `no receipt` /")
    add("`no record` / `not recorded` means the field does not exist in this")
    add("copy of the study; nothing is inferred into it. `null` is the receipt's")
    add("own JSON null, quoted literally. Receipts carry no elapsed-time field")
    add("and no content-byte count; the seven `ceiling` rows' content bytes are")
    add("quoted from the published raw-`responses/*.txt` table in the register's")
    add("appendix (`PLAN.md`, \"Why: what occurrence-04 and occurrence-05")
    add("actually recorded\"), the only record of those bytes in this copy, and")
    add("each such cell says so.")
    add("")
    add("| occurrence | endpoint | ceiling (max_tokens) | arm | cycle | node | class | status | failure_code | finish_reason | completion tokens | content bytes | elapsed ms |")
    add("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for e in unresolved:
        if e["cls"] == "unclassified" and e["status"] != "no receipt":
            ct = "null (usage is null)"
        else:
            ct = cell(e["completion_tokens"])
        add(
            "| %s | %s | %d | %s | %d | %s | %s | %s | %s | %s | %s | %s | %s |"
            % (
                e["occurrence"],
                e["endpoint"],
                e["ceiling"],
                e["arm"],
                e["cycle"],
                e["node"],
                e["cls"],
                e["status"],
                cell(e["failure_code"]),
                cell(e["finish_reason"]),
                ct,
                e["content_bytes"],
                e["elapsed_ms"],
            )
        )
    add("")
    add("Receipt paths: `responses/daily/<arm>/cycle01/<node>.json` under the")
    add("row's occurrence directory. The two `PARTIAL` rows carry")
    add("`envelope_status: OPAQUE`; per the register, a partial delivery is")
    add("preserved, usable, never retried and never relabelled.")
    add("")

    # blocked evidence
    add("## `blocked` coordinates: the earlier FAILED node that ended the arm")
    add("")
    add("The truncation rule is declared in the register (`PLAN.md`, \"Resource")
    add("boundary and dispatch discipline\"): one FAILED node ends that arm for")
    add("the rest of the occurrence, and every node's failure policy in")
    add("`manifests/fork5.json` is `action: stop, retries: 0, tolerance: 0`.")
    add("Each blocked coordinate below has no receipt, and an earlier node of")
    add("the same arm carries a FAILED receipt. Round-mates in one wave are")
    add("dispatched together (PLAN.md's measured cadence puts `objection` and")
    add("`rival` of both mini arms in one round, `response` and `carry` in")
    add("later rounds), which is why an arm can hold more than one FAILED")
    add("receipt — e.g. occurrence-04 `mini_fcl` objection and rival.")
    add("")
    add("| occurrence | blocked coordinate | arm | earliest earlier FAILED node | its receipt | that receipt's failure_code / finish_reason | its class above |")
    add("|---|---|---|---|---|---|---|")
    for e in blocked:
        other = next(
            u
            for u in unresolved
            if u["occurrence"] == e["occurrence"]
            and u["arm"] == e["arm"]
            and u["node"] == e["truncated_by"]
        )
        add(
            "| %s | %s/cycle01/%s | %s | %s | responses/daily/%s/cycle01/%s.json | %s / %s | %s |"
            % (
                e["occurrence"],
                e["arm"],
                e["node"],
                e["arm"],
                e["truncated_by"],
                e["arm"],
                e["truncated_by"],
                cell(e["truncated_by_code"]),
                cell(e["truncated_by_reason"]),
                other["cls"],
            )
        )
    add("")
    add("On occurrence-07 the ending node is itself unclassified (see below):")
    add("the truncation evidence there is a FAILED receipt with")
    add("`failure_code: TRANSPORT_OR_RESPONSE_ERROR`, not a ceiling hit. The")
    add("`blocked` class does not depend on *why* the earlier node failed — only")
    add("on the recorded FAILED terminal and the declared no-retry rule.")
    add("")

    # unclassified
    add("## Coordinates left unclassified — the evidence gap, stated")
    add("")
    if unclassified:
        add("These do not meet `ceiling` (their `finish_reason` is null and")
        add("`usage` is null) and the record in this copy does not settle")
        add("`timeout`. They are reported unresolved, not guessed:")
        add("")
        for e in unclassified:
            add(
                "* `%s` `daily/%s/cycle01/%s` (endpoint `%s`, ceiling %d,"
                % (
                    e["occurrence"],
                    e["arm"],
                    e["node"],
                    e["endpoint"],
                    e["ceiling"],
                )
            )
            add("  timeout %d s): %s" % (e["timeout_seconds"], e["evidence_gap"]))
        add("")
        add("What would settle them is a record carrying the error text and the")
        add("elapsed time — e.g. the provider call record or the attempt log.")
        add("Those records are not part of this copy of the study (only the")
        add("receipts, arms, plans and manifest are), so the class stays")
        add("unresolved. The `timeout` class total is zero not because the clock")
        add("was shown to be uninvolved, but because the evidence that would")
        add("establish either verdict is not in the records at hand.")
    else:
        add("None.")
    add("")

    # totals
    add("## Totals")
    add("")
    add("Counts and their provenance: every table above is emitted by")
    add("`python3 check/f001_classify.py` from the receipt files, the plans and")
    add("the manifest; the same run asserts the cross-checks (planned = receipts")
    add("+ receipt-less; every ceiling row sits exactly at its arm's declared")
    add("ceiling; every `finish_reason: length` receipt in the study is a")
    add("ceiling row — %d of %d)." % (length_total, len(ceilings_hits)))
    add("")
    add("### By class")
    add("")
    add("| class | total | occurrences |")
    add("|---|---|---|")
    add(
        "| ceiling | %d | occurrence-04: %d, occurrence-05: %d |"
        % (
            len(ceilings_hits),
            sum(1 for e in ceilings_hits if e["occurrence"] == "occurrence-04"),
            sum(1 for e in ceilings_hits if e["occurrence"] == "occurrence-05"),
        )
    )
    add(
        "| blocked | %d | occurrence-04: %d, occurrence-05: %d, occurrence-07: %d |"
        % (
            len(blocked),
            sum(1 for e in blocked if e["occurrence"] == "occurrence-04"),
            sum(1 for e in blocked if e["occurrence"] == "occurrence-05"),
            sum(1 for e in blocked if e["occurrence"] == "occurrence-07"),
        )
    )
    add("| timeout | %d | — (no coordinate's record settles this class) |" % len(timeouts))
    add(
        "| unclassified | %d | occurrence-07: %d, occurrence-08: %d |"
        % (
            len(unclassified),
            sum(1 for e in unclassified if e["occurrence"] == "occurrence-07"),
            sum(1 for e in unclassified if e["occurrence"] == "occurrence-08"),
        )
    )
    add("| **unresolved total** | **%d** |  |" % len(unresolved))
    add("")
    add("### By occurrence")
    add("")
    add("| occurrence | endpoint | arm ceiling | ceiling | timeout | blocked | unclassified | unresolved |")
    add("|---|---|---|---|---|---|---|---|")
    for occ, data in occ_data.items():
        endpoints_here = sorted({a["endpoint"] for a in data["plan"]["arms"].values()})
        assert len(endpoints_here) == 1, endpoints_here
        ceilings_here = sorted(
            {a["max_tokens"] for a in data["plan"]["arms"].values()}
        )
        rows_here = [e for e in unresolved if e["occurrence"] == occ]
        add(
            "| %s | %s | %s | %d | %d | %d | %d | %d |"
            % (
                occ,
                endpoints_here[0],
                "/".join(str(c) for c in ceilings_here),
                sum(1 for e in rows_here if e["cls"] == "ceiling"),
                sum(1 for e in rows_here if e["cls"] == "timeout"),
                sum(1 for e in rows_here if e["cls"] == "blocked"),
                sum(1 for e in rows_here if e["cls"] == "unclassified"),
                len(rows_here),
            )
        )
    add("")
    add("### By endpoint")
    add("")
    add("Occurrences 04/07 and 05/08 share an endpoint each but run under")
    add("different resource conditions (arm ceilings 8,192 then 32,768; runner v1")
    add("then v2 — `PLAN.md`, successor section). They are kept on separate lines")
    add("so that no resource condition is conflated; no endpoint is totalled")
    add("across conditions, and none are ordered.")
    add("")
    add("| endpoint | occurrence (arm ceiling) | ceiling | timeout | blocked | unclassified | unresolved |")
    add("|---|---|---|---|---|---|---|")
    endpoint_occ = OrderedDict()
    for occ, data in occ_data.items():
        endpoint = sorted({a["endpoint"] for a in data["plan"]["arms"].values()})[0]
        ceiling_here = sorted({a["max_tokens"] for a in data["plan"]["arms"].values()})[0]
        endpoint_occ[(endpoint, occ, ceiling_here)] = [
            e for e in unresolved if e["occurrence"] == occ
        ]
    for (endpoint, occ, ceiling_here), rows_here in endpoint_occ.items():
        add(
            "| %s | %s (%d) | %d | %d | %d | %d | %d |"
            % (
                endpoint,
                occ,
                ceiling_here,
                sum(1 for e in rows_here if e["cls"] == "ceiling"),
                sum(1 for e in rows_here if e["cls"] == "timeout"),
                sum(1 for e in rows_here if e["cls"] == "blocked"),
                sum(1 for e in rows_here if e["cls"] == "unclassified"),
                len(rows_here),
            )
        )
    add("")
    add("## What this table is not")
    add("")
    add("These rows classify how each unresolved coordinate ended against the")
    add("declared boundaries — a completion-token ceiling, a wall clock, or the")
    add("no-retry truncation rule. They are resource-boundary facts. Nothing")
    add("here ranks endpoints or families, calls any of them less reliable,")
    add("measures anyone's reasoning, or treats a boundary as exhaustion of the")
    add("inquiry. No failure rate is computed; a count is information, not a")
    add("warrant.")

    text = "\n".join(lines) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)

    # ---- stdout verification ------------------------------------------------
    print("wrote", OUT)
    print("planned total               :", planned_total)
    print("receipts present            :", receipt_total, counts_by_status)
    print("planned, no receipt         :", planned_total - receipt_total)
    print("unresolved total            :", len(unresolved))
    print(
        "by class                    : ceiling=%d timeout=%d blocked=%d unclassified=%d"
        % (len(ceilings_hits), len(timeouts), len(blocked), len(unclassified))
    )
    print(
        "finish_reason=length receipts: %d (all are ceiling rows; cross-check)"
        % length_total
    )
    print("receipt key union           :", sorted(all_receipt_keys))
    for occ, data in occ_data.items():
        rows_here = [e for e in unresolved if e["occurrence"] == occ]
        print(
            "  %s planned=%d receipts=%d unresolved=%d (%s)"
            % (
                occ,
                len(data["planned"]),
                sum(1 for r in data["rows"] if r["receipt"] is not None),
                len(rows_here),
                ", ".join(
                    "%s:%d"
                    % (cls, sum(1 for e in rows_here if e["cls"] == cls))
                    for cls in ("ceiling", "timeout", "blocked", "unclassified")
                ),
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
