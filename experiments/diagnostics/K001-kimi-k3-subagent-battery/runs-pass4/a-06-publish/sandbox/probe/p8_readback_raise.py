"""Probe 8: transport failure during the read-back, after a successful push.

PENDING_REASONS carries REMOTE_NOT_CONFIRMED, and the docstring promises
'Network failure is retried on an exponential backoff (:data:`PUSH_BACKOFF_SECONDS`)'
and that a publication that does not complete is a PublishPending, never
forced. The question: if the push succeeds but ls-remote/fetch then fail, does
publish() return PublishPending(REMOTE_NOT_CONFIRMED) or raise?

Injection: LocalGit is the published seam; subclass it so the push runs for
real and every ls-remote/fetch afterwards fails like a network blip.
"""

from fixture import Fixture, pub


class BlippedGit(pub.LocalGit):
    """Real git, except ls-remote and fetch fail as a transport blip."""

    def _invoke(self, tokens):
        if tokens and tokens[0] in ("ls-remote", "fetch"):
            return pub.GitOutcome(128, b"", b"fatal: connection reset by peer",
                                  False, tuple(tokens))
        return super()._invoke(tokens)


def main():
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("bytes\n")
        git = BlippedGit(fix.local)
        try:
            result = pub.publish(git, ["run"], "msg", sleep=lambda s: None)
            print("returned:", result.status,
                  result.pending.reason if result.pending else None)
        except pub.PublishError as exc:
            print("RAISED", type(exc).__name__, "code:", exc.code)
            print("detail:", exc.detail[:120])
        # the push really did succeed: check the remote
        remote = fix.sh("-C", str(fix.local), "ls-remote", "origin", "refs/heads/work")
        print("remote tip after the call:", remote.split()[0][:12])
        head = fix.sh("-C", str(fix.local), "rev-parse", "HEAD")
        print("push had already landed:", remote.split()[0] == head)
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
