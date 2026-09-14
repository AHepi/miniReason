# Adversarial review — `src/minireason/loop/receipts.py` (W0-RECEIPTS)

Scope: the module as it stands in this frozen sandbox snapshot, read against its own
docstring, `notes/WAVE0-INTERFACE.md` §5 and O3/O4, the W0-RECEIPTS row of
`design/design-s7-wave-plan.md` §7, and `AGENTS.md`. `design/design-s2-roles-and-guard.md`
assigns this module no guard: G0–G12 are the trial's, and nothing in §2 names the ledger
writer. So the acceptance clauses this module answers to are the wave-plan row and the
repository operating rules, and those are what I attacked.

Every finding below was executed. Probes live in `probe/` and run as
`python3 probe/<name>.py` from the sandbox root. Nothing under `src/` was edited; the two
probes that replace a module attribute (`_open_append`, `_unlock`) restore it in a
`finally` and say so in their own docstrings.

Counts in this review are reported with the command that produced them. The snapshot
ships no test module for this file: `python3 run_tests.py` prints `Ran 0 tests in 0.000s`
and `python3 run_tests.py tests.loop.test_receipts` prints `Ran 1 test … FAILED
(errors=1)` (the loader error for a missing module). So no claim below is checked by a
test that exists here.

Findings are ordered BLOCKER, SHOULD-FIX, NOTE. They are not ranked inside a band and
nothing here is scored.

---

## BLOCKER

### B1 — `open_receipt(render=…)` mints an id it never checks the paragraph carries, so two callers get the same receipt id

**Claim.** Minting reads the ledger's own bytes; a `render` callback that does not echo
the minted id verbatim spends no id, and the next `open_receipt` hands the same
`REC-<date>-<letter>` to a second caller — with no contention and no second process.

**Where.** `src/minireason/loop/receipts.py` lines 643–666 (the `_render` closure inside
`open_receipt`, and its return of `appended.receipt_id`), together with
lines 518–541 (`_append`, which appends whatever `render` returned without inspecting it).

**What it contradicts.** Module docstring, lines 22–25:

> **The receipt id is minted under the same lock that performs the append**, so two
> concurrent agents cannot mint the same letter.

`open_receipt`'s own docstring, lines 619–621:

> The id is minted from the ledger's own bytes under the same lock that writes the
> paragraph, so two agents opening a receipt at the same instant get different letters.

And the W0-RECEIPTS acceptance clause in `design/design-s7-wave-plan.md` §7:

> id minting under contention never collides

**Probe.** `python3 probe/p09_render_id.py`:

```
ids returned to three callers: REC-20260914-A REC-20260914-A REC-20260914-B
ids visible in the ledger    : ('A',)
collision                    : False
--- ledger ---
# ledger

Pre-registration opened at 2026-09-14 09:12:33 UTC: a paragraph that omits its own id.

REC-20260914-A opened at 2026-09-14 09:12:33 UTC: an ordinary receipt. Choice: c. Why: w. Contribution: k. State: pending.

Pre-registration opened at 2026-09-14 09:12:33 UTC: a paragraph that omits its own id.

lower-cased id in the paragraph: REC-20260914-A REC-20260914-A -> same id twice: True
open_preregistration then open_receipt: REC-20260914-A REC-20260914-B -> distinct: True
activity decision field: not-a-receipt-id
close_receipt same string -> RECEIPT_ID_MALFORMED
```

The first and second callers both hold `REC-20260914-A`. Every later
`outcome_receipt` / `checkpoint_receipt` / `close_receipt` from either caller appends
under that one id, and the ledger then carries two unrelated decisions under one receipt.
The `.lower()` variant is the same defect one step removed: `RECEIPT_ID_RE` is
`REC-(\d{8})-([A-Z]+)`, so a case change makes the id invisible to `scan_receipt_ids`.
`probe/p15_minting_attacks.py` shows the same blindness from the other side:

```
suffixes scanned: ()
mint             -> REC-20260914-A
```

on a ledger whose only paragraphs are `rec-20260914-a` and `REC-20260914-b`.

The shipped caller is safe: `open_preregistration` renders
`_PREREGISTRATION_HEADER` (lines 741–744), which formats the id in, and the probe's last
contrast line confirms two successive pre-registrations get `A` then `B`. The defect is
in the seam, not in that one use of it — and the seam is published: the wave plan's
`public_interface` for this module is `open_receipt(**kw) -> rec_id`.

**Repair.** In `_render` (lines 643–647), after calling `render`, assert that the returned
text spends the id it was handed — cheapest correct form, reusing the minting scanner so
the assertion and the mint cannot diverge:

```python
text = render(receipt_id, stamp)
if receipt_id.rsplit("-", 1)[1] not in scan_receipt_ids(text.encode("utf-8"), token):
    raise ReceiptError("RECEIPT_ID_MALFORMED",
                       f"the rendered paragraph does not carry {receipt_id}")
```

A plainer `if receipt_id not in text` would also close it; the form above reuses the
scanner so a paragraph that spells the id in a way `scan_receipt_ids` cannot see — the
lower-cased case — is refused too. Either way the refusal must happen inside
`_append`'s lock, before the write, so no id is spent by a rejected paragraph.

The predicate separates the cases. `python3 probe/p16_b1_repair_predicate.py` evaluates it
against the same render callables, without patching `src/`:

```
 refused  omits the id (the defect)
          scan_receipt_ids -> ()
 refused  lower-cases the id (the defect)
          scan_receipt_ids -> ()
accepted  the shipped pre-registration header shape
          scan_receipt_ids -> ('A',)
accepted  carries the id mid-sentence
          scan_receipt_ids -> ('A',)
 refused  carries a DIFFERENT id only
          scan_receipt_ids -> ('Q',)
```

