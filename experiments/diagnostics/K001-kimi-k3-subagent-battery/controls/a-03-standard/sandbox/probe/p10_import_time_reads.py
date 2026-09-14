"""What the module does at import, and what it raises when its data is damaged.

Module docstring: "Nothing here reads anything, calls anything or decides
anything: it is data plus the two pure functions that serialise and parse it."
notes/WAVE0-INTERFACE.md section 7: "Every wave-0 exception is a
``types.LoopError`` and keeps its original base."

The module source is executed in a fresh namespace whose ``__file__`` points at a
fixture directory under ``probe/``; nothing under ``src/`` is touched.
"""
from __future__ import annotations

import json
import os
import shutil

import _boot  # noqa: F401

from minireason.loop import standard as S

SRC = os.path.join(_boot.ROOT, "src", "minireason", "loop", "standard.py")
FIX = os.path.join(_boot.ROOT, "probe", "_fixtures")
SOURCE = open(SRC, encoding="utf-8").read()


def fresh_namespace(where: str, name: str) -> dict:
    """A live module object, so ``@dataclass`` can find its own module."""
    import sys
    from types import ModuleType

    module = ModuleType(name)
    module.__file__ = os.path.join(where, "standard.py")
    sys.modules[name] = module
    return module.__dict__


def exec_module(where: str) -> None:
    namespace = fresh_namespace(where, "probe_standard_copy")
    exec(compile(SOURCE, os.path.join(where, "standard.py"), "exec"), namespace)


def attempt(label: str, prepare) -> None:
    shutil.rmtree(FIX, ignore_errors=True)
    os.makedirs(os.path.join(FIX, "data"), exist_ok=True)
    prepare(os.path.join(FIX, "data"))
    try:
        exec_module(FIX)
    except S.StandardInvalid as exc:
        print("%-40s StandardInvalid %s" % (label, exc.code))
    except Exception as exc:  # noqa: BLE001 - the point is what class arrives
        print("%-40s %s: %s" % (label, type(exc).__name__, str(exc)[:56]))
    else:
        print("%-40s imported" % label)


def copy_good(data_dir: str) -> None:
    shipped = os.path.join(_boot.ROOT, "src", "minireason", "loop", "data")
    for name in ("ceiling_v1.md", "plan_8a_mirror.json"):
        shutil.copyfile(os.path.join(shipped, name), os.path.join(data_dir, name))


print("import-time file reads in standard.py:")
for i, line in enumerate(SOURCE.split("\n"), 1):
    if "read_text" in line or "read_bytes" in line:
        print("   line %d: %s" % (i, line.strip()))

print()
attempt("intact copy (control)", copy_good)


def no_ceiling(data_dir: str) -> None:
    copy_good(data_dir)
    os.remove(os.path.join(data_dir, "ceiling_v1.md"))


attempt("ceiling_v1.md absent", no_ceiling)


def truncated_ceiling(data_dir: str) -> None:
    copy_good(data_dir)
    open(os.path.join(data_dir, "ceiling_v1.md"), "w", encoding="utf-8").write(
        "**What this run claims.** Under registered standard.\n")


attempt("ceiling_v1.md truncated to one clause", truncated_ceiling)


def mirror_missing_register(data_dir: str) -> None:
    copy_good(data_dir)
    path = os.path.join(data_dir, "plan_8a_mirror.json")
    mirror = json.loads(open(path, encoding="utf-8").read())
    del mirror["registers"]["G"]
    open(path, "w", encoding="utf-8").write(json.dumps(mirror))


attempt("plan_8a_mirror.json missing register G", mirror_missing_register)


def mirror_not_json(data_dir: str) -> None:
    copy_good(data_dir)
    open(os.path.join(data_dir, "plan_8a_mirror.json"), "w", encoding="utf-8").write("{")


attempt("plan_8a_mirror.json truncated", mirror_not_json)


def mirror_marks_widened(data_dir: str) -> None:
    copy_good(data_dir)
    path = os.path.join(data_dir, "plan_8a_mirror.json")
    mirror = json.loads(open(path, encoding="utf-8").read())
    mirror["marks"] = ["differs", "same", "unresolved", "better"]
    open(path, "w", encoding="utf-8").write(json.dumps(mirror))


attempt("plan_8a_mirror.json marks widened", mirror_marks_widened)

print()
print("what a widened `marks` list does to the published mark vocabulary:")
shutil.rmtree(FIX, ignore_errors=True)
os.makedirs(os.path.join(FIX, "data"), exist_ok=True)
mirror_marks_widened(os.path.join(FIX, "data"))
wide = fresh_namespace(FIX, "probe_standard_widemarks")
exec(compile(SOURCE, "standard.py", "exec"), wide)
print("   MARKS                        =", wide["MARKS"])
print("   MARKER_SCHEMA mark enum      =",
      wide["MARKER_SCHEMA"]["properties"]["mark"]["enum"])
print("   body.marks                   =", json.loads(wide["STANDARD_BODY"])["marks"])
print("   'better' is in FORBIDDEN_KEYS:", "better" in S.FORBIDDEN_KEYS)
print("   build_standard refused it    :", False)

print()
print("what a truncated ceiling does to the published tuple:")
shutil.rmtree(FIX, ignore_errors=True)
os.makedirs(os.path.join(FIX, "data"), exist_ok=True)
truncated_ceiling(os.path.join(FIX, "data"))
namespace = fresh_namespace(FIX, "probe_standard_truncated")
exec(compile(SOURCE, "standard.py", "exec"), namespace)
print("   CEILING_REQUIRED_SENTENCES =", namespace["CEILING_REQUIRED_SENTENCES"])
print("   CEILING_CLAIM_TEMPLATE     =", namespace["CEILING_CLAIM_TEMPLATE"][:60])
print("   the body still built, sha256 =", namespace["STANDARD_BODY_SHA256"])
shutil.rmtree(FIX, ignore_errors=True)
