"""BLOCKER probe: the bracket glob carries an unscanned file past BOTH scans.

The value used here is a synthetic placeholder string invented for this probe.
No real credential is read, written or printed anywhere.

Two scans stand between a byte and the remote:

  1. ``_refuse_credentials`` walks the *named* paths in the working tree;
  2. ``_refuse_credential_text`` reads ``git diff --cached -- <names>``.

Scan 1 walks ``repo/"report[1].md"`` literally and never sees the neighbour the
glob will stage. Scan 2 does see the neighbour -- but git renders a file with a
NUL byte as "Binary files ... differ" and prints none of its content. So the
neighbour reaches the remote unread by either scan.

Run: python3 probe/p02_bracket_defeats_credential_scan.py
"""
from __future__ import annotations

import os

import _lab

SECRET_ENV = "PROBE_FAKE_KEY_ENV"
SECRET_VALUE = "PROBE-FAKE-CREDENTIAL-0123456789"       # synthetic, not a credential
os.environ[SECRET_ENV] = SECRET_VALUE

from minireason import provider_openai_compat as transport      # noqa: E402
from minireason.loop import publish                             # noqa: E402

transport.register_secret_envs([SECRET_ENV])
print("registered secret env NAMES :", transport.registered_secret_envs())

lab = _lab.Lab("bracket-cred")
try:
    lab.write("report[1].md", "the named file, clean\n")
    # The neighbour the glob will stage. A leading NUL makes git call it binary.
    (lab.repo / "report1.md").write_bytes(b"\x00header\n" + SECRET_VALUE.encode() + b"\n")

    scanned = publish._walk_files(lab.repo.resolve(), ("report[1].md",))
    print("scan 1 walked              :", scanned)

    result = publish.publish(lab.repo, ["report[1].md"], "publish the named file",
                             "origin/main", git=_lab.local_git(lab))
    print("publish status             :", result.status)
    print("publish files              :", result.files)

    landed = _lab.git(lab.remote, "show", "refs/heads/main:report1.md").stdout
    print("remote blob is binary      :", b"\x00" in landed)
    print("remote blob carries value  :", SECRET_VALUE.encode() in landed)
    print("remote blob length         :", len(landed))

finally:
    lab.close()

# The same staging step, stopped one line before the commit, so the exact bytes
# scan 2 reads are on the record.
lab = _lab.Lab("bracket-cred-2")
try:
    lab.write("report[1].md", "the named file, clean\n")
    (lab.repo / "report1.md").write_bytes(b"\x00header\n" + SECRET_VALUE.encode() + b"\n")
    git = _lab.local_git(lab)
    git.run("add", "--", "report[1].md")
    staged = git.run("diff", "--cached", "--no-color", "--", "report[1].md")
    text = staged.decode("utf-8", "replace")
    print("--- the whole text scan 2 reads ---")
    print(text)
    print("--- end ---")
    print("scan 2 finds the value      :", SECRET_VALUE in text)
    print("scan 2 hit names            :", publish._redact_with_names(text)[1])
finally:
    lab.close()
