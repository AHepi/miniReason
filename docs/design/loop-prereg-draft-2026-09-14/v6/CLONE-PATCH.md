# L004 v6 implementation and launch dispositions

**DRAFT. No initialization, provider call or publication.**

| Item | Disposition | Evidence |
|---|---|---|
| Contribution-pair builder | Implemented proposal; six exposed F09 slots admitted offline | src/minireason/loop/rows_pairs.py:201; reading_set.json:candidate_rows |
| Exact source surfaces | Whole UTF-8 contributions and raw span maps; account/archive context labelled separately | src/minireason/loop/rows_pairs.py:325-331 |
| READ selection | Explicit reading_rows_builder=pairs-v1; inherited behavior when absent | config.json; docs/design/loop-impl/WAVE7-INTERFACE.md |
| Conditional S0 closure | Builder/source dependencies added by opt-in driver path; no plan minted | docs/design/loop-impl/WAVE7-INTERFACE.md; reading_set.json:source_pins |
| F003 source | Contingent: separate draft, no live observations or reading keys | reading_set.json:contingent_sources |
| Native F003 boundary | Follow F003 PLAN's actual node topology and input map, including unresolved absent-rival slots | experiments/diagnostics/F003-operative-return/PLAN.md |
| Keys and paths | Actual six-key injectivity; longest 189 < 240, no output directories | reading_set.json:path_length |
| O1 and O3 runtime enforcement | Builder supplies admission evidence; downstream predicate coverage is not established by its success | obligations.json; src/minireason/loop/obligations.py |
| O5 audit | Actual bundle-anchor consumption, exact seat/coverage semantics and registration unresolved | src/minireason/loop/audits.py:538-567; src/minireason/loop/obligations.py:1203-1226 |
| Reading-only stop | Empty mark-set comparison does not track relation reading changes | src/minireason/loop/graph.py:1596-1610 |
| Scoped ceiling | Fixed renderer digest remains; approve explicit scoped treatment before launch | src/minireason/loop/report.py:593-618 |
| Provider budget | 112 initial allowance; true runtime provider-call cap, actual audit cost and reopening allowance unresolved | PREREG.md section4; V5/PREREG.md:129-133 |
| Zero source dispatch | Must demonstrate delivered/no-ready return without any new frozen-source write before authorized execution | V5/PREREG.md:94-98 |
| Reopening | Existing provider coordinate is no-replay; fresh path support is a launch condition | V5/PREREG.md:191 |
| Source/guard preservation | Historical observations, guarded role vocabulary and four reading dispositions retained | V5/PREREG.md:173-179; obligations.json |

V5 expands to docs/design/loop-prereg-draft-2026-09-14/v5. Approval of the current offline engineering task supplies no executable L004 registration. The next owner decision is F003 PLAN and its declared departures, followed by F003's own authorized receipt and eventual L004/v6 minting decisions.
