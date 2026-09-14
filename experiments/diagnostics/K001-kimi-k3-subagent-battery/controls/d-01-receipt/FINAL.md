REC-20260914-V publication outcome at 2026-09-14 09:28 UTC: The second contrast-triple driver and the second frozen occurrence are published and verified on `claude/project-state-direction-j5rbun` in one commit. The choice this records, opened under this letter at 2026-09-14 09:13 UTC with `REC-20260914-U` closed at 09:05 UTC and carrying its own correction at 09:06:10 UTC behind it, was to publish a second contrast-triple driver and a second frozen occurrence and only then dispatch twenty live calls on the one cell occurrence-01 could not resolve; the instrument and the occurrence are published **before any occurrence-02 provider call exists**, which is the substance of the choice and not a formality. The commit carries `tools/contrast_triple_study_v2.py` (sha256 `1857110385da3e2e4740086410ba6f840947dc4d8267527c6c9b86aada80f9cf`), `tests/test_contrast_triple_study_v2.py` (`1a5b9fccc6c6fc913e43f54a60641e591a85bf4cc3650d2b41b474ab9688e937`), `experiments/diagnostics/C001-contrast-triple/material-occurrence-02.json` (`1ba7be081b6fb0c56af7433589ae8bd8591c3a9e697a816d32b0950851874f30`), `experiments/diagnostics/C001-contrast-triple/build/build_occurrence02_material.py` (`8d2cfd79976944ef203a4f578ab71ea2d30e55554be94fd6b24e27c1ca72debd`) and `docs/sources/contrast-triple-deepseek-ceiling-probe-2026-09-14.md`, every sha256 re-read from the repository copy and every one equal to its staged value, together with `PLAN.md` section 15 and one workflow section, which are appends and not rewrites -- `docs/lessons/operations.md` requires that an append-only record be appended to in byte mode. The provenance script rebuilt the occurrence-02 material from the **published** occurrence-01 `material.json` (`94edfe61...`) into a byte-identical file: `cmp` clean, `target_sha256` `1ba7be08...`. Suites, every count kept beside the invocation that produced it as `docs/lessons/operations.md` requires: `PYTHONPATH=src python3 -X utf8 -m unittest tests.test_contrast_triple_study` is **Ran 121 tests, OK**, the published v1 file untouched byte for byte; `PYTHONPATH=src python3 -X utf8 -m unittest tests.test_contrast_triple_study_v2` is **Ran 154 tests, OK**; and `PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests` is **Ran 1397 tests, OK (skipped=1)**, against the **1243 OK (skipped=1)** `REC-20260914-U` measured on that same command in this tree before these files existed. Freeze evidence, zero provider calls, read off the files rather than asserted: `prepare` reports `{"plan_id": "1d9f47acdc692146792e354afdd9c6944036cb7d55bd83cc32c905e7c4ffeb83", "planned_calls": 20, "provider_calls": 0}` and `verify` reports `{"plan_id": "1d9f47ac...", "verified": true}`; `plan.json` re-derives to the path-independent `0c4aa5bbd9f71ab6d988f67ba91d4810861f16e65df5637d7b09a06bed6d52a3`; `preflight.json` records `OFFLINE_PREFLIGHT_PASSED` with `payloads_built_by_the_transport` **20**, `provider_calls` **0** and `distinct_message_pairs` **4**; `dispatch_scope` is `{"endpoints": ["deepseek-flash"], "arms": ["fcl"], ...}` over exactly twenty coordinates, all `deepseek-flash`, all `fcl`, four cases at five replicates each; `endpoints[].max_tokens` and `ceilings.max_tokens` both read **32768** and both `timeout_seconds` tables read **600**; `helper_sha256` equals `sha256(tools/contrast_triple_study_v2.py)` = `18571103...` and is **not** v1's `f5f9dfca...`; `transport_pins_verified` re-hashes to `cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db` for the transport module and `03eff16b8f575c113871a1266439874b2622a75d200ecb84a1b79464aa98aee7` for the endpoint registry, `resolved_from` `/home/user/miniReason/src`, with `git status --short src/` empty, so the registry was not edited; `occurrence-02/RECODING_TABLE.md` is byte-identical to the published `dcaebaf8336c1943700a762b4836679307349d6ff8dfad082e4cd77e23fd7ae7`; all eight brief documents' `messages_sha256` and `brief_sha256` equal occurrence-01's and the two plans' `briefs` blocks are equal; and the two `plan.json` files differ in exactly `ceilings`, `coordinates`, `endpoints`, `helper_sha256`, `material_sha256`, `partial_delivery_rule`, `plan_id`, `planned_calls` and the added `dispatch_scope`, and in nothing else. Twelve files are frozen -- `plan.json`, `preflight.json`, `material.json`, `RECODING_TABLE.md` and the eight briefs -- and four of those eight, the whole `prose` arm, are frozen, hashed into `plan_id` and **never dispatched**, because the pre-registration is a claim about the whole 85-row correspondence table while the scope narrows only what is sent. Occurrence-01 stands exactly as published and is modified, reinterpreted and superseded by nothing here: `git status --short` and `git diff HEAD` are both empty over `occurrence-01/`, `material.json`, `tools/contrast_triple_study.py`, `tests/test_contrast_triple_study.py` and `src/`. Why this occurrence exists, stated as the condition it is: in occurrence-01 the `deepseek-flash` x `fcl` cell yielded **1 of 20** usable coordinates at the **8192** ceiling, nineteen of the twenty finishing at exactly 8192 completion tokens -- eleven of those spending the entire ceiling on reasoning (`reasoning_tokens` 8192) and returning no public content, the other nine spending between 5488 and 7890 on reasoning and stopping at `finish_reason: "length"` -- while the same endpoint's `prose` arm returned **20 of 20 COMPLETE** at the same 8192 ceiling, at completion tokens 3,621 to 6,985. Both of those 8192 readings are **a resource observation and not a semantic one**, in exactly those terms: nothing about how any family reasons may be read off them, the `fcl` and `prose` arms are two independent occasions and never competitors, no merit claim and no ordering between them is made or implied, and a ceiling or a clock is a **resource boundary** and is never the exhaustion of the inquiry. Occurrence-02 accordingly raises the ceiling to **32768** and the clock to **600 s** and changes nothing else that the two `plan.json` files do not already record. The contribution to the end goal is that the one cell occurrence-01 could not resolve gets a second occasion, twenty coordinates under a declared resource allowance, published as a pre-registration carrying its own `plan_id` before any reply to it exists, with the first occurrence's record standing untouched beside it. Dispatch readiness, recorded here and not acted on: no C001 or F001 `run` process is alive, so the five-per-key DeepSeek slots are free; `ceilings.automatic_retries` is **0** and `ceilings.max_concurrent_per_key` is **5**; and `build_waves` on this plan gives **four waves of five, every one single-key on `DEEPSEEK_API_KEY`**, one case per wave. Credential scan over the staged set, counts only: **zero** hits at full, twelve-character and six-character key length, zero `Bearer ` tokens and zero `sk-` prefixes, across twelve instrument files and then twelve occurrence files, with no value and no fragment printed or written. State stays **PENDING**: dispatch of the authorised calls begins only after the commit's ref and tree are read back from the remote. Verified publication: remote `claude/project-state-direction-j5rbun` at 2d7239acd70f14aa049b62034a803784883da7b7, tree 9d0ab88f6940b220110797722fd4e628aef9c43e, read back with `git ls-remote --refs origin refs/heads/claude/project-state-direction-j5rbun`.

