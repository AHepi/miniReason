# B001 — bare-model and native-reasoning matched comparison

**Staged, not published. Zero provider calls authorised by this register.**

B001 was commissioned as a three-arm mechanism argument: a BARE arm, a
NATIVE-REASONING arm, and the already-published Mini fork5 chain as a third arm,
over the same frozen problem bytes. It was commissioned on the premise that *no
published study yet has a bare-model arm*.

**The committed bytes refute that premise.** Every arm B001 was asked to add is
already published, on the material it was asked to use, at the conditions it was
asked to hold fixed. What is missing is not the arms. It is (i) the **reading**
of them, which the permitted instrument cannot perform, and (ii) the **content of
the native arm's reasoning**, which the transport discards by design.

This register therefore states the claim and its defeat conditions, states the
arm table, states what is fixed and what changes, and then **refuses the
dispatch** and says exactly why, with the refusal made mechanically checkable by
`tools/arm_inventory.py` and its suite. Sections 1–7 are the design as
commissioned; section 8 is the refusal; section 9 is what B001 stages instead.

---

## 0. The premise, checked

Run, from this directory, against the read-only repository:

```
PYTHONPATH=<repo>/src:tools python -X utf8 tools/arm_inventory.py <out> \
    --study <repo>/experiments/diagnostics/H005-open-prose-commitments \
    --study <repo>/experiments/diagnostics/F001-fork5-multifamily \
    --study <repo>/experiments/diagnostics/F002-fork5-raised-clock \
    --proposal proposal-bare-deepseek.json
```

`proposal-bare-deepseek.json` **is** the brief's arm (a), declared at the
conditions of the occurrence whose Mini chain it would be compared against:
`deepseek-flash`, `kind` `bare`, `surface` `prose`, `max_tokens` 8192,
`timeout_seconds` 180, `seed` null, `daily`, cycle 1. The inventory reports:

| published arm | problem/cycle match | terminal artifacts | differs on |
|---|---|---:|---|
| `F001-fork5-multifamily/occurrence-01/bare` | yes | 1 | **nothing** |
| `H005-open-prose-commitments/occurrence-01/bare` | yes | 1 | `kind`, `surface` — *fields H005's plan does not record at all* |
| `F001-fork5-multifamily/occurrence-02…06/bare` | yes | 1 each | `endpoint`, `seed` |
| `F001-fork5-multifamily/occurrence-07…08/bare` | yes | 1 each | `endpoint`, `max_tokens`, `seed` |

The three facts that follow, each pinned by a test:

* **H005 occurrence-01 publishes all five arms** — `bare`, `native`, `matched`,
  `mini_prose`, `mini_fcl` — on `daily` cycle 1, with **17 provider call
  records**, on `deepseek-flash` at 8,192 tokens and a 180-second clock. The
  five-arm comparison the brief describes is not missing; it is the study H005
  already ran.
* **F001 occurrence-01 publishes `bare`, `native`, `mini_fcl`, `mini_prose`** —
  **12 provider call records**, same endpoint, same ceiling, with `kind` and
  `surface` declared per arm in `arms.json`, which H005's plan does not carry.
* **Every F001 occurrence, 01 through 08, declares a `bare` arm** and every one
  of them has a terminal `daily/bare/cycle01/answer` artifact.

Re-sending any of these coordinates is a replay. The runner refuses it
(`NO_REPLAY`, write-once records) and the continuation workflow forbids it
("do not … rerun completed experiments"). **B001 does not re-run them.**

---

## 1. The claim under test, and what a defeat looks like

The claim is scoped to what the published arms could settle *if read*. It is not
a claim about models, families, creativity or Mini in general.

> **C1.** On the H005 `daily` problem at cycle 1, under `fork5`, the five-call
> chain's authored commitment surface takes up and carries forward material that
> the one-call arms' surfaces do not — specifically, on the four C001 §8a
> registers: **T** the target named, **E** the objection record engaged, **D** the
> proposed disposition, **G** the grounds cited.

C1 is a claim about *what the surfaces exhibit*, never a witness of reason use:
FW5:628 requires a structural map that a transcript does not supply, and C001 §9
already fixes that ceiling for this repository.

### Defeats for Mini — Mini is allowed to lose

* **DM1 — the chain buys no distinction.** Root reads the `bare` answer and finds
  it already carries, in prose, the same four registers the `mini_fcl` chain's
  records carry: same target, same criticism engaged, same disposition, same
  grounds. Then the chain bought nothing at this node set, and the FCL-1 carrier
  is a notation rather than an enablement (LP-05, LP-07).
