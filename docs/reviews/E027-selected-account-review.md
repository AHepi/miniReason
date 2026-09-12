# Review of the selected E027 SQL construction

The actual selected Mini account is sufficient to define a concrete, attributed use study. It is not an executed algorithm or a creativity finding. Its full public occurrence remains unchanged at `experiments/records/E027-sql-construction-continuation/mini-disabled/public-answer.txt`, SHA256 `b5fb115264eaff0a0466ea19012b58624a2669f95c4b6e47aab545c2074268c0`. The source contract is the frozen SQL001/E026 participant packet, with integer-or-NULL keys, legal full-row events and one initial database read.

Independent review agrees that §§2–4 supply a usable retained-state organization and most update operations. The correct bridge must record concrete decoding choices, preserve the candidate's uncertainties, and expose any supplied operation. An incomplete executable presentation does not invalidate prose as a conjecture.

| Candidate commitment | Attributed bridge reading |
|---|---|
| §2.1 Lrows | Current left-row IDs mapped to nullable integer keys |
| §2.2 Rrows | Current right-row IDs mapped to key and nullable value |
| §§2.3–2.4 key indexes | Non-NULL integer keys mapped to distinct left/right IDs; omitted buckets mean empty |
| §2.5 optional matchCount | Derive count from right-ID bucket; do not introduce independent redundant count state |
| §3 initialization | Read initial rows once, build declared maps/indexes and initial output bag |
| §4 signed deltas | Maintain an explicitly cached output bag; preserve multiplicity and declared state changes |
| §5 live-row/output invariants | Check retained-state meaning separately from immediate emitted output |

Using JSON null for SQL NULL, a canonical ordering for serialization, ID sets for indexes and a cached output bag are operator choices. They instantiate the proposal rather than prove it uniquely determines an executable language. Retaining complete row maps is expressly allowed by the source's retained-state exception. It is not unauthorized later access to the original database.

## The NULL-key deletion omission has two relevant readings

Section4.2 explicitly removes the output triple for a NULL-key left deletion. Its instruction to delete the row from Lrows is indented under the non-NULL branch. Executing only the listed branch operations leaves the deleted row in retained state, contrary to §2.1's definition of Lrows as live rows. Broader prose intent, including the heading “Delete from L” and live-row invariant, supports removing it uniformly. That operation must be attributed when made explicit; it must not be silently presented as an operation spelled out in the NULL branch.

The [exact diagnostic](../../experiments/diagnostics/E027-null-delete-interpretations/witness.json) starts with L={(1,NULL)}, empty R, then deletes that left row. SQLite's new output is empty. Both readings issue the correct immediate output delta. The literal branch reading retains the row; subsequently reconstructing the output from its retained rows wrongly restores the NULL triple. The uniform-removal reading has empty retained rows and reconstructs the correct result. The [checker](../../experiments/diagnostics/E027-null-delete-interpretations/check.py) reproduces this distinction without a provider call or candidate-code execution.

This establishes a specific written state-mutation omission under a declared reading. It does not establish that an LLM using the account will make the error, that the immediate output delta is wrong, or that the literal reading is the only legitimate reading. A model may infer the intended removal before criticism. The live use study must allow and record that outcome rather than force the omission to become a failure.

## Several reservations misdescribe the admitted task

Section7.4 calls integer-versus-text affinity and text collation a genuine gap. Textual keys are outside the specified integer-or-NULL domain. The Unicode value field is projected, not used in the join predicate. These reservations concern extensions of the task and do not establish in-domain insufficiency.

Section7.3 says using sets instead of multisets would be wrong. Sets of projected values would erase multiplicity, but sets of distinct right-row IDs retain separate occurrences with equal projected values. The actual rid-indexed design therefore permits ID sets. Section2's label “minimal” also lacks an irredundancy argument: the key indexes derive from row maps, although they support the intended access pattern. Neither reservation is a reason to replace the selected proposal.

The lack of a machine-checked proof, illegal-event behavior and concurrent snapshots do not independently defeat the offered account under the frozen legal sequential-event contract. No conclusion about historical novelty, explanatory bearing or recursive universality follows from this finite review.

## Consequence for the next study

E028 is being prepared as a distinct one-cycle use/criticism-return template. It will preserve the whole candidate, the exact initial state mapping, actual first use, actual criticism and branch-specific subsequent state. The first use must disclose inferred operations. The same actual criticism will be returned to one apply/use branch and archived outside the other's input route; the first use and criticism occurrences are shared, with replay identified rather than billed as new provider calls.

Fresh legal ID reuse, matching-row deletion and NULL-valued insertion will test the chosen state after return while protecting an unaffected key. If initial use already handles the omitted written operation, that is evidence about interpretation and cannot be relabeled criticism-induced repair. Identical outputs may mean criticism was unnecessary; changed outputs alone do not establish use of its intended reason. The experiment may retain, revise or suspend, and it does not claim a Mini advantage from this internal route comparison.
