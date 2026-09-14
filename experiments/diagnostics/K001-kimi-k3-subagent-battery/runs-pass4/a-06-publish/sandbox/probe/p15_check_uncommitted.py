"""Probe 15: check_published can pass on content that was never committed.

check_published's docstring: 'publication-before-dispatch: are these bytes, or
this commit, on the ref? ... A path ... answers "are the working-tree bytes
under it exactly the bytes on the published ref"'. In the path branch it never
checks the working tree == the published commit: anything uncommitted under
the path is invisible. _explicit_paths only checks existence, _tracked_files
the index. Construct: publish v1; then rewrite the file in the working tree
back to the published bytes WITHOUT committing; then check_published.
"""

from fixture import Fixture, pub


def main():
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("published v1\n")
        (run / "b.txt").write_text("stays published\n")
        result = pub.publish(fix.local, ["run"], "publish run", sleep=lambda s: None)
        assert result.published

        # Local history moves on: a.txt changed and COMMITTED locally...
        (run / "a.txt").write_text("v2, committed locally, never pushed\n")
        fix.sh("-C", str(fix.local), "add", "run/a.txt")
        fix.sh("-C", str(fix.local), "commit", "-m", "local v2, unpushed")
        # ... then the working tree is restored byte-for-byte to v1 by hand.
        (run / "a.txt").write_text("published v1\n")
        print("git status --porcelain run:", repr(fix.sh("-C", str(fix.local),
              "status", "--porcelain", "--", "run")))
        print("a.txt committed at HEAD:", fix.sh("-C", str(fix.local),
              "show", "HEAD:run/a.txt"))
        print("a.txt on the remote    :", fix.sh("-C", str(fix.local),
              "show", result.remote_commit + ":run/a.txt"))
        verdict = pub.check_published(fix.local, "run")
        print("check_published('run'):", verdict)
        print("-> True means: the gate passed although HEAD under 'run' differs",
              "\n   from what is published (its own commit is unpushed).")
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
