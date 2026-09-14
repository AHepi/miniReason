"""Corner attacks.

  C1 reading_dir: fold-collision - two keys that fold alike must differ
  C2 reading_dir: key that folds to empty ('///') gets 'row-<digest>'
  C3 reading_dir: key of all unsafe chars, and a key ending in dots
  C4 _fraction(True) and float('nan') for judge_err_max
  C5 _whole(True) for cycle_budget - True is not a budget
  C6 loop_plan_id pins: null, upper-hex, absolute path, '..' path, non-str key
  C7 loop_plan_id: pin order must not change the identity
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop.types import run_paths, loop_plan_id, LoopConfig, LoopError

rp = run_paths("/repo", "run1")
d1 = rp.reading_dir("a/b/c").name
d2 = rp.reading_dir("a:b:c").name
print("C1 fold-collision differ:", d1 != d2, d1.split("-")[-1] != d2.split("-")[-1])

print("C2 '///' ->", rp.reading_dir("///").name)
print("C3 dots ->", rp.reading_dir("...").name)

GOOD = dict(
    run_id="r1", study="s", occurrences=["o1"], runner="run.py",
    cycle_budget=1, max_calls=5, reading_set=["a"], obligations_path="ob.json",
    graph_root="g", reopen_reasons=["x"],
    audit=dict(period=1, judge_err_max=0.5, streak_max=3,
               judge_err_max_account="a", streak_max_account="b"),
)
def refuse(label, mutation, *path):
    try:
        LoopConfig.from_mapping(mutation)
        print(label, "ACCEPTED")
    except LoopError as exc:
        print(label, "refused:", exc.code)

m = dict(GOOD); m["cycle_budget"] = True
refuse("C5 bool budget", m)
m = dict(GOOD); m["audit"] = dict(GOOD["audit"]); m["audit"]["judge_err_max"] = float("nan")
refuse("C4 nan judge_err_max", m)
m = dict(GOOD); m["audit"] = dict(GOOD["audit"]); m["audit"]["judge_err_max"] = True
refuse("C4 bool judge_err_max", m)

cfg = LoopConfig.from_mapping(GOOD)
h = "a"*64
print("C7 pin order equal:",
      loop_plan_id(cfg, {"b/x": h, "a/x": h}) == loop_plan_id(cfg, {"a/x": h, "b/x": h}))

for label, pins in [
    ("null pin", {"p/f.py": None}),
    ("upper hex", {"p/f.py": "A"*64}),
    ("short hex", {"p/f.py": "abc"}),
    ("abs path", {"/etc/passwd": h}),
    ("dotdot", {"a/../b": h}),
    ("backslash", {"a\\b": h}),
    ("nonstr", {1: h}),
]:
    try:
        loop_plan_id(cfg, pins)
        print("C6", label, "ACCEPTED")
    except LoopError as exc:
        print("C6", label, "refused:", exc.code)
    except Exception as exc:
        print("C6", label, "WRONG-EXC:", type(exc).__name__, exc)
