# Adversarial review — W0-CUSTODY (`src/minireason/loop/custody.py`)

Scope: pin computation and verification (`pins`, `verify_pins`, `_pin_key`,
`_pinned_path`), the digest helpers (`sha256_bytes`, `sha256_path`, `encoded`,
`digest`), write-once writes (`write_new`, `_fsync_directory`), and path fencing
(`fenced`), reviewed against what the module claims of itself — its own
docstrings, the integrator's entries in `notes/WAVE0-INTERFACE.md` (§4, and O6/O8
where they touch custody), and the W0-CUSTODY acceptance clause in
`design/design-s7-wave-plan.md`.

Method. Every finding below was executed against the frozen sandbox copy. All
probes live in `probe/` and run as `python3 probe/<name>.py`; each adds `src` to
`sys.path` itself and works only in `tempfile` space; every environment variable a
probe sets is removed or restored before the probe exits, confirmed by a printed
scrub line. Probe results print `RESULT PASS|FAIL|NOTE` lines and are quoted
verbatim. The module under review was not edited, and nothing under `src/` was
touched.

The acceptance clause being reviewed against, quoted from
`design/design-s7-wave-plan.md`, W0-CUSTODY entry:

> "acceptance":"A one-byte change to any pinned file is detected and named; a
> path escaping the run root is refused; write_new refuses an existing path and
> refuses credential-bearing content; verify_pins is pure and order-stable."

Findings are ordered BLOCKER, SHOULD-FIX, NOTE. Nothing is scored or ranked.

---

## BLOCKER — none reproduced

