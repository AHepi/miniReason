# R003 run

Run: `20260917T092337Z-r002-47f57d`. Condition: `LOOP-CROSS`.

Calls/attempts: 12/15. Schema repairs: 3. Strict policy: one initial attempt plus at most one schema repair per logical call; zero fallbacks/transport retries; CEILING_HIT receives no repair.

Ceilings: native 32768; off 16384; prompt 32768; wall 300 seconds per attempt; at most 14 logical calls and 28 attempts. Base/max completion allowance: 409600/819200.

Reached by repair: `["c0001-return", "c0001-use"]`. Reached without repair: `["c0001-signal-a", "c0001-signal-b", "c0002-return", "c0002-signal-a", "c0002-signal-b", "c0002-use", "c0003-signal-a", "c0003-signal-b", "initial"]`. Repair attempted but not completed: `["c0003-return"]`.

Completed cycles: 2. Closing return: not-run.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 0.

Episode records/supplements: 2.

Reported usage (known portions only): `{"completion_tokens": 72266, "prompt_tokens": 105285, "total_tokens": 177551, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

Stop reason: `SCHEMA_FAILURE`. Uptake must reconstruct the full derivation suffix

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
      "sha256": "b97b03d3ccdb5107b565ce40c7a000fd22bbaab6a636e5b23d471d53b9482b58"
    },
    "response": {
      "path": "calls/c0001-return/a00/response.json",
      "sha256": "0d2cd08409b6c9ff0e925be93d054ff2ff3b5b90f021b4a5f73094197dcd012e"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "prose_return_with_forced_dispositions",
      "schema": "../../R002-episodes-under-calibrated-difficulty/contracts/prose-return.schema.json",
      "thinking": "native"
    },
    "status": "SCHEMA_FAILURE",
    "thinking": "native",
    "usage": {
      "completion_tokens": 11799,
      "completion_tokens_details": {
        "reasoning_tokens": 9352
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 5232,
      "prompt_tokens": 5488,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 17287
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a01",
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
      "path": "calls/c0001-return/a01/request.json",
      "sha256": "f4f21dd29774e961aff7a8bb7c0ba9ef3cca2a2470bb71da623c3027ded50967"
    },
    "response": {
      "path": "calls/c0001-return/a01/response.json",
      "sha256": "566a41620454fe41858929592ae3a293df3a5a2787c39107b7064469cdd7d7ff"
    },
    "schema_repair": true,
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
      "completion_tokens": 3440,
      "completion_tokens_details": {
        "reasoning_tokens": 1047
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 10225,
      "prompt_tokens": 10481,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 13921
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
      "sha256": "ca8166465731ea437d9e15175b75c2e683a70da57540f7d5bebc15cd687cfed8"
    },
    "response": {
      "path": "calls/c0001-signal-a/a00/response.json",
      "sha256": "5f09e4123c444b92fd6f2c3f3604126f10e9c3a04f866733b42bed1f6176f946"
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
      "completion_tokens": 178,
      "prompt_tokens": 3632,
      "total_tokens": 3810
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
      "sha256": "a950774f961250bdb91385264490488a78f3bc4262c01f0e51d27aaed8a5ddd2"
    },
    "response": {
      "path": "calls/c0001-signal-b/a00/response.json",
      "sha256": "dd03670684b731f33457d1fad9f5956152dc07e97aef339178e2ba0b6284617a"
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
      "completion_tokens": 139,
      "prompt_tokens": 3519,
      "total_tokens": 3658
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
      "sha256": "bbcb66ef1185e4c5686b2a2212290f08c7bc86b129341fc2e70b0d324be4000d"
    },
    "response": {
      "path": "calls/c0001-use/a00/response.json",
      "sha256": "f17c366a12cff9f5b09daec747ea0e1dd697027b4d29e8122f122f1bf307308f"
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
      "completion_tokens": 2247,
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 6861,
      "prompt_tokens": 7245,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 9492
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
      "sha256": "06e4bb4ef9cb4cef20ea67fcfc4d8ded78b9c7f785a59fba52a082e120472c4b"
    },
    "response": {
      "path": "calls/c0001-use/a01/response.json",
      "sha256": "3250b0e9bd4c2c1d8105bc771908c02dbfe8c5cc05ce33aa827c2a629389ce47"
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
      "completion_tokens": 2207,
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 11361,
      "prompt_tokens": 11745,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 13952
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
      "sha256": "a652c6fe02128dae6d0782e7c64eac2657e4dc9201a445fb934c43bf6874fb17"
    },
    "response": {
      "path": "calls/c0002-return/a00/response.json",
      "sha256": "3725e900d7957496a48fbc20b4bc9481dc0f13bfb993c29e4d272226d1f7773f"
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
      "completion_tokens": 17565,
      "completion_tokens_details": {
        "reasoning_tokens": 14760
      },
      "prompt_cache_hit_tokens": 896,
      "prompt_cache_miss_tokens": 6199,
      "prompt_tokens": 7095,
      "prompt_tokens_details": {
        "cached_tokens": 896
      },
      "total_tokens": 24660
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
      "sha256": "2dd2de3b1476569c47e4aaf5050a483238339b99fb9ae6b11550c051f20f51ec"
    },
    "response": {
      "path": "calls/c0002-signal-a/a00/response.json",
      "sha256": "52eea14f21fba3a1ddee1055d3bfad5278bd833156ce471a046f42d74e07e83d"
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
      "completion_tokens": 198,
      "prompt_tokens": 5199,
      "total_tokens": 5397
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
      "sha256": "80aeeaf3ba24f8bb20272ccaef3ac43fe7e8224846e078171fc727c223c5b010"
    },
    "response": {
      "path": "calls/c0002-signal-b/a00/response.json",
      "sha256": "ba5bc5a1fe2b2cf02dc1a9e555d851b6d4daba755fcfa1382aa6a75a0f98fd5a"
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
      "completion_tokens": 240,
      "prompt_tokens": 5059,
      "total_tokens": 5299
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
      "sha256": "b1b09c566c72a8fda45bde04df6f92b90a06aaed7594fa9b7a67687fdad73554"
    },
    "response": {
      "path": "calls/c0002-use/a00/response.json",
      "sha256": "6b20f256750fcfe9befe2654f52fc267b2fca231ef8fdb286d7373e569d26f5a"
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
      "completion_tokens": 1703,
      "prompt_cache_hit_tokens": 896,
      "prompt_cache_miss_tokens": 7415,
      "prompt_tokens": 8311,
      "prompt_tokens_details": {
        "cached_tokens": 896
      },
      "total_tokens": 10014
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0003-return",
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
      "path": "calls/c0003-return/a00/request.json",
      "sha256": "28a00a6e9a59638f57b52e954669c86982a4d975956e452c1585492f753d04dd"
    },
    "response": {
      "path": "calls/c0003-return/a00/response.json",
      "sha256": "c8f9e13fbeb7850cda8e457ac0ad3f5faa47937c7891766ae24cee9bcb9f2893"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "prose_return_with_forced_dispositions",
      "schema": "../../R002-episodes-under-calibrated-difficulty/contracts/prose-return.schema.json",
      "thinking": "native"
    },
    "status": "SCHEMA_FAILURE",
    "thinking": "native",
    "usage": {
      "completion_tokens": 8734,
      "completion_tokens_details": {
        "reasoning_tokens": 5699
      },
      "prompt_cache_hit_tokens": 896,
      "prompt_cache_miss_tokens": 7724,
      "prompt_tokens": 8620,
      "prompt_tokens_details": {
        "cached_tokens": 896
      },
      "total_tokens": 17354
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a01",
    "call": "c0003-return",
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
      "path": "calls/c0003-return/a01/request.json",
      "sha256": "513862225ff0b9b2bea4d3f7155bc3e67b30c74018259eb5eab5837799f28d74"
    },
    "response": {
      "path": "calls/c0003-return/a01/response.json",
      "sha256": "4089b9cb2cc588408d4275ea659a1d83e5c92f24c029680c3b40b265323907a4"
    },
    "schema_repair": true,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "prose_return_with_forced_dispositions",
      "schema": "../../R002-episodes-under-calibrated-difficulty/contracts/prose-return.schema.json",
      "thinking": "native"
    },
    "status": "SCHEMA_FAILURE",
    "thinking": "native",
    "usage": {
      "completion_tokens": 7165,
      "completion_tokens_details": {
        "reasoning_tokens": 4206
      },
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 13812,
      "prompt_tokens": 14196,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 21361
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0003-signal-a",
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
      "path": "calls/c0003-signal-a/a00/request.json",
      "sha256": "11f7b8f0b0a294286ecf0e98cb24ce1db95b3eac41f02c3d64598f5add581103"
    },
    "response": {
      "path": "calls/c0003-signal-a/a00/response.json",
      "sha256": "3ba0ec01c854a417aaeee493c99ef2fd97cdd191c1d8ea55e0ced50280283248"
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
      "completion_tokens": 250,
      "prompt_tokens": 6725,
      "total_tokens": 6975
    },
    "wall_seconds": 300
  },
  {
    "attempt": "a00",
    "call": "c0003-signal-b",
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
      "path": "calls/c0003-signal-b/a00/request.json",
      "sha256": "4a09a04582d559e27e34fc3dcc2a414e3c6e399b43127e344b78679ad9afdcd6"
    },
    "response": {
      "path": "calls/c0003-signal-b/a00/response.json",
      "sha256": "8fcb32ec003cd2e887e58e9a8bf66cc1a75554c32d04122c6eca0933d068c257"
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
      "completion_tokens": 197,
      "prompt_tokens": 6536,
      "total_tokens": 6733
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
      "sha256": "e1282b84812481463879e6f206671e44cfedb90437e2bad440106e71c26b3c79"
    },
    "response": {
      "path": "calls/initial/a00/response.json",
      "sha256": "d5afe4b8fb5380a913dbc50daa59c43b67f7bac4c4aa80bf8277804452547fd2"
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
      "completion_tokens": 16204,
      "completion_tokens_details": {
        "reasoning_tokens": 14472
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 1178,
      "prompt_tokens": 1434,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 17638
    },
    "wall_seconds": 300
  }
]
```
