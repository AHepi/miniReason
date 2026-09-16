from __future__ import annotations
import json
from _derivation_certificates import check
CID='C22'
SEALED={'problem_id': 'C22', 'P(x)': 'x^4'}
check_result=check(CID)
assert check_result["certificate_passed"], (CID,check_result)
assert check_result["trap_check"]["passed"], (CID,check_result)
record={"candidate_id":CID,"oracle_kind":"derivation-only","sealed":SEALED,"expected_match":True,"trap_rejected":True,"certificate_check":check_result,"universal_proof_claimed_by_script":False,"human_derivation_is_oracle":True}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
