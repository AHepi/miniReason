# C001 — Three-case contrast triple at one responder node

Pre-registration. Published before dispatch. Written under
[AGENTS.md](../../../AGENTS.md), [PURPOSE.md](../../../PURPOSE.md),
[docs/EXPERIMENT_METHOD.md](../../../docs/EXPERIMENT_METHOD.md) ("Freeze a concrete
claim") and [docs/SEMANTIC_GUIDE.md](../../../docs/SEMANTIC_GUIDE.md) ("Declare the
interpretation before the evidence").

| field | value |
|---|---|
| id | `C001-contrast-triple` |
| kind | diagnostic; one node, four cases, two arms, six endpoints |
| implements | proposal **P2** of `fw5-vs-harness-spec-review.md` §5 — the three-case contrast triple redirected from the judge to the responder |
| designated source | FW5 reading edition, sha256 `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` |
| load-bearing source lines | FW5:601, :609, :626, **:628**, **:630**, :634, :640, :851 |
| material | `material.json`, sha256 `94edfe612097441c8a5957c41a8a1140833b89bd155bd9794b60a1bfb8979975` |
| driver | `tools/contrast_triple_study.py` |
| plan identity | `plan_id` = digest of the frozen plan body; minted by `prepare`, written to `plan.json`. For the published material and driver: `328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8`. It supersedes `34f510170282f374cf1132eb7b2334030a3b39965c97313b36e79fb746f3184f` (material `52251e15…90a4632`), the staged identity, which carried no per-endpoint `timeout_seconds` table (§5) |
| planned calls | **240** = 4 cases × 5 replicates × 6 endpoints × 2 arms |
| offline preflight | 240 planned, **0 provider calls** |
| status | pre-registered, not dispatched |

---

## 1. Question

At **one** responder node — the fork5 `response` node, whose instruction and whose
non-objection inputs are frozen from the H005 material and from
`H005-open-prose-commitments/occurrence-01` — does the successor's authored commitment
surface

1. **differ** against a no-objection control,
2. and **not** differ under a content-preserving recoding of the objection,
3. and **not** differ under a carrier disturbance at fixed content?

This is FW5:630's contrast contract — "a content-changing case, a content-preserving
recoding, and the distinction between a change in the objection and an irrelevant
carrier disturbance" — applied where FW5:626–628 actually locates reason use: in the
**response**, not in a judge. The review's finding XD-3/LI-3 is that harness v1.3
already has all three legs (`paraphrase invariance`, `premise-deletion sensitivity`,
`verbosity pairs`) but aims every one of them at the judge. C001 re-aims them.

The study answers the question with a **reading**, not a computation. FW5:628 requires
a structural map preserving internal role bindings on an active dependency route; a
transcript supplies no such map. What a positive pattern here can be is *consistent
with* a reason-use witness. It is never the witness.

---

## 2. How this avoids the Appendix-B-14 confound

Appendix B item 14 of the review records that the fork5 `objection`/`rival` pair is
confounded: those two nodes differ in **instruction** (`material.json:60` vs `:70`) as
well as in **view**, so a difference between their successors cannot be attributed to
the withheld commitment content.

C001 removes that confound by construction, and the removal is checked mechanically,
not asserted:

* **One node.** Every one of the 240 calls is the fork5 `response` node.
* **One instruction.** The node instruction is copied verbatim from the H005 material
  and is byte-identical in all four cases; its sha256 is pinned in `plan.json`.
* **One system message.** `system` + the arm's policy (`formal_instruction` /
  `prose_instruction`) + the public contract, byte-identical across the four cases of
  an arm.
* **Two frozen inputs.** The `account` and `rival` projections are byte-identical in
  all four cases, and each is the projection the real H005 `response` node saw (the
  test asserts each appears verbatim inside
  `occurrence-01/requests/daily/mini_*/cycle01/response.json`).
* **One varying block.** Only the `objection` projection block differs. `prepare`
  computes, per arm, the shared prefix and suffix around that block and refuses the
  plan unless all four briefs equal `prefix + <this case's objection block> + suffix`
  (`SHARED_ENVELOPE_MISMATCH`). Both hashes are frozen in `plan.json` and copied into
  every request record.

Measured, from the frozen material. **Two bases are reported, because only one of them
is the honest denominator.** The brief-level figures include the shared prefix and
suffix — 15.3 k characters that are byte-identical across all four cases — so a
percentage taken on them understates the variation the responder can actually see. The
only thing that varies is the objection block, so the block is the base a length-
sensitive responder would respond to.

*Brief level* (whole user message):

| arm | shared prefix (chars) | shared suffix (chars) | original | recoding | carrier | control |
|---|---|---|---|---|---|---|
| fcl | 7460 | 7846 | 23032 | 23267 | 23599 | 15384 |
| prose | 6485 | 8731 | 20867 | 21019 | 20936 | 15294 |

*Block level* (the objection projection block alone — the honest base):

| arm | original | recoding | carrier | control |
|---|---|---|---|---|
| fcl | 7726 | 7961 (**+3.0 %**) | 8293 (**+7.3 %**) | 78 |
| prose | 5651 | 5803 (**+2.7 %**) | 5720 (**+1.2 %**) | 78 |

The fcl CARRIER block is the longest of the four, **+7.3 % on the ORIGINAL block**, and
the inflation is entirely the declared `indent=2` re-serialisation of §4(c). A
length-sensitive responder could therefore produce an ORIGINAL/CARRIER difference driven
by block size alone; that reading is recorded as a live alternative to the
grain-declaration reading of F3 (§11 L5). The control is necessarily shorter; see §11
(L1).

---

## 3. The node and the frozen material

| item | value |
|---|---|
| template | `fork5` |
| node | `response` |
| instruction | *"Continue the inquiry in light of the account, criticism and alternative. Decide what to use, leave open, revise or reject, and explain your grounds where they matter."* (verbatim, H005 material) |
| inputs, in order | `account` (view `both`), `objection` (view `both`), `rival` (view `both`) |
| varying input | `objection` only |
| problem | `daily`, verbatim H005 prose |
| rendering | `direct_explicit_views` — the non-Mini branch of `render_node`; sections joined by `\n\n` |
| projection | byte-identical to `project()` in `tools/multicycle_commitment_study.py` |

**Why not the canonical Mini reducer render.** H005's `mini_*` arms render through
`compile_manifest`/`render_brief`, whose port headers carry a *content-addressed*
artifact id (`[b5dbbb04b5acd035] (h005.fork5.p.response.0)`). Since three of the four
cases deliver different bytes, that id would vary across cases as an uncontrolled
carrier difference, and freezing it at the ORIGINAL value would make the header false.
C001 therefore renders through the runner's own `direct_explicit_views` shape, which
contains no content-derived identifier. The `project()` output itself is unchanged, so
the ORIGINAL objection block is byte-for-byte the block the H005 `response` node saw.

**Pinned sources** (`material.json.source_pins`, re-read and re-hashed by `prepare`,
`verify`, `run`, `audit` and `table`):

