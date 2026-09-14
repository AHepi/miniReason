"""Is the stop vocabulary closed against the one token it must never carry?

types.py: "the stop vocabulary carries no token that would say otherwise".
STOP_REASONS itself is clean (probe 04). is_stop_reason is the predicate the
rest of the package will use, and it has one parameterised tail.
"""
from _fixture import config  # noqa: E402

from minireason.loop import types  # noqa: E402

print("--- the seven declared members")
for token in sorted(types.STOP_REASONS):
    print(f"  {token!r:32} is_stop_reason -> {types.is_stop_reason(token)}")

print()
print("--- the parameterised tail")
for token in ("preregistered_condition:obligation-o3",
              "preregistered_condition:exhaustion",
              "preregistered_condition:inquiry_exhausted",
              "preregistered_condition:nothing_left_to_say",
              "preregistered_condition:",
              "preregistered_condition:../x",
              "exhaustion",
              "resource_boundary "):
    print(f"  {token!r:44} -> {types.is_stop_reason(token)}")

print()
print("--- the same token through block_code, for contrast")
try:
    types.block_code("exhaustion")
except types.LoopError as exc:
    print("  block_code('exhaustion') ->", exc.code)

print()
print("--- and there is no is_block_reason/assert helper that would scan it")
print("  names exported by types:", [n for n in types.__all__ if n.startswith("is_")])
