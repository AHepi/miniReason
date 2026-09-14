# F002 — the F001 `mini_fcl` cells the wall clock refused, re-asked at 600 s

**No label produced by these imports is a semantic attribution.** Statuses are
mechanism bookkeeping over the imported attack relation; they do not bear on the
FCL-1 hypothesis, on FW5, or on the merit of any contribution. Root alone
interprets substantive output (H005 `PROTOCOL.md` §Interpretation). Both use
tables leave all four interpretive columns — `root_reading`,
`root_passage_cited`, `root_notes`, `root_initials_date` — empty in every row; a
blank cell is an unread row, not a reading of `unresolved`.

**No cross-family merit reading is made here, and none may be read off these
counts.** A family whose FCL-1 documents parse is not thereby correct, and a
family whose documents do not parse has not thereby failed to reason. Parser
success, more objections, longer documents, more refs, more ν nodes and a larger
graph are not repair. A `refuted` label is bookkeeping over the attack relation
the authors themselves declared. Transport status is never a verdict: a `FAILED`
coordinate and a ceiling truncation are resource facts.

**Any difference between these two occurrences and any F001 occurrence is a
resource observation, never a semantic one.** F002 differs from F001's
occurrences 07 and 08 in the wall clock *and* the runner identity, and from 04
and 05 in the ceiling *and* the clock *and* the runner. More tokens and more
seconds buy the model more room; they do not ask it to reason differently.
Within F002 both occurrences share one ceiling and one clock, so the
family-to-family comparison this study actually asks is unaffected.
**No F001 record is modified, relabelled, repaired, re-sent or superseded**, and
nothing here is written inside `F001-fork5-multifamily/`.

## What this directory is

The output of the two published instruments over the two F002 occurrences, at
**full scope** (no `--problem`/`--arm`/`--cycle` selector), plus each
occurrence's runner audit. Per occurrence:

```
occurrence-0N/import/      python -X utf8 tools/import_h005.py \
                             experiments/diagnostics/F002-fork5-raised-clock/occurrence-0N \
                             experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-0N/import
occurrence-0N/use-table/   python -X utf8 tools/use_relation_h005.py \
                             experiments/diagnostics/F002-fork5-raised-clock/occurrence-0N \
                             experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-0N/use-table
occurrence-0N/audit.json   PYTHONPATH=src python -X utf8 tools/multicycle_commitment_study_multi_v3.py audit \
                             --study experiments/diagnostics/F002-fork5-raised-clock \
                             --output experiments/diagnostics/F002-fork5-raised-clock/occurrence-0N
```

Register: `experiments/diagnostics/F002-fork5-raised-clock/PLAN.md`.
Workflow: `docs/workflows/fork5-multifamily.md` § *The v3 successor runner*.
Receipt: REC-20260914-X.

Material: F001's material with one `study_id` value changed and nothing else,
sha256 `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679`, the
same bytes in both occurrences. Runner:
`tools/multicycle_commitment_study_multi_v3.py`, sha256
`ccbb1165fd3bb1d14e6c9247821e9c4e67fbea09a2153339984bd7eaff5cc42e`, written into
both plans as `runner_sha256` and `helper_sha256`, so no F002 plan can collide
with a v1 or v2 plan.

| Occurrence | Endpoint | `plan_id` |
|---|---|---|
| occurrence-01 | `ollama/glm-5.3` | `9aa92a837569bd56a86b172eb56dd80dbc69c519a86286d3387b020c2709a0d5` |
| occurrence-02 | `ollama/kimi-k3` | `a59debaf6382ce7c01c4c07d14894890736e2a960b66d4323f9eb84ac72b1163` |

Both at `max_tokens` 32,768, `timeout_seconds` **600**, `seed` 7, `retries` 0,
scope `{"problems": ["daily"], "cycles": [1]}`, one arm `mini_fcl`, five fork5
nodes each, `max_calls` 5 each.

## MECHANISM-FACTS — counts only

### Every coordinate, as the records carry it

