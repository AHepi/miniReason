"""Run a battery of worker tasks against kimi-k3, concurrently, and summarise.

    python3 kimi/run_battery.py                      # every task in battery/tasks.json
    python3 kimi/run_battery.py --only b-001 b-003   # a subset
    python3 kimi/run_battery.py --workers 4          # fewer than the ceiling of 8

Each task gets ``runs/<id>/transcript.jsonl``, ``runs/<id>/result.json`` and its
own sandbox; the battery writes ``runs/SUMMARY.md``.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from kimi_agent import (MAX_CONCURRENCY, MAX_TOKENS, REASONING_SETTINGS,  # noqa: E402
                        DEFAULT_RUNS_DIR, TaskSpec, TaskResult, run_tasks)

HERE = Path(__file__).resolve().parent
DEFAULT_TASKS = HERE / "battery" / "tasks.json"


def load_tasks(path: Path | str = DEFAULT_TASKS) -> list[TaskSpec]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        raw = raw["tasks"]
    return [TaskSpec.from_mapping(entry) for entry in raw]


def summary_markdown(results: list[TaskResult]) -> str:
    header = ("| id | title | status | mode | transport | iters | tool calls | tokens | wall s | "
              "finish | harness failure |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
    rows = []
    for result in results:
        calls = ", ".join(f"{name} {count}" for name, count in sorted(result.tool_calls.items())) or "-"
        transport = result.transport_used or "-"
        if result.transport_fallbacks:
            transport += f" (fell back from {result.transport_requested})"
        rows.append("| {id} | {title} | {status} | {mode} | {transport} | {iters} | "
                    "{calls} ({total}) | {tokens} | {wall} | {finish} | {failure} |".format(
                        id=result.task_id, title=result.title.replace("|", "/"),
                        status=result.status, mode=result.mode, transport=transport,
                        iters=result.iterations, calls=calls, total=result.tool_call_total,
                        tokens=result.total_tokens, wall=f"{result.wall_seconds:.1f}",
                        finish=result.finish_reason or "-",
                        failure=result.harness_failure or "-"))
    totals = ("\nTotals: {n} task(s), {tokens} tokens, {calls} tool calls, "
              "{failed} harness failure(s).\n").format(
                  n=len(results), tokens=sum(r.total_tokens for r in results),
                  calls=sum(r.tool_call_total for r in results),
                  failed=sum(1 for r in results if r.harness_failure))
    files = "\n".join(
        f"\n### {r.task_id} — files written\n" + ("\n".join(
            f"- `{entry['path']}` ({entry['change']}, sha256 {str(entry['sha256'])[:16]})"
            for entry in r.files_written) or "- (none)")
        # Reasoning is billed against the same per-turn budget as the answer, so
        # per-turn reasoning length is the throughput number worth reading.
        + "\n\nReasoning characters per turn: "
        + (", ".join(str(count) for count in r.reasoning_chars) or "(none)")
        + f"\n\nExpected outputs present: {', '.join(r.expected_outputs_present) or '(none)'}"
        + f"; missing: {', '.join(r.expected_outputs_missing) or '(none)'}"
        for r in results)
    return ("# kimi-k3 worker battery\n\n" + header + "\n".join(rows) + "\n" + totals + files + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", default=str(DEFAULT_TASKS))
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR))
    parser.add_argument("--workers", type=int, default=MAX_CONCURRENCY)
    parser.add_argument("--only", nargs="*", default=None, help="task ids to run")
    parser.add_argument("--max-tokens", type=int, default=None,
                        help=f"override every task's per-turn budget (default {MAX_TOKENS})")
    parser.add_argument("--max-iterations", type=int, default=None,
                        help="override every task's iteration cap")
    parser.add_argument("--reasoning", choices=REASONING_SETTINGS, default=None,
                        help="override every task's reasoning setting")
    arguments = parser.parse_args(argv)

    tasks = load_tasks(arguments.tasks)
    if arguments.only:
        wanted = set(arguments.only)
        tasks = [task for task in tasks if task.id in wanted]
    # Overrides are applied here, not inside the harness: the task file stays
    # the record of what the battery declared, and the run prints what it ran.
    overrides = {name: value for name, value in
                 (("max_tokens", arguments.max_tokens),
                  ("max_iterations", arguments.max_iterations),
                  ("reasoning", arguments.reasoning)) if value is not None}
    if overrides:
        tasks = [dataclasses.replace(task, **overrides) for task in tasks]
        print("overrides: " + ", ".join(f"{name}={value}" for name, value in overrides.items()))
    if not tasks:
        print("no tasks selected", file=sys.stderr)
        return 2
    print(f"running {len(tasks)} task(s) at up to {min(arguments.workers, MAX_CONCURRENCY)} "
          f"concurrent (key ceiling {MAX_CONCURRENCY})")
    results = run_tasks(tasks, workers=arguments.workers, runs_dir=arguments.runs_dir)
    runs_dir = Path(arguments.runs_dir)
    runs_dir.mkdir(parents=True, exist_ok=True)
    (runs_dir / "SUMMARY.md").write_text(summary_markdown(results), encoding="utf-8")
    for result in results:
        print(f"{result.task_id:<12} {result.status:<16} iters={result.iterations:<3} "
              f"tools={result.tool_call_total:<3} tokens={result.total_tokens:<7} "
              f"{result.wall_seconds:.1f}s {result.harness_failure or ''}")
    print(f"summary: {runs_dir / 'SUMMARY.md'}")
    return 1 if any(r.harness_failure for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
