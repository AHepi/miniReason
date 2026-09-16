from __future__ import annotations
import json
from _calculations import out
CID='C10'
EXPECTED={'count': 1, 'least': 1912, 'sum_mod_2520': 1912, 'solutions': [1912], 'omitted_offset_trap': {'count': 1, 'least': 1142, 'sum': 1142}}
SEALED={'problem_id': 'C10', 'count': 1, 'least': 1912, 'sum_mod_2520': 1912}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['count']==s['count'] and d['least']==s['least'] and d['sum_mod_2520']==s['sum_mod_2520'], (CID,"sealed mismatch",d,s)
assert d['omitted_offset_trap']['least'] != s['least'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'complete residue enumeration',"recommended_independent_check":'CRT/small-modulus affine composition',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
