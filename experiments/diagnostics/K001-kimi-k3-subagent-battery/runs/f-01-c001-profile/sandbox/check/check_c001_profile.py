#!/usr/bin/env python3
"""Independent verification of out/c001-profile.md.

Recomputes the C001 occurrence-01 aggregates with its own aggregation pass
(no code shared with check/c001_profile.py) and asserts that the written
profile contains the corresponding numbers. Run:

    python3 check/check_c001_profile.py
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESP_DIR = ROOT / "experiments" / "diagnostics" / "C001-contrast-triple" / "occurrence-01" / "responses"
ENDPOINTS = ROOT / "src" / "minireason" / "data" / "endpoints.json"
PROFILE = ROOT / "out" / "c001-profile.md"


def main():
    fam_by_slug = {e["name"].replace("/", "-"): e["family"]
                   for e in json.loads(ENDPOINTS.read_text(encoding="utf-8"))["endpoints"]}

    code_by_field = defaultdict(Counter)
    both = only_ft = only_vft = neither = 0
    fam_any = Counter()
    ep_status = defaultdict(Counter)
    coded_rows = []
    n = 0

    for p in sorted(RESP_DIR.glob("*/*/*/rep*.json")):  # slug/arm/case/repN.json
        r = json.loads(p.read_text(encoding="utf-8"))
        n += 1
        slug = r["coordinate"]["endpoint_slug"]
        ft, vft = r.get("failure_type"), r.get("validation_failure_type")
        if ft:
            code_by_field["failure_type"][ft] += 1
        if vft:
            code_by_field["validation_failure_type"][vft] += 1
        if ft and vft:
            both += 1
        elif ft:
            only_ft += 1
        elif vft:
            only_vft += 1
        else:
            neither += 1
        if ft or vft:
            fam_any[fam_by_slug[slug]] += 1
            usage = r.get("usage") or {}
            coded_rows.append((slug, r["coordinate"]["arm"], r["coordinate"]["case"],
                               r["coordinate"]["replicate"], r.get("finish_reason"),
                               usage.get("completion_tokens") if isinstance(usage, dict) else None))
        ep_status[slug][r["status"]] += 1

    assert n == 240, n
    assert dict(code_by_field["failure_type"]) == {"INCOMPLETE_GENERATION": 20}
    assert dict(code_by_field["validation_failure_type"]) == {"NO_PUBLIC_CONTENT": 11}
    assert (both, only_ft, only_vft, neither) == (11, 9, 0, 220)
    assert dict(fam_any) == {"deepseek": 19, "ollama-cloud/glm": 1}
    assert ep_status["deepseek-flash"] == Counter({"COMPLETE": 21, "PARTIAL": 8, "FAILED": 11})
    assert ep_status["ollama-glm-5.3"] == Counter({"COMPLETE": 39, "PARTIAL": 1})
    for slug in ("ollama-gemma4-31b", "ollama-gpt-oss-120b", "ollama-kimi-k3", "ollama-qwen3.5-397b"):
        assert ep_status[slug] == Counter({"COMPLETE": 40}), (slug, ep_status[slug])
    assert len(coded_rows) == 20
    # Every coded receipt that reports finish_reason=length sits at a recorded stopping point.
    assert sorted(x[5] for x in coded_rows if x[4] == "length") == [8192] * 8 + [32768]
    # All coded receipts are in arm fcl; none in prose.
    assert {x[1] for x in coded_rows} == {"fcl"}

    text = PROFILE.read_text(encoding="utf-8")
    for needle in (
        "| `INCOMPLETE_GENERATION` | `failure_type` (provider-side) | 20 |",
        "| `NO_PUBLIC_CONTENT` | `validation_failure_type` (validation-side) | 11 |",
        "| both `failure_type` and `validation_failure_type` | 11 |",
        "| only `failure_type` | 9 |",
        "| only `validation_failure_type` | 0 |",
        "| neither field | 220 |",
        "| any code (union) | 20 |",
        "| `deepseek` | 40 | 19 | 11 | 11 | 19 |",
        "| `ollama-cloud/glm` | 40 | 1 | 0 | 0 | 1 |",
        "| `deepseek-flash` | `deepseek` | 21 | 8 | 11 | 40 |",
        "| `ollama-glm-5.3` | `ollama-cloud/glm` | 39 | 1 | 0 | 40 |",
        "Counts below are information, never a warrant.",
        "What the records do not settle",
    ):
        assert needle in text, needle
    # One spot-checked coded-receipt row, verbatim.
    assert ("| `ollama-glm-5.3` | fcl | control | 2 | `failure_type=INCOMPLETE_GENERATION` "
            "| length | 32768 |") in text

    print("check_c001_profile: all assertions passed")
    print(f"  recomputed: receipts={n}, both={both}, only_ft={only_ft}, only_vft={only_vft}, neither={neither}")
    print(f"  coded rows verified independently: {len(coded_rows)}")


if __name__ == "__main__":
    main()
