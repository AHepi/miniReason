# H003 preparation: oversized Windows command

Recorded 2026-09-13 under REC-20260913-K. This supplement concerns local material preparation, before H003 provider execution.

| Item | Recorded incident and action |
|---|---|
| Symptom | A single material builder of approximately 61,221 characters embedded in a shell command failed before process creation with Windows error 206: `filename or extension too long`. |
| Cause / boundary | The oversized command failed at process launch. The builder did not execute: that failed command made no file mutation and no provider attempt. This is distinct from the earlier sandbox ACL setup failure, directory-fsync incompatibility and GitHub permission denials. |
| Successful workaround | Root first verified that the intended output was absent, then wrote the exact builder as ordered literal string segments of 10,000 characters using native PowerShell `AppendAllText`. Root executed the completed builder successfully and subsequently reviewed material hashes and finite expectations. |
| Avoid repeating | Keep shell invocations bounded. For large generated content, assemble a file from exact literal segments, preserving order, encoding and newlines, then invoke the completed file with a short command. Check whether a partial file exists before appending; never blindly repeat chunks into it. Preserve and identify any partial output instead of overwriting frozen evidence. |

The segment size describes the successful workaround on this host; it is not a universal Windows command-length guarantee. Do not retry the same oversized command, infer repository corruption from the launch error, or count it as a failed model call. File construction and later provider dispatch remain separate operations with their own evidence and publication gates.

Evidence: [decision ledger](../DECISION_LEDGER.md), REC-20260913-K root-freeze receipt at 10:26:30 UTC and operational-guidance drafting receipt at 10:30:12 UTC; root's incident handoff supplies the approximate builder length, absence check and literal segment size. See the earlier [Windows execution guide](REC-20260913-windows-execution.md) for the distinct failures. This document records root's preparation outcome; it does not independently appraise the material or its semantic expectations.

Root reviewed and accepted this operational classification on 2026-09-13 against the actual launch failure and successful bounded file construction. Astra drafted the supplement; root retains all review responsibility.
