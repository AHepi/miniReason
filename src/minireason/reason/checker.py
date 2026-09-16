"""Bounded host execution for R002 checker proposals.

The reviewed personal-harness backend uses a fresh working directory, an AST
allowlist, runtime audit guards and OS resource controls. Qualification is
restricted to the tested Windows CPython bytes. These layers are not an
OS/container network or filesystem boundary; see the declared workflow limits.
"""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from typing import Any


SCHEMA = "minireason.r002.checker-execution.v1"
BACKEND = "windows-personal-python-guard-v2"
REVIEWED_RUNTIME_SHA256 = "5f7b89a612c9b8af1d6456cdfcd1dbe5ca630849e79aebced9bee9a6694952ec"
POLICY_NAME = "restricted-python-v1"
DEFAULT_POLICY = {
    "policy": POLICY_NAME,
    "timeout_seconds": 5,
    "memory_mib": 256,
    "stdout_bytes": 65536,
    "stderr_bytes": 65536,
    "network": "deny",
    "filesystem": "isolated-readonly-runtime-and-empty-workdir",
    "source_bytes": 32768,
}

_ALLOWED_IMPORTS = frozenset({
    "collections", "decimal", "fractions", "functools", "itertools",
    "json", "math", "operator", "statistics", "sys",
})
_FORBIDDEN_IMPORTS = frozenset({
    "asyncio", "builtins", "ctypes", "http", "importlib", "io", "os",
    "pathlib", "pickle", "requests", "shutil", "socket", "subprocess",
    "tempfile", "time", "urllib",
})
_FORBIDDEN_NAMES = frozenset({
    "__builtins__", "__import__", "breakpoint", "compile", "dir", "eval",
    "exec", "format", "getattr", "globals", "help", "input", "locals", "memoryview",
    "open", "setattr", "delattr", "type", "vars",
})
_FORBIDDEN_ATTRIBUTES = frozenset({
    "argv", "attrgetter", "environ", "executable", "format", "format_map",
    "gettrace", "methodcaller", "modules", "mro", "path", "platform",
    "settrace", "setprofile", "getprofile", "addaudithook",
    "f_back", "f_globals", "f_locals", "f_builtins", "f_code",
    "gi_frame", "cr_frame", "ag_frame", "tb_frame", "tb_next",
    "stdin_buffer", "stdout_buffer",
})


_CHILD = r'''# Reviewed restricted personal-harness guard; not an OS/container security boundary.
import builtins
import collections
import decimal
import fractions
import functools
import itertools
import json
import math
import operator
import os
import statistics
import sys

source_path, work_path = sys.argv[1], sys.argv[2]
with builtins.open(source_path, "r", encoding="utf-8", newline="") as handle:
    source = handle.read()
os.chdir(work_path)
os.environ.clear()
sys.path[:] = []

allowed_imports = frozenset({
    "collections", "decimal", "fractions", "functools", "itertools",
    "json", "math", "operator", "statistics", "sys",
})
real_import = builtins.__import__
real_open = builtins.open
work_root = os.path.realpath(work_path)

def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".", 1)[0]
    if level or root not in allowed_imports:
        raise PermissionError("checker import denied")
    return real_import(name, globals, locals, fromlist, level)

def guarded_open(file, *args, **kwargs):
    try:
        resolved = os.path.realpath(os.fspath(file))
    except (TypeError, ValueError):
        raise PermissionError("checker filesystem denied")
    if os.path.commonpath((work_root, resolved)) != work_root:
        raise PermissionError("checker filesystem denied")
    return real_open(file, *args, **kwargs)

def audit(event, args):
    if event.startswith("socket.") or event.startswith("subprocess."):
        raise PermissionError("checker network/process denied")
    if event.startswith("os.") or event.startswith("ctypes."):
        raise PermissionError("checker filesystem/process denied")
    if event in {"sys.setprofile", "sys.settrace", "sys._getframe", "sys._current_frames", "sys.addaudithook"}:
        raise PermissionError("checker reflection denied")
    if event == "open":
        file = args[0]
        try:
            resolved = os.path.realpath(os.fspath(file))
        except (TypeError, ValueError):
            raise PermissionError("checker filesystem denied")
        if os.path.commonpath((work_root, resolved)) != work_root:
            raise PermissionError("checker filesystem denied")

builtins.__import__ = guarded_import
builtins.open = guarded_open
sys.addaudithook(audit)
scope = {"__builtins__": builtins.__dict__, "__name__": "__checker__"}
exec(compile(source, "<checker-proposal>", "exec"), scope, scope)
'''


