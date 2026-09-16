from __future__ import annotations
import json
from _calculations import out
CID='C14'
EXPECTED={'answer': (20369, 309202), 'one_is_prime_trap': (21187, 361799), 'trace': [(0, 52), (1, 72), (2, 103), (3, 146), (4, 197), (5, 278), (6, 373), (7, 524), (8, 701), (9, 937), (10, 1252), (11, 1755), (12, 2343), (13, 3282), (14, 4379), (15, 5841), (16, 7791), (17, 10909), (18, 14548), (19, 20369)]}
SEALED={'problem_id': 'C14', 'x_20': 20369, 'H': 309202}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['answer'][0]==s['x_20'] and d['answer'][1]==s['H'], (CID,"sealed mismatch",d,s)
assert d['one_is_prime_trap'] != d['answer'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'literal integer recurrence trace',"recommended_independent_check":'quotient/remainder trace certificates',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