No published seam was reproduced as unsound and no pre-registered guard was
reproduced as failing to fire. Each guard the acceptance clause names fired in
its advertised direction when attacked directly (see "Tried, and could not
break"): the one-byte change is detected and named; a path escaping the run root
is refused, including the symlink and sibling-prefix constructions a text-prefix
fence would miss; `write_new` refuses an existing path and refuses content
carrying any of the scanned credentials, in raw and JSON-escaped renderings;
`verify_pins` is pure and order-stable; the three-way digest identity
(`custody.digest == provider_openai_compat.digest == sha256_hex(canonical_json)`)
holds on all six fixtures including the non-ASCII one a non-UTF-8 canonical form
would lose. The four findings below are weaknesses around the seams, not
unsoundness in them.

---

## SHOULD-FIX 1 — the write-once existence pre-check runs after the credential scan: a TOCTOU window, and on that path the named refusal leaves a file behind

**Claim.** In `write_new`, the existence pre-check (`target.exists() or
target.is_symlink()`) executes after the credential scan rather than before it,
opening a check-to-open window; and if the target is created inside that window,
the function raises `WriteOnceViolation` while the intruder's bytes remain on
disk at the same named path — contradicting "nothing was written or accepted"
and the leave-nothing-behind claim on the very path the caller's `except
FileExistsError` handlers treat as safe to proceed past.

**Location.** `src/minireason/loop/custody.py:384-391` (the ordering), with the
contradicted sentence at :177 and :368-371.

**Contradicted text.**

- `CustodyMismatch` docstring (:177): "Custody failed under a named code;
  **nothing was written or accepted.**"
- `write_new` docstring: "The credential scan runs **before anything is
  created**, so a refused write leaves no file and no parent directory behind."

The second sentence is written for the credential-refusal path and holds there
(NOTE 4). But the same function's existence-refusal path is also a
`CustodyMismatch`, and a refusal raised from it with the target still on disk
breaks the first sentence. `WriteOnceViolation` deliberately inherits
`FileExistsError` (:209-214), so every caller written against `open('xb')` — the
transport's own `_open_record` catches `FileExistsError` and proceeds on the
assumption the path is someone else's problem — walks away from a violation
while the bytes that triggered it stay put.

**Mechanism.** The order is: build `raw` (:384), scan it (:386-388), *then*
check existence (:389-390), then `open('xb')` (:392-395). The `open('xb')` guard
itself cannot be raced (p06 shows one writer winning, one refused), but the
pre-check above it can: anything that creates the path between the scan and the
check is never seen by the check's intended moment, `write_new` raises
`WriteOnceViolation`, and the raising call performs no cleanup — the class
docstring's promise is left for someone else to keep. The window exists only
because the scan precedes the check; scan-first buys nothing the
check-first-then-scan order would not also give (a refused credential write
still creates nothing; check-first merely refuses earlier).

**Probe.** `python3 probe/p07_toctou_proof.py` — the scan function is wrapped
at the caller level (the module under review is untouched) so the target is
created by a third party while the module is executing its own scan; the
existence pre-check then fires late, the exception raises, and the intruder's
bytes are what remains. Printed verbatim:

```
RESULT NOTE defender thread: WriteOnceViolation WRITE_ONCE_VIOLATION
RESULT FAIL after a WriteOnceViolation raised on the TOCTOU path, the named path exists: True | bytes there: b'intruder-created content'
RESULT NOTE the violation was raised; the intruder's bytes are what remains. An existence-first order would have raised before the intruder could exist; a fail-closed order raises only after it no longer exists.
```

**Repair.** Two cheap changes, either sufficient, both defensible:

1. Move the existence check to *before* the credential scan (scan after
   existence is known-clear). This preserves "a refused write leaves nothing
   behind" for both refusal kinds and shrinks the window to the one `open('xb')`
   already closes; and
2. In the `except FileExistsError` path (:394-395), unlink the pre-existing
   target before raising when it can be named, so a refusal does not leave the
   very bytes it named behind.

**Holding test.** A test that monkeypatches nothing under `src/`: create the
target between `credential_names_in` and the existence check by substituting a
scan wrapper at the *caller* level (as p07 does), assert the exception, then
assert `not target.exists()`. A plain version: attempt `write_new` to a path in
a directory another thread populates mid-call, and assert no refusal leaves the
target present.

---

## SHOULD-FIX 2 — `verify_pins` accepts, and `pins` names, a non-string pin-map key instead of refusing it as malformed

**Claim.** `_pin_key`'s `str(entry)` coercion turns any non-string pin key into
a plausible-looking path key, so `verify_pins` reports a custody finding rather
than a malformation, and `pins` silently accepts a non-string entry. The
published signature is `verify_pins(plan: Mapping[str, Any], ...)`; a plan body
loaded from JSON cannot carry a non-string key, but the module's own stated
reason for requiring the `pins` envelope is to refuse exactly this species of
silent misreading.

**Location.** `src/minireason/loop/custody.py:427` (`text =
str(entry).replace("\\", "/")`), consumed by `_pin_key` at :420-436,
`pins` at :463, `verify_pins` at :513-515.

**Contradicted text.** `verify_pins` docstring (:497-499), the module's stated
reason for refusing bare maps:

> "a plan body whose values all happened to be strings would be verified as a
> pin map, which is **the sort of silent misreading this module exists to
> refuse**."

A non-string key is the same misreading at the key position: `7` is not a path
anyone pinned, yet it is coerced to `"7"` and reported as
`SOURCE_PIN_MISSING` — a custody *finding*, indistinguishable in the receipt
from a real missing file, and attached to a path string that was never in the
plan. A halt keyed on this finding would name a file that was never pinned.

**Probe.** `python3 probe/p08_nonstring_key.py`, verbatim:

```
RESULT FAIL non-string key: verified with no complaint: [CustodyFinding(code='SOURCE_PIN_MISSING', path='7', expected='0000000000000000000000000000000000000000000000000000000000000000', observed=None)]
RESULT NOTE mixed map findings: [{'code': 'SOURCE_PIN_MISSING', 'path': '7', ...}]
RESULT PASS key equal to the envelope's own name: ['SOURCE_PIN_MISSING']
RESULT PASS pins([7]): CustodyMismatch SOURCE_PIN_MISSING | detail: SOURCE_PIN_MISSING: 7
```

The first line is the defect: a non-string key produces no `CustodyMismatch`
(the "FAIL" is the probe's verdict that an *expected refusal* did not fire), and
the finding it does produce mislabels the malformation as a missing file.

**Repair.** In `_pin_key`, refuse a non-string `entry` outright: `if not
isinstance(entry, (str, Path)): raise CustodyMismatch("SOURCE_PIN_MALFORMED",
repr(entry))` before the `str()` coercion. (Passing `repr(entry)` keeps the
detail a printable string without minting a path.)

**Holding test.** `verify_pins({"pins": {7: "0"*64}}, repo)` raises
`CustodyMismatch` with code `SOURCE_PIN_MALFORMED`; `pins(repo, [7])` raises the
same. Add the symmetric `CustodyFinding.code == "SOURCE_PIN_MALFORMED"` path for
`verify_pins` over the mixed map.

---

## NOTE 3 — `verify_pins` accepts a `./`-prefixed pin key that `pins` cannot produce, and two spellings of one key silently collapse at freeze time

**Claim.** `_pin_key` canonicalises a `./`-prefixed relative key to a bare key
but only refuses `""`/`"."` exactly, so a nominal asymmetry appears: under the
strict caller contract `pins` would emit only the bare key, yet
`verify_pins({"pins": {"./src/a.py": sha}}, repo)` verifies clean under the bare
spelling. Separately, when two entries spell one physical file (`src\a.py` and
`src/a.py`), `pins` emits one entry with no signal that a duplicate was
collapsed.

Neither is a custody failure — the file checked is the pinned file in every
case, and deviation 2 (:69-72) documents the POSIX canonicalisation as
deliberate, quoting "REC-20260913-I" as the cross-host motivation. But two
things follow that the module does not say:

1. A plan whose pin map was built by a *different* tool with literal `./`-keys
   verifies here without ever being flagged, so a verifier reading the plan body
   sees keys the strict caller would never have produced by hand. The wave
   plan's acceptance is silent on this; the module that "refuses silent
   misreadings" (SHOULD-FIX 2's quote) silently normalises this one.
2. Collapsing two spellings of one file into one pin sits opposite the
   interface note for `CustodyReport.from_findings` ("does not de-duplicate"):
   where the receipt deliberately keeps two findings for two moved files, the
   freeze keeps one pin for two spelled entries. A caller that pinned
   `["src/b.py", "src\a.py"]` intending two distinct files and made a typo gets
   one pin and no notice.

**Location.** `_pin_key` (:427, :434); the collapse surface at `pins` :463-470;
the acceptance entry it shades is `design/design-s7-wave-plan.md` W0-CUSTODY
("verify_pins is pure and order-stable") — which it satisfies; the note is about
the key space, not the order.

**Probe.** `python3 probe/p06_race_and_torture.py`, verbatim:

```
RESULT PASS two spellings of one key collapse silently: entries in: 2 entries out: 1
RESULT PASS verify_pins accepts the './' spelling pins() refuses: []
RESULT PASS both spellings in one plan: key after canonicalisation is ['src/a.py']
```

And from `python3 probe/p03_pins_verify.py`:

```
RESULT PASS duplicate entry under './' collapses to one key: ['src/a.py']
```

**Repair.** Document the normalisation of `./` in the deviation-2 paragraph
(alongside the separator sentence) so the acceptance is stated, or refuse
`"./"`-prefixed keys at verification as `SOURCE_PIN_MALFORMED` and let `pins`
keep emitting canonical keys only. For the collapse: have `pins` raise
`CustodyMismatch("SOURCE_PIN_MALFORMED", name)` (or a new code) when a computed
key is already present in `out`, since a freeze-time duplicate is a caller error
a freeze should name rather than absorb.

**Holding test.** `pins(repo, ["src\\a.py", "src/a.py"])` raises; and either
`verify_pins` refuses `{"./src/a.py": sha}` or a docstring test greps the module
for the sentence that says it is accepted.

---

## NOTE 4 — the credential scan is a substring scan over two renderings only; a transformed credential (base64, halved) is written to disk

**Claim.** `credential_names_in` searches each scanned credential's raw UTF-8
spelling and its `json.dumps`-escaped spelling, and nothing else. A credential
encountered in any other encoding — hex, base64, split across an inserted
separator — is written verbatim by `write_new` with no refusal.

This is fully documented behaviour, reported as a finding only so the review
does not imply the guard is a detector: the transport's own docstring states the
bound ("known to this process", the `_MIN_SECRET_LENGTH` floor, the two
renderings) and O8 states the analogous bound for the publish scan ("it can only
see credentials present in *this process's* environment ... not a proof that no
credential is present"). The scan's purpose is that an *accidentally embedded*
live credential refuses the write (which the probes show it does, in both
renderings, with no bytes left behind); it is not, and is not claimed to be, a
proof that written records carry no credential material. A reader downstream of
this module should not read a clean scan as the latter.

**Location.** `credential_names_in` (:308-332): the decode at :316
(`bytes(raw).decode("utf-8", "surrogateescape")`), the two renderings at :322
(`value in text or json.dumps(value)[1:-1] in text`), and the transport's
`redact_with_names` at :327-328, which inherits the same two-renderings bound
from `provider_openai_compat._renderings`.

**Contradicted text.** None — the module claims no more than it does. The
boundary sentences are: `provider_openai_compat` module docstring ("a value
shorter than :data:`_MIN_SECRET_LENGTH` (8) characters is **not** treated as a
credential at all"), and `notes/WAVE0-INTERFACE.md` O8 ("the scan covers the
credentials this process could see — not a proof that no credential is
present").

**Probe.** `python3 probe/p04_credential_scan.py`, verbatim (the two FAIL lines
are the probe asserting its own strict expectation — that *no* credential-shaped
bytes land — against a guard that never promised it):

```
RESULT FAIL base64 of the value WRITE SUCCEEDED; on disk: b'c2stZmFrZXByb2JlLTlmOGU3ZDZjNWI0YTM='
RESULT FAIL value split across halves WRITE SUCCEEDED; on disk: b'sk-fakeprobe- ... 9f8e7d6c5b4a3'
```

For contrast, the refusals that did fire:

```
RESULT PASS raw value in bytes refused as CREDENTIAL_IN_OUTPUT | value names in detail: DEEPSEEK_API_KEY | file leaked on disk: False | orphan parent left: False
RESULT PASS JSON-escaped value refused as CREDENTIAL_IN_OUTPUT | ...
RESULT PASS custom registered value refused as CREDENTIAL_IN_OUTPUT | value names in detail: PROBE_CUSTOM_CREDENTIAL | ...
RESULT PASS value below the 8-char floor is not searched: []
```

**Repair.** None in this module — widening a substring scan toward decoded
forms has false-positive teeth, and the declared bound is the correct place to
stop. The repair belongs to the downstream reader: the closing record should
repeat O8's sentence about custody-side writes too ("the scan covers the scanned
credentials' raw and JSON-escaped renderings"), mirroring the recommendation O8
already makes for publish.

**Holding test.** A docstring test asserting the boundary sentence is present in
`write_new`'s documentation — the failure mode to guard is a future wave citing
`write_new`'s refusal as a no-credential-material proof.

---

## Tried, and could not break

Attacks executed against the module that failed, recorded as evidence about it.
Each line is a probe verdict; full output is in the per-probe transcripts.

1. **Write-once overwrite, in all three target states** (`p01`): existing
   regular file, existing directory, and a dangling symlink at the target each
   raised `WriteOnceViolation` (code `WRITE_ONCE_VIOLATION`), and the refusal
   object carries no smuggled payload in `exc.args`.
   ```
   RESULT PASS dangling symlink: WriteOnceViolation code= WRITE_ONCE_VIOLATION
   RESULT NOTE refusal object args: ('WRITE_ONCE_VIOLATION: ...',) | refused value reachable from exception state: False
   ```

2. **The write-once race** (`p06`): two threads racing `write_new` on one path
   produced exactly one success and one named refusal, with the winner's bytes
   on disk — the `open('xb')` core cannot be raced; only the pre-check above it
   can (SHOULD-FIX 1).
   ```
   RESULT PASS racing writers: ['a: wrote', 'b: refused'] | final bytes: b'a-payload'
   ```

3. **Fence escapes** (`p02`): literal `..`, mid-path `..`, an absolute path
   outside, a `..` threaded through a mid-path symlink, a symlink pointing
   outside, and the `/tmp/run` vs `/tmp/run-evil` sibling prefix that a
   text-prefix fence would admit — all refused with `PATH_ESCAPES_RUN_ROOT`.
   The fence's resolve-then-contain check is component-wise, not prefix-wise:
   ```
   RESULT PASS symlink pointing outside -> refused code= PATH_ESCAPES_RUN_ROOT ...
   RESULT PASS sibling sharing the name prefix -> refused code= PATH_ESCAPES_RUN_ROOT detail= .../run-evil/loot.txt
   ```

4. **Pin verification** (`p03`): a one-byte flip is `SOURCE_PIN_MISMATCH` naming
   the path with both digests; deletion is `SOURCE_PIN_MISSING`; a directory at
   the pinned path is `SOURCE_PIN_NOT_A_FILE`; a non-string, uppercase or null
   digest is `SOURCE_PIN_MALFORMED`; a `..` key or an absolute-outside key is
   `SOURCE_PIN_OUTSIDE_REPOSITORY`; permuting the map changes nothing; a second
   call returns identical findings with the plan untouched; a bare
   `{path: sha}` map is refused as `PIN_MAP_MISSING`; a backslash-spelled key
   verifies clean and a mismatch under one is named under the POSIX key
   (deviation 2 doing its documented work).

5. **Digest identity, decision 7** (`p05`): on all six fixtures —
   nested-with-unicode, the non-ASCII identity char (U+FFE9),
   booleans/numbers, an empty list, a bare string, a float —
   `custody.digest(v) == provider_openai_compat.digest(v) ==
   sha256_hex(canonical_json(v))`, `canonical_json(v)` is byte-identical to the
   compact form `digest` hashes, `encoded`'s record form round-trips to the same
   digest, and `encoded` genuinely differs (indent + trailing newline) so the
   claimed two-forms distinction is not vacuous. `MIN_CREDENTIAL_LENGTH ==
   provider_openai_compat._MIN_SECRET_LENGTH == 8`; `CUSTODY_CODES` is a sorted
   9-member slice of `types.FAILURE_CODES`; the exception hierarchy matches the
   interface (a `LoopError` keeping `ValueError`/`FileExistsError`).

6. **Credential scan robustness** (`p06`): non-UTF-8 payload bytes neither crash
   the scan (the `surrogateescape` decode holds) nor get altered on write
   (bytes verbatim); a quote-bearing credential is caught in its JSON-escaped
   rendering; a NUL-bearing credential cannot be planted through this probe
   vector because `os.environ` itself refuses it
   (`ValueError: embedded null byte` — recorded as the boundary, not assumed).
   ```
   RESULT PASS credential_names_in over non-UTF-8 bytes returns: []
   RESULT NOTE os.environ refuses a NUL-bearing value itself: ValueError - embedded null byte
   RESULT PASS JSON-escaped rendering of a quote-bearing key is caught: ['DEEPSEEK_API_KEY']
   ```

7. **Root-as-target and internal `..`** (`p09`): `fenced(root, "")` returns the
   resolved root and `write_new` at it succeeds — which the layout needs
   (`plan.json` is written at the root); an internal `a/../b` that would resolve
   back inside is still refused outright, a conservatism deviation 3 states in
   as many words.

## Sandbox state, and limits of this review

- `python3 run_tests.py` (discovery over `tests/`) ran 0 tests: the frozen
  sandbox snapshot ships `tests/__init__.py` and `tests/loop/__init__.py` but no
  `test_custody.py`, so the wave-0 unit suite is not in this copy and nothing
  here is a verdict on it. Counts reported with their command: `python3
  run_tests.py` → "Ran 0 tests in 0.000s, OK".
- Probes ran against `src/` on `sys.path` as `run_tests.py` arranges; all file
  effects were confined to `tempfile` space and all env changes scrubbed (each
  probe prints its scrub line).
- Suspected and not reproduced: a race on the `open('xb')` core (fails, item 2);
  a fence bypass via sibling prefix (fails, item 3); digest divergence on
  non-ASCII (fails, item 5). The E028-adjacent question — whether a repaired
  *pinned module* invalidates a live `loop_plan_id` — is out of this sandbox's
  reach (no driver, no frozen plan here) and is left unresolved rather than
  asserted.
