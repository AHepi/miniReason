# Working answer

## UC4 — Adversarial mapping of FW5 onto the pilot harness's own records

### 1. Information needed; available evidence

Available semantic material (only these):
- `FW5-excerpts` — pinned excerpt set of the reading edition (path `docs/sources/FW5-explanatory-construction.md` names the edition; edition SHA256 given in premises). Pinned units L33…L1372 only. No unread portions may be inferred.
- `pilot-offline-episode` — offline scripted fixture (provenance field itself says `NOT a provider observation`). It records a `task`, five `events` (seal/route/spawn/assemble/verify), one `child`, one `assembly`, and a `terminal` block.

Information **not** accessible here (per premises and the P-A2 description): arbitrary path access, repository search, reader briefs, derived-properties memoranda, unread FW5 material, live hidden organization, a real provider episode, any recorded critical episode.

### 2. Declared question/respect, boundary, grain, role bindings, obligations, contrasts (declared **before** outcomes)

- **Question / respect (κ):** *Which FW5 structural notions, if any, are supported by the harness's own records, and at what grain?* Respect: structural-support / attribution-fit (not production of the answer 42, not performance).
- **Boundary:** the pinned FW5 excerpt set + the offline episode projection. Nothing else.
- **Grain:** record-field grain — each mapping must name an exact JSON field (or exact FW5 clause) as its anchor, not a family of fields.
- **Role bindings attempted (host-level, not FW5-level):** `route` event → candidate route construction; `child.template_id` → candidate role; `assembly.dependencies` → candidate role bindings; `terminal.verification_status` → candidate verification.
- **Obligations:** cite exact FW5 text; cite exact record field; attack each mapping with a concrete counterexample or missing definition; preserve rejected versions; name reversal evidence; do **not** force FW5 to win or lose; distinguish the four failure kinds at the end.
- **Contrasts I will use** (candidate contrast contract for this exercise): presence/absence of a named record field; offline vs live provenance; single-event vs structural subnetwork; performed-and-recorded vs merely requested.

### 3. Candidate mappings, predictions, attacks, revisions

Notation: field lookups are RFC-6901-like JSON Pointers into `pilot-offline-episode` decoded text.

---

#### Mapping M1 — ‘active route’ (FW5 L601) ↔ `events[a0002].choice="route"`, `state="SEALED_TASK"`

**Prediction if mapping holds:** the record's route event would name a subnetwork joining a *represented input* to a *named operative result*, and its designation would need to “satisfy the corresponding component relations and role bindings”.

**Attack (recorded counterexample):** the record's `route` event is `{id:"a0002", utc:…, choice:"route", state:"SEALED_TASK"}`. It carries **no** input port, no output port, no component-relation field, no role-binding field. The only subnetwork-like structure in the episode is `assembly.dependencies = {"c0001":"dd23…"}` — a hash map from one dependency to one digest, i.e. a single node, not a connected subnetwork.

**Exact record field targeted:** `/events/1` (choice="route") and `/assembly/dependencies`.

**Exact FW5 clause targeted (L601):** an active route is “a connected subnetwork of those actual occurrences joining the named represented input to the named operative result. Its designation must satisfy the corresponding component relations and role bindings; it is not inferred from the presence of a similar sentence in a record.” The final clause explicitly forbids exactly the inference M1 would need (“route” label ⇒ active route).

**Revision (preserved, rejected version):** *M1-rejected.* M1 fails as a **missing application criterion**: the record supplies a label but none of the route-identifying fields (input port, output port, directed connection, component relations, role bindings).

**Defended version (M1′):** the record supplies **route-plumbing facts at host grain only** — call ordering (`seal→route→spawn→assemble→verify`) and a dependency hash map. FW5-compatible mapping stops at: *“a route event was recorded; whether the recorded organization is an FW5-level active route is not decidable from this projection.”*