---

## Facts from the sheet I deliberately left out, and why

The paragraph carries every substantive fact the sheet states about this publication:
the letter, both timestamps, the predecessor and its correction, what was authorised,
the commit and tree and the branch and the read-back command, all six carried items with
the four sha256 values the sheet gives, the provenance rebuild, all three suites with
their invocations, all thirteen freeze-evidence items, the twelve frozen files and the
four never-dispatched `prose` briefs with the reason, the dispatch-readiness items, the
credential-scan counts, and the whole occurrence-01 resource condition including the
`prose` arm's twenty-of-twenty figure. What I left out is therefore short, and each item
is named here.

1. **The sheet's preamble and its closing section "Constraints on how this paragraph may
   be written."** These are instructions to the writer, not facts about the publication.
   Their substance is honoured in the paragraph rather than quoted in it: the 8192
   readings are called "a resource observation and not a semantic one" in those terms, a
   ceiling and a clock are called a resource boundary and never the exhaustion of the
   inquiry, `fcl` and `prose` are called two independent occasions and never competitors,
   and occurrence-01 is said to stand exactly as published and to be modified,
   reinterpreted and superseded by nothing in the paragraph.

2. **The full-length forms behind the digests the sheet itself abbreviates.** The sheet
   writes `94edfe61...` for the published occurrence-01 `material.json`, `f5f9dfca...`
   for v1's `helper_sha256`, and the abbreviated `1ba7be08...`, `18571103...` and
   `1d9f47ac...` at their second mentions. I carried those abbreviations exactly as
   given and did not lengthen them. Full forms for `94edfe61...` and `f5f9dfca...` do
   appear in `docs/ledger/REC-20260914-U.md` in the sandbox, but the sheet is the whole
   of the evidence for this paragraph, so importing them would have been adding a fact
   the sheet does not contain.

