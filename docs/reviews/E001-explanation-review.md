# E001 independent explanatory review

E001 produced substantive prose about the reservation problem, but no successfully executed final program and no completed native-reasoning answer. The observed failure is concentrated in delivery, JSON construction and realization of the proposed program. These records do not justify saying that the models failed to explain the underlying reservation rule, that Mini improved task performance, or that any arm demonstrated creative knowledge creation.

This review was written after `summary.json` existed. I read the complete public response text from each completed nonnative call, the native response receipts, final results and errata. I inspected malformed JSON diagnostically without modifying it or treating a recovered prefix as the submitted program. No source, immutable record or model output was changed, and no new model calls were made. This is an addendum to the frozen experiment, not a replacement score.

The evidence root is [E001-reservation-critic](../../experiments/records/E001-reservation-critic/REPORT.md). [The pre-result task audit](../TASK_AUDIT.md) and [the semantic guide](../SEMANTIC_GUIDE.md) state the prior interpretation and limitations.

## What the records actually contain

| Arm | Available material | Observed limitation |
|---|---|---|
| Bare | One completed public response with a detailed explanation and an attempted program | Strict record parsing found a duplicate `do` key; commitments was an object rather than the required string. No task execution was established |
| Matched serialized workflow | Proposal, criticism and revision, with recorded public feedback | Both proposed and revised commitments strings fail JSON parsing. The final public and holdout case lists are empty |
| Mini | Proposal, machine feedback, criticism and a final revision response | Initial program fails parsing. Final response fails the outer submission format, and Mini completes no declared cycle |
| Native direct | Response receipt with empty public content and `finish_reason: length` | No final explanatory text or program is available |
| Matched native | Response receipt with empty public content and `finish_reason: length` on its first call | No completed proposal, later criticism or final program is available |
| Mini native | Response receipt with empty public content and `finish_reason: length` on its first call | No completed proposal or Mini cycle is available |

Each native condition exhausted its configured 8,192-token completion ceiling before delivering public answer content. Native reasoning text was not persisted. There is consequently no native final account to compare with the nonnative prose. This is a missing-output comparison, not a negative judgment on the content of an unseen argument.

The broad `OPERATIONAL_FAILURE` label covers different mechanisms here. Bare and Mini received public text but failed a submission boundary; native arms received no public final text within the ceiling. The matched workflow produced a completed final submission whose inner program could not parse. These conditions must remain distinct when interpreting the experiment.

## The central reservation explanation has bearing

The bare and matched proposals identify the relevant computational organization: select the highest revision separately for each booking, classify only that selected version as active or inactive, then aggregate one contribution per booking by item. They connect strict expiry after selection to the prohibition on resurrecting an older hold. They connect larger revision to later cancellation and preserve negative availability rather than inventing a rejection rule. Starting from stock rather than event-derived item names explains why unused items remain in the result.

The Mini proposal expresses the same central account as a register updated only by larger revisions. That is a coherent abstract procedure even though the supplied expression language lacks its proposed mutable fold. A fold over the bag can be order independent because its update retains the maximum revision and equal-revision records have identical contents. The explanation names the assumption that makes tie handling harmless.

These are task-relevant component relations, not decorative text surrounding an arbitrary answer. A direct conditional argument supports them: the maximum of the booking's admitted revisions is unaffected by replay or permutation; selecting it before expiry removes any fallback to lower revisions; classifying that winner implements the current hold/release rule; summing one quantity per booking implements version-total rather than delta semantics. The argument depends on the contract's nonconflicting-version and immutable-item assumptions.

This supports provisional bearing for the central abstract account in the declared computational respect. It does not establish that the delivered bytes realize it. Nor does it supply all representation, active-route, historical-newness and deployment obligations needed for a system-level creativity attribution. Prose does not lose its explanatory legitimacy when a machine reading fails; the stronger claim that the accompanying program implements the prose can still be false.

## Errors within the prose accounts

The matched proposal says deduplicating records must come before everything else, claiming a duplicated lower revision could otherwise survive comparison. That necessity claim is false. A procedure can enumerate distinct booking keys and select a maximum from each booking's full delivery bag; duplicates of lower revisions do not alter its maximum. It can count one selected record per booking without first structurally deduplicating the raw events. The proposed early deduplication is harmless, but the argument that this exact order is forced overstates its role.

The bare explanation is more careful about raw deduplication being dispensable, although its description of the composed reductions as idempotent can blur the difference between duplicate-insensitive selection and ordinary summation. Summation of arbitrary duplicated contributions is not idempotent. The account works because it first establishes one selected contribution per booking.

All three nonnative accounts mix domain changes with within-contract falsifiers. Conflicting payloads at the same booking/revision, unknown stock items or a changed inclusive-expiry rule challenge the applicability of the stated account to a changed problem. They do not refute an account conditional on the present contract excluding those situations. By contrast, duplicate deliveries changing totals or an expired latest hold reviving a superseded version would defeat its behavior within the declared task. ECS §9.4 requires keeping those claims distinct rather than moving scope after evidence.

