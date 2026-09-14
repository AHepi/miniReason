"""Shared fixture: a real clone with a real bare remote through publish()'s own path."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from minireason.loop import publish as pub  # noqa: E402

GIT = shutil.which("git") or "git"


class Fixture:
    """temp bare remote + local clone with an upstream branch."""

    def __init__(self, make_bare=True):
        self.tmp = Path(tempfile.mkdtemp(prefix="pubprobe-"))
        self.bare = self.tmp / "remote.git"
        self.local = self.tmp / "local"
        if make_bare:
            self.sh("init", "--bare", str(self.bare))
        self.sh("init", str(self.local))
        self.sh("-C", str(self.local), "config", "user.email", "probe@example.invalid")
        self.sh("-C", str(self.local), "config", "user.name", "Probe")
        self.sh("-C", str(self.local), "config", "commit.gpgsign", "false")
        (self.local / "seed.txt").write_text("seed\n")
        self.sh("-C", str(self.local), "add", "seed.txt")
        self.sh("-C", str(self.local), "commit", "-m", "seed")
        self.sh("-C", str(self.local), "branch", "-M", "work")
        if make_bare:
            self.sh("-C", str(self.local), "remote", "add", "origin", str(self.bare))
            self.sh("-C", str(self.local), "push", "-u", "origin", "work")

    def sh(self, *argv):
        done = subprocess.run([GIT, *argv], capture_output=True, check=True)
        return done.stdout.decode().strip()

    def cleanup(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


def with_secret(name, value):
    """Context-free helper: register and set a secret env var for the scanner."""
    os.environ[name] = value
    from minireason.provider_openai_compat import register_secret_envs

    register_secret_envs([name])
