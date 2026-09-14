# F001 — one fork5 invocation across six model families

> **Mechanism facts only. Root reads the content.** This study reports what the
> published instruments can *compute* about six occurrences of the same frozen
> material — parse outcomes, reference resolution, edges, labels, counts. It
> reports nothing about whether any criticism was good, whether any dependence
> was real, or whether any amendment repaired anything. No count here ranks a
> family, and invariant I7 of the importer holds throughout: no label it
> computes is a semantic attribution.

Read [the decision ledger](../DECISION_LEDGER.md), [STATUS](../STATUS.md), the
[experiment workflow](experiment.md) and the register itself —
[`experiments/diagnostics/F001-fork5-multifamily/PLAN.md`](../../experiments/diagnostics/F001-fork5-multifamily/PLAN.md)
— before running anything. Where this page is silent, the register governs;
where the register is silent, H005's `PROTOCOL.md` governs.

## What F001 is

One complete `fork5` invocation of the `daily` problem, cycle 1, on H005's
material verbatim (plus one `study_id` key), run once on each of six model
families. Six occurrences, **19 arms, 67 provider calls**:

| Occurrence | Endpoint | Key | Arms | Calls |
|---|---|---|---|---|
| occurrence-01 | `deepseek-flash` | `DEEPSEEK_API_KEY` | `bare`, `native`, `mini_fcl`, `mini_prose` | 12 |
| occurrence-02 | `ollama/gpt-oss-120b` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 11 |
| occurrence-03 | `ollama/qwen3.5-397b` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 11 |
| occurrence-04 | `ollama/glm-5.3` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 11 |
| occurrence-05 | `ollama/kimi-k3` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 11 |
| occurrence-06 | `ollama/gemma4-31b` | `OLLAMA_API_KEY` | `bare`, `mini_fcl`, `mini_prose` | 11 |

The family lives in the **occurrence**, never in the arm name: the published
importer decides whether to parse a commitment surface as FCL-1 by exact
membership, `graph_import_h005.FCL_SURFACE_ARMS == ("mini_fcl",)`, so an arm
called `mini_fcl@kimi-k3` would be read as prose and the study's first fact
would vanish silently after the calls were spent.

Three asymmetries are declared, not corrected, and any cross-occurrence reading
must carry them:

* **`native` is available on one family only.** DeepSeek carries a thinking
  control on the wire; the five Ollama families do not, and the runner refuses
  the arm at plan time with `ARM_NATIVE_WIRE_UNKNOWN` rather than guessing at
  dispatch. The comparison is marked unavailable there, not dropped.
* **`bare` is not the same control everywhere.** Reasoning-disabled direct
  baseline on occurrence-01; default direct baseline on 02–06, where reasoning
  cannot be switched off through this surface.
* **OPAQUE rates are not comparable with H005 occurrence-01.** The fork declares
  two decode repairs and no others — strip one outer Markdown fence, then
  re-parse with `strict=False` — before the same strict shape check. The
  comparable figure is `strict_parse_would_succeed`, recorded per node beside
  `envelope_repairs`. A fence is a formatting habit, not a reasoning failure.

## The command sequence

`S=experiments/diagnostics/F001-fork5-multifamily`, and every command runs with
`PYTHONPATH=src python -X utf8 tools/multicycle_commitment_study_multi.py`.

Once, per occurrence — zero provider calls:

```
... initialize --study $S --output $S/occurrence-0N
... verify     --study $S --output $S/occurrence-0N
```

then **commit and push** the six frozen `plan.json`/`preflight.json` pairs.

Then four rounds. Per round, in this order and no other:

```
# 1. prepare, per occurrence with ready coordinates -- zero calls
... prepare-wave --study $S --output $S/occurrence-0N --problem daily --cycle 1

# 2. ONE commit + push covering every prepared wave's required input paths

# 3. one process, all six occurrences, against that one published commit
... send-round --study $S --publish-ref origin/<branch> \
      --occurrences occurrence-01 occurrence-02 occurrence-03 \
                    occurrence-04 occurrence-05 occurrence-06

# 4. ONE commit + push of every new record, then read the audit signal
```

