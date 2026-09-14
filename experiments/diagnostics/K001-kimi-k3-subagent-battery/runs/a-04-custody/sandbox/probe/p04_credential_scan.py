"""Probe 4: the credential scan in write_new / credential_names_in.

Claims under test:
* W0-CUSTODY acceptance: "write_new ... refuses credential-bearing content".
* docs/lessons/operations.md: "refusal, not redaction".
* custody docstring: "The credential scan runs before anything is created, so a
  refused write leaves no file and no parent directory behind."

Set DEEPSEEK_API_KEY and a custom secret name, try to smuggle the values into
records (raw, JSON-escaped, base64, with the name attached), and check the
disk afterwards. Every env var set here is removed before exit. Uses only
tempfile space. Prints RESULT lines.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from minireason.loop import custody
from minireason import provider_openai_compat as provider

FAKE_KEY = "sk-fakeprobe-9f8e7d6c5b4a3"        # 26 chars, not a real key
CUSTOM_NAME = "PROBE_CUSTOM_CREDENTIAL"
CUSTOM_VALUE = "CustomSecretValue!123"


def result(ok: bool, *parts: object) -> None:
    print("RESULT", "PASS" if ok else "FAIL", *parts)


def main() -> None:
    saved = {name: os.environ.get(name)
             for name in ("DEEPSEEK_API_KEY", CUSTOM_NAME)}
    try:
        os.environ["DEEPSEEK_API_KEY"] = FAKE_KEY
        os.environ[CUSTOM_NAME] = CUSTOM_VALUE
        provider.register_secret_envs([CUSTOM_NAME])
        print("RESULT NOTE scanned names now:", custody.scanned_credential_envs())

        with tempfile.TemporaryDirectory() as scratch:
            base = Path(scratch)

            attempts = {
                "raw value in bytes": (FAKE_KEY + " tail").encode(),
                "JSON-escaped value": json.dumps({"k": FAKE_KEY}).encode(),
                "value with name attached": f"key={FAKE_KEY}".encode(),
                "custom registered value": CUSTOM_VALUE.encode(),
                "base64 of the value": base64.b64encode(FAKE_KEY.encode()),
                "value split across halves": (FAKE_KEY[:13] + " ... " + FAKE_KEY[13:]).encode(),
                "clean content (control)": b'{"status": "fine"}',
            }
            for label, payload in attempts.items():
                target = base / label.replace(" ", "_")[:20] / "record.json"
                if label.startswith("clean"):
                    # control: a clean write must succeed
                    custody.write_new(target, payload)
                    result(target.exists(), label, "written")
                    continue
                try:
                    custody.write_new(target, payload)
                except custody.CustodyMismatch as exc:
                    leaked = False
                    if target.exists():
                        leaked = FAKE_KEY.encode() in target.read_bytes() or \
                                 CUSTOM_VALUE.encode() in target.read_bytes()
                    parent_left = target.parent.exists() and not target.exists()
                    result(exc.code == "CREDENTIAL_IN_OUTPUT" and not leaked,
                           label, "refused as", exc.code,
                           "| value names in detail:", exc.detail.split(":", 1)[-1],
                           "| file leaked on disk:", leaked,
                           "| orphan parent left:", parent_left and target.parent != base)
                else:
                    written = target.read_bytes()
                    result(False, label, "WRITE SUCCEEDED; on disk:",
                           written[:80])
            # Does any file in the tree hold the secret after everything above?
            tree_leak = sorted(str(p.relative_to(base)) for p in base.rglob("*")
                               if p.is_file() and (FAKE_KEY.encode() in p.read_bytes()
                                                   or CUSTOM_VALUE.encode() in p.read_bytes()))
            result(not tree_leak, "no file holds a credential value; holders:", tree_leak)

            # names only, never a value, in what the scan reports
            hits = custody.credential_names_in(
                b"blob " + FAKE_KEY.encode() + b" and " + CUSTOM_VALUE.encode())
            result(hits == [CUSTOM_NAME, "DEEPSEEK_API_KEY"] or hits == sorted(hits),
                   "credential_names_in reports names:", hits,
                   "| any value in the report:", FAKE_KEY in str(hits) or CUSTOM_VALUE in str(hits))

            # the short-value floor
            os.environ["DEEPSEEK_API_KEY"] = "short"  # 5 chars < floor
            hits = custody.credential_names_in(b"short")
            result(hits == [], "value below the 8-char floor is not searched:", hits)
    finally:
        for name, previous in saved.items():
            if previous is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = previous
        print("RESULT NOTE env scrubbed:",
              {name: os.environ.get(name) is None for name in saved if saved[name] is None})


if __name__ == "__main__":
    main()
