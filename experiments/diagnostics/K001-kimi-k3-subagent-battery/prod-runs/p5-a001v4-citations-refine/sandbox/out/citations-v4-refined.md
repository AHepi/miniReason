# A001 v4 citation audit -- refinement of the 80 WRONG verdicts

Source: `docs/sources/FW5-explanatory-construction.md` (sha256 `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a`, matches the task-declared hash).

The first pass (`staging/citations-v4-first-pass.json`) tested every quoted fragment on a staging line against every citation on that line, so fragments that belonged to a sibling citation were marked WRONG. This refinement re-attributes each failed fragment by locating every source line where it occurs (typographic quotes and whitespace normalised), then classifies the row. All matching is computed by `check/refine.py`; nothing here is transcribed by hand.

## Summary of classes

| class | definition | count |
|---|---|---|
| RESOLVED-BY-SIBLING | the staging line carries several citations; the fragment is verbatim at a line targeted by another citation on the same line, so the first pass blamed the wrong sibling | 42 |
| NOT-A-QUOTE | the fragment occurs nowhere in the source and is A001/staging notation (a normalised LaTeX rewrite whose tokens exist in the source, a file path, a receipt field, or an audit label) | 30 |
| OFF-BY-N | the fragment is a genuine quotation that occurs exactly once, N lines from the cited line (candidate rows that produced such a fragment; distinct fragments counted) | 2 |
| TAG-CONVENTION | the cited line is a \tag{...} display-tag line and the quoted fragment sits in the display body on preceding lines (citation names the tag while quoting the display) | 1 |
| UNRESOLVED | the fragment occurs in the source but not at any cited line, citing a non-tag line at an offset too large (or too ambiguous) for a clean off-by-N re-attribution | 1 |
| (WRONG rows total) | rows re-examined; candidate rows may hold several fragments | 80 |

Row counts: 42 RESOLVED-BY-SIBLING, 30 NOT-A-QUOTE, 8 CANDIDATE rows (4 distinct candidate fragments).

## Row-level classification

### staging line 160, citation `:947` -> CANDIDATE

- cited line 947 starts: `\tag{CT2}`
- fragment `## The retention fixed point`: CANDIDATE; fragment occurs in the source but not at any line cited by this staging line; occurs at source lines [941]

### staging line 194, citation `:743` -> NOT-A-QUOTE

- cited line 743 starts: `\tag{N}`
- fragment `d\equiv\ell c`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 196, citation `:650` -> NOT-A-QUOTE

- cited line 650 starts: `\tag{K2}`
- fragment `\operatorname{Live}j`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 198, citation `:857` -> RESOLVED-BY-SIBLING

- cited line 857 starts: `A pianist can imagine a passage without playing it. A geometer can manipulate a spatial relation without naming every component. An investigator can notice an i`
- fragment `partial, distributed, or temporally extended`: RESOLVED-BY-SIBLING; sibling citation `:859`; occurs at source lines [859]

### staging line 203, citation `:86` -> NOT-A-QUOTE

- cited line 86 starts: `D=(V,(X_v)_{v\in V},J,B,A,L,\operatorname{role}).`
- fragment `D=(V,(Xv),J,B,A,L,\mathrm{role})`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 203, citation `:106` -> NOT-A-QUOTE

- cited line 106 starts: `\tag{O}`
- fragment `D=(V,(Xv),J,B,A,L,\mathrm{role})`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 204, citation `:123` -> NOT-A-QUOTE

- cited line 123 starts: `The target is \(D\). The scope \(\Sigma\subseteq A\times B\) fixes which edits and boundary conditions are in the claim. The distinguished baseline is \((1,b_0)`
- fragment `p=(D,\Sigma,b0,\kappa,\mathcal C,\mathcal Q,Op)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 204, citation `:125` -> NOT-A-QUOTE

- cited line 125 starts: `The query operator \(\mathcal Q\) is a specified set-theoretic operation on the relevant organization, its solutions, and, where needed, its component structure`
- fragment `p=(D,\Sigma,b0,\kappa,\mathcal C,\mathcal Q,Op)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 204, citation `:131` -> NOT-A-QUOTE

