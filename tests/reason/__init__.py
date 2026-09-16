"""Offline reason tests with an optional persistent artifact root."""
import os
from pathlib import Path


def artifact_root():
    return Path(__file__).resolve().parents[2] / os.environ.get("MINIREASON_TEST_WORK", "work/review12b")
