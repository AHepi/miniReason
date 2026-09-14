"""What the module actually emits, what it strips, and what importing it costs.

Three separate questions:

  A. deviation 8 / N3 -- does importing ``publish`` load the endpoint registry?
  B. the ALLOWED_SUBCOMMANDS docstring -- "the guard now refuses everything this
     module does not itself emit" and "the list cannot be wider than the
     module's own need". Every argv the three entry points emit is captured.
  C. ``LocalGit.environment()`` -- "every credential removed", against the
     transport's own declared set.

Run: python3 probe/p08_argv_env_and_imports.py
"""
from __future__ import annotations

import os
import subprocess
import sys

import _lab

_lab.banner("A. import cost")
out = subprocess.run(
    [sys.executable, "-c",
     "import sys; sys.path.insert(0, 'src');"
     " import minireason.loop.publish as p;"
     " print('provider loaded at import:',"
     "       'minireason.provider_openai_compat' in sys.modules);"
     " p.LocalGit.environment.__doc__;"],
    cwd=str(_lab.ROOT), capture_output=True, text=True, env=dict(os.environ))
print(out.stdout.strip() or out.stderr.strip())

_lab.banner("B. every argv the three entry points emit")
from minireason.loop import publish                                    # noqa: E402

emitted = []


class Recording(publish.LocalGit):
    def _invoke(self, tokens):
        emitted.append(tuple(tokens))
        return super()._invoke(tokens)


lab = _lab.Lab("argv")
try:
    lab.write("docs/note.md", "published bytes\n")
    git = Recording(lab.repo, env=dict(_lab.GIT_ENV))
    result = publish.publish(lab.repo, ["docs/note.md"], "publish", "origin/main", git=git)
    publish.verify_published(lab.repo, ["docs/note.md"], result.remote_commit,
                             "origin/main", git=git)
    publish.check_published(lab.repo, "docs/note.md", "origin/main", git=git)
    publish.check_published(lab.repo, result.remote_commit, "origin/main", git=git)
    ancestor = _lab.git(lab.repo, "rev-parse", result.remote_commit + "^"
                        ).stdout.decode().strip()
    publish.check_published(lab.repo, ancestor, "origin/main", git=git)   # merge-base path
    publish.upstream_ref(lab.repo, git=git)
finally:
    lab.close()

used = sorted({publish._subcommand(tokens) for tokens in emitted})
print("subcommands emitted        :", used)
print("ALLOWED_SUBCOMMANDS        :", sorted(publish.ALLOWED_SUBCOMMANDS))
print("allowed but never emitted  :", sorted(publish.ALLOWED_SUBCOMMANDS - set(used)))
print("emitted but not allowed    :", sorted(set(used) - publish.ALLOWED_SUBCOMMANDS))
print("argvs emitted (count)     :", len(emitted))
print("argvs, in order:")
for tokens in emitted:
    print("   git", " ".join(tokens))

_lab.banner("C. LocalGit.environment() versus the transport's declared set")
from minireason import provider_openai_compat as transport             # noqa: E402

os.environ["DEEPSEEK_API_KEY"] = "PROBE-FAKE-DEEPSEEK-0123456789"      # synthetic
os.environ["OLLAMA_API_KEY"] = "PROBE-FAKE-OLLAMA-0123456789"          # synthetic
lab = _lab.Lab("env")
try:
    git = publish.LocalGit(lab.repo)
    child = git.environment()
    print("transport declares          :", transport._secret_env_names())
    print("publish strips              :", publish._credential_env_names())
    print("names left in the child env :",
          [name for name in transport._secret_env_names() if name in child])

    # The two sets agree only because every _ALWAYS_SECRET_ENVS member happens to
    # be an endpoint key_env today. Drop one endpoint family and they diverge.
    kept = {name: endpoint for name, endpoint in transport.ENDPOINTS.items()
            if endpoint.key_env != "OLLAMA_API_KEY"}
    saved = dict(transport.ENDPOINTS)
    transport.ENDPOINTS.clear()
    transport.ENDPOINTS.update(kept)
    transport._REGISTRY.clear()
    transport._REGISTRY.update(kept)
    try:
        print()
        print("with no OLLAMA endpoint in the registry:")
        print("  transport declares        :", transport._secret_env_names())
        print("  publish strips            :", publish._credential_env_names())
        leaked = [name for name in transport._secret_env_names()
                  if name in publish.LocalGit(lab.repo).environment()]
        print("  still in the child env    :", leaked)
        print("  and the scanner still flags it:",
              publish._redact_with_names("x " + os.environ["OLLAMA_API_KEY"] + " y")[1])
    finally:
        transport.ENDPOINTS.clear()
        transport.ENDPOINTS.update(saved)
        transport._REGISTRY.clear()
        transport._REGISTRY.update(saved)
finally:
    lab.close()
