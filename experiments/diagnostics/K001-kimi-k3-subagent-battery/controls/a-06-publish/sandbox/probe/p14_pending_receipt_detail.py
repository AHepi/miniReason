"""What a pending publication puts in the step receipt.

``as_receipt()`` is "the step-receipt fields section 4.3 keeps for a
publication". It keeps ``pending_reason`` and drops ``pending.detail``, which is
where the module puts the two runner-v2 codes its compatibility paragraph names
(``PUBLISH_REF_CHANGED``, ``INPUT_NOT_PUBLISHED``).

Run: python3 probe/p14_pending_receipt_detail.py
"""
from __future__ import annotations

import _lab
from minireason.loop import publish


class RefMovesAfterPush(publish.LocalGit):
    """The remote ref is advanced by somebody else between push and read-back."""

    def __init__(self, repo, remote_dir, **kwargs):
        super().__init__(repo, **kwargs)
        self.remote_dir = remote_dir
        self.done = False

    def _invoke(self, tokens):
        outcome = super()._invoke(tokens)
        if tokens and tokens[0] == "push" and outcome.ok and not self.done:
            self.done = True
            head = _lab.git(self.remote_dir, "rev-parse", "refs/heads/main"
                            ).stdout.decode().strip()
            # A DIFFERENT tree: the parent's, so the ref really does disagree.
            tree = _lab.git(self.remote_dir, "rev-parse", head + "^^{tree}"
                            ).stdout.decode().strip()
            other = _lab.git(self.remote_dir, "commit-tree", tree, "-p", head,
                             "-m", "somebody else's later commit").stdout.decode().strip()
            _lab.git(self.remote_dir, "update-ref", "refs/heads/main", other, head)
        return outcome


lab = _lab.Lab("refmoved")
try:
    lab.write("docs/note.md", "published bytes\n")
    git = RefMovesAfterPush(lab.repo, lab.remote, env=dict(_lab.GIT_ENV))
    result = publish.publish(lab.repo, ["docs/note.md"], "publish", "origin/main", git=git)
    print("status          :", result.status)
    print("pending.reason  :", result.pending.reason)
    print("pending.detail  :", result.pending.detail)
    print("verified_line   :", result.verified_line)
    print("as_receipt()    :")
    for key, value in sorted(result.as_receipt().items()):
        print(f"    {key:18}: {value}")
    print("detail in receipt?:",
          any("PUBLISH_REF_CHANGED" in str(v) for v in result.as_receipt().values()))
finally:
    lab.close()
