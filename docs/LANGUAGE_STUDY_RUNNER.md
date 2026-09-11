# Running the model-origin language study

The runner records expression, source-text-withheld reading and criticism of frozen model proposals. It does not grade semantic adequacy or creativity. Raw prose is usable without JSON, Lean or semantic-schema admission. The selected language is an experimental carrier, and a prose escape remains a legitimate recorded objection.

The entry point is `python -m minireason.language_study`. Provider configuration uses the existing DeepSeek client and credential environment. Every setup call and every carrier comparison consumes a frozen plan. Inspect, commit and publish each plan before its calls; inspect and publish the resulting records before the next test. Source changes after planning are refused, so finish implementation changes before creating the plan.

## Freeze original prose before inventing languages

```bash
python -m minireason.language_study prepare-plan --id L001-corpus --stage corpus --max-tokens 16384 --output experiments/plans/L001-corpus.json
```

After publishing that plan, the following command makes one recorded model call. A different problem can be supplied to the plan through `--problem path/to/problem.txt`.

```bash
python -m minireason.language_study prepare --plan experiments/plans/L001-corpus.json --output experiments/records/L001-corpus
```

Inspect and publish its `corpus.json`, original public response, report and errata. Then prepare the paired language proposal from those exact frozen corpus bytes.

```bash
python -m minireason.language_study prepare-plan --id L002-languages --stage languages --corpus experiments/records/L001-corpus/corpus.json --max-tokens 32768 --output experiments/plans/L002-languages.json
```

After publishing that plan, make its one model call.

```bash
python -m minireason.language_study prepare --plan experiments/plans/L002-languages.json --output experiments/records/L002-languages
```

`packet.json` contains the original corpus and the model's Lean-compatible and non-Lean languages. Its identity binds both languages and the corpus. Inspect it for embedded source quotations or ready-made translations before probing. If the model does not return identifiable language boundaries, `raw-artifact.json` and the provider records remain available, and the setup reports an incomplete extraction without erasing its prose.

## Compare one carrier per configuration test

```bash
python -m minireason.language_study plan --id L003-nonlean --packet experiments/records/L002-languages/packet.json --carrier nonlean_candidate --arms matched mini --max-tokens 16384 --rationale 'Compare expression and criticism paths using the same frozen non-Lean language.' --output experiments/plans/L003-nonlean.json
```

After publishing that plan, run its arms with at most five concurrent calls.

```bash
python -m minireason.language_study run --plan experiments/plans/L003-nonlean.json --output experiments/records/L003-nonlean --jobs 2
```

Carriers are `prose`, `lean_candidate` and `nonlean_candidate`. Available arms are `bare`, `native`, `matched`, `matched_native`, `mini` and `mini_native`. One-shot arms make one intervention call; matched and Mini arms make three. Native thinking is set by the arm name. Use a separately declared completion allowance for native comparisons and record actual token usage.

Each completed stage receives an immutable artifact record. Direct-call results retain earlier artifacts if a later call fails. Mini preserves its log and raw artifacts. No successor language or conjecture is installed during these probes. The summary reports recording outcomes and resources only; substantive findings belong in a separate review tied to the actual source, expression, reading and criticism.

New probe plans bind the exact UTF8 bytes of the shared packet, selected language and optional compiler observations. Before constructing any provider or starting an arm, the runner checks those snapshots and compiles the actual Mini manifest with its full material sources once. Both Mini arms reuse that compiled plan, and their records contain exact source copies. The preflight uses the real frozen material, including its size; it supplies no semantic adequacy gate. A configuration failure blocks the complete comparison with zero model calls and writes typed arm results, `preflight.json`, `errata.json`, `summary.json` and `REPORT.md`. Plans frozen before a source repair must be explicitly superseded and regenerated. Source drift is still refused before a run directory is created.

The reader stage omits the original corpus field and the nonselected language. It still sees the selected language and actual expression, either of which can contain source-derived information. A marked `PROSE-ESCAPE` quotation remains visible and must not be counted as evidence that the selected language represented that content. Matched and Mini use the same conditional outgoing prompt renderer after Mini's declared port visibility is checked, so their comparison calibrates routing and recording rather than supplying different reasoning instructions.

Optional compiler observations can be included through `plan --compiler-observations path/to/observations.txt`. They are frozen evidence supplied to criticism, with no semantic priority. This runner does not execute model-generated Lean source; compilation belongs to the separate controlled compiler workflow.
