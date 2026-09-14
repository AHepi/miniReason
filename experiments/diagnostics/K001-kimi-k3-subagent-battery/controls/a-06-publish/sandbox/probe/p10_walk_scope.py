"""What _walk_files reads, and what git would actually stage.

``_walk_files`` drops a path only when its FIRST component is ``.git``. Below
the top level the exclusion does not apply, so a nested repository's own
``.git/config`` -- which git will never stage and which is exactly where a
credentialed remote URL lives -- is read into the scan.

Run: python3 probe/p10_walk_scope.py
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

_lab.banner("A. a nested .git below the top level is walked")
lab = _lab.Lab("nested-git")
try:
    lab.write("sub/note.md", "the document being published\n")
    lab.write("sub/.git/config", "[remote \"origin\"]\n\turl = https://x:"
              + SECRET_VALUE + "@example.invalid/r.git\n")
    print("_walk_files(['sub'])        :", publish._walk_files(lab.repo.resolve(), ("sub",)))
    print("git add --dry-run -- sub    :",
          _lab.git(lab.repo, "add", "--dry-run", "--", "sub").stdout.decode().split())
    try:
        publish.publish(lab.repo, ["sub"], "publish the note", "origin/main",
                        git=_lab.local_git(lab))
    except publish.PublishError as error:
        print("publish(['sub'])            :", error.code, "|", error.detail)
    else:
        print("publish(['sub'])            : PUBLISHED")
finally:
    lab.close()

_lab.banner("B. the top-level .git is accepted as a path and skipped by the scan")
lab = _lab.Lab("dot-git")
try:
    print("_explicit_paths(['.git/config']) :",
          publish._explicit_paths(lab.repo.resolve(), [".git/config"]))
    print("_walk_files(['.git/config'])     :",
          publish._walk_files(lab.repo.resolve(), (".git/config",)))
    try:
        publish.publish(lab.repo, [".git/config"], "publish git config", "origin/main",
                        git=_lab.local_git(lab))
    except publish.PublishError as error:
        print("publish(['.git/config'])         :", error.code, "|", error.detail[:90])
    else:
        print("publish(['.git/config'])         : PUBLISHED")
finally:
    lab.close()
