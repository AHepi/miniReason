"""Probe 9: verify_published checks the index, not the commit's blobs.

verify_published's docstring asks 'Is ``commit``'s tree on ``ref``, with these
paths' objects published?' and deviation 7 says 'Verification compares
committed trees, never the working tree'. But _read_back expects the blobs of
``source`` built by _tracked_files = ``ls-files --cached`` = the INDEX. So a
caller asking about an older commit, with the index holding newer content
under the same paths, must get False even though the older commit's tree is
equal to the remote tree — the expected side is wrong because the index moved.

This is the committed-vs-index confusion, exercised through the published seam.
"""

from fixture import Fixture, pub


def main():
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("v1\n")
        r1 = pub.publish(fix.local, ["run"], "v1", sleep=lambda s: None)
        assert r1.published
        c1 = r1.remote_commit
        print("verify_published(v1) right after publishing v1:",
              pub.verify_published(fix.local, ["run"], c1))

        # Publish v2: the remote ref now carries v2 over the same paths.
        (run / "a.txt").write_text("v2\n")
        r2 = pub.publish(fix.local, ["run"], "v2", sleep=lambda s: None)
        assert r2.published

        # Roll the remote ref back to v1 (simulating the connector keeping v1
        # or a re-publish decision): v1's tree IS the remote tree.
        fix.sh("-C", str(fix.local), "push", "--force", "origin", c1 + ":refs/heads/work")
        # But the local index/HEAD now carries v2.
        print("remote tip is v1 again:",
              fix.sh("-C", str(fix.local), "ls-remote", "origin", "refs/heads/work").split()[0] == c1)
        print("index (ls-files --cached) content for run/a.txt: v2")
        print("verify_published(v1)  :", pub.verify_published(fix.local, ["run"], c1),
              "<-- v1's per-path blobs ARE the remote's per-path blobs, yet False")
        # And, symmetrically: verify_published(v2) must be False (correct),
        # but for the wrong reason — the expected side is the index, which
        # happens to equal v2, masking whether v2 actually reached the remote.
        print("verify_published(v2)  :", pub.verify_published(fix.local, ["run"], r2.remote_commit))
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