def _canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _runtime(executable: str) -> tuple[str, str]:
    path = Path(executable).resolve()
    try:
        digest = _sha(path.read_bytes())
    except OSError as error:
        raise RuntimeError("checker runtime bytes are unavailable; execution refused") from error
    identity = f"{sys.implementation.name} {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} {path}"
    return identity, digest


def host_qualified(runtime_sha: str | None = None) -> bool:
    """Qualification is this reviewed host/runtime, not a formal isolation proof."""
    if os.name != "nt" or sys.version_info[:3] != (3, 11, 9):
        return False
    if runtime_sha is None:
        _identity, runtime_sha = _runtime(sys.executable)
    return runtime_sha == REVIEWED_RUNTIME_SHA256


def _proposal_bytes(proposal: dict[str, Any] | bytes | bytearray | str) -> tuple[bytes, Any]:
    if isinstance(proposal, dict):
        try:
            raw = _canonical(proposal)
        except (TypeError, ValueError):
            raw = (json.dumps(proposal, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":")) + "\n").encode("utf-8")
        return raw, proposal
    if isinstance(proposal, str):
        raw = proposal.encode("utf-8")
    elif isinstance(proposal, (bytes, bytearray)):
        raw = bytes(proposal)
    else:
        raise TypeError("proposal must be a dict, str, or bytes")
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError):
        parsed = None
    return raw, parsed


def _policy(policy: dict[str, Any] | bytes | str | None) -> tuple[dict[str, Any], bytes, list[str]]:
    if policy is None:
        supplied: Any = dict(DEFAULT_POLICY)
        raw = _canonical(supplied)
    elif isinstance(policy, bytes):
        raw = bytes(policy)
        supplied = json.loads(raw.decode("utf-8"))
    elif isinstance(policy, str):
        supplied = {"policy": policy}
        raw = _canonical(supplied)
    elif isinstance(policy, dict):
        supplied = dict(policy)
        raw = _canonical(supplied)
    else:
        raise TypeError("policy must be a dict, str, bytes, or None")

    effective = dict(DEFAULT_POLICY)
    effective.update({key: supplied[key] for key in DEFAULT_POLICY if key in supplied})
    errors: list[str] = []
    name = supplied.get("policy", supplied.get("name", POLICY_NAME))
    if name != POLICY_NAME:
        errors.append("unknown checker policy")
    for key, maximum in (("timeout_seconds", 5), ("memory_mib", 256),
                         ("stdout_bytes", 65536), ("stderr_bytes", 65536),
                         ("source_bytes", 32768)):
        value = effective.get(key)
        if (isinstance(value, bool) or not isinstance(value, (int, float)) or
                value != value or value in {float("inf"), float("-inf")} or
                value <= 0 or value > maximum):
            errors.append(f"{key} must be positive and no greater than {maximum}")
    if effective.get("network") != "deny":
        errors.append("network must be deny")
    if effective.get("filesystem") != "isolated-readonly-runtime-and-empty-workdir":
        errors.append("filesystem policy is weaker than the R002 contract")
    return effective, raw, errors


