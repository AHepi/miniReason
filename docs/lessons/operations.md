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


## E025: a response path is not a completed observation

E025 created one zero-byte response file before its attempt was interrupted. Progress counts must distinguish existing response paths, parseable terminal response records and terminal run completion. File count alone is delivery-process evidence. Preserve empty or incomplete files and unknown usage; do not manufacture a negative semantic result or infer provider receipt merely from a recorded request. A renewed automatic disclosure rejection is recorded separately from prior authorization and provider behavior. See [the E025 erratum](../errata/E025-disclosure-interruption.md).


## E026: distinguish planned selection, actual occurrence and interruption

A preselected arm is not an available candidate until its call actually returns public content. E026 stopped before mini-disabled, so using the successful direct-disabled answer as its handoff would change selection after seeing outputs. A continuation must retain the original selection rationale while naming the new actual occurrence, preserve the missing original occurrence, and report changed scheduling explicitly.

The existing E001/E002 lesson applies again: an equal 8192 completion ceiling can be consumed by native reasoning before any public answer. Preserve that failed resource condition and include it in the study's accounting. Disabled-only continuation can answer a narrower question; it cannot complete the missing native comparison or establish an orchestration advantage. New budget conditions require separate freezing rather than retrospective repair.

A successful shell exit and an existing response path do not establish experiment completion. E026's zero-exit CLI wrote INTERRUPTED, while the failed provider receipt still supplied token usage omitted from the generic arm summary. Use terminal status, public content, finish reason and provider usage together. Exact transport reachability, credential acceptance, complete generation and semantic appraisal are distinct observations.

When an earlier fail-stop prevents independent unattempted arms, freeze a separate minimal continuation instead of replaying successful calls. Keep original request bytes and participant isolation where the scientific condition is unchanged, identify the scheduling intervention, and bind both the parent record and new implementation. The planned E027 does this for disabled arms; its preparation is not itself an observed continuation result.

## H003/H004: continuity, partial delivery, and fallible custody claims

H003's full-delivery guard stopped allfive arms at the4,096-token cap. H004's separately declared admission rule used the actual nonempty prefixes to continue only unvisited coordinates. It reached20steps per arm without replaying H003, yielding50complete/50partial contributions across100calls. A partial-delivery failure under one frozen rule can remain useful content under another explicitly attributed rule; neither rule turns a prefix into a complete answer.

A participant can falsely describe a complete input as truncated or a verbatim old input as reconstructed. Inspect the actual occurrence's request, response, receipt and hashes before diagnosing infrastructure. Do not use the critic's current target list to infer the previous contributor's available evidence. The relevant checks and counterexamples are in the [H004 terminal failure supplement](../errata/REC-20260913-windows-execution.md#h004-terminal-supplement-participant-descriptions-are-not-delivery-receipts).

Five provider slots permit independent dependency-ready arms, while each arm's causal successors remain ordered. H004 reached an observed maximum of five overlapping helper intervals; its tail narrowed as arms finished. One publisher serialized durable Git checkpoints, not allmodel work. Preserve the distinction between local helper timing and server-observed overlap.

Exact-public-byte approval evidence is occurrence-specific. A previously accepted wave is not proof about different new bytes. Present fresh canonical derivation, published-input matches and established destination authorization to normal approval review; preserve any rejection and its resolution. The successful resolution is evidence for that action, not a bypass rule.

H004's final audit checked65new canonical request/trace pairs,100uniquecombined provider coordinates, zero pending markers, preserved source/plan/record trees and4,081tracked/H004files without credential-pattern matches. Its terminal state closes those coordinates; it does not qualify the full durable scheduler or authorize their replay. Reopening requires a separately identified scientific question and occurrence, with unchanged old evidence.


## 2026-09-19 — Running two reasoning models as hostile witnesses

Evidence: the adjudication's §0 in the [cross-examination folder](../reviews/2026-09-19-fable-cross-examination/), the harness and battery files there, and the reply text files. Hidden reasoning text was captured for diagnosis and is not published; only public reply text, usage counts and finish reasons are.

A reasoning model spends its completion allowance on reasoning first. deepseek-flash returned empty content at 6,000 and 24,000 output tokens on a third of items and needed its cap (131,072); Atria-Dawn-Preview returned nothing at 24,000 and its cap is 65,536 (100,000 is rejected). Treat an empty reply with finish reason "length" as a resource failure and rerun at the cap; count it in the accounting either way.

A 600-second read timeout in the harness was raised on the belief that Atria replies took about thirty minutes; the receipts later showed every successful attempt finished in two to five minutes and every failed attempt was closed by the remote end after 306 seconds, four times over. The apparent slowness was a four-worker queue in which each failing item held a worker for 21 minutes. Print every retry; read per-attempt durations from the receipts before diagnosing a provider as slow; launch within the provider's stated rate (60 requests per minute here) rather than a guessed worker count; and stream so that a long reply survives a fixed connection cut. Atria reported burst-rate limits as "Invalid API key" (401); a direct small request succeeding while every harness call failed was the tell.

Both hosts were policy-denied at the egress gateway (403) until the user changed the environment policy; an automatic reviewer then denied one curl carrying the key as exfiltration while the same request from Python was allowed. Preserve both events; neither is a provider observation.

`pkill -f` with the script's name matched the shell issuing it and killed the session twice. Stop a run by scanning process argv for the exact command.

Check that each battery item is assembled with every document its prompt asks about: one item (D8) was sent without the design file it was to map, one of three samples noticed, and the item had to be rebuilt and rerun. Items written to overlap on purpose produce repeated findings, so a count of findings overstates distinct findings; mark duplicates in the adjudication.

Credentials pasted into a chat transcript are a security incident, not a footnote: rotate them at once. The keys never entered any deliverable (scanned), but the transcript cannot be edited.
