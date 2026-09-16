# Personal reasoning run

This is a personal working tool. Its output is a working answer with its objections, not a finding.

Run ID: `20260916T103424Z-04bf836ad4-795717`

Recipe: `cross-family`; SHA-256 `04bf836ad436d0458f543e61adbd5c9b8b6a3cfb96606f22633857e59a0a0494`.

Seats: `{"conjecture": {"endpoint": "deepseek-flash", "thinking": "native", "reasoning_effort": "medium"}, "critics": [{"endpoint": "ollama/qwen3.5-397b.native", "thinking": "off", "reasoning_effort": "medium"}, {"endpoint": "ollama/glm-5.3.native", "thinking": "off", "reasoning_effort": "medium"}], "use": {"endpoint": "ollama/qwen3.5-397b.native", "thinking": "off", "reasoning_effort": "medium"}, "rival": null}`

Requested cycles: 3; completed cycles: 1.

Recorded call attempts: 13; planned logical calls without early stop: 16. Includes one conditional closing return allowance. Completion allowance without repair/retry/fallback: 278528. Input tokens are additional and depend on problem and growing objection history.

Closing return enabled: True; outcome: not required. When enabled, one extra logical return follows cycle_budget if any use objection remains open; it supplies a final disposition for all open objections and preserves cycle_budget on success.

Wall per attempt: 300 seconds; explicit transport retries: 0.

Schema repair calls: 3; at most one per logical call. Repair transport errors are not retried; a native ceiling may use the declared fallback. Maximum attempts including repairs, fallbacks and configured transport retries: 37; maximum completion allowance: 720896.

Native-to-off ceiling fallback calls: 0; allowance: 5. Each allowed fallback keeps the same context and ceiling; failure ends that logical call. Under reasoning-exposure-v2, named critic/use failures are recorded as unavailable.

Unavailable critic seats: 0; Unavailable use seats: 0. Counts are logical seat occurrences across cycles, not failed attempts.

Declared ceilings and reasoning effort per seat (effort is sent only when the provider builder supports it):

```json
[
  {
    "role": "conjecture",
    "seat": "deepseek-flash",
    "thinking": "native",
    "reasoning_effort": "medium",
    "logical_calls": 1,
    "completion_tokens": 32768,
    "fallback_allowed": true
  },
  {
    "role": "return",
    "seat": "deepseek-flash",
    "thinking": "native",
    "reasoning_effort": "medium",
    "logical_calls": 3,
    "completion_tokens": 32768,
    "fallback_allowed": true
  },
  {
    "role": "use",
    "seat": "ollama/qwen3.5-397b.native",
    "thinking": "off",
    "reasoning_effort": "medium",
    "logical_calls": 3,
    "completion_tokens": 8192,
    "fallback_allowed": false
  },
  {
    "role": "critic-1",
    "seat": "ollama/qwen3.5-397b.native",
    "thinking": "off",
    "reasoning_effort": "medium",
    "logical_calls": 3,
    "completion_tokens": 8192,
    "fallback_allowed": false
  },
  {
    "role": "critic-2",
    "seat": "ollama/glm-5.3.native",
    "thinking": "off",
    "reasoning_effort": "medium",
    "logical_calls": 3,
    "completion_tokens": 8192,
    "fallback_allowed": false
  },
  {
    "role": "closing-return (conditional)",
    "seat": "deepseek-flash",
    "thinking": "native",
    "reasoning_effort": "medium",
    "logical_calls": 1,
    "completion_tokens": 32768,
    "fallback_allowed": true
  },
  {
    "role": "baseline-bare",
    "seat": "deepseek-flash",
    "thinking": "off",
    "reasoning_effort": "medium",
    "logical_calls": 1,
    "completion_tokens": 8192,
    "fallback_allowed": false
  },
  {
    "role": "baseline-native",
    "seat": "deepseek-flash",
    "thinking": "native",
    "reasoning_effort": "medium",
    "logical_calls": 1,
    "completion_tokens": 32768,
    "fallback_allowed": false
  }
]
```

