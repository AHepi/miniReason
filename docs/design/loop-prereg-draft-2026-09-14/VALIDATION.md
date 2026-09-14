# VALIDATION — L001 pre-registration bundle

Every command below was run from the **wave-0 staging clone**
`/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-impl/repo`
with `PYTHONPATH=src`, against the bundle at
`/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-prereg`.
The published repository `/home/user/miniReason` was opened **read-only**: no `git add`,
`commit`, `checkout`, `stash` or `reset` was run there, and no file under it was written.
**No provider call was made; nothing in this bundle has been dispatched.**

---

## 1. The one-line check the task asks for

```
$ cd /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-impl/repo
$ PYTHONPATH=src python3 -c "import sys; sys.path.insert(0,'src'); \
    from minireason.loop.types import LoopConfig; \
    c = LoopConfig.load('/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-prereg/config.json'); \
    print('OK', c.run_id, c.max_calls, len(c.reading_set))"
OK L001-loop-first-live-2026-09-14 396 38
```

`LoopConfig.load` calls `LoopConfig.from_mapping`, which is strict: it refuses an unknown
key rather than ignoring it, requires every member of `LoopConfig._REQUIRED`, requires all
three `AuditConfig` thresholds (none of them has a default, by design — a threshold that
appears by default was never pre-registered), and validates every bound. The config loaded
first time without a fix being needed after the seat and budget figures were settled; the
iterations before that were on the content, not on the schema.

## 2. The full bundle check

`validate.py` is the whole check, offline and pure. It re-derives everything this bundle
asserts rather than restating it: the strict loader on six deliberately broken copies of
the config, the seat registry lookups and the G0 constitution, the guard parameters
against the pinned standard, the reading-set/`max_calls` arithmetic, the obligations
digest over canonical bytes, every calibration anchor's source-byte digest and quoted-span
uniqueness against the published files, the two published-material facts the order
rationale rests on, the frozen ceiling and pre-registration sentences inside `PREREG.md`,
and a credential scan over the bundle.

```
$ cd /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-impl/repo
$ PYTHONPATH=src python3 -X utf8 /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/loop-prereg/validate.py
PASS  LoopConfig.load(config.json) -> schema minireason.loop.config.v1, run_id L001-loop-first-live-2026-09-14
PASS  cycle_budget=3 max_calls=396 provider_mode=live max_per_key=5 publish_ref=None
PASS  audit={'period': 2, 'judge_err_max': 0.2, 'streak_max': 12}
PASS  contrast={'attached': True, 'study': 'experiments/diagnostics/C001-contrast-triple', 'occurrences': ['experiments/diagnostics/C001-contrast-triple/occurrence-02']}
PASS  loop_plan_id is one id from file and object (cc7c137fbcb37b4f...); a changed pin changes it (f3b53f9522b7a48b...)
PASS  refused as CONFIG_UNKNOWN_KEY
PASS  refused as CONFIG_MISSING_KEY
PASS  refused as CONFIG_MISSING_KEY
PASS  refused as CONFIG_INVALID_VALUE
PASS  refused as CONFIG_INVALID_VALUE
PASS  refused as CONFIG_INVALID_VALUE
PASS  seat critic    ollama/kimi-k3           family=ollama-cloud/kimi      key_env=OLLAMA_API_KEY     timeout_seconds=180
PASS  seat defender  ollama/gemma4-31b        family=ollama-cloud/gemma     key_env=OLLAMA_API_KEY     timeout_seconds=180
PASS  seat variator  deepseek-flash           family=deepseek               key_env=DEEPSEEK_API_KEY   timeout_seconds=180
PASS  seat judge-1   ollama/gpt-oss-120b      family=ollama-cloud/gpt-oss   key_env=OLLAMA_API_KEY     timeout_seconds=180
PASS  seat judge-2   ollama/qwen3.5-397b      family=ollama-cloud/qwen      key_env=OLLAMA_API_KEY     timeout_seconds=180
PASS  G0 constitution: 2 judge families distinct; critic not in judge families; defender distinct from critic and from judge families; 5 distinct families over 5 seats
PASS  reopen_reasons, paraphrase_n, schema_repair_budget and min_judge_families equal standard.REOPEN_REASONS / standard.GUARD_PARAMETERS
PASS  reading_set.json entries == config.reading_set, 38 unique keys (16 c001-mark + 22 h005-row)
PASS  max_calls derivation: 0 (baseline) + 108 (12 cross-case x 9) + 242 (22 rows x 11) + 46 (one audit window) + 0 (dispatch) = 396 == config.max_calls
PASS  obligations.json sha256 713119a7cd255296058b18084a40cbac7a3353903bbf8cd260b6e78c173e4302 reproduces over canonical bytes; |O|=7 |P|=12; every clause carries a why_not_a_count note
PASS  calibration.json: 16 source-byte digests re-verify against the published files; every quoted span occurs exactly once in its source record
PASS  cal-05's framing-only quote occurs once in the banner and in no record; cal-07's duplicated sentence occurs once in o2 before the construction adds its second copy
PASS  cal-08's two order-swap pairs re-read from the published comparison.json: (empty, empty) -> same; ({n1,n2,n4}, {n1,n2}) -> differs
PASS  calibration.json carries 9 rows (>= 8) and covers every standard.CALIBRATION_ANCHORS id
PASS  C001 occurrence-02: 20/20 replicates COMPLETE, unresolved_cells empty - the order rationale holds
PASS  H005 golden and full use tables carry byte-identical row lists (22 rows); the published 90-row figure counts them twice and the reading set names them once
PASS  PREREG.md contains standard.CEILING_TEXT byte-for-byte, all 11 CEILING_REQUIRED_SENTENCES, all 10 PREREGISTRATION_REQUIRED_SENTENCES, and the obligations digest
PASS  every bundle file passes the standard's forbidden-stop-token scan
PASS  the bundle names DEEPSEEK_API_KEY and OLLAMA_API_KEY only as key_env names; no key value, no assignment form and no secret-shaped token appears anywhere

ALL CHECKS PASSED
$ echo $?
0
```

