# R001 premise supplement after concurrent judge revision

DRAFT R002; staged and not run. During preparation, independent judge review15 changed ten R001 reading/report drafts under receipts in docs/DECISION_LEDGER.md. Root did not modify those files. Initial [extracts](R001-PREMISE.md) and pins remain unchanged; byte-identical initial snapshots are recorded in work/w18/AS-FOUND-SNAPSHOTS.json. This supplement quotes the revised REPORT exactly, SHA-256 `db484b1c67658617887e213b79e1ff975f6e5e0fc086f74255d17631869d0af5`. The native-loop verdict is unchanged; P07 BARE is adjudicated incorrect, and all nine GLM unavailabilities are diagnosed as8192 output-length stops.

```text
|Problem|BARE|NATIVE|LOOP-CROSS|LOOP-SINGLE|
|---|---|---|---|---|
|[P01](readings/P01.md)|incorrect|correct|correct|correct|
|[P02](readings/P02.md)|incorrect|correct|correct|correct|
|[P03](readings/P03.md)|incorrect|correct|correct|correct|
|[P04](readings/P04.md)|correct|correct|correct|correct|
|[P05](readings/P05.md)|incorrect|correct|correct|correct|
|[P06](readings/P06.md)|correct|correct|correct|correct|
|[P07](readings/P07.md)|incorrect|correct|correct|correct|
|[P08](readings/P08.md)|undecidable|undecidable|correct|correct|
```

```text
## Episodes, basins and recurrent failures

No required four-way comparison shares the same wrong answer. P01/P02/P03/P05 BARE differ from the correct NATIVE and two initial conjectures; P04/P06 agree correctly; P07 shares a correct recap with one BARE contradiction; P08 lacks two complete baselines. Thus no "attractor signature: shared wrong answer" and no empty same-lineage critic on a wrong presented answer are witnessed. The exact initial/baseline quotations are in every case's basin section. This does not test or disprove the broader shared-prior hypothesis.

The selected CROSS runs repeatedly generate self-defeating raw objections, false arithmetic, and caveats about changed premises. Twelve raw objection objects in eight critic attempts themselves conclude no error or withdraw their allegation; repair turns each affected critic response into an empty delivered list. These are preserved as manufactured attempted objections, not falsely attributed to return. A further archived P02 malformed object does the same; its dated [supplement](readings/P02-SUPPLEMENT.md) preserves that text and correction to the initial parsing assessment. The two delivered use objections in P04/P08 challenge robustness to changed premises. In P07 Qwen asserts "7^2 = 49 = 2*19 + 10"; return rejects the arithmetic and use computes d(7)=3. In P05 Qwen estimates1.029 against the correct root; return rejects it and use confirms a roughly166Pa imbalance. These are successful resistance, not missed corrections.

P08-CROSS use repeatedly says the problem does not determine the release6 hypothetical, while its working derivation answers it. This is a failure of that use check to return an independently derived result for its own question. It is not the preregistered category "criticism failed to return", which requires a named actual error and a rejecting return. Most other uses ask confirmatory subquestions rather than independently solving the whole task. Their exact scope and separate derivations are in the readings. No observed wrong-to-right current endpoint is hidden behind those confirmations.

CROSS and SINGLE differ in traces: CROSS has the named false attacks, repairs and nine unavailable GLM critic occurrences; SINGLE supplies the explicit fixed-order dominance repair in P08. They also differ in critic multiplicity, model/use identity, thinking mode, completion allowances and fallback opportunities. Neither a lineage-only advantage nor advantage over a matched multi-call control is identified.

Operational diagnosis: all nine unavailable GLM critic occurrences are c0001-k02, c0002-k02 and c0003-k02 in each of [P02](runs/LOOP-CROSS/P02/TRACE.md), [P05](runs/LOOP-CROSS/P05/TRACE.md) and [P08](runs/LOOP-CROSS/P08/TRACE.md). Each provider record says `INCOMPLETE_GENERATION`, `finish_reason: length`, and8192 completion tokens; the request sends `think:false` and `options.num_predict:8192`. The adapter records `CEILING_HIT`. These are output-length failures, not transport or schema failures. Their public prefixes remain preserved; none is a delivered empty objection list. Off seats have no native-to-off fallback, and length failures do not enter schema repair. For a successor, preregister the GLM output allowance or output-contract change and the matching resource controls, then establish that this seat completes before interpreting its absence as blindness or attributing cross-lineage effects. No particular allowance is proven sufficient here.
```

R002 consequence after binding judge amendment 6: unavailable GLM does not establish blindness. The prospective R002 off allowance is now 16384 in every matched seat, with bounded critic working. No particular allowance is proven adequate; validate completion before any lineage reading. R001's fixed8192 observations remain unchanged.
