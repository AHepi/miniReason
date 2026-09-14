# kimi-k3 worker battery

| id | title | status | mode | transport | iters | tool calls | tokens | wall s | finish | harness failure |
|---|---|---|---|---|---|---|---|---|---|---|
| p6-manifest-reverify-f001 | Re-verify every manifest and sha256 list in today's published experiment records | COMPLETE | tools | native | 37 | grep 3, list_dir 3, read_file 6, run_command 25, write_file 20 (57) | 4473352 | 442.9 | stop | - |

Totals: 1 task(s), 4473352 tokens, 57 tool calls, 0 harness failure(s).

### p6-manifest-reverify-f001 — files written
- `check/custody.py` (added, sha256 792b33390e7c39b5)
- `check/diag.py` (added, sha256 99d3487b746e61d4)
- `check/diag2.py` (added, sha256 bf12418ba7ce45be)
- `check/diag3.py` (added, sha256 1f7232f729eb3534)
- `check/keys.py` (added, sha256 7bca3fcd38b514d8)
- `check/locate.py` (added, sha256 386becfe3ca7888c)
- `check/patch2.py` (added, sha256 6e7d411c0ba81528)
- `check/patch3.py` (added, sha256 d17535539b53060a)
- `check/patch4.py` (added, sha256 ab12f7bdefe189eb)
- `check/patch_c001.py` (added, sha256 e348686f259031cc)
- `check/peek.py` (added, sha256 9724d3476b060e1e)
- `check/planid.py` (added, sha256 811453c65450561a)
- `check/reverify-results.json` (added, sha256 567961fee5162b13)
- `check/reverify.py` (added, sha256 73006c9537852113)
- `check/run_all.py` (added, sha256 c20e915e501fcd31)
- `check/survey.py` (added, sha256 a39032687ce41f9f)
- `check/survey2.py` (added, sha256 574efa399e9f85ff)
- `check/survey3.py` (added, sha256 0b8fe0ed15494b6d)
- `check/verify_out.py` (added, sha256 22b10deb0c8ae356)
- `out/manifest-reverify.json` (added, sha256 b0f8fb4bf3965020)
- `out/manifest-reverify.md` (added, sha256 11f8762d543e735c)

Reasoning characters per turn: 35, 127, 0, 199, 651, 502, 0, 1187, 527, 0, 3499, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8057, 199, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31

Expected outputs present: out/manifest-reverify.md, out/manifest-reverify.json, check/; missing: (none)
