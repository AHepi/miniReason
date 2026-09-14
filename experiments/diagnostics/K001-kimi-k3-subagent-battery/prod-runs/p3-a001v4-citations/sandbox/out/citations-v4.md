# FW5 line-citation verification of staging/STAGING-v4.md

Source: `docs/sources/FW5-explanatory-construction.md`, sha256 `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` — **verified by computation before anything else; identical to the designated sha256.**
Source has 1503 newline-split segments.

Extraction regex: `(?:FW5)?+:(\d{2,4})(?:[-\u2013](\d{2,4}))?(?:\s*s(\d+)(?:-s?(\d+))?)?`
Context filter: matches preceded by `.md`, `.json`, `.py`, `.toml`, `PLAN` or `SKILL` (allowing a trailing backtick/asterisk/paren) are file:line references to other documents and are excluded.
Quoted fragments (straight/typographic quotes, backticks, `\(...\)` LaTeX, >= 12 characters) on each staging line are assigned to the citation whose target contains them where identifiable, otherwise to the nearest citation on the line. Ellipses inside a quote split the fragment into separately-tested parts. `s1`-style suffixes name a numbered sentence of the cited line.

Total citations checked: **491**; distinct cited source lines: **198**.

## Summary
- citations: 491
- CORRECT: 39
- CORRECT IN SUBSTANCE: 26
- WRONG: 29
- NO-QUOTE-TO-CHECK: 394
- REVERSED-RANGE: 0
- OUT-OF-RANGE: 3

**WRONG citations:**
- staging line 115: `FW5:228` (target 228) — fragment '\\(\\mathcal E\\)' not in cited target; cited line 228 starts: 'This is a substantive proposal about explanation, not a logical consequence of realism alone. Its strongest claim is tha'; found at source line(s) [167, 172, 217, 616, 620]
- staging line 141: `:228` (target 228) — fragment '\\(\\operatorname{Account}(c,p_c)\\)' not in cited target; cited line 228 starts: 'This is a substantive proposal about explanation, not a logical consequence of realism alone. Its strongest claim is tha'; found at source line(s) [831]
- staging line 145: `FW5:1192` (target 1192) — fragment ', and says it' not in cited target; cited line 1192 starts: 'The **base class** \\(\\mathsf{FW5}\\) consists of interpretations supplying the data above, respecting their typing, and s'; not found anywhere in source
- staging line 147: `FW5:1192` (target 1192) — fragment '\\(\\mathcal E\\)' not in cited target; cited line 1192 starts: 'The **base class** \\(\\mathsf{FW5}\\) consists of interpretations supplying the data above, respecting their typing, and s'; found at source line(s) [167, 172, 217, 616, 620]
- staging line 160: `:947` (target 947) — fragment '## The retention fixed point' not in cited target; cited line 947 starts: '\\tag{CT2}'; found at source line(s) [941]
- staging line 203: `:86` (target 86) — fragment '\\(D=(V,(X_v),J,B,A,L,\\mathrm{role})\\)' not in cited target; cited line 86 starts: 'D=(V,(X_v)_{v\\in V},J,B,A,L,\\operatorname{role}).'; not found anywhere in source
- staging line 208: `:176 s5` (target 176 s5) — fragment '\\(\\lambda_w\\)' not in cited target; cited line 176 starts: 'More formally, the anchoring data include a port translation for each component, depending only on the ports of its anch'; not found anywhere in source
- staging line 209: `:154` (target 154) — fragment '\\(\\mathcal C\\)' not in cited target; cited line 154 starts: 'A grain fixes which structural distinctions count as differences for the attribution at issue. A genuine recoding is an '; found at source line(s) [120, 123, 179]
- staging line 216: `:617` (target 617) — fragment '\\(\\operatorname{Bearing}(c,z,p)\\iff\\operatorname{Account}(\\mathcal E_c,p_\\delta)' not in cited target; cited line 617 starts: '\\tag{K1}'; not found anywhere in source
- staging line 217: `:609` (target 609) — fragment '\\(z,\\delta,g\\)' not in cited target; cited line 609 starts: 'A criticism has a represented target \\(z\\), an alleged defect \\(\\delta\\), grounds \\(g\\), and a proposed connection from '; not found anywhere in source
- staging line 224: `:128-130` (target 128-130) — fragment '\\(\\operatorname{Ans}_p(a,b)=\\mathcal Q(D,a,b)\\)' not in cited target; cited line 128 starts: '\\operatorname{Ans}_p(a,b)'; not found anywhere in source
- staging line 224: `:125` (target 125) — fragment '\\(\\operatorname{Ans}_E=\\mathcal Q(E,\\cdot,\\cdot)\\)' not in cited target; cited line 125 starts: 'The query operator \\(\\mathcal Q\\) is a specified set-theoretic operation on the relevant organization, its solutions, an'; not found anywhere in source
- staging line 291: `:123` (target 123) — fragment 'Weakens the claim that falling recurrence would confirm c1 and rising recurrence' not in cited target; cited line 123 starts: 'The target is \\(D\\). The scope \\(\\Sigma\\subseteq A\\times B\\) fixes which edits and boundary conditions are in the claim.'; not found anywhere in source | fragment 'quoted verbatim from the record' not in cited target; cited line 123 starts: 'The target is \\(D\\). The scope \\(\\Sigma\\subseteq A\\times B\\) fixes which edits and boundary conditions are in the claim.'; not found anywhere in source
- staging line 345: `:123` (target 123) — fragment 'bridge-strained' not in cited target; cited line 123 starts: 'The target is \\(D\\). The scope \\(\\Sigma\\subseteq A\\times B\\) fixes which edits and boundary conditions are in the claim.'; not found anywhere in source
- staging line 442: `:617` (target 617) — fragment '\\(\\operatorname{Account}(c,p_c)\\)' not in cited target; cited line 617 starts: '\\tag{K1}'; found at source line(s) [831]
- staging line 558: `:170` (target 170) — fragment '\\(\\tau,\\sigma\\)' not in cited target; cited line 170 starts: 'The map \\(\\pi\\) sends target valuations in the stated scope to explanatory valuations. It may be many-to-one. The maps \\'; found at source line(s) [167]
- staging line 617: `:125` (target 125) — fragment '\\(\\operatorname{Ans}_p(a,b)=\\mathcal Q(D,a,b)\\)' not in cited target; cited line 125 starts: 'The query operator \\(\\mathcal Q\\) is a specified set-theoretic operation on the relevant organization, its solutions, an'; not found anywhere in source
- staging line 626: `:205` (target 205) — fragment '\\(\\operatorname{Ans}_E(\\tau(a),\\sigma(b))\\)' not in cited target; cited line 205 starts: '\\tag{A}'; found at source line(s) [202]
- staging line 666: `:210 s1` (target 210 s1) — fragment '\\(\\operatorname{Ans}_E\\)' not in cited target; cited line 210 starts: '**Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent b'; found at source line(s) [162, 202]
- staging line 687: `:176` (target 176) — fragment "neither does any endpoint-level abstraction of FW5's own discriminating pair" not in cited target; cited line 176 starts: 'More formally, the anchoring data include a port translation for each component, depending only on the ports of its anch'; not found anywhere in source
- staging line 740: `:212 s3` (target 212 s3) — fragment '\\(\\forall x(\\text{could-matter}(x)\\to\\text{excluded}(x))\\)' not in cited target; cited line 212 starts: '**Non-vacuity.** The baseline organization has a compatible state or history. A claim of impossibility may correctly ass'; not found anywhere in source
- staging line 794: `:1372` (target 1372) — fragment 'possible counterexample' not in cited target; cited line 1372 starts: 'The explicit representation interpretation is not eliminated. If the fidelity and integration conditions admit a system '; not found anywhere in source
- staging line 797: `:1372` (target 1372) — fragment 'Representation and apparent reason use' not in cited target; cited line 1372 starts: 'The explicit representation interpretation is not eliminated. If the fidelity and integration conditions admit a system '; found at source line(s) [1370]
- staging line 799: `:1370` (target 1370) — fragment 'FW5-research-plan-decision.md' not in cited target; cited line 1370 starts: '## Representation and apparent reason use'; not found anywhere in source
- staging line 847: `:896` (target 896) — fragment '\\(\\operatorname{Bearing}(c,z,p)\\)' not in cited target; cited line 896 starts: 'states that a reason bears on a work in an aesthetic respect. \\(\\mathcal Rsn\\) is a set of reason contents; \\(\\mathcal V'; found at source line(s) [614]
- staging line 905: `:170` (target 170) — fragment '\\(\\mathcal E_c\\)' not in cited target; cited line 170 starts: 'The map \\(\\pi\\) sends target valuations in the stated scope to explanatory valuations. It may be many-to-one. The maps \\'; found at source line(s) [616, 620]
- staging line 1026: `:176 s3` (target 176 s3) — fragment '\\(\\mathcal E_c\\)' not in cited target; cited line 176 starts: 'More formally, the anchoring data include a port translation for each component, depending only on the ports of its anch'; found at source line(s) [616, 620]
- staging line 1137: `:1206` (target 1206) — fragment 'account#c1-c3' not in cited target; cited line 1206 starts: 'The result does not apply to arbitrary compression, loss of event identity, a changed boundary, or a coarsening that ide'; not found anywhere in source
- staging line 1138: `:1202` (target 1202) — fragment 'the stipulated bijections' not in cited target; cited line 1202 starts: 'Suppose all carriers, component relations, role bindings, maps, histories, question contracts, and attribution indices a'; found at source line(s) [1206]

