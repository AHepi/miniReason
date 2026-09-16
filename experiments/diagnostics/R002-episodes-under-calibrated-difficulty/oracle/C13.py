from __future__ import annotations
import json
from _calculations import out
CID='C13'
EXPECTED={'cyclic_count': 3120, 'linear_trap': 5281}
SEALED={'problem_id': 'C13', 'count': 3120}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['cyclic_count']==s['count'], (CID,"sealed mismatch",d,s)
assert d['linear_trap'] != s['count'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'memoized prefix/suffix recurrence',"recommended_independent_check":'position-combination enumeration',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
