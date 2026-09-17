# R002 A1 implementation map

Registered 2026-09-17T00:51:01.057733+00:00 before any main-phase participant call. See [PLAN A1](PLAN.md) and the appended [reading protocol](READING_TEMPLATE.md).

LOOP-DECOMPOSED uses three cycles, one step each: native INITIAL-DECOMPOSE; off STEP for subsequent steps; one tested critic (Qwen/GLM/Qwen), native current-step return and off use in each cycle; native SYNTHESIS only after the complete plan is accepted. Limits: plan<=8, goal<=256 characters, derivation<=2000, result<=512. A plan exceeding three steps remains partial. Strict failures retain evidence and never fall back.

Maximum completed route:13 calls,5 native plus8 off,294912 completion tokens. All six main conditions on C05/C06/C09/C12 allow280 attempts and6291456 completion tokens. Input cap32768 uses the reviewed bound descriptor or qualified tokenizer; wire-byte qualification and provider-rendering premises are documented separately. No host checker execution is added to this arm.

Engineering surfaces: `src/minireason/reason/r002.py`, `r002_reports.py`, `config.py`, `prompts.py`, `r002_custody.py`, `r002_preflight.py`, `r002_launcher.py`; new `recipes/r002-decomposed-v1.json` and decomposed contracts. Existing recipes/contracts and calibration observations remain frozen. The engineering record, tests, capability successor and future detached command are indexed in `work/w22/INDEX.md`; that command is documentation, never dispatched by this task.

Acceptance/synthesis are plumbing states, not a semantic verdict. A later independent reader must establish final correctness, any decomposition escape and each substantive critical episode. Fresh main NATIVE and unmatched resource differences remain visible.
