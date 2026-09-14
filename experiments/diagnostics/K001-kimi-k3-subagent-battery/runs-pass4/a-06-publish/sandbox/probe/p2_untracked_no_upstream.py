"""Probe 2: untracked path + no upstream -> the refusal order.

Docstring, publish(): '''paths are explicit repo-relative or absolute paths
that must exist'''. Design §4.5: explicit path add; acceptance:
'a planted secret in the staged diff refuses the publish'. _explicit_paths is
documented to refuse 'anything absent'. For a path that exists on disk but is
never tracked, and a publish_ref that cannot resolve, which refusal wins?
"""

import os

from fixture import Fixture, pub, with_secret


def main():
    fix = Fixture(make_bare=False)  # no 'origin' remote at all -> upstream unresolvable
    try:
        secret = "probe-credential-00a1b2c3"
        with_secret("PROBE_CRED", secret)
        run_dir = fix.local / "run"
        run_dir.mkdir()
        (run_dir / "planted.txt").write_text(f"key={secret}\n")  # untracked, credential-bearing
        try:
            pub.publish(fix.local, ["run"], "publish run", sleep=lambda s: None)
            print("no exception raised")
        except pub.PublishError as exc:
            print("raised code:", exc.code)
            print("order: _explicit_paths first would give PATH_MISSING/PATH_IS_REPO_ROOT;")
            print("       _refuse_credentials first would give SECRET_IN_STAGED_DIFF;")
            print("       upstream_ref first gives PUBLISH_REF_UNRESOLVED")
        finally:
            os.environ.pop("PROBE_CRED", None)
    finally:
        fix.cleanup()


if __name__ == "__main__":
    main()