**Test that would hold it.** In `tests/loop/test_receipts.py`: append with
`render=lambda rid, stamp: "a paragraph with no id"` and assert the refusal code; then
two successive `open_receipt(render=…)` calls whose renders *do* carry the id, and assert
the two returned ids differ and both appear in `scan_receipt_ids(ledger.read_bytes(),
token)`. A property-style version is stronger: after *n* opens by any mix of the three
body forms, `len(set(returned_ids)) == n == len(scan_receipt_ids(data, token))`.

---

### B2 — `DEFAULT_LEDGER_PATH` resolves to whichever ancestor directory carries `tools/repo_activity.py`, so a default-path receipt can land in another repository's ledger

**Claim.** `_repository_root()` walks every ancestor of the module file to `/`. An
installed wheel that sits under *some* checkout — a virtualenv inside one — resolves to
that checkout, not to `None`, and `open_receipt()` with no `ledger_path=` appends a
receipt to that project's `docs/DECISION_LEDGER.md`.

**Where.** `src/minireason/loop/receipts.py` lines 148–174 (`_repository_root`,
`DEFAULT_REPO_ROOT`, `DEFAULT_LEDGER_PATH`); the deviation it is justified by is
lines 69–76.

**What it contradicts.** Module docstring, deviation 8, lines 69–76:

> **:data:`DEFAULT_REPO_ROOT` is found by walking up for ``tools/repo_activity.py``**,
> not by counting ``parents[3]``, and is ``None`` when this module was not imported from
> a checkout — which is what an installed wheel is. ``None`` is a named refusal at the
> call (``LEDGER_NOT_FOUND`` / ``ACTIVITY_TOOL_MISSING``) rather than a write into
> whatever directory ``parents[3]`` happened to name.

and deviation 7, lines 63–68, which names the harm:

> a mistyped path or a wrong repository root used to succeed into a *second* ledger whose
> receipt letters restarted at ``A`` — the collision the id minting exists to prevent,
> arrived at from the other side.

**Probe.** `python3 probe/p14_default_root.py` copies `src/minireason` and
`src/deepreason_core` into `…/some-other-checkout/.venv/lib/python3/site-packages/`,
gives that checkout a `tools/repo_activity.py` and a ledger of its own, and re-imports:

```
imported from       : /tmp/tmpp_x79pwf/some-other-checkout/.venv/lib/python3/site-packages/minireason/loop/receipts.py
DEFAULT_REPO_ROOT   : /tmp/tmpp_x79pwf/some-other-checkout
DEFAULT_LEDGER_PATH : /tmp/tmpp_x79pwf/some-other-checkout/docs/DECISION_LEDGER.md
is that this run's repository?  no - it is some-other-checkout
open_receipt() with no ledger_path minted: REC-20260914-B
and appended into the other checkout's ledger: True
# Another project's decision ledger

REC-20260914-A opened at 2026-09-14 00:00:00 UTC: not ours.

REC-20260914-B opened at 2026-09-14 11:28:00 UTC: a receipt with no ledger_path=. Choice: use the default. Why: O3 says pass it explicitly. Contribution: shows what the default resolves to. State: pending.
```

The `create=False` guard of deviation 7 cannot help here: the wrong ledger exists, so the
append is not a "new ledger" and nothing refuses. The wheel case deviation 8 names
explicitly — "which is what an installed wheel is" — is exactly the case that resolves to
a non-`None` wrong root, because a venv normally lives inside a checkout.

I am not claiming the walk is wrong in a source checkout. In this sandbox it correctly
returns `None` (`python3 probe/p01_smoke.py` prints `DEFAULT_REPO_ROOT = None`), and the
refusal path works (`probe/p04_refusals.py`, cases 4 and 6, print `LEDGER_NOT_FOUND`).
The defect is that "not imported from a checkout" is not the same predicate as "no
ancestor carries the marker", and the second predicate can name a repository that has
nothing to do with the run.

**Repair.** Two parts, both cheap.
1. Stop at the first ancestor that is a *repository*, not the first that carries the
   marker: require `(candidate / ".git").exists()` **and**
   `(candidate / ACTIVITY_TOOL_RELATIVE).is_file()`, and stop the walk at the first
   `.git` seen whether or not it carries the tool (so a checkout without the tool is a
   named refusal rather than a silent climb past it into a parent checkout).
2. Refuse to walk out of the installation: if any ancestor between the module and the
   candidate is named `site-packages`, return `None`. That makes deviation 8's sentence
   about wheels true as written.

Independently, O3's recommendation — always pass `ledger_path=` and `repo_root=`
explicitly from the run's resolved root — should become a PREFLIGHT assertion rather than
advice, since the default is reachable from every published entry point.

**Test that would hold it.** Build the layout the probe builds (an outer directory with
`tools/repo_activity.py` and a `site-packages` copy of the package), import
`minireason.loop.receipts` from it in a subprocess, and assert `DEFAULT_REPO_ROOT is
None`. A second case: an outer directory with `.git` and the marker, imported from a
source path under it, asserts the root is that directory.

---

## SHOULD-FIX

### S1 — a refusal inside `_append` with `create=True` leaves a zero-byte ledger behind, and every later `create=False` call then appends into it

**Claim.** `_open_append` runs before the paragraph is checked, so `SECRET_IN_RECEIPT`,
`LEDGER_EMPTY_PARAGRAPH` and any exception raised by `render` all leave the created file
on disk. Deviation 7's guard then passes for that path forever after.

**Where.** `src/minireason/loop/receipts.py` lines 519–527 — `_open_append(path)` at 519,
`render(data)` at 523, `LEDGER_EMPTY_PARAGRAPH` at 526, `_refuse_secret` at 527. The file
is created by `_open_append` (lines 438–441, `path.open("ab", buffering=0)`).

**What it contradicts.** Module docstring, lines 27–30:

> **A receipt body carrying a registered credential is refused, never redacted.** … A
> refusal names the environment variable, never the value, and writes nothing.

**Probe.** `python3 probe/p04_refusals.py`:

```
registered: PROBE_FAKE_KEY
1 existing ledger  -> SecretInReceipt SECRET_IN_RECEIPT | ledger paragraph carries PROBE_FAKE_KEY
   names: ('PROBE_FAKE_KEY',)
   bytes unchanged: True
2 before: fresh.md exists = False
2 fresh ledger     -> SECRET_IN_RECEIPT
   after refusal: fresh.md exists = True size = 0
3 create=False into the file the refusal left behind -> REC-20260914-A
4 missing ledger   -> LEDGER_NOT_FOUND
   nope.md exists = False
5 blank paragraph  -> LEDGER_EMPTY_PARAGRAPH
6 no default       -> LEDGER_NOT_FOUND
```

Case 1 is the load-bearing half and it holds: on an existing ledger the refusal changes
no byte. Case 2 is the defect: the refusal created the file. Case 3 shows the
consequence — a subsequent `create=False` open now succeeds and mints `REC-20260914-A`
into a second ledger, which is the letter-restart deviation 7 names.

**Repair.** Open the handle only after the paragraph is composed and cleared, or record
whether the file existed before `_open_append` and unlink it on any exception raised
before a byte is written:

```python
pre_existing = path.exists()
...
except BaseException:
    if not pre_existing and path.exists() and path.stat().st_size == 0:
        path.unlink()
    raise
```

The size check keeps the cleanup from ever removing a ledger that has content.

**Test that would hold it.** `ledger_append(<text carrying a registered env value>,
missing_path, create=True)` raises `SecretInReceipt` **and** `missing_path.exists()` is
`False`; the same for `create=True` with a blank paragraph, and for a `render` that
raises.

---

### S2 — `activity` still lets one class of logger failure escape as a non-`LoopError`

**Claim.** A spawn failure from the runner (`OSError`, and every `subprocess.SubprocessError`
other than `TimeoutExpired`) propagates unchanged, so `except LoopError` misses it and the
step can name no `failure_code` — the precise defect the docstring says was fixed for
timeouts.

**Where.** `src/minireason/loop/receipts.py` lines 938–943: the `try` around
`runner(...)` catches `subprocess.TimeoutExpired` only.

**What it contradicts.** `activity`'s docstring, lines 900–906:

> Every way the logger can fail carries a code from the table. A timeout used to
> propagate ``subprocess.TimeoutExpired`` unchanged, which is not a
> :class:`~minireason.loop.types.LoopError`, so ``except LoopError`` missed it and the
> step could name no ``failure_code``; it is now ``ACTIVITY_LOGGER_FAILED``.

**Probe.** `python3 probe/p06_activity.py`, last block:

```
=== how the logger can fail ===
  timeout              -> LoopError ACTIVITY_LOGGER_FAILED
  no returncode        -> LoopError ACTIVITY_LOGGER_FAILED
  exit 3               -> LoopError ACTIVITY_LOGGER_FAILED
  OSError from spawn   -> OSError (NOT a LoopError): [Errno 8] Exec format error
```

Three of the four named failures carry a code. The fourth does not, and it is the one
`subprocess.run` raises for a real spawn failure — a `sys.executable` that is not
executable, `EMFILE`, `ENOMEM`, a `tools/repo_activity.py` that passed `is_file()` and
then could not be run.

**Repair.** Widen the handler at lines 940–943:

```python
except subprocess.TimeoutExpired as expired:
    raise ReceiptError("ACTIVITY_LOGGER_FAILED", f"timed out after {timeout} s") from expired
except (OSError, subprocess.SubprocessError) as failed:
    raise ReceiptError("ACTIVITY_LOGGER_FAILED", type(failed).__name__) from failed
```

The detail must stay a type name: an `OSError`'s `strerror` can carry the argv, and the
argv carries `--why` and `--goal` text.

**Test that would hold it.** A runner that raises `OSError(8, "Exec format error")`, and
one that raises `subprocess.SubprocessError`, both asserted to raise `ReceiptError` with
`.code == "ACTIVITY_LOGGER_FAILED"` and a detail that does not contain the goal string.

---

### S3 — `bracket` replaces the failure it is bracketing when the outcome record cannot be written

**Claim.** If the `outcome` activity call fails, the `ReceiptError` from the logger
propagates and the real repository failure survives only as `__context__`. A driver's
`except LoopError` then records the logging failure as the step's `failure_code`.

**Where.** `src/minireason/loop/receipts.py` lines 966–969 — `activity("outcome", …)`
called inside `except BaseException` with the `raise` after it.

**What it contradicts.** `bracket`'s docstring, lines 959–960, which promises the
opposite direction of care about what reaches the record:

> An exception is reported by type only; an exception message can carry anything,
> including a credential, and is never logged.

and `AGENTS.md`: "Every failure receives an erratum with evidence" — the erratum will
name the wrong failure.

**Probe.** `python3 probe/p10_bracket_reentry.py`:

```
what the caller catches : ReceiptError ACTIVITY_LOGGER_FAILED | ACTIVITY_LOGGER_FAILED: exit 9
what it replaced        : Disk | the disk went away
traceback tail:
    minireason.loop.receipts.ReceiptError: ACTIVITY_LOGGER_FAILED: exit 9
```

`Disk("the disk went away")` is the failure the bracket was wrapping. What the caller
catches is `ACTIVITY_LOGGER_FAILED`.

**Repair.** In the `except` branch, attempt the outcome record and swallow only the
logging refusal, re-raising the original:

```python
except BaseException as error:
    try:
        activity("outcome", action, f"{why}; interrupted by {type(error).__name__}",
                 goal, paths, **kwargs)
    except ReceiptError as logging_failed:
        error.__notes__ = getattr(error, "__notes__", [])
        error.__notes__.append(f"activity outcome record failed: {logging_failed.code}")
    raise
```

The unlogged outcome must still be visible, hence the note rather than a bare `pass`.

