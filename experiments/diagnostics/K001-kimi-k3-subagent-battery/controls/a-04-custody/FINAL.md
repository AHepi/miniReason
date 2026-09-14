# Adversarial review — `src/minireason/loop/custody.py` (W0-CUSTODY)

Read first: `notes/WAVE0-INTERFACE.md` §4, `src/minireason/loop/__init__.py`
("Conventions a later wave must not re-invent"), `design/design-s7-wave-plan.md`
(the `W0-CUSTODY` acceptance string), `design/design-s2-roles-and-guard.md` §2.4,
`src/minireason/loop/types.py` (the only sibling custody imports), and
`src/minireason/provider_openai_compat.py` (the transport custody derives its
credential-name set from).

Everything below was executed. The probes live in `probe/` and each is run as
`python3 probe/<name>.py` from the sandbox root; `probe/_boot.py` puts the
sandbox root and `src` on `sys.path` and nothing else, exactly as `run_tests.py`
does. `tests/loop/` in this sandbox contains only `__init__.py` — there is no
`tests/loop/test_custody.py` here, and `python3 run_tests.py` reports
`Ran 0 tests in 0.000s`, so nothing below is a report of an existing test
failing. Python is 3.11.15 (`probe/p05_seam_with_types.py`, first line). Every
probe builds its own `tempfile.TemporaryDirectory`, so the `/tmp/tmpXXXX` paths
in the transcripts below differ from run to run; everything else is stable, and
all twelve probes were re-run to completion after the review was written.

Findings are ordered BLOCKER, SHOULD-FIX, NOTE, as the brief requires. The
order inside each class is the order I found them in and carries no further
meaning.

---

## BLOCKER 1 — the documented `write_new(fenced(root, rel), value)` pairing writes *through* a symlink, so a record lands at a coordinate the caller never named

**Claim.** `fenced` returns the fully symlink-resolved path, so by the time
`write_new` sees it there is no symlink left for `write_new`'s own
`target.is_symlink()` refusal to catch. On the call shape the package
publishes, a step receipt is written into whatever inside-the-root path a
pre-existing symlink points at, and the real owner of that path is then refused
as already spent.

**Where.** `src/minireason/loop/custody.py:335-362` (`fenced`, in particular the
`resolved = target.resolve()` / `return resolved` at 359 and 362) interacting
with `src/minireason/loop/custody.py:389-390` (`write_new`'s
`if target.exists() or target.is_symlink():`).

**What it contradicts.** `src/minireason/loop/__init__.py`, "Conventions a later
wave must not re-invent":

> **``custody.write_new(path, value)`` does not fence.**  Its signature carries
> no root, so a caller writing under the run root passes
> ``write_new(fenced(run_root, relative), value)``.  ``write_new`` refuses an
> existing path and refuses credential-bearing bytes; ``fenced`` refuses a path
> that escapes the root.  They are two guards and both are needed.

and `custody.write_new`'s own first line
(`src/minireason/loop/custody.py:368`):

> Write VALUE to PATH once.  An existing path is a custody failure.

`design/design-s2-roles-and-guard.md` §2.4 G11 is the clause that rests on this
mechanism — "**Enforced by refusing the write**, not by a convention" — and
`WAVE0-INTERFACE.md` §4 publishes `write_new` with the annotation
`# does NOT fence; pair with fenced()`.

**Probe.** `python3 probe/p12_fence_disarms_symlink_refusal.py`. It builds
`experiments/loops/RUN-0001/` with `steps/` and `cycles/0/`, plants a symlink at
`steps/0001-S0.json` pointing at `cycles/0/decision.json` (still inside the run
root, so the fence has no reason to refuse), then writes one step receipt both
ways. Verbatim:

```
named coordinate is a symlink     : True
write_new(raw path)               : WRITE_ONCE_VIOLATION
fenced(run_root, 'steps/0001-S0.json'): /tmp/tmpwn4uzg2k/experiments/loops/RUN-0001/cycles/0/decision.json
write_new(fenced(...))            : WROTE
bytes at the named coordinate     : b'{\n  "step": "0001-S0"\n}\n'
bytes at cycles/0/decision.json   : b'{\n  "step": "0001-S0"\n}\n'
steps/0001-S0.json is still a symlink, not a file: True /tmp/tmpwn4uzg2k/experiments/loops/RUN-0001/cycles/0/decision.json
write_new(cycles/0/decision.json) : WRITE_ONCE_VIOLATION /tmp/tmpwn4uzg2k/experiments/loops/RUN-0001/cycles/0/decision.json
```

The first line of that pair is the guard the module advertises firing on the raw
path. The second is the same write, through the fence the package tells callers
to use, succeeding — and the last line is the cycle decision record being
refused because the step receipt is already sitting in its coordinate. A
symlink inside the run tree is inside the module's own declared threat model:
`fenced`'s docstring (`custody.py:341-342`) names "an intermediate symlink
pointing away" as the thing resolution catches.

**Repair.** `write_new` should decide against the path it was handed, not
against a path something else already resolved. Two changes, either of which
closes it, both of which are cheap:

1. In `write_new`, refuse a symlink anywhere in the target's own spelling before
   writing — `if target.is_symlink() or any(p.is_symlink() for p in target.parents ...)`
   is the heavy version; the light version is `os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW)`,
   which is atomic against the final component and raises `ELOOP`/`OSError` to
   be re-raised as `WriteOnceViolation`.
2. In `fenced`, return the *un-resolved* `target` after checking that
   `target.resolve()` is inside `resolved_root`, so the caller writes at the name
   it asked for and `write_new`'s `is_symlink()` check still has a symlink to see.
   This keeps the fence's guarantee (the escape check still runs on the resolved
   form) and restores the second guard.

