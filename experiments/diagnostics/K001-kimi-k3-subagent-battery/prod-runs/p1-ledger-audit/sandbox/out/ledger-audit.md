# Mechanical audit of `docs/DECISION_LEDGER.md`

Subject file: `docs/DECISION_LEDGER.md`. Computed by the scripts under `check/`; no value is transcribed.

## 1. Line census

| metric | value |
|---|---|
| total lines | 1495 |
| lines ending CRLF (\r\n) | 37 |
| lines ending bare LF (\n) | 1458 |
| unterminated final line count | 0 |

CRLF line numbers: 924, 926, 928, 930, 932, 934, 936, 938, 942, 944, 948, 950, 954, 956, 958, 960, 964, 966, 970, 972, 976, 978, 982, 984, 988, 990, 992, 996, 998, 1000, 1002, 1004, 1006, 1008, 1010, 1012, 1204

## 2. Receipt ids (`REC-\d{8}-[A-Z]+`), first-appearance order

Distinct ids: **37**

| id | first appearance line | lines carrying id |
|---|---|---|
| REC-20260912-B | 524 | 12 |
| REC-20260912-C | 529 | 6 |
| REC-20260912-D | 586 | 14 |
| REC-20260912-E | 617 | 9 |
| REC-20260912-F | 626 | 7 |
| REC-20260912-G | 655 | 42 |
| REC-20260912-H | 741 | 44 |
| REC-20260913-I | 829 | 29 |
| REC-20260913-J | 879 | 24 |
| REC-20260913-K | 918 | 33 |
| REC-20260913-L | 1002 | 59 |
| REC-20260914-A | 1194 | 6 |
| REC-20260914-B | 1198 | 24 |
| REC-20260914-C | 1214 | 1 |
| REC-20260914-D | 1232 | 4 |
| REC-20260914-E | 1238 | 1 |
| REC-20260914-F | 1244 | 3 |
| REC-20260914-G | 1252 | 3 |
| REC-20260914-H | 1266 | 3 |
| REC-20260914-I | 1274 | 2 |
| REC-20260914-J | 1282 | 2 |
| REC-20260914-K | 1288 | 3 |
| REC-20260914-L | 1294 | 3 |
| REC-20260914-M | 1302 | 2 |
| REC-20260914-N | 1308 | 4 |
| REC-20260914-O | 1314 | 3 |
| REC-20260914-P | 1324 | 3 |
| REC-20260914-Q | 1332 | 5 |
| REC-20260914-R | 1340 | 3 |
| REC-20260914-S | 1350 | 8 |
| REC-20260914-T | 1380 | 11 |
| REC-20260914-U | 1392 | 14 |
| REC-20260914-V | 1427 | 13 |
| REC-20260914-W | 1447 | 5 |
| REC-20260914-X | 1455 | 12 |
| REC-20260914-Y | 1473 | 5 |
| REC-20260914-Z | 1481 | 8 |

## 3. Today's receipts (date 20260914)

| metric | value |
|---|---|
| distinct ids dated 20260914 | 26 |
| letter sequence (first-appearance order) | A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z |
| single-letter suffixes present | A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z |
| A..Z fully used? | yes |
| any id after Z (two-or-more-letter suffix)? | no |
| two-or-more-letter ids | (none) |

## 4. Entry count under three definitions (no single count chosen)

| definition | count |
|---|---|
| (a) lines beginning with REC- — Lines with content starting with 'REC-' at column 0 (line.startswith('REC-')). | 381 |
| (b) lines beginning with REC- or **REC- — Lines with content starting with 'REC-' or with the markdown bold opener '**REC-' at column 0. | 381 |
| (c) paragraphs opening with REC- or **REC- — Blank-line separated blocks (blank = empty or whitespace-only) whose first non-space token starts with 'REC-' or '**REC-'. | 364 |

Detail line numbers are in `ledger-audit.json` (`entry_counts.*.line_numbers` / `first_line_numbers`).

## 5. Lines containing `Prior verified commit/tree:`

| metric | value |
|---|---|
| line count | 25 |
| line numbers | 1224, 1230, 1236, 1242, 1248, 1250, 1254, 1256, 1258, 1260, 1262, 1264, 1270, 1272, 1278, 1280, 1392, 1427, 1447, 1455, 1469, 1473, 1477, 1481, 1493 |

## 6. `VERIFIED <40 hex> TREE <40 hex>` lines

Matches: **77**