* **DM2 — the chain's own structure does not hold.** The importer's published
  residues already say whether the chain's authored refs resolve to anything and
  whether each document's declared `uptake` matches the records present. A chain
  whose refs resolve to nothing, or whose `uptake` omits its own records, has
  produced the appearance of cross-document structure without the structure.
* **DM3 — five calls lost content relative to one.** The `carry` node is the
  chain's completed contribution. If root reads it as less differentiated than
  the `bare` answer, the chain spent four extra calls to contract. *This defeat
  has a fact waiting for it: at F001 occurrence-01 the `bare` answer is 5,365
  characters for 1,083 completion tokens, and the `native` answer 3,492
  characters for 3,701 completion tokens of which 2,979 were reasoning.* Neither
  has been read.

### Defeats for the bare arm

* **DB1 — the comparison is vacuous, not favourable.** The `bare` answer
  represents no objection, no rival and no criticism at all, so there is nothing
  for T/E/D/G to apply to. That is not "bare did as well"; it is "the registers
  do not apply", and the cell is **unresolved** (FW5:634), never a point for
  either side.
* **DB2 — no independent surface.** The `bare` answer's `commitments` repeats its
  `body` wholesale, which the instruction forbids. There is then no commitment
  surface of its own to place beside the chain's.

### The defeat that is available today and has never been taken

* **DX — the topology, not Mini.** H005 occurrence-01's `matched` arm is *the
  same five-call topology and selected field content as the Mini arms, rendered
  directly outside Mini, with free-prose commitments* (PROTOCOL §Five arms). It
  is published and complete for `daily` cycle 1. **If root reads `matched` and
  `mini_prose` as indistinguishable on T/E/D/G, then nothing this programme
  attributes to Mini is Mini's — it is the topology's.** That is the sharpest
  available defeat of Mini's rationale, it requires no provider call, and it has
  never been performed. B001 promotes it (§9, B001-P1).

---

## 2. The material

The same frozen problem bytes the fork5 chain received: **`daily`, cycle 1,
template `fork5`**, as frozen in
`experiments/diagnostics/H005-open-prose-commitments/material.json` and copied
with one added `study_id` key into
`experiments/diagnostics/F001-fork5-multifamily/material.json`.

The Mini-chain arm is the **already-published record**, not a re-run:

| occurrence | endpoint | ceiling / clock | Mini arms complete for `daily` cycle 1 |
|---|---|---|---|
| `H005-…/occurrence-01` | `deepseek-flash` | 8192 / 180 | `mini_fcl` 5 nodes, `mini_prose` 5 nodes, `matched` 5 nodes |
| `F001-…/occurrence-01` | `deepseek-flash` | 8192 / 180 | `mini_fcl` 5 nodes, `mini_prose` 5 nodes |
| `F001-…/occurrence-08` | `ollama/kimi-k3` | 32768 / 180 | `mini_prose` 5 nodes; `mini_fcl` 4 of 5 (`carry` absent) |

**F001 occurrence-01 is the designated occurrence** for B001's reading: it is the
only one carrying `bare`, `native`, `mini_fcl` and `mini_prose` all complete,
with kinds and surfaces declared in `arms.json`, at one ceiling and one clock.

**F002 is not available and is not used.** Its two occurrences declare
`mini_fcl` alone at 32,768/600 and are **in flight** under another agent at the
time of writing. Per the ledger's last F002 checkpoint, occurrence-01 stands at
`COMPLETE` 3, `FAILED` 1, `unvisited` 1 with its invocation `"complete": false`
— one FAILED node ends that arm for the rest of the occurrence, so **F002
occurrence-01 will never carry a complete fork5 chain** — and occurrence-02 is at
`COMPLETE` 4 with `carry` still ahead of it. The brief's 32768/600 conditions
therefore have no completed Mini chain to compare against, and no bare arm at
those conditions exists anywhere. A B001 arm at 32768/600 would be matched to
nothing. Nothing in this register reads, re-sends or depends on F002's in-flight
records.

---

## 3. The arms

