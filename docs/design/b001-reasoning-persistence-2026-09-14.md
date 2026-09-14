# B001 — persisting native reasoning: what it would take, what it risks, what to do instead

**Recommendation: do not persist the reasoning text. Persist a digest of it and
its character count; the token count needs no change at all, because it is
already published and has never been read.**

This document answers item (3b) of B001's brief. It changes nothing. It names
exactly which bytes would have to move, which published identities each move
invalidates, and what the alternative buys.

---

## 1. What the record says today

PURPOSE.md asks whether Mini adds anything "compared with a bare model **and the
same model's native reasoning**". The `native` arm exists and is published. What
the record preserves of its reasoning is this, and only this:

| field | F001 occ-01 `native` | H005 occ-01 `native` |
|---|---|---|
| `request.thinking` | `{"type": "enabled"}` | `{"type": "enabled"}` |
| `request.reasoning_effort` | `"low"` | `"low"` |
| `reasoning_content_present` | `true` | `true` |
| `reasoning_content_persisted` | `false` | `false` |
| `usage.completion_tokens_details.reasoning_tokens` | **2979** | **886** |
| `usage.completion_tokens` | 3701 | 1552 |
| `provider_response_bytes` | 18368 | — |
| `provider_response_sha256` | `be1509f2…` | present |

So the `native` arm is distinguishable from the `bare` arm by **a wire flag and a
token count**. What the model actually reasoned is gone. That is the gap, and it
is real.

Two things in that table are worth separating, because they are usually
conflated:

* **`reasoning_tokens` is already persisted.** DeepSeek returns it inside
  `usage`, the transport records `usage` verbatim, and both published `native`
  calls carry it. **No change of any kind is needed for the token half of "a
  digest plus token counts".** It is in the tree now. It has never been read.
* **`provider_response_sha256` is not a digest of the reasoning.** It covers the
  whole chat body, including `id`, `created` and `system_fingerprint`, which vary
  per call. Two calls that reasoned identically would still hash differently, so
  it cannot answer "did these two calls reason the same way?".

---

## 2. Where the text is discarded — five points, two pinned files

`src/minireason/provider_openai_compat.py`, sha256
`cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db`:

1. **`_normalise_openai`** binds `reasoning = message.get("reasoning_content") or
   message.get("reasoning")` and returns `reasoning_present=bool(reasoning)`. The
   text is never bound to a name that outlives the function.
2. **`_normalise_native`** does the same with `message.get("thinking") or
   message.get("reasoning")` for Ollama's `POST /api/chat`.
3. **`_finish`** writes `reasoning_content_persisted=False` into the record as a
   literal, beside `reasoning_content_present`.
4. **`CallResult.reasoning_content_persisted`** is a dataclass field defaulting to
   `False`, with the comment *"a constant so that a record, a result and the
   documentation cannot drift"*.
5. **`_settings_view`** writes `"native_reasoning_text_persisted": False` into
   every record's `settings` block.

Beside those, the raw chat body is never written at all — only
`provider_response_sha256` and `provider_response_bytes`. The single documented
exception is `list_models`, "because a model list carries no reasoning text".

`tools/multicycle_commitment_study_multi_v3.py`, sha256
`ccbb1165fd3bb1d14e6c9247821e9c4e67fbea09a2153339984bd7eaff5cc42e`, adds a sixth
point downstream:

6. **`decode_contribution`** raises `PROVIDER_CONTENT_CUSTODY` when
   `record.get('reasoning_content_persisted')` is truthy. F001's declared
   difference (i) and F002's PLAN both restate it as *"a hard refusal"*.

**Neither file may be edited.** The transport's digest is pinned in C001's
`material.json.transport_pins` and in every F001 and F002 plan's `provider_pins`;
the runner writes its own digest as `runner_sha256`/`helper_sha256` into every
plan it has built, folded into `plan_id`. One changed byte invalidates every
published plan that pins it and every custody check that reads one. Any change is
therefore a **successor file with its own identity**, exactly as v1 → v2 → v3 was
done for the runner and v1 → v2 for the contrast driver.

---

## 3. Option A — persist the reasoning text

### The change

A successor transport `src/minireason/provider_openai_compat_v2.py`: a byte copy
of `cdc4b57…` with a `# V2:` mark per hunk and a declared difference list —
`_Normalised` carries the text; `_normalise_openai` and `_normalise_native` pass
it through; `_finish` redacts it and writes it beside a
`reasoning_content_persisted` that is now a **computed** field rather than a
constant; `_settings_view`'s `native_reasoning_text_persisted` becomes the
declaration the caller made. Plus a successor runner `…_v4.py` whose
`decode_contribution` admits a persisted-reasoning record **only** for arms that
declared persistence, and refuses it everywhere else — otherwise the refusal that
protects every other arm is simply deleted.

### The receipt it would need

A ledger receipt in house style stating, before any call: the choice and why;
the two new file identities and their sha256s; that the published transport and
runner are **not** edited, so every existing plan's `provider_pins`,
`runner_sha256` and `plan_id` remain valid and no published occurrence gains the
field retroactively; the **owner's decision on provider terms**, quoted, because
an agent cannot make it; the size ceiling adopted and what happens at it; the new
refusal that keeps persisted reasoning out of any later call's inputs; the
credential-scan extension over the new field; and the diff-proof test result
showing the successor differs from its parent only on the declared hunks. Plus a
new row in `THIRD_PARTY_NOTICES.md`, because the repository would begin
redistributing provider-generated content it has never redistributed before.

