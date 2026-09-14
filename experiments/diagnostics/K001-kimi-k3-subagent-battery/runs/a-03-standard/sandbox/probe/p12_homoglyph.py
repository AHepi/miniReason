"""The non-ASCII homoglyph stem: how far it goes through the module's own scan family.

assert_no_exhaustion_claim tokenizes nothing - it searches for the ASCII byte sequence
'exhaust' in the whitespace-flattened, casefolded text. A stem with one look-alike
glyph carries no 'exhaust' byte sequence and is admitted. Same probe against
assert_no_scoring_headers, whose token scan is [A-Za-z][A-Za-z0-9_]* and likewise
cannot see a scoring word spelled with one non-ASCII letter.
"""
from __future__ import annotations

from _probe_setup import check

from minireason.loop import standard


def outcome(text: str, fn, where: str = "probe"):
    try:
        fn(text, where=where)
    except standard.StandardInvalid as exc:
        return ("raised", exc.code)
    return ("ok", None)


def main() -> None:
    # 1. 'exhåusted' (LATIN SMALL LETTER A WITH RING ABOVE inside the stem).
    homo = "The budget was exh\u00e5usted at call 50. Stopping here."
    status, code = outcome(homo, standard.assert_no_exhaustion_claim)
    check("homoglyph 'exhåusted' is admitted by assert_no_exhaustion_claim",
          status == "ok", f"{status} {code}")

    # 2. Same token, UPPER-CASED, then casefold-sensitive check.
    homo_up = "The budget was EXH\u00c5USTED at call 50."
    status, code = outcome(homo_up, standard.assert_no_exhaustion_claim)
    check("upper-cased homoglyph is still admitted",
          status == "ok", f"{status} {code}")

    # 3. The scoring-header sibling: a table header 'sc\u00f8re'.
    table = "| cell | sc\u00f8re |\n|---|---|\n| r1 | 1 |\n"
    status, code = outcome(table, standard.assert_no_scoring_headers)
    check("homoglyph 'scøre' table header is admitted by assert_no_scoring_headers",
          status == "ok", f"{status} {code}")

    # 4. Control: the ASCII spellings ARE refused, so the guard itself is armed.
    status, code = outcome("The budget was exhausted at call 50.",
                           standard.assert_no_exhaustion_claim)
    check("ASCII 'exhausted' is refused (control)",
          status == "raised" and code == "RESOURCE_BOUNDARY_MISDESCRIBED",
          f"{status} {code}")
    status, code = outcome("| cell | score |\n|---|---|\n| r1 | 1 |\n",
                           standard.assert_no_scoring_headers)
    check("ASCII 'score' header is refused (control)",
          status == "raised" and code == "SCORING_KEY_FORBIDDEN", f"{status} {code}")


if __name__ == "__main__":
    main()
