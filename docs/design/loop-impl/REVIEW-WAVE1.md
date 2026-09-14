# Adversarial review — wave 1 of the automated loop, as integrated

Read: `WAVE1-INTERFACE.md`, `WAVE0-INTERFACE.md` (incl. §9 "Carried to later waves"),
`REVIEW-WAVE0.md`, `WAVE1-INTEGRATION-DECISIONS.md`, `design-loop/automated-loop-design.md`
§2–5, `src/minireason/loop/{surface,seats,obligations,graph,steps,synthetic}.py` and their
tests, `src/deepreason_core/adjudication/{edges,grounded,support}.py`, `SESSION_RULINGS.md`
6/7/10/13. Every claim was executed against the staging clone (`loop-impl/repo`, `9045a94`)
in a scratch tempdir. No repository file written, no git state changed, no network, no
provider call. `packs/roles/markprep/decide` ignored. Baseline: **704 loop tests OK**.

## Wave-0 fixes: three spot-checked, all held

**B1 (git allow-list):** `push -d`, `push --mirror`, `push --prune`, `update-ref -d`,
`branch -D` → `HistoryRewriteRefused`; `checkout --orphan`, `symbolic-ref`, `stash push` →
`GitSubcommandNotAllowed`. **B2 (G12 on a rendered file):** `assert_no_scoring_keys("| cell
| score |")` raises `CONTRACT_VIOLATION` and `standard.assert_no_scoring_headers` refuses
`| best endpoint | merit |` — held **as a function**; see blocker 1 for the caller.
**S1 (CRLF):** `.gitattributes` ships `src/minireason/loop/data/** -text`, no `\r` in the
ceiling, `CEILING_SHA256 == 1e26be08…`. (`assert_config_matches_standard` exists too, so B3
landed.)

# Blockers

## B1 — `p4` reports SATISFIED for a published table carrying `score` and `rank`
`obligations.py:952-963` (`_forbidden_hits`), `:1275-1284` (`no_scoring_key`),
`:1497-1521` (`ceiling_and_trichotomy_intact`).

**Claim.** §2.4 G12 runs the scan "over every emitted artifact, **every table header and
every rendered file**"; §5 P4 is "no scoring key appears **anywhere**", protected, failure ⇒
`STOP protected_loss`. Wave-0 B1 existed for exactly this.

**Evidence.** A fixture graph whose `rendered_files` record carries `READING_TABLE.md` =
`"# table\n\n| cell | score | rank |\n|---|---|---|\n| r1 | 0.9 | 1 |\n…"`:
`evaluate(...).verdict("p4")` → `SATISFIED`, detail *"no registered record carries a
forbidden scoring key"*; `p12` → `SATISFIED` (it reads that file's text but checks only
ceiling sentences). `_walk_keys` yields mapping **keys** only, so a file's text — a value —
is never scanned. `assert_no_scoring_headers` refuses that header in isolation; nothing
calls it. **No predicate in the document scans a rendered file**, so the protected
obligation is unfalsifiable on G12's named subject.

**Fix.** `no_scoring_key` scans `rendered_files`' file text for Markdown table headers and
headings against the graph-declared `forbidden_keys` vocabulary (a local tokeniser —
`obligations` may not import `standard`), naming each offending file. **Test.** The probe
above: `p4` reads `NOT_SATISFIED` naming `READING_TABLE.md`; the clean fixture stays
`SATISFIED`.

## B2 — a landed publication can end with no receipt and an open marker
`steps.py:1118-1131` (`publish_step`, after `run(...)` returns published).

**Claim.** §4.3: "Every transition writes exactly one write-once receipt."
WAVE1-INTERFACE §5: a missing ledger is `LEDGER_NOT_FOUND` "at the first publication — a
misconfigured driver named at once".

**Evidence.** `publish_step("PUBLISH_CY", …, publisher=<stub returning PUBLISHED>)` with a
`ledger_path` that does not exist: the push succeeded and verified, then
`receipts.ledger_append` raised `LEDGER_NOT_FOUND` **outside** any handler — the
`try/except BaseException: handle.fail_from(exc)` covers only the `run(...)` call. Resulting
`steps/`: `['0001-PUBLISH_CY.json.open', '0001-PUBLISH_CY.verified']` — marker, sidecar, and
**no receipt**. On resume `guard()` raises `UNRESOLVED_STEP`; `acknowledge()` then writes an
erratum saying *"the step never resolved its open marker, so its body was not re-entered"*,
which is false. After acknowledgement `begin()` finds no `COMPLETE` receipt for the key, so
the next run **publishes the same paths again** at a fresh index with `attempt=1`. The same
window swallows a `custody.write_new` failure on the sidecar.
`tests/loop/test_steps.py:1113` asserts the code and that no ledger was created; nothing
about `steps/`.

