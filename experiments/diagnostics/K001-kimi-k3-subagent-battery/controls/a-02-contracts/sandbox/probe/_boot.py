"""Put the sandbox root and ``src`` on ``sys.path``; nothing else.

Every probe starts with ``import _boot``.  Reads nothing, writes nothing.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _entry in (ROOT, os.path.join(ROOT, "src")):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)
