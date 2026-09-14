"""Attacks on custody.write_new: second write, existing directory, dangling
symlink, a parent component that is a regular file, and the credential refusal
in several renderings.
"""
import _boot  # noqa: F401
import os
import tempfile
from pathlib import Path

from minireason.loop import custody
from minireason.loop.custody import write_new, CustodyMismatch
from minireason.loop.types import LoopError


def attempt(label, path, value):
    try:
        write_new(path, value)
    except LoopError as exc:
        print(f"{label:<46} LoopError {exc.code} detail={exc.detail!r}")
    except Exception as exc:  # noqa: BLE001
        print(f"{label:<46} ESCAPED   {type(exc).__name__}: {exc}")
    else:
        print(f"{label:<46} WROTE     {Path(path).read_bytes()!r}")


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()

    attempt("fresh json value", root / "a.json", {"b": 1, "a": "x"})
    attempt("second write, same path", root / "a.json", {"b": 2})
    attempt("bytes verbatim", root / "b.bin", b"\x00\x01raw")
    attempt("str is a JSON string", root / "c.json", "hello")
    attempt("deep parent created", root / "x" / "y" / "z.json", [1, 2])

    (root / "adir").mkdir()
    attempt("path is an existing directory", root / "adir", {"k": 1})

    os.symlink(root / "nowhere", root / "dangling")
    attempt("path is a dangling symlink", root / "dangling", {"k": 1})
    print("dangling still a symlink, unfollowed:", (root / "dangling").is_symlink(),
          "target created:", (root / "nowhere").exists())

    (root / "plain.txt").write_bytes(b"z")
    attempt("parent component is a regular file", root / "plain.txt" / "k.json", {"k": 1})

    # credential refusal
    os.environ["DEEPSEEK_API_KEY"] = "sk-abcdefghijklmnop"
    try:
        print("credential_names_in(raw)   :",
              custody.credential_names_in(b'{"k": "sk-abcdefghijklmnop"}'))
        attempt("record carrying the credential", root / "leak.json",
                {"authorization": "Bearer sk-abcdefghijklmnop"})
        print("leak.json exists after refusal:", (root / "leak.json").exists())
        attempt("credential in a deep parent path", root / "p" / "q" / "leak.json",
                {"k": "sk-abcdefghijklmnop"})
        print("parent dir created after refusal:", (root / "p").exists())
        os.environ["DEEPSEEK_API_KEY"] = "shortkey"          # exactly 8 -> scanned
        attempt("8-byte credential (at the floor)", root / "eight.json", {"k": "shortkey"})
        os.environ["DEEPSEEK_API_KEY"] = "short7x"           # 7 -> below the floor
        attempt("7-byte credential (below floor)", root / "seven.json", {"k": "short7x"})
        os.environ["DEEPSEEK_API_KEY"] = 'quote"back\\slash'
        attempt("credential needing JSON escaping", root / "esc.json",
                {"k": 'quote"back\\slash'})
        os.environ["DEEPSEEK_API_KEY"] = "café-secret-value"
        attempt("non-ASCII credential, ensure_ascii=False", root / "uni.json",
                {"k": "café-secret-value"})
        import json as _json
        ascii_bytes = _json.dumps({"k": "café-secret-value"}, ensure_ascii=True).encode()
        print("names in ensure_ascii=True bytes:", custody.credential_names_in(ascii_bytes))
        os.environ["DEEPSEEK_API_KEY"] = "sk-utf16-secret"
        attempt("credential written as UTF-16 bytes", root / "u16.bin",
                "sk-utf16-secret".encode("utf-16"))
    finally:
        os.environ.pop("DEEPSEEK_API_KEY", None)
