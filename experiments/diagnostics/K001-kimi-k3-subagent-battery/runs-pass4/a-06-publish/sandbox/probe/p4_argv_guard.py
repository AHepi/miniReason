"""Probe 4: the argv guard against every destructive git spelling.

The guard claims: 'refuses everything this module does not itself emit' and
never allows '-A', '--force', '--amend', 'rebase', 'reset', a '+'-prefixed
push refspec, any ref deletion. Attack it with the spellings deviation 6 names
and a few more, on a real checkout, and confirm the module's own argv set
passes. The deletion refspec attack demonstrates the remote ref really gone.
"""

from fixture import Fixture, pub


ATTACKS = [
    ("add", "-A"),
    ("add", "--all", "."),
    ("add", "-u"),
    ("add", "."),
    ("commit", "-a", "-m", "sweep everything"),
    ("push", "--force", "origin", "HEAD:refs/heads/work"),
    ("push", "-f", "origin", "HEAD:refs/heads/work"),
    ("push", "--force-with-lease", "origin", "HEAD:refs/heads/work"),
    ("push", "-d", "origin", "work"),          # short form of --delete
    ("push", "--delete", "origin", "work"),
    ("push", "--mirror", "origin"),
    ("push", "--prune", "origin"),
    ("push", "origin", "+HEAD:refs/heads/work"),
    ("push", "origin", ":refs/heads/work"),    # deletion refspec, empty left side
    ("commit", "--amend", "-m", "x"),
    ("rebase", "origin/work"),
    ("reset", "--hard", "HEAD~1"),
    ("reset", "HEAD~1"),
    ("update-ref", "-d", "refs/heads/work"),
    ("branch", "-D", "work"),
    ("checkout", "--orphan", "tmp"),
    ("symbolic-ref", "HEAD", "refs/heads/other"),
    ("clean", "-fd"),
    ("stash", "drop"),
]


def main():
    fix = Fixture()
    try:
        git = pub.LocalGit(fix.local)
        for argv in ATTACKS:
            try:
                outcome = git.status(*argv)
                print("ALLOWED: git", " ".join(argv), "(exit", outcome.code, ")")
            except pub.HistoryRewriteRefused as exc:
                print(f"refused {exc.code}: git {' '.join(argv)}")
    finally:
        fix.cleanup()

    # The deletion refspec in action: prove the remote branch survived or not.
    fix = Fixture()
    try:
        before = fix.sh("-C", str(fix.local), "ls-remote", "origin", "refs/heads/work")
        git = pub.LocalGit(fix.local)
        outcome = git.status("push", "origin", ":refs/heads/work")
        after = fix.sh("-C", str(fix.local), "ls-remote", "origin", "refs/heads/work")
        print()
        print("remote refs/heads/work before:", bool(before))
        print("deletion push exit code:", outcome.code)
        print("remote refs/heads/work after:", repr(after) or "GONE")
    finally:
        fix.cleanup()

    # explicit-path sweep: does 'add -A' actually stage outside the named path?
    fix = Fixture()
    try:
        (fix.local / "outside.txt").write_text("not mine\n")
        (fix.local / "run").mkdir()
        (fix.local / "run" / "in.txt").write_text("mine\n")
        git = pub.LocalGit(fix.local)
        git.status("add", "-A")
        staged = fix.sh("-C", str(fix.local), "diff", "--cached", "--name-only")
        print("'add -A' staged via LocalGit:", sorted(staged.split()))
    finally:
        fix.cleanup()

    # The module's own argv set must all pass the allow-list check.
    own = [
        ("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"),
        ("rev-parse", "--verify", "--quiet", "HEAD"),
        ("rev-parse", "HEAD"),
        ("rev-parse", "HEAD^{tree}"),
        ("diff", "--cached", "--name-only", "-z"),
        ("ls-files", "--cached", "-z"),
        ("ls-files", "-z", "--cached", "--", "run"),
        ("add", "--", "run"),
        ("diff", "--cached", "--no-color", "--", "run"),
        ("commit", "-m", "msg", "--", "run"),
        ("push", "--porcelain", "--set-upstream", "origin", "HEAD:refs/heads/work"),
        ("ls-remote", "--refs", "origin", "refs/heads/work"),
        ("fetch", "--no-tags", "origin", "refs/heads/work"),
        ("ls-tree", "-r", "-z", "HEAD", "--", "run"),
        ("show", "HEAD:run/a.txt"),
        ("merge-base", "--is-ancestor", "HEAD", "FETCH_HEAD"),
    ]
    for argv in own:
        pub._refuse_history_rewrite(argv)
    print("module's own", len(own), "argvs: all passed the guard")
    try:
        pub._refuse_history_rewrite([])
        print("empty argv ALLOWED <-- defect")
    except pub.HistoryRewriteRefused as exc:
        print("empty argv refused:", exc.code)


if __name__ == "__main__":
    main()