- cited line 131 starts: `\tag{Q}`
- fragment `p=(D,\Sigma,b0,\kappa,\mathcal C,\mathcal Q,Op)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 207, citation `:170` -> RESOLVED-BY-SIBLING

- cited line 170 starts: `The map \(\pi\) sends target valuations in the stated scope to explanatory valuations. It may be many-to-one. The maps \(\tau\) and \(\sigma\) translate edits a`
- fragment `\pi,\tau,\sigma,\lambda`: RESOLVED-BY-SIBLING; sibling citation `:167`; occurs at source lines [167]

### staging line 207, citation `:170` -> RESOLVED-BY-SIBLING

- cited line 170 starts: `The map \(\pi\) sends target valuations in the stated scope to explanatory valuations. It may be many-to-one. The maps \(\tau\) and \(\sigma\) translate edits a`
- fragment `\pi,\tau,\sigma,\lambda`: RESOLVED-BY-SIBLING; sibling citation `:167`; occurs at source lines [167]

### staging line 208, citation `:174` -> RESOLVED-BY-SIBLING

- cited line 174 starts: `**Anchoring.** Every active explanatory component has a stated target interpretation under \(\lambda\). Its port roles and edit semantics are preserved. A causa`
- fragment `the declared abstraction`: RESOLVED-BY-SIBLING; sibling citation `:176`; occurs at source lines [176]
- fragment `only on the ports of its anchored subnetwork and the explicitly declared boundary`: RESOLVED-BY-SIBLING; sibling citation `:176`; occurs at source lines [176]
- fragment `Together with (F), which checks the assembled organization, this prevents local relation matches from silently losing constraints shared between components`: RESOLVED-BY-SIBLING; sibling citation `:176`; occurs at source lines [176]

### staging line 211, citation `:185` -> RESOLVED-BY-SIBLING

- cited line 185 starts: `\tag{F}`
- fragment `the comparisons specified in \(\Sigma\cap\mathcal C\)`: RESOLVED-BY-SIBLING; sibling citation `:179`; occurs at source lines [179]
- fragment `every composition for which a claim is made`: RESOLVED-BY-SIBLING; sibling citation `:188`; occurs at source lines [188]
- fragment `includes the respect \(\kappa\)`: RESOLVED-BY-SIBLING; sibling citation `:208`; occurs at source lines [208]

### staging line 211, citation `:194` -> RESOLVED-BY-SIBLING

- cited line 194 starts: `\tag{C}`
- fragment `the comparisons specified in \(\Sigma\cap\mathcal C\)`: RESOLVED-BY-SIBLING; sibling citation `:179`; occurs at source lines [179]
- fragment `every composition for which a claim is made`: RESOLVED-BY-SIBLING; sibling citation `:188`; occurs at source lines [188]
- fragment `includes the respect \(\kappa\)`: RESOLVED-BY-SIBLING; sibling citation `:208`; occurs at source lines [208]

### staging line 211, citation `:205` -> RESOLVED-BY-SIBLING

- cited line 205 starts: `\tag{A}`
- fragment `the comparisons specified in \(\Sigma\cap\mathcal C\)`: RESOLVED-BY-SIBLING; sibling citation `:179`; occurs at source lines [179]
- fragment `every composition for which a claim is made`: RESOLVED-BY-SIBLING; sibling citation `:188`; occurs at source lines [188]
- fragment `includes the respect \(\kappa\)`: RESOLVED-BY-SIBLING; sibling citation `:208`; occurs at source lines [208]

### staging line 211, citation `:179` -> RESOLVED-BY-SIBLING

- cited line 179 starts: `**Structural fidelity.** For the comparisons specified in \(\Sigma\cap\mathcal C\),`
- fragment `every composition for which a claim is made`: RESOLVED-BY-SIBLING; sibling citation `:188`; occurs at source lines [188]
- fragment `includes the respect \(\kappa\)`: RESOLVED-BY-SIBLING; sibling citation `:208`; occurs at source lines [208]

### staging line 211, citation `:199` -> RESOLVED-BY-SIBLING

- cited line 199 starts: `**Question fidelity.** For the same comparisons,`
- fragment `the comparisons specified in \(\Sigma\cap\mathcal C\)`: RESOLVED-BY-SIBLING; sibling citation `:179`; occurs at source lines [179]
- fragment `every composition for which a claim is made`: RESOLVED-BY-SIBLING; sibling citation `:188`; occurs at source lines [188]
- fragment `includes the respect \(\kappa\)`: RESOLVED-BY-SIBLING; sibling citation `:208`; occurs at source lines [208]

### staging line 211, citation `:188` -> RESOLVED-BY-SIBLING

- cited line 188 starts: `The translation preserves identities and every composition for which a claim is made:`
- fragment `the comparisons specified in \(\Sigma\cap\mathcal C\)`: RESOLVED-BY-SIBLING; sibling citation `:179`; occurs at source lines [179]
- fragment `includes the respect \(\kappa\)`: RESOLVED-BY-SIBLING; sibling citation `:208`; occurs at source lines [208]

### staging line 211, citation `:208` -> RESOLVED-BY-SIBLING

- cited line 208 starts: `This includes the respect \(\kappa\), not just a matching number. The contract ranges over the declared class of changes, including unperformed changes, not mer`
- fragment `the comparisons specified in \(\Sigma\cap\mathcal C\)`: RESOLVED-BY-SIBLING; sibling citation `:179`; occurs at source lines [179]
- fragment `every composition for which a claim is made`: RESOLVED-BY-SIBLING; sibling citation `:188`; occurs at source lines [188]

### staging line 212, citation `:210` -> RESOLVED-BY-SIBLING

- cited line 210 starts: `**Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent boundary conditions. The target answer is`
- fragment `at least one admitted contrast that removes or changes a nonempty block of active organizational commitments … for which the answer profile changes or ceases to be determined in the claimed way`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `A contrast family containing only notational variants, or one defined to exclude every change that could matter, does not meet non-circular dependence`: RESOLVED-BY-SIBLING; sibling citation `:212`; occurs at source lines [212]
- fragment `could matter`: RESOLVED-BY-SIBLING; sibling citation `:212`; occurs at source lines [212]

### staging line 212, citation `:212` -> NOT-A-QUOTE

- cited line 212 starts: `**Non-vacuity.** The baseline organization has a compatible state or history. A claim of impossibility may correctly assert that a specified goal has no compati`
- fragment `at least one admitted contrast that removes or changes a nonempty block of active organizational commitments … for which the answer profile changes or ceases to be determined in the claimed way`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 212, citation `:210` -> RESOLVED-BY-SIBLING

- cited line 210 starts: `**Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent boundary conditions. The target answer is`
- fragment `at least one admitted contrast that removes or changes a nonempty block of active organizational commitments … for which the answer profile changes or ceases to be determined in the claimed way`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `A contrast family containing only notational variants, or one defined to exclude every change that could matter, does not meet non-circular dependence`: RESOLVED-BY-SIBLING; sibling citation `:212`; occurs at source lines [212]
- fragment `could matter`: RESOLVED-BY-SIBLING; sibling citation `:212`; occurs at source lines [212]

### staging line 212, citation `:212` -> NOT-A-QUOTE

- cited line 212 starts: `**Non-vacuity.** The baseline organization has a compatible state or history. A claim of impossibility may correctly assert that a specified goal has no compati`
- fragment `at least one admitted contrast that removes or changes a nonempty block of active organizational commitments … for which the answer profile changes or ceases to be determined in the claimed way`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 212, citation `:210` -> RESOLVED-BY-SIBLING

- cited line 210 starts: `**Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent boundary conditions. The target answer is`
- fragment `at least one admitted contrast that removes or changes a nonempty block of active organizational commitments … for which the answer profile changes or ceases to be determined in the claimed way`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `A contrast family containing only notational variants, or one defined to exclude every change that could matter, does not meet non-circular dependence`: RESOLVED-BY-SIBLING; sibling citation `:212`; occurs at source lines [212]
- fragment `could matter`: RESOLVED-BY-SIBLING; sibling citation `:212`; occurs at source lines [212]

### staging line 212, citation `:212` -> NOT-A-QUOTE

- cited line 212 starts: `**Non-vacuity.** The baseline organization has a compatible state or history. A claim of impossibility may correctly assert that a specified goal has no compati`
- fragment `at least one admitted contrast that removes or changes a nonempty block of active organizational commitments … for which the answer profile changes or ceases to be determined in the claimed way`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 214, citation `:152` -> NOT-A-QUOTE

- cited line 152 starts: `is declared model data about reference and representation at boundary \(\beta\). It is not a host's claim that the token was supplied to a prompt. Its admissibi`
- fragment `\operatorname{Rep}{\beta,\ell}`: NOT-A-QUOTE; normalised LaTeX rewrite of source text (subscripts/operators flattened); substantive text occurs at source lines [149]

