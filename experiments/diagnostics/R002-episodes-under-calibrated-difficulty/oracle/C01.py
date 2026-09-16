from __future__ import annotations
import json
from _calculations import out
CID='C01'
EXPECTED={'posterior_C': '25/129', 'next_red': '224/387', 'weights': {'A': '2/35', 'B': '12/245', 'C': '5/196'}, 'with_replacement_trap': {'posterior_C': '83349/373141', 'next_red': '30951965/62687688'}}
SEALED={'problem_id': 'C01', 'posterior_C': '25/129', 'next_red': '224/387'}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['posterior_C']==s['posterior_C'] and d['next_red']==s['next_red'], (CID,"sealed mismatch",d,s)
assert d['with_replacement_trap']['posterior_C'] != s['posterior_C'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'exact ordered likelihood arithmetic',"recommended_independent_check":'indexed-card path enumeration',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
