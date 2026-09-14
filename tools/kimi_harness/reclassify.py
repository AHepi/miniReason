"""Re-label every recorded kimi-k3 run under the harness's current statuses.

    python3 kimi/reclassify.py              # writes kimi/RUNS-RECLASSIFIED.md
    python3 kimi/reclassify.py --print      # also print the table to stdout

The runs under ``runs/``, ``runs-pass2/`` and ``runs-pass3/`` were recorded by
an older rule: *any* assistant turn without a tool call ended the loop as
``COMPLETE``, even a turn that came back ``finish_reason: length`` with empty
content because the whole per-turn budget had gone to native reasoning. That is
not a completion, and neither is a run that reached ``stop`` without writing a
single one of its declared ``expected_outputs``.

This script re-reads those records — ``result.json``, ``transcript.jsonl`` and
the task's ``expected_outputs`` from ``battery/tasks*.json`` — and says what
each run *would* be labelled today. It is strictly read-only: no record is
rewritten, no sandbox is touched, no provider is called. The verdict lands in a
new file, ``RUNS-RECLASSIFIED.md``, beside the records it describes.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from kimi_agent import TURN_BUDGET_EXHAUSTED, is_stop_finish  # noqa: E402

OUTPUT = HERE / "RUNS-RECLASSIFIED.md"

#: (pass label, runs directory, task file). Ordered oldest to newest.
PASSES: tuple[tuple[str, str, str], ...] = (
    ("pass1", "runs", "battery/tasks.json"),
    ("pass2", "runs-pass2", "battery/tasks-pass2.json"),
    ("pass3", "runs-pass3", "battery/tasks-pass3.json"),
)

#: ``runs/`` also holds the live smoke run, which is not a battery task and
#: whose "expected outputs" are prose rather than paths. It is listed at the
#: bottom of the report rather than scored against a path that never existed.
NOT_BATTERY = ("smoke-001",)

PRESENT_WRITTEN = "+"    # exists, and this run wrote it
PRESENT_COPIED = "="     # exists, but it came in with the context copy
MISSING = "-"            # not there at all


# --------------------------------------------------------------------------
# Reading the records
# --------------------------------------------------------------------------


def load_tasks(path: Path) -> dict[str, dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        raw = raw["tasks"]
    return {entry["id"]: entry for entry in raw}


def last_response(transcript: Path) -> dict[str, Any] | None:
    """The final ``response`` event in a transcript, or None if there is none."""

    found: dict[str, Any] | None = None
    if not transcript.is_file():
        return None
    with transcript.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("event") == "response":
                found = event
    return found


def output_state(sandbox: Path, declared: str, written: set[str]) -> str:
    """One declared output's mark: written, merely present, or missing.

    Mirrors ``kimi_agent.expected_output_state``: a declared output ending in
    ``/`` (or naming a directory) counts as present only when the directory
    exists *and* holds at least one file. Read-only — nothing is created here,
    unlike the harness's ``Sandbox``, which would make its own root.
    """

    relative = declared.rstrip("/") or "."
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        return MISSING
    target = sandbox / relative
    if target.is_dir():
        present = any(child.is_file() for child in target.rglob("*"))
        under = {path for path in written if path == relative or path.startswith(relative + "/")}
        return (PRESENT_WRITTEN if (present and under) else
                PRESENT_COPIED if present else MISSING)
    if target.is_file():
        return PRESENT_WRITTEN if relative in written else PRESENT_COPIED
    return MISSING


# --------------------------------------------------------------------------
# The rules
# --------------------------------------------------------------------------


def reclassify(recorded: str, response: dict[str, Any] | None,
               marks: Sequence[str]) -> tuple[str, str | None, str]:
    """(status, harness failure, why) for one recorded run under today's rules.

    A run that failed in the harness or ran out of iterations is already
    labelled honestly and keeps its label. Only the runs recorded ``COMPLETE``
    are re-examined, against the two claims that word makes: that the final
    turn finished, and that the task's outputs exist.
    """

    if recorded != "COMPLETE":
        return recorded, None, "recorded label already names how it stopped"
    finish = (response or {}).get("finish_reason")
    content = (response or {}).get("content") or ""
    calls = (response or {}).get("tool_calls") or []
    if response is not None and not calls and not content.strip() and not is_stop_finish(finish):
        return ("INCOMPLETE_TURN", TURN_BUDGET_EXHAUSTED,
                f"final turn finished as {finish!r} with no tool call and no content")
    missing = [mark for mark in marks if mark == MISSING]
    if missing:
        return "NO_DELIVERABLE", None, f"{len(missing)} expected output(s) missing"
    return "COMPLETE", None, "final turn finished and every expected output exists"


@dataclass
class Row:
    pass_label: str
    task_id: str
    recorded: str
    reclassified: str
    harness_failure: str | None
    recorded_failure: str | None
    iterations: int
    tool_calls: int
    prompt_tokens: int
    completion_tokens: int
    wall_seconds: float
    finish_reason: str | None
    max_tokens: int | None = None
    expected: list[tuple[str, str]] = field(default_factory=list)
    last_turn: dict[str, Any] = field(default_factory=dict)
    why: str = ""

    @property
    def relabelled(self) -> bool:
        return self.recorded != self.reclassified


def collect() -> tuple[list[Row], list[Row], dict[str, list[str]]]:
    """Every (pass, task) row, the non-battery rows, and the task order."""

    rows: list[Row] = []
    extras: list[Row] = []
    order = list(load_tasks(HERE / PASSES[0][2]))
    for pass_label, runs_name, tasks_name in PASSES:
        runs_dir = HERE / runs_name
        tasks = load_tasks(HERE / tasks_name)
        if not runs_dir.is_dir():
            continue
        for run_dir in sorted(runs_dir.iterdir()):
            result_path = run_dir / "result.json"
            if not result_path.is_file():
                continue
            result = json.loads(result_path.read_text(encoding="utf-8"))
            task_id = result.get("task_id", run_dir.name)
            task = tasks.get(task_id)
            written = {entry["path"] for entry in result.get("files_written") or []}
            sandbox = run_dir / "sandbox"
            declared = list((task or {}).get("expected_outputs") or [])
            marks = [(name, output_state(sandbox, name, written)) for name in declared]
            response = last_response(run_dir / "transcript.jsonl")
            recorded = result.get("status", "?")
            if task is None:
                status, failure, why = recorded, result.get("harness_failure"), "not a battery task"
            else:
                status, failure, why = reclassify(recorded, response, [m for _, m in marks])
            row = Row(
                pass_label=pass_label, task_id=task_id, recorded=recorded,
                reclassified=status,
                harness_failure=failure or (result.get("harness_failure") if status == recorded else failure),
                recorded_failure=result.get("harness_failure"),
                iterations=result.get("iterations", 0),
                tool_calls=result.get("tool_call_total", 0),
                prompt_tokens=result.get("prompt_tokens", 0),
                completion_tokens=result.get("completion_tokens", 0),
                wall_seconds=result.get("wall_seconds", 0.0),
                finish_reason=(response or {}).get("finish_reason", result.get("finish_reason")),
                max_tokens=(task or {}).get("max_tokens"),
                expected=marks, last_turn=response or {}, why=why)
            (extras if task is None or task_id in NOT_BATTERY else rows).append(row)
    index = {task_id: position for position, task_id in enumerate(order)}
    rows.sort(key=lambda r: (index.get(r.task_id, len(index)), r.pass_label))
    return rows, extras, {"order": order}


# --------------------------------------------------------------------------
# The report
# --------------------------------------------------------------------------


def render_expected(row: Row) -> str:
    if not row.expected:
        return "(none declared)"
    return " ".join(f"`{name}` [{mark}]" for name, mark in row.expected)


def table(rows: Sequence[Row]) -> str:
    header = ("| pass | task | recorded | reclassified | iters | tool calls | prompt tok | "
              "completion tok | wall s | last finish | harness failure | expected outputs |\n"
              "|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    lines = []
    for row in rows:
        label = row.reclassified if not row.relabelled else f"**{row.reclassified}**"
        lines.append(
            f"| {row.pass_label} | `{row.task_id}` | {row.recorded} | {label} | "
            f"{row.iterations} | {row.tool_calls} | {row.prompt_tokens} | {row.completion_tokens} | "
            f"{row.wall_seconds:.1f} | {row.finish_reason or '-'} | "
            f"{row.harness_failure or row.recorded_failure or '-'} | {render_expected(row)} |")
    return header + "\n".join(lines) + "\n"


def summaries(rows: Sequence[Row], order: Sequence[str]) -> list[str]:
    """One line per battery task: the latest pass that is genuinely COMPLETE."""

    by_task: dict[str, list[Row]] = {task_id: [] for task_id in order}
    for row in rows:
        by_task.setdefault(row.task_id, []).append(row)
    lines = []
    for task_id in order:
        runs = sorted(by_task.get(task_id, []), key=lambda r: r.pass_label)
        complete = [run for run in runs if run.reclassified == "COMPLETE"]
        latest = complete[-1].pass_label if complete else None
        trail = ", ".join(
            f"{run.pass_label} {run.recorded}"
            + (f" -> {run.reclassified}" if run.relabelled else "")
            for run in runs) or "no recorded run"
        verdict = f"**{latest}**" if latest else "**none**"
        lines.append(f"- `{task_id}` — latest genuinely COMPLETE pass: {verdict} ({trail})")
    return lines


def budget_evidence(rows: Sequence[Row]) -> list[str]:
    lines = []
    for row in rows:
        if row.reclassified != "INCOMPLETE_TURN":
            continue
        turn = row.last_turn
        usage = turn.get("usage") or {}
        lines.append(
            f"| {row.pass_label} | `{row.task_id}` | {turn.get('iteration', '-')} | "
            f"{turn.get('finish_reason', '-')} | {usage.get('completion_tokens', '-')} | "
            f"{row.max_tokens if row.max_tokens is not None else '-'} | "
            f"{turn.get('reasoning_content_chars', '-')} | "
            f"{turn.get('reasoning_tokens_estimated', '-')} | "
            f"`{str(turn.get('reasoning_content_sha256'))[:16]}` |")
    return lines


def counts(rows: Sequence[Row], attribute: str) -> str:
    tally: dict[str, int] = {}
    for row in rows:
        tally[getattr(row, attribute)] = tally.get(getattr(row, attribute), 0) + 1
    return ", ".join(f"{status} {count}" for status, count in sorted(tally.items()))


def report(rows: Sequence[Row], extras: Sequence[Row], order: Sequence[str]) -> str:
    relabelled = [row for row in rows if row.relabelled]
    incomplete = [row for row in relabelled if row.reclassified == "INCOMPLETE_TURN"]
    no_deliverable = [row for row in relabelled if row.reclassified == "NO_DELIVERABLE"]
    evidence = budget_evidence(rows)
    parts = [
        "# kimi-k3 battery runs, reclassified",
        "",
        "Every run recorded under `runs/` (pass 1), `runs-pass2/` and `runs-pass3/`, "
        "re-read from its `result.json`, its `transcript.jsonl` and its task's "
        "`expected_outputs`, and labelled under the statuses the harness uses now. "
        "**Nothing here was re-run and no record was altered**: this file is a second "
        "reading of the same bytes, written beside them by `reclassify.py`.",
        "",
        "## Why the recorded labels are wrong",
        "",
        "The harness used to end its loop on *any* assistant turn that carried no tool "
        "call, and call that `COMPLETE`. Two different non-completions were swept into "
        "that word:",
        "",
        "1. A turn that came back **`finish_reason: length` with empty content and no "
        "tool call** — the entire per-turn `max_tokens` budget was spent on native "
        "reasoning, so the turn produced neither an action nor an answer. That is a "
        "resource boundary on the turn, and it is now "
        f"`INCOMPLETE_TURN` / `{TURN_BUDGET_EXHAUSTED}`.",
        "2. A turn that finished on its own (`stop`) but left the task's declared "
        "outputs unwritten. The model talked; it did not deliver. That is now "
        "`NO_DELIVERABLE`.",
        "",
        "`COMPLETE` now survives only when the final turn finished **and** every "
        "declared expected output exists.",
        "",
        "## Rules applied here",
        "",
        "| recorded | evidence re-read | reclassified |",
        "|---|---|---|",
        "| `HARNESS_FAILURE` | — | unchanged (the record already names how it stopped) |",
        "| `ITERATION_CAP` | — | unchanged |",
        "| `COMPLETE` | last `response` event: non-`stop` finish, no `tool_calls`, blank `content` |"
        f" `INCOMPLETE_TURN` (`{TURN_BUDGET_EXHAUSTED}`) |",
        "| `COMPLETE` | any declared `expected_output` absent from the run's sandbox |"
        " `NO_DELIVERABLE` |",
        "| `COMPLETE` | finished turn, every declared output present | `COMPLETE` |",
        "",
        "Expected-output marks: "
        f"`[{PRESENT_WRITTEN}]` exists and this run wrote it, "
        f"`[{PRESENT_COPIED}]` exists but came in with the task's context copy, "
        f"`[{MISSING}]` missing. A declared directory (trailing `/`) counts as present "
        "only when it holds at least one file.",
        "",
        "## Every recorded run",
        "",
        table(rows),
        f"Recorded: {counts(rows, 'recorded')}.",
        "",
        f"Reclassified: {counts(rows, 'reclassified')}.",
        "",
        f"{len(relabelled)} of {len(rows)} rows change label: "
        f"{len(incomplete)} to `INCOMPLETE_TURN`, {len(no_deliverable)} to `NO_DELIVERABLE`.",
        "",
        "## Runs whose recorded COMPLETE does not survive",
        "",
    ]
    if relabelled:
        parts += ["| pass | task | recorded | reclassified | why |", "|---|---|---|---|---|"]
        parts += [f"| {row.pass_label} | `{row.task_id}` | {row.recorded} | "
                  f"{row.reclassified} | {row.why} |" for row in relabelled]
    else:
        parts.append("None.")
    parts += ["", "### The turns that ran out of budget", ""]
    if evidence:
        parts += ["| pass | task | turn | finish | completion tokens | turn budget "
                  "(`max_tokens`) | reasoning chars | reasoning tokens (est.) | "
                  "reasoning sha256 |",
                  "|---|---|---|---|---|---|---|---|---|"] + evidence
        parts += ["", "The reasoning **text** was never persisted by the harness and is not "
                  "recoverable from these records; the digest, the character count and the "
                  "derived token count are what the transcript kept."]
        spent = {(row.last_turn.get("usage") or {}).get("completion_tokens")
                 for row in rows if row.reclassified == "INCOMPLETE_TURN"}
        asked = {row.max_tokens for row in rows if row.reclassified == "INCOMPLETE_TURN"}
        chars = [row.last_turn.get("reasoning_content_chars") or 0
                 for row in rows if row.reclassified == "INCOMPLETE_TURN"]
        if len(spent) == 1 and len(asked) == 1 and spent == asked:
            budget = spent.pop()
            others = sorted({row.max_tokens for row in rows
                             if row.max_tokens is not None and row.max_tokens != budget})
            note = (f"Every one of these turns spent its **entire** per-turn budget: "
                    f"{budget} completion tokens against a `max_tokens` of {budget}, "
                    f"with {min(chars):,}-{max(chars):,} characters of native reasoning "
                    "behind them and nothing left for a tool call or an answer. ")
            if others:
                note += ("The budget was lowered to that figure for these passes — pass 1 ran "
                         f"at {', '.join(str(value) for value in others)} — so this is a "
                         "boundary the harness set, not one the provider imposed. The runs "
                         "are cheap and fast *and* they deliver nothing; the recorded "
                         "`COMPLETE` labels made that trade invisible.")
            parts += ["", note]
    else:
        parts.append("None.")
    parts += ["", "## Per task: the latest pass that is genuinely COMPLETE", ""]
    parts += summaries(rows, order)
    genuine = sum(1 for line in summaries(rows, order) if "**none**" not in line)
    parts += ["", f"{genuine} of {len(order)} battery tasks have a genuinely COMPLETE pass; "
              f"{len(order) - genuine} have none.", ""]
    if extras:
        parts += ["## Outside the battery", "",
                  "Recorded runs that are not battery tasks, listed for completeness and "
                  "not scored: their `expected_outputs` are prose, not paths.", "",
                  "| pass | run | recorded | iters | tool calls | wall s | last finish |",
                  "|---|---|---|---|---|---|---|"]
        parts += [f"| {row.pass_label} | `{row.task_id}` | {row.recorded} | {row.iterations} | "
                  f"{row.tool_calls} | {row.wall_seconds:.1f} | {row.finish_reason or '-'} |"
                  for row in extras]
        parts.append("")
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(OUTPUT))
    parser.add_argument("--print", action="store_true", dest="echo",
                        help="also write the report to stdout")
    arguments = parser.parse_args(argv)

    rows, extras, meta = collect()
    text = report(rows, extras, meta["order"])
    Path(arguments.out).write_text(text, encoding="utf-8")
    if arguments.echo:
        print(text)
    relabelled = [row for row in rows if row.relabelled]
    print(f"{len(rows)} run(s) re-read, {len(relabelled)} relabelled -> {arguments.out}")
    for row in relabelled:
        print(f"  {row.pass_label:6s} {row.task_id:20s} {row.recorded} -> {row.reclassified}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
