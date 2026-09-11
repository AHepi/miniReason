# Operational lessons

The DeepSeek key is available through the process environment and is never part of a configuration identity. Successful model discovery is a transport preflight only; it does not show that generation or a configuration experiment completed.

An interrupted or truncated response must remain visible as an operational failure. Omitting it from comparison denominators can create an apparent advantage for whichever arm failed to return usable output.

E001 recorded three native-mode calls ending at exactly 8192 completion tokens with length termination. This is an insufficient completion allowance for those responses, not evidence that the model cannot solve the task. E002 changes that ceiling alone and preserves the failed E001 observations.

E002 shows why resource changes need separate records: a larger allowance made one previously unavailable native answer assessable while a different native arm still truncated. Provider completion tokens include native reasoning expenditure; equal per-call ceilings are not equal realized budgets. Keep both observations and the one-repetition limitation.

The E009 recovery in OPS-008 shows that an uploaded tree checkpoint, a local commit and a published branch are distinct states. Resume by verifying the remote parent and final tree, reuse content-addressed objects where possible, and checkpoint progress without advancing main until the full reviewed tree is available. Preserve separate local/remote commit identities when the authenticated connector assigns different commit metadata. Refresh STATUS from terminal records and later reviews; never revise an archived observation just to make its historical state look current.
