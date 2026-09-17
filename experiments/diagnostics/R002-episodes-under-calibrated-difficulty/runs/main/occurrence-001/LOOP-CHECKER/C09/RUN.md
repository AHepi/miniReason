# R002 run

Run: `20260917T023302Z-r002-0eff8c`. Condition: `LOOP-CHECKER`.

Calls/attempts: 3/3. Strict policy: one attempt, zero repairs/fallbacks/retries.

Ceilings: native 32768; off 16384; prompt 32768; wall 300 seconds per call; at most 14 loop calls.

Completed cycles: 0. Closing return: not-run.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 0.

Episode records/supplements: 0.

Reported usage (known portions only): `{"completion_tokens": 43628, "prompt_tokens": 5526, "total_tokens": 49154, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

Stop reason: `CEILING_HIT`. Provider finish_reason=length

Schema, counter and episode assembly success is custody evidence, not a score or correctness verdict.

## Actual request controls and reported usage

```json
[
  {
    "call": "c0001-signal-a",
    "completion_tokens": 16384,
    "endpoint": {
      "base_url": "https://ollama.com",
      "chat_path": "/api/chat",
      "family": "ollama-cloud/qwen",
      "key_env": "OLLAMA_API_KEY",
      "max_concurrency": 5,
      "model": "qwen3.5:397b",
      "name": "ollama/qwen3.5-397b.native",
      "native": true,
      "timeout_seconds": 300
    },
    "reasoning_effort": "medium",
    "request": {
      "path": "calls/c0001-signal-a/a00/request.json",
      "sha256": "a8ffa920fecabc667cd034be9fc9ab2e618cf0f7bf427de68f62b3947d0a4748"
    },
    "seat": {
      "endpoint": "ollama/qwen3.5-397b.native",
      "reasoning_effort": "medium",
      "role": "tested_critic",
      "schema": "../contracts/tested-objection.schema.json",
      "thinking": "off"
    },
    "thinking": "off",
    "usage": {
      "completion_tokens": 283,
      "prompt_tokens": 2335,
      "total_tokens": 2618
    },
    "wall_seconds": 300
  },
  {
    "call": "c0001-signal-b",
    "completion_tokens": 16384,
    "endpoint": {
      "base_url": "https://ollama.com",
      "chat_path": "/api/chat",
      "family": "ollama-cloud/glm",
      "key_env": "OLLAMA_API_KEY",
      "max_concurrency": 5,
      "model": "glm-5.3",
      "name": "ollama/glm-5.3.native",
      "native": true,
      "timeout_seconds": 300
    },
    "reasoning_effort": "medium",
    "request": {
      "path": "calls/c0001-signal-b/a00/request.json",
      "sha256": "a61f74d9758598476a90957e3258f49d3f7e39e356e4ea5a04e05044a37a5dfe"
    },
    "seat": {
      "endpoint": "ollama/glm-5.3.native",
      "reasoning_effort": "medium",
      "role": "tested_critic",
      "schema": "../contracts/tested-objection.schema.json",
      "thinking": "off"
    },
    "thinking": "off",
    "usage": {
      "completion_tokens": 16384,
      "prompt_tokens": 2139,
      "total_tokens": 18523
    },
    "wall_seconds": 300
  },
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
      "sha256": "39ab0c35df3db1946006229e5fddab4a2979282c316c2830cb7b7b3c8982ca6e"
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
      "completion_tokens": 26961,
      "completion_tokens_details": {
        "reasoning_tokens": 26286
      },
      "prompt_cache_hit_tokens": 896,
      "prompt_cache_miss_tokens": 156,
      "prompt_tokens": 1052,
      "prompt_tokens_details": {
        "cached_tokens": 896
      },
      "total_tokens": 28013
    },
    "wall_seconds": 300
  }
]
```
