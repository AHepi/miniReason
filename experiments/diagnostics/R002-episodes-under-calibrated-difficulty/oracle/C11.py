from __future__ import annotations
import json
from _calculations import out
CID='C11'
EXPECTED={'minimum': 26, 'order': 'FABCDEGH', 'second_cost': 27, 'unconstrained_trap': (23, 'BADCEFGH')}
SEALED={'problem_id': 'C11', 'sequence': 'FABCDEGH', 'minimum': 26, 'second_distinct': 27}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['order']==s['sequence'] and d['minimum']==s['minimum'] and d['second_cost']==s['second_distinct'], (CID,"sealed mismatch",d,s)
assert d['unconstrained_trap'][0] != s['minimum'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'precedence-feasible permutation enumeration',"recommended_independent_check":'precedence-ideal dynamic program',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
