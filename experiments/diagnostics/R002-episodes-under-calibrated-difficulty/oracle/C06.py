from __future__ import annotations
import json
from _calculations import out
CID='C06'
EXPECTED={'count': 27, 'lex_D_before_R': 'DDRDDRDDRRDRRDRDRR', 'at_least_one_trap': 41}
SEALED={'problem_id': 'C06', 'count': 27, 'first': 'DDRDDRDDRRDRRDRDRR'}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['count']==s['count'] and d['lex_D_before_R']==s['first'], (CID,"sealed mismatch",d,s)
assert d['at_least_one_trap'] != s['count'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'complete move-string enumeration',"recommended_independent_check":'run/checkpoint dynamic program',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
