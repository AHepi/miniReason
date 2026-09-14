# kimi-k3 worker battery

| id | title | mode | iters | tool calls | tokens | wall s | finish | harness failure |
|---|---|---|---|---|---|---|---|---|
| a-01-types | Adversarial review of W0-TYPES (types) | tools | 40 | grep 9, list_dir 4, read_file 12, run_command 13, write_file 14 (52) | 1902351 | 459.9 | tool_calls | ITERATION_CAP |
| a-02-contracts | Adversarial review of W0-CONTRACTS (contracts) | tools | 40 | grep 8, list_dir 2, read_file 16, run_command 18, write_file 14 (58) | 3750719 | 1053.6 | tool_calls | ITERATION_CAP |
| a-03-standard | Adversarial review of W0-STANDARD (standard) | tools | 40 | grep 7, list_dir 3, read_file 14, run_command 14, write_file 13 (51) | 3020841 | 889.5 | tool_calls | ITERATION_CAP |
| a-04-custody | Adversarial review of W0-CUSTODY (custody) | tools | 37 | grep 5, list_dir 4, read_file 15, run_command 33, write_file 12 (69) | 2489795 | 539.5 | stop | - |
| a-05-receipts | Adversarial review of W0-RECEIPTS (receipts) | tools | 8 | grep 1, list_dir 2, read_file 9 (12) | 204935 | 338.1 | - | TRANSPORT_OR_RESPONSE_ERROR |
| a-06-publish | Adversarial review of W0-PUBLISH (publish) | tools | 5 | read_file 7 (7) | 94623 | 322.2 | - | TRANSPORT_OR_RESPONSE_ERROR |
| b-01-surface | Unit tests for W1-SURFACE (surface) | tools | 11 | grep 5, read_file 12 (17) | 566712 | 356.7 | - | TRANSPORT_OR_RESPONSE_ERROR |
| b-02-seats | Unit tests for W1-SEATS (seats) | tools | 40 | grep 6, list_dir 5, read_file 14, run_command 21, write_file 6 (52) | 2425621 | 552.5 | tool_calls | ITERATION_CAP |
| b-03-obligations | Unit tests for W1-OBLIGATIONS (obligations) | tools | 5 | grep 1, list_dir 1, read_file 9 (11) | 145725 | 362.6 | - | TRANSPORT_OR_RESPONSE_ERROR |
| b-04-steps | Unit tests for W1-STEPS (steps) | tools | 6 | grep 1, list_dir 1, read_file 12 (14) | 235324 | 448.9 | - | TRANSPORT_OR_RESPONSE_ERROR |
| c-01-packs | Implement W2-PACKS (packs) with its tests | tools | 14 | grep 2, list_dir 1, read_file 23 (26) | 917662 | 359.5 | - | TRANSPORT_OR_RESPONSE_ERROR |
| c-02-roles | Implement W2-ROLES (roles) with its tests | tools | 16 | grep 5, list_dir 3, read_file 18, run_command 1, write_file 1 (28) | 956617 | 560.7 | - | TRANSPORT_OR_RESPONSE_ERROR |
| c-03-markprep | Implement W2-MARKPREP (markprep) with its tests | tools | 10 | grep 5, read_file 13 (18) | 325798 | 343.0 | - | TRANSPORT_OR_RESPONSE_ERROR |
| c-04-decide | Implement W2-DECIDE (decide) with its tests | tools | 11 | grep 3, list_dir 1, read_file 14, run_command 1 (19) | 555556 | 558.5 | - | TRANSPORT_OR_RESPONSE_ERROR |
| d-01-receipt | Receipt paragraph in house style from a fact sheet | tools | 4 | grep 1, list_dir 2, read_file 5 (8) | 29257 | 313.2 | - | TRANSPORT_OR_RESPONSE_ERROR |
| d-02-operator-page | Operator-page section for W1-STEPS | tools | 14 | grep 5, list_dir 1, read_file 10, run_command 5, write_file 1 (22) | 812670 | 750.2 | stop | - |
| d-03-decision-record | Condense design section 5 into a decision-record paragraph | tools | 7 | grep 1, list_dir 2, read_file 5, run_command 1, write_file 1 (10) | 101714 | 213.0 | stop | - |
| d-04-f002-outcome | F002 closing-receipt outcome paragraph | tools | 8 | list_dir 6, read_file 5, run_command 3, write_file 1 (15) | 149531 | 312.2 | stop | - |
| e-01-refute | Refute three named claims in the session orchestration report | tools | 24 | grep 5, list_dir 22, read_file 15, run_command 3, write_file 3 (48) | 785525 | 481.0 | stop | - |
| e-02-metric-creep | Metric creep in standard.py and types.py | tools | 3 | list_dir 2, read_file 10 (12) | 44787 | 360.7 | - | TRANSPORT_OR_RESPONSE_ERROR |
| e-03-fw5-citations | Verify twenty FW5 line citations in the A001 staging document | tools | 20 | grep 2, list_dir 3, read_file 4, run_command 10, write_file 7 (26) | 952650 | 542.0 | stop | - |
| e-04-f001-classes | Classify the unresolved F001 coordinates | tools | 24 | grep 1, read_file 13, run_command 13, write_file 3 (30) | 1306658 | 766.0 | stop | - |
| f-01-c001-profile | C001 occurrence-01 failure profile by code and per family | tools | 25 | grep 5, list_dir 10, read_file 9, run_command 7, write_file 5 (36) | 859857 | 529.8 | stop | - |
| f-02-commit-tree | Check every published commit/tree identity in REC-20260914-U and -X | tools | 29 | grep 2, list_dir 4, read_file 9, run_command 13, write_file 7 (35) | 1790229 | 886.9 | stop | - |
| f-03-occ02-usage | C001 occurrence-02 usage and envelope profile | tools | 16 | grep 4, list_dir 1, read_file 10, run_command 5, write_file 2 (22) | 260436 | 248.1 | stop | - |
| b-004 | Packed-context variant of b-001 (fallback mode) | packed | 1 | - (0) | 0 | 300.3 | - | TRANSPORT_OR_RESPONSE_ERROR |

