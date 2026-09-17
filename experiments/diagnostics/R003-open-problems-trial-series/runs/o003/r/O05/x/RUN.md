# R003 run

Run: `20260917T091623Z-r002-ae20a2`. Condition: `LOOP-CROSS`.

Calls/attempts: 9/11. Schema repairs: 2. Strict policy: one initial attempt plus at most one schema repair per logical call; zero fallbacks/transport retries; CEILING_HIT receives no repair.

Ceilings: native 32768; off 16384; prompt 32768; wall 300 seconds per attempt; at most 14 logical calls and 28 attempts. Base/max completion allowance: 409600/819200.

Reached by repair: `["c0001-use"]`. Reached without repair: `["c0001-return", "c0001-signal-a", "c0001-signal-b", "c0002-return", "c0002-signal-a", "c0002-signal-b", "initial"]`. Repair attempted but not completed: `["c0002-use"]`.

Completed cycles: 1. Closing return: not-run.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 1.

Episode records/supplements: 1.

Reported usage (known portions only): `{"completion_tokens": 26887, "prompt_tokens": 48975, "total_tokens": 75862, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

Stop reason: `SCHEMA_FAILURE`. propagation-use-r3-a2.schema.json:objections.0: Additional properties are not allowed ('working' was unexpected)

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
      "sha256": "165a0348b66d7a0a2f0fb59256fed2b579b525338e50adedb310d40ab1d8bedf"
    },
    "response": {
      "path": "calls/c0001-return/a00/response.json",
      "sha256": "c8a3a3279b6e2eabca88bbf95276f259172c5563c53914c1df6b3cc4607ecca5"
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
      "completion_tokens": 2749,
      "completion_tokens_details": {
        "reasoning_tokens": 1818
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 4197,
      "prompt_tokens": 4453,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 7202
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
      "sha256": "e169ff67355ff60bf85ae6a421751a41c7cae4158692726a8f3bb844cc6f0a31"
    },
    "response": {
      "path": "calls/c0001-signal-a/a00/response.json",
      "sha256": "4329abd41ebf1b45a6abf627e54a7830976da829a64479a3e2569a701f380c6d"
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
      "completion_tokens": 203,
      "prompt_tokens": 2551,
      "total_tokens": 2754
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
      "sha256": "2ff50919089ac2875382c75b5e343dc802cd08f0f2f8dd1a2624cd5425a2468d"
    },
    "response": {
      "path": "calls/c0001-signal-b/a00/response.json",
      "sha256": "bc81f1bb5b083568464c21375d8666f72b34200c849d3196fcc7f42df6d91c9e"
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
      "completion_tokens": 226,
      "prompt_tokens": 2441,
      "total_tokens": 2667
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
      "sha256": "c900b6e5659c126503e72df5331319417e4450b505298b8a2dfb9322ea5a049e"
    },
    "response": {
      "path": "calls/c0001-use/a00/response.json",
      "sha256": "f9ad9bbb6c1f387270d6800e0f2712d14cc03807311343fa3a27bb32a19456e2"
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
    "status": "SCHEMA_FAILURE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 1500,
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 4267,
      "prompt_tokens": 4651,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 6151
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a01",
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
      "path": "calls/c0001-use/a01/request.json",
      "sha256": "1127d745a3f6b94b8f23d7fac008b63b8e7c86baca2c7edd45eef6eb738db180"
    },
    "response": {
      "path": "calls/c0001-use/a01/response.json",
      "sha256": "406cffdb5e899b5935417ed7d35b521f98ea4fe68db6af54b727d1a9f991910d"
    },
    "schema_repair": true,
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
      "completion_tokens": 1485,
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 8010,
      "prompt_tokens": 8394,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 9879
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0002-return",
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
      "path": "calls/c0002-return/a00/request.json",
      "sha256": "e74c4d329cb98a7fbd584f1a195da654f1a2f5d57f471dd1dd528f785b8976c5"
    },
    "response": {
      "path": "calls/c0002-return/a00/response.json",
      "sha256": "c3fff6dfcae83dec4445b889803feaf536bbf4ecc529015197cfd5ae83c93250"
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
      "completion_tokens": 11885,
      "completion_tokens_details": {
        "reasoning_tokens": 10765
      },
      "prompt_cache_hit_tokens": 512,
      "prompt_cache_miss_tokens": 4643,
      "prompt_tokens": 5155,
      "prompt_tokens_details": {
        "cached_tokens": 512
      },
      "total_tokens": 17040
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0002-signal-a",
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
      "path": "calls/c0002-signal-a/a00/request.json",
      "sha256": "beacc40a8e0be1dd100b82833add2c6f1eff6a3b9e36197ce1641ac6d6181bd1"
    },
    "response": {
      "path": "calls/c0002-signal-a/a00/response.json",
      "sha256": "0b31123a41acf7359609a94229a79560b10895ee9196fa2553cdf93a8abffbab"
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
      "completion_tokens": 167,
      "prompt_tokens": 3322,
      "total_tokens": 3489
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0002-signal-b",
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
      "path": "calls/c0002-signal-b/a00/request.json",
      "sha256": "3d476788cbc775d542d15e836ae3cae21863f496f23819625efc163c20a16b83"
    },
    "response": {
      "path": "calls/c0002-signal-b/a00/response.json",
      "sha256": "16c55fa7f09801e631cbafcb329f47f04041d37df20dc0159bd4fecac9b3a0e7"
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
      "completion_tokens": 279,
      "prompt_tokens": 3193,
      "total_tokens": 3472
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0002-use",
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
      "path": "calls/c0002-use/a00/request.json",
      "sha256": "f787612aba7e7e932415911ba2449ae73ddf609ab9d64841176ce595e05990d9"
    },
    "response": {
      "path": "calls/c0002-use/a00/response.json",
      "sha256": "f7b38e4e70929579f0a5fb8cc4875ddd483ba6b3c7e026d565766988a79fee30"
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
    "status": "SCHEMA_FAILURE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 1686,
      "prompt_cache_hit_tokens": 640,
      "prompt_cache_miss_tokens": 4240,
      "prompt_tokens": 4880,
      "prompt_tokens_details": {
        "cached_tokens": 640
      },
      "total_tokens": 6566
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a01",
    "call": "c0002-use",
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
      "path": "calls/c0002-use/a01/request.json",
      "sha256": "a3289cd78b4d635a4f2ae0253b2461b54f93e7c87468ea155eadda923782e219"
    },
    "response": {
      "path": "calls/c0002-use/a01/response.json",
      "sha256": "726e86d0cebb000ab6f78915e00c3da745a6e9c0a36dddd3a768e542e83b0dc8"
    },
    "schema_repair": true,
    "seat": {
      "checker_mode": "disabled",
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "propagation_use",
      "schema": "../contracts/propagation-use-r3-a2.schema.json",
      "thinking": "off"
    },
    "status": "SCHEMA_FAILURE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 1646,
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 8421,
      "prompt_tokens": 8805,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 10451
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
      "sha256": "6271bd998e949485971011c14e6155b74de9c246060683a8b9a6b0ce4566a23d"
    },
    "response": {
      "path": "calls/initial/a00/response.json",
      "sha256": "0e897d0c91c07d9a95c3c9b574446fa9d75eefb3346f059241022b52859bb7d9"
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
      "completion_tokens": 5061,
      "completion_tokens_details": {
        "reasoning_tokens": 4160
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 874,
      "prompt_tokens": 1130,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 6191
    },
    "wall_seconds": 300
  }
]
```