| | (a) BARE | (b) NATIVE-REASONING | (c) MINI CHAIN | (d) MATCHED-TOPOLOGY | (e) MATCHED-CONCAT |
|---|---|---|---|---|---|
| calls | 1 | 1 | 5 | 5 | 1 |
| instruction | `bare_instruction` | `bare_instruction` | 5 `fork5` node instructions | 5 `fork5` node instructions | the 5 node instructions concatenated |
| topology | none | none | fork5, selected views | fork5, selected views, no Mini | none |
| engine | none | none | Mini compiler/reducer/ports | none | none |
| wire | `thinking: disabled` | `thinking: enabled`, `reasoning_effort: low` | `thinking: disabled` | `thinking: disabled` | `thinking: disabled` |
| surface | prose (forced) | prose (forced) | `mini_fcl` FCL-1 / `mini_prose` prose | prose | prose (forced) |
| **status** | **published** F001 occ-01, H005 occ-01 | **published** F001 occ-01, H005 occ-01 | **published** both | **published** H005 occ-01 | **absent everywhere** |

### Held fixed across (a)–(e)

The problem bytes; the system message; the material digest; the endpoint
(`deepseek-flash`); the completion ceiling (8,192); the wall clock (180 s); the
seed (null — DeepSeek declares none); `temperature` and `top_p` at provider
default; `response_format: {"type":"json_object"}`; zero retries at every layer;
write-once records with `NO_REPLAY`; the `(body, commitments)` envelope contract.

### What changes, arm by arm

* **(a) → (c):** six things change **at once** — the number of calls (1 → 5), the
  tokens spent, the instruction text, the number of authored documents (1 → 5),
  the availability of selected views of earlier nodes, and the commitment carrier
  (prose → FCL-1 for `mini_fcl`). A BARE-versus-chain difference is therefore a
  difference between two *bundles*, and attributing it to any one of the six is
  not available from this pair alone. This is stated as a limitation, not
  repaired.
* **(a) → (b):** exactly one wire field changes — `thinking` `disabled` →
  `enabled`, with `reasoning_effort: low`. Everything else is byte-identical:
  `messages` are equal at F001 occurrence-01, verified. `prompt_tokens`
  nonetheless differs (462 vs 487) because the control is priced server-side;
  that is an uncontrolled residual, recorded.
* **(c) → (d):** the Mini engine is removed and nothing else. (d) is the control
  that separates *Mini* from *the fork5 topology*.
* **(c) → (e):** the topology is removed and the instructions kept. (e) is the
  control that separates *five calls with selected views* from *the chain's
  instructions and more tokens spent in one call*.

### The matched direct control that would defeat the rationale

Two are needed, and they are different controls:

* **(d) MATCHED-TOPOLOGY** defeats *"the difference is Mini's"*. It exists,
  published, unread (§1 DX).
* **(e) MATCHED-CONCAT** defeats *"the difference is the chain and not the token
  spend"*. It does **not** exist. It is specified here and **not dispatched**
  (§8).

Neither control separates the commitment **carrier**: `mini_fcl` authors FCL-1
and every other arm authors prose. That separation is `mini_prose`'s job, and
`mini_prose` is published in both occurrences.

---

## 4. How the arms would be read

Through `tools/use_relation_h005.py` only, juxtaposed, with the four root columns
(`root_reading`, `root_passage_cited`, `root_notes`, `root_initials_date`)
emitted empty and filled by root alone. The four C001 §8a registers T/E/D/G
apply, reported separately, never summed, averaged, weighted or ranked. No score,
no rank, no merit, no progress meter. `unresolved` is a legal value and stays
unresolved (FW5:634).

**This is where the design fails, and §8 says why.**

---

## 5. Claim ceiling

* **One problem, one cycle, one template, one endpoint.** Nothing reaches
  `physics`, `philosophy`, `sociology`, cycles 2–3, `return6`, `weave7`, or any
  other family.
* **Consistent-with, never a witness.** The best positive outcome is: *these
  surfaces are consistent with the chain having taken up material the one-call
  arms did not*. A transcript supplies no active-route map, no role-binding
  correspondence and no three-case contrast (FW5:628, :630; C001 §9).
* **N = 1 per arm.** The published Mini chain is one invocation. There is no
  within-arm replicate spread, so C001 §8a's replicate-baseline rule — a register
  is `differs` only if the difference is not also read between replicates — has
  **no baseline available on the Mini side**. Any cross-arm difference read here
  is therefore compatible with ordinary run-to-run variation and must be reported
  as such. This alone bars a strong reading.
