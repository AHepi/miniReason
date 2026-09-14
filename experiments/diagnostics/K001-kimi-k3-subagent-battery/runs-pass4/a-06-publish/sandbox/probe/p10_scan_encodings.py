"""Probe 10: is the credential scan byte-complete on non-UTF-8 files?

_refuse_credentials decodes with 'utf-8', errors='replace'. A credential whose
bytes are pure ASCII is unaffected by the codec; but a file that is not valid
UTF-8 and embeds the ASCII credential keeps the credential bytes intact under
'replace' decoding (only the invalid sequences are replaced). Test whether a
credential split by an invalid UTF-8 byte, or in a UTF-16 file, is detected.

Claim under test: 'scan the bytes for any credential this process can see'
and 'The detail carries the environment variable NAMES only, never a value'.
"""

import os

from fixture import Fixture, pub, with_secret


def attempt(write, label):
    fix = Fixture()
    secret = "sk-abcdef01-23456789"
    with_secret("PROBE_CRED", secret)
    try:
        run = fix.local / "run"
        run.mkdir(exist_ok=True)
        (run / "blob.bin").write_bytes(write(secret))
        fix.sh("-C", str(fix.local), "add", "run/blob.bin")
        fix.sh("-C", str(fix.local), "commit", "-m", label)
        try:
            pub.publish(fix.local, ["run"], label, sleep=lambda s: None)
            print(label, "-> PUBLISHED (scan did not see it)")
        except pub.CredentialInStagedDiff as exc:
            print(label, "-> refused", exc.code, "| detail:", exc.detail)
            print("   secret in detail:", secret in exc.detail)
    finally:
        os.environ.pop("PROBE_CRED", None)
        fix.cleanup()


def main():
    # credential intact inside an otherwise-invalid-utf8 file
    attempt(lambda s: b"\xff\xfe head " + s.encode() + b" tail \x80\x81", "invalid-utf8 wrapper")
    # credential split across an invalid byte: 'abc' + 0xff + 'def...'
    attempt(lambda s: s[:6].encode() + b"\xff" + s[6:].encode(), "split by invalid byte")
    # credential encoded UTF-16 (bytes interleaved with NUL)
    attempt(lambda s: s.encode("utf-16-le"), "utf-16-le encoding")
    # credential rot13'd -- a transformed rendering the scanner cannot know
    attempt(lambda s: s.translate(str.maketrans(
        "abcdefghijklmnopqrstuvwxyz", "nopqrstuvwxyzabcdefghijklm")).encode(),
        "rot13 rendering")


if __name__ == "__main__":
    main()