| path | sha256 |
|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b…e33ee63a` |
| `experiments/.../H005-open-prose-commitments/material.json` | `24ca4552…b756c927` |
| `…/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5…2562110db` |
| `…/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d…999732e6` |
| `…/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d…a748e8cd` |
| `…/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe9…0280ad06` |
| `…/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb575…63e3f1005` |
| `…/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93…0a6df52` |

**Pinned transport** (`material.json.transport_pins`, re-hashed by `prepare`, `verify`,
`run`, `audit` and `table`). `base_url`, `chat_path`, `timeout_seconds` and
`max_concurrency` reach this study from the transport module and its endpoint registry
rather than from this material, so pinning only the material and the driver would have
left the parts of the effective configuration most likely to move uncovered
(EXPERIMENT_METHOD:11, "model and software identity" and "full effective
configuration").

At dispatch **the endpoint registry and the transport module are the **published
repository files**, and the pinned bytes below are theirs.** *(Corrected before
dispatch. An earlier build of this material was made while both files existed only in a
staged provider package, and said so here; that is no longer true of either file, and
the sentence was corrected rather than left standing beside the hashes it contradicts.
The pins themselves did not move: the staged build already pinned exactly these bytes.)*

| file | sha256 |
|---|---|
| `src/minireason/provider_openai_compat.py` | `cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db` |
| `src/minireason/data/endpoints.json` | `03eff16b8f575c113871a1266439874b2622a75d200ecb84a1b79464aa98aee7` |

A mismatch on any source pin stops the study (`SOURCE_PIN_MISMATCH`); a mismatch on
either transport pin stops it too (`TRANSPORT_PIN_MISMATCH`). **The repository is read
only; C001 never writes into it** — including `endpoints.json`, whose 180-second
`timeout_seconds` rows this study leaves exactly as they are while dispatching under its
own per-endpoint values (§5). Those values are applied to the resolved `Endpoint`
*value* by `dataclasses.replace` at provider construction, so the file other studies'
plans pin stays byte-identical and their plans stay valid.

**Receipt owed on §5's reachability claim.** "All six answered live on the
OpenAI-compatible chat path" is a provenance assertion from the provider smoke test. It
is *not* receipted inside this occurrence, and until the smoke-test receipt is published
beside it the sentence should be read as a statement of why six endpoints were planned,
not as evidence about them (NOTES §6 item 4).

---

## 4. The four cases

All four are delivered under otherwise identical payloads.

### (a) ORIGINAL

The real H005 objection document — `daily/mini_fcl/cycle01/objection` for the FCL arm,
`daily/mini_prose/cycle01/objection` for the prose arm — exactly as the H005 `response`
node saw it: the same `body` and `commitments` bytes, projected by the same `project()`
with view `both`. `prepare` refuses unless the case bytes equal the occurrence artifact
bytes (`ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES`).

### (b) RECODING — content-preserving

A recoding of that objection, **authored offline by the study designer before dispatch.
No model call produced it.** It is published as a human-checkable correspondence table
in `material.json` (`arms.<arm>.recoding.units`) and rendered to `RECODING_TABLE.md`.

*Unit definition.* Prose documents: the sentences produced by
`re.split(r'(?<=[.!?])\s+', paragraph.strip())` over paragraphs split on `\n\n`. FCL-1
documents: the same sentence split applied to each string field (`text`, `scope`,
`grounds`, `bearing`, `action`, `consequence`) of each record. **85 units in all** — 50
for the FCL arm (28 body + 22 commitment-field), 35 for the prose arm (20 body + 15
commitment).

*Rules, declared before the recoding was written.*

| rule | operation |
|---|---|
| `R1` SYNONYM | lexical substitution preserving reference and illocutionary force. A contraction and its expansion (`I'd` / `I would`, `can't` / `cannot`) are the same lexical items in the same order with the same modal force; that alternation is orthographic and is recorded under `R1`, not as an operation of its own |
| `R2` CONSTITUENT-ORDER | reordering of constituents (clauses, phrases, adverbials) **inside one unit**. Broadened 2026-09-14 from "reordering of clauses": the label was already carried by units that front a PP or an adverbial (`B.P3.S1`, `B.P5.S4`, `K.c1.grounds.S1`, prose `C.P2.S4`), and the narrower wording made those labels false. The restriction is unchanged — the reordering stays inside one unit — and it may **not** be used for an operation on an NP head |
| `R3` VOICE | active/passive or verbal/nominal alternation |
| `R4` DEIXIS | demonstrative ↔ explicit antecedent inside one unit — **applicable only where the demonstrative has a unique antecedent inside the same paragraph, with the uniqueness argument recorded in the unit row** |
| `R5` CONNECTIVE | substitution of an equivalent discourse connective |

There is **no** rule for information structure (clefting, pseudo-clefting,
topicalisation, equative inversion, subordination ↔ coordination, assertion ↔
presupposition) and **no** rule for determiner or definiteness change. Both were
considered and declined: the content-preservation argument is not clear-cut for either,
so units that had used one were reverted to the simplest declared operation instead of
being licensed by a new rule (FIXES.md, §1).

*Invariants.* Unit count, unit order and unit boundaries preserved (no cross-unit
move); quoted material reproduced verbatim; FCL-1 record ids, types, `uptake` and every
reference array (`target`, `depends`, `mentions`, `revises`, `withdraws`) unchanged; no
proposition added, dropped, strengthened or weakened; hedge force preserved — checked
per unit as an exact count of every declared hedge/modal marker family; **no
information-structure operation beyond the topic/focus reassignment intrinsic to `R3`
(active/passive alternation)** — no clefting, pseudo-clefting, topicalisation, equative
inversion, existential-`there` insertion or deletion, subordination ↔ coordination,
assertion ↔ presupposition — and **no determiner or definiteness operation of its own**:
no `the` ↔ `a`, `the` ↔ `this`/`that` or bare ↔ determined change to an otherwise
unchanged referring expression; the criticism's constituents keep their roles —
represented target *z*, alleged defect *δ*, grounds *g*, bearing (FW5:609).

The `R3` qualification is not a loophole opened after the fact, it is the correction of
a wording that was literally false of the material: an active/passive alternation *is* a
reassignment of topic and focus, and 16 fcl and 14 prose units apply one. The invariant
is stated to exclude those rather than to be refuted by them; every information-structure
operation that is **not** an `R3` voice alternation — including the two existential-`there`
moves and the predicate-nominal definiteness change the independent spot-check caught —
was reverted, and the reverted units are listed exhaustively under *Not exercised*.

The determiner clause is qualified for the same reason, found on the implementer's own
re-read of the closed units: an `R1` lexical paraphrase and an `R3` verbal ↔ nominal
alternation each carry a determiner with them — `falling recurrence` → `a fall in
recurrence`, `presenting that sequence` → `the presentation of that sequence`, `being
able to hold` → `the ability to hold` — and 26 units show a determiner-token delta of
that kind. What is excluded is a determiner or definiteness change applied **as an
operation of its own**, to a referring expression the unit otherwise leaves alone; that
is what the four reverted determiner units (prose `B.P2.S3`, `B.P4.S2`, `C.P3.S2`, fcl
`B.P5.S2`) had done.

*Not exercised.* (i) Cross-unit sentence re-ordering — available under the rule set and
deliberately unused: unit order can carry argumentative dependence, and preserving it
makes the correspondence table checkable unit by unit (NOTES Q1). (ii) `R4` DEIXIS —
declared, and used nowhere. Under its uniqueness restriction no demonstrative in either
document has a unique antecedent inside its own paragraph, so the re-read reverted every
unit that had applied a deixis operation. (iii) Information structure (other than the
`R3` voice alternation) and determiner/definiteness — not declared, not used, and the
revert list is now **exhaustive**: 15 units of the fcl document and 19 of the prose,
named one by one in `material.json.arms.<arm>.recoding.not_exercised`. The earlier
version of that list was not exhaustive, which is how the three units the independent
spot-check recorded as outright violations — fcl `K.o1.text.S1` (existential-`there`
inserted, in record `o1`'s own `text` field), fcl `B.P4.S1` (existential-`there` deleted)
and fcl `B.P4.S2` (definite possessive predicate nominal turned into a bare plural) —
came to sit outside it. (iv) Evaluative and relational predicate substitution — `R1` is
restricted to substitutions preserving reference **and** illocutionary force, so a
substitution that loosens or strengthens an evaluative or relational predicate is not
licensed; the nine such units the spot-check named are listed in `not_exercised` with the
wording restored in each. `prepare` reports which declared rules went unused.

*Mechanical checks in `prepare`.* Every original unit is mapped exactly once; the
recoded document is reconstructed **from the table alone** and must equal the frozen
recoded bytes; the same reconstruction applied to the original units must reproduce the
original bytes; and the recoding must not be the identity. In addition:

* **(a) FCL-1 structure, record by record.** Each record's id, type, field set,
  every reference array, every non-string field, the document's `uptake` list and its
  language tag are compared individually, so a refusal names what moved
  (`RECODING_CHANGED_FCL_RECORD_TYPE`, `…_REFERENCES`, `…_UPTAKE`, `…_LANGUAGE`).
* **(b) Hedge force, per unit.** Every declared hedge/modal marker family — `if`,
  `unless`, `whether`, `may`, `might`, `can`, `could`, `will`, `would`, `shall`,
  `should`, `must`, `ought`, `need`, `deserve`, `necessarily`, `probably`, `possibly`,
  `perhaps`, `merely`/`just`/`simply`/`only`, `seem`, `appear`, and the negation family
  — is counted in the original and in the recoded text of each unit, after contraction
  expansion, and any change is `RECODING_HEDGE_FORCE_CHANGED`. The marker table is
  published in `RECODING_TABLE.md` and is part of the material.

  **What this counter cannot see.** It refuses a change in the *count* of a declared
  marker family inside a unit and nothing else. It is blind to illocutionary and
  evaluative force carried by ordinary predicates, and blind to which constituent a
  preserved marker attaches to. The independent spot-check of 2026-09-14 found it passing
  all 85 units while missing: `consistent with` → `fit` (a bare compatibility relation
  loosened into a confirmatory one); `downweight` → `discount`; `issue` → `point`;
  `fine` → `unobjectionable` (an `un-` litotes is not in the `NEGATION` family); `or` →
  `and` under a negation, which admits a not-both reading the original excludes; and
  get-passive → be-passive. Changes of that kind are caught only **by reading**. The
  85-row correspondence table is published so that the reading can be disputed row by
  row, and the two-reviewer re-read recorded in `FIXES.md` — the constituent re-read and
  the independent spot-check that followed it — is the record of its having been done.
  Every case listed here was reverted, not licensed. The same paragraph is carried inside
  the material (`recoding.hedge_marker_limits`) and rendered into `RECODING_TABLE.md`, so
  it is inside the frozen identity rather than beside it.
* **(c) Rule labels.** Every unit's declared labels must be a subset of the declared
  rule set (`RECODING_UNDECLARED_RULE`).
* Quoted spans are compared in order, so a recoding cannot rewrite what the objection
  quotes (`RECODING_QUOTATION_CHANGED`).

None of this establishes constituent-role preservation; that is a reading, and the
published unit table is what makes it checkable. What the checks do is refuse the three
mechanically detectable ways the first draft of this recoding went wrong.

### (c) CARRIER — same content, disturbed carrier

*Operations.*

| arm | body | commitments |
|---|---|---|
| fcl | paragraphs hard-wrapped to 72 columns (whitespace only) | FCL-1 re-serialised with `indent=2`, keys sorted alphabetically, `records` array reversed, `uptake` array reversed |
| prose | paragraphs hard-wrapped to 72 columns (whitespace only) | each paragraph rendered as one `- ` bullet item, wrapped to 68 columns with two-space continuation indent; sentence order unchanged |

*Grain declaration* (a criticisable interpretation claim, not a fact): an FCL-1
document's content is the **set** of records keyed by id — each a field→value map —
together with the **set** of uptake ids and the language tag; array order, key order
and whitespace are carrier. A prose document's content is the **sequence of
whitespace-separated word tokens**; line breaks, indentation and bullet markers are
carrier.

*Byte-level proof* (recomputed by `prepare` and by the tests, and frozen in
`material.json.arms.<arm>.carrier.proof`): `normalise(original) == normalise(carrier)`
for both fields, while the raw bytes differ. Normalisation is
`normalise_prose` (strip a leading bullet marker per line, collapse whitespace runs to
one space, strip) for prose, and `canonical_fcl` (parse; sort records by id; sort
uptake; re-serialise with `sort_keys`, `separators=(',',':')`) for FCL-1.

| arm | field | normalised sha256 (original = carrier) | bytes differ |
|---|---|---|---|
| fcl | body | `4b999291a3e55e18…` | yes |
| fcl | commitments | `afc365628d1aaae3…` | yes |
| prose | body | `7ef63adfcfaab53c…` | yes |
| prose | commitments | `a4eca70ef37ea482…` | yes |

### (d) CONTROL — no objection

The `objection` view is absent, rendered with **the runner's own absent wording**,
verbatim from `project()`:

```
Source objection: absent in the first template invocation; selected view both.
```

`prepare` refuses unless the control brief equals the original brief with the objection
block replaced by exactly that line
(`CONTROL_DIFFERS_OUTSIDE_THE_OBJECTION_BLOCK`), and unless no 6-word shingle of the
objection document occurs in the control brief other than shingles the objection shares
with the frozen `account`/`rival`/problem/instruction text
(`CONTROL_CARRIES_OBJECTION_CONTENT`). Those shared phrases — 12 for the FCL arm, 16
for the prose arm — reach the node identically in all four cases and therefore cannot
differentiate them; the count is recorded in `preflight.json`, not treated as a
failure.

---

## 5. Arms, endpoints, replicates, ceilings

| dimension | value |
|---|---|
| arms | **FCL-1** (`formal_instruction`) and **prose** (`prose_instruction`), both verbatim from the H005 material |
| cases | `original`, `recoding`, `carrier`, `control` |
| replicates | **N = 5** per case per endpoint per arm |
| temperature | provider default — never sent, so the endpoint's own default applies |
| seeds | 1…5 (the replicate index), sent where the endpoint honours seed |
| max_tokens | **declared per endpoint**: 8192 for `deepseek-flash`, **32768** for the five Ollama endpoints (authorised maximum 32768). See *The per-endpoint completion ceiling* below |
| timeout | **declared per endpoint**: 180 s for `deepseek-flash`, **600 s** for the five Ollama endpoints (the transport's own validation maximum). See *The per-endpoint wall-clock timeout* below |
| automatic retries | **0** |
| concurrency | ≤ 5 per credential, enforced twice: by the transport's process-wide per-key semaphore and by the driver's own `KeyGate` |

**Endpoints** (registry names in the staged provider package's
`minireason/data/endpoints.json` — **the registry is supplied by that package, not by
the repository**, and both it and the transport module are pinned in §3; the
OpenAI-compatible chat path in every case, never the `.native` variant):

| registry name | model | credential | seed | max_tokens | timeout |
|---|---|---|---|---|---|
| `deepseek-flash` | `deepseek-flash` | `DEEPSEEK_API_KEY` | **unverified** — sent, effect unestablished | 8192 | 180 s |
| `ollama/gpt-oss-120b` | `gpt-oss:120b` | `OLLAMA_API_KEY` | honoured | **32768** | **600 s** |
| `ollama/qwen3.5-397b` | `qwen3.5:397b` | `OLLAMA_API_KEY` | honoured | **32768** | **600 s** |
| `ollama/glm-5.3` | `glm-5.3` | `OLLAMA_API_KEY` | honoured | **32768** | **600 s** |
| `ollama/kimi-k3` | `kimi-k3` | `OLLAMA_API_KEY` | honoured | **32768** | **600 s** |
| `ollama/gemma4-31b` | `gemma4:31b` | `OLLAMA_API_KEY` | honoured | **32768** | **600 s** |

All six answered live on the OpenAI-compatible chat path in the provider smoke test, so
the plan is written for six. **If an endpoint is not reachable at dispatch time**, its
40 coordinates are written as `NOT_DISPATCHED` with the operational reason, the audit
reports 240 planned against N dispatched, and no semantic verdict is issued for that
endpoint (EXPERIMENT_METHOD, operational-delivery-failure row). *Substituting a
different endpoint changes the material and therefore mints a new `plan_id`: it is a
new pre-registration, not an amendment of this one.*

Seed policy, recorded per call: `honors_seed`, `seed_requested`, `seed_sent`,
`seed_echoed_in_response` and `system_fingerprint`. `seed_echoed_in_response` is
tri-state: the value the provider echoed where it echoed one, and `null` — unknown, not
denied (FW5:634) — where it reported none. `system_fingerprint` is the determinism
signal the OpenAI-compatible families actually return. `audit` aggregates both over the
five replicates of an endpoint. Where seed support is unverified the five replicates are
recorded as independent samples whose seed effect is unestablished — not as five
deterministic repetitions.

Native reasoning is **not** manipulated. Most Ollama models emit reasoning by default
and those tokens count against `max_tokens`; the presence of reasoning is recorded
(`reasoning_content_present`), the text is never persisted, and no arm of this study
turns it on or off. This is not a native-reasoning comparison.

**The per-endpoint completion ceiling, and why the Ollama ceiling was raised before
dispatch.** `max_tokens` is declared **per endpoint**, not once for the study:
`deepseek-flash` keeps **8192**, the five Ollama endpoints carry **32768**, and 32768 is
the authorised maximum. The value is frozen twice — in `endpoints[].max_tokens` and in
`ceilings.max_tokens` — and `prepare` refuses unless the two agree and unless every one
of the 240 built payloads carries its own endpoint's value (`CEILING_NOT_APPLIED`,
`MATERIAL_ENDPOINT_MAX_TOKENS`). The transport's own argument validation accepts
1 … 393216, so 32768 is inside its range; the preflight builds every payload through
that validation.

The raise is made **before dispatch**, on live evidence rather than on a guess, and the
evidence is cited so a reader can check it: **REC-20260914-S**, F001 in
`experiments/diagnostics/F001-fork5-multifamily` — `occurrence-04` (`ollama/glm-5.3`)
and `occurrence-05` (`ollama/kimi-k3`), both run at `max_tokens` 8192. Across those two
occurrences **five nodes returned no content at all**: `INCOMPLETE_GENERATION`,
`finish_reason: "length"`, `completion_tokens: 8192`, `reasoning_content_present: true`
— the whole ceiling went to reasoning and nothing was left for the reply — and **two
further nodes came back PARTIAL** on the same signature. Those two families emit
reasoning by default and its tokens count against `max_tokens`, so at 8192 the study
would have been measuring the ceiling rather than the responder.

Raising the ceiling **does not manipulate reasoning.** `temperature`, `thinking` and
`reasoning_effort` are still never sent; the endpoint's own default still decides whether
and how much it reasons; nothing is turned on or off, and §5's "not a native-reasoning
comparison" stands unchanged. A larger `max_tokens` buys the reply room to exist beside
the reasoning; it is a headroom change, not an intervention. Its one methodological cost
is recorded: the six endpoints no longer share a single completion ceiling, so a
difference between `deepseek-flash` and an Ollama endpoint has one more uncontrolled
difference behind it (§11 L7 already says the endpoints differ in more than identity).

**A cell that hits even the raised ceiling is still unresolved.** The rule is unchanged:
a `finish_reason: "length"` delivery at the endpoint's own ceiling is PARTIAL, marked
`comparable: false`, its mechanical columns withheld, compared against nothing; a
delivery that returns no content at all is a refusal recorded with its failure code
(`INCOMPLETE_GENERATION`) and likewise compared against nothing (FW5:634). The raise
makes those outcomes less likely. It does not change how they are read, and no cell is
rescued by it.

**The per-endpoint wall-clock timeout, and why the Ollama timeout was raised before
dispatch.** `timeout_seconds` is declared **per endpoint** exactly as `max_tokens` is:
`deepseek-flash` keeps **180**, the five Ollama endpoints carry **600**, and 600 is not a
number this study picked — it is the **transport's own validation maximum**,
`minireason.provider_openai_compat.Endpoint.__post_init__`, which admits
`1 … 600` seconds and refuses anything else. The value is frozen twice, in
`endpoints[].timeout_seconds` and in `ceilings.timeout_seconds`, carried into
`plan.json`, written into **every request record and every receipt**, and re-tied to the
frozen plan by `audit`; any disagreement between the plan, the material, the call spec,
the written record and the transport's own settings view is one refusal,
**`TIMEOUT_NOT_APPLIED`**.

**`src/minireason/data/endpoints.json` is not edited.** Its rows still read
`"timeout_seconds": 180`, and they must: that file is pinned by this material (§3) *and*
by the F001 plans, and rewriting it would invalidate theirs. The declared value is
applied instead to the resolved `Endpoint` **value**, by `dataclasses.replace`, at
provider construction inside `resolve_endpoint` — the single point every provider this
driver builds, live or offline, passes through. The replacement re-runs the dataclass's
own validation, so an out-of-range value is refused by the transport rather than by this
driver's opinion of it, and the driver additionally checks that replacing the timeout
back yields the registry's own object, so nothing else moved with it.

The raise is made **before dispatch**, on live evidence, and the evidence is cited so a
reader can check it: **REC-20260914-T**, `experiments/diagnostics/F001-fork5-multifamily`.
That run spent 20 provider calls at `max_tokens` 32768 over occurrences 07 and 08 and
failed exactly twice — **both times on the fixed 180-second endpoint timeout, neither
time on the ceiling**:

| record | endpoint | failure | provider record |
|---|---|---|---|
| `occurrence-07/responses/daily/mini_fcl/cycle01/objection.json` | `ollama/glm-5.3` | `TRANSPORT_OR_RESPONSE_ERROR` | `occurrence-07/provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` — `error` "The read operation timed out", `elapsed_ms` **180368**, `settings.timeout_seconds` **180**, `max_tokens` 32768 |
| `occurrence-08/responses/daily/mini_fcl/cycle01/carry.json` | `ollama/kimi-k3` | `TRANSPORT_OR_RESPONSE_ERROR` | `occurrence-08/provider/daily/mini_fcl/cycle01/carry/call-0001.response.json` — `error` "The read operation timed out", `elapsed_ms` **180456**, `settings.timeout_seconds` **180**, `max_tokens` 32768 |

Neither carries a `finish_reason`, a `usage` block or any content; neither is
`INCOMPLETE_GENERATION`; and in that whole run **`finish_reason: "length"` occurs zero
times**, the largest single completion being 16,871 tokens. So what those two calls met
was the wall clock, which did not move when the completion ceiling moved. C001 plans 240
calls on the same two families among others, at the same raised ceiling; leaving the
timeout at 180 s would be planning the same refusal.

**Raising the timeout does not manipulate reasoning, and changes no request byte.** It is
a socket read deadline, not a payload field: nothing new is sent, `temperature`,
`thinking` and `reasoning_effort` are still never sent, and the request bytes whose
hashes `plan_id` binds are byte-for-byte what they would be at any timeout — a test
asserts it. Its one methodological cost is recorded, in the same terms as the ceiling's:
the six endpoints no longer share a single wall clock, so a difference between
`deepseek-flash` and an Ollama endpoint has one more uncontrolled difference behind it
(§11 L7 already says the endpoints differ in more than identity).

**A call that exceeds even 600 s is still a refusal.** It is recorded with its failure
code (`TRANSPORT_OR_RESPONSE_ERROR`), it is compared against nothing, and its cell stays
unresolved (FW5:634). The raise makes that outcome less likely. It does not change how it
is read, and **no cell is rescued by it.**

Waves: the 240 coordinates are dispatched in **47 deterministic waves**, each holding
**at most 5 coordinates per credential** — which is the authorisation, and is what the
driver's `KeyGate` and the transport's own per-key semaphore each enforce independently.
The coordinate order is endpoint-major, so 46 of the 47 waves are single-key and hold
five; the **one** wave that straddles the boundary between `deepseek-flash`'s forty
coordinates and the first Ollama endpoint's holds ten — five on `DEEPSEEK_API_KEY` and
five on `OLLAMA_API_KEY`. That is ten requests in flight across **two** credentials, five
on each, and it is inside the five-per-credential authorisation rather than an exception
to it. *(This paragraph previously said every wave was single-key and that at most five
requests were ever in flight; that was false of the boundary wave, and is corrected here
before dispatch rather than discovered afterwards. `WaveShape` in the suite pins both the
47 and the one ten-coordinate wave, and `Concurrency` pins the five-per-key ceiling
against the dispatcher itself.)*

---

## 6. Declared differences from the H005 decoder and from the F001 transport settings

All three are forced by the multi-endpoint set and are stated here, before dispatch,
rather than discovered afterwards.

**(i) `envelope_unwrap`.** Ollama cloud accepts `response_format: json_object` but does
not enforce it: a model may wrap its JSON in a ```` ```json ```` fence, or emit control
characters inside strings. H005 ran one endpoint that did enforce it, so its decoder
needed no unwrap. C001 declares exactly two repairs, applied in this order and recorded
per call:

