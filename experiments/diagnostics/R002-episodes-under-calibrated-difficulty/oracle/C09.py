from __future__ import annotations
import json
from _calculations import out
CID='C09'
EXPECTED={'probability': '4129056/244140625', 'matching_words': 59, 'sequential_trap': '2729376/244140625'}
SEALED={'problem_id': 'C09', 'probability': '4129056/244140625', 'matching_strings': 59}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['probability']==s['probability'] and d['matching_words']==s['matching_strings'], (CID,"sealed mismatch",d,s)
assert d['sequential_trap'] != s['probability'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'complete weighted word enumeration',"recommended_independent_check":'weighted state/count dynamic program',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