| line | commit | tree | nearest receipt id above |
|---|---|---|---|
| 942 | `b8a77a5521aff3976a93b39b447282ed3caa62de` | `546079eb29eeb1c9ba981d092641feeb0a3be465` | REC-20260913-K (line 940) |
| 948 | `393a2720a418aba6a76a13ba0283fbada9bf415a` | `725e43baa5236a63e921f18c9ca796d15a92d139` | REC-20260913-K (line 946) |
| 954 | `59785ba28474ffcb63e574ef42b459cbe390e8fc` | `2c04c7a0e3dbd0a9e413ec301870d561b96dbd55` | REC-20260913-K (line 952) |
| 964 | `eb5e5cf7dda473df40e5b6e744f035832c57e848` | `ad6b41c413590277f0f8f87c3947384622e86116` | REC-20260913-K (line 962) |
| 970 | `1634f569481c2c127cc0f0dcbafa806c0e53d3e3` | `e0a8e22546dec4268f1eb8f6c59800ca239ef097` | REC-20260913-K (line 968) |
| 976 | `7ab66682b85c734f9addb5a9a9aeecdea5222912` | `1c13d7c62eaa0b3a80f1514d3aa25dfc89970829` | REC-20260913-K (line 974) |
| 982 | `8e095dc6ec2d337c18c1327ea777f5b630f738d9` | `dbe14897e8911d4ea87f44942587b6d90867414f` | REC-20260913-K (line 980) |
| 988 | `edb5d59208be043e78c01ab04b86fd8f4afc26a2` | `5721518b69c0a403be80a8b6dd0406cfc1336b98` | REC-20260913-K (line 986) |
| 996 | `39aab1d627b00273c8bac5c488a7d3b24852105d` | `076a988e4e8a462899acecf26ac9985e5041c2cc` | REC-20260913-K (line 994) |
| 1020 | `8d07a7733ea482ca139080c7955295fc0b0f02b7` | `115b1052b7b0af2a6884266e0a60e9375e2c4e46` | REC-20260913-L (line 1018) |
| 1024 | `1a2bccf24fa3f5b38dd5d38161ca46215ca5616b` | `0f52d513aeddd073ab771fea61b8892cd96a0378` | REC-20260913-L (line 1022) |
| 1030 | `590d41451a96183e3547a341b56129c0c7d3ac0d` | `100341551e9827c2c7d7427fc9e30b9151329084` | REC-20260913-L (line 1028) |
| 1036 | `9eb522d0a3de08f091ca4563b8e72c1b02d35b54` | `c953cd7de023de7c91cf90b66976b96eb976425e` | REC-20260913-L (line 1034) |
| 1044 | `5166e58dda30eed30bfc1d0a27f1dad1b96e9ddb` | `ccec500c2bcf4f89a0db85b84fd6a2191ba693b8` | REC-20260913-L (line 1042) |
| 1050 | `6fedd193fce01639b2aaf2fe1e4c2a99b48fcfd5` | `0eb54de1d1fa0b5ea6c2cfa25b58fa8841b3a91c` | REC-20260913-L (line 1048) |
| 1054 | `0c466bbc9bb7cbacd63b9a2f95496a456f9dfc37` | `a04fe9d66d649358b2b1ced2317784548906a149` | REC-20260913-L (line 1052) |
| 1062 | `454ee1c9d9993e9cda8323bde1e92dd6bdfef09d` | `7ed3291a0d0c0b83cff4cf189f8314b897f6e2c2` | REC-20260913-L (line 1060) |
| 1070 | `15a4cb65b8d3598f0b9649673fc7916621583d8a` | `2ed492a85f7b960e663a2aed7b8059578b922eb5` | REC-20260913-L (line 1068) |
| 1078 | `8c5d0b8c623c5c364b5971dce9760d5f3594ee52` | `96f7856ccd1faae4ce455453542ea6e8aafad247` | REC-20260913-L (line 1076) |
| 1085 | `ef8752f3594b3866ea4a9df6856cacddedb3f169` | `30b461cb4c2f8ce5d3678ba3798e37113d9bce12` | REC-20260913-L (line 1083) |
| 1092 | `5d153f56417bea7b925959e7d402bb94cb7dce74` | `122acb4ece0ad01105db7cc4fba252ad298a7588` | REC-20260913-L (line 1090) |
| 1096 | `0557249bff5a437de52f74677de63776d5b5f0bf` | `8120a66a9a85b8fc016075f71e1f9554c220642f` | REC-20260913-L (line 1094) |
| 1100 | `d310795fae84039222c68fcb82f5167777f705ce` | `3f623f16f4a160af5401927e37cca6293b0b5489` | REC-20260913-L (line 1098) |
| 1109 | `ba617f3a0e08b88e252320ffd0492791e88ed19f` | `b63fbbf2328f8b37767c9d34295360e4e32d6652` | REC-20260913-L (line 1107) |
| 1116 | `ad0e9e02c0c74c687639b27ae13a1cc415ec0500` | `6c721d8301f21271b9833c6d9a4ff406af929f10` | REC-20260913-L (line 1114) |
| 1123 | `c58dd790822bca5d0f5084b2d392c6478e9d8043` | `93ee9e81d58b025518ad9e4b5198debfcf07bd65` | REC-20260913-L (line 1121) |
| 1130 | `a593701cceea2785fd76925fb8bc25787e2dcc69` | `fdc96f17c4d40782c62c68864f7f87ef8b6c9260` | REC-20260913-L (line 1128) |
| 1137 | `bbfa1cd9127bd449f2b411d06c1c7094aa7795e3` | `e9ea136c5393702a71982b8fd527dd9edcdc066e` | REC-20260913-L (line 1135) |
| 1141 | `1ec3cc7f2b2404e2ed196c93c1ac2d72df7c9d7b` | `ec93654f949c41a865821996cca0ced76549df12` | REC-20260913-L (line 1139) |
| 1148 | `166ac59ad45d8e50c9f327d8270aa921c88d3095` | `f29aa03f5209332ffe71a0a0a1cde6cd462c561a` | REC-20260913-L (line 1146) |
| 1155 | `4e9532fd57cba3238a221b89a8fc93c70f3db66d` | `5119eb20d9dcd026eb889dd5d26a08e1eba4b6a8` | REC-20260913-L (line 1153) |
| 1164 | `8d0c87ed483f3951bc5275d3a3d3684024895afd` | `548f8936d45a01ef2481deb6d7da819ba91b3692` | REC-20260913-L (line 1162) |
| 1168 | `ea48fd676520f63417c9856f08e6058c1f6feb49` | `aa1056199555bd180c030f7ebc1deee5b5212afa` | REC-20260913-L (line 1166) |
| 1172 | `459ca775750f2d4998080337a2539014d25c0ac6` | `b8c08eeaabb0b6af6cb110cbc8960e626cfd0d5e` | REC-20260913-L (line 1170) |
| 1176 | `14e1a75e72b1f19664082bb3dc65bef95fc4b797` | `9e2de4d41094357eece2480d7dfd1304baa6934d` | REC-20260913-L (line 1174) |
| 1180 | `2b6affd4a13ccf42afa747e09d274783969080cc` | `2e164837198e6d3bead228bfd056c1806b171894` | REC-20260913-L (line 1178) |
| 1184 | `0ecef2654df3d2e8e9cd94b682196c54b0abe31b` | `9303f2f80c8322fcbe42cefd00c2bb5f06e3a591` | REC-20260913-L (line 1182) |
| 1188 | `2c514664c2b6bfd58286c7aa292b477678ddeb86` | `651a83da2be2aa39fde1983e80e5d2378ff35cda` | REC-20260913-L (line 1186) |
| 1204 | `5dbac3724d8fdf83bb13b952d0415501a56e3699` | `066f83993df8479297f3221c6cc42db9a71ba1bf` | REC-20260914-B (line 1202) |
| 1208 | `4ef269b6152c91b1f1cca89b3c89693eba77803f` | `de24837540cb4bd80167dfb7689f6cfcf75809ba` | REC-20260914-B (line 1206) |
| 1212 | `44550f565b806d1ff343c66a0e8855334263d0c4` | `c0ea553bc76eef020ecb7432fbb9c040d0f51897` | REC-20260914-B (line 1210) |
| 1218 | `b02ef276fb7d90ee4ff563bbcc8b33efae4bfd00` | `4e8e4f2c0a9257c99e210745d0ccc2ffffdb41e3` | REC-20260914-B (line 1216) |
| 1222 | `d671dc9290b554d978d6b84b15b511a5d5530036` | `62a93be23479e805cd2b9a46f5cad504a6c43438` | REC-20260914-B (line 1220) |
| 1228 | `ca7db9a3b4ab06999fd2262d5875e3be6d79817e` | `7d87b80cb3274011779322f11b81b6680eb90237` | REC-20260914-B (line 1226) |
| 1234 | `b55832f684f91729ade4317465c748f891aa522a` | `7edef50c95f9a566df8633f3a9eb43892413ea9f` | REC-20260914-D (line 1232) |
| 1240 | `554e0dc02155d4cbf5f012b72c08825dd248fa71` | `0272b4a02d12e2854f399364d51f9f5152262cb3` | REC-20260914-D (line 1238) |
| 1246 | `38bde7dc5b4d657969d229f2a602e3577ec80d4e` | `501d29b3bd1add8e876ee826f94042a65105b0e5` | REC-20260914-F (line 1244) |
| 1268 | `c40dda76579ebd3f1b873598f6d8c6c06d39c777` | `31e5f165046d36f04d0a2ea878d18d2da1893872` | REC-20260914-D (line 1266) |
| 1276 | `22dc9f3450041fbca1298dc8b5763c1e4bbbc1e2` | `b4c516c48fc81b788bb2067c2902706d3dd23c9c` | REC-20260914-H (line 1274) |
| 1286 | `20b82184b6cd69415b2d5ae743afda53df321b93` | `995cb82574f2a4b4cb372e31b1e0310827c29eb5` | REC-20260914-I (line 1284) |
| 1292 | `ffbb9f3fe1f65fff4dc74d4afca7daaf53051c49` | `05228b5150b5091666bc20997e2bf8c1123838d1` | REC-20260914-H (line 1290) |
| 1298 | `8d5f149ddb07b5556f4d2f89c10e0bf2b8c8800e` | `cc2cc151d6c5a28760126ed788a3f115f8ab0400` | REC-20260914-K (line 1296) |
| 1300 | `5bb083a3fbae926b35c5da507f8e08a4ef448012` | `5447572f35318e0dadf31a11aadc73aafe92b022` | REC-20260914-K (line 1296) |
| 1306 | `649ae2b69bcabf44f828e8806883db3bd8762afb` | `29271e92a537a0499bfda94fa7a67a49597b03ff` | REC-20260914-L (line 1304) |
| 1308 | `1feed77c3e39acf69271b960f0b5e1e1b4743ea9` | `38b07b0957d467d34ad7e27e7ab9cfbfed7576ae` | REC-20260914-L (line 1304) |
| 1312 | `c2366dd5a1d7e97b3abdbe15cea73167dbb46717` | `1e92dc0d0eb40a1a3fa05a8ee959644b865903e8` | REC-20260914-N (line 1310) |
| 1314 | `c2b92e1eef04cf4aa3c90ad36769718ed705b53b` | `9ad5031e740cfa90b4db274cf672321aba46c619` | REC-20260914-N (line 1310) |
| 1318 | `4d9cb75a7e25610c12c85825ee738c5d3bcc17a1` | `9b0806593175471a7e33f23f5fb3a7c78eba07b6` | REC-20260914-N (line 1316) |
| 1320 | `6e7dac00966e120a67eb90694fe0d818ae8c07e4` | `bbf87ffec67b825744eccf2b14537544de8cdb46` | REC-20260914-N (line 1316) |
| 1322 | `0ae29ee9dd6f83ad18428dcef6fbc0f3fb0f5269` | `d3d42fad4b1a55516be5ec3f68ca9044e8df1599` | REC-20260914-N (line 1316) |
| 1326 | `4cac6b342a647bc1348fec5aafcc558e8fc8f9d3` | `2942e3f414038b57c71edd6eab50f14696dfa442` | REC-20260914-P (line 1324) |
| 1330 | `63c345beea3e662f5ed940e1a993ab7da5b1ce25` | `91cc723c97cef90d7e1b4444a4c7e1aaf3cb1ab4` | REC-20260914-P (line 1328) |
| 1336 | `c2d438e9358439d4b2c84aed313cde532c833c6a` | `ebe284e4631b1180247590b82e74ec3ae229e11a` | REC-20260914-Q (line 1334) |
| 1338 | `b7136622a6c3c414083a8f85ab21c38d236b0b8a` | `403ea5fa819079a6d803dbf676b434c4f559be99` | REC-20260914-Q (line 1334) |
| 1342 | `aaaeea1bfb53b226053e6a43cdfc536c28e4b3f0` | `472915f12092c708a67dbd9e2a4d0edb2672ab94` | REC-20260914-Q (line 1340) |
| 1346 | `6114aedb3de0d06a0861229d310d7a5a40932526` | `3a110e1fa0d4d0f7e4f19b98b08f8252055f4eb4` | REC-20260914-Q (line 1344) |
| 1348 | `7e5ae00f1960f32b6c24002cfebe5727249e0906` | `470803a4ac147dca96c85177eb293185f040aa78` | REC-20260914-Q (line 1344) |
| 1362 | `f166069ab46987666275ecf3c503a4b7c2e3eb34` | `67c9d820b72eefefe9d12b3135c435cab38e25f5` | REC-20260914-S (line 1360) |
| 1364 | `1abe87ecbd9928f2a63145f79f27c50ee738322f` | `8f0014547afae299f6dc1369bd54fa7b5b6aa7b5` | REC-20260914-S (line 1360) |
| 1378 | `31522aa359d91f0bb86a82a869ed7617256433fd` | `193477c098077c4965e05476258f6d6132e92c13` | REC-20260914-S (line 1374) |
| 1429 | `2d7239acd70f14aa049b62034a803784883da7b7` | `9d0ab88f6940b220110797722fd4e628aef9c43e` | REC-20260914-U (line 1427) |
| 1449 | `dc5491e0e6d992ecd2e36b2f6c2adf7e854fe91c` | `7034b1266a8aca02b39d368d00e10a1d131e2c9c` | REC-20260914-V (line 1447) |
| 1457 | `96ca2eb3188beeb3ca1d399cddb203a9d38ec8a9` | `da1d4bff5619b9a189575e11058c3b7a66d6be7b` | REC-20260914-V (line 1455) |
| 1471 | `958f2f4173da679283388c1820d218a209dffdbb` | `79cbdfe9d1a03192d4bea8d84dc605d7862abdb8` | REC-20260914-X (line 1469) |
| 1475 | `bfc5c8e7e18ca4797566a742f94df3d4b69df1f5` | `03937a46aa681b69caf7ba4203c195c440c8cc6d` | REC-20260914-X (line 1473) |
| 1479 | `920cfc3c8968db302f5a3c30beed0a03981873c7` | `65700b3689d90e3681af134cf6f6f64141122737` | REC-20260914-A (line 1477) |
| 1495 | `c56b129dc36eaf87dcb39e0a36e9a227164c3525` | `05eebc4bbb715a83121a507dc31dc27b0818d776` | REC-20260914-Z (line 1493) |

