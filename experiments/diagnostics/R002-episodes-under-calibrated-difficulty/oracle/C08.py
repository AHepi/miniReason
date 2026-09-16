from __future__ import annotations
import json
from _calculations import out
CID='C08'
EXPECTED={'trees': 1680, 'containing_01': 900, 'independence_trap': '784'}
SEALED={'problem_id': 'C08', 'spanning_trees': 1680, 'containing_01': 900}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['trees']==s['spanning_trees'] and d['containing_01']==s['containing_01'], (CID,"sealed mismatch",d,s)
assert d['independence_trap'] != str(s['containing_01']), (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'complete seven-edge-subset enumeration',"recommended_independent_check":'matrix-tree deletion/contraction',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