1. strict `json.loads` of the delivered content; if it yields `{"body","commitments"}`
   of strings, no repair is recorded;
2. otherwise strip **one** outer code fence and retry the strict parse —
   `envelope_repairs += ["strip_outer_code_fence"]`;
3. otherwise retry with `json.loads(strict=False)` —
   `envelope_repairs += ["json_strict_false"]`;
4. otherwise the envelope is `OPAQUE` and the whole delivered text is kept as the body.

Every call records `envelope_repairs` and `strict_parse_would_succeed`. The raw
delivered bytes are preserved untouched in `responses/<…>.txt` and in the write-once
provider record. **No other repair is ever applied to content.** A repair touches the
carrier of the reply, never its content, and the mechanical table shows which cells
needed one.

**(ii) Missing usage is unknown, not zero.** A provider that reports no usage yields
`usage_status: "UNKNOWN"` rather than a decode failure (EXPERIMENT_METHOD: "Missing
usage is unknown, not zero"). A completion exceeding the declared ceiling is still a
hard failure.

**(iii) The wall-clock timeout is per endpoint, where F001's was fixed.** F001 — and
H005 before it — ran every endpoint at the registry's own 180 seconds, which is not a
per-arm or per-endpoint declaration and did not move when F001's completion ceiling was
raised to 32768. That is where both failures of **REC-20260914-T** landed:
`occurrence-07/responses/daily/mini_fcl/cycle01/objection.json` on `ollama/glm-5.3` and
`occurrence-08/responses/daily/mini_fcl/cycle01/carry.json` on `ollama/kimi-k3`, each
`TRANSPORT_OR_RESPONSE_ERROR`, each whose provider record reads "The read operation timed
out" at `elapsed_ms` 180368 and 180456 against `settings.timeout_seconds` 180, both at
`max_tokens` 32768, and neither with a `finish_reason`, a `usage` block or any content.
C001 therefore declares `timeout_seconds` per endpoint (§5): 180 for `deepseek-flash`,
600 — the transport's own validation maximum — for the five Ollama endpoints. It is
applied to the registry `Endpoint` by `dataclasses.replace` at provider construction, so
`src/minireason/data/endpoints.json` is never written; it is frozen in `plan_body`,
recorded in every request record and receipt, and refused with `TIMEOUT_NOT_APPLIED`
wherever the plan, the material, the spec, the record and the transport disagree. **It is
a resource fact about this transport and nothing more.** No payload field changes, no
reasoning is manipulated, and a call that exceeds 600 s is a refusal read exactly as a
call that exceeded 180 s would have been.

**PARTIAL cells are unresolved.** A delivery with `finish_reason: "length"` at the
**endpoint's own declared ceiling** — 8192 for `deepseek-flash`, 32768 for the five
Ollama endpoints (§5) — yields a truncated commitment surface. Such a cell is marked
`comparable: false` with the reason recorded, its mechanical columns are **withheld**,
and it is **not compared against any other case** (FW5:634). It is reported, not
dropped. A delivery that returns **no content at all** because the ceiling went entirely
to reasoning is a refusal, recorded with its failure code (`INCOMPLETE_GENERATION`) and
compared against nothing either — the failure mode F001 exhibited five times at 8192,
and the reason the Ollama ceiling was raised to 32768 before dispatch. **The raised
ceiling rescues no cell**: a cell that hits 32768 is read exactly as a cell that hit
8192 would have been.

---

## 7. Evidence

Per `(endpoint, arm)` cell — twelve cells, twenty deliveries each.

**Mechanical comparison table** (`COMPARISON.md` + `comparison.json`, both written by
`tools/contrast_triple_study.py table`):

*For the FCL arm*, read off the successor's own `commitments` string:

* whether it parses as an FCL-1 document, and the language tag;
* parsed records **by type** (`claim`, `commitment`, `objection`, `use`, `problem`, plus
  any undeclared type);
* record ids;
* **targets named** — every string appearing in a `target` array;
* every `depends` / `mentions` / `revises` / `withdraws` reference;
* **which original-objection record ids are referenced, prefix-resolved** — a
  cross-document reference is `<prefix>#<record id>`, and the **prefix** is what says
  which document is meant. Each prefix is resolved against the three artifact addresses
  declared in `material.json.arms.<arm>.artifact_addresses`, against each address
  truncated to its first 16 hex characters (the form the real H005 `response` node
  emitted, `b5dbbb04b5acd035#c2`), and against the source name. The table then reports
  **four separate columns**: objection-prefixed ids intersected with
  `o1,o2,o3,c1,c2,o4,p1,u1`; account-prefixed ids; rival-prefixed ids; and references
  whose prefix matches nothing. This matters because the objection and the account share
  five of the objection's eight ids, so a reference reduced to its suffix would be
  attributed to the objection whichever document was actually cited;
* **bare-token occurrences** of those ids in the body and in the commitments, in a
  separate channel. A token preceded by `#` or `.` belongs to a structured reference and
  is excluded here, so the two channels really are separate rather than overlapping by
  construction. A bare token stays **unresolved**;
* `uptake`;
* byte hashes and lengths of `body` and `commitments`.

*For the prose arm*: **none mechanical beyond byte hashes and lengths.** There is no
parse to perform and this study invents none. Root reads the text.

*Recorded ambiguity.* The account document uses some of the same bare record ids
(`o1`, `c1`, `c2`, `p1`, `u1`) as the objection document. Which document a **bare**
token names is not mechanically resolvable. That cell stays unresolved (FW5:634) and the
table says so in place of guessing. A *prefixed* reference is unambiguous — but only
because the prefix is retained; it is not unambiguous "as reduced by this table" unless
the table keeps it, and it now does.

**Raw juxtaposition for root** (`juxtaposition/<endpoint>__<arm>.md`): all twenty
delivered texts of a cell — four cases × five replicates — laid out in full, as
delivered, with nothing computed over them. **A delivery the decoder refused is printed
too**, under a `FAILED` heading that names the refusal code, because the replies root
most needs to read are exactly the ones a decoder rejected; the cell still counts as
unresolved. `(no delivered text reached disk)` is reserved for coordinates where no
bytes arrived at all.

**Root's columns** (`original_vs_control`, `original_vs_recoding`,
`original_vs_carrier`, `pattern_read`, `grounds`, `unresolved`) are rendered **empty**
and stay empty until root reads the juxtaposition. Nothing in the driver fills them.

