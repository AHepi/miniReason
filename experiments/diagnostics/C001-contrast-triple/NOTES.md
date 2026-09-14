# C001 — design notes, the recoding rule, and open questions for root

Companion to `PLAN.md`. Design decisions and their reasons; what was deliberately not
done; what root has to settle. Nothing here is evidence.

---

## 1. Design decisions and why

**D1 — The node was chosen because it is the only one where holding the instruction
fixed is free.** P2 needs a single node whose successor surface can be read against a
varying objection. `fork5.response` takes `account`, `objection` and `rival` all at view
`both`, so the objection can be varied while two other inputs and the instruction stay
byte-identical. `carry` would have worked too but its inputs include `origin`, adding a
second absent-source projection; `objection` and `rival` are precisely the pair
Appendix B item 14 rules out.

**D2 — `direct_explicit_views`, not the canonical Mini render.** The canonical render
prefixes each port with `[<content hash>] (<kind id>)`, derived from the projected text.
Three of the four cases deliver different bytes, so that id varies across cases — an
uncontrolled carrier difference sitting inside the very comparison the study makes.
Freezing it at the ORIGINAL value would make the header assert a content address that
does not address the content. The runner's own non-Mini branch has no such identifier
and reuses `project()` unchanged, so the ORIGINAL objection block is byte-for-byte the
block the real H005 `response` node saw. This is a deliberate departure from H005's
`mini_*` rendering and is stated in `material.json.render.note`.

**D3 — The `Artifact:` line is held constant; the SHA lines are recomputed.** In all
three content-bearing cases the header names the same objection *occurrence* — because
it is the same occurrence, in three codings — while the two SHA-256 lines honestly
describe the bytes actually delivered. The alternative (freeze all header lines) would
put a false hash in front of the responder; the other alternative (drop the header)
would stop ORIGINAL being what H005 delivered. The residual is analysed in PLAN §11 L4:
it can only produce a false *negative* of the recoding and carrier clauses.

*Disclosure added after the adversarial review.* The header **field name** is
`project()`'s own: "Original body SHA256" / "Original commitments SHA256". In the
RECODING and CARRIER cases the value is a true hash of the bytes actually delivered, so
the label is false of those two cases while the value is true of them. The wording is
the runner's and was not altered; the residual is the same false-negative-only one as
the varying hex, and it is a further candidate for the neutral-wording follow-up opened
at Q3. PLAN §11 L4 states it.

**D4 — The recoding changes words and holds structure; the carrier changes
serialisation and holds words.** That gives the two legs disjoint operations, which is
what makes them separable at all:

| | words | structure / serialisation |
|---|---|---|
| RECODING | rewritten unit by unit | unchanged (ids, types, refs, uptake, record order, field order) |
| CARRIER | byte-identical | rewritten (key order, record order, indentation, wrapping, bullets) |

If both legs had reordered things, F2 and F3 could not be told apart.

**D5 — Unit-order preservation in the recoding.** Cross-unit sentence re-ordering is in
the declared rule set and was not used. Sentence order can carry argumentative
dependence ("There is also a second difficulty" presupposes a first), and preserving it
makes the correspondence table checkable one row at a time and makes the recoded
document mechanically reconstructible from the table. A reader who thinks this makes
the recoding too weak has a real objection — see Q1.

