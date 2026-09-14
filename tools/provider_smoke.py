#!/usr/bin/env python3
"""One small live call per declared endpoint, under the repository's discipline.

What this does, and only this:

* reads credentials from an environment file into this process (never printing,
  echoing, logging or returning any part of a key);
* for every endpoint in ``endpoints.json`` whose key is present, sends exactly
  one small chat call with a new records directory given on the command line;
* for an Ollama model it sends that call to the OpenAI-compatible path first;
  only if that path fails does it send one call to the model's declared native
  ``/api/chat`` endpoint. That is a second declared path, recorded as its own
  call with its own settings — it is not a retry of the first, and neither path
  is ever attempted twice;
* asks each base URL for its model list once (``/models``), recorded the same way;
* prints a table of status, returned model, finish reason, latency, whether the
  answer parsed as JSON, whether native reasoning was present, and usage.

Concurrency is whatever the per-key semaphores allow: five requests per
credential, shared by every provider instance in this process.

    python3 tools/provider_smoke.py RECORDS_DIR --env-file /path/to/.env
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from minireason.provider_openai_compat import (  # noqa: E402
    ENDPOINTS, CallResult, Endpoint, OpenAICompatProvider, ProviderFailure,
    register_secret_envs, write_new,
)

PROMPT = 'Reply with a JSON object {"ok": true, "model": <your model name>}'
NATIVE_SUFFIX = ".native"


def load_env_file(path: Path) -> list[str]:
    """Put ``NAME=value`` lines into this process's environment.

    Returns the names it set, and **registers those names** with the transport
    so that every value this file loaded is inside the redaction, echo-check
    and refusal set - whatever the variable happens to be called. Without that
    a credential in a name outside the ``*_API_KEY`` convention (``HF_TOKEN``,
    ``OLLAMA_TOKEN``) would be live in the process and outside every check.
    Values are never returned, printed or logged.
    """

    names: list[str] = []
    if not path.exists():
        return names
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        name = name.strip()
        value = value.strip().strip('"').strip("'")
        if name and value:
            os.environ[name] = value
            names.append(name)
    register_secret_envs(names)
    return names


def supports_seed(endpoint: Endpoint) -> bool:
    """DeepSeek's chat API declares no seed; the repository claims no determinism there."""

    return endpoint.family != "deepseek"


def records_dir_for(root: Path, endpoint: Endpoint, label: str) -> Path:
    """One directory per (endpoint, label), never shared between two providers.

    Records are write-once and every provider instance restarts its call
    numbering at 0001, so two providers pointed at one directory collide on
    ``call-0001.request.json``. The ``--headroom`` probe builds a second
    provider for an endpoint already probed, so a shared directory made that
    flag crash - after the live calls had been spent - and lost the summary.
    """

    return root / endpoint.name.replace("/", "__") / label


def probe(root: Path, endpoint: Endpoint, *, max_tokens: int, label: str) -> dict:
    """Exactly one call. Never called twice for the same endpoint and label."""

    row = {"endpoint": endpoint.name, "label": label, "model": endpoint.model,
           "path": "native" if endpoint.native else "openai-compat",
           "family": endpoint.family, "max_tokens": max_tokens}
    try:
        client = OpenAICompatProvider(endpoint, records_dir_for(root, endpoint, label))
    except ProviderFailure as failure:
        row.update({"status": failure.code, "error": str(failure)})
        return row
    try:
        result: CallResult = client.complete(
            [{"role": "user", "content": PROMPT}],
            response_format={"type": "json_object"},
            max_tokens=max_tokens,
            seed=7 if supports_seed(endpoint) else None,
        )
        record = result.record
        content = result.content
        status = result.status
    except ProviderFailure as failure:
        record = failure.record or {}
        content = record.get("content", "")
        status = failure.code
        row["error"] = str(failure)[:400]
    row.update({
        "status": status,
        "returned_model": record.get("returned_model"),
        "finish_reason": record.get("finish_reason"),
        "elapsed_ms": record.get("elapsed_ms"),
        "usage": record.get("usage") or {},
        "reasoning_content_present": record.get("reasoning_content_present"),
        "reasoning_content_persisted": record.get("reasoning_content_persisted", False),
        "json_parsed": parses_as_json(content),
        "content_chars": len(content or ""),
        "request_sha256": record.get("request_sha256"),
        "provider_response_sha256": record.get("provider_response_sha256"),
    })
    return row


