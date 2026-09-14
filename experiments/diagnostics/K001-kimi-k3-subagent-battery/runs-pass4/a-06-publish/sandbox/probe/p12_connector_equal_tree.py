"""Probe 12: equal-tree connector commit recorded with both ids (§4.5 claim).

Claim: 'the equal-tree acceptance of a connector-authored remote commit with
**both** commit ids recorded'. Simulation: the connector force-pushes a
re-authored commit (same tree, new id) over ours; the driver's next publish
step for the same paths must then be accepted as PUBLISHED with local !=
remote recorded on the result and in the line.
"""

from fixture import Fixture, pub


def main():
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("x\n")
        r1 = pub.publish(fix.local, ["run"], "publish", sleep=lambda s: None)
        assert r1.published

        # Driver reconciles after seeing the connector's re-authored commit:
        fix.sh("-C", str(fix.local), "fetch", "origin", "work")
        fix.sh("-C", str(fix.local), "commit", "--amend", "--no-edit",
               "--author=Connector <c@example.invalid>")
        reauthored = fix.sh("-C", str(fix.local), "rev-parse", "HEAD")
        fix.sh("-C", str(fix.local), "push", "--force", "origin", "HEAD:refs/heads/work")
        fix.sh("-C", str(fix.local), "reset", "--hard", r1.remote_commit)
        fix.sh("-C", str(fix.local), "fetch", "origin", "work")
        fix.sh("-C", str(fix.local), "merge", "--no-edit", "FETCH_HEAD")
        local_after_merge = fix.sh("-C", str(fix.local), "rev-parse", "HEAD")

        r2 = pub.publish(fix.local, ["run"], "nothing new (attempt 2)",
                         attempt=2, sleep=lambda s: None)
        print("status:", r2.status, "committed:", r2.committed)
        print("local_commit :", r2.local_commit)
        print("remote_commit:", r2.remote_commit)
        print("local == merged HEAD:", r2.local_commit == local_after_merge)
        print("distinct_remote_commit:", r2.distinct_remote_commit)
        print("both ids in verified_line:",
              r2.local_commit in (r2.verified_line or "") and
              r2.remote_commit in (r2.verified_line or ""))
        print("verified_line:", r2.verified_line)
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
