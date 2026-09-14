# H005 cycle 1: a transport-layer envelope asymmetry in the matched control arm

Root review, REC-20260914-L, 2026-09-14. Sentences are marked **Measured** (read from the merged tree) or **Interpretation**.

## What was observed

**Measured.** In `experiments/diagnostics/H005-open-prose-commitments/occurrence-01`, merged here unchanged at 6d11ae7, two of the five matched-arm nodes in daily cycle 1 record `"envelope_status": "OPAQUE"`: `responses/daily/matched/cycle01/response.json` and `.../carry.json`. Both also record `"status": "COMPLETE"` and `"finish_reason": "stop"`. Their public texts, in that directory, are `response.txt`, sha256 `054b1c43c50e4d2a581023dc73cd08439665cf18b7663681559a8ab19345df3a`, 7,732 bytes, and `carry.txt`, sha256 `c61e45da74b50542ae5d07b2e4af9a18e0696c789981ca26b42c944ec3913c8e`, 6,505 bytes.

**Measured.** `occurrence-01/checkpoints/wave0005.json` counts COMPLETE 17, OPAQUE 2, PARTIAL 0, FAILED 0; all 17 delivered nodes are daily cycle 1 and both OPAQUE ones are `matched`. `mini_prose` and `mini_fcl` have five nodes each and zero OPAQUE; `bare` and `native` are single-node arms.

## The mechanism

**Measured.** Each public text is JSON whose string values contain raw newline control characters — twelve in `response.txt`, sixteen in `carry.txt` — so strict `json.loads` raises `Invalid control character at: line 1 column 756 (char 755)` and `... column 727 (char 726)`. `tools/multicycle_commitment_study.py` `decode_contribution` (lines 329–341) then takes the failure branch:

```
        envelope = json.loads(content, object_pairs_hook=unique)
        …                                    # {'body','commitments'} shape check
    except (ValueError, TypeError):
        valid = False
    body = envelope['body'] if valid else content
    commitments = envelope['commitments'] if valid else ''
```

**Measured.** So `artifacts/daily/matched/cycle01/response.json` and `.../carry.json` store the whole raw text as `body` and `""` as `commitments`, `commitments_sha256` being `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, the sha256 of the empty string. **Measured.** Parsed with `strict=False` the same bytes yield exactly `{body, commitments}`, both strings, the commitments 2,346 and 2,363 characters; in `response.txt` the commitments field escapes its newlines and the body does not. **Measured.** Downstream, `requests/daily/matched/cycle01/carry.json` renders that dependency as `Delivery: COMPLETE; envelope: OPAQUE`, then `BODY` and the raw JSON, then an empty `COMMITMENTS` section.

**Measured.** `payload_for` sets `response_format {'type': 'json_object'}`; the plan sets `formal_syntax_validation` false; `PROTOCOL.md:56` requires an unparseable envelope's text to stay an opaque body and the commitment field to be "never reconstructed by the harness". **Measured.** DeepSeek's JSON-output documentation records only that the API "may occasionally return empty content"; it does not document malformed content. **Interpretation.** The commitments are absent by contract, not because the model omitted them.

## Why it matters

**Interpretation.** The matched control has lost its commitment surface twice in cycle 1 while both Mini arms lost none, so any later comparison of commitment persistence across arms must first separate carrier loss from substantive loss; reading `commitments_sha256 = e3b0c442…` at face value would score an encoding fault as an arm that declined to commit. The records are correct; the reading needs care.

## What is not claimed

No semantic verdict; nothing about creativity, correctness or quality. No claim that the model omitted commitments: the returned bytes contain them. No claim that the asymmetry is systematic — two nodes, one cycle, one problem. No recommendation to re-run, repair or modify the frozen run. `PROTOCOL.md:62` reserves substantive review of outputs to root, and this review does not exercise it.

## Two options, for a future occurrence only

Each would be a declared intervention with its own identity (`PURPOSE.md:5`), never a change to occurrence-01.

**Option A — record both parses.** Keep the strict parse as the sole authority for `envelope_status`; additionally record a `strict=False` reading in its own fields and digests, so carrier failures are visible and countable without the harness reconstructing a commitment field.

**Option B — instruct against literal newlines.** State in the material that newlines inside JSON strings must be escaped, with a sample envelope. **Interpretation.** This alters the prompt and therefore the studied arrangement, so it is not the same condition as occurrence-01.

Neither option is adopted here.
