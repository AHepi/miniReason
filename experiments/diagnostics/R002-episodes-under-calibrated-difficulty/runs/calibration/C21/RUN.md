# R002 run

Run: `20260916T234656Z-r002-526496`. Condition: `CAL-NATIVE`.

Calls/attempts: 1/1. Strict policy: one attempt, zero repairs/fallbacks/retries.

Ceilings: native 32768; off 16384; prompt 32768; wall 300 seconds per call; at most 14 loop calls.

Completed cycles: 0. Closing return: not-run.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 0.

Episode records/supplements: 0.

Reported usage (known portions only): `{"completion_tokens": 4373, "prompt_tokens": 1015, "total_tokens": 5388, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

Stop reason: `complete`. 

Schema, counter and episode assembly success is custody evidence, not a score or correctness verdict.

## Actual request controls and reported usage

```json
[
  {
    "call": "initial",
    "completion_tokens": 32768,
    "endpoint": {
      "base_url": "https://api.deepseek.com/v1",
      "chat_path": "/chat/completions",
      "family": "deepseek",
      "key_env": "DEEPSEEK_API_KEY",
      "max_concurrency": 5,
      "model": "deepseek-flash",
      "name": "deepseek-flash",
      "native": false,
      "timeout_seconds": 300
    },
    "reasoning_effort": "medium",
    "request": {
      "path": "calls/initial/a00/request.json",
      "sha256": "434182a0c130720b1d990ef47a468d931f70e97438936f20389c0c59e3848d52"
    },
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "answer",
      "thinking": "native"
    },
    "thinking": "native",
    "usage": {
      "completion_tokens": 4373,
      "completion_tokens_details": {
        "reasoning_tokens": 3589
      },
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 1015,
      "prompt_tokens": 1015,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 5388
    },
    "wall_seconds": 300
  }
]
```
