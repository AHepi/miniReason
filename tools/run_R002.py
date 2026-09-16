#!/usr/bin/env python3
"""Run the implemented R002 calibration or main phase."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from minireason.reason.r002_launcher import LauncherError, main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LauncherError as error:
        print("R002_LAUNCHER_REFUSED: " + str(error), file=sys.stderr)
        raise SystemExit(2)
