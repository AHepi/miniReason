"""Probe 3: happy path, VERIFIED line shape, and the divergent-remote case.

* Happy path against a real bare repo, checking the VERIFIED line fields.
* Divergent rejection: remote advances beyond local; publish() must return
  PublishPending(PUSH_REJECTED), never force.
* After the driver's documented flow (fetch + merge), the same publication
  succeeds on a later attempt.
"""

from fixture import Fixture, pub


def main():
    fix = Fixture()
    try:
        run = fix.local / "run" / "data"
        run.mkdir(parents=True)
        (run / "a.txt").write_text("alpha-bytes\n")
        (run / "b.txt").write_text("beta-bytes\n")

        slept = []
        result = pub.publish(fix.local, ["run"], "publish run/data",
                             sleep=slept.append)
        print("status:", result.status)
        print("published:", result.published)
        print("committed:", result.committed)
        print("local_commit == remote_commit:", result.local_commit == result.remote_commit)
        print("distinct_remote_commit:", result.distinct_remote_commit)
        print("sleeps taken:", slept)
        print("VERIFIED line:")
        print(result.verified_line)
        head = fix.sh("-C", str(fix.local), "rev-parse", "HEAD")
        print("line carries HEAD:", head in result.verified_line)
        remote_sha = fix.sh("-C", str(fix.local), "ls-remote", "origin", "refs/heads/work")
        print("ls-remote:", remote_sha.split()[0] == result.remote_commit)
        print("verify_published(own commit):",
              pub.verify_published(fix.local, ["run"], result.remote_commit))
        print("staged after:", repr(fix.sh("-C", str(fix.local), "diff", "--cached", "--name-only")))
    finally:
        fix.cleanup()

    # --- divergent remote: the remote tip advances past local HEAD ---
    fix = Fixture()
    try:
        other = fix.tmp / "other"
        fix.sh("clone", "--branch", "work", str(fix.bare), str(other))
        fix.sh("-C", str(other), "config", "user.email", "other@example.invalid")
        fix.sh("-C", str(other), "config", "user.name", "Other")
        fix.sh("-C", str(other), "config", "commit.gpgsign", "false")
        fix.sh("-C", str(other), "commit", "--allow-empty", "-m", "connector commit")
        fix.sh("-C", str(other), "push", "origin", "work")

        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("content\n")
        result = pub.publish(fix.local, ["run"], "publish run", sleep=lambda s: None)
        print()
        print("divergent remote -> status:", result.status)
        print("pending reason:", result.pending.reason if result.pending else None)
        print("pending detail:", (result.pending.detail or "")[:120].replace("\n", " | "))
        fix.sh("-C", str(fix.local), "fetch", "origin", "work")
        fix.sh("-C", str(fix.local), "merge", "--no-edit", "FETCH_HEAD")
        result2 = pub.publish(fix.local, ["run"], "publish run (attempt 2)",
                              attempt=2, sleep=lambda s: None)
        print("after fetch+merge, attempt 2 -> status:", result2.status)
        print("after fetch+merge, published:", result2.published)
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
