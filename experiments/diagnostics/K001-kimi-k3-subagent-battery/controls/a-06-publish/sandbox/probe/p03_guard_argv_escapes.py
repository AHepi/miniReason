"""BLOCKER probe: _refuse_history_rewrite is an exact-token deny-list.

``REWRITING_FLAGS`` is tested with ``token in REWRITING_FLAGS`` -- exact string
equality. Git's own option parser accepts an ``=``-valued spelling and an
unambiguous abbreviation of the same option, neither of which is that exact
string. So the argv guard admits:

  * ``push --force-with-lease=<ref>:<sha>``  -- a force push;
  * ``commit --amen``                        -- ``--amend`` abbreviated;
  * ``add -A`` / ``commit -a``               -- the stage-everything spellings
    the module docstring's "Never:" list names first.

Every case below is *executed* against a real bare remote and the remote ref is
read back afterwards.

Run: python3 probe/p03_guard_argv_escapes.py
"""
from __future__ import annotations

import _lab
from minireason.loop import publish

_lab.banner("A. push --force-with-lease=<ref>:<sha> is admitted and rewrites the ref")
lab = _lab.Lab("force-lease")
try:
    lab.write("a.md", "first\n")
    _lab.git(lab.repo, "add", "--", "a.md")
    _lab.git(lab.repo, "commit", "-m", "A")
    _lab.git(lab.repo, "push", "origin", "main")
    seed = _lab.git(lab.repo, "rev-parse", "HEAD~1").stdout.decode().strip()
    published = lab.remote_main()
    print("remote main after honest push :", published)

    # Diverge: throw the published commit away locally and author a rival.
    _lab.git(lab.repo, "reset", "--hard", seed)
    lab.write("a.md", "rival\n")
    _lab.git(lab.repo, "add", "--", "a.md")
    _lab.git(lab.repo, "commit", "-m", "B (rival, not a descendant of A)")
    rival = lab.head()
    print("local rival commit            :", rival)
    print("rival descends from published :",
          _lab.git(lab.repo, "merge-base", "--is-ancestor", published, rival,
                   check=False).returncode == 0)

    git = _lab.local_git(lab)

    honest = git.status("push", "--porcelain", "origin", "HEAD:refs/heads/main")
    print("honest push ok                :", honest.ok, "| classify:",
          publish._classify_push_failure(honest))

    try:
        forced = git.status("push", "--force-with-lease=refs/heads/main:" + published,
                            "origin", "HEAD:refs/heads/main")
    except publish.HistoryRewriteRefused as refused:
        print("GUARD FIRED                   :", refused.code, refused.detail)
    else:
        print("GUARD DID NOT FIRE            : exit", forced.code)
        print("push output                   :", forced.text().strip())
    after = lab.remote_main()
    print("remote main afterwards        :", after)
    print("remote ref now the rival      :", after == rival)
    print("published commit still on ref :", after == published)
finally:
    lab.close()

_lab.banner("B. commit --amen (unambiguous abbreviation of --amend) is admitted")
lab = _lab.Lab("amend-abbrev")
try:
    before = lab.head()
    lab.write("b.md", "one\n")
    git = _lab.local_git(lab)
    git.run("add", "--", "b.md")
    try:
        out = git.status("commit", "--amen", "-m", "rewritten seed")
    except publish.HistoryRewriteRefused as refused:
        print("GUARD FIRED                   :", refused.code, refused.detail)
    else:
        print("GUARD DID NOT FIRE            : exit", out.code)
        print("HEAD before                   :", before)
        print("HEAD after                    :", lab.head())
        print("seed commit rewritten         :", before != lab.head())
        print("b.md folded into the amended commit :",
              "b.md" in _lab.git(lab.repo, "ls-tree", "-r", "--name-only", "HEAD"
                                 ).stdout.decode().split())
finally:
    lab.close()

_lab.banner("C. add -A and commit -a are admitted")
lab = _lab.Lab("add-all")
try:
    lab.write("wanted.md", "wanted\n")
    lab.write("private/notes.md", "never named by any caller\n")
    git = _lab.local_git(lab)
    try:
        git.run("add", "-A")
    except publish.HistoryRewriteRefused as refused:
        print("GUARD FIRED on add -A         :", refused.code, refused.detail)
    else:
        print("GUARD DID NOT FIRE on add -A  : staged", lab.staged())

    lab.write("wanted.md", "wanted, edited\n")
    _lab.git(lab.repo, "commit", "-m", "everything")
    lab.write("wanted.md", "edited again\n")
    lab.write("private/notes.md", "edited too\n")
    try:
        git.run("commit", "-a", "-m", "stage every tracked file")
    except publish.HistoryRewriteRefused as refused:
        print("GUARD FIRED on commit -a      :", refused.code, refused.detail)
    else:
        committed = _lab.git(lab.repo, "show", "--name-only", "--format=", "HEAD"
                             ).stdout.decode().split()
        print("GUARD DID NOT FIRE, committed :", committed)
finally:
    lab.close()

_lab.banner("D. for contrast: the spellings the guard does catch")
lab = _lab.Lab("caught")
try:
    git = _lab.local_git(lab)
    for tokens in (("push", "--force", "origin", "main"),
                   ("commit", "--amend", "-m", "x"),
                   ("reset", "--hard"),
                   ("push", "origin", "+refs/heads/main:refs/heads/main"),
                   ("push", "-f", "origin", "main"),
                   ("update-ref", "refs/heads/main", "HEAD"),
                   ("checkout", "--orphan", "x")):
        try:
            git.status(*tokens)
        except publish.HistoryRewriteRefused as refused:
            print(f"git {' '.join(tokens):<45} -> {refused.code}")
        else:
            print(f"git {' '.join(tokens):<45} -> ADMITTED")
finally:
    lab.close()
