# Bounded construction and problem promotion

The installed inquiry runner extends the frozen carrier study with separately recorded construct, criticize, revise and promote occurrences. Read [PURPOSE](../../PURPOSE.md), [problem promotion](../PROBLEM_PROMOTION.md), the [research agenda](../RESEARCH_AGENDA.md) and the latest published records before selecting a question. This is the agenda's `joint_construction_v1` configuration; its four original instruction texts are retained exactly in `src/minireason/inquiry_data.py`.

The first integrated comparison freezes one issue occurrence and its selection reason for every arm. Parent material supplies the actual A/B passages, existing criticisms, unresolved relationship, new-use question and protected claims or uses. This is attributed research input, not an automatic assessment that the proposed relationship has bearing. Neither a syntax check nor a compulsory semantic schema admits or rejects the supplied prose.

| Arm | Calls | Requested stages |
|---|---:|---|
| bare, native | 1 | construct |
| matched, matched_native | 4 | construct, criticize, revise, promote |
| mini, mini_native | 4 | The same stages through actual Mini ports |

Compare construction J across all six arms. Compare proposed revisions and promoted questions only where those stages were requested. A bare construction and a four-stage promotion answer different questions, so their positions as terminal files do not make them comparable answers. A revision remains a proposed response; it does not demonstrate an executed repair.

Every stage receives the complete frozen packet, selected carrier, selected issue with allocation record, and supplied parents. Later stages additionally receive every exact prior output from that arm. Matched and Mini use the same system message and pure conditional prompt renderer. Mini validates its complete actual rendered brief before each provider dispatch. This establishes an orchestration comparison under the same conditional request policy; different realized prior answers can produce different later requests. Native mode and actual token use are recorded separately.

## Freeze the shared issue and plans

The runner is available as `python -m minireason.inquiry_study`. All paths below are placeholders for reviewed material; the commands make no calls until `run`.

```sh
python -m minireason.inquiry_study freeze-occurrence \
  --text selected-original-occurrence.txt \
  --origin attributed-origin.json \
  --packet experiments/records/E004-paired-languages/packet.json \
  --output experiments/plans/selected-issue.json

python -m minireason.inquiry_study plan \
  --id E011-inquiry-prose \
  --packet experiments/records/E004-paired-languages/packet.json \
  --issue experiments/plans/selected-issue.json \
  --parents experiments/plans/selected-parent.json \
  --carrier prose \
  --allocation-reason 'State the discriminating inquiry and its relation to the selected occurrence.' \
  --max-tokens 32768 \
  --parent-test E009-sources-lean \
  --output experiments/plans/E011-inquiry-prose.json
```

`freeze-occurrence` decodes exact UTF-8 bytes without newline normalization. Its origin file is a nonempty JSON object naming the actual experiment, arm, repeat, stage, artifact or source path and any separate reviewer attribution. Supply the whole selected occurrence rather than an extracted, improved question. Parent files use the same occurrence format. The absence of parents is represented explicitly as `[]`.

`make_plan(test_id, packet, issue, carrier, allocation_reason, *, parents=None, arms=None, max_tokens=16384, repetitions=1, parent_test=None)` is the Python interface. Supported carriers are `prose`, `lean_candidate` and `nonlean_candidate`; all six arms are used by default. Use an explicit 32768 ceiling when matching E008–E010's allowance. A different allowance is a declared intervention. Settings, stage instructions, complete input snapshots and repository source hashes are signed into the plan before execution.

`freeze_occurrence(text, origin, packet_id)` preserves raw text and hashes it. `load_frozen(path)` reads JSON without duplicate-key normalization. A selected queued promotion can be passed unchanged to `make_plan`; selection is recorded separately in the new plan's `activation` object. An occurrence identity is an integrity binding, not independent verification of the supplied historical attribution.

## Run and preserve the record

```sh
python -m minireason.inquiry_study run \
  --plan experiments/plans/E011-inquiry-prose.json \
  --output experiments/records/E011-inquiry-prose \
  --jobs 5
```

The Python interface is `run_test(plan_path, root, *, jobs=5, provider_factory=DeepSeek)`. A test uses at most five arm workers; the real provider also enforces a shared five-call cap in the process. Separate processes require an external shared cap. Source or plan identity drift refuses execution. Material and configuration failures produce zero-provider preflight records for the comparison. Transport failures stop that arm without retries, retain earlier occurrences and record errata. The CLI exits nonzero for an operationally failed comparison.

The actual Mini route performs four deterministic source-copy stages without model calls and four declared model stages. Attention is off. The final promote stage uses Mini's required structural `mini.verdict.v1` kind; that engine label does not assign its prose a semantic verdict. Raw output is copied identically into body and commitments only to satisfy transport, and the material ports render the body once. The adapter generates no `about` or `answers` edges from exposure or stage order.

The root stores the frozen plan, packet, selected occurrence, activation, parent material, preflight, summary, report and errata. Each arm retains actual provider requests and public responses, resources, stage artifacts and an `inquiry-queue.json` sidecar. Mini arms additionally retain source files, compiled manifest, route validation evidence and replayable engine logs. Native hidden reasoning text is discarded by the existing provider.

Calls include failed attempts. Token counters contain provider-reported usage only; a failed delivery may have unknown billed cost. Missing or malformed accounting is marked unavailable rather than silently reported as zero. Nonempty raw prose, usage, completion ceiling and frozen provider settings are transport conditions. Their failure does not refute an idea or disqualify prose criticism.

## Review and choose a later inquiry

The complete promote output enters the queue with `content_appraisal = unresolved`, `standing_effect = none` and `disposition = queued`, including a proposal to suspend or an awkward output that identifies no clear question. The host does not extract an improved question, accept a diagnosis, install a proposed language extension or automatically begin another episode. Selection into a later plan requires its own allocation reason; whether the occurrence identifies a useful question remains criticizable.

C0, L0 and prior occurrences remain unchanged. A later language or interpretation intervention receives a separate identity and an explicit changed-component account. Publish every completed configuration's record, including failure, through [the publication workflow](publish.md) before beginning its successor. A finite resource ceiling is not exhaustion of possible inquiry.

Prototype preparation findings and integration corrections are retained in [operations errata](../errata/operations.md) and [operations lessons](../lessons/operations.md). The preparation fixes preserve complete queue identities and keep child-route metadata from overwriting the host schema and neutral standing fields.

## Offline checks

```sh
python -m unittest discover -s tests -p 'test_inquiry_*.py' -v
```

The targeted suite uses scripted provider replies and the actual large E004 packet. It checks six-arm prompt parity, full-material routing, concurrent isolation, one shared compilation, partial failure retention, whole-occurrence selection, absence of implicit standing changes, frozen activation and text integrity, provider setting drift, missing usage and completion-cap refusal. It makes no live calls and establishes no substantive novelty, preservation, adequacy or creativity verdict.
