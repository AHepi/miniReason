from __future__ import annotations
import json
from _calculations import out
CID='C05'
EXPECTED={'minimum': 611, 'order': 'BHEDGFCA', 'timeline': [('B', 2, 5), ('H', 5, 8), ('E', 8, 9), ('D', 10, 12), ('G', 12, 14), ('F', 15, 19), ('C', 19, 24), ('A', 26, 30)], 'second_cost': 619, 'greedy_trap': {'order': 'BDEGHFCA', 'cost': 740}}
SEALED={'problem_id': 'C05', 'sequence': 'BHEDGFCA', 'timeline': [['B', 2, 5], ['H', 5, 8], ['E', 8, 9], ['D', 10, 12], ['G', 12, 14], ['F', 15, 19], ['C', 19, 24], ['A', 26, 30]], 'objective': 611, 'second_objective': 619}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['order']==s['sequence'] and [list(x) for x in d['timeline']]==s['timeline'] and d['minimum']==s['objective'] and d['second_cost']==s['second_objective'], (CID,"sealed mismatch",d,s)
assert d['greedy_trap']['cost'] != s['objective'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'all-permutation enumeration',"recommended_independent_check":'subset dynamic program',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
