"""Probe 11: does publish() always commit every change under its named paths?

Claim ('Nothing else is ever staged' + explicit-path add + 'publish step'
discipline): after publish() returned, the working tree is clean under the
published paths. Attack: give publish() a path with one tracked-modified and
one new-untracked file, and afterwards ask git status whether anything under
the path was left behind. If anything under `paths` remains uncommitted after
a PUBLISHED result, a run under this module can drift silently.
"""

from fixture import Fixture, pub


def main():
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "tracked.txt").write_text("v1\n")
        fix.sh("-C", str(fix.local), "add", "run/tracked.txt")
        fix.sh("-C", str(fix.local), "commit", "-m", "base")
        fix.sh("-C", str(fix.local), "push", "origin", "work")

        (run / "tracked.txt").write_text("v2 MODIFIED\n")       # tracked, modified
        (run / "new.txt").write_text("brand new\n")             # untracked
        result = pub.publish(fix.local, ["run"], "publish run", sleep=lambda s: None)
        print("status:", result.status, "committed:", result.committed)
        status = fix.sh("-C", str(fix.local), "status", "--porcelain", "--", "run")
        print("git status -- run, after PUBLISHED:", repr(status))
        # what did the published commit actually contain under run/?
        committed = fix.sh("-C", str(fix.local), "ls-tree", "-r", "--name-only", "HEAD", "run")
        print("committed files under run/:", committed.split())
        print("check_published('run'):", pub.check_published(fix.local, "run"))
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
