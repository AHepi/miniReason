"""Can a transport that dies mid-push be read as a divergence?

"failed to push some refs" is one of ``_REJECTION_MARKERS``. Git prints it for
a rejection, but it also prints it when the remote end goes away after the
connection is up. If that reaches ``_classify_push_failure`` as PUSH_REJECTED,
``_push`` returns without a single backoff retry and the driver is told to
re-fetch and merge a divergence that does not exist.

Drives the ``ext::`` transport, whose helper is a command that dies, so the
failure happens after git has started talking to a "remote".

Run: python3 probe/p12_transport_dies_midpush.py
"""
from __future__ import annotations

import os
import stat

import _lab
from minireason.loop import publish

HELPERS = {
    "helper exits 1 immediately": "#!/bin/sh\nexit 1\n",
    "helper prints garbage then dies": "#!/bin/sh\nprintf 'noise\\n'\nexit 2\n",
    "helper closes stdout after the ref advertisement": (
        "#!/bin/sh\nprintf '0000'\nexit 0\n"),
}

for label, body in HELPERS.items():
    lab = _lab.Lab("ext")
    try:
        helper = lab.dir / "helper.sh"
        helper.write_text(body)
        helper.chmod(helper.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        _lab.git(lab.repo, "remote", "set-url", "origin", f"ext::{helper} %S")
        lab.write("docs/note.md", "x\n")
        _lab.git(lab.repo, "add", "--", "docs/note.md")
        _lab.git(lab.repo, "commit", "-m", "x")
        outcome = _lab.local_git(lab, timeout=30.0).status(
            "push", "--porcelain", "--set-upstream", "origin", "HEAD:refs/heads/main")
        blob = outcome.text().lower()
        matched = [m for m in publish._REJECTION_MARKERS if m in blob]
        print(f"--- {label} ---")
        for line in outcome.text().strip().splitlines():
            print("   ", line)
        print("    markers matched :", matched)
        print("    classified as   :", publish._classify_push_failure(outcome))
        print()
    finally:
        lab.close()

# The ext:: transport is refused by git's own protocol allow-list, so the same
# question is asked again with a receive-pack that is killed mid-conversation.
HOOKS = {
    "receive-pack killed mid-push": "#!/bin/sh\nkill -9 $PPID\n",
    "pre-receive hook exits non-zero": "#!/bin/sh\necho 'policy says no' >&2\nexit 1\n",
}

for label, body in HOOKS.items():
    lab = _lab.Lab("hook")
    try:
        hooks = lab.remote / "hooks"
        hooks.mkdir(exist_ok=True)
        hook = hooks / "pre-receive"
        hook.write_text(body)
        hook.chmod(hook.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        lab.write("docs/note.md", "x\n")
        _lab.git(lab.repo, "add", "--", "docs/note.md")
        _lab.git(lab.repo, "commit", "-m", "x")
        outcome = _lab.local_git(lab, timeout=30.0).status(
            "push", "--porcelain", "--set-upstream", "origin", "HEAD:refs/heads/main")
        blob = outcome.text().lower()
        matched = [m for m in publish._REJECTION_MARKERS if m in blob]
        print(f"--- {label} ---")
        for line in outcome.text().strip().splitlines():
            print("   ", line)
        print("    markers matched :", matched)
        print("    classified as   :", publish._classify_push_failure(outcome))
        print("    remote ref moved:",
              lab.remote_main() == _lab.git(lab.repo, "rev-parse", "HEAD"
                                            ).stdout.decode().strip())
        print()
    finally:
        lab.close()