* **No creativity claim, no pretraining-repertoire claim.** A finite observation
  does not establish creativity across tasks or what the model already held
  (PURPOSE.md; LP-17).
* **ECS is not refuted by an implementation failure.** An unreadable arm, a
  discarded reasoning text and an absent control are facts about this
  implementation and this instrument. None bears on FW5 or ECS 2.0.
* **No (P) claim.** No repair, no progress, no `ProducedBy`. One cross-section.
* **Nothing here ranks `deepseek-flash` against any other family**, and no count
  in any output is a warrant (FW5:851).

---

## 6. The instrument

**Dispatch driver — none is needed, because nothing dispatches.** Had an arm been
authorised, the answer would have been:

* **`tools/contrast_triple_study_v2.py` does not serve.** It is not a general
  brief driver. Its material schema is `minireason.c001.material.v1`, its cases
  are the closed tuple `('original','recoding','carrier','control')`, and
  `validate_material` requires the recoding correspondence table, the carrier
  normalisation and the control-leak check. Generalising it to arbitrary briefs
  would be a rewrite, not a parameterisation, and would have to be a new identity
  anyway.
* **`tools/multicycle_commitment_study_multi_v3.py` serves (a) and (b)
  directly.** `nodes_for` already returns a single `bare_instruction` node for any
  arm whose `kind` is in `BASELINE_KINDS = ('bare','native')`, and `settings_for`
  already emits the thinking control on the `deepseek` family alone. No new
  driver would be needed for the BARE or NATIVE arms. This is itself evidence for
  §0: the runner was *built* to carry these arms, and did.
* **(e) MATCHED-CONCAT would need a successor runner.** `KINDS` already admits
  `'matched'`, but `is_baseline` excludes it, so a `matched` arm receives the full
  five-node template — it is (d), not (e). A one-call concatenated arm is a new
  kind and would be `tools/multicycle_commitment_study_multi_v4.py`: a byte copy
  of v3 with a declared difference list, a `# V4:` mark per hunk and a diff-proof
  test, exactly as v2 and v3 were made. **It is not written**, because §8 refuses
  its dispatch and writing a driver for an unauthorised arm would be building an
  instrument for an experiment that cannot be read.
* **Replicates would need one arm per replicate.** The coordinate is
  `(problem, arm, cycle, node)`; there is no replicate axis. Five replicates means
  five arm names (`bare_r1`…`bare_r5`), which the runner admits. On
  `deepseek-flash` `seed` is null, so replicates are independent draws; on an
  Ollama family the declared `seed: 7` would make five replicates of one payload
  near-identical, and the seed would have to be varied — which changes what is
  held fixed.

**New offline instrument — written, with tests.** `tools/arm_inventory.py`:
read-only, provider-free, deterministic, no score/rank/label anywhere, every file
digested, nothing written under any occurrence. It answers the two questions
whose wrong answers produced this brief: *which arms are already published, at
which conditions*, and *which of them the published reading instrument can read*.
The readability answer is the importer's own — `FCL_SURFACE_ARMS` is imported,
never restated — so it cannot drift from the instrument it reports on.

---

## 7. Call count and wall time

**Zero provider calls. Zero wall time. Zero tokens.** Nothing in this register is
authorised to contact a provider.

The offline inventory over all eleven occurrences of the three studies completes
in well under a second, digests 121 files and lists 100 terminal coordinates.

Conditional figures, for a successor that is *not* authorised here: arm (e) at
five replicates on one endpoint is 5 coordinates, one wave under the
five-per-credential ceiling, one round; at F001 occurrence-01's observed
`bare` latency of 9.4 s and `native` of 22.6 s, a single wave is well under a
minute of wall time and roughly 8 k prompt tokens plus whatever the ceiling
admits. The cost was never the obstacle. The reading was.

---

## 8. Refusal — stated honestly, and mechanically checkable

Three independent blocks. Any one of them alone would be enough.

### B1 — arms (a) and (b) are published; running them is a replay

Established in §0 and pinned by
`tests/test_arm_inventory.py::ProposalTests::test_a_bare_deepseek_arm_matches_every_compared_field_of_a_published_one`
and `…::test_a_native_proposal_also_already_stands_published`. A proposed BARE
arm at F001 occurrence-01's conditions is identical to the published one on
**every** compared field — `endpoint`, `kind`, `surface`, `max_tokens`,
`timeout_seconds`, `seed` — at a coordinate that already carries a terminal
artifact. The same holds for NATIVE.

