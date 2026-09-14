"""The path discipline and the argument checks, one case per line.

Includes three behaviours worth naming in the review:
  * a deletion cannot be published at all (``_explicit_paths`` requires
    ``exists()``);
  * a symlink is silently replaced by its target's repo-relative name;
  * an ignored, never-published file under a named directory refuses the whole
    publish (the working-tree scan reads it).

Run: python3 probe/p09_path_and_argument_refusals.py
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


def show(label, fn):
    try:
        value = fn()
    except publish.PublishError as error:
        print(f"{label:<46} -> {error.code}  ({error.detail[:48]})")
    except Exception as error:                                   # noqa: BLE001
        print(f"{label:<46} -> {type(error).__name__}: {error}")
    else:
        print(f"{label:<46} -> {value}")


_lab.banner("A. _explicit_paths")
lab = _lab.Lab("paths")
try:
    lab.write("docs/note.md", "x\n")
    lab.write("docs/sub/deep.md", "y\n")
    repo = lab.repo.resolve()
    for label, arg in (
        ("['docs/note.md']", ["docs/note.md"]),
        ("['docs']", ["docs"]),
        ("[absolute path]", [str(repo / "docs/note.md")]),
        ("['.']", ["."]),
        ("['docs/..']", ["docs/.."]),
        ("['']", [""]),
        ("[] (empty iterable)", []),
        ("['-A']", ["-A"]),
        ("[':(glob)docs/*']", [":(glob)docs/*"]),
        ("['docs/*']", ["docs/*"]),
        ("['docs/?ote.md']", ["docs/?ote.md"]),
        ("['docs/[n]ote.md']", ["docs/[n]ote.md"]),
        ("['../outside']", ["../outside"]),
        ("['docs/absent.md']", ["docs/absent.md"]),
        ("['.git']", [".git"]),
        ("['.git/config']", [".git/config"]),
        ("duplicate names", ["docs/note.md", "./docs/note.md"]),
    ):
        show(f"_explicit_paths({label})", lambda a=arg: publish._explicit_paths(repo, a))

    os.symlink(repo / "docs/note.md", repo / "link.md")
    show("_explicit_paths(['link.md'])  (a symlink)",
         lambda: publish._explicit_paths(repo, ["link.md"]))
    os.symlink("/etc/hostname", repo / "outward.md")
    show("_explicit_paths(['outward.md']) (escaping)",
         lambda: publish._explicit_paths(repo, ["outward.md"]))
finally:
    lab.close()

_lab.banner("B. publish() argument checks")
lab = _lab.Lab("args")
try:
    lab.write("docs/note.md", "x\n")
    git = _lab.local_git(lab)
    for label, kwargs in (("attempt=0", {"attempt": 0}), ("attempt=-1", {"attempt": -1}),
                          ("attempt=True", {"attempt": True}), ("attempt='1'", {"attempt": "1"}),
                          ("attempt=4", {"attempt": 4})):
        show(f"publish(..., {label})",
             lambda k=kwargs: publish.publish(lab.repo, ["docs/note.md"], "m",
                                              "origin/main", git=git, **k).status)
    show("publish(..., message='   ')",
         lambda: publish.publish(lab.repo, ["docs/note.md"], "   ", "origin/main",
                                 git=git).status)
finally:
    lab.close()

_lab.banner("C. a deletion cannot be published")
lab = _lab.Lab("deletion")
try:
    lab.write("docs/note.md", "x\n")
    publish.publish(lab.repo, ["docs/note.md"], "publish", "origin/main",
                    git=_lab.local_git(lab))
    (lab.repo / "docs/note.md").unlink()
    show("publish(['docs/note.md']) after unlink",
         lambda: publish.publish(lab.repo, ["docs/note.md"], "remove it", "origin/main",
                                 git=_lab.local_git(lab)).status)
    print("still tracked in the index               :", lab.tracked())
finally:
    lab.close()

_lab.banner("D. an already-staged file outside the named paths")
lab = _lab.Lab("stray")
try:
    lab.write("docs/note.md", "x\n")
    lab.write("other/thing.md", "y\n")
    _lab.git(lab.repo, "add", "--", "other/thing.md")
    show("publish(['docs/note.md']) with other/ staged",
         lambda: publish.publish(lab.repo, ["docs/note.md"], "publish", "origin/main",
                                 git=_lab.local_git(lab)).status)
finally:
    lab.close()

_lab.banner("E. an ignored file under a named directory")
lab = _lab.Lab("ignored")
try:
    lab.write("docs/note.md", "x\n")
    lab.write("docs/.gitignore", "local.env\n")
    lab.write("docs/local.env", SECRET_VALUE + "\n")     # never staged, never published
    show("publish(['docs'])",
         lambda: publish.publish(lab.repo, ["docs"], "publish", "origin/main",
                                 git=_lab.local_git(lab)).status)
    print("what git would have staged              :",
          _lab.git(lab.repo, "add", "--dry-run", "--", "docs").stdout.decode().split())
finally:
    lab.close()
