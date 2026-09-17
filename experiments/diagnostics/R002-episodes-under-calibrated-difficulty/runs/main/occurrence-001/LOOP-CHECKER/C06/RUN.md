# R002 run

Run: `20260917T021902Z-r002-1e9df1`. Condition: `LOOP-CHECKER`.

Calls/attempts: 1/1. Strict policy: one attempt, zero repairs/fallbacks/retries.

Ceilings: native 32768; off 16384; prompt 32768; wall 300 seconds per call; at most 14 loop calls.

Completed cycles: 0. Closing return: not-run.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 0.

Episode records/supplements: 0.

Reported usage (known portions only): `{"completion_tokens": 32768, "prompt_tokens": 1045, "total_tokens": 33813, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

Stop reason: `CEILING_HIT`. Provider finish_reason=length

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
      "sha256": "237e6615ab51dfa25da16be48197f2ce73ab91a3088de3c0529f46d3a5d45ce5"
    },
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "conjecture",
      "schema": "../contracts/answer.schema.json",
      "thinking": "native"
    },
    "thinking": "native",
    "usage": {
      "completion_tokens": 32768,
      "completion_tokens_details": {
        "reasoning_tokens": 32768
      },
      "prompt_cache_hit_tokens": 896,
      "prompt_cache_miss_tokens": 149,
      "prompt_tokens": 1045,
      "prompt_tokens_details": {
        "cached_tokens": 896
      },
      "total_tokens": 33813
    },
    "wall_seconds": 300
  }
]
```
