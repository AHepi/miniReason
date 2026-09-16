# Personal reasoning run

This is a personal working tool. Its output is a working answer with its objections, not a finding.

Run ID: `20260916T184624Z-04bf836ad4-95a8f8`

Recipe: `cross-family`; SHA-256 `04bf836ad436d0458f543e61adbd5c9b8b6a3cfb96606f22633857e59a0a0494`.

Seats: `{"conjecture": {"endpoint": "deepseek-flash", "thinking": "native", "reasoning_effort": "medium"}, "critics": [{"endpoint": "ollama/qwen3.5-397b.native", "thinking": "off", "reasoning_effort": "medium"}, {"endpoint": "ollama/glm-5.3.native", "thinking": "off", "reasoning_effort": "medium"}], "use": {"endpoint": "ollama/qwen3.5-397b.native", "thinking": "off", "reasoning_effort": "medium"}, "rival": null}`

Requested cycles: 3; completed cycles: 3.

Recorded call attempts: 17; planned logical calls without early stop: 16. Includes one conditional closing return allowance. Completion allowance without repair/retry/fallback: 278528. Input tokens are additional and depend on problem and growing objection history.

Closing return enabled: True; outcome: not required. When enabled, one extra logical return follows cycle_budget if any use objection remains open; it supplies a final disposition for all open objections and preserves cycle_budget on success.

Wall per attempt: 300 seconds; explicit transport retries: 0.

Schema repair calls: 2; at most one per logical call. Repair transport errors are not retried; a native ceiling may use the declared fallback. Maximum attempts including repairs, fallbacks and configured transport retries: 37; maximum completion allowance: 720896.

Native-to-off ceiling fallback calls: 0; allowance: 5. Each allowed fallback keeps the same context and ceiling; failure ends that logical call. Under reasoning-exposure-v2, named critic/use failures are recorded as unavailable.

Unavailable critic seats: 3; Unavailable use seats: 0. Counts are logical seat occurrences across cycles, not failed attempts.

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
    "call": "calls\\c0002-use\\a00",
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
    "call": "calls\\c0003-k01\\a00",
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
    "call": "calls\\c0003-k02\\a00",
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
    "call": "calls\\c0003-return\\a00",
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
    "call": "calls\\c0003-use\\a00",
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

Stop reason: `cycle_budget`.

Baseline outcomes: `{"bare": "COMPLETE", "native": "COMPLETE"}`.

Baselines run first; named ceiling, transport and schema failures are nonfatal under the saved resilience policy. Baseline outputs, when requested, are in BASELINE.md. Extra loop calls are not matched multi-call controls. No comparison is computed. Native support means locally implemented explicit control, not a fresh service capability check.

The use reader derives a dependent question separately from the problem and working answer; both derivations can be wrong. Review its exact request and response alongside returned objections. Original observations are in calls/. Custody checker: minireason.reason.prompts.parse (first JSON object with validated role fields); semantic use checker: the declared use seat. JSON validation checks custody fields only and does not decide the legitimacy of prose criticism.

Reported usage by attempt (null means unknown):

```json
[
  {
    "call": "calls\\base-bare\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 458,
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 391,
      "prompt_tokens": 391,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 849
    }
  },
  {
    "call": "calls\\base-native\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 7380,
      "completion_tokens_details": {
        "reasoning_tokens": 7070
      },
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 416,
      "prompt_tokens": 416,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 7796
    }
  },
  {
    "call": "calls\\c0001-k01\\a00",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 1167,
      "prompt_tokens": 1197,
      "total_tokens": 2364
    }
  },
  {
    "call": "calls\\c0001-k01\\a01",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 364,
      "prompt_tokens": 2782,
      "total_tokens": 3146
    }
  },
  {
    "call": "calls\\c0001-k02\\a00",
    "status": "CEILING_HIT",
    "usage": {
      "completion_tokens": 8192,
      "prompt_tokens": 1105,
      "total_tokens": 9297
    }
  },
  {
    "call": "calls\\c0001-return\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 4677,
      "completion_tokens_details": {
        "reasoning_tokens": 4244
      },
      "prompt_cache_hit_tokens": 128,
      "prompt_cache_miss_tokens": 1262,
      "prompt_tokens": 1390,
      "prompt_tokens_details": {
        "cached_tokens": 128
      },
      "total_tokens": 6067
    }
  },
  {
    "call": "calls\\c0001-use\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 560,
      "prompt_tokens": 1701,
      "total_tokens": 2261
    }
  },
  {
    "call": "calls\\c0002-k01\\a00",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 816,
      "prompt_tokens": 3069,
      "total_tokens": 3885
    }
  },
  {
    "call": "calls\\c0002-k01\\a01",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 203,
      "prompt_tokens": 4303,
      "total_tokens": 4506
    }
  },
  {
    "call": "calls\\c0002-k02\\a00",
    "status": "CEILING_HIT",
    "usage": {
      "completion_tokens": 8192,
      "prompt_tokens": 2692,
      "total_tokens": 10884
    }
  },
  {
    "call": "calls\\c0002-return\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 3925,
      "completion_tokens_details": {
        "reasoning_tokens": 3471
      },
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 2150,
      "prompt_tokens": 2534,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 6459
    }
  },
  {
    "call": "calls\\c0002-use\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 560,
      "prompt_tokens": 3213,
      "total_tokens": 3773
    }
  },
  {
    "call": "calls\\c0003-k01\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 176,
      "prompt_tokens": 4585,
      "total_tokens": 4761
    }
  },
  {
    "call": "calls\\c0003-k02\\a00",
    "status": "CEILING_HIT",
    "usage": {
      "completion_tokens": 8192,
      "prompt_tokens": 4042,
      "total_tokens": 12234
    }
  },
  {
    "call": "calls\\c0003-return\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 5087,
      "completion_tokens_details": {
        "reasoning_tokens": 4611
      },
      "prompt_cache_hit_tokens": 384,
      "prompt_cache_miss_tokens": 3411,
      "prompt_tokens": 3795,
      "prompt_tokens_details": {
        "cached_tokens": 384
      },
      "total_tokens": 8882
    }
  },
  {
    "call": "calls\\c0003-use\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 560,
      "prompt_tokens": 4754,
      "total_tokens": 5314
    }
  },
  {
    "call": "calls\\initial\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 7488,
      "completion_tokens_details": {
        "reasoning_tokens": 6987
      },
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 417,
      "prompt_tokens": 417,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 7905
    }
  }
]
```

## Attempt diagnostics

calls\c0001-k01\a00: SCHEMA_FAILURE: OBJECTION_TEXT_TOO_LONG: final objection text exceeds 1200 characters; move public working into working; extra keys []

calls\c0001-k02\a00: CEILING_HIT: Provider finish_reason=length; extra keys []

calls\c0002-k01\a00: SCHEMA_FAILURE: OBJECTION_TEXT_TOO_LONG: final objection text exceeds 1200 characters; move public working into working; extra keys []

calls\c0002-k02\a00: CEILING_HIT: Provider finish_reason=length; extra keys []

calls\c0003-k02\a00: CEILING_HIT: Provider finish_reason=length; extra keys []
