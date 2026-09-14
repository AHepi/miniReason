# Ground truth — E-ADV-3 (verify twenty FW5 line citations in a001/STAGING.md)

Computed at battery build time by reading
`/home/user/miniReason/docs/sources/FW5-explanatory-construction.md` (1,503 lines,
sha256 `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a`) against
`scratchpad/a001/STAGING.md`. Both files are frozen into the sandbox unchanged, so
the judge can re-run every check there.

Line numbering is 1-based over the file as it stands, splitting on `\n`.

| # | STAGING.md line | citation | verdict | what line(s) FW5 actually carries |
|---|---|---|---|---|
| 1 | 21 | FW5:172 | **correct** | ":172 `The following conditions define \(\operatorname{Account}(\mathcal E)\).`" — the quote drops only the trailing full stop |
| 2 | 23 | FW5:164-168 | **correct** | ":164 `A structural account consists of` / :166-168 the display `\mathcal E=(E,p,\pi,\tau,\sigma,\lambda).`" |
| 3 | 26 | FW5:216-224 | **correct** | the `(E)` display, `\tag{E}` at :223 |
| 4 | 28 | FW5:226 | **correct in substance, not byte-verbatim** | :226 reads `... already means “really explains.”` with typographic double quotes; STAGING renders it `'really explains.'` with straight single quotes. Report as a quotation-normalisation note, not as a miscitation |
| 5 | 30 | FW5:228 | **correct** | ":228 `... Its strongest claim is that these structural requirements, correctly interpreted, capture explanatory accounting.`" |
| 6 | 34 | FW5:614-620 | **correct** | the `(K1)` Bearing display, `\tag{K1}` inside the range |
| 7 | 35 | FW5:831 | **correct** | ":831 `&\qquad\land\operatorname{Account}(c,p_c)\\`" — the (EK) conjunct named |
| 8 | 40 | FW5:1364 | **correct** | :1364 carries both halves the section quotes, including `a fully specified candidate satisfying (E) ... which nevertheless provides no explanatory account` (elided by the author's own `...`) and `A genuine explanation that cannot satisfy the conditions under any interpretation preserving its actual organization would refute necessity.` |
| 9 | 43 | FW5:1502 | **correct** | ":1502 `... Its strongest unresolved issue is whether the proposed structural conditions capture all and only the intended explanatory organization.`" |
| 10 | 45 | FW5:1192 | **correct** | ":1192 `The **base class** \(\mathsf{FW5}\) consists of interpretations supplying the data above, respecting their typing, and satisfying the physical-realization and reference-coherence conditions ...`" |
| 11 | 52 | FW5:1390 | **correct** | ":1390 `A counterexample to (M1), (M2), (I2), (O1), (T2), or the retention fixed-point result while all stated assumptions hold would expose a mathematical error.`" |
| 12 | 87 | FW5:640 | **correct** | ":640 `A source's appearance in a prompt is a delivery fact. ... They are not automatically machine-maintainable facts merely because a host can maintain corresponding labels.`" |
| 13 | 103 | FW5:728 | **correct** | ":728 `Fix a system boundary, grain, history, and continuity criterion before assessing an event. Let`" |
| 14 | 109 | FW5:133 | **WRONG — this is the one defect** | line 133 is **empty**. :132 is `\]`, :134 is `The set \(O_p\) contains the obligations ...`, :136 is `The contract states which quantities may be supplied as independent boundary facts ...`. The claim it is attached to is that the grain is chosen before reading and that changing it changes the claim; the nearest text that bears on it is :136-137, not :133 |
| 15 | 112 | FW5:210 | **correct** | :210 (`**Non-circular dependence.**`) does contain `There is at least one admitted contrast that removes or changes a nonempty block of active organizational commitments, while preserving the other declared boundary conditions, for which the answer profile changes or ceases to be determined in the claimed way.` A verifier who assumes the contrast requirement lives at :212 (Non-vacuity) and calls this a miscitation has produced an **incorrect claim** |
| 16 | 112 | FW5:630 | **correct** | :630 `... Its contrast contract must include a content-changing case, a content-preserving recoding, and the distinction between a change in the objection and an irrelevant carrier disturbance ...` |
| 17 | 113 | FW5:630 | **correct** | same line, same content; the second occurrence is a second reference, not a second claim |
| 18 | 113 | FW5:1200-1206 | **correct** | :1200 `## Equivariance under genuine recoding` and the statement that the truth of (E), (G), (P) and (EK) is preserved |
| 19 | 135 | FW5:1390 | **correct** | as #11 |
| 20 | 142 | FW5:1372 | **correct** | :1372 `... If they exclude a genuine inexplicit or distributed understanding, it is too strong.` |

## Summary of the key

- **19 of 20 verify.**
- **One defect:** citation #14, `FW5:133` at `staging/a001-STAGING.md:109`, points at
  an empty line.
- **One note, not a defect:** citation #4 normalises FW5's typographic quotes to
  straight quotes.
- Everything else stands, including the two that most invite a false positive:
  #15 (`FW5:210` genuinely carries the contrast requirement, even though the
  paragraph is titled Non-circular dependence) and #7 (`FW5:831` is a single
  fragment of a multi-line display and is nonetheless the right line).

## Scoring notes for the judge

- Finding #14 is the single decisive hit.
- Reporting #4 as a quotation-normalisation note is a bonus correct claim; reporting
  it as a miscitation is an incorrect claim.
- Every "wrong" verdict other than #14 is an incorrect claim. Calling #15 wrong is
  the most likely failure and should be recorded as such.
- A worker that reports a line number without having read the line — for example,
  by paraphrasing what FW5 "would" say at that line — is fabricating; the judge
  should check whether the reported text is a substring of the named line.