Statements that previously successful behavior was preserved are also too strong as reports of this run. The records contain proposed invariants, but no successful execution of the candidate or revision. They can be preservation obligations and conditional arguments; they are not observed preserved successes.

## The matched critic identifies the layer but invents a specific parse cause

The matched critic correctly separates a commitments-string parse failure from a reservation-semantic failure. It correctly notes that an empty case list means execution never began. It then says the error establishes a second concatenated JSON value at the indicated position. Inspection does not support that diagnosis.

The first commitments string contains one parseable leading JSON value followed by a single surplus `}`. The final revision contains one leading value followed by `}}`. Those are extra closing braces, not a second well-formed JSON value. The error establishes trailing material; the exact bytes identify what that material is. The proposed story about duplicated serialized objects is speculation presented too strongly.

The revision repeats that story and announces that it has removed the parse failure. The recorded final error directly contradicts that claim. It has attempted repair and produced an explanation of a repair, but it has not satisfied the elementary obligation that the delivered commitments be one valid JSON value.

The critic also calls a maximum-based lookup on a singleton filtered set fragile. Redundancy alone is not a defect. With the stated invariant that at most one matching row exists, choosing its maximum by either its item or its value returns the same row. No independently demonstrated failure justifies changing that detail. This illustrates how a criticism can contain a sound primary point and an unsupported secondary repair target.

## Mini exposes a substantive construction gap

Mini's critic sees both the proposed account and its program text. It notices that the attempted accumulator is never threaded through the `map`, so the stated mutable register is not realized. It identifies the nonsensical sentinel comparison and the absence of keyed state update. This is a useful criticism at the interface between an abstract procedure and its chosen expression language.

The final revision responds with a materially different abstract construction: select each booking's maximum revision through filtering and `max_by`, collapse identical selected records, then aggregate. It explicitly explains why a map cannot emulate the unavailable stateful fold. The relevant criticism was present in its request, and the changed prose addresses that specific issue. This supplies evidence of correspondence between criticism and response content.

It does not complete an ECS reason-use attribution. There were no content-preserving recodings, changed-reason controls or reason-removal probes. Textual agreement and a matching proposed remedy can arise without establishing the full active-route condition of §§5.1–5.2.

The critic and revision also overstate the hypothetical executable result. They say the malformed original would return constant zero reservations once syntax is repaired. The submitted program does not execute, and fixing syntax alone does not resolve invalid operations and bindings. The supported statement is that the inspected construction fails to realize the claimed accumulator; a unique hypothetical runtime result is not established.

The final response remains unusable. Its outer object lacks the closing delimiter, its commitments contain surplus closing braces, and inspection shows unsupported `{"op":"var","name":...}` forms, a contribution list that loses item bindings while later trying to read item fields, and literal-zero output fields. These are additional construction defects. The prose's claim that the program now implements the repaired account is not borne out by the submitted text.

## ECS obligations after this run

| Obligation | Review disposition |
|---|---|
| Accounting for the abstract reservation rule | The central highest-revision-then-expiry explanation has substantive bearing under the stated contract; some necessity and falsifier claims need correction |
| Accounting for what the delivered program actually does | Not established; assertions of faithful implementation and successful parse repair conflict with the records |
| Admissible prose criticism | Present and substantive. Its legitimacy does not depend on executable commitments, but particular claims within it can be unsupported |
| Reason use on an active route | Correspondence is visible in Mini's criticism and revised account; the required content-controlled contrasts remain missing |
| Bounded repair with protected behavior | No executed success or preserved successful candidate behavior was demonstrated; the delivered construction obligation still fails |
| Originative contribution | Unresolved. An apparent conceptual change does not settle historical New or the complete owned-construction attribution |
| Created explanatory knowledge | Not established; required repair, deployment and other conjuncts are missing |
| Native versus nonnative semantic comparison | Unavailable because native final outputs are absent |
| Defeat or confirmation of ECS | Neither follows. The run exposes differences among delivery, interpretation, criticism and executable realization; it is not an independent constitutive counterexample |

## The next informative change concerns construction

The immediate evidence favors repairing the representation and execution route before increasing task complexity. A simpler program surface or a separate fallible translation stage could reduce nested-string and brace errors, provided the translation remains visible, criticizable and equally available in matched controls. That is an interface intervention, not permission to discard prose. The current DSL already has enough expressive power for the task, as independently supplied calibration established; the issue is realizing a sound account in it.

Native conditions need a separately declared completion-budget or reasoning-effort intervention capable of producing final outputs. Their absence cannot be repaired retrospectively by scoring them as wrong programs. E001 remains the record of what happened under its original settings.

The evidence supports a useful distinction: an account can identify how the problem works while its attempted operative realization fails. It also shows that criticism can correctly identify a missing mechanism yet fail to produce a working repair. Those observations are reasons to test the construction route more precisely; they are not a numerical creativity judgment.
