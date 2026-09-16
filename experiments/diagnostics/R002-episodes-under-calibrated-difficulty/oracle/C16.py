from __future__ import annotations
import json
from _calculations import out
CID='C16'
EXPECTED={'winning': True, 'remoteness': 13, 'optimal_moves': [(2, 0), (0, 2), (1, 1)], 'four_is_winning_trap': {'outcome': (True, 11), 'optimal_moves': [(1, 0), (0, 1)]}}
SEALED={'problem_id': 'C16', 'winning': True, 'remoteness': 13, 'optimal_first_moves': [[2, 0], [0, 2], [1, 1]]}
d=out[CID]; s=SEALED
assert d==EXPECTED, (CID,"calculation drift",d,EXPECTED)
assert d['winning']==s['winning'] and d['remoteness']==s['remoteness'] and [list(x) for x in d['optimal_moves']]==s['optimal_first_moves'], (CID,"sealed mismatch",d,s)
assert d['four_is_winning_trap']['outcome'] != (d['winning'],d['remoteness']) or d['four_is_winning_trap']['optimal_moves'] != d['optimal_moves'], (CID,"trap was not rejected",d,s)
record={"candidate_id":CID,"oracle_kind":"computable","sealed":s,"calculation":d,"expected_match":True,"trap_rejected":True,"primary_calculation":'memoized minimax recursion',"recommended_independent_check":'bottom-up game table',"recommended_check_executed":False}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