"Differs against control, not under recoding, not under carrier disturbance"
(FW5:630) is a **pattern root reads**. It is never a score, never computed, and never
expressed as a quantity. The driver refuses to write any field named
`score`/`rank`/`merit`/`grade`/`rating`/`quality`/`verdict`/… anywhere in
`comparison.json` or in a `COMPARISON.md` table header (`SCORING_KEY_FORBIDDEN`), and a
test asserts it.

**The within-case baseline.** N = 5 exists so that root reads each cross-case
comparison *against the spread among five replicates of the same case*. A difference
between ORIGINAL and CONTROL means nothing unless it exceeds what two ORIGINAL
replicates already show. Counts may inform that reading; no count warrants it
(FW5:851 — counts "are not outlawed as information", only as *automatic* warrants).

---

## 8. Falsifier, stated in advance

Predicted per resolved cell:

* **D1** ORIGINAL vs CONTROL — the authored commitment surface differs in *what it
  takes up*: which target it names, which objection record it engages, what it proposes
  to do — beyond the replicate spread within either case.
* **D2** ORIGINAL vs RECODING — no difference of that kind; differences confined to
  wording, within the replicate spread.
* **D3** ORIGINAL vs CARRIER — no difference of that kind.

Defeating observations, committed before the first look:

* **F1 — the content-changing leg fails.** In a majority of resolved cells root cannot
  read any ORIGINAL/CONTROL difference exceeding the within-ORIGINAL replicate spread.
  Then the node's surface is not shown to depend on the objection's presence at all,
  the contrast contract is unsatisfied here, and P2 as designed is **defeated for this
  node**. No positive claim survives F1.