`send-wave`/`send-round` refuse unless HEAD equals the publication ref **and**
every path in the wave's transitive closure — plan, material, arms, manifests,
the runner, the runtime pins, the provider module, the endpoint registry, and
every request, trace, attempt, receipt, artifact, raw response text and provider
call record a dependency reaches — is byte-identical to the committed bytes.
That closure includes the *previous* round's receipts, so a round cannot be sent
until the previous round's results are published: **one push per round**, five
in all. A moved ref is `PUBLISH_REF_CHANGED`; one changed byte is
`INPUT_NOT_PUBLISHED`. Neither constructs a provider.

After round 4, per occurrence:

```
... audit --study $S --output $S/occurrence-0N
```

Expect `max_calls` = COMPLETE + PARTIAL, `unvisited` 0, `out_of_scope` 0.

## The per-key rule

**At most five concurrent requests per credential**, and **one coordinator
process**. Both halves matter.

Five is enforced in three places: `ready_coordinates` admits at most `key_cap`
per `key_env` when the wave is built; `send-wave` re-refuses an oversized wave
with `WAVE_SIZE_INVALID` before any attempt marker or provider object exists;
and a module-level gate keyed by `key_env` holds every in-flight call, acquired
**before** the attempt marker is written, so an attempt exists only for a call
this process is about to make. `provider_openai_compat.slots_for` is a fourth
ceiling around the socket itself.

Because that gate is process-wide, **one `send-round` may drive all six
occurrences**: the five Ollama occurrences share one gate of five on
`OLLAMA_API_KEY` while occurrence-01 overlaps them on `DEEPSEEK_API_KEY`. What
is not authorised is two coordinator *processes* on one credential — nothing in
this repository can hold a ceiling across processes.

Keys are read from the environment at call time only. Load them into the send
command's environment from a gitignored file; never write one into a tracked
file, a record, a log or a commit. The runner's `write_new` refuses any record
containing a credential (`CREDENTIAL_IN_OUTPUT`).

## No retries, and what one failure costs

`retries` is 0 at every layer: one `complete` is one request on the wire or
none, and an attempted coordinate with no terminal evidence is audited, never
re-sent. **One `FAILED` node ends that arm for the rest of the occurrence** —
the next `prepare-wave` simply returns fewer coordinates and refuses nothing.
The audit signal is `counts.FAILED` >= 1 together with `counts.unvisited` > 0
and that arm's `invocations` row reading `"complete": false`. Read it after
every round. Each `FAILED` receipt carries `failure_code` beside `failure_type`,
so `HTTP_429`, `KEY_MISSING` and `TRANSPORT_OR_RESPONSE_ERROR` are
distinguishable without opening the provider call records.

Scope is frozen in each `arms.json` as `{"problems": ["daily"], "cycles": [1]}`,
pinned by `arms_sha256` and enforced as `SCOPE_EXCLUDED`. There is no path from
this register to `physics`, `philosophy`, `sociology`, cycle 2 or cycle 3, or to
the `matched` arm. `plan["max_calls"]` counts only what the scope admits and
**is** the authorisation; `plan["max_calls_envelope"]` keeps the full material
figure visible beside it.

## The follow-up: importer, then use relation

The occurrences are evidence; the reading is separate. Per occurrence, offline
and against published bytes:

```
python -X utf8 tools/import_h005.py      $S/occurrence-0N <analysis>/occurrence-0N/import
python -X utf8 tools/use_relation_h005.py $S/occurrence-0N <analysis>/occurrence-0N/use-table
```

See [graph-import-h005](graph-import-h005.md) and
[use-relation-h005](use-relation-h005.md). Both open the occurrence read-only
and refuse a destination inside `experiments/diagnostics/`; outputs belong under
`experiments/analyses/`. The importer supplies the mechanism facts the register
names — FCL-1 parse/schema outcomes, `report.resolution`, cross-document
`depends`, warrants, `att` edges, ν-attacks, reinstatement, grounded labels —
and the use-relation table supplies the juxtaposition whose four interpretive
cells only root fills by reading. **No cross-family merit reading is made by
either instrument, and none may be read off their counts.**

## Design record

* Register and pre-registration: [`PLAN.md`](../../experiments/diagnostics/F001-fork5-multifamily/PLAN.md)
* Fork design notes and the offline proof: [`docs/design/multicycle-commitment-study-multi-notes-2026-09-14.md`](../design/multicycle-commitment-study-multi-notes-2026-09-14.md)
* Adversarial review closure: [`docs/sources/multicycle-commitment-study-multi-review-fixes.md`](../sources/multicycle-commitment-study-multi-review-fixes.md)
* Transport: [provider-openai-compat](provider-openai-compat.md)
* Suite: `PYTHONPATH=src python -X utf8 -m unittest tests.test_multicycle_commitment_study_multi`

