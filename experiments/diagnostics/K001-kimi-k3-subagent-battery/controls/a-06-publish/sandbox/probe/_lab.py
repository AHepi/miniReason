"""Shared scaffolding for the W0-PUBLISH probes.

Every probe builds a *real* checkout with a *real* bare remote in a temp dir and
drives ``minireason.loop.publish`` against it, which is the path design section
4.7 asks for ("every git operation runs against a real bare repo in a temp dir
through the same ``publish()`` path").

Nothing here is imported by anything under ``src/``; these files only read it.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _entry in (str(ROOT), str(ROOT / "src")):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

GIT_ENV = {
    "GIT_AUTHOR_NAME": "probe",
    "GIT_AUTHOR_EMAIL": "probe@example.invalid",
    "GIT_COMMITTER_NAME": "probe",
    "GIT_COMMITTER_EMAIL": "probe@example.invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_SYSTEM": "/dev/null",
    "GIT_TERMINAL_PROMPT": "0",
    "HOME": "/nonexistent-probe-home",
    "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
    "LANG": "C.UTF-8",
}


def git(cwd, *tokens, check=True):
    """Raw git, outside the module's guard: used only to BUILD fixtures."""

    done = subprocess.run(["git", "-C", str(cwd), *tokens], capture_output=True,
                          env=GIT_ENV, check=False)
    if check and done.returncode != 0:
        raise RuntimeError(f"git {tokens} -> {done.returncode}\n"
                           f"{done.stdout.decode(errors='replace')}\n"
                           f"{done.stderr.decode(errors='replace')}")
    return done


class Lab:
    """A work checkout with an ``origin`` bare remote, on branch ``main``."""

    def __init__(self, name: str) -> None:
        self.dir = Path(tempfile.mkdtemp(prefix=f"w0publish-{name}-")).resolve()
        self.remote = self.dir / "remote.git"
        self.repo = self.dir / "work"
        git(self.dir, "init", "--bare", "--initial-branch=main", str(self.remote))
        git(self.dir, "init", "--initial-branch=main", str(self.repo))
        git(self.repo, "remote", "add", "origin", str(self.remote))
        self.write("README.md", "seed\n")
        git(self.repo, "add", "--", "README.md")
        git(self.repo, "commit", "-m", "seed")
        git(self.repo, "push", "--set-upstream", "origin", "main")

    # -- fixture helpers ----------------------------------------------------
    def write(self, relative: str, text: str) -> Path:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def head(self, where=None) -> str:
        target = self.remote if where == "remote" else self.repo
        return git(target, "rev-parse", "HEAD" if where != "remote" else "refs/heads/main"
                   ).stdout.decode().strip()

    def remote_main(self) -> str:
        return git(self.remote, "rev-parse", "refs/heads/main").stdout.decode().strip()

    def staged(self) -> list[str]:
        out = git(self.repo, "diff", "--cached", "--name-only").stdout.decode()
        return [line for line in out.splitlines() if line]

    def tracked(self) -> list[str]:
        out = git(self.repo, "ls-files").stdout.decode()
        return [line for line in out.splitlines() if line]

    def close(self) -> None:
        shutil.rmtree(self.dir, ignore_errors=True)


def local_git(lab, **kwargs):
    """A :class:`publish.LocalGit` whose child env is the probe's clean env."""

    from minireason.loop import publish

    return publish.LocalGit(lab.repo, env=dict(GIT_ENV), **kwargs)


def banner(text: str) -> None:
    print("=" * 72)
    print(text)
    print("=" * 72)