**Fix.** Write the `COMPLETE` receipt (carrying `published_commit` and the verified-line
digest) **before** the ledger append and record a ledger failure as its own erratum; at
minimum put lines 1119-1131 inside the same `except BaseException: fail_from; raise`.
**Test.** Extend that test with `assertTrue(step_path(1,"PUBLISH_CY").is_file())` and
`assertNotIn("0001-PUBLISH_CY.json.open", self.step_files())`.

## B3 — the `self-juxtaposition` calibration anchor cannot resolve a single quote
`standard.py:1136-1149` (`must_sustain=True`, inside `STANDARD_BODY`, pinned into
`loop_plan_id`); `surface.py:263-281` (`_starts`), `:574-712`, `:728-753`.

**Claim.** §2.5: the planted-flaw set's ground truth is true by construction — "a row
juxtaposed with itself ⇒ `retains`" — and it must sustain; an error rate above
`JUDGE_ERR_MAX` Spawns `instrument_fault` (§4.4 rail 6).

**Evidence.** The two sides are the same bytes, so `build_surface` lays them out twice.
Executed on such a row: `count("grounds must be stated") == 2`, `count(<whole record>) == 2`,
`count("The account") == 2`, and `resolve_unique` is `None` for all three. **Every**
substring of the record occurs exactly twice, so no `passage_quote` can satisfy G2(a): the
anchor blocks with `blocked:referential-integrity` on every run, never sustains, and the
calibration arm reads a permanent instrument fault. The anchor is inside the frozen standard
body, so after PREREGISTER it cannot be changed without a successor standard.

**Fix (pre-registration review, beside p7/o5).** Build the anchor with only the referring
region present (same target coordinate, `target_record_verbatim` absent) so one region
carries the bytes; or state G2(a) per declared region for `mode: absolute` anchors and have
`resolve_unique` return the region-local span. Do not weaken `_starts` — overlapping
counting is correct and strictly stronger.

**Test.** `tests/loop/test_standard.py`: build each `CALIBRATION_ANCHORS` entry's surface
and assert some quote of it resolves uniquely inside a declared span. Today this one fails.

# Should-fix

**S1 — an appellate ruling may attack a node under study, which stops the chain.**
`graph.py:1273-1320`. `apply_appeal` validates only that `ruling.target` is *registered*.
Executed: `AppellateRuling(target=<material id>)` was accepted and minted
`att: appeal → MATERIAL`; the material went `REFUTED`, the cell `unsupported`. §3 enumerates
the admissible targets (ν_bearing, ν_soundness, the standard, a register definition, a
`difference_kind` set); the material is not among them, and p7 conjunct 1 then reads
`not_satisfied` ⇒ `STOP protected_loss`. §3/§4.4 also say the appellate is optional and the
loop never blocks on it, so a mis-aimed human ruling should be a named refusal, not a chain
stop. *Fix:* refuse a target whose registered `record` token is outside
`{validity_node, standard, appellate_ruling}`. *Test:* an appeal naming the material raises;
one naming ν_bearing still reinstates the default.

**S2 — an `artifact`-grain row has no target region, so every quote of its target blocks,
and the gate's outside-vocabulary leg is lost with it.** `surface.py:627-655`
(`target_verbatim is None` ⇒ region omitted). On the synthetic table (grain histogram
`{record: 7, artifact: 1}`) the artifact-grain row's `Surface.text` carries the referring
record and five body passages and **no target bytes at all**; its scripted critic quote
resolves `count=0`. So `M` does not contain the thing the row is about, the row is
unreadable by construction, and its block is filed under a *semantic* code
(`blocked:referential-integrity`) for what is an operational fact.
`tests/loop/test_synthetic.py:538-552` works around it by opening the artifact from disk,
which `surface` refuses to do by design. The same row is `read/unresolved-b`, whose fixture
intent (`tests/loop/test_synthetic.py:632`) is `unresolved:outside-vocabulary` with the text
preserved (D6) — but the guard order is G1→G2→G3→G4, so it blocks at G2 and D6 is never
exercised by the dry-run gate, while `describe()` accounts for only one referential-integrity
induction. *Fix:* carry the target contribution's `commitments` verbatim plus its published
span as a fourth declared region (or refuse the row with an operational code), then give
that row a quote that resolves uniquely while keeping `outside_vocabulary` non-empty.
*Test:* for every row of the synthetic table, `resolve_unique(build_surface(row), quote)` is
not `None` or the row is refused with a named operational code.