## 3. What each block of that output establishes

| block | establishes |
|---|---|
| `LoopConfig.load` … `contrast=` | the document is a valid `minireason.loop.config.v1` and every resolved value is the one declared |
| `loop_plan_id is one id …` | the plan identity is a pure function of the declared values and of the pins; formatting and key order are not part of it, and a one-byte pin change changes it |
| six `refused as …` lines | negative controls: an unknown key, a missing `audit` block, a missing `audit.judge_err_max`, an unknown `provider_mode`, a `max_per_key` above the provider ceiling and a repeated reading-set entry are each refused with the code the loader declares |
| five `seat …` lines | every seat exists in `src/minireason/data/endpoints.json`; no endpoint, family or `key_env` is invented |
| `G0 constitution …` | two judge families are distinct, the critic's family is in neither, the defender's differs from the critic's and is in neither, and five distinct families cover five seats |
| `reopen_reasons, paraphrase_n …` | the config's guard parameters are byte-equal to `standard.REOPEN_REASONS` and `standard.GUARD_PARAMETERS`, so attacking the standard reaches them |
| `reading_set.json entries == …` | the config's ordered key list and the documented reading set are the same 38 unique keys |
| `max_calls derivation …` | the budget arithmetic reproduces from the per-entry costs; `max_calls` is a declared boundary, not a round number |
| `obligations.json sha256 …` | the digest re-computes over the canonical bytes, so `obligations.json` is pinnable before cycle 1 and any later edit is visible |
| three `cal-…` lines and `calibration.json carries 9 rows` | every anchor is built from published bytes that still hash to what the file says, every quoted span occurs exactly once in its source, and the anchors cover every id in `standard.CALIBRATION_ANCHORS` |
| `C001 occurrence-02: 20/20 …` and `H005 golden and full …` | the two published-material facts the reading order rests on, re-read from the published files rather than quoted |
| `PREREG.md contains …` | the frozen ceiling is present byte-for-byte and every required sentence of both frozen texts is present |
| `every bundle file passes …` | no file describes a reached boundary as the inquiry running out of things to say |
| `the bundle names DEEPSEEK_API_KEY …` | key **names** only; no value, no assignment form, no secret-shaped token |

## 4. Bundle digests at the time of validation

*(`VALIDATION.md` itself is absent from the table: a file cannot carry its own digest.)*

| file | sha256 |
|---|---|
| `PREREG.md` | `c04c2092f672b52572ea98a60575e3405c5072f6b381b9b55a30cb3f7dcd16d6` |
| `calibration.json` | `9ca9ad04672e99becc19096e3de4d4010d9f21c700a979695ef034f9c19aae95` |
| `config.json` | `46495a6fa0ee5667b6ba5128adbaee9062ed5b6637310bb44b12efdf14c0da90` |
| `obligations.json` | `2913693abce664af387f1683c7cbfd622043a697343a6d415d89a8179d3652d6` |
| `reading_set.json` | `ef8c62a5ad6148c4bf676fadabba1ae0504babef26b4f793cce7d80ff37c728e` |
| `validate.py` | `fd8015261e86cf34cf87f1fd576fd28fb98cc635a7889ee7cb63cb5dde41f25e` |

The `loop_plan_id` printed above (`cc7c137f…`) is a **demonstration digest only**: it was
taken over a one-entry placeholder pin map to show that the identity is stable and
pin-sensitive. The run's real `loop_plan_id` is minted at S0 PREREGISTER over the full pin
set — runner v2, `graph_import_h005.py`, `use_relation_h005.py`, `contrast_triple_study.py`,
`provider_openai_compat.py`, `endpoints.json`, every prompt template, `obligations.json`,
`CEILING.md`, the `STD_READING` body, and each attached study's `PLAN.md` and
`material.json` — and is written into `plan.json` and published before the first call.
