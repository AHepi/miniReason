"""Probe 16: do the rejection markers fire on every push-failure wording?

_claim_: '[rejected]' in _REJECTION_MARKERS makes any porcelain line
containing it classify as PUSH_REJECTED. A rejected-delete line also carries
'[rejected]'; but this module never deletes. More important: does a real
rejection (hook refusal) print differently, e.g. '[remote rejected]'? And does
GitOutcome.text() leak anything raw? Also confirm PublishResult.as_receipt()
never carries credential values and never 'exhaustion'.
"""

from fixture import Fixture, pub


def main():
    # A hook-refused push: install a pre-receive hook on the bare repo.
    fix = Fixture()
    try:
        hook = fix.bare / "hooks" / "pre-receive"
        hook.write_text("#!/bin/sh\necho 'policy: no pushes today' >&2\nexit 1\n")
        hook.chmod(0o755)
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("x\n")
        result = pub.publish(fix.local, ["run"], "msg", sleep=lambda s: None)
        print("hook refusal ->", result.status, result.pending.reason)
        print("detail:", result.pending.detail[:160].replace("\n", " | "))
    finally:
        fix.cleanup()

    # as_receipt shape
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("x\n")
        result = pub.publish(fix.local, ["run"], "msg", sleep=lambda s: None)
        receipt = result.as_receipt()
        print("receipt keys:", sorted(receipt))
        print("'exhaustion' anywhere in receipt:", "exhaustion" in str(receipt))
        print("pending_reason:", receipt["pending_reason"])
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
