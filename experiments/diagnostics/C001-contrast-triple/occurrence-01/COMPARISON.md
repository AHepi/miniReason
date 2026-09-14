# C001 comparison: successor commitment surfaces across four cases

plan_id: `328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8`

**Question.** At one responder node - the fork5 `response` node, instruction and non-objection inputs frozen from the H005 material and occurrence-01 - does the successor's authored commitment surface differ against a no-objection control, and NOT under a content-preserving recoding of the objection, and NOT under a carrier disturbance at fixed content? (FW5:630 contrast contract, redirected from the judge to the responder.)

**Claim ceiling.** One system, one problem, one respect. Consistent-with, never a reason-use witness (FW5:628). An unresolved cell stays unresolved (FW5:634).

**Unresolved cells.** A PARTIAL delivery (finish_reason "length" at the endpoint's own declared max_tokens ceiling - 8192 for deepseek-flash, 32768 for the five Ollama endpoints) yields a truncated commitment surface. Such a cell is marked unresolved in the evidence table and is not compared against any other case (FW5:634; EXPERIMENT_METHOD operational-failure table). A delivery that returns no content at all because the ceiling went entirely to reasoning is a refusal (INCOMPLETE_GENERATION), recorded with its failure code and likewise compared against nothing. Raising the Ollama ceiling makes those outcomes less likely; it does not change how they are read.

**How to read this.** "differs against control, not under recoding, not under carrier disturbance" is a pattern root reads off these surfaces. It is never computed here and never expressed as a quantity (FW5:628, :630, :851).

Every `root_*` cell below is deliberately empty. Root fills it by reading the raw juxtaposition; nothing in this file computes it.

## What "differs" means, pre-declared

Root reads every cross-case comparison on exactly the four registers below and records for each one of `differs` / `same` / `unresolved`. The four marks are reported separately and stand or fall separately; they are never summed, averaged, weighted or reduced to one mark.

| register | reads | `differs` iff |
|---|---|---|
| `T` target named | The represented target of the successor's own engagement. FCL arm: the set of values in `target` arrays, read with the source artifact prefix intact (a reference into the account is not a reference into the objection). Prose arm: the phrase by which the successor says what it is responding to. | the two sets of distinct targets are not the same set |
| `E` objection record engaged, prefix-resolved | Which of the objection document's records (o1 o2 o3 c1 c2 o4 p1 u1) the successor takes up, by prefix-qualified reference or by quotation of that record's own text. The prefix is resolved against the declared artifact addresses (arms.<arm>.artifact_addresses). | the sets of prefix-resolved objection records engaged are not the same set. A bare id token shared with the account document (o1 c1 c2 p1 u1) is `unresolved` for this register and never `differs`. |
| `D` proposed action (disposition) | What the successor proposes to do about the criticism: use, leave open, revise, reject or withdraw. FCL arm: read off record `type`, `uptake`, `revises`, `withdraws` and the `action` field. Prose arm: read off the text. | the disposition attached to the same criticism changes |
| `G` grounds cited | Whether the successor grounds that disposition in the objection's grounds, the account's, the rival's, or none. | the cited source of grounds is not the same |

**The replicate baseline.** A register is marked `differs` for a case pair only if the difference root reads between the two cases is one root does NOT also read between at least one pair of replicates inside ORIGINAL. Where the same kind of difference already appears inside ORIGINAL's own five replicates, the register is `same` for that pair and the fact is recorded.

**Order of reading.** Root reads the five ORIGINAL replicates and writes the within-ORIGINAL spread on all four registers into COMPARISON.md BEFORE opening any other case’s juxtaposition for that cell. The baseline note is written first and is not revised afterwards.

**Two readers.** The registers are written so that two readers of the same juxtaposition mark the same cells. Where two readers disagree on a register, that register is `unresolved` for that cell and the disagreement is recorded, never averaged (FW5:634).

**Never aggregated.** No mark is a quantity. The four registers are never summed, averaged, weighted, ranked or reduced to a single mark (FW5:851; PURPOSE.md, "no scalar progress meter").

## deepseek-flash / fcl

| case | rep | delivery | envelope | repairs | strict parse | comparable | fcl parse | records | by type | record ids | targets named | objection ids in refs (prefix-resolved) | account-prefixed refs | rival-prefixed refs | refs with an unrecognised prefix | bare id refs (unresolved) | uptake | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| original | 2 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| original | 3 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| original | 4 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| original | 5 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| recoding | 1 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| recoding | 2 | PARTIAL | OPAQUE | (none) | no | no | unresolved |  |  |  |  |  |  |  |  |  |  | 4269b02011ccc54d | e3b0c44298fc1c14 | 10477 | 0 |
| recoding | 3 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| recoding | 4 | PARTIAL | OPAQUE | (none) | no | no | unresolved |  |  |  |  |  |  |  |  |  |  | 170df492946f7a3f | e3b0c44298fc1c14 | 6626 | 0 |
| recoding | 5 | PARTIAL | OPAQUE | (none) | no | no | unresolved |  |  |  |  |  |  |  |  |  |  | f228a7f04687475e | e3b0c44298fc1c14 | 4086 | 0 |
| carrier | 1 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 10 | claim=4, commitment=2, objection=2, problem=1, use=1 | c1, c2, c3, c4, o1, o2, p1, u1, k1, k2 | a6a817c0#r6, c3, u1 | (none) | (none) | (none) | 406eff78#c2, 406eff78#o2, a6a817c0#r3, a6a817c0#r6, a6a817c0#r7, a6a817c0#r9 | c1, c2, u1 | c1, c2, c3, u1, k1, k2, o2, o1, p1 | e6aa2b4a395770f8 | 6cda20f77a6e8c0e | 5827 | 5292 |
| carrier | 2 | PARTIAL | OPAQUE | (none) | no | no | unresolved |  |  |  |  |  |  |  |  |  |  | d8601d72c5cf67d6 | e3b0c44298fc1c14 | 8774 | 0 |
| carrier | 3 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| carrier | 4 | PARTIAL | OPAQUE | (none) | no | no | unresolved |  |  |  |  |  |  |  |  |  |  | 54f7f596cb908561 | e3b0c44298fc1c14 | 4659 | 0 |
| carrier | 5 | PARTIAL | OPAQUE | (none) | no | no | unresolved |  |  |  |  |  |  |  |  |  |  | 8f28703237e73f80 | e3b0c44298fc1c14 | 6937 | 0 |
| control | 1 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| control | 2 | PARTIAL | OPAQUE | (none) | no | no | unresolved |  |  |  |  |  |  |  |  |  |  | e035e1a3782edb6f | e3b0c44298fc1c14 | 3144 | 0 |
| control | 3 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| control | 4 | FAILED (NO_PUBLIC_CONTENT) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| control | 5 | PARTIAL | OPAQUE | (none) | no | no | unresolved |  |  |  |  |  |  |  |  |  |  | a62f13b9222a561f | e3b0c44298fc1c14 | 1546 | 0 |

**Unresolved in this cell:** original/rep1, original/rep2, original/rep3, original/rep4, original/rep5, recoding/rep1, recoding/rep2, recoding/rep3, recoding/rep4, recoding/rep5, carrier/rep2, carrier/rep3, carrier/rep4, carrier/rep5, control/rep1, control/rep2, control/rep3, control/rep4, control/rep5

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/deepseek-flash__fcl.md`

## deepseek-flash / prose

| case | rep | delivery | envelope | repairs | strict parse | comparable | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | (none) | yes | yes | ae809dc6ce06ae9a | 2146b30ccbbeaee8 | 4286 | 2483 |
| original | 2 | COMPLETE | AUTHORED | (none) | yes | yes | a9617de45f333ca4 | d6a6d5fbfad32817 | 3222 | 2353 |
| original | 3 | COMPLETE | AUTHORED | (none) | yes | yes | fef060f597173cf7 | 069070d22ffa566b | 3675 | 2453 |
| original | 4 | COMPLETE | AUTHORED | (none) | yes | yes | e0017debaeaee36e | 471ab982a238ac93 | 3371 | 2535 |
| original | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 22651262364cbe30 | 2e69919241e2f76d | 4655 | 1766 |
| recoding | 1 | COMPLETE | AUTHORED | (none) | yes | yes | 64cef1c6c9c64010 | f631e74cc400f729 | 5400 | 3099 |
| recoding | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 3da88b0fb806b4ef | a76d3c16092eb1e5 | 4401 | 2498 |
| recoding | 3 | COMPLETE | OPAQUE | (none) | no | yes | 3a3b4d30cdfced72 | e3b0c44298fc1c14 | 6321 | 0 |
| recoding | 4 | COMPLETE | AUTHORED | (none) | yes | yes | aa0be06ce3d6a67b | 4250fdd1e52f844a | 4078 | 2482 |
| recoding | 5 | COMPLETE | AUTHORED | (none) | yes | yes | d7a5596a33bf8b3a | e399edc1bd6556ed | 3518 | 2215 |
| carrier | 1 | COMPLETE | AUTHORED | (none) | yes | yes | 9666a7532f9052de | f26a4c173dddb7db | 4306 | 3331 |
| carrier | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 454c22d7c802a429 | d87dca149180117e | 3693 | 2483 |
| carrier | 3 | COMPLETE | AUTHORED | (none) | yes | yes | d581be461108c26c | a0c8c93a3d99931b | 4114 | 3232 |
| carrier | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 0cc9f6208d4d9207 | 7eb6bbbffda7fa72 | 3293 | 1716 |
| carrier | 5 | COMPLETE | AUTHORED | (none) | yes | yes | aa10ba5f1c3d7ea2 | 681e86eb6a2d6ca2 | 4943 | 3252 |
| control | 1 | COMPLETE | AUTHORED | (none) | yes | yes | be3d07b9c6a54157 | dace8d777a580d70 | 6203 | 3334 |
| control | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 3ae9403a873f307e | 014bc0d3d635e6f2 | 3850 | 2329 |
| control | 3 | COMPLETE | AUTHORED | (none) | yes | yes | e83471938e34477f | f1a9c88afdb1f33b | 4247 | 2671 |
| control | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 9ec630832c883ccd | 93ce9a5db48e65e6 | 4962 | 3134 |
| control | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 71d530e5f4aa2db5 | 9f7522d9fe10726b | 3068 | 2466 |

**Unresolved in this cell:** (none)

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/deepseek-flash__prose.md`

## ollama-gemma4-31b / fcl

| case | rep | delivery | envelope | repairs | strict parse | comparable | fcl parse | records | by type | record ids | targets named | objection ids in refs (prefix-resolved) | account-prefixed refs | rival-prefixed refs | refs with an unrecognised prefix | bare id refs (unresolved) | uptake | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 5 | claim=2, commitment=0, objection=0, problem=1, use=2 | c1, c2, u1, u2, p1 | (none) | (none) | (none) | (none) | p.objection.0#o1, p.rival.0#r3, p.rival.0#r7, p.rival.0#r8 | u1 | c1, c2, u1, u2 | bf28b558da3fc443 | 40d202bdff0f9a55 | 2701 | 1489 |
| original | 2 | COMPLETE | OPAQUE | strip_outer_code_fence | no | yes | FAILED |  |  |  |  |  |  |  |  |  |  | e9de734da5683810 | e3b0c44298fc1c14 | 4819 | 0 |
| original | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 6 | claim=2, commitment=0, objection=0, problem=1, use=3 | c1, c2, u1, u2, u3, p1 | (none) | (none) | (none) | (none) | p.objection.0#o1, p.rival.0#r2, p.rival.0#r9 | (none) | c1, c2, u1, u2, u3 | 44c87475c619c10e | 37719c3dcb1618de | 2638 | 1801 |
| original | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 6 | claim=2, commitment=0, objection=0, problem=1, use=3 | c1, c2, u1, u2, u3, p1 | (none) | (none) | (none) | (none) | p.objection.0#o1, p.rival.0#r11, p.rival.0#r2, p.rival.0#r3, p.rival.0#r6, p.rival.0#r7, p.rival.0#r8 | (none) | u1, u2, u3 | bfff2e6dee05384d | 4abaa4fd730bc672 | 3085 | 1790 |
| original | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 5 | claim=2, commitment=0, objection=0, problem=1, use=2 | c1, c2, u1, u2, p1 | (none) | (none) | (none) | (none) | (none) | u1 | c1, c2, u1, u2 | ab016590a4e9006d | 8069870efbee9e53 | 2929 | 1503 |
| recoding | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 6 | claim=2, commitment=0, objection=0, problem=1, use=3 | c1, c2, u1, u2, u3, p1 | (none) | (none) | (none) | (none) | (none) | c1 | c1, c2, u1, u2, u3, p1 | 482dff96d1bdaf71 | 568fff53443ce65f | 2687 | 1700 |
| recoding | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | FAILED |  |  |  |  |  |  |  |  |  |  | 3528071fbfd72dd9 | 1ebc41c7b88952f1 | 2151 | 1737 |
| recoding | 3 | COMPLETE | OPAQUE | strip_outer_code_fence | no | yes | FAILED |  |  |  |  |  |  |  |  |  |  | d9b0471be90cac8e | e3b0c44298fc1c14 | 4133 | 0 |
| recoding | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 5 | claim=2, commitment=1, objection=0, problem=0, use=2 | c1, c2, c3, c4, c5 | (none) | (none) | (none) | (none) | (none) | c1 |  | 1e182e4544a51e8c | f60402e90eba610d | 2873 | 1472 |
| recoding | 5 | COMPLETE | OPAQUE | strip_outer_code_fence | no | yes | FAILED |  |  |  |  |  |  |  |  |  |  | ad99668dd34ce5df | e3b0c44298fc1c14 | 3284 | 0 |
| carrier | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 4 | claim=1, commitment=1, objection=0, problem=1, use=1 | rec1, rec2, rec3, rec4 | (none) | (none) | (none) | (none) | (none) | (none) |  | fbb942acc841ab72 | fe2afd10c07d4b71 | 2719 | 1282 |
| carrier | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 7 | claim=2, commitment=1, objection=0, problem=1, use=3 | c1, c2, u1, u2, u3, p1, com1 | (none) | (none) | (none) | (none) | p.objection.0#c2, p.objection.0#o2, p.objection.0#p1, p.rival.0#r11, p.rival.0#r2, p.rival.0#r3, p.rival.0#r6, p.rival.0#r7, p.rival.0#r8 | (none) | c1, c2, u1, u2, u3, p1, com1 | 377b64792a8bfe80 | 971d7970a774429b | 2674 | 2116 |
| carrier | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 5 | claim=2, commitment=1, objection=0, problem=0, use=2 | rec1, rec2, rec3, rec4, rec5 | (none) | (none) | (none) | (none) | p.account.0#step-5, p.objection.0#p1, p.rival.0#r11, p.rival.0#r2, p.rival.0#r7, p.rival.0#r8 | (none) | rec1, rec2, rec3, rec4, rec5 | fc6addcb9c105f63 | e15e047c079d5053 | 2031 | 1821 |
| carrier | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 5 | claim=2, commitment=0, objection=0, problem=1, use=2 | c1, c2, u1, u2, p1 | (none) | (none) | (none) | (none) | p.objection.0#c1, p.rival.0#r4, p.rival.0#r7 | (none) |  | 333239e0e44cb91e | 1bec33e5208dac55 | 2479 | 1489 |
| carrier | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 3 | claim=2, commitment=0, objection=0, problem=0, use=1 | c1, c2, u1 | o2 | (none) | (none) | (none) | (none) | o2 |  | 220937c05e0e00c9 | 09d044b1c6112bc2 | 2303 | 974 |
| control | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | FAILED |  |  |  |  |  |  |  |  |  |  | 706fc31a94bc3160 | fd80b0857b206541 | 1829 | 1034 |
| control | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 4 | claim=1, commitment=2, objection=0, problem=1, use=0 | rec1, rec2, rec3, rec4 | (none) | (none) | (none) | (none) | (none) | c2 | rec1, rec2, rec3 | 99ef40bbf8a19979 | e9e26c293d26dbde | 1940 | 1291 |
| control | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 3 | claim=0, commitment=0, objection=1, problem=0, use=2 | u_final_1, u_final_2, r_final_1 | (none) | (none) | (none) | (none) | (none) | c2 | u_final_1, u_final_2 | 782c1e2ee05dbde6 | 3b91cf1f7c81b13c | 2231 | 915 |
| control | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 4 | claim=1, commitment=2, objection=0, problem=0, use=1 | c1, c2, c3, c4 | (none) | (none) | (none) | (none) | (none) | c2 | c1, c2, c3, c4 | ab456757ed3c1a00 | 23b989ce8cb48d63 | 2325 | 1332 |
| control | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 4 | claim=1, commitment=2, objection=0, problem=0, use=1 | s1, s2, s3, s4 | (none) | (none) | (none) | (none) | (none) | c1, c2 | s1, s2, s3, s4 | 3bdce60b7784c4ad | bf56bb3c4c908270 | 2275 | 1221 |

**Unresolved in this cell:** (none)

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/ollama-gemma4-31b__fcl.md`

## ollama-gemma4-31b / prose

| case | rep | delivery | envelope | repairs | strict parse | comparable | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 2bc7265a61c408b3 | 85ff0e8f2bb74af5 | 2168 | 1499 |
| original | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | e76f917d3c6bbb5b | 08d1b1a44ba3c9ba | 2194 | 1598 |
| original | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 0aeab96caf498b02 | 5282dfcdda122896 | 2254 | 1296 |
| original | 4 | COMPLETE | OPAQUE | strip_outer_code_fence | no | yes | b8bface6caeb8a21 | e3b0c44298fc1c14 | 3512 | 0 |
| original | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 10ca1bbbdb5520c9 | 3ea5f849cfbc0f35 | 2200 | 1378 |
| recoding | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | e4e402e79a57308c | 753a299b90bb2253 | 2101 | 1454 |
| recoding | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 823c89b05adf31e0 | 138eb0fd5c566c4d | 2270 | 1433 |
| recoding | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | b9d104a7738ffaaa | bf3876230ddc6223 | 2339 | 1441 |
| recoding | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 894b1aeb7d734fef | 1f3df600c637b7f0 | 2305 | 1497 |
| recoding | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | bae84d1eeb5f1ad7 | d501aa8a4735ddfd | 1651 | 1101 |
| carrier | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 658031b087d05c86 | 3f760aabed8e01a4 | 2104 | 1305 |
| carrier | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 025cfba90828073d | c040308c21142d52 | 2415 | 1266 |
| carrier | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 1ad1140ff9e54cc9 | 3a6587029b1e3c82 | 2059 | 1267 |
| carrier | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | d897b286332c4f7c | d733d5023d83e124 | 1980 | 1413 |
| carrier | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | be9f402724970df3 | 4e2e98bcf7d7f1ef | 2149 | 1438 |
| control | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 1a96c7c57515c52a | 325f9aa46233ffc1 | 2098 | 1272 |
| control | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | de8a018235ff3df4 | 05b51809afcca5d6 | 1839 | 1240 |
| control | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 7b11bdb975307fd1 | 021a52040b7654f2 | 2136 | 1259 |
| control | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | efb6a98e13d4c8f3 | 15c844a0f5ad0724 | 2138 | 1506 |
| control | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 22fc0b8cc6c5e10f | 05d04a70c026d8bc | 2005 | 1235 |

**Unresolved in this cell:** (none)

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/ollama-gemma4-31b__prose.md`

## ollama-glm-5.3 / fcl

| case | rep | delivery | envelope | repairs | strict parse | comparable | fcl parse | records | by type | record ids | targets named | objection ids in refs (prefix-resolved) | account-prefixed refs | rival-prefixed refs | refs with an unrecognised prefix | bare id refs (unresolved) | uptake | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 12 | claim=3, commitment=1, objection=2, problem=1, use=5 | k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12 | account#c2, account#c3, objection#c1, objection#o1, objection#o2, objection#o3, objection#p1, objection#u1, rival#r6, rival#r7 | c1, o1, o2, o3, o4, p1, u1 | c2, c3 | r10, r11, r2, r3, r6, r7, r9 | (none) | (none) | k1, k2, k3, k4, k5, k6, k7, k8, k9, k11, k12 | e857d4a330f08c64 | 9576ce92da5a7e21 | 7243 | 8160 |
| original | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 12 | claim=5, commitment=1, objection=3, problem=2, use=1 | c1, c2, o1, c3, o2, o3, c4, c5, u1, k1, p1, p2 | (none) | (none) | (none) | (none) | (none) | u1 | u1, c3, c4, c5, k1 | efff273da09aaf70 | 113852ef0d36c015 | 5402 | 5454 |
| original | 3 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 16 | claim=4, commitment=3, objection=3, problem=2, use=4 | c1, c2, c3, c4, o1, o2, o3, u1, u2, u3, u4, m1, m2, m3, p1, p2 | c2, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#o1, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/objection#u1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r2, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | c1, c2, o3 | c1, c2, c3, c4, o1, o2, o3, u1, u2, u3, u4, m1, m2, m3, p1, p2 | 3ee0df7a4c35dddd | d127837822eb6acc | 5555 | 8976 |
| original | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 14 | claim=7, commitment=1, objection=3, problem=1, use=2 | c1, c2, c3, c4, c5, c6, c7, c8, o1, o2, o3, p1, u1, u2 | account#c1, account#c2, c3, objection#o1, objection#o2, objection#o3, rival#r10, rival#r11, rival#r2, rival#r3, rival#r6, rival#r7, rival#r8, rival#r9 | c1, o1, o2, o3, p1, u1 | c1, c2 | r10, r11, r2, r3, r4, r6, r7, r8, r9 | (none) | c1, c2, o2, o3 | c1, c2, c3, c4, c5, c6, c7, c8, o1, o2, o3, p1, u1, u2 | ac4f0181ad9a9735 | b910d980f57040a7 | 7110 | 7523 |
| original | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 17 | claim=5, commitment=3, objection=3, problem=3, use=3 | c1, c2, c3, c4, c5, c6, o1, o2, u1, u2, u3, rev1, rev2, rev3, p1, p2, p3 | account#c2, c3 | c2, o2, o3, p1, u1 | c2, c3 | r10, r11, r2, r3, r6, r7, r8, r9 | (none) | c1, c2, o1, o2, u1 | c1, c2, c3, c5, c6, o1, o2, u1, u2, u3, rev1, rev2, rev3, p2, p3 | f1af2bdf9a97658d | 3c639cf181c0b7c3 | 5571 | 7428 |
| recoding | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 12 | claim=4, commitment=1, objection=2, problem=1, use=4 | k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12 | (none) | (none) | (none) | (none) | (none) | (none) | k1, k4, k5, k6, k8, k9, k10, k11, k12 | 4835db08d6cc0acc | a8f9836d5be61881 | 6246 | 7479 |
| recoding | 2 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 20 | claim=7, commitment=3, objection=4, problem=2, use=4 | c1, c2, c3, c4, c5, c6, c7, o1, o2, o3, o4, u1, u2, u3, u4, k1, k2, k3, p1, p2 | c4, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r6 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#o1, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/account#u1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | c1, o1, o4 | c1, c2, c3, c4, c5, c6, c7, o1, o2, o3, o4, u1, u2, u3, u4, k1, k2, k3, p1, p2 | 40e5cec993ff9737 | d40a65ff9271d57b | 7273 | 10972 |
| recoding | 3 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 13 | claim=5, commitment=1, objection=3, problem=1, use=3 | m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13 | m1, m2, m3, rival#r6, rival#r8 | o1, o2, o3, p1, u1 | c1, c2, c3 | r10, r11, r5, r6, r7, r8, r9 | (none) | (none) | m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13 | 66208e714ee03938 | 1597da088e1ba66c | 6822 | 7739 |
| recoding | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 18 | claim=6, commitment=5, objection=4, problem=2, use=1 | c1, c2, c3, c4, c5, c6, o1, o2, o3, o4, k1, k2, k3, k4, k5, p1, p2, u1 | account#c2, objection#o2, objection#o3, rival#r6, rival#r7 | c1, o1, o2, o3, p1, u1 | c2, c3, p1 | r10, r11, r3, r5, r6, r7, r8, r9 | (none) | c1 | c1, c3, c4, c5, c6, o1, o2, o3, o4, k1, k2, k3, k4, k5, p1, p2, u1 | 1a55a27ed8804184 | 4bd7b1f61eac812e | 5848 | 7767 |
| recoding | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 13 | claim=4, commitment=2, objection=1, problem=2, use=4 | c1, c2, c3, c4, o1, u1, u2, u3, u4, k1, k2, p1, p2 | daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r6 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#o1, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r2, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r9 | (none) | c1, c2, c3, c4, o1, u1, u2, u3, u4, k1, k2 | 8f9eb3f9a803e700 | c4a625dd03095836 | 5794 | 7231 |
| carrier | 1 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 11 | claim=5, commitment=2, objection=2, problem=1, use=1 | d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11 | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/objection#c2, daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#c2, daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11 | 2b04421d0c51d293 | e56e1666f99ce7c9 | 7370 | 7481 |
| carrier | 2 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 15 | claim=5, commitment=3, objection=2, problem=3, use=2 | k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15 | account#c2, objection#o4, objection#u1, rival#r7, rival#r8 | c1, o1, o2, o4, p1, u1 | c1, c2, c3 | r10, r11, r2, r6, r7, r8, r9 | (none) | (none) | k1, k3, k4, k5, k6, k7, k12, k13, k14 | 45aae01fc2dd17f0 | 01f89aa7cebc3b08 | 5621 | 7915 |
| carrier | 3 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 16 | claim=7, commitment=1, objection=2, problem=2, use=4 | k1, k2, k3, k4, k5, k6, k7, m1, m2, u1, u2, u3, u4, cm1, p1, p2 | daily/mini_fcl/cycle-1/rival#r2, daily/mini_fcl/cycle-1/rival#r6, k3 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c1, daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#o4, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/objection#u1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r2, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | k1, k2, k3, k4, k5, k6, k7, m1, m2, u1, u2, u3, u4, cm1, p1, p2 | 971241bcaa020687 | dbbfd2699b2bdee3 | 5717 | 10221 |
| carrier | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 14 | claim=5, commitment=3, objection=2, problem=1, use=3 | k1, k14, k4, k7, k2, k3, k5, k6, k13, k8, k10, k9, k11, k12 | k6, objection#o1, rival#r6 | c1, c2, o1, o2, p1 | c1, c2, c3 | r10, r11, r2, r3, r4, r6, r7, r8 | (none) | (none) | k1, k14, k4, k7, k2, k3, k5, k6, k8, k9, k10, k11, k13 | 59e09477d48727af | 4fdbc316d0c46cab | 5893 | 7995 |
| carrier | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 11 | claim=3, commitment=2, objection=2, problem=2, use=2 | k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11 | account#c2, rival#r6, rival#r8, rival#r9 | o1, o2, o4, p1 | c1, c2, c3, p1 | r10, r11, r2, r3, r4, r5, r6, r7, r8, r9 | (none) | (none) | k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11 | 943b20387c034447 | bcdb6b4ca1f463ae | 8031 | 7010 |
| control | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 16 | claim=4, commitment=2, objection=4, problem=3, use=3 | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16 | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#u1, daily/mini_fcl/cycle-1/rival#r4, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#o1, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/account#u1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r2, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r4, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8 | (none) | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n15 | 669f1aa8f2c3423d | 4dae95f4096dd264 | 7323 | 7577 |
| control | 2 | PARTIAL | AUTHORED | strip_outer_code_fence | no | no | unresolved |  |  |  |  |  |  |  |  |  |  | 1f6d407b2eac5f0b | e31194dec7efb59d | 7628 | 10276 |
| control | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 11 | claim=3, commitment=2, objection=1, problem=2, use=3 | k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11 | (none) | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#o1, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/account#u1, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11 | 9505b46a53939afa | 2189ed1205bd9adf | 5661 | 7823 |
| control | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 11 | claim=3, commitment=1, objection=1, problem=1, use=5 | k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11 | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/rival#r6 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#o1, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r4, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8 | (none) | k1, k2, k3, k4, k5, k6, k7, k8, k9, k10 | 45f73780ebbbdfdb | 64ae5349a568644c | 5672 | 6865 |
| control | 5 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 14 | claim=6, commitment=3, objection=1, problem=2, use=2 | k1, k2, k3, k4, k5, k6, k7, u1, u2, u3, u4, u5, p1, p2 | daily/mini_fcl/cycle-1/rival#r6 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c1, daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#o1, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r2, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r4, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | p1, u1 | k1, k2, k3, k4, k5, k6, k7, u1, u2, u3, u4, u5 | b0c06b4991b4a702 | 567d398b60e1d428 | 6105 | 9432 |

**Unresolved in this cell:** control/rep2

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/ollama-glm-5.3__fcl.md`

## ollama-glm-5.3 / prose

| case | rep | delivery | envelope | repairs | strict parse | comparable | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 93d83ec73d1cf4d8 | 84b9a385b2816ca2 | 6416 | 3538 |
| original | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 57fa96c2a25bddc4 | c165b79024dfd18f | 5905 | 2820 |
| original | 3 | COMPLETE | AUTHORED | (none) | yes | yes | 779ab90b646f7142 | 106c3a2ec2433d53 | 6933 | 4549 |
| original | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | c613caf33876c340 | 17df0ec17e8794e3 | 5162 | 2849 |
| original | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 82d1d97b6d940f6e | ad6e1bdc78703a20 | 5283 | 3682 |
| recoding | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 1e6604520daecd64 | 6a2d6604be01d929 | 6367 | 3502 |
| recoding | 2 | COMPLETE | AUTHORED | (none) | yes | yes | d5f47a2c308c12d5 | 65aff45de1c6ba33 | 4520 | 3025 |
| recoding | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 84abf89ded446964 | ac89b1053cf0a892 | 5774 | 3912 |
| recoding | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | d10cae9e5a563b0f | a3306db0e1fe52c0 | 6235 | 3702 |
| recoding | 5 | COMPLETE | AUTHORED | (none) | yes | yes | dcc0b93f308bba14 | 3cab627e80d6679b | 5513 | 3236 |
| carrier | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 4b192f9bafabcf46 | 6259299282b9b2b4 | 6327 | 3524 |
| carrier | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | ef34c7b3be6f8ce5 | 05458360f2edd486 | 5877 | 3097 |
| carrier | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | eb8778ea31dc72d2 | 6bccae78e7ec5a95 | 5451 | 2738 |
| carrier | 4 | COMPLETE | AUTHORED | json_strict_false | no | yes | 9eaa569abec3f6e7 | 8fb92972cafc72d7 | 7104 | 4665 |
| carrier | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 7cd52bc44ba31416 | 830f61992b23e9c8 | 5620 | 3040 |
| control | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 8c2385285d1655d1 | 06ff8ef0340060eb | 6358 | 2778 |
| control | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 77f13a04653e28c5 | 12ddf70c1163e26d | 5158 | 3004 |
| control | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 0a72841996a67005 | 6351bea223867644 | 5813 | 3679 |
| control | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 6cac677d4d7017b5 | a0400cb2efb56adc | 5244 | 2978 |
| control | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 36bfbfbf7a266bed | 12f4d90eba2235d0 | 6615 | 3475 |

**Unresolved in this cell:** (none)

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/ollama-glm-5.3__prose.md`

## ollama-gpt-oss-120b / fcl

| case | rep | delivery | envelope | repairs | strict parse | comparable | fcl parse | records | by type | record ids | targets named | objection ids in refs (prefix-resolved) | account-prefixed refs | rival-prefixed refs | refs with an unrecognised prefix | bare id refs (unresolved) | uptake | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 8 | claim=2, commitment=2, objection=1, problem=1, use=2 | d1, d2, d3, d4, d5, d6, d7, d8 | c3 | (none) | (none) | (none) | (none) | c1, c2 | d1, d2, d3, d4, d5, d6, d7, d8 | 9a7fa7fe3cdb63d3 | fd21554483bd05e9 | 2555 | 2710 |
| original | 2 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 9 | claim=1, commitment=2, objection=2, problem=1, use=3 | a1, a2, a3, a4, a5, a6, a7, a8, a9 | a4, c2 | (none) | (none) | (none) | (none) | c1, c2 | a1, a2, a3, a4, a5, a6, a7, a8, a9 | 564861e18d25b6aa | ef46067358c757f5 | 2786 | 3211 |
| original | 3 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 9 | claim=3, commitment=3, objection=1, problem=1, use=1 | d1, d2, d3, d4, d5, d6, d7, d8, d9 | c3 | (none) | (none) | (none) | (none) | c1, c2 | d1, d2, d3, d4, d5, d6, d7, d8, d9 | 5d5bf5a5a37c5f3c | c33981c1d326f42b | 2565 | 2544 |
| original | 4 | COMPLETE | AUTHORED | (none) | yes | yes | FAILED |  |  |  |  |  |  |  |  |  |  | 7fd8a84f611c9a06 | b98c40145ed2ebcc | 2848 | 2064 |
| original | 5 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 8 | claim=2, commitment=1, objection=1, problem=1, use=3 | a1, a2, a3, a4, a5, a6, a7, a8 | (none) | (none) | (none) | (none) | (none) | (none) | a1, a2, a4, a5, a7, a8 | 7553b30ae981ebdd | 775b81252f559c72 | 1818 | 2595 |
| recoding | 1 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 8 | claim=2, commitment=1, objection=1, problem=1, use=3 | a1, a2, oA, uA, uB, uC, pA, cA | c2 | (none) | (none) | (none) | (none) | c2 | c1, c2, c3, o1, o2, r2, r6 | 8834601c84430fd6 | cd862d2e66c7d0f5 | 2259 | 2745 |
| recoding | 2 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 10 | claim=3, commitment=2, objection=1, problem=1, use=3 | d1, d2, d3, d4, d5, d6, d7, d8, d9, d10 | c2 | (none) | (none) | (none) | (none) | c1, c2 | d1, d2, d3, d4, d5, d6, d7, d8, d9, d10 | 1d445612a189ce45 | 30522100b8c70fcc | 2945 | 3483 |
| recoding | 3 | COMPLETE | OPAQUE | (none) | no | yes | FAILED |  |  |  |  |  |  |  |  |  |  | 3edba3f52abc2517 | e3b0c44298fc1c14 | 5734 | 0 |
| recoding | 4 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 7 | claim=2, commitment=2, objection=1, problem=1, use=1 | d1, d2, d3, d4, d5, d6, d7 | c2, c3 | (none) | (none) | (none) | (none) | c1, c2 | c2, c3, r2, o1, o2 | c8e43a59f524f2c7 | 0b319b71d8f16cd2 | 2630 | 2025 |
| recoding | 5 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 9 | claim=2, commitment=3, objection=1, problem=1, use=2 | c1, c2, c3, c4, c5, c6, c7, c8, c9 | c5 | (none) | (none) | (none) | (none) | c1, c2 | c1, c2, c3, c4, c5, c6, c7, c8, c9 | 054418d00489cb86 | 4bb0a157732cba05 | 3807 | 3716 |
| carrier | 1 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 6 | claim=0, commitment=1, objection=1, problem=1, use=3 | d1, d2, d3, d4, d5, d6 | c1, c2, c3, r2 | (none) | (none) | (none) | (none) | c1, c2 | d1, d2, d3, d4, d5, d6 | 0d3b554e34977818 | a263105522d0614b | 1408 | 1467 |
| carrier | 2 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 10 | claim=3, commitment=0, objection=2, problem=1, use=3 | cA, u1, r1, o1, o2, p1, u2, cB, cC, u3 | account#c2, account#c3 | (none) | c2, c3 | (none) | (none) | p1, u1 | cA, u1, r1, o1, o2, p1, u2, cB, cC, u3 | 68a402b39fa69b3e | fe4d1756ea89ae20 | 3244 | 3096 |
| carrier | 3 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 7 | claim=3, commitment=1, objection=1, problem=1, use=1 | a1, a2, a3, a4, a5, a6, a7 | c2 | (none) | (none) | (none) | (none) | c2 | a1, a2, a3, a5 | 1b7f86eef747eff2 | 58918fafbb260614 | 2360 | 2348 |
| carrier | 4 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 10 | claim=3, commitment=2, objection=2, problem=1, use=2 | r1, r2, r3, r4, r5, r6, r7, r8, r9, r10 | (none) | (none) | (none) | (none) | (none) | (none) | r1, r2, r3, r4, r5, r6, r7, r8, r9, r10 | 6da306c0b392f2e6 | 8338997772723acf | 2006 | 3206 |
| carrier | 5 | COMPLETE | AUTHORED | (none) | yes | yes | FAILED |  |  |  |  |  |  |  |  |  |  | 10d5006a44fbdf7c | f3354a2c681ba604 | 3417 | 3509 |
| control | 1 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 10 | claim=4, commitment=0, objection=1, problem=1, use=2 | c1, c2, c3, c4, u1, u2, p1, r1, r2, o1 | (none) | (none) | (none) | (none) | (none) | c1, c2 | c1, c2, c3, c4, u1, u2, p1, r1, r2, o1 | f1a54a7eb5e366c0 | 68451134cbe818ad | 2134 | 3085 |
| control | 2 | COMPLETE | OPAQUE | (none) | no | yes | FAILED |  |  |  |  |  |  |  |  |  |  | c7e2f79b710bf58c | e3b0c44298fc1c14 | 5873 | 0 |
| control | 3 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 5 | claim=0, commitment=1, objection=1, problem=1, use=2 | a1, a2, a3, a4, a5 | (none) | (none) | (none) | (none) | (none) | c1, c2 | c1, c2, o1, r2, r6, r7 | 8b4750cc6d4f21f3 | 83cf7893be8b3255 | 1426 | 1250 |
| control | 4 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 5 | claim=1, commitment=1, objection=1, problem=1, use=1 | a1, a2, a3, a4, a5 | (none) | (none) | (none) | (none) | (none) | c1, c2 | c1, c2, c3, o1, r2, a1, a2, a3, a4, a5 | 4a58d988d190301b | a28fe0a0a9bb6ece | 2942 | 1611 |
| control | 5 | COMPLETE | AUTHORED | (none) | yes | yes | FAILED |  |  |  |  |  |  |  |  |  |  | 6786699a13e92ad8 | aaa0cab27372449d | 2843 | 2468 |

**Unresolved in this cell:** (none)

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/ollama-gpt-oss-120b__fcl.md`

## ollama-gpt-oss-120b / prose

| case | rep | delivery | envelope | repairs | strict parse | comparable | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | (none) | yes | yes | c435835295c6cf9d | 133214665f7078c6 | 3559 | 850 |
| original | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 753893580463b993 | d93f5140a487159b | 4076 | 739 |
| original | 3 | COMPLETE | AUTHORED | (none) | yes | yes | 5fb0f4feadbced07 | a616fefbb52f5970 | 3501 | 1033 |
| original | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 8b76c8c304adb260 | cdb3dfdf2a32f704 | 3657 | 1041 |
| original | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 2fcd2e9dc83fb36c | 828550fa102f1602 | 3991 | 1196 |
| recoding | 1 | COMPLETE | AUTHORED | (none) | yes | yes | 3b1b3378aa6d979d | cdc9a98ce7f86ead | 3077 | 1505 |
| recoding | 2 | COMPLETE | AUTHORED | (none) | yes | yes | c53509e7c0700c55 | d31c9832deec0a3b | 4119 | 1058 |
| recoding | 3 | COMPLETE | AUTHORED | (none) | yes | yes | 0c9903875bf01a28 | 3a71fdb2c8e3fa7c | 4605 | 745 |
| recoding | 4 | COMPLETE | AUTHORED | (none) | yes | yes | f312306e731fb5eb | 6d78f6343a99476f | 3519 | 1017 |
| recoding | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 55daee3ff8189739 | 41a42a258c238d97 | 3653 | 886 |
| carrier | 1 | COMPLETE | OPAQUE | (none) | no | yes | 0c9040dd34faa64d | e3b0c44298fc1c14 | 4756 | 0 |
| carrier | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 14811385d2ec3aa7 | 70daf04bb68efbcc | 2097 | 1322 |
| carrier | 3 | COMPLETE | AUTHORED | (none) | yes | yes | 99e668f996e5bb22 | d6c9f9449a5553f7 | 2493 | 727 |
| carrier | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 4d2f1245cf41745d | 8eb9c6c7e9647691 | 3615 | 1674 |
| carrier | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 83fc9d230297d805 | 8d2c1c60f23662e4 | 3763 | 1600 |
| control | 1 | COMPLETE | AUTHORED | (none) | yes | yes | c8f83ac88ebbf25f | e882414d9fc04967 | 3429 | 1007 |
| control | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 9b0221a5ac135ded | cab612d1cdad5df7 | 3622 | 747 |
| control | 3 | COMPLETE | AUTHORED | (none) | yes | yes | 19f0c1cfef1a1081 | 6ae80ed611740ef9 | 3726 | 966 |
| control | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 3d07b8d59dd4cbdb | e935beb9797c7d53 | 3210 | 929 |
| control | 5 | COMPLETE | AUTHORED | (none) | yes | yes | acbde917f9e54b2c | 202baa2ac82ce05d | 3585 | 1110 |

**Unresolved in this cell:** (none)

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/ollama-gpt-oss-120b__prose.md`

## ollama-kimi-k3 / fcl

| case | rep | delivery | envelope | repairs | strict parse | comparable | fcl parse | records | by type | record ids | targets named | objection ids in refs (prefix-resolved) | account-prefixed refs | rival-prefixed refs | refs with an unrecognised prefix | bare id refs (unresolved) | uptake | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 11 | claim=4, commitment=1, objection=2, problem=1, use=3 | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11 | daily/mini_fcl/cycle-1/rival#r6, n3, n6 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c1, daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/objection#c2, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o4, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | n2, n3, n5, n6, n8, n9, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r11 | 3e85757cf702d915 | 6ca3d32187006ebf | 4910 | 6215 |
| original | 2 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 15 | claim=7, commitment=4, objection=1, problem=1, use=2 | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15 | 406eff787391049a53c08a1fa638c1576c4a54c65be4bdde122593deb25fdbbe#u1, a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r6 | c2, o1, o2, o3, o4, p1, u1 | c1, c2, c3 | r10, r11, r2, r6, r7, r8 | (none) | (none) | n3, n4, n5, n6, n8, n9, n10, n11, n12, n13, n14, cd6e3e2f307e0dac79543de9bed087db4ee7dcd40b3d989d3c6d4b02057d8b99#c1, cd6e3e2f307e0dac79543de9bed087db4ee7dcd40b3d989d3c6d4b02057d8b99#c3, 406eff787391049a53c08a1fa638c1576c4a54c65be4bdde122593deb25fdbbe#o2, 406eff787391049a53c08a1fa638c1576c4a54c65be4bdde122593deb25fdbbe#o3, 406eff787391049a53c08a1fa638c1576c4a54c65be4bdde122593deb25fdbbe#p1, a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r2, a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r7, a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r8, a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r9, a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r10, a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r11 | e2f0919a4c7472a9 | b42958efefca9a10 | 5630 | 8083 |
| original | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 14 | claim=5, commitment=2, objection=3, problem=2, use=2 | c1, c2, c3, c4, c5, o1, o2, o3, u1, u2, m1, m2, p1, p2 | c4, c5, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/rival#r6, u1 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c1, daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/account#u1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#o4, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | c1, c2, o3, u1 | c1, c2, c4, c5, u1, u2, m1, m2 | b59ee61aea9d6d05 | aaaf5de1228dc257 | 6997 | 8164 |
| original | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 13 | claim=4, commitment=2, objection=1, problem=1, use=5 | s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13 | 406eff787391049a53c08a1fa638c1576c4a54c65be4bdde122593deb25fdbbe#o1, s5, s6, s7, s8 | c1, o1, o2, o4, p1, u1 | c2, p1, u1 | r10, r11, r2, r4, r5, r6, r7, r8, r9 | (none) | (none) | s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12 | 4dc850dd5bb60762 | 7f652de08e3acfcb | 6781 | 8982 |
| original | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 12 | claim=6, commitment=1, objection=2, problem=1, use=2 | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12 | n4, n5, rival#r6 | c1, o1, o2, o4, p1, u1 | BODY, c1, c2, c3, o1 | r11, r2, r6, r7, r8, r9 | (none) | (none) | n1, n2, n3, n4, n5, n6, n7, n9, n10, n11 | 227c18045c7eaa14 | 7bd792ddc02b4123 | 5027 | 5612 |
| recoding | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 12 | claim=2, commitment=2, objection=3, problem=2, use=3 | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, p1, p2 | daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#u1, daily/mini_fcl/cycle-1/rival#r6 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c1, daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#o4, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/objection#u1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r2, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10 | 5a5258d444fda5f7 | f6f57498c61549c0 | 5671 | 6678 |
| recoding | 2 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 10 | claim=5, commitment=0, objection=2, problem=0, use=3 | s1, s2, s3, s4, s5, s6, s7, s8, s9, s10 | a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r6, a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r7 | c2, o1, o2 | c1, c2, c3, u1 | r2, r4, r6, r7, r8 | (none) | (none) |  | e5e01ee346a9deaf | 3160f556eba9a2bf | 6093 | 6434 |
| recoding | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 12 | claim=3, commitment=2, objection=3, problem=1, use=3 | a1, a2, a3, u1, u2, u3, o1, o2, o3, co1, co2, p1 | 406eff787391049a53c08a1fa638c1576c4a54c65be4bdde122593deb25fdbbe#o3, a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#BODY, u1, u3 | o1, o2, o3, o4 | BODY, c1, c2, c3, p1 | BODY, r10, r11, r2, r6, r7, r8, r9 | (none) | u1 | a1, a2, a3, u1, u2, u3, o1, co1, co2 | fdc2191279655590 | 0f94bc3fd17a804a | 5837 | 6911 |
| recoding | 4 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 14 | claim=2, commitment=2, objection=2, problem=2, use=6 | t1, h1, h2, s1, s2, s3, s4, s5, k1, k2, j1, j2, q1, q2 | daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/rival#r6, s3, s4 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#BODY, daily/mini_fcl/cycle-1/account#c1, daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/account#u1, daily/mini_fcl/cycle-1/objection#c2, daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#o4, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r4, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | t1, h1, h2, s1, s2, s3, s4, s5, k1, k2, j1, j2 | f6dbe563035f1667 | efc885259d674c31 | 4490 | 7211 |
| recoding | 5 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 12 | claim=4, commitment=3, objection=2, problem=2, use=1 | n-cl1, n-cl2, n-cl3, n-cl4, n-o1, n-o2, n-c1, n-c2, n-c3, n-u1, n-p1, n-p2 | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#u1, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#o4, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/objection#u1, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | n-cl1, n-cl2, n-cl3, n-cl4, n-o1, n-o2, n-c1, n-c2, n-c3, n-u1, n-p1, n-p2 | d7ddfae4365a6451 | 62e2d22ffa6e30f6 | 6497 | 7639 |
| carrier | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 12 | claim=2, commitment=4, objection=2, problem=1, use=3 | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n12, n11 | n2, n3, n4 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#BODY, daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/account#u1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#o4, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/rival#r10, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n12 | 90a90c67e905c64b | b4b49e390c7602c9 | 5540 | 5944 |
| carrier | 2 | COMPLETE | OPAQUE | (none) | no | yes | FAILED |  |  |  |  |  |  |  |  |  |  | 8fc9602442765e4c | e3b0c44298fc1c14 | 17106 | 0 |
| carrier | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 11 | claim=5, commitment=1, objection=1, problem=1, use=3 | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11 | a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r3 | o1, o2, o3, o4, p1 | c2, c3, o1, p1, u1 | r11, r3, r5, r6, r7, r8, r9 | (none) | (none) | n1, n2, n3, n4, n5, n6, n7, n8, n9, n11 | 96c1dc033b773660 | dee433ee4f93f14b | 5520 | 7757 |
| carrier | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 12 | claim=5, commitment=2, objection=2, problem=1, use=2 | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12 | (none) | o1, o4, p1 | BODY, c1, c2, o1, p1 | r10, r11, r2, r5, r7, r8, r9 | (none) | (none) | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11 | 2995d736d39c57b1 | 08cdb452be2b9ab4 | 5145 | 6409 |
| carrier | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 10 | claim=2, commitment=4, objection=3, problem=1, use=0 | c1, c2, k1, k2, k3, k4, o1, o2, o3, p1 | daily/mini_fcl/cycle-1/rival#r6, k2, k3 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#BODY, daily/mini_fcl/cycle-1/account#c1, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/account#u1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#o1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o4, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/objection#u1, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r2, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r4, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | c1, c2 | c1, c2, k1, k2, k3, k4, o1, o2, o3 | 1e3e786b0684150f | ba3cc496b51d8cbc | 5350 | 5915 |
| control | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 11 | claim=4, commitment=2, objection=2, problem=1, use=2 | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11 | a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r3 | (none) | c2, c3, o1, p1, u1 | r1, r10, r11, r2, r3, r6, r7, r8, r9 | (none) | (none) | n1, n2, n3, n4, n5, n6, n7, n8, n10 | 2630dc5bad44bdf2 | fd19688739b08c5c | 5278 | 5494 |
| control | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 12 | claim=4, commitment=2, objection=2, problem=1, use=3 | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12 | (none) | (none) | BODY, c2, c3, p1 | r11, r2, r5, r6, r7, r8, r9 | (none) | (none) | n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11 | 0c0d2f88aaf17e2e | df1ae6d2bf29c12b | 5474 | 6794 |
| control | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 11 | claim=3, commitment=1, objection=2, problem=1, use=4 | s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11 | daily/mini_fcl/cycle-1/rival#r7 | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#BODY, daily/mini_fcl/cycle-1/account#c1, daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#o1, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r2, daily/mini_fcl/cycle-1/rival#r3, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | s1, s2, s3, s4, s5, s6, s7, s8, s9, s10 | 8c842e039b942e48 | ea4f4c8cefa1d5a0 | 4843 | 5515 |
| control | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 9 | claim=4, commitment=2, objection=1, problem=1, use=1 | n1, n2, n3, n4, n5, n6, n7, n8, n9 | (none) | (none) | BODY, c1, c2, c3, o1, p1, u1 | r10, r11, r2, r3, r4, r5, r6, r7, r8, r9 | (none) | (none) | n1, n2, n3, n4, n5, n6, n7, n9 | 5ef2a8922f2c45b2 | 44c45fa4eed27f0a | 4677 | 6589 |
| control | 5 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 9 | claim=3, commitment=2, objection=2, problem=2, use=0 | n1, n2, n3, n4, n5, n6, n7, n8, n9 | a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r7, a6a817c086b877f919ae3a927d532ce46d007e49969962bcc613eb541fae0644#r8, cd6e3e2f307e0dac79543de9bed087db4ee7dcd40b3d989d3c6d4b02057d8b99#c2 | (none) | BODY, c1, c2, c3, o1, p1 | r11, r2, r5, r6, r7, r8, r9 | (none) | (none) | n1, n2, n3, n4, n5, n6, n7 | bd376768182c3515 | 5b29bc6aff425305 | 4442 | 6078 |

**Unresolved in this cell:** (none)

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/ollama-kimi-k3__fcl.md`

## ollama-kimi-k3 / prose

| case | rep | delivery | envelope | repairs | strict parse | comparable | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | (none) | yes | yes | 64a1335b6dd2f2e5 | 54d15bc618077dd3 | 5571 | 2595 |
| original | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 927fa69ec2e7162d | 4314a927e48b5147 | 5761 | 3314 |
| original | 3 | COMPLETE | AUTHORED | (none) | yes | yes | 771ecf7f53ce4325 | 39230b2ce47f42b3 | 6900 | 3302 |
| original | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 3b5e4a68c3f17ebc | d8ff3c49f2f2e0fb | 6017 | 2937 |
| original | 5 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 64975bae40fb0a19 | 879658aa55d90e1d | 5300 | 3248 |
| recoding | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | fd0c6ed84470d217 | 3356a77dd236bd4b | 6564 | 3175 |
| recoding | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 84ab46fcd23ca95e | ffbdecb3aeb223c9 | 4796 | 3182 |
| recoding | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | c14cfd486fa0a3d4 | aa17850d2a3349bd | 4897 | 2860 |
| recoding | 4 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | 2cc96b27ad6b18a9 | b220f9f1b7242b98 | 6088 | 3598 |
| recoding | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 8510edbec408470e | 46572d5eb46889c3 | 6005 | 3281 |
| carrier | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | ab7f6e7fe3bdad59 | e99635b9077fc4be | 5174 | 3011 |
| carrier | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | a3a8a64347f61aff | 4c58c70776e54a50 | 5778 | 3191 |
| carrier | 3 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | ea3dcceb7e95d5bc | e13b0d71a7212362 | 4767 | 3385 |
| carrier | 4 | COMPLETE | OPAQUE | (none) | no | yes | 91f11f0e36c56db5 | e3b0c44298fc1c14 | 9313 | 0 |
| carrier | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 0f258fde5aba6e49 | 03c03e66fae73eee | 6207 | 2734 |
| control | 1 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | a06c9b6b051009b9 | 43e4cc399c76e845 | 5657 | 2677 |
| control | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | a39453e060e461e5 | 5fedc34f0205b038 | 4716 | 2846 |
| control | 3 | COMPLETE | AUTHORED | (none) | yes | yes | f592ee6eba42615d | 7e9021ecafef4a53 | 5176 | 4005 |
| control | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 17c47d4d8aa4e969 | 9a3d9d816a11eb09 | 5041 | 3656 |
| control | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 0d27c2c5b0d55cb2 | 5a196ac5f877ce78 | 5434 | 3729 |

**Unresolved in this cell:** (none)

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/ollama-kimi-k3__prose.md`

## ollama-qwen3.5-397b / fcl

| case | rep | delivery | envelope | repairs | strict parse | comparable | fcl parse | records | by type | record ids | targets named | objection ids in refs (prefix-resolved) | account-prefixed refs | rival-prefixed refs | refs with an unrecognised prefix | bare id refs (unresolved) | uptake | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 9 | claim=3, commitment=3, objection=1, problem=1, use=1 | m1, m2, m3, m4, m5, m6, m7, m8, m9 | (none) | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#step5, daily/mini_fcl/cycle-1/rival#r6, p.objection.0#o2 | (none) | m1, m2, m3, m4, m5, m6, m9 | 82d07bda73cb9f4c | 4dcabec1a70c4589 | 2915 | 3114 |
| original | 2 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 8 | claim=3, commitment=0, objection=1, problem=2, use=2 | c1, c2, c3, o1, u1, u2, p1, p2 | (none) | (none) | (none) | (none) | (none) | c1, u1 | c1, c2, c3, u1, u2 | 00445a20de108da6 | 34b57b3a2bd2c596 | 2621 | 2688 |
| original | 3 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 7 | claim=2, commitment=2, objection=1, problem=1, use=1 | i1, i2, i3, i4, i5, i6, p1 | i1, i2 | o1, o2 | (none) | r6, r7 | (none) | (none) | i1, i2, i3, i4, i6 | 8b4b8a24ff2a2194 | e2fe24764d107f7f | 2741 | 2802 |
| original | 4 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 9 | claim=3, commitment=0, objection=2, problem=2, use=2 | c1, c2, c3, o1, o2, u1, u2, p1, p2 | p.objection.0#BODY, p.rival.0#r6 | (none) | (none) | (none) | p.objection.0#BODY, p.objection.0#o2, p.rival.0#r6, p.rival.0#r7 | c1, c2 | c1, c2, c3, o1, o2, u1, u2, p1, p2 | a207ce079b8afbb8 | cfbc2257b1589bcc | 2970 | 3033 |
| original | 5 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 7 | claim=2, commitment=2, objection=1, problem=1, use=1 | m1, m2, m3, m4, m5, m6, p1 | (none) | (none) | (none) | (none) | (none) | (none) | m1, m2, m3, m4, m5, m6 | 1bd0cc5bcfbceb43 | 3e38fe403280c24b | 2294 | 2242 |
| recoding | 1 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 8 | claim=2, commitment=3, objection=1, problem=1, use=1 | s1, s2, s3, s4, s5, s6, s7, s8 | (none) | (none) | (none) | (none) | (none) | (none) | s1, s2, s3, s4, s5, s8 | 64756b0341bfdea9 | 208d19c5381c93bf | 3419 | 3217 |
| recoding | 2 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 9 | claim=3, commitment=0, objection=2, problem=2, use=2 | c1, c2, c3, o1, o2, u1, u2, p1, p2 | (none) | (none) | (none) | (none) | (none) | c1, c2, o1, u1 | c1, c2, c3, u1, u2 | b12006f02402aa35 | 6b03b4fcac5aad8b | 3103 | 2255 |
| recoding | 3 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 10 | claim=3, commitment=0, objection=2, problem=2, use=3 | c1, c2, c3, o1, o2, u1, u2, u3, p1, p2 | (none) | (none) | (none) | (none) | (none) | (none) | c1, c2, c3, o1, u1, u2, u3 | 22f3ccae8974d4be | 45eefd6a2efccb06 | 3581 | 1995 |
| recoding | 4 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 9 | claim=2, commitment=4, objection=1, problem=1, use=1 | d1, d2, d3, d4, d5, d6, d7, d8, d9 | e360ee14fa7545c90cadf79c7d2fe9c157faf470d6368504b06768e36e0d13c79#c2 | (none) | (none) | (none) | e360ee14fa7545c90cadf79c7d2fe9c157faf470d6368504b06768e36e0d13c79#c2 | (none) | d1, d2, d3, d4, d5, d6, d8, d9 | 72b305500095be65 | af9e455c98f368d2 | 3567 | 3790 |
| recoding | 5 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 11 | claim=3, commitment=2, objection=2, problem=1, use=3 | c1, c2, c3, o1, o2, u1, u2, u3, p1, cm1, cm2 | account#c1, account#c2 | o2 | c1, c2 | r11, r6, r7 | (none) | c1, c2, u1 | c1, c2, c3, o1, u1, u2, u3, p1, cm1, cm2 | 1fcc7d7df5a26274 | 4240bd809e6f62f1 | 2933 | 4531 |
| carrier | 1 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 9 | claim=3, commitment=2, objection=1, problem=1, use=2 | m1, m2, m3, m4, m5, m6, m7, m8, m9 | (none) | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/account#p1, daily/mini_fcl/cycle-1/objection#c1, daily/mini_fcl/cycle-1/objection#o2, daily/mini_fcl/cycle-1/objection#o3, daily/mini_fcl/cycle-1/objection#p1, daily/mini_fcl/cycle-1/rival#r11, daily/mini_fcl/cycle-1/rival#r2, daily/mini_fcl/cycle-1/rival#r4, daily/mini_fcl/cycle-1/rival#r5, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7 | (none) | m1, m2, m3, m4, m5, m6, m7, m8, m9 | 7a5887566805c375 | 262f50f077c938ca | 3761 | 3933 |
| carrier | 2 | COMPLETE | AUTHORED | strip_outer_code_fence | no | yes | OK | 8 | claim=2, commitment=3, objection=1, problem=1, use=1 | s1, s2, s3, s4, s5, o1, p1, u1 | (none) | (none) | (none) | (none) | e3647350a300c0ed#BODY | (none) | s1, s2, s3, s4, s5, u1 | 47d6982021b678d8 | 8b687a671d38b84b | 2412 | 2853 |
| carrier | 3 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 6 | claim=2, commitment=1, objection=1, problem=1, use=1 | s1, s2, s3, s4, s5, s6 | (none) | (none) | (none) | (none) | (none) | (none) | s1, s2, s3, s6 | 6ca0c6310a705a47 | 821e52ff79c925a4 | 2820 | 1339 |
| carrier | 4 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 10 | claim=3, commitment=1, objection=2, problem=1, use=3 | s1, s2, s3, s4, s5, s6, s7, s8, s9, s10 | p.objection.0#c2 | (none) | (none) | (none) | p.objection.0#c2 | (none) | s1, s2, s3, s6, s7, s8, s10 | f9303239cd9904f4 | 7e76b5390fea746e | 2838 | 2641 |
| carrier | 5 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 9 | claim=2, commitment=3, objection=2, problem=1, use=1 | m1, m2, m3, m4, m5, m6, m7, m8, m9 | p.account#c2 | (none) | (none) | (none) | p.account#BODY, p.account#c1, p.account#c2, p.objection#o1, p.objection#o2, p.rival#r11, p.rival#r2, p.rival#r7, p.rival#r9 | (none) | m1, m2, m3, m4, m5, m7, m9 | 3a77973a6e391625 | f5c4c72ab42a70e8 | 3659 | 3844 |
| control | 1 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 8 | claim=3, commitment=2, objection=1, problem=1, use=1 | m1, m2, m3, m4, m5, m6, m7, m8 | (none) | (none) | (none) | (none) | (none) | (none) | m1, m2, m3, m4, m5, m6, m8 | 2ba2d5447f0073af | 593e3980433e579b | 3187 | 2841 |
| control | 2 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 7 | claim=2, commitment=2, objection=1, problem=1, use=1 | m1, m2, m3, m4, m5, m6, o1 | (none) | (none) | (none) | (none) | (none) | (none) | m1, m2, m3, m4, m6, o1 | ae0834c9cc70607b | 6822e1ce4d36588a | 2374 | 2486 |
| control | 3 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 8 | claim=3, commitment=2, objection=1, problem=1, use=1 | h1, h2, h3, h4, h5, h6, h7, u1 | (none) | (none) | (none) | (none) | (none) | (none) | h1, h2, h3, h4, h5, u1 | 1c2259e5ac403317 | a5063deb006af558 | 3342 | 2279 |
| control | 4 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 4 | claim=1, commitment=1, objection=1, problem=0, use=1 | m1, m2, m3, m4 | (none) | (none) | (none) | (none) | daily/mini_fcl/cycle-1/account#c2, daily/mini_fcl/cycle-1/account#c3, daily/mini_fcl/cycle-1/rival#r6, daily/mini_fcl/cycle-1/rival#r7, daily/mini_fcl/cycle-1/rival#r8, daily/mini_fcl/cycle-1/rival#r9 | (none) | m1, m2, m3, m4 | 60d9279f1dc96645 | 8cdc4d1584a0fa8a | 1400 | 1580 |
| control | 5 | COMPLETE | AUTHORED | (none) | yes | yes | OK | 7 | claim=1, commitment=3, objection=1, problem=1, use=1 | m1, m2, m3, m4, m5, m6, m7 | (none) | (none) | (none) | (none) | (none) | (none) | m1, m2, m3, m4, m7 | 365b29a784af9b72 | d0d90e7f29a53dc8 | 2670 | 2252 |

**Unresolved in this cell:** (none)

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/ollama-qwen3.5-397b__fcl.md`

## ollama-qwen3.5-397b / prose

| case | rep | delivery | envelope | repairs | strict parse | comparable | body sha256 | commitments sha256 | body chars | commitments chars |
|---|---|---|---|---|---|---|---|---|---|---|
| original | 1 | COMPLETE | AUTHORED | (none) | yes | yes | 8467e8ef0d78a2e6 | 228f2d45db4a5e38 | 2542 | 2476 |
| original | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 87540bb3a920e508 | 2fdd4764320f186b | 1794 | 1921 |
| original | 3 | COMPLETE | AUTHORED | (none) | yes | yes | 94c6f59ad118cd3f | a791d966f352010f | 2487 | 2536 |
| original | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 19f69afb6a6ae2a9 | 15f36de09f5f92ac | 2168 | 1686 |
| original | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 4b1edc468e5e2f0b | 69f1cf28738decf4 | 3047 | 2531 |
| recoding | 1 | COMPLETE | AUTHORED | (none) | yes | yes | a9f369526628acd6 | e0a686e2aa3bf3ca | 2361 | 2226 |
| recoding | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 9ea75acb7642861c | 78323736f4cd2eeb | 1883 | 1318 |
| recoding | 3 | COMPLETE | AUTHORED | (none) | yes | yes | 6c84270b5b3711ef | bc530d92d2e2b855 | 2201 | 1973 |
| recoding | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 6236bfb35f2efa39 | 2a5aeff4077d3238 | 1953 | 1761 |
| recoding | 5 | COMPLETE | AUTHORED | (none) | yes | yes | e5c95c0fca164d18 | 8c985aa3e1bf5491 | 1626 | 1560 |
| carrier | 1 | COMPLETE | AUTHORED | (none) | yes | yes | 6045582208b64c06 | e0f824474dde6d94 | 1855 | 1702 |
| carrier | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 923a09c92df7a54c | 74339e681e7651e3 | 3026 | 2828 |
| carrier | 3 | COMPLETE | AUTHORED | (none) | yes | yes | 4f4a93dbab5fb717 | f6033776d24e65df | 2209 | 1244 |
| carrier | 4 | COMPLETE | AUTHORED | (none) | yes | yes | 86481ee01ffe1551 | 42464bfb78abb98e | 2198 | 2099 |
| carrier | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 0ff0bff619bfe680 | 34739bee7f0fa1ee | 3239 | 2848 |
| control | 1 | COMPLETE | AUTHORED | (none) | yes | yes | 502cc75d69ff9ad0 | d397dbccd28ab81c | 1372 | 1269 |
| control | 2 | COMPLETE | AUTHORED | (none) | yes | yes | 35ed22eb38edb0dd | dad983c4f585c30a | 1869 | 1249 |
| control | 3 | COMPLETE | AUTHORED | (none) | yes | yes | c6948804b6098a02 | 806a1aae9f40a331 | 1210 | 1199 |
| control | 4 | COMPLETE | AUTHORED | (none) | yes | yes | a84e7722966180ba | 5c060d5afcd520f6 | 2107 | 1516 |
| control | 5 | COMPLETE | AUTHORED | (none) | yes | yes | 685f43e157b5230e | a3e30cd07f1adec2 | 1541 | 1458 |

**Unresolved in this cell:** (none)

### Root's reading (empty until root reads the juxtaposition)

| original_vs_control | original_vs_recoding | original_vs_carrier | pattern_read | grounds | unresolved |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Register marks (empty; one of `differs` / `same` / `unresolved` each)

| comparison | T target named | E objection record engaged | D proposed action | G grounds cited |
|---|---|---|---|---|
| within ORIGINAL (baseline, written first) |  |  |  |  |
| ORIGINAL vs CONTROL |  |  |  |  |
| ORIGINAL vs RECODING |  |  |  |  |
| ORIGINAL vs CARRIER |  |  |  |  |

### Raw juxtaposition

`juxtaposition/ollama-qwen3.5-397b__prose.md`

