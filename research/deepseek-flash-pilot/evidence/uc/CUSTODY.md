# Run custody

Captured 2026-09-17T15:54:13.046141+00:00; root-w43. All 1303 files in the sixteen run trees were SHA-256 hashed (116,651,073 bytes). No run was modified. Full trees are deliberately not copied. Only 33 original artifact/continuation files and exact artifact extractions are copied, totaling 147,088 bytes; all copied absolute paths are shorter than200 characters. [RUN-SHA256.json](RUN-SHA256.json) records every original path/size/hash; [COPY-MANIFEST.json](COPY-MANIFEST.json) records every copy and extraction.

| Run | Files | Bytes |
|---|---:|---:|
| UC1 | 208 | 73,185,171 |
| UC1-attempt1-20260917T1356Z | 38 | 803,217 |
| UC1-attempt2-20260917T1424Z | 76 | 2,247,765 |
| UC1-attempt3-20260917T1502Z | 134 | 4,584,952 |
| UC2 | 76 | 1,542,952 |
| UC2-attempt1-20260917T1356Z | 32 | 556,661 |
| UC2-attempt2-20260917T1424Z | 45 | 955,924 |
| UC2-attempt3-20260917T1502Z | 57 | 1,342,860 |
| UC3 | 75 | 1,952,700 |
| UC3-attempt1-20260917T1356Z | 37 | 822,116 |
| UC3-attempt2-20260917T1424Z | 44 | 1,150,818 |
| UC3-attempt3-20260917T1502Z | 115 | 5,194,517 |
| UC4 | 193 | 15,511,787 |
| UC4-attempt1-20260917T1356Z | 41 | 1,197,049 |
| UC4-attempt2-20260917T1424Z | 47 | 1,746,827 |
| UC4-attempt3-20260917T1502Z | 85 | 3,855,757 |

Secret scan: every regular file in the sixteen run trees was checked for credential key names and common secret-shaped values (sk tokens, GitHub tokens, private-key headers, bearer values, long quoted key assignments). Zero secret-value patterns were found; key NAME references do occur in endpoint/config/prose records and are reported as names/counts, never values. No .env or environment key values were read. [SECRET-SCAN.json](SECRET-SCAN.json) is the full scoped result. Copies are exact subsets or exact substrings of scanned artifacts, and receive a second delivery scan. This confirms no detected persisted key value in the requested scope; pattern scanning cannot prove absence of an arbitrary unrecognized secret format. Hidden-reasoning fields in call outcomes report false; public prose was retained.

Original RUN.md, TRACE.md, result.json, pass files, child records, every call/repair/preflight, verification and events are bound by the manifest. Inventory metrics are a separately generated reading, not replacements for originals. Historical amendments and partial artifacts retain their original statuses. Judge and publisher follow; no Git mutation or publication was performed.
