"""BLOCKER probe: a bracketed path name reaches git as a pathspec GLOB.

``_explicit_paths`` refuses ``*`` and ``?`` but not ``[`` / ``]``. Git's
pathspec matcher is wildmatch, where ``[ab]`` is a character class. So an
explicit, existing, caller-named path can

  * fail to match itself, and
  * match and stage a *different* file the caller never named and
    ``_refuse_credentials`` never read.

Run: python3 probe/p01_bracket_pathspec.py
"""
from __future__ import annotations

import _lab
from minireason.loop import publish

lab = _lab.Lab("bracket")
try:
    # The file the caller names, literally called "report[1].md".
    lab.write("report[1].md", "THE NAMED FILE\n")
    # A neighbour the caller does not name. "[1]" as a class matches "1".
    lab.write("report1.md", "THE UNNAMED NEIGHBOUR\n")

    names = publish._explicit_paths(lab.repo.resolve(), ["report[1].md"])
    print("_explicit_paths accepted :", names)

    result = publish.publish(lab.repo, ["report[1].md"], "publish the named file",
                             "origin/main", git=_lab.local_git(lab))
    print("status                   :", result.status)
    print("result.paths (named)     :", result.paths)
    print("result.files (published) :", result.files)
    print("VERIFIED line            :", result.verified_line)

    published = _lab.git(lab.remote, "ls-tree", "-r", "--name-only",
                         "refs/heads/main").stdout.decode().split()
    print("remote tree contents     :", published)
    print("named file published?    :", "report[1].md" in published)
    print("unnamed file published?  :", "report1.md" in published)
    print("bytes of what landed     :",
          _lab.git(lab.remote, "show", "refs/heads/main:report1.md").stdout)
finally:
    lab.close()