Thinking, ceiling, effort, repair and fallback actually recorded for each attempt:

```json
[
  {
    "call": "calls\\base-bare\\a00",
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "thinking": "native"
    },
    "thinking": "off",
    "schema_repair": false,
    "ceiling_fallback": false,
    "max_tokens": 8192,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": null,
    "wire_think": null
  },
  {
    "call": "calls\\base-bare\\a01",
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "thinking": "native"
    },
    "thinking": "off",
    "schema_repair": true,
    "ceiling_fallback": false,
    "max_tokens": 8192,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": null,
    "wire_think": null
  },
  {
    "call": "calls\\base-native\\a00",
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "thinking": "native"
    },
    "thinking": "native",
    "schema_repair": false,
    "ceiling_fallback": false,
    "max_tokens": 32768,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": "medium",
    "wire_think": null
  },
  {
    "call": "calls\\c0001-k01\\a00",
    "seat": {
      "endpoint": "ollama/qwen3.5-397b.native",
      "reasoning_effort": "medium",
      "thinking": "off"
    },
    "thinking": "off",
    "schema_repair": false,
    "ceiling_fallback": false,
    "max_tokens": 8192,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": null,
    "wire_think": false
  },
  {
    "call": "calls\\c0001-k02\\a00",
    "seat": {
      "endpoint": "ollama/glm-5.3.native",
      "reasoning_effort": "medium",
      "thinking": "off"
    },
    "thinking": "off",
    "schema_repair": false,
    "ceiling_fallback": false,
    "max_tokens": 8192,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": null,
    "wire_think": false
  },
  {
    "call": "calls\\c0001-return\\a00",
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "thinking": "native"
    },
    "thinking": "native",
    "schema_repair": false,
    "ceiling_fallback": false,
    "max_tokens": 32768,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": "medium",
    "wire_think": null
  },
  {
    "call": "calls\\c0001-use\\a00",
    "seat": {
      "endpoint": "ollama/qwen3.5-397b.native",
      "reasoning_effort": "medium",
      "thinking": "off"
    },
    "thinking": "off",
    "schema_repair": false,
    "ceiling_fallback": false,
    "max_tokens": 8192,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": null,
    "wire_think": false
  },
  {
    "call": "calls\\c0002-k01\\a00",
    "seat": {
      "endpoint": "ollama/qwen3.5-397b.native",
      "reasoning_effort": "medium",
      "thinking": "off"
    },
    "thinking": "off",
    "schema_repair": false,
    "ceiling_fallback": false,
    "max_tokens": 8192,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": null,
    "wire_think": false
  },
  {
    "call": "calls\\c0002-k01\\a01",
    "seat": {
      "endpoint": "ollama/qwen3.5-397b.native",
      "reasoning_effort": "medium",
      "thinking": "off"
    },
    "thinking": "off",
    "schema_repair": true,
    "ceiling_fallback": false,
    "max_tokens": 8192,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": null,
    "wire_think": false
  },
  {
    "call": "calls\\c0002-k02\\a00",
    "seat": {
      "endpoint": "ollama/glm-5.3.native",
      "reasoning_effort": "medium",
      "thinking": "off"
    },
    "thinking": "off",
    "schema_repair": false,
    "ceiling_fallback": false,
    "max_tokens": 8192,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": null,
    "wire_think": false
  },
  {
    "call": "calls\\c0002-return\\a00",
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "thinking": "native"
    },
    "thinking": "native",
    "schema_repair": false,
    "ceiling_fallback": false,
    "max_tokens": 32768,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": "medium",
    "wire_think": null
  },
  {
    "call": "calls\\c0002-return\\a01",
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "thinking": "native"
    },
    "thinking": "native",
    "schema_repair": true,
    "ceiling_fallback": false,
    "max_tokens": 32768,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": "medium",
    "wire_think": null
  },
  {
    "call": "calls\\initial\\a00",
    "seat": {
      "endpoint": "deepseek-flash",
      "reasoning_effort": "medium",
      "thinking": "native"
    },
    "thinking": "native",
    "schema_repair": false,
    "ceiling_fallback": false,
    "max_tokens": 32768,
    "reasoning_effort": "medium",
    "wire_reasoning_effort": "medium",
    "wire_think": null
  }
]
```

