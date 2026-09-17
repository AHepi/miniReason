# R003 run

Run: `20260917T093255Z-r002-dbb39f`. Condition: `LOOP-DECOMPOSED`.

Calls/attempts: 5/6. Schema repairs: 1. Strict policy: one initial attempt plus at most one schema repair per logical call; zero fallbacks/transport retries; CEILING_HIT receives no repair.

Ceilings: native 32768; STEP/use 16384; critics 32768; prompt 32768; wall 300 seconds per attempt; at most 14 logical calls and 28 attempts. Base/max completion allowance: 376832/753664.

Reached by repair: `[]`. Reached without repair: `["c0001-critic", "c0001-return", "c0001-use", "initial"]`. Repair attempted but not completed: `["c0002-step"]`.

Completed cycles: 1. Closing return: not-run.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 0.

Episode records/supplements: 0.

Reported usage (known portions only): `{"completion_tokens": 14194, "prompt_tokens": 18918, "total_tokens": 33112, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

Stop reason: `SCHEMA_FAILURE`. R3-A2 step result must end with the exact final commitment as 'COMMITMENT: <claim>'

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
      "sha256": "1e7f0c746012dc5dc6660d5b136f5757eadbb89aef23bdfc5370b4ec2f38811d"
    },
    "response": {
      "path": "calls/c0001-critic/a00/response.json",
      "sha256": "ea85e544ba91156d55b35b32cf7cd3461d10da7f1cdfcdfc333bee706876fd41"
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
      "completion_tokens": 203,
      "prompt_tokens": 3077,
      "total_tokens": 3280
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
      "sha256": "c749cfd97ca11367c1c3e0697bd784477f7e1245ddf4f7f1699c91318a8968c3"
    },
    "response": {
      "path": "calls/c0001-return/a00/response.json",
      "sha256": "7769a83657b65ac74c8c71f59e54e20596612c5c61a97005f8c4ba864d453c9a"
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
      "completion_tokens": 6137,
      "completion_tokens_details": {
        "reasoning_tokens": 5371
      },
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 2673,
      "prompt_tokens": 3057,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 9194
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
      "sha256": "8fe565e37725e5a4f3192375e6e9c73e1ec1dd155c64d855214bef6550ab9fb4"
    },
    "response": {
      "path": "calls/c0001-use/a00/response.json",
      "sha256": "7b65429f5008146cd4bb3c0263eebd3593616667ab0eda02ff8cc9cbc0f0c44c"
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
      "completion_tokens": 406,
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 2095,
      "prompt_tokens": 2351,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 2757
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
      "sha256": "54cd8f7144fe6fb2bc7f103eaa82bd129261cf518865e293b7cdd9ee939ffaad"
    },
    "response": {
      "path": "calls/c0002-step/a00/response.json",
      "sha256": "f5d47f34bcd1913e0c4a396c63dcdc71afa3704d18a59adaea8b20daf4596e00"
    },
    "schema_repair": false,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "decomposed_step",
      "schema": "../contracts/decomposed-step-r3-a2.schema.json",
      "thinking": "off"
    },
    "status": "SCHEMA_FAILURE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 1171,
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 2572,
      "prompt_tokens": 2956,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 4127
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
      "sha256": "d374881c735c5ae107e6ae963896579c585e9ab09e6d1d320e735f830cc500e5"
    },
    "response": {
      "path": "calls/c0002-step/a01/response.json",
      "sha256": "260110302fc63dd9f2adcf249cbaba5b02048f56833b4a4fe2a4d5210f19e68f"
    },
    "schema_repair": true,
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "role": "decomposed_step",
      "schema": "../contracts/decomposed-step-r3-a2.schema.json",
      "thinking": "off"
    },
    "status": "SCHEMA_FAILURE",
    "thinking": "off",
    "usage": {
      "completion_tokens": 1177,
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 4879,
      "prompt_tokens": 5263,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 6440
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
      "sha256": "cf5b2d99875aa82b47fde6c16483a506a0b37c56b1f916d5f5788aabfb30596d"
    },
    "response": {
      "path": "calls/initial/a00/response.json",
      "sha256": "463ca9b8872be6b7fb0ec158c385ec47bace5e880e51cc071dd1b28b24407d92"
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
      "completion_tokens": 5100,
      "completion_tokens_details": {
        "reasoning_tokens": 4337
      },
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 1830,
      "prompt_tokens": 2214,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 7314
    },
    "wall_seconds": 300
  }
]
```
