"""_validate_params coverage and build_standard refusal checks."""
import sys

sys.path.insert(0, "src")

from minireason.loop import standard as s

base = dict(s.GUARD_PARAMETERS)


def attempt(label, params):
    try:
        s.build_standard(params=params)
        print(f"{label}: accepted")
    except s.StandardInvalid as e:
        print(f"{label}: refused -> {e.code} | {e.detail[:90]}")

# control: the frozen params build
attempt("frozen params", base)

# int params: type and range
p = dict(base); p["judge_seats"] = 1; attempt("judge_seats=1", p)          # below range
p = dict(base); p["judge_seats"] = True; attempt("judge_seats=True", p)    # bool is an int
p = dict(base); p["paraphrase_n"] = 2.0; attempt("paraphrase_n=2.0 float", p)
p = dict(base); p["paraphrase_n"] = 9; attempt("paraphrase_n=9", p)
p = dict(base); p["min_judge_families"] = 1; attempt("min_judge_families=1 (< judge_seats=2)", p)

# bool params
p = dict(base); p["order_swap_both_orders"] = "yes"; attempt("order_swap='yes'", p)
p = dict(base); p["marker_reuses_judge_seats"] = 1; attempt("marker_reuses=1 int", p)

# unanimity_rule
p = dict(base); p["unanimity_rule"] = 0; attempt("unanimity_rule=0", p)
p = dict(base); p["unanimity_rule"] = None; attempt("unanimity_rule=None", p)
p = dict(base); p["unanimity_rule"] = "Every judge seat, majority fallback"; attempt("majority rule", p)

# reopen_reasons
p = dict(base); p["reopen_reasons"] = 0; attempt("reopen_reasons=0", p)
p = dict(base); p["reopen_reasons"] = ["new-material", "new-material"]; attempt("reopen duplicate", p)
p = dict(base); p["reopen_reasons"] = ("retry",); attempt("unlisted reopen reason", p)
p = dict(base); p["reopen_reasons"] = None; attempt("reopen_reasons=None", p)

# missing key: unanimity_rule removed
p = dict(base); del p["unanimity_rule"]; attempt("unanimity_rule missing", p)

# build with narrowed vocabulary / register edits
try:
    s.build_standard(vocabulary=["retains", "unresolved"])
    print("narrowed vocabulary: accepted")
except s.StandardInvalid as e:
    print("narrowed vocabulary: refused ->", e.code, "|", e.detail[:90])

try:
    s.build_standard(vocabulary=list(s.READING_VOCABULARY) + ["invents"])
    print("extended vocabulary: accepted")
except s.StandardInvalid as e:
    print("extended vocabulary: refused ->", e.code, "|", e.detail[:90])

# register tamper
reg = dict(s.PLAN_8A_REGISTERS)
broken = s.Register(id="T", name="t", plan_text="  ", reads="r", differs_iff="d",
                    difference_kinds=reg["T"].difference_kinds, carries_falsifiers=())
reg["T"] = broken
try:
    s.build_standard(registers=reg)
    print("empty plan_text register: accepted")
except s.StandardInvalid as e:
    print("empty plan_text register: refused ->", e.code)
