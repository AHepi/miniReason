"""Baseline: publish() against a real bare remote returns a VERIFIED line.

Establishes that the lab scaffolding drives the module's production path, so a
later probe's failure is the module's and not the scaffolding's.
"""
from __future__ import annotations

import _lab
from minireason.loop import publish

lab = _lab.Lab("happy")
try:
    lab.write("docs/note.md", "a published note\n")
    result = publish.publish(lab.repo, ["docs/note.md"], "publish note",
                             "origin/main", git=_lab.local_git(lab))
    print("status          :", result.status)
    print("paths           :", result.paths)
    print("files           :", result.files)
    print("committed       :", result.committed)
    print("local == remote :", result.local_commit == result.remote_commit)
    print("distinct_remote :", result.distinct_remote_commit)
    print("verified_line   :", result.verified_line)
    print("remote main     :", lab.remote_main())
    print("as_receipt keys :", sorted(result.as_receipt()))
finally:
    lab.close()
