# UC2 P-A2 offline validation - 2026-09-17

PASS: 2 passes; 8 logical calls / 8 physical fixture attempts; zero provider calls and zero token usage.
The recorded decisions are CONTINUE then STOP, both citing actual runtime verification.

Actual entrypoint: `minireason.pilot.__main__.main` in offline mode. The CLI loads the real task file and an empty scripted-list seed; a disclosed constructor wrapper supplies the callable fixture needed to cite runtime verification hashes. This is the same kind of offline seam used for P-A1 qualification.

Task SHA-256: `f00d45a4ce258d523f9d445d13c0dfc80ed89f150e6c84016ce6b2f21ef02607`. Before/after source and task hashes are equal. Compact spawn references, frozen unit hashes, scoped read offsets/excerpt hashes, per-call source delivery, accepted request preflight, prepared/provider would-send wire equality and artifact/verification references all pass.

Exact call summaries and source hashes: [OFFLINE-VALIDATION-PA2.json](OFFLINE-VALIDATION-PA2.json). Durable full custody: `work/w45/offline-custody/UC2`; aggregate transcript: `work/w45/offline-validation-pa2-20260917T124557446514Z.log`.

The original OFFLINE-VALIDATION files and sealed briefs/manifests remain historical and unchanged. These scripted outputs establish interface/custody behavior only, not answer quality, FW5 comprehension, Blender runtime correctness, or live provider reliability.
