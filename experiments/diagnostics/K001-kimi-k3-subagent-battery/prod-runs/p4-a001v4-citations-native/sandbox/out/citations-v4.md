# FW5 line-citation verification — staging/STAGING-v4.md

Source: `docs/sources/FW5-explanatory-construction.md`, sha256 `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` — computed, matches the declared value.

Extraction regex: `\bFW5:(\d{2,4})(?:[-\u2013](\d{2,4}))?|(?<![\d\w./-]):(\d{2,4})(?:[-\u2013](\d{2,4}))?` (N, M are 2–4 digits; hyphen or en-dash inclusive ranges; bare `:N`/`:N-M` excluded when preceded by a digit, word char, `.`, `/` or `-`, so sha256 fragments, times, dates and file paths do not match).

Total citations extracted: **363**; distinct targets: **127**.

Counts by verdict: **CORRECT: 38**, **CORRECT IN SUBSTANCE: 2**, **WRONG: 80**, **NO-QUOTE-TO-CHECK: 243**.

**WRONG citations:** staging line 160 `:947`, staging line 194 `:743`, staging line 196 `:650`, staging line 198 `:857`, staging line 203 `:86`, staging line 203 `:106`, staging line 204 `:123`, staging line 204 `:125`, staging line 204 `:131`, staging line 207 `:170`, staging line 207 `:170`, staging line 208 `:174`, staging line 211 `:185`, staging line 211 `:194`, staging line 211 `:205`, staging line 211 `:179`, staging line 211 `:199`, staging line 211 `:188`, staging line 211 `:208`, staging line 212 `:210`, staging line 212 `:212`, staging line 212 `:210`, staging line 212 `:212`, staging line 212 `:210`, staging line 212 `:212`, staging line 214 `:152`, staging line 214 `:156`, staging line 214 `:156`, staging line 215 `:743`, staging line 215 `:746`, staging line 215 `:746`, staging line 216 `:617`, staging line 216 `:613-618`, staging line 216 `:620`, staging line 216 `:620`, staging line 220 `:638`, staging line 220 `:642`, staging line 220 `:650`, staging line 220 `FW5:640`, staging line 224 `:162`, staging line 224 `:128-130`, staging line 224 `:125`, staging line 224 `:210`, staging line 224 `:162`, staging line 224 `:202`, staging line 224 `:201-205`, staging line 224 `:162`, staging line 224 `:128-130`, staging line 224 `:125`, staging line 224 `:210`, staging line 224 `:197`, staging line 291 `:123`, staging line 343 `:123`, staging line 343 `:609`, staging line 344 `:123`, staging line 345 `:123`, staging line 451 `FW5:1372`, staging line 487 `:1519`, staging line 490 `:82`, staging line 617 `:125`, staging line 626 `:1402`, staging line 626 `:205`, staging line 666 `:210`, staging line 666 `:197`, staging line 797 `:1372`, staging line 834 `:912`, staging line 834 `:1005`, staging line 834 `:1320`, staging line 845 `:622`, staging line 847 `:893`, staging line 847 `:896`, staging line 847 `:893`, staging line 847 `:896`, staging line 847 `:896`, staging line 849 `:1182`, staging line 849 `:1178`, staging line 1006 `:620`, staging line 1137 `:1206`, staging line 1138 `:1202`, staging line 1323 `:35-47`.

Cited lines that are blank in the source: [36, 38, 40, 42, 44, 46, 82, 175, 200, 207, 299, 643, 745, 788, 799, 801, 990, 996, 998, 1000, 1004, 1006, 1008, 1010, 1012, 1209, 1211, 1217, 1257, 1259, 1337, 1339, 1341, 1343, 1363, 1385].

Ranges whose end precedes start: none.

Method notes: a quote on a staging line is tested against **every** citation on that line; lines that bundle several citations with one quote therefore mark the sibling citations WRONG even when the quote is present at its own citation's line — the note names the source line where the fragment actually sits, and those rows are attribution ambiguities of the line, not missing text. Fragments that are A001's own prose (meta-citations like `:170 Their meanings…`, file paths, receipt field names, LaTeX written by A001 rather than quoted) are excluded from the quote test.

