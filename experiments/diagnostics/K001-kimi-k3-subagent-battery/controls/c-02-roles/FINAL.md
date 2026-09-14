# W2-ROLES — `src/minireason/loop/roles.py`

Written: `src/minireason/loop/roles.py` (1199 lines) and `tests/loop/test_roles.py`
(719 lines). No other file under `src/` was touched; nothing outside the sandbox was
read or written.

Test command and its result, verbatim:

    python3 run_tests.py tests.loop.test_roles
    Ran 45 tests in 0.618s
    OK

    python3 run_tests.py            # discovery over tests/
    Ran 45 tests in 0.617s
    OK

(The sandbox carries no other test module, so the discovery run and the named run
cover the same 45 tests. The line counts above came from
`python3 -c "import pathlib; ..."` over the two files.)

## 1. The acceptance clauses, and how each is tested

**"Runs end to end on OfflineProvider with zero sockets."** Satisfied.
`call_role` takes a provider instance, a factory `(endpoint, records_dir) -> provider`,
or `None` for the live transport; the offline path passes a factory over
`OfflineProvider` and no code path in this module opens a socket.
`RunsEndToEndOnOfflineProviderWithZeroSockets.test_runs_end_to_end_on_offline_provider_with_zero_sockets`
runs all five roles with `socket.socket` **and** `provider_openai_compat._open`
replaced by a function that appends to a list and raises, then asserts the list is
empty. `test_one_exchange_runs_through_four_seats_under_one_records_dir` runs
critic → defender → a cross-family judge pair → variator under one records directory
and asserts five distinct coordinates, one record triple each.
`test_the_offline_record_says_that_nothing_was_contacted` asserts the transport's own
record carries `url: null`, `not_contacted_url`, an empty `request_header_names`, and
`settings.retries == 0`.

