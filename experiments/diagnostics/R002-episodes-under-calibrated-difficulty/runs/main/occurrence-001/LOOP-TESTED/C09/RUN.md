# R002 run

Run: `20260917T022807Z-r002-5e785d`. Condition: `LOOP-TESTED`.

Calls/attempts: 3/3. Strict policy: one attempt, zero repairs/fallbacks/retries.

Ceilings: native 32768; off 16384; prompt 32768; wall 300 seconds per call; at most 14 loop calls.

Completed cycles: 0. Closing return: not-run.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 0.

Episode records/supplements: 0.

Reported usage (known portions only): `{"completion_tokens": 47086, "prompt_tokens": 5850, "total_tokens": 52936, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

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
      "sha256": "6a1aa37db460a1b1172021b439d69aa40040ebc146adc8536047d21b4add7c6c"
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
      "completion_tokens": 292,
      "prompt_tokens": 2501,
      "total_tokens": 2793
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
      "sha256": "ede522517cdcbf80fa842ba7755b9ea09c5c110a81c0673b05d18a5e5489a658"
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
      "prompt_tokens": 2297,
      "total_tokens": 18681
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
      "sha256": "37aff9b2c0240de1e1f5215150ac4ba442a6f3c77391554298547dc76ea8e6a5"
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
      "completion_tokens": 30410,
      "completion_tokens_details": {
        "reasoning_tokens": 29573
      },
      "prompt_cache_hit_tokens": 896,
      "prompt_cache_miss_tokens": 156,
      "prompt_tokens": 1052,
      "prompt_tokens_details": {
        "cached_tokens": 896
      },
      "total_tokens": 31462
    },
    "wall_seconds": 300
  }
]
```
