"""The credential guard: what scanned_credential_envs() derives, and what it
does when the transport it derives from misbehaves.
"""
import _boot  # noqa: F401
import os
import tempfile
from pathlib import Path

from minireason.loop import custody
from minireason import provider_openai_compat as tx

SECRET = "or-v1-0123456789abcdef"

print("default scanned names   :", custody.scanned_credential_envs())
tx.register_secret_envs(["OPENROUTER_API_KEY"])
print("after register_secret_envs:", custody.scanned_credential_envs())

os.environ["OPENROUTER_API_KEY"] = SECRET
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()

    print("names in a bearing record:",
          custody.credential_names_in(custody.encoded({"h": SECRET})))
    try:
        custody.write_new(root / "one.json", {"h": SECRET})
    except custody.CustodyMismatch as exc:
        print("write_new (healthy transport):", exc.code, exc.detail)
    else:
        print("write_new (healthy transport): WROTE", (root / "one.json").read_bytes())

    # now make the transport's own helper fail, exactly as the two
    # `except Exception: pass` arms in custody anticipate
    real_names = tx._secret_env_names
    real_items = tx._secret_items

    def boom(*a, **k):
        raise RuntimeError("registry unavailable")

    tx._secret_env_names = boom
    tx._secret_items = boom
    try:
        print("scanned names, broken tx:", custody.scanned_credential_envs())
        print("names in bearing record :",
              custody.credential_names_in(custody.encoded({"h": SECRET})))
        try:
            custody.write_new(root / "two.json", {"h": SECRET})
        except custody.CustodyMismatch as exc:
            print("write_new (broken transport):", exc.code, exc.detail)
        else:
            print("write_new (broken transport): WROTE",
                  (root / "two.json").read_bytes())
    finally:
        tx._secret_env_names = real_names
        tx._secret_items = real_items
        os.environ.pop("OPENROUTER_API_KEY", None)
        tx._reset_registered_secret_envs()

print("names never carry a value:",
      all("-" not in n or n.isupper() for n in custody.scanned_credential_envs()),
      custody.scanned_credential_envs())

# The other arm custody documents: the transport is not importable at all.
print()
print("--- transport not importable (custody's documented 'optional' path) ---")
import sys
tx.register_secret_envs(["OPENROUTER_API_KEY"])
os.environ["OPENROUTER_API_KEY"] = SECRET
import minireason
saved = sys.modules.pop("minireason.provider_openai_compat")
sys.modules["minireason.provider_openai_compat"] = None      # makes the import raise
delattr(minireason, "provider_openai_compat")
try:
    print("_provider_module()      :", custody._provider_module())
    print("scanned names           :", custody.scanned_credential_envs())
    print("names in bearing record :",
          custody.credential_names_in(custody.encoded({"h": SECRET})))
    with tempfile.TemporaryDirectory() as tmp2:
        p = Path(tmp2) / "three.json"
        try:
            custody.write_new(p, {"h": SECRET})
        except custody.CustodyMismatch as exc:
            print("write_new               :", exc.code, exc.detail)
        else:
            print("write_new               : WROTE", p.read_bytes())
finally:
    sys.modules["minireason.provider_openai_compat"] = saved
    os.environ.pop("OPENROUTER_API_KEY", None)
    tx._reset_registered_secret_envs()
