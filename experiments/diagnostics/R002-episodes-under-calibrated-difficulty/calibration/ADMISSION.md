# R002 calibration admission

Guarded reader: Codex root-w21 (OpenAI lineage, distinct from DeepSeek); read UTC 2026-09-16T23:57:01.109085+00:00. Decision REC-20260917-A. All24 calls were already complete; this reading made no provider/model endpoint call.

**Admitted: C05, C06, C09, C12.** Target8; actual4. Counts:20 correct,0 incorrect,4 not answered (`no_answer`),0 unresolved;0 nonterminal or custody-incomplete trials.

PLAN section2 is applied in C01..C24 order. CEILING_HIT with no usable final answer is eligible. Only four candidates qualify, so the pre-registered1-7 underfill rule applies: use all four as an explicitly underfilled diagnostic, with no replacement and no second pilot. Zero-admission stopping does not apply. All four are computable; no derivation-only case qualifies and that contrast is unavailable.

| Candidate | Verdict | Admitted | Reason |
|---|---|---|---|
| [C01](C01.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C02](C02.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C03](C03.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C04](C04.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C05](C05.md) | not answered | yes | CEILING_HIT/length; empty final content; selected under underfill rule. |
| [C06](C06.md) | not answered | yes | CEILING_HIT/length; empty final content; selected under underfill rule. |
| [C07](C07.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C08](C08.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C09](C09.md) | not answered | yes | CEILING_HIT/length; empty final content; selected under underfill rule. |
| [C10](C10.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C11](C11.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C12](C12.md) | not answered | yes | CEILING_HIT/length; empty final content; selected under underfill rule. |
| [C13](C13.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C14](C14.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C15](C15.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C16](C16.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C17](C17.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C18](C18.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C19](C19.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C20](C20.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C21](C21.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C22](C22.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C23](C23.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |
| [C24](C24.md) | correct | no | Every requested fact and proof obligation satisfied; ineligible. |

## Evidence and operational outcome

24 calls /24 attempts, one native DeepSeek Flash call per candidate, requested medium effort,32768 completion and300s wall, no retries.20 stop/complete responses and4 length/CEILING_HIT responses. Known usage:24995 prompt +363057 completion =388052 total tokens;344049 reasoning tokens are included in completion. Provider elapsed sum1384.867s; supervised-worker elapsed sum1392.677s; maximum provider elapsed137.296s. No wall breach, nonterminal trial or custody gap was found.

All700 trial files were copied byte-for-byte to [runs/calibration](../runs/calibration/), with two original phase/manifest provenance copies and [SHA-256 manifest](../runs/calibration/SHA256-MANIFEST.json). All72 problem/answer/oracle-output source pins match. Longest absolute copied path155 characters. Credential-name occurrences are names only; the custody scan found no credential value or secret-shaped string and no native hidden reasoning text. No .env was read.

The launcher-compatible [admission.json](admission.json) contains all24 records, source/reference hashes and decisive quotations. For no-answer cases, native_final_answer_path/hash are null because no participant final exists, while answer_file_read_path/hash bind the actual ANSWER.md harness placeholder that was read. [Source phase receipt](../runs/calibration/SOURCE-CALIBRATION-PHASE-RECEIPT.json) and [source manifest](../runs/calibration/SOURCE-RUN-MANIFEST.json) are exact copied bytes; their embedded original directory references remain unchanged.

## Claim boundary and next gate

This is admission selection evidence only. It does not show an oracle-wrong native answer, correction, blindness, comparative advantage or a general success rate. Pilot outputs must never be reused as main inputs; main NATIVE must be fresh. Main launch is not authorized by this reader: independent judge/publisher handoff and reviewed dynamic tokenizer pins remain, as specified in work/w21/MAIN-LAUNCH.md. Keep PLAN and its pre-registered sections unchanged. Reopen for a concrete requested-fact/proof/custody discrepancy, recording a separately named correction.
