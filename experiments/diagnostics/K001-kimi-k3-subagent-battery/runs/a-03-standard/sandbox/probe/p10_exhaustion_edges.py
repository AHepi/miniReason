"""Sharper attacks on assert_no_exhaustion_claim, each reported as it lands."""
from __future__ import annotations

from _probe_setup import check

from minireason.loop import standard


def outcome(text: str):
    try:
        standard.assert_no_exhaustion_claim(text, where="probe")
    except standard.StandardInvalid as exc:
        return ("raised", exc.code)
    return ("ok", None)


def main() -> None:
    denial = standard.CEILING_EXHAUSTION_DENIAL

    # The denial embedded TWICE: replace removes every occurrence (str.replace
    # replaces all), so two denials both vanish. Not a hole per se; verify.
    double = f"The denial says: {denial}. And once more: {denial}."
    print(f"double-denial: {outcome(double)}")

    # The denial joined INSIDE a claim, so removing it concatenates the halves:
    #   "was exhaust" + DENIAL + "ive of the budget"
    # after removal -> "was exhaust ive" -> flattened to "exhaust ive" and the
    # stem 'exhaust' survives (it is contiguous within the first half).
    around = "the run was exhaust " + denial + "ive when it stopped"
    status, code = outcome(around)
    check("a claim wrapped around the denial still carries the stem and is refused",
          status == "raised", f"{status} {code}")

    # Stem split ONLY by the flattening: "exhaust" + NBSP + "ed". str.split()
    # splits on NBSP, so the join leaves 'exhaust ed' — stem still contiguous?
    nbsp = "the budget was exhaust\u00a0ed at call 50"
    status, code = outcome(nbsp)
    print(f"nbsp inside the stem: {status} {code}")
    check("an NBSP inside the stem is caught after flattening",
          status == "raised", f"{status} {code}")

    # Stem split by a zero-width space: split() does NOT split on U+200B.
    zwsp = "the budget was exhaust\u200bed at call 50"
    status, code = outcome(zwsp)
    print(f"zero-width space inside the stem: {status} {code}")
    check("a zero-width space inside the stem defeats the scan",
          status == "ok", f"{status} {code}")

    # Stem spelled with a look-alike: 'exhåust'. A pure ASCII scan cannot see it.
    lookalike = "the budget was exh\u00e5usted at call 50"
    status, code = outcome(lookalike)
    print(f"a look-alike stem: {status} {code}")
    check("a non-ASCII look-alike stem defeats the scan",
          status == "ok", f"{status} {code}")

    # And the plain, honest way to say it, which must PASS (this is the outcome
    # the whole house style wants to be legal):
    fine = "Cycle budget reached at cycle 9 of 9: a declared resource boundary; reopen on new material."
    status, code = outcome(fine)
    check("an honest resource-boundary sentence passes", status == "ok", f"{status}")


if __name__ == "__main__":
    main()
