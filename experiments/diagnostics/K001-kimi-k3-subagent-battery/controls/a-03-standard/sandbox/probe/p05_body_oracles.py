"""The oracles the module docstring states over the shipped bytes.

* "every integer in the built body lies under ``guard_parameters`` or under
  ``role_contracts.word_limits``, and each one is a declared resource, seat count
  or prose bound";
* "the only occurrence of that token [``exhaust``] in the shipped bytes is the
  ceiling's own denial of it";
* ceiling clause seven's nine block reason codes against ``types.BLOCK_CODES``
  and ``types.CEILING_BLOCK_REASONS``, in both directions.
"""
from __future__ import annotations

import json
import re

import _boot  # noqa: F401

from minireason.loop import standard as S
from minireason.loop import types as T

body = json.loads(S.STANDARD_BODY)


def walk(value, path=()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk(item, path + (str(key),))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield from walk(item, path + ("[%d]" % i,))
    else:
        yield path, value


ints = [(p, v) for p, v in walk(body) if isinstance(v, int) and not isinstance(v, bool)]
print("integers in STANDARD_BODY: %d" % len(ints))
for p, v in ints:
    print("   %-46s = %r" % (".".join(p), v))
outside = [p for p, _ in ints
           if p[0] != "guard_parameters" and p[:2] != ("role_contracts", "word_limits")]
print("integers outside guard_parameters / role_contracts.word_limits:", outside)

print()
text = S.STANDARD_BODY.decode("utf-8")
hits = [m.start() for m in re.finditer("exhaust", text, re.IGNORECASE)]
print("occurrences of the stem 'exhaust' in the shipped bytes:", len(hits))
for h in hits:
    print("   ...%s..." % text[h - 60:h + 30].replace("\\n", " "))

print()
clause = [c for c in S.CEILING_REQUIRED_SENTENCES if "block register" in c.lower()]
print("ceiling block-register clause:")
print("   ", clause[0])
named = re.findall(r"`([a-z-]+)`", clause[0])
print("codes the clause names, in its order:", named)
print("types.CEILING_BLOCK_REASONS         :", list(T.CEILING_BLOCK_REASONS))
print("same object order                   :", tuple(named) == T.CEILING_BLOCK_REASONS)
print("every named reason is a BLOCK_CODE  :",
      sorted(set("blocked:" + n for n in named) - T.BLOCK_CODES) or "yes")
print("BLOCK_CODES not named by the ceiling:",
      sorted(T.BLOCK_CODES - set("blocked:" + n for n in named)))

print()
print("-- the ceiling's stop vocabulary against types.STOP_REASONS --")
print("'resource_boundary' is a stop reason:", "resource_boundary" in T.STOP_REASONS)
print("no stop reason carries the stem     :",
      not any("exhaust" in r for r in T.STOP_REASONS))

print()
print("-- guard scans over the shipped bytes --")
for name, fn in (("assert_no_exhaustion_claim", S.assert_no_exhaustion_claim),
                 ("assert_no_scoring_headers", S.assert_no_scoring_headers)):
    for what, blob in (("STANDARD_BODY", text), ("CEILING_TEXT", S.CEILING_TEXT)):
        try:
            fn(blob, what)
        except S.StandardInvalid as exc:
            print("   %-26s %-14s REFUSED %s" % (name, what, exc.code))
        else:
            print("   %-26s %-14s passes" % (name, what))
