# kimi-k3 worker battery

| id | title | mode | iters | tool calls | tokens | wall s | finish | harness failure |
|---|---|---|---|---|---|---|---|---|
| a-01-types | Adversarial review of W0-TYPES (types) | tools | 14 | grep 9, list_dir 8, read_file 13, run_command 1 (31) | 519105 | 295.0 | length | - |
| a-02-contracts | Adversarial review of W0-CONTRACTS (contracts) | tools | 56 | grep 2, list_dir 4, read_file 14, run_command 28, write_file 20 (68) | 5229222 | 599.1 | stop | - |
| a-03-standard | Adversarial review of W0-STANDARD (standard) | tools | 6 | read_file 8 (8) | 174302 | 168.9 | length | - |
| a-05-receipts | Adversarial review of W0-RECEIPTS (receipts) | tools | 3 | read_file 4 (4) | 61246 | 156.6 | length | - |
| a-06-publish | Adversarial review of W0-PUBLISH (publish) | tools | 6 | list_dir 2, read_file 7, run_command 1 (10) | 119600 | 183.9 | - | HTTP_500 |
| b-01-surface | Unit tests for W1-SURFACE (surface) | tools | 11 | grep 4, list_dir 1, read_file 11, run_command 3 (19) | 883728 | 357.6 | length | - |
| b-02-seats | Unit tests for W1-SEATS (seats) | tools | 6 | grep 1, list_dir 1, read_file 10, run_command 1 (13) | 193855 | 206.9 | length | - |
| b-03-obligations | Unit tests for W1-OBLIGATIONS (obligations) | tools | 8 | grep 5, read_file 16, run_command 1 (22) | 481833 | 313.6 | length | - |
| b-04-steps | Unit tests for W1-STEPS (steps) | tools | 14 | grep 3, read_file 15, run_command 2 (20) | 766392 | 313.4 | - | HTTP_500 |
| c-01-packs | Implement W2-PACKS (packs) with its tests | tools | 17 | grep 3, list_dir 2, read_file 27, run_command 1 (33) | 1243934 | 206.5 | - | HTTP_500 |
| c-02-roles | Implement W2-ROLES (roles) with its tests | tools | 14 | grep 4, list_dir 2, read_file 19, run_command 1 (26) | 910356 | 216.5 | length | - |
| c-03-markprep | Implement W2-MARKPREP (markprep) with its tests | tools | 8 | grep 1, list_dir 1, read_file 15 (17) | 376885 | 175.1 | length | - |
| c-04-decide | Implement W2-DECIDE (decide) with its tests | tools | 17 | grep 5, read_file 18, run_command 3, write_file 1 (27) | 1313162 | 282.3 | length | - |
| d-01-receipt | Receipt paragraph in house style from a fact sheet | tools | 5 | list_dir 3, read_file 5 (8) | 43990 | 151.7 | - | HTTP_500 |
| e-02-metric-creep | Metric creep in standard.py and types.py | tools | 3 | read_file 7 (7) | 92947 | 165.1 | length | - |
| f-02-commit-tree | Check every published commit/tree identity in REC-20260914-U and -X | tools | 7 | list_dir 5, read_file 5 (10) | 116994 | 171.3 | length | - |
| b-004 | Packed-context variant of b-001 (fallback mode) | packed | 2 | run_command 2 (2) | 27972 | 281.0 | length | - |

Totals: 17 task(s), 12555523 tokens, 325 tool calls, 4 harness failure(s).

### a-01-types — files written
- (none)

### a-02-contracts — files written
- `probe/__init__.py` (added, sha256 e3b0c44298fc1c14)
- `probe/p01_totality.py` (added, sha256 d4056f4b743825bf)
- `probe/p02_exceptions.py` (added, sha256 dbc74a276741891e)
- `probe/p03_outside_vocabulary.py` (added, sha256 6179e97deac09a14)
- `probe/p04_g12.py` (added, sha256 470898acf86c323e)
- `probe/p04b_warrant.py` (added, sha256 f4b390ae19c2b5a5)
- `probe/p05_identity.py` (added, sha256 f6ad8e2ec7a5d749)
- `probe/p06_schemas.py` (added, sha256 fc66d8593d5b3c31)
- `probe/p06b_restore.py` (added, sha256 2f1b363dab92477d)
- `probe/p07_transcript.py` (added, sha256 92afa871f37816c3)
- `probe/p08_shapes.py` (added, sha256 2183bd7a394565d2)
- `probe/p09_headers.py` (added, sha256 de337ab5c7b65c6f)
- `probe/p10_misc.py` (added, sha256 5ca721e137e63f64)
- `probe/p11_roundtrip.py` (added, sha256 f5d0a2557dbd2787)
- `probe/p12_aggregate.py` (added, sha256 c10ee4b00f86cbc9)
- `review/contracts.md` (added, sha256 f32bec4da892b731)

### a-03-standard — files written
- (none)

### a-05-receipts — files written
- (none)

### a-06-publish — files written
- (none)

### b-01-surface — files written
- (none)

### b-02-seats — files written
- (none)

### b-03-obligations — files written
- (none)

### b-04-steps — files written
- (none)

### c-01-packs — files written
- (none)

### c-02-roles — files written
- (none)

### c-03-markprep — files written
- (none)

### c-04-decide — files written
- `src/minireason/loop/decide.py` (added, sha256 11cea6522c423530)

### d-01-receipt — files written
- (none)

### e-02-metric-creep — files written
- (none)

### f-02-commit-tree — files written
- (none)

### b-004 — files written
- (none)
