> Published verbatim, body unedited: this document was written against the staging tree `scratchpad/contrast/`, so `scratchpad/contrast/...`, `.build/` and "the staging tree" below name that scratchpad tree and not any path in this repository, where the files it describes are `tools/contrast_triple_study.py`, `tests/test_contrast_triple_study.py`, `experiments/diagnostics/C001-contrast-triple/{PLAN.md,NOTES.md,material.json,RECODING_TABLE.md}` and the two provenance scripts at `experiments/diagnostics/C001-contrast-triple/build/`. Two of its stated identities are superseded by the publication that carries it, under REC-20260914-U, and this note is the only correction made to it: the material sha256 is now `94edfe612097441c8a5957c41a8a1140833b89bd155bd9794b60a1bfb8979975` and the `plan_id` is now `328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8`, because a per-endpoint `timeout_seconds` table was added to the material and the driver before dispatch (PLAN §5, §6(iii)); the `34f51017…` / `52251e15…` pair the table below states is the staged identity it superseded. The suite line it quotes, `Ran 106 tests`, is the staging tree's figure; in this repository the same file runs **119** tests — thirteen were added for that change — inside the whole offline suite, `PYTHONPATH=src python -X utf8 -m unittest discover -s tests`.

# C001 — closing the adversarial review

Every finding of the two-lens adversarial review of the staged C001 contrast-triple
study, the change made for it, and the test that pins the change. All work is in the
**staging tree only** (`scratchpad/contrast/`); `/home/user/miniReason` was not written
to, no live provider call was made, and no credential or `.env` value was read or
displayed.

| item | value |
|---|---|
| new `plan_id` | `34f510170282f374cf1132eb7b2334030a3b39965c97313b36e79fb746f3184f` |
| new `material.json` sha256 | `52251e152a22b79e13c0cc9430540304897bffd02b89d8aed937bf55990a4632` |
| previous `plan_id` | `4f3748ba27ed6e088a352aaaf73026af8723eae11afc9c4314daabc69dc934a5` (superseded at the spot-check closure), before it `4c5058a05a770c7dfa0341475b5c580525c558f0a6a273aa174c6fd47eeea84c` |
| previous `material.json` sha256 | `a4e6e6a9bd5e02765b50f17d5eaf4fa3e0b2cf45cfb65c4065263f747e7cdd5a` (superseded at the spot-check closure), before it `cf4af694995645dd50a6f581b57da0fc9225faaf06b68b90f18c6203d6c36a50` |
| suite | `Ran 106 tests` — **OK** (101 at the adversarial-review close; 42 before it) |
| determinism | two `prepare` runs from different working directories produce byte-identical `plan.json` with the new `plan_id` |
| status | still **pre-registered, not dispatched**. This is a successor pre-registration with its own identity, not an amendment (PLAN §13) |

The material, the recoding rules, the reading rule and the driver all changed, so the
`plan_id` changed, as PLAN §13 requires. `PLAN.md`'s plan-identity line, its material
sha256, `RECODING_TABLE.md` and `NOTES.md` have been updated to the new values.

---

## Part 1 — findings, changes, pinning tests

Lens 0 is *FW5 fidelity and pre-registration quality*; lens 1 is *engineering*. Every
finding of every severity is listed.

### Lens 0 — FW5 fidelity and pre-registration quality