**Test that would hold it.** A runner whose first call returns 0 and whose second returns
non-zero; the body raises a sentinel; assert the sentinel is what escapes, and that the
`ACTIVITY_LOGGER_FAILED` code appears in the escaping exception's notes.

---

### S4 — `open_receipt`'s two content guards check presence, not content, and the "three mutually exclusive ways" are not exclusive

**Claim.** `RECEIPT_FIELDS_MISSING` passes on four whitespace fields;
`LEDGER_EMPTY_PARAGRAPH` passes on `body=""` because the id/form/stamp prefix keeps the
paragraph non-blank; and `body=` or `render=` given *together with* the four house fields
silently drops `title`, `choice`, `why`, `contribution`, `paths`, `evidence` and
`source_identity` instead of raising `RECEIPT_BODY_AMBIGUOUS`.

**Where.** `src/minireason/loop/receipts.py` lines 631–638 (the two guards) and 647–659
(the `composed = …` branch, skipped by the `if body is not None` at line 647).

**What it contradicts.** `open_receipt`'s docstring, lines 623–629:

> Three mutually exclusive ways to say what the receipt says: the four house fields
> (``title``/``choice``/``why``/``contribution``, what AGENTS.md requires), a
> pre-composed ``body`` …, or a ``render(receipt_id, stamp)`` callable …

and `AGENTS.md`:

> Every design, implementation, experiment, interpretation, delegation, publication and
> stopping decision must have an append-only receipt in the ledger before action: choice,
> reason, contribution to the end goal, and pending or completed state with evidence.

The `source_identity` case is the sharpest: deviation 5 (lines 55–59) says that field is
`docs/lessons/operations.md` line 20's disclosure rule "given a place to live", and line
20 reads "a future retry must disclose that new identity … never silently edit an old
plan to make it runnable". With `render=` given, the disclosure is dropped without a word.

**Probe.** `python3 probe/p05_empty_receipt.py`:

```
1 whitespace fields   -> minted REC-20260914-A
  paragraph: b'REC-20260914-A opened at 2026-09-14 09:12:33 UTC: State: pending.'
2 body=''             -> minted REC-20260914-A
  paragraph: b'REC-20260914-A opened at 2026-09-14 09:12:33 UTC: '
3 render->''          -> LEDGER_EMPTY_PARAGRAPH
4 body + four fields  -> minted REC-20260914-A (no RECEIPT_BODY_AMBIGUOUS)
  paragraph: b'REC-20260914-A opened at 2026-09-14 09:12:33 UTC: only this survives'
5 render + four fields-> minted REC-20260914-A (no RECEIPT_BODY_AMBIGUOUS)
  paragraph: b'REC-20260914-A opened at 2026-09-14 09:12:33 UTC: only this.'
6 paths='...' (a str) -> paragraph:
   b'REC-20260914-A opened at 2026-09-14 09:12:33 UTC: T. Choice: C. Why: W. Contribution: K. Paths: `s`, `r`, `c`, `/`, `m`, `i`, `n`, `i`, `r`, `e`, `a`, `s`, `o`, `n`, `/`, `l`, `o`, `o`, `p`, `/`, `r`,'
```

Cases 1 and 2 are receipts that carry no choice, no reason, no contribution and no
evidence, and they spend a receipt id. Case 3 shows the guard that does work, which is
what makes 1 and 2 gaps rather than policy. Case 6 is the `Sequence[str]` hazard: a `str`
*is* a `Sequence[str]`, so a single path passed unwrapped is rendered one backticked
character at a time.

**Repair.**
* Lines 631–638: build `given` from all three ways —
  `given = [name for name, value in (("fields", title or choice or why or contribution),
  ("body", body), ("render", render)) if value is not None]` — and raise
  `RECEIPT_BODY_AMBIGUOUS` when more than one is present.
* Test the four fields for content, not truth: require `_sentence(title)` and each of
  `_sentence(choice/why/contribution)` to be non-empty, else `RECEIPT_FIELDS_MISSING`.
* Move the emptiness test in `_append` (line 526) off the whole paragraph and onto the
  body: `_receipt_paragraph` should refuse `body.strip() == ""` with
  `LEDGER_EMPTY_PARAGRAPH` at lines 594–598.
* `_paths_clause` (lines 587–591) and `activity`'s `listed` (line 917) should refuse a
  bare `str` — `if isinstance(paths, (str, bytes)): raise ReceiptError(...)` — rather than
  iterate it.

**Test that would hold it.** Parametrised refusals: `title=" ", choice=" ", why=" ",
contribution=" "` → `RECEIPT_FIELDS_MISSING`; `body=""` → `LEDGER_EMPTY_PARAGRAPH`;
`body="x"` with any house field → `RECEIPT_BODY_AMBIGUOUS`; `render=…` with
`source_identity=…` → `RECEIPT_BODY_AMBIGUOUS`; `paths="a/b"` → refused. Each asserts the
ledger is byte-unchanged afterwards.

---

### S5 — `_COMMAND_TEXT_MARKERS` is a fifteen-substring blocklist, and plainly credential-bearing command text walks through it

**Claim.** `activity` accepts `--api-key sk-…`, `--key sk-…`, a `postgres://user:pass@…`
URL, a `https://user:pass@host` URL and an `X-Api-Key:` header, none of which hit a
marker. A credential that is not a value of a registered environment variable in *this*
process is not caught by the secret scan either.

**Where.** `src/minireason/loop/receipts.py` lines 202–206 (the marker tuple) and
342–348 (`_refuse_command_text`).

**What it contradicts.** `activity`'s docstring, lines 896–898:

> No command is ever forwarded — the wrapper has no command channel at all, so no record
> can carry raw command text — and any field carrying a registered credential is refused
> rather than redacted.

the W0-RECEIPTS acceptance clause in `design/design-s7-wave-plan.md` §7 —
"activity records carry no raw command text" — and `AGENTS.md`: "never log credentials or
raw secret-bearing command text."

