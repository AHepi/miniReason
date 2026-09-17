"""Host-owned reference menus for multi-pass pilot work products."""

from __future__ import annotations

from copy import deepcopy
import json
from typing import Any

from .inputs.canonical import canonical_json, sha256_hex
from .inputs.preflight import InputError


_NAMESPACES = {
    "child": "children",
    "assembly": "assemblies",
    "verification": "verifications",
    "host_artifact": "host_artifacts",
}
_JSON_INPUT_ROLES = frozenset({"task_input", "task_derived"})


class ReferenceMenu:
    """Register immutable host artifacts and expose exact reference choices.

    Model-facing artifact references (for example ``c0001``) are distinct from
    the bare SHA-256 unit ids accepted by ``read_source`` and ``source_reads``.
    """

    def __init__(self, task_inputs: Any) -> None:
        required = ("_register", "catalog", "read_source")
        if any(not callable(getattr(task_inputs, name, None)) for name in required):
            raise TypeError("task_inputs must provide _register, catalog, and read_source")
        self.task_inputs = task_inputs
        self._artifacts: dict[tuple[str, str], dict[str, Any]] = {}
        self._artifact_raw: dict[tuple[str, str], bytes] = {}

    @staticmethod
    def _source_read(unit_id: str, byte_count: int) -> dict[str, Any]:
        return {
            "unit_id": unit_id,
            "start": 0,
            "end": byte_count,
            "limit": min(byte_count, 65536),
        }

    def _input_entries(self) -> list[dict[str, Any]]:
        entries = []
        for card in self.task_inputs.catalog():
            if card.get("role") == "host_artifact":
                continue
            unit_id = card["unit_id"]
            byte_count = card["byte_count"]
            entry = {
                "namespace": "input_units",
                "kind": "input_unit",
                "ref": unit_id,
                "unit_id": unit_id,
                "pass_number": 0,
                "status": "pinned",
                "role": card["role"],
                "media_type": card["media_type"],
                "byte_count": byte_count,
                "range": {"start": 0, "end": byte_count},
                "source_read": self._source_read(unit_id, byte_count),
            }
            if card["role"] in _JSON_INPUT_ROLES and card["media_type"] == "application/json":
                entry["input_ref"] = {
                    "unit_id": unit_id,
                    "start": 0,
                    "end": byte_count,
                    "encoding": "json",
                }
            entries.append(entry)
        return sorted(entries, key=lambda item: item["unit_id"])

    def register(
        self,
        kind: str,
        ref: str,
        value: Any,
        pass_number: int,
        status: str,
    ) -> dict[str, Any]:
        """Register one immutable artifact and return its menu entry.

        Re-observing the identical artifact in a later pass is idempotent and
        retains the earliest pass number. A changed value or status under the
        same kind/ref is an immutable-reference conflict.
        """
        if kind not in _NAMESPACES:
            raise ValueError(f"unknown reference kind: {kind!r}")
        if not isinstance(ref, str) or not ref:
            raise ValueError("reference id must be a nonempty string")
        if type(pass_number) is not int or pass_number < 1:
            raise ValueError("pass_number must be a positive integer")
        if not isinstance(status, str) or not status:
            raise ValueError("status must be a nonempty string")
        envelope = {"kind": kind, "ref": ref, "status": status, "value": deepcopy(value)}
        try:
            raw = canonical_json(envelope)
        except (TypeError, ValueError) as error:
            raise ValueError("reference value must be canonical JSON") from error
        key = (kind, ref)
        if key in self._artifacts:
            if self._artifact_raw[key] != raw:
                raise ValueError(f"immutable reference conflict for {kind}:{ref}")
            if pass_number < self._artifacts[key]["pass_number"]:
                self._artifacts[key]["pass_number"] = pass_number
            return deepcopy(self._artifacts[key])

        unit_id = sha256_hex(raw)
        card = {
            "unit_id": unit_id,
            "sha256": unit_id,
            "byte_count": len(raw),
            "path": f"host-artifact/{kind}/{unit_id}.json",
            "media_type": "application/json",
            "role": "host_artifact",
        }
        self.task_inputs._register(raw, card)
        entry = {
            "namespace": _NAMESPACES[kind],
            "kind": kind,
            "ref": ref,
            "unit_id": unit_id,
            "pass_number": pass_number,
            "status": status,
            "byte_count": len(raw),
            "range": {"start": 0, "end": len(raw)},
            "source_read": self._source_read(unit_id, len(raw)),
        }
        self._artifacts[key] = entry
        self._artifact_raw[key] = raw
        return deepcopy(entry)

    def snapshot(self, pass_number: int) -> dict[str, Any]:
        if type(pass_number) is not int or pass_number < 1:
            raise ValueError("pass_number must be a positive integer")
        namespaces: dict[str, list[dict[str, Any]]] = {
            "input_units": self._input_entries(),
            "children": [],
            "assemblies": [],
            "verifications": [],
            "host_artifacts": [],
        }
        for entry in sorted(
            self._artifacts.values(),
            key=lambda item: (item["pass_number"], item["namespace"], item["ref"]),
        ):
            if entry["pass_number"] <= pass_number:
                namespaces[entry["namespace"]].append(deepcopy(entry))
        task_ids = sorted(
            item["unit_id"]
            for item in namespaces["input_units"]
            if "input_ref" in item
        )
        artifact_entries = [
            item
            for name in ("children", "assemblies", "verifications", "host_artifacts")
            for item in namespaces[name]
        ]
        valid_ids = {
            "inputs": task_ids,
            "source_reads": sorted(
                [item["unit_id"] for item in namespaces["input_units"]]
                + [item["unit_id"] for item in artifact_entries]
            ),
            "depends_on": sorted(item["ref"] for item in namespaces["children"]),
            "artifacts": sorted(item["ref"] for item in artifact_entries),
        }
        return {
            "schema": "pilot.reference-menu.pa5.v1",
            "pass_number": pass_number,
            "namespaces": namespaces,
            "valid_ids": valid_ids,
        }

    def _latest_pass(self) -> int:
        return max((item["pass_number"] for item in self._artifacts.values()), default=1)

    def error_menu(self, pass_number: int | None = None) -> str:
        """Return the complete valid-id menu in canonical, prompt-ready JSON."""
        number = self._latest_pass() if pass_number is None else pass_number
        return json.dumps(
            self.snapshot(number)["valid_ids"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    def _invalid(self, value: Any, *, pass_number: int, detail: str) -> ValueError:
        message = f"{detail}: {value!r}; valid IDs: {self.error_menu(pass_number)}"
        if detail == "invalid source-read unit id":
            return InputError("INPUT_UNPINNED", message)
        if detail in {"invalid source-read range", "source-read range splits UTF-8 text"}:
            return InputError("INPUT_RANGE_INVALID", message)
        return ValueError(message)

    def read_source(
        self,
        unit_id: str,
        start: int = 0,
        end: int | None = None,
        limit: int = 65536,
        call_id: str = "host-read",
    ) -> dict[str, Any]:
        snapshot = self.snapshot(self._latest_pass())
        if unit_id not in snapshot["valid_ids"]["source_reads"]:
            raise self._invalid(
                unit_id,
                pass_number=snapshot["pass_number"],
                detail="invalid source-read unit id",
            )
        return self.task_inputs.read_source(
            unit_id, start=start, end=end, limit=limit, call_id=call_id
        )

    def _validate_input_ref(
        self, value: Any, input_entries: dict[str, dict[str, Any]], pass_number: int
    ) -> None:
        # Existing worker schemas also admit a normalized raw input object.
        # Reference validation has no authority to parse or rewrite that form;
        # the established template and sealed-scope validators check it later.
        if isinstance(value, dict) and "unit_id" not in value:
            return
        unit_id = value.get("unit_id") if isinstance(value, dict) else value
        if not isinstance(value, dict) or unit_id not in input_entries:
            raise self._invalid(
                unit_id,
                pass_number=pass_number,
                detail="invalid compact input unit id",
            )
        if set(value) - {"unit_id", "start", "end", "encoding", "overrides"}:
            raise ValueError(f"invalid compact input reference shape for {unit_id!r}")
        expected = input_entries[unit_id]["input_ref"]
        if any(value.get(field) != expected[field] for field in ("start", "end", "encoding")):
            raise self._invalid(
                unit_id,
                pass_number=pass_number,
                detail="compact input must reference the complete JSON unit",
            )
        if "overrides" in value and not isinstance(value["overrides"], dict):
            raise ValueError(f"compact input overrides must be an object for {unit_id!r}")

    def validate_subtasks(
        self, subtasks: Any, *, pass_number: int | None = None
    ) -> None:
        """Validate model-authored reference fields without resolving any read."""
        number = self._latest_pass() if pass_number is None else pass_number
        snapshot = self.snapshot(number)
        if not isinstance(subtasks, list) or not subtasks:
            raise ValueError("subtasks must be a nonempty list")
        input_entries = {
            item["unit_id"]: item
            for item in snapshot["namespaces"]["input_units"]
            if "input_ref" in item
        }
        source_entries = {
            item["unit_id"]: item
            for namespace in snapshot["namespaces"].values()
            for item in namespace
        }
        child_refs = set(snapshot["valid_ids"]["depends_on"])
        earlier_ids: set[str] = set()
        for index, subtask in enumerate(subtasks, 1):
            if not isinstance(subtask, dict):
                raise ValueError(f"subtasks[{index - 1}] must be an object")
            self._validate_input_ref(subtask.get("inputs"), input_entries, number)
            subtask_id = subtask.get("id", f"s{index}")
            if not isinstance(subtask_id, str) or not subtask_id or subtask_id in earlier_ids:
                raise ValueError("subtask ids must be nonempty and unique")
            source_reads = subtask.get("source_reads", [])
            if not isinstance(source_reads, list):
                raise ValueError(f"{subtask_id}.source_reads must be a list")
            for request in source_reads:
                unit_id = request.get("unit_id") if isinstance(request, dict) else request
                if not isinstance(request, dict) or unit_id not in source_entries:
                    raise self._invalid(
                        unit_id,
                        pass_number=number,
                        detail="invalid source-read unit id",
                    )
                if set(request) != {"unit_id", "start", "end", "limit"}:
                    raise ValueError(f"invalid source-read request for {unit_id!r}")
                start, end, limit = request["start"], request["end"], request["limit"]
                byte_count = source_entries[unit_id]["byte_count"]
                if (
                    type(start) is not int
                    or type(end) is not int
                    or type(limit) is not int
                    or not 0 <= start < end <= byte_count
                    or not 1 <= limit <= 65536
                ):
                    raise self._invalid(
                        unit_id,
                        pass_number=number,
                        detail="invalid source-read range",
                    )
                body = self.task_inputs._units[unit_id]
                try:
                    body[start:end].decode("utf-8", errors="strict")
                except UnicodeDecodeError as error:
                    raise self._invalid(
                        unit_id,
                        pass_number=number,
                        detail="source-read range splits UTF-8 text",
                    ) from error
            depends_on = subtask.get("depends_on", [])
            if not isinstance(depends_on, list):
                raise ValueError(f"{subtask_id}.depends_on must be a list")
            for dependency in depends_on:
                if not isinstance(dependency, str) or (
                    dependency not in earlier_ids and dependency not in child_refs
                ):
                    raise self._invalid(
                        dependency,
                        pass_number=number,
                        detail="invalid dependency reference",
                    )
            earlier_ids.add(subtask_id)