| occ | endpoint | node | status | `failure_code` | `finish_reason` | completion tokens | content bytes | `elapsed_ms` |
|---|---|---|---|---|---|---|---|---|
| 01 | `ollama/glm-5.3` | account | COMPLETE | — | stop | 17,317 | 11,349 | 150,813 |
| 01 | `ollama/glm-5.3` | objection | COMPLETE | — | stop | 23,257 | 20,342 | **223,839** |
| 01 | `ollama/glm-5.3` | rival | COMPLETE | — | stop | 9,040 | 9,269 | 90,719 |
| 01 | `ollama/glm-5.3` | response | **FAILED** | TRANSPORT_OR_RESPONSE_ERROR | — | — | 0 | **300,270** |
| 01 | `ollama/glm-5.3` | carry | — (no attempt) | — | — | — | — | — |
| 02 | `ollama/kimi-k3` | account | COMPLETE | — | stop | 4,772 | 6,426 | 54,187 |
| 02 | `ollama/kimi-k3` | objection | COMPLETE | — | stop | 10,757 | 11,619 | 133,968 |
| 02 | `ollama/kimi-k3` | rival | COMPLETE | — | stop | 5,315 | 6,011 | 69,743 |
| 02 | `ollama/kimi-k3` | response | COMPLETE | — | stop | 17,040 | 15,804 | **188,623** |
| 02 | `ollama/kimi-k3` | carry | COMPLETE | — | stop | 16,843 | 11,762 | **196,250** |

`reasoning_content_present` is **true on every one of the eight COMPLETE
records**; it is null on the FAILED one, which has no usage at all. No
`reasoning_tokens` field is present in any usage block on either endpoint.

**Nine calls spent of ten authorised.** The tenth is occurrence-01
`mini_fcl/carry`, removed from the queue by the no-retry truncation rule after
that arm's `response` failed: no attempt marker, no request, no provider record,
no receipt. It was never dispatched and is not a failure of anything.

### Transport and decode (from `audit.json`)

| | 01 `ollama/glm-5.3` | 02 `ollama/kimi-k3` |
|---|---|---|
| authorised calls (`max_calls`) | 5 | 5 |
| spent | 4 | 5 |
| COMPLETE | 3 | 5 |
| PARTIAL | 0 | 0 |
| FAILED | 1 | 0 |
| OPAQUE | 0 | 0 |
| unvisited (arm ended) | 1 | 0 |
| unresolved attempts | 0 | 0 |
| out of scope | 0 | 0 |
| invocation `complete` | false | **true** |
| `fence_stripped` | 2 | 5 |
| `lenient_control_chars` | 0 | 0 |
| `strict_parse_would_succeed` | 1 / 3 | 0 / 5 |
| `reasoning_content_present` | 3 | 5 |
| known completion tokens | 49,614 | 54,727 |
| known total tokens | 54,861 | 72,728 |
| calls with unknown usage | 1 | 0 |

### The two bounds this study declared

| | value | reached | largest observed | headroom |
|---|---|---|---|---|
| `timeout_seconds` | 600 | **no** | 300,270 ms (the FAILED call); 223,839 ms among calls that returned | 50.0 % / 62.7 % unused |
| `max_tokens` | 32,768 | **no** | 23,257 completion tokens | 29.0 % unused |

**`finish_reason: "length"` occurs zero times across all nine spent calls, and
no node reached either bound.** Nothing in F002 is ceiling-caused, and **no call
was refused by the 600-second clock**.

**Three calls ran past the 180-second wall the endpoint record declares** and
would have been `TRANSPORT_OR_RESPONSE_ERROR` refusals under it: occurrence-01
`objection` (223,839 ms), occurrence-02 `response` (188,623 ms) and
occurrence-02 `carry` (196,250 ms). A fourth call, occurrence-01 `response`,
also ran past it and then failed for a different reason — see below.

### The one FAILED coordinate, stated exactly

occurrence-01 `mini_fcl/response`: `failure_code` `TRANSPORT_OR_RESPONSE_ERROR`,
error **`"Remote end closed connection without response"`**, at **300,270 ms**
against a declared and applied `settings.timeout_seconds` of **600**. No
`finish_reason`, no `usage`, zero bytes of content. **This is not the 600-second
clock**: the clock was not reached, and the timed-out calls this study exists to
displace carry `"The read operation timed out"` at their own clock value, which
this record does not. It is a third resource wall, distinct from the
8,192-token ceiling of F001's occurrences 04 and 05 and from the 180-second read
timeout of its occurrences 07 and 08. Why the remote closed is **not known and
is not guessed at**: nothing here says whether it is characteristic of the
endpoint, the hour, the payload size or the request, and **no retry was made at
any layer**. It ended `mini_fcl` on occurrence-01 for the rest of the occurrence.

### FCL-1 commitment surface, `mini_fcl` arm (from `import/report.json`)

| | 01 | 02 |
|---|---|---|
| `mini_fcl` nodes reaching the importer | 3 | 5 |
| `read_fcl1` | **3** | **5** |
| `parse_failure` | 0 | 0 |
| `schema_failure` | 0 | 0 |
| `unavailable_decode_failure` | 0 | 0 |
| `opaque_envelope` | 0 | 0 |