**OUT-OF-RANGE:**
- staging line 1335: `:58` — sentence index beyond line length
- staging line 1336: `:58` — sentence index beyond line length
- staging line 1377: `:14` — sentence index beyond line length

Cited source lines that are blank (cited singly or inside a cited range): :175, :200, :207, :643, :745, :788, :799, :801, :990, :996, :998, :1000, :1004, :1006, :1008, :1010, :1012, :1209, :1211, :1217, :1257, :1259, :1337, :1339, :1341, :1343, :1363, :1385
Ranges whose end precedes start: none

## Table

| staging line | citation | target | verdict | note |
|---|---|---|---|---|
| 50 | `FW5:831` | 831 | NO-QUOTE-TO-CHECK |  |
| 81 | `FW5:208` | 208 | NO-QUOTE-TO-CHECK |  |
| 83 | `FW5:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 83 | `:188` | 188 | NO-QUOTE-TO-CHECK |  |
| 83 | `:174` | 174 | NO-QUOTE-TO-CHECK |  |
| 83 | `:170` | 170 | NO-QUOTE-TO-CHECK |  |
| 83 | `:244` | 244 | NO-QUOTE-TO-CHECK |  |
| 84 | `FW5:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 84 | `:188` | 188 | NO-QUOTE-TO-CHECK |  |
| 84 | `:174` | 174 | NO-QUOTE-TO-CHECK |  |
| 84 | `:170` | 170 | NO-QUOTE-TO-CHECK |  |
| 84 | `:244` | 244 | NO-QUOTE-TO-CHECK |  |
| 102 | `FW5:172` | 172 | NO-QUOTE-TO-CHECK |  |
| 104 | `:167` | 167 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\mathcal E=(E,p,\\pi,\\tau,\\sigma,\\lambda)\\)': markdown emphasis / LaTeX delimiters / line label |
| 105 | `:170` | 170 | NO-QUOTE-TO-CHECK |  |
| 105 | `:174-176` | 174-176 | NO-QUOTE-TO-CHECK |  |
| 106 | `:185` | 185 | NO-QUOTE-TO-CHECK |  |
| 106 | `:194` | 194 | NO-QUOTE-TO-CHECK |  |
| 106 | `:188` | 188 | NO-QUOTE-TO-CHECK |  |
| 107 | `:205` | 205 | NO-QUOTE-TO-CHECK |  |
| 107 | `:208` | 208 | NO-QUOTE-TO-CHECK |  |
| 107 | `:210` | 210 | NO-QUOTE-TO-CHECK |  |
| 108 | `:212` | 212 | NO-QUOTE-TO-CHECK |  |
| 108 | `:223` | 223 | NO-QUOTE-TO-CHECK |  |
| 110 | `FW5:226` | 226 | NO-QUOTE-TO-CHECK |  |
| 111 | `FW5:226` | 226 | NO-QUOTE-TO-CHECK |  |
| 112 | `FW5:228` | 228 | NO-QUOTE-TO-CHECK |  |
| 113 | `FW5:228` | 228 | NO-QUOTE-TO-CHECK |  |
| 114 | `FW5:228` | 228 | NO-QUOTE-TO-CHECK |  |
| 115 | `FW5:228` | 228 | WRONG | fragment '\\(\\mathcal E\\)' not in cited target; cited line 228 starts: 'This is a substantive proposal about explanation, not a logical consequence of realism alone. Its strongest claim is tha'; found at source line(s) [167, 172, 217, 616, 620] |
| 116 | `:617` | 617 | NO-QUOTE-TO-CHECK |  |
| 116 | `:613-618` | 613-618 | NO-QUOTE-TO-CHECK |  |
| 117 | `FW5:831` | 831 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\operatorname{Account}(c,p_c)\\)': markdown emphasis / LaTeX delimiters / line label |
| 119 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 120 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 134 | `FW5:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 135 | `FW5:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 136 | `FW5:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 137 | `FW5:1502` | 1502 | NO-QUOTE-TO-CHECK |  |
| 138 | `FW5:1502` | 1502 | NO-QUOTE-TO-CHECK |  |
| 140 | `:228` | 228 | NO-QUOTE-TO-CHECK |  |
| 141 | `:228` | 228 | WRONG | fragment '\\(\\operatorname{Account}(c,p_c)\\)' not in cited target; cited line 228 starts: 'This is a substantive proposal about explanation, not a logical consequence of realism alone. Its strongest claim is tha'; found at source line(s) [831] |
| 142 | `:831` | 831 | NO-QUOTE-TO-CHECK |  |
| 143 | `FW5:1192` | 1192 | CORRECT |  |
| 144 | `FW5:1192` | 1192 | NO-QUOTE-TO-CHECK |  |
| 145 | `FW5:1192` | 1192 | WRONG | fragment ', and says it' not in cited target; cited line 1192 starts: 'The **base class** \\(\\mathsf{FW5}\\) consists of interpretations supplying the data above, respecting their typing, and s'; not found anywhere in source |
| 146 | `FW5:1192` | 1192 | NO-QUOTE-TO-CHECK |  |
| 147 | `FW5:1192` | 1192 | WRONG | fragment '\\(\\mathcal E\\)' not in cited target; cited line 1192 starts: 'The **base class** \\(\\mathsf{FW5}\\) consists of interpretations supplying the data above, respecting their typing, and s'; found at source line(s) [167, 172, 217, 616, 620] |
| 148 | `FW5:1192` | 1192 | CORRECT |  |
| 149 | `:1192` | 1192 | NO-QUOTE-TO-CHECK |  |
| 154 | `:1390` | 1390 | NO-QUOTE-TO-CHECK |  |
| 154 | `:1390` | 1390 | NO-QUOTE-TO-CHECK |  |
| 157 | `:306` | 306 | NO-QUOTE-TO-CHECK |  |
| 158 | `:315` | 315 | NO-QUOTE-TO-CHECK |  |
| 158 | `:296` | 296 | NO-QUOTE-TO-CHECK |  |
| 158 | `:429` | 429 | NO-QUOTE-TO-CHECK |  |
| 158 | `:497` | 497 | NO-QUOTE-TO-CHECK |  |
| 159 | `:582` | 582 | NO-QUOTE-TO-CHECK |  |
| 159 | `:947` | 947 | NO-QUOTE-TO-CHECK |  |
| 159 | `:950` | 950 | NO-QUOTE-TO-CHECK |  |
| 159 | `:952` | 952 | NO-QUOTE-TO-CHECK |  |
| 159 | `:941` | 941 | NO-QUOTE-TO-CHECK |  |
| 160 | `:947` | 947 | WRONG | fragment '## The retention fixed point' not in cited target; cited line 947 starts: '\\tag{CT2}'; found at source line(s) [941] |
| 161 | `:945-948` | 945-948 | NO-QUOTE-TO-CHECK |  |
| 162 | `:950` | 950 | NO-QUOTE-TO-CHECK |  |
| 162 | `:952` | 952 | NO-QUOTE-TO-CHECK |  |
| 164 | `:1390` | 1390 | NO-QUOTE-TO-CHECK |  |
| 165 | `:1202` | 1202 | NO-QUOTE-TO-CHECK |  |
| 165 | `:1204` | 1204 | NO-QUOTE-TO-CHECK |  |
| 166 | `:1206` | 1206 | NO-QUOTE-TO-CHECK |  |
| 166 | `:1208` | 1208 | NO-QUOTE-TO-CHECK |  |
| 166 | `:1210-1218` | 1210-1218 | NO-QUOTE-TO-CHECK |  |
| 167 | `:1220` | 1220 | NO-QUOTE-TO-CHECK |  |
| 167 | `:1222` | 1222 | NO-QUOTE-TO-CHECK |  |
| 167 | `:1224` | 1224 | NO-QUOTE-TO-CHECK |  |
| 168 | `:1390` | 1390 | NO-QUOTE-TO-CHECK |  |
| 169 | `:1390` | 1390 | NO-QUOTE-TO-CHECK |  |
| 172 | `:1384-1386` | 1384-1386 | NO-QUOTE-TO-CHECK |  |
| 172 | `:902` | 902 | CORRECT |  |
| 173 | `:1384-1386` | 1384-1386 | NO-QUOTE-TO-CHECK |  |
| 173 | `:902` | 902 | NO-QUOTE-TO-CHECK |  |
| 176 | `:893` | 893 | NO-QUOTE-TO-CHECK |  |
| 176 | `:896` | 896 | NO-QUOTE-TO-CHECK |  |
| 176 | `:896` | 896 | NO-QUOTE-TO-CHECK |  |
| 177 | `:893` | 893 | NO-QUOTE-TO-CHECK |  |
| 177 | `:896` | 896 | NO-QUOTE-TO-CHECK |  |
| 177 | `:896` | 896 | NO-QUOTE-TO-CHECK |  |
| 191 | `:85` | 85 | NO-QUOTE-TO-CHECK |  |
| 191 | `:86` | 86 | NO-QUOTE-TO-CHECK |  |
| 191 | `:106` | 106 | NO-QUOTE-TO-CHECK |  |
| 191 | `:117` | 117 | NO-QUOTE-TO-CHECK |  |
| 191 | `:120` | 120 | NO-QUOTE-TO-CHECK |  |
| 192 | `:131` | 131 | NO-QUOTE-TO-CHECK |  |
| 192 | `:166` | 166 | NO-QUOTE-TO-CHECK |  |
| 192 | `:167` | 167 | NO-QUOTE-TO-CHECK |  |
| 192 | `:617` | 617 | NO-QUOTE-TO-CHECK |  |
| 193 | `:1210-1218` | 1210-1218 | NO-QUOTE-TO-CHECK |  |
| 194 | `:738-746` | 738-746 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(d\\equiv_\\ell c\\)': markdown emphasis / LaTeX delimiters / line label |
| 194 | `:742` | 742 | NO-QUOTE-TO-CHECK |  |
| 194 | `:743` | 743 | NO-QUOTE-TO-CHECK |  |
| 195 | `:746` | 746 | NO-QUOTE-TO-CHECK |  |
| 195 | `:642-651` | 642-651 | NO-QUOTE-TO-CHECK |  |
| 195 | `:638` | 638 | NO-QUOTE-TO-CHECK |  |
| 196 | `:642` | 642 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\operatorname{Live}_j\\)': markdown emphasis / LaTeX delimiters / line label |
| 196 | `:650` | 650 | NO-QUOTE-TO-CHECK |  |
| 197 | `:644-650` | 644-650 | NO-QUOTE-TO-CHECK |  |
| 198 | `:859` | 859 | CORRECT |  |
| 198 | `:857` | 857 | NO-QUOTE-TO-CHECK |  |
| 199 | `:859` | 859 | NO-QUOTE-TO-CHECK |  |
| 199 | `:857` | 857 | NO-QUOTE-TO-CHECK |  |
| 203 | `:86` | 86 | WRONG | fragment '\\(D=(V,(X_v),J,B,A,L,\\mathrm{role})\\)' not in cited target; cited line 86 starts: 'D=(V,(X_v)_{v\\in V},J,B,A,L,\\operatorname{role}).'; not found anywhere in source |
| 203 | `:106` | 106 | NO-QUOTE-TO-CHECK |  |
| 204 | `:120` | 120 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(p=(D,\\Sigma,b_0,\\kappa,\\mathcal C,\\mathcal Q,O_p)\\)': markdown emphasis / LaTeX delimiters / line label |
| 204 | `:123` | 123 | NO-QUOTE-TO-CHECK |  |
| 204 | `:125` | 125 | NO-QUOTE-TO-CHECK |  |
| 204 | `:131` | 131 | NO-QUOTE-TO-CHECK |  |
| 205 | `:123` | 123 | CORRECT |  |
| 206 | `:123` | 123 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\mathcal C\\)': markdown emphasis / LaTeX delimiters / line label; 'distinctions **material to that question**': markdown emphasis / LaTeX delimiters / line label |
| 207 | `:167` | 167 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\pi,\\tau,\\sigma,\\lambda\\)': markdown emphasis / LaTeX delimiters / line label |
| 207 | `:170` | 170 | CORRECT IN SUBSTANCE | found only after normalisation: ':170 Their meanings are held fixed across the comparison': markdown emphasis / LaTeX delimiters / line label |
| 207 | `:170` | 170 | NO-QUOTE-TO-CHECK |  |
| 208 | `:176` | 176 | CORRECT |  |
| 208 | `:176 s1` | 176 s1 | NO-QUOTE-TO-CHECK |  |
| 208 | `:176 s5` | 176 s5 | WRONG | fragment '\\(\\lambda_w\\)' not in cited target; cited line 176 starts: 'More formally, the anchoring data include a port translation for each component, depending only on the ports of its anch'; not found anywhere in source |
| 208 | `:174` | 174 | NO-QUOTE-TO-CHECK |  |
| 209 | `:154` | 154 | WRONG | fragment '\\(\\mathcal C\\)' not in cited target; cited line 154 starts: 'A grain fixes which structural distinctions count as differences for the attribution at issue. A genuine recoding is an '; found at source line(s) [120, 123, 179] |
| 209 | `:154` | 154 | NO-QUOTE-TO-CHECK |  |
| 210 | `:162` | 162 | CORRECT |  |
| 211 | `:185` | 185 | NO-QUOTE-TO-CHECK |  |
| 211 | `:194` | 194 | NO-QUOTE-TO-CHECK |  |
| 211 | `:205` | 205 | NO-QUOTE-TO-CHECK |  |
| 211 | `:179` | 179 | CORRECT |  |
| 211 | `:199` | 199 | NO-QUOTE-TO-CHECK |  |
| 211 | `:188` | 188 | CORRECT IN SUBSTANCE | found only after normalisation: 'every composition **for which a claim is made**': markdown emphasis / LaTeX delimiters / line label |
| 211 | `:208` | 208 | CORRECT |  |
| 212 | `:210` | 210 | NO-QUOTE-TO-CHECK |  |
| 212 | `:212` | 212 | CORRECT |  |
| 212 | `:210` | 210 | NO-QUOTE-TO-CHECK |  |
| 212 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 212 | `:210` | 210 | CORRECT |  |
| 212 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 213 | `:212 s1-s2` | 212 s1-s2 | CORRECT |  |
| 214 | `:149` | 149 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\operatorname{Rep}_{\\beta,\\ell}\\)': markdown emphasis / LaTeX delimiters / line label |
| 214 | `:148-150` | 148-150 | NO-QUOTE-TO-CHECK |  |
| 214 | `:152` | 152 | NO-QUOTE-TO-CHECK |  |
| 214 | `:156` | 156 | CORRECT IN SUBSTANCE | found only after normalisation: ':156 The representation relation is an explicit semantic pri': markdown emphasis / LaTeX delimiters / line label |
| 214 | `:156` | 156 | NO-QUOTE-TO-CHECK |  |
| 215 | `:742` | 742 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(d\\equiv_\\ell c\\)': markdown emphasis / LaTeX delimiters / line label |
| 215 | `:743` | 743 | NO-QUOTE-TO-CHECK |  |
| 215 | `:746` | 746 | CORRECT IN SUBSTANCE | found only after normalisation: ':746 The equivalence is structural at the stated grain, not ': markdown emphasis / LaTeX delimiters / line label |
| 215 | `:746` | 746 | NO-QUOTE-TO-CHECK |  |
| 216 | `:617` | 617 | WRONG | fragment '\\(\\operatorname{Bearing}(c,z,p)\\iff\\operatorname{Account}(\\mathcal E_c,p_\\delta)' not in cited target; cited line 617 starts: '\\tag{K1}'; not found anywhere in source |
| 216 | `:613-618` | 613-618 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\mathcal E_c\\)': markdown emphasis / LaTeX delimiters / line label |
| 216 | `:620` | 620 | CORRECT |  |
| 216 | `:620 s2` | 620 s2 | NO-QUOTE-TO-CHECK |  |
| 217 | `:609` | 609 | WRONG | fragment '\\(z,\\delta,g\\)' not in cited target; cited line 609 starts: 'A criticism has a represented target \\(z\\), an alleged defect \\(\\delta\\), grounds \\(g\\), and a proposed connection from '; not found anywhere in source |
| 217 | `:609` | 609 | NO-QUOTE-TO-CHECK |  |
| 218 | `:601` | 601 | CORRECT |  |
| 219 | `:628` | 628 | CORRECT IN SUBSTANCE | found only after normalisation: ':628 The map must preserve internal role bindings, not merel': markdown emphasis / LaTeX delimiters / line label |
| 219 | `:630` | 630 | NO-QUOTE-TO-CHECK |  |
| 219 | `:628` | 628 | NO-QUOTE-TO-CHECK |  |
| 220 | `:638` | 638 | NO-QUOTE-TO-CHECK |  |
| 220 | `:642` | 642 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\operatorname{Live}_j\\)': markdown emphasis / LaTeX delimiters / line label |
| 220 | `:650` | 650 | NO-QUOTE-TO-CHECK |  |
| 220 | `FW5:640` | 640 | CORRECT |  |
| 221 | `:787-800` | 787-800 | CORRECT |  |
| 222 | `:1210-1218` | 1210-1218 | NO-QUOTE-TO-CHECK |  |
| 222 | `:1220` | 1220 | NO-QUOTE-TO-CHECK |  |
| 222 | `:1224` | 1224 | CORRECT IN SUBSTANCE | found only after normalisation: ':1224 The theorem identifies missing information in a projec': markdown emphasis / LaTeX delimiters / line label |
| 222 | `:1218` | 1218 | NO-QUOTE-TO-CHECK |  |
| 222 | `:1222` | 1222 | NO-QUOTE-TO-CHECK |  |
| 222 | `:1224` | 1224 | NO-QUOTE-TO-CHECK |  |
| 223 | `:620 s2` | 620 s2 | NO-QUOTE-TO-CHECK |  |
| 223 | `:123` | 123 | NO-QUOTE-TO-CHECK |  |
| 224 | `:162` | 162 | CORRECT IN SUBSTANCE | found only after normalisation: 'An explanatory candidate for \\(p\\) **supplies** an organizat': markdown emphasis / LaTeX delimiters / line label |
| 224 | `:128-130` | 128-130 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\mathcal Q\\)': markdown emphasis / LaTeX delimiters / line label; '\\(\\mathcal Q\\)': markdown emphasis / LaTeX delimiters / line label |
| 224 | `:125` | 125 | CORRECT |  |
| 224 | `:210 s1` | 210 s1 | CORRECT IN SUBSTANCE | found only after normalisation: 'The answer follows by evaluating **the anchored organization': markdown emphasis / LaTeX delimiters / line label |
| 224 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 224 | `:202` | 202 | NO-QUOTE-TO-CHECK |  |
| 224 | `:201-205` | 201-205 | NO-QUOTE-TO-CHECK |  |
| 224 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 224 | `:128-130` | 128-130 | WRONG | fragment '\\(\\operatorname{Ans}_p(a,b)=\\mathcal Q(D,a,b)\\)' not in cited target; cited line 128 starts: '\\operatorname{Ans}_p(a,b)'; not found anywhere in source |
| 224 | `:125` | 125 | WRONG | fragment '\\(\\operatorname{Ans}_E=\\mathcal Q(E,\\cdot,\\cdot)\\)' not in cited target; cited line 125 starts: 'The query operator \\(\\mathcal Q\\) is a specified set-theoretic operation on the relevant organization, its solutions, an'; not found anywhere in source |
| 224 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 224 | `:197` | 197 | CORRECT |  |
| 227 | `:989-991` | 989-991 | NO-QUOTE-TO-CHECK |  |
| 227 | `:995-1012` | 995-1012 | NO-QUOTE-TO-CHECK |  |
| 228 | `:989-991` | 989-991 | NO-QUOTE-TO-CHECK |  |
| 228 | `:995-1012` | 995-1012 | NO-QUOTE-TO-CHECK |  |
| 247 | `FW5:728` | 728 | NO-QUOTE-TO-CHECK |  |
| 248 | `FW5:728` | 728 | NO-QUOTE-TO-CHECK |  |
| 271 | `:609` | 609 | NO-QUOTE-TO-CHECK |  |
| 275 | `:609` | 609 | NO-QUOTE-TO-CHECK |  |
| 289 | `FW5:140` | 140 | CORRECT |  |
| 291 | `:123` | 123 | WRONG | fragment 'Weakens the claim that falling recurrence would confirm c1 and rising recurrence' not in cited target; cited line 123 starts: 'The target is \\(D\\). The scope \\(\\Sigma\\subseteq A\\times B\\) fixes which edits and boundary conditions are in the claim.'; not found anywhere in source \| fragment 'quoted verbatim from the record' not in cited target; cited line 123 starts: 'The target is \\(D\\). The scope \\(\\Sigma\\subseteq A\\times B\\) fixes which edits and boundary conditions are in the claim.'; not found anywhere in source |
| 293 | `FW5:210` | 210 | NO-QUOTE-TO-CHECK |  |
| 293 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 293 | `FW5:630` | 630 | NO-QUOTE-TO-CHECK |  |
| 294 | `FW5:630` | 630 | NO-QUOTE-TO-CHECK |  |
| 327 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 327 | `FW5:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 328 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 328 | `FW5:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 332 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 333 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 334 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 335 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 336 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 340 | `:123` | 123 | NO-QUOTE-TO-CHECK |  |
| 341 | `:123` | 123 | NO-QUOTE-TO-CHECK |  |
| 342 | `:123` | 123 | NO-QUOTE-TO-CHECK |  |
| 343 | `:123` | 123 | NO-QUOTE-TO-CHECK |  |
| 343 | `:609` | 609 | NO-QUOTE-TO-CHECK |  |
| 343 | `:212 s2` | 212 s2 | CORRECT |  |
| 344 | `:123` | 123 | NO-QUOTE-TO-CHECK |  |
| 344 | `:609` | 609 | CORRECT |  |
| 345 | `:123` | 123 | WRONG | fragment 'bridge-strained' not in cited target; cited line 123 starts: 'The target is \\(D\\). The scope \\(\\Sigma\\subseteq A\\times B\\) fixes which edits and boundary conditions are in the claim.'; not found anywhere in source |
| 417 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 418 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 419 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 420 | `:37` | 37 | NO-QUOTE-TO-CHECK |  |
| 426 | `:226` | 226 | NO-QUOTE-TO-CHECK |  |
| 426 | `:226` | 226 | NO-QUOTE-TO-CHECK |  |
| 432 | `:228` | 228 | NO-QUOTE-TO-CHECK |  |
| 435 | `:226` | 226 | NO-QUOTE-TO-CHECK |  |
| 436 | `:226` | 226 | NO-QUOTE-TO-CHECK |  |
| 441 | `:617` | 617 | NO-QUOTE-TO-CHECK |  |
| 442 | `:617` | 617 | WRONG | fragment '\\(\\operatorname{Account}(c,p_c)\\)' not in cited target; cited line 617 starts: '\\tag{K1}'; found at source line(s) [831] |
| 443 | `:831` | 831 | NO-QUOTE-TO-CHECK |  |
| 444 | `:1202` | 1202 | NO-QUOTE-TO-CHECK |  |
| 444 | `:1210-1218` | 1210-1218 | NO-QUOTE-TO-CHECK |  |
| 445 | `:947` | 947 | NO-QUOTE-TO-CHECK |  |
| 445 | `:950` | 950 | NO-QUOTE-TO-CHECK |  |
| 445 | `:952` | 952 | NO-QUOTE-TO-CHECK |  |
| 447 | `:228` | 228 | NO-QUOTE-TO-CHECK |  |
| 448 | `:831` | 831 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\operatorname{Account}(c,p_c)\\)': markdown emphasis / LaTeX delimiters / line label |
| 449 | `:831` | 831 | NO-QUOTE-TO-CHECK |  |
| 450 | `:831` | 831 | NO-QUOTE-TO-CHECK |  |
| 451 | `:1192` | 1192 | CORRECT |  |
| 451 | `FW5:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 452 | `:1192` | 1192 | NO-QUOTE-TO-CHECK |  |
| 452 | `FW5:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 454 | `FW5:1392` | 1392 | NO-QUOTE-TO-CHECK |  |
| 455 | `FW5:1392` | 1392 | NO-QUOTE-TO-CHECK |  |
| 456 | `FW5:688` | 688 | NO-QUOTE-TO-CHECK |  |
| 457 | `FW5:1404` | 1404 | NO-QUOTE-TO-CHECK |  |
| 458 | `FW5:1404` | 1404 | NO-QUOTE-TO-CHECK |  |
| 460 | `:1336-1344` | 1336-1344 | NO-QUOTE-TO-CHECK |  |
| 461 | `:1342` | 1342 | NO-QUOTE-TO-CHECK |  |
| 462 | `:1342` | 1342 | NO-QUOTE-TO-CHECK |  |
| 477 | `FW5:1392` | 1392 | NO-QUOTE-TO-CHECK |  |
| 494 | `FW5:688` | 688 | NO-QUOTE-TO-CHECK |  |
| 516 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 519 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 526 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 526 | `:125` | 125 | NO-QUOTE-TO-CHECK |  |
| 526 | `:128-130` | 128-130 | NO-QUOTE-TO-CHECK |  |
| 526 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 527 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 527 | `:125` | 125 | NO-QUOTE-TO-CHECK |  |
| 527 | `:128-130` | 128-130 | NO-QUOTE-TO-CHECK |  |
| 527 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 528 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 528 | `:125` | 125 | NO-QUOTE-TO-CHECK |  |
| 528 | `:128-130` | 128-130 | NO-QUOTE-TO-CHECK |  |
| 528 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 529 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 529 | `:125` | 125 | NO-QUOTE-TO-CHECK |  |
| 529 | `:128-130` | 128-130 | NO-QUOTE-TO-CHECK |  |
| 529 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 530 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 530 | `:125` | 125 | NO-QUOTE-TO-CHECK |  |
| 530 | `:128-130` | 128-130 | NO-QUOTE-TO-CHECK |  |
| 530 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 531 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 531 | `:125` | 125 | NO-QUOTE-TO-CHECK |  |
| 531 | `:128-130` | 128-130 | NO-QUOTE-TO-CHECK |  |
| 531 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 532 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 532 | `:125` | 125 | NO-QUOTE-TO-CHECK |  |
| 532 | `:128-130` | 128-130 | NO-QUOTE-TO-CHECK |  |
| 532 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 536 | `:1222` | 1222 | NO-QUOTE-TO-CHECK |  |
| 537 | `:1402` | 1402 | NO-QUOTE-TO-CHECK |  |
| 538 | `:1402` | 1402 | NO-QUOTE-TO-CHECK |  |
| 539 | `:1402` | 1402 | NO-QUOTE-TO-CHECK |  |
| 553 | `:210` | 210 | NO-QUOTE-TO-CHECK |  |
| 554 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 558 | `:170` | 170 | WRONG | fragment '\\(\\tau,\\sigma\\)' not in cited target; cited line 170 starts: 'The map \\(\\pi\\) sends target valuations in the stated scope to explanatory valuations. It may be many-to-one. The maps \\'; found at source line(s) [167] |
| 567 | `:1402` | 1402 | NO-QUOTE-TO-CHECK |  |
| 568 | `:208` | 208 | CORRECT |  |
| 574 | `FW5:236` | 236 | NO-QUOTE-TO-CHECK |  |
| 577 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 586 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 589 | `:1208-1218` | 1208-1218 | NO-QUOTE-TO-CHECK |  |
| 590 | `:1218` | 1218 | NO-QUOTE-TO-CHECK |  |
| 594 | `:1214-1215` | 1214-1215 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(M_1\\not\\models\\phi\\)': markdown emphasis / LaTeX delimiters / line label |
| 596 | `:1224` | 1224 | NO-QUOTE-TO-CHECK |  |
| 598 | `:1222` | 1222 | NO-QUOTE-TO-CHECK |  |
| 599 | `:1222` | 1222 | NO-QUOTE-TO-CHECK |  |
| 613 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 613 | `:202` | 202 | NO-QUOTE-TO-CHECK |  |
| 613 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 614 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 614 | `:202` | 202 | NO-QUOTE-TO-CHECK |  |
| 614 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 615 | `:162` | 162 | CORRECT |  |
| 615 | `:202` | 202 | NO-QUOTE-TO-CHECK |  |
| 615 | `:162` | 162 | NO-QUOTE-TO-CHECK |  |
| 616 | `:128-130` | 128-130 | NO-QUOTE-TO-CHECK |  |
| 617 | `:125` | 125 | WRONG | fragment '\\(\\operatorname{Ans}_p(a,b)=\\mathcal Q(D,a,b)\\)' not in cited target; cited line 125 starts: 'The query operator \\(\\mathcal Q\\) is a specified set-theoretic operation on the relevant organization, its solutions, an'; not found anywhere in source |
| 623 | `:208` | 208 | NO-QUOTE-TO-CHECK |  |
| 626 | `:1402` | 1402 | NO-QUOTE-TO-CHECK |  |
| 626 | `:205` | 205 | WRONG | fragment '\\(\\operatorname{Ans}_E(\\tau(a),\\sigma(b))\\)' not in cited target; cited line 205 starts: '\\tag{A}'; found at source line(s) [202] |
| 628 | `:208` | 208 | NO-QUOTE-TO-CHECK |  |
| 630 | `:199-208` | 199-208 | NO-QUOTE-TO-CHECK |  |
| 632 | `:208` | 208 | NO-QUOTE-TO-CHECK |  |
| 638 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 645 | `:197` | 197 | CORRECT |  |
| 649 | `:210 s2` | 210 s2 | NO-QUOTE-TO-CHECK |  |
| 655 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 664 | `:236` | 236 | NO-QUOTE-TO-CHECK |  |
| 664 | `:208` | 208 | NO-QUOTE-TO-CHECK |  |
| 664 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 665 | `:208` | 208 | NO-QUOTE-TO-CHECK |  |
| 666 | `:210 s1` | 210 s1 | WRONG | fragment '\\(\\operatorname{Ans}_E\\)' not in cited target; cited line 210 starts: '**Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent b'; found at source line(s) [162, 202] |
| 666 | `:197` | 197 | NO-QUOTE-TO-CHECK |  |
| 670 | `:208` | 208 | NO-QUOTE-TO-CHECK |  |
| 684 | `:176` | 176 | NO-QUOTE-TO-CHECK |  |
| 685 | `:176` | 176 | NO-QUOTE-TO-CHECK |  |
| 686 | `:176` | 176 | NO-QUOTE-TO-CHECK |  |
| 687 | `:176` | 176 | WRONG | fragment "neither does any endpoint-level abstraction of FW5's own discriminating pair" not in cited target; cited line 176 starts: 'More formally, the anchoring data include a port translation for each component, depending only on the ports of its anch'; not found anywhere in source |
| 694 | `:176 s1` | 176 s1 | NO-QUOTE-TO-CHECK |  |
| 695 | `:176 s1` | 176 s1 | NO-QUOTE-TO-CHECK |  |
| 696 | `:176 s1` | 176 s1 | NO-QUOTE-TO-CHECK |  |
| 697 | `:176 s1` | 176 s1 | NO-QUOTE-TO-CHECK |  |
| 698 | `:176 s1` | 176 s1 | NO-QUOTE-TO-CHECK |  |
| 709 | `:176 s5` | 176 s5 | NO-QUOTE-TO-CHECK |  |
| 710 | `:176 s5` | 176 s5 | NO-QUOTE-TO-CHECK |  |
| 711 | `:176 s5` | 176 s5 | NO-QUOTE-TO-CHECK |  |
| 720 | `:174` | 174 | NO-QUOTE-TO-CHECK |  |
| 723 | `:176 s3` | 176 s3 | NO-QUOTE-TO-CHECK |  |
| 724 | `:1402` | 1402 | NO-QUOTE-TO-CHECK |  |
| 727 | `:185` | 185 | NO-QUOTE-TO-CHECK |  |
| 737 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 739 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 740 | `:212 s3` | 212 s3 | WRONG | fragment '\\(\\forall x(\\text{could-matter}(x)\\to\\text{excluded}(x))\\)' not in cited target; cited line 212 starts: '**Non-vacuity.** The baseline organization has a compatible state or history. A claim of impossibility may correctly ass'; not found anywhere in source |
| 741 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 742 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 743 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 750 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |
| 754 | `:210` | 210 | NO-QUOTE-TO-CHECK |  |
| 754 | `:212` | 212 | NO-QUOTE-TO-CHECK |  |
| 754 | `:208` | 208 | NO-QUOTE-TO-CHECK |  |
| 761 | `:859` | 859 | NO-QUOTE-TO-CHECK |  |
| 762 | `:859` | 859 | NO-QUOTE-TO-CHECK |  |
| 763 | `:859` | 859 | NO-QUOTE-TO-CHECK |  |
| 764 | `:244` | 244 | NO-QUOTE-TO-CHECK |  |
| 765 | `:244` | 244 | NO-QUOTE-TO-CHECK |  |
| 766 | `:244` | 244 | NO-QUOTE-TO-CHECK |  |
| 767 | `:244` | 244 | NO-QUOTE-TO-CHECK |  |
| 772 | `:188` | 188 | NO-QUOTE-TO-CHECK |  |
| 775 | `:174` | 174 | NO-QUOTE-TO-CHECK |  |
| 779 | `:170` | 170 | NO-QUOTE-TO-CHECK |  |
| 779 | `:244` | 244 | NO-QUOTE-TO-CHECK |  |
| 780 | `:170` | 170 | NO-QUOTE-TO-CHECK |  |
| 781 | `:244` | 244 | NO-QUOTE-TO-CHECK |  |
| 784 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 791 | `:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 791 | `:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 792 | `:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 792 | `:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 793 | `:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 793 | `:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 794 | `:1372` | 1372 | WRONG | fragment 'possible counterexample' not in cited target; cited line 1372 starts: 'The explicit representation interpretation is not eliminated. If the fidelity and integration conditions admit a system '; not found anywhere in source |
| 794 | `:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 795 | `:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 795 | `:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 797 | `:1372` | 1372 | WRONG | fragment 'Representation and apparent reason use' not in cited target; cited line 1372 starts: 'The explicit representation interpretation is not eliminated. If the fidelity and integration conditions admit a system '; found at source line(s) [1370] |
| 798 | `:1370` | 1370 | NO-QUOTE-TO-CHECK |  |
| 798 | `:1362` | 1362 | NO-QUOTE-TO-CHECK |  |
| 799 | `:1370` | 1370 | WRONG | fragment 'FW5-research-plan-decision.md' not in cited target; cited line 1370 starts: '## Representation and apparent reason use'; not found anywhere in source |
| 799 | `:1362` | 1362 | NO-QUOTE-TO-CHECK |  |
| 800 | `:1370` | 1370 | NO-QUOTE-TO-CHECK |  |
| 800 | `:1362` | 1362 | NO-QUOTE-TO-CHECK |  |
| 801 | `:1370` | 1370 | NO-QUOTE-TO-CHECK |  |
| 801 | `:1362` | 1362 | NO-QUOTE-TO-CHECK |  |
| 824 | `:617` | 617 | NO-QUOTE-TO-CHECK |  |
| 833 | `:800` | 800 | CORRECT |  |
| 834 | `:912` | 912 | CORRECT |  |
| 834 | `:1005` | 1005 | NO-QUOTE-TO-CHECK |  |
| 834 | `:1320` | 1320 | CORRECT |  |
| 835 | `:607` | 607 | NO-QUOTE-TO-CHECK |  |
| 835 | `:614` | 614 | NO-QUOTE-TO-CHECK |  |
| 835 | `:622` | 622 | NO-QUOTE-TO-CHECK |  |
| 835 | `:773` | 773 | NO-QUOTE-TO-CHECK |  |
| 836 | `:896` | 896 | NO-QUOTE-TO-CHECK |  |
| 836 | `:900` | 900 | NO-QUOTE-TO-CHECK |  |
| 836 | `:1182` | 1182 | NO-QUOTE-TO-CHECK |  |
| 836 | `:609` | 609 | NO-QUOTE-TO-CHECK |  |
| 836 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 837 | `:613-618` | 613-618 | NO-QUOTE-TO-CHECK |  |
| 838 | `:613-618` | 613-618 | NO-QUOTE-TO-CHECK |  |
| 842 | `:607` | 607 | CORRECT |  |
| 843 | `:609` | 609 | CORRECT |  |
| 844 | `:620` | 620 | CORRECT |  |
| 844 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 845 | `:622` | 622 | CORRECT |  |
| 846 | `:773` | 773 | CORRECT |  |
| 847 | `:893` | 893 | CORRECT IN SUBSTANCE | found only after normalisation: '\\(\\mathcal N\\subseteq A\\times K\\times\\mathcal Rsn\\times\\math': markdown emphasis / LaTeX delimiters / line label; '\\(\\mathcal N\\)': markdown emphasis / LaTeX delimiters / line label |
| 847 | `:896` | 896 | CORRECT IN SUBSTANCE | found only after normalisation: 'states that a reason **bears** on a work in an aesthetic res': markdown emphasis / LaTeX delimiters / line label |
| 847 | `:893` | 893 | NO-QUOTE-TO-CHECK |  |
| 847 | `:896` | 896 | WRONG | fragment '\\(\\operatorname{Bearing}(c,z,p)\\)' not in cited target; cited line 896 starts: 'states that a reason bears on a work in an aesthetic respect. \\(\\mathcal Rsn\\) is a set of reason contents; \\(\\mathcal V'; found at source line(s) [614] |
| 847 | `:896` | 896 | NO-QUOTE-TO-CHECK |  |
| 848 | `:900` | 900 | CORRECT IN SUBSTANCE | found only after normalisation: 'effects belong to \\(\\mathcal R\\), purposes to \\(G\\), **norma': markdown emphasis / LaTeX delimiters / line label |
| 849 | `:1182` | 1182 | CORRECT IN SUBSTANCE | found only after normalisation: '**Critical bearing is accounting for the specified defect qu': markdown emphasis / LaTeX delimiters / line label |
| 849 | `:1178` | 1178 | CORRECT |  |
| 851 | `:1182` | 1182 | NO-QUOTE-TO-CHECK |  |
| 852 | `:1182` | 1182 | NO-QUOTE-TO-CHECK |  |
| 853 | `:1182` | 1182 | NO-QUOTE-TO-CHECK |  |
| 854 | `:1182` | 1182 | CORRECT |  |
| 859 | `:1182` | 1182 | NO-QUOTE-TO-CHECK |  |
| 903 | `:1364` | 1364 | NO-QUOTE-TO-CHECK |  |
| 904 | `:170` | 170 | NO-QUOTE-TO-CHECK |  |
| 905 | `:170` | 170 | WRONG | fragment '\\(\\mathcal E_c\\)' not in cited target; cited line 170 starts: 'The map \\(\\pi\\) sends target valuations in the stated scope to explanatory valuations. It may be many-to-one. The maps \\'; found at source line(s) [616, 620] |
| 925 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 925 | `FW5:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1000 | `:620` | 620 | CORRECT |  |
| 1003 | `:1364` | 1364 | CORRECT |  |
| 1006 | `:620` | 620 | CORRECT |  |
| 1006 | `FW5:634` | 634 | CORRECT |  |
| 1026 | `:176 s3` | 176 s3 | WRONG | fragment '\\(\\mathcal E_c\\)' not in cited target; cited line 176 starts: 'More formally, the anchoring data include a port translation for each component, depending only on the ports of its anch'; found at source line(s) [616, 620] |
| 1046 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1099 | `FW5:640` | 640 | NO-QUOTE-TO-CHECK |  |
| 1100 | `FW5:640` | 640 | NO-QUOTE-TO-CHECK |  |
| 1101 | `FW5:640` | 640 | NO-QUOTE-TO-CHECK |  |
| 1133 | `FW5:1202` | 1202 | NO-QUOTE-TO-CHECK |  |
| 1133 | `:1202` | 1202 | NO-QUOTE-TO-CHECK |  |
| 1134 | `FW5:1202` | 1202 | NO-QUOTE-TO-CHECK |  |
| 1134 | `:1202` | 1202 | NO-QUOTE-TO-CHECK |  |
| 1135 | `FW5:1202` | 1202 | NO-QUOTE-TO-CHECK |  |
| 1135 | `:1202` | 1202 | NO-QUOTE-TO-CHECK |  |
| 1136 | `FW5:1202` | 1202 | NO-QUOTE-TO-CHECK |  |
| 1136 | `:1202` | 1202 | NO-QUOTE-TO-CHECK |  |
| 1137 | `:1206` | 1206 | WRONG | fragment 'account#c1-c3' not in cited target; cited line 1206 starts: 'The result does not apply to arbitrary compression, loss of event identity, a changed boundary, or a coarsening that ide'; not found anywhere in source |
| 1138 | `:1202` | 1202 | WRONG | fragment 'the stipulated bijections' not in cited target; cited line 1202 starts: 'Suppose all carriers, component relations, role bindings, maps, histories, question contracts, and attribution indices a'; found at source line(s) [1206] |
| 1152 | `FW5:849` | 849 | NO-QUOTE-TO-CHECK |  |
| 1152 | `:851` | 851 | NO-QUOTE-TO-CHECK |  |
| 1153 | `FW5:849` | 849 | NO-QUOTE-TO-CHECK |  |
| 1153 | `:851` | 851 | NO-QUOTE-TO-CHECK |  |
| 1155 | `FW5:851` | 851 | NO-QUOTE-TO-CHECK |  |
| 1159 | `:831` | 831 | NO-QUOTE-TO-CHECK |  |
| 1162 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1163 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1175 | `FW5:634` | 634 | NO-QUOTE-TO-CHECK |  |
| 1176 | `:743-745` | 743-745 | NO-QUOTE-TO-CHECK |  |
| 1177 | `:743-745` | 743-745 | NO-QUOTE-TO-CHECK |  |
| 1191 | `FW5:800` | 800 | NO-QUOTE-TO-CHECK |  |
| 1192 | `FW5:787-802` | 787-802 | NO-QUOTE-TO-CHECK |  |
| 1194 | `FW5:609` | 609 | NO-QUOTE-TO-CHECK |  |
| 1194 | `:622` | 622 | NO-QUOTE-TO-CHECK |  |
| 1196 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1196 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1209 | `FW5:1256-1260` | 1256-1260 | NO-QUOTE-TO-CHECK |  |
| 1211 | `FW5:688` | 688 | NO-QUOTE-TO-CHECK |  |
| 1211 | `FW5:1392` | 1392 | NO-QUOTE-TO-CHECK |  |
| 1211 | `FW5:1404` | 1404 | NO-QUOTE-TO-CHECK |  |
| 1212 | `:1336-1344` | 1336-1344 | NO-QUOTE-TO-CHECK |  |
| 1219 | `FW5:1368` | 1368 | NO-QUOTE-TO-CHECK |  |
| 1226 | `FW5:630` | 630 | NO-QUOTE-TO-CHECK |  |
| 1287 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1297 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1310 | `:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1335 | `:58` | 58 | OUT-OF-RANGE | sentence index beyond line length |
| 1336 | `:58` | 58 | OUT-OF-RANGE | sentence index beyond line length |
| 1377 | `:14` | 14 | OUT-OF-RANGE | sentence index beyond line length |
| 1423 | `FW5:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1426 | `FW5:1372` | 1372 | NO-QUOTE-TO-CHECK |  |
| 1426 | `:188` | 188 | NO-QUOTE-TO-CHECK |  |
| 1426 | `:174` | 174 | NO-QUOTE-TO-CHECK |  |
| 1426 | `:170` | 170 | NO-QUOTE-TO-CHECK |  |
| 1426 | `:244` | 244 | NO-QUOTE-TO-CHECK |  |
| 1426 | `FW5:208` | 208 | NO-QUOTE-TO-CHECK |  |
| 1440 | `FW5:620` | 620 | NO-QUOTE-TO-CHECK |  |
| 1444 | `FW5:1362-1364` | 1362-1364 | NO-QUOTE-TO-CHECK |  |
| 1445 | `:1502` | 1502 | NO-QUOTE-TO-CHECK |  |
| 1450 | `FW5:617` | 617 | NO-QUOTE-TO-CHECK |  |
| 1525 | `:210 s1` | 210 s1 | NO-QUOTE-TO-CHECK |  |
| 1528 | `:210 s2` | 210 s2 | NO-QUOTE-TO-CHECK |  |
| 1539 | `:212 s3` | 212 s3 | NO-QUOTE-TO-CHECK |  |

## What the extraction pattern would not catch
- Line references with no colon prefix: "line 617", "FW5 line 617", "FW5 617", "lines 613 through 618", "613 to 618".
- Numbers outside the 2-4 digit width: `:8` or `:15000` match nothing.
- Range separators other than hyphen/en-dash (em-dash, spaces around the dash: ":613 - 618").
- Compound forms like ":950-:952": the trailing `:952` is captured as a separate bare citation, so the check still visits line 952 but does not treat it as the range end of one citation.
- Citations spanning a staging line break, and fragments (e.g. block-quote lines) that sit on a staging line carrying no citation at all — those are never extracted, hence never tested.
- Fragments shorter than 12 characters, and paraphrases with no quote at all: such citations can only ever get NO-QUOTE-TO-CHECK, which is not an endorsement.
- A citation whose quoted fragment is genuinely present but whose *surrounding claim* about the line is wrong: only substring presence is tested, not what the staging text asserts about the line.