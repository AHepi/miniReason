"""Build out/checkpoint-manifest.json and credential scan data.

Covers src/minireason/loop (recursive), tests/loop (recursive),
.gitattributes, pyproject.toml, and the *.md files at the sandbox root.
Never prints anything resembling a credential: only path and line number.
"""
import hashlib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAT_SK = re.compile(rb"sk-[0-9a-f]{32}")
PAT_DOT = re.compile(rb"[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}")
PAT_ENV = re.compile(rb"(DEEPSEEK_API_KEY|OLLAMA_API_KEY)=(.*)")


def collect_files():
    files = []
    for base in ("src/minireason/loop", "tests/loop"):
        for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, base)):
            dirnames.sort()
            for name in sorted(filenames):
                full = os.path.join(dirpath, name)
                files.append(os.path.relpath(full, ROOT))
    for name in (".gitattributes", "pyproject.toml"):
        files.append(name)
    for name in sorted(os.listdir(ROOT)):
        if name.endswith(".md") and os.path.isfile(os.path.join(ROOT, name)):
            files.append(name)
    return files


def main():
    files = collect_files()
    entries = []
    total_bytes = 0
    scan_hits = {"sk_pattern": [], "dot_pattern": []}
    env_assignments = []  # variable assigned a value (not allowed)
    env_name_only = 0     # lines that merely name the variable (allowed)

    for rel in files:
        with open(os.path.join(ROOT, rel), "rb") as fh:
            data = fh.read()
        total_bytes += len(data)
        lines = data.split(b"\n")
        # remove trailing empty element from final newline
        if lines and lines[-1] == b"":
            lines = lines[:-1]
        has_crlf = any(line.endswith(b"\r") for line in lines)
        entries.append({
            "path": rel,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "lines": len(lines),
            "crlf_line_endings": has_crlf,
        })
        for i, line in enumerate(lines, start=1):
            if PAT_SK.search(line):
                scan_hits["sk_pattern"].append({"path": rel, "line": i})
            if PAT_DOT.search(line):
                scan_hits["dot_pattern"].append({"path": rel, "line": i})
            m = PAT_ENV.search(line)
            if m:
                rest = m.group(2).strip()
                # allowed: nothing after '=', or a quote immediately
                # followed by the matching close quote (empty value)
                if rest == b"" or (
                    len(rest) >= 2
                    and rest[:1] in (b"'", b'"')
                    and rest[1:2] == rest[:1]
                ):
                    env_name_only += 1
                else:
                    env_assignments.append({"path": rel, "line": i})

    manifest = {
        "snapshot": "minireason.loop checkpoint",
        "file_count": len(entries),
        "total_bytes": total_bytes,
        "files": entries,
        "credential_scan": {
            "sk_pattern_hits": scan_hits["sk_pattern"],
            "dot_pattern_hits": scan_hits["dot_pattern"],
            "env_var_name_only_line_count": env_name_only,
            "env_var_value_assignment_hits": env_assignments,
        },
    }
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    with open(os.path.join(ROOT, "out", "checkpoint-manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)
        fh.write("\n")

    # Persist scan summary for the report builder (contains no secrets,
    # only paths and line numbers).
    with open(os.path.join(ROOT, "check", "_scan_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest["credential_scan"], fh, indent=2)
        fh.write("\n")

    print("files:", len(entries), "bytes:", total_bytes)
    print("sk hits:", len(scan_hits["sk_pattern"]),
          "dot hits:", len(scan_hits["dot_pattern"]),
          "env name-only:", env_name_only,
          "env assignments:", len(env_assignments))


if __name__ == "__main__":
    main()
