from __future__ import annotations
import json
from _calculations import out
CID='C12'
EXPECTED={'most_likely_state': (4, 3, 3), 'probability': '13283197/64012032', 'sixth_red': '107600351813/246446323200', 'states': 22, 'fixed_composition_trap': '1/2'}
SEALED={'problem_id': 'C12', 'most_probable_state': [4, 3, 3], 'state_probability': '13283197/64012032', 'sixth_red': '107600351813/246446323200'}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert list(d['most_likely_state'])==s['most_probable_state'] and d['probability']==s['state_probability'] and d['sixth_red']==s['sixth_red'], (CID,"sealed mismatch",d,s)
assert d['fixed_composition_trap'] != s['sixth_red'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'exact composition-state propagation',"recommended_independent_check":'explicit draw tree',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