Last such line in file: line 1495 — commit `c56b129dc36eaf87dcb39e0a36e9a227164c3525`, tree `05eebc4bbb715a83121a507dc31dc27b0818d776`, nearest receipt above REC-20260914-Z (line 1493).

## 7. Credential scan

| metric | value |
|---|---|
| patterns searched | sk-hex32; hex32-dot-token |
| hit line count | 0 |
| hit line numbers (only numbers are ever reported) | (none) |

## 8. Last five lines, verbatim

Line 1491 (`
`):

```text
REC-20260914-Z analyses outcome at 2026-09-14 11:34 UTC: Both published instruments are run over occurrence-03 at **full scope** — no `--problem`, `--arm` or `--cycle` selector — into `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/`, following the layout occurrences 01 and 02 already use: `audit.json`, `import/` and `use-table/`. **`tools/import_h005.py` exits 0** with custody **verified 18 of 18** and `event_ts_nondecreasing` true; the one skip is the usual structural one, `projection_source` running 1 of 2 because the first invocation's other projection has no exposed source (`daily/mini_fcl/cycle01/account#p.account.0`). It reports `plan_id` `9aa92a83…`, scope `daily/mini_fcl/cycle01/account` and `daily/mini_fcl/cycle01/rival`, **26 events, 4 artifacts, 0 warrants, 0 `att` edges, 0 `dep` edges**, 52 references of which **52 resolved and 0 dangling** (48 intra-document, 4 to the exposed task artifact), 0 ν artifacts, 0 reinstatements, 4 `accepted` labels and 0 `refuted`. **`error_severity_residue` is empty** — nothing of error severity fired at all, where occurrence-01's carries `ref_unresolved` 28 and occurrence-02's 153; that is a difference in what these documents happened to reference and **no merit reading may be taken from it**. **FCL-1 commitment surface on the two nodes that reached the importer: `read_fcl1` 2 of 2**, with `parse_failure` 0, `schema_failure` 0, `unavailable_decode_failure` 0 and `opaque_envelope` 0 — the contribution occurrence-03 makes to the falsifier F002 pre-registers, and nothing else in F001's fact table is re-opened. **`tools/use_relation_h005.py` exits 0** with **0 rows**, because `cross_document_rows` is 0 and the instrument walks cross-document references and nothing else; `nodes_not_read` is empty and `unresolved_refs` is empty. All four interpretive columns stay empty, which here is no rows to fill, and **the reading remains root's and is not done**. `audit.json` carries the counts already published in dispatch checkpoint 2. An occurrence-03 section is appended to the analyses README at **172 insertions and 0 deletions**, with nothing above it altered. Every `accepted` label is **accept-by-position** — there are no `att` edges, so no artifact is attacked and no `refuted` label can arise — and **no label produced by this import is a semantic attribution**.
```

Line 1492 (`
`):

```text

