"""Round-trip and identity claims of W0-STANDARD."""
import sys

sys.path.insert(0, "src")
sys.path.insert(0, ".")

from deepreason_core.canonical import canonical_json, sha256_hex
from minireason import use_relation_h005
from minireason.loop import standard as s

print("STANDARD_BODY == build_standard():", s.STANDARD_BODY == s.build_standard())
print("STANDARD_BODY_SHA256 == sha256_hex(STANDARD_BODY):",
      s.STANDARD_BODY_SHA256 == sha256_hex(s.STANDARD_BODY))
parsed = s.standard_body(s.STANDARD_BODY)
print("standard_body(STANDARD_BODY) parses: OK, sections:", len(parsed))
print("standard_body(str form) equal:", s.standard_body(s.STANDARD_BODY.decode()) == parsed)

# identity claims
print("READING_VOCABULARY is ROOT_READING_VOCABULARY:",
      s.READING_VOCABULARY is use_relation_h005.ROOT_READING_VOCABULARY)
print("READING_BANNER is USE_RELATION_BANNER:",
      s.READING_BANNER is use_relation_h005.USE_RELATION_BANNER)
print("REGISTERS is REGISTER_IDS:", s.REGISTERS is s.REGISTER_IDS)

# ceiling clause partition
print("CEILING_REQUIRED_SENTENCES count:", len(s.CEILING_REQUIRED_SENTENCES))
print("template has placeholder '…':", "…" in s.CEILING_CLAIM_TEMPLATE)
print("every required sentence single-line:",
      all("\n" not in t for t in s.CEILING_REQUIRED_SENTENCES))
print("CEILING_EXHAUSTION_DENIAL in CEILING_TEXT:",
      s.CEILING_EXHAUSTION_DENIAL in s.CEILING_TEXT)

# VOCABULARY_NOTE vs the published docstring text of ROOT_READING_VOCABULARY
import re
doc = use_relation_h005.__doc__  # module docstring does not hold the note; the comment does
src = open("src/minireason/use_relation_h005.py", encoding="utf-8").read()
note_lines = s.VOCABULARY_NOTE.splitlines()
all_present = all(line.strip("#: ").strip() in src for line in note_lines)
print("VOCABULARY_NOTE lines present in source:", all_present)

# falsifier map claim: G carries none
print("G carries any falsifier:",
      any(f.carries("G") for f in s.FALSIFIER_MAP.values()))
print("FALSIFIER_MAP keys:", sorted(s.FALSIFIER_MAP))
print("_CARRIES from registers:",
      {rid: reg.carries_falsifiers for rid, reg in s.PLAN_8A_REGISTERS.items()})

# CRITIC_RELATIONS contents
print("CRITIC_RELATIONS:", s.CRITIC_RELATIONS)
print("NOMINABLE_RELATIONS:", s.NOMINABLE_RELATIONS)

# mirrors of material falafelifier text
print("D1 rule starts:", s.FALSIFIER_MAP["D1"].rule[:60])
