# Verified join — decision ledger × branch commit log

Every commit/tree identity published in `docs/DECISION_LEDGER.md`, joined against `evidence/git-log-branch.txt` — the frozen `git log --format='%H %T %h %ad %an %s' --date=iso-strict` extract over the whole branch: **397 lines, 397 unique commits, 397 unique trees, 397 unique short ids, no short-id collisions**.

## 1. What was extracted, and by which pattern

| rule | pattern | strings extracted |
|---|---|---|
| 1. VERIFIED pair | `VERIFIED ([0-9a-f]{40}) TREE ([0-9a-f]{40})` | **79** |
| 2. `Prior verified commit/tree:` sentence | `Prior verified commit/tree:\s*`?([0-9a-f]{7,40})`?\s*/\s*`?([0-9a-f]{7,40})`?` | **25** |
| 3. other bare 40-hex / 7-hex token near a keyword | `(?<![0-9a-f])(?:[0-9a-f]{40}|[0-9a-f]{7})(?![0-9a-f]) with the NEAREST word of /(commit|tree|remote|published)/i within a 40-character gap` | **496** distinct (token, role) pairs |

Rule 2: in this ledger every such sentence writes the identifiers **commit-first** — a full 40-hex commit, ` / `, a full 40-hex tree, optionally backticked — so the join takes the first identifier as the commit; the pattern as coded would also accept short ids or the reversed order without silently misreading them (the two capture groups are kept as first/second-as-written and the written order is reported per row).

Rule 3: the exact spans already claimed by rules 1 and 2 are excluded; distance is the character gap to the **nearest** keyword word, case-insensitive, substrings allowed (so `commits`, `trees`, `publication`, `remote main` all qualify), window ≤ 40 characters.

## 2. VERIFIED pairs — each claim joined against the log by commit

| ledger line | claimed commit | claimed tree | verdict | log line · logged tree · subject |
|---|---|---|---|---|
| 942 | `b8a77a5521aff3976a93b39b447282ed3caa62de` | `546079eb29eeb1c9ba981d092641feeb0a3be465` | **MATCH** | 217 · `546079eb29eeb1c9ba981d092641feeb0a3be465` · Preserve H003 cycle 2 observations and custody checkpoint |
| 948 | `393a2720a418aba6a76a13ba0283fbada9bf415a` | `725e43baa5236a63e921f18c9ca796d15a92d139` | **MATCH** | 215 · `725e43baa5236a63e921f18c9ca796d15a92d139` · Preserve H003 cycle 3 observations and custody checkpoint |
| 954 | `59785ba28474ffcb63e574ef42b459cbe390e8fc` | `2c04c7a0e3dbd0a9e413ec301870d561b96dbd55` | **MATCH** | 213 · `2c04c7a0e3dbd0a9e413ec301870d561b96dbd55` · Preserve H003 cycle 4 observations and custody checkpoint |
| 964 | `eb5e5cf7dda473df40e5b6e744f035832c57e848` | `ad6b41c413590277f0f8f87c3947384622e86116` | **MATCH** | 209 · `ad6b41c413590277f0f8f87c3947384622e86116` · Record current H003 block1 state and next continuation |
| 970 | `1634f569481c2c127cc0f0dcbafa806c0e53d3e3` | `e0a8e22546dec4268f1eb8f6c59800ca239ef097` | **MATCH** | 207 · `e0a8e22546dec4268f1eb8f6c59800ca239ef097` · Preserve H003 cycle 6 observations and custody checkpoint |
| 976 | `7ab66682b85c734f9addb5a9a9aeecdea5222912` | `1c13d7c62eaa0b3a80f1514d3aa25dfc89970829` | **MATCH** | 205 · `1c13d7c62eaa0b3a80f1514d3aa25dfc89970829` · Preserve H003 cycle 7 observations and custody checkpoint |
| 982 | `8e095dc6ec2d337c18c1327ea777f5b630f738d9` | `dbe14897e8911d4ea87f44942587b6d90867414f` | **MATCH** | 203 · `dbe14897e8911d4ea87f44942587b6d90867414f` · Preserve H003 cycle 8 observations and custody checkpoint |
| 988 | `edb5d59208be043e78c01ab04b86fd8f4afc26a2` | `5721518b69c0a403be80a8b6dd0406cfc1336b98` | **MATCH** | 201 · `5721518b69c0a403be80a8b6dd0406cfc1336b98` · Preserve H003 cycle 9 observations and custody checkpoint |
| 996 | `39aab1d627b00273c8bac5c488a7d3b24852105d` | `076a988e4e8a462899acecf26ac9985e5041c2cc` | **MATCH** | 198 · `076a988e4e8a462899acecf26ac9985e5041c2cc` · Review H003 block2 correction and output-limit stops |
| 1020 | `8d07a7733ea482ca139080c7955295fc0b0f02b7` | `115b1052b7b0af2a6884266e0a60e9375e2c4e46` | **MATCH** | 188 · `115b1052b7b0af2a6884266e0a60e9375e2c4e46` · Preserve H004 wave 1 observations and separate partial coverage |
| 1024 | `1a2bccf24fa3f5b38dd5d38161ca46215ca5616b` | `0f52d513aeddd073ab771fea61b8892cd96a0378` | **MATCH** | 187 · `0f52d513aeddd073ab771fea61b8892cd96a0378` · Accept H004 first-wave custody and document partial-continuity operation |
| 1030 | `590d41451a96183e3547a341b56129c0c7d3ac0d` | `100341551e9827c2c7d7427fc9e30b9151329084` | **MATCH** | 185 · `100341551e9827c2c7d7427fc9e30b9151329084` · Preserve H004 wave 2 observations and separate partial coverage |
| 1036 | `9eb522d0a3de08f091ca4563b8e72c1b02d35b54` | `c953cd7de023de7c91cf90b66976b96eb976425e` | **MATCH** | 183 · `c953cd7de023de7c91cf90b66976b96eb976425e` · Preserve H004 wave 3 observations and separate partial coverage |
| 1044 | `5166e58dda30eed30bfc1d0a27f1dad1b96e9ddb` | `ccec500c2bcf4f89a0db85b84fd6a2191ba693b8` | **MATCH** | 180 · `ccec500c2bcf4f89a0db85b84fd6a2191ba693b8` · Preserve H004 wave 4 observations and separate partial coverage |
| 1050 | `6fedd193fce01639b2aaf2fe1e4c2a99b48fcfd5` | `0eb54de1d1fa0b5ea6c2cfa25b58fa8841b3a91c` | **MATCH** | 178 · `0eb54de1d1fa0b5ea6c2cfa25b58fa8841b3a91c` · Preserve H004 wave 5 observations and separate partial coverage |
| 1054 | `0c466bbc9bb7cbacd63b9a2f95496a456f9dfc37` | `a04fe9d66d649358b2b1ced2317784548906a149` | **MATCH** | 177 · `a04fe9d66d649358b2b1ced2317784548906a149` · Record H004 wave5 root review and accept late-return continuation |
| 1062 | `454ee1c9d9993e9cda8323bde1e92dd6bdfef09d` | `7ed3291a0d0c0b83cff4cf189f8314b897f6e2c2` | **MATCH** | 175 · `7ed3291a0d0c0b83cff4cf189f8314b897f6e2c2` · Preserve H004 wave 6 observations and separate partial coverage |
| 1070 | `15a4cb65b8d3598f0b9649673fc7916621583d8a` | `2ed492a85f7b960e663a2aed7b8059578b922eb5` | **MATCH** | 173 · `2ed492a85f7b960e663a2aed7b8059578b922eb5` · Preserve H004 wave 7 observations and separate partial coverage |
| 1078 | `8c5d0b8c623c5c364b5971dce9760d5f3594ee52` | `96f7856ccd1faae4ce455453542ea6e8aafad247` | **MATCH** | 171 · `96f7856ccd1faae4ce455453542ea6e8aafad247` · Preserve H004 wave 8 observations and separate partial coverage |
| 1085 | `ef8752f3594b3866ea4a9df6856cacddedb3f169` | `30b461cb4c2f8ce5d3678ba3798e37113d9bce12` | **MATCH** | 169 · `30b461cb4c2f8ce5d3678ba3798e37113d9bce12` · Preserve H004 wave 9 observations and separate partial coverage |
| 1092 | `5d153f56417bea7b925959e7d402bb94cb7dce74` | `122acb4ece0ad01105db7cc4fba252ad298a7588` | **MATCH** | 167 · `122acb4ece0ad01105db7cc4fba252ad298a7588` · Preserve H004 wave 10 observations and separate partial coverage |
| 1096 | `0557249bff5a437de52f74677de63776d5b5f0bf` | `8120a66a9a85b8fc016075f71e1f9554c220642f` | **MATCH** | 166 · `8120a66a9a85b8fc016075f71e1f9554c220642f` · Record late prose error discovery and accept H004 wave10 gate |
| 1100 | `d310795fae84039222c68fcb82f5167777f705ce` | `3f623f16f4a160af5401927e37cca6293b0b5489` | **MATCH** | 165 · `3f623f16f4a160af5401927e37cca6293b0b5489` · Update recovery status at H004 wave10 with remaining bounded work |
| 1109 | `ba617f3a0e08b88e252320ffd0492791e88ed19f` | `b63fbbf2328f8b37767c9d34295360e4e32d6652` | **MATCH** | 163 · `b63fbbf2328f8b37767c9d34295360e4e32d6652` · Preserve H004 wave 11 observations and separate partial coverage |
| 1116 | `ad0e9e02c0c74c687639b27ae13a1cc415ec0500` | `6c721d8301f21271b9833c6d9a4ff406af929f10` | **MATCH** | 161 · `6c721d8301f21271b9833c6d9a4ff406af929f10` · Preserve H004 wave 12 observations and separate partial coverage |
| 1123 | `c58dd790822bca5d0f5084b2d392c6478e9d8043` | `93ee9e81d58b025518ad9e4b5198debfcf07bd65` | **MATCH** | 159 · `93ee9e81d58b025518ad9e4b5198debfcf07bd65` · Preserve H004 wave 13 observations and separate partial coverage |
| 1130 | `a593701cceea2785fd76925fb8bc25787e2dcc69` | `fdc96f17c4d40782c62c68864f7f87ef8b6c9260` | **MATCH** | 157 · `fdc96f17c4d40782c62c68864f7f87ef8b6c9260` · Preserve H004 wave 14 observations and separate partial coverage |
| 1137 | `bbfa1cd9127bd449f2b411d06c1c7094aa7795e3` | `e9ea136c5393702a71982b8fd527dd9edcdc066e` | **MATCH** | 155 · `e9ea136c5393702a71982b8fd527dd9edcdc066e` · Preserve H004 wave 15 observations and separate partial coverage |
| 1141 | `1ec3cc7f2b2404e2ed196c93c1ac2d72df7c9d7b` | `ec93654f949c41a865821996cca0ced76549df12` | **MATCH** | 154 · `ec93654f949c41a865821996cca0ced76549df12` · Publish H004 wave15 root review and final three-call gate |
| 1148 | `166ac59ad45d8e50c9f327d8270aa921c88d3095` | `f29aa03f5209332ffe71a0a0a1cde6cd462c561a` | **MATCH** | 152 · `f29aa03f5209332ffe71a0a0a1cde6cd462c561a` · Preserve H004 wave 16 observations and separate partial coverage |
| 1155 | `4e9532fd57cba3238a221b89a8fc93c70f3db66d` | `5119eb20d9dcd026eb889dd5d26a08e1eba4b6a8` | **MATCH** | 150 · `5119eb20d9dcd026eb889dd5d26a08e1eba4b6a8` · Preserve H004 wave 17 observations and separate partial coverage |
| 1164 | `8d0c87ed483f3951bc5275d3a3d3684024895afd` | `548f8936d45a01ef2481deb6d7da819ba91b3692` | **MATCH** | 148 · `548f8936d45a01ef2481deb6d7da819ba91b3692` · Preserve H004 wave 18 observations and separate partial coverage |
| 1168 | `ea48fd676520f63417c9856f08e6058c1f6feb49` | `aa1056199555bd180c030f7ebc1deee5b5212afa` | **MATCH** | 147 · `aa1056199555bd180c030f7ebc1deee5b5212afa` · Publish successful H004 final custody audit |
| 1172 | `459ca775750f2d4998080337a2539014d25c0ac6` | `b8c08eeaabb0b6af6cb110cbc8960e626cfd0d5e` | **MATCH** | 146 · `b8c08eeaabb0b6af6cb110cbc8960e626cfd0d5e` · Publish H004 terminal results and root scientific review |
| 1176 | `14e1a75e72b1f19664082bb3dc65bef95fc4b797` | `9e2de4d41094357eece2480d7dfd1304baa6934d` | **MATCH** | 145 · `9e2de4d41094357eece2480d7dfd1304baa6934d` · Publish supervised prose-audit candidate template card |
| 1180 | `2b6affd4a13ccf42afa747e09d274783969080cc` | `2e164837198e6d3bead228bfd056c1806b171894` | **MATCH** | 144 · `2e164837198e6d3bead228bfd056c1806b171894` · Document H004 terminal boundaries and transferable failure guidance |
| 1184 | `0ecef2654df3d2e8e9cd94b682196c54b0abe31b` | `9303f2f80c8322fcbe42cefd00c2bb5f06e3a591` | **MATCH** | 143 · `9303f2f80c8322fcbe42cefd00c2bb5f06e3a591` · Record H004 continuity and evidence-operation lessons |
| 1188 | `2c514664c2b6bfd58286c7aa292b477678ddeb86` | `651a83da2be2aa39fde1983e80e5d2378ff35cda` | **MATCH** | 142 · `651a83da2be2aa39fde1983e80e5d2378ff35cda` · Update miniReason status with completed H004 and candidate |
| 1204 | `5dbac3724d8fdf83bb13b952d0415501a56e3699` | `066f83993df8479297f3221c6cc42db9a71ba1bf` | **MATCH** | 138 · `066f83993df8479297f3221c6cc42db9a71ba1bf` · Record revised multi-cycle error-correction research contract |
| 1208 | `4ef269b6152c91b1f1cca89b3c89693eba77803f` | `de24837540cb4bd80167dfb7689f6cfcf75809ba` | **MATCH** | 137 · `de24837540cb4bd80167dfb7689f6cfcf75809ba` · Record recovered commitment interface and current source interpretation |
| 1212 | `44550f565b806d1ff343c66a0e8855334263d0c4` | `c0ea553bc76eef020ecb7432fbb9c040d0f51897` | **MATCH** | 136 · `c0ea553bc76eef020ecb7432fbb9c040d0f51897` · Propose FCL-1 for multi-cycle prose and commitment inquiry |
| 1218 | `b02ef276fb7d90ee4ff563bbcc8b33efae4bfd00` | `4e8e4f2c0a9257c99e210745d0ccc2ffffdb41e3` | **MATCH** | 135 · `4e8e4f2c0a9257c99e210745d0ccc2ffffdb41e3` · Freeze H005 prose problems and explicit template connectivity |
| 1222 | `d671dc9290b554d978d6b84b15b511a5d5530036` | `62a93be23479e805cd2b9a46f5cad504a6c43438` | **MATCH** | 133 · `62a93be23479e805cd2b9a46f5cad504a6c43438` · Publish H005 three-cycle comparative protocol |
| 1228 | `ca7db9a3b4ab06999fd2262d5875e3be6d79817e` | `7d87b80cb3274011779322f11b81b6680eb90237` | **MATCH** | 131 · `7d87b80cb3274011779322f11b81b6680eb90237` · Checkpoint H005 source custody and preparation boundary |
| 1234 | `b55832f684f91729ade4317465c748f891aa522a` | `7edef50c95f9a566df8633f3a9eb43892413ea9f` | **MATCH** | 128 · `7edef50c95f9a566df8633f3a9eb43892413ea9f` · Record the missing CLAUDE.md receipt after the fact |
| 1240 | `554e0dc02155d4cbf5f012b72c08825dd248fa71` | `0272b4a02d12e2854f399364d51f9f5152262cb3` | **MATCH** | 127 · `0272b4a02d12e2854f399364d51f9f5152262cb3` · Stop the stages_entered repair and record why it cannot be applied |
| 1246 | `38bde7dc5b4d657969d229f2a602e3577ec80d4e` | `501d29b3bd1add8e876ee826f94042a65105b0e5` | **MATCH** | 125 · `501d29b3bd1add8e876ee826f94042a65105b0e5` · Gate pushes and pull requests on the complete offline suite |
| 1268 | `c40dda76579ebd3f1b873598f6d8c6c06d39c777` | `31e5f165046d36f04d0a2ea878d18d2da1893872` | **MATCH** | 114 · `31e5f165046d36f04d0a2ea878d18d2da1893872` · Log the merge outcome and the post-merge suite baseline |
| 1276 | `22dc9f3450041fbca1298dc8b5763c1e4bbbc1e2` | `b4c516c48fc81b788bb2067c2902706d3dd23c9c` | **MATCH** | 109 · `b4c516c48fc81b788bb2067c2902706d3dd23c9c` · Correct the E028 published-summary assertion and normalize campaign.py |
| 1286 | `20b82184b6cd69415b2d5ae743afda53df321b93` | `995cb82574f2a4b4cb372e31b1e0310827c29eb5` | **MATCH** | 103 · `995cb82574f2a4b4cb372e31b1e0310827c29eb5` · Merge origin/main into the working branch, keeping both tails in full |
| 1292 | `ffbb9f3fe1f65fff4dc74d4afca7daaf53051c49` | `05228b5150b5091666bc20997e2bf8c1123838d1` | **MATCH** | 101 · `05228b5150b5091666bc20997e2bf8c1123838d1` · Recover Mini's requirement register from h-EPI and record its provenance |
| 1298 | `8d5f149ddb07b5556f4d2f89c10e0bf2b8c8800e` | `cc2cc151d6c5a28760126ed788a3f115f8ab0400` | **MATCH** | 99 · `cc2cc151d6c5a28760126ed788a3f115f8ab0400` · Record the decision to publish the H005 envelope-asymmetry review |
| 1300 | `5bb083a3fbae926b35c5da507f8e08a4ef448012` | `5447572f35318e0dadf31a11aadc73aafe92b022` | **MATCH** | 98 · `5447572f35318e0dadf31a11aadc73aafe92b022` · Publish the H005 cycle-1 matched-arm envelope-asymmetry review |
| 1306 | `649ae2b69bcabf44f828e8806883db3bd8762afb` | `29271e92a537a0499bfda94fa7a67a49597b03ff` | **MATCH** | 96 · `29271e92a537a0499bfda94fa7a67a49597b03ff` · Publish the upstream inventory, the engine-path decision and the unbuilt design of record |
| 1308 | `1feed77c3e39acf69271b960f0b5e1e1b4743ea9` | `38b07b0957d467d34ad7e27e7ab9cfbfed7576ae` | **MATCH** | 95 · `38b07b0957d467d34ad7e27e7ab9cfbfed7576ae` · Close REC-20260914-M with the verified publication identities |
| 1312 | `c2366dd5a1d7e97b3abdbe15cea73167dbb46717` | `1e92dc0d0eb40a1a3fa05a8ee959644b865903e8` | **MATCH** | 93 · `1e92dc0d0eb40a1a3fa05a8ee959644b865903e8` · Publish the vendored DeepReason harness-spec-v1.3 P0 core |
| 1314 | `c2b92e1eef04cf4aa3c90ad36769718ed705b53b` | `9ad5031e740cfa90b4db274cf672321aba46c619` | **MATCH** | 92 · `9ad5031e740cfa90b4db274cf672321aba46c619` · Close REC-20260914-N with the verified publication identities |
| 1318 | `4d9cb75a7e25610c12c85825ee738c5d3bcc17a1` | `9b0806593175471a7e33f23f5fb3a7c78eba07b6` | **MATCH** | 91 · `9b0806593175471a7e33f23f5fb3a7c78eba07b6` · Record the decision to publish the H005 graph importer |
| 1320 | `6e7dac00966e120a67eb90694fe0d818ae8c07e4` | `bbf87ffec67b825744eccf2b14537544de8cdb46` | **MATCH** | 90 · `bbf87ffec67b825744eccf2b14537544de8cdb46` · Publish the H005 graph importer and its offline evidence replay |
| 1322 | `0ae29ee9dd6f83ad18428dcef6fbc0f3fb0f5269` | `d3d42fad4b1a55516be5ec3f68ca9044e8df1599` | **MATCH** | 89 · `d3d42fad4b1a55516be5ec3f68ca9044e8df1599` · Close the three follow-ups REC-20260914-N left open |
| 1326 | `4cac6b342a647bc1348fec5aafcc558e8fc8f9d3` | `2942e3f414038b57c71edd6eab50f14696dfa442` | **MATCH** | 88 · `2942e3f414038b57c71edd6eab50f14696dfa442` · Close REC-20260914-O with the verified publication identities |
| 1330 | `63c345beea3e662f5ed940e1a993ab7da5b1ce25` | `91cc723c97cef90d7e1b4444a4c7e1aaf3cb1ab4` | **MATCH** | 87 · `91cc723c97cef90d7e1b4444a4c7e1aaf3cb1ab4` · Publish the FW5 versus harness-spec-v1.3 review and its supporting record |
| 1336 | `c2d438e9358439d4b2c84aed313cde532c833c6a` | `ebe284e4631b1180247590b82e74ec3ae229e11a` | **MATCH** | 85 · `ebe284e4631b1180247590b82e74ec3ae229e11a` · Open REC-20260914-Q for the transport and use-relation instruments |
| 1338 | `b7136622a6c3c414083a8f85ab21c38d236b0b8a` | `403ea5fa819079a6d803dbf676b434c4f559be99` | **MATCH** | 84 · `403ea5fa819079a6d803dbf676b434c4f559be99` · Publish the multi-endpoint transport and the H005 use-relation instrument |
| 1342 | `aaaeea1bfb53b226053e6a43cdfc536c28e4b3f0` | `472915f12092c708a67dbd9e2a4d0edb2672ab94` | **MATCH** | 83 · `472915f12092c708a67dbd9e2a4d0edb2672ab94` · Close REC-20260914-Q with the verified publication identities |
| 1346 | `6114aedb3de0d06a0861229d310d7a5a40932526` | `3a110e1fa0d4d0f7e4f19b98b08f8252055f4eb4` | **MATCH** | 82 · `3a110e1fa0d4d0f7e4f19b98b08f8252055f4eb4` · Open REC-20260914-R for the occurrence-01 snapshot analysis outputs |
| 1348 | `7e5ae00f1960f32b6c24002cfebe5727249e0906` | `470803a4ac147dca96c85177eb293185f040aa78` | **MATCH** | 81 · `470803a4ac147dca96c85177eb293185f040aa78` · Publish the H005 occurrence-01 snapshot analysis outputs |
| 1362 | `f166069ab46987666275ecf3c503a4b7c2e3eb34` | `67c9d820b72eefefe9d12b3135c435cab38e25f5` | **MATCH** | 79 · `67c9d820b72eefefe9d12b3135c435cab38e25f5` · Open REC-20260914-S for the multi-family fork5 study |
| 1364 | `1abe87ecbd9928f2a63145f79f27c50ee738322f` | `8f0014547afae299f6dc1369bd54fa7b5b6aa7b5` | **MATCH** | 78 · `8f0014547afae299f6dc1369bd54fa7b5b6aa7b5` · Publish the multi-provider H005 runner fork and the F001 register |
| 1378 | `31522aa359d91f0bb86a82a869ed7617256433fd` | `193477c098077c4965e05476258f6d6132e92c13` | **MATCH** | 67 · `193477c098077c4965e05476258f6d6132e92c13` · Publish the F001 mechanism-facts analysis outputs |
| 1429 | `2d7239acd70f14aa049b62034a803784883da7b7` | `9d0ab88f6940b220110797722fd4e628aef9c43e` | **MATCH** | 42 · `9d0ab88f6940b220110797722fd4e628aef9c43e` · Publish the C001 occurrence-02 instrument under REC-20260914-V |
| 1449 | `dc5491e0e6d992ecd2e36b2f6c2adf7e854fe91c` | `7034b1266a8aca02b39d368d00e10a1d131e2c9c` | **MATCH** | 31 · `7034b1266a8aca02b39d368d00e10a1d131e2c9c` · Publish the refreshed session orchestration report under REC-20260914-W |
| 1457 | `96ca2eb3188beeb3ca1d399cddb203a9d38ec8a9` | `da1d4bff5619b9a189575e11058c3b7a66d6be7b` | **MATCH** | 28 · `da1d4bff5619b9a189575e11058c3b7a66d6be7b` · Open REC-20260914-X to publish and dispatch F002, the fork5 raised-clock follow-on |
| 1457 | `7bff688f89cbb7cdbb5a6f76c63fed6db8cb80e9` | `9b354336e5cc54c20e63a0795f69de7914a42c85` | **MATCH** | 27 · `9b354336e5cc54c20e63a0795f69de7914a42c85` · Publish the F002 register, the v3 successor runner and both frozen occurrences |
| 1471 | `958f2f4173da679283388c1820d218a209dffdbb` | `79cbdfe9d1a03192d4bea8d84dc605d7862abdb8` | **MATCH** | 13 · `79cbdfe9d1a03192d4bea8d84dc605d7862abdb8` · Close REC-20260914-X: F002 is published, dispatched, analysed and verified |
| 1475 | `bfc5c8e7e18ca4797566a742f94df3d4b69df1f5` | `03937a46aa681b69caf7ba4203c195c440c8cc6d` | **MATCH** | 10 · `03937a46aa681b69caf7ba4203c195c440c8cc6d` · Opus 5 (1M context) B001: the register, the reasoning-persistence note, the arm inventory and its output |
| 1475 | `228e33ff931b69994e40d333701f6efac905421b` | `6be02776a3d66e6eaee888029b10919ae3570e41` | **MATCH** | 11 · `6be02776a3d66e6eaee888029b10919ae3570e41` · Opus 5 (1M context) Open REC-20260914-Y: publish B001 as an offline register and refuse its dispatch |
| 1479 | `920cfc3c8968db302f5a3c30beed0a03981873c7` | `65700b3689d90e3681af134cf6f6f64141122737` | **MATCH** | 9 · `65700b3689d90e3681af134cf6f6f64141122737` · Opus 5 (1M context) Close REC-20260914-Y: B001 is published, its dispatch refused, at zero calls |
| 1495 | `c56b129dc36eaf87dcb39e0a36e9a227164c3525` | `05eebc4bbb715a83121a507dc31dc27b0818d776` | **MATCH** | 2 · `05eebc4bbb715a83121a507dc31dc27b0818d776` · F002 occurrence-03: register, workflow and STATUS sections; close REC-20260914-Z |