**Reversal evidence:** a live/host record exposing, for this episode, (a) a named represented input occurrence, (b) a named operative-result occurrence, (c) explicit directed connections between them, (d) explicit component-relation/role-binding fields whose values satisfy those relations. Also, a nonconstant-dependence witness on the relevant represented distinction (FW5 L601, later sentence) would be required for reason-use/contribution variants.

---

#### Mapping M2 — ‘contrast contract’ (FW5 L123) ↔ `events[*].state` + `terminal.status`

**Prediction if mapping holds:** the record would declare which edits/boundary conditions are in the claim, a distinguished baseline, a respect κ, and material distinctions for the question.

**Attack (concrete counterexample):** FW5 L123 states the contrast contract “fixes the input changes, component changes, and distinctions material to that question. It includes the baseline and is not identified with a collection of performed experiments.” The episode's `state` and `terminal.status` fields are status labels on the same single execution — that is precisely “a collection of performed experiments” (here, one), not a declared set of input/component changes and a declared baseline.

**Exact record field targeted:** `/events/0..4/state`, `/terminal/status`.

**Exact FW5 clause targeted (L123):** “…fixes the input changes, component changes, and distinctions material to that question. It includes the baseline and is not identified with a collection of performed experiments.” Also relevant: L140 — “The question contract is not immune. It can be criticized and replaced. What is prohibited is changing it during an assessment without recording the resulting change in what is claimed.” Nothing in the episode records such a change.

**Revision (preserved, rejected version):** *M2-rejected.* M2 fails as an **unsupported mapping**: the episode has zero declared contrasts, zero baselines, zero content-changing vs content-preserving pairs. The offline projection's own `omissions` field says: “no recoding intervention or historical repertoire is recorded here.”

**Defended version (M2′):** the **contrast across episodes** (offline vs live; task-sealed vs verified) is a *contrast we construct as readers*, not a contrast the record declares. FW5 forbids silently substituting the construct for the declared contract: it must be recorded as an *outcome of criticism* (L140), not treated as if already in the record.

