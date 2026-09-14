"""How _classify_push_failure labels REAL git push failures.

The markers in ``_REJECTION_MARKERS`` are matched against stdout+stderr
lower-cased. Two of them -- "failed to push some refs" and "fetch first" -- are
printed by git for failures that are not divergences. A PUSH_REJECTED label is
load-bearing: ``_push`` returns immediately without any backoff retry, and the
module's own docstring says a rejection "is a divergence to be re-fetched and
merged by the driver, not a transient".

The sandbox has no network, so the unreachable-host case exercises a real DNS
failure rather than a simulated one.

Run: python3 probe/p11_classify_real_failures.py
"""
from __future__ import annotations

import _lab
from minireason.loop import publish

print("_REJECTION_MARKERS :", publish._REJECTION_MARKERS)
print()

CASES = (
    ("remote directory does not exist", "/nonexistent/path/to/remote.git"),
    ("unreachable host over https", "https://no-such-host.invalid/r.git"),
    ("remote directory exists but is not a repo", None),
)

for label, url in CASES:
    lab = _lab.Lab("classify")
    try:
        if url is None:
            plain = lab.dir / "not-a-repo"
            plain.mkdir()
            url = str(plain)
        _lab.git(lab.repo, "remote", "set-url", "origin", url)
        lab.write("docs/note.md", "x\n")
        _lab.git(lab.repo, "add", "--", "docs/note.md")
        _lab.git(lab.repo, "commit", "-m", "x")
        git = _lab.local_git(lab, timeout=30.0)
        outcome = git.status("push", "--porcelain", "--set-upstream", "origin",
                             "HEAD:refs/heads/main")
        print(f"--- {label} ---")
        print("exit code      :", outcome.code, "| timed_out:", outcome.timed_out)
        print("git said       :")
        for line in outcome.text().strip().splitlines():
            print("                 ", line)
        print("classified as  :", publish._classify_push_failure(outcome))
        print("would retry?   :",
              publish._classify_push_failure(outcome) != publish.PUSH_REJECTED)
        print()
    finally:
        lab.close()

_lab.banner("for contrast: a real non-fast-forward rejection")
lab = _lab.Lab("real-reject")
try:
    lab.write("a.md", "one\n")
    _lab.git(lab.repo, "add", "--", "a.md")
    _lab.git(lab.repo, "commit", "-m", "A")
    _lab.git(lab.repo, "push", "origin", "main")
    seed = _lab.git(lab.repo, "rev-parse", "HEAD~1").stdout.decode().strip()
    _lab.git(lab.repo, "reset", "--hard", seed)
    lab.write("a.md", "two\n")
    _lab.git(lab.repo, "add", "--", "a.md")
    _lab.git(lab.repo, "commit", "-m", "B")
    outcome = _lab.local_git(lab).status("push", "--porcelain", "--set-upstream",
                                         "origin", "HEAD:refs/heads/main")
    print("git said       :")
    for line in outcome.text().strip().splitlines():
        print("                 ", line)
    print("classified as  :", publish._classify_push_failure(outcome))
finally:
    lab.close()
