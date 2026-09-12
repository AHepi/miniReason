# Operational lessons

The DeepSeek key is available through the process environment and is never part of a configuration identity. Successful model discovery is a transport preflight only; it does not show that generation or a configuration experiment completed.

An interrupted or truncated response must remain visible as an operational failure. Omitting it from comparison denominators can create an apparent advantage for whichever arm failed to return usable output.

E001 recorded three native-mode calls ending at exactly 8192 completion tokens with length termination. This is an insufficient completion allowance for those responses, not evidence that the model cannot solve the task. E002 changes that ceiling alone and preserves the failed E001 observations.

E002 shows why resource changes need separate records: a larger allowance made one previously unavailable native answer assessable while a different native arm still truncated. Provider completion tokens include native reasoning expenditure; equal per-call ceilings are not equal realized budgets. Keep both observations and the one-repetition limitation.

The E009 recovery in OPS-008 shows that an uploaded tree checkpoint, a local commit and a published branch are distinct states. Resume by verifying the remote parent and final tree, reuse content-addressed objects where possible, and checkpoint progress without advancing main until the full reviewed tree is available. Preserve separate local/remote commit identities when the authenticated connector assigns different commit metadata. Refresh STATUS from terminal records and later reviews; never revise an archived observation just to make its historical state look current.

E019 in OPS-011 distinguishes an observed provider failure, a cancelled execution approval and a missing driver summary. Preserve the original per-call receipts and partial logs, and describe the captured state in a separately named recovery record. Successful earlier stages remain evidence; absent terminal summaries must not erase them or be replaced with invented completion. Unknown failed-call costs remain unknown. Prepare a distinct retry offline if useful, but an unchanged plan or a fresh window does not itself restore cancelled access.

A recorded network approval rejection can concern the classification of an outbound payload rather than provider semantics. Preserve it verbatim and retain partial files; check immutable public source evidence when the review permits that check. Public-source proof is evidence to present through normal review, never a reason to route around an access decision.


E022's completed local commit still required eight upload batches before it became durable on main. The publication boundary therefore applies to each completed document as well as each experiment: publish and verify it immediately, carrying its decision receipt and current continuation state. A review can finish independently of a run, and an original partial review should survive alongside its separately named completion supplement. When a connector creates different commit metadata, exact shared tree and fresh main verification establish content publication.

E020 shows that an earlier successful call through the same endpoint does not establish approval for a later interrupted call. Preserve transport and automatic-review events separately, stop live dispatch after renewed rejection, and finish offline code, tests and review. If unrelated new modules change the repository-wide source digest, a future retry must disclose that new identity while checking that the original task, prompts, provider and controls remain unchanged; never silently edit an old plan to make it runnable.
