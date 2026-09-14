"""The W0-CUSTODY acceptance clause "verify_pins is pure and order-stable",
and the docstring's "order-stable under any iteration order of the pin map".
"""
import _boot  # noqa: F401
import itertools
import os
import random
import tempfile
from pathlib import Path

from minireason.loop.custody import verify_pins, sha256_path

GOOD = "b" * 64


def snapshot(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in sorted(filenames):
            p = Path(dirpath) / name
            out.append((str(p.relative_to(root)), p.stat().st_size))
    return sorted(out)


with tempfile.TemporaryDirectory() as tmp:
    repo = Path(tmp).resolve()
    (repo / "src").mkdir()
    for name in ("a.py", "b.py", "c.py", "d.py"):
        (repo / "src" / name).write_bytes(name.encode())
    (repo / "adir").mkdir()

    entries = [
        ("src/a.py", sha256_path(repo / "src" / "a.py")),   # clean
        ("src/b.py", GOOD),                                  # mismatch
        ("src/gone.py", GOOD),                               # missing
        ("adir", GOOD),                                      # not a file
        ("../out.py", GOOD),                                 # outside
        ("src/c.py", "nope"),                                # malformed
    ]

    before = snapshot(repo)
    baseline = None
    rng = random.Random(7)
    unstable = 0
    for trial in range(200):
        order = entries[:]
        rng.shuffle(order)
        plan = {"pins": dict(order)}
        found = [(f.code, f.path, f.expected, f.observed) for f in verify_pins(plan, repo)]
        if baseline is None:
            baseline = found
        elif found != baseline:
            unstable += 1
    print("string-keyed map, 200 shuffles, differing results:", unstable)
    print("baseline:")
    for row in baseline:
        print("   ", row)
    print("tree unchanged by verify_pins:", snapshot(repo) == before)

    plan = {"pins": dict(entries)}
    keys_before = list(plan["pins"])
    verify_pins(plan, repo)
    print("plan mapping unmutated      :", list(plan["pins"]) == keys_before)
    print("repeat call equal           :",
          [f.as_dict() for f in verify_pins(plan, repo)]
          == [f.as_dict() for f in verify_pins(plan, repo)])

    # keys that are distinct objects but share str() and canonicalise to one path
    print()
    print("--- keys whose str() collides ---")
    results = set()
    for order in itertools.permutations([(1, "c" * 64), ("1", "d" * 64)]):
        plan2 = {"pins": dict(order)}
        found = tuple((f.code, f.path, f.expected) for f in verify_pins(plan2, repo))
        print("   insertion order", [k for k, _ in order], "->", found)
        results.add(found)
    print("distinct results across insertion orders:", len(results))

    print()
    print("--- keys that canonicalise to one path but sort deterministically ---")
    results = set()
    for order in itertools.permutations([("src/a.py", "e" * 64), ("./src/a.py", "f" * 64)]):
        plan3 = {"pins": dict(order)}
        found = tuple((f.code, f.path, f.expected) for f in verify_pins(plan3, repo))
        print("   insertion order", [k for k, _ in order], "->", found)
        results.add(found)
    print("distinct results across insertion orders:", len(results))
