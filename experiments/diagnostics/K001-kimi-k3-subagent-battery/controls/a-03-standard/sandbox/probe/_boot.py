"""Put the sandbox root and ``<root>/src`` on ``sys.path``.

Every probe starts with ``import _boot``; there is no PYTHONPATH in this
sandbox and the tool layer allows only ``python3`` command forms.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _entry in (ROOT, os.path.join(ROOT, "src")):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)