### staging line 214, citation `:156` -> NOT-A-QUOTE

- cited line 156 starts: `The representation relation is an explicit semantic primitive. Removing the word “explanation” from a formula does not derive reference from uninterpreted matte`
- fragment `\operatorname{Rep}{\beta,\ell}`: NOT-A-QUOTE; normalised LaTeX rewrite of source text (subscripts/operators flattened); substantive text occurs at source lines [149]

### staging line 214, citation `:156` -> NOT-A-QUOTE

- cited line 156 starts: `The representation relation is an explicit semantic primitive. Removing the word “explanation” from a formula does not derive reference from uninterpreted matte`
- fragment `\operatorname{Rep}{\beta,\ell}`: NOT-A-QUOTE; normalised LaTeX rewrite of source text (subscripts/operators flattened); substantive text occurs at source lines [149]

### staging line 215, citation `:743` -> NOT-A-QUOTE

- cited line 743 starts: `\tag{N}`
- fragment `d\equiv\ell c`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 215, citation `:746` -> NOT-A-QUOTE

- cited line 746 starts: `The equivalence is structural at the stated grain, not string equality or similarity. Forgotten prior understanding belongs to \(R_{<e}\) when the claim is firs`
- fragment `d\equiv\ell c`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 215, citation `:746` -> NOT-A-QUOTE