* **F2 — the recoding leg fails.** Root reads ORIGINAL/RECODING differences of the same
  kind and extent as ORIGINAL/CONTROL. Then the surface tracks the **coding**, not the
  content: FW5:628's requirement that "content-preserving recodings preserve the
  interpreted transition" is not exhibited, and no reason-use-consistent reading is
  available at this node. (Alternatively the recoding is not content-preserving after
  all — which is itself a criticism of §4(b), and root records which reading it takes.)
* **F3 — the carrier leg fails.** Root reads ORIGINAL/CARRIER differences of the same
  kind and extent as ORIGINAL/CONTROL. Then the surface is sensitive to a carrier
  detail that leaves the represented reason unchanged, which FW5:601 says "cannot
  supply that dependence" — the carrier/objection distinction collapses at the declared
  grain of §4(c), and either the grain declaration or the attribution must go.
* **F4 — the instrument fails.** Any cell whose four requests differ outside the
  objection block, or whose ORIGINAL bytes differ from the occurrence's, voids its whole
  arm. Checked mechanically by `prepare` (`SHARED_ENVELOPE_MISMATCH`,
  `ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES`) and re-checked by `audit`.

**Mechanical defeaters** (counts may defeat; they never warrant). If, in a cell, every
resolved ORIGINAL replicate's `commitments` is byte-identical to some resolved CONTROL
replicate's, **D1 is not exhibited in that cell** and root records it so. Root may
still record a stated reason to read it otherwise; the reason is written down.

