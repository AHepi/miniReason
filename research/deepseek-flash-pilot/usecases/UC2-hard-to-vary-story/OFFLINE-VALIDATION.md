# UC2 current offline validation

UTC 2026-09-17T11:26:11.190829+00:00. Scripted interface and custody evidence only; no provider/model or Blender call. The fixture deliberately stops after two passes to exercise CONTINUE then STOP. **The live task has no pass-count cap.**

Exact root validation command:

```powershell
& 'C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe' -B -X utf8 work\w37\validate_tasks_pa1.py
```

The helper uses PYTHONPATH=src;tests, PYTHONUTF8=1, PYTHONIOENCODING=utf-8, TMP=C:\tw37 and bytecode suppression. Each task gets a fresh Python child running the actual Pilot in offline mode. Callable fixtures supply the verification hash created at runtime; the stock CLI static `--scripted` JSON list cannot precompute that reference.

Pasted compact results:

```json
{
  "label": "UC2",
  "status": "PASS",
  "mode": "offline callable scripted fixture",
  "provider_calls": 0,
  "selected_route": "evidence_read",
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
  "task_sha256": "094a7d21f267a521b5fe20676a2ade1279e4aeabc79967f34f01b3c2d853f3ed",
  "result_sha256": "ec382294ed9036188ebd53fbdea7614783542889ab4671d27ad19eed1b495a07",
  "output_directory": "C:\\tw37\\UC2-pa1-20260917T112228456629Z-568948"
}
```

[Exact argv/stdout/stderr transcript](../../../../work/w37/validate-tasks-pa1-20260917T112228456629Z.log); [full source pins and pass records](../../../../work/w37/validate-tasks-pa1-20260917T112228456629Z.json). Immutable call evidence remains at the output directory above.

Actual post-verification decisions:

```json
[
  {
    "decision": "continue",
    "reason": "sha256:2cdb65fff0fdf00b6d2beb7f4b7732c5aae76f124d76c48b8de50703252c7767 completed the first fixture verification; continue once with an explicitly changed premise to exercise P-A1 continuation custody.",
    "stop_rule": "Stop after the changed second offline fixture pass verifies; this is interface validation only.",
    "what_changes_next": "Reuse the selected template with one additional fixture-only premise, preserving all sealed authority fields."
  },
  {
    "decision": "stop",
    "reason": "sha256:7d08488aa459504b15ae49d75d89c1c39fe4e2288f184d0e8d59999b4e629db6 completed the changed second fixture verification; stop under the declared fixture-only rule.",
    "stop_rule": "Stop after the changed second offline fixture pass verifies; this is interface validation only.",
    "what_changes_next": ""
  }
]
```

UC2/UC3 fixture artifacts are field-complete placeholders, UC4 critic support is scripted, and UC1 uses its supplied positive spec/script fixture. Scripted zero usage is not live-token usage. COMPLETE is not semantic success, camera-framing proof or an FW5 verdict. Live found/missed/invented fields remain NOT RUN.
