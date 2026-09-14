"""Probe 13: attack the credential scan's coverage claims.

* Credential set via LocalGit(env=...): environment() strips it from the child,
  but 'this process can see' is os.environ only — the scan must not refuse,
  and the child must not receive the value.
* Credential in a file OUTSIDE the named paths but inside the repo: publish
  must succeed (explicit-path discipline), and the scan stays silent.
* Credential of length 7 (below _MIN_SECRET_LENGTH=8): never detected.
* Credential string that appears inside the commit MESSAGE: is the message
  scanned at all?
"""

import os

from fixture import Fixture, pub, with_secret


def main():
    # A: child environment is scrubbed even when the caller hands env in.
    fix = Fixture()
    try:
        git = pub.LocalGit(fix.local, env={"SECRET_VALUE": "sk-zzzzzzzz", "HOME": "/tmp"})
        env = git.environment()
        print("A: SECRET_VALUE in env passed to LocalGit:",
              "SECRET_VALUE" in env, "(not a registry name -> kept)")
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("clean\n")
        result = pub.publish(git, ["run"], "msg", sleep=lambda s: None)
        print("A: publish over env-only secret:", result.status)
    finally:
        fix.cleanup()

    # B: credential in a path NOT being published
    secret = "sk-outside-the-paths-1234"
    with_secret("PROBE_CRED", secret)
    fix = Fixture()
    try:
        (fix.local / "private").mkdir()
        (fix.local / "private" / "notes.txt").write_text(f"token={secret}\n")
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("clean\n")
        result = pub.publish(fix.local, ["run"], "msg", sleep=lambda s: None)
        print("B: publish with credential outside named paths:", result.status)
    finally:
        fix.cleanup()

    # C: 7-char credential
    with_secret("PROBE_CRED", "short77")
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("short77\n")
        result = pub.publish(fix.local, ["run"], "msg", sleep=lambda s: None)
        print("C: 7-char credential published:", result.status)
    finally:
        os.environ.pop("PROBE_CRED", None)
        fix.cleanup()

    # D: credential in the commit message itself
    secret = "sk-in-the-message-98765"
    with_secret("PROBE_CRED", secret)
    fix = Fixture()
    try:
        run = fix.local / "run"
        run.mkdir()
        (run / "a.txt").write_text("clean\n")
        result = pub.publish(fix.local, ["run"], f"rotate key {secret}",
                             sleep=lambda s: None)
        print("D: publish with credential in the commit MESSAGE:", result.status)
        log = fix.sh("-C", str(fix.local), "log", "-1", "--format=%B")
        print("   remote commit message carries the credential:", secret in log)
    finally:
        os.environ.pop("PROBE_CRED", None)
        fix.cleanup()


if __name__ == "__main__":
    main()
