# Personal reasoning run

This is a personal working tool. Its output is a working answer with its objections, not a finding.

Run ID: `20260916T101032Z-04bf836ad4-c7b306`

Recipe: `cross-family`; SHA-256 `04bf836ad436d0458f543e61adbd5c9b8b6a3cfb96606f22633857e59a0a0494`.

Seats: `{"conjecture": {"endpoint": "deepseek-flash", "thinking": "native", "reasoning_effort": "medium"}, "critics": [{"endpoint": "ollama/qwen3.5-397b.native", "thinking": "off", "reasoning_effort": "medium"}, {"endpoint": "ollama/glm-5.3.native", "thinking": "off", "reasoning_effort": "medium"}], "use": {"endpoint": "ollama/qwen3.5-397b.native", "thinking": "off", "reasoning_effort": "medium"}, "rival": null}`

Requested cycles: 3; completed cycles: 1.

Recorded call attempts: 13; planned logical calls without early stop: 16. Includes one conditional closing return allowance. Completion allowance without repair/retry/fallback: 278528. Input tokens are additional and depend on problem and growing objection history.

Closing return enabled: True; outcome: not required. When enabled, one extra logical return follows cycle_budget if any use objection remains open; it supplies a final disposition for all open objections and preserves cycle_budget on success.

Wall per attempt: 300 seconds; explicit transport retries: 0.

Schema repair calls: 3; at most one per logical call. Repair transport errors are not retried; a native ceiling may use the declared fallback. Maximum attempts including repairs, fallbacks and configured transport retries: 37; maximum completion allowance: 720896.

Native-to-off ceiling fallback calls: 0; allowance: 5. Each allowed fallback keeps the same context and ceiling; failure ends that logical call. Under reasoning-exposure-v2, named critic/use failures are recorded as unavailable.

Unavailable critic seats: 2; Unavailable use seats: 0. Counts are logical seat occurrences across cycles, not failed attempts.

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
    "call": "calls\\c0001-k01\\a01",
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

Baseline outcomes: `{"bare": "CEILING_HIT", "native": "COMPLETE"}`.

Baselines run first; named ceiling, transport and schema failures are nonfatal under the saved resilience policy. Baseline outputs, when requested, are in BASELINE.md. Extra loop calls are not matched multi-call controls. No comparison is computed. Native support means locally implemented explicit control, not a fresh service capability check.

The use reader derives a dependent question separately from the problem and working answer; both derivations can be wrong. Review its exact request and response alongside returned objections. Original observations are in calls/. Custody checker: minireason.reason.prompts.parse (first JSON object with validated role fields); semantic use checker: the declared use seat. JSON validation checks custody fields only and does not decide the legitimacy of prose criticism.

Reported usage by attempt (null means unknown):

```json
[
  {
    "call": "calls\\base-bare\\a00",
    "status": "CEILING_HIT",
    "usage": {
      "completion_tokens": 8192,
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 250,
      "prompt_tokens": 250,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 8442
    }
  },
  {
    "call": "calls\\base-native\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 19785,
      "completion_tokens_details": {
        "reasoning_tokens": 19051
      },
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 275,
      "prompt_tokens": 275,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 20060
    }
  },
  {
    "call": "calls\\c0001-k01\\a00",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 860,
      "prompt_tokens": 1164,
      "total_tokens": 2024
    }
  },
  {
    "call": "calls\\c0001-k01\\a01",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 551,
      "prompt_tokens": 2446,
      "total_tokens": 2997
    }
  },
  {
    "call": "calls\\c0001-k02\\a00",
    "status": "CEILING_HIT",
    "usage": {
      "completion_tokens": 8192,
      "prompt_tokens": 1121,
      "total_tokens": 9313
    }
  },
  {
    "call": "calls\\c0001-return\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 12696,
      "completion_tokens_details": {
        "reasoning_tokens": 11865
      },
      "prompt_cache_hit_tokens": 128,
      "prompt_cache_miss_tokens": 1559,
      "prompt_tokens": 1687,
      "prompt_tokens_details": {
        "cached_tokens": 128
      },
      "total_tokens": 14383
    }
  },
  {
    "call": "calls\\c0001-use\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 633,
      "prompt_tokens": 2163,
      "total_tokens": 2796
    }
  },
  {
    "call": "calls\\c0002-k01\\a00",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 7853,
      "prompt_tokens": 4210,
      "total_tokens": 12063
    }
  },
  {
    "call": "calls\\c0002-k01\\a01",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 190,
      "prompt_tokens": 12470,
      "total_tokens": 12660
    }
  },
  {
    "call": "calls\\c0002-k02\\a00",
    "status": "CEILING_HIT",
    "usage": {
      "completion_tokens": 8192,
      "prompt_tokens": 3962,
      "total_tokens": 12154
    }
  },
  {
    "call": "calls\\c0002-return\\a00",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 11140,
      "completion_tokens_details": {
        "reasoning_tokens": 10110
      },
      "prompt_cache_hit_tokens": 256,
      "prompt_cache_miss_tokens": 2864,
      "prompt_tokens": 3120,
      "prompt_tokens_details": {
        "cached_tokens": 256
      },
      "total_tokens": 14260
    }
  },
  {
    "call": "calls\\c0002-return\\a01",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 6839,
      "completion_tokens_details": {
        "reasoning_tokens": 5801
      },
      "prompt_cache_hit_tokens": 3072,
      "prompt_cache_miss_tokens": 1323,
      "prompt_tokens": 4395,
      "prompt_tokens_details": {
        "cached_tokens": 3072
      },
      "total_tokens": 11234
    }
  },
  {
    "call": "calls\\initial\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 25909,
      "completion_tokens_details": {
        "reasoning_tokens": 25253
      },
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 276,
      "prompt_tokens": 276,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 26185
    }
  }
]
```
