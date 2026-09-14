"""custody.pins and custody.verify_pins under the acceptance clause of
design-s7-wave-plan.md W0-CUSTODY: "A one-byte change to any pinned file is
detected and named ... verify_pins is pure and order-stable."
"""
import _boot  # noqa: F401
import os
import tempfile
from pathlib import Path

from minireason.loop import custody
from minireason.loop.custody import pins, verify_pins, CustodyMismatch


def call(label, fn, *a, **k):
    try:
        out = fn(*a, **k)
    except CustodyMismatch as exc:
        print(f"{label:<44} REFUSED {exc.code} detail={exc.detail!r}")
    except Exception as exc:  # noqa: BLE001
        print(f"{label:<44} ESCAPED {type(exc).__name__}: {exc}")
    else:
        print(f"{label:<44} OK      {out}")


with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve()
    repo = base / "repo"
    (repo / "src" / "minireason").mkdir(parents=True)
    (repo / "src" / "minireason" / "a.py").write_bytes(b"one\n")
    (repo / "src" / "minireason" / "b.py").write_bytes(b"two\n")
    (repo / "adir").mkdir()
    (base / "outside.txt").write_bytes(b"out\n")
    os.symlink(base / "outside.txt", repo / "away.txt")

    frozen = pins(repo, ["src/minireason/b.py", "src/minireason/a.py"])
    print("pins sorted, POSIX     :", frozen)
    print("pins are byte-stable   :", pins(repo, ["src/minireason/a.py",
                                                  "src/minireason/b.py"]) == frozen)
    call("pins: missing", pins, repo, ["src/minireason/nope.py"])
    call("pins: a directory", pins, repo, ["adir"])
    call("pins: escaping key", pins, repo, ["../outside.txt"])
    call("pins: absolute outside", pins, repo, [str(base / "outside.txt")])
    call("pins: absolute inside", pins, repo, [str(repo / "src" / "minireason" / "a.py")])
    call("pins: symlink leaving the repo", pins, repo, ["away.txt"])
    call("pins: './' prefixed key", pins, repo, ["./src/minireason/a.py"])
    call("pins: repo root itself", pins, repo, ["."])

    plan = {"pins": dict(frozen)}
    print("verify clean           :", verify_pins(plan, repo))

    # one byte changed
    (repo / "src" / "minireason" / "a.py").write_bytes(b"onE\n")
    found = verify_pins(plan, repo)
    print("verify after one byte  :", [f.as_dict() for f in found])
    print("str(finding)           :", str(found[0]))
    (repo / "src" / "minireason" / "a.py").write_bytes(b"one\n")

    # removed, replaced by a directory, key outside the repo, malformed digest
    (repo / "src" / "minireason" / "b.py").unlink()
    plan2 = {"pins": {
        "src/minireason/a.py": frozen["src/minireason/a.py"],
        "src/minireason/b.py": frozen["src/minireason/b.py"],
        "adir": "0" * 64,
        "../outside.txt": "1" * 64,
        "away.txt": "2" * 64,
        "src/minireason/c.py": "not-a-digest",
        "src/minireason/d.py": None,
    }}
    for f in verify_pins(plan2, repo):
        print("   finding:", f.as_dict())

    print("plan untouched         :", list(plan2["pins"]))

    # the sha256 shape: trailing newline
    plan3 = {"pins": {"src/minireason/a.py": frozen["src/minireason/a.py"] + "\n"}}
    print("trailing-newline digest:", [f.as_dict() for f in verify_pins(plan3, repo)])
    print("custody._SHA256 match  :", bool(custody._SHA256.match(frozen["src/minireason/a.py"] + "\n")))
    from minireason.loop import types as loop_types
    print("types._HEX64 fullmatch :",
          bool(loop_types._HEX64.fullmatch(frozen["src/minireason/a.py"] + "\n")))
    try:
        loop_types.loop_plan_id({"schema": "x"}, plan3["pins"])
    except Exception as exc:  # noqa: BLE001
        print("types.loop_plan_id says:", type(exc).__name__, getattr(exc, "code", None),
              getattr(exc, "detail", None))

    # no pin map at all
    call("verify: no pins key", verify_pins, {"config": {}}, repo)
    call("verify: pins is a list", verify_pins, {"pins": []}, repo)
    call("verify: plan not a mapping", verify_pins, ["pins"], repo)