**"A second call on an existing coordinate raises NO_REPLAY."** Satisfied.
The guard is the write-once `"x"` open of the request record itself, with a cheap
state read in front of it for a legible message.
`ASecondCallOnAnExistingCoordinateRaisesNoReplay.test_a_second_call_on_an_existing_coordinate_raises_no_replay`
(state `TERMINAL`),
`test_a_coordinate_with_a_request_and_no_response_is_indeterminate` (the response
record is removed to stand for a killed run; the state is `INDETERMINATE`, design
4.3's third state, and the coordinate is still refused), and
`test_two_callers_racing_on_one_coordinate_leave_one_record` (two threads through a
`Barrier`; exactly one refusal, exactly one request record).
`test_the_coordinate_is_a_pure_function_of_role_seat_pack_and_repair` pins the
identity; `test_no_replay_is_a_declared_failure_code` pins `NO_REPLAY ∈
types.FAILURE_CODES`.

**"Six concurrent calls on one key_env are impossible because slots_for is acquired,
not reimplemented."** Satisfied.
`_inner_gate` returns `provider_openai_compat.slots_for(seat.key_env,
seat.max_concurrency)` — the same module-level semaphore every `OpenAICompatProvider`
on that credential already holds — and `call_role` acquires it only when the provider
does not (an `OpenAICompatProvider` holds it inside `complete`; acquiring it twice
would halve the authorisation and self-deadlock at a cap of 1).
`SixConcurrentCallsOnOneKeyEnvAreImpossible.test_the_gate_is_the_transports_own_semaphore_for_that_credential`
asserts object identity (`assertIs`) between what this module acquires and what the
transport's registry hands out for both fixture endpoints.
`test_a_sixth_concurrent_call_on_one_key_env_cannot_proceed` takes all five permits
in the main thread, starts a sixth call in another thread, asserts it has not
finished after 0.5 s and has written nothing, releases one permit and asserts it then
finishes. That is a proof by holding the gate rather than by racing six real calls —
deterministic, and stated as such here.
`test_this_module_builds_no_gate_of_its_own` scans this module's source for
`Semaphore(`, `BoundedSemaphore(` and `_SLOT_REGISTRY` and finds none.
`test_a_provider_that_already_holds_the_gate_is_not_gated_twice` asserts the attempt
record says `inner_held_by: "provider"` for a live `OpenAICompatProvider`.

**"At schema_repair_budget 0 an invalid output yields unresolved and no re-ask."**
Satisfied. `AtBudgetZeroAnInvalidOutputYieldsUnresolvedAndNoReAsk.test_at_schema_repair_budget_zero_an_invalid_output_yields_unresolved`
feeds a one-answer offline script, asserts `outcome == unresolved`, `value is None`,
`schema_reason == "missing-field"`, `block_code == "blocked:schema"`,
`repair_admissible is False`, and that the provider's own call counter reads 1 — a
re-ask would have taken a second scripted answer and there is only one.
`test_the_budget_of_record_is_the_standards_own_frozen_value` pins the budget to
`standard.GUARD_PARAMETERS["schema_repair_budget"]` rather than a number typed in this
module. `test_a_repair_past_the_budget_is_refused_before_anything_is_written` asserts
`repair=1` at budget 0 is `REPAIR_BUDGET_EXCEEDED` and leaves no coordinate.
`test_an_unresolved_output_is_not_an_absence_and_keeps_its_raw` asserts the raw blob
still holds the unparsable answer byte for byte.

**"A repair is a new coordinate with its own write-once record."** Satisfied, and it
is the clause with a conflict behind it (see §3.10).
`ARepairIsANewCoordinateWithItsOwnWriteOnceRecord.test_a_repair_is_a_new_coordinate_with_its_own_write_once_record`
asks once at a raised budget, gets `unresolved` with `repair_admissible True`, asks
again with `repair=1`, and asserts a different coordinate ending `#repair1`, the same
`pack_sha`, two records of each of the three kinds, and both coordinates `TERMINAL`.
`test_a_repair_coordinate_is_itself_asked_only_once` asserts the repair coordinate is
itself covered by `NO_REPLAY`. `test_a_second_repair_past_the_raised_budget_is_refused`
asserts `repair=2` at budget 1 is refused.

**"Every record carries seat, family, key_env, pack sha, prompt ref and raw ref."**
Satisfied, with one narrowing stated in the record itself.
`EveryRecordCarriesTheSeatAndEveryRef.test_every_record_carries_seat_family_key_env_pack_sha_and_both_refs`
asserts all six keys are present in all three records, that `seat` equals
`Seat.as_dict()`, and that `raw_ref` is **present and null** in the request and the
attempt (there is no answer yet) and holds the ref in the response.
`test_the_transports_own_record_carries_the_same_coordinate_block` asserts the
transport's own `call-NNNN.response.json` carries the same coordinate, family,
`key_env`, `pack_sha` and `prompt_ref` under its `coordinate` block.
`test_the_refs_address_the_bytes_they_name` recomputes both sha256s from the blob
files. `test_a_record_never_carries_a_credential_value_only_its_name` plants a fake
`OLLAMA_API_KEY` value in the pack and asserts the module **refuses**
(`CREDENTIAL_IN_OUTPUT`), names the environment variable, never prints the value, and
writes no blob and no record. `test_no_record_may_carry_a_scoring_key` runs G12
(`contracts.assert_no_scoring_keys`) over every written record and asserts
`_write_record` refuses a planted scoring key without creating the file.

Supporting coverage beyond the clauses: a provider failure ends the arm with the
transport's own code, `blocked:provider`, the fixed §4.4 sentence and no value
(`DeliveryEndsAnArmAndMintsNothing`); an ended arm closes its coordinate rather than
leaving it half open; an argument the transport refuses is recorded `NOT_DISPATCHED`;
the pack's declared seal is taken verbatim and a missing one is recorded as derived
(`ThePackIsTakenAsRenderedAndSealed`); a schema that is not the role's contract is
refused, an unknown role is `contracts.SchemaInvalid("unknown-role")`, and only the
seat that holds a role may be asked it (`TheContractHasOneOwner`); `ROLES is
contracts.ROLE_NAMES` by identity; every code the source can emit is in
`types.FAILURE_CODES` or in `NEW_CODES`; and this module's own prose passes
`standard.assert_no_exhaustion_claim`.

## 2. Stubs

**None.** Every name in the wave-plan's `public_interface` — `ROLES`, `call_role`,
`RoleResult.raw_ref`, `RoleResult.prompt_ref`, `ProviderArmEnded`, `NO_REPLAY` — is
implemented and exercised. Three things are *conditional* rather than stubbed, and the
record says which in every case:

* The **outer gate** (runner v2's `key_gate`, reached through
  `seats.key_gate_for`) is acquired when this process carries
  `tools/multicycle_commitment_study_multi_v2.py` and is otherwise recorded as
  `outer_unavailable: "RUNNER_NOT_IMPORTABLE"` — by name, never silently assumed.
  This sandbox does not carry runner v2, so the unavailable branch is what runs here;
  the acquired branch is tested by substituting a context manager for
  `key_gate_for` and asserting enter/exit and the recorded gate name.
* The **live transport** (`OpenAICompatProvider`) is the default when `provider` is
  `None`. No test dispatches through it to a network; one test constructs it with a
  fake credential in the environment and a patched `_open`, which exercises the
  gate-already-held branch and `ProviderArmEnded` without a socket.
* `repair >= 1` is implemented but unreachable through a *loaded* config in this
  build — see §3.10.

## 3. What the design entry, the wave-0 interface and the wave-1 decisions did not
settle, what I decided, and what would change if it went the other way

**3.1 What a `pack` is.** W2-PACKS is a sibling of this wave, not a dependency, and
`packs.py` is not in the sandbox. *Decided:* take the pack structurally — a string, a
message sequence, or an object/mapping carrying `messages`, `text`, `body`, `prompt`
or `render` — and take its **own** `sha256` (or `pack_sha`/`sha`/`digest`) verbatim
where it declares one, recording `pack_sha_source: "declared-by-pack"`; otherwise
derive a sha over the canonical prompt bytes and record
`"derived-from-prompt-bytes"`. `pack_sha` keeps its one owner, and no record claims a
seal the pack never gave. *If it went the other way* — importing `packs.pack_sha` and
requiring a `Pack` — this module would gain a wave-2 sibling dependency the wave plan
does not give it, and could not be tested before W2-PACKS lands.

**3.2 Whether `schema` may differ from the role's contract.** The signature takes a
`schema`, and `contracts` validates against its own. *Decided:* `schema=None` or a
mapping equal to `contracts.schema_for(role)`; anything else is
`SCHEMA_NOT_THE_CONTRACT`. A widened or narrowed contract is a successor standard and
a new `loop_plan_id`, never an argument. *If it went the other way* — validating
against whatever is handed in — a caller could weaken a pre-registered contract
without minting a new plan, and O11's per-register narrowing would have two rival
mechanisms (`schema` and `register=`) instead of one.

**3.3 What names a coordinate.** The signature has no coordinate argument.
*Decided:* the coordinate is `<role>/<seat label>/<endpoint>/<pack sha>` plus
`#repair<n>` (§2.3's own spelling), a pure function of the four things that make the
call what it is; `coordinate_for` exposes it and `coordinate_state` /`coordinates`
read it back for design 4.3's per-coordinate resume. So an order-swap (a different
pack), a second judge seat and a repair are all different coordinates by
construction. *If it went the other way* — an explicit caller-supplied coordinate —
`NO_REPLAY` would protect only what the caller remembered to name, and two callers
rendering the same pack for the same seat could both spend a call.

**3.4 Whether roles acquires `slots_for` itself.** Design 4.6 says the loop adds no
third gate, but `OfflineProvider` acquires nothing. *Decided:* acquire the transport's
own `slots_for` **only when the provider does not hold it**, and record which side
held it. So the offline path is held to the same authorisation as the live one, and
no permit is taken twice. *If it went the other way* — always acquiring — a live call
would consume two permits of five and would deadlock at a cap of 1; never acquiring
would leave the offline dry run ungated and the acceptance clause untrue for it.

**3.5 The plan's `max_per_key` versus the gate in force.** `seats.key_cap_for` is
`min(5, max_per_key, endpoint.max_concurrency)`, but the transport's gate is fixed at
`endpoint.max_concurrency` by whoever creates it first. *Decided:* refuse with
`CONCURRENCY_LIMIT_CONFLICT`, naming both numbers and the reason ("the loop adds no
third gate"), before anything is written. *If it went the other way* — passing the
narrower cap to `slots_for` — the first live provider on that credential would raise
the same conflict from inside the transport, after a coordinate had been opened; and
silently accepting the wider gate would exceed an authorisation that is inside
`loop_plan_id`.

**3.6 Which record carries `raw_ref`.** There is no raw at request time. *Decided:*
carry the key in all three records, **null** until the response — present-and-empty
rather than absent, the same discipline the design uses for `losses_outside_P`. *If it
went the other way* — omitting it — a reader of a request record could not tell "no
answer yet" from "this record kind does not carry that field".

**3.7 What `raw_ref` addresses.** The transport deliberately never persists a
response body. *Decided:* `raw_ref` addresses the answer text as the transport
returned it (after the transport's own redaction), stored in a content-addressed blob;
the wire body's digest rides beside it as `provider_response_sha256` where the
transport has one (it is `null` offline). *If it went the other way* — addressing the
wire body — this module would have to persist a body the transport refuses to persist,
which is a change to the transport's promise, not to this module's.

**3.8 `max_tokens`.** W1-SEATS' first deviation says W2-ROLES must pin what it
passes. *Decided:* `COMPLETION_CEILING = 8192` (the transport's own default),
overridable per call, recorded in every record as `completion_ceiling`, and described
as a RESOURCE BOUNDARY. *If it went the other way* — a per-role ceiling — the four
word limits (400/400/120/120) would suggest much smaller numbers, and a truncation
would become likelier without any record saying which role's ceiling did it.

**3.9 `thinking` on a DeepSeek seat.** *Decided:* send `thinking=False` for a seat
whose family is `deepseek` and nothing for any other family — exactly what
`CompatMiniResponder` does, for the reason it gives (a ported call otherwise gets the
provider's own default, changing token spend and truncation with nothing to flag it).
The transport then compares the control against the returned evidence and raises
`THINKING_MODE_MISMATCH` if it was ignored. *If it went the other way* — sending
nothing — native reasoning would be on by default on that family and the record would
carry no claim about it either way.

**3.10 `schema_repair_budget` — a conflict between §2.3 and W0-TYPES.** §2.3 says
"where the config raises it to 1 the re-ask is a new coordinate". `types.SeatsConfig.
from_mapping` admits `schema_repair_budget` only in the range **0..0**, deliberately
(its docstring: "raising it turns a re-ask into a budgeted new coordinate the standard
has not pre-registered"). So a *loaded* config cannot raise the budget in this build.
*Decided:* implement the repair coordinate fully, take the budget from
`standard.GUARD_PARAMETERS` when no config is given, refuse `repair > budget`, and
test clause 5 against a `SeatsConfig` **constructed directly** — the shape a successor
standard would produce — with a test
(`test_the_config_loader_pins_the_budget_at_the_standards_value`) that records the
loader's refusal so the integrator sees the boundary. I did not edit `types.py`.
*If it went the other way* — treating the 0..0 range as the last word and refusing
`repair` entirely — acceptance clause 5 would be unimplementable, and raising the
budget later would mean writing the coordinate machinery then rather than now.
**This is the one place where the design entry and a wave-0 module disagree, and the
integrator must settle it**: either §2.3's sentence is reworded at review, or
`types.SeatsConfig`'s range is opened with the standard's own range beside it.

**3.11 What goes into the prompt.** *Decided:* exactly one system message, the role's
contract schema under `SCHEMA_INSTRUCTION` ("Return one JSON object conforming to: "),
prepended to the pack's messages — the same sentence `CompatMiniResponder` adds, which
also carries the token `JSON` that DeepSeek's JSON mode requires. *If it went the
other way* — adding nothing — a pack that does not itself say "json" would be refused
by the transport on a DeepSeek seat, and the schema would have to be duplicated into
every pack renderer.

**3.12 Which role may sit in which seat.** *Decided:* `seats.REUSED_ROLES` is the one
table; a marker call takes a judge seat and every other role must take its own, else
`CONFIG_INVALID_VALUE`. A record may not name a seat that does not hold the role it
records. *If it went the other way* — no check — a critic call on a judge seat would
be recorded as a critic reading from a judge, which G0's constitution is written to
prevent.

**3.13 How the provider reaches `call_role`.** Not in the published signature.
*Decided:* a keyword `provider=` taking an instance, a factory, or `None` for the live
transport, with `SEAT_PROVIDER_MISMATCH` when an instance is bound to another
endpoint; each coordinate gets its own `provider/<stem>/` directory, because the
transport's `call-NNNN` stem counter restarts with every instance and a shared
directory would raise `RECORD_EXISTS` on the second call. *If it went the other way* —
a module-level provider mode read from the config — `provider_mode: "offline"` would
have to build an `OfflineProvider` with a script this module has no way to obtain
(W1-SYNTHETIC owns the canned deliveries).

**3.14 Two other additive keywords.** `register=` is forwarded to `contracts.check`
so a marker is held to its own register's closed token set (open question O11's
recommendation, which names W2-MARKPREP but which the marker *call* has to carry);
`require_outer_gate=` lets the driver demand runner v2's gate rather than accept the
recorded-unavailable branch. Both have defaults that keep the published call shape
valid.

**3.15 Timestamps.** *Decided:* records carry `recorded_utc` from
`datetime.now(timezone.utc)`, with no clock injection. These are spending records, not
replayable ones (`types.REPLAYABLE_STEPS` does not contain `READ`, `MARK` or `AUDIT`),
so byte-identical replay is not a promise this module owes. *If it went the other way*
— injecting a clock — the records would be replayable byte for byte and W6-DRYRUN
could compare them directly; nothing else changes.

**3.16 An argument the transport refuses.** `_validate_call_args`,
`_check_json_mode_prompt` and `_build_payload` raise `ValueError` before anything is
sent. *Decided:* close the coordinate with a response record whose status is
`NOT_DISPATCHED` and raise `RoleRefused(NOT_DISPATCHED)` — G0's own word; nothing was
formed, addressed or transmitted, so it is not an ended arm. A transport that cannot
even be *built* (a missing credential) is refused before any record exists, so the
coordinate stays `ABSENT`. *If it went the other way* — `ProviderArmEnded` — the
driver would end an arm over an argument error that spent nothing.

**3.17 What `ProviderArmEnded.code` carries.** *Decided:* the transport's own stable
code (`HTTP_429`, `KEY_MISSING`, `TRANSPORT_OR_RESPONSE_ERROR`, ...), which is what
design 4.4 puts on the `FAILED` receipt, with `.provider_code` as the same string
under a name that says where it came from and `.block_code == "blocked:provider"`.
*If it went the other way* — a single `PROVIDER_ARM_ENDED` token with the transport's
code on a field — `NEW_CODES` would shrink to six entries and the receipt would have
to reach through the exception for the code design 4.4 names.

**3.18 Fencing.** `custody.fenced` is not in this sandbox, so `records_dir` is used as
given and the write-once refusal is the transport's own `write_new` (`"x"` open,
credential redaction) with a *refusal* scan in front of it, so a credential-bearing
record is refused rather than redacted. The W0-CUSTODY convention ("`write_new` does
not fence; pair it with `fenced()`") is the caller's to keep; this module does not
fence and says so.

**3.19 The exhaustion scan.** I run `standard.assert_no_exhaustion_claim` over this
module's own prose (a test does), but **not** over the records: a failed delivery's
`error` field quotes the transport's own words verbatim (`OfflineProvider`'s "offline
script exhausted" among them), and rewriting a delivery's own message would be editing
an observation. §4.4 keeps the token out of the *stop vocabulary*, which is
W2-DECIDE's and W3-REPORT's, not this module's.

## 4. New failure codes, and the table each belongs in

`roles.NEW_CODES` is a `tuple[str, ...]` of 13 tokens, with a one-line reason for each
in `roles.NEW_CODE_REASONS`. All of them belong in **`types.FAILURE_CODES`** (wave-1
integration decision 6), in these existing groups of that table:

* *provider / delivery* — `CONTENT_TYPE`, `CREDENTIAL_ECHO`, `EMPTY_GENERATION`,
  `INCOMPLETE_GENERATION`, `RECORD_EXISTS`, `THINKING_MODE_MISMATCH`,
  `USAGE_UNAVAILABLE` (the transport's own statuses, propagated verbatim on
  `ProviderArmEnded`), and `SEAT_PROVIDER_MISMATCH` (a provider bound to another
  endpoint than the seat's).
* *role contracts (loop/contracts.py)* — `PACK_NOT_RENDERABLE`, `PACK_SHA_MALFORMED`,
  `SCHEMA_NOT_THE_CONTRACT`.
* *guard and instrument* — `BLOB_CONTENT_CONFLICT`, `REPAIR_BUDGET_EXCEEDED`.

The integrator also needs `RoleRefused`, `NoReplay` and `ProviderArmEnded` added to
`tests/loop/test_types.py::TheCodeTablesAreComplete`'s `TOKEN_ARGUMENT` map, as
decision 6 and open question O9 prescribe.

Codes this module raises that `types.FAILURE_CODES` **already** declares, so nothing
is needed for them: `NO_REPLAY`, `INDETERMINATE` (as `NoReplay.state`),
`NOT_DISPATCHED`, `CONCURRENCY_LIMIT_CONFLICT`, `CREDENTIAL_IN_OUTPUT`,
`SCORING_KEY_FORBIDDEN`, `SCHEMA_INVALID`, `CONFIG_INVALID_VALUE`,
`CONFIG_NOT_A_MAPPING`, plus `RUNNER_NOT_IMPORTABLE` and `FAMILY_COUNT_INSUFFICIENT`
which reach a caller unchanged from `seats`.

## What I could not determine

* **The real shape of a W2-PACKS `Pack`.** `packs.py` is not in this sandbox and is
  not a dependency of this module, so whether a real pack exposes `messages`, `text`
  or something else, and whether it seals itself with `sha256` or only through
  `packs.pack_sha(pack)`, is **unresolved**. I built a structural contract that
  accepts five spellings and records which seal it used; if W2-PACKS lands with a
  different one, `PACK_BODY_ATTRS` / `PACK_SHA_ATTRS` are the two lines to change.
* **Whether the outer and inner gates compose as design 4.6 describes.** Runner v2
  (`tools/multicycle_commitment_study_multi_v2.py`) is not in the sandbox, so
  `seats.key_gate_for` cannot be exercised against the real registry here. I take the
  gates in the order outer-then-inner (the order runner v2's own waves take them, from
  reading §4.6), and the acquired branch is tested against a substitute. That "a
  reading call and a dispatch call in flight together are held to five per credential
  between them" is a claim I could not run; I could not determine it and this is why.
* **The `HTTP_<status>` family.** `types.FAILURE_CODES` declares `HTTP_429` only, and
  the transport mints `HTTP_<code>` for any status. Those tokens never appear
  literally in this module's source, so the code-table scan cannot see them and
  `NEW_CODES` cannot enumerate them. Whether the table should carry a parameterised
  entry (as `STOP_REASONS` does for `preregistered_condition:<id>`) is a question for
  the integrator; I left it open rather than inventing a spelling.
* **Whether `blocked:provider` is right for every transport status.** I map every
  `ProviderFailure` at dispatch to `blocked:provider`. `RECORD_EXISTS` is really a
  records-directory collision rather than a delivery failure, and
  `SECRET_IN_REQUEST` is a refusal to send rather than a failed send. Both are
  recorded with their own status; whether they deserve a different block code is
  **unresolved** and needs W3-TRIAL's view of the block register.
* **The `schema_repair_budget` conflict (§3.10) is reported, not settled.** I could
  not settle it inside this module: settling it means either editing `types.py`
  (which this sandbox forbids) or rewording §2.3, and both are the integrator's.
* **Cross-process concurrency.** The gate holds within one process only; design 4.6
  says so and `run.lock` is W1-STEPS'. Nothing here covers a second process on the
  same credential, and this module makes no claim about one.
* **What I did not cover.** I wrote no test that dispatches to a live endpoint (no
  network, by instruction), none that exercises `publish`, `custody` or `receipts`
  (those modules are not in this sandbox), and none that runs the wider repository
  suite — only `tests/loop/test_roles.py` exists here, so the "45 tests OK" above is
  the whole of what I ran and is not evidence about any other module. Whether
  `roles.py` still passes the repository's own `tests/loop/test_types.py` code-table
  scan is **unresolved** until `NEW_CODES` is folded into `types.FAILURE_CODES`: by
  construction that scan will fail on this module's thirteen new tokens, which is
  exactly the signal O9 designs for.
