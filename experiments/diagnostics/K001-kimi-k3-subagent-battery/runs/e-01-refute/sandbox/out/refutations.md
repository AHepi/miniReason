# Refutation check — three §4 "Live spend" claims

Source of the claims: `docs/reviews/session-orchestration-report-2026-09-14.md`,
section 4 ("Failure profile by code" and "Decode" paragraphs).

Record used, exactly as published in this sandbox:

- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/<endpoint_slug>/<arm>/<case>/rep<n>.json` — 240 receipts, 12 (endpoint, arm) cells of 20.
- `experiments/diagnostics/F001-fork5-multifamily/occurrence-0N/responses/<problem>/<arm>/cycle01/<node>.json` — 63 receipts in occurrences 01–06 ("F001 v1"), 20 in occurrences 07–08 (kept for context only).

Method: nothing eyeballed. Two scripts in `check/` walk the receipts and count.

- `check/refute_claims.py` — run as `python3 check/refute_claims.py` (exit code 0). Loads every C001 occurrence-01 receipt and every F001 receipt, then prints every figure quoted below.
- `check/refute_claims_tail.py` — run as `python3 check/refute_claims_tail.py` (exit code 0). The per-coordinate cross-checks (usage blocks, reasoning tokens, repair/strict cross-tab) quoted below.

Every count below is followed by the output line that produced it.

---

## CLAIM 1 — REFUTED IN PART

> "`INCOMPLETE_GENERATION`: ... 20 in C001 occurrence-01, the eleven FAILED plus
> the nine PARTIAL of the `deepseek-flash` x `fcl` cell, the provider raising it
> on both".

Clauses checked one by one against the 240 occurrence-01 receipts.

**(a) "20 in C001 occurrence-01" — survives.**
Script output (`failure_type counts (null = no failure): {None: 220, 'INCOMPLETE_GENERATION': 20}`)
and (`INCOMPLETE_GENERATION receipts: 20`; `statuses among them: Counter({'FAILED': 11, 'PARTIAL': 9})`).

**(b) "the eleven FAILED" — survives.**
All 20 `INCOMPLETE_GENERATION` coordinates printed by the script: the eleven
FAILED are exactly the eleven `deepseek-flash/fcl/{carrier rep3; control
rep1/rep3/rep4; original rep1..rep5; recoding rep1/rep3}` receipts, each carrying
`failure_type: INCOMPLETE_GENERATION` and `validation_failure_type: NO_PUBLIC_CONTENT`.

**(c) "the nine PARTIAL of the `deepseek-flash` x `fcl` cell" — REFUTED, with a
named coordinate.** The cell carries **8** PARTIAL with the code
(`cells among them: Counter({('deepseek-flash', 'fcl'): 19, ('ollama-glm-5.3', 'fcl'): 1})`,
i.e. 19 of the 20 codes are in that cell). The ninth PARTIAL carrying
`INCOMPLETE_GENERATION` is outside the cell:

- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep2.json` — `status: PARTIAL`, `failure_type: INCOMPLETE_GENERATION`, `provider_status: INCOMPLETE_GENERATION`, `finish_reason: length`, `completion_tokens: 32768`.

The count arithmetic in (a) balances either way (11 + 9 = 20), which is exactly
why the misplacement is invisible to anyone who checks only the count. Checked
against the cell directly: `deepseek-flash x fcl receipts: 20 / FAILED: 11
PARTIAL: 8 COMPLETE: 1 / INCOMPLETE_GENERATION in cell: 19`.

