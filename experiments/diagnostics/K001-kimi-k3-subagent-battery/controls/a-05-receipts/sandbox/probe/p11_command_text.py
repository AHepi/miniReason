"""W0-RECEIPTS acceptance: 'activity records carry no raw command text.'
AGENTS.md: 'never log credentials or raw secret-bearing command text.'

_COMMAND_TEXT_MARKERS is a 15-substring blocklist.  What gets through it?
"""
from __future__ import annotations

import _bootstrap  # noqa: F401
import os
import tempfile
from pathlib import Path
from types import SimpleNamespace

from minireason.loop import receipts as R
from minireason.loop.types import LoopError

os.environ["PROBE_FAKE_KEY"] = "sk-probe-0123456789abcdef"
from minireason.provider_openai_compat import register_secret_envs  # noqa: E402
register_secret_envs(["PROBE_FAKE_KEY"])

CANDIDATES = [
    # plainly credential-bearing command text, no marker in the list
    "python3 tools/provider_smoke.py --api-key sk-live-9f3a2b7c11de",
    "python3 tools/provider_smoke.py --key sk-live-9f3a2b7c11de",
    "psql postgres://loop:hunter2hunter2@db.internal/runs",
    "wget -O plan.json https://user:hunter2hunter2@host/plan.json",
    "ssh -i /home/user/.ssh/id_ed25519 deploy@host",
    "http POST api.example/v1 X-Api-Key:sk-live-9f3a2b7c11de",
    # the markers that are in the list, for contrast
    "curl -H 'Authorization: Bearer sk-live-9f3a2b7c11de' https://api.example",
    "export DEEPSEEK_API_KEY=sk-live-9f3a2b7c11de",
    # a value this process really holds, for contrast
    "ran the smoke test with sk-probe-0123456789abcdef",
]

with tempfile.TemporaryDirectory() as tmp:
    repo = Path(tmp)
    (repo / "tools").mkdir()
    (repo / "tools" / "repo_activity.py").write_text("# stand-in\n", encoding="utf-8")
    common = dict(decision="REC-20260914-A", repo_root=repo,
                  runner=lambda argv, **kw: SimpleNamespace(returncode=0))

    for action in CANDIDATES:
        try:
            argv = R.activity("event", action, "why", "goal", **common)
            print("ACCEPTED ", repr(action))
            print("          -> argv carries:", argv[argv.index("--action") + 1])
        except LoopError as error:
            print("refused  ", repr(action), "->", error.code)
