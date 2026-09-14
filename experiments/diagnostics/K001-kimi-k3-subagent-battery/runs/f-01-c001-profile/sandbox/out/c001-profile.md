# C001 occurrence-01 failure profile

Produced by `python3 check/c001_profile.py` from the 240 response receipts under `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/` and the endpoint registry `src/minireason/data/endpoints.json`. Each receipt carries two code-bearing fields: `failure_type` (provider-side) and `validation_failure_type` (validation-side); one receipt may carry both.

Counts below are information, never a warrant. No rate, share or ranking between families, arms or endpoints is computed; these are independent occasions under different declared ceilings, not competitors.

## Endpoint-to-family mapping (derived)

`endpoint_slug` in each receipt is the registry `name` with `/` replaced by `-`; `family` is then read from `src/minireason/data/endpoints.json`. The six endpoints present in this occurrence map as follows:

| endpoint_slug | registry name | family | receipts |
|---|---|---|---|
| `deepseek-flash` | `deepseek-flash` | `deepseek` | 40 |
| `ollama-gemma4-31b` | `ollama/gemma4-31b` | `ollama-cloud/gemma` | 40 |
| `ollama-glm-5.3` | `ollama/glm-5.3` | `ollama-cloud/glm` | 40 |
| `ollama-gpt-oss-120b` | `ollama/gpt-oss-120b` | `ollama-cloud/gpt-oss` | 40 |
| `ollama-kimi-k3` | `ollama/kimi-k3` | `ollama-cloud/kimi` | 40 |
| `ollama-qwen3.5-397b` | `ollama/qwen3.5-397b` | `ollama-cloud/qwen` | 40 |

## 1. Failure-code census over all 240 receipts

| failure code | source field | receipts carrying it |
|---|---|---|
| `INCOMPLETE_GENERATION` | `failure_type` (provider-side) | 20 |
| `NO_PUBLIC_CONTENT` | `validation_failure_type` (validation-side) | 11 |

Co-carriage of the two code fields across the 240 receipts:

| field combination | receipts |
|---|---|
| both `failure_type` and `validation_failure_type` | 11 |
| only `failure_type` | 9 |
| only `validation_failure_type` | 0 |
| neither field | 220 |
| any code (union) | 20 |

## 2. Failure codes per family

| family | receipts | `INCOMPLETE_GENERATION` (`failure_type`) | `NO_PUBLIC_CONTENT` (`validation_failure_type`) | receipts with both fields | receipts with any code |
|---|---|---|---|---|---|
| `deepseek` | 40 | 19 | 11 | 11 | 19 |
| `ollama-cloud/gemma` | 40 | 0 | 0 | 0 | 0 |
| `ollama-cloud/glm` | 40 | 1 | 0 | 0 | 1 |
| `ollama-cloud/gpt-oss` | 40 | 0 | 0 | 0 | 0 |
| `ollama-cloud/kimi` | 40 | 0 | 0 | 0 | 0 |
| `ollama-cloud/qwen` | 40 | 0 | 0 | 0 | 0 |

## 3. Failure codes per family and arm

| family | arm | receipts | `INCOMPLETE_GENERATION` (`failure_type`) | `NO_PUBLIC_CONTENT` (`validation_failure_type`) | receipts with both fields | receipts with any code |
|---|---|---|---|---|---|---|
| `deepseek` | `fcl` | 20 | 19 | 11 | 11 | 19 |
| `deepseek` | `prose` | 20 | 0 | 0 | 0 | 0 |
| `ollama-cloud/gemma` | `fcl` | 20 | 0 | 0 | 0 | 0 |
| `ollama-cloud/gemma` | `prose` | 20 | 0 | 0 | 0 | 0 |
| `ollama-cloud/glm` | `fcl` | 20 | 1 | 0 | 0 | 1 |
| `ollama-cloud/glm` | `prose` | 20 | 0 | 0 | 0 | 0 |
| `ollama-cloud/gpt-oss` | `fcl` | 20 | 0 | 0 | 0 | 0 |
| `ollama-cloud/gpt-oss` | `prose` | 20 | 0 | 0 | 0 | 0 |
| `ollama-cloud/kimi` | `fcl` | 20 | 0 | 0 | 0 | 0 |
| `ollama-cloud/kimi` | `prose` | 20 | 0 | 0 | 0 | 0 |
| `ollama-cloud/qwen` | `fcl` | 20 | 0 | 0 | 0 | 0 |
| `ollama-cloud/qwen` | `prose` | 20 | 0 | 0 | 0 | 0 |

## 4. Status distribution per endpoint

| endpoint_slug | family | COMPLETE | PARTIAL | FAILED | total |
|---|---|---|---|---|---|
| `deepseek-flash` | `deepseek` | 21 | 8 | 11 | 40 |
| `ollama-gemma4-31b` | `ollama-cloud/gemma` | 40 | 0 | 0 | 40 |
| `ollama-glm-5.3` | `ollama-cloud/glm` | 39 | 1 | 0 | 40 |
| `ollama-gpt-oss-120b` | `ollama-cloud/gpt-oss` | 40 | 0 | 0 | 40 |
| `ollama-kimi-k3` | `ollama-cloud/kimi` | 40 | 0 | 0 | 40 |
| `ollama-qwen3.5-397b` | `ollama-cloud/qwen` | 40 | 0 | 0 | 40 |

