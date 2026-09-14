"""assert_config_matches_standard — the reconciliation standard.py claims settles
which of two owners of the guard parameters wins (deviation 8, and the
SeatsConfig docstring). Probe both directions: refusal, and the holes a config
could pass through while disagreeing with the pinned standard.
"""
from __future__ import annotations

import json

from _probe_setup import check

from minireason.loop import standard


def raised(fn) -> str | None:
    try:
        fn()
    except standard.StandardInvalid as exc:
        return exc.code
    return None


def main() -> None:
    # The intended refuse paths fire.
    code = raised(lambda: standard.assert_config_matches_standard(
        {"min_judge_families": 3}, None))
    check("seats.min_judge_families=3 contradicting the pinned 2 is refused",
          code == "GUARD_PARAMETER_INVALID", f"{code}")

    code = raised(lambda: standard.assert_config_matches_standard(
        {"paraphrase_n": 1}, None))
    check("seats.paraphrase_n=1 contradicting the pinned 2 is refused",
          code == "GUARD_PARAMETER_INVALID", f"{code}")

    code = raised(lambda: standard.assert_config_matches_standard(
        {"schema_repair_budget": 1}, None))
    check("seats.schema_repair_budget=1 contradicting the pinned 0 is refused",
          code == "GUARD_PARAMETER_INVALID", f"{code}")

    code = raised(lambda: standard.assert_config_matches_standard(
        {"judges": ["e1", "e2", "e3"]}, None))
    check("naming 3 judge seats against frozen judge_seats=2 is refused",
          code == "GUARD_PARAMETER_INVALID", f"{code}")

    code = raised(lambda: standard.assert_config_matches_standard(
        None, ["repaired-guard", "retry-until-pass"]))
    check("an unlisted reopen reason is refused",
          code == "REOPEN_REASON_UNKNOWN", f"{code}")

    code = raised(lambda: standard.assert_config_matches_standard(None, None))
    check("None/None (the module default) reconciles",
          code is None, f"{code}")

    # Now probe the seam boundaries. GUARD_PARAMETERS has twelve keys.
    print("GUARD_PARAMETERS:", sorted(standard.GUARD_PARAMETERS))
    print("_SEATS_TO_GUARD:", sorted(standard._SEATS_TO_GUARD))

    # A seats mapping that disagrees with GUARD_PARAMETERS but only on keys
    # assert_config_matches_standard never compares:
    odd = {
        "critic": "e1",           # a seat NAME, not a count
        "defender": "e2",
        "variator": "e3",
        "min_judge_families": 2,
        "paraphrase_n": 2,
        "schema_repair_budget": 0,
        "critic_seats": 99,       # contradicts GUARD_PARAMETERS['critic_seats'] == 1
        "defender_seats": 99,     # contradicts GUARD_PARAMETERS['defender_seats'] == 1
        "judge_seats": 99,        # contradicts GUARD_PARAMETERS['judge_seats'] == 2
        "variator_seats": 99,     # contradicts GUARD_PARAMETERS['variator_seats'] == 1
        "order_swap_both_orders": False,  # contradicts GUARD_PARAMETERS (frozen True)
        "min_resolved_replicates_per_case": 99,  # contradicts frozen 3
        "marker_reuses_judge_seats": False,      # contradicts frozen True
        "unanimity_rule": "we vote",             # contradicts the frozen text
    }
    code = raised(lambda: standard.assert_config_matches_standard(odd, None))
    print(f"assert_config_matches_standard(odd seats, None): {code!r}")
    check("all nine disagreements pass unreconciled",
          code is None, f"returned {code!r}")

    # The narrowed reopen list is allowed by design:
    code = raised(lambda: standard.assert_config_matches_standard(
        None, ["new-material"]))
    check("narrowing reopen_reasons to one member is admitted (documented: may narrow)",
          code is None, f"{code}")


if __name__ == "__main__":
    main()
