"""bracket(): does a failing outcome log mask the original exception?"""
import sys, subprocess, tempfile
from pathlib import Path

sys.path.insert(0, "src")
from minireason.loop import receipts
from minireason.loop.types import LoopError

tmp = Path(tempfile.mkdtemp())
(tmp / "tools").mkdir()
(tmp / "tools" / "repo_activity.py").write_text("import sys; sys.exit(0)\n")
receipts.set_current_receipt("REC-20260915-A")

calls = []
def flaky(argv, **k):
    calls.append(argv)
    class R: returncode = 0 if len(calls) == 1 else 3
    return R()

class OriginalError(Exception):
    pass

try:
    with receipts.bracket("act", "why", "goal", repo_root=tmp, runner=flaky):
        raise OriginalError("the real failure")
except OriginalError:
    print("original exception preserved")
except LoopError as e:
    print("original exception MASKED by", e.code)
