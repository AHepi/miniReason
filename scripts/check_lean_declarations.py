#!/usr/bin/env python3
"""Optional, deliberately narrow Lean declaration check. Never a semantic gate.

This is a syntax guard plus resource controls, NOT an operating-system sandbox.
Arbitrary Lean input is refused before a compiler process can start.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import tempfile


PRIMITIVES = {"Nat", "Int", "Bool", "String", "Unit", "Prop", "Type",
              "Option", "List", "Array", "Prod", "Sum"}
RESERVED = set("""abbrev axiom by class def deriving do else end example export
false forall fun if import in include inductive instance let macro match mutual
namespace noncomputable notation opaque open partial private protected public
quote section set_option sorry structure syntax then theorem true universe
unsafe variable where with run_cmd elab initialize builtin_initialize""".split())
IDENT = r"[A-Za-z][A-Za-z0-9_]*"
HEADER = re.compile(rf"(structure|inductive) ({IDENT}) where")
FIELD = re.compile(rf" +({IDENT}) *: *(.*?) *")
CONSTRUCTOR = re.compile(rf" +\| *({IDENT})(?: *: *(.*?))? *")
TOKEN = re.compile(rf"{IDENT}|->|\(|\)")


class UnsafeOrUnsupported(ValueError):
    pass


def identifier(value: str) -> None:
    if value in RESERVED or not re.fullmatch(IDENT, value):
        raise UnsafeOrUnsupported(f"Unsupported identifier: {value!r}")


def type_expression(source: str, names: set[str]) -> None:
    """Parse only named type application, parentheses, and right-associative arrows."""
    tokens = TOKEN.findall(source)
    if "".join(tokens) != re.sub(r"\s", "", source):
        raise UnsafeOrUnsupported("Type contains unsupported tokens")
    position = 0

    def arrow(depth: int = 0) -> None:
        nonlocal position
        if depth > 40:
            raise UnsafeOrUnsupported("Type nesting exceeds the review limit")
        atoms = 0
        while position < len(tokens) and tokens[position] not in {"->", ")"}:
            token = tokens[position]
            position += 1
            if token == "(":
                arrow(depth + 1)
                if position >= len(tokens) or tokens[position] != ")":
                    raise UnsafeOrUnsupported("Unclosed type parentheses")
                position += 1
            elif token not in names:
                raise UnsafeOrUnsupported(f"Unadmitted type name: {token}")
            atoms += 1
        if not atoms:
            raise UnsafeOrUnsupported("Expected a type expression")
        if position < len(tokens) and tokens[position] == "->":
            position += 1
            arrow(depth + 1)

    arrow()
    if position != len(tokens):
        raise UnsafeOrUnsupported("Unexpected type suffix")


def guard(source: str) -> dict:
    if len(source.encode()) > 32768 or not source.isascii():
        raise UnsafeOrUnsupported("Source must be ASCII and at most 32 KiB")
    if re.search(r"[^A-Za-z0-9_\s:|()\->]", source):
        raise UnsafeOrUnsupported("Unsupported source character")
    names = set(PRIMITIVES)
    kind = None
    declarations = 0
    members = 0
    current_members = set()
    for number, raw in enumerate(source.splitlines(), 1):
        line = raw.rstrip()
        if not line:
            continue
        header = HEADER.fullmatch(line)
        if header:
            kind, name = header.groups()
            identifier(name)
            if name in names:
                raise UnsafeOrUnsupported(f"Repeated or primitive declaration: {name}")
            names.add(name)
            current_members = set()
            declarations += 1
            if declarations > 128:
                raise UnsafeOrUnsupported("Too many declarations")
            continue
        match = FIELD.fullmatch(line) if kind == "structure" else (
            CONSTRUCTOR.fullmatch(line) if kind == "inductive" else None)
        if not match:
            raise UnsafeOrUnsupported(f"Line {number} is outside the declaration subset")
        name, expression = match.groups()
        identifier(name)
        if name in current_members:
            raise UnsafeOrUnsupported(f"Duplicate member on line {number}")
        current_members.add(name)
        if expression is not None:
            type_expression(expression, names)
        members += 1
        if members > 512:
            raise UnsafeOrUnsupported("Too many members")
    if not declarations:
        raise UnsafeOrUnsupported("No declarations found")
    return {"declarations": declarations, "members": members,
            "guard": "ascii_structure_inductive_types_v1"}


def child_limits() -> None:
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (2 * 1024**2, 2 * 1024**2))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    resource.setrlimit(resource.RLIMIT_NPROC, (32, 32))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    os.umask(0o077)
    if os.getuid() == 0:
        os.setgroups([])
        os.setgid(65534)
        os.setuid(65534)


def check(source: str, lean: Path, reviewer: str, review_note: str) -> dict:
    receipt = {"source_sha256": hashlib.sha256(source.encode()).hexdigest(),
               "reviewed_by": reviewer, "review_note": review_note,
               "semantic_admission": "unchanged",
               "full_os_sandbox": False}
    try:
        receipt.update(guard(source))
    except UnsafeOrUnsupported as error:
        return receipt | {"status": "NOT_EXECUTED_OUTSIDE_SAFE_SUBSET",
                          "reason": str(error)}
    if not lean.is_file():
        return receipt | {"status": "NOT_EXECUTED_COMPILER_UNAVAILABLE"}
    with tempfile.TemporaryDirectory(prefix="minireason-lean-") as temporary:
        root = Path(temporary)
        root.chmod(0o755)
        specimen = root / "Specimen.lean"
        specimen.write_text(source)
        specimen.chmod(0o444)
        # The child sees no inherited provider credentials, home, or search paths.
        environment = {"PATH": "/usr/bin:/bin", "TMPDIR": str(root), "LANG": "C.UTF-8"}
        command = [str(lean.resolve()), "--threads=1", "--memory=1024", str(specimen)]
        receipt["command"] = [command[0], *command[1:-1], "<frozen-specimen>"]
        try:
            with (root / "stdout").open("wb") as stdout, (root / "stderr").open("wb") as stderr:
                process = subprocess.run(command, cwd=root, env=environment,
                                         stdout=stdout, stderr=stderr,
                                         timeout=45, preexec_fn=child_limits)
            receipt.update(status="COMPILED" if process.returncode == 0 else "COMPILER_REJECTED",
                           returncode=process.returncode,
                           stdout=(root / "stdout").read_text(errors="replace"),
                           stderr=(root / "stderr").read_text(errors="replace"))
        except subprocess.TimeoutExpired:
            receipt.update(status="CHECK_TIMEOUT", timeout_seconds=45)
        except (OSError, subprocess.SubprocessError) as error:
            receipt.update(status="CHECK_OPERATIONAL_FAILURE", reason=str(error))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--reviewed-by", required=True)
    parser.add_argument("--review-note", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.source.read_text(), args.lean, args.reviewed_by, args.review_note)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    # Receipts are immutable. Use a new destination for a successor check.
    with args.receipt.open("x") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    print(result["status"])


if __name__ == "__main__":
    main()