- cited line 746 starts: `The equivalence is structural at the stated grain, not string equality or similarity. Forgotten prior understanding belongs to \(R_{<e}\) when the claim is firs`
- fragment `d\equiv\ell c`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 216, citation `:617` -> RESOLVED-BY-SIBLING

- cited line 617 starts: `\tag{K1}`
- fragment `\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal Ec,p\delta)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The alleged defect must concern the stated target and respect`: RESOLVED-BY-SIBLING; sibling citation `:620`; occurs at source lines [620]

### staging line 216, citation `:613-618` -> RESOLVED-BY-SIBLING

- cited line 613 starts: `\[`
- fragment `\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal Ec,p\delta)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The alleged defect must concern the stated target and respect`: RESOLVED-BY-SIBLING; sibling citation `:620`; occurs at source lines [620]

### staging line 216, citation `:620` -> NOT-A-QUOTE

- cited line 620 starts: `where \(\mathcal E_c\) is the criticism's interpreted structural account. The alleged defect must concern the stated target and respect. A counterexample to a u`
- fragment `\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal Ec,p\delta)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 216, citation `:620` -> NOT-A-QUOTE

- cited line 620 starts: `where \(\mathcal E_c\) is the criticism's interpreted structural account. The alleged defect must concern the stated target and respect. A counterexample to a u`
- fragment `\operatorname{Bearing}(c,z,p)\iff\operatorname{Account}(\mathcal Ec,p\delta)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 220, citation `:638` -> RESOLVED-BY-SIBLING

- cited line 638 starts: `Standing is the system's enacted permission to use a content in a particular application and respect. It may be explicit or inexplicit. An appraisal can change `
- fragment `\operatorname{Live}j`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `not automatically machine-maintainable`: RESOLVED-BY-SIBLING; sibling citation `FW5:640`; occurs at source lines [640]

### staging line 220, citation `:642` -> RESOLVED-BY-SIBLING

- cited line 642 starts: `For an argument application \(u\), let \(\operatorname{Prem}(u)\) be its declared essential premises, including interpretation and scope premises. Let \(\operat`
- fragment `not automatically machine-maintainable`: RESOLVED-BY-SIBLING; sibling citation `FW5:640`; occurs at source lines [640]

### staging line 220, citation `:650` -> RESOLVED-BY-SIBLING

- cited line 650 starts: `\tag{K2}`
- fragment `\operatorname{Live}j`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `not automatically machine-maintainable`: RESOLVED-BY-SIBLING; sibling citation `FW5:640`; occurs at source lines [640]

### staging line 220, citation `FW5:640` -> NOT-A-QUOTE

- cited line 640 starts: `A source's appearance in a prompt is a delivery fact. A named field asking for a criticism is an invitation fact. Actual use of the source as a premise, actual `
- fragment `\operatorname{Live}j`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 224, citation `:162` -> RESOLVED-BY-SIBLING