```

Line 1493 (`
`):

```text
REC-20260914-Z closed at 2026-09-14 11:40 UTC: State pending -> **closed**. Everything the opening receipt promised is published and verified on the working branch `claude/project-state-direction-j5rbun`, in six commits from `3c49718` through the closing one, each read back with `git ls-remote --refs origin refs/heads/claude/project-state-direction-j5rbun`. Identity: `occurrence-03/arms.json` sha256 `2a181f80eae29f0716be1fdcae1f67c38df38f096b6cbd7c7a344acbdf013b3b`, byte-identical to occurrence-01's; material `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679`, re-derived in this tree by `build/build_f002_material.py --check` printing `MATCHES`; runner `runner_sha256` = `helper_sha256` = `ccbb1165fd3bb1d14e6c9247821e9c4e67fbea09a2153339984bd7eaff5cc42e`, re-derived by `build/build_runner_v3.py --check` printing `MATCHES`; `provider_pins` unmoved at `cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db` and `03eff16b8f575c113871a1266439874b2622a75d200ecb84a1b79464aa98aee7`, and `src/minireason/data/endpoints.json` never written. **`plan_id` `9aa92a837569bd56a86b172eb56dd80dbc69c519a86286d3387b020c2709a0d5` — occurrence-01's own, exactly as this receipt's opening paragraph predicted and for the reason it gave**, `verify` true, `max_calls` 5, and `plan.json`, `material.json` and all three manifests byte-identical to occurrence-01's under `cmp`. **PER-COORDINATE OUTCOME, all five authorised coordinates.** occurrence-03 `ollama/glm-5.3`, arm `mini_fcl`, problem `daily`, cycle 1: `account` **COMPLETE**, no `failure_code`, `finish_reason` `"stop"`, **12,489** completion tokens, **114,364 ms**; `objection` **FAILED**, `TRANSPORT_OR_RESPONSE_ERROR`, no `finish_reason`, **no usage at all**, **300,453 ms**; `rival` **COMPLETE**, no `failure_code`, `"stop"`, **19,700** completion tokens, **234,864 ms**; `response` **never dispatched** — no attempt marker, no request, no provider record, no receipt; `carry` **never dispatched** — the same. No usage block carries a `reasoning_tokens` field, so that column is absent rather than zero; `reasoning_content_present` is true on both COMPLETE records and null on the FAILED one. Three calls spent of five authorised: **2 COMPLETE, 0 PARTIAL, 1 FAILED, 0 OPAQUE, 0 unresolved attempts, 0 out of scope**, `unvisited` 2, `fence_stripped` 2, `lenient_control_chars` 0, `strict_parse_would_succeed` **0 of 2**, known usage 32,189 completion and 34,333 total tokens, `unknown_usage_calls` 1 — the FAILED call, whose cost stays unknown. **DID THE 300-SECOND CLOSE RECUR: YES.** `mini_fcl/objection` ended at **300,453 ms** with **`"Remote end closed connection without response"`** against `settings.timeout_seconds` 600 and `request.max_tokens` 32768 both present in the provider record — the same error string, the same band and the same shape as occurrence-01's `response` at 300,270 ms, at a **different node** on a **different request** **63 minutes later**. **Maximum elapsed, against both bounds and against the undeclared one**: longest call of any kind **300,453 ms** — **50.1 % of the declared 600,000 ms clock** and **100.2 % of the ~300,000 ms host wall**; longest call that returned **234,864 ms** (39.1 % of the clock, 78.3 % of the wall); largest completion **19,700 of 32,768** (60.1 %); **`finish_reason: "length"` occurs zero times across all three spent calls**, so nothing here is ceiling-caused, and **no call was refused by the 600-second clock**. One call ran past the 180-second wall the endpoint record declares and returned: `rival` at 234,864 ms. **THE WALL, STATED AS PRECISELY AS THE RECORDS ALLOW AND NO FURTHER.** Five closes carrying that exact string are known to this publisher, inside a **183-millisecond band around 300.3 s**: 300.270 s (F002 occurrence-01 `response`, `ollama/glm-5.3`, 10:20 UTC), 300.286 / 300.348 / 300.377 s (three requests of a separate worker process on `ollama/kimi-k3` at 600 s and 32,768, 11:07 UTC — untracked scratchpad transcripts in another harness's schema, **not** `minireason.call.v2` records, read and verified by this publisher and cited with those limits in this decision's correction paragraph) and 300.453 s (occurrence-03 `objection`, `ollama/glm-5.3`, 11:23 UTC). **Two model families, two client processes, two different fork5 nodes — so the close follows neither a node, nor a position in the chain, nor one endpoint: a host gateway closes a request still open at about 300 seconds, and F002's declared 600-second clock cannot be exercised past 300 s on this host.** Why it closes is **not known and is not guessed at** — nothing here says whether 300 s is fixed policy, whether the closing party is the provider or an intermediary, or whether payload, model, concurrency or the shared credential's load bears on it — and **no retry was made at any layer**. **It is a resource observation and never a semantic one**: no claim about how `ollama/glm-5.3` or `ollama/kimi-k3` reasons may be read off a closed socket, two closes on one endpoint and three on another rank nothing, and **one call is one call** however many of them there now are. **WHAT THIS DECISION DID NOT DO.** It did not close F001 occurrence-07's residue: `mini_fcl/response` and `mini_fcl/carry` still have **no terminal COMPLETE record anywhere** — 07 never dispatched them, F002 occurrence-01 lost `response` to the close and never dispatched `carry`, and occurrence-03 lost `objection` and never dispatched either. Three occurrences have now ended that arm early at three different nodes, and this receipt reports that rather than a shortfall dressed as something else. It did not modify, relabel, repair, re-send or supersede **any** F001 or F002 record; nothing was written inside `F001-fork5-multifamily/` or `C001-contrast-triple/`; `material.json` was not extended and no existing entry was edited. **Analyses**: both published instruments at **full scope** into `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/`, following the layout occurrences 01 and 02 use. `tools/import_h005.py` exits 0, custody **verified 18 of 18**, `event_ts_nondecreasing` true, one structural skip (`projection_source` 1 of 2); 26 events, 4 artifacts, **0 `att` edges, 0 warrants, 0 `dep` edges, 0 ν artifacts**, 52 references with **52 resolved and 0 dangling**, 4 `accepted` labels and 0 `refuted`, and **no error-severity residue fired at all**. **FALSIFIER CONTRIBUTION, in the terms PLAN.md pre-registers and no others**: the `mini_fcl` FCL-1 parse outcome on the nodes that reached the importer is **`read_fcl1` 2 of 2**, with `parse_failure` 0, `schema_failure` 0, `unavailable_decode_failure` 0 and `opaque_envelope` 0; `strict_parse_would_succeed` is **0 of 2**, so both surfaces were read only after the declared `fence_stripped` repair, and the figure comparable with H005 occurrence-01 is the strict one. Nothing else in F001's fact table is re-opened, the falsifier is neither restated nor weakened, and **the reading remains root's and is not done**. `tools/use_relation_h005.py` exits 0 with **0 rows** (`cross_document_rows` 0; 48 intra-document, 4 to the exposed task artifact, 0 unresolved), every interpretive column empty. **Suite**, invocation beside the numbers as `docs/lessons/operations.md` requires: `PYTHONPATH=src python3 -X utf8 -m unittest discover -s tests` reported **Ran 1450 tests in 187.754s, OK (skipped=1)**, run **once**, directly and not wrapped in the activity logger per E028; adding one `arms.json` adds no test. **Credential scan**: the final pass covered the whole F002 study directory, the whole F002 analyses directory, the decision ledger, STATUS, both workflow pages and the activity log — **267 files**, at full, 12-character and 6-character length for both key names in the gitignored `/home/user/miniReason/.env`, loaded into the scanner's own process and neither printed nor written — **0 matches**; earlier per-commit passes ran at 2, 104, 113, 123, 125, 141 and 4 files, every one of them 0. **Concurrency and credentials**: one coordinator process; the dispatch wrapper passed **`OLLAMA_API_KEY` alone** and removed `DEEPSEEK_API_KEY` from the child environment, printing only `['OLLAMA_API_KEY']` and `DEEPSEEK_API_KEY in child env: False` and never a value or fragment; **at most two requests in flight**, held there by dispatching one occurrence per `send-round` with no two rounds overlapping rather than by a flag, since the v3 CLI exposes none and its per-key gate is five — 2 beside the concurrent worker battery's 8 is exactly the owner's authorisation of 10 and never above it; **zero retries at every layer**; write-once records with `NO_REPLAY`; and each wave's inputs committed, pushed and read back before that wave was sent. **DEVIATIONS.** One was declared in the opening receipt before it was taken and is the substantive one: **occurrence-03 does not have its own `plan_id`** and shares occurrence-01's, because plan identity is content-addressed over the material, arms, scope, pins and runner and carries no occurrence name; the seed stayed at 7 deliberately, there being no plan-level replay refusal to evade and no honest reason to change the condition under observation. One was forced by the evidence and is recorded in this decision's **correction paragraph at 11:22 UTC**, appended rather than edited into the opening receipt: that receipt's inference that the close was "a one-off so far" is **withdrawn**, its scan of the branch remaining true while the inference from it does not, on three verified further closes outside the repository. Two are cadence facts: the planned cadence was **1 / 2 / 1 / 1** and the actual was **1 / 2**, the shortfall being the truncation rule working and not a refusal; and the register's own operating sequence names four rounds and five pushes, where this decision made six commits. The opening receipt is the only paragraph of this decision whose reading was corrected, and no paragraph above this one is edited. **Cadence**: five-minute publication was kept, with no mid-round commit touching any file under the study directory while a round was open. `git status --short` is empty and nothing is untracked. Prior verified commit/tree: `4ff209bb04e27289d1994bbd89b2391b64a29bbb` / `d3a89d46d8912789e053753cac408a936618ed0a`. **NO FURTHER F002 PROVIDER CALL IS AUTHORIZED**: a fourth occurrence, a retry of either closed coordinate, or a run under a clock chosen against the ~300-second wall would each be a new decision needing its own receipt and its own reason, and none is taken here. **No pull request was opened.** Publication to `main` remains **pending owner merge**. The next authorized task is the reading, which is root's and is not done.
```

Line 1494 (`
`):

```text

