"""A path name that is not valid UTF-8.

``_staged_names`` and ``_tracked_files`` both call ``.decode("utf-8")`` with no
error handler, on bytes that came from the filesystem through git.

Run: python3 probe/p15_non_utf8_path.py
"""
from __future__ import annotations

import os

import _lab
from minireason.loop import publish

lab = _lab.Lab("non-utf8")
try:
    raw = os.fsencode(str(lab.repo)) + b"/docs"
    os.makedirs(raw, exist_ok=True)
    name = raw + b"/caf\xe9.md"
    with open(name, "wb") as handle:
        handle.write(b"a document whose NAME is latin-1\n")
    relative = os.fsdecode(b"docs/caf\xe9.md")
    print("path as python sees it :", repr(relative))
    print("_explicit_paths        :", publish._explicit_paths(lab.repo.resolve(), [relative]))
    try:
        result = publish.publish(lab.repo, [relative], "publish", "origin/main",
                                 git=_lab.local_git(lab))
    except publish.PublishError as error:
        print("publish()              -> PublishError", error.code)
    except Exception as error:                                   # noqa: BLE001
        import traceback

        from minireason.loop.types import LoopError

        print("publish()              ->", type(error).__name__, ":", error)
        print("is it a LoopError?     :", isinstance(error, LoopError))
        frames = [f for f in traceback.extract_tb(error.__traceback__)
                  if f.filename.endswith("publish.py")]
        for frame in frames:
            print(f"    publish.py:{frame.lineno}  {frame.line}")
        print("index left staged      :", lab.staged() or "(clean)")
    else:
        print("publish()              -> ", result.status, result.files)
finally:
    lab.close()
