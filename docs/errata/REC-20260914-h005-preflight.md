# H005 preparation incident — 2026-09-14

REC-20260914-B. This is a preparation failure, not a provider result.

The implementation agent reported that its first complete helper-file write was rejected before process creation with Windows error 206 (command or filename too long). No helper bytes were written by that command and no H005 provider request had begun. The proposed helper draft was about 700 lines.

The existing Windows recovery guide already warns about command length. The immediate recovery is native PowerShell writes split into commands below 10,000 characters, using a first WriteAllText followed by ordered AppendAllText calls. Root will not import or accept an incomplete chunk sequence. Source and old observations remain unchanged.

Do not resend a giant shell argument, change shells to evade the boundary, weaken filesystem durability, or treat this failure as evidence about the language or template. Keep multiline content literal and credentials absent. After the final chunk, inspect the resulting file, run the focused offline checks, and let root perform acceptance review before freezing any live occurrence.

This incident shows that having a skill installed is insufficient unless the demonstrated limit is applied at the write boundary. Future H005 implementation delegates should receive the chunk-size constraint explicitly as well as the required guide.
