"""Deviation 3's "refused with the index still clean" is not always true.

The working-tree scan runs before ``git add``; the staged-diff scan runs after
it. Two reachable inputs make the *second* scan the one that fires, so the
refusal lands with the caller's paths staged in a repository this module may
not ``reset``:

  A. a commit that REMOVES a credential already in HEAD -- the deletion line
     ``-<value>`` is in the staged diff, and nowhere in the working tree;
  B. a file whose NAME carries the value -- the ``diff --git a/<name>`` header
     is in the staged diff, and no file's content carries it.

The value used here is a synthetic placeholder invented for this probe.

Run: python3 probe/p05_refusal_leaves_index_dirty.py
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


def attempt(label, build, paths):
    lab = _lab.Lab(label)
    try:
        build(lab)
        print(f"--- {label} ---")
        print("staged before publish() :", lab.staged())
        try:
            publish.publish(lab.repo, paths, "publish", "origin/main",
                            git=_lab.local_git(lab))
        except publish.CredentialInStagedDiff as refused:
            print("refused with            :", refused.code, "|", refused.detail)
        except publish.PublishError as other:
            print("refused with            :", other.code, "|", other.detail)
        else:
            print("NOT refused")
        print("staged after refusal    :", lab.staged())
        print("index still clean?      :", lab.staged() == [])
        print()
    finally:
        lab.close()


def build_removal(lab):
    lab.write("docs/leak.md", "header\n" + SECRET_VALUE + "\ntail\n")
    _lab.git(lab.repo, "add", "--", "docs/leak.md")
    _lab.git(lab.repo, "commit", "-m", "an earlier commit that carried it")
    lab.write("docs/leak.md", "header\nREMOVED\ntail\n")


def build_named(lab):
    lab.write(f"docs/{SECRET_VALUE}.md", "entirely innocuous content\n")


attempt("removal", build_removal, ["docs/leak.md"])
attempt("named", build_named, [f"docs/{SECRET_VALUE}.md"])

# For contrast: the case deviation 3 is written about really is refused clean.
def build_planted(lab):
    lab.write("docs/planted.md", "header\n" + SECRET_VALUE + "\n")


attempt("planted-in-working-tree", build_planted, ["docs/planted.md"])