**Reversal evidence:** a record field enumerating distinct input edits, component edits, a distinguished baseline element, and the respect κ governing this run — e.g., an explicit `contrast_contract` field with at least one content-changing case and one content-preserving recoding (L630's contrast requirement).

---

#### Mapping M3 — ‘elimination without a truth machine’ (FW5 L661, L665–L676, esp. K3) ↔ `terminal.verification_status="verified"` + `terminal.verification_scope`

**Prediction if mapping holds:** the record would show that a passing execution is a limited proposition (equality with source bytes / validity relative to formal premises) and that non-observation of an outcome contradicts only the conjunction T∧B∧I, never T alone.

**Attack (concrete counterexample from the record and FW5):** FW5 L661 says “A passing execution cannot make the program's specification, the model of the experiment, or the claimed relevance immune to prose criticism.” The record's `terminal.verification_scope` is the single sentence *“The answer is the decimal representation of 6 times 7.”* — that is a limited proposition, exactly the kind FW5 permits; but the record does **not** contain any argument showing negated outcomes derived from K3, nor any labelled auxiliary set B or observation-interpretation set I. So the record instantiates the *positive half* of M3 (a limited machine check that does not, by itself, immunize the spec) and does **not** instantiate the elimination structure on which K3 turns.

**Exact record field targeted:** `/terminal/verification_status`, `/terminal/verification_scope`.

**Exact FW5 clauses targeted:** L661 as above; L665–L676 (“It does not yield ¬T without additional premises about B and I. … This is not an argument against testing. It states exactly what the test contradicts and where further criticism can matter.”).

**Revision (preserved, rejected version):** *M3a (strong form) rejected* — the record does not perform an FW5-style elimination; it performs a bounded check.

**Defended version (M3b):** the record supplies a **positive exemplary instance** of FW5 L661's first sentence (limited machine check whose interpretation has real consequences) and a **null instance** of K3 (no negated observation is present, so no elimination inference is licensed either way). Calling this “elimination without a truth machine” would be a **source-clause substitution**: it would read K3 as a description of *any* passing check, whereas K3 is a schema for *failing* checks with specified B and I.

**Reversal evidence:** a record with (a) a stated T∧B∧I→O schema, (b) an established ¬O, and (c) explicit auxiliary/interpretation fields B and I, plus (d) a recorded prose-criticism step against the spec or relevance of the check.

---

#### Mapping M4 — ‘critical episode’ (FW5 L773, L609, L628, L630, L634, L1052) ↔ any field combination in the episode

**Prediction if mapping holds:** the record would contain (per L773) a recognized difficulty, a represented target available before the criticism, a conjectural objection, and a content-sensitive response with a resulting situation; per L628 a reason-use witness mapping the objection organization into the response suborganization and lying on an active dependency route; per L630 its contrast contract must include a content-changing case, a content-preserving recoding, and the objection/carrier distinction.

**Attack (missing definition and absent fields):** the episode has **no** objection field, **no** defect field, **no** grounds field, **no** response suborganization, **no** role-binding fields, and **no** content-change/carrier contrast. The projection itself states: *“No live hidden organization, no critical objection/return/use episode, no recoding intervention or historical repertoire is recorded here.”* Per FW5 L634, “An observer may lack the data needed to establish the witness. That makes the attribution unresolved; it does not prove either understanding or its absence.”

**Exact record field targeted:** the string field `/omissions` (and the absence of any corresponding positive field).

**Exact FW5 clauses targeted:** L773 (“A complete critical episode contains a recognized difficulty, a represented target available before the criticism of it, a conjectural objection, and a content-sensitive response with a resulting situation.”); L628; L630; L634; L1052 (“At least one alternative subsidiary result in the contract must permit a different use-state…”).

**Revision (preserved, rejected version):** *M4-rejected.* No FW5-level critical episode is recorded. Also note FW5 L640's caution even about partial analogues: “A source's appearance in a prompt is a delivery fact. A named field asking for a criticism is an invitation fact.” The episode records neither a delivery nor an invitation of an objection, so this caution does not even need to be applied to rescue M4 — M4 has no candidate referent.

**Defended version:** the correct FW5-consistent result for the critical-episode notion on this record is **unresolved / not_found**, not “present” and not “absent in the world” (L634).

**Reversal evidence:** a record containing (a) a represented target field populated before a later objection field, (b) at least one conjectural objection with defect and grounds, (c) a response suborganization with role-binding fields, (d) at least one content-changing contrast and one content-preserving recoding in the same contract, and (e) an active-dependency-route link between the objection map and the response occurrence.

---

### 4. Summary table (human-inspectable)

| Notion (FW5) | Candidate record anchor | Prediction | Attack type | Rejected version | Defensible version | Reversal evidence |
|---|---|---|---|---|---|---|
| Active route (L601) | `/events/1` (choice=route) | Names input→result subnetwork with role bindings | Missing application criterion | ‘route label ⇒ active route’ | Host-level call ordering + dependency hash only | Live record with input port, output port, connections, component relations, nonconstant dependence |
| Contrast contract (L123) | `/events/*/state`, `/terminal/status` | Declares edits, baseline, κ, material distinctions | Unsupported mapping | ‘status labels are a contrast contract’ | Reader-constructed cross-episode contrast, must be recorded per L140 | Field enumerating input/component edits, baseline, κ, content-changing + content-preserving pair |
| Elimination w/o truth machine (L661, K3) | `/terminal/verification_status`, `/terminal/verification_scope` | T∧B∧I→O schema plus recorded ¬O | Source-clause substitution (K3 read as generic pass-license) | ‘verified ⇒ elimination inference’ | Exemplary bounded machine check (L661 first sentence); no K3 instance | Explicit T/B/I fields, established ¬O, prose criticism step |
| Critical episode (L773, L609, L628, L630, L634, L1052) | `/omissions` (asserts absence) | Target, objection, defect, grounds, response suborganization, contrast contract | Missing definition + absent fields | ‘any episode = critical episode’ | Unresolved; FW5 L634 forbids reading absence-of-data as absence-of-capacity | Record with target, objection, defect, grounds, role bindings, content-preserving recoding, active-route link |

### 5. Failure-kind classification (required distinction)

- **Source-clause challenge:** none. No pinned clause was shown to be internally inconsistent or false on its face; on the contrary, L601's “is not inferred from the presence of a similar sentence in a record” and L634's unresolved-attribution clause *foreclosed* the mappings we were tempted to make.
- **Missing application criterion:** M1 and M3a. The record lacks the identifying fields FW5 requires to *apply* the notions (route ports/component relations; T,B,I structure).
- **Unsupported mapping:** M2 and M4. The record holds no referent to attach the notion to; the projection's own `omissions` string confirms this for M4.
- **Instrument failure:** none observed. The offline fixture and the pinned excerpts loaded within their declared byte ranges. The fixture is explicitly *not* a provider observation, which is a **provenance** fact, not an instrument failure.

### 6. Continuation log (provisional, pre-verification)

- **Pass 1 (this artifact).**
  - Artifact ref: none yet assigned (worker output).
  - Verification ref/result: **not yet verified**; nothing is claimed passed.
  - Remaining calls: assumed 299-ish, strictly bounded above by 300 LOGICAL calls per the owner contract; must be confirmed against host-reported counters at the control step.
  - Decision proposed: **CONTINUE** for a second pass.
  - Reason/stop rule: stop when further passes would require material outside the pinned excerpts (unread FW5 text, unread record fields, a second-offline-mechanics arm) — i.e., when the next step would need evidence the harness cannot supply. Not yet met.
  - Unresolved commitments: exact byte-span resolution of the quotes below; whether a live record exposes the route/contrast/elimination/episode fields named in the reversal-evidence column.
  - Intended next route: one targeted `read_source` against the pinned units to confirm that no *other* pinned passage bears on the four notions, plus one targeted attempt to obtain a live (non-scripted) episode record; then assemble and verify.
- **Authoritative continuation decision:** to be made after host verification via the pilot `continue_or_stop` control call with the verification reference and the stated stop rule above. This section itself is a **provisional self-check proposal made before host verification** and is not the authoritative decision.

### 7. What would reverse this artifact's conclusion

- A live record exposing any of the four reversal-evidence sets in §4 would move the corresponding row from “missing criterion / unsupported” to “supported at the stated grain.”
- A pinned FW5 passage (L33–L1372) contradicting the four anchors we did use (L601, L123/L140, L661/K3, L773/L634) would be a source-clause challenge and would force a revision of the table, not a retraction of the four failure-kind distinctions.
- Exhibit of a **provider** observation matching the offline episode's structure would convert the offline fixture's role from “low-authority mechanics illustration” to “confirmed live instance” for the host-level mappings; it would *not* by itself satisfy M1, M2, or M4 under FW5 criteria.

### 8. Not found

- Any record field naming an FW5-level active route, contrast contract, elimination argument, or critical episode.
- Any pinned FW5 excerpt that licenses inferring such fields from host labels.
- Any live provider observation, reader brief, or derived-properties memorandum accessible from this seat.

### 9. Unresolved

- Whether the reversal candidates in §4 exist in a record type outside this projection.
- How the host's byte-span resolver will treat the escape-containing offline-episode quote; if resolution fails, that quote must be treated as a host-resolver issue and not silently dropped.
- Whether “logical calls” in the owner contract counts this very response; the host-reported remaining-call count at the control step controls.

### 10. Explicit refusals

- I do **not** claim any unexecuted check passed.
- I do **not** claim a second pass occurred.
- I do **not** treat the provisional continuation proposal in §6 as an authoritative decision; the authoritative decision is the post-verification control call.
- I do **not** force FW5 to win (by over-reading labels) or lose (by over-reading absences).
- I do **not** infer any unread portion of FW5 from the pinned excerpts.

Status: partial