## 3. `Prior verified commit/tree:` sentences — same join

| ledger line | commit (first, as written) | tree (second, as written) | verdict | log line · logged tree · subject |
|---|---|---|---|---|
| 1224 | `d30829a00d8b381a108550e6c7021d6c04ad91ae` | `1a7d0d9610d032818f6334d8ec005a502faaf70b` | **MATCH** | 132 · `1a7d0d9610d032818f6334d8ec005a502faaf70b` · Update status for complete-template H005 study |
| 1230 | `1cdbdf3e0fa05980229ac8c87794c68e4ce2dec2` | `f3eb47ce4faf49015addd0d45a94b852a9d61186` | **MATCH** | 130 · `f3eb47ce4faf49015addd0d45a94b852a9d61186` · Record H005 command-length preparation failure |
| 1236 | `6fae74fcee9141b63ae71c5d40c6008a14a254f8` | `57e2f1448a125b80ed37058ceb90d252ecb270cd` | **MATCH** | 129 · `57e2f1448a125b80ed37058ceb90d252ecb270cd` · Connect H005 command-length incident to agent entry guidance |
| 1242 | `ad4d33c257954170c31a3287f82bed96a247c995` | `f1f2d947bde7861234aafa15bbca1b81d9b87f68` | **MATCH** | 126 · `f1f2d947bde7861234aafa15bbca1b81d9b87f68` · Checkpoint H005 implementation review in progress |
| 1248 | `994740dbd6452a17f9d9f0ea91887fbab09836da` | `e5a10ff2d6e1e09c7f16be4ae6dc4768c4bf6d26` | **MATCH** | 124 · `e5a10ff2d6e1e09c7f16be4ae6dc4768c4bf6d26` · Record root H005 preflight review findings |
| 1250 | `c7925274fcf97fe29ef94311225803a33d66be63` | `0dffb02abfb0b007907837bc0c0c9a1a4c73d860` | **MATCH** | 122 · `0dffb02abfb0b007907837bc0c0c9a1a4c73d860` · Accept and freeze H005 template invocation runner |
| 1254 | `461df55bbcd5de29594294443d0aea141e75e77c` | `5ce7b439576a814e1844066ebd278d9bd24c35d7` | **MATCH** | 121 · `5ce7b439576a814e1844066ebd278d9bd24c35d7` · Freeze actual H005 occurrence and first five requests |
| 1256 | `b5ba7e3dd9ac3df740a4da34e42801b8809b02d2` | `6a1b1048274faa502d9c3431767978715857e387` | **MATCH** | 119 · `6a1b1048274faa502d9c3431767978715857e387` · Publish H005 wave0001 terminal evidence |
| 1258 | `8a1ad17e3b27b6c76c3caf90bf47832e73825181` | `86beb540c612762599212014fcf46e34229f3bc4` | **MATCH** | 117 · `86beb540c612762599212014fcf46e34229f3bc4` · Publish H005 wave0002 ready inputs |
| 1260 | `61eecd4b8065151a61194e0482f2fa0bf1ebee2c` | `251add3c61f4b5d1f86b0b08bac2060d2f84aca3` | **MATCH** | 116 · `251add3c61f4b5d1f86b0b08bac2060d2f84aca3` · Publish H005 wave0002 terminal evidence |
| 1262 | `8e81a34f7fe30e791bfdc76db0cf521f280213a6` | `17fe40be6e67d293536e930075bef8979da89240` | **MATCH** | 115 · `17fe40be6e67d293536e930075bef8979da89240` · Publish H005 wave0003 ready inputs |
| 1264 | `772ba0cd29976a585c5d62b927ee95355d38c8c9` | `12afe166849eb52b69462d70990c6e6a77723a25` | **MATCH** | 113 · `12afe166849eb52b69462d70990c6e6a77723a25` · Publish H005 wave0003 terminal evidence |
| 1270 | `f76c7369120a0138e065696a47e1c4dd987cbb23` | `a902e9aadeed4d1be5195a0abe54738c3c295815` | **MATCH** | 112 · `a902e9aadeed4d1be5195a0abe54738c3c295815` · Publish H005 wave0004 ready inputs |
| 1272 | `bcf10022e21f497e6439bb7e5afdbbe4af9d9450` | `2250681371935933d05616a0c6e32bc8c6f194e3` | **MATCH** | 111 · `2250681371935933d05616a0c6e32bc8c6f194e3` · Publish H005 wave0004 terminal evidence |
| 1278 | `1efa2af4c3e7602edf600c68f78ff190a3e95793` | `13cecb5070a6f279f5a1c03a9a9a1d1a1a1da562` | **MATCH** | 110 · `13cecb5070a6f279f5a1c03a9a9a1d1a1a1da562` · Publish H005 wave0005 ready inputs |
| 1280 | `c6cfd0dd271d1f62ba794abe600a7023c02aca97` | `d0b7fcfafaa23154f2226ae749deceb92562a729` | **MATCH** | 107 · `d0b7fcfafaa23154f2226ae749deceb92562a729` · Publish H005 wave0005 terminal evidence |
| 1392 | `f50db28cafd4f84683564aab7f5943393ed5e99c` | `4e7c6622aa734d0ceebc523daaa1aa5bd842a893` | **MATCH** | 53 · `4e7c6622aa734d0ceebc523daaa1aa5bd842a893` · Close REC-20260914-T with the verified publication identities |
| 1427 | `9045a94cd7762f06066c23125167c26e4f07e2a9` | `95f94112e6930bb3c5db4d476c6ccce3e173f448` | **MATCH** | 43 · `95f94112e6930bb3c5db4d476c6ccce3e173f448` · Correct a register-mark count in REC-20260914-U |
| 1447 | `dd2e0673bcedb2208265ed79cb73a279e5df96de` | `c3d494f1366ffcc65a7a35feed082452c88f5a5d` | **MATCH** | 33 · `c3d494f1366ffcc65a7a35feed082452c88f5a5d` · Correct a commit count in REC-20260914-V |
| 1455 | `8b25a306332cd0c560b53214d94550eddf673919` | `fe03802edd79351f6cace4e1d3862cd4f10215b2` | **MATCH** | 29 · `fe03802edd79351f6cace4e1d3862cd4f10215b2` · Record the verified closing commit and tree in REC-20260914-W |
| 1469 | `f25b4a93723c88a40ade062c065df20fd22490e9` | `908d0f5ee884a989772eecd00cb68aaf44bb8a87` | **MATCH** | 14 · `908d0f5ee884a989772eecd00cb68aaf44bb8a87` · Refresh STATUS and append the F002 section to the fork5 workflow |
| 1473 | `65c846477df14a6cb1532d10b423ef354f8c2e13` | `b104af92a25fab9dbc60ddb75b0b0606295b4f32` | **MATCH** | 12 · `b104af92a25fab9dbc60ddb75b0b0606295b4f32` · Record the verified closing commit and tree in REC-20260914-X |
| 1477 | `bfc5c8e7e18ca4797566a742f94df3d4b69df1f5` | `03937a46aa681b69caf7ba4203c195c440c8cc6d` | **MATCH** | 10 · `03937a46aa681b69caf7ba4203c195c440c8cc6d` · Opus 5 (1M context) B001: the register, the reasoning-persistence note, the arm inventory and its output |
| 1481 | `c81ef6060f907ef7f59f4680d1fe05acdf8ed65c` | `b6e0b2de6f789fdfcd636b95d748751d3f6556b1` | **MATCH** | 8 · `b6e0b2de6f789fdfcd636b95d748751d3f6556b1` · Opus 5 (1M context) Record the verified closing commit and tree in REC-20260914-Y |
| 1493 | `4ff209bb04e27289d1994bbd89b2391b64a29bbb` | `d3a89d46d8912789e053753cac408a936618ed0a` | **MATCH** | 3 · `d3a89d46d8912789e053753cac408a936618ed0a` · F002 occurrence-03 analyses: audit, graph import and use table at full scope |

