"""``build_standard``'s three validators, on the paths they do cover."""
from __future__ import annotations

from dataclasses import replace

import _boot  # noqa: F401

from minireason.loop import standard as S


def run(label: str, **kwargs) -> None:
    try:
        S.build_standard(**kwargs)
    except S.StandardInvalid as exc:
        print("REFUSED  %-46s %-28s %s" % (label, exc.code, exc.detail[:34]))
    else:
        print("ADMITTED %-46s" % label)


regs = dict(S.PLAN_8A_REGISTERS)
print("-- registers --")
run("a register missing", registers={k: v for k, v in regs.items() if k != "G"})
run("a fifth register", registers=dict(regs, X=regs["T"]))
run("a register that is not a Register", registers=dict(regs, G="G"))
run("a register whose id disagrees with its key",
    registers=dict(regs, G=replace(regs["G"], id="Q")))
run("a register with empty plan_text",
    registers=dict(regs, G=replace(regs["G"], plan_text="   ")))
run("a register with no difference_kinds",
    registers=dict(regs, G=replace(regs["G"], difference_kinds=())))
run("a register with a duplicate kind token",
    registers=dict(regs, G=replace(
        regs["G"], difference_kinds=regs["G"].difference_kinds * 2)))

print()
print("-- vocabulary --")
run("empty", vocabulary=())
run("duplicated value", vocabulary=("retains", "retains", "unresolved"))
run("a value outside the six", vocabulary=("is-better-than", "unresolved"))
run("no 'unresolved'", vocabulary=("retains",))

print()
print("-- guard parameters --")
base = dict(S.GUARD_PARAMETERS)
run("an unknown key", params=dict(base, judge_families=2))
run("a missing key", params={k: v for k, v in base.items() if k != "paraphrase_n"})
run("a boolean where an integer is required", params=dict(base, judge_seats=True))
run("judge_seats below the floor", params=dict(base, judge_seats=1))
run("paraphrase_n = 0 (G7 switched off)", params=dict(base, paraphrase_n=0))
run("min_resolved_replicates_per_case = 2", params=dict(base, min_resolved_replicates_per_case=2))
run("an integer where a boolean is required", params=dict(base, order_swap_both_orders=1))
run("an empty unanimity rule", params=dict(base, unanimity_rule="  "))
run("an empty reopen list", params=dict(base, reopen_reasons=()))
run("a reopen reason outside the list",
    params=dict(base, reopen_reasons=("retry-until-it-sticks",)))
run("the shipped defaults (control)")