### Graph facts (from `import/report.json`)

| | 01 | 02 |
|---|---|---|
| events | 27 | 41 |
| artifacts labelled | 6 | 10 |
| refs seen | 79 | 216 |
| refs resolved | 51 | 63 |
| refs dangling | 28 | 153 |
| ref extensions | 0 | 0 |
| refs to task artifact | 1 | 0 |
| `depends_cross_document` | 0 | 0 |
| `depends_intra_document` | 18 | 14 |
| warrants | 0 | 0 |
| `att` edges | 0 | 0 |
| `dep` edges | 0 | 0 |
| ν artifacts (`validity_node_minted_unasserted`) | 0 | 0 |
| ν nodes appearing in `att` (ν-attacks) | 0 | 0 |
| `criticism_of_criticism_retargeted` | 0 | 0 |
| reinstatements | 0 | 0 |
| labels — `accepted` | 6 | 10 |
| labels — `refuted` | 0 | 0 |
| use-table rows | **0** | **0** |

Error-severity residue, as the importer prints it above its own label table:
occurrence-01 `ref_unresolved` 28; occurrence-02 `ref_unresolved` 153. Read the
residue before reading any label. Every `accepted` here is
**accept-by-position**: there are no `att` edges on either occurrence, so no
artifact is attacked and no `refuted` label can arise. Both use tables have 0
rows because every authored reference resolved intra-document or not at all —
`cross_document_rows` is 0 on both, with `intra_document` 50 and 63 — and the
instrument walks cross-document references and nothing else.

### Custody

Both imports exit 0. Every cross-file and self-consistency check is
**verified — 18 of 18 on each occurrence**: material pin, manifest pins, receipt
presence, artifact bytes against receipt, status against receipt, public text,
attempt against receipt, request record, trace pinning, provider bytes and wave
placement. The single skip pattern is the usual one: `projection_source` skips
the structurally absent `previous`/`origin` slots of the first invocation, 1 of
3 on occurrence-01 and 2 of 10 on occurrence-02. `event_ts_nondecreasing` is
`no` on both, the importer's own **declared deviation** for concurrently run
waves and not a fault. Both audits report `max_calls` against
COMPLETE + PARTIAL + FAILED + unvisited exactly (3 + 0 + 1 + 1 and 5 + 0 + 0 + 0,
both 5), with `out_of_scope` 0 and `unresolved_attempts` 0.

## The four coordinates F002 was built to reach

F001's residue of 15 fell into three classes; the two the wall clock took, and
the two the truncation rule then removed behind one of them, are these four:

| F001 coordinate | F001 outcome | F002 coordinate | F002 outcome |
|---|---|---|---|
| 07 `ollama/glm-5.3` `mini_fcl/objection` | FAILED, `"The read operation timed out"`, 180,368 ms | 01 `objection` | **COMPLETE**, stop, 23,257 tokens, 223,839 ms |
| 07 `ollama/glm-5.3` `mini_fcl/response` | never dispatched (arm truncated) | 01 `response` | **FAILED**, remote closed the connection, 300,270 ms |
| 07 `ollama/glm-5.3` `mini_fcl/carry` | never dispatched (arm truncated) | 01 `carry` | **never dispatched** (arm truncated again) |
| 08 `ollama/kimi-k3` `mini_fcl/carry` | FAILED, `"The read operation timed out"`, 180,456 ms | 02 `carry` | **COMPLETE**, stop, 16,843 tokens, 196,250 ms |

**Two of the four now have a terminal COMPLETE record; two do not.** F002 does
not close its own residue, and says so rather than reporting the shortfall as
anything else.

## What a reader may and may not take from this

**May**: that these counts are what the published instruments could compute over
two occurrences of one `fork5` invocation of the `daily` problem, cycle 1, at
`max_tokens` 32,768, `timeout_seconds` 600 and `seed` 7, on 2026-09-14; that
three calls ran past 180 seconds and returned; that no call reached 600 seconds
or 32,768 tokens; and that one call ended when the remote closed the connection
at about five minutes.

**May not**: that either family reasons better, worse, or differently at the
longer clock; that a longer clock improves, repairs or degrades anything; that
more seconds, more tokens, more refs, more events or a parsed FCL-1 document is a
better contribution; that `ollama/glm-5.3` is less reliable than `ollama/kimi-k3`
because one of its calls met a connection close — **one call is one call**; or
that any F001 record is corrected by these. A clock is a transport budget.
Reasoning was not manipulated on either family — no thinking control is available
on this surface and none was set — and `reasoning_content_present` is 3 of 3 and
5 of 5 here. Two occurrences of one arm are two observations, not a sample.
**Root alone reads the content**, and no count here is a substitute for reading
the artifacts.

