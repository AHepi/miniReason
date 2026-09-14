# Workflows

Use [continue](continue.md) at session start, [experiment](experiment.md) before and after every configuration test, and [publish](publish.md) for durable publication. These workflows answer where to look and where to add evidence; they do not restrict which hypotheses may be considered.

| Situation | Read | Write |
|---|---|---|
| Resume | PURPOSE, STATUS, latest plan, last published records | STATUS with verified next action |
| Collect initial proposals | PURPOSE, language-proposal propositions, method | Original frozen scheme and material conditions; no adequacy admission gate |
| Design a configuration or later integration | Semantic guide, method, problem promotion, relevant errata and lessons | New causal rationale and immutable successor plan/template |
| Run fails | Wire request, answer, actual Mini ports, checker trace | Erratum with causes and uncertainty |
| Learn something transferable | Evidence and competing explanations | Appropriate lesson file |
| Compare arms | Exact inputs, mode, calls, tokens, chronology, repeated controls | New comparison with narrow claims |
| Test finishes | Full record and diagnosis | Immediate main commit and verified push |
| Stop or hand over | Untried mechanisms and outstanding confounds | Honest stopping rationale and reopening conditions |
| Re-express a finished occurrence in the harness-spec vocabulary | [graph-import-h005](graph-import-h005.md), the occurrence's own artifacts, attempts, receipts and traces | Offline import report, residue table and custody ledger; no label it computes is a semantic attribution |
| Read what a finished occurrence's authors declared about using one another | [use-relation-h005](use-relation-h005.md), the occurrence's own FCL-1 commitment surfaces, the passages it quotes | Offline juxtaposition table whose four interpretive cells root fills by reading; the instrument classifies nothing, and a lexical overlap is not evidence of use |
| Call a declared endpoint other than the DeepSeek arm's | [provider-openai-compat](provider-openai-compat.md), `src/minireason/data/endpoints.json` and the credential environment names it declares | Write-once request and response records outside the repository, request bytes hashed before the send, credentials redacted on write; `src/minireason/provider.py` remains the DeepSeek arm's transport and is not touched |
| Run one frozen fork5 invocation across several model families | [fork5-multifamily](fork5-multifamily.md), the F001 register `experiments/diagnostics/F001-fork5-multifamily/PLAN.md` and each occurrence's frozen `arms.json` | One occurrence per family, published before every dispatch, at most five concurrent requests per credential and no retries; mechanism-level counts only, and no cross-family merit reading is made from them |
| Raise a frozen study's completion ceiling after a truncated run | [fork5-multifamily](fork5-multifamily.md) § *The v2 successor runner*, the register's successor section and the earlier occurrences’ audits and receipts | A successor runner file with its own `runner_sha256`, never an edit to the published one; its difference list declared in its header, marked in its source and proved by a diff test; the ceiling declared per arm in `arms.json`; new occurrences beside the old ones, which are never re-sent, relabelled or superseded |
| Deliver one criticism in four codings to one responder node and publish the replies unread | [contrast-triple](contrast-triple.md), the `C001-contrast-triple` register `experiments/diagnostics/C001-contrast-triple/PLAN.md` (not the E024/C001 template-chain occurrence), its `material.json` and its 85-row `RECODING_TABLE.md` | The correspondence table and the frozen plan published and the remote verified BEFORE the first call; only the objection block varying, checked mechanically; per-endpoint ceiling and wall-clock timeout applied to the resolved Endpoint without editing the pinned `endpoints.json`; mechanical columns and raw juxtapositions only, with root's reading columns rendered empty and left empty |

The active original runner has a dedicated [frozen language workflow](language-study.md), including setup ordering, controls, withheld-source limits and publication points.

The [construction inquiry workflow](inquiry-study.md) continues from a whole frozen issue occurrence into construction, criticism, proposed revision and unresolved promotion. Use it for the first P7/P9 inquiry block and later separately justified selections. Selecting an issue is recorded as an allocation decision; the route neither installs a successor automatically nor assigns semantic standing.

The [reason-use workflow](reason-use.md) compares supplemental criticisms on fixed J and tests isolated account use against an explicit no-return control. Its design amendment and limitations are frozen separately from the earlier four-stage studies.


The [distinct-template continuation workflow](template-chain.md) covers the prepared E023 control, E024/C001 construction-to-successor chain, exact published handoff, six downstream controls and no-promotion outcome. The [activity log](../AGENT_ACTIVITY.jsonl) records every agent repository search/read/modification; use tools/repo_activity.py for atomic begin/outcome receipts. Read STATUS before execution: live dispatch remains blocked by automatic approval review pending explicit DeepSeek destination/disclosure approval.