3. **Everything in `docs/ledger/REC-20260914-U.md` and
   `docs/ledger/house-style-samples.md` except register.** I read both only for the two
   receipt forms. No figure from them is in the paragraph -- not U's commit `ad3e347`,
   not its 240-call/47-wave counts, not its 1243-test baseline as its own evidence (the
   1243 figure appears only because the fact sheet itself states it as the comparison
   for 1397, and it is kept beside the same invocation the sheet names), and not the
   content of U's 09:06:10 correction, which the sheet records as existing and does not
   quote.

4. **The elided interior of `dispatch_scope`.** The sheet gives
   `{"endpoints": ["deepseek-flash"], "arms": ["fcl"], ...}`; I reproduced the ellipsis
   rather than guessing what it covers.

5. **A sha256 for `docs/sources/contrast-triple-deepseek-ceiling-probe-2026-09-14.md`,
   and any file-count or insertion-count for the commit.** The sheet gives neither, so
   the paragraph names that file without a digest and describes the commit without a
   diffstat, where the house style would normally carry both.

Two further choices are worth naming because they were deliberate rather than incidental.
The paragraph states the `docs/lessons/operations.md` byte-mode rule as the requirement
governing the appended `PLAN.md` section 15 and workflow section; it does **not** assert
that the append was performed in byte mode, because the sheet says only that the sections
were appended. And the `prose` arm's 20-of-20 figure is reported as the sheet reports it,
with no inference drawn from the pair of arms in either direction.

## What I could not determine

* **I could not verify a single figure in the receipt.** The sandbox holds five files --
  `AGENTS.md`, `factsheets/D-DOC-1-fact-sheet.md`, `docs/lessons/operations.md`,
  `docs/ledger/REC-20260914-U.md` and `docs/ledger/house-style-samples.md`. There is no
  repository, no `src/`, no `tests/`, no `plan.json`, no `preflight.json`, no commit and
  no `run_tests.py`. Every hash, count, timestamp and path in the paragraph is carried
  from the fact sheet on the sheet's own authority; none of it was re-measured here, and
  I make no claim that any of it is true of any tree. This is expected -- the sheet is
  declared to be the whole of the evidence -- but it means the receipt is a faithful
  transcription and not an independent verification.
* **I ran no command.** `run_tests.py` is not present in the sandbox, and there is no
  test module to invoke, so the three suite lines are quoted with their invocations
  exactly as the sheet pairs them and were not re-run. The only `python3` use here was
  to read the sandbox files, to extract the digests character-exactly rather than
  retype them, and to write `out/receipt.md` in byte mode.
* **Whether the `PLAN.md` and workflow appends were made in byte mode is unresolved.**
  The sheet says "appended" and says nothing about the mode. I could not determine this
  and the reason is that the evidence does not address it, so the paragraph names the
  rule and stops there rather than claiming compliance.
* **The commit's diffstat, the probe document's digest and the elided `dispatch_scope`
  keys are unresolved**, for the same reason: the sheet does not contain them and
  nothing in the sandbox could supply them without going outside the declared evidence.
* **I could not confirm where this paragraph belongs in the real ledger.** There is no
  `docs/DECISION_LEDGER.md` in the sandbox, so the receipt was written as a standalone
  file at the path the task names, `out/receipt.md`, written in byte mode as a single
  paragraph on one line with a single trailing newline. Whether appending it to the live
  append-only record would produce an insertions-only diff is not something I could
  check from here.
