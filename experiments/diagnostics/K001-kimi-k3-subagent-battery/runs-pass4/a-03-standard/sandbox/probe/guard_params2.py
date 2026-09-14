"""Remaining guard-param edge cases, catching undeclared exception types."""
import sys

sys.path.insert(0, "src")

from minireason.loop import standard as s

base = dict(s.GUARD_PARAMETERS)


def attempt(label, **kwargs):
    try:
        s.build_standard(**kwargs)
        print(f"{label}: accepted")
    except s.StandardInvalid as e:
        print(f"{label}: refused -> {e.code} | {e.detail[:90]}")
    except Exception as e:
        print(f"{label}: UNDECLARED {type(e).__name__}: {e}")

p = dict(base); p["reopen_reasons"] = 0; attempt("reopen_reasons=0", params=p)
p = dict(base); p["reopen_reasons"] = None; attempt("reopen_reasons=None", params=p)
p = dict(base); p["reopen_reasons"] = ["new-material", "new-material"]; attempt("reopen duplicate", params=p)
p = dict(base); p["reopen_reasons"] = ("retry",); attempt("unlisted reopen reason", params=p)
p = dict(base); p["reopen_reasons"] = []; attempt("reopen empty", params=p)
p = dict(base); del p["unanimity_rule"]; attempt("unanimity_rule missing", params=p)
p = dict(base); p["unanimity_rule"] = ["x"]; attempt("unanimity_rule list", params=p)

# vocabulary edges
attempt("vocabulary as bare string 'retains'", vocabulary="retains")
attempt("vocabulary with duplicate", vocabulary=["retains", "retains", "unresolved"])
attempt("vocabulary without unresolved", vocabulary=[v for v in s.READING_VOCABULARY if v != "unresolved"])

# register tamper
reg = dict(s.PLAN_8A_REGISTERS)
broken = s.Register(id="T", name="t", plan_text="  ", reads="r", differs_iff="d",
                    difference_kinds=reg["T"].difference_kinds, carries_falsifiers=())
reg["T"] = broken
attempt("empty plan_text register", registers=reg)

# G11 docstring of assert_config_matches_standard: code for seat param mismatch
try:
    s.assert_config_matches_standard({"paraphrase_n": 1}, None)
    print("paraphrase_n=1 via config reconciliation: accepted")
except s.StandardInvalid as e:
    print("paraphrase_n=1 via config reconciliation: refused ->", e.code)
