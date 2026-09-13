"""Portable entry point for the unchanged, frozen E028 SQL use-return adapter.

Invoke with ``python -X utf8 tools/run_sql_use_return.py ...``. Verification is
portable; preparation and execution require a filesystem supporting the frozen
adapter's file and directory fsync contract. Only relative repository metadata
names use forward slashes; identity checks and provider behavior stay unchanged.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from minireason import sql_use_return_study as study
from creib.errors import RecordError
from creib.forge.conformance.common import publish_no_clobber


class PortableRepositoryPath(type(Path())):
    """Keep native absolute paths and serialize relative identity keys portably.

    The frozen adapters immediately stringify their three ``relative_to``
    results. Changing absolute path strings would break WindowsPath equality
    and therefore the adapters' imported-runtime checks.
    """

    def __str__(self) -> str:
        original = super().__str__()
        return original if self.drive or self.root else original.replace("\\", "/")


def probe_output_filesystem(destination: Path) -> None:
    """Exercise the original durability contract before creating an experiment."""
    if destination.exists():
        raise FileExistsError(destination)
    parent = destination.resolve().parent
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".sql-use-return-preflight-", dir=parent) as name:
        scratch = Path(name).resolve()
        scratch.relative_to(parent)  # Confirm cleanup stays under the target parent.
        probe = scratch / "publication.bin"
        payload = b"E028 offline filesystem publication probe\n"
        publish_no_clobber(probe, payload)
        if probe.read_bytes() != payload:
            raise RecordError("FILESYSTEM_PROBE_BYTES_CHANGED")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "verify", "run"))
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expected-plan-id")
    args = parser.parse_args(argv)
    if args.operation == "run":
        if args.output is None or args.expected_plan_id is None:
            parser.error("run requires --output and --expected-plan-id")
    if args.operation in ("prepare", "run"):
        if not sys.flags.utf8_mode:
            parser.error(args.operation + " requires Python UTF-8 mode; invoke python -X utf8")

    repo = PortableRepositoryPath(args.repo.resolve())
    if args.operation == "run":
        if study.verify(args.root, repo)["plan_id"] != args.expected_plan_id:
            raise ValueError("EXTERNALLY_PINNED_PLAN_ID_MISMATCH")
    if args.operation in ("prepare", "run"):
        destination = args.output if args.operation == "run" else args.root
        try:
            probe_output_filesystem(destination)
        except FileExistsError:
            raise
        except (OSError, RecordError):
            parser.error("TARGET_FILESYSTEM_DURABILITY_UNAVAILABLE: the frozen adapter requires "
                         "file and directory fsync; use a supported POSIX filesystem. "
                         "No provider was initialized.")
    if args.operation == "prepare":
        result = study.prepare(args.root, repo)
    elif args.operation == "verify":
        result = study.verify(args.root, repo)
    else:
        result = study.run(args.root, args.output, repo, args.expected_plan_id)
    print(json.dumps({"plan_id": result.get("plan_id"), "status": result.get("status"),
                      "provider_calls": result.get("provider_calls", 0)}))
    return 2 if args.operation == "run" and result["status"] != "COMPLETE" else 0


if __name__ == "__main__":
    raise SystemExit(main())
