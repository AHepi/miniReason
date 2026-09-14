"""The ceiling's block-register clause (clause 7) names nine reason codes. The
module docstring says 'Ceiling clause seven fixes nine block reason codes by name'
and that types.BLOCK_CODES carries all nine plus blocked:constitution. Check the
correspondence in both directions, the way the docstring claims a test does.
"""
from __future__ import annotations

import re

from _probe_setup import check

from minireason.loop import standard, types


def main() -> None:
    # Clause 7 is the one containing 'block register by reason code'.
    clause = next(s for s in standard.CEILING_REQUIRED_SENTENCES
                  if "block register" in s)
    print("clause 7:", clause[:200], "...")
    named = re.findall(r"`([a-z-]+)`", clause)
    print("codes extracted from clause 7:", named)
    check("clause 7 names the same nine, in the ceiling's order",
          list(types.CEILING_BLOCK_REASONS) == named, f"{named}")
    check("every ceiling-named reason maps to a member of BLOCK_CODES",
          all("blocked:" + r in types.BLOCK_CODES for r in types.CEILING_BLOCK_REASONS))
    check("BLOCK_CODES carries exactly the nine plus blocked:constitution",
          types.BLOCK_CODES
          == {"blocked:" + r for r in types.CEILING_BLOCK_REASONS}
          | {"blocked:constitution"},

          f"extra: {sorted(types.BLOCK_CODES - {'blocked:' + r for r in types.CEILING_BLOCK_REASONS})}")

    # The ceiling's trichotomy, machine-checked against the ceiling text itself.
    check("'unread', 'unresolved' and 'machine-unresolved' are three distinct ceiling tokens",
          all(t in standard.CEILING_TEXT
              for t in ("*unread*", "*unresolved*", "*machine-unresolved*")))


if __name__ == "__main__":
    main()
