# Fixed-construction reason response and isolated use

Read PURPOSE, STATUS, DECISION_LEDGER and the candidate/design/implementation reviews before acting. This two-stage workflow is a prospective amendment of the candidate deployment design: the response sees full frozen source, J and exactly one selected supplemental criticism; use sees only separately frozen domain data/questions and the returned account when enabled. It does not receive source, J, the original criticism or accumulated history as separate ports. A response may quote that material; its exact content is retained.

`return_path` is part of the frozen plan and Mini manifest. When false, the account field is exactly empty and the response port is absent. The response call still runs and is archived to keep instructions and stage counts fixed. Its resource cost remains counted. Bare and native have one response call. Matched, matched-native, Mini and Mini-native have response and use calls. Compare corresponding stages and record actual tokens; equal ceilings are not equal spending. One shared no-return baseline is one observation, even if used in several comparisons.

The stimulus package records exact original J/R bytes, the reviewed recoding, a different relevant criticism and zero-byte omission. Its separate review states which content is already present in common source and which questions supply diagnostic cues. Mechanical exclusion checks do not prove that a paraphrase or an earlier source contains no equivalent reason. No score decides creativity, criticism validity or language adequacy.

Plans are generated only after source integration and verification. For an already frozen and published plan, run from the repository root with the authorized key in `DEEPSEEK_API_KEY`:

```sh
python -m minireason.reason_use_study run --plan experiments/plans/E016-reason-original.json --output experiments/records/E016-reason-original --jobs 5
```

Inspect STATUS first: never run this example if its output already exists. No output path is overwritten and no automatic retry occurs. An interrupted or failed test must be preserved and published; a retry requires a new ID and frozen plan. There are no live calls in plan creation or the focused offline checks:

```sh
python -m unittest discover -s tests -p 'test_reason_use*.py' -v
```

For a future new plan, use `freeze-occurrence` and `plan` subcommands (see `--help`) or `make_plan`. Inputs contain exactly source, construction, original_criticism, criticism, use_data and use_questions signed occurrences. `original_criticism` is audit-only unless selected as criticism. CLI `--no-return-path` declares account omission. Freeze allocation reason, parent, relation, arms, resource settings and interpretation predicates before model responses.

Publish the plan and decision receipts before activation. After each configuration, preserve terminal or partial request/response evidence, Mini logs, original output occurrences, settings, token use and errata; perform separate integrity and passage-level review. Publish and verify that completed record before successor dispatch. A provider-access failure is an external blocker, not a verdict on reason use or the semantic class. Consult the running ledger for exact outstanding work.
