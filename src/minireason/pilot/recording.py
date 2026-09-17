"""Bounded calls with immutable public custody records."""

from __future__ import annotations

from collections import deque
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import threading
import time
from typing import Any, Callable, Mapping

from minireason.reason import config
from minireason.reason.adapter import Adapter
from minireason.reason.types import ReasonFailure

from .templates import validate
from .inputs import preflight_for_endpoint
from .budget import Budget, load_price_table
from .util import digest, strict_loads, write


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8", newline="") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ReasonFailure("RECORD_ERROR", f"Expected an object in {path}")
    return value


class RecordedCalls:
    """Run calls through :class:`Adapter` and bind their public evidence.

    ``count`` counts provider attempts, including the sole schema-repair
    attempt.  ``receipts`` contains one terminal public receipt per attempt.
    """

    def __init__(
        self,
        root: Path,
        mode: str = "offline",
        max_calls: int = 300,
        scripted: Callable[..., Any] | list[Any] | None = None,
        *,
        adapter: Adapter | None = None,
        max_spend_usd: float = 6.0,
        prices=None,
        task_inputs=None,
    ) -> None:
        if mode not in {"offline", "live"}:
            raise ValueError("mode must be offline or live")
        if type(max_calls) is not int or max_calls < 1:
            raise ValueError("max_calls must be a positive integer")
        self.root = Path(root)
        self.calls_root = self.root / "calls"
        self.calls_root.mkdir(parents=True, exist_ok=True)
        if any(self.calls_root.iterdir()):
            raise ReasonFailure("RECORD_EXISTS", "Pilot calls directory is not empty")
        self.mode = mode
        self.max_calls = max_calls
        self.budget = Budget(max_spend_usd, prices=prices or load_price_table())
        self.pass_number = 1
        self.endpoint_snapshot = config.load_endpoint_snapshot()
        self.adapter = adapter or Adapter(mode, self.endpoint_snapshot)
        self._scripted = scripted
        self.task_inputs = task_inputs
        self._script_queue = deque(scripted) if isinstance(scripted, list) else None
        self._logical_count = 0
        self._count = 0
        self._receipts: list[dict[str, Any]] = []
        self._lock = threading.RLock()

    @property
    def count(self) -> int:
        with self._lock:
            return self._count

    @property
    def receipts(self) -> list[dict[str, Any]]:
        with self._lock:
            return deepcopy(self._receipts)

    @property
    def logical_count(self) -> int:
        return self._logical_count

    def budget_snapshot(self):
        return {**self.budget.snapshot(self.receipts).to_dict(), "max_calls": self.max_calls,
                "logical_calls": self.logical_count, "remaining_calls": max(0, self.max_calls-self.logical_count),
                "attempts": self.count}

    def _check_spend(self):
        snapshot = self.budget.snapshot(self.receipts)
        if not snapshot.dispatch_allowed:
            raise ReasonFailure(snapshot.stop_reason, "Spend guard stopped further dispatch; inspect recorded budget")

    def _reserve_attempt(self) -> int:
        with self._lock:
            self._check_spend()
            attempt_number = self._count
            self._count += 1
            return attempt_number

    def _fixture(self, context: dict[str, Any]) -> Any:
        if self._script_queue is not None:
            with self._lock:
                if not self._script_queue:
                    raise ReasonFailure("CONFIG_ERROR", "Offline scripted responses are exhausted")
                return self._script_queue.popleft()
        if callable(self._scripted):
            return self._scripted(**context)
        return None

    @staticmethod
    def _parsed(content: Any) -> dict[str, Any]:
        if not isinstance(content, str):
            raise ValueError("provider public content must be text")
        value = strict_loads(content)
        if not isinstance(value, dict):
            raise ValueError("provider public content must be a JSON object")
        return value

    def _endpoint_metadata(self, seat: str | dict[str, Any]) -> dict[str, Any]:
        data = self.endpoint_snapshot["data"]
        endpoint = config.endpoint_for(seat, data)
        return {
            "name": endpoint.name,
            "model": endpoint.model,
            "family": endpoint.family,
            "lineage": config.lineage(seat, data),
            "native_thinking_available": config.native_thinking_available(endpoint),
        }

    @staticmethod
    def _actual_wire(request: Mapping[str, Any]) -> tuple[str, str]:
        if request.get("request_bytes_sha256"):
            return "request_bytes_sha256", str(request["request_bytes_sha256"])
        if request.get("would_send_bytes_sha256"):
            return "would_send_bytes_sha256", str(request["would_send_bytes_sha256"])
        raise ReasonFailure("CUSTODY_MISMATCH", "Provider request has no actual-byte authority")

    def _check_custody(self, prepared: dict[str, Any], request_path: Path) -> dict[str, Any]:
        request = _read_json(request_path)
        authority, actual_sha = self._actual_wire(request)
        recorded_text = request.get("wire_body_text")
        if not isinstance(recorded_text, str):
            raise ReasonFailure("CUSTODY_MISMATCH", "Provider request omitted wire_body_text")
        recorded_sha = hashlib.sha256(recorded_text.encode("utf-8")).hexdigest()
        checks = {
            "prepared_equals_provider_payload": prepared["payload"] == request.get("request"),
            "prepared_wire_sha256": prepared["wire_body_sha256"],
            "provider_wire_sha256": request.get("wire_body_sha256"),
            "actual_authority": authority,
            "actual_wire_sha256": actual_sha,
            "recorded_wire_sha256": recorded_sha,
            "request_recorded_epoch": request.get("recorded_epoch"),
        }
        if not (
            checks["prepared_equals_provider_payload"]
            and prepared["wire_body_text"] == recorded_text
            and len({prepared["wire_body_sha256"], request.get("wire_body_sha256"), actual_sha, recorded_sha}) == 1
        ):
            raise ReasonFailure("CUSTODY_MISMATCH", "Prepared and provider wire bytes differ", checks)
        return checks

    def _attempt(
        self,
        *,
        call_id: str,
        attempt: int,
        role: str,
        messages: list[dict[str, Any]],
        seat: str | dict[str, Any],
        max_tokens: int,
        thinking: str,
        schema: Mapping[str, Any] | None,
        reason: str,
        validator=None,
    ) -> tuple[dict[str, Any] | None, str | None, dict[str, Any]]:
        self._check_spend()
        attempt_dir = self.calls_root / call_id / f"a{attempt:02d}"
        provider_dir = attempt_dir / "provider"
        # The existing live Adapter persists worker input with sorted mapping
        # keys. Freeze that same message order before preparing and dispatching
        # every attempt, so the child's reload cannot change the wire bytes.
        # JSON string contents are preserved; no observed record is rewritten.
        messages = json.loads(json.dumps(messages, ensure_ascii=False,
                                        sort_keys=True, allow_nan=False))
        if self.task_inputs is not None:
            self.task_inputs.freeze(self.root)
        exposure_receipts = (
            self.task_inputs.exposure_receipts(messages, f"{call_id}/a{attempt:02d}")
            if self.task_inputs is not None else []
        )
        try:
            prepared = self.adapter.prepare(
                seat=seat,
                messages=messages,
                max_tokens=max_tokens,
                thinking=thinking,
                role=role,
                coordinate={"call_id": call_id, "attempt": attempt, "role": role, "pilot": True},
            )
            write(attempt_dir / "prepared-request.json", {
                "schema_version": "minireason.pilot.prepared-request.v1",
                "endpoint": deepcopy(prepared["endpoint"]),
                "coordinate": deepcopy(prepared["kwargs"].get("coordinate", {})),
                "payload": deepcopy(prepared["payload"]),
                "wire_body_text": prepared["wire_body_text"],
                "wire_body_sha256": prepared["wire_body_sha256"],
            })
            endpoint_metadata = self._endpoint_metadata(seat)
            input_preflight = preflight_for_endpoint(prepared, max_tokens, endpoint_metadata)
        except BaseException as error:
            write(attempt_dir / "preflight-refusal.json", {
                "schema_version": "minireason.pilot.input-preflight-refusal.v1",
                "call_id": call_id,
                "attempt": attempt,
                "status": "not_dispatched",
                "failure_code": getattr(error, "code", type(error).__name__),
                "reason": str(error),
                "input_preflight": deepcopy(getattr(error, "receipt", {})),
                "source_reads": exposure_receipts,
                "recorded_epoch": time.time(),
            })
            raise
        attempt_number = self._reserve_attempt()
        decision = {
            "schema_version": "minireason.pilot.call-decision.v1",
            "call_id": call_id,
            "pass_number": self.pass_number,
            "attempt": attempt,
            "dispatch_number": attempt_number + 1,
            "status": "pending",
            "reason": reason,
            "role": role,
            "endpoint": endpoint_metadata,
            "max_tokens": max_tokens,
            "thinking": thinking,
            "messages_sha256": digest(messages),
            "schema_sha256": digest(schema) if schema is not None else None,
            "prepared_wire_sha256": prepared["wire_body_sha256"],
            "input_preflight": input_preflight,
            "source_reads": exposure_receipts,
            "recorded_epoch": time.time(),
        }
        write(attempt_dir / "decision.json", decision)
        try:
            fixture = self._fixture({
                "role": role,
                "messages": deepcopy(messages),
                "attempt": attempt,
                "call_id": call_id,
                "prepared": deepcopy(prepared),
            })
            result = self.adapter.call(
                seat=seat,
                messages=messages,
                records_dir=provider_dir,
                max_tokens=max_tokens,
                thinking=thinking,
                role=role,
                coordinate={"call_id": call_id, "attempt": attempt, "role": role, "pilot": True},
                scripted=fixture,
            )
            request_path = Path(result["request_path"])
            response_path = Path(result["response_path"])
            custody = self._check_custody(prepared, request_path)
            public_content = result.get("content", "")
            validation_error: str | None = None
            parsed: dict[str, Any] | None = None
            try:
                parsed = self._parsed(public_content)
                if schema is not None:
                    validate(parsed, schema)
                if validator is not None:
                    validator(parsed)
            except (TypeError, ValueError) as error:
                validation_error = str(error)
            provider_record = result.get("record", {})
            receipt = {
                "schema_version": "minireason.pilot.call-outcome.v1",
                "call_id": call_id,
                "attempt": attempt,
                "dispatch_number": attempt_number + 1,
                "status": "accepted" if validation_error is None else "contract_rejected",
                "request_path": str(request_path),
                "response_path": str(response_path),
                "request_wire": custody,
                "input_preflight": input_preflight,
                "source_reads": exposure_receipts,
                "provider_status": result.get("status"),
                "started_epoch": custody.get("request_recorded_epoch", prepared["prepared_epoch"]),
                "finished_epoch": result.get("finished_epoch"),
                "elapsed_ms": provider_record.get("elapsed_ms"),
                "usage": deepcopy(result.get("usage", {})),
                "endpoint": self._endpoint_metadata(seat),
                "pass_number": self.pass_number,
                "role": role,
                "returned_model": provider_record.get("returned_model"),
                "reasoning_content_present": provider_record.get("reasoning_content_present", False),
                "hidden_reasoning_persisted": provider_record.get("reasoning_content_persisted", False),
                "public_content_sha256": hashlib.sha256(str(public_content).encode("utf-8")).hexdigest(),
                "validation_error": validation_error,
                "recorded_epoch": time.time(),
            }
            if receipt["hidden_reasoning_persisted"] is not False:
                raise ReasonFailure("CUSTODY_MISMATCH", "Provider evidence says hidden reasoning was persisted")
            write(attempt_dir / "outcome.json", receipt)
            with self._lock:
                self._receipts.append(deepcopy(receipt))
            return parsed, validation_error, receipt
        except BaseException as error:
            provider_request = provider_dir / "call-0001.request.json"
            dispatched = provider_request.exists()
            failure = {
                "schema_version": "minireason.pilot.call-outcome.v1",
                "call_id": call_id,
                "attempt": attempt,
                "dispatch_number": attempt_number + 1,
                "status": "failed" if dispatched else "not_dispatched",
                "failure_code": getattr(error, "code", "HOST_ERROR"),
                "endpoint": self._endpoint_metadata(seat),
                "pass_number": self.pass_number,
                "role": role,
                "detail": (
                    "Call stopped after request evidence was created; inspect immutable provider records."
                    if dispatched
                    else "Call setup stopped before provider request evidence was created; nothing was dispatched."
                ),
                "recorded_epoch": time.time(),
            }
            provider_response = provider_dir / "call-0001.response.json"
            if provider_response.exists():
                response = _read_json(provider_response)
                failure["usage"] = deepcopy(response.get("usage", {}))
                failure["returned_model"] = response.get("returned_model")
            outcome_path = attempt_dir / "outcome.json"
            if not outcome_path.exists():
                write(outcome_path, failure)
                with self._lock:
                    self._receipts.append(deepcopy(failure))
            raise

    def call(
        self,
        role: str,
        messages: list[dict[str, Any]],
        seat: str | dict[str, Any] = "deepseek-flash",
        max_tokens: int = 8192,
        thinking: str = "off",
        schema: Mapping[str, Any] | None = None,
        validator=None,
    ) -> dict[str, Any]:
        if not isinstance(role, str) or not role.strip():
            raise ValueError("role must be a nonempty string")
        if not isinstance(messages, list) or not messages:
            raise ValueError("messages must be a nonempty list")
        if type(max_tokens) is not int or not 1 <= max_tokens <= 8192:
            raise ValueError("the MVP max_tokens bound is 1 through 8192")
        if thinking != "off":
            raise ValueError("the MVP supports thinking='off' only")
        original = deepcopy(messages)
        with self._lock:
            self._check_spend()
            if self._logical_count >= self.max_calls:
                raise ReasonFailure("CALL_BUDGET", "Logical call ceiling reached")
            self._logical_count += 1
            call_id = f"c{self._logical_count:04d}"
        parsed, error, _receipt = self._attempt(
            call_id=call_id,
            attempt=0,
            role=role,
            messages=original,
            seat=seat,
            max_tokens=max_tokens,
            thinking=thinking,
            schema=schema,
            reason="initial bounded call",
            validator=validator,
        )
        if error is None:
            assert parsed is not None
            return parsed
        self._check_spend()
        rejected_path = self.calls_root / call_id / "a00" / "provider" / "call-0001.response.json"
        rejected = _read_json(rejected_path).get("content", "")
        repaired_messages = original + [
            {"role": "assistant", "content": rejected},
            {"role": "user", "content": f"Your public JSON failed the declared schema: {error}. Return one corrected JSON object only."},
        ]
        parsed, second_error, receipt = self._attempt(
            call_id=call_id,
            attempt=1,
            role=role,
            messages=repaired_messages,
            seat=seat,
            max_tokens=max_tokens,
            thinking=thinking,
            schema=schema,
            reason="sole schema repair preserving the rejected public answer and exact checker error",
            validator=validator,
        )
        if second_error is not None:
            raise ReasonFailure("SCHEMA_REJECTED", "Public result failed its schema after one repair", receipt)
        assert parsed is not None
        return parsed


__all__ = ["RecordedCalls"]
