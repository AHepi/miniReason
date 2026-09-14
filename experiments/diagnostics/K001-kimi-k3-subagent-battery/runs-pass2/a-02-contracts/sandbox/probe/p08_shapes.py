"""Probe 8: Validation payload on guard-rail failures; Mapping-vs-dict forms.

 * §2.4: "the block is logged with its reason code". For an unparseable output
   the receipt must fall back to SCHEMA_INVALID. Show what Validation carries
   and what raise_for_failure raises.
 * check() accepts dict only (_as_object). A Mapping that is not a dict is
   refused while its JSON-text twin is accepted: is there a divergence between
   the two documented input forms of the same value?
 * Path determinism on a multiply-broken body.
"""
import sys, os, json, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import contracts
from minireason.loop.contracts import check, SCHEMA_INVALID

# 8a: unknown-role Validation
v = check("decider", {"x": 1})
print(f"8a unknown role: ok={v.ok} role={v.role!r} reason={v.reason!r} "
      f"path={v.path} message={v.message!r}")
try:
    v.raise_for_failure()
except Exception as exc:
    print(f"   raise_for_failure -> {type(exc).__name__} role={exc.role!r} "
          f"reason={exc.reason!r} code={exc.code!r}")

# 8b: marker + unknown register keyword
mk = {"mark": "differs", "difference_kind": "grounds_source",
      "left_quote": "l", "right_quote": "r", "case": "c"}
v = check("marker", mk, register="bogus")
print(f"\n8b marker register='bogus': ok={v.ok} role={v.role!r} reason={v.reason!r} "
      f"code-on-raise=", end="")
try:
    v.raise_for_failure()
except Exception as exc:
    print(exc.code)

# 8c: Mapping-but-not-dict input vs its JSON text form
od = collections.OrderedDict([("answer", "a"), ("concedes", True)])
proxy = __import__("types").MappingProxyType({"answer": "a", "concedes": True})
v_dict = check("defender", dict(od))
v_od = check("defender", od)
v_proxy = check("defender", proxy)
v_text = check("defender", json.dumps({"answer": "a", "concedes": True}))
print(f"\n8c defender input as dict:          ok={v_dict.ok} reason={v_dict.reason}")
print(f"   defender input as OrderedDict:   ok={v_od.ok} reason={v_od.reason}")
print(f"   defender input as MappingProxy:  ok={v_proxy.ok} reason={v_proxy.reason}")
print(f"   defender input as JSON text:     ok={v_text.ok} reason={v_text.reason}")

# 8d: bytes with a BOM / invalid UTF-8
v = check("critic", b"\xff\xfe{}")
print(f"\n8d invalid UTF-8 bytes: ok={v.ok} reason={v.reason}")
v = check("critic", b'\xef\xbb\xbf{}')  # BOM then {}
print(f"   UTF-8 BOM bytes ('bom{{}}'): ok={v.ok} reason={v.reason}")
v = check("critic", '\ufeff{}')
print(f"   str with U+FEFF prefix: ok={v.ok} reason={v.reason}")

# 8e: determinism of first-error selection on multiply-broken output
body = {"zzz": 1, "relation": "bogus-token", "case": 5}  # 3 problems
sigs = set()
for _ in range(3):
    v = check("critic", dict(body))
    sigs.add((v.reason, v.path, v.message))
print(f"\n8e multiply-broken body, 3 runs identical: {len(sigs) == 1}")
print(f"   reported: reason={v.reason} path={v.path}")
print(f"   (relation error message: {[s for s in sigs][0][2][:80]!r})")
print("done")
