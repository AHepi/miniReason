from __future__ import annotations
import json
from _calculations import out
CID='C17'
EXPECTED={'values': [11, 8, 417, 17774, 247103, 1879476, 9809573, 39556682, 132174099, 382736288], 'coefficients': [11, -7, 5, 0, -3, 2, 0, -1, 0, 1], 'p20': 510725921871, 'x7_coefficient': -1, 'degree8_trap_predicted_p9': 382373408}
SEALED={'problem_id': 'C17', 'P20': 510725921871, 'coefficient_x7': -1}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['p20']==s['P20'] and d['x7_coefficient']==s['coefficient_x7'], (CID,"sealed mismatch",d,s)
assert d['degree8_trap_predicted_p9'] != d['values'][9], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'exact Newton forward-difference interpolation',"recommended_independent_check":'rational Lagrange interpolation',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