**(d) "the provider raising it on both" — survives for the nine PARTIAL; the
record does not support it for the eleven FAILED.** On all nine PARTIAL receipts
(the eight in the cell plus the one named above) the receipts record
`provider_status: INCOMPLETE_GENERATION` — the provider side of the exchange is
captured and does raise it. On all eleven FAILED receipts every provider-side
field is null — `provider_status: null`, `finish_reason: null`, `usage: null`,
`returned_model: null` (script lines `FAILED with provider_status non-null: 0`
and the per-coordinate `usage_null=True` list in the tail script). On the
receipts themselves, `INCOMPLETE_GENERATION` for the eleven sits in the
receipt's own `failure_type` field, and the same §4 paragraph attributes the
eleven to validation ("`NO_PUBLIC_CONTENT`: 11 in C001 occurrence-01, the
validation code on the eleven empty deliveries"), which matches the receipts'
`validation_failure_type: NO_PUBLIC_CONTENT`. The receipts neither confirm nor
deny what the provider said over the wire on those eleven calls — they record
nothing provider-side — so the clause is unsupported for the FAILED eleven, not
contradicted by them.

**Verdict: REFUTED IN PART.** The count (a) and the FAILED attribution (b)
survive. The PARTIAL attribution (c) is refuted by
`ollama-glm-5.3/fcl/control/rep2.json`, and the provider clause (d) is
unsupported for the eleven FAILED receipts named under (b).

---

## CLAIM 2 — SURVIVES

> "`INCOMPLETE_GENERATION`: 7 in F001 v1, every one at `finish_reason: length`
> and exactly 8,192 completion tokens, five returning zero bytes". ("F001 v1" is
> occurrences 01 to 06.)

Script output over the 63 v1 receipts
(`failure_code counts in v1 (None = no failure): {None: 56, 'INCOMPLETE_GENERATION': 7}`),
per coordinate:

| coordinate | status | finish_reason | completion_tokens | artifact_sha256 |
|---|---|---|---|---|
| occurrence-04/daily/mini_fcl/cycle01/objection | FAILED | length | 8192 | null |
| occurrence-04/daily/mini_fcl/cycle01/rival | FAILED | length | 8192 | null |
| occurrence-04/daily/mini_prose/cycle01/objection | PARTIAL | length | 8192 | present |
| occurrence-04/daily/mini_prose/cycle01/response | FAILED | length | 8192 | null |
| occurrence-05/daily/mini_fcl/cycle01/response | FAILED | length | 8192 | null |
| occurrence-05/daily/mini_fcl/cycle01/rival | PARTIAL | length | 8192 | present |
| occurrence-05/daily/mini_prose/cycle01/carry | FAILED | length | 8192 | null |

**(a) "7 in F001 v1" — survives** (7 of 63; occurrences 07–08 carry two
`TRANSPORT_OR_RESPONSE_ERROR` and no `INCOMPLETE_GENERATION`, context only).
**(b) "every one at finish_reason: length" — survives** (`at finish_reason 'length': 7`).
**(c) "exactly 8,192 completion tokens" — survives** (`at exactly 8192 completion tokens: 7`).
**(d) "five returning zero bytes" — survives on the markers the record actually
carries, with a stated limit.** Exactly five of the seven carry no
`artifact_sha256` (the five FAILED rows above), and exactly the two PARTIAL rows
carry one — i.e. five calls left no captured payload and two left a partial one,
matching "five returning zero bytes". The limit: this sandbox slice of F001
contains **no** delivered-bytes files at all (`*.txt sibling files anywhere
under F001: 0`), so a byte count cannot be measured directly for the F001 seven;
the clause is corroborated by the absent/present artifact markers and the
FAILED/PARTIAL statuses, all named above, and I could not verify the byte figure
itself from this slice because the bytes are not in it. On the evidence present
there is no coordinate that refutes the clause.

**Verdict: SURVIVES.**

---

## CLAIM 3 — SURVIVES

> "C001 occurrence-01: `envelope_repairs` on 93 of 240 calls
> (`strip_outer_code_fence` 92, `json_strict_false` 1) against
> `strict_parse_would_succeed` 122 of 240".

Script output over the 240 receipts:

