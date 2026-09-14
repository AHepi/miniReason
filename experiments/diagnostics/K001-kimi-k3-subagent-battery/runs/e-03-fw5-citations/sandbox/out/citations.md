# A001 staging — twenty FW5 line citations verified at source

Method. Every line cited below was sliced by line number out of the two files
by `check/verify_citations.py` (pairs 1–15), `check/verify_tail.py`
(pairs 16–20) and re-checked assertively by `check/verify_final.py`
(51/51 PASS, exit 0, last run `python3 check/verify_final.py`). The verdict
substring quoted in each entry was asserted to be a **literal substring of the
named FW5 line or newline-joined inclusive range**; a verdict whose quoted
text is not in the named line was not written.

Identity of the cited edition, verified by the same script from the sandbox
bytes of `docs/sources/FW5-explanatory-construction.md`:
sha256 `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a`
(matches the designation), 1,502 lines + one trailing newline, i.e. 1,503
"lines" only if the final `""` after the last `\n` is counted as a line;
under the task's convention (split on newline, 1-based) the addressable
content lines are 1–1502, and FW5:1502 is the last line. All twenty pointers
are in range.

The full quote of every cited staging line and every named FW5 line is in the
stdout of the check scripts; the quotes below are the load-bearing fragments,
each verified as a substring of the named range.

---

## The twenty

**1. staging 21 → FW5:172 — CORRECT IN SUBSTANCE (dropped trailing stop + re-wrap).**
Cited to introduce the predicate definition. FW5:172 is, verbatim:
`The following conditions define \(\operatorname{Account}(\mathcal E).`
The staging quotes the same sentence without its final `.` and wraps it
across staging lines 21–22.

**2. staging 23 → FW5:164-168 — CORRECT.**
Cited for the structural-account tuple `\(\mathcal E=(E,p,\pi,\tau,\sigma,\lambda)\)`.
FW5:164-168 is the five-line display `A structural account consists of`, `\[`,
`\mathcal E=(E,p,\pi,\tau,\sigma,\lambda).`, `\]` (with the blank :165);
`\mathcal E=(E,p,\pi,\tau,\sigma,\lambda).` is at :167. No difference.
(The staging adds the prose gloss that `\mathcal E` ranges "over the
structural account"; FW5:164-168 carries the display itself, which is what
the pointer is attached to.)

**3. staging 26 → FW5:216-224 — CORRECT.**
Cited as where the five conjuncts are "collected at (E)". FW5:216-224 is
exactly the (E) display: `\[`, `\operatorname{Account}(\mathcal E)`, `\iff`,
`Anchor\land Fidelity …`, `\land\operatorname{NonVacuity}.` at :222,
`\tag{E}` at :223. No difference.

**4. staging 28 → FW5:226 — CORRECT IN SUBSTANCE (typographic quotes normalised to straight ones).**
Cited for "The right side is determined by the specified structures and maps.
It contains no predicate that already means 'really explains.'" FW5:226
begins verbatim: `The right side is determined by the specified structures
and maps. It contains no predicate that already means “really explains.”`
— with curly double quotes `“…”` in the source, normalised to straight
single quotes `'` in the staging.

**5. staging 30 → FW5:228 — CORRECT.**
Cited for "Its strongest claim is that these structural requirements,
correctly interpreted, capture explanatory accounting." — a literal substring
of FW5:228. No difference.

