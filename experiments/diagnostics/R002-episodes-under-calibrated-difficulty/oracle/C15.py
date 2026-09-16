from __future__ import annotations
import json
from _calculations import out
CID='C15'
EXPECTED={'answer': (4, 'S-wait-A-T'), 'vertex_only_trap': (9, 'S-A-T')}
SEALED={'problem_id': 'C15', 'arrival': 4, 'route': 'S-wait-A-T'}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['answer'][0]==s['arrival'] and d['answer'][1]==s['route'], (CID,"sealed mismatch",d,s)
assert d['vertex_only_trap'][0] != s['arrival'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'parity-state Dijkstra',"recommended_independent_check":'time-expanded reachability',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
