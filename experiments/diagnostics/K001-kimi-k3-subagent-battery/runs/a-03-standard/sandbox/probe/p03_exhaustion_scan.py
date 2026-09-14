"""Assertable behaviour of standard.assert_no_exhaustion_claim.

Claim under test (WAVE0-INTERFACE, wave-plan W3-REPORT acceptance, and
standard.py's own docstring): the frozen ceiling passes; a record that anywhere
describes a boundary as the inquiry running out raises RESOURCE_BOUNDARY_MISDESCRIBED;
the one exemption is CEILING_EXHAUSTION_DENIAL, whitespace- and case-insensitive.
"""
from __future__ import annotations

from _probe_setup import check

from minireason.loop import standard


def outcome(text: str):
    try:
        standard.assert_no_exhaustion_claim(text, where="probe")
    except standard.StandardInvalid as exc:
        return ("raised", exc.code, str(exc)[:110])
    return ("ok", None, None)


def main() -> None:
    status, code, _msg = outcome(standard.CEILING_TEXT)
    check("the frozen ceiling passes its own scan", status == "ok", f"{status} {code}")

    denial = standard.CEILING_EXHAUSTION_DENIAL  # "not exhaustion of the inquiry"

    # 1. The banner's own phrase: "exhaustive", an adjective, not a boundary claim.
    banner_phrase = "a thorough and exhaustive reading of the material"
    status, code, msg = outcome(banner_phrase)
    check("a mere 'exhaustive' adjective is refused",
          status == "raised" and code == "RESOURCE_BOUNDARY_MISDESCRIBED",
          f"{status} {code} {msg}")

    # 2. The docstring's own smuggle claim: a claim built AROUND the denial, so that
    #    removing the denial concatenates the halves and the stem survives the join.
    suffix = "ed"
    joined = "the budget was " + "not " + "exhaust" + suffix[:0] + "ed"
    print(f"joined without the smuggle reads: {joined!r}")
    smuggled = ("the run stopped because the analysis was not "
                + "EXHAUSTION of the inquiry, we assert; still, it was exhaust"
                + "ed in the end")
    status, code, msg = outcome(smuggled)
    check("a claim built around the denial is caught after the join",
          status == "raised" and code == "RESOURCE_BOUNDARY_MISDESCRIBED",
          f"{status} {code} {msg}")

    # 3. The exemption is only the ONE phrase. Split-casing it leaves a bare stem.
    split_case = "Not exhaustion of the inquiry. The inquiry was exhausted."
    status, code, msg = outcome(split_case)
    check("the denial exempted once; a second bare stem is refused",
          status == "raised" and code == "RESOURCE_BOUNDARY_MISDESCRIBED",
          f"{status} {code} {msg}")

    # 4. Whitespace-insensitive exemption: re-wrapped denial in a wider record is ok.
    rewrapped = ("A reached ceiling is a declared resource boundary,\n"
                 "not   exhaustion\n"
                 "of the inquiry, and this record states which was reached.")
    status, code, _msg = outcome(rewrapped)
    check("a re-wrapped denial is still the exemption", status == "ok", status)

    # 5. A resource-boundary sentence with NO stem is fine (sanity).
    plain = "The token budget was reached at call 41 of 50. This is a declared resource boundary."
    status, code, _msg = outcome(plain)
    check("a plain resource-boundary sentence passes", status == "ok", status)


if __name__ == "__main__":
    main()
