# CLONE-PATCH - L004 current dispositions and implementation decisions

DRAFT only. No source patch, driver action, provider call or launch is authorized here. This supersedes no historical checklist. V4 = docs/design/loop-prereg-draft-2026-09-14/v4; L003 = experiments/loops/L003-loop-first-live-2026-09-14.

The read-only recon-S section 2 supplied the checklist. Each disposition below is checked against the current repository; item 3 corrects that report. Existing historical claims remain at V4/CLONE-PATCH.md:15-237.

| Item | Current disposition | Evidence |
|---|---|---|
| 1 Calibration consumption/audit pin | PARTIAL. Plan and audit carry digest, seats and coverage, but module-built anchor exchanges still replace bundle consumption. Full O5 compliance NOT FOUND. | tools/auto_loop.py:1118-1149,2297-2316; src/minireason/loop/audits.py:538-567; src/minireason/loop/obligations.py:1203-1226; L003/CLOSING.md:52 |
| 2 Calibration-exchange pin | IMPLEMENTED in named pin map; historical absent claim is stale. | tools/auto_loop.py:244-245,713-718 |
| 3 Audit period account | IMPLEMENTED as optional period_account. Recon-S's assertion that it is absent is incorrect at this checkout. L004 puts the proposed account in config. | src/minireason/loop/types.py:1041-1052,1066-1067,1074-1075 |
| 4 Resource conditions | Config remains closed; roles.py is now pinned. Declare actual resource bounds in reading_set.json and require explicit manifest/prompt coverage. | V4/CLONE-PATCH.md:118-129; src/minireason/loop/types.py:1150-1154; tools/auto_loop.py:249-259 |
| 5 Streak counter | IMPLEMENTED/WIRED. Code keeps maximum encountered per-role streak; docstring describes end-of-pass maximum. L004 account follows code and flags the discrepancy. | tools/auto_loop.py:389-426,1274-1276,1985-1996 |
| 6 Unread inventory | PARTIAL. Attached-study juxtapositions/open cells are inventoried; this supplies no occurrence-09 pair rows. Future adapter must enumerate admitted and unadmitted slots. | tools/auto_loop.py:952-995; src/minireason/loop/reader.py:667-678 |
| 7 Occurrence staging | OUT OF SCOPE. Historical separate staging addressed v4; no S-step initializes an occurrence. L004 reads existing frozen material and permits no new initialization. | V4/CLONE-PATCH.md:210-215,228-236; V4/PREREG.md:242-246 |
| 8 No-change publication | IMPLEMENTED WITH LIMIT. Empty selection without pending publication gives UNCHANGED; selected already-committed files still undergo push/read-back and may return VERIFIED without a new commit. This worker publishes nothing. | src/minireason/loop/publish.py:1051-1056,1087-1089,1117-1147 |
| 10 Native runner / foreign-study bridge | OUT OF SCOPE for this reading-only successor. V4 separately identified the foreign-study dispatch seam; this proposal retains already delivered native F001 and requests no new dispatch or bridge. It does not claim the general seam is repaired. | V4/CLONE-PATCH.md:228-236; experiments/diagnostics/F001-fork5-multifamily/occurrence-09/plan.json:32,144-150; PREREG.md section 3 |
| 9 PREFLIGHT overwrite | STILL PRESENT on refusal and success. Never use diagnostic PREFLIGHT against published evidence. This task does not invoke it. | tools/auto_loop.py:1224-1226,1331; V4/CLONE-PATCH.md:220-222 |

## New required decisions

1. **Row builder and adapter - UNIMPLEMENTED.** PREREG.md's Row-construction contract is the proposal: one candidate contribution pair per declared slot; exact references and source spans; no invented author record; unresolved admission preserved. The existing UseRow index has no matching occurrence-09 rows (L003/cycles/cycle-01/use-table/occurrence-09/use_table.json:523; cycle-02 equivalent:523). New adapter aliases must never be presented as historical authored references. Reader surface integration and raw-byte/decoded-offset correspondence require implementation and independent custody checks.

2. **Pin coverage - UNRESOLVED.** Six fixed paths and current S0 extras are in tools/auto_loop.py:236-259,692-718. Direct coverage of builder, source map, reading_set.json, reader/surface/packs, prompt files, source responses, arms/manifests and attached PLAN.md is NOT FOUND there. Draft source hashes are not proof S0 binds them. Freeze the complete relevant closure, with an explicit nonrecursive recipe for a manifest's own pin. Do not promise prompt or study pinning beyond actual implementation.

3. **Audit-record semantics / O5 - UNRESOLVED.** tools/auto_loop.py:2312 registers audit material; obligations.py:1211 seeks AUDIT_RECORD. The predicate also does not establish the stronger bundle requirement of the exact judge pair and actually consumed pinned rows merely from nonempty seats/calibration fields (:1216-1219). Resolve registration, coverage, seat matching and actual bundle-anchor consumption together. L003's closing reports no audit record entered (L003/CLOSING.md:52); an audit step is not itself O5 discharge.

4. **Paths - CONDITIONAL BOUND, NO ACTUAL ROW PATH.** Proposed no-arrow grammar h005-row/<a><l>#u/ref/<e> is parser-compatible (tools/auto_loop.py:328-350), but depends on the unimplemented adapter. Raw maximum 19, folded maximum 32, prefix 81; the longest initial trial provider path is 189 < 240. Actual longest key/path: NOT FOUND. Check all actual paths before admission. The alternative shortened helper is not used by this READ route (src/minireason/loop/types.py:1713-1726; reader.py:576-596). Reopening has no demonstrated fresh path allocation and may encounter existing-coordinate refusal (roles.py:1000-1007).

5. **Budget enforcement - UNRESOLVED.** 11R + 46W is conditional and is not an exact runtime cap. calls_reached counts completed spending-step receipts (tools/auto_loop.py:2466-2469,2491); the planner separately omits dispatch/audit derivation (:470-492,1320-1329). Zero max_calls disables that stop. The draft adds invalid cycle_budget=0 and provider_mode=DRAFT-NO-RUN; types.py:1198-1208 rejects them. True provider-call accounting, actual audit spending and authorized limits must be reconciled before execution.

6. **Reading-only stop and scoped ceiling - UNRESOLVED.** graph.mark_triples ignores relation cells (src/minireason/loop/graph.py:1596-1610); decide.py:930-933 therefore compares empty mark sets here. Approve an explicit relation-state comparison or honestly retain the narrower empty-set stop, never claim relation stability. The inherited renderer's C001/N=5 ceiling clauses need a pinned, explicitly scoped successor treatment. No constant is patched here.

7. **Zero dispatch containment - UNVERIFIED HERE.** Occurrence-09 remains in the nonempty occurrence list. A later route must verify frozen runner/source custody and no pending wave; delivered coordinates and excluded cycles must return before source writes/SEND. Source-only completion must not trigger all_arms_ended as if the reading arm had completed. See PREREG.md section 3 and tools/auto_loop.py:1548-1591,1614-1642,1665-1685.

8. **O/P implementation correspondence - UNRESOLVED.** Draft obligation text is narrower than v4 in study scope and stronger in actual row admission/custody. Existing predicate names are reference points, not proof those words are implemented. Retired C001 obligations are removed from active sets and retained as explicit dispositions; no vacuous discharge is claimed.

Owner approval of this contract and budget, implementation, separately authorized validation/registration and publication precede any future launch. Approval of this drafting task is not launch authorization.