## 5. Receipts carrying a code

20 receipts carry at least one code (9 with `status` = PARTIAL, 11 with `status` = FAILED). Each is listed with its coordinate, the code(s) present, `finish_reason` and `usage.completion_tokens` (`null` means the receipt does not record a value).

| endpoint_slug | arm | case | replicate | codes present | finish_reason | usage.completion_tokens |
|---|---|---|---|---|---|---|
| `deepseek-flash` | fcl | carrier | 2 | `failure_type=INCOMPLETE_GENERATION` | length | 8192 |
| `deepseek-flash` | fcl | carrier | 3 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | carrier | 4 | `failure_type=INCOMPLETE_GENERATION` | length | 8192 |
| `deepseek-flash` | fcl | carrier | 5 | `failure_type=INCOMPLETE_GENERATION` | length | 8192 |
| `deepseek-flash` | fcl | control | 1 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | control | 2 | `failure_type=INCOMPLETE_GENERATION` | length | 8192 |
| `deepseek-flash` | fcl | control | 3 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | control | 4 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | control | 5 | `failure_type=INCOMPLETE_GENERATION` | length | 8192 |
| `deepseek-flash` | fcl | original | 1 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | original | 2 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | original | 3 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | original | 4 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | original | 5 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | recoding | 1 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | recoding | 2 | `failure_type=INCOMPLETE_GENERATION` | length | 8192 |
| `deepseek-flash` | fcl | recoding | 3 | `failure_type=INCOMPLETE_GENERATION`; `validation_failure_type=NO_PUBLIC_CONTENT` | null | null |
| `deepseek-flash` | fcl | recoding | 4 | `failure_type=INCOMPLETE_GENERATION` | length | 8192 |
| `deepseek-flash` | fcl | recoding | 5 | `failure_type=INCOMPLETE_GENERATION` | length | 8192 |
| `ollama-glm-5.3` | fcl | control | 2 | `failure_type=INCOMPLETE_GENERATION` | length | 32768 |

## 6. Where the codes are concentrated, and at what declared ceiling

- `INCOMPLETE_GENERATION` (provider-side, `failure_type`) is concentrated on `deepseek-flash`: 19 of the 20 coded receipts are `deepseek-flash`, all in arm `fcl`; the remaining coded receipt is `ollama-glm-5.3/fcl/control/rep2`.
- On `deepseek-flash`, the coded receipts show `finish_reason` values length and null (no recorded value) and `usage.completion_tokens` values 8192 and null (no recorded value). Every coded `deepseek-flash` receipt that records a stopping point reports `finish_reason` = `length` with `usage.completion_tokens` = 8,192, and its `unresolved_reason` names an 8,192-token completion ceiling (quoted verbatim below). The recorded call timeout on `deepseek-flash` is `timeout_seconds` = 180 s. A token ceiling is a resource boundary; it is not evidence about the model's ability to solve the task.
- The single `ollama-glm-5.3` coded receipt (`fcl/control/rep2`) also reports `finish_reason` = `length`; receipts on this endpoint record `timeout_seconds` = 600 s. It reports `usage.completion_tokens` = 32,768, and its `unresolved_reason` names an 8,192-token ceiling; the two do not match (see section 7).
- `NO_PUBLIC_CONTENT` (validation-side, `validation_failure_type`) appears only on `deepseek-flash` arm `fcl`, and only together with the provider-side code: no receipt carries the validation-side code alone.
- No receipt in arm `prose` carries a code (0 of 120); arm `fcl` holds 20 of 120 coded-cell receipts.

`unresolved_reason` text recorded on the coded receipts, quoted verbatim:

> PARTIAL delivery: generation stopped at the 8192-token ceiling, so the commitment surface is truncated. The cell is unresolved and is not compared against another case (FW5:634).

This concentration is a count under each endpoint's own declared conditions; it is not a comparison between endpoints and no rate or ranking is drawn from it.

## 7. What the records do not settle

- The 11 `FAILED` coded receipts (all `deepseek-flash` arm `fcl`) record `finish_reason` = null and `usage` = null (`usage_status` = `UNKNOWN`). Whether those calls stopped at the same 8,192-token completion ceiling, earlier, or for a different reason (a resource boundary such as the recorded 180-second call timeout, or a transport event) cannot be determined from these receipts.
- `ollama-glm-5.3/fcl/control/rep2` reports `usage.completion_tokens` = 32,768 with `finish_reason` = `length`, while its `unresolved_reason` text names an 8,192-token ceiling. Which completion ceiling was actually declared for that call is unresolved by these receipts; no C001 plan or config file is present in this sandbox under `experiments/diagnostics/C001-contrast-triple/occurrence-01/` to cross-check against.
- On the `FAILED` receipts, `provider_status`, `returned_model` and `strict_parse_would_succeed` are null, so the records do not settle whether the provider returned any usable content before validation recorded `NO_PUBLIC_CONTENT`.
- The receipts do not record why the provider-side and validation-side codes co-occur exactly on the 11 `FAILED` receipts; they say what each field carries, not which check ran first or caused the other.