A cell in which fewer than three replicates of any case are resolved yields no reading
for that case; it is reported as unresolved, not as an absence.

---

## 8a. What "differs" means, pre-declared

*This section is **mirrored into `material.json.reading_rule`** and is therefore inside
the frozen identity, not beside it. Adding it changed the `plan_id`, as PLAN §13
requires. It closes NOTES Q5 before dispatch.*

Root reads every cross-case comparison on exactly the four registers below and records
for each one of `differs` / `same` / `unresolved`. The four marks are reported
separately and stand or fall separately; they are never summed, averaged, weighted,
ranked or reduced to one mark (FW5:851; PURPOSE.md, "no scalar progress meter").

* **T — target named.** The represented target of the successor's own engagement. FCL
  arm: the set of values in `target` arrays, read **with the source artifact prefix
  intact** — a reference into the account is not a reference into the objection. Prose
  arm: the phrase by which the successor says what it is responding to. `differs` iff
  the two sets of distinct targets are not the same set.
* **E — objection record engaged, prefix-resolved.** Which of the objection document's
  records (`o1 o2 o3 c1 c2 o4 p1 u1`) the successor takes up, by prefix-qualified
  reference (resolved per §7) or by quotation of that record's own text. A bare id token
  shared with the account document (`o1 c1 c2 p1 u1`) is `unresolved` for this register
  and **never** `differs`.
* **D — proposed action (disposition).** What the successor proposes to do about the
  criticism: use, leave open, revise, reject, or withdraw. FCL arm: read off record
  `type`, `uptake`, `revises`, `withdraws` and the `action` field. Prose arm: read off
  the text. `differs` iff the disposition attached to the same criticism changes.
* **G — grounds cited.** Whether the successor grounds that disposition in the
  objection's grounds, the account's, the rival's, or none. `differs` iff the cited
  source of grounds is not the same.

**The replicate baseline, as a rule.** A register is marked `differs` for a case pair
only if the difference root reads between the two cases is one root does **not** also
read between at least one pair of replicates inside ORIGINAL. Where the same kind of
difference already appears inside ORIGINAL's own five replicates, the register is `same`
for that pair and the fact is recorded.