**Test that would hold the repair.** In `tests/loop/test_custody.py`:

```python
def test_write_new_through_the_fence_refuses_a_planted_symlink(self):
    run_root = self.tmp / "experiments" / "loops" / "RUN-0001"
    (run_root / "steps").mkdir(parents=True)
    (run_root / "cycles" / "0").mkdir(parents=True)
    os.symlink(run_root / "cycles" / "0" / "decision.json",
               run_root / "steps" / "0001-S0.json")
    gate = custody.fenced(run_root, "steps/0001-S0.json")
    with self.assertRaises(custody.WriteOnceViolation) as caught:
        custody.write_new(gate, {"step": "0001-S0"})
    self.assertEqual(caught.exception.code, "WRITE_ONCE_VIOLATION")
    self.assertFalse((run_root / "cycles" / "0" / "decision.json").exists())
```

---

## BLOCKER 2 — a pin digest with a trailing newline is reported as `SOURCE_PIN_MISMATCH`, a statement about the tree that is false

**Claim.** `_SHA256` is anchored with `$`, which in Python matches before a
single trailing newline. A pin value of `<64 hex>\n` therefore passes the
well-formedness gate, is compared against the observed digest (which has no
newline), and is reported as `SOURCE_PIN_MISMATCH` with `expected` and
`observed` both filled in — the finding says the pinned file moved when the file
is byte-for-byte unchanged and the plan is the thing that is malformed. The
same value is `PIN_INVALID` to `types.loop_plan_id`, the function that folded
those pins into the plan identity in the first place.

**Where.** `src/minireason/loop/custody.py:173`
(`_SHA256 = re.compile(r"^[0-9a-f]{64}$")`), used at
`src/minireason/loop/custody.py:517-519`.

**What it contradicts.** `verify_pins`' own first line
(`src/minireason/loop/custody.py:491`):

> Re-read every pinned file and report, by name, each one that moved.

and the module docstring's deviation 1
(`src/minireason/loop/custody.py:61-68`), whose whole justification for
reporting rather than raising is naming precision — the frozen-plan drivers
"cannot say which file moved". A `SOURCE_PIN_MISMATCH` carrying
`observed != expected` for an unchanged file is exactly a custody fact that is
not true. `types.py:483` spells the same shape `_HEX64 = re.compile(r"[0-9a-f]{64}\Z")`
and `types.py:584` applies it with `fullmatch`, so the two halves of the pin
seam disagree.

**Probe.** `python3 probe/p05_seam_with_types.py`. It writes one real file,
computes its real digest, and hands each spelling to both `custody.verify_pins`
and `types.loop_plan_id` (with a valid `LoopConfig` mapping). Verbatim, the
first three cases:

```
digest + trailing \n
  verify_pins(digest + trailing \n        ) -> [('SOURCE_PIN_MISMATCH', 'src/a.py')]
  loop_plan_id(digest + trailing \n        ) -> PIN_INVALID: pins['src/a.py'] must be a lowercase sha256 hex digest
digest + trailing space
  verify_pins(digest + trailing space     ) -> [('SOURCE_PIN_MALFORMED', 'src/a.py')]
  loop_plan_id(digest + trailing space     ) -> PIN_INVALID: pins['src/a.py'] must be a lowercase sha256 hex digest
UPPERCASE digest
  verify_pins(UPPERCASE digest            ) -> [('SOURCE_PIN_MALFORMED', 'src/a.py')]
  loop_plan_id(UPPERCASE digest            ) -> PIN_INVALID: pins['src/a.py'] must be a lowercase sha256 hex digest
```

A trailing space and an uppercase digest are named correctly; only the trailing
newline slips through the shape gate and is renamed a mismatch. `python3
probe/p04_pins.py` shows the resulting finding in full, and shows the two
regexes disagreeing on the same string:

```
trailing-newline digest: [{'code': 'SOURCE_PIN_MISMATCH', 'path': 'src/minireason/a.py', 'expected': '2c8b08da5ce60398e1f19af0e5dccc744df274b826abe585eaba68c525434806\n', 'observed': '2c8b08da5ce60398e1f19af0e5dccc744df274b826abe585eaba68c525434806'}]
custody._SHA256 match  : True
types._HEX64 fullmatch : False
```

This is not a hypothetical spelling: a pin map assembled by reading a
`.sha256` sidecar file, or by a shell capture, carries the trailing newline by
default, and `custody.sha256_path` is documented (`custody.py:249-252`) against
exactly that class of line-ending accident.

**Repair.** `_SHA256 = re.compile(r"[0-9a-f]{64}\Z")` and use `fullmatch`,
matching `types._HEX64` verbatim; better still, import the shape from `types`
so there is one owner, as the package's "Shared constants have one owner" rule
asks. Nothing else changes: the value then falls to `SOURCE_PIN_MALFORMED`,
which is already a member of `CUSTODY_CODES`.

**Test that would hold the repair.**

```python
def test_a_pin_digest_with_trailing_whitespace_is_malformed_not_a_mismatch(self):
    real = custody.sha256_path(self.pinned)
    for suffix in ("\n", "\r\n", " ", "\t"):
        with self.subTest(suffix=suffix):
            found = custody.verify_pins({"pins": {"src/a.py": real + suffix}}, self.repo)
            self.assertEqual([f.code for f in found], ["SOURCE_PIN_MALFORMED"])
            self.assertIsNone(found[0].observed)

def test_custody_and_types_agree_on_what_a_pin_digest_is(self):
    real = custody.sha256_path(self.pinned)
    for spelling in (real + "\n", real + " ", real.upper(), "0" * 63, "0" * 65):
        with self.subTest(spelling=spelling):
            custody_ok = bool(custody._SHA256.fullmatch(spelling))
            types_ok = bool(loop_types._HEX64.fullmatch(spelling))
            self.assertEqual(custody_ok, types_ok)
```