- cited line 162 starts: `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}_E\), and an interpretation of its active commitments. `
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `a specified set-theoretic operation on the relevant organization`: RESOLVED-BY-SIBLING; sibling citation `:125`; occurs at source lines [125]
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The answer follows by evaluating the anchored organization under its declared independent boundary conditions`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]

### staging line 224, citation `:128-130` -> RESOLVED-BY-SIBLING

- cited line 128 starts: `\operatorname{Ans}_p(a,b)`
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}E\), and an interpretation of its active commitments.`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `a specified set-theoretic operation on the relevant organization`: RESOLVED-BY-SIBLING; sibling citation `:125`; occurs at source lines [125]
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The answer follows by evaluating the anchored organization under its declared independent boundary conditions`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 224, citation `:125` -> RESOLVED-BY-SIBLING

- cited line 125 starts: `The query operator \(\mathcal Q\) is a specified set-theoretic operation on the relevant organization, its solutions, and, where needed, its component structure`
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}E\), and an interpretation of its active commitments.`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The answer follows by evaluating the anchored organization under its declared independent boundary conditions`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 224, citation `:210` -> RESOLVED-BY-SIBLING

- cited line 210 starts: `**Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent boundary conditions. The target answer is`
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}E\), and an interpretation of its active commitments.`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `a specified set-theoretic operation on the relevant organization`: RESOLVED-BY-SIBLING; sibling citation `:125`; occurs at source lines [125]
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 224, citation `:162` -> RESOLVED-BY-SIBLING

- cited line 162 starts: `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}_E\), and an interpretation of its active commitments. `
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `a specified set-theoretic operation on the relevant organization`: RESOLVED-BY-SIBLING; sibling citation `:125`; occurs at source lines [125]
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The answer follows by evaluating the anchored organization under its declared independent boundary conditions`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]

### staging line 224, citation `:202` -> RESOLVED-BY-SIBLING

- cited line 202 starts: `\operatorname{Ans}_E(\tau(a),\sigma(b))`
- fragment `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}E\), and an interpretation of its active commitments.`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `a specified set-theoretic operation on the relevant organization`: RESOLVED-BY-SIBLING; sibling citation `:125`; occurs at source lines [125]
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The answer follows by evaluating the anchored organization under its declared independent boundary conditions`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]

### staging line 224, citation `:201-205` -> RESOLVED-BY-SIBLING

- cited line 201 starts: `\[`
- fragment `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}E\), and an interpretation of its active commitments.`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `a specified set-theoretic operation on the relevant organization`: RESOLVED-BY-SIBLING; sibling citation `:125`; occurs at source lines [125]
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The answer follows by evaluating the anchored organization under its declared independent boundary conditions`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]

### staging line 224, citation `:162` -> RESOLVED-BY-SIBLING

- cited line 162 starts: `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}_E\), and an interpretation of its active commitments. `
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `a specified set-theoretic operation on the relevant organization`: RESOLVED-BY-SIBLING; sibling citation `:125`; occurs at source lines [125]
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The answer follows by evaluating the anchored organization under its declared independent boundary conditions`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]

### staging line 224, citation `:128-130` -> RESOLVED-BY-SIBLING

- cited line 128 starts: `\operatorname{Ans}_p(a,b)`
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}E\), and an interpretation of its active commitments.`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `a specified set-theoretic operation on the relevant organization`: RESOLVED-BY-SIBLING; sibling citation `:125`; occurs at source lines [125]
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The answer follows by evaluating the anchored organization under its declared independent boundary conditions`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 224, citation `:125` -> RESOLVED-BY-SIBLING

- cited line 125 starts: `The query operator \(\mathcal Q\) is a specified set-theoretic operation on the relevant organization, its solutions, and, where needed, its component structure`
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}E\), and an interpretation of its active commitments.`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The answer follows by evaluating the anchored organization under its declared independent boundary conditions`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 224, citation `:210` -> RESOLVED-BY-SIBLING

- cited line 210 starts: `**Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent boundary conditions. The target answer is`
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}E\), and an interpretation of its active commitments.`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `a specified set-theoretic operation on the relevant organization`: RESOLVED-BY-SIBLING; sibling citation `:125`; occurs at source lines [125]
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `Equations (F) and (C) are applied at the stated abstraction and scope`: RESOLVED-BY-SIBLING; sibling citation `:197`; occurs at source lines [197]
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 224, citation `:197` -> RESOLVED-BY-SIBLING

- cited line 197 starts: `Component surgeries must commute with their anchors. Replacing an explanatory component cannot be interpreted as changing an unrelated part of the target solely`
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `An explanatory candidate for \(p\) supplies an organization \(E\), an answer profile \(\operatorname{Ans}E\), and an interpretation of its active commitments.`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `a specified set-theoretic operation on the relevant organization`: RESOLVED-BY-SIBLING; sibling citation `:125`; occurs at source lines [125]
- fragment `\operatorname{Ans}E=\mathcal Q(E,\cdot,\cdot)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `The answer follows by evaluating the anchored organization under its declared independent boundary conditions`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 291, citation `:123` -> NOT-A-QUOTE

