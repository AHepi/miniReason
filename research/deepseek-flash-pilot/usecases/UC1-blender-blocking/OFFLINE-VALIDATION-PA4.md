# UC1 P-A4 offline validation - 2026-09-17

Status: **PASS**. Two actual-CLI offline fixture passes completed with 8 logical calls, zero provider calls, exact compact input references, scoped pinned reads, byte-range quote locators where the selected route reads evidence, and CONTINUE then STOP decisions tied to actual verification references.

The recorded live failure addressed by P-A4 was `CEILING_HIT at pass2 planner c0007/a00 (4096 tokens)`. This fixture verifies interface, custody, repair-compatible source delivery and task loading only; it does not establish live reliability or semantic success.

Exact calls, source hashes and limits: [OFFLINE-VALIDATION-PA4.json](OFFLINE-VALIDATION-PA4.json). Fresh custody: `work/w47/offline-custody-final/UC1`. Historical validations remain unchanged. Earlier P-A3 qualification remains under `work/w46/offline-custody-final`.
