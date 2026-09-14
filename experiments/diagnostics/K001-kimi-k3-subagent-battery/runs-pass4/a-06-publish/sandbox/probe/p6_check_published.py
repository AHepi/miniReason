"""Probe 6: check_published / verify_published edge behaviour (corrected).

* check_published on a path whose remote bytes differ from disk (post-publish
  local edit): must be False.
* check_published on a target that is neither path nor 40-hex: must RAISE
  CHECK_TARGET_UNKNOWN, not return False ('a gate that cannot answer must not
  answer False').
* check_published with an ancestor sha: True; with an unpushed commit: False.
* verify_published must keep answering True after later local writes under the
  same paths (deviation 7 claim, the seam that was once broken).
* verify_published on an unpushed commit whose tree differs from the remote
  tree must be False — the p6 draft got True only because the empty commit it
  built happened to carry an equal tree.
"""

from fixture import Fixture, pub


def main():
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("published bytes\n")
        result = pub.publish(fix.local, ["run"], "publish run", sleep=lambda s: None)
        assert result.published
        print("check_published(path, clean):", pub.check_published(fix.local, "run"))

        (run / "a.txt").write_text("edited after publish\n")
        print("check_published(path, edited):", pub.check_published(fix.local, "run"))
        print("verify_published(paths, commit) after edit:",
              pub.verify_published(fix.local, ["run"], result.remote_commit))

        parent = fix.sh("-C", str(fix.local), "rev-parse", "HEAD~1")
        print("check_published(ancestor sha):", pub.check_published(fix.local, parent))

        try:
            print("check_published(bogus token):",
                  pub.check_published(fix.local, "not-a-path-nor-sha"))
        except pub.PublishError as exc:
            print("check_published(bogus token) raises:", exc.code)

        # unpushed commit with DIFFERENT content under the published paths
        (run / "a.txt").write_text("unpushed different bytes\n")
        fix.sh("-C", str(fix.local), "add", "run/a.txt")
        fix.sh("-C", str(fix.local), "commit", "-m", "not pushed")
        unpushed = fix.sh("-C", str(fix.local), "rev-parse", "HEAD")
        print("check_published(unpushed commit, differing tree):",
              pub.check_published(fix.local, unpushed))
        print("verify_published(unpushed commit, differing tree):",
              pub.verify_published(fix.local, ["run"], unpushed))
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
