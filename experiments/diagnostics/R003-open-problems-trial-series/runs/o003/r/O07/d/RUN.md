# R003 run

Run: `20260917T092936Z-r002-f7eb61`. Condition: `LOOP-DECOMPOSED`.

Calls/attempts: 4/4. Schema repairs: 0. Strict policy: one initial attempt plus at most one schema repair per logical call; zero fallbacks/transport retries; CEILING_HIT receives no repair.

Ceilings: native 32768; STEP/use 16384; critics 32768; prompt 32768; wall 300 seconds per attempt; at most 14 logical calls and 28 attempts. Base/max completion allowance: 376832/753664.

Reached by repair: `[]`. Reached without repair: `["c0001-critic", "c0001-return", "c0001-use", "initial"]`. Repair attempted but not completed: `[]`.

Completed cycles: 0. Closing return: not-run.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 0.

Episode records/supplements: 0.

Reported usage (known portions only): `{"completion_tokens": 12621, "prompt_tokens": 10071, "total_tokens": 22692, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

Stop reason: `step_unresolved`. Use check inconclusive with the returned step result

Schema, counter and episode assembly success is custody evidence, not a score or correctness verdict.

## Actual request controls and reported usage

```json
[
  {
    "attempt": "a00",
    "call": "c0001-critic",
    "completion_tokens": 32768,
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
      "path": "calls/c0001-critic/a00/request.json",
      "sha256": "78c99abec5e9566eeb734123c9d2b0456e64fde8f2d7807a24c75bb5e30640ef"
    },
    "response": {
      "path": "calls/c0001-critic/a00/response.json",
      "sha256": "1afb219572aba00251b6a50142f524f6ca71ff1755fe992b8b42479fde65123c"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "ollama/qwen3.5-397b.native",
      "reasoning_effort": "medium",
      "role": "decomposed_critic",
      "schema": "../contracts/tested-objection-r3-a2.schema.json",
      "thinking": "off"
    },
    "status": "COMPLETE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 232,
      "prompt_tokens": 2882,
      "total_tokens": 3114
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0001-return",
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
      "path": "calls/c0001-return/a00/request.json",
      "sha256": "298c2b2b936cde6586406f32e68fc964b35f83e57beb5227bea3e11a56e0a421"
    },
    "response": {
      "path": "calls/c0001-return/a00/response.json",
      "sha256": "6657f3d19a93d47134ea48580ad65a7757e97f6dafd0f924853c521822c84f26"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "decomposed_return",
      "schema": "../contracts/decomposed-return-r3-a2.schema.json",
      "thinking": "native"
    },
    "status": "COMPLETE",
    "thinking": "native",
    "usage": {
      "completion_tokens": 4508,
      "completion_tokens_details": {
        "reasoning_tokens": 3700
      },
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 2489,
      "prompt_tokens": 2873,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 7381
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0001-use",
    "completion_tokens": 16384,
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
      "path": "calls/c0001-use/a00/request.json",
      "sha256": "2cc47736dd2cdf75318e5ae42ff99494c2b27408342f783015232a8289f0b3ec"
    },
    "response": {
      "path": "calls/c0001-use/a00/response.json",
      "sha256": "e62f52074c332f6a2f8c2821d5bdada91013597bb03e64a0b9066895e963eb98"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "decomposed_use",
      "schema": "../../R002-episodes-under-calibrated-difficulty/contracts/decomposed-use.schema.json",
      "thinking": "off"
    },
    "status": "COMPLETE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 273,
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 1982,
      "prompt_tokens": 2238,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 2511
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
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
      "sha256": "ebc77516b366e7c8198a04cdb10bb8321a2ec0c77762819be138dfc5ddd6e7c1"
    },
    "response": {
      "path": "calls/initial/a00/response.json",
      "sha256": "d047156ee861eb1783c425d9d67bc2505ea69bb5df68a5e805a3042775eb6bf0"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "initial_decompose",
      "schema": "../contracts/initial-decompose-r3-a2.schema.json",
      "thinking": "native"
    },
    "status": "COMPLETE",
    "thinking": "native",
    "usage": {
      "completion_tokens": 7608,
      "completion_tokens_details": {
        "reasoning_tokens": 6895
      },
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 1694,
      "prompt_tokens": 2078,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 9686
    },
    "wall_seconds": 300
  }
]
```
