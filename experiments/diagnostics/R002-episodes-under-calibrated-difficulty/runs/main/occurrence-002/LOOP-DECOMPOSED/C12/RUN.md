# R002 run

Run: `20260917T041352Z-r002-71c1af`. Condition: `LOOP-DECOMPOSED`.

Calls/attempts: 5/6. Schema repairs: 1. Strict policy: one initial attempt plus at most one schema repair per logical call; zero fallbacks/transport retries; CEILING_HIT receives no repair.

Ceilings: native 32768; STEP/use 16384; critics 32768; prompt 32768; wall 300 seconds per attempt; at most 13 logical calls and 26 attempts. Base/max completion allowance: 344064/688128.

Reached by repair: `["c0002-step"]`. Reached without repair: `["c0001-critic", "c0001-return", "c0001-use", "initial"]`. Repair attempted but not completed: `[]`.

Completed cycles: 1. Closing return: not-run.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 1.

Episode records/supplements: 0.

Reported usage (known portions only): `{"completion_tokens": 4941, "prompt_tokens": 10689, "total_tokens": 15630, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

Stop reason: `step_unresolved`. The full exact round-4, round-5, and round-6 state distributions are not supplied by any accepted prior step, and completing the six-round recursion exactly without code or retrieval exceeds the derivable content of the accepted prior steps.

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
      "sha256": "cbb594ca831093e7706cecd4d51565491919be3550bc901cdb53c9a735759c22"
    },
    "response": {
      "path": "calls/c0001-critic/a00/response.json",
      "sha256": "096cf848d085b01efda684c1d3965209a127c9cca6d8d1ef8484ee526866f7c5"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "ollama/qwen3.5-397b.native",
      "reasoning_effort": "medium",
      "role": "decomposed_critic",
      "schema": "../contracts/tested-objection.schema.json",
      "thinking": "off"
    },
    "status": "COMPLETE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 427,
      "prompt_tokens": 1911,
      "total_tokens": 2338
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
      "sha256": "b732b08a7e4f394ede98d8817e7ff016973459a50ce8ada1df1df357586d930e"
    },
    "response": {
      "path": "calls/c0001-return/a00/response.json",
      "sha256": "3a0648f888291b1cdd9490c5daed7f6a77527bc81f6b71afd6084d4cd9395797"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "decomposed_return",
      "schema": "../contracts/decomposed-return.schema.json",
      "thinking": "native"
    },
    "status": "COMPLETE",
    "thinking": "native",
    "usage": {
      "completion_tokens": 862,
      "completion_tokens_details": {
        "reasoning_tokens": 451
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 1405,
      "prompt_tokens": 1661,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 2523
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
      "sha256": "3e7084e4cbfef81ba5ff5ac4ae7dbcd2bc1e8f123ef4abe0f490abcedb985909"
    },
    "response": {
      "path": "calls/c0001-use/a00/response.json",
      "sha256": "b158237fba88f191bf35615f77de9d1d669df82ae8b5b37fd06ec71c80bf206b"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "decomposed_use",
      "schema": "../contracts/decomposed-use.schema.json",
      "thinking": "off"
    },
    "status": "COMPLETE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 236,
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 1080,
      "prompt_tokens": 1336,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 1572
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0002-step",
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
      "path": "calls/c0002-step/a00/request.json",
      "sha256": "905f2a6092275ffa96ca65df59170dfeb7362c57aa8305c9d1eb7c2389c1e0d1"
    },
    "response": {
      "path": "calls/c0002-step/a00/response.json",
      "sha256": "1c4c1136671b1350a2f35fd1d89d8d2cda7b4aec0c5b01efd6f57c4ad776dc35"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "decomposed_step",
      "schema": "../contracts/decomposed-step.schema.json",
      "thinking": "off"
    },
    "status": "SCHEMA_FAILURE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 1272,
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 1348,
      "prompt_tokens": 1604,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 2876
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a01",
    "call": "c0002-step",
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
      "path": "calls/c0002-step/a01/request.json",
      "sha256": "4db4c97ce86a33f4b226f06c1a0663f27f35dafe73e3fb471fbc69d721a07c2a"
    },
    "response": {
      "path": "calls/c0002-step/a01/response.json",
      "sha256": "a6575586ff58db06ed17ebe85074efaaa00bc8d48cdc417f1c8b2867c03378f6"
    },
    "schema_repair": true,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "decomposed_step",
      "schema": "../contracts/decomposed-step.schema.json",
      "thinking": "off"
    },
    "status": "COMPLETE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 67,
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 3071,
      "prompt_tokens": 3071,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 3138
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
      "sha256": "c314f48f67572ce66094fb6d4301eae8000604671936a9769e6b18a157ce2319"
    },
    "response": {
      "path": "calls/initial/a00/response.json",
      "sha256": "f6ac727e37ee99bc7ca0e6091f576b4adce304d1e5bdbe5c1e25147e2532dca9"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "initial_decompose",
      "schema": "../contracts/initial-decompose.schema.json",
      "thinking": "native"
    },
    "status": "COMPLETE",
    "thinking": "native",
    "usage": {
      "completion_tokens": 2077,
      "completion_tokens_details": {
        "reasoning_tokens": 1524
      },
      "prompt_cache_hit_tokens": 896,
      "prompt_cache_miss_tokens": 210,
      "prompt_tokens": 1106,
      "prompt_tokens_details": {
        "cached_tokens": 896
      },
      "total_tokens": 3183
    },
    "wall_seconds": 300
  }
]
```