---

## BLOCKER 3 — `verify_pins`, `pins`, `fenced` and `write_new` let unnamed non-`LoopError` exceptions out, on inputs the plan body and the tree control

**Claim.** `verify_pins` says it raises only `CustodyMismatch("PIN_MAP_MISSING")`.
It demonstrably also raises `ValueError` (a NUL in a pin key), `OSError`
(`ENAMETOOLONG` on a long pin key) and `RuntimeError` (a symlink loop under the
repo). None of those carries a `.code`, so the halt receipt design 4.4 requires
has nothing to record, and `except LoopError` — the package's published single
catch — does not catch any of them. `fenced` and `write_new` leak the same way.

**Where.** `src/minireason/loop/custody.py:358-359` (`root_path.resolve()` /
`target.resolve()` inside `fenced`), reached from
`src/minireason/loop/custody.py:439-445` (`_pinned_path`), from
`src/minireason/loop/custody.py:462-469` (`pins`) and from
`src/minireason/loop/custody.py:520-523` (`verify_pins`); and
`src/minireason/loop/custody.py:391` (`target.parent.mkdir(...)` in
`write_new`).

**What it contradicts.** `verify_pins`' docstring
(`src/minireason/loop/custody.py:503-505`):

> Raises only :class:`CustodyMismatch` ``PIN_MAP_MISSING``, for a
> plan that carries no pin map at all, which is a caller error rather than a
> custody fact.

the module docstring's 4.4 paragraph (`src/minireason/loop/custody.py:29-32`):

> **4.4** - *"Custody failure halts and records ... The loop never works
> around custody."*  Every check here either raises a :class:`CustodyMismatch`
> carrying a named code or reports one as a :class:`CustodyFinding`

`pins`' docstring (`src/minireason/loop/custody.py:455-457`), which names three
codes and no other outcome; and `CustodyMismatch`'s own docstring
(`custody.py:182-184`): "``failure_code`` in ``tools/contrast_triple_study.py``
reads ``.code`` off an exception, so a halt receipt gets the code without
parsing the message."

**Probe.** `python3 probe/p06_verify_pins_escapes.py`. Verbatim (the long-key
line is truncated here only at the repeated `x`s; the probe prints it in full):

```
euid: 0
NUL in a pin key                         ESCAPED ValueError: embedded null byte (is LoopError: False, has .code: False)
key of 5000 chars                        ESCAPED OSError: [Errno 36] File name too long: '/tmp/tmpu1kneqc9/xxxxxxxx…' (is LoopError: False, has .code: False)
key is a FIFO (made)                     returned [('SOURCE_PIN_NOT_A_FILE', 'fifo')]
symlink loop                             ESCAPED RuntimeError: Symlink loop from '/tmp/tmpu1kneqc9/l1' (is LoopError: False, has .code: False)
integer pin key                          returned [('SOURCE_PIN_MISSING', '1')]
None pin key                             returned [('SOURCE_PIN_MISSING', 'None')]
fenced NUL                               ESCAPED ValueError: embedded null byte (is LoopError: False)
fenced symlink loop                      ESCAPED RuntimeError: Symlink loop from '/tmp/tmpu1kneqc9/l1' (is LoopError: False)
write_new parent is a file               ESCAPED FileExistsError: [Errno 17] File exists: '/tmp/tmpu1kneqc9/src/a.py' (is LoopError: False)
write_new into a symlink loop            ESCAPED FileExistsError: [Errno 17] File exists: '/tmp/tmpu1kneqc9/l1' (is LoopError: False)
```

`python3 probe/p05_seam_with_types.py` reaches the same `RuntimeError` through
`pins` as well:

```
fenced(repo,'loopa')         ESCAPED RuntimeError: Symlink loop from '/tmp/tmpnoy5a8x7/loopa'
pins(repo,['loopa'])         ESCAPED RuntimeError: Symlink loop from '/tmp/tmpnoy5a8x7/loopa'
verify_pins loopa            ESCAPED RuntimeError: Symlink loop from '/tmp/tmpnoy5a8x7/loopa'
```

Two of these are entirely under the plan body's control and are expressible in
JSON: `"src/\u0000a.py"` is a legal JSON object key, and so is a 5000-character
one. The `ValueError` case is the sharpest, because `CredentialInOutput`
inherits `ValueError` precisely so that "callers written against the drivers'
``ValueError('CREDENTIAL_IN_OUTPUT')`` keep working"
(`custody.py:198-199`) — such a caller reads a NUL-bearing pin key as a
credential leak.

**Repair.** Wrap the two `resolve()` calls in `fenced` and the `mkdir` in
`write_new` so that an `OSError`, `RuntimeError` or `ValueError` from the
filesystem layer becomes the named refusal the module already owns:

```python
try:
    resolved_root = root_path.resolve()
    resolved = target.resolve()
except (OSError, RuntimeError, ValueError) as exc:
    raise CustodyMismatch("PATH_ESCAPES_RUN_ROOT", text) from exc
```

and in `write_new`:

```python
try:
    target.parent.mkdir(parents=True, exist_ok=True)
except (FileExistsError, NotADirectoryError) as exc:
    raise WriteOnceViolation("WRITE_ONCE_VIOLATION", str(target.parent)) from exc
except OSError as exc:
    raise CustodyMismatch("PATH_ESCAPES_RUN_ROOT", str(target)) from exc
```

