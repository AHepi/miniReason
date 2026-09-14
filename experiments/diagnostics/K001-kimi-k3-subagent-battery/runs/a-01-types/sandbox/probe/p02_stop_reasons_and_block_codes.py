"""BLOCKER attack: the 'exhaustion' acceptance clause and the block table.

W0-TYPES acceptance (design-s7-wave-plan.md) says:
  "the token 'exhaustion' appears in no vocabulary; every block code used
   anywhere in the package is a member of BLOCK_CODES."

We test:
  T1 - 'exhaustion' not in STOP_REASONS and not rendered by is_stop_reason.
  T2 - block_code() refuses a non-BLOCK_CODES reason.
  T3 - a member of CEILING_BLOCK_REASONS that block_code() refuses
       (drift between the ceiling's prose and the closed table).
  T4 - STOP_REASONS rejects the empty parameterised form and whitespace form.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop import types

print("T1 'exhaustion' in STOP_REASONS:", "exhaustion" in types.STOP_REASONS)
print("T1 is_stop_reason('exhaustion'):", types.is_stop_reason("exhaustion"))

# every ceiling reason is a block code member?
missing = [r for r in types.CEILING_BLOCK_REASONS
           if types.BLOCK_CODE_PREFIX + r not in types.BLOCK_CODES]
print("T3 ceiling reasons missing from BLOCK_CODES:", missing)

try:
    types.block_code("not-a-reason")
    print("T2 block_code accepted junk")
except types.LoopError as exc:
    print("T2 refused:", exc.code)

for tok in ("preregistered_condition:", "preregistered_condition: ",
            "preregistered_condition:valid", "preregistered_condition:valid-id_1"):
    print("T4", repr(tok), "->", types.is_stop_reason(tok))