| # | sev | finding | change | pinning test |
|---|---|---|---|---|
| **0.0** | HIGH | prose `B.P5.S2` moved the objected-to items out of the objected-to role into the grounds role, breaking FW5:609 constituent preservation on the prose arm's own role-declaring sentence | Recoded as *"What I have grounds for objecting to is order of operations and the diagnostic confidence that rests on a conjecture the account itself calls a conjecture."* — the objected-to items stay objected-to; grounds stay where the objection puts them (`B.P1.S2`). Rules relabelled `R1 R3`. Material re-frozen, table re-rendered, new `plan_id` accepted | `RecodingReRead.test_objected_to_items_stay_in_the_objected_to_role` |
| **0.1** | HIGH | `fcl_surface` reduced every cross-document reference to the text after `#`, discarding the artifact address; the objection and the account share 5 of the objection's 8 record ids, so 5 of 8 were attributed to the objection whichever document was cited. NOTES D8 called this "unambiguous" | Reference resolution is now keyed on **(artifact prefix, record id)**. `resolve_ref` matches a prefix against each declared artifact address, that address truncated to 16 hex characters (the form the real H005 response node emitted), and the source name. `material.json.arms.<arm>.artifact_addresses` declares the three addresses (plus `record_ids_by_document`) so the driver reads them rather than inferring them. The table now has four separate columns — objection-prefixed, account-prefixed, rival-prefixed, unrecognised-prefix — and bare/unprefixed refs stay in the bare-token/unresolved channel (`bare_refs_unresolved`). NOTES D8 rewritten: a structured reference is unambiguous **only when its prefix is retained**. PLAN §7 rewritten to match | `ReferenceDisambiguation.test_an_account_prefixed_ref_is_not_counted_as_an_objection_ref`, `…test_the_sixteen_hex_truncation_the_h005_node_emitted_resolves`, `…test_an_unrecognised_prefix_is_reported_and_not_attributed`, `…test_a_bare_ref_stays_in_the_unresolved_channel`, `…test_the_artifact_addresses_are_declared_and_distinct`, `…test_notes_no_longer_call_a_bare_structured_ref_unambiguous` |
| **0.2** | MED | the per-unit `rules` column did not describe the operations performed, and several units used operations with no rule in the declared set at all | **All 85 units re-read and every `rules` cell relabelled truthfully** (73 of 85 units changed in text, label or both — Part 2). Undeclared operations were **reverted, not licensed**: no `R6` (information structure) and no `R7` (determiner/definiteness) were added, because the content-preservation argument for each is not clear-cut. `prepare` now checks (c) that each unit's labels are a subset of the declared set and reports which declared rules went unused. The mood problem the review named (`K.c2.text.S1`, declarative → pseudo-imperative) is gone because that unit was reverted | `RecodingReRead.test_no_unit_is_the_identity_and_every_label_is_declared`, `…test_an_undeclared_rule_label_is_refused`, `PreRegistrationDocument.test_no_information_structure_or_determiner_rule_is_declared` |
| **0.3** | MED | systematic conditional-modality drift: 11 units dropped `if`, 9 substituting `should`/`were`/`where`, two of them inside FCL-1 `bearing` fields and two in the prose objection's own self-defeater sentences | **Conditional form is now held constant (`if` → `if`) in every conditional unit** — `K.o1.bearing.S1`, `K.o4.bearing.S1`, `K.o4.text.S2`, `B.P4.S4` (`as though` → `as if`), `B.P6.S4` (`Were the account` → `If the account were`), prose `B.P4.S2`, `C.P1.S2`, `C.P2.S2`, `C.P3.S2`, `C.P4.S1`, `C.P6.S1`. The invariant "hedge force preserved" is now *enforced*: `prepare` counts 23 declared hedge/modal marker families per unit after contraction expansion and refuses any change (`RECODING_HEDGE_FORCE_CHANGED`). No `R8 MODALITY` rule was declared — the invariant was made true instead of being dropped | `RecodingReRead.test_conditional_form_is_held_constant_in_every_condition_unit`, `…test_hedge_force_is_checked_per_unit_and_a_change_is_refused` |
| **0.4** | MED | the evaluative modal *"deserves to be"* was flattened into a placement assertion twice, once inside an FCL-1 `commitment` record's text | **"deserves to be" restored** in `fcl B.P5.S2` and `fcl K.c1.text.S1`; the rest of each recoding stands (`B.P5.S2` now `R1 R2 R5`, `K.c1.text.S1` now `R1`). The `DESERVE` marker family is in the hedge check, so it cannot be dropped again silently | `RecodingReRead.test_the_desert_claim_is_not_flattened_into_a_placement_claim` |
| **0.5** | MED | `R4` was used to resolve an antecedent the original leaves open (prose `C.P4.S2`), which adds a distinction the objection did not make | **`That` left as `That`** in `C.P4.S2` (now `R1 R3`). `R4`'s rule text now carries the uniqueness restriction — *applicable only where the demonstrative has a unique antecedent inside the same paragraph, with the uniqueness argument recorded in the unit row*. All five `R4`-labelled units were re-checked against it: **none survives**, so `R4` is now declared and **not exercised**, and is listed in `not_exercised` beside cross-unit re-ordering. `prepare` reports `rule_labels_declared_and_not_used` | `RecodingReRead.test_an_open_demonstrative_is_not_resolved_for_the_objection`, `…test_r4_is_declared_and_not_exercised_under_its_uniqueness_restriction` |
| **0.6** | MED | software identity was not pinned: the endpoint registry and the transport module live only in the staged provider package and supply `base_url`, `chat_path`, `timeout_seconds`, `max_concurrency`; PLAN cited a repository path that does not hold the study's registry | New **`material.json.transport_pins`** block: sha256 of `minireason/provider_openai_compat.py` and of `minireason/data/endpoints.json`, both resolved from the actually-imported module. `check_transport_pins` **re-hashes both on every command** — `prepare`, `verify`, and therefore `run`, `audit` and `table` — raising `TRANSPORT_PIN_MISMATCH`/`TRANSPORT_PIN_MISSING`. The block is carried into `plan_body`. PLAN §3 publishes both hashes and states that **the registry is supplied by the staged provider package, not by the repository**; §5's endpoint table says the same; §13 now names "the transport module's or endpoint registry's bytes" as a change that mints a new `plan_id`. The preflight also asserts the transport's own `timeout_seconds` and `max_concurrency` against the declared ceilings. The unreceipted §5 provenance sentence ("All six answered live…") is now explicitly marked as a **receipt owed**, to be read as why six endpoints were planned rather than as evidence | `TransportPins.test_the_transport_and_its_registry_are_pinned_and_rehashed`, `…test_a_tampered_transport_pin_stops_the_study`, `…test_the_pinned_registry_is_the_one_beside_the_resolved_transport`, `PreRegistrationDocument.test_the_transport_pins_are_published_and_section_13_names_them` |
| **0.7** | MED | §9's claim ceiling said the design *excludes* the coding and carrier rivals — contradicting its own next bullet three lines below — and §11 omitted SEMANTIC_GUIDE's named rival, redundancy | §9 now reads: *"…and **do not exhibit the differences** a coding-tracking or a carrier-tracking explanation predicts. **A null on the recoding and carrier legs does not exclude those explanations; at N = 5 it leaves them unrefuted and unsupported at this node.**"* New **L8 — redundancy can conceal use in endpoint invariance**, quoting SEMANTIC_GUIDE and separating the all-four-cases-invariant case (F1) from the recoding-and-carrier-invariant case (may be use, may be redundancy; C001 cannot separate them) | `PreRegistrationDocument.test_the_claim_ceiling_no_longer_claims_to_exclude_the_rivals`, `…test_the_new_limitations_are_recorded` |
| **0.8** | MED | the §10 interpretation registry omitted **component edit semantics**, the one SEMANTIC_GUIDE item most load-bearing for a study made of three edits of one document | Row added to §10, naming the three edit kinds (RECODING preserves the FW5:609 constituents, hedge force, quotations and every FCL-1 id/type/reference/uptake; CARRIER preserves the normalised form under §4(c); CONTROL deletes the block) and stating that **no edit composes with another** — each case is a single edit of ORIGINAL | `PreRegistrationDocument.test_the_interpretation_registry_names_component_edit_semantics` |
| **0.9** | MED | "differs" was not defined well enough for two readers to mark the same cells; the registers were a prose list, "beyond the replicate spread" had no procedure, nothing fixed the order of reading, and a rule added to PLAN.md alone would sit outside the pre-registration digest | New **PLAN §8a "What 'differs' means, pre-declared"**, **mirrored into `material.json.reading_rule`** so it is inside the frozen identity (`plan_body` carries it; the mirror is what changed `plan_id`). Four registers — **T** target named, **E** objection record engaged *prefix-resolved*, **D** proposed action, **G** grounds cited — each marked `differs`/`same`/`unresolved`, never summed or averaged; the within-ORIGINAL replicate spread as the baseline, stated as a rule; a fixed order of reading (the within-ORIGINAL spread is written into `COMPARISON.md` **first** and not revised); a register-to-falsifier mapping (G alone does not carry D1); and a two-readers rule that sends disagreement to `unresolved`. `COMPARISON.md` now renders the registers and an **empty** mark grid per cell (`root_register_marks`). NOTES Q5 is marked CLOSED | `ReadingRule.test_the_reading_rule_is_inside_the_frozen_identity`, `…test_a_missing_reading_rule_is_refused`, `…test_the_rendered_comparison_carries_the_registers_and_empty_marks`, `PreRegistrationDocument.test_section_8a_is_present_and_mirrored_into_the_material` |
| **0.10** | LOW | the "~3% of each other in length" gloss was computed on the whole brief, which is 15.3 k characters of shared prefix and suffix; on the block the spread is more than twice that | §2 now reports **both bases**. Block level, recomputed on the material as it now stands (spot-check closure): fcl 7726 → 7961 (+3.0 %) → 8293 (**+7.3 %**) → 78; prose 5651 → 5803 (+2.7 %) → 5720 (+1.2 %) → 78. The fcl CARRIER block is the longest of the four and the +7.3 % is attributed explicitly to the declared `indent=2` serialisation. §11 L5 gains the consequence: a block-length effect is a live alternative reading of F3 alongside the grain-declaration reading | `PreRegistrationDocument.test_the_block_level_length_basis_is_reported`, `…test_the_lengths_reported_are_the_lengths_measured` (recomputes every figure from the frozen material) |
| **0.11** | LOW | the carrier intervention differs in kind between arms and nothing said an F3 firing on one arm is not an arm difference | New **L9 — the carrier leg is not comparable across arms**: the FCL-1 carrier reorders and re-serialises structure, the prose carrier changes layout only, so an F3 that fires on one arm and not the other records a difference between two *interventions*, not between two commitment languages | `PreRegistrationDocument.test_the_new_limitations_are_recorded` |
| **0.12** | LOW | the bare-token channel double-counted structured references, because `#` and `.` are word boundaries under the old lookaround | `token_occurrences` now uses `(?<![A-Za-z0-9_#.])`, so a token preceded by `#` or `.` is excluded and counted only in the prefix-resolved channel. The column note and PLAN §7 say so | `ReferenceDisambiguation.test_the_bare_token_channel_does_not_double_count_a_structured_ref` |
| **0.13** | LOW | the fcl recoding introduced 2 em dashes (U+2014) the fcl source document never uses, putting a carrier disturbance on the RECODING leg | Both were in `B.P1.S1`, which was rewritten for an independent reason (its pseudo-cleft), and the em dashes are gone: fcl originals 0, fcl recodings **0**. The test generalises to every quotation and dash character in both arms, and also caught two `centers` → `centre` spelling drifts (`B.P5.S4`, `K.c1.grounds.S1`), now reverted | `RecodingReRead.test_the_fcl_recoding_introduces_no_typography_the_source_does_not_use` |
| **0.14** | LOW | L4 analysed the varying hex but not the field **name**: "Original body SHA256" is false of the RECODING and CARRIER cases while its value is true of them | L4 extended with exactly that sentence, in the runner's own wording, with the same false-negative-only direction argument, and recorded as a further candidate for the neutral-wording follow-up at NOTES Q3. NOTES D3 carries the matching disclosure | `PreRegistrationDocument.test_the_new_limitations_are_recorded` |