```

Line 1495 (`
`):

```text
REC-20260914-Z verified publication at 2026-09-14 11:42 UTC: The closing receipt above named its prior verified checkpoint but could not name its own, since a commit cannot contain its own identity. It is recorded here: the closing commit is **VERIFIED c56b129dc36eaf87dcb39e0a36e9a227164c3525 TREE 05eebc4bbb715a83121a507dc31dc27b0818d776** on remote `claude/project-state-direction-j5rbun`, read back with `git ls-remote --refs origin refs/heads/claude/project-state-direction-j5rbun`, with the working tree clean and nothing untracked at that commit. The decision's six commits, each pushed and read back in turn: **`3c49718`** / tree `23bae77`, the opening receipt alone, before any occurrence-03 file existed in a commit; **`f11f350`** / tree `d1c4197`, `occurrence-03/arms.json`, the frozen `plan.json`, the occurrence's `material.json`, all three manifests and `wave0001` with its one request and trace, together with the publication-outcome and correction paragraphs; **`90d55fb`** / tree `b49b68f`, round 1's records and `wave0002`'s inputs with dispatch checkpoint 1; **`341c29c`** / tree `674fa0b`, round 2's records with dispatch checkpoint 2 — the round in which the close recurred; **`4ff209b`** / tree `d3a89d4`, the occurrence-03 analyses directory, both instruments at full scope, the audit and a 172/0 append to the analyses README, with the analyses-outcome paragraph; and **`c56b129`** / tree `05eebc4`, the 78/0 append to the F002 register, the 84/0 append to `docs/workflows/fork5-multifamily.md`, the one new row in the workflow index, the 60/0 STATUS section inserted ahead of the existing ones with nothing above it touched, and the closing receipt. **Publication preceded every dispatch**: `wave0001` was sent against `f11f350` and `wave0002` against `90d55fb`, each admitted by `check_published`, which byte-compares the transitive closure of the wave's inputs against the commit HEAD points at and refuses `PUBLISH_REF_CHANGED` or `INPUT_NOT_PUBLISHED` otherwise. The decision-ledger appends in this decision are **seven**, every one of them written in byte mode after an insertions-only `git diff --numstat`, and the file's 37 historical CRLF lines are **still 37** at the closing commit (OPS-20260914-LEDGERCRLF); `docs/STATUS.md`'s single historical CRLF line is likewise unmoved. One figure inside the closing paragraph was corrected **before** that paragraph was ever committed and is disclosed rather than passed over: the final credential-scan count was written as 164 and the measured figure is **267 files, 0 matches**; the byte-mode fix changed the file's length by zero and its CRLF count not at all, and no published paragraph was touched by it. **Three provider calls were made under this decision**, all on `ollama/glm-5.3` through `OLLAMA_API_KEY`, at most two ever in flight. No paragraph above this one is edited, and nothing published by REC-20260914-A through Y is modified, relabelled, repaired or superseded by any of them.
```

## Limitations of these patterns

What these patterns would NOT catch: they match fixed byte patterns on whole lines, so anything presented differently is invisible to them. A receipt id split across lines (for example a line break inside 'REC-20260914-') matches nothing on either side, and the same is true of a VERIFIED/TREE line whose hashes wrap onto the next line. Ids with lowercase letters, a wrong-length date field, extra characters glued on either end, or 'REC' written with look-alike characters are not receipt ids as far as the pattern is concerned. A 40-hex commit or tree shorter than 40 digits, uppercase, or separated from 'VERIFIED'/'TREE' by different spacing escapes item 6, and a 'Prior verified commit/tree:' line with extra inner spacing or a trailing colon variant is missed by item 5. Entry counting by 'starts with REC-/'**REC-' on lines and blocks cannot see receipts introduced mid-sentence (for example 'See REC-...'), indented occurrences, or two receipts opened inside one paragraph, and paragraph splitting depends entirely on blank lines. The credential scan is only as strong as its two regular expressions: credentials of any other shape (different length, characters, or prefix, or broken across lines) would not be found, so zero hits means 'no match to these two patterns', not 'the file contains no secret of any kind'. Finally, line numbers are 1-based over raw split lines and presume the file is UTF-8; a file whose final line lacks a terminator or that mixes endings is handled, but counts refer to the exact current bytes, and any later append invalidates them.