## The v2 successor runner — a raised completion ceiling

Added 2026-09-14, for occurrences 07 and 08. Read the register's
[`Successor occurrences 07 and 08 under runner v2`](../../experiments/diagnostics/F001-fork5-multifamily/PLAN.md)
section before running anything under it.

**The published runner is never edited.** `tools/multicycle_commitment_study_multi.py`
pins its own sha256 into every plan it has written, as `runner_sha256` and
`helper_sha256`, both folded into `plan_id`; one changed byte invalidates every
published plan and every custody check that reads one. A runner change is
therefore a *successor file with its own identity*, never an edit:
`tools/multicycle_commitment_study_multi_v2.py`, a byte copy with a declared and
proven difference list.

v2's four differences, each marked `# V2:` in its source and listed in its
header: the provenance header; `CAP = 8192` split by role, so the bound
`validate_arms` enforces becomes `MAX_CEILING = 393216` (the provider's own
bound, mirrored from `provider_openai_compat`) while the default an undeclared
arm receives stays `DEFAULT_CEILING = 8192`; `manifest_for` deriving
`cycles.completion_tokens_per_call` and `cycles.max_completion_tokens` from the
occurrence's declared arm ceilings instead of the constant; and a docstring that
says v2. `tests/test_multicycle_commitment_study_multi_v2.py::V2DiffProofTests`
normalises the header away, diffs the two files and refuses any hunk that is not
on that list — so *the ceiling is the only behavioural difference between the two
runners*, and that is checked by the suite rather than promised by a comment.

The command sequence is the one above with the v2 file in place of the v1 file.
`S=experiments/diagnostics/F001-fork5-multifamily`, and every command runs with
`PYTHONPATH=src python -X utf8 tools/multicycle_commitment_study_multi_v2.py`:

```
... initialize   --study $S --output $S/occurrence-0N
... verify       --study $S --output $S/occurrence-0N
... prepare-wave --study $S --output $S/occurrence-0N --problem daily --cycle 1
... send-round   --study $S --publish-ref origin/<branch> \
      --occurrences occurrence-07 occurrence-08
... audit        --study $S --output $S/occurrence-0N
```

Everything else is unchanged and still binds: one commit and push per round
covering the whole transitive closure, `send-round` refusing unless HEAD equals
the publication ref and every required path is byte-identical to the committed
bytes, at most five concurrent requests per credential through one process-wide
gate, `retries` 0, one FAILED node ending its arm for the rest of the occurrence,
and the same offline follow-up with `tools/import_h005.py` and
`tools/use_relation_h005.py` into `experiments/analyses/`.

Two things that are easy to get wrong:

* **Declare the ceiling per arm.** A raised `MAX_CEILING` is only a bound. An arm
  that declares no `max_tokens` still gets 8,192 under v2, exactly as under v1 —
  by design, so that the successor changes nothing it was not asked to change.
  The ceiling reaches the wire because `arms.json` says `"max_tokens": 32768` on
  each arm, and `plan["ceilings"]` is where to read back what each arm actually
  got.
* **A raised ceiling is a budget, not a repair.** A node truncated at the new
  ceiling is still PARTIAL (and OPAQUE if its envelope will not parse), preserved
  and never relabelled; a node returning zero bytes is still FAILED with
  `INCOMPLETE_GENERATION` and still ends its arm. Occurrences at two ceilings are
  two occurrences, not a before and an after: the earlier records are never
  re-sent, superseded or corrected by the later ones.

Suite: `PYTHONPATH=src python -X utf8 -m unittest tests.test_multicycle_commitment_study_multi_v2`
(and the v1 suite must keep passing unchanged beside it).

## The v3 successor runner — a per-arm wall clock, and F002

**Appended 2026-09-14 (REC-20260914-X). Nothing above this line is altered.**
Read the v2 section first: everything it says about successor identities still
binds, and v3 is a successor to v2 exactly as v2 is a successor to v1.

