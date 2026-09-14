"""Probe 4: the G12 forbidden-key guard.

Claims tested:
 * contracts module docstring: a str/bytes argument "is now a
   :class:`ContractError`".
 * contracts docstring on the mirrored key set: "The behaviour of the guard
   here is identical to the tool's except that it also descends into tuples".
 * "a scoring key nested anywhere raises SCORING_KEY_FORBIDDEN" (W0-CONTRACTS
   acceptance).
 * O2: the vendored warrant's `verdict` field collides with FORBIDDEN_KEYS and
   the guard must never run over the vendored Warrant record.
"""
import sys, os, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts, standard
from minireason.loop.contracts import (
    assert_no_scoring_keys, assert_no_scoring_headers, ScoringKeyForbidden,
    ContractError, FORBIDDEN_KEYS, CONTRACT_VIOLATION,
)
from minireason.loop.standard import StandardInvalid

def outcome(fn, *a, **kw):
    try:
        fn(*a, **kw)
        return "passed silently"
    except Exception as exc:
        return "raised %s code=%s" % (type(exc).__name__, getattr(exc, 'code', '-'))

# 4a: a bare str / bytes at the root
print("4a guard('score: 1')            ->", outcome(assert_no_scoring_keys, 'score: 1'))
print("4a guard(b'score: 1')           ->", outcome(assert_no_scoring_keys, b'score: 1'))
print("4a guard(bytearray)             ->", outcome(assert_no_scoring_keys, bytearray(b'score: 1')))
try:
    assert_no_scoring_keys("score: 1")
except Exception as exc:
    print("4a isinstance ContractError:", isinstance(exc, ContractError),
          " type name:", type(exc).__name__, " str:", str(exc))

# 4b: case folding, both implementations
print("\n4b contracts, {'x':[{'SCORE':1}]} ->",
      outcome(assert_no_scoring_keys, {'x': [{'SCORE': 1}]}))
print("4b standard._refuse {'x':[{'SCORE':1}]} ->",
      outcome(standard._refuse_forbidden_keys, {'x': [{'SCORE': 1}]}))
raw_body = '{"schema": "x", "verdict": 1}'
print("4b standard.standard_body on", raw_body, "->",
      outcome(standard.standard_body, raw_body))

# 4c: tuple descent (contracts) vs not (standard's private copy)
t = {"a": ({"score": 1},)}
print("\n4c contracts nested-in-tuple ->", outcome(assert_no_scoring_keys, t))
print("4c standard  nested-in-tuple ->", outcome(standard._refuse_forbidden_keys, t))

# 4d: mapping SUBCLASS as the root value (Mapping check vs dict check)
od = collections.OrderedDict({"verdict": "fail"})
print("\n4d contracts OrderedDict root ->", outcome(assert_no_scoring_keys, od))
print("4d standard._refuse OrderedDict ->", outcome(standard._refuse_forbidden_keys, od))

# 4e: O2 — the vendored warrant record
from deepreason_core.ontology.warrant import Warrant
import inspect
wfields = [ln.strip() for ln in inspect.getsource(Warrant).splitlines()
           if 'verdict' in ln.lower()][:4]
print("\n4e Warrant source lines mentioning verdict:", wfields)
w = Warrant(kind=1, commitment="c", transcript="t", verdict="fail")
d = w.as_dict()
print("4e Warrant.as_dict() keys:", sorted(d), " verdict value:", repr(d.get('verdict')))
print("4e guard over Warrant.as_dict() ->", outcome(assert_no_scoring_keys, d))

# 4f: assert_no_scoring_headers over a table header and a heading
md_bad = "| cell | score |\n|---|---|\n| a | b |\n"
print("\n4f headers over bad table ->", outcome(assert_no_scoring_headers, md_bad))
print("4f headers over '# Verdicts' heading ->",
      outcome(assert_no_scoring_headers, '# Verdicts of the run'))
print("4f headers over prose with the word score ->",
      outcome(assert_no_scoring_headers, 'This sentence contains the word score in prose.'))

# 4g: other containers
print("\n4g guard over a set ->", outcome(assert_no_scoring_keys, {('score',)}))
print("done")