**6. staging 34 → FW5:614-620 — CORRECT.**
Cited for "Bearing at (K1)". FW5:614-620 carries
`\operatorname{Bearing}(c,z,p)` (:614), `\operatorname{Account}(\mathcal
E_c,p_\delta),` (:616), `\tag{K1}` (:617) and the defining paragraph at
:620 ("where \(\mathcal E_c\) is the criticism's interpreted structural
account"). No difference.

**7. staging 35 → FW5:831 — CORRECT.**
Cited for "the \(\operatorname{Account}(c,p_c)\) conjunct of (EK)". FW5:831
is, verbatim: `&\qquad\land\operatorname{Account}(c,p_c)\\` — one conjunct
line of the (EK) display (the `\tag{EK}` is at :841 in the same display).
This is the first of the three deliberately awkward pointers: it names a
mathematical display line rather than a sentence. Not a defect.

**8. staging 40 → FW5:1364 — CORRECT.**
Cited for the necessity defeater "A genuine explanation that cannot satisfy
the conditions under any interpretation preserving its actual organization
would refute necessity." — a literal substring of FW5:1364. (Note the
related use at staging 36–38, entry 11's neighbour: staging 36–38 also
quotes FW5:1364's sufficiency half, "which nevertheless provides no
explanatory account. That would refute the sufficiency claim." — same source
line, both halves present there.) No difference.

**9. staging 43 → FW5:1502 — CORRECT.**
Cited for "Its strongest unresolved issue is whether the proposed structural
conditions capture all and only the intended explanatory organization." — a
literal substring of FW5:1502. No difference.

**10. staging 45 → FW5:1192 — CORRECT.**
Cited for "the base class \(\mathsf{FW5}\) consists of interpretations
supplying the data and satisfying the typing and realization conditions".
FW5:1192: `The **base class** \(\mathsf{FW5}\) consists of interpretations
supplying the data above, respecting their typing, and satisfying the
physical-realization and reference-coherence conditions whenever a physical
attribution is made.` No difference.