**D6 — Record-array reversal counts as carrier, by declaration.** The grain declaration
in `material.json.arms.<arm>.carrier.grain_declaration` says an FCL-1 document's content
is the *set* of records keyed by id. This is the most aggressive part of the carrier
leg and the most contestable; it is written down precisely so a criticism can land on
it rather than on the result (SEMANTIC_GUIDE, "these are criticisable interpretation
claims, not facts made true by a registry entry").

**D7 — The prose arm gets no mechanical surface beyond hashes and lengths.** There is
nothing to parse and this study does not invent a parser for prose. Inventing one would
be exactly the move FW5:1218 and the review's MC-08 warn against: fixing an accounting
predicate with an endpoint projection. Root reads the prose.

**D8 — A structured reference is unambiguous only when its prefix is retained.**
*Corrected after the adversarial review; the earlier wording of this note was wrong.*
The objection and the account share five of the objection's eight record ids
(`o1 c1 c2 p1 u1` of `o1 o2 o3 c1 c2 o4 p1 u1`), so a reference reduced to the text
after `#` is not unambiguous at all: five of eight would be attributed to the objection
whichever document the successor actually cited. What disambiguates is the **prefix**,
which names the artifact. The three artifact addresses are now declared in
`material.json.arms.<arm>.artifact_addresses`, and `fcl_surface` resolves each
reference's prefix against each address, against that address truncated to its first 16
hex characters (the form the real H005 response node emitted — `b5dbbb04b5acd035#c2`),
and against the source name. The table then reports **separate** columns for
objection-prefixed, account-prefixed and rival-prefixed references, plus a column for
references whose prefix matches nothing. A reference with **no** prefix is not a
cross-document reference: it stays in the bare-token channel and is unresolved
(FW5:634). The bare-token channel no longer double-counts a structured reference — a
token preceded by `#` or `.` is excluded from it — so the two channels PLAN §7 presents
as separate really are separate.

**D9 — Counts defeat; they never warrant.** Following Appendix B item 1 (FW5:851
continues "…are not outlawed as information"), the falsifier in PLAN §8 admits a
mechanical *defeater* — byte-identical ORIGINAL and CONTROL surfaces defeat D1 — but no
mechanical confirmer. The positive reading is root's, off the juxtaposition.

**D10 — N = 5 is a within-case baseline, not a sample size for a statistic.** Its job is
to let root see how much two replicates of the *same* case differ before reading
anything into a difference between cases. No test statistic is computed and none should
be.

**D11 — Waves hold at most five per credential, and 46 of the 47 are single-key.** The
coordinate order is endpoint-major, so 46 waves draw on one credential and hold five. The
**one** wave straddling the boundary between `deepseek-flash`'s forty coordinates and the
first Ollama endpoint's holds ten — five on each credential — which is inside the
five-per-credential authorisation, not an exception to it; `WaveShape` in the suite pins
both figures. *(This note and PLAN §5 previously said every wave was single-key and that
at most five requests were ever in flight. That was false of the boundary wave. It is
corrected here before dispatch, not repaired afterwards.)* The design is still
conservative: deliberately interleaving the keys throughout would put ten in flight on
every wave and roughly halve the wall time, but the coordinate order is inside the frozen
plan, so changing it mints a new `plan_id` — not worth a new pre-registration for a
scheduling gain.

**D12 — `envelope_unwrap` repairs the carrier of the *reply*, never its content.** The
two permitted repairs (one outer code fence; `strict=False`) are declared in the
material before dispatch, applied in a fixed order, and recorded per call together with
`strict_parse_would_succeed`, so a reader can see exactly which cells needed one and
re-derive the surface without them. Raw bytes are kept untouched. This is a declared
difference from the H005 decoder, forced by Ollama cloud accepting `response_format`
without enforcing it.

**D13 — PARTIAL is unresolved, not comparable.** A reply truncated at the ceiling has a
truncated commitment surface; comparing it with a complete one would manufacture a
difference out of a delivery fact. The cell keeps its hashes and lengths, its mechanical
columns are withheld, and it is listed in `unresolved_cells`.

**D15 — `max_tokens` is per endpoint, and the Ollama ceiling was raised before
dispatch.** `deepseek-flash` keeps 8192; the five Ollama endpoints carry 32768
(authorised maximum 32768, inside the transport's own 1…393216 validation range). The
reason is live evidence, not caution: under **REC-20260914-S**, F001
(`experiments/diagnostics/F001-fork5-multifamily`, `occurrence-04` `ollama/glm-5.3` and
`occurrence-05` `ollama/kimi-k3`, both at 8192) returned **five** nodes with
`INCOMPLETE_GENERATION`, `finish_reason "length"`, `completion_tokens 8192` and **no
content at all** — the whole ceiling spent on reasoning — plus **two** PARTIAL nodes on
the same signature. At 8192 C001 would have been measuring its own ceiling on two of its
six endpoints. The raise does **not** manipulate reasoning: `temperature`, `thinking` and
`reasoning_effort` are still never sent and the endpoint default still decides
(§5, D13 unchanged). Its cost is that the six endpoints no longer share one ceiling, so
a `deepseek-flash`-vs-Ollama difference has one more uncontrolled difference behind it
(§11 L7). A cell that hits even the raised ceiling is still PARTIAL-and-unresolved, or a
recorded refusal; **no cell is rescued by the raise**.

**D16 — `timeout_seconds` is per endpoint too, and the Ollama timeout was raised before
dispatch — without touching `endpoints.json`.** F001's runs used the registry's fixed
180 seconds, which is not a per-arm declaration and did not move with the completion
ceiling; under **REC-20260914-T**, at `max_tokens` 32768, it took *both* failures of the
run — `occurrence-07/responses/daily/mini_fcl/cycle01/objection.json` on `ollama/glm-5.3`
(`TRANSPORT_OR_RESPONSE_ERROR`, provider record "The read operation timed out",
`elapsed_ms` 180368, `settings.timeout_seconds` 180) and
`occurrence-08/responses/daily/mini_fcl/cycle01/carry.json` on `ollama/kimi-k3` (the same
at `elapsed_ms` 180456) — while `finish_reason: "length"` occurred zero times there. C001
runs 240 calls at the same ceiling on the same families among others, so it declares the
timeout per endpoint: 180 for `deepseek-flash`, **600** for the five Ollama endpoints,
600 being the transport's own validation maximum (`Endpoint.__post_init__` admits
1…600). The mechanism matters as much as the number: `src/minireason/data/endpoints.json`
is a **published, pinned file that other studies' plans pin too**, so it is not edited.
The declared value is applied to the resolved `Endpoint` *value* by `dataclasses.replace`
inside `resolve_endpoint` — the one place every provider this driver constructs passes
through — frozen into `plan.json`, written into every request record and receipt, re-tied
to the plan by `audit`, and refused as `TIMEOUT_NOT_APPLIED` wherever plan, material,
spec, record and transport disagree. It changes **no request byte**: a socket deadline is
not a payload field, and a test asserts the payload digest is the same at 180 and at 600.
Its cost is the ceiling's cost restated — the six endpoints no longer share one wall
clock (§11 L7) — and a call that exceeds 600 s is still a refusal compared against
nothing. **No cell is rescued by the raise.**

**D14 — The driver refuses to name a quantity.** `assert_no_scoring_keys` runs over
`comparison.json` before it is written, and a test also scans every `COMPARISON.md`
table header. *Stated precisely, after the review:* over the CURRENT output this guard
cannot fire, because every key in `comparison.json` comes from a code constant, from
`FCL_TYPES`/`FCL_REF_FIELDS`, or from an objection record id in the material — no
model-produced string ever becomes a key. It does not constrain this output; it is
insurance against a future edit that interpolates model text as a key. Its own logic is
now exercised by negative tests (`GuardsWithTeeth`) that feed it forbidden keys nested
in lists and sub-dicts and assert `SCORING_KEY_FORBIDDEN`.

---

## 2. The recoding rule, in full

Authored offline by the study designer before dispatch. **No model call produced any
entry.** Published in `material.json` and rendered to `RECODING_TABLE.md`.

*Units.* Prose: sentences from `re.split(r'(?<=[.!?])\s+', paragraph.strip())`,
paragraphs from `\n\n`. FCL-1: the same split applied to each string field of each
record. The split is exactly reversible — joining units with a single space and
paragraphs with `\n\n` reproduces the original bytes, which `prepare` checks — so the
table is a complete, loss-free partition of the document, not a summary of it.
85 units: 50 FCL (28 body + 22 field), 35 prose (20 body + 15 commitment).

*Operations.* `R1` synonym (contraction ↔ expansion counts as R1: same lexical items,
same force) · `R2` constituent-order within a unit — clauses, phrases, adverbials;
broadened from "clause-order" on 2026-09-14 because the label was already carried by
units that front a PP or an adverbial, and it may not be used for an operation on an NP
head · `R3` voice · `R4` deixis ↔ antecedent within a unit, **only where the
demonstrative has a unique antecedent inside the same paragraph** · `R5` equivalent
connective. Each unit's row names the operations actually applied to it. Information
structure **beyond the topic/focus reassignment intrinsic to `R3`** (clefting,
pseudo-clefting, topicalisation, equative inversion, existential-`there` insertion or
deletion, subordination ↔ coordination, assertion ↔ presupposition) and
determiner/definiteness change are **not** declared rules and are used nowhere; the
units reverted for one are listed exhaustively in `not_exercised`.

*Invariants.* Unit count, order and boundaries preserved. Quotations verbatim — a
recoding must not rewrite what the objection quotes from the account or the problem.
FCL-1 ids, types, `uptake` and all reference arrays unchanged. No proposition added,
dropped, strengthened or weakened; hedges kept at their original force ("I cannot tell
from the material" stays a disclaimer, not a concession). No information-structure
operation **beyond the topic/focus reassignment intrinsic to `R3`**, and no determiner
or definiteness operation **of its own** — an active/passive alternation *is* such a
reassignment and 16 fcl and 14 prose units apply one, and an `R1` paraphrase or an `R3`
verbal ↔ nominal alternation carries its own determiner with it (26 units show a
determiner-token delta of that kind), so the invariant is worded to exclude those rather
than to be refuted by them. What is excluded is a determiner change applied on its own,
to a referring expression the unit otherwise leaves alone. FW5:609's four constituents —
target, defect, grounds, bearing — preserved.

*What makes it checkable.* The recoded document is **derived from the table**: `prepare`
rebuilds it from the `recoded` column alone and refuses unless the result equals the
frozen bytes. So a reader who disputes one row disputes one row of the delivered
document, not the whole recoding.

*Worked examples.*

| unit | original | recoded | rules |
|---|---|---|---|
| `B.P3.S5` (fcl) | The account's test does not distinguish these. | These are not told apart by the account's test. | R1 R3 |
| `K.o2.bearing.S1` | Weakens the claim that falling recurrence would confirm c1 and rising recurrence would refute it; the test has lower discriminating power than the account implies. | Weakens the claim that a fall in recurrence would confirm c1 and a rise in recurrence would refute it; the discriminating power of the test is lower than the account implies. | R1 R3 |
| `C.P4.S3` (prose) | I'd treat a quiet week as uninformative either way. | I would treat a quiet week as uninformative in either direction. | R1 |

*The 2026-09-14 re-read.* After the adversarial review all 85 units were re-read once
more, unit by unit, against FW5:609 constituent role (target *z*, defect *δ*, grounds
*g*, bearing), hedge force, evaluative modals, determiner and definiteness, information
structure, and antecedent resolution. Thirty-nine units changed; they are listed with
the reason in `FIXES.md`. The principle applied where the review offered a choice was to
**revert to the simplest declared operation** rather than to declare a new rule: no `R6`
(information structure) and no `R7` (determiner/definiteness) were added, and `R4` came
out of the re-read declared but unexercised, because under its uniqueness restriction no
demonstrative in either document has a unique antecedent inside its own paragraph.

*The 2026-09-14 spot-check closure.* An independent reviewer then re-read all 85 units
against the originals and re-ran the mechanical checks from a separate implementation.
It returned three units whose operation lay outside the declared rule set (fcl
`K.o1.text.S1`, `B.P4.S1`, `B.P4.S2` — two existential-`there` moves and one
definite-possessive predicate nominal) and twenty more it called doubtful. Every one was
closed by **reverting** the recoded text or by **correcting the label**, never by
declaring a new rule; thirty units changed in text, label or both, and each is listed
with its old and new wording in `FIXES.md` ("Spot-check closures"). Four documentation
faults were closed with them: the information-structure invariant was reworded to admit
the `R3` alternation it had always licensed, `R2` was broadened to constituents, the
`not_exercised` revert list was made exhaustive, and the limits of the hedge-force
counter were published.

*What `prepare` now checks mechanically*, beyond coverage and reconstruction:
(a) every FCL-1 record's id, type, reference arrays, non-string fields, the document's
`uptake` list and its language tag are unchanged, record by record; (b) every declared
hedge/modal marker family is preserved **in count, per unit**, after contraction
expansion (`RECODING_HEDGE_FORCE_CHANGED`) — the marker table is published in
`RECODING_TABLE.md`, together with the paragraph saying what the counter **cannot** see
(evaluative and relational predicates such as `consistent with` → `fit`, `downweight`
→ `discount`, `issue` → `point`, an `un-` litotes, `or` → `and` under negation, and
get-passive → be-passive), which is checked by reading and by the published
two-reviewer re-read; (c) every unit's declared rule labels are a subset of the declared
rule set, and the report names which declared rules went unused. Quoted material is also
compared span by span (`RECODING_QUOTATION_CHANGED`). None of this establishes
constituent-role preservation — that is a reading, and the published unit table is what
makes it checkable — but each of the three faults the review found at a unit now has a
mechanical refusal or a named pinning test behind it.

---

## 3. Open questions for root

**Q1 — Is a unit-order-preserving recoding strong enough?** The recoding rewrites every
sentence but moves none. FW5:628 asks that "content-preserving recodings preserve the
interpreted transition"; it does not say how far a recoding must travel. A stronger
recoding (paragraph re-ordering where no argumentative dependence exists) would be a
harder test of D2 but would need per-move dependence arguments. **Root's call: accept
this recoding as adequate, or require a second, order-changing recoding as a fifth
case.**

**Q2 — Should there be a length-matched control?** PLAN §11 L1: the no-objection
control is ~7.6 k chars shorter for the FCL arm. A padded control (irrelevant text of
matched length) would separate "responds to the objection's content" from "responds to
having a third input". It is a different intervention with its own confound — the
padding has to be *about* something. **Root's call: run C001 as designed and read the
recoding/carrier legs as carrying the weight, or add a padded fifth case before
dispatch.**

**Q3 — The control's borrowed absent wording.** `project()`'s absent string says
"absent in the first template invocation", which is H005's reason for a missing
`previous`/`origin`, not C001's reason for a withheld within-cycle view. The instruction
was to use the runner's own wording, and the plan does. **Root's call: keep it (one
fewer invented string), or mint a neutral wording and re-register.**

**Q4 — Is record-array order carrier?** D6/L5. If root reads array order as content,
the carrier leg is a weak content change and F3 must be read as a criticism of the grain
declaration rather than of the node. **Root's call: endorse the grain declaration, or
split the carrier leg into whitespace-only and order-changing variants.**

**Q5 — What does "differs" mean, operationally, for root? — CLOSED before dispatch.**
The answer is now PLAN §8a and it is **mirrored into `material.json.reading_rule`**, so
it sits inside the frozen identity rather than beside it: four registers (T target
named, E objection record engaged and prefix-resolved, D proposed action, G grounds
cited), each marked `differs` / `same` / `unresolved`, never summed or averaged; the
within-ORIGINAL replicate spread as the baseline; a fixed order of reading (the
within-ORIGINAL spread is written into COMPARISON.md first and not revised); and a
register-to-falsifier mapping. `COMPARISON.md` now renders the registers and an empty
mark grid per cell. Mirroring it changed `plan_id`, as it must.

**Q6 — Does the seed matter for DeepSeek?** Support is unverified there. If DeepSeek
ignores the seed, its five replicates are five independent samples and its within-case
spread will be wider than the Ollama endpoints' — which changes the baseline against
which root reads that cell, not the pattern. Every record carries `seed_requested`,
`seed_sent`, `seed_echoed_in_response` and `system_fingerprint`. *Corrected after the
review:* `seed_echoed_in_response` used to be computed as `'seed' in <call record>`,
which no OpenAI-compatible call record ever satisfies — the field could only ever say
`false`, which asserted an absence it could not have observed. It is now tri-state: the
echoed value when the provider actually returned one, and `null` — unknown, not denied
(FW5:634) — otherwise. `system_fingerprint` is the determinism signal these families do
return and is recorded beside it; `audit` reports both aggregated over the five
replicates of an endpoint, not sampled from whichever replicate came last.

**Q7 — Should the prose arm get any mechanical surface at all?** D7 says no. A reader
may object that byte hashes and lengths are so thin that the prose arm reduces to
"root read twenty texts". That is the intended state, but root should confirm it is
worth the 120 calls.

---

## 4. What was deliberately not built

* No parser, classifier or judge over the successor's prose.
* No similarity measure, distance, or threshold anywhere.
* No automatic retry, no fallback endpoint, no "best of N".
* No padded control, no second recoding, no native-reasoning arm (each is a distinct
  intervention needing its own registration).
* No write into `/home/user/miniReason`. Every source is read-only and hash-pinned.

---

## 5. Staging, provenance and how to run

Staged under `scratchpad/contrast/` in repository layout:

```
experiments/diagnostics/C001-contrast-triple/PLAN.md
experiments/diagnostics/C001-contrast-triple/NOTES.md
experiments/diagnostics/C001-contrast-triple/material.json
experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md
tools/contrast_triple_study.py
tests/test_contrast_triple_study.py
```

`material.json` is generated by
`experiments/diagnostics/C001-contrast-triple/build/build_material.py` from
`build/recoding_units.py` beside it (the hand-authored recoding); both were staged at
`scratchpad/contrast/.build/` and are published under the study directory as provenance.
They are provenance, not the study's content: the material is the frozen artifact. The same build script also
writes `RECODING_TABLE.md`, by calling the driver's own `render_recoding_table` on the
material bytes it has just written — the same function `prepare` calls — so the table
and the material cannot disagree about a unit, a rule label or an invariant (a test
asserts the staged file equals the driver's rendering).

**Resolving the transport.** Before publication the transport module and its endpoint
registry live only in the provider staging tree, so `MINIREASON_PROVIDER_SRC` must point
at it. **After publication that export must be dropped**: `src/minireason` in the
repository is then the module, and a stale staging path on `PYTHONPATH` would silently
shadow the published one — which is the single thing this suite exists to rule out. The
test file therefore hardcodes no path and exports nothing: it uses
`MINIREASON_PROVIDER_SRC` when the operator sets it and `REPO/src` otherwise. Whichever
module is resolved, its bytes and its `data/endpoints.json` are re-hashed against
`material.json.transport_pins` by `prepare`, `verify`, `run`, `audit` and `table`
(`TRANSPORT_PIN_MISMATCH`).

```
export MINIREASON_PROVIDER_SRC=<provider staging>/src      # BEFORE publication only
export PYTHONPATH="$MINIREASON_PROVIDER_SRC:/home/user/miniReason/src"

python3 tools/contrast_triple_study.py prepare \
    --material experiments/diagnostics/C001-contrast-triple/material.json \
    --output   experiments/diagnostics/C001-contrast-triple/occurrence-01
# -> {"plan_id": "...", "planned_calls": 240, "provider_calls": 0}

# publish PLAN.md, NOTES.md, material.json, RECODING_TABLE.md, plan.json, preflight.json
# to main and verify the remote tree BEFORE the next line.

python3 tools/contrast_triple_study.py run   --output <occ> --plan-id <id>
# after an interruption, complete the occurrence without replaying a spent call:
python3 tools/contrast_triple_study.py run   --output <occ> --plan-id <id> --resume
python3 tools/contrast_triple_study.py audit --output <occ>
python3 tools/contrast_triple_study.py table --output <occ>

python3 -m unittest discover -s tests -p 'test_contrast_triple_study.py'
```

`run` needs `DEEPSEEK_API_KEY` and `OLLAMA_API_KEY` in the environment at call time; they
are never written to any record. `prepare`, `audit` and `table` need no credential and
open no socket.

---

## 6. Receipts owed before dispatch

1. A decision-ledger receipt for this design (choice, reason, contribution to the end
   goal, pending state) before any call.
2. Publication of the six staged files to `main`, remote commit and tree verified.
3. A recorded answer to Q1–Q5 — at minimum Q2 and Q5, which can still change the design.
4. A reachability check of the six endpoints at dispatch time, with any unreachable one
   recorded as `NOT_DISPATCHED` rather than substituted.