### What it makes available

The only thing that would make PURPOSE.md's third comparand legible. Root could
read what the model reasoned, beside what it answered, beside what the chain
authored. Nothing else in this repository can supply that.

### What it risks

1. **Provider terms — the blocking risk.** DeepSeek's and Ollama's reasoning
   content is served under their terms. Persisting it into a public repository is
   a redistribution decision. `THIRD_PARTY_NOTICES.md` has no entry covering
   provider-generated reasoning text, and the transport's own docstring treats
   non-persistence as an obligation it *keeps*, not a default it happens to have.
   **This is an owner decision and an agent must not take it.**
2. **Size.** F001 occurrence-01's `native` call returned 18,368 body bytes for
   2,979 reasoning tokens at an 8,192 ceiling. At 32,768 on a family that reasons
   by default, a single node could write on the order of 150 kB. Across F001's
   own `max_calls_envelope` of 156 coordinates that is tens of megabytes into a
   tree that currently stores digests.
3. **Non-determinism and custody.** Reasoning text is not covered by
   `request_sha256` and is not reproducible: two calls with byte-identical
   payloads return different reasoning. It would be the first large field in a
   write-once record that is neither pinned nor derivable, and `plan_id` would not
   cover it. A custody chain whose discipline is "every field is pinned or
   explained" would acquire a field that is neither.
4. **Leakage into the run.** The transport promises reasoning is "never
   persisted, never returned, and **never fed to another call**". Persisting it
   creates a path — a later node reading a stored reasoning file — that no current
   check forbids. The comparability of every H005-family arm depends on that path
   not existing, so a new refusal would have to be written, tested and pinned
   before the first call, not after.
5. **Credential surface.** Redaction and the `CREDENTIAL_ECHO` check currently run
   over the record and the raw text. Reasoning is a much larger surface for an
   echoed credential and would need the same `redact_with_names` treatment plus
   its own echo check, or `write_new`'s `CREDENTIAL_IN_OUTPUT` guarantee weakens
   silently.

---

## 4. Option B — digest and counts only. **Recommended.**

### The change

One successor transport, `src/minireason/provider_openai_compat_v2.py`, a byte
copy of `cdc4b57…` with these declared differences and no others:

* **(a)** the provenance header, naming the parent digest and this list;
* **(b)** `_Normalised` gains `reasoning_sha256: str | None` and
  `reasoning_chars: int`;
* **(c)** `_normalise_openai` computes both from the text it already holds, after
  `redact()`, and discards the text as it does today;
* **(d)** `_normalise_native` does the same for `message.thinking`;
* **(e)** `_finish` writes `reasoning_content_sha256` and
  `reasoning_content_chars` into the record beside `reasoning_content_present`;
* **(f)** `CallResult` gains the two read-only fields.

`reasoning_content_persisted` **stays the constant `False`** and
`native_reasoning_text_persisted` stays `False` in `_settings_view`, because the
text still is not persisted. A digest is not the content. **No runner change is
needed**: `decode_contribution` refuses on `reasoning_content_persisted`, which
does not move, so every existing custody check passes unchanged.

### Tests the successor would need

The diff proof (normalise the header away, refuse any hunk not marked `# V2:`),
as v2/v3 and the contrast driver v2 each carry; the digest is taken of the
**redacted** text; a call with no reasoning writes `null` and `0`; two identical
reasoning strings digest identically and two different ones differ; the written
record still carries `reasoning_content_persisted: false`; **a scan asserting the
reasoning text itself appears nowhere in the record bytes**; and the payload
digest is byte-identical to the parent's, so no request byte moves.

### What it buys, stated exactly

* **Identity across calls.** "Did these two calls reason the same way?" becomes
  answerable. Today it is not, at any ceiling, on any family.
* **Extent.** `reasoning_chars` beside the already-published `reasoning_tokens`
  separates "how much reasoning" from "how much reasoning was billed".
* **A check on the wire control.** `reasoning_content_present` is a boolean;
  a digest that is stable across a `thinking: disabled` arm and differs across a
  `thinking: enabled` one is stronger evidence the control was honoured than
  `THINKING_MODE_MISMATCH` alone.

### What it does not buy, stated just as exactly

**A digest answers identity, never content.** Option B does *not* make native
reasoning legible to root, and no reading of it can say what the model reasoned.
If root wants the content, that is Option A, and Option A is an owner decision on
provider terms that this document does not pre-empt.

---

## 5. The decision

**Option B, and not now.** The digest is the smallest change that answers a
question the current record cannot answer, at no redistribution risk, no size
risk and no new path into a later call. But it should be made **when a study
needs it**, not speculatively: it is a successor transport whose only consumer
today would be a `native` arm that nothing is authorised to dispatch (see
`PLAN.md` §8). Writing a transport successor for no live consumer would add an
unpinned identity to a tree whose whole discipline is that identities have
consumers.

**The step available now costs nothing and has never been taken:** the published
`native` calls already carry `reasoning_tokens` — 2,979 at F001 occurrence-01,
886 at H005 occurrence-01 — beside `bare` calls that carry none, on
byte-identical `messages`. That comparison is in the tree, unread, and needs no
code at all.
