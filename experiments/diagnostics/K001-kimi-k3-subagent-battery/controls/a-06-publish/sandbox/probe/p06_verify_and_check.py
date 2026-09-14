"""verify_published / check_published / upstream_ref / split_publish_ref.

Exercises deviation 7's split ("verification compares committed trees, never the
working tree ... check_published keeps the working-tree comparison") and the
ref helpers, against a real bare remote.

Run: python3 probe/p06_verify_and_check.py
"""
from __future__ import annotations

import _lab
from minireason.loop import publish

_lab.banner("A. deviation 7: a later step writing under the same path")
lab = _lab.Lab("verify")
try:
    lab.write("docs/note.md", "published bytes\n")
    result = publish.publish(lab.repo, ["docs/note.md"], "publish", "origin/main",
                             git=_lab.local_git(lab))
    commit = result.remote_commit
    git = _lab.local_git(lab)
    print("verify_published (fresh)          :",
          publish.verify_published(lab.repo, ["docs/note.md"], commit, "origin/main", git=git))
    print("check_published  (fresh)          :",
          publish.check_published(lab.repo, "docs/note.md", "origin/main", git=git))

    lab.write("docs/note.md", "a later step wrote here\n")
    print("verify_published (after a write)  :",
          publish.verify_published(lab.repo, ["docs/note.md"], commit, "origin/main", git=git))
    print("check_published  (after a write)  :",
          publish.check_published(lab.repo, "docs/note.md", "origin/main", git=git))
    print("check_published  (by commit sha)  :",
          publish.check_published(lab.repo, commit, "origin/main", git=git))
    parent = _lab.git(lab.repo, "rev-parse", commit + "^").stdout.decode().strip()
    print("check_published  (ancestor sha)   :",
          publish.check_published(lab.repo, parent, "origin/main", git=git))
    unknown = "0" * 40
    print("check_published  (unknown sha)    :",
          publish.check_published(lab.repo, unknown, "origin/main", git=git))
    try:
        publish.check_published(lab.repo, "no/such/thing", "origin/main", git=git)
    except publish.PublishError as error:
        print("check_published  (neither)        : raised", error.code)
finally:
    lab.close()

_lab.banner("B. the connector case: a distinct remote commit over an equal tree")


class ReauthoringPush(publish.LocalGit):
    """Real push, then the remote re-authors the same tree under a new id."""

    def __init__(self, repo, remote_dir, **kwargs):
        super().__init__(repo, **kwargs)
        self.remote_dir = remote_dir
        self.reauthored = None

    def _invoke(self, tokens):
        outcome = super()._invoke(tokens)
        if tokens and tokens[0] == "push" and outcome.ok and self.reauthored is None:
            head = _lab.git(self.remote_dir, "rev-parse", "refs/heads/main").stdout.decode().strip()
            tree = _lab.git(self.remote_dir, "rev-parse", head + "^{tree}").stdout.decode().strip()
            parent = _lab.git(self.remote_dir, "rev-parse", head + "^").stdout.decode().strip()
            new = _lab.git(self.remote_dir, "commit-tree", tree, "-p", parent,
                           "-m", "re-authored by the connector").stdout.decode().strip()
            _lab.git(self.remote_dir, "update-ref", "refs/heads/main", new, head)
            self.reauthored = new
        return outcome


lab = _lab.Lab("connector")
try:
    lab.write("docs/note.md", "published bytes\n")
    git = ReauthoringPush(lab.repo, lab.remote, env=dict(_lab.GIT_ENV))
    result = publish.publish(lab.repo, ["docs/note.md"], "publish", "origin/main", git=git)
    print("status                    :", result.status)
    print("local_commit              :", result.local_commit)
    print("remote_commit             :", result.remote_commit)
    print("distinct_remote_commit    :", result.distinct_remote_commit)
    print("both ids in the receipt   :",
          result.as_receipt()["local_commit"], "/", result.as_receipt()["published_commit"])
    print("VERIFIED line             :", result.verified_line)
    print("verify_published(local)   :",
          publish.verify_published(lab.repo, ["docs/note.md"], result.local_commit,
                                   "origin/main", git=_lab.local_git(lab)))
finally:
    lab.close()

_lab.banner("C. ref helpers")
for ref in ("origin/main", "origin/feature/x", "origin", "/origin/main", "origin/",
            "origin/a..b", "or igin/main", "origin/-x", ""):
    try:
        print(f"split_publish_ref({ref!r:20}) -> {publish.split_publish_ref(ref)}")
    except publish.PublishError as error:
        print(f"split_publish_ref({ref!r:20}) -> {error.code}")

lab = _lab.Lab("upstream")
try:
    git = _lab.local_git(lab)
    print("upstream_ref (set)        :", publish.upstream_ref(lab.repo, git=git))
    _lab.git(lab.repo, "branch", "--unset-upstream")
    try:
        publish.upstream_ref(lab.repo, git=git)
    except publish.PublishError as error:
        print("upstream_ref (unset)      :", error.code)
finally:
    lab.close()