def _validate_proposal(proposal: Any) -> list[str]:
    if not isinstance(proposal, dict):
        return ["proposal must be an object"]
    required = {
        "query_id", "question", "relation_id", "working_claim_quote",
        "working_value", "language", "source", "stdin_json",
        "expected_output_schema",
    }
    errors = []
    if set(proposal) != required:
        errors.append("proposal fields do not exactly match checker-proposal.schema.json")
    for key in ("query_id", "question", "relation_id", "working_claim_quote", "source"):
        if not isinstance(proposal.get(key), str) or not proposal.get(key):
            errors.append(f"{key} must be a nonempty string")
    if proposal.get("language") != "python-3.11-restricted":
        errors.append("language must be python-3.11-restricted")
    if proposal.get("expected_output_schema") != {
            "relation_id": "string", "value": "json", "derivation": "string"}:
        errors.append("expected_output_schema does not match the frozen contract")
    try:
        _canonical(proposal.get("working_value"))
        _canonical(proposal.get("stdin_json"))
    except (TypeError, ValueError):
        errors.append("working_value and stdin_json must be finite JSON values")
    return errors


def _static_policy(source: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    breaches: set[str] = set()
    try:
        tree = ast.parse(source, mode="exec")
    except (SyntaxError, ValueError):
        return ["source is not valid Python"], ["source_policy"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root not in _ALLOWED_IMPORTS:
                    errors.append(f"import denied: {root}")
                    breaches.add("network" if root in {"http", "requests", "socket", "urllib"} else
                                 "filesystem" if root in {"io", "os", "pathlib", "shutil", "tempfile"} else
                                 "nondeterministic_api" if root in {"asyncio", "subprocess", "time"} else
                                 "source_policy")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            if node.level or root not in _ALLOWED_IMPORTS:
                errors.append(f"import denied: {root or '<relative>'}")
                breaches.add("network" if root in {"http", "requests", "socket", "urllib"} else
                             "filesystem" if root in {"io", "os", "pathlib", "shutil", "tempfile"} else
                             "nondeterministic_api" if root in {"asyncio", "subprocess", "time"} else
                             "source_policy")
            if root == "sys" or any(alias.name.startswith("_") or alias.name in _FORBIDDEN_ATTRIBUTES
                                    for alias in node.names):
                errors.append("unsafe from-import denied")
                breaches.add("source_policy")
        elif isinstance(node, ast.Name) and (node.id.startswith("__") or node.id in _FORBIDDEN_NAMES):
            errors.append(f"name denied: {node.id}")
            breaches.add("filesystem" if node.id == "open" else "source_policy")
        elif isinstance(node, ast.Attribute) and (
                node.attr.startswith("_") or node.attr in _FORBIDDEN_ATTRIBUTES):
            errors.append(f"attribute denied: {node.attr}")
            breaches.add("source_policy")
    return sorted(set(errors)), sorted(breaches or ({"source_policy"} if errors else set()))


def _decode_bounded(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def _read_bounded(path: Path, limit: int) -> bytes:
    if not path.exists():
        return b""
    with path.open("rb") as handle:
        return handle.read(limit)


def _empty_record(proposal_raw: bytes, policy_raw: bytes,
                  runtime_identity: str, runtime_sha: str,
                  started: str, elapsed_ms: int, breaches: list[str]) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "proposal_sha256": _sha(proposal_raw),
        "policy_sha256": _sha(policy_raw),
        "sandbox_backend": BACKEND,
        "runtime_identity": runtime_identity,
        "runtime_sha256": runtime_sha,
        "source_sha256": _sha(b""),
        "stdin_sha256": _sha(b""),
        "started_utc": started,
        "elapsed_ms": elapsed_ms,
        "status": "REFUSED_POLICY",
        "limit_breaches": sorted(set(breaches or ["source_policy"])),
        "exit_code": None,
        "stdout_utf8": "",
        "stderr_utf8": "",
        "stdout_sha256": _sha(b""),
        "parsed": None,
        "comparison": "not_compared",
    }


class _WindowsJob:
    def __init__(self, memory_bytes: int | None):
        self.handle = None
        if os.name != "nt":
            return
        import ctypes
        from ctypes import wintypes

        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [(name, ctypes.c_ulonglong) for name in (
                "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

        class BASIC_LIMIT(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", wintypes.DWORD),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", wintypes.DWORD),
                ("SchedulingClass", wintypes.DWORD),
            ]

        class EXTENDED_LIMIT(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", BASIC_LIMIT),
                ("IoInfo", IO_COUNTERS),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateJobObjectW.restype = wintypes.HANDLE
        kernel32.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
        kernel32.SetInformationJobObject.argtypes = (
            wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD)
        kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
        kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
        handle = kernel32.CreateJobObjectW(None, None)
        if not handle:
            raise OSError(ctypes.get_last_error(), "CreateJobObjectW failed")
        info = EXTENDED_LIMIT()
        info.BasicLimitInformation.LimitFlags = 0x00002000 | 0x00000008
        if memory_bytes is not None:
            info.BasicLimitInformation.LimitFlags |= 0x00000100
        info.BasicLimitInformation.ActiveProcessLimit = 1
        info.ProcessMemoryLimit = memory_bytes or 0
        if not kernel32.SetInformationJobObject(handle, 9, ctypes.byref(info), ctypes.sizeof(info)):
            kernel32.CloseHandle(handle)
            raise OSError(ctypes.get_last_error(), "SetInformationJobObject failed")
        self.handle = handle
        self._kernel32 = kernel32

    def assign(self, process: subprocess.Popen[bytes]) -> None:
        if self.handle is not None and not self._kernel32.AssignProcessToJobObject(
                self.handle, int(process._handle)):
            raise OSError("AssignProcessToJobObject failed")

    def close(self) -> None:
        if self.handle is not None:
            self._kernel32.CloseHandle(self.handle)
            self.handle = None


def _unix_limits(memory_bytes: int):
    def apply() -> None:
        import resource
        resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
        resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    return apply


def _terminate(process: subprocess.Popen[bytes], job: _WindowsJob | None) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        if job is not None:
            job.close()
        else:
            process.kill()
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def _parse_output(data: bytes, relation_id: str) -> dict[str, Any] | None:
    try:
        text = data.decode("utf-8", errors="strict")
        parsed = json.loads(text, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    except (UnicodeError, ValueError, TypeError):
        return None
    if not isinstance(parsed, dict) or set(parsed) != {"relation_id", "value", "derivation"}:
        return None
    if parsed.get("relation_id") != relation_id or not isinstance(parsed.get("derivation"), str):
        return None
    try:
        _canonical(parsed["value"])
    except (TypeError, ValueError):
        return None
    return parsed


def _write_once(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _persist(evidence_dir: str | Path | None, proposal_raw: bytes, policy_raw: bytes,
             source_raw: bytes, stdin_raw: bytes, record: dict[str, Any]) -> None:
    if evidence_dir is None:
        return
    directory = Path(evidence_dir)
    _write_once(directory / "proposal.json", proposal_raw)
    _write_once(directory / "policy.json", policy_raw)
    _write_once(directory / "checker.py", source_raw)
    _write_once(directory / "stdin.json", stdin_raw)
    _write_once(directory / "execution.json", _canonical(record))


def run_checker(proposal: dict[str, Any] | bytes | bytearray | str, *,
                mode: str = "offline", policy: dict[str, Any] | bytes | str | None = None,
                evidence_dir: str | Path | None = None,
                python_executable: str | None = None) -> dict[str, Any]:
    """Validate and execute one checker proposal, returning the frozen record shape."""
    executable = str(Path(python_executable or sys.executable).resolve())
    if Path(executable) != Path(sys.executable).resolve():
        raise RuntimeError("checker runtime differs from the reviewed host interpreter")
    runtime_identity, runtime_sha = _runtime(executable)
    started_utc = _utc_now()
    started = time.monotonic()
    try:
        proposal_raw, parsed_proposal = _proposal_bytes(proposal)
    except TypeError:
        proposal_raw, parsed_proposal = repr(proposal).encode("utf-8", errors="replace"), None
    try:
        effective, policy_raw, policy_errors = _policy(policy)
    except (TypeError, ValueError, UnicodeError):
        effective, policy_raw, policy_errors = dict(DEFAULT_POLICY), b"", ["invalid policy"]

    if mode not in {"offline", "live"}:
        policy_errors.append("mode must be offline or live")
    if mode == "live" and not host_qualified(runtime_sha):
        policy_errors.append("checker host/runtime differs from the reviewed Windows runtime")
    proposal_errors = _validate_proposal(parsed_proposal)
    source = parsed_proposal.get("source", "") if isinstance(parsed_proposal, dict) else ""
    source_raw = source.encode("utf-8") if isinstance(source, str) else b""
    stdin_raw = b""
    if isinstance(parsed_proposal, dict):
        try:
            stdin_raw = _canonical(parsed_proposal.get("stdin_json"))
        except (TypeError, ValueError):
            pass
    if not policy_errors and len(source_raw) > int(effective["source_bytes"]):
        proposal_errors.append("source exceeds policy byte limit")
    static_errors, static_breaches = _static_policy(source) if isinstance(source, str) else (
        ["source must be text"], ["source_policy"])
    if policy_errors or proposal_errors or static_errors:
        record = _empty_record(
            proposal_raw, policy_raw, runtime_identity, runtime_sha, started_utc,
            int((time.monotonic() - started) * 1000), static_breaches,
        )
        record["source_sha256"] = _sha(source_raw)
        record["stdin_sha256"] = _sha(stdin_raw)
        _persist(evidence_dir, proposal_raw, policy_raw, source_raw, stdin_raw, record)
        return record

    stdout_limit = int(effective["stdout_bytes"])
    stderr_limit = int(effective["stderr_bytes"])
    timeout = float(effective["timeout_seconds"])
    memory_bytes = int(effective["memory_mib"] * 1024 * 1024)
    tmp_parent = os.environ.get("TMP") or os.environ.get("TEMP")
    with tempfile.TemporaryDirectory(prefix="r2c-", dir=tmp_parent) as temp_name:
        root = Path(temp_name)
        control = root / "control"
        work = root / "work"
        control.mkdir()
        work.mkdir()
        runner_path = control / "runner.py"
        source_path = control / "proposal.py"
        stdin_path = control / "stdin.json"
        stdout_path = control / "stdout.bin"
        stderr_path = control / "stderr.bin"
        runner_path.write_text(_CHILD, encoding="utf-8", newline="")
        source_path.write_bytes(source_raw)
        stdin_path.write_bytes(stdin_raw)
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        env = {"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
               "PYTHONHASHSEED": "0", "TZ": "UTC"}
        job: _WindowsJob | None = None
        status = "NONZERO_EXIT"
        breaches: list[str] = []
        process: subprocess.Popen[bytes] | None = None
        host_error = ""
        try:
            job = _WindowsJob(memory_bytes)
            with (stdin_path.open("rb") as stdin_handle,
                  stdout_path.open("wb") as stdout_handle,
                  stderr_path.open("wb") as stderr_handle):
                process = subprocess.Popen(
                    [executable, "-P", "-s", "-S", "-B", "-X", "utf8", str(runner_path),
                     str(source_path), str(work)],
                    stdin=stdin_handle, stdout=stdout_handle, stderr=stderr_handle,
                    cwd=work, env=env, creationflags=flags,
                    start_new_session=(os.name != "nt"),
                    preexec_fn=_unix_limits(memory_bytes) if os.name != "nt" else None,
                )
                if job is not None:
                    job.assign(process)
                while process.poll() is None:
                    elapsed = time.monotonic() - started
                    if elapsed > timeout:
                        breaches.append("wall_seconds")
                        status = "TIMEOUT"
                        _terminate(process, job)
                        break
                    if stdout_path.stat().st_size > stdout_limit:
                        breaches.append("stdout_bytes")
                    if stderr_path.stat().st_size > stderr_limit:
                        breaches.append("stderr_bytes")
                    if breaches:
                        status = "OUTPUT_LIMIT"
                        _terminate(process, job)
                        break
                    time.sleep(0.005)
                if process.poll() is None:
                    process.wait()
        except (OSError, subprocess.SubprocessError) as error:
            if process is not None:
                _terminate(process, job)
            status = "REFUSED_POLICY"
            breaches = ["source_policy"]
            host_error = f"host containment startup failed: {type(error).__name__}: {error}"
        finally:
            if job is not None:
                job.close()

        stdout_size = stdout_path.stat().st_size if stdout_path.exists() else 0
        stderr_size = stderr_path.stat().st_size if stderr_path.exists() else 0
        if stdout_size > stdout_limit:
            breaches.append("stdout_bytes")
        if stderr_size > stderr_limit:
            breaches.append("stderr_bytes")
        if breaches and status not in {"TIMEOUT", "REFUSED_POLICY"}:
            status = "OUTPUT_LIMIT"
        stdout_raw = _read_bounded(stdout_path, stdout_limit)
        stderr_raw = _read_bounded(stderr_path, stderr_limit)
        if host_error:
            stderr_raw = (stderr_raw + host_error.encode("utf-8"))[:stderr_limit]
        exit_code = process.returncode if process is not None else None
        if exit_code not in {None, 0} and b"MemoryError" in stderr_raw:
            breaches.append("memory_mib")
        parsed = None
        comparison = "not_compared"
        if status not in {"TIMEOUT", "OUTPUT_LIMIT", "REFUSED_POLICY"}:
            if exit_code != 0:
                status = "NONZERO_EXIT"
            else:
                parsed = _parse_output(stdout_raw, parsed_proposal["relation_id"])
                if parsed is None:
                    status = "OUTPUT_INVALID"
                else:
                    status = "COMPLETE"
                    comparison = ("agrees" if _canonical(parsed["value"]) ==
                                  _canonical(parsed_proposal["working_value"]) else "disagrees")

    record = {
        "schema": SCHEMA,
        "proposal_sha256": _sha(proposal_raw),
        "policy_sha256": _sha(policy_raw),
        "sandbox_backend": BACKEND,
        "runtime_identity": runtime_identity,
        "runtime_sha256": runtime_sha,
        "source_sha256": _sha(source_raw),
        "stdin_sha256": _sha(stdin_raw),
        "started_utc": started_utc,
        "elapsed_ms": int((time.monotonic() - started) * 1000),
        "status": status,
        "limit_breaches": sorted(set(breaches)),
        "exit_code": exit_code,
        "stdout_utf8": _decode_bounded(stdout_raw),
        "stderr_utf8": _decode_bounded(stderr_raw),
        "stdout_sha256": _sha(stdout_raw),
        "parsed": parsed,
        "comparison": comparison,
    }
    _persist(evidence_dir, proposal_raw, policy_raw, source_raw, stdin_raw, record)
    return record


class CheckerRunner:
    """Engine-facing R002 checker runner."""

    def __init__(self, *, mode: str = "offline", python_executable: str | None = None):
        self.mode = mode
        self.python_executable = python_executable

    def run(self, proposal_bytes: dict[str, Any] | bytes | bytearray | str,
            policy: dict[str, Any] | bytes | str | None,
            evidence_dir: str | Path | None) -> dict[str, Any]:
        return run_checker(
            proposal_bytes, mode=self.mode, policy=policy,
            evidence_dir=evidence_dir, python_executable=self.python_executable,
        )
