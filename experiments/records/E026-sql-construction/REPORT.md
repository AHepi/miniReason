# E026 SQL construction: interrupted original run

The unchanged six-arm construction plan was dispatched on 2026-09-12 at 21:01:20 UTC. The first arm returned a complete public account. The second arm consumed its completion-token allowance without a public answer, and the frozen fail-stop runner left the remaining four arms unattempted. This record is an operational interruption, not a completed comparison or a failed Mini construction.

| Arm | Outcome | Prompt tokens | Completion tokens | Total tokens |
|---|---|---:|---:|---:|
| direct-disabled | Complete public response; stop | 796 | 4115 | 4911 |
| direct-native | Empty public answer; length; INCOMPLETE_GENERATION | 821 | 8192 | 9013 |
| prompt-control-disabled | Unattempted | — | — | — |
| prompt-control-native | Unattempted | — | — | — |
| mini-disabled | Unattempted; preselected occurrence unavailable | — | — | — |
| mini-native | Unattempted | — | — | — |

Known reported usage is 13,924 total tokens, including 12,307 completion tokens. The native response reports all 8,192 completion tokens as reasoning tokens. Hidden reasoning text was discarded as specified. The recorded request keeps thinking enabled with low effort and max_tokens 8192; a resource ceiling does not establish semantic incapacity. The generic failed-arm summary says unreturned usage is unknown, but the original provider response contains the reported usage shown here. Preserve both original records; this report resolves their different granularity without rewriting them.

Plan identity is f8c3ab9ecb3285ea3d1d167427e413be2a30a1583a05fd5a411210430390a197. The original provider request hashes match the frozen direct-disabled and direct-native requests. Returned model is deepseek-flash for both. All 24 focused offline tests and exact frozen verification passed before dispatch; renewed evidence is in ../../preflights/E026-session-H-verification. The live CLI exited zero while summary.json correctly recorded INTERRUPTED, so shell status is insufficient to establish study completion.

The direct-disabled prose proposes keyed retained state, multiplicity-sensitive updates, and a distinction between NULL padding and actual matched NULL values. This is a description of its public proposal, not an executed correctness or explanatory-bearing verdict. The preselected Mini candidate never ran and cannot be replaced by this direct answer. No model output is supplied to an unattempted construction arm, and no B initialization/use/return bridge exists.

The immediate next decision is a separately frozen continuation for unattempted disabled-reasoning arms with unchanged original request bytes. Original completed or failed calls must not be replayed or overwritten. Native resource remediation remains a separate decision; no higher budget or automatic retry is selected in this report. Any later continuation has a new execution identity and must disclose changed scheduling. Publish this original record before preparing it.
