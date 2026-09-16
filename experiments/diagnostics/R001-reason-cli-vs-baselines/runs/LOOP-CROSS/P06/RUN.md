# Personal reasoning run

This is a personal working tool. Its output is a working answer with its objections, not a finding.

Run ID: `20260916T185532Z-04bf836ad4-8fe913`

Recipe: `cross-family`; SHA-256 `04bf836ad436d0458f543e61adbd5c9b8b6a3cfb96606f22633857e59a0a0494`.

Seats: `{"conjecture": {"endpoint": "deepseek-flash", "thinking": "native", "reasoning_effort": "medium"}, "critics": [{"endpoint": "ollama/qwen3.5-397b.native", "thinking": "off", "reasoning_effort": "medium"}, {"endpoint": "ollama/glm-5.3.native", "thinking": "off", "reasoning_effort": "medium"}], "use": {"endpoint": "ollama/qwen3.5-397b.native", "thinking": "off", "reasoning_effort": "medium"}, "rival": null}`

Requested cycles: 3; completed cycles: 1.

Recorded call attempts: 8; planned logical calls without early stop: 16. Includes one conditional closing return allowance. Completion allowance without repair/retry/fallback: 278528. Input tokens are additional and depend on problem and growing objection history.

Closing return enabled: True; outcome: not required. When enabled, one extra logical return follows cycle_budget if any use objection remains open; it supplies a final disposition for all open objections and preserves cycle_budget on success.

Wall per attempt: 300 seconds; explicit transport retries: 0.

Schema repair calls: 1; at most one per logical call. Repair transport errors are not retried; a native ceiling may use the declared fallback. Maximum attempts including repairs, fallbacks and configured transport retries: 37; maximum completion allowance: 720896.

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

Stop reason: `no_new_objections`.

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
      "completion_tokens": 1658,
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 291,
      "prompt_tokens": 291,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 1949
    }
  },
  {
    "call": "calls\\base-native\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 4266,
      "completion_tokens_details": {
        "reasoning_tokens": 3697
      },
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 316,
      "prompt_tokens": 316,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 4582
    }
  },
  {
    "call": "calls\\c0001-k01\\a00",
    "status": "SCHEMA_FAILURE",
    "usage": {
      "completion_tokens": 1341,
      "prompt_tokens": 960,
      "total_tokens": 2301
    }
  },
  {
    "call": "calls\\c0001-k01\\a01",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 128,
      "prompt_tokens": 2719,
      "total_tokens": 2847
    }
  },
  {
    "call": "calls\\c0001-k02\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 1960,
      "prompt_tokens": 933,
      "total_tokens": 2893
    }
  },
  {
    "call": "calls\\c0001-return\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 1557,
      "completion_tokens_details": {
        "reasoning_tokens": 1295
      },
      "prompt_cache_hit_tokens": 128,
      "prompt_cache_miss_tokens": 817,
      "prompt_tokens": 945,
      "prompt_tokens_details": {
        "cached_tokens": 128
      },
      "total_tokens": 2502
    }
  },
  {
    "call": "calls\\c0001-use\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 586,
      "prompt_tokens": 914,
      "total_tokens": 1500
    }
  },
  {
    "call": "calls\\initial\\a00",
    "status": "COMPLETE",
    "usage": {
      "completion_tokens": 1575,
      "completion_tokens_details": {
        "reasoning_tokens": 1123
      },
      "prompt_cache_hit_tokens": 0,
      "prompt_cache_miss_tokens": 317,
      "prompt_tokens": 317,
      "prompt_tokens_details": {
        "cached_tokens": 0
      },
      "total_tokens": 1892
    }
  }
]
```

## Attempt diagnostics

calls\c0001-k01\a00: SCHEMA_FAILURE: OBJECTION_TEXT_TOO_LONG: final objection text exceeds 1200 characters; move public working into working; extra keys []