**What the v2 runner could not express.** F001 occurrences 07 and 08 raised the
per-arm completion ceiling to 32,768 and were then refused by something else:
both of that run's two failures are `TRANSPORT_OR_RESPONSE_ERROR` — `"The read
operation timed out"` at 180,368 ms and 180,456 ms against the endpoint record's
180 seconds — on `occurrence-07 mini_fcl/objection` and `occurrence-08
mini_fcl/carry`, neither of them a ceiling truncation, each ending its arm and
leaving `mini_fcl/response` and `mini_fcl/carry` on 07 never dispatched. Four
`mini_fcl` coordinates on those two families were therefore unresolved for a
reason the ceiling cannot reach. v2's own header says why v2 could not answer it:
"the timeout is NOT [a per-arm declaration] — it is the endpoint record's and no
arm declaration can change it." `ARM_OPTIONAL` is `{declared_name, max_tokens,
seed}`, `validate_arms` refuses a `timeout_seconds` key as `ARM_FIELDS`, and the
only other way to move the clock is to edit `src/minireason/data/endpoints.json`
— a pinned published file that C001's two occurrences and all eight F001 plans
hash into their own identities, so editing it would invalidate them.

**v3's seven differences, in eight hunks**, each marked `# V3:` in the source and
listed in the file's own header: the module docstring; `replace` joining the
`dataclasses` import; `MAX_TIMEOUT = 600` mirrored from the transport, with
deliberately no default constant beside it because the default is the endpoint
record's own value; `ARM_OPTIONAL` gaining `timeout_seconds`; `validate_arms`
reading, bounding and freezing it, and writing the key into the frozen arm **only
where the declaration carries one**; `settings_for` taking the arm's clock or the
endpoint record's; the `plan_body` comment that v3 makes false, rewritten; and
`send_wave` applying the clock to the resolved `Endpoint` **value** by
`dataclasses.replace` and refusing `TIMEOUT_NOT_APPLIED` — before the per-key
gate, before the attempt marker and before any provider is constructed — if the
value the transport is about to receive is not the declared one.
`tests/test_multicycle_commitment_study_multi_v3.py` proves the list rather than
promising it: the diff proof normalises the docstring away and asserts the hunks
are exactly those eight **line for line, comments included** — strictly stronger
than v2's own proof, which excluded comments; a parity test shows that where no
arm declares a clock a v3 plan differs from a v2 plan in exactly `runner_sha256`,
`helper_sha256` and the `plan_id` they feed; and a dispatch test drives the
transport's own `OfflineProvider` and asserts the constructed endpoint carries
600, that it is not the registry object, that the registry row still reads 180,
and that `src/minireason/data/endpoints.json` has the same sha256 before and
after. **600 is not a chosen number**: `provider_openai_compat.Endpoint.__post_init__`
admits 1…600 and refuses 601, so it is the transport's own validation maximum,
reached rather than invented, exactly as C001 occurrence-02 reached it.

**Declare the clock per arm, in `arms.json`, beside the ceiling:**

```json
{"arms": {"mini_fcl": {"endpoint": "ollama/glm-5.3", "kind": "mini",
                       "surface": "fcl", "seed": 7,
                       "max_tokens": 32768, "timeout_seconds": 600}}}
```

An arm that declares no `timeout_seconds` is settled exactly as v2 settles it,
from the endpoint record. `plan["ceilings"]` is where to read back what each arm
actually got, and the frozen request's `settings` block carries the clock, so a
dispatch that did not apply it fails terminal custody rather than passing quietly.

**F002** (`experiments/diagnostics/F002-fork5-raised-clock/PLAN.md`) is the study
v3 exists for: two occurrences, `ollama/glm-5.3` and `ollama/kimi-k3`, **one arm
each** (`mini_fcl`, surface `fcl`, kind `mini`, seed 7), five fork5 nodes each,
scope `{"problems": ["daily"], "cycles": [1]}`, `max_tokens` 32,768 and
`timeout_seconds` 600, **ten calls and no more**, both single-key on
`OLLAMA_API_KEY` through one process-wide gate of five. The command sequence is
the v2 one with the v3 file in place of it and
`--occurrences occurrence-01 occurrence-02`:

```
S=experiments/diagnostics/F002-fork5-raised-clock
... initialize   --study $S --output $S/occurrence-0N
... verify       --study $S --output $S/occurrence-0N
... prepare-wave --study $S --output $S/occurrence-0N --problem daily --cycle 1
... send-round   --study $S --publish-ref origin/<branch> \
      --occurrences occurrence-01 occurrence-02
... audit        --study $S --output $S/occurrence-0N
```