What the extraction pattern does **not** catch: one-digit line references (`:7`); numbers of five or more digits; spelled-out citations ("line 208", "lines 613 to 618"); citations embedded inside prose without colon form; and bare `:N`-shaped references that are actually to other files (e.g. a review document's `:299`) — the pattern counts those as FW5 citations because it cannot see which file the author meant.

| staging line | citation | target | verdict | note |
|---|---|---|---|---|
| 160 | :947 | :947 | WRONG | cited line starts: \tag{CT2} \|\| fragment NOT in cited target: ## The retention fixed point \| found elsewhere at source lines [941] |
| 194 | :743 | :743 | WRONG | cited line starts: \tag{N} \|\| fragment NOT in cited target: d\equiv\ell c \| found elsewhere at source lines [742] |
| 196 | :650 | :650 | WRONG | cited line starts: \tag{K2} \|\| fragment NOT in cited target: \operatorname{Live}j \| found elsewhere at source lines [642, 649] |
| 198 | :857 | :857 | WRONG | cited line starts: A pianist can imagine a passage without playing it. A geometer can manipulate a spatial relation without naming every co \|\| fragment NOT in cited target: partial, distributed, or temporally extended \| found elsewhere at source lines [859] |
| 203 | :86 | :86 | WRONG | cited line starts: D=(V,(X_v)_{v\in V},J,B,A,L,\operatorname{role}). \|\| fragment NOT in cited target: D=(V,(Xv),J,B,A,L,\mathrm{role}) \| not found anywhere in source |
| 203 | :106 | :106 | WRONG | cited line starts: \tag{O} \|\| fragment NOT in cited target: D=(V,(Xv),J,B,A,L,\mathrm{role}) \| not found anywhere in source |
| 204 | :123 | :123 | WRONG | cited line starts: The target is \(D\). The scope \(\Sigma\subseteq A\times B\) fixes which edits and boundary conditions are in the claim. \|\| fragment NOT in cited target: p=(D,\Sigma,b0,\kappa,\mathcal C,\mathcal Q,Op) \| found elsewhere at source lines [120] |
| 204 | :125 | :125 | WRONG | cited line starts: The query operator \(\mathcal Q\) is a specified set-theoretic operation on the relevant organization, its solutions, an \|\| fragment NOT in cited target: p=(D,\Sigma,b0,\kappa,\mathcal C,\mathcal Q,Op) \| found elsewhere at source lines [120] |
| 204 | :131 | :131 | WRONG | cited line starts: \tag{Q} \|\| fragment NOT in cited target: p=(D,\Sigma,b0,\kappa,\mathcal C,\mathcal Q,Op) \| found elsewhere at source lines [120] |
| 207 | :170 | :170 | WRONG | cited line starts: The map \(\pi\) sends target valuations in the stated scope to explanatory valuations. It may be many-to-one. The maps \ \|\| fragment NOT in cited target: \pi,\tau,\sigma,\lambda \| found elsewhere at source lines [167] |
| 207 | :170 | :170 | WRONG | cited line starts: The map \(\pi\) sends target valuations in the stated scope to explanatory valuations. It may be many-to-one. The maps \ \|\| fragment NOT in cited target: \pi,\tau,\sigma,\lambda \| found elsewhere at source lines [167] |
| 208 | :174 | :174 | WRONG | cited line starts: **Anchoring.** Every active explanatory component has a stated target interpretation under \(\lambda\). Its port roles a \|\| fragment NOT in cited target: the declared abstraction \| found elsewhere at source lines [176] ; fragment NOT in cited target: only on the ports of its an |
| 211 | :185 | :185 | WRONG | cited line starts: \tag{F} \|\| fragment NOT in cited target: the comparisons specified in \(\Sigma\cap\mathcal C\) \| found elsewhere at source lines [179] ; fragment NOT in cited target: every composition for which a claim is made \| found elsewhere at source lines [188] ; fragment NOT in cited ta |
| 211 | :194 | :194 | WRONG | cited line starts: \tag{C} \|\| fragment NOT in cited target: the comparisons specified in \(\Sigma\cap\mathcal C\) \| found elsewhere at source lines [179] ; fragment NOT in cited target: every composition for which a claim is made \| found elsewhere at source lines [188] ; fragment NOT in cited ta |
| 211 | :205 | :205 | WRONG | cited line starts: \tag{A} \|\| fragment NOT in cited target: the comparisons specified in \(\Sigma\cap\mathcal C\) \| found elsewhere at source lines [179] ; fragment NOT in cited target: every composition for which a claim is made \| found elsewhere at source lines [188] ; fragment NOT in cited ta |
| 211 | :179 | :179 | WRONG | cited line starts: **Structural fidelity.** For the comparisons specified in \(\Sigma\cap\mathcal C\), \|\| fragment NOT in cited target: every composition for which a claim is made \| found elsewhere at source lines [188] ; fragment NOT in cited target: includes the respect \(\kappa\) \| found else |
| 211 | :199 | :199 | WRONG | cited line starts: **Question fidelity.** For the same comparisons, \|\| fragment NOT in cited target: the comparisons specified in \(\Sigma\cap\mathcal C\) \| found elsewhere at source lines [179] ; fragment NOT in cited target: every composition for which a claim is made \| found elsewhere at sour |
| 211 | :188 | :188 | WRONG | cited line starts: The translation preserves identities and every composition for which a claim is made: \|\| fragment NOT in cited target: the comparisons specified in \(\Sigma\cap\mathcal C\) \| found elsewhere at source lines [179] ; fragment NOT in cited target: includes the respect \(\kappa\) \ |
| 211 | :208 | :208 | WRONG | cited line starts: This includes the respect \(\kappa\), not just a matching number. The contract ranges over the declared class of changes \|\| fragment NOT in cited target: the comparisons specified in \(\Sigma\cap\mathcal C\) \| found elsewhere at source lines [179] ; fragment NOT in cited target |
| 212 | :210 | :210 | WRONG | cited line starts: **Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent b \|\| fragment NOT in cited target: at least one admitted contrast that removes or changes a nonempty block of activ \| found elsewhere at source lines [210] ; f |
| 212 | :212 | :212 | WRONG | cited line starts: **Non-vacuity.** The baseline organization has a compatible state or history. A claim of impossibility may correctly ass \|\| fragment NOT in cited target: at least one admitted contrast that removes or changes a nonempty block of activ \| found elsewhere at source lines [210] |
| 212 | :210 | :210 | WRONG | cited line starts: **Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent b \|\| fragment NOT in cited target: at least one admitted contrast that removes or changes a nonempty block of activ \| found elsewhere at source lines [210] ; f |
| 212 | :212 | :212 | WRONG | cited line starts: **Non-vacuity.** The baseline organization has a compatible state or history. A claim of impossibility may correctly ass \|\| fragment NOT in cited target: at least one admitted contrast that removes or changes a nonempty block of activ \| found elsewhere at source lines [210] |
| 212 | :210 | :210 | WRONG | cited line starts: **Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent b \|\| fragment NOT in cited target: at least one admitted contrast that removes or changes a nonempty block of activ \| found elsewhere at source lines [210] ; f |
| 212 | :212 | :212 | WRONG | cited line starts: **Non-vacuity.** The baseline organization has a compatible state or history. A claim of impossibility may correctly ass \|\| fragment NOT in cited target: at least one admitted contrast that removes or changes a nonempty block of activ \| found elsewhere at source lines [210] |
| 214 | :152 | :152 | WRONG | cited line starts: is declared model data about reference and representation at boundary \(\beta\). It is not a host's claim that the token \|\| fragment NOT in cited target: \operatorname{Rep}{\beta,\ell} \| found elsewhere at source lines [149] |
| 214 | :156 | :156 | WRONG | cited line starts: The representation relation is an explicit semantic primitive. Removing the word “explanation” from a formula does not d \|\| fragment NOT in cited target: \operatorname{Rep}{\beta,\ell} \| found elsewhere at source lines [149] |
| 214 | :156 | :156 | WRONG | cited line starts: The representation relation is an explicit semantic primitive. Removing the word “explanation” from a formula does not d \|\| fragment NOT in cited target: \operatorname{Rep}{\beta,\ell} \| found elsewhere at source lines [149] |
| 215 | :743 | :743 | WRONG | cited line starts: \tag{N} \|\| fragment NOT in cited target: d\equiv\ell c \| found elsewhere at source lines [742] |
| 215 | :746 | :746 | WRONG | cited line starts: The equivalence is structural at the stated grain, not string equality or similarity. Forgotten prior understanding belo \|\| fragment NOT in cited target: d\equiv\ell c \| found elsewhere at source lines [742] |
| 215 | :746 | :746 | WRONG | cited line starts: The equivalence is structural at the stated grain, not string equality or similarity. Forgotten prior understanding belo \|\| fragment NOT in cited target: d\equiv\ell c \| found elsewhere at source lines [742] |
| 216 | :617 | :617 | WRONG | cited line starts: \tag{K1} \|\| fragment NOT in cited target: \operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal Ec,p\delta) \| not found anywhere in source ; fragment NOT in cited target: The alleged defect must concern the stated target and respect \| found elsewhere at source lines |
| 216 | :613-618 | :613-618 | WRONG | cited line starts: \[ \|\| fragment NOT in cited target: \operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal Ec,p\delta) \| not found anywhere in source ; fragment NOT in cited target: The alleged defect must concern the stated target and respect \| found elsewhere at source lines [620] |
| 216 | :620 | :620 | WRONG | cited line starts: where \(\mathcal E_c\) is the criticism's interpreted structural account. The alleged defect must concern the stated tar \|\| fragment NOT in cited target: \operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal Ec,p\delta) \| not found anywhere in source |
| 216 | :620 | :620 | WRONG | cited line starts: where \(\mathcal E_c\) is the criticism's interpreted structural account. The alleged defect must concern the stated tar \|\| fragment NOT in cited target: \operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal Ec,p\delta) \| not found anywhere in source |
| 220 | :638 | :638 | WRONG | cited line starts: Standing is the system's enacted permission to use a content in a particular application and respect. It may be explicit \|\| fragment NOT in cited target: \operatorname{Live}j \| found elsewhere at source lines [642, 649] ; fragment NOT in cited target: not automatically machine- |
| 220 | :642 | :642 | WRONG | cited line starts: For an argument application \(u\), let \(\operatorname{Prem}(u)\) be its declared essential premises, including interpre \|\| fragment NOT in cited target: not automatically machine-maintainable \| found elsewhere at source lines [640] |
| 220 | :650 | :650 | WRONG | cited line starts: \tag{K2} \|\| fragment NOT in cited target: \operatorname{Live}j \| found elsewhere at source lines [642, 649] ; fragment NOT in cited target: not automatically machine-maintainable \| found elsewhere at source lines [640] |
| 220 | FW5:640 | :640 | WRONG | cited line starts: A source's appearance in a prompt is a delivery fact. A named field asking for a criticism is an invitation fact. Actual \|\| fragment NOT in cited target: \operatorname{Live}j \| found elsewhere at source lines [642, 649] |
| 224 | :162 | :162 | WRONG | cited line starts: An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}_E\), and an in \|\| fragment NOT in cited target: \operatorname{Ans}p(a,b)=\mathcal Q(D,a,b) \| not found anywhere in source ; fragment NOT in cited target: a specified set-th |
| 224 | :128-130 | :128-130 | WRONG | cited line starts: \operatorname{Ans}_p(a,b) \|\| fragment NOT in cited target: \operatorname{Ans}E \| found elsewhere at source lines [162, 202] ; fragment NOT in cited target: \operatorname{Ans}E \| found elsewhere at source lines [162, 202] ; fragment NOT in cited target: An explanatory candidate |
| 224 | :125 | :125 | WRONG | cited line starts: The query operator \(\mathcal Q\) is a specified set-theoretic operation on the relevant organization, its solutions, an \|\| fragment NOT in cited target: \operatorname{Ans}E \| found elsewhere at source lines [162, 202] ; fragment NOT in cited target: \operatorname{Ans}E \| foun |
| 224 | :210 | :210 | WRONG | cited line starts: **Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent b \|\| fragment NOT in cited target: \operatorname{Ans}E \| found elsewhere at source lines [162, 202] ; fragment NOT in cited target: \operatorname{Ans}E \| foun |
| 224 | :162 | :162 | WRONG | cited line starts: An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}_E\), and an in \|\| fragment NOT in cited target: \operatorname{Ans}p(a,b)=\mathcal Q(D,a,b) \| not found anywhere in source ; fragment NOT in cited target: a specified set-th |
| 224 | :202 | :202 | WRONG | cited line starts: \operatorname{Ans}_E(\tau(a),\sigma(b)) \|\| fragment NOT in cited target: An explanatory candidate for \(p\) supplies an organization \(E\), an answer pro \| found elsewhere at source lines [162] ; fragment NOT in cited target: \operatorname{Ans}p(a,b)=\mathcal Q(D,a,b) \| not fo |
| 224 | :201-205 | :201-205 | WRONG | cited line starts: \[ \|\| fragment NOT in cited target: An explanatory candidate for \(p\) supplies an organization \(E\), an answer pro \| found elsewhere at source lines [162] ; fragment NOT in cited target: \operatorname{Ans}p(a,b)=\mathcal Q(D,a,b) \| not found anywhere in source ; fragment NOT |
| 224 | :162 | :162 | WRONG | cited line starts: An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}_E\), and an in \|\| fragment NOT in cited target: \operatorname{Ans}p(a,b)=\mathcal Q(D,a,b) \| not found anywhere in source ; fragment NOT in cited target: a specified set-th |
| 224 | :128-130 | :128-130 | WRONG | cited line starts: \operatorname{Ans}_p(a,b) \|\| fragment NOT in cited target: \operatorname{Ans}E \| found elsewhere at source lines [162, 202] ; fragment NOT in cited target: \operatorname{Ans}E \| found elsewhere at source lines [162, 202] ; fragment NOT in cited target: An explanatory candidate |
| 224 | :125 | :125 | WRONG | cited line starts: The query operator \(\mathcal Q\) is a specified set-theoretic operation on the relevant organization, its solutions, an \|\| fragment NOT in cited target: \operatorname{Ans}E \| found elsewhere at source lines [162, 202] ; fragment NOT in cited target: \operatorname{Ans}E \| foun |
| 224 | :210 | :210 | WRONG | cited line starts: **Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent b \|\| fragment NOT in cited target: \operatorname{Ans}E \| found elsewhere at source lines [162, 202] ; fragment NOT in cited target: \operatorname{Ans}E \| foun |
| 224 | :197 | :197 | WRONG | cited line starts: Component surgeries must commute with their anchors. Replacing an explanatory component cannot be interpreted as changin \|\| fragment NOT in cited target: \operatorname{Ans}E \| found elsewhere at source lines [162, 202] ; fragment NOT in cited target: \operatorname{Ans}E \| foun |
| 291 | :123 | :123 | WRONG | cited line starts: The target is \(D\). The scope \(\Sigma\subseteq A\times B\) fixes which edits and boundary conditions are in the claim. \|\| fragment NOT in cited target: Weakens the claim that falling recurrence would confirm c1 and rising recurrence \| not found anywhere in source ; fragment N |
| 343 | :123 | :123 | WRONG | cited line starts: The target is \(D\). The scope \(\Sigma\subseteq A\times B\) fixes which edits and boundary conditions are in the claim. \|\| fragment NOT in cited target: no compatible realization \| found elsewhere at source lines [212] |
| 343 | :609 | :609 | WRONG | cited line starts: A criticism has a represented target \(z\), an alleged defect \(\delta\), grounds \(g\), and a proposed connection from  \|\| fragment NOT in cited target: no compatible realization \| found elsewhere at source lines [212] |
| 344 | :123 | :123 | WRONG | cited line starts: The target is \(D\). The scope \(\Sigma\subseteq A\times B\) fixes which edits and boundary conditions are in the claim. \|\| fragment NOT in cited target: a missing distinction \| found elsewhere at source lines [609] |
| 345 | :123 | :123 | WRONG | cited line starts: The target is \(D\). The scope \(\Sigma\subseteq A\times B\) fixes which edits and boundary conditions are in the claim. \|\| fragment NOT in cited target: bridge-strained \| not found anywhere in source |
| 451 | FW5:1372 | :1372 | WRONG | cited line starts: The explicit representation interpretation is not eliminated. If the fidelity and integration conditions admit a system  \|\| fragment NOT in cited target: \mathsf{FW5} \| found elsewhere at source lines [1192] |
| 487 | :1519 | :1519 | WRONG | cited line 1519 is beyond the source (1503 lines) |
| 490 | :82 | :82 | WRONG | cited line starts:  \|\| fragment NOT in cited target: occurrence-02/plan.json \| not found anywhere in source |
| 617 | :125 | :125 | WRONG | cited line starts: The query operator \(\mathcal Q\) is a specified set-theoretic operation on the relevant organization, its solutions, an \|\| fragment NOT in cited target: \operatorname{Ans}p(a,b)=\mathcal Q(D,a,b) \| not found anywhere in source |
| 626 | :1402 | :1402 | WRONG | cited line starts: All four Boolean input assignments were checked for the parallel and priority constructions. Their endpoint outputs agre \|\| fragment NOT in cited target: \operatorname{Ans}E(\tau(a),\sigma(b)) \| found elsewhere at source lines [202] |
| 626 | :205 | :205 | WRONG | cited line starts: \tag{A} \|\| fragment NOT in cited target: \operatorname{Ans}E(\tau(a),\sigma(b)) \| found elsewhere at source lines [202] |
| 666 | :210 | :210 | WRONG | cited line starts: **Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent b \|\| fragment NOT in cited target: \operatorname{Ans}E \| found elsewhere at source lines [162, 202] |
| 666 | :197 | :197 | WRONG | cited line starts: Component surgeries must commute with their anchors. Replacing an explanatory component cannot be interpreted as changin \|\| fragment NOT in cited target: the anchored organization \| found elsewhere at source lines [210] ; fragment NOT in cited target: \operatorname{Ans}E \| fou |
| 797 | :1372 | :1372 | WRONG | cited line starts: The explicit representation interpretation is not eliminated. If the fidelity and integration conditions admit a system  \|\| fragment NOT in cited target: Representation and apparent reason use \| found elsewhere at source lines [1370] |
| 834 | :912 | :912 | WRONG | cited line starts: An information variable is, in the constructor-theoretic treatment, a clonable computation variable. Computation variabl \|\| fragment NOT in cited target: standing-bearing \| found elsewhere at source lines [1320] |
| 834 | :1005 | :1005 | WRONG | cited line starts: for this physical attribution, displaying the realization ecology \(\mathcal E\): information-bearing media, interpretin \|\| fragment NOT in cited target: standing-bearing \| found elsewhere at source lines [1320] |
| 834 | :1320 | :1320 | WRONG | cited line starts: A fixed implementation does not, merely through being fixed, exclude some explanatory domain. Its represented programs o \|\| fragment NOT in cited target: information-bearing \| found elsewhere at source lines [912, 1005] |
| 845 | :622 | :622 | WRONG | cited line starts: A criticism occurrence can exist when (K1) is false. Its grounds may be mistaken, its target misidentified, its inferenc \|\| fragment NOT in cited target: A criticism occurrence can exist when (K1) is false… It can become grounds for a \| not found anywhere in source |
| 847 | :893 | :893 | WRONG | cited line starts: \mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A \|\| fragment NOT in cited target: states that a reason bears on a work in an aesthetic respect \| found elsewhere at source lines [896] ; fragment NOT in cited target: \operatorname{Bearing}(c,z,p) \| found elsewhe |
| 847 | :896 | :896 | WRONG | cited line starts: states that a reason bears on a work in an aesthetic respect. \(\mathcal Rsn\) is a set of reason contents; \(\mathcal V \|\| fragment NOT in cited target: \mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal VA \| found elsewhere at source lines [893] ; fragment NOT in c |
| 847 | :893 | :893 | WRONG | cited line starts: \mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A \|\| fragment NOT in cited target: states that a reason bears on a work in an aesthetic respect \| found elsewhere at source lines [896] ; fragment NOT in cited target: \operatorname{Bearing}(c,z,p) \| found elsewhe |
| 847 | :896 | :896 | WRONG | cited line starts: states that a reason bears on a work in an aesthetic respect. \(\mathcal Rsn\) is a set of reason contents; \(\mathcal V \|\| fragment NOT in cited target: \mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal VA \| found elsewhere at source lines [893] ; fragment NOT in c |
| 847 | :896 | :896 | WRONG | cited line starts: states that a reason bears on a work in an aesthetic respect. \(\mathcal Rsn\) is a set of reason contents; \(\mathcal V \|\| fragment NOT in cited target: \mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal VA \| found elsewhere at source lines [893] ; fragment NOT in c |
| 849 | :1182 | :1182 | WRONG | cited line starts: Critical bearing is accounting for the specified defect question. Reason use is a representation-preserving map into an  \|\| fragment NOT in cited target: Defined relations and dependence order \| found elsewhere at source lines [1178] |
| 849 | :1178 | :1178 | WRONG | cited line starts: ## Defined relations and dependence order \|\| fragment NOT in cited target: Critical bearing is accounting for the specified defect question. \| found elsewhere at source lines [1182] |
| 1006 | :620 | :620 | WRONG | cited line starts: where \(\mathcal E_c\) is the criticism's interpreted structural account. The alleged defect must concern the stated tar \|\| fragment NOT in cited target: An observer may lack the data needed to establish the witness. That makes the at \| found elsewhere at source lines [634] |
| 1137 | :1206 | :1206 | WRONG | cited line starts: The result does not apply to arbitrary compression, loss of event identity, a changed boundary, or a coarsening that ide \|\| fragment NOT in cited target: account#c1-c3 \| not found anywhere in source |
| 1138 | :1202 | :1202 | WRONG | cited line starts: Suppose all carriers, component relations, role bindings, maps, histories, question contracts, and attribution indices a \|\| fragment NOT in cited target: the stipulated bijections \| found elsewhere at source lines [1206] |
| 1323 | :35-47 | :35-47 | WRONG | cited line starts: ## What “no gaps” can responsibly mean \|\| fragment NOT in cited target: campaign.sourceidentity() \| not found anywhere in source |
| 206 | :123 | :123 | CORRECT IN SUBSTANCE | matched only after normalisation (typographic quotes / markdown emphasis / whitespace): 'distinctions material to that question' |
| 848 | :900 | :900 | CORRECT IN SUBSTANCE | matched only after normalisation (typographic quotes / markdown emphasis / whitespace): 'effects belong to \(\mathcal R\), purposes to \(G\), normati' |
| 104 | :167 | :167 | CORRECT |  |
| 117 | FW5:831 | :831 | CORRECT |  |
| 143 | FW5:1192 | :1192 | CORRECT |  |
| 194 | :738-746 | :738-746 | CORRECT |  |
| 194 | :742 | :742 | CORRECT |  |
| 196 | :642 | :642 | CORRECT |  |
| 198 | :859 | :859 | CORRECT |  |
| 204 | :120 | :120 | CORRECT |  |
| 205 | :123 | :123 | CORRECT |  |
| 207 | :167 | :167 | CORRECT |  |
| 208 | :176 | :176 | CORRECT |  |
| 208 | :176 | :176 | CORRECT |  |
| 208 | :176 | :176 | CORRECT |  |
| 209 | :154 | :154 | CORRECT |  |
| 209 | :154 | :154 | CORRECT |  |
| 210 | :162 | :162 | CORRECT |  |
| 213 | :212 | :212 | CORRECT |  |
| 214 | :149 | :149 | CORRECT |  |
| 214 | :148-150 | :148-150 | CORRECT |  |
| 215 | :742 | :742 | CORRECT |  |
| 218 | :601 | :601 | CORRECT |  |
| 221 | :787-800 | :787-800 | CORRECT |  |
| 289 | FW5:140 | :140 | CORRECT |  |
| 343 | :212 | :212 | CORRECT |  |
| 344 | :609 | :609 | CORRECT |  |
| 448 | :831 | :831 | CORRECT |  |
| 451 | :1192 | :1192 | CORRECT |  |
| 568 | :208 | :208 | CORRECT |  |
| 594 | :1214-1215 | :1214-1215 | CORRECT |  |
| 645 | :197 | :197 | CORRECT |  |
| 833 | :800 | :800 | CORRECT |  |
| 842 | :607 | :607 | CORRECT |  |
| 843 | :609 | :609 | CORRECT |  |
| 844 | :620 | :620 | CORRECT |  |
| 844 | :620 | :620 | CORRECT |  |
| 846 | :773 | :773 | CORRECT |  |
| 1003 | :1364 | :1364 | CORRECT |  |
| 1006 | FW5:634 | :634 | CORRECT |  |
| 50 | FW5:831 | :831 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 81 | FW5:208 | :208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 83 | FW5:1372 | :1372 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 83 | :188 | :188 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 83 | :174 | :174 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 83 | :170 | :170 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 83 | :244 | :244 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 102 | FW5:172 | :172 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 105 | :170 | :170 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 105 | :174-176 | :174-176 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 106 | :185 | :185 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 106 | :194 | :194 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 106 | :188 | :188 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 107 | :205 | :205 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 107 | :208 | :208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 107 | :210 | :210 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 108 | :212 | :212 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 108 | :223 | :223 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 110 | FW5:226 | :226 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 112 | FW5:228 | :228 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 116 | :617 | :617 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 116 | :613-618 | :613-618 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 119 | :1364 | :1364 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 134 | FW5:1364 | :1364 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 137 | FW5:1502 | :1502 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 140 | :228 | :228 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 142 | :831 | :831 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 149 | :1192 | :1192 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 154 | :1390 | :1390 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 154 | :1390 | :1390 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 157 | :306 | :306 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 158 | :315 | :315 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 158 | :296 | :296 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 158 | :429 | :429 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 158 | :497 | :497 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 159 | :582 | :582 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 159 | :947 | :947 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 159 | :950 | :950 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 159 | :941 | :941 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 161 | :945-948 | :945-948 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 162 | :950 | :950 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 162 | :952 | :952 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 164 | :1390 | :1390 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 165 | :1202 | :1202 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 165 | :1204 | :1204 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 166 | :1206 | :1206 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 166 | :1208 | :1208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 166 | :1210-1218 | :1210-1218 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 167 | :1220 | :1220 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 167 | :1222 | :1222 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 167 | :1224 | :1224 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 168 | :1390 | :1390 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 169 | :1390 | :1390 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 172 | :1384-1386 | :1384-1386 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 172 | :902 | :902 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 176 | :893 | :893 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 176 | :896 | :896 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 176 | :896 | :896 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 191 | :85 | :85 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 191 | :86 | :86 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 191 | :106 | :106 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 191 | :117 | :117 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 191 | :120 | :120 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 192 | :131 | :131 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 192 | :166 | :166 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 192 | :167 | :167 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 192 | :617 | :617 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 193 | :1210-1218 | :1210-1218 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 195 | :746 | :746 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 195 | :642-651 | :642-651 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 195 | :638 | :638 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 197 | :644-650 | :644-650 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 217 | :609 | :609 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 217 | :609 | :609 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 219 | :628 | :628 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 219 | :630 | :630 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 219 | :628 | :628 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 222 | :1210-1218 | :1210-1218 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 222 | :1220 | :1220 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 222 | :1218 | :1218 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 222 | :1222 | :1222 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 222 | :1224 | :1224 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 223 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 223 | :123 | :123 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 227 | :989-991 | :989-991 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 227 | :995-1012 | :995-1012 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 247 | FW5:728 | :728 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 271 | :609 | :609 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 275 | :609 | :609 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 293 | FW5:210 | :210 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 293 | :212 | :212 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 293 | FW5:630 | :630 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 294 | FW5:630 | :630 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 327 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 327 | FW5:620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 330 | :299 | :299 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 332 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 334 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 340 | :123 | :123 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 341 | :123 | :123 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 342 | :123 | :123 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 417 | :1364 | :1364 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 420 | :37 | :37 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 426 | :226 | :226 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 426 | :226 | :226 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 432 | :228 | :228 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 435 | :226 | :226 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 436 | :226 | :226 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 441 | :617 | :617 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 443 | :831 | :831 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 444 | :1202 | :1202 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 444 | :1210-1218 | :1210-1218 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 445 | :947 | :947 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 445 | :950 | :950 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 447 | :228 | :228 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 454 | FW5:1392 | :1392 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 456 | FW5:688 | :688 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 457 | FW5:1404 | :1404 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 460 | :1336-1344 | :1336-1344 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 461 | :1342 | :1342 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 477 | FW5:1392 | :1392 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 494 | FW5:688 | :688 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 516 | :1364 | :1364 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 519 | :1364 | :1364 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 526 | :162 | :162 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 526 | :125 | :125 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 526 | :128-130 | :128-130 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 526 | :210 | :210 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 536 | :1222 | :1222 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 537 | :1402 | :1402 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 553 | :210 | :210 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 554 | :212 | :212 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 558 | :170 | :170 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 567 | :1402 | :1402 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 574 | FW5:236 | :236 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 577 | :1364 | :1364 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 586 | :212 | :212 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 589 | :1208-1218 | :1208-1218 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 590 | :1218 | :1218 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 596 | :1224 | :1224 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 598 | :1222 | :1222 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 613 | :162 | :162 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 613 | :202 | :202 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 613 | :162 | :162 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 616 | :128-130 | :128-130 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 623 | :208 | :208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 628 | :208 | :208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 630 | :199-208 | :199-208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 632 | :208 | :208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 638 | :210 | :210 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 649 | :210 | :210 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 655 | :210 | :210 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 664 | :236 | :236 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 664 | :208 | :208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 664 | :1364 | :1364 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 665 | :208 | :208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 670 | :208 | :208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 684 | :176 | :176 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 694 | :176 | :176 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 696 | :176 | :176 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 709 | :176 | :176 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 720 | :174 | :174 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 723 | :176 | :176 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 724 | :1402 | :1402 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 727 | :185 | :185 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 737 | :212 | :212 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 739 | :212 | :212 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 750 | :212 | :212 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 754 | :210 | :210 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 754 | :208 | :208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 761 | :859 | :859 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 764 | :244 | :244 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 772 | :188 | :188 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 775 | :174 | :174 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 779 | :170 | :170 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 779 | :244 | :244 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 780 | :170 | :170 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 781 | :244 | :244 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 784 | :1364 | :1364 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 791 | :1372 | :1372 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 791 | :1372 | :1372 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 798 | :1370 | :1370 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 798 | :1362 | :1362 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 824 | :617 | :617 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 835 | :607 | :607 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 835 | :614 | :614 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 835 | :622 | :622 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 835 | :773 | :773 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 836 | :896 | :896 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 836 | :900 | :900 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 836 | :1182 | :1182 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 836 | :609 | :609 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 836 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 837 | :613-618 | :613-618 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 851 | :1182 | :1182 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 859 | :1182 | :1182 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 871 | :299 | :299 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 903 | :1364 | :1364 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 904 | :170 | :170 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 925 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 925 | FW5:620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1000 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1026 | :176 | :176 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1046 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1099 | FW5:640 | :640 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1133 | FW5:1202 | :1202 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1133 | :1202 | :1202 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1152 | FW5:849 | :849 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1152 | :851 | :851 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1155 | FW5:851 | :851 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1159 | :831 | :831 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1162 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1163 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1175 | FW5:634 | :634 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1191 | FW5:800 | :800 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1192 | FW5:787-802 | :787-802 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1194 | FW5:609 | :609 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1196 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1196 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1209 | FW5:1256-1260 | :1256-1260 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1211 | FW5:688 | :688 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1211 | FW5:1392 | :1392 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1211 | FW5:1404 | :1404 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1212 | :1336-1344 | :1336-1344 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1219 | FW5:1368 | :1368 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1226 | FW5:630 | :630 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1287 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1297 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1310 | :620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1423 | FW5:620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1426 | FW5:1372 | :1372 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1426 | :188 | :188 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1426 | :174 | :174 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1426 | :170 | :170 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1426 | :244 | :244 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1426 | FW5:208 | :208 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1440 | FW5:620 | :620 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1444 | FW5:1362-1364 | :1362-1364 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1445 | :1502 | :1502 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1450 | FW5:617 | :617 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1525 | :210 | :210 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1528 | :210 | :210 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
| 1539 | :212 | :212 | NO-QUOTE-TO-CHECK | no quoted fragment >= 12 chars on staging line |