**S3 — `o3` is G2(a) only, and its uniqueness rule contradicts `surface`'s.**
`obligations.py:882-895`, `:965-979`, `:1058-1097`. Its statement is "every mark and every
relation carries a citation resolving under **G2 and G3**". The predicate reads
`{quote, surface}` only — no side, no offsets — so a quote resolving uniquely into the
surface's own **framing** satisfies o3, which is exactly what G3 exists to refuse. And
`_resolves_uniquely` is `partition`-based, i.e. non-overlapping: executed,
`_resolves_uniquely("aaa","aa")` is `True` where `Surface.count("aa")` on `b"aaa"` is 2 and
`resolve_unique` returns `None`. o3 can therefore certify a citation that G2(a) blocked.
*Fix:* have the reading record carry `Offset.as_dict()` (interface S1) and have o3 check the
recorded `side ∈ DECLARED_SIDES`; replace `partition` with "occurs at exactly one start
offset". *Test:* a doubled overlapping quote, and a `framing` side, each read
`not_satisfied`.

**S4 — the audit window is unbounded, so one hit collapses a seat's whole history.**
`graph.py:1201-1208`, `:1223`. `validity_nodes_for_seat` returns *every* ν_soundness the
seat ever carried, and is `register_audit_warrant`'s default `targets`. §2.5 says "every
reading that seat carried **in the window**", the window being `AUDIT_PERIOD` cycles;
`graph` cannot see cycles, so the bound must come from the caller — but the docstring calls
the unbounded set "the window", which W5 will read as the design's. *Fix:* re-document it as
"every node, all time" and require an explicit `targets`. *Test:* an empty `targets` refuses.

**S5 — the count-free AST guard has five blind spots.**
`tests/loop/test_obligations.py:757-846`. `obligations.py` itself is clean (I scanned it:
zero ordering comparisons, zero unary minus, zero banned builtin, zero `.count()`), but this
test is the standing guard for waves 2-6, and a probe function doing all of the following
passed **every one** of its five assertions: (a) `if Best.stamp > Scored[-1].stamp:` —
only `BinOp`/`AugAssign` are checked, so `ast.Compare` makes a threshold invisible;
(b) `sorted(nodes, key=…)[0]` — `sorted` is not in `BANNED_CALLS` and `[0]` is
subscript-exempt, which is "best/top" selection; (c) identifiers `Counter`, `Scored`,
`Best` — `FORBIDDEN` is lowercase and `tokens()` never casefolds; (d) `f"{x:.2f}"` — a
format spec is a `str` constant and survives both the numeric and the string scan;
(e) any numeric literal nested anywhere inside a subscript, because `ast.walk(node.slice)`
exempts every `Constant` it finds, including one inside a `Compare`. *Fix:* casefold
`tokens()`; add `Lt/LtE/Gt/GtE` `Compare` to the arithmetic assertion; ban `sorted`,
`statistics`, `Counter`; exempt only a `Constant` that *is* the slice. *Test:* the probe
must fail each added assertion.

**S6 — the offline gate never exercises the resolver it is a gate for.**
`tests/loop/test_synthetic.py:517-527`, `:538-553` build the surface by hand
(`"\n".join(...)`, `a + b`) and count with `str.count`, so the fixture is validated against a
string that is not `Surface.text` (no label framing, no `\n\n` separators) with a counter
that is not `Surface.count` (non-overlapping) — the "second counter" that interface
recommendation S3 warns against. I ran the real resolver over all eight scripted critic
quotes: they agree *today* (6 unique, `read/rejects` 2 by design, `read/unresolved-b` 0 —
S2), so this is drift risk, not a present error. *Fix/Test:* replace both hand-joins with
`build_surface` + `Surface.count` / `resolve_unique` / `within_declared_span`.

**S7 — `.gitattributes` does not yet cover the pre-registration bundle.**
`obligations.pin()` is the **file's** sha256 (deviation 1) and is folded into
`loop_plan_id`; `.gitattributes` protects only `src/minireason/loop/data/**` and
`docs/DECISION_LEDGER.md`, and says so in its own comment ("Two such files exist today").
A CRLF checkout of the committed `obligations.json`/`CEILING.md`/`config.json` moves the pin
silently — wave-0 S1's failure mode one directory over. *Fix:* add the bundle path with
`-text` in the commit that lands the bundle. *Test:* `assert b"\r" not in
(bundle/"obligations.json").read_bytes()`.

# Notes

* `seats.require_cross_family_judges({"judge_families": "ab"})` returns `('a','b')` — a
  `str` is iterated into characters (`seats.py:752-770`). PREFLIGHT is meant to run this over
  a *frozen* `plan.json` (Q6), where a hand-edited scalar is the shape to refuse.
