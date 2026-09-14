"""Probe 3: pins() and verify_pins() against the acceptance clauses.

Claims under test (W0-CUSTODY acceptance): "A one-byte change to any pinned
file is detected and named", "verify_pins is pure and order-stable".
Also under test (the module's own deviation 2): "Pin keys are canonicalised to
POSIX separators before lookup."

Exercises: one-byte flip, deletion, replaced-with-directory, malformed digest,
uppercase digest, key that crawls out of the repo, map-order permutation,
repeated verification with no mutation, a bare map passed instead of a plan
body, a Windows-spelled key, and a same-bytes / same-POSIX-key duplicate.
Uses only tempfile space. Prints RESULT lines.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import custody


def result(ok: bool, *parts: object) -> None:
    print("RESULT", "PASS" if ok else "FAIL", *parts)


def note(*parts: object) -> None:
    print("RESULT NOTE", *parts)


def build_tree(base: Path) -> Path:
    (base / "src").mkdir()
    (base / "src" / "a.py").write_bytes(b"alpha-bytes\n")
    (base / "src" / "b.py").write_bytes(b"beta-bytes\n")
    return base


def main() -> None:
    with tempfile.TemporaryDirectory() as scratch:
        repo = build_tree(Path(scratch))
        frozen = custody.pins(repo, ["src/a.py", "src/b.py"])
        note("frozen pin map:", frozen)

        # -- one-byte change: detected and named --------------------------
        original = (repo / "src" / "a.py").read_bytes()
        flipped = bytes([original[0] ^ 0x01]) + original[1:]
        (repo / "src" / "a.py").write_bytes(flipped)
        findings = custody.verify_pins({"pins": frozen}, repo)
        one = findings[0] if len(findings) == 1 else None
        result(one is not None
               and one.code == "SOURCE_PIN_MISMATCH"
               and one.path == "src/a.py"
               and one.expected == frozen["src/a.py"]
               and one.observed == custody.sha256_bytes(flipped)
               and frozen["src/b.py"] not in str(findings),
               "one-byte flip:", findings)
        (repo / "src" / "a.py").write_bytes(original)

        # -- missing and directory ----------------------------------------
        os.remove(repo / "src" / "a.py")
        findings = custody.verify_pins({"pins": frozen}, repo)
        result([f.code for f in findings] == ["SOURCE_PIN_MISSING"]
               and findings[0].path == "src/a.py"
               and findings[0].observed is None,
               "deleted file:", findings)
        (repo / "src" / "a.py").mkdir()  # now a directory at the pinned path
        findings = custody.verify_pins({"pins": frozen}, repo)
        result([f.code for f in findings] == ["SOURCE_PIN_NOT_A_FILE"],
               "replaced with directory:", findings)
        shutil.rmtree(repo / "src" / "a.py")
        (repo / "src" / "a.py").write_bytes(original)

        # -- malformed digests ----------------------------------------------
        findings = custody.verify_pins({"pins": {"src/a.py": "not-a-sha"}}, repo)
        result([f.code for f in findings] == ["SOURCE_PIN_MALFORMED"],
               "non-string-shaped value:", findings)
        findings = custody.verify_pins({"pins": {"src/a.py": frozen["src/a.py"].upper()}}, repo)
        result([f.code for f in findings] == ["SOURCE_PIN_MALFORMED"],
               "uppercase sha256:", findings)
        findings = custody.verify_pins({"pins": {"src/a.py": None}}, repo)
        result([f.code for f in findings] == ["SOURCE_PIN_MALFORMED"],
               "null pin:", findings)

        # -- a key that crawls out of the repository ------------------------
        findings = custody.verify_pins({"pins": {"../outside.txt": "0" * 64}}, repo)
        result([f.code for f in findings] == ["SOURCE_PIN_OUTSIDE_REPOSITORY"]
               and findings[0].path == "../outside.txt",
               "crawling key:", findings)
        findings = custody.verify_pins(
            {"pins": {str(repo.parent / "outside.txt"): "0" * 64}}, repo)
        result([f.code for f in findings] == ["SOURCE_PIN_OUTSIDE_REPOSITORY"],
               "absolute outside key:", findings)

        # -- order stability -------------------------------------------------
        plan_a = {"pins": {"src/a.py": frozen["src/a.py"], "src/b.py": frozen["src/b.py"],
                           "../bad": "zz", "src/c-missing.py": "0" * 64}}
        plan_b = {"pins": dict(reversed(list(plan_a["pins"].items())))}
        fa = [f.as_dict() for f in custody.verify_pins(plan_a, repo)]
        fb = [f.as_dict() for f in custody.verify_pins(plan_b, repo)]
        result(fa == fb and [f["code"] for f in fa] == [
            "SOURCE_PIN_OUTSIDE_REPOSITORY", "SOURCE_PIN_MISSING",
            "SOURCE_PIN_MISMATCH"][:len(fa)] or fa == fb,
            "map-order permutation gives identical findings:", fa)
        note("sorted order is by (path, code):",
             [(f["path"], f["code"]) for f in fa])

        # -- purity: repeat verification mutates nothing ---------------------
        before_map = dict(plan_a["pins"])
        fa2 = [f.as_dict() for f in custody.verify_pins(plan_a, repo)]
        result(fa2 == fa and plan_a["pins"] == before_map,
               "second call identical, plan untouched")

        # -- bare map refused ------------------------------------------------
        try:
            custody.verify_pins(frozen, repo)
        except custody.CustodyMismatch as exc:
            result(exc.code == "PIN_MAP_MISSING",
                   "bare {path: sha} map:", exc.code, "detail=", exc.detail)
        else:
            result(False, "bare {path: sha} map: ACCEPTED AS A PLAN")

        # -- deviation 2: a Windows-spelled key must verify on this host -----
        findings = custody.verify_pins({"pins": {"src\\a.py": frozen["src/a.py"]}}, repo)
        result(findings == [], "backslash key verifies clean:", findings)
        findings = custody.verify_pins({"pins": {"src\\a.py": "0" * 64}}, repo)
        result(len(findings) == 1 and findings[0].code == "SOURCE_PIN_MISMATCH"
               and findings[0].path == "src/a.py",
               "backslash key mismatch named under the POSIX key:", findings)

        # -- the same bytes under two spellings of one POSIX key -------------
        two = custody.pins(repo, ["src/a.py", "./src/a.py"])
        result(list(two) == ["src/a.py"],
               "duplicate entry under './' collapses to one key:", list(two))
        # pins() key order is sorted regardless of insertion order
        frozen_rev = custody.pins(repo, ["src/b.py", "src/a.py"])
        result(list(frozen_rev) == ["src/a.py", "src/b.py"],
               "pins() returns sorted keys:", list(frozen_rev))


if __name__ == "__main__":
    main()
