# kimi-k3 worker battery

| id | title | status | mode | transport | iters | tool calls | tokens | wall s | finish | harness failure |
|---|---|---|---|---|---|---|---|---|---|---|
| a-01-types | Adversarial review of W0-TYPES (types) | COMPLETE | tools | native | 24 | grep 4, list_dir 1, read_file 9, run_command 11, write_file 11 (36) | 1026089 | 760.0 | stop | - |
| a-03-standard | Adversarial review of W0-STANDARD (standard) | COMPLETE | tools | native | 21 | grep 6, read_file 8, run_command 11, write_file 10 (35) | 1060822 | 676.5 | stop | - |
| a-05-receipts | Adversarial review of W0-RECEIPTS (receipts) | COMPLETE | tools | native | 16 | grep 5, read_file 6, run_command 10, write_file 9 (30) | 754277 | 872.1 | stop | - |
| a-06-publish | Adversarial review of W0-PUBLISH (publish) | COMPLETE | tools | native | 44 | grep 2, list_dir 1, read_file 4, run_command 29, write_file 23 (59) | 1832647 | 1112.1 | stop | - |
| b-01-surface | Unit tests for W1-SURFACE (surface) | COMPLETE | tools | native | 18 | grep 3, read_file 6, run_command 10, write_file 2 (21) | 652256 | 354.6 | stop | - |
| b-02-seats | Unit tests for W1-SEATS (seats) | HARNESS_FAILURE | tools | native | 0 | - (0) | 0 | 0.0 | - | CONTEXT_PATH_MISSING |
| b-03-obligations | Unit tests for W1-OBLIGATIONS (obligations) | COMPLETE | tools | native | 13 | grep 2, read_file 6, run_command 6, write_file 2 (16) | 564212 | 406.2 | stop | - |
| b-04-steps | Unit tests for W1-STEPS (steps) | COMPLETE | tools | native | 16 | grep 5, read_file 9, run_command 3, write_file 3 (20) | 1015168 | 598.4 | stop | - |
| c-01-packs | Implement W2-PACKS (packs) with its tests | COMPLETE | tools | native | 32 | grep 10, read_file 16, run_command 13, write_file 3 (42) | 2960559 | 607.1 | stop | - |
| c-02-roles | Implement W2-ROLES (roles) with its tests | COMPLETE | tools | native | 26 | grep 3, read_file 10, run_command 12, write_file 4 (29) | 1878186 | 719.2 | stop | - |
| c-03-markprep | Implement W2-MARKPREP (markprep) with its tests | HARNESS_FAILURE | tools | native | 9 | grep 5, list_dir 1, read_file 8, run_command 1 (15) | 235204 | 419.4 | - | TRANSPORT_OR_RESPONSE_ERROR |
| c-04-decide | Implement W2-DECIDE (decide) with its tests | COMPLETE | tools | native | 23 | grep 4, read_file 13, run_command 7, write_file 6 (30) | 2553351 | 986.9 | stop | - |
| d-01-receipt | Receipt paragraph in house style from a fact sheet | COMPLETE | tools | native | 10 | list_dir 2, read_file 5, run_command 5, write_file 1 (13) | 244256 | 117.2 | stop | - |
| e-02-metric-creep | Metric creep in standard.py and types.py | COMPLETE | tools | native | 11 | grep 1, list_dir 2, read_file 6, run_command 5, write_file 4 (18) | 456077 | 244.7 | stop | - |

Totals: 14 task(s), 15233104 tokens, 364 tool calls, 2 harness failure(s).

### a-01-types — files written
- `probe/p01_custody_checks_string.py` (added, sha256 e55fc74f2fae4a28)
- `probe/p02_utc_impossible.py` (added, sha256 55bd8685a5c43c90)
- `probe/p03_reading_dir.py` (added, sha256 2930b5ed1939a620)
- `probe/p04_pins.py` (added, sha256 acadcfe12cacc5fb)
- `probe/p05_tables.py` (added, sha256 720df51fe4df8218)
- `probe/p06_receipt.py` (added, sha256 8f1f9dd4afd51b1f)
- `probe/p07_acceptance.py` (added, sha256 bb8f580ade6d3ad0)
- `probe/p08_more.py` (added, sha256 96c461bff4e380ad)
- `probe/p09_ids.py` (added, sha256 ee2b8aad5c6bcbcc)
- `review/types.md` (added, sha256 5ee019bbb3bb09b3)