Measured cadence, four rounds: `wave0001` `account`; `wave0002` `objection` +
`rival`; `wave0003` `response`; `wave0004` `carry` — **2 / 4 / 2 / 2** where no
arm truncates, fewer where one does.

**Three things that are easy to get wrong.**

* **The whole arm, not the unresolved nodes.** fork5 is a dependency graph:
  `objection` and `rival` read `account`'s artifact, `response` reads
  `objection`'s, `carry` reads the rest. A node cannot be re-asked without its
  inputs, and importing an earlier study's artifacts into a differently
  identified occurrence would put an artifact produced under one frozen plan
  inside another. The smallest honestly re-dispatchable unit is the arm chain
  from `account` down.
* **A longer clock is a budget, not a repair, and it is not predicted to be
  sufficient.** A call that reaches 600 s is a `TRANSPORT_OR_RESPONSE_ERROR`
  refusal recorded with its code, ending that arm, reported as any other outcome.
  A node that truncates at 32,768 is still PARTIAL, or FAILED at zero bytes.
* **Two occurrences at two clocks are two occurrences, not a before and an
  after.** F002 differs from F001's 07 and 08 in the wall clock *and* the runner
  identity, and from 04 and 05 in the ceiling *and* the clock *and* the runner, so
  any difference read across them is a **resource observation, never a semantic
  one**. Within F002 both occurrences share one ceiling and one clock, which is
  the comparison the study actually asks. No F001 record is re-sent, relabelled,
  repaired or superseded, and F002 writes nothing inside
  `F001-fork5-multifamily/`.

Suite: `PYTHONPATH=src python -X utf8 -m unittest tests.test_multicycle_commitment_study_multi_v3`
(and the v1 and v2 suites must keep passing unchanged beside it).

**What F002 actually did**, recorded here because a workflow page that only
describes the intent is half a page. Nine calls spent of ten authorised, in four
rounds of 2 / 4 / 2 / 1: **8 COMPLETE, 1 FAILED, 1 never dispatched**. Neither
declared bound was reached — `finish_reason: "length"` occurs **zero** times, the
largest completion is 23,257 tokens of 32,768, and the longest call that returned
is 223,839 ms of 600,000. **Three calls ran past 180 seconds and returned**
(223,839 ms, 188,623 ms, 196,250 ms), two of them the exact coordinates
occurrences 07 and 08 lost at 180,368 ms and 180,456 ms. **One call FAILED and
not on the clock**: occurrence-01 `mini_fcl/response` ended at 300,270 ms with
`"Remote end closed connection without response"` against an applied 600-second
clock — a third resource wall, neither the ceiling nor the read timeout — and the
truncation rule then removed that occurrence's `carry`. So **two of the four
coordinates F002 was built to reach now have a terminal COMPLETE record and two
do not**, which is the outcome and not a shortfall to be reported as something
else. The counts, the custody table and the two instruments' output are in
`experiments/analyses/F002-fork5-raised-clock-2026-09-14/README.md`; the decision
and its per-coordinate table are REC-20260914-X.

A fourth lesson for the next raise, from that one failure: **a bound you declare
is not the only bound you will meet.** F001 met the ceiling, then the read
timeout, then F002 met an upstream connection close at about five minutes on
`ollama/glm-5.3`. Raising a declared bound tells you nothing about the undeclared
ones, so read the `error` string of every `TRANSPORT_OR_RESPONSE_ERROR` before
calling it a timeout: `"The read operation timed out"` at the clock value is the
client's deadline, and anything else is not.

## Occurrence-03, and a bound nobody declared — appended 2026-09-14 (REC-20260914-Z)

**Nothing above this line is altered.** The section above closes with a lesson
from F002's one failure — *a bound you declare is not the only bound you will
meet* — and tells you to read the `error` string of every
`TRANSPORT_OR_RESPONSE_ERROR` before calling it a timeout. Occurrence-03 was
dispatched to test the obvious next question about that failure, and the answer
changes how the page's own advice should be used.

**The question.** F002 occurrence-01 `mini_fcl/response` ended with
`"Remote end closed connection without response"` at **300,270 ms** against an
applied 600-second clock. One record is one record. **Does it recur?**

