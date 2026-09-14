"""Probe 5: misclassification risk of _classify_push_failure, and timeout.

A push that fails for a NON-rejection reason must never come back as
PUSH_REJECTED (that would ask the driver to merge a transient) nor silently
as PUBLISHED. Attack with an unreachable remote (transport) and a tiny timeout.
"""

from fixture import Fixture, pub


def main():
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("bytes\n")
        # Point origin at a path that does not exist: git exits non-zero,
        # nothing matches _REJECTION_MARKERS -> must be PUSH_TRANSPORT.
        fix.sh("-C", str(fix.local), "remote", "set-url", "origin",
               str(fix.tmp / "nonexistent.git"))
        slept = []
        result = pub.publish(fix.local, ["run"], "msg", sleep=slept.append)
        print("status:", result.status, "reason:", result.pending.reason)
        print("sleeps:", slept, "count==len(PUSH_BACKOFF_SECONDS):",
              len(slept) == len(pub.PUSH_BACKOFF_SECONDS))
        detail = result.pending.detail
        print("detail length <= ~400+prefix:", len(detail) - len('git push - ' if False else '') )
        print("detail:", detail[:120].replace("\n", " | "))

        # attempt 3 with the same failure must raise PublishNotConverging
        try:
            pub.publish(fix.local, ["run"], "msg", attempt=3, sleep=lambda s: None)
            print("attempt 3: NO RAISE <-- defect")
        except pub.PublishNotConverging as exc:
            print("attempt 3 raises:", exc.code)
    finally:
        fix.cleanup()

    # timeout path: LocalGit with a tiny timeout against an unreachable host
    fix = Fixture()
    try:
        fix.sh("-C", str(fix.local), "remote", "set-url", "origin",
               "http://192.0.2.1:9/never.git")  # TEST-NET-1, port 9, will hang/refuse
        fix.sh("-C", str(fix.local), "commit", "--allow-empty", "-m", "pending work")
        git = pub.LocalGit(fix.local, timeout=0.5)
        try:
            result = pub.publish(git, ["seed.txt"], "msg", sleep=lambda s: None)
            print("timeout-ish -> status:", result.status,
                  "reason:", result.pending.reason if result.pending else None)
        finally:
            pass
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