## 4. Other bare tokens — do they resolve in the log?

Membership only, per rule 4: a full 40-hex id is **COMMIT** (exact logged commit; its logged tree and subject shown), **TREE** (the sha is the tree of the commit(s) listed), **COMMIT+TREE** or **NEITHER**. 7-hex ids are **UNRESOLVED-SHORT** — never promoted — because one short id can prefix both a commit and a tree; their `role` column is the ledger's own nearest keyword, not a log resolution.

| ledger line | token | declared role (nearest keyword, gap) | verdict | resolves to |
|---|---|---|---|---|
| 11 (also 35) | `506b716bb7a2b4504e9e4f0ba54966587ac36465` | commit (commit, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 11 (also 35, 169) | `78331ad4469831610e3a4a0eb6efee835ea26f37` | remote/publication (remote, 7) | **COMMIT** | commit `78331ad` — Record independent E012 verification and start frozen non-Lean comparison |
| 11 (also 35) | `ebcd5631eba03a218c9a117e5407c46f2b532a67` | tree (tree, 2) | **TREE** | tree of `e0309ae` (line 373) |
| 35 (also 59) | `cceeded` | remote/publication (remote, 17) | **UNRESOLVED-SHORT** | — |
| 35 | `e0309aef15346428b8854e3669476f44732d1eda` | tree (tree, 7) | **COMMIT** | commit `e0309ae` — Recover completed E013 non-Lean experiment after interrupted publication |
| 59 | `0bc33c00ba5ad32932c244b9e351959e44b54005` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 59 | `59bc4335b7b1157bac842c748687e19755fd0013` | remote/publication (remote, 7) | **COMMIT** | commit `59bc433` — Preserve decision ledger and recovery instructions after the second interrupted window |
| 59 | `ab3488f17d8aac51c3bc7233ecae932ddfccb401` | tree (tree, 2) | **TREE** | tree of `59bc433` (line 372) |
| 81 | `5201b1385d7ff433fd031da361f34a41cf3f1443` | remote/publication (remote, 7) | **COMMIT** | commit `5201b13` — Complete E013 review and integrate tested reason-use controls with decision receipts |
| 81 | `55a38fc2cd1b14b5c972dd0eea69fd4c87bb2746` | tree (tree, 2) | **TREE** | tree of `5201b13` (line 371) |
| 81 | `d1c57279cc94b8b7ebf4c79291b80561c7030aa5` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 105 | `7fc2b9928a06d7f6ac75159dfcf447536a9a43bc` | remote/publication (remote, 7) | **COMMIT** | commit `7fc2b99` — Freeze reason-use inputs, independent review and five preflighted plans before live calls |
| 105 | `e5968f35aa77e3fed2be6eb892e4527562dbd1b9` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 105 | `f35d384bb92919a777e85271f014cf78a95ae102` | tree (tree, 2) | **TREE** | tree of `7fc2b99` (line 370) |
| 113 | `0c5751468efe0f0606a1438b96587dbde820d96f` | remote/publication (remote, 2) | **COMMIT** | commit `0c57514` — Record E016 activation and exact continuation state before model calls |
| 113 | `48ea06e16213f3c25b934ada7db7cfcd8aa5eafb` | tree (tree, 2) | **TREE** | tree of `0c57514` (line 369) |
| 113 | `d38836e9430ef94e3c187241d7cb8be9d10bb606` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 135 | `154f65a595ba81a77aa75c678e188c3d7c52aac7` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 135 | `31b2db694023d4268dbbb08dbc695344475552d8` | remote/publication (remote, 2) | **COMMIT** | commit `31b2db6` — Record complete E016 original-reason comparison and continuation receipt |
| 135 | `e32ff3400113e0946c94fd124b10acd87b6c8d76` | tree (tree, 2) | **TREE** | tree of `31b2db6` (line 367) |
| 163 | `ceb72f8d7daf35436138dd2ff6f02b6ede14ac99` | tree (tree, 2) | **TREE** | tree of `8363c4c` (line 364) |
| 163 | `d951dd95b11e8e0d868193a4d87bf09391fdee07` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 181 | `0f13035ee9bc30d89e3c49a94e6822d424638240` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 181 | `17c2f5aaf08fd79be0e7d4a06e81e0b681b30218` | tree (tree, 2) | **TREE** | tree of `9e59d57` (line 361) |
| 199 | `cef27f14c91bcde79eba8faa46e76fbffa995882` | commit (commit, 35) | **COMMIT** | commit `cef27f1` — Record E018 publication and activate the frozen E019 omission condition |
| 221 | `3e2e96e5684c1f8b464801739507a5d88dc10f1c` | remote/publication (remote, 7) | **COMMIT** | commit `3e2e96e` — Preserve interrupted E019 and publish complete recovery handover |
| 221 | `ab2ab5ecdf2e2168ba9e41681d750e6b623ffa2b` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 221 | `bde248a2f1075f82f0c82eb4adc6b2da8a95b085` | tree (tree, 2) | **TREE** | tree of `3e2e96e` (line 359) |
| 225 | `4d38c5d62309a34fbcf20d8165c44b8a5d7e6c4d` | remote/publication (remote, 7) | **COMMIT** | commit `4d38c5d` — Record verified recovery publication and final continuation state |
| 225 | `78ce9eb9df0e982f736e52acf12b7ef32fb89c47` | tree (tree, 2) | **TREE** | tree of `4d38c5d` (line 358) |
| 225 | `f2f6707a8fe2bd390a294d069617bd7ad675e4fc` | tree (tree, 8) | **NEITHER** | neither a logged commit nor a logged tree |
| 233 | `3e1ad2d46bfe034433ab88dee34a296766bd0ca8` | remote/publication (remote, 2) | **COMMIT** | commit `3e1ad2d` — Resume frozen controls and commission distinct-template promotion design |
| 233 | `5c9c59aa065acf154b5bb6a84a047a6c119fca32` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 233 | `a6ceddc6ae15cd82395475420fe0e55b37913c88` | tree (tree, 2) | **TREE** | tree of `3e1ad2d` (line 357) |
| 241 | `bd4a898a439b1632a189f120b0d204c38f1a4e40` | tree (tree, 2) | **TREE** | tree of `18bf7ae` (line 356) |
| 241 | `daa317e01ac427929742f627dd3f82632b9ed6ac` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 253 | `3e158b16b9cf140b4b00237f02a16eea516db81b` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 253 (also 264) | `a13b7032adec43d1a35681327081300f203eee40` | tree (tree, 2) | **TREE** | tree of `0de446c` (line 355) |
| 264 | `0de446c9f90beeae2a8a510a576c47174dcaded4` | tree (tree, 6) | **COMMIT** | commit `0de446c` — Select distinct construction and successor inquiry templates with receipts |
| 264 | `b4c0ae2a8e87e57fdbf2b3b06651d4110de8ebdd` | remote/publication (remote, 14) | **NEITHER** | neither a logged commit nor a logged tree |
| 270 | `814649dba32264dddd7ccd466dbbd57e32c63bcb` | remote/publication (remote, 2) | **COMMIT** | commit `814649d` — Record complete omission retry before frozen no-return control |
| 270 | `ae6eb00407373a78b30337617c06cc7f71abbb6e` | tree (tree, 2) | **TREE** | tree of `814649d` (line 354) |
| 270 | `b4c0ae2a8e87e57fdbf2b3b06651d4110de8ebdd` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 278 | `3859f3d29ce735605b8954e16fa8cd100c8befdb` | remote/publication (remote, 2) | **COMMIT** | commit `3859f3d` — Recover E022 publication and set per-document continuation checkpoint |
| 278 | `9c9404cff86945e615c14c0e0946e075294cae37` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 278 | `ab6e8363e438eabe4a5d2bdf20423a60e359a585` | tree (tree, 2) | **TREE** | tree of `3859f3d` (line 353) |
| 291 | `89997ac7acf0f2eeace78704532a5dcc1b3143ef` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 291 | `e589dacffe6aa36a68955d52a01a000d76a8d48b` | remote/publication (remote, 2) | **COMMIT** | commit `e589dac` — Preserve interrupted E020 and the exact live approval blocker |
| 291 | `e86d2743a159b8a66200b51b6c97a006764de573` | tree (tree, 2) | **TREE** | tree of `e589dac` (line 349) |
| 299 | `099df9c979ef404e7958db366ddbfd3fce6ddca0` | tree (tree, 2) | **TREE** | tree of `2292485` (line 346) |
| 299 | `22924850b4094d34dbc92ee07799ac56954846de` | remote/publication (remote, 2) | **COMMIT** | commit `2292485` — Complete independent E022 custody and substantive review |
| 299 | `28348e2da6df633a0b4f1fa7b6feb710030361a9` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 324 | `ccb19c391802e6761f749b2e02c33582d70d252f` | tree (tree, 1) | **TREE** | tree of `d1b175e` (line 342) |
| 324 | `d1b175e12c6b9f96ecf792d42752dd5f506574b8` | remote/publication (remote, 1) | **COMMIT** | commit `d1b175e` — Implement verified one-cycle construction to distinct successor inquiry |
| 324 | `ed05c18fb7dbb998b50aea2cc4c460f0c9acfb7d` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 354 | `9d920e9433bb81fcaa85042245fc6a87ca87daee` | tree (tree, 1) | **TREE** | tree of `cfb91d0` (line 333) |
| 354 | `bb74f5808c561038f66a7b950dab7c57efe2564b` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 354 | `cfb91d0016cce66070b68ef4b90db4265fb8d3e8` | remote/publication (remote, 1) | **COMMIT** | commit `cfb91d0` — Link the tested distinct-template implementation and exact next prepared steps |
| 361 | `5de75f089d903be3fab5d23f28240130e13c2b9a` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 361 | `a2c7c8c7adb5ad70a47b88bbbc67c973eb58d5cd` | remote/publication (remote, 1) | **COMMIT** | commit `a2c7c8c` — Push current activity checkpoint and confirm implementation recovery complete |
| 361 | `f165e76aa30b698b7e71d0c364b6a43dadfa12ec` | tree (tree, 1) | **TREE** | tree of `a2c7c8c` (line 331) |
| 367 | `831984ab5108f65a6217029ac0cc5c0cf8fdc19a` | remote/publication (remote, 1) | **COMMIT** | commit `831984a` — Finish current handover with completed implementation and exact prepared next run |
| 367 | `bf6382b549a23803282aed065a27688495fefb61` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 367 | `e30426588607703e31838b6ce9323ad57a50e4d3` | tree (tree, 1) | **TREE** | tree of `831984a` (line 330) |
| 371 | `47803113476e8bb7c14398c291b964e2eb0641ec` | tree (tree, 2) | **COMMIT** | commit `4780311` — Lead recovery entry point with completed implementation and the live-call boundary |
| 371 (also 383) | `96fbc419fc7c14e015005b44335fc0bc8a5e8277` | tree (tree, 1) | **TREE** | tree of `4780311` (line 329) |
| 383 | `66dd670ee3b18089b33c760c4856e7af80abbfbc` | tree (tree, 5) | **NEITHER** | neither a logged commit nor a logged tree |
| 391 | `192e56faad9d0538e5ac3a7153334fdeeb6fa594` | tree (tree, 1) | **TREE** | tree of `b61aa09` (line 328) |
| 391 | `b61aa0926e72fc8610678c808db225f627a31ad9` | remote/publication (remote, 6) | **COMMIT** | commit `b61aa09` — Resume formal consistency research with timed progress receipts |
| 391 | `f86ff329ede0388b21fc7befdf1f55565ac83b1d` | tree (tree, 12) | **NEITHER** | neither a logged commit nor a logged tree |
| 409 | `4c34fa878254627d923c5de55280e4a94ff6e0b2` | tree (tree, 1) | **TREE** | tree of `65a906c` (line 327) |
| 409 | `65a906cc212cc0ca5e1cbeaeadd456d8bb948c29` | remote/publication (remote, 6) | **COMMIT** | commit `65a906c` — Predeclare controlled formal-argument feedback research |
| 409 | `cea0d742c0de24d121e9b081ebc91008eb091674` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 413 | `feedbac` | remote/publication (published, 11) | **UNRESOLVED-SHORT** | — |
| 423 | `5715cf781a6d25a3127c7752120b44061b4256df` | tree (tree, 12) | **NEITHER** | neither a logged commit nor a logged tree |
| 423 | `bf97aedb876902fbb498b43b32c25c22f5d8f9ea` | remote/publication (remote, 6) | **COMMIT** | commit `bf97aed` — Clarify formal-feedback attribution and adverse-case coverage |
| 423 | `f19a771a5f7f2ba70ad15eb361e1ada1a90f31a8` | tree (tree, 1) | **TREE** | tree of `bf97aed` (line 326) |
| 429 | `549c7193edf8dfc41af227b56afa58078c72e5fe` | tree (tree, 1) | **TREE** | tree of `c689d48` (line 325) |
| 429 | `755f4058e3e4c7e5e9ac2618301de3e5f153e2bf` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 429 | `c689d485be0f1f9d50e36fe0aa49ffab08c01b9d` | remote/publication (remote, 1) | **COMMIT** | commit `c689d48` — Activate installed five-minute progress skill for continuations |
| 433 | `6f64d4453d95a820d87ce2ad1f57e64d354c5c0b` | remote/publication (remote, 1) | **COMMIT** | commit `6f64d44` — Add reproducible finite argument and dependency-chain diagnostics |
| 433 | `c855fa410a75e406dcbba4b79bc9bc20b6d96fd1` | tree (tree, 1) | **TREE** | tree of `6f64d44` (line 324) |
| 433 | `d7b7cbb5fdd24428fbb81ce2efde3a92347723e0` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 437 | `2ef17f745a2e7f6f320311450ae86916f3175c48` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 437 | `3adfc5a43a5b706e273b664b012d7082cc72e094` | tree (tree, 1) | **TREE** | tree of `a67853b` (line 323) |
| 437 | `a67853b978250c69139ad0ede421b63a8fb13649` | remote/publication (remote, 1) | **COMMIT** | commit `a67853b` — Report formal-chain checking results and semantic failure cases |
| 439 | `2e28fe8dee969f1fa67ddd8c67d68bff2250d49d` | tree (tree, 12) | **NEITHER** | neither a logged commit nor a logged tree |
| 439 | `846fa5723a69554c653fe9aa5f4fa7d277c58aca` | tree (tree, 1) | **TREE** | tree of `9fb0418` (line 322) |
| 439 | `9fb0418120861b54a8a86f6f731ec7ca4ecc1f99` | remote/publication (remote, 1) | **COMMIT** | commit `9fb0418` — Hand over completed formal-feedback research and unchanged live boundary |
| 447 | `02c3fd21aae858f499eae9f503cc7264de3c7404` | remote/publication (remote, 1) | **COMMIT** | commit `02c3fd2` — Lead README with checked formal-argument research and progress cadence |
| 447 | `33f7f9564e390e4b099c5e1d4257971faba742e6` | tree (tree, 1) | **TREE** | tree of `02c3fd2` (line 321) |
| 447 | `b4e271cb5b1fd0ebde011a92a06a5829819ee29b` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 453 | `2b2ab4ce8d8f088276590fe9a59375967c9ccf50` | tree (tree, 10) | **NEITHER** | neither a logged commit nor a logged tree |
| 453 | `816a6a0cd79de13e18e081decd511e1da0719b3f` | tree (tree, 1) | **TREE** | tree of `54c9f86` (line 320) |
| 465 | `1f811f11bbfb4afb63ea18b60486061f1c682f00` | remote/publication (remote, 1) | **COMMIT** | commit `1f811f1` — Record explicit DeepSeek approval and activate frozen E023 control |
| 465 | `26ed35edb34bbe4a8d3a3477ed957b7d6edb4603` | tree (tree, 1) | **TREE** | tree of `1f811f1` (line 319) |
| 465 | `fcbefee3aeef7aaab59e1761842feb90ee418894` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 479 | `4033a17a7f86bc5926ffc6cd469689a2ef62f7ce` | remote/publication (remote, 1) | **COMMIT** | commit `4033a17` — Record complete E023 no-return control with eight live responses |
| 479 | `44fa2879b17aa888e94331c74ca2308facdc1c09` | tree (tree, 12) | **NEITHER** | neither a logged commit nor a logged tree |
| 479 | `87887d057428b203b66e6f22790fe88dad415c1c` | tree (tree, 1) | **TREE** | tree of `4033a17` (line 318) |
| 487 | `470cec28859b62de5357bd74d5387b922675124b` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 487 | `642dab8ff174f290a17871dff1133efab9707f41` | remote/publication (remote, 1) | **NEITHER** | neither a logged commit nor a logged tree |
| 487 | `b2b4fd2e6deaeb6666db9b170f8a05e664749c9e` | tree (tree, 1) | **TREE** | tree of `f71193e` (line 317) |
| 487 | `f71193ef9170bbc949e4f3c8c00e61e622dca2bb` | remote/publication (remote, 1) | **COMMIT** | commit `f71193e` — Review E023 account omission and retained semantic defects |
| 495 | `12a4754ca1902afd33f9dd98616fee408231f762` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 495 | `4788c308031fe89a22b57537a5f7ce861c0b56c6` | remote/publication (remote, 1) | **COMMIT** | commit `4788c30` — Approve frozen E024 activation after published E023 control |
| 495 | `d82e7fdc1660c33ae3c0627b7a9601844153032f` | tree (tree, 1) | **TREE** | tree of `4788c30` (line 316) |
| 499 | `5c61c18b00314e230fa091681eea75318bff7162` | tree (tree, 1) | **TREE** | tree of `6877dd2` (line 315) |
| 499 | `63a0ef0bf468453edfab276a5dbc4eb8b21f10bc` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 509 | `4d65a09059f5af7ab616ea6f46eccd0ee6ad5094` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 509 | `6456e2177a214ac57f7a29f9ca3a7284acb53c5a` | tree (tree, 1) | **TREE** | tree of `8d94188` (line 314) |
| 515 | `48523f07d0c09ab990bf05b8d34adba2a3cab891` | tree (tree, 1) | **TREE** | tree of `9c876cc` (line 313) |
| 515 | `7411a9f58eddf918a42f94a1e726efea4605eca2` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 521 | `656229c` | commit (commit, 15) | **UNRESOLVED-SHORT** | — |
| 521 | `9c876cc21686bd0e309449a4ca7dcbd9b737539c` | commit (commit, 12) | **COMMIT** | commit `9c876cc` — Record complete E024 construction observations |
| 526 | `656229c` | remote/publication (remote, 2) | **UNRESOLVED-SHORT** | — |
| 526 | `9c876cc21686bd0e309449a4ca7dcbd9b737539c` | remote/publication (remote, 6) | **COMMIT** | commit `9c876cc` — Record complete E024 construction observations |
| 535 | `0d828bd7f7d4279ba6eef94682a6d0ba6f5c13fb` | remote/publication (remote, 1) | **COMMIT** | commit `0d828bd` — Review actual E024 construction and authorize fixed successor |
| 535 | `656229c5bae98fe7b3731c48511670b4d42934c0` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 535 | `99f8a8a9d66cd96744409cae9be1e15156314d52` | tree (tree, 1) | **TREE** | tree of `0d828bd` (line 312) |
| 539 | `184e5ae250a51f139ee7548ba23371e9d5ecb1b7` | remote/publication (remote, 1) | **COMMIT** | commit `184e5ae` — Restore configuration-space and ECS-gap research goals |
| 539 | `704081239612a77d5e8902242837dc6fef7aa13c` | tree (tree, 1) | **TREE** | tree of `184e5ae` (line 311) |
| 539 | `dbbeb05387b7ab83ad0bf86d39fc8fc8d6b46727` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 543 | `6d863a0fe8060622942261689ab4616e4d7a6703` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 543 | `90f0766dad2e9e578b50fc77b81957b2139df3cd` | remote/publication (remote, 1) | **COMMIT** | commit `90f0766` — Freeze verified E024 handoff for distinct successor template |
| 543 | `b78837e3077a6c04c1ce67202add9a2268623811` | tree (tree, 1) | **TREE** | tree of `90f0766` (line 310) |
| 547 | `906c2ace53d0502132f68e5b1a9a9ef9701365f9` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 547 | `a1b1b24a64dd7d609abe070310f2b3f438f887b6` | tree (tree, 1) | **TREE** | tree of `c4dd5aa` (line 309) |
| 547 | `c4dd5aa2dd7fc1dc8c0c1659aca9d14d94be709d` | remote/publication (remote, 1) | **COMMIT** | commit `c4dd5aa` — Freeze E025 successor controls from actual published handoff |
| 551 | `656fd3b196e77bb23ac5e41520b33b9725650bcb` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 551 | `e7af4eb85dee2b08246dbaf402dec9514aadaf94` | tree (tree, 1) | **TREE** | tree of `ecedc2e` (line 308) |
| 551 | `ecedc2e7489fd5f6d5d8f79a472df920e1ca35e1` | remote/publication (remote, 1) | **COMMIT** | commit `ecedc2e` — Validate actual E025 handoff and activate successor run |
| 555 | `42517221ee960aa2850f4560c0b2791406be2859` | remote/publication (remote, 1) | **COMMIT** | commit `4251722` — Correct research navigation and remove stale live blocker |
| 555 | `5a4d35f6c43543ef7f0914ce1c4aa1ab42d08aad` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 555 | `c90a72ffb97569c727a230f3db2351d804f90999` | tree (tree, 1) | **TREE** | tree of `4251722` (line 307) |
| 561 | `32736b3a27b43657388b7d339abb5a9dc16a1b4b` | tree (tree, 1) | **TREE** | tree of `96dbd89` (line 306) |
| 561 | `96dbd892c3f4b2c18e87f03a6e0a544e471d075b` | remote/publication (remote, 1) | **COMMIT** | commit `96dbd89` — Preserve interrupted E025 after renewed disclosure rejection |
| 561 | `9e098213ce0f6134c5fb4dacb77eb7d9c7149671` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 567 | `b151582e978299e632bf4308a1297b7698e8502e` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 567 | `d6c07b3d84db4db75e8ac34a540cd914078d1612` | tree (tree, 1) | **TREE** | tree of `fb58b3f` (line 305) |
| 567 | `fb58b3fcca38e7f2d5126b518e4df5e4979300b7` | remote/publication (remote, 1) | **COMMIT** | commit `fb58b3f` — Map configuration coverage and challenge candidate ECS scope gap |
| 571 | `7c05351fe37c79954645c7f3361b3883f2de06ee` | tree (tree, 1) | **TREE** | tree of `a8c6bf7` (line 304) |
| 571 | `a8c6bf76907c78797a777b6ad77b7cdd458e808e` | remote/publication (remote, 1) | **COMMIT** | commit `a8c6bf7` — Document E025 disclosure block and prepare isolated fresh attempt |
| 571 | `b6c4841b3d92b1c9c96ae471fcf0759cc656c5d1` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 575 | `2a701e06d7b8e102109034b622e8cab641ced407` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 575 | `32a5a30eaff655a6b439cf9064236b81049f0e15` | remote/publication (remote, 1) | **COMMIT** | commit `32a5a30` — Record lesson separating response paths from completed observations |
| 575 | `f10e92d33edc5ce4c0711b6e26aba3b303f1b18b` | tree (tree, 1) | **TREE** | tree of `32a5a30` (line 303) |
| 579 | `370276d892c00c13a5aa52ef56738ed6c075f695` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 579 (also 581) | `aef9a035519634c6e77c0dfa5545c9ff180fd2f8` | tree (tree, 1) | **TREE** | tree of `d3a83a5` (line 302) |
| 579 (also 581) | `d3a83a5f9506b99611a84d0338cf07ec7617f16a` | remote/publication (remote, 1) | **COMMIT** | commit `d3a83a5` — Finalize E025 blocked handover and verified preservation state |
| 581 | `370276d892c00c13a5aa52ef56738ed6c075f695` | tree (tree, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 588 (also 590) | `aa5f143572cfebdb0881cbc48866ac6a24623156` | remote/publication (remote, 23) | **NEITHER** | neither a logged commit nor a logged tree |
| 590 | `0438201fa9339e9d3d3bd36a9094f5752faa5591` | remote/publication (remote, 1) | **COMMIT** | commit `0438201` — Complete recovery navigation and expose exact E025 disclosure boundary |
| 590 | `a0d76ed44e89cb460898efd66277d8402049c7f8` | tree (tree, 1) | **TREE** | tree of `0438201` (line 301) |
| 598 | `7a96e742d16628e8110d44cad4b0408371662faf` | remote/publication (remote, 1) | **COMMIT** | commit `7a96e74` — Recover pending handover and activate isolated E025 retry |
| 598 | `8cdd7915a2ae3c44f89d54720a5481d0a18e01e3` | tree (tree, 1) | **TREE** | tree of `7a96e74` (line 300) |
| 598 | `d327d2bb630e3a68e4ff4b24aa273d34637af83f` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 606 | `5f755c05c8872b00c5d667ab2d2fbf5d671a9ea3` | remote/publication (remote, 1) | **COMMIT** | commit `5f755c0` — Preserve E025 retry interruption and exact disclosure blocker |
| 606 | `971c45607113905c3abb130c506437e7c803b689` | tree (tree, 1) | **TREE** | tree of `5f755c0` (line 299) |
| 606 | `b1651a5851eb92206624d82c726e76a0ec241e30` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 610 | `895d925115a3a63f2884c2e6bcf70149c22ae0c4` | remote/publication (remote, 1) | **COMMIT** | commit `895d925` — Prepare exact E025 retry 02 approval handover |
| 610 | `994cad4d371ad2039d647a5bf21244c64d902d06` | tree (tree, 1) | **TREE** | tree of `895d925` (line 298) |
| 610 | `c1211d88dc871019cbabcb1b2e9548c5d3d4b974` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 614 | `8f4b25c63777a7ecf9e607e03117aed12f807438` | remote/publication (remote, 1) | **COMMIT** | commit `8f4b25c` — Finalize interrupted E025 continuation and precise approval boundary |
| 614 | `c0629ba8681973c2232c641f301a43b8d22c84b3` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 614 | `c7202633b652ce04ebe72094d087a8efe12299dd` | tree (tree, 1) | **TREE** | tree of `8f4b25c` (line 297) |
| 623 | `34638d23dd724f96ce8226477402c556ce6bccc1` | remote/publication (remote, 1) | **COMMIT** | commit `34638d2` — Record explicit DeepSeek payload approval and activate E025 retry 02 |
| 623 | `944b3774311322e9d0241b0a23e65d415f4b0ab2` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 623 | `e2742c3aa2f7939fa35acbdab652a3821c7b89d7` | tree (tree, 1) | **TREE** | tree of `34638d2` (line 296) |
| 632 | `26b3b62b2ffaa156ef5cc6de557f04a7745bdd57` | tree (tree, 1) | **TREE** | tree of `f2cea6a` (line 295) |
| 632 | `c6c585f9020980ff775c8efbb16126c9c2d4bfec` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 632 | `f2cea6a04c49b8334b4dfa95cabdeec13aaeb5ad` | remote/publication (remote, 1) | **COMMIT** | commit `f2cea6a` — Pause E025 for actual-source plan approval decision |
| 636 | `749fa030b6ae16cc19fa8fcdb93b4534cf91cd7c` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 636 | `a936b443000f06d23a57ec967d124817b7f9a438` | remote/publication (remote, 1) | **COMMIT** | commit `a936b44` — Checkpoint complete FW5 source reading and proposed roadmap distinction |
| 636 | `e30dfb7e5713314c7c434b44501f21cc20ce0429` | tree (tree, 1) | **TREE** | tree of `a936b44` (line 294) |
| 640 | `0410d138b0825a9194e4c754aab2fe4bf88fabad` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 640 | `079955d365571c96d3e5bc039a9e62de08de6aa3` | remote/publication (remote, 1) | **COMMIT** | commit `079955d` — Partial upload checkpoint for 96686cd2c7aaf204b2fdf0e4cb8e00f525580fcb: Preserve partial E025 retry 02 after network-policy interruption |
| 640 | `fdc0745bb6cac2c6932655d0bdf9a2481568dbd8` | tree (tree, 1) | **TREE** | tree of `079955d` (line 293) |
| 642 | `425fdd97b3163e54fba827e804f994b0649eb6a1` | tree (tree, 1) | **TREE** | tree of `e36c03b` (line 292) |
| 642 | `96686cd2c7aaf204b2fdf0e4cb8e00f525580fcb` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 642 | `e36c03bd26afffa639ea74a6068dd9b6dd90a373` | remote/publication (remote, 1) | **COMMIT** | commit `e36c03b` — Preserve partial E025 retry 02 after network-policy interruption |
| 648 (also 650) | `85647abf4425fca39533a7e9b202cb2caf71fd64` | remote/publication (remote, 1) | **COMMIT** | commit `85647ab` — Propose FW5 source and research-priority update for user approval |
| 648 | `d8aa155efa29864a7f81f8e7bd7d6a4a8dd4892e` | tree (tree, 1) | **TREE** | tree of `85647ab` (line 291) |
| 648 | `dd2ef1fef322c451143cfec5e8089fd53f86c356` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 652 (also 657) | `6be8b9e86b43e940371cd4d5bdfd5cca7998315c` | remote/publication (remote, 1) | **COMMIT** | commit `6be8b9e` — Stop miniReason at FW5 research-plan approval decision |
| 652 | `7749431ee6d27fab6db3d84c90d1f8dceda93d2c` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 652 (also 657) | `7bf81f260229ade336ce26a3f4eeec8beb471309` | tree (tree, 1) | **TREE** | tree of `6be8b9e` (line 290) |
| 657 | `7749431ee6d27fab6db3d84c90d1f8dceda93d2c` | tree (tree, 9) | **NEITHER** | neither a logged commit nor a logged tree |
| 659 | `250c123813383955908245afe1e06981642fbe95` | tree (tree, 1) | **TREE** | tree of `9b5bf1b` (line 289) |
| 659 | `9b5bf1bd8f4fe40b9c83c044370c6026eca3f288` | remote/publication (remote, 1) | **COMMIT** | commit `9b5bf1b` — Resume approved FW5 mapping and concrete study preparation |
| 659 | `c17681fbdbc2f596853962a7181d151e05deed19` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 663 | `3d555a1a1196a9194ca99c51d34c8dda4156c517` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 663 | `a974cadfabc929810774cec8e8b0ce1d7ece19be` | tree (tree, 1) | **TREE** | tree of `df8f9a4` (line 288) |
| 663 | `df8f9a4d7307892a18a6c21a1ae7363fa8191970` | remote/publication (remote, 1) | **COMMIT** | commit `df8f9a4` — Designate FW5 source and prioritize construction with operative use |
| 669 | `0507323ed96feb00689870fd1fb0b250bff26e86` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 669 | `63b85999f1ca176af35b28fbdc420293cf3727ee` | remote/publication (remote, 1) | **COMMIT** | commit `63b8599` — Map attribution obligations to FW5 and isolate ECS2 hypotheses |
| 669 | `c35fe9b7884b3c621346af8e6b77307146d05ea2` | tree (tree, 1) | **TREE** | tree of `63b8599` (line 287) |
| 673 | `042f142c4b26510513100c0a2f9fd714c00754c2` | tree (tree, 1) | **TREE** | tree of `61eefa8` (line 286) |
| 673 | `176d35db8b7d019e9802a1b7d662904bd0b32fa8` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 673 | `61eefa8ddf17e47e51759fd1dcdead045d8b47a8` | remote/publication (remote, 1) | **COMMIT** | commit `61eefa8` — Prioritize SQL construction-use study and independent Account challenge |
| 677 | `2780f0ef9fe433d00e0964cf0e64ddd9a42cbff3` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 677 | `ed8625b84f6d8c9d09b1e43e995f3b06faf98766` | remote/publication (remote, 1) | **COMMIT** | commit `ed8625b` — Align experimental method with FW5 use and contrast obligations |
| 677 | `eec8dc4e7874d173c6a3cd6dd995bdab2d8613c1` | tree (tree, 1) | **TREE** | tree of `ed8625b` (line 285) |
| 681 | `9b49847c58a09bda8ee7f4e89d665fb9cd4f446b` | tree (tree, 1) | **TREE** | tree of `a868224` (line 284) |
| 681 | `a8682247742c5ee57bc97e7c89f22a4189566609` | remote/publication (remote, 1) | **COMMIT** | commit `a868224` — Retain exact knowledge-creation dependencies after independent review |
| 681 | `ff2a1b2a3bf52d36f71e6de324a0b30658478fa2` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 687 | `37d7cd70d15da70c1c4e98d64193af46136dfb59` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 687 | `72b8b1aa6f62bd6e1c894d98a1fb1930c774e501` | remote/publication (remote, 1) | **COMMIT** | commit `72b8b1a` — Publish failed FW5 sufficiency attack with exact matrix evidence |
| 687 | `da8b27903c49c911d27244a2eb8e033d8e7f0f55` | tree (tree, 1) | **TREE** | tree of `72b8b1a` (line 283) |
| 689 | `1d9b131996f176e1e1fc1ba3999cc45611b8988c` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 689 | `703556266704fdf4836e2ebd89c0fc70baf81972` | remote/publication (remote, 1) | **COMMIT** | commit `7035562` — Update agent source authority and record construction preflight scope |
| 689 | `881c85600179fcbc37435511b3adba5c736a21ac` | tree (tree, 1) | **TREE** | tree of `7035562` (line 282) |
| 693 | `703556266704fdf4836e2ebd89c0fc70baf81972` | commit (commit, 20) | **COMMIT** | commit `7035562` — Update agent source authority and record construction preflight scope |
| 699 | `2c7c782ee2d6473d1f1064a58efdae2a074542f0` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 699 | `b0936667e430bd542a4f039ea0057cf578e73e4e` | remote/publication (remote, 1) | **COMMIT** | commit `b093666` — Apply FW5 agent guidance and exact construction adapter decision |
| 699 | `ba43e357fb0097af93da5da461db88a84670d52d` | tree (tree, 1) | **TREE** | tree of `b093666` (line 281) |
| 703 | `45f608acfb621905968d2015897e345c4ae189e7` | tree (tree, 1) | **TREE** | tree of `cf146c7` (line 280) |
| 703 | `b530cc87f9d7033deae035ee87efb67b02e2fc24` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 703 | `cf146c7bde81bb136fd424ba9fdd12c01976b50d` | remote/publication (remote, 1) | **COMMIT** | commit `cf146c7` — Recover current FW5 programme and SQL construction dependency from workflow |
| 707 | `03d28b74e2d3ab7fd73879d8d1c04ce29eb71610` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 707 | `3238fb3c8803d2264cd7c268b60cff36b4b61ac1` | remote/publication (remote, 1) | **COMMIT** | commit `3238fb3` — Prepare SQL construction-use materials with exact missing-state witness |
| 707 | `fd2caec9587ed0734fceca89ef675c0466ede665` | tree (tree, 1) | **TREE** | tree of `3238fb3` (line 279) |
| 711 | `211bf158150d25bf722b1cc6aa04d5fc413a935c` | remote/publication (remote, 1) | **COMMIT** | commit `211bf15` — Record continuation transport and preparation failures with verified fixes |
| 711 | `8d470ab275a6b7acd68abd05c01fae9163e651d2` | tree (tree, 1) | **TREE** | tree of `211bf15` (line 278) |
| 711 | `b416397c13e27e8a30cfb284c61f7ace05efd4af` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 715 | `05c58ae0bce60fcb14f715c115d8ea7d00cf20c5` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 715 | `19ca80175a945eb5b537b3cae5ff615e29253eb7` | tree (tree, 1) | **TREE** | tree of `d4b0675` (line 277) |
| 715 | `d4b06755d12b958074e1e71054a654febdeb1b56` | remote/publication (remote, 1) | **COMMIT** | commit `d4b0675` — Record bounded lessons on information need, prompt custody and Account attack |
| 719 | `6a4c1ea295c5f4d58abe2b4f0457942ccada041e` | remote/publication (remote, 1) | **COMMIT** | commit `6a4c1ea` — Preserve explicit FW5 source mapping and unavailable DeepSeek transport |
| 719 | `a9a047f1eb3c187bdd82cf7d9b2c23866f22c399` | tree (tree, 1) | **TREE** | tree of `6a4c1ea` (line 276) |
| 719 | `f7360e2176008e64655027d8531f712b401fda6d` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 723 | `2a9818173e7501ef214827ae475da093bbbebb2a` | tree (tree, 1) | **TREE** | tree of `f167da9` (line 275) |
| 723 | `e01d574af4cec4b4143fc0e769e51fa04108a297` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 723 | `f167da966719d61dedc3c46ec700d7116f3ffffe` | remote/publication (remote, 1) | **COMMIT** | commit `f167da9` — Record implemented FW5 update, SQL evidence and live transport blocker |
| 727 | `6e972954612c7c2828af73dca086ef2145e8088c` | remote/publication (remote, 1) | **COMMIT** | commit `6e97295` — Freeze E026 SQL construction adapter and zero-call actual-source preflight |
| 727 | `9aa53b69977d2205da5224c07f3bf43c8b3e022f` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 727 | `c70377c74a9fc760a1d6a112ff8716731abc7b07` | tree (tree, 1) | **TREE** | tree of `6e97295` (line 274) |
| 731 | `0b21489f81619173948c2fdf78cb0ceacae95d35` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 731 | `c1507bdde678e9b6101386a8ecb51333bbd075db` | remote/publication (remote, 1) | **COMMIT** | commit `c1507bd` — Document exact E026 continuation command and preserve preparation errata |
| 731 | `e34412028cdaf6a3e3b9c20d999a919549efc975` | tree (tree, 1) | **TREE** | tree of `c1507bd` (line 273) |
| 735 | `6ede6bd6da92a0dfc5ae238835384e42bd14c1a0` | remote/publication (remote, 1) | **COMMIT** | commit `6ede6bd` — Complete E026 handover at live construction transport boundary |
| 735 | `834316497ede54eee0682e083e89d11411633bc0` | tree (tree, 1) | **TREE** | tree of `6ede6bd` (line 272) |
| 735 | `a25aca50ead0f02e02ab572a1cbab65c30ee8191` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 739 (also 741, 743) | `46208163c5e2e1439d9cc1147034642687228999` | tree (tree, 1) | **TREE** | tree of `c4efc77` (line 271) |
| 739 (also 741) | `c4efc7765d05e8999e06322289e068d8198722bd` | remote/publication (remote, 1) | **COMMIT** | commit `c4efc77` — Finish miniReason continuation at prepared E026 live-transport boundary |
| 739 (also 741) | `d971e146e3c97e8ed6d15a4c58961ee81f331d18` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 743 | `c4efc7765d05e8999e06322289e068d8198722bd` | tree (tree, 18) | **COMMIT** | commit `c4efc77` — Finish miniReason continuation at prepared E026 live-transport boundary |
| 747 | `02b12612424759e7a6384321947ae108d4a0d953` | tree (tree, 1) | **TREE** | tree of `d6a6b75` (line 270) |
| 747 | `2dba1ff37f1d9f1c7db866b289c6fd81b8ab85aa` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 747 | `d6a6b754ddc9d901f86e400d84a2140994b56a73` | remote/publication (remote, 1) | **COMMIT** | commit `d6a6b75` — Recover E026 and verify restored DeepSeek transport |
| 757 | `09b24555d3cded90225719b406512202e79dbcf8` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 757 | `ddd455d72f96b1b87d6db3005fa008e645a41bf5` | tree (tree, 1) | **TREE** | tree of `eb6b532` (line 269) |
| 757 | `eb6b53208425cc27aef1bb9c5b80b52e20d2cfa8` | remote/publication (remote, 1) | **COMMIT** | commit `eb6b532` — Record restored E026 runtime and first live construction dispatch |
| 763 (also 765) | `4f0c1444eb7d06f90e6e15a3b0b154733ea69069` | tree (tree, 1) | **TREE** | tree of `da9158f` (line 268) |
| 763 | `d534d4f0b573a46eecbfd420b187badfd857c961` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 763 (also 765) | `da9158fbbc05258ec128861e4124c34fefed2057` | remote/publication (remote, 1) | **COMMIT** | commit `da9158f` — Preserve E026 partial construction and native token-limit interruption |
| 765 | `d534d4f0b573a46eecbfd420b187badfd857c961` | tree (tree, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 769 | `325c9f71f71f74834f9c61256b8902e62cd67bf9` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 769 | `9594175d6feff0981089fd50ba7665c5228f6798` | remote/publication (remote, 1) | **COMMIT** | commit `9594175` — Record E026 environment and repeated native allowance limitation |
| 769 | `dbd726023547d55d3aa0a205b945d939e9af1743` | tree (tree, 1) | **TREE** | tree of `9594175` (line 267) |
| 773 | `05157cc16d7e8506edfab689ef6178cea3fcaef5` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 773 | `64cebfc335d681b23457c0fea9c3b6a027404ecc` | tree (tree, 1) | **TREE** | tree of `6a1de86` (line 266) |
| 773 | `6a1de8600ce71bde4b7e4a81856444d326d177db` | remote/publication (remote, 1) | **COMMIT** | commit `6a1de86` — Preserve E026 lessons on missing selection and scoped continuation |
| 777 | `05b865e10c5ac1989a77277a311c95d777aea333` | tree (tree, 1) | **TREE** | tree of `847f9c0` (line 265) |
| 777 | `7b1d7aa2595e5ac792f6ea69772f9a9faf71ae22` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 777 | `847f9c0ebfd987f2dff92d1cc5135b1bd4845e50` | remote/publication (remote, 1) | **COMMIT** | commit `847f9c0` — Checkpoint reviewed E027 continuation adapter before focused test completion |
| 781 | `0592fe98ae01fe100c3ac9eb8e80b8c4e1c15468` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 781 (also 783) | `6a2b82708aa328984845ec00837c9038a7c295a4` | tree (tree, 1) | **TREE** | tree of `86ad598` (line 264) |
| 781 (also 783) | `86ad5980e353a839e80358c40dd931ea208a571c` | remote/publication (remote, 1) | **COMMIT** | commit `86ad598` — Freeze verified E027 disabled-arm continuation and exact workflow |
| 783 | `0592fe98ae01fe100c3ac9eb8e80b8c4e1c15468` | tree (tree, 7) | **NEITHER** | neither a logged commit nor a logged tree |
| 789 | `1e105b01d05e33e539d28e7e6ae307737cee6678` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 789 (also 791) | `2321ec157093a63f6daab7c9b551c8121e5929ff` | remote/publication (remote, 1) | **COMMIT** | commit `2321ec1` — Publish complete E027 selected Mini construction and exact-prompt control |
| 789 (also 791) | `a7715512f5a7084f9cea650e7241b998dae1c200` | tree (tree, 1) | **TREE** | tree of `2321ec1` (line 263) |
| 791 | `1e105b01d05e33e539d28e7e6ae307737cee6678` | tree (tree, 1) | **NEITHER** | neither a logged commit nor a logged tree |
| 795 | `47c461e7689b4d7e1f8248d3eeaba656f81fa6f5` | tree (tree, 1) | **TREE** | tree of `e239235` (line 262) |
| 795 | `a7c6be3e8661b21d4f1cd9920a127360831d406e` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 795 | `e239235451215d38e326a1eba58515298c79141b` | remote/publication (remote, 1) | **COMMIT** | commit `e239235` — Preserve selected-account interpretation witness and E028 study decision |
| 801 | `26730e138d4843f234f7e4551352bb9014d3f879` | remote/publication (remote, 1) | **COMMIT** | commit `26730e1` — Review selected E027 account and preserve interpretation-dependent omission |
| 801 | `ac2a0be99a3e7eb3a93a583dd4215763c162f525` | tree (tree, 1) | **TREE** | tree of `26730e1` (line 261) |
| 801 | `f21d33069fb7e6184356f1ce306814244cbc6ef6` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 807 | `4b0490e96f20de50f5a16c4bd479a43e8d3768bb` | tree (tree, 1) | **TREE** | tree of `61c9a74` (line 260) |
| 807 | `61c9a74ddf97c07e01c493f200862faa989fee70` | remote/publication (remote, 1) | **COMMIT** | commit `61c9a74` — Compare actual SQL samples by update route and retained-state claims |
| 807 | `f49fd81f29849b2d235490c41d0c0d2220755e78` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 813 | `55686c1c228d07a2e55d9558fd2a4efa09027f5e` | remote/publication (remote, 1) | **COMMIT** | commit `55686c1` — Record SQL observation-route lessons and separate E028 event oracle |
| 813 | `cd02f29eeb150f459042f4e8b8866f641fe3e935` | tree (tree, 1) | **TREE** | tree of `55686c1` (line 259) |
| 813 | `cea0619f8d950e289e7302d5c9eb07d7db91823b` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 819 | `6da9eda0bc8cfd53b120f939621649cc8cb514ea` | tree (tree, 1) | **TREE** | tree of `9c39f75` (line 258) |
| 819 | `9c39f756db54c6ed032cada80f06f0cd70d22f67` | remote/publication (remote, 1) | **COMMIT** | commit `9c39f75` — Verify E028 one-cycle use and shared-criticism return adapter |
| 819 | `ac8f12df5d3cd0db345ea73274a9ba6b577ae460` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 823 | `0dcb69ddb09907c29998b35ad0f0fdf02170d861` | remote/publication (remote, 1) | **COMMIT** | commit `0dcb69d` — Freeze E028 actual-candidate use and shared criticism return study |
| 823 | `274859008565ebc52f1ae44d48f94e4f96093538` | remote/publication (remote, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 823 | `999bca14601b25dc35b468150936e51e99e53f2e` | tree (tree, 1) | **TREE** | tree of `0dcb69d` (line 257) |
| 825 | `274859008565ebc52f1ae44d48f94e4f96093538` | tree (tree, 13) | **NEITHER** | neither a logged commit nor a logged tree |
| 831 | `164c34bc0d043fad420fa33474491db233a0cf00` | tree (tree, 1) | **TREE** | tree of `770eeec` (line 255) |
| 831 | `770eeecf6d552f5299b0e4a0af40dee9d2d4d466` | tree (tree, 2) | **COMMIT** | commit `770eeec` — Record E028 evidence recovery and Windows execution blockers |
| 831 | `9350089` | remote/publication (remote, 32) | **UNRESOLVED-SHORT** | — |
| 837 | `24004293ac67ac4940699ee6ce5c6d335163fe69` | remote/publication (remote, 1) | **COMMIT** | commit `2400429` — Checkpoint exact-byte verification and logger recovery progress |
| 837 | `6642435` | remote/publication (remote, 25) | **UNRESOLVED-SHORT** | — |
| 837 | `d51614673ec54a0248cc2c7fac41e98a8c5fa6fa` | tree (tree, 1) | **TREE** | tree of `2400429` (line 254) |
| 843 | `3c636a98114abe786a372b78b89d601ad98ea9f6` | commit (commit, 1) | **COMMIT** | commit `3c636a9` — Support atomic experiment activity logging on Windows |
| 843 | `659825bd06e8d2edf5b26f87dd4eaad7faf03f9d` | tree (tree, 1) | **TREE** | tree of `3c636a9` (line 253) |
| 843 | `7380178` | commit (commit, 18) | **UNRESOLVED-SHORT** | — |
| 849 | `24948f5519fc52f329f219cdb1f15c53240e1996` | tree (tree, 1) | **TREE** | tree of `87fe552` (line 252) |
| 849 | `7832109` | remote/publication (remote, 25) | **UNRESOLVED-SHORT** | — |
| 849 | `87fe552c45d8f8f5c2981907557b23fa5eeff0f5` | remote/publication (remote, 1) | **COMMIT** | commit `87fe552` — Record full-route Windows blocker and select Linux preflight |
| 853 | `3207588` | remote/publication (remote, 18) | **UNRESOLVED-SHORT** | — |
| 853 | `8ed2e4e66b7f4e35c0786fd72e851e4af8570546` | tree (tree, 1) | **TREE** | tree of `a9c3a6f` (line 251) |
| 853 | `a9c3a6fb8695b5e826453607fdb3386d921dff7d` | remote/publication (remote, 1) | **COMMIT** | commit `a9c3a6f` — Checkpoint no-spend filesystem guard and Linux execution design |
| 859 | `19c600bb5dfb668fca1ee82b4328a63159d4e0ab` | tree (tree, 1) | **TREE** | tree of `c1eeb5e` (line 250) |
| 859 | `9055740` | remote/publication (remote, 9) | **UNRESOLVED-SHORT** | — |
| 859 | `c1eeb5e2f056cb71190daa3242357afd0fa86187` | tree (tree, 5) | **COMMIT** | commit `c1eeb5e` — Refuse unsupported experiment storage before spending provider calls |
| 863 | `1182fe0b22f1a69621cede8779a3de573e27c758` | tree (tree, 1) | **TREE** | tree of `94772a4` (line 249) |
| 863 | `2313283` | remote/publication (published, 19) | **UNRESOLVED-SHORT** | — |
| 863 | `94772a432ba79df5274b73b19e1efa39a67eb169` | remote/publication (published, 1) | **COMMIT** | commit `94772a4` — Checkpoint bounded Linux workflow and call-publication design |
| 870 | `0899289` | remote/publication (remote, 9) | **UNRESOLVED-SHORT** | — |
| 870 | `232364232e8e44482ea0101a57aa9061ee639777` | tree (tree, 9) | **COMMIT** | commit `2323642` — Record E028 entrypoint review and recovery progress |
| 870 | `3d90cac4a96b2dd3702d9706cdd3921920276ace` | tree (tree, 1) | **TREE** | tree of `2323642` (line 247) |
| 871 | `095ae4696413c0392ae549bd4f58000f00b749e2` | tree (tree, 1) | **TREE** | tree of `b82e7da` (line 246) |
| 871 | `8332239` | remote/publication (remote, 28) | **UNRESOLVED-SHORT** | — |
| 871 | `b82e7da3dbfda4e43a4ca8826f406e26ee4e7339` | tree (tree, 2) | **COMMIT** | commit `b82e7da` — Add checkpointed Linux runner for the frozen E028 recovery |
| 882 | `7808c70c46c27c42be1d4d10f8ac5cbb4a293f1b` | tree (tree, 1) | **COMMIT** | commit `7808c70` — Assess research trajectory against revised FW5 goals |
| 886 | `28ec4f4b2efa1dd8f1598247ffb3775c0c278534` | commit (commit, 0) | **COMMIT** | commit `28ec4f4` — Freeze DeepSeek routing harness and first actual request |
| 886 | `28ec4f4b2efa1dd8f1598247ffb3775c0c278534` | tree (tree, 1) | **COMMIT** | commit `28ec4f4` — Freeze DeepSeek routing harness and first actual request |
| 890 | `35338a761e8947003399be42cfc4a7506b073776` | tree (tree, 1) | **COMMIT** | commit `35338a7` — Record H002 initial DeepSeek use and freeze criticism request |
| 896 | `54fad3e` | tree (tree, 29) | **UNRESOLVED-SHORT** | — |
| 898 | `d5c992ae26799dc72d49da0b475c6d9e6b6521d4` | tree (tree, 1) | **COMMIT** | commit `d5c992a` — Record H002 returned fresh use and freeze archived branch |
| 900 | `88798e6e0dd63b3d1dbf37a2154abe1902a8a20b` | tree (tree, 1) | **COMMIT** | commit `88798e6` — Preserve H002 archived U1 and freeze final DeepSeek request |
| 912 | `74806e48634aff6a51aeb8e3e169b8b1e8ea6337` | tree (tree, 1) | **COMMIT** | commit `74806e4` — Add reusable miniReason operations skill and agent entry hook |
| 918 | `c07a730aa9ac3dbc550a6dbc5cc93439d040bf93` | tree (tree, 1) | **COMMIT** | commit `c07a730` — Record H002 attribution and continuation lessons |
| 924 | `fea4defaf9835e29f739f001cd973db28676174d` | tree (tree, 1) | **COMMIT** | commit `fea4def` — Define source-led twenty-cycle language error-discovery study |
| 926 | `f4cb6e6c360069f47d9e8b310a93753e3f0311fd` | tree (tree, 1) | **COMMIT** | commit `f4cb6e6` — Record H003 preparation and reopened testing |
| 928 | `74f1e196e2531efc24e96545ff97ba531d047824` | tree (tree, 1) | **COMMIT** | commit `74f1e19` — Freeze H003 twenty-cycle language error study and concurrent runner |
| 932 | `68792be5dd70bff75047ed0660f9193d94325b9b` | tree (tree, 1) | **COMMIT** | commit `68792be` — Verify public H003 inputs and authorize first concurrent cycle |
| 934 | `9106e406c47c866956109717b2f3c9b25cc9005f` | tree (tree, 1) | **COMMIT** | commit `9106e40` — Preserve H003 first concurrent cycle and instrumentation gate |
| 936 | `95c0d0623f84583118416ae86194c6efbb21d344` | tree (tree, 1) | **COMMIT** | commit `95c0d06` — Document H003 Windows command-length failure and recovery |
| 958 | `4d3709d33a207552411d88e1c87480986b253a4c` | tree (tree, 1) | **COMMIT** | commit `4d3709d` — Preserve H003 cycle 5 observations and custody checkpoint |
| 960 | `9efc032f9550c4cc9e21fd3109823bfc0c8491b7` | tree (tree, 1) | **COMMIT** | commit `9efc032` — Review H003 block1 errors and accept grounded continuation |
| 992 | `a5626642f5917504bd7a98aaedae63f9fb5ce536` | tree (tree, 1) | **COMMIT** | commit `a562664` — Preserve H003 cycle 10 observations and custody checkpoint |
| 1000 | `103516c` | remote/publication (published, 36) | **UNRESOLVED-SHORT** | — |
| 1000 | `39d40bc64217d1903b1691410deab96b7b8ba4ce` | tree (tree, 1) | **COMMIT** | commit `39d40bc` — Preserve H003 cycle 11 observations and custody checkpoint |
| 1004 | `db5d852b93d0312c56e2ca6b3998d698f373d88d` | tree (tree, 1) | **COMMIT** | commit `db5d852` — Close H003 and distinguish partial work from failed inquiry |
| 1006 | `fabe590013147bfeabf4d61a6c3578188bb14536` | tree (tree, 1) | **COMMIT** | commit `fabe590` — Declare bounded H004 partial-contribution continuation |
| 1008 | `b1f0513baf7eece614676952008f08933c100c04` | tree (tree, 1) | **COMMIT** | commit `b1f0513` — Record H003 terminal state and H004 preparation boundary |
| 1012 | `ca2f9eea17846223db10f916f1f79f7a7402c58f` | tree (tree, 1) | **COMMIT** | commit `ca2f9ee` — Record exact visibility evidence for partial criticism targets |
| 1014 | `4d2cc4b24df8b6ce0c4c27770a7eb9217107ac8b` | tree (tree, 1) | **COMMIT** | commit `4d2cc4b` — Record H004 root review gate and strict partial-status requirement |
| 1057 | `c78c6b1435a9feb49876f9509cfd84285ca2f4fd` | commit (commit, 3) | **COMMIT** | commit `c78c6b1` — Freeze H004 wave 6 exact dependency-ready inputs |
| 1065 | `fceb867ec8a6f104338031f92b01d85a354a964b` | commit (commit, 3) | **COMMIT** | commit `fceb867` — Freeze H004 wave 7 exact dependency-ready inputs |
| 1066 | `fceb867` | commit (commit, 1) | **UNRESOLVED-SHORT** | — |
| 1073 | `fbb789f7d3f8714d7f76e37d3aed34ecab241144` | commit (commit, 3) | **COMMIT** | commit `fbb789f` — Freeze H004 wave 8 exact dependency-ready inputs |
| 1074 | `15a4cb6` | remote/publication (published, 3) | **UNRESOLVED-SHORT** | — |
| 1081 | `248fc249b84df6cc46949fbc398f9216819cd654` | commit (commit, 3) | **COMMIT** | commit `248fc24` — Freeze H004 wave 9 exact dependency-ready inputs |
| 1088 | `c081a1808e5e620adb75966588a4370b360b9bd2` | commit (commit, 3) | **COMMIT** | commit `c081a18` — Freeze H004 wave 10 exact dependency-ready inputs |
| 1105 | `0c562e068089c695a2b45f099d53c93aeb962057` | commit (commit, 3) | **COMMIT** | commit `0c562e0` — Freeze H004 wave 11 exact dependency-ready inputs |
| 1112 | `0f83a19ade9df56f4c8dd32d01c264dd0a6407b8` | commit (commit, 3) | **COMMIT** | commit `0f83a19` — Freeze H004 wave 12 exact dependency-ready inputs |
| 1119 | `962e02a06786ac018029728e1e517e0b26a9b83a` | commit (commit, 3) | **COMMIT** | commit `962e02a` — Freeze H004 wave 13 exact dependency-ready inputs |
| 1126 | `5620742b21db6c6879ca544eba8608fccfbea062` | commit (commit, 3) | **COMMIT** | commit `5620742` — Freeze H004 wave 14 exact dependency-ready inputs |
| 1133 | `16aa04cb58d1f5c996e70fd9ec60aff5c44e972d` | commit (commit, 3) | **COMMIT** | commit `16aa04c` — Freeze H004 wave 15 exact dependency-ready inputs |
| 1144 | `ef0be892982604ace4fc2aeefaf61c03d35583f3` | commit (commit, 3) | **COMMIT** | commit `ef0be89` — Freeze H004 wave 16 exact dependency-ready inputs |
| 1151 | `a01079ff5e08e72652248d39ece82aa79c03ffc2` | commit (commit, 3) | **COMMIT** | commit `a01079f` — Freeze H004 wave 17 exact dependency-ready inputs |
| 1158 | `73356d208e66231325f72db31443a353f4e231ed` | commit (commit, 3) | **COMMIT** | commit `73356d2` — Freeze H004 wave 18 exact dependency-ready inputs |
| 1160 | `8d0c87ed483f3951bc5275d3a3d3684024895afd` | tree (tree, 2) | **COMMIT** | commit `8d0c87e` — Preserve H004 wave 18 observations and separate partial coverage |
| 1190 (also 1192) | `bd4a0fdd8809196ad78050d53c3760d4b81e4040` | tree (tree, 2) | **COMMIT** | commit `bd4a0fd` — Update README with completed study and prose-audit candidate |
| 1214 | `40bd5de738170ce84f1c483abe49f63ec774f07e` | commit (commit, 1) | **COMMIT** | commit `40bd5de` — Add CLAUDE.md with orchestration rule |
| 1214 | `40bd5de738170ce84f1c483abe49f63ec774f07e` | tree (tree, 1) | **COMMIT** | commit `40bd5de` — Add CLAUDE.md with orchestration rule |
| 1214 | `44bc683ce24d172e3fb93fea5fd65ba597116181` | tree (tree, 1) | **TREE** | tree of `40bd5de` (line 134) |
| 1244 | `b55832f684f91729ade4317465c748f891aa522a` | remote/publication (published, 37) | **COMMIT** | commit `b55832f` — Record the missing CLAUDE.md receipt after the fact |
| 1252 | `8b3a1f170f1f7507336447f8f469c5f1afab6241` | tree (tree, 1) | **COMMIT** | commit `8b3a1f1` — Close the session with the final verified publication line |
| 1252 | `b02ef276fb7d90ee4ff563bbcc8b33efae4bfd00` | commit (commit, 21) | **COMMIT** | commit `b02ef27` — Freeze H005 prose problems and explicit template connectivity |
| 1252 | `bc011faa75474cd4902ee026a293eefd70677b78` | tree (tree, 1) | **TREE** | tree of `8b3a1f1` (line 123) |
| 1252 | `d671dc9290b554d978d6b84b15b511a5d5530036` | commit (commit, 3) | **COMMIT** | commit `d671dc9` — Publish H005 three-cycle comparative protocol |
| 1268 | `575bc5844aca282e5407760393e2936a6a08860c` | commit (commit, 1) | **COMMIT** | commit `575bc58` — Merge origin/main into the working branch, keeping both tails in full |
| 1268 | `6a3a344e1cac4379162e5aeb4a73e5f434ad7d23` | tree (tree, 1) | **TREE** | tree of `575bc58` (line 118) |
| 1274 | `c40dda76579ebd3f1b873598f6d8c6c06d39c777` | tree (tree, 21) | **COMMIT** | commit `c40dda7` — Log the merge outcome and the post-merge suite baseline |
| 1282 | `1cadd3ec61f79315fb356d07c9ed36baaa6ff707` | tree (tree, 1) | **COMMIT** | commit `1cadd3e` — Close with the verified merge and E028 correction identities |
| 1282 | `1d6f3d29bfc98d6f678694fcdba69bd4ca9a1648` | tree (tree, 1) | **TREE** | tree of `1cadd3e` (line 108) |
| 1284 | `20b82184b6cd69415b2d5ae743afda53df321b93` | commit (commit, 1) | **COMMIT** | commit `20b8218` — Merge origin/main into the working branch, keeping both tails in full |
| 1284 | `995cb82574f2a4b4cb372e31b1e0310827c29eb5` | tree (tree, 1) | **TREE** | tree of `20b8218` (line 103) |
| 1284 | `bc21850` | commit (commit, 1) | **UNRESOLVED-SHORT** | — |
| 1288 | `b2a33283dc1e05fb83c3357b26e2cc12115f6b6c` | commit (commit, 1) | **NEITHER** | neither a logged commit nor a logged tree |
| 1290 | `e63f8d5` | commit (commit, 31) | **UNRESOLVED-SHORT** | — |
| 1290 | `ffbb9f3fe1f65fff4dc74d4afca7daaf53051c49` | commit (commit, 4) | **COMMIT** | commit `ffbb9f3` — Recover Mini's requirement register from h-EPI and record its provenance |
| 1294 | `1bcc1c8e537d31b7e62647f382e93e0120baeb7a` | tree (tree, 1) | **TREE** | tree of `23e2f80` (line 100) |
| 1294 | `23e2f801f8f5edc5eb122fc913185889455356be` | tree (tree, 1) | **COMMIT** | commit `23e2f80` — Close REC-20260914-K with the verified register publication identities |
| 1302 | `5d39dedd85bee8fcc72f329a9bae87d0c34e0533` | tree (tree, 1) | **TREE** | tree of `ad2fb9d` (line 97) |
| 1302 (also 1304) | `9607fba6f0a3066fbcab282c9ae0fad823e52e0c` | commit (commit, 2) | **NEITHER** | neither a logged commit nor a logged tree |
| 1302 | `ad2fb9da1a5eb8df9b08e1e941304e9f36c9268a` | tree (tree, 1) | **COMMIT** | commit `ad2fb9d` — Close REC-20260914-L with the verified review publication identities |
| 1304 | `377e5965ad20b22b07274655a9151d913d76db0a` | commit (commit, 5) | **NEITHER** | neither a logged commit nor a logged tree |
| 1308 | `1feed77c3e39acf69271b960f0b5e1e1b4743ea9` | tree (tree, 32) | **COMMIT** | commit `1feed77` — Close REC-20260914-M with the verified publication identities |
| 1308 | `38b07b0957d467d34ad7e27e7ab9cfbfed7576ae` | tree (tree, 5) | **TREE** | tree of `1feed77` (line 95) |
| 1308 | `649ae2b` | remote/publication (published, 5) | **UNRESOLVED-SHORT** | — |
| 1308 (also 1310) | `9607fba6f0a3066fbcab282c9ae0fad823e52e0c` | tree (tree, 28) | **NEITHER** | neither a logged commit nor a logged tree |
| 1310 | `1feed77` | tree (tree, 2) | **UNRESOLVED-SHORT** | — |
| 1310 | `7745fe9` | commit (commit, 32) | **UNRESOLVED-SHORT** | — |
| 1314 | `9ad5031e740cfa90b4db274cf672321aba46c619` | tree (tree, 5) | **TREE** | tree of `c2b92e1` (line 92) |
| 1314 | `c2366dd` | remote/publication (published, 5) | **UNRESOLVED-SHORT** | — |
| 1314 | `c2b92e1eef04cf4aa3c90ad36769718ed705b53b` | commit (commit, 2) | **COMMIT** | commit `c2b92e1` — Close REC-20260914-N with the verified publication identities |
| 1314 | `c2b92e1eef04cf4aa3c90ad36769718ed705b53b` | tree (tree, 32) | **COMMIT** | commit `c2b92e1` — Close REC-20260914-N with the verified publication identities |
| 1316 | `0ae29ee` | commit (commit, 2) | **UNRESOLVED-SHORT** | — |
| 1316 | `0ae29ee` | tree (tree, 2) | **UNRESOLVED-SHORT** | — |
| 1316 | `6e7dac0` | commit (commit, 2) | **UNRESOLVED-SHORT** | — |
| 1316 | `c2b92e1` | tree (tree, 2) | **UNRESOLVED-SHORT** | — |
| 1328 | `63c345b` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1332 | `8a99d3fb4f9ab39e2a061d8a1389c11fb6c4be5b` | tree (tree, 1) | **COMMIT** | commit `8a99d3f` — Close REC-20260914-P with the verified publication identities |
| 1332 | `d48f25524844f29bca930d2e1af3a0b31ebe6e46` | tree (tree, 1) | **TREE** | tree of `8a99d3f` (line 86) |
| 1334 | `b713662` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1344 | `3a110e1fa0d4d0f7e4f19b98b08f8252055f4eb4` | tree (tree, 2) | **TREE** | tree of `6114aed` (line 82) |
| 1344 | `6114aedb3de0d06a0861229d310d7a5a40932526` | commit (commit, 2) | **COMMIT** | commit `6114aed` — Open REC-20260914-R for the occurrence-01 snapshot analysis outputs |
| 1344 | `7e5ae00` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1358 | `d0e5d343b01792d9be93e22616f2758c7028e874` | remote/publication (remote, 25) | **COMMIT** | commit `d0e5d34` — Close REC-20260914-R with the verified publication identities |
| 1360 (also 1382) | `1abe87e` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1374 | `ace70aa` | commit (commit, 2) | **UNRESOLVED-SHORT** | — |
| 1376 | `31522aa` | commit (commit, 2) | **UNRESOLVED-SHORT** | — |
| 1380 | `e9a4063b41c8422583e83e61005f69c21cb64a33` | remote/publication (remote, 25) | **COMMIT** | commit `e9a4063` — Close REC-20260914-S with the verified publication identities |
| 1382 (also 1390) | `d777561` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1382 | `d777561e41968d6bf26ba900e6953ac91f852503` | tree (tree, 2) | **COMMIT** | commit `d777561` — Publish the F001 successor runner v2 and the occurrence-07/08 register |
| 1382 | `e9a4063` | remote/publication (published, 40) | **UNRESOLVED-SHORT** | — |
| 1384 | `3c8cf00` | commit (commit, 2) | **UNRESOLVED-SHORT** | — |
| 1384 | `3c8cf008b1f8f4f87ace0516e2e86d221f2a6452` | tree (tree, 2) | **COMMIT** | commit `3c8cf00` — Freeze F001 occurrences 07 and 08 under runner v2 |
| 1386 | `05f9112` | commit (commit, 17) | **UNRESOLVED-SHORT** | — |
| 1386 | `1e497fb` | commit (commit, 17) | **UNRESOLVED-SHORT** | — |
| 1386 | `537939c` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1386 | `667849d` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1386 | `70d89f5` | commit (commit, 26) | **UNRESOLVED-SHORT** | — |
| 1386 | `7b0c993` | commit (commit, 17) | **UNRESOLVED-SHORT** | — |
| 1386 | `d64bf7e` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1386 | `ed83543` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1388 | `4bae24bbbc7c7eb3f3714cafe19883c6b0e45d11` | tree (tree, 2) | **TREE** | tree of `d777561` (line 65) |
| 1388 | `abf19ad` | commit (commit, 2) | **UNRESOLVED-SHORT** | — |
| 1390 | `240b0ce` | commit (commit, 26) | **UNRESOLVED-SHORT** | — |
| 1390 | `240b0ceb51c3e5e5f1215abfd85b40e1e3b120a8` | tree (tree, 2) | **COMMIT** | commit `240b0ce` — Record the REC-20260914-T publication, freeze, round and analysis outcomes |
| 1390 | `75b2d0d15520f3b1c7f81c337c9af8abc2ee5ac1` | tree (tree, 1) | **TREE** | tree of `240b0ce` (line 54) |
| 1394 (also 1421) | `89c4f9142b3c9c7eef12e7a33b3e28adfe48efab` | tree (tree, 1) | **TREE** | tree of `ad3e347` (line 52) |
| 1394 (also 1423) | `ad3e347` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1394 | `ad3e347b7c629414582a952c2bea8e4031bea702` | tree (tree, 2) | **COMMIT** | commit `ad3e347` — Publish the C001 contrast-triple study and freeze occurrence-01 |
| 1421 | `04654a3` | remote/publication (published, 20) | **UNRESOLVED-SHORT** | — |
| 1421 | `ab0a812c1bc45fcdf27d883ebd343df06be0ed1a` | remote/publication (published, 32) | **TREE** | tree of `04654a3` (line 51) |
| 1421 | `ad3e347` | tree (tree, 4) | **UNRESOLVED-SHORT** | — |
| 1423 | `14b776dbe7b8d651f3d418a9546e83361cf1bffa` | tree (tree, 1) | **TREE** | tree of `d6b7e30` (line 45) |
| 1423 | `d6b7e30fbb15d86834bef0e6f86ed9239a6768fc` | tree (tree, 2) | **COMMIT** | commit `d6b7e30` — Close REC-20260914-U with the C001 dispatch, audit and juxtaposition outcomes |
| 1431 (also 1445) | `9c0ca99` | commit (commit, 2) | **UNRESOLVED-SHORT** | — |
| 1435 (also 1443) | `2ebc05255cc08a827a452234ec98268dc350f5e0` | tree (tree, 2) | **COMMIT** | commit `2ebc052` — C001 occurrence-02 dispatch checkpoint 1: wave 1 (original), 5 of 20 |
| 1435 (also 1443) | `9d13ff9d21c3a0d488726c44acf4bb58ab22b833` | tree (tree, 1) | **TREE** | tree of `2ebc052` (line 40) |
| 1437 (also 1443) | `15ce6f5f426355dd4b31593310c697bd32b872a9` | tree (tree, 1) | **TREE** | tree of `861542b` (line 39) |
| 1437 (also 1443) | `861542b5add60d61e18e182288b820c4ac6003f7` | tree (tree, 2) | **COMMIT** | commit `861542b` — C001 occurrence-02 dispatch checkpoint 2: wave 2 (recoding), 10 of 20 |
| 1439 (also 1443) | `0325dfe61ac16e8bde351595d3a0152d80aeb6a2` | tree (tree, 1) | **TREE** | tree of `297e686` (line 38) |
| 1439 (also 1443) | `297e686eb0935ee6d9260e3177909cbffab7ccce` | tree (tree, 2) | **COMMIT** | commit `297e686` — C001 occurrence-02 dispatch checkpoint 3: wave 3 (carrier), 15 of 20 |
| 1441 (also 1445) | `2d7239a` | commit (commit, 8) | **UNRESOLVED-SHORT** | — |
| 1441 (also 1449) | `9045a94` | commit (commit, 2) | **UNRESOLVED-SHORT** | — |
| 1441 (also 1443) | `b37f6581765502f1364cfb5e112790cc2eee4985` | tree (tree, 1) | **TREE** | tree of `ff3b6b3` (line 36) |
| 1441 (also 1443) | `ff3b6b3aa3fdc84023b58bff85d36911dc2eeb16` | tree (tree, 2) | **COMMIT** | commit `ff3b6b3` — C001 occurrence-02 audit and table: 20/20 COMPLETE, one juxtaposition |
| 1443 | `0afbc6647b3359afc10761d655a14ec24dedd776` | tree (tree, 4) | **COMMIT** | commit `0afbc66` — Close REC-20260914-V: C001 occurrence-02 is 20 of 20 COMPLETE |
| 1443 | `1f5e2646a2534e59a45e84b0e6abf42f6a154ce8` | tree (tree, 3) | **COMMIT** | commit `1f5e264` — C001 occurrence-02 dispatch checkpoint 4: wave 4 (control), 20 of 20 |
| 1443 | `25c19aff1c4190a08e0c2a9b73a0f299b7f33a66` | tree (tree, 3) | **TREE** | tree of `0afbc66` (line 35) |
| 1443 | `2d7239acd70f14aa049b62034a803784883da7b7` | tree (tree, 3) | **COMMIT** | commit `2d7239a` — Publish the C001 occurrence-02 instrument under REC-20260914-V |
| 1443 | `333ad29b04099e75835b9824ef7050b8509b89e4` | tree (tree, 1) | **TREE** | tree of `1f5e264` (line 37) |
| 1443 | `9c0ca9982548f256354e164c3b31df17decc6c78` | tree (tree, 3) | **COMMIT** | commit `9c0ca99` — Freeze C001 occurrence-02 before dispatch: plan_id 1d9f47ac, 20 calls, 0 sent |
| 1443 | `9d0ab88f6940b220110797722fd4e628aef9c43e` | tree (tree, 1) | **TREE** | tree of `2d7239a` (line 42) |
| 1443 | `a440df4bf85f34ddd16030c0631e84e95c899a09` | tree (tree, 1) | **TREE** | tree of `9c0ca99` (line 41) |
| 1447 (also 1449) | `dd2e067` | commit (commit, 2) | **UNRESOLVED-SHORT** | — |
| 1447 | `f50db28` | commit (commit, 36) | **UNRESOLVED-SHORT** | — |
| 1449 (also 1453) | `28f0d6bcbc6ec0022a75d73f9bb6468547ac2fb4` | tree (tree, 1) | **TREE** | tree of `4714ee8` (line 32) |
| 1449 (also 1453) | `4714ee82f4109cddbce57a3f232e86f79489bb27` | tree (tree, 3) | **COMMIT** | commit `4714ee8` — Open REC-20260914-W to refresh and publish the session orchestration report |
| 1451 | `4714ee8` | tree (tree, 31) | **UNRESOLVED-SHORT** | — |
| 1451 (also 1453) | `7034b1266a8aca02b39d368d00e10a1d131e2c9c` | tree (tree, 1) | **TREE** | tree of `dc5491e` (line 31) |
| 1451 | `dc5491e` | tree (tree, 4) | **UNRESOLVED-SHORT** | — |
| 1451 (also 1453) | `dc5491e0e6d992ecd2e36b2f6c2adf7e854fe91c` | tree (tree, 3) | **COMMIT** | commit `dc5491e` — Publish the refreshed session orchestration report under REC-20260914-W |
| 1453 | `710b14ad01890e18a0e40d194461b61f716f2aba` | tree (tree, 3) | **TREE** | tree of `94edb7a` (line 30) |
| 1453 | `94edb7ac36d027eca098bf81aa42e521bfb8b4c0` | tree (tree, 4) | **COMMIT** | commit `94edb7a` — Close REC-20260914-W: the session orchestration report is published and verified |
| 1459 | `a1e516c54673c8a3ea2968ca3362ec6d1d725fb8` | commit (commit, 2) | **COMMIT** | commit `a1e516c` — F002 round 1: publish wave0001's frozen inputs for both occurrences |
| 1459 | `e9d9c47d96f45f8e9f356d7300ff7a8b4796b044` | remote/publication (published, 29) | **COMMIT** | commit `e9d9c47` — F002 round 1 records: wave0001 terminal on both occurrences, 2 of 10 calls |
| 1463 | `48ca127540a40dee7dee62b7d1f4a8386174d0ba` | commit (commit, 2) | **COMMIT** | commit `48ca127` — F002 round 2: publish wave0002's frozen inputs and checkpoint round 1 |
| 1463 | `7b0303f182289142bc0d79794aa95a1823b12a10` | remote/publication (published, 29) | **COMMIT** | commit `7b0303f` — F002 round 2 records: wave0002 terminal on both occurrences, 6 of 10 calls |
| 1467 | `d6157cf39f07aa60abf209e32c46ae0d57535c7d` | remote/publication (published, 29) | **COMMIT** | commit `d6157cf` — F002 round 3 records: wave0003 terminal, 8 of 10 calls, one FAILED |
| 1467 | `e8357c3d236c4c837a27920c96ae8c7301c447c4` | commit (commit, 2) | **COMMIT** | commit `e8357c3` — F002 round 3: publish wave0003's frozen inputs and checkpoint round 2 |
| 1469 (also 1471) | `96ca2eb` | commit (commit, 8) | **UNRESOLVED-SHORT** | — |
| 1471 | `7bff688` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1475 | `96ca2eb` | remote/publication (published, 18) | **UNRESOLVED-SHORT** | — |
| 1477 (also 1479) | `228e33f` | commit (commit, 39) | **UNRESOLVED-SHORT** | — |
| 1477 | `bfc5c8e` | remote/publication (published, 11) | **UNRESOLVED-SHORT** | — |
| 1479 | `bfc5c8e` | commit (commit, 3) | **UNRESOLVED-SHORT** | — |
| 1487 | `f11f350236827bcb150117a9c6400c76d301b514` | commit (commit, 2) | **COMMIT** | commit `f11f350` — F002 occurrence-03: freeze and publish the plan and wave0001 inputs, before dispatch |
| 1489 | `90d55fb0d7aee891a333e3b0c88cb2fdc7126f0c` | commit (commit, 2) | **COMMIT** | commit `90d55fb` — F002 occurrence-03: round 1 records (account COMPLETE) and wave0002 inputs |
| 1493 | `3c49718` | commit (commit, 8) | **UNRESOLVED-SHORT** | — |
| 1495 | `05eebc4` | tree (tree, 2) | **UNRESOLVED-SHORT** | — |
| 1495 | `23bae77` | tree (tree, 2) | **UNRESOLVED-SHORT** | — |
| 1495 | `341c29c` | tree (tree, 6) | **UNRESOLVED-SHORT** | — |
| 1495 | `3c49718` | tree (tree, 6) | **UNRESOLVED-SHORT** | — |
| 1495 | `4ff209b` | tree (tree, 6) | **UNRESOLVED-SHORT** | — |
| 1495 | `674fa0b` | tree (tree, 2) | **UNRESOLVED-SHORT** | — |
| 1495 | `90d55fb` | tree (tree, 6) | **UNRESOLVED-SHORT** | — |
| 1495 | `90d55fb` | remote/publication (published, 27) | **UNRESOLVED-SHORT** | — |
| 1495 | `b49b68f` | tree (tree, 2) | **UNRESOLVED-SHORT** | — |
| 1495 | `c56b129` | tree (tree, 6) | **UNRESOLVED-SHORT** | — |
| 1495 | `d1c4197` | tree (tree, 2) | **UNRESOLVED-SHORT** | — |
| 1495 | `d3a89d4` | tree (tree, 2) | **UNRESOLVED-SHORT** | — |
| 1495 | `f11f350` | commit (commit, 5) | **UNRESOLVED-SHORT** | — |

## 5. Summary

- **VERIFIED pairs:** MATCH × 79
- **Prior verified sentences:** MATCH × 25
- **Bare tokens:** COMMIT × 184, NEITHER × 106, TREE × 130, UNRESOLVED-SHORT × 76

### Not MATCH: none

Every joined claim matched the log; no discrepancy was found and none is manufactured.

- **Every VERIFIED pair verifies: YES** (79 of 79 joined MATCH).
- Every prior-verified sentence verifies: **YES** (25 of 25 joined MATCH).

Notes on the bare-token classes (a clean join, so these are provenance observations, not failures):

- The 106 NEITHER full-length identities are those the ledger itself attributes off this branch: the local/connector half of each "remote main `X`, local `Y`, shared tree `Z`" publication receipt (equal-tree connector publication; the local commit never enters the branch), cross-repository source pins (AHepi/h-EPI, AHepi/DeepReason, the personal-skill remote), and one earlier-workspace local commit on line 11. Each such row names its ledger line and role so a reader can check the attribution.
- Each of the 76 UNRESOLVED-SHORT ids prefixes at most one logged commit (the log has no short-id collisions), but none was joined or classified, per the no-promotion rule; the role column is only the nearest-keyword heuristic — e.g. the line-1495 enumeration mixes commit and tree short ids, all sitting nearest the word 'tree'.

## 6. Limits — what these patterns would not have caught

- The three patterns are exhaustive for their keywords in this ledger: every occurrence of the word VERIFIED and every "Prior verified commit/tree:" phrase was matched (verified computationally); no VERIFIED or prior-sentence identity was left unparsed.
- Bare-token sweep is confined to tokens within 40 characters of the words commit / tree / remote / published (case-insensitive, substrings allowed, nearest word wins). Identities elsewhere — the line-11 workspace id 4043a04d6092, all SHA-256 document/material hashes, plan ids, REC-2026091x receipt ids — are out of scope by the rule itself.
- 7-hex bare tokens are reported UNRESOLVED-SHORT and never joined: a short id may prefix both a commit and a tree. The log itself has no short-id collisions, so every short id appearing in the ledger is at most a unique text reference, which the role column records.
- NEITHER verdicts are identities this branch log does not contain. Contextually they are the local/connector-half commits of remote/local publication pairs, cross-repo source pins (AHepi/h-EPI commit b2a33283dc1e05fb83c3357b26e2cc12115f6b6c, AHepi/DeepReason commit 9607fba6f0a3066fbcab282c9ae0fad823e52e0c and its upstream root commit 377e5965ad20b22b07274655a9151d913d76db0a, the personal-skill remote 642dab8ff174f290a17871dff1133efab9707f41, and the line-11 earlier-workspace local commit 506b716bb7a2b4504e9e4f0ba54966587ac36465) — the ledger states equal-tree publication for remote/local pairs, but a commit identity that never entered this branch cannot be verified from this extract.
- Bare tokens occurring in more than one keyword context: 0592fe98ae01fe100c3ac9eb8e80b8c4e1c15468, 0ae29ee, 1e105b01d05e33e539d28e7e6ae307737cee6678, 274859008565ebc52f1ae44d48f94e4f96093538, 28ec4f4b2efa1dd8f1598247ffb3775c0c278534, 370276d892c00c13a5aa52ef56738ed6c075f695, 3c49718, 40bd5de738170ce84f1c483abe49f63ec774f07e, 656229c, 703556266704fdf4836e2ebd89c0fc70baf81972, 7749431ee6d27fab6db3d84c90d1f8dceda93d2c, 90d55fb, 9607fba6f0a3066fbcab282c9ae0fad823e52e0c, 96ca2eb, 9c876cc21686bd0e309449a4ca7dcbd9b737539c, ad3e347, b4c0ae2a8e87e57fdbf2b3b06651d4110de8ebdd, bfc5c8e, c2b92e1eef04cf4aa3c90ad36769718ed705b53b, c4efc7765d05e8999e06322289e068d8198722bd, d534d4f0b573a46eecbfd420b187badfd857c961.
- Every 40-hex bare token carries exactly one membership verdict per log regardless of role; the multi-context list above is presentation-only.
- Credential-pattern guard: no line matched; nothing withheld.