**Probe.** `python3 probe/p11_command_text.py`:

```
ACCEPTED  'python3 tools/provider_smoke.py --api-key sk-live-9f3a2b7c11de'
          -> argv carries: python3 tools/provider_smoke.py --api-key sk-live-9f3a2b7c11de
ACCEPTED  'python3 tools/provider_smoke.py --key sk-live-9f3a2b7c11de'
          -> argv carries: python3 tools/provider_smoke.py --key sk-live-9f3a2b7c11de
ACCEPTED  'psql postgres://loop:hunter2hunter2@db.internal/runs'
          -> argv carries: psql postgres://loop:hunter2hunter2@db.internal/runs
ACCEPTED  'wget -O plan.json https://user:hunter2hunter2@host/plan.json'
          -> argv carries: wget -O plan.json https://user:hunter2hunter2@host/plan.json
ACCEPTED  'ssh -i /home/user/.ssh/id_ed25519 deploy@host'
          -> argv carries: ssh -i /home/user/.ssh/id_ed25519 deploy@host
ACCEPTED  'http POST api.example/v1 X-Api-Key:sk-live-9f3a2b7c11de'
          -> argv carries: http POST api.example/v1 X-Api-Key:sk-live-9f3a2b7c11de
refused   "curl -H 'Authorization: Bearer sk-live-9f3a2b7c11de' https://api.example" -> ACTIVITY_RAW_COMMAND_TEXT
refused   'export DEEPSEEK_API_KEY=sk-live-9f3a2b7c11de' -> ACTIVITY_RAW_COMMAND_TEXT
refused   'ran the smoke test with sk-probe-0123456789abcdef' -> SECRET_IN_RECEIPT
```

`probe/p06_activity.py` adds that plain commands (`git push --force origin main`,
`rm -rf experiments/loops/RUN-1`, `python3 tools/auto_loop.py run --config loop.json`)
are accepted verbatim into `--action`.

The last three lines are the module working: the two markers it does carry fire, and a
value this process really holds is refused by name. The finding is that the sentence "no
record can carry raw command text" is stronger than the mechanism, and the mechanism is
the only thing standing between a pasted command line and `docs/AGENT_ACTIVITY.jsonl`.

**Repair.** Either weaken the sentence to what the code does — "a short blocklist refuses
the most common credential-bearing command forms; the structural guarantee is only that
this wrapper forwards no command" — or strengthen the check. A structural check is
available and cheap: refuse an `action`/`why`/`goal` whose first whitespace-delimited
token is an executable name the repository knows (`git`, `curl`, `python3`, `ssh`, `psql`,
`wget`, `http`, `pip`, `gh`) or that contains ` -` followed by a letter, and add
`key=`, `key:`, `-key `, `--key`, `password`, `secret`, `://` with an `@`, and `Basic ` to
the markers. Whichever is chosen, the docstring and the mechanism must agree.

**Test that would hold it.** The six accepted strings above become a parametrised refusal
list asserting `ACTIVITY_RAW_COMMAND_TEXT`; a companion list of ordinary prose actions
("read the wave plan", "exported the reading table") asserts they are *not* refused, so
the widened blocklist is pinned against over-refusal too.

---

### S6 — a `paths` entry that looks like an option is forwarded into the logger's argv unescaped

**Claim.** `activity` validates each path for control characters and command markers but
not for a leading `-`, so `paths=["--agent", "someone-else"]` is placed into the argv
after `--paths` as two more option-shaped tokens.

**Where.** `src/minireason/loop/receipts.py` lines 917–920 (the per-path scans) and
lines 930–937 (argv assembly, `argv.extend(["--paths", *listed])`).

**What it contradicts.** `activity`'s docstring, lines 894–898:

> The logger is shelled, never reimplemented: it owns the atomic locked append to
> ``docs/AGENT_ACTIVITY.jsonl`` and this module has no business owning a second
> implementation of it. No command is ever forwarded …

and `AGENTS.md`: "Record a specific action, relevant paths, why and goal".

**Probe.** `python3 probe/p06_activity.py`:

```
=== a path that is an option of the logger's own CLI ===
  argv: ('--paths', '--agent', 'someone-else', '--decision', 'REC-20260101-Z')
  full argv tail: ('--agent', 'auto_loop', '--decision', 'REC-20260914-A', '--action', 'an action', '--why', 'why', '--goal', 'goal', '--phase', 'event', '--paths', '--agent', 'someone-else', '--decision', 'REC-20260101-Z')
```

**Honest limit.** The argv above is what the module builds, and that much is executed.
What `tools/repo_activity.py` then does with it I could not determine: the file is not in
this sandbox — `python3 -c "import os; print('tools dir present:', os.path.isdir('tools'))"`
prints `tools dir present: False` — so I do
not know whether its parser takes `--paths` as `nargs="+"` (in which case argparse would
reject the call outright, since the next token starts with `-`), as `nargs="*"`, or as a
repeated option. All three outcomes are wrong records; which one it is, I am not
reporting.

**Repair.** Refuse a path beginning with `-` (`ACTIVITY_RAW_COMMAND_TEXT` or a new
`ACTIVITY_PATH_INVALID`), or pass `--paths` with an explicit `--` terminator ahead of the
list and require the logger to honour it. Refusing is the smaller change and keeps the
wrapper's "no channel" story true.

**Test that would hold it.** `activity("event", "a", "w", "g", paths=["--agent"])` raises;
`paths=["-"]` raises; `paths=["docs/STATUS.md"]` still produces
`("--paths", "docs/STATUS.md")`.

---

### S7 — the same missed deadline is disclosed with two different numbers depending on which seam writes the paragraph

