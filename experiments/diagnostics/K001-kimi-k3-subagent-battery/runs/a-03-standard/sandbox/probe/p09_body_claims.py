"""The docstring's own claims of the shipped body, machine-checked:

- "every integer in the built body lies under guard_parameters or under
  role_contracts.word_limits" (module docstring, 'What this module refuses to do');
- "It emits no scalar meter, no rank, no score and no aggregate" — FORBIDDEN_KEYS
  as neither keys nor value substrings anywhere in the built body;
- StandardInvalid is a LoopError and a ValueError (interface note §2);
- every code the module raises is in types.FAILURE_CODES (interface note §2);
- 'G3 — operative target (R10)' vs the rubric: where does R10 actually live.
"""
from __future__ import annotations

import json

from _probe_setup import check

from minireason.loop import standard, types


def walk_ints(value, path=()):
    if isinstance(value, bool):
        return
    if isinstance(value, int):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_ints(item, path + (str(key),))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            yield from walk_ints(item, path + (str(index),))


def walk_strings(value, path=()):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str):
                yield path + ("<key>",), key
            yield from walk_strings(item, path + (str(key),))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            yield from walk_strings(item, path + (str(index),))


def main() -> None:
    body = json.loads(standard.STANDARD_BODY)

    ints = list(walk_ints(body))
    print("integers in the built body:")
    for path, value in ints:
        print(f"    {'/'.join(path)} = {value}")

    allowed_prefixes = ("guard_parameters/", "role_contracts/word_limits/")
    bad = [("/".join(path), value) for path, value in ints
           if not "/".join(path).startswith(allowed_prefixes)]
    check("every integer lies under guard_parameters/ or role_contracts/word_limits/",
          not bad, f"violations: {bad}")

    # No forbidden token as a KEY (build-time _refuse_forbidden_keys), and no
    # forbidden token as a word inside any string VALUE of the body.
    key_hits = [(path, s) for path, s in walk_strings(body)
                if path and path[-1] == "<key>"
                and s.lower() in standard.FORBIDDEN_KEYS]
    check("no forbidden key anywhere in the body", not key_hits,
          f"hits: {key_hits}")

    import re
    word = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
    value_hits = []
    for path, s in walk_strings(body):
        if path and path[-1] == "<key>":
            continue
        for token in word.findall(s):
            if token.lower() in standard.FORBIDDEN_KEYS:
                value_hits.append(("/".join(path), token))
    print("forbidden tokens found as words inside body strings:")
    for path, token in value_hits:
        print(f"    {'/'.join(path)}: {token!r}")
    check("no forbidden token as a word inside any body string", not value_hits)

    # Exception hygiene.
    check("StandardInvalid is a LoopError and a ValueError",
          issubclass(standard.StandardInvalid, types.LoopError)
          and issubclass(standard.StandardInvalid, ValueError))
    try:
        standard.build_standard(params={"x": 1})
    except standard.StandardInvalid as exc:
        check("raised code is in types.FAILURE_CODES",
              exc.code in types.FAILURE_CODES, f"{exc.code}")
        check("str(exc) renders CODE: detail", str(exc).startswith(f"{exc.code}: "),
              repr(str(exc)[:60]))

    # 'G3 — operative target (R10)' — design s2 line 132. Where is R10?
    rubric = standard.RUBRIC_V1["relation"].body
    r6 = [line for line in rubric.split("\n") if line.startswith("R6.")][0]
    r10 = [line for line in rubric.split("\n") if line.startswith("R10.")][0]
    print("R6:", r6.strip()[:110])
    print("R10:", r10.strip()[:110])
    check("operative-target rule is R6, not R10",
          "operative target" in rubric and "R6." in rubric
          and rubric.index("R6.") < rubric.index("operative target") < rubric.index("R7."))
    check("R10 is the ensemble-disagreement rule (not operative target) - design label mismatch",
          "R10." in rubric and "judge seats" in rubric)

    # CEILING_CLAIM_TEMPLATE placeholders deliberately unfilled (deviation 3 / O5).
    template = standard.CEILING_CLAIM_TEMPLATE
    check("claim template keeps its four placeholders",
          all(mark in template for mark in ("(digest …)", "relation *r*", "*N*", "*A*")),
          template[:140])


if __name__ == "__main__":
    main()