Stop reason: `SCHEMA_FAILURE`.

Baseline outcomes: `{"bare": "COMPLETE", "native": "COMPLETE"}`.

Baselines run first; named ceiling, transport and schema failures are nonfatal under the saved resilience policy. Baseline outputs, when requested, are in BASELINE.md. Extra loop calls are not matched multi-call controls. No comparison is computed. Native support means locally implemented explicit control, not a fresh service capability check.

The use reader derives a dependent question separately from the problem and working answer; both derivations can be wrong. Review its exact request and response alongside returned objections. Original observations are in calls/. Custody checker: minireason.reason.prompts.parse (first JSON object with validated role fields); semantic use checker: the declared use seat. JSON validation checks custody fields only and does not decide the legitimacy of prose criticism.

Reported usage by attempt (null means unknown):

```json
[
  {
    "call": "calls\\base-bare\\a00",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 983,
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 468,
      "prompt_tokens": 468,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 1451
    }
  },
  {
    "call": "calls\\base-bare\\a01",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 938,
      "prompt_cache_hit_tokens": 1408,
      "prompt_cache_miss_tokens": 159,
      "prompt_tokens": 1567,
      "prompt_tokens_details": {
        "cached_tokens": 1408
      },
      "total_tokens": 2505
    }
  },
  {
    "call": "calls\\base-native\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 3702,
      "completion_tokens_details": {
        "reasoning_tokens": 3425
      },
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 493,
      "prompt_tokens": 493,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 4195
    }
  },
  {
    "call": "calls\\c0001-k01\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 384,
      "prompt_tokens": 1263,
      "total_tokens": 1647
    }
  },
  {
    "call": "calls\\c0001-k02\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 2740,
      "prompt_tokens": 1197,
      "total_tokens": 3937
    }
  },
  {
    "call": "calls\\c0001-return\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 4692,
      "completion_tokens_details": {
        "reasoning_tokens": 3937
      },
      "prompt_cache_hit_tokens": 128,
      "prompt_cache_miss_tokens": 1636,
      "prompt_tokens": 1764,
      "prompt_tokens_details": {
        "cached_tokens": 128
      },
      "total_tokens": 6456
    }
  },
  {
    "call": "calls\\c0001-use\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 365,
      "prompt_tokens": 2297,
      "total_tokens": 2662
    }
  },
  {
    "call": "calls\\c0002-k01\\a00",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 812,
      "prompt_tokens": 4010,
      "total_tokens": 4822
    }
  },
  {
    "call": "calls\\c0002-k01\\a01",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 335,
      "prompt_tokens": 5244,
      "total_tokens": 5579
    }
  },
  {
    "call": "calls\\c0002-k02\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 2742,
      "prompt_tokens": 3714,
      "total_tokens": 6456
    }
  },
  {
    "call": "calls\\c0002-return\\a00",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 2320,
      "completion_tokens_details": {
        "reasoning_tokens": 1544
      },
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 2513,
      "prompt_tokens": 2897,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 5217
    }
  },
  {
    "call": "calls\\c0002-return\\a01",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 1116,
      "completion_tokens_details": {
        "reasoning_tokens": 340
      },
      "prompt_cache_hit_tokens": 2816,
      "prompt_cache_miss_tokens": 1102,
      "prompt_tokens": 3918,
      "prompt_tokens_details": {
        "cached_tokens": 2816
      },
      "total_tokens": 5034
    }
  },
  {
    "call": "calls\\initial\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 5516,
      "completion_tokens_details": {
        "reasoning_tokens": 4969
      },
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 494,
      "prompt_tokens": 494,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 6010
    }
  }
]
```