### Lens 1 — engineering

| # | sev | finding | change | pinning test |
|---|---|---|---|---|
| **1.0** | HIGH | `audit` never re-tied a written request to the frozen plan brief: `messages_sha256`, `brief_sha256`, `objection_projection_sha256` and the shared prefix/suffix hashes were written and never read again, so a record set could be perfectly self-consistent about a brief that was never planned | `read_terminal` now takes the plan and asserts `plan_id` on request and attempt, `messages_sha256`, `brief_sha256`, `objection_projection_sha256`, and the arm's `shared_prefix_sha256`/`shared_suffix_sha256` against `plan['briefs']`, plus that the request's user message re-hashes to the frozen `brief_sha256`. Any mismatch raises **`REQUEST_NOT_FROM_PLAN`**. PLAN §12 step 4 states it | `AuditTiesToThePlan.test_a_request_carrying_another_cases_brief_is_refused` (reproduces the review's probe — swaps in another case's brief *and* refreshes every internal cross-reference), `…test_a_foreign_plan_id_on_a_request_is_refused`, `…test_a_clean_occurrence_still_audits` |
| **1.1** | MED | `audit` never recomputed an artifact's content digests from the delivered bytes, so an artifact body no model returned survived the audit | `read_terminal` now re-runs **`decode_contribution`** against the provider record and compares `body`, `commitments`, all three digests, `envelope_status`, `envelope_repairs`, `strict_parse_would_succeed`, `delivery_status`, `comparable`, usage and finish fields, and re-derives the two text hashes. Mismatch raises **`ARTIFACT_NOT_DERIVED_FROM_DELIVERY`** | `AuditTiesToThePlan.test_an_artifact_body_that_was_never_delivered_is_refused` (reproduces the review's probe, receipt hash refreshed) |
| **1.2** | MED | every failure was recorded as an exception class name, so `ProviderFailure.code` and the declared validation codes were discarded and a rate-limit storm was indistinguishable from a missing key | New `failure_code(exc)`: `getattr(exc, 'code')` where the transport supplies one, else the message when it matches `[A-Z0-9_]+`, else the class name. Receipts now carry `failure_type` + `failure_class` and `validation_failure_type` + `validation_failure_class`. `audit` reports a `failure_codes` profile for the whole run. PLAN §12 step 3 states it | `FailureRecording.test_a_declared_refusal_code_reaches_the_receipt_and_the_audit`, `…test_failure_code_prefers_the_declared_code_over_the_class` |
| **1.3** | MED | the juxtaposition dropped the delivered text of any refused delivery — exactly the replies root most needs — even though the bytes were on disk | `comparison()` sets `row['path']` whenever `responses/<…>.txt` exists, independently of whether an artifact was written, and a FAILED row carries `failure_type`, `validation_failure_type`, `provider_status` and `finish_reason`. `render_juxtaposition` prints the delivered bytes under the FAILED heading with a line **naming the refusal** and stating the cell is unresolved; `(no delivered text reached disk)` is reserved for coordinates where nothing arrived. `COMPARISON.md` shows the refusal code beside the state. PLAN §7 states it | `FailureRecording.test_a_refused_delivery_still_shows_root_the_delivered_bytes` (asserts the scripted text appears in the juxtaposition), `…test_no_delivered_text_says_so_rather_than_pretending` |
| **1.4** | MED | no resume path: `NO_REPLAY` fired before the wave re-verify branch, which was therefore unreachable; and `table()` could permanently consume its three write-once names on an empty occurrence | `run(..., resume=True)` / CLI **`--resume`** skips coordinates that already have a receipt and **keeps `NO_REPLAY` for a coordinate with a request or attempt but no receipt** — the genuinely ambiguous case, never silently re-sent. The wave record is now the wave **as the plan defines it**, so it is byte-identical under any filter or resume and the re-verify branch is reachable and tested; a real redefinition is still `WAVE_CHANGED`. `table(..., force=False)` now refuses an occurrence with undispatched or unresolved-attempt coordinates (**`OCCURRENCE_INCOMPLETE`**), with CLI `--force`. PLAN §12 gains step 3a; NOTES §5 shows the `--resume` invocation | `Resume.test_resume_completes_an_interrupted_case_without_replaying_it`, `…test_resume_still_refuses_a_request_without_a_receipt`, `…test_the_wave_record_is_idempotent_across_a_resume`, `PrematureRender.test_table_refuses_an_incomplete_occurrence_unless_forced` |
| **1.5** | MED | the test file hardcoded a session-specific scratchpad path as the default provider source and exported it into the process environment, which after publication would shadow the published module | The default is gone. `PROVIDER_SRC = os.environ.get('MINIREASON_PROVIDER_SRC') or str(REPO / 'src')`, inserted so the provider source wins over the repository `src`, and **nothing is written to `os.environ`**. NOTES §5 now says the export is *BEFORE publication only* and must be dropped afterwards, and explains why | `GuardsWithTeeth.test_the_suite_hardcodes_no_session_staging_path` (scans the test file, the driver and NOTES) |
| **1.6** | LOW | `seed_echoed_in_response` was `'seed' in record` — structurally always `False` — while the material and NOTES Q6 told root to read it | The field is **tri-state**: the echoed value when the provider returned one, otherwise `None` — unknown, not denied (FW5:634). New `seed_echo_reported` (did the record carry the key at all) and **`system_fingerprint`**, the determinism signal the OpenAI-compatible families actually return, are recorded per call. `material.json.seed_policy`, PLAN §5 and NOTES Q6 rewritten to match | `SeedReporting.test_seed_echo_is_unknown_rather_than_denied`, `…test_a_returned_seed_and_fingerprint_are_recorded_as_returned` |
| **1.7** | LOW | two preflight assertions could not fail: the providers were built and never referenced, so `provider_calls` was 0 by construction; and one check compared a value to an immediate recomputation of itself | The preflight now builds **every one of the 240 payloads through the OfflineProvider itself** — `_validate_call_args`, `_check_json_mode_prompt`, `_build_payload`, `_settings_view` — with an **empty script**, so an actual `complete()` would raise. The self-comparison is replaced by `digest(provider_payload) == digest(payload)` (**`PAYLOAD_NOT_THE_TRANSPORTS`**), and the count is read as `p.calls`, not `getattr(p, 'calls', 0)`, so a renamed counter is an `AttributeError`. `preflight.json` records `payloads_built_by_the_transport` | `GuardsWithTeeth.test_the_preflight_call_count_assertion_can_actually_fail` (a stand-in that moves the counter; asserts `OFFLINE_PREFLIGHT_MADE_A_PROVIDER_CALL`), `…test_the_preflight_builds_every_payload_through_the_transport` |
| **1.8** | LOW | `assert_no_scoring_keys` cannot fire on real data and its own logic was untested | Negative tests added for forbidden keys at top level, nested in a sub-dict, nested in a list of lists, and in upper case; a positive test on an innocent dict. The call site is kept as insurance against a future edit that interpolates model text as a key, and **NOTES D14 now says plainly that it does not constrain the current output** | `GuardsWithTeeth.test_a_scoring_key_anywhere_is_refused`, `…test_a_scoring_key_is_recognised_whatever_its_case`, `…test_an_innocent_dict_passes` |
| **1.9** | LOW | `_md` escaped `\|` only on the `str` branch; list and dict elements — three of which are model-controlled — were joined unescaped, and no branch stripped newlines | New `_cell()` applies backslash, `\|` and newline escaping to **every rendered scalar**, including elements joined inside the list and dict branches; `_md` routes all branches through it | `GuardsWithTeeth.test_markdown_cells_escape_pipes_and_newlines_everywhere`, `…test_a_model_emitted_pipe_cannot_break_the_rendered_table` (a scripted reply whose record id and target contain `\|` and a newline; asserts the rendered rows keep the header's unescaped-cell count) |
| **1.10a** | LOW | `_offline_provider` called `tempfile.mkdtemp` once per endpoint and never removed the directories | One `tempfile.TemporaryDirectory` for the whole preflight, passed to the factory, removed on exit | `GuardsWithTeeth.test_the_preflight_leaves_no_temporary_directories_behind` |
| **1.10b** | LOW | `audit`'s `seed_by_endpoint` was assigned per coordinate, so a field named per-endpoint reported the last replicate's value | Aggregated over replicates: `seeds_sent` (sorted set), `honors_seed_constant`, `seed_echoes`, `seed_echoes_reported`, `system_fingerprints`, `coordinates` | `SeedReporting.test_seed_by_endpoint_aggregates_over_replicates` |
| **1.10c** | LOW | `write_new`'s credential scan hardcoded two env names rather than deriving them | `register_credential_envs(material)` derives the scanned set from the two literals ∪ every `key_env` in the material ∪ the transport's own `_secret_env_names()`; `validate_material` registers it, and `preflight.json` records `credential_envs_scanned` | `GuardsWithTeeth.test_the_scanned_credential_names_are_derived_from_the_material` |

---

## Part 2 — Recoding re-read

All **85 units** (50 fcl: 28 body + 22 FCL-1 field; 35 prose: 20 body + 15 commitment)
were re-read one by one, against the original H005 objection documents, on six axes:

1. **FW5:609 constituent role** — does the recoded unit keep the represented target *z*,
   the alleged defect *δ*, the grounds *g* and the bearing in the roles the original
   assigns them?
2. **Hedge force** — is every modal and hedge at its original strength?
3. **Evaluative modals** — is a desert or obligation claim still a desert or obligation
   claim, not a flat assertion?
4. **Determiner and definiteness** — `the`/`a`, `the`/`this`/`that`, bare/determined.
5. **Information structure** — clefting, pseudo-clefting, topicalisation, equative
   inversion, subordination ↔ coordination, assertion ↔ presupposition.
6. **Antecedent resolution** — does the recoding fix a reading the original leaves open,
   or introduce a new anaphor?

**The governing decision.** Where the review offered a choice between declaring a new
rule and reverting, the recoding was **reverted to the simplest declared operation**.
No `R6` (information structure) and no `R7` (determiner/definiteness) were added: the
content-preservation argument for either is not clear-cut — information structure is
precisely where an objection's emphasis and presupposition live, and definiteness is
where its commitments about what exists live — and a rule set that licensed them would
be certifying more than the designer can argue. One consequence is that the recoding is
now *smaller*: it changes words, voice, clause order within a unit, and connectives, and
nothing else. `R4` came out of the re-read declared and unexercised.

**Counts.** 60 units have a changed recoded text; 13 more keep their text and have a
corrected `rules` label; 12 are untouched. **73 of 85 units changed.**

### 2a. Units whose recoded text changed (60)

Reason codes: **CONST** FW5:609 constituent role · **MODAL** evaluative modal ·
**COND** conditional form held constant · **HEDGE** other hedge/modal force ·
**INFO** information-structure operation reverted · **DET** determiner/definiteness
reverted · **ANTE** antecedent/deixis reverted · **TYPO** introduced typography or
spelling reverted · **PUNCT** punctuation restored.

| arm | unit | rules (was → now) | why |
|---|---|---|---|
| fcl | `B.P1.S1` | R1 R2 → R1 | INFO pseudo-cleft *"…is what I want to push on"* reverted; TYPO both introduced em dashes removed |
| fcl | `B.P1.S2` | R1 R3 → R1 | INFO negation relocated (*"offers it no obvious support"*) reverted |
| fcl | `B.P2.S3` | R1 → R1 R5 | HEDGE `will` restored; DET *"that settlement"* → *"the settlement"* |
| fcl | `B.P2.S5` | R1 → R1 | ANTE *"One of them"* introduced an anaphor; *"One person"* restored |
| fcl | `B.P2.S7` | R1 R3 R5 → R1 R5 | INFO pseudo-cleft *"what is later disputed is"* reverted; DET *"its terms"* → *"the terms"*; HEDGE *"just as well"* |
| fcl | `B.P2.S8` | R1 → R1 | HEDGE *"not necessarily"* restored (was *"need not … at all"*) |
| fcl | `B.P2.S9` | R1 R3 → R1 | HEDGE `can` restored (was `may`); *"instead"* not added |
| fcl | `B.P3.S1` | R1 R2 → R1 R2 R5 | ANTE *"the point"* → *"this"*; DET *"its working one"* → *"the working one"* |
| fcl | `B.P3.S2` | R1 R2 R5 → R1 R2 R3 R5 | HEDGE `has to` not `must`, *"looks"* not *"appears"*; *"even"* not added |
| fcl | `B.P3.S3` | R1 R2 → R2 | INFO modifier promoted to an independent clause, reverted |
| fcl | `B.P3.S4` | R1 → R1 R3 | HEDGE `might` restored (was `may`) |
| fcl | `B.P4.S3` | R1 R2 R3 → R1 R2 R3 | PUNCT `;` → `,` restored |
| fcl | `B.P4.S4` | R1 R3 → R1 | INFO pseudo-cleft reverted; COND *"as though"* → *"as if"* |
| fcl | `B.P5.S2` | R1 R4 → R1 R2 R5 | MODAL *"deserves to be"* restored; ANTE *"the one"* → *"the part"*; HEDGE negation restored |
| fcl | `B.P5.S3` | R2 R3 → R1 | INFO negative-quantifier subject (*"No flatmate…"*) reverted |
| fcl | `B.P5.S4` | R1 R2 → R2 R5 | ANTE *"the point"* → *"this"*; DET *"its overall frame"*; TYPO *"centre"* → *"centers"* |
| fcl | `B.P6.S2` | R2 R3 → R1 | HEDGE `cannot` restored (was *"The material does not let me tell"*) |
| fcl | `B.P6.S3` | R2 R3 → R1 | INFO pseudo-cleft *"What I object to is"* reverted |
| fcl | `B.P6.S4` | R2 → R1 | COND *"Were the account"* → *"If the account were"* |
| fcl | `K.o1.text.S2` | R1 R2 R3 → R1 R3 | INFO argument swap of *"is consistent with"* and adverbial fronting reverted; HEDGE *"just as well"* |
| fcl | `K.o1.bearing.S1` | R1 R5 → R1 R3 | COND `Should` → `If` — a `bearing` field, the FW5:609 constituent the invariant names |
| fcl | `K.o2.text.S2` | R1 R2 → R1 | INFO argument swap of *"coexist with"* reverted |
| fcl | `K.o2.bearing.S1` | R1 R2 → R1 R3 | ellipsis *"a rise"* made explicit as *"a rise in recurrence"* |
| fcl | `K.o3.text.S1` | R2 → R1 | INFO assertion → presupposition (*"Having called the material 'thin'…"*) reverted |
| fcl | `K.o3.text.S2` | R1 R2 R3 → R3 | INFO double pseudo-cleft reverted to a plain passive |
| fcl | `K.c1.text.S1` | R1 R2 → R1 | MODAL *"deserves to be"* restored inside a `commitment` record text; INFO fronted because-clause and its cataphoric *"it"* reverted |
| fcl | `K.c1.grounds.S1` | R1 R2 R3 R5 → R2 R5 | ANTE *"the point"* → *"this"*; DET; TYPO *"centre"* → *"centers"* |
| fcl | `K.c2.text.S1` | R2 R3 → R2 R3 | INFO declarative → pseudo-imperative (*"Specify … and it remains …"*) reverted, inside a `commitment` text |
| fcl | `K.c2.consequence.S1` | R1 R2 R3 → R1 R3 | ANTE argument swap left *"it"* with an ambiguous antecedent; HEDGE `ought` → `should` |
| fcl | `K.o4.text.S2` | R1 R5 → R1 | COND `Where` → `If`; HEDGE *"genuinely"* restored |
| fcl | `K.o4.bearing.S1` | R1 R5 → R1 | COND `Should` → `If` — the second `bearing` field |
| fcl | `K.p1.text.S2` | R1 R4 → R1 | ANTE demonstrative → pronoun (the *opposite* of R4) reverted; HEDGE added `can` removed |
| fcl | `K.u1.text.S1` | R1 → R1 R3 R5 | HEDGE negation *"not merely"* restored (was *"rather than merely"*); PUNCT |
| prose | `B.P1.S1` | R1 R2 → R1 | INFO identificational subject changed from *the account* to *my objection*, reverted |
| prose | `B.P2.S2` | R2 R3 → R3 | INFO negative-quantifier subject (*"Nothing in the material forces"*) reverted |
| prose | `B.P2.S3` | R1 R2 → R1 | INFO equative inversion reverted |
| prose | `B.P2.S4` | R1 R3 → R3 | HEDGE *"simply"* restored (was *"do no more than"*); PUNCT comma restored |
| prose | `B.P3.S2` | R1 R2 → R1 R2 | ANTE *"the two"* → *"them"* |
| prose | `B.P3.S3` | R1 → R1 | HEDGE negation *"is not a case"* restored (was *"is no case"*) |
| prose | `B.P3.S5` | R1 R2 R5 → R1 R5 | INFO object fronting reverted; HEDGE `ought` → `should` |
| prose | `B.P3.S6` | R1 R2 R5 → R2 R5 | HEDGE both `can`s restored (were `may` + bare verb) |
| prose | `B.P3.S7` | R3 R4 → R1 R3 | INFO relative clause → coordination reverted; HEDGE added `can` removed; label had claimed a deixis operation that was never performed |
| prose | `B.P4.S1` | R1 R2 → R2 | DET definite → indefinite (*"a dependency of its own"*) reverted; INFO *"As caveats go"* reverted |
| prose | `B.P4.S2` | R1 R5 → R1 R5 | COND `Where` → `If`, on the unit stating the mechanism the objection turns on |
| prose | `B.P4.S3` | R2 R4 → R3 | INFO fronting + cleft reverted; label had claimed a deixis operation that was never performed |
| prose | `B.P4.S4` | R1 R2 → R1 | INFO equative inversion reverted |
| prose | `B.P5.S1` | R2 → R1 | INFO object fronting reverted |
| prose | `B.P5.S2` | R1 R3 → R1 R3 | **CONST** — the HIGH finding: objected-to items restored to the objected-to role |
| prose | `B.P5.S3` | R1 R5 → R1 R5 | DET *"A clean version"* → *"The clean version"* |
| prose | `C.P1.S2` | R1 R5 → R1 | COND `Should` → `If` |
| prose | `C.P2.S1` | R2 R3 → R1 | INFO restructure into a relative-clause NP reverted |
| prose | `C.P2.S2` | R1 R5 → R1 R3 | COND `Where` → `If`, on the objection's own stated falsifier |
| prose | `C.P2.S4` | R1 R2 → R1 R2 | INFO asyndeton restored (an added *"and"* had made a contrast into a coordination) |
| prose | `C.P3.S1` | R1 → R1 | DET *"that distinction"* → *"the distinction"*; added relativizer removed |
| prose | `C.P3.S2` | R1 R5 → R1 | COND open indicative restored (was a counterfactual *"Were someone to show … would lose"*), on the objection's own defeasibility condition |
| prose | `C.P4.S1` | R1 R2 R5 → R1 R5 | COND `should` → `if`; INFO end-shifted *"included"* reverted to *"including"* |
| prose | `C.P4.S2` | R1 R3 R4 → R1 R3 | ANTE *"That"* left as *"That"*; R4 label dropped |
| prose | `C.P4.S3` | R2 → R1 | INFO object fronting reverted |
| prose | `C.P5.S2` | R2 R3 → R3 | INFO PP fronting reverted; HEDGE *"possible"* restored (was *"possibly"*) |
| prose | `C.P6.S1` | R1 R5 → R1 | COND `Should` → `If` |

### 2b. Units relabelled only (13)

Text unchanged; the `rules` cell now names the operation actually performed.

| arm | unit | was → now |
|---|---|---|
| fcl | `B.P2.S1` | R1 R2 → R1 |
| fcl | `B.P3.S5` | R3 R1 → R1 R3 |
| fcl | `B.P4.S1` | R1 R2 → R1 R3 |
| fcl | `B.P4.S2` | R2 R3 → R1 R3 |
| fcl | `K.o2.text.S1` | R2 R3 → R1 R2 R3 |
| fcl | `K.o3.bearing.S1` | R2 R3 → R1 R3 |
| fcl | `K.c2.scope.S1` | R2 → R3 |
| fcl | `K.p1.text.S1` | R2 R3 → R1 R3 |
| fcl | `K.u1.action.S1` | R1 R2 → R1 R3 |
| prose | `B.P1.S2` | R1 → R1 R3 |
| prose | `B.P2.S1` | R2 R3 → R1 R3 |
| prose | `B.P3.S1` | R1 R3 → R3 |
| prose | `C.P5.S1` | R1 R2 → R1 R3 |

### 2c. Units untouched (12)

`fcl B.P2.S2`, `fcl B.P2.S4`, `fcl B.P2.S6`, `fcl B.P5.S1`, `fcl B.P6.S1`,
`fcl K.o1.text.S1`, `fcl K.c1.scope.S1`, `fcl K.o4.text.S1`, `prose B.P3.S4`,
`prose C.P1.S1`, `prose C.P2.S3`, `prose C.P3.S3`.

### 2d. What `prepare` now refuses

Added to the existing coverage, reconstruction, FCL-structure and non-identity checks:

* **(a) FCL-1 string-field record integrity, record by record.** Each record's `id`,
  `type`, field set, every reference array (`target`, `depends`, `mentions`, `revises`,
  `withdraws`), every non-string field, the document's `uptake` list and its `language`
  tag are compared individually, so the refusal names what moved:
  `RECODING_CHANGED_FCL_RECORD_IDS`, `…_RECORD_TYPE`, `…_RECORD_FIELDS`,
  `…_REFERENCES`, `…_NON_STRING_FIELD`, `…_UPTAKE`, `…_LANGUAGE`.
* **(b) Hedge force, per unit.** 23 declared marker families — `if`, `unless`,
  `whether`, `may`, `might`, `can`, `could`, `will`, `would`, `shall`, `should`, `must`,
  `ought`, `need`, `deserve`, `necessarily`, `probably`, `possibly`, `perhaps`,
  `merely`/`just`/`simply`/`only`, `seem`, `appear`, and a negation family — counted in
  original and recoded after contraction expansion, any difference refused as
  `RECODING_HEDGE_FORCE_CHANGED`. The family table is published in `RECODING_TABLE.md`
  and is part of the material, so it is declared before the evidence.
* **(c) Rule labels.** Every unit's labels must be a subset of the declared rule set
  (`RECODING_UNDECLARED_RULE`); the report names the declared rules that went unused.
* Quoted spans compared in order (`RECODING_QUOTATION_CHANGED`), so a recoding cannot
  rewrite what the objection quotes from the account or the problem.

None of this establishes constituent-role preservation — that is a reading, and the
published unit table is what makes it checkable. What it does is refuse the three
mechanically detectable ways this recoding went wrong the first time.

---

## Part 2.5 — Spot-check closures

After the re-read above, an **independent spot-check** re-read all 85 units against the
originals and re-ran the mechanical verification from a separate implementation (56
checks, 0 failures). It returned **3 violates, 23 doubtful, 59 preserves**, plus four
documentation findings. Every violate and every doubtful is closed here. The governing
decision is the same one Part 2 records: **revert the text or correct the label; never
declare a new rule to license what was done.**

**30 units changed** — 25 in recoded text, 15 in rule label (10 of them in both).

| arm | unit | class | rules (was → now) | recoded, was | recoded, now |
|---|---|---|---|---|---|
| fcl | `B.P4.S1` | **violates** | R1 R3 → R1 | A point about phrasing is also worth flagging. | There is also an issue of phrasing worth flagging. |
| fcl | `B.P4.S2` | **violates** | R1 R3 → R1 | According to the account the problem as posed is "practical" and the material is "thin." Those are characterizations supplied by the author, not features of the situation. | The account states that the problem as posed is "practical" and the material is "thin." Those are the author's characterizations, not features of the situation. |
| fcl | `K.o1.text.S1` | **violates** | R1 R3 → R1 | There is insufficient support for the account's recasting of the dispute as chiefly a problem of ambiguity/specification. | The account's recasting of the dispute as chiefly a problem of ambiguity/specification is insufficiently supported. |
| fcl | `B.P2.S3` | doubtful / content | R1 R5 (unchanged) | On occasion they settle who will do a task, and afterwards fall out over what the settlement meant. | On occasion they agree who will do a task, and afterwards fall out over what the agreement meant. |
| fcl | `B.P2.S7` | doubtful / content | R1 R5 (unchanged) | Yet the same observation is equally consistent with an alternative reading: the agreement was clear enough, and the later dispute is about whether the terms still hold given changed circumstances, or about who has standing to enforce them. | Yet the same observation is equally consistent with an alternative reading: the agreement was clear enough, and the later dispute is about whether the terms still bind given changed circumstances, or about who has standing to enforce them. |
| fcl | `B.P3.S1` | doubtful / content | R1 R2 R5 (unchanged) | In o1 the account acknowledges this, yet it then adopts the ambiguity hypothesis as the working one and discounts the alternatives. | In o1 the account acknowledges this, yet it then treats the ambiguity hypothesis as the working one and gives less weight to the alternatives. |
| fcl | `B.P3.S4` | doubtful / content | R1 R3 (unchanged) | A fall in recurrence would fit the ambiguity hypothesis, but the rival hypotheses forecast a different pattern: recurrence might fall on the items specified and resurface as fresh complaint items, or fall for a time and then come back at the next change of circumstances. | A fall in recurrence would be consistent with the ambiguity hypothesis, but the rival hypotheses forecast a different pattern: recurrence might fall on the items specified and resurface as fresh complaint items, or fall for a time and then come back at the next change of circumstances. |
| fcl | `B.P5.S1` | doubtful / content | R1 R2 (unchanged) | Probably the most useful move in the account is the one it relegates to second place: that the avoidance may concern the form of the conversations rather than the chores. | Probably the most useful move in the account is the one it treats as secondary: that the avoidance may concern the form of the conversations rather than the chores. |
| fcl | `B.P5.S2` | doubtful / content | R1 R2 R5 → R5 | That deserves to be nearer the front, since it is the genuinely distinctive part of the situation and the part the specific-negotiation advice does not address. | That deserves to be nearer the front, since it is the part of the situation that is genuinely distinctive and that the specific-negotiation advice does not address. |
| fcl | `K.c2.text.S1` | doubtful / content | R2 R3 → R3 | A lopsided or resented arrangement specified more tightly is still a lopsided or resented arrangement with clearer paperwork; load imbalance and legitimacy are not addressed by specification alone. | A lopsided or resented arrangement specified more tightly is still a lopsided or resented arrangement with clearer paperwork; specification alone does not address load imbalance or legitimacy. |
| fcl | `K.o1.text.S2` | doubtful / content | R1 R3 (unchanged) | The reported pattern - later disagreement about what an agreement meant - is equally consistent with a renegotiation problem or a legitimacy problem under changed schedules, and those alternatives are discounted by the account after it has named them in its own o1. | The reported pattern - later disagreement about what an agreement meant - is equally consistent with a renegotiation problem or a legitimacy problem under changed schedules, and those alternatives are given less weight by the account after it has named them in its own o1. |
| prose | `B.P2.S3` | doubtful / content | R1 (unchanged) | Taken the other way round, the avoidance is the load-bearing fact and the chore disputes are the place where an already-shifting household keeps failing to talk. | Taken the other way round, the avoidance is the load-bearing fact and the chore disputes are where an already-shifting household keeps failing to talk. |
| prose | `B.P2.S4` | doubtful / content | R3 → R1 | On that reading, the memory-gap conjecture describes the surface, and a written record may simply give the same unresolved conversation a new medium. | On that reading, the memory-gap conjecture is a description of the surface, and a written record may simply give the same unresolved conversation a fresh medium. |
| prose | `B.P4.S2` | doubtful / content | R1 R5 → R1 R3 | If the avoidance is the mechanism by which the group has lost the ability to hold the conversation, then a weekly check-in is a proposal to do more of what has already failed, addressed to the person who withdrew from it. | If the avoidance is the mechanism by which the group has lost the ability to hold the conversation, then a weekly check-in is a proposal to do more of the thing that already failed, addressed to the person who withdrew from it. |
| prose | `C.P3.S2` | doubtful / content | R1 (unchanged) | If someone shows that in a household of this kind the two are not separable in practice, that the act of writing something down does shift the norms, my criticism loses some of its bite. | If someone demonstrates that in this kind of household the two are not separable in practice, that the act of writing something down does shift the norms, my criticism loses some of its bite. |
| prose | `C.P4.S1` | doubtful / content | R1 R5 (unchanged) | As to the local trial: if a written record or check-in is attempted, I would want the result reported in the household's own description of it, including the case where the avoiding friend reads the note as surveillance. | As to the local trial: if a written record or check-in is attempted, I would want the result reported as the household describes it, including the case where the avoiding friend reads the note as surveillance. |
| fcl | `B.P3.S2` | doubtful / structure | R1 R2 R3 R5 (unchanged) | As a starting point, if one has to be chosen, that is defensible, but the diagnostic step the account itself proposes - try two or three concrete items and see if recurrence falls - is weaker than it looks, since a specification move can lower friction while the driver underneath is load imbalance or resentment. | That is a defensible starting point if one has to be chosen, but the diagnostic step the account itself proposes - try two or three concrete items and see if recurrence falls - is weaker than it looks, since a specification move can lower friction while the driver underneath is load imbalance or resentment. |
| fcl | `B.P3.S3` | doubtful / structure | R2 → R1 | A lopsided arrangement with tighter specs is still a lopsided arrangement, just with clearer paperwork. | Tighter specs on a lopsided arrangement are still a lopsided arrangement, only with clearer paperwork. |
| fcl | `B.P4.S3` | doubtful / structure | R1 R2 R3 (unchanged) | As a caution, calling the material thin is unobjectionable, but the thinness is then used by the account to license a good deal of construction (the three-column spec, the low-pressure approach to the withdrawing friend, the step-5 threshold). | As a caution, calling the material thin is fine, but the thinness is then used by the account to license a good deal of construction (the three-column spec, the low-pressure approach to the withdrawing friend, the step-5 threshold). |
| fcl | `K.o3.bearing.S1` | doubtful / structure | R1 R3 → R3 | Prescriptive work that the stated evidence does not carry is being done by the order in which the account's recommendations are placed. | The order in which the account's recommendations are placed is doing prescriptive work that the stated evidence does not carry. |
| fcl | `K.o3.text.S2` | doubtful / structure | R3 (unchanged) | Tentative probes are supported by thin material; presenting that sequence as the natural order is not supported by it. | Thin material supports tentative probes; it does not support the presentation of that sequence as the natural order. |
| prose | `B.P2.S2` | doubtful / structure | R3 (unchanged) | Under the account's reading the first element is made primary and the third is demoted to a symptom — 'avoidance is a symptom worth understanding before it's treated as a problem to correct.' The material does not force that ordering. | Under the account's reading the first element is made primary and the third is demoted to a symptom — 'avoidance is a symptom worth understanding before it's treated as a problem to correct.' That ordering is not forced by the material. |
| prose | `B.P3.S1` | doubtful / structure | R3 → R1 | A second difficulty arises. | There is a second difficulty. |
| prose | `B.P3.S4` | doubtful / structure | R3 (unchanged) | Who said what is settled by a written record. | A written record settles what was said by whom. |
| prose | `B.P4.S1` | doubtful / structure | R2 → R1 | The account also names, without resolving it, its own unresolved dependency: the proposal assumes all three flatmates can talk without a mediator, 'which the avoidance itself puts in question.' That is not a peripheral caveat. | The account also names its own unresolved dependency without settling it: the proposal assumes all three flatmates can talk without a mediator, 'which the avoidance itself puts in question.' That is not a peripheral caveat. |
| fcl | `K.c1.scope.S1` | label only | R1 → R1 R5 | *(unchanged)* | *(unchanged)* |
| fcl | `K.c2.scope.S1` | label only | R3 → R1 | *(unchanged)* | *(unchanged)* |
| fcl | `K.u1.action.S1` | label only | R1 R3 → R1 R3 R5 | *(unchanged)* | *(unchanged)* |
| fcl | `K.u1.text.S1` | label only | R1 R3 R5 → R1 R3 | *(unchanged)* | *(unchanged)* |
| prose | `C.P2.S2` | label only | R1 R3 → R1 R3 R5 | *(unchanged)* | *(unchanged)* |

**Why each class was closed the way it was.**

* **violates (3).** All three applied an operation with no rule in the declared set: an
  existential-`there` inserted (`K.o1.text.S1`, in record `o1`'s own `text` — the field
  that states the criticism's target and alleged defect), an existential-`there` deleted
  (`B.P4.S1`), and a definite possessive predicate nominal turned into a bare plural with
  an equative → predicational shift (`B.P4.S2`). Each is now `R1` alone, with the target
  *z* back in the subject of the defect predication and the definite possessive restored.
* **doubtful / content (13).** Each changed the force of an evaluative or relational
  predicate, or stranded a definite antecedent, without the hedge counter being able to
  see it: `bind` → `hold`, `consistent with` → `fit`, `treats`/`downweights` →
  `adopts`/`discounts`, `treats as secondary` → `relegates to second place`, `issue` →
  `point`, `or` → `and` under a negation, `agree`/`agreement` → `settle`/`settlement`
  (which stranded "the agreements" in `B.P2.S6–S7`), `is a description of` → `describes`,
  and four determiner or definiteness moves. The original wording is restored in every
  one; where that left the unit with no operation, the operation was moved elsewhere in
  the unit (prose `B.P2.S4`: `new medium` → `fresh medium`; prose `C.P3.S2`: the `R1`
  moved onto the verb, `shows` → `demonstrates`).
* **doubtful / structure (9).** Backgrounded concessions, NP-head switches, double
  passives and a cataphor — emphasis operations the rule set does not license even where
  the propositional content survives. `fcl B.P3.S3` is reverted with `just` → `only`
  (the same `MERELY` family, so the hedge counter still passes); `fcl K.o3.text.S2` and
  `K.o3.bearing.S1` keep their `R3` but apply it to the object and the subject nominal
  respectively, so the constant topic survives.
* **label only (5).** No text change: the spurious `R5` dropped where no connective is
  substituted (`fcl K.u1.text.S1`), `R5` added where one is (`fcl K.u1.action.S1` `so` →
  `so that`; `fcl K.c1.scope.S1` `given` → `in view of`; prose `C.P2.S2` `nonetheless` →
  `nevertheless`), and `fcl K.c2.scope.S1` relabelled `R1`, since a compound → PP
  alternation is a lexical substitution and not a voice one. Prose `B.P4.S2` also lost a
  spurious `R5` and gained the `R3` its nominal alternation actually performs.

**One deviation from the spot-check's suggested wording, recorded.** For prose `B.P3.S4`
the spot-check proposed `A written record settles who said what.` — which is
**byte-identical to the original unit**. The material's own contract forbids that: every
unit must carry at least one declared operation (`RECODING_UNIT_RULES`), and a unit whose
recoded text equals its original would make its `rules` cell false and would fail
`RecodingReRead.test_no_unit_is_the_identity_and_every_label_is_declared`. The point of
the spot-check's note is the **constant topic** — the following sentence's "It does not
settle…" needs the written record to stay the subject. That is what was applied: the
matrix clause is active with `A written record settles` restored, and the `R3` voice
alternation is moved into the object clause — `A written record settles what was said by
whom.` The topic and the settles / does-not-settle parallelism with `B.P3.S5` both hold,
and the unit is not the identity. (The spot-check made the same accommodation itself for
`fcl B.P3.S3`, choosing `only` over a bare revert to `just` for exactly this reason.)

**Documentation findings, closed.**

1. **The information-structure invariant was literally false.** `R3` licenses
   active/passive alternation, which *is* a topic/focus reassignment, and 16 fcl and 14
   prose units exercise it. The invariant now reads *"no information-structure operation
   beyond the topic/focus reassignment intrinsic to `R3` (active/passive alternation)"*,
   with the excluded list spelled out (clefting, pseudo-clefting, topicalisation, equative
   inversion, existential-`there` insertion or deletion, subordination ↔ coordination,
   assertion ↔ presupposition) and the determiner/definiteness clause unchanged. Reworded
   in `material.json` (both arms), `RECODING_TABLE.md`, PLAN §4(b) and NOTES §2.
2. **`R2` was defined as clause reordering and used for PP and adverbial fronting.**
   Broadened to *"reordering of constituents (clauses, phrases, adverbials) inside one
   unit"*, with the restriction unchanged and an explicit exclusion of NP-head operations.
   The one unit that had used `R2` for an NP-head switch (`fcl B.P3.S3`) is reverted, so
   it no longer needs `R2` and is now `R1`.
3. **Spurious and missing `R5` labels.** Fixed as listed above.
4. **The hedge-force counter is necessary but not sufficient, and now says so.** A new
   `recoding.hedge_marker_limits` paragraph is carried in the material and rendered into
   `RECODING_TABLE.md`, and the same paragraph is in PLAN §4(b): the counter refuses a
   change in the *count* of a declared marker family and nothing else; it is blind to
   evaluative and relational predicates (`consistent with` → `fit`, `downweight` →
   `discount`, `issue` → `point`, an `un-` litotes, `or` → `and` under negation,
   get-passive → be-passive) and to which constituent a preserved marker attaches to;
   those are checked **by reading**, and by the published two-reviewer re-read.
5. **`not_exercised` was not exhaustive.** It now lists every reverted unit by id — 15 in
   the fcl document, 19 in the prose — and gains a fourth entry, *evaluative and
   relational predicate substitution*, naming the nine units whose predicate force was
   restored. The three violates are inside the list, which is where the earlier version
   failed.

**Two further faults, found on the implementer's own re-read of the closed units.** The
closure was followed by an independent re-read of only the 30 changed units, against the
originals, and it turned up two things the spot-check had not:

* **`fcl K.c2.text.S1` still carried `R2`.** Its subject alternation — *"A tighter
  specification of a lopsided or resented arrangement"* → *"A lopsided or resented
  arrangement specified more tightly"* — switches the NP head, which the newly broadened
  `R2` explicitly excludes; the operation is the `R3` nominal ↔ participial alternation,
  which licenses it and brings the reordering with it. Relabelled **`R3`** alone. (This
  is what distinguishes it from `fcl B.P3.S3`, which performed the same head switch with
  no voice or nominal alternation at all and is therefore reverted.)
* **The determiner clause of the invariant was false in the same way the
  information-structure clause had been.** An `R1` lexical paraphrase and an `R3`
  verbal ↔ nominal alternation each carry a determiner with them — `falling recurrence`
  → `a fall in recurrence` (fcl `B.P3.S4`, `K.o2.bearing.S1`, `K.c2.consequence.S1`),
  `presenting that sequence` → `the presentation of that sequence` (fcl `K.o3.text.S2`,
  the wording the spot-check itself proposed), `being able to hold` → `the ability to
  hold` (prose `B.P4.S2`), `a commitment to hold` → `to commit to holding` (prose
  `C.P1.S1`) — and 26 units show a determiner-token delta. The invariant now reads *"no
  determiner or definiteness operation **of its own**: no `the` ↔ `a`, `the` ↔
  `this`/`that` or bare ↔ determined change to an otherwise unchanged referring
  expression"*, which is what the four reverted determiner units (prose `B.P2.S3`,
  `B.P4.S2`, `C.P3.S2`, fcl `B.P5.S2`) had each violated and what no surviving unit does.

**One change that is not a spot-check closure: the per-endpoint completion ceiling.**
Folded in before the identity was frozen, on live evidence published under
**REC-20260914-S**. `max_tokens` is now declared **per endpoint** — 8192 for
`deepseek-flash` (it sends no reasoning on the wire), **32768** for the five Ollama
endpoints, authorised maximum 32768 — and is frozen twice, in `endpoints[].max_tokens`
and in `ceilings.max_tokens`, which `prepare` refuses to let disagree
(`MATERIAL_ENDPOINT_MAX_TOKENS`); every one of the 240 built payloads must carry its own
endpoint's value (`CEILING_NOT_APPLIED`). The evidence: F001
(`experiments/diagnostics/F001-fork5-multifamily`), `occurrence-04` `ollama/glm-5.3` and
`occurrence-05` `ollama/kimi-k3`, both run at 8192 — **five** nodes returned
`INCOMPLETE_GENERATION`, `finish_reason "length"`, `completion_tokens 8192`,
`reasoning_content_present true` and **no content at all**, and **two** more came back
PARTIAL on the same signature. The transport's own argument validation accepts
1…393216, so 32768 is inside its range, and the preflight builds all 240 payloads
through that validation. The raise does **not** manipulate reasoning — `temperature`,
`thinking` and `reasoning_effort` are still never sent — and it **rescues no cell**: a
delivery that hits even the raised ceiling is still PARTIAL-and-unresolved or a recorded
refusal, compared against nothing (FW5:634). Stated in PLAN §5 (with the endpoint table
now carrying a `max_tokens` column) and §6, and in NOTES D15. Pinned by
`Preflight.test_max_tokens_is_per_endpoint_and_reaches_every_payload`,
`…test_the_raised_ceiling_is_inside_the_transports_own_validation_range`,
`…test_a_material_whose_ceiling_table_and_endpoint_disagree_is_refused`,
`…test_a_payload_built_with_another_endpoints_ceiling_is_refused`, and
`PreRegistrationDocument.test_section_5_and_6_state_the_raised_ollama_ceiling_and_its_evidence`.
Its one methodological cost is recorded rather than hidden: the six endpoints no longer
share a single ceiling, so a `deepseek-flash`-vs-Ollama difference carries one more
uncontrolled difference (§11 L7).

**The table and the material can no longer disagree.** `.build/build_material.py` now
writes `RECODING_TABLE.md` itself, by calling the driver's own `render_recoding_table` on
the material bytes it has just written — the same function `prepare` calls — so the
published table is a rendering of the frozen material by construction, not a file kept in
step by hand.

---

## Part 3 — verification performed

* `python3 tests/test_contrast_triple_study.py` → **`Ran 106 tests in 18.999s` … `OK`**
  at the spot-check closure with the per-endpoint ceiling folded in (`Ran 101 tests in
  19.086s … OK` at the adversarial-review close; baseline before either: 42 tests).
* `prepare` run twice, from two different working directories
  (`scratchpad/contrast` and `/home/user/miniReason`), into two fresh outputs:
  both minted `plan_id`
  `34f510170282f374cf1132eb7b2334030a3b39965c97313b36e79fb746f3184f`
  and `cmp` reports the two `plan.json` files **byte-identical**.
* The mechanical recoding checks were re-run over the closed material and pass in both
  arms: every original unit mapped exactly once (50 fcl, 35 prose); the recoded document
  reconstructed **from the `recoded` column alone** equals the frozen recoded bytes, and
  the same reconstruction over the `original` column equals the frozen original bytes, in
  body and commitments, in both arms; the FCL-1 structural invariants (record ids, types,
  field sets, every reference array, every non-string field, `uptake`, `language`) are
  byte-identical between original and recoded; 23 hedge/modal marker families counted in
  all 85 units with no count changed; quoted spans verbatim and in order; every unit's
  rule labels a subset of `{R1..R5}`, with `R4` reported declared-and-unused in both arms;
  and no unit is the identity.
* `verify --output <occ>` on the prepared occurrence returns `{"verified": true}` with
  the same `plan_id`, re-hashing the source pins and both transport pins.
* The staged `RECODING_TABLE.md` is byte-identical to the driver's rendering of the
  frozen material (asserted by `Recoding.test_recoding_table_file_matches_the_material`).
* No write to `/home/user/miniReason`: `git status` there shows nothing from this work
  and no `C001-contrast-triple` path exists in the repository.
* No provider call: the preflight builds 240 payloads through an `OfflineProvider` with
  an empty script and asserts `provider_calls == 0`; every test uses either that
  provider or the scripted stand-in. No `.env` file and no credential value was read,
  printed or written.

## Part 4 — what is still open, and deliberately

* **The transport pin is a moving target while the provider is under revision.** The
  pinned bytes are the staged provider module and registry as of this build. If that
  module changes, `prepare`/`verify`/`run`/`audit`/`table` stop with
  `TRANSPORT_PIN_MISMATCH` and the material must be rebuilt, minting a new `plan_id` —
  which is the declared behaviour (PLAN §13), not a fault.
* **The §5 smoke-test claim is still unreceipted.** PLAN §3 now says so explicitly and
  NOTES §6 item 4 carries the owed receipt; C001 makes no live call, so it cannot supply
  one itself.
* **R4 is declared and unexercised.** The alternative — removing it from the rule set —
  would hide the fact that a deixis operation was considered and found unlicensable at
  this grain. It is recorded in `not_exercised` instead.
* **Constituent-role preservation remains a reading.** No mechanical check establishes
  it; the 85-row published table is what lets a reader dispute one row rather than the
  whole recoding, and the re-read is recorded here so a reader can see what was changed
  and why.