**The method.** A third occurrence of the same study: the same `mini_fcl` arm
chain re-run from `account` on `ollama/glm-5.3` at 32,768 / 600 s, seed 7,
`arms.json` byte-identical to occurrence-01's, dispatched alone so that at most
two requests were ever in flight on the shared credential. Five calls
authorised.

**Read this before copying the pattern: a re-run of an identical `arms.json`
does not get a new `plan_id`.** `plan_body` digests the material, the frozen arms
and scope, the runtime and provider pins and the runner, and **no occurrence
name**, so occurrence-03 minted occurrence-01's own
`9aa92a837569bd56a86b172eb56dd80dbc69c519a86286d3387b020c2709a0d5`; its
`plan.json`, `material.json` and all three manifests are byte-identical, and so
is `wave0001`'s `account` request hash. There is no plan-level replay refusal to
work around — `NO_REPLAY` is per coordinate inside one occurrence directory, and
`OCCURRENCE_EXISTS` only guards a non-empty output directory — so **nothing
forces the seed to differ, and changing it to manufacture a distinct `plan_id`
would change the condition you are trying to observe.** An occurrence has its own
identity through its directory, waves, attempt markers, provider bytes and
receipts; sharing a plan identity is what "the same question, asked again" means.
Say so in the receipt before the run, not after it.

**The result: it recurs.** Two rounds, not four. `account` COMPLETE at 114,364 ms;
`rival` COMPLETE at **234,864 ms**, past the 180-second endpoint wall;
**`objection` FAILED** at **300,453 ms** with the same error string, no
`finish_reason`, no usage, no content, against `settings.timeout_seconds` 600.
The truncation rule then ended the arm and `response` and `carry` were never
dispatched — **3 of 5 authorised calls spent**.

**The bound, as precisely as the records state it.** Five closes carrying that
exact string are known, inside a **183-millisecond band around 300.3 s**:
300.270 s and 300.453 s on `ollama/glm-5.3` (F002 occurrences 01 and 03, 63
minutes apart, at *different* nodes) and 300.286 / 300.348 / 300.377 s on
`ollama/kimi-k3` from a separate worker process at 600 s and 32,768 (transcripts
cited with their provenance and their limits in REC-20260914-Z — another
harness's schema, **not** `minireason.call.v2` records). Two model families, two
client processes, two different fork5 nodes. **A host gateway closes a request
still open at about 300 seconds, and a declared 600-second clock cannot be
exercised past 300 s on this host.**

**What this means for the v3 runner and for the next raise.**

* **`timeout_seconds: 600` is still correct to declare and is still not the
  binding constraint.** The runner applies it, the provider record proves it, and
  `TIMEOUT_NOT_APPLIED` still guards it. What 600 buys you here is the right to
  wait; the host does not grant it.
* **Budget against 300 s, not 600.** F002's own arithmetic — 77.9–151.0
  completion tokens per second, a full 32,768 taking 217–421 s — describes calls
  this host will close before the slower half of them can finish. A ceiling you
  cannot spend inside the gateway's window is not a ceiling you have.
* **Read the error string, and now also read the elapsed value against 300 s.**
  `"The read operation timed out"` at the clock value is the client's deadline;
  `"Remote end closed connection without response"` at ~300 s is this wall; they
  are different facts and neither is the other.
* **Do not retry it.** There is no retry at any layer in this harness and none
  was made. A close is a resource fact; re-sending a coordinate inside its own
  occurrence is refused as `NO_REPLAY`, and re-sending it as a new occurrence is a
  new decision that needs its own receipt and its own reason.
* **Nothing semantic follows.** `ollama/glm-5.3` is not less reliable than
  `ollama/kimi-k3`, or the reverse, because of where a socket closed; two closes
  on one and three on another rank nothing. **A closed socket is never a verdict.**

**What is still open.** F001 occurrence-07's `mini_fcl/response` and
`mini_fcl/carry` have **no terminal COMPLETE record anywhere**: three occurrences
have now ended that arm early, for three different reasons at three different
nodes. Why the gateway closes at ~300 s — fixed policy or not, provider or
intermediary, payload- or load-dependent — is **not known and is not guessed at**
here. The counts, the custody table and both instruments' output for
occurrence-03 are in
`experiments/analyses/F002-fork5-raised-clock-2026-09-14/README.md`; the decision
and its per-coordinate table are REC-20260914-Z.