* `graph._cell_index` (`:891-894`) is a dict comprehension: two `C_open` bodies sharing a
  `key` silently last-wins, and a reading attacking the other default would leave the cell
  `unresolved` forever. `open_cells` is content-addressed so it cannot produce one; a
  hand-registered default can.
* `graph._standing:1393` `elif len(accepted) > 1:` is the only cardinality test that changes a
  cell's state. §3 authorises it ("≥2 surviving rivals") and `relation` is read only when
  exactly one survives, so there is no hidden tie-break — but `accepted[1:]` says the same
  without a number, and ruling 7 is easier to audit if it does.
* Import-time file reads, measured: `surface` 2, `graph` 2, `seats` 3, `synthetic` 3
  (`endpoints.json` plus the two `loop/data` files); `obligations` and `steps` 0 — wave-0
  N3/N7 now span four of six wave-1 modules. `seats._repository_root` (`:804-808`) resolves
  `parents[3]` looking for `tools/multicycle_commitment_study_multi_v2.py`, which is not in
  the wheel at all, so `key_gate_for` is source-checkout-only and nothing says so.
* `RunLock.release()` leaves the holder record in the file, so `holder()` names a stale pid
  while the lock is free (`steps.py:489-496`) — documented as "for the human", who is exactly
  the reader it misleads. Decisions-doc item 11 confirmed as written: `complete()` runs
  outside `run_step`'s `except BaseException` and `custody.digest` raises a bare
  `TypeError`; B2 is the same window on the publication path, worse because the push landed.
* `produced_by`'s conjunct 2 (`obligations.py:1786-1802`) treats *not evaluable under
  withholding* as *stopped holding*. Conjunct 1 (`evidence ∩ registered`) saves it today — I
  checked: `registered=[reading_set]` gives `produced_by(s,"o1") == frozenset()` although the
  withheld verdict is `NOT_EVALUABLE` — but the distinction FW5 R5 draws is not recorded, and
  a predicate returning a declaring record in its evidence would discharge itself every
  cycle. One field in `Evaluation.as_dict` would settle it.

# Tried, and could not break

* **Two survivors are never resolved into one.** Two accepted rival readings of one cell:
  `state='contested'`, `relation=None`, `len(accepted)==2`, and `mark_triples` contributes
  **no** triple. No path in `graph` picks one, averages or votes.
* **An attack on bearing alone reinstates the default.** `split_validity_nodes`
  (`graph.py:1080-1084`) declares ν_bearing as `evidence` of ν_soundness, so the vendored
  evidence closure lifts the attack onto ν_soundness and the validity-node closure onto the
  carrier: executed, cell `read` → `unresolved`, reading `REFUTED`. R2 holds. Refuting the
  standard does the same through the case-law closure.
* **Refuting the material orphans, it does not refute.** Attacking the material: material
  `REFUTED`, reading `SUSPENDED_UNSUPPORTED`, ν_soundness still `ACCEPTED`, cell
  `unsupported`. The material is a `dep` target of the reading and deliberately *not* ν
  evidence, so pass 2 — not pass 1 — moves the reading. Orphaned is not false.
* **No reading's standing reaches the material.** The complete edge set of a read cell is
  `att: READING → C_OPEN` and `dep: {C_OPEN, READING, other C_OPEN} → MATERIAL`; `build_att`
  only adds carrier→target and closure edges onto ν and carriers, so nothing the loop mints
  targets the material. The one hole is an *appeal* (S1).
* **`RunLock` across two real OS processes.** Holder acquires; a second process gets
  `RUN_LOCKED`; after release a third acquires. `flock(LOCK_EX|LOCK_NB)`, not a thread lock.
* **`seats` orders nothing by merit.** The only orderings are `sorted((family, name))` and
  `sorted(name)`. The lineage fix works: default judges `deepseek-flash` (deepseek) and
  `ollama/gemma4-31b` (gemma), `digest == 2fe78293…` matching the interface's pinned literal,
  zero relaxations. `key_cap_for`/`key_caps` are `min(...)` over spend bounds only.
* **`obligations.py` is genuinely count-free.** AST scan of the shipped module finds no
  ordering comparison, no unary minus, no `len`/`sum`/`min`/`max`/`abs`/`round`, no
  `.count()`. What is weak is the guard protecting that property (S5), not the property.
  **`synthetic`**'s determinism and zero-socket assertions are tested and hold; the ten
  `describe()` inductions each name a failure or outcome **code**, never a score.
* **The record vocabulary partitions cleanly.** `graph.RECORD_KINDS − RECORDS_NOT_READ ⊆
  obligations.RECORD_KINDS` and `RECORDS_NOT_READ ∩ obligations.RECORD_KINDS = ∅`; the
  15-entry `not_evaluable` allow-list reproduces exactly.
