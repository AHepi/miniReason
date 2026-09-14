"""Loader / type edges.

  L1  load() of a JSON file whose top level is a LIST -> must be CONFIG_NOT_A_MAPPING
  L2  load() of invalid JSON -> currently raises CONFIG_NOT_A_MAPPING too
      (doc/interface says CONFIG_NOT_A_MAPPING is 'not a mapping' but here it
      means 'not JSON'.  Harmless but the code name lies.)
  L3  block_code(123)  -> 'blocked:123' refused?  block_code(None)?
  L4  TimeoutsConfig().step_seconds shared mutable default across instances?
  L5  SeatsConfig() default mutable 'judges' tuple is immutable - fine; check
        as_dict() returns a copy that mutation doesn't leak back
  L6  CustodyReport.from_findings accepts an object with .code (duck) AND a
      bare string; a finding without .code is refused.
"""
import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop import types

# L1 list top level
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
    fh.write("[1,2,3]"); p = fh.name
try:
    types.LoopConfig.load(p)
    print("L1 list ACCEPTED")
except types.LoopError as exc:
    print("L1 list refused:", exc.code)

# L2 not JSON
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
    fh.write("{nope"); p = fh.name
try:
    types.LoopConfig.load(p)
    print("L2 accepted")
except types.LoopError as exc:
    print("L2 notJSON ->", exc.code, "|", exc.detail[:40])

# L3 block_code non-str
for v in (123, None, ("x",)):
    try:
        types.block_code(v)
        print("L3", repr(v), "ACCEPTED")
    except types.LoopError as exc:
        print("L3", repr(v), "->", exc.code)

# L4 mutable default sharing
a = types.TimeoutsConfig(); b = types.TimeoutsConfig()
print("L4 step_seconds is MappingProxy:", type(a.step_seconds).__name__,
      "shared?", a.step_seconds is b.step_seconds)
print("L4 git default:", a.git_seconds)

# L5 as_dict copy
s = types.SeatsConfig(judges=("j1",))
d = s.as_dict(); d["judges"].append("EVIL")
print("L5 mutation leaks:", s.judges)

# L6 duck-typed findings
class F:  # mimics custody.CustodyFinding
    def __init__(self, code): self.code = code
rep = types.CustodyReport.from_findings([F("SRC_A"), "SRC_B"])
print("L6 from_findings checks:", rep.checks, "verified:", rep.verified)
print("L6 empty findings verified:", types.CustodyReport.from_findings([]).verified)
try:
    types.CustodyReport.from_findings([object()])
    print("L6 no-code ACCEPTED")
except types.LoopError as exc:
    print("L6 no-code finding refused:", exc.code)

# L6b empty-string code finding - _text refuses empty
class E:
    code = ""
try:
    types.CustodyReport.from_findings([E()])
    print("L6b empty code ACCEPTED")
except types.LoopError as exc:
    print("L6b empty code refused:", exc.code)
