"""Probe 1: a credential in a file under the publish path, NOT staged.

Deviation 3 / O8 claim the working-tree scan is load-bearing: 'Scanning first
means a planted credential is refused with the index still clean'. We plant a
credential in an unstaged file under the published directory and check both the
refusal and the index afterwards.
"""

import os
import subprocess

from fixture import Fixture, GIT, pub, with_secret


def staged_entries(local):
    out = subprocess.run([GIT, "-C", str(local), "diff", "--cached", "--name-only"],
                         capture_output=True, check=True)
    return out.stdout.decode()


def main():
    fix = Fixture()
    try:
        secret = "probe-secret-value-7f3c9d1a"
        with_secret("PROBE_CRED", secret)
        target = fix.local / "run" / "notes.txt"
        target.parent.mkdir(parents=True)
        # The credential file exists only in the working tree, never staged.
        target.write_text(f"token = {secret}\n")
        # Confirm git does not have it staged.
        print("staged before publish():", repr(staged_entries(fix.local)))
        try:
            pub.publish(fix.local, ["run"], "publish run", sleep=lambda s: None)
            print("NOT REFUSED -- defect")
        except pub.CredentialInStagedDiff as exc:
            print("refused code:", exc.code)
            print("refused detail:", exc.detail)
            print("secret value in detail:", secret in str(exc))
        print("staged after publish():", repr(staged_entries(fix.local)))
        # Also: the unstaged file must not have been committed.
        log = fix.sh("-C", str(fix.local), "log", "--oneline", "-1")
        print("last commit:", log)
        # And environment(): the credential must not reach the child process.
        git = pub.LocalGit(fix.local)
        print("PROBE_CRED in child env:", "PROBE_CRED" in git.environment())
    finally:
        os.environ.pop("PROBE_CRED", None)
        fix.cleanup()


if __name__ == "__main__":
    main()
