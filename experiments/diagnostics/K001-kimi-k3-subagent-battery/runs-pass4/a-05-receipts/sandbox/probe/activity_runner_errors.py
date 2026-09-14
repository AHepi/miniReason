"""Does every way the activity logger can fail carry a LoopError code?

activity() docstring: 'Every way the logger can fail carries a code from the
table.' It converts subprocess.TimeoutExpired. Try other failure shapes.
"""
import sys, subprocess
from pathlib import Path
import tempfile

sys.path.insert(0, "src")
from minireason.loop import receipts
from minireason.loop.types import LoopError

tmp = Path(tempfile.mkdtemp())
(tmp / "tools").mkdir()
(tmp / "tools" / "repo_activity.py").write_text("import sys; sys.exit(0)\n")
receipts.set_current_receipt("REC-20260915-A")

# 1. negative timeout -> subprocess.run raises ValueError, not TimeoutExpired
try:
    receipts.activity("begin", "act", "why", "goal", repo_root=tmp, timeout=-1.0)
    print("negative timeout: no exception")
except LoopError as e:
    print("negative timeout: LoopError", e.code)
except Exception as e:
    print("negative timeout: NON-LoopError", type(e).__name__, e)

# 2. runner that raises OSError (e.g. executable vanished)
def dead_runner(*a, **k):
    raise OSError("No such file or directory")
try:
    receipts.activity("begin", "act", "why", "goal", repo_root=tmp, runner=dead_runner)
    print("OSError runner: no exception")
except LoopError as e:
    print("OSError runner: LoopError", e.code)
except Exception as e:
    print("OSError runner: NON-LoopError", type(e).__name__, e)

# 3. timeout -> converted (control, should be LoopError)
def slow_runner(*a, **k):
    raise subprocess.TimeoutExpired(cmd=a[0], timeout=30.0)
try:
    receipts.activity("begin", "act", "why", "goal", repo_root=tmp, runner=slow_runner)
except LoopError as e:
    print("timeout runner: LoopError", e.code)
