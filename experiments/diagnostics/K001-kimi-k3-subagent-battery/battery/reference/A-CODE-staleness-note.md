# Staleness note — REVIEW-WAVE0.md against the frozen wave-0 snapshot

**Read this before judging any family-A task or E-ADV-2.**

`REVIEW-WAVE0.md` was written against the wave-0 modules as they stood earlier on
2026-09-14. The battery's frozen copy of those modules was taken later, after the
wave-0 fixer had begun applying the review's own repairs. The two are not the same
bytes. Probes executed at battery build time, inside a sandbox built exactly like a
task sandbox (`python3 run_tests.py` layout, `src` on `sys.path`):

| review finding | probe | result against the frozen snapshot |
|---|---|---|
| B1 history-rewrite guard passes eight destructive argvs | ran `publish._refuse_history_rewrite` over the review's own probe table (`push -d`, `push --mirror`, `push --prune`, `update-ref -d`, `update-ref <sha>`, `branch -D`, `stash push`, `checkout --orphan`, `symbolic-ref HEAD`) | **repaired** — every one is now refused |
| B2 `assert_no_scoring_keys` silent on a rendered file and a table header | called it with `"\| cell \| relation \| score \| rank \|"`, with `b"score"`, and with `{"score": 1}` | **repaired** — raises `ContractError` on `str` and `bytes`; `contracts.assert_no_scoring_headers` now exists |
| B3 a config can turn off a pre-registered guard | `types.SeatsConfig.from_mapping({"paraphrase_n": 0})` | **repaired** — refused with `CONFIG_INVALID_VALUE`; `standard.assert_config_matches_standard` now exists |
| S1 CRLF checkout changes `loop_plan_id` | read `standard.CEILING_PATH` bytes | **repaired** — no `\r`; a `.gitattributes` is present in the staging clone |
| S2 ledger default silently creates a second ledger | `open_receipt(..., ledger_path=<missing file>)` | **repaired** — `ReceiptError LEDGER_NOT_FOUND` |
| S5 exhaustion exemption byte-exact and case-sensitive | passed the denial sentence-initial, upper-cased and re-wrapped | **repaired** — all three accepted |
| S6 audit thresholds carry no account | `types.AuditConfig.from_mapping({"period":3,"judge_err_max":0.2,"streak_max":5})` | **repaired** — `CONFIG_MISSING_KEY` |
| S7 `judge_seats` may be raised while the frozen text says "Both" | built the standard at `judge_seats=8` and read `unanimity_rule` | **repaired** — the rule now reads "Every judge seat must return the same `sustained` value." |
| S10 nothing stops a per-seat calibration rate | read `types.AuditConfig.__doc__` | **repaired** — the docstring now addresses the per-seat case |
| S11 `VALIDATORS` cannot pass `register` | `inspect.signature(contracts.VALIDATORS["marker"])` | **repaired** — `(raw, *, register=None, _role='marker')` |
| N6 a critic may claim a relation and an `outside_vocabulary` | `contracts.check("critic", {...,"relation":"repairs","outside_vocabulary":"x"})` | **repaired** — `relation` is forced to `none` and the nomination moves to a new `nominated_relation` field |
| S4 the §2.3 contracts are in no pinned artifact | read `types.PINNED_SOURCE_PATHS` and the standard body keys | **partly addressed** — the body now carries a `role_contracts` section; `PINNED_SOURCE_PATHS` still names no loop module and the body carries no `contracts_sha256` |
| S8 the code-table scan is blind to keywords and name indirection | read `tests/loop/test_types.py` | **partly live** — the scan now uses `rglob` and a `TOKEN_ARGUMENT` table, but still does not read `ast.Call.keywords` |
| N2 `write_new` does not fsync the parent directory | read the source of `custody.write_new` | **live** — six `fsync` calls, none on a directory handle |
| N4 `verify_published` also byte-compares the working tree | `_read_back` still present in `publish.py` | **live** |

## What follows for scoring

1. **REVIEW-WAVE0.md is not a hit list for the frozen snapshot.** Judging a
   family-A review by overlap with it alone would punish a correct reading of the
   current bytes and reward pattern-matching against a stale document.
2. Each family-A task and E-ADV-2 therefore carries an **Opus control on the same
   frozen bytes**, and the primary comparison is Kimi's finding set against Opus's
   finding set on those bytes.
3. `REVIEW-WAVE0.md` is still used, as a **secondary reference in two directions**:
   - a finding that reproduces one of the rows above still marked *live* or *partly
     live* is a confirmed hit, whoever found it;
   - a finding that restates a row marked *repaired* — asserting a defect the
     frozen code no longer has — is a **false positive**, and the judge must say so
     by name. This is the battery's sharpest single test of whether a worker read
     the code or recited a pattern.
4. For E-ADV-2 (metric creep), the lens-1 table of `REVIEW-WAVE0.md` is matched on
   **site identity — module plus symbol — and never on line number**, because the
   frozen files have grown by 2 to 6 KB each since the review. A lens-1 row whose
   subject no longer exists in the frozen file is removed from the denominator and
   the judge records which rows were removed.
