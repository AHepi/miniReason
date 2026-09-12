# E025: renewed automatic disclosure rejection

The E025 handoff, frozen plan and actual-material preflight were published before dispatch. The prior ledger R20260912-09 records explicit user approval to send the published experiment material and generated outputs to the DeepSeek endpoint. Nevertheless automatic approval review rejected the running-process polling action, stating that repository-derived handoff content would be disclosed to an untrusted external DeepSeek API without explicit approval.

The current attempt stopped. Inspection found no surviving runner. Five request records exist, along with one zero-byte response file and no terminal summary. No complete response, token count or semantic outcome is available. The action that triggered the review was polling; the reason concerns the underlying experiment disclosure. No causal claim about provider/network behavior follows from that rejection.

An initial progress read counted one response path. That did not establish a completed response; subsequent parsing/byte inspection corrected the interpretation. Future progress observations must distinguish paths, parseable complete records and terminal run status. The failed JSON read was a diagnostic error, not a provider observation.

All 31 original files are hashed in [the recovery record](../../experiments/records/E025-chain-successor/recovery.json) and remain unchanged. No alternative execution route, automatic retry or successor dispatch was used. The [fresh-attempt declaration](../../experiments/attempts/E025-retry-01.json) preserves the same frozen plan and uses a separate absent output directory.

The remaining approval concerns sending the declared source packet and model outputs to https://api.deepseek.com/v1/chat/completions for that ten-call attempt. Automatic review, rather than a project skill requiring redundant consent, is the source of this renewed boundary. Do not overwrite E025 or repeat E023/E024. After explicit approval, recheck the frozen plan/source identities and output-path absence, then run the declared fresh attempt once and publish the actual outcome.

This is an operational erratum. It supplies no result on the successor configuration, problem promotion or ECS.