## Occurrence-03 — appended 2026-09-14 (REC-20260914-Z)

**Nothing above this line is altered.** Occurrence-03 is a third occurrence of
the same study, added after occurrences 01 and 02 were published and audited. It
re-asks the **same `mini_fcl` arm chain from `account`** on `ollama/glm-5.3` at
`max_tokens` 32,768, `timeout_seconds` 600 and `seed` 7, to observe **whether the
300-second connection close that ended occurrence-01's `response` node recurs**.
No record of occurrence-01 or occurrence-02 is modified, relabelled, repaired,
re-sent or superseded by it, and nothing is written inside
`F001-fork5-multifamily/`.

Its `arms.json` is byte-identical to occurrence-01's, so the runner mints **the
same content-addressed `plan_id`**
`9aa92a837569bd56a86b172eb56dd80dbc69c519a86286d3387b020c2709a0d5`: `plan_id` is
a digest over the material, the frozen arms and scope, the runtime and provider
pins and the runner, and carries no occurrence name. Occurrence-03 has its own
occurrence identity — its own waves, attempt markers, provider bytes and receipts
— and shares occurrence-01's **plan** identity by construction. `plan.json`,
`material.json` and all three manifests are byte-identical to occurrence-01's,
and so is `wave0001`'s `account` request hash `679a6146…`; the answers are not.

### Every coordinate, as the records carry it

| occ | endpoint | node | status | `failure_code` | `finish_reason` | completion tokens | content bytes | `elapsed_ms` |
|---|---|---|---|---|---|---|---|---|
| 03 | `ollama/glm-5.3` | account | COMPLETE | — | stop | 12,489 | 10,454 | 114,364 |
| 03 | `ollama/glm-5.3` | objection | **FAILED** | TRANSPORT_OR_RESPONSE_ERROR | — | — | 0 | **300,453** |
| 03 | `ollama/glm-5.3` | rival | COMPLETE | — | stop | 19,700 | 13,567 | **234,864** |
| 03 | `ollama/glm-5.3` | response | — (no attempt) | — | — | — | — | — |
| 03 | `ollama/glm-5.3` | carry | — (no attempt) | — | — | — | — | — |

`reasoning_content_present` is true on both COMPLETE records and null on the
FAILED one, which has no usage at all. No `reasoning_tokens` field is present in
any usage block. **Three calls spent of five authorised.** The other two are
`response` and `carry`, removed from the queue by the no-retry truncation rule
after `objection` failed: no attempt marker, no request, no provider record, no
receipt. They were never dispatched and are not failures of anything.

### Transport and decode (from `occurrence-03/audit.json`)

| | 03 `ollama/glm-5.3` |
|---|---|
| authorised calls (`max_calls`) | 5 |
| spent | 3 |
| COMPLETE | 2 |
| PARTIAL | 0 |
| FAILED | 1 |
| OPAQUE | 0 |
| unvisited (arm ended) | 2 |
| unresolved attempts | 0 |
| out of scope | 0 |
| invocation `complete` | false |
| `fence_stripped` | 2 |
| `lenient_control_chars` | 0 |
| `strict_parse_would_succeed` | 0 / 2 |
| `reasoning_content_present` | 2 |
| known completion tokens | 32,189 |
| known total tokens | 34,333 |
| calls with unknown usage | 1 |

### The two declared bounds, and the undeclared one

| | value | reached | largest observed | headroom |
|---|---|---|---|---|
| `timeout_seconds` | 600 | **no** | 300,453 ms (the FAILED call); 234,864 ms among calls that returned | 49.9 % / 60.9 % unused |
| `max_tokens` | 32,768 | **no** | 19,700 completion tokens | 39.9 % unused |
| host gateway close | ~300 s (**undeclared**) | **yes** | 300,453 ms | 0.2 % over |

**`finish_reason: "length"` occurs zero times across all three spent calls**, so
nothing here is ceiling-caused, and **no call was refused by the 600-second
clock**. One call ran past the 180-second wall the endpoint record declares and
returned: `rival` at 234,864 ms.

### The one FAILED coordinate — the close recurred