- cited line 123 starts: `The target is \(D\). The scope \(\Sigma\subseteq A\times B\) fixes which edits and boundary conditions are in the claim. The distinguished baseline is \((1,b_0)`
- fragment `Weakens the claim that falling recurrence would confirm c1 and rising recurrence would refute it; the test has lower discriminating power than the account implies`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `quoted verbatim from the record`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 343, citation `:123` -> RESOLVED-BY-SIBLING

- cited line 123 starts: `The target is \(D\). The scope \(\Sigma\subseteq A\times B\) fixes which edits and boundary conditions are in the claim. The distinguished baseline is \((1,b_0)`
- fragment `no compatible realization`: RESOLVED-BY-SIBLING; sibling citation `:212`; occurs at source lines [212]

### staging line 343, citation `:609` -> RESOLVED-BY-SIBLING

- cited line 609 starts: `A criticism has a represented target \(z\), an alleged defect \(\delta\), grounds \(g\), and a proposed connection from \(g\) to \(\delta\) relative to a questi`
- fragment `no compatible realization`: RESOLVED-BY-SIBLING; sibling citation `:212`; occurs at source lines [212]

### staging line 344, citation `:123` -> RESOLVED-BY-SIBLING

- cited line 123 starts: `The target is \(D\). The scope \(\Sigma\subseteq A\times B\) fixes which edits and boundary conditions are in the claim. The distinguished baseline is \((1,b_0)`
- fragment `a missing distinction`: RESOLVED-BY-SIBLING; sibling citation `:609`; occurs at source lines [609]

### staging line 345, citation `:123` -> NOT-A-QUOTE

- cited line 123 starts: `The target is \(D\). The scope \(\Sigma\subseteq A\times B\) fixes which edits and boundary conditions are in the claim. The distinguished baseline is \((1,b_0)`
- fragment `bridge-strained`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 451, citation `FW5:1372` -> RESOLVED-BY-SIBLING

- cited line 1372 starts: `The explicit representation interpretation is not eliminated. If the fidelity and integration conditions admit a system whose apparent reasons are merely discon`
- fragment `\mathsf{FW5}`: RESOLVED-BY-SIBLING; sibling citation `:1192`; occurs at source lines [1192]

### staging line 487, citation `:1519` -> NOT-A-QUOTE

- cited line 1519 starts: ``
- fragment `material-occurrence-02.json`: NOT-A-QUOTE; contains a repository file path produced by the audit, not source text
- fragment `no finishreason`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 490, citation `:82` -> NOT-A-QUOTE

- cited line 82 starts: ``
- fragment `occurrence-02/plan.json`: NOT-A-QUOTE; contains a repository file path produced by the audit, not source text

### staging line 617, citation `:125` -> NOT-A-QUOTE

- cited line 125 starts: `The query operator \(\mathcal Q\) is a specified set-theoretic operation on the relevant organization, its solutions, and, where needed, its component structure`
- fragment `\operatorname{Ans}p(a,b)=\mathcal Q(D,a,b)`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 626, citation `:1402` -> NOT-A-QUOTE

- cited line 1402 starts: `All four Boolean input assignments were checked for the parallel and priority constructions. Their endpoint outputs agree, while the active second route differs`
- fragment `\operatorname{Ans}E(\tau(a),\sigma(b))`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 626, citation `:205` -> NOT-A-QUOTE

- cited line 205 starts: `\tag{A}`
- fragment `\operatorname{Ans}E(\tau(a),\sigma(b))`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 666, citation `:210` -> NOT-A-QUOTE

- cited line 210 starts: `**Non-circular dependence.** The answer follows by evaluating the anchored organization under its declared independent boundary conditions. The target answer is`
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 666, citation `:197` -> RESOLVED-BY-SIBLING

- cited line 197 starts: `Component surgeries must commute with their anchors. Replacing an explanatory component cannot be interpreted as changing an unrelated part of the target solely`
- fragment `the anchored organization`: RESOLVED-BY-SIBLING; sibling citation `:210`; occurs at source lines [210]
- fragment `\operatorname{Ans}E`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

### staging line 797, citation `:1372` -> CANDIDATE

- cited line 1372 starts: `The explicit representation interpretation is not eliminated. If the fidelity and integration conditions admit a system whose apparent reasons are merely discon`
- fragment `Representation and apparent reason use`: CANDIDATE; fragment occurs in the source but not at any line cited by this staging line; occurs at source lines [1370]