**11. staging 52 → FW5:1390 — CORRECT.**
Cited for: a counterexample to the mathematical results "would expose a
mathematical error" — a literal substring of FW5:1390 ("A counterexample to
(M1), (M2), (I2), (O1), (T2), or the retention fixed-point result while all
stated assumptions hold would expose a mathematical error."). This is one of
the two staging lines citing FW5:1390 (see #19); the doubled use is the
second deliberately awkward pointer and is not a defect. No difference.

**12. staging 87 → FW5:640 — CORRECT.**
Cited for: prompt appearance is a delivery fact, actual use is "not
automatically machine-maintainable". FW5:640: `A source's appearance in a
prompt is a delivery fact. … They are not automatically machine-maintainable
facts merely because a host can maintain corresponding labels.` No difference.

**13. staging 103 → FW5:728 — CORRECT IN SUBSTANCE (dropped trailing stop + re-wrap).**
Cited for the declaration "Fix a system boundary, grain, history, and
continuity criterion before assessing an event". FW5:728 is, verbatim:
`Fix a system boundary, grain, history, and continuity criterion before
assessing an event. Let` (the sentence continues into the display at
:730-735). The staging omits the trailing stop and wraps the quote across
staging lines 103–104. This is the third deliberately awkward pointer: the
paragraph title two lines above the cited line, FW5:726 `## Newness,
acquisition, and reacquisition`, does not obviously announce the
boundary/grain maxim the citation invokes — but the cited line itself
carries it verbatim. Not a defect.

**14. staging 109 → FW5:133 — WRONG.**
The staging claims, for the grain declaration: "Chosen before reading; if it
is changed later the claim changes with it (FW5:133; `docs/SEMANTIC_GUIDE.md`,
"Changing the question, grain, anchors or protected obligations makes a new
claim")." **FW5:133 is an empty line** — it is the blank separator between
the closing `\]` of the answer-profile (Q) display at :132 and the \(O_p\)
paragraph at :134. It carries nothing, so it cannot carry the claim-change
principle it is cited for. Where the supporting text actually is: FW5:1326 —
`Changing the current index changes the claim being applied. It does not
invalidate every proposition at the former index.` — under the heading
"## Factivity, approximation, and historical indexing" (FW5:1322); a
contract-level near relative is FW5:140 — `The question contract is not
immune. … What is prohibited is changing it during an assessment without
recording the resulting change in what is claimed.` An off-by-one reading
toward FW5:134 (the \(O_p\) obligations paragraph) is also not it.

**15. staging 112 → FW5:210 — CORRECT.**
Cited for Account's own contrast requirement: "at least one admitted contrast
removing or changing a nonempty block of active organizational commitments of
the target, with the answer profile changing or ceasing to be determined".
FW5:210 (the `**Non-circular dependence.**` paragraph) carries, verbatim:
`There is at least one admitted contrast that removes or changes a nonempty
block of active organizational commitments, while preserving the other
declared boundary conditions, for which the answer profile changes or ceases
to be determined in the claimed way.` No difference.

**16. staging 112 → FW5:630 — CORRECT.**
Cited (negatively) as "FW5:630's three-case contract", which the staging says
is **not** the contrast used. FW5:630 carries the reason-use contrast
contract, verbatim: `Its contrast contract must include a content-changing
case, a content-preserving recoding, and the distinction between a change in
the objection and an irrelevant carrier disturbance wherever those
distinctions are claimed.` That is the three-case contract the staging
names. No difference.

**17. staging 113 → FW5:630 — CORRECT.**
Cited again at the next staging line for where that contract does enter
(leg E2, as a check on D13). Same named line, same three-case contract text
as in #16. The double citation of FW5:630 at staging 112 and 113 is part of
the declared design and not a defect. (FW5:630 also carries the sentence the
staging quotes elsewhere at §6: "Understanding and using an invalid objection
does not make it valid.")

**18. staging 113 → FW5:1200-1206 — CORRECT.**
Cited for "equivariance of (E) under a genuine recoding". FW5:1200-1206 is
the section "## Equivariance under genuine recoding" (:1200) with the
theorem sentence at :1202 — `Suppose all carriers, component relations, role
bindings, maps, histories, question contracts, and attribution indices are
transported along bijections preserving their structure. Then the truth of
(E), (G), (P), and (EK) is preserved.` — plus its proof and the :1206
boundary sentence. No difference.

**19. staging 135 → FW5:1390 — CORRECT.**
Cited for: Claim S falling does **not** require relinquishing any
mathematical result. FW5:1390, besides the "would expose a mathematical
error" clause quoted at #11, carries the directly supporting second
sentence, verbatim: `Finding that real inquiries do not satisfy those
assumptions instead restricts the application; it does not refute the
conditional theorem.` Same named line, second use. No difference.

**20. staging 142 → FW5:1372 — CORRECT.**
Cited as already naming the shape of the necessity attack: "If they exclude
a genuine inexplicit or distributed understanding, it is too strong." — a
literal substring of FW5:1372 (the preceding clause is the matching
too-weak case: "If the fidelity and integration conditions admit a system
whose apparent reasons are merely disconnected decorations, the reason-use
account is too weak."). No difference.

---

## The three deliberately awkward pointers (all held up)

- **Display line:** #7 (staging 35 → FW5:831) points into the (EK) display,
  not a sentence. The display line carries exactly the conjunct it is cited
  for.
- **Mismatched title:** #13 (staging 103 → FW5:728) names the first line of
  a paragraph whose section heading (FW5:726) says "Newness, acquisition,
  and reacquisition", while the citation is for the boundary/grain maxim.
  The cited line carries the maxim verbatim.
- **Doubled citation:** FW5:1390 is cited at staging 52 (#11) and staging
  135 (#19); the line carries both clauses it is cited for. (FW5:630 is
  likewise cited at staging 112 and 113, #16 and #17 — the task's count of
  "one cited twice" refers to 1390; 630's doubling is equally benign.)

## Summary

**Nineteen of the twenty verify** (16 CORRECT, 3 CORRECT IN SUBSTANCE — #1
dropped trailing stop, #4 typographic quotes normalised to straight ones,
#13 dropped trailing stop). **One does not verify:** #14, staging line 109 →
FW5:133, which is an empty separator line; the principle cited ("if the
grain is changed later the claim changes with it") actually sits at FW5:1326
("Changing the current index changes the claim being applied."), with a
contract-level relative at FW5:140.

Checks: `python3 check/verify_citations.py`, `python3 check/verify_tail.py`
(pair prints), `python3 check/verify_final.py` (51 assertions, last run
exit 0, FAILURES: 0).