- `envelope_repairs non-empty: 93`
- `repair-name counts (flattened): {'strip_outer_code_fence': 92, 'json_strict_false': 1}` — and `receipts with more than one repair entry: 0`, so 92 + 1 = 93 with no double-counting. The single `json_strict_false` is at `ollama-glm-5.3/prose/carrier/rep4` (`json_strict_false coordinates: ['ollama-glm-5.3/prose/carrier/rep4']`).
- `strict_parse_would_succeed true: 122` (`false: 107`, `null: 11`; the eleven nulls are exactly the eleven FAILED receipts, which have no delivery to decode — their `envelope_repairs` is likewise null, `envelope_repairs null (no delivery to decode): 11 / statuses ... Counter({'FAILED': 11})`).

Cross-tab printed by the tail script for completeness:
`(status, strict_parse_would_succeed): {('COMPLETE', True): 122, ('COMPLETE', False): 98, ('PARTIAL', False): 9, ('FAILED', None): 11}` — sums to 240 —
with `repaired and strict false: 93`, `unrepaired delivered and strict false:
14`, `unrepaired delivered and strict true: 122`. The claim's wording "93 of 240
calls" matches the receipts literally (93 receipts with a non-empty repair list
out of all 240), and 122 + 107 + 11 = 240 on the strict side.

Note: the one `json_strict_false` repair sits on the **prose** arm of
`ollama-glm-5.3` (carrier/rep4), not to be confused with the similarly shaped
occurrence-02 repair the report mentions elsewhere (`control/rep2`) — that is a
different occurrence and no conflict. Both figures as claimed are reproduced by
the run.

**Verdict: SURVIVES.**

---

## Which clauses the record does not support

1. **Claim 1, clause "the nine PARTIAL of the `deepseek-flash` x `fcl` cell":
   not supported (refuted).** The cell carries eight PARTIAL; the ninth is
   `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep2.json`
   (`status: PARTIAL`, `failure_type: INCOMPLETE_GENERATION`,
   `completion_tokens: 32768`). The totals still sum to 20, which conceals the
   misattribution from any count-only check.
2. **Claim 1, clause "the provider raising it on both": not supported for the
   eleven FAILED.** Those eleven receipts (named in the claim-1 table above)
   carry `provider_status: null` and `failure_class: ProviderFailure` with
   `validation_failure_type: NO_PUBLIC_CONTENT`; every provider-side field is
   null, so the receipts show the provider raising it on the nine PARTIAL only.
3. **Claim 2: the record supports every clause** via the seven receipts tabled
   above, with the stated limit that F001 delivered-bytes files are absent from
   this sandbox slice, so the "zero bytes" clause rests on the five null
   `artifact_sha256` markers rather than on a measurable byte count.
4. **Claim 3: the record supports every clause** (93 = 92 + 1; strict true 122;
   breakdowns and the cross-tab above).

## Incidental observation (not one of the three claims; surfaced by the same runs)

While checking claim 1 clause by clause, the tail script also recomputed the
figures the report's §2 states for the same cell. §2 says "19 of its 20
coordinates carry `completion_tokens` exactly 8,192 ... of which eleven spent
the *entire* ceiling on reasoning (`reasoning_tokens` 8,192) ... while the other
nine spent 5,488–7,890 on reasoning". The receipts read: **8** of the 20 cell
coordinates carry `completion_tokens: 8192` (the eight PARTIAL, `reasoning_tokens`
5,923–7,890 — not 5,488), and the eleven FAILED coordinates carry `usage: null`
with no `reasoning_tokens` recorded at all (`deepseek-flash x fcl at
completion_tokens 8192: 8 of 20 / with reasoning_tokens == 8192: 0 / with usage
null: 11`; per-coordinate list printed by `python3 check/refute_claims_tail.py`).
I could not determine which figure was intended for occurrences outside this
sandbox slice; within the record here, that §2 sentence is not supported. This
observation is a by-product of the claim-1 aggregation and touches none of the
three claimed sentences themselves; the neighbouring §2 figures that *are*
rechecked here and do hold are: deepseek-flash x prose 20 of 20 COMPLETE at
3,621–6,985 completion tokens, and 29 of 40 deepseek-flash receipts with
`reasoning_content_present: true`.
