from __future__ import annotations
import json
from _derivation_certificates import check
CID='C21'
SEALED={'problem_id': 'C21', 'closed_form': 'a_n(x)=sum_{j=0}^{n-1}x^j', 'at_x_1': 'a_n(1)=n'}
check_result=check(CID)
assert check_result["certificate_passed"], (CID,check_result)
assert check_result["trap_check"]["passed"], (CID,check_result)
record={"candidate_id":CID,"oracle_kind":"derivation-only","sealed":SEALED,"expected_match":True,"trap_rejected":True,"certificate_check":check_result,"universal_proof_claimed_by_script":False,"human_derivation_is_oracle":True}
print(json.dumps(record,separators=(",",":"),sort_keys=True))