Totals: 26 task(s), 24685593 tokens, 698 tool calls, 16 harness failure(s).

### a-01-types — files written
- `probe/p01_env_driven_identity.py` (added, sha256 030b012e57b137d1)
- `probe/p01_unicode_identity.py` (added, sha256 ff95b6f42c4769f0)
- `probe/p02_stop_reasons_and_block_codes.py` (added, sha256 4607d4665f352d40)
- `probe/p03_strict_loader.py` (added, sha256 0751314b06fb65d9)
- `probe/p04_receipt_selfcheck.py` (added, sha256 5b4388f9e7c3fe74)
- `probe/p05_corners.py` (added, sha256 ed62339adbf93866)
- `probe/p06_receipt_uniqueness_and_failurecode.py` (added, sha256 304378ff7f3829d3)
- `probe/p07_loader_edges.py` (added, sha256 d467a5fb4724e8c1)
- `probe/p08_publish_ref_and_misc.py` (added, sha256 285d1e54cc59de6e)
- `probe/p09_receipt_cycle_code_and_looperror.py` (added, sha256 d6034a2c5860791c)
- `probe/p10_config_object_vs_mapping.py` (added, sha256 a6394ca22a5d4970)
- `probe/p11_step_classification.py` (added, sha256 94ac051453ff8bb3)
- `probe/p12_ceiling_parsing.py` (added, sha256 db51305119022bce)
- `probe/p13_determinism.py` (added, sha256 a01139f81ca7482a)

### a-02-contracts — files written
- `probe/fallback_and_transcript.py` (added, sha256 4f208cb471fed6ce)
- `probe/guard_g12.py` (added, sha256 d1e041c3b6fdf751)
- `probe/identity.py` (added, sha256 9ae9ae868da7bc68)
- `probe/marker_enum.py` (added, sha256 17a5cc3a12230111)
- `probe/never_raises.py` (added, sha256 53c53c7aea392294)
- `probe/ownership_body.py` (added, sha256 76bb1ea471bab3eb)
- `probe/purity_mut.py` (added, sha256 96cf247286747833)
- `probe/validate_core.py` (added, sha256 382773faee0a7083)
- `review/contracts.md` (added, sha256 ec29ffffc67ab1e7)

### a-03-standard — files written
- `probe/_probe_setup.py` (added, sha256 1f4fa58c0800b6f2)
- `probe/p01_basics.py` (added, sha256 247337dcbe074f8e)
- `probe/p02_vocabulary_note.py` (added, sha256 7f12fa9982fb5149)
- `probe/p03_exhaustion_scan.py` (added, sha256 044f2e5deb8ff8b9)
- `probe/p04_scoring_headers.py` (added, sha256 b3377635b56cf801)
- `probe/p05_build_parse.py` (added, sha256 c9720f53fc4a78ce)
- `probe/p06_scoring_and_prefix.py` (added, sha256 1d7890d99aed26dd)
- `probe/p07_mirror_boundary.py` (added, sha256 d02486ee9af4ddd1)
- `probe/p08_reconciliation.py` (added, sha256 ba11f4694b6e8272)
- `probe/p09_body_claims.py` (added, sha256 a6ee9c4629a0df96)
- `probe/p10_exhaustion_edges.py` (added, sha256 d1ba79641838799d)
- `probe/p11_ceiling_block_codes.py` (added, sha256 4e0521e7abfe8c5d)
- `probe/p12_homoglyph.py` (added, sha256 0c297a99d87cae02)

