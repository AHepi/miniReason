# R003 run

Run: `20260917T092051Z-r002-efb1be`. Condition: `LOOP-CROSS`.

Calls/attempts: 6/6. Schema repairs: 0. Strict policy: one initial attempt plus at most one schema repair per logical call; zero fallbacks/transport retries; CEILING_HIT receives no repair.

Ceilings: native 32768; off 16384; prompt 32768; wall 300 seconds per attempt; at most 14 logical calls and 28 attempts. Base/max completion allowance: 409600/819200.

Reached by repair: `[]`. Reached without repair: `["c0001-return", "c0001-signal-a", "c0001-signal-b", "c0001-use", "closing-return", "initial"]`. Repair attempted but not completed: `[]`.

Completed cycles: 1. Closing return: complete.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 0.

Episode records/supplements: 0.

Reported usage (known portions only): `{"completion_tokens": 11604, "prompt_tokens": 19659, "total_tokens": 31263, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

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
      "sha256": "6fe251c816151bf55dde7ab1eaca598e7edbcbb0c0233a798506bb61df145f9d"
    },
    "response": {
      "path": "calls/c0001-return/a00/response.json",
      "sha256": "45db587dcd6deee7dcadec3f4366d39bdf1a6be6ac643705f1f6e1cbc37e6eaa"
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
      "completion_tokens": 3288,
      "completion_tokens_details": {
        "reasoning_tokens": 2286
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 4383,
      "prompt_tokens": 4639,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 7927
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
      "sha256": "53254e20878e64ebf240d8ff0fb8365f6debe842e8c5d00c3a042535034c45f3"
    },
    "response": {
      "path": "calls/c0001-signal-a/a00/response.json",
      "sha256": "a8b2c538074039df01440f5193e1f8398b0078b686671019fdcf2743c0ba9800"
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
      "completion_tokens": 277,
      "prompt_tokens": 2586,
      "total_tokens": 2863
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
      "sha256": "ecf2248832740b0669b7d070932514d515409bb286cde7a6fb591a20d12db154"
    },
    "response": {
      "path": "calls/c0001-signal-b/a00/response.json",
      "sha256": "26bce30ba633279e853e54c5924acc3830c032b6c2474bbde75b4346f3db4584"
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
      "completion_tokens": 281,
      "prompt_tokens": 2463,
      "total_tokens": 2744
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
      "sha256": "2822efe41c02d2f09f8a63d7d5ca043a10f9614710c8c7e80284371abb7d2ed0"
    },
    "response": {
      "path": "calls/c0001-use/a00/response.json",
      "sha256": "e1718e84eeb85156ab26c593d238cafaf0bed55790d1d31e3a0517fd5cf0496e"
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
      "completion_tokens": 1252,
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 4388,
      "prompt_tokens": 4772,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 6024
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
      "sha256": "ad55f71db0f2329dcf98482928fd60dce5c2560f10c727cd56d82e54e473b6e9"
    },
    "response": {
      "path": "calls/closing-return/a00/response.json",
      "sha256": "34ca8f51eaa575e356babf0b32d8e11b7e4530de83d810b34b4af2ad81e3e07b"
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
      "completion_tokens": 2318,
      "completion_tokens_details": {
        "reasoning_tokens": 1298
      },
      "prompt_cache_hit_tokens": 512,
      "prompt_cache_miss_tokens": 3573,
      "prompt_tokens": 4085,
      "prompt_tokens_details": {
        "cached_tokens": 512
      },
      "total_tokens": 6403
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
      "sha256": "c28e1bddbefa22a828d7b5a83ba65ecf4929c1a7a4d1ac7340d6efd38770ea9e"
    },
    "response": {
      "path": "calls/initial/a00/response.json",
      "sha256": "6ec19670d2f892c569a370e3b3a8ca0b0f29365662897ab6b850a75b9bb1f981"
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
      "completion_tokens": 4188,
      "completion_tokens_details": {
        "reasoning_tokens": 3225
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 858,
      "prompt_tokens": 1114,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 5302
    },
    "wall_seconds": 300
  }
]
```
