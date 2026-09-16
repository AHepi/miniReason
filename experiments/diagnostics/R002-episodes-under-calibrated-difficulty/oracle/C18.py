from __future__ import annotations
import json
from _calculations import out
CID='C18'
EXPECTED={'answer': ([('C', 5), ('D', 6), ('B', 7), ('F', 9), ('E', 13), ('A', 16), ('G', 19)], 47), 'arrival_first_trap': ([('C', 4), ('D', 5), ('B', 6), ('F', 8), ('E', 12), ('A', 16), ('G', 19)], 42)}
SEALED={'problem_id': 'C18', 'completions': [['C', 5], ['D', 6], ['B', 7], ['F', 9], ['E', 13], ['A', 16], ['G', 19]], 'turnaround_sum': 47}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert [[x[0],x[1]] for x in d['answer'][0]]==s['completions'] and d['answer'][1]==s['turnaround_sum'], (CID,"sealed mismatch",d,s)
assert d['arrival_first_trap'] != d['answer'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'boundary-ordered event simulation',"recommended_independent_check":'minute-by-minute service ledger',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