### a-04-custody — files written
- `probe/p01_write_once_existing.py` (added, sha256 93070c4f89004d54)
- `probe/p02_fence_escapes.py` (added, sha256 6ef5c0f9ec2901a9)
- `probe/p03_pins_verify.py` (added, sha256 f13479d247b815fc)
- `probe/p04_credential_scan.py` (added, sha256 24a43146d779d5e7)
- `probe/p05_digest_identity.py` (added, sha256 3c130f484212357a)
- `probe/p06_race_and_torture.py` (added, sha256 456d4039d29a406c)
- `probe/p07_toctou_proof.py` (added, sha256 73c739e8aa888ec9)
- `probe/p08_nonstring_key.py` (added, sha256 a83a5e6d00177f47)
- `probe/p09_root_writable.py` (added, sha256 59256cc0297eedc8)
- `review/custody.md` (added, sha256 f3b77888e539d2cf)

### a-05-receipts — files written
- (none)

### a-06-publish — files written
- (none)

### b-01-surface — files written
- (none)

### b-02-seats — files written
- `_scratch/_scratch/src/minireason/__init__.py` (added, sha256 4032724b98ed2671)
- `_scratch/_scratch/src/minireason/loop/__init__.py` (added, sha256 4032724b98ed2671)
- `_scratch/_scratch/src/minireason/loop/contracts.py` (added, sha256 91bb2419a7b69d50)
- `_scratch/_scratch/src/minireason/loop/types.py` (added, sha256 4092a0556e3e7761)
- `_scratch/_scratch/tools/__init__.py` (added, sha256 e3b0c44298fc1c14)
- `_scratch/_scratch/tools/multicycle_commitment_study_multi_v2.py` (added, sha256 7c1e295c86562d5f)
- `_scratch/run_scratch.py` (added, sha256 ecfa209ad5d182d9)
- `_scratch/sitecustomize.py` (added, sha256 564b51c7eb8dd63c)
- `_scratch/src/minireason/__init__.py` (added, sha256 9cd30fb590a035bd)
- `_scratch/src/minireason/loop/__init__.py` (added, sha256 2489c47b11259531)
- `_scratch/src/minireason/loop/contracts.py` (added, sha256 91bb2419a7b69d50)
- `_scratch/src/minireason/loop/types.py` (added, sha256 e9f2f123de0603cf)
- `_scratch/tools/__init__.py` (added, sha256 e3b0c44298fc1c14)
- `_scratch/tools/multicycle_commitment_study_multi_v2.py` (added, sha256 7c1e295c86562d5f)
- `tests/loop/test_seats.py` (added, sha256 ba27ce5ff560f8bb)

### b-03-obligations — files written
- (none)

### b-04-steps — files written
- (none)

### c-01-packs — files written
- (none)

### c-02-roles — files written
- `src/minireason/loop/roles.py` (added, sha256 2fb656a85ae81531)

### c-03-markprep — files written
- (none)

### c-04-decide — files written
- (none)

### d-01-receipt — files written
- (none)

### d-02-operator-page — files written
- `out/steps-operator-section.md` (added, sha256 344dcd6fb5a633f6)

### d-03-decision-record — files written
- `out/decision-record.md` (added, sha256 53212347e96d028a)

### d-04-f002-outcome — files written
- `out/f002-closing.md` (added, sha256 9822d101bfe80b09)

### e-01-refute — files written
- `check/refute_claims.py` (added, sha256 02ca543b5fed858e)
- `check/refute_claims_tail.py` (added, sha256 6dba6241864f1b13)
- `out/refutations.md` (added, sha256 19aedd3fbf2b6f2f)

### e-02-metric-creep — files written
- (none)

### e-03-fw5-citations — files written
- `check/verify_citations.py` (added, sha256 fd4eeebe9d7d10bc)
- `check/verify_final.py` (added, sha256 52c14eb3b12a3632)
- `check/verify_tail.py` (added, sha256 3be60ed67120c90a)
- `out/citations.md` (added, sha256 9f35f586f484ec50)

### e-04-f001-classes — files written
- `check/f001_classify.py` (added, sha256 f486978a8486ec6b)
- `out/f001-classes.md` (added, sha256 3d3c93bf1c9d1c9d)

### f-01-c001-profile — files written
- `check/c001_profile.py` (added, sha256 3c8854f492fe8238)
- `check/check_c001_profile.py` (added, sha256 5cd21f2be0d90d64)
- `out/c001-profile.md` (added, sha256 75f1484e7f6842ef)

### f-02-commit-tree — files written
- `check/commit_tree.py` (added, sha256 b3792b3439948b8f)
- `check/test_commit_tree.py` (added, sha256 f0fc5ca2f6883d5e)
- `out/commit-tree.md` (added, sha256 c69224b716aebaf1)

### f-03-occ02-usage — files written
- `check/occ02_usage.py` (added, sha256 a27e403b545484e2)
- `out/occ02-usage.md` (added, sha256 622b599609c8c118)

### b-004 — files written
- (none)
