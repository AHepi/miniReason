"""standard_body round-trip and assert_config_matches_standard behaviour."""
import json
import sys

sys.path.insert(0, "src")

from minireason.loop import standard as s
from minireason.loop.types import SeatsConfig

# 1. standard_body accepts a non-canonical re-serialisation of the same content
body = json.loads(s.STANDARD_BODY)
respelled = json.dumps(body, indent=4, sort_keys=False)
try:
    again = s.standard_body(respelled)
    print("non-canonical respelling accepted:", again == body)
except s.StandardInvalid as e:
    print("non-canonical respelling refused:", e.code, e.detail[:80])

# 2. standard_body with an injected scoring key
tampered = json.loads(s.STANDARD_BODY)
tampered["vocabulary"]["score"] = 5
try:
    s.standard_body(json.dumps(tampered))
    print("scoring-key tamper: accepted")
except s.StandardInvalid as e:
    print("scoring-key tamper: refused ->", e.code)

# 3. standard_body checks schema/spec only; does it validate guard ranges on read?
weakened = json.loads(s.STANDARD_BODY)
weakened["guard_parameters"]["judge_seats"] = 1
weakened["guard_parameters"]["min_judge_families"] = 1
try:
    result = s.standard_body(json.dumps(weakened))
    print("weakened guard params on read: accepted, judge_seats =",
          result["guard_parameters"]["judge_seats"])
except s.StandardInvalid as e:
    print("weakened guard params on read: refused ->", e.code)

# 4. section missing
broken = json.loads(s.STANDARD_BODY)
del broken["ceiling"]
try:
    s.standard_body(json.dumps(broken))
    print("missing ceiling: accepted")
except s.StandardInvalid as e:
    print("missing ceiling: refused ->", e.code)

# 5. SeatsConfig.as_dict() through assert_config_matches_standard
cfg = SeatsConfig.from_mapping({})
d = cfg.as_dict()
print("default SeatsConfig.as_dict():", d)
try:
    s.assert_config_matches_standard(d, None)
    print("default seats block: reconciles")
except s.StandardInvalid as e:
    print("default seats block: refused ->", e.code, e.detail[:120])

# 6. a config that disagrees
cfg2 = SeatsConfig.from_mapping({"paraphrase_n": 3})
try:
    s.assert_config_matches_standard(cfg2.as_dict(), None)
    print("paraphrase_n=3 config: accepted")
except s.StandardInvalid as e:
    print("paraphrase_n=3 config: refused ->", e.code)

# 7. SeatsConfig itself enforces min_judge_families >= #judges? test judges=3
try:
    cfg3 = SeatsConfig.from_mapping({"judges": ["a", "b", "c"]})
    s.assert_config_matches_standard(cfg3.as_dict(), None)
    print("three named judges: accepted")
except Exception as e:
    print("three named judges: refused ->", type(e).__name__, getattr(e, "code", e))

# 8. reopen narrowing admitted, widening refused
try:
    s.assert_config_matches_standard(None, ("new-material",))
    print("narrowed reopen list: accepted")
except s.StandardInvalid as e:
    print("narrowed reopen list: refused ->", e.code)
try:
    s.assert_config_matches_standard(None, ("budget-retry",))
    print("extra reopen reason: accepted")
except s.StandardInvalid as e:
    print("extra reopen reason: refused ->", e.code)

# 9. non-mapping seats argument
try:
    s.assert_config_matches_standard(["critic"], None)
    print("seats-as-list: accepted")
except s.StandardInvalid as e:
    print("seats-as-list: refused ->", e.code)

# 10. seats min_judge_families mismatch
try:
    s.assert_config_matches_standard({"min_judge_families": 3}, None)
    print("min_judge_families=3: accepted")
except s.StandardInvalid as e:
    print("min_judge_families=3: refused ->", e.code)
