# UC1 current offline validation

UTC 2026-09-17T11:26:11.190829+00:00. Scripted interface and custody evidence only; no provider/model or Blender call. The fixture deliberately stops after two passes to exercise CONTINUE then STOP. **The live task has no pass-count cap.**

Exact root validation command:

```powershell
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -B -X utf8 work\w37\validate_tasks_pa1.py
```

The helper uses PYTHONPATH=src;tests, PYTHONUTF8=1, PYTHONIOENCODING=utf-8, TMP=C:\tw37 and bytecode suppression. Each task gets a fresh Python child running the actual Pilot in offline mode. Callable fixtures supply the verification hash created at runtime; the stock CLI static `--scripted` JSON list cannot precompute that reference.

Pasted compact results:

```json
{
  "label": "UC1",
  "status": "PASS",
  "mode": "offline callable scripted fixture",
  "provider_calls": 0,
  "selected_route": "direct_answer",
  "logical_calls": 8,
  "physical_attempts": 8,
  "repairs": 0,
  "closed_passes": 2,
  "continuation_decisions": [
    "continue",
    "stop"
  ],
  "requested_completion_ceiling_sum": 28672,
  "actual_usage": {
    "cached_prompt_tokens": 0,
    "completion_tokens": 0,
    "prompt_tokens": 0,
    "reasoning_tokens": 0,
    "total_tokens": 0,
    "uncached_prompt_tokens": 0
  },
  "source_hashes_equal": true,
  "task_sha256": "5e003ff28b56137e0faa6430d5b095d34d0df75459c9dd5d396fc41c5940feca",
  "result_sha256": "8a947b6d3ea409ce6022dc42590b078764a10baddb0360c6617cc586ecc54eee",
  "output_directory": "C:\\tw37\\UC1-pa1-20260917T112228456629Z-568948"
}
```

[Exact argv/stdout/stderr transcript](../../../../work/w37/validate-tasks-pa1-20260917T112228456629Z.log); [full source pins and pass records](../../../../work/w37/validate-tasks-pa1-20260917T112228456629Z.json). Immutable call evidence remains at the output directory above.

Actual post-verification decisions:

```json
[
  {
    "decision": "continue",
    "reason": "sha256:9888aae88cf44f7b434bcf77753a75f53f29f503492318aa945fb92a47330991 completed the first fixture verification; continue once with an explicitly changed premise to exercise P-A1 continuation custody.",
    "stop_rule": "Stop after the changed second offline fixture pass verifies; this is interface validation only.",
    "what_changes_next": "Reuse the selected template with one additional fixture-only premise, preserving all sealed authority fields."
  },
  {
    "decision": "stop",
    "reason": "sha256:bc9d5535eb96cdcc4ce23b2a6f38f5856d75106cf008fdb5cf0b1415fe691bc9 completed the changed second fixture verification; stop under the declared fixture-only rule.",
    "stop_rule": "Stop after the changed second offline fixture pass verifies; this is interface validation only.",
    "what_changes_next": ""
  }
]
```

UC2/UC3 fixture artifacts are field-complete placeholders, UC4 critic support is scripted, and UC1 uses its supplied positive spec/script fixture. Scripted zero usage is not live-token usage. COMPLETE is not semantic success, camera-framing proof or an FW5 verdict. Live found/missed/invented fields remain NOT RUN.
