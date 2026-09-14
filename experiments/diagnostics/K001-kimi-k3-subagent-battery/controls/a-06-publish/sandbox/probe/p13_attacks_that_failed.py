"""Attacks on the module that did not succeed, plus two that misfire harmlessly.

Kept in the review because a failed attack is evidence about the module.

Run: python3 probe/p13_attacks_that_failed.py
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

_lab.banner("A. push a '+' refspec or a second ':' through the ref argument")
for ref in ("origin/+main", "origin/main:refs/heads/other", "origin/main --force",
            "origin/refs/heads/../../heads/main", "origin/HEAD"):
    try:
        print(f"  split_publish_ref({ref!r:38}) -> {publish.split_publish_ref(ref)}")
    except publish.PublishError as error:
        print(f"  split_publish_ref({ref!r:38}) -> {error.code}")

_lab.banner("B. a credential in git's own output reaching an exception detail")
outcome = publish.GitOutcome(
    128, b"", ("fatal: unable to access 'https://x:" + SECRET_VALUE
               + "@example.invalid/r.git'\n").encode(), False, ("push", "origin"))
print("  GitOutcome.text()    :", outcome.text().strip())
print("  GitOutcome.summary() :", outcome.summary())
print("  value present?       :", SECRET_VALUE in outcome.summary())
try:
    raise publish.GitCommandFailed(outcome.summary())
except publish.GitCommandFailed as error:
    print("  exception detail     :", error.detail)
    print("  value present?       :", SECRET_VALUE in str(error))

_lab.banner("C. make verify_published true against a remote that moved")
lab = _lab.Lab("moved")
try:
    lab.write("docs/note.md", "published bytes\n")
    result = publish.publish(lab.repo, ["docs/note.md"], "publish", "origin/main",
                             git=_lab.local_git(lab))
    commit = result.remote_commit
    git = _lab.local_git(lab)
    print("  verify (on the ref)            :",
          publish.verify_published(lab.repo, ["docs/note.md"], commit, "origin/main", git=git))
    # The remote moves on to a commit with a different tree.
    lab.write("docs/note.md", "someone else's bytes\n")
    _lab.git(lab.repo, "add", "--", "docs/note.md")
    _lab.git(lab.repo, "commit", "-m", "later work")
    _lab.git(lab.repo, "push", "origin", "main")
    print("  verify (remote moved on)       :",
          publish.verify_published(lab.repo, ["docs/note.md"], commit, "origin/main", git=git))
    # And with the ref deleted entirely.
    _lab.git(lab.remote, "update-ref", "-d", "refs/heads/main")
    print("  verify (ref deleted)           :",
          publish.verify_published(lab.repo, ["docs/note.md"], commit, "origin/main", git=git))
    print("  check_published (ref deleted)  :",
          publish.check_published(lab.repo, "docs/note.md", "origin/main", git=git))
finally:
    lab.close()

_lab.banner("D. get publish() itself to emit a forcing argv")
recorded = []


class Recording(publish.LocalGit):
    def _invoke(self, tokens):
        recorded.append(tuple(tokens))
        return super()._invoke(tokens)


lab = _lab.Lab("nonforcing")
try:
    lab.write("docs/note.md", "x\n")
    publish.publish(lab.repo, ["docs/note.md"], "publish", "origin/main",
                    git=Recording(lab.repo, env=dict(_lab.GIT_ENV)))
    forcing = [t for t in recorded
               if any(token in publish.REWRITING_FLAGS or token.startswith("+")
                      for token in t)]
    print("  argvs emitted                  :", len(recorded))
    print("  any forcing token              :", forcing)
    print("  push argv                      :",
          [t for t in recorded if t and t[0] == "push"])
finally:
    lab.close()

_lab.banner("E. two harmless misfires of the exact-token deny-list")
lab = _lab.Lab("misfire")
try:
    lab.write("--force", "a file whose name is a flag\n")
    try:
        publish.publish(lab.repo, ["--force"], "publish", "origin/main",
                        git=_lab.local_git(lab))
    except publish.PublishError as error:
        print("  publish(['--force'])           :", error.code)
    lab.write("docs/note.md", "x\n")
    try:
        publish.publish(lab.repo, ["docs/note.md"], "--amend", "origin/main",
                        git=_lab.local_git(lab))
    except publish.PublishError as error:
        print("  publish(message='--amend')     :", error.code, "|", error.detail)
finally:
    lab.close()
