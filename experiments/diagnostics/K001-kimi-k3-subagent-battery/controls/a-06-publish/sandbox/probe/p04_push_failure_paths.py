"""What each push failure actually costs, and what it returns.

Real repo, real bare remote, real git for everything except ``push``, which is
replaced with a scripted outcome so the failure mode is exactly the one under
test. The backoff sleeps are captured rather than slept.

Run: python3 probe/p04_push_failure_paths.py
"""
from __future__ import annotations

import _lab
from minireason.loop import publish


class ScriptedPush(publish.LocalGit):
    """Real git, except that ``push`` returns a scripted failure."""

    def __init__(self, repo, mode, **kwargs):
        super().__init__(repo, **kwargs)
        self.mode = mode
        self.pushes = 0

    def _invoke(self, tokens):
        if tokens and tokens[0] == "push":
            self.pushes += 1
            if self.mode == "timeout":
                return publish.GitOutcome(-1, b"", b"", True, tuple(tokens))
            if self.mode == "rejected":
                return publish.GitOutcome(
                    1, b"! HEAD:refs/heads/main [rejected] (non-fast-forward)\n",
                    b"error: failed to push some refs\n", False, tuple(tokens))
            return publish.GitOutcome(
                128, b"", b"fatal: unable to access remote: connection reset\n",
                False, tuple(tokens))
        return super()._invoke(tokens)


def run(mode, attempt=1):
    lab = _lab.Lab("push-" + mode)
    try:
        lab.write("docs/note.md", f"note for {mode}\n")
        git = ScriptedPush(lab.repo, mode, env=dict(_lab.GIT_ENV))
        slept = []
        try:
            result = publish.publish(lab.repo, ["docs/note.md"], "publish", "origin/main",
                                     attempt=attempt, git=git, sleep=slept.append)
        except publish.PublishError as error:
            print(f"{mode:>9} attempt={attempt}: raised {type(error).__name__} "
                  f"{error.code}; push invocations={git.pushes}; sleeps={slept} "
                  f"(total {sum(slept)}s)")
            return
        pending = result.pending
        print(f"{mode:>9} attempt={attempt}: status={result.status} "
              f"reason={pending.reason if pending else None}; "
              f"push invocations={git.pushes}; sleeps={slept} (total {sum(slept)}s); "
              f"committed={result.committed}; verified_line={result.verified_line}")
    finally:
        lab.close()


print("GIT_TIMEOUT_SECONDS =", publish.GIT_TIMEOUT_SECONDS,
      "| PUSH_BACKOFF_SECONDS =", publish.PUSH_BACKOFF_SECONDS,
      "| MAX_PUBLISH_ATTEMPTS =", publish.MAX_PUBLISH_ATTEMPTS)
for mode in ("rejected", "timeout", "transport"):
    run(mode)
print()
for attempt in (2, 3):
    run("timeout", attempt=attempt)
print()
print("worst-case wall clock inside ONE publish() call on a timing-out push:")
print("   ", 5 * publish.GIT_TIMEOUT_SECONDS + sum(publish.PUSH_BACKOFF_SECONDS),
      "seconds =", (5 * publish.GIT_TIMEOUT_SECONDS
                    + sum(publish.PUSH_BACKOFF_SECONDS)) / 60.0, "minutes")
