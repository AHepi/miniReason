"""Host-controlled bounded sub-call execution."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import threading
from typing import Any, Callable, Mapping

from .recording import RecordedCalls
from .templates import OUTPUT_SCHEMA, TEMPLATES, validate, validate_inputs
from .util import digest, write


class SpawnHost:
    """Validate an entire batch, then execute it in declared order."""

    def __init__(
        self,
        calls: RecordedCalls,
        fanout: int = 24,
        max_depth: int = 3,
        executor: Callable[[str, dict[str, Any], int], dict[str, Any]] | None = None,
    ) -> None:
        if type(fanout) is not int or not 1 <= fanout <= 24:
            raise ValueError("fanout must be an integer from 1 through 24")
        if type(max_depth) is not int or not 1 <= max_depth <= 3:
            raise ValueError("max_depth must be from 1 through 3")
        if executor is not None and not callable(executor):
            raise TypeError("executor must be callable")
        if not hasattr(calls, "root"):
            raise TypeError("calls must expose its custody root")
        self.calls = calls
        self.children_root = Path(calls.root) / "children"
        self.children_root.mkdir(parents=True, exist_ok=True)
        self.fanout = fanout
        self.max_depth = max_depth
        self.executor = executor
        self._next_result = 0
        self._results: dict[str, dict[str, Any]] = {}
        self._nested_receipts: set[str] = set()
        self._lock = threading.RLock()

    def _validate_batch(
        self, subtasks: list[dict[str, Any]], depth: int, receipt: dict[str, Any] | str
    ) -> list[dict[str, Any]]:
        if type(depth) is not int or not 1 <= depth <= self.max_depth:
            raise ValueError(f"depth must be between 1 and {self.max_depth}")
        if not isinstance(receipt, (dict, str)) or not receipt:
            raise ValueError("spawn requires a nonempty host decision receipt")
        if not isinstance(subtasks, list) or not subtasks:
            raise ValueError("subtasks must be a nonempty list")
        if len(subtasks) > self.fanout or len(subtasks) > 24:
            raise ValueError("subtask batch exceeds the fanout bound")
        normalized: list[dict[str, Any]] = []
        earlier_ids: set[str] = set()
        prior_refs = set(self._results)
        for index, value in enumerate(subtasks, 1):
            if not isinstance(value, dict):
                raise ValueError(f"subtasks[{index - 1}] must be an object")
            extra = sorted(set(value) - {"id", "template_id", "inputs", "depends_on"})
            if extra:
                raise ValueError(f"subtasks[{index - 1}] has unexpected fields: {extra!r}")
            template_id = value.get("template_id")
            if template_id not in TEMPLATES:
                raise ValueError(f"unknown template_id: {template_id!r}")
            inputs = value.get("inputs")
            if not isinstance(inputs, dict):
                raise ValueError(f"subtasks[{index - 1}] is missing object inputs")
            validate_inputs(template_id, inputs)
            subtask_id = value.get("id", f"s{index}")
            if not isinstance(subtask_id, str) or not subtask_id.strip() or subtask_id in earlier_ids:
                raise ValueError("subtask ids must be nonempty and unique")
            depends_on = value.get("depends_on", [])
            if not isinstance(depends_on, list) or any(not isinstance(item, str) for item in depends_on):
                raise ValueError(f"{subtask_id}.depends_on must be a list of strings")
            if len(set(depends_on)) != len(depends_on):
                raise ValueError(f"{subtask_id}.depends_on contains duplicates")
            unavailable = [item for item in depends_on if item not in earlier_ids and item not in prior_refs]
            if unavailable:
                raise ValueError(f"{subtask_id} has unavailable or forward dependencies: {unavailable!r}")
            normalized.append({
                "id": subtask_id,
                "template_id": template_id,
                "inputs": deepcopy(inputs),
                "depends_on": list(depends_on),
            })
            earlier_ids.add(subtask_id)
        receipt_key = digest(receipt)
        if depth > 1 and receipt_key in self._nested_receipts:
            raise ValueError("nested spawn requires a new decision receipt")
        return normalized

    def _default_execute(
        self,
        template_id: str,
        inputs: dict[str, Any],
        depth: int,
        dependencies: list[dict[str, Any]],
    ) -> dict[str, Any]:
        template = TEMPLATES[template_id]
        if len(template["seats"]) != 1 or template_id not in {"direct_answer", "evidence_read"}:
            raise ValueError(f"{template_id} needs an owner-supplied multi-seat executor")
        seat = template["seats"][0]
        if seat["model"] == "host-selected":
            raise ValueError(f"{template_id} needs an owner-supplied multi-seat executor")
        system = (
            f"Execute the {template_id} template: {template['purpose']} "
            "Return JSON only, conforming exactly to this schema: "
            + json.dumps(template["output_schema"], ensure_ascii=False, sort_keys=True)
        )
        packet: dict[str, Any] = {"inputs": inputs}
        if dependencies:
            packet["accepted_dependencies"] = dependencies
        return self.calls.call(
            role=f"pilot-{seat['role']}",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(packet, ensure_ascii=False, sort_keys=True)},
            ],
            seat=seat["model"],
            max_tokens=seat["max_completion_tokens"],
            thinking=seat["thinking"],
            schema=template["output_schema"],
        )

    def spawn(
        self,
        subtasks: list[dict[str, Any]],
        depth: int = 1,
        receipt: dict[str, Any] | str = "",
    ) -> list[dict[str, Any]]:
        planned = self._validate_batch(subtasks, depth, receipt)
        receipt_key = digest(receipt)
        if depth > 1:
            self._nested_receipts.add(receipt_key)
        by_id: dict[str, dict[str, Any]] = {}
        completed: list[dict[str, Any]] = []
        for task in planned:
            dependency_results = [
                by_id[item] if item in by_id else self._results[item]
                for item in task["depends_on"]
            ]
            if any(item["status"] != "accepted" for item in dependency_results):
                raise ValueError(f"{task['id']} depends on an unaccepted result")
            if self.executor is None:
                output = self._default_execute(
                    task["template_id"], task["inputs"], depth, dependency_results
                )
            else:
                executor_inputs = deepcopy(task["inputs"])
                executor_inputs["premises"].extend(
                    json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                    for item in dependency_results
                )
                output = self.executor(task["template_id"], executor_inputs, depth)
            schema: Mapping[str, Any] = TEMPLATES[task["template_id"]].get("output_schema", OUTPUT_SCHEMA)
            validate(output, schema)
            with self._lock:
                self._next_result += 1
                result_ref = f"c{self._next_result:04d}"
            output_status = output["status"]
            result = {
                "result_ref": result_ref,
                "template_id": task["template_id"],
                "status": "accepted" if output_status == "complete" else "unaccepted",
                "output_status": output_status,
                "depends_on": list(task["depends_on"]),
                "output": deepcopy(output),
            }
            with self._lock:
                write(self.children_root / f"{result_ref}.json", result)
                self._results[result_ref] = deepcopy(result)
            by_id[task["id"]] = result
            completed.append(result)
        return completed


__all__ = ["SpawnHost"]
