"""Probe: does the wave-0 oracle's integer-in-body test pass against the
bytes in this sandbox?

The module docstring of standard.py promises: "every integer in the built
body lies under ``guard_parameters`` or under ``role_contracts.word_limits``".
The oracle docs/examples/test_standard_example.py asserts every integer lies
under ``guard_parameters.`` only. Run the assertion directly against
STANDARD_BODY and print the result.
"""
import sys, pathlib

root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "src"))

from minireason.loop import standard
from minireason.loop.standard import standard_body, STANDARD_BODY


def walk(value, path=""):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from walk(v, f"{path}.{k}" if path else str(k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, value


body = standard_body(STANDARD_BODY)
integers = [(p, v) for p, v in walk(body)
            if isinstance(v, int) and not isinstance(v, bool)]
print("integers in STANDARD_BODY:")
for p, v in integers:
    oracle_ok = p.startswith("guard_parameters.")
    print(f"   {p} = {v}   oracle path startswith 'guard_parameters.': {oracle_ok}")

bad = [p for p, v in integers if not p.startswith("guard_parameters.")]
print()
print("oracle assertion (every integer under guard_parameters.) would "
      f"{'PASS' if not bad else 'FAIL'} on these paths: {bad}")
print("docstring promise (guard_parameters or role_contracts.word_limits): "
      + str(all(p.startswith(("guard_parameters.", "role_contracts.word_limits."))
                for p, v in integers)))
