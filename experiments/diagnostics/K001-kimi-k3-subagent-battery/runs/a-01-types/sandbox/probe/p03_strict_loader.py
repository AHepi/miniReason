"""Attack: the strict loader claims 'an unknown key is refused rather than ignored'.

Test:
  U1 - unknown top-level key refused
  U2 - 'schema' as a key: from_mapping's _keys includes it as OPTIONAL, but only
       *the exact* CONFIG_SCHEMA is accepted. What happens with a dict subclass
       or a non-top-level schema field?  (nested unknown keys)
  U3 - a second 'schema' key deep inside 'seats' must ALSO be refused
       (nested _keys sets don't include 'schema')
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop.types import LoopConfig, LoopError

GOOD = dict(
    run_id="r1", study="s", occurrences=["o1"], runner="run.py",
    cycle_budget=1, max_calls=5, reading_set=["a"], obligations_path="ob.json",
    graph_root="g", reopen_reasons=["x"],
    audit=dict(period=1, judge_err_max=0.5, streak_max=3,
               judge_err_max_account="a", streak_max_account="b"),
)

def tryone(label, mutation):
    try:
        LoopConfig.from_mapping(mutation)
        print(label, "ACCEPTED")
    except LoopError as exc:
        print(label, "refused:", exc.code)

m = dict(GOOD); m["zzz_unknown"] = 1
tryone("U1 top unknown", m)

m = dict(GOOD); m["seats"] = {"schema": "x"}
tryone("U2 nested schema in seats", m)

m = dict(GOOD); m["audit"] = dict(GOOD["audit"]); m["audit"]["roque"] = 1
tryone("U3 nested unknown in audit", m)

# 'schema' itself with wrong value
m = dict(GOOD); m["schema"] = "minireason.loop.config.v2"
tryone("U4 wrong schema value", m)

# 'schema' omitted entirely: should work
tryone("U5 schema omitted", {k: v for k, v in GOOD.items()})
