# UC3 P-A3 offline validation - 2026-09-17

Status: **PASS**. Two actual-CLI offline fixture passes completed with 8 logical calls, zero provider calls, exact compact input references, scoped pinned reads, byte-range quote locators where the selected route reads evidence, and CONTINUE then STOP decisions tied to actual verification references.

The recorded live failure addressed by P-A3 was `OUTER_INPUTS_MUST_MATCH_SEALED_TASK`. This fixture verifies interface, custody, repair-compatible source delivery and task loading only; it does not establish live reliability or semantic success.

Exact calls, source hashes and limits: [OFFLINE-VALIDATION-PA3.json](OFFLINE-VALIDATION-PA3.json). Fresh custody: `work/w46/offline-custody-final/UC3`. Historical validations remain unchanged. The superseded first P-A3 fixture output is retained under `work/w46/initial-pa3`.