**Order of reading.** Root reads the five ORIGINAL replicates and writes the
within-ORIGINAL spread on all four registers into `COMPARISON.md` **before** opening any
other case's juxtaposition for that cell. The baseline note is written first and is not
revised afterwards.

**Register-to-falsifier mapping.** D1 is exhibited in a cell only if **T, E or D**
differs ORIGINAL vs CONTROL; `G` alone does not carry D1, since the control has no
objection grounds to cite and a `G` difference there is forced by the design. **F2**
fires if T, E or D differs ORIGINAL vs RECODING. **F3** fires if T, E or D differs
ORIGINAL vs CARRIER.

**Two readers.** The registers are written so that two readers of the same juxtaposition
mark the same cells. Where two readers disagree on a register, that register is
`unresolved` for that cell and the disagreement is recorded, never averaged (FW5:634).

`COMPARISON.md` renders the four registers and, per cell, an **empty** mark grid whose
rows are the within-ORIGINAL baseline and the three comparisons. Nothing in the driver
fills it.

---

## 9. Claim ceiling

* **One system, one problem, one respect.** One node of one template, on the `daily`
  problem, in the respect fixed by that node's instruction. Nothing here reaches other
  problems, other nodes, other templates, or Mini's graph as a whole.
* **Consistent-with, never a witness.** FW5:628 requires a structural map from the
  represented objection organization into a response suborganization, preserving
  internal role bindings on an active dependency route. A transcript supplies no such
  map. The best available positive outcome is: *these surfaces are consistent with the
  node having used the objection's content, and do not exhibit the differences a
  coding-tracking or a carrier-tracking explanation predicts.* **A null on the recoding
  and carrier legs does not exclude those explanations; at N = 5 it leaves them
  unrefuted and unsupported at this node.** That is not a reason-use witness and must
  never be reported as one. (The earlier wording of this bullet said the design
  *excludes* the two rivals, which contradicted the next bullet three lines below.)
* **An unresolved cell stays unresolved** (FW5:634). Absent data makes the attribution
  unresolved; it proves neither understanding nor its absence. PARTIAL deliveries,
  failed deliveries, bare-token ambiguity and under-replicated cases all stay
  unresolved and are printed as such.
* **Not a test of the models.** No endpoint is compared with another for merit. The six
  endpoints are six independent occasions to look for the same pattern; a pattern that
  appears at one and not another is a recorded difference between occasions, not a
  ranking (FW5:849, :851).
* **No (P) claim.** C001 establishes no repair, no progress, no `ProducedBy`. It is one
  cross-section, not a before/after pair.
* **Understanding and using an invalid objection does not make it valid** (FW5:630).
  Whether the H005 objection is a good one is not at issue anywhere in this study.

---

## 10. Interpretation registry, grain, boundary, O and P

Declared before the evidence (SEMANTIC_GUIDE).

| item | declaration |
|---|---|
| source claim | FW5:626–630, reason use as causal organization; the contrast contract at :630 |
| represented occurrence | the H005 `objection` document at `daily/mini_*/cycle01/objection`, in one of four codings |
| role bindings | criticism constituents per FW5:609 — target *z*, defect *δ*, grounds *g*, bearing — carried in FCL-1 by `target`, free `text`, `grounds`, `bearing`, and in the prose arm by the prose itself |
| target organization | the single `response` call: its request bytes, its delivered text, its authored commitment surface |
| question and respect | the `response` node's instruction, unchanged |
| component edit semantics | Three edit kinds are applied to the represented objection. A **RECODING** edit rewrites unit text and must preserve the FW5:609 constituents (*z*, *δ*, *g*, bearing), hedge force, quoted material, and every FCL-1 id, type, reference array and `uptake` entry. A **CARRIER** edit rewrites serialisation and layout only and must preserve the normalised form under §4(c). A **CONTROL** edit deletes the projection block entirely. No edit composes with another; each case is a single edit of ORIGINAL |
| grain | the delivered document; for FCL-1, the record keyed by id (see §4(c) grain declaration) |
| system boundary | model + endpoint + the frozen request bytes. Mini's graph, scheduler and store are **outside** it: C001 runs one call, not a template |
| history/continuity | none claimed. Each call is independent; no state crosses calls |
| enabling contributions | the operator-supplied FCL-1 language, the H005 instructions, the four codings, the decoder |
| contrasts | the four cases of §4 |
| normative relation invoked | none. No adequacy, merit or progress predicate is applied to any output |
| repair obligations **O** | **none.** C001 discharges no failed obligation of a prior cycle and makes no (P) claim (FW5:787–800) |
| protected obligations **P** (on the instrument) | (P1) the ORIGINAL case's bytes remain the occurrence's bytes; (P2) the correspondence table remains complete and published before dispatch; (P3) no case's request differs outside the objection block; (P4) no scoring key appears in any generated artifact; (P5) provider and study records stay write-once with no replay; (P6) root's reading columns stay empty until root fills them. Every one is enforced in code and asserted in `tests/test_contrast_triple_study.py`. **A loss against any of these must be exposed in the report, not repaired silently** (FW5:802) |

---

## 11. Known limitations and residuals

**L1 — the control is not length-matched.** Withholding the objection necessarily
shortens the brief (by ~7.6 k chars for the FCL arm, ~5.6 k for the prose arm). A
length-matched control would require irrelevant padding, which is a *different*
intervention with its own confound. C001 does not run one. Consequence: an
ORIGINAL/CONTROL difference is compatible with "the node responds to having a third
input at all" as well as with "the node used this objection's content". **The recoding
and carrier legs do not share this limitation** — they are length-matched to within 3%
— which is exactly why the three-case contract, and not the control alone, carries the
reading. A length-matched control is named as follow-up work (NOTES Q2).