Reasoning characters per turn: 31, 7149, 155, 6048, 0, 11980, 17870, 23066, 0, 886, 0, 0, 0, 551, 0, 3414, 0, 56, 0, 0, 0, 0, 0, 0

Expected outputs present: review/types.md, probe/; missing: (none)

### a-03-standard — files written
- `probe/exhaustion_and_headers.py` (added, sha256 636c4eab88a3aa5b)
- `probe/guard_params.py` (added, sha256 d1212e25d0492a21)
- `probe/guard_params2.py` (added, sha256 0dc6f674fdf32b73)
- `probe/int_oracle.py` (added, sha256 41f9123d92b1547b)
- `probe/more_attacks.py` (added, sha256 6e2cbdc7d2c502bd)
- `probe/parse_and_reconcile.py` (added, sha256 e454664ae7526da2)
- `probe/roundtrip.py` (added, sha256 7f9c5f4c8da2f292)
- `probe/secondary.py` (added, sha256 fd07fd71a44faa5e)
- `review/standard.md` (added, sha256 af29da353523a71f)

Reasoning characters per turn: 26, 7711, 127, 0, 8904, 0, 18677, 0, 0, 0, 5392, 0, 1206, 0, 0, 4150, 508, 303, 138, 0, 275

Expected outputs present: review/standard.md, probe/; missing: (none)

### a-05-receipts — files written
- `probe/activity_runner_errors.py` (added, sha256 65a098f80e282aa0)
- `probe/attacks_failed.py` (added, sha256 d98f1f373ac798d3)
- `probe/bracket_masking.py` (added, sha256 3eb0ba2737cb2b73)
- `probe/byte_mode_add_only.py` (added, sha256 abee25e532082b53)
- `probe/render_collision.py` (added, sha256 e58f28fa6ecc1a74)
- `probe/render_render_reenter.py` (added, sha256 f5a014ebafaf55ce)
- `probe/secret_refusal_fixed.py` (added, sha256 9ea7f897b9e4ac7e)
- `review/receipts.md` (added, sha256 5eb2e5f9db04de65)

Reasoning characters per turn: 26, 12218, 14788, 9495, 30633, 10704, 0, 7054, 0, 519, 0, 0, 0, 130, 0, 20

Expected outputs present: review/receipts.md, probe/; missing: (none)

### a-06-publish — files written
- `probe/fixture.py` (added, sha256 06eb96f4c5be024e)
- `probe/p10_scan_encodings.py` (added, sha256 a5138b552395a6ff)
- `probe/p11_leftovers.py` (added, sha256 5dd5481b354f4496)
- `probe/p12_connector_equal_tree.py` (added, sha256 7abc08da24c7862f)
- `probe/p13_scan_coverage.py` (added, sha256 4e0d685dbda4bae9)
- `probe/p14_refs_and_paths.py` (added, sha256 c85ee073286d337b)
- `probe/p15_check_uncommitted.py` (added, sha256 7461be09fe30947f)
- `probe/p16_rejection_markers.py` (added, sha256 70ef729787f0e45b)
- `probe/p1_credential_refusal.py` (added, sha256 0649264d7d035c60)
- `probe/p2_untracked_no_upstream.py` (added, sha256 8d00cba0b39f5ff3)
- `probe/p3_happy_and_diverged.py` (added, sha256 1cdeef1b21676631)
- `probe/p4_argv_guard.py` (added, sha256 4fd64246838fb55b)
- `probe/p5_push_failures.py` (added, sha256 0501b477aa44b2aa)
- `probe/p6_check_published.py` (added, sha256 a115ffcfca95e824)
- `probe/p7_verify_semantics.py` (added, sha256 b52ac2b548e467b3)
- `probe/p8_readback_raise.py` (added, sha256 c11a602b34d81c09)
- `probe/p9_index_vs_commit.py` (added, sha256 6e04e3da4bfd9d5d)
- `probe/util_codes.py` (added, sha256 5a306fc0f3b38106)
- `review/publish.md` (added, sha256 6fb7fca1a4e49ccf)

