"""The package's documented pairing is write_new(fenced(run_root, relative)).
fenced() returns the fully symlink-RESOLVED path, so by the time write_new sees
it there is no symlink left for its ``target.is_symlink()`` refusal to catch.
This probe writes one step receipt and looks at where it lands.
"""
import _boot  # noqa: F401
import os
import tempfile
from pathlib import Path

from minireason.loop import custody
from minireason.loop.custody import fenced, write_new

with tempfile.TemporaryDirectory() as tmp:
    run_root = Path(tmp).resolve() / "experiments" / "loops" / "RUN-0001"
    (run_root / "steps").mkdir(parents=True)
    (run_root / "cycles" / "0").mkdir(parents=True)

    # a symlink sitting where the next step receipt is going to be written
    os.symlink(run_root / "cycles" / "0" / "decision.json",
               run_root / "steps" / "0001-S0.json")

    named = run_root / "steps" / "0001-S0.json"
    print("named coordinate is a symlink     :", named.is_symlink())

    # (a) write_new on the raw relative path: the refusal the module advertises
    try:
        write_new(named, {"step": "0001-S0"})
    except custody.CustodyMismatch as exc:
        print("write_new(raw path)               :", exc.code)
    else:
        print("write_new(raw path)               : WROTE")

    # (b) the documented pairing
    gate = fenced(run_root, "steps/0001-S0.json")
    print("fenced(run_root, 'steps/0001-S0.json'):", gate)
    try:
        write_new(gate, {"step": "0001-S0"})
    except custody.CustodyMismatch as exc:
        print("write_new(fenced(...))            :", exc.code)
    else:
        print("write_new(fenced(...))            : WROTE")

    print("bytes at the named coordinate     :", named.read_bytes())
    print("bytes at cycles/0/decision.json   :",
          (run_root / "cycles" / "0" / "decision.json").read_bytes())
    print("steps/0001-S0.json is still a symlink, not a file:",
          named.is_symlink(), named.resolve())

    # (c) the coordinate the record actually occupies is now spent
    try:
        write_new(fenced(run_root, "cycles/0/decision.json"), {"decision": "stop"})
    except custody.CustodyMismatch as exc:
        print("write_new(cycles/0/decision.json) :", exc.code, exc.detail)
    else:
        print("write_new(cycles/0/decision.json) : WROTE")