Whether an unresolvable path deserves `PATH_ESCAPES_RUN_ROOT` or a tenth code is
a judgement for the module's owner; what matters is that the refusal is named
and is a `LoopError`, since `CUSTODY_CODES` is published as "every code this
module can name" (`custody.py:145-147`).

**Test that would hold the repair.**

```python
def test_every_refusal_this_module_makes_is_a_named_LoopError(self):
    os.symlink(self.repo / "l2", self.repo / "l1")
    os.symlink(self.repo / "l1", self.repo / "l2")
    cases = [
        lambda: custody.fenced(self.repo, "a\x00b"),
        lambda: custody.fenced(self.repo, "l1"),
        lambda: custody.pins(self.repo, ["l1"]),
        lambda: custody.verify_pins({"pins": {"a\x00b": "0" * 64}}, self.repo),
        lambda: custody.verify_pins({"pins": {"x" * 5000: "0" * 64}}, self.repo),
        lambda: custody.write_new(self.repo / "file.txt" / "k.json", {"k": 1}),
    ]
    for index, case in enumerate(cases):
        with self.subTest(index=index):
            with self.assertRaises(LoopError) as caught:
                case()
            self.assertIn(caught.exception.code, custody.CUSTODY_CODES)
```

---

## SHOULD-FIX 1 — the credential guard narrows to two names, silently, whenever the transport is missing or its helper raises

**Claim.** Both derivations of the credential-name set are wrapped in bare
`except Exception:` arms that pass. When the transport is not importable, or
when `_secret_env_names()` raises, `scanned_credential_envs()` silently falls
back to `ALWAYS_SCANNED_ENVS` and a record carrying a credential from any other
registered name is written, with no code, no finding, and nothing in the record
saying the scan was narrowed.