Reasoning characters per turn: 25, 247, 27070, 17838, 6776, 461, 643, 0, 212, 0, 0, 0, 0, 0, 0, 255, 0, 0, 3980, 0, 0, 0, 9966, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116

Expected outputs present: review/publish.md, probe/; missing: (none)

### b-01-surface — files written
- `tests/loop/test_surface.py` (added, sha256 01915ca3c00a5cae)

Reasoning characters per turn: 26, 129, 0, 0, 4871, 0, 5464, 0, 854, 0, 156, 0, 330, 181, 145, 175, 0, 153

Expected outputs present: tests/loop/test_surface.py; missing: (none)

### b-02-seats — files written
- (none)

Reasoning characters per turn: (none)

Expected outputs present: (none); missing: (none)

### b-03-obligations — files written
- `tests/loop/test_obligations.py` (added, sha256 a2261e97d2dd82e5)

Reasoning characters per turn: 26, 0, 96, 4136, 1495, 6702, 215, 0, 0, 1630, 0, 266, 65

Expected outputs present: tests/loop/test_obligations.py; missing: (none)

### b-04-steps — files written
- `tests/loop/test_steps.py` (added, sha256 c1711fd9dd0d6e5d)

Reasoning characters per turn: 41, 71, 137, 0, 314, 2979, 0, 3942, 149, 4201, 0, 608, 470, 0, 0, 1277

Expected outputs present: tests/loop/test_steps.py; missing: (none)

### c-01-packs — files written
- `src/minireason/loop/packs.py` (added, sha256 72574fa0889bdf4a)
- `tests/loop/test_packs.py` (added, sha256 962a5cd445a20491)

Reasoning characters per turn: 26, 0, 145, 0, 286, 239, 0, 0, 6499, 0, 706, 660, 0, 0, 0, 0, 0, 78, 0, 120, 0, 0, 748, 0, 111, 0, 0, 384, 0, 0, 0, 212

Expected outputs present: src/minireason/loop/packs.py, tests/loop/test_packs.py; missing: (none)

### c-02-roles — files written
- `src/minireason/loop/roles.py` (added, sha256 fc47b57727205850)
- `tests/loop/test_roles.py` (added, sha256 114774214a0089c6)

Reasoning characters per turn: 26, 0, 0, 0, 204, 0, 19503, 135, 0, 278, 200, 0, 0, 0, 1338, 0, 0, 177, 0, 290, 69, 0, 0, 0, 0, 0

Expected outputs present: src/minireason/loop/roles.py, tests/loop/test_roles.py; missing: (none)

### c-03-markprep — files written
- (none)

Reasoning characters per turn: 26, 0, 213, 6276, 679, 363, 8382, 837

Expected outputs present: (none); missing: src/minireason/loop/markprep.py, tests/loop/test_markprep.py

### c-04-decide — files written
- `src/minireason/loop/decide.py` (added, sha256 2cf2504d898fdb5f)
- `tests/loop/test_decide.py` (added, sha256 92a4fcd49dc01472)

Reasoning characters per turn: 19, 83, 286, 757, 10468, 388, 13422, 5124, 2180, 285, 11764, 0, 1915, 0, 360, 0, 834, 276, 0, 172, 0, 366, 0

Expected outputs present: src/minireason/loop/decide.py, tests/loop/test_decide.py; missing: (none)

### d-01-receipt — files written
- `out/receipt.md` (added, sha256 79deba22d2e1cfb4)

Reasoning characters per turn: 21, 26, 37, 0, 0, 169, 125, 619, 0, 220

Expected outputs present: out/receipt.md; missing: (none)

### e-02-metric-creep — files written
- `out/metric-creep.md` (added, sha256 6c1c6213c299f255)
- `probe/probe_audit_thresholds.py` (added, sha256 b782d993c5435dfc)
- `probe/probe_integer_oracle.py` (added, sha256 156bd399e0816c25)
- `probe/probe_preflight_reconciliation.py` (added, sha256 c220110a1776292a)

Reasoning characters per turn: 15, 61, 6298, 118, 11007, 0, 0, 0, 2668, 0, 37

Expected outputs present: out/metric-creep.md, probe/; missing: (none)