**Claim.** `Cadence.record_checkpoint` discloses the lateness recorded at *first notice*;
`checkpoint_receipt(cadence=<CadenceCheck>)` fabricates a `CadenceMiss` whose
`recorded_utc` is the *write* moment, and so states a notice time that is not the notice
time.

**Where.** `src/minireason/loop/receipts.py` lines 706–708 (`checkpoint_receipt`'s
`CadenceCheck` branch, which builds `CadenceMiss(cadence.deadline_utc, cadence.now,
cadence.overdue_seconds)`) against line 1042 (`record_checkpoint`'s
`miss = self._misses[-1]`).

**What it contradicts.** `CadenceMiss`'s docstring, lines 285–286:

> ``recorded_utc`` is the observation time and is never the deadline: a missed deadline
> is recorded truthfully and never backdated.

and the W0-RECEIPTS acceptance clause "a missed cadence deadline is recorded and never
backdated", and `AGENTS.md`: "Record a missed deadline truthfully, never backdate it."

**Probe.** `python3 probe/p12_miss_disclosure.py` — one clock started at 09:00:00, first
looked at at 09:05:10 (10 s past the 300 s deadline), paragraph written at 09:13:30 in
both arms:

```
A record_checkpoint       : REC-20260914-A progress at 2026-09-14 09:13:30 UTC: arm A progress. Cadence deadline 2026-09-14 09:05:00 UTC was missed and is recorded at the time it was noticed, 2026-09-14 09:05:10 UTC, 10 s overdue; it is not backdated.
B checkpoint_receipt(check): REC-20260914-A progress at 2026-09-14 09:13:30 UTC: arm B progress. Cadence deadline 2026-09-14 09:05:00 UTC was missed and is recorded at the time it was noticed, 2026-09-14 09:13:30 UTC, 510 s overdue; it is not backdated.

A discloses overdue: 10.0 s
B discloses overdue: 510.0 s
true lateness at the moment both paragraphs are stamped: 510.0 s
```

Arm A is defensible on its own terms — 09:05:10 really is when it was noticed. Arm B is
not: the clock noticed at 09:05:10 and arm B's sentence asserts it was noticed at
09:13:30. The sentence is generated by the module, not by the caller, so the module is
the author of the inaccurate claim.

**Repair.** Two sentences, not one. Keep `CadenceMiss.sentence()` for the notice, and have
`checkpoint_receipt` add a separate clause for the lateness at write time when they
differ — e.g. `"… recorded at the time it was noticed, {noticed}, {overdue:.0f} s
overdue; this paragraph is written {later:.0f} s after the deadline; it is not
backdated."` The `CadenceCheck` branch at 706–708 should consult the clock's recorded
miss rather than invent one; simplest is to delete that branch and require callers to
pass `cadence=<CadenceMiss>`, which is what `Cadence.record_checkpoint` already does.

**Test that would hold it.** Drive one `Cadence` through notice-then-write as the probe
does, take the paragraph from both seams, and assert the two texts carry the same
`recorded at the time it was noticed, <stamp>` and the same overdue figure; and assert
that figure equals `(first_notice - deadline).total_seconds()`.

---

## NOTE

### N1 — `LedgerAppend.sha256` is the digest of the whole file after the append, taken after the flock is released

`src/minireason/loop/receipts.py` lines 535–541. The dataclass docstring at line 245 says
"What one append did, in bytes, so a caller can prove it added only." `offset`, `written`
and `text` support that claim; `sha256` is `hashlib.sha256(after).hexdigest()` over the
entire file, and `after = _read_bytes(path)` happens outside the lock.
`python3 probe/p12_miss_disclosure.py`:

```
append.sha256            : cb5732f41aa0ae76
sha256(whole file)       : cb5732f41aa0ae76
sha256(appended payload) : 3987aa34cf5f94bc
…
c.md after         : b"# ledger\n\nmine\n\nsomeone else's paragraph\n"
my append verified : b'\nmine\n'
out.sha256 covers the outsider's bytes: True
```

The second block plants a second writer between unlock and read-back. The verification
slice is unaffected (it is taken by offset, and appends only grow the tail), so the
`LEDGER_APPEND_NOT_VERIFIED` guard is sound. Only the reported digest is of a file state
this append did not produce. Repair: take the read-back inside the lock, and either
rename the field `file_sha256` or make it the digest of `payload`.

### N2 — `notes/WAVE0-INTERFACE.md` §5 and O3 no longer describe this module

`python3 probe/p13_interface_drift.py`:

```
ledger_append
  note  : (text, ledger_path=DEFAULT_LEDGER_PATH, *, newline=b'\n') -> LedgerAppend
  actual: (text: 'str', ledger_path: 'Path | str | None' = None, *, newline: 'bytes' = b'\n', create: 'bool' = False) -> 'LedgerAppend'
  'create' in the actual signature: True
…
DEFAULT_REPO_ROOT   note: 'Path'  actual: NoneType = None
DEFAULT_LEDGER_PATH note: 'Path'  actual: NoneType = None
```

`create=` is absent from all four recorded signatures; `DEFAULT_REPO_ROOT` and
`DEFAULT_LEDGER_PATH` are typed `Path` in the note and are `Path | None` in the module;
`LEDGER_NOT_FOUND` is raised by the module (`probe/p01_smoke.py`:
`raised but not in WAVE0-INTERFACE section 5: ['LEDGER_NOT_FOUND']`) and is absent from
the note's code list, though it *is* a member of `types.FAILURE_CODES`
(`python3 probe/p01_smoke.py` → `all in FAILURE_CODES : True`). O3's text —
"`receipts.DEFAULT_REPO_ROOT` is `Path(__file__).parents[3]`" — describes code that is no
longer there; `parents[3]` survives only as prose inside `_repository_root`'s docstring.

The note is a published observation and must not be edited. The correction belongs in a
separately named supplement that identifies its source and its limits, as `AGENTS.md`
requires; a downstream wave that types against `DEFAULT_REPO_ROOT: Path` will be wrong.

