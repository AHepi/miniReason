# R003 run

Run: `20260917T090255Z-r002-03343d`. Condition: `LOOP-CROSS`.

Calls/attempts: 6/6. Schema repairs: 0. Strict policy: one initial attempt plus at most one schema repair per logical call; zero fallbacks/transport retries; CEILING_HIT receives no repair.

Ceilings: native 32768; off 16384; prompt 32768; wall 300 seconds per attempt; at most 14 logical calls and 28 attempts. Base/max completion allowance: 409600/819200.

Reached by repair: `[]`. Reached without repair: `["c0001-return", "c0001-signal-a", "c0001-signal-b", "c0001-use", "closing-return", "initial"]`. Repair attempted but not completed: `[]`.

Completed cycles: 1. Closing return: complete.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 0.

Episode records/supplements: 0.

Reported usage (known portions only): `{"completion_tokens": 17168, "prompt_tokens": 16766, "total_tokens": 33934, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

Stop reason: `no_new_objections`. 

Schema, counter and episode assembly success is custody evidence, not a score or correctness verdict.

## Actual request controls and reported usage

```json
[
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
      "sha256": "511efc6a48cc3506f0c055cde9844f9cd58f358ea094bee20da15c63aa9a9866"
    },
    "response": {
      "path": "calls/c0001-return/a00/response.json",
      "sha256": "481e148673198564756259755af108ac113f4f372cc00126745fc6923126d5d3"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "prose_return_with_forced_dispositions",
      "schema": "../../R002-episodes-under-calibrated-difficulty/contracts/prose-return.schema.json",
      "thinking": "native"
    },
    "status": "COMPLETE",
    "thinking": "native",
    "usage": {
      "completion_tokens": 4314,
      "completion_tokens_details": {
        "reasoning_tokens": 3728
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 3781,
      "prompt_tokens": 4037,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 8351
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0001-signal-a",
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
      "path": "calls/c0001-signal-a/a00/request.json",
      "sha256": "ae623ad5f431b7de503d21f51457a24cbda1cc883a83f7becb59d75d2d207a9b"
    },
    "response": {
      "path": "calls/c0001-signal-a/a00/response.json",
      "sha256": "0c94ea5e55690138cd418a8aaefa98465dbe9147e9e5deed18ceef477a19579f"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "ollama/qwen3.5-397b.native",
      "reasoning_effort": "medium",
      "role": "critic",
      "schema": "../contracts/prose-objection-r3-a2.schema.json",
      "thinking": "off"
    },
    "status": "COMPLETE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 220,
      "prompt_tokens": 2093,
      "total_tokens": 2313
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0001-signal-b",
    "completion_tokens": 32768,
    "endpoint": {
      "base_url": "https://ollama.com",
      "chat_path": "/api/chat",
      "family": "ollama-cloud/kimi",
      "key_env": "OLLAMA_API_KEY",
      "max_concurrency": 5,
      "model": "kimi-k3",
      "name": "ollama/kimi-k3.native",
      "native": true,
      "timeout_seconds": 300
    },
    "reasoning_effort": "medium",
    "request": {
      "path": "calls/c0001-signal-b/a00/request.json",
      "sha256": "aaf07ba4502e0f1bf776b9535f2b1f0a0b608d29202601ae259d2835c3e7228a"
    },
    "response": {
      "path": "calls/c0001-signal-b/a00/response.json",
      "sha256": "4f21cad4228b230b41362d9a6e6716e3014a4e3cce6e089f88385925e7fa7898"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "ollama/kimi-k3.native",
      "reasoning_effort": "medium",
      "role": "critic",
      "schema": "../contracts/prose-objection-r3-a2.schema.json",
      "thinking": "off"
    },
    "status": "COMPLETE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 224,
      "prompt_tokens": 1973,
      "total_tokens": 2197
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
      "sha256": "fb23fec1179d3330a499dddbe95a9b78edebc263d1a17d69875d9a0ba767d337"
    },
    "response": {
      "path": "calls/c0001-use/a00/response.json",
      "sha256": "c2ffbdad7de75cd2b18f5707b08e2d89ee7aad54a07feba48c7f3fbe55e79e8c"
    },
    "schema_repair": false,
    "seat": {
      "checker_mode": "disabled",
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "propagation_use",
      "schema": "../contracts/propagation-use-r3-a2.schema.json",
      "thinking": "off"
    },
    "status": "COMPLETE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 1018,
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 3485,
      "prompt_tokens": 3869,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 4887
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "closing-return",
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
      "path": "calls/closing-return/a00/request.json",
      "sha256": "b20b4ddd05b0a9831b6d4c9f4cc45714c1582c6c6fa241368cdc715f07ccd713"
    },
    "response": {
      "path": "calls/closing-return/a00/response.json",
      "sha256": "cfdc0d4dd2f4968a316c01265760b7774db39247b0b4d4ae09f959a1f173425f"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "prose_return_with_forced_dispositions",
      "schema": "../../R002-episodes-under-calibrated-difficulty/contracts/prose-return.schema.json",
      "thinking": "native"
    },
    "status": "COMPLETE",
    "thinking": "native",
    "usage": {
      "completion_tokens": 5993,
      "completion_tokens_details": {
        "reasoning_tokens": 5410
      },
      "prompt_cache_hit_tokens": 512,
      "prompt_cache_miss_tokens": 3159,
      "prompt_tokens": 3671,
      "prompt_tokens_details": {
        "cached_tokens": 512
      },
      "total_tokens": 9664
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
      "sha256": "ea87a83efe9532a3aec694a54efc3d567a3ce203c2edbcd6937dd79e7e7cd730"
    },
    "response": {
      "path": "calls/initial/a00/response.json",
      "sha256": "40033b054804fbf1ba22f9f1d0d941451bd704be3b01d8818d176bf026211147"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "conjecture",
      "schema": "../../R002-episodes-under-calibrated-difficulty/contracts/answer.schema.json",
      "thinking": "native"
    },
    "status": "COMPLETE",
    "thinking": "native",
    "usage": {
      "completion_tokens": 5399,
      "completion_tokens_details": {
        "reasoning_tokens": 4936
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 867,
      "prompt_tokens": 1123,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 6522
    },
    "wall_seconds": 300
  }
]
```
