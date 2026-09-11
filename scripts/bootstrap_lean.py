#!/usr/bin/env python3
"""Install the pinned optional compiler outside the repository."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import urllib.request


VERSION = "4.19.0"
ARCHIVE = f"lean-{VERSION}-linux.tar.zst"
URL = f"https://github.com/leanprover/lean4/releases/download/v{VERSION}/{ARCHIVE}"
SIZE = 343842845
SHA256 = "6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe"


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        raise SystemExit("This bootstrap pins the Linux x86_64 build only")
    root = args.destination.resolve()
    repository = Path(__file__).resolve().parents[1]
    if root == repository or repository in root.parents:
        raise SystemExit("Choose a runtime directory outside the repository")
    root.mkdir(parents=True, exist_ok=True)
    archive = root / ARCHIVE
    if not archive.exists():
        temporary = root / (ARCHIVE + ".partial")
        with urllib.request.urlopen(URL, timeout=180) as incoming, temporary.open("wb") as outgoing:
            total = 0
            while block := incoming.read(1024 * 1024):
                total += len(block)
                if total > SIZE:
                    raise RuntimeError("Download exceeded the pinned archive size")
                outgoing.write(block)
        if temporary.stat().st_size != SIZE or digest(temporary) != SHA256:
            raise RuntimeError("Pinned archive size/hash mismatch; do not extract")
        temporary.replace(archive)
    if archive.stat().st_size != SIZE or digest(archive) != SHA256:
        raise RuntimeError("Pinned archive size/hash mismatch; do not extract")
    with (root / "extraction.log").open("wb") as log:
        subprocess.run(["tar", "--no-same-owner", "--zstd", "-xf", str(archive), "-C", str(root)],
                       stdout=log, stderr=log, check=True)
    binary = root / f"lean-{VERSION}-linux" / "bin" / "lean"
    probe = subprocess.run([str(binary), "--version"], text=True, capture_output=True,
                           env={"PATH": "/usr/bin:/bin"}, timeout=30)
    version = probe.stdout.strip() if probe.returncode == 0 else None
    receipt = {"release": f"v{VERSION}", "url": URL, "archive_bytes": SIZE,
               "archive_sha256": SHA256, "version": version, "binary": str(binary),
               "version_probe_returncode": probe.returncode,
               "version_probe_stderr": probe.stderr,
               "sha_provenance": "locally measured official release archive, then pinned; not an independently authenticated vendor checksum"}
    (root / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(version or "COMPILER_UNAVAILABLE: see receipt.json for the failed version probe")


if __name__ == "__main__":
    main()