**L2 — the instruction names a criticism the control cannot see.** The instruction says
"in light of the account, criticism and alternative". Holding it fixed is required by
§2. In the CONTROL case it therefore refers to something not delivered. The H005 system
prompt already covers this ("A missing view says what you can currently see; it does
not establish what happened earlier"), but the control means *objection withheld from
this node*, not *no criticism was ever made*, and must be read that way.

**L3 — the control's absent wording is borrowed.** `project()`'s absent string reads
"absent in the first template invocation", which in H005 describes a missing
`previous`/`origin` source in cycle 1, never a within-cycle source. C001 uses it
verbatim, as instructed, rather than inventing wording. Residual: the phrase carries an
H005-specific clause. An alternative neutral wording is named as follow-up (NOTES Q3);
running both would be a fifth case and a new plan.

**L4 — the projection header's SHA-256 lines vary honestly.** `project()`'s header
states the delivered document's body and commitments hashes. C001 recomputes them per
case, so they differ between ORIGINAL, RECODING and CARRIER. The `Artifact:` line keeps
the H005 objection artifact id in all three: it names the *criticism occurrence* whose
document is delivered in that case's coding, not the byte string, which the two SHA
lines identify. Residual: the varying hex is a carrier difference shared by RECODING
and CARRIER. It can only produce a **false negative** of the "not under recoding / not
under carrier" clauses — never a false positive — because if the hex drove the surface,
both legs would differ from ORIGINAL, which is the F2/F3 direction. *A second residual,
in the same field:* the header field is **named** "Original body SHA256" /
"Original commitments SHA256" by `project()`; in the RECODING and CARRIER cases it
reports the delivered bytes under that name, so the **label** is false of those two
cases while the **value** is true of them. The wording is the runner's own and was not
altered; the risk runs in the same false-negative-only direction as the varying hex.
Recorded as a further candidate for the neutral-wording follow-up already opened at
NOTES Q3.

**L5 — record-array order is *declared* carrier.** Reversing the FCL-1 `records` array
is treated as carrier at the grain of §4(c). If a reader holds that array order carries
emphasis, the carrier leg is instead a weak content change, and F3 should be read as a
criticism of the grain declaration rather than of the node. The declaration is in the
material so that this criticism has something to land on. *Second alternative reading of
F3:* the fcl CARRIER objection block is the **longest of the four**, +7.3 % on the
ORIGINAL block, and the inflation is the `indent=2` re-serialisation (§2, block-level
table). An ORIGINAL/CARRIER difference driven by block length alone is therefore a live
alternative to both the grain reading and the node reading, and root records which of
the three it takes.

**L6 — one occurrence, one problem, one cycle.** The objection under test is a single
authored document. Its particular content may be unusually easy or hard to use. Nothing
here generalises past it.

**L7 — the endpoints differ in more than identity.** Different families, different
default temperatures, different reasoning behaviour, different JSON enforcement. The
six cells are six occasions, never a comparison between models.

**L8 — redundancy can conceal use in endpoint invariance.** SEMANTIC_GUIDE states it
directly: "Recoding, changed-content and irrelevant-carrier contrasts help assess
content dependence; they do not replace an interpreted active route. Redundancy can
conceal use in endpoint invariance." A node whose surface is insensitive to all four
cases yields **F1**, not a clean null. A node whose surface is insensitive only to the
recoding and carrier legs may be using the objection's content, or may be **redundant
with respect to it** — reaching the same surface by a route the objection does not
enter. C001 cannot separate those two, and the D2/D3 nulls must never be reported as
though it could.

**L9 — the carrier leg is not comparable across arms.** The FCL-1 carrier reorders and
re-serialises structure (`records` reversed, `uptake` reversed, keys sorted,
`indent=2`); the prose carrier changes layout only (wrapping and bullet markers). An F3
that fires on one arm and not the other records **a difference between two
interventions**, not a difference between two commitment languages. §9 already forbids
reading an endpoint difference as a ranking; the same discipline is owed here.

---

## 12. Operating procedure

1. **Publication before dispatch.** `material.json`, this plan, `RECODING_TABLE.md`,
   `plan.json` and `preflight.json` are committed and pushed to `main`, and the remote
   commit and tree verified, **before** the first call. The recoding table in particular
   must be public before any reply exists.
2. **`prepare`** freezes `plan.json` (`plan_id` = digest of the plan body) and runs the
   offline preflight: it renders all 240 calls with an `OfflineProvider` in hand and
   asserts **240 planned, 0 provider calls**. No wall clock enters `plan_id`, any
   request digest, or any artifact digest; two `prepare` runs at different times produce
   byte-identical `plan.json`.
3. **`run --plan-id <id>`** dispatches by waves, ≤ 5 per credential, at the endpoint's
   own declared `timeout_seconds` (§5) — re-read off the frozen plan before each send and
   written into the request record and the receipt, `TIMEOUT_NOT_APPLIED` on any
   disagreement — writing an **attempt marker before the send**, then the raw reply text,
   then the receipt. Every
   record is opened `x` — write-once. A coordinate with an existing request, attempt or
   response refuses: `NO_REPLAY`. No automatic retry exists anywhere. Every failure
   records the **declared code** (`HTTP_429`, `KEY_MISSING`, `PROVIDER_NOT_USABLE`,
   `PROVIDER_CAP_EXCEEDED`, …) alongside the exception class, so a rate-limit storm is
   distinguishable from a missing key in the published record.
3a. **`run … --resume`** completes an interrupted occurrence: a coordinate that already
   has a receipt is skipped, and a coordinate with a request or attempt but **no**
   receipt still refuses (`NO_REPLAY`) — that is the ambiguous case, where a call may
   have reached the provider and been billed, and it is never silently re-sent. The wave
   record is the wave as the plan defines it, so it is byte-identical under any
   invocation and a genuine redefinition is still `WAVE_CHANGED`.
4. **`audit`** re-reads every written coordinate and recomputes custody end to end:
   request digest ↔ attempt ↔ receipt, provider bytes ↔ recorded hashes, delivered text
   ↔ provider record, artifact ↔ receipt — **and, beyond internal consistency**, ties
   each request back to the frozen plan (`messages_sha256`, `brief_sha256`,
   `objection_projection_sha256`, the arm's shared prefix and suffix hashes, and the
   `plan_id` itself → `REQUEST_NOT_FROM_PLAN`; and the endpoint's declared
   `timeout_seconds` in the request, in its spec and in the receipt →
   `TIMEOUT_NOT_APPLIED`) and **re-derives** each artifact's
   content digests from the delivered bytes through `decode_contribution`
   (→ `ARTIFACT_NOT_DERIVED_FROM_DELIVERY`). Without those two, a record set can be
   perfectly self-consistent about a brief that was never planned, or carry an artifact
   body no model ever returned. It also reports the run's failure-code profile and the
   per-endpoint seed regime aggregated over replicates.
5. **`table`** renders `COMPARISON.md`, `comparison.json` and the twelve juxtaposition
   files, and refuses to write a scoring key.
6. **Root reads content.** Root reads the juxtaposition and fills the empty columns.
   No agent fills them; no agent proposes a reading in them.
7. **Failures are records.** An endpoint failure, timeout, missing reply or containment
   kill is an operational delivery failure: the sanitized receipt is kept and **no
   semantic verdict is issued** for that coordinate (EXPERIMENT_METHOD; harness v1.3 §1,
   "a containment kill MUST NOT mint a warrant").
8. **Credentials** are read from the environment at call time only, never written to any
   record; `write_new` refuses any output containing a known key.

---

## 13. What would make this a new claim

Changing the node, the instruction, the problem, the objection document, the case set,
the endpoint set, the replicate count, the grain declaration of §4(c), the recoding
rules or any recoded unit, the pre-declared reading rule of §8a, the declared hedge
marker set, the declared artifact addresses, the per-endpoint completion ceiling or
wall-clock timeout of §5, **or the transport module's or endpoint
registry's bytes** changes the material or the driver, hence the `plan_id`, hence the
claim. (`prepare`, `verify`, `run`, `audit` and `table` re-hash the transport and the
registry on every invocation, so a transport change is a stop, not a surprise.) Such a change is a
**successor pre-registration with its own identity**, never an amendment of this one.
Development failures may motivate one; they do not license editing this plan after the
evidence.

## 14. What would reopen the inquiry after a negative result

* F2 or F3 firing at one endpoint but not others → a recoding/carrier sensitivity
  localised to an occasion; the next step is the same design on a second objection
  document, not a stronger claim from this one.
* F1 firing everywhere → the next step is P3 (criticism-ablation at occurrence-02, with
  a *substantively different* objection as the content-changing case) rather than a
  no-objection control, since P3's content change is length-matched by construction.
* The instrument holding but every cell unresolved through PARTIAL truncation → raise
  the ceiling, or split body and commitments into two calls, and re-register.
