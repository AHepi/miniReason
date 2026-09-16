from __future__ import annotations
import json
from _calculations import out
CID='C02'
EXPECTED={'linear_valid': 2324, 'rotation_classes': 166, 'bracelets': 90, 'reflection_fixed_rotation_classes': 14, 'half_rotation_trap': '83'}
SEALED={'problem_id': 'C02', 'bracelets': 90, 'rotation_classes': 166}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['bracelets']==s['bracelets'] and d['rotation_classes']==s['rotation_classes'], (CID,"sealed mismatch",d,s)
assert d['half_rotation_trap'] != str(s['bracelets']) and d['reflection_fixed_rotation_classes']==14, (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'complete rotation/dihedral orbit canonicalization',"recommended_independent_check":'Burnside fixed-point accounting',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
