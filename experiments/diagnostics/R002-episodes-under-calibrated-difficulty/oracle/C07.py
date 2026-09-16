from __future__ import annotations
import json
from _calculations import out
CID='C07'
EXPECTED={'expected_steps': '3373/896', 'absorb_by_5': '209293/259200', 'geometric_trap': '6'}
SEALED={'problem_id': 'C07', 'expected_steps': '3373/896', 'absorbed_by_5': '209293/259200'}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['expected_steps']==s['expected_steps'] and d['absorb_by_5']==s['absorbed_by_5'], (CID,"sealed mismatch",d,s)
assert d['geometric_trap'] != s['expected_steps'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'rational Gaussian elimination plus exact transient-mass propagation',"recommended_independent_check":'independent equation residual and path enumeration',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
