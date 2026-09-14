"""Static probe: every failure code publish.py can raise is in types.FAILURE_CODES."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from minireason.loop.types import FAILURE_CODES  # noqa: E402
from minireason.loop import publish  # noqa: E402

src = Path(publish.__file__).read_text()
raised = set(re.findall(r'raise \w+\(\s*"([A-Z][A-Z0-9_]*)"', src))
via_sub = re.findall(r'super\(\)\.__init__\("([A-Z][A-Z0-9_]*)"', src)
raised.update(via_sub)
raised.update(re.findall(r'PublishError\.__init__\(self, "([A-Z][A-Z0-9_]*)"', src))

print("codes raised by publish.py:", len(raised))
missing = sorted(raised - set(FAILURE_CODES))
print("missing from FAILURE_CODES:", missing)
assert not missing
