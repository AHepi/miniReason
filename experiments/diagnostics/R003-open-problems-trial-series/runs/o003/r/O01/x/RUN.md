# R003 run

Run: `20260917T085951Z-r002-a14f1a`. Condition: `LOOP-CROSS`.

Calls/attempts: 6/6. Schema repairs: 0. Strict policy: one initial attempt plus at most one schema repair per logical call; zero fallbacks/transport retries; CEILING_HIT receives no repair.

Ceilings: native 32768; off 16384; prompt 32768; wall 300 seconds per attempt; at most 14 logical calls and 28 attempts. Base/max completion allowance: 409600/819200.

Reached by repair: `[]`. Reached without repair: `["c0001-return", "c0001-signal-a", "c0001-signal-b", "c0001-use", "closing-return", "initial"]`. Repair attempted but not completed: `[]`.

Completed cycles: 1. Closing return: complete.

Tail edits: 0. Stall switches: 0. Checker runs: 0. Cannot-decide responses: 0.

Episode records/supplements: 0.

Reported usage (known portions only): `{"completion_tokens": 18757, "prompt_tokens": 24946, "total_tokens": 43703, "unknown_attempts": 0, "unknown_by_field": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}}`. Unknown usage is not zero.

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
      "sha256": "3e3a8eabd5d9010ad6c690c0261cdb8f081ce9e85b76a504ca6306d642153931"
    },
    "response": {
      "path": "calls/c0001-return/a00/response.json",
      "sha256": "59da13dd5d8766d78632549bfdb23e43af14563afe60e9c10cbbf0af53293139"
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
      "completion_tokens": 5126,
      "completion_tokens_details": {
        "reasoning_tokens": 3443
      },
      "prompt_cache_hit_tokens": 128,
      "prompt_cache_miss_tokens": 5317,
      "prompt_tokens": 5445,
      "prompt_tokens_details": {
        "cached_tokens": 128
      },
      "total_tokens": 10571
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
      "sha256": "d8bc0c67bb6bd9e045016c5f3522aef3343da72d713caec03dc55ad39096aa99"
    },
    "response": {
      "path": "calls/c0001-signal-a/a00/response.json",
      "sha256": "c9eca8edf3597465ed46f0d847d21eff81dbd531ee0426eac7953c96ae070027"
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
      "completion_tokens": 191,
      "prompt_tokens": 3574,
      "total_tokens": 3765
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
      "sha256": "b221df9b7965d9fde4027ae5158ef4eb8c1c401d8174f51d67e2c11d77b4230d"
    },
    "response": {
      "path": "calls/c0001-signal-b/a00/response.json",
      "sha256": "7cd129086e3989362d9ff002d2f8fe6f88f3b899a070d26bb2f35530ad944bce"
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
      "completion_tokens": 171,
      "prompt_tokens": 3471,
      "total_tokens": 3642
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
      "sha256": "9beff01cee0a74672c74ac79f9c61f9d7ecec7a7b14cf13f18b0065f41daaa67"
    },
    "response": {
      "path": "calls/c0001-use/a00/response.json",
      "sha256": "bb118379862ed8928d27e7c5c929b4c7fd7978525ddd2c46bad90834f5ec2876"
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
      "completion_tokens": 1177,
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 6471,
      "prompt_tokens": 6471,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 7648
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
      "sha256": "92be62c519c5fd9974b7fcb525a66a2068c0eff5285f7a65748df940b7b24dff"
    },
    "response": {
      "path": "calls/closing-return/a00/response.json",
      "sha256": "037d5f6325565465543b1458c567da242507953f9ff09b5a17e0b41dc5bb20d1"
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
      "completion_tokens": 3575,
      "completion_tokens_details": {
        "reasoning_tokens": 1881
      },
      "prompt_cache_hit_tokens": 640,
      "prompt_cache_miss_tokens": 4179,
      "prompt_tokens": 4819,
      "prompt_tokens_details": {
        "cached_tokens": 640
      },
      "total_tokens": 8394
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
      "sha256": "b2f74f19c83b570aefd9c6afb85f9f7a150a6c73e6b0ec39a6a704da03ff29a9"
    },
    "response": {
      "path": "calls/initial/a00/response.json",
      "sha256": "7a3a030972e46e83521b286dd697b2309d5e7e6d8af213570644cde9d1fdc13e"
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
      "completion_tokens": 8517,
      "completion_tokens_details": {
        "reasoning_tokens": 6594
      },
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 1166,
      "prompt_tokens": 1166,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 9683
    },
    "wall_seconds": 300
  }
]
```
