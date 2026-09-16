from __future__ import annotations
import json
from _calculations import out
CID='C03'
EXPECTED={'answer': ((4, 7, 3), 501), 'sequential_trap': ((10, 7, 14), 42), 'trace': [(1, 'A', 11, 16, 13), (2, 'B', 1, 8, 8), (3, 'A', 9, 16, 9), (4, 'C', 8, 10, 11), (5, 'B', 10, 4, 15), (6, 'C', 2, 1, 5), (7, 'A', 3, 6, 7), (8, 'B', 13, 4, 3), (9, 'B', 12, 8, 10), (10, 'A', 3, 1, 5), (11, 'C', 6, 11, 9), (12, 'A', 0, 3, 15), (13, 'C', 7, 15, 4), (14, 'B', 1, 1, 6), (15, 'B', 8, 4, 13), (16, 'A', 12, 0, 4), (17, 'C', 13, 11, 7), (18, 'A', 7, 1, 3), (19, 'B', 0, 10, 7), (20, 'C', 4, 7, 3)]}
SEALED={'problem_id': 'C03', 'final': [4, 7, 3], 'H': 501}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert list(d['answer'][0])==s['final'] and d['answer'][1]==s['H'], (CID,"sealed mismatch",d,s)
assert d['sequential_trap'] != d['answer'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'literal snapshot tuple trace',"recommended_independent_check":'affine-matrix trace',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
