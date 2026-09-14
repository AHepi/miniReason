"""Two follow-ups from p05: (a) T's prefix-intact rule with the right characters;
(b) what standard_body does with a scoring key carried as a VALUE vs as a KEY."""
from __future__ import annotations

import json

from _probe_setup import check

from minireason.loop import standard


def raised(fn):
    try:
        fn()
    except standard.StandardInvalid as exc:
        return exc.code
    except Exception as exc:  # noqa: BLE001 - report whatever happened
        return f"{type(exc).__name__}: {exc}"
    return None


def main() -> None:
    t_text = standard.PLAN_8A_MIRROR["registers"]["T"]["plan_text"]
    print("T plan_text:")
    print(t_text)
    print()
    check("T prefix-intact rule (em dash)",
          "read **with the source artifact prefix intact**" in t_text)
    check("T prefix-intact rule present by substring",
          "with the source artifact prefix intact" in t_text)

    # (b) standard_body with a scoring token as a VALUE, not a key.
    tampered = json.loads(standard.STANDARD_BODY)
    tampered["registers"]["G"]["carries_falsifiers"] = ["score"]
    code = raised(lambda: standard.standard_body(json.dumps(tampered)))
    print(f"standard_body with a VALUE 'score' nested under registers.G: {code!r}")
    check("a scoring KEY nested anywhere raises SCORING_KEY_FORBIDDEN",
          raised(lambda: standard.standard_body(
              json.dumps({**json.loads(standard.STANDARD_BODY), "score": 1}))
          ) == "SCORING_KEY_FORBIDDEN")
    check("a scoring VALUE nested anywhere passes standard_body (finding)",
          code is None, f"returned code {code!r}")

    # And the same input through build_standard's own forbidden-key pass:
    tampered2 = json.loads(standard.STANDARD_BODY)
    tampered2["marks"] = ["differs", "same", "unresolved", "score is value"]
    code2 = raised(lambda: standard.standard_body(json.dumps(tampered2)))
    print(f"standard_body with 'score is value' inside body['marks']: {code2!r}")


if __name__ == "__main__":
    main()
