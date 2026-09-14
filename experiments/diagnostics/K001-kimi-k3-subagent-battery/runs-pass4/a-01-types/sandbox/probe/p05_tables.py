"""Probe: is the STOP_REASONS set closed, and is the 'exhaustion' token absent?
Also: STEP_KINDS count vs the wave plan's '17' claim, seats validation edges,
step_path boundary checks, block_code, and the canonical-json agreement claim.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, "src")

from minireason.loop import types as T
from minireason.loop.types import LoopError
from deepreason_core.canonical import canonical_json, sha256_hex

# 1. 'exhaustion' token in any vocabulary
for name in ("STOP_REASONS", "BLOCK_CODES", "FAILURE_CODES", "STEP_KINDS"):
    hits = [t for t in sorted(getattr(T, name)) if "exhaust" in t]
    print(f"{name}: tokens containing 'exhaust' -> {hits}")

# 2. parameterised stop reason admits junk?
print("is_stop_reason('preregistered_condition:p1'):",
      T.is_stop_reason("preregistered_condition:p1"))
print("is_stop_reason('preregistered_condition:'):",
      T.is_stop_reason("preregistered_condition:"))
print("is_stop_reason('preregistered_condition:..'):",
      T.is_stop_reason("preregistered_condition:.."))

# 3. STEP_KINDS: 17 per interface
print("STEP_KINDS len:", len(T.STEP_KINDS), "distinct:", len(set(T.STEP_KINDS)))
print("REPLAYABLE & SPENDING disjoint:", not (T.REPLAYABLE_STEPS & T.SPENDING_STEPS))
print("REPLAYABLE+SPENDING <= STEP_KINDS:",
      (T.REPLAYABLE_STEPS | T.SPENDING_STEPS) <= set(T.STEP_KINDS))
unclassified = set(T.STEP_KINDS) - T.REPLAYABLE_STEPS - T.SPENDING_STEPS
print("kinds in neither:", sorted(unclassified))

# 4. block_code refuses unknown reasons
try:
    T.block_code("ensemble_split")  # underscore, not hyphen
    print("block_code('ensemble_split'): ACCEPTED (would surprise a renderer)")
except LoopError as e:
    print("block_code('ensemble_split'): refused", e.code)

# 5. canonical digest agreement
v = {"b": 1, "a": [True, None, "xé"]}
print("canonical agrees with provider_openai_compat.digest:",
      sha256_hex(canonical_json(v)) ==
      __import__("minireason.provider_openai_compat", fromlist=["digest"]).digest(v))

# 6. step_path boundaries
rp = T.run_paths(Path("/r"), "ok")
for idx in (-1, 10000, 7):
    try:
        print(f"step_path({idx}):", rp.step_path(idx, "SEND").name)
    except LoopError as e:
        print(f"step_path({idx}): refused {e.code}")

# 7. seats: judges shorter than min_judge_families refused; seats may be None
from minireason.loop.types import SeatsConfig
try:
    SeatsConfig.from_mapping({"judges": ["only-one"]})
    print("one judge: ACCEPTED (bad)")
except LoopError as e:
    print("one judge refused:", e.code)
s = SeatsConfig.from_mapping({})
print("empty seats:", s.as_dict()["judges"], s.as_dict()["critic"])

# 8. max_calls=0 admitted though cycle_budget low is 1
cfg = {"run_id": "r", "study": "s", "occurrences": ["o"], "runner": "t/x.py",
       "cycle_budget": 1, "max_calls": 0, "reading_set": ["r1"],
       "obligations_path": "o.json", "graph_root": "g",
       "reopen_reasons": ["new-material"],
       "audit": {"period": 1, "judge_err_max": 0.4, "streak_max": 2,
                 "judge_err_max_account": "a", "streak_max_account": "b"}}
c = T.LoopConfig.from_mapping(cfg)
print("max_calls=0 accepted:", c.max_calls)