### staging line 834, citation `:912` -> RESOLVED-BY-SIBLING

- cited line 912 starts: `An information variable is, in the constructor-theoretic treatment, a clonable computation variable. Computation variables are characterized through possible pe`
- fragment `standing-bearing`: RESOLVED-BY-SIBLING; sibling citation `:1320`; occurs at source lines [1320]

### staging line 834, citation `:1005` -> RESOLVED-BY-SIBLING

- cited line 1005 starts: `for this physical attribution, displaying the realization ecology \(\mathcal E\): information-bearing media, interpreting or executing vehicles, resources, repa`
- fragment `standing-bearing`: RESOLVED-BY-SIBLING; sibling citation `:1320`; occurs at source lines [1320]

### staging line 834, citation `:1320` -> RESOLVED-BY-SIBLING

- cited line 1320 starts: `A fixed implementation does not, merely through being fixed, exclude some explanatory domain. Its represented programs or procedures may support extension. Conv`
- fragment `information-bearing`: RESOLVED-BY-SIBLING; sibling citation `:912`; occurs at source lines [912, 1005]

### staging line 845, citation `:622` -> NOT-A-QUOTE

- cited line 622 starts: `A criticism occurrence can exist when (K1) is false. Its grounds may be mistaken, its target misidentified, its inference invalid, or its relevance wrong. A mer`
- fragment `A criticism occurrence can exist when (K1) is false… It can become grounds for a criticism when an organization represents how it bears on a target.`: NOT-A-QUOTE; A001 audit label (e.g. account#cN, D-number, F-number), not source text

### staging line 847, citation `:893` -> CANDIDATE

- cited line 893 starts: `\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A`
- fragment `states that a reason bears on a work in an aesthetic respect`: RESOLVED-BY-SIBLING; sibling citation `:896`; occurs at source lines [896]
- fragment `\operatorname{Bearing}(c,z,p)`: CANDIDATE; fragment occurs in the source but not at any line cited by this staging line; occurs at source lines [614]

### staging line 847, citation `:896` -> CANDIDATE

- cited line 896 starts: `states that a reason bears on a work in an aesthetic respect. \(\mathcal Rsn\) is a set of reason contents; \(\mathcal V_A\) is a set of aesthetic respects, not`
- fragment `\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal VA`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Bearing}(c,z,p)`: CANDIDATE; fragment occurs in the source but not at any line cited by this staging line; occurs at source lines [614]

### staging line 847, citation `:893` -> CANDIDATE

- cited line 893 starts: `\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A`
- fragment `states that a reason bears on a work in an aesthetic respect`: RESOLVED-BY-SIBLING; sibling citation `:896`; occurs at source lines [896]
- fragment `\operatorname{Bearing}(c,z,p)`: CANDIDATE; fragment occurs in the source but not at any line cited by this staging line; occurs at source lines [614]

### staging line 847, citation `:896` -> CANDIDATE

- cited line 896 starts: `states that a reason bears on a work in an aesthetic respect. \(\mathcal Rsn\) is a set of reason contents; \(\mathcal V_A\) is a set of aesthetic respects, not`
- fragment `\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal VA`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Bearing}(c,z,p)`: CANDIDATE; fragment occurs in the source but not at any line cited by this staging line; occurs at source lines [614]

### staging line 847, citation `:896` -> CANDIDATE

- cited line 896 starts: `states that a reason bears on a work in an aesthetic respect. \(\mathcal Rsn\) is a set of reason contents; \(\mathcal V_A\) is a set of aesthetic respects, not`
- fragment `\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal VA`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording
- fragment `\operatorname{Bearing}(c,z,p)`: CANDIDATE; fragment occurs in the source but not at any line cited by this staging line; occurs at source lines [614]

### staging line 849, citation `:1182` -> RESOLVED-BY-SIBLING

- cited line 1182 starts: `Critical bearing is accounting for the specified defect question. Reason use is a representation-preserving map into an active response suborganization. Use and`
- fragment `Defined relations and dependence order`: RESOLVED-BY-SIBLING; sibling citation `:1178`; occurs at source lines [1178]

### staging line 849, citation `:1178` -> RESOLVED-BY-SIBLING

- cited line 1178 starts: `## Defined relations and dependence order`
- fragment `Critical bearing is accounting for the specified defect question.`: RESOLVED-BY-SIBLING; sibling citation `:1182`; occurs at source lines [1182]

