# Continue the inquiry

Read [DECISION_LEDGER](../DECISION_LEDGER.md) first, then [README](../../README.md), [PURPOSE](../../PURPOSE.md), [AGENTS](../../AGENTS.md) and [STATUS](../STATUS.md). The current initial question is what model-proposed languages and semantic classes let Mini express and do under actual material and resource conditions, and which components expand or hinder that process. Initial correctness or adequacy is not an admission requirement. Lean-oriented, other formal and non-Lean schemes are legitimate specimens; prose conjectures and criticisms retain full semantic legitimacy.

## Restart after a failed window

Locate the last publication receipt in the ledger and the completed and pending work in STATUS. Record a recovery decision before acting. Its receipt must state what will be recovered, why, how it advances the project purpose, and which evidence will establish completion. Preserve unexpected user changes and all untracked records. Do not reset, clean, overwrite partial reviews, or rerun completed experiments to compensate for a failed publication.

From the surviving repository root, inspect the local state without changing it:

```sh
git status --short --branch
git branch --show-current
git log -1 --format='%H %T %P %s'
git diff --stat
git diff --cached --stat
git ls-files --others --exclude-standard
```

Match the local commit and tree to the ledger's intended publication checkpoint; do not assume the current HEAD is that checkpoint. Inspect any saved publication progress and the exact reviewed path set. A run can be complete while its upload, review or publication remains incomplete. Preserve original partial reports unchanged, even when they contain stale in-progress statements. Put the recovery assessment or completed review in a separately named file that identifies the original and distinguishes fresh findings from recovered ones.

Read the actual remote `refs/heads/main` and its commit's tree through the authenticated GitHub connector, or fetch it through Git when that route works:

```sh
git fetch origin refs/heads/main
```

Only if that fetch succeeds, inspect the fetched remote identity:

```sh
git log -1 --format='%H %T %P %s' FETCH_HEAD
```

A failed fetch does not refresh `FETCH_HEAD`; never use an old value as current remote evidence. If Git authentication is unavailable, use the connector's independent authentication under [the publication workflow](publish.md). Record the read route and observed remote commit and tree in the recovery receipt. Do not print credential-bearing remote URLs or credentials.

For an ordinary push, verify that remote `main` points to the intended published commit. A connector can create a different commit because its parent or commit metadata differs. In that case, compare the remote commit's tree SHA with the intended local checkpoint's tree SHA. Exact equality establishes identical tracked paths and bytes; it does not establish identical commit history. Record the local commit, remote commit, shared tree and remote-main confirmation. If remote main has advanced, inspect its ancestry and intervening changes before choosing an integration; do not overwrite them or infer publication from a similar commit message.

When publication is incomplete, finish the existing reviewed checkpoint without altering completed evidence, using a normal non-forced update. A partial tree upload or a created commit without a verified main reference is still pending. Append failure and recovery outcomes to the ledger and preserve enough progress to resume, including the intended local commit/tree, observed remote base, created tree or commit identities, remaining paths, and verification state. Keep these receipts free of credentials. No successor experiment starts until the completed predecessor's publication is verified.

After verification, append the publication outcome and update STATUS with completed work, unresolved reviews or code, and the next authorized action. Publish this recovery receipt at the next small checkpoint. A receipt cannot contain its own commit identity in advance: the publisher reports that checkpoint's verified commit externally and records it in the next ledger entry. Never label an attempted push as successful.

## Continue the research

Read the latest frozen experiment plan, original proposal bytes, complete unsuccessful records as well as successful ones, and relevant errata and lesson files. Read [Language Proposal Theorems](../LANGUAGE_PROPOSAL_THEOREMS.md) and [Problem promotion](../PROBLEM_PROMOTION.md) before changing the study's interpretation or integration rules. Use [the research agenda](../RESEARCH_AGENDA.md) to select a mechanism-specific successor; its proposed construction configuration is not implemented by the expression-only runner.

Before each new choice, append a ledger receipt stating the choice, why it was made, how it contributes to the end goal, and its pending state or evidence. This applies to design, implementation, experiment selection, interpretation, delegation, publication and stopping decisions. Append dated outcomes and corrections instead of changing earlier receipts; mechanical executions belong under the decision they implement. One publisher serializes ledger edits, commits and pushes. Delegated agents send their new decision receipts to that publisher before acting. Publish reviewed receipts and recoverable artifacts in small main checkpoints throughout the work, including after failed or interrupted tests.

Recover the stage of the research. First proposals are frozen for their initial trials. Preserve each scheme's initial text, interpretation or undeclared maps, model settings, tools, rendering, inputs and resource conditions. Do not silently repair a specimen before measuring what it allows or obstructs. Later adaptations are separately identified successor experiments with an explicit parent, changed component and reason. A revised interpretation, grain, boundary or task creates a new claim; it does not rewrite the earlier result.

Reconstruct what actually ran. A directory, compiled manifest, provider smoke check or mocked response is not a completed model comparison. Verify call records and the Mini log, the declared observation route and whether there was an interruption. A non-executable semantic proposal can still be a completed specimen for an expression study. Conversely, a missing terminal record is an interrupted run, never a negative verdict about the proposal's semantic content.

Choose the next experiment because a particular expression, use or failure mechanism remains unresolved. State what differs from its parent, what should happen if the diagnosis is right, what would defeat it and which control receives equivalent information and allowance. Keep the bare model, candidate Mini and supported native-reasoning comparisons essential. If an earlier proposed language or operative artifact is supplied as a starting point, give the same selected bytes and evidence to the relevant arms under a declared selection rule.

Freeze task, proposal/template, interpreter and measurement identities before sending. Preserve original prose alongside any attempted formal translation, and let criticisms of the language itself enter even when its own syntax cannot encode them. Distinguish a lost distinction in one route from inability of the whole system. Do not use a progress meter, a syntax-only adequacy gate or random template mutation to choose successors.

Keep prompts and mutable state isolated between concurrent configurations. At most five configuration tests may run at once. Run appropriate offline instrument checks before spending tokens; these checks do not require every proposal to have an executable form. Load the authorised DeepSeek credential only into the process environment and keep it out of shell output and repository content. Follow [experiment](experiment.md), then [publish](publish.md) immediately after each test finishes.

When there is a blocker, name it precisely and preserve reviewable work. When stopping by judgement, state the failed and surviving mechanisms and why the remaining concrete interventions lack a distinguishing rationale under the available conditions. Missing native outputs, absent tools or an uncompleted translation are scoped limitations, not evidence that scientific options are exhausted. A finite campaign never literally exhausts every possible configuration or representational scheme.
