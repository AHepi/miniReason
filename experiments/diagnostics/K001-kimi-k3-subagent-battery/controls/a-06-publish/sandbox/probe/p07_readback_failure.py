"""A read-back that cannot run raises instead of leaving the publication PENDING.

The push has already succeeded and the remote ref already carries the commit.
``REMOTE_NOT_CONFIRMED`` is a published member of ``PENDING_REASONS``, but it is
only reachable when ``ls-remote``/``fetch`` *succeed and disagree*; when either
command fails or hits the 90 s git wall clock, ``LocalGit.run``/``.text`` raise
``GitCommandFailed`` straight out of ``publish()``.

Run: python3 probe/p07_readback_failure.py
"""
from __future__ import annotations

import _lab
from minireason.loop import publish


class BreakAfterPush(publish.LocalGit):
    """Real git, except that one named subcommand fails once the push is done."""

    def __init__(self, repo, break_on, mode, **kwargs):
        super().__init__(repo, **kwargs)
        self.break_on = break_on
        self.mode = mode
        self.pushed = False

    def _invoke(self, tokens):
        if tokens and tokens[0] == self.break_on and self.pushed:
            if self.mode == "timeout":
                return publish.GitOutcome(-1, b"", b"", True, tuple(tokens))
            return publish.GitOutcome(128, b"",
                                      b"fatal: unable to access remote: connection reset\n",
                                      False, tuple(tokens))
        outcome = super()._invoke(tokens)
        if tokens and tokens[0] == "push" and outcome.ok:
            self.pushed = True
        return outcome


print("PENDING_REASONS :", publish.PENDING_REASONS)
print()

for break_on, mode in (("ls-remote", "timeout"), ("ls-remote", "transport"),
                       ("fetch", "timeout"), ("rev-parse", "transport")):
    lab = _lab.Lab(f"readback-{break_on}-{mode}")
    try:
        lab.write("docs/note.md", "published bytes\n")
        git = BreakAfterPush(lab.repo, break_on, mode, env=dict(_lab.GIT_ENV))
        try:
            result = publish.publish(lab.repo, ["docs/note.md"], "publish", "origin/main",
                                     git=git)
        except publish.PublishError as error:
            outcome = f"raised {type(error).__name__} {error.code}"
            detail = error.detail
        else:
            outcome = (f"returned {result.status}"
                       + (f" / {result.pending.reason}" if result.pending else ""))
            detail = ""
        local = _lab.git(lab.repo, "rev-parse", "HEAD").stdout.decode().strip()
        print(f"{break_on} {mode:<9} -> {outcome}")
        if detail:
            print(f"    detail            : {detail.strip()[:110]}")
        print(f"    local HEAD         : {local}")
        print(f"    remote refs/heads/main: {lab.remote_main()}")
        print(f"    the push DID land   : {local == lab.remote_main()}")
    finally:
        lab.close()