### staging line 1006, citation `:620` -> RESOLVED-BY-SIBLING

- cited line 620 starts: `where \(\mathcal E_c\) is the criticism's interpreted structural account. The alleged defect must concern the stated target and respect. A counterexample to a u`
- fragment `An observer may lack the data needed to establish the witness. That makes the attribution unresolved; it does not prove either understanding or its absence`: RESOLVED-BY-SIBLING; sibling citation `FW5:634`; occurs at source lines [634]

### staging line 1137, citation `:1206` -> NOT-A-QUOTE

- cited line 1206 starts: `The result does not apply to arbitrary compression, loss of event identity, a changed boundary, or a coarsening that identifies a relevant distinction. Those op`
- fragment `account#c1-c3`: NOT-A-QUOTE; A001 audit label (e.g. account#cN, D-number, F-number), not source text

### staging line 1138, citation `:1202` -> CANDIDATE

- cited line 1202 starts: `Suppose all carriers, component relations, role bindings, maps, histories, question contracts, and attribution indices are transported along bijections preservi`
- fragment `the stipulated bijections`: CANDIDATE; fragment occurs in the source but not at any line cited by this staging line; occurs at source lines [1206]

### staging line 1323, citation `:35-47` -> NOT-A-QUOTE

- cited line 35 starts: `## What “no gaps” can responsibly mean`
- fragment `campaign.sourceidentity()`: NOT-A-QUOTE; fragment occurs nowhere in the source and is staging-authored wording

## Candidates (off-by-N test)

### staging line 160, citation `:947` -> TAG-CONVENTION (distance -6 lines)

- sentence: **(CT2)** is the tag at **:947**
- citation as written: `:947`
- cited line starts: `\tag{CT2}`
- failed fragment: `## The retention fixed point`
- occurs at source line 941: `## The retention fixed point`
- cited line is a `\tag{...}` display-tag line: True; display body on preceding lines: True
- verdict: **TAG-CONVENTION**

### staging line 797, citation `:1372` -> OFF-BY-N (distance -2 lines)

- sentence: **Branch, recorded.** :1372 sits under "Representation and apparent reason use"
- citation as written: `:1372`
- cited line starts: `The explicit representation interpretation is not eliminated. If the fidelity and integration conditions admit a system whose apparent reasons are merely discon`
- failed fragment: `Representation and apparent reason use`
- occurs at source line 1370: `## Representation and apparent reason use`
- cited line is a `\tag{...}` display-tag line: False; display body on preceding lines: False
- verdict: **OFF-BY-N**

### staging line 847, citation `:893` -> UNRESOLVED (distance -279 lines)

- sentence: | **:893** *(display)* **/ :896** *(prose)* | the relation \(\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A\) is displayed at **:893**;
- citation as written: `:893`
- cited line starts: `\mathcal N\subseteq A\times K\times\mathcal Rsn\times\mathcal V_A`
- failed fragment: `\operatorname{Bearing}(c,z,p)`
- occurs at source line 614: `\operatorname{Bearing}(c,z,p)`
- cited line is a `\tag{...}` display-tag line: False; display body on preceding lines: False
- verdict: **UNRESOLVED**

### staging line 1138, citation `:1202` -> OFF-BY-N (distance +4 lines)

- sentence: **No E2 outcome bears on :1202.***
- citation as written: `:1202`
- cited line starts: `Suppose all carriers, component relations, role bindings, maps, histories, question contracts, and attribution indices are transported along bijections preservi`
- failed fragment: `the stipulated bijections`
- occurs at source line 1206: `The result does not apply to arbitrary compression, loss of event identity, a changed boundary, or a coarsening that identifies a relevant distinction. Those op`
- cited line is a `\tag{...}` display-tag line: False; display body on preceding lines: False
- verdict: **OFF-BY-N**

## Full lists

### OFF-BY-N

- staging line 797, citation `:1372`, fragment `Representation and apparent reason use`, distance -2
- staging line 1138, citation `:1202`, fragment `the stipulated bijections`, distance +4

### UNRESOLVED

- staging line 847, citation `:893`, fragment `\operatorname{Bearing}(c,z,p)`, distance -279

## Limit

This refinement locates where each fragment actually sits relative to the cited line; it cannot decide whether a cited line was *meant* to point at the `\tag{...}` line or at the display body above it -- that convention is an authorial question that only the staging author can settle.
