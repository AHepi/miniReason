"""Probe 4b: O2 — the vendored Warrant's own `verdict` field vs the G12 guard.

O2 (notes/WAVE0-INTERFACE.md): "Design D2 gives the reading warrant
`verdict: \"fail\"`; `verdict` is a member of FORBIDDEN_KEYS ... keep both ... Run
`assert_no_scoring_keys` over artifact content only, never over the vendored
`Warrant`/`Commitment` records".

Check that Warrant.as_dict() indeed carries a forbidden key and that the guard
fires on it (i.e. O2's premise is real in this sandbox).
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from deepreason_core.ontology.warrant import Warrant, WarrantType
from deepreason_core.ontology.commitment import Commitment

from minireason.loop.contracts import assert_no_scoring_keys, FORBIDDEN_KEYS, ScoringKeyForbidden

w = Warrant(id="w1", target="a1", type=WarrantType.DEMONSTRATIVE,
            commitment="k", verdict="fail", trace_ref="blob:x",
            validity_node="vn1")
d = w.model_dump(mode="json")
print("Warrant dict keys:", sorted(d))
print("verdict value:", repr(d.get("verdict")))

try:
    assert_no_scoring_keys(d)
    print("guard over Warrant record: passed silently")
except Exception as exc:
    print(f"guard over Warrant record: raised {type(exc).__name__} "
          f"code={getattr(exc, 'code', '-')} path={getattr(exc, 'path', '-')}")

# also the Commitment record (O2 names both)
import inspect
src = inspect.getsource(Commitment)
hits = [ln.strip() for ln in src.splitlines()
        if any(tok in ln.lower() for tok in FORBIDDEN_KEYS)][:6]
print("Commitment source lines w/ forbidden tokens:", hits)
print("done")
