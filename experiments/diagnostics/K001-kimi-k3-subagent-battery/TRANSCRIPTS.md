# Transcript index — K001 Kimi K3 subagent battery

Read at **2026-09-14T16:33:32+00:00**. Every size, line count and digest below is of the file as it stood at
that instant; see the note on the one transcript that was still being written.

Every call the harness made is recorded in a per-run `transcript.jsonl`: the full message text
of every turn (system prompt, task prompt, assistant turns, tool calls, tool results, final
answer), redacted by `Redactor.scrub`, together with per-turn usage, latency, request and
response digests, and the reasoning **digest** — `reasoning_content_sha256`,
`reasoning_content_chars`, `reasoning_tokens_estimated` and a constant
`reasoning_content_persisted: false`. The reasoning **text** is never written down.

## The transcripts are not published in this repository

They remain in the session scratchpad, at
`<scratchpad>/kimi/<run set>/<task>/transcript.jsonl`, which is ephemeral: when the session
ends they are gone. They are omitted for **size**, not for content. The eighty-one files total
**465,537,533 bytes (444.0 MB)** — larger than this entire repository working tree, which was
249 MB with this checkpoint already staged into it. This index
records each one's path, byte size, line count and sha256, so a transcript recovered from any
other copy can be proved to be the one the judgements read, and so their absence is a stated
gap rather than a silent one.

The publishing instruction admitted the transcripts of the judged battery runs — `runs/`,
`runs-pass2/`, `runs-pass3/`, `runs-pass4/`, `runs-pass4-retry/` — if those alone came in under
80 MB. They are 64 files totalling **257,938,091 bytes (246.0 MB)**, more than three
times the allowance, so **no transcript is published** and this index is the whole of the
transcript record here.

What *is* published beside each run: its `result.json` — status, mode, per-tool counts, token
totals, wall seconds, finish reason, harness failure and detail, and the sha256 and byte size
of every file the worker wrote — and the worker's own output directories. Figures the report
and the judgements take from transcripts (turn-level `finish_reason`, per-turn completion
tokens, reasoning characters) are quotable from this checkpoint only as those documents quote
them, each naming the file it computed the figure in.

## One transcript was still being written

A wave-3 production battery (`prod-tasks/tasks-w3.json`, three workers) was still running while
this index was read. The publishing instruction admits a `prod-runs-w3/` run only if its
`result.json` exists **at the moment the publisher looks**; the look was made at
**2026-09-14T16:33:03+00:00**, when `w3-trial` and `w3-report` had finished and were staged and
`w3-audits` had not. An unfinished run therefore has no record in this checkpoint; its
transcript appears below only for completeness, and its size and digest are those of a
**partial file at the instant named at the top**, not of a finished transcript:
`prod-runs-w3/w3-audits` — 48,648,218 bytes, in flight.

`prod-runs-w3` also has no `SUMMARY.md` yet — `run_battery.py` writes it when the whole battery
finishes, and that battery had not. The wave-3 records that complete after this checkpoint
belong to the next one, not to a later edit of this one.

## Index