### N3 — `Cadence` accepts negative thresholds

`src/minireason/loop/receipts.py` lines 986–988 compare `deadline_seconds < warn_seconds`
and nothing else. `python3 probe/p07_cadence.py`:

```
  inverted thresholds -> CADENCE_THRESHOLDS_INVERTED
  negative thresholds -> accepted; check at t+0 state = overdue
```

`Cadence(t, warn_seconds=-10.0, deadline_seconds=-5.0)` is overdue at construction and
records a miss whose deadline precedes its own start. A `warn_seconds < 0` /
`deadline_seconds <= 0` refusal under the same code would close it.

### N4 — a `render` that appends self-deadlocks with no timeout and no refusal

`_append`'s docstring (lines 501–502) says "``render`` … must not itself append", and the
consequence of disobeying is a hang, not a refusal: `flock` excludes a second open file
description in the same process. `python3 probe/p10_bracket_reentry.py`:

```
mint_receipt_id inside render -> returned ['REC-20260914-A']
   paragraph: b'REC-20260914-A opened at 2026-09-14 09:12:33 UTC: nested mint returned REC-20260914-A.'
ledger_append inside render   -> STILL BLOCKED after 5 s (self-deadlock)
```

The hang is inside `_APPEND_LOCK`, so it stops every other thread's ledger append for the
life of the process — including the cadence checkpoint that would report the stall. A
thread-local "already appending" flag raising a named refusal would turn it into a
diagnosis. The same probe's first line also shows `mint_receipt_id`'s warning at lines
404–405 ("Never call this from inside a render callback — the append lock is not
re-entrant across threads") is not what happens: `_APPEND_LOCK` is a `threading.RLock`
(line 212), so the nested mint succeeds and returns the id the outer render already holds.

### N5 — the free follow-up functions accept any `moment`, including one in the past

`_follow_up` (lines 669–675) passes `moment` straight to `utc_stamp` with no ordering
check. `python3 probe/p07_cadence.py`:

```
  checkpoint_receipt(moment=T0-400d): REC-20260914-A progress at 2025-08-10 09:00:00 UTC: progress.
```

The `Cadence` path is honest — `CADENCE_BACKDATED` fires on both `check` and
`acknowledge` — but the published `checkpoint_receipt` / `outcome_receipt` /
`close_receipt` seams do not carry that guarantee, and `AGENTS.md` says "never backdate
it". A module-level "last stamp written" high-water mark, refused below, would extend the
clock's discipline to the seams that write the paragraphs.

### N6 — `activity`'s `decision` is not held to the shape `_follow_up` enforces

Lines 910–912 accept any truthy string as the decision id, while `_follow_up` (lines
671–672) refuses anything that is not `RECEIPT_ID_RE.fullmatch`.
`python3 probe/p09_render_id.py`:

```
activity decision field: not-a-receipt-id
close_receipt same string -> RECEIPT_ID_MALFORMED
```

`AGENTS.md` requires mechanical executions to be recorded "under the decision they
implement"; the activity log can currently carry a decision id no ledger paragraph
matches.

### N7 — the Windows lock path is not exercisable here

Lines 444–457 take a different lock on `os.name == "nt"` (`handle.seek(0)` then
`msvcrt.locking(fileno, LK_LOCK, 1)` on a handle opened `"ab"`), marked
`# pragma: no cover - exercised on Windows only`. Every concurrency result in this review
is POSIX `flock`. Whether byte-0 locking on an append-mode handle gives the same exclusion
— in particular on a zero-length ledger, where byte 0 is past EOF — I could not determine
in this sandbox and am not reporting either way.

---

## Tried, and could not break

Six attacks that failed. Each is evidence about the module.

**1. Thread contention with simulated short writes.** `python3 probe/p02_threads.py` —
16 threads × 8 `open_receipt` calls, twice: once with ordinary writes, once with
`_open_append` wrapped in a handle that lands at most 3 bytes per `write()` call (the
"simulated short writes" the acceptance clause names).

```
[plain] expected=128 minted=128 distinct_minted=128 well_formed_paragraphs=128 distinct_paragraph_ids=128 errors=0
[plain] lines that are neither the header nor a whole receipt: 0
[short-write] expected=128 minted=128 distinct_minted=128 well_formed_paragraphs=128 distinct_paragraph_ids=128 errors=0
[short-write] lines that are neither the header nor a whole receipt: 0
```

No loss, no torn record, no duplicate letter, and 128 ids in one UTC date exercises the
bijective continuation past `Z`.

**2. Cross-process contention.** `python3 probe/p03_processes.py` — 8 forked processes
released from a barrier, 12 receipts each, where the in-process `RLock` cannot help and
only the `flock` is doing the work:

```
expected            : 96
ids returned        : 96 distinct: 96
paragraphs in file  : 96 distinct: 96
duplicate ids minted: []
torn / stray lines  : 0 []
```

The load-bearing claim — "two concurrent agents cannot mint the same letter" — holds for
the shipped body forms.

**3. Byte preservation against a mixed-ending, partly undecodable ledger.**
`python3 probe/p08_bytes.py` on a file mixing CRLF, LF, UTF-8 prose and `\xff\xfe`:

```
prefix sha256 before: 93769815a005ad6f len 216
minted: REC-20260914-B (new UTC date letters restart: ('Z',) -> ('A', 'B') )
prefix preserved byte-for-byte: True
appended region: b'\nREC-20260914-B opened at 2026-09-14 09:12:33 UTC: a receipt beside undecodable '
crlf file now: b'# ledger\r\nREC-20260914-A opened at x: seed.\r\n\na second paragraph\n'
```

Nothing re-encoded, no CRLF rewritten, no spurious blank line on a CRLF tail, and the
previous day's `Z` does not carry into the new date.

**4. The two write-integrity guards fire.** Same probe. A handle that reports writing
more than it wrote, and a handle that writes nothing:

```
lying handle -> LEDGER_APPEND_NOT_VERIFIED
victim bytes: b'# ledger\n\nthis write drops its last byte'
deaf handle  -> LEDGER_INCOMPLETE_WRITE | 0 of 16 bytes
```

Both are pre-registered refusals and both fire. (The lying-handle case does leave the
partial bytes on disk — unavoidable in an append-only file once a byte has landed, and
the refusal is what tells the caller to write an erratum.)

**5. Backdating the cadence clock.** `python3 probe/p07_cadence.py`:

```
  t+0      state=ok       due=False missed=False overdue=0.0
  t+239.9  state=ok       due=False missed=False overdue=0.0
  t+240    state=warn     due=True missed=False overdue=0.0
  t+299.9  state=warn     due=True missed=False overdue=0.0
  t+300    state=overdue  due=True missed=True overdue=0.0
  t+480    state=overdue  due=True missed=True overdue=180.0
…
  backwards check -> CADENCE_BACKDATED | 2026-09-14 09:06:40 UTC precedes 2026-09-14 09:08:20 UTC
  backwards acknowledge -> CADENCE_BACKDATED
  naive datetime -> MOMENT_NOT_AWARE
  inverted thresholds -> CADENCE_THRESHOLDS_INVERTED
…
  one deadline, two looks -> misses: [('2026-09-14T09:06:40+00:00', 100.0)]
```

The 240/300 boundaries are exact, the clock refuses to move backwards through either
entry point, a naive datetime is refused, and one deadline seen twice records one miss at
first notice. I could not make the clock forget a miss or accept an earlier moment.

**6. Poisoning the mint by quoting an id inside a receipt.**
`python3 probe/p15_minting_attacks.py` writes a body quoting `REC-20260914-ZZ` and
`REC-20260913-ZZZZ` and then mints twice more:

```
after quoting REC-20260914-ZZ: REC-20260914-A REC-20260914-AAA REC-20260914-AAB
any reuse: False
next_letter([])      : A
next_letter(['Z'])   : AA
next_letter(['AZ'])  : BA
next_letter(['ZZ'])  : AAA
next_letter(['B','A']): C
30 successive letters: A B C D E ... Z AA AB AC AD | all distinct: True
mint beside \xff\xfe\x80 -> REC-20260914-B
```

Quoting a high id burns letters but can never cause a reuse, because `next_letter` takes
the maximum rather than the first gap; the other date's `ZZZZ` is ignored; and an
undecodable byte beside the ids does not stop the mint, as `scan_receipt_ids`' docstring
promises. The only way I found to make the mint reuse a letter is B1 — a paragraph that
does not carry the id it was given.

---

## What I could not determine

* **Whether `tools/repo_activity.py` mis-parses the argv S6 builds.** The tool is not in
  this sandbox (the `os.path.isdir('tools')` check quoted in S6 prints `False`), so the
  wrapper's argv is all I executed. Which of the three plausible argparse shapes it uses,
  and therefore what the resulting activity record actually says, is unresolved.
  S6 reports the argv and nothing beyond it.
* **Whether `PREREGISTRATION_REQUIRED_SENTENCES` and `_PREREGISTRATION_BODY` reproduce
  section 8.** `design/design-s7-wave-plan.md` ends at its line 53, the bare heading
  `## 8. Pre-registration text for the ledger receipt`, with no body. Deviation 3 claims
  the wording and order of section 8 are preserved and only its blockquote marks dropped;
  I could not check that against anything, and `render_preregistration`'s assertion checks
  the module's constants against the module's own output, which is a tautology from
  outside. Unresolved.
* **Whether `C001_PLAN_ID` is the frozen value.** Line 196 says it is quoted from
  `experiments/diagnostics/C001-contrast-triple/PLAN.md`; that study is not in the
  sandbox, so the sha is unverified here. I did not treat this as a finding.
* **The Windows locking path** (N7): `msvcrt.locking` on a byte-0 region of an
  append-mode handle, including on a zero-length file. Not exercisable on this platform;
  I could not determine whether it gives the exclusion the POSIX path gives, and I am
  not asserting either answer.
* **`_refuse_secret`'s reach in a real run.** The scan sees only credentials whose values
  are in *this* process's environment under a name the transport treats as registered
  (`provider_openai_compat._ALWAYS_SECRET_ENVS`, which is
  `('DEEPSEEK_API_KEY', 'OLLAMA_API_KEY')`, plus the endpoint registry's `key_env` values
  and anything passed to `register_secret_envs`), at or above the 8-byte floor
  (`_MIN_SECRET_LENGTH = 8`). That is a property of
  `provider_openai_compat._secret_items`, not of this module, and it means "refused, not
  redacted" is a guarantee about declared credentials and not a proof that no credential
  reached the ledger. I did not open that as a finding against `receipts.py`, but a
  closing record that describes the ledger as credential-free would be overstating it.
* **Anything that needs the real ledger.** The module's first property is argued from
  `docs/DECISION_LEDGER.md` "mixing LF and CRLF line endings (37 CRLF lines at the time of
  writing)". That file is not in the sandbox, so I reproduced the mixed-ending case
  synthetically (probe 3 of "Tried, and could not break") rather than against the artifact
  the claim is about. The count of 37 is unverified here.
* **Coverage I did not attempt.** I did not exercise `erratum_receipt`,
  `outcome_receipt` or `close_receipt` beyond their shared `_follow_up` path; I did not
  attack `utc_stamp`/`_stamp` for locale or year-boundary behaviour; and I did not test
  behaviour on a ledger large enough for the whole-file read of deviation 1 to matter
  (the deviation says ~0.5 MB per receipt, which I did not measure).
* **No test module exists for this file in this snapshot.** `python3 run_tests.py` reports
  `Ran 0 tests in 0.000s`, so every "test that would hold the repair" above is a test to
  be written, not an existing one to be extended.
