"""Probe 7: does publish() itself ever emit the spellings the guard refuses?

The two holes stand against LocalGit-as-a-seam only if publish()'s own argv is
clean. Re-derive publish()'s argv from source and run the guard on each.

Also: verify_published claims "Is ``commit``'s tree on ``ref`` ... True also
when the remote carries a *different* commit id over an equal tree". The code
compares trees, not ancestry: is a commit whose tree equals the remote tree but
which is NOT an ancestor of the ref reported published? And the inverse: a
commit that IS an ancestor but whose per-path blobs differ?
"""

from fixture import Fixture, pub


def main():
    # --- part A: publish()'s own argv ---
    for argv in [
        ("add", "--", "run"),
        ("push", "--porcelain", "--set-upstream", "origin", "HEAD:refs/heads/work"),
        ("commit", "-m", "msg", "--", "run"),
    ]:
        pub._refuse_history_rewrite(argv)
    print("publish()'s own argv passes the guard: True")

    # --- part B: same tree, zero ancestry ---
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("published bytes\n")
        result = pub.publish(fix.local, ["run"], "publish run", sleep=lambda s: None)
        assert result.published
        remote_tree = fix.sh("-C", str(fix.local), "rev-parse", "HEAD^{tree}")

        # Build a completely unrelated root commit carrying the SAME tree.
        orphan = fix.tmp / "orphan"
        fix.sh("init", str(orphan))
        fix.sh("-C", str(orphan), "config", "user.email", "o@example.invalid")
        fix.sh("-C", str(orphan), "config", "user.name", "Orphan")
        # materialise the tree in the orphan by copying the files
        for p in fix.local.rglob("*"):
            if p.is_file() and ".git" not in p.parts and p.name != "orphan":
                rel = p.relative_to(fix.local)
                target = orphan / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(p.read_bytes())
        fix.sh("-C", str(orphan), "add", "-A")
        fix.sh("-C", str(orphan), "commit", "-m", "unrelated root commit, same content")
        orphan_tree = fix.sh("-C", str(orphan), "rev-parse", "HEAD^{tree}")
        orphan_commit = fix.sh("-C", str(orphan), "rev-parse", "HEAD")
        print("trees equal:", orphan_tree == remote_tree)
        # confirm zero ancestry: merge-base should fail
        ancestor = fix.sh("-C", str(fix.local), "rev-list", "--all")
        print("orphan commit known to local clone:", orphan_commit in ancestor.split())
        verdict = pub.verify_published(fix.local, ["run"], orphan_commit, git=pub.LocalGit(fix.local)) \
            if False else None
        # verify over the local clone: the orphan commit object is not in it,
        # so fetch the object first via the object db? verify_published does
        # rev-parse <commit>^{tree} which requires the object locally.
        try:
            fix.sh("-C", str(fix.local), "fetch", str(orphan), "HEAD")
            orphan_commit_in_local = fix.sh("-C", str(fix.local), "rev-parse", "FETCH_HEAD")
        except Exception:
            orphan_commit_in_local = None
        if orphan_commit_in_local:
            verdict = pub.verify_published(fix.local, ["run"], orphan_commit_in_local)
            print("orphan in local rev-list --all:",
                  orphan_commit_in_local in fix.sh("-C", str(fix.local), "rev-list", "--all").split())
            print("verify_published(zero-ancestry, equal tree):", verdict)
    finally:
        fix.cleanup()

    # --- part C: ancestor of the ref, different content under the paths ---
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        old_seed = fix.sh("-C", str(fix.local), "rev-parse", "HEAD")  # pre-'run' commit
        (run / "a.txt").write_text("v1\n")
        r1 = pub.publish(fix.local, ["run"], "v1", sleep=lambda s: None)
        (run / "a.txt").write_text("v2\n")
        r2 = pub.publish(fix.local, ["run"], "v2", sleep=lambda s: None)
        assert r1.published and r2.published
        # old_seed has no 'run' at all; its tree is an ancestor of the remote
        # tip but the published paths' blobs differ (or are absent).
        print()
        print("verify_published(pre-'run' ancestor commit):",
              pub.verify_published(fix.local, ["run"], old_seed))
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
