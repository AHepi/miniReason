from __future__ import annotations
import json
from _calculations import out
CID='C04'
EXPECTED={'answer': [('Blue', 2, 3, 17, 3), ('Gold', 2, 2, 12, 3)], 'where_trap': [('Blue', 2, 3, 17, 3), ('Gold', 1, 2, 12, 2)]}
SEALED={'problem_id': 'C04', 'rows': [['Blue', 2, 3, 17, 3], ['Gold', 2, 2, 12, 3]]}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert [list(x) for x in d['answer']]==s['rows'], (CID,"sealed mismatch",d,s)
assert d['where_trap'] != d['answer'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'bag-semantics interpreter',"recommended_independent_check":'direct SQLite execution',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
