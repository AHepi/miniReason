"""Attacks aimed at the acceptance clause "A one-byte change to any pinned file
is detected and named", plus the decision-7 round-trip claim and two spellings
the module docstring says it mirrors.
"""
import _boot  # noqa: F401
import json
import os
import tempfile
from pathlib import Path

from minireason.loop import custody
from minireason.loop.custody import pins, verify_pins, digest, encoded

with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve()
    repo = base / "repo"
    (repo / "src").mkdir(parents=True)
    f = repo / "src" / "a.py"
    f.write_bytes(b"original bytes\n")
    frozen = {"pins": pins(repo, ["src/a.py"])}

    def state(label):
        print(f"{label:<48}", [(x.code, x.path) for x in verify_pins(frozen, repo)] or "CLEAN")

    state("untouched")

    # 1. flip one byte in the middle
    f.write_bytes(b"original bytEs\n")
    state("one byte flipped")
    f.write_bytes(b"original bytes\n")

    # 2. append one byte
    f.write_bytes(b"original bytes\n\n")
    state("one byte appended")
    f.write_bytes(b"original bytes\n")

    # 3. truncate to empty
    f.write_bytes(b"")
    state("truncated to empty")
    f.write_bytes(b"original bytes\n")

    # 4. CRLF normalisation of the same text
    f.write_bytes(b"original bytes\r\n")
    state("LF -> CRLF (same text)")
    f.write_bytes(b"original bytes\n")

    # 5. same bytes, new inode (rewrite)
    f.unlink()
    f.write_bytes(b"original bytes\n")
    state("same bytes, new inode")

    # 6. replaced by a hard link to identical bytes elsewhere
    other = repo / "src" / "twin.py"
    other.write_bytes(b"original bytes\n")
    f.unlink()
    os.link(other, f)
    state("replaced by a hard link, same bytes")
    f.unlink()
    f.write_bytes(b"original bytes\n")

    # 7. replaced by a symlink to identical bytes inside the repo
    f.unlink()
    os.symlink(other, f)
    state("replaced by a symlink, same bytes")
    other.write_bytes(b"original bytEs\n")
    state("  ... and then that target flipped one byte")
    f.unlink()
    f.write_bytes(b"original bytes\n")

    # 8. mtime rolled back to the pinned moment
    os.utime(f, (0, 0))
    state("mtime rolled back to the epoch")

    # 9. the same file pinned twice under two spellings, one byte changed
    two = {"pins": {"src/a.py": frozen["pins"]["src/a.py"],
                    "./src/a.py": frozen["pins"]["src/a.py"]}}
    f.write_bytes(b"original bytEs\n")
    print(f"{'two spellings of one path, byte flipped':<48}",
          [(x.code, x.path) for x in verify_pins(two, repo)])
    f.write_bytes(b"original bytes\n")

print()
print("--- decision 7: encoded() round-trips to a value the digests agree on ---")
for label, value in [
    ("plain object", {"a": 1, "b": [1, 2, 3]}),
    ("non-ASCII", {"k": "café 日本語"}),
    ("tuple becomes list", {"k": (1, 2)}),
    ("int key becomes string key", {1: "a"}),
    ("bool key", {True: "a"}),
    ("float edge", {"k": [-0.0, 1e400, 1.5]}),
    ("empty containers", {"a": {}, "b": []}),
]:
    try:
        before = digest(value)
        after = digest(json.loads(encoded(value).decode("utf-8")))
    except Exception as exc:  # noqa: BLE001
        print(f"{label:<30} RAISED {type(exc).__name__}: {exc}")
    else:
        print(f"{label:<30} agree={before == after}")

for label, value in [("int and str keys that collide", {1: "a", "1": "b"})]:
    try:
        print(f"{label:<30} digest={digest(value)}")
    except Exception as exc:  # noqa: BLE001
        print(f"{label:<30} RAISED {type(exc).__name__}: {exc} "
              f"(is LoopError: {isinstance(exc, custody.CustodyMismatch)})")

print()
print("--- spellings the module docstring says it mirrors ---")
root = Path(custody.__file__).parents[2]
gi = (root / "minireason" / "graph_import_h005.py").read_text(encoding="utf-8")
for token in ("PATH_ESCAPES_OCCURRENCE", "OutRootRefused"):
    print(f"graph_import_h005 carries {token:<24}", token in gi)
tx = (root / "minireason" / "provider_openai_compat.py").read_text(encoding="utf-8")
print("provider_openai_compat carries CREDENTIAL_IN_OUTPUT ",
      "CREDENTIAL_IN_OUTPUT" in tx)