def parses_as_json(content: str | None) -> bool:
    if not content:
        return False
    try:
        return isinstance(json.loads(content), (dict, list))
    except Exception:
        return False


def list_models(root: Path, endpoint: Endpoint) -> dict:
    row = {"endpoint": endpoint.name, "base_url": endpoint.base_url, "operation": "models"}
    try:
        client = OpenAICompatProvider(endpoint, root / ("models__" + endpoint.base_url
                                                        .replace("https://", "").replace("/", "_")))
        # list_models' CREDENTIAL_ECHO attaches the model-list body; the copy
        # on the exception is redacted, but this tool never prints it anyway.
        record = client.list_models()
        body = record.get("models") or {}
        listed = body.get("data") if isinstance(body, dict) else None
        names = sorted(str(item.get("id")) for item in listed) if isinstance(listed, list) else []
        row.update({"status": record.get("status"), "elapsed_ms": record.get("elapsed_ms"),
                    "count": len(names), "models": names})
    except ProviderFailure as failure:
        record = failure.record or {}
        row.update({"status": failure.code, "elapsed_ms": record.get("elapsed_ms"),
                    "error": str(failure)[:400], "count": 0, "models": []})
    return row


def primary_endpoints(selected: list[str] | None) -> list[Endpoint]:
    """The endpoints this run probes first.

    With no selection that is every non-native entry, so an Ollama model is
    tried on the OpenAI-compatible path first. A selection is taken literally,
    native entries included, so a run can address the native path directly.
    """

    if selected:
        unknown = [name for name in selected if name not in ENDPOINTS]
        if unknown:
            raise SystemExit(f"Unknown endpoint name(s): {sorted(unknown)}")
        return [ENDPOINTS[name] for name in selected]
    return [ENDPOINTS[name] for name in ENDPOINTS if not name.endswith(NATIVE_SUFFIX)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("records_dir", type=Path,
                        help="a NEW directory for this run's call records")
    parser.add_argument("--env-file", type=Path, default=Path(".env"),
                        help="NAME=value file read into this process's environment")
    parser.add_argument("--max-tokens", type=int, default=64)
    parser.add_argument("--headroom", type=int, default=0, metavar="N",
                        help="after the run, send ONE further call at ceiling N to each endpoint "
                             "that ended INCOMPLETE_GENERATION. A separately declared probe with "
                             "different settings, recorded as its own call; not a retry.")
    parser.add_argument("--only", nargs="*", default=None, help="endpoint names to probe")
    parser.add_argument("--workers", type=int, default=10,
                        help="thread count; the per-key semaphores still cap each key at 5")
    args = parser.parse_args(argv)

    root: Path = args.records_dir
    if root.exists() and any(root.iterdir()):
        parser.error(f"{root} already holds records; give a new directory (records are write-once)")
    root.mkdir(parents=True, exist_ok=True)

    set_names = load_env_file(args.env_file)
    endpoints = primary_endpoints(args.only)
    available = [e for e in endpoints if os.environ.get(e.key_env)]
    skipped = [e for e in endpoints if not os.environ.get(e.key_env)]

    print(f"env file      : {args.env_file} ({len(set_names)} name(s) loaded)")
    for key_env in sorted({e.key_env for e in endpoints}):
        print(f"credential    : {key_env} {'present' if os.environ.get(key_env) else 'ABSENT'}")
    print(f"records       : {root}")
    print(f"endpoints     : {len(available)} probed, {len(skipped)} skipped for a missing key")
    print()

    rows: list[dict] = []
    model_rows: list[dict] = []

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        model_futures = []
        seen_bases: set[tuple[str, str]] = set()
        for endpoint in available:
            # A native base URL has no /models surface: https://ollama.com/models
            # is a redirect, and this transport refuses redirects. The model list
            # belongs to the OpenAI-compatible base.
            if endpoint.native:
                continue
            marker = (endpoint.key_env, endpoint.base_url)
            if marker in seen_bases:
                continue
            seen_bases.add(marker)
            model_futures.append(pool.submit(list_models, root, endpoint))
        probe_futures = [pool.submit(probe, root, endpoint, max_tokens=args.max_tokens,
                                     label="compat") for endpoint in available]
        model_rows = [future.result() for future in model_futures]
        rows = [future.result() for future in probe_futures]

    # The declared fallback: only for an Ollama model whose OpenAI-compatible
    # path did not come back COMPLETE, and only once.
    fallback = [ENDPOINTS[row["endpoint"] + NATIVE_SUFFIX] for row in rows
                if row["status"] != "COMPLETE" and row["endpoint"] + NATIVE_SUFFIX in ENDPOINTS]
    if fallback:
        print(f"-- OpenAI-compatible path failed for {len(fallback)} Ollama model(s); "
              f"sending one call each to the declared native /api/chat path --\n")
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            rows += [future.result() for future in
                     [pool.submit(probe, root, endpoint, max_tokens=args.max_tokens, label="native")
                      for endpoint in fallback]]

    if args.headroom:
        truncated = [row for row in rows if row["status"] == "INCOMPLETE_GENERATION"]
        if truncated:
            print(f"-- {len(truncated)} endpoint(s) ran out of the {args.max_tokens}-token ceiling; "
                  f"one further declared probe at {args.headroom} tokens (not a retry) --\n")
            with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
                rows += [future.result() for future in
                         [pool.submit(probe, root, ENDPOINTS[row["endpoint"]],
                                      max_tokens=args.headroom, label=f"headroom-{args.headroom}")
                          for row in truncated]]

    print_models(model_rows)
    print_table(rows)
    summary = {
        "schema_version": "minireason.smoke.v1",
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "prompt": PROMPT,
        "max_tokens": args.max_tokens,
        "headroom": args.headroom or None,
        "key_envs": sorted({e.key_env for e in endpoints}),
        "skipped_for_missing_key": [e.name for e in skipped],
        "model_lists": model_rows,
        "calls": rows,
    }
    write_new(root / "smoke-summary.json", summary)
    print(f"\nsummary: {root / 'smoke-summary.json'}")
    return 0 if any(row["status"] == "COMPLETE" for row in rows) else 1


def print_models(rows: list[dict]) -> None:
    for row in rows:
        print(f"models {row['base_url']}/models -> {row['status']} "
              f"({row.get('elapsed_ms')} ms, {row.get('count')} listed)")
        if row.get("models"):
            print("   " + ", ".join(row["models"]))
        elif row.get("error"):
            print("   " + row["error"].splitlines()[0][:200])
    print()


def print_table(rows: list[dict]) -> None:
    header = ("endpoint", "path", "status", "returned_model", "finish", "ms", "json", "reas",
              "prompt", "compl")
    table = [header]
    for row in sorted(rows, key=lambda item: (item["endpoint"], item["label"])):
        usage = row.get("usage") or {}
        table.append((
            row["endpoint"] + ("" if row["label"] in {"compat", "native"} else f" [{row['label']}]"),
            row["path"],
            str(row["status"]),
            str(row.get("returned_model") or "-"),
            str(row.get("finish_reason") or "-"),
            str(row.get("elapsed_ms") if row.get("elapsed_ms") is not None else "-"),
            {True: "yes", False: "no", None: "-"}[row.get("json_parsed")],
            {True: "yes", False: "no", None: "-"}[row.get("reasoning_content_present")],
            str(usage.get("prompt_tokens", "-")),
            str(usage.get("completion_tokens", "-")),
        ))
    widths = [max(len(str(cell)) for cell in column) for column in zip(*table)]
    for index, line in enumerate(table):
        print("  ".join(str(cell).ljust(width) for cell, width in zip(line, widths)).rstrip())
        if index == 0:
            print("  ".join("-" * width for width in widths))
    for row in sorted(rows, key=lambda item: item["endpoint"]):
        if row["status"] != "COMPLETE" and row.get("error"):
            print(f"\n{row['endpoint']} [{row['label']}] {row['status']}: "
                  f"{row['error'].splitlines()[0][:300]}")


if __name__ == "__main__":
    raise SystemExit(main())