| run set | task | bytes | lines | sha256 | run record published |
|---|---|---:|---:|---|---|
| `runs` | `a-01-types` | 8,082,793 | 186 | `d4d4c5f179a40b73ce8a677543fc469bed97fc33fc54038254cd2fa7853ffcef` | yes |
| `runs` | `a-02-contracts` | 16,567,632 | 198 | `ab118fa4db6047aae43e1d4617b8d2e104adbb22b1fb8cd6c7d8bed2780280b1` | yes |
| `runs` | `a-03-standard` | 13,104,670 | 184 | `a08cd6c7529e975a686dc2a7a64b7a6a3c210081e63006dfcb51833f2b9e073b` | yes |
| `runs` | `a-04-custody` | 11,226,633 | 214 | `00f52cc6f8505b18d27f7b1814b3ee2e34684e911f2df274ddea48b0972ed05b` | yes |
| `runs` | `a-05-receipts` | 1,214,244 | 42 | `6f35e22f7542985c20c61998b39fbb649e39ae2d18b4a9d59fa9c647c54e8dc3` | yes |
| `runs` | `a-06-publish` | 700,506 | 26 | `dfd4143e6f6cae8af8d9904a1fa8bdff4ece6785ab044f97a3dd5294cf6194b3` | yes |
| `runs` | `b-004` | 25,722 | 4 | `832ab4c71e85fc188fb0a2a84e2e7b56c0f89a9658a862eb144d8e94c79fa2aa` | yes |
| `runs` | `b-01-surface` | 3,118,490 | 58 | `d03f42ba0dcf6412fcb240b452aa0308b6faf9d8fe721c17a7e1a422c93b669a` | yes |
| `runs` | `b-02-seats` | 10,964,648 | 186 | `fdd232c8d881549345c875e3596a8d41bcb24843ebc1a380a763c406ca2d080a` | yes |
| `runs` | `b-03-obligations` | 958,873 | 34 | `ea6158534ba1b44fd19a3d35a7b3b6912d26c8f6da5d98fca1de251fc9f2e8c8` | yes |
| `runs` | `b-04-steps` | 1,445,870 | 42 | `8f59beb6f01fcedbb240da2fd09c2e8d06070d0ff6e11afda5bfcebcd4767848` | yes |
| `runs` | `c-01-packs` | 4,778,802 | 82 | `d03533be121d14831ce41d61b4a48dc9ae8e449ac6d913862c508b00a47bd233` | yes |
| `runs` | `c-02-roles` | 4,772,604 | 90 | `cb2068797a7d83a0e15c7f48b8761a8f24478a885cbe7ffe3b6a3ffaf5b55043` | yes |
| `runs` | `c-03-markprep` | 1,808,297 | 58 | `f2c24234806e67edf66c0d5df2a54513d55f8960a4241963e329c43c51a4501d` | yes |
| `runs` | `c-04-decide` | 2,856,703 | 62 | `f617f8bee20f92f1fe456799b32777ceb8bb42f703c629f829e4fbe9a8a9ccc1` | yes |
| `runs` | `d-01-receipt` | 283,852 | 26 | `624d11451e15ea3f4c5ed9fb1be3acca73ce1c03ff4240aa1735a19a6b3c3e22` | yes |
| `runs` | `d-02-operator-page` | 3,468,283 | 74 | `b327f0c8b9e339e006ba7dcccd84cff742e106d17efb81c468f900cd148e40a3` | yes |
| `runs` | `d-03-decision-record` | 454,387 | 36 | `46dbc709e72a00e66dddbd9c79e4525c0c76edd2fccb66bf7dad21ac7769a04d` | yes |
| `runs` | `d-04-f002-outcome` | 640,903 | 48 | `84ccc7f1c46a3f7d1c19a1171eff6273c08e27bca8acf28f14011b43c23cd173` | yes |
| `runs` | `e-01-refute` | 3,053,410 | 146 | `76a6e45dfaa73437a8f5518bdad515695c2b4de55ece9eb37f0af96be93ce26b` | yes |
| `runs` | `e-02-metric-creep` | 483,253 | 32 | `275be9ebca8de78932665bdbf94dd4a3de99c68570b7e777a82ca51ba6bfb2bf` | yes |
| `runs` | `e-03-fw5-citations` | 4,487,401 | 94 | `7310a696db31290be229925081dcf517175db170f42bbb94c80f7fded238349f` | yes |
| `runs` | `e-04-f001-classes` | 5,211,159 | 110 | `a7b6c972064da4aa0be9eb34b1d8517389488054a6eaa680d519f490e2b98c6a` | yes |
| `runs` | `f-01-c001-profile` | 3,432,385 | 124 | `3d3655157310a1081a8f3df3fea428b577ee6f0ffd5533410b6ff17219805ea4` | yes |
| `runs` | `f-02-commit-tree` | 6,781,828 | 130 | `27d8b1d11aa46bf265f45289a52a92fc81d7ccdc36780a22a27a281bd9429f6b` | yes |
| `runs` | `f-03-occ02-usage` | 1,200,167 | 78 | `012d7827d0f19fd1b90c951e60eada3a17558d152f435eed00bf305bb0b1a928` | yes |
| `runs` | `smoke-001` | 56,764 | 30 | `6578d5b6898c778f85c638d8008f477d510cbb205cfae871bca503deb94e69cd` | yes |
| `runs-pass2` | `a-01-types` | 2,222,628 | 92 | `e6baa67efdbde91049cde18d00901ef52af488f3d1362dd1443dbde8e082ecd1` | yes |
| `runs-pass2` | `a-02-contracts` | 22,753,200 | 250 | `a74188bd6e8eacdf84c18d003a3e6b3c40999527fbb4c54999490a0222755505` | yes |
| `runs-pass2` | `a-03-standard` | 768,300 | 30 | `a1246ec56b9d528ca7f11ceb14d1a1fe748b98c6b80aeba6cfe1933bcb15a3ad` | yes |
| `runs-pass2` | `a-05-receipts` | 259,312 | 16 | `95ac152b9e8b35449d04b04f2435bf0aae5c3ddb9ce09d29c02bd9565819f26b` | yes |
| `runs-pass2` | `a-06-publish` | 799,820 | 34 | `c315671d8b1e59cab3c4b2eb16af7a3021b492d09b9814059b44848ee59a1143` | yes |
| `runs-pass2` | `b-004` | 55,175 | 8 | `51512adb3e0940383cf5b0720ac8d93eb36f8af5767897847964ee83c3764282` | yes |
| `runs-pass2` | `b-01-surface` | 3,992,043 | 62 | `d4a3a9c18193b553009bee4a5c4236b37efac19f2235ef6265ce8dc02a4be7fc` | yes |
| `runs-pass2` | `b-02-seats` | 880,191 | 40 | `6da4f28e02e0fc8d6dedbb0f7176698fd470128e7bc2de145402f8b8790d13a8` | yes |
| `runs-pass2` | `b-03-obligations` | 2,141,011 | 62 | `8b648110a52143dc715262bb557e472cc9297e89a2826c5773c3169cb2b3b229` | yes |
| `runs-pass2` | `b-04-steps` | 3,830,808 | 70 | `52f81d95ffa26f13dcd37cc141dca7151835361085c6f406c6526c8e8c66e30b` | yes |
| `runs-pass2` | `c-01-packs` | 6,060,471 | 102 | `a34ed145635e58f7129595b8b1c16b8a4e3313967e00cf588dbd88f92fd6acbf` | yes |
| `runs-pass2` | `c-02-roles` | 4,044,056 | 82 | `925fbe54eddaf477fb29fe8f58fc67346767b80458d1dba5f646c8a1ec7d03a9` | yes |
| `runs-pass2` | `c-03-markprep` | 1,665,678 | 52 | `ed0f62e67c8087b9eede95574bf55cd813b38b826cae22bfb9ae15f2ee091b11` | yes |
| `runs-pass2` | `c-04-decide` | 5,801,629 | 90 | `df5f97d28aab4aa29a5de75fbb8dbd86435a377de930299cdc2ddf6762f50015` | yes |
| `runs-pass2` | `d-01-receipt` | 327,112 | 28 | `3d8efbe746af553a43bf330ea055a638b3781050f47476a469615b6d2dd9107c` | yes |
| `runs-pass2` | `e-02-metric-creep` | 415,453 | 22 | `8c898f486e4c8ca8660a9d070f9664de93f6d9fa89ea0c665d52282bde5edfcd` | yes |
| `runs-pass2` | `f-02-commit-tree` | 445,470 | 36 | `5f269988874508be1bc588354537132a024945d68c3ee09a14c981a48def7ad6` | yes |
| `runs-pass3` | `a-06-publish` | 1,595,811 | 52 | `bca26dcedb0d90147d13f3e9fc0fa6a1a46226c750ceffac2af4f51e014bcc02` | yes |
| `runs-pass3` | `b-04-steps` | 1,402,848 | 40 | `d75ef302118ef2ff07cc110b620824c67b06dd00b00ae190296c6705f73b88b7` | yes |
| `runs-pass3` | `c-01-packs` | 4,811,647 | 76 | `2a0a647c51d3682cb355b92b7c902419e2e3dd8609d2d22f4f7f06ce1da4d3b6` | yes |
| `runs-pass3` | `d-01-receipt` | 166,040 | 20 | `1cd5ed4bc471a0f2f64aad94bdededaa35164c627cfb3eedcbd421ced5abcecb` | yes |
| `runs-pass4` | `a-01-types` | 4,249,736 | 122 | `87aeb07ed3904ab0475edfe6ef016a6a7214713af17374bcd399d6fccf56988d` | yes |
| `runs-pass4` | `a-03-standard` | 4,574,846 | 114 | `071567caa8a2cc456d1891ee09403987be285058b047e8ed9cfab6bda03c7d41` | yes |
| `runs-pass4` | `a-05-receipts` | 3,261,399 | 94 | `f0795ab670f6bd89405a60def5541e9c4102e1598eed6e11481c4feb77fbd60a` | yes |
| `runs-pass4` | `a-06-publish` | 7,811,963 | 208 | `15b6c04cf299066eea13027c283a5c66388c3b3499d13ddff3c625643d978871` | yes |
| `runs-pass4` | `b-01-surface` | 2,907,226 | 80 | `a0ad37008bc8f1653fda591b32c17bd35fac01c18413cebc586cfaa896d4e607` | yes |
| `runs-pass4` | `b-02-seats` | 6,072 | 3 | `5bffbf049bfa198181411105c2e5a1b79c35ad667929a2e292ad48e5c92a05e8` | yes |
| `runs-pass4` | `b-02-seats-fixed` | 2,723,206 | 64 | `e88c1ab538c8493a88bb1106050365b4064da22420c064f073ee66c71c0ff689` | yes |
| `runs-pass4` | `b-03-obligations` | 2,540,228 | 60 | `6e5077719e2a18d6c91e1224f259f83ef453dedac42ec2ce0ca233f89de027ca` | yes |
| `runs-pass4` | `b-04-steps` | 4,577,173 | 74 | `169b54b4d56d59012342cbbc33038afad6be648f80a2670cb12495e8b2fa6803` | yes |
| `runs-pass4` | `c-01-packs` | 13,181,631 | 150 | `9a8c7e69e380da397438171397b954c5700abee9c6ccbcf68fb768419040c487` | yes |
| `runs-pass4` | `c-02-roles` | 8,399,802 | 112 | `7251fc5a99c5e7ddcc23bcce39163d768edf906b69b7780bed5948944ffd3e8a` | yes |
| `runs-pass4` | `c-03-markprep` | 1,385,879 | 50 | `424dadf84f8b363d4ff8ec3dd9e9737f09d91109957551ad235ac53074ab5a2d` | yes |
| `runs-pass4` | `c-04-decide` | 11,384,769 | 108 | `5936a67e1a312f2ae8ad453c457859053bbf3b21906d43119c4a132b9a3a72fd` | yes |
| `runs-pass4` | `d-01-receipt` | 1,052,517 | 48 | `be4720a7fdb54e4e2197503ffc56de2817ce0c2e8a865872c1bb1a81965ecc4c` | yes |
| `runs-pass4` | `e-02-metric-creep` | 2,011,442 | 60 | `9072730a87d4fc7161826290828c9693b5ab1b7763bc218a26d2b859296d0223` | yes |
| `runs-pass4-retry` | `c-03-markprep` | 12,251,220 | 144 | `efa8a730c000cb941f856813435923ca6937df4c02ac97c59fddc93212cccab5` | yes |
| `prod-runs` | `p1-a001v3-citations` | 8,353,487 | 166 | `9d84276e21404a1a4c2b7518fcc34598a50bea8c100abd774e4b712c7cb061d3` | yes |
| `prod-runs` | `p1-a001v3-citations.attempt1-context-missing` | 4,346 | 3 | `0748610119037c0a13de6eebb23967d7d87a35dc545e8fb4ff874bb9c1e64c40` | yes |
| `prod-runs` | `p1-ledger-audit` | 3,223,646 | 88 | `476bcc5fd08db513ecfe19c8bc81b8a7f5dbc4eed9ea1187f1dd7387b8fa3fd6` | yes |
| `prod-runs` | `p1-ledger-verified-join` | 12,184,323 | 130 | `828ac444c48f0a536e4e5db80d400dbdb8dc8113e61f3f8b8197bec7a349b66d` | yes |
| `prod-runs` | `p2-activity-log-audit` | 4,287,466 | 66 | `712467f4c45a94dcc162988693fbae7475af288ab41cbdf8f219b56ce225c72f` | yes |
| `prod-runs` | `p2-prereg-mechanical` | 7,713,028 | 178 | `2bb9dccf3b5d033e51bf5de590ad4cac04f06653f5c9d52d23615e4a54f258cf` | yes |
| `prod-runs` | `p3-a001v4-citations` | 8,081,852 | 164 | `ae75161cc8fe2c091b65bf88444aec9f85f81277a123525aa06b6e321a714727` | yes |
| `prod-runs` | `p3-manifest-reverify` | 5,258,839 | 184 | `eea842bc864141a423f7cb28d29e1df0edff40ae7811a7f45b3397ab6f1d8a14` | yes |
| `prod-runs` | `p4-a001v4-citations-native` | 2,048,078 | 56 | `930be9ea4a8a9dd3c63325a2e5bbef9c0dbf4c042f6dd445d7919e5be89df0c0` | yes |
| `prod-runs` | `p4-checkpoint-scan` | 583,470 | 76 | `7261d4e9aaefbbea640131e63dd12f86c2fdbaeb986bc37a92822f982b1e6b76` | yes |
| `prod-runs` | `p5-a001v4-citations-refine` | 1,215,279 | 100 | `eac29f6ba8fb90a487d04db5909d7848e4831a47958e724980a3ed5e72bc947b` | yes |
| `prod-runs` | `p5-manifest-reverify-full` | 4,473,918 | 120 | `96d4b52f7408e55440a8623b187b6aa24a3897779252c838750a2c5fd11a3625` | yes |
| `prod-runs` | `p6-manifest-reverify-f001` | 15,882,138 | 190 | `74f508c46e2b8b3210ef0be4d64d7d405c9353a002dbbb2bad97857418ed7bef` | yes |
| `prod-runs-smoke` | `smoke-native-001` | 23,392 | 16 | `20ba90694ecf0542ecc77bf53d1321ff5929e162ddeb6713afc38ab29aa1500c` | yes |
| `prod-runs-w3` | `w3-audits` | 48,648,218 | 264 | `4b2cc01f4961b0db3d43dd5794a803d56300e8adb91166de44ee6b7cfb76daf5` | no — in flight |
| `prod-runs-w3` | `w3-report` | 62,655,674 | 372 | `62d08b33b3ced61fa25c105359fc27c0cc4004515cc1ed259a5b0d82fbefea57` | yes |
| `prod-runs-w3` | `w3-trial` | 22,962,288 | 146 | `efd1fe9a3d9c429d65136ac807c51984bbb98e343fcc27e75b03410790b5356a` | yes |
| **total** | **81 transcripts** | **465,537,533** | | | |

Line counts are `\n` counts; every transcript is newline-terminated JSON Lines, one event per
line. The judged-battery subtotal above covers the first five run sets, 64 of these 81 files.