### B2 — the permitted instrument cannot read any bare-shaped arm, ever

`graph_import_h005._Node.surface` is

```python
return "fcl1" if self.coord.arm in FCL_SURFACE_ARMS else "prose"
```

with `FCL_SURFACE_ARMS = ("mini_fcl",)`. **It is an exact arm-NAME membership
test.** Three consequences, each mechanical:

1. **Any arm not literally named `mini_fcl` is read as prose**, and the
   use-relation instrument extracts no references from prose. It lists the node
   under *"Nodes whose commitment surface was not read"* and emits **zero rows**.
   This is already visible in both published tables: H005 occurrence-01's
   `USE_TABLE.md` lists `daily/bare/cycle01/answer` and
   `daily/native/cycle01/answer` there, and F001 occurrence-01's does the same.
   Of five published arms, the instrument reads **one**.
2. **The name cannot be borrowed.** Declaring a baseline arm with
   `surface: "fcl"` is refused by the runner at plan time
   (`ARM_BASELINE_SURFACE`), and naming a non-Mini arm `mini_fcl` is the exact
   trap `docs/workflows/fork5-multifamily.md` already warns about — *"the study's
   first fact would vanish silently after the calls were spent."* Two independent
   locks, both deliberate.
3. **A one-call arm has nothing to tabulate.** The use-relation instrument rows
   are *cross-document references*. One call is one document. Even with an FCL-1
   surface it would emit zero rows, because there is no second document to refer
   to.

So the brief's item (5) — *read through the use-relation instrument only,
juxtaposed* — is **unsatisfiable for any bare-shaped arm**, by construction and
not by judgement. Spending calls on an arm the permitted instrument is
structurally unable to read would be spending them to produce a record nobody is
authorised to interpret.

### B3 — the confound in (a) → (c) is nameable but not removable here

Six differences move at once (§3). (d) removes one of them and is already
published. (e) removes another and cannot be read (B2). Even with both, the
carrier and the document-count differences remain, and at N = 1 per arm there is
no replicate baseline to separate any of it from run-to-run variation (§5). A
BARE arm dispatched under this register would add a seventh unread record to a
comparison that already has five.

### What is *not* refused

Nothing above says the comparison is uninformative. It says the comparison
**already exists in published bytes** and its obstacle is a reading instrument,
not a missing arm. Root can defeat Mini's rationale today, from the tree as it
stands, by reading `matched` against `mini_prose` at H005 occurrence-01 (§1 DX).

---

## 9. What B001 stages instead

1. **This register**, recording the premise failure with checkable evidence, and
   the claim, defeats, arm table and claim ceiling that a successor would inherit.
2. **`REASONING_PERSISTENCE.md`** — the one genuinely open question the brief
   raised: what the transport would need to change to make native reasoning
   legible, what that risks, and the digest-only alternative. Recommendation:
   **do not persist the text.**
3. **`tools/arm_inventory.py` + `tests/test_arm_inventory.py`** — 34 offline
   tests, no provider call, nothing written into the repository.
4. **Two promoted problems**, under `docs/PROBLEM_PROMOTION.md`'s discipline.
   Promotion selects a question; it endorses no diagnosis.

   * **B001-P1 — the reading gap.** *Trigger:* five published arms per
     occurrence, one readable. *Target:* the use-relation instrument's coverage,
     not any contribution's merit. *Relevance:* PURPOSE.md names bare-model and
     native-reasoning comparison as a programme question, and no instrument in
     this repository can place a one-call prose answer beside a five-call chain.
     *Successor question:* what juxtaposition, with the same "records, never
     reads" discipline and the same four empty root cells, would let root compare
     a prose single-document arm with an FCL-1 chain without minting a relation,
     a score or a label? *Preserved:* U1–U7, I7, and root's sole authority to
     read. *Unresolved:* whether such a juxtaposition can avoid smuggling in a
     similarity measure. That is the hard part and is not assumed solvable.
   * **B001-P2 — reasoning legibility.** *Trigger:* `reasoning_content_persisted`
     is a constant `False` at five points across two pinned files. *Target:* the
     transport's record contract. *Relevance:* the `native` arm is currently
     distinguishable from `bare` only by a wire flag and a token count.
     *Successor question:* see `REASONING_PERSISTENCE.md`. *Unresolved:* an owner
     decision about provider terms that no agent may make.

**No dispatch. No provider call. No edit to any published file.**