occurrence-03 `mini_fcl/objection`: `failure_code` `TRANSPORT_OR_RESPONSE_ERROR`,
error **`"Remote end closed connection without response"`**, at **300,453 ms**
against a declared and applied `settings.timeout_seconds` of **600**. No
`finish_reason`, no `usage`, zero bytes of content. Occurrence-01's README entry
above says of the same error that "why the remote closed is not known and is not
guessed at"; that stands, and what **is** now known is only that it recurs. Five
closes carrying that exact string are known to this publisher, all inside a
**183-millisecond band** around 300.3 s: **300.270 s** (occurrence-01 `response`,
`ollama/glm-5.3`, 10:20 UTC), **300.286 / 300.348 / 300.377 s** (three requests
of a separate worker process on `ollama/kimi-k3` at 11:07 UTC, transcripts cited
in REC-20260914-Z — untracked scratchpad files in another harness's schema, **not
`minireason.call.v2` records and not observations of this study**) and
**300.453 s** (occurrence-03 `objection`, `ollama/glm-5.3`, 11:23 UTC). Across
**two model families, two client processes and two different fork5 nodes**, so it
follows neither a node, nor a position in the chain, nor one endpoint. The
reading this supports and no more: **a host gateway closes a request still open
at about 300 seconds, and F002's declared 600-second clock cannot be exercised
past 300 s on this host.** Why it closes is still not known and is not guessed
at; whether 300 s is fixed policy, whether the closing party is the provider or
something between, and whether payload, model, concurrency or credential load
bear on it are all unanswered here. **No retry was made at any layer.**

### FCL-1 commitment surface, `mini_fcl` arm (from `occurrence-03/import/report.json`)

| | 03 |
|---|---|
| `mini_fcl` nodes reaching the importer | 2 |
| `read_fcl1` | **2** |
| `parse_failure` | 0 |
| `schema_failure` | 0 |
| `unavailable_decode_failure` | 0 |
| `opaque_envelope` | 0 |

### Graph facts (from `occurrence-03/import/report.json`)

| | 03 |
|---|---|
| events | 26 |
| artifacts labelled | 4 |
| refs seen | 52 |
| refs resolved | **52** |
| refs dangling | **0** |
| ref extensions | 0 |
| refs to task artifact | 4 |
| `depends_cross_document` | 0 |
| `depends_intra_document` | 15 |
| warrants | 0 |
| `att` edges | 0 |
| `dep` edges | 0 |
| ν artifacts (`validity_node_minted_unasserted`) | 0 |
| ν nodes appearing in `att` (ν-attacks) | 0 |
| `criticism_of_criticism_retargeted` | 0 |
| reinstatements | 0 |
| labels — `accepted` | 4 |
| labels — `refuted` | 0 |
| use-table rows | **0** |

**No error-severity residue fired at all on this occurrence** — the importer's
`error_severity_residue` is empty, where occurrence-01's carries
`ref_unresolved` 28 and occurrence-02's 153. That is a difference in what these
two documents happened to reference, not a merit difference between runs, and
nothing may be read off it about either. Every `accepted` here is
**accept-by-position**: there are no `att` edges, so no artifact is attacked and
no `refuted` label can arise. The use table has 0 rows because
`cross_document_rows` is 0 — all 52 references resolved, 48 intra-document and 4
to the exposed task artifact, none unresolved — and the instrument walks
cross-document references and nothing else.

### Custody

The import exits 0 and every cross-file and self-consistency check is
**verified — 18 of 18**, with `event_ts_nondecreasing` true. The single skip is
the usual structural one: `projection_source` runs 1 of 2, the other projection
having no exposed source because the slot is absent on the first invocation
(`daily/mini_fcl/cycle01/account#p.account.0`). The use table exits 0 with no
node left unread and no unresolved reference.

### What occurrence-03 did and did not settle

**Did**: it re-asked the chain and the close recurred, at a different node, on a
different request, 63 minutes later — so the 300-second close is **reproducible
and not a one-off**, which is the whole of what this occurrence was added to
observe.

**Did not**: it does not close F001 occurrence-07's two residual coordinates.
`mini_fcl/response` and `mini_fcl/carry` still have **no terminal COMPLETE record
anywhere** — F001's 07 never dispatched them, F002's 01 lost `response` to the
close and never dispatched `carry`, and F002's 03 lost `objection` to the close
and never dispatched either. Three occurrences have now ended that arm early, and
this directory reports that rather than a shortfall dressed as anything else.

**May not be read from any of it**: that `ollama/glm-5.3` reasons worse, better
or differently; that a longer clock repairs or degrades anything; that two closes
on one endpoint and three on another rank the endpoints; or that any F001 or
F002 record is corrected by these. **A closed socket is a resource fact and never
a verdict.** Root alone reads the content.