**Where.** `src/minireason/loop/custody.py:283-287` (`_provider_module`'s
`except Exception: return None`), `src/minireason/loop/custody.py:301-305`
(`scanned_credential_envs`' `except Exception: pass`) and
`src/minireason/loop/custody.py:324-329` (`credential_names_in`'s
`except Exception: pass`).

**What it contradicts.** `scanned_credential_envs`' docstring
(`src/minireason/loop/custody.py:293-296`):

> Derived, never guessed: :data:`ALWAYS_SCANNED_ENVS` plus whatever the
> transport itself treats as credential-bearing (the endpoint registry's own
> ``key_env`` values and any name a caller registered).

and `src/minireason/loop/__init__.py`: "a bearing record is **refused, not
redacted**". `design/design-s7-wave-plan.md`'s W0-CUSTODY acceptance string
says "write_new refuses an existing path and refuses credential-bearing
content".

**Probe.** `python3 probe/p08_credential_scan.py`. It registers
`OPENROUTER_API_KEY` through the transport's own public
`register_secret_envs` (the path `tools/provider_smoke.load_env_file` uses, per
`provider_openai_compat.py:85-88`), puts a 20-character value in it, and writes
the same record three times: with a healthy transport, with `_secret_env_names`
/ `_secret_items` raising, and with the transport not importable. Verbatim:

```
default scanned names   : ('DEEPSEEK_API_KEY', 'OLLAMA_API_KEY')
after register_secret_envs: ('DEEPSEEK_API_KEY', 'OLLAMA_API_KEY', 'OPENROUTER_API_KEY')
names in a bearing record: ['OPENROUTER_API_KEY']
write_new (healthy transport): CREDENTIAL_IN_OUTPUT /tmp/tmp3c5iuc9a/one.json:OPENROUTER_API_KEY
scanned names, broken tx: ('DEEPSEEK_API_KEY', 'OLLAMA_API_KEY')
names in bearing record : []
write_new (broken transport): WROTE b'{\n  "h": "or-v1-0123456789abcdef"\n}\n'
```

```
--- transport not importable (custody's documented 'optional' path) ---
_provider_module()      : None
scanned names           : ('DEEPSEEK_API_KEY', 'OLLAMA_API_KEY')
names in bearing record : []
write_new               : WROTE b'{\n  "h": "or-v1-0123456789abcdef"\n}\n'
```

The unimportable-transport case is not an invented state: `custody.py:39-40`
says the module "reaches ``minireason.provider_openai_compat`` lazily and
optionally, so it stays importable on its own", which is the whole point of
`_provider_module` returning `None`.

I checked the blast radius in this tree. The command

```
python3 -c "import json; d=json.load(open('src/minireason/data/endpoints.json',encoding='utf-8')); eps=d['endpoints']; ks={}; [ks.setdefault(e.get('key_env'),[]).append(e.get('name')) for e in eps]; print(len(eps)); [print(k,len(v)) for k,v in ks.items()]"
```

prints `24`, `DEEPSEEK_API_KEY 2`, `OLLAMA_API_KEY 22` — the registry declares
24 endpoints over exactly two `key_env` values, both of which are already in
`ALWAYS_SCANNED_ENVS`. So on *this* registry the degradation costs nothing; it
costs exactly the names a caller registered at runtime, which is the case
`_secret_env_names`' own docstring says the registry exists for
(`provider_openai_compat.py:152-161`, the `OLLAMA_TOKEN` incident).

**Repair.** Make the degradation loud rather than silent. Either (a) let the
transport's failure propagate as a named `CustodyMismatch` — a custody module
that cannot determine its own scan set should refuse the write, not narrow it —
or (b) keep the fallback but return the fact alongside the names, e.g.
`scanned_credential_envs() -> tuple[str, ...]` plus a
`credential_scan_is_complete() -> bool` that `write_new` records into the
refusal detail and that PREFLIGHT asserts. Option (a) matches 4.4's "nothing
here repairs, retries, redacts or works around"; option (b) matches O8's
recommendation that "the closing record should state that the scan covers the
credentials this process could see".

**Test that would hold the repair.**

```python
def test_a_transport_that_cannot_name_its_credentials_does_not_silently_shrink_the_scan(self):
    tx.register_secret_envs(["OPENROUTER_API_KEY"])
    os.environ["OPENROUTER_API_KEY"] = "or-v1-0123456789abcdef"
    with mock.patch.object(tx, "_secret_env_names", side_effect=RuntimeError("registry")):
        with mock.patch.object(tx, "_secret_items", side_effect=RuntimeError("registry")):
            with self.assertRaises(custody.CustodyMismatch) as caught:
                custody.write_new(self.tmp / "r.json", {"h": os.environ["OPENROUTER_API_KEY"]})
    self.assertEqual(caught.exception.code, "CREDENTIAL_IN_OUTPUT")
    self.assertFalse((self.tmp / "r.json").exists())
```

---

## SHOULD-FIX 2 — `write_new` writes in place, so a crash mid-write leaves a truncated record that write-once then forbids anyone from repairing

**Claim.** The bytes go straight to the final name. A process death between the
first and second half of `handle.write(raw)` leaves a partial, unparseable
record at the coordinate; because the same function refuses an existing path,
no later run can complete or replace it. The docstring reasons carefully about
one crash window (file fsynced, directory not) and closes it, and leaves this
one open.

**Where.** `src/minireason/loop/custody.py:392-400`.

**What it contradicts.** `write_new`'s own docstring
(`src/minireason/loop/custody.py:374-381`):

> The bytes are flushed and ``fsync``ed, **and the parent directory is
> ``fsync``ed after them**: a receipt that resolves a spent call must survive
> the process, and on a crash between the two an ``fsync`` of the file alone can
> leave durable bytes under a name that was never committed to the directory - a
> spent call with no receipt, which is the one failure this function exists to
> prevent.

A spent call with a truncated receipt is the same failure wearing a filename,
and write-once makes it permanent rather than recoverable.

**Probe.** `python3 probe/p09_torn_write.py`. The kill is real, not simulated:
a forked child replaces `Path.open` with a handle whose `write()` emits half the
bytes, `fsync`s them, and calls `os._exit(9)`. Verbatim:

```
record would be 140 bytes
child exit status      : 9
file exists after crash: True
bytes on disk          : b'{\n  "coordinate": "row-3#judge-b",\n  "raw_ref": "blob:9999999999999999'
is it the whole record : False
json.loads(partial)    : ValueError: Unterminated string starting at: line 3 column 14 (char 48)
re-write the record    : WRITE_ONCE_VIOLATION /tmp/tmp38mjjyfo/steps/0007-S7.json
os.link / os.replace / os.rename in custody.py: []
```

W1-STEPS' acceptance in `design/design-s7-wave-plan.md` asks for
"kill-and-resume at every state leaves no coordinate re-sent", and
`W5-DRIVER`'s asks that "a killed run resumes without re-sending any coordinate
that already has a request or attempt" — a receipt that parses as nothing is a
coordinate the resume planner cannot classify.

**Repair.** Write to a sibling temp name in the same directory, `fsync` it,
then `os.link(tmp, target)` and unlink the temp. `os.link` fails with
`FileExistsError` when the target exists, so write-once survives unchanged and
the record becomes atomic: after the crash the coordinate is either absent or
complete. `_fsync_directory` stays where it is, after the link.

**Test that would hold the repair.**

```python
def test_a_crash_mid_write_leaves_the_coordinate_absent_not_truncated(self):
    target = self.tmp / "steps" / "0007-S7.json"
    pid = os.fork()
    if pid == 0:
        _install_half_writing_open()
        try:
            custody.write_new(target, RECORD)
        finally:
            os._exit(0)
    os.waitpid(pid, 0)
    self.assertFalse(target.exists())
    custody.write_new(target, RECORD)                      # the retry now works
    self.assertEqual(json.loads(target.read_bytes()), RECORD)
```

---

## SHOULD-FIX 3 — `verify_pins` verifies pin maps clean that `types.loop_plan_id` refuses, so "custody verified" does not imply "this plan's identity can be recomputed"

**Claim.** Three pin-key spellings verify clean under `custody.verify_pins` and
are `PIN_INVALID` to `types.loop_plan_id`: an absolute key, a backslash-spelled
key, and a key with a trailing slash. Design 4.2 makes the pin map part of the
plan identity; a plan body that passes custody and cannot reproduce its own
`loop_plan_id` is a seam that reports a clean tree over an unusable plan.

**Where.** `src/minireason/loop/custody.py:420-436` (`_pin_key`), called from
`src/minireason/loop/custody.py:512-515`; against `types.py:529-536`
(`_relative`) reached from `types.py:946`.

**What it contradicts.** `src/minireason/loop/__init__.py`:

> **``loop_plan_id(config, pins)`` refuses a null pin.**  A pin whose value is
> ``None``, not a lowercase sha256, or keyed by an absolute or ``..``-bearing
> path is ``PIN_INVALID``: an unpinned file inside a plan identity pins nothing.

and the module's own deviation 2 (`custody.py:69-73`), whose stated reason for
canonicalising separators is host portability — "a pin map frozen on one host
must verify on another or it pins nothing". Accepting an *absolute* key does
the opposite: an absolute key verifies on the freezing host and is
`SOURCE_PIN_OUTSIDE_REPOSITORY` on any other, which is the failure deviation 2
says the canonicalisation exists to prevent.

**Probe.** `python3 probe/p05_seam_with_types.py`, verbatim:

```
backslash key
  verify_pins(backslash key               ) -> CLEAN
  loop_plan_id(backslash key               ) -> PIN_INVALID: pins key must be a relative path inside the repository
absolute key inside repo
  verify_pins(absolute key inside repo    ) -> CLEAN
  loop_plan_id(absolute key inside repo    ) -> PIN_INVALID: pins key must be a relative path inside the repository
'./'-prefixed key
  verify_pins('./'-prefixed key           ) -> CLEAN
  loop_plan_id('./'-prefixed key           ) -> accepted
trailing-slash key
  verify_pins(trailing-slash key          ) -> CLEAN
  loop_plan_id(trailing-slash key          ) -> PIN_INVALID: pins key must be a relative path inside the repository
```

The `./`-prefixed row is the control: both sides canonicalise it and both
accept, which is what agreement looks like.

**Repair.** Custody is right to canonicalise separators (deviation 2 earns
that) and should not silently accept a key shape the identity function rejects.
Add one finding code — or reuse `SOURCE_PIN_MALFORMED`, which already covers "the
plan says something a pin map may not say" — for a key that is absolute or
carries a trailing slash, and leave the backslash rewrite as the documented
deviation it is. Either way the two sides then partition the same key space.

**Test that would hold the repair.**

```python
def test_a_pin_map_verify_pins_calls_clean_is_a_pin_map_loop_plan_id_accepts(self):
    real = custody.sha256_path(self.pinned)
    for key in ("src/a.py", "./src/a.py", "src\\a.py", str(self.pinned), "src/a.py/"):
        with self.subTest(key=key):
            clean = custody.verify_pins({"pins": {key: real}}, self.repo) == []
            try:
                loop_types.loop_plan_id(CONFIG, {key: real})
            except LoopError:
                identified = False
            else:
                identified = True
            self.assertEqual(clean, identified)
```

---

## NOTE 1 — deviation 1 cites E028 for a lesson E028 does not record

`src/minireason/loop/custody.py:63-68` says:

> The frozen-plan drivers compare the whole map at once
> (``sql_construction_study.py:206`` raises a bare ``RUNTIME_SOURCE_CHANGED``),
> which cannot say which file moved - the defect
> ``docs/lessons/operations.md`` records under E028.

`docs/lessons/operations.md:50` is headed "E028: a frozen source pin can outlive
the defect it froze", and its body (lines 52-58) records that hash-pinning
"makes the plan reproducible and simultaneously makes its defects permanent ...
the repair turns a wrong answer into `RUNTIME_SOURCE_CHANGED`", and that a
frozen pin "does not license leaving a wrong assertion in place". I read the
whole section (`python3 -c` printing lines 50-60 of that file) and found no
sentence about per-path naming or about which file moved. The deviation itself
is sound and worth keeping; the citation points at a different lesson. No
runtime effect — a reader chasing the justification lands somewhere else.
Repair: cite the lesson that actually records the granularity defect, or drop
the citation and let the reasoning stand on its own. A test cannot hold this;
a reviewer reading both files can.

## NOTE 2 — "order-stable under any iteration order" is true for every pin map JSON can express, and not true in general

`verify_pins` iterates `sorted(mapping, key=str)` (`custody.py:510`) and
finally sorts by `(path, code)` (`custody.py:533`). Neither key separates two
*distinct* mapping keys whose `str()` is equal, so their relative order is
Python's stable-sort tie-break, i.e. insertion order.
`python3 probe/p07_order_and_purity.py`, verbatim:

```
string-keyed map, 200 shuffles, differing results: 0
...
--- keys whose str() collides ---
   insertion order [1, '1'] -> (('SOURCE_PIN_MISSING', '1', 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'), ('SOURCE_PIN_MISSING', '1', 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'))
   insertion order ['1', 1] -> (('SOURCE_PIN_MISSING', '1', 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'), ('SOURCE_PIN_MISSING', '1', 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'))
distinct results across insertion orders: 2

--- keys that canonicalise to one path but sort deterministically ---
   insertion order ['src/a.py', './src/a.py'] -> ... distinct results across insertion orders: 1
```

The unstable case needs `1` and `"1"` as separate keys of one mapping, which a
JSON plan body cannot produce, so the W0-CUSTODY acceptance clause "verify_pins
is pure and order-stable" holds for every input the design puts in front of it.
The docstring's sentence at `custody.py:500-503` is the thing that is broader
than the input. Repair: sort by `(name, code, expected or "", observed or "")`
in the final sort, or narrow the sentence to string keys.

## NOTE 3 — `digest` and `encoded` are defined over JSON values, and say nothing when handed a Python value that is not one

`python3 probe/p10_attacks_that_failed.py`, verbatim:

```
int and str keys that collide  RAISED TypeError: '<' not supported between instances of 'str' and 'int' (is LoopError: False)
```

`digest({1: "a", "1": "b"})` raises a bare `TypeError` from `sort_keys=True`
(`custody.py:269-270`). The docstring says "Identity digest of a JSON value"
(`custody.py:264`), and such a mapping is not one, so this is a boundary
statement rather than a contradiction — but it is another way an unnamed
exception leaves the module (see BLOCKER 3). Every genuinely JSON-shaped value I
tried round-tripped through `encoded` to a value the three digests agree on:
`plain object / non-ASCII / tuple becomes list / int key becomes string key /
bool key / float edge / empty containers` all printed `agree=True`.

## NOTE 4 — the credential scan sees UTF-8 renderings only

`credential_names_in` decodes `raw` as UTF-8 with `surrogateescape`
(`custody.py:316`) and searches the raw value and the JSON-escaped value
(`custody.py:322`). A `bytes` value written verbatim in another encoding passes.
`python3 probe/p03_write_new.py`, verbatim:

```
credential written as UTF-16 bytes              WROTE     b'\xff\xfes\x00k\x00-\x00u\x00t\x00f\x001\x006\x00-\x00s\x00e\x00c\x00r\x00e\x00t\x00'
```

Every UTF-8 rendering I tried was refused, including the JSON-escaped form, a
value needing escaping, a non-ASCII value under `ensure_ascii=False`, the same
under `ensure_ascii=True`, and a value exactly at the 8-byte floor. The
docstring claims only the two renderings it searches, so this is the documented
boundary being visible rather than a broken promise — worth stating because
`write_new` accepts arbitrary `bytes` and the acceptance clause says "refuses
credential-bearing content" without qualifying the encoding.

## NOTE 5 — `verify_pins` and `write_new` take opposite stances on a symlink

`write_new` treats a symlink appearing at a target as a custody event
(`custody.py:389`, and `probe/p03` prints `path is a dangling symlink LoopError
WRITE_ONCE_VIOLATION`). `verify_pins` follows one silently: a pinned regular
file replaced by a symlink to a twin with identical bytes verifies clean.
`python3 probe/p10_attacks_that_failed.py`:

```
replaced by a hard link, same bytes              CLEAN
replaced by a symlink, same bytes                CLEAN
  ... and then that target flipped one byte      [('SOURCE_PIN_MISMATCH', 'src/a.py')]
```

Content-addressing is about bytes and the bytes at the pinned path really are
unchanged, so the acceptance clause is not broken here — but the module is
making two different judgements about the same fact, and a reader of
`CUSTODY_CODES` cannot tell which one applies where. Repair, if wanted: record
`is_symlink` alongside the digest in the pin map, or say in the `verify_pins`
docstring that a pin addresses bytes and not inodes.

---

## Tried, and could not break

**1. Escaping the fence.** `python3 probe/p02_fence.py` puts 22 shapes through
`fenced`: `..` at the front and embedded mid-path, an absolute path outside the
root, an absolute path whose prefix is a *sibling* of the root (`/x/running`
against root `/x/run`), a directory symlink to outside, a file symlink to
outside, a dangling symlink to outside, a symlink to the root's own parent, a
relative root resolved against the cwd, and a root itself reached through a
symlink. Every escape was refused with `PATH_ESCAPES_RUN_ROOT`, and every form
the docstring says it accepts (`''`, `'.'`, `'./'`, a not-yet-existing relative
path, an absolute path already inside, an inward symlink) was accepted. The one
shape that is neither is `sub\..\..\outside\secret.txt` on POSIX, which `fenced`
resolves to a single filename containing backslashes *inside* the root — it does
not escape. I could not construct a path that left the root.

**2. Making `verify_pins` miss a byte.** `python3 probe/p10_attacks_that_failed.py`
flips one byte mid-file, appends one byte, truncates to empty, rewrites
`\n` as `\r\n` with the same text, rewrites identical bytes into a new inode,
replaces the file with a hard link to identical bytes, replaces it with a
symlink to identical bytes, and rolls `mtime` back to the epoch. Every change
of bytes was named `SOURCE_PIN_MISMATCH`; every preservation of bytes was
`CLEAN`. The design's clause "A one-byte change to any pinned file is detected
and named" held under all of them. `sha256_path`'s byte-mode read
(`custody.py:246-254`) is what makes the CRLF case land.

**3. Breaking the three-way digest identity of decision 7.**
`python3 probe/p01_published_facts.py` and `probe/p10` push a fixture carrying
non-ASCII text, an em dash, CJK, embedded quotes, backslashes, newlines and tabs,
nested empty containers, `None`, booleans, floats including `-0.0` and `1e400`,
tuples and integer keys through `custody.digest`, `provider_openai_compat.digest`
and `sha256_hex(canonical_json(...))`. All three agreed on every input
(`three-way identity : True`), `canonical_json(v)` was byte-identical to the
compact `json.dumps` custody hashes, and `encoded(v)` round-tripped to a value
with the same digest in every case. I also confirmed
`custody.encoded`'s byte form matches the transport's record writer:
`provider_openai_compat.py:243-251` builds
`json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"`.

**4. Getting a credential past `write_new` in any UTF-8 rendering, or getting
`write_new` to overwrite.** `python3 probe/p03_write_new.py`: a second write to
the same path, a write onto an existing directory, and a write onto a dangling
symlink were all `WRITE_ONCE_VIOLATION`, and the dangling symlink's target was
not created. A credential was refused as a raw value, as a JSON-escaped value,
as a value needing escaping (`quote"back\slash`), as a non-ASCII value under
`ensure_ascii=False` and under `ensure_ascii=True`, and at exactly the 8-byte
floor; a 7-byte value was written, which is the documented floor behaving as
documented. A refused write left no file and no parent directory
(`leak.json exists after refusal: False`, `parent dir created after refusal:
False`).

**5. Making `verify_pins` order-unstable, impure, or self-mutating on a
JSON-shaped pin map.** `python3 probe/p07_order_and_purity.py` shuffles a
six-entry pin map covering clean / mismatch / missing / not-a-file / outside /
malformed, 200 times, and compares the full finding tuples:
`string-keyed map, 200 shuffles, differing results: 0`. In the same run the
tree snapshot before and after was equal (`tree unchanged by verify_pins: True`),
the plan mapping's key order was unchanged, and two consecutive calls returned
equal dictionaries.

**6. Mangling the exception contract.** `python3 probe/p11_exception_shapes.py`
instantiates all three exception classes. `.code` and `.detail` are present on
each, `str(exc)` is `'WRITE_ONCE_VIOLATION: /run/steps/0001-S0.json'` for all
three (the `OSError` in `WriteOnceViolation`'s MRO does not hijack the message,
and `.errno` stays `None`), `CredentialInOutput` is a `ValueError`,
`WriteOnceViolation` is a `FileExistsError`, all three are `LoopError`, a
lower-case or hyphenated or empty code is refused by `types.LoopError`'s shape
gate, and the set of codes literally constructed anywhere in the module is
exactly `CUSTODY_CODES` — nine codes, none undeclared, none unused:

```
CUSTODY_CODES              : ('CREDENTIAL_IN_OUTPUT', 'PATH_ESCAPES_RUN_ROOT', 'PIN_MAP_MISSING', 'SOURCE_PIN_MALFORMED', 'SOURCE_PIN_MISMATCH', 'SOURCE_PIN_MISSING', 'SOURCE_PIN_NOT_A_FILE', 'SOURCE_PIN_OUTSIDE_REPOSITORY', 'WRITE_ONCE_VIOLATION')
constructed but undeclared : []
declared but never used    : []
```

`probe/p01` separately confirms the interface's arithmetic claims:
`CUSTODY_CODES len : 9`, `CUSTODY_CODES sorted : True`,
`not in FAILURE_CODES : []`, and
`MIN_CREDENTIAL_LENGTH : 8 == tx._MIN_SECRET_LENGTH 8 True`.

---

## Suspected and could not reproduce

* I suspected `fenced` would admit an absolute path whose *textual* prefix
  matches the root but whose resolved parent is a sibling directory
  (`/x/running/y` against root `/x/run`). It refuses:
  `absolute sibling-prefix  REFUSED PATH_ESCAPES_RUN_ROOT` in `probe/p02`. The
  check at `custody.py:360` compares resolved paths and uses `Path.parents`, not
  a string prefix.
* I suspected `pins()` could be made to return two different maps for the same
  files depending on the order of `paths`, since it builds an unsorted dict
  first. It cannot: `custody.py:470` re-emits in `sorted(out)` order and
  `probe/p04` prints `pins are byte-stable : True`.
* I suspected the `str`-key collision in `verify_pins` would be reachable from a
  JSON plan body through some key spelling that `_pin_key` collapses. Every
  collapsing pair I found (`"a/b"` vs `"./a/b"`, `"a/b"` vs `"a\\b"`) still sorts
  deterministically under `sorted(..., key=str)`, so the finding order is stable
  — `probe/p07`, `distinct results across insertion orders: 1`. I could not
  build a collision out of strings alone.

---

## What I could not determine

* **The other four wave-0 modules are not in this sandbox.**
  `src/minireason/loop/` here contains only `__init__.py`, `types.py`,
  `custody.py` and `data/` (`python3 -c "import os; print(sorted(os.listdir('src/minireason/loop')))"`).
  So every cross-module claim I checked was checked against `types`,
  `provider_openai_compat` and `deepreason_core` only. The interface note's
  claims that `CUSTODY_CODES` is asserted a subset by a test in
  `tests/loop/test_types.py`, and that `CustodyReport.from_findings` is the one
  adapter between `verify_pins` and the receipt, I could read in `types.py` but
  could not exercise against the test that is said to pin them. Unresolved.
* **There is no `tests/loop/test_custody.py` in this sandbox.**
  `tests/loop/` holds only `__init__.py`, and `python3 run_tests.py` discovers
  and runs `Ran 0 tests in 0.000s`. The interface note reports "loop-only
  `224 tests OK`" on the quiesced tree; I could not reproduce, contradict or
  even locate that suite here, so I have said nothing about whether the existing
  tests would catch any finding above.
* **Several of the module's provenance citations are outside this sandbox.**
  `tools/multicycle_commitment_study_multi_v2.py`,
  `tools/contrast_triple_study.py` (for `failure_code`, `FORBIDDEN_KEYS`,
  `scanned_credential_envs` and `check_transport_pins`) and
  `sql_construction_study.py:206` are cited by the module docstring and are not
  present. I confirmed the two citations I *could* reach —
  `graph_import_h005.PATH_ESCAPES_OCCURRENCE` and
  `graph_import_h005.OutRootRefused` both exist (`probe/p10`), and the
  transport's record encoding is byte-identical to `custody.encoded` — and I
  left the rest unverified rather than guessing. In particular I could not check
  the docstring's claim that `write_new` keeps "their `CREDENTIAL_IN_OUTPUT`
  spelling": that token does not appear in `provider_openai_compat.py`, but the
  drivers the sentence names are not here, so this is unresolved, not a finding.
  `REC-20260913-I`, cited at `custody.py:70`, appears nowhere in this sandbox
  (`docs/DECISION_LEDGER.md` is not included); I could not confirm or deny what
  it records.
* **Concurrency.** I did not probe two processes racing on the same
  `write_new` path, or a `verify_pins` running while the tree is being rewritten
  under it. `write_new`'s `exists()`/`is_symlink()` check at
  `custody.py:389` is separated from `open("xb")` at `custody.py:393` by a
  window, and `open("xb")` is the thing that actually holds write-once; I read
  the code as correct there but did not execute a race, because a passing race
  probe is not evidence and a failing one on this filesystem would not
  generalise. Unresolved.
* **Non-POSIX behaviour.** Every claim about backslashes, symlinks, `O_DIRECTORY`
  and directory `fsync` was executed on Linux 6.18 as euid 0
  (`probe/p06` prints `euid: 0`). Deviation 2 and the `_fsync_directory`
  docstring both talk about Windows and network filesystems; I could not
  exercise either, and the permission-denied path in particular is unreachable
  as root, so I made no claim about it.
* **The repository's own ledger, activity-log and publication obligations**
  (`AGENTS.md`) are not executable here: the sandbox is a frozen snapshot with
  no `git`, no network and no `docs/DECISION_LEDGER.md`, and the operating note
  confines me to `python3` forms. This review and its probes are the record.
